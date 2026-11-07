"""Integrate the izzyfrm/roblox-ai checkout into 'niceforwh vault'. Runs no repo code, no hooks.

  python -I integrate_roblox_ai.py <repo_dir> <tree.tsv> <vault>

Steps (idempotent where possible):
  1. _originali/roblox-ai-izzyfrm-<sha7>.zip via `git archive` (object DB, so it has every file of HEAD)
  2. move the working tree (no .git) to 08 Knowledge/roblox-ai
  3. write README.md and the files missing from the checkout straight from their git blobs; shorten a name if the path is >= 250
  4. verify every HEAD entry against its blob hash
  5. _data/roblox-ai-inventario.csv (path, ext, size, sha1, git_blob, renamed_from, in_vault_before)
  6. thematic copies with dedupe -> _data/roblox-ai-log.csv, and the same rows appended to riorganizzazione-log.csv
"""
import csv, hashlib, os, shutil, subprocess, sys

repo, tree_tsv, V = sys.argv[1], sys.argv[2], sys.argv[3]
DEST_REL = '08 Knowledge/roblox-ai'
DEST = os.path.join(V, DEST_REL)
MAXP = 249


def git(*a):
    return subprocess.run(['git', '-c', 'core.hooksPath=NUL', '-c', 'core.autocrlf=false', '-C', repo, *a],
                          capture_output=True, check=True).stdout


def sha1(p):
    h = hashlib.sha1()
    with open(p, 'rb') as f:
        for ch in iter(lambda: f.read(1 << 20), b''):
            h.update(ch)
    return h.hexdigest()


def blobsha(p):
    data = open(p, 'rb').read()
    return hashlib.sha1(b'blob %d\0' % len(data) + data).hexdigest()


head = git('rev-parse', 'HEAD').decode().strip()
tree = [l.rstrip('\n').split('\t') for l in open(tree_tsv, encoding='utf-8')][1:]

# 1. archive
os.makedirs(os.path.join(V, '_originali'), exist_ok=True)
zp = os.path.join(V, '_originali', f'roblox-ai-izzyfrm-{head[:7]}.zip')
if not os.path.exists(zp):
    git('archive', '--format=zip', '-o', zp, 'HEAD')
print('archive', os.path.basename(zp), round(os.path.getsize(zp) / 1e6, 1), 'MB')

# 2. move working tree
os.makedirs(DEST, exist_ok=True)
for name in os.listdir(repo):
    if name == '.git':
        continue
    src, dst = os.path.join(repo, name), os.path.join(DEST, name)
    if os.path.exists(dst):
        continue
    shutil.move(src, dst)

# 3. blobs for README / missing files, with short names where needed
renamed = {}
for mode, blob, path, st in tree:
    if st == 'ok':
        continue
    target_rel = path
    full = os.path.join(DEST, path)
    if len(f'{V}/{DEST_REL}/{path}') > MAXP:
        d, fn = os.path.split(path)
        stem, ext = os.path.splitext(fn)
        keep = MAXP - len(f'{V}/{DEST_REL}/{d}/') - len(ext) - 9
        target_rel = f'{d}/{stem[:keep]}-{blob[:8]}{ext}'
        renamed[path] = target_rel
        full = os.path.join(DEST, target_rel)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    open(full, 'wb').write(git('cat-file', 'blob', blob))
print('restored from blobs', sum(1 for t in tree if t[3] != 'ok'), 'renamed', renamed)

# 4. verify
bad = []
for mode, blob, path, st in tree:
    p = os.path.join(DEST, renamed.get(path, path))
    if not os.path.isfile(p) or blobsha(p) != blob:
        bad.append(path)
print('verify', len(tree) - len(bad), '/', len(tree), 'ok', bad[:5])

# 5. inventory
vault_inv = list(csv.DictReader(open(os.path.join(V, '_data/inventario-dopo.csv'), encoding='utf-8')))
before = {}
for r in vault_inv:
    if not r['path'].startswith(DEST_REL + '/'):
        before.setdefault(r['sha1'], r['path'])
inv = []
for mode, blob, path, st in tree:
    rel = renamed.get(path, path)
    p = os.path.join(DEST, rel)
    h = sha1(p)
    inv.append({'path': f'{DEST_REL}/{rel}', 'ext': os.path.splitext(rel)[1].lower().lstrip('.'),
                'size': os.path.getsize(p), 'sha1': h, 'git_blob': blob,
                'renamed_from': path if path in renamed else '', 'in_vault_before': before.get(h, '')})
with open(os.path.join(V, '_data/roblox-ai-inventario.csv'), 'w', newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=list(inv[0]))
    w.writeheader()
    w.writerows(inv)
print('inventory', len(inv), 'already in vault', sum(1 for r in inv if r['in_vault_before']))

# 6. thematic copies
VFX, ANIM, UI = '01 VFX and Audio', '02 Animation', '05 UI and Icons'
RULES = [  # repo prefix -> vault folder (subpath after the prefix is kept)
    ('sfx/cc0-audio/', f'{VFX}/SFX/CC0 Library (roblox-ai)/'),
    ('motion-references/animation/', f'{ANIM}/References/Roblox Docs Motion (roblox-ai)/animation/'),
    ('motion-references/motion-sequences/', f'{ANIM}/References/Roblox Docs Motion (roblox-ai)/motion-sequences/'),
    ('motion-references/camera/', f'{VFX}/Cinematics/Roblox Docs Camera and Cutscene (roblox-ai)/camera/'),
    ('motion-references/cutscene/', f'{VFX}/Cinematics/Roblox Docs Camera and Cutscene (roblox-ai)/cutscene/'),
    ('game-refs/anime-fighting/', f'{VFX}/Reference Images/Anime Fighting Games (roblox-ai)/'),
    ('thumbnails/', f'{UI}/Branding/Thumbnails/'),
]
thematic = {}
for r in vault_inv:
    if not r['path'].startswith(('07 ', '08 ', '_originali/', '_data/')):
        thematic.setdefault(r['sha1'], r['path'])
log = [{'action': 'project-dir', 'old': f'github.com/izzyfrm/roblox-ai@{head}', 'new': DEST_REL,
        'note': f'whole repo, {len(tree)} files; original archive _originali/{os.path.basename(zp)}'}]
for old, new in renamed.items():
    log.append({'action': 'rename', 'old': old, 'new': f'{DEST_REL}/{new}', 'note': 'path over 249 chars'})
for r in inv:
    rel = r['path'][len(DEST_REL) + 1:]
    for pre, folder in RULES:
        if rel.startswith(pre):
            sub = rel[len(pre):]
            if pre == 'thumbnails/' and '/' in sub:
                break  # curated-2026-11 stays in the repo only
            dst_rel = folder + sub
            if r['sha1'] in thematic:
                log.append({'action': 'skip-copy', 'old': r['path'], 'new': dst_rel, 'note': 'identical to ' + thematic[r['sha1']]})
                break
            if len(f'{V}/{dst_rel}') > MAXP:
                log.append({'action': 'skip-copy', 'old': r['path'], 'new': dst_rel, 'note': 'path too long'})
                break
            dst = os.path.join(V, dst_rel)
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            if not os.path.exists(dst):
                shutil.copy2(os.path.join(V, r['path']), dst)
            thematic[r['sha1']] = dst_rel
            log.append({'action': 'copy', 'old': r['path'], 'new': dst_rel, 'note': ''})
            break
with open(os.path.join(V, '_data/roblox-ai-log.csv'), 'w', newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=['action', 'old', 'new', 'note'])
    w.writeheader()
    w.writerows(log)
mlog = os.path.join(V, '_data/riorganizzazione-log.csv')
existing = open(mlog, encoding='utf-8').read()
if 'izzyfrm/roblox-ai' not in existing:
    with open(mlog, 'a', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=['action', 'old', 'new', 'note'])
        w.writerows(log)
from collections import Counter
print('log', dict(Counter(r['action'] for r in log)))
