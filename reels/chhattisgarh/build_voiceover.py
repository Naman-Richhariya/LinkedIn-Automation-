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
VOICE = "af_heart"
SPEED = 1.0
HERE = Path(__file__).parent
SEG_DIR = HERE / "vo_segments"

LINES = [
    (0.5, [("en-us", "Thirty-six forts. One heart.")]),
    (4.4, [("en-us", "This is"), ("hi", "छत्तीसगढ़।"),
           ("en-us", "India's twenty-sixth state, born November first, two thousand.")]),
    (10.4, [("en-us", "More than forty percent of this land is forest. Sal, teak, and mahua.")]),
    (16.4, [("en-us", "In Bastar, Chitrakote Falls roars across the Indravati. The Niagara of India.")]),
    (22.4, [("en-us", "They call it"), ("hi", "धान का कटोरा।"), ("en-us", "The rice bowl of India.")]),
    (28.4, [("en-us", "Bastar Dussehra lasts seventy-five days. One of the longest festivals on Earth.")]),
    (34.4, [("en-us", "Dhokra artisans still cast metal the four-thousand-year-old way.")]),
    (40.4, [("en-us", "At Sirpur, the seventh-century Laxman Temple still stands, in brick.")]),
    (46.4, [("en-us", "And on the plate?"), ("hi", "चीला, फरा, बोरे बासी, ठेठरी, खुरमी।")]),
    (52.6, [("hi", "छत्तीसगढ़िया, सबसे बढ़िया!"), ("hi", "हैप्पी राज्योत्सव!")]),
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
        out = SEG_DIR / f"l{n:02d}_s{k}_{speed:.2f}.wav"
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
