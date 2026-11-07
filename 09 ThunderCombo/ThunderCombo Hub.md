---
tags: [hub, project, thundercombo, type/hub]
---
# ThunderCombo Hub

> [!note] Esperimento
> ThunderCombo è un esperimento fatto in Place1 per provare le risorse del vault: utile come caso di studio (cosa ha funzionato, errori da non rifare), **non** è il modello da seguire. Per lavorare parti dal metodo generale: [[VFX Method - Principles and Pipeline]], [[Kit Emitters - Reference Sheet]], [[Combat Timing Cheat Sheet]], [[Impact Frames Hitstop and Camera]].

Combo anime elettrica sul rig R6 `Workspace.TemplateR6` di **Place1**: carica, tre colpi (diretto, montante, calcio circolare), salto, salto mortale in aria, picchiata e schianto con cratere. Animazione in KeyframeSequence (formato Moon Animator) + VFX client-side sincronizzati con i marker. Quattro versioni (v1 → v4); la v4 applica i principi della knowledge base di questo vault.

![[09 ThunderCombo/Screenshots/v4/5_calcio_profilo.jpg|560]]

## Note
- [[ThunderCombo - Build Log]]: cosa è stato fatto in v1-v4, i problemi risolti e da quale nota viene ogni scelta della v4
- [[ThunderCombo - Timing and Markers]]: marker, pose, overlap, hitstop, camera
- [[ThunderCombo - Asset IDs and Instances]]: istanze in Place1, ID di texture, mesh e suoni
- [[ThunderCombo - Screenshots]]: galleria v1-v4 (con il confronto v3 → v4)
- Procedura riutilizzabile: [[Skill - Roblox VFX Combo]]

> [!warning] Salvataggio e pubblicazione
> Place1 è il file `Desktop/nicco/anim/Place1.rbxl` (ultimo salvataggio con la v4: 2026-11-06 12:03). Dopo ogni modifica in Studio serve **Ctrl+S**. Per un gioco pubblicato servono `AnimationId` / `IdleAnimationId` caricati (la registrazione a runtime funziona solo in Studio).

<!-- related:start -->
## Related
[[VFX and Audio Hub]] · [[Animation Hub]] · [[Kit Emitters - Reference Sheet]]
<!-- related:end -->
