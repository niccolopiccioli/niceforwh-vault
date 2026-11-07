---
tags: [reference, glossary, type/reference, level/beginner]
---
# Glossary - niceforwh

Termini usati in questo vault. Il glossario completo della knowledge base è [[08 Knowledge/fwjelaa-vault/fwjelaa vault/Glossary|Glossary (fwjelaa)]]; quello di animazione è [[08 Knowledge/fwjelaa-vault/fwjelaa vault/08 Animation/Animation Glossary|Animation Glossary (fwjelaa)]].

| Termine | Significato | Dove |
|---|---|---|
| **KeyframeSequence (KFS)** | L'animazione salvata come istanze (Keyframe > Pose); Moon Animator la tiene in `<Rig>.AnimSaves` | [[ThunderCombo - Timing and Markers]] |
| **KeyframeMarker** | Evento con nome su un keyframe; lo script lo ascolta con `GetMarkerReachedSignal` per far partire i VFX | [[Combat Timing Cheat Sheet]] |
| **Motor6D / Transform** | Giuntura del rig; la posa è `Part0 * C0 * Transform * C1^-1` | [[Anim Research 01 - Roblox Animation Pipeline]] |
| **Hitstop** | Freeze breve dell'animazione al contatto per dare peso; qui 0.066-0.22 s | [[Impact Frames Hitstop and Camera]] |
| **Impact frame** | 1-3 frame di grafica piatta (silhouette + linee radiali) sul colpo forte | [[Impact Frames Hitstop and Camera]] |
| **Flipbook** | Texture a griglia (2x2, 4x4, 8x8) che un ParticleEmitter anima come sprite sheet | [[Kit Emitters - Reference Sheet]] |
| **SpecialMesh** | Mesh applicata a una Part; si scala con `Mesh.Scale`, non con `Size` | [[Kit Meshes - Reference Sheet]] |
| **Superhero landing** | Posa d'atterraggio R6 a gambe aperte (±50°) con busto piegato e pugni a terra | [[ThunderCombo - Timing and Markers]] |
| **Stepped tremble** | Tremolio "anime" con pose Constant ogni 2 frame invece di interpolate | [[Combat Timing Cheat Sheet]] |
| **Progetto intatto** | Cartella con codice che dipende dai suoi percorsi: spostata intera, mai smontata | [[Tools and Pipelines Hub]] |
| **Copia estratta** | Copia di un asset preso da un progetto intatto e messa nella cartella tematica | [[riorganizzazione-log|Riorganizzazione - Log]] |
| **CC0** | Pubblico dominio: si può usare senza attribuzione | [[CC0 SFX Library (roblox-ai)]] |
| **CC BY 4.0** | Uso libero con attribuzione (qui: "Roblox Creator Documentation") | [[Roblox Docs Motion References]] |
