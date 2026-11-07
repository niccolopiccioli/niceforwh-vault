---
tags: [index, log, type/reference]
---
# Riorganizzazione - Log

Riorganizzazione del 2026-11-06: dal vecchio ordine per pack (`docs/`, `vfx/`, `models/`, `ui/`, `animations/`, `tools/`, `knowledge/`) all'ordine per tema. **Mappatura completa per file**: `_data/riorganizzazione-log.csv` (vecchio → nuovo) e `_data/piano.csv` (una riga per ognuno dei 12.021 file della baseline, con azione e SHA1).

## Numeri
| Azione | File |
|---|---|
| spostati in cartelle tematiche (`move`) | 4367 |
| nei progetti intatti (`project`, spostati con la loro cartella) | 7582 |
| copie estratte da progetti intatti o da `anim/screens` (`copy`) | 711 |
| copie non fatte perché già presenti (`skip-copy`) | 4351 |
| duplicati rimossi (`remove-dup`) | 71 |

> [!note] File modificati dopo lo spostamento
> - Le 11 copie delle research (`02 Animation/Research`, `04 Maps and World/Research`) hanno in testa un blocco di provenienza (frontmatter `source:` + un riquadro): il loro SHA1 non corrisponde più a `piano.csv`. Gli originali intatti sono nei progetti in `07 Tools and Pipelines`.
> - Il vecchio `README.md` (scritto nel round precedente, descriveva l'ordine per pack) è stato sostituito da un rimando a [[00 Start Here]].
> - `_assets/thundercombo-banner.jpg` è un ritaglio largo di `09 ThunderCombo/Screenshots/v3/1_carica_kit.jpg`, non una copia.

### Duplicati (baseline, file non vuoti, per SHA1)
| | |
|---|---|
| gruppi di file identici | 4620 |
| copie in più trovate | 4783 (217 MB) |
| rimosse | 71 |
| tenute apposta: almeno una copia sta dentro un progetto intatto (vault fwjelaa, tool), che non si smonta | 4712 |
| tenute fuori dai progetti (README, LICENSE, note .md con lo stesso testo in pack diversi) | 0 |

Elenco completo gruppo per gruppo: `_data/duplicati.csv`.


## Integrazione roblox-ai (2026-11-06)
Repo `github.com/izzyfrm/roblox-ai`, commit `082517a`: **intero** in `08 Knowledge/roblox-ai/` (14381 file), archivio `_originali/roblox-ai-izzyfrm-082517a.zip`. Dettagli in [[roblox-ai Reference Library]].

| Azione | File |
|---|---|
| repo intero (`project-dir`) | 14381 |
| copie nelle cartelle tematiche (`copy`) | 2429 |
| copie non fatte perché già presenti (`skip-copy`) | 8 |
| nome accorciato, percorso oltre 249 caratteri (`rename`) | 1 |

Righe aggiunte anche in coda a `_data/riorganizzazione-log.csv`; dettaglio in `_data/roblox-ai-log.csv`.

## Regole per cartella
| Vecchio | Nuovo |
|---|---|
| `docs/fwjelaa vfx method.md` | `01 VFX and Audio/Sources/fwjelaa VFX Method (prompt originale).md` |
| `docs/MASTER_PROMPT.md` | `05 UI and Icons/Sources/ForgeGUI UI Rebuild Brief (prompt originale).md` |
| `vfx/particle and model kit.rbxm` | `06 Studio Kits/VFX/PDS Particles and Models Kit.rbxm` |
| `models/Lift Rock Models (personaggi glb)/*` | `03 Models and Characters/Characters/*` (README → `README - Lift Rock Models.txt`) |
| `ui/UI Icon Pack/*` | `05 UI and Icons/Icons/*` (README → `README - UI Icon Pack.txt`) |
| `ui/roblox ui references/roblox-ui/references/{previews,style-refs,ui-styles,visual-refs}` | `05 UI and Icons/Style References/{Previews,Style Refs,UI Styles,Visual Refs}` |
| `ui/roblox ui references/roblox-ui/screenshots` | `05 UI and Icons/Screenshots/Stud Simulator` |
| `ui/roblox ui references/community-kits/lando-stud-ui-pack/*` | `06 Studio Kits/UI/Stud UI Pack (lando).rbxm` + `- SOURCE.txt` |
| resto di `ui/roblox ui references/` (kit, tools, textures, icons, docs, .superpowers) | `07 Tools and Pipelines/Roblox UI Kit (fwjelaa)/` |
| `animations/Roblox-Animations-by-fwjelaa` | `07 Tools and Pipelines/Roblox-Animations-by-fwjelaa` (intero) |
| `tools/Picture-to-Roblox-Model-by-fwjelaa` | `07 Tools and Pipelines/Picture-to-Roblox-Model-by-fwjelaa` (intero) |
| `tools/Roblox-Maps-by-fwjelaa` | `07 Tools and Pipelines/Roblox-Maps-by-fwjelaa` (intero) |
| `knowledge/fwjelaa-vault` | `08 Knowledge/fwjelaa-vault` (intero) |
| vecchio `README.md` | sostituito da un rimando a [[00 Start Here]] |

## Copie estratte (rinominate)
| Da | A |
|---|---|
| animation pack `research/01..05-*.md` | `02 Animation/Research/Anim Research 01..05 - ....md` |
| animation pack `fwjelaa animation method.md` | `02 Animation/Sources/fwjelaa Animation Method (originale).md` |
| animation pack `images/*` | `02 Animation/Previews/Animation Pack - *` |
| animation pack `ref/*` | `02 Animation/References/*` |
| animation pack `out/*.rbxmx` e fwjelaa `73 Kits and Models/Animations/*.rbxmx` | `06 Studio Kits/Animations/R6|R15/` (una copia per file) |
| MapKit `maps/*/shots/*`, `research/*.md` | `04 Maps and World/Map Shots/*`, `Research/Maps Research - *.md` |
| Picture-to-Model `images/*` | `03 Models and Characters/Picture-to-Model Previews/` |
| fwjelaa `80 Reference Library/{vfx,cutscenes,sfx,animations,ui-icons,ui-screenshots,ui-styles,previews,style-refs,visual-refs,logos,thumbnails}` | `01 VFX and Audio/...`, `02 Animation/References/Motion Refs`, `05 UI and Icons/...` |
| fwjelaa `18 Rigs and Skeletons`, `19 Concept Sheets`, `73 Kits and Models/Creatures` | `03 Models and Characters/Rigs`, `Concept Sheets`, `Creatures` |
| UI kit `roblox-ui/icons`, `textures` | `05 UI and Icons/Icons/12 Kit Icons (roblox-ui)`, `Textures` |
| `Desktop/nicco/anim/screens/**` | `09 ThunderCombo/Screenshots/v1|v2|v3` |

## Duplicati rimossi (71)
Tutti asset (immagini, modelli, kit): README, LICENSE, manifest e file senza estensione non vengono mai deduplicati. Per ognuno resta una copia identica nella cartella tematica (e l'archivio originale in `_originali/`).
| Rimosso (vecchio percorso) | Identico a |
|---|---|
| `ui/UI Icon Pack/09 Rank Icons/Hexagon/Wood/hexagon-wood-1.png` | `05 UI and Icons/Icons/09 Rank Icons/Hexagon/Bronze/hexagon-bronze-1.png` |
| `ui/roblox ui references/roblox-ui/references/previews/buttons-user-interface/02.gif` | `05 UI and Icons/Style References/Previews/animation-user-interface/03.gif` |
| `ui/roblox ui references/roblox-ui/references/previews/buttons-user-interface/06.gif` | `05 UI and Icons/Style References/Previews/animation-user-interface/04.gif` |
| `ui/roblox ui references/roblox-ui/references/previews/casual-user-interface/01.gif` | `05 UI and Icons/Style References/Previews/buttons-user-interface/01.gif` |
| `ui/roblox ui references/roblox-ui/references/previews/fantasy-user-interface/08.png` | `05 UI and Icons/Style References/Previews/buttons-user-interface/03.png` |
| `ui/roblox ui references/roblox-ui/references/previews/fighting-user-interface/01.png` | `05 UI and Icons/Style References/Previews/fantasy-user-interface/02.png` |
| `ui/roblox ui references/roblox-ui/references/previews/hand-drawn-user-interface/01.png` | `05 UI and Icons/Style References/Previews/animation-user-interface/05.png` |
| `ui/roblox ui references/roblox-ui/references/previews/hand-drawn-user-interface/11.png` | `05 UI and Icons/Style References/Previews/card-game-user-interface/12.png` |
| `ui/roblox ui references/roblox-ui/references/previews/horror-user-interface/07.gif` | `05 UI and Icons/Style References/Previews/dark-user-interface/01.gif` |
| `ui/roblox ui references/roblox-ui/references/previews/horror-user-interface/12.png` | `05 UI and Icons/Style References/Previews/dark-user-interface/03.png` |
| `ui/roblox ui references/roblox-ui/references/previews/icons-user-interface/04.gif` | `05 UI and Icons/Style References/Previews/buttons-user-interface/01.gif` |
| `ui/roblox ui references/roblox-ui/references/previews/icons-user-interface/05.gif` | `05 UI and Icons/Style References/Previews/fantasy-user-interface/03.gif` |
| `ui/roblox ui references/roblox-ui/references/previews/icons-user-interface/06.gif` | `05 UI and Icons/Style References/Previews/casual-user-interface/02.gif` |
| `ui/roblox ui references/roblox-ui/references/previews/icons-user-interface/07.png` | `05 UI and Icons/Style References/Previews/fantasy-user-interface/06.png` |
| `ui/roblox ui references/roblox-ui/references/previews/icons-user-interface/08.png` | `05 UI and Icons/Style References/Previews/buttons-user-interface/03.png` |
| `ui/roblox ui references/roblox-ui/references/previews/icons-user-interface/09.gif` | `05 UI and Icons/Style References/Previews/fantasy-user-interface/10.gif` |
| `ui/roblox ui references/roblox-ui/references/previews/medieval-user-interface/01.png` | `05 UI and Icons/Style References/Previews/horror-user-interface/02.png` |
| `ui/roblox ui references/roblox-ui/references/previews/medieval-user-interface/02.png` | `05 UI and Icons/Style References/Previews/fantasy-user-interface/04.png` |
| `ui/roblox ui references/roblox-ui/references/previews/medieval-user-interface/03.gif` | `05 UI and Icons/Style References/Previews/fantasy-user-interface/05.gif` |
| `ui/roblox ui references/roblox-ui/references/previews/medieval-user-interface/04.gif` | `05 UI and Icons/Style References/Previews/fantasy-user-interface/07.gif` |
| `ui/roblox ui references/roblox-ui/references/previews/medieval-user-interface/05.png` | `05 UI and Icons/Style References/Previews/fantasy-user-interface/12.png` |
| `ui/roblox ui references/roblox-ui/references/previews/medieval-user-interface/08.jpg` | `05 UI and Icons/Style References/Previews/gothic-user-interface/02.jpg` |
| `ui/roblox ui references/roblox-ui/references/previews/mobile-user-interface/01.png` | `05 UI and Icons/Style References/Previews/horror-user-interface/04.png` |
| `ui/roblox ui references/roblox-ui/references/previews/mobile-user-interface/07.png` | `05 UI and Icons/Style References/Previews/idle-user-interface/01.png` |
| `ui/roblox ui references/roblox-ui/references/previews/paper-user-interface/01.png` | `05 UI and Icons/Style References/Previews/hand-drawn-user-interface/05.png` |
| `ui/roblox ui references/roblox-ui/references/previews/pixel-art-user-interface/01.gif` | `05 UI and Icons/Style References/Previews/animation-user-interface/01.gif` |
| `ui/roblox ui references/roblox-ui/references/previews/pixel-art-user-interface/03.png` | `05 UI and Icons/Style References/Previews/horror-user-interface/02.png` |
| `ui/roblox ui references/roblox-ui/references/previews/pixel-art-user-interface/04.png` | `05 UI and Icons/Style References/Previews/icons-user-interface/02.png` |
| `ui/roblox ui references/roblox-ui/references/previews/pixel-art-user-interface/06.gif` | `05 UI and Icons/Style References/Previews/fantasy-user-interface/01.gif` |
| `ui/roblox ui references/roblox-ui/references/previews/pixel-art-user-interface/07.png` | `05 UI and Icons/Style References/Previews/icons-user-interface/03.png` |
| `ui/roblox ui references/roblox-ui/references/previews/pixel-art-user-interface/08.gif` | `05 UI and Icons/Style References/Previews/buttons-user-interface/01.gif` |
| `ui/roblox ui references/roblox-ui/references/previews/pixel-art-user-interface/09.png` | `05 UI and Icons/Style References/Previews/fantasy-user-interface/02.png` |
| `ui/roblox ui references/roblox-ui/references/previews/pixel-art-user-interface/11.gif` | `05 UI and Icons/Style References/Previews/fantasy-user-interface/03.gif` |
| `ui/roblox ui references/roblox-ui/references/previews/pixel-art-user-interface/12.gif` | `05 UI and Icons/Style References/Previews/animation-user-interface/02.gif` |
| `ui/roblox ui references/roblox-ui/references/previews/racing-user-interface/01.png` | `05 UI and Icons/Style References/Previews/mobile-user-interface/05.png` |
| `ui/roblox ui references/roblox-ui/references/previews/retro-user-interface/01.png` | `05 UI and Icons/Style References/Previews/icons-user-interface/01.png` |
| `ui/roblox ui references/roblox-ui/references/previews/retro-user-interface/02.png` | `05 UI and Icons/Style References/Previews/horror-user-interface/02.png` |
| `ui/roblox ui references/roblox-ui/references/previews/retro-user-interface/03.gif` | `05 UI and Icons/Style References/Previews/pixel-art-user-interface/05.gif` |
| `ui/roblox ui references/roblox-ui/references/previews/retro-user-interface/04.gif` | `05 UI and Icons/Style References/Previews/fantasy-user-interface/01.gif` |
| `ui/roblox ui references/roblox-ui/references/previews/retro-user-interface/05.png` | `05 UI and Icons/Style References/Previews/fantasy-user-interface/02.png` |
| `ui/roblox ui references/roblox-ui/references/previews/retro-user-interface/06.gif` | `05 UI and Icons/Style References/Previews/pixel-art-user-interface/10.gif` |
| `ui/roblox ui references/roblox-ui/references/previews/retro-user-interface/07.png` | `05 UI and Icons/Style References/Previews/fantasy-user-interface/04.png` |
| `ui/roblox ui references/roblox-ui/references/previews/retro-user-interface/09.gif` | `05 UI and Icons/Style References/Previews/fantasy-user-interface/05.gif` |
| `ui/roblox ui references/roblox-ui/references/previews/retro-user-interface/11.gif` | `05 UI and Icons/Style References/Previews/fantasy-user-interface/07.gif` |
| `ui/roblox ui references/roblox-ui/references/previews/retro-user-interface/12.gif` | `05 UI and Icons/Style References/Previews/fantasy-user-interface/11.gif` |
| `ui/roblox ui references/roblox-ui/references/previews/roblox-user-interface/01.png` | `05 UI and Icons/Style References/Previews/icons-user-interface/01.png` |
| `ui/roblox ui references/roblox-ui/references/previews/roblox-user-interface/02.png` | `05 UI and Icons/Style References/Previews/icons-user-interface/11.png` |
| `ui/roblox ui references/roblox-ui/references/previews/roblox-user-interface/09.png` | `05 UI and Icons/Style References/Previews/idle-user-interface/01.png` |
| `ui/roblox ui references/roblox-ui/references/previews/roblox-user-interface/12.png` | `05 UI and Icons/Style References/Previews/mobile-user-interface/10.png` |
| `ui/roblox ui references/roblox-ui/references/previews/space-user-interface/01.jpg` | `05 UI and Icons/Style References/Previews/buttons-user-interface/04.jpg` |
| `ui/roblox ui references/roblox-ui/references/previews/space-user-interface/02.jpg` | `05 UI and Icons/Style References/Previews/fighting-user-interface/02.jpg` |
| `ui/roblox ui references/roblox-ui/references/previews/space-user-interface/04.png` | `05 UI and Icons/Style References/Previews/shooter-user-interface/01.png` |
| `ui/roblox ui references/roblox-ui/references/previews/space-user-interface/08.png` | `05 UI and Icons/Style References/Previews/nature-user-interface/02.png` |
| `ui/roblox ui references/roblox-ui/references/previews/tycoon-user-interface/01.png` | `05 UI and Icons/Style References/Previews/icons-user-interface/11.png` |
| `ui/roblox ui references/roblox-ui/references/previews/tycoon-user-interface/02.jpg` | `05 UI and Icons/Style References/Previews/roblox-user-interface/05.jpg` |
| `ui/roblox ui references/roblox-ui/references/previews/tycoon-user-interface/03.jpg` | `05 UI and Icons/Style References/Previews/roblox-user-interface/08.jpg` |
| `ui/roblox ui references/roblox-ui/references/previews/tycoon-user-interface/04.png` | `05 UI and Icons/Style References/Previews/idle-user-interface/01.png` |
| `ui/roblox ui references/roblox-ui/references/previews/tycoon-user-interface/05.png` | `05 UI and Icons/Style References/Previews/mobile-user-interface/10.png` |
| `ui/roblox ui references/roblox-ui/references/previews/tycoon-user-interface/09.png` | `05 UI and Icons/Style References/Previews/idle-user-interface/06.png` |
| `ui/roblox ui references/roblox-ui/references/previews/tycoon-user-interface/10.png` | `05 UI and Icons/Style References/Previews/idle-user-interface/07.png` |
| `ui/roblox ui references/roblox-ui/references/previews/tycoon-user-interface/12.png` | `05 UI and Icons/Style References/Previews/idle-user-interface/12.png` |
| `ui/roblox ui references/roblox-ui/references/previews/visual-novel-user-interface/02.gif` | `05 UI and Icons/Style References/Previews/low-poly-user-interface/02.gif` |
| `ui/roblox ui references/roblox-ui/references/previews/wood-user-interface/07.png` | `05 UI and Icons/Style References/Previews/paper-user-interface/06.png` |
| `ui/roblox ui references/roblox-ui/references/ui-styles/16-garden-farm-cozy/gag-ui-3.png` | `05 UI and Icons/Style References/UI Styles/111-codes-redeem-box/gag-ui-3.png` |
| `ui/roblox ui references/roblox-ui/references/ui-styles/74-kawaii-pastel/simple-pink-3.png` | `05 UI and Icons/Style References/UI Styles/44-ios-soft/simple-pink-3.png` |
| `ui/roblox ui references/roblox-ui/references/ui-styles/85-cosmic-cartoon-space/casual-260-3.png` | `05 UI and Icons/Style References/UI Styles/10-chunky-candy-buttons/casual-260-3.png` |
| `ui/roblox ui references/roblox-ui/references/visual-refs/studs-ui/original/stud-blue-inventory.png` | `05 UI and Icons/Style References/Style Refs/studs/mockup-inventory.png` |
| `ui/roblox ui references/roblox-ui/references/visual-refs/studs-ui/original/stud-blue-leaderboard.png` | `05 UI and Icons/Style References/Style Refs/studs/mockup-leaderboard.png` |
| `ui/roblox ui references/roblox-ui/references/visual-refs/studs-ui/original/stud-blue-reward.png` | `05 UI and Icons/Style References/Style Refs/studs/mockup-reward.png` |
| `ui/roblox ui references/roblox-ui/references/visual-refs/studs-ui/original/stud-blue-settings.png` | `05 UI and Icons/Style References/Style Refs/studs/mockup-settings.png` |
| `ui/roblox ui references/roblox-ui/references/visual-refs/studs-ui/original/stud-blue-shop.png` | `05 UI and Icons/Style References/Style Refs/studs/mockup-shop.png` |
