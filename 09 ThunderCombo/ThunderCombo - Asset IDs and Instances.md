---
tags: [project, thundercombo, assets, ids, type/reference]
---
# ThunderCombo - Asset IDs and Instances

## Istanze in Place1
| Percorso | Cosa |
|---|---|
| `Workspace.TemplateR6.AnimSaves` | `ThunderCombo` (KFS v4, 138 keyframe), `ThunderIdle` (loop 4 s) |
| `Workspace.TemplateR6.ThunderHeroOutline` | Highlight creato a runtime dal LocalScript (contorno sulla posa finale) |
| `ServerStorage.ThunderCombo_v3_KFS_backup` | KFS v3 di backup |
| `ServerStorage.ThunderCombo_v2_KFS_backup` | KFS v2 di backup |
| `ServerStorage.ThunderCombo_v1_old` | script v1, disattivato |
| `ReplicatedStorage.ThunderVFX.Particles` | emitter v1/v2 (Aura, HitSparks, GroundRing, SlamSmoke, Pillar, Embers, Star, Wisps, Dust...) + 10 del kit (KRing...) |
| `ReplicatedStorage.ThunderVFX.Kit` | i 34 emitter del kit ricreati (K01..K34) |
| `ReplicatedStorage.ThunderVFX.Meshes` | RockCluster, Rubble, Torus (Part + SpecialMesh) |
| `ReplicatedStorage.ThunderVFX.Parts` | Ring, Sphere, Core, Rock, Crack, Shard, ShardGlow, Spike, Line, **Shell** (sfera ForceField per la distorsione, v4) |
| `ReplicatedStorage.ThunderVFX.Sounds` | suoni (sotto) |
| `StarterPlayer.StarterPlayerScripts.ThunderCombo` | LocalScript v4 |
| `StarterPlayerScripts.Client` | vecchio KatanaFX, disattivato |

## Suoni
| Nome | ID | Uso |
|---|---|---|
| Whoosh | rbxassetid://9120972444 | swing, salto, flip, picchiata |
| Charge | rbxassetid://9125980435 | carica, apex |
| Burst | rbxassetid://77174423806230 | fine carica |
| Punch | rbxassetid://132504023010884 | transiente del colpo |
| Slam | rbxassetid://79476956608476 | schianto |
| **Thunder** (v4) | rbxassetid://9126082854 | coda dei finisher e dello schianto (ProSoundEffects, "Synth Thunder Cracks Individual Explosion Booms 5") |
| **Zap** (v4) | rbxassetid://9114277757 | scarica elettrica su ogni colpo (ProSoundEffects, "Electric Zaps 12") |
| Jump / Land / Boom | `rbxasset://sounds/action_jump.mp3`, `action_jump_land.mp3`, `impact_explosion_03.mp3` | salto, atterraggio, corpo del colpo |

## Texture e mesh del kit
Vedi [[Kit Emitters - Reference Sheet]] (ID texture dei 34 emitter) e [[Kit Meshes - Reference Sheet]] (13378856215, 13378853138, 10695006543). Le texture degli emitter v1/v2 sono `rbxasset://textures/particles/*.dds` incluse in Studio.

## Palette
Ciano 80,230,255 · Viola 150,70,255 · Bianco 235,250,255 · Inchiostro 10,12,34. Impact frame: A inchiostro/bianco/linee ciano, B bianco/inchiostro/linee viola, C (solo schianto) viola scuro 30,10,64 / ciano / linee bianche.
