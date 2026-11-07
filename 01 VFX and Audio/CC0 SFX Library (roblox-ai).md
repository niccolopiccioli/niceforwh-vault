---
tags: [audio, sfx, cc0, combat, roblox-ai, type/resource]
---
# CC0 SFX Library (roblox-ai)

<!-- tldr:start -->
> [!tldr] TL;DR
> - 2210 effetti sonori mp3 in 31 categorie, in 01 VFX and Audio/SFX/CC0 Library (roblox-ai)/
> - Licenza CC0 secondo il README del repo roblox-ai (non verificata file per file)
> - Copia estratta di 08 Knowledge/roblox-ai/sfx/cc0-audio (l'originale resta lì)
> - In Studio: carica l'mp3 come asset audio, poi usa rbxassetid:// in un Sound
<!-- tldr:end -->


## Categorie
| Gruppo | Categorie (file) |
|---|---|
| Combattimento | `punch` 102 · `impact-hit` 108 · `whoosh` 94 · `swoosh` 105 · `sword-slash` 88 · `sword-clash` 25 · `land-thud` 11 · `explosion` 104 · `gunshot` 102 · `reload` 119 |
| Poteri e magia | `charge-up` 13 · `power-up` 68 · `magic-spell` 109 · `laser` 112 · `teleport` 55 · `portal` 37 · `fire-burst` 11 · `level-up` 42 |
| Movimento e mondo | `jump` 104 · `footstep` 63 · `door-open` 97 · `chest-open` 15 · `unlock` 102 |
| UI e ricompense | `ui-click` 120 · `button-press` 108 · `menu-select` 60 · `notification` 129 · `error-buzz` 7 · `reward` 57 · `coin-pickup` 33 · `pickup-item` 10 |

I nomi dei file contengono la descrizione originale del suono e un hash corto (per esempio `basic-click-wooden-e50d3e8f.mp3`): cerca per parola dentro la cartella.

## Per una combo come ThunderCombo
Strati del colpo ([[Impact Frames Hitstop and Camera]], [[08 Knowledge/fwjelaa-vault/fwjelaa vault/07 Lighting VFX and Audio/Combat Sound Design and Feedback|Combat Sound Design and Feedback]]): **transiente** (`punch`, `impact-hit`) + **corpo** (`whoosh`/`swoosh` prima del contatto, `land-thud` o `explosion` sui finisher) + **colore** del potere (`charge-up`, `power-up`, `laser`, `magic-spell` per l'elettrico). Varia il pitch del 3-5% e alza di un semitono a ogni colpo della catena.

## Come portarli in Studio
1. Ascolta e scegli (in Esplora file, o in Obsidian incorporando l'mp3 in una nota: diventa riproducibile).
2. Caricalo come audio: Asset Manager → Import, o Creator Hub → Audio. Il caricamento passa la moderazione di Roblox e ha un limite mensile.
3. Usa l'ID in un `Sound` (`SoundId = "rbxassetid://<id>"`); per un gioco pubblicato l'audio deve essere tuo o pubblico.

Il server MCP di Studio ha `upload_image` solo per le immagini: per l'audio questo passo resta manuale (o API Open Cloud Assets con una chiave tua, da tenere fuori dalle chat).

## Le anteprime che c'erano già
`01-button-click`, `14-sword-swing-whoosh`, `15-sword-hit-metal`, `27-spell-cast-charge` vengono dalla Reference Library fwjelaa (stessi file della cartella `sfx/` numerata del repo).

<!-- related:start -->
## Related
[[VFX and Audio Hub]] · [[roblox-ai Reference Library]] · [[Impact Frames Hitstop and Camera]] · [[ThunderCombo - Asset IDs and Instances]]
<!-- related:end -->
