Copyright © 2026 Arsh Buttar. All rights reserved. Confidential and proprietary.
Unauthorized copying, distribution, or use of this work is prohibited.

# CINEMA SKILL — BOOK II: THE WORLD

> This document extends Book I: The Constitution.
> Everything written here obeys the Constitution.
> No principle in this document may violate Book I.
> This document defines the permanent memory architecture of Cinema.

---

## 1. THE WORLD ENGINE

The World Engine is the permanent memory of every film project.

The World Engine owns reality.

The World Engine is NOT responsible for prompts.
The World Engine is NOT responsible for cameras.
The World Engine is NOT responsible for rendering.

Every department reads from the World.
Every department writes back to the World.

The World is the single source of truth.
No department may maintain its own private continuity.

---

## 2. FUNDAMENTAL PRINCIPLE

Nothing exists unless it exists inside the World.

Characters live in the World.
Props live in the World.
Buildings live in the World.
Time lives in the World.
Weather lives in the World.
Damage lives in the World.
Relationships live in the World.

If it is not in the World, it does not exist in the story.

---

## 3. WORLD STORAGE STRUCTURE

Each project contains a `world/` directory. This is the World Engine's storage.

```
<project>/
├── (story files, sequence plans, backstory)
└── world/
    ├── world_state.yaml          ← current state snapshot (the present moment)
    ├── timeline.yaml             ← chronological event log (the past)
    ├── relationships.yaml        ← character relationship graph
    ├── memory.yaml               ← important remembered facts
    ├── locations/
    │   └── <location_id>.yaml    ← per-location persistent state
    ├── props/
    │   └── <prop_id>.yaml        ← per-prop persistent state
    ├── characters/
    │   └── <character_id>.yaml   ← per-character live state (separate from character definition)
    └── continuity/
        └── scene_<N>.yaml        ← per-scene continuity snapshot
```

### Separation of Definition and State

A character's DEFINITION lives in the global `characters/` directory.
A character's LIVE STATE lives in the project's `world/characters/` directory.

- Definition = who the character IS (permanent identity, appearance, personality).
- Live State = where the character IS RIGHT NOW (location, wardrobe, emotional state, inventory, knowledge).

Definitions do not change during a story.
Live State changes after every scene.

The same separation applies to locations and props:
- A location's definition describes its architecture and base state.
- A location's live state describes its current damage, occupancy, weather effects, time of day.

---

## 4. ENTITY OWNERSHIP

### 4.1 PROJECT

A project is the top-level container. It owns everything below it.

```
Project
  ↓
  Characters (definitions + live states)
  Locations (definitions + live states)
  Props (registry + live states)
  Episodes
  Scenes
  World State
  Continuity
  Timeline
  Memory
  Relationships
```

### 4.2 EPISODES

An episode is a narrative unit containing one or more scenes.

An episode owns:
- Its episode number
- Its title
- Its narrative purpose
- The scenes within it
- Its position in the sequence

### 4.3 SCENES

A scene is the smallest narrative unit the user can produce.

A scene owns:
- Its scene number
- Its episode assignment
- Its duration
- Its setting (location + time + weather)
- The characters present
- The actions that occur
- The dialogue spoken
- The changes to the world (what is different after this scene)

Every completed scene writes a continuity snapshot to `world/continuity/scene_<N>.yaml`.

### 4.4 CHARACTERS

A character is a persistent entity — NOT simply a prompt.

#### Character Definition (permanent, in `characters/`)

Owned by the character file. Does not change during story:
- Identity (name, species, breed, role)
- Appearance (fur, eyes, build, distinguishing features)
- Personality (archetype, traits, likes, dislikes, quirks, fears)
- Speech patterns (voice style, catchphrases, sounds)
- Scale (dimensions, proportions, screen presence)
- 3D model specifications (materials, rig, blendshapes)

#### Character Live State (changing, in `world/characters/`)

Owned by the World Engine. Updated after every scene:
- Current location (which location the character is in)
- Current wardrobe (what they are wearing, if applicable)
- Physical state (health, injuries, fatigue, wetness, dirt)
- Emotional state (current mood, intensity)
- Knowledge (what the character knows — facts learned, secrets known)
- Current objective (what the character wants right now)
- Inventory (what the character is carrying)
- History (log of significant events experienced)
- Visible changes (damage, scars, wardrobe changes, fur condition)
- Invisible changes (fears acquired, trust gained or lost, emotional growth)

The user never edits these. Cinema updates them.

### 4.5 LOCATIONS

Locations are persistent. A location remembers:
- Architecture (physical structure, layout, dimensions)
- Objects present (props fixed to this location)
- Lighting conditions (ambient light character, not the lighting department's choices)
- Time of day (current)
- Damage (structural changes, wear, stains)
- Occupancy (who is currently here)
- Weather effects (wetness, snow, leaves, debris)
- History (significant events that occurred here)

Nothing resets automatically. If a window was broken in scene 3, it is still broken in scene 7.

### 4.6 PROPS

Every important prop has identity.

A prop owns:
- Unique ID
- Name
- Description
- Current location (which location or character holds it)
- State (intact, damaged, consumed, lost)
- History (where it has been, who has held it)
- Introduced in (which scene it first appeared)

The same prop remains the same object throughout the story.

Example: Biscuit's red leather collar with brass bone tag.
- It exists from the beginning.
- It gets wet in the rain.
- It gets cracked and tarnished.
- It persists until explicitly removed.

A samosa is consumed. Once consumed, its state becomes `consumed` and it no longer exists in the world as an active prop.

### 4.7 VEHICLES

Vehicles are specialized props that can move characters.
- Identity, current location, condition, occupancy, fuel/state.

### 4.8 ANIMALS

Non-character animals (background wildlife, other dogs, cats).
- Species, current location, behavior state, relationship to characters.

### 4.9 ENVIRONMENT

The environment is the ambient world state:
- Season
- Temperature
- Air quality (smoke, mist, clear)
- Ground condition (dry, wet, muddy, snow-covered)
- Vegetation state (green, autumn, bare)

### 4.10 WEATHER

Weather is tracked independently:
- Current weather condition
- Intensity
- Direction (wind, rain direction)
- Duration (how long it has been this way)
- Transition (is it clearing, worsening, stable?)

Weather does not randomly change. It changes only when the story or time advancement requires it.

### 4.11 TIME

Time always advances.
- Current date (within the story's timeline)
- Current time of day
- Elapsed time since previous scene
- Time of year (season, festival period)

Time is never ambiguous. The World always knows what time it is.

### 4.12 RELATIONSHIPS

Relationships are tracked in `world/relationships.yaml`:
- Character A → Character B
- Relationship type (family, friend, rival, stranger, enemy)
- Strength (0-10)
- Current emotional valence (positive, negative, mixed)
- History of significant relationship events

Relationships change based on what happens in scenes. If Scraps protects Biscuit in a scene, the relationship strength increases.

### 4.13 TIMELINE

The timeline is a chronological log of significant events.
- Event timestamp (story time)
- Event description
- Characters involved
- Locations involved
- Consequences

Every significant story event is logged. This is the World's long-term memory.

### 4.14 MEMORY

The World remembers everything important in `world/memory.yaml`:
- Facts the World should not forget
- Character-specific knowledge
- World-altering decisions
- Off-screen events that affect on-screen reality

The user should never remind Cinema. Cinema should remember.

---

## 5. WORLD STATE

The `world_state.yaml` file is the current snapshot of the world — the present moment.

It always knows:

```
world_state:
  current_episode: S05
  current_scene: 3
  current_time: "dawn, 5:45 AM"
  current_date: "Day 2 of the story"
  current_weather: "light drizzle, clearing"
  current_season: "late monsoon"
  
  characters:
    biscuit:
      location: "wet_street_near_chai_stall"
      wardrobe: "red_leather_collar (cracked, tarnished)"
      physical_state: "tired, slightly wet, ribs visible"
      emotional_state: "cautious optimism, intensity 3"
      knowledge: ["Scraps is his friend", "Mrs. Sharma is gone", "this street is home"]
      current_objective: "find breakfast"
      inventory: []
    scraps:
      location: "wet_street_near_chai_stall"
      wardrobe: "no collar"
      physical_state: "alert, dry under van"
      emotional_state: "protective, mild annoyance, intensity 2"
      knowledge: ["Biscuit is helpless", "the chai wala gives food", "this is their territory"]
      current_objective: "keep Biscuit safe"
      inventory: []
  
  locations_active:
    wet_street_near_chai_stall:
      time_of_day: "dawn"
      weather_effects: "wet pavement, puddles, dripping"
      occupancy: ["biscuit", "scraps"]
      damage: "none new"
  
  props_active:
    red_collar:
      state: "worn"
      holder: "biscuit"
      condition: "cracked leather, tarnished brass"
  
  props_consumed: []
  
  doors:
    chai_stall_shutter: "closed"
  windows:
    none_tracked
  environment:
    ground: "wet"
    air: "misty, rain smell"
    vegetation: "n/a (urban)"
```

Nothing should disappear unless explicitly removed.

---

## 6. CONTINUITY PROTOCOL

### 6.1 INHERITANCE

Every new scene inherits the world exactly as the previous scene left it.

Before producing a scene, Cinema reads:
1. `world_state.yaml` (current state)
2. `world/characters/*.yaml` (all character live states)
3. `world/continuity/scene_<previous>.yaml` (previous scene snapshot)
4. `world/relationships.yaml` (current relationships)
5. `world/memory.yaml` (remembered facts)

### 6.2 RULES

- Characters do not magically heal.
- Objects do not teleport.
- Weather does not randomly change.
- Time always advances.
- Damage persists.
- Wardrobe changes only when explicitly changed.
- Knowledge only grows — characters do not forget unless the story requires it.
- Consumed props stay consumed.
- Broken objects stay broken.

### 6.3 UPDATE

After every completed scene:

1. Cinema writes a continuity snapshot to `world/continuity/scene_<N>.yaml`.
2. Cinema updates `world_state.yaml` to reflect all changes.
3. Cinema updates each character's live state in `world/characters/`.
4. Cinema updates `world/timeline.yaml` with significant events.
5. Cinema updates `world/relationships.yaml` if relationships changed.
6. Cinema updates `world/memory.yaml` if important facts were established.
7. Cinema updates location states if locations changed.
8. Cinema updates prop states if props changed.

This happens silently. The user is never asked to do this. The user is never told it happened.

---

## 7. DOCUMENT COMMUNICATION ARCHITECTURE

### 7.1 PRINCIPLE

Every department must communicate through documents.
No department communicates directly.

A department produces a document.
The next department reads the previous document.
No verbal handoffs. No implicit understanding. Only documents.

### 7.2 DOCUMENT FLOW

The execution order is defined in Book I, Section 11 (Execution Order). The document flow below shows how documents are produced and consumed through that sequence:

```
Director (Book V)                      → director_report      ┐
Cinematic Language (Book IV)           → cinematic_language   │
Writer                                 → scene_specification  │
Production Designer (Book X)           → environment_spec     ├─→ _sequence.yaml
Spatial Staging (Book VII)             → spatial_staging_spec │   (consolidated)
Character Supervisor (Book XI)         → continuity_report    │
Camera (Book III)                      → camera_specification │
Lighting (Book VI)                     → lighting_specification│
Sound (Book VIII)                      → sound_specification  │
Editor (Book IX)                       → edit_decision_list   ┘
Producer (Book XII)                    → production_specification
                                           └→ _sequence.yaml (episode fragment)
Prompt Compiler (Book XIII)            → render_prompt
                                           └→ R###_<name>_prompt.md
```

Each department reads the documents produced by all previous departments and produces its own document internally. The specific inputs for each department are defined in that department's book.

**However, the STANDARD DELIVERABLE FORMAT is consolidated.** All department outputs are merged by the Producer into the `_sequence.yaml` file — a single master sequence document containing all specifications within its episode fragments. Individual department YAML files are NOT written to disk. The `_sequence.yaml` is the single source of truth for all specifications.

The Prompt Compiler additionally produces `R###_<name>_prompt.md` — a standalone render-ready prompt file derived from the `_sequence.yaml` fragment.

This consolidated format is MANDATORY. No separate department files are permitted in the project directory.

### 7.3 DOCUMENT DEFINITIONS

#### director_report

Produced by: Director
Consumed by: Writer

```
director_report:
  scene_number: <N>
  episode: <episode_id>
  
  intent: >
    What this scene is about at its core.
  
  emotion: >
    What the audience should feel.
  
  narrative_purpose: >
    What this beat accomplishes in the story.
  
  what_changes: >
    What is different by the end of this scene.
  
  director_notes: >
    Any thematic or tonal guidance (not dialogue, not camera, not lighting).
```

#### scene_specification

Produced by: Writer
Consumed by: Production Designer, Character Supervisor

```
scene_specification:
  scene_number: <N>
  episode: <episode_id>
  
  beats:
    - beat_number: 1
      time_range: "0:00 - 0:02"
      action: "What happens"
      dialogue:
        speaker: "Character"
        text: "Dialogue in project language"
      emotion: "What the character feels"
    
    - beat_number: 2
      ...
  
  characters_present: ["biscuit", "scraps"]
  
  connection_to_previous: >
    How this scene connects to the last scene.
  
  setup_for_next: >
    How this scene sets up the next.
  
  new_information_established:
    - "Any facts the audience or characters learn"
```

#### environment_specification

Produced by: Production Designer
Consumed by: Character Supervisor, Producer

```
environment_specification:
  scene_number: <N>
  
  location: <location_id>
  location_description: "Where this takes place"
  
  time_of_day: "specific time"
  weather: "current weather"
  season: "current season"
  
  objects_present:
    - object_id: "description and position"
  
  new_objects_introduced:
    - object_id: "description"
  
  changes_from_previous_scene:
    - "What has changed in the environment since last scene"
  
  atmosphere: >
    The physical feeling of the space.
```

#### spatial_staging_specification

Produced by: Spatial Staging
Consumed by: Character Supervisor, Camera, Lighting, Producer

```
spatial_staging_specification:
  scene_number: <N>
  
  environment_affordances:
    - affordance_id: "<unique_id>"
      type: "step | wall | corner | open_space | edge | pillar | threshold | elevated | enclosed | narrow_passage"
      location: "position in environment"
      claimed_by: "<character_id or null>"
      narrative_reason: "why this character claims this affordance"
  
  staging:
    formation:
      initial_type: "circle | v-formation | cluster | scatter | stacked | threshold"
      final_type: "same or different"
    
    characters:
      - character_id: "<character_id>"
        initial_position:
          location: "where in the environment"
          elevation: "relative height description"
          facing: "body and head orientation"
          territory: "center | edge | corner | threshold | between"
          proximity_to: "<character_id> at <distance>"
        final_position: "..."
        sightlines:
          can_see: ["what the character can see"]
          cannot_see: ["what the character cannot see"]
        blocking:
          - trigger: "what causes movement"
            path: "trajectory"
            speed: "slow | moderate | fast"
            target: "character | position | exit"
  
  flags_for_camera:
    - "Spatial elements Camera must account for"
```

#### continuity_report

Produced by: Character Supervisor
Consumed by: Producer

```
continuity_report:
  scene_number: <N>
  
  character_states:
    biscuit:
      appearance_verified: true
      wardrobe: "red collar, cracked"
      physical_state: "as expected from world state"
      emotional_state: "consistent with previous scene"
      continuity_flags: []
    
    scraps:
      appearance_verified: true
      wardrobe: "none"
      physical_state: "as expected"
      emotional_state: "consistent"
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

#### production_specification

Produced by: Producer
Consumed by: (Future: Prompt Compiler, and future-book departments)

```
production_specification:
  scene_number: <N>
  episode: <episode_id>
  
  merged_from:
    - director_report
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

### 7.4 COMPLETE DOCUMENT FLOW

All books are now defined. The document flow is complete:
- `director_report` (Director, Book V)
- `cinematic_language_specification` (Cinematic Language, Book IV)
- `scene_specification` (Writer)
- `environment_specification` (Production Designer)
- `spatial_staging_specification` (Spatial Staging, Book VII)
- `continuity_report` (Character Supervisor)
- `camera_specification` (Camera, Book III)
- `lighting_specification` (Lighting, Book VI)
- `sound_specification` (Sound, Book VIII)
- `edit_decision_list` (Editor, Book IX)
- `production_specification` (Producer)
- `render_prompt` (Prompt Compiler, Book XIII)

### 7.5 SCHEMA OWNERSHIP

Each document's full schema is defined in its producing department's book:
- `director_report` → Book V (Director)
- `cinematic_language_specification` → Book IV (Cinematic Language)
- `scene_specification` → Book II (Writer, this book)
- `environment_specification` → Book X (Production Designer)
- `spatial_staging_specification` → Book VII (Spatial Staging)
- `continuity_report` → Book XI (Character Supervisor)
- `camera_specification` → Book III (Camera)
- `lighting_specification` → Book VI (Lighting)
- `sound_specification` → Book VIII (Sound)
- `edit_decision_list` → Book IX (Editor)
- `production_specification` → Book XII (Producer)
- `render_prompt` → Book XIII (Prompt Compiler)

The World Engine does not define these schemas. It only defines the communication architecture that routes them.

### 7.6 CONFLICT RESOLUTION PROTOCOL

The World Engine does NOT resolve conflicts between departments. That responsibility belongs to the Producer (Book XII).

However, the World Engine provides the ground truth that the Producer uses for resolution:

1. **World State is authoritative.** When two departments disagree about world conditions (weather, time, character location), the World Engine's `world_state.yaml` is the single source of truth.
2. **Changes must be declared.** Any department that changes the world must declare the change in its document. The Producer uses these declarations to compute the delta.
3. **The World Engine validates post-production.** After the Producer merges, the World Engine validates that the merged `production_specification` makes no impossible claims (e.g., a character in two places simultaneously, a consumed prop still active).

The 6-domain conflict detection system is defined in Book XII, Section 2.

---

## 8. MEMORY SYSTEM

### 8.1 WHAT THE WORLD REMEMBERS

The World remembers:
1. **Timeline** — every significant event in chronological order
2. **Character knowledge** — what each character knows (separate from what the audience knows)
3. **Relationships** — how characters feel about each other and how that has changed
4. **Prop history** — where every prop has been and what has happened to it
5. **Location history** — what events have occurred in each location
6. **World facts** — anything established as true in the story world

### 8.2 MEMORY ACCESS

When Cinema loads a project, it reads:
- `world/memory.yaml` — persistent facts
- `world/timeline.yaml` — event history
- `world/relationships.yaml` — relationship graph
- All character live states

When a department needs to know something, it reads from the World.
Departments do not maintain their own memory.
The World is the only memory.

### 8.3 MEMORY WRITES

After each scene, Cinema writes:
- New events to `timeline.yaml`
- New facts to `memory.yaml`
- Relationship changes to `relationships.yaml`
- Character knowledge updates to character live states

The user should never remind Cinema. Cinema should remember.

---

## 9. WORLD ENGINE INITIALIZATION

When Cinema loads a project for the first time (no `world/` directory exists):

1. Cinema reads all character definitions from `characters/`.
2. Cinema reads the backstory file (if present) to establish initial world state.
3. Cinema reads all existing scene files to reconstruct what has happened.
4. Cinema creates the `world/` directory structure.
5. Cinema creates initial `world_state.yaml` based on the latest scene.
6. Cinema creates character live states from the latest scene's ending state.
7. Cinema creates `timeline.yaml` from the events of all existing scenes.
8. Cinema creates `relationships.yaml` from the backstory and scenes.
9. Cinema creates `memory.yaml` from established facts.
10. Cinema creates location and prop states from scene history.

This happens silently. The user is never asked to participate in initialization.

If the project has no scenes yet, Cinema initializes the world from the backstory's starting point.

---

## 10. ACCEPTANCE TEST

The following scenario must work conceptually:

```
User types: /cinema
Cinema activates.

Project: Biscuit
Cinema loads the project.

Cinema reads:
  - characters/biscuit.yaml (definition)
  - characters/scraps.yaml (definition)
  - storylines/biscuit/world/world_state.yaml (current state)
  - storylines/biscuit/world/characters/biscuit_state.yaml (live state)
  - storylines/biscuit/world/characters/scraps_state.yaml (live state)
  - storylines/biscuit/world/memory.yaml (remembered facts)
  - storylines/biscuit/world/timeline.yaml (event history)
  - storylines/biscuit/world/relationships.yaml (relationships)
  - All previous scene files (S01-S04, rainy-shift)

Cinema asks: "What happens next?"

User: "Biscuit notices a little girl eating a samosa."

Without asking further questions, Cinema already knows:

WHO BISCUIT IS:
  → From character definition: golden-tan corgi mix, stubby legs, floppy right ear, red collar.

WHAT HE LOOKS LIKE:
  → From character definition + live state: fur condition, current damage, current wardrobe.

WHERE HE CURRENTLY IS:
  → From world_state.yaml → characters.biscuit.location

WHAT HE WEARS:
  → From world_state.yaml → characters.biscuit.wardrobe

WHO ELSE IS NEARBY:
  → From world_state.yaml → locations_active.<location>.occupancy

WHAT HAPPENED PREVIOUSLY:
  → From timeline.yaml → most recent events
  → From the latest scene file

WHAT TIME IT IS:
  → From world_state.yaml → current_time

WHAT WEATHER EXISTS:
  → From world_state.yaml → current_weather

WHICH PROPS EXIST:
  → From world_state.yaml → props_active

WHICH PROPS HAVE BEEN CONSUMED:
  → From world_state.yaml → props_consumed

WHAT EMOTIONAL STATE BISCUIT HAS:
  → From world_state.yaml → characters.biscuit.emotional_state

The World provides this automatically.
The user provides only the story beat.
Cinema handles everything else.
```

---

## 11. SCOPE BOUNDARY

This book defines ONLY the World Engine and document communication architecture.

It does NOT define:
- Cameras or cinematography
- Lighting systems
- Renderer prompts
- Plugin systems
- Veo integrations
- Shot lists
- Lighting specifications
- Sound specifications
- Edit decision lists
- Render prompts

Those belong to future books.

---

## 12. CONSTITUTIONAL COMPLIANCE

This book complies with all applicable principles from Book I: user never edits internal files, continuity is automatic, Cinema owns every project, nothing resets automatically, departments are isolated, the Prompt Compiler has no creative authority, model independence, and execution order is preserved. No principle in this document violates the Constitution.
