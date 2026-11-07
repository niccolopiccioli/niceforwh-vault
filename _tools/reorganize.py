"""Plan-driven reorganization of 'niceforwh vault'.

  python -I reorganize.py plan <vault> <extra_screens_dir>   -> writes _data/piano.csv and prints validation
  python -I reorganize.py run  <vault> <extra_screens_dir>   -> executes _data/piano.csv (idempotent), writes _data/riorganizzazione-log.csv

Actions:
  move         loose file -> thematic folder (os.rename)
  project      file inside an intact project; moved with one directory rename per project
  copy         deliberate copy out of an intact project (or from outside the vault) into a thematic folder
  remove-dup   loose asset whose identical twin (same sha1) stays in the kept tree
  skip-copy    copy not made because an identical file is already in a thematic folder
  keep         left where it is (handled by hand, e.g. the old root README)
Nothing reads from or writes to _originali/.
"""
import csv, hashlib, os, re, shutil, sys

ASSET_EXT = {'png', 'jpg', 'jpeg', 'svg', 'gif', 'webp', 'glb', 'fbx', 'rbxm', 'rbxmx', 'mp4'}
VFX, ANIM, MOD, MAPS, UI, KITS, TOOLS, KNOW, TC = ('01 VFX and Audio', '02 Animation', '03 Models and Characters',
                                                  '04 Maps and World', '05 UI and Icons', '06 Studio Kits',
                                                  '07 Tools and Pipelines', '08 Knowledge', '09 ThunderCombo')
PROJECTS = {  # old dir -> new dir (moved whole)
    'animations/Roblox-Animations-by-fwjelaa': f'{TOOLS}/Roblox-Animations-by-fwjelaa',
    'tools/Picture-to-Roblox-Model-by-fwjelaa': f'{TOOLS}/Picture-to-Roblox-Model-by-fwjelaa',
    'tools/Roblox-Maps-by-fwjelaa': f'{TOOLS}/Roblox-Maps-by-fwjelaa',
    'knowledge/fwjelaa-vault': f'{KNOW}/fwjelaa-vault',
}
UIREF = 'ui/roblox ui references'
UIKIT = f'{TOOLS}/Roblox UI Kit (fwjelaa)'
FW = f'{KNOW}/fwjelaa-vault/fwjelaa vault'          # new location of the nested vault
AP = f'{TOOLS}/Roblox-Animations-by-fwjelaa'
MP = f'{TOOLS}/Roblox-Maps-by-fwjelaa'
PM = f'{TOOLS}/Picture-to-Roblox-Model-by-fwjelaa'
REFNAMES = {'previews': 'Previews', 'style-refs': 'Style Refs', 'ui-styles': 'UI Styles', 'visual-refs': 'Visual Refs'}
RESEARCH = {'01-roblox-pipeline': 'Anim Research 01 - Roblox Animation Pipeline',
            '02-moon-animator-2': 'Anim Research 02 - Moon Animator 2',
            '03-animation-craft': 'Anim Research 03 - Animation Craft Numbers',
            '04-blender-mcp-and-ai': 'Anim Research 04 - Blender MCP and AI',
            '05-popular-animations': 'Anim Research 05 - Popular Roblox Animations'}


def loose_dest(p):
    """Destination for a loose file (not in an intact project), or None."""
    s = p.split('/')
    if p == 'docs/fwjelaa vfx method.md':
        return f'{VFX}/Sources/fwjelaa VFX Method (prompt originale).md'
    if p == 'docs/MASTER_PROMPT.md':
        return f'{UI}/Sources/ForgeGUI UI Rebuild Brief (prompt originale).md'
    if p == 'vfx/particle and model kit.rbxm':
        return f'{KITS}/VFX/PDS Particles and Models Kit.rbxm'
    if s[0] == 'models':
        rest = '/'.join(s[2:])
        if rest == 'README.txt':
            return f'{MOD}/Characters/README - Lift Rock Models.txt'
        return f'{MOD}/Characters/{rest}'
    if p.startswith('ui/UI Icon Pack/'):
        rest = p[len('ui/UI Icon Pack/'):]
        if rest == 'README.txt':
            return f'{UI}/Icons/README - UI Icon Pack.txt'
        return f'{UI}/Icons/{rest}'
    if p.startswith(UIREF + '/'):
        rest = p[len(UIREF) + 1:]
        if rest.startswith('roblox-ui/references/'):
            sub = rest[len('roblox-ui/references/'):]
            if sub == 'README.md':
                return f'{UI}/Style References/README - Style References.md'
            k, tail = sub.split('/', 1)
            return f'{UI}/Style References/{REFNAMES[k]}/{tail}'
        if rest.startswith('roblox-ui/screenshots/'):
            return f'{UI}/Screenshots/Stud Simulator/{rest.split("/", 2)[2]}'
        if rest == 'community-kits/lando-stud-ui-pack/stud-ui-pack.rbxm':
            return f'{KITS}/UI/Stud UI Pack (lando).rbxm'
        if rest == 'community-kits/lando-stud-ui-pack/SOURCE.txt':
            return f'{KITS}/UI/Stud UI Pack (lando) - SOURCE.txt'
        return f'{UIKIT}/{rest}'          # kit, tools, textures, icons, docs, .superpowers: the UI kit project
    return None


def copies(new_path):
    """Thematic copies to extract from a file at its NEW intact-project location. Returns list of destinations."""
    p = new_path
    out = []
    if p.startswith(UIKIT + '/roblox-ui/icons/'):
        out.append(f'{UI}/Icons/12 Kit Icons (roblox-ui)/{os.path.basename(p)}')
    if p.startswith(UIKIT + '/roblox-ui/textures/'):
        out.append(f'{UI}/Textures/{os.path.basename(p)}')
    if p.startswith(AP + '/'):
        rest = p[len(AP) + 1:]
        m = re.match(r'research/(.+)\.md$', rest)
        if m and m.group(1) in RESEARCH:
            out.append(f'{ANIM}/Research/{RESEARCH[m.group(1)]}.md')
        if rest == 'fwjelaa animation method.md':
            out.append(f'{ANIM}/Sources/fwjelaa Animation Method (originale).md')
        if rest.startswith('ref/'):
            out.append(f'{ANIM}/References/{rest[4:]}')
        if rest.startswith('images/'):
            out.append(f'{ANIM}/Previews/Animation Pack - {rest[7:]}')
        if rest.startswith('out/') and rest.endswith('.rbxmx'):
            b = os.path.basename(rest)
            out.append(f'{KITS}/Animations/{"R15" if b.startswith("R15") else "R6"}/{b}')
    if p.startswith(MP + '/'):
        rest = p[len(MP) + 1:]
        m = re.match(r'maps/([^/]+)/shots/(.+)$', rest)
        if m and not m.group(1).startswith('_'):
            out.append(f'{MAPS}/Map Shots/{m.group(1)}/{m.group(2)}')
        m = re.match(r'research/(.+)\.md$', rest)
        if m:
            out.append(f'{MAPS}/Research/Maps Research - {m.group(1)}.md')
    if p.startswith(PM + '/images/') and p.rsplit('.', 1)[-1].lower() in ASSET_EXT:
        out.append(f'{MOD}/Picture-to-Model Previews/{os.path.basename(p)}')
    if p.startswith(FW + '/'):
        rest = p[len(FW) + 1:]
        ext = rest.rsplit('.', 1)[-1].lower()
        if ext in ASSET_EXT or ext in ('mp3', 'ogg', 'wav'):
            for src, dst in (('80 Reference Library/vfx/', f'{VFX}/Reference Images/'),
                             ('80 Reference Library/cutscenes/', f'{VFX}/Cinematics/'),
                             ('80 Reference Library/sfx/', f'{VFX}/SFX/'),
                             ('70 fwjelaa Packs/VFX/', f'{VFX}/Packs/'),
                             ('80 Reference Library/animations/', f'{ANIM}/References/Motion Refs/'),
                             ('73 Kits and Models/Creatures/', f'{MOD}/Creatures/'),
                             ('18 Rigs and Skeletons/', f'{MOD}/Rigs/'),
                             ('19 Concept Sheets/', f'{MOD}/Concept Sheets/'),
                             ('80 Reference Library/ui-icons/', f'{UI}/Icons/13 fwjelaa Library Icons/'),
                             ('80 Reference Library/ui-screenshots/', f'{UI}/Screenshots/Game HUDs/'),
                             ('80 Reference Library/ui-styles/', f'{UI}/Style References/UI Styles/'),
                             ('80 Reference Library/previews/', f'{UI}/Style References/Previews/'),
                             ('80 Reference Library/style-refs/', f'{UI}/Style References/Style Refs/'),
                             ('80 Reference Library/visual-refs/', f'{UI}/Style References/Visual Refs/'),
                             ('80 Reference Library/logos/', f'{UI}/Branding/Logos/'),
                             ('80 Reference Library/thumbnails/', f'{UI}/Branding/Thumbnails/')):
                if rest.startswith(src):
                    out.append(dst + rest[len(src):])
        if rest.startswith('73 Kits and Models/Animations/') and rest.endswith('.rbxmx'):
            b = os.path.basename(rest)
            out.append(f'{KITS}/Animations/{"R15" if b.startswith("R15") else "R6"}/{b}')
    return out


def new_project_path(p):
    for old, new in PROJECTS.items():
        if p == old or p.startswith(old + '/'):
            return new + p[len(old):]
    return None


def sha1(path):
    h = hashlib.sha1()
    with open(path, 'rb') as f:
        for c in iter(lambda: f.read(1 << 20), b''):
            h.update(c)
    return h.hexdigest()


def build(vault, screens):
    rows = list(csv.DictReader(open(os.path.join(vault, '_data/inventario-prima.csv'), encoding='utf-8')))
    plan = []        # (action, src, dst, sha1, ext, note)
    for r in rows:
        p, h, e = r['path'], r['sha1'], r['ext']
        if p.startswith('_data/'):
            continue
        np_ = new_project_path(p)
        if np_:
            plan.append(['project', p, np_, h, e, ''])
            continue
        d = loose_dest(p)
        if d is None:
            plan.append(['keep', p, p, h, e, 'handled by hand'])
        elif d.startswith(UIKIT + '/'):
            plan.append(['project', p, d, h, e, 'UI kit project, kept together'])
        else:
            plan.append(['move', p, d, h, e, ''])
    # extra: ThunderCombo screenshots from outside the vault
    for dp, _, fns in os.walk(screens):
        for fn in sorted(fns):
            if fn.lower().endswith(('.jpg', '.png')):
                src = os.path.join(dp, fn)
                rel = os.path.relpath(src, screens).replace(os.sep, '/')
                sub = rel.split('/')[0] if '/' in rel else 'v1'
                plan.append(['copy', 'EXT:' + src.replace(os.sep, '/'), f'{TC}/Screenshots/{sub}/{os.path.basename(rel)}',
                             sha1(src), fn.rsplit('.', 1)[-1].lower(), 'from anim/screens'])
    # copies out of intact projects
    for row in list(plan):
        if row[0] == 'project':
            for d in copies(row[2]):
                plan.append(['copy', row[2], d, row[3], row[4], 'extracted from intact project'])
    # dedupe among thematic files (move + copy). Keep first by preference: move before copy, then path.
    thematic = [r for r in plan if r[0] in ('move', 'copy')]
    thematic.sort(key=lambda r: (r[0] != 'move', r[2]))
    seen = {}
    for r in thematic:
        if r[4] not in ASSET_EXT:
            continue
        if r[3] in seen:
            keep = seen[r[3]]
            if r[0] == 'move':
                r[0], r[5] = 'remove-dup', f'identical to {keep}'
            else:
                r[0], r[5] = 'skip-copy', f'identical already at {keep}'
        else:
            seen[r[3]] = r[2]
    # destination clashes (different content, same destination) -> suffix
    taken = {}
    for r in plan:
        if r[0] not in ('move', 'copy', 'project'):
            continue
        k = r[2].lower()
        if k in taken and taken[k] != r[3]:
            base, ext = os.path.splitext(r[2])
            i = 2
            while f'{base} ({i}){ext}'.lower() in taken:
                i += 1
            r[5] = (r[5] + '; ' if r[5] else '') + f'renamed from {os.path.basename(r[2])} (name clash)'
            r[2] = f'{base} ({i}){ext}'
            k = r[2].lower()
        taken.setdefault(k, r[3])
    return plan


def validate(vault, plan):
    ok = True
    srcs = [r[1] for r in plan if not r[1].startswith('EXT:') and r[0] != 'copy']
    if len(srcs) != len(set(srcs)):
        print('ERROR: a source is mapped twice'); ok = False
    dst = {}
    for r in plan:
        if r[0] in ('move', 'copy', 'project'):
            if r[2].lower() in dst and dst[r[2].lower()] != r[3]:
                print('ERROR clash', r[2]); ok = False
            dst[r[2].lower()] = r[3]
            if len(os.path.join(vault, r[2])) > 250:
                print('ERROR long path', len(os.path.join(vault, r[2])), r[2]); ok = False
        if '_originali' in r[1].split('/')[0] or r[2].startswith('_originali'):
            print('ERROR touches _originali', r); ok = False
    return ok


def write_plan(vault, plan):
    with open(os.path.join(vault, '_data/piano.csv'), 'w', newline='', encoding='utf-8') as f:
        w = csv.writer(f)
        w.writerow(['action', 'src', 'dst', 'sha1', 'ext', 'note'])
        w.writerows(plan)


def run(vault, plan):
    J = lambda p: os.path.join(vault, p)
    log = []
    # 1) loose moves and dup removals
    for a, s, d, h, e, n in plan:
        if a == 'move':
            if os.path.exists(J(d)):
                if sha1(J(d)) == h:
                    if os.path.exists(J(s)) and J(s) != J(d):
                        os.remove(J(s))
                    continue
                raise SystemExit(f'destination exists with other content: {d}')
            os.makedirs(os.path.dirname(J(d)), exist_ok=True)
            os.rename(J(s), J(d))
            log.append((a, s, d, n))
        elif a == 'remove-dup':
            if os.path.exists(J(s)):
                os.remove(J(s))
            log.append((a, s, '', n))
    # 2) intact projects: one directory rename each
    for old, new in PROJECTS.items():
        if os.path.isdir(J(old)) and not os.path.exists(J(new)):
            os.makedirs(os.path.dirname(J(new)), exist_ok=True)
            os.rename(J(old), J(new))
            log.append(('project-dir', old, new, 'moved whole'))
    # UI kit project parts (per file, kept together under one folder)
    for a, s, d, h, e, n in plan:
        if a == 'project' and d.startswith(UIKIT + '/') and os.path.exists(J(s)):
            os.makedirs(os.path.dirname(J(d)), exist_ok=True)
            os.rename(J(s), J(d))
            log.append(('project-file', s, d, n))
    # 3) copies
    for a, s, d, h, e, n in plan:
        if a != 'copy':
            continue
        src = s[4:] if s.startswith('EXT:') else J(s)
        if os.path.exists(J(d)) and sha1(J(d)) == h:
            continue
        os.makedirs(os.path.dirname(J(d)), exist_ok=True)
        shutil.copy2(src, J(d))
        log.append((a, s, d, n))
    # 4) remove now-empty old folders (only if empty)
    for top in ('docs', 'vfx', 'models', 'ui', 'animations', 'tools', 'knowledge'):
        for dp, dns, fns in sorted(os.walk(J(top), topdown=False), key=lambda x: -len(x[0])):
            try:
                os.rmdir(dp)
            except OSError:
                pass
    with open(J('_data/riorganizzazione-log.csv'), 'w', newline='', encoding='utf-8') as f:
        w = csv.writer(f)
        w.writerow(['action', 'old', 'new', 'note'])
        w.writerows(log)
    print(len(log), 'log rows')


if __name__ == '__main__':
    cmd, vault, screens = sys.argv[1], sys.argv[2], sys.argv[3]
    plan = build(vault, screens)
    good = validate(vault, plan)
    from collections import Counter
    print(Counter(r[0] for r in plan))
    print('valid' if good else 'INVALID')
    if cmd == 'plan':
        write_plan(vault, plan)
    elif cmd == 'run':
        if not good:
            raise SystemExit('plan invalid, not running')
        write_plan(vault, plan)
        run(vault, plan)
