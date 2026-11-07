---
tags: [animation, tool, pack, type/resource]
---
# fwjelaa Animation Pack

<!-- tldr:start -->
> [!tldr] TL;DR
> - Progetto intatto: 07 Tools and Pipelines/Roblox-Animations-by-fwjelaa
> - Genera animazioni R6/R15 da una clip o da una descrizione, con Blender + Studio via MCP (skill make-anim)
> - Le 41 animazioni generate sono in anims/*.py (sorgente) e out/*.rbxmx (pronte, copiate in 06 Studio Kits/Animations)
> - Non eseguito niente; usate solo le research e i numeri di timing e posa
<!-- tldr:end -->


## Cos'è
Dal suo README: "Tell Claude the move and get back a finished Roblox animation (R6 or R15)". Il flusso: clip di riferimento → animazione in Blender → confronto frame per frame → caricamento in Studio → import in Moon Animator 2 o pubblicazione. Metodo di fwjelaa (FWJ STUDIOS), da accreditare (`CREDITS.md`).

## Dove sta
| Cosa | Percorso |
|---|---|
| Progetto | `07 Tools and Pipelines/Roblox-Animations-by-fwjelaa/` (README, GUIDE, `anims/`, `kit/`, `roblox/AnimKit.luau`, `out/`) |
| Research (copie) | `02 Animation/Research/` |
| Riferimento PunchRef (copia) | `02 Animation/References/PunchRef/` |
| Animazioni pronte (copie) | `06 Studio Kits/Animations/R6` e `R15` |

## Cosa è stato preso per ThunderCombo
- carica tremolante a scatti da `R6_ChargedPunch` (pose costanti ogni 2 frame, ampiezza crescente);
- posa superhero landing da `R6_GroundSlam` (busto ~−60°, gambe divaricate, abbassamento R6 `2·(1−cos φ)`);
- hitstop per peso e regole di overlap da `research/03-animation-craft.md` ([[Combat Timing Cheat Sheet]]).

## Sicurezza
Contiene `.py`, `CLAUDE.md`, `.claude/skills/make-anim` e `.secrets/` (solo un `README.txt`, posto per una chiave API opzionale). Niente eseguito; i `.md` letti come riferimento.

<!-- related:start -->
## Related
[[Animation Hub]] · [[Tools and Pipelines Hub]] · [[Studio Kits Hub]] · [[08 Knowledge/fwjelaa-vault/fwjelaa vault/70 fwjelaa Packs/make-anim|make-anim (fwjelaa)]]
<!-- related:end -->
