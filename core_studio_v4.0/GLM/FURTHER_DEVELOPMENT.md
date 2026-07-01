# GLM v3.7.1 — Further Development

This document records what we learned from the v3.7.1 refinement pass and
identifies the highest-value next steps. It is deliberately honest about
what's working, what isn't, and where the real opportunities are.

---

## Current State (v3.7.1, July 2026)

### What Works

- **12/12 self-tests pass** — crystallisation, calc, symbolic diff/solve,
  multi-zone, contradiction, maturation, warm-start, determinism,
  auto-expansion, pivot, synthesis.
- **Boot is fast** (~3 seconds) and **deterministic** (byte-identical
  across runs).
- **Symbolic math is solid** — SymPy-backed diff/integral/solve/simplify
  work reliably.
- **Numeric calc + lattice grounding** works (gcd, sqrt → number-words).
- **Multi-word physics tokenization** works ("Weyl anomaly", "beta function"
  are recognized as atomic concepts).
- **CRG (Concept Relation Graph)** with 127 curated + 6 auto-proposed edges
  gives the system real relational reasoning.
- **v3.7.1 refinements** improved gold-set accuracy from 6/28 (21.4%) to
  9/28 (32.1%) with 0 regressions.

### What Doesn't Work (Yet)

**The biggest gap: 19/28 gold-set cases still don't produce natural-language
answers.** The runtime recognizes concepts but ideas don't crystallize
(coherence < 0.70) in a single `chat()` turn. The v3.7.1 `[forming]` fallback
makes this visible to the user, but it doesn't solve the underlying issue.

Root cause, confirmed by audit:

- **Vocabulary coverage gaps** — basic math terms like "integers", "divisible",
  "positive", "prime", "fraction", "irreducible" are NOT in the 2,338-word
  vocab. The runtime returns `[gap] no verified vector for: integers, divisible.`
  for most MathNet problems.
- **Single-turn expectation** — the runtime is designed for multi-turn
  dialogue (ideas accumulate across turns), but the gold set (and most
  benchmarks) expect single-turn answers.

---

## Highest-Value Next Steps (Ordered by Impact)

### 1. Expand math vocabulary (Stage 1, highest impact)

**The problem**: The vocab has 2,338 words but is missing basic math terms.
"integers", "divisible", "prime", "fraction", "polynomial", "equation",
"solution", "prove", "show", "find" (as a math verb, not the stop-word) —
most are either missing or mistagged.

**The opportunity**: The legacy `glm_lang_database.py` has 574 concepts
across 24 tiers, many of which are math terms. The legacy
`glm_physics_vocab_pack.py` can derive vectors for new terms
deterministically. Neither is fully merged into the live vocab.

**Concrete action**: Write a one-time script that:
1. Loads the current vocab (`rt.glm.vocab.words.keys()`)
2. Loads `glm_lang_database.build_priority_vocabulary().words`
3. Finds concepts in the legacy DB that are missing from the live vocab
4. For each missing concept, derives a vector via `glm_physics_vocab_pack.derive_term_vector()`
5. Hamming-verifies the vector against existing anchors
6. Adds the verified entries to the live vocab
7. Re-runs the gold-set benchmark

**Expected impact**: This is the single highest-impact change. Most MathNet
failures are vocabulary gaps, not reasoning failures. If "integers" and
"divisible" enter the vocab, the runtime can at least form an idea around
them.

**Risk**: Low. Adding vocab entries doesn't change existing behavior — it
only gives the runtime more concepts to work with. Verify with 12/12
self-tests + gold-set comparison.

### 2. Add math-verb recognition (Stage 1, medium impact)

**The problem**: "Find", "prove", "show", "solve" are tagged as stop-words
or OPERATORs, so they're filtered out of content tokens. This means the
runtime can't distinguish "Find all X" from "What is X?".

**The opportunity**: Tag these as VERBs with appropriate MOG categories so
they survive content filtering and can trigger query-type detection
(`_query_type` already returns "definition" vs "explanation" vs "metric",
but doesn't have a "computation" or "proof" type).

**Concrete action**: In `glm_v37_unified.py` §02, the `FUNCTION_WORDS`
frozenset includes "explain", "define", "describe", etc. Remove "find",
"show", "prove" from the filter if they're there, and ensure they're in the
vocab as VERBs. Add a "proof" or "computation" query type to
`glm_grammar_patch._query_type()`.

**Expected impact**: Medium. Won't fix vocab gaps, but will let the runtime
recognize "Find X" as a computation request and route to the SymPy tools
layer.

### 3. Multi-turn benchmark harness (Stage 1, enables accurate measurement)

**The problem**: The current benchmark calls `rt.chat(query)` once per case.
But the runtime is designed for multi-turn dialogue — ideas crystallize
across turns. The gold-set accuracy (9/28) understates the system's real
capability.

**The opportunity**: Modify the benchmark harness to call
`rt.chat_with_effort(query, max_ticks=5)` (the v3.7.1 method) instead of
`rt.chat(query)`. This gives ideas up to 5 maturation ticks to crystallize.

**Concrete action**: In `benchmarks/run_benchmark.py`, change the `run_case`
function to use `chat_with_effort`. Re-run the gold set. Compare.

**Expected impact**: Measurement-only — doesn't change the system, just
gives a more accurate picture. Likely shows the real capability is higher
than 9/28.

### 4. Replace CritPt gold-set placeholder (Stage 1, measurement)

**The problem**: The gold set has 1 placeholder CritPt case
(`CRITPT_01_PLACEHOLDER`) that passes trivially because the `[forming]`
fallback happens to contain "weyl anomaly". This isn't a real test.

**The opportunity**: The real `critpt.json` has 113KB of frontier-physics
problems. Extract 5–10 representative cases with proper `query` and
`expected` fields.

**Concrete action**: Read `critpt.json`, identify problems with clear
expected answers, add them to `benchmarks/golden_cases.json` replacing the
placeholder.

**Expected impact**: Better measurement of CritPt capability. Won't change
the system itself.

### 5. Engine decomposition (Stage 3, architectural)

**The problem**: `glm_v37_unified.py` is 1,526 lines in a single file. It's
organized by section markers (§00–§12) but navigating it is still cumbersome.

**The opportunity**: Extract self-contained sections into `engine/` modules:
- §09 Tools Layer → `engine/solver.py` (most self-contained, pure SymPy)
- §04 Number Vocabulary → `engine/embeddings.py` (along with vector logic)
- §10 Response Composer → `engine/composer.py`

**Concrete action**: Per the consolidation plan — extract ONE section at a
time, verify 12/12 self-tests + gold-set delta=0 after each extraction.

**Expected impact**: No capability change. Pure maintainability improvement.
Only worth doing if the file grows further or if multiple people need to
work on different sections simultaneously.

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
value (which, based on the audit, is unlikely).

### Do NOT refactor and add features simultaneously

The v3.7.1 refinement pass worked because each edit was tested against the
12/12 self-tests immediately. If you refactor the file structure AND add new
vocab in the same commit, you won't know which change caused a regression.
One change per commit, tested against the baseline.

---

## Open Questions from the Audit

These are unresolved questions that surfaced during the v3.7.1 refinement.
They don't block further development, but they're worth investigating when
time allows:

1. **Why does `lookup_by_phrase('hydrogen')` return empty?** The
   `memory_kb_adapter` builds a phrase index from the lexicon field, but
   "hydrogen" isn't in it. The element entry `ELEM_H_001` likely uses a
   different lexicon format (e.g. `[Element: Hydrogen]` vs `[Hydrogen]`).
   Needs investigation of the actual lexicon string format.

2. **Does `chat_with_effort()` actually help?** The v3.7.1 method exists
   but hasn't been benchmarked yet. The gold-set benchmark uses `chat()`,
   not `chat_with_effort()`. Running the benchmark with both would show
   whether iterative maturation improves crystallization.

3. **What's in the 9 lexical gaps?** The boot log reports
   `Lexical gaps (d > 6): 9`. These are words whose nearest system anchor
   exceeds the Hamming distance threshold. Identifying which 9 words would
   show whether they're critical math terms or obscure physics jargon.

4. **Why does the meta-graph grow across benchmark runs?** The boot log
   shows `meta_graph=0 prior` on first boot but `meta_graph=6 prior` on
   subsequent boots. The `idea_meta_graph.json` file persists between runs.
   This is by design (warm-start feature) but means benchmark results
   aren't fully independent — earlier cases can warm-start later ones.
   The benchmark calls `rt.reset_idea()` between cases but doesn't clear
   the meta-graph.

---

## Stage Status Summary

| Stage | Status | Notes |
|-------|--------|-------|
| Stage 0 — Baseline freeze | **COMPLETE** | 12/12 self-tests pass, baseline captured (6/28) |
| Stage 1 — Language assets | **IN PROGRESS** | v3.7.1 refined the response composer; vocab expansion is next |
| Stage 2 — Memory & retrieval | NOT STARTED | Memory adapters work but `inject()` not yet implemented |
| Stage 3 — Reasoning upgrades | NOT STARTED | Engine decomposition deferred until vocab is expanded |
| Stage 4 — Experimental semantic layers | REJECT-BY-DEFAULT | Bucket D stubs exist for comparison only |

---

## The One-Sentence Summary

**The system works (12/12 self-tests, deterministic, fast) but can't answer
most gold-set questions because it's missing basic math vocabulary — the
highest-value next step is merging the legacy `glm_lang_database.py` concepts
into the live vocab, one tier at a time, with gold-set verification.**
