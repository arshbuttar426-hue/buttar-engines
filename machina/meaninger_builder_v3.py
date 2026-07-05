#!/usr/bin/env python3
import json, os, re, signal, sys, time
from collections import Counter
from typing import Dict, Any
import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
SESSION = requests.Session()

MODEL_SWARM = {
    "M": "gemma2:9b",
    "R": "qwen2.5-coder:1.5b",
    "E": "phi3.5:latest",
    "S": "qwen2:0.5b"
}

STATE_FILE      = "meaninger_state.json"
UNDERSTAND_FILE = "meaninger_understand.txt"
SCHEMA_FILE     = "meaninger_schema.key"
DICT_FILE       = "meaninger_dict.jsonl"
LOG_FILE        = "meaninger_run.log"

SEP = "|"
MAX_ENTRIES = int(os.environ.get("MAX_ENTRIES", 0))

_state: Dict[str, Any] = {}
_shutdown = False

def _sig(signum, frame):
    global _shutdown
    _shutdown = True
    _save_state()
    print("\n[SHUTDOWN] Saved.")
    sys.exit(0)

signal.signal(signal.SIGINT, _sig)
signal.signal(signal.SIGTERM, _sig)

def _save_state():
    tmp = STATE_FILE + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(_state, f)
    os.replace(tmp, STATE_FILE)

def _load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"last_idx": -1, "global_freq": {}, "start": time.time(), "v": "3.0"}

def _ensure_dict():
    if os.path.exists(DICT_FILE):
        return
    print("[INIT] Seeding dictionary...")
    import nltk
    try:
        nltk.data.find("corpora/wordnet")
    except LookupError:
        nltk.download("wordnet", quiet=True)
    from nltk.corpus import wordnet as wn
    seen = set()
    with open(DICT_FILE, "w", encoding="utf-8") as out:
        for syn in wn.all_synsets():
            word = syn.name().split(".")[0].replace("_", " ")
            defin = syn.definition()
            key = word.lower()
            if key not in seen:
                seen.add(key)
                out.write(json.dumps({"w": word, "d": defin}) + "\n")
    print(f"[INIT] {len(seen)} entries.")

def _load_dict():
    entries = []
    with open(DICT_FILE, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                entries.append(json.loads(line))
    return entries

def _ensure_schema():
    if os.path.exists(SCHEMA_FILE):
        return
    content = """# MEANINGER SCHEMA v3.0
# 0  | IDX | system | Entry index
# 1  | W   | system | Word
# 2  | D   | system | Definition (8 words max)
# 3  | LF  | python | Local letter freq
# 4  | L   | python | Length
# 5  | VC  | python | Vowel count
# 6  | CC  | python | Consonant count
# 7  | VR  | python | Vowel ratio
# 8  | M   | gemma2:9b | MEANING: 3 bridges
# 9  | R   | qwen2.5-coder:1.5b | REASONING: 2 keywords
# 10 | E   | phi3.5:latest | EMOTION: valence;metaphor
# 11 | S   | qwen2:0.5b | STRUCTURE: length;root_hint
# 12 | TS  | system | Unix timestamp
"""
    with open(SCHEMA_FILE, "w", encoding="utf-8") as f:
        f.write(content)

def _stats(word: str, global_freq: Dict) -> tuple:
    w = word.lower()
    local = Counter(c for c in w if c.isalpha())
    for ch, cnt in local.items():
        global_freq[ch] = global_freq.get(ch, 0) + cnt
    vowels = set("aeiou")
    vc = sum(local[c] for c in local if c in vowels)
    cc = sum(local[c] for c in local if c not in vowels)
    vr = round(vc / max(cc, 1), 3)
    lf = "".join(f"{c}{local[c]}" for c in sorted(local.keys()))
    return lf, len(w), vc, cc, vr

def _clean(s: str) -> str:
    s = s.replace("|", "").replace("\n", " ").replace("\r", " ").strip()
    s = re.sub(r'\s+', ' ', s)
    return s

def _extract(raw: str, role: str) -> str:
    raw = _clean(raw)
    if not raw or raw.startswith("ERR"):
        return "ERR_EMPTY"
    
    chunks = [c.strip() for c in raw.split(";") if c.strip()]
    chunks = [c for c in chunks if 2 <= len(c) <= 30]
    
    if role == "M":
        words = [c for c in chunks if " " not in c][:3]
        if len(words) >= 1:
            return ";".join(words[:3])
        return ";".join(chunks[:3]) if len(chunks) >= 1 else "ERR_FMT"
    
    elif role == "R":
        words = [c for c in chunks if " " not in c][:2]
        if len(words) >= 1:
            return ";".join(words[:2])
        return ";".join(chunks[:2]) if len(chunks) >= 1 else "ERR_FMT"
    
    elif role == "E":
        if chunks:
            val = chunks[0]
            if val in "+-0" and len(chunks) >= 2:
                return f"{val};{chunks[1][:40]}"
            for i, c in enumerate(chunks):
                if c in "+-0":
                    rest = " ".join(chunks[i+1:])[:40] if i+1 < len(chunks) else "neutral"
                    return f"{c};{rest}"
        return "0;neutral"
    
    elif role == "S":
        if chunks:
            if chunks[0].isdigit():
                hint = chunks[1][:30] if len(chunks) > 1 else "unknown"
                return f"{chunks[0]};{hint}"
            return ";".join(chunks[:3])
        return "ERR_FMT"
    
    return "ERR_FMT"

PROMPTS = {
    "M": "COMPRESSION CHIP. WORD:{word} DEF:{defin}. RULE: Output ONLY 3 related single-word concepts separated by semicolons. NO sentences. NO filler. Example: capability;skill;power",
    "R": "COMPRESSION CHIP. WORD:{word} DEF:{defin}. RULE: Output ONLY 2 contradiction keywords separated by semicolons. NO sentences. Example: intent;neglect",
    "E": "COMPRESSION CHIP. WORD:{word} DEF:{defin}. RULE: Output ONLY valence(+/-/0);short_metaphor separated by semicolons. NO sentences. Example: +;authority",
    "S": "COMPRESSION CHIP. WORD:{word} DEF:{defin}. RULE: Output ONLY word_length;root_hint separated by semicolons. NO sentences. Example: 4;Latin"
}

def _query(role: str, word: str, defin: str, timeout: int = 300) -> str:
    model = MODEL_SWARM[role]
    prompt = PROMPTS[role].format(word=word, defin=defin)
    
    def _call():
        try:
            r = SESSION.post(OLLAMA_URL, json={
                "model": model,
                "prompt": prompt,
                "stream": False,
                "options": {"temperature": 0.2, "num_predict": 50}
            }, timeout=timeout)
            r.raise_for_status()
            return r.json().get("response", "").strip()
        except requests.exceptions.ConnectionError:
            return "ERR_NO_OLLAMA"
        except Exception as e:
            return f"ERR_{type(e).__name__}"
    
    raw = _call()
    if not raw or raw.startswith("ERR"):
        time.sleep(2)
        raw = _call()
    return _extract(raw, role)

def _build_entry(idx: int, word: str, defin: str, stats: tuple, outputs: Dict[str, str]) -> str:
    lf, L, vc, cc, vr = stats
    d_words = defin.split()[:8]
    d_compressed = "_".join(d_words)
    fields = [
        str(idx), _clean(word), _clean(d_compressed), lf, str(L), str(vc), str(cc), str(vr),
        outputs.get("M", "ERR"), outputs.get("R", "ERR"), outputs.get("E", "ERR"), outputs.get("S", "ERR"),
        str(int(time.time()))
    ]
    return SEP.join(fields)

def main():
    global _state
    _state = _load_state()
    _ensure_dict()
    _ensure_schema()

    dictionary = _load_dict()
    total = len(dictionary)
    resume = _state["last_idx"] + 1
    target = total if MAX_ENTRIES == 0 else min(resume + MAX_ENTRIES, total)

    print(f"[RUN] Total: {total} | Resume: {resume} | Target: {target}")
    print(f"[RUN] MODELS: {MODEL_SWARM}")
    print(f"[RUN] SERIAL | 300s timeout | Ctrl+C stops\n")

    err_count = 0
    ok_count = 0
    start_t = time.time()

    for idx in range(resume, target):
        if _shutdown:
            break

        entry = dictionary[idx]
        word = entry["w"]
        defin = entry["d"]

        stats = _stats(word, _state["global_freq"])

        outputs = {}
        for role in ["M", "R", "E", "S"]:
            outputs[role] = _query(role, word, defin)
            if outputs[role].startswith("ERR"):
                err_count += 1
                print(f"    -> {role}:{MODEL_SWARM[role]} = {outputs[role]}")
            else:
                ok_count += 1

        line = _build_entry(idx, word, defin, stats, outputs)
        with open(UNDERSTAND_FILE, "a", encoding="utf-8") as f:
            f.write(line + "\n")

        _state["last_idx"] = idx
        _save_state()

        if (idx + 1) % 5 == 0:
            wpm = (idx + 1 - resume) / ((time.time() - start_t) / 60)
            err_rate = (err_count / max(ok_count + err_count, 1)) * 100
            print(f"[PROGRESS] {idx+1}/{target} | {wpm:.1f} words/min | errors: {err_rate:.1f}%")

    print(f"\n[DONE] Last: {_state['last_idx']}")
    print(f"[STATS] Errors: {err_count} | OK: {ok_count}")

if __name__ == "__main__":
    main()
