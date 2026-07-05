Copyright © 2026 Arsh Buttar. All rights reserved. Confidential and proprietary.
Unauthorized copying, distribution, or use of this work is prohibited.

# CINEMA SKILL — BOOK III: THE CAMERA

> This document extends Book I: The Constitution and Book II: The World.
> Everything written here obeys the Constitution.
> No principle in this document may violate Book I or Book II.
> This document defines the permanent observation handbook of Cinema.

---

## 1. PURPOSE

The Camera does not generate images.
The Camera observes reality.

The renderer creates images.
The Camera determines what reality is visible.

These are different responsibilities.

Book III defines the observation system.
It does not define rendering.

---

## 2. FUNDAMENTAL PHILOSOPHY

The Camera is not a recording device.
The Camera is a conscious observer.

Every shot begins with one question:

**"What can this observer physically perceive?"**

Everything outside that answer does not belong in the shot.

The Camera does not invent reality. It does not enhance reality. It does not embellish reality. It observes what is there and determines what portion of what is there becomes visible to the audience.

---

## 3. OBSERVABLE TRUTH

### 3.1 DEFINITION

Observable Truth is the complete set of information physically visible from one camera position at one instant.

It includes:
- Everything within the camera's field of view
- Everything not occluded by geometry or objects
- Everything within the visible distance range for the current lens
- Everything the lighting makes perceptible (lighting is determined by another department, but the Camera must respect it)

It excludes:
- Everything outside the field of view
- Everything behind occluding geometry
- Everything beyond the visible distance
- Everything in total darkness (if the lighting department has not illuminated it)

### 3.2 RULE

Anything outside Observable Truth does not exist for that shot.

Never compute beyond Observable Truth unless another department explicitly requires it.

### 3.3 IMPLICATION

This principle governs every future renderer. A renderer may only render what the Camera has determined to be observable. If the Camera has not declared something visible, the renderer has no authority to show it.

---

## 4. CAMERA RESPONSIBILITIES

The Camera Department owns only observation.

It never changes story.
It never changes emotion.
It never changes character.

It only determines how reality is observed.

Specifically, the Camera Department determines:
- Which observer is active
- Where the observer is positioned
- What the observer can see
- What the observer cannot see
- Where the observer directs attention
- How the observer moves
- How observation transitions between shots

The Camera Department does NOT determine:
- What happens in the story (Writer)
- What the environment looks like (Production Designer)
- How characters feel (Director)
- What light is present (Book VI — Lighting)
- What sound is present (Book VIII — Sound)

---

## 5. INTERNAL DEPARTMENTS

The Camera Department is itself divided into sub-departments. Each owns one responsibility. They are isolated from each other exactly as Book I's departments are isolated from each other.

### 5.1 CAMERA DIRECTOR

Owns: observer purpose

The Camera Director answers:
- Why does this shot exist?
- What is the audience's viewpoint?
- What should the audience be paying attention to?
- What is the emotional purpose of observing from this position?

The Camera Director does NOT choose lenses, positions, or movements. The Camera Director defines WHY we observe, not HOW.

### 5.2 CAMERA RIG

Owns: camera position and physical parameters

The Camera Rig answers:
- Where is the camera positioned in world space?
- At what height?
- At what orientation (pitch, yaw, roll)?
- What focal length (lens)?
- What movement (static, pan, tilt, dolly, track, handheld, crane)?
- What focus distance and focus pull?

The Camera Rig does NOT decide why the camera is there. It executes the positioning that fulfills the Camera Director's purpose.

### 5.3 VISIBILITY SOLVER

Owns: line of sight and occlusion

The Visibility Solver answers:
- What geometry is visible from the camera position?
- What geometry is occluded?
- What is partially visible?
- What is hidden?
- Which observer cell is the camera in?

The Visibility Solver computes. It never guesses. If it cannot compute, it declares the status as Unknown and flags it for resolution.

### 5.4 BLOCKING SOLVER

Owns: subject movement and timing

The Blocking Solver answers:
- Where do subjects move during the shot?
- What path do they follow?
- What is the timing of their movement?
- How do subjects interact with each other in space?
- When does a subject enter or leave the frame?
- When does a camera handoff occur?

The Blocking Solver works with the scene's action (from the Writer's scene_specification) and translates it into spatial choreography.

### 5.5 SHOT PLANNER

Owns: framing and composition

The Shot Planner answers:
- How is the frame composed?
- Where is the subject in the frame?
- What negative space exists?
- What is the visual hierarchy?
- Where should viewer attention be directed?
- What is the aspect ratio and safe area?

The Shot Planner works within the Camera Rig's field of view and the Visibility Solver's visible geometry.

### 5.6 CAMERA CONTINUITY

Owns: visual continuity between shots

Camera Continuity answers:
- Where was the previous camera?
- Where is the current camera?
- Is this transition allowed (does it violate the 180-degree rule, 30-degree rule, or eyeline match)?
- What screen direction is established?
- What is the established visual language?
- How does the next shot inherit the previous shot's framing?

Camera Continuity reads from the World Engine's continuity records and ensures no visual contradiction.

---

## 6. CAMERA PSYCHOLOGY

### 6.1 PRINCIPLE

Every project defines one camera personality.

The camera is not neutral. The camera has a character. That character determines how it observes.

### 6.2 PERSONALITY TYPES

The project may define one of these personalities (or define a custom one):

| Personality | Behavior |
|---|---|
| Patient Observer | Slow movements, long holds, wide frames, minimal cutting. Watches without interfering. |
| Curious Child | Low angles, quick pans, close-ups, restless movement. Discovers the world. |
| Silent Witness | Static framing, medium distance, observes without judgment. Does not move unless necessary. |
| Predator | High angles, tracking movement, telephoto compression, stalking perspective. |
| Survivor | Handheld, unstable, close to subject, reactive movement. Camera feels present and vulnerable. |
| Documentarian | Eye-level, neutral framing, natural movement. Invisible observation. |
| Memory | Soft focus, dreamlike movement, dissolves, subjective perspective. The camera remembers, not records. |

### 6.3 DERIVATION

The camera personality determines:
- Movement style (speed, smoothness, pattern)
- Pause behavior (how long the camera holds)
- Framing distance (how close the camera sits to subjects)
- Distance from action
- Reaction to events (does the camera flinch, settle, pursue, retreat?)

All camera decisions derive from personality. The Camera Director interprets the personality for each specific shot.

### 6.4 PROJECT ASSIGNMENT

The camera personality is defined at the project level. It persists across the entire project unless the Director explicitly changes it for narrative purposes (e.g., a flashback uses "Memory" personality while the present timeline uses "Patient Observer").

The personality is stored in the project's configuration and read by the Camera Department at the start of each scene.

---

## 7. OBSERVER CELLS

### 7.1 CONCEPT

The world is divisible into observation regions called Observer Cells.

An Observer Cell is a volume of space from which the set of visible geometry is approximately the same. Any camera placed within a cell sees the same occlusion pattern.

### 7.2 CELL CONTENTS

Each Observer Cell stores:
- Visible cameras (which cameras can observe into this cell)
- Hidden cameras (which cameras cannot observe into this cell)
- Distance (from cell to subjects of interest)
- Viewing angle (range of angles from which the cell can be observed)
- Occlusion (what geometry blocks lines of sight from this cell)
- Subject scale (how large subjects appear from this cell)
- Camera priority (which camera is preferred when multiple can observe)

### 7.3 PURPOSE

Observer Cells make observation deterministic. Instead of computing visibility from scratch for every shot, the Camera Department references the cell's precomputed visibility data.

When a subject moves between cells, the Blocking Solver tracks which cell the subject is in and the Visibility Solver knows immediately what is visible.

### 7.4 SCOPE

Book III defines the concept and ownership of Observer Cells. The actual spatial subdivision of the world into cells belongs to future implementation books.

---

## 8. LINE OF SIGHT

### 8.1 PRINCIPLE

Line of sight is computed. Never guessed.

### 8.2 VISIBILITY STATES

Every object, character, and geometry element in the world has one of these visibility states for any given camera position:

| State | Meaning |
|---|---|
| Visible | Fully within field of view, not occluded, within visible distance. |
| Partially Visible | Within field of view but partially occluded, or at the edge of the frame, or beyond full focus range. |
| Hidden | Exists in the world but outside field of view or fully occluded. |
| Occluded | Exists and is within field of view but completely blocked by intervening geometry. |
| Unknown | Visibility cannot be determined from available data. Flagged for resolution. |

### 8.3 REUSABILITY

Visibility determinations are reusable. Once the Visibility Solver has determined that a wall occludes a doorway from Camera A, that fact is stored in the Observer Cell and does not need to be recomputed for every shot from the same cell.

### 8.4 MOVEMENT

When a subject moves, the Visibility Solver tracks the transition:
- Subject was Visible → moves behind a wall → becomes Occluded
- Subject was Occluded → emerges from behind wall → becomes Visible
- Subject was Visible → exits frame edge → becomes Hidden

These transitions are logged by the Blocking Solver.

---

## 9. CAMERA HANDOFF

### 9.1 PRINCIPLE

When multiple cameras exist, handoffs must be deterministic. Never randomly choose cameras.

### 9.2 HANDOFF PROTOCOL

The Camera Department always knows:

1. **Current Observer** — which camera is actively observing
2. **Next Observer** — which camera will observe next
3. **Reason for Transition** — why the handoff occurs (narrative beat, subject movement, attention shift)
4. **Transition Timing** — when the handoff occurs (at what beat, what frame, what action)

### 9.3 HANDOFF RULES

- A handoff occurs only when the Camera Director determines a narrative reason.
- The handoff must respect Camera Continuity (no 180-degree violation, no jump cut without purpose).
- The handoff timing must align with the Editor's rhythm (Book IX) — but the Camera Department proposes the timing.
- After a handoff, the new observer inherits the visual language established by the previous observer unless the Camera Director explicitly changes it.

---

## 10. SCRUBBER PRINCIPLE

### 10.1 CONCEPT

The observer never perceives infinite information.

The camera deliberately ignores unnecessary detail.

### 10.2 RULE

Observation is constrained. The camera does not attempt to perceive everything in the world. It perceives only what matters for the current shot.

### 10.3 IMPLICATION

Computation follows observation. The Camera Department does not compute visibility for objects that do not affect the current shot. The Visibility Solver determines the relevant set of objects and computes only for those.

This means:
- Background objects beyond the focal plane are noted but not fully resolved.
- Objects outside the narrative scope of the shot are marked Hidden but not analyzed.
- Detail is allocated where attention is directed, not uniformly across the frame.

### 10.4 FOUNDATIONAL STATUS

This is a foundational philosophy. It governs all future implementation. The Scrubber Principle ensures that Cinema never wastes computation on what the observer cannot meaningfully perceive.

---

## 11. PRECOMPUTATION

### 11.1 PRINCIPLE

Whenever geometry is static, visibility should become precomputable.

### 11.2 SCOPE

Book III only defines this philosophy. The actual precomputation system — building visibility maps, caching occlusion data, precomputing observer cell contents — belongs to future implementation books.

### 11.3 INTENT

The intent is that static environments (buildings, streets, furniture) have fixed occlusion patterns. These patterns should be computed once and reused across all shots in that environment, rather than recomputed for every camera position.

Dynamic objects (characters, moving props, weather particles) are computed per-shot against the precomputed static visibility map.

---

## 12. CAMERA OUTPUT

### 12.1 DOCUMENT

The Camera Department produces only one document:

**`camera_specification`**

### 12.2 CONTENTS

```
camera_specification:
  scene_number: <N>
  
  camera_personality: "<project-defined personality>"
  
  shot: <shot_number>
  
  camera_director:
    purpose: "Why this shot exists"
    audience_viewpoint: "Whose perspective"
    attention_target: "What the audience should watch"
    emotional_purpose: "What the observation feels like"
  
  camera_rig:
    position: "world-space coordinates"
    height: "camera height"
    orientation:
      pitch: "<value>"
      yaw: "<value>"
      roll: "<value>"
    focal_length: "<lens in mm>"
    movement: "static | pan | tilt | dolly | track | handheld | crane"
    movement_path: "description of movement if not static"
    focus_distance: "<value>"
    focus_pull: "description of focus change if any"
  
  visibility:
    observer_cell: "<cell_id>"
    visible_objects: ["list of what is visible"]
    partially_visible: ["list of what is partially visible"]
    hidden: ["list of what is hidden"]
    occluded: ["list of what is occluded"]
  
  blocking:
    subject_paths: "how subjects move during this shot"
    frame_entries: "when subjects enter frame"
    frame_exits: "when subjects leave frame"
    interactions: "spatial interactions between subjects"
    handoff: "if a camera handoff occurs, when and why"
  
  shot_planner:
    framing: "description of frame composition"
    subject_position_in_frame: "where subject sits in the frame"
    negative_space: "where empty space is"
    visual_hierarchy: "order of visual importance"
    attention_direction: "where viewer eye should go"
    aspect_ratio: "9:16"
    safe_area: "what must remain visible on all devices"
  
  camera_continuity:
    previous_shot: "<shot_id>"
    established_screen_direction: "left-to-right | right-to-left"
    transition_type: "cut | dissolve | match-cut"
    transition_validated: true
    inherited_visual_language: "what carried over from previous shot"
  
  scrubber:
    relevant_objects: ["only objects that affect this shot"]
    ignored_detail: "what the camera is deliberately not perceiving"
  
  observable_truth: >
    The complete set of information physically visible from this
    camera position at this instant. This is what the renderer
    is authorized to show.
```

### 12.3 CONSUMER

This document becomes input to Books VI (Lighting), VIII (Sound), IX (Editor), and XIII (Prompt Compiler). No renderer-specific language appears here. The camera_specification describes observation, not rendering.

---

## 13. EXECUTION POSITION

The full execution order is defined in Book I, Section 11 (Execution Order). The Camera Department works after Spatial Staging and the Character Supervisor, and before Lighting.

Camera reads:
- `scene_specification` (Writer)
- `environment_specification` (Production Designer)
- `spatial_staging_specification` (Book VII)
- `continuity_report` (Character Supervisor)
- `cinematic_language_specification` (Book IV)
- `world_state` (Book II)

Camera produces:
- `camera_specification`

The Producer merges the camera_specification with all other documents into the production_specification.

---

## 14. ACCEPTANCE TEST

### 14.1 SCENARIO

Given:
- A world (from Book II)
- Three cameras (Camera A, Camera B, Camera C)
- One moving subject (Biscuit walking down a street)
- Static geometry (buildings, a van, a chai stall)

### 14.2 EXPECTED BEHAVIOR

The Camera Department should determine:

**Which camera currently observes:**
- Based on the camera personality, the Camera Director selects the active observer.
- Based on Biscuit's position (from world_state), the Visibility Solver determines which cameras can see him.
- If Camera A can see Biscuit but Camera B is occluded by the van, Camera A is the current observer.

**What is visible:**
- The Visibility Solver computes: Biscuit is Visible from Camera A. The chai stall is Visible. The van's near side is Visible. The van's far side is Occluded. The alley behind the stall is Hidden.

**What is hidden:**
- Scraps sleeping behind the van is Occluded from Camera A. He is not in the shot. He still exists in the world (Book II ensures this) but the camera cannot perceive him.

**Where attention should be directed:**
- The Shot Planner places Biscuit at the left third of the frame. The chai stall occupies the right third. Negative space is above Biscuit. Attention is directed to Biscuit's face, then to the chai stall steam.

**How the next shot inherits the previous shot:**
- Camera Continuity records: Camera A was at eye-level, looking left-to-right. Screen direction is established. If the next shot uses Camera B, it must respect the established screen direction unless the Camera Director explicitly breaks it for narrative purpose.

### 14.3 INVARIANT

This entire determination occurs without involving any renderer. The camera_specification is produced. It describes what is observable. A future renderer may only render what this document authorizes.

---

## 15. LENS AND SENSOR SCIENCE

### 15.1 SENSOR FORMATS

The camera sensor determines field of view, depth of field characteristics, and light sensitivity. Different productions may use different sensor formats.

| Format | Sensor Width (mm) | Crop Factor (vs FF) | Circle of Confusion (mm) | Common Cameras |
|---|---|---|---|---|
| Full Frame | 36.0 | 1.0x | 0.029 | Sony VENICE, Alexa LF, Canon R5C |
| Super 35 | 24.89 | 1.5x | 0.019 | Alexa Mini, Sony FX6, BMPCC 6K |
| APS-C | 23.6 | 1.5x | 0.019 | Fuji X, Sony a series |
| Micro Four Thirds | 17.3 | 2.0x | 0.015 | Panasonic GH, BMPCC 4K |
| Broadcast 2/3" | 9.6 | 3.7x | 0.011 | ENG cameras |
| IMAX | 52.5 | 0.7x | 0.035 | IMAX film cameras |

The Circle of Confusion (CoC) is calculated using the Zeiss formula: sensor diagonal / 1500. This is the standard used by the ASC Manual and professional cinematography tools.

### 15.2 T-STOP VS F-STOP

| Measure | Definition | Used For |
|---|---|---|
| f-stop | Geometric ratio of focal length to aperture diameter (f/N) | Depth of field calculations |
| T-stop | Actual light transmission accounting for glass absorption | Exposure metering |

For DOF calculations, use f-stop. For exposure planning, use T-stop. Most cinema lenses are marked in T-stops.

### 15.3 DEPTH OF FIELD CALCULATION

Depth of field is calculated using the hyperfocal distance equation from the ASC Manual:

```
H = f² / (N × c) + f
```

Where:
- H = hyperfocal distance (mm)
- f = focal length (mm)
- N = f-stop number
- c = circle of confusion (mm)

Once hyperfocal distance is known:

```
Near Limit = H × d / (H + (d - f))
Far Limit = H × d / (H - (d - f))
```

Where d = subject distance (mm). If d ≥ H, far limit extends to infinity.

Total DOF = Far Limit - Near Limit

DOF is governed by four variables:

| Variable | Effect on DOF | Shallow DOF | Deep DOF |
|---|---|---|---|
| Aperture (f-stop) | Wider aperture = shallower DOF | f/1.4, f/2 | f/8, f/11 |
| Focal length | Longer lens = shallower DOF | 85mm, 135mm | 24mm, 35mm |
| Subject distance | Closer subject = shallower DOF | 1 meter | 5+ meters |
| Sensor size | Larger sensor = shallower DOF (at same FoV) | Full Frame | Micro Four Thirds |

### 15.4 DEPTH OF FIELD QUICK REFERENCE

For a subject at 2 meters on Super 35 sensor:

| Focal Length | f/2.8 | f/5.6 | f/11 |
|---|---|---|---|
| 24mm | 1.4m → ∞ | 0.9m → ∞ | 0.5m → ∞ |
| 50mm | 1.9m → 2.1m | 1.8m → 2.3m | 1.5m → 3.0m |
| 85mm | 1.97m → 2.03m | 1.93m → 2.07m | 1.85m → 2.17m |

These values are approximate. Use the DOF calculator for precision.

### 15.5 CAMERA MOVEMENT PHYSICS

Camera movement is defined by spatial path, velocity profile, and acceleration envelope.

**Movement Types with Physical Properties:**

| Movement | Axis | Typical Speed | Emotional Effect | Equipment |
|---|---|---|---|---|
| Static | None | 0 | Stability, neutrality | Tripod, locked-off |
| Pan | Yaw (horizontal rotation) | 5-30 deg/s | Scanning, revealing, following | Tripod head |
| Tilt | Pitch (vertical rotation) | 5-20 deg/s | Revealing height, power dynamic | Tripod head |
| Dolly In | Z (forward) | 0.3-1.0 m/s | Intimacy, tension, focus | Dolly, track |
| Dolly Out | Z (backward) | 0.3-1.0 m/s | Isolation, revelation, release | Dolly, track |
| Truck | X (lateral) | 0.5-1.5 m/s | Following, parallel movement | Dolly, track |
| Boom/Crane | Y (vertical) | 0.3-0.8 m/s | Scale, power, reveal | Crane, jib |
| Arc | Curved XY path | 0.3-1.0 m/s | 3D revelation, circling | Curved track |
| Steadicam | Any axis, stabilized | 0.5-2.0 m/s | Fluid, immersive, following | Steadicam, gimbal |
| Handheld | Any axis, unstabilized | Variable | Urgency, vulnerability, realism | Handheld rig |
| Zoom | Optical (no physical move) | Variable | Attention without perspective change | Zoom lens |
| Dolly Zoom | Z + optical simultaneous | Coordinated | Disorientation, Vertigo effect | Dolly + zoom lens |

**Velocity Profile:**
- Acceleration phase (0 → target velocity): 0.3-0.5s for smooth start
- Cruise phase (constant velocity): maintains target speed
- Deceleration phase (target velocity → 0): 0.3-0.5s for smooth stop

**Rule:** Camera movement must have a definite purpose matching the camera personality. Random movement disorients the audience. Every acceleration must be motivated by narrative intent.

### 15.6 FOCAL LENGTH AND PERSPECTIVE

| Focal Length | Category | Field of View (S35) | Perspective Effect |
|---|---|---|---|
| 14-24mm | Ultra-wide | >90° | Exaggerated depth, distortion at edges, dynamic |
| 24-35mm | Wide | 75-90° | Moderate depth, environmental, establishing |
| 35-50mm | Normal | 40-55° | Natural perspective, closest to human eye |
| 50-85mm | Short telephoto | 25-40° | Flattering portraits, moderate compression |
| 85-135mm | Medium telephoto | 15-25° | Flattering compression, isolates subject |
| 135-200mm | Long telephoto | 8-15° | Strong compression, flattens space |
| 200mm+ | Super telephoto | <8° | Extreme compression, surveillance effect |

### 15.7 EXPOSURE TRIANGLE

The Camera Rig must consider the relationship between:

- **Aperture (T-stop)**: Controls DOF and light transmission
- **Shutter speed/angle**: Controls motion blur (180° rule = 1/48s at 24fps)
- **ISO**: Controls sensitivity (higher ISO = more noise/grain)

Default setting: 24fps, 1/48s shutter, T-stop appropriate for required DOF, ISO set to achieve correct exposure based on Lighting department's lux levels.

---

## 16. SCOPE BOUNDARY

This book defines ONLY the observation system.

It does NOT define:
- Rendering or image generation
- Renderer-specific prompts or syntax
- Lighting systems or lighting specifications
- Sound systems or sound specifications
- Editing systems or edit decision lists
- Plugin systems
- Veo, SDXL, Flux, Sora, or any renderer integration
- YAML schemas for storage (the camera_specification is a document format, not a storage schema)

Those belong to future books.

---

## 17. CONSTITUTIONAL COMPLIANCE

This book complies with all applicable principles from Books I and II: departments are isolated, the World is the single source of truth, nothing resets automatically, camera continuity inherits from previous shots, execution order is preserved, and model independence. No principle in this document violates the Constitution or the World.

---

## 18. SPATIAL COHERENCE & DOF MANAGEMENT

### 18.1 PRINCIPLE

Every simultaneous camera movement consumes a portion of the renderer's spatial coherence budget. Independent movements compete for the same spatial reasoning capacity. When the budget is exceeded, the world hallucinates — geometry deforms, pillars slide, roads detach from their environment.

Spatial coherence is the renderer's ability to maintain a stable, continuous 3D world across a camera movement. Coherence degrades as the number of independent camera DOFs (degrees of freedom) increases.

### 18.2 DOF BUDGET

A Degree of Freedom (DOF) is one independent axis of camera movement:

| Movement | DOF | Axis |
|---|---|---|
| Pan | 1 | Yaw (horizontal rotation) |
| Tilt | 1 | Pitch (vertical rotation) |
| Roll | 1 | Bank (rotation around lens axis) |
| Dolly | 1 | Forward/backward translation (Z) |
| Track/Truck | 1 | Lateral translation (X) |
| Crane/Boom | 1 | Vertical translation (Y) |
| Zoom | 1 | Focal length change |
| Focus pull | 0 | (Does not affect spatial coherence) |

**Budget rule:**
- 1-2 simultaneous DOFs: Safe. Maximum spatial coherence.
- 3 simultaneous DOFs: Manageable if coupled into a single purposeful trajectory. Risk depends on coupling.
- 4+ simultaneous DOFs: High risk of spatial hallucination. Only acceptable with extreme spatial anchoring and coupled trajectories.
- 5+ simultaneous DOFs: Known to cause failure. Geometry deforms, world slides, spatial relationships break.

Each zoom or focus rack counts as a DOF only if it occurs simultaneously with camera translation or rotation. A zoom alone (0 translation, 0 rotation) is 1 DOF and safe.

### 18.3 DOF COUPLING

DOFs that are COUPLED into a single trajectory consume less budget than independent DOFs.

**Coupled**: Forward dolly + vertical crane + pitch tilt, tracing a single smooth arc (like a stone thrown upward). The renderer computes one trajectory, not three independent axes.

**Uncoupled**: Forward dolly while rolling while swaying laterally, with no geometric relationship between the axes. The renderer must compute three independent movements and maintain spatial coherence across all three simultaneously.

**Rule:**
- Always prefer coupled DOFs over independent DOFs.
- A coupled multi-DOF movement is equivalent to a lower-budget movement than the same number of uncoupled DOFs.
- The coupling must be geometric — the axes must share a purpose. A dolly + crane + pitch that trace an arc are coupled. A dolly + roll + lateral sway are not coupled unless the scene geometry justifies them.

### 18.4 SPATIAL ANCHORING

Camera positions and subject trajectories must be described in WORLD-RELATIVE terms, not frame-relative terms.

| Description type | Example | Reliability |
|---|---|---|
| World-relative | "The rider is on the road surface at the far end of the curve. Her wheels are on the asphalt." | High — anchors subject to world geometry |
| Frame-relative | "The rider appears at the upper-left of frame." | Low — describes a 2D pixel position, not a 3D spatial relationship |

**Rule:**
- Every subject position must reference world geometry (road surface, bridge deck, mesa base, canyon rim).
- Frame coordinates (upper-left, center-right, lower-third) must NEVER substitute for world coordinates.
- Frame coordinates may supplement world coordinates but never replace them.
- The spatial anchor (the fixed geometry the subject relates to) must be explicitly declared.

### 18.5 ACTIVE VS PASSIVE DOFS

A DOF may be active (a creative camera choice) or passive (a mechanical constraint of the rig).

- **Passive DOF**: A drone maintains a fixed distance behind a moving subject. The drone translates forward, but this is not a creative choice — it is the minimum requirement of keeping the subject in frame. Passive DOFs consume minimal budget.
- **Active DOF**: A zoom-out from 200mm to 24mm that transforms the subject from frame-dominant to landscape-insignificant. This is the creative movement. Active DOFs consume the budget.

**Rule:**
- Declare whether each DOF is active or passive in the camera specification.
- Passive DOFs may be discounted from the budget. Active DOFs count fully.
- A camera rig that "follows" a subject (matching speed, maintaining distance) is passive. The camera movement that carries narrative intent is active.

### 18.6 THE SCALE REVEAL

A single-active-DOF technique: the zoom-out from telephoto to wide with the camera at a fixed distance from the subject.

The camera maintains constant position relative to the subject. The focal length racks from telephoto (200mm+) to wide (24mm-35mm). The subject shrinks in frame. The landscape expands. The subject transforms from frame-dominant to landscape-insignificant.

This creates a specific emotional arc:
- **Compression**: Telephoto flattens space, subject feels close and substantial.
- **Opening**: As focal length widens, space expands. The background grows.
- **Revelation**: Wide focal length reveals the landscape's true scale. The subject becomes a tiny element within it.
- **Dread/Isolation**: The subject is lost in the space. The landscape dominates.

**Technical requirements:**
- 1 active DOF (zoom) + 0-1 passive DOFs (tracking the subject).
- Subject stays centered in frame throughout.
- The zoom must be continuous and smooth — no steps or cuts.
- The landscape must be spatially consistent across the focal length range. No new landmarks appear. The telephoto compression does not "hide" anything — the wide reveal is the same world, just seen at its true scale.

### 18.7 APPLICATION TO PROMPT CONSTRUCTION

When the Camera Department produces its specification, it must include:
- Explicit DOF count (number of simultaneous movements)
- DOF coupling declaration (are the DOFs coupled into a single trajectory?)
- Active vs passive DOF identification
- Spatial anchor declaration (what fixed geometry the camera and subject relate to)
- World-relative position descriptions for all subjects in all key frames

The Prompt Compiler (Book XIII) uses these declarations to construct a render prompt that preserves spatial coherence.
