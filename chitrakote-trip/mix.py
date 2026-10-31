"""Score, foley and voice for Chitrakote, all from events.json (exported from the page timeline).
Two resolutions in the music: a hi-fi band (FM electric piano, bass, brushes) is the app's world,
a pulse-wave chip voice is Pip. Writes out/mix.wav."""
import json, os, sys
import numpy as np
import soundfile as sf, soxr

LIB = os.environ['LIB']; sys.path.insert(0, os.path.join(LIB, 'core', 'audio'))
from sfx import SR, t_, env_exp, bp, lp, hp, noise, norm, brown, click, thump, whoosh, pop, ding, compress, limit, add

HERE = os.path.dirname(os.path.abspath(__file__))
E = json.load(open(os.path.join(HERE, 'events.json')))
DUR, EV = E['dur'], E['ev']
meta = next(e for e in EV if e['type'] == 'meta')
BPM = meta['bpm']; BEAT = 60 / BPM; BAR = 4 * BEAT
N = int(DUR * SR)
rng = np.random.default_rng(11)
mtof = lambda m: 440 * 2 ** ((m - 69) / 12)

music = np.zeros((N, 2)); chip = np.zeros((N, 2)); fx = np.zeros((N, 2)); bed = np.zeros((N, 2)); vo = np.zeros((N, 2))

# ---------- instruments ----------
def ep(m, d, v=1.0):
    """FM electric piano: bell-ish attack, mellow tail"""
    f = mtof(m); tt = t_(d); idx = 2.2 * np.exp(-tt / .25) + .3
    x = np.sin(2 * np.pi * f * tt + idx * np.sin(2 * np.pi * f * tt)) * np.exp(-tt / 1.1)
    x += .25 * np.sin(2 * np.pi * 2 * f * tt) * np.exp(-tt / .3)
    a = np.minimum(1, tt / .004); r = np.minimum(1, (d - tt) / .08)
    return x * a * r * v * (1 + .08 * np.sin(2 * np.pi * 5 * tt))

def bass(m, d, v=1.0):
    f = mtof(m); tt = t_(d)
    x = np.sin(2 * np.pi * f * tt) + .45 * np.sin(4 * np.pi * f * tt) + .2 * np.sin(6 * np.pi * f * tt)
    return lp(x * np.minimum(1, tt / .01) * np.exp(-tt / .9) * np.minimum(1, (d - tt) / .05), 900) * v

def pulse(m, d, v=1.0, duty=.25, sweep=0.0):
    tt = t_(d); f = mtof(m) * (1 + sweep * tt / max(d, 1e-3))
    ph = np.cumsum(f) / SR % 1
    x = np.where(ph < duty, 1.0, -1.0) * .5
    # 8-bit stepped envelope (four steps)
    e = np.floor(np.clip(1 - tt / d, 0, 1) * 4) / 4
    return x * e * v

def brush(v=1.0, d=.22):
    return bp(noise(d), 2500, 9000) * np.minimum(1, t_(d) / .03) * np.exp(-t_(d) / .07) * v

def hat(v=1.0):
    d = .05; return hp(noise(d), 7000) * env_exp(d, .012) * v

def pad(ms, d, v=1.0):
    tt = t_(d); x = sum(np.sin(2 * np.pi * mtof(m) * (1 + det) * tt) for m in ms for det in (-.003, .003))
    return lp(x, 2000) * np.minimum(1, tt / 1.2) * np.minimum(1, (d - tt) / .8) * v / (2 * len(ms))

CH = {'D': (62, [62, 66, 69, 74], 38), 'Bm': (59, [59, 62, 66, 71], 35), 'G': (55, [55, 59, 62, 67], 31), 'A': (57, [57, 61, 64, 69], 33)}
PROG = ['D', 'Bm', 'G', 'A']

def section(t):
    if t < 19.2: return 'A'
    if t < 24.0: return 'B'
    if t < 33.6: return 'C'
    return 'D'

# ---------- score ----------
nbars = int(np.ceil(DUR / BAR))
for b in range(nbars):
    t0 = b * BAR; sec = section(t0 + .01); ch = CH[PROG[b % 4]]
    if sec == 'B':
        continue
    last = t0 >= 43.1
    # piano comp
    hits = [0, 2] if sec in 'AD' else [0, 1.5, 2, 3.5]
    if last: hits = [0]
    for h in hits:
        for i, m in enumerate(ch[1]):
            add_t = t0 + h * BEAT + i * .012
            if add_t < DUR - .05:
                d = (BAR * 1.2 if last else BEAT * 1.6)
                add(music, ep(m, min(d, DUR - add_t), .22 if sec != 'C' else .26), add_t, pan=-.2 + .13 * i)
    # bass
    bh = [0, 2] if sec != 'C' else [0, 1.5, 2, 3, 3.5]
    if last: bh = [0]
    for h in bh:
        tt0 = t0 + h * BEAT
        if tt0 < DUR - .1: add(music, bass(ch[2] + (12 if h in (1.5, 3.5) else 0), min(BEAT * 1.4, DUR - tt0), .5), tt0)
    # kit
    if (sec == 'A' and b >= 2) or sec == 'C' or (sec == 'D' and not last):
        for k in range(4):
            tk = t0 + k * BEAT
            if k in (1, 3): add(music, brush(.35 if sec != 'C' else .45), tk, pan=.25)
            if sec == 'C':
                if k in (0, 2): add(music, thump(.6, 62), tk)
                for e8 in (0, .5): add(music, hat(.18), tk + e8 * BEAT, pan=.35)
        if sec == 'A' and b < nbars: add(music, thump(.35, 58), t0)
# section B: one held pad, gone before the near-silence
add(music, pad([62, 69, 74, 76], 3.6, .5), 19.2)
# the flood swell (on the switch downbeat)
tt = t_(1.4); sw = lp(brown(1.4), 300) * (tt / 1.4) ** 2 * .9 + np.sin(2 * np.pi * (40 + 25 * tt) * tt) * (tt / 1.4) ** 2 * .5
add(music, sw, 24.0 - 1.0 + .6)
# drum fills / crash at chapter seams
for ts in (9.6, 36.0):
    for k in range(4): add(music, thump(.4, 90 + 18 * k), ts - BEAT + k * BEAT / 4)
add(music, hp(noise(1.8), 3000) * env_exp(1.8, .5) * .25, 24.0, pan=.2)

# chip melody in C (duet with piano) and D (trading)
MEL_C = [(0, 74, 1), (1, 76, .5), (1.5, 78, .5), (2, 81, 1.5), (4, 78, 1), (5, 76, 1), (6, 74, 2),
         (8, 71, 1), (9, 74, .5), (9.5, 76, .5), (10, 79, 1.5), (12, 78, 1), (13, 76, .5), (13.5, 74, .5), (14, 76, 2)]
for bt, m, l in MEL_C + [(b + 16, m, l) for b, m, l in MEL_C[:7]]:
    tm = 24.0 + bt * BEAT
    if tm < 33.4: add(chip, pulse(m, l * BEAT * .9, .22), tm, pan=.15)
MEL_D = [(2, 78, .5), (2.5, 76, .5), (3, 74, 1), (10, 81, .5), (10.5, 78, .5), (11, 76, 1), (18, 74, .5), (18.5, 76, .5), (19, 78, 1), (24, 74, 2)]
for bt, m, l in MEL_D:
    tm = 33.6 + bt * BEAT
    if tm < 44.5: add(chip, pulse(m, l * BEAT * .9, .18), tm, pan=.15)

# Pip's notes on landings (D pentatonic, climbing through the film)
PENT = [74, 76, 78, 81, 83, 86]
li = 0
for e in EV:
    t = e['t']; ty = e['type']
    if ty == 'jump': add(chip, pulse(62 + (li % 3) * 2, .14, .22, duty=.125, sweep=1.2), t, pan=.1)
    elif ty == 'land': add(chip, pulse(PENT[li % len(PENT)], .12, .2), t, pan=.1); add(fx, hp(noise(.04), 1500) * env_exp(.04, .01) * .25, t); li += 1
    elif ty == 'step': add(chip, pulse(50 + (int(t * 5) % 2) * 2, .05, .12, duty=.5), t, pan=.05)
    elif ty == 'sit': add(chip, pulse(74, .25, .18, sweep=-.5), t)

# ---------- foley ----------
def thock(v=1.0):
    d = .07; tt = t_(d)
    return (np.sin(2 * np.pi * 150 * tt) * env_exp(d, .015) * .8 + bp(noise(d), 1800, 6000) * env_exp(d, .006) * .6) * v

for e in EV:
    t = e['t']; ty = e['type']
    if ty == 'key': add(fx, thock(.55 if not e.get('enter') else .8), t, pan=-.1); add(fx, click(1.4, .25), t + .004, pan=-.1)
    elif ty == 'click': add(fx, click(.8, .45), t)
    elif ty == 'pop': add(fx, pop(.45), t)
    elif ty == 'pin': add(fx, ding(.25), t, pan=.4)
    elif ty == 'whoosh': add(fx, whoosh(e.get('d', .35), .5), t - .1)
    elif ty == 'swish': add(fx, whoosh(.3, .18), t)
    elif ty == 'flood':
        add(fx, whoosh(.8, .8), t - .2)
        sp = lp(noise(1.2), 2500) * np.minimum(1, t_(1.2) / .05) * env_exp(1.2, .35) * .6
        add(fx, sp, t + .5)
    elif ty == 'drain': add(fx, whoosh(1.0, .6), t)
    elif ty == 'badge': add(fx, pop(.4), t); add(fx, ding(.18), t + .05)
    elif ty == 'toast': add(fx, pop(.5), t); add(fx, ding(.35), t + .12)

# ---------- beds ----------
tt = np.arange(N) / SR
room = lp(brown(DUR), 400) * .02
bed[:, 0] += room; bed[:, 1] += room
falls = lp(brown(DUR), 1400) * .6 + bp(noise(DUR), 800, 5000) * .12
lvl = np.interp(tt, [0, 24.2, 25.6, 32.6, 34.2, 45], [0, 0, 1.0, 1.0, .22, .18])
bed[:, 0] += falls * lvl; bed[:, 1] += np.roll(falls, 900) * lvl

# ---------- voice ----------
vmask = np.zeros(N)
for v in meta['vo']:
    x, sr = sf.read(os.path.join(HERE, 'vo', v['id'] + '.wav'), dtype='float64')
    if x.ndim > 1: x = x.mean(1)
    x = soxr.resample(x, sr, SR)
    x = compress(norm(x, .9), thr=.3, ratio=3)
    add(vo, x, v['t'])
    s, e = int(v['t'] * SR), min(N, int(v['t'] * SR) + len(x))
    vmask[s:e] = 1
# smooth ducking envelope
from scipy.ndimage import uniform_filter1d, maximum_filter1d
duck = uniform_filter1d(maximum_filter1d(vmask, int(.25 * SR)), int(.15 * SR))

# near-silence before the switch: everything but room tone dips
quiet = 1 - .92 * np.interp(tt, [0, 21.9, 22.5, 23.95, 24.0, 45], [0, 0, 1, 1, 0, 0])

def rms(x): return np.sqrt(np.mean(x ** 2) + 1e-12)
vr = rms(vo[vmask > 0])
music *= (vr / rms(music)) * 10 ** (-12 / 20)
chip *= (vr / rms(chip)) * 10 ** (-17 / 20)
mus = (music + chip) * (1 - .55 * duck)[:, None] * quiet[:, None]
bedm = bed * (1 - .45 * duck)[:, None]
fxm = fx * .9
out = vo + mus + bedm * .55 + fxm
out[:, 0] = limit(out[:, 0], .95); out[:, 1] = limit(out[:, 1], .95)
os.makedirs(os.path.join(HERE, 'out'), exist_ok=True)
sf.write(os.path.join(HERE, 'out', 'mix.wav'), out.astype(np.float32), SR, subtype='PCM_24')
print('mix ok', out.shape, 'peak', float(np.abs(out).max()))
