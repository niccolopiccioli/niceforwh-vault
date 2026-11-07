# SDD ledger — plan: docs/superpowers/plans/2026-10-25-roblox-ui-skill.md

Spec: docs/superpowers/specs/2026-10-25-roblox-ui-skill-design.md
Executor: inline (executing-plans), user chose Native + no git.

Ruling: no git, no worktree, no commits — user chose "No git" at plan handoff — cost if wrong: no per-task rollback; files are the record.
Ruling: task-start/task-done scripts not used (they need git and a shell test command); tests are KitCheck/MotionCheck run through MCP and their output is written here by hand — cost if wrong: ledger lines are manual.

Pre-flight (shared interfaces):
- T2 KitCheck pins builder signatures ↔ T3–T6 builders: names/props match (checked in plan self-review).
- T3 Util/Decor ↔ T4–T13 themes and components: every Decor/Util call has a definition (grep check, only regex false positives).
- T7 Motion ↔ T14 ShowcaseRuntime: enter/loading/splash/toast/damage/cooldown/setBar all produced by T7.
- T8 Showcase names (Moves/Slot3, Vitals, LevelBar, Toasts, LevelUp, Reward) ↔ T14 runtime lookups: match.
- T15 adds Util.minTouch + KitCheck case after T2–T13 counts: counts in T15 account for it (196→202).

Task 1: complete (spike: UIShadow yes, UIBlur no, dot tile yes, Path2D/triangles/slant yes, emoji yes, Source writable, clone-require fresh → docs/superpowers/plans/spike-results.md)
Task 1: Ruling: Decor.USE_UIBLUR = false — UIBlur showed no blur over GUI in edit or play — cost if wrong: Cyber Holo loses a frosted look it could have had.
Task 2: Ruling: install kit files by HttpService:GetAsync from a local `python -m http.server 8765` (serving roblox-ui/) and setting .Source, instead of pasting each file through multi_edit — same resulting ModuleScripts, far fewer tokens; spike showed Source is writable and HTTP to 127.0.0.1 works — cost if wrong: none for the kit; viewers without HTTP enabled fall back to multi_edit (documented).
Task 8: USER REVIEW → "Looks bad" + reference library github.com/izzyfrm/roblox-ai (5.9k images). User confirmed all four diagnoses: polka-dot studs, emoji icons, too big/chunky, panel look. Chose Blender-rendered 3D icon pack.
Task 8: Ruling (scope change, user-approved): uploads become part of the showcase build (stud tile + 3D icon pack, uploaded via upload_image); kit keeps zero-upload fallbacks (dot tile, emoji) for viewers who skip the upload step. Task 16 (texture pack) moves before the remaining themes and grows an icon pack. Stud theme redesigned from refs: header "bar" style, saturated studded bodies, thin dark borders, flat buttons, smaller HUD, bare currency readouts. Remaining themes will also be driven by the repo's ui-styles refs.
Task 8b: texture + icon pack done — tools/make_texture_pack.py (rounded-square tone-on-tone stud, matched to Stud-GUI-2 offer tiles), tools/render_icons_blender.py (22 original 3D icons, Blender 5.1 EEVEE + Freestyle ink, separate "UIKitIcons" scene; user's own scene untouched), tools/finish_icons.py (512→256). Uploaded via upload_image: stud_tile rbxassetid://100994647021017 + 22 icons (ids in kit/Icons.luau).
Task 8b: Ruling: ship the uploaded icon/stud ids as kit defaults (the user's own original uploads; public images load in any experience) with emoji/dot fallbacks — viewers get the art with zero work — cost if wrong: if ids get moderated or removed, kit falls back to emoji/dots and the README tells viewers to re-render/re-upload.
Task 8c: user: "Use the icons from the pack LOOK AT THE REFERENCES". Switched to the pack's visual-refs/icons (27 uploaded, ids in kit/Icons.luau PACK) + 14 kit gap icons re-rendered in the pack's style (render_icons_blender.py STYLE="cel": toon ramp, navy #000034 ink ~14px@256). Glossy 3D set discarded. Stud theme v2 written from style-refs/studs palette (blue #2890FF/#1760C9, yellow #FFD23F, red #FF5A40, navy #1E1B2F): header "bar", bare currency, Offer builder, Decor.shine. TDD: KitCheck red 35/4 (Icons, currencyStyle, Offer, named icon) → green 39/0. Showcase HUD re-laid out per Stud-GUI-2.
Task 8c: Ruling: pack icons kept out of the skill folder (third-party art, "belong to their creators"); only their uploaded ids + attribution live in Icons.luau — cost if wrong: viewers depend on those ids; README must flag the licence.
Task 8c: Diagnosed: UI/UX window was minimized (IsIconic=True); restored+maximized+foreground via user32, still no capture. Desktop screenshot (PowerShell CopyFromScreen) shows the UI/UX Studio window painting solid white (viewport, ribbon, panels) while execute_luau still works → Studio renderer hung. Needs user to save + restart Studio. Workaround for future captures: PowerShell desktop capture works when Studio renders.
Task 8d: user asked to save every GUI/UI/icon image as skill reference → roblox-ui/references/ (1,142 images, 158 MB: previews, style-refs, ui-styles, visual-refs from izzyfrm/roblox-ai) + references/README.md indexing refs per kit theme and per screen, with licence note (all listed paths verified to exist).
Task 8d: UNBLOCKED — user OK'd a restart; killed UI/UX Studio (pid 44320) and relaunched with -task EditPlace -placeId 82819238997132 -universeId 10772929345 (new studio_id 16be2368-…). Kit + 5 SC_StudSimulator guis were still in the place. screen_capture only works while the Studio window is the foreground window (Alt-tap + SetForegroundWindow + ShowWindow 3); a background window times out even when it renders.
Task 8d: (was) BLOCKED on screenshots — 2026-10-26 window cycle didn't help; screen_capture also times out in the "Untitled Experience" Studio, so all 4 Studio processes (running since 25/10) have stalled rendering. Needs user to save + restart Studio.
Task 8c: BLOCKED — screen_capture times out in BOTH Studio windows (and the 3D world stopped rendering earlier); PreloadAsync hangs; likely Studio windows minimized/occluded or screen locked. Waiting on user to bring the UI/UX Studio window to the front.
Task 8: in progress — Steps 1–6 done (rebuild-safety red→"PASS rebuild safety"; Showcase installed; backdrop built; 5 Stud screens built, critiqued, fixed, captured to roblox-ui/screenshots/stud-simulator-*.jpg; KitCheck 36/0). Step 7 = waiting on user review.
Task 8: Ruling: Stud Simulator loading/menu background uses a purple→cyan gradient + white rays instead of the dark backdrop — first capture read drab for a candy style — cost if wrong: one decorate.screen change.
Task 8: Ruling: showcase Feedback moves the splash top-left and damage numbers lower-left; Pets icon 🐾→🥚; offer x 0.985→0.97 — splash covered the popup title, paw emoji was dark-on-dark, offer tag hit the edge — cost if wrong: cosmetic.
Task 8: Note: the UI/UX Studio window renders no 3D world (baseplate, backdrop and view cube invisible in edit and play) while GUI renders fine; Lighting/camera normal. Likely window minimized/background; asked user.
Task 7: complete (Motion, UIRuntime, MotionCheck; red "0 passed, 1 failed - Motion installed" → green KitCheck 36/0 and MotionCheck 12/0 in Play; console has no UIKit errors)
Task 7: Ruling: Motion.toast falls back to theme.color.bars.accent when `kind` isn't a bar colour — the plan's MotionCheck passes "success", which isn't a bars key, so the plan code would error — cost if wrong: an unknown kind silently shows the accent stripe.
Task 6: complete (Feedback, Screens; KitCheck → "36 passed, 0 failed", matches Expected)
Task 5: complete (Readouts; KitCheck → "30 passed, 6 failed", the 6 = ToastStack/Popup/Splash/DamageNumber/LoadingScreen/MainMenu, matches Expected)
Task 4: complete (Controls, Containers, StudSimulator; KitCheck → "22 passed, 14 failed", all 14 = unbuilt Readouts/Feedback/Screens "attempt to call a nil value", matches Expected; preview matches Lift a Rock Featured panel)
Task 4: Ruling: softened Stud Simulator dot-stud transparency (panel 0.82→0.88, tab 0.65→0.75, slot 0.86→0.9) — preview showed the whiteCircle dots louder than Lift a Rock's studs — cost if wrong: studs a bit faint; one-line token change.
Task 3: complete (UIKit, Util, Decor installed; KitCheck → "4 passed, 1 failed - theme StudSimulator exists", matches Expected)
Task 2: complete (KitCheck installed at ServerStorage.UIKitDev.KitCheck; run → "KitCheck: 0 passed, 1 failed - kit installed: ReplicatedStorage.UIKit not found", matches Expected)

