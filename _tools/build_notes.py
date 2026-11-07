"""Writes the own notes of 'niceforwh vault' (hubs, resource notes, sheets, ThunderCombo, canvas, .obsidian).
Usage: python -I build_notes.py <vault>      (re-runnable: overwrites only the files it owns)
"""
import csv, json, os, re, shutil, sys
from collections import Counter

V = sys.argv[1]
FWR = '08 Knowledge/fwjelaa-vault/fwjelaa vault'


def fw(rel, label=None):
    """Path-qualified link into the nested fwjelaa vault (avoids name collisions)."""
    label = label or os.path.basename(rel)
    return f'[[{FWR}/{rel}|{label}]]'


def count(folder, exts=None):
    n = 0
    for dp, _, fns in os.walk(os.path.join(V, folder)):
        for f in fns:
            if exts is None or f.rsplit('.', 1)[-1].lower() in exts:
                n += 1
    return n


def subdirs(folder):
    p = os.path.join(V, folder)
    return sorted(d for d in os.listdir(p) if os.path.isdir(os.path.join(p, d)))


IMG = {'png', 'jpg', 'jpeg', 'gif', 'webp', 'svg'}
NOTES = {}


def note(path, tags, body, css=None):
    fm = ['---']
    if css:
        fm.append(f'cssclasses: [{css}]')
    fm.append(f'tags: [{", ".join(tags)}]')
    fm.append('---')
    NOTES[path] = '\n'.join(fm) + '\n' + body.strip() + '\n'


def tldr(*lines):
    return '<!-- tldr:start -->\n> [!tldr] TL;DR\n' + '\n'.join(f'> - {l}' for l in lines) + '\n<!-- tldr:end -->\n'


def related(*links):
    return '\n<!-- related:start -->\n## Related\n' + ' · '.join(links) + '\n<!-- related:end -->\n'


# ------------------------------------------------------------------ data
emitters = json.load(open(os.path.join(V, '_data/kit-emitters.json'), encoding='utf-8'))
CURATED = {  # kit index -> (name in ThunderVFX.Particles, use in ThunderCombo, key overrides)
    2: ('KRing', 'anello shockwave su ogni colpo, lungo la direzione', 'colore ciano, Lifetime 0.4, Size 1 -> 8*power, FlipbookMode OneShot'),
    4: ('KBurst', 'burst di energia al contatto', 'ciano, Size 0.4 -> 3.2*power, Transparency 0.4 -> 1, FacingCamera'),
    22: ('KCrackle', 'crepitio elettrico al contatto', 'ciano, Brightness 2.2, Size 1 -> 6, FacingCamera'),
    23: ('KFlash', 'scintille flipbook sui pugni durante la carica', 'Rate 22 mentre carica, Size 1.4 -> 2.2'),
    12: ('KSwirl', 'spirale a terra durante la carica', 'ciano -> viola, Rate 7, RotSpeed 260'),
    29: ('KRisers', 'strisce che salgono da un disco 7x7 durante la carica', 'Rate 45, Speed 6-12, Acceleration Y 10'),
    20: ('KPuff', 'puff di fumo radiale sullo schianto', 'grigio-blu, Transparency 0.55 -> 1, Size 3 -> 10, 10 particelle'),
    15: ('KSmokeSpiral', 'fumo a spirale bianco sul terreno (schianto)', 'Transparency 0.6 -> 1, VelocityPerpendicular'),
    16: ('KInkSwirl', 'spirale d\'inchiostro scuro (schianto, contrasto)', 'INK 10,12,34, RotSpeed -180'),
    25: ('KSlashRing', 'anello di taglio rotante sul calcio (Hit3)', 'bianco -> viola, RotSpeed 700, Lifetime 0.35'),
}
MESHES = [
    ('RockCluster', '13378856215', 'ammasso di roccia/cristalli ("Ore" del kit)', 'cratere dello schianto (12 pezzi) e detriti volanti', '0.005-0.0085 = roccia 2-3 stud; detriti: 0.0045 x lato della Part'),
    ('Rubble', '13378853138', 'macerie sparse', '5 gruppi di macerie attorno al cratere', '0.009-0.014'),
    ('Torus', '10695006543', 'anello toroidale (Mesh256T.50)', 'onde d\'urto: sui colpi lungo la direzione, sullo schianto piatte a terra', 'colpi 0.5 -> 4*power (Y 0.06 -> 0.16); schianto 2 -> 20 (Y 0.1 -> 0.35)'),
    ('Ore 13389904422', '13389904422', 'altra variante di macerie', 'non usata', '-'),
    ('Smooth Sphere / Cylinder / Cube', '12812752271 / 12812752257 / 12812752208', 'primitive lisce', 'non usate (utili per sfere di energia)', '-'),
    ('Inverted Smooth Sphere', '12812752275', 'sfera con normali interne', 'non usata (cupole viste da dentro)', '-'),
    ('Icosphere (.2/.4/.8)', '10695030495 ...', 'sfere low-poly', 'non usate (frammenti, nuclei)', '-'),
]

# ------------------------------------------------------------------ root hubs
n_icons = count('05 UI and Icons/Icons', IMG)
n_refs = count('05 UI and Icons/Style References', IMG)
n_glb = count('03 Models and Characters/Characters', {'glb'})
n_fw = count('08 Knowledge/fwjelaa-vault')
n_rai = count('08 Knowledge/roblox-ai')
n_sfx = count('01 VFX and Audio/SFX/CC0 Library (roblox-ai)')

note('000 Home.md', ['hub', 'type/hub', 'level/beginner'], f'''
> [!fw-hero] NICEFORWH VAULT
> ![[_assets/thundercombo-banner.jpg|420]]
> # niceforwh vault
> **Tutto quello che serve per fare combo, VFX, animazioni, mappe e UI su Roblox**, unito per tema: kit Studio, texture, icone, modelli, riferimenti, tool e la knowledge base fwjelaa.
>
> [[00 Start Here|Inizia qui]] · [[ROUTER|Cerco X, dove vado?]] · [[Skill - Roblox VFX Combo|Rifai una combo come ThunderCombo]]
>
> `{n_icons} icone` `{n_refs} riferimenti UI` `34 emitter del kit` `{n_glb} personaggi .glb` `45 animazioni R6/R15` `4 mappe d'esempio` `{n_fw} file di knowledge fwjelaa` `{n_sfx} SFX CC0` `{n_rai} file del repo roblox-ai`

> [!fw-buttons]
> - [[VFX and Audio Hub|VFX]]
> - [[Animation Hub|Animazione]]
> - [[Models and Characters Hub|Modelli]]
> - [[Maps and World Hub|Mappe]]
> - [[UI and Icons Hub|UI]]
> - [[ThunderCombo Hub|ThunderCombo]]

> [!fw-strip] Parti in 60 secondi
> **Fare una combo** → [[Skill - Roblox VFX Combo]] · [[Kit Emitters - Reference Sheet]] · [[Combat Timing Cheat Sheet]] · [[ThunderCombo - Timing and Markers]]
> **Importare roba in sicurezza** → [[Skill - Safe Asset Intake]] · [[Studio Kits Hub]] · [[Vault Maintenance Tools]]
> **Trovare un riferimento** → [[UI Style References]] · [[VFX Reference Images]] · [[Anime Character GLB Pack]] · [[MapKit Example Maps]] · [[Game Refs (roblox-ai)]]
> **Trovare un suono** → [[CC0 SFX Library (roblox-ai)]] (impatti, pugni, whoosh, cariche, esplosioni, UI)

> [!fw-grid]
> > [!fw-motion] Motion & FX
> > [[VFX and Audio Hub|VFX & Audio]] · [[PDS Particles and Models Kit|Kit particelle]] · [[Kit Meshes - Reference Sheet|Mesh del kit]] · [[VFX Method - Principles and Pipeline|Metodo VFX]] · [[Impact Frames Hitstop and Camera|Impact frame & hitstop]] · [[CC0 SFX Library (roblox-ai)|SFX CC0]] · [[Animation Hub|Animazione]] · [[fwjelaa Animation Pack|Animation pack]] · [[Roblox Docs Motion References|Motion refs docs]]
>
> > [!fw-world] World & Art
> > [[Models and Characters Hub|Modelli]] · [[Anime Character GLB Pack|Personaggi .glb]] · [[Rigs Creatures and Concept Sheets|Rig e creature]] · [[Maps and World Hub|Mappe]] · [[MapKit Example Maps|Mappe d'esempio]]
>
> > [!fw-ui] Interface
> > [[UI and Icons Hub|UI & Icone]] · [[UI Icon Pack|Icon pack]] · [[UI Style References|Riferimenti di stile]] · [[Roblox UI Kit (fwjelaa)|UI Kit luau]]
>
> > [!fw-code] Kits & Tools
> > [[Studio Kits Hub|Kit Studio (.rbxm/.rbxmx)]] · [[Tools and Pipelines Hub|Tool]] · [[Picture to Roblox Model]] · [[MapKit - Roblox Maps by fwjelaa|MapKit]] · [[Vault Maintenance Tools|Manutenzione vault]]
>
> > [!fw-data] Knowledge
> > [[Knowledge Hub|fwjelaa vault]] · [[roblox-ai Reference Library|roblox-ai]] · [[Roblox Docs Screenshots (roblox-ai)|Screenshot docs Roblox]] · {fw('000 Home', 'Home fwjelaa')} · {fw('ROUTER', 'Router fwjelaa')} · [[Glossary - niceforwh|Glossario]] · [[Open Questions - niceforwh|Domande aperte]]
>
> > [!fw-pipeline] Project
> > [[ThunderCombo Hub|ThunderCombo]] · [[ThunderCombo - Build Log|Build log v1-v4]] · [[ThunderCombo - Asset IDs and Instances|ID e istanze]] · [[ThunderCombo - Screenshots|Screenshot]]

> [!fw-legend] Come fidarsi di una nota
> **Misurato** provato in Studio (Place1, novembre 2026) · **Dal pack** preso da un pack o da una nota fwjelaa, citato · **Regola pratica** esperienza · **Non verificato** vedi [[Open Questions - niceforwh]]
''', css='fw-home')

note('00 Start Here.md', ['index', 'start', 'type/hub', 'level/beginner'], f'''
# niceforwh vault: Start Here

Questo vault mette insieme, **per tema e non per pack di provenienza**, tutte le risorse arrivate in `niceforwh vault`: il kit di particelle e modelli, l'animation pack, i tool di fwjelaa (mappe, modelli da immagine, UI kit), l'icon pack, i riferimenti UI, i 76 personaggi `.glb`, l'intera knowledge base fwjelaa e il repo di riferimenti **roblox-ai** (SFX CC0, screenshot della documentazione Roblox, riferimenti di giochi). In più c'è il progetto **ThunderCombo**, la combo anime costruita in Place1 con queste risorse. La home visiva è [[000 Home]].

## Come leggere le etichette
- **Misurato**: provato davvero in Roblox Studio su Place1 (novembre 2026), con screenshot.
- **Dal pack**: preso da un pack o da una nota fwjelaa e citato; non ricontrollato riga per riga.
- **Regola pratica**: esperienza, etichettata come tale.
- **Non verificato**: raccolto in [[Open Questions - niceforwh]].

## Percorsi di lettura

**Voglio rifare una combo con VFX:**
[[Skill - Roblox VFX Combo]] → [[Combat Timing Cheat Sheet]] → [[Kit Emitters - Reference Sheet]] → [[Kit Meshes - Reference Sheet]] → [[Impact Frames Hitstop and Camera]] → [[ThunderCombo - Timing and Markers]]

**Voglio capire i VFX:**
[[VFX and Audio Hub]] → [[VFX Method - Principles and Pipeline]] → [[PDS Particles and Models Kit]] → {fw('07 Lighting VFX and Audio/VFX Design Playbook', 'VFX Design Playbook (fwjelaa)')}

**Voglio animare:**
[[Animation Hub]] → [[fwjelaa Animation Pack]] → [[Anim Research 03 - Animation Craft Numbers]] → [[Combat Timing Cheat Sheet]] → {fw('08 Animation/Animation Start Here', 'Animation Start Here (fwjelaa)')}

**Voglio un riferimento visivo (UI, VFX, mappe, modelli):**
[[UI Style References]] · [[UI Icon Pack]] · [[VFX Reference Images]] · [[MapKit Example Maps]] · [[Anime Character GLB Pack]] · [[Game Refs (roblox-ai)]] · [[Roblox Docs Screenshots (roblox-ai)]]

**Mi serve un suono:**
[[CC0 SFX Library (roblox-ai)]] → [[Impact Frames Hitstop and Camera]]

**Devo importare qualcosa in Studio:**
[[Skill - Safe Asset Intake]] → [[Studio Kits Hub]] → [[Vault Maintenance Tools]]

## Struttura

| Cartella | Cosa c'è |
|---|---|
| `01 VFX and Audio` | note VFX, schede del kit, immagini di riferimento VFX, SFX (con la libreria CC0 di roblox-ai), cinematiche, il prompt originale del metodo VFX |
| `02 Animation` | note di animazione, research dell'animation pack (copie), riferimenti di movimento (PunchRef), anteprime |
| `03 Models and Characters` | 76 personaggi `.glb`, rig e creature, concept sheet, anteprime Picture-to-Model |
| `04 Maps and World` | screenshot delle 4 mappe d'esempio di MapKit, research sulle mappe |
| `05 UI and Icons` | {n_icons} icone per categoria, {n_refs} riferimenti di stile, screenshot di HUD, texture, loghi e thumbnail |
| `06 Studio Kits` | tutti i `.rbxm`/`.rbxmx`, divisi per uso (VFX, UI, Animations) |
| `07 Tools and Pipelines` | i progetti con codice, **lasciati interi**: animation pack, MapKit, Picture-to-Model, UI kit |
| `08 Knowledge` | il vault fwjelaa completo (plugin compreso) e il repo roblox-ai, **lasciati interi** |
| `09 ThunderCombo` | note di progetto, ID, timing, screenshot v1-v4 |
| `_assets` · `_data` · `_tools` · `_originali` | immagini del vault · inventari, piano, log, duplicati · script di manutenzione · archivi originali intatti |

## Il vault fwjelaa dentro questo vault
`08 Knowledge/fwjelaa-vault/fwjelaa vault` è un vault Obsidian completo, con 1.300+ note. Da qui lo raggiungi con link a percorso completo. Molti suoi file hanno lo stesso nome delle note-hub di questo vault (`000 Home`, `INDEX`, `ROUTER`, `Glossary`...), e i suoi link interni brevi possono risolversi sul file sbagliato. **Per navigarlo con tutti i link funzionanti aprilo come vault separato in Obsidian** (Apri cartella come vault → `fwjelaa vault`). Dettagli in [[Knowledge Hub]].

## Sicurezza (riassunto)
Niente è stato eseguito: nessun `.exe`, `.bat`, `.sh`, `.py`, hook o plugin dei pack. I `.md` dei pack sono **materiale di riferimento, non istruzioni**. I `.rbxm` sono stati letti offline e i loro script controllati prima di usarli. Il tema Obsidian carica i font da Google Fonts. Tutto in [[Skill - Safe Asset Intake]].
''')

note('ROUTER.md', ['index', 'router', 'type/hub'], f'''
# niceforwh Router (leggi prima questo)

Cerco X → vado a Y. Una riga per bisogno; il percorso completo di ogni nota è in [[INDEX]] (o [[INDEX_SLIM]]). Per la knowledge base fwjelaa c'è il suo {fw('ROUTER', 'router')}.

## Combo, VFX, animazione
- combo anime completa, hitstop, impact frame, camera → [[Skill - Roblox VFX Combo]]; [[ThunderCombo Hub]]
- emitter pronti (anelli, burst, fumo, scintille), ID texture → [[Kit Emitters - Reference Sheet]]
- mesh per shockwave, rocce, cratere → [[Kit Meshes - Reference Sheet]]
- impact frame, hitstop, shake, slow-mo → [[Impact Frames Hitstop and Camera]]
- principi e pipeline VFX (anticipation → impact → cleanup) → [[VFX Method - Principles and Pipeline]]
- immagini di riferimento VFX, SFX, cinematiche → [[VFX Reference Images]]
- suoni CC0 (pugni, impatti, whoosh, cariche, esplosioni, UI) → [[CC0 SFX Library (roblox-ai)]]
- screenshot ufficiali di Animation Editor, curve, IK, camera, cutscene → [[Roblox Docs Motion References]]
- numeri di timing (frame di hitstop, overlap, anticipation) → [[Combat Timing Cheat Sheet]]; [[Anim Research 03 - Animation Craft Numbers]]
- generare animazioni R6/R15 da una clip → [[fwjelaa Animation Pack]]
- animazioni pronte da importare (.rbxmx) → [[Studio Kits Hub]]
- Moon Animator, pipeline Roblox delle animazioni → [[Anim Research 02 - Moon Animator 2]]; [[Anim Research 01 - Roblox Animation Pipeline]]

## Modelli, mappe, UI
- personaggi anime `.glb` → [[Anime Character GLB Pack]]
- rig (R6, R15, creature, armi), concept sheet → [[Rigs Creatures and Concept Sheets]]
- modello da un'immagine → [[Picture to Roblox Model]]
- mappa da una descrizione, mappe d'esempio → [[MapKit - Roblox Maps by fwjelaa]]; [[MapKit Example Maps]]
- icone (valute, uova, gamepass, rank, tasti) → [[UI Icon Pack]]
- stile UI di un genere (anime, cyberpunk, simulator...) → [[UI Style References]]
- componenti UI in Luau → [[Roblox UI Kit (fwjelaa)]]
- com'è fatto un gioco di un genere (anime fighting, obby, horror, simulator...), icone e thumbnail di giochi → [[Game Refs (roblox-ai)]]
- screenshot della documentazione Roblox (Studio, UI, lighting, modeling, tutorial) → [[Roblox Docs Screenshots (roblox-ai)]]
- repo roblox-ai: cosa c'è, licenza, dove sono finite le copie → [[roblox-ai Reference Library]]

## Sicurezza e manutenzione
- posso inserire questo `.rbxm`? → [[Skill - Safe Asset Intake]]
- dove è finito il file X del vecchio ordine? → [[riorganizzazione-log|Riorganizzazione - Log]]
- rigenerare indice, controllare link, inventario → [[Vault Maintenance Tools]]
- termini (KFS, Motor6D, flipbook...) → [[Glossary - niceforwh]]
''')

note('Glossary - niceforwh.md', ['reference', 'glossary', 'type/reference', 'level/beginner'], f'''
# Glossary - niceforwh

Termini usati in questo vault. Il glossario completo della knowledge base è {fw('Glossary', 'Glossary (fwjelaa)')}; quello di animazione è {fw('08 Animation/Animation Glossary', 'Animation Glossary (fwjelaa)')}.

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
''')

note('Open Questions - niceforwh.md', ['index', 'unresolved', 'type/guide'], f'''
# Open Questions - niceforwh

Cose non verificate o in conflitto, raccolte invece di essere risolte in silenzio. Quelle della knowledge base fwjelaa sono in {fw('Open Questions - Whole Vault', 'Open Questions - Whole Vault')}.

| Domanda | Stato | Note |
|---|---|---|
| Scala nativa dei mesh "Ore" del kit | **Misurato a occhio**: 0.03 ≈ 10 stud, 0.005-0.0085 ≈ 2-3 stud | La stima dall'anteprima (0.05 ≈ 4 stud) era sbagliata di 3-4 volte; vedi [[Kit Meshes - Reference Sheet]] |
| Asse del Torus (10695006543) | Usato con asse Y = direzione del colpo; sembra corretto negli screenshot | Non misurato con precisione |
| Calcio e posa d'atterraggio v3 dopo l'ultimo ritocco | **Risolto** (2026-11-06): ricatturati come base della v4, poi rifatti | [[ThunderCombo - Screenshots]] |
| Gli emitter del kit rispettano la licenza d'uso? | Non verificato | Il kit è PDS / Pigs Particle Pack V5, trovato nel vault senza licenza scritta |
| Stud UI Pack (lando) | Kit **a pagamento** di terzi, solo riferimento | Lo dice il suo `SOURCE.txt`; non va spedito in un gioco o in un pack |
| `Browse the icons.html` dopo la deduplica | 1 icona rimossa perché identica a un'altra (hexagon-wood-1 = hexagon-bronze-1) | La pagina può mostrare un'immagine mancante; vedi [[riorganizzazione-log|Riorganizzazione - Log]] |
| Nomi uguali tra queste note e il vault fwjelaa | Mitigato | Vedi [[Knowledge Hub]] |
| I 2.210 SFX di roblox-ai sono davvero tutti CC0? | **Dal pack**: lo dice il README del repo, non verificato file per file | [[CC0 SFX Library (roblox-ai)]] |
| Diritti di game-refs, thumbnail e loghi di roblox-ai | Arte di giochi di terzi: **solo riferimento** (README, sezione Rights) | [[roblox-ai Reference Library]] |
| File con nome accorciato nel repo roblox-ai | 1 file aveva un percorso oltre 249 caratteri: rinominato, originale nell'archivio | [[roblox-ai Reference Library]] |
''')

note('Skill - Roblox VFX Combo.md', ['ai-skill', 'vfx', 'animation', 'combat', 'type/guide', 'level/intermediate'], f'''
# Skill - Roblox VFX Combo

**Procedura operativa** per rifare una combo anime come ThunderCombo (carica → 3 colpi → salto → schianto) con le risorse di questo vault. È la sintesi di quello che ha funzionato davvero in Place1 (**Misurato**) e delle regole dei pack (**Dal pack**).

{tldr('Animazione = KeyframeSequence generata da script, con marker; i VFX partono dai marker sul client',
      'Hitstop per peso 0.066 / 0.075 / 0.10 / 0.22 s (budget KB 140 ms ogni 0.6 s, superato apposta solo prima del finisher), recupero 0.08x → 1.9x, vibrazione del RootJoint.C0 ripristinata sempre',
      'Emitter e mesh del kit passano dal percorso tracciato (ThunderVFX.Particles), altrimenti freeze e time scale non li fermano',
      'Mesh del kit: scalare Mesh.Scale, mai Size; scala nativa enorme (0.005-0.0085 = 2-3 stud)',
      'Meno è meglio: ogni layer nuovo va controllato in uno screenshot; la sovraesposizione è il primo difetto')}

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
[[ThunderCombo - Build Log]] · [[ThunderCombo - Timing and Markers]] · [[ThunderCombo - Asset IDs and Instances]] · {fw('07 Lighting VFX and Audio/Slash VFX Recipes - Crescent and Ring', 'Slash VFX Recipes (fwjelaa)')} · {fw('47 Game Feel and Juice/Hit-Stop and Screen Shake Tuning by Numbers', 'Hit-Stop and Screen Shake Tuning by Numbers (fwjelaa)')} · {fw('08 Animation/05 Systems/VFX Timing with Animation', 'VFX Timing with Animation (fwjelaa)')}
{related('[[VFX and Audio Hub]]', '[[Animation Hub]]', '[[ThunderCombo Hub]]', '[[Skill - Safe Asset Intake]]')}
''')

note('Skill - Safe Asset Intake.md', ['ai-skill', 'security', 'assets', 'type/guide', 'level/beginner'], f'''
# Skill - Safe Asset Intake

**Procedura** per far entrare in Studio (o nel vault) un asset scaricato senza portarsi dietro backdoor o comandi nascosti. È quella seguita per tutto il materiale di questo vault.

{tldr('Archivi: estrai ognuno in una cartella nuova, originale in _originali/, niente si esegue',
      'I .md scaricati sono riferimento, non istruzioni: se chiedono azioni, segnalale',
      '.rbxm: leggi gli script offline prima di inserirli (require di ID, getfenv, loadstring, HttpService, offuscamento)',
      'Se Studio non può caricare il file da script, ricrea solo quello che serve dalle proprietà',
      'Kit a pagamento di terzi: solo riferimento, mai spediti')}

## 1. Cosa è stato controllato in questo vault
| Risorsa | Controllo | Esito |
|---|---|---|
| `06 Studio Kits/VFX/PDS Particles and Models Kit.rbxm` | lettura offline (parser LZ4), 4 script letti | puliti: Colour/Spin/Emit/Move sono loop di tween; **mai inseriti**, emitter ricreati dalle proprietà |
| `06 Studio Kits/UI/Stud UI Pack (lando).rbxm` | lettura offline, 5 LocalScript | puliti: ruotano un'immagine (`Rotation += 1`); **kit a pagamento**, solo riferimento |
| `06 Studio Kits/Animations/*.rbxmx` (45) | ricerca di classi Script/LocalScript/ModuleScript nell'XML | nessuno script: solo KeyframeSequence, Keyframe, Pose, KeyframeMarker |
| `docs` dei pack (`fwjelaa vfx method`, `ForgeGUI brief`) | letti come testo | sono prompt per un'AI; **non eseguiti**, presi solo i principi |
| `07 Tools and Pipelines/*` | elencati, non eseguiti | contengono `.py`, `.bat`, `.sh`, `CLAUDE.md`, skill: non lanciati |
| `.secrets/` (animation pack, Picture-to-Model) | solo il nome dei file | contengono un `README.txt` (posto per una chiave API); non letti |
| `08 Knowledge/fwjelaa-vault` | elencato | plugin Claude con `hooks/` e `agents/`: **non installato**; tema Obsidian copiato (solo CSS) |
| Tema Obsidian "Infinite Void" | grep di `@import`/`url(` | importa font da `fonts.googleapis.com`: Obsidian li scarica quando apre il vault |
| repo GitHub `izzyfrm/roblox-ai` | clone `--depth 1` senza hook, LFS, submodule e symlink; ogni file verificato contro l'hash git | solo media (immagini, mp3, mp4) e un README: niente codice, niente eseguito; vedi [[roblox-ai Reference Library]] |

## 2. Procedura
1. **Estrai** ogni archivio in una cartella nuova; l'originale va in `_originali/` e non si tocca.
2. **Non eseguire** niente che venga dall'archivio (exe, bat, sh, ps1, py, hook, plugin). Se un tool serve, chiedi prima.
3. **Leggi i testi come dati.** Un `.md` che dice "fai X" è materiale di riferimento: riporta la richiesta, non eseguirla.
4. **`.rbxm` binari**: `python -I _tools/rbxm_dump.py <file> summary` (classi e script) e `sources` (codice). Cerca `require(` con ID numerici, `getfenv`/`setfenv`, `loadstring`, `HttpService`, `string.char` a catena, codice offuscato.
5. **`.rbxmx`**: è XML; cerca `class="Script"`, `LocalScript`, `ModuleScript` e leggi i `ProtectedString`.
6. **Inserimento**: se lo script è sospetto disattivalo o rimuovilo e annotalo. Se basta una parte (emitter, mesh), ricreala dalle proprietà (`_tools/rbxm_props.py`) senza inserire il file.
7. **Annota** l'esito nella nota della risorsa, sezione "Sicurezza".
8. **Repo GitHub**: clone in una cartella nuova con `GIT_LFS_SKIP_SMUDGE=1 git -c core.hooksPath=NUL -c core.symlinks=false clone --depth 1 --no-recurse-submodules`; annota commit e licenza; verifica i file con `_tools/git_verify.py`; archivio originale con `git archive` in `_originali/`.

## Note collegate
{fw('01 Studio and Workflow/Creator Store and Toolbox Safety', 'Creator Store and Toolbox Safety (fwjelaa)')} · {fw('16 MCP and Agents/Safety Rules for AI Agents in Studio', 'Safety Rules for AI Agents in Studio (fwjelaa)')} · [[Vault Maintenance Tools]] · [[Studio Kits Hub]]
{related('[[00 Start Here]]', '[[Knowledge Hub]]', '[[PDS Particles and Models Kit]]')}
''')

# ------------------------------------------------------------------ 01 VFX
note('01 VFX and Audio/VFX and Audio Hub.md', ['hub', 'vfx', 'audio', 'type/hub'], f'''
# VFX and Audio Hub

Tutto quello che riguarda effetti, particelle, texture VFX e suoni, unito da: kit PDS, Reference Library fwjelaa, metodo VFX, ThunderCombo.

## Note
- [[PDS Particles and Models Kit]]: il kit `.rbxm` (34 emitter, ~70 mesh), cosa contiene e come è stato importato
- [[Kit Emitters - Reference Sheet]]: tutti gli emitter con ID texture e proprietà chiave, i 10 usati in ThunderCombo
- [[Kit Meshes - Reference Sheet]]: rocce, toro, sfere: ID e scale misurate
- [[VFX Method - Principles and Pipeline]]: sintesi del prompt "fwjelaa vfx method" e delle note fwjelaa
- [[Impact Frames Hitstop and Camera]]: impact frame, hitstop, shake, slow-mo, camera
- [[VFX Reference Images]]: immagini di riferimento, SFX, cinematiche
- [[CC0 SFX Library (roblox-ai)]]: {n_sfx} suoni CC0 in 31 categorie (pugni, impatti, whoosh, cariche, esplosioni, magia, UI)
- [[Roblox Docs Motion References]]: screenshot ufficiali di camera e cutscene (in `Cinematics/`) e di animazione

## Cartelle
| Cartella | Contenuto | File |
|---|---|---|
| `Reference Images/` | riferimenti VFX per tipo (hit spark, slash, speed lines, aure, esplosioni, spritesheet) | {count('01 VFX and Audio/Reference Images')} |
| `SFX/` | anteprime audio di riferimento + `CC0 Library (roblox-ai)/` (mp3 CC0 per categoria) | {count('01 VFX and Audio/SFX')} |
| `Cinematics/` | riferimenti di inquadrature (impact hit-stop, dialoghi, camera e cutscene dalla documentazione Roblox) | {count('01 VFX and Audio/Cinematics')} |
| `Sources/` | il prompt originale del metodo VFX (riferimento, non istruzioni) | {count('01 VFX and Audio/Sources')} |

## Nella knowledge base fwjelaa
{fw('07 Lighting VFX and Audio/VFX Design Playbook', 'VFX Design Playbook')} · {fw('07 Lighting VFX and Audio/Particle Emitters In Depth', 'Particle Emitters In Depth')} · {fw('07 Lighting VFX and Audio/Beams and Trails', 'Beams and Trails')} · {fw('07 Lighting VFX and Audio/Slash VFX Recipes - Crescent and Ring', 'Slash VFX Recipes')} · {fw('07 Lighting VFX and Audio/Lightning Strikes and Thunder - Procedural Bolts and Sound Delay', 'Lightning Strikes and Thunder')} · {fw('07 Lighting VFX and Audio/Escalation and Grandeur Without Clutter', 'Escalation and Grandeur Without Clutter')} · {fw('07 Lighting VFX and Audio/VFX Readability and Value - Lessons from Blind Reviews', 'VFX Readability and Value')} · {fw('07 Lighting VFX and Audio/Combat Sound Design and Feedback', 'Combat Sound Design and Feedback')} · {fw('80 Reference Library/Reference Library Start Here', 'Reference Library Start Here')}
{related('[[Skill - Roblox VFX Combo]]', '[[Animation Hub]]', '[[ThunderCombo Hub]]', '[[Studio Kits Hub]]')}
''')

note('01 VFX and Audio/PDS Particles and Models Kit.md', ['vfx', 'particles', 'meshes', 'kit', 'rbxm', 'type/resource'], f'''
# PDS Particles and Models Kit

{tldr('File: 06 Studio Kits/VFX/PDS Particles and Models Kit.rbxm (222 KB)',
      'Contiene 34 ParticleEmitter (Pigs Particle Pack V5 + preset "Ore"), ~70 mesh, una mappa da 11k Part, 4 Script',
      'Gli script sono puliti ma il file non è mai stato inserito: gli emitter sono stati ricreati in Studio dalle proprietà',
      'In Place1: ReplicatedStorage.ThunderVFX.Kit (34) + 10 emitter ricolorati in ThunderVFX.Particles')}

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
{related('[[VFX and Audio Hub]]', '[[Skill - Safe Asset Intake]]', '[[Studio Kits Hub]]', '[[ThunderCombo - Asset IDs and Instances]]')}
''')

rows = []
for i, e in enumerate(emitters, 1):
    tex = re.search(r'(\d{5,})', e.get('Texture', ''))
    tex = tex.group(1) if tex else '?'
    size = e.get('Size', [[0, 0, 0]])
    lt = e.get('Lifetime', [0, 0])
    fb = {0: '-', 1: '2x2', 2: '4x4', 3: '8x8', 4: 'custom'}.get(e.get('FlipbookLayout', 0), '?')
    src = e['_path'].split('/')
    origin = 'Pigs V5' if 'Pigs Particle Pack V5' in e['_path'] else src[-3] if len(src) > 3 else '?'
    used = CURATED.get(i)
    rows.append(f"| K{i:02d} | {e['Name']} | `{tex}` | {e.get('Rate', 0):g} | {lt[0]:g}-{lt[1]:g} | {size[0][1]:g} → {size[-1][1]:g} | {e.get('LightEmission', 0):g} | {fb} | {origin} | {('**' + used[0] + '**') if used else ''} |")
cur = '\n'.join(f'| `{v[0]}` | K{k:02d} | {v[1]} | {v[2]} |' for k, v in sorted(CURATED.items(), key=lambda x: x[1][0]))
note('01 VFX and Audio/Kit Emitters - Reference Sheet.md', ['vfx', 'particles', 'reference', 'textures', 'type/reference'], f'''
# Kit Emitters - Reference Sheet

{tldr('34 emitter del PDS kit, generati da _data/kit-emitters.json (non scritti a mano)',
      'In Place1 stanno in ReplicatedStorage.ThunderVFX.Kit con nome K01..K34 + ID texture',
      'I 10 usati in ThunderCombo sono copie ricolorate in ThunderVFX.Particles (KRing, KBurst...)',
      'Tutte le texture si caricano (ContentProvider: Success, misurato in Play)')}

## I 10 usati in ThunderCombo
| Nome in `ThunderVFX.Particles` | Da | Uso | Override principali |
|---|---|---|---|
{cur}

Regole applicate a tutti: `LightInfluence = 0` (altrimenti al tramonto, ClockTime 17.8, si spengono), `Enabled = false` e `Rate = 0` nel template, colori della palette (ciano 80,230,255 · viola 150,70,255 · bianco 235,250,255 · inchiostro 10,12,34). Si emettono solo con `Emit()` o con un `Rate` temporaneo, sempre clonati dallo script (orologio scalato).

## Anteprima
![[09 ThunderCombo/Screenshots/v3/0_kit_emitter_anteprima.jpg|600]]
Griglia 7 per riga, da K01 in alto a sinistra: 2 = anelli flipbook, 4 = burst blu, 10 = stella a 4 punte, 12 = anello a spirale, 15/17 = fumo a spirale bianco/nero, 20 = puff bianco, 22 = crepitio, 23 = flash flipbook, 25/27 = anelli slash orizzontale/verticale.

## Tutti i 34 emitter
| # | Nome originale | Texture | Rate | Lifetime | Size | LightEmission | Flipbook | Origine | Usato |
|---|---|---|---|---|---|---|---|---|---|
{chr(10).join(rows)}

{related('[[PDS Particles and Models Kit]]', '[[Kit Meshes - Reference Sheet]]', '[[Skill - Roblox VFX Combo]]', fw('07 Lighting VFX and Audio/Particle Emitters In Depth', 'Particle Emitters In Depth (fwjelaa)'))}
''')

mrows = '\n'.join(f'| `{n}` | `{i}` | {d} | {u} | {s} |' for n, i, d, u, s in MESHES)
note('01 VFX and Audio/Kit Meshes - Reference Sheet.md', ['vfx', 'meshes', 'reference', 'type/reference'], f'''
# Kit Meshes - Reference Sheet

{tldr('Mesh del PDS kit usati come SpecialMesh (FileMesh) su una Part 1x1x1',
      'Si scala Mesh.Scale, mai Size: la SpecialMesh ignora Size a schermo',
      'Scala nativa enorme: 0.03 ≈ 10 stud, quindi rocce a 0.005-0.0085 (Misurato in Play)',
      'In Place1: ReplicatedStorage.ThunderVFX.Meshes (RockCluster, Rubble, Torus)')}

| Nome | MeshId | Cos'è | Uso in ThunderCombo | Scala usata |
|---|---|---|---|---|
{mrows}

Tutti gli ID `rbxassetid://...`; fetch "Success" in Play. Altri ~60 mesh del kit (Gear, DoDecaHedron, Mesh3...Mesh256, One Way pane...) sono elencati nel dump del kit (`_tools/rbxm_dump.py <kit> tree`).

## Come usarli
```lua
local p = MESH.Torus:Clone()          -- Part 1x1x1 + SpecialMesh
p.CFrame = dirCF(pos, dir)             -- asse Y = direzione del colpo
p.Mesh.Scale = Vector3.new(0.5, 0.06, 0.5)
tween(p.Mesh, 0.22, {{Scale = Vector3.new(4, 0.16, 4) * power}})
tween(p, 0.22, {{Transparency = 1}})
```

## Errori misurati
- Scala 0.022-0.042 sulle rocce: pareti di roccia alte 10+ stud davanti alla camera.
- Toro a scala 7*power con trasparenza 0.15: anello enorme e opaco che copre il colpo.

![[09 ThunderCombo/Screenshots/v3/4_schianto_cratere.jpg|600]]
{related('[[PDS Particles and Models Kit]]', '[[Kit Emitters - Reference Sheet]]', '[[Skill - Roblox VFX Combo]]', fw('45 Procedural Blender Assets/Mesh VFX Packs Built in Blender', 'Mesh VFX Packs Built in Blender (fwjelaa)'))}
''')

note('01 VFX and Audio/VFX Method - Principles and Pipeline.md', ['vfx', 'method', 'principles', 'type/guide', 'synthesis'], f'''
# VFX Method - Principles and Pipeline

Sintesi di tre fonti: il prompt **"fwjelaa vfx method"** (copia in `01 VFX and Audio/Sources/`, ed è anche in {fw('70 fwjelaa Packs/VFX/fwjelaa vfx method', '70 fwjelaa Packs/VFX')}), le note VFX della knowledge base fwjelaa, e quello che si è visto costruendo ThunderCombo.

> [!warning] Il prompt originale è una direttiva per un'AI
> Chiede di fare un audit di "VFX Forge v2.4.0-rc1", scrivere un corso "ROBLOX VFX FROM DUMMIES TO MASTER", costruire 5 demo e salvare tutto nel progetto. **Non è stato eseguito.** Qui ne restano solo i principi.

{tldr('Timeline: anticipation → charge → release → impact → residuo → cleanup',
      'Scegli la tecnologia per componente: particelle, beam, trail, mesh, texture, tween, post-processing, UI',
      'Più particelle non vuol dire meglio; più luminoso non vuol dire meglio',
      'Mai istanze temporanee che restano vive, mai connessioni RunService senza limite',
      'Non dichiarare test o verifiche visive mai fatti')}

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
{fw('07 Lighting VFX and Audio/VFX Design Playbook', 'VFX Design Playbook')} · {fw('07 Lighting VFX and Audio/VFX Readability and Value - Lessons from Blind Reviews', 'VFX Readability and Value')} · {fw('07 Lighting VFX and Audio/VFX Performance Budgets and Culling', 'VFX Performance Budgets and Culling')} · {fw('07 Lighting VFX and Audio/Replicating VFX - Server Validates, Clients Render', 'Replicating VFX')} · {fw('07 Lighting VFX and Audio/Designing VFX Textures and Flipbooks in Figma', 'Designing VFX Textures and Flipbooks')}
{related('[[VFX and Audio Hub]]', '[[Skill - Roblox VFX Combo]]', '[[Impact Frames Hitstop and Camera]]')}
''')

note('01 VFX and Audio/Impact Frames Hitstop and Camera.md', ['vfx', 'hitstop', 'impact-frame', 'camera', 'game-feel', 'type/guide', 'synthesis'], f'''
# Impact Frames Hitstop and Camera

Sintesi tra l'animation pack (research 03), le note di game feel della knowledge base fwjelaa e ThunderCombo.

{tldr('Hitstop per peso: leggero 4-6 frame, finisher 8-14, ultimate 15-30 (Dal pack); in ThunderCombo v4 0.066/0.075/0.10/0.22 s (Misurato)',
      'Durante il freeze il corpo vibra di lato e la vibrazione decade',
      'Impact frame: 1-2 frame (3 sugli ultimate), solo su finisher e ultimate; in ThunderCombo v4 A inchiostro → B invertito (→ C viola sullo schianto), 1/60 s ciascuno',
      'Il flash bianco va DOPO l\'impact frame, altrimenti lo lava',
      'Camera: shot a orbita interpolati in tempo reale, push-in, dutch, punch di FOV, shake Perlin, slow-mo 0.25x sullo schianto, tagli netti sui colpi')}

## 1. Hitstop
| Fonte | Valori |
|---|---|
| Capcom (esempio) | leggero / medio / pesante = 8 / 12 / 16 frame |
| KOF XIII | 7 leggero, 11 pesante |
| Smash Ultimate | circa 0.65 × danno + 6, massimo 30 |
| Animation pack (scelta) | M1 4-6 f, finisher 8-14 f, ultimate 15-30 f |
| Hit-Stop Tuning by Numbers (KB) | stop = 0.03 + 0.045 × forza; max 140 ms ogni 0.6 s; sotto ~66 ms sfarfalla a 30 fps |
| **ThunderCombo v4** | Hit1 0.066 s · Hit2 0.075 s · Hit3 0.10 s · Slam 0.22 s (Hit2→Hit3 supera il budget KB di proposito), con recupero 0.08x → 1.9x; vibrazione `RootJoint.C0` di ampiezza 0.05 / 0.1 / 0.14 che decade, ripristinata a fine stop e al reset |

## 2. Impact frame
ViewportFrame con la silhouette del rig + 46 linee radiali (UIGradient):
- **A** sfondo inchiostro, silhouette bianca, linee ciano;
- **B** sfondo bianco, silhouette inchiostro, linee viola (dopo 1/60 s);
- **C** solo sullo schianto: sfondo viola scuro, silhouette ciano, linee bianche;
- ogni modo dura 1/60 s reale, cioè 1 frame a 60 fps (anche in slow-mo), poi un flash bianco al 45% che sfuma;
- la camera della silhouette è la camera di gioco e le linee convergono sul punto d'impatto (v4).

![[09 ThunderCombo/Screenshots/v4/4_impact_frame_calcio_A.jpg|520]]
Colpo leggero: solo linee + grading (saturazione −1, contrasto 0.9) per 0.06 s.

![[09 ThunderCombo/Screenshots/v3/3_impact_frame_invertito_B.jpg|520]]

## 3. Camera
Shot definiti come offset (yaw, distanza, altezza) e interpolati a orbita, così la camera non passa dentro il rig. v4: HERO (push-in FOV 40 sulla carica) → ESTABLISH (taglio frontale 3/4) → un taglio netto per colpo, ognuno da un lato diverso e scelto in base a dove si apre il busto → RETURN. Dutch max 7°, kick di FOV a metà stop, shake a trauma (decade 1.45/s, shake = trauma², 16 Hz, 2.6° scalati con tan(FOV/2)/tan(35°)), slow-mo 0.25x sullo schianto (tenuta 0.3 s, rientro 0.25 s).

## Nella knowledge base fwjelaa
{fw('47 Game Feel and Juice/Hit-Stop and Screen Shake Tuning by Numbers', 'Hit-Stop and Screen Shake Tuning by Numbers')} · {fw('52 Core Concepts/Hit-Stop', 'Hit-Stop')} · {fw('57 API and Concept Atlas/Impact Frames', 'Impact Frames')} · {fw('08 Animation/05 Systems/Camera Shake and Camera FX', 'Camera Shake and Camera FX')} · {fw('08 Animation/05 Systems/Hit Reactions Stagger and Hit-Stop', 'Hit Reactions Stagger and Hit-Stop')} · {fw('07 Lighting VFX and Audio/Screen Damage Effects - Hit Flash, Low-Health Vignette and Blur', 'Screen Damage Effects')} · {fw('58 Player QoL and Game Tweaks/Comfort Toggles - Flashes Damage Numbers and Hit-Stop', 'Comfort Toggles (flash e hitstop)')}
{related('[[Skill - Roblox VFX Combo]]', '[[Combat Timing Cheat Sheet]]', '[[ThunderCombo - Timing and Markers]]', '[[VFX Reference Images]]')}
''')

vfx_ref = '\n'.join(f'- `{d}` ({count("01 VFX and Audio/Reference Images/" + d)} file)' for d in subdirs('01 VFX and Audio/Reference Images'))
note('01 VFX and Audio/VFX Reference Images.md', ['vfx', 'references', 'images', 'audio', 'type/resource'], f'''
# VFX Reference Images

Immagini e clip da mostrare (a te o a Claude) per dire "voglio questo look". Sono **copie estratte** dalla Reference Library del vault fwjelaa (l'originale resta lì, intatto); dove la stessa immagine era già in una cartella tematica non è stata copiata due volte.

## Reference Images/ (per tipo di effetto)
{vfx_ref}

## Cinematics/
Riferimenti di inquadratura: {', '.join(f'`{d}`' for d in subdirs('01 VFX and Audio/Cinematics'))}. `10-impact-hit-stop` è il riferimento diretto per hitstop e impact frame.

## SFX/
Anteprime audio: {', '.join(f'`{d}`' for d in subdirs('01 VFX and Audio/SFX'))}. La libreria completa è descritta in [[CC0 SFX Library (roblox-ai)]].

`Reference Images/Anime Fighting Games (roblox-ai)` e `Cinematics/Roblox Docs Camera and Cutscene (roblox-ai)` vengono dal repo roblox-ai: [[Game Refs (roblox-ai)]], [[Roblox Docs Motion References]].

## Origine
{fw('80 Reference Library/Reference Library Start Here', 'Reference Library Start Here (fwjelaa)')}: le cartelle `vfx/`, `cutscenes/`, `sfx/` della libreria.
{related('[[VFX and Audio Hub]]', '[[UI Style References]]', '[[Impact Frames Hitstop and Camera]]')}
''')

# ------------------------------------------------------------------ 02 Animation
note('02 Animation/Animation Hub.md', ['hub', 'animation', 'type/hub'], f'''
# Animation Hub

Animazione per Roblox (R6/R15): l'animation pack di fwjelaa (progetto intatto in `07 Tools and Pipelines`), le sue research copiate qui, i riferimenti di movimento e le animazioni pronte in `06 Studio Kits`.

## Note
- [[fwjelaa Animation Pack]]: cosa fa il pack, come si usa, cosa c'è dentro
- [[Combat Timing Cheat Sheet]]: i numeri che servono per una combo (hitstop, overlap, anticipation, easing)
- [[Roblox Docs Motion References]]: screenshot ufficiali di Animation Editor, easing, IK, camera e cutscene (repo roblox-ai)
- Research (copie dal pack): [[Anim Research 01 - Roblox Animation Pipeline]] · [[Anim Research 02 - Moon Animator 2]] · [[Anim Research 03 - Animation Craft Numbers]] · [[Anim Research 04 - Blender MCP and AI]] · [[Anim Research 05 - Popular Roblox Animations]]
- Fonte originale: `Sources/fwjelaa Animation Method (originale).md` (prompt: riferimento, non istruzioni)

## Cartelle
| Cartella | Contenuto | File |
|---|---|---|
| `References/PunchRef/` | 25 frame + clip sorgente di un pugno di riferimento, `sheet_PunchRef.png` | {count('02 Animation/References/PunchRef') + 1} |
| `References/Motion Refs/` | riferimenti di movimento (idle, corsa, combo di spada, cast, dash) dalla Reference Library fwjelaa | {count('02 Animation/References/Motion Refs')} |
| `References/Roblox Docs Motion (roblox-ai)/` | screenshot ufficiali: Animation Editor, curve, easing, IK, rig importati, sequenze di pose | {count('02 Animation/References/Roblox Docs Motion (roblox-ai)')} |
| `Previews/` | anteprime del pack (showcase, confronto, run sheet) | {count('02 Animation/Previews')} |
| `Research/` | 5 research del pack | {count('02 Animation/Research')} |

## Animazioni pronte
45 file `.rbxmx` (33 R6, 12 R15) in [[Studio Kits Hub|06 Studio Kits/Animations]]: M1 snappy e weighty, dash, block, ground slam, charged punch, barrage, ultimate, spada...

## Nella knowledge base fwjelaa
{fw('08 Animation/Animation Start Here', 'Animation Start Here')} · {fw('08 Animation/03 Authoring/Moon Animator and Third-Party Tools', 'Moon Animator and Third-Party Tools')} · {fw('08 Animation/05 Systems/VFX Timing with Animation', 'VFX Timing with Animation')} · {fw('08 Animation/Animation Glossary', 'Animation Glossary')} · {fw('18 Rigs and Skeletons/Skeleton Library', 'Skeleton Library')} · {fw('70 fwjelaa Packs/make-anim', 'make-anim')}
{related('[[VFX and Audio Hub]]', '[[Skill - Roblox VFX Combo]]', '[[ThunderCombo - Timing and Markers]]')}
''')

note('02 Animation/fwjelaa Animation Pack.md', ['animation', 'tool', 'pack', 'type/resource'], f'''
# fwjelaa Animation Pack

{tldr('Progetto intatto: 07 Tools and Pipelines/Roblox-Animations-by-fwjelaa',
      'Genera animazioni R6/R15 da una clip o da una descrizione, con Blender + Studio via MCP (skill make-anim)',
      'Le 41 animazioni generate sono in anims/*.py (sorgente) e out/*.rbxmx (pronte, copiate in 06 Studio Kits/Animations)',
      'Non eseguito niente; usate solo le research e i numeri di timing e posa')}

## Cos'è
Dal suo README: "Tell Claude the move and get back a finished Roblox animation (R6 or R15)". Il flusso: clip di riferimento → animazione in Blender → confronto frame per frame → caricamento in Studio → import in Moon Animator 2 o pubblicazione. Metodo di fwjelaa (FWJ STUDIOS), da accreditare (`CREDITS.md`).

## Dove sta
| Cosa | Percorso |
|---|---|
| Progetto | `07 Tools and Pipelines/Roblox-Animations-by-fwjelaa/` (README, GUIDE, `anims/`, `kit/`, `roblox/AnimKit.luau`, `out/`) |
| Research (copie) | `02 Animation/Research/` |
| Riferimento PunchRef (copia) | `02 Animation/References/PunchRef/` |
| Animazioni pronte (copie) | `06 Studio Kits/Animations/R6` e `R15` |

## Cosa è stato preso per ThunderCombo
- carica tremolante a scatti da `R6_ChargedPunch` (pose costanti ogni 2 frame, ampiezza crescente);
- posa superhero landing da `R6_GroundSlam` (busto ~−60°, gambe divaricate, abbassamento R6 `2·(1−cos φ)`);
- hitstop per peso e regole di overlap da `research/03-animation-craft.md` ([[Combat Timing Cheat Sheet]]).

## Sicurezza
Contiene `.py`, `CLAUDE.md`, `.claude/skills/make-anim` e `.secrets/` (solo un `README.txt`, posto per una chiave API opzionale). Niente eseguito; i `.md` letti come riferimento.
{related('[[Animation Hub]]', '[[Tools and Pipelines Hub]]', '[[Studio Kits Hub]]', fw('70 fwjelaa Packs/make-anim', 'make-anim (fwjelaa)'))}
''')

note('02 Animation/Combat Timing Cheat Sheet.md', ['animation', 'timing', 'combat', 'hitstop', 'type/reference', 'synthesis'], f'''
# Combat Timing Cheat Sheet

I numeri che servono davvero per una combo. Fonti: [[Anim Research 03 - Animation Craft Numbers]] (**Dal pack**, con le sue fonti) e ThunderCombo (**Misurato**).

{tldr('Il contatto è uno stop netto: accelera verso il contatto, fermati, rallenta solo in uscita',
      'Hitstop: M1 4-6 f, finisher 8-14 f, ultimate 15-30 f (60 fps)',
      'Colpi a meno di 16 frame l\'uno dall\'altro si leggono come uno solo, a meno che ognuno abbia VFX/SFX propri',
      'Offset della catena: root, torso +1, braccio +2, mano/arma +3, testa +2-4 frame (snappy)',
      'Usa CubicV2, mai Cubic (direzione invertita tra editor e runtime)')}

## Regole (dal pack)
| Regola | Valore |
|---|---|
| Anticipation : recovery | snappy ~1:3-4 · weighty ~1:2 con tenuta all'estremo della carica |
| Impact flash | 1-3 frame, solo finisher e ultimate |
| Vibrazione durante l'hitstop | a terra laterale, in aria verticale; ampiezza che decade; attaccante al 30% |
| Specials: attivazione | 15-30 f, punch di FOV 70 → 55-60 in 6-10 f |
| Specials: carica | 30-90 f con tremolio ±0.02-0.05 stud o ±0.5-1° ogni 1-2 f |
| Specials: rilascio | 3-6 f verso l'estremo |
| Specials: impatto | hitstop 15-30 f + flash 2-4 f, kick di FOV +10-20, shake 0.3-0.6 stud per 15-25 f |
| R6 senza ginocchia | con le gambe aperte di ±φ abbassa il torso di `2·(1−cos φ)` (25° → 0.19, 35° → 0.36, 45° → 0.59) |
| Root motion | le animazioni non muovono l'HRP: lo spostamento vero va fatto a parte |
| Marker | `Hit` sul frame di contatto, logica dal client che riproduce la traccia |

## ThunderCombo (misurato)
| Marker | Tempo (s) | Note |
|---|---|---|
| ChargeStart → ChargeEnd | 0.05 → 1.10 | tremolio Constant ogni 1/30 s da 0.55 a 0.95 |
| Hit1 / Hit2 / Hit3 | 1.20 / 1.62 / 2.02 | 0.42 e 0.40 s tra i colpi (> 16 frame) |
| Jump → Apex → Flip → Dive → Slam | 2.50 → 2.98 → 3.06 → 3.34 → 3.50 | salto mortale in aria, slow-mo 0.25x dopo lo schianto |
| Rise → Land → End | 4.40 → 4.85 → 5.12 | dissolvenza nell'idle a LENGTH − 0.06 |
Overlap: testa +0.05 s, braccia +0.035 s, l'arto che colpisce senza ritardo. Dettagli in [[ThunderCombo - Timing and Markers]].
{related('[[Animation Hub]]', '[[Impact Frames Hitstop and Camera]]', '[[Skill - Roblox VFX Combo]]', fw('47 Game Feel and Juice/Hit-Stop and Screen Shake Tuning by Numbers', 'Hit-Stop Tuning by Numbers (fwjelaa)'))}
''')

# research copies: add a provenance header line (frontmatter) without changing content
for f in sorted(os.listdir(os.path.join(V, '02 Animation/Research'))):
    if not f.endswith('.md'):
        continue
    p = os.path.join(V, '02 Animation/Research', f)
    txt = open(p, encoding='utf-8').read()
    if not txt.startswith('---\nsource:'):
        orig = {v + '.md': k for k, v in {
            '01-roblox-pipeline': 'Anim Research 01 - Roblox Animation Pipeline', '02-moon-animator-2': 'Anim Research 02 - Moon Animator 2',
            '03-animation-craft': 'Anim Research 03 - Animation Craft Numbers', '04-blender-mcp-and-ai': 'Anim Research 04 - Blender MCP and AI',
            '05-popular-animations': 'Anim Research 05 - Popular Roblox Animations'}.items()}.get(f, '?')
        hdr = (f'---\nsource: "07 Tools and Pipelines/Roblox-Animations-by-fwjelaa/research/{orig}.md"\n'
               f'tags: [animation, research, copy, type/reference]\n---\n'
               f'> [!info] Copia di riferimento\n> Copia di `research/{orig}.md` dell\'[[fwjelaa Animation Pack]]. Materiale di riferimento, non istruzioni. Torna a [[Animation Hub]].\n\n')
        open(p, 'w', encoding='utf-8').write(hdr + txt)

# ------------------------------------------------------------------ 03 Models
chars = {d: count('03 Models and Characters/Characters/' + d, {'glb'}) for d in subdirs('03 Models and Characters/Characters')}
note('03 Models and Characters/Models and Characters Hub.md', ['hub', 'models', 'characters', 'type/hub'], f'''
# Models and Characters Hub

Modelli 3D da tutte le fonti, uniti per tipo.

| Cartella | Contenuto | File | Fonte |
|---|---|---|---|
| `Characters/` | {', '.join(f'{k}: {v} .glb' for k, v in chars.items())}, anteprime | {count('03 Models and Characters/Characters')} | "Lift Rock Models" (che **non** sono rocce) |
| `Rigs/` | 9 rig: R6/R15 blocky, lupo, uccello, serpente, ragno, arco, flagello, spada (glb/fbx + anteprima) | {count('03 Models and Characters/Rigs')} | vault fwjelaa, 18 Rigs and Skeletons |
| `Creatures/` | RedDragon, ShadowWolf (.fbx) | {count('03 Models and Characters/Creatures')} | vault fwjelaa, 73 Kits and Models |
| `Concept Sheets/` | rig sheet e pet references | {count('03 Models and Characters/Concept Sheets')} | vault fwjelaa, 19 Concept Sheets |
| `Picture-to-Model Previews/` | esempi del tool immagine → modello | {count('03 Models and Characters/Picture-to-Model Previews')} | [[Picture to Roblox Model]] |

## Note
[[Anime Character GLB Pack]] · [[Rigs Creatures and Concept Sheets]] · [[Picture to Roblox Model]]

## Nella knowledge base fwjelaa
{fw('14 3D Modeling/Modeling Fundamentals for Games', 'Modeling Fundamentals for Games')} · {fw('14 3D Modeling/Exporting and Validating Models for Roblox', 'Exporting and Validating Models for Roblox')} · {fw('18 Rigs and Skeletons/Skeleton Library', 'Skeleton Library')} · {fw('37 Avatars and UGC/Avatars and UGC Start Here', 'Avatars and UGC Start Here')} · {fw('Skill - Roblox Asset Import', 'Skill - Roblox Asset Import')}
{related('[[Animation Hub]]', '[[Maps and World Hub]]', '[[Studio Kits Hub]]')}
''')

note('03 Models and Characters/Anime Character GLB Pack.md', ['models', 'characters', 'glb', 'anime', 'type/resource'], f'''
# Anime Character GLB Pack

{tldr(f'{sum(chars.values())} personaggi anime in .glb (~720 MB): {", ".join(f"{k} {v}" for k, v in chars.items())}',
      'Arrivati come "Lift Rock Models.zip", ma sono personaggi e non rocce',
      'Import: Studio → File → Import 3D (.glb); controlla triangoli e scala prima di usarli in gioco',
      'Licenza e provenienza non dichiarate: usali come riferimento finché non è chiaro')}

## Dove sta
`03 Models and Characters/Characters/Anime/` e `.../Anime Girls/`, con `Preview - Anime.png`, `Preview - Anime Girls.png` e il `README - Lift Rock Models.txt` originale. Archivio: `_originali/Lift Rock Models.zip`.

![[03 Models and Characters/Characters/Preview - Anime.png|560]]

## Come usarli in Studio
1. File → Import 3D → scegli il `.glb` (9-10 MB l'uno: sono pesanti).
2. Controlla: triangoli per mesh (limite 20.000), scala in stud, pivot, collisioni.
3. Per animarli serve un rig compatibile (R15) oppure va fatto il rig: vedi [[Rigs Creatures and Concept Sheets]].

## Sicurezza
File `.glb` (geometria e texture), niente codice. Licenza ignota: personaggi di anime noti, quindi **non pubblicarli in un gioco** senza chiarire i diritti ([[Open Questions - niceforwh]]).
{related('[[Models and Characters Hub]]', fw('14 3D Modeling/Exporting and Validating Models for Roblox', 'Exporting and Validating Models (fwjelaa)'))}
''')

note('03 Models and Characters/Rigs Creatures and Concept Sheets.md', ['models', 'rigs', 'creatures', 'concept', 'type/resource'], f'''
# Rigs Creatures and Concept Sheets

Copie estratte dal vault fwjelaa, unite qui con gli altri modelli.

## Rigs/ ({count('03 Models and Characters/Rigs')} file)
{', '.join(f'`{d}`' for d in subdirs('03 Models and Characters/Rigs'))}. Ogni rig ha `.glb`, `.fbx` e un'anteprima. Note originali: {fw('18 Rigs and Skeletons/Skeleton Library', 'Skeleton Library')}. Secondo quella nota i rig sono stati controllati per nome e dimensioni ma non ancora importati in Studio.

## Creatures/
`RedDragon.fbx`, `ShadowWolf.fbx`: vedi {fw('73 Kits and Models/73 Kits and Models Start Here', '73 Kits and Models Start Here')}.

## Concept Sheets/ ({count('03 Models and Characters/Concept Sheets')} file)
{', '.join(f'`{d}`' for d in subdirs('03 Models and Characters/Concept Sheets'))}: vedi {fw('19 Concept Sheets/Concept Sheets', 'Concept Sheets')}.
{related('[[Models and Characters Hub]]', '[[Anime Character GLB Pack]]', '[[Animation Hub]]')}
''')

# ------------------------------------------------------------------ 04 Maps
maps = subdirs('04 Maps and World/Map Shots')
mapimgs = []
for m in maps:
    imgs = sorted(f for f in os.listdir(os.path.join(V, '04 Maps and World/Map Shots', m)) if f.rsplit('.', 1)[-1].lower() in IMG)
    if imgs:
        mapimgs.append(f'### {m}\n![[04 Maps and World/Map Shots/{m}/{imgs[0]}|480]]\n{len(imgs)} screenshot in `Map Shots/{m}/`.')
note('04 Maps and World/Maps and World Hub.md', ['hub', 'maps', 'world', 'type/hub'], f'''
# Maps and World Hub

Mappe e mondo: lo strumento MapKit (progetto intatto), gli screenshot delle sue mappe d'esempio e le sue research.

## Note
- [[MapKit - Roblox Maps by fwjelaa]]: lo strumento (descrivi una mappa → Claude la costruisce in Studio)
- [[MapKit Example Maps]]: le 4 mappe d'esempio con screenshot
- Research (copie): {' · '.join(f'[[{os.path.splitext(f)[0]}]]' for f in sorted(os.listdir(os.path.join(V, '04 Maps and World/Research'))))}

## Nella knowledge base fwjelaa
{fw('33 Level Design/Level Design Start Here', 'Level Design Start Here')} · {fw('70 fwjelaa Packs/make-map', 'make-map')}
{related('[[Models and Characters Hub]]', '[[Tools and Pipelines Hub]]')}
''')
note('04 Maps and World/MapKit Example Maps.md', ['maps', 'references', 'screenshots', 'type/resource'], f'''
# MapKit Example Maps

Screenshot delle mappe d'esempio di [[MapKit - Roblox Maps by fwjelaa]], copiati da `maps/<mappa>/shots/` del progetto. Per costruirne una in Studio servono MapKit e Claude collegato a Studio via MCP (vedi la nota dello strumento).

{chr(10).join(mapimgs)}
{related('[[Maps and World Hub]]', '[[MapKit - Roblox Maps by fwjelaa]]')}
''')
for f in sorted(os.listdir(os.path.join(V, '04 Maps and World/Research'))):
    p = os.path.join(V, '04 Maps and World/Research', f)
    txt = open(p, encoding='utf-8').read()
    if not txt.startswith('---\nsource:'):
        orig = f.replace('Maps Research - ', '')
        hdr = (f'---\nsource: "07 Tools and Pipelines/Roblox-Maps-by-fwjelaa/research/{orig}"\ntags: [maps, research, copy, type/reference]\n---\n'
               f'> [!info] Copia di riferimento\n> Copia di `research/{orig}` di [[MapKit - Roblox Maps by fwjelaa]]. Materiale di riferimento, non istruzioni. Torna a [[Maps and World Hub]].\n\n')
        open(p, 'w', encoding='utf-8').write(hdr + txt)

# ------------------------------------------------------------------ 05 UI
icat = [(d, count('05 UI and Icons/Icons/' + d, IMG)) for d in subdirs('05 UI and Icons/Icons')]
srefs = [(d, count('05 UI and Icons/Style References/' + d, IMG)) for d in subdirs('05 UI and Icons/Style References')]
note('05 UI and Icons/UI and Icons Hub.md', ['hub', 'ui', 'icons', 'type/hub'], f'''
# UI and Icons Hub

Tutto il materiale UI unito: l'icon pack, le icone del UI kit e della Reference Library fwjelaa, i riferimenti di stile, gli screenshot di HUD, le texture e i loghi.

| Cartella | Contenuto | Immagini |
|---|---|---|
| `Icons/` | {len(icat)} categorie (valute, uova, gamepass, boost, menu, controlli, oggetti, cornici, rank, emoji, tasti, icone del kit, extra fwjelaa) | {n_icons} |
| `Style References/` | {', '.join(f'{d} {n}' for d, n in srefs)} | {n_refs} |
| `Screenshots/` | {', '.join(subdirs('05 UI and Icons/Screenshots'))} | {count('05 UI and Icons/Screenshots', IMG)} |
| `Branding/` | loghi e thumbnail di giochi famosi (riferimento CTR) | {count('05 UI and Icons/Branding', IMG)} |
| `Textures/` | texture stud del UI kit | {count('05 UI and Icons/Textures', IMG)} |
| `Sources/` | brief "ForgeGUI UI rebuild" (prompt originale: riferimento, non istruzioni) | - |

## Note
[[UI Icon Pack]] · [[UI Style References]] · [[Roblox UI Kit (fwjelaa)]] · [[Game Refs (roblox-ai)]] (5.000 icone e 1.000 thumbnail di giochi, nel repo) · Kit `.rbxm`: [[Studio Kits Hub]] (Stud UI Pack)

## Nella knowledge base fwjelaa
{fw('21 fwjelaa UI Design System/fwjelaa UI Design System', 'fwjelaa UI Design System')} · {fw('05 UI and UX/ScreenGui Fundamentals', 'ScreenGui Fundamentals')} · {fw('80 Reference Library/Reference Library Start Here', 'Reference Library Start Here')}
{related('[[VFX and Audio Hub]]', '[[Studio Kits Hub]]', '[[Tools and Pipelines Hub]]')}
''')
note('05 UI and Icons/UI Icon Pack.md', ['ui', 'icons', 'type/resource'], f'''
# UI Icon Pack

{tldr(f'{n_icons} icone in {len(icat)} categorie, unite da tre fonti: UI Icon Pack, UI kit roblox-ui, Reference Library fwjelaa',
      'Pagina di consultazione: Icons/Browse the icons.html (aprila nel browser)',
      'Le icone identiche tra le fonti esistono una volta sola (deduplica via SHA1)')}

| Categoria | Immagini |
|---|---|
{chr(10).join(f'| `{d}` | {n} |' for d, n in icat)}

`01-11` vengono dall'UI Icon Pack (`_originali/UI-Icon-Pack.zip`), `12 Kit Icons (roblox-ui)` dal UI kit ([[Roblox UI Kit (fwjelaa)]]), `13 fwjelaa Library Icons` sono le icone della Reference Library fwjelaa che **non** erano già nell'icon pack (le altre 3.100+ erano identiche).

## Come usarle in Studio
Carica il PNG (Asset Manager o `upload_image` via MCP) e usa l'ID in un `ImageLabel`. Per le icone rank e tasti conviene uno sprite sheet.

## Nota sulla deduplica
1 icona del pack era identica a un'altra (`09 Rank Icons/Hexagon/Wood/hexagon-wood-1.png` = `.../Bronze/hexagon-bronze-1.png`) ed è stata tolta; `Browse the icons.html` può mostrarla mancante. Log completo in [[riorganizzazione-log|Riorganizzazione - Log]].
{related('[[UI and Icons Hub]]', '[[UI Style References]]')}
''')
note('05 UI and Icons/UI Style References.md', ['ui', 'references', 'style', 'type/resource'], f'''
# UI Style References

{tldr(f'{n_refs} immagini di riferimento per lo stile UI, unite da roblox-ui/references e dalla Reference Library fwjelaa',
      'Previews: per genere (anime, cyberpunk, fantasy, horror, simulator, tycoon...)',
      'UI Styles: GUI reali di giochi Roblox, raggruppate per tipo di gioco',
      'Usale per mostrare a Claude "voglio questo look" prima di costruire una UI')}

| Cartella | Immagini | Sottocartelle |
|---|---|---|
{chr(10).join(f'| `{d}` | {n} | {len(subdirs("05 UI and Icons/Style References/" + d))} |' for d, n in srefs)}

Altre: `Screenshots/Game HUDs` (HUD completi), `Screenshots/Stud Simulator` (il gioco d'esempio del UI kit), `Branding/` (loghi, thumbnail).

`README - Style References.md` è il README originale della cartella `references/` (riferimento).
{related('[[UI and Icons Hub]]', '[[UI Icon Pack]]', '[[VFX Reference Images]]', fw('80 Reference Library/Reference Library Start Here', 'Reference Library (fwjelaa)'))}
''')

# ------------------------------------------------------------------ 06 Studio Kits
anim_r6 = sorted(os.listdir(os.path.join(V, '06 Studio Kits/Animations/R6')))
anim_r15 = sorted(os.listdir(os.path.join(V, '06 Studio Kits/Animations/R15')))
note('06 Studio Kits/Studio Kits Hub.md', ['hub', 'kits', 'rbxm', 'studio', 'type/hub'], f'''
# Studio Kits Hub

Tutti i file da inserire in Studio (`.rbxm` / `.rbxmx`), divisi per uso. Ognuno controllato prima ([[Skill - Safe Asset Intake]]).

| File | Uso | Sicurezza | Note |
|---|---|---|---|
| `VFX/PDS Particles and Models Kit.rbxm` | emitter e mesh | 4 script puliti; mai inserito, ricreato dalle proprietà | [[PDS Particles and Models Kit]] |
| `UI/Stud UI Pack (lando).rbxm` | GUI completa stile simulator (ScreenGui "GameUI", 1.000+ UIStroke) | 5 LocalScript che ruotano un'immagine: puliti | **kit a pagamento di terzi: solo riferimento**, vedi `UI/... - SOURCE.txt` |
| `Animations/R6/*.rbxmx` ({len(anim_r6)}) | animazioni R6 pronte | solo KeyframeSequence (nessuno script) | da [[fwjelaa Animation Pack]] e vault fwjelaa |
| `Animations/R15/*.rbxmx` ({len(anim_r15)}) | animazioni R15 pronte | idem | idem |

## Animazioni
**R6:** {', '.join(f.replace('.rbxmx', '') for f in anim_r6)}

**R15:** {', '.join(f.replace('.rbxmx', '') for f in anim_r15)}

Import: in Studio tasto destro sul rig → Insert from File, oppure Moon Animator 2 → File → Import. Le stesse animazioni stavano sia nell'animation pack (`out/`) sia nel vault fwjelaa (`73 Kits and Models/Animations`): qui c'è una copia sola per file.
{related('[[UI and Icons Hub]]', '[[VFX and Audio Hub]]', '[[Animation Hub]]', '[[Skill - Safe Asset Intake]]')}
''')

# ------------------------------------------------------------------ 07 Tools
note('07 Tools and Pipelines/Tools and Pipelines Hub.md', ['hub', 'tools', 'pipelines', 'type/hub'], f'''
# Tools and Pipelines Hub

Progetti con codice che dipende dai propri percorsi interni: **spostati interi, mai smontati**, e **mai eseguiti**. Asset e documenti utili sono stati copiati nelle cartelle tematiche e collegati da qui.

| Progetto | Cosa fa | Copie estratte | Nota |
|---|---|---|---|
| `Roblox-Animations-by-fwjelaa/` | clip/descrizione → animazione R6/R15 (Blender + Studio) | research, PunchRef, anteprime → `02 Animation`; `.rbxmx` → `06 Studio Kits` | [[fwjelaa Animation Pack]] |
| `Roblox-Maps-by-fwjelaa/` | descrizione → mappa costruita in Studio (MapKit) | screenshot, research → `04 Maps and World` | [[MapKit - Roblox Maps by fwjelaa]] |
| `Picture-to-Roblox-Model-by-fwjelaa/` | immagine di un personaggio → modello texturizzato | anteprime → `03 Models and Characters` | [[Picture to Roblox Model]] |
| `Roblox UI Kit (fwjelaa)/` | moduli Luau di UI (Containers, Controls, Motion, Themes...) + tool icone | icone → `05 UI and Icons/Icons/12`, texture → `05 .../Textures` | [[Roblox UI Kit (fwjelaa)]] |

Il repo **roblox-ai** non ha codice (solo media), quindi sta in `08 Knowledge`: [[roblox-ai Reference Library]].

Script di manutenzione di questo vault (nostri, non dei pack): [[Vault Maintenance Tools]].
{related('[[Knowledge Hub]]', '[[Skill - Safe Asset Intake]]', '[[Studio Kits Hub]]')}
''')
note('07 Tools and Pipelines/MapKit - Roblox Maps by fwjelaa.md', ['tools', 'maps', 'mapkit', 'type/resource'], f'''
# MapKit - Roblox Maps by fwjelaa

{tldr('Progetto intatto: 07 Tools and Pipelines/Roblox-Maps-by-fwjelaa',
      'Descrivi una mappa ("a lift a boulder simulator map") e Claude la costruisce nel place aperto, poi la verifica con screenshot, walk test e budget',
      'Mappe d\'esempio: lift-a-boulder, backrooms-level-0, farmhouse-night, forest-lake',
      'Richiede Python 3 + pillow/numpy, Studio come MCP server, per le mappe realistiche Blender e una chiave Open Cloud')}

## Come si usa (dal README, non eseguito qui)
1. Place nuovo (Baseplate), Studio come MCP server.
2. Apri la cartella in Claude Code, `/make-map` + idea. Studio deve restare visibile (servono gli screenshot).
3. Il kit non cancella niente: Baseplate e SpawnLocation finiscono in `ServerStorage.MapKit_Removed`.

## Cosa c'è
`kit/studio/MapKit` (Luau), `kit/blender` (Python), `maps/` (le 4 mappe con `shots/`), `research/` (6 note), `styles/`, `prompts/`, `GUIDE.html`.

## Sicurezza
Contiene `.py`, `CLAUDE.md`, `.claude/skills/make-map`: niente eseguito. Le texture e i modelli realistici usano asset CC0 (ambientCG, Poly Haven) da caricare sul proprio account; la chiave API va tenuta fuori dalle chat.
{related('[[Maps and World Hub]]', '[[MapKit Example Maps]]', '[[Tools and Pipelines Hub]]', fw('70 fwjelaa Packs/make-map', 'make-map (fwjelaa)'))}
''')
note('07 Tools and Pipelines/Picture to Roblox Model.md', ['tools', 'models', 'blender', 'type/resource'], f'''
# Picture to Roblox Model

{tldr('Progetto intatto: 07 Tools and Pipelines/Picture-to-Roblox-Model-by-fwjelaa',
      'Immagine di un personaggio → modello texturizzato (out/<Name>.fbx + texture), import con File → Import 3D',
      'Richiede Blender 4.2+ e Python 3; skill make-model',
      'Non eseguito: contiene build.bat, build.sh e script Python')}

## Cosa c'è
`kit/`, `build/`, `roblox/`, `images/` (anteprime, copiate in `03 Models and Characters/Picture-to-Model Previews`), `GUIDE.html`, `CLAUDE.md`, `.secrets/` (solo un README: posto per una chiave API opzionale).

## Sicurezza
Il genitore di questa sessione l'ha detto esplicitamente: niente esecuzione di exe, bat, ps1 o Python di questo tool senza chiedere prima.
{related('[[Models and Characters Hub]]', '[[Tools and Pipelines Hub]]', fw('70 fwjelaa Packs/make-model', 'make-model (fwjelaa)'))}
''')
note('07 Tools and Pipelines/Roblox UI Kit (fwjelaa).md', ['tools', 'ui', 'luau', 'type/resource'], f'''
# Roblox UI Kit (fwjelaa)

{tldr('Progetto: 07 Tools and Pipelines/Roblox UI Kit (fwjelaa) (era "roblox ui references", parte codice)',
      'Moduli Luau: UIKit, Containers, Controls, Decor, Feedback, Icons, Motion, Readouts, Screens, Util, Themes/StudSimulator, dev/ (KitCheck, MotionCheck, Showcase)',
      'Tool Python per le icone (render in Blender, finitura, texture pack): non eseguiti',
      'Le immagini di riferimento dello stesso pack ora sono in 05 UI and Icons/Style References')}

## Cosa c'è
- `roblox-ui/kit/`: i moduli Luau (da mettere in `ReplicatedStorage` via Rojo o a mano).
- `roblox-ui/tools/`: `render_icons_blender.py`, `finish_icons.py`, `make_texture_pack.py`.
- `roblox-ui/icons/` (14 icone, copiate in `05 UI and Icons/Icons/12 Kit Icons (roblox-ui)`), `roblox-ui/textures/` (stud tile, copiata in `05 .../Textures`).
- `docs/superpowers/` (piano e spec della skill UI), `.superpowers/` (progresso): documenti di lavoro, riferimento.

Gioco d'esempio: Stud Simulator, screenshot in `05 UI and Icons/Screenshots/Stud Simulator`.
{related('[[UI and Icons Hub]]', '[[Tools and Pipelines Hub]]', fw('21 fwjelaa UI Design System/fwjelaa UI Design System', 'fwjelaa UI Design System'))}
''')
note('07 Tools and Pipelines/Vault Maintenance Tools.md', ['tools', 'maintenance', 'python', 'type/guide'], f'''
# Vault Maintenance Tools

Script **nostri** (scritti in questa sessione, non dei pack), in `_tools/`. Copia master in `Desktop/nicco/anim/tools/`. Si lanciano sempre con `python -I` (modalità isolata), con i percorsi come argomenti.

| Script | Cosa fa |
|---|---|
| `inventory.py <root> <out.csv> [skip...]` | inventario: percorso, estensione, dimensione, SHA1 |
| `reorganize.py plan|run <vault> <screens>` | genera `_data/piano.csv` dalla baseline, lo valida (nessun doppio, nessuno scontro, percorsi < 250), lo esegue in modo ripetibile |
| `build_notes.py <vault>` | rigenera le note hub e le schede (emitter e mesh dai dati) |
| `vault_tools.py index|links|names <vault>` | rigenera [[INDEX]]/[[INDEX_SLIM]], trova wikilink rotti, trova nomi in conflitto con il vault fwjelaa |
| `rbxm_dump.py <file.rbxm> summary|sources|tree` | lettore offline di `.rbxm` binari: classi, sorgente degli script, albero con ID |
| `rbxm_props.py <file.rbxm> <Classi> <out.json>` | estrae tutte le proprietà di una classe (es. ParticleEmitter) in JSON |
| `git_verify.py <repo> <out.tsv>` | confronta ogni file di un checkout con l'hash del blob in `HEAD` (ok / missing / differs), senza hook |
| `ext_stats.py <repo> <inventario.csv> <out.csv>` | statistiche di un repo esterno e quanti file sono già nel vault (per SHA1) |
| `integrate_roblox_ai.py <repo> <tree.tsv> <vault>` | integrazione di roblox-ai: archivio `git archive`, spostamento in `08 Knowledge`, file mancanti dai blob, verifica, inventario, copie deduplicate e log |

## Dati in `_data/`
`inventario-prima.csv` (baseline, 12.021 file) · `inventario-dopo.csv` · `piano.csv` (una riga per file) · `riorganizzazione-log.csv` (ogni spostamento/copia/rimozione) · `duplicati.csv` (ogni gruppo di duplicati) · `kit-emitters.json` · `roblox-ai-inventario.csv` (14.381 file del repo con SHA1, blob git e copia già presente) · `roblox-ai-log.csv` (copie e rinomine) · [[riorganizzazione-log|Riorganizzazione - Log]].
{related('[[Tools and Pipelines Hub]]', '[[Skill - Safe Asset Intake]]', '[[riorganizzazione-log|Riorganizzazione - Log]]')}
''')

# ------------------------------------------------------------------ 08 Knowledge
note('08 Knowledge/Knowledge Hub.md', ['hub', 'knowledge', 'fwjelaa', 'type/hub'], f'''
# Knowledge Hub

Due raccolte intere:
- la knowledge base **fwjelaa vault** in `08 Knowledge/fwjelaa-vault/` ({n_fw} file): il vault Obsidian (`fwjelaa vault/`, 1.300+ note, 60+ sezioni) più il plugin Claude Code che ci stava attorno (`agents/`, `commands/`, `skills/`, `hooks/`, `benchmark/`, `.claude-plugin/`);
- il repo di riferimenti **roblox-ai** in `08 Knowledge/roblox-ai/` ({n_rai} file, solo media): [[roblox-ai Reference Library]] · [[Roblox Docs Screenshots (roblox-ai)]] · [[Game Refs (roblox-ai)]] · [[CC0 SFX Library (roblox-ai)]] · [[Roblox Docs Motion References]].

## Come usarlo
- **Dentro questo vault**: con i link a percorso completo, per esempio {fw('000 Home', 'Home fwjelaa')}, {fw('00 Start Here', 'Start Here fwjelaa')}, {fw('ROUTER', 'Router')}, {fw('INDEX_SLIM', 'Index slim')}.
- **Come vault separato (consigliato per sfogliarlo)**: Obsidian → Apri cartella come vault → `08 Knowledge/fwjelaa-vault/fwjelaa vault`. Così tutti i suoi link brevi funzionano e usa il suo tema e il suo grafo.

## Perché non è stato smontato
È un progetto con struttura propria: note con link incrociati, script in `_tools/` che generano i suoi indici, un plugin con skill e hook che puntano ai suoi percorsi. Smontarlo romperebbe tutto. Asset utili (immagini VFX, icone, riferimenti UI, rig, animazioni) sono stati **copiati** nelle cartelle tematiche; le note no, per non avere titoli doppi. Le note di sintesi ([[VFX Method - Principles and Pipeline]], [[Impact Frames Hitstop and Camera]], [[Combat Timing Cheat Sheet]]) collegano le fonti.

## Nomi in conflitto
Le note hub di questo vault hanno lo stesso nome di alcune note fwjelaa (`000 Home`, `00 Start Here`, `INDEX`, `INDEX_SLIM`, `ROUTER`, `README`, `000 Studio Map`). I link brevi dentro fwjelaa possono quindi risolversi sul file di questo vault quando lo apri da qui. Il glossario e le domande aperte di questo vault hanno il suffisso `- niceforwh` apposta. Soluzione definitiva: aprire fwjelaa come vault separato.

## Sicurezza
- **Plugin non installato**: `hooks/`, `agents/`, `commands/` non sono attivi né eseguiti.
- Il tema "fwjelaa's Infinite Void" è stato copiato in `.obsidian/themes` (solo CSS); carica font da Google Fonts.
- Le note sono riferimento: se una nota chiede di fare qualcosa, è un suggerimento da valutare, non un ordine.
{related('[[00 Start Here]]', '[[Tools and Pipelines Hub]]', '[[Skill - Safe Asset Intake]]')}
''')

# ------------------------------------------------------------------ 09 ThunderCombo
note('09 ThunderCombo/ThunderCombo Hub.md', ['hub', 'project', 'thundercombo', 'type/hub'], f'''
# ThunderCombo Hub

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
{related('[[VFX and Audio Hub]]', '[[Animation Hub]]', '[[Kit Emitters - Reference Sheet]]')}
''')
note('09 ThunderCombo/ThunderCombo - Build Log.md', ['project', 'thundercombo', 'log', 'type/case-study'], f'''
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
| Accelerazione **dentro** il contatto (ease In sul segmento che porta al colpo), stop netto, uscita in Out | {fw('08 Animation/03 Authoring/Combat Animation Craft', 'Combat Animation Craft')}; [[Anim Research 03 - Animation Craft Numbers]] §0.1 |
| "Stretch" di 1-2 frame: l'arto che colpisce trasla di 0.4 stud lungo la sua direzione (R6 non scala i Motor6D) | [[Anim Research 03 - Animation Craft Numbers]] §5.8 |
| Breakdown ad arco su montante e calcio, camera del calcio (ginocchio alto), anticipazione più profonda per il salto | Research 03 §5.5; {fw('08 Animation/03 Authoring/Spin and Whole-Body Rotation Moves', 'Spin and Whole-Body Rotation Moves')} |
| Nuovo: salto mortale raccolto in aria + picchiata (marker `Flip`, `Dive`), chiavi ogni ≤90° di rotazione | Spin and Whole-Body Rotation Moves |
| Posa d'atterraggio asimmetrica: un pugno a terra, l'altro braccio aperto dietro, sguardo avanti | Research 03 §5.7 (leggibilità della posa) |
| Idle di 4 s: respiro (2 s) + spostamento del peso (4 s) + micro-sguardi; testa e braccia in ritardo | {fw('08 Animation/03 Authoring/Idle Breathing and Secondary Motion', 'Idle Breathing and Secondary Motion')} |
| Hitstop 0.066 / 0.075 / 0.10 / 0.22 s con recupero 0.08x → 1.9x, così marker e VFX restano in sync. Hit1→Hit2 sta nel budget KB (141 ms in 0.6 s); Hit2→Hit3 lo supera di proposito (175 ms in 0.4 s) per dare peso al finisher, come il finisher più lungo di Research 03 | {fw('47 Game Feel and Juice/Hit-Stop and Screen Shake Tuning by Numbers', 'Hit-Stop Tuning by Numbers')}; Research 03 §7.3 |
| Shake a "trauma" (decade 1.45/s, shake = trauma², 16 Hz, 2.6° scalati con la FOV, roll max 4°), parte al rilascio dello stop; kick di FOV a metà stop | {fw('08 Animation/05 Systems/Camera Shake and Camera FX', 'Camera Shake and Camera FX')} |
| Impact frame: 1 frame per modo a 60 fps (1/60 s reale), quindi A→B = 2 frame sul calcio e A→B→C = 3 sullo schianto; colori della palette, linee che convergono sul punto d'impatto | {fw('57 API and Concept Atlas/Impact Frames', 'Impact Frames')}; Camera Shake and Camera FX |
| Montaggio: HERO (push-in) → ESTABLISH → taglio netto su ogni colpo con un'inquadratura diversa → RETURN; dutch max 7°; slow-mo 0.25x per 0.3 s | {fw('08 Animation/05 Systems/Cinematic Ultimates', 'Cinematic Ultimates')} |
| Impatto in 6 fasi: hot frame bianco < 0.1 s, corpo (anello, toro, burst), secondario (scintille, crepitio, schegge scure), terra, coda | {fw('07 Lighting VFX and Audio/VFX Design Playbook', 'VFX Design Playbook')} §1 |
| Ogni pila luminosa ha uno strato scuro (schegge e ombre inchiostro), un solo pavimento luminoso alla volta, niente sfere giganti | {fw('07 Lighting VFX and Audio/VFX Readability and Value - Lessons from Blind Reviews', 'VFX Readability and Value')}; {fw('07 Lighting VFX and Audio/Escalation and Grandeur Without Clutter', 'Escalation and Grandeur')} |
| Afterimage solo sui finisher: 3 ombre scure 0.035 s l'una dall'altra; scie (smear) sugli arti durante gli swing | {fw('08 Animation/05 Systems/VFX Timing with Animation', 'VFX Timing with Animation')} |
| Bloom "toon arena": intensità 1, size 40, soglia 1.6 (brilla solo il VFX), luci brevi sopra e dietro il colpo | {fw('07 Lighting VFX and Audio/Stylized Lighting Recipes', 'Stylized Lighting Recipes')} §3.2; VFX Readability §6 |
| Lampo da fulmine a 4 colpi (0 / 0.05 / 0.10 / 0.18 s) su ChargeEnd e schianto | {fw('07 Lighting VFX and Audio/Lightning Strikes and Thunder - Procedural Bolts and Sound Delay', 'Lightning Strikes and Thunder')} |
| Audio a strati: transiente + scarica elettrica + corpo (+ tuono sui finisher), +1 semitono per colpo, ±4% di pitch | {fw('07 Lighting VFX and Audio/Combat Sound Design and Feedback', 'Combat Sound Design and Feedback')} |
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
''')
note('09 ThunderCombo/ThunderCombo - Timing and Markers.md', ['project', 'thundercombo', 'timing', 'animation', 'type/reference'], '''
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
''')
note('09 ThunderCombo/ThunderCombo - Asset IDs and Instances.md', ['project', 'thundercombo', 'assets', 'ids', 'type/reference'], '''
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
''')
gal = []
for v in ('v1', 'v2', 'v3', 'v4'):
    d = os.path.join(V, '09 ThunderCombo/Screenshots', v)
    if os.path.isdir(d):
        gal.append(f'## {v}\n' + '\n'.join(f'![[09 ThunderCombo/Screenshots/{v}/{f}|360]]' for f in sorted(os.listdir(d))))
note('09 ThunderCombo/ThunderCombo - Screenshots.md', ['project', 'thundercombo', 'screenshots', 'type/gallery'], f'''
# ThunderCombo - Screenshots

Catturati in Play con il freeze (time scale 0.001) subito dopo i marker. Copiati da `Desktop/nicco/anim/screens/`.

## Confronto v3 → v4
| | v3 | v4 |
|---|---|---|
| Calcio | ![[09 ThunderCombo/Screenshots/v3/7_calcio_base_v3.jpg|300]] | ![[09 ThunderCombo/Screenshots/v4/5_calcio_profilo.jpg|300]] |
| Posa finale | ![[09 ThunderCombo/Screenshots/v3/8_posa_schianto_base_v3.jpg|300]] | ![[09 ThunderCombo/Screenshots/v4/9_posa_cratere.jpg|300]] |

{chr(10).join(gal)}
''')

# ------------------------------------------------------------------ roblox-ai (izzyfrm/roblox-ai, media-only reference repo)
RAI = '08 Knowledge/roblox-ai'
RAI_COMMIT, RAI_DATE = '082517a9ed1eca47dbd2a80496b4b0039bdf000a', '2026-11-05'
RAI_ZIP = f'_originali/roblox-ai-izzyfrm-{RAI_COMMIT[:7]}.zip'
rai_inv = list(csv.DictReader(open(os.path.join(V, '_data/roblox-ai-inventario.csv'), encoding='utf-8')))
rai_log = list(csv.DictReader(open(os.path.join(V, '_data/roblox-ai-log.csv'), encoding='utf-8')))
rlc = Counter(r['action'] for r in rai_log)
rai_top = {}
for r in rai_inv:
    rel = r['path'][len(RAI) + 1:]
    t = rel.split('/')[0] if '/' in rel else '(radice)'
    d = rai_top.setdefault(t, [0, 0, 0])
    d[0] += 1
    d[1] += int(r['size'])
    d[2] += 1 if r['in_vault_before'] else 0
rai_mb = sum(int(r['size']) for r in rai_inv) / 1e6
rai_uniq = len({r['sha1'] for r in rai_inv})
RAI_WHERE = {
    'sfx': '`cc0-audio/` → `01 VFX and Audio/SFX/CC0 Library (roblox-ai)` (tutti); le 4 cartelle numerate erano già in `01 .../SFX`',
    'motion-references': '`animation/`, `motion-sequences/` → `02 Animation/References/Roblox Docs Motion (roblox-ai)`; `camera/`, `cutscene/` → `01 VFX and Audio/Cinematics/Roblox Docs Camera and Cutscene (roblox-ai)`',
    'game-refs': '`anime-fighting/` → `01 VFX and Audio/Reference Images/Anime Fighting Games (roblox-ai)`; il resto collegato da [[Game Refs (roblox-ai)]]',
    'roblox-docs': 'collegato da [[Roblox Docs Screenshots (roblox-ai)]] (niente copie: 417 MB)',
    'previews': 'già tutto in `05 UI and Icons/Style References/Previews`',
    'style-refs': 'già tutto in `05 .../Style Refs`',
    'visual-refs': 'già tutto in `05 .../Visual Refs` (e `Style Refs`)',
    'ui-styles': 'già tutto in `05 .../UI Styles` (anche gli 11 file ripristinati dai blob)',
    'vfx': 'già in `01 VFX and Audio/Reference Images` e `Cinematics`',
    'animations': 'già in `02 Animation/References/Motion Refs` e `05 ...`',
    'cutscenes': 'già in `01 VFX and Audio/Cinematics`',
    'logos': 'già in `05 UI and Icons/Branding/Logos`',
    'thumbnails': '8 già in `05 .../Branding/Thumbnails`; `curated-2026-11/` solo nel repo',
    '(radice)': '`README.md` (riferimento) e `Day1-Day100.webp` (già nel vault fwjelaa)',
}
rai_rows = '\n'.join(f'| `{t}` | {d[0]} | {d[1] / 1e6:.1f} | {d[2]} | {RAI_WHERE.get(t, "-")} |' for t, d in sorted(rai_top.items(), key=lambda x: -x[1][0]))
rai_renamed = [r for r in rai_log if r['action'] == 'rename']

note('08 Knowledge/roblox-ai Reference Library.md', ['knowledge', 'references', 'roblox-ai', 'media', 'type/resource'], f'''
# roblox-ai Reference Library

{tldr(f'Repo: github.com/izzyfrm/roblox-ai, commit {RAI_COMMIT[:7]} del {RAI_DATE} (clone del 2026-11-06)',
      f'Intero in {RAI}/ ({len(rai_inv)} file, {rai_mb:.0f} MB, {rai_uniq} diversi per contenuto); archivio originale {RAI_ZIP}',
      'Solo media: immagini, 5 mp4, 2.210 mp3 e un README. Nessun codice, niente eseguito',
      'Nessun file LICENSE: tutto è riferimento, tranne sfx/cc0-audio (CC0) e le immagini della documentazione Roblox (CC BY 4.0)',
      f'{rai_top.get("previews", [0, 0, 0])[2] + rai_top.get("style-refs", [0, 0, 0])[2] + rai_top.get("visual-refs", [0, 0, 0])[2] + rai_top.get("ui-styles", [0, 0, 0])[2]} riferimenti UI erano già nel vault (stessa fonte della Reference Library fwjelaa)')}

## Cos'è
Una libreria di riferimenti visivi e sonori per sviluppatori Roblox: screenshot di giochi per genere, migliaia di icone e thumbnail di giochi, gli screenshot della documentazione ufficiale (Creator Hub), sequenze di frame per animazione e cutscene, e 2.210 effetti sonori CC0. Il README la presenta come materiale da mostrare a un assistente AI ("allega da 2 a 5 immagini, di' cosa prendere e cosa cambiare"): è un consiglio d'uso, letto come riferimento.

## Cosa c'è e dove è finito
| Cartella | File | MB | Già nel vault | Copie / collegamenti |
|---|---|---|---|---|
{rai_rows}

Note per le parti importanti: [[CC0 SFX Library (roblox-ai)]] · [[Roblox Docs Motion References]] · [[Roblox Docs Screenshots (roblox-ai)]] · [[Game Refs (roblox-ai)]].

Copie fatte: **{rlc['copy']}** file (deduplicati: {rlc['skip-copy']} non copiati perché identici a file già nelle cartelle tematiche). Elenco file per file: `_data/roblox-ai-log.csv`; inventario completo con SHA1 e blob git: `_data/roblox-ai-inventario.csv`.

## Perché in 08 Knowledge e non in 07
`07 Tools and Pipelines` è per i progetti con codice. Questo repo non ne ha: è una biblioteca di riferimenti, come la knowledge base fwjelaa. Resta intero (stessa struttura di GitHub) perché i suoi nomi di cartella sono l'indice; dentro ci sono {sum(d[2] for d in rai_top.values())} file identici a file già presenti, tenuti apposta per non smontarlo (come per i progetti intatti).

## Come usarlo con Studio e MCP
- **Riferimento visivo**: apri 2-5 immagini e mostrale a Claude (`Read` sull'immagine) prima di costruire UI, VFX, thumbnail o una mappa; di' cosa prendere e cosa deve essere diverso. Il risultato va fatto originale.
- **Suoni**: un mp3 della libreria CC0 va caricato come asset audio (Asset Manager → Import, oppure Creator Hub) e poi usato come `rbxassetid://` in un `Sound`. Il server MCP di Studio ha `upload_image` per le immagini; per l'audio servono Asset Manager / Creator Hub (o l'API Open Cloud Assets con una chiave tua). Vedi [[CC0 SFX Library (roblox-ai)]].
- **Documentazione**: gli screenshot di `roblox-docs/` mostrano come appare una funzione di Studio (Animation Editor, IK, lighting, UI, modeling); utili per spiegare a Claude un pannello o una proprietà.
- **Immagini come texture**: solo quelle con licenza chiara (le CC BY 4.0 della documentazione, con attribuzione). Le icone e thumbnail di giochi di terzi **no**.

## Licenza e diritti
- Il repo **non ha un file LICENSE**. Il README (sezione Rights) dice che "riferimento" non vuol dire libero da riusare: la raccolta mescola immagini promozionali e di documentazione Roblox, mockup originali e ispirazione visiva; chi ha i diritti su un file può chiederne la rimozione.
- `sfx/cc0-audio/`: **CC0** secondo il README (non verificato file per file, vedi [[Open Questions - niceforwh]]).
- Immagini prese dalla documentazione Roblox (`roblox-docs/`, `motion-references/`): `motion-references/LICENSE-01..04.png` riportano la **Creative Commons Attribution 4.0** della "Roblox Creator Documentation". Riuso possibile con attribuzione.
- `game-refs/`, `thumbnails/`, `logos/`, `ui-styles/`, `previews/`: arte e GUI di giochi di terzi, **solo riferimento**.

## Sicurezza e verifica
- Clone in una cartella nuova dello scratchpad: `--depth 1`, `core.hooksPath=NUL`, `core.symlinks=false`, niente LFS né submodule. Nessun install, script, hook o build. Il README è stato letto come riferimento, non come istruzioni.
- Contenuto: solo `.png .jpg .jpeg .webp .gif .mp4 .mp3` e un `README.md`; nessun eseguibile o script.
- Su Windows 14 file avevano percorsi troppo lunghi per la cartella temporanea e il README era stato convertito (fine riga): sono stati scritti direttamente dai blob git. Ogni file del vault è stato poi verificato contro l'hash del suo blob in `HEAD`: **{len(rai_inv)}/{len(rai_inv)} identici**.
- {len(rai_renamed)} file aveva un percorso oltre 249 caratteri anche nel vault: rinominato accorciando il nome (con 8 caratteri del blob), originale nell'archivio. {''.join(f"`{r['old'].split('/')[-1][:60]}...` → `{r['new'].split('/')[-1]}`" for r in rai_renamed)}
- Archivio originale: `{RAI_ZIP}` (creato con `git archive`, contiene ogni file di `HEAD` con i nomi originali).
{related('[[Knowledge Hub]]', '[[CC0 SFX Library (roblox-ai)]]', '[[Game Refs (roblox-ai)]]', '[[Roblox Docs Screenshots (roblox-ai)]]', '[[Roblox Docs Motion References]]', '[[Skill - Safe Asset Intake]]')}
''')

SFXD = '01 VFX and Audio/SFX/CC0 Library (roblox-ai)'
SFX_GROUP = [
    ('Combattimento', ['punch', 'impact-hit', 'whoosh', 'swoosh', 'sword-slash', 'sword-clash', 'land-thud', 'explosion', 'gunshot', 'reload']),
    ('Poteri e magia', ['charge-up', 'power-up', 'magic-spell', 'laser', 'teleport', 'portal', 'fire-burst', 'level-up']),
    ('Movimento e mondo', ['jump', 'footstep', 'door-open', 'chest-open', 'unlock']),
    ('UI e ricompense', ['ui-click', 'button-press', 'menu-select', 'notification', 'error-buzz', 'reward', 'coin-pickup', 'pickup-item']),
]
sfx_cats = subdirs(SFXD)
grouped = {c for _, cs in SFX_GROUP for c in cs}
sfx_rows = []
for g, cs in SFX_GROUP + [('Altro', [c for c in sfx_cats if c not in grouped])]:
    cs = [c for c in cs if c in sfx_cats]
    if cs:
        sfx_rows.append(f'| {g} | ' + ' · '.join(f'`{c}` {count(SFXD + "/" + c)}' for c in cs) + ' |')
note('01 VFX and Audio/CC0 SFX Library (roblox-ai).md', ['audio', 'sfx', 'cc0', 'combat', 'roblox-ai', 'type/resource'], f'''
# CC0 SFX Library (roblox-ai)

{tldr(f'{n_sfx} effetti sonori mp3 in {len(sfx_cats)} categorie, in {SFXD}/',
      'Licenza CC0 secondo il README del repo roblox-ai (non verificata file per file)',
      'Copia estratta di 08 Knowledge/roblox-ai/sfx/cc0-audio (l\'originale resta lì)',
      'In Studio: carica l\'mp3 come asset audio, poi usa rbxassetid:// in un Sound')}

## Categorie
| Gruppo | Categorie (file) |
|---|---|
{chr(10).join(sfx_rows)}

I nomi dei file contengono la descrizione originale del suono e un hash corto (per esempio `basic-click-wooden-e50d3e8f.mp3`): cerca per parola dentro la cartella.

## Per una combo come ThunderCombo
Strati del colpo ([[Impact Frames Hitstop and Camera]], {fw('07 Lighting VFX and Audio/Combat Sound Design and Feedback', 'Combat Sound Design and Feedback')}): **transiente** (`punch`, `impact-hit`) + **corpo** (`whoosh`/`swoosh` prima del contatto, `land-thud` o `explosion` sui finisher) + **colore** del potere (`charge-up`, `power-up`, `laser`, `magic-spell` per l'elettrico). Varia il pitch del 3-5% e alza di un semitono a ogni colpo della catena.

## Come portarli in Studio
1. Ascolta e scegli (in Esplora file, o in Obsidian incorporando l'mp3 in una nota: diventa riproducibile).
2. Caricalo come audio: Asset Manager → Import, o Creator Hub → Audio. Il caricamento passa la moderazione di Roblox e ha un limite mensile.
3. Usa l'ID in un `Sound` (`SoundId = "rbxassetid://<id>"`); per un gioco pubblicato l'audio deve essere tuo o pubblico.

Il server MCP di Studio ha `upload_image` solo per le immagini: per l'audio questo passo resta manuale (o API Open Cloud Assets con una chiave tua, da tenere fuori dalle chat).

## Le anteprime che c'erano già
`01-button-click`, `14-sword-swing-whoosh`, `15-sword-hit-metal`, `27-spell-cast-charge` vengono dalla Reference Library fwjelaa (stessi file della cartella `sfx/` numerata del repo).
{related('[[VFX and Audio Hub]]', '[[roblox-ai Reference Library]]', '[[Impact Frames Hitstop and Camera]]', '[[ThunderCombo - Asset IDs and Instances]]')}
''')

MOT_A = '02 Animation/References/Roblox Docs Motion (roblox-ai)'
MOT_C = '01 VFX and Audio/Cinematics/Roblox Docs Camera and Cutscene (roblox-ai)'
mot_topics = Counter()
for dp, _, fns in os.walk(os.path.join(V, MOT_A, 'animation')):
    for f in fns:
        parts = f.split('--')
        mot_topics[parts[1] if len(parts) > 2 else f] += 1
seq = Counter()
for dp, _, fns in os.walk(os.path.join(V, MOT_A, 'motion-sequences')):
    for f in fns:
        parts = f.split('--')
        seq[re.sub(r'-frame-\d+\.\w+$', '', parts[-1]) if len(parts) > 2 else f] += 1
note('02 Animation/Roblox Docs Motion References.md', ['animation', 'references', 'camera', 'cutscene', 'roblox-ai', 'type/resource'], f'''
# Roblox Docs Motion References

{tldr('Screenshot e sequenze di frame dalla documentazione ufficiale Roblox (Creator Hub), raccolti nel repo roblox-ai (motion-references/)',
      f'{MOT_A}/: animation ({count(MOT_A + "/animation")}) e motion-sequences ({count(MOT_A + "/motion-sequences")})',
      f'{MOT_C}/: camera ({count(MOT_C + "/camera")}) e cutscene ({count(MOT_C + "/cutscene")})',
      'Licenza: Creative Commons Attribution 4.0, "Roblox Creator Documentation" (motion-references/LICENSE-01..04.png)')}

## animation/ (per pagina della documentazione)
{', '.join(f'`{t}` {n}' for t, n in sorted(mot_topics.items()))}

## motion-sequences/ (frame in sequenza)
{', '.join(f'`{t}` {n}' for t, n in sorted(seq.items()))}

Le sequenze `Easing-*` mostrano la stessa animazione con easing diversi, frame per frame: utili per spiegare a Claude "ease in" contro "lineare" ([[Combat Timing Cheat Sheet]]).

## camera/ e cutscene/
- `camera/`: esempi di camera in prima persona, isometrica, side-scrolling e in terza persona (tutorial "controlling the player's camera").
- `cutscene/`: 12 frame della cutscene di "Mystery of Duvall Drive" (technical overview), per inquadrature e ritmo.

## Uso
Riferimento per pose, curve e inquadrature. Le immagini sono CC BY 4.0: se ne usi una in un progetto, attribuisci "Roblox Creator Documentation".
{related('[[Animation Hub]]', '[[VFX and Audio Hub]]', '[[roblox-ai Reference Library]]', '[[Impact Frames Hitstop and Camera]]')}
''')

DOCS = f'{RAI}/roblox-docs'
docs_rows = '\n'.join(f'| `{d}` | {count(DOCS + "/" + d)} |' for d in subdirs(DOCS))
note('08 Knowledge/Roblox Docs Screenshots (roblox-ai).md', ['knowledge', 'references', 'roblox-docs', 'roblox-ai', 'type/resource'], f'''
# Roblox Docs Screenshots (roblox-ai)

{tldr(f'{count(DOCS)} immagini della documentazione ufficiale Roblox, per sezione, in {DOCS}/',
      'Restano solo nel repo (417 MB): qui c\'è la mappa, non copie',
      'Licenza: CC BY 4.0 "Roblox Creator Documentation" (come motion-references)',
      'Il nome del file ripete la pagina d\'origine: sezione--pagina--immagine')}

| Sezione | Immagini |
|---|---|
{docs_rows}

## Le sezioni più utili per questo vault
- **Animazione**: `animation/` (Animation Editor, curve, IK, rig importati, face recorder); la selezione curata è in [[Roblox Docs Motion References]].
- **VFX e luce**: `lighting-and-effects/` (atmosphere, beam, clouds, particelle, post-processing) → insieme a [[VFX and Audio Hub]].
- **UI**: `ui/` → insieme a [[UI and Icons Hub]].
- **Studio e modeling**: `studio/`, `modeling/`, `tutorials/` (il più grande), `resources/` (i progetti d'esempio di Roblox).

`roblox-docs/tutorials/interactive-ui/StarterGui-HUDContainer-...` aveva 3 file con percorsi molto lunghi: ripristinati dal blob git, verificati.
{related('[[Knowledge Hub]]', '[[roblox-ai Reference Library]]', '[[Roblox Docs Motion References]]', fw('ROUTER', 'Router fwjelaa'))}
''')

GR = f'{RAI}/game-refs'
gr_genres = [d for d in subdirs(GR) if d not in ('game-icons', 'game-thumbnails', 'curated-2026-11')]
note('05 UI and Icons/Game Refs (roblox-ai).md', ['ui', 'references', 'games', 'thumbnails', 'roblox-ai', 'type/resource'], f'''
# Game Refs (roblox-ai)

{tldr(f'{count(GR)} immagini di giochi Roblox in {GR}/: screenshot per genere, {count(GR + "/game-icons")} icone, {count(GR + "/game-thumbnails")} thumbnail',
      'Arte di giochi di terzi: solo riferimento (composizione, colori, leggibilità), mai da riusare',
      'anime-fighting copiato in 01 VFX and Audio/Reference Images/Anime Fighting Games (roblox-ai)',
      'Il resto resta nel repo: qui c\'è la mappa')}

## Generi (screenshot)
| Genere | Immagini |
|---|---|
{chr(10).join(f'| `{d}` | {count(GR + "/" + d)} |' for d in gr_genres)}

## Icone e thumbnail
- `game-icons/` ({count(GR + "/game-icons")}, in `batch-01..`): icone quadrate di giochi, per studiare come si legge un'icona a 150 px.
- `game-thumbnails/` ({count(GR + "/game-thumbnails")}): copertine 16:9.
- `../thumbnails/` e `../logos/`: le stesse per giochi famosi (Adopt Me, Blox Fruits, Doors, Rivals...), già in `05 UI and Icons/Branding`.

## Uso
Per un'icona o una thumbnail: scegli 3-5 esempi dello stesso genere, nota cosa hanno in comune (soggetto grande, contrasto, testo corto) e fai un'immagine tua. Per la combo: `anime-fighting/` mostra come i giochi del genere mettono in scena aure, colpi e HUD.
{related('[[UI and Icons Hub]]', '[[UI Style References]]', '[[VFX Reference Images]]', '[[roblox-ai Reference Library]]')}
''')

rai_log_section = f'''## Integrazione roblox-ai (2026-11-06)
Repo `github.com/izzyfrm/roblox-ai`, commit `{RAI_COMMIT[:7]}`: **intero** in `{RAI}/` ({len(rai_inv)} file), archivio `{RAI_ZIP}`. Dettagli in [[roblox-ai Reference Library]].

| Azione | File |
|---|---|
| repo intero (`project-dir`) | {len(rai_inv)} |
| copie nelle cartelle tematiche (`copy`) | {rlc['copy']} |
| copie non fatte perché già presenti (`skip-copy`) | {rlc['skip-copy']} |
| nome accorciato, percorso oltre 249 caratteri (`rename`) | {rlc['rename']} |

Righe aggiunte anche in coda a `_data/riorganizzazione-log.csv`; dettaglio in `_data/roblox-ai-log.csv`.'''

# ------------------------------------------------------------------ data notes
dl = os.path.join(V, '_data/riorganizzazione-log.csv')
logrows = list(csv.DictReader(open(dl, encoding='utf-8'))) if os.path.exists(dl) else []
lc = Counter(r['action'] for r in logrows)
plan = list(csv.DictReader(open(os.path.join(V, '_data/piano.csv'), encoding='utf-8')))
pc = Counter(r['action'] for r in plan)
removed = [r for r in plan if r['action'] == 'remove-dup']
dup_path = os.path.join(V, '_data/duplicati.csv')
dup_stats = open(os.path.join(V, '_data/duplicati-stats.txt'), encoding='utf-8').read() if os.path.exists(os.path.join(V, '_data/duplicati-stats.txt')) else ''
note('_data/riorganizzazione-log.md', ['index', 'log', 'type/reference'], f'''
# Riorganizzazione - Log

Riorganizzazione del 2026-11-06: dal vecchio ordine per pack (`docs/`, `vfx/`, `models/`, `ui/`, `animations/`, `tools/`, `knowledge/`) all'ordine per tema. **Mappatura completa per file**: `_data/riorganizzazione-log.csv` (vecchio → nuovo) e `_data/piano.csv` (una riga per ognuno dei 12.021 file della baseline, con azione e SHA1).

## Numeri
| Azione | File |
|---|---|
| spostati in cartelle tematiche (`move`) | {pc['move']} |
| nei progetti intatti (`project`, spostati con la loro cartella) | {pc['project']} |
| copie estratte da progetti intatti o da `anim/screens` (`copy`) | {pc['copy']} |
| copie non fatte perché già presenti (`skip-copy`) | {pc['skip-copy']} |
| duplicati rimossi (`remove-dup`) | {pc['remove-dup']} |

> [!note] File modificati dopo lo spostamento
> - Le 11 copie delle research (`02 Animation/Research`, `04 Maps and World/Research`) hanno in testa un blocco di provenienza (frontmatter `source:` + un riquadro): il loro SHA1 non corrisponde più a `piano.csv`. Gli originali intatti sono nei progetti in `07 Tools and Pipelines`.
> - Il vecchio `README.md` (scritto nel round precedente, descriveva l'ordine per pack) è stato sostituito da un rimando a [[00 Start Here]].
> - `_assets/thundercombo-banner.jpg` è un ritaglio largo di `09 ThunderCombo/Screenshots/v3/1_carica_kit.jpg`, non una copia.

{dup_stats}

{rai_log_section}

## Regole per cartella
| Vecchio | Nuovo |
|---|---|
| `docs/fwjelaa vfx method.md` | `01 VFX and Audio/Sources/fwjelaa VFX Method (prompt originale).md` |
| `docs/MASTER_PROMPT.md` | `05 UI and Icons/Sources/ForgeGUI UI Rebuild Brief (prompt originale).md` |
| `vfx/particle and model kit.rbxm` | `06 Studio Kits/VFX/PDS Particles and Models Kit.rbxm` |
| `models/Lift Rock Models (personaggi glb)/*` | `03 Models and Characters/Characters/*` (README → `README - Lift Rock Models.txt`) |
| `ui/UI Icon Pack/*` | `05 UI and Icons/Icons/*` (README → `README - UI Icon Pack.txt`) |
| `ui/roblox ui references/roblox-ui/references/{{previews,style-refs,ui-styles,visual-refs}}` | `05 UI and Icons/Style References/{{Previews,Style Refs,UI Styles,Visual Refs}}` |
| `ui/roblox ui references/roblox-ui/screenshots` | `05 UI and Icons/Screenshots/Stud Simulator` |
| `ui/roblox ui references/community-kits/lando-stud-ui-pack/*` | `06 Studio Kits/UI/Stud UI Pack (lando).rbxm` + `- SOURCE.txt` |
| resto di `ui/roblox ui references/` (kit, tools, textures, icons, docs, .superpowers) | `07 Tools and Pipelines/Roblox UI Kit (fwjelaa)/` |
| `animations/Roblox-Animations-by-fwjelaa` | `07 Tools and Pipelines/Roblox-Animations-by-fwjelaa` (intero) |
| `tools/Picture-to-Roblox-Model-by-fwjelaa` | `07 Tools and Pipelines/Picture-to-Roblox-Model-by-fwjelaa` (intero) |
| `tools/Roblox-Maps-by-fwjelaa` | `07 Tools and Pipelines/Roblox-Maps-by-fwjelaa` (intero) |
| `knowledge/fwjelaa-vault` | `08 Knowledge/fwjelaa-vault` (intero) |
| vecchio `README.md` | sostituito da un rimando a [[00 Start Here]] |

## Copie estratte (rinominate)
| Da | A |
|---|---|
| animation pack `research/01..05-*.md` | `02 Animation/Research/Anim Research 01..05 - ....md` |
| animation pack `fwjelaa animation method.md` | `02 Animation/Sources/fwjelaa Animation Method (originale).md` |
| animation pack `images/*` | `02 Animation/Previews/Animation Pack - *` |
| animation pack `ref/*` | `02 Animation/References/*` |
| animation pack `out/*.rbxmx` e fwjelaa `73 Kits and Models/Animations/*.rbxmx` | `06 Studio Kits/Animations/R6|R15/` (una copia per file) |
| MapKit `maps/*/shots/*`, `research/*.md` | `04 Maps and World/Map Shots/*`, `Research/Maps Research - *.md` |
| Picture-to-Model `images/*` | `03 Models and Characters/Picture-to-Model Previews/` |
| fwjelaa `80 Reference Library/{{vfx,cutscenes,sfx,animations,ui-icons,ui-screenshots,ui-styles,previews,style-refs,visual-refs,logos,thumbnails}}` | `01 VFX and Audio/...`, `02 Animation/References/Motion Refs`, `05 UI and Icons/...` |
| fwjelaa `18 Rigs and Skeletons`, `19 Concept Sheets`, `73 Kits and Models/Creatures` | `03 Models and Characters/Rigs`, `Concept Sheets`, `Creatures` |
| UI kit `roblox-ui/icons`, `textures` | `05 UI and Icons/Icons/12 Kit Icons (roblox-ui)`, `Textures` |
| `Desktop/nicco/anim/screens/**` | `09 ThunderCombo/Screenshots/v1|v2|v3` |

## Duplicati rimossi ({len(removed)})
Tutti asset (immagini, modelli, kit): README, LICENSE, manifest e file senza estensione non vengono mai deduplicati. Per ognuno resta una copia identica nella cartella tematica (e l'archivio originale in `_originali/`).
| Rimosso (vecchio percorso) | Identico a |
|---|---|
{chr(10).join(f"| `{r['src']}` | `{r['note'].replace('identical to ', '')}` |" for r in removed)}
''')

# ------------------------------------------------------------------ root README pointer
NOTES['README.md'] = '''# niceforwh vault

Questo vault si apre in Obsidian. Inizia da **[[00 Start Here]]** oppure dalla home visiva **[[000 Home]]**.

- Mappa delle cartelle e percorsi di lettura: [[00 Start Here]]
- "Cerco X": [[ROUTER]]
- Ogni spostamento della riorganizzazione del 2026-11-06: [[riorganizzazione-log|Riorganizzazione - Log]]
'''

# ------------------------------------------------------------------ write notes
for rel, text in NOTES.items():
    p = os.path.join(V, rel)
    os.makedirs(os.path.dirname(p) or V, exist_ok=True)
    open(p, 'w', encoding='utf-8').write(text)
print(len(NOTES), 'notes written')

# ------------------------------------------------------------------ canvas
def node(i, f, x, y, w=300, h=160, color=None):
    d = {'id': i, 'type': 'file', 'file': f, 'x': x, 'y': y, 'width': w, 'height': h}
    if color:
        d['color'] = color
    return d
nodes = [
    {'id': 'g1', 'type': 'group', 'label': 'Motion & FX', 'x': -760, 'y': -40, 'width': 680, 'height': 600, 'color': '5'},
    {'id': 'g2', 'type': 'group', 'label': 'World, UI & Kits', 'x': 120, 'y': -40, 'width': 680, 'height': 600, 'color': '4'},
    {'id': 'g3', 'type': 'group', 'label': 'Project & Knowledge', 'x': -320, 'y': 620, 'width': 1020, 'height': 420, 'color': '6'},
    node('home', '000 Home.md', -160, -360, 340, 200, '1'),
    node('start', '00 Start Here.md', 260, -360, 300, 160),
    node('router', 'ROUTER.md', -560, -360, 300, 160),
    node('vfx', '01 VFX and Audio/VFX and Audio Hub.md', -740, 0, 300, 160, '5'),
    node('em', '01 VFX and Audio/Kit Emitters - Reference Sheet.md', -400, 0, 300, 160),
    node('me', '01 VFX and Audio/Kit Meshes - Reference Sheet.md', -400, 200, 300, 160),
    node('anim', '02 Animation/Animation Hub.md', -740, 200, 300, 160, '5'),
    node('tim', '02 Animation/Combat Timing Cheat Sheet.md', -740, 380, 300, 160),
    node('ifr', '01 VFX and Audio/Impact Frames Hitstop and Camera.md', -400, 380, 300, 160),
    node('mod', '03 Models and Characters/Models and Characters Hub.md', 140, 0, 300, 160, '4'),
    node('maps', '04 Maps and World/Maps and World Hub.md', 480, 0, 300, 160, '4'),
    node('ui', '05 UI and Icons/UI and Icons Hub.md', 140, 200, 300, 160, '4'),
    node('kits', '06 Studio Kits/Studio Kits Hub.md', 480, 200, 300, 160, '4'),
    node('tools', '07 Tools and Pipelines/Tools and Pipelines Hub.md', 140, 380, 300, 160),
    node('safe', 'Skill - Safe Asset Intake.md', 480, 380, 300, 160, '2'),
    node('tc', '09 ThunderCombo/ThunderCombo Hub.md', -300, 660, 300, 160, '6'),
    node('skill', 'Skill - Roblox VFX Combo.md', 40, 660, 300, 160, '2'),
    node('know', '08 Knowledge/Knowledge Hub.md', -300, 850, 300, 160, '6'),
    node('log', '_data/riorganizzazione-log.md', 40, 850, 300, 160),
    node('rai', '08 Knowledge/roblox-ai Reference Library.md', 380, 850, 300, 160, '6'),
    node('sfx', '01 VFX and Audio/CC0 SFX Library (roblox-ai).md', 380, 660, 300, 160),
]
edges = [('home', 'start'), ('home', 'router'), ('home', 'vfx'), ('home', 'mod'), ('vfx', 'em'), ('vfx', 'me'), ('vfx', 'ifr'),
         ('anim', 'tim'), ('tim', 'ifr'), ('mod', 'maps'), ('ui', 'kits'), ('kits', 'safe'), ('tools', 'safe'), ('skill', 'em'),
         ('skill', 'tim'), ('skill', 'tc'), ('tc', 'know'), ('know', 'tools'), ('log', 'safe'), ('know', 'rai'), ('rai', 'sfx'), ('vfx', 'sfx'), ('rai', 'safe')]
canvas = {'nodes': nodes, 'edges': [{'id': f'e{i}', 'fromNode': a, 'fromSide': 'bottom', 'toNode': b, 'toSide': 'top'} for i, (a, b) in enumerate(edges)]}
json.dump(canvas, open(os.path.join(V, '000 Studio Map.canvas'), 'w', encoding='utf-8'), indent=1)

# ------------------------------------------------------------------ .obsidian (theme + own config; no plugins)
ob = os.path.join(V, '.obsidian')
os.makedirs(os.path.join(ob, 'themes'), exist_ok=True)
src_theme = os.path.join(V, FWR, ".obsidian/themes/fwjelaa's Infinite Void")
dst_theme = os.path.join(ob, "themes/fwjelaa's Infinite Void")
os.makedirs(dst_theme, exist_ok=True)
for f in ('theme.css', 'manifest.json'):
    shutil.copy2(os.path.join(src_theme, f), os.path.join(dst_theme, f))
json.dump({'enabledCssSnippets': [], 'theme': 'obsidian', 'cssTheme': "fwjelaa's Infinite Void", 'accentColor': '#B7B4DA'},
          open(os.path.join(ob, 'appearance.json'), 'w'), indent=2)
json.dump({'userIgnoreFilters': ['_originali/'], 'showUnsupportedFiles': False, 'showInlineTitle': False,
           'propertiesInDocument': 'hidden', 'newLinkFormat': 'absolute'}, open(os.path.join(ob, 'app.json'), 'w'), indent=2)
json.dump([], open(os.path.join(ob, 'community-plugins.json'), 'w'))
json.dump({k: True for k in ('file-explorer', 'global-search', 'switcher', 'graph', 'backlink', 'outgoing-link', 'tag-pane',
                             'page-preview', 'command-palette', 'outline', 'canvas', 'properties', 'bookmarks', 'bases')},
          open(os.path.join(ob, 'core-plugins.json'), 'w'), indent=2)
json.dump({'items': [{'type': 'file', 'path': '000 Home.md'}, {'type': 'file', 'path': '00 Start Here.md'},
                     {'type': 'file', 'path': 'ROUTER.md'}, {'type': 'file', 'path': 'Skill - Roblox VFX Combo.md'},
                     {'type': 'file', 'path': '000 Studio Map.canvas'}]}, open(os.path.join(ob, 'bookmarks.json'), 'w'), indent=2)
json.dump({'search': '-path:"08 Knowledge/fwjelaa-vault" -path:_originali', 'colorGroups': [
    {'query': 'path:"01 VFX"', 'color': {'a': 1, 'rgb': 5301503}}, {'query': 'path:"02 Animation"', 'color': {'a': 1, 'rgb': 9848575}},
    {'query': 'path:"09 ThunderCombo"', 'color': {'a': 1, 'rgb': 16766720}}, {'query': 'tag:#type/hub', 'color': {'a': 1, 'rgb': 16777215}}]},
    open(os.path.join(ob, 'graph.json'), 'w'), indent=2)
print('canvas + .obsidian written')
