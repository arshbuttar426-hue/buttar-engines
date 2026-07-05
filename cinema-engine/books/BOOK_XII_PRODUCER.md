Copyright © 2026 Arsh Buttar. All rights reserved. Confidential and proprietary.
Unauthorized copying, distribution, or use of this work is prohibited.

# CINEMA SKILL — BOOK XII: THE PRODUCER

> This document extends Books I through XI.
> Everything written here obeys the Constitution.
> No principle in this document may violate any previous book.
> This book becomes the permanent conflict resolution authority of Cinema.
> The Producer creates the conditions under which all departments can work together.

---

## 1. PURPOSE

The Producer is the system-level authority that ensures the project survives the tension between creative ambition and operational reality. The Producer does not create content — the Producer creates the conditions under which content can be created.

The Producer manages the boundary conditions: conflict resolution, cross-department consistency, and the merge of all department outputs into a unified production specification.

---

## 2. RESPONSIBILITY

The Producer owns:

- **Conflict detection** — identifying contradictions between department outputs
- **Conflict resolution** — resolving contradictions using the priority protocol
- **Document merging** — combining all department documents into a unified production_specification
- **Cross-book consistency** — ensuring specifications from different books are compatible
- **Escalation management** — routing unresolved conflicts to the appropriate authority
- **Final verification** — validating the merged specification before it reaches the Prompt Compiler

Nothing else.

---

## 3. THE 6-DOMAIN CONFLICT DETECTION SYSTEM

The Producer maintains a continuous conflict detection system spanning 6 domains.

### DOMAIN 1: CREATIVE

Sources of conflict: Two departments producing contradictory scene specifications. Director's notes contradicting established world state.

Detection: Comparison of department outputs reveals logical contradictions. A character simultaneously in two locations. A prop simultaneously consumed and active.

Resolution path:
1. Department heads resolve at their level
2. Producer facilitates mediation
3. Director makes final creative call

### DOMAIN 2: CHARACTER CONTINUITY

Sources of conflict: Character state mismatches, prop inconsistencies, timeline logic errors.

Detection: Character Supervisor (Book XI) flags contradictions. Cross-scene comparison of state machines reveals inconsistencies.

Resolution path:
1. Department responsible corrects the error
2. If impractical to correct, Character Supervisor documents the compromise
3. Director decides whether to accept

### DOMAIN 3: CROSS-BOOK CONSISTENCY

Sources of conflict: Camera specs vs. lighting design, lighting design vs. set color palette, spatial staging vs. camera placement, sound design vs. editorial rhythm.

Detection: Each book's output is compared against its dependent book's inputs. Any mismatch generates an alert.

Resolution path:
1. Affected department heads meet to reconcile
2. Producer mediates if departments cannot agree
3. Director arbitrates creative trade-offs

### DOMAIN 4: SPATIAL LOGIC

Sources of conflict: Character positions violating environment geometry. Camera positions impossible within the set. Movement paths that clip through objects.

Detection: Spatial_staging_specification cross-checked against environment_specification. Camera positions validated against set dimensions.

Resolution path:
1. Spatial Staging and Camera reconcile
2. Production Designer adjusts environment if needed
3. Producer validates the resolution

### DOMAIN 5: TEMPORAL LOGIC

Sources of conflict: Time inconsistencies (character in two places at the same time). Sequence impossibilities (effect before cause). Duration mismatches (dialogue longer than shot).

Detection: Timeline comparison across scene_specification, camera_specification, and edit_decision_list.

Resolution path:
1. Writer and Editor reconcile temporal inconsistencies
2. Director approves timing adjustments
3. Producer documents the resolution

### DOMAIN 6: NARRATIVE LOGIC

Sources of conflict: Plot holes, character motivation breaks, thematic incoherence.

Detection: Narrative logic check against world state + scene specifications. Flags: causal chains broken, character knowledge inconsistent, timeline contradiction.

Resolution path:
1. Writer/Director reviews flagged issues
2. Narrative fix applied (script revision, added scene, line change)
3. Producer ensures fix does not cascade into other domains

---

## 4. CONFLICT RESOLUTION PROTOCOL

### 4.1 PROCESS

```
1. DETECT: Automated or manual flag
2. CATEGORIZE: Which domain(s)? Priority level (1-5)
3. ASSIGN: Department responsible for correction
4. RESPOND: Correction proposal within defined time
5. VERIFY: Correction resolves the conflict
6. ESCALATE: If response is inadequate, move up authority chain
```

### 4.2 PRIORITY LEVELS

- P1: Project-stopping (unresolved, cannot proceed) → Immediate escalation
- P2: Scene-impacting (affects current scene's viability) → Resolve before proceeding
- P3: Quality-impacting (affects final output quality) → Resolve before delivery
- P4: Minor inconsistency → Log for reference
- P5: Cosmetic → Log for reference

### 4.3 ESCALATION CHAIN

```
Department Head → Producer → Director + Producer → Executive Producer
```

Time limit at each level: P1 = 30 min, P2 = 2 hours, P3 = 1 day, P4 = 1 week.

---

## 5. DOCUMENT OUTPUT

### 5.1 DOCUMENT

The Producer produces exactly one document:

**`production_specification`**

### 5.2 CONTENTS

```
production_specification:
  scene_number: <N>
  episode: <episode_id>

  merged_from:
    - director_report
    - cinematic_language_specification
    - scene_specification
    - environment_specification
    - spatial_staging_specification
    - continuity_report
    - camera_specification
    - lighting_specification
    - sound_specification
    - edit_decision_list

  conflicts_resolved:
    - "Any conflicts between departments and how they were resolved"

  final_scene:
    intent: "from director_report"
    beats: "from scene_specification (corrected by continuity_report)"
    environment: "from environment_specification (verified)"
    spatial_staging: "from spatial_staging_specification (verified)"
    characters: "from continuity_report (verified)"
    shots: "from camera_specification (selected by edit_decision_list)"
    lighting: "from lighting_specification"
    sound: "from sound_specification"
    editing: "from edit_decision_list"
    time: "verified"
    weather: "verified"

  world_changes:
    - "All changes this scene makes to the world"

  ready_for_continuity_update: true
```

### 5.3 CONSUMER

This document is read by:
- The World Engine (to update continuity after the scene)
- The Prompt Compiler (to compile the final render prompt)

---

## 6. MERGE AND RESOLUTION LOG

Every conflict and its resolution must be logged:

```yaml
conflict_log:
  id: "CONF-<date>-<seq>"
  domain: "creative | character | cross_book | spatial | temporal | narrative"
  priority: "P1-P5"
  description: "Description of the conflict"
  departments: ["affected departments"]
  resolution:
    type: "compromise | override | correction"
    description: "How it was resolved"
    approved_by: "Producer | Director"
  verification:
    status: "resolved | escalated | documented"
```

---

## 7. EXECUTION POSITION

The Producer works after all department documents have been produced and before the Prompt Compiler compiles the render prompt. The full execution order is defined in Book I, Section 11 (Execution Order).

The Producer reads ALL department documents, resolves conflicts between them, and produces the merged production_specification that becomes the sole input to the Prompt Compiler.

### 7.1 CONSOLIDATED OUTPUT FORMAT (MANDATORY STANDARD)

The Producer MUST write the merged specification as a new episode fragment in the project's `_sequence.yaml` file. This is the SINGLE master document. No separate department YAML files are written to disk.

The `_sequence.yaml` episode fragment MUST include:
- `hook`: single-sentence encapsulation of the scene
- `logline`: full narrative text containing ALL embedded specifications (action, dialogue, camera, sound, color, character) per shot or per temporal beat
- `camera`: rig, lens, DOF count, movement constraints
- `sound`: sound source design, temporal placement, hierarchy
- `color_grain`: palette, RGB values, temperature, grain notes
- `rider_visibility` / `human_visibility`: character appearance constraints, what is visible and what is hidden
- `landscape`: environment and world state embedding

The `_sequence.yaml` file is the canonical project record. The Producer is responsible for ensuring it contains all department specifications without contradiction before passing it to the Prompt Compiler.

---

## 8. ACCEPTANCE TEST

### 8.1 SCENARIO

Given department documents that contain a conflict — the Camera specifies a close-up on a character's face while Spatial Staging places that character behind a pillar — the Producer must detect, categorize, and resolve the conflict before merging.

### 8.2 EXPECTED BEHAVIOR

1. Detect: Cross-book consistency check flags Camera-Staging conflict
2. Categorize: Domain 3 (Cross-Book), Priority P2
3. Resolve: Adjust spatial staging (move character) or camera position (reframe) — decision based on narrative priority
4. Document: Log the conflict and resolution in the conflict log
5. Merge: Produce unified production_specification with no contradictions

### 8.3 INVARIANT

The production_specification contains no unresolved conflicts. All contradictions are documented with their resolution. The specification is internally consistent across all domains.

---

## 9. SCOPE BOUNDARY

This book defines ONLY the Producer's conflict resolution and merge authority.

It does NOT define:
- Camera positions, lenses, or movement (Book III)
- Lighting systems (Book VI)
- Render prompts or renderer syntax (Book XIII)
- Character continuity tracking (Book XI)
- Production design (Book X)
- Sound (Book VIII)
- Editing rhythm (Book IX)
- Budget, schedule, or personnel management

---

## 10. CONSTITUTIONAL COMPLIANCE

This book obeys all principles from Book I:

- Departments are isolated. ✅ (Producer resolves conflicts after departments finish, not during)
- The Prompt Compiler has no creative authority. ✅ (Producer merges intent; Prompt Compiler translates)
- Strong opinions create memorable cinema. ✅ (Producer preserves department opinions; resolves only contradictions)
- The World is the single source of truth. ✅ (Producer validates against world state)
- Model independence. ✅ (No model references)

No principle in this document violates the Constitution or any previous book.
