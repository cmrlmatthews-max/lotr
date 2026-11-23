#!/usr/bin/env python3
"""Assembles the single-file explorer: for each land, data + cards + images; then the bundled script -> one HTML file."""
import json, glob, base64, os, math, subprocess, sys, re, unicodedata
from collections import Counter
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))   # repo root (was '/home/claude/me')
B = R + '/source'                                                   # esbuild project and template (was R + '/build', files in src/)
DIST = os.environ.get('LOTR_DIST', B + '/dist')                     # scratch folder for the esbuild bundle
SHEETS = {'bel': ('data-beleriand', 'source/cards-beleriand'), 'num': ('data-numenor', 'source/cards-numenor'), 'ama': ('data-aman', 'source/cards-aman')}
LANG = ['English', 'Westron', 'Sindarin', 'Quenya', 'Khuzdul', 'Rohirric', 'Other']
KIND = {'Towns': 'Settlement', 'Harbors': 'Haven', 'Fortresses': 'Stronghold', 'Doors_Gates': 'Gate', 'Buildings': 'Building', 'Bridges': 'Bridge', 'Fords': 'Ford', 'Cave_entrances': 'Cave', 'Falls': 'Waterfall', 'Graves_Tombs': 'Tomb', 'Mountains': 'Mountains', 'Mountains_of_Moria': 'Mountain', 'Hills': 'Hills', 'Forests': 'Forest', 'Swamps': 'Marsh', 'Lakes': 'Lake', 'Islands': 'Island', 'Bays': 'Bay', 'Fields': 'Field', 'Valleys': 'Valley', 'Rivers': 'River', 'Roads': 'Road', 'Walls': 'Wall'}
warn = []
PREFIX = {'me': '', 'bel': 'b:', 'num': 'n:', 'ama': 'a:'}   # id prefix of each sheet
def load(p, default):
    try: return json.load(open(p))
    except Exception as e: warn.append(f'{p[len(R):]}: {e}'); return default
def clean(c, keys): return {k: c[k] for k in keys if k in c and c[k] not in (None, '', [], {})}
def nk(t):
    t = unicodedata.normalize('NFD', t); t = ''.join(c for c in t if not unicodedata.combining(c)); return re.sub(r'\s*\(.*?\)', '', t).strip().lower()

def make_land(tag, datadir, cardsdir, meta, regions=None):
    ns = lambda i: PREFIX[tag] + i
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
        it.update(clean(b, ['title', 'date', 'year_sort', 'war', 'sides', 'outcome', 'blurb', 'book', 'film', 'series', 'sources', 'related'])); it['kind'] = b.get('kind') if tag in ('num', 'ama') and b.get('kind') else 'Battle'
        if tag in ('num', 'ama'): it['neutral'] = 1   # these events list the two parties without a victor-first order
        items[b['id']] = it
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
                lore_ref = lambda i: k == 'related' and tag in ('num', 'ama') and i.startswith(('person:', 'thing:'))
                it[k] = [(i if lore_ref(i) else ns(i)) for i in dict.fromkeys(redirect.get(j, j) for j in it[k]) if (i in items or lore_ref(i)) and i != it['id']][:6]
                if not it[k]: del it[k]
        it['land'] = tag; it['id'] = ns(it['id']); out[it['id']] = it
    feats = [{k: (ns(f[k]) if k in ('id', 'card') else f[k]) for k in ('id', 'layer', 'name', 'kind', 'geom', 'card') if f.get(k) is not None} | ({'attrs': {'Type': f['attrs']['Type']}} if f['layer'] == 'Roads' and 'Type' in f.get('attrs', {}) else {}) for f in FE if f.get('geom')]
    print(tag, Counter(i['type'] for i in out.values()), '| place cards', len(cards), '| merged', len(redirect), '| tiers', dict(Counter(i['tier'] for i in out.values() if i['type'] == 'place')))
    return out, dict(meta, id=tag, wkm=W, hkm=H, features=feats)

ART_PLACES = {'me': {'Hobbiton': 'hobbiton', 'Rivendell': 'rivendell', 'Doors of Durin': 'moria', 'Caras Galadhon': 'lorien', 'Edoras': 'edoras', "Helm's Deep": 'helmsdeep', 'Isengard': 'isengard', 'Minas Tirith': 'minastirith', 'Barad-dûr': 'baraddur', 'Mount Doom': 'mountdoom', 'Lonely Mountain': 'erebor', 'Lake-town': 'laketown'},
              'bel': {'Gondolin': 'gondolin', 'Menegroth': 'menegroth', 'Angband': 'angband', 'Havens of Sirion': 'havens'}}
# second set: these map drawings show only when the view is close
ART_PLACES2 = {'me': {'Bree': 'bree', 'Weathertop': 'weathertop', 'Argonath': 'argonath', 'Minas Morgul': 'minasmorgul', 'Black Gate': 'blackgate', 'Dol Guldur': 'dolguldur', 'Grey Havens': 'greyhavens',
                      "Elvenking's Halls": 'elvenking', 'Dale': 'dale', 'Osgiliath': 'osgiliath'},
               'bel': {'Nargothrond': 'nargothrond', 'Himring': 'himring', 'Tol Sirion': 'tolsirion', 'Amon Rûdh': 'amonrudh'}}
# card pictures for peoples and battles: (type, title) -> art key
ART_CARDS = {'me': {('people', 'Hobbits'): 'p-hobbits', ('people', 'Rohirrim (Men of Rohan)'): 'p-rohirrim', ('people', 'Men of Gondor'): 'p-gondor', ('people', "Dwarves of Durin's Folk"): 'p-dwarves',
                    ('people', 'Silvan Elves'): 'p-elves', ('people', 'Ents'): 'p-ents', ('people', 'Orcs'): 'p-orcs', ('people', 'Great Eagles'): 'p-eagles',
                    ('battle', 'Battle of the Hornburg'): 'b-hornburg', ('battle', 'Battle of the Pelennor Fields'): 'b-pelennor', ('battle', 'Battle of the Morannon'): 'b-morannon',
                    ('battle', 'Battle of Five Armies'): 'b-fivearmies', ('battle', "Ents' Destruction of Isengard"): 'b-isengard', ('battle', 'Battle of Azanulbizar'): 'b-azanulbizar',
                    ('battle', 'Battle of Dagorlad and Siege of Barad-dûr'): 'b-dagorlad', ('battle', 'Battle of Bywater'): 'b-bywater'},
             'bel': {('people', 'Noldor'): 'p-noldor', ('people', 'Sindar'): 'p-sindar', ('people', 'House of Hador'): 'p-hador', ('people', 'Dragons'): 'p-dragons',
                     ('battle', 'Dagor Bragollach (Battle of Sudden Flame)'): 'b-bragollach', ('battle', 'Nírnaeth Arnoediad (Battle of Unnumbered Tears)'): 'b-nirnaeth',
                     ('battle', 'Fall of Gondolin'): 'b-gondolinfall', ('battle', 'War of Wrath'): 'b-warofwrath'}}
LANDS = [('me', R + '/data', R + '/source/cards', {'name': 'Middle-earth', 'age': 'The Third Age', 'sub': "An explorer's map of the Third Age", 'compass': [250, 250, 62], 'sea': [['BELEGAER', 118, 900, 50, 30, -1.5708]],
          'orn': {'border': 16, 'corner': 200, 'items': [['ship', 215, 735, 105], ['serpent', 160, 1130, 150]], 'cartouche': [272, 522, 380]}}, None)]
if os.path.exists(R + '/data-beleriand/height.png'):
    rg = {r['id']: r for r in load(R + '/data-beleriand/regions.json', [])}
    LANDS.append(('bel', R + '/data-beleriand', R + '/source/cards-beleriand', {'name': 'Beleriand', 'age': 'The First Age', 'sub': 'The lost lands of the Elder Days', 'modelled': True, 'compass': [182, 225, 56], 'sea': [['BELEGAER', 62, 820, 32, 20, -1.5708]],
        'orn': {'border': 11, 'corner': 100, 'items': [['ship', 150, 640, 70], ['swanship', 470, 105, 70], ['serpent', 128, 1060, 105]], 'cartouche': [128, 400, 205]}}, rg))
# sheets made with landgen/ (Númenor, Aman): the map maker's plan.json holds the sheet settings, the art list and the link maps
PLANS = {}
for tag in ('num', 'ama'):
    dd_, cd_ = R + '/' + SHEETS[tag][0], R + '/' + SHEETS[tag][1]
    if not (os.path.exists(dd_ + '/height.png') and os.path.exists(cd_ + '/plan.json')): continue
    P = json.load(open(cd_ + '/plan.json')); PLANS[tag] = P
    rg = {r['id']: r for r in load(dd_ + '/regions.json', [])}
    LANDS.append((tag, dd_, cd_, dict(P['meta'], modelled=True), rg))
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
    for title, key in ART_PLACES2.get(tag, {}).items():
        hit = [i for i in it.values() if i['type'] == 'place' and i['title'] == title]
        if not hit: warn.append(f'{tag}: no place titled {title!r} for art'); continue
        if key in art: hit[0]['art'] = key; hit[0]['artNear'] = 1
    for (typ, title), key in ART_CARDS.get(tag, {}).items():
        hit = [i for i in it.values() if i['type'] == typ and i['title'] == title]
        if not hit: warn.append(f'{tag}: no {typ} titled {title!r} for art'); continue
        if key in art: hit[0]['art'] = key
    for a in PLANS.get(tag, {}).get('art', []):
        t = it.get(PREFIX[tag] + a['for']); key = a.get('artkey')
        if not t: warn.append(f"{tag}: art target {a['for']!r} does not exist"); continue
        if key in art: t['art'] = key; t.update({'artNear': 1} if a.get('near') else {})
    images += f'<img id="img-height-{tag}" class="hide" alt="" src="data:image/png;base64,{b64(dd + "/height.png")}">\n<img id="img-base-{tag}" class="hide" alt="" src="data:image/jpeg;base64,{b64(dd + "/base_sepia.jpg")}">\n'
# ---- expansion: new places, persons, things (cards in new/cards) ----
NEW = R + '/source/cards-lore'
def _load(pat):
    out = []
    for f in sorted(glob.glob(NEW + '/' + pat)):
        d = json.load(open(f)); out += d if isinstance(d, list) else next(iter(d.values()))
    return out
land_ids = {l['id'] for l in lands}
PLACE_KEYS = ('id', 'title', 'kind', 'tier', 'blurb', 'book', 'film', 'series', 'facts', 'related', 'sources', 'confidence', 'layer', 'x', 'y', 'land', 'names')
nplaces = 0
for c in _load('newplaces_*.json'):
    if c.get('land') not in land_ids: continue
    if c['id'] in items: warn.append(f"new place id clash {c['id']}"); continue
    it = {k: c[k] for k in PLACE_KEYS if c.get(k) not in (None, '', [], {})}; it['type'] = 'place'; it['approx'] = 1; it.setdefault('tier', 3); it.setdefault('confidence', 'medium')
    items[c['id']] = it; nplaces += 1
for it in items.values():
    if it.get('related'): it['related'] = [r for r in it['related'] if r in items or r.startswith(('person:', 'thing:'))]
OFFMAP = {}; XLINKS = {}; LORELINKS = {}
for tag, P in PLANS.items():
    for name, i in (P.get('offmap_map') or {}).items():
        if PREFIX[tag] + i in items: OFFMAP.setdefault(name, PREFIX[tag] + i)
        else: warn.append(f'{tag}: offmap_map target {i!r} does not exist')
    for k, v in (P.get('lore_links') or {}).items(): LORELINKS.setdefault(k, []).extend(PREFIX[tag] + i for i in v)
    lf = R + '/' + SHEETS[tag][1] + '/links.json'
    if os.path.exists(lf):
        for k, v in json.load(open(lf)).items(): XLINKS.setdefault(k, []).extend(dict(p, id=PREFIX[tag] + p['id']) for p in v)
LORE_KEYS = ('id', 'title', 'kind', 'group', 'aka', 'blurb', 'book', 'film', 'series', 'facts', 'sources', 'confidence')
lore = []
for typ, pat in (('person', 'people_*.json'), ('thing', 'things_*.json')):
    for c in _load(pat):
        if c['id'] in items: warn.append(f"lore id clash {c['id']}"); continue
        it = {k: c[k] for k in LORE_KEYS if c.get(k) not in (None, '', [], {})}; it['type'] = typ; it['land'] = None
        pl = []
        for p in c.get('places') or []:
            t = items.get(p.get('id'))
            if not t or t['type'] not in ('place', 'realm', 'battle'): warn.append(f"{c['id']}: unknown place ref {p.get('id')!r}"); continue
            pl.append({k: p[k] for k in ('id', 'role', 'note') if p.get(k)})
        off = []
        for p in XLINKS.get(c['id'], []):          # links to exact places on the new sheets
            if p['id'] in items and not any(q['id'] == p['id'] for q in pl): pl.append({k: p[k] for k in ('id', 'role', 'note') if p.get(k)})
        for p in c.get('offmap') or []:            # a place that was off the map and now has a sheet becomes a map link
            if not p.get('name'): continue
            t = OFFMAP.get(p['name'])
            if not t: off.append({k: p[k] for k in ('name', 'role', 'note') if p.get(k)})
            elif not any(q['id'] == t for q in pl): pl.append({'id': t, 'role': p.get('role', 'other'), **({'note': p['note']} if p.get('note') else {})})
        if pl: it['places'] = pl
        if off: it['offmap'] = off
        it['_rel'] = c.get('related') or []
        if typ == 'thing' and 't-' + c['id'].split(':', 1)[1] in art: it['art'] = 't-' + c['id'].split(':', 1)[1]
        items[c['id']] = it; lore.append(it)
for it in lore:
    rel = [r for r in it.pop('_rel') if r in items and r != it['id']]
    if rel: it['related'] = rel
    for p in it.get('places', []):
        L = items[p['id']].setdefault('linked', [])
        if it['id'] not in L: L.append(it['id'])
# ---- knowledge entries (new/know): chapters, timelines, ideas, lands off the map, lists, screen versions, questions ----
KNOW = ['hob', 'fotr', 'tt', 'rotk', 'silm', 'ut', 'time_a', 'time_b', 'idea_a', 'idea_b', 'land', 'line', 'screen', 'faq']
ORDERED = {'The Hobbit', 'The Fellowship of the Ring', 'The Two Towers', 'The Return of the King', 'The Silmarillion', 'Timeline'}
know = []
for n in KNOW:
    f = R + '/source/knowledge/lore_' + n + '.json'
    if not os.path.exists(f): warn.append('no knowledge file ' + f); continue
    for c in json.load(open(f)):
        if c['id'] in items: warn.append(f"knowledge id clash {c['id']}"); continue
        it = {k: c[k] for k in LORE_KEYS if c.get(k) not in (None, '', [], {})}; it['type'] = 'lore'; it['land'] = None; it['ord'] = len(know)
        pl = []
        for p in c.get('places') or []:
            t = items.get(p.get('id'))
            if not t or t['type'] not in ('place', 'realm', 'battle'): warn.append(f"{c['id']}: unknown place ref {p.get('id')!r}"); continue
            if any(q['id'] == p['id'] for q in pl): continue
            pl.append({k: p[k] for k in ('id', 'role', 'note') if p.get(k)})
        for i in LORELINKS.get(c['id'], []):
            if i in items and not any(q['id'] == i for q in pl): pl.append({'id': i, 'role': 'other'})
        if pl: it['places'] = pl
        it['_rel'] = c.get('related') or []
        items[c['id']] = it; know.append(it)
for a, b in zip(know, know[1:]):
    if a['group'] == b['group'] and a['group'] in ORDERED: a['next'] = b['id']; b['prev'] = a['id']
for it in know:
    rel = [r for r in dict.fromkeys(it.pop('_rel')) if r in items and r != it['id']]
    if rel: it['related'] = rel
    for p in it.get('places', []):
        L = items[p['id']].setdefault('lorelinks', [])
        if it['id'] not in L: L.append(it['id'])
print('knowledge entries', len(know), dict(Counter(i['group'] for i in know)), '| places with lore links', sum(1 for i in items.values() if i.get('lorelinks')))
for it in items.values():   # place and battle cards may point to persons and things; drop refs that do not exist
    if it.get('related'): it['related'] = [r for r in it['related'] if r in items]
print('expansion: new places', nplaces, '| persons', sum(1 for i in lore if i['type'] == 'person'), '| things', sum(1 for i in lore if i['type'] == 'thing'), '| places with links', sum(1 for i in items.values() if i.get('linked')))
data = {'lands': lands, 'items': items, 'art': art}
print('art', {k: sorted(v) for k, v in art.items()})
subprocess.run(['npx', 'esbuild', 'app.js', '--bundle', '--minify', '--format=iife', '--target=es2020', '--outfile=' + DIST + '/app.js', '--log-level=warning'], cwd=B, check=True)
app = open(DIST + '/app.js').read().replace('</script', '<\\/script')
html = open(B + '/template.html').read()
dj = json.dumps(data, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/')
out = html.replace('__IMAGES__', images).replace('__DATA__', dj).replace('__APP__', app)
dest = sys.argv[1] if len(sys.argv) > 1 else DIST + '/Middle-earth Explorer.html'
open(dest, 'w').write(out)
print('html MB', round(len(out.encode()) / 1e6, 2))
for w in warn: print('WARN', w)
