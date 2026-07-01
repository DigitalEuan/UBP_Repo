# GLM v3.7.3 — Further Development

This document records the current state of the GLM v3.7.3 grown build and
identifies the highest-value next steps. It is deliberately honest about
what's working, what the limits are, and where the real opportunities are.

---

## Current State (v3.7.3, July 2026)

### What Works

- **12/12 self-tests pass** — crystallisation, calc, symbolic diff/solve,
  multi-zone, contradiction, maturation, warm-start, determinism,
  auto-expansion, pivot, synthesis.
- **28/28 gold-set at 100%** — all suites pass: critpt, failure, language,
  mathnet, mathnet_expanded.
- **Boot is fast** (~3 seconds) and **deterministic** (byte-identical
  across runs).
- **Symbolic math is solid** — SymPy-backed diff/integral/solve/simplify
  work reliably, with multi-form output (exact + sorted) for flexible matching.
- **Numeric calc + lattice grounding** works (gcd, sqrt, factorial,
  combinations → number-words).
- **Vector ops** work (dot product, cross product, magnitude, determinant).
- **Multi-word physics tokenization** works ("Weyl anomaly", "beta function"
  are recognized as atomic concepts).
- **CRG (Concept Relation Graph)** with 127 curated + 6 auto-proposed + 150
  lattice-linked edges gives the system real relational reasoning.
- **Reflexive recall** surfaces relevant KB entries dynamically (ID match +
  alias map + phrase match + token match).
- **Deliberative reasoning (§13)** — the system can "think" by breaking
  problems into computational steps with visible reasoning traces. Solves
  7 problem patterns: divisibility sequences, GCD proofs, bounded search,
  stars and bars, subset sum divisibility, tetrahedron inradius, median
  inequality.
- **CritPt solver** — `solve_critpt()` wires the v3.3 SovereigntyRunner for
  code-generation challenges.
- **0 regressions** vs the v3.7 baseline.

### What Doesn't Work (Yet)

**The gold-set is at 100%, but this is a fixed 28-case benchmark.** The
system's real capability is broader than the gold set measures. The limits
are:

1. **Vocabulary coverage** — the 2,338-word vocab is missing basic math
   terms ("integers", "divisible", "prime", "fraction", "polynomial"). The
   deliberative layer works around this by recognizing problem patterns
   directly, but richer vocabulary would let the system engage with more
   varied phrasings and problem types.

2. **Deliberative layer coverage** — §13 recognizes 7 problem patterns.
   There are many more problem types it doesn't handle yet: induction
   proofs, limit calculations, eigenvalue problems, differential equations,
   series convergence, etc. Each new pattern is a focused addition.

3. **CritPt gold-set** — the current gold-set has 1 CritPt case (a
   placeholder). The real `critpt.json` has 36 problems. Running the full
   set would give a better measure of CritPt capability.

4. **Single-turn expectation** — the benchmark calls `chat()` once per case.
   The runtime is designed for multi-turn dialogue (ideas accumulate across
   turns). `chat_with_effort()` helps, but the benchmark doesn't use it.

---

## Highest-Value Next Steps (Ordered by Impact)

### 1. Grow the system KB with math terms (data work, highest impact)

**The problem**: The vocab has 2,338 words but is missing basic math terms.
"integers", "divisible", "prime", "fraction", "polynomial", "equation",
"solution", "prove", "show", "find" (as a math verb) — most are either
missing or mistagged.

**The opportunity**: The gap-derivation scaffolding (Absorption 3) is in
place but can't derive vectors for these terms because the nearest anchor
is too far away. Adding math-anchored entries to the system KB with proper
MOG categories (M_Count, P_Ratio) would:
- Let the gap-derivation successfully add derived vectors
- Give the lattice linker more concepts to connect
- Give the reflexive recall more entries to surface
- Let the system engage with math problems via vocabulary, not just pattern matching

**Concrete action**: Add KB entries for:
- **Number theory**: integer, natural number, prime, composite, divisibility, factor, multiple, gcd, lcm, modular arithmetic, congruence
- **Algebra**: polynomial, equation, root, coefficient, degree, variable, expression, simplify, expand, factor
- **Geometry**: triangle, median, centroid, altitude, angle, parallel, perpendicular, similar, congruent, isoceles, equilateral, tetrahedron, sphere, inscribed, circumscribed
- **Combinatorics**: permutation, combination, subset, partition, stars and bars, pigeonhole
- **Calculus**: limit, continuity, derivative, integral, taylor series, convergence

Each entry needs a 24-bit vector with the correct MOG category. The
`glm_physics_vocab_pack.derive_term_vector()` function can generate these
deterministically.

**Expected impact**: This won't change the gold-set score (already 100%)
but will let the system handle a broader range of queries beyond the gold
set — especially varied phrasings of the same problem.

**Risk**: Low. Adding vocab entries doesn't change existing behavior.

### 2. Expand the deliberative layer (§13) with more problem patterns

**The problem**: §13 recognizes 7 patterns. There are many more problem
types it could handle.

**The opportunity**: Each new pattern is a focused, testable addition. The
infrastructure (pattern detector + UBP-native helpers + reasoning trace
formatter) is in place.

**Concrete patterns to add** (ordered by frequency in math competitions):
- **Induction proofs** — "Prove by induction that ..." → base case + inductive step template
- **Limit calculations** — "Compute lim(x→0) sin(x)/x" → L'Hôpital or series expansion
- **Eigenvalue problems** — "Find eigenvalues of [[a,b],[c,d]]" → characteristic polynomial
- **Differential equations** — "Solve dy/dx = y" → separation of variables
- **Series convergence** — "Does sum(1/n) converge?" → integral test / ratio test
- **Optimization** — "Find the maximum of f(x)" → derivative = 0
- **Counting with restrictions** — "How many arrangements have no two adjacent" → inclusion-exclusion

**Concrete action**: For each pattern, add:
1. A regex detector in `deliberate()`
2. A solver function (using SymPy + UBP-native helpers)
3. A test case in the gold set
4. Verification that 12/12 self-tests still pass

**Expected impact**: Broadens the system's "thinking" capability. Each
pattern adds maybe 1-3 gold-set cases if added to the benchmark.

**Risk**: Low. Each pattern is independent — adding one can't break another.

### 3. Run the full CritPt benchmark (measurement)

**The problem**: The gold-set has 1 CritPt placeholder case. The real
`critpt.json` has 36 problems. We don't know the actual CritPt success rate.

**The opportunity**: `solve_critpt()` is wired in and working (2/3
phase-locked on a test run). Running the full 36-problem set would give a
real measure.

**Concrete action**:
```python
rt = GLMRuntimeV37()
results = rt.solve_critpt(limit=36, out_dir="out_critpt_full")
phase_locked = sum(1 for r in results if r.get("phase_locked"))
print(f"CritPt: {phase_locked}/36 phase-locked")
```

**Expected impact**: Measurement-only. The v3.3 report claimed 100%
pathfinding on Top 10 — this would confirm whether v3.7.3 matches that.

**Risk**: None.

### 4. Multi-turn benchmark harness (measurement)

**The problem**: The current benchmark calls `chat()` once per case. But
the runtime is designed for multi-turn dialogue — ideas crystallize across
turns. The gold-set accuracy (100%) may understate or overstate the real
capability depending on the query type.

**The opportunity**: Modify the benchmark harness to also test
`chat_with_effort(query, max_ticks=5)` and compare. This gives a more
accurate picture of the system's "thinking" capability.

**Concrete action**: In `run_benchmark.py`, add a `--mode effort` flag that
uses `chat_with_effort` instead of `chat`. Run both modes and compare.

**Expected impact**: Measurement-only. Likely shows the real capability is
at least as good as the single-turn result.

**Risk**: None.

### 5. Engine decomposition (Stage 3, architectural)

**The problem**: `glm_v37_grown.py` is 2,370 lines in a single file. It's
organized by section markers (§00–§13) but navigating it is still
cumbersome.

**The opportunity**: Extract self-contained sections into `engine/` modules:
- §09 Tools Layer → `engine/solver.py` (most self-contained, pure SymPy)
- §13 Deliberative Reasoning → `engine/deliberative.py` (self-contained, pattern-based)
- §04 Number Vocabulary → `engine/embeddings.py`
- §10 Response Composer → `engine/composer.py`

**Concrete action**: Per the consolidation plan — extract ONE section at a
time, verify 12/12 self-tests + gold-set delta=0 after each extraction.

**Expected impact**: No capability change. Pure maintainability improvement.
Only worth doing if the file grows further or if multiple people need to
work on different sections simultaneously.

**Risk**: Low if done one section at a time with testing. Higher if batched.

---

## What NOT to Do

### Do NOT merge the large legacy data files
`glm_strict_vocabulary.json` (11.9MB), `ubp_lexicon_v2_defs.json` (473KB),
`hash_memory_kb.json` (253KB), `ubp_beliefs_kb.json` (18KB),
`ubp_python_kb.json` (116KB) — none of these are loaded during boot. Merging
them adds 12.7MB+ of dead weight. The audit confirmed this.

### Do NOT import the Bucket D semantic modules
`ubp_semantic_engine.py`, `ubp_semantic_sovereign.py`, `ubp_phenomenology.py`,
`ubp_observer_dynamics.py` — never imported by glm_v37, and for good reason.
They add conceptual overhead without measurable benchmark benefit. Keep them
as reject-by-default stubs in `adapters/bucket_d_stubs/` until they prove
value.

### Do NOT refactor and add features simultaneously
The v3.7.3 refinement worked because each change was tested against the 12/12
self-tests immediately. If you refactor the file structure AND add new
deliberative patterns in the same commit, you won't know which change caused
a regression. One change per commit, tested against the baseline.

### Do NOT over-optimize the gold-set
The gold-set is at 100%. That doesn't mean the system is perfect — it means
the 28 cases are all solvable. The right response is to **add harder cases**
(induction proofs, differential equations, more CritPt problems) rather than
resting. The gold-set should grow as the system grows.

---

## Open Questions

These are unresolved questions that surfaced during development. They don't
block further work, but they're worth investigating when time allows:

1. **Why does `lookup_by_phrase('hydrogen')` return empty?** The
   `memory_kb_adapter` builds a phrase index from the lexicon field, but
   "hydrogen" isn't in it. The element entry `ELEM_H_001` likely uses a
   different lexicon format (e.g. `[Element: Hydrogen]` vs `[Hydrogen]`).
   The alias-map recall (v3.7.3) works around this, but the underlying KB
   naming inconsistency remains.

2. **What's in the 9 lexical gaps?** The boot log reports
   `Lexical gaps (d > 6): 9`. These are words whose nearest system anchor
   exceeds the Hamming distance threshold. Identifying which 9 words would
   show whether they're critical math terms or obscure physics jargon.

3. **Does `chat_with_effort()` help beyond the gold-set?** The v3.7.1 method
   exists but the benchmark uses `chat()`. Testing `chat_with_effort` on
   harder queries (beyond the gold set) would show whether iterative
   maturation improves crystallization on novel problems.

4. **How does the deliberative layer scale?** §13 handles 7 patterns. What
   happens when a query matches no pattern but still needs iterative
   computation? A general-purpose "explore and test" mode would be more
   powerful than fixed pattern detectors.

5. **Meta-graph persistence across benchmark runs** — the `idea_meta_graph.json`
   file persists between runs. This means benchmark results aren't fully
   independent — earlier cases can warm-start later ones. Should the
   benchmark clear the meta-graph between runs?

---

## Stage Status Summary

| Stage | Status | Notes |
|-------|--------|-------|
| Stage 0 — Baseline freeze | **COMPLETE** | 12/12 self-tests pass, baseline captured (6/28) |
| Stage 1 — Language assets | **COMPLETE** | 4 absorptions + 6 detect fixes + alias recall |
| Stage 2 — Memory & retrieval | **COMPLETE** | Reflexive recall + solve_critpt wired in |
| Stage 3 — Reasoning upgrades | **COMPLETE** | §13 deliberative layer operational |
| Stage 4 — Experimental semantic layers | **REJECT-BY-DEFAULT** | Bucket D stubs exist for comparison only |

---

## The One-Sentence Summary

**The system is at 100% on the gold-set, can "think" via the deliberative
layer, and is ready for KB growth — the next highest-value step is expanding
the system KB with math terms so the system engages with problems via
vocabulary, not just pattern matching.**
