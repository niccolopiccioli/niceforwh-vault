"""Duplicate report from the baseline inventory + plan.
Usage: python -I dupes.py <vault>   -> writes _data/duplicati.csv and _data/duplicati-stats.txt
"""
import csv, os, sys
from collections import defaultdict

V = sys.argv[1]
inv = list(csv.DictReader(open(os.path.join(V, '_data/inventario-prima.csv'), encoding='utf-8')))
plan = {r['src']: r for r in csv.DictReader(open(os.path.join(V, '_data/piano.csv'), encoding='utf-8'))}
INTACT_SRC = ('animations/Roblox-Animations-by-fwjelaa/', 'tools/', 'knowledge/', 'ui/roblox ui references/')

groups = defaultdict(list)
for r in inv:
    if int(r['size']) > 0:
        groups[r['sha1']].append(r)
dup = {h: g for h, g in groups.items() if len(g) > 1}

rows, removed, extra, extra_bytes, kept_proj, kept_other = [], 0, 0, 0, 0, 0
for h, g in sorted(dup.items(), key=lambda x: -int(x[1][0]['size']) * (len(x[1]) - 1)):
    acts = [plan.get(r['path'], {}).get('action', '?') for r in g]
    n_rm = acts.count('remove-dup')
    removed += n_rm
    extra += len(g) - 1
    extra_bytes += int(g[0]['size']) * (len(g) - 1)
    survivors = len(g) - n_rm
    if survivors > 1:
        if any(a == 'project' for a in acts):
            kept_proj += survivors - 1
        else:
            kept_other += survivors - 1
    if n_rm:
        status = 'rimosso (resta 1 copia per ogni posto tematico)'
    elif all(a == 'project' for a in acts):
        status = 'tenuto: tutto dentro progetti intatti'
    elif any(a == 'project' for a in acts):
        status = 'tenuto: una copia nel progetto intatto, una nella cartella tematica'
    else:
        status = 'tenuto: non-asset (README/LICENSE/md) o posti diversi'
    for r, a in zip(g, acts):
        rows.append([h, r['size'], len(g), r['path'], a, plan.get(r['path'], {}).get('dst', ''), status])

with open(os.path.join(V, '_data/duplicati.csv'), 'w', newline='', encoding='utf-8') as f:
    w = csv.writer(f)
    w.writerow(['sha1', 'size', 'copie_nel_gruppo', 'vecchio_percorso', 'azione', 'nuovo_percorso', 'stato_gruppo'])
    w.writerows(rows)

stats = (f'### Duplicati (baseline, file non vuoti, per SHA1)\n'
         f'| | |\n|---|---|\n'
         f'| gruppi di file identici | {len(dup)} |\n'
         f'| copie in più trovate | {extra} ({extra_bytes / 1e6:.0f} MB) |\n'
         f'| rimosse | {removed} |\n'
         f'| tenute apposta: almeno una copia sta dentro un progetto intatto (vault fwjelaa, tool), che non si smonta | {kept_proj} |\n'
         f'| tenute fuori dai progetti (README, LICENSE, note .md con lo stesso testo in pack diversi) | {kept_other} |\n\n'
         f'Elenco completo gruppo per gruppo: `_data/duplicati.csv`.\n')
open(os.path.join(V, '_data/duplicati-stats.txt'), 'w', encoding='utf-8').write(stats)
print(stats)
