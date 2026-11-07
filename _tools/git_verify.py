"""Verify a checked-out tree against git HEAD blob hashes, without running git hooks or any repo code.
Usage: python -I git_verify.py <repo_dir> <out_tree.tsv>
Writes: mode, blob sha, path, status (ok / missing / differs). Prints a summary.
"""
import hashlib, os, subprocess, sys

repo, out = sys.argv[1], sys.argv[2]
tree = subprocess.run(['git', '-c', 'core.hooksPath=NUL', '-C', repo, 'ls-tree', '-r', '-z', 'HEAD'],
                      capture_output=True, check=True).stdout.split(b'\0')
rows, stat = [], {'ok': 0, 'missing': 0, 'differs': 0, 'nonfile': 0}
for ent in tree:
    if not ent:
        continue
    meta, path = ent.split(b'\t', 1)
    mode, typ, sha = meta.decode().split()
    path = path.decode('utf-8', 'replace')
    if typ != 'blob' or mode in ('120000', '160000'):
        rows.append((mode, sha, path, 'nonfile'))
        stat['nonfile'] += 1
        continue
    p = os.path.join(repo, path)
    if not os.path.isfile(p):
        st = 'missing'
    else:
        data = open(p, 'rb').read()
        h = hashlib.sha1(b'blob %d\0' % len(data) + data).hexdigest()
        st = 'ok' if h == sha else 'differs'
    stat[st] += 1
    rows.append((mode, sha, path, st))
with open(out, 'w', encoding='utf-8') as f:
    f.write('mode\tblob\tpath\tstatus\n')
    for r in rows:
        f.write('\t'.join(r) + '\n')
print(len(rows), 'entries', stat)
for r in rows:
    if r[3] not in ('ok',):
        print(r[3], r[2])
