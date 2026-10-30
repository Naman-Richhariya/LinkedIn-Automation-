"""Original ambient score for Day 2 (Chitrakote): warm pads, santoor-like plucks,
river texture and soft swells into each scene. Sits low so a voiceover can ride on top.

Usage: python generate_music.py <out.wav>
"""
import sys
import wave

import numpy as np

SR = 44100
DUR = 55.0
N = int(SR * DUR)
BOUNDS = [3, 9, 16, 23, 31, 38, 45, 50]
rng = np.random.default_rng(2)
t = np.arange(N) / SR
mix = np.zeros((N, 2))


def hz(m):
    return 440 * 2 ** ((m - 69) / 12)


def add(sig, start, gain, pan=0.0):
    i = int(start * SR)
    if i >= N:
        return
    sig = sig[: N - i] * gain
    mix[i : i + len(sig), 0] += sig * np.cos((pan + 1) * np.pi / 4)
    mix[i : i + len(sig), 1] += sig * np.sin((pan + 1) * np.pi / 4)


# ---- pads: chord progression, 7 s per chord, cross-faded ----
chords = [[50, 57, 62, 66, 69], [47, 54, 59, 62, 66], [43, 50, 55, 59, 62], [45, 52, 57, 61, 64]]
seg = 7.0
pad = np.zeros(N)
for c in range(int(np.ceil(DUR / seg)) + 1):
    notes = chords[c % 4]
    s0 = c * seg - 1.5
    n = int((seg + 3) * SR)
    tt = np.arange(n) / SR
    env = np.clip(tt / 2.0, 0, 1) * np.clip((seg + 3 - tt) / 2.0, 0, 1)
    sig = np.zeros(n)
    for m in notes:
        for d in (-0.07, 0.07):
            f = hz(m) * 2 ** (d / 12)
            for h in range(1, 5):
                sig += np.sin(2 * np.pi * f * h * tt + rng.uniform(0, 6)) / (h ** 1.6)
    i = int(max(0, s0) * SR)
    sig = sig[int(max(0, -s0) * SR):] * env[int(max(0, -s0) * SR):]
    pad[i : i + len(sig)] += sig[: N - i]
pad *= np.clip(t / 3, 0, 1) * np.clip((DUR - t) / 3, 0, 1)
add(pad, 0, 0.022, -0.2)
add(pad, 0.013, 0.022, 0.2)


# ---- santoor-like plucks: D major pentatonic arpeggios ----
def pluck(m, length=2.2):
    n = int(length * SR)
    tt = np.arange(n) / SR
    f = hz(m)
    s = (np.sin(2 * np.pi * f * tt) + 0.5 * np.sin(2 * np.pi * f * 2.01 * tt) + 0.22 * np.sin(2 * np.pi * f * 3.02 * tt))
    s *= np.exp(-tt / 0.55) * np.clip(tt / 0.003, 0, 1)
    return s


scale = [62, 64, 66, 69, 71, 74, 76, 78, 81]
beat = 60 / 76
time = 3.0
k = 0
while time < 49.5:
    phrase = [0, 2, 4, 5, 3, 4, 2, 1] if (k // 8) % 2 == 0 else [5, 4, 2, 3, 4, 6, 5, 3]
    m = scale[phrase[k % 8]] + (0 if time < 23 else 0)
    add(pluck(m), time, 0.06 if k % 2 == 0 else 0.04, 0.35 if k % 2 else -0.35)
    if k % 4 == 0:
        add(pluck(m - 12, 3.0), time, 0.05, 0)
    time += beat / 2 if 16 <= time < 45 else beat
    k += 1
# closing phrase
for j, m in enumerate([74, 78, 81, 86]):
    add(pluck(m, 3.5), 50.2 + j * 0.45, 0.06, -0.3 + j * 0.2)

# ---- river texture: filtered noise with slow movement ----
noise = rng.standard_normal(N)
river = np.convolve(noise, np.ones(40) / 40, "same") - np.convolve(noise, np.ones(400) / 400, "same")
river *= 0.6 + 0.4 * np.sin(2 * np.pi * 0.07 * t)
river *= np.clip(t / 2, 0, 1) * np.clip((DUR - t) / 3, 0, 1)
add(river, 0, 0.12, 0)

# ---- soft low pulse from 16 s ----
for b in np.arange(16, 49.5, beat * 2):
    n = int(0.8 * SR)
    tt = np.arange(n) / SR
    add(np.sin(2 * np.pi * hz(38) * tt) * np.exp(-tt / 0.25), b, 0.10, 0)

# ---- swells into each scene ----
for s in BOUNDS:
    n = int(1.4 * SR)
    sw = np.convolve(rng.standard_normal(n), np.ones(30) / 30, "same") * (np.arange(n) / n) ** 2.5
    add(sw, s - 1.4, 0.05, 0)
    n2 = int(2.0 * SR)
    tt = np.arange(n2) / SR
    add(np.sin(2 * np.pi * hz(50) * tt) * np.exp(-tt / 0.7) * np.clip(tt / 0.01, 0, 1), s, 0.06, 0)

# room
out = mix.copy()
for d, g in ((0.037, 0.3), (0.061, 0.25), (0.113, 0.18), (0.197, 0.12), (0.29, 0.08)):
    kd = int(d * SR)
    out[kd:, 0] += mix[:-kd, 1] * g
    out[kd:, 1] += mix[:-kd, 0] * g
out /= np.max(np.abs(out)) / 0.7
with wave.open(sys.argv[1], "wb") as w:
    w.setnchannels(2)
    w.setsampwidth(2)
    w.setframerate(SR)
    w.writeframes((out * 32767).astype("<i2").tobytes())
