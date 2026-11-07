---
tags: [vfx, particles, reference, textures, type/reference]
---
# Kit Emitters - Reference Sheet

<!-- tldr:start -->
> [!tldr] TL;DR
> - 34 emitter del PDS kit, generati da _data/kit-emitters.json (non scritti a mano)
> - In Place1 stanno in ReplicatedStorage.ThunderVFX.Kit con nome K01..K34 + ID texture
> - I 10 usati in ThunderCombo sono copie ricolorate in ThunderVFX.Particles (KRing, KBurst...)
> - Tutte le texture si caricano (ContentProvider: Success, misurato in Play)
<!-- tldr:end -->


## I 10 usati in ThunderCombo
| Nome in `ThunderVFX.Particles` | Da | Uso | Override principali |
|---|---|---|---|
| `KBurst` | K04 | burst di energia al contatto | ciano, Size 0.4 -> 3.2*power, Transparency 0.4 -> 1, FacingCamera |
| `KCrackle` | K22 | crepitio elettrico al contatto | ciano, Brightness 2.2, Size 1 -> 6, FacingCamera |
| `KFlash` | K23 | scintille flipbook sui pugni durante la carica | Rate 22 mentre carica, Size 1.4 -> 2.2 |
| `KInkSwirl` | K16 | spirale d'inchiostro scuro (schianto, contrasto) | INK 10,12,34, RotSpeed -180 |
| `KPuff` | K20 | puff di fumo radiale sullo schianto | grigio-blu, Transparency 0.55 -> 1, Size 3 -> 10, 10 particelle |
| `KRing` | K02 | anello shockwave su ogni colpo, lungo la direzione | colore ciano, Lifetime 0.4, Size 1 -> 8*power, FlipbookMode OneShot |
| `KRisers` | K29 | strisce che salgono da un disco 7x7 durante la carica | Rate 45, Speed 6-12, Acceleration Y 10 |
| `KSlashRing` | K25 | anello di taglio rotante sul calcio (Hit3) | bianco -> viola, RotSpeed 700, Lifetime 0.35 |
| `KSmokeSpiral` | K15 | fumo a spirale bianco sul terreno (schianto) | Transparency 0.6 -> 1, VelocityPerpendicular |
| `KSwirl` | K12 | spirale a terra durante la carica | ciano -> viola, Rate 7, RotSpeed 260 |

Regole applicate a tutti: `LightInfluence = 0` (altrimenti al tramonto, ClockTime 17.8, si spengono), `Enabled = false` e `Rate = 0` nel template, colori della palette (ciano 80,230,255 · viola 150,70,255 · bianco 235,250,255 · inchiostro 10,12,34). Si emettono solo con `Emit()` o con un `Rate` temporaneo, sempre clonati dallo script (orologio scalato).

## Anteprima
![[09 ThunderCombo/Screenshots/v3/0_kit_emitter_anteprima.jpg|600]]
Griglia 7 per riga, da K01 in alto a sinistra: 2 = anelli flipbook, 4 = burst blu, 10 = stella a 4 punte, 12 = anello a spirale, 15/17 = fumo a spirale bianco/nero, 20 = puff bianco, 22 = crepitio, 23 = flash flipbook, 25/27 = anelli slash orizzontale/verticale.

## Tutti i 34 emitter
| # | Nome originale | Texture | Rate | Lifetime | Size | LightEmission | Flipbook | Origine | Usato |
|---|---|---|---|---|---|---|---|---|---|
| K01 | ParticleEmitter | `7216855914` | 20 | 1-2 | 1 → 1 | 1 | - | Pigs V5 |  |
| K02 | ParticleEmitter | `16502428362` | 3 | 2-2 | 0 → 10 | 1 | 4x4 | Pigs V5 | **KRing** |
| K03 | ParticleEmitter | `14049993216` | 100 | 2-2 | 1.1875 → 11.4275 | 1 | - | Pigs V5 |  |
| K04 | ParticleEmitter | `8315450991` | 20 | 3-5 | 0 → 10.7906 | 1 | - | Pigs V5 | **KBurst** |
| K05 | ParticleEmitter | `12222002958` | 20 | 2-3 | 0 → 0 | 0 | - | Pigs V5 |  |
| K06 | ParticleEmitter | `8890667599` | 20 | 5-5 | 0 → 12.429 | 1 | - | Pigs V5 |  |
| K07 | ParticleEmitter | `7216847852` | 20 | 2-3 | 0.5 → 1.5625 | 1 | - | Pigs V5 |  |
| K08 | ParticleEmitter | `17426661930` | 50 | 5-5 | 0 → 0 | 1 | - | Pigs V5 |  |
| K09 | ParticleEmitter | `14049993216` | 20 | 2-2 | 0 → 10 | 1 | - | Pigs V5 |  |
| K10 | star | `7216849325` | 10 | 1-1 | 13.2213 → 20 | 1 | - | Pigs V5 |  |
| K11 | ParticleEmitter | `7216855914` | 20 | 2-3 | 0 → 0.6875 | 1 | - | Pigs V5 |  |
| K12 | swirl | `10558425570` | 150 | 2-2 | 7 → 7 | 1 | - | Pigs V5 | **KSwirl** |
| K13 | ParticleEmitter | `14050321697` | 20 | 4-4 | 0 → 12.4757 | 1 | - | Pigs V5 |  |
| K14 | ParticleEmitter | `14054628491` | 20 | 5-5 | 0 → 16.1986 | 1 | - | Pigs V5 |  |
| K15 | ParticleEmitter | `12389944306` | 20 | 4-4 | 0 → 12.4757 | 1 | - | Pigs V5 | **KSmokeSpiral** |
| K16 | ParticleEmitter | `12389944306` | 20 | 4-4 | 0 → 12.4757 | 0 | - | Pigs V5 | **KInkSwirl** |
| K17 | ParticleEmitter | `7216850580` | 20 | 4-4 | 0 → 18.8475 | 0 | - | Pigs V5 |  |
| K18 | swirl | `14050094484` | 5 | 2-2 | 0 → 10 | 1 | - | Pigs V5 |  |
| K19 | ParticleEmitter | `12878479033` | 20 | 4-4 | 0 → 12.4757 | 1 | - | Pigs V5 |  |
| K20 | ParticleEmitter | `14221378803` | 30 | 4-4 | 0 → 18.8475 | 1 | - | Pigs V5 | **KPuff** |
| K21 | ParticleEmitter | `15440984216` | 60 | 5-5 | 6 → 6 | 1 | - | Pigs V5 |  |
| K22 | ParticleEmitter | `917181007` | 20 | 4-4 | 0 → 5.4375 | 1 | - | Pigs V5 | **KCrackle** |
| K23 | ParticleEmitter | `12800314277` | 40 | 0.15-0.15 | 1.5 → 1.5 | 1 | 2x2 | Pigs V5 | **KFlash** |
| K24 | ParticleEmitter | `7216849325` | 20 | 1-1 | 6.375 → 0 | 1 | - | Pigs V5 |  |
| K25 | Slash | `14054635072` | 3 | 8-8 | 10 → 0 | 1 | - | Hitbox | **KSlashRing** |
| K26 | Fog | `14050109275` | 8 | 5-5 | 8 → 10 | 1 | - | Hitbox |  |
| K27 | Top | `7216849703` | 40 | 8-8 | 0 → 16 | 1 | - | Hitbox |  |
| K28 | Fog2 | `14049414463` | 40 | 6-6 | 10 → 7.7966 | 1 | - | Hitbox |  |
| K29 | Risers | `7216855914` | 40 | 6-6 | 0.904 → 0 | 1 | - | Hitbox | **KRisers** |
| K30 | Sparkles | `7216849325` | 200 | 2-2 | 2.4294 → 2.4859 | 1 | - | Big Ore |  |
| K31 | Fog | `14050223758` | 8 | 5-5 | 0 → 10 | 1 | - | Big Ore |  |
| K32 | ParticlesGreen | `7216855914` | 20 | 1-2 | 0 → 0.339 | 1 | - | Hitbox |  |
| K33 | Clover | `14279114116` | 20 | 2-3 | 0 → 0.2825 | 1 | - | Hitbox |  |
| K34 | Particles | `7216855914` | 30 | 1-2 | 0 → 0.113 | 1 | - | Hitbox |  |


<!-- related:start -->
## Related
[[PDS Particles and Models Kit]] · [[Kit Meshes - Reference Sheet]] · [[Skill - Roblox VFX Combo]] · [[08 Knowledge/fwjelaa-vault/fwjelaa vault/07 Lighting VFX and Audio/Particle Emitters In Depth|Particle Emitters In Depth (fwjelaa)]]
<!-- related:end -->
