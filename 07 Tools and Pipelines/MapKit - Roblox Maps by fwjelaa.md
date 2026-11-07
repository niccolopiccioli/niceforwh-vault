---
tags: [tools, maps, mapkit, type/resource]
---
# MapKit - Roblox Maps by fwjelaa

<!-- tldr:start -->
> [!tldr] TL;DR
> - Progetto intatto: 07 Tools and Pipelines/Roblox-Maps-by-fwjelaa
> - Descrivi una mappa ("a lift a boulder simulator map") e Claude la costruisce nel place aperto, poi la verifica con screenshot, walk test e budget
> - Mappe d'esempio: lift-a-boulder, backrooms-level-0, farmhouse-night, forest-lake
> - Richiede Python 3 + pillow/numpy, Studio come MCP server, per le mappe realistiche Blender e una chiave Open Cloud
<!-- tldr:end -->


## Come si usa (dal README, non eseguito qui)
1. Place nuovo (Baseplate), Studio come MCP server.
2. Apri la cartella in Claude Code, `/make-map` + idea. Studio deve restare visibile (servono gli screenshot).
3. Il kit non cancella niente: Baseplate e SpawnLocation finiscono in `ServerStorage.MapKit_Removed`.

## Cosa c'è
`kit/studio/MapKit` (Luau), `kit/blender` (Python), `maps/` (le 4 mappe con `shots/`), `research/` (6 note), `styles/`, `prompts/`, `GUIDE.html`.

## Sicurezza
Contiene `.py`, `CLAUDE.md`, `.claude/skills/make-map`: niente eseguito. Le texture e i modelli realistici usano asset CC0 (ambientCG, Poly Haven) da caricare sul proprio account; la chiave API va tenuta fuori dalle chat.

<!-- related:start -->
## Related
[[Maps and World Hub]] · [[MapKit Example Maps]] · [[Tools and Pipelines Hub]] · [[08 Knowledge/fwjelaa-vault/fwjelaa vault/70 fwjelaa Packs/make-map|make-map (fwjelaa)]]
<!-- related:end -->
