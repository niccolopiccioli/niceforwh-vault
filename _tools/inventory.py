"""Inventory of a folder tree: path, ext, size, sha1. Read-only. Usage: python -I inventory.py <root> <out.csv> [skipdir ...]"""
import csv, hashlib, os, sys

root, out = sys.argv[1], sys.argv[2]
skip = set(sys.argv[3:])
rows = []
for dp, dns, fns in os.walk(root):
    rel_dp = os.path.relpath(dp, root)
    if rel_dp.split(os.sep)[0] in skip:
        dns[:] = []
        continue
    for fn in fns:
        p = os.path.join(dp, fn)
        h = hashlib.sha1()
        try:
            with open(p, 'rb') as f:
                for chunk in iter(lambda: f.read(1 << 20), b''):
                    h.update(chunk)
            size = os.path.getsize(p)
        except OSError as e:
            print('ERR', p, e)
            continue
        ext = os.path.splitext(fn)[1].lower().lstrip('.')
        rows.append((os.path.relpath(p, root).replace(os.sep, '/'), ext, size, h.hexdigest()))
rows.sort()
os.makedirs(os.path.dirname(out), exist_ok=True)
with open(out, 'w', newline='', encoding='utf-8') as f:
    w = csv.writer(f)
    w.writerow(['path', 'ext', 'size', 'sha1'])
    w.writerows(rows)
print(len(rows), 'files ->', out)
