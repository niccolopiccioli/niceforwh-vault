# References

1,142 GUI and icon images (about 158 MB), copied from the
[izzyfrm/roblox-ai](https://github.com/izzyfrm/roblox-ai) visual library. Every subfolder keeps the
source repo's own README.

**Before building a screen, open 2–3 images from the rows for your style and screen. After building,
put your screenshot next to them.** Match layout, sizes, stroke weight and palette. Don't copy artwork.

## By style

| Kit theme | Look at first | Then |
|---|---|---|
| **StudSimulator** | `visual-refs/studs-ui/Stud-GUI-1.png`, `Stud-GUI-2.png`, `Stud-Buttons.png`, `style-refs/studs/` (palette + 8 screen mockups) | `visual-refs/studs-ui/simulator-games/`, `visual-refs/studs-ui/original/`, `style-refs/simulator/`, `style-refs/candy/`, `ui-styles/08-stud-wood-metal`, `09-modern-cartoon-simulator`, `10-chunky-candy-buttons`, `11-glossy-bubble`, `13-pet-collector-grid`, `previews/roblox-user-interface/` |
| **Battlegrounds** | `ui-styles/66-fighting-game`, `ui-styles/90-anime-fighter-menu`, `previews/fighting-user-interface/` | `ui-styles/108-damage-numbers`, `ui-styles/43-dark-mode-pro`, `style-refs/anime/`, `style-refs/dark-pro/`, `previews/shooter-user-interface/` |
| **KineticComic** | `previews/hand-drawn-user-interface/`, `style-refs/cartoon/` | `previews/paper-user-interface/`, `previews/animation-user-interface/`, `ui-styles/85-cosmic-cartoon-space`, `previews/casual-user-interface/` |
| **CyberHolo** | `ui-styles/31-neon-cyberpunk`, `ui-styles/32-holographic-hud`, `previews/cyberpunk-user-interface/` | `ui-styles/41-glassmorphism`, `ui-styles/40-futuristic-racing`, `style-refs/cyberpunk/`, `style-refs/sci-fi/`, `style-refs/glass/`, `previews/neon-user-interface/`, `previews/space-user-interface/` |
| **MangaInk** | `ui-styles/90-anime-fighter-menu`, `previews/hand-drawn-user-interface/` | `style-refs/anime/`, `previews/paper-user-interface/`, `previews/minimal-user-interface/` |
| **DarkFantasy** | `ui-styles/52-gothic-horror`, `ui-styles/23-parchment-scroll`, `previews/gothic-user-interface/` | `ui-styles/22-modern-medieval`, `ui-styles/73-steampunk-brass`, `style-refs/horror/`, `style-refs/medieval/`, `style-refs/fantasy/`, `previews/dark-user-interface/`, `previews/medieval-user-interface/`, `previews/fantasy-user-interface/` |

## By screen

| Screen | Where |
|---|---|
| HUD | `style-refs/studs/mockup-hud.png`, `ui-styles/55-minimal-survival-hud`, `ui-styles/68-racing-dashboard`, `visual-refs/studs-ui/Stud-GUI-2.png` |
| Menus (shop, inventory, settings, codes) | `style-refs/studs/mockup-shop.png`, `mockup-inventory.png`, `mockup-settings.png`, `ui-styles/103-settings-menu`, `ui-styles/111-codes-redeem-box`, `ui-styles/13-pet-collector-grid` |
| Loading | `style-refs/studs/mockup-loading.png`, `visual-refs/sports/Loading-Screen.png` |
| Main menu | `visual-refs/sports/Main-Menu.png`, `Football-Main-Menu.png`, `ui-styles/90-anime-fighter-menu` |
| Feedback (toasts, rewards, damage) | `style-refs/studs/mockup-reward.png`, `visual-refs/studs-ui/Stud-DailyRewards.png`, `ui-styles/108-damage-numbers` |
| Buttons on their own | `previews/buttons-user-interface/`, `ui-styles/10-chunky-candy-buttons`, `visual-refs/studs-ui/Stud-Buttons.png` |
| Icons | `visual-refs/icons/` (the 256 px outline pack), `previews/icons-user-interface/` |

## Icons

`kit/Icons.luau` already points at uploaded copies of the `visual-refs/icons/` pack (`PACK`). It also
has 14 gap icons rendered in the same cel style by `tools/render_icons_blender.py` (`KIT`).
`Icons.get(name)` returns the art, or an emoji if there's no art. New icons should match the pack:
a thick navy outline, flat toon shading, and a 3/4 view.

## Licence

These are references, not assets. The pack icons, game screenshots and mockups belong to their
creators. The source repo says only `style-refs/` contact sheets are CC0 (Kenney). Look, don't ship:
build your own version, and check the creator's licence before putting any of these images in a game.
