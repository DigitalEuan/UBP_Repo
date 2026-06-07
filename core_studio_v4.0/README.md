# Universal Binary Principle (UBP) — Core Studio v7.2

**Author:** Euan R. A. Craig, New Zealand
**Version:** 7.2.0 (Genesis Edition)
**Date:** 27 May 2026
**License / Status:** Experimental research platform — *please double-check results against your own work before drawing conclusions.*

| Resource | Link |
| :--- | :--- |
| **Live Environment (Google AI Studio)** | <https://ai.studio/apps/6d78d479-2a4e-4e34-89b3-4b87b85d5b9a> |
| **Core Studio App Repository** | <https://github.com/DigitalEuan/ubp_core_studio_app> |
| **Digital Twin Physics Engine Repository** | <https://github.com/DigitalEuan/ubp_digital_twin_physics_engine> |
| **Operational Manifest** | [`core/ubp_files_and_usage.md`](core/ubp_files_and_usage.md) |
| **Primary Knowledge Bank** | [`system_kb/ubp_system_kb.json`](system_kb/ubp_system_kb.json) (746 entries, 420 Laws) |

---

## 1. What Is the Universal Binary Principle?

The **Universal Binary Principle (UBP)** is a theoretical and computational framework that proposes physical reality is fundamentally an **information-processing system** running on a **24-bit geometric substrate**. Rather than treating particle masses, coupling constants, and physical laws as arbitrary empirical numbers, UBP attempts to *derive* them as emergent geometric properties of a self-correcting code — the **Extended Binary Golay Code [24, 12, 8]** — embedded inside the **24-dimensional Leech Lattice (Λ₂₄)**.

The central claim is simple but radical: the universe is not merely *described* by mathematics; it *is* mathematics — specifically, a recursive, deterministic, error-corrected computation whose stable codewords correspond to particles, elements, molecules, and physical constants. Every entity in the framework has a unique 24-bit "hardware address" that is generated deterministically from its measurable properties; no curve-fitting, no free parameters.

UBP Core Studio is the active research workbench for that hypothesis. It is a suite of Python scripts plus a JSON knowledge bank that together let a researcher:

- **Derive fundamental constants from geometry alone.** The fine-structure constant, the proton/electron mass ratio, the muon/electron ratio, the Higgs mass, the Top quark mass, and others all emerge from the interaction of the three transcendental primitives π, φ, e with the Leech Lattice — with errors typically under 0.05% and several constants under 0.001%.
- **Assign every physical entity a deterministic 24-bit address** derived solely from its `math` (Phenomenal DNA) field via Grey-Code fingerprinting and Golay encoding.
- **Model the stability, complexity, and metabolic cost** of any physical or conceptual object using **exact rational arithmetic** (Python's `fractions.Fraction`), eliminating floating-point drift.
- **Simulate the synthesis of matter** from primitives (quarks → nucleons → atoms → molecules) and predict emergent properties such as binding energy, topological stability, and "Islands of Stability" in the super-heavy element regime.
- **Run a domain-specific geometric programming language (UBP-Py)** that translates text commands into 24-dimensional vector additions inside the Leech Lattice.
- **Talk to the system through a semantic engine** that maps natural-language queries onto 24-bit vectors via Cosine Resonance, and uses a swarm of agents to invent new mathematical operators when no human word exists for a given lattice state - experimental.

This is an **active research environment**, not a polished product. Things move, scripts get refactored, and benchmarks tighten as the work matures. Treat every number as a working hypothesis to be reproduced.

---

## 2. The Core Pillars (v7.0 Standard)

Five architectural pillars define what makes the current platform "UBP":

| Pillar | What it is | Why it matters |
| :--- | :--- | :--- |
| **Substrate** | 24-bit Extended Binary Golay Code **[24,12,8]** → 4,096 perfect codewords ("Noumenal Seeds") | The smallest space in which a perfect error-correcting code exists with a 3-bit correction radius. Every "real" object must be one of these codewords. |
| **Geometry** | The **Leech Lattice Λ₂₄** with 196,560 kissing points | The densest possible 24-D sphere packing. Provides every codeword with a unique geometric position and a calculable "Symmetry Tax." |
| **Macro-Bulk** | 256-dimensional **Barnes-Wall Lattice (BW₂₅₆)** | For molecules and macroscopic structures that are too complex to compress into 24 bits without extreme topological tension. SHA-256 hashes map 1:1 onto BW₂₅₆ coordinates. |
| **Logic** | 100% **Exact Rational Arithmetic** (`fractions.Fraction`) | "Float-free" core — eliminates the floating-point aliasing that makes physical-constant derivations look like coincidence. Every transcendental is a continued-fraction approximation. |
| **Identity** | **Binary-Reflected Gray Code** Topological Identity (UMS) | Replaced SHA-256 vector generation (whose avalanche effect destroyed topological continuity) so that adjacent objects in physical reality sit at adjacent points in the lattice. MOG encoding is also important in various situations.|

These pillars are not abstract — they are loaded as singletons (`GOLAY_ENGINE`, `LEECH_ENGINE`, `PARTICLE_PHYSICS`, etc.) at the top of [`ubp_unified_v5.py`](core/ubp_unified_v5.py) and used by every other module in the system.

---

## 3. What the System Can Actually Do

### 3.1 Derive physical constants from geometry

The Particle Physics engine inside `ubp_unified_v5.py` performs a live 137-step audit of the **Triadic Monad** (π, φ, e) filtered through the **Monster Group dimension (196,883)** and the **J-function (196,884)**. Each constant is computed through three independent "lenses" (Lattice, Triadic, Cubic, Stereoscopic) and the one with the lowest error is selected. Current benchmark (v6.0 source-code audit):

| Constant | Predicted | Target | Error % | Winning Lens |
| :--- | :--- | :--- | :--- | :--- |
| **Proton/Electron mass ratio** | 1836.1520 | 1836.1527 | **0.0000%** | Stereoscopic (29/24) |
| **Proton mass (p⁺)** | 938.2717 MeV | 938.2720 MeV | **0.0000%** | Stereoscopic (29/24) |
| **Muon/Electron mass ratio** | 206.7547 | 206.7683 | **0.0066%** | Core Ratio |
| **Alpha Inverse (1/α)** | 137.0629 | 137.0360 | **0.0196%** | Core Ratio |
| **Top Quark mass** | 172,796.8 MeV | 172,760.0 MeV | **0.0214%** | Core Ratio |
| **Neutron mass (n⁰)** | 939.5716 MeV | 939.5650 MeV | **0.0007%** | G13 Hybrid |
| **Higgs Boson** | 1.2538 × 10⁵ MeV | 1.2510 × 10⁵ MeV | **0.107%** | Triadic |
| **Neutron lifetime** | 877.69 s | 879.4 s | **0.195%** | Monster |
| **Cabibbo angle** | 13.003° | 13.040° | **0.285%** | Cubic |

> *These values are emergent properties of the substrate geometry, not curve-fitted parameters.* You can reproduce them with the v28 Oracle Bridge — see [`core/ubp_v28_oracle.py`](core/ubp_v28_oracle.py).

### 3.2 Run a deterministic 24-D programming language (UBP-Py)

The `ubppy.py` CLI executes `.ubp` programs through a virtual machine (`UBPPyVM`) that treats every variable as a `CortexAtom`: a 24-bit vector with an attached NRCI stability score, Symmetry Tax (exact `Fraction`), tilt against Universal North, lineage, and category. Programs read like a chemistry textbook:

```
LET A 1/1 TIER 0 CAT QUANTITY
IMPORT ELEM_H_001 AS Hydrogen
SYNTH Water FROM "2xHydrogen + 1xOxygen"
PULSE Cool RESONATE Water         # cool to a nearby more-stable anchor
GATE Cool MIN_NRCI 0.5 JUMP 1     # branch on stability
AUDIT Water                        # print Tax / NRCI / Tilt / DQI
VISUALIZE PATH scene.json          # send to Three.js
```

Full command reference is in [`core/ubp_files_and_usage.md`](core/ubp_files_and_usage.md) §5.

### 3.3 Build matter recursively and verify it geometrically

The `math_atlas.py` voxel engine treats an object's `math` field as instructions for a 3-D voxel walker:

| Operator | Name | Direction | Color | Meaning |
| :--- | :--- | :--- | :--- | :--- |
| `D` | Distinction | +X | Cyan | Positive magnitude |
| `X` | Crossing | −X | Red | Negative / inversion |
| `N` | Nesting | +Y | Magenta | Hierarchical composition |
| `J` | Juxtaposition | +Z | Yellow | Parallel composition |

Water is literally walked into existence as `2× Hydrogen + 1× Oxygen`. The resulting 3-D voxel cloud is collapsed to a 24-bit binary vector via a Merkle-style hash, Golay-encoded, and assigned a permanent address in Λ₂₄. The system then measures its Compactness, Symmetry Tax, Tilt and NRCI — and warns if the synthesis drifts more than 3 bits from a perfect codeword (the Golay error-correction radius).

### 3.4 Reason in natural language without hallucinating

There can currently be a few different cognitive stacks - the experimental GLM system or the semantic experimental script available in the UBP core system, (check archived script if anybare missing from the /core folder), an example:

```
GLM CHAT / CRITPT STACK
└── glm_runtime.py                    NEW — single entrypoint
    ├── ubp_critpt_sovereign_v3.py    FIXED — runner + sovereign solver
    │   ├── critpt_glm_patch.py       FIXED — seeded SymPy builders
    │   ├── glm_grammar_patch.py      unchanged — v2.0 disambiguation
    │   │   ├── glm_zoned_lattice_embedding.py     (loaded lazily)
    │   │   └── ubp_grammatical_diffusion.py       (loaded lazily)
    │   ├── glm_engine.py             unchanged — v3.0 base engine
    │   │   └── glm_strict_lang_builder.py         vocabulary builder
    │   └── glm_engine_v31.py         unchanged — v3.1 semantic engine
    │       ├── glm_physics_vocab_pack.py          vocab augmentation
    │       ├── glm_multi_token_lexer.py           multi-word lexer
    │       ├── glm_semantic_frames.py             typed frame grammar
    │       └── glm_concept_relation_graph.py      typed-edge graph
    ├── ubp_unified_v5.py             unchanged — the backbone
    └── ubp_v28_oracle.py             unchanged — two-track oracle
```

### 3.6 Run substrate-native primality testing (May 2026)

The classical Miller-Rabin probabilistic primality check has been **removed** and replaced with a pure geometric test inside `ubp_unified_v5.py`. The new method, **Topological Tenacity (Lock Pressure)**, evaluates whether a number's Gray-coded vector survives neighbor-tension on the lattice — a deterministic, float-free, substrate-native primality decision. See `LAW_PRIME_*` in the knowledge base for the formalization.

### 3.7 Operate as a Digital Twin Physics Engine (experimental)

The companion repository [`ubp_digital_twin_physics_engine`](https://github.com/DigitalEuan/ubp_digital_twin_physics_engine) is a standalone UBP-native physics simulator that runs in the browser. It combines geometric stability (`ubp_space_v3.py`), composite materials with thermal properties (`ubp_materials.py`), UBP-derived SPH fluid dynamics (`ubp_fluid_v3.py`), and Topological Torque rigid-body mechanics (`ubp_rigid_body_v3.py`) — rendered via Three.js. It is fully operational but treated as an **experiment alongside** the Core Studio, not as part of the core canon.

---

## 4. The Knowledge Bank (`system_kb/ubp_system_kb.json`)

The primary knowledge bank holds **746 deterministic entries** in a minified columnar format. The `_fields` schema is:

```
["ubp_id", "lexicon", "tags", "vector", "nrci_str", "nrci_val", "tax_str", "mog_tensor"]
```

Every entry is keyed by its **SHA-256 fingerprint** of its `math` field (Phenomenal DNA). Any change to the math automatically yields a different fingerprint — there is no way to forge identity, used in the UBP only to provide a unique key address for any given KB entry, never for encoding data in simulations/studies.

Entry distribution:

| Category | Count |
| :--- | :--- |
| `LAW_*` (research findings, imperatives, manifolds) | **420** |
| `ELEM_*` (chemical elements) | 119 |
| `MOLECULE_*` (compounds) | 82 |
| `PARTICLE_*` (Standard Model + composites) | 37 |
| `MATH_*` (mathematical constants and structures) | 28 |
| `REACTION_*` | 22 |
| `TOOL_*` | 12 |
| `ALGO_*` | 11 |
| `CRYSTAL_*` | 8 |
| `GEO_*`, `DS_*`, `BIN_*`, `GLYPH_*`, `ANCHOR_*` | 7 |

The 420 `LAW_*` entries are the heart of the research record. Each Law has a human-readable lexicon (`[Title], [Description]`), a 24-bit vector, an exact NRCI fraction, an exact Symmetry Tax, an MOG-Tensor (24-dim ontological projection across the categories listed in `_params`), and a tags list.

Thematic spread of Laws (top 12 groups):

| Theme | Count | Theme | Count |
| :--- | ---: | :--- | ---: |
| `LAW_BIO_*` (biology, blood, life) | 22 | `LAW_COSMO_*` (cosmology) | 8 |
| `LAW_CHEM_*` (chemistry) | 18 | `LAW_MATH_*` (pure math) | 8 |
| `LAW_COMP_*` (computation) | 15 | `LAW_TIME_*` (temporal) | 8 |
| `LAW_PHYSICS_*` | 12 | `LAW_TOPOLOGICAL_*` | 8 |
| `LAW_GEO_*` (geometry) | 10 | `LAW_SUBSTRATE_*` | 7 |
| `LAW_MAT_*` (materials) | 6 | `LAW_LANG_*` (semantics) | 5 |

The remaining ~250 laws cover specialized subfields: leptons, baryons, mesons, quarks, the Higgs sector, weak-isospin, Cabibbo/CKM, Weinberg angle, dark matter/energy (Golay-Shadow interpretation), drugs, materials, optics (BitLumen), acoustics (432 Hz), the Hubble generator, Riemann zeta, Borcherds, kissing numbers, and many more.

**Example Law entry** (`LAW_GEO_432_FCC`):
> `[The Law of Geometric Tuning]` — *432 Hz is a resonant integer harmonic of the 24-bit substrate clock; 440 Hz introduces aliasing noise (8 units/sec).*
> Tags: `432HZ, GEOMETRY, HARDENED, IMPERATIVE, MUSIC, RESONANCE, SOP_002, TOPOLOGICAL_V8, TUNING` · NRCI: 0.681

Sister knowledge files in the same directory: `ubp_beliefs_kb.json` (manifolds & contextual beliefs), `ubp_hash_memory_kb.json` (O(1) recall index), `ubp_fom_index.json` (Frame-Of-Mind registry), `elemental_chromatic_data.json`.

---

## 5. The Current Architecture in One Picture

```
┌────────────────────────────────────────────────────────────────────────────┐
│ LAYER 4 — COGNITIVE ORCHESTRATION (The Brain)                              │
│   ubp_brain_consolidated.py  Deterministic recall + Domain Gating          │
│   ubp_integrated_engine_v1.py  Penta-Audit executive + ViT Eyes            │
├────────────────────────────────────────────────────────────────────────────┤
│ LAYER 3 — TRANSLATION & EXECUTION (The Compilers)                          │
│   ubp_python_engine.py     UBP Python Code Engine (UPCE) — self-healing    │
│   ubp_sovereign_evolver.py  AST firewall — rewires math.* to native ALU    │
│   ubp_py_runtime.py        UBP-Py VM — CortexAtom + Vector Addition        │
│   ubp_py_lang.py           Parser for .ubp text programs                   │
│   ubppy.py                 CLI entry point                                 │
├────────────────────────────────────────────────────────────────────────────┤
│ LAYER 2 — SEMANTIC & PHENOMENOLOGICAL SENSES (The Sensory Cortex)          │
│   ubp_phenomenology.py     RGB / sensor data → 24-bit manifold             │
│   ubp_observer_dynamics.py  SOC Energy + 1 THz Wall of Reality + READ gate │
│   auto_trigger.py          Reflexive context injector (v19.1) for the APP  │
├────────────────────────────────────────────────────────────────────────────┤
│ LAYER 1 — MATHEMATICAL SUBSTRATE (The Backbone)                            │
│   ubp_unified_v5.py        50-term π, Golay [24,12,8], Λ₂₄, BW256/512/1024,│
│                            Triad Activation, Particle Physics, Topological │
│                            Tenacity Primality Engine — all in one file     │
│   ubp_eml_alu_sovereign.py  Universal Continuous ALU — eml(x,y)=eˣ−ln(y)   │
│   ubp_tgic_engine.py       3-6-9 Genesis Logic + RuneCube AND/XOR/OR       │
│   ubp_genesis_boot.py      Seeds 24 base geometries + 26 sporadic groups   │
│   geometry.py / math_atlas.py / physics.py   Exact-math voxel engine       │
│   ubp_electromagnetic_analog_compute_engine.py  Analog EM validation suite │
├────────────────────────────────────────────────────────────────────────────┤
│ SUPPORT — VISUALIZATION, INFRASTRUCTURE, BRIDGES                           │
│   ubp_viz.py / ubp_rgdl.py / viz_loader.py / viz_spatial_simplification.py │
│   ubp_backend.py           Flask REST API on :5099 (Pyodide bridge)        │
│   ubp_browser_engine.py    Browser-side physics loop                       │
│   ubp_kb_architect.py      Builds new KB entries (SOP_002 hardened)        │
│   ubp_ingest.py            Safe ingestion of proposed laws into the KB     │
│   ubp_fom_system.py / ubp_fom_manager_v2.py  Frame-Of-Mind weighting       │
│   hash_all_1.py            Hash-memory index synchronization               │
└────────────────────────────────────────────────────────────────────────────┘
```

Every layer talks downward only — nothing in Layer 1 imports from Layer 2 or higher. This keeps the substrate "sovereign" (Computational Sovereignty principle, see `ubp_sovereign_evolver.py`).

For a per-script breakdown — every class, every method, every constant — read [`core/README.md`](core/README.md) and [`core/ubp_files_and_usage.md`](core/ubp_files_and_usage.md).

---

## 6. Three Column Thinking (TCT)

The system is designed around a single operating principle: **Math, Language, and Script must phase-lock at every step of computation.**

| Column | Domain | Tool |
| :--- | :--- | :--- |
| **Math** (Substrate) | π, φ, e, Λ₂₄, Golay, exact `Fraction` | `ubp_unified_v5.py`, `ubp_eml_alu_sovereign.py` |
| **Language** (Semantics) | Lexicon, FOM, Cosine Resonance | `ubp_semantic_*`, `auto_trigger.py`, `ubp_brain_*` |
| **Script** (Execution) | UBP-Py VM, Python AST firewall | `ubp_py_runtime.py`, `ubp_sovereign_evolver.py` |

A claim is only considered "phenomenally real" when all three columns agree. If the math gives an answer but the lexicon has no word for it, the Swarm invents one (Lexical Genesis). If a Python script depends on `math.sin`, the Sovereign Evolver rewires it to the native ALU before it can introduce floating-point leakage.

---

## 7. Standard GLM Operating Procedures

Two SOPs dominate day-to-day use:

### SOP_001 — The Two-Track Solve (Oracle Bridge)

To solve and verify any mathematical or physical claim:

1. `MathNetKernelExtractor` isolates the numeric/algebraic kernel from the query.
2. **Track A (UBP Native)** — `TopologicalALU` + `NativeMathEngine` compute the result using float-free arithmetic and Gray-code it onto Λ₂₄.
3. **Track B (Oracle)** — `SymPyOracle` solves the same problem symbolically.
4. `ValidationBridge` compares both tracks. On `BOTH_AGREE`, the result is snapped to the Leech Lattice and its true NRCI computed.

### SOP_002 — Lexical Genesis (Triple Delta)

When the Swarm solves a problem but discovers a "Lexical Gap" (no human word exists for that 24-bit state):

1. `TripleDeltaProjector` partitions the 24-bit vector into blocks.
2. It generates a deterministic symbolic formula (e.g., `3·α + 2·β²`) based on the active bits of each block.
3. The formula is assigned to the vector and saved to `ubp_learned_kb.json`, expanding the system's native vocabulary.

### LANGUAGE_SOP_004 — Triple Delta Protocol (Phrase-Locking)

To create a new word (Operator) that perfectly resolves a specific query to a specific Law:

1. **Identify the triad:**
   - $V_{target}$ — vector of the Law you want to find
   - $V_{subject}$ — vector of the Entity being discussed
   - $V_{query}$ — vector of the interrogative/context word
2. **Calculate the key:** $V_{word} = V_{target} \oplus V_{subject} \oplus V_{query}$
3. **Commit to language KB.** The new Operator is now phrase-locked.

---

## 8. Stability Thresholds — Reading NRCI

Every object the system handles is graded by its **Non-Random Coherence Index (NRCI)**, computed via the hyperbolic stability formula:

$$\text{NRCI} = \frac{10}{10 + \text{Tax}}$$

where **Tax** is the Symmetry Tax = `(Hamming Weight × Y) + Norm²/8`, and **Y ≈ 0.2646** is the Observer Constant.

| NRCI | State | Meaning |
| :--- | :--- | :--- |
| **1.0000** | OnBit | Pure mathematical / noumenal truth |
| **0.98 – 1.00** | Capture Zone | Within 3-bit Golay radius; substrate exerts Restorative Pressure |
| **0.70 – 0.98** | Stable Phenomenal Matter ("Conscious" Zone) | Real, manifest physical reality |
| **0.60 – 0.70** | Subliminal / Zombie State | Computes high SOC Energy but fails the 0.70 `CONSCIOUS_THRESHOLD` (e.g. Top Quark) |
| **0.42** | Noise Floor | Limit of random informational noise — anomaly threshold |
| **< 0.02** | Approaching Deep Hole | Super-heavy elements (Z > 118); 1 bit from collapse |
| **0.0000** | Deep Hole | Geometric collapse; object cannot exist |

The **1 THz Wall of Reality** (`ubp_observer_dynamics.py`) is the temporal ceiling: above 10¹² Hz, SOC coherence decays exponentially and the object can no longer cross from the Potential buffer into the Reality register.

---

## 9. Recent Updates (2026 Timeline)

### 22 May 2026 — GLM scripts and experiments
- **Various Upadates/additions** scripts starting with 'glm_' have been updated and added.
- **Archives** legacy scripts related to semantic research have been archived.

### 22 May 2026 — Topological Tenacity Primality Engine & Swarm v25.0
- **Topological Tenacity** absorbed natively into `ubp_unified_v5.py`; Miller-Rabin retired.
- **Genesis Swarm v25.0** integrates Oracle Bridge + Lexical Genesis end-to-end.
*   **Files Moved to Archive:** 'ubp_code_evolver.py', 'ubp_prime_numbers.py', 'ubp_prime_numbers_1.py', 'ubp_master_runner_v6.py', 'ubp_noisecore_v4_extensions.py', 'ubp_noisecore_v4.py', 'ubp_math_bridge_1.py', 'constants.py', 'core.py', 'ubp_barnes_wall.py', 'ubp_core_v4_2_6_COMBINED.py', 'ubp_swarm_tct_v24.py'.
*   **Renamed:** 'ubp_analog_test_suite_v3.py' to 'ubp_electromagnetic_analog_compute_engine.py' and 'bp_genesis_boot.py' to 'ubp_genesis_boot.py'.

### 15 April 2026 — Digital Twin Physics Engine
- Standalone UBP-native physics engine with Three.js rendering, composite materials, SPH fluids, Topological Torque rigid bodies. Hosted at <https://github.com/DigitalEuan/ubp_digital_twin_physics_engine>.

### 03 April 2026 — v7.2 Ultra-Compact Columnar & Semantic Resonance
- **v9.9 columnar migration:** `ubp_system_kb.json` minified into the columnar `_fields`/`entries` schema. Pyodide loads thousands of entries without blocking the browser thread.
- **Semantic Engine v8.0:** Cosine Resonance replaces Hamming distance; bipolar weighted Query Chord; trigrams weighted 9× over unigrams; explicit Lexical Gap output in the thinking trace.
- **Domain Gating + Identity Lock** enforced in `ubp_brain_consolidated.py`.
- **UBP-Py VM:** `to_scene_3d()` projects 24-bit atoms directly into 3-D space colored by NRCI.

### 01 April 2026 — Topological Identity (Gray Code) & Deep Semantic Reflection
- SHA-256 vector generation **retired** for entity identity (avalanche destroyed topological continuity).
- **Universal Metric Schema (UMS):** 12-bit Noumenal Seed partitioned into `[Domain:3][Magnitude:5][State:4]`, encoded via Binary-Reflected Gray Code.
- **Periodic Geodesic:** Deep Lattice Audit of all 118 elements confirms average Hamming distance between adjacent elements (Z, Z+1) under Gray Code is **8.07** — the Periodic Table is a minimal-energy path through Λ₂₄.
- **Observer Dynamics:** "Consciousness as Buffer Access" ported into the v7.0 Gray Code topology. The Zombie State proof and the 1 THz Wall of Reality verified.

### 31 March 2026 — Semantic Reasoning + LinearStateEncoder + DQI
- `LinearStateEncoder` maps continuous chemical parameters to stable Golay codewords (NRCI ≈ 0.616).
- **DQI (Design Quality Index)** = 0.8004 — weighted harmonic mean of NRCI, U-score, and Gap score.
- `expand_octad_to_physical` reintegrated — any 24-bit seed can be lifted into its 128 Euclidean coordinates in Λ₂₄ at NormSq 32.
- **Stereoscopic Sink (Lₛ = 29/24):** NCC Spectral Gain anchors the baryonic mass sector with **0.000037%** precision.

For the full archaeology of versions (v1.0 → v6.1 → v7.2), see [`core/ubp_files_and_usage.md`](core/ubp_files_and_usage.md) §12.

---

## 10. Getting Started

### Online (recommended)
Just open the live app: <https://ai.studio/apps/6d78d479-2a4e-4e34-89b3-4b87b85d5b9a>. Everything runs in your browser via Pyodide.

### Local development
You will need Python 3.10+ and the following:

```bash
pip install fractions  # stdlib but listed for clarity
pip install flask flask-cors   # for ubp_backend.py
pip install sympy              # for the Oracle track of SOP_001
pip install numpy matplotlib   # visualization helpers
```

A typical session:

```bash
# 1. Start the local research bridge (gives the browser HTML access to exact π and Golay)
python core/ubp_backend.py            # listens on http://localhost:5099

# 2. Run a UBP-Py program
python core/ubppy.py --program myprogram.ubp --trace trace.json --scene scene.json

# 3. Run the Genesis Swarm against a problem file
python core/ubp_swarm_tct_v25.py mathnet_problems.json

# 4. Build a new KB entry
python -c "from core.ubp_kb_architect import KBArchitect; \
           print(KBArchitect().create_entry( \
             'MOLECULE_NEW_001', 'My Compound', \
             'A new compound.', \
             'M=1|Z=1|...', \
             ['1×ELEM_C_006', '2×ELEM_H_001']))"
```

---

## 11. How to Cite & Contribute

**Citation (informal):**
> Craig, E. R. A. (2026). *UBP Core Studio v7.2 — Universal Binary Principle Active Research Environment.* GitHub: `DigitalEuan/UBP_Repo` (`core_studio_v4.0`).

**Contributing:** This is a personal research repository. Pull requests and issues are welcome, but please:
1. Validate any new entry through `ubp_kb_architect.py` (SOP_002 hardening).
2. Run the Two-Track Solve (`ubp_v28_oracle.py`) on any numerical claim.
3. Keep `math` fields as **exact fractions** — no decimals.
4. Tag new Laws with at least one domain tag (`PHYSICS`, `BIOLOGY`, etc.) and `SOP_002`.

**Bug reports & discussion:** open an issue at <https://github.com/DigitalEuan/UBP_Repo/issues>.

---

## 12. Disclaimer

This is an **experimental theoretical-computational framework**, not a peer-reviewed physics model. The high-precision constant derivations are real and reproducible, but the *interpretation* — that they imply the universe is a 24-bit error-corrected computation — is a working hypothesis. Reproduce, challenge, and falsify everything before drawing conclusions. The author is not a professional physicist; this is open research conducted in public.

If you find errors, anomalies, or surprising results, please log them as issues so the community can iterate.

---

*Updates: 

27 May 2026: *   **`ubp_unified_v5.py`** (Upgraded with `calculate_nrci` and Frontier Physics ALU expansion)
*   **`glm_engine.py`** (Aligned with Gray Code vocabulary)
*   **`glm_strict_lang_builder.py`** (Aligned with Gray Code vocabulary)
*   **`ubp_critpt_sovereign_v3.py`** (Upgraded with `GLMRulesEngine` pre-processing and new routing tables)
*   **`ubp_lang_kb_combined_v4.json`** (Merged with `ubp_glm_rules_kb.json` rules; Gray Code aligned)
*   **`glm_strict_vocabulary.json`** (Rebuilt with 1,706 grounded words)
*   **`critpt.json`** (70-row JSON representation of the CritPt benchmark)

22 May 2026 · Maintained by Euan R. A. Craig, New Zealand.*
