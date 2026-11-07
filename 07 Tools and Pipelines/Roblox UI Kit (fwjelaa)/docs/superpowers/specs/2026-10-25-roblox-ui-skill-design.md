# Roblox UI Skill — Design Spec

Date: 2026-10-25
Status: Draft for review

## 1. Goal

A Claude Code skill that makes Claude produce polished, style-consistent Roblox UI through the Roblox Studio MCP, in six named styles, for any game. It must be good enough to show on the user's YouTube channel and usable by viewers who have Claude Code + the Studio MCP but none of the user's private assets.

Success means:

- Given a prompt like "add a Stud Simulator shop and HUD to my game", Claude builds working, themed UI in Studio, screenshots it, and fixes what the screenshot shows before calling it done.
- Each of the six styles is recognisable at a glance and proven by real builds in the `UI/UX` place (placeId 82819238997132).
- Everything works with zero asset uploads. Uploaded textures are an optional polish step.
- Phone-size screens are usable: touch targets ≥ 44 px, nothing under the Roblox top bar or notches, text never overflows.

Out of scope: game logic (data stores, purchases, combat). The kit fires events and exposes setters; games wire their own data.

## 2. What was learned from the references

### Lift a Rock for Cuh (style 1 source, inspected in Studio)

- Font: FredokaOne for everything. Text white with a thick dark `UIStroke` (`#14101F`, 2.5–4.5 px, Contextual).
- Frames: dark navy base, 9-slice "skin" images, gold border `#E8B818` 5 px, corner radius ≈ 0.045 scale on panels, 10–14 px on rows.
- Buttons: 3-stop vertical `UIGradient` (rotation 90): purple `#D58CFF→#9B3BFF→#6A12D6`, green `#9CFF3A→#33CC14`, red `#FF5A78→#D6123A`. Two strokes: border stroke + contextual text stroke in a darker shade of the button hue.
- Texture: tiled stud image at 45–82 % transparency on every surface (tile 35–54 px) plus a diagonal "streaks" gloss overlay.
- Layout: title tab overhangs the panel's top-left (`Position.Y = -0.1`) with an oversized icon breaking the frame; the close button overhangs the top-right corner (anchor 0.5,0.5 at 0.985,0.015).
- Motion and UX (from `PanelController` and `Ui` modules): panel open = `UIScale` 0.85 → 1, Back/Out, 0.2 s; button press = `UIScale` 0.9 → 1, Back/Out, 0.15 s; world `BlurEffect` size 14 tweened in 0.2 s while any panel is open; one panel open at a time; HUD clutter hidden while a panel is open; lists are `Template` (hidden) + clones.
- Gotcha found in its code: a `UIGridLayout` with Scale cell sizes inside an `AutomaticCanvasSize` `ScrollingFrame` never settles and stops scrolling part-way. Fix: convert cells to pixel sizes from the window's `AbsoluteSize` and re-apply on resize.

### Combat references (web research, gameplay screenshots)

- The Strongest Battlegrounds / Jujutsu Shenanigans: flat. Four numbered gray translucent move tiles bottom-centre with name text, one bright bar above them, a slanted red italic "ultimate" banner, round translucent mobile buttons on the right.
- Type Soul: sleek dark. Split health/energy bar (purple left, cyan right) with segment ticks and a diamond emblem at the seam, thin secondary bar under it, 12 dark slots. Menus are near-black with chamfered top corners, colour-coded column headers, bold sans text.
- Ghoul://Re: gothic. Crimson health bar, amber sub-bar, thin ornate frames, small serif type, muted palette.

### Studio capabilities confirmed (Studio 0.744)

`UIShadow` (BlurRadius, Offset, Spread, Inset, Color), `UIBlur` (Strength, Color, Transparency), `Path2D` (stroke only), `StyleSheet`/`StyleRule`, `UIFlexItem`, `UIDragDetector`, `CanvasGroup`, `UIStroke.BorderStrokePosition` / `BorderOffset`, `ScreenGui.ScreenInsets`. Fonts include FredokaOne, LuckiestGuy, Bangers, PermanentMarker, Michroma, Sarpanch, Oswald, GrenzeGotisch, Fondamento, Merriweather, BuilderSans family, RobotoMono, SpecialElite, Creepster.

Whether `UIShadow` and `UIBlur` render in edit-time screenshots and on live clients is unverified — the first build step is a spike to check (see §7).

## 3. The six styles

Each style is a theme module: a token table plus "signature" decorator functions that add the details that make it recognisable.

| Style | Source | Palette | Type | Signature details | Motion |
|---|---|---|---|---|---|
| Stud Simulator | Lift a Rock | Navy base, gold rim, candy gradients | FredokaOne, thick dark text stroke | Stud tile, gloss streaks, overhanging title tab + close, 3-stop gradients | Bouncy: Back/Out pops, squash on press, count-up numbers |
| Battlegrounds | TSB, JJS, Type Soul | Charcoal translucent, white text, one hot accent per game (red default, cyan alternate) | BuilderSans Bold / Gotham; italic accents | Numbered move tiles, split segmented bar with emblem, slanted ultimate banner, round mobile buttons | Snappy: Quad/Out 0.08–0.12 s, cooldown sweeps, hit flashes |
| Kinetic Comic | Persona-style | Red, black, white only | Bangers / LuckiestGuy, rotated words | Slanted parallelogram panels, offset hard shadows, jagged burst behind headers, mixed-case "ransom" labels | Slam-in: overshoot + slight rotation, screen-shake on confirm |
| Cyber Holo | Sci-fi HUDs | Near-black, cyan + magenta neon | Michroma / Sarpanch, RobotoMono numbers | Corner brackets, scanlines, chamfered frames, glow strokes, tick-mark rulers | Flicker-in, typewriter text, glitch offset on errors |
| Manga Ink | Manga pages | Paper white, ink black, one spot colour | PermanentMarker / Bangers, speech bubbles | Thick ink borders with rough offset double line, screentone dots, speed lines, bubble tails | Panel "stamp" (scale 1.15 → 1, no easing), speed-line wipe |
| Dark Fantasy | Ghoul://Re, Deepwoken | Black, crimson, antique gold, parchment | GrenzeGotisch / Fondamento titles, Merriweather body | Thin double frames, ornate corner pieces, parchment panels, diamond dividers | Slow: Sine 0.3–0.45 s fades, ember drift |

## 4. Architecture

```
roblox ui skill/                      (this workspace, the distributable)
  README.md                           for viewers: install, example prompts, screenshots
  roblox-ui/                          the skill (copied to ~/.claude/skills/roblox-ui)
    SKILL.md                          ≤ 120 lines: when to use, workflow, style picker, gotchas
    workflow.md                       MCP build → bake → screenshot → critique loop, device checks
    ux-rules.md                       screen zones, safe areas, touch sizes, hierarchy, motion timing
    components.md                     kit API reference
    styles/<style>.md                 tokens, signature moves, do/don't, proof screenshots (×6)
    assets.md                         optional texture pack: generate, upload, swap IDs into a theme
    kit/
      UIKit.luau                      component builders
      Motion.luau                     runtime behaviour
      Themes/<Style>.luau             6 theme modules
      Showcase.luau                   builds the demo place screens
      KitCheck.luau                   structural self-test
      install.luau                    creates the ModuleScripts in a game from these sources
    screenshots/                      proof images (style × screen)
  docs/superpowers/specs/             this spec
```

### Kit (`UIKit`)

Pure builder functions: `UIKit.<Component>(theme, props) -> GuiObject`. No yields, no services beyond creating instances, so they run both at edit time (through MCP `execute_luau`) and at runtime.

Components:

- Containers: `Screen` (ScreenGui with insets + IgnoreGuiInset rules), `Panel` (title tab, close, body), `Card`, `Grid` (pixel-cell fix built in), `List`, `Tabs`.
- Controls: `Button` (primary / secondary / danger / ghost), `IconButton`, `Toggle`, `Slider`, `TextInput`.
- Readouts: `Bar` (single, split, segmented), `Currency`, `Badge`, `Slot` (hotbar / move tile / inventory cell), `Hotbar`, `Tooltip`.
- Feedback: `Toast`, `Popup` (reward / confirm), `Splash` (level-up), `DamageNumber`.
- Screens: `LoadingScreen`, `MainMenu`.

Contract naming carries over from Lift a Rock so runtime code can find things: panels are `ScreenGui > Main` with `Close`, `List`/`Grid`, and a hidden `Template`; button captions live in a child `Label`. Every built element gets a CollectionService tag (`UIKit.Button`, `UIKit.Panel`, …) and a `UIKitTheme` attribute so `Motion` knows how to animate it.

### Themes

```lua
-- Themes/StudSimulator.luau (shape, not final values)
return {
  name = "StudSimulator",
  color = { base = …, surface = …, rim = …, text = …, textStroke = …, primary = {…3 stops}, success = {…}, danger = {…}, accent = {…} },
  font = { display = Font.new(…FredokaOne…), body = …, number = … },
  stroke = { frame = 5, button = 4, text = 3 },
  radius = { panel = UDim.new(0.045, 0), button = UDim.new(0.3, 0), slot = UDim.new(0, 10) },
  motion = { open = TweenInfo…, press = TweenInfo…, pressScale = 0.9, openFrom = 0.85, blur = 14 },
  assets = { studTile = nil, streaks = nil, skin = nil }, -- optional, filled by the texture pack
  decorate = { panel = function(frame, props) … end, button = …, slot = …, bar = …, header = … },
}
```

Rules: components never hard-code colours, fonts or sizes; all of it comes from the theme. A theme missing a token is a bug that `KitCheck` catches. Decorators add children (stud tile, brackets, screentone, corner ornaments) and must work when `assets` is empty.

### Runtime (`Motion`)

A ModuleScript plus a short LocalScript `UIRuntime` that starts it. Responsibilities: press squash/hover on tagged buttons, one-panel-at-a-time open/close with blur and HUD hiding, toast queue, count-up numbers, damage-number pops, cooldown sweeps, loading-screen progress. Motion reads the theme's `motion` profile so the same call feels bouncy in Stud Simulator and snappy in Battlegrounds.

### Edit-time baking

Claude installs the kit (ModuleScripts under `ReplicatedStorage.UIKit`), then runs a build script through `execute_luau` that requires the kit and parents finished ScreenGuis into `StarterGui`. Result: real instances the user can inspect and hand-edit. Re-running a build replaces only the ScreenGuis it made (identified by a `UIKitBuilt` attribute), never hand-made UI.

## 5. Showcase place (`UI/UX`, placeId 82819238997132)

- One ScreenGui per style × screen set: 6 styles × {HUD, Menus, Loading + Main Menu, Feedback} = 24 screens.
- A `Showcase` switcher (style tabs + screen tabs) that works in Play mode for video B-roll, with feedback screens replaying their animations.
- A plain backdrop scene so screenshots read well (a neutral sky/terrain behind the UI; each style may set its own backdrop colour).
- Only the showcase place is modified. The Lift a Rock place stays read-only.

## 6. Assets (hybrid)

- Default: zero uploads. Stud look uses a procedural fallback (or Roblox built-in `rbxasset://` textures if the spike shows they render in game).
- Optional: `assets.md` walks through generating textures (MCP `generate_texture` or local image generation) and uploading them (MCP `upload_image`, or Open Cloud), then filling a theme's `assets` table. The kit must look complete with or without them.

## 7. Verification

1. Spike before the kit: does `UIShadow` render in edit-time `screen_capture` and in Play? Does `UIBlur`? Do `rbxasset://` textures render in a `ScreenGui`? Can ModuleScripts be created with source via MCP and re-required without a stale cache?
2. `KitCheck.luau`: builds every component in every theme, asserts required children/contract names exist, asserts no theme token is nil, reports failures by name. Runs after every kit change.
3. Screenshot review per style × screen against that style's do/don't list in `styles/<style>.md`.
4. Mobile pass with the Studio device simulator (phone landscape): touch targets ≥ 44 px, safe insets respected, no text overflow or clipped strokes.
5. A cold-start test: in a fresh baseplate, follow only `SKILL.md` + `README.md` to install the kit and build one style, to prove a viewer can do it.

## 8. Risks

- `UIShadow` / `UIBlur` may be beta-only or not render on all clients. Mitigation: decorators feature-detect and fall back to layered frames / `BlurEffect`.
- Six styles × many components is a lot of surface. Mitigation: build Stud Simulator end to end first, review it with the user, then the rest reuse the same components with new themes.
- Edit-time `require` caches modules. Mitigation: the build script clones the kit modules before requiring, so edits are always picked up.
- Long `execute_luau` calls can freeze Studio. Mitigation: build one screen per call and `task.wait()` between large batches.

## 9. Amendment (2026-10-26): premade catalog

The user wants every style to ship fully built, so viewers get every button, panel and screen ready-made in all six
styles. Their choices: **models + code**, **all four piece groups**, **animated + wired**, **a matching icon set per style**.

### The catalog: 35 pieces, same names in every style

`kit/Catalog.luau` turns builders into finished pieces with real copy, icons, sizes and variants. One line builds one:
`UIKit.piece("StudSimulator", "OfferBanner", { Title = "AUTO LIFT", Price = 30 })`. Every style has the same piece
names, so switching style means changing one string.

| Group | Pieces |
|---|---|
| Buttons (12) | PrimaryButton, SecondaryButton, SuccessButton, DangerButton, GhostButton, CloseButton, IconTile (caption + badge), RoundButton, Toggle, Tabs, Slider, TextBox |
| Shop + offers (6) | OfferBanner (icon over the top edge, "ONLY ⓪ 30"), OfferTile (the "+10B" tile), ItemCard, PriceTag, GamepassCard, ShopPanel |
| HUD readouts (8) | Currency, HealthBar, XPBar, LevelBar, Hotbar, Slot, Timer, StatLine |
| Popups + screens (9) | Toast, RewardPopup, ConfirmDialog, DailyRewards, CodesBox, Settings, Inventory, LoadingScreen, MainMenu |

That's 35 pieces × 6 styles = 210 premade pieces. The five showcase screens (§5) stay; they're built from these pieces.

### Model packs (drag in, no code)

`roblox-ui/packs/<Style>.rbxm`, one per style, contains:

- the `UIKit_<Style>` ScreenGui with every piece, sorted into Buttons / Shop / HUD / Popups folders and laid out as a
  catalog board;
- the runtime (`UIKit` modules, `UIRuntime`) and server templates.

Drop the pack into a game and it works. Packs are exported from the showcase place with
`SerializationService:SerializeInstancesAsync`, then posted to a local receiver (`tools/pack_receiver.py`) that writes
the file. A spike on 2026-10-26 showed serialize → `<roblox!` binary → deserialize round-trips.

### Wiring (the `Motion` runtime; data lives in attributes, so it's editable in Properties)

- Every piece animates: hover/press, panel open/close, tabs, toggles, sliders, toasts, count-ups.
- `Opens = "<PanelName>"` on any button opens that panel; `CloseButton` closes its own.
- Robux pieces (OfferBanner, OfferTile, PriceTag, GamepassCard) carry `ProductId` or `GamePassId`. A click calls
  `PromptProductPurchase` / `PromptGamePassPurchase`. An id of 0 is demo mode: it logs and shows a toast instead of
  prompting.
- Server templates: `UIKitPurchases` (a `ProcessReceipt` stub with a `grant(player, productId)` hook) and
  `UIKitCodes` (a RemoteFunction that `CodesBox` calls, checked against a codes table).

### A matching icon set per style

Every style gets the same 30 core icon names in its own look:

> coin, gem, cash, star, heart, bolt, shield, sword, skull, trophy, crown, gift, shop, backpack, gear, lock, unlock,
> key, potion, egg, rebirth, clover, dumbbell, scroll, book, clock, friends, ticket, codes, upgrade

`Icons.get(name, style)` picks the style's set, then falls back to emoji.

| Style | Icon look (all rendered by `tools/render_icons_blender.py`, original art) |
|---|---|
| StudSimulator | Current cel set (third-party pack + 14 kit icons) |
| Battlegrounds | Flat white silhouettes, a red accent, thin dark rim |
| KineticComic | Bold cel with halftone shading; red, black and white only; thick black ink |
| CyberHolo | Emissive cyan/magenta wire glow on transparent |
| MangaInk | Black ink with screentone shading and one spot colour |
| DarkFantasy | Muted metal and bone, dark painted shading, gold rim light |

That's about 150 new renders and uploads.

### Verification additions

- KitCheck builds all 35 pieces in all 6 themes, checks contract names, and checks that wired pieces carry their
  attributes.
- Pack check: insert each `.rbxm` into a fresh baseplate, press Play, and click one piece of each kind. Purchases run
  in demo mode.
- Screenshots per style: the catalog board plus the five screens.

### Order

Stud Simulator first: HUD fixes, catalog board, wiring, pack export. Then a user review. After that, each other
style gets its theme, icon set, catalog board, screens and pack.
