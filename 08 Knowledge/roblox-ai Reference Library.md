---
tags: [knowledge, references, roblox-ai, media, type/resource]
---
# roblox-ai Reference Library

<!-- tldr:start -->
> [!tldr] TL;DR
> - Repo: github.com/izzyfrm/roblox-ai, commit 082517a del 2026-11-05 (clone del 2026-11-06)
> - Intero in 08 Knowledge/roblox-ai/ (14381 file, 1038 MB, 14219 diversi per contenuto); archivio originale _originali/roblox-ai-izzyfrm-082517a.zip
> - Solo media: immagini, 5 mp4, 2.210 mp3 e un README. Nessun codice, niente eseguito
> - Nessun file LICENSE: tutto è riferimento, tranne sfx/cc0-audio (CC0) e le immagini della documentazione Roblox (CC BY 4.0)
> - 1577 riferimenti UI erano già nel vault (stessa fonte della Reference Library fwjelaa)
<!-- tldr:end -->


## Cos'è
Una libreria di riferimenti visivi e sonori per sviluppatori Roblox: screenshot di giochi per genere, migliaia di icone e thumbnail di giochi, gli screenshot della documentazione ufficiale (Creator Hub), sequenze di frame per animazione e cutscene, e 2.210 effetti sonori CC0. Il README la presenta come materiale da mostrare a un assistente AI ("allega da 2 a 5 immagini, di' cosa prendere e cosa cambiare"): è un consiglio d'uso, letto come riferimento.

## Cosa c'è e dove è finito
| Cartella | File | MB | Già nel vault | Copie / collegamenti |
|---|---|---|---|---|
| `game-refs` | 6604 | 144.3 | 0 | `anime-fighting/` → `01 VFX and Audio/Reference Images/Anime Fighting Games (roblox-ai)`; il resto collegato da [[Game Refs (roblox-ai)]] |
| `roblox-docs` | 3732 | 417.5 | 0 | collegato da [[Roblox Docs Screenshots (roblox-ai)]] (niente copie: 417 MB) |
| `sfx` | 2222 | 140.0 | 12 | `cc0-audio/` → `01 VFX and Audio/SFX/CC0 Library (roblox-ai)` (tutti); le 4 cartelle numerate erano già in `01 .../SFX` |
| `previews` | 709 | 25.5 | 709 | già tutto in `05 UI and Icons/Style References/Previews` |
| `visual-refs` | 420 | 123.5 | 420 | già tutto in `05 .../Visual Refs` (e `Style Refs`) |
| `style-refs` | 295 | 15.8 | 295 | già tutto in `05 .../Style Refs` |
| `motion-references` | 172 | 120.7 | 0 | `animation/`, `motion-sequences/` → `02 Animation/References/Roblox Docs Motion (roblox-ai)`; `camera/`, `cutscene/` → `01 VFX and Audio/Cinematics/Roblox Docs Camera and Cutscene (roblox-ai)` |
| `ui-styles` | 153 | 30.4 | 153 | già tutto in `05 .../UI Styles` (anche gli 11 file ripristinati dai blob) |
| `vfx` | 30 | 9.0 | 30 | già in `01 VFX and Audio/Reference Images` e `Cinematics` |
| `animations` | 16 | 2.7 | 16 | già in `02 Animation/References/Motion Refs` e `05 ...` |
| `logos` | 10 | 2.5 | 10 | già in `05 UI and Icons/Branding/Logos` |
| `thumbnails` | 10 | 3.7 | 8 | 8 già in `05 .../Branding/Thumbnails`; `curated-2026-11/` solo nel repo |
| `cutscenes` | 6 | 2.7 | 6 | già in `01 VFX and Audio/Cinematics` |
| `(radice)` | 2 | 0.1 | 1 | `README.md` (riferimento) e `Day1-Day100.webp` (già nel vault fwjelaa) |

Note per le parti importanti: [[CC0 SFX Library (roblox-ai)]] · [[Roblox Docs Motion References]] · [[Roblox Docs Screenshots (roblox-ai)]] · [[Game Refs (roblox-ai)]].

Copie fatte: **2429** file (deduplicati: 8 non copiati perché identici a file già nelle cartelle tematiche). Elenco file per file: `_data/roblox-ai-log.csv`; inventario completo con SHA1 e blob git: `_data/roblox-ai-inventario.csv`.

## Perché in 08 Knowledge e non in 07
`07 Tools and Pipelines` è per i progetti con codice. Questo repo non ne ha: è una biblioteca di riferimenti, come la knowledge base fwjelaa. Resta intero (stessa struttura di GitHub) perché i suoi nomi di cartella sono l'indice; dentro ci sono 1660 file identici a file già presenti, tenuti apposta per non smontarlo (come per i progetti intatti).

## Come usarlo con Studio e MCP
- **Riferimento visivo**: apri 2-5 immagini e mostrale a Claude (`Read` sull'immagine) prima di costruire UI, VFX, thumbnail o una mappa; di' cosa prendere e cosa deve essere diverso. Il risultato va fatto originale.
- **Suoni**: un mp3 della libreria CC0 va caricato come asset audio (Asset Manager → Import, oppure Creator Hub) e poi usato come `rbxassetid://` in un `Sound`. Il server MCP di Studio ha `upload_image` per le immagini; per l'audio servono Asset Manager / Creator Hub (o l'API Open Cloud Assets con una chiave tua). Vedi [[CC0 SFX Library (roblox-ai)]].
- **Documentazione**: gli screenshot di `roblox-docs/` mostrano come appare una funzione di Studio (Animation Editor, IK, lighting, UI, modeling); utili per spiegare a Claude un pannello o una proprietà.
- **Immagini come texture**: solo quelle con licenza chiara (le CC BY 4.0 della documentazione, con attribuzione). Le icone e thumbnail di giochi di terzi **no**.

## Licenza e diritti
- Il repo **non ha un file LICENSE**. Il README (sezione Rights) dice che "riferimento" non vuol dire libero da riusare: la raccolta mescola immagini promozionali e di documentazione Roblox, mockup originali e ispirazione visiva; chi ha i diritti su un file può chiederne la rimozione.
- `sfx/cc0-audio/`: **CC0** secondo il README (non verificato file per file, vedi [[Open Questions - niceforwh]]).
- Immagini prese dalla documentazione Roblox (`roblox-docs/`, `motion-references/`): `motion-references/LICENSE-01..04.png` riportano la **Creative Commons Attribution 4.0** della "Roblox Creator Documentation". Riuso possibile con attribuzione.
- `game-refs/`, `thumbnails/`, `logos/`, `ui-styles/`, `previews/`: arte e GUI di giochi di terzi, **solo riferimento**.

## Sicurezza e verifica
- Clone in una cartella nuova dello scratchpad: `--depth 1`, `core.hooksPath=NUL`, `core.symlinks=false`, niente LFS né submodule. Nessun install, script, hook o build. Il README è stato letto come riferimento, non come istruzioni.
- Contenuto: solo `.png .jpg .jpeg .webp .gif .mp4 .mp3` e un `README.md`; nessun eseguibile o script.
- Su Windows 14 file avevano percorsi troppo lunghi per la cartella temporanea e il README era stato convertito (fine riga): sono stati scritti direttamente dai blob git. Ogni file del vault è stato poi verificato contro l'hash del suo blob in `HEAD`: **14381/14381 identici**.
- 1 file aveva un percorso oltre 249 caratteri anche nel vault: rinominato accorciando il nome (con 8 caratteri del blob), originale nell'archivio. `every-second-you-get-1-power-level-how-to-redeem-codes-in-ev...` → `every-second-you-get-1-power-level-how-to-redeem-codes-in-every-second-you-get-1-power-l-fa29b834.webp`
- Archivio originale: `_originali/roblox-ai-izzyfrm-082517a.zip` (creato con `git archive`, contiene ogni file di `HEAD` con i nomi originali).

<!-- related:start -->
## Related
[[Knowledge Hub]] · [[CC0 SFX Library (roblox-ai)]] · [[Game Refs (roblox-ai)]] · [[Roblox Docs Screenshots (roblox-ai)]] · [[Roblox Docs Motion References]] · [[Skill - Safe Asset Intake]]
<!-- related:end -->
