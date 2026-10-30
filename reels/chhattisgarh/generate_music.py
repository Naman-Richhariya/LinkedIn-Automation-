"""Original procedural soundtrack for the Chhattisgarh reel.

120 BPM (one bar = 2 s) so every scene cut (multiples of 2 s) lands on a downbeat.
Layers: tanpura-style drone, dholak-style hand drums, shaker, bansuri-style
pentatonic flute, and swells into each scene boundary. Fully deterministic.

Usage: python generate_music.py <output.wav>
"""
import sys
import wave

import numpy as np

SR = 44100
DUR = 60.0
BPM = 120
BEAT = 60 / BPM
N = int(SR * DUR)
rng = np.random.default_rng(36)  # 36 forts

mix = np.zeros((N, 2))


def add(sig, start, gain=1.0, pan=0.0):
    i = int(start * SR)
    if i >= N:
        return
    sig = sig[: N - i] * gain
    left, right = np.cos((pan + 1) * np.pi / 4), np.sin((pan + 1) * np.pi / 4)
    mix[i : i + len(sig), 0] += sig * left
    mix[i : i + len(sig), 1] += sig * right


def env(n, attack, decay_tau):
    t = np.arange(n) / SR
    a = np.clip(t / max(attack, 1e-4), 0, 1)
    return a * np.exp(-t / decay_tau)


def hz(note):  # MIDI -> Hz
    return 440 * 2 ** ((note - 69) / 12)


# ---- drone (D2 + A2 + D3), tanpura-ish shimmer ----
t = np.arange(N) / SR
drone = np.zeros(N)
for f, g in ((hz(38), 0.5), (hz(45), 0.35), (hz(50), 0.3), (hz(57), 0.12)):
    for h in range(1, 7):
        shimmer = 1 + 0.35 * np.sin(2 * np.pi * (0.13 * h + 0.07) * t + h)
        drone += g / h**1.3 * shimmer * np.sin(2 * np.pi * f * h * t + 0.002 * np.sin(2 * np.pi * 0.2 * t))
fade = np.clip(t / 3.0, 0, 1) * np.clip((DUR - t) / 2.5, 0, 1)
add(drone * fade, 0, 0.09)


# ---- drums ----
def dha(pitch=hz(41)):
    n = int(0.6 * SR)
    tt = np.arange(n) / SR
    f = pitch * (1 + 0.6 * np.exp(-tt / 0.03))
    body = np.sin(2 * np.pi * np.cumsum(f) / SR) * env(n, 0.002, 0.18)
    return body + 0.15 * rng.standard_normal(n) * env(n, 0.001, 0.01)


def ta(pitch=hz(67)):
    n = int(0.25 * SR)
    tt = np.arange(n) / SR
    tone = np.sin(2 * np.pi * pitch * tt) * env(n, 0.001, 0.05)
    slap = rng.standard_normal(n) * env(n, 0.0005, 0.02)
    slap = np.convolve(slap, [1, -0.9], "same")
    return 0.6 * tone + 0.5 * slap


def shaker():
    n = int(0.09 * SR)
    s = rng.standard_normal(n) * env(n, 0.012, 0.025)
    return np.convolve(s, [1, -1], "same")


def swell(length=1.5):
    n = int(length * SR)
    s = rng.standard_normal(n)
    s = np.convolve(s, np.ones(8) / 8, "same")
    ramp = (np.arange(n) / n) ** 3
    return s * ramp


def crash():
    n = int(2.5 * SR)
    s = rng.standard_normal(n)
    s = np.convolve(s, [1, -1], "same") * env(n, 0.002, 0.6)
    return s


# groove pattern per bar (in beats): dha=low, ta=high
LOW = [0, 1.5, 2, 3.5]
HIGH = [1, 2.75, 3]
groove_start, groove_end = 4.0, 52.0
bar = 0
time = groove_start
while time < groove_end - 1e-6:
    intensity = 0.8 if time < 28 else 1.0
    for b in LOW:
        add(dha(), time + b * BEAT, 0.55 * intensity, -0.15)
    for b in HIGH:
        add(ta(), time + b * BEAT, 0.32 * intensity, 0.25)
    if time >= 16:
        for k in range(8):
            add(shaker(), time + k * BEAT / 2 + 0.01 * rng.standard_normal(), 0.10 * (1.3 if k % 2 else 0.8), 0.5)
    if bar % 3 == 2:  # fill into the next scene
        for k, p in enumerate((72, 69, 67, 64)):
            add(ta(hz(p)), time + (3 + k * 0.25) * BEAT, 0.3, 0.1 * k - 0.2)
    bar += 1
    time += 4 * BEAT

# intro taps
for k in range(4):
    add(ta(hz(72)), 2 + k * BEAT, 0.12 + 0.05 * k, 0.3)

# swells + crashes on scene boundaries
for s in (4, 10, 16, 22, 28, 34, 40, 46, 52):
    add(swell(1.2), s - 1.2, 0.05)
    add(crash(), s, 0.06, 0.2)
    add(dha(hz(38)), s, 0.6)

# outro: double-time celebration 52-58, final hit at 58
time = 52.0
while time < 58 - 1e-6:
    for b in (0, 0.5, 1.5, 2, 2.5, 3.5):
        add(dha(), time + b * BEAT, 0.6, -0.15)
    for b in (1, 1.75, 3, 3.25, 3.75):
        add(ta(), time + b * BEAT, 0.34, 0.25)
    for k in range(16):
        add(shaker(), time + k * BEAT / 4, 0.08, 0.5)
    time += 4 * BEAT
add(dha(hz(36)), 58, 0.9)
add(crash(), 58, 0.1)


# ---- bansuri-style flute ----
def flute(note, length, vib=5.2):
    n = int(length * SR)
    tt = np.arange(n) / SR
    f = hz(note) * (1 + 0.006 * np.sin(2 * np.pi * vib * tt) * np.clip(tt / 0.25, 0, 1))
    ph = 2 * np.pi * np.cumsum(f) / SR
    tone = np.sin(ph) + 0.25 * np.sin(2 * ph) + 0.08 * np.sin(3 * ph)
    breath = np.convolve(rng.standard_normal(n), np.ones(20) / 20, "same") * 0.25
    a = np.clip(tt / 0.06, 0, 1) * np.clip((length - tt) / 0.12, 0, 1)
    return (tone + breath) * a


# D major pentatonic around D5: D E F# A B
P = {"D": 74, "E": 76, "F": 78, "A": 81, "B": 83, "d": 86, "a": 69, "b": 71}
phrases = {
    0.4: [("A", 1), ("B", 0.5), ("A", 0.5), ("F", 1.5)],
    10: [("D", 0.5), ("E", 0.5), ("F", 1), ("A", 1), ("F", 0.5), ("E", 0.5), ("D", 2)],
    22: [("A", 0.5), ("B", 0.5), ("d", 1), ("B", 0.5), ("A", 0.5), ("F", 1), ("A", 2)],
    34: [("F", 0.5), ("A", 0.5), ("B", 1), ("A", 0.5), ("F", 0.5), ("E", 1), ("D", 2)],
    46: [("D", 0.5), ("F", 0.5), ("A", 0.5), ("B", 0.5), ("d", 1.5), ("B", 0.5), ("A", 2)],
    52: [("A", 0.5), ("B", 0.5), ("d", 0.5), ("B", 0.5), ("A", 0.5), ("B", 0.5), ("d", 1),
         ("d", 0.5), ("B", 0.5), ("A", 0.5), ("F", 0.5), ("A", 1), ("D", 1)],
    58: [("d", 2)],
}
for start, notes in phrases.items():
    tm = start
    for name, beats in notes:
        add(flute(P[name], beats * BEAT * 0.98), tm, 0.11, -0.25)
        tm += beats * BEAT

# simple stereo room: a few short delays
out = mix.copy()
for d, g in ((0.031, 0.25), (0.047, 0.2), (0.089, 0.15), (0.143, 0.1)):
    k = int(d * SR)
    out[k:, 0] += mix[:-k, 1] * g
    out[k:, 1] += mix[:-k, 0] * g

out /= np.max(np.abs(out)) / 0.89
out[-int(0.05 * SR):] *= np.linspace(1, 0, int(0.05 * SR))[:, None]

with wave.open(sys.argv[1], "wb") as w:
    w.setnchannels(2)
    w.setsampwidth(2)
    w.setframerate(SR)
    w.writeframes((out * 32767).astype("<i2").tobytes())
