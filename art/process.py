"""Prepares the Gemini images for the map.
vignettes  -> out/<key>_card.jpg (flat white ground, for 'multiply' on the card) and out/<key>_sprite.png (sepia ink with transparency)
ornaments  -> out/orn_<key>.png (sepia ink with transparency)
textures   -> out/tex_<key>.jpg"""
import sys, glob, os, numpy as np
from PIL import Image
from scipy import ndimage as ndi
INK = np.array([54, 39, 25], np.float32)
def flat(path, n=1024):
    im = Image.open(path).convert('RGB'); im = im.resize((n, n), Image.LANCZOS) if im.size != (n, n) else im
    a = np.asarray(im, np.float32) / 255
    bg = np.stack([ndi.gaussian_filter(ndi.maximum_filter(a[..., c], size=45), 38) for c in range(3)], -1)   # the paper without the drawing
    return np.clip(a / np.maximum(bg, 1e-3), 0, 1)
def ink_alpha(ff, gain=2.4, floor=0.06):
    L = ff @ np.array([0.299, 0.587, 0.114], np.float32); return np.clip((1 - L - floor) * gain, 0, 1)
def bbox(al, pad=0.04, square=True):
    ys, xs = np.nonzero(ndi.binary_opening(al > 0.2, iterations=2)); n = al.shape[0]
    if len(xs) == 0: return 0, 0, n, n
    x0, x1, y0, y1 = xs.min(), xs.max(), ys.min(), ys.max(); p = int(n * pad)
    if square:
        s = max(x1 - x0, y1 - y0) + 2 * p; cx, cy = (x0 + x1) // 2, (y0 + y1) // 2; x0, y0 = cx - s // 2, cy - s // 2; x1, y1 = x0 + s, y0 + s
    else: x0, y0, x1, y1 = x0 - p, y0 - p, x1 + p, y1 + p
    return max(0, x0), max(0, y0), min(n, x1), min(n, y1)
def rgba(al, size):
    out = np.dstack([np.broadcast_to(INK, al.shape + (3,)), al[..., None] * 255]).astype(np.uint8)
    im = Image.fromarray(out, 'RGBA'); w, h = im.size; k = size / max(w, h); return im.resize((max(1, round(w * k)), max(1, round(h * k))), Image.LANCZOS)
def vignette(path, key):
    ff = flat(path); al = ink_alpha(ff); x0, y0, x1, y1 = bbox(al)
    # fade the picture to white at the edge of the crop so no rectangle shows on the card
    crop = ff[y0:y1, x0:x1]; h, w = crop.shape[:2]; yy, xx = np.mgrid[0:h, 0:w]; e = np.minimum(np.minimum(xx, w - 1 - xx) / w, np.minimum(yy, h - 1 - yy) / h); f = np.clip(e / 0.05, 0, 1)[..., None]
    Image.fromarray(((crop * f + (1 - f)) * 255).astype(np.uint8)).resize((600, round(600 * h / w)), Image.LANCZOS).save(f'out/{key}_card.jpg', quality=80, optimize=True)
    if key[:2] in ('p-', 'b-'): return   # peoples and battles: card picture only
    # map drawing: tonal sepia ink on a soft cream ground, so that it stays readable on dark relief
    L = crop @ np.array([0.299, 0.587, 0.114], np.float32); ia = np.clip((1 - L - 0.04) * 1.6, 0, 1) ** 0.9 * f[..., 0]
    m = ndi.gaussian_filter(ndi.binary_closing(al[y0:y1, x0:x1] > 0.12, iterations=6).astype(np.float32), 14); ha = np.clip(m * 1.5 - 0.15, 0, 1) * 0.8 * f[..., 0]
    a = ia + ha * (1 - ia); cream = np.array([238, 224, 190], np.float32)
    rgb = (INK * ia[..., None] + cream * (ha * (1 - ia))[..., None]) / np.maximum(a, 1e-3)[..., None]
    im = Image.fromarray(np.dstack([rgb, a[..., None] * 255]).astype(np.uint8), 'RGBA'); im.resize((256, round(256 * h / w)), Image.LANCZOS).quantize(colors=128, method=Image.FASTOCTREE).save(f'out/{key}_sprite.png', optimize=True)
def ornament(path, key, size):
    ff = flat(path); al = ink_alpha(ff, 2.8, 0.07); x0, y0, x1, y1 = bbox(al, 0.015, False); rgba(al[y0:y1, x0:x1], size).save(f'out/orn_{key}.png', optimize=True)
def texture(path, key, size):
    Image.open(path).convert('RGB').resize((size, size), Image.LANCZOS).save(f'out/tex_{key}.jpg', quality=72, optimize=True)
ORN = {'compass': 420, 'ship': 300, 'serpent': 340, 'cartouche': 760, 'corner': 320, 'swanship': 300}
for p in sorted(glob.glob('raw/*.jpeg') + glob.glob('raw/*.png')):
    key = os.path.splitext(os.path.basename(p))[0]
    if key.endswith('_sepia'): continue
    if key in ORN: ornament(p, key, ORN[key])
    elif key.startswith('tex_'): texture(p, key[4:], 1024)
    else: vignette(p, key)
print({f: os.path.getsize('out/' + f) for f in sorted(os.listdir('out'))})
