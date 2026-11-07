---
tags: [vfx, meshes, reference, type/reference]
---
# Kit Meshes - Reference Sheet

<!-- tldr:start -->
> [!tldr] TL;DR
> - Mesh del PDS kit usati come SpecialMesh (FileMesh) su una Part 1x1x1
> - Si scala Mesh.Scale, mai Size: la SpecialMesh ignora Size a schermo
> - Scala nativa enorme: 0.03 ≈ 10 stud, quindi rocce a 0.005-0.0085 (Misurato in Play)
> - In Place1: ReplicatedStorage.ThunderVFX.Meshes (RockCluster, Rubble, Torus)
<!-- tldr:end -->


| Nome | MeshId | Cos'è | Uso in ThunderCombo | Scala usata |
|---|---|---|---|---|
| `RockCluster` | `13378856215` | ammasso di roccia/cristalli ("Ore" del kit) | cratere dello schianto (12 pezzi) e detriti volanti | 0.005-0.0085 = roccia 2-3 stud; detriti: 0.0045 x lato della Part |
| `Rubble` | `13378853138` | macerie sparse | 5 gruppi di macerie attorno al cratere | 0.009-0.014 |
| `Torus` | `10695006543` | anello toroidale (Mesh256T.50) | onde d'urto: sui colpi lungo la direzione, sullo schianto piatte a terra | colpi 0.5 -> 4*power (Y 0.06 -> 0.16); schianto 2 -> 20 (Y 0.1 -> 0.35) |
| `Ore 13389904422` | `13389904422` | altra variante di macerie | non usata | - |
| `Smooth Sphere / Cylinder / Cube` | `12812752271 / 12812752257 / 12812752208` | primitive lisce | non usate (utili per sfere di energia) | - |
| `Inverted Smooth Sphere` | `12812752275` | sfera con normali interne | non usata (cupole viste da dentro) | - |
| `Icosphere (.2/.4/.8)` | `10695030495 ...` | sfere low-poly | non usate (frammenti, nuclei) | - |

Tutti gli ID `rbxassetid://...`; fetch "Success" in Play. Altri ~60 mesh del kit (Gear, DoDecaHedron, Mesh3...Mesh256, One Way pane...) sono elencati nel dump del kit (`_tools/rbxm_dump.py <kit> tree`).

## Come usarli
```lua
local p = MESH.Torus:Clone()          -- Part 1x1x1 + SpecialMesh
p.CFrame = dirCF(pos, dir)             -- asse Y = direzione del colpo
p.Mesh.Scale = Vector3.new(0.5, 0.06, 0.5)
tween(p.Mesh, 0.22, {Scale = Vector3.new(4, 0.16, 4) * power})
tween(p, 0.22, {Transparency = 1})
```

## Errori misurati
- Scala 0.022-0.042 sulle rocce: pareti di roccia alte 10+ stud davanti alla camera.
- Toro a scala 7*power con trasparenza 0.15: anello enorme e opaco che copre il colpo.

![[09 ThunderCombo/Screenshots/v3/4_schianto_cratere.jpg|600]]

<!-- related:start -->
## Related
[[PDS Particles and Models Kit]] · [[Kit Emitters - Reference Sheet]] · [[Skill - Roblox VFX Combo]] · [[08 Knowledge/fwjelaa-vault/fwjelaa vault/45 Procedural Blender Assets/Mesh VFX Packs Built in Blender|Mesh VFX Packs Built in Blender (fwjelaa)]]
<!-- related:end -->
