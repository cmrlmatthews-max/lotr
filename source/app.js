import * as THREE from 'three';
import { MapControls } from 'three/examples/jsm/controls/MapControls.js';
import { Line2 } from 'three/examples/jsm/lines/Line2.js';
import { LineGeometry } from 'three/examples/jsm/lines/LineGeometry.js';
import { LineMaterial } from 'three/examples/jsm/lines/LineMaterial.js';
import { LineSegments2 } from 'three/examples/jsm/lines/LineSegments2.js';
import { LineSegmentsGeometry } from 'three/examples/jsm/lines/LineSegmentsGeometry.js';

const $ = (s, el = document) => el.querySelector(s);
const esc = s => String(s ?? '').replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
const clamp = (v, a, b) => Math.max(a, Math.min(b, v));
const params = new URLSearchParams(location.search);
const STEP = Math.max(1, parseInt(params.get('q') || '1', 10));

const D = JSON.parse($('#me-data').textContent);
let W = 1, H = 1, LAND = null, FE = [];
const ITEMS = D.items;
let EX = 18;
const exFor = d => { const k = clamp((d - 110) / 800, 0, 1); return S.ex * (0.36 + 0.64 * k * k * (3 - 2 * k)); };
const S = {
  ex: 18,
  layers: { settle: true, strong: true, landmark: true, relief: true, woods: true, water: true, roads: true, realms: true, battles: true },
  src: { book: true, film: true, series: true },
  sel: null, journey: null,
};
const LAYER_GROUP = { Towns: 'settle', Harbors: 'settle', Fortresses: 'strong', Doors_Gates: 'strong', Walls: 'strong', Buildings: 'landmark', Bridges: 'landmark', Fords: 'landmark', Cave_entrances: 'landmark', Falls: 'landmark', Graves_Tombs: 'landmark', Mountains: 'relief', Mountains_of_Moria: 'relief', Hills: 'relief', Valleys: 'relief', Fields: 'relief', Islands: 'relief', Forests: 'woods', Swamps: 'woods', Rivers: 'water', Lakes: 'water', Bays: 'water', Roads: 'roads' };
const LAYER_CLASS = { Towns: 'pt town', Harbors: 'pt town', Fortresses: 'pt fort', Doors_Gates: 'pt fort', Buildings: 'pt bld', Bridges: 'pt bld', Fords: 'pt bld', Cave_entrances: 'pt bld', Falls: 'pt bld', Graves_Tombs: 'pt bld', Walls: 'ar road', Mountains: 'ar mtn', Mountains_of_Moria: 'ar mtn', Hills: 'ar hill', Valleys: 'ar hill', Fields: 'ar hill', Islands: 'ar hill', Forests: 'ar wood', Swamps: 'ar wood', Rivers: 'ar water', Lakes: 'ar water', Bays: 'ar water', Roads: 'ar road' };
const TYPE_NAME = { place: 'Place', realm: 'Realm', people: 'People', battle: 'Battle', journey: 'Journey' };

/* ---------- terrain data ---------- */
let hImg, bImg;
let GW, GH, heights;
function decodeHeights() {
  GW = hImg.naturalWidth; GH = hImg.naturalHeight;
  const c = document.createElement('canvas'); c.width = GW; c.height = GH;
  const x = c.getContext('2d', { willReadFrequently: true }); x.drawImage(hImg, 0, 0);
  const d = x.getImageData(0, 0, GW, GH).data; heights = new Float32Array(GW * GH);
  for (let i = 0, j = 0; i < heights.length; i++, j += 4) heights[i] = (d[j] * 256 + d[j + 1]) / 65535 * 4.0; // km
}
function hAt(x, y) {
  const fx = clamp(x / W * (GW - 1), 0, GW - 1.001), fy = clamp((1 - y / H) * (GH - 1), 0, GH - 1.001);
  const i = fx | 0, j = fy | 0, u = fx - i, v = fy - j, o = j * GW + i;
  return (heights[o] * (1 - u) + heights[o + 1] * u) * (1 - v) + (heights[o + GW] * (1 - u) + heights[o + GW + 1] * u) * v;
}
const wx = x => x - W / 2, wz = y => H / 2 - y;

/* ---------- three scene ---------- */
const canvas = $('#gl');
const renderer = new THREE.WebGLRenderer({ canvas, antialias: true, alpha: true, powerPreference: 'high-performance' });
renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));
const scene = new THREE.Scene();
scene.fog = new THREE.FogExp2(0x1a120b, 0.00011);
const camera = new THREE.PerspectiveCamera(36, 1, 6, 14000);
const controls = new MapControls(camera, canvas);
controls.enableDamping = true; controls.dampingFactor = 0.09; controls.screenSpacePanning = false;
controls.minDistance = 28; controls.maxDistance = 4300; controls.maxPolarAngle = Math.PI * 0.46;
controls.zoomToCursor = true; controls.zoomSpeed = 1.1; controls.rotateSpeed = 0.5;
const terrain = new THREE.Group(); scene.add(terrain);
let tex, cv, ctx, KX, KY, mesh, slab;
const lineMats = [];

function buildTerrain() {
  const nx = Math.floor((GW - 1) / STEP) + 1, ny = Math.floor((GH - 1) / STEP) + 1;
  const pos = new Float32Array(nx * ny * 3), uv = new Float32Array(nx * ny * 2);
  for (let j = 0, p = 0, q = 0; j < ny; j++) for (let i = 0; i < nx; i++) {
    const fi = i * STEP, fj = j * STEP;
    pos[p++] = (fi / (GW - 1) - 0.5) * W; pos[p++] = heights[fj * GW + fi]; pos[p++] = (fj / (GH - 1) - 0.5) * H;
    uv[q++] = fi / (GW - 1); uv[q++] = 1 - fj / (GH - 1);
  }
  const idx = new Uint32Array((nx - 1) * (ny - 1) * 6);
  for (let j = 0, k = 0; j < ny - 1; j++) for (let i = 0; i < nx - 1; i++) {
    const a = j * nx + i, b = a + 1, c = a + nx, d = c + 1;
    idx[k++] = a; idx[k++] = c; idx[k++] = b; idx[k++] = b; idx[k++] = c; idx[k++] = d;
  }
  const g = new THREE.BufferGeometry();
  g.setAttribute('position', new THREE.BufferAttribute(pos, 3)); g.setAttribute('uv', new THREE.BufferAttribute(uv, 2));
  g.setIndex(new THREE.BufferAttribute(idx, 1));
  g.boundingSphere = new THREE.Sphere(new THREE.Vector3(0, 0, 0), Math.hypot(W, H) / 2 + 100);
  const maxT = renderer.capabilities.maxTextureSize; const sc = Math.min(1, maxT / bImg.naturalWidth);
  cv = document.createElement('canvas'); cv.width = Math.round(bImg.naturalWidth * sc); cv.height = Math.round(bImg.naturalHeight * sc);
  ctx = cv.getContext('2d'); KX = cv.width / W; KY = cv.height / H;
  tex = new THREE.CanvasTexture(cv); tex.colorSpace = THREE.SRGBColorSpace; tex.anisotropy = renderer.capabilities.getMaxAnisotropy();
  const gc = document.createElement('canvas'); gc.width = gc.height = 256; const gx = gc.getContext('2d'), gd = gx.createImageData(256, 256);
  for (let i = 0; i < gd.data.length; i += 4) { const v = 96 + Math.random() * 64 + (Math.random() < 0.04 ? -50 : 0); gd.data[i] = gd.data[i + 1] = gd.data[i + 2] = v; gd.data[i + 3] = 255; }
  gx.putImageData(gd, 0, 0); const grain = new THREE.CanvasTexture(gc); grain.wrapS = grain.wrapT = THREE.RepeatWrapping;
  const mat = new THREE.MeshBasicMaterial({ map: tex });
  mat.onBeforeCompile = sh => { sh.uniforms.grain = { value: grain }; sh.fragmentShader = sh.fragmentShader.replace('#include <common>', '#include <common>\nuniform sampler2D grain;').replace('#include <map_fragment>', '#include <map_fragment>\n diffuseColor.rgb *= 0.90 + 0.20 * texture2D(grain, vMapUv * vec2(150.0, 123.0)).r; diffuseColor.rgb *= 0.95 + 0.10 * texture2D(grain, vMapUv * vec2(23.0, 19.0) + 0.37).r;'); };
  mesh = new THREE.Mesh(g, mat);
  terrain.add(mesh);
  // underside slab so the sheet reads as an object on a table
  slab = new THREE.Mesh(new THREE.BoxGeometry(W + 26, 12, H + 26), new THREE.MeshBasicMaterial({ color: 0x4a3622 }));
  slab.position.y = -9; scene.add(slab);
  terrain.scale.y = EX;
}

/* ---------- map ink (2D canvas draped on the terrain) ---------- */
function trace(geom, close) {
  ctx.beginPath();
  for (const p of geom) { for (let i = 0; i < p.length; i += 2) { const X = p[i] * KX, Y = (H - p[i + 1]) * KY; i ? ctx.lineTo(X, Y) : ctx.moveTo(X, Y); } if (close) ctx.closePath(); }
}
function pattern(kind) {
  const c = document.createElement('canvas'), s = cv.width / 3920; c.width = Math.round(26 * s); c.height = Math.round(22 * s);
  const x = c.getContext('2d'); x.scale(s, s); x.lineCap = 'round';
  if (kind === 'wood') {
    x.strokeStyle = 'rgba(58,76,40,.62)'; x.fillStyle = 'rgba(96,120,64,.30)'; x.lineWidth = 1;
    for (const [cx, cy] of [[6, 8], [19, 5], [13, 17]]) { x.beginPath(); x.arc(cx, cy, 3.6, Math.PI, 0); x.lineTo(cx + 3.6, cy + 1); x.lineTo(cx - 3.6, cy + 1); x.closePath(); x.fill(); x.stroke(); x.beginPath(); x.moveTo(cx, cy + 1); x.lineTo(cx, cy + 3.6); x.stroke(); }
  } else {
    x.strokeStyle = 'rgba(60,84,84,.6)'; x.lineWidth = 1;
    for (const [cx, cy] of [[6, 7], [18, 15]]) { x.beginPath(); x.moveTo(cx - 4, cy); x.lineTo(cx + 4, cy); x.moveTo(cx - 2, cy); x.lineTo(cx - 3, cy - 3); x.moveTo(cx, cy); x.lineTo(cx, cy - 4); x.moveTo(cx + 2, cy); x.lineTo(cx + 3, cy - 3); x.stroke(); }
  }
  return ctx.createPattern(c, 'repeat');
}
let patWood, patSwamp;
function lineLen(geom) { let L = 0; for (const p of geom) for (let i = 2; i < p.length; i += 2) L += Math.hypot(p[i] - p[i - 2], p[i + 1] - p[i - 1]); return L; }
function redraw() {
  const s = cv.width / 3920; ctx.setLineDash([]); ctx.globalAlpha = 1;
  ctx.drawImage(bImg, 0, 0, cv.width, cv.height);
  ctx.lineJoin = 'round'; ctx.lineCap = 'round';
  patWood = patWood || pattern('wood'); patSwamp = patSwamp || pattern('swamp');
  if (S.layers.woods) for (const f of FE) {
    if (f.layer === 'Forests') { trace(f.geom, true); ctx.fillStyle = 'rgba(104,126,66,.24)'; ctx.fill('evenodd'); ctx.fillStyle = patWood; ctx.fill('evenodd'); ctx.strokeStyle = 'rgba(58,76,40,.45)'; ctx.lineWidth = 1.1 * s; ctx.stroke(); }
    if (f.layer === 'Swamps') { trace(f.geom, true); ctx.fillStyle = 'rgba(96,128,120,.20)'; ctx.fill('evenodd'); ctx.fillStyle = patSwamp; ctx.fill('evenodd'); }
  }
  if (S.layers.water) {
    for (const f of FE) if (f.layer === 'Lakes') {
      trace(f.geom, true); ctx.fillStyle = 'rgb(176,193,180)'; ctx.fill('evenodd'); ctx.strokeStyle = 'rgba(70,58,40,.9)'; ctx.lineWidth = 1.3 * s; ctx.stroke();
      ctx.save(); ctx.clip('evenodd'); ctx.strokeStyle = 'rgba(62,98,116,.35)'; ctx.lineWidth = 7 * s; ctx.stroke(); ctx.restore();
    }
  }
  if (LAND.compass) drawCompass(...LAND.compass); drawSeaNames(s);
  tex.needsUpdate = true; dirty = true;
}
function drawCompass(x, y, r) {
  const X = x * KX, Y = (H - y) * KY, R = r * KX; ctx.save(); ctx.translate(X, Y);
  ctx.strokeStyle = 'rgba(58,42,27,.75)'; ctx.fillStyle = 'rgba(58,42,27,.75)'; ctx.lineWidth = Math.max(1, R / 70);
  for (const rr of [1, 0.93, 0.52]) { ctx.beginPath(); ctx.arc(0, 0, R * rr, 0, 7); ctx.stroke(); }
  for (let k = 0; k < 16; k++) {
    const a = k * Math.PI / 8, len = k % 4 === 0 ? 1.18 : k % 2 === 0 ? 0.8 : 0.5, wd = k % 4 === 0 ? 0.11 : 0.075;
    ctx.save(); ctx.rotate(a); ctx.beginPath(); ctx.moveTo(0, -R * len); ctx.lineTo(R * wd, 0); ctx.lineTo(-R * wd, 0); ctx.closePath();
    ctx.stroke(); ctx.beginPath(); ctx.moveTo(0, -R * len); ctx.lineTo(R * wd, 0); ctx.lineTo(0, 0); ctx.closePath(); ctx.fillStyle = k === 0 ? 'rgba(142,47,31,.85)' : 'rgba(58,42,27,.7)'; ctx.fill(); ctx.restore();
  }
  ctx.fillStyle = 'rgba(142,47,31,.9)'; ctx.font = `600 ${R * 0.34}px "Hoefler Text",Baskerville,Georgia,serif`; ctx.textAlign = 'center'; ctx.fillText('N', 0, -R * 1.28);
  // scale bar
  const u = 100 * KX; ctx.translate(-u * 1.5, R * 1.62); ctx.fillStyle = 'rgba(58,42,27,.8)';
  for (let k = 0; k < 3; k++) { ctx.beginPath(); ctx.rect(k * u, 0, u, R * 0.07); k % 2 ? ctx.stroke() : ctx.fill(); }
  ctx.font = `${R * 0.2}px "Hoefler Text",Baskerville,Georgia,serif`; ctx.fillStyle = 'rgba(58,42,27,.85)';
  ctx.fillText('0', 0, R * 0.33); ctx.fillText('100', u, R * 0.33); ctx.fillText('200', 2 * u, R * 0.33); ctx.fillText('300 km', 3 * u, R * 0.33);
  ctx.restore();
}
function drawSeaNames(s) {
  ctx.save(); ctx.fillStyle = 'rgba(54,84,100,.55)'; ctx.textAlign = 'center';
  const spaced = (t, x, y, size, gap, rot) => { ctx.save(); ctx.translate(x * KX, (H - y) * KY); ctx.rotate(rot); const f = KX * 0.6; ctx.font = `italic ${size * f}px "Hoefler Text",Baskerville,Georgia,serif`; let w = 0; for (const ch of t) w += ctx.measureText(ch).width + gap * f; let px = -w / 2; ctx.textAlign = 'left'; for (const ch of t) { ctx.fillText(ch, px, 0); px += ctx.measureText(ch).width + gap * f; } ctx.restore(); };
  for (const n of LAND.sea || []) spaced(...n);
  ctx.restore();
}

/* ---------- labels ---------- */
const labelLayer = $('#labels'); const labels = [];
function addLabel(item, cls, group, rank, prio) {
  const el = document.createElement('div'); el.className = `lbl ${cls} r${rank}`; el.dataset.id = item.id;
  el.innerHTML = (cls.startsWith('pt') || cls.startsWith('battle') ? '<i></i>' : '') + `<span>${esc(cls.includes('realm') ? item.title.replace(/\s*\(.*\)/, '') : item.title)}</span>`;
  labelLayer.appendChild(el);
  labels.push({ item, el, cls, group, rank, prio, pt: cls.startsWith('pt') || cls.startsWith('battle'), wx: wx(item.x), wz: wz(item.y), hy: hAt(item.x, item.y), on: false, w: 0, h: 0 });
}
function buildLabels() {
  for (const it of Object.values(ITEMS)) {
    if (it.x == null || it.land !== LAND.id) continue;
    if (it.type === 'place') addLabel(it, LAYER_CLASS[it.layer] || 'pt bld', LAYER_GROUP[it.layer] || 'landmark', it.tier || 3, (it.tier || 3) * 10 + (it.layer === 'Towns' ? 1 : it.layer === 'Fortresses' ? 2 : /Mountains|Forests|Rivers/.test(it.layer) ? 4 : 6));
    else if (it.type === 'realm') addLabel(it, 'ar realm' + (it.rtype === 'region' ? ' region' : ''), 'realms', it.tier || 2, (it.tier || 2) * 10);
    else if (it.type === 'battle') addLabel(it, 'battle', 'battles', it.tier || 2, (it.tier || 2) * 10 + 3);
  }
  for (const L of labels) { const sp = L.el.lastElementChild; L.w = sp.offsetWidth; L.h = sp.offsetHeight; }
  labels.sort((a, b) => a.prio - b.prio || a.item.title.localeCompare(b.item.title));
}
function rankVisible(L, dl) {
  if (L.group === 'realms') return L.rank === 1 ? dl > 520 : L.rank === 2 ? dl > 200 && dl < 1700 : dl > 110 && dl < 800;
  if (L.group === 'battles') return L.rank === 1 ? dl < 3200 : L.rank === 2 ? dl < 1300 : dl < 600;
  return L.rank === 1 ? dl < 3400 : L.rank === 2 ? dl < 950 : dl < 340;
}
const _v = new THREE.Vector3(); let vw = 1, vh = 1; const placed = [], placedR = [];
function updateLabels() {
  placed.length = 0; placedR.length = 0; const cp = camera.position;
  const one = L => {
    const sel = L.item.id === S.sel; let show = sel || (S.layers[L.group] && !(S.journey && L.group === 'battles')), sx = 0, sy = 0;
    if (show) {
      _v.set(L.wx, L.hy * EX, L.wz); const dl = _v.distanceTo(cp);
      show = sel || rankVisible(L, dl);
      if (show) {
        _v.project(camera);
        if (_v.z > 1 || _v.z < -1 || Math.abs(_v.x) > 1.02 || Math.abs(_v.y) > 1.02) show = false;
        else {
          sx = (_v.x * 0.5 + 0.5) * vw; sy = (-_v.y * 0.5 + 0.5) * vh;
          const x0 = L.pt ? sx - 6 : sx - L.w / 2 - 3, x1 = L.pt ? sx + 10 + L.w : sx + L.w / 2 + 3, y0 = sy - L.h / 2 - 1, y1 = sy + L.h / 2 + 1;
          const pool = L.group === 'realms' ? placedR : placed;
          if (!sel) for (let k = 0; k < pool.length; k += 4) if (x0 < pool[k + 2] && x1 > pool[k] && y0 < pool[k + 3] && y1 > pool[k + 1]) { show = false; break; }
          if (show) { pool.push(x0, y0, x1, y1); L.rect = [x0, y0 - 3, x1, y1 + 3]; }
        }
      }
    }
    if (show) L.el.style.transform = `translate(${sx.toFixed(1)}px,${sy.toFixed(1)}px)`;
    if (show !== L.on) { L.on = show; L.el.classList.toggle('on', show); }
    L.el.classList.toggle('sel', sel);
  };
  for (const L of labels) if (L.item.id === S.sel) one(L);
  for (const L of labels) if (L.item.id !== S.sel) one(L);
}
function project(x, y, lift = 0) { _v.set(wx(x), (hAt(x, y) + lift) * EX, wz(y)).project(camera); return _v.z > 1 || _v.z < -1 ? null : [(_v.x * 0.5 + 0.5) * vw, (-_v.y * 0.5 + 0.5) * vh]; }

/* ---------- lines on the terrain ---------- */
function densify(pts, stepKm = 1.5) {
  const out = [];
  for (let i = 0; i < pts.length - 1; i++) {
    const [ax, ay] = pts[i], [bx, by] = pts[i + 1], n = Math.max(1, Math.ceil(Math.hypot(bx - ax, by - ay) / stepKm));
    for (let k = 0; k < n; k++) out.push([ax + (bx - ax) * k / n, ay + (by - ay) * k / n]);
  }
  out.push(pts[pts.length - 1]); return out;
}
function makeLine(pts, color, width, opts = {}) {
  const arr = new Float32Array(pts.length * 3);
  for (let i = 0; i < pts.length; i++) {
    const [x, y] = pts[i]; let h = hAt(x, y);
    h = Math.max(h, hAt(x + 1.2, y), hAt(x - 1.2, y), hAt(x, y + 1.2), hAt(x, y - 1.2));
    arr[i * 3] = wx(x); arr[i * 3 + 1] = h + (opts.lift ?? 0.07); arr[i * 3 + 2] = wz(y);
  }
  const g = new LineGeometry(); g.setPositions(arr);
  const m = new LineMaterial({ color, linewidth: width, transparent: true, opacity: opts.opacity ?? 1, dashed: !!opts.dash, dashSize: opts.dash?.[0] ?? 1, gapSize: opts.dash?.[1] ?? 1, depthWrite: false });
  m.resolution.set(vw, vh); lineMats.push(m); if (opts.dash) dashMats.add(m);
  const l = new Line2(g, m); l.computeLineDistances(); l.renderOrder = opts.order ?? 2; terrain.add(l); return l;
}
function dropLine(l) { if (!l) return; terrain.remove(l); l.geometry.dispose(); const i = lineMats.indexOf(l.material); if (i >= 0) lineMats.splice(i, 1); dashMats.delete(l.material); l.material.dispose(); }
const ink = { water: [], roads: [], realms: [] }, dashMats = new Set();
const hLine = (x, y) => Math.max(hAt(x, y), hAt(x + 1.2, y), hAt(x - 1.2, y), hAt(x, y + 1.2), hAt(x, y - 1.2));
function makeSegs(feats, color, width, opts = {}) {
  const arr = [];
  for (const f of feats) for (const p of f.geom) {
    const raw = []; for (let i = 0; i < p.length; i += 2) raw.push([p[i], p[i + 1]]); if (opts.close) raw.push(raw[0]);
    const pts = densify(raw, 1.5);
    for (let i = 0; i < pts.length - 1; i++) arr.push(wx(pts[i][0]), hLine(pts[i][0], pts[i][1]) + 0.05, wz(pts[i][1]), wx(pts[i + 1][0]), hLine(pts[i + 1][0], pts[i + 1][1]) + 0.05, wz(pts[i + 1][1]));
  }
  if (!arr.length) return null;
  const g = new LineSegmentsGeometry(); g.setPositions(arr);
  const m = new LineMaterial({ color, linewidth: width, transparent: true, opacity: opts.opacity ?? 0.92, dashed: !!opts.dash, dashSize: opts.dash?.[0] ?? 1, gapSize: opts.dash?.[1] ?? 1, depthWrite: false });
  m.resolution.set(vw, vh); lineMats.push(m); if (opts.dash) dashMats.add(m);
  const l = new LineSegments2(g, m); l.computeLineDistances(); l.renderOrder = 1; terrain.add(l); return l;
}
function buildInk() {
  const rv = FE.filter(f => f.layer === 'Rivers'), len = f => lineLen(f.geom);
  ink.water.push(makeSegs(rv.filter(f => len(f) > 450), 0x3a6078, 3.1), makeSegs(rv.filter(f => len(f) > 140 && len(f) <= 450), 0x3a6078, 2.1), makeSegs(rv.filter(f => len(f) <= 140), 0x3a6078, 1.4));
  const rd = FE.filter(f => f.layer === 'Roads'), major = f => /major/i.test((f.attrs && f.attrs.Type) || '') || len(f) > 180;
  ink.roads.push(makeSegs(rd.filter(major), 0x74381c, 2.1, { dash: [1, 0.55] }), makeSegs(rd.filter(f => !major(f)), 0x74381c, 1.3, { dash: [0.6, 0.5], opacity: 0.8 }), makeSegs(FE.filter(f => f.layer === 'Walls'), 0x2e2016, 1.8));
  ink.realms.push(makeSegs(FE.filter(f => f.layer === 'Realms' || f.layer === 'Place_Boundaries'), 0x8e2f1f, 1.9, { dash: [1.5, 0.5], opacity: 0.6, close: true }));
  ink.water = ink.water.filter(Boolean); ink.roads = ink.roads.filter(Boolean); ink.realms = ink.realms.filter(Boolean);
}
function syncInk() { ink.water.forEach(l => l.visible = S.layers.water); ink.roads.forEach(l => l.visible = S.layers.roads); ink.realms.forEach(l => l.visible = S.layers.realms); }
let hiLines = [];
function setHighlight(it) {
  hiLines.forEach(dropLine); hiLines = [];
  if (!it || it.type !== 'place') return;
  for (const f of FE) if (f.card === it.id && f.geom) for (const p of f.geom) {
    const pts = []; for (let i = 0; i < p.length; i += 2) pts.push([p[i], p[i + 1]]);
    if (f.kind === 'poly') pts.push(pts[0]);
    if (pts.length > 1) hiLines.push(makeLine(densify(pts, 2.5), 0xa8321c, 2.6, { opacity: 0.9 }));
  }
  dirty = true;
}

/* ---------- camera ---------- */
let tween = null;
function flyTo(x, y, dist, ms = 1500) {
  x = clamp(x, 0, W); y = clamp(y, 0, H);
  const to = new THREE.Vector3(wx(x), hAt(x, y) * EX, wz(y));
  const off = camera.position.clone().sub(controls.target); const cur = off.length(); dist = dist || cur;
  const sph = new THREE.Spherical().setFromVector3(off); const phi1 = dist < 500 ? clamp(sph.phi, 0.75, 1.05) : sph.phi;
  tween = { t0: performance.now(), ms, a: controls.target.clone(), b: to, r0: cur, r1: dist, phi0: sph.phi, phi1, theta: sph.theta };
}
function stepTween(now) {
  if (!tween) return; let k = clamp((now - tween.t0) / tween.ms, 0, 1); const e = k < 0.5 ? 4 * k * k * k : 1 - Math.pow(-2 * k + 2, 3) / 2;
  controls.target.lerpVectors(tween.a, tween.b, e);
  const r = Math.exp(Math.log(tween.r0) + (Math.log(tween.r1) - Math.log(tween.r0)) * e) + Math.sin(e * Math.PI) * tween.a.distanceTo(tween.b) * 0.22;
  const sph = new THREE.Spherical(r, tween.phi0 + (tween.phi1 - tween.phi0) * e, tween.theta);
  camera.position.setFromSpherical(sph).add(controls.target); camera.lookAt(controls.target);
  if (k >= 1) tween = null; dirty = true;
}
canvas.addEventListener('pointerdown', () => { tween = null; if (J && J.playing) setPlaying(false); });
canvas.addEventListener('wheel', () => { tween = null; }, { passive: true });
const ray = new THREE.Raycaster();
function groundAt(clientX, clientY) {
  const r = canvas.getBoundingClientRect(); ray.setFromCamera(new THREE.Vector2((clientX - r.left) / r.width * 2 - 1, -(clientY - r.top) / r.height * 2 + 1), camera);
  const o = ray.ray.origin, d = ray.ray.direction; let t = 0;
  for (let i = 0; i < 4000; i++) { const px = o.x + d.x * t, py = o.y + d.y * t, pz = o.z + d.z * t; const x = px + W / 2, y = H / 2 - pz; if (x >= 0 && x <= W && y >= 0 && y <= H && py <= hAt(x, y) * EX) return [x, y]; if (py < -5) return null; t += Math.max(1.5, t * 0.004); }
  return null;
}
canvas.addEventListener('dblclick', e => { const L = hitLabel(e.clientX, e.clientY); if (L) { select(L.item.id, true); return; } const g = groundAt(e.clientX, e.clientY); if (g) flyTo(g[0], g[1], Math.max(40, camera.position.distanceTo(controls.target) * 0.45), 900); });

/* ---------- selection and cards ---------- */
const card = $('#card');
const paras = t => String(t || '').split(/\n\s*\n/).map(p => `<p>${esc(p.trim())}</p>`).join('');
const chip = id => ITEMS[id] ? `<a class="chip" data-go="${esc(id)}">${esc(ITEMS[id].title)}</a>` : '';
function renderCard(it) {
  let h = `<button class="x" data-close title="Close (Esc)">&times;</button><div class="kind">${esc(it.kind || TYPE_NAME[it.type])}${it.status ? ' &middot; ' + esc(it.status) : ''}</div><h2>${esc(it.title)}</h2>`;
  if (it.date || it.dates) h += `<div class="date">${esc(it.date || it.dates)}${it.war ? ' &middot; ' + esc(it.war) : ''}</div>`;
  if (it.travellers) h += `<div class="date">${esc(it.travellers)} &middot; <em>${esc(it.source || '')}</em></div>`;
  if (it.blurb) h += `<p class="blurb">${esc(it.blurb)}</p>`;
  if (it.names && Object.keys(it.names).length) h += `<div class="names">${Object.entries(it.names).map(([k, v]) => `<span><b>${esc(k)}</b> ${esc(v)}</span>`).join('')}</div>`;
  if (it.sides) h += `<div class="sides"><div><b>Victor / defender</b>${it.sides.a.map(esc).join('<br>')}</div><div><b>Opponent</b>${it.sides.b.map(esc).join('<br>')}</div></div>${it.outcome ? `<p class="outcome"><b>Outcome.</b> ${esc(it.outcome)}</p>` : ''}`;
  const sec = (key, name, txt) => txt && S.src[key] ? `<section class="src ${key}"><h3><span class="tag">${name}</span></h3>${paras(txt)}</section>` : '';
  const body = sec('book', 'Book', it.book) + sec('film', 'Film', it.film) + sec('series', 'Series', it.series);
  h += body || `<p class="muted">No text for the selected sources.</p>`;
  if (it.facts && Object.keys(it.facts).length) h += `<dl class="facts">${Object.entries(it.facts).map(([k, v]) => `<dt>${esc(k)}</dt><dd>${esc(v)}</dd>`).join('')}</dl>`;
  if (it.type === 'journey') h += `<h4>Stages</h4><ol class="stages">${it.stages.map((s, i) => `<li data-stage="${i}"><b>${esc(s.title)}</b>${s.date ? `<span class="sd">${esc(s.date)}</span>` : ''}<div>${esc(s.note)}</div>${s.film && S.src.film ? `<div class="sf"><span class="tag f">Film</span> ${esc(s.film)}</div>` : ''}</li>`).join('')}</ol>`;
  const list = (title, ids) => { const c = (ids || []).map(chip).join(''); return c ? `<h4>${title}</h4><div class="chips">${c}</div>` : ''; };
  h += list('Peoples', it.peoples) + list('Lands', it.realms) + list('See also', it.related);
  if (it.sources && it.sources.length) h += `<p class="sources"><b>Where to read:</b> ${it.sources.map(esc).join('; ')}</p>`;
  h += `<p class="conf c-${esc(it.confidence || 'medium')}">Confidence: ${esc(it.confidence || 'medium')}${it.confidence === 'high' ? '' : '. Check this card against the books.'}</p>`;
  card.innerHTML = h; card.scrollTop = 0; card.classList.add('open');
}
function select(id, fly = true) {
  const it = ITEMS[id]; if (!it) return;
  if (LAND && it.land !== LAND.id) { setLand(it.land).then(() => select(id, fly)); return; }
  if (it.type === 'journey') { startJourney(id); return; }
  if (it.type !== 'journey' && J && !(it.type === 'place' || it.type === 'battle')) stopJourney();
  S.sel = id; renderCard(it); setHighlight(it);
  if (fly && it.x != null) {
    const d = it.type === 'realm' ? clamp((it.radius || 200) * 4.2, 320, 2200) : it.type === 'battle' ? 200 : it.area ? clamp(Math.sqrt(it.area) * 5, 90, 1500) : /Rivers|Roads/.test(it.layer) ? 420 : (it.tier === 1 ? 170 : 110);
    flyTo(it.x, it.y, d);
  } else if (fly && it.type === 'people' && it.realms && ITEMS[it.realms[0]]) { const r = ITEMS[it.realms[0]]; flyTo(r.x, r.y, 900); }
  dirty = true;
}
function closeCard() { card.classList.remove('open'); S.sel = null; setHighlight(null); dirty = true; }
card.addEventListener('click', e => {
  const t = e.target.closest('[data-go],[data-close],[data-stage]'); if (!t) return;
  if (t.dataset.close !== undefined) { J ? stopJourney() : closeCard(); }
  else if (t.dataset.go) select(t.dataset.go);
  else if (t.dataset.stage !== undefined && J) gotoStage(+t.dataset.stage, true);
});
function hitLabel(x, y) {
  let best = null;
  for (const L of labels) if (L.on && L.rect && x >= L.rect[0] && x <= L.rect[2] && y >= L.rect[1] && y <= L.rect[3]) { if (L.group !== 'realms') return L; best = best || L; }
  return best;
}
let downXY = null, hover = null;
canvas.addEventListener('pointerdown', e => { downXY = [e.clientX, e.clientY]; });
canvas.addEventListener('pointerup', e => { if (!downXY) return; const m = Math.hypot(e.clientX - downXY[0], e.clientY - downXY[1]); downXY = null; if (m < 5 && e.button === 0) { const L = hitLabel(e.clientX, e.clientY); if (L) select(L.item.id, false); } });
canvas.addEventListener('pointermove', e => { if (e.buttons) return; const L = hitLabel(e.clientX, e.clientY); if (L !== hover) { if (hover) hover.el.classList.remove('hov'); hover = L; if (L) L.el.classList.add('hov'); canvas.style.cursor = L ? 'pointer' : ''; } });

/* ---------- journeys ---------- */
let J = null; const bar = $('#jbar'), stageLayer = $('#stages'), walker = $('#walker');
function spline(P) {
  const pts = P.filter((p, i) => !i || Math.hypot(p[0] - P[i - 1][0], p[1] - P[i - 1][1]) > 0.5); if (pts.length < 3) return pts;
  const out = []; const g = i => pts[clamp(i, 0, pts.length - 1)];
  for (let i = 0; i < pts.length - 1; i++) {
    const p0 = g(i - 1), p1 = g(i), p2 = g(i + 1), p3 = g(i + 2);
    for (let k = 0; k < 14; k++) { const t = k / 14, t2 = t * t, t3 = t2 * t; out.push([0.5 * (2 * p1[0] + (-p0[0] + p2[0]) * t + (2 * p0[0] - 5 * p1[0] + 4 * p2[0] - p3[0]) * t2 + (-p0[0] + 3 * p1[0] - 3 * p2[0] + p3[0]) * t3), 0.5 * (2 * p1[1] + (-p0[1] + p2[1]) * t + (2 * p0[1] - 5 * p1[1] + 4 * p2[1] - p3[1]) * t2 + (-p0[1] + 3 * p1[1] - 3 * p2[1] + p3[1]) * t3)]); }
  }
  out.push(pts[pts.length - 1]); return out;
}
function startJourney(id) {
  stopJourney(true); const it = ITEMS[id]; if (!it || !it.stages || it.stages.length < 2) return;
  const raw = it.path && it.path.length > 3 ? it.path : spline(it.stages.map(s => [s.x, s.y]));
  const pts = densify(raw, 1.5).map(p => [clamp(p[0], 1, W - 1), clamp(p[1], 1, H - 1)]); const cum = [0];
  for (let i = 1; i < pts.length; i++) cum.push(cum[i - 1] + Math.hypot(pts[i][0] - pts[i - 1][0], pts[i][1] - pts[i - 1][1]));
  let last = 0; const sp = it.stages.map(s => { let bi = last, bd = 1e9; for (let i = last; i < pts.length; i++) { const d = Math.hypot(pts[i][0] - s.x, pts[i][1] - s.y); if (d < bd) { bd = d; bi = i; } } last = bi; return bi; });
  sp[0] = 0; sp[sp.length - 1] = pts.length - 1;
  J = { it, pts, cum, total: cum[cum.length - 1], sp, i: 0, k: 0, playing: false, stage: 0 };
  J.ghost = makeLine(pts, 0x8e2f1f, 2.2, { dash: [1, 0.8], opacity: 0.6, order: 3, lift: 0.09 });
  J.done = makeLine(pts, 0xb3261a, 4, { opacity: 0.95, order: 4, lift: 0.1 }); J.done.geometry.instanceCount = 0;
  stageLayer.innerHTML = it.stages.map((s, i) => `<div class="stg" data-stage="${i}" title="${esc(s.title)}"><b>${i + 1}</b></div>`).join('');
  J.els = [...stageLayer.children]; S.journey = id; S.sel = id; setHighlight(null); renderCard(it);
  bar.classList.add('open'); walker.classList.add('on'); document.querySelectorAll('#journeys button').forEach(b => b.classList.toggle('act', b.dataset.go === id));
  gotoStage(0, false); const xs = pts.map(p => p[0]), ys = pts.map(p => p[1]);
  const cx = (Math.min(...xs) + Math.max(...xs)) / 2, cy = (Math.min(...ys) + Math.max(...ys)) / 2, span = Math.max(Math.max(...xs) - Math.min(...xs), (Math.max(...ys) - Math.min(...ys)) * 1.4);
  flyTo(cx, cy, clamp(span * 1.25, 300, 3200)); dirty = true;
}
function stopJourney(keepCard) {
  if (!J) return; dropLine(J.ghost); dropLine(J.done); stageLayer.innerHTML = ''; bar.classList.remove('open'); walker.classList.remove('on');
  document.querySelectorAll('#journeys button').forEach(b => b.classList.remove('act')); J = null; S.journey = null; if (!keepCard) closeCard(); dirty = true;
}
function setProgress(i) {
  J.i = clamp(i, 0, J.pts.length - 1); J.done.geometry.instanceCount = Math.floor(J.i);
  let st = 0; for (let s = 0; s < J.sp.length; s++) if (J.sp[s] <= J.i + 0.5) st = s;
  if (st !== J.stage || !bar.dataset.s) { J.stage = st; bar.dataset.s = '1'; showStage(st); }
  dirty = true;
}
function showStage(st) {
  const s = J.it.stages[st];
  $('#jtitle').textContent = J.it.title; $('#jstage').innerHTML = `<b>${st + 1} / ${J.it.stages.length} &middot; ${esc(s.title)}</b>${s.date ? ` <span>${esc(s.date)}</span>` : ''}`;
  $('#jnote').innerHTML = esc(s.note) + (s.film && S.src.film ? ` <span class="tag f">Film</span> ${esc(s.film)}` : '');
  J.els.forEach((e, i) => { e.classList.toggle('cur', i === st); e.classList.toggle('past', i < st); });
  card.querySelectorAll('.stages li').forEach((li, i) => li.classList.toggle('cur', i === st));
  const li = card.querySelector('.stages li.cur'); if (li && !J.playing) li.scrollIntoView({ block: 'nearest' });
}
function gotoStage(st, fly) { st = clamp(st, 0, J.it.stages.length - 1); setPlaying(false); setProgress(J.sp[st]); J.stage = st; showStage(st); if (fly) { const s = J.it.stages[st]; flyTo(s.x, s.y, Math.min(camera.position.distanceTo(controls.target), 380), 1100); } }
function setPlaying(p) {
  if (!J) return; J.playing = p; $('#jplay').textContent = p ? 'Pause' : 'Play'; if (p) { tween = null; if (J.i >= J.pts.length - 2) setProgress(0); J.dur = clamp(J.total / 55, 22, 80); const d = camera.position.distanceTo(controls.target); if (d > 520) { const p0 = J.pts[Math.floor(J.i)]; flyTo(p0[0], p0[1], 360, 900); } }
}
bar.addEventListener('click', e => { const b = e.target.closest('button'); if (!b || !J) return; if (b.id === 'jplay') setPlaying(!J.playing); if (b.id === 'jprev') gotoStage(J.stage - 1, true); if (b.id === 'jnext') gotoStage(J.stage + 1, true); if (b.id === 'jclose') stopJourney(); });
stageLayer.addEventListener('click', e => { const s = e.target.closest('.stg'); if (s && J) gotoStage(+s.dataset.stage, true); });
function stepJourney(dt) {
  if (!J) return;
  if (J.playing && !tween) {
    setProgress(J.i + (J.pts.length - 1) / J.dur * dt);
    const p = J.pts[Math.floor(J.i)], to = new THREE.Vector3(wx(p[0]), hAt(p[0], p[1]) * EX, wz(p[1])), d = to.sub(controls.target).multiplyScalar(Math.min(1, dt * 2.2));
    controls.target.add(d); camera.position.add(d);
    if (J.i >= J.pts.length - 1) setPlaying(false);
  }
  const p = J.pts[Math.floor(J.i)], s = project(p[0], p[1], 0.1);
  walker.style.transform = s ? `translate(${s[0].toFixed(1)}px,${s[1].toFixed(1)}px)` : 'translate(-99px,-99px)';
  J.it.stages.forEach((st, i) => { const q = project(st.x, st.y, 0.1); J.els[i].style.transform = q ? `translate(${q[0].toFixed(1)}px,${q[1].toFixed(1)}px)` : 'translate(-99px,-99px)'; });
}

/* ---------- side panel, search ---------- */
function buildPanel() {
  const by = t => Object.values(ITEMS).filter(i => i.type === t && i.land === LAND.id);
  $('#journeys').innerHTML = by('journey').map(j => `<button data-go="${esc(j.id)}"><b>${esc(j.title)}</b><span>${esc(j.travellers || '')}</span></button>`).join('') || '<p class="muted">No journeys loaded.</p>';
  $('#peoples').innerHTML = by('people').sort((a, b) => a.title.localeCompare(b.title)).map(p => `<a class="chip" data-go="${esc(p.id)}">${esc(p.title)}</a>`).join('');
  const bs = by('battle').sort((a, b) => (a.year_sort || 0) - (b.year_sort || 0));
  $('#battlelist').innerHTML = bs.map(b => `<a data-go="${esc(b.id)}"><span>${esc((b.date || '').replace(/,.*/, ''))}</span>${esc(b.title)}</a>`).join('');
  const rs = by('realm').sort((a, b) => a.title.localeCompare(b.title));
  $('#realmlist').innerHTML = rs.map(r => `<a class="chip" data-go="${esc(r.id)}">${esc(r.title)}</a>`).join('');
  $('#counts').textContent = `${by('place').length} places · ${rs.length} realms · ${by('people').length} peoples · ${bs.length} battles · ${by('journey').length} journeys`;
}
$('#panel').addEventListener('click', e => { const g = e.target.closest('[data-go]'); if (g) { if (S.journey === g.dataset.go) stopJourney(); else select(g.dataset.go); } });
$('#panel').addEventListener('change', e => {
  const t = e.target; if (t.dataset.layer) { S.layers[t.dataset.layer] = t.checked; if (/woods|water/.test(t.dataset.layer)) redraw(); syncInk(); }
  if (t.dataset.src) { S.src[t.dataset.src] = t.checked; if (S.sel) renderCard(ITEMS[S.sel]); if (J) showStage(J.stage); }
  dirty = true;
});
$('#ex').addEventListener('input', e => { S.ex = +e.target.value; $('#exv').textContent = S.ex + '×'; dirty = true; });
const q = $('#q'), res = $('#results'); let INDEX = [];
function buildIndex() { INDEX = Object.values(ITEMS).map(it => ({ it, t: it.title.toLowerCase(), alt: Object.values(it.names || {}).join(' ').toLowerCase() })); }
const fold = s => s.toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g, '');
function search(s) {
  s = fold(s.trim()); if (!s) { res.innerHTML = ''; res.classList.remove('open'); return []; }
  const out = []; for (const e of INDEX) { const t = fold(e.t); let sc = t === s ? 0 : t.startsWith(s) ? 1 : t.includes(' ' + s) ? 2 : t.includes(s) ? 3 : fold(e.alt).includes(s) ? 5 : -1; if (sc >= 0) out.push([sc + (e.it.tier || 2) * 0.1 + (e.it.land !== LAND.id ? 0.45 : 0), e.it]); }
  out.sort((a, b) => a[0] - b[0] || a[1].title.localeCompare(b[1].title)); const top = out.slice(0, 9).map(o => o[1]);
  res.innerHTML = top.map(it => `<a data-go="${esc(it.id)}"><b>${esc(it.title)}</b><span>${esc(it.kind || TYPE_NAME[it.type])}${it.land !== LAND.id ? ' · ' + esc(D.lands.find(l => l.id === it.land).name) : ''}</span></a>`).join('') || '<p class="muted">No match.</p>'; res.classList.add('open'); return top;
}
q.addEventListener('input', () => search(q.value));
q.addEventListener('keydown', e => { if (e.key === 'Enter') { const t = search(q.value); if (t[0]) { select(t[0].id); res.classList.remove('open'); q.value = ''; q.blur(); } } if (e.key === 'Escape') { q.value = ''; search(''); q.blur(); } });
res.addEventListener('click', e => { const g = e.target.closest('[data-go]'); if (g) { select(g.dataset.go); res.classList.remove('open'); q.value = ''; } });
window.addEventListener('keydown', e => {
  if (e.target === q) return;
  if (e.key === '/') { e.preventDefault(); q.focus(); q.select(); }
  if (e.key === 'Escape') { if ($('#about').classList.contains('open')) $('#about').classList.remove('open'); else if (J) stopJourney(); else closeCard(); }
  if (e.key === ' ' && J) { e.preventDefault(); setPlaying(!J.playing); }
  if (J && e.key === 'ArrowRight') gotoStage(J.stage + 1, true); if (J && e.key === 'ArrowLeft') gotoStage(J.stage - 1, true);
});
$('#btn-about').addEventListener('click', () => $('#about').classList.add('open'));
$('#about').addEventListener('click', e => { if (e.target.id === 'about' || e.target.closest('[data-close]')) $('#about').classList.remove('open'); });
$('#btn-north').addEventListener('click', () => { const off = camera.position.clone().sub(controls.target); const sph = new THREE.Spherical().setFromVector3(off); sph.theta = 0; camera.position.setFromSpherical(sph).add(controls.target); camera.lookAt(controls.target); dirty = true; });
$('#btn-home').addEventListener('click', home);
const togglePanel = () => { document.body.classList.toggle('nopanel'); dirty = true; }; $('#btn-panel').addEventListener('click', togglePanel); $('#btn-panel2').addEventListener('click', togglePanel);
function home() { tween = null; const k = Math.max(W, H * 1.13) / 2352, cx = W * 0.489, cy = H * 0.487; controls.target.set(wx(cx), 0, wz(cy)); camera.position.set(wx(cx), 2350 * k, wz(cy) + 2050 * k); camera.lookAt(controls.target); dirty = true; }
function clearLand() {
  if (J) stopJourney(true); closeCard(); hiLines.forEach(dropLine); hiLines = [];
  for (const k of ['water', 'roads', 'realms']) { ink[k].forEach(dropLine); ink[k] = []; }
  if (mesh) { terrain.remove(mesh); mesh.geometry.dispose(); mesh.material.map.dispose(); mesh.material.dispose(); mesh = null; }
  if (slab) { scene.remove(slab); slab.geometry.dispose(); slab.material.dispose(); slab = null; }
  labels.length = 0; labelLayer.innerHTML = ''; hover = null; patWood = patSwamp = null; canvas.style.cursor = '';
}
let landBusy = null;
function setLand(id) {
  const L = D.lands.find(l => l.id === id); if (!L) return Promise.resolve();
  if (LAND && LAND.id === id) return landBusy || Promise.resolve();
  clearLand(); LAND = L; W = L.wkm; H = L.hkm; FE = L.features;
  hImg = $('#img-height-' + id); bImg = $('#img-base-' + id);
  document.querySelectorAll('#lands button').forEach(b => b.classList.toggle('act', b.dataset.land === id));
  $('#land-name').textContent = L.name; $('#land-sub').textContent = L.sub; $('#land-note').classList.toggle('hide', !L.modelled);
  landBusy = Promise.all([hImg.decode(), bImg.decode()]).then(() => {
    if (LAND !== L) return;
    decodeHeights(); buildTerrain(); redraw(); buildInk(); syncInk(); buildLabels(); buildPanel();
    controls.maxDistance = Math.max(W, H) * 1.85; home(); landBusy = null; dirty = true;
  });
  return landBusy;
}
$('#lands').addEventListener('click', e => { const b = e.target.closest('button'); if (b) setLand(b.dataset.land); });

/* ---------- loop ---------- */
let dirty = true, lastT = performance.now(), poCur = 150;
const poGoal = () => (document.body.classList.contains('nopanel') ? 0 : Math.min(306, vw * 0.25)) - (card.classList.contains('open') ? Math.min(390, vw * 0.3) : 0);
function resize() { vw = window.innerWidth; vh = window.innerHeight; renderer.setSize(vw, vh, false); camera.aspect = vw / vh; camera.setViewOffset(vw, vh, -poCur / 2, 0, vw, vh); camera.updateProjectionMatrix(); for (const m of lineMats) m.resolution.set(vw, vh); dirty = true; }
window.addEventListener('resize', resize);
controls.addEventListener('change', () => { dirty = true; });
function frame(now) {
  const dt = Math.min(0.1, (now - lastT) / 1000); lastT = now;
  stepTween(now); if (!tween) controls.update();
  const pg = poGoal(); if (Math.abs(pg - poCur) > 0.5) { poCur += (pg - poCur) * Math.min(1, dt * 5); camera.setViewOffset(vw, vh, -poCur / 2, 0, vw, vh); camera.updateProjectionMatrix(); dirty = true; }
  const nEX = exFor(camera.position.distanceTo(controls.target)); if (Math.abs(nEX - EX) > 0.005) { EX = nEX; terrain.scale.y = EX; dirty = true; }
  const t = controls.target; t.x = clamp(t.x, -W / 2, W / 2); t.z = clamp(t.z, -H / 2, H / 2);
  const gy = hAt(t.x + W / 2, H / 2 - t.z) * EX, dy = (gy - t.y) * 0.2; if (Math.abs(dy) > 0.01) { t.y += dy; camera.position.y += dy; dirty = true; }
  const cx = camera.position.x + W / 2, cy = H / 2 - camera.position.z;
  if (cx > 0 && cx < W && cy > 0 && cy < H) { const fl = hAt(cx, cy) * EX + 6; if (camera.position.y < fl) { camera.position.y = fl; dirty = true; } }
  if (J) { stepJourney(dt); if (J && J.playing) dirty = true; }
  if (dirty) { dirty = false; const ds = 1 / (0.0075 * camera.position.distanceTo(controls.target)); for (const m of dashMats) m.dashScale = ds; camera.updateMatrixWorld(); renderer.render(scene, camera); updateLabels(); if (J) stepJourney(0); }
  requestAnimationFrame(frame);
}
async function boot() {
  resize(); buildIndex();
  $('#lands').innerHTML = D.lands.length > 1 ? D.lands.map(l => `<button data-land="${l.id}"><b>${esc(l.age)}</b>${esc(l.name)}</button>`).join('') : '';
  await setLand(D.lands.some(l => l.id === params.get('land')) ? params.get('land') : D.lands[0].id);
  $('#exv').textContent = S.ex + '×'; $('#ex').value = S.ex;
  requestAnimationFrame(t => { frame(t); document.body.classList.add('ready'); window.__ready = true; });
}
window.__api = { S, ITEMS, D, setLand, get LAND() { return LAND; }, select, flyTo, startJourney, stopJourney, setPlaying, gotoStage, home, get J() { return J; }, camera, controls, labels };
boot().catch(e => { document.body.classList.add('ready'); $('#loading').textContent = 'The map did not load: ' + e.message; console.error(e); });
