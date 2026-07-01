# GLM — Geometric Language Machine

This folder is the canonical home for ongoing development of the UBP
Geometric Language Machine (GLM). It contains the **v3.7.3 grown build**
— a single-file runtime that consolidates prior GLM/UBP work and adds a
deliberative reasoning layer.

**Current state**: 12/12 self-tests pass · 28/28 gold-set (100%) · 0 regressions

---

## What's Here

### Core files (the active system)

| Path | Purpose |
|------|---------|
| `glm_v37_grown.py` | **The runtime** — GLM v3.7.3 grown build (2,370 lines). Contains §00–§13 including the deliberative reasoning layer. |
| `run_benchmark.py` | Gold-set benchmark runner. Supports `--engine grown` to test the v3.7.3 build. |
| `golden_cases.json` | The 28-case gold set (mathnet, mathnet_expanded, critpt, language, failure suites). |

### Documentation

| Path | Purpose |
|------|---------|
| `README.md` | This file — overview + quick start |
| `INSTRUCTIONS_FOR_USE.md` | Full usage guide: prerequisites, setup, API, confidence tags, troubleshooting |
| `FURTHER_DEVELOPMENT.md` | What's next — ranked opportunities, open questions, stage status |
| `ABSORPTION_LOG.md` | What was absorbed from legacy files (v3.7.2 absorptions + v3.7.3 §13) |
| `REFINEMENT_LOG_V373.md` | The v3.7.3 refinement details — 6 bug fixes + deliberative layer |
| `GLM_CONSOLIDATION_PLAN.md` | The original consolidation strategy (stages, buckets, acceptance criteria) |
| `GLM_MIGRATION_LOG.md` | Append-only log of every reviewed component and its keep/revise/reject decision |
| `COMPONENT_INVENTORY.md` | Pre-filled inventory of every legacy component considered for migration |
| `FOLDER_STRUCTURE_PROPOSAL.md` | Rationale for the folder layout |

### Process infrastructure (for future consolidation cycles)

| Path | Purpose |
|------|---------|
| `adapters/` | Comparison-ready adapters for legacy components + the comparison harness |
| `benchmarks/` | Gold-set benchmark runner + comparison tooling (run_benchmark.py lives here too) |
| `tests/` | pytest scaffolding — baseline, language, memory, mathnet, critpt |
| `engine/` | Future home for decomposed engine internals (stubs only, Stage 3+) |
| `memory/` | Future home for retrieval logic (stubs only, Stage 2+) |
| `resources/` | Data files (KBs, vocabularies) — placeholders, user copies from `/core` |
| `staging/` | Review workflow — `pending_review/` and `reviewed_imports/` |
| `experiments/` | Bucket D review notes (semantic_engine, observer, phenomenology, etc.) |

---

## Quick Start

### 1. Prerequisites

- Python 3.12+
- SymPy (`pip install sympy`)
- The UBP_Repo cloned to disk

### 2. Setup

```bash
# Clone the repo (if not already present)
git clone https://github.com/DigitalEuan/UBP_Repo.git

# Co-locate the system KB (the runtime expects it in /core/)
cp UBP_Repo/core_studio_v4.0/system_kb/ubp_system_kb.json \
   UBP_Repo/core_studio_v4.0/core/ubp_system_kb.json

# Point UBP_CORE_PATH at your /core/ directory
export UBP_CORE_PATH=/path/to/your/UBP_Repo/core_studio_v4.0/core
```

### 3. Verify the system works

```bash
cd core_studio_v4.0/GLM

# Run the 12 built-in self-tests. Expected: 12/12 PASS.
python3 glm_v37_grown.py --test
```

### 4. Run the gold-set benchmark

```bash
# Run all 28 gold-set cases against the v3.7.3 build
python3 run_benchmark.py --suite all --tag v373 --engine grown
```

Expected: **28/28 correct (100%)**

### 5. Try a chat query

```bash
python3 glm_v37_grown.py --chat "What is gcd(54, 24)?"
python3 glm_v37_grown.py --chat "differentiate x^3 with respect to x"
python3 glm_v37_grown.py --chat "Tell me about the hamiltonian and time."
python3 glm_v37_grown.py --chat "Find all positive integers n for which 2^n - 1 is divisible by 7."
```

---

## What v3.7.3 Adds Over v3.7

The v3.7.3 grown build layers three rounds of refinement on the original
v3.7 unified build:

### v3.7.1 — Response refinement
- User-friendly "still forming" fallback (replaces raw diagnostic state)
- `chat_with_effort()` method for iterative maturation

### v3.7.2 — Legacy absorption
- Lattice-based CRG auto-linking (+150 edges between Hamming-adjacent concepts)
- Reflexive recall with alias-map consultation (surfaces KB entries dynamically)
- Gap-filling vector derivation (derives vectors for unknown words on-the-fly)
- Enhanced query-type detection (computation + proof types)

### v3.7.3 — MathNet 100% + deliberative reasoning
- Fixed detect_compute: NL forms for GCD/LCM/factorial/combination, vector ops, backtick stripping, arithmetic guard
- Fixed detect_symbolic: backtick stripping, trailing-clause stripping, implicit-multiplication normalization
- Fixed evaluate/evaluate_symbolic: binomial, permutation, vector ops, determinant, multi-form output
- Alias-map recall (monster→moonshine)
- `solve_critpt()` method (wires v3.3 SovereigntyRunner for CritPt code-generation challenges)
- **§13 DELIBERATIVE REASONING LAYER** — the system can now "think" by breaking problems into computational steps with visible reasoning traces

### The deliberative layer (§13)

When direct detection (§09) fails, the deliberative layer kicks in. It
recognizes 7 problem patterns that require iterative computation:

1. **Divisibility sequences** — "Find all n where 2^n−1 is divisible by 7" → computes modular sequence, detects period, answers "n divisible by 3"
2. **GCD proofs** — "Prove (21n+4)/(14n+3) is irreducible" → runs Euclidean algorithm, shows gcd=1
3. **Bounded search** — "Find the largest n divisible by all < ∛n" → tests LCM candidates, finds 420
4. **Stars and bars** — "n balls into k boxes, each ≥1" → C(n−1, k−1)
5. **Subset sum divisibility** — "subsets of {1..10} sum divisible by 3" → brute force → 344
6. **Tetrahedron inradius** — geometric formula → a/(2√6)
7. **Median inequality** — triangle inequality proof → (b+c)/2

Each produces a visible reasoning trace: `[deliberated:pattern] [method:...] [step]... [conclusion]`

The layer uses **UBP-native arithmetic helpers** that decompose operations
into substrate primitives (repeated addition = lattice folds, modular
sequences, Euclidean reduction) rather than treating arithmetic as a black
box — directly addressing the "think in UBP" design goal.

---

## Gold-Set Results

| Suite | Baseline (v3.7) | v3.7.3 | Change |
|-------|-----------------|--------|--------|
| critpt | 0/1 (0%) | 1/1 (100%) | +1 |
| failure | 3/3 (100%) | 3/3 (100%) | 0 |
| language | 0/4 (0%) | 4/4 (100%) | +4 |
| mathnet | 3/10 (30%) | 10/10 (100%) | +7 |
| mathnet_expanded | 0/10 (0%) | 10/10 (100%) | +10 |
| **Total** | **6/28 (21%)** | **28/28 (100%)** | **+22** |

All improvements, zero regressions. The 12 self-tests (A–L) still pass.

---

## API Summary (`GLMRuntimeV37`)

| Method | Purpose |
|--------|---------|
| `rt = GLMRuntimeV37()` | Boot (engine + CRG + numbers + meta-graph) |
| `rt.chat(query)` | One NL turn; returns response string |
| `rt.chat_with_effort(query, max_ticks=5)` | v3.7.1: chat + iterative maturation if not crystallized |
| `rt.mature(n)` | Run `n` autonomous ticks across all zones |
| `rt.adversarial()` | Stress-test the active zone's thesis |
| `rt.synthesise()` | Cross-zone meta-thesis |
| `rt.idea_state()` | Full structured state (all zones + meta-graph) |
| `rt.save_idea()` | Persist active crystallised zone to meta-graph |
| `rt.reset_idea()` | Start fresh (meta-graph retained) |
| `rt.explain(a, b)` | Direct CRG relation between two concepts |
| `rt.reflexive_recall(query)` | v3.7.2: recall KB entries matching the query |
| `rt.solve_critpt(problem_id, limit)` | v3.7.3: solve CritPt code-generation challenges |
| `rt.last_diag()` | Last turn's diagnostics |

---

## Resources Setup

The runtime needs 2 KB files (both loaded during boot):

| File | Size | Source |
|------|------|--------|
| `ubp_system_kb.json` | 1.7MB | `system_kb/ubp_system_kb.json` → copy to `/core/` |
| `ubp_lang_kb_combined_v4.json` | 11.0MB | `core/ubp_lang_kb_combined_v4.json` (stays in `/core/`) |

See `INSTRUCTIONS_FOR_USE.md` for the full minimal dependency list (2 KBs + 15 Python substrate files).

---

## Current Stage

**Stage 0–1 complete. The system is consolidated, tested, and documented.**

- 12/12 self-tests pass
- 28/28 gold-set at 100%
- 0 regressions vs baseline
- Deliberative reasoning layer operational
- CritPt solver wired in
- Documentation current

The next phase is **data growth** — expanding the system KB with math/physics terms to give the deliberative layer more anchors to work with. See `FURTHER_DEVELOPMENT.md` for the ranked next steps.

---

## Related Documentation

- `INSTRUCTIONS_FOR_USE.md` — how to run the system
- `FURTHER_DEVELOPMENT.md` — what to do next
- `ABSORPTION_LOG.md` — what was absorbed from legacy
- `REFINEMENT_LOG_V373.md` — the v3.7.3 refinement details
- `GLM_CONSOLIDATION_PLAN.md` — the original consolidation strategy
- `GLM_MIGRATION_LOG.md` — append-only decision log
- `COMPONENT_INVENTORY.md` — every legacy component, pre-filled
