"""Draws the control geometry with names on top of data/preview.jpg -> data/preview_labels.jpg, so that the map maker can check positions.
Usage: python3 preview.py <land dir>"""
import json, sys, os
from PIL import Image, ImageDraw, ImageFont
D = os.path.abspath(sys.argv[1]); sys.path.insert(0, D); os.chdir(D)
import geo
im = Image.open('data/preview.jpg').convert('RGB'); k = 1600 / im.width; im = im.resize((1600, int(im.height * k)), Image.LANCZOS); d = ImageDraw.Draw(im)
sc = im.width / geo.W; P = lambda x, y: (x * sc, (geo.H - y) * sc)
try: f = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 13); fb = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 15)
except Exception: f = fb = ImageFont.load_default()
V = json.load(open('data/vectors.json'))['features']
col = {'Rivers': (40, 90, 200), 'Roads': (150, 60, 20), 'Forests': (30, 120, 40), 'Swamps': (90, 120, 110), 'Lakes': (40, 90, 200), 'Mountains': (110, 60, 60), 'Hills': (140, 100, 70), 'Realms': (120, 30, 120)}
for ft in V:
    for g in ft.get('geom') or []:
        pts = [P(g[i], g[i + 1]) for i in range(0, len(g), 2)]
        if ft['kind'] == 'poly': pts.append(pts[0])
        d.line(pts, fill=col.get(ft['layer'], (0, 0, 0)), width=2)
for ft in V:
    if not ft['name']: continue
    x, y = P(ft['x'], ft['y'])
    if ft['kind'] == 'pt': d.ellipse((x - 4, y - 4, x + 4, y + 4), fill=(200, 20, 20), outline=(255, 255, 255))
    d.text((x + 6, y - 7), ft['name'], fill=(0, 0, 0), font=f, stroke_width=2, stroke_fill=(255, 250, 235))
for id, name, typ, tier, x, y, r in geo.REGIONS:
    px, py = P(x, y); d.text((px, py), name.upper(), fill=(120, 30, 120), font=fb, anchor='mm', stroke_width=2, stroke_fill=(255, 250, 235))
for gx in range(0, int(geo.W) + 1, 200): d.line([P(gx, 0), P(gx, geo.H)], fill=(0, 0, 0, 60), width=1); d.text(P(gx + 3, geo.H - 2), str(gx), fill=(0, 0, 0), font=f)
for gy in range(0, int(geo.H) + 1, 200): d.line([P(0, gy), P(geo.W, gy)], fill=(0, 0, 0), width=1); d.text(P(3, gy + 16), str(gy), fill=(0, 0, 0), font=f)
im.save('data/preview_labels.jpg', quality=88); print('preview_labels.jpg', im.size)
