"""Stats of an external checkout vs the vault inventory. Read-only.
Usage: python -I ext_stats.py <repo_dir> <vault_inventory.csv> <out.csv>
"""
import csv, hashlib, os, sys
from collections import Counter, defaultdict

repo, invp, out = sys.argv[1], sys.argv[2], sys.argv[3]
vault = defaultdict(list)
for r in csv.DictReader(open(invp, encoding='utf-8')):
    vault[r['sha1']].append(r['path'])
rows = []
for dp, dns, fns in os.walk(repo):
    if '.git' in dns:
        dns.remove('.git')
    for fn in fns:
        p = os.path.join(dp, fn)
        rel = os.path.relpath(p, repo).replace(os.sep, '/')
        h = hashlib.sha1()
        with open(p, 'rb') as f:
            for ch in iter(lambda: f.read(1 << 20), b''):
                h.update(ch)
        rows.append((rel, os.path.splitext(fn)[1].lower().lstrip('.'), os.path.getsize(p), h.hexdigest()))
rows.sort()
with open(out, 'w', newline='', encoding='utf-8') as f:
    w = csv.writer(f)
    w.writerow(['path', 'ext', 'size', 'sha1', 'in_vault'])
    for r in rows:
        w.writerow(list(r) + [vault[r[3]][0] if r[3] in vault else ''])
ext = Counter(r[1] for r in rows)
print('files', len(rows), 'MB', round(sum(r[2] for r in rows) / 1e6, 1))
print('ext', dict(ext.most_common()))
top = defaultdict(lambda: [0, 0, 0, 0])
for r in rows:
    t = r[0].split('/')[0] if '/' in r[0] else '(root)'
    top[t][0] += 1
    top[t][1] += r[2]
    if r[3] in vault:
        top[t][2] += 1
seen = {}
for r in rows:
    seen.setdefault(r[3], r[0])
uniq = len(seen)
print('unique by content', uniq)
for t, v in sorted(top.items()):
    print(f'{t:20s} files {v[0]:6d}  MB {v[1]/1e6:7.1f}  already in vault {v[2]:6d}')
