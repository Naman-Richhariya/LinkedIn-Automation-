"""Day 2 — Chitrakote Falls. High-energy kinetic-typography reel (HyperFrames atelier).

Style follows the client reference: one idea per beat, heavy stacked type revealed
word by word, bold colour fields, B&W photo + colour type, sky-replaced depth layering,
highlight tags, counters and whip transitions. Beats follow the Day 2 VO script.
Run: python build_index.py
"""
import html
import random
from pathlib import Path

W, H = 1080, 1920
DUR = 55
rnd = random.Random(7)

# (id, start, end) — beats, aligned to script lines
BEATS = [
    ("b1", 0.0, 3.0),    # भारत का सबसे चौड़ा जलप्रपात
    ("b2", 3.0, 4.6),    # जोहार!
    ("b3", 4.6, 6.6),    # ये है चित्रकोट
    ("b4", 6.6, 9.0),    # बस्तर · इंद्रावती
    ("b5", 9.0, 12.2),   # जगदलपुर से 40 km
    ("b6", 12.2, 16.0),  # 95 ft
    ("b7", 16.0, 18.0),  # बारिश में
    ("b8", 18.0, 21.2),  # 300 m
    ("b9", 21.2, 23.0),  # भारत का नियाग्रा
    ("b10", 23.0, 27.0), # घोड़े की नाल
    ("b11", 27.0, 31.0), # इंद्रधनुष
    ("b12", 31.0, 38.0), # monsoon vs winter wipe
    ("b13", 38.0, 45.0), # boat
    ("b14", 45.0, 50.0), # best time
    ("b15", 50.0, 55.0), # end card
]
X = 0.3  # transition overlap


def words(text, cls="w"):
    return " ".join(f'<span class="{cls}">{html.escape(t)}</span>' for t in text.split(" "))


def beat(i, bid, start, end, inner, bg="#0B0B0C"):
    s = max(0.0, start - (X if i else 0))
    return (
        f'<section id="{bid}" class="clip beat" data-start="{s:g}" data-duration="{end - s:g}" '
        f'data-track-index="{i + 1}" style="z-index:{i + 1}"><div class="fill" style="background:{bg}"></div>{inner}</section>'
    )


rain = "".join(
    f'<div class="drop" style="left:{rnd.uniform(0, W):.0f}px;top:{rnd.uniform(-400, H):.0f}px;height:{rnd.uniform(60, 160):.0f}px;opacity:{rnd.uniform(.25, .7):.2f}"></div>'
    for _ in range(70)
)
ticks = "".join(f'<div class="tick" style="bottom:{k * 40}px;width:{60 if k % 5 == 0 else 30}px"></div>' for k in range(26))
road = "".join(f'<div class="dash" style="top:{k * 120}px"></div>' for k in range(-2, 18))
months = "".join(f'<div class="mo" id="mo{k}"><b>{m}</b><span>{h}</span></div>' for k, (m, h) in enumerate([("JUL", "जुलाई"), ("AUG", "अगस्त"), ("SEP", "सितंबर"), ("OCT", "अक्टूबर")]))
shoe_dots = "".join(f'<circle cx="{x}" cy="{y}" r="9" fill="#14110F"/>' for x, y in ((70, 100), (70, 170), (330, 100), (330, 170), (115, 300), (285, 300)))

B = {}
B["b1"] = f"""
  <div class="fill" style="background:radial-gradient(120% 70% at 50% 30%,#F0353C 0%,#C8161E 60%,#8E0D12 100%)"></div>
  <div class="center" style="top:250px">
    <div class="H stack white" id="b1-l1">{words('भारत का')}</div>
    <div class="H stack xl white" id="b1-l2">{words('सबसे चौड़ा')}</div>
  </div>
  <div class="center" style="top:815px"><div class="H mega white stack" id="b1-l3">जलप्रपात</div></div>
  <div class="photo-wrap" id="b1-ph" style="top:900px;height:1020px">
    <img class="fgimg bw" id="b1-bw" src="assets/monsoon_fg.png"/>
    <img class="fgimg" id="b1-col" src="assets/monsoon_fg.png"/>
  </div>
  <div class="tag" id="b1-tag" style="left:330px;top:1130px">INDIA'S WIDEST WATERFALL</div>
"""
B["b2"] = f"""
  <div class="center" style="top:640px"><div class="H mega orange" id="b2-a">जोहार!</div></div>
  <div class="center" style="top:1020px"><div class="E small white" id="b2-b">GREETINGS FROM CHHATTISGARH</div></div>
"""
B["b3"] = f"""
  <img class="cover" id="b3-img" src="assets/rainbow.jpg" style="object-position:50% 50%"/>
  <div class="shade"></div>
  <div class="center" style="top:1050px"><div class="H white" id="b3-a">ये है</div></div>
  <div class="center" style="top:1160px"><div class="H xxl white shadowed" id="b3-b">चित्रकोट</div></div>
  <div class="tag" id="b3-tag" style="left:360px;top:1460px">CHITRAKOTE FALLS</div>
"""
B["b4"] = f"""
  <div class="fill grid"></div>
  <div class="card" id="b4-card" style="left:120px;top:560px;width:840px;height:560px;--r:-4deg"><img src="assets/sunset.jpg"/></div>
  <svg class="pin" id="b4-pin" viewBox="0 0 100 140" style="left:470px;top:380px"><path d="M50 0C22 0 0 22 0 50c0 38 50 90 50 90s50-52 50-90C100 22 78 0 50 0z" fill="#F25C1F"/><circle cx="50" cy="48" r="18" fill="#fff"/></svg>
  <div class="label" id="b4-l1" style="left:90px;top:1180px;--r:-3deg">बस्तर</div>
  <div class="label" id="b4-l2" style="left:470px;top:1290px;--r:2deg">इंद्रावती नदी</div>
"""
B["b5"] = f"""
  <div class="fill" style="background:radial-gradient(110% 80% at 50% 20%,#FF7A2F 0%,#E2491A 55%,#9B2B0B 100%)"></div>
  <div class="road" id="b5-road">{road}</div>
  <div class="center" style="top:330px"><div class="H white" id="b5-a">{words('जगदलपुर से')}</div></div>
  <div class="center" style="top:640px"><div class="num white" id="b5-n"><span id="b5-v">0</span><small>KM</small></div></div>
  <div class="center" style="top:1080px"><div class="H yellow" id="b5-b">{words('लगभग चालीस किलोमीटर')}</div></div>
"""
B["b6"] = f"""
  <img class="cover" id="b6-img" src="assets/canoe.jpg" style="object-position:72% 50%"/>
  <div class="shade top"></div>
  <div class="ruler" id="b6-ruler">{ticks}</div>
  <div class="num-sm white" id="b6-n" style="left:200px;top:330px"><span id="b6-v">0</span><small>FT</small></div>
  <div class="center" style="top:1250px"><div class="H white shadowed" id="b6-a">{words('की ऊँचाई से')}</div></div>
  <div class="center" style="top:1380px"><div class="H yellow shadowed" id="b6-b">{words('गिरता है पानी')}</div></div>
"""
B["b7"] = f"""
  <div class="rain" id="b7-rain">{rain}</div>
  <div class="center" style="top:700px"><div class="H mega white" id="b7-a">{words('बारिश में')}</div></div>
  <div class="center" style="top:1030px"><div class="E small sky" id="b7-b">IN THE MONSOON</div></div>
"""
B["b8"] = f"""
  <div class="pan" id="b8-pan"><img src="assets/monsoon.jpg"/></div>
  <div class="shade"></div>
  <div class="arrow" id="b8-arrow"><span class="ah l"></span><span class="ah r"></span></div>
  <div class="center" style="top:420px"><div class="num yellow shadowed" id="b8-n"><span id="b8-v">0</span><small>M</small></div></div>
  <div class="center" style="top:1250px"><div class="H white shadowed" id="b8-a">{words('तक चौड़ाई')}</div></div>
"""
B["b9"] = f"""
  <div class="fill" style="background:radial-gradient(120% 70% at 50% 40%,#F0353C 0%,#B5121A 70%,#6E0A0E 100%)"></div>
  <div class="center" style="top:560px"><div class="H xl white" id="b9-a">{words('भारत का')}</div></div>
  <div class="center" style="top:780px"><div class="H mega yellow" id="b9-b">नियाग्रा!</div></div>
  <div class="tag dark" id="b9-tag" style="left:395px;top:1150px">INDIA'S NIAGARA</div>
"""
B["b10"] = f"""
  <img class="cover" id="b10-img" src="assets/rainbow.jpg" style="object-position:50% 60%"/>
  <div class="shade"></div>
  <svg class="shoe" id="b10-shoe" viewBox="0 0 400 400"><path d="M70 60 L70 220 A130 130 0 0 0 330 220 L330 60" fill="none" stroke="#FFC531" stroke-width="34" stroke-linecap="round"/>{shoe_dots}</svg>
  <div class="center" style="top:1180px"><div class="H white shadowed" id="b10-a">{words('घोड़े की नाल')}</div></div>
  <div class="center" style="top:1310px"><div class="H yellow shadowed" id="b10-b">{words('जैसा आकार')}</div></div>
"""
B["b11"] = f"""
  <img class="cover" id="b11-img" src="assets/rainbow.jpg" style="object-position:45% 62%"/>
  <div class="shade"></div>
  <div class="center" style="top:300px"><div class="H xxl rainbow" id="b11-a">इंद्रधनुष</div></div>
  <div class="center" style="top:1250px"><div class="H white shadowed" id="b11-b" style="font-size:88px">{words('नज़ारा देखते ही बनता है')}</div></div>
"""
B["b12"] = f"""
  <img class="cover" id="b12-w" src="assets/rainbow.jpg" style="object-position:55% 40%"/>
  <div class="wipe" id="b12-wipe"><div class="wipe-in" id="b12-in"><img class="cover" src="assets/monsoon.jpg" style="object-position:40% 50%"/></div></div>
  <div class="divider" id="b12-div"></div>
  <div class="seasontag" id="b12-t1" style="top:360px"><b>मानसून</b><span>मिट्टी&nbsp;जैसा&nbsp;भूरा</span></div>
  <div class="seasontag light" id="b12-t2" style="top:360px"><b>सर्दी</b><span>दूध&nbsp;जैसा&nbsp;सफ़ेद</span></div>
"""
B["b13"] = f"""
  <img class="cover" id="b13-img" src="assets/canoe.jpg" style="object-position:70% 70%"/>
  <div class="shade"></div>
  <div class="center" style="top:300px"><div class="H xl white shadowed" id="b13-a">{words('नाव से')}</div></div>
  <div class="center" style="top:1220px"><div class="H white shadowed" id="b13-b">{words('झरने के')}</div></div>
  <div class="center" style="top:1350px"><div class="H yellow shadowed" id="b13-c">{words('बेहद करीब')}</div></div>
  <div class="tag" id="b13-tag" style="left:390px;top:520px">BOAT RIDES</div>
"""
B["b14"] = f"""
  <img class="cover dim" id="b14-img" src="assets/sunset.jpg" style="object-position:50% 50%"/>
  <div class="center" style="top:330px"><div class="H white" id="b14-a">{words('घूमने का सबसे')}</div></div>
  <div class="center" style="top:460px"><div class="H xl yellow" id="b14-b">{words('अच्छा समय')}</div></div>
  <div class="months" id="b14-m">{months}</div>
  <div class="center" style="top:1330px"><div class="E small white" id="b14-c">BEST FLOW · JULY TO OCTOBER</div></div>
"""
B["b15"] = f"""
  <img class="cover" id="b15-img" src="assets/night.jpg" style="object-position:38% 50%"/>
  <div class="shade"></div>
  <div class="center" style="top:300px"><div class="E small white" id="b15-k">31 DAYS OF CHHATTISGARH</div></div>
  <div class="center" style="top:380px"><div class="num white" id="b15-n"><span id="b15-v">01</span><small>/31</small></div></div>
  <div class="center" style="top:1120px"><div class="H white shadowed" id="b15-a">{words('कल: तीरथगढ़')}</div></div>
  <div class="center" style="top:1250px"><div class="H xl orange shadowed" id="b15-b">{words('सबले बढ़िया!')}</div></div>
  <div class="tag" id="b15-tag" style="left:300px;top:1480px">#31DaysOfChhattisgarh</div>
"""

bg_override = {"b4": "#0E5E5E"}
sections = "\n".join(beat(i, bid, s, e, B[bid], bg_override.get(bid, "#0B0B0C")) for i, (bid, s, e) in enumerate(BEATS))

FONTS = """
@font-face{font-family:NotoDeva;font-weight:900;src:url(assets/noto-sans-devanagari-devanagari-900-normal.woff2) format('woff2')}
@font-face{font-family:NotoDeva;font-weight:700;src:url(assets/noto-sans-devanagari-devanagari-700-normal.woff2) format('woff2')}
@font-face{font-family:Archivo;src:url(assets/archivo-black-latin-400-normal.woff2) format('woff2')}
@font-face{font-family:InterX;font-weight:900;src:url(assets/inter-latin-900-normal.woff2) format('woff2')}
@font-face{font-family:InterX;font-weight:600;src:url(assets/inter-latin-600-normal.woff2) format('woff2')}
"""
CSS = FONTS + f"""
html,body{{margin:0;background:#0B0B0C}}
#root{{position:relative;width:{W}px;height:{H}px;overflow:hidden;background:#0B0B0C}}
.beat{{position:absolute;inset:0;overflow:hidden}}
.fill{{position:absolute;inset:0}}
.center{{position:absolute;left:0;width:{W}px;display:flex;flex-direction:column;align-items:center;text-align:center;padding:0 50px;box-sizing:border-box}}
.H{{font-family:NotoDeva,sans-serif;font-weight:900;font-size:110px;line-height:1.15;letter-spacing:-1px}}
.H.xl{{font-size:150px}} .H.xxl{{font-size:190px;line-height:1.1}} .H.mega{{font-size:230px;line-height:1.1}}
.E{{font-family:Archivo,sans-serif;text-transform:uppercase;letter-spacing:1px}}
.E.small{{font-size:40px;letter-spacing:6px}}
.w{{display:inline-block}}
.white{{color:#FFFFFF}} .yellow{{color:#FFC531}} .orange{{color:#FF6A1F}} .sky{{color:#7CC8FF}}
.shadowed{{text-shadow:0 6px 0 rgba(0,0,0,.25),0 16px 40px rgba(0,0,0,.55)}}
.stack{{text-shadow:0 8px 0 rgba(90,0,0,.35)}}
.rainbow{{background:linear-gradient(90deg,#FF4D4D,#FF9F1C,#FFE14D,#5BE37D,#4DB8FF,#9B6BFF);-webkit-background-clip:text;background-clip:text;color:transparent;filter:drop-shadow(0 10px 24px rgba(0,0,0,.6))}}
.tag{{position:absolute;padding:14px 26px;background:#FFC531;color:#111;font-family:InterX,sans-serif;font-weight:900;font-size:30px;letter-spacing:2px;white-space:nowrap;box-shadow:0 10px 24px rgba(0,0,0,.35)}}
.tag.dark{{background:#111;color:#FFC531}}
.label{{position:absolute;padding:10px 30px 18px;background:#FFC531;color:#111;font-family:NotoDeva,sans-serif;font-weight:900;font-size:84px;transform:rotate(var(--r));box-shadow:0 14px 30px rgba(0,0,0,.35);white-space:nowrap}}
.photo-wrap{{position:absolute;left:-360px;width:1800px}}
.fgimg{{position:absolute;left:0;top:0;width:100%;height:auto}}
.bw{{filter:grayscale(1) contrast(1.15)}}
.cover{{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}}
.dim{{filter:brightness(.45)}}
.shade{{position:absolute;inset:0;background:linear-gradient(180deg,rgba(0,0,0,.45) 0%,rgba(0,0,0,0) 30%,rgba(0,0,0,0) 50%,rgba(0,0,0,.75) 100%)}}
.shade.top{{background:linear-gradient(180deg,rgba(0,0,0,.6) 0%,rgba(0,0,0,0) 40%,rgba(0,0,0,0) 55%,rgba(0,0,0,.75) 100%)}}
.grid{{background-color:#0E5E5E;background-image:linear-gradient(rgba(255,255,255,.12) 2px,transparent 2px),linear-gradient(90deg,rgba(255,255,255,.12) 2px,transparent 2px);background-size:90px 90px}}
.card{{position:absolute;background:#fff;padding:16px;box-sizing:border-box;transform:rotate(var(--r));box-shadow:0 30px 60px rgba(0,0,0,.45)}}
.card img{{width:100%;height:100%;object-fit:cover;display:block}}
.pin{{position:absolute;width:140px;height:196px;filter:drop-shadow(0 14px 18px rgba(0,0,0,.4))}}
.num{{font-family:Archivo,sans-serif;font-size:330px;line-height:1;letter-spacing:-6px;display:flex;align-items:baseline}}
.num small{{font-size:110px;margin-left:16px;letter-spacing:0}}
.num-sm{{position:absolute;font-family:Archivo,sans-serif;font-size:200px;line-height:1;display:flex;align-items:baseline;text-shadow:0 10px 30px rgba(0,0,0,.5)}}
.num-sm small{{font-size:80px;margin-left:12px}}
.road{{position:absolute;left:510px;top:0;width:60px;height:{H}px;opacity:.18}}
.dash{{position:absolute;left:0;width:60px;height:70px;background:#FFE3C9;border-radius:8px}}
.ruler{{position:absolute;left:90px;bottom:560px;width:80px;height:1040px;border-left:10px solid #FFC531;transform-origin:50% 100%}}
.tick{{position:absolute;left:0;height:8px;background:#FFC531}}
.rain{{position:absolute;inset:0}}
.drop{{position:absolute;width:4px;background:linear-gradient(180deg,rgba(124,200,255,0),#7CC8FF);border-radius:2px}}
.pan{{position:absolute;top:0;left:0;height:{H}px}}
.pan img{{height:{H}px;width:auto;display:block}}
.arrow{{position:absolute;left:60px;top:1110px;width:960px;height:10px;background:#FFC531;transform-origin:50% 50%}}
.ah{{position:absolute;top:-22px;width:0;height:0;border-top:27px solid transparent;border-bottom:27px solid transparent}}
.ah.l{{left:-30px;border-right:40px solid #FFC531}} .ah.r{{right:-30px;border-left:40px solid #FFC531}}
.shoe{{position:absolute;left:290px;top:320px;width:500px;height:500px;filter:drop-shadow(0 18px 30px rgba(0,0,0,.5))}}
.wipe{{position:absolute;inset:0;overflow:hidden}}
.wipe-in{{position:absolute;inset:0}}
.divider{{position:absolute;top:0;left:{W}px;width:12px;margin-left:-6px;height:{H}px;background:#FFC531;box-shadow:0 0 30px rgba(0,0,0,.5)}}
.seasontag{{position:absolute;white-space:nowrap;left:70px;padding:20px 34px 26px;background:#6B3E1E;color:#fff;font-family:NotoDeva,sans-serif;font-weight:900;box-shadow:0 18px 40px rgba(0,0,0,.4)}}
.seasontag b{{display:block;font-size:110px;line-height:1.1}} .seasontag span{{display:block;font-size:56px;color:#FFD9A8;white-space:nowrap}}
.seasontag.light{{left:auto;right:70px;background:#F4F7FA;color:#111}} .seasontag.light span{{color:#2C6E9E}}
.months{{position:absolute;left:90px;top:780px;width:900px;display:grid;grid-template-columns:repeat(2,1fr);gap:28px}}
.mo{{height:220px;background:#FFC531;color:#111;display:flex;flex-direction:column;align-items:center;justify-content:center;box-shadow:0 16px 34px rgba(0,0,0,.4)}}
.mo b{{font-family:Archivo,sans-serif;font-size:110px;line-height:1}} .mo span{{font-family:NotoDeva,sans-serif;font-weight:700;font-size:44px}}
#grain{{position:absolute;inset:0;opacity:.09;mix-blend-mode:overlay;pointer-events:none}}
#vig{{position:absolute;inset:0;pointer-events:none;background:radial-gradient(130% 90% at 50% 50%,rgba(0,0,0,0) 60%,rgba(0,0,0,.45) 100%)}}
"""

JS = """
window.__timelines = window.__timelines || {};
const tl = gsap.timeline({ paused: true });
const X = 0.3;
const S = {b1:0,b2:3,b3:4.6,b4:6.6,b5:9,b6:12.2,b7:16,b8:18,b9:21.2,b10:23,b11:27,b12:31,b13:38,b14:45,b15:50};
// whip-style entrances, alternating
const ent = {b2:{yPercent:100}, b3:{scale:1.6,opacity:0}, b4:{xPercent:100}, b5:{yPercent:-100}, b6:{scale:0.6,opacity:0},
  b7:{yPercent:100}, b8:{xPercent:-100}, b9:{scale:1.8,opacity:0}, b10:{yPercent:100}, b11:{scale:0.7,opacity:0},
  b12:{xPercent:100}, b13:{yPercent:-100}, b14:{scale:1.5,opacity:0}, b15:{yPercent:100}};
for (const id in ent) tl.from('#' + id, Object.assign({ duration: X, ease: 'expo.out' }, ent[id]), S[id] - X);

const pop = (sel, t, st) => tl.from(sel, { scale: 1.6, opacity: 0, y: 40, duration: 0.35, ease: 'back.out(2.2)', stagger: st || 0.12 }, t);
const rise = (sel, t, st) => tl.from(sel, { yPercent: 80, opacity: 0, duration: 0.4, ease: 'power4.out', stagger: st || 0.1 }, t);
const slam = (sel, t) => tl.from(sel, { scale: 3, opacity: 0, duration: 0.28, ease: 'power4.in' }, t);
const tag = (sel, t) => tl.from(sel, { scaleX: 0, transformOrigin: '0% 50%', duration: 0.3, ease: 'power3.out' }, t);
const push = (sel, t0, t1, a, b) => tl.fromTo(sel, Object.assign({ scale: 1.0 }, a || {}), Object.assign({ scale: 1.12, duration: t1 - t0, ease: 'none' }, b || {}), t0);
const count = (id, to, t, d, pad) => { const o = { v: 0 }; const el = document.getElementById(id);
  tl.to(o, { v: to, duration: d, ease: 'power2.out', onUpdate: () => { const v = Math.round(o.v); el.textContent = pad ? String(v).padStart(2, '0') : v; } }, t); };

// b1 0–3
pop('#b1-l1 .w', 0.15); pop('#b1-l2 .w', 0.55, 0.15);
tl.fromTo('#b1-ph', { y: 120, scale: 1.05 }, { y: 0, scale: 1.0, duration: 3, ease: 'power2.out' }, 0);
tl.fromTo('#b1-col', { opacity: 0 }, { opacity: 1, duration: 0.25 }, 1.7);
tl.to(['#b1-l1', '#b1-l2'], { y: -60, opacity: 0, duration: 0.25, ease: 'power2.in' }, 1.6);
slam('#b1-l3', 1.75); tag('#b1-tag', 2.15);

// b2 3–4.6
slam('#b2-a', 3.0); rise('#b2-b', 3.35);
tl.to('#b2-a', { scale: 1.06, duration: 1.2, ease: 'none' }, 3.3);

// b3 4.6–6.6
push('#b3-img', 4.3, 6.9); rise('#b3-a', 4.75); slam('#b3-b', 5.0); tag('#b3-tag', 5.4);

// b4 6.6–9
tl.from('#b4-card', { y: 900, rotation: 18, duration: 0.6, ease: 'back.out(1.2)' }, 6.4);
tl.from('#b4-pin', { y: -500, duration: 0.45, ease: 'bounce.out' }, 7.0);
tl.from('#b4-l1', { scale: 0, rotation: -20, duration: 0.35, ease: 'back.out(2)' }, 7.3);
tl.from('#b4-l2', { scale: 0, rotation: 20, duration: 0.35, ease: 'back.out(2)' }, 7.8);
tl.to('#b4-card', { rotation: -1, scale: 1.04, duration: 2.2, ease: 'none' }, 7.0);

// b5 9–12.2
tl.fromTo('#b5-road', { y: -240 }, { y: 0, duration: 3.5, ease: 'none' }, 8.8);
rise('#b5-a .w', 9.1); tl.from('#b5-n', { scale: 0.6, opacity: 0, duration: 0.35, ease: 'back.out(2)' }, 9.4);
count('b5-v', 40, 9.5, 1.4); pop('#b5-b .w', 10.6, 0.12);

// b6 12.2–16
push('#b6-img', 11.9, 16.3, { yPercent: 2 }, { yPercent: -2 });
tl.from('#b6-ruler', { scaleY: 0, duration: 1.6, ease: 'power2.out' }, 12.4);
tl.from('#b6-n', { opacity: 0, x: -40, duration: 0.3 }, 12.5); count('b6-v', 95, 12.5, 1.6);
rise('#b6-a .w', 13.6); rise('#b6-b .w', 14.2);

// b7 16–18
tl.fromTo('#b7-rain .drop', { y: -300 }, { y: 700, duration: 2.3, ease: 'none' }, 15.7);
pop('#b7-a .w', 16.1, 0.18); rise('#b7-b', 16.6);

// b8 18–21.2 — pan across the full width of the falls
tl.fromTo('#b8-pan', { x: 0 }, { x: -2336, duration: 3.5, ease: 'power1.inOut' }, 17.7);
tl.from('#b8-arrow', { scaleX: 0, duration: 0.6, ease: 'power3.out' }, 18.2);
tl.from('#b8-n', { scale: 0.5, opacity: 0, duration: 0.3, ease: 'back.out(2)' }, 18.2);
count('b8-v', 300, 18.3, 1.5); rise('#b8-a .w', 19.4);

// b9 21.2–23
pop('#b9-a .w', 21.3, 0.12); slam('#b9-b', 21.7); tag('#b9-tag', 22.1);
tl.fromTo('#b9-b', { x: -8 }, { x: 8, duration: 0.05, repeat: 5, yoyo: true, ease: 'none' }, 21.98);

// b10 23–27
push('#b10-img', 22.7, 27.3);
tl.from('#b10-shoe', { scale: 0, rotation: -30, duration: 0.6, ease: 'back.out(1.8)' }, 23.4);
tl.to('#b10-shoe', { rotation: 6, duration: 2.5, ease: 'sine.inOut' }, 24.0);
rise('#b10-a .w', 23.8); pop('#b10-b .w', 24.5, 0.14);

// b11 27–31
tl.fromTo('#b11-img', { scale: 1.0 }, { scale: 1.35, duration: 4.3, ease: 'power1.inOut' }, 26.7);
slam('#b11-a', 27.3); rise('#b11-b .w', 28.6, 0.12);

// b12 31–38 — season wipe
tl.from('#b12-t1', { x: -500, duration: 0.45, ease: 'power3.out' }, 31.4);
tl.from('#b12-t1 span', { opacity: 0, y: 20, duration: 0.3 }, 31.8);
tl.to('#b12-t1', { x: -700, duration: 0.35, ease: 'power3.in' }, 34.0);
tl.fromTo('#b12-wipe', { xPercent: 0 }, { xPercent: -100, duration: 0.9, ease: 'power3.inOut' }, 34.3);
tl.fromTo('#b12-in', { xPercent: 0 }, { xPercent: 100, duration: 0.9, ease: 'power3.inOut' }, 34.3);
tl.fromTo('#b12-div', { x: 0 }, { x: -1080, duration: 0.9, ease: 'power3.inOut' }, 34.3);
tl.from('#b12-t2', { x: 600, duration: 0.45, ease: 'power3.out' }, 35.1);
tl.from('#b12-t2 span', { opacity: 0, y: 20, duration: 0.3 }, 35.5);
tl.fromTo('#b12-w', { scale: 1.08 }, { scale: 1.0, duration: 7.3, ease: 'none' }, 30.7);

// b13 38–45
tl.fromTo('#b13-img', { scale: 1.0 }, { scale: 1.25, duration: 7.3, ease: 'none' }, 37.7);
slam('#b13-a', 38.2); tag('#b13-tag', 38.6);
rise('#b13-b .w', 39.5); pop('#b13-c .w', 40.2, 0.14);

// b14 45–50
push('#b14-img', 44.7, 50.3);
rise('#b14-a .w', 45.1); pop('#b14-b .w', 45.6, 0.14);
for (let k = 0; k < 4; k++) tl.from('#mo' + k, { scale: 0, rotation: k % 2 ? 8 : -8, duration: 0.35, ease: 'back.out(2.2)' }, 46.4 + k * 0.35);
rise('#b14-c', 48.0);

// b15 50–55
push('#b15-img', 49.7, 55);
rise('#b15-k', 50.2); tl.from('#b15-n', { scale: 0.6, opacity: 0, duration: 0.35, ease: 'back.out(2)' }, 50.4);
count('b15-v', 2, 50.5, 0.6, true);
rise('#b15-a .w', 51.4); pop('#b15-b .w', 52.2, 0.18); tag('#b15-tag', 53.0);

window.__timelines['main'] = tl;
"""

GRAIN = (
    f'<svg id="grain" viewBox="0 0 {W} {H}"><filter id="n"><feTurbulence type="fractalNoise" baseFrequency=".9" '
    f'numOctaves="2" seed="11"/></filter><rect width="100%" height="100%" filter="url(#n)"/></svg>'
)

page = f"""<!doctype html>
<html lang="hi">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width={W}, height={H}" />
<title>Day 2 — Chitrakote Falls</title>
<script src="assets/gsap.min.js"></script>
<style>{CSS}</style>
</head>
<body>
<div id="root" data-composition-id="main" data-width="{W}" data-height="{H}" data-duration="{DUR}">
{sections}
<div id="fx" class="clip" data-start="0" data-duration="{DUR}" data-track-index="40" style="position:absolute;inset:0;z-index:80;pointer-events:none"><div id="vig"></div>{GRAIN}</div>
<audio id="bgm" src="assets/music.wav" data-start="0" data-duration="{DUR}" data-track-index="50" data-volume="1"></audio>
</div>
<script>{JS}</script>
</body>
</html>
"""
Path(__file__).with_name("index.html").write_text(page, encoding="utf-8")
print("wrote index.html", len(page))
