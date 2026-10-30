"""Builds index.html for the Chhattisgarh reel (atelier HyperFrames composition).

Text that animates per-letter is pre-split here so the page needs no DOM
mutation at load time. Run: python build_index.py  (writes index.html beside it)
"""
import html
import math
import random
from pathlib import Path

W, H = 1080, 1920
BOUNDS = [0, 4, 10, 16, 22, 28, 34, 40, 46, 52, 60]
OVERLAP = 0.4
rnd = random.Random(36)


def sp(text, cls="ch"):
    """Split Latin text into per-letter inline-block spans (spaces kept)."""
    out = []
    for c in text:
        if c == " ":
            out.append('<span class="sp"> </span>')
        else:
            out.append(f'<span class="{cls}">{html.escape(c)}</span>')
    return "".join(out)


def words(text, cls="wd"):
    """Split into word spans (safe for Devanagari conjuncts)."""
    return " ".join(f'<span class="{cls}">{html.escape(w)}</span>' for w in text.split(" "))


def scene(i, inner, bg):
    start = BOUNDS[i - 1] - (OVERLAP if i > 1 else 0)
    dur = BOUNDS[i] - start
    return (
        f'<section id="s{i}" class="clip scene" data-start="{start:g}" data-duration="{dur:g}" '
        f'data-track-index="{i}" style="z-index:{i}">\n'
        f'  <div class="bg" style="background:{bg}"></div>\n{inner}\n</section>'
    )


# ---------- reusable SVG bits ----------
def fort_icon(x, y, s, fill):
    # crenellated fort silhouette, 100x80 box
    return (
        f'<g class="fort" transform="translate({x},{y}) scale({s})"><g class="fort-in">'
        f'<path d="M0 80 V30 H12 V18 H22 V30 H34 V10 H44 V0 H56 V10 H66 V30 H78 V18 H88 V30 H100 V80 Z" fill="{fill}"/>'
        f'<path d="M42 80 V58 a8 8 0 0 1 16 0 V80 Z" fill="#14213D"/></g></g>'
    )


def sal_tree(x, base, h, fill, trunk="#3B2A1E"):
    w = h * 0.55
    blobs = "".join(
        f'<ellipse cx="{x + dx * w:.1f}" cy="{base - h + dy * h:.1f}" rx="{r * w:.1f}" ry="{r * w * 0.8:.1f}" fill="{fill}"/>'
        for dx, dy, r in ((0, 0.12, 0.42), (-0.28, 0.28, 0.34), (0.28, 0.3, 0.34), (0, 0.42, 0.36))
    )
    return (
        f'<g class="tree"><rect x="{x - h * 0.03:.1f}" y="{base - h * 0.55:.1f}" width="{h * 0.06:.1f}" '
        f'height="{h * 0.55:.1f}" fill="{trunk}"/>{blobs}</g>'
    )


def dot_border(color, n=46, y=0, r=5):
    return "".join(f'<circle cx="{12 + k * 23.2:.1f}" cy="{y}" r="{r}" fill="{color}"/>' for k in range(n))


# ---------- scenes ----------
forts = "".join(
    fort_icon(90 + (k % 6) * 155, 330 + (k // 6) * 120, 1.0, "#E8A93B" if k != 14 else "#C2502A")
    for k in range(36)
)
S1 = scene(1, f"""
  <svg class="full" viewBox="0 0 {W} {H}">{forts}</svg>
  <div class="center col" style="justify-content:flex-start;padding-top:1120px">
    <div id="s1-count" class="label gold">छत्तीस + गढ़ &nbsp;=&nbsp; 36 FORTS</div>
    <h1 id="s1-title" class="display" style="font-size:150px">{sp("CHHATTISGARH")}</h1>
    <div id="s1-hi" class="hindi cream" style="font-size:96px;margin-top:10px">छत्तीसगढ़</div>
  </div>""", "#14213D")

rays = "".join(
    f'<rect class="ray" x="537" y="300" width="6" height="520" fill="#F4E9D8" opacity=".35" '
    f'transform="rotate({-80 + k * 10} 540 1140)"/>' for k in range(17)
)
S2 = scene(2, f"""
  <svg class="full" viewBox="0 0 {W} {H}">
    <g id="s2-rays">{rays}</g>
    <circle id="s2-sun" cx="540" cy="1140" r="260" fill="#E8A93B"/>
    <rect x="0" y="1140" width="{W}" height="{H - 1140}" fill="#8E3B1F"/>
    <g opacity=".5">{dot_border("#F4E9D8", y=1170, r=6)}</g>
  </svg>
  <div class="center col" style="justify-content:flex-start;padding-top:300px">
    <div class="label cream" id="s2-k">BORN · 1 NOVEMBER 2000</div>
    <div class="display cream" style="font-size:300px;line-height:1" id="s2-year">2000</div>
  </div>
  <div class="center col" style="justify-content:flex-start;padding-top:1250px">
    <div class="serif cream" style="font-size:84px" id="s2-l1">India's <em>26th</em> state</div>
    <div class="body cream" style="font-size:44px;opacity:.85;margin-top:24px" id="s2-l2">Carved from Madhya Pradesh · Capital: Raipur</div>
    <div class="pill" id="s2-pill">26 YEARS YOUNG</div>
  </div>""", "#C2502A")

trees_back = "".join(sal_tree(60 + k * 120 + rnd.uniform(-20, 20), 1560, rnd.uniform(380, 480), "#2E6B4F") for k in range(9))
trees_front = "".join(sal_tree(-20 + k * 170 + rnd.uniform(-25, 25), 1800, rnd.uniform(520, 640), "#173D2E", "#24170F") for k in range(8))
flies = "".join(
    f'<circle class="fly" cx="{rnd.uniform(60, 1020):.0f}" cy="{rnd.uniform(1000, 1700):.0f}" r="{rnd.uniform(4, 8):.1f}" fill="#F7E27A"/>'
    for _ in range(26)
)
S3 = scene(3, f"""
  <svg class="full" viewBox="0 0 {W} {H}">
    <g id="s3-back">{trees_back}</g>
    <rect x="0" y="1560" width="{W}" height="400" fill="#1F4D3A"/>
    <g id="s3-front">{trees_front}</g>
    <g id="s3-flies">{flies}</g>
  </svg>
  <div class="center col" style="justify-content:flex-start;padding-top:280px">
    <div class="label gold" id="s3-k">GREEN HEART OF INDIA</div>
    <div class="display cream" style="font-size:330px;line-height:1" id="s3-num">40%+</div>
    <div class="serif cream" style="font-size:72px;max-width:860px;text-align:center" id="s3-l1">of the land is <em>forest</em></div>
    <div class="body cream" style="font-size:40px;opacity:.85;margin-top:22px" id="s3-l2">Sal · teak · tendu · mahua</div>
  </div>""", "#1F4D3A")

streaks = "".join(
    f'<rect x="{rnd.uniform(250, 830):.0f}" y="{rnd.uniform(0, 1600):.0f}" width="{rnd.uniform(4, 12):.0f}" '
    f'height="{rnd.uniform(90, 260):.0f}" rx="4" fill="#FFFFFF" opacity="{rnd.uniform(.35, .9):.2f}"/>'
    for _ in range(90)
)
mist = "".join(
    f'<circle class="mist" cx="{250 + k * 75}" cy="{1510 + (k % 3) * 25}" r="{rnd.uniform(70, 120):.0f}" fill="#FFFFFF" opacity=".55"/>'
    for k in range(9)
)
S4 = scene(4, f"""
  <svg class="full" viewBox="0 0 {W} {H}">
    <defs><clipPath id="s4-clip"><path d="M230 900 Q540 820 850 900 L850 1520 L230 1520 Z"/></clipPath></defs>
    <path d="M0 860 Q540 760 1080 860 L1080 {H} L0 {H} Z" fill="#5A3A28"/>
    <path d="M0 860 Q540 760 1080 860 L1080 900 Q540 800 0 900 Z" fill="#2E6B4F"/>
    <path d="M230 900 Q540 820 850 900 L850 1520 L230 1520 Z" fill="#9EC9D6"/>
    <g clip-path="url(#s4-clip)"><g id="s4-water">{streaks}<g transform="translate(0,-1600)">{streaks}</g></g></g>
    <rect x="0" y="1500" width="{W}" height="420" fill="#2B6A84"/>
    <g id="s4-mist">{mist}</g>
  </svg>
  <div class="center col" style="justify-content:flex-start;padding-top:260px">
    <div class="label cream" id="s4-k">BASTAR · INDRAVATI RIVER</div>
    <h2 class="display cream" style="font-size:132px" id="s4-t">{sp("CHITRAKOTE")}</h2>
    <div class="serif gold" style="font-size:76px" id="s4-s">the <em>Niagara</em> of India</div>
    <div class="body cream" style="font-size:42px;margin-top:18px" id="s4-f">India's widest waterfall</div>
  </div>""", "#1D4E63")

stalks = []
for k in range(16):
    x = 40 + k * 66 + rnd.uniform(-10, 10)
    h = rnd.uniform(420, 560)
    grains = "".join(
        f'<ellipse cx="{x + 14 * math.sin(j * 0.5):.0f}" cy="{1700 - h + j * 26:.0f}" rx="9" ry="16" fill="#E8A93B" '
        f'transform="rotate({25 if j % 2 else -25} {x + 14 * math.sin(j * 0.5):.0f} {1700 - h + j * 26:.0f})"/>'
        for j in range(7)
    )
    stalks.append(
        f'<g class="stalk" data-o="{x:.0f} 1700"><path d="M{x:.0f} 1700 Q{x - 10:.0f} {1700 - h / 2:.0f} {x:.0f} {1700 - h:.0f}" '
        f'stroke="#6B8F3A" stroke-width="6" fill="none"/>{grains}</g>'
    )
rice = "".join(
    f'<ellipse cx="{540 + rnd.uniform(-190, 190):.0f}" cy="{1010 + rnd.uniform(-60, 20):.0f}" rx="7" ry="13" fill="#FFFDF5" '
    f'transform="rotate({rnd.uniform(0, 180):.0f} 540 1000)"/>' for _ in range(0)
)
grains_mound = "".join(
    f'<ellipse class="grain" cx="{x:.0f}" cy="{y:.0f}" rx="8" ry="14" fill="#FFFDF5" stroke="#E6DCC4" stroke-width="2" '
    f'transform="rotate({rnd.uniform(0, 180):.0f} {x:.0f} {y:.0f})"/>'
    for x, y in ((540 + rnd.uniform(-1, 1) * 230 * math.sqrt(1 - t * t), 1020 - t * 120) for t in (rnd.uniform(0, 1) for _ in range(120)))
)
S5 = scene(5, f"""
  <svg class="full" viewBox="0 0 {W} {H}">
    <g id="s5-stalks">{"".join(stalks)}</g>
    <g id="s5-bowl">
      {grains_mound}
      <path d="M260 1010 H820 Q810 1230 540 1250 Q270 1230 260 1010 Z" fill="#C2502A"/>
      <path d="M260 1010 H820" stroke="#8E3B1F" stroke-width="14" stroke-linecap="round"/>
      <g opacity=".6">{"".join(f'<circle cx="{330 + k * 52}" cy="1100" r="7" fill="#F4E9D8"/>' for k in range(9))}</g>
    </g>
  </svg>
  <div class="center col" style="justify-content:flex-start;padding-top:280px">
    <div class="hindi ink" style="font-size:124px" id="s5-hi">{words("धान का कटोरा")}</div>
    <div class="serif ink" style="font-size:78px;text-align:center;max-width:900px" id="s5-en">The <em>Rice Bowl</em> of India</div>
    <div class="body ink" style="font-size:40px;opacity:.75;margin-top:20px" id="s5-s">Thousands of native rice varieties</div>
  </div>""", "#F4E9D8")

flames = "".join(
    f'<g class="flame" transform="translate({rnd.uniform(40, 1040):.0f},{rnd.uniform(1680, 1890):.0f})">'
    f'<path d="M0 0 Q-14 -20 0 -46 Q14 -20 0 0 Z" fill="#F7C04A"/><ellipse cx="0" cy="4" rx="16" ry="7" fill="#8E3B1F"/></g>'
    for _ in range(22)
)


def wheel(cx, cy, r):
    spokes = "".join(f'<line x1="{cx}" y1="{cy - r}" x2="{cx}" y2="{cy + r}" stroke="#E8A93B" stroke-width="8" transform="rotate({a} {cx} {cy})"/>' for a in range(0, 180, 30))
    return f'<g class="wheel" data-o="{cx} {cy}"><circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="#E8A93B" stroke-width="16"/>{spokes}<circle cx="{cx}" cy="{cy}" r="16" fill="#E8A93B"/></g>'


S6 = scene(6, f"""
  <svg class="full" viewBox="0 0 {W} {H}">
    <g id="s6-rath">
      <path d="M300 1080 L540 760 L780 1080 Z" fill="#E8A93B"/>
      <path d="M380 1080 L540 860 L700 1080 Z" fill="#C2502A"/>
      <rect x="520" y="700" width="40" height="70" fill="#E8A93B"/><path d="M560 700 L640 720 L560 740 Z" fill="#F4E9D8"/>
      <rect x="250" y="1080" width="580" height="190" fill="#3B1410" stroke="#E8A93B" stroke-width="10"/>
      <g opacity=".8">{"".join(f'<circle cx="{290 + k * 50}" cy="1175" r="10" fill="#E8A93B"/>' for k in range(11))}</g>
      {wheel(360, 1330, 95)}{wheel(720, 1330, 95)}
    </g>
    <g id="s6-flames">{flames}</g>
  </svg>
  <div class="center col" style="justify-content:flex-start;padding-top:250px">
    <div class="label gold" id="s6-k">BASTAR DUSSEHRA</div>
    <div class="display cream" style="font-size:240px;line-height:1" id="s6-num">75 DAYS</div>
  </div>
  <div class="center col" style="justify-content:flex-start;padding-top:1440px">
    <div class="serif cream" style="font-size:60px;text-align:center;max-width:900px" id="s6-l1">One of the <em>longest festivals</em> on Earth</div>
    <div class="body cream" style="font-size:38px;opacity:.85;margin-top:18px" id="s6-l2">in honour of Maa Danteshwari</div>
  </div>""", "#7A1F1A")

coil = "".join(f'<circle cx="{x}" cy="{y}" r="5" fill="#5A3A14" opacity=".55"/>' for x in range(380, 720, 22) for y in (1000, 1030))
S7 = scene(7, f"""
  <svg class="full" viewBox="0 0 {W} {H}">
    <defs>
      <linearGradient id="bronze" x1="0" x2="1" y1="0" y2="1">
        <stop offset="0" stop-color="#F2C46B"/><stop offset=".5" stop-color="#B9792C"/><stop offset="1" stop-color="#6B4012"/>
      </linearGradient>
      <clipPath id="s7-clip"><rect x="0" y="0" width="{W}" height="{H}"/></clipPath>
    </defs>
    <g id="s7-horse">
      <ellipse cx="550" cy="1010" rx="210" ry="95" fill="url(#bronze)"/>
      {coil}
      <path d="M680 950 Q720 860 770 820 L860 860 Q880 900 850 915 L800 900 Q770 960 760 1010 Z" fill="url(#bronze)"/>
      <path d="M770 822 L768 770 L795 812 Z M790 830 L798 778 L815 830 Z" fill="url(#bronze)"/>
      <path d="M690 930 Q720 860 765 822" stroke="#5A3A14" stroke-width="10" stroke-dasharray="2 14" stroke-linecap="round" fill="none"/>
      <circle cx="815" cy="852" r="9" fill="#2A1A08"/>
      <path d="M350 970 Q280 990 290 1110" stroke="url(#bronze)" stroke-width="22" fill="none" stroke-linecap="round"/>
      <rect x="400" y="1070" width="34" height="230" rx="12" fill="url(#bronze)"/>
      <rect x="470" y="1080" width="34" height="220" rx="12" fill="url(#bronze)"/>
      <rect x="610" y="1080" width="34" height="220" rx="12" fill="url(#bronze)"/>
      <rect x="680" y="1070" width="34" height="230" rx="12" fill="url(#bronze)"/>
      <g fill="none" stroke="#5A3A14" stroke-width="5" opacity=".6">
        <path d="M480 960 a26 26 0 1 1 1 0"/><path d="M560 960 a26 26 0 1 1 1 0"/><path d="M640 960 a26 26 0 1 1 1 0"/>
      </g>
      <rect x="330" y="1300" width="420" height="30" rx="10" fill="#6B4012"/>
    </g>
    <g clip-path="url(#s7-clip)"><rect id="s7-shine" x="-300" y="600" width="120" height="900" fill="#FFF6DA" opacity=".35" transform="skewX(-20)"/></g>
  </svg>
  <div class="center col" style="justify-content:flex-start;padding-top:260px">
    <div class="label gold" id="s7-k">BASTAR'S BELL-METAL ART</div>
    <h2 class="display" style="font-size:210px;color:#F2C46B" id="s7-t">{sp("DHOKRA")}</h2>
  </div>
  <div class="center col" style="justify-content:flex-start;padding-top:1440px">
    <div class="serif cream" style="font-size:62px;text-align:center" id="s7-l1">Lost-wax casting,</div>
    <div class="serif cream" style="font-size:62px;text-align:center" id="s7-l2">a <em>4,000-year-old</em> craft</div>
  </div>""", "#17110B")

bricks = []
rows = 22
for r in range(rows):
    y = 1500 - (r + 1) * 30
    half = 300 - r * 11 if r < 18 else 300 - 18 * 11 - (r - 17) * 22
    half = max(half, 28)
    off = 0 if r % 2 else 22
    x = 540 - half
    while x < 540 + half - 10:
        bw = min(44, 540 + half - x)
        bricks.append(f'<rect class="brick r{r}" x="{x + off * 0:.0f}" y="{y}" width="{bw - 4:.0f}" height="26" rx="2" fill="{"#B5532E" if (r + int(x)) % 3 else "#9C4426"}"/>')
        x += 44
S8 = scene(8, f"""
  <svg class="full" viewBox="0 0 {W} {H}">
    <rect x="0" y="1500" width="{W}" height="420" fill="#5A3A28"/>
    <rect x="200" y="1500" width="680" height="40" fill="#8E3B1F"/>
    <g id="s8-temple">{"".join(bricks)}</g>
    <g id="s8-top"><circle cx="540" cy="820" r="40" fill="#E8A93B"/><rect x="532" y="740" width="16" height="50" fill="#E8A93B"/></g>
  </svg>
  <div class="center col" style="justify-content:flex-start;padding-top:250px">
    <div class="label cream" id="s8-k">SIRPUR · 7TH CENTURY</div>
    <div class="serif cream" style="font-size:96px;text-align:center;max-width:960px;line-height:1.05" id="s8-t">Laxman Temple</div>
    <div class="body cream" style="font-size:42px;opacity:.9;margin-top:16px" id="s8-s">A masterpiece built in brick</div>
  </div>
  <div class="center col" style="justify-content:flex-start;padding-top:1590px">
    <div class="body gold" style="font-size:38px" id="s8-b">+ Bhoramdeo, the "Khajuraho of Chhattisgarh"</div>
  </div>""", "#7E3A22")

foods = [("CHILA", 220, 560, -6), ("FARA", 760, 640, 5), ("BORE BAASI", 540, 820, -3), ("THETHRI", 260, 1010, 4), ("KHURMI", 800, 1080, -5)]
food_html = "".join(
    f'<div class="sticker" id="s9-f{k}" style="left:{x}px;top:{y}px;--r:{r}deg">{n}</div>' for k, (n, x, y, r) in enumerate(foods)
)
S9 = scene(9, f"""
  <svg class="full" viewBox="0 0 {W} {H}">
    <g id="s9-plate">
      <circle cx="540" cy="1480" r="300" fill="#F4E9D8"/><circle cx="540" cy="1480" r="240" fill="none" stroke="#C2502A" stroke-width="10" stroke-dasharray="4 22" stroke-linecap="round"/>
      <circle cx="430" cy="1430" r="70" fill="#E8C27A"/><circle cx="610" cy="1410" r="80" fill="#FFFDF5"/><circle cx="560" cy="1570" r="65" fill="#8E3B1F"/>
    </g>
  </svg>
  <div class="center col" style="justify-content:flex-start;padding-top:260px">
    <div class="label ink" id="s9-k">ON THE PLATE</div>
    <div class="serif ink" style="font-size:110px" id="s9-t"><em>Taste</em> of home</div>
  </div>
  {food_html}""", "#E8A93B")

S10 = scene(10, f"""
  <svg class="full" viewBox="0 0 {W} {H}">
    <g id="s10-top">{dot_border("#E8A93B", y=140, r=7)}{dot_border("#C2502A", y=170, r=5)}</g>
    <g id="s10-bot">{dot_border("#C2502A", y=1750, r=5)}{dot_border("#E8A93B", y=1780, r=7)}</g>
    <circle id="s10-sun" cx="540" cy="1420" r="150" fill="#C2502A"/>
  </svg>
  <div class="center col" style="justify-content:flex-start;padding-top:560px">
    <div class="hindi cream" style="font-size:150px;line-height:1.15;text-align:center" id="s10-hi1">{words("छत्तीसगढ़िया")}</div>
    <div class="hindi gold" style="font-size:150px;line-height:1.15;text-align:center" id="s10-hi2">{words("सबसे बढ़िया")}</div>
    <div class="serif cream" style="font-size:52px;margin-top:30px;opacity:.9" id="s10-en"><em>"Chhattisgarhis are the best"</em></div>
    <div class="pill" id="s10-pill" style="margin-top:60px">HAPPY RAJYOTSAVA · 1 NOV</div>
    <div class="body cream" style="font-size:36px;margin-top:40px;opacity:.8" id="s10-cta">Save · Share · Visit Chhattisgarh</div>
  </div>""", "#14213D")

progress = "".join(f'<div class="seg"><div class="fill" id="p{k}"></div></div>' for k in range(1, 11))

FONTS = """
@font-face{font-family:Anton;src:url(assets/anton-latin-400-normal.woff2) format('woff2')}
@font-face{font-family:Fraunces;font-weight:900;src:url(assets/fraunces-latin-900-normal.woff2) format('woff2')}
@font-face{font-family:Fraunces;font-style:italic;font-weight:400;src:url(assets/fraunces-latin-400-italic.woff2) format('woff2')}
@font-face{font-family:Grotesk;font-weight:700;src:url(assets/space-grotesk-latin-700-normal.woff2) format('woff2')}
@font-face{font-family:Grotesk;font-weight:400;src:url(assets/space-grotesk-latin-400-normal.woff2) format('woff2')}
@font-face{font-family:Tiro;src:url(assets/tiro-devanagari-hindi-devanagari-400-normal.woff2) format('woff2');unicode-range:U+0900-097F,U+200C-200D,U+25CC,U+A8E0-A8FF}
"""

CSS = FONTS + f"""
html,body{{margin:0;background:#14213D}}
#root{{position:relative;width:{W}px;height:{H}px;overflow:hidden;background:#14213D}}
.scene{{position:absolute;inset:0;overflow:hidden}}
.bg{{position:absolute;inset:0}}
.full{{position:absolute;inset:0;width:{W}px;height:{H}px}}
.center{{position:absolute;inset:0;display:flex;align-items:center;box-sizing:border-box}}
.col{{flex-direction:column}}
.display{{font-family:Anton,sans-serif;margin:0;letter-spacing:2px;color:#F4E9D8}}
.serif{{font-family:Fraunces,Georgia,serif;font-weight:900}}
.serif em{{font-style:italic;font-weight:400}}
.body{{font-family:Grotesk,Inter,sans-serif;font-weight:400}}
.label{{font-family:Grotesk,Inter,sans-serif;font-weight:700;font-size:34px;letter-spacing:8px;margin-bottom:18px}}
.hindi{{font-family:Tiro,serif}}
.cream{{color:#F4E9D8}} .gold{{color:#E8A93B}} .ink{{color:#2A1A10}}
.ch,.wd{{display:inline-block}}
.pill{{margin-top:40px;font-family:Grotesk,sans-serif;font-weight:700;font-size:38px;letter-spacing:6px;color:#14213D;background:#E8A93B;padding:18px 36px;border-radius:60px;display:block}}
.sticker{{position:absolute;transform:translate(-50%,-50%) rotate(var(--r));font-family:Anton,sans-serif;font-size:96px;letter-spacing:2px;color:#F4E9D8;background:#8E3B1F;padding:14px 34px;border-radius:24px;box-shadow:8px 8px 0 #2A1A10;white-space:nowrap}}
#progress{{position:absolute;left:40px;right:40px;top:70px;display:flex;gap:10px;z-index:50}}
.seg{{flex:1;height:8px;border-radius:4px;background:rgba(244,233,216,.3);overflow:hidden}}
.fill{{width:100%;height:100%;background:#F4E9D8;transform-origin:0 50%;transform:scaleX(0)}}
#grain{{position:absolute;inset:0;z-index:60;opacity:.10;mix-blend-mode:overlay;pointer-events:none}}
"""

JS = """
window.__timelines = window.__timelines || {};
const tl = gsap.timeline({ paused: true });
const B = [0, 4, 10, 16, 22, 28, 34, 40, 46, 52, 60];
const O = 0.4;
// deterministic PRNG
let seed = 36; const rand = () => { seed = (seed * 16807) % 2147483647; return (seed - 1) / 2147483646; };

// progress bar
for (let k = 1; k <= 10; k++) tl.to('#p' + k, { scaleX: 1, duration: B[k] - B[k - 1], ease: 'none' }, B[k - 1]);

// scene entrances (alternate directions)
const dirs = [null, null, {yPercent: 100}, {xPercent: 100}, {yPercent: -100}, {xPercent: -100}, {yPercent: 100}, {scale: 1.4, opacity: 0}, {xPercent: 100}, {yPercent: 100}, {scale: 0.6, opacity: 0, rotation: -8}];
for (let k = 2; k <= 10; k++) tl.from('#s' + k, Object.assign({ duration: O, ease: 'power3.inOut' }, dirs[k]), B[k - 1] - O);

// S1 — 36 forts + title
tl.from('#s1 .fort-in', { scale: 0, opacity: 0, transformOrigin: '50% 100%', duration: 0.35, ease: 'back.out(2)', stagger: { each: 0.03, from: 'random' } }, 0.05);
tl.to('#s1 .fort-in', { y: -14, duration: 0.25, ease: 'power2.out', yoyo: true, repeat: 1, stagger: 0.012 }, 1.9);
tl.from('#s1-count', { y: 40, opacity: 0, duration: 0.4, ease: 'power3.out' }, 1.0);
tl.from('#s1-title .ch', { y: 160, opacity: 0, duration: 0.45, ease: 'power4.out', stagger: 0.04 }, 1.6);
tl.from('#s1-hi', { scale: 0.6, opacity: 0, duration: 0.5, ease: 'back.out(1.8)' }, 2.5);

// S2 — born 2000 -> 2026
const yr = { v: 2000 }; const yel = document.getElementById('s2-year');
tl.to(yr, { v: 2026, duration: 2.2, ease: 'power2.inOut', onUpdate: () => { yel.textContent = Math.round(yr.v); } }, 4.6);
tl.from('#s2-sun', { y: 300, duration: 1.4, ease: 'power3.out' }, 3.8);
tl.from('#s2-rays', { rotation: -30, opacity: 0, svgOrigin: '540 1140', duration: 2.4, ease: 'power2.out' }, 4.0);
tl.to('#s2-rays', { rotation: 8, svgOrigin: '540 1140', duration: 3.6, ease: 'none' }, 6.4);
tl.from('#s2-k', { y: 30, opacity: 0, duration: 0.4 }, 4.3);
tl.from('#s2-year', { scale: 0.7, opacity: 0, duration: 0.5, ease: 'back.out(1.6)' }, 4.4);
tl.from('#s2-l1', { y: 40, opacity: 0, duration: 0.5, ease: 'power3.out' }, 6.0);
tl.from('#s2-l2', { y: 30, opacity: 0, duration: 0.5, ease: 'power3.out' }, 6.4);
tl.from('#s2-pill', { scale: 0, opacity: 0, duration: 0.5, ease: 'back.out(2.2)' }, 7.0);
tl.to('#s2-pill', { scale: 1.08, duration: 0.25, yoyo: true, repeat: 3, ease: 'sine.inOut' }, 8.0);

// S3 — forest
tl.from('#s3 .tree', { y: 700, duration: 0.9, ease: 'power3.out', stagger: 0.05 }, 9.7);
tl.to('#s3-back', { x: -40, duration: 6, ease: 'none' }, 10);
tl.to('#s3-front', { x: -90, duration: 6, ease: 'none' }, 10);
document.querySelectorAll('#s3 .fly').forEach((el, i) => {
  tl.fromTo(el, { opacity: 0 }, { opacity: 1, duration: 0.5 + rand() * 0.6, yoyo: true, repeat: 3, ease: 'sine.inOut' }, 10.6 + rand() * 1.5);
  tl.to(el, { x: (rand() - 0.5) * 120, y: -60 - rand() * 120, duration: 4.5, ease: 'sine.inOut' }, 10.6);
});
tl.from('#s3-k', { y: 30, opacity: 0, duration: 0.4 }, 10.3);
tl.from('#s3-num', { scale: 0.5, opacity: 0, duration: 0.6, ease: 'back.out(1.7)' }, 10.5);
tl.from('#s3-l1', { y: 40, opacity: 0, duration: 0.5 }, 11.2);
tl.from('#s3-l2', { y: 30, opacity: 0, duration: 0.5 }, 11.8);

// S4 — Chitrakote
tl.fromTo('#s4-water', { y: 0 }, { y: 1600, duration: 6.4, ease: 'none' }, 15.6);
document.querySelectorAll('#s4 .mist').forEach((el, i) => {
  tl.fromTo(el, { scale: 0.8 }, { scale: 1.25, transformOrigin: '50% 50%', duration: 1.1 + (i % 3) * 0.3, yoyo: true, repeat: 3, ease: 'sine.inOut' }, 15.6 + i * 0.07);
});
tl.from('#s4-k', { y: 30, opacity: 0, duration: 0.4 }, 16.2);
tl.from('#s4-t .ch', { y: -120, opacity: 0, duration: 0.5, ease: 'bounce.out', stagger: 0.05 }, 16.3);
tl.from('#s4-s', { y: 40, opacity: 0, duration: 0.5 }, 17.3);
tl.from('#s4-f', { y: 30, opacity: 0, duration: 0.5 }, 18.2);

// S5 — rice bowl
document.querySelectorAll('#s5 .stalk').forEach((el, i) => {
  tl.fromTo(el, { rotation: -4, svgOrigin: el.dataset.o }, { rotation: 4, svgOrigin: el.dataset.o, duration: 1.5, yoyo: true, repeat: 3, ease: 'sine.inOut' }, 21.6 + (i % 4) * 0.12);
});
tl.from('#s5-bowl', { y: 500, duration: 0.8, ease: 'power3.out' }, 22.0);
tl.from('#s5 .grain', { y: -500, opacity: 0, duration: 0.5, ease: 'bounce.out', stagger: { each: 0.008, from: 'random' } }, 22.6);
tl.from('#s5-hi .wd', { y: 60, opacity: 0, duration: 0.5, ease: 'power3.out', stagger: 0.15 }, 22.3);
tl.from('#s5-en', { y: 40, opacity: 0, duration: 0.5 }, 23.3);
tl.from('#s5-s', { y: 30, opacity: 0, duration: 0.5 }, 24.0);

// S6 — Bastar Dussehra
tl.from('#s6-rath', { x: -900, duration: 1.4, ease: 'power3.out' }, 27.8);
tl.to('#s6-rath', { x: 60, duration: 4.6, ease: 'none' }, 29.2);
document.querySelectorAll('#s6 .wheel').forEach((el) => tl.fromTo(el, { rotation: -540, svgOrigin: el.dataset.o }, { rotation: 200, svgOrigin: el.dataset.o, duration: 6, ease: 'power1.out' }, 27.8));
document.querySelectorAll('#s6 .flame').forEach((el, i) => {
  tl.fromTo(el, { scaleY: 0.85, opacity: 0.6 }, { scaleY: 1.15, opacity: 1, transformOrigin: '50% 100%', duration: 0.35 + rand() * 0.3, yoyo: true, repeat: 7, ease: 'sine.inOut' }, 28 + rand() * 0.5);
});
tl.from('#s6-k', { y: 30, opacity: 0, duration: 0.4 }, 28.3);
tl.from('#s6-num', { scale: 1.8, opacity: 0, duration: 0.5, ease: 'power4.out' }, 28.5);
tl.from('#s6-l1', { y: 40, opacity: 0, duration: 0.5 }, 29.6);
tl.from('#s6-l2', { y: 30, opacity: 0, duration: 0.5 }, 30.2);

// S7 — Dhokra
tl.from('#s7-horse', { scale: 0.7, svgOrigin: '550 1150', opacity: 0, y: 80, duration: 0.9, ease: 'power3.out' }, 34.0);
tl.to('#s7-horse', { y: -24, duration: 1.2, yoyo: true, repeat: 3, ease: 'sine.inOut' }, 34.9);
tl.fromTo('#s7-shine', { x: 0 }, { x: 1600, duration: 1.6, ease: 'power2.inOut' }, 35.2);
tl.fromTo('#s7-shine', { x: 0 }, { x: 1600, duration: 1.6, ease: 'power2.inOut', immediateRender: false }, 37.6);
tl.from('#s7-k', { y: 30, opacity: 0, duration: 0.4 }, 34.3);
tl.from('#s7-t .ch', { scale: 2.2, opacity: 0, duration: 0.45, ease: 'power4.out', stagger: 0.07 }, 34.4);
tl.from('#s7-l1', { y: 40, opacity: 0, duration: 0.5 }, 35.6);
tl.from('#s7-l2', { y: 40, opacity: 0, duration: 0.5 }, 36.1);

// S8 — temple builds brick by brick
for (let r = 0; r < 22; r++) tl.from('#s8 .r' + r, { y: -300, opacity: 0, duration: 0.3, ease: 'power2.in', stagger: 0.01 }, 40.0 + r * 0.09);
tl.from('#s8-top', { scale: 0, svgOrigin: '540 800', duration: 0.5, ease: 'back.out(2.5)' }, 42.1);
tl.from('#s8-k', { y: 30, opacity: 0, duration: 0.4 }, 40.3);
tl.from('#s8-t', { y: 50, opacity: 0, duration: 0.5, ease: 'power3.out' }, 40.5);
tl.from('#s8-s', { y: 30, opacity: 0, duration: 0.5 }, 41.1);
tl.from('#s8-b', { y: 30, opacity: 0, duration: 0.5 }, 42.8);

// S9 — food stickers
tl.from('#s9-plate', { y: 600, rotation: -90, svgOrigin: '540 1480', duration: 0.9, ease: 'power3.out' }, 45.8);
tl.from('#s9-k', { y: 30, opacity: 0, duration: 0.4 }, 46.2);
tl.from('#s9-t', { scale: 0.6, opacity: 0, duration: 0.5, ease: 'back.out(1.8)' }, 46.3);
for (let k = 0; k < 5; k++) tl.from('#s9-f' + k, { scale: 0, opacity: 0, duration: 0.45, ease: 'back.out(2.6)' }, 47.0 + k * 0.5);
for (let k = 0; k < 5; k++) tl.to('#s9-f' + k, { y: -16, duration: 0.5, yoyo: true, repeat: 1, ease: 'sine.inOut' }, 49.6 + k * 0.1);

// S10 — outro
tl.from('#s10-top', { y: -200, duration: 0.6, ease: 'power3.out' }, 52.0);
tl.from('#s10-bot', { y: 200, duration: 0.6, ease: 'power3.out' }, 52.0);
tl.from('#s10-sun', { scale: 0, svgOrigin: '540 1420', duration: 0.8, ease: 'back.out(1.5)' }, 52.1);
tl.from('#s10-hi1 .wd', { y: 80, opacity: 0, duration: 0.5, ease: 'power3.out' }, 52.4);
tl.from('#s10-hi2 .wd', { y: 80, opacity: 0, duration: 0.5, ease: 'power3.out', stagger: 0.2 }, 53.0);
tl.from('#s10-en', { opacity: 0, duration: 0.6 }, 54.0);
tl.from('#s10-pill', { scale: 0, opacity: 0, duration: 0.5, ease: 'back.out(2.2)' }, 55.0);
tl.from('#s10-cta', { y: 30, opacity: 0, duration: 0.5 }, 56.0);
tl.to('#s10-sun', { scale: 1.12, svgOrigin: '540 1420', duration: 0.5, yoyo: true, repeat: 1, ease: 'sine.inOut' }, 58.0);

window.__timelines['main'] = tl;
"""

GRAIN = (
    f'<svg id="grain" viewBox="0 0 {W} {H}"><filter id="n"><feTurbulence type="fractalNoise" baseFrequency=".9" '
    f'numOctaves="2" seed="36"/></filter><rect width="100%" height="100%" filter="url(#n)"/></svg>'
)

page = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width={W}, height={H}" />
<title>Chhattisgarh — The Heart of India</title>
<script src="assets/gsap.min.js"></script>
<style>{CSS}</style>
</head>
<body>
<div id="root" data-composition-id="main" data-width="{W}" data-height="{H}" data-duration="60">
{S1}
{S2}
{S3}
{S4}
{S5}
{S6}
{S7}
{S8}
{S9}
{S10}
<div id="progress" class="clip" data-start="0" data-duration="60" data-track-index="20">{progress}</div>
<div class="clip" data-start="0" data-duration="60" data-track-index="21" style="position:absolute;inset:0;z-index:60;pointer-events:none">{GRAIN}</div>
<audio id="bgm" src="assets/soundtrack.wav" data-start="0" data-duration="60" data-track-index="30" data-volume="1"></audio>
</div>
<script>{JS}</script>
</body>
</html>
"""

Path(__file__).with_name("index.html").write_text(page, encoding="utf-8")
print("wrote index.html", len(page), "bytes")
