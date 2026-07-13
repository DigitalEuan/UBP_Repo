# GLM — Geometric Language Machine

**A deterministic, geometry-grounded language engine built on the 24-bit Golay/Leech substrate.**

[![Version](https://img.shields.io/badge/Version-3.22.0-blue.svg)]()
[![Status](https://img.shields.io/badge/Status-Active_Development-orange.svg)]()
[![Substrate](https://img.shields.io/badge/Substrate-Golay--Leech-cyan.svg)]()

**Part of:** [UBP Core Studio](https://github.com/DigitalEuan/UBP_Repo)
**Live demo:** [Google AI Studio](https://ai.studio/apps/6d78d479-2a4e-4e34-89b3-4b87b85d5b9a)

---

## What is the GLM?

The **Geometric Language Machine (GLM)** is a deterministic AI engine that grounds language in geometry. Unlike standard LLMs (which predict the next token probabilistically from training data), the GLM represents every word as a 24-bit vector in the [Golay code](https://en.wikipedia.org/wiki/Binary_Golay_code) / [Leech lattice](https://en.wikipedia.org/wiki/Leech_lattice) substrate, and reasons by computing geometric relationships between those vectors.

### The core idea

Every word in the GLM vocabulary has a 24-bit vector. These vectors are not learned from text — they are derived from the word's semantic content via SVD (singular value decomposition) on a co-occurrence matrix, then snapped to the nearest Golay codeword. This means:

- **Hamming distance between word vectors = semantic distance** (words that are close in Hamming space are semantically related)
- **NRCI (Non-Random Coherence Index) = word stability** (words at stable lattice positions have high NRCI)
- **The CRG (Concept Relation Graph) = semantic network** (curated edges like "hamiltonian generates time")

The GLM reasons by walking this geometric space: it finds related concepts via Hamming proximity, follows CRG edges for semantic relationships, and computes sentence structure (subject-verb-object) from vector geometry.

---

## Architecture

The GLM has 34 modules organized into 5 layers. Here is the essential structure (19 core files):

### Layer 1: The Substrate

| Module | What it does |
|--------|-------------|
| `ubp_unified_v5.py` | The Golay `[24,12,8]` engine + Leech lattice engine + Barnes-Wall engine. Exact rational arithmetic (no floats). 2,325-entry syndrome table, 4,096 codewords, 759 octads. |
| `refined_nrci.py` | **New.** The 5-shell sign-sensitive NRCI. Drop-in replacement for `LEECH_ENGINE.calculate_nrci()`. Breaks sign-blindness: 1 → 9 unique values across 128 octad variants. [See below.](#refined-nrci) |

### Layer 2: Vocabulary & CRG

| Module | What it does |
|--------|-------------|
| `GLM01_substrate.py` | Vocabulary builder + BLA (Binary Linear Algebra) + adapters to the real UBP engine. |
| `GLM20_svd_vocab.py` | Builds SVD-derived 24-bit vectors from corpus co-occurrence, snapped to Golay codewords. |
| `GLM23_grammar_vectors.py` | Computes grammatical roles (NOUN/VERB/ADJECTIVE/OPERATOR) from vector quadrant structure. |
| `GLM15_physics_pack.py` | Physics vocabulary with definitions (density matrix, Hamiltonian, etc.). |
| `GLM16_master_resource.py` | Loads `glm_master_resource_v1.json` (4,256 words with definitions + vectors). |
| `GLM03_crg.py` | The Concept Relation Graph. 173 curated edges: "hamiltonian generates time", "entropy measures dimension", etc. |
| `GLM27_crg_expander.py` | Auto-expands CRG from definition co-occurrence (173 → 5,000+ edges). |

### Layer 3: The Pipeline

| Module | What it does |
|--------|-------------|
| `GLM11_runtime.py` | **The orchestrator.** The 8-step `_run_pipeline(query)` that processes every query. [See below.](#the-chat-pipeline) |
| `GLM09_tools.py` | Math/symbolic computation detection and evaluation. |
| `GLM13_deliberative_reasoning.py` | Pattern-based multi-step reasoning (fallback for non-math queries). |
| `GLM14_lexer.py` | Multi-word tokenization (preserves "weyl anomaly", "quantum metric"). |
| `GLM07_idea_manager.py` | Idea zone management (accumulates evidence, crystallizes theses). |

### Layer 4: Generation

| Module | What it does |
|--------|-------------|
| `GLM21_generator.py` | Word-chain generator. Walks the 24-bit lattice using EMA centroid + CRG transition grammar. Uses the displaced-Golay resonance mechanism. |
| `GLM22_ontological_grammar.py` | Computed SVO grammar. Derives the verb from the AND-gap between subject and object vectors. Uses CRG edge labels + physics-verb whitelist for quality. |

### Layer 5: Composers

| Module | What it does |
|--------|-------------|
| `GLM10_response_composer.py` | Terse bracket-tag response (`[Recall]`, `[Backbone]`, `[Metrics]`, etc.). |
| `GLM19_prose_composer.py` | Fluent natural-language paragraph. Assembles recalled KB entries + definitions + generated text into prose. |
| `GLM17_semantic_frames.py` | Template-based backbone verbalization ("Hamiltonian generates time"). |

---

## The Chat Pipeline

When you call `rt.chat_prose("What is the weyl anomaly?")`, the query flows through 8 steps:

```
Query → [0] Anaphora resolution → [1] Math/symbolic detection → [2] Deliberative reasoning
      → [3] KB recall (alias map, phrase match, physics pack)
      → [4] Tokenization (multi-word phrases)
      → [5] Warm-start check (match prior ideas)
      → [6] Zone update (accumulate evidence, possibly crystallize)
      → [7] Generation (GLM22 ontological grammar — NEW)
      → [8] Composition (assemble prose)
      → Response
```

### Step 7: Generation (new in v3.22.0)

**This is the key architectural fix.** Previously, the chat pipeline was pure recall + reformat — zero generation. The generation engine (GLM21/GLM22) existed but was never called by `chat()` or `chat_prose()`. Now, Step 7 calls `OntologicalGrammar.construct_paragraph(topic, n_sentences=3)` and weaves the generated text into the response as "Extending from the substrate: ...".

This adds ~38% to output length and introduces novel word sequences for the first time.

---

## Refined NRCI

**New in v3.22.0.** The `refined_nrci.py` module is a drop-in replacement for the original NRCI that breaks sign-blindness.

### The problem

The original NRCI formula is:
```
tax = hw × Y + ns / 8
NRCI = 10 / (10 + tax)
```
where `hw` = Hamming weight (count of nonzero) and `ns` = sum of squares. Both terms **ignore sign** — so all 128 sign-variants of an octad (8 coordinates of ±2) have identical NRCI. **7 bits of information per octad are invisible.**

### The solution: 5-shell system

The Refined NRCI adds shells, each capturing structure the original discards:

| Shell | Name | What it measures | Sign-sensitive? | Unique values (128 octad variants) |
|-------|------|-----------------|-----------------|-----------------------------------|
| 0 | Golay | hw + ns/8 (original) | No | 1 |
| 1 | Sign-parity | Balance of +/− signs | Yes | 5 (Pascal 1-28-70-28-1) |
| 2 | Sextet-balance | Evenness across 4 MOG tetrads | Partial | — |
| 3 | Coset-type | Golay syndrome weight | No | — |
| 4 | Sextet-signed | 4-tuple of signed sextet sums | Yes | 24 |
| **All** | **Combined** | | | **9** |

### Usage

```python
from refined_nrci import RefinedNRCI
from ubp_unified_v5 import GOLAY_ENGINE

rnrci = RefinedNRCI(golay_engine=GOLAY_ENGINE)

# Binary vector (Shells 1,4 give 0 — no sign structure)
nrci = rnrci.compute([1,0,1,1,...])  # → float in (0, 1]

# Physical Leech point (±2 — all shells active)
nrci = rnrci.compute([2,-2,0,2,...])

# Full breakdown
breakdown = rnrci.describe([2,-2,0,2,...])
# → {shell0_golay, shell1_sign_parity, shell2_sextet_balance,
#    shell3_coset_type, shell4_sextet_signed, tax_total, nrci, sign_class, sextet_pattern}
```

### The MOG topology connection

Shell 4 (sextet-signed) is connected to the [MOG (Miracle Octad Generator)](https://en.wikipedia.org/wiki/Witt_design) — the native 4×6 column structure of the Golay code. The 24 coordinates split into 4 sextets (MOG tetrads):

```
Sextet 0: coords[0:6]   — Reality (Mass, Charge, Space, Time, Thermal, Count)
Sextet 1: coords[6:12]  — Information (Topology, Symmetry, Density, ...)
Sextet 2: coords[12:18] — Activation (Energy, Force, Velocity, ...)
Sextet 3: coords[18:24] — Potential (Probability, Ratio, Limit, ...)
```

The signed sum of each sextet gives a 4-tuple that distinguishes sign-variants within a Pascal class. This is the finest shell and the one that connects to the Leech lattice's sign structure.

---

## Generation: How It Works

The GLM has two generation modes:

### GLM21: Word-chain generator (displaced-Golay resonance)

The generator walks the 24-bit lattice using:
- **EMA centroid** (exponential moving average) as state — prevents the centroid collapse that plagued earlier versions
- **Resonance-guided selection** — picks words whose perturbation of the centroid lands closest to a target NRCI plateau (0.7196, the "saturation" plateau from cymatics analysis)
- **CRG bonus** — prefers words that are CRG-reachable from the last word

**Best configuration** (from 6 sessions of tuning):
```python
resonance_weight = 3.0  # resonance dominates
hamming_weight = 0.0    # no Hamming term (Session 2 finding)
crg_bonus = 0.30        # CRG guidance weight
target_nrci = 0.7196    # saturation plateau
ema_alpha = 0.3         # EMA update rate
```

### GLM22: Ontological grammar (computed SVO)

Constructs sentences as geometric objects:
```
Subject (NOUN) → gap_vector(subject, object) → Verb (nearest VERB to gap) → Object (NOUN)
```

The verb is **computed from geometry**, not looked up from a template. The AND-intersection of subject and object vectors tends to fall in the VERB quadrant — the gap between two nouns *contains* the verb that connects them.

**Verb quality fix (v3.22.0):**
1. **CRG-label first:** if there's a CRG edge between subject and object, use the edge label as the verb ("hamiltonian generates time" → verb = "generates")
2. **Physics-verb whitelist:** if no CRG edge, filter verb candidates to a curated list of ~80 high-frequency physics verbs (generates, measures, commutes, scales, transforms, etc.) instead of any random VERB-role word

---

## Getting Started

### Quick start

```python
from GLM11_runtime import GLMRuntimeV37

rt = GLMRuntimeV37()

# Terse bracket-tag response
print(rt.chat("what is the weyl anomaly?"))

# Fluent prose response (includes generation)
print(rt.chat_prose("how does the hamiltonian generate time?"))

# 4-paragraph considered response
print(rt.chat_considered("explain the relationship between entropy and dimension"))
```

### CLI

```bash
# Self-test
python3 GLM12_cli_entry.py --test

# Interactive chat (terse)
python3 GLM12_cli_entry.py --chat "what is hydrogen?"

# Prose mode (longer, more fluent)
python3 GLM12_cli_entry.py --chat-prose "what is the weyl anomaly?"
```

### Using the Refined NRCI

```python
from refined_nrci import RefinedNRCI
from ubp_unified_v5 import GOLAY_ENGINE

rnrci = RefinedNRCI(golay_engine=GOLAY_ENGINE)

# Test sign-blindness breaking
from ubp_unified_v5 import LEECH_ENGINE
octads = GOLAY_ENGINE.get_octads()
sample_octad = octads[0]
physical_points = LEECH_ENGINE.expand_octad_to_physical(sample_octad)

# Old NRCI: 1 unique value across 128 variants
old_nrcis = [float(LEECH_ENGINE.calculate_nrci(p)) for p in physical_points]
print(f"Old NRCI unique values: {len(set(round(n, 6) for n in old_nrcis))}")  # → 1

# Refined NRCI: 9 unique values
refined_nrcis = [rnrci.compute(p) for p in physical_points]
print(f"Refined NRCI unique values: {len(set(round(n, 6) for n in refined_nrcis))}")  # → 9
```

---

## Data: What the GLM Needs

The GLM's quality is bottlenecked by **data**, not code. Three data sources need growth:

### 1. The CRG (Concept Relation Graph)

**Current:** 173 curated edges over 130 nodes.
**Target:** 5,000+ edges over 2,000+ nodes.

The CRG is the semantic backbone. Every edge with a meaningful label (generates, measures, commutes_with, scales_as) directly improves generation quality — the verb fix uses CRG labels as verbs.

**To grow:** Use `GLM27_crg_expander.py` for auto-expansion from definition co-occurrence, then manually curate physics relationships:
- Hamiltonian → generates → Time
- Entropy → measures → Dimension
- Symmetry → generates → Anomaly
- etc.

### 2. Vocabulary definitions

**Current:** 4,256 words in `glm_master_resource_v1.json`.
**Target:** 10,000+ words with rich (2-3 sentence) definitions.

Definitions are used for recall and as generation seeds. Focus on:
- Physics concepts (QFT, condensed matter, optics)
- Mathematical operators (derivative, integral, commutator — verb candidates)
- Relations (equivalence, duality — operator candidates)
- Multi-word phrases (density matrix, partition function)

### 3. The System KB

**Current:** 746 entries in `system_kb/ubp_system_kb.json`.
**Target:** One KB entry per concept users might ask about.

Each entry needs: `name`, `desc` (2-3 sentences), `ubp_id`.

---

## File Map

### Essential (keep)

```
GLM/
├── GLM00_config.py                 # Paths + config
├── GLM01_substrate.py              # Vocab + Golay/Leech adapters
├── GLM02_constants.py              # Function words, edge labels
├── GLM03_crg.py                    # Concept Relation Graph
├── GLM04_number_vocab.py           # Number vocabulary
├── GLM07_idea_manager.py           # Zone management
├── GLM09_tools.py                  # Math/symbolic computation
├── GLM10_response_composer.py      # Terse response composer
├── GLM11_runtime.py                # Orchestrator (8-step pipeline + generation)
├── GLM13_deliberative_reasoning.py # Pattern-based reasoning
├── GLM14_lexer.py                  # Multi-word tokenization
├── GLM15_physics_pack.py           # Physics definitions
├── GLM16_master_resource.py        # Resource loading
├── GLM17_semantic_frames.py        # Backbone verbalization
├── GLM19_prose_composer.py         # Prose response composer
├── GLM20_svd_vocab.py              # SVD vocabulary builder
├── GLM21_generator.py              # Word-chain generator (displaced-Golay)
├── GLM22_ontological_grammar.py    # Computed SVO grammar
├── GLM23_grammar_vectors.py        # Grammar vector builder
├── GLM27_crg_expander.py           # CRG auto-expansion (for data growth)
├── refined_nrci.py                 # NEW: 5-shell sign-sensitive NRCI
├── glm_master_resource_v1.json     # Vocabulary (4,256 words, 15MB)
└── glm_unified_resource.json       # Unified resource
```

### Archive (not needed for core operation)

```
GLM05_idea_evidence.py          # (check if GLM07 needs it)
GLM06_idea_zone.py              # (check if GLM07 needs it)
GLM08_idea_meta_graph.py        # Long-term idea graph (optional)
GLM18_hex_colour.py             # Visualization only
GLM24_continuous_learner.py     # Experimental
GLM25_native_alu.py             # Redundant with GLM09
GLM26_crg_alu.py                # Redundant with GLM21
GLM28_native_poly.py            # Niche
GLM29_answer_extractor.py       # Optional ([Answer] tag)
GLM30_domain_filter.py          # Optional (domain filtering)
GLM31_verification.py           # Optional ([Verified] tag)
GLM32_mode_algebra.py           # Experimental
GLM33_considered_response.py    # Alternative composer
GLM34_simplicial_crg.py         # Experimental (2-complex topology)
exp_*.py                        # Experiment scripts (findings in reports)
test_*.py                       # Tests (keep for regression)
```

---

## Key Concepts

### NRCI (Non-Random Coherence Index)

Measures how stable a point in the 24-bit substrate is. High NRCI = stable lattice position; low NRCI = noisy. The **Refined NRCI** (`refined_nrci.py`) adds 4 shells to break sign-blindness. [See above.](#refined-nrci)

### CRG (Concept Relation Graph)

The semantic network. Nodes are vocab words, edges are labeled relationships (generates, measures, commutes_with). The CRG guides generation and backbone verbalization.

### Displaced-Golay resonance

The generation mechanism from Session 1. Instead of picking the nearest word to the centroid (Hamming), pick the word whose perturbation of the centroid lands closest to a target NRCI plateau. This is the "displaced Golay" pattern from the noisecore system — computation driven by perturbation-induced change, not absolute position.

### MOG (Miracle Octad Generator)

The native 4×6 column structure of the Golay code. The 24 coordinates split into 4 sextets (MOG tetrads). The Refined NRCI's Shell 4 (sextet-signed) operates on this structure. The MOG is the correct topology for the Golay code — better than the torus (which collapses sign-variants).

### Idea Zone

A dynamic accumulation of evidence around a topic. As the GLM processes a query, it builds a zone with topic nouns, a CRG backbone, and a centroid. When enough evidence accumulates, the zone "crystallizes" a thesis.

---

## Development History

The GLM has been developed across multiple sessions:

| Version | Focus | Key result |
|---------|-------|-----------|
| v3.10 | Real engine integration | Connected to ubp_unified_v5.py (real Golay/Leech) |
| v3.13 | GLM21 generator | First generation layer (word-chain walk) |
| v3.14 | GLM22 ontological grammar | Computed SVO from vector geometry |
| v3.17 | Sovereign computation | Native ALU, SVD-only vocab, CRG-Traversal-ALU |
| v3.18 | CRG expansion | Auto-expand from definitions (173 → 260+ edges) |
| v3.19 | Output fidelity | Answer extraction, domain filtering, verification |
| v3.21 | Simplicial CRG | 2-complex topology (Betti numbers, Euler characteristic) |
| **v3.22** | **Generation wiring + Refined NRCI** | **Generation plumbed into chat pipeline; 5-shell sign-sensitive NRCI; verb quality fix; Session 2-6 best configs** |

---

## License

Part of the UBP research initiative by Euan R. A. Craig. Experimental — please verify results independently.
