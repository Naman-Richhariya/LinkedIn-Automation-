// Pip: an original 12×15 pixel explorer. Teal hat, orange shirt, a backpack strap.
const COL = { H: '#14B8A6', h: '#0F766E', S: '#F2BE94', O: '#F97316', o: '#C2410C', K: '#7C2D12', L: '#1E293B', E: '#1E1B4B', W: '#FFFFFF' };
const BODY = [
  '....HHHH....',
  '...HHHHHH...',
  '..HHhhhhHH..',
  '.HHHHHHHHHH.',
  '..SSSSSSSS..',
  '..SSSSSSSS..',
  '..SSSSSSSS..',
  '...SSSSSS...',
  '..OOKOOOOO..',
  '..OOOKOOOO..',
  '..OOOOKOOO..',
  '..ooooooooo.',
];
const LEGS = {
  stand: ['...LL..LL...', '...LL..LL...', '..LLL..LLL..'],
  walkA: ['...LL...LL..', '..LL....LL..', '..LL.....LL.'],
  walkB: ['....LL.LL...', '....LL.LL...', '...LLL.LLL..'],
  tuck: ['...LLLLLL...', '....L..L....', '............'],
  sit: ['............', '............', '..LLLLLLLLL.'],
};
export function drawPip(ctx, x, y, p, o) {
  const sx = p * (1 + o.squash), sy = p * (1 - o.squash);
  const legs = LEGS[o.legs] || LEGS.stand;
  const rows = o.legs === 'sit' ? BODY.length + 1 : BODY.length + 3; // sitting body drops two rows
  const grid = BODY.map(r => r.split(''));
  // eyes (cols 4 and 7 on row 5) with look offsets
  const look = { left: [-1, 0], right: [1, 0], up: [0, -1], down: [0, 1] }[o.eyes] || [0, 0];
  const eye = (r, c, v = 'E') => { if (grid[r] && c >= 0 && c < 12) grid[r][c] = v; };
  for (const c0 of [4, 7]) {
    const c = c0 + look[0] * (o.flip ? -1 : 1), r = 5 + look[1];
    if (o.eyes === 'shut') { eye(5, c0 - (c0 === 4 ? 0 : 0), 'E'); eye(5, c0 + (c0 === 4 ? 1 : -1), 'E'); }
    else if (o.eyes === 'happy') { eye(4, c0, 'E'); eye(5, c0 - 1, 'E'); eye(5, c0 + 1, 'E'); }
    else if (o.eyes === 'wide') { eye(4, c0, 'W'); eye(5, c0, 'E'); eye(4, c0 + (c0 === 4 ? -1 : 1), 'W'); eye(5, c0 + (c0 === 4 ? -1 : 1), 'W'); }
    else eye(r, c);
  }
  const px = (r, c, col) => {
    const cc = o.flip ? 11 - c : c;
    ctx.fillStyle = col;
    ctx.fillRect(Math.round(x + (cc - 6) * sx), Math.round(y - (rows - r) * sy), Math.ceil(sx), Math.ceil(sy));
  };
  // soft shadow on the floor
  ctx.fillStyle = 'rgba(15,23,42,.18)'; ctx.fillRect(Math.round(x - 4 * sx), Math.round(y - sy * .4), Math.round(8 * sx), Math.ceil(sy * .5));
  grid.forEach((row, r) => row.forEach((ch, c) => { if (ch !== '.') px(r, c, COL[ch]); }));
  legs.forEach((row, i) => row.split('').forEach((ch, c) => { if (ch !== '.') px(BODY.length + i - (o.legs === 'sit' ? 2 : 0), c, COL[ch]); }));
  // arms
  const arm = (side, up) => {
    const c = side < 0 ? 1 : 10;
    if (up) { px(6, c, COL.S); px(7, c, COL.O); px(8, c, COL.O); }
    else { px(9, c, COL.O); px(10, c, COL.S); }
  };
  arm(-1, o.arms === 'up');
  arm(1, o.arms === 'up' || (o.arms === 'wave' && o.wave));
}
