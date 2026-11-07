---
tags: [vfx, method, principles, type/guide, synthesis]
---
# VFX Method - Principles and Pipeline

Sintesi di tre fonti: il prompt **"fwjelaa vfx method"** (copia in `01 VFX and Audio/Sources/`, ed è anche in [[08 Knowledge/fwjelaa-vault/fwjelaa vault/70 fwjelaa Packs/VFX/fwjelaa vfx method|70 fwjelaa Packs/VFX]]), le note VFX della knowledge base fwjelaa, e quello che si è visto costruendo ThunderCombo.

> [!warning] Il prompt originale è una direttiva per un'AI
> Chiede di fare un audit di "VFX Forge v2.4.0-rc1", scrivere un corso "ROBLOX VFX FROM DUMMIES TO MASTER", costruire 5 demo e salvare tutto nel progetto. **Non è stato eseguito.** Qui ne restano solo i principi.

<!-- tldr:start -->
> [!tldr] TL;DR
> - Timeline: anticipation → charge → release → impact → residuo → cleanup
> - Scegli la tecnologia per componente: particelle, beam, trail, mesh, texture, tween, post-processing, UI
> - Più particelle non vuol dire meglio; più luminoso non vuol dire meglio
> - Mai istanze temporanee che restano vive, mai connessioni RunService senza limite
> - Non dichiarare test o verifiche visive mai fatti
<!-- tldr:end -->


## 1. Il processo in 7 passi (dal prompt)
1. Interpreta: identità visiva, intensità, scala, scopo nel gameplay.
2. Scomponi l'effetto in componenti (mesh, particelle, beam, luce, camera...).
3. Scegli la tecnologia giusta per ciascuno, senza forzare tutto nei ParticleEmitter.
4. Disegna la timeline (combat: anticipation → charge → release → impact → residuo → cleanup; aure: attivazione → formazione → loop → risposta al movimento → disattivazione).
5. Implementa.
6. Testa in Studio: aspetto, allineamento, timing, leggibilità, performance, rete, camera, pulizia.
7. Rifinisci: non fermarti al primo risultato che funziona.

## 2. Livelli di intensità
Tier 1 minimale · Tier 2 standard · Tier 3 avanzato (texture custom, geometria in movimento) · Tier 4 elite · Tier 5 cinematico (multi-fase, ambiente, camera). ThunderCombo è un Tier 4-5.

## 3. Come si è tradotto in ThunderCombo (Misurato)
| Principio | Applicazione |
|---|---|
| Composizione deliberata | ogni colpo ha 3 toni: bordo bianco, corpo ciano/viola, inchiostro scuro ([[Kit Emitters - Reference Sheet]]) |
| Brighter ≠ better | tre giri di correzione della sovraesposizione (burst, toro, puff) |
| Cleanup | un orologio scalato unico (delay, tween, Debris); reset che svuota tutto; verifica dell'accumulo su due loop |
| Leggibilità a velocità piena | impact frame di 2 frame reali (3 sullo schianto), hitstop scalato per peso ([[Impact Frames Hitstop and Camera]]) |

## Nella knowledge base fwjelaa
[[08 Knowledge/fwjelaa-vault/fwjelaa vault/07 Lighting VFX and Audio/VFX Design Playbook|VFX Design Playbook]] · [[08 Knowledge/fwjelaa-vault/fwjelaa vault/07 Lighting VFX and Audio/VFX Readability and Value - Lessons from Blind Reviews|VFX Readability and Value]] · [[08 Knowledge/fwjelaa-vault/fwjelaa vault/07 Lighting VFX and Audio/VFX Performance Budgets and Culling|VFX Performance Budgets and Culling]] · [[08 Knowledge/fwjelaa-vault/fwjelaa vault/07 Lighting VFX and Audio/Replicating VFX - Server Validates, Clients Render|Replicating VFX]] · [[08 Knowledge/fwjelaa-vault/fwjelaa vault/07 Lighting VFX and Audio/Designing VFX Textures and Flipbooks in Figma|Designing VFX Textures and Flipbooks]]

<!-- related:start -->
## Related
[[VFX and Audio Hub]] · [[Skill - Roblox VFX Combo]] · [[Impact Frames Hitstop and Camera]]
<!-- related:end -->
