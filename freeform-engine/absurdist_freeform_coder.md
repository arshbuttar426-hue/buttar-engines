Copyright © 2026 Arsh Buttar. All rights reserved. Confidential and proprietary.
Unauthorized copying, distribution, or use of this work is prohibited.

# Absurdist Freeform Coder — Project Protocol

> *Every insight terminates in code. Every stroke is a planned path. No pixel without a purpose.*

---

## Project Map (The Chart)

```
┌──────────────────────────────────────────────────────────────────┐
│  FREEFORM DRAWING PROJECT — Architecture                        │
│                                                                  │
│  L7  Verification     count_ink, verify_phase, preflight_check   │
│  L6  Vehicles         ground, frame, horizon                    │
│  L5  Composition      house, sun, cloud, tree, eye, door        │
│  L4  Styles           bold5, bold3, paraline                    │
│  L3  Draw primitives  polyline, zigzag_fill, grid_lines         │
│  L2  Geometry         catmull, polygon, circle, line, arc       │
│  L1  Input atoms      click, keystroke, activate_pen, stroke    │
│  L0  Substrate        activate_freeform, new_board              │
│                                                                  │
│  ┌─────────────────┐     ┌─────────────────┐     ┌───────────┐  │
│  │ PYTHON ENGINE   │────▶│ DRAWING SCRIPTS │────▶│ SWIFT APP │  │
│  │ freeform_engine │     │ draw_*.py       │     │ Drawing   │  │
│  │ L0-L7 unified   │     │ 15+ compositions│     │ Server    │  │
│  └─────────────────┘     └─────────────────┘     └───────────┘  │
└──────────────────────────────────────────────────────────────────┘
```

## 4-Phase Workflow (Applied to Freeform)

### Phase 1: PREDETERMINE — Planning a Drawing

Before any `stroke()` call, apply the Force-Down Protocol:

| Step | Question | Freeform Example |
|------|----------|-----------------|
| 1. Reveal Principle | What's the visual principle? | "Depth through overlapping mountain silhouettes" |
| 2. Envision Artifact | What concrete drawing? | `mountain_silhouette()` |
| 3. Define Interface | What params? | `pts, smooth_n=45, bold=True` |
| 4. Pinpoint File | Where in codebase? | `freeform_engine.py:530` |
| 5. Identify Call Site | Where invoked? | `draw_landscape.py:12` |
| 6. Plan Tests | How verify? | `verify_phase("mountains", 50, 200, 550, 480)` |

**Specificity Engine Gate** — reject if:
- ❌ No exact coordinates planned (each element must have position + size)
- ❌ No verification region defined (ink count bbox)
- ❌ No calibration check (pen coordinates must be current)

### Phase 2: NORMALIZE — Domain Selection

Map the drawing intent to the right composition:

| What you want | Domain pattern | Use this |
|---------------|----------------|----------|
| Smooth organic curves | Biology → Mycelial | `catmull(pts, n=40)` |
| Area fill, not per-line | Physics → Entropy | `zigzag_fill()` over `hatch_lines()` |
| Repetitive elements | Chemistry → Catalytic | `brick_wall()` template |
| Thick visible edges | Biomechanics → Joints | `bold5()` with parallel offsets |
| Multiple interpretations | Philosophy → Death of Director | Draw same scene at 2 zoom levels |
| Objects off-screen | Psychology → Object Permanence | Add `[PERSISTS]` notes to `freeform_drawing.md` |
| Drift detection | Medicine → Homeostat | `preflight_check()` before main draw |
| Model selection | Economics → VCG | Python for composition, Swift for native rendering |
| Identity verification | Cryptography → Merkle | `screenshot("/tmp/verify.png")` → `count_ink()` |

### Phase 3: OPTIMIZE — Efficient Execution

**Token budget** (time, not tokens — but same principle):
```
Drawing time budget: 120 seconds
  Setup + calibration:    10s  (8%)
  Composition layer:      15s  (13%) — backgrounds, ground, sky
  Primary elements:       40s  (33%) — main subject (house/tree/character)
  Detail elements:        30s  (25%) — windows, leaves, texture
  Verification:           10s  (8%)
  Buffer:                 15s  (13%)
```

**Parallelization rules:**
- `bold5()` is 5 serial strokes — group bold calls to minimize pen reactivations
- `zigzag_fill()` replaces 10+ `hatch_lines()` calls — always prefer zigzag
- Batch independent strokes (e.g., all windows at once) to share `activate_pen()` calls

**Granularity:**
- Each composition call should span 50-200 screen pixels
- Catmull-Rom n=40 for organic, n=20 for angular
- Bold offsets: ±4px for visibility, ±2px for subtle weight

### Phase 4: VERIFY — Industrial Gates for Drawing

**Gate 1 — Scope Check:**
- Each composition function ≤ 50 lines of Python
- `freeform_engine.py` modules organized by L level (L0-L7)
- Swift DrawingServer files ≤ 130 lines per file

**Gate 2 — Ink Count Check:**
```python
verify_phase("house_body", 180, 380, 480, 470, threshold=100)
# FAIL if ink < 50: stroke was too thin or didn't register
# WARN if ink > 1000: area may be over-filled
```

**Gate 3 — Completeness:**
Every drawing must have:
- [ ] Preflight check (`preflight_check()`)
- [ ] Setup (`activate_freeform()` + `new_board()`)
- [ ] At least 1 bold element (visual anchor)
- [ ] At least 1 composition call (L5)
- [ ] Screenshot saved
- [ ] Ink report generated

**Gate 4 — Calibration Validation:**
```python
pen_calibration.txt must be readable
SHAPE coordinates must be within Freeform window bounds
PEN coordinates must be within Freeform window bounds
If coordinates haven't been updated in >30 days → request recalibration
```

---

## 10 Domain Patterns — Freeform-Specific Mappings

### Domain 1: Biology — Mycelial Distribution (Parallel Drawing)

**Principle:** Split complex drawings into independent specialist modules, not a single monolithic script.

**Freeform Mapping:**
- Single scripts → decomposed into composition functions
- `draw_house.py` calls `roof()`, `door()`, `window_pane()` — each independently testable
- If a `draw_*.py` script exceeds 80 lines, extract compositions into `freeform_engine.py`

**Concrete:**
```python
# BAD: monolithic
def draw_entire_house():
    stroke([(180,470),(480,470)])  # ground
    stroke([(180,470),(180,380)])  # wall left
    ...

# GOOD: composed
setup()
ground(470, 100, 560)
rect_outline(180, 470, 480, 380, bold=True)
roof(330, 290, 180, 365, 480, bold=True)
door(305, 470, 355, 405)
# Each function independently testable via verify_phase()
```

**File:** `freeform_engine.py:L5`
**Test:** `verify_phase("door", 300, 400, 360, 475)`

### Domain 2: Physics — Maxwell's Demon (Dimension Sorted)

**Principle:** Sort drawing elements into labeled layers, not a flat sequence. Each layer has its own schema.

**Freeform Mapping:**
Drawing layers (applied in order):
```
[BACKGROUND]  →  ground, sky, horizon, frame
[STRUCTURE]   →  walls, roof, chimney, fence
[DETAIL]      →  windows, doors, bricks, tiles
[NATURE]      →  trees, clouds, sun, mountains
[FOREGROUND]  →  characters, objects, highlights
[INK]         →  verification marks, ink regions
```

**Concrete:** Every drawing script follows layer order. Each layer sets its own `bold` and `slp` settings.

**File:** All `draw_*.py` scripts
**Test:** Scripts that skip layer order → WARN

### Domain 3: Chemistry — Catalytic Templates (Frozen Compositions)

**Principle:** Compositions are static templates that never mutate. Data flows through them.

**Freeform Mapping:**
- `roof()`, `door()`, `sun()`, `cloud()` — these are catalytic templates
- Parameters change, template stays the same
- Never edit a composition's internal structure — extend by adding new compositions

**Concrete:**
```python
# Catalytic — NEVER change the internal geometry
def door(x1, y1, x2, y2, arch_top=8, has_knob=True, bold=False):
    trait = y2 - y1
    arch_top = arch_top or trait * 0.08
    pts = [...]  # frozen template
    polyline(catmull(pts, 25), bold=bold)
    if has_knob:
        circle_outline(...)  # frozen sub-template

# Extend by adding NEW compositions, not editing existing ones
def door_double(x1, y1, x2, y2, **kwargs):  # NEW, not modified
    door(x1, y1, x2, y2, **kwargs)
    door((x1+x2)/2, ...)
```

**File:** `freeform_engine.py:L5` composition functions
**Test:** Each composition has a corresponding Swift equivalent in `Compositions.swift`

### Domain 4: Biomechanics — Joints Over Levers (Composition Over Inheritance)

**Principle:** Build drawings from small, composable joints. No deep hierarchies.

**Freeform Mapping:**
- `house = rect_outline + roof + door + window_pane + chimney` — composition, not inheritance
- `castle = rect_outline + crenelation + door + brick_wall + arrow_slit` — same joints, different assembly
- Maximum 2 levels deep (composition calls primitive, primitive calls geometry)

**Concrete:**
```python
# Composition (Joint) — not inheritance (Lever)
# Joint: rect_outline + roof + door + window_pane
# Joint: rect_outline + crenelation + arched_window + drawbridge

def castle(cx, cy, scale=1.0):
    # Assembled from the SAME joints as house, just different params
    rect_outline(cx-100, cy-100, cx+100, cy+100, bold=True)
    crenelation(cx-100, cx+100, cy-100, 15, 14)
    door(cx-20, cy+100, cx+20, cy+40, arch_top=15)
    # No castle-specific inheritance needed
```

**File:** `freeform_engine.py:L5` — all compositions use the same joint vocabulary
**Test:** Any new composition should use ≥2 existing composition functions

### Domain 5: Philosophy — Death of the Director (Multiple Interpretations)

**Principle:** No single "correct" drawing. Generate multiple visual interpretations.

**Freeform Mapping:**
- Same scene at different zoom levels: `zoom_in(3)` → same coordinates, different scale
- Same composition with different parameters: `bold=False` vs `bold=True`, `n=20` vs `n=60`
- Multiple ink reports to compare which interpretation had better coverage

**Concrete:**
```python
# Multiple interpretations of the same scene
def eye_multiscale(cx, cy):
    for level in [1, 2, 3]:
        eye(cx, cy, s=1.0)
        verify_phase(f"eye_level_{level}", cx-50, cy-50, cx+50, cy+50)
        zoom_in(4)
```

**File:** `draw_infinite_eye.py`, `draw_infinite_tree.py`
**Test:** Each interpretation produces a different ink count

### Domain 6: Psychology — Object Permanence (World Schema)

**Principle:** Objects continue to exist off-screen. Don't forget what was drawn.

**Freeform Mapping:**
- The canvas has "object permanence" — strokes don't disappear when scrolled away
- Swift DrawingServer `DrawingDocument.strokes` array — all strokes persist
- `count_ink()` can detect strokes even if visually occluded

**Concrete:**
```python
# Object permanence in the SwiftUI app
document.strokes  # ALL strokes ever drawn, not just visible ones
# count_ink works on ALL strokes, not just what's on screen
```

**File:** `DrawingServer/Sources/DrawingServer/Stroke.swift:DrawingDocument`
**Test:** Draw, scroll away, scroll back — strokes remain

### Domain 7: Medicine — Homeostatic Regulation (Ink Density Correction)

**Principle:** Monitor critical values (ink density), detect deviation from set points, apply correction.

**Freeform Mapping:**
- Set point: expected ink count per region (from `freeform_drawing.md` verified recipes)
- Measure: `count_ink(x1, y1, x2, y2)` after each phase
- Correct: If ink < threshold → redraw stroke with `bold=True` or increase `n` in `catmull`

**Concrete:**
```python
INK_SET_POINTS = {
    "door": {"expected": 300, "tolerance": 100},
    "roof": {"expected": 500, "tolerance": 150},
    "window": {"expected": 200, "tolerance": 80},
}

def homeostatic_draw(name, draw_fn, bbox, **kwargs):
    draw_fn(**kwargs)
    ink = count_ink(*bbox)
    setpoint = INK_SET_POINTS.get(name)
    if setpoint and abs(ink - setpoint["expected"]) > setpoint["tolerance"]:
        print(f"[CORRECTION] {name}: {ink}px vs {setpoint['expected']}px expected")
        # Re-draw with bold=True
        draw_fn(**{**kwargs, "bold": True})
```

**File:** `freeform_engine.py:L7` (proposed addition)
**Test:** `homeostatic_draw("door", door, (300,400,360,475))` produces consistent ink counts

### Domain 8: Economics — VCG Auction (Tool Selection)

**Principle:** When multiple tools can achieve the same drawing, select the best one.

**Freeform Mapping:**
- Python engine vs Swift DrawingServer: which to use for what?
- CGEvent click simulation vs TCP JSON commands: which is more reliable?

**Auction table:**
| Task | Python (CGEvent) | Swift (TCP) | Winner |
|------|-----------------|-------------|--------|
| Single quick sketch | ✅ Fast setup, ⚠️ fragile coords | ❌ Requires app build | Python |
| Complex multi-layer drawing | ⚠️ Sequential per-stroke | ✅ Parallel batch via TCP | Swift |
| Pixel-level verification | ✅ Direct pixel access | ⚠️ Point-density only | Python |
| Interactive zoom/pan | ❌ Not possible | ✅ Native gestures | Swift |
| Variable stroke width | ❌ Only via bold offsets | ✅ True width parameter | Swift |

**Concrete:**
```python
def bid_task(task_type, complexity):
    """VCG-style bidding between Python and Swift render paths."""
    bids = {
        "quick_sketch": {"python": 0.2, "swift": 0.8},
        "detailed_scene": {"python": 0.6, "swift": 0.3},
        "verification": {"python": 0.1, "swift": 0.7},
    }
    return min(bids.get(task_type, {}), key=bids.get(task_type, {}).get)
```

**File:** Implementation guidance in `freeform_drawing.md`
**Test:** Complex drawings use Swift; quick sketches use Python

### Domain 9: Cryptography — Integrity Chains (Stroke Verification)

**Principle:** Every drawing produces a verifiable hash chain of its strokes. Detect drift.

**Freeform Mapping:**
- Screenshot → hash → store
- Next drawing's `preflight_check()` compares against stored hash
- If pixels changed unexpectedly → calibration drift detected → recalibrate

**Concrete:**
```python
import hashlib

DRAWING_HASHES = {}

def verify_drawing_integrity(name, bbox):
    """Hash the ink region and compare against known-good drawing."""
    _, img_data = capture_region(bbox)
    current_hash = hashlib.sha256(img_data).hexdigest()[:16]
    
    if name in DRAWING_HASHES:
        if current_hash != DRAWING_HASHES[name]:
            print(f"[INTEGRITY BREACH] {name}: hash mismatch")
            print(f"  Expected: {DRAWING_HASHES[name]}")
            print(f"  Got:      {current_hash}")
            return False
    else:
        DRAWING_HASHES[name] = current_hash
    return True
```

**File:** `freeform_engine.py:L7` (proposed addition)
**Test:** Same drawing produces same hash; different drawing produces different hash

### Domain -1: Parsimony — Occam's Razor (Freeform-Specific)

**Principle:** The simplest stroke that achieves the visual effect is superior to any complex alternative.

**Freeform Mapping:**
| Over-engineered | Simple alternative | Why simpler wins |
|----------------|-------------------|-----------------|
| Custom spline algorithm for a straight line | `line(x1, y1, x2, y2)` | 1 call vs 10+ lines |
| `hatch_lines(step=1)` for fill | `zigzag_fill(step=3)` | 1 stroke vs 30+ strokes |
| 10 separate `activate_pen()` + `stroke()` calls | `bold5()` wrapping the same pts | 5 strokes via 1 call |
| Custom composition that duplicates logic | Use `roof()` + `door()` + `window_pane()` from library | 3 calls vs 30+ lines |
| DrawingServer for a 2-line sketch | Python `stroke([(x1,y1), (x2,y2)])` | No build step needed |

**Vote NAY on:**
- Adding a new composition that duplicates existing geometry
- Creating a drawing script longer than 80 lines without extracting compositions
- Using the Swift DrawingServer for single-stroke sketches
- Adding a new L5 composition when 3 existing ones can combine to the same effect

---

## Implementation: Files to Create/Modify

| File | Action | Lines | Domain |
|------|--------|-------|--------|
| `freeform_engine.py` | Add `homeostatic_draw()` to L7 | ~30 | Domain 7 |
| `freeform_engine.py` | Add `verify_drawing_integrity()` to L7 | ~25 | Domain 9 |
| `freeform_drawing.md` | Add "Absurdist Coder" section referencing this doc | ~20 | All |
| `DrawingServer/Sources/...` | Already implements Domain 6 (object permanence) | — | D6 |
| `draw_*.py` | Each script should add `verify_phase()` calls | ~5 each | D7 |
| `pen_calibration.txt` | Add last-verified timestamp field | 1 | D9 |

---

## Unified PR Checklist (Freeform Edition)

### Phase 1 Check
- [ ] Drawing intent parsed into composition sequence
- [ ] Coordinates planned for each element
- [ ] Verification bbox defined for each element
- [ ] Failure modes identified (pen not responding, calibration drift)

### Phase 2 Check
- [ ] Domain pattern selected
- [ ] Composition library checked first (L5) before reinventing
- [ ] Bold used strategically (not everywhere)
- [ ] Zigzag preferred over hatch for fills

### Phase 3 Check
- [ ] Time budget computed and not exceeded
- [ ] Bold calls batched together (minimize pen activations)
- [ ] Catmull-Rom n value appropriate for the feature

### Phase 4 Check
- [ ] `preflight_check()` passed
- [ ] Each element's `verify_phase()` ink count is above threshold
- [ ] Screenshot saved
- [ ] No calibration drift detected
- [ ] Composition complexity ≤ 2 levels deep
- [ ] Script length ≤ 80 lines (if exceeded, extract compositions)

---

*Every stroke is a planned path. Every pixel has a purpose. No insight without coordinates.*
