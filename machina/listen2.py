import os
import glob
import subprocess
import json
import numpy as np
import librosa
import whisper
from scipy.signal import medfilt

# ===== CONFIGURATION =====
FOLDER_PATH = os.path.expanduser("~/Desktop/GemmaAudio")
MODEL_NAME = "gemma4:e4b"               
WHISPER_MODEL = "small"                 
TEMP_WAV = os.path.expanduser("~/Desktop/GemmaAudio/proc_temp.wav")

# ===== FORENSIC DSP ENGINE =====
def extract_acoustic_features(wav_path):
    """
    Extracts objective acoustic anomalies. Strictly masked to true vocal activity.
    """
    y, sr = librosa.load(wav_path, sr=16000, mono=True)
    duration = len(y) / sr

    # 1. Base Energy & Noise Floor
    rms = librosa.feature.rms(y=y, frame_length=512, hop_length=256)[0]
    rms_db = 20 * np.log10(rms + 1e-6)
    bg_noise_db = np.percentile(rms_db, 10)

    # 2. Hardened VAD (Voice Activity Detection)
    # Requires 12dB above noise floor, smoothed over ~150ms to ignore clicks
    silence_thresh = bg_noise_db + 12.0
    
    # FIX APPLIED HERE: Cast the boolean array to integers so medfilt can process it
    raw_is_speech = (rms_db > silence_thresh).astype(int)
    is_speech_int = medfilt(raw_is_speech, kernel_size=15) 
    
    # Convert back to boolean for accurate masking later
    is_speech = is_speech_int.astype(bool)
    
    changes = np.diff(is_speech_int)
    speech_segments = np.sum(changes == 1)
    silence_segments = np.sum(changes == -1)
    speech_ratio = np.sum(is_speech_int) / len(is_speech_int) if len(is_speech_int) > 0 else 0.0

    # 3. Masked Pitch & Micro-Tremors (Stress Proxies)
    f0, voiced_flag, _ = librosa.pyin(y, fmin=80, fmax=450, sr=sr)
    
    # Only evaluate pitch when BOTH pyin and our VAD agree there is speech
    valid_mask = voiced_flag & is_speech[:len(voiced_flag)]
    valid_f0 = f0[valid_mask]
    
    if len(valid_f0) > 0:
        pitch_mean = np.mean(valid_f0)
        pitch_std = np.std(valid_f0)
        pitch_min = np.min(valid_f0)
        pitch_max = np.max(valid_f0)
        # Jitter: Cycle-to-cycle frequency instability
        jitter = np.mean(np.abs(np.diff(valid_f0))) / np.mean(valid_f0)
    else:
        pitch_mean = pitch_std = pitch_min = pitch_max = jitter = 0.0

    # Masked Shimmer (Amplitude instability)
    valid_rms = rms[is_speech[:len(rms)]]
    if len(valid_rms) > 1:
        shimmer = np.mean(np.abs(np.diff(valid_rms))) / (np.mean(valid_rms) + 1e-6)
    else:
        shimmer = 0.0

    # 4. Kinetic Anomalies (Sudden >10dB spikes)
    energy_deriv = np.diff(rms_db)
    anomaly_spikes = np.sum(energy_deriv > 10.0)

    # 5. Type-Safe Export
    return {
        "duration_sec": float(round(duration, 3)),
        "rms_mean_db": float(round(np.mean(rms_db), 2)),
        "rms_std_db": float(round(np.std(rms_db), 2)),
        "background_noise_db": float(round(bg_noise_db, 2)),
        "pitch_mean_hz": float(round(pitch_mean, 1)),
        "pitch_std_hz": float(round(pitch_std, 1)),
        "pitch_min_hz": float(round(pitch_min, 1)),
        "pitch_max_hz": float(round(pitch_max, 1)),
        "speech_ratio": float(round(speech_ratio, 3)),
        "num_speech_segments": int(speech_segments),
        "num_silence_segments": int(silence_segments),
        "jitter_stress_proxy": float(round(jitter, 5)),
        "shimmer_stress_proxy": float(round(shimmer, 5)),
        "anomalous_energy_spikes": int(anomaly_spikes)
    }

# ===== KINETIC TRANSCRIPTION =====
def transcribe_and_profile(wav_path):
    """
    Extracts transcript and word-level velocity metrics.
    """
    model = whisper.load_model(WHISPER_MODEL)
    # Enable word timestamps for velocity analysis
    result = model.transcribe(wav_path, language="en", word_timestamps=True)
    
    transcript = result["text"].strip()
    words = []
    
    for segment in result.get("segments", []):
        for word in segment.get("words", []):
            words.append(word)

    # Calculate Speech Velocity (Words Per Minute) & Max Hesitation
    wpm = 0.0
    max_gap_sec = 0.0
    
    if len(words) > 1:
        total_speaking_time = words[-1]["end"] - words[0]["start"]
        if total_speaking_time > 0:
            wpm = (len(words) / total_speaking_time) * 60.0
            
        # Find the longest pause between two adjacent words
        for i in range(1, len(words)):
            gap = words[i]["start"] - words[i-1]["end"]
            if gap > max_gap_sec:
                max_gap_sec = gap

    return transcript, float(round(wpm, 1)), float(round(max_gap_sec, 2))

# ===== AI PROMPT ENGINEERING =====
def build_forensic_prompt(transcript, features, wpm, max_gap):
    """Strict prompt demanding psych-acoustic correlation."""
    return f"""<|think|>
ROLE: Expert Forensic Audio Profiler. 
TASK: Cross-reference linguistic content with physical DSP metrics to detect anomalies, stress, and behavioral leaks.

RAW EVIDENCE:
---
TRANSCRIPT: "{transcript}"
- Speech Velocity: {wpm} Words Per Minute
- Maximum Intra-Word Hesitation: {max_gap} seconds

DSP BIOMETRICS:
- Duration: {features['duration_sec']}s (Speaking Ratio: {features['speech_ratio']})
- Structural Pauses/Silences: {features['num_silence_segments']}
- Jitter (Vocal Cord Stress): {features['jitter_stress_proxy']}
- Shimmer (Breath/Amplitude Stress): {features['shimmer_stress_proxy']}
- Anomalous Energy Spikes (Kinetic impacts/shouts): {features['anomalous_energy_spikes']}
- Pitch Variance: {features['pitch_std_hz']} Hz
---

OUTPUT A CLINICAL REPORT WITH THESE HEADINGS:

1. **KINETIC DELIVERY & PACING**: Analyze the WPM and the Max Intra-Word Hesitation. Does the pacing match the transcript's context, or does it indicate cognitive load/fabrication?
2. **PHYSIOLOGICAL STRESS MARKERS**: Interpret Jitter, Shimmer, and Pitch Variance. Is the subject's vocal tract relaxed, or showing micro-tremors associated with anxiety or deception?
3. **ANOMALY DETECTIONS**: Detail the structural pauses and any anomalous energy spikes. Are there signs of aggression, heavy editing, or environmental interruptions?
4. **FORENSIC CONCLUSION**: A single paragraph synthesizing the subject's probable psychological state (e.g., highly rehearsed, acutely stressed, spontaneous/relaxed).

RULES: Be cold, analytical, and ruthless. If a metric is 0 or unnotable, state "Nominal Baseline". DO NOT hallucinate audio that isn't represented by the data.
"""

def ask_gemma(prompt):
    import ollama
    response = ollama.generate(model=MODEL_NAME, prompt=prompt)
    return response['response']

# ===== MAIN EXECUTION =====
def analyze():
    files = [f for f in glob.glob(os.path.join(FOLDER_PATH, "*.wav"))
             if "proc_temp" not in os.path.basename(f)]
    if not files:
        print("❌ No .wav found in ~/Desktop/GemmaAudio.")
        return
    
    target = max(files, key=os.path.getctime)
    print(f"🔬 FORENSIC TARGET: {os.path.basename(target)}")

    # Standardize audio for macOS
    subprocess.run(["afconvert", "-f", "WAVE", "-d", "LEF32@16000", "-c", "1",
                    target, TEMP_WAV], check=True)

    try:
        print("⚙️  Running DSP Biometric Scan...")
        features = extract_acoustic_features(TEMP_WAV)
        
        print("⏱️  Running Velocity & Transcription Matrix...")
        transcript, wpm, max_gap = transcribe_and_profile(TEMP_WAV)
        print(f"   -> Words Per Minute: {wpm}")
        print(f"   -> Max Hesitation: {max_gap}s")

        prompt = build_forensic_prompt(transcript, features, wpm, max_gap)
        
        print("🧠 Compiling Psych-Acoustic Profile via LLM...")
        report = ask_gemma(prompt)

        print("\n" + "━"*60)
        print("☢️ ADVANCED PSYCH-ACOUSTIC FORENSIC PROFILE ☢️")
        print("━"*60)
        print(report)
        print("━"*60)
        
        # Merge stats for final JSON dump
        features["wpm"] = wpm
        features["max_hesitation_sec"] = max_gap
        features["transcript"] = transcript
        
        print("\n📋 VERIFIED RAW TELEMETRY:")
        print(json.dumps(features, indent=2))
        
    except Exception as e:
        print(f"❌ CRITICAL FAILURE: {e}")
    finally:
        if os.path.exists(TEMP_WAV):
            os.remove(TEMP_WAV)

if __name__ == "__main__":
    analyze()
