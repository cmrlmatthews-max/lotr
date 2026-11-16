"""Check a card file.  Usage: python3 check.py <file.json> people|things|places <batch or land>
Prints every problem; prints OK when there is none."""
import json, sys, csv, re
N = '/home/claude/me/new/'
f, kind, batch = sys.argv[1], sys.argv[2], sys.argv[3]
try: d = json.load(open(f))
except Exception as e: print('INVALID JSON:', e); sys.exit(1)
if not isinstance(d, list): print('The file must hold one JSON list'); sys.exit(1)
idx = {r['id']: r for r in csv.DictReader(open(N + 'map_index.tsv'), delimiter='\t')}
mp = json.load(open(N + 'master_places.json')); mpe = json.load(open(N + 'master_people.json')); mth = json.load(open(N + 'master_things.json'))
place_ok = {i for i, r in idx.items() if r['type'] in ('place', 'realm', 'battle')} | {p['id'] for p in mp}
lore_ok = {p['id'] for p in mpe} | {t['id'] for t in mth}
ROLES = {'born', 'lived', 'ruled', 'travelled', 'fought', 'died', 'buried', 'made', 'kept', 'found', 'lost', 'destroyed', 'other'}
err = []
if kind == 'places':
    want = {p['id']: p for p in mp if p['land'] == batch or batch == 'all'}
    m = re.match(r'(me|bel):(\d+)-(\d+)$', batch)
    if m: want = {p['id']: p for p in mp if p['land'] == m.group(1) and int(m.group(2)) <= int(p['id'][-3:]) <= int(m.group(3))}
else:
    m = mpe if kind == 'people' else mth
    want = {p['id']: p for p in m if str(p['batch']) == str(batch)}
got = {}
for c in d:
    i = c.get('id', '?')
    if i in got: err.append(f'{i}: appears two times')
    got[i] = c
    if i not in want: err.append(f'{i}: is not in this batch of the master list'); continue
    w = want[i]
    for k in ('title', 'kind', 'blurb', 'book', 'sources', 'confidence'):
        if not c.get(k): err.append(f'{i}: field "{k}" is missing or empty')
    for k in ('film', 'series'):
        if not isinstance(c.get(k, ''), str): err.append(f'{i}: "{k}" must be a string')
    if c.get('title') != w['title']: err.append(f'{i}: title must be exactly {w["title"]!r}')
    if c.get('confidence') not in ('high', 'medium', 'low'): err.append(f'{i}: confidence must be high, medium or low')
    if len((c.get('blurb') or '').split()) > 30: err.append(f'{i}: blurb is longer than 30 words')
    for k, v in (c.get('facts') or {}).items():
        if not isinstance(v, str) or not v.strip(): err.append(f'{i}: facts["{k}"] must be a string that is not empty (remove the key if unknown)')
    if kind == 'places':
        for k in ('land', 'layer', 'tier', 'x', 'y'):
            if c.get(k) != w[k]: err.append(f'{i}: "{k}" must be {w[k]!r} (copy from master_places.json)')
        for r in c.get('related') or []:
            if r not in place_ok and r not in lore_ok and r not in idx: err.append(f'{i}: related id {r!r} does not exist')
        if not c.get('facts'): err.append(f'{i}: facts is empty')
    else:
        if c.get('group') != w['group']: err.append(f'{i}: group must be {w["group"]!r}')
        pl = c.get('places') or []
        if not pl and not c.get('offmap'): err.append(f'{i}: needs at least one entry in "places" or "offmap"')
        for p in pl:
            if p.get('id') not in place_ok: err.append(f'{i}: place id {p.get("id")!r} is not a place, realm or battle in map_index.tsv or master_places.json')
            if p.get('role') not in ROLES: err.append(f'{i}: role {p.get("role")!r} is not allowed')
            if len((p.get('note') or '').split()) > 26: err.append(f'{i}: a place note is longer than 26 words')
        for p in c.get('offmap') or []:
            if not p.get('name'): err.append(f'{i}: an offmap entry has no name')
            if p.get('role') not in ROLES: err.append(f'{i}: offmap role {p.get("role")!r} is not allowed')
        for r in c.get('related') or []:
            if r not in lore_ok: err.append(f'{i}: related id {r!r} is not in the master lists')
        if not isinstance(c.get('aka', []), list): err.append(f'{i}: aka must be a list')
    nw = len(re.findall(r'\w+', c.get('book') or ''))
    if nw < 40: err.append(f'{i}: book text is very short ({nw} words)')
    if nw > 330: err.append(f'{i}: book text is too long ({nw} words)')
for i in want:
    if i not in got: err.append(f'{i} ({want[i]["title"]}): card is missing')
print('\n'.join(err) if err else f'OK {len(d)} cards')
