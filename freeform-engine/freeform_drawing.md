Copyright © 2026 Arsh Buttar. All rights reserved. Confidential and proprietary.
Unauthorized copying, distribution, or use of this work is prohibited.

# Freeform Drawing Engine — Knowledge Specification

> **Single source of truth for the Freeform drawing system. Hierarchical, not chronological.**
>
> Last consolidation: 2026-07-04 (v4 — synthesis: integrated ~/shorts spatial physics framework, unified coordinate system, anatomical landmarks, anchoring triangulation, normal-based shading)
> Files of record:
> - `~/.opencode_knowledge/scripts/freeform_renderer.py` — **Quartz CGContext Canvas class (ACTIVE)**
> - `~/.opencode_knowledge/scripts/freeform_engine.py` — legacy CGEventPost engine (retained for activation only)
> - `~/.opencode_knowledge/freeform_drawing.md` — THIS FILE (knowledge spec)
> - `~/.opencode_knowledge/pen_calibration.txt` — calibrated pen activation coordinates (legacy only)
> - `~/shorts/` — **Creative production studio framework. Mandatory reference for any spatial/coordinate task.**
> - `~/shorts/microcosmos/spatial/rules.yaml` — 3D coordinate system, icosahedral grid, distance bands, camera physics
> - `~/shorts/microcosmos/CONSTITUTION.yaml` — 12-Book governance framework
> - `~/shorts/lessons.md` — Anchoring triangulation, camera metal, mechanical transitions

---

## 0. Hierarchy

The engine is a 7-level stack. Higher levels compose lower levels.

```
L7  Verification           count_ink, verify_phase, preflight_check, screenshot
L6  Vehicles              ground, frame, horizon (large-scale compositional aids)
L5b Drawing Fundamentals  Shading, Perspective, Form Construction, Proportion, Warmups
L5  Composition           house/roof/window/door/chimney, sun/cloud/tree/fence,
                          wheel/eye/leaf/cloud/brick_wall/sphere/star/smoke,
                          mountain/river/tier_block, crenelation
L4  Styles                bold5, bold3, paraline (modifiers on L3)
L3  Draw primitives       polyline, paraline, hatch_lines, zigzag_fill, grid_lines
L2  Geometry              catmull, polygon, circle, line, arc  (pure math)
L1  Input atoms           click, keystroke, key_combo, activate_pen, stroke,
                          zoom_in, zoom_out
L0.5 UI Navigation        click_tool, click_canvas_control, insert_shape,
                          insert_text_box, group/align/distribute, zoom_*
L0  Substrate             activate_freeform, new_board
```

Every drawing script imports the engine and uses compositions (L5) directly. Lower levels are accessed when no composition fits.

---

## 1. Substrate & Calibration (L0)

### 1.1 Verified Environment

```
Machine:  MacBook Air 13.6" M5 (2026), A3449
OS:       macOS Tahoe 26
Display:  2560×1664 native @224ppi, "More Space" scaled
          → 1470×956 @1x   (CGEventPost coordinates)
          → 2940×1912 @2x  (CGImageGetWidth of CGDisplayCreateImage)
Freeform: window (0, 32) size 660×700; canvas starts y≥84
```

### 1.2 Resolution rule

`CGDisplayCreateImage` returns @2x. `CGEventPost` clicks at @1x. **Divide screen pixels by 2 when reading them from `CGImageGetWidth` results, multiply by 2 to write to image bytes.**

The engine's `count_ink` handles this conversion internally — pass `@1x` screen coordinates.

### 1.3 Pen Activation (CRITICAL — order matters)

```
Step 1: click_tool("shape") — accessibility-click toolbar Shape button  [NEW — no pixel coords]
Step 2: sleep(0.25)
Step 3: click(PEN_POP)      — selects "Draw with Pen" in popover
Step 4: sleep(0.5)
```

**Order: Shape FIRST.** Reversed order produces no pen activation.

The Shape button is found by accessibility description (`AXMenuButton desc="Insert Shape"`),
not by pixel coordinates. This is robust against UI resizing/theme changes.

The Pen popover position remains pixel-calibrated (stored in `~/.opencode_knowledge/pen_calibration.txt`):
```
PEN_X, PEN_Y = 381, 511      # "Draw with Pen" popover item
```

(Older scripts in the archive used (404, 55) / (395, 509) — those coords no longer match the current Freeform UI; the engine reads the calibrated file.)

When the user clicks new positions, run `capture_clicks(2)` — interactive utility that updates the file.

### 1.4 Stroke commit

Every pen stroke must be terminated with Escape (keycode 53):
```python
keystroke(53)  # commits the stroke and deactivates Pen tool
```

The next stroke requires `activate_pen()` again. The engine's `polyline`, `paraline`, `bold3`, `bold5` all handle this implicitly.

---

## 2. Input Atoms (L1)

| Function | Purpose | Returns |
|---|---|---|
| `click(x, y, slp)` | Atomic left-click at screen pixel coords | — |
| `keystroke(kc)` | Press and release a single key | — |
| `key_combo(mod, kc)` | Press modifier + key (e.g. Cmd+Plus) | — |
| `activate_pen()` | Two-click protocol to make Pen tool active | — |
| `stroke(pts, slp)` | One pen drag through pts + Escape commit | — |
| `stroke_soft(pts, slp)` | Like `stroke` but assumes Pen already active | — |
| `zoom_in(n)` / `zoom_out(n)` | Cmd+Plus/Minus n times | — |

**Rules:**
- `slp` (per-click sleep) must be ≥ 0.005s for HID to register each click as a separate vertex.
- `keystroke(53)` is mandatory after every stroke — Freeform deactivates Pen after Escape.
- Pen re-activates on next `activate_pen()` call. This adds ~0.5s overhead per stroke.

---

## 3. Geometry Primitives (L2)

Pure math. No Freeform dependencies.

### 3.1 `catmull(pts, n=40, closed=False)` — Spline interpolation

Catmull-Rom spline. Maps N control points to N×n interpolated points along a smooth curve.

```python
from freeform_engine import catmull
curve = catmull([(100, 100), (200, 50), (300, 80), (400, 60), (500, 100)], n=40)
# Returns [(100, 100), ..., (500, 100)] with 5×40=200 points
```

| n | Use case |
|---|---|
| 15-20 | Quick curves, simple shapes |
| 30 | Smooth detail (letters, small features) |
| 40-50 | Hero silhouettes (mountains, bodies, roofs) |
| 60+ | Deluxe smoothness for showcase curves |

`closed=True` treats pts as a closed polygon (wraps around).

### 3.2 `polygon(cx, cy, r, n=60, phase=0, scale_y=1.0)` — Regular polygon

`n=60` is a perfect circle approximation (error < 0.2 pixels). Used for circles, rims, suns, pupils, cells.

```python
poly = polygon(330, 400, 100, n=60)  # 60-gon approximating circle of r=100
```

### 3.3 `circle(cx, cy, r, n=60)` — alias of `polygon`

Identical. Returns a circular point list.

### 3.4 `line(x1, y1, x2, y2, n=20)` — Polyline approximation of a straight line

Returns n+1 points, including both endpoints.

### 3.5 `arc(cx, cy, rx, ry, a0, a1, n=30)` — Elliptical arc

From angle a0 to a1 (radians). Useful for partial circles, curve segments.

---

## 4. Draw Primitives (L3)

### 4.1 `polyline(pts, slp, bold)` — One pen drag through pts

```python
polyline(catmull(roof_ctrl_pts, 40), bold=True)  # bold Catmull-Rom curve
```

If `bold=True`, draws 5 parallel offset passes (≈ 8px thickness on screen).
If `bold=False`, draws 1 stroke (≈ 1px thickness).

### 4.2 `paraline(pts, offsets, slp)` — Polyline at every offset in list

```python
paraline([[100,100],[200,200]], [-3, 0, 3])  # 3 parallel offset strokes
```

### 4.3 `hatch_lines(x1, x2, y_start, y_end, step=3)` — Vertical hatching

Calls `activate_pen()` for every line — slow but explicit. **Avoid for large fills; use `zigzag_fill` instead.**

### 4.4 `zigzag_fill(x1, x2, y_start, y_end, step=3)` — One continuous fill

Fills a rectangular area with ONE pen drag (no separate lines). **Always prefer over `hatch_lines` for fills.**

```python
zigzag_fill(100, 500, 400, 470, step=3)  # one drag fills in 0.4s
hatch_lines(100, 500, 400, 470, step=3)  # could take 10+s with N activations
```

### 4.5 `grid_lines(x_start, y_start, x_end, y_end, dx, dy)` — Rectangular grid

```python
grid_lines(0, 0, 600, 400, dx=20, dy=20)  # 30×20 grid of horizontal+vertical lines
```

---

## 5. Style Modifiers (L4)

### 5.1 `bold5(pts, slp)` — Standard bold

5 parallel passes at offsets `[-4, -2, 0, 2, 4]`, with `y_offset = dx * 0.3` for diagonal consistency.

**Use for** any feature that should "stand out" (outlines, primary edges).

### 5.2 `bold3(pts, slp)` — Lighter bold

3 passes at `[-3, 0, 3]`. Use for less prominent features.

---

## 6. Composition Library (L5)

These are the named, reusable building blocks. Always prefer a composition over reinventing.

### 6.1 Geometric primitives

| Function | Purpose |
|---|---|
| `line_simple(x1, y1, x2, y2, bold)` | Single straight line |
| `rect_outline(x1, y1, x2, y2, bold)` | Rectangle outline |
| `rhombus(cx, cy, dx, dy, bold)` | Diamond shape via Catmull-Rom |
| `star4(cx, cy, r, bold)` | 4-arm sparkle (+ shape with diagonals) |
| `circle_outline(cx, cy, r, n, bold)` | Circle (60-gon default) |
| `ellipse_outline(cx, cy, rx, ry, n, bold)` | Oval (scaled 60-gon) |
| `crenelation(x1, x2, y_base, tooth_h, tooth_w)` | Returns pts for battlement pattern |

### 6.2 Architecture & Buildings

| Function | What it draws |
|---|---|
| `roof(peak_x, peak_y, base_left_x, base_y, base_right_x, smooth, bold)` | Pitched roof with curved peak via Catmull-Rom |
| `window_pane(x1, y1, x2, y2, dividers_h, dividers_v, bold)` | Window with mullion grid |
| `door(x1, y1, x2, y2, arch_top, has_knob, bold)` | Arched door + knob |
| `chimney(x, y, w, h)` | Rectangular chimney with cap |
| `window_arch(cx, cy, w, h, mullion_h, mullion_v, bold)` | Arched gothic window |
| `arrow_slit(cx, cy, h)` | Vertical arrow loop (loophole) |
| `tier_block(x1, y_base, x2, width, height)` | Trapezoidal stacked tier (Burj Khalifa style) |
| `brick_wall(x1, y1, x2, y2, brick_w, brick_h)` | Staggered brick grid with mortar |

### 6.3 Nature & Environment

| Function | What it draws |
|---|---|
| `sun(cx, cy, r_inner, r_outer, n_rays, ray_length)` | Concentric circles + radial rays |
| `cloud(cx, cy, rx, ry, n_loops, bold)` | Cloud blob via 4-loop Catmull-Rom |
| `tree_conifer(cx, base_y, height, base_width)` | Layered triangle pine tree |
| `tree_deciduous(cx, base_y, height, canopy_radius)` | Trunk + circular foliage |
| `leaf(cx, cy, w, h, lean, bold)` | Teardrop leaf |
| `mountain_silhouette(pts, smooth_n, bold)` | Mountain range (Catmull-Rom) |
| `river_curve(centerline_pts, w_start, w_end, smooth, bold)` | Two parallel bank curves |
| `star_twinkle(cx, cy, r, rays)` | Multi-pointed star |
| `smoke_puff(start_x, start_y, n_puffs, drift)` | Curling chimney smoke |
| `raincloud(cx, cy, w, h, drops, drop_length)` | Cloud + falling drops |

### 6.4 Vehicles, Bodies, Symbols

| Function | What it draws |
|---|---|
| `fence(x_start, x_end, y_base, picket_h, picket_w, rail_count)` | Picket fence |
| `wheel(cx, cy, r_tire, r_rim, spokes)` | Tire + rim + radial spokes |
| `sphere_grid(cx, cy, r, lat_count, lon_count, smooth)` | 60-gon outline + lat/lon gridlines |
| `eye(cx, cy, s, with_iris, with_lashes)` | Almond eye + iris + pupil; scale `s` for zoom levels |
| `tri_pyramid(cx, base_y, w, h, smooth, bold)` | Triangle pyramid (alternate shape for tree/conical) |

### 6.5 Vehicles (L6)

| Function | What it draws |
|---|---|
| `ground(y, x_start, x_end, bold)` | Slightly curved ground line |
| `frame(x1, y1, x2, y2, bold)` | Decorative border rectangle |
| `horizon(x_start, x_end, y, n_waves, ampx)` | Wavy horizon (sky/water transition) |

---

## 7. Verification (L7)

| Function | Purpose |
|---|---|
| `count_ink(x1, y1, x2, y2, threshold=80)` | Count dark pixels in screen-coord bbox. Threshold 80 distinguishes ink from canvas. |
| `verify_phase(name, x1, y1, x2, y2)` | Print named region with its ink count |
| `preflight_check(x, y)` | Draw a test stroke; returns ink count at (x,y). Use BEFORE main drawing to verify substrate is responsive. |
| `screenshot(path)` | Save full display to PNG file |

---

## 8. Verified Capabilities (only successes stored)

### 8.1 What WORKS — Verified Patterns

| Pattern | Verified by | Best use |
|---|---|---|
| Catmull-Rom curves | All ~15 drawings | Smooth organic features |
| Zigzag fill | landscape, house | Area fill in 1 stroke |
| Bold5 parallel offset | house, ARSH, supercar, Burj | Outlines, prominent edges |
| Triangular fill / tier stack | Burj Khalifa | Stepped buildings, cones |
| 60-gon ≈ circle | earth, infinite eye | All circular features |
| Stroke + Escape commit | All drawings | Basic pen protocol |
| Zoom in/out via Cmd-Plus/Minus | infinite eye, infinite tree, castle detail | Variable stroke thickness |
| AppleScript new board | All drawings | Fresh canvas |
| Pre-flight coordinate probe | integration framework | Substrate calibration |

### 8.2 What DOES NOT WORK — Rejected Patterns (kept as memory)

| Failure | Why | Use instead |
|---|---|---|
| 3-pass parallel for **vertical-dominant** strokes | Time cost 3x | bold5 (5 passes) only when critical |
| Single dot for verification | Single click = no stroke (`Pen` degrades to nothing) | preflight_check() draws 20-point stroke |
| Zoom-based ink verification at >4x centers | Offset by viewport drift | All drawing at zoom = 1; use bold for detail |
| Default Pen tool guess (404, 55) | Coordinates drift over Freeform updates | Read from calibration file |
| One-click Pen protocol | Pen requires TWO clicks | Two-step: Shape then Pen item |

### 8.3 Threshold Calibration

- **Dark ink detection**: r,g,b all < 80 → counts as ink pixel
- **Tan canvas**: RGB (241, 194, 118) — well above threshold
- **Per-stroke ink count**: ranges from 30 (single 6-pt stroke) to 11,000 (bold rectangle)

---

## 9. Composition Recipes (How to Build Common Drawings)

### 9.1 A small house (verified, ~30 sec)

```python
from freeform_engine import *
setup()
ground(470, 100, 560)
rect_outline(180, 470, 480, 380, bold=True)        # walls
roof(330, 290, 180, 365, 480, bold=True)            # pitched roof
door(305, 470, 355, 405)                            # arched door
window_pane(215, 380, 260, 420)                     # left window
window_pane(395, 380, 440, 420)                     # right window
chimney(420, 310, 25, 50)                            # chimney
sun(560, 280, 18, 22, n_rays=8, ray_length=10)      # sun
cloud(95, 245, 80, 12, bold=True)                     # cloud
screenshot("/tmp/house.png")
```

### 9.2 A landscape scene

```python
setup()
mountain_silhouette([(60, 470), (130, 380), (200, 300), (280, 280),
                     (350, 240), (430, 290), (510, 360), (560, 470)],
                     smooth_n=45, bold=True)
river_curve([(295, 480), (310, 510), (330, 540), (340, 570), (350, 610)],
            w_start=3, w_end=12, smooth=18, bold=True)
sun(490, 220, 15, 20)
cloud(150, 200, 60, 10, bold=True)
tree_conifer(380, 470, 80, 50)
tree_conifer(140, 470, 60, 35)
```

### 9.3 A sphere (Earth, planet)

```python
setup()
sphere_grid(330, 380, 140, lat_count=5, lon_count=6, smooth=15)
polygon(330, 380, 140, n=60)   # explicit sharper outline
```

### 9.4 A castle

```python
setup()
crenelation_pts = crenelation(258, 395, 300, 15, 14)
polyline(crenelation_pts)  # connect battlement
rect_outline(260, 300, 400, 420)  # main keep
rect_outline(190, 340, 220, 430)  # left tower
rect_outline(440, 340, 480, 430)  # right tower
door(305, 460, 345, 420, arch_top=15)
brick_wall(260, 305, 395, 415, brick_w=20, brick_h=10)  # detailed wall
```

### 9.5 A letter (e.g., "ARSH")

```python
# Use Catmull-Rom for organic curves
s_curve = catmull([(420, 340), (440, 335), (445, 320),
                   (425, 320), (390, 320), (370, 335), (360, 350),
                   (370, 360), (385, 370), (415, 375), (440, 385),
                   (445, 405), (440, 425), (415, 440), (390, 440),
                   (370, 438), (355, 425)],
                  n=60)
bold5(s_curve)
```

### 9.6 Infinite detail (zoom-in nest)

```python
setup()
eye(330, 400, s=1.0)               # level 1 (1x zoom)
zoom_in(4)
eye(330, 400, s=1.0)               # level 2 — same coords, smaller canvas footprint
zoom_in(5)
eye(330, 400, s=1.0)               # level 3
# ...zoom_out(n) to reveal
```

---

## 10. Philosophy & Principles

### 10.1 Caterpillar Principle (Foundation)

A curve = many small straight segments. The eye doesn't distinguish if n is large enough.

| Concept | Implementation |
|---|---|
| Curve | Catmull-Rom: N control points → n·N interpolated vertices |
| Circle | Regular polygon, n=60 |
| Fill | Zigzag continuous stroke |
| Thickness | Parallel offset passes (bold3 or bold5) |
| Detail | Same stroke at higher canvas zoom |

### 10.2 Working Principles

1. **Compose before computing.** Prefer `cloud()` over computing cloud pts yourself.
2. **Bold only where it counts.** A full-bold drawing hides detail. Use bold3/bold5 strategically.
3. **Area = visual weight.** Match bounding boxes for balanced compositions.
4. **Continuous path > many lines.** Use `zigzag_fill`, not `hatch_lines`, whenever possible.
5. **One stroke per feature, not one stroke per pass.** `bold5` is 5 strokes internally — let it manage that.
6. **Pre-flight every long drawing.** Run `preflight_check(x, y)` before committing 5 minutes of drawing.

### 10.3 Failure Mode Vocabulary

- **Strokes too thin**: increase offsets (`bold5`), redo with stroke density
- **Strokes too rough**: increase Catmull-Rom `n` (40-60)
- **Strokes too dense**: use `zigzag_fill` instead of hatch
- **Composition missing element**: re-check L5 library — almost certainly covered
- **Pen not responding**: `preflight_check`, then `capture_clicks` to re-calibrate

---

## 11. File Map

```
~/.opencode_knowledge/
├── freeform_drawing.md              ← THIS FILE — engine specification
├── pen_calibration.txt              ← Shape/Pen coordinates (user-verified)
├── think_on_paper_caterpillar.md    ← Philosophical companion
└── scripts/
    ├── freeform_engine.py          ← L0-L7 unified API (PUBLIC)
    ├── freeform_core_legacy.py     ← Old primitives (DEPRECATED)
    ├── capture_two_clicks.py       ← Old calibration capture
    ├── verify_protocol.py          ← Old single-shot verify
    ├── calibrate_pen.py            ← Latest interactive re-calibrate
    ├── draw_*.py                   ← Archived individual drawings
    │
    └── INDEX.md                    ← Drawing archive index (legacy)
```

**Future work imports `from freeform_engine import *`.** Never define click/stroke/catmull/etc. in a standalone script — they live in the engine.

---

## 12. Migration Path (from old scripts)

If a new script must import the engine and prefer compositions:

| Old pattern | New (engine) pattern |
|---|---|
| `click(x,y); time.sleep(0.005); ...` | `click(x, y, slp=0.005)` |
| `for dx in [-3,0,3]: stroke(pts+dx)` | `bold3(pts)` |
| `for dy in range: stroke([(x1,dy),(x2,dy)])` | `zigzag_fill(x1,x2,y_start,y_end,step)` |
| `activate_pen(); stroke(...)` | `stroke(...)` — auto-activates |
| `40-pt catmull(...)` | `catmull(pts, n=40)` |
| `polygon(cx,cy,r,60)` | `polygon(cx,cy,r,n=60)` |
| Drawing skull | `eye(cx,cy,s=1)` |

---

## 13. Shape Palette Mapping

Shape palette coordinates mapped via capture_clicks (2026-07-04). All use `click(SHAPE_BTN)` first (≈403,57), then the shape popover item:

| Shape | First click (Shape) | Second click (popover) |
|---|---|---|
| **Pen tool** | (403, 57) | (381, 511) — from pen_calibration.txt |
| **Square** | (403, 54) | (489, 151) |
| **Triangle** | (405, 57) | (302, 458) |
| **Speech Bubble** | (401, 59) | (401, 349) |
| **Curve** | (406, 60) | (493, 335) |
| **Tripod Camera** | (409, 56) | (307, 437) |
| **Table** | (490, 60) | — single click toolbar button |

Raw data: `~/.opencode_knowledge/shape_map.jsonl`

### 13.1 Shape spawning workflow

```
click(SHAPE_BTN)  → opens shape popover (~250ms delay)
click(popover_item) → selects shape tool, closes popover (~300ms delay)
click(canvas_x, canvas_y) → places shape at canvas position (~400ms delay)
```

To place multiple shapes of the **same type**, select once then click canvas multiple times:
```python
click(SHAPE_BTN); time.sleep(0.3); click(SQUARE_POP); time.sleep(0.4)
click(canvas_1); time.sleep(0.4)   # place 1st square
click(canvas_2); time.sleep(0.4)   # place 2nd square
```

### 13.2 Reliability notes

- Shape placement at far-right positions (>x=430) sometimes produces 0 ink. Keep shapes in x=150-430 range.
- Popover coordinates drift when Freeform UI updates (re-run capture_clicks to recalibrate).
- After placing a shape, the shape tool remains active. Must call `activate_pen()` before drawing pen strokes.

## 14. Text Tool

Freeform supports native text via **Insert → Text Box** (menu bar, no keyboard shortcut exposed).

```python
import subprocess
subprocess.run(['osascript', '-e', '''
tell app "System Events"
    tell process "Freeform"
        click menu item "Text Box" of menu "Insert" of menu bar 1
    end tell
end tell
'''], capture_output=True)
time.sleep(1.5)  # wait for text box to appear
```

After insertion:
- **Paste** (Cmd+V): inserts clipboard text into the text box
- **Type** via CGEventPost: each keycode types one character
- **Escape** (keycode 53): deselects text box

Default font is small (~12pt). Font size can be increased via Format → Font → Bigger (Cmd+Shift++), but multi-modifier key combos require special CGEvent handling.

### 14.1 Text vs drawn letters

| Method | Reliability | Quality | Speed |
|---|---|---|---|
| Native text box | High (text renders correctly) | Perfect typography | Fast (1 paste = full text) |
| Bold5 Catmull-Rom cursive | Low (control points need tuning) | Variable | Slow (5 passes × catmull) |
| Block letters (geometric strokes) | Medium | Readable but crude | Medium |
| Shape palette letters | Low (shapes at edges fail) | Clean but positional issues | Medium |

**Prefer text box** for any text content. Only use pen-drawn letters when text box is unavailable.

## 15. Key Performance Learnings

| Operation | Time per call | Notes |
|---|---|---|
| `activate_pen()` | ~0.75s | Shape button (0.25s) + popover (0.5s) |
| `stroke()` | ~0.75s + 0.006s × n_points | Includes activate_pen |
| `polyline(bold=True)` | 5 × (activate_pen + draw) | ~5 strokes per call |
| `bold5()` | Same as polyline bold | 5 passes |
| `bold3()` | 3 passes | ~60% of bold5 time |
| `brick_wall()` | ~136s for 182 strokes | **Too slow** — avoid at normal zoom |
| Catmull-Rom n=40 per segment | 0.006s × n_segments × n | Use n=20-25 for speed, n=40 for smooth |
| Shape placement | ~1.2s per shape | SHAPE+type+canvas + sleeps |
| `count_ink()` | ~2-5s per region | Depends on bbox size |

**Design rules:**
- Keep total pen activations < 40 for < 60s runtime
- Use `zigzag_fill` (1 stroke) not `hatch_lines` (N strokes)
- Use shapes for geometric elements (walls, roofs) + pen for details
- For zoom detail: limit zoom level to 4x (8x is ~2× slower)
- Default shape placement range: x=150-430, y=250-500

---

## 16. Freeform UI Navigation Reference

> Mapped 2026-07-04 via AppleScript accessibility introspection.
> All toolbar buttons accessible by description — no hard-coded coordinates needed.

### 16.1 Toolbar Drawing Tools

Located at y≈39 within the toolbar area (window y=32-84). Use `click_tool(name)`:

| Tool | Accessibility desc | Function |
|---|---|---|
| **Text Box** | `"Insert Text Box"` | `click_tool("text box")` |
| **Shape** | `"Insert Shape"` | `click_tool("shape")` |
| **Sticky Note** | `"Insert Sticky Note"` | `click_tool("sticky note")` |
| **Table** | `"Insert Table"` | `click_tool("table")` |
| **Media** | `"Insert Media"` | `click_tool("media")` |

### 16.2 Canvas Controls

Located below the toolbar in the split group. Use `click_canvas_control(name)`:

| Control | Accessibility desc | Function |
|---|---|---|
| **Scene Navigator** | `"Show Scene Navigator"` | `click_canvas_control("scene navigator")` |
| **Zoom Out** | `"Decrease zoom"` | `click_canvas_control("zoom out")` |
| **Zoom Menu** | `"Zoom"` | `click_canvas_control("zoom menu")` |
| **Zoom In** | `"Increase zoom"` | `click_canvas_control("zoom in")` |
| **Connectors** | `"Connectors"` | `click_canvas_control("connectors")` |
| **Grid** | `"Grid"` | `click_canvas_control("grid")` |

### 16.3 Full Menu Reference

| Menu | Key items | AppleScript path |
|---|---|---|
| **File** | New Board, New Board in New Window, Export Board as PDF, Share, Print | `menu "File" of menu bar 1` |
| **Edit** | Undo/Redo, Cut/Copy/Paste, Select All, Duplicate Selection, Find, Emoji & Symbols | `menu "Edit"` |
| **Insert** | Sticky Note, **Shape** (12 types), **Text Box**, **Table**, Line/Arrow/Connection, Generate Image, Choose Photo/Video, Link, Choose File | `menu "Insert"` |
| **Format** | **Font** (Show Fonts, Bold, Italic, Bigger/Smaller), **Text** (Align, Writing Direction), **Shapes and Lines** (Change Shape, Make Editable, Break Apart, Boolean ops, Point type), Table, Image, Shadow, Round Corners, Loop, Show Colours | `menu "Format"` |
| **Arrange** | Bring Forward/Back, Send to Front/Back, **Align Objects** (Left/Centre/Right/Top/Middle/Bottom), **Distribute Objects** (Horizontally/Vertically/Evenly), Lock/Unlock, Move to Board, Group/Ungroup, Constrain Proportions | `menu "Arrange"` |
| **View** | as Icons/List, Sort By, Show Content Hub, Show Connectors, Show Grid, Snap to Grid, **Guides** (Centre/Edge Guides, Relative Sizing/Spacing), **Zoom** (In/Out, Actual Size, Zoom to Selection, Zoom to Fit Content), Scenes, Show Tab Bar, Show Sidebar, Enter Full Screen | `menu "View"` |

### 16.4 Insert → Shape (12 types)

Accessible via `insert_shape("Rectangle")` — uses menu item lookup:

1. Rectangle
2. Rounded Rectangle
3. Oval
4. Triangle
5. Right Triangle
6. Arrow
7. Double Arrow
8. Diamond
9. Quote Bubble
10. Callout
11. Polygon
12. Star

### 16.5 Shape Formatting (post-selection)

After selecting a shape, use **Format → Shapes and Lines**:

| Operation | Description |
|---|---|
| `Change Shape` | Convert between shape types (e.g. Rectangle → Rounded Rectangle) |
| `Make Editable` | Edit individual vector points |
| `Break Apart` | Decompose into sub-paths |
| `Unite Shapes` | Boolean union |
| `Intersect Shapes` | Boolean intersection |
| `Subtract Shapes` | Boolean subtraction |
| `Exclude Shapes` | Boolean XOR |
| `Make Sharp/Smooth/Bézier Point` | Change point type |
| `Toggle Line Type` | Toggle between open/closed path |

### 16.6 Zoom and View

| Action | Method |
|---|---|
| Zoom in | `key_combo(0x37, 24)` — Cmd+Plus, or `click_canvas_control("zoom in")` |
| Zoom out | `key_combo(0x37, 27)` — Cmd+Minus, or `click_canvas_control("zoom out")` |
| Actual size (100%) | `zoom_actual_size()` |
| Zoom to fit | `zoom_to_fit()` |
| Zoom to selection | `zoom_to_selection()` |
| Toggle grid | `show_grid(True/False)` |
| Toggle connectors | `show_connectors(True/False)` |
| Toggle centre guides | `toggle_guides("centre")` |
| Toggle edge guides | `toggle_guides("edge")` |

### 16.7 Object Manipulation

| Action | Function |
|---|---|
| Select all | `select_all()` |
| Group | `group_items()` |
| Ungroup | `ungroup_items()` |
| Lock | `lock_items()` |
| Unlock | `unlock_items()` |
| Align | `align_objects("centre"/"left"/"right"/"top"/"middle"/"bottom")` |
| Distribute | `distribute_objects("horizontally"/"vertically"/"evenly")` |
| Show Colors | `show_colors()` — opens macOS color picker |
| Font bigger | `font_bigger()` |
| Font smaller | `font_smaller()` |
| Scene navigator | `scene_navigator()` |

### 16.8 Usage Patterns

```python
# NEW: Use toolbar buttons by description (no pixel coords needed)
click_tool("shape")       # Open shape palette (robust!)
click_tool("text box")    # Insert text box
click_tool("table")       # Insert table
click_canvas_control("grid")      # Toggle grid on/off
click_canvas_control("zoom in")   # Zoom in via UI

# Menu-based shape insertion (for precise shape selection)
insert_shape("Rounded Rectangle")
insert_shape("Oval")
insert_shape("Star")

# Object manipulation workflow
select_all()              # Select everything
align_objects("centre")   # Centre-align
group_items()             # Group into one object
lock_items()              # Lock in place

# Zoom management
zoom_actual_size()        # Reset to 100%
zoom_to_fit()             # Fit all content in view
```

### 16.9 Performance Trade-offs

| Method | Reliability | Speed | Best for |
|---|---|---|---|
| Click by accessibility | High (immune to UI drift) | ~0.5s | Toolbar buttons, canvas controls |
| Click by pixel coordinate | Low (drifts with UI updates) | ~0.05s | Popover items, canvas placement |
| Menu bar AppleScript | High | ~0.3s | Menu navigation, shape insertion |

**When to use each:**
- Use `click_tool("shape")` instead of `click(405, 58)` — always more reliable
- Use `click(x, y)` for canvas placement (no accessibility target on canvas)
- Use `insert_shape("Rectangle")` when you need a specific shape without the popover
- Pen popover remains pixel-coordinated as it's a transient popover (no accessibility handle)

---

## 17. Drawing Fundamentals Curriculum (L5b — New 2026-07-04)

Extracted from RapidFireArt (10 lessons), Proko Drawing Basics (185 lessons), Kesh Art Begin Drawing (7 days), and Ctrl+Paint Draw 1.

Fundamentals organized in 5 skill tiers, each building on the previous:

```
Tier 1: LINE      — line quality, warmups, ghosting, tapered strokes
Tier 2: SHAPE     — simplification, overall structure, secondary shapes
Tier 3: FORM      — 2D → 3D, contour lines, planes, constructive drawing
Tier 4: PERSPECTIVE — horizon line, vanishing points, 1/2/3-point grids
Tier 5: VALUE     — shading, cross-hatching, form shading, stippling
```

### 16.1 Shading Techniques (Value + Edge)

| Function | What it does | Source |
|---|---|---|
| `hatch_fill(x1,y1,x2,y2,angle,spacing,bold)` | Parallel hatching at any angle | Proko Value |
| `crosshatch_fill(x1,y1,x2,y2,angle1,angle2,spacing,bold)` | Two-layer cross-hatching | RFA Lesson 8 |
| `stipple_fill(x1,y1,x2,y2,density,size)` | Dot stippling pattern (reproducible) | RFA Lesson 8 |
| `form_shading(cx,cy,rx,ry,light_angle,n_bands)` | Curved contour-hatching following surface | Proko Edge |

```python
# Cross-hatch a shadow area under an object
crosshatch_fill(300, 460, 360, 480, angle1=45, angle2=-45, spacing=3)

# Form shading on a curved surface
form_shading(330, 400, 100, 120, light_angle=45, n_bands=6)
```

### 16.2 Perspective (Spatial Depth)

| Function | What it does | Source |
|---|---|---|
| `perspective_grid(cx,cy,vpx,vpy,horizon_y,n_lines,extent)` | Full perspective grid: horizon + converging + transverse lines | RFA Lesson 6, Proko |
| `vanishing_point(x,y,n_rays,r)` | Mark VP with radiating construction lines | Proko |

```python
# Set up a 1-point perspective scene
perspective_grid(330, 400, 330, 250, horizon_y=250, n_lines=8, extent=600)
vanishing_point(330, 250)
```

### 16.3 Form Construction (2D → 3D)

| Function | What it does | Source |
|---|---|---|
| `contour_rings(cx,cy,rx,ry,n_rings,n_pts,bold)` | Contour rings describing ellipsoid surface | RFA Lesson 3 |
| `constructive_box(cx,cy,w,h,depth,angle)` | Isometric 3D box with visible back faces | Ctrl+Paint Constructive Form |
| `constructive_cylinder(cx,cy,r,h)` | Cylinder with top/bottom ellipses + body contour rings | RFA Lesson 3 |

```python
constructive_cylinder(330, 400, 80, 180)
contour_rings(330, 380, 100, 80, n_rings=4)
```

### 16.4 Proportion Tools

| Function | What it does | Source |
|---|---|---|
| `proportion_grid(x1,y1,x2,y2,cols,rows)` | Measurement grid overlay for reference mapping | Ctrl+Paint Visual Measuring |
| `visual_measure(x,y,direction,units,unit_length)` | Sight-size ruler with tick marks | Ctrl+Paint |

```python
proportion_grid(100, 200, 560, 500, cols=4, rows=4)
```

### 16.5 Warm-ups (Line Quality + Muscle Memory)

| Function | What it does | Source |
|---|---|---|
| `warmup_lines(n,x1,x2,y_start,step)` | Parallel line drills (shoulder/elbow motion) | Proko Line, Kesh Day 1 |
| `warmup_ellipses(n,cx,cy,r_min,r_max)` | Concentric ellipse control practice | Ctrl+Paint Ellipse Control |
| `warmup_ghost_boxes(n,x1,y1,w,h)` | Ghosted box drawing practice | Proko Ghosting |
| `warmup_circles(n,cx,cy,r_min,r_max)` | One-stroke circle control drills | Drawabox Lesson 1 |

```python
# 2-minute warmup before a real drawing
setup()
warmup_lines(n_lines=15, x1=100, x2=500, y_start=300, step=12)
warmup_ellipses(n=8, cx=330, cy=400, r_min=20, r_max=100)
warmup_circles(n=5, cx=330, cy=400, r_min=15, r_max=70)
```

### 16.6 Constructive Drawing Workflow

| Function | What it does | Source |
|---|---|---|
| `constructive_draw(shape_pts, form_fn, detail_fn, slp)` | 3-stage workflow: overall shape → form → detail | RFA Lesson 2-3 |
| `still_life_setup()` | Table + backdrop for still life composition | Ctrl+Paint Still Life |

**3-stage method (RFA Lesson 2):**
1. Overall structure — sketch the bounding shape (squint until details fade)
2. Secondary shapes — identify sub-shapes within
3. Define subject — refine into the final form

```python
def apple_form():
    contour_rings(330, 400, 40, 50, n_rings=3)

def apple_detail():
    polyline([(330, 440), (330, 460)])  # stem
    leaf(330, 455, 12, 8)               # leaf

constructive_draw(
    [(330, 340), (290, 360), (290, 430), (330, 450), (370, 430), (370, 360), (330, 340)],
    form_fn=apple_form,
    detail_fn=apple_detail
)
```

## 18. Lesson Plan Integration

For a structured Freeform practice session, follow this sequence (Kesh Art 7-day + RFA 10-lesson):

### Session Template (20-30 min)
```python
from freeform_engine import *
setup()

# Phase 1: Warm-ups (2 min)
warmup_lines(n_lines=12, x1=100, x2=500, y_start=300, step=12)
warmup_ellipses(n=6, cx=330, cy=400, r_min=20, r_max=100)

# Phase 2: Shape simplification (5 min) — 3 objects as stacked shapes
rect_outline(280, 350, 380, 440)
circle_outline(330, 340, 20)
polyline(catmull([(280, 350), (285, 330), (375, 330), (380, 350)], n=20))

# Phase 3: Form construction (5 min) — convert shapes to 3D
constructive_cylinder(330, 400, 50, 120)

# Phase 4: Shading practice (5 min)
crosshatch_fill(300, 450, 360, 480, angle1=45, angle2=-45, spacing=3)

# Phase 5: Perspective study (5 min)
perspective_grid(330, 300, 330, 200, horizon_y=200, n_lines=6, extent=500)
```

## 19. Composition Recipes (new from fundamentals)

### 18.1 Still life with shading
```python
setup()
still_life_setup()
constructive_cylinder(250, 380, 40, 100)   # cup
constructive_cylinder(400, 390, 30, 80)    # bottle
circle_outline(320, 370, 25)               # apple
crosshatch_fill(200, 490, 500, 510, angle1=35, angle2=-35, spacing=3)
```

### 18.2 3D scene with perspective
```python
setup()
perspective_grid(330, 300, 330, 200, horizon_y=200, n_lines=6, extent=500)
constructive_box(330, 300, 120, 80, depth=50, perspective_angle=20)
constructive_cylinder(200, 370, 25, 60)
constructive_cylinder(460, 370, 25, 60)
```

### 18.3 Form study
```python
setup()
contour_rings(200, 380, 50, 60, n_rings=5)   # organic form
contour_rings(330, 380, 80, 80, n_rings=6)    # sphere study
contour_rings(460, 380, 60, 30, n_rings=4)    # flattened form
form_shading(330, 380, 80, 80, light_angle=315, n_bands=5)
```

---

## 20. Tool Behavior Reference (Empirical)

> Each tool tested on Freeform (macOS Tahoe 26). Ink measured via `count_ink()` in a
> tight bbox around the placed element. All shapes placed at default size.

### 20.1 Shape Types — Default Ink Output

| Shape | Ink (px) | Notes |
|---|---|---|
| Rectangle | 11,293 | Thin outline, white fill |
| Rounded Rectangle | 13,130 | Slightly more ink due to corner curves |
| Oval | 13,003 | Smooth ellipse |
| Triangle | 526 | Very thin — filled triangle has little visible stroke |
| Right Triangle | 24 | Nearly invisible — likely tiny default size |
| Arrow | 3,002 | Arrowhead shape, moderate ink |
| Double Arrow | 13,012 | Two arrowheads, well-inked |
| Diamond | 10,906 | Rhombus outline |
| Quote Bubble | 8,586 | Speech bubble with tail |
| Callout | 13,776 | Box with pointer line |
| Polygon | 12,482 | Default pentagon/hexagon |
| Star | 8,342 | 5-pointed star |

**Rule:** Rectangle, Rounded Rect, Oval, Diamond, Double Arrow, and Callout produce the most ink. Triangle and Right Triangle produce very little — prefer other shapes or use the pen tool for small triangles.

### 20.2 Native Elements — Ink Output

| Element | Ink (px) | Notes |
|---|---|---|
| Text Box ("Hello Freeform") | 15,648 | Default font ~12pt, black text |
| Text Box + Bigger font (×2) | 5,393 | Larger glyphs, auto-scaled bbox |
| Text Box + Align Centre | ~84 | Same as normal text box (text region) |
| Sticky Note | 5,636 | Yellow note with text |
| Table (3×3 default) | 27,297 | Grid with cell borders — high ink density |
| Line | 3,804 | Straight line segment |
| Line with Arrowhead | 5,412 | Arrow tip at end |
| Connection Line | 4,126 | Right-angle connection path |
| Rectangle + Shadow | 19,095 | Shadow adds ~7,800 ink (41% increase) |
| Rectangle + Round Corners | 13,422 | Modest increase over plain rectangle |
| Rectangle + Loop | 11,035 | Looping/endless effect applied |

**Key insights:**
- Text box is denser (more ink) than pen-drawn text for the same content — always prefer text box
- Shadow adds significant visual weight (~40% ink increase) — use sparingly
- Table has the highest ink density of any element — useful for grid-based compositions
- Arrowhead adds ~1,600 ink over a plain line

### 20.3 Shape Boolean Operations

Four boolean operations on the **Format → Shapes and Lines → (Unite / Intersect / Subtract / Exclude)** menu:

| Operation | Result | Ink (test) | Use case |
|---|---|---|---|
| **Unite Shapes** | Merges two shapes into one compound path | 18,210 | Combine overlapping elements |
| **Intersect Shapes** | Keeps only the overlapping area | 19,695 | Create crescent/clip shapes |
| **Subtract Shapes** | Front shape cuts away from back | 8,646 | Cutout windows, donut shapes |
| **Exclude Shapes** | Removes overlapping area, keeps rest | — | XOR-like mask |

**Workflow:**
1. Place two overlapping shapes (e.g., Rectangle + Oval)
2. `Edit → Select All` (or Shift+click both)
3. `Format → Shapes and Lines → Unite (or Intersect/Subtract/Exclude)`
4. Result is a single compound shape with the combined/intersected outline

Equivalent AppleScript:
```python
menu_click("Edit", "Select All")
# then
format_shapes_lines("Unite Shapes")
```

### 20.4 Shape Editing Operations

| Operation | What it does | Visible effect |
|---|---|---|
| **Make Editable** | Activates vector point editing | Shows control points (low ink, ~700px) |
| **Break Apart** | Decomposes compound shape | Splits into subpaths (12,511px) |
| **Change Shape → X** | Converts between shape types | Shape redraws (9,204px for →Rounded Rect) |
| **Toggle Line Type** | Open/closed path toggle | Changes stroke endpoints (13,939px) |
| **Make Sharp Point** | Corner point type | Affects existing editable points |
| **Make Smooth Point** | Smooth curve point | Affects existing editable points (24px) |
| **Make Bézier Point** | Bézier control point | Full Bézier handles |

**Important:** Make Editable must be applied before point type changes work.
Change Shape can convert to any of the 12 shape types without re-placing.

### 20.5 View Controls

All work via accessibility button clicks:

| Control | Function | AppleScript |
|---|---|---|
| **Grid** | Toggle grid overlay | `click_canvas_control("grid")` |
| **Connectors** | Toggle connector visibility | `click_canvas_control("connectors")` |
| **Centre Guides** | Show/hide centre alignment guides | `toggle_guides("centre")` |
| **Edge Guides** | Show/hide edge alignment guides | `toggle_guides("edge")` |
| **Snap to Grid** | Toggle snap behavior | `menu_click("View", "Snap to Grid")` |
| **Zoom In/Out** | By ±1 step | `click_canvas_control("zoom in")` / `click_canvas_control("zoom out")` |
| **Zoom menu** | Dropdown zoom level | `click_canvas_control("zoom menu")` |
| **Scene Navigator** | Toggle left sidebar | `scene_navigator()` |

### 20.6 Guide Types

| Guide | Behavior |
|---|---|
| **Centre Guides** | Show vertical/horizontal center lines when object is near canvas center |
| **Edge Guides** | Show alignment lines when object edges align with other objects |
| **Relative Sizing** | Show size indicators when objects match dimensions |
| **Relative Spacing** | Show spacing indicators between evenly-spaced objects |

### 20.7 Interactive Tools (not fully automatable)

| Tool | Opens | Notes |
|---|---|---|
| **Generate Image** | Apple Intelligence image generation dialog | Requires user prompt input |
| **Choose Photo or Video** | macOS file picker | Requires file selection |
| **Show Colours** | macOS color picker (Shift+Cmd+C) | Can close with Escape |
| **Browse Content Hub** | Content browser sidebar | Requires network content |

### 20.8 Object Manipulation

| Operation | AppleScript / Function | Notes |
|---|---|---|
| Select All | `menu_click("Edit", "Select All")` or `select_all()` |  |
| Duplicate Selection | `menu_click("Edit", "Duplicate Selection")` | Creates copy offset by ~20px |
| Group | `group_items()` or `menu_click("Arrange", "Group")` |  |
| Ungroup | `ungroup_items()` |  |
| Lock | `lock_items()` | Prevents movement/editing |
| Unlock | `unlock_items()` |  |
| Align | `align_objects("centre"/"left"/"right"/"top"/"middle"/"bottom")` | Requires ≥2 selected |
| Distribute | `distribute_objects("horizontally"/"vertically"/"evenly")` | Requires ≥3 selected |
| Constrain Proportions | `menu_click("Arrange", "Constrain Proportions")` | Toggle |
| Bring Forward/Back | `menu_click("Arrange", "Bring Forward")` | Z-order |
| Send to Front/Back | `menu_click("Arrange", "Bring to Front")` | Z-order extremes |

### 20.9 Text Styling (Format → Font / Text)

| Style | Method |
|---|---|
| **Bold** | `menu_click("Format", "Bold")` or Cmd+B |
| **Italic** | `menu_click("Format", "Italic")` or Cmd+I |
| **Underline** | `menu_click("Format", "Underline")` or Cmd+U |
| **Bigger** | `font_bigger()` or Cmd+Shift++ |
| **Smaller** | `font_smaller()` or Cmd+Shift+- |
| **Show Fonts** | `menu_click("Format", "Show Fonts")` or Cmd+T |
| **Align Left/Center/Right/Justify** | Via `Format → Text → Align X` |
| **Writing Direction** | LTR/RTL toggle via `Format → Text → Writing Direction` |
| **Autosize Text** | Auto-resize text box to content via `Format → Text → Autosize Text` |

**Best practice for text:**
1. `click_tool("text box")` then click canvas position
2. Wait 1s for text box to appear and be selected
3. Set clipboard content via `subprocess.run(["osascript", "-e", 'set the clipboard to "..."'])`
4. `key_combo(0x37, 9)` — Cmd+V to paste
5. Apply font size/style via menu
6. `keystroke(53)` — Escape to deselect

### 20.10 Scene Management

| Operation | Method |
|---|---|
| **New Board** | `new_board()` or Cmd+N |
| **New Board in New Window** | `menu_click("File", "New Board in New Window")` |
| **New Tab** | `menu_click("File", "New Tab")` or Cmd+T |
| **Close** | `menu_click("File", "Close")` or Cmd+W |
| **Delete Board** | `menu_click("File", "Delete")` |
| **Export as PDF** | `menu_click("File", "Export Board as PDF")` |
| **Move Items to Board** | `menu_click("Arrange", "Move Items to Board")` |

---

## 21. Freeform Hacking Reference (Internal Architecture + Exploits)

> Internal architecture discovered 2026-07-04 via binary analysis, SQLite inspection, accessibility introspection, and systematic tool testing.

### 21.1 Core Architecture (No AppleScript)

| Property | Value |
|---|---|
| **AppleScript** | NOT supported — no `sdef`, no `.scriptTerminology`, no `.scriptSuite` |
| **App Intents** | SUPPORTED — ~25+ intent classes (CRLCreateBoardIntent, CRLAddItemToBoardIntent, etc.) |
| **Shortcuts integration** | Via App Intents framework, but **no prebuilt shortcuts** exist for Freeform |
| **URL scheme** | `freeform://board?id=<uuid>` — opens specific board |
| **Universal Links** | `https://www.icloud.com/freeform/` and `.../freeform-folder/` and `.../freeform-copy` |
| **Handoff types** | `com.apple.freeform.viewModelItemHandoff`, `com.apple.freeform.viewModelDrag` |
| **Automator** | No actions |
| **Services** | None (only system defaults) |
| **Share Sheet** | FreeformSharingExtension.appex (images, URLs, text, RTF, movies, map items) |
| **USD Renderer** | USDRendererExtension.appex (3D model rendering) |

**Bottom line:** Freeform is NOT AppleScript-scriptable. Automation path is via Shortcuts (App Intents) or direct SQLite manipulation.

### 21.2 Storage Layer — SQLite CRDT Database

Boards are stored in a SQLite database, NOT as `.board` files on macOS.

| Location | Contents |
|---|---|
| `~/Library/Group Containers/group.com.apple.freeform/Boards/boards.db` | **Main database** — all board data, items, assets, metadata |
| `~/Library/Group Containers/group.com.apple.freeform/Boards/side.db` | Board load/open marks |
| `~/Library/Group Containers/group.com.apple.freeform/Boards/Assets/` | Raw asset files (UUID-named: `.svg`, `.png`, `.jpg`, `.pdf`, `.tiff`) |
| `~/Library/Group Containers/group.com.apple.freeform/BoardPreviewImages/` | Cached preview images |
| `~/Library/Containers/com.apple.freeform/Data/Library/Caches/BoardPreviewImages/` | Additional preview cache |
| `~/Library/Preferences/com.apple.freeform.plist` | Preferences |

#### Schema — `boards` table

```sql
board_identifier BLOB PRIMARY KEY -- UUID
owner_name TEXT
container_uuid BLOB
data BLOB              -- CRDT protobuf (prefix: "crdt\x06\x00\x00\x00")
last_activity_time REAL
tombstoned INTEGER
```

#### Schema — `board_items` table

```sql
item_uuid BLOB NOT NULL
parent_uuid BLOB
board_identifier BLOB
item_type INTEGER     -- Known: 2, 3, 4, 5, 10, 12
common_data BLOB     -- CRDT protobuf (crdt\x06 prefix)
specific_data BLOB   -- CRDT protobuf (crdt\x06 prefix)
tombstoned INTEGER
sub_item_type INTEGER DEFAULT 0
```

**Known `item_type` values:**
| Type | Likely meaning |
|---|---|
| 2 | ? |
| 3 | ? |
| 4 | ? |
| 5 | ? |
| 10 | ? |
| 12 | Photo/image (has asset_references) |

#### Schema — `assets` / `asset_references`

```sql
assets(asset_uuid BLOB PK, extension TEXT, tombstone_date REAL)
asset_references(referrer_identifier BLOB, board_identifier BLOB,
    referrer_asset_name TEXT, asset_uuid BLOB, referrer_type INTEGER)
```

**Known extensions in Assets:** `.svg`, `.png`, `.jpg`, `.pdf`, `.tiff`

**Blob format:** All `data` blobs start with `6372647406000000` ("crdt" + version 6). This is Apple's **CRDT framework** (Conflict-free Replicated Data Type) with protobuf-serialized payloads — NOT plain plist or JSON.

**Container marker:** `~/Library/Containers/com.apple.freeform/Data/Library/Freeform/Boards` contains the text "Migrated to group container" — confirming boards moved to the shared group container.

### 21.3 Shape Library — 1000+ Built-in Shapes

Freeform ships with a massive built-in shape library at:
`/System/Applications/Freeform.app/Contents/Resources/shape_library.json`

| Property | Value |
|---|---|
| **Format** | JSON, ~5.2 MB |
| **Version ID** | `S4214C3270` |
| **Shape count** | ~1000+ unique shapes |
| **Categories** | 15 categories (Geometry, Objects, Nature, People, Food, Technology, etc.) |
| **Shape IDs** | Numeric (e.g. 277, 877, 95, 672, 569, 950) |
| **Localization** | Shape names via `CRLShapeLibrarianShapeNames.loctable` (620KB) |
| **Keywords** | Search keywords via `CRLShapeLibrarianKeywords.loctable` (3.1MB) |

**Category structure:**
```json
{
  "id": 59,
  "localizationKey": "Geometry_59",
  "shapeIDs": [569, 950, 951, 982, 563, 948, 949, 954, ...]
}
```

**The 12 basic shapes** (Insert → Shape menu) are just the tip of the iceberg. The full library has categorized shapes accessible via:
- **Content Hub** (`Insert → Browse Content Hub`)
- **Shape palette popover** (click Shape toolbar button)
- **Search** within the shape picker

**Hack:** The `shape_library.json` contains SVG path data for all 1000+ shapes. These could be extracted, modified, and re-injected as custom SVG assets.

### 21.4 Brush/Ink System — SVG-Based Custom Brushes

Freeform's pen/pencil/crayon/chalk tools use SVG-based brush definitions:

```
/System/Applications/Freeform.app/Contents/Resources/
  CRLBrush_Basic.svg            — Basic pen
  CRLBrush_Basic Rounded.svg    — Rounded pen
  CRLBrush_Basic Square.svg     — Square pen
  CRLBrush_Chalk2.svg           — Chalk (281KB — complex noise texture)
  CRLBrush_Crayon.svg           — Crayon (99KB)
  CRLBrush_Dry Brush.svg        — Dry brush (453KB — heaviest)
  CRLBrush_Feathered Brush.svg  — Feathered brush (33KB)
  CRLBrush_Pen.svg              — Pen (20KB)
  CRLBrush_Pencil.svg           — Pencil (82KB)
```

**Hack:** The brush SVGs could be modified to create custom brush textures. Freeform's rendering pipeline converts these SVG strokes into actual ink on canvas. Replacing the SVGs (requires SIP disable or codesign) or creating new brush definitions would give custom drawing tools.

**Shadow effect** uses custom CIKernels:
```
CRLCurvedShadow_BlurBlend.cikernel
CRLCurvedShadow_CurveDisplacement.cikernel
```

### 21.5 Menu Exploits — Complete Untested Format Submenus

The following Format submenus exist but were NOT tested in the exploration session:

#### Image Menu (Format → Image)
| Item | Description |
|---|---|
| **Edit Mask** | Enter image mask editing mode |
| **Reset Mask** | Remove mask from image |
| **Mask With Shape** | Clip image to a shape |
| **Generate from Image** | Apple Intelligence image generation from source |
| **Super Resolution** | ML-based image upscaling |
| **Remove Background** | ML-based subject isolation |

**Hack pipeline:** Insert photo → Super Resolution (upscale) → Remove Background (matte) → Mask With Shape (frame) → compositing → export. This is a full image processing pipeline inside Freeform.

#### Table Menu (Format → Table)
| Item | Description |
|---|---|
| Add Row Above/Below | Row insertion |
| Add Column Before/After | Column insertion |
| Delete Row/Column | Removal |
| Resize Rows/Columns to Fit Content | Auto-sizing |
| Distribute Rows/Columns Evenly | Equal spacing |

#### Style Copy/Paste
| Item | Description |
|---|---|
| **Copy Style** | Copy visual properties (stroke, fill, shadow, etc.) |
| **Paste Style** | Apply copied style to selection |
| **Save as Insert Style** | Save current style as default for new inserts |

**Hack:** `Save as Insert Style` + automation = create a style template once, then every new element inherits it. Useful for themed boards.

### 21.6 The Quartz Renderer + Import Pipeline (PRIMARY APPROACH)

The definitive approach for getting content into Freeform:

```python
from freeform_renderer import Canvas

c = Canvas(660, 700)
c.background()
# ... draw everything with Quartz CGContext ...
c.save("/tmp/art.png")

# Method A: Clipboard paste (preferred — no file dialog)
import AppKit, subprocess, time
img = AppKit.NSImage.alloc().initWithContentsOfFile_("/tmp/art.png")
AppKit.NSPasteboard.generalPasteboard().clearContents()
AppKit.NSPasteboard.generalPasteboard().writeObjects_([img])
subprocess.run(["osascript", "-e", '''
    tell app "System Events"
        tell process "Freeform"
            keystroke "v" using command down
        end tell
    end tell
'''])
time.sleep(1)

# Method B: Menu import (Insert → Choose Photo or Video)
# Works but file dialog navigation is fragile

# Method C: open -a Freeform image.png
# Opens Freeform with the image in a new board
```

**The canvas size (660x700) matches Freeform's visible window area at 1x.** At retina 2x, Freeform renders at 2x logical resolution.

### 21.7 Canvas Content — Not Exposed to Accessibility

**Critical limitation:** Freeform's canvas uses a custom rendering engine (likely SceneKit or Metal). The AXScrollArea behind the visible canvas has:

```
AXContents: empty list (0 items)
AXContentSize: "3194 x 3194" (enormous canvas scroll area)
Children: only scroll bars (2)
AXChildrenInNavigationOrder: 0 items
```

**No shapes, text, images, or drawings are exposed as accessibility elements.** This means:
- Cannot read canvas content via AX API
- Cannot select elements by accessibility identifier
- Cannot verify content without screenshots

**Workaround:** Screenshot + pixel analysis (`count_ink()`) or Vision framework OCR.

### 21.8 Inventory of All 12 Shape Types (reality-checked)

| Shape | Approx ink | Best for |
|---|---|---|
| Rectangle | 11,293 | Boxes, frames, backgrounds |
| Rounded Rect | 13,130 | UI elements, cards |
| Oval | 13,003 | Orbits, faces, wheels |
| Triangle | 526 | Tiny — avoid for structural elements |
| Right Triangle | 24 | Too small — use Oval or Diamond instead |
| Arrow | 3,002 | Direction indicators |
| Double Arrow | 13,012 | Bidirectional indicators |
| Diamond | 10,906 | Pointers, markers |
| Quote Bubble | 8,586 | Speech bubbles, callouts |
| Callout | 13,776 | Annotations, labels (HIGHEST ink) |
| Polygon | 12,482 | Custom N-gons (edit points) |
| Star | 8,342 | Accents, badges |

### 21.9 Boolean Operations — Vector Sculpting Toolkit

Freeform's Format → Shapes and Lines menu provides 4 boolean operations:

| Operation | Effect | Use case |
|---|---|---|
| **Unite Shapes** | Union of two paths | Combine elements |
| **Intersect Shapes** | Keep only overlap | Clip regions |
| **Subtract Shapes** | Front cuts back | Cutouts, negative space |
| **Exclude Shapes** | XOR mask | Invert overlap area |

**Sculpting workflow:** Insert base shapes → Unite → Make Editable → point editing → style → composite.

### 21.10 Freeform's Internal Frameworks

Interesting frameworks inside the app bundle:
```
TSImageGeneration.framework    — Apple Intelligence image gen
TSUtility.framework            — General utilities
TSMediaLibrary.framework       — Media library/browser
TSAccessibility.framework      — Accessibility helpers
AppsGen.framework              — App Intents generation
```

### 21.11 Quick Reference — All Shortcuts CLI Commands

```bash
shortcuts list                              # List all shortcuts
shortcuts list --show-identifiers           # With UUIDs
shortcuts run "Name"                        # Run a shortcut
shortcuts run "Name" -i input.txt           # With input
shortcuts run "Name" -o output.txt          # Capture output
shortcuts view "Name"                       # Open in Shortcuts app
shortcuts sign -i input -o output           # Sign a shortcut
open "freeform://board?id=<uuid>"           # Open specific board
open "https://www.icloud.com/freeform/"     # Open web version
```

---

## 22. Quartz CGContext Renderer — Complete Reference

> **Primary drawing engine as of 2026-07-04.** Renders via CoreGraphics CGBitmapContext (no CGEventPost mouse simulation). Imports into Freeform via clipboard paste.

### 22.1 Architecture

```
Python script → Canvas(w, h) → CGBitmapContext → Quartz CGContext API → PNG export → NSImage → NSPasteboard → Cmd+V into Freeform
```

**Key file:** `~/.opencode_knowledge/scripts/freeform_renderer.py` (366 lines)

### 22.2 Canvas Class — Complete API

#### Construction

```python
Canvas(w=660, h=700, scale=2)
```

- Creates CGBitmapContext at `w×scale` × `h×scale` (default 1320×1400)
- Pixel format: `kCGBitmapByteOrder32Host | kCGImageAlphaPremultipliedFirst` (BGRA on little-endian)
- Applies CTM flip: `CGContextTranslateCTM(ctx, 0, h)` + `CGContextScaleCTM(ctx, 1, -1)` — fixes bottom-left origin to top-left

#### CTM Flip Fix (CRITICAL)

```python
CGContextTranslateCTM(self.ctx, 0, self.h)
CGContextScaleCTM(self.ctx, 1, -1)
```

- CGBitmapContext origin is bottom-left; canvas coordinates are top-left
- **Order matters:** Translate FIRST, then Scale. Reversed order flips around wrong origin and draws off-screen
- After flip: `(0, 0)` in canvas → `(0, h×scale)` in Quartz
- All `proj()` output in user scripts returns canvas coordinates — the `c.*` methods scale internally

#### Coordinate System

| Space | Origin | Scale | Notes |
|---|---|---|---|
| Canvas (user) | top-left, (0,0) | 1× (660×700) | User draws here |
| Buffer (Quartz) | bottom-left | 2× (1320×1400) | Internal — all methods scale ×2 |

#### Method Reference

| Method | Signature | Behavior |
|---|---|---|
| `bg` | `bg(r,g,b)` | Fill whole canvas with solid color |
| `gs` | `gs()` | `CGContextSaveGState` — push state |
| `gr` | `gr()` | `CGContextRestoreGState` — pop state |
| `sc` | `sc(color, a=None)` | Set stroke color. Color: `(r,g,b)` or `(r,g,b,a)` in 0-1 |
| `fc` | `fc(color, a=None)` | Set fill color. Same format as sc |
| `lw` | `lw(w)` | Set line width (will be ×2 internally) |
| `line` | `line(x1,y1,x2,y2)` | Draw single line segment. **NO gs/gr wrapper** — uses current stroke |
| `polyline` | `polyline(pts)` | Draw connected line through all points. **NO gs/gr wrapper** |
| `rect` | `rect(x1,y1,x2,y2, f=None, s=None)` | Rectangle. If f: fill. If s or both None: stroke. Has internal gs/gr |
| `ellipse` | `ellipse(cx,cy,rx,ry, f=None, s=None)` | Oval. Same f/s logic as rect |
| `circle` | `circle(cx,cy,r, f=None, s=None)` | Circle alias for ellipse |
| `fill_path` | `fill_path(pts)` | Fill closed polygon. Points are canvas coords |
| `fill_curve` | `fill_curve(pts, n=30)` | Fill closed Catmull-Rom curve |
| `gradient_linear` | `gradient_linear(x1,y1,x2,y2, colors, locations=None)` | Linear gradient between two points. Colors: list of (r,g,b) or (r,g,b,a). Uses `kCGGradientDrawsBeforeStartLocation\|kCGGradientDrawsAfterEndLocation` |
| `gradient_radial` | `gradient_radial(cx,cy,r1, cx2,cy2,r2, colors, locations=None)` | Radial gradient between two circles |
| `clip_rect` | `clip_rect(x1,y1,x2,y2)` | Clip subsequent drawing to rectangle |
| `draw_image` | `draw_image(path, x=0, y=0, w=None, h=None)` | Direct pixel buffer write (bypasses CTM). Uses BGRA byte order on little-endian |
| `catmull` | `catmull(pts, n=20)` | Catmull-Rom spline polyline (non-closed) |
| `bezier` | `bezier(p0, p1, p2, p3)` | Cubic Bézier curve |
| `arc` | `arc(cx, cy, r, sa, ea)` | Arc from start angle to end angle (degrees) |
| `save` | `save(path)` | Export CGBitmapContext → PNG at 1× scale |
| `show` | `show(path="/tmp/freeform_drawing.png")` | Save + paste into Freeform via clipboard |

#### Color Handling

```python
def _norm(c):
    """Normalize any color tuple to 0-1 range."""
    return tuple(x / 255.0 if max(c) > 1 else x for x in c)
```

Both `sc()` and `fc()` call `_norm()` internally — accept both 0-1 and 0-255 color values.

#### Performance Notes

| Operation | Speed | Notes |
|---|---|---|
| `line()` | ~1µs | No gs/gr — very fast |
| `rect(f=color)` | ~5µs | Has internal gs/gr |
| `fill_path(10 pts)` | ~2µs | No gs/gr internally |
| `gradient_linear` | ~10µs | Creates CGGradient |
| `circle(f=color)` | ~5µs | Delegates to ellipse |
| Batch 1000 lines | ~1ms | If in single gs/gr block |

**Optimization principle:** Use a single `c.gs()/c.gr()` pair around batched calls. `c.sc()` and `c.lw()` modify the current gstate — no need for per-element gs/gr unless colors change.

### 22.3 Draw Image — Pixel Buffer Write Details

```python
def draw_image(self, path, x=0, y=0, w=None, h=None):
```

**Memory layout:** CGBitmapContext backing store is `self.buf` (ctypes string buffer). With `kCGBitmapByteOrder32Host | kCGImageAlphaPremultipliedFirst`:

| Byte offset | Content (little-endian arm64/x86_64) |
|---|---|
| 0 | Blue |
| 1 | Green |
| 2 | Red |
| 3 | Alpha |

**Row order:** Buffer row `r` stores Quartz y = `(h-1)-r`. Buffer row 0 = bottom of Quartz space = top of saved PNG after `save()`.

**Direct buffer write bypasses CTM entirely.** The method:
1. Reads PIL image
2. Resizes to target canvas resolution (×2 scale)
3. Writes BGRA pixels directly into buffer using `np.frombuffer`

### 22.4 Color Ranges for Realism

#### Sky

| Element | Color (0-1) |
|---|---|
| Sky top (deep blue) | (0.50, 0.65, 0.82) |
| Sky bottom (haze) | (0.82, 0.87, 0.93) |
| Distant haze line | (0.70, 0.78, 0.88, α0.3) |

#### Glass Buildings

| Face | Blue glass | Green glass |
|---|---|---|
| Right (east, sunlight) | (0.62, 0.70, 0.82) | (0.55, 0.75, 0.60) |
| Left (north, shaded) | (0.52, 0.60, 0.72) | (0.45, 0.65, 0.50) |
| Top (direct light) | (0.78, 0.84, 0.92) | (0.70, 0.88, 0.75) |

#### Non-glass Buildings

| Material | Right | Left | Top |
|---|---|---|---|
| Concrete | (0.78, 0.76, 0.70) | (0.68, 0.66, 0.60) | (0.88, 0.86, 0.80) |
| Brick | (0.72, 0.58, 0.48) | (0.62, 0.48, 0.38) | (0.82, 0.68, 0.58) |
| White stone | (0.82, 0.82, 0.80) | (0.72, 0.72, 0.70) | (0.92, 0.92, 0.90) |
| Steel | (0.58, 0.60, 0.65) | (0.48, 0.50, 0.55) | (0.68, 0.70, 0.75) |

#### Windows (Lit at Day)

| Type | Color | Alpha |
|---|---|---|
| Bright window | (0.9-1.0, 0.85-0.9, 0.55-0.7) | 0.4-0.85 |
| Dim window | (0.5, 0.5, 0.5) | 0.2-0.3 |
| Dark window | (0.25, 0.28, 0.35) | 0.3 |

### 22.5 Clipboard Paste into Freeform (Import Pipeline)

```python
import AppKit, subprocess, time
subprocess.run(['osascript', '-e', 'tell app "Freeform" to activate'],
               capture_output=True)
time.sleep(0.3)
subprocess.run(['osascript', '-e', '''
    tell app "System Events"
        tell process "Freeform"
            click menu item "New Board" of menu "File" of menu bar 1
        end tell
    end tell
'''], capture_output=True)
time.sleep(1.2)
ns_img = AppKit.NSImage.alloc().initWithContentsOfFile_(out_path)
AppKit.NSPasteboard.generalPasteboard().clearContents()
AppKit.NSPasteboard.generalPasteboard().writeObjects_([ns_img])
time.sleep(0.2)
subprocess.run(['osascript', '-e', '''
    tell app "System Events"
        tell process "Freeform"
            keystroke "v" using command down
        end tell
    end tell
'''], capture_output=True)
time.sleep(1)
```

**Critical: The 1.2s sleep after "New Board" is mandatory** — Freeform needs time to create the board canvas before paste target exists.

## 23. Isometric Projection System

### 23.1 Projection Math

Standard isometric projection (45° × 30°):

```python
COS30 = math.cos(math.radians(30))  # ≈ 0.8660254
SIN30 = math.sin(math.radians(30))  # = 0.5

def project(x, y, z=0):
    """3D world coords → 2D canvas coords."""
    sx = CX + (x - y) * COS30 * SCALE
    sy = CY + (x + y) * SIN30 * SCALE - z * SCALE
    return sx, sy
```

| Variable | Meaning |
|---|---|
| `x, y` | World coordinates on ground plane |
| `z` | Height (upward) |
| `SCALE` | World units → canvas pixels (use 4.5-5.5 for city) |
| `CX, CY` | Canvas center of projection |

### 23.2 Which Faces Are Visible

Camera position: NE (large x, large y), looking SW (small x, small y).

| Face | World coords | Screen appearance | Normal |
|---|---|---|---|
| **Top** | z = max | Roof | (0,0,1) — always visible from above |
| **Right** | x = xb + w/2 | Right side of building | (1,0,0) — facing east toward camera |
| **Left** | y = yb + d/2 | Left/front side | (0,1,0) — facing north toward camera |

Faces at x = xb - w/2 (west) and y = yb - d/2 (south) are **hidden** — they face away from the NE camera.

### 23.3 Building Corners (8-point box)

For building centered at (xb, yb) with width w, depth d, height h:

```
Corner       World (x, y, z)         Screen appearance
FLB (front-left-base):  (xb-w/2, yb+d/2, 0)  → lowest on screen (closest)
FRB (front-right-base): (xb+w/2, yb+d/2, 0)  → lowest-right
BLB (back-left-base):   (xb-w/2, yb-d/2, 0)  → highest (farthest)
BRB (back-right-base):  (xb+w/2, yb-d/2, 0)  → highest-right
FLT (front-left-top):   (xb-w/2, yb+d/2, h)  → offset up from FLB
FRT (front-right-top):  (xb+w/2, yb+d/2, h)  → offset up from FRB
BLT (back-left-top):    (xb-w/2, yb-d/2, h)  → offset up from BLB
BRT (back-right-top):   (xb+w/2, yb-d/2, h)  → offset up from BRB
```

**Face vertex order (clockwise from top-left of screen projection):**

| Face | Vertices | Color |
|---|---|---|
| Right | `[BR, FR, FRT, BRT]` | Light (sunlit) |
| Left | `[FR, FL, FLT, FRT]` | Medium |
| Top | `[FLT, FRT, BRT, BLT]` | Lightest |

### 23.4 Painter's Algorithm (Depth Sort)

Draw buildings from back to front. Sort key:

```python
buildings.sort(key=lambda b: b[0] + b[1] - b[3]*0.3)
# b[0]=x, b[1]=y, b[3]=depth(d)
```

Smaller `x + y - d*0.3` = farther from NE camera = drawn first.

Draw order: **shadows → buildings with depth sort → windows → roof details → haze**

### 23.5 Shadow Calculation

```python
offset = bh * 0.12  # shadow stretch: 12% of building height
shadow = [
    project(bx - hw, by - hd, 0),
    project(bx + hw, by - hd, 0),
    project(bx + hw + offset, by + hd + offset*0.5, 0),
    project(bx - hw + offset, by - hd + offset*0.5, 0),
]
```

Shadows stretch SE (increasing x and y) proportional to height. Fill color: (0.30, 0.28, 0.25, α0.10).

### 23.6 Rendering Pipeline (Full Pass Order)

```
1. SKY:       gradient_linear top→bottom + distant haze line
2. CLOUDS:    white semi-transparent filled circles in sky
3. GROUND:    filled isometric diamond + grid lines
4. RIVER:     blue surface (polygon follow river course) + shimmer lines
5. CLOUD SHADOWS: dark patches on ground (world-coord circles → projected)
6. BUILDING SHADOWS: per-building offset, α0.10
7. BUILDINGS: 3 visible faces + highlights + edge outlines
8. WINDOWS:   full-width gold horizontal bands, varying brightness
9. ROOFTOP DETAILS: antennae, mechanical boxes
10. HAZE:     gradient overlay from horizon upward
11. PIL POST-PROCESSING: tilt-shift blur + vignette
```

### 23.7 Tilt-Shift Miniature Effect (PIL)

```python
from PIL import Image, ImageFilter, ImageDraw

# Generate blur at different strengths
blur_heavy = img.copy()
for _ in range(3):
    blur_heavy = blur_heavy.filter(ImageFilter.GaussianBlur(3))

# Gradient mask — sharp at y≈0.4×h, blurry at edges
mask = Image.new("L", img.size, 0)
draw = ImageDraw.Draw(mask)
for y in range(h):
    t = y / h
    alpha = int(255 * max(0, 1 - abs(t - 0.4) * 3.5))
    draw.line([(0, y), (w, y)], fill=alpha)

result = Image.composite(img, blur_heavy, mask)
```

### 23.8 Vignette (PIL + NumPy)

```python
import numpy as np
arr = np.array(img, dtype=np.float32)
for y in range(h):
    for x in range(w):
        dx, dy = (x-cx)/r, (y-cy)/r
        vig = max(0.75, min(1.0, 1 - (dx*dx + dy*dy) * 0.3))
        arr[y, x, :] *= vig
```

## 24. Rendering Realistic Black Objects

> Key insight: "Black" in realistic rendering is never pure black. It's a narrow band of very low values (0.05-0.25 in 0-1 range) with subtle hue shifts toward blue, purple, or brown depending on the material and lighting.

### 24.1 The Black Value Spectrum

| Value | Appearance | Use |
|---|---|---|
| 0.02-0.05 | Near-black (core shadow) | Deepest crevices, occluded areas |
| 0.05-0.10 | Very dark (form shadow) | Shadow side of form |
| 0.10-0.15 | Dark gray (mid-shadow) | Transition zone, cast shadows on self |
| 0.15-0.20 | Medium-dark (half-tone) | Ambient-lit areas of black surface |
| 0.20-0.30 | Light-dark (reflected light) | Bounce light from environment |
| 0.30-0.50 | Highlight (rim/top) | Edge where light wraps around |
| 0.60-1.00 | Specular glint | Direct light reflection (sharp, small) |

### 24.2 Layering Black (The Palette)

For a blued-steel black pistol:

| Layer | RGB (0-1) | What it simulates |
|---|---|---|
| Base black | (0.08, 0.08, 0.10) | The raw material color |
| Core shadow | (0.03, 0.03, 0.05) | Crevices, under-barrel, grip texture depth |
| Midtone | (0.12, 0.12, 0.15) | Main body surfaces |
| Ambient light | (0.18, 0.18, 0.22) | Areas facing sky/environment |
| Rim light | (0.30, 0.32, 0.38) | Sharp edge where slide meets frame |
| Specular | (0.50, 0.55, 0.65) + to (0.90, 0.92, 0.95) | Bright glints on bevels, slide serrations |
| Color reflection | (0.15, 0.18, 0.25) | Sky reflected in blued steel (blue shift) |

### 24.3 Why Black Needs Blue

Pure black (0,0,0) feels dead. Real blued steel / anodized black has subtle blue/purple:

| Material | Hue shift | Reason |
|---|---|---|
| Blued steel | +B, +slight R | Iron oxide + oil treatment |
| Anodized aluminum | +B, +slight G | Oxide layer interference |
| Painted matte black | Neutral | No shift, but needs value layers |
| Rubber/plastic | +slight R or Y | Material absorption |
| Oiled steel | +B, +warm glints | Oil film on dark metal |

### 24.4 Geometry → Reflection Mapping

The geometry of an object determines WHERE reflections occur:

| Feature | Reflection type | What it reflects |
|---|---|---|
| Flat surface (slide side) | Broad, dim | Sky/environment gradient |
| Beveled edge (slide top) | Sharp line | Sky horizon (sharp transition) |
| Cylinder (barrel) | Vertical gradient band | Lamp/light strip reflection |
| Serrations (rear slide) | Repeating highlights | Each serration catches a glint |
| Curved surface (trigger guard) | Sweeping gradient | Wraparound sky reflection |
| Hole/cavity (trigger well) | No reflection | Pure shadow (blackest black) |
| Grip texture | Diffuse scattering | Lower overall, no sharp glints |

### 24.5 Rendering Black in CGContext

**Technique:** Draw the object as a filled path in the base black, then layer progressively lighter fills on top for each reflection zone.

```python
# Step 1: Base silhouette (darkest)
c.gs(); c.fc((0.08, 0.08, 0.10))
c.fill_path(pistol_outline); c.gr()

# Step 2: Ambient midtone (wider than highlights)
c.gs(); c.fc((0.15, 0.15, 0.20))
c.fill_path(top_face_of_slide); c.gr()

# Step 3: Rim/edge highlight (thin)
c.gs(); c.lw(1.5); c.sc((0.35, 0.38, 0.45, 0.6))
c.polyline(upper_edge_of_slide); c.gr()

# Step 4: Specular glint (small, bright)
c.gs(); c.fc((0.7, 0.75, 0.85, 0.4))
c.fill_path(bevel_highlight_polygon); c.gr()
```

### 24.6 Sub-Pixel Rendering

Canvas renders at 2× (1320×1400). After LANCZOS downscale to 660×700:

```
1 canvas-unit rect → 2×2 Quartz pixels → ~1×1 output pixel (blended)
0.5 canvas-unit rect → 1×1 Quartz pixel → ~0.5 output pixel (sub-pixel)
```

**Minimum visible mark:** A `c.rect(x-0.25, y-0.25, x+0.25, y+0.25, f=color)` at 2× renders a single Quartz pixel. After downscale, this produces a ~0.5px blended mark — visible but soft.

For sharp specular glints: use `c.circle(x, y, 0.5, f=(1,1,1,0.8))` → renders as a 1px Quartz circle → sharp (~1px) in output.

## 25. Drawing Script Archive

### 25.1 WTC Isometric Map (`/tmp/wtc_isometric.py`)

| Property | Value |
|---|---|
| Canvas | 660×700 |
| Projection | Isometric, SC=5.2 |
| Center | CX=340, CY=380 |
| Buildings | ~70 (hand-placed + 30 random filler) |
| Twin Towers | 7×7×55 units, blue glass, 14° rotated, spire on 1WTC |
| WTC 7 | 8×5×38 units, north of Vesey |
| Sky | Gradient top-to-bottom + clouds (8, white α0.2-0.45) |
| Ground | Diamond grid 0-90 at 5-unit intervals |
| River | Hudson River polygon + shimmer lines |
| Layers | Shadows → Buildings → Window bands → Antennae → Haze |
| Post-processing | Tilt-shift blur + vignette (both PIL) |
| Output | `/tmp/wtc_isometric.png` → pasted into Freeform |

### 25.2 Chameleon Drawing (`/tmp/chameleon.py`)

| Property | Value |
|---|---|
| Canvas | 660×700 |
| Style | Algorithmic construction (no tracing) |
| Body | Catmull-Rom fill, green, 378×284px bbox |
| Eye | Yellow iris + dark pupil + highlight |
| Tail | Catmull-Rom spiral |
| Features | Casque (crest), gripping feet, diagonal branch+leaf |
| Texture | ~50 randomized spots/scales |
| Background | Sage green (0.56, 0.65, 0.48) |

### 25.3 Side-by-Side Comparison (`/tmp/dog_side_by_side_v2.py`)

| Property | Value |
|---|---|
| Canvas | 660×700 |
| Left half | Original pixel blit (direct buffer write, MSE~1.08) |
| Right half | Vector sketch (12 k-means color clusters → 476 filled regions → per-region average colors) |
| Vector quality | MSE ~16000 (poor vs original) |

## 26. Working Principles (Quartz Era)

1. **CTM flip first, ask questions later.** Every Canvas applies `Translate(0,h) + Scale(1,-1)` in `__init__`. Never draw without it.

2. **Batch inside gs/gr.** `c.sc()` and `c.lw()` modify the current gstate. Wrap multiple `c.line()` calls in one `c.gs()/c.gr()` save/restore to avoid per-line state overhead.

3. **Sub-pixel for glints, 1+ px for fills.** Specular glints: 0.25-0.5 canvas-unit radius. Shape fills and large features: 1+ canvas-units.

4. **Layering over rewriting.** Add visual complexity in passes (shadows → solids → highlights → windows → details → haze). Each pass adds a dimension of realism.

5. **3D world → 2D projection → canvas coordinates.** Define everything in world space (x, y, z), project to canvas with `proj()`. Never hardcode screen positions for isometric scenes.

6. **Gradients are cheap, use them.** `gradient_linear` creates a CGGradient (~10µs). Use for sky, haze, and any face that should look reflective.

7. **Black is layering, not color.** Pure black (0,0,0) reads as flat silhouette. Real black objects need 4-8 value layers within 0.02-0.50 range, with material-appropriate hue shifts (blue for steel, warm for rubber, etc.).

---

## 27. Unified Spatial Framework (Synthesis: shorts × drawing)

> **Everything in this section overrides or supersedes earlier ad-hoc approaches. These are not "nice to have" — they are the operating system for every spatial drawing task. Apply fractal: every element at every scale follows the same rules.**

### 27.1 Coordinate System Standard (`~/shorts/microcosmos/spatial/rules.yaml`)

Every subject gets its own coordinate system:

```
Origin:   (0, 0, 0)  = subject's anatomical center (trigger center for pistol,
                       thorax center for insect, hip center for dog)
+X:       toward viewer's right (also the "toward viewer" axis in side view)
+Y:       up (toward sights/toward dorsal)
+Z:       forward (toward muzzle/toward anterior)
Units:    millimeters
```

**This is the ONLY coordinate system.** Do not invent ad-hoc ones. Every drawing starts by defining the origin and axes.

### 27.2 Anatomical Landmarks (`~/shorts/microcosmos/characters/honeybee.yaml`)

Before any drawing, define named landmarks as `[x, y, z]` tuples. These are the vocabulary of the subject.

```
Example — 1911 pistol landmarks:
  trigger_center:     [0,   0,   0]     # origin
  slide_front_top:    [0,  15, 110]     # front of slide, top edge
  barrel_muzzle:      [0,   8, 130]     # barrel end
  hammer_pivot:       [0,  15, -40]     # hammer axle
  grip_bottom:        [0, -50, -15]     # base of grip
  trigger:            [0,  -8,   5]     # trigger face
  mag_well:           [0, -45,   5]     # magazine insertion
  ejection_port:      [0,  12,  60]     # port center
```

**Rules:**
- Every landmark is relative to origin `(0,0,0)`
- Named landmarks are the ONLY way to reference positions — no "250 pixels from the left"
- Landmarks enable projection to any viewpoint (right-side, isometric, ¾-view) from the same data

### 27.3 Anchoring Triangulation (`~/shorts/lessons.md`)

**Every element's position is determined by exactly two fixed anchors and one offset.** Nothing floats.

```
# NOT:  trigger_at = (330, 490)                    # ad-hoc screen coord
# BUT:  trigger_center = anchor_lh                  # landmark
#       trigger_face = anchor_lh + [0, -4, 5]       # offset from landmark
```

**Why it matters:** Anchored positions are resilient to scale/resolution changes. They can be projected to any viewpoint. They compose — moving the origin moves everything.

**Failure mode caught:** In pistol V2, trigger and grip positions were hardcoded screen pixels. If the canvas size changed, the entire drawing broke. V3 fixed this by defining all positions relative to landmarks.

### 27.4 Surface Normal → Value Mapping (Connects §23 + §24)

This is the most important synthesis: **lighting is not manual — it falls out of geometry.**

```
value = BASE_V + RANGE_V * max(0, dot(surface_normal, light_direction))
```

Where:
- `BASE_V` = ambient light value (0.25 for black objects)
- `RANGE_V` = light contribution range (0.65 — slides to 0.90 for highlights)
- `surface_normal` = unit vector perpendicular to the surface, pointing outward
- `light_direction` = unit vector from surface to light source (normalized)

**How to compute a surface normal from landmarks:**

For a face defined by 3+ landmarks, take the cross product of two edges:

```python
def surface_normal(p0, p1, p2):
    """Right-hand rule: (p1-p0) × (p2-p0), normalized."""
    e1 = [p1[i] - p0[i] for i in range(3)]
    e2 = [p2[i] - p0[i] for i in range(3)]
    n = [e1[1]*e2[2] - e1[2]*e2[1],   # cross product
         e1[2]*e2[0] - e1[0]*e2[2],
         e1[0]*e2[1] - e1[1]*e2[0]]
    mag = math.sqrt(sum(v*v for v in n))
    return [v/mag for v in n] if mag else [1,0,0]
```

**Value mapping for black objects (from §24.1):**

| dot(n, L) | Final value | Appearance |
|---|---|---|
| 0.0 (face away) | 0.02-0.08 | Core shadow |
| 0.1-0.2 | 0.08-0.15 | Form shadow |
| 0.3-0.4 | 0.15-0.22 | Midtone |
| 0.5-0.6 | 0.25-0.40 | Lit |
| 0.7-0.8 | 0.45-0.65 | Bright |
| 0.9+ | 0.70-1.00 | Glint |

**Cylindrical parts** (barrel, tubes): approximate as an N-sided prism. Each band has its own normal.

```python
# 6 bands for a cylinder at angle θ from center:
bands = 6
for i in range(bands):
    angle = -PI/2 + i * PI/(bands-1)  # -90° to +90°
    normal = [cos(angle), sin(angle), 0]
    value = base + range_v * max(0, dot(normal, light_dir))
    # draw band at this value
```

**Rim lights** occur where the surface normal is perpendicular to the camera direction:

```
rim = 1.0 - abs(dot(normal, cam_dir))
if rim > RIM_THRESHOLD:  # ≈ 0.85
    draw rim highlight at value = 0.50-0.70
```

### 27.5 Camera Metal (Fixed Optical Properties)

The camera is a physical object with mass, velocity limits, and fixed properties:

| Property | Value | Meaning |
|---|---|---|
| Position | Fixed for scene | Defines visible faces |
| Direction | Fixed for scene | Defines what "forward" is |
| Focal length | Fixed for scene | No zoom breathing |
| Max velocity | 10 mm/s | No teleportation |
| Acceleration | 50 mm/s² | Smooth moves only |

**Connection to isometric (§23):** The isometric camera at NE looking SW was correct — it follows camera metal. But it was implicit. Make it explicit: define `CAM_POS`, `CAM_DIR`, `LIGHT_DIR` as constants at the top of every script.

```
CAM_POS = [300, 300, 200]     # NE + above
CAM_DIR = normalize([-1, -1, -0.5])  # looking SW + slightly down
LIGHT_DIR = normalize([1, -1, 2])   # from above-right-forward
```

**Failure mode caught (pistol V3):** I defined surfaces with normals in the +X hemisphere but computed shading correctly. What I missed was defining cam_dir = [1, 0, 0] (viewed from the right). This is correct — cam_pos needs to match what you're rendering. For a right-side view of a pistol, the camera is at +X infinity.

### 27.6 Mechanical Transitions (Physical Consequence)

Borrowed from the Gas Station scene structure in `~/shorts/lessons.md`: every mechanical action produces a physical consequence visible in the frame.

**Application to drawings:**

| Mechanism | What must be visible | Purpose |
|---|---|---|
| Trigger + guard | Gap between trigger and guard. Trigger face angled. | Shows trigger can move. |
| Hammer + frame | Hammer pivot, clearance behind hammer. | Shows hammer can rotate. |
| Slide + frame | Ejection port shows barrel/hood inside. | Shows slide is separate. |
| Recoil spring | Spring rod visible beneath barrel. | Explains how slide cycles. |
| Magazine | Base pad below grip. Follower visible in well. | Shows detachable magazine. |
| Safety | Tab visible at slide-frame interface. | Shows manual safety exists. |

**General principle:** For every pair of adjacent parts, there must be at least one visible gap, seam, or differentiation line. Without it, they read as a single blob.

### 27.7 Property Inheritance (CreativeInertia from MODELTUNE/DNA)

From the Absurdity Protocol's CreativeInertia concept: objects have "mass" that resists property changes. Properties persist unless explicitly overridden.

**Application:**

| Property | Inherited by default | Must change for |
|---|---|---|
| Material (blued steel) | All metal parts | Grip (rubber), sights (white dot) |
| Value range (black) | Entire figure | Glints, bright edges |
| Light direction | All surfaces | No exceptions |
| Line width (1px) | Fine detail | Sub-pixel glints |
| Hue shift (blue) | Steel surfaces | Grip (warm brown), muzzle (carbon) |

```python
# Correct — properties cascade:
material = "blued_steel"           # All metal parts inherit
value_slider = Shader(light_dir)   # All surfaces inherit light
grip = material "rubber"           # Only grip overrides
grip.value_range = [0.02, 0.12]    # Grip is darker, no glints
```

### 27.8 Unified Rendering Pipeline (All Lessons Combined)

```
PHASE 1: COORDINATE SETUP
  1. Define origin at subject's anatomical center
  2. Define all landmarks as [x, y, z] relative to origin
  3. Define CAM_POS, CAM_DIR, LIGHT_DIR, SCALE
  4. Define projection function: 3D [x,y,z] → 2D canvas (cx, cy)

PHASE 2: GEOMETRY
  5. For each visible part:
     a. Select relevant landmarks
     b. Define surface vertices (winding order: outward normal)
     c. Compute surface normal from cross product
  6. Identify hidden/silhouette surfaces (normal dot cam_dir < 0)

PHASE 3: SHADING
  7. For each visible surface:
     a. value = BASE + RANGE * max(0, dot(normal, LIGHT_DIR))
     b. Apply material tint (blued, rubber, etc.)
     c. If rim condition: add rim highlight (value + 0.25)
  8. Core shadows: draw darkest (0.02-0.08) at joints, crevices

PHASE 4: DETAIL PASS
  9. Mechanical gaps: draw separation lines (0.01-0.03) at all part boundaries
  10. Specular glints (WHITE, 0.5-1px) at normal ≈ reflect_dir
  11. Texture: grip crosshatch, slide serrations, trigger checkering

PHASE 5: SHADOWS
  12. Cast shadow on ground plane (proportional to height, α0.10-0.15)
  13. Self-shadow where parts overlap (ejection port interior, trigger well)

PHASE 6: POST-PROCESSING (if PIL available)
  14. Tilt-shift blur gradient
  15. Vignette
```

### 27.9 Verification Gates (Drawing Quality)

| Gate | What to check | Fail condition |
|---|---|---|
| Coordinate check | Every position references a named landmark. No magic numbers. | Any screen-coord literal |
| Normal check | Every surface has a computed normal. Compare dot values. | Manual value assignments |
| Mechanical check | Every pair of adjacent parts has a visible seam. | Parts blend together |
| Range check | Values span full 0.02-1.00 range. Read on Freeform canvas. | All values in 0.1-0.3 range |
| Palette check | Black has blue/purple shift in midtones. | Pure gray or pure black |

### 27.10 Key Decision: Legacy Endings

| Old approach | Unified approach | Why |
|---|---|---|
| Ad-hoc screen coords for pistol parts | All positions from named landmarks | Resilient to scale/resolution changes |
| Manual value selection (0.08 base, 0.35 highlight) | `dot(normal, light_dir)` computes value | Consistent lighting, fewer decisions |
| One big polygon for barrel | 6-sided cylinder bands with distinct normals | Reads as round |
| Single value per face | Gradient across face when face twists away from light | Shows curvature |
| Softcode camera implicitly | `CAM_POS`, `CAM_DIR`, `LIGHT_DIR` as constants | Enables viewpoint switching |
| Pistol drawn as isolated object | Pistol in 3D coordinate space with ground plane shadow | Feels like a real object in space |

### 27.11 Quick-Start Template

```python
# === PHASE 1: COORDINATE SETUP ===
import math
import numpy as np
from freeform_renderer import Canvas

# Light & camera (RIGHT SIDE VIEW)
CAM_POS = [1000, 0, 0]          # from the right
CAM_DIR = [-1, 0, 0]            # looking left
LIGHT_DIR = [0.3, -0.5, 0.8]    # above-right-forward
LIGHT_DIR_N = [v/math.sqrt(sum(d*d for d in LIGHT_DIR)) for v in LIGHT_DIR]

# Projection: orthographic from the right (y-up, z-forward)
def proj(x, y, z):
    """3D [x,y,z] → 2D (cx, cy) for right-side view."""
    return CX + z * SCALE, CY - y * SCALE

# Anatomical landmarks
L = {
    "origin":       [0,   0,   0],
    "slide_front":  [0,  15, 110],
    # ... all landmarks
}

# === PHASE 2+3: SURFACES with computed normals ===
for surf in SURFACES:
    pts_3d = [L[name] for name in surf.landmarks]
    normal = surface_normal(*pts_3d[:3])
    value = 0.25 + 0.65 * max(0, sum(n*1 for n,1 in zip(normal, LIGHT_DIR_N)))
    pts_2d = [proj(*p) for p in pts_3d]
    c.gs(); c.fc((value*v for v in palette))
    c.fill_path(pts_2d); c.gr()
```

### 27.12 Reference: Source Files in `~/shorts/`

| File | What it provides |
|---|---|
| `microcosmos/spatial/rules.yaml` | Coordinate system, icosahedral grid camera positions, distance bands, camera velocity/acceleration limits |
| `microcosmos/CONSTITUTION.yaml` | 12-Book governance: Director, Camera, Lighting, Editor, Producer, Spatial Staging, Character, Writer, Production Design, Sound, Prompt Compiler |
| `microcosmos/characters/honeybee.yaml` | Model for anatomical landmarks — precise [x,y,z] for named body parts |
| `lessons.md` | Anchoring triangulation (two anchors + one target), camera metal, mechanical transitions with physical consequences |
| `MODELTUNE/SKILL.md` | Absurdity Protocol — CharacterDNA, CreativeInertia, WorldSchema, Specificity Engine. Every output must name: file, interface, call sites |
| `characters/*.yaml` | 5 character specs with absolute 3D dimensions (mm), proportion ratios, screen presence percentages |

---

*The coordinate grounds every point. The normal computes every value. The gap shows every part. The anchor holds every position.**
