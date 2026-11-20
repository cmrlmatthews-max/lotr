"""Makes vectors.json, the gazetteer, the index and the writer slices for one map sheet. Usage: python3 make_vectors.py <land dir>"""
import json, math, sys, os
D = os.path.abspath(sys.argv[1]); sys.path.insert(0, D); sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); os.chdir(D); os.makedirs("data", exist_ok=True); os.makedirs("slices", exist_ok=True); os.makedirs("cards", exist_ok=True)
import geo
from shape import *
CLOSED = getattr(geo, "CLOSED_RIDGES", {"MT08"})
flat = lambda p: [round(v, 1) for xy in p for v in xy]
F = []; gaz = []; G = {}
def add(id, layer, name, kind, geom, x, y, hint='', card='self', attrs=None, **kw):
    c = id if (card == 'self' and name) else (None if card == 'self' else card)
    f = {'id': id, 'layer': layer, 'name': name or '', 'kind': kind, 'geom': [flat(g) for g in geom] if geom else None, 'x': round(x, 1), 'y': round(y, 1), 'card': c, 'attrs': attrs or {}} | kw
    F.append(f)
    if c == id: gaz.append({'id': id, 'layer': layer, 'name': name, 'x': f['x'], 'y': f['y'], 'attrs': {'Hint': hint}})
parent = lambda i: i[:-1] if i.endswith('b') else None
for id, name, layer, lp, pts, h, w, hint in geo.RIDGES:
    L = length(pts); line = chaikin(wobble(resample(pts, 18), w * 0.18, id), id in CLOSED, 2) if L > 12 else None
    c = centroid(pts); x, y = lp or c
    add(id, layer, name, 'line' if line else 'pt', [line] if line else None, x, y, hint, card=parent(id) or 'self')
RIV = {}
for id, name, lp, pts, hint in geo.RIVERS:
    line = chaikin(meander(pts, 2.2, 6, id), False, 2); RIV[id] = line; x, y = lp or pts[len(pts) // 2]
    add(id, 'Rivers', name, 'line', [line], x, y, hint, card=parent(id) or 'self')
for id, name, poly, hint in geo.LAKES:
    p = chaikin(wobble(poly, 1.0, id), True, 1); c = centroid(poly); add(id, 'Lakes', name, 'poly', [p], c[0], c[1], hint, area=round(area(p), 1))
for id, name, poly, hint in geo.FORESTS:
    p = chaikin(wobble(resample(poly + [poly[0]], 14)[:-1], 3.0, id), True, 2); c = centroid(poly); add(id, 'Forests', name, 'poly', [p], c[0], c[1], hint, area=round(area(p), 1))
for id, name, poly, hint in geo.SWAMPS:
    p = chaikin(wobble(resample(poly + [poly[0]], 9)[:-1], 2.0, id), True, 2); c = centroid(poly); add(id, 'Swamps', name, 'poly', [p], c[0], c[1], hint, area=round(area(p), 1))
for id, name, lp, pts, typ, hint in geo.ROADS:
    line = chaikin(meander(pts, 1.2, 10, id), False, 2); x, y = lp or pts[len(pts) // 2]
    add(id, 'Roads', name, 'line', [line], x, y, hint, card=parent(id) or 'self', attrs={'Type': 'Major road'})
for bid, bname, bpoly in getattr(geo, 'BORDERS', []):
    g = chaikin(wobble(resample(bpoly + [bpoly[0]], 16)[:-1], 2.0, bid), True, 2); c = centroid(bpoly); add(bid, 'Realms', bname, 'poly', [g], c[0], c[1], card=None)
for id, name, layer, x, y, hint in geo.POINTS: add(id, layer, name, 'pt', None, x, y, hint)
ids = [f['id'] for f in F]; assert len(ids) == len(set(ids))
json.dump({'wkm': geo.W, 'hkm': geo.H, 'features': F}, open('data/vectors.json', 'w'), ensure_ascii=False, separators=(',', ':'))
json.dump({k: [list(p) for p in v] for k, v in RIV.items()}, open('data/rivers_smooth.json', 'w'))
with open('data/gaz_index.tsv', 'w') as o:
    o.write('id\tname\tlayer\tx_km_east\ty_km_north\thint\n')
    for a in gaz: o.write(f"{a['id']}\t{a['name']}\t{a['layer']}\t{a['x']}\t{a['y']}\t{a['attrs']['Hint']}\n")
    for id, name, typ, tier, x, y, r in geo.REGIONS: o.write(f"{id}\t{name}\tRegion ({typ})\t{x}\t{y}\tradius about {r} km. {geo.REGION_HINTS.get(id, '')}\n")
json.dump(gaz, open('data/gazetteer.json', 'w'), ensure_ascii=False, indent=0)
pt = [a for a in gaz if a['layer'] not in ('Mountains', 'Hills', 'Lakes', 'Forests', 'Swamps', 'Rivers', 'Roads')]
land = [a for a in gaz if a['layer'] in ('Mountains', 'Hills', 'Lakes', 'Forests', 'Swamps')]; riv = [a for a in gaz if a['layer'] in ('Rivers', 'Roads')]
allc = pt + land + riv; NS = max(1, round(len(allc) / 20)); per = math.ceil(len(allc) / NS)
for i in range(NS): json.dump(allc[i * per:(i + 1) * per], open(f'slices/slice_{i + 1:02d}.json', 'w'), ensure_ascii=False, indent=1); print('slice', i + 1, len(allc[i * per:(i + 1) * per]))
json.dump([dict(zip(('id', 'title', 'type', 'tier', 'x', 'y', 'radius_km'), r)) | {'hint': geo.REGION_HINTS.get(r[0], '')} for r in geo.REGIONS], open('slices/regions.json', 'w'), ensure_ascii=False, indent=1)
print('features', len(F), 'cards', len(gaz), 'regions', len(geo.REGIONS))
