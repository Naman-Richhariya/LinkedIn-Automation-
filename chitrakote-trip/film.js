import { clamp, lerp, seg, ss, eio, eo, back, hash, vnoise, track } from '/core/lib.js';
import { drawFalls } from './falls.js';
import { drawPip } from './pip.js';

const FPS = 30, DUR = 45;
const $ = id => document.getElementById(id);

// ---------- timeline (single source of truth) ----------
const BPM = 100, BEAT = 60 / BPM, BAR = BEAT * 4;
const VO = [ // id, start, caption; lengths from vo/dur.json
  ['L1', 1.0, 'This is Pip. Pip wants to see a waterfall.'],
  ['L2', 4.6, 'Search Chitrakote, in Bastar, Chhattisgarh.'],
  ['L3', 9.6, '38 km from Jagdalpur, on the Indravati River.'],
  ['L4', 14.6, '29 m high, and the widest falls in India.'],
  ['L5', 19.8, 'But when should Pip go?'],
  ['L6', 22.6, 'Switch to monsoon.'],
  ['L7', 28.2, 'Nearly 300 m of roaring water. The Niagara of India.'],
  ['L8', 36.0, 'Go between July and October. Trip saved.'],
];
let VODUR = {};
const CHAP = [[0, '01', 'Search'], [9.6, '02', 'Plan'], [19.2, '03', 'Season'], [36.0, '04', 'Save']];
const WORD = 'Chitrakote', K0 = 4.95, KD = 0.16, KENTER = 6.95;
const T = { result: 7.25, route: 9.4, facts: 14.4, season: 19.2, click: 24.0, floodA: 25.0, floodB: 26.2, badge: 28.2,
  drainA: 32.6, drainB: 33.8, saveClick: 37.6, toast: 38.1 };

// camera: [t, worldX, worldY, zoom]; focus lands at screen (540, 820)
const camT = track([
  [0, [540, 600, 1.12]], [4.3, [540, 590, 1.15]], [5.0, [470, 520, 1.45]], [6.9, [500, 520, 1.42]],
  [7.9, [540, 800, 1.1]], [9.5, [540, 815, 1.1]], [10.4, [420, 1156, 1.35]], [13.2, [680, 1156, 1.35]], [14.2, [660, 1170, 1.3]],
  [15.0, [540, 1400, 1.25]], [19.1, [545, 1400, 1.25]], [20.0, [580, 1634, 1.6]], [23.85, [620, 1634, 1.7]],
  [24.35, [540, 860, 1.08]], [32.6, [540, 860, 1.08]], [34.0, [540, 960, 1.0]], [35.5, [540, 960, 1.0]],
  [36.4, [540, 1700, 1.3]], [38.1, [540, 1680, 1.3]], [39.6, [540, 1540, 1.3]], [45, [540, 1420, 1.22]],
]);
function cam(t) {
  const [wx, wy, z] = camT(t);
  let tx = 540 - wx * z, ty = 820 - wy * z;
  tx = clamp(tx, 1080 - 1080 * z, 0); ty = clamp(ty, 1920 - 2300 * z, 0);
  return { tx, ty, z };
}

// cursor keys: [t, anchor|null, fx, fy] (null = screen x,y in fx,fy); hidden ranges
const CUR = [
  [3.6, null, 1000, 1480], [4.55, '#search', .42, .62], [4.9, '#search', .45, .62],
  [8.6, '#place', .92, .95], [12.0, '#route', .9, .9], [17.5, '#facts', .9, 1.05],
  [20.6, '#season', .32, .95], [22.3, '#season', .6, .8], [23.75, '#season', .74, .55], [24.6, '#season', .78, .6],
  [34.4, '#place', .7, .9], [37.3, '#save', .52, .55], [38.0, '#save', .55, .6], [40.5, '#save', .75, .95], [45, '#save', .78, 1.0],
];
const CUR_HIDE = [[0, 3.6], [5.0, 7.6], [24.9, 33.9]];
const CLICKS = [4.7, 24.0, 37.6];

// Pip acts: [t0, t1, kind, a, b]  anchors are [selector, fx]
const PA = {
  search: ['#search', .8], title: ['#ptitle', .82], rA: ['#rA', .5], rline: ['#rline', 0], rB: ['#rB', .5],
  f1: ['#f1', .5], f2: ['#f2', .5], f3: ['#f3', .5], segS: ['#season', .25], chip: ['#fchip', .82],
  save: ['#save', .82], toast: ['#toast', .8],
};
const ACTS = [
  [0, .45, 'hide'], [.45, .95, 'drop', PA.search], [.95, 7.5, 'stand', PA.search],
  [7.5, 8.1, 'jump', PA.search, PA.title], [8.1, 9.85, 'stand', PA.title],
  [9.85, 10.45, 'jump', PA.title, PA.rA], [10.45, 13.35, 'run', ['#rline', 0], ['#rline', 1]],
  [13.35, 13.75, 'jump', ['#rline', 1], PA.rB], [13.75, 14.65, 'stand', PA.rB],
  [14.65, 15.25, 'jump', PA.rB, PA.f1], [15.25, 15.8, 'stand', PA.f1], [15.8, 16.3, 'jump', PA.f1, PA.f2],
  [16.3, 16.9, 'stand', PA.f2], [16.9, 17.4, 'jump', PA.f2, PA.f3], [17.4, 19.35, 'stand', PA.f3],
  [19.35, 19.95, 'jump', PA.f3, PA.segS], [19.95, 24.1, 'stand', PA.segS], [24.1, 24.45, 'jump', PA.segS, PA.segS],
  [24.45, 25.1, 'stand', PA.segS], [25.1, 26.3, 'jump', PA.segS, PA.chip], [26.3, 32.75, 'stand', PA.chip],
  [32.75, 33.75, 'jump', PA.chip, PA.title], [33.75, 36.25, 'stand', PA.title], [36.25, 36.85, 'jump', PA.title, PA.save],
  [36.85, 37.6, 'stand', PA.save], [37.6, 37.9, 'jump', PA.save, PA.save], [37.9, 38.35, 'stand', PA.save],
  [38.35, 38.85, 'jump', PA.save, PA.toast], [38.85, 41.0, 'stand', PA.toast], [41.0, 45.1, 'sit', PA.toast],
];
// eyes & arms over time
const EYES = [[0, 'down'], [1.2, 'neutral'], [2.6, 'up'], [3.6, 'left'], [4.6, 'down'], [7.3, 'wide'], [8.2, 'down'], [10.4, 'right'],
  [13.8, 'happy'], [14.6, 'down'], [17.6, 'neutral'], [20.0, 'right'], [22.6, 'neutral'], [23.3, 'right'], [24.1, 'wide'],
  [26.3, 'happy'], [28.0, 'down'], [32.0, 'happy'], [33.8, 'down'], [36.9, 'down'], [38.4, 'happy'], [42.4, 'shut']];
const ARMS = [[0, 'down'], [1.2, 'wave'], [2.4, 'down'], [13.8, 'up'], [14.5, 'down'], [26.4, 'up'], [27.8, 'down'], [38.9, 'up'], [39.9, 'wave'], [40.9, 'down']];
const at = (list, t) => { let v = list[0][1]; for (const [k, x] of list) if (t >= k) v = x; return v; };

// ---------- helpers ----------
function rectOf(sel) { const r = document.querySelector(sel).getBoundingClientRect(); return r; }
function anchorPt(a) { const r = rectOf(a[0]); return { x: r.left + a[1] * r.width, y: r.top }; }
const show = (el, o, dy = 0, sc = 1) => { el.style.opacity = o; el.style.transform = `translateY(${dy}px) scale(${sc})`; };
function reveal(el, t, t0) { const k = seg(t, t0, t0 + .45); show(el, ss(k * 1.6), (1 - eo(k)) * 40, lerp(.94, 1, back(k))); }

// ---------- falls canvases ----------
const pc = $('pc').getContext('2d'), fc = $('fc').getContext('2d'), tcx = $('tc').getContext('2d');
function monsoon(t) { return eio(seg(t, 24.4, 27.0)); }

// ---------- render ----------
let lastT = -1;
function render(t) {
  const mon = monsoon(t);
  // UI states
  const typed = Math.max(0, Math.min(WORD.length, Math.floor((t - K0) / KD) + 1));
  const ph = '<span class="ph">Search a place</span>';
  if (t < 4.7) $('q').innerHTML = ph;
  else if (t < K0) $('q').innerHTML = '<span id="caret"></span>' + ph;
  else if (t < 7.4) $('q').innerHTML = WORD.slice(0, typed) + (Math.floor((t - K0) * 3) % 2 && t > 6.7 ? '' : '<span id="caret"></span>');
  else $('q').innerHTML = WORD;
  $('search').classList.toggle('focus', t >= 4.7 && t < 7.4);
  reveal($('place'), t, T.result); reveal($('route'), t, T.route); reveal($('facts'), t, T.facts);
  reveal($('seasonrow'), t, T.season); reveal($('save'), t, T.season + .15);
  // heading fades a little once results exist
  $('h2').style.opacity = 1 - .6 * seg(t, 7.2, 8);
  // rB pin bounce when Pip arrives
  const pb = seg(t, 13.35, 13.9); $('rB').style.transform = `translateY(${-Math.sin(pb * Math.PI) * 14}px)`;
  // facts: squash when Pip lands
  [['#f1', 15.25], ['#f2', 16.3], ['#f3', 17.4]].forEach(([s, l]) => {
    const k = seg(t, l, l + .3); const el = document.querySelector(s);
    el.style.transform = `translateY(${Math.sin(k * Math.PI) * 8}px)`;
    el.style.borderColor = (t > l && t < l + .9) ? '#A5B4FC' : '';
  });
  // season knob
  const kn = eio(seg(t, T.click, T.click + .32));
  $('knob').style.left = lerp(8, 344, kn) + 'px';
  $('segS').style.color = kn < .5 ? '#fff' : '#334155'; $('segM').style.color = kn >= .5 ? '#fff' : '#334155';
  $('tag').textContent = t >= T.click + .2 ? 'Monsoon' : 'Summer';
  // save press
  const sp = seg(t, T.saveClick - .05, T.saveClick + .25);
  $('save').style.transform = `scale(${1 - .04 * Math.sin(sp * Math.PI)})`;
  // toast
  const tk = seg(t, T.toast, T.toast + .6);
  $('toast').style.opacity = ss(seg(t, T.toast, T.toast + .2));
  $('toast').style.transform = `translateY(${lerp(130, 0, back(tk, 1.4))}px)`;
  // rack focus: photo soft while reading facts/season; never on text being read
  const rf = Math.max(env(t, 14.6, 19.6), 0);
  $('photo').style.filter = rf > .01 ? `blur(${rf * 4}px)` : 'none';

  // camera + motion blur on whips only
  const c = cam(t), cp = cam(Math.max(0, t - 1 / FPS));
  $('world').style.transform = `translate(${c.tx}px,${c.ty}px) scale(${c.z})`;
  const vx = Math.abs(c.tx - cp.tx), vy = Math.abs(c.ty - cp.ty);
  const bx = vx > 60 ? (vx - 60) * .08 : 0, by = vy > 60 ? (vy - 60) * .08 : 0;
  $('mbg').setAttribute('stdDeviation', `${bx.toFixed(2)} ${by.toFixed(2)}`);
  $('blurwrap').style.filter = (bx + by) > .2 ? 'url(#mb)' : 'none';

  // photo canvas (live falls)
  drawFalls(pc, 820, 290, t, mon, 1);
  drawFalls(tcx, 240, 168, t, mon, .5);

  // flood: the photo breaks out of its card and fills the screen
  const fl = $('flood');
  const fIn = eio(seg(t, T.floodA, T.floodB)), fOut = eio(seg(t, T.drainA, T.drainB));
  const fk = t < T.drainA ? fIn : 1 - fOut;
  if (t >= T.floodA && t < T.drainB) {
    const r = $('photo').getBoundingClientRect();
    const x = lerp(r.left, 0, fk), y = lerp(r.top, 0, fk), w = lerp(r.width, 1080, fk), h = lerp(r.height, 1920, fk);
    fl.style.display = 'block';
    Object.assign(fl.style, { left: x + 'px', top: y + 'px', width: w + 'px', height: h + 'px', borderRadius: lerp(24 * c.z, 0, fk) + 'px' });
    const W = Math.round(w), H = Math.round(h);
    const cv = $('fc'); if (cv.width !== W || cv.height !== H) { cv.width = W; cv.height = H; }
    cv.style.width = W + 'px'; cv.style.height = H + 'px';
    // spotlight push-in during the freeze
    const push = 1 + .05 * eio(seg(t, T.badge, T.badge + 3.4)) * (1 - fOut);
    cv.style.transform = `scale(${push})`; cv.style.transformOrigin = '50% 45%';
    const L = drawFalls(fc, W, H, t, mon, Math.max(1, W / 820));
    const ui = ss(seg(t, 25.9, 26.3)) * (1 - ss(seg(t, T.drainA - .1, T.drainA + .2)));
    $('fui').style.opacity = ui;
    // bracket spans the lip of the falls, measured from the drawing
    const bk = eo(seg(t, T.badge, T.badge + .7));
    const bl = L.cx - L.R * bk * push, bw = 2 * L.R * bk * push;
    Object.assign($('bracket').style, { left: bl + 'px', width: Math.max(0, bw) + 'px', top: (L.lipY * push + (1 - push) * H * .45 - 120) + 'px', opacity: ss(seg(t, T.badge, T.badge + .2)) });
    const bb = $('badge'); bb.style.top = (L.lipY * push + (1 - push) * H * .45 - 250) + 'px';
    bb.style.opacity = ss(seg(t, T.badge + .3, T.badge + .6));
    bb.style.transform = `translateX(-50%) scale(${lerp(.85, 1, back(seg(t, T.badge + .3, T.badge + .75)))})`;
  } else fl.style.display = 'none';
  // the drained card keeps its photo hidden while the flood layer is over it
  $('photo').style.visibility = (t >= T.floodA && t < T.drainB) ? 'hidden' : 'visible';

  // vignette: before the switch, and during the spotlight freeze
  $('vig').style.opacity = Math.max(.75 * env(t, 20.0, 24.1, .8, .25), .6 * env(t, T.badge, 31.8, .5, .6));

  // chapter pill (wipe on change)
  let ci = 0; CHAP.forEach((x, i) => { if (t >= x[0]) ci = i; });
  const cw = seg(t, CHAP[ci][0], CHAP[ci][0] + .35);
  $('chap').querySelector('.n').textContent = CHAP[ci][1]; $('chap').querySelector('.t').textContent = CHAP[ci][2];
  $('chap').style.clipPath = ci === 0 && t < .3 ? `inset(0 ${100 - eo(seg(t, 0, .3)) * 100}% 0 0 round 999px)` : `inset(0 ${(1 - eo(cw)) * 100}% 0 0 round 999px)`;
  $('chap').style.opacity = 1 - ss(seg(t, 25.0, 25.4)) + ss(seg(t, 33.6, 34.0));

  // key HUD
  const hud = $('hud');
  if (t >= K0 && t < 7.7) {
    const keys = WORD.slice(0, typed).split('');
    let html = keys.slice(-6).map(k => `<i>${k === k.toUpperCase() ? '⇧' + k : k}</i>`).join('');
    if (t >= KENTER) html = `<i>⏎ return</i>`;
    hud.innerHTML = html; hud.style.opacity = ss(seg(t, K0, K0 + .1)) * (1 - ss(seg(t, 7.4, 7.7)));
  } else hud.style.opacity = 0;

  // captions
  let cap = '', co = 0;
  for (const [id, s, txt] of VO) {
    const e = s + (VODUR[id] || 2), a = s - .1, b = Math.max(s + 1.8, e + .6);
    if (t >= a && t < b) { cap = txt; co = Math.min(seg(t, a, a + .15), 1 - seg(t, b - .15, b)); }
  }
  $('cap').textContent = cap; $('cap').style.opacity = co;

  // cursor
  drawCursor(t, c);
  // Pip
  pipFrame(t, c);
}

function env(t, a, b, fi = .3, fo = .3) { return Math.min(seg(t, a, a + fi), 1 - seg(t, b - fo, b)); }

function curPos(k) { if (!k[1]) return { x: k[2], y: k[3] }; const r = rectOf(k[1]); return { x: r.left + k[2] * r.width, y: r.top + k[3] * r.height }; }
function drawCursor(t, c) {
  const el = $('cursor');
  const hidden = CUR_HIDE.some(([a, b]) => t >= a && t < b);
  if (hidden) { el.style.opacity = 0; $('ring').style.opacity = 0; return; }
  let i = 0; while (i < CUR.length - 1 && t >= CUR[i + 1][0]) i++;
  const A = CUR[i], B = CUR[Math.min(i + 1, CUR.length - 1)];
  const k = B === A ? 0 : eio(seg(t, A[0], B[0]));
  const pa = curPos(A), pbp = curPos(B);
  // slight arc for a hand-drawn path
  const x = lerp(pa.x, pbp.x, k) + Math.sin(k * Math.PI) * 18, y = lerp(pa.y, pbp.y, k) - Math.sin(k * Math.PI) * 24;
  let press = 1; for (const cl of CLICKS) { const q = seg(t, cl - .06, cl + .2); if (q > 0 && q < 1) press = 1 - .18 * Math.sin(q * Math.PI); }
  const s = Math.sqrt(c.z) * press;
  el.style.opacity = 1; el.style.transform = `translate(${x}px,${y}px) scale(${s})`;
  const rg = $('ring'); let ro = 0, rs = 1;
  for (const cl of CLICKS) { const q = seg(t, cl, cl + .45); if (q > 0 && q < 1) { ro = 1 - q; rs = .4 + q * 1.2; } }
  rg.style.opacity = ro; rg.style.transform = `translate(${x}px,${y}px) scale(${rs})`;
}

// ---------- Pip ----------
const pipC = $('pip').getContext('2d');
const P = 5; // world units per sprite pixel
function pipFrame(t, c) {
  pipC.clearRect(0, 0, 1080, 1920);
  let a = ACTS.find(x => t >= x[0] && t < x[1]); if (!a) a = ACTS[ACTS.length - 1];
  const [t0, t1, kind, A, B] = a;
  const p = P * c.z;
  let x, y, squash = 0, legs = 'stand', flip = false;
  const breath = Math.sin(t / BEAT * Math.PI) * .03; // breathes on the beat
  const landSquash = (lt) => { const q = seg(t, lt, lt + .28); return q > 0 && q < 1 ? .28 * Math.exp(-q * 4) * Math.cos(q * 12) : 0; };
  // previous landing for squash
  let lastLand = -9; for (const x2 of ACTS) if ((x2[2] === 'jump' || x2[2] === 'drop') && x2[1] <= t) lastLand = x2[1];
  if (kind === 'hide') return;
  if (kind === 'stand' || kind === 'sit') {
    ({ x, y } = anchorPt(A)); squash = breath + landSquash(lastLand);
    if (kind === 'sit') { legs = 'sit'; squash += .12 * Math.exp(-seg(t, t0, t0 + .4) * 6); }
  } else if (kind === 'drop') {
    const e = anchorPt(A); const k = seg(t, t0, t1);
    x = e.x; y = lerp(-120, e.y, k * k); legs = 'tuck'; squash = -.12;
  } else if (kind === 'jump') {
    const a0 = anchorPt(A), b0 = anchorPt(B); const k = seg(t, t0, t1);
    const ant = seg(t, t0, t0 + .12); // anticipation crouch inside the first 0.12 s
    if (ant < 1) { x = a0.x; y = a0.y; squash = .22 * Math.sin(ant * Math.PI); legs = 'stand'; }
    else {
      const q = seg(t, t0 + .12, t1);
      const h = Math.max(70 * c.z, Math.abs(a0.y - b0.y) * .35 + 60 * c.z);
      x = lerp(a0.x, b0.x, q); y = lerp(a0.y, b0.y, q) - Math.sin(q * Math.PI) * h + (Math.min(a0.y, b0.y) < 0 ? 0 : 0);
      squash = q < .25 ? -.2 : q > .8 ? -.1 : 0; legs = 'tuck';
    }
    flip = b0.x < a0.x - 2;
  } else if (kind === 'run') {
    const a0 = anchorPt(A), b0 = anchorPt(B); const k = ss(seg(t, t0, t1));
    x = lerp(a0.x, b0.x, k); y = lerp(a0.y, b0.y, k); legs = Math.floor(t * 10) % 2 ? 'walkA' : 'walkB'; squash = breath * .5;
    flip = b0.x < a0.x;
  }
  // eyes / blink
  let eyes = at(EYES, t);
  const blinkTimes = [2.1, 5.8, 9.1, 12.2, 17.9, 21.8, 30.2, 35.0, 40.2];
  if (eyes !== 'shut' && blinkTimes.some(b => t >= b && t < b + .12)) eyes = 'shut';
  const arms = at(ARMS, t);
  if (kind === 'stand' && (A === PA.segS) && t > 20 && t < 24) flip = false;
  // snap to half sprite-pixels
  const hp = p / 2; x = Math.round(x / hp) * hp; y = Math.round(y / hp) * hp;
  drawPip(pipC, x, y, p, { squash, legs, eyes, arms, flip, wave: Math.floor(t * 6) % 2 });
}

// ---------- texts for readcheck ----------
function TEXTS(t) {
  const out = [];
  const add = (id, sel, text) => {
    const el = document.querySelector(sel); if (!el) return;
    const r = el.getBoundingClientRect(); let o = 1, n = el;
    while (n && n !== document.body) { const s = getComputedStyle(n); o *= +s.opacity; if (s.display === 'none' || s.visibility === 'hidden') o = 0; n = n.parentElement; }
    if (o > .5 && r.width > 0) out.push({ id, text, x0: r.left, y0: r.top, x1: r.right, y1: r.bottom });
  };
  if (t >= K0 && t < 7.4) add('q', '#q', WORD);
  add('chap', '#chap', $('chap').textContent);
  if (t >= T.result) { add('pt', '#ptitle', 'Chitrakote Falls'); }
  if (t >= T.route) add('km', '#rkms', '38 km by road');
  if (t >= T.facts) { add('f1', '#f1', '29 m high'); add('f2', '#f2', 'Widest in India'); add('f3', '#f3', 'Indravati River'); }
  if (t >= T.badge) add('badge', '#badge', '≈ 300 m wide');
  add('fchip', '#fchip', 'Monsoon · Jul–Oct');
  if (t >= T.toast) add('toast', '#tt', 'Trip saved Chitrakote · go Jul–Oct');
  return out;
}

// ---------- events for the mixer ----------
function buildEV() {
  const ev = [];
  VO.forEach(([id, s]) => ev.push({ t: s, type: 'vo', id }));
  for (let i = 0; i < WORD.length; i++) ev.push({ t: K0 + i * KD + (hash(i) - .5) * .03, type: 'key', i });
  ev.push({ t: KENTER, type: 'key', i: 99, enter: 1 });
  CLICKS.forEach(t => ev.push({ t, type: 'click' }));
  [T.result, T.route, T.facts, T.season].forEach(t => ev.push({ t, type: 'pop' }));
  ACTS.forEach(([a, b, k, A, B]) => {
    if (k === 'jump') { ev.push({ t: a + .12, type: 'jump' }); ev.push({ t: b, type: 'land' }); }
    if (k === 'drop') ev.push({ t: b, type: 'land' });
    if (k === 'run') for (let s = a + .05; s < b; s += .2) ev.push({ t: s, type: 'step' });
    if (k === 'sit') ev.push({ t: a, type: 'sit' });
  });
  ev.push({ t: 13.4, type: 'pin' });
  ev.push({ t: 24.2, type: 'whoosh', d: .4 });
  ev.push({ t: T.floodA, type: 'flood' });
  ev.push({ t: T.drainA, type: 'drain' });
  ev.push({ t: T.badge + .3, type: 'badge' });
  ev.push({ t: T.toast + .1, type: 'toast' });
  ev.push({ t: 20.5, type: 'swish' }); ev.push({ t: 22.0, type: 'swish' });
  ev.push({ t: 0, type: 'meta', bpm: BPM, vo: VO.map(v => ({ id: v[0], t: v[1], text: v[2] })) });
  return ev.sort((a, b) => a.t - b.t);
}

// ---------- boot ----------
(async () => {
  try { VODUR = await (await fetch('vo/dur.json')).json(); } catch (e) { }
  await document.fonts.ready;
  await Promise.all([...document.fonts].map(f => f.load().catch(() => { })));
  window.DUR = DUR; window.EV = buildEV(); window.TEXTS = TEXTS;
  window.render = render;
  render(0);
  window.READY = true;
})();
