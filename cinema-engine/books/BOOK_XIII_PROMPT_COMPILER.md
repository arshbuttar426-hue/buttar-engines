Copyright © 2026 Arsh Buttar. All rights reserved. Confidential and proprietary.
Unauthorized copying, distribution, or use of this work is prohibited.

# CINEMA SKILL — BOOK XIII: THE PROMPT COMPILER

> This document extends Books I through XII.
> Everything written here obeys the Constitution.
> No principle in this document may violate any previous book.
> This book becomes the permanent compilation authority of Cinema.
> The Prompt Compiler translates — it does not create.

---

## 1. PURPOSE

The Prompt Compiler is the final department in the Cinema pipeline. Every other department — Camera, Lighting, Sound, Production Designer, Spatial Staging, Director, Editor — produces specifications. The Prompt Compiler takes all specifications and compiles them into a single, coherent, renderer-agnostic instruction set.

The Prompt Compiler does not create content. The Prompt Compiler ensures that the content created by all other departments can be expressed as a complete, unambiguous instruction set to the renderer.

---

## 2. RESPONSIBILITY

The Prompt Compiler owns:

- **Collection** — gathering all department specifications
- **Validation** — checking completeness of required fields
- **Cross-book consistency checking** — verifying specifications are compatible
- **Compilation** — organizing specifications into a renderer-agnostic format
- **Format adaptation** — translating the intermediate format to renderer-specific syntax
- **DOF budget declaration** — including spatial coherence constraints from the Camera
- **Temporal breakdown** — structuring the prompt as a second-by-second timeline
- **Compilation logging** — documenting what was compiled and any warnings

Nothing else.

---

## 3. COMPILATION PIPELINE

```
INPUT PHASE:
  Book II (World) → Current world state snapshot
  Book III (Camera) → Shot specification (lens, position, movement, DOF)
  Book IV (Cinematic Language) → Visual grammar keys
  Book V (Director) → Narrative intent, emotional objective, scene weight
  Book VI (Lighting) → Light positions, colors, intensities, ratios
  Book VII (Spatial Staging) → Character positions, orientations, blocking
  Book VIII (Sound) → Sound hierarchy, levels, emotional frequency profile
  Book IX (Editor) → Rhythm, transition type, pacing
  Book X (Production Designer) → Color palette, environment description, props
  Book XI (Character Supervisor) → Character state, continuity constraints
  Book XII (Producer) → Merged production specification

COMPILATION PHASE:
  1. COLLECT — Gather all specifications from all departments
  2. VALIDATE — Check for completeness (every required field filled)
  3. DEDUPLICATE — Resolve conflicting instructions with Producer's conflict log
  4. STRUCTURE — Organize into renderer-agnostic template
  5. FORMAT — Apply output-target-specific formatting

OUTPUT PHASE:
  Compiled prompt → sent to renderer
  Compilation log → returned for verification
```

---

## 4. VALIDATION

### 4.1 REQUIRED INPUT FIELDS

Every compiled prompt must contain:

| Field | Source Book |
|---|---|
| scene_id | World (II) |
| narrative_intent | Director (V) |
| emotional_objective | Director (V) |
| camera_position | Camera (III) |
| camera_lens | Camera (III) |
| character_positions | Spatial Staging (VII) |
| character_state | Character Supervisor (XI) |
| lighting_spec | Lighting (VI) |
| sound_profile | Sound (VIII) |
| color_palette | Production Designer (X) |
| visual_grammar | Cinematic Language (IV) |
| transition_type | Editor (IX) |

Any missing mandatory field → prompt is not sent → error returned to originating department.

### 4.2 CROSS-BOOK CONSISTENCY CHECKS

| Check | Books Involved | What's Verified |
|---|---|---|
| Lighting-Set Conflict | VI + X | Light temperature vs. set color produces expected result |
| Camera-Staging Conflict | III + VII | Camera can see all positioned characters |
| Sound-Editor Conflict | VIII + IX | Sound levels match editorial emphasis |
| Continuity-Camera Conflict | XI + III | Lens/FOV matches what Character Supervisor logged |
| Director-ProductionDesign | V + X | Color palette supports emotional objective |
| Spatial-Camera Movement | VII + III | Movement path does not clip through characters |

Any failed check → halt compilation → send conflict alert to Producer (Book XII).

---

## 5. TEMPORAL BREAKDOWN

### 5.1 PRINCIPLE

The renderer processes temporally. It generates frames in sequence. The prompt structure must match this temporal nature.

A prompt that describes the scene as a static collection of attributes forces the renderer to infer temporal behavior. A prompt that describes the scene as a temporal sequence (second-by-second, beat-by-beat) tells the renderer exactly what to generate at each moment.

### 5.2 SECOND-BY-SECOND FORMAT

Every temporal prompt should contain a timeline:

```
SECOND-BY-SECOND:

0s — [State at start: camera position, subject position, environment state, sound state]
1s — [What changes by 1s: camera movement progress, subject movement, new visual elements]
2s — [What develops: intermediate state]
...
8s — [Final state: what the frame holds at the end]
```

Rules:
- Each entry describes what EXISTS at that moment — camera state, subject position, visible elements, sound.
- Each entry describes what CHANGES from the previous second — camera movement progress, subject displacement, new elements.
- Sound is integrated into each entry, not described separately.
- Spatial positions are described in world-relative terms.

### 5.3 WORLD-RELATIVE VS FRAME-RELATIVE

Every subject position must be described relative to world geometry.

| Type | Format | Example |
|---|---|---|
| World-relative (correct) | Subject + spatial relationship to world geometry | "The rider is ON the road surface at the far end of the curve." |
| Frame-relative (incorrect) | Subject + position within the 2D frame | "The rider appears at the upper-left of frame." |

The Prompt Compiler must reject any department specification that describes subject position in frame-relative terms without a corresponding world-relative anchor.

### 5.4 DOF BUDGET DECLARATION

When the Camera Department (Book III) specifies camera movement, the Prompt Compiler must include a DOF budget declaration:

```
CAMERA — DOF BUDGET: N DOFs (X active, Y passive)
- [DOF 1]: description (active/passive)
- [DOF 2]: description (active/passive)
- Coupling: [coupled/independent]
```

If the budget exceeds safe limits (see Book III Section 18.2), the Prompt Compiler must flag the risk.

### 5.5 SPATIAL COHERENCE CONSTRAINTS

The compiled prompt must include explicit spatial coherence constraints:

```
SPATIAL COHERENCE CONSTRAINTS:
1. [Fixed geometry element] must remain [stable behavior] — it must NOT [hallucinated behavior].
2. [Subject] must stay [spatial relationship to world geometry] — it must NOT [incorrect behavior].
```

### 5.6 INTEGRATED SOUND

Sound must be integrated into the temporal breakdown, not described as a separate block. Each second entry includes the sound state at that moment, matching the visual state.

---

## 6. TEMPLATE SYSTEM

### 6.1 RENDERER-AGNOSTIC INTERMEDIATE FORMAT

```yaml
prompt:
  meta:
    scene_id: "SCENE_ID"
    compiled_at: "TIMESTAMP"
    departments_contributing: ["II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X", "XI", "XII"]
    compiler_notes: "FREE_TEXT"

  world:
    environment: "WORLD_DESCRIPTION"
    time_of_day: "DAWN|DAY|DUSK|NIGHT"
    weather: "CLEAR|OVERCAST|RAIN|FOG|STORM"
    location_id: "LOCATION_REF"

  camera:
    position: [x, y, z]
    target: [x, y, z]
    focal_length_mm: NUMBER
    aperture_f: NUMBER
    sensor_format: "FULL_FRAME|SUPER_35|MFT|CUSTOM"
    movement:
      type: "STATIC|PAN|TILT|DOLLY|TRUCK|CRANE|STEADICAM|HANDHELD|ZOOM|DOLLY_ZOOM|ARC|AERIAL"
      path: [sequence of [x, y, z, time]]
    focus:
      target: "CHARACTER|OBJECT|DISTANCE"
      distance_m: NUMBER

  lighting:
    key:
      position: [x, y, z]
      intensity_lux: NUMBER
      color_temp_k: NUMBER
    fill:
      position: [x, y, z]
      intensity_lux: NUMBER
      color_temp_k: NUMBER
      ratio_to_key: NUMBER
    back:
      position: [x, y, z]
      intensity_lux: NUMBER
      color_temp_k: NUMBER
    practicals: [list of additional light sources]
    ambient:
      base_level_lux: NUMBER
      color_temp_k: NUMBER

  characters:
    - id: "CHARACTER_ID"
      position: [x, y, z]
      orientation_deg: NUMBER
      action: "ACTION_DESCRIPTION"
      emotional_state:
        primary: "EMOTION"
        intensity: 1-10
      costume_colors: ["HEX"]
      props: [list of visible props]

  sound:
    hierarchy:
      primary: "DIALOGUE|SCORE|AMBIENCE|FOLEY|SILENCE"
      secondary: "..."
      tertiary: "..."
    levels:
      dialogue_db: NUMBER
      music_db: NUMBER
      ambience_db: NUMBER
      effects_db: NUMBER

  editorial:
    transition_from_previous: "CUT|FADE|DISSOLVE|WIPE|JUMP_CUT|MATCH_CUT|NONE"
    transition_duration_frames: NUMBER
    internal_tempo: "SLOW|MODERATE|BRISK|RAPID|STACCATO"

  production_design:
    dominant_palette:
      hues: ["HEX", "HEX", "HEX"]
      saturation_range: [low, high]
      brightness_range: [low, high]
    environment_condition: "DESCRIPTION"

  visual_grammar:
    active_keys: ["GRAMMAR_KEYS"]
    hierarchy:
      primary_focus: "SUBJECT"
      secondary_focus: "SUBJECT"

  narrative:
    intent: "DESCRIPTION"
    emotional_objective: "EMOTION"
    scene_weight: 1-10
```

### 6.2 OUTPUT FORMATTING (MANDATORY STANDARD)

The Prompt Compiler MUST produce the output as `R###_<name>_prompt.md` — a standalone markdown file in the project root directory.

This file MUST contain a single markdown code block with the following sections in order:

| Section | Contents |
|---|---|
| STYLE | Photorealistic or stylized specification, camera body, sensor, color grade, grain |
| NEGATIVE | Excluded styles, artifacts, visual failures |
| LIGHTING | Primary/secondary sources, color temperatures, shadow philosophy, volumetrics |
| ENVIRONMENT | Location, geography, weather, time of day, season, atmosphere |
| BIKE/VEHICLE | Vehicle description, colors, visible mechanics, state |
| RIDER/CHARACTER | Character description, gear, constraints (never looks at camera, etc.) |
| SHOT SEQUENCE | Per-shot: camera rig, DOF count, duration, second-by-second action, synchronous sound |
| COLOR PALETTE | RGB values for all key elements |
| SPATIAL COHERENCE CONSTRAINT | DOF budgets, spatial anchors, world-relative positions |

Additionally, the file MUST append a **Spatial Coherence Validation** table and a **Lessons Applied** section outside the code block.

The file naming convention is:
- `R###` = episode number (R101, R102, etc.)
- `_<name>_` = short episode descriptor
- `prompt.md` = suffix

Example: `R101_the_curve_prompt.md`, `R102_vastness_prompt.md`

The Prompt Compiler maintains format adapters for each known renderer type. When a new renderer is encountered, a new adapter is created. However, the `R###_<name>_prompt.md` file format is invariant across all renderers — the adapter transforms the content within the code block, not the file format itself.

---

## 7. COMPILATION LOG

After every compilation, the Prompt Compiler generates:

```
COMPILATION LOG
Scene: SCENE_ID
Version: N
Status: PASS | FAIL | WARN

Mandatory fields: 12/12 present ✓
Optional fields:  8/14 present ⚠
Cross-book checks: 6/6 passed ✓
Renderer compatibility: ALL supported ✓

Warnings:
  - sound_profile.tension_hz not specified (defaulting to 30-60Hz)
  - editorial.transition_duration_frames not specified (defaulting to 0/cut)

Next action: Send to renderer ✓
```

---

## 8. EXECUTION POSITION

The Prompt Compiler works after the Producer has merged all department documents. The full execution order is defined in Book I, Section 11 (Execution Order).

The Prompt Compiler reads the `_sequence.yaml` production_specification (produced by the Producer) and produces the render prompt as a standalone file: `R###_<name>_prompt.md`. No other department works after the Prompt Compiler.

The Prompt Compiler MUST also update the `_sequence.yaml` to note that the episode fragment has been compiled (add `compiled: true` and the `R###_<name>_prompt.md` filename to the fragment metadata).

---

## 9. INTEGRITY RULES

1. The Prompt Compiler never invents specifications. If a department has not provided a mandatory field, the prompt is not sent.
2. Defaults are documented and transparent. Every default value must have a rationale.
3. The compiled prompt is the single source of truth for the renderer. No last-minute changes after compilation.
4. Cross-book consistency checks are enforced before compilation. If checks fail, the Producer is notified, not bypassed.
5. The Prompt Compiler is renderer-agnostic. Format adapters must be separate from the compilation logic.
6. No creative authority. Pure translation.

---

## 10. ACCEPTANCE TEST

### 10.1 SCENARIO

All 11 department documents have been produced and merged by the Producer into a production_specification. The Prompt Compiler must compile these into a single render-ready prompt with temporal breakdown, DOF budget declaration, spatial coherence constraints, and integrated sound.

### 10.2 EXPECTED BEHAVIOR

1. All mandatory fields are present and validated
2. Cross-book consistency checks pass
3. A second-by-second temporal breakdown is produced
4. DOF budget is declared with active/passive distinction
5. Spatial coherence constraints are explicit
6. Sound is integrated into temporal beats
7. All positions are world-relative, not frame-relative
8. The compilation log is generated with status PASS

### 10.3 INVARIANT

The compiled prompt contains only translations of department specifications. No creative embellishment. No invented details. Every element can be traced back to its originating department. The renderer receives complete, unambiguous instructions.

---

## 11. SCOPE BOUNDARY

This book defines ONLY the Prompt Compiler.

It does NOT define:
- Camera positions, lenses, or movement (Book III)
- Lighting systems (Book VI)
- Spatial staging (Book VII)
- Sound design (Book VIII)
- Editing rhythm (Book IX)
- Production design (Book X)
- Character continuity (Book XI)
- Conflict resolution (Book XII)
- Any creative or narrative decisions
- Any specific renderer's API, syntax, or capabilities

---

## 12. CONSTITUTIONAL COMPLIANCE

This book obeys all principles from Book I:

- The Prompt Compiler has no creative authority. ✅ (Explicitly restated in Section 9)
- Departments are isolated. ✅ (Prompt Compiler reads only the merged production_specification)
- The World is the single source of truth. ✅ (Prompt Compiler validates against world state)
- Never lose continuity. ✅ (Continuity constraints are embedded in every prompt)
- Model independence. ✅ (Format adapters handle renderer-specific syntax; compilation logic is agnostic)

No principle in this document violates the Constitution or any previous book.
