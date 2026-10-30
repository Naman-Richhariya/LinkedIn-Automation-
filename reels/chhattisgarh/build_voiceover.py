"""Voiceover for the Chhattisgarh reel: Kokoro TTS via `npx hyperframes tts`,
one line per scene, mixed over the soundtrack with ducking.

Each line is a list of (lang, text) segments so Hindi words get Hindi phonemes
while keeping one voice. Lines are placed at scene starts (scenes are 6 s).

Usage: python build_voiceover.py <soundtrack.wav> <out_mix.wav>
Needs HYPERFRAMES_PYTHON pointing at a python with kokoro-onnx + soundfile.
"""
import json
import subprocess
import sys
import wave
from pathlib import Path

import numpy as np

SR = 44100
VOICE = sys.argv[3] if len(sys.argv) > 3 else "hf_alpha"  # Kokoro Hindi voice
SPEED = 1.0
HERE = Path(__file__).parent
SEG_DIR = HERE / "vo_segments"

# Hindi narration with Chhattisgarhi greeting and sign-off
# (जोहार = greeting, सबले बढ़िया = the best, गाड़ा-गाड़ा बधाई = heartiest wishes).
LINES = [
    (0.5, [("hi", "जोहार! छत्तीस गढ़, एक दिल।")]),
    (4.4, [("hi", "ये है छत्तीसगढ़। भारत का छब्बीसवाँ राज्य, जो एक नवंबर, दो हज़ार को बना।")]),
    (10.4, [("hi", "यहाँ चालीस प्रतिशत से ज़्यादा धरती पर जंगल है। साल, सागौन और महुआ।")]),
    (16.4, [("hi", "बस्तर में इंद्रावती पर गरजता चित्रकोट जलप्रपात। भारत का नियाग्रा।")]),
    (22.4, [("hi", "इसीलिए इसे कहते हैं, धान का कटोरा।")]),
    (28.4, [("hi", "बस्तर दशहरा पूरे पचहत्तर दिन चलता है। दुनिया के सबसे लंबे त्योहारों में से एक।")]),
    (34.4, [("hi", "ढोकरा शिल्पी आज भी चार हज़ार साल पुरानी विधि से धातु ढालते हैं।")]),
    (40.4, [("hi", "सिरपुर में सातवीं सदी का लक्ष्मण मंदिर, ईंटों से बना, आज भी खड़ा है।")]),
    (46.4, [("hi", "और थाली में? चीला, फरा, बोरे बासी, ठेठरी, खुरमी!")]),
    (52.6, [("hi", "छत्तीसगढ़िया, सबले बढ़िया!"), ("hi", "राज्योत्सव के गाड़ा गाड़ा बधाई!")]),
]
MAX_LINE = 5.6  # each line must finish before the next scene's swell


def read_wav(path):
    """Read any wav as mono float at SR (via ffmpeg for resampling)."""
    raw = subprocess.run(
        ["ffmpeg", "-v", "error", "-i", str(path), "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"],
        check=True, capture_output=True,
    ).stdout
    return np.frombuffer(raw, dtype="<f4").astype(np.float64)


def tts(text, lang, out, speed):
    if out.exists():
        return
    res = subprocess.run(
        ["npx", "--yes", "hyperframes", "tts", text, "-v", VOICE, "-l", lang, "-s", str(speed), "-o", str(out), "--json"],
        capture_output=True, text=True,
    )
    payload = json.loads(res.stdout.strip().splitlines()[-1])
    if not payload.get("ok"):
        raise RuntimeError(f"tts failed for {text!r}: {payload}")


def trim(sig, thresh=0.01):
    idx = np.where(np.abs(sig) > thresh)[0]
    if not len(idx):
        return sig
    return sig[max(0, idx[0] - int(0.02 * SR)) : idx[-1] + int(0.06 * SR)]


def build_line(n, segments, speed):
    parts = []
    for k, (lang, text) in enumerate(segments):
        out = SEG_DIR / f"{VOICE}_l{n:02d}_s{k}_{speed:.2f}.wav"
        tts(text, lang, out, speed)
        parts.append(trim(read_wav(out)))
        parts.append(np.zeros(int(0.12 * SR)))
    return np.concatenate(parts[:-1])


def main():
    SEG_DIR.mkdir(exist_ok=True)
    music = read_wav(sys.argv[1])  # mono read is only used for length
    n = len(music)
    with wave.open(sys.argv[1]) as w:
        stereo = np.frombuffer(w.readframes(w.getnframes()), dtype="<i2").reshape(-1, 2) / 32768.0
    vo = np.zeros(n)
    duck = np.ones(n)
    report = []
    for i, (start, segs) in enumerate(LINES):
        speed = SPEED
        line = build_line(i, segs, speed)
        while len(line) / SR > MAX_LINE and speed < 1.3:
            speed = round(speed + 0.08, 2)
            line = build_line(i, segs, speed)
        a = int(start * SR)
        line = line[: n - a]
        vo[a : a + len(line)] += line
        # duck music under the line with 150 ms ramps
        ramp = int(0.15 * SR)
        lo, hi = max(0, a - ramp), min(n, a + len(line) + ramp)
        duck[lo:hi] = np.minimum(duck[lo:hi], 0.38)
        report.append({"line": i + 1, "start": start, "seconds": round(len(line) / SR, 2), "speed": speed})
    # smooth the duck envelope
    k = int(0.15 * SR)
    duck = np.convolve(duck, np.ones(k) / k, "same")
    vo *= 0.9 / max(1e-9, np.max(np.abs(vo)))
    mix = stereo[:n] * duck[:, None] + vo[:, None] * 0.95
    mix *= 0.89 / np.max(np.abs(mix))
    with wave.open(sys.argv[2], "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes((mix * 32767).astype("<i2").tobytes())
    with wave.open(str(HERE / "voiceover.wav"), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes((vo * 32767).astype("<i2").tobytes())
    print(json.dumps(report, indent=1))


if __name__ == "__main__":
    main()
