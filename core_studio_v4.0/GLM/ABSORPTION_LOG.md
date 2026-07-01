# GLM v3.7.2 — Absorption Log

This document records what was absorbed into `glm_v37_grown.py` from legacy
UBP/GLM files, what was rejected, and what needs data work.

**Working copy**: `glm_v37_grown.py` (experimental — grows from `glm_v37_unified.py`)
**Baseline reference**: `glm_v37_unified.py` (v3.7.1, preserved unchanged)
**Test protocol**: After each absorption, run 12 self-tests (must be 12/12) + gold-set benchmark (must have 0 regressions).

---

## Absorption 1: Lattice-based CRG auto-linking — KEPT

**Source**: `glm_concept_relation_graph.py` → `LatticeConceptLinker.auto_link()`

**What it does**: Links any two NOUNs that are Hamming-adjacent (≤4) AND share the same dominant zone. Adds `lattice_adjacent_N` edges (symmetric).

**Difference from glm_v37's existing `auto_expand_crg`**: The existing function requires a *shared CRG neighbour* (conservative — only links nouns already indirectly connected). This absorption links *any* within-zone adjacent pair (aggressive — discovers new connections).

**Optimization applied**: Zone-bucketing first, so we only compare within-zone pairs. For 2,338 words across ~24 zones, this is ~120K comparisons vs 2.7M brute force. Capped at 50 edges per zone to prevent runaway growth.

**Result**:
- 12/12 self-tests PASS
- CRG edges: 277 → 427 (+150 lattice links)
- Test G (maturation): 18 → 20 inferred nouns (lattice links give the ticker more to follow)
- Gold-set: 9/28 (no change), 0 regressions
- Boot time: +123ms (3072ms → 3195ms)

**Sample lattice edges discovered**:
- complexity ↔ difference (weight 4)
- complexity ↔ emergence (weight 3)
- complexity ↔ equivalence (weight 4)

**Decision**: KEPT. Discovers genuine semantic relationships. Small boot cost is acceptable.

---

## Absorption 2: Reflexive recall — KEPT

**Source**: `auto_trigger.py` → `reflexive_recall()`

**What it does**: Before composing a response, scans the query for:
1. Direct UBP ID matches (regex `XXX_XXX_NNN`)
2. Full KB name phrases found in the query
3. Token matches (query word found in KB name) — broader coverage

Returns up to 3 relevant KB entries, displayed as `[recall] N KB match: ...` in the response.

**Improvement over original**: The original `auto_trigger.reflexive_recall` only did ID + full-phrase match. I added token match (step 3) because KB names are descriptive phrases like "the law of leech surface tension" — users rarely type that exact phrase, but they do type "leech". Token match catches these cases.

**Result**:
- 12/12 self-tests PASS
- Gold-set: 9/28 (no change), 0 regressions
- Recall now fires correctly:
  - "Tell me about the Leech lattice" → 3 entries (Law of Lattice Activation, Law of Leech Surface Tension, Law of the Leech Generator)
  - "What is monstrous moonshine?" → 1 entry (Law of Monstrous Moonshine)
  - "Explain the Golay code" → 3 entries (Golay Drag Coefficient ×2, Law of the Golay Engine)

**Decision**: KEPT. Gives the response composer more context to work with. Will become more valuable as the KB grows.

---

## Absorption 3: Gap-filling vector derivation — KEPT (scaffolding, needs data)

**Source**: `glm_physics_vocab_pack.py` → `derive_term_vector()`

**What it does**: When a query has unknown words (gaps), derives a 24-bit vector for each using the deterministic `derive_term_vector()` function, then Hamming-verifies it against existing vocab. If the nearest anchor is within distance 8, adds the word to the vocab. Otherwise leaves it as a gap (safety: don't insert ungrounded vectors).

**Result**:
- 12/12 self-tests PASS
- Gold-set: 9/28 (no change), 0 regressions
- **Derivation attempted but rejected for basic math terms**: "integers" and "divisible" both derived vectors but were rejected (nearest anchor >8 Hamming distance away)

**Why it didn't improve accuracy (yet)**: The `derive_term_vector` function uses `I_Topology` as the default MOG category for math terms. But the existing vocab's math-adjacent words may be in different categories (M_Count, P_Ratio, etc.), so the derived vectors land too far away. The Hamming safety check correctly rejects them.

**What needs to happen for this to help**: Either (a) assign MOG categories more intelligently based on the word (e.g. "integers" → M_Count, "divisible" → P_Ratio), or (b) grow the KB with more math terms so there are closer anchors. Both are data work — the user's responsibility per the task brief.

**Decision**: KEPT as scaffolding. The code is correct and safe. It will start helping once the KB has better math coverage. The `_derived_cache` prevents re-deriving the same word across turns.

---

## Absorption 4: Enhanced query-type detection — KEPT

**Source**: `glm_grammar_patch.py` → `_query_type()` (wrapped)

**What it does**: Wraps the existing `_query_type()` with two new categories:
- `computation` — queries containing "find", "compute", "calculate", "evaluate", "determine", "solve", "simplify", "differentiate", "integrate"
- `proof` — queries containing "prove", "proof", "show that", "verify that", "demonstrate"

Computation/proof queries get a `[qtype:computation]` or `[qtype:proof]` tag at the start of the response.

**Result**:
- 12/12 self-tests PASS
- Gold-set: 9/28 (no change), 0 regressions
- Query classification now works:
  - "Find all positive integers" → computation ✓
  - "Prove that 2+2=4" → proof ✓
  - "What is a boson?" → definition (no tag) ✓
  - "How does X relate to Y?" → explanation (no tag) ✓

**Decision**: KEPT. Lightweight, no regressions, gives the system explicit awareness of math/proof queries. Future: route computation queries directly to SymPy tools, route proof queries to a structured-reasoning path.

---

## What Was NOT Absorbed (and why)

### `GrammaticalDiffusionReasoner` (A* search) — REJECTED for now
**Source**: `ubp_grammatical_diffusion.py`
**Reason**: The A* reasoner does full vocabulary-wide search (O(n) per step, n=2338). Even with the FSM pruning, a single `reason()` call explores thousands of states. glm_v37's existing CRG-based reasoning (§06-§07) is faster and sufficient for the current gold set. The A* reasoner would be worth revisiting if the system needs to find *explanatory paths* between concepts (e.g. "explain how X relates to Y"), but that's not a current gold-set requirement.

### `GrammarFSM` (zone-transition gatekeeper) — REJECTED
**Source**: `glm_grammar_fsm.py`
**Reason**: The FSM enforces grammatical zone transitions (Noun → Verb → Noun). glm_v37 doesn't use zone-transition grammar — it uses CRG edges + idea coherence. Adding the FSM would constrain the system without clear benefit, and would require deep changes to the IdeaZone/ IdeaManager logic.

### `ZonedVocabulary.apply_shift` (operator composition) — DEFERRED
**Source**: `glm_zoned_lattice_embedding.py`
**Reason**: This composes an operator with a subject to produce a new vector (e.g. `apply_shift("energy", "increase")` → a vector for "increase(energy)"). It's interesting but the runtime doesn't currently have a use case for it. Would be worth absorbing if the system needs to handle compositional queries like "increase the energy of the system".

### Bucket D semantic modules — REJECTED (reject-by-default)
**Sources**: `ubp_semantic_engine.py`, `ubp_phenomenology.py`, `ubp_observer_dynamics.py`, `ubp_semantic_sovereign.py`
**Reason**: Per the consolidation plan, these are reject-by-default. The audit confirmed they're never imported. No clear path to benchmark improvement. Keeping them out.

### `build_glm_response` / `_assemble_sentence` (grammar patch response builder) — REJECTED
**Source**: `glm_grammar_patch.py`
**Reason**: These are the v3.3 response composer, superseded by glm_v37's §10 `compose_response`. Importing them would create two competing response composers.

---

## Summary Table

| # | Absorption | Source | Status | Gold-set delta | Self-tests |
|---|------------|--------|--------|----------------|------------|
| 1 | Lattice CRG auto-linking | `glm_concept_relation_graph.py` | KEPT | 0 | 12/12 |
| 2 | Reflexive recall | `auto_trigger.py` | KEPT | 0 | 12/12 |
| 3 | Gap-filling vector derivation | `glm_physics_vocab_pack.py` | KEPT (scaffolding) | 0 | 12/12 |
| 4 | Enhanced query-type detection | `glm_grammar_patch.py` | KEPT | 0 | 12/12 |

**Cumulative**: 9/28 gold-set (same as v3.7.1), 12/12 self-tests, 0 regressions, +123ms boot, +150 CRG edges, +20 inferred nouns/turn (was 18).

---

## What Needs to Happen Next (Data Work)

The absorptions added *capability* but didn't improve gold-set accuracy because the bottleneck is **vocabulary coverage**, not reasoning logic. Specifically:

1. **Basic math terms are missing**: "integers", "divisible", "prime", "fraction", "polynomial", "equation", "solution" — none are in the 2,338-word vocab. The gap-derivation (Absorption 3) tries to create vectors for them but the nearest anchor is too far away.

2. **The KB needs more math-anchored entries**: If the system KB had entries for "integer", "divisibility", "primality" etc. with proper MOG categories (M_Count, P_Ratio), the gap-derivation would have closer anchors and could successfully add derived vectors.

3. **The lexicon format needs reconciliation**: The `memory_kb_adapter` test failure (`lookup_by_phrase('hydrogen')` returns empty) is because KB entries use descriptive names like "Element: Hydrogen (H)" not just "hydrogen". The recall logic now handles this via token match, but the underlying KB naming inconsistency remains.

**The system is now ready to absorb a richer KB.** The scaffolding (lattice linking, recall, gap-derivation, query-type detection) will all become more effective as the KB grows. The user's task of growing the KBs is the correct next step — the system is equipped to use what they add.
