# Roblox UI Skill Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Ship a `roblox-ui` Claude skill: a themed Luau UIKit with six styles, proven by 30 built screens in the user's `UI/UX` Studio place, plus the docs that teach Claude to use it.

**Architecture:** Kit source lives as `.luau` files in this workspace and is installed into a game as ModuleScripts with the Studio MCP `multi_edit` tool. Builders (`UIKit.*`) are pure functions `(theme, props) -> Instance` that run at edit time through `execute_luau` and bake real ScreenGuis into `StarterGui`. A runtime module (`UIKit.Motion`) gives baked UI behaviour by tag and contract name. Six theme modules hold all colours, fonts, sizes, motion and decorator functions.

**Tech Stack:** Luau (`--!strict`), Roblox Studio 0.744 through the Roblox Studio MCP (`execute_luau`, `multi_edit`, `screen_capture`, `start_stop_play`, `upload_image`), Markdown for the skill docs, optional Python + Pillow for the texture pack.

**Spec:** `docs/superpowers/specs/2026-10-25-roblox-ui-skill-design.md`

## Global Constraints

- Build only in Studio id for name `UI/UX (placeId: 82819238997132)`. The `+1 Lift a Rock for CUH` place (placeId 79409359952462) is read-only reference. Look up studio ids with `list_roblox_studios` at the start of every session; they change.
- Zero uploads by default: every theme must look finished with `theme.assets = {}`. Uploaded textures are only added in Task 16.
- Components never hard-code colours, fonts or sizes. Everything comes from the theme. A missing token is a KitCheck failure.
- Contract names (from Lift a Rock): panels are `ScreenGui > Main` with `TitleTab`, `Close`, and `List` or `Grid` or `Body`; lists hold a hidden `Template`; button captions live in a child TextLabel named `Label`; bars hold `Fill` (split bars: `Left.Fill` and `Right.Fill`).
- Every kit-made instance that needs behaviour carries a tag `UIKit.<Kind>` and the attribute `UIKitTheme`. Every kit-made ScreenGui has `UIKitBuilt = true`.
- Every kit-made `UIStroke` stores its design thickness in the attribute `BaseThickness` (designed for a 600-px-tall screen).
- Touch targets ≥ 44 px on a phone-landscape screen; HUD ScreenGuis use `ScreenInsets.CoreUISafeInsets`; full-screen ScreenGuis use `IgnoreGuiInset = true` and `ScreenInsets.None`.
- `execute_luau` calls must not freeze Studio: build one screen per call and `task.wait()` between big batches.
- Edit-time requires go through a clone of `ReplicatedStorage.UIKit` so module edits are always picked up (see Task 2's runner snippet).
- Skill docs follow `~/.claude/rules/core/SKILL_AUTHORING.md`: frontmatter with "Use when", `allowed_tools`, SKILL.md ≤ 120 lines, `## Gotchas` with ≥ 3 items.
- The workspace is not a git repo. "Commit" steps run only if the user approved `git init` at plan review; otherwise skip them.

## Review Focus

1. **Phone-sized screens.** A viewer opens the place on a phone: buttons must stay ≥ 44 px, nothing under the top bar, strokes not comically thick. Pinned by Task 15's device pass and KitCheck's `BaseThickness` case (Task 2).
2. **Big and edge-case numbers.** Currency readouts get values like 999.6, 999 999, negative refunds and 0. Expected: `1K`, `1M`, `-2.5K`, `0`, never `1000K`. Pinned by KitCheck's `abbreviate` case (Task 2), implemented in Task 3.
3. **Long inventories scroll to the end.** A grid with 60 items must scroll to the last row (the Lift a Rock bug). Pinned by Task 7's scroll test.
4. **Re-running a build.** Running a showcase or game build twice must replace only the ScreenGuis it made, never hand-made UI, and leave no duplicates. Pinned by Task 8's rebuild test.
5. **Long text.** Titles like "Legendary Golden Dumbbell of Power" must shrink to fit, not overflow. Pinned by KitCheck's long-title case (Task 2): every kit TextLabel has `TextScaled` and a `UITextSizeConstraint`.

## File Structure

```
roblox ui skill/
  README.md                          Task 18  viewer-facing install + prompts
  docs/superpowers/specs/…           (exists)
  docs/superpowers/plans/…           (this file)
  roblox-ui/                          the skill folder, copied to ~/.claude/skills/roblox-ui in Task 18
    SKILL.md                         Task 17
    workflow.md                      Task 17  install, build, screenshot, critique loop
    ux-rules.md                      Task 17  zones, safe areas, touch, hierarchy, motion timing
    components.md                    Task 17  API reference for every builder
    assets.md                        Task 16  optional texture pack
    styles/<style>.md  ×6            Task 17  tokens, signature moves, do/don't, screenshot list
    screenshots/                     Tasks 8–15
    kit/
      UIKit.luau                     Task 3   entry: re-exports builders, theme lookup
      Util.luau                      Task 3   make, colours, text, icon, strokes, pixelGrid, abbreviate
      Decor.luau                     Task 3   signature details (studs, gloss, chamfer, slant, …)
      Controls.luau                  Task 4   Button, IconButton, Toggle, Slider, TextInput, setVariant
      Containers.luau                Task 4   Screen, Panel, List, Grid, Tabs, Card
      Readouts.luau                  Task 5   Bar, Currency, Badge, Slot, Hotbar, Tooltip
      Feedback.luau                  Task 6   ToastStack, Toast, Popup, Splash, DamageNumber
      Screens.luau                   Task 6   LoadingScreen, MainMenu
      Motion.luau                    Task 7   runtime behaviour
      UIRuntime.client.luau          Task 7   LocalScript that starts Motion
      Themes/StudSimulator.luau      Task 4
      Themes/Battlegrounds.luau      Task 9
      Themes/KineticComic.luau       Task 10
      Themes/CyberHolo.luau          Task 11
      Themes/MangaInk.luau           Task 12
      Themes/DarkFantasy.luau        Task 13
      dev/KitCheck.luau              Task 2   structural self-test (edit mode)
      dev/MotionCheck.luau           Task 7   runtime self-test (play mode, client)
      dev/Showcase.luau              Task 8   builds the 30 demo screens
      dev/ShowcaseRuntime.client.luau Task 14 play-mode style/screen switcher
    tools/make_texture_pack.py       Task 16  draws the optional stud tile PNG
    textures/stud_tile.png           Task 16  generated texture (source for uploads)
```

Studio layout after install (same for any game):

```
ReplicatedStorage.UIKit            ModuleScript  (UIKit.luau)
  Util, Decor, Controls, Containers, Readouts, Feedback, Screens, Motion   ModuleScripts
  Themes                           Folder of 6 ModuleScripts
StarterPlayer.StarterPlayerScripts.UIRuntime          LocalScript
ServerStorage.UIKitDev.KitCheck / Showcase             ModuleScripts (dev only)
ReplicatedStorage.UIKitDev.MotionCheck                 ModuleScript (dev only; clients can't see ServerStorage)
StarterPlayer.StarterPlayerScripts.ShowcaseRuntime    LocalScript (showcase place only)
```

## How to install a kit file (used by every task)

Read the workspace file, then call `multi_edit` on the UI/UX studio:

- `file_path`: the Studio path from the layout above, e.g. `game.ReplicatedStorage.UIKit.Util`
- `className`: `ModuleScript` (or `LocalScript` for `*.client.luau`)
- `edits`: `[{ "old_string": "", "new_string": "<entire file content>" }]` when the script does not exist yet. When it exists, first replace its whole source: read it with `script_read`, then one edit whose `old_string` is the full current source.

Parents must exist first. Create folders with `execute_luau`:

```lua
local function folder(parent: Instance, name: string): Instance
	local f = parent:FindFirstChild(name)
	if not f then
		f = Instance.new("Folder")
		f.Name = name
		f.Parent = parent
	end
	return f
end
folder(game:GetService("ServerStorage"), "UIKitDev")
return "ok"
```

`ReplicatedStorage.UIKit` itself is a ModuleScript, so install `UIKit.luau` before its children, and create `ReplicatedStorage.UIKit.Themes` as a Folder with the snippet above (`folder(game.ReplicatedStorage.UIKit, "Themes")`).

## How to run KitCheck (used by every task)

`execute_luau` on the UI/UX studio, `datamodel_type: "Edit"`:

```lua
local RS = game:GetService("ReplicatedStorage")
local SS = game:GetService("ServerStorage")
local temp = Instance.new("Folder")
temp.Name = "_UIKitRun"
temp.Parent = SS
local kitSource = RS:FindFirstChild("UIKit")
local kit = if kitSource then require((kitSource:Clone() :: any)) else nil
local check = SS.UIKitDev.KitCheck:Clone()
check.Parent = temp
local ok, report = pcall(function() return require(check).run(kit) end)
temp:Destroy()
return if ok then report else ("KitCheck crashed: " .. tostring(report))
```

Expected output format: `KitCheck: <n> passed, <m> failed` followed by one `- <case>: <reason>` line per failure.

---

### Task 1: Spike — confirm the Studio features the kit relies on

Answers questions the kit's fallbacks depend on. Nothing here is kept: the spike ScreenGui is deleted at the end.

**Files:**
- Modify (temporary): `UI/UX` place `StarterGui._Spike` (deleted in Step 7)
- Create: `docs/superpowers/plans/spike-results.md`

**Interfaces:**
- Produces: values for three constants used in Task 3's `Decor.luau`: `Decor.DOT_TILE` (string or nil), `Decor.USE_UISHADOW` (boolean), `Decor.USE_UIBLUR` (boolean); and a yes/no on emoji icons used by Task 8's `Showcase.luau`.

- [ ] **Step 1: Build the spike screen**

`execute_luau` (Edit) on the UI/UX studio:

```lua
local SG = game:GetService("StarterGui")
local old = SG:FindFirstChild("_Spike")
if old then old:Destroy() end
local gui = Instance.new("ScreenGui")
gui.Name = "_Spike"
gui.ZIndexBehavior = Enum.ZIndexBehavior.Sibling
local function frame(name, x, y, color)
	local f = Instance.new("Frame")
	f.Name = name
	f.Size = UDim2.fromOffset(120, 80)
	f.Position = UDim2.fromOffset(x, y)
	f.BackgroundColor3 = color
	f.BorderSizePixel = 0
	f.Parent = gui
	return f
end
-- 1 UIShadow (hard + soft)
local a = frame("Shadow", 20, 20, Color3.fromRGB(230, 40, 50))
local s = Instance.new("UIShadow")
s.Offset = UDim2.fromOffset(10, 10)
s.BlurRadius = UDim.new(0, 0)
s.Color = Color3.new(0, 0, 0)
s.Parent = a
local b = frame("SoftShadow", 170, 20, Color3.fromRGB(46, 242, 255))
local s2 = Instance.new("UIShadow")
s2.Offset = UDim2.fromOffset(0, 6)
s2.BlurRadius = UDim.new(0, 16)
s2.Color = Color3.fromRGB(46, 242, 255)
s2.Parent = b
-- 2 UIBlur
local c = frame("Blur", 320, 20, Color3.new(1, 1, 1))
c.BackgroundTransparency = 0.6
local bl = Instance.new("UIBlur")
bl.Parent = c
-- 3 whiteCircle tile
local d = Instance.new("ImageLabel")
d.Name = "Dots"
d.Size = UDim2.fromOffset(200, 120)
d.Position = UDim2.fromOffset(470, 20)
d.BackgroundColor3 = Color3.fromRGB(43, 29, 69)
d.Image = "rbxasset://textures/whiteCircle.png"
d.ScaleType = Enum.ScaleType.Tile
d.TileSize = UDim2.fromOffset(24, 24)
d.ImageTransparency = 0.7
d.Parent = gui
-- 4 Path2D chamfer rim + gradient triangles
local e = frame("Chamfer", 20, 160, Color3.fromRGB(7, 16, 25))
e.Size = UDim2.fromOffset(200, 120)
e.BackgroundTransparency = 1
local cut = 16
local hide = NumberSequence.new({ NumberSequenceKeypoint.new(0, 1), NumberSequenceKeypoint.new(0.499, 1), NumberSequenceKeypoint.new(0.501, 0), NumberSequenceKeypoint.new(1, 0) })
for _, t in { { "TL", 0, 0, 45 }, { "TR", 1, 0, 135 }, { "BR", 1, 1, 225 }, { "BL", 0, 1, -45 } } do
	local tri = Instance.new("Frame")
	tri.Name = t[1]
	tri.Size = UDim2.fromOffset(cut, cut)
	tri.Position = UDim2.new(t[2], if t[2] == 1 then -cut else 0, t[3], if t[3] == 1 then -cut else 0)
	tri.BackgroundColor3 = Color3.fromRGB(46, 242, 255)
	tri.BorderSizePixel = 0
	tri.Parent = e
	local g = Instance.new("UIGradient")
	g.Rotation = t[4]
	g.Transparency = hide
	g.Parent = tri
end
local path = Instance.new("Path2D")
path.Closed = true
path.Thickness = 2
path.Color3 = Color3.fromRGB(255, 46, 136)
path.Parent = e
path:SetControlPoints({
	Path2DControlPoint.new(UDim2.fromOffset(cut, 0)), Path2DControlPoint.new(UDim2.new(1, -cut, 0, 0)),
	Path2DControlPoint.new(UDim2.new(1, 0, 0, cut)), Path2DControlPoint.new(UDim2.new(1, 0, 1, -cut)),
	Path2DControlPoint.new(UDim2.new(1, -cut, 1, 0)), Path2DControlPoint.new(UDim2.new(0, cut, 1, 0)),
	Path2DControlPoint.new(UDim2.new(0, 0, 1, -cut)), Path2DControlPoint.new(UDim2.fromOffset(0, cut)),
})
-- 5 slant caps (aspect-constrained triangles hanging off a bar)
local f = frame("Slant", 290, 190, Color3.fromRGB(229, 0, 26))
f.Size = UDim2.fromOffset(160, 40)
for _, t in { { "CapL", 0, 1, 45 }, { "CapR", 1, 0, 225 } } do
	local cap = Instance.new("Frame")
	cap.Name = t[1]
	cap.Size = UDim2.fromScale(1, 1)
	cap.AnchorPoint = Vector2.new(t[3], 0)
	cap.Position = UDim2.fromScale(t[2], 0)
	cap.BackgroundColor3 = f.BackgroundColor3
	cap.BorderSizePixel = 0
	cap.Parent = f
	local ar = Instance.new("UIAspectRatioConstraint")
	ar.DominantAxis = Enum.DominantAxis.Height
	ar.Parent = cap
	local g = Instance.new("UIGradient")
	g.Rotation = t[4]
	g.Transparency = hide
	g.Parent = cap
end
-- 6 emoji
local emoji = Instance.new("TextLabel")
emoji.Name = "Emoji"
emoji.Size = UDim2.fromOffset(300, 60)
emoji.Position = UDim2.fromOffset(500, 170)
emoji.BackgroundTransparency = 1
emoji.TextScaled = true
emoji.Text = "🛒💎💵🐾⬆️🔄🎁⚔️🛡️"
emoji.FontFace = Font.fromEnum(Enum.Font.FredokaOne)
emoji.Parent = gui
gui.Parent = SG
return "spike built"
```

- [ ] **Step 2: Capture and judge the edit-time render**

`screen_capture` (capture_id `Spike_Edit`). Record for each of the six items: renders correctly / renders wrong / invisible. Expected: chamfer shows four cyan corner triangles inside a magenta 8-point outline; slant shows a red parallelogram leaning right ("/" ends).

- [ ] **Step 3: Check play mode**

`start_stop_play` `is_start: true`, wait for `get_studio_state` to report Client available, `screen_capture` (capture_id `Spike_Play`), then `start_stop_play` `is_start: false`. Record whether UIShadow / UIBlur / dots render on the live client too (edit-only rendering counts as "no").

- [ ] **Step 4: Check script install and require freshness**

Call `multi_edit` with `file_path: "game.ServerStorage._SpikeMod"`, `className: "ModuleScript"`, `edits: [{"old_string": "", "new_string": "return 1"}]`. Then `execute_luau`:

```lua
local m = game.ServerStorage._SpikeMod
local first = require(m:Clone())
m.Source = "return 2"
local second = require(m:Clone())
local direct = require(m)
m:Destroy()
return string.format("first=%s second=%s direct=%s", tostring(first), tostring(second), tostring(direct))
```

Expected: `first=1 second=2 direct=2`. If `m.Source = …` errors, record "Source not writable from execute_luau" (installs then always go through `multi_edit`, which is already the plan).

- [ ] **Step 5: Write `spike-results.md`**

Create `docs/superpowers/plans/spike-results.md` with one line per item, using exactly these keys so later tasks can read them:

```markdown
# Spike results (Task 1)
- UISHADOW_EDIT: yes|no
- UISHADOW_PLAY: yes|no
- UIBLUR_EDIT: yes|no
- UIBLUR_PLAY: yes|no
- DOT_TILE: yes|no   (rbxasset://textures/whiteCircle.png tiles as dots in edit AND play)
- PATH2D_CHAMFER: yes|no
- GRADIENT_TRIANGLES: yes|no
- SLANT_CAPS: yes|no
- EMOJI: yes|no      (colour emoji render in a TextLabel)
- SOURCE_WRITABLE: yes|no
- CLONE_REQUIRE_FRESH: yes|no
```

- [ ] **Step 6: Apply the decision rules**

- `Decor.USE_UISHADOW = (UISHADOW_EDIT and UISHADOW_PLAY)`; `Decor.USE_UIBLUR = (UIBLUR_EDIT and UIBLUR_PLAY)`.
- `Decor.DOT_TILE = "rbxasset://textures/whiteCircle.png"` if DOT_TILE is yes, else `nil` (studs and screentone then only appear after Task 16's texture pack).
- If PATH2D_CHAMFER, GRADIENT_TRIANGLES or SLANT_CAPS is "no": stop and tell the user. Those three underpin Cyber Holo, Battlegrounds and Kinetic Comic shapes, and the plan needs a revised shape strategy before Task 3.
- If EMOJI is "no": Task 8's `ICONS` table uses the plain-text fallback column instead of emoji.

- [ ] **Step 7: Clean up**

`execute_luau`: `game.StarterGui._Spike:Destroy() return "clean"`. Confirm with `search_game_tree` path `StarterGui` that only kit-made or user-made ScreenGuis remain.

### Task 2: KitCheck harness (the failing test suite)

**Files:**
- Create: `roblox-ui/kit/dev/KitCheck.luau`
- Install: `game.ServerStorage.UIKitDev.KitCheck` (ModuleScript)

**Interfaces:**
- Consumes: nothing yet (UIKit does not exist, so the suite must fail cleanly).
- Produces: `KitCheck.run(UIKit: any): string` and `KitCheck.EXPECTED_THEMES: { string }`. Every later task runs this and adds to `EXPECTED_THEMES` when it adds a theme. It pins these builder signatures, which Tasks 3–6 must match exactly:
  - `UIKit.Util.abbreviate(n: number): string`, `UIKit.Util.sequence(stops: {Color3}): ColorSequence`, `UIKit.Util.strokeFactor(screenHeight: number): number`
  - `UIKit.themeNames(): {string}`, `UIKit.theme(name: string): Theme`
  - `UIKit.Screen(theme, {Name, FullScreen?, DisplayOrder?, Enabled?, Role?}): ScreenGui`
  - `UIKit.Panel(theme, {Title, Icon?, Body?: "list"|"grid"|"none", Columns?, CellAspect?, Tilt?, Size?, Position?, AnchorPoint?, AspectRatio?, Name?, Parent?}): (Frame, GuiObject)`
  - `UIKit.List(theme, {Name?, Gap?, Size?, Position?, AnchorPoint?, Parent?}): ScrollingFrame`, `UIKit.Grid(theme, {Columns?, Gap?, CellAspect?, Name?, Size?, Position?, AnchorPoint?, Parent?}): ScrollingFrame`
  - `UIKit.Button(theme, {Text, Variant?, Icon?, Name?, Size?, Position?, AnchorPoint?, LayoutOrder?, ZIndex?, Parent?}): TextButton`
  - `UIKit.setVariant(theme, button, variantName)`
  - `UIKit.IconButton(theme, {Icon, Caption?, Badge?, Name?, Size?, Position?, AnchorPoint?, LayoutOrder?, Parent?}): TextButton`
  - `UIKit.Toggle(theme, {On?, Name?, Size?, Position?, AnchorPoint?, Parent?}): TextButton`
  - `UIKit.Slider(theme, {Value?, Name?, Size?, Position?, AnchorPoint?, Parent?}): Frame`
  - `UIKit.TextInput(theme, {Placeholder?, Name?, Size?, Position?, AnchorPoint?, Parent?}): Frame` (child TextBox `Box`)
  - `UIKit.Tabs(theme, {Tabs, Selected?, Name?, Size?, Position?, AnchorPoint?, Parent?}): Frame`
  - `UIKit.Card(theme, {Title, Subtitle?, Icon?, Action?, ActionVariant?, Height?, Name?, Visible?, LayoutOrder?, Parent?}): Frame`
  - `UIKit.Bar(theme, {Style?, Kind?, Value?, RightKind?, RightValue?, Label?, ValueText?, Segments?, Emblem?, Icon?, Name?, Size?, Position?, AnchorPoint?, Parent?}): Frame`
  - `UIKit.Currency(theme, {Icon, Amount, Kind?, Name?, Size?, Position?, AnchorPoint?, LayoutOrder?, Parent?}): Frame`
  - `UIKit.Badge(theme, {Text, Kind?, Slant?, Rotation?, Name?, Size?, Position?, AnchorPoint?, Parent?}): Frame`
  - `UIKit.Slot(theme, {Key?, Title?, Icon?, Value?, Cooldown?, Selected?, Name?, Size?, Position?, LayoutOrder?, Visible?, Parent?}): TextButton`
  - `UIKit.Hotbar(theme, {Slots: {SlotProps}, Name?, Size?, Position?, AnchorPoint?, Parent?}): Frame`
  - `UIKit.Tooltip(theme, {Text, Name?, Size?, Position?, AnchorPoint?, Parent?}): Frame`
  - `UIKit.ToastStack(theme, {Name?, Size?, Position?, AnchorPoint?, Parent?}): Frame` (hidden `Template` toast inside)
  - `UIKit.Toast(theme, {Text, Kind?, Name?, Visible?, LayoutOrder?, Parent?}): Frame`
  - `UIKit.Popup(theme, {Title, Body?, Icon?, Confirm?, Cancel?, Name?, Parent?}): Frame` (dim overlay > `Main` > `Body` > `Actions`)
  - `UIKit.Splash(theme, {Text, Kind?, Name?, Size?, Position?, AnchorPoint?, Parent?}): Frame`
  - `UIKit.DamageNumber(theme, {Amount, Crit?, Name?, Position?, Parent?}): TextLabel`
  - `UIKit.LoadingScreen(theme, {Title, Tip?, Progress?, Name?}): ScreenGui`
  - `UIKit.MainMenu(theme, {Title, Subtitle?, Buttons?, Name?}): ScreenGui`

- [ ] **Step 1: Write the suite**

Create `roblox-ui/kit/dev/KitCheck.luau` with the content of the code block below. (The same file is the source of truth for every later task; when a task says "add X to `EXPECTED_THEMES`", edit this file and re-install it.)

```lua
--!strict
-- Structural self-test for UIKit. Builds every component in every theme and checks the contract names that
-- Motion and game code rely on. Run it through MCP execute_luau (see workflow.md); it returns a report string.

local KitCheck = {}

-- Themes the kit must ship. A task that adds a theme adds its name here first (red), then the theme (green).
KitCheck.EXPECTED_THEMES = { "StudSimulator" }

local REQUIRED_TOKENS = {
	"name", "hudLayout",
	"color.backdrop", "color.base", "color.baseTransparency", "color.surface", "color.surfaceTransparency",
	"color.rim", "color.barEdge", "color.text", "color.textMuted", "color.textStroke", "color.track", "color.header",
	"color.variants.primary", "color.variants.secondary", "color.variants.success", "color.variants.danger",
	"color.variants.ghost",
	"color.bars.health", "color.bars.energy", "color.bars.xp", "color.bars.accent",
	"font.display", "font.body", "font.number",
	"textStroke.display", "textStroke.body",
	"stroke.panel", "stroke.control", "stroke.slot",
	"radius.panel", "radius.control", "radius.slot", "radius.pill",
	"shape.chamfer", "shape.slantButtons", "shape.tilt", "shape.header", "shape.iconFrame", "shape.gradientText",
	"shape.barStyle",
	"motion.style", "motion.easing", "motion.fast", "motion.normal", "motion.slow", "motion.pressScale",
	"motion.openFrom", "motion.worldBlur",
	"assets",
	"decorate.panel", "decorate.header", "decorate.button", "decorate.slot", "decorate.bar", "decorate.screen",
}

local function lookup(root: any, path: string): any
	local node = root
	for key in string.gmatch(path, "[^%.]+") do
		if type(node) ~= "table" then
			return nil
		end
		node = node[key]
	end
	return node
end

local function need(root: Instance, path: string)
	local node: Instance? = root
	for name in string.gmatch(path, "[^%.]+") do
		node = if node then node:FindFirstChild(name) else nil
	end
	assert(node ~= nil, root.Name .. " is missing " .. path)
end

-- Long text must shrink to fit, and every stroke must be rescalable for phones
local function assertSafe(root: Instance)
	for _, d in root:GetDescendants() do
		if d:IsA("TextLabel") then
			assert(d.TextScaled, d:GetFullName() .. " is not TextScaled")
			assert(d:FindFirstChildOfClass("UITextSizeConstraint"), d:GetFullName() .. " has no UITextSizeConstraint")
		elseif d:IsA("UIStroke") then
			assert(type(d:GetAttribute("BaseThickness")) == "number", d:GetFullName() .. " has no BaseThickness")
		end
	end
end

local function report(passed: number, failures: { string }): string
	local lines = { string.format("KitCheck: %d passed, %d failed", passed, #failures) }
	for _, failure in failures do
		table.insert(lines, "- " .. failure)
	end
	return table.concat(lines, "\n")
end

function KitCheck.run(UIKit: any): string
	local passed = 0
	local failures: { string } = {}
	local function case(label: string, fn: () -> ())
		local ok, err = pcall(fn)
		if ok then
			passed += 1
		else
			table.insert(failures, label .. ": " .. tostring(err))
		end
	end

	case("kit installed", function()
		assert(UIKit ~= nil, "ReplicatedStorage.UIKit not found")
	end)
	if UIKit == nil then
		return report(passed, failures)
	end

	case("Util.abbreviate", function()
		local cases = {
			{ 0, "0" }, { 999, "999" }, { 999.6, "1K" }, { 1000, "1K" }, { 1234, "1.2K" }, { 15000, "15K" },
			{ 999999, "1M" }, { 1500000, "1.5M" }, { -2500, "-2.5K" }, { 2.5e12, "2.5T" },
		}
		for _, c in cases do
			local got = UIKit.Util.abbreviate(c[1])
			assert(got == c[2], string.format("abbreviate(%s) = %s, want %s", tostring(c[1]), got, c[2]))
		end
	end)

	case("Util.sequence", function()
		local one = UIKit.Util.sequence({ Color3.new(1, 0, 0) })
		assert(#one.Keypoints == 2, "a single stop should make a 2-keypoint sequence")
		local three = UIKit.Util.sequence({ Color3.new(1, 0, 0), Color3.new(0, 1, 0), Color3.new(0, 0, 1) })
		assert(math.abs(three.Keypoints[2].Time - 0.5) < 1e-6, "the middle stop should sit at 0.5")
	end)

	case("Util.strokeFactor", function()
		assert(UIKit.Util.strokeFactor(600) == 1, "600 px is the design height")
		assert(UIKit.Util.strokeFactor(300) == 0.75, "small screens clamp to 0.75")
		assert(UIKit.Util.strokeFactor(2160) == 1.75, "huge screens clamp to 1.75")
	end)

	local names = UIKit.themeNames()
	for _, expected in KitCheck.EXPECTED_THEMES do
		case("theme " .. expected .. " exists", function()
			assert(table.find(names, expected), "no theme module named " .. expected)
		end)
	end

	for _, name in names do
		local theme = UIKit.theme(name)
		local function build(label: string, fn: () -> Instance?)
			case(name .. " " .. label, function()
				local root = fn()
				if root then
					assertSafe(root)
					root:Destroy()
				end
			end)
		end

		case(name .. " tokens", function()
			assert(theme.name == name, "theme.name must equal the module name")
			for _, path in REQUIRED_TOKENS do
				assert(lookup(theme, path) ~= nil, "missing token " .. path)
			end
			for vname, v in theme.color.variants do
				assert(type(v.fill) == "table" and #v.fill >= 1, vname .. ".fill needs at least one colour")
				assert(typeof(v.text) == "Color3" and typeof(v.edge) == "Color3" and typeof(v.textStroke) == "Color3",
					vname .. " needs text, edge and textStroke colours")
				assert(type(v.fillTransparency) == "number", vname .. ".fillTransparency must be a number")
			end
			assert(table.find({ "simulator", "combat" }, theme.hudLayout), "hudLayout must be simulator|combat")
			assert(table.find({ "tab", "strip", "center" }, theme.shape.header), "shape.header must be tab|strip|center")
			assert(table.find({ "single", "split", "segmented" }, theme.shape.barStyle), "bad shape.barStyle")
			assert(table.find({ "pop", "slam", "flicker", "slide", "stamp", "fade" }, theme.motion.style), "bad motion.style")
		end)

		build("Screen", function()
			local hud = UIKit.Screen(theme, { Name = "HUD" })
			assert(hud.ScreenInsets == Enum.ScreenInsets.CoreUISafeInsets and not hud.IgnoreGuiInset,
				"HUD screens must keep clear of the top bar")
			assert(hud:GetAttribute("UIKitBuilt") == true and hud:GetAttribute("UIKitTheme") == name, "screen attributes missing")
			local full = UIKit.Screen(theme, { Name = "Full", FullScreen = true })
			assert(full.IgnoreGuiInset and full.ScreenInsets == Enum.ScreenInsets.None, "full-screen guis must cover the top bar")
			full:Destroy()
			return hud
		end)

		build("Panel(list)", function()
			local main, list = UIKit.Panel(theme, { Title = "Legendary Golden Dumbbell of Power", Icon = "🛒", Body = "list" })
			assert(main.Name == "Main" and main:HasTag("UIKit.Panel"), "panel root must be Main, tagged UIKit.Panel")
			need(main, "TitleTab.Title")
			need(main, "Close.Label")
			assert(main.Close:HasTag("UIKit.Close"), "Close must be tagged UIKit.Close")
			assert(list.Name == "List" and list:IsA("ScrollingFrame") and list:FindFirstChildOfClass("UIListLayout"), "list body wrong")
			return main
		end)

		build("Panel(grid)", function()
			local main, grid = UIKit.Panel(theme, { Title = "Inventory", Body = "grid", Columns = 4 })
			local layout = grid:FindFirstChildOfClass("UIGridLayout")
			assert(grid.Name == "Grid" and layout, "grid body wrong")
			assert(typeof(layout:GetAttribute("DesignCell")) == "UDim2", "grid layout needs DesignCell for the pixel fix")
			return main
		end)

		build("Panel(none)", function()
			local main, body = UIKit.Panel(theme, { Title = "Settings", Body = "none" })
			assert(body.Name == "Body", "a none body must be a Frame named Body")
			return main
		end)

		for vname in theme.color.variants do
			build("Button(" .. vname .. ")", function()
				local b = UIKit.Button(theme, { Text = "Play", Variant = vname })
				need(b, "Label")
				assert(b:IsA("TextButton") and b.Text == "" and b:HasTag("UIKit.Button") and b:GetAttribute("Variant") == vname,
					"button contract wrong")
				return b
			end)
		end

		build("setVariant", function()
			local b = UIKit.Button(theme, { Text = "Tab", Variant = "secondary" })
			UIKit.setVariant(theme, b, "primary")
			assert(b:GetAttribute("Variant") == "primary", "Variant attribute not updated")
			assert(b.Label.TextColor3 == theme.color.variants.primary.text, "label colour not updated")
			return b
		end)

		build("IconButton", function()
			local b = UIKit.IconButton(theme, { Icon = "🛒", Caption = "Shop" })
			need(b, "Icon")
			need(b, "Caption")
			assert(b:HasTag("UIKit.Button"), "icon buttons need press feedback too")
			return b
		end)

		build("Toggle", function()
			local t = UIKit.Toggle(theme, { On = true })
			need(t, "Knob")
			need(t, "Fill")
			assert(t:GetAttribute("On") == true and t:HasTag("UIKit.Toggle"), "toggle contract wrong")
			return t
		end)

		build("Slider", function()
			local s = UIKit.Slider(theme, { Value = 0.3 })
			need(s, "Track.Fill")
			need(s, "Knob")
			assert(math.abs(s:GetAttribute("Value") - 0.3) < 1e-6 and s:HasTag("UIKit.Slider"), "slider contract wrong")
			return s
		end)

		build("TextInput", function()
			local i = UIKit.TextInput(theme, { Placeholder = "Enter code" })
			need(i, "Box")
			return i
		end)

		build("Tabs", function()
			local t = UIKit.Tabs(theme, { Tabs = { "Featured", "Passes", "Coins" }, Selected = "Passes" })
			assert(t:GetAttribute("Selected") == "Passes" and t:HasTag("UIKit.Tabs"), "tabs contract wrong")
			assert(t.Passes:GetAttribute("Variant") == "primary" and t.Featured:GetAttribute("Variant") == "secondary",
				"the selected tab must use the primary variant")
			return t
		end)

		build("Card(template)", function()
			local c = UIKit.Card(theme, {
				Name = "Template", Title = "2X Strength", Subtitle = "Double gains", Icon = "💪", Action = "R$ 199", Visible = false,
			})
			need(c, "Title")
			need(c, "Subtitle")
			need(c, "Action.Label")
			assert(c.Visible == false, "templates must start hidden")
			return c
		end)

		for _, style in { "single", "split", "segmented" } do
			build("Bar(" .. style .. ")", function()
				local b = UIKit.Bar(theme, { Style = style, Value = 0.5, Label = "HP", ValueText = "50/100", Segments = 10 })
				if style == "split" then
					need(b, "Left.Fill")
					need(b, "Right.Fill")
					need(b, "Emblem")
				else
					need(b, "Fill")
				end
				if style == "segmented" then
					local ticks = b:FindFirstChild("Ticks")
					assert(ticks and #ticks:GetChildren() == 9, "10 segments need 9 ticks")
				end
				return b
			end)
		end

		build("Currency", function()
			local c = UIKit.Currency(theme, { Icon = "💵", Amount = "$1.2K", Kind = "accent" })
			need(c, "Amount")
			need(c, "Icon")
			return c
		end)

		build("Badge", function()
			local b = UIKit.Badge(theme, { Text = "NEW!", Kind = "accent" })
			need(b, "Label")
			return b
		end)

		build("Slot", function()
			local s = UIKit.Slot(theme, { Key = "1", Title = "Lapse Blue", Cooldown = 0.5 })
			need(s, "Key")
			need(s, "Title")
			need(s, "Cooldown")
			return s
		end)

		build("Hotbar", function()
			local h = UIKit.Hotbar(theme, { Slots = { { Key = "1" }, { Key = "2" }, { Key = "3" }, { Key = "4" } } })
			local count = 0
			for _, child in h:GetChildren() do
				if child:IsA("GuiButton") then
					count += 1
				end
			end
			assert(count == 4, "the hotbar should hold 4 slots, has " .. count)
			return h
		end)

		build("Tooltip", function()
			local t = UIKit.Tooltip(theme, { Text = "Deals 2x damage" })
			need(t, "Label")
			return t
		end)

		build("ToastStack", function()
			local s = UIKit.ToastStack(theme, {})
			need(s, "Template.Label")
			assert(s.Template.Visible == false and s:FindFirstChildOfClass("UIListLayout"), "toast stack contract wrong")
			return s
		end)

		build("Popup", function()
			local p = UIKit.Popup(theme, { Title = "You got!", Body = "Golden Dumbbell", Icon = "🎁", Confirm = "Claim", Cancel = "Later" })
			need(p, "Main.Body.Actions.Confirm")
			need(p, "Main.Body.Actions.Cancel")
			return p
		end)

		build("Splash", function()
			local s = UIKit.Splash(theme, { Text = "LEVEL UP!", Kind = "xp" })
			need(s, "Text")
			return s
		end)

		build("DamageNumber", function()
			local d = UIKit.DamageNumber(theme, { Amount = "1.2K", Crit = true })
			assert(d:IsA("TextLabel"), "damage numbers are TextLabels")
			return d
		end)

		build("LoadingScreen", function()
			local g = UIKit.LoadingScreen(theme, { Title = "Lift a Rock", Tip = "Tip: rebirth for x1.5" })
			need(g, "Background.Progress.Fill")
			need(g, "Background.Title")
			assert(g:IsA("ScreenGui") and g.IgnoreGuiInset, "the loading screen must be full-screen")
			return g
		end)

		build("MainMenu", function()
			local g = UIKit.MainMenu(theme, { Title = "Lift a Rock", Buttons = { "PLAY", "SHOP", "SETTINGS" } })
			need(g, "Background.Buttons.PLAY.Label")
			return g
		end)
	end

	return report(passed, failures)
end

return KitCheck
```

- [ ] **Step 2: Install it**

Create the dev folder with the folder snippet (`folder(game:GetService("ServerStorage"), "UIKitDev")`), then `multi_edit` `game.ServerStorage.UIKitDev.KitCheck`, `className: "ModuleScript"`, with the whole file as the first edit's `new_string`.

- [ ] **Step 3: Run it and watch it fail**

Run the KitCheck runner snippet from "How to run KitCheck".
Expected:

```
KitCheck: 0 passed, 1 failed
- kit installed: ReplicatedStorage.UIKit not found
```

- [ ] **Step 4: Commit**

```bash
git add roblox-ui/kit/dev/KitCheck.luau
git commit -m "test: add UIKit structural self-test"
```

### Task 3: Kit core — UIKit entry, Util, Decor

**Files:**
- Create: `roblox-ui/kit/UIKit.luau`, `roblox-ui/kit/Util.luau`, `roblox-ui/kit/Decor.luau`
- Install: `game.ReplicatedStorage.UIKit` (ModuleScript), `.Util`, `.Decor` (ModuleScripts), `.Themes` (Folder)

**Interfaces:**
- Consumes: spike constants from `docs/superpowers/plans/spike-results.md` (Task 1).
- Produces:
  - `UIKit` table merging every function exported by `Containers`, `Controls`, `Readouts`, `Feedback`, `Screens` (modules that don't exist yet contribute nothing), plus `UIKit.Util`, `UIKit.Decor`, `UIKit.theme(name)`, `UIKit.themeNames()`.
  - `Util.make(className, props?, children?) -> Instance`, `Util.shade(color, amount) -> Color3`, `Util.sequence(stops) -> ColorSequence`, `Util.gradient(parent, stops, rotation?) -> UIGradient`, `Util.corner(parent, radius) -> UICorner`, `Util.stroke(parent, color, thickness, transparency?) -> UIStroke?` (named `Edge`), `Util.padding(parent, all) -> UIPadding`, `Util.aspect(parent, ratio) -> UIAspectRatioConstraint`, `Util.place(inst, props, defaultSize)`, `Util.text(theme, TextProps) -> TextLabel`, `Util.icon(theme, value, props) -> GuiObject`, `Util.tag(inst, kind, theme)`, `Util.strokeFactor(h) -> number`, `Util.scaleStrokes(root, h)`, `Util.pixelGrid(layout) -> RBXScriptConnection?`, `Util.abbreviate(n) -> string`.
  - `Decor.DOT_TILE`, `Decor.USE_UISHADOW`, `Decor.USE_UIBLUR`, and `Decor.triangle / tile / studs / dots / gloss / shadow / hardShadow / glow / glass / chamfer / slant / burst / rays / speedlines / scanlines / brackets / ink / ornate / divider / vignette / embers / slash / ticks` (signatures in the code below).

- [ ] **Step 1: Write `roblox-ui/kit/Util.luau`**

```lua
--!strict
-- Instance and colour helpers shared by every UIKit module. Nothing here yields or needs a player, so it runs
-- the same at edit time (MCP execute_luau) and at runtime.

local Util = {}

-- Strokes are designed for a 600-px-tall screen (roughly Studio's viewport); see scaleStrokes
Util.DESIGN_HEIGHT = 600
local MIN_STROKE_FACTOR = 0.75
local MAX_STROKE_FACTOR = 1.75
local SUFFIXES = { "", "K", "M", "B", "T", "Qa", "Qi" }

function Util.make(className: string, props: { [string]: any }?, children: { Instance }?): any
	local inst = Instance.new(className)
	local parent: Instance? = nil
	if props then
		for key, value in props do
			if key == "Parent" then
				parent = value
			else
				(inst :: any)[key] = value
			end
		end
	end
	if children then
		for _, child in children do
			child.Parent = inst
		end
	end
	if parent then
		inst.Parent = parent
	end
	return inst
end

-- amount < 0 darkens toward black, amount > 0 lightens toward white (both by up to 1)
function Util.shade(color: Color3, amount: number): Color3
	if amount < 0 then
		return color:Lerp(Color3.new(0, 0, 0), -amount)
	end
	return color:Lerp(Color3.new(1, 1, 1), amount)
end

function Util.sequence(stops: { Color3 }): ColorSequence
	if #stops == 1 then
		return ColorSequence.new(stops[1])
	end
	local points = {}
	for i, color in stops do
		table.insert(points, ColorSequenceKeypoint.new((i - 1) / (#stops - 1), color))
	end
	return ColorSequence.new(points)
end

-- The gradient carries the colour, so give its parent BackgroundColor3 = white (UIGradient multiplies)
function Util.gradient(parent: Instance, stops: { Color3 }, rotation: number?): UIGradient
	return Util.make("UIGradient", { Color = Util.sequence(stops), Rotation = rotation or 90, Parent = parent })
end

function Util.corner(parent: Instance, radius: UDim): UICorner
	return Util.make("UICorner", { CornerRadius = radius, Parent = parent })
end

-- Border stroke named "Edge". Thickness 0 means the theme wants no border here, so nothing is made.
function Util.stroke(parent: Instance, color: Color3, thickness: number, transparency: number?): UIStroke?
	if thickness <= 0 then
		return nil
	end
	local stroke = Util.make("UIStroke", {
		Name = "Edge",
		Color = color,
		Thickness = thickness,
		Transparency = transparency or 0,
		ApplyStrokeMode = Enum.ApplyStrokeMode.Border,
		LineJoinMode = Enum.LineJoinMode.Round,
		Parent = parent,
	})
	stroke:SetAttribute("BaseThickness", thickness)
	return stroke
end

function Util.padding(parent: Instance, all: UDim): UIPadding
	return Util.make("UIPadding", {
		PaddingTop = all, PaddingBottom = all, PaddingLeft = all, PaddingRight = all, Parent = parent,
	})
end

function Util.aspect(parent: Instance, ratio: number): UIAspectRatioConstraint
	return Util.make("UIAspectRatioConstraint", { AspectRatio = ratio, Parent = parent })
end

-- Applies the layout props every builder accepts (Name, Size, Position, AnchorPoint, LayoutOrder, Visible)
function Util.place(inst: GuiObject, props: { [string]: any }, defaultSize: UDim2)
	if props.Name then
		inst.Name = props.Name
	end
	inst.Size = props.Size or defaultSize
	inst.Position = props.Position or UDim2.new()
	inst.AnchorPoint = props.AnchorPoint or Vector2.zero
	inst.LayoutOrder = props.LayoutOrder or 0
	if props.Visible ~= nil then
		inst.Visible = props.Visible
	end
end

export type TextProps = {
	Name: string?,
	Text: string,
	Role: string?, -- "display" | "body" | "number"
	Color: Color3?,
	StrokeColor: Color3?,
	Stroke: number?, -- overrides the theme's text stroke thickness
	Size: UDim2?,
	Position: UDim2?,
	AnchorPoint: Vector2?,
	XAlign: Enum.TextXAlignment?,
	MaxTextSize: number?,
	Rotation: number?,
	ZIndex: number?,
	RichText: boolean?,
	Parent: Instance?,
}

-- Every kit label is TextScaled with a size cap, so long text shrinks instead of overflowing
function Util.text(theme: any, props: TextProps): TextLabel
	local role = props.Role or "body"
	local label = Util.make("TextLabel", {
		Name = props.Name or "Label",
		Text = props.Text,
		FontFace = theme.font[role],
		TextColor3 = props.Color or theme.color.text,
		TextScaled = true,
		RichText = props.RichText == true,
		TextXAlignment = props.XAlign or Enum.TextXAlignment.Center,
		BackgroundTransparency = 1,
		Size = props.Size or UDim2.fromScale(1, 1),
		Position = props.Position or UDim2.new(),
		AnchorPoint = props.AnchorPoint or Vector2.zero,
		Rotation = props.Rotation or 0,
		ZIndex = props.ZIndex or 4,
		Parent = props.Parent,
	})
	Util.make("UITextSizeConstraint", { MaxTextSize = props.MaxTextSize or 72, MinTextSize = 6, Parent = label })
	local thickness = props.Stroke or (if role == "display" then theme.textStroke.display else theme.textStroke.body)
	if thickness > 0 then
		local stroke = Util.make("UIStroke", {
			Name = "TextStroke",
			Color = props.StrokeColor or theme.color.textStroke,
			Thickness = thickness,
			ApplyStrokeMode = Enum.ApplyStrokeMode.Contextual,
			LineJoinMode = Enum.LineJoinMode.Round,
			Parent = label,
		})
		stroke:SetAttribute("BaseThickness", thickness)
	end
	return label
end

-- An icon is an image ("rbxassetid://…", "rbxasset://…", "http…") or a glyph/emoji drawn as text, so the kit
-- works with zero uploads
function Util.icon(theme: any, value: string, props: { [string]: any }): GuiObject
	local isImage = string.find(value, "^rbx") ~= nil or string.find(value, "^http") ~= nil
	local icon: GuiObject
	if isImage then
		icon = Util.make("ImageLabel", {
			Name = props.Name or "Icon",
			Image = value,
			ScaleType = Enum.ScaleType.Fit,
			BackgroundTransparency = 1,
			Size = props.Size or UDim2.fromScale(1, 1),
			Position = props.Position or UDim2.new(),
			AnchorPoint = props.AnchorPoint or Vector2.zero,
			ZIndex = props.ZIndex or 4,
		})
	else
		icon = Util.text(theme, {
			Name = props.Name or "Icon",
			Text = value,
			Role = "display",
			Stroke = 0,
			MaxTextSize = 200,
			Color = props.Color,
			Size = props.Size,
			Position = props.Position,
			AnchorPoint = props.AnchorPoint,
			ZIndex = props.ZIndex,
		})
	end
	Util.aspect(icon, 1)
	icon.Parent = props.Parent
	return icon
end

function Util.tag(inst: Instance, kind: string, theme: any)
	inst:AddTag("UIKit." .. kind)
	inst:SetAttribute("UIKitTheme", theme.name)
end

function Util.strokeFactor(screenHeight: number): number
	return math.clamp(screenHeight / Util.DESIGN_HEIGHT, MIN_STROKE_FACTOR, MAX_STROKE_FACTOR)
end

-- Pixel strokes look twice as heavy on a phone as on a big monitor. Kit strokes keep their design thickness in
-- BaseThickness; this rescales them (and Path2D rims) for the current screen height.
function Util.scaleStrokes(root: Instance, screenHeight: number)
	local factor = Util.strokeFactor(screenHeight)
	for _, d in root:GetDescendants() do
		if d:IsA("UIStroke") or d:IsA("Path2D") then
			local base = d:GetAttribute("BaseThickness")
			if type(base) == "number" then
				(d :: any).Thickness = math.max(1, base * factor)
			end
		end
	end
end

-- A UIGridLayout with Scale cells inside an auto-sizing ScrollingFrame never settles: the cells scale with the
-- canvas they make grow, so scrolling stops part-way (found in Lift a Rock's Index). Cells are designed in Scale
-- (kept in attributes) and turned into pixels of the visible window here, again whenever the window resizes.
function Util.pixelGrid(layout: UIGridLayout): RBXScriptConnection?
	local scroller = layout.Parent
	local cell = layout:GetAttribute("DesignCell")
	local gap = layout:GetAttribute("DesignGap")
	if not scroller or not scroller:IsA("ScrollingFrame") or typeof(cell) ~= "UDim2" or typeof(gap) ~= "UDim2" then
		return nil
	end
	local aspect = layout:GetAttribute("CellAspect")
	local cellAspect = if type(aspect) == "number" and aspect > 0 then aspect else 1
	local function apply()
		local padding = scroller:FindFirstChildOfClass("UIPadding")
		local inset = if padding then padding.PaddingLeft.Offset + padding.PaddingRight.Offset else 0
		local width = math.max(0, scroller.AbsoluteSize.X - scroller.ScrollBarThickness - inset)
		local cellWidth = math.floor(cell.X.Scale * width + cell.X.Offset)
		layout.CellSize = UDim2.fromOffset(cellWidth, math.floor(cellWidth / cellAspect))
		layout.CellPadding = UDim2.fromOffset(math.floor(gap.X.Scale * width + gap.X.Offset), math.floor(gap.Y.Scale * width + gap.Y.Offset))
	end
	apply()
	return scroller:GetPropertyChangedSignal("AbsoluteSize"):Connect(apply)
end

-- 999.6 -> "1K", 999999 -> "1M", -2500 -> "-2.5K". Values that would round up to 1000 move to the next suffix.
function Util.abbreviate(n: number): string
	if n ~= n then
		return "0"
	end
	local sign = if n < 0 then "-" else ""
	local value = math.abs(n)
	if value < 999.5 then
		return sign .. tostring(math.floor(value + 0.5))
	end
	local i = 1
	repeat
		value /= 1000
		i += 1
	until value < 999.95 or i == #SUFFIXES
	local text = (string.gsub(string.format("%.1f", value), "%.0$", ""))
	return sign .. text .. SUFFIXES[i]
end

return Util
```

- [ ] **Step 2: Write `roblox-ui/kit/Decor.luau`**

Set the three constants at the top from `spike-results.md` (Task 1 Step 6) before installing.

```lua
--!strict
-- Signature details that themes bolt onto components. Everything is procedural so it works with zero uploaded
-- assets; when a theme has uploaded textures (theme.assets) those are used instead.

local Util = require(script.Parent.Util)
local make = Util.make

local Decor = {}

-- From Task 1's spike. DOT_TILE is a client-bundled texture: fine for polish, not guaranteed forever.
Decor.DOT_TILE = "rbxasset://textures/whiteCircle.png" :: string?
Decor.USE_UISHADOW = true
Decor.USE_UIBLUR = true

local WHITE = Color3.new(1, 1, 1)
local BLACK = Color3.new(0, 0, 0)
local CORNERS = { Vector2.new(0, 0), Vector2.new(1, 0), Vector2.new(0, 1), Vector2.new(1, 1) }

-- A square whose UIGradient hides one diagonal half. rotation picks the visible half:
-- 45 = bottom-right, 135 = bottom-left, 225 = top-left, -45 = top-right
local TRIANGLE_HIDE = NumberSequence.new({
	NumberSequenceKeypoint.new(0, 1),
	NumberSequenceKeypoint.new(0.499, 1),
	NumberSequenceKeypoint.new(0.501, 0),
	NumberSequenceKeypoint.new(1, 0),
})

function Decor.triangle(parent: Instance, name: string, color: Color3, transparency: number, rotation: number, props: { [string]: any }): Frame
	local tri = make("Frame", {
		Name = name,
		BackgroundColor3 = color,
		BackgroundTransparency = transparency,
		BorderSizePixel = 0,
		Size = props.Size,
		Position = props.Position or UDim2.new(),
		AnchorPoint = props.AnchorPoint or Vector2.zero,
		ZIndex = props.ZIndex or 1,
		Parent = parent,
	})
	make("UIGradient", { Rotation = rotation, Transparency = TRIANGLE_HIDE, Parent = tri })
	return tri
end

local function stripShapeOf(frame: GuiObject)
	for _, child in frame:GetChildren() do
		if child:IsA("UICorner") or (child:IsA("UIStroke") and child.Name == "Edge") then
			child:Destroy()
		end
	end
end

function Decor.tile(parent: GuiObject, image: string, tilePx: number, transparency: number, radius: UDim?, color: Color3?): ImageLabel
	local tile = make("ImageLabel", {
		Name = "Texture",
		Image = image,
		ScaleType = Enum.ScaleType.Tile,
		TileSize = UDim2.fromOffset(tilePx, tilePx),
		ImageTransparency = transparency,
		ImageColor3 = color or WHITE,
		BackgroundTransparency = 1,
		Size = UDim2.fromScale(1, 1),
		ZIndex = 1,
		Parent = parent,
	})
	if radius then
		Util.corner(tile, radius)
	end
	return tile
end

-- Stud field: the theme's uploaded stud tile if there is one, else the built-in dot tile
function Decor.studs(parent: GuiObject, theme: any, transparency: number, tilePx: number, radius: UDim?)
	local image = theme.assets.studTile or Decor.DOT_TILE
	if image then
		Decor.tile(parent, image, tilePx, transparency, radius)
	end
end

-- Halftone dots over a region (screentone). Fade = gradient rotation that fades the dots out across the region.
function Decor.dots(parent: GuiObject, color: Color3, transparency: number, tilePx: number, props: { [string]: any }?): ImageLabel?
	if not Decor.DOT_TILE then
		return nil
	end
	local p = props or {}
	local field = Decor.tile(parent, Decor.DOT_TILE, tilePx, transparency, nil, color)
	field.Name = "Screentone"
	field.Size = p.Size or UDim2.fromScale(1, 1)
	field.Position = p.Position or UDim2.new()
	field.AnchorPoint = p.AnchorPoint or Vector2.zero
	if p.Fade then
		make("UIGradient", { Rotation = p.Fade, Transparency = NumberSequence.new(0, 1), Parent = field })
	end
	return field
end

-- Diagonal gloss streaks plus a soft top shine (the "Streaks" overlay on Lift a Rock buttons)
function Decor.gloss(parent: GuiObject, strength: number, radius: UDim?)
	local clear = 1 - strength
	local band = make("Frame", {
		Name = "Gloss", BackgroundColor3 = WHITE, BorderSizePixel = 0, Size = UDim2.fromScale(1, 1), ZIndex = 2, Parent = parent,
	})
	if radius then
		Util.corner(band, radius)
	end
	make("UIGradient", {
		Rotation = -60,
		Transparency = NumberSequence.new({
			NumberSequenceKeypoint.new(0, 1), NumberSequenceKeypoint.new(0.2, 1), NumberSequenceKeypoint.new(0.26, clear),
			NumberSequenceKeypoint.new(0.34, clear), NumberSequenceKeypoint.new(0.4, 1), NumberSequenceKeypoint.new(0.46, 1),
			NumberSequenceKeypoint.new(0.5, (1 + clear) / 2), NumberSequenceKeypoint.new(0.54, 1), NumberSequenceKeypoint.new(1, 1),
		}),
		Parent = band,
	})
	local shine = make("Frame", {
		Name = "Shine", BackgroundColor3 = WHITE, BorderSizePixel = 0, Size = UDim2.fromScale(1, 0.5), ZIndex = 2, Parent = parent,
	})
	if radius then
		Util.corner(shine, radius)
	end
	make("UIGradient", { Rotation = 90, Transparency = NumberSequence.new(1 - strength * 0.7, 1), Parent = shine })
end

-- Native drop shadow. Returns false when UIShadow is off so callers can fall back.
function Decor.shadow(frame: GuiObject, color: Color3, offset: Vector2, blur: number, transparency: number): boolean
	if not Decor.USE_UISHADOW then
		return false
	end
	make("UIShadow", {
		Name = "Shadow",
		Color = color,
		Offset = UDim2.fromOffset(offset.X, offset.Y),
		BlurRadius = UDim.new(0, blur),
		Transparency = transparency,
		Parent = frame,
	})
	return true
end

-- Solid offset shadow (comic / manga). The fallback draws the frame's fill on a child "Face" so a child "Drop"
-- can sit under it: children always draw above their parent's own background.
function Decor.hardShadow(frame: GuiObject, color: Color3, offset: Vector2)
	if Decor.shadow(frame, color, offset, 0, 0) then
		return
	end
	local face = make("Frame", {
		Name = "Face",
		BackgroundColor3 = frame.BackgroundColor3,
		BackgroundTransparency = frame.BackgroundTransparency,
		BorderSizePixel = 0,
		Size = UDim2.fromScale(1, 1),
		ZIndex = 0,
		Parent = frame,
	})
	local drop = make("Frame", {
		Name = "Drop", BackgroundColor3 = color, BorderSizePixel = 0, Position = UDim2.fromOffset(offset.X, offset.Y),
		Size = UDim2.fromScale(1, 1), ZIndex = -1, Parent = frame,
	})
	local corner = frame:FindFirstChildOfClass("UICorner")
	if corner then
		corner:Clone().Parent = face
		corner:Clone().Parent = drop
	end
	local gradient = frame:FindFirstChildOfClass("UIGradient")
	if gradient then
		gradient.Parent = face
	end
	frame.BackgroundTransparency = 1
end

function Decor.glow(frame: GuiObject, color: Color3, blur: number?)
	Decor.shadow(frame, color, Vector2.zero, blur or 14, 0.5)
end

-- Frosted glass behind translucent panels
function Decor.glass(frame: GuiObject)
	if Decor.USE_UIBLUR then
		make("UIBlur", { Name = "Glass", Parent = frame })
	end
end

-- Cut-corner shape (Cyber Holo, Battlegrounds menus). UICorner only rounds and ClipsDescendants ignores shapes,
-- so the fill is rebuilt from 3 strips + 4 corner triangles and the rim is a closed Path2D through the cut points.
function Decor.chamfer(frame: GuiObject, cut: number, rim: Color3?, rimThickness: number?): Frame
	local color, transparency = frame.BackgroundColor3, frame.BackgroundTransparency
	frame.BackgroundTransparency = 1
	stripShapeOf(frame)
	local shape = make("Frame", { Name = "Shape", BackgroundTransparency = 1, Size = UDim2.fromScale(1, 1), ZIndex = 0, Parent = frame })
	local function strip(name: string, position: UDim2, size: UDim2)
		make("Frame", {
			Name = name, BackgroundColor3 = color, BackgroundTransparency = transparency, BorderSizePixel = 0,
			Position = position, Size = size, ZIndex = 0, Parent = shape,
		})
	end
	strip("Middle", UDim2.fromOffset(cut, 0), UDim2.new(1, -2 * cut, 1, 0))
	strip("Left", UDim2.fromOffset(0, cut), UDim2.new(0, cut, 1, -2 * cut))
	strip("Right", UDim2.new(1, -cut, 0, cut), UDim2.new(0, cut, 1, -2 * cut))
	local square = UDim2.fromOffset(cut, cut)
	Decor.triangle(shape, "TL", color, transparency, 45, { Size = square, ZIndex = 0 })
	Decor.triangle(shape, "TR", color, transparency, 135, { Size = square, Position = UDim2.new(1, -cut, 0, 0), ZIndex = 0 })
	Decor.triangle(shape, "BR", color, transparency, 225, { Size = square, Position = UDim2.new(1, -cut, 1, -cut), ZIndex = 0 })
	Decor.triangle(shape, "BL", color, transparency, -45, { Size = square, Position = UDim2.new(0, 0, 1, -cut), ZIndex = 0 })
	if rim and rimThickness and rimThickness > 0 then
		local path = make("Path2D", { Name = "Rim", Closed = true, Color3 = rim, Thickness = rimThickness, ZIndex = 6, Parent = frame })
		path:SetAttribute("BaseThickness", rimThickness)
		path:SetControlPoints({
			Path2DControlPoint.new(UDim2.fromOffset(cut, 0)),
			Path2DControlPoint.new(UDim2.new(1, -cut, 0, 0)),
			Path2DControlPoint.new(UDim2.new(1, 0, 0, cut)),
			Path2DControlPoint.new(UDim2.new(1, 0, 1, -cut)),
			Path2DControlPoint.new(UDim2.new(1, -cut, 1, 0)),
			Path2DControlPoint.new(UDim2.new(0, cut, 1, 0)),
			Path2DControlPoint.new(UDim2.new(0, 0, 1, -cut)),
			Path2DControlPoint.new(UDim2.fromOffset(0, cut)),
		})
	end
	return shape
end

-- 45° parallelogram (Kinetic Comic buttons, ultimate banners): the root's flat fill is the middle and two
-- square triangle caps hang off its ends. Flat colours only: a cap can't also carry a colour gradient.
function Decor.slant(frame: GuiObject)
	stripShapeOf(frame)
	local function cap(name: string, anchorX: number, positionX: number, rotation: number)
		local c = Decor.triangle(frame, name, frame.BackgroundColor3, frame.BackgroundTransparency, rotation, {
			Size = UDim2.fromScale(1, 1), AnchorPoint = Vector2.new(anchorX, 0), Position = UDim2.fromScale(positionX, 0), ZIndex = 0,
		})
		Util.aspect(c, 1).DominantAxis = Enum.DominantAxis.Height
	end
	cap("CapL", 1, 0, 45)
	cap("CapR", 0, 1, 225)
end

-- Comic starburst: overlapping squares rotated evenly make a 4n-point star
function Decor.burst(parent: GuiObject, color: Color3, spikes: number, scale: number): Frame
	local holder = make("Frame", {
		Name = "Burst", BackgroundTransparency = 1, AnchorPoint = Vector2.new(0.5, 0.5), Position = UDim2.fromScale(0.5, 0.5),
		Size = UDim2.fromScale(scale, scale), ZIndex = 0, Parent = parent,
	})
	Util.aspect(holder, 1)
	local squares = math.max(2, math.floor(spikes / 4))
	for i = 1, squares do
		make("Frame", {
			Name = "Spike", BackgroundColor3 = color, BorderSizePixel = 0, AnchorPoint = Vector2.new(0.5, 0.5),
			Position = UDim2.fromScale(0.5, 0.5), Size = UDim2.fromScale(0.7, 0.7), Rotation = (90 / squares) * (i - 1),
			ZIndex = 0, Parent = holder,
		})
	end
	return holder
end

-- Each ray sits in its own centred "Arm": GuiObjects rotate around their own centre, not their anchor, so
-- rotating the arm swings the ray around the middle
local function radial(parent: GuiObject, name: string, scale: number, count: number, ray: (arm: Frame, i: number) -> ()): Frame
	local holder = make("Frame", {
		Name = name, BackgroundTransparency = 1, AnchorPoint = Vector2.new(0.5, 0.5), Position = UDim2.fromScale(0.5, 0.5),
		Size = UDim2.fromScale(scale, scale), ZIndex = 0, Parent = parent,
	})
	Util.aspect(holder, 1)
	for i = 1, count do
		local arm = make("Frame", {
			Name = "Arm", BackgroundTransparency = 1, Size = UDim2.fromScale(1, 1), Rotation = (360 / count) * (i - 1),
			ZIndex = 0, Parent = holder,
		})
		ray(arm, i)
	end
	return holder
end

function Decor.rays(parent: GuiObject, color: Color3, count: number, transparency: number, scale: number?): Frame
	return radial(parent, "Rays", scale or 1, count, function(arm, _)
		local ray = make("Frame", {
			Name = "Ray", BackgroundColor3 = color, BackgroundTransparency = transparency, BorderSizePixel = 0,
			AnchorPoint = Vector2.new(0.5, 1), Position = UDim2.fromScale(0.5, 0.5), Size = UDim2.fromScale(0.06, 0.5),
			ZIndex = 0, Parent = arm,
		})
		make("UIGradient", { Rotation = 90, Transparency = NumberSequence.new(1, 0), Parent = ray })
	end)
end

-- Manga speed lines: thin rays with an empty centre, slightly uneven
function Decor.speedlines(parent: GuiObject, color: Color3, count: number, scale: number?): Frame
	return radial(parent, "Speedlines", scale or 2.2, count, function(arm, i)
		arm.Rotation += (i % 3) * 2.5
		local line = make("Frame", {
			Name = "Line", BackgroundColor3 = color, BorderSizePixel = 0, AnchorPoint = Vector2.new(0.5, 1),
			Position = UDim2.fromScale(0.5, 0.32), Size = UDim2.fromScale(0.003 + (i % 3) * 0.002, 0.32),
			ZIndex = 0, Parent = arm,
		})
		make("UIGradient", { Rotation = 90, Transparency = NumberSequence.new(0, 1), Parent = line })
	end)
end

function Decor.scanlines(parent: GuiObject, color: Color3, transparency: number, spacingPx: number, maxLines: number): Frame
	local holder = make("Frame", {
		Name = "Scanlines", BackgroundTransparency = 1, ClipsDescendants = true, Size = UDim2.fromScale(1, 1), ZIndex = 8, Parent = parent,
	})
	make("UIListLayout", { Padding = UDim.new(0, math.max(0, spacingPx - 1)), SortOrder = Enum.SortOrder.LayoutOrder, Parent = holder })
	for i = 1, maxLines do
		make("Frame", {
			Name = "Line", BackgroundColor3 = color, BackgroundTransparency = transparency, BorderSizePixel = 0,
			Size = UDim2.new(1, 0, 0, 1), LayoutOrder = i, Parent = holder,
		})
	end
	return holder
end

-- HUD corner brackets, drawn outsetPx outside the frame
function Decor.brackets(parent: GuiObject, color: Color3, lengthPx: number, thickness: number, outsetPx: number)
	for _, corner in CORNERS do
		local position = UDim2.new(
			corner.X, if corner.X == 0 then -outsetPx else outsetPx,
			corner.Y, if corner.Y == 0 then -outsetPx else outsetPx
		)
		make("Frame", {
			Name = "BracketH", BackgroundColor3 = color, BorderSizePixel = 0, AnchorPoint = corner, Position = position,
			Size = UDim2.fromOffset(lengthPx, thickness), ZIndex = 7, Parent = parent,
		})
		make("Frame", {
			Name = "BracketV", BackgroundColor3 = color, BorderSizePixel = 0, AnchorPoint = corner, Position = position,
			Size = UDim2.fromOffset(thickness, lengthPx), ZIndex = 7, Parent = parent,
		})
	end
end

-- A second outline nudged off-register, like a hand-inked panel
function Decor.ink(frame: GuiObject, color: Color3, thickness: number, offsetPx: number)
	local ghost = make("Frame", {
		Name = "InkGhost", BackgroundTransparency = 1, Position = UDim2.fromOffset(offsetPx, -offsetPx / 2),
		Size = UDim2.new(1, -offsetPx / 2, 1, offsetPx / 2), ZIndex = 7, Parent = frame,
	})
	Util.stroke(ghost, color, thickness)
end

-- Thin inner frame plus diamond gems on the corners (Dark Fantasy)
function Decor.ornate(frame: GuiObject, color: Color3, insetPx: number, gemPx: number)
	local inner = make("Frame", {
		Name = "InnerFrame", BackgroundTransparency = 1, AnchorPoint = Vector2.new(0.5, 0.5), Position = UDim2.fromScale(0.5, 0.5),
		Size = UDim2.new(1, -2 * insetPx, 1, -2 * insetPx), ZIndex = 7, Parent = frame,
	})
	Util.stroke(inner, color, 1, 0.45)
	for _, corner in CORNERS do
		local gem = make("Frame", {
			Name = "Gem", BackgroundColor3 = color, BorderSizePixel = 0, AnchorPoint = Vector2.new(0.5, 0.5),
			Position = UDim2.fromScale(corner.X, corner.Y), Size = UDim2.fromOffset(gemPx, gemPx), Rotation = 45, ZIndex = 8, Parent = frame,
		})
		Util.stroke(gem, BLACK, 1)
	end
end

-- Fading line with a diamond in the middle
function Decor.divider(parent: GuiObject, color: Color3, props: { [string]: any }?): Frame
	local p = props or {}
	local line = make("Frame", {
		Name = "Divider", BackgroundColor3 = color, BorderSizePixel = 0, AnchorPoint = Vector2.new(0.5, 0.5),
		Position = p.Position or UDim2.fromScale(0.5, 1.12), Size = p.Size or UDim2.new(0.9, 0, 0, 1), ZIndex = 7, Parent = parent,
	})
	make("UIGradient", {
		Transparency = NumberSequence.new({ NumberSequenceKeypoint.new(0, 1), NumberSequenceKeypoint.new(0.5, 0), NumberSequenceKeypoint.new(1, 1) }),
		Parent = line,
	})
	make("Frame", {
		Name = "Gem", BackgroundColor3 = color, BorderSizePixel = 0, AnchorPoint = Vector2.new(0.5, 0.5),
		Position = UDim2.fromScale(0.5, 0.5), Size = UDim2.fromOffset(7, 7), Rotation = 45, ZIndex = 8, Parent = line,
	})
	return line
end

-- Darkens the top and bottom of a full-screen background
function Decor.vignette(parent: GuiObject, color: Color3, strength: number)
	for _, rotation in { 90, -90 } do
		local atBottom = rotation == 90
		local band = make("Frame", {
			Name = "Vignette", BackgroundColor3 = color, BorderSizePixel = 0, AnchorPoint = Vector2.new(0, if atBottom then 1 else 0),
			Position = UDim2.fromScale(0, if atBottom then 1 else 0), Size = UDim2.fromScale(1, 0.45), ZIndex = 0, Parent = parent,
		})
		make("UIGradient", { Rotation = rotation, Transparency = NumberSequence.new(1, 1 - strength), Parent = band })
	end
end

-- Scattered glowing specks; positions come from the index so every build looks the same
function Decor.embers(parent: GuiObject, color: Color3, count: number)
	for i = 1, count do
		local size = 2 + (i % 3) * 2
		local ember = make("Frame", {
			Name = "Ember", BackgroundColor3 = color, BackgroundTransparency = 0.2 + (i % 4) * 0.15, BorderSizePixel = 0,
			Position = UDim2.fromScale(((i * 37) % 100) / 100, ((i * 61) % 100) / 100), Size = UDim2.fromOffset(size, size),
			ZIndex = 1, Parent = parent,
		})
		Util.corner(ember, UDim.new(1, 0))
	end
end

-- A long rotated band (Battlegrounds / comic backgrounds)
function Decor.slash(parent: GuiObject, color: Color3, rotation: number, props: { [string]: any }?): Frame
	local p = props or {}
	return make("Frame", {
		Name = "Slash", BackgroundColor3 = color, BackgroundTransparency = p.Transparency or 0, BorderSizePixel = 0,
		AnchorPoint = Vector2.new(0.5, 0.5), Position = p.Position or UDim2.fromScale(0.5, 0.5),
		Size = p.Size or UDim2.fromScale(1.6, 0.08), Rotation = rotation, ZIndex = 0, Parent = parent,
	})
end

-- Ruler ticks under a header (Cyber Holo)
function Decor.ticks(parent: GuiObject, color: Color3, count: number)
	local holder = make("Frame", {
		Name = "Ruler", BackgroundTransparency = 1, AnchorPoint = Vector2.new(0, 1), Position = UDim2.new(0, 0, 1, 5),
		Size = UDim2.new(1, 0, 0, 4), ZIndex = 7, Parent = parent,
	})
	for i = 0, count do
		make("Frame", {
			Name = "Tick", BackgroundColor3 = color, BorderSizePixel = 0, Position = UDim2.fromScale(i / count, 0),
			Size = UDim2.new(0, 1, if i % 4 == 0 then 1 else 0.5, 0), ZIndex = 7, Parent = holder,
		})
	end
end

return Decor
```

- [ ] **Step 3: Write `roblox-ui/kit/UIKit.luau`**

```lua
--!strict
-- UIKit: themed Roblox UI builders. Every builder is UIKit.<Component>(theme, props) and returns plain
-- instances, so it works at edit time (bake into StarterGui through MCP) and at runtime.

local UIKit: { [string]: any } = {}

UIKit.Util = require(script.Util)
UIKit.Decor = require(script.Decor)

-- Component modules contribute their exported functions. A module that isn't installed yet adds nothing, so
-- KitCheck reports the missing builders instead of crashing.
for _, part in { "Containers", "Controls", "Readouts", "Feedback", "Screens" } do
	local module = script:FindFirstChild(part)
	if module and module:IsA("ModuleScript") then
		for key, value in require(module) :: any do
			UIKit[key] = value
		end
	end
end

function UIKit.theme(name: string): any
	local themes = script:FindFirstChild("Themes")
	local module = themes and themes:FindFirstChild(name)
	assert(module and module:IsA("ModuleScript"), "UIKit: no theme named " .. name)
	return require(module) :: any
end

function UIKit.themeNames(): { string }
	local names = {}
	local themes = script:FindFirstChild("Themes")
	if themes then
		for _, module in themes:GetChildren() do
			if module:IsA("ModuleScript") then
				table.insert(names, module.Name)
			end
		end
	end
	table.sort(names)
	return names
end

return UIKit
```

- [ ] **Step 4: Install**

`multi_edit` in this order (className `ModuleScript` each): `game.ReplicatedStorage.UIKit` ← `UIKit.luau`, `game.ReplicatedStorage.UIKit.Util` ← `Util.luau`, `game.ReplicatedStorage.UIKit.Decor` ← `Decor.luau`. Then create the Themes folder with the folder snippet: `folder(game:GetService("ReplicatedStorage").UIKit, "Themes")`.

- [ ] **Step 5: Run KitCheck**

Expected:

```
KitCheck: 4 passed, 1 failed
- theme StudSimulator exists: no theme module named StudSimulator
```

If `Util.abbreviate` fails, fix `abbreviate` until the 10 cases pass before moving on.

- [ ] **Step 6: Commit**

```bash
git add roblox-ui/kit/UIKit.luau roblox-ui/kit/Util.luau roblox-ui/kit/Decor.luau
git commit -m "feat: add UIKit core helpers and decorators"
```

### Task 4: Stud Simulator theme, Controls and Containers

**Files:**
- Create: `roblox-ui/kit/Themes/StudSimulator.luau`, `roblox-ui/kit/Controls.luau`, `roblox-ui/kit/Containers.luau`
- Install: `game.ReplicatedStorage.UIKit.Themes.StudSimulator`, `game.ReplicatedStorage.UIKit.Controls`, `game.ReplicatedStorage.UIKit.Containers`

**Interfaces:**
- Consumes: `Util.*`, `Decor.*` from Task 3.
- Produces: `Controls.Button / IconButton / Toggle / Slider / TextInput / setVariant`, `Containers.Screen / Panel / List / Grid / Tabs / Card` with the signatures pinned in Task 2. The theme table shape every later theme copies:
  - `decorate.panel(main, theme)`, `decorate.header(tab, theme)`, `decorate.button(button, theme, variant)` where `variant` is a variant name or `"icon"` for IconButtons, `decorate.slot(slot, theme)` for slots, cards and toasts, `decorate.bar(bar, theme)`, `decorate.screen(background, theme, kind)` with `kind` = `"loading"` or `"menu"`.
  - `IconButton` also accepts `Round = true` (circular mobile buttons).

- [ ] **Step 1: Write the theme `roblox-ui/kit/Themes/StudSimulator.luau`**

```lua
--!strict
-- Stud Simulator: candy gradients, chunky dark outlines, studs and gloss. Matches "+1 Lift a Rock for CUH".

local Decor = require(script.Parent.Parent.Decor)

local hex = Color3.fromHex
local INK = hex("14101F")
local WHITE = Color3.new(1, 1, 1)

local function variant(stops: { string }, textStroke: string)
	local fill = {}
	for _, h in stops do
		table.insert(fill, hex(h))
	end
	return { fill = fill, fillTransparency = 0, text = WHITE, edge = hex("120A1C"), textStroke = hex(textStroke) }
end

local function stops(...: string): { Color3 }
	local list = {}
	for _, h in { ... } do
		table.insert(list, hex(h))
	end
	return list
end

return {
	name = "StudSimulator",
	hudLayout = "simulator",
	color = {
		backdrop = hex("1F222C"),
		base = hex("2B1D45"),
		baseTransparency = 0,
		surface = hex("5A4C26"),
		surfaceTransparency = 0,
		rim = hex("E8B818"),
		barEdge = INK,
		text = WHITE,
		textMuted = hex("E6E2C8"),
		textStroke = INK,
		track = hex("2A2433"),
		header = stops("FF7AA8", "FF3D7F", "D61B5A"),
		variants = {
			primary = variant({ "D58CFF", "9B3BFF", "6A12D6" }, "4A0E8F"),
			secondary = variant({ "7FD8FF", "2FA8FF", "1466D6" }, "0B2F66"),
			success = variant({ "9CFF3A", "5CE01E", "33CC14" }, "0B4A0E"),
			danger = variant({ "FF5A78", "FF2E4A", "D6123A" }, "4A0A14"),
			ghost = { fill = { INK }, fillTransparency = 0.45, text = WHITE, edge = INK, textStroke = INK },
		},
		bars = {
			health = stops("FF8A96", "FF2E4A", "C8102E"),
			energy = stops("7FD8FF", "2FA8FF", "1466D6"),
			xp = stops("FFD23A", "FFA61A", "FF7A00"),
			accent = stops("D8FF6A", "5CE01E", "2EB81E"),
		},
	},
	font = {
		display = Font.fromEnum(Enum.Font.FredokaOne),
		body = Font.fromEnum(Enum.Font.FredokaOne),
		number = Font.fromEnum(Enum.Font.FredokaOne),
	},
	textStroke = { display = 3.5, body = 2.5 },
	stroke = { panel = 5, control = 4, slot = 3 },
	radius = { panel = UDim.new(0.045, 0), control = UDim.new(0.3, 0), slot = UDim.new(0, 10), pill = UDim.new(0.5, 0) },
	shape = {
		chamfer = 0, slantButtons = false, tilt = 0, header = "tab", iconFrame = false, gradientText = true, barStyle = "single",
	},
	motion = {
		style = "pop", easing = Enum.EasingStyle.Back, fast = 0.15, normal = 0.2, slow = 0.4,
		pressScale = 0.9, openFrom = 0.85, worldBlur = 14,
	},
	assets = {},
	decorate = {
		panel = function(main: Frame, theme: any)
			Decor.studs(main, theme, 0.82, 44, theme.radius.panel)
		end,
		header = function(tab: Frame, theme: any)
			Decor.studs(tab, theme, 0.65, 35, theme.radius.control)
			Decor.gloss(tab, 0.3, theme.radius.control)
		end,
		button = function(button: GuiObject, theme: any, variantName: string)
			if variantName ~= "ghost" and variantName ~= "icon" then
				Decor.gloss(button, 0.35, theme.radius.control)
			end
		end,
		slot = function(slot: GuiObject, theme: any)
			Decor.studs(slot, theme, 0.86, 40, theme.radius.slot)
			Decor.gloss(slot, 0.12, theme.radius.slot)
		end,
		bar = function(bar: Frame, theme: any)
			local fill = bar:FindFirstChild("Fill")
			if fill and fill:IsA("GuiObject") then
				Decor.gloss(fill, 0.3, theme.radius.control)
			end
		end,
		screen = function(background: Frame, theme: any, _kind: string)
			Decor.studs(background, theme, 0.9, 64, nil)
			Decor.rays(background, theme.color.rim, 16, 0.86, 1.6)
		end,
	},
}
```

- [ ] **Step 2: Add the theme to KitCheck's expectations**

It is already listed (`EXPECTED_THEMES = { "StudSimulator" }`). Install the theme only after Steps 3–4 so the component cases have something to call.

- [ ] **Step 3: Write `roblox-ui/kit/Controls.luau`**

```lua
--!strict
-- Interactive controls. Each returns plain instances tagged UIKit.<Kind>; Motion gives them behaviour at runtime.

local Util = require(script.Parent.Util)
local Decor = require(script.Parent.Decor)
local make = Util.make

local Controls = {}

local WHITE = Color3.new(1, 1, 1)

function Controls.Button(theme: any, props: { [string]: any }): TextButton
	local variantName = props.Variant or "primary"
	local v = theme.color.variants[variantName]
	local slant = theme.shape.slantButtons
	local button = make("TextButton", {
		Name = "Button",
		Text = "",
		AutoButtonColor = false,
		-- gradient buttons keep a white base because UIGradient multiplies; slanted ones need the flat colour
		BackgroundColor3 = if slant then v.fill[1] else WHITE,
		BackgroundTransparency = v.fillTransparency,
		BorderSizePixel = 0,
		ZIndex = props.ZIndex or 3,
	})
	Util.place(button, props, UDim2.fromScale(0.3, 0.12))
	button:SetAttribute("Variant", variantName)
	if slant then
		Decor.slant(button)
	else
		Util.gradient(button, v.fill, 90)
		Util.corner(button, theme.radius.control)
		Util.stroke(button, v.edge, theme.stroke.control)
	end
	local labelZ = (props.ZIndex or 3) + 2
	if props.Icon then
		Util.icon(theme, props.Icon, {
			Name = "Icon", Size = UDim2.fromScale(0.7, 0.7), Position = UDim2.fromScale(0.06, 0.15), ZIndex = labelZ, Parent = button,
		})
	end
	Util.text(theme, {
		Name = "Label",
		Text = props.Text,
		Role = "display",
		Color = v.text,
		StrokeColor = v.textStroke,
		Size = if props.Icon then UDim2.fromScale(0.62, 0.72) else UDim2.fromScale(0.86, 0.72),
		Position = if props.Icon then UDim2.fromScale(0.62, 0.5) else UDim2.fromScale(0.5, 0.5),
		AnchorPoint = Vector2.new(0.5, 0.5),
		ZIndex = labelZ,
		Parent = button,
	})
	theme.decorate.button(button, theme, variantName)
	Util.tag(button, "Button", theme)
	button.Parent = props.Parent
	return button
end

-- Re-colours a built button for another variant (selected tabs, toggled states)
function Controls.setVariant(theme: any, button: GuiObject, variantName: string)
	local v = theme.color.variants[variantName]
	button:SetAttribute("Variant", variantName)
	local face = button:FindFirstChild("Face")
	local holder: GuiObject = if face and face:IsA("GuiObject") then face else button
	local gradient = holder:FindFirstChildOfClass("UIGradient")
	if gradient then
		gradient.Color = Util.sequence(v.fill)
	else
		holder.BackgroundColor3 = v.fill[1]
	end
	holder.BackgroundTransparency = v.fillTransparency
	for _, name in { "CapL", "CapR" } do
		local cap = button:FindFirstChild(name)
		if cap and cap:IsA("Frame") then
			cap.BackgroundColor3 = v.fill[1]
			cap.BackgroundTransparency = v.fillTransparency
		end
	end
	local edge = button:FindFirstChild("Edge")
	if edge and edge:IsA("UIStroke") then
		edge.Color = v.edge
	end
	local label = button:FindFirstChild("Label")
	if label and label:IsA("TextLabel") then
		label.TextColor3 = v.text
		local stroke = label:FindFirstChild("TextStroke")
		if stroke and stroke:IsA("UIStroke") then
			stroke.Color = v.textStroke
		end
	end
end

-- Big icon with an optional caption and notification badge (HUD menu buttons, mobile action buttons)
function Controls.IconButton(theme: any, props: { [string]: any }): TextButton
	local framed = theme.shape.iconFrame or props.Round == true
	local button = make("TextButton", {
		Name = "IconButton",
		Text = "",
		AutoButtonColor = false,
		BackgroundColor3 = theme.color.surface,
		BackgroundTransparency = if framed then theme.color.surfaceTransparency else 1,
		BorderSizePixel = 0,
		ZIndex = 3,
	})
	Util.place(button, props, UDim2.fromScale(0.08, 0.14))
	Util.aspect(button, 1)
	if framed then
		Util.corner(button, if props.Round then UDim.new(1, 0) else theme.radius.slot)
		Util.stroke(button, theme.color.rim, theme.stroke.slot)
	end
	local iconScale = if framed then 0.62 else 0.9
	Util.icon(theme, props.Icon, {
		Name = "Icon",
		Size = UDim2.fromScale(iconScale, iconScale),
		Position = UDim2.fromScale(0.5, if props.Caption and framed then 0.42 else 0.45),
		AnchorPoint = Vector2.new(0.5, 0.5),
		ZIndex = 4,
		Parent = button,
	})
	if props.Caption then
		Util.text(theme, {
			Name = "Caption",
			Text = props.Caption,
			Role = "display",
			Size = if framed then UDim2.fromScale(0.92, 0.26) else UDim2.fromScale(1.2, 0.38),
			Position = UDim2.fromScale(0.5, if framed then 0.86 else 0.84),
			AnchorPoint = Vector2.new(0.5, 0.5),
			ZIndex = 6,
			Parent = button,
		})
	end
	if props.Badge then
		local badge = make("Frame", {
			Name = "Badge",
			AnchorPoint = Vector2.new(0.5, 0.5),
			Position = UDim2.fromScale(0.86, 0.08),
			Size = UDim2.fromScale(0.55, 0.26),
			BackgroundColor3 = theme.color.variants.danger.fill[1],
			BorderSizePixel = 0,
			ZIndex = 7,
			Parent = button,
		})
		Util.corner(badge, theme.radius.pill)
		Util.stroke(badge, theme.color.textStroke, math.max(1, theme.stroke.slot - 1))
		Util.text(theme, {
			Name = "Label", Text = props.Badge, Role = "display", Size = UDim2.fromScale(0.9, 0.86),
			Position = UDim2.fromScale(0.5, 0.5), AnchorPoint = Vector2.new(0.5, 0.5), ZIndex = 8, Parent = badge,
		})
	end
	theme.decorate.button(button, theme, "icon")
	Util.tag(button, "Button", theme)
	button.Parent = props.Parent
	return button
end

function Controls.Toggle(theme: any, props: { [string]: any }): TextButton
	local on = props.On == true
	local root = make("TextButton", {
		Name = "Toggle", Text = "", AutoButtonColor = false, BackgroundColor3 = theme.color.track, BorderSizePixel = 0, ZIndex = 3,
	})
	Util.place(root, props, UDim2.fromScale(0.16, 0.6))
	Util.aspect(root, 2.1)
	Util.corner(root, theme.radius.pill)
	Util.stroke(root, theme.color.barEdge, theme.stroke.slot)
	local fill = make("Frame", {
		Name = "Fill", BackgroundColor3 = WHITE, BackgroundTransparency = if on then 0 else 1, BorderSizePixel = 0,
		Size = UDim2.fromScale(1, 1), ZIndex = 3, Parent = root,
	})
	Util.corner(fill, theme.radius.pill)
	Util.gradient(fill, theme.color.variants.success.fill, 90)
	local knob = make("Frame", {
		Name = "Knob", AnchorPoint = Vector2.new(0.5, 0.5), Position = UDim2.fromScale(if on then 0.73 else 0.27, 0.5),
		Size = UDim2.fromScale(0.8, 0.8), BackgroundColor3 = theme.color.text, BorderSizePixel = 0, ZIndex = 4, Parent = root,
	})
	Util.aspect(knob, 1)
	Util.corner(knob, theme.radius.pill)
	Util.stroke(knob, theme.color.barEdge, math.max(1, theme.stroke.slot - 1))
	root:SetAttribute("On", on)
	Util.tag(root, "Toggle", theme)
	root.Parent = props.Parent
	return root
end

function Controls.Slider(theme: any, props: { [string]: any }): Frame
	local value = math.clamp(props.Value or 0.5, 0, 1)
	local root = make("Frame", { Name = "Slider", BackgroundTransparency = 1, ZIndex = 3 })
	Util.place(root, props, UDim2.fromScale(0.4, 0.5))
	local track = make("Frame", {
		Name = "Track", AnchorPoint = Vector2.new(0, 0.5), Position = UDim2.fromScale(0, 0.5), Size = UDim2.fromScale(1, 0.34),
		BackgroundColor3 = theme.color.track, BorderSizePixel = 0, ZIndex = 3, Parent = root,
	})
	Util.corner(track, theme.radius.pill)
	Util.stroke(track, theme.color.barEdge, theme.stroke.slot)
	local fill = make("Frame", {
		Name = "Fill", Size = UDim2.fromScale(value, 1), BackgroundColor3 = WHITE, BorderSizePixel = 0, ZIndex = 3, Parent = track,
	})
	Util.corner(fill, theme.radius.pill)
	Util.gradient(fill, theme.color.variants.primary.fill, 90)
	local knob = make("TextButton", {
		Name = "Knob", Text = "", AutoButtonColor = false, AnchorPoint = Vector2.new(0.5, 0.5), Position = UDim2.fromScale(value, 0.5),
		Size = UDim2.fromScale(1, 0.95), BackgroundColor3 = theme.color.text, BorderSizePixel = 0, ZIndex = 5, Parent = root,
	})
	Util.aspect(knob, 1).DominantAxis = Enum.DominantAxis.Height
	Util.corner(knob, theme.radius.pill)
	Util.stroke(knob, theme.color.barEdge, theme.stroke.slot)
	root:SetAttribute("Value", value)
	Util.tag(root, "Slider", theme)
	root.Parent = props.Parent
	return root
end

function Controls.TextInput(theme: any, props: { [string]: any }): Frame
	local root = make("Frame", { Name = "TextInput", BackgroundColor3 = theme.color.track, BorderSizePixel = 0, ZIndex = 3 })
	Util.place(root, props, UDim2.fromScale(0.5, 0.1))
	Util.corner(root, theme.radius.control)
	Util.stroke(root, theme.color.barEdge, theme.stroke.slot)
	local box = make("TextBox", {
		Name = "Box", Text = "", PlaceholderText = props.Placeholder or "", PlaceholderColor3 = theme.color.textMuted,
		TextColor3 = theme.color.text, FontFace = theme.font.body, TextScaled = true, ClearTextOnFocus = false,
		TextXAlignment = Enum.TextXAlignment.Left, BackgroundTransparency = 1, Size = UDim2.fromScale(0.92, 0.7),
		Position = UDim2.fromScale(0.5, 0.5), AnchorPoint = Vector2.new(0.5, 0.5), ZIndex = 4, Parent = root,
	})
	make("UITextSizeConstraint", { MaxTextSize = 40, MinTextSize = 6, Parent = box })
	Util.tag(root, "TextInput", theme)
	root.Parent = props.Parent
	return root
end

return Controls
```

- [ ] **Step 4: Write `roblox-ui/kit/Containers.luau`**

```lua
--!strict
-- Screens, panels and the scrolling bodies inside them. Contract names (Main, TitleTab, Close, List, Grid, Body,
-- Template) come from Lift a Rock so runtime code can find things without references.

local Util = require(script.Parent.Util)
local Decor = require(script.Parent.Decor)
local Controls = require(script.Parent.Controls)
local make = Util.make

local Containers = {}

-- Where the title sits for each theme header style, and where the body starts below it
local HEADER = {
	tab = { position = UDim2.fromScale(0.04, -0.1), size = UDim2.fromScale(0.38, 0.13), bodyTop = 0.08 },
	strip = { position = UDim2.fromScale(0.03, 0.03), size = UDim2.fromScale(0.55, 0.1), bodyTop = 0.16 },
	center = { position = UDim2.fromScale(0.2, 0.025), size = UDim2.fromScale(0.6, 0.11), bodyTop = 0.18 },
}

function Containers.Screen(theme: any, props: { [string]: any }): ScreenGui
	local fullScreen = props.FullScreen == true
	local gui = make("ScreenGui", {
		Name = props.Name,
		ResetOnSpawn = false,
		ZIndexBehavior = Enum.ZIndexBehavior.Sibling,
		IgnoreGuiInset = fullScreen,
		ScreenInsets = if fullScreen then Enum.ScreenInsets.None else Enum.ScreenInsets.CoreUISafeInsets,
		DisplayOrder = props.DisplayOrder or 0,
		Enabled = props.Enabled ~= false,
	})
	gui:SetAttribute("UIKitTheme", theme.name)
	gui:SetAttribute("UIKitBuilt", true)
	gui:SetAttribute("UIKitRole", props.Role or "Screen")
	return gui
end

local function scroller(theme: any, name: string, props: { [string]: any }): ScrollingFrame
	local frame = make("ScrollingFrame", {
		Name = name,
		BackgroundTransparency = 1,
		BorderSizePixel = 0,
		CanvasSize = UDim2.new(),
		AutomaticCanvasSize = Enum.AutomaticSize.Y,
		ScrollingDirection = Enum.ScrollingDirection.Y,
		ScrollBarThickness = 6,
		ScrollBarImageColor3 = theme.color.rim,
		ZIndex = 3,
	})
	Util.place(frame, props, UDim2.fromScale(1, 1))
	make("UIPadding", {
		PaddingTop = UDim.new(0, 6), PaddingBottom = UDim.new(0, 6), PaddingLeft = UDim.new(0, 6), PaddingRight = UDim.new(0, 12),
		Parent = frame,
	})
	return frame
end

function Containers.List(theme: any, props: { [string]: any }): ScrollingFrame
	local list = scroller(theme, props.Name or "List", props)
	make("UIListLayout", {
		Padding = UDim.new(0, props.Gap or 8), HorizontalAlignment = Enum.HorizontalAlignment.Center,
		SortOrder = Enum.SortOrder.LayoutOrder, Parent = list,
	})
	Util.tag(list, "List", theme)
	list.Parent = props.Parent
	return list
end

function Containers.Grid(theme: any, props: { [string]: any }): ScrollingFrame
	local grid = scroller(theme, props.Name or "Grid", props)
	local columns = props.Columns or 4
	local gap = props.Gap or 0.025
	local cellWidth = (1 - gap * (columns - 1)) / columns - 0.003
	local layout = make("UIGridLayout", {
		-- placeholder sizes; Util.pixelGrid swaps in pixel cells once the grid is on screen
		CellSize = UDim2.new(cellWidth, 0, 0, 80),
		CellPadding = UDim2.fromScale(gap, 0),
		SortOrder = Enum.SortOrder.LayoutOrder,
		HorizontalAlignment = Enum.HorizontalAlignment.Center,
		Parent = grid,
	})
	layout:SetAttribute("DesignCell", UDim2.fromScale(cellWidth, 0))
	layout:SetAttribute("DesignGap", UDim2.fromScale(gap, gap))
	layout:SetAttribute("CellAspect", props.CellAspect or 1)
	Util.tag(grid, "Grid", theme)
	grid.Parent = props.Parent
	return grid
end

function Containers.Panel(theme: any, props: { [string]: any }): (Frame, GuiObject)
	local body = props.Body or "list"
	local headerStyle = theme.shape.header
	local header = HEADER[headerStyle]
	local main = make("Frame", {
		Name = props.Name or "Main",
		AnchorPoint = props.AnchorPoint or Vector2.new(0.5, 0.5),
		Position = props.Position or UDim2.fromScale(0.5, 0.53),
		Size = props.Size or UDim2.fromScale(0.85, 0.66),
		BackgroundColor3 = theme.color.base,
		BackgroundTransparency = theme.color.baseTransparency,
		BorderSizePixel = 0,
		-- a rotated ancestor switches off ClipsDescendants, so only non-scrolling panels tilt (Tilt = false opts out
		-- when a "none" body will hold a scrolling list)
		Rotation = if body == "none" and props.Tilt ~= false then theme.shape.tilt else 0,
		ZIndex = 1,
	})
	Util.aspect(main, props.AspectRatio or 1.45)
	if theme.shape.chamfer > 0 then
		Decor.chamfer(main, theme.shape.chamfer, theme.color.rim, theme.stroke.panel)
	else
		Util.corner(main, theme.radius.panel)
		Util.stroke(main, theme.color.rim, theme.stroke.panel)
	end

	local tab = make("Frame", {
		Name = "TitleTab", BackgroundColor3 = Color3.new(1, 1, 1), BorderSizePixel = 0,
		Position = header.position, Size = header.size, ZIndex = 5, Parent = main,
	})
	Util.gradient(tab, theme.color.header, 90)
	Util.corner(tab, theme.radius.control)
	Util.stroke(tab, theme.color.textStroke, theme.stroke.control)
	local hasIcon = props.Icon ~= nil and headerStyle == "tab"
	if hasIcon then
		-- oversized icon breaking out of the tab, like Lift a Rock's panel headers
		Util.icon(theme, props.Icon, {
			Name = "Icon", Size = UDim2.fromScale(0.42, 1.9), Position = UDim2.fromScale(0.1, 0.42),
			AnchorPoint = Vector2.new(0.5, 0.5), ZIndex = 8, Parent = tab,
		})
	end
	Util.text(theme, {
		Name = "Title",
		Text = props.Title,
		Role = "display",
		XAlign = if headerStyle == "center" then Enum.TextXAlignment.Center else Enum.TextXAlignment.Left,
		Size = if hasIcon then UDim2.fromScale(0.64, 0.84) else UDim2.fromScale(0.9, 0.84),
		Position = if hasIcon then UDim2.fromScale(0.3, 0.08) else UDim2.fromScale(0.05, 0.08),
		ZIndex = 7,
		Parent = tab,
	})
	theme.decorate.header(tab, theme)

	local overhang = headerStyle == "tab"
	local close = Controls.Button(theme, {
		Name = "Close",
		Text = "X",
		Variant = "danger",
		Size = UDim2.fromScale(0.08, 0.12),
		Position = if overhang then UDim2.fromScale(0.985, 0.015) else UDim2.fromScale(0.975, 0.03),
		AnchorPoint = if overhang then Vector2.new(0.5, 0.5) else Vector2.new(1, 0),
		ZIndex = 6,
		Parent = main,
	})
	Util.aspect(close, 1)
	close:AddTag("UIKit.Close")

	local bodyPosition = UDim2.fromScale(0.03, header.bodyTop)
	local bodySize = UDim2.fromScale(0.94, 0.96 - header.bodyTop)
	local content: GuiObject
	if body == "grid" then
		content = Containers.Grid(theme, {
			Columns = props.Columns, CellAspect = props.CellAspect, Position = bodyPosition, Size = bodySize, Parent = main,
		})
	elseif body == "none" then
		content = make("Frame", {
			Name = "Body", BackgroundTransparency = 1, Position = bodyPosition, Size = bodySize, ZIndex = 3, Parent = main,
		})
	else
		content = Containers.List(theme, { Position = bodyPosition, Size = bodySize, Parent = main })
	end

	theme.decorate.panel(main, theme)
	Util.tag(main, "Panel", theme)
	main.Parent = props.Parent
	return main, content
end

function Containers.Tabs(theme: any, props: { [string]: any }): Frame
	local bar = make("Frame", { Name = "Tabs", BackgroundTransparency = 1, ZIndex = 3 })
	Util.place(bar, props, UDim2.fromScale(1, 0.12))
	make("UIListLayout", {
		FillDirection = Enum.FillDirection.Horizontal, Padding = UDim.new(0.015, 0), SortOrder = Enum.SortOrder.LayoutOrder,
		VerticalAlignment = Enum.VerticalAlignment.Center, Parent = bar,
	})
	local selected = props.Selected or props.Tabs[1]
	local width = 1 / #props.Tabs - 0.015
	for i, id in props.Tabs do
		Controls.Button(theme, {
			Name = id, Text = id, Variant = if id == selected then "primary" else "secondary",
			Size = UDim2.fromScale(width, 1), LayoutOrder = i, Parent = bar,
		})
	end
	bar:SetAttribute("Selected", selected)
	Util.tag(bar, "Tabs", theme)
	bar.Parent = props.Parent
	return bar
end

-- A list row: icon, title, subtitle and an action button (shop items, quests, settings rows)
function Containers.Card(theme: any, props: { [string]: any }): Frame
	local card = make("Frame", {
		Name = "Card",
		BackgroundColor3 = theme.color.surface,
		BackgroundTransparency = theme.color.surfaceTransparency,
		BorderSizePixel = 0,
		ZIndex = 3,
	})
	-- rows are pixel-tall like Lift a Rock's: Scale heights inside an auto-sizing list feed back into the canvas
	Util.place(card, props, UDim2.new(1, 0, 0, props.Height or 84))
	Util.corner(card, theme.radius.slot)
	Util.stroke(card, theme.color.rim, theme.stroke.slot)
	local textLeft = 0.04
	if props.Icon then
		Util.icon(theme, props.Icon, {
			Name = "Icon", Size = UDim2.fromScale(0.8, 0.8), Position = UDim2.fromScale(0.015, 0.1), ZIndex = 5, Parent = card,
		})
		textLeft = 0.2
	end
	Util.text(theme, {
		Name = "Title", Text = props.Title, Role = "display", XAlign = Enum.TextXAlignment.Left,
		Size = UDim2.fromScale(0.5, 0.42), Position = UDim2.fromScale(textLeft, 0.08), ZIndex = 5, Parent = card,
	})
	Util.text(theme, {
		Name = "Subtitle", Text = props.Subtitle or "", Color = theme.color.textMuted, XAlign = Enum.TextXAlignment.Left,
		Size = UDim2.fromScale(0.5, 0.34), Position = UDim2.fromScale(textLeft, 0.54), ZIndex = 5, Parent = card,
	})
	if props.Action then
		Controls.Button(theme, {
			Name = "Action", Text = props.Action, Variant = props.ActionVariant or "success",
			Size = UDim2.fromScale(0.25, 0.62), Position = UDim2.fromScale(0.735, 0.19), ZIndex = 4, Parent = card,
		})
	end
	theme.decorate.slot(card, theme)
	Util.tag(card, "Card", theme)
	card.Parent = props.Parent
	return card
end

return Containers
```

- [ ] **Step 5: Install and run KitCheck**

`multi_edit` (ModuleScript): `game.ReplicatedStorage.UIKit.Controls` ← `Controls.luau`, `game.ReplicatedStorage.UIKit.Containers` ← `Containers.luau`, `game.ReplicatedStorage.UIKit.Themes.StudSimulator` ← `Themes/StudSimulator.luau`. Run KitCheck.

Expected: `KitCheck: 22 passed, 14 failed`, and every one of the 14 failures is a `StudSimulator` Readouts/Feedback/Screens case (`Bar(single|split|segmented)`, `Currency`, `Badge`, `Slot`, `Hotbar`, `Tooltip`, `ToastStack`, `Popup`, `Splash`, `DamageNumber`, `LoadingScreen`, `MainMenu`) failing with "attempt to call a nil value". Any other failure is a bug in this task: fix it before moving on.

- [ ] **Step 6: Look at it next to the reference**

`execute_luau` (Edit) on the UI/UX studio:

```lua
local RS = game:GetService("ReplicatedStorage")
local UIKit = require(RS.UIKit:Clone())
local theme = UIKit.theme("StudSimulator")
local old = game.StarterGui:FindFirstChild("_Preview")
if old then old:Destroy() end
local gui = UIKit.Screen(theme, { Name = "_Preview" })
local main, list = UIKit.Panel(theme, { Title = "Featured", Icon = "🛒", Body = "list", Size = UDim2.fromScale(0.6, 0.66), Parent = gui })
for i, item in { { "2X Strength", "Double all strength gains", "R$ 199", "💪" }, { "VIP", "Exclusive chat tag", "R$ 399", "👑" }, { "Lucky Pack", "+50% luck for 30 min", "R$ 49", "🍀" } } do
	UIKit.Card(theme, { Name = "Item" .. i, Title = item[1], Subtitle = item[2], Action = item[3], Icon = item[4], LayoutOrder = i, Parent = list })
end
gui.Parent = game.StarterGui
UIKit.Util.scaleStrokes(gui, workspace.CurrentCamera.ViewportSize.Y)
return "preview built"
```

`screen_capture` (capture_id `Task4_StudPanel`). Compare with the Lift a Rock "Featured" screenshot taken during research (purple 9-slice body with gold rim, pink title tab with an oversized icon, red X overhanging the top-right corner, olive rows with gold strokes, green price pills). Fix anything that reads clearly different: wrong z-order, clipped icon, text without its dark outline, missing gloss. Then remove the preview: `game.StarterGui._Preview:Destroy()`.

- [ ] **Step 7: Commit**

```bash
git add roblox-ui/kit/Controls.luau roblox-ui/kit/Containers.luau roblox-ui/kit/Themes/StudSimulator.luau
git commit -m "feat: add Stud Simulator theme, controls and containers"
```

### Task 5: Readouts — bars, currency, badges, slots, hotbar, tooltip

**Files:**
- Create: `roblox-ui/kit/Readouts.luau`
- Install: `game.ReplicatedStorage.UIKit.Readouts`

**Interfaces:**
- Consumes: `Util.*`, `Decor.slant`, theme tokens.
- Produces: `Readouts.Bar / Currency / Badge / Slot / Hotbar / Tooltip` (signatures pinned in Task 2). Contract names later tasks rely on: `Bar.Fill` (single/segmented), `Bar.Left.Fill` + `Bar.Right.Fill` + `Bar.Emblem` (split), `Bar.Label`, `Bar.Value`, `Bar.Ticks`; `Currency.Amount`; `Slot.Key`, `Slot.Title`, `Slot.Value`, `Slot.Icon`, `Slot.Cooldown`; hotbar slots named `Slot1…SlotN` unless given names.

- [ ] **Step 1: Confirm the failing cases**

Run KitCheck. Expected: `KitCheck: 22 passed, 14 failed`. This task turns 8 of those green: `Bar(single)`, `Bar(split)`, `Bar(segmented)`, `Currency`, `Badge`, `Slot`, `Hotbar`, `Tooltip`.

- [ ] **Step 2: Write `roblox-ui/kit/Readouts.luau`**

```lua
--!strict
-- Read-only HUD pieces. Game code changes values through the contract names (Fill, Amount, Cooldown) or with
-- Motion.setBar / Motion.countTo / Motion.cooldown.

local Util = require(script.Parent.Util)
local Decor = require(script.Parent.Decor)
local make = Util.make

local Readouts = {}

local WHITE = Color3.new(1, 1, 1)
local BLACK = Color3.new(0, 0, 0)

local function makeFill(theme: any, parent: Instance, kind: string, value: number, fromRight: boolean): Frame
	local fill = make("Frame", {
		Name = "Fill",
		BackgroundColor3 = WHITE,
		BorderSizePixel = 0,
		-- the left half of a split bar drains toward the emblem in the middle
		AnchorPoint = Vector2.new(if fromRight then 1 else 0, 0),
		Position = UDim2.fromScale(if fromRight then 1 else 0, 0),
		Size = UDim2.fromScale(math.clamp(value, 0, 1), 1),
		ZIndex = 2,
		Parent = parent,
	})
	Util.corner(fill, theme.radius.control)
	Util.gradient(fill, theme.color.bars[kind], 90)
	return fill
end

local function makeTicks(theme: any, parent: Instance, segments: number)
	local holder = make("Frame", { Name = "Ticks", BackgroundTransparency = 1, Size = UDim2.fromScale(1, 1), ZIndex = 4, Parent = parent })
	for i = 1, segments - 1 do
		make("Frame", {
			Name = "Tick", BackgroundColor3 = theme.color.barEdge, BackgroundTransparency = 0.3, BorderSizePixel = 0,
			AnchorPoint = Vector2.new(0.5, 0), Position = UDim2.fromScale(i / segments, 0), Size = UDim2.new(0, 2, 1, 0),
			ZIndex = 4, Parent = holder,
		})
	end
end

function Readouts.Bar(theme: any, props: { [string]: any }): Frame
	local style = props.Style or theme.shape.barStyle
	local kind = props.Kind or "health"
	local bar = make("Frame", { Name = "Bar", BackgroundColor3 = theme.color.track, BorderSizePixel = 0, ZIndex = 2 })
	Util.place(bar, props, UDim2.fromScale(0.4, 0.05))
	Util.corner(bar, theme.radius.control)
	Util.stroke(bar, theme.color.barEdge, theme.stroke.control)
	if style == "split" then
		local gap = 0.05
		local left = make("Frame", {
			Name = "Left", BackgroundTransparency = 1, Size = UDim2.fromScale(0.5 - gap / 2, 1), ZIndex = 2, Parent = bar,
		})
		makeFill(theme, left, kind, props.Value or 1, true)
		local right = make("Frame", {
			Name = "Right", BackgroundTransparency = 1, Position = UDim2.fromScale(0.5 + gap / 2, 0),
			Size = UDim2.fromScale(0.5 - gap / 2, 1), ZIndex = 2, Parent = bar,
		})
		makeFill(theme, right, props.RightKind or "energy", props.RightValue or props.Value or 1, false)
		if props.Segments then
			makeTicks(theme, left, math.max(2, math.floor(props.Segments / 2)))
			makeTicks(theme, right, math.max(2, math.floor(props.Segments / 2)))
		end
		local emblem = make("Frame", {
			Name = "Emblem", AnchorPoint = Vector2.new(0.5, 0.5), Position = UDim2.fromScale(0.5, 0.5),
			Size = UDim2.fromScale(1, 1.9), Rotation = 45, BackgroundColor3 = theme.color.base, BorderSizePixel = 0,
			ZIndex = 5, Parent = bar,
		})
		Util.aspect(emblem, 1).DominantAxis = Enum.DominantAxis.Height
		Util.stroke(emblem, theme.color.rim, math.max(1.5, theme.stroke.control))
		if props.Emblem then
			-- the glyph sits on the bar, not inside the rotated diamond, so it stays upright
			Util.icon(theme, props.Emblem, {
				Name = "Glyph", Size = UDim2.fromScale(1, 1.3), Position = UDim2.fromScale(0.5, 0.5),
				AnchorPoint = Vector2.new(0.5, 0.5), ZIndex = 6, Parent = bar,
			})
		end
	else
		makeFill(theme, bar, kind, props.Value or 1, false)
		if style == "segmented" then
			makeTicks(theme, bar, props.Segments or 10)
		end
	end
	if props.Icon then
		Util.icon(theme, props.Icon, {
			Name = "Icon", Size = UDim2.fromScale(1, 1.75), Position = UDim2.fromScale(0, 0.45),
			AnchorPoint = Vector2.new(0.5, 0.5), ZIndex = 7, Parent = bar,
		})
	end
	if props.Label then
		Util.text(theme, {
			Name = "Label", Text = props.Label, Role = "display", XAlign = Enum.TextXAlignment.Left,
			Size = UDim2.fromScale(0.46, 0.84), Position = UDim2.fromScale(if props.Icon then 0.08 else 0.03, 0.08), ZIndex = 6, Parent = bar,
		})
	end
	if props.ValueText then
		Util.text(theme, {
			Name = "Value", Text = props.ValueText, Role = "number", XAlign = Enum.TextXAlignment.Right,
			Size = UDim2.fromScale(0.4, 0.8), Position = UDim2.fromScale(0.57, 0.1), ZIndex = 6, Parent = bar,
		})
	end
	theme.decorate.bar(bar, theme)
	Util.tag(bar, "Bar", theme)
	bar.Parent = props.Parent
	return bar
end

-- Icon + amount pill (cash, gems, tokens). Amount is the contract name game code writes to.
function Readouts.Currency(theme: any, props: { [string]: any }): Frame
	local kind = props.Kind or "accent"
	local root = make("Frame", {
		Name = "Currency", BackgroundColor3 = theme.color.base, BackgroundTransparency = math.max(theme.color.baseTransparency, 0.25),
		BorderSizePixel = 0, ZIndex = 2,
	})
	Util.place(root, props, UDim2.fromScale(0.18, 0.07))
	Util.aspect(root, 3.6)
	Util.corner(root, theme.radius.pill)
	Util.stroke(root, theme.color.barEdge, theme.stroke.slot)
	Util.icon(theme, props.Icon, {
		Name = "Icon", Size = UDim2.fromScale(1, 1.35), Position = UDim2.fromScale(0.02, 0.5),
		AnchorPoint = Vector2.new(0.2, 0.5), ZIndex = 5, Parent = root,
	})
	local amount = Util.text(theme, {
		Name = "Amount", Text = props.Amount, Role = "number", XAlign = Enum.TextXAlignment.Left,
		Size = UDim2.fromScale(0.66, 0.8), Position = UDim2.fromScale(0.3, 0.1), ZIndex = 5, Parent = root,
	})
	if theme.shape.gradientText then
		local stops = theme.color.bars[kind]
		Util.gradient(amount, stops, 90)
		local stroke = amount:FindFirstChild("TextStroke")
		if stroke and stroke:IsA("UIStroke") then
			stroke.Color = Util.shade(stops[#stops], -0.65)
		end
	end
	Util.tag(root, "Currency", theme)
	root.Parent = props.Parent
	return root
end

-- Small label: "NEW!", "-50%", "Permanent!", or a slanted ultimate banner (Slant = true)
function Readouts.Badge(theme: any, props: { [string]: any }): Frame
	local stops = theme.color.bars[props.Kind or "accent"]
	local slant = props.Slant == true
	local badge = make("Frame", {
		Name = "Badge", BackgroundColor3 = if slant then stops[1] else WHITE, BorderSizePixel = 0,
		Rotation = props.Rotation or 0, ZIndex = 4,
	})
	Util.place(badge, props, UDim2.fromScale(0.12, 0.05))
	if slant then
		Decor.slant(badge)
	else
		Util.gradient(badge, stops, 90)
		Util.corner(badge, theme.radius.pill)
		Util.stroke(badge, theme.color.textStroke, math.max(1, theme.stroke.slot - 1))
	end
	Util.text(theme, {
		Name = "Label", Text = props.Text, Role = "display", Size = UDim2.fromScale(0.9, 0.82),
		Position = UDim2.fromScale(0.5, 0.5), AnchorPoint = Vector2.new(0.5, 0.5), ZIndex = 6, Parent = badge,
	})
	Util.tag(badge, "Badge", theme)
	badge.Parent = props.Parent
	return badge
end

-- Square cell: hotbar slot, move tile ("1 / Lapse Blue"), inventory item. Cooldown is a dark overlay whose
-- height is the remaining fraction.
function Readouts.Slot(theme: any, props: { [string]: any }): TextButton
	local slot = make("TextButton", {
		Name = "Slot", Text = "", AutoButtonColor = false, BackgroundColor3 = theme.color.surface,
		BackgroundTransparency = theme.color.surfaceTransparency, BorderSizePixel = 0, ZIndex = 3,
	})
	Util.place(slot, props, UDim2.fromScale(0.1, 1))
	Util.aspect(slot, 1)
	Util.corner(slot, theme.radius.slot)
	Util.stroke(slot, if props.Selected then theme.color.rim else theme.color.barEdge, theme.stroke.slot)
	if props.Icon then
		Util.icon(theme, props.Icon, {
			Name = "Icon", Size = UDim2.fromScale(0.6, 0.6), Position = UDim2.fromScale(0.5, if props.Title or props.Value then 0.42 else 0.5),
			AnchorPoint = Vector2.new(0.5, 0.5), ZIndex = 4, Parent = slot,
		})
	end
	if props.Key then
		Util.text(theme, {
			Name = "Key", Text = props.Key, Role = "number", XAlign = Enum.TextXAlignment.Left,
			Size = UDim2.fromScale(0.36, 0.3), Position = UDim2.fromScale(0.07, 0.04), ZIndex = 7, Parent = slot,
		})
	end
	if props.Title then
		Util.text(theme, {
			Name = "Title", Text = props.Title, Role = "body",
			Size = if props.Icon then UDim2.fromScale(0.94, 0.22) else UDim2.fromScale(0.88, 0.46),
			Position = if props.Icon then UDim2.fromScale(0.03, 0.75) else UDim2.fromScale(0.06, 0.32),
			ZIndex = 7, Parent = slot,
		})
	end
	if props.Value then
		Util.text(theme, {
			Name = "Value", Text = props.Value, Role = "number", Color = theme.color.bars.accent[1],
			Size = UDim2.fromScale(0.9, 0.22), Position = UDim2.fromScale(0.05, 0.74), ZIndex = 7, Parent = slot,
		})
	end
	local cooldown = make("Frame", {
		Name = "Cooldown", AnchorPoint = Vector2.new(0, 1), Position = UDim2.fromScale(0, 1),
		Size = UDim2.fromScale(1, math.clamp(props.Cooldown or 0, 0, 1)), BackgroundColor3 = BLACK,
		BackgroundTransparency = 0.4, BorderSizePixel = 0, ZIndex = 6, Parent = slot,
	})
	Util.corner(cooldown, theme.radius.slot)
	slot:SetAttribute("Selected", props.Selected == true)
	theme.decorate.slot(slot, theme)
	Util.tag(slot, "Slot", theme)
	slot.Parent = props.Parent
	return slot
end

function Readouts.Hotbar(theme: any, props: { [string]: any }): Frame
	local bar = make("Frame", { Name = "Hotbar", BackgroundTransparency = 1, ZIndex = 3 })
	Util.place(bar, props, UDim2.fromScale(0.5, 0.12))
	if not props.AnchorPoint then
		bar.AnchorPoint = Vector2.new(0.5, 1)
	end
	if not props.Position then
		bar.Position = UDim2.fromScale(0.5, 0.98)
	end
	make("UIListLayout", {
		FillDirection = Enum.FillDirection.Horizontal, HorizontalAlignment = Enum.HorizontalAlignment.Center,
		VerticalAlignment = Enum.VerticalAlignment.Center, Padding = UDim.new(0, 6), SortOrder = Enum.SortOrder.LayoutOrder, Parent = bar,
	})
	for i, slotProps in props.Slots do
		local p = table.clone(slotProps)
		p.Name = p.Name or ("Slot" .. i)
		p.LayoutOrder = i
		p.Size = UDim2.fromScale(1, 1)
		p.Parent = bar
		Readouts.Slot(theme, p)
	end
	Util.tag(bar, "Hotbar", theme)
	bar.Parent = props.Parent
	return bar
end

function Readouts.Tooltip(theme: any, props: { [string]: any }): Frame
	local tip = make("Frame", {
		Name = "Tooltip", BackgroundColor3 = theme.color.base, BackgroundTransparency = math.max(theme.color.baseTransparency, 0.08),
		BorderSizePixel = 0, ZIndex = 20,
	})
	Util.place(tip, props, UDim2.fromScale(0.2, 0.06))
	Util.corner(tip, theme.radius.control)
	Util.stroke(tip, theme.color.rim, theme.stroke.slot)
	Util.text(theme, {
		Name = "Label", Text = props.Text, Size = UDim2.fromScale(0.92, 0.8), Position = UDim2.fromScale(0.5, 0.5),
		AnchorPoint = Vector2.new(0.5, 0.5), ZIndex = 21, Parent = tip,
	})
	Util.tag(tip, "Tooltip", theme)
	tip.Parent = props.Parent
	return tip
end

return Readouts
```

- [ ] **Step 3: Install and run KitCheck**

`multi_edit` `game.ReplicatedStorage.UIKit.Readouts` (ModuleScript). Run KitCheck.
Expected: `KitCheck: 30 passed, 6 failed`; the 6 are `ToastStack`, `Popup`, `Splash`, `DamageNumber`, `LoadingScreen`, `MainMenu`.

- [ ] **Step 4: Commit**

```bash
git add roblox-ui/kit/Readouts.luau
git commit -m "feat: add bars, currency, badges, slots and hotbar"
```

### Task 6: Feedback and full screens

**Files:**
- Create: `roblox-ui/kit/Feedback.luau`, `roblox-ui/kit/Screens.luau`
- Install: `game.ReplicatedStorage.UIKit.Feedback`, `game.ReplicatedStorage.UIKit.Screens`

**Interfaces:**
- Consumes: `Containers.Screen / Panel`, `Controls.Button`, `Readouts.Bar`, `Decor.rays`.
- Produces: `Feedback.ToastStack / Toast / Popup / Splash / DamageNumber`, `Screens.LoadingScreen / MainMenu`. Contract names: toast stack `Toasts` with hidden `Template` (a Toast whose `Stripe` gradient and `Label` text Motion rewrites); popup `Popup > Main > Body > {Reward, Message, Actions > {Cancel, Confirm}}`; splash `Splash > {Rays, Text}`; loading `Loading > Background > {Title, Progress(Bar with Fill + Value), Tip, Skip}`; menu `MainMenu > Background > {Title, Subtitle, Buttons > <one Button per label>, Version}`.

- [ ] **Step 1: Write `roblox-ui/kit/Feedback.luau`**

```lua
--!strict
-- Moments: toasts, reward popups, level-up splashes and damage numbers. Motion animates them; these builders
-- only make the pieces.

local Util = require(script.Parent.Util)
local Decor = require(script.Parent.Decor)
local Containers = require(script.Parent.Containers)
local Controls = require(script.Parent.Controls)
local make = Util.make

local Feedback = {}

local WHITE = Color3.new(1, 1, 1)
local BLACK = Color3.new(0, 0, 0)

function Feedback.Toast(theme: any, props: { [string]: any }): Frame
	local kind = props.Kind or "accent"
	local toast = make("Frame", {
		Name = "Toast", BackgroundColor3 = theme.color.base, BackgroundTransparency = math.max(theme.color.baseTransparency, 0.1),
		BorderSizePixel = 0, ZIndex = 10,
	})
	-- pixel height: a Scale height inside the stack's list would follow the stack, not the text
	Util.place(toast, props, UDim2.new(1, 0, 0, 44))
	Util.corner(toast, theme.radius.control)
	Util.stroke(toast, theme.color.barEdge, theme.stroke.slot)
	local stripe = make("Frame", {
		Name = "Stripe", BackgroundColor3 = WHITE, BorderSizePixel = 0, Size = UDim2.new(0, 6, 1, 0), ZIndex = 11, Parent = toast,
	})
	Util.corner(stripe, theme.radius.control)
	Util.gradient(stripe, theme.color.bars[kind], 90)
	Util.text(theme, {
		Name = "Label", Text = props.Text, Role = "display", XAlign = Enum.TextXAlignment.Left,
		Size = UDim2.fromScale(0.88, 0.7), Position = UDim2.fromScale(0.07, 0.15), ZIndex = 12, Parent = toast,
	})
	toast:SetAttribute("Kind", kind)
	theme.decorate.slot(toast, theme)
	Util.tag(toast, "Toast", theme)
	toast.Parent = props.Parent
	return toast
end

function Feedback.ToastStack(theme: any, props: { [string]: any }): Frame
	local stack = make("Frame", { Name = "Toasts", BackgroundTransparency = 1, ZIndex = 10 })
	Util.place(stack, props, UDim2.fromScale(0.26, 0.5))
	if not props.Position then
		stack.AnchorPoint = Vector2.new(1, 0)
		stack.Position = UDim2.fromScale(0.99, 0.12)
	end
	make("UIListLayout", {
		Padding = UDim.new(0, 6), SortOrder = Enum.SortOrder.LayoutOrder,
		HorizontalAlignment = Enum.HorizontalAlignment.Right, Parent = stack,
	})
	Feedback.Toast(theme, { Name = "Template", Text = "Template", Visible = false, Parent = stack })
	Util.tag(stack, "ToastStack", theme)
	stack.Parent = props.Parent
	return stack
end

-- Modal: dims the screen and shows a small panel with an optional rewarded item, a message and buttons
function Feedback.Popup(theme: any, props: { [string]: any }): Frame
	local dim = make("Frame", {
		Name = props.Name or "Popup", BackgroundColor3 = BLACK, BackgroundTransparency = 0.45, BorderSizePixel = 0,
		Size = UDim2.fromScale(1, 1), ZIndex = 20,
	})
	local _, body = Containers.Panel(theme, {
		Title = props.Title, Body = "none", AspectRatio = 1.15, Size = UDim2.fromScale(0.5, 0.56),
		Position = UDim2.fromScale(0.5, 0.52), Parent = dim,
	})
	if props.Icon then
		local reward = make("Frame", {
			Name = "Reward", BackgroundTransparency = 1, AnchorPoint = Vector2.new(0.5, 0), Position = UDim2.fromScale(0.5, 0.02),
			Size = UDim2.fromScale(0.5, 0.5), ZIndex = 3, Parent = body,
		})
		Util.aspect(reward, 1)
		Decor.rays(reward, theme.color.bars.xp[1], 14, 0.55, 1.5)
		Util.icon(theme, props.Icon, {
			Name = "Icon", Size = UDim2.fromScale(0.8, 0.8), Position = UDim2.fromScale(0.5, 0.5),
			AnchorPoint = Vector2.new(0.5, 0.5), ZIndex = 5, Parent = reward,
		})
	end
	if props.Body then
		Util.text(theme, {
			Name = "Message", Text = props.Body, Role = "display", Size = UDim2.fromScale(0.9, 0.16),
			Position = UDim2.fromScale(0.5, if props.Icon then 0.58 else 0.3), AnchorPoint = Vector2.new(0.5, 0),
			ZIndex = 5, Parent = body,
		})
	end
	local actions = make("Frame", {
		Name = "Actions", BackgroundTransparency = 1, AnchorPoint = Vector2.new(0.5, 1), Position = UDim2.fromScale(0.5, 0.98),
		Size = UDim2.fromScale(0.9, 0.18), ZIndex = 4, Parent = body,
	})
	make("UIListLayout", {
		FillDirection = Enum.FillDirection.Horizontal, HorizontalAlignment = Enum.HorizontalAlignment.Center,
		VerticalAlignment = Enum.VerticalAlignment.Center, Padding = UDim.new(0.04, 0), SortOrder = Enum.SortOrder.LayoutOrder,
		Parent = actions,
	})
	if props.Cancel then
		Controls.Button(theme, {
			Name = "Cancel", Text = props.Cancel, Variant = "secondary", Size = UDim2.fromScale(0.42, 1), LayoutOrder = 1, Parent = actions,
		})
	end
	if props.Confirm then
		Controls.Button(theme, {
			Name = "Confirm", Text = props.Confirm, Variant = "success", Size = UDim2.fromScale(0.42, 1), LayoutOrder = 2, Parent = actions,
		})
	end
	Util.tag(dim, "Popup", theme)
	dim.Parent = props.Parent
	return dim
end

-- "LEVEL UP!" / "X2 LUCK" banner with rays behind it
function Feedback.Splash(theme: any, props: { [string]: any }): Frame
	local stops = theme.color.bars[props.Kind or "xp"]
	local splash = make("Frame", { Name = "Splash", BackgroundTransparency = 1, ZIndex = 15 })
	Util.place(splash, props, UDim2.fromScale(0.6, 0.2))
	if not props.Position then
		splash.AnchorPoint = Vector2.new(0.5, 0.5)
		splash.Position = UDim2.fromScale(0.5, 0.2)
	end
	Util.aspect(splash, 3)
	Decor.rays(splash, stops[1], 18, 0.5, 1.3)
	local text = Util.text(theme, {
		Name = "Text", Text = props.Text, Role = "display", Stroke = math.max(theme.textStroke.display, 3),
		Size = UDim2.fromScale(1, 0.8), Position = UDim2.fromScale(0.5, 0.5), AnchorPoint = Vector2.new(0.5, 0.5),
		MaxTextSize = 120, ZIndex = 16, Parent = splash,
	})
	Util.gradient(text, stops, 90)
	Util.tag(splash, "Splash", theme)
	splash.Parent = props.Parent
	return splash
end

-- Always outlined, whatever the theme's text stroke: it floats over the 3D world
function Feedback.DamageNumber(theme: any, props: { [string]: any }): TextLabel
	local crit = props.Crit == true
	local label = Util.text(theme, {
		Name = props.Name or "Damage",
		Text = props.Amount .. (if crit then "!" else ""),
		Role = "number",
		Color = if crit then theme.color.bars.accent[1] else theme.color.text,
		Stroke = math.max(theme.textStroke.display, 2.5),
		Size = if crit then UDim2.fromScale(0.16, 0.1) else UDim2.fromScale(0.11, 0.07),
		Position = props.Position or UDim2.fromScale(0.5, 0.5),
		AnchorPoint = Vector2.new(0.5, 0.5),
		Rotation = if crit then -8 else 0,
		MaxTextSize = 96,
		ZIndex = 25,
		Parent = props.Parent,
	})
	Util.tag(label, "DamageNumber", theme)
	return label
end

return Feedback
```

- [ ] **Step 2: Write `roblox-ui/kit/Screens.luau`**

```lua
--!strict
-- Full-screen screens. Both cover the top bar (FullScreen) and get the theme's background art from
-- decorate.screen(background, theme, "loading" | "menu").

local Util = require(script.Parent.Util)
local Containers = require(script.Parent.Containers)
local Controls = require(script.Parent.Controls)
local Readouts = require(script.Parent.Readouts)
local make = Util.make

local Screens = {}

local function background(theme: any, gui: ScreenGui, transparency: number): Frame
	return make("Frame", {
		Name = "Background", BackgroundColor3 = theme.color.backdrop, BackgroundTransparency = transparency,
		BorderSizePixel = 0, Size = UDim2.fromScale(1, 1), ZIndex = 1, Parent = gui,
	})
end

local function bigTitle(theme: any, parent: Instance, text: string, props: { [string]: any }): TextLabel
	local title = Util.text(theme, {
		Name = "Title", Text = text, Role = "display", Stroke = math.max(theme.textStroke.display, 2),
		XAlign = props.XAlign, Size = props.Size, Position = props.Position, AnchorPoint = props.AnchorPoint,
		MaxTextSize = 160, ZIndex = 6, Parent = parent,
	})
	if theme.shape.gradientText then
		Util.gradient(title, theme.color.bars.xp, 90)
	end
	return title
end

function Screens.LoadingScreen(theme: any, props: { [string]: any }): ScreenGui
	local gui = Containers.Screen(theme, { Name = props.Name or "Loading", FullScreen = true, DisplayOrder = 50, Role = "Loading" })
	local bg = background(theme, gui, 0)
	theme.decorate.screen(bg, theme, "loading")
	bigTitle(theme, bg, props.Title, {
		Size = UDim2.fromScale(0.72, 0.22), Position = UDim2.fromScale(0.5, 0.38), AnchorPoint = Vector2.new(0.5, 0.5),
	})
	local progress = math.clamp(props.Progress or 0.35, 0, 1)
	Readouts.Bar(theme, {
		Name = "Progress", Style = "single", Kind = "xp", Value = progress,
		ValueText = string.format("%d%%", math.floor(progress * 100)),
		Size = UDim2.fromScale(0.44, 0.05), Position = UDim2.fromScale(0.5, 0.7), AnchorPoint = Vector2.new(0.5, 0.5), Parent = bg,
	})
	if props.Tip then
		Util.text(theme, {
			Name = "Tip", Text = props.Tip, Color = theme.color.textMuted, Size = UDim2.fromScale(0.6, 0.045),
			Position = UDim2.fromScale(0.5, 0.79), AnchorPoint = Vector2.new(0.5, 0.5), ZIndex = 6, Parent = bg,
		})
	end
	Controls.Button(theme, {
		Name = "Skip", Text = "Skip", Variant = "ghost", Size = UDim2.fromScale(0.1, 0.06),
		Position = UDim2.fromScale(0.97, 0.95), AnchorPoint = Vector2.new(1, 1), Parent = bg,
	})
	return gui
end

function Screens.MainMenu(theme: any, props: { [string]: any }): ScreenGui
	local gui = Containers.Screen(theme, { Name = props.Name or "MainMenu", FullScreen = true, DisplayOrder = 40, Role = "MainMenu" })
	-- partly see-through so the game world shows behind the menu
	local bg = background(theme, gui, 0.25)
	theme.decorate.screen(bg, theme, "menu")
	bigTitle(theme, bg, props.Title, {
		XAlign = Enum.TextXAlignment.Left, Size = UDim2.fromScale(0.5, 0.2), Position = UDim2.fromScale(0.06, 0.12),
	})
	if props.Subtitle then
		Util.text(theme, {
			Name = "Subtitle", Text = props.Subtitle, Color = theme.color.textMuted, XAlign = Enum.TextXAlignment.Left,
			Size = UDim2.fromScale(0.45, 0.05), Position = UDim2.fromScale(0.065, 0.33), ZIndex = 6, Parent = bg,
		})
	end
	local buttons = make("Frame", {
		Name = "Buttons", BackgroundTransparency = 1, Position = UDim2.fromScale(0.06, 0.42), Size = UDim2.fromScale(0.28, 0.5),
		ZIndex = 5, Parent = bg,
	})
	make("UIListLayout", { Padding = UDim.new(0.04, 0), SortOrder = Enum.SortOrder.LayoutOrder, Parent = buttons })
	for i, label in props.Buttons or { "PLAY", "SETTINGS" } do
		Controls.Button(theme, {
			Name = label, Text = label, Variant = if i == 1 then "primary" else "secondary",
			Size = UDim2.fromScale(if i == 1 then 1 else 0.82, if i == 1 then 0.26 else 0.17), LayoutOrder = i, Parent = buttons,
		})
	end
	Util.text(theme, {
		Name = "Version", Text = props.Version or "v1.0", Color = theme.color.textMuted, XAlign = Enum.TextXAlignment.Left,
		Size = UDim2.fromScale(0.2, 0.03), Position = UDim2.fromScale(0.015, 0.96), ZIndex = 6, Parent = bg,
	})
	return gui
end

return Screens
```

- [ ] **Step 3: Install and run KitCheck**

`multi_edit` `game.ReplicatedStorage.UIKit.Feedback` and `game.ReplicatedStorage.UIKit.Screens` (ModuleScripts). Run KitCheck.
Expected: `KitCheck: 36 passed, 0 failed`.

- [ ] **Step 4: Commit**

```bash
git add roblox-ui/kit/Feedback.luau roblox-ui/kit/Screens.luau
git commit -m "feat: add feedback pieces, loading screen and main menu"
```

### Task 7: Motion runtime

**Files:**
- Create: `roblox-ui/kit/dev/MotionCheck.luau`, `roblox-ui/kit/Motion.luau`, `roblox-ui/kit/UIRuntime.client.luau`
- Install: `game.ReplicatedStorage.UIKitDev.MotionCheck` (ModuleScript, dev only: clients can't see ServerStorage), `game.ReplicatedStorage.UIKit.Motion` (ModuleScript), `game.StarterPlayer.StarterPlayerScripts.UIRuntime` (LocalScript)

**Interfaces:**
- Consumes: every builder, `UIKit.setVariant`, `Util.pixelGrid / scaleStrokes / strokeFactor / abbreviate`.
- Produces (used by Task 14's showcase runtime and documented in `components.md`):
  - `Motion.start()` — binds every kit element in PlayerGui now and as it appears. Safe to call twice.
  - `Motion.open(gui: ScreenGui)`, `Motion.close(gui)`, `Motion.toggle(gui)`, `Motion.isOpen(gui): boolean`
  - `Motion.enter(gui: GuiObject)`, `Motion.press(button)`, `Motion.hover(button, on)`
  - `Motion.setToggle(toggle, on)`, `Motion.setSlider(slider, value)`, `Motion.selectTab(tabs, id)`
  - `Motion.toast(stack, text, kind?, seconds?): GuiObject?`, `Motion.countTo(label, from, to, seconds?, format?)`, `Motion.damage(layer, at: UDim2, amount, crit?): TextLabel`, `Motion.splash(splash, seconds?)`, `Motion.setBar(bar, fraction, side?)`, `Motion.cooldown(slot, seconds)`, `Motion.loading(gui, seconds, onDone?)`
  - Zero-code wiring: a kit button with attribute `Opens = "<ScreenGui name>"` toggles that panel; a button tagged `UIKit.Close` closes its ScreenGui; a button inside `UIKit.Tabs` selects itself; anything tagged `UIKit.HideWithPanel` hides while a panel is open.

- [ ] **Step 1: Write the play-mode test `roblox-ui/kit/dev/MotionCheck.luau`**

```lua
--!strict
-- Play-mode checks for Motion. Run with execute_luau on the Client datamodel during a playtest:
--   return require(game.ReplicatedStorage.UIKitDev.MotionCheck).run()

local Players = game:GetService("Players")
local ReplicatedStorage = game:GetService("ReplicatedStorage")

local MotionCheck = {}

function MotionCheck.run(): string
	local passed = 0
	local failures: { string } = {}
	local function case(label: string, fn: () -> ())
		local ok, err = pcall(fn)
		if ok then
			passed += 1
		else
			table.insert(failures, label .. ": " .. tostring(err))
		end
	end
	local function report(): string
		local lines = { string.format("MotionCheck: %d passed, %d failed", passed, #failures) }
		for _, failure in failures do
			table.insert(lines, "- " .. failure)
		end
		return table.concat(lines, "\n")
	end

	local kitModule = ReplicatedStorage:FindFirstChild("UIKit")
	local motionModule = kitModule and kitModule:FindFirstChild("Motion")
	case("Motion installed", function()
		assert(motionModule, "ReplicatedStorage.UIKit.Motion not found")
	end)
	if not kitModule or not motionModule then
		return report()
	end
	local UIKit = require(kitModule) :: any
	local Motion = require(motionModule) :: any
	local theme = UIKit.theme("StudSimulator")
	local playerGui = (Players.LocalPlayer :: Player):WaitForChild("PlayerGui")

	local panelGui = UIKit.Screen(theme, { Name = "_CheckInventory", Enabled = false })
	local _, grid = UIKit.Panel(theme, { Title = "Inventory", Body = "grid", Columns = 5, Parent = panelGui })
	for i = 1, 60 do
		UIKit.Slot(theme, { Name = string.format("Slot%02d", i), Icon = "💎", LayoutOrder = i, Parent = grid })
	end
	local otherGui = UIKit.Screen(theme, { Name = "_CheckShop", Enabled = false })
	UIKit.Panel(theme, { Title = "Shop", Body = "list", Parent = otherGui })
	local hud = UIKit.Screen(theme, { Name = "_CheckHud" })
	local side = UIKit.Button(theme, { Text = "Shop", Size = UDim2.fromScale(0.1, 0.08), Parent = hud })
	side:AddTag("UIKit.HideWithPanel")
	local toggle = UIKit.Toggle(theme, { On = false, Size = UDim2.fromScale(0.08, 0.06), Position = UDim2.fromScale(0.2, 0.1), Parent = hud })
	local slider = UIKit.Slider(theme, { Value = 0.2, Size = UDim2.fromScale(0.2, 0.05), Position = UDim2.fromScale(0.2, 0.2), Parent = hud })
	local tabs = UIKit.Tabs(theme, { Tabs = { "A", "B" }, Selected = "A", Size = UDim2.fromScale(0.2, 0.06), Position = UDim2.fromScale(0.2, 0.3), Parent = hud })
	local stack = UIKit.ToastStack(theme, { Parent = hud })
	local counter = UIKit.Util.text(theme, { Name = "Counter", Text = "0", Size = UDim2.fromScale(0.1, 0.05), Parent = hud })
	panelGui.Parent = playerGui
	otherGui.Parent = playerGui
	hud.Parent = playerGui
	Motion.start()
	task.wait(0.3)

	case("open shows the panel, blurs the world and hides side HUD", function()
		Motion.open(panelGui)
		task.wait(0.6)
		assert(panelGui.Enabled and Motion.isOpen(panelGui), "panel not open")
		local blur = (workspace.CurrentCamera :: Camera):FindFirstChild("UIKitBlur") :: BlurEffect?
		assert(blur and math.abs(blur.Size - theme.motion.worldBlur) < 0.5, "world blur not applied")
		assert(side.Visible == false, "HideWithPanel element still visible")
	end)

	case("long grid scrolls to the last row", function()
		local layout = grid:FindFirstChildOfClass("UIGridLayout") :: UIGridLayout
		assert(layout.CellSize.X.Scale == 0 and layout.CellSize.Y.Offset > 0, "pixel cells not applied")
		grid.CanvasPosition = Vector2.new(0, 1e6)
		task.wait(0.3)
		local last = grid:FindFirstChild("Slot60") :: GuiObject
		local windowTop = grid.AbsolutePosition.Y
		local windowBottom = windowTop + grid.AbsoluteSize.Y
		assert(last.AbsolutePosition.Y + last.AbsoluteSize.Y <= windowBottom + 2, "the last slot is below the scroll window")
		assert(last.AbsolutePosition.Y >= windowTop - 2, "scrolled past the last slot")
	end)

	case("opening another panel closes the first", function()
		Motion.open(otherGui)
		task.wait(0.3)
		assert(otherGui.Enabled and not panelGui.Enabled and not Motion.isOpen(panelGui), "two panels open at once")
	end)

	case("close restores the world", function()
		Motion.close(otherGui)
		task.wait(0.6)
		assert(not otherGui.Enabled and not Motion.isOpen(otherGui), "panel still open")
		local blur = (workspace.CurrentCamera :: Camera):FindFirstChild("UIKitBlur") :: BlurEffect
		assert(blur.Size < 0.5, "blur not removed")
		assert(side.Visible, "side HUD not restored")
	end)

	case("toggle", function()
		Motion.setToggle(toggle, true)
		task.wait(0.4)
		local knob = toggle:FindFirstChild("Knob") :: GuiObject
		assert(toggle:GetAttribute("On") == true and knob.Position.X.Scale > 0.6, "toggle did not switch on")
	end)

	case("slider moves and clamps", function()
		Motion.setSlider(slider, 0.8)
		local fill = (slider:FindFirstChild("Track") :: Frame):FindFirstChild("Fill") :: Frame
		assert(math.abs(slider:GetAttribute("Value") - 0.8) < 1e-3 and math.abs(fill.Size.X.Scale - 0.8) < 1e-3, "slider did not move")
		Motion.setSlider(slider, 3)
		assert(slider:GetAttribute("Value") == 1, "slider must clamp to 1")
	end)

	case("tabs", function()
		Motion.selectTab(tabs, "B")
		local a = tabs:FindFirstChild("A") :: Instance
		local b = tabs:FindFirstChild("B") :: Instance
		assert(tabs:GetAttribute("Selected") == "B", "Selected attribute not updated")
		assert(b:GetAttribute("Variant") == "primary" and a:GetAttribute("Variant") == "secondary", "tab colours not swapped")
	end)

	case("toast appears then removes itself", function()
		local toast = Motion.toast(stack, "Quest complete!", "success", 0.3)
		assert(toast and toast.Visible, "toast not shown")
		local label = toast:FindFirstChild("Label") :: TextLabel
		assert(label.Text == "Quest complete!", "toast text not set")
		task.wait(0.9)
		assert(toast.Parent == nil, "toast not removed after its time")
	end)

	case("countTo lands on the abbreviated target", function()
		Motion.countTo(counter, 0, 1500, 0.2)
		task.wait(0.5)
		assert(counter.Text == "1.5K", "countTo ended at " .. counter.Text)
	end)

	case("press springs back to full size", function()
		Motion.press(side)
		task.wait(0.5)
		local s = side:FindFirstChild("PressScale") :: UIScale?
		assert(s and math.abs(s.Scale - 1) < 0.01, "button stuck at " .. tostring(s and s.Scale))
	end)

	case("strokes are rescaled for this screen", function()
		local edge = side:FindFirstChild("Edge") :: UIStroke
		local expected = math.max(1, edge:GetAttribute("BaseThickness") * UIKit.Util.strokeFactor((workspace.CurrentCamera :: Camera).ViewportSize.Y))
		assert(math.abs(edge.Thickness - expected) < 0.01, "stroke not rescaled")
	end)

	panelGui:Destroy()
	otherGui:Destroy()
	hud:Destroy()
	return report()
end

return MotionCheck
```

- [ ] **Step 2: Install it and watch it fail**

Create `ReplicatedStorage.UIKitDev` with the folder snippet, `multi_edit` `game.ReplicatedStorage.UIKitDev.MotionCheck` (ModuleScript). `start_stop_play` `is_start: true`; when `get_studio_state` lists Client, `execute_luau` (Client): `return require(game.ReplicatedStorage.UIKitDev.MotionCheck).run()`.
Expected:

```
MotionCheck: 0 passed, 1 failed
- Motion installed: ReplicatedStorage.UIKit.Motion not found
```

`start_stop_play` `is_start: false`.

- [ ] **Step 3: Write `roblox-ui/kit/Motion.luau`**

```lua
--!strict
-- Runtime behaviour for kit-built UI. Builders make instances; this makes them feel alive. Every animation reads
-- the theme's motion profile, so one call is bouncy in Stud Simulator and snappy in Battlegrounds.
-- Start it once from a LocalScript: require(ReplicatedStorage.UIKit.Motion).start()

local GuiService = game:GetService("GuiService")
local Players = game:GetService("Players")
local RunService = game:GetService("RunService")
local TweenService = game:GetService("TweenService")
local UserInputService = game:GetService("UserInputService")

local UIKit = require(script.Parent) :: any
local Util = UIKit.Util

local Motion = {}

local BLUR_NAME = "UIKitBlur"
local HOVER_SCALE = 1.05
local TOAST_SECONDS = 2.5
local SPLASH_SECONDS = 2
local RAY_SPIN_SECONDS = 6
local FLICKER_STEP = 0.035
local SLAM_FROM = UDim2.fromScale(-0.6, 0)
local SLAM_TILT = 8
local SLIDE_FROM = UDim2.fromScale(0, 0.04)
local DAMAGE_POP = 0.18
local DAMAGE_HOLD = 0.25
local DAMAGE_FADE = 0.7
local DAMAGE_RISE = UDim2.fromScale(0, 0.06)
local HIT_POP_SCALE = 1.3
local CRIT_POP_SCALE = 1.8
local COUNT_SECONDS = 0.6

local themeCache: { [string]: any } = {}
local openPanels: { [ScreenGui]: boolean } = {}
local bound: { [Instance]: boolean } = setmetatable({}, { __mode = "k" }) :: any
local toastCount = 0
local started = false

local function themeOf(inst: Instance): any
	local node: Instance? = inst
	while node do
		local name = node:GetAttribute("UIKitTheme")
		if type(name) == "string" then
			local theme = themeCache[name]
			if not theme then
				theme = UIKit.theme(name)
				themeCache[name] = theme
			end
			return theme
		end
		node = node.Parent
	end
	return UIKit.theme(UIKit.themeNames()[1])
end

local function tweenInfo(theme: any, speed: string, easing: Enum.EasingStyle?, direction: Enum.EasingDirection?): TweenInfo
	return TweenInfo.new(theme.motion[speed], easing or theme.motion.easing, direction or Enum.EasingDirection.Out)
end

local function play(inst: Instance, info: TweenInfo, goal: { [string]: any }): Tween
	local tween = TweenService:Create(inst, info, goal)
	tween:Play()
	return tween
end

local function scaleOf(gui: GuiObject, name: string): UIScale
	local existing = gui:FindFirstChild(name)
	if existing and existing:IsA("UIScale") then
		return existing
	end
	return Util.make("UIScale", { Name = name, Parent = gui })
end

local function playerGui(): PlayerGui
	return (Players.LocalPlayer :: Player):WaitForChild("PlayerGui") :: PlayerGui
end

function Motion.press(button: GuiObject)
	local theme = themeOf(button)
	local s = scaleOf(button, "PressScale")
	s.Scale = theme.motion.pressScale
	play(s, TweenInfo.new(theme.motion.fast, Enum.EasingStyle.Back, Enum.EasingDirection.Out), { Scale = 1 })
end

function Motion.hover(button: GuiObject, on: boolean)
	play(scaleOf(button, "HoverScale"), tweenInfo(themeOf(button), "fast"), { Scale = if on then HOVER_SCALE else 1 })
end

-- Remembers where an element lives so repeated entrances never drift
local function home(gui: GuiObject): (UDim2, number)
	local position = gui:GetAttribute("HomePosition")
	if typeof(position) ~= "UDim2" then
		position = gui.Position
		gui:SetAttribute("HomePosition", position)
	end
	local rotation = gui:GetAttribute("HomeRotation")
	if type(rotation) ~= "number" then
		rotation = gui.Rotation
		gui:SetAttribute("HomeRotation", rotation)
	end
	return position :: UDim2, rotation :: number
end

-- Plays the theme's entrance: pop, stamp, slam, flicker, slide or fade
function Motion.enter(gui: GuiObject)
	local theme = themeOf(gui)
	local m = theme.motion
	local s = scaleOf(gui, "OpenScale")
	local position, rotation = home(gui)
	gui.Position = position
	gui.Rotation = rotation
	-- players with Reduced Motion on get the element in place: no slams, flicker or bounce
	if GuiService.ReducedMotionEnabled then
		s.Scale = 1
		gui.Visible = true
		return
	end
	s.Scale = m.openFrom
	if m.style == "pop" then
		play(s, TweenInfo.new(m.normal, Enum.EasingStyle.Back, Enum.EasingDirection.Out), { Scale = 1 })
	elseif m.style == "stamp" then
		play(s, TweenInfo.new(m.fast, Enum.EasingStyle.Linear), { Scale = 1 })
	elseif m.style == "slam" then
		gui.Position = position + SLAM_FROM
		gui.Rotation = rotation - SLAM_TILT
		play(gui, TweenInfo.new(m.normal, Enum.EasingStyle.Back, Enum.EasingDirection.Out), { Position = position, Rotation = rotation })
		play(s, TweenInfo.new(m.slow, Enum.EasingStyle.Back, Enum.EasingDirection.Out), { Scale = 1 })
	elseif m.style == "flicker" then
		task.spawn(function()
			for _, visible in { false, true, false, true } do
				gui.Visible = visible
				task.wait(FLICKER_STEP)
			end
			play(s, tweenInfo(theme, "normal"), { Scale = 1 })
		end)
	elseif m.style == "slide" then
		gui.Position = position + SLIDE_FROM
		play(gui, tweenInfo(theme, "normal"), { Position = position })
		play(s, tweenInfo(theme, "normal"), { Scale = 1 })
	else
		play(s, tweenInfo(theme, "slow"), { Scale = 1 })
	end
end

local function updateWorld(theme: any)
	local anyOpen = next(openPanels) ~= nil
	local camera = workspace.CurrentCamera
	if camera then
		local blur = camera:FindFirstChild(BLUR_NAME)
		if not blur then
			blur = Util.make("BlurEffect", { Name = BLUR_NAME, Size = 0, Parent = camera })
		end
		-- Quad, not the theme easing: a Back overshoot would push the blur below zero
		play(blur :: BlurEffect, tweenInfo(theme, "normal", Enum.EasingStyle.Quad), { Size = if anyOpen then theme.motion.worldBlur else 0 })
	end
	for _, d in playerGui():GetDescendants() do
		if d:IsA("GuiObject") and d:HasTag("UIKit.HideWithPanel") then
			d.Visible = not anyOpen
		end
	end
end

function Motion.isOpen(gui: ScreenGui): boolean
	return openPanels[gui] == true
end

-- One panel at a time: opening one closes the rest, blurs the world and hides HUD clutter tagged
-- UIKit.HideWithPanel (the Lift a Rock behaviour)
function Motion.open(gui: ScreenGui)
	for other in openPanels do
		if other ~= gui then
			Motion.close(other)
		end
	end
	gui.Enabled = true
	openPanels[gui] = true
	local main = gui:FindFirstChild("Main")
	if main and main:IsA("GuiObject") then
		Motion.enter(main)
	end
	updateWorld(themeOf(gui))
end

function Motion.close(gui: ScreenGui)
	gui.Enabled = false
	if openPanels[gui] then
		openPanels[gui] = nil
		updateWorld(themeOf(gui))
	end
end

function Motion.toggle(gui: ScreenGui)
	if openPanels[gui] then
		Motion.close(gui)
	else
		Motion.open(gui)
	end
end

function Motion.setToggle(toggle: GuiObject, on: boolean)
	local theme = themeOf(toggle)
	toggle:SetAttribute("On", on)
	local knob = toggle:FindFirstChild("Knob")
	if knob and knob:IsA("GuiObject") then
		play(knob, tweenInfo(theme, "fast"), { Position = UDim2.fromScale(if on then 0.73 else 0.27, 0.5) })
	end
	local fill = toggle:FindFirstChild("Fill")
	if fill and fill:IsA("GuiObject") then
		play(fill, tweenInfo(theme, "fast", Enum.EasingStyle.Quad), { BackgroundTransparency = if on then 0 else 1 })
	end
end

function Motion.setSlider(slider: GuiObject, value: number)
	local v = math.clamp(value, 0, 1)
	slider:SetAttribute("Value", v)
	local track = slider:FindFirstChild("Track")
	local fill = track and track:FindFirstChild("Fill")
	if fill and fill:IsA("GuiObject") then
		fill.Size = UDim2.fromScale(v, 1)
	end
	local knob = slider:FindFirstChild("Knob")
	if knob and knob:IsA("GuiObject") then
		knob.Position = UDim2.fromScale(v, 0.5)
	end
end

function Motion.selectTab(tabs: Instance, id: string)
	local theme = themeOf(tabs)
	for _, child in tabs:GetChildren() do
		if child:IsA("GuiButton") then
			UIKit.setVariant(theme, child, if child.Name == id then "primary" else "secondary")
		end
	end
	tabs:SetAttribute("Selected", id)
end

local function isPress(input: InputObject): boolean
	return input.UserInputType == Enum.UserInputType.MouseButton1 or input.UserInputType == Enum.UserInputType.Touch
end

local function bindSlider(slider: GuiObject)
	local track = slider:FindFirstChild("Track")
	if not track or not track:IsA("GuiObject") then
		return
	end
	local dragging = false
	local function follow(x: number)
		Motion.setSlider(slider, (x - track.AbsolutePosition.X) / math.max(1, track.AbsoluteSize.X))
	end
	local function begin(input: InputObject)
		if isPress(input) then
			dragging = true
			follow(input.Position.X)
		end
	end
	slider.InputBegan:Connect(begin)
	local knob = slider:FindFirstChild("Knob")
	if knob and knob:IsA("GuiObject") then
		-- the knob is a button, so it swallows input before the slider frame sees it
		knob.InputBegan:Connect(begin)
	end
	UserInputService.InputChanged:Connect(function(input)
		if dragging and (input.UserInputType == Enum.UserInputType.MouseMovement or input.UserInputType == Enum.UserInputType.Touch) then
			follow(input.Position.X)
		end
	end)
	UserInputService.InputEnded:Connect(function(input)
		if isPress(input) then
			dragging = false
		end
	end)
end

function Motion.toast(stack: Instance, text: string, kind: string?, seconds: number?): GuiObject?
	local template = stack:FindFirstChild("Template")
	if not template or not template:IsA("GuiObject") then
		return nil
	end
	local theme = themeOf(stack)
	local toast = template:Clone()
	toast.Name = "Toast"
	toastCount += 1
	toast.LayoutOrder = -toastCount -- newest on top
	local label = toast:FindFirstChild("Label")
	if label and label:IsA("TextLabel") then
		label.Text = text
	end
	local stripe = toast:FindFirstChild("Stripe")
	local gradient = stripe and stripe:FindFirstChildOfClass("UIGradient")
	if gradient then
		gradient.Color = Util.sequence(theme.color.bars[kind or "accent"])
	end
	toast.Visible = true
	toast.Parent = stack
	Motion.enter(toast)
	task.delay(seconds or TOAST_SECONDS, function()
		if toast.Parent then
			local info = tweenInfo(theme, "fast", Enum.EasingStyle.Quad, Enum.EasingDirection.In)
			play(scaleOf(toast, "OpenScale"), info, { Scale = 0 }).Completed:Wait()
			toast:Destroy()
		end
	end)
	return toast
end

function Motion.countTo(label: TextLabel, from: number, to: number, seconds: number?, format: ((number) -> string)?)
	local fmt = format or Util.abbreviate
	local duration = seconds or COUNT_SECONDS
	local startedAt = os.clock()
	local connection: RBXScriptConnection
	connection = RunService.RenderStepped:Connect(function()
		local t = math.clamp((os.clock() - startedAt) / duration, 0, 1)
		local eased = 1 - (1 - t) ^ 3
		label.Text = fmt(from + (to - from) * eased)
		if t >= 1 then
			connection:Disconnect()
		end
	end)
end

function Motion.damage(layer: Instance, at: UDim2, amount: number, crit: boolean?): TextLabel
	local theme = themeOf(layer)
	local label = UIKit.DamageNumber(theme, { Amount = Util.abbreviate(amount), Crit = crit, Position = at, Parent = layer })
	local s = scaleOf(label, "OpenScale")
	s.Scale = if crit then CRIT_POP_SCALE else HIT_POP_SCALE
	play(s, TweenInfo.new(DAMAGE_POP, Enum.EasingStyle.Back, Enum.EasingDirection.Out), { Scale = 1 })
	local fade = TweenInfo.new(DAMAGE_FADE, Enum.EasingStyle.Quad, Enum.EasingDirection.Out, 0, false, DAMAGE_HOLD)
	local rise = play(label, fade, { Position = at - DAMAGE_RISE, TextTransparency = 1 })
	local stroke = label:FindFirstChild("TextStroke")
	if stroke then
		play(stroke, fade, { Transparency = 1 })
	end
	rise.Completed:Connect(function()
		label:Destroy()
	end)
	return label
end

function Motion.splash(splash: GuiObject, seconds: number?)
	splash.Visible = true
	Motion.enter(splash)
	local rays = splash:FindFirstChild("Rays")
	local spin: Tween? = nil
	if rays and rays:IsA("GuiObject") then
		rays.Rotation = 0
		spin = play(rays, TweenInfo.new(RAY_SPIN_SECONDS, Enum.EasingStyle.Linear, Enum.EasingDirection.InOut, -1), { Rotation = 360 })
	end
	task.delay(seconds or SPLASH_SECONDS, function()
		if spin then
			spin:Cancel()
		end
		splash.Visible = false
	end)
end

function Motion.setBar(bar: Instance, fraction: number, side: string?)
	local holder = if side then bar:FindFirstChild(side) else bar
	local fill = holder and holder:FindFirstChild("Fill")
	if fill and fill:IsA("GuiObject") then
		play(fill, tweenInfo(themeOf(bar), "normal", Enum.EasingStyle.Quad), { Size = UDim2.fromScale(math.clamp(fraction, 0, 1), 1) })
	end
end

function Motion.cooldown(slot: Instance, seconds: number)
	local shade = slot:FindFirstChild("Cooldown")
	if shade and shade:IsA("GuiObject") then
		shade.Size = UDim2.fromScale(1, 1)
		play(shade, TweenInfo.new(seconds, Enum.EasingStyle.Linear), { Size = UDim2.fromScale(1, 0) })
	end
end

function Motion.loading(gui: Instance, seconds: number, onDone: (() -> ())?)
	local bar = gui:FindFirstChild("Progress", true)
	local fill = bar and bar:FindFirstChild("Fill")
	local value = bar and bar:FindFirstChild("Value")
	task.spawn(function()
		local startedAt = os.clock()
		while true do
			local t = math.clamp((os.clock() - startedAt) / seconds, 0, 1)
			if fill and fill:IsA("GuiObject") then
				fill.Size = UDim2.fromScale(t, 1)
			end
			if value and value:IsA("TextLabel") then
				value.Text = string.format("%d%%", math.floor(t * 100))
			end
			if t >= 1 then
				break
			end
			task.wait()
		end
		if onDone then
			onDone()
		end
	end)
end

local function bind(inst: Instance)
	if bound[inst] then
		return
	end
	if inst:IsA("GuiButton") and inst:HasTag("UIKit.Button") then
		bound[inst] = true
		inst.Activated:Connect(function()
			Motion.press(inst)
			if inst:HasTag("UIKit.Close") then
				local screen = inst:FindFirstAncestorOfClass("ScreenGui")
				if screen then
					Motion.close(screen)
				end
			end
			local target = inst:GetAttribute("Opens")
			if type(target) == "string" then
				local screen = playerGui():FindFirstChild(target)
				if screen and screen:IsA("ScreenGui") then
					Motion.toggle(screen)
				end
			end
			local parent = inst.Parent
			if parent and parent:HasTag("UIKit.Tabs") then
				Motion.selectTab(parent, inst.Name)
			end
		end)
		-- touch fires MouseEnter without a matching MouseLeave, which leaves buttons stuck big on phones
		if UserInputService.MouseEnabled then
			inst.MouseEnter:Connect(function()
				Motion.hover(inst, true)
			end)
			inst.MouseLeave:Connect(function()
				Motion.hover(inst, false)
			end)
		end
	elseif inst:IsA("GuiButton") and inst:HasTag("UIKit.Toggle") then
		bound[inst] = true
		inst.Activated:Connect(function()
			Motion.setToggle(inst, not inst:GetAttribute("On"))
		end)
	elseif inst:IsA("GuiObject") and inst:HasTag("UIKit.Slider") then
		bound[inst] = true
		bindSlider(inst)
	elseif inst:IsA("UIGridLayout") and inst:GetAttribute("DesignCell") ~= nil then
		bound[inst] = true
		Util.pixelGrid(inst)
	end
end

local function rescaleStroke(inst: Instance)
	local camera = workspace.CurrentCamera
	local base = inst:GetAttribute("BaseThickness")
	if camera and type(base) == "number" and (inst:IsA("UIStroke") or inst:IsA("Path2D")) then
		(inst :: any).Thickness = math.max(1, base * Util.strokeFactor(camera.ViewportSize.Y))
	end
end

function Motion.start()
	if started then
		return
	end
	started = true
	local pg = playerGui()
	for _, d in pg:GetDescendants() do
		bind(d)
		rescaleStroke(d)
	end
	pg.DescendantAdded:Connect(function(d)
		task.defer(bind, d)
		rescaleStroke(d)
	end)
	local camera = workspace.CurrentCamera
	if camera then
		camera:GetPropertyChangedSignal("ViewportSize"):Connect(function()
			Util.scaleStrokes(pg, camera.ViewportSize.Y)
		end)
	end
end

return Motion
```

- [ ] **Step 4: Write `roblox-ui/kit/UIRuntime.client.luau`**

```lua
-- Gives every kit-built ScreenGui its runtime behaviour: press feedback, panels, toggles, sliders, tabs, grid
-- sizing and stroke scaling. Game code can require the same Motion module for toasts, damage numbers and bars.
local ReplicatedStorage = game:GetService("ReplicatedStorage")

local Motion = require(ReplicatedStorage:WaitForChild("UIKit"):WaitForChild("Motion"))
Motion.start()
```

- [ ] **Step 5: Install and run both suites**

`multi_edit` `game.ReplicatedStorage.UIKit.Motion` (ModuleScript) and `game.StarterPlayer.StarterPlayerScripts.UIRuntime` (LocalScript). Run KitCheck (Edit): expected `KitCheck: 36 passed, 0 failed`. Then play, run MotionCheck on the Client, stop play.
Expected: `MotionCheck: 12 passed, 0 failed`. If "long grid scrolls to the last row" fails, the pixel-grid fix is broken; that is the exact bug Lift a Rock hit, so fix `Util.pixelGrid` before moving on.

- [ ] **Step 6: Commit**

```bash
git add roblox-ui/kit/Motion.luau roblox-ui/kit/UIRuntime.client.luau roblox-ui/kit/dev/MotionCheck.luau
git commit -m "feat: add Motion runtime with play-mode checks"
```

### Task 8: Showcase builder + Stud Simulator screens (user checkpoint)

**Files:**
- Create: `roblox-ui/kit/dev/Showcase.luau`, `roblox-ui/screenshots/stud-simulator-{hud,menus,loading,mainmenu,feedback}.jpg`
- Install: `game.ServerStorage.UIKitDev.Showcase` (ModuleScript)
- Modify (UI/UX place): `Workspace.ShowcaseBackdrop` (new Model), `StarterGui.SC_StudSimulator_*` (5 new ScreenGuis)

**Interfaces:**
- Consumes: every builder; `Util.scaleStrokes`, `Util.pixelGrid`.
- Produces: `Showcase.SCREENS`, `Showcase.USE_EMOJI`, `Showcase.build(UIKit, themeName, screenName): ScreenGui`, `Showcase.buildTheme(UIKit, themeName)`, `Showcase.show(UIKit, themeName, screenName): string`. ScreenGuis are named `SC_<Theme>_<Screen>` with attributes `ShowcaseTheme`, `ShowcaseScreen`. Task 14's runtime switches between them by those attributes.

- [ ] **Step 1: Write the rebuild-safety test first**

`execute_luau` (Edit). It must fail now because Showcase doesn't exist:

```lua
local RS, SS, SG = game:GetService("ReplicatedStorage"), game:GetService("ServerStorage"), game:GetService("StarterGui")
local showcaseModule = SS.UIKitDev:FindFirstChild("Showcase")
if not showcaseModule then
	return "FAIL: ServerStorage.UIKitDev.Showcase not found"
end
local UIKit = require(RS.UIKit:Clone())
local Showcase = require(showcaseModule:Clone())
local handMade = Instance.new("ScreenGui")
handMade.Name = "SC_StudSimulator_Feedback"
handMade.Parent = SG
local mine = Instance.new("ScreenGui")
mine.Name = "MyOwnHud"
mine.Parent = SG
Showcase.build(UIKit, "StudSimulator", "HUD")
Showcase.build(UIKit, "StudSimulator", "HUD")
local count = 0
for _, g in SG:GetChildren() do
	if g.Name == "SC_StudSimulator_HUD" then
		count += 1
	end
end
local refused = not pcall(Showcase.build, UIKit, "StudSimulator", "Feedback")
local ok = count == 1 and mine.Parent == SG and handMade.Parent == SG and refused
handMade:Destroy()
mine:Destroy()
return if ok then "PASS rebuild safety" else string.format("FAIL count=%d mineKept=%s handMadeKept=%s refused=%s", count, tostring(mine.Parent == SG), tostring(handMade.Parent == SG), tostring(refused))
```

Expected now: `FAIL: ServerStorage.UIKitDev.Showcase not found`.

- [ ] **Step 2: Write `roblox-ui/kit/dev/Showcase.luau`**

```lua
--!strict
-- Builds the demo screens for the UI/UX showcase place: every theme × HUD, Menus, Loading, MainMenu, Feedback.
-- Each is a ScreenGui named SC_<Theme>_<Screen> in StarterGui, built disabled; show() enables exactly one.
-- Rebuilding replaces only kit-built screens and refuses to overwrite a hand-made ScreenGui with the same name.

local StarterGui = game:GetService("StarterGui")

local Showcase = {}

Showcase.SCREENS = { "HUD", "Menus", "Loading", "MainMenu", "Feedback" }

-- Emoji icons need zero uploads. Set to false if Task 1 found emoji don't render; plain letters are used then.
Showcase.USE_EMOJI = true

local ICONS: { [string]: { string } } = {
	cash = { "💵", "$" }, gem = { "💎", "G" }, shop = { "🛒", "S" }, pets = { "🐾", "P" }, upgrade = { "⬆️", "U" },
	rebirth = { "🔄", "R" }, gift = { "🎁", "!" }, star = { "⭐", "*" }, muscle = { "💪", "M" }, crown = { "👑", "V" },
	clover = { "🍀", "L" }, sword = { "⚔️", "X" }, shield = { "🛡️", "B" }, fist = { "👊", "F" }, dash = { "💨", "D" },
	jump = { "⏫", "J" }, skull = { "💀", "K" }, bolt = { "⚡", "Z" }, book = { "📖", "I" }, bag = { "🎒", "B" },
	potion = { "🧪", "+" }, settings = { "⚙️", "=" }, film = { "🎬", "W" },
}

-- Copy per theme so each style reads like a real game (original names, no other game's content)
local COPY: { [string]: { [string]: any } } = {
	StudSimulator = {
		game = "Lift a Rock", tagline = "Get strong. Lift bigger rocks.", tip = "Tip: rebirth to lift heavier rocks!",
		moves = { "Lift", "Throw", "Flex", "Smash" },
	},
	Battlegrounds = {
		game = "BATTLEGROUNDS", tagline = "Last one standing wins.", tip = "Tip: dash-cancel your combo with Q",
		moves = { "Rapid Blows", "Flare Burst", "Shock Shot", "Sky Dive" },
	},
	KineticComic = {
		game = "PHANTOM RUSH", tagline = "Steal the show. Leave a calling card.", tip = "The deadline is in 3 days",
		moves = { "Slash", "Pistol", "Summon", "All-Out" },
	},
	CyberHolo = {
		game = "NEON//PROTOCOL", tagline = "SYS.BOOT > ALL SYSTEMS NOMINAL", tip = "SYS: overclock drains energy 2x faster",
		moves = { "Pulse", "Phase", "Overclock", "EMP" },
	},
	MangaInk = {
		game = "INK BLADE", tagline = "Chapter 1: The Brush That Cuts", tip = "Hold the brush stroke to charge",
		moves = { "Ink Slash", "Splash", "Brush Dash", "Final Panel" },
	},
	DarkFantasy = {
		game = "ASHEN CROWN", tagline = "The flame remembers those who kneel.", tip = "Rest at a shrine to restore your blood",
		moves = { "Rend", "Blood Ward", "Ember Step", "Crimson Rite" },
	},
}

local function icon(key: string): string
	local pair = ICONS[key]
	return if Showcase.USE_EMOJI then pair[1] else pair[2]
end

local function group(UIKit: any, parent: Instance, name: string, props: { [string]: any }, direction: Enum.FillDirection?): Frame
	local frame = UIKit.Util.make("Frame", {
		Name = name, BackgroundTransparency = 1, Position = props.Position, Size = props.Size,
		AnchorPoint = props.AnchorPoint or Vector2.zero, ZIndex = 2, Parent = parent,
	})
	if direction then
		UIKit.Util.make("UIListLayout", {
			FillDirection = direction, Padding = UDim.new(0, 8), SortOrder = Enum.SortOrder.LayoutOrder,
			HorizontalAlignment = Enum.HorizontalAlignment.Center, VerticalAlignment = Enum.VerticalAlignment.Center, Parent = frame,
		})
	end
	return frame
end

local function hudSimulator(UIKit: any, theme: any, gui: ScreenGui)
	local stats = group(UIKit, gui, "Stats", { Position = UDim2.fromScale(0.01, 0.16), Size = UDim2.fromScale(0.2, 0.18) }, Enum.FillDirection.Vertical)
	UIKit.Currency(theme, { Name = "Gems", Icon = icon("gem"), Amount = "1,250", Kind = "health", Size = UDim2.fromScale(1, 0.42), LayoutOrder = 1, Parent = stats })
	UIKit.Currency(theme, { Name = "Cash", Icon = icon("cash"), Amount = "$12.4K", Kind = "accent", Size = UDim2.fromScale(1, 0.48), LayoutOrder = 2, Parent = stats })

	local menu = group(UIKit, gui, "LeftButtons", { Position = UDim2.fromScale(0.01, 0.38), Size = UDim2.fromScale(0.16, 0.34) })
	UIKit.Util.aspect(menu, 1)
	UIKit.Util.make("UIGridLayout", { CellSize = UDim2.fromScale(0.46, 0.46), CellPadding = UDim2.fromScale(0.06, 0.06), SortOrder = Enum.SortOrder.LayoutOrder, Parent = menu })
	for i, b in { { "Shop", "shop" }, { "Pets", "pets" }, { "Upgrades", "upgrade" }, { "Rebirth", "rebirth" } } do
		UIKit.IconButton(theme, { Name = b[1], Icon = icon(b[2]), Caption = b[1], Badge = if i == 2 then "NEW!" else nil, LayoutOrder = i, Parent = menu })
	end

	local top = group(UIKit, gui, "TopButtons", { Position = UDim2.fromScale(0.5, 0.02), AnchorPoint = Vector2.new(0.5, 0), Size = UDim2.fromScale(0.3, 0.1) }, Enum.FillDirection.Horizontal)
	UIKit.Button(theme, { Name = "Spawn", Text = "Spawn", Variant = "primary", Size = UDim2.fromScale(0.47, 1), LayoutOrder = 1, Parent = top })
	UIKit.Button(theme, { Name = "Home", Text = "Home", Variant = "success", Size = UDim2.fromScale(0.47, 1), LayoutOrder = 2, Parent = top })
	UIKit.Bar(theme, {
		Name = "Quest", Style = "single", Kind = "xp", Value = 0.4, Label = "Lift 10 rocks", ValueText = "4/10",
		Size = UDim2.fromScale(0.26, 0.045), Position = UDim2.fromScale(0.5, 0.135), AnchorPoint = Vector2.new(0.5, 0), Parent = gui,
	})

	local offer = UIKit.Button(theme, {
		Name = "Offer", Text = "2X Strength", Variant = "primary", Size = UDim2.fromScale(0.15, 0.1),
		Position = UDim2.fromScale(0.985, 0.2), AnchorPoint = Vector2.new(1, 0), Parent = gui,
	})
	UIKit.Badge(theme, { Text = "Permanent!", Kind = "health", Rotation = 4, Size = UDim2.fromScale(0.6, 0.38), Position = UDim2.fromScale(0.42, -0.25), Parent = offer })
	UIKit.IconButton(theme, {
		Name = "FreeGift", Icon = icon("gift"), Caption = "Free", Size = UDim2.fromScale(0.07, 0.12),
		Position = UDim2.fromScale(0.95, 0.35), AnchorPoint = Vector2.new(0.5, 0), Parent = gui,
	})

	UIKit.Util.text(theme, {
		Name = "Strength", Text = "1,240 Strength", Role = "display", Size = UDim2.fromScale(0.3, 0.06),
		Position = UDim2.fromScale(0.5, 0.76), AnchorPoint = Vector2.new(0.5, 0.5), Parent = gui,
	})
	UIKit.Bar(theme, {
		Name = "LevelBar", Style = "single", Kind = "xp", Value = 0.62, Label = "Level 7", ValueText = "62/100", Icon = icon("star"),
		Size = UDim2.fromScale(0.46, 0.065), Position = UDim2.fromScale(0.5, 0.84), AnchorPoint = Vector2.new(0.5, 0.5), Parent = gui,
	})

	local corner = group(UIKit, gui, "BottomLeft", { Position = UDim2.fromScale(0.01, 0.98), AnchorPoint = Vector2.new(0, 1), Size = UDim2.fromScale(0.24, 0.1) }, Enum.FillDirection.Horizontal)
	for i, b in { { "Index", "book" }, { "Rewards", "film" }, { "Inventory", "bag" } } do
		UIKit.IconButton(theme, { Name = b[1], Icon = icon(b[2]), Size = UDim2.fromScale(1, 1), LayoutOrder = i, Parent = corner })
	end
end

local function hudCombat(UIKit: any, theme: any, gui: ScreenGui, copy: { [string]: any })
	local card = group(UIKit, gui, "PlayerCard", { Position = UDim2.fromScale(0.01, 0.03), Size = UDim2.fromScale(0.24, 0.1) })
	UIKit.Util.icon(theme, icon("skull"), { Name = "Portrait", Size = UDim2.fromScale(1, 1), Parent = card })
	UIKit.Util.text(theme, {
		Name = "PlayerName", Text = "Player1", Role = "display", XAlign = Enum.TextXAlignment.Left,
		Size = UDim2.fromScale(0.68, 0.45), Position = UDim2.fromScale(0.3, 0.02), Parent = card,
	})
	UIKit.Badge(theme, { Name = "Level", Text = "LV 42", Kind = "xp", Size = UDim2.fromScale(0.3, 0.38), Position = UDim2.fromScale(0.3, 0.56), Parent = card })
	UIKit.Currency(theme, {
		Name = "Coins", Icon = icon("gem"), Amount = "8,450", Kind = "accent", Size = UDim2.fromScale(0.16, 0.06),
		Position = UDim2.fromScale(0.99, 0.03), AnchorPoint = Vector2.new(1, 0), Parent = gui,
	})

	UIKit.Badge(theme, {
		Name = "Ultimate", Text = "MAXIMUM OUTPUT [G]", Kind = "accent", Slant = true, Size = UDim2.fromScale(0.26, 0.045),
		Position = UDim2.fromScale(0.5, 0.6), AnchorPoint = Vector2.new(0.5, 0.5), Parent = gui,
	})
	local style = theme.shape.barStyle
	local split = style == "split"
	UIKit.Bar(theme, {
		Name = "Vitals", Style = style, Kind = "health", Value = 0.72, RightKind = "energy", RightValue = 0.45,
		Segments = if style == "single" then nil else 12, Emblem = if split then icon("skull") else nil,
		Label = if split then nil else "HP", ValueText = if split then nil else "72/100",
		Size = UDim2.fromScale(0.42, 0.04), Position = UDim2.fromScale(0.5, 0.67), AnchorPoint = Vector2.new(0.5, 0.5), Parent = gui,
	})
	if not split then
		UIKit.Bar(theme, {
			Name = "Energy", Style = style, Kind = "energy", Value = 0.45, Segments = 12, Size = UDim2.fromScale(0.3, 0.02),
			Position = UDim2.fromScale(0.5, 0.715), AnchorPoint = Vector2.new(0.5, 0.5), Parent = gui,
		})
	end
	local slots = {}
	for i, move in copy.moves do
		table.insert(slots, { Key = tostring(i), Title = move, Cooldown = if i == 3 then 0.55 else 0, Selected = i == 1 })
	end
	UIKit.Hotbar(theme, {
		Name = "Moves", Slots = slots, Size = UDim2.fromScale(0.36, 0.13), Position = UDim2.fromScale(0.5, 0.86),
		AnchorPoint = Vector2.new(0.5, 0.5), Parent = gui,
	})

	local mobile = group(UIKit, gui, "MobileButtons", { Position = UDim2.fromScale(0.985, 0.97), AnchorPoint = Vector2.new(1, 1), Size = UDim2.fromScale(0.17, 0.32) })
	for _, b in {
		{ "Jump", "jump", 0.72, 0.76, 0.5 }, { "Dash", "dash", 0.2, 0.82, 0.34 },
		{ "Attack", "fist", 0.74, 0.3, 0.36 }, { "Block", "shield", 0.24, 0.4, 0.34 },
	} do
		UIKit.IconButton(theme, {
			Name = b[1], Icon = icon(b[2]), Round = true, Size = UDim2.fromScale(b[5], b[5]), Position = UDim2.fromScale(b[3], b[4]),
			AnchorPoint = Vector2.new(0.5, 0.5), Parent = mobile,
		})
	end
end

-- Rows are pixel-tall (52) inside a scrolling list so a phone keeps 44-px controls and simply scrolls
local SETTINGS_ROW_HEIGHT = 52
local TAB_HEIGHT = 44

local function settingsRow(UIKit: any, theme: any, list: Instance, index: number, label: string): Frame
	local row = UIKit.Util.make("Frame", {
		Name = label, BackgroundColor3 = theme.color.surface, BackgroundTransparency = theme.color.surfaceTransparency,
		BorderSizePixel = 0, Size = UDim2.new(1, 0, 0, SETTINGS_ROW_HEIGHT), LayoutOrder = index, ZIndex = 3, Parent = list,
	})
	UIKit.Util.corner(row, theme.radius.slot)
	UIKit.Util.stroke(row, theme.color.barEdge, theme.stroke.slot)
	UIKit.Util.text(theme, {
		Name = "Label", Text = label, Role = "display", XAlign = Enum.TextXAlignment.Left, Size = UDim2.fromScale(0.5, 0.6),
		Position = UDim2.fromScale(0.05, 0.2), Parent = row,
	})
	return row
end

local function menus(UIKit: any, theme: any, gui: ScreenGui)
	local panelSize = UDim2.fromScale(0.31, 0.72)
	local _, shopBody = UIKit.Panel(theme, {
		Name = "Shop", Title = "Shop", Icon = icon("shop"), Body = "none", Tilt = false, AspectRatio = 0.85,
		Size = panelSize, Position = UDim2.fromScale(0.175, 0.55), Parent = gui,
	})
	UIKit.Tabs(theme, { Tabs = { "Featured", "Passes", "Coins" }, Selected = "Featured", Size = UDim2.new(1, 0, 0, TAB_HEIGHT), Parent = shopBody })
	local list = UIKit.List(theme, { Position = UDim2.fromOffset(0, TAB_HEIGHT + 8), Size = UDim2.new(1, 0, 1, -(TAB_HEIGHT + 8)), Parent = shopBody })
	for i, item in {
		{ "2X Strength", "Double every lift", "R$ 199", "muscle" }, { "VIP", "Chat tag + 10% cash", "R$ 399", "crown" },
		{ "Lucky Pack", "+50% luck, 30 min", "R$ 49", "clover" }, { "Starter Bundle", "Gems, pets and boosts", "R$ 99", "gift" },
	} do
		UIKit.Card(theme, { Name = "Item" .. i, Title = item[1], Subtitle = item[2], Action = item[3], Icon = icon(item[4]), Height = 64, LayoutOrder = i, Parent = list })
	end

	local _, grid = UIKit.Panel(theme, {
		Name = "Inventory", Title = "Inventory", Icon = icon("bag"), Body = "grid", Columns = 4, AspectRatio = 0.85,
		Size = panelSize, Position = UDim2.fromScale(0.5, 0.55), Parent = gui,
	})
	for i, key in { "gem", "muscle", "crown", "clover", "gift", "potion", "star", "sword", "shield", "bolt", "skull", "book" } do
		UIKit.Slot(theme, { Name = "Item" .. i, Icon = icon(key), Value = if i % 3 == 0 then "x" .. i else nil, Selected = i == 2, LayoutOrder = i, Parent = grid })
	end

	local _, settingsList = UIKit.Panel(theme, {
		Name = "Settings", Title = "Settings", Icon = icon("settings"), Body = "list", AspectRatio = 0.85,
		Size = panelSize, Position = UDim2.fromScale(0.825, 0.55), Parent = gui,
	})
	local function control(row: Frame, kind: string, value: any)
		local anchor = Vector2.new(1, 0.5)
		if kind == "toggle" then
			UIKit.Toggle(theme, { On = value, Size = UDim2.fromScale(0.3, 0.7), Position = UDim2.fromScale(0.95, 0.5), AnchorPoint = anchor, Parent = row })
		elseif kind == "slider" then
			UIKit.Slider(theme, { Value = value, Size = UDim2.fromScale(0.4, 0.6), Position = UDim2.fromScale(0.93, 0.5), AnchorPoint = anchor, Parent = row })
		else
			UIKit.TextInput(theme, { Placeholder = "Enter code", Size = UDim2.fromScale(0.44, 0.7), Position = UDim2.fromScale(0.95, 0.5), AnchorPoint = anchor, Parent = row })
		end
	end
	for i, r in { { "Music", "toggle", true }, { "Sound FX", "toggle", true }, { "Volume", "slider", 0.7 }, { "Low Graphics", "toggle", false }, { "Codes", "input", nil } } do
		control(settingsRow(UIKit, theme, settingsList, i, r[1]), r[2], r[3])
	end
end

local function feedback(UIKit: any, theme: any, gui: ScreenGui)
	local popup = UIKit.Popup(theme, {
		Name = "Reward", Title = "You got!", Body = "Golden Dumbbell", Icon = icon("gift"), Confirm = "Claim", Cancel = "Later", Parent = gui,
	})
	-- keep the splash, toasts and damage numbers above the popup's dim for the showcase shot
	popup.ZIndex = 5
	local stack = UIKit.ToastStack(theme, { Parent = gui })
	for i, t in { { "Quest complete! +250 XP", "xp" }, { "x2 Luck active for 15:00", "accent" }, { "Not enough coins", "health" } } do
		UIKit.Toast(theme, { Name = "Toast" .. i, Text = t[1], Kind = t[2], LayoutOrder = i, Parent = stack })
	end
	UIKit.Splash(theme, { Name = "LevelUp", Text = "LEVEL UP!", Kind = "xp", Parent = gui })
	for _, d in { { 0.16, 0.42, "125", false }, { 0.24, 0.55, "1.2K", true }, { 0.12, 0.64, "98", false } } do
		UIKit.DamageNumber(theme, { Amount = d[3], Crit = d[4], Position = UDim2.fromScale(d[1], d[2]), Parent = gui })
	end
end

local function fitToViewport(UIKit: any, gui: ScreenGui)
	local camera = workspace.CurrentCamera
	if camera then
		UIKit.Util.scaleStrokes(gui, camera.ViewportSize.Y)
	end
	for _, d in gui:GetDescendants() do
		if d:IsA("UIGridLayout") and d:GetAttribute("DesignCell") ~= nil then
			UIKit.Util.pixelGrid(d)
		end
	end
end

function Showcase.build(UIKit: any, themeName: string, screenName: string): ScreenGui
	local theme = UIKit.theme(themeName)
	local copy = COPY[themeName]
	assert(copy, "Showcase has no copy for theme " .. themeName)
	local name = "SC_" .. themeName .. "_" .. screenName
	local old = StarterGui:FindFirstChild(name)
	if old then
		assert(old:GetAttribute("UIKitBuilt") == true, name .. " exists and was not built by UIKit; rename it first")
		old:Destroy()
	end
	local gui: ScreenGui
	if screenName == "Loading" then
		gui = UIKit.LoadingScreen(theme, { Name = name, Title = copy.game, Tip = copy.tip, Progress = 0.62 })
	elseif screenName == "MainMenu" then
		gui = UIKit.MainMenu(theme, { Name = name, Title = copy.game, Subtitle = copy.tagline, Buttons = { "PLAY", "SHOP", "SETTINGS", "CODES" } })
	else
		gui = UIKit.Screen(theme, { Name = name })
		if screenName == "HUD" then
			if theme.hudLayout == "simulator" then
				hudSimulator(UIKit, theme, gui)
			else
				hudCombat(UIKit, theme, gui, copy)
			end
		elseif screenName == "Menus" then
			menus(UIKit, theme, gui)
		elseif screenName == "Feedback" then
			feedback(UIKit, theme, gui)
		else
			error("unknown showcase screen " .. screenName)
		end
	end
	gui.Enabled = false
	gui:SetAttribute("ShowcaseTheme", themeName)
	gui:SetAttribute("ShowcaseScreen", screenName)
	gui.Parent = StarterGui
	return gui
end

function Showcase.buildTheme(UIKit: any, themeName: string)
	for _, screenName in Showcase.SCREENS do
		Showcase.build(UIKit, themeName, screenName)
		task.wait()
	end
end

-- Enables one showcase screen, disables the rest, and fits strokes and grids to the current viewport
function Showcase.show(UIKit: any, themeName: string, screenName: string): string
	local target = "SC_" .. themeName .. "_" .. screenName
	local shown: ScreenGui? = nil
	for _, gui in StarterGui:GetChildren() do
		if gui:IsA("ScreenGui") and gui:GetAttribute("ShowcaseScreen") ~= nil then
			gui.Enabled = gui.Name == target
			if gui.Name == target then
				shown = gui
			end
		end
	end
	assert(shown, "no showcase screen " .. target)
	task.wait()
	fitToViewport(UIKit, shown)
	return target
end

return Showcase
```

- [ ] **Step 3: Install and re-run the rebuild test**

`multi_edit` `game.ServerStorage.UIKitDev.Showcase` (ModuleScript). Re-run Step 1's snippet. Expected: `PASS rebuild safety`.

- [ ] **Step 4: Build a backdrop scene for screenshots**

`execute_luau` (Edit) once:

```lua
local old = workspace:FindFirstChild("ShowcaseBackdrop")
if old then
	old:Destroy()
end
local model = Instance.new("Model")
model.Name = "ShowcaseBackdrop"
local function block(name: string, size: Vector3, cf: CFrame, color: Color3, material: Enum.Material)
	local p = Instance.new("Part")
	p.Name = name
	p.Anchored = true
	p.Size = size
	p.CFrame = cf
	p.Color = color
	p.Material = material
	p.Parent = model
end
block("Arena", Vector3.new(120, 2, 120), CFrame.new(0, 1, -40), Color3.fromRGB(96, 104, 120), Enum.Material.Concrete)
for i = 1, 6 do
	local angle = math.rad(i * 60)
	block("Pillar" .. i, Vector3.new(6, 18 + i * 2, 6), CFrame.new(math.cos(angle) * 40, 10, -40 + math.sin(angle) * 40), Color3.fromRGB(70, 76, 90), Enum.Material.Slate)
end
block("Rock", Vector3.new(10, 8, 9), CFrame.new(0, 6, -30) * CFrame.Angles(0, 0.6, 0.2), Color3.fromRGB(120, 110, 100), Enum.Material.Rock)
model.Parent = workspace
local Lighting = game:GetService("Lighting")
Lighting.ClockTime = 15
Lighting.Brightness = 2.5
return "backdrop ready"
```

Screenshot camera for every capture: `camera_position: [0, 14, 10]`, `look_at_position: [0, 6, -30]`.

- [ ] **Step 5: Build the Stud Simulator screens and capture each**

`execute_luau` (Edit):

```lua
local RS, SS = game:GetService("ReplicatedStorage"), game:GetService("ServerStorage")
local UIKit = require(RS.UIKit:Clone())
local Showcase = require(SS.UIKitDev.Showcase:Clone())
Showcase.buildTheme(UIKit, "StudSimulator")
return "built"
```

Then for each screen in `HUD, Menus, Loading, MainMenu, Feedback`: run

```lua
local RS, SS = game:GetService("ReplicatedStorage"), game:GetService("ServerStorage")
return require(SS.UIKitDev.Showcase:Clone()).show(require(RS.UIKit:Clone()), "StudSimulator", "HUD")
```

(swap the screen name), then `screen_capture` with capture_id `Stud_<Screen>` and the camera from Step 4. Copy each saved capture file (the `source:` path in the tool result) to `roblox-ui/screenshots/stud-simulator-<screen lowercase>.jpg` with `cp`.

- [ ] **Step 6: Critique against the reference**

For each screenshot check, and fix in the theme or component before continuing:
- Every text has its dark outline; nothing is clipped at the panel edge.
- The title tab overhangs the panel's top-left, its icon breaks out of the tab, and the X overhangs the top-right.
- Buttons show a 3-stop vertical gradient plus gloss streaks; no flat-looking buttons.
- Studs (dot tile) visible but quiet on panels; not on small buttons.
- Inventory cells are square and evenly spaced (pixel grid applied).
- HUD layout matches Lift a Rock zones: currencies top-left, 2×2 menu buttons left, Spawn/Home top-centre, offer top-right, level bar bottom-centre.

- [ ] **Step 7: User checkpoint**

Send the five screenshots with `SendUserFile` and ask the user whether Stud Simulator looks right before the other five themes reuse the same components. Apply their feedback (re-run Steps 5–6) before Task 9. Do not start Task 9 without their go-ahead.

- [ ] **Step 8: Commit**

```bash
git add roblox-ui/kit/dev/Showcase.luau roblox-ui/screenshots/stud-simulator-*.jpg
git commit -m "feat: add showcase builder and Stud Simulator screens"
```

### Task 9: Battlegrounds theme

**Files:**
- Create: `roblox-ui/kit/Themes/Battlegrounds.luau`, `roblox-ui/screenshots/battlegrounds-*.jpg`
- Modify: `roblox-ui/kit/dev/KitCheck.luau` (EXPECTED_THEMES)
- Install: `game.ReplicatedStorage.UIKit.Themes.Battlegrounds`, re-install `game.ServerStorage.UIKitDev.KitCheck`

**Interfaces:**
- Consumes: theme table shape from Task 4; `Decor.slash / vignette`, `Util.make`.
- Produces: theme `Battlegrounds` (hudLayout `combat`, barStyle `split`, header `strip`, chamfer 12).

- [ ] **Step 1: Make KitCheck expect the theme (red)**

In `roblox-ui/kit/dev/KitCheck.luau` set `KitCheck.EXPECTED_THEMES = { "StudSimulator", "Battlegrounds" }`, re-install it with `multi_edit` (replace the whole source), run KitCheck.
Expected: `KitCheck: 36 passed, 1 failed` with `- theme Battlegrounds exists: no theme module named Battlegrounds`.

- [ ] **Step 2: Write `roblox-ui/kit/Themes/Battlegrounds.luau`**

```lua
--!strict
-- Battlegrounds: flat charcoal tiles, one hot accent, a split vitals bar with an emblem, cut-corner menus.
-- Built from The Strongest Battlegrounds / Jujutsu Shenanigans move tiles and Type Soul's split bar.

local Decor = require(script.Parent.Parent.Decor)
local Util = require(script.Parent.Parent.Util)

local hex = Color3.fromHex
local BLACK = hex("000000")
local WHITE = hex("FFFFFF")
local TEXT = hex("F4F4F4")
local RED = { hex("FF4B55"), hex("C3121D") }

local function flat(color: string, transparency: number)
	return { fill = { hex(color) }, fillTransparency = transparency, text = TEXT, edge = BLACK, textStroke = BLACK }
end

return {
	name = "Battlegrounds",
	hudLayout = "combat",
	color = {
		backdrop = hex("0E0F12"),
		base = hex("121419"),
		baseTransparency = 0.12,
		surface = hex("3A3D45"),
		surfaceTransparency = 0.35,
		rim = hex("5B606C"),
		barEdge = BLACK,
		text = TEXT,
		textMuted = hex("A9ADB8"),
		textStroke = BLACK,
		track = hex("0B0C0F"),
		header = RED,
		variants = {
			primary = { fill = RED, fillTransparency = 0, text = WHITE, edge = BLACK, textStroke = hex("3A0004") },
			secondary = flat("3A3D45", 0.3),
			success = { fill = { hex("3DDC84"), hex("1E9E57") }, fillTransparency = 0, text = WHITE, edge = BLACK, textStroke = hex("06301A") },
			danger = { fill = RED, fillTransparency = 0, text = WHITE, edge = BLACK, textStroke = hex("3A0004") },
			ghost = flat("000000", 0.55),
		},
		bars = {
			health = { hex("6BFF9E"), hex("1FB85A") },
			energy = { hex("4FE3FF"), hex("1186C9") },
			xp = { WHITE, hex("BFC4CF") },
			accent = RED,
		},
	},
	font = {
		display = Font.fromEnum(Enum.Font.BuilderSansExtraBold),
		body = Font.fromEnum(Enum.Font.BuilderSansBold),
		number = Font.fromEnum(Enum.Font.GothamBlack),
	},
	textStroke = { display = 1.5, body = 1 },
	stroke = { panel = 1.5, control = 1, slot = 1 },
	radius = { panel = UDim.new(0, 4), control = UDim.new(0, 4), slot = UDim.new(0, 3), pill = UDim.new(0.5, 0) },
	shape = {
		chamfer = 12, slantButtons = false, tilt = 0, header = "strip", iconFrame = true, gradientText = false, barStyle = "split",
	},
	motion = {
		style = "slide", easing = Enum.EasingStyle.Quad, fast = 0.08, normal = 0.12, slow = 0.25,
		pressScale = 0.95, openFrom = 0.97, worldBlur = 6,
	},
	assets = {},
	decorate = {
		-- the cut corners and the red strip header carry the panel look
		panel = function(_main: Frame, _theme: any) end,
		header = function(_tab: Frame, _theme: any) end,
		button = function(_button: GuiObject, _theme: any, _variant: string) end,
		slot = function(slot: GuiObject, theme: any)
			Util.make("Frame", {
				Name = "Accent", BackgroundColor3 = theme.color.bars.accent[1], BorderSizePixel = 0, AnchorPoint = Vector2.new(0.5, 1),
				Position = UDim2.fromScale(0.5, 1), Size = UDim2.new(0.5, 0, 0, 2), ZIndex = 8, Parent = slot,
			})
		end,
		bar = function(_bar: Frame, _theme: any) end,
		screen = function(background: Frame, theme: any, _kind: string)
			Decor.slash(background, theme.color.bars.accent[2], -14, {
				Position = UDim2.fromScale(0.5, 0.42), Size = UDim2.fromScale(1.6, 0.16), Transparency = 0.2,
			})
			Decor.slash(background, theme.color.bars.accent[1], -14, { Position = UDim2.fromScale(0.5, 0.52), Size = UDim2.fromScale(1.6, 0.012) })
			Decor.vignette(background, BLACK, 0.85)
		end,
	},
}
```

- [ ] **Step 3: Install and run KitCheck (green)**

`multi_edit` `game.ReplicatedStorage.UIKit.Themes.Battlegrounds` (ModuleScript). Run KitCheck.
Expected: `KitCheck: 68 passed, 0 failed`.

- [ ] **Step 4: Build, capture, critique**

`execute_luau` (Edit):

```lua
local RS, SS = game:GetService("ReplicatedStorage"), game:GetService("ServerStorage")
require(SS.UIKitDev.Showcase:Clone()).buildTheme(require(RS.UIKit:Clone()), "Battlegrounds")
return "built"
```

For each of `HUD, Menus, Loading, MainMenu, Feedback`: run `return require(game.ServerStorage.UIKitDev.Showcase:Clone()).show(require(game.ReplicatedStorage.UIKit:Clone()), "Battlegrounds", "<Screen>")`, `screen_capture` (capture_id `Battlegrounds_<Screen>`, camera `[0, 14, 10]` → `[0, 6, -30]`), and `cp` the capture to `roblox-ui/screenshots/battlegrounds-<screen lowercase>.jpg`.

Check and fix before continuing:
- Move tiles: four numbered charcoal squares, white names, a red underline, tile 3 with a cooldown shade, tile 1 highlighted.
- The split bar reads green-left / blue-right with a diamond emblem and segment ticks; the slanted red "MAXIMUM OUTPUT" banner sits above it.
- Menus have cut corners on all four corners with a continuous grey rim (Path2D); a red strip title sits inside the top-left.
- Mobile buttons are round, translucent, bottom-right; nothing overlaps the move tiles.
- No text outline thicker than ~1.5 px; this style is flat, not chunky.

- [ ] **Step 5: Commit**

```bash
git add roblox-ui/kit/Themes/Battlegrounds.luau roblox-ui/kit/dev/KitCheck.luau roblox-ui/screenshots/battlegrounds-*.jpg
git commit -m "feat: add Battlegrounds theme"
```

### Task 10: Kinetic Comic theme

**Files:**
- Create: `roblox-ui/kit/Themes/KineticComic.luau`, `roblox-ui/screenshots/kinetic-comic-*.jpg`
- Modify: `roblox-ui/kit/dev/KitCheck.luau` (EXPECTED_THEMES)
- Install: `game.ReplicatedStorage.UIKit.Themes.KineticComic`, re-install KitCheck

**Interfaces:**
- Consumes: `Decor.hardShadow / burst / slant / dots / slash`, `Util.make`; Button's `shape.slantButtons` path.
- Produces: theme `KineticComic` (slant buttons, tilt -2, motion `slam`).

- [ ] **Step 1: Make KitCheck expect the theme (red)**

Set `KitCheck.EXPECTED_THEMES = { "StudSimulator", "Battlegrounds", "KineticComic" }`, re-install KitCheck, run it.
Expected: `KitCheck: 68 passed, 1 failed` with `- theme KineticComic exists: no theme module named KineticComic`.

- [ ] **Step 2: Write `roblox-ui/kit/Themes/KineticComic.luau`**

```lua
--!strict
-- Kinetic Comic: red, black and white only. Slanted buttons, tilted panels, hard offset shadows, starbursts
-- behind titles, halftone dots and slam-in motion.

local Decor = require(script.Parent.Parent.Decor)
local Util = require(script.Parent.Parent.Util)

local hex = Color3.fromHex
local RED = hex("E5001A")
local BLACK = hex("0A0A0A")
local WHITE = hex("FFFFFF")
local YELLOW = hex("FFE600")
local NO_RADIUS = UDim.new(0, 0)

return {
	name = "KineticComic",
	hudLayout = "combat",
	color = {
		backdrop = RED,
		base = RED,
		baseTransparency = 0,
		surface = hex("111111"),
		surfaceTransparency = 0,
		rim = BLACK,
		barEdge = BLACK,
		text = WHITE,
		textMuted = hex("FFD0D5"),
		textStroke = BLACK,
		track = BLACK,
		header = { BLACK },
		variants = {
			primary = { fill = { WHITE }, fillTransparency = 0, text = BLACK, edge = BLACK, textStroke = WHITE },
			secondary = { fill = { BLACK }, fillTransparency = 0, text = WHITE, edge = WHITE, textStroke = BLACK },
			success = { fill = { YELLOW }, fillTransparency = 0, text = BLACK, edge = BLACK, textStroke = YELLOW },
			danger = { fill = { BLACK }, fillTransparency = 0, text = RED, edge = RED, textStroke = BLACK },
			ghost = { fill = { BLACK }, fillTransparency = 0.25, text = WHITE, edge = WHITE, textStroke = BLACK },
		},
		bars = { health = { RED }, energy = { WHITE }, xp = { YELLOW }, accent = { RED } },
	},
	font = {
		display = Font.fromEnum(Enum.Font.Bangers),
		body = Font.fromEnum(Enum.Font.GothamBlack),
		number = Font.fromEnum(Enum.Font.Bangers),
	},
	textStroke = { display = 3, body = 0 },
	stroke = { panel = 5, control = 3, slot = 3 },
	radius = { panel = NO_RADIUS, control = NO_RADIUS, slot = NO_RADIUS, pill = NO_RADIUS },
	shape = {
		chamfer = 0, slantButtons = true, tilt = -2, header = "tab", iconFrame = true, gradientText = false, barStyle = "single",
	},
	motion = {
		style = "slam", easing = Enum.EasingStyle.Back, fast = 0.07, normal = 0.16, slow = 0.3,
		pressScale = 0.92, openFrom = 1.1, worldBlur = 0,
	},
	assets = {},
	decorate = {
		panel = function(main: Frame, _theme: any)
			Decor.hardShadow(main, BLACK, Vector2.new(12, 12))
		end,
		header = function(tab: Frame, _theme: any)
			tab.Rotation = -6
			-- the tab's own fill goes transparent so a white starburst can sit behind a black box
			tab.BackgroundTransparency = 1
			Decor.burst(tab, WHITE, 12, 2.2)
			Util.make("Frame", { Name = "Box", BackgroundColor3 = BLACK, BorderSizePixel = 0, Size = UDim2.fromScale(1, 1), ZIndex = 1, Parent = tab })
		end,
		-- Button already slants itself because shape.slantButtons is on
		button = function(_button: GuiObject, _theme: any, _variant: string) end,
		slot = function(slot: GuiObject, _theme: any)
			Decor.hardShadow(slot, WHITE, Vector2.new(4, 4))
		end,
		bar = function(bar: Frame, _theme: any)
			Decor.slant(bar)
		end,
		screen = function(background: Frame, _theme: any, _kind: string)
			Decor.dots(background, BLACK, 0.8, 14, { Size = UDim2.fromScale(0.6, 1), Fade = 0 })
			Decor.slash(background, BLACK, -18, { Position = UDim2.fromScale(0.62, 0.55), Size = UDim2.fromScale(1.4, 0.28) })
			Decor.slash(background, WHITE, -18, { Position = UDim2.fromScale(0.62, 0.38), Size = UDim2.fromScale(1.4, 0.015) })
		end,
	},
}
```

- [ ] **Step 3: Install and run KitCheck (green)**

`multi_edit` `game.ReplicatedStorage.UIKit.Themes.KineticComic`. Run KitCheck.
Expected: `KitCheck: 100 passed, 0 failed`.

- [ ] **Step 4: Build, capture, critique**

`execute_luau` (Edit):

```lua
local RS, SS = game:GetService("ReplicatedStorage"), game:GetService("ServerStorage")
require(SS.UIKitDev.Showcase:Clone()).buildTheme(require(RS.UIKit:Clone()), "KineticComic")
return "built"
```

For each screen: `show(…, "KineticComic", "<Screen>")`, `screen_capture` (capture_id `KineticComic_<Screen>`, same camera), `cp` to `roblox-ui/screenshots/kinetic-comic-<screen lowercase>.jpg`.

Check and fix before continuing:
- Only red, black, white (and yellow for "success" accents). No gradients, no rounded corners anywhere.
- Buttons are parallelograms leaning right; their labels stay inside the slant.
- Panel titles: black box rotated about -6° with a white starburst peeking around it.
- The reward popup's panel is tilted -2°; Shop, Inventory and Settings stay level because they scroll (rotation switches off clipping).
- Hard black shadow offset down-right on every panel; slots show a white offset shadow.
- Loading/menu background: red with halftone dots fading left to right and a black diagonal band.

- [ ] **Step 5: Commit**

```bash
git add roblox-ui/kit/Themes/KineticComic.luau roblox-ui/kit/dev/KitCheck.luau roblox-ui/screenshots/kinetic-comic-*.jpg
git commit -m "feat: add Kinetic Comic theme"
```

### Task 11: Cyber Holo theme

**Files:**
- Create: `roblox-ui/kit/Themes/CyberHolo.luau`, `roblox-ui/screenshots/cyber-holo-*.jpg`
- Modify: `roblox-ui/kit/dev/KitCheck.luau` (EXPECTED_THEMES)
- Install: `game.ReplicatedStorage.UIKit.Themes.CyberHolo`, re-install KitCheck

**Interfaces:**
- Consumes: `Decor.brackets / scanlines / glow / glass / ticks / vignette / slash`; chamfered panels (shape.chamfer 16).
- Produces: theme `CyberHolo` (barStyle `segmented`, motion `flicker`).

- [ ] **Step 1: Make KitCheck expect the theme (red)**

Set `KitCheck.EXPECTED_THEMES = { "StudSimulator", "Battlegrounds", "KineticComic", "CyberHolo" }`, re-install, run.
Expected: `KitCheck: 100 passed, 1 failed` with `- theme CyberHolo exists: no theme module named CyberHolo`.

- [ ] **Step 2: Write `roblox-ui/kit/Themes/CyberHolo.luau`**

```lua
--!strict
-- Cyber Holo: near-black glass, cyan and magenta neon, cut corners, HUD brackets, scanlines and flicker-in motion.

local Decor = require(script.Parent.Parent.Decor)

local hex = Color3.fromHex
local CYAN = hex("2EF2FF")
local MAGENTA = hex("FF2E88")
local INK = hex("05070D")
local NO_RADIUS = UDim.new(0, 0)

return {
	name = "CyberHolo",
	hudLayout = "combat",
	color = {
		backdrop = INK,
		base = hex("071019"),
		baseTransparency = 0.12,
		surface = hex("0B1B2A"),
		surfaceTransparency = 0.2,
		rim = CYAN,
		barEdge = hex("1E6F7A"),
		text = hex("D8FDFF"),
		textMuted = hex("5FA7B3"),
		textStroke = INK,
		track = hex("04121A"),
		header = { MAGENTA, hex("B3125C") },
		variants = {
			primary = { fill = { CYAN, hex("12A9C9") }, fillTransparency = 0, text = hex("02161C"), edge = hex("B8FCFF"), textStroke = INK },
			secondary = { fill = { hex("0B1B2A") }, fillTransparency = 0.1, text = CYAN, edge = CYAN, textStroke = INK },
			success = { fill = { hex("39FF9E"), hex("12B86B") }, fillTransparency = 0, text = hex("021A0E"), edge = hex("B8FFDA"), textStroke = INK },
			danger = { fill = { MAGENTA, hex("B3125C") }, fillTransparency = 0, text = hex("FFFFFF"), edge = hex("FFB8D6"), textStroke = INK },
			ghost = { fill = { INK }, fillTransparency = 0.5, text = CYAN, edge = CYAN, textStroke = INK },
		},
		bars = {
			health = { hex("39FF9E"), hex("12B86B") },
			energy = { CYAN, hex("12A9C9") },
			xp = { MAGENTA, hex("B3125C") },
			accent = { hex("FFE14D"), hex("D9A400") },
		},
	},
	font = {
		display = Font.fromEnum(Enum.Font.Michroma),
		body = Font.fromName("Sarpanch", Enum.FontWeight.Bold),
		number = Font.fromName("RobotoMono", Enum.FontWeight.Bold),
	},
	textStroke = { display = 0, body = 0 },
	stroke = { panel = 1.5, control = 1.5, slot = 1 },
	radius = { panel = NO_RADIUS, control = NO_RADIUS, slot = NO_RADIUS, pill = NO_RADIUS },
	shape = {
		chamfer = 16, slantButtons = false, tilt = 0, header = "strip", iconFrame = true, gradientText = false, barStyle = "segmented",
	},
	motion = {
		style = "flicker", easing = Enum.EasingStyle.Quad, fast = 0.06, normal = 0.14, slow = 0.3,
		pressScale = 0.96, openFrom = 0.98, worldBlur = 8,
	},
	assets = {},
	decorate = {
		panel = function(main: Frame, _theme: any)
			Decor.brackets(main, CYAN, 22, 2, 5)
			Decor.scanlines(main, CYAN, 0.94, 4, 110)
			Decor.glow(main, CYAN, 18)
			Decor.glass(main)
		end,
		header = function(tab: Frame, _theme: any)
			Decor.ticks(tab, CYAN, 16)
		end,
		button = function(button: GuiObject, _theme: any, variant: string)
			if variant ~= "icon" then
				Decor.brackets(button, CYAN, 8, 1.5, 3)
			end
		end,
		slot = function(slot: GuiObject, _theme: any)
			Decor.brackets(slot, CYAN, 8, 1.5, 2)
		end,
		bar = function(bar: Frame, _theme: any)
			Decor.glow(bar, CYAN, 10)
		end,
		screen = function(background: Frame, _theme: any, _kind: string)
			Decor.scanlines(background, CYAN, 0.95, 3, 300)
			Decor.vignette(background, INK, 0.9)
			Decor.slash(background, MAGENTA, 0, { Position = UDim2.fromScale(0.5, 0.6), Size = UDim2.new(1, 0, 0, 2), Transparency = 0.3 })
		end,
	},
}
```

- [ ] **Step 3: Install and run KitCheck (green)**

`multi_edit` `game.ReplicatedStorage.UIKit.Themes.CyberHolo`. Run KitCheck.
Expected: `KitCheck: 132 passed, 0 failed`.

- [ ] **Step 4: Build, capture, critique**

`execute_luau` (Edit):

```lua
local RS, SS = game:GetService("ReplicatedStorage"), game:GetService("ServerStorage")
require(SS.UIKitDev.Showcase:Clone()).buildTheme(require(RS.UIKit:Clone()), "CyberHolo")
return "built"
```

For each screen: `show(…, "CyberHolo", "<Screen>")`, `screen_capture` (capture_id `CyberHolo_<Screen>`, same camera), `cp` to `roblox-ui/screenshots/cyber-holo-<screen lowercase>.jpg`.

Check and fix before continuing:
- Panels: cut corners with a thin cyan rim, cyan L-brackets just outside each corner, faint scanlines over everything, a magenta strip title with a tick ruler under it.
- Glow: if `UIShadow` renders, a soft cyan halo around panels and bars. If the halo shows as a hard rectangle around the chamfered panel (the frame's own background is transparent), remove `Decor.glow` from `decorate.panel` and keep it only on bars.
- Text is Michroma (wide caps) for titles, Sarpanch for body, RobotoMono for numbers. No text outlines.
- Bars are segmented (ticks every twelfth), green HP and cyan energy.
- Scanline holder never blocks clicks (it is a plain Frame); confirm a button under it still presses in Play.

- [ ] **Step 5: Commit**

```bash
git add roblox-ui/kit/Themes/CyberHolo.luau roblox-ui/kit/dev/KitCheck.luau roblox-ui/screenshots/cyber-holo-*.jpg
git commit -m "feat: add Cyber Holo theme"
```

### Task 12: Manga Ink theme

**Files:**
- Create: `roblox-ui/kit/Themes/MangaInk.luau`, `roblox-ui/screenshots/manga-ink-*.jpg`
- Modify: `roblox-ui/kit/dev/KitCheck.luau` (EXPECTED_THEMES)
- Install: `game.ReplicatedStorage.UIKit.Themes.MangaInk`, re-install KitCheck

**Interfaces:**
- Consumes: `Decor.ink / dots / hardShadow / speedlines`.
- Produces: theme `MangaInk` (paper and ink, motion `stamp`, tilt 1.5).

- [ ] **Step 1: Make KitCheck expect the theme (red)**

Set `KitCheck.EXPECTED_THEMES = { "StudSimulator", "Battlegrounds", "KineticComic", "CyberHolo", "MangaInk" }`, re-install, run.
Expected: `KitCheck: 132 passed, 1 failed` with `- theme MangaInk exists: no theme module named MangaInk`.

- [ ] **Step 2: Write `roblox-ui/kit/Themes/MangaInk.luau`**

```lua
--!strict
-- Manga Ink: paper white and ink black with one red spot colour. Off-register ink outlines, screentone dots,
-- speed lines and panels that "stamp" in.

local Decor = require(script.Parent.Parent.Decor)

local hex = Color3.fromHex
local INK = hex("111111")
local PAPER = hex("FFFFFF")
local RED = hex("E8212B")

return {
	name = "MangaInk",
	hudLayout = "combat",
	color = {
		backdrop = hex("F4F1EA"),
		base = PAPER,
		baseTransparency = 0,
		surface = PAPER,
		surfaceTransparency = 0,
		rim = INK,
		barEdge = INK,
		text = INK,
		textMuted = hex("4A4A4A"),
		-- white outline keeps ink text readable over the 3D world
		textStroke = PAPER,
		track = hex("E6E2DA"),
		-- title boxes are paper with an ink border; an ink box would hide ink text
		header = { PAPER },
		variants = {
			primary = { fill = { INK }, fillTransparency = 0, text = PAPER, edge = INK, textStroke = INK },
			secondary = { fill = { PAPER }, fillTransparency = 0, text = INK, edge = INK, textStroke = PAPER },
			success = { fill = { PAPER }, fillTransparency = 0, text = INK, edge = INK, textStroke = PAPER },
			danger = { fill = { RED }, fillTransparency = 0, text = PAPER, edge = INK, textStroke = INK },
			ghost = { fill = { PAPER }, fillTransparency = 0.15, text = INK, edge = INK, textStroke = PAPER },
		},
		bars = { health = { RED }, energy = { INK }, xp = { hex("5A5A5A") }, accent = { RED } },
	},
	font = {
		display = Font.fromEnum(Enum.Font.Bangers),
		body = Font.fromName("Kalam", Enum.FontWeight.Bold),
		number = Font.fromEnum(Enum.Font.Bangers),
	},
	textStroke = { display = 2, body = 0 },
	stroke = { panel = 4, control = 3, slot = 3 },
	radius = { panel = UDim.new(0, 2), control = UDim.new(0, 2), slot = UDim.new(0, 2), pill = UDim.new(0.5, 0) },
	shape = {
		chamfer = 0, slantButtons = false, tilt = 1.5, header = "tab", iconFrame = true, gradientText = false, barStyle = "single",
	},
	motion = {
		style = "stamp", easing = Enum.EasingStyle.Linear, fast = 0.05, normal = 0.1, slow = 0.25,
		pressScale = 0.9, openFrom = 1.15, worldBlur = 0,
	},
	assets = {},
	decorate = {
		panel = function(main: Frame, _theme: any)
			Decor.ink(main, INK, 2, 5)
			Decor.dots(main, INK, 0.75, 8, {
				Size = UDim2.fromScale(0.5, 0.45), Position = UDim2.fromScale(1, 1), AnchorPoint = Vector2.new(1, 1), Fade = 225,
			})
			Decor.hardShadow(main, INK, Vector2.new(8, 8))
		end,
		header = function(tab: Frame, _theme: any)
			tab.Rotation = -3
		end,
		button = function(button: GuiObject, _theme: any, variant: string)
			if variant ~= "icon" then
				Decor.hardShadow(button, INK, Vector2.new(4, 4))
			end
		end,
		slot = function(slot: GuiObject, _theme: any)
			Decor.ink(slot, INK, 1.5, 3)
		end,
		bar = function(_bar: Frame, _theme: any) end,
		screen = function(background: Frame, _theme: any, _kind: string)
			Decor.speedlines(background, INK, 56)
			Decor.dots(background, INK, 0.82, 10, {
				Size = UDim2.fromScale(0.45, 0.5), Position = UDim2.fromScale(0, 1), AnchorPoint = Vector2.new(0, 1), Fade = -45,
			})
		end,
	},
}
```

- [ ] **Step 3: Install and run KitCheck (green)**

`multi_edit` `game.ReplicatedStorage.UIKit.Themes.MangaInk`. Run KitCheck.
Expected: `KitCheck: 164 passed, 0 failed`.

- [ ] **Step 4: Build, capture, critique**

`execute_luau` (Edit):

```lua
local RS, SS = game:GetService("ReplicatedStorage"), game:GetService("ServerStorage")
require(SS.UIKitDev.Showcase:Clone()).buildTheme(require(RS.UIKit:Clone()), "MangaInk")
return "built"
```

For each screen: `show(…, "MangaInk", "<Screen>")`, `screen_capture` (capture_id `MangaInk_<Screen>`, same camera), `cp` to `roblox-ui/screenshots/manga-ink-<screen lowercase>.jpg`.

Check and fix before continuing:
- Paper-white panels, thick ink borders with a second thin outline slightly off-register, a dot-screentone patch fading out from the bottom-right corner.
- Every label readable: ink text on paper, or white-outlined ink text over the 3D world (HUD player name, damage numbers, splash).
- Buttons cast a hard ink shadow; the danger X is red.
- Loading/menu: speed lines radiating from the centre and screentone in the bottom-left; title in Bangers.
- Red only for health, danger and accents.

- [ ] **Step 5: Commit**

```bash
git add roblox-ui/kit/Themes/MangaInk.luau roblox-ui/kit/dev/KitCheck.luau roblox-ui/screenshots/manga-ink-*.jpg
git commit -m "feat: add Manga Ink theme"
```

### Task 13: Dark Fantasy theme

**Files:**
- Create: `roblox-ui/kit/Themes/DarkFantasy.luau`, `roblox-ui/screenshots/dark-fantasy-*.jpg`
- Modify: `roblox-ui/kit/dev/KitCheck.luau` (EXPECTED_THEMES)
- Install: `game.ReplicatedStorage.UIKit.Themes.DarkFantasy`, re-install KitCheck

**Interfaces:**
- Consumes: `Decor.ornate / shadow / divider / vignette / embers`, `Util.make / stroke`.
- Produces: theme `DarkFantasy` (header `center`, motion `fade`).

- [ ] **Step 1: Make KitCheck expect the theme (red)**

Set `KitCheck.EXPECTED_THEMES = { "StudSimulator", "Battlegrounds", "KineticComic", "CyberHolo", "MangaInk", "DarkFantasy" }`, re-install, run.
Expected: `KitCheck: 164 passed, 1 failed` with `- theme DarkFantasy exists: no theme module named DarkFantasy`.

- [ ] **Step 2: Write `roblox-ui/kit/Themes/DarkFantasy.luau`**

```lua
--!strict
-- Dark Fantasy: black, crimson and antique gold with parchment text. Thin double frames with corner gems,
-- gothic titles over a jewelled divider, embers, and slow fades. Built from Ghoul://Re and Deepwoken.

local Decor = require(script.Parent.Parent.Decor)
local Util = require(script.Parent.Parent.Util)

local hex = Color3.fromHex
local GOLD = hex("B8954A")
local DIM_GOLD = hex("6E5A33")
local PARCHMENT = hex("EDE3CF")
local BLACK = hex("000000")
local EMBER = hex("FF7A2E")
local CRIMSON = { hex("9E2430"), hex("5A0E14") }
local NO_RADIUS = UDim.new(0, 0)

local function innerLine(parent: GuiObject, insetPx: number, transparency: number)
	local inner = Util.make("Frame", {
		Name = "InnerLine", BackgroundTransparency = 1, AnchorPoint = Vector2.new(0.5, 0.5), Position = UDim2.fromScale(0.5, 0.5),
		Size = UDim2.new(1, -2 * insetPx, 1, -2 * insetPx), ZIndex = 4, Parent = parent,
	})
	Util.stroke(inner, GOLD, 1, transparency)
end

return {
	name = "DarkFantasy",
	hudLayout = "combat",
	color = {
		backdrop = hex("07060A"),
		base = hex("120E10"),
		baseTransparency = 0.06,
		surface = hex("1E1618"),
		surfaceTransparency = 0.1,
		rim = GOLD,
		barEdge = DIM_GOLD,
		text = PARCHMENT,
		textMuted = hex("9C8F7A"),
		textStroke = BLACK,
		track = hex("0C0809"),
		header = { hex("2A2124"), hex("17110F") },
		variants = {
			primary = { fill = CRIMSON, fillTransparency = 0, text = PARCHMENT, edge = GOLD, textStroke = hex("1A0507") },
			secondary = { fill = { hex("2A2124"), hex("17110F") }, fillTransparency = 0, text = PARCHMENT, edge = DIM_GOLD, textStroke = BLACK },
			success = { fill = { hex("4A6B3E"), hex("23381C") }, fillTransparency = 0, text = PARCHMENT, edge = GOLD, textStroke = BLACK },
			danger = { fill = CRIMSON, fillTransparency = 0, text = PARCHMENT, edge = GOLD, textStroke = hex("1A0507") },
			ghost = { fill = { BLACK }, fillTransparency = 0.5, text = PARCHMENT, edge = DIM_GOLD, textStroke = BLACK },
		},
		bars = {
			health = { hex("D2333D"), hex("7A0F17") },
			energy = { hex("E2AE4A"), hex("9C6B1C") },
			xp = { GOLD, hex("7A6230") },
			accent = { hex("8C6AD9"), hex("4A3290") },
		},
	},
	font = {
		display = Font.fromEnum(Enum.Font.GrenzeGotisch),
		body = Font.fromEnum(Enum.Font.Merriweather),
		number = Font.fromName("Merriweather", Enum.FontWeight.Bold),
	},
	textStroke = { display = 1.5, body = 1 },
	stroke = { panel = 1.5, control = 1, slot = 1 },
	radius = { panel = NO_RADIUS, control = NO_RADIUS, slot = NO_RADIUS, pill = NO_RADIUS },
	shape = {
		chamfer = 0, slantButtons = false, tilt = 0, header = "center", iconFrame = true, gradientText = false, barStyle = "single",
	},
	motion = {
		style = "fade", easing = Enum.EasingStyle.Sine, fast = 0.12, normal = 0.35, slow = 0.6,
		pressScale = 0.97, openFrom = 0.96, worldBlur = 10,
	},
	assets = {},
	decorate = {
		panel = function(main: Frame, _theme: any)
			Decor.ornate(main, GOLD, 6, 10)
			Decor.shadow(main, BLACK, Vector2.new(0, 8), 28, 0.35)
		end,
		header = function(tab: Frame, _theme: any)
			-- the title floats over the panel with a jewelled divider instead of sitting in a box
			tab.BackgroundTransparency = 1
			local edge = tab:FindFirstChild("Edge")
			if edge then
				edge:Destroy()
			end
			Decor.divider(tab, GOLD)
		end,
		button = function(button: GuiObject, _theme: any, variant: string)
			if variant ~= "icon" and variant ~= "ghost" then
				innerLine(button, 3, 0.55)
			end
		end,
		slot = function(slot: GuiObject, _theme: any)
			innerLine(slot, 3, 0.7)
		end,
		bar = function(_bar: Frame, _theme: any) end,
		screen = function(background: Frame, _theme: any, _kind: string)
			Decor.vignette(background, BLACK, 0.95)
			Decor.embers(background, EMBER, 36)
		end,
	},
}
```

- [ ] **Step 3: Install and run KitCheck (green)**

`multi_edit` `game.ReplicatedStorage.UIKit.Themes.DarkFantasy`. Run KitCheck.
Expected: `KitCheck: 196 passed, 0 failed`.

- [ ] **Step 4: Build, capture, critique**

`execute_luau` (Edit):

```lua
local RS, SS = game:GetService("ReplicatedStorage"), game:GetService("ServerStorage")
require(SS.UIKitDev.Showcase:Clone()).buildTheme(require(RS.UIKit:Clone()), "DarkFantasy")
return "built"
```

For each screen: `show(…, "DarkFantasy", "<Screen>")`, `screen_capture` (capture_id `DarkFantasy_<Screen>`, same camera), `cp` to `roblox-ui/screenshots/dark-fantasy-<screen lowercase>.jpg`.

Check and fix before continuing:
- Square-cornered near-black panels with a gold outer rim, a fainter inner rim and gold diamond gems on the four corners.
- Centred gothic title (GrenzeGotisch) above a gold line that fades at both ends with a diamond in the middle; no title box.
- Crimson primary buttons with a faint gold inner line; parchment text everywhere.
- Health bar crimson, energy amber; HUD stays muted (no bright neon).
- Loading/menu: dark vignette with scattered ember specks.

- [ ] **Step 5: Commit**

```bash
git add roblox-ui/kit/Themes/DarkFantasy.luau roblox-ui/kit/dev/KitCheck.luau roblox-ui/screenshots/dark-fantasy-*.jpg
git commit -m "feat: add Dark Fantasy theme"
```

### Task 14: Play-mode showcase switcher

**Files:**
- Create: `roblox-ui/kit/dev/ShowcaseRuntime.client.luau`
- Install: `game.StarterPlayer.StarterPlayerScripts.ShowcaseRuntime` (LocalScript, showcase place only)

**Interfaces:**
- Consumes: `Motion.enter / loading / splash / toast / damage / cooldown / setBar`; ScreenGuis `SC_<Theme>_<Screen>` with `ShowcaseScreen` attributes (Task 8).
- Produces: in Play, Q/E cycles styles, 1–5 picks the screen, H hides the switcher, clickable chips for touch. Setting the PlayerGui attribute `ShowcaseTarget = "<Theme>/<Screen>"` switches too (used by the test below and by MCP-driven recording).

- [ ] **Step 1: Write the play test first**

Start play (`start_stop_play` true), then `execute_luau` (Client):

```lua
local pg = game:GetService("Players").LocalPlayer:WaitForChild("PlayerGui")
task.wait(2)
local function enabled(): string
	local names = {}
	for _, g in pg:GetChildren() do
		if g:IsA("ScreenGui") and g:GetAttribute("ShowcaseScreen") ~= nil and g.Enabled then
			table.insert(names, g.Name)
		end
	end
	table.sort(names)
	return table.concat(names, ",")
end
local first = enabled()
pg:SetAttribute("ShowcaseTarget", "CyberHolo/Menus")
task.wait(1)
local second = enabled()
local nav = pg:FindFirstChild("ShowcaseNav")
return string.format("first=%s second=%s nav=%s", first, second, tostring(nav ~= nil))
```

Expected now (no runtime yet): `first= second= nav=false`. Stop play.

- [ ] **Step 2: Write `roblox-ui/kit/dev/ShowcaseRuntime.client.luau`**

```lua
-- Play-mode switcher for the UI/UX showcase place. Q / E change style, 1–5 change screen, H hides the switcher.
-- Each screen replays its animations when it opens, so a screen recording shows the motion of every style.
-- Setting PlayerGui's "ShowcaseTarget" attribute to "<Theme>/<Screen>" switches too.

local Players = game:GetService("Players")
local ReplicatedStorage = game:GetService("ReplicatedStorage")
local UserInputService = game:GetService("UserInputService")

local Motion = require(ReplicatedStorage:WaitForChild("UIKit"):WaitForChild("Motion"))

local THEMES = { "StudSimulator", "Battlegrounds", "KineticComic", "CyberHolo", "MangaInk", "DarkFantasy" }
local SHORT_NAMES = { "Stud", "Battle", "Comic", "Cyber", "Manga", "Fantasy" }
local SCREENS = { "HUD", "Menus", "Loading", "MainMenu", "Feedback" }
local SCREEN_KEYS = { Enum.KeyCode.One, Enum.KeyCode.Two, Enum.KeyCode.Three, Enum.KeyCode.Four, Enum.KeyCode.Five }
local TOASTS = { { "Quest complete! +250 XP", "xp" }, { "x2 Luck active for 15:00", "accent" }, { "Not enough coins", "health" } }
local LOADING_SECONDS = 4
local DAMAGE_EVERY = 0.6
local HUD_LOOP_SECONDS = 3
local MOVE_COOLDOWN = 2.5
local BUTTON_STAGGER = 0.06
local TOAST_STAGGER = 0.3
local CHIP_IDLE = Color3.fromRGB(40, 40, 48)
local CHIP_ACTIVE = Color3.fromRGB(235, 235, 240)

local playerGui = (Players.LocalPlayer :: Player):WaitForChild("PlayerGui")
local themeIndex, screenIndex = 1, 1
local generation = 0 -- bumps on every switch so the previous screen's loops stop
local chips: { [string]: TextButton } = {}

local function replay(gui: ScreenGui, screenName: string, myGeneration: number)
	if screenName == "Menus" then
		for _, child in gui:GetChildren() do
			if child:IsA("GuiObject") and child:HasTag("UIKit.Panel") then
				Motion.enter(child)
			end
		end
	elseif screenName == "Loading" then
		task.spawn(function()
			while generation == myGeneration do
				Motion.loading(gui, LOADING_SECONDS)
				task.wait(LOADING_SECONDS + 1)
			end
		end)
	elseif screenName == "MainMenu" then
		local buttons = gui:FindFirstChild("Buttons", true)
		if buttons then
			for i, button in buttons:GetChildren() do
				if button:IsA("GuiObject") then
					task.delay(i * BUTTON_STAGGER, Motion.enter, button)
				end
			end
		end
	elseif screenName == "Feedback" then
		local splash = gui:FindFirstChild("LevelUp")
		if splash and splash:IsA("GuiObject") then
			Motion.splash(splash, 3)
		end
		local popup = gui:FindFirstChild("Reward")
		local main = popup and popup:FindFirstChild("Main")
		if main and main:IsA("GuiObject") then
			Motion.enter(main)
		end
		task.spawn(function()
			local stack = gui:FindFirstChild("Toasts")
			if stack then
				for _, toast in TOASTS do
					Motion.toast(stack, toast[1], toast[2], 4)
					task.wait(TOAST_STAGGER)
				end
			end
			local rng = Random.new(7)
			while generation == myGeneration do
				local at = UDim2.fromScale(rng:NextNumber(0.1, 0.3), rng:NextNumber(0.35, 0.65))
				Motion.damage(gui, at, rng:NextInteger(40, 2400), rng:NextNumber() < 0.25)
				task.wait(DAMAGE_EVERY)
			end
		end)
	elseif screenName == "HUD" then
		task.spawn(function()
			local moves = gui:FindFirstChild("Moves")
			local bar = gui:FindFirstChild("Vitals") or gui:FindFirstChild("LevelBar")
			while generation == myGeneration do
				local slot = moves and moves:FindFirstChild("Slot3")
				if slot then
					Motion.cooldown(slot, MOVE_COOLDOWN)
				end
				if bar then
					Motion.setBar(bar, 0.3 + math.random() * 0.7, if bar:FindFirstChild("Left") then "Left" else nil)
				end
				task.wait(HUD_LOOP_SECONDS)
			end
		end)
	end
end

local function show()
	generation += 1
	local themeName, screenName = THEMES[themeIndex], SCREENS[screenIndex]
	local target = "SC_" .. themeName .. "_" .. screenName
	for _, gui in playerGui:GetChildren() do
		if gui:IsA("ScreenGui") and gui:GetAttribute("ShowcaseScreen") ~= nil then
			gui.Enabled = gui.Name == target
		end
	end
	for key, chip in chips do
		local active = key == themeName or key == screenName
		chip.BackgroundColor3 = if active then CHIP_ACTIVE else CHIP_IDLE
		chip.TextColor3 = if active then CHIP_IDLE else CHIP_ACTIVE
	end
	local gui = playerGui:WaitForChild(target, 5)
	if gui and gui:IsA("ScreenGui") then
		replay(gui, screenName, generation)
	end
end

local function buildNav(): ScreenGui
	local nav = Instance.new("ScreenGui")
	nav.Name = "ShowcaseNav"
	nav.DisplayOrder = 100
	nav.ResetOnSpawn = false
	nav.ScreenInsets = Enum.ScreenInsets.CoreUISafeInsets
	local bar = Instance.new("Frame")
	bar.Name = "Bar"
	bar.AnchorPoint = Vector2.new(0.5, 0)
	bar.Position = UDim2.fromScale(0.5, 0.005)
	bar.Size = UDim2.fromScale(0.64, 0.07)
	bar.BackgroundColor3 = Color3.new(0, 0, 0)
	bar.BackgroundTransparency = 0.4
	bar.Parent = nav
	local corner = Instance.new("UICorner")
	corner.CornerRadius = UDim.new(0.3, 0)
	corner.Parent = bar
	local layout = Instance.new("UIListLayout")
	layout.FillDirection = Enum.FillDirection.Horizontal
	layout.HorizontalAlignment = Enum.HorizontalAlignment.Center
	layout.VerticalAlignment = Enum.VerticalAlignment.Center
	layout.Padding = UDim.new(0.004, 0)
	layout.SortOrder = Enum.SortOrder.LayoutOrder
	layout.Parent = bar
	local function chip(key: string, label: string, order: number, onClick: () -> ())
		local button = Instance.new("TextButton")
		button.Name = key
		button.Text = label
		button.TextScaled = true
		button.FontFace = Font.fromEnum(Enum.Font.BuilderSansBold)
		button.TextColor3 = CHIP_ACTIVE
		button.BackgroundColor3 = CHIP_IDLE
		button.Size = UDim2.fromScale(0.085, 0.78)
		button.LayoutOrder = order
		local round = Instance.new("UICorner")
		round.CornerRadius = UDim.new(0.3, 0)
		round.Parent = button
		local padding = Instance.new("UIPadding")
		padding.PaddingTop = UDim.new(0.18, 0)
		padding.PaddingBottom = UDim.new(0.18, 0)
		padding.Parent = button
		button.Activated:Connect(onClick)
		button.Parent = bar
		chips[key] = button
	end
	for i, themeName in THEMES do
		chip(themeName, SHORT_NAMES[i], i, function()
			themeIndex = i
			show()
		end)
	end
	for i, screenName in SCREENS do
		chip(screenName, screenName, 10 + i, function()
			screenIndex = i
			show()
		end)
	end
	nav.Parent = playerGui
	return nav
end

local nav = buildNav()

UserInputService.InputBegan:Connect(function(input, processed)
	if processed then
		return
	end
	if input.KeyCode == Enum.KeyCode.Q then
		themeIndex = (themeIndex - 2) % #THEMES + 1
		show()
	elseif input.KeyCode == Enum.KeyCode.E then
		themeIndex = themeIndex % #THEMES + 1
		show()
	elseif input.KeyCode == Enum.KeyCode.H then
		nav.Enabled = not nav.Enabled
	else
		local number = table.find(SCREEN_KEYS, input.KeyCode)
		if number then
			screenIndex = number
			show()
		end
	end
end)

playerGui:GetAttributeChangedSignal("ShowcaseTarget"):Connect(function()
	local target = playerGui:GetAttribute("ShowcaseTarget")
	if type(target) ~= "string" then
		return
	end
	local themeName, screenName = string.match(target, "^(%w+)/(%w+)$")
	local t = themeName and table.find(THEMES, themeName)
	local s = screenName and table.find(SCREENS, screenName)
	if t and s then
		themeIndex, screenIndex = t, s
		show()
	end
end)

show()
```

- [ ] **Step 3: Install and re-run the play test**

`multi_edit` `game.StarterPlayer.StarterPlayerScripts.ShowcaseRuntime` (LocalScript). Play, run Step 1's snippet on the Client.
Expected: `first=SC_StudSimulator_HUD second=SC_CyberHolo_Menus nav=true`.

- [ ] **Step 4: Watch each screen move**

Still in Play, for each theme set `ShowcaseTarget` to `<Theme>/Feedback` and `<Theme>/Menus`, wait 1 s, `screen_capture` (capture_id `Play_<Theme>_<Screen>`). Confirm toasts slide/pop in, damage numbers rise and fade, panels use the theme's entrance (pop, slide, slam, flicker, stamp, fade). Stop play.

- [ ] **Step 5: Commit**

```bash
git add roblox-ui/kit/dev/ShowcaseRuntime.client.luau
git commit -m "feat: add play-mode showcase switcher"
```

### Task 15: Phone pass (touch targets, safe areas, overflow)

**Files:**
- Modify: `roblox-ui/kit/dev/KitCheck.luau` (new case), `roblox-ui/kit/Util.luau` (`Util.minTouch`), `roblox-ui/kit/Controls.luau` (IconButton, Toggle), `roblox-ui/kit/Containers.luau` (Panel close button)
- Create: `roblox-ui/screenshots/mobile/<theme>-{hud,menus}.jpg`

**Interfaces:**
- Consumes: Studio device simulator (Roblox MCP skill `rbx-device-simulator-lua`).
- Produces: `Util.MIN_TOUCH = 44`, `Util.minTouch(button: GuiObject, aspect: number?)`.

- [ ] **Step 1: Add the failing KitCheck case**

Inside the per-theme loop of `KitCheck.run`, after the `MainMenu` case, add:

```lua
		build("touch targets", function()
			local holder = Instance.new("Folder")
			local iconButton = UIKit.IconButton(theme, { Icon = "🛒", Parent = holder })
			local main = UIKit.Panel(theme, { Title = "Shop", Body = "none", Parent = holder })
			local toggle = UIKit.Toggle(theme, { Parent = holder })
			for _, target in { iconButton, main:FindFirstChild("Close"), toggle } do
				local limit = target and target:FindFirstChildOfClass("UISizeConstraint")
				assert(limit and math.min(limit.MinSize.X, limit.MinSize.Y) >= 44,
					(if target then target.Name else "?") .. " can shrink below a 44 px touch target")
			end
			return holder
		end)
```

Re-install KitCheck, run it. Expected: `KitCheck: 196 passed, 6 failed`, one `touch targets` failure per theme.

- [ ] **Step 2: Add `Util.minTouch` and use it**

In `roblox-ui/kit/Util.luau`, after `Util.aspect`:

```lua
-- Keeps a tap target at least 44 px (the Apple and Google minimum) however small the screen scales it
Util.MIN_TOUCH = 44
function Util.minTouch(button: GuiObject, aspect: number?)
	Util.make("UISizeConstraint", { MinSize = Vector2.new(Util.MIN_TOUCH * math.max(1, aspect or 1), Util.MIN_TOUCH), Parent = button })
end
```

Then add one line in each builder:
- `Controls.IconButton`: `Util.minTouch(button)` right after `Util.aspect(button, 1)`.
- `Controls.Toggle`: `Util.minTouch(root, 2.1)` right after `Util.aspect(root, 2.1)`.
- `Containers.Panel`: `Util.minTouch(close)` right after `Util.aspect(close, 1)`.

Re-install Util, Controls, Containers. Run KitCheck. Expected: `KitCheck: 202 passed, 0 failed`.

- [ ] **Step 3: Switch Studio to a phone**

Load the Roblox MCP skill `rbx-device-simulator-lua` (`mcp__Roblox_Studio__skill`) and follow it to emulate a phone in landscape (an iPhone-class 844×390 device). Rebuild every theme's showcase so strokes and grids fit the new viewport:

```lua
local RS, SS = game:GetService("ReplicatedStorage"), game:GetService("ServerStorage")
local UIKit = require(RS.UIKit:Clone())
local Showcase = require(SS.UIKitDev.Showcase:Clone())
for _, name in UIKit.themeNames() do
	Showcase.buildTheme(UIKit, name)
	task.wait()
end
return "rebuilt"
```

- [ ] **Step 4: Audit each theme's HUD and Menus on the phone**

For each theme and each of `HUD`, `Menus`: `show(…)` then run:

```lua
local problems = {}
local function shown(inst: Instance): boolean
	local node: Instance? = inst
	while node and not node:IsA("ScreenGui") do
		if node:IsA("GuiObject") and not node.Visible then
			return false
		end
		node = node.Parent
	end
	return true
end
for _, gui in game:GetService("StarterGui"):GetChildren() do
	if gui:IsA("ScreenGui") and gui.Enabled then
		for _, d in gui:GetDescendants() do
			if d:IsA("GuiButton") and shown(d) and (d.AbsoluteSize.X < 44 or d.AbsoluteSize.Y < 44) then
				table.insert(problems, string.format("small target %s %dx%d", d:GetFullName(), d.AbsoluteSize.X, d.AbsoluteSize.Y))
			elseif d:IsA("TextLabel") and shown(d) and not d.TextFits then
				table.insert(problems, "text overflow " .. d:GetFullName())
			end
		end
	end
end
return if #problems == 0 then "0 problems" else table.concat(problems, "\n")
```

and `screen_capture` to `roblox-ui/screenshots/mobile/<theme>-<screen>.jpg`. Also look at the capture: nothing under the Roblox top-bar buttons or a notch.

- [ ] **Step 5: Fix every finding, then re-audit**

- A control under 44 px: give it `Util.minTouch`, or give it more of the layout (bigger `Size` share) in the showcase builder.
- Text overflow: shorten the copy or enlarge the label's container; never lower `MinTextSize` below 6.
- Overlaps at phone size: move the element to its zone in `ux-rules.md` (Task 17) rather than shrinking it.
Re-run Step 4 until every screen reports `0 problems`, then run KitCheck again (`202 passed, 0 failed`).

- [ ] **Step 6: Back to desktop**

Reset the device simulator to the default (follow the same skill), rebuild all themes with Step 3's snippet so desktop screenshots stay correct.

- [ ] **Step 7: Commit**

```bash
git add roblox-ui/kit roblox-ui/screenshots/mobile
git commit -m "fix: keep touch targets 44 px and verify every theme on a phone"
```

### Task 16: Optional texture pack (stud tile)

The user allowed uploads in the original request ("you can upload stuff if you need to"). The shipped kit keeps `assets = {}`; the uploaded ID is only written into the showcase place's installed copy of the theme.

**Files:**
- Create: `roblox-ui/tools/make_texture_pack.py`, `roblox-ui/textures/stud_tile.png`, `roblox-ui/assets.md`, `roblox-ui/screenshots/stud-simulator-{hud,menus}-textured.jpg`
- Modify (UI/UX place only): installed `game.ReplicatedStorage.UIKit.Themes.StudSimulator` (`assets` line)

**Interfaces:**
- Consumes: `theme.assets.studTile` read by `Decor.studs` (Task 3).
- Produces: a 128×128 RGBA stud tile, tinted at runtime by `ImageColor3`/`ImageTransparency`.

- [ ] **Step 1: Check Python and Pillow**

```bash
python -c "import PIL; print(PIL.__version__)"
```

If it fails: `python -m pip install Pillow`.

- [ ] **Step 2: Write `roblox-ui/tools/make_texture_pack.py`**

```python
"""Draws UIKit's optional texture pack: a stud tile for Stud Simulator surfaces.

Usage: python make_texture_pack.py <out_dir>
The stud is white/grey on a transparent background so UIKit can tint it with ImageColor3.
"""
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter

TILE = 128
STUD_RADIUS = 40
SHADOW_OFFSET = 5
SHADOW_BLUR = 4
SHADOW_ALPHA = 110
RIM_WIDTH = 3
RIM_GREY = 120
SHADE_STEPS = 24
HIGHLIGHT_SHIFT = 10


def stud_tile() -> Image.Image:
    img = Image.new("RGBA", (TILE, TILE), (0, 0, 0, 0))
    centre = TILE // 2
    shadow = Image.new("RGBA", (TILE, TILE), (0, 0, 0, 0))
    ImageDraw.Draw(shadow).ellipse(
        (
            centre - STUD_RADIUS + SHADOW_OFFSET,
            centre - STUD_RADIUS + SHADOW_OFFSET,
            centre + STUD_RADIUS + SHADOW_OFFSET,
            centre + STUD_RADIUS + SHADOW_OFFSET,
        ),
        fill=(0, 0, 0, SHADOW_ALPHA),
    )
    img.alpha_composite(shadow.filter(ImageFilter.GaussianBlur(SHADOW_BLUR)))
    body = Image.new("RGBA", (TILE, TILE), (0, 0, 0, 0))
    draw = ImageDraw.Draw(body)
    # shrinking, brightening circles drifting to the top-left read as a lit, raised stud
    for i in range(SHADE_STEPS):
        t = i / (SHADE_STEPS - 1)
        radius = STUD_RADIUS * (1 - 0.55 * t)
        shade = int(170 + 85 * t)
        shift = -HIGHLIGHT_SHIFT * t
        draw.ellipse(
            (centre + shift - radius, centre + shift - radius, centre + shift + radius, centre + shift + radius),
            fill=(shade, shade, shade, 255),
        )
    img.alpha_composite(body)
    ImageDraw.Draw(img).ellipse(
        (centre - STUD_RADIUS, centre - STUD_RADIUS, centre + STUD_RADIUS, centre + STUD_RADIUS),
        outline=(RIM_GREY, RIM_GREY, RIM_GREY, 255),
        width=RIM_WIDTH,
    )
    return img


def main() -> None:
    out = Path(sys.argv[1] if len(sys.argv) > 1 else ".")
    out.mkdir(parents=True, exist_ok=True)
    path = out / "stud_tile.png"
    stud_tile().save(path)
    print(path)


if __name__ == "__main__":
    main()
```

- [ ] **Step 3: Generate and look at it**

```bash
python "roblox-ui/tools/make_texture_pack.py" "roblox-ui/textures"
```

Expected output: `roblox-ui/textures/stud_tile.png`. Open it with Read and confirm one raised grey stud with a soft shadow on transparency.

- [ ] **Step 4: Upload through the Studio MCP**

Serve the folder in the background:

```bash
python -m http.server 8765 --directory "roblox-ui/textures"
```

(`run_in_background: true`), then `upload_image` with `imagePaths: ["http://localhost:8765/stud_tile.png"]`. Record the returned `rbxassetid://…`. Stop the server (TaskStop on the background task).

- [ ] **Step 5: Use it in the showcase only**

`script_read` `game.ReplicatedStorage.UIKit.Themes.StudSimulator`, then `multi_edit` replacing `	assets = {},` with `	assets = { studTile = "rbxassetid://<id>" },` in the installed module (the workspace file stays `{}`). Rebuild the Stud Simulator showcase, `show` HUD and Menus, capture to `roblox-ui/screenshots/stud-simulator-hud-textured.jpg` and `…-menus-textured.jpg`. New uploads can render blank for a few minutes while Roblox moderates them; wait and re-capture if the studs are missing.

- [ ] **Step 6: Write `roblox-ui/assets.md`**

Sections, in this order:
1. **Zero uploads is the default** — what each theme looks like without textures (Stud Simulator falls back to the built-in `rbxasset://textures/whiteCircle.png` dot tile; everything else is procedural).
2. **Make the stud tile** — the Step 3 command.
3. **Upload it** — (a) Studio MCP: the Step 4 local server + `upload_image`; (b) by hand: Studio → Asset Manager → Bulk Import, then right-click → Copy ID.
4. **Wire it in** — set `assets = { studTile = "rbxassetid://<id>" }` in the game's installed theme module; `Decor.studs` picks it up on the next build.
5. **Gotchas** — new images render blank until moderation finishes; a group-owned game needs the image uploaded to the group (or it may not load for players); `rbxasset://` textures ship inside the Roblox client, so they cost nothing but aren't guaranteed forever; uploads are public assets, so never upload anything private.

- [ ] **Step 7: Commit**

```bash
git add roblox-ui/tools roblox-ui/textures roblox-ui/assets.md roblox-ui/screenshots/stud-simulator-*-textured.jpg
git commit -m "feat: add optional stud texture pack"
```

### Task 17: Skill documents

**Files:**
- Create: `roblox-ui/SKILL.md`, `roblox-ui/workflow.md`, `roblox-ui/ux-rules.md`, `roblox-ui/components.md`, `roblox-ui/styles/{stud-simulator,battlegrounds,kinetic-comic,cyber-holo,manga-ink,dark-fantasy}.md`

**Interfaces:**
- Consumes: every builder signature (Task 2), Motion API (Task 7), each theme's tokens and critique checklist (Tasks 4, 9–13), the audit snippet (Task 15), spike findings (Task 1). Install is documented as the `multi_edit` procedure; it replaces the spec's planned `install.luau` because MCP `multi_edit` creates scripts with source directly.
- Produces: the skill Claude loads.

- [ ] **Step 1: Write `roblox-ui/SKILL.md`**

```markdown
---
name: roblox-ui
description: "Builds polished, themed Roblox UI in Studio through the Roblox Studio MCP: HUDs, shops, inventories, settings, loading screens, main menus, toasts, reward popups and damage numbers, in six styles (Stud Simulator, Battlegrounds, Kinetic Comic, Cyber Holo, Manga Ink, Dark Fantasy). Use when the user asks for Roblox UI or UX, a HUD, menu, shop, inventory, loading screen or main menu, a UI style or reskin, or UI that looks like a Roblox genre (simulator, battlegrounds, anime, horror, sci-fi)."
allowed_tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
  - mcp__Roblox_Studio__list_roblox_studios
  - mcp__Roblox_Studio__get_studio_state
  - mcp__Roblox_Studio__execute_luau
  - mcp__Roblox_Studio__multi_edit
  - mcp__Roblox_Studio__script_read
  - mcp__Roblox_Studio__search_game_tree
  - mcp__Roblox_Studio__inspect_instance
  - mcp__Roblox_Studio__screen_capture
  - mcp__Roblox_Studio__start_stop_play
  - mcp__Roblox_Studio__upload_image
  - mcp__Roblox_Studio__skill
---

# Roblox UI

Build Roblox UI with **UIKit**, a themed Luau component kit in `kit/`, through the Studio MCP. Don't hand-place
frames one at a time: install the kit, pick a theme, call builders, bake the result into StarterGui, screenshot
it, and fix what the screenshot shows.

## When to Use

- "Make a shop / HUD / inventory / settings / loading screen / main menu for my game"
- "Make my UI look like a battlegrounds / simulator / anime / horror game", "reskin my UI"
- Adding feedback moments: toasts, reward popups, level-up splashes, damage numbers

## Pick a style

| Style | Feels like | Good for |
|---|---|---|
| Stud Simulator | Candy gradients, chunky outlines, studs, bouncy pops | Simulators, tycoons, obbies, pet games |
| Battlegrounds | Flat charcoal tiles, one hot accent, split vitals bar | PvP fighting, anime battlegrounds |
| Kinetic Comic | Red/black/white, slanted shapes, slam-ins | Stylish action, heists, rhythm |
| Cyber Holo | Neon on glass, cut corners, scanlines, flicker | Sci-fi shooters, hacking, space |
| Manga Ink | Paper and ink, screentone, speed lines, stamps | Anime story games, sword fighters |
| Dark Fantasy | Black, crimson, gold, gothic type, slow fades | Horror, souls-likes, ghoul/vampire games |

No style named? Ask with this table. Details and checklists: `styles/<style>.md`.

## Workflow

1. `list_roblox_studios`, pick the user's place by name, confirm before writing to it.
2. Install the kit and the chosen theme(s) — `workflow.md` § Install.
3. Run KitCheck — it must report `0 failed`.
4. One `execute_luau` per screen: call builders from `components.md`, parent the ScreenGui to StarterGui.
5. `screen_capture`, compare with `styles/<style>.md` and `ux-rules.md`, fix, capture again.
6. Playtest (`start_stop_play`): presses squash, panels open one at a time, lists scroll to the end.
7. Phone check with the device simulator — `workflow.md` § Phone audit.
8. Tell the user what was built and how to feed it data (`components.md` § Wiring).

## Rules

- Every colour, font, size and timing comes from the theme. Need something new? Add a token to the theme.
- Keep the contract names: `ScreenGui > Main` (`TitleTab`, `Close`, `List`/`Grid`/`Body`), `Template`, `Label`,
  `Fill`, `Amount`, `Cooldown`. Game code and Motion find UI by these names.
- One panel open at a time, the world blurs behind it, HUD clutter tagged `UIKit.HideWithPanel` hides.
- Zero uploads by default. Textures are optional polish — `assets.md`.
- Never destroy a ScreenGui without `UIKitBuilt = true`; ask before replacing hand-made UI.

## Gotchas

- **Scale cells in a scrolling grid never settle.** A `UIGridLayout` with Scale cell sizes inside an auto-sizing
  `ScrollingFrame` grows the canvas it sizes against, so scrolling stops part-way. Use `UIKit.Grid` (pixel cells
  from `Util.pixelGrid`) and pixel-tall list rows.
- **Rotation switches off clipping.** Anything rotated, or inside something rotated, ignores `ClipsDescendants`.
  Tilt only panels that don't scroll (`Tilt = false` on the rest).
- **UIGradient multiplies.** A gradient's colours multiply `BackgroundColor3`, so gradient fills sit on white.
  Text on a gradient button lives in a child `Label`, or the gradient tints the text too.
- **Children always draw above their parent's own background.** Shadows behind a frame need `UIShadow` or a child
  "Face" that carries the fill (`Decor.hardShadow` does both).
- **Edit-time `require` is cached.** Require a clone (`require(RS.UIKit:Clone())`) or edits won't show up.
- **Touch fires `MouseEnter` without `MouseLeave`.** Hover effects only when `UserInputService.MouseEnabled`.
- **Pixel strokes don't scale.** A 4 px outline is twice as heavy on a phone. Kit strokes store `BaseThickness`
  and Motion rescales them; set it on any stroke you add by hand.
- **TextScaled needs a cap.** Without `UITextSizeConstraint` a short label in a big box becomes enormous.
- **Players can ask for less motion.** Motion checks `GuiService.ReducedMotionEnabled`; keep that check if you
  write your own tweens.
- **Emoji icons are a placeholder, not art.** They make the kit work with zero uploads; swap in real icons for
  a released game.

## Files

`workflow.md` (install, build, screenshot, playtest, phone audit) · `components.md` (every builder, Motion API,
wiring examples) · `ux-rules.md` (screen zones, safe areas, touch, hierarchy, motion, accessibility, loading
screens) · `styles/` (one per style) · `assets.md` (optional textures) · `kit/` (Luau source; `kit/dev/` is
for testing only).
```

Check: the file is under 120 lines (`wc -l roblox-ui/SKILL.md`). If over, move the style table into `styles/README` and keep one line per style.

- [ ] **Step 2: Write `roblox-ui/workflow.md`**

Sections, each with the exact snippet from this plan:
1. **Find the place** — `list_roblox_studios`; names include the place id; confirm with the user before writing.
2. **Install** — the folder snippet; `multi_edit` order: `ReplicatedStorage.UIKit` ← `kit/UIKit.luau`, then `Util`, `Decor`, `Controls`, `Containers`, `Readouts`, `Feedback`, `Screens`, `Motion`; folder `UIKit.Themes`; only the theme modules the game uses; `StarterPlayer.StarterPlayerScripts.UIRuntime` (LocalScript) ← `kit/UIRuntime.client.luau`. Optional dev: `ServerStorage.UIKitDev.KitCheck` ← `kit/dev/KitCheck.luau`. Re-installing a module = replace its whole source.
3. **Verify** — the KitCheck runner snippet and the expected `0 failed`. A game that installs fewer themes should set `KitCheck.EXPECTED_THEMES` to the ones it installed.
4. **Build a screen** — a complete example script (Shop panel with tabs, a hidden `Template` card and three items; a HUD IconButton with `Opens = "Shop"`), including the "refuse to replace hand-made UI" check and `Util.scaleStrokes(gui, workspace.CurrentCamera.ViewportSize.Y)`. Panels are built with `Enabled = false`; to look at one, enable it, capture, disable it again.
5. **Look at it** — `screen_capture` with an explicit camera; compare with the style checklist; common fixes (z-order: raise `ZIndex` on the content, not the decor; clipped icon: give it room in its parent; washed-out text: check the variant's `text` colour).
6. **Playtest** — `start_stop_play`, then on the Client `require(game.ReplicatedStorage.UIKitDev.MotionCheck).run()` if the dev module is installed; manual checks: press squash, open/close, scroll to the end, toggles and sliders.
7. **Phone audit** — the Task 15 audit snippet; load `rbx-device-simulator-lua` with `mcp__Roblox_Studio__skill` to switch devices; fix rules from Task 15 Step 5.
8. **Hand-off** — list the ScreenGuis made and their contract names, and point at `components.md` § Wiring.

- [ ] **Step 3: Write `roblox-ui/components.md`**

One section per builder, in Task 2's order. Each section: the signature line from Task 2, a one-line purpose, the children it creates (contract names), the theme tokens it reads, and a 2–5 line example. Then:
- **Motion** — every function from Task 7's Interfaces with one example each.
- **Zero-code wiring** — `Opens` attribute, `UIKit.Close`, tabs, `UIKit.HideWithPanel`.
- **Wiring examples** (copy verbatim):

```lua
local Players = game:GetService("Players")
local ReplicatedStorage = game:GetService("ReplicatedStorage")
local Motion = require(ReplicatedStorage.UIKit.Motion)
local player = Players.LocalPlayer
local hud = player:WaitForChild("PlayerGui"):WaitForChild("HUD")

-- cash that counts up when the leaderstat changes
local cash = player:WaitForChild("leaderstats"):WaitForChild("Cash")
local shown = cash.Value
cash.Changed:Connect(function(value)
	Motion.countTo(hud.Stats.Cash.Amount, shown, value)
	shown = value
end)

-- health on the left half of a split bar
local humanoid = (player.Character or player.CharacterAdded:Wait()):WaitForChild("Humanoid")
humanoid.HealthChanged:Connect(function(health)
	Motion.setBar(hud.Vitals, health / humanoid.MaxHealth, "Left")
end)

-- a toast and a damage number from game events
Motion.toast(hud.Toasts, "Quest complete! +250 XP", "xp")
Motion.damage(hud, UDim2.fromScale(0.5, 0.4), 1240, true)

-- filling a shop list from data: clone the hidden Template
local list = player.PlayerGui.Shop.Main.List
for i, item in { { name = "VIP", price = 399 }, { name = "2X Cash", price = 199 } } do
	local card = list.Template:Clone()
	card.Name = "Item" .. i
	card.Title.Text = item.name
	card.Action.Label.Text = "R$ " .. item.price
	card.LayoutOrder = i
	card.Visible = true
	card.Parent = list
end
```

- [ ] **Step 4: Write `roblox-ui/ux-rules.md`**

Sections:
1. **Screen zones** — this map, then one line per zone:

```
┌───────────────────────── Roblox top bar (keep clear) ──────────────────────────┐
│ status: avatar, level, HP      objective / quest          currency, offers      │
│                                                                                 │
│ menu buttons                                                    offers / gifts  │
│ (2×2 grid)                                                                      │
│                              world + toasts (top-right)                         │
│ joystick zone (mobile,                                                          │
│  keep empty)                bars + ultimate                     action buttons  │
│ small shortcuts           hotbar / move tiles                   (mobile)        │
└─────────────────────────────────────────────────────────────────────────────────┘
```
2. **Safe areas** — HUD ScreenGuis use `ScreenInsets.CoreUISafeInsets`; full-screen ones `IgnoreGuiInset = true` + `ScreenInsets.None`; never put tappable UI in the bottom-left 35 % × 45 % on mobile (thumbstick).
3. **Touch** — 44 px minimum (`Util.minTouch`), 8 px between targets, primary actions in thumb reach (bottom corners).
4. **Hierarchy** — one primary button per screen; `danger` only for close/destructive; prices on the buy button itself; one panel at a time.
5. **Text and numbers** — every label `TextScaled` + `UITextSizeConstraint`; nothing under ~14 px on a phone; numbers through `Util.abbreviate` (1.2K, 3.4M).
6. **Colour** — 4.5:1 contrast for text; never colour alone (rarity = colour + label); outline text that sits over the 3D world.
7. **Motion** — the per-style timing table (style, entrance, fast/normal/slow seconds, press scale) copied from the six themes; respect `GuiService.ReducedMotionEnabled`.
8. **Accessibility settings** — `GuiService.PreferredTransparency` (multiply your background transparency by it so players who want solid panels get them) and `GuiService.PreferredTextSize`.
9. **Loading screens** — a `ReplicatedFirst` LocalScript: `ReplicatedFirst:RemoveDefaultLoadingScreen()`, build `UIKit.LoadingScreen` into PlayerGui, drive the bar from `ContentProvider:PreloadAsync(assets, callback)` progress (or `Motion.loading` for a fixed time), then fade out; always offer Skip after a few seconds.

- [ ] **Step 5: Write the six `roblox-ui/styles/<style>.md` files**

Each file, same sections:
1. **When to use** — genres and the reference games it was built from (Lift a Rock for CUH; TSB, Jujutsu Shenanigans, Type Soul; Persona-style menus; sci-fi HUDs; manga pages; Ghoul://Re and Deepwoken).
2. **Palette** — table of token → hex copied from the theme module.
3. **Type** — the three fonts and the text-stroke rule.
4. **Signature details** — the decorators and shape tokens the theme uses, one line each, in plain words.
5. **Motion** — entrance style and timings.
6. **HUD layout** — `simulator` or `combat`, and which bar style.
7. **Do / Don't** — 4–6 bullets each, specific to the style (for example Kinetic Comic: "don't add gradients or rounded corners").
8. **Checklist** — the critique list from that theme's task, verbatim.
9. **Screenshots** — relative links to its five desktop captures and two mobile captures.

- [ ] **Step 6: Lint the skill**

```bash
wc -l "roblox-ui/SKILL.md"
grep -c "Use when" "roblox-ui/SKILL.md"
grep -c "^- \*\*" "roblox-ui/SKILL.md"
```

Expected: ≤ 120 lines, at least 1 "Use when", at least 3 gotchas (10 written). Every relative link in the docs points at a file that exists (`ls` each linked screenshot).

- [ ] **Step 7: Commit**

```bash
git add roblox-ui/SKILL.md roblox-ui/workflow.md roblox-ui/ux-rules.md roblox-ui/components.md roblox-ui/styles
git commit -m "docs: add roblox-ui skill documents"
```

### Task 18: README, install, cold-start test

**Files:**
- Create: `README.md` (workspace root)
- Copy: `roblox-ui/` → `C:\Users\Administrator\.claude\skills\roblox-ui\`

**Interfaces:**
- Consumes: everything above.
- Produces: the installed skill and the viewer-facing README.

- [ ] **Step 1: Write `README.md`**

Sections:
1. **Title + one-line pitch** — "A Claude Code skill that builds polished Roblox UI in six styles through the Roblox Studio MCP."
2. **Gallery** — a table, one row per style, columns HUD / Menus / Main menu, each cell an image link into `roblox-ui/screenshots/`.
3. **What you need** — Claude Code; Roblox Studio with the Studio MCP connected; Studio 0.744+ for native shadows/blur (older Studio still works, without those).
4. **Install** — copy the folder:

```bash
cp -r roblox-ui ~/.claude/skills/roblox-ui
```

or into a project's `.claude/skills/` to share it with that project only.
5. **Try it** — five example prompts:
   - "Add a Stud Simulator HUD and shop to my game."
   - "Reskin my inventory in the Manga Ink style."
   - "Make a Battlegrounds loading screen and main menu."
   - "Give my fighting game Cyber Holo damage numbers and toasts."
   - "Build all six styles in my UI test place so I can compare them."
6. **What's inside** — the file list from Task 17's SKILL.md "Files" line, plus `kit/dev/` (KitCheck, MotionCheck, Showcase) for testing.
7. **Optional textures** — one paragraph pointing at `roblox-ui/assets.md`.
8. **Credits** — styles inspired by the listed Roblox games and genres; not affiliated with them; all UI is original and built from Roblox primitives.

- [ ] **Step 2: Install for the user**

```bash
rm -rf "/c/Users/Administrator/.claude/skills/roblox-ui"
cp -r "roblox-ui" "/c/Users/Administrator/.claude/skills/roblox-ui"
ls "/c/Users/Administrator/.claude/skills/roblox-ui"
```

(The `rm -rf` targets only a previous copy of this same skill; check with `ls` first that the folder is ours or absent.) Expected listing: `SKILL.md assets.md components.md kit screenshots styles textures tools ux-rules.md workflow.md`.

- [ ] **Step 3: Cold-start test with a fresh agent**

Dispatch one `general-purpose` subagent with only this brief: "Use the skill at `C:\Users\Administrator\.claude\skills\roblox-ui` (read its SKILL.md first and follow it) to add a Manga Ink shop panel ScreenGui named `ColdStartShop` with three items to the Roblox Studio place whose `list_roblox_studios` name starts with `UI/UX`. Do not touch any other ScreenGui. Report the KitCheck output, the instances you created, and the path of a screenshot of the shop." When it reports, verify with `inspect_instance StarterGui.ColdStartShop` and look at its screenshot. Any step it got wrong or had to guess is a doc gap: fix `SKILL.md`/`workflow.md`, re-copy the skill (Step 2). Then delete `StarterGui.ColdStartShop` (it has `UIKitBuilt = true`).

- [ ] **Step 4: Final verification**

- KitCheck: `202 passed, 0 failed`.
- MotionCheck in Play: `12 passed, 0 failed`.
- `ls roblox-ui/screenshots` shows 30 desktop captures (6 styles × 5 screens), 12 mobile captures, 2 textured captures.
- The Lift a Rock place is unchanged (`search_game_tree` on its StarterGui shows no `_ClaudePreview` or `SC_` guis).

- [ ] **Step 5: Hand-off to the user**

Send the gallery screenshots with `SendUserFile` (one per style: HUD + Menus), give the install path, and list what still needs the user (real icon art for a released game; whether to publish the README/skill to their audience).

- [ ] **Step 6: Commit**

```bash
git add README.md
git commit -m "docs: add README for the roblox-ui skill"
```

