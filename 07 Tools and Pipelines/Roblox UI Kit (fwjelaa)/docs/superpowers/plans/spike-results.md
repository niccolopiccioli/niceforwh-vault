# Spike results (Task 1)

Studio 0.744.0.7441077, UI/UX place, 2026-10-25.

- UISHADOW_EDIT: yes   (hard 10px offset shadow and soft 16px cyan glow both render)
- UISHADOW_PLAY: yes
- UIBLUR_EDIT: no      (yellow stripes behind a UIBlur frame stay sharp)
- UIBLUR_PLAY: no
- DOT_TILE: yes        (rbxasset://textures/whiteCircle.png tiles as touching dots in edit and play)
- PATH2D_CHAMFER: yes  (closed 8-point Path2D rim draws in edit and play)
- GRADIENT_TRIANGLES: yes (rotations 45/135/225/-45 show the inner half of each corner square)
- SLANT_CAPS: yes      (aspect-constrained caps make a right-leaning parallelogram)
- EMOJI: yes           (colour emoji render in a FredokaOne TextLabel)
- SOURCE_WRITABLE: yes (ModuleScript.Source can be set from execute_luau)
- CLONE_REQUIRE_FRESH: yes (first=1 second=2 direct=2)

Decisions (Task 1 Step 6):
- Decor.USE_UISHADOW = true
- Decor.USE_UIBLUR = false  → Decor.glass is a no-op; Cyber Holo panels rely on translucency + scanlines.
- Decor.DOT_TILE = "rbxasset://textures/whiteCircle.png"
- Showcase.USE_EMOJI = true
- No shape strategy change needed.
