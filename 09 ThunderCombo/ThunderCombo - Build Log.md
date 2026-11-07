---
tags: [project, thundercombo, log, type/case-study]
---
# ThunderCombo - Build Log

## v1: da zero
- KFS `ThunderCombo` (29 keyframe, 4.6 s) generata da script: posa progettata come rotazione D nello spazio di Part0, convertita con `Transform = C0rot^-1 * D * C0rot`.
- VFX in `ReplicatedStorage.ThunderVFX` (solo texture `rbxasset://` incluse in Studio), LocalScript con camera cinematica, hitstop, impact frame, afterimage, fulmini a zigzag, cratere.
- Disattivato il vecchio `StarterPlayerScripts.Client` (KatanaFX), su richiesta dell'utente.
- **Problema**: negli screenshot i VFX mancavano perché Debris e tween girano in tempo reale durante il freeze. **Fix**: orologio scalato unico (`doom`), tween in pausa, tabella di emitter non weak.

## v2: "1000x più figo", più fluido
- KFS rigenerata: 94 keyframe, 4.9 s, overlap (testa +0.05, braccia +0.035), breakdown, overshoot; nuova `ThunderIdle` (respiro, loop di 2 s) e dissolvenza combo → idle.
- Impact frame A/B/C con silhouette in ViewportFrame + 46 linee radiali; camera a orbita interpolata, push-in, dutch, punch di FOV, slow-mo 0.28x.
- Crescent slash a Beam, starburst, ink spikes, X-slash con schegge, post-processing proprio (bloom, blur, DOF).

## v3: con le risorse del vault
- Kit PDS letto offline (4 script puliti), 34 emitter ricreati, 10 ricolorati; mesh del kit (rocce, macerie, toro). Vedi [[Kit Emitters - Reference Sheet]] e [[Kit Meshes - Reference Sheet]].
- Animazione: carica a scatti (pose Constant ogni 1/30 s), schianto superhero landing calcolato. Hitstop per peso + vibrazione del RootJoint.C0; cratere di mesh roccia.
- Difetti trovati riguardando la v3 (screenshot `v3/7_calcio_base_v3`, `v3/8_posa_schianto_base_v3`): calcio visto di scorcio, posa finale sepolta tra rocce e pavimento ciano, avvicinamento ai colpi in decelerazione (ease Out *verso* il contatto), afterimage ciano traslucide che velavano lo schermo.

## v4: la knowledge base come regolamento
Backup v3 in `ServerStorage.ThunderCombo_v3_KFS_backup`. KFS v4: 138 keyframe, 5.15 s; idle di 4 s.

| Cambio | Da quale nota |
|---|---|
| Accelerazione **dentro** il contatto (ease In sul segmento che porta al colpo), stop netto, uscita in Out | [[08 Knowledge/fwjelaa-vault/fwjelaa vault/08 Animation/03 Authoring/Combat Animation Craft|Combat Animation Craft]]; [[Anim Research 03 - Animation Craft Numbers]] §0.1 |
| "Stretch" di 1-2 frame: l'arto che colpisce trasla di 0.4 stud lungo la sua direzione (R6 non scala i Motor6D) | [[Anim Research 03 - Animation Craft Numbers]] §5.8 |
| Breakdown ad arco su montante e calcio, camera del calcio (ginocchio alto), anticipazione più profonda per il salto | Research 03 §5.5; [[08 Knowledge/fwjelaa-vault/fwjelaa vault/08 Animation/03 Authoring/Spin and Whole-Body Rotation Moves|Spin and Whole-Body Rotation Moves]] |
| Nuovo: salto mortale raccolto in aria + picchiata (marker `Flip`, `Dive`), chiavi ogni ≤90° di rotazione | Spin and Whole-Body Rotation Moves |
| Posa d'atterraggio asimmetrica: un pugno a terra, l'altro braccio aperto dietro, sguardo avanti | Research 03 §5.7 (leggibilità della posa) |
| Idle di 4 s: respiro (2 s) + spostamento del peso (4 s) + micro-sguardi; testa e braccia in ritardo | [[08 Knowledge/fwjelaa-vault/fwjelaa vault/08 Animation/03 Authoring/Idle Breathing and Secondary Motion|Idle Breathing and Secondary Motion]] |
| Hitstop 0.066 / 0.075 / 0.10 / 0.22 s con recupero 0.08x → 1.9x, così marker e VFX restano in sync. Hit1→Hit2 sta nel budget KB (141 ms in 0.6 s); Hit2→Hit3 lo supera di proposito (175 ms in 0.4 s) per dare peso al finisher, come il finisher più lungo di Research 03 | [[08 Knowledge/fwjelaa-vault/fwjelaa vault/47 Game Feel and Juice/Hit-Stop and Screen Shake Tuning by Numbers|Hit-Stop Tuning by Numbers]]; Research 03 §7.3 |
| Shake a "trauma" (decade 1.45/s, shake = trauma², 16 Hz, 2.6° scalati con la FOV, roll max 4°), parte al rilascio dello stop; kick di FOV a metà stop | [[08 Knowledge/fwjelaa-vault/fwjelaa vault/08 Animation/05 Systems/Camera Shake and Camera FX|Camera Shake and Camera FX]] |
| Impact frame: 1 frame per modo a 60 fps (1/60 s reale), quindi A→B = 2 frame sul calcio e A→B→C = 3 sullo schianto; colori della palette, linee che convergono sul punto d'impatto | [[08 Knowledge/fwjelaa-vault/fwjelaa vault/57 API and Concept Atlas/Impact Frames|Impact Frames]]; Camera Shake and Camera FX |
| Montaggio: HERO (push-in) → ESTABLISH → taglio netto su ogni colpo con un'inquadratura diversa → RETURN; dutch max 7°; slow-mo 0.25x per 0.3 s | [[08 Knowledge/fwjelaa-vault/fwjelaa vault/08 Animation/05 Systems/Cinematic Ultimates|Cinematic Ultimates]] |
| Impatto in 6 fasi: hot frame bianco < 0.1 s, corpo (anello, toro, burst), secondario (scintille, crepitio, schegge scure), terra, coda | [[08 Knowledge/fwjelaa-vault/fwjelaa vault/07 Lighting VFX and Audio/VFX Design Playbook|VFX Design Playbook]] §1 |
| Ogni pila luminosa ha uno strato scuro (schegge e ombre inchiostro), un solo pavimento luminoso alla volta, niente sfere giganti | [[08 Knowledge/fwjelaa-vault/fwjelaa vault/07 Lighting VFX and Audio/VFX Readability and Value - Lessons from Blind Reviews|VFX Readability and Value]]; [[08 Knowledge/fwjelaa-vault/fwjelaa vault/07 Lighting VFX and Audio/Escalation and Grandeur Without Clutter|Escalation and Grandeur]] |
| Afterimage solo sui finisher: 3 ombre scure 0.035 s l'una dall'altra; scie (smear) sugli arti durante gli swing | [[08 Knowledge/fwjelaa-vault/fwjelaa vault/08 Animation/05 Systems/VFX Timing with Animation|VFX Timing with Animation]] |
| Bloom "toon arena": intensità 1, size 40, soglia 1.6 (brilla solo il VFX), luci brevi sopra e dietro il colpo | [[08 Knowledge/fwjelaa-vault/fwjelaa vault/07 Lighting VFX and Audio/Stylized Lighting Recipes|Stylized Lighting Recipes]] §3.2; VFX Readability §6 |
| Lampo da fulmine a 4 colpi (0 / 0.05 / 0.10 / 0.18 s) su ChargeEnd e schianto | [[08 Knowledge/fwjelaa-vault/fwjelaa vault/07 Lighting VFX and Audio/Lightning Strikes and Thunder - Procedural Bolts and Sound Delay|Lightning Strikes and Thunder]] |
| Audio a strati: transiente + scarica elettrica + corpo (+ tuono sui finisher), +1 semitono per colpo, ±4% di pitch | [[08 Knowledge/fwjelaa-vault/fwjelaa vault/07 Lighting VFX and Audio/Combat Sound Design and Feedback|Combat Sound Design and Feedback]] |
| Contorno bianco (Highlight AlwaysOnTop) sulla posa tenuta, camera sopra il bordo del cratere | VFX Readability (leggibilità della sagoma) |
| Guscio ForceField che si espande = distorsione sui colpi forti e sullo schianto | scelta propria (Roblox non ha distorsione) |

### Lezioni (Misurate durante la v4)
- **Camera dal lato verso cui si apre il busto**: al contatto del diretto il busto ruota di 44°; la camera a destra vedeva la schiena. Prima di scegliere l'inquadratura calcolare direzione del busto e dell'arto (script che legge le CFrame), poi mettere la camera perpendicolare all'arto, dal lato del petto.
- **Le afterimage al Neon traslucide sono il primo colpevole del "velo"**: vicino alla camera diventano pannelli enormi. Solo sui finisher, scure, poche.
- **Un evento di un marker può cadere nel momento di un altro**: le 4 afterimage dell'`Apex` finivano proprio sul salto mortale e lo trasformavano in un blob.
- **Il taglio va applicato subito** (`updateCamera(0)` dopo `cut`), altrimenti la silhouette dell'impact frame usa l'inquadratura precedente.
- **Anteprima delle pose in Edit**: `Motor6D.Transform` non si vede in Edit; copiare temporaneamente `C0 * Transform` in `C0` e ripristinare.
- Verifiche: console senza errori nuovi (solo il vecchio 203785492), tutti i suoni "Success", `ThunderFX_Live` stabile a 64 istanze tra un loop e l'altro, RootJoint.C0 ripristinato, velocità della traccia tornata a 1.

Note di sessione originali: `side-session-notes/.../thundercombo.md` (fuori dal vault).
