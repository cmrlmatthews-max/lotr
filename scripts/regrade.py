"""Regrade a baked parchment relief image to a muted sepia palette (one paper tone, one ink tone, faint grey sea).
Usage: python3 regrade.py <data dir>   reads base.jpg + height.png, writes base_sepia.jpg"""
import sys, numpy as np
from PIL import Image
from scipy import ndimage as ndi
Image.MAX_IMAGE_PIXELS = None
PAPER = np.array([203, 188, 153], np.float32)   # land paper
LIGHT = np.array([224, 211, 180], np.float32)   # lit slopes
INK   = np.array([58, 45, 27], np.float32)      # deepest shade
SEA   = np.array([190, 181, 154], np.float32)   # faint grey tint on the sea
def main(d):
    b = np.asarray(Image.open(d + '/base.jpg').convert('RGB')).astype(np.float32)
    h = Image.open(d + '/height.png').convert('RGB')
    m = np.asarray(h.getchannel('B').resize((b.shape[1], b.shape[0]), Image.BICUBIC)).astype(np.float32) / 255
    m = np.clip((ndi.gaussian_filter(m, 1.5) - 0.3) / 0.4, 0, 1)                      # 1 = land
    L = b @ np.array([0.299, 0.587, 0.114], np.float32)
    ref_l = np.median(L[m > 0.99][::37]); ref_s = np.median(L[m < 0.01][::37]) if (m < 0.01).any() else ref_l
    t = L / (ref_s + (ref_l - ref_s) * m)                                            # 1 = plain paper
    paper = SEA + (PAPER - SEA) * m[..., None]
    dark = np.clip(t, 0, 1)[..., None] ** 1.25; lit = np.clip((t - 1) / 0.09, 0, 1)[..., None]
    out = INK + (paper - INK) * dark; out = out + (LIGHT - PAPER) * lit * (0.35 + 0.65 * m[..., None])
    # keep a trace of the original hue so that the sheet does not look flat
    out = out * 0.93 + (b * (out.mean(-1, keepdims=True) / np.maximum(b.mean(-1, keepdims=True), 1))) * 0.07
    Image.fromarray(np.clip(out, 0, 255).astype(np.uint8)).save(d + '/base_sepia.jpg', quality=86, optimize=True)
    print(d, 'land ref', ref_l, 'sea ref', ref_s)
for d in sys.argv[1:]: main(d)
