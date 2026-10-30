"""Original score + sound design for the Day 2 kinetic reel.

A punchy 100 BPM groove (kick, clap, hats, sub bass, dholak-style accents and a
pentatonic pluck hook) plus synthesized SFX on every beat change: whooshes into cuts,
impacts on slams, pops on text, a riser before the "Niagara" hit and a tail at the end.

Usage: python generate_music.py <out.wav>
"""
import sys
import wave

import numpy as np

SR = 44100
DUR = 55.0
N = int(SR * DUR)
BPM = 100
BEAT = 60 / BPM
rng = np.random.default_rng(31)
mix = np.zeros((N, 2))

CUTS = [3.0, 4.6, 6.6, 9.0, 12.2, 16.0, 18.0, 21.2, 23.0, 27.0, 31.0, 38.0, 45.0, 50.0]
SLAMS = [1.75, 3.0, 5.0, 21.7, 27.3, 38.2]
POPS = [0.15, 0.55, 0.7, 7.0, 7.3, 7.8, 9.4, 10.6, 16.1, 18.2, 23.4, 24.5, 34.3, 40.2, 45.6, 46.4, 46.75, 47.1, 47.45, 50.4, 52.2]


def hz(m):
    return 440 * 2 ** ((m - 69) / 12)


def env(n, a, d):
    t = np.arange(n) / SR
    return np.clip(t / max(a, 1e-4), 0, 1) * np.exp(-t / d)


def add(sig, start, gain, pan=0.0):
    i = int(start * SR)
    if i >= N or i + len(sig) <= 0:
        return
    if i < 0:
        sig, i = sig[-i:], 0
    sig = sig[: N - i] * gain
    mix[i : i + len(sig), 0] += sig * np.cos((pan + 1) * np.pi / 4)
    mix[i : i + len(sig), 1] += sig * np.sin((pan + 1) * np.pi / 4)


def kick():
    n = int(0.45 * SR); t = np.arange(n) / SR
    f = 48 + 110 * np.exp(-t / 0.04)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * env(n, 0.001, 0.18)


def clap():
    n = int(0.3 * SR)
    s = rng.standard_normal(n)
    s = np.convolve(s, [1, -0.6], "same") * env(n, 0.001, 0.07)
    for d in (0.008, 0.016):
        k = int(d * SR); s[k:] += 0.6 * s[:-k]
    return s


def hat(open_=False):
    n = int((0.25 if open_ else 0.06) * SR)
    s = np.diff(rng.standard_normal(n + 1)) * env(n, 0.0005, 0.08 if open_ else 0.015)
    return s


def dhol(p=hz(55)):
    n = int(0.35 * SR); t = np.arange(n) / SR
    return (np.sin(2 * np.pi * p * t) * env(n, 0.001, 0.09) + 0.4 * rng.standard_normal(n) * env(n, 0.0005, 0.01))


def sub(m, length):
    n = int(length * SR); t = np.arange(n) / SR
    s = np.sin(2 * np.pi * hz(m) * t) + 0.25 * np.sin(2 * np.pi * hz(m) * 2 * t)
    return s * np.clip(t / 0.01, 0, 1) * np.clip((length - t) / 0.05, 0, 1)


def pluck(m, length=0.6):
    n = int(length * SR); t = np.arange(n) / SR
    f = hz(m)
    s = np.sign(np.sin(2 * np.pi * f * t)) * 0.3 + np.sin(2 * np.pi * f * t) + 0.4 * np.sin(4 * np.pi * f * t)
    return s * env(n, 0.002, 0.16)


def whoosh(length=0.45, up=True):
    n = int(length * SR)
    s = rng.standard_normal(n)
    k = np.linspace(40, 4, n) if up else np.linspace(4, 40, n)
    out = np.zeros(n); acc = 0.0
    for i in range(n):  # moving one-pole filter = sweep
        a = 1 / k[i]
        acc += a * (s[i] - acc); out[i] = acc
    shape = np.sin(np.linspace(0, np.pi, n)) ** 2
    return out * shape * 6


def impact():
    n = int(1.2 * SR); t = np.arange(n) / SR
    boom = np.sin(2 * np.pi * (40 + 60 * np.exp(-t / 0.05)) * t) * env(n, 0.001, 0.35)
    crack = rng.standard_normal(n) * env(n, 0.0005, 0.03)
    return boom + 0.5 * crack


def pop():
    n = int(0.09 * SR); t = np.arange(n) / SR
    return np.sin(2 * np.pi * (900 - 500 * t / 0.09) * t) * env(n, 0.001, 0.025)


def riser(length):
    n = int(length * SR); t = np.arange(n) / SR
    f = 200 * (8 ** (t / length))
    tone = np.sin(2 * np.pi * np.cumsum(f) / SR)
    noise = np.convolve(rng.standard_normal(n), np.ones(6) / 6, "same")
    return (0.4 * tone + noise) * (t / length) ** 2


# ---- groove ----
bassline = [38, 38, 41, 36]  # D, D, F, C (one bar each)
hook = [62, 65, 67, 69, 72, 69, 67, 65]
t0 = 3.0
bar = 0
time = t0
while time < 50.0 - 1e-6:
    energy = 0.75 if time < 9 else (1.0 if time < 45 else 0.8)
    for b in (0, 1.5, 2.5):
        add(kick(), time + b * BEAT, 0.9 * energy)
    for b in (1, 3):
        add(clap(), time + b * BEAT, 0.35 * energy, 0.05)
    for k in range(8):
        add(hat(k == 7), time + k * BEAT / 2, (0.12 if k % 2 else 0.07) * energy, 0.35)
    for b in (0.75, 2.25, 3.5):
        add(dhol(hz(57 if b == 3.5 else 52)), time + b * BEAT, 0.22 * energy, -0.3)
    add(sub(bassline[bar % 4], 4 * BEAT * 0.98), time, 0.32 * energy)
    if time >= 9:
        for k, m in enumerate(hook):
            if (bar % 2 == 1) and k >= 4:
                m = hook[7 - k]
            add(pluck(m), time + k * BEAT / 2, 0.07 * energy, 0.25 if k % 2 else -0.25)
    bar += 1
    time += 4 * BEAT

# intro 0–3: filtered pulse + plucks
for k in range(6):
    add(pluck(62 + (k % 3) * 3, 0.8), k * BEAT, 0.05, 0)
add(sub(38, 3.0), 0, 0.15)
# outro 50–55: hook + sustained bass
for k, m in enumerate([74, 72, 69, 67, 69, 74]):
    add(pluck(m, 1.0), 50.0 + k * BEAT / 2, 0.08, 0)
add(sub(38, 4.5), 50.0, 0.3)
add(kick(), 50.0, 1.0)

# ---- sound design ----
for c in CUTS:
    add(whoosh(0.4), c - 0.35, 0.18, 0)
for s in SLAMS:
    add(impact(), s + 0.25, 0.45, 0)
for p in POPS:
    add(pop(), p, 0.12, 0.2)
add(riser(2.0), 19.7, 0.12, 0)
add(impact(), 21.2, 0.6, 0)

# glue: soft room + limiter
out = mix.copy()
for d, g in ((0.029, 0.18), (0.053, 0.14), (0.097, 0.1)):
    k = int(d * SR)
    out[k:, 0] += mix[:-k, 1] * g
    out[k:, 1] += mix[:-k, 0] * g
out = np.tanh(out * 1.4 / np.max(np.abs(out)) * 1.2) * 0.9
with wave.open(sys.argv[1], "wb") as w:
    w.setnchannels(2)
    w.setsampwidth(2)
    w.setframerate(SR)
    w.writeframes((out * 32767).astype("<i2").tobytes())
