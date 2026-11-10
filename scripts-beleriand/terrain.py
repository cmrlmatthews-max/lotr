"""Models the Beleriand terrain from the control geometry in geo.py and bakes the parchment relief image.
Outputs: data/height.png (1.5 km grid, same encoding as the Middle-earth map), data/base.jpg (500 m), data/preview.jpg."""
import json, math, numpy as np
from PIL import Image, ImageDraw, ImageFilter
from scipy import ndimage as ndi
import geo
from shape import chaikin, wobble, resample

W, H = geo.W, geo.H
R = 0.5                                   # km per pixel, relief image
ww, hh = int(W / R), int(H / R)
sw, sh = int(W), int(H)                   # 1 km structure grid
rng = np.random.default_rng(11)

def up(a, shape, mode=Image.BICUBIC): return np.asarray(Image.fromarray(np.asarray(a, np.float32)).resize((shape[1], shape[0]), mode))
def vnoise(shape, cell): return up(rng.random((int(shape[0] / cell) + 3, int(shape[1] / cell) + 3)), shape)
def fbm(shape, cell, octs=4, gain=0.5):
    a = np.zeros(shape, np.float32); amp = 1.0; tot = 0.0
    for o in range(octs):
        if cell / 2 ** o < 2: break
        a += amp * vnoise(shape, cell / 2 ** o); tot += amp; amp *= gain
    return a / tot
def ridged(shape, cell, octs=5, gain=0.55):
    a = np.zeros(shape, np.float32); amp = 1.0; tot = 0.0
    for o in range(octs):
        if cell / 2 ** o < 2: break
        a += amp * (1 - np.abs(2 * vnoise(shape, cell / 2 ** o) - 1)) ** 2; tot += amp; amp *= gain
    return a / tot
def raster(shapes, size, scale, fill=False, width=1):
    im = Image.new('L', (size[1], size[0]), 0); d = ImageDraw.Draw(im)
    for p in shapes:
        q = [(x * scale, (H - y) * scale) for x, y in p]
        if fill: d.polygon(q, fill=255)
        elif len(q) > 1: d.line(q, fill=255, width=width)
    return np.asarray(im) > 0
def blur(a, s): return ndi.gaussian_filter(np.asarray(a, np.float32), s)

# 1. land and sea
coast = chaikin(wobble(resample(geo.COAST + [geo.COAST[0]], 22)[:-1], 5.0, 'coast'), True, 2)
m = raster([coast, geo.ISLE_BALAR], (hh, ww), 1 / R, fill=True).astype(np.float32)
# push the outline about with smooth noise so the coast has bays and headlands
yy0, xx0 = np.mgrid[0:hh, 0:ww].astype(np.float32)
wx_ = (fbm((hh, ww), 150, 2) - 0.5) * 2 * 26 + (fbm((hh, ww), 44, 3) - 0.5) * 2 * 13
wy_ = (fbm((hh, ww), 150, 2) - 0.5) * 2 * 26 + (fbm((hh, ww), 44, 3) - 0.5) * 2 * 13
mb = ndi.map_coordinates(blur(m, 2.5), [yy0 + wy_, xx0 + wx_], order=1, mode='nearest'); del yy0, xx0
n = fbm((hh, ww), 16, 3) - 0.5
land = (mb + 0.8 * n * (4 * mb * (1 - mb))) > 0.5
lab, k = ndi.label(land); sizes = ndi.sum(land, lab, range(1, k + 1)); land = np.isin(lab, [i + 1 for i, s in enumerate(sizes) if s > 400])
lab, k = ndi.label(~land); sizes = ndi.sum(~land, lab, range(1, k + 1)); land = ~np.isin(lab, [i + 1 for i, s in enumerate(sizes) if s > 3000])
dcoast = ndi.distance_transform_edt(land) * R
yy, xx = np.mgrid[0:hh, 0:ww].astype(np.float32); X = xx * R; Y = H - yy * R

# 2. base ground and raised lands
base = 25 + 150 * (1 - np.exp(-dcoast / 90)) + 70 * (fbm((hh, ww), 320, 3) - 0.5)
SIG = {'dorthonion': 7, 'tumladen': 4, 'north_of_andram': 5, 'himring': 8, 'hithlum': 9}
for name, poly, add in geo.PLATEAUS:
    base += add * up(blur(raster([poly], (sh, sw), 1.0, fill=True), SIG.get(name, 14)), (hh, ww))

# 3. mountains and hills
warp = fbm((hh, ww), 60, 4) - 0.5; crest = 0.72 + 0.56 * fbm((hh, ww), 110, 3)
M = np.zeros((hh, ww), np.float32)
for id, name, layer, lp, pts, h, w, hint in geo.RIDGES:
    closed = id == 'MT08'
    line = chaikin(wobble(resample(pts, 18), w * 0.18, id), closed, 2) if len(pts) > 2 else pts
    d = up(ndi.distance_transform_edt(~raster([line + ([line[0]] if closed else [])], (sh, sw), 1.0)), (hh, ww), Image.BILINEAR)
    d2 = np.clip(d + w * 0.9 * warp, 0, None)
    M = np.maximum(M, h * np.exp(-d2 ** 2 / (2 * (w * 0.78) ** 2)) * crest)
tex = ridged((hh, ww), 56, 5) - 0.42; fine = ridged((hh, ww), 14, 3) - 0.4
total = base + M * (1 + 0.60 * tex + 0.16 * fine) + 34 * (fbm((hh, ww), 26, 4) - 0.5) * np.clip(dcoast / 15, 0, 1)
# pine highlands and plateaus get broken ground too
total += np.clip(base - 330, 0, 500) * (0.5 * tex + 0.12 * fine)
# rolling lowlands and foothills, so the plains are not flat
inl = np.clip(dcoast / 25, 0, 1); foot = np.clip(blur((M > 250).astype(np.float32), 30) * 2.2, 0, 1)
roll = ridged((hh, ww), 90, 4) - 0.38; roll2 = ridged((hh, ww), 30, 3) - 0.4
dry = np.clip((Y - 960) / 120, 0, 1) * np.clip((X - 600) / 60, 0, 1)       # Anfauglith: a level plain
total += inl * (1 - 0.8 * dry) * ((70 + 190 * foot) * roll + (26 + 60 * foot) * roll2)

# 4. rivers cut valleys; lakes lie flat
riv = [[tuple(p) for p in v] for v in json.load(open('data/rivers_smooth.json')).values()]
dr = ndi.distance_transform_edt(~raster(riv, (hh, ww), 1 / R)) * R
total -= np.exp(-(dr / 2.6) ** 2) * (14 + 0.34 * np.clip(total - 50, 0, None)) + np.exp(-(dr / 11) ** 2) * 0.10 * np.clip(total - 90, 0, None)
for id, name, poly, hint in geo.LAKES:
    lm = raster([poly], (hh, ww), 1 / R, fill=True)
    if lm.any(): total[lm] = np.percentile(total[lm], 20)
total = np.where(land, np.clip(total, 3, 3900), 0).astype(np.float32)

# 5. the sheet stops at the east, north and south-east edges: fade the land to plain paper there
ufade = np.clip(np.maximum.reduce([(X - (W - 26)) / 24, (Y - (H - 26)) / 24, np.where(X > 860, (26 - Y) / 24, -1)]), 0, 1) * land
total *= (1 - ufade)

# 6. height map for the 3D mesh (1.5 km)
lw, lh = int(W / 1.5), int(H / 1.5)
lo = np.asarray(Image.fromarray(total).resize((lw, lh), Image.BOX)); lland = np.asarray(Image.fromarray(land.astype(np.uint8) * 255).resize((lw, lh), Image.BOX)) > 127
v = np.round(np.clip(lo, 0, 4000) / 4000 * 65535).astype(np.uint16)
Image.fromarray(np.dstack([(v >> 8).astype(np.uint8), (v & 255).astype(np.uint8), np.where(lland, 255, 0).astype(np.uint8)]), 'RGB').save('data/height.png', optimize=True)

# 7. parchment relief (same recipe as the Middle-earth sheet)
def pblur(a, r): return np.asarray(Image.fromarray((np.clip(a, 0, 1) * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(r)), np.float32) / 255
def noise(scale, amp):
    small = rng.random((max(2, hh // scale), max(2, ww // scale))).astype(np.float32)
    return (np.asarray(Image.fromarray(small).resize((ww, hh), Image.BICUBIC)) - 0.5) * amp
h = total; z = 7.0
dzdx = np.zeros_like(h); dzdy = np.zeros_like(h)
dzdx[:, 1:-1] = (h[:, 2:] - h[:, :-2]) / (2000 * R); dzdy[1:-1, :] = (h[:-2, :] - h[2:, :]) / (2000 * R)
nx = -z * dzdx; ny = -z * dzdy; nn = np.sqrt(nx * nx + ny * ny + 1)
rel = (nx * -0.5 + ny * 0.5 + 0.7071) / nn / 0.7071
slope = np.sqrt(dzdx * dzdx + dzdy * dzdy)
mult = np.clip(0.30 + 0.70 * rel, 0.42, 1.16) * (1 - 0.22 * np.clip(slope * 9, 0, 1))
t = np.clip(h / 2600, 0, 1)[..., None]
lowc = np.array([226, 213, 170], np.float32); midc = np.array([214, 192, 148], np.float32); topc = np.array([238, 229, 208], np.float32)
col = np.where(t < 0.5, lowc + (midc - lowc) * (t * 2), midc + (topc - midc) * ((t - 0.5) * 2)) * mult[..., None]
band = np.floor(h / 400); edge = np.zeros_like(land)
edge[:, 1:] |= band[:, 1:] != band[:, :-1]; edge[1:, :] |= band[1:, :] != band[:-1, :]
col = np.where((edge & land)[..., None], col * 0.90, col)
b1 = pblur(land, 8.5); b2 = pblur(land, 31)
sea = np.array([194, 204, 190], np.float32) * (1 - 0.10 * b2[..., None]) - np.array([14, 10, 6], np.float32) * b1[..., None]
q = np.floor(np.power(np.clip(b1, 0, 1), 0.6) * 7); we = np.zeros_like(land)
we[:, 1:] |= q[:, 1:] != q[:, :-1]; we[1:, :] |= q[1:, :] != q[:-1, :]
sea = np.where((we & (b1 > 0.03))[..., None], sea * 0.80, sea)
img = np.where(land[..., None], col, sea)
ce = np.zeros_like(land); ce[:, 1:] |= land[:, 1:] != land[:, :-1]; ce[1:, :] |= land[1:, :] != land[:-1, :]; ce[:, :-1] |= land[:, 1:] != land[:, :-1]
img = np.where(ce[..., None], np.array([84, 62, 40], np.float32), img)
paper = np.array([224, 210, 168], np.float32); uf = pblur(ufade, 10)[..., None]
img = img * (1 - uf) + paper * uf
img = img * (1 + noise(260, 0.10) + noise(60, 0.05))[..., None]
e = np.minimum(np.minimum(xx, ww - 1 - xx), np.minimum(yy, hh - 1 - yy)) / ww
burn = np.clip(1 - (e + noise(90, 0.012)) / 0.022, 0, 1) ** 1.5 * 0.6
img = img * (1 - burn[..., None]) + np.array([92, 66, 40], np.float32) * burn[..., None]
out = Image.fromarray(np.clip(img, 0, 255).astype(np.uint8), 'RGB')
out.save('data/base.jpg', quality=84, optimize=True, subsampling=1)
out.resize((1100, int(1100 * hh / ww)), Image.LANCZOS).save('data/preview.jpg', quality=82)
out.crop((1000, 1300, 2000, 2100)).save('data/preview_crop.jpg', quality=85)
import os
print('max m', float(total.max()), 'land frac', float(land.mean()), {f: os.path.getsize('data/' + f) for f in ('height.png', 'base.jpg')})
