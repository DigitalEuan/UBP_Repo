# GLM v3.3 Implementation & Reproduction Guide

## System Overview
The Geometric Language Machine (GLM) v3.3 is a deterministic, phase-locked semantic engine grounded in the 24-bit Golay/Leech-lattice substrate. It uses a combination of zoned lattice embeddings, A* reasoning, and tensor-based concept transformations to process scientific and mathematical queries.

## Script Stack (Core Components)

1.  **`ubp_unified_v5.py`**: The mathematical core. Provides the `GOLAY_ENGINE` and `LEECH_ENGINE` for vector operations, NRCI calculation, and ontological health auditing.
2.  **`glm_zoned_lattice_embedding.py`**: Implements the grammar lattice. Partitions the 24 bits into S/O/M zones and provides the `apply_shift` logic for tensor composition.
3.  **`glm_lang_database.py`**: The priority vocabulary. Contains ~1000 grounded concepts across 70 tiers, ensuring 100% semantic coverage for the CritPt dataset.
4.  **`glm_grammar_fsm.py`**: The structural gatekeeper. Enforces grammatically valid zone transitions (e.g., Noun -> Verb -> Noun) using a finite state machine.
5.  **`ubp_grammatical_diffusion.py`**: The reasoning engine. Uses A* search with contextual attraction potentials to find grounded paths between concepts.
6.  **`glm_multi_token_lexer.py`**: The linguistic processor. Handles multi-word detection, recursive LaTeX scrubbing, and fuzzy matching biased by manifold memory.
7.  **`glm_concept_relation_graph.py`**: The semantic layer. Stores hand-curated physical relations (e.g., `generates`, `scales_as`) used to stylize reasoning paths.
8.  **`glm_engine_v31.py`**: The integrated engine. Consolidates all components into the `GLMSemanticEngine`, implementing stateful memory and health feedback.
9.  **`glm_runtime.py`**: The main entry point. Provides a high-level facade for `chat()` and `solve()` operations.

## How to Run

### 1. Natural Language Query (Chat)
To interact with the GLM in a stateful, grounded dialogue session:
```python
from glm_runtime import GLMRuntime
rt = GLMRuntime()
response = rt.chat("How does the hamiltonian relate to time?")
print(response)
```

### 2. CritPt Benchmark
To run the full suite of CritPt challenges and generate reasoning traces:
```python
from glm_runtime import GLMRuntime
rt = GLMRuntime()
results = rt.solve_critpt(limit=10, out_dir="out_v3.3")
```

### 3. Diagnostic Audit
To evaluate grounding coverage and path success rates:
```bash
python3 critpt_diagnostic.py
```

## Implementation Notes
*   **100% Grounding**: Every token in the CritPt dataset is now matched against a deterministic lattice point in `LANG_DB`.
*   **Stateful Bias**: The engine maintains a `context_centroid` which attracts reasoning paths toward the ongoing topic.
*   **Self-Correction**: Unstable query concepts (low NRCI) are automatically substituted with healthier neighbors before reasoning begins.
