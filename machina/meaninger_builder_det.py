#!/usr/bin/env python3
"""
MEANINGER BUILDER — DETERMINISTIC PASS v1.0
No models. Rule-based meaning extraction + valence bucketing.
Outputs:
  - meaninger_understand.txt (full entries with buckets)
  - meaninger_meanings.txt (word|meaning only, no context)
  - understand_pos.txt / understand_neg.txt / understand_neu.txt (bucketed)
"""

import json, os, re, signal, sys, time
from collections import Counter
from typing import Dict, Any, Tuple

# =============================================================================
# CONFIG
# =============================================================================
STATE_FILE      = "meaninger_state.json"
UNDERSTAND_FILE = "meaninger_understand.txt"
MEANINGS_FILE   = "meaninger_meanings.txt"
POS_FILE        = "understand_pos.txt"
NEG_FILE        = "understand_neg.txt"
NEU_FILE        = "understand_neu.txt"
DICT_FILE       = "meaninger_dict.jsonl"
LOG_FILE        = "meaninger_run.log"

SEP = "|"
MAX_ENTRIES = int(os.environ.get("MAX_ENTRIES", 0))

_state: Dict[str, Any] = {}
_shutdown = False

# =============================================================================
# SIGNALS
# =============================================================================
def _sig(signum, frame):
    global _shutdown
    _shutdown = True
    _save_state()
    print("\n[SHUTDOWN] Saved.")
    sys.exit(0)

signal.signal(signal.SIGINT, _sig)
signal.signal(signal.SIGTERM, _sig)

# =============================================================================
# STATE
# =============================================================================
def _save_state():
    tmp = STATE_FILE + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(_state, f)
    os.replace(tmp, STATE_FILE)

def _load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"last_idx": -1, "global_freq": {}, "start": time.time(), "v": "det1.0"}

# =============================================================================
# LOAD DICTIONARY
# =============================================================================
def _load_dict():
    entries = []
    with open(DICT_FILE, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                entries.append(json.loads(line))
    return entries

# =============================================================================
# DETERMINISTIC MEANING EXTRACTION
# =============================================================================
STOP_WORDS = {
    "the", "a", "an", "to", "of", "in", "on", "at", "by", "for", "with",
    "from", "as", "is", "are", "was", "were", "be", "been", "being",
    "have", "has", "had", "do", "does", "did", "will", "would", "could",
    "should", "may", "might", "can", "shall", "it", "its", "this", "that",
    "these", "those", "i", "you", "he", "she", "we", "they", "them",
    "their", "there", "then", "than", "or", "and", "but", "if", "so",
    "not", "no", "yes", "up", "down", "out", "off", "over", "under",
    "again", "further", "then", "once", "here", "when", "where", "why",
    "how", "all", "each", "few", "more", "most", "other", "some", "such",
    "only", "own", "same", "so", "than", "too", "very", "just", "now"
}

def _extract_meaning(defin: str) -> str:
    """Extract first 3 content words from definition."""
    # Clean: remove parentheticals, backticks, extra punctuation
    cleaned = re.sub(r'\(.*?\)', '', defin)
    cleaned = cleaned.replace("`", "").replace("'", "")
    words = re.findall(r'[a-zA-Z]+', cleaned.lower())
    content = [w for w in words if w not in STOP_WORDS and len(w) > 2]
    # Return up to 3, joined by semicolons
    return ";".join(content[:3]) if content else "unknown"

# =============================================================================
# VALENCE DETECTOR (DETERMINISTIC)
# =============================================================================
NEGATIVE_TRIGGERS = {
    "not", "no", "without", "lack", "unable", "absence", "fail", "loss",
    "devoid", "exclusion", "negation", "negative", "deny", "denial",
    "refuse", "reject", "remove", "absent", "missing", "void", "empty",
    "destroy", "damage", "harm", "hurt", "injury", "pain", "suffer",
    "bad", "evil", "wrong", "false", "fake", "fraud", "lie", "cheat",
    "steal", "kill", "die", "death", "dead", "sick", "ill", "disease",
    "poison", "toxic", "waste", "rotten", "corrupt", "decay", "decline",
    "fall", "drop", "decrease", "reduce", "less", "fewer", "small",
    "weak", "poor", "low", "bottom", "under", "beneath", "below",
    "backward", "reverse", "oppose", "against", "anti", "counter",
    "dis", "un", "in", "non", "ab", "mal", "mis", "pseudo"
}

POSITIVE_TRIGGERS = {
    "able", "having", "possess", "capable", "presence", "include", "gain",
    "success", "advantage", "favorable", "good", "right", "true", "real",
    "help", "aid", "assist", "support", "care", "love", "like", "enjoy",
    "happy", "joy", "pleasure", "delight", "bliss", "cheer", "smile",
    "laugh", "fun", "play", "game", "win", "victory", "triumph",
    "strong", "power", "might", "force", "energy", "vigor", "health",
    "heal", "cure", "fix", "repair", "build", "create", "make", "grow",
    "rise", "increase", "more", "most", "many", "much", "large", "big",
    "high", "top", "above", "over", "up", "forward", "advance", "progress",
    "pro", "en", "co", "bene", "eu"
}

def _detect_valence(word: str, defin: str, meaning: str) -> str:
    """Return 'pos', 'neg', or 'neu' based on keyword scan."""
    text = f"{word} {defin} {meaning}".lower()
    words = set(re.findall(r'[a-zA-Z]+', text))

    neg_hits = len(words & NEGATIVE_TRIGGERS)
    pos_hits = len(words & POSITIVE_TRIGGERS)

    # Check prefixes on the word itself
    w = word.lower()
    neg_prefixes = ("un", "dis", "in", "non", "ab", "mal", "mis")
    pos_prefixes = ("pro", "en", "co", "bene")

    if any(w.startswith(p) for p in neg_prefixes):
        neg_hits += 1
    if any(w.startswith(p) for p in pos_prefixes):
        pos_hits += 1

    if neg_hits > pos_hits:
        return "neg"
    elif pos_hits > neg_hits:
        return "pos"
    else:
        return "neu"

# =============================================================================
# STATS ENGINE (same as before)
# =============================================================================
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

# =============================================================================
# CLEAN
# =============================================================================
def _clean(s: str) -> str:
    s = s.replace("|", "").replace("\n", " ").replace("\r", " ").strip()
    s = re.sub(r'\s+', ' ', s)
    return s

# =============================================================================
# BUILD ENTRY
# =============================================================================
def _build_entry(idx: int, word: str, defin: str, stats: tuple, meaning: str, valence: str) -> str:
    lf, L, vc, cc, vr = stats
    d_words = defin.split()[:8]
    d_compressed = "_".join(d_words)
    fields = [
        str(idx), _clean(word), _clean(d_compressed), lf, str(L), str(vc), str(cc), str(vr),
        meaning,
        valence,
        str(int(time.time()))
    ]
    return SEP.join(fields)

# =============================================================================
# MAIN
# =============================================================================
def main():
    global _state
    _state = _load_state()

    dictionary = _load_dict()
    total = len(dictionary)
    resume = _state["last_idx"] + 1
    target = total if MAX_ENTRIES == 0 else min(resume + MAX_ENTRIES, total)

    print(f"[RUN] Total: {total} | Resume: {resume} | Target: {target}")
    print(f"[RUN] DETERMINISTIC — zero model calls")
    print(f"[RUN] Ctrl+C = graceful stop. Restart resumes.\n")

    with open(LOG_FILE, "a", encoding="utf-8") as log:
        log.write(f"\n--- DET_START {int(time.time())} RESUME {resume}/{target} ---\n")

    pos_count = 0
    neg_count = 0
    neu_count = 0
    start_t = time.time()

    for idx in range(resume, target):
        if _shutdown:
            break

        entry = dictionary[idx]
        word = entry["w"]
        defin = entry["d"]

        # Deterministic processing
        stats = _stats(word, _state["global_freq"])
        meaning = _extract_meaning(defin)
        valence = _detect_valence(word, defin, meaning)

        # Build full entry
        line = _build_entry(idx, word, defin, stats, meaning, valence)
        with open(UNDERSTAND_FILE, "a", encoding="utf-8") as f:
            f.write(line + "\n")

        # Clean meaning file (word|meaning only)
        with open(MEANINGS_FILE, "a", encoding="utf-8") as f:
            f.write(f"{_clean(word)}|{meaning}\n")

        # Bucket file
        bucket_line = f"{_clean(word)}|{_clean(defin)}|{meaning}\n"
        if valence == "pos":
            with open(POS_FILE, "a", encoding="utf-8") as f:
                f.write(bucket_line)
            pos_count += 1
        elif valence == "neg":
            with open(NEG_FILE, "a", encoding="utf-8") as f:
                f.write(bucket_line)
            neg_count += 1
        else:
            with open(NEU_FILE, "a", encoding="utf-8") as f:
                f.write(bucket_line)
            neu_count += 1

        _state["last_idx"] = idx
        _save_state()

        with open(LOG_FILE, "a", encoding="utf-8") as log:
            log.write(f"{int(time.time())} {idx+1}/{target} {word} {valence}\n")

        if (idx + 1) % 1000 == 0:
            wpm = (idx + 1 - resume) / ((time.time() - start_t) / 60)
            print(f"[PROGRESS] {idx+1}/{target} | {wpm:.0f} words/min | pos:{pos_count} neg:{neg_count} neu:{neu_count}")

    print(f"\n[DONE] Last: {_state['last_idx']}")
    print(f"[BUCKETS] pos:{pos_count} neg:{neg_count} neu:{neu_count}")
    print(f"[FILES] {UNDERSTAND_FILE} | {MEANINGS_FILE} | {POS_FILE} | {NEG_FILE} | {NEU_FILE}")

if __name__ == "__main__":
    main()
