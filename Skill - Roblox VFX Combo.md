---
tags: [ai-skill, vfx, animation, combat, type/guide, level/intermediate]
---
# Skill - Roblox VFX Combo

**Procedura operativa** per fare una combo anime con VFX (carica → colpi → salto → schianto) con le risorse di questo vault. Nasce dall'esperimento ThunderCombo: prendine le regole e gli errori da evitare, non copiarne lo stile. È la sintesi di quello che ha funzionato davvero in Place1 (**Misurato**) e delle regole dei pack (**Dal pack**).

<!-- tldr:start -->
> [!tldr] TL;DR
> - Animazione = KeyframeSequence generata da script, con marker; i VFX partono dai marker sul client
> - Hitstop per peso 0.066 / 0.075 / 0.10 / 0.22 s (budget KB 140 ms ogni 0.6 s, superato apposta solo prima del finisher), recupero 0.08x → 1.9x, vibrazione del RootJoint.C0 ripristinata sempre
> - Emitter e mesh del kit passano dal percorso tracciato (ThunderVFX.Particles), altrimenti freeze e time scale non li fermano
> - Mesh del kit: scalare Mesh.Scale, mai Size; scala nativa enorme (0.005-0.0085 = 2-3 stud)
> - Meno è meglio: ogni layer nuovo va controllato in uno screenshot; la sovraesposizione è il primo difetto
<!-- tldr:end -->


## 1. Ordine di lavoro
1. **Timeline prima dei VFX**: anticipation → charge → release → impact → residuo → cleanup ([[VFX Method - Principles and Pipeline]]). Fissa i marker: `ChargeStart, ChargeEnd, SwingN, HitN, Jump, Apex, Slam, Rise, Land, End`.
2. **Pose**: progetta ogni posa come rotazione D nello spazio di Part0 e convertila con `Transform = C0rot^-1 * D * C0rot` (R6: x destra, y su, z indietro, il rig guarda -Z).
3. **Overlap**: ritarda testa (+0.05 s) e braccia (+0.035 s), l'arto che colpisce senza ritardo ([[Combat Timing Cheat Sheet]]).
4. **Carica a scatti**: pose `Constant` ogni 1/30 s con ampiezza crescente (ChargedPunch di fwjelaa).
5. **Schianto**: superhero landing, busto -58°, gambe ±50° nel mondo, bacino abbassato finché i piedi toccano terra (calcolalo, non a occhio).
6. **VFX sul client**: un LocalScript ascolta i marker, clona emitter e mesh da `ReplicatedStorage`, usa un orologio scalato unico per delay, tween e Debris.
7. **Verifica**: freeze (time scale 0.001) subito dopo ogni marker, screen capture, correggi, ripeti.

## 2. Ricetta per colpo (cosa ha funzionato)
| Momento | Layer | Risorsa |
|---|---|---|
| Carica | aura, spirale a terra, strisce che salgono, scintille flipbook sui pugni, fulmini a zigzag | `KSwirl`, `KRisers`, `KFlash` ([[Kit Emitters - Reference Sheet]]) |
| Colpo leggero | starburst, anello flipbook, burst piccolo, crepitio, toro sottile lungo la direzione, linee radiali + grading | `KRing`, `KBurst`, `KCrackle`, `Torus` |
| Colpo forte (calcio) | come sopra + impact frame di 2 frame (1/60 s ciascuno), guscio di distorsione, 3 ombre scure, anello di taglio rotante | `KSlashRing`, [[Impact Frames Hitstop and Camera]] |
| Schianto | impact frame di 3 frame, slow-mo 0.25x, lampo da fulmine, cratere, un solo pavimento luminoso, fumo scuro + inchiostro, due tori piatti, X-slash, contorno bianco sull'eroe | `RockCluster`, `Rubble`, `Torus`, `KPuff`, `KSmokeSpiral`, `KInkSwirl` ([[Kit Meshes - Reference Sheet]]) |

## 3. Errori già fatti (non rifarli)
- Toro a scala 10 e opaco: copre l'inquadratura → scala 4*power, trasparenza iniziale 0.45.
- Rocce a scala 0.03: la camera finisce dentro una roccia → 0.005-0.0085.
- Burst bianco + starburst + flare sul colpo leggero = blob bianco → burst piccolo e trasparente.
- Toro ciano Neon a terra + GroundRing + flash = pavimento sovraesposto → trasparenza 0.72.
- VFX fuori dal percorso tracciato non si fermano col freeze (successo nella v1).
- Il marker `End` all'ultimo frame può non scattare se la traccia si ferma a LENGTH-0.06.
- Afterimage ciano traslucide su ogni colpo = velo su tutto lo schermo: solo sui finisher, scure (v4).
- Camera dal lato sbagliato del busto: calcola dove guarda il petto al contatto prima di scegliere il lato (v4).
- Avvicinamento al colpo in ease Out = colpo molle: il segmento verso il contatto va in In (v4).

## 4. Checklist
- [ ] Marker su ogni contatto, VFX solo dai marker
- [ ] Hitstop scalato per peso, C0 ripristinato a fine stop e al reset
- [ ] Ogni emitter/mesh clonato dal percorso tracciato, distrutto con un timer sull'orologio scalato
- [ ] Mesh scalati con `Mesh.Scale`, misurati in Studio
- [ ] Screenshot di carica, ogni colpo, impact frame, schianto e tenuta
- [ ] Console senza errori nuovi; nessun accumulo di istanze tra un loop e l'altro
- [ ] `.rbxm` di terzi controllati prima di inserirli ([[Skill - Safe Asset Intake]])

## Note dietro questa skill
[[ThunderCombo - Build Log]] · [[ThunderCombo - Timing and Markers]] · [[ThunderCombo - Asset IDs and Instances]] · [[08 Knowledge/fwjelaa-vault/fwjelaa vault/07 Lighting VFX and Audio/Slash VFX Recipes - Crescent and Ring|Slash VFX Recipes (fwjelaa)]] · [[08 Knowledge/fwjelaa-vault/fwjelaa vault/47 Game Feel and Juice/Hit-Stop and Screen Shake Tuning by Numbers|Hit-Stop and Screen Shake Tuning by Numbers (fwjelaa)]] · [[08 Knowledge/fwjelaa-vault/fwjelaa vault/08 Animation/05 Systems/VFX Timing with Animation|VFX Timing with Animation (fwjelaa)]]

<!-- related:start -->
## Related
[[VFX and Audio Hub]] · [[Animation Hub]] · [[ThunderCombo Hub]] · [[Skill - Safe Asset Intake]]
<!-- related:end -->
