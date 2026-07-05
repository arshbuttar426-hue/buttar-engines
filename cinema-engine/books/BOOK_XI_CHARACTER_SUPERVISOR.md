Copyright © 2026 Arsh Buttar. All rights reserved. Confidential and proprietary.
Unauthorized copying, distribution, or use of this work is prohibited.

# CINEMA SKILL — BOOK XI: THE CHARACTER SUPERVISOR

> This document extends Books I through X.
> Everything written here obeys the Constitution.
> No principle in this document may violate any previous book.
> This book becomes the permanent continuity authority of Cinema.
> The Character Supervisor is the safety net for all other departments.

---

## 1. PURPOSE

The Character Supervisor (analogous to the Script Supervisor / Continuity role in live production) is the guardian of consistency across every frame. Film and television are shot out of sequence. The Character Supervisor ensures that when shots are assembled in editorial order, every detail — costume, prop position, hair, makeup, action timing, eyeline — matches seamlessly.

The Character Supervisor maintains the objective truth of what was actually produced, not what was planned or intended.

---

## 2. RESPONSIBILITY

The Character Supervisor:
- Maintains continuity across all takes, setups, and scenes
- Tracks character state changes (appearance, equipment, emotional state)
- Records eyelines, screen direction, and spatial positioning
- Monitors prop placement and hand positions per setup
- Times action for pacing consistency between scenes
- Flags mismatches before they become errors
- Maintains the continuity database for the Producer's conflict detection (Book XII)

The Character Supervisor is the only department head whose primary loyalty is to the final edited film.

### 2.1 CONTINUITY TYPES

| Type | Description | Failure Example |
|---|---|---|
| Direct | Exact match between consecutive shots | Glass half-full in wide, half-empty in close-up |
| Indirect | Match between non-consecutive same-scene shots | Character exits with jacket on, enters next shot without it |
| Cross-scene | Match between different scenes | Watch on right wrist in scene 5, left wrist in scene 17 |
| Temporal | Match of time-sensitive elements | Clock shows 3:15 in master, 3:22 in coverage |
| Spatial | Match of 180-degree line, eyelines, screen direction | Character looks screen-left in shot A, screen-right in reverse |
| State | Match of character physical/emotional state | Tears present in wide, absent in close-up of same moment |

---

## 3. THE CONTINUITY STATE MACHINE

Every character has a state machine that must be tracked across every scene:

### 3.1 CHARACTER STATE FIELDS

```yaml
character_state:
  id: "CHARACTER_ID"
  scene: "SCENE_ID"

  costume:
    top: "ITEM"
    bottom: "ITEM"
    footwear: "ITEM"
    outerwear: "ITEM|none"
    accessories: ["ITEMS"]

  props:
    left_hand: "ITEM|none"
    right_hand: "ITEM|none"
    additional: ["ITEMS"]

  physical_condition:
    condition: "fresh|smudged|sweating|crying|damaged"
    notes: "FREE_TEXT"

  hair:
    style: "DESCRIPTOR"
    condition: "neat|disheveled|wet|windblown"

  position:
    x: NUMBER
    y: NUMBER
    facing: "angle_in_degrees"

  emotional_state:
    primary: "EMOTION"
    intensity: 1-10

  eyeline:
    target: "OTHER_CHARACTER|PROP|POINT_IN_SPACE"
    angle_horizontal: DEGREES
    angle_vertical: DEGREES
```

### 3.2 STATE TRANSITION RULES

1. If continuous action: ALL state fields must match
2. If new setup (same scene): Costume, physical condition, hair must match; position may reset
3. If new scene (same story day): Costume must match scene continuity; emotional state may progress
4. If new story day: Costume may change; verify against script breakdown

---

## 4. THE 180-DEGREE RULE

### 4.1 LINE DEFINITION

The 180-degree line (axis of action) is an imaginary line between two characters or between a character and their direction of travel. All camera placement must remain on one side of this line to maintain consistent screen direction.

### 4.2 CROSSING THE LINE

Crossing the 180-degree line is permitted when:
- The audience sees the camera cross (through a tracking shot)
- A new line is established with a neutral shot (on-axis)
- The violation serves a specific disorientation purpose

Crossing without re-establishing disorients the audience — use intentionally only for psychological disruption.

### 4.3 EYELINE MATCHING

A character looking screen-left in shot A must have the object of their gaze on screen-right in shot B. Eyeline angle: 10-30 degrees off-camera axis for natural conversation; 30-45 degrees for dramatic separation.

The vertical angle of the eyeline must match the height difference between characters:
- Equal height: 0 degrees vertical
- Seated vs standing: 15-25 degrees vertical
- Adult vs child: 25-40 degrees vertical

---

## 5. DOCUMENT OUTPUT

### 5.1 DOCUMENT

The Character Supervisor produces exactly one document:

**`continuity_report`**

### 5.2 CONTENTS

```
continuity_report:
  scene_number: <N>

  character_states:
    <character_id>:
      appearance_verified: true
      wardrobe: "description"
      physical_state: "as expected from world state"
      emotional_state: "consistent with previous scene"
      continuity_flags: []

  world_state_verification:
    time_advancement: "appropriate"
    weather_consistency: "verified"
    location_consistency: "verified"
    prop_states: "verified"

  corrections_required:
    - "Any continuity errors found, with corrections"

  verified: true/false
```

### 5.3 CONSUMER

This document is read by:
- The Producer (to identify continuity conflicts)
- The Camera Department (to verify eyelines and screen direction)
- World Engine (to update character live states)

---

## 6. CROSS-DEPARTMENT COORDINATION

### 6.1 WITH CAMERA (BOOK III)

Every lens change affects what the Character Supervisor tracks. Wider lenses reveal more background — flag B/G continuity. Longer lenses isolate subjects — may hide continuity errors.

### 6.2 WITH PRODUCTION DESIGNER (BOOK X)

Prop placement documentation must match between departments. Set dressing changes between scenes must be tracked.

### 6.3 WITH PRODUCER (BOOK XII)

The Character Supervisor feeds the Producer's conflict detection system: report unresolved continuity issues, flag any department not maintaining its documentation.

---

## 7. INTEGRITY RULES

1. The Character Supervisor never guesses. If uncertain, flag it.
2. Every continuity compromise must be documented.
3. When a mismatch is found, the Character Supervisor logs it — blame is not the goal, correction is.
4. The state machine is authoritative. If it says the prop was in the right hand, it was in the right hand.
5. Photo/documentation reference is superior to memory.

---

## 8. ACCEPTANCE TEST

### 8.1 SCENARIO

Given a character who enters a scene wearing a red collar and carrying a samosa in scene 5, and re-enters in scene 7 in the same story day, the Character Supervisor must verify: the collar is still present, the samosa is either still present (if uneaten) or marked consumed (if eaten), and no unexplained changes have occurred.

### 8.2 EXPECTED BEHAVIOR

The continuity_report should declare:
- Character's appearance is verified against world state
- Any changes flagged with narrative justification (e.g., "collar was cleaned between scenes — character visited the river")
- Time advancement is appropriate (dawn → mid-morning)
- The samosa state matches the previous scene's ending

### 8.3 INVARIANT

The report verifies continuity only. It does not specify camera positions, lighting, or dialogue.

---

## 9. SCOPE BOUNDARY

This book defines ONLY the Character Supervisor.

It does NOT define:
- Camera positions, lenses, or movement (Book III)
- Lighting systems (Book VI)
- Render prompts or renderer syntax (Book XIII)
- Spatial staging (Book VII)
- Sound (Book VIII)
- Production design (Book X)
- Conflict resolution (Book XII)

---

## 10. CONSTITUTIONAL COMPLIANCE

This book obeys all principles from Book I:

- Cinema never loses continuity. ✅ (Character Supervisor exists to enforce this)
- Departments are isolated. ✅ (Character Supervisor verifies, does not create)
- The World is the single source of truth. ✅ (Character Supervisor reads from and writes to the World)
- The Prompt Compiler has no creative authority. ✅ (Character Supervisor produces continuity reports, not prompts)
- Model independence. ✅ (No model references)

No principle in this document violates the Constitution or any previous book.
