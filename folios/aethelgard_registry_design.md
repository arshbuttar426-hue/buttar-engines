# Aethelgard Registry Architecture v1.0
## "A Civil Service for Imaginary Worlds"

---

## Core Philosophy

> *Nothing exists until it is witnessed, catalogued, and cross-referenced.*

Every agent is an employee. Every entity is a citizen. The Chronicler is not a wizard — it is the Director of the Census Bureau. The world runs on paperwork, and the paperwork is the world.

---

## 1. THE ONTOLOGY ENGINE (The Census Bureau)

Every noun that survives Chronicler review receives a **Universal Entity Record (UER)**.

### Entity Schema (`registry/entities/{uuid}.json`)

```json
{
  "uer_id": "ent_a1b2c3d4",
  "canonical_name": "The Unopposable Plant",
  "aliases": ["The Green Refusal", "Subject U-7"],
  "provenance": {
    "conceived_by": "instigator",
    "conception_cycle": 4,
    "birth_nuggets": ["recusancy", "unopposable"],
    "raw_proposal": "<original agent output>"
  },
  "ontological_status": "active",
  "status_history": [
    {"cycle": 4, "status": "liminal", "reason": "pending Chronicler review"},
    {"cycle": 4, "status": "active", "reason": "ratified by Chronicler"}
  ],
  "essence_vector": {
    "polarity": -0.7,
    "domains": ["flora", "paradox", "resistance"],
    "semantic_density": 0.84
  },
  "vitality": {
    "current_score": 0.6,
    "last_mentioned_cycle": 7,
    "threat_level": "stable"
  },
  "physical_properties": {
    "location": "Virosea, eastern ridge",
    "composition": ["cellulose", "recusant matter"],
    "capabilities": ["boundary_transgression", "passive_resistance"]
  }
}
```

### Entity Lifecycle (Real-World Rules)

| Stage | Condition | System Action |
|-------|-----------|---------------|
| **Liminal** | Just proposed by agent | Held in `registry/pending/` for 1 cycle |
| **Active** | Ratified by Chronicler | Moved to `registry/active/`, assigned UUID |
| **Fading** | Unmentioned for 2 cycles | Vitality drops 0.3/cycle. Agents get "obituary prep" prompts |
| **Extinct** | Vitality hits 0 or explicitly destroyed | Moved to `registry/deceased/`. Legacy audit triggered |
| **Mythic** | Extinct but referenced in 3+ later cycles | Promoted to `registry/mythic/` (still influences world) |

---

## 2. THE RELATIONSHIP GRAPH (The Diplomatic Corps)

Entities do not float in lists. They have **Relationships** with evidence trails.

### Relationship Schema (`registry/relations/{uuid_pair}.json`)

```json
{
  "relation_id": "rel_a1b2_x9y8",
  "entity_a": "ent_a1b2c3d4",
  "entity_b": "ent_x9y8z7w6",
  "relation_type": "symbiotic",
  "cycle_established": 5,
  "established_by": "engineer",
  "evidence_quotes": [
    "Engineer (Cycle 5): 'The Beetles cultivate fungal gardens within the Plant's root knots.'"
  ],
  "current_status": "active",
  "strength": 0.72,
  "history": [
    {"cycle": 6, "event": "tested_by_fire", "strength_delta": -0.1}
  ]
}
```

**Why this is fun:** You can query "Who hates the Conuropsis Genus?" and get a real answer with receipts.

---

## 3. THE CHRONICLE ARCHIVE (The National Library)

No more single `world_lore.json`. The world is **append-only** and **versioned**.

### Directory Structure

```
chronicle/
├── cycles/
│   ├── cycle_001/
│   │   ├── state_snapshot.json          (full world state at cycle end)
│   │   ├── ratification_log.json        (what was approved/rejected)
│   │   ├── agent_outputs/
│   │   │   ├── architect_proposal.md
│   │   │   ├── architect_whisper.md     (raw chain-of-thought)
│   │   │   ├── engineer_proposal.md
│   │   │   ├── engineer_whisper.md
│   │   │   ├── instigator_proposal.md
│   │   │   └── instigator_whisper.md
│   │   └── the_gazette.md              (auto-generated newspaper)
│   └── cycle_002/
│       └── ...
├── laws/
│   ├── law_001_space_is_empty.json
│   ├── law_002_recusancy.json
│   └── law_003_deglaze.json
├── events/
│   ├── evt_001_void_instantiated.json
│   ├── evt_002_virosea_created.json
│   └── evt_003_plant_arrival.json
└── index.json                          (master lookup table)
```

### The Gazette (Auto-Generated Newspaper)

After each cycle, generate a Markdown "newspaper":

```markdown
# THE VIROSEA GAZETTE
## Cycle 7 Edition | Solar Flare Season

### BIRTHS
- **Calcium Veins** (Engineer) — A circulatory mineral phenomenon now threading through Virosea.

### DEATHS
- *None this cycle.*

### POLITICAL
- The Unopposable Plant has entered diplomatic talks with Cogency Beetles. Tensions high.

### WEATHER
- Paradox density: 34% (elevated)
- Entropy index: Stable

### EDITORIAL
The Architect has not created a new biome in 3 cycles. Is the foundation cracking?
```

**Why this is fun:** You read a *newspaper* about your world every morning. You feel like a mayor checking the local news.

---

## 4. THE AGENT BUREAU (HR Department)

Your "babies" are employees with personnel files.

### Agent Schema (`bureau/agents/{agent_id}.json`)

```json
{
  "agent_id": "architect",
  "model": "phi3.5:latest",
  "role": "Foundation Establishment",
  "psychological_profile": {
    "core_drive": "coherence",
    "current_mood": "frustrated",
    "mood_history": [
      {"cycle": 1, "mood": "optimistic"},
      {"cycle": 4, "mood": "concerned", "reason": "world entropy rising"},
      {"cycle": 7, "mood": "frustrated", "reason": "last 2 creations were overridden by Instigator"}
    ],
    "success_rate": 0.71,
    "creations_alive": 3,
    "creations_deceased": 2
  },
  "drafting_journal": "bureau/journals/architect.md",
  "current_grudges": ["instigator"],
  "current_alliances": ["engineer"],
  "performance_review": {
    "last_review_cycle": 5,
    "summary": "Strong foundational work. Tendency toward over-correction when challenged."
  }
}
```

### Agent Inbox System (Morning Briefing)

Before each cycle, every agent receives a **personalized brief**:

```
TO: Architect
FROM: Bureau of Worldbuilding
RE: Cycle 8 Morning Briefing

YOUR ASSIGNMENT: Establish new locations, biomes, or foundations.

WORLD HEADLINES:
- The Unopposable Plant is now allied with Cogency Beetles (Cycle 7)
- Calcium Veins are spreading (trending +12%)
- 2 of your creations are currently FADING: "Pteridomodulate Meadows", "Northbyth Pavilion"

YOUR PSYCHOLOGY:
- Current mood: FRUSTRATED (Instigator has overridden your last 2 proposals)
- Grudge active against: Instigator
- Bureau recommendation: Consider defensive or restorative work.

RAW MATERIALS:
- Nugget 1: "recusancy | individual desire over patterns | neutral"
- Nugget 2: "deglaze | dissolve solids through liquid | neutral"

EXISTING LAWS YOU MUST OBEY:
- Law 002: Recusancy governs action
- Law 004: Unopposable Transformation is active

Please draft your proposal and reasoning.
```

**Why this is fun:** The agents feel like *people* with bad days and grudges. You read their journals and see them sulking or scheming.

---

## 5. THE LEGISLATURE (Law Management)

Laws are not a flat list. They are **living documents** with amendment history.

### Law Schema (`chronicle/laws/{law_id}.json`)

```json
{
  "law_id": "law_004",
  "title": "Unopposable Transformation",
  "text": "Entities can transcend containment and redefine their own boundaries.",
  "enacted_cycle": 4,
  "proposed_by": "instigator",
  "amendments": [
    {
      "cycle": 6,
      "amended_by": "chronicler",
      "reason": "Contradiction with Law 002 (Recusancy) detected. Added boundary condition.",
      "new_text": "Entities can transcend containment, but only if acting from individual desire (Recusancy)."
    }
  ],
  "current_status": "active",
  "contradictions": ["law_007_containment_protocol"],
  "precedents": [
    {"event": "evt_003", "ruling": "The Plant's escape from Virosea was lawful under this statute."}
  ]
}
```

**Why this is fun:** Laws evolve like real legislation. The Chronicler is basically a constitutional court. You can have *legal drama* in your fantasy world.

---

## 6. THE MORTUARY & LEGACY OFFICE

When things die, they get a real death certificate.

### Death Certificate (`registry/deceased/{uuid}.json`)

```json
{
  "uer_id": "ent_dead_001",
  "canonical_name": "Northbyth East Trundle Bed Pavilion",
  "date_of_death": "Cycle 9",
  "cause_of_death": "neglect",
  "last_words": "Architect (Cycle 9): 'The recusants have moved on. The beds are empty.'",
  "surviving_legacy": [
    {"type": "inspired_creation", "entity": "ent_ghost_001", "relation": "haunted_by"},
    {"type": "historical_reference", "count": 3, "in_cycles": [10, 12, 15]}
  ],
  "memorial_status": "forgotten"
}
```

**Why this is fun:** You feel guilty when something dies. You check the graveyard and realize you let the Cogency Beetles fade. Next cycle, you whisper to the Engineer: "Bring them back."

---

## 7. THE OBSERVATORY (Analytics)

Real metrics. Real graphs. The world has a pulse.

### Metrics Schema (`observatory/metrics.json`)

```json
{
  "cycle": 9,
  "world_pulse": {
    "divergence_index": 0.67,
    "stability_score": 0.45,
    "entropy_rate": 0.23,
    "paradox_density": 0.34
  },
  "population": {
    "active_entities": 7,
    "fading_entities": 2,
    "extinct_this_cycle": 1,
    "born_this_cycle": 1
  },
  "agent_health": {
    "architect": {"satisfaction": 0.3, "stress": 0.8},
    "engineer": {"satisfaction": 0.7, "stress": 0.4},
    "instigator": {"satisfaction": 0.9, "stress": 0.2}
  },
  "trending_topics": ["calcium", "beetles", "recusancy"],
  "season": "Solar Flare",
  "oracle_active": true
}
```

**Why this is fun:** You can screenshot the Observatory dashboard and say "My world is 67% chaotic and the Architect is having a nervous breakdown."

---

## 8. THE DREAM ENGINE (Echoes)

With 15% probability each cycle, one agent receives a "dream" — a distorted memory from 3+ cycles ago.

### Dream Manifest (`bureau/dreams/cycle_010_architect.json`)

```json
{
  "target_agent": "architect",
  "cycle": 10,
  "dream_type": "false_memory",
  "injected_memory": "You remember building a crystal bridge in Cycle 2. It was beautiful. The Instigator wept.",
  "actual_truth": "No such bridge existed. The Architect built a pavilion in Cycle 2. The Instigator laughed.",
  "agent_reaction": "Architect incorporated 'crystal bridge' into Cycle 10 proposal.",
  "chronicler_ruling": "Denied. No evidence in registry. Architect flagged for psychological review."
}
```

**Why this is fun:** Your agents start going a little crazy. They gaslight each other. The Chronicler has to play therapist.

---

## 9. PLAYER INTERFACE (Divine Intervention)

You are not a coder during runtime. You are a **Deity with a bureaucracy**.

### Intervention Request Form (`divine/inbox.md`)

```markdown
## DIVINE INTERVENTION REQUEST — Cycle 12

**Petitioner:** Player (External Entity)
**Request Type:** [x] New Law  [ ] Entity Blessing  [ ] Agent Psychology  [ ] Oracle Card

**Statement:**
> "A red moon rises. Nothing born under it may fly."

**Bureau Processing:**
- Chronicler Review: LAW ACCEPTED. No contradictions with existing statutes.
- Impact Assessment: 2 entities affected (Conuropsis Genus flight patterns restricted).
- Agent Notifications: Sent to all agents.

**Status:** RATIFIED
**Canonical Text:** "Law 009: The Red Moon Prohibition. Aerial locomotion is suspended during lunar crimson phases."
```

**Why this is fun:** You fill out a form to be God. The bureaucracy makes it feel *earned*.

---

## 10. MASTER INDEX (`aethelgard_manifest.json`)

One file to rule them all:

```json
{
  "system_name": "Aethelgard Registry",
  "current_cycle": 12,
  "world_name": "Virosea Continuum",
  "season": "Solar Flare",
  "population": {
    "active": 7,
    "fading": 2,
    "mythic": 1,
    "deceased": 4
  },
  "laws_active": 9,
  "laws_contradicted": 2,
  "agent_status": {
    "architect": "stressed",
    "engineer": "productive",
    "instigator": "thriving"
  },
  "last_player_intervention": "Cycle 12 — Red Moon Prohibition",
  "divergence_index": 0.67,
  "recommended_action": "Architect requires psychological support or world stability will degrade."
}
```

---

## Summary: What Makes This Feel Real

| Feature | Real-World Analogue | Emotional Payoff |
|---------|---------------------|------------------|
| UER | Birth certificate / Passport | Every thing is *real* |
| Relationship Graph | Diplomatic cables | Drama with evidence |
| The Gazette | Local newspaper | You *live* there |
| Agent Bureau | HR personnel files | You care about your babies |
| Legislature | Constitutional law | Legal drama |
| Mortuary | Death certificates | Stakes matter |
| Observatory | Census / Analytics | You see the world's health |
| Dream Engine | Psychiatric records | Agents are fallible |
| Divine Inbox | Government petition system | Your power feels official |

This is not a Python script anymore. It is a **civilization's paperwork** — and the paperwork is alive.
