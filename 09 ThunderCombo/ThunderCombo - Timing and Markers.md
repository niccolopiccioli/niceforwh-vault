---
tags: [project, thundercombo, timing, animation, type/reference]
---
# ThunderCombo - Timing and Markers

## Marker (KFS v4, 5.15 s, Priority Action4)
| Marker | s | Cosa succede | Camera |
|---|---|---|---|
| ChargeStart | 0.05 | aura, spirale a terra, strisce, scintille flipbook sui pugni, fulmini | HERO: push-in FOV 40, poi a 0.85 taglio frontale 3/4 |
| ChargeEnd | 1.10 | sfera di energia, starburst, anello, lampo da fulmine, scarica; trail accesi | |
| Swing1 / Hit1 | 1.12 / 1.20 | scia bianca sul pugno, mezzaluna; diretto: hitstop 0.066 s | taglio fronte-sinistra (-11, 0.6, -6) FOV 50 |
| Swing2 / Hit2 | 1.53 / 1.62 | montante: hitstop 0.075 s, +1 semitono | taglio dal basso fronte-destra (6.5, -1.8, -8.5) |
| Swing3 / Hit3 | 1.90 / 2.02 | scia viola sul piede; calcio: impact frame A→B, hitstop 0.10 s, guscio di distorsione, 3 ombre scure, anelli di taglio | taglio di profilo (-12, 0.8, -3), poi RETURN |
| Jump | 2.50 | fumo, anello a terra, pilastro | taglio basso largo FOV 64 |
| Apex | 2.98 | nucleo d'energia tra le mani, fulmini | |
| Flip | 3.06 | salto mortale raccolto; il nucleo si rimpicciolisce, 2 scie viola | taglio laterale (-8, -0.5, -4) |
| Dive | 3.34 | fulmine dal corpo al suolo, scia, ombre scure | taglio dall'alto (5, 8, -10) |
| Slam | 3.50 | slow-mo 0.25x, impact frame A→B→C, lampo, hitstop 0.22 s, cratere, tori, guscio, fumo scuro, X-slash, contorno bianco | taglio 3/4 sopra il bordo del cratere, poi deriva lenta |
| Rise / Land / End | 4.40 / 4.85 / 5.12 | ritorno, atterraggio, dissolvenza nell'idle | RETURN largo |

## Pose (gradi; R = {x, y, z, rx, ry, rz} del busto)
- Stance: root {0, −0.35, 0, −8, −22, 0}, testa {6, 16, 0}, braccio dx {70, 25, 0}, sx {82, −25, 0}, gamba dx {−20, 0, 8}, sx {25, 0, −5}.
- Diretto 1.20: busto ry 44, braccio dx {94, −44, 0} + stretch (−0.22, 0, −0.42); overshoot a 1.245.
- Montante 1.52 → 1.575 → 1.62: abbassamento a y −0.78, arco, braccio sx {130, 18, −8} + stretch (0, 0.42, −0.12).
- Calcio 1.90 (camera del ginocchio {78, 0, 38}) → 1.965 → 2.02 {44, 0, 86} + stretch (0.38, 0.18, 0): il piede arriva avanti all'altezza della testa, busto di profilo verso −X.
- Salto mortale 3.06 → 3.36: rx −40 → −130 → −220 → −310 → −345 (raccolto, gambe 112°), poi −418 (= −58) all'atterraggio.
- Atterraggio 3.50 / 3.60 / 4.05: busto −58 / −62 / −54°, testa 30-48° (sguardo avanti), braccio dx a terra {60, 10, 0}, sx aperto dietro {−30, −10, −40}; piedi a 0.21 stud, pugno a 0.74 stud dal suolo.
- Overlap: testa +0.05 s, braccia +0.035 s, l'arto che colpisce senza ritardo. Easing CubicV2 (mai Cubic); segmento verso il contatto in **In**.

## Tempo
- Attributo `workspace.ThunderTimeScale` × slow-mo interno = scala del tempo (0.001 = freeze per gli screenshot).
- Hitstop con recupero: 0.08x per la durata dello stop, poi 1.9x per la stessa durata.
- Tasti in Play: R = replay, C = camera cinematica on/off.
