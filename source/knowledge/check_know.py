"""Check a knowledge entry file.  Usage: python3 check_know.py <file.json> <id prefix> "<group>[|<group2>...]" <min words> <max words> [min items]"""
import json, sys, csv, re
N = '/home/claude/me/new/'
f, prefix, groups, lo, hi = sys.argv[1], sys.argv[2], sys.argv[3].split('|'), int(sys.argv[4]), int(sys.argv[5])
minitems = int(sys.argv[6]) if len(sys.argv) > 6 else 1
try: d = json.load(open(f))
except Exception as e: print('INVALID JSON:', e); sys.exit(1)
if not isinstance(d, list): print('The file must hold one JSON list'); sys.exit(1)
idx = {r['id']: r for r in csv.DictReader(open(N + 'all_index.tsv'), delimiter='\t')}
place_ok = {i for i, r in idx.items() if r['type'] in ('place', 'realm', 'battle')}
titles = {r['title'].lower() for r in idx.values()}
ROLES = {'born', 'lived', 'ruled', 'travelled', 'fought', 'died', 'buried', 'made', 'kept', 'found', 'lost', 'destroyed', 'other'}
err, seen = [], set()
for c in d:
    i = c.get('id', '?')
    if i in seen: err.append(f'{i}: appears two times')
    seen.add(i)
    if not re.fullmatch(r'lore:' + re.escape(prefix) + r'[a-z0-9-]+', i): err.append(f'{i}: id must be "lore:{prefix}<slug>" with lowercase letters, digits and hyphens')
    for k in ('title', 'kind', 'blurb', 'sources', 'confidence'):
        if not c.get(k): err.append(f'{i}: field "{k}" is missing or empty')
    if c.get('group') not in groups: err.append(f'{i}: group must be one of {groups}')
    if (c.get('title') or '').lower() in titles: err.append(f'{i}: a card with the title {c.get("title")!r} exists already; remove this entry or change its subject')
    if c.get('confidence') not in ('high', 'medium', 'low'): err.append(f'{i}: confidence must be high, medium or low')
    if len((c.get('blurb') or '').split()) > 30: err.append(f'{i}: blurb is longer than 30 words')
    for k in ('book', 'film', 'series'):
        if not isinstance(c.get(k, ''), str): err.append(f'{i}: "{k}" must be a string')
    nw = sum(len(re.findall(r'\w+', c.get(k) or '')) for k in ('book', 'film', 'series'))
    if nw < lo: err.append(f'{i}: text is too short ({nw} words; at least {lo})')
    if nw > hi: err.append(f'{i}: text is too long ({nw} words; at most {hi})')
    for k, v in (c.get('facts') or {}).items():
        if not isinstance(v, str) or not v.strip(): err.append(f'{i}: facts["{k}"] must be a string that is not empty')
    for p in c.get('places') or []:
        if p.get('id') not in place_ok: err.append(f'{i}: place id {p.get("id")!r} is not a place, realm or battle in all_index.tsv')
        if p.get('role') not in ROLES: err.append(f'{i}: role {p.get("role")!r} is not allowed')
        if len((p.get('note') or '').split()) > 26: err.append(f'{i}: a place note is longer than 26 words')
    for r in c.get('related') or []:
        if r not in idx: err.append(f'{i}: related id {r!r} is not in all_index.tsv')
    if not isinstance(c.get('aka', []), list): err.append(f'{i}: aka must be a list')
if len(d) < minitems: err.append(f'the file has {len(d)} entries; your task needs at least {minitems}')
print('\n'.join(err) if err else f'OK {len(d)} entries')
