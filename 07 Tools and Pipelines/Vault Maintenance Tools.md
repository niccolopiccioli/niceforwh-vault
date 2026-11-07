---
tags: [tools, maintenance, python, type/guide]
---
# Vault Maintenance Tools

Script **nostri** (scritti in questa sessione, non dei pack), in `_tools/`. Copia master in `Desktop/nicco/anim/tools/`. Si lanciano sempre con `python -I` (modalità isolata), con i percorsi come argomenti.

| Script | Cosa fa |
|---|---|
| `inventory.py <root> <out.csv> [skip...]` | inventario: percorso, estensione, dimensione, SHA1 |
| `reorganize.py plan|run <vault> <screens>` | genera `_data/piano.csv` dalla baseline, lo valida (nessun doppio, nessuno scontro, percorsi < 250), lo esegue in modo ripetibile |
| `build_notes.py <vault>` | rigenera le note hub e le schede (emitter e mesh dai dati) |
| `vault_tools.py index|links|names <vault>` | rigenera [[INDEX]]/[[INDEX_SLIM]], trova wikilink rotti, trova nomi in conflitto con il vault fwjelaa |
| `rbxm_dump.py <file.rbxm> summary|sources|tree` | lettore offline di `.rbxm` binari: classi, sorgente degli script, albero con ID |
| `rbxm_props.py <file.rbxm> <Classi> <out.json>` | estrae tutte le proprietà di una classe (es. ParticleEmitter) in JSON |
| `git_verify.py <repo> <out.tsv>` | confronta ogni file di un checkout con l'hash del blob in `HEAD` (ok / missing / differs), senza hook |
| `ext_stats.py <repo> <inventario.csv> <out.csv>` | statistiche di un repo esterno e quanti file sono già nel vault (per SHA1) |
| `integrate_roblox_ai.py <repo> <tree.tsv> <vault>` | integrazione di roblox-ai: archivio `git archive`, spostamento in `08 Knowledge`, file mancanti dai blob, verifica, inventario, copie deduplicate e log |

## Dati in `_data/`
`inventario-prima.csv` (baseline, 12.021 file) · `inventario-dopo.csv` · `piano.csv` (una riga per file) · `riorganizzazione-log.csv` (ogni spostamento/copia/rimozione) · `duplicati.csv` (ogni gruppo di duplicati) · `kit-emitters.json` · `roblox-ai-inventario.csv` (14.381 file del repo con SHA1, blob git e copia già presente) · `roblox-ai-log.csv` (copie e rinomine) · [[riorganizzazione-log|Riorganizzazione - Log]].

<!-- related:start -->
## Related
[[Tools and Pipelines Hub]] · [[Skill - Safe Asset Intake]] · [[riorganizzazione-log|Riorganizzazione - Log]]
<!-- related:end -->
