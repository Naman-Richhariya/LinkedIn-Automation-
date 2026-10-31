// Chitrakote, drawn live: a horseshoe lip on the Indravati, thin and white in summer,
// a wall of tea-brown monsoon water at mon = 1. Layout is a function of (w, h), so the
// same drawing works in the card, in the toast thumbnail and full screen.
import { clamp, lerp, ss, hash, vnoise } from '/core/lib.js';

const mix = (a, b, k) => a.map((v, i) => Math.round(lerp(v, b[i], k)));
const rgb = (c, a = 1) => `rgba(${c[0]},${c[1]},${c[2]},${a})`;
const C = {
  skyS0: [150, 204, 234], skyS1: [228, 243, 250], skyM0: [118, 138, 152], skyM1: [196, 206, 211],
  hillS: [92, 128, 120], hillM: [82, 108, 104], forS: [47, 96, 60], forM: [36, 82, 50],
  rock: [88, 72, 60], rockD: [64, 52, 44],
  curS: [238, 246, 248], curM: [190, 150, 104], foamM: [244, 236, 222],
  poolS: [104, 164, 176], poolM: [150, 116, 80], poolD: [70, 58, 46],
};
const strands = u => Math.max(...[-0.62, -0.18, 0.35].map(c => Math.exp(-(((u - c) / .07) ** 2)))) * .9;

export function drawFalls(ctx, w, h, t, mon, s = 1) {
  const af = clamp((h / w - .4) / 1.4);
  const cx = w / 2, R = w * lerp(.40, .42, af);
  const lipY = h * lerp(.36, .40, af);
  const Hf = Math.min(h * .28, w * .30), d = Hf * .35;
  const lip = u => lipY + d * Math.min(u * u, 1.0);
  const pool = u => lipY + Hf + d * .6 * Math.min(u * u, 1.0);
  // sky
  let g = ctx.createLinearGradient(0, 0, 0, lipY);
  g.addColorStop(0, rgb(mix(C.skyS0, C.skyM0, mon))); g.addColorStop(1, rgb(mix(C.skyS1, C.skyM1, mon)));
  ctx.fillStyle = g; ctx.fillRect(0, 0, w, lipY + 2);
  // far hills
  ctx.fillStyle = rgb(mix(C.hillS, C.hillM, mon));
  ctx.beginPath(); ctx.moveTo(0, lipY);
  for (let x = 0; x <= w; x += 6 * s) ctx.lineTo(x, lipY - Hf * (.55 + .35 * vnoise(x / (120 * s) + 3.1)));
  ctx.lineTo(w, lipY); ctx.fill();
  // rock walls of the gorge (lip → pool, full width)
  ctx.fillStyle = rgb(C.rock);
  ctx.beginPath();
  for (let x = 0; x <= w; x += 4 * s) { const u = (x - cx) / R; ctx.lineTo(x, lip(u) - 1); }
  for (let x = w; x >= 0; x -= 4 * s) { const u = (x - cx) / R; ctx.lineTo(x, pool(u) + 2); }
  ctx.fill();
  ctx.strokeStyle = rgb(C.rockD, .6); ctx.lineWidth = 2 * s;
  for (let k = 1; k < 5; k++) {
    ctx.beginPath();
    for (let x = 0; x <= w; x += 8 * s) { const u = (x - cx) / R; ctx.lineTo(x, lerp(lip(u), pool(u), k / 5) + (vnoise(x / (40 * s) + k * 7) - .5) * 6 * s); }
    ctx.stroke();
  }
  // forest on the plateau
  ctx.fillStyle = rgb(mix(C.forS, C.forM, mon));
  ctx.beginPath(); ctx.moveTo(0, lip(-cx / R) + 1);
  for (let x = 0; x <= w; x += 5 * s) { const u = (x - cx) / R; ctx.lineTo(x, lip(u) - Hf * (.12 + .22 * vnoise(x / (26 * s) + 11))); }
  for (let x = w; x >= 0; x -= 5 * s) { const u = (x - cx) / R; ctx.lineTo(x, lip(u) + 1); }
  ctx.fill();
  // pool and river below
  g = ctx.createLinearGradient(0, lipY + Hf, 0, h);
  g.addColorStop(0, rgb(mix(C.poolS, C.poolM, mon))); g.addColorStop(1, rgb(mix(C.poolS, C.poolD, mon * .8 + .2)));
  ctx.fillStyle = g; ctx.beginPath();
  for (let x = 0; x <= w; x += 4 * s) { const u = (x - cx) / R; ctx.lineTo(x, pool(u)); }
  ctx.lineTo(w, h); ctx.lineTo(0, h); ctx.fill();
  // river flow lines
  ctx.strokeStyle = 'rgba(255,255,255,.18)'; ctx.lineWidth = 2.5 * s;
  for (let k = 0; k < 40; k++) {
    const y0 = lipY + Hf + d * .6; const yy = y0 + ((hash(k + 40) + t * (.05 + .1 * mon)) % 1) * (h - y0);
    const xx = hash(k + 90) * w, L = w * (.06 + .12 * hash(k + 3)) * (.5 + (yy - y0) / (h - y0 + 1));
    ctx.beginPath(); ctx.moveTo(xx, yy); ctx.lineTo(xx + L, yy); ctx.stroke();
  }
  // water curtains
  const stride = 3.6 * s, N = Math.round(2 * R / stride);
  const cur = mix(C.curS, C.curM, mon), foam = mix(C.curS, C.foamM, mon);
  ctx.lineCap = 'butt';
  for (let i = 0; i < N; i++) {
    const u = -1 + 2 * (i + .5) / N;
    const dens = Math.max(strands(u), ss(clamp(mon * 1.35 - Math.abs(u) * .35)));
    if (dens < .04) continue;
    const x = cx + u * R + Math.sin(t * 3 + i * .7) * .6 * s, top = lip(u), bot = pool(u) + 3 * s, L = bot - top;
    ctx.strokeStyle = rgb(cur, .9 * dens); ctx.lineWidth = stride * 1.25;
    ctx.beginPath(); ctx.moveTo(x, top); ctx.lineTo(x + Math.sin(i) * s, bot); ctx.stroke();
    ctx.strokeStyle = rgb(foam, .85 * dens); ctx.lineWidth = stride * .7;
    for (let j = 0; j < 3; j++) {
      const ph = (t * (1.1 + .5 * hash(i + j * 31)) + hash(i * 3 + j)) % 1;
      const y0 = top + (ph * 1.3 - .3) * L, y1 = y0 + L * .24;
      ctx.beginPath(); ctx.moveTo(x, Math.max(top, y0)); ctx.lineTo(x, Math.min(bot, y1)); if (y1 > top && y0 < bot) ctx.stroke();
    }
    ctx.fillStyle = rgb(foam, .9 * dens); ctx.fillRect(x - stride * .6, top - 1.5 * s, stride * 1.2, 4 * s);
  }
  // foam at the foot
  const M = Math.round(30 + 90 * mon);
  for (let k = 0; k < M; k++) {
    const u = hash(k * 1.7) * 2.1 - 1.05;
    const dens = Math.max(strands(u), ss(clamp(mon * 1.35 - Math.abs(u) * .35)));
    if (dens < .1) continue;
    const x = cx + u * R, y = pool(u) + hash(k + 7) * Hf * .22;
    const r = (5 + hash(k + 3) * 13) * s * (.5 + dens) * (.85 + .15 * Math.sin(t * 5 + k));
    ctx.fillStyle = `rgba(255,255,255,${.35 + .3 * dens})`; ctx.beginPath(); ctx.ellipse(x, y, r * 1.6, r, 0, 0, 6.283); ctx.fill();
  }
  // mist
  const mistA = .10 + .22 * mon;
  for (let k = 0; k < 9; k++) {
    const u = hash(k + 200) * 2.2 - 1.1;
    const life = (t * .09 + hash(k + 201)) % 1;
    const x = cx + u * R + Math.sin(t * .5 + k) * 20 * s, y = pool(u) - Hf * (.05 + .7 * life);
    const r = Hf * (.5 + .5 * hash(k + 202)) * (1 + mon * .5);
    const rg = ctx.createRadialGradient(x, y, 0, x, y, r);
    const a = mistA * Math.sin(life * Math.PI);
    rg.addColorStop(0, `rgba(255,255,255,${a})`); rg.addColorStop(1, 'rgba(255,255,255,0)');
    ctx.fillStyle = rg; ctx.fillRect(x - r, y - r, 2 * r, 2 * r);
  }
  // foreground boulders when tall
  if (af > .3) {
    ctx.fillStyle = rgb([66, 54, 44], af * .9);
    const by = h * .9;
    ctx.beginPath(); ctx.ellipse(w * .02, by + h * .04, w * .16, h * .06, -.1, 0, 6.283); ctx.fill();
    ctx.beginPath(); ctx.ellipse(w * 1.0, by + h * .06, w * .18, h * .06, .15, 0, 6.283); ctx.fill();
  }
  return { cx, R, lipY, Hf };
}
