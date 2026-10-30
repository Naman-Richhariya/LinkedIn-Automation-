"""Day 2 — Chitrakote Falls. Editorial paper-collage reel (HyperFrames atelier).

Scene timings follow the voiceover script (reels/chhattisgarh/day02-chitrakote/script.md)
so the recorded VO can be dropped in. Run: python build_index.py
"""
import random
from pathlib import Path

W, H = 1080, 1920
DUR = 55
BOUNDS = [0, 3, 9, 16, 23, 31, 38, 45, 50, 55]
OVERLAP = 0.6
rnd = random.Random(2)


def torn(jit=0.9, step=3.2):
    """clip-path polygon (in %) with hand-torn edges."""
    pts = []
    def edge(a, b, fixed, horiz, inward):
        t = a
        while (t < b) if a < b else (t > b):
            j = rnd.uniform(0, jit)
            v = fixed + (j if inward > 0 else -j)
            pts.append((t, v) if horiz else (v, t))
            t += step if a < b else -step
    edge(0, 100, 0, True, 1)
    edge(0, 100, 100, False, -1)
    edge(100, 0, 100, True, -1)
    edge(100, 0, 0, False, 1)
    return "polygon(" + ",".join(f"{x:.2f}% {y:.2f}%" for x, y in pts) + ")"


def cut(cid, img, x, y, w, h, rot, pos="50% 50%", border=18):
    """A torn photo print with a paper border and shadow."""
    return (
        f'<div class="shadow" id="{cid}" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px;--r:{rot}deg">'
        f'<div class="print" style="clip-path:{torn()};padding:{border}px">'
        f'<div class="frame"><img id="{cid}-img" src="assets/{img}.jpg" style="object-position:{pos}"/></div>'
        f"</div></div>"
    )


def tape(tid, x, y, w, rot):
    return f'<div class="tape" id="{tid}" style="left:{x}px;top:{y}px;width:{w}px;--r:{rot}deg;clip-path:{torn(1.8, 6)}"></div>'


def line(lid, text, cls, style=""):
    """Masked line for reveal animations."""
    return f'<div class="mask" style="{style}"><div class="ln {cls}" id="{lid}">{text}</div></div>'


def scene(i, inner):
    start = BOUNDS[i - 1] - (OVERLAP if i > 1 else 0)
    dur = BOUNDS[i] - start
    return (
        f'<section id="s{i}" class="clip scene" data-start="{start:g}" data-duration="{dur:g}" data-track-index="{i}" style="z-index:{i}">'
        f'<div class="paper"></div>{inner}</section>'
    )


S = []
# 1 — hook
S.append(scene(1, f"""
  {line('s1-a', 'भारत का', 'hi ink', 'top:300px')}
  {line('s1-b', 'सबसे चौड़ा जलप्रपात', 'hi big ink', 'top:390px')}
  {cut('s1-c', 'monsoon', 70, 640, 940, 700, -3, '45% 50%')}
  {tape('s1-t1', 120, 615, 220, -8)}{tape('s1-t2', 760, 1300, 220, 6)}
  {line('s1-d', "India's widest waterfall — in Chhattisgarh", 'en-i ink', 'top:1420px')}
"""))
# 2 — title
S.append(scene(2, f"""
  {cut('s2-c', 'rainbow', 60, 230, 960, 820, 2, '50% 40%')}
  {tape('s2-t1', 440, 205, 200, -3)}
  {cut('s2-c2', 'sunset', 560, 1460, 440, 300, -4, '50% 50%', 12)}
  <div class="stamp" id="s2-stamp" style="left:800px;top:130px"><div>DAY</div><b>02</b><div>OF 31</div></div>
  {line('s2-k', 'BASTAR · INDRAVATI RIVER', 'label teal', 'top:1130px;left:70px;text-align:left;width:auto')}
  {line('s2-t', 'Chitrakote', 'title ink', 'top:1180px;left:60px;text-align:left;width:auto')}
  {line('s2-h', 'चित्रकोट जलप्रपात', 'hi rust', 'top:1340px;left:70px;text-align:left;width:auto')}
"""))
# 3 — height & distance
S.append(scene(3, f"""
  {cut('s3-c', 'canoe', 300, 230, 720, 1100, 2.5, '78% 50%')}
  {tape('s3-t1', 560, 205, 200, 4)}
  <div class="tag" id="s3-tag1" style="left:60px;top:470px;--r:-4deg"><b>~95 ft</b><span>ऊँचाई से गिरता पानी</span></div>
  <div class="tag" id="s3-tag2" style="left:90px;top:880px;--r:3deg"><b>~40 km</b><span>from Jagdalpur</span></div>
  {line('s3-n', 'Scale: a lone canoe at the foot of the falls', 'note ink', 'top:1390px')}
"""))
# 4 — width / Niagara
S.append(scene(4, f"""
  <div class="bignum ink" id="s4-num">300<small>m</small></div>
  {line('s4-a', 'wide in the monsoon', 'en-i ink', 'top:560px')}
  {cut('s4-c', 'monsoon', 40, 700, 1000, 640, -1.5, '60% 50%')}
  {tape('s4-t1', 80, 680, 200, -10)}{tape('s4-t2', 800, 1310, 200, 8)}
  {line('s4-h', 'भारत का नियाग्रा', 'hi big rust', 'top:1400px')}
"""))
# 5 — horseshoe & rainbow
S.append(scene(5, f"""
  {cut('s5-c', 'rainbow', 70, 250, 940, 1150, -2, '55% 60%')}
  {tape('s5-t1', 430, 225, 220, 2)}
  <div class="chip" id="s5-chip" style="left:640px;top:1080px;--r:-6deg">🌈 in the spray</div>
  {line('s5-h', 'घोड़े की नाल जैसा आकार', 'hi rust', 'top:1440px')}
  {line('s5-e', 'A horseshoe of falling water', 'en-i ink', 'top:1530px')}
"""))
# 6 — two seasons
S.append(scene(6, f"""
  {cut('s6-a', 'monsoon', 60, 240, 960, 560, -2, '30% 50%')}
  {cut('s6-b', 'rainbow', 60, 860, 960, 560, 1.5, '50% 70%')}
  <div class="chip" id="s6-l1" style="left:90px;top:720px;--r:-3deg">MONSOON · मिट्टी जैसा भूरा</div>
  <div class="chip light" id="s6-l2" style="left:430px;top:1350px;--r:2deg">WINTER · दूध जैसा सफ़ेद</div>
  {line('s6-n', 'Same falls, two seasons', 'en-i ink', 'top:1500px')}
"""))
# 7 — boat ride
S.append(scene(7, f"""
  {line('s7-h', 'नाव से, झरने के पास', 'hi big ink', 'top:290px')}
  {cut('s7-c', 'canoe', 40, 470, 1000, 900, -1.5, '45% 55%')}
  {tape('s7-t1', 760, 445, 220, 7)}
  {line('s7-e', 'Boat rides at the base of the falls', 'en-i ink', 'top:1430px')}
"""))
# 8 — best time
S.append(scene(8, f"""
  {cut('s8-c', 'sunset', 50, 300, 980, 760, 2, '50% 45%')}
  {tape('s8-t1', 100, 275, 200, -6)}
  <div class="cal" id="s8-cal"><span>BEST TIME TO VISIT</span><b>Jul — Oct</b><i>घूमने का सबसे अच्छा समय</i></div>
"""))
# 9 — end card (night)
S.append(scene(9, f"""
  <div class="night" id="s9-night"><img id="s9-img" src="assets/night.jpg"/></div>
  <div class="stamp light" id="s9-stamp"><div>DAY</div><b>02</b><div>OF 31</div></div>
  {line('s9-a', 'कल मिलते हैं', 'hi cream', 'top:1050px')}
  {line('s9-b', 'Next: तीरथगढ़ जलप्रपात', 'en-i cream', 'top:1150px')}
  {line('s9-c', 'छत्तीसगढ़िया सबले बढ़िया', 'hi gold', 'top:1260px')}
  {line('s9-d', '#31DaysOfChhattisgarh', 'label cream', 'top:1380px')}
"""))

FONTS = """
@font-face{font-family:Fraunces;font-weight:400;src:url(assets/fraunces-latin-400-normal.woff2) format('woff2')}
@font-face{font-family:Fraunces;font-weight:700;src:url(assets/fraunces-latin-700-normal.woff2) format('woff2')}
@font-face{font-family:Fraunces;font-weight:900;src:url(assets/fraunces-latin-900-normal.woff2) format('woff2')}
@font-face{font-family:Fraunces;font-style:italic;font-weight:400;src:url(assets/fraunces-latin-400-italic.woff2) format('woff2')}
@font-face{font-family:Grotesk;font-weight:700;src:url(assets/space-grotesk-latin-700-normal.woff2) format('woff2')}
@font-face{font-family:Grotesk;font-weight:400;src:url(assets/space-grotesk-latin-400-normal.woff2) format('woff2')}
@font-face{font-family:Tiro;src:url(assets/tiro-devanagari-hindi-devanagari-400-normal.woff2) format('woff2');unicode-range:U+0900-097F,U+200C-200D,U+25CC,U+A8E0-A8FF}
"""

CSS = FONTS + f"""
html,body{{margin:0;background:#EEE7DA}}
#root{{position:relative;width:{W}px;height:{H}px;overflow:hidden;background:#EEE7DA}}
.scene{{position:absolute;inset:0;overflow:hidden}}
.paper{{position:absolute;inset:0;background:url(assets/paper.jpg) center/cover;box-shadow:0 -30px 60px rgba(40,25,10,.25)}}
.shadow{{position:absolute;filter:drop-shadow(0 22px 26px rgba(45,30,15,.32)) drop-shadow(0 3px 4px rgba(45,30,15,.25));transform:rotate(var(--r))}}
.print{{position:absolute;inset:0;background:#FAF6EE;box-sizing:border-box}}
.frame{{position:relative;width:100%;height:100%;overflow:hidden}}
.frame img{{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;filter:saturate(1.05) contrast(1.04)}}
.tape{{position:absolute;height:54px;background:rgba(232,220,190,.78);transform:rotate(var(--r));box-shadow:0 2px 4px rgba(0,0,0,.08)}}
.mask{{position:absolute;left:0;width:{W}px;overflow:hidden;text-align:center;padding:0 60px;box-sizing:border-box}}
.ln{{display:block}}
.hi{{font-family:Tiro,serif;font-size:76px;line-height:1.3}}
.hi.big{{font-size:104px;line-height:1.25}}
.en-i{{font-family:Fraunces,serif;font-style:italic;font-weight:400;font-size:46px;line-height:1.3}}
.title{{font-family:Fraunces,serif;font-weight:900;font-size:150px;letter-spacing:-3px;line-height:1.05}}
.label{{font-family:Grotesk,sans-serif;font-weight:700;font-size:28px;letter-spacing:9px}}
.note{{font-family:Grotesk,sans-serif;font-size:32px;opacity:.75}}
.ink{{color:#1E1A16}} .rust{{color:#A8401F}} .teal{{color:#1F5260}} .cream{{color:#F4ECDD}} .gold{{color:#E9B866}}
.stamp{{position:absolute;left:770px;top:1100px;width:220px;height:220px;border-radius:50%;border:4px dashed #A8401F;color:#A8401F;display:flex;flex-direction:column;align-items:center;justify-content:center;font-family:Grotesk,sans-serif;font-weight:700;font-size:24px;letter-spacing:6px;transform:rotate(-12deg);background:rgba(250,246,238,.6)}}
.stamp b{{font-family:Fraunces,serif;font-weight:900;font-size:96px;letter-spacing:0;line-height:.95}}
.stamp.light{{left:430px;top:700px;color:#E9B866;border-color:#E9B866;background:rgba(10,12,16,.35)}}
.tag{{position:absolute;width:380px;padding:26px 28px 24px 54px;background:#FAF6EE;box-shadow:0 14px 22px rgba(45,30,15,.28);transform:rotate(var(--r));box-sizing:border-box}}
.tag:before{{content:"";position:absolute;left:20px;top:34px;width:18px;height:18px;border-radius:50%;background:#EEE7DA;box-shadow:inset 0 2px 3px rgba(0,0,0,.3)}}
.tag b{{display:block;font-family:Fraunces,serif;font-weight:900;font-size:68px;color:#1E1A16;line-height:1;white-space:nowrap}}
.tag span{{display:block;font-family:Tiro,Grotesk,sans-serif;font-size:30px;color:#A8401F;margin-top:6px}}
.bignum{{position:absolute;left:0;width:{W}px;top:240px;text-align:center;font-family:Fraunces,serif;font-weight:900;font-size:300px;line-height:1;letter-spacing:-8px}}
.bignum small{{font-size:120px;letter-spacing:0;margin-left:10px;font-weight:400;font-style:italic}}
.chip{{position:absolute;padding:14px 26px;background:#1E1A16;color:#F4ECDD;font-family:Grotesk,Tiro,sans-serif;font-weight:700;font-size:32px;letter-spacing:2px;transform:rotate(var(--r));box-shadow:0 10px 18px rgba(0,0,0,.25);white-space:nowrap}}
.chip.light{{background:#FAF6EE;color:#1E1A16}}
.cal{{position:absolute;left:150px;top:1120px;width:780px;padding:40px 30px 44px;background:#FAF6EE;text-align:center;box-shadow:0 18px 28px rgba(45,30,15,.3);transform:rotate(-1.5deg);border-top:16px solid #A8401F;box-sizing:border-box}}
.cal span{{display:block;font-family:Grotesk,sans-serif;font-weight:700;font-size:28px;letter-spacing:8px;color:#1F5260}}
.cal b{{display:block;font-family:Fraunces,serif;font-weight:900;font-size:130px;color:#1E1A16;line-height:1.1}}
.cal i{{display:block;font-family:Tiro,serif;font-style:normal;font-size:44px;color:#A8401F}}
.night{{position:absolute;inset:0;overflow:hidden;background:#07090C}}
.night img{{position:absolute;left:-30%;top:0;height:100%;width:auto;opacity:.92}}
#series{{position:absolute;left:60px;top:120px;z-index:40;font-family:Grotesk,sans-serif;font-weight:700;font-size:24px;letter-spacing:7px;color:#1E1A16;opacity:.8}}
#grain{{position:absolute;inset:0;z-index:50;opacity:.07;mix-blend-mode:multiply;pointer-events:none}}
"""

JS = """
window.__timelines = window.__timelines || {};
const tl = gsap.timeline({ paused: true });
const B = [0, 3, 9, 16, 23, 31, 38, 45, 50, 55];
const O = 0.6;
const dirs = [null, null, {yPercent: 100}, {xPercent: 100}, {yPercent: 100}, {xPercent: -100}, {yPercent: 100}, {xPercent: 100}, {yPercent: 100}, {yPercent: 100}];
for (let k = 2; k <= 9; k++) tl.from('#s' + k, Object.assign({ duration: O, ease: 'power3.inOut' }, dirs[k]), B[k - 1] - O);

// helpers
const settle = (sel, t, extra) => tl.from(sel, Object.assign({ y: 140, rotation: '+=8', opacity: 0, duration: 0.9, ease: 'back.out(1.15)' }, extra || {}), t);
const reveal = (sel, t) => tl.from(sel, { yPercent: 110, opacity: 0, duration: 0.7, ease: 'power3.out' }, t);
const tapeOn = (sel, t) => tl.from(sel, { scaleX: 0, opacity: 0, transformOrigin: '0% 50%', duration: 0.35, ease: 'power2.out' }, t);
const drift = (img, t0, t1, from, to) => tl.fromTo(img, Object.assign({ scale: 1.14 }, from || {}), Object.assign({ scale: 1.0, duration: t1 - t0, ease: 'none' }, to || {}), t0);
const pop = (sel, t) => tl.from(sel, { scale: 0.4, opacity: 0, duration: 0.55, ease: 'back.out(2)' }, t);

// S1 0-3
reveal('#s1-a', 0.1); reveal('#s1-b', 0.3);
settle('#s1-c', 0.2); drift('#s1-c-img', 0, 3.6);
tapeOn('#s1-t1', 0.8); tapeOn('#s1-t2', 0.95);
reveal('#s1-d', 1.0);

// S2 3-9
settle('#s2-c', 2.6); drift('#s2-c-img', 2.4, 9.6, { xPercent: 3 }, { xPercent: -3 });
tapeOn('#s2-t1', 3.2);
settle('#s2-c2', 3.6, { x: 200 }); drift('#s2-c2-img', 3.6, 9.6);
pop('#s2-stamp', 4.4);
reveal('#s2-k', 3.5); reveal('#s2-t', 3.7); reveal('#s2-h', 4.1);

// S3 9-16
settle('#s3-c', 8.6); drift('#s3-c-img', 8.4, 16.6, { yPercent: 2 }, { yPercent: -2 });
tapeOn('#s3-t1', 9.3);
settle('#s3-tag1', 9.8, { x: -300, y: 0 }); settle('#s3-tag2', 11.6, { x: -300, y: 0 });
reveal('#s3-n', 12.6);

// S4 16-23
tl.from('#s4-num', { scale: 1.25, opacity: 0, duration: 1.0, ease: 'power3.out' }, 15.8);
reveal('#s4-a', 16.6);
settle('#s4-c', 15.9); drift('#s4-c-img', 15.4, 23.6, { xPercent: -5 }, { xPercent: 5 });
tapeOn('#s4-t1', 16.6); tapeOn('#s4-t2', 16.8);
reveal('#s4-h', 18.8);

// S5 23-31
settle('#s5-c', 22.6); drift('#s5-c-img', 22.4, 31.6, { yPercent: -3 }, { yPercent: 2 });
tapeOn('#s5-t1', 23.3);
pop('#s5-chip', 25.6);
reveal('#s5-h', 23.8); reveal('#s5-e', 24.4);

// S6 31-38
settle('#s6-a', 30.6, { x: -200, y: 0 }); drift('#s6-a-img', 30.4, 38.6);
settle('#s6-b', 32.8, { x: 200, y: 0 }); drift('#s6-b-img', 32.6, 38.6);
pop('#s6-l1', 31.6); pop('#s6-l2', 33.8);
reveal('#s6-n', 34.8);

// S7 38-45
reveal('#s7-h', 37.9);
settle('#s7-c', 38.0); drift('#s7-c-img', 37.6, 45.6, { xPercent: 4 }, { xPercent: -3 });
tapeOn('#s7-t1', 38.7);
reveal('#s7-e', 39.4);

// S8 45-50
settle('#s8-c', 44.6); drift('#s8-c-img', 44.4, 50.6);
tapeOn('#s8-t1', 45.2);
settle('#s8-cal', 45.6, { y: 260, rotation: '-=6' });

// S9 50-55
tl.fromTo('#s9-img', { scale: 1.15 }, { scale: 1.0, duration: 5.6, ease: 'none' }, 49.4);
pop('#s9-stamp', 50.4);
reveal('#s9-a', 50.8); reveal('#s9-b', 51.3); reveal('#s9-c', 52.0); reveal('#s9-d', 52.8);
tl.to('#series', { opacity: 0, duration: 0.4 }, 49.6);

window.__timelines['main'] = tl;
"""

GRAIN = (
    f'<svg id="grain" viewBox="0 0 {W} {H}"><filter id="n"><feTurbulence type="fractalNoise" baseFrequency=".85" '
    f'numOctaves="2" seed="7"/></filter><rect width="100%" height="100%" filter="url(#n)"/></svg>'
)

page = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width={W}, height={H}" />
<title>Day 2 — Chitrakote Falls</title>
<script src="assets/gsap.min.js"></script>
<style>{CSS}</style>
</head>
<body>
<div id="root" data-composition-id="main" data-width="{W}" data-height="{H}" data-duration="{DUR}">
{"".join(S)}
<div id="series" class="clip" data-start="0" data-duration="{DUR}" data-track-index="20">31 DAYS OF CHHATTISGARH · 02</div>
<div id="grain-wrap" class="clip" data-start="0" data-duration="{DUR}" data-track-index="21" style="position:absolute;inset:0;z-index:50;pointer-events:none">{GRAIN}</div>
<audio id="bgm" src="assets/music.wav" data-start="0" data-duration="{DUR}" data-track-index="30" data-volume="1"></audio>
</div>
<script>{JS}</script>
</body>
</html>
"""

Path(__file__).with_name("index.html").write_text(page, encoding="utf-8")
print("wrote index.html", len(page))
