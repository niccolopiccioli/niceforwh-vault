---
tags: [vfx, particles, meshes, kit, rbxm, type/resource]
---
# PDS Particles and Models Kit

<!-- tldr:start -->
> [!tldr] TL;DR
> - File: 06 Studio Kits/VFX/PDS Particles and Models Kit.rbxm (222 KB)
> - Contiene 34 ParticleEmitter (Pigs Particle Pack V5 + preset "Ore"), ~70 mesh, una mappa da 11k Part, 4 Script
> - Gli script sono puliti ma il file non è mai stato inserito: gli emitter sono stati ricreati in Studio dalle proprietà
> - In Place1: ReplicatedStorage.ThunderVFX.Kit (34) + 10 emitter ricolorati in ThunderVFX.Particles
<!-- tldr:end -->


## Cos'è
Un kit di terzi ("PDS' Particles & Models Kit", con dentro "Pigs Particle Pack V5" e una cartella "PDS Models Pack for BSED"). Classi trovate leggendo il file offline: Part 11.388, Model 2.269, Decal 2.228, MeshPart 98, ParticleEmitter 34, Script 4, più SurfaceGui, Highlight, constraint e valori.

## Dove sta
- File: `06 Studio Kits/VFX/PDS Particles and Models Kit.rbxm`
- Originale: `_originali/particle and model kit.rbxm`
- Dati estratti: `_data/kit-emitters.json` (tutte le proprietà dei 34 emitter)

## Come usarlo in Studio
`InsertService:LoadLocalAsset` da script non è permesso (manca la capability RobloxScript), quindi:
1. leggi le proprietà con `python -I _tools/rbxm_props.py <file> ParticleEmitter out.json`;
2. genera un Luau che crea gli emitter (`Instance.new("ParticleEmitter")` + proprietà) e lancialo in Studio;
3. per i mesh crea una Part con una `SpecialMesh` (FileMesh) e il `MeshId` della [[Kit Meshes - Reference Sheet]].
In alternativa: File > Insert from File in Studio, a mano, **dopo** aver letto gli script.

## Sicurezza
4 script, tutti letti: `ColourScript`, `SpinScript`, `MoveScript`, `EmitScript` (preset "SampleOre"). Fanno tween di colore, rotazioni ed Emit periodici e aspettano di stare in `workspace`. Nessun `require` di ID, getfenv, loadstring, HttpService o codice offuscato. Il file comunque non è mai entrato in Place1.

## Schede
[[Kit Emitters - Reference Sheet]] · [[Kit Meshes - Reference Sheet]]

<!-- related:start -->
## Related
[[VFX and Audio Hub]] · [[Skill - Safe Asset Intake]] · [[Studio Kits Hub]] · [[ThunderCombo - Asset IDs and Instances]]
<!-- related:end -->
