---
tags: [vfx, hitstop, impact-frame, camera, game-feel, type/guide, synthesis]
---
# Impact Frames Hitstop and Camera

Sintesi tra l'animation pack (research 03), le note di game feel della knowledge base fwjelaa e ThunderCombo.

<!-- tldr:start -->
> [!tldr] TL;DR
> - Hitstop per peso: leggero 4-6 frame, finisher 8-14, ultimate 15-30 (Dal pack); in ThunderCombo v4 0.066/0.075/0.10/0.22 s (Misurato)
> - Durante il freeze il corpo vibra di lato e la vibrazione decade
> - Impact frame: 1-2 frame (3 sugli ultimate), solo su finisher e ultimate; in ThunderCombo v4 A inchiostro → B invertito (→ C viola sullo schianto), 1/60 s ciascuno
> - Il flash bianco va DOPO l'impact frame, altrimenti lo lava
> - Camera: shot a orbita interpolati in tempo reale, push-in, dutch, punch di FOV, shake Perlin, slow-mo 0.25x sullo schianto, tagli netti sui colpi
<!-- tldr:end -->


## 1. Hitstop
| Fonte | Valori |
|---|---|
| Capcom (esempio) | leggero / medio / pesante = 8 / 12 / 16 frame |
| KOF XIII | 7 leggero, 11 pesante |
| Smash Ultimate | circa 0.65 × danno + 6, massimo 30 |
| Animation pack (scelta) | M1 4-6 f, finisher 8-14 f, ultimate 15-30 f |
| Hit-Stop Tuning by Numbers (KB) | stop = 0.03 + 0.045 × forza; max 140 ms ogni 0.6 s; sotto ~66 ms sfarfalla a 30 fps |
| **ThunderCombo v4** | Hit1 0.066 s · Hit2 0.075 s · Hit3 0.10 s · Slam 0.22 s (Hit2→Hit3 supera il budget KB di proposito), con recupero 0.08x → 1.9x; vibrazione `RootJoint.C0` di ampiezza 0.05 / 0.1 / 0.14 che decade, ripristinata a fine stop e al reset |

## 2. Impact frame
ViewportFrame con la silhouette del rig + 46 linee radiali (UIGradient):
- **A** sfondo inchiostro, silhouette bianca, linee ciano;
- **B** sfondo bianco, silhouette inchiostro, linee viola (dopo 1/60 s);
- **C** solo sullo schianto: sfondo viola scuro, silhouette ciano, linee bianche;
- ogni modo dura 1/60 s reale, cioè 1 frame a 60 fps (anche in slow-mo), poi un flash bianco al 45% che sfuma;
- la camera della silhouette è la camera di gioco e le linee convergono sul punto d'impatto (v4).

![[09 ThunderCombo/Screenshots/v4/4_impact_frame_calcio_A.jpg|520]]
Colpo leggero: solo linee + grading (saturazione −1, contrasto 0.9) per 0.06 s.

![[09 ThunderCombo/Screenshots/v3/3_impact_frame_invertito_B.jpg|520]]

## 3. Camera
Shot definiti come offset (yaw, distanza, altezza) e interpolati a orbita, così la camera non passa dentro il rig. v4: HERO (push-in FOV 40 sulla carica) → ESTABLISH (taglio frontale 3/4) → un taglio netto per colpo, ognuno da un lato diverso e scelto in base a dove si apre il busto → RETURN. Dutch max 7°, kick di FOV a metà stop, shake a trauma (decade 1.45/s, shake = trauma², 16 Hz, 2.6° scalati con tan(FOV/2)/tan(35°)), slow-mo 0.25x sullo schianto (tenuta 0.3 s, rientro 0.25 s).

## Nella knowledge base fwjelaa
[[08 Knowledge/fwjelaa-vault/fwjelaa vault/47 Game Feel and Juice/Hit-Stop and Screen Shake Tuning by Numbers|Hit-Stop and Screen Shake Tuning by Numbers]] · [[08 Knowledge/fwjelaa-vault/fwjelaa vault/52 Core Concepts/Hit-Stop|Hit-Stop]] · [[08 Knowledge/fwjelaa-vault/fwjelaa vault/57 API and Concept Atlas/Impact Frames|Impact Frames]] · [[08 Knowledge/fwjelaa-vault/fwjelaa vault/08 Animation/05 Systems/Camera Shake and Camera FX|Camera Shake and Camera FX]] · [[08 Knowledge/fwjelaa-vault/fwjelaa vault/08 Animation/05 Systems/Hit Reactions Stagger and Hit-Stop|Hit Reactions Stagger and Hit-Stop]] · [[08 Knowledge/fwjelaa-vault/fwjelaa vault/07 Lighting VFX and Audio/Screen Damage Effects - Hit Flash, Low-Health Vignette and Blur|Screen Damage Effects]] · [[08 Knowledge/fwjelaa-vault/fwjelaa vault/58 Player QoL and Game Tweaks/Comfort Toggles - Flashes Damage Numbers and Hit-Stop|Comfort Toggles (flash e hitstop)]]

<!-- related:start -->
## Related
[[Skill - Roblox VFX Combo]] · [[Combat Timing Cheat Sheet]] · [[ThunderCombo - Timing and Markers]] · [[VFX Reference Images]]
<!-- related:end -->
