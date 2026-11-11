#!/usr/bin/env python3
"""Assembles the single-file explorer: for each land, data + cards + images; then the bundled script -> one HTML file."""
import json, glob, base64, os, math, subprocess, sys, re, unicodedata
from collections import Counter
R = '/home/claude/me'; B = R + '/build'
LANG = ['English', 'Westron', 'Sindarin', 'Quenya', 'Khuzdul', 'Rohirric', 'Other']
KIND = {'Towns': 'Settlement', 'Harbors': 'Haven', 'Fortresses': 'Stronghold', 'Doors_Gates': 'Gate', 'Buildings': 'Building', 'Bridges': 'Bridge', 'Fords': 'Ford', 'Cave_entrances': 'Cave', 'Falls': 'Waterfall', 'Graves_Tombs': 'Tomb', 'Mountains': 'Mountains', 'Mountains_of_Moria': 'Mountain', 'Hills': 'Hills', 'Forests': 'Forest', 'Swamps': 'Marsh', 'Lakes': 'Lake', 'Islands': 'Island', 'Bays': 'Bay', 'Fields': 'Field', 'Valleys': 'Valley', 'Rivers': 'River', 'Roads': 'Road', 'Walls': 'Wall'}
warn = []
def load(p, default):
    try: return json.load(open(p))
    except Exception as e: warn.append(f'{p[len(R):]}: {e}'); return default
def clean(c, keys): return {k: c[k] for k in keys if k in c and c[k] not in (None, '', [], {})}
def nk(t):
    t = unicodedata.normalize('NFD', t); t = ''.join(c for c in t if not unicodedata.combining(c)); return re.sub(r'\s*\(.*?\)', '', t).strip().lower()

def make_land(tag, datadir, cardsdir, meta, regions=None):
    ns = (lambda i: i) if tag == 'me' else (lambda i: 'b:' + i)
    vec = load(datadir + '/vectors.json', {}); W, H = vec['wkm'], vec['hkm']; FE = vec['features']
    feat = {f['id']: f for f in FE}; regions = regions or {}
    def at(a):
        g = feat.get((a or {}).get('near')) or regions.get((a or {}).get('near'))
        if not g: return None
        return round(min(W - 4, max(4, g['x'] + float(a.get('dx') or 0))), 1), round(min(H - 4, max(4, g['y'] + float(a.get('dy') or 0))), 1)
    items = {}; cards = {}
    for p in sorted(glob.glob(cardsdir + '/places_*.json')):
        for c in load(p, []):
            if isinstance(c, dict) and c.get('id') in feat: cards[c['id']] = c
    for f in FE:
        if f.get('card') != f['id']: continue
        c = cards.get(f['id'], {}); title = c.get('title') or f['name']
        names = {k: f['attrs'][k].replace('"', '') for k in LANG if k in f.get('attrs', {}) and f['attrs'][k].strip().lower() != title.lower()}
        names.update({k: v for k, v in (c.get('names') or {}).items() if v})
        it = {'id': f['id'], 'type': 'place', 'layer': f['layer'], 'x': f['x'], 'y': f['y'], 'title': title, 'kind': c.get('kind') or KIND.get(f['layer'], 'Place'),
              'tier': c.get('tier') if c.get('tier') in (1, 2, 3) else 3, 'confidence': c.get('confidence', 'low' if not c else 'medium'), 'names': names}
        if 'area' in f: it['area'] = f['area']
        it.update(clean(c, ['blurb', 'book', 'film', 'series', 'facts', 'sources']))
        if not c: it['book'] = 'No card text is available for this place yet.'
        it['related'] = c.get('related') or []; items[f['id']] = it
    # one card for places that share a name and lie close together
    groups = {}; redirect = {}
    for it in items.values(): groups.setdefault(nk(it['title']), []).append(it)
    for g in groups.values():
        g.sort(key=lambda it: (it['tier'], -len(it.get('book', '')))); keep = []
        for it in g:
            hit = next((h for h in keep if math.hypot(h['x'] - it['x'], h['y'] - it['y']) < 60), None)
            if hit: redirect[it['id']] = hit['id']
            else: keep.append(it)
    for k in redirect: del items[k]
    for f in FE:
        if f.get('card') in redirect: f['card'] = redirect[f['card']]
    rp = load(cardsdir + '/realms.json', {})
    for r in rp.get('realms', []):
        rg = regions.get(r.get('id')); xy = (rg['x'], rg['y']) if rg else at(r.get('center'))
        if not xy: warn.append(f'{tag}: realm without centre: ' + str(r.get('id'))); continue
        it = {'id': r['id'], 'type': 'realm', 'rtype': (rg or r).get('type', 'realm'), 'x': xy[0], 'y': xy[1], 'radius': (rg or r).get('radius_km', 200), 'tier': (rg or r).get('tier', 2), 'confidence': r.get('confidence', 'medium')}
        it.update(clean(r, ['title', 'kind', 'status', 'blurb', 'book', 'film', 'series', 'facts', 'sources', 'peoples', 'related', 'names'])); items[r['id']] = it
    for p in rp.get('peoples', []):
        it = {'id': p['id'], 'type': 'people', 'confidence': p.get('confidence', 'medium')}
        it.update(clean(p, ['title', 'kind', 'blurb', 'book', 'film', 'series', 'facts', 'sources', 'realms', 'related'])); items[p['id']] = it
    # a realm card that repeats a mapped place gives way to the place card
    pk = {}
    for it in items.values():
        if it['type'] == 'place': pk.setdefault(nk(it['title']), []).append(it)
    for it in [i for i in items.values() if i['type'] == 'realm']:
        for h in pk.get(nk(it['title']), []):
            if math.hypot(h['x'] - it['x'], h['y'] - it['y']) < 90: redirect[it['id']] = h['id']; del items[it['id']]; break
    for b in load(cardsdir + '/battles.json', []):
        xy = at(b.get('at'))
        if not xy: warn.append(f'{tag}: battle without site: ' + str(b.get('id'))); continue
        it = {'id': b['id'], 'type': 'battle', 'x': xy[0], 'y': xy[1], 'tier': b.get('tier', 2), 'confidence': b.get('confidence', 'medium')}
        it.update(clean(b, ['title', 'date', 'year_sort', 'war', 'sides', 'outcome', 'blurb', 'book', 'film', 'series', 'sources', 'related'])); it['kind'] = 'Battle'; items[b['id']] = it
    def frodo_path():
        f = feat.get('FRX00')
        if not f: return None
        parts = [[(p[i], p[i + 1]) for i in range(0, len(p), 2)] for p in f['geom']]
        hob = (feat['TO050']['x'], feat['TO050']['y']); d = lambda a, b: math.hypot(a[0] - b[0], a[1] - b[1])
        parts.sort(key=lambda p: min(d(p[0], hob), d(p[-1], hob))); cur = parts.pop(0)
        if d(cur[-1], hob) < d(cur[0], hob): cur.reverse()
        while parts:
            j = min(range(len(parts)), key=lambda k: min(d(parts[k][0], cur[-1]), d(parts[k][-1], cur[-1]))); p = parts.pop(j)
            if d(p[-1], cur[-1]) < d(p[0], cur[-1]): p.reverse()
            cur += p
        return [[round(x, 1), round(y, 1)] for x, y in cur]
    for j in load(cardsdir + '/journeys.json', []):
        st = []
        for s in j.get('stages', []):
            xy = at(s.get('at'))
            if xy: st.append({'x': xy[0], 'y': xy[1], **clean(s, ['title', 'date', 'note', 'film'])})
        if len(st) < 2: warn.append(f'{tag}: journey without stages: ' + str(j.get('id'))); continue
        it = {'id': j['id'], 'type': 'journey', 'stages': st, 'kind': 'Journey', 'confidence': j.get('confidence', 'medium')}
        it.update(clean(j, ['title', 'travellers', 'source', 'dates', 'blurb', 'book', 'film', 'sources']))
        if j['id'] == 'journey:frodo':
            fp = frodo_path()
            if fp: it['path'] = fp
        items[j['id']] = it
    out = {}
    for it in items.values():
        for k in ('related', 'peoples', 'realms'):
            if k in it:
                it[k] = [ns(i) for i in dict.fromkeys(redirect.get(j, j) for j in it[k]) if i in items and i != it['id']][:6]
                if not it[k]: del it[k]
        it['land'] = tag; it['id'] = ns(it['id']); out[it['id']] = it
    feats = [{k: (ns(f[k]) if k in ('id', 'card') else f[k]) for k in ('id', 'layer', 'name', 'kind', 'geom', 'card') if f.get(k) is not None} | ({'attrs': {'Type': f['attrs']['Type']}} if f['layer'] == 'Roads' and 'Type' in f.get('attrs', {}) else {}) for f in FE if f.get('geom')]
    print(tag, Counter(i['type'] for i in out.values()), '| place cards', len(cards), '| merged', len(redirect), '| tiers', dict(Counter(i['tier'] for i in out.values() if i['type'] == 'place')))
    return out, dict(meta, id=tag, wkm=W, hkm=H, features=feats)

ART_PLACES = {'me': {'Hobbiton': 'hobbiton', 'Rivendell': 'rivendell', 'Doors of Durin': 'moria', 'Caras Galadhon': 'lorien', 'Edoras': 'edoras', "Helm's Deep": 'helmsdeep', 'Isengard': 'isengard', 'Minas Tirith': 'minastirith', 'Barad-dûr': 'baraddur', 'Mount Doom': 'mountdoom', 'Lonely Mountain': 'erebor', 'Lake-town': 'laketown'},
              'bel': {'Gondolin': 'gondolin', 'Menegroth': 'menegroth', 'Angband': 'angband', 'Havens of Sirion': 'havens'}}
LANDS = [('me', R + '/data', R + '/cards', {'name': 'Middle-earth', 'age': 'The Third Age', 'sub': "An explorer's map of the Third Age", 'compass': [250, 250, 62], 'sea': [['BELEGAER', 118, 900, 50, 30, -1.5708]],
          'orn': {'border': 16, 'corner': 200, 'items': [['ship', 215, 735, 105], ['serpent', 160, 1130, 150]], 'cartouche': [272, 522, 380]}}, None)]
if os.path.exists(R + '/bel/data/height.png'):
    rg = {r['id']: r for r in load(R + '/bel/slices/regions.json', [])}
    LANDS.append(('bel', R + '/bel/data', R + '/bel/cards', {'name': 'Beleriand', 'age': 'The First Age', 'sub': 'The lost lands of the Elder Days', 'modelled': True, 'compass': [182, 225, 56], 'sea': [['BELEGAER', 62, 820, 32, 20, -1.5708]],
        'orn': {'border': 11, 'corner': 100, 'items': [['ship', 150, 640, 70], ['swanship', 470, 105, 70], ['serpent', 128, 1060, 105]], 'cartouche': [128, 400, 205]}}, rg))
art = {}
mime = {'jpg': 'image/jpeg', 'png': 'image/png'}
for f in sorted(glob.glob(R + '/art/out/*')):
    n, ext = os.path.basename(f).rsplit('.', 1); uri = f'data:{mime[ext]};base64,' + base64.b64encode(open(f, 'rb').read()).decode()
    if n.startswith('orn_'): art.setdefault(n[4:], {})['orn'] = uri
    elif n.startswith('tex_'): art.setdefault(n[4:], {})['tex'] = uri
    else: k, kind = n.rsplit('_', 1); art.setdefault(k, {})[kind] = uri
only = os.environ.get('LANDS')
items = {}; lands = []; images = ''
b64 = lambda p: base64.b64encode(open(p, 'rb').read()).decode()
for tag, dd, cd, meta, rg in LANDS:
    if only and tag not in only.split(','): continue
    it, land = make_land(tag, dd, cd, meta, rg); items.update(it); lands.append(land)
    for title, key in ART_PLACES.get(tag, {}).items():
        hit = [i for i in it.values() if i['type'] == 'place' and i['title'] == title]
        if not hit: warn.append(f'{tag}: no place titled {title!r} for art'); continue
        if key in art: hit[0]['art'] = key
    images += f'<img id="img-height-{tag}" class="hide" alt="" src="data:image/png;base64,{b64(dd + "/height.png")}">\n<img id="img-base-{tag}" class="hide" alt="" src="data:image/jpeg;base64,{b64(dd + "/base_sepia.jpg")}">\n'
data = {'lands': lands, 'items': items, 'art': art}
print('art', {k: sorted(v) for k, v in art.items()})
subprocess.run(['npx', 'esbuild', 'src/app.js', '--bundle', '--minify', '--format=iife', '--target=es2020', '--outfile=dist/app.js', '--log-level=warning'], cwd=B, check=True)
app = open(B + '/dist/app.js').read().replace('</script', '<\\/script')
html = open(B + '/src/template.html').read()
dj = json.dumps(data, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/')
out = html.replace('__IMAGES__', images).replace('__DATA__', dj).replace('__APP__', app)
dest = sys.argv[1] if len(sys.argv) > 1 else B + '/dist/Middle-earth Explorer.html'
open(dest, 'w').write(out)
print('html MB', round(len(out.encode()) / 1e6, 2))
for w in warn: print('WARN', w)
