---
tags: [animation, timing, combat, hitstop, type/reference, synthesis]
---
# Combat Timing Cheat Sheet

I numeri che servono davvero per una combo. Fonti: [[Anim Research 03 - Animation Craft Numbers]] (**Dal pack**, con le sue fonti) e ThunderCombo (**Misurato**).

<!-- tldr:start -->
> [!tldr] TL;DR
> - Il contatto è uno stop netto: accelera verso il contatto, fermati, rallenta solo in uscita
> - Hitstop: M1 4-6 f, finisher 8-14 f, ultimate 15-30 f (60 fps)
> - Colpi a meno di 16 frame l'uno dall'altro si leggono come uno solo, a meno che ognuno abbia VFX/SFX propri
> - Offset della catena: root, torso +1, braccio +2, mano/arma +3, testa +2-4 frame (snappy)
> - Usa CubicV2, mai Cubic (direzione invertita tra editor e runtime)
<!-- tldr:end -->


## Regole (dal pack)
| Regola | Valore |
|---|---|
| Anticipation : recovery | snappy ~1:3-4 · weighty ~1:2 con tenuta all'estremo della carica |
| Impact flash | 1-3 frame, solo finisher e ultimate |
| Vibrazione durante l'hitstop | a terra laterale, in aria verticale; ampiezza che decade; attaccante al 30% |
| Specials: attivazione | 15-30 f, punch di FOV 70 → 55-60 in 6-10 f |
| Specials: carica | 30-90 f con tremolio ±0.02-0.05 stud o ±0.5-1° ogni 1-2 f |
| Specials: rilascio | 3-6 f verso l'estremo |
| Specials: impatto | hitstop 15-30 f + flash 2-4 f, kick di FOV +10-20, shake 0.3-0.6 stud per 15-25 f |
| R6 senza ginocchia | con le gambe aperte di ±φ abbassa il torso di `2·(1−cos φ)` (25° → 0.19, 35° → 0.36, 45° → 0.59) |
| Root motion | le animazioni non muovono l'HRP: lo spostamento vero va fatto a parte |
| Marker | `Hit` sul frame di contatto, logica dal client che riproduce la traccia |

## ThunderCombo (misurato)
| Marker | Tempo (s) | Note |
|---|---|---|
| ChargeStart → ChargeEnd | 0.05 → 1.10 | tremolio Constant ogni 1/30 s da 0.55 a 0.95 |
| Hit1 / Hit2 / Hit3 | 1.20 / 1.62 / 2.02 | 0.42 e 0.40 s tra i colpi (> 16 frame) |
| Jump → Apex → Flip → Dive → Slam | 2.50 → 2.98 → 3.06 → 3.34 → 3.50 | salto mortale in aria, slow-mo 0.25x dopo lo schianto |
| Rise → Land → End | 4.40 → 4.85 → 5.12 | dissolvenza nell'idle a LENGTH − 0.06 |
Overlap: testa +0.05 s, braccia +0.035 s, l'arto che colpisce senza ritardo. Dettagli in [[ThunderCombo - Timing and Markers]].

<!-- related:start -->
## Related
[[Animation Hub]] · [[Impact Frames Hitstop and Camera]] · [[Skill - Roblox VFX Combo]] · [[08 Knowledge/fwjelaa-vault/fwjelaa vault/47 Game Feel and Juice/Hit-Stop and Screen Shake Tuning by Numbers|Hit-Stop Tuning by Numbers (fwjelaa)]]
<!-- related:end -->
