"""Check card files of a new sheet.
Usage: python3 check_cards.py <sheet dir> places <NN> | realms | battles | journeys | links
Prints every problem; prints OK when there is none."""
import json, sys, csv, re, os
D = os.path.abspath(sys.argv[1]); kind = sys.argv[2]; arg = sys.argv[3] if len(sys.argv) > 3 else ''
gaz = {r['id']: r for r in csv.DictReader(open(D + '/data/gaz_index.tsv'), delimiter='\t')}
allx = {r['id'] for r in csv.DictReader(open('/home/claude/me/new/all_index.tsv'), delimiter='\t')}
plan = json.load(open(D + '/plan.json')) if os.path.exists(D + '/plan.json') else {}
regions = {r['id']: r for r in json.load(open(D + '/slices/regions.json'))}
pids = {p['id'] for p in plan.get('peoples', [])}; bids = {b['id'] for b in plan.get('battles', [])}
ok_rel = set(gaz) | pids | bids | {i for i in allx if i.startswith(('person:', 'thing:'))}
ROLES = {'born', 'lived', 'ruled', 'travelled', 'fought', 'died', 'buried', 'made', 'kept', 'found', 'lost', 'destroyed', 'other'}
err = []
W = lambda s: len(re.findall(r'\w+', s or ''))
def common(c, i, lo, hi):
    for k in ('title', 'kind', 'blurb', 'book', 'sources', 'confidence'):
        if not c.get(k): err.append(f'{i}: field "{k}" is missing or empty')
    if c.get('confidence') not in ('high', 'medium', 'low'): err.append(f'{i}: confidence must be high, medium or low')
    for k in ('film', 'series'):
        if not isinstance(c.get(k, ''), str): err.append(f'{i}: "{k}" must be a string')
    n = W(c.get('book'))
    if n < lo: err.append(f'{i}: book text is too short ({n} words; at least {lo})')
    if n > hi: err.append(f'{i}: book text is too long ({n} words; at most {hi})')
    if W(c.get('blurb')) > 26: err.append(f'{i}: blurb is longer than 26 words')
    for r in c.get('related') or []:
        if r not in ok_rel: err.append(f'{i}: related id {r!r} does not exist (use ids from gaz_index.tsv, plan.json, or person:/thing: ids from all_index.tsv)')
    for k, v in (c.get('facts') or {}).items():
        if not isinstance(v, str) or not v.strip(): err.append(f'{i}: facts["{k}"] must be a string that is not empty')
    for k, v in (c.get('names') or {}).items():
        if not isinstance(v, str) or not v.strip(): err.append(f'{i}: names["{k}"] must be a string that is not empty')
def loadj(p):
    try: return json.load(open(p))
    except Exception as e: print('INVALID JSON or missing file:', p, e); sys.exit(1)
if kind == 'places':
    sl = loadj(f'{D}/slices/slice_{arg}.json'); d = loadj(f'{D}/cards/places_{arg}.json')
    if not isinstance(d, list): print('The file must hold one JSON list'); sys.exit(1)
    if [c.get('id') for c in d] != [s['id'] for s in sl]: err.append('The ids must be the same as the slice, in the same order: ' + ', '.join(s['id'] for s in sl))
    for c in d:
        i = c.get('id', '?'); t = c.get('tier')
        if t not in (1, 2, 3): err.append(f'{i}: tier must be 1, 2 or 3'); t = 3
        common(c, i, {1: 115, 2: 60, 3: 25}[t], {1: 235, 2: 140, 3: 75}[t])
    n = len(d)
elif kind == 'realms':
    d = loadj(D + '/cards/realms.json')
    if set(d) != {'realms', 'peoples'}: print('The file must be one object with the keys "realms" and "peoples"'); sys.exit(1)
    if {c.get('id') for c in d['realms']} != set(regions): err.append('realms must hold exactly the ids of slices/regions.json; missing or extra: ' + str(set(regions) ^ {c.get('id') for c in d['realms']}))
    if {c.get('id') for c in d['peoples']} != pids: err.append('peoples must hold exactly the ids of plan.json; missing or extra: ' + str(pids ^ {c.get('id') for c in d['peoples']}))
    for c in d['realms']:
        i = c.get('id', '?'); t = c.get('tier') if c.get('tier') in (1, 2, 3) else 2; common(c, i, 110 if t == 1 else 50, 225 if t == 1 else 130)
        if i in regions and c.get('type') != regions[i]['type']: err.append(f'{i}: type must be {regions[i]["type"]!r}')
        for p in c.get('peoples') or []:
            if p not in pids and p not in allx: err.append(f'{i}: people id {p!r} does not exist')
    for c in d['peoples']:
        i = c.get('id', '?'); common(c, i, 85, 205)
        for r in c.get('realms') or []:
            if r not in regions: err.append(f'{i}: realm id {r!r} is not in regions.json')
    n = len(d['realms']) + len(d['peoples'])
elif kind == 'battles':
    d = loadj(D + '/cards/battles.json'); pl = {b['id']: b for b in plan['battles']}
    if {c.get('id') for c in d} != set(pl): err.append('battles must hold exactly the ids of plan.json; missing or extra: ' + str(set(pl) ^ {c.get('id') for c in d}))
    for c in d:
        i = c.get('id', '?'); common(c, i, 95, 225)
        for k in ('date', 'outcome', 'sides'):
            if not c.get(k): err.append(f'{i}: field "{k}" is missing or empty')
        if not isinstance(c.get('year_sort'), (int, float)): err.append(f'{i}: year_sort must be a number')
        if i in pl and (c.get('at') or {}).get('near') != pl[i]['near']: err.append(f'{i}: "at.near" must be {pl[i]["near"]!r} (copy from the plan)')
        s = c.get('sides') or {}
        if not (isinstance(s.get('a'), list) and isinstance(s.get('b'), list)): err.append(f'{i}: sides must be {{"a": [...], "b": [...]}}')
    n = len(d)
elif kind == 'journeys':
    d = loadj(D + '/cards/journeys.json'); pl = {j['id']: j for j in plan['journeys']}
    if {c.get('id') for c in d} != set(pl): err.append('journeys must hold exactly the ids of plan.json; missing or extra: ' + str(set(pl) ^ {c.get('id') for c in d}))
    for c in d:
        i = c.get('id', '?')
        for k in ('title', 'travellers', 'dates', 'blurb', 'book', 'sources', 'confidence', 'stages'):
            if not c.get(k): err.append(f'{i}: field "{k}" is missing or empty')
        if not 100 <= W(c.get('book')) <= 225: err.append(f'{i}: book text must be 100 to 225 words ({W(c.get("book"))})')
        st = c.get('stages') or []; ps = pl.get(i, {}).get('stages', [])
        if len(st) != len(ps): err.append(f'{i}: must have {len(ps)} stages as in the plan (has {len(st)})'); continue
        for k, (a, b) in enumerate(zip(st, ps)):
            at = a.get('at') or {}
            if at.get('near') != b['near'] or float(at.get('dx') or 0) != float(b.get('dx') or 0) or float(at.get('dy') or 0) != float(b.get('dy') or 0): err.append(f'{i} stage {k + 1}: "at" must be near={b["near"]!r}, dx={b.get("dx", 0)}, dy={b.get("dy", 0)} (copy from the plan)')
            if not a.get('title'): err.append(f'{i} stage {k + 1}: no title')
            if not 18 <= W(a.get('note')) <= 55: err.append(f'{i} stage {k + 1}: note must be 18 to 55 words ({W(a.get("note"))})')
    n = len(d)
elif kind == 'links':
    d = loadj(D + '/cards/links.json')
    if not isinstance(d, dict): print('The file must hold one JSON object: {"<person or thing id>": [links]}'); sys.exit(1)
    lore_ok = {i for i in allx if i.startswith(('person:', 'thing:'))}
    for i, L in d.items():
        if i not in lore_ok: err.append(f'{i}: is not a person or thing id in all_index.tsv')
        if not isinstance(L, list) or not L: err.append(f'{i}: needs a list with at least one link'); continue
        for p in L:
            if p.get('id') not in gaz or gaz[p['id']]['layer'] in ('Rivers', 'Roads') and False: err.append(f'{i}: place id {p.get("id")!r} is not in gaz_index.tsv')
            if p.get('role') not in ROLES: err.append(f'{i}: role {p.get("role")!r} is not allowed')
            if not p.get('note') or W(p['note']) > 26: err.append(f'{i}: each link needs a note of 26 words or fewer')
    n = len(d)
else: print('unknown kind'); sys.exit(1)
print('\n'.join(err) if err else f'OK {n} items')
