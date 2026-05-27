# UBP Core Studio v7.2 — `/core/` Directory Reference

**Author:** Euan R. A. Craig, New Zealand
**Version:** 7.2.0 (Genesis Edition)
**Date:** 27 May 2026
**Scope:** This document is the per-script reference for everything inside `core_studio_v4.0/core/`.

> For the high-level overview of what UBP **is**, see the parent [`README.md`](../README.md).
> For day-to-day operational SOPs and the UBP-Py language reference, see [`ubp_files_and_usage.md`](ubp_files_and_usage.md).
> For the philosophical and mathematical foundations (Y-constant, Triadic Monad, Octad, SOP_002, Barnes-Wall macro-bulk, full v5.8/v6.0/v6.1 formalism), see the comprehensive guide at [`../system_kb/ubp_files_and_usage.md`](../system_kb/ubp_files_and_usage.md).

---

## 0. How to Read This Document

The `/core/` directory contains the live runtime of UBP Core Studio v7.2. Files are grouped into the four architectural layers introduced in the parent README, plus a support tier:

```
LAYER 4 — COGNITIVE ORCHESTRATION
LAYER 3 — TRANSLATION & EXECUTION
LAYER 2 — SEMANTIC & PHENOMENOLOGICAL SENSES
LAYER 1 — MATHEMATICAL SUBSTRATE
SUPPORT — Visualization · Infrastructure · Bridges · Data
```

For each script we document:
- **Purpose** — what the script does in one sentence
- **Classes & key methods** — the actual public surface
- **Key constants** — singletons and tunable values defined at module level
- **How it stacks** — its upstream dependencies and downstream consumers

Every code reference is taken directly from the source as of 22 May 2026.

---

# LAYER 1 — Mathematical Substrate

These modules implement the **float-free backbone**. They depend on nothing in Layers 2–4. Everything else in the system imports from here.

## `ubp_unified_v5.py` — *The Backbone* (3,409 lines)

**Module docstring (excerpt):**
> UBP UNIFIED v5.2 — HARDENED TRIAD-PHYSICS EDITION (FLOAT-FREE CORE). Upgraded from v6.0 to preserve workspace import compatibility. Includes ExactRoot.denest, AdaptiveManifold, and NeuralPatternDetector. THE MERGE: This single self-contained module unifies three previously-separate scripts: (1) `core.py` — UBP Core v6.1 Triad / Particle Physics / Construction; (2) `ubp_noisecore_v4.py` — Noise-Core v4.0 Triad ALU / Substrate / Tests; (3) `ubp_noisecore_v4_extensions.py` — Physics ALU / Linear Algebra ALU / MathNet Runner.

This is the largest and most important file in the system. It defines **28 classes** that act as singletons providing all foundational mathematics. Major classes:

| Class | Role |
| :--- | :--- |
| **`ExactMath`** | Float-free integer & rational mathematics. `isqrt`, `ilog`, `iceil_div`, `igcd`, `ifact`, `icomb`, `sqrt_frac` (Newton on rationals to arbitrary precision). |
| **`ExactRoot`** | Symbolic representation of `coef · √radicand` with `Fraction` internals; supports `.denest(p,q,c)`, arithmetic, comparison, hashing. |
| **`UBPUltimateSubstrate`** | Ultimate-precision constants. `get_pi(terms=50)` returns the 50-term continued-fraction π as a `Fraction`. `get_constants(precision)` returns `{π, e, φ, Y, …}`. `get_v6_constants()` adds v6.0 additions. |
| **`BinaryLinearAlgebra`** | All operations modulo 2 — no floats anywhere. `hamming_weight`, `hamming_distance`, `matrix_vector_multiply`, `matrix_multiply`, **`fold24_to3`** (LAW_GEO_FOLD_001 recursive pairwise XOR collapse 24 → 12 → 6 → 3). |
| **`GolayCodeEngine`** (singleton: `GOLAY_ENGINE`) | Extended Binary Golay [24,12,8]. `encode(msg12)`, `syndrome(v24)`, `syndrome_weight`, `decode(v24)`, `snap_to_codeword(v24)`, `get_all_codewords()`, `get_octads()`, `get_random_octad(seed_int)`, `get_shadow_metrics()`. |
| **`LeechPointScaled`** | Dataclass for a Λ₂₄ point in scaled integer coordinates (each entry × √8 in physical). |
| **`LeechLatticeEngine`** (singleton: `LEECH_ENGINE`) | 100% `Fraction` arithmetic. `expand_octad_to_physical(octad)` lifts a 24-bit codeword into its **128 Euclidean coordinates** (NormSq 32). `calculate_symmetry_tax(point, compactness)` implements **LAW_SYMMETRY_001**: `Tax = HW·Y + Norm²/8`. `ontological_health`, `rank_by_stability`, `nearest_octad_idx(seed24)`. |
| **`MonsterGroup`** | All 26 sporadic simple groups + Triad activation logic. `happy_family()`, `pariahs()`, `walk(seed_idx, count)`, `triad_state(stable_count, sporadic_count)`. |
| **`BarnesWallEngine`** | Generalized Barnes-Wall engine for any power-of-two dimension ≥ 32. `generate(seed, dim)`, `snap(macro)`, `nrci(macro)`, `audit(fingerprint, micro_nrci, dim)`. Used for **BW₂₅₆** macro-bulk computations. |
| **`GolaySubstrateStub`** + **`SubstrateLibrary`** + **`NoiseCellV3`** + **`NoiseRegisterV3`** + **`SubstrateCalibrator`** | The base-12 / displacement-curve substrate from the merged `ubp_noisecore_v4.py`. Auto-expanding base-12 registers with empirical displacement-curve calibration. |
| **`ConstructionPrimitive`** + **`ConstructionPath`** + **`UBPObject`** | Datatypes for recursive object synthesis. `ConstructionPath._calculate_tax()` computes the cumulative Symmetry Tax along a build path; `is_oscillatory()` detects D/X cycles. |
| **`TriadActivationEngine`** | Triad Activation: Golay → Leech → Monster. `seed_primitives(verbose)`, `activate(max_iter, verbose)`, `export_atlas(filename)`. Boots a primitive atlas from the substrate. *Note: the active-mode version of this engine has moved into `ubp_genesis_boot.py`.* |
| **`UBPSourceCodeParticlePhysics`** (singleton: `PARTICLE_PHYSICS`) | Source-Code Particle Physics v6.2 with **Stereoscopic Sink (29/24)**. `get_ultimate_predictions()` returns the full constant audit. |
| **`LinearStateEncoder`** | SOP_002 — encodes continuous chemical/physical parameters into the 24-bit Golay manifold via Gray-code partitioning. Returns a stable codeword. |
| **`UBPQualityMetrics`** | **Design Quality Index (DQI)** — weighted harmonic mean of NRCI, U-score, Gap-score. Returns `Fraction`. |
| **`AdaptiveManifold`** + **`NeuralPatternDetector`** | Pattern-detection helpers. `fingerprint(value)` adapts bit-width up to `max_bits`. |
| **`ParallelUBP`** | Multiprocessing worker pool. `process_batch(tasks)`. |
| **`NoiseALU`** | Arithmetic Logic Unit; every result carries a UBP fingerprint. **30+ methods**: `add`, `sub`, `mul`, `divmod_`, `gcd`, `lcm`, `modpow`, `factorial`, `fibonacci`, `detect_pattern`, … |
| **`PhysicsALU`** | Physical-law ALU using exact `Fraction` / `ExactRoot`. `kinematics_displacement`, `schwarzschild_radius`, `lorentz_factor`, `escape_velocity`, `photon_energy`, `compton_wavelength`. |
| **`LinearAlgebraALU`** | Float-free 2×2 / 3×3 / n×n determinants (Bareiss algorithm for general n). |
| **`MathNetNoiseRunner`** | Routes natural-language style problems to the appropriate ALU operation. Used by the swarm orchestrator. |

**Module-level functions:**
- `to_gray_code(n, bits)` — Binary-Reflected Gray-code encoder.
- `ubp_fingerprint_logic(val)` — Lightweight UBP fingerprint (Golay snap + lattice classification).
- `run_tests(verbose)` — Multi-perspective comprehensive test suite for the whole module.
- `run_all(output_path, report_path)` — Master test runner producing JSON + Markdown report.

**Topological Tenacity Primality Engine (May 2026)** — Now built into this file. Replaces Miller-Rabin with a pure substrate-native test based on **Lock Pressure** and **neighbor-tension** along the Gray manifold.

**Used by:** every other script in the system. Imports from this file are exclusively *downward* — never the reverse.

---

## `ubp_eml_alu_sovereign.py` — *Universal Continuous ALU v9.2* (255 lines)

**Module docstring:**
> ZERO DEPENDENCIES: No math, no cmath, no numpy. All transcendental functions implemented via Taylor / Newton / Lanczos series. Supports complex numbers and automatic differentiation via Dual. Core projection: `eml(x, y) = exp(x) − ln(y)`. Inspired by *"All elementary functions from a single operator"* (Odrzywolek).

The Sovereign ALU. Derives the **Triadic Monad** and exact particle masses purely from the projection `eml(x,y) = eˣ − ln(y)` without external floating-point libraries.

| Class | Role |
| :--- | :--- |
| **`Dual`** | Automatic differentiation via dual numbers. Supports `__add__, __sub__, __mul__, __truediv__, __pow__, __neg__`. `__init__(real, deriv)`. |
| **`GrandUnifiedEmlALU`** | The ALU itself. Public methods: `eml(x,y)`, `exp(x)`, `ln(x)`, `add`, `subtract`, `mul`, `div`, `sqrt`, `sin`, `cos`, `pow`, plus the **Grand Audit** that verifies internal consistency. |

**Pure helper functions** (no imports outside the stdlib): `_pure_exp(z, terms)`, `_pure_ln(z, iterations)`, `_pure_sqrt(z, iterations)`, `_pure_sin(z, terms)`, `_pure_cos(z, terms)`, `run_grand_audit()`.

**How it stacks:** `ubp_sovereign_evolver.py` rewires Python AST nodes (`math.sin`, `math.exp`, etc.) onto this ALU at parse time. The two files together form the **Computational Sovereignty firewall** — no externally-compiled floating-point math can leak into substrate calculations.

---

## `ubp_tgic_engine.py` — *TGIC v6.4 (Genesis Edition / RuneCube)* (205 lines)

**Module docstring:**
> The definitive TGIC implementation. Integrates all 9 internal interactions + Cross-Node Relational Gravity. STANDARDS: Internal Harmony (9 pairwise interactions across X, Y, Z blocks); External Harmony (Relational Pull, Hamming-weighted attraction); Hardware (Leech Tax + Coherence Pressure d>3 penalty).

Implements **3-6-9 Genesis Logic** (Tesla's triad realized on the substrate):

| Class | Role |
| :--- | :--- |
| **`TGICConstraintSystem`** | The Genesis Logic. `check_3_axis_orthogonality(v)` (ideal: Hamming distance 4 between 8-bit blocks); `check_6_face_coherence(v, engine)` (stability of the 6 interaction faces); `check_9_neighbor_limit(target_v, manifold_vectors)` (prevents "overheating" if neighbors > 9). |
| **`OffBit`** | A single phenomenal bit slot with phase. `with_updates(new_v, delta_phi)`. |
| **`TGICInteractionEngine`** (v6.3 RuneCube) | The 9-fold interaction engine. `calculate_total_stability(v, manifold_vectors)` runs the master 3-6-9 audit. Three RuneCube ops: `rune_resonance_xy(v)` (AND), `rune_entangle_xz(v)` (XOR), `rune_expand_yz(v)` (OR). Plus `resonance_op`, `entanglement_op`, `superposition_op`, `mixed_op`, `_snap(v)` (internal Lattice Snap for immortality), `calculate_internal_cost(v)`. |
| **`TGICExactEngine`** | Full TGIC engine with cross-node gravity. `get_relational_pull(coord_target, v_target, S)`, `get_node_energy(coord, v, S)`, `step(S)`, `get_total_energy(S)`. |

**Stack position:** TGIC is the *interaction* layer of Layer 1. Every internal bit-flow is protected by a mandatory Lattice Snap, ensuring simulations remain within the Golay correction radius. Node energy is **Identity-Aware** — it calculates the restorative pressure required to maintain structural integrity, not just raw potential.

---

## `ubp_genesis_boot.py` — *Genesis Boot Engine v7.0 (Topological)* (206 lines)

**Module docstring:**
> Replaces the legacy `TriadActivationEngine`. Boots the 24-bit universe from scratch using **Gray Code Topological Identity**. Phases: (1) Seeding — injects 24 base geometries and 26 sporadic groups; (2) Activation — slides unstable objects along the Gray manifold until they resonate at a stable Leech Lattice coordinate (Weight 8, NRCI 0.7–0.8); (3) Export — generates the foundational `genesis_atlas.json`.

| Class | Role |
| :--- | :--- |
| **`UBPBootObject`** | A foundational entity during Genesis Boot. `update_vector()` generates the 24-bit coordinate via Gray Code UMS. `is_stable()`, `decompose()` (Topological Decomposition), `to_dict()`. |
| **`GenesisBootEngine`** | The boot orchestrator. `seed_primitives()`, `activate(max_iter)`, `_update_triad_state()`, `_is_fully_active()`, `_print_status()`, `export()`. |

**Module function:** `to_gray(n, bits)` — standard Binary-to-Gray-code conversion.

**Stack position:** Called once per system startup to produce `genesis_atlas.json` — the authoritative seed of the 24 base geometries (Needham Triad + their compositions) and the 26 sporadic groups (Happy Family + Pariahs). Other modules read from this atlas rather than re-deriving primitives at runtime.

---

## `geometry.py` — *Condensed Geometry Module* (340 lines)

**Module docstring:** *UBP Condensed Module: geometry.*

Self-contained subset of `math_atlas.py` + the `HexDictionaryV4Exact` memory system. Used when a script needs the voxel walker but does not want to pull in the entire MathAtlas.

| Class | Role |
| :--- | :--- |
| **`HexDictionaryV4Exact`** | Symbolic-hash memory. `_int_to_gray(n, bits)` (Gray code ensures similar volumes get similar bit patterns); `_get_domain_for_id(ubp_id)`; `_measure_topology(math_dna)` (SYMBOLIC HASHING — extracts topological features from the math string); `mint_rational_vector(ubp_id, math_dna)` projects a vector from the spatial properties of the math; `load_memory(filepath)`, `find_by_id(ubp_id)`, `get_vector(ubp_id)`. |
| **`MathAtlasConstants`** | Ultra-high-precision constants. `get_pi`, `get_e`, `get_phi`, `get_sqrt(n)` — all return `Fraction`. |
| **`ConstructionPath`** | Specific geometric construction for a MathObject. `_build(offset)` walks the voxel cloud. |
| **`MathObjectV4`** | Rich object record. `add_path(primitives, method)`, `get_canonical_path`, `get_vector`, `get_charge`, `get_recursive_math()` (builds the full embedded math string), `calculate_compactness()` (3-D efficiency of the voxel cloud), `get_nrci()` (v6.0 unified stability formula incorporating compactness rebate). |
| **`ExactRationalEncoder`** | Custom `json.JSONEncoder` that serializes `Fraction` as a fraction string rather than a float. |

**Module constants:**
- `HEX_DB_EXACT = HexDictionaryV4Exact()` — global memory singleton.
- `UNIVERSAL_NORTH = [-0.30656966974248284, -0.9197090092274486, 0.2452557357939863]` — the orientation toward Truth in the 3-D projection.
- `PI = MathAtlasConstants.get_pi()`, `E`, `PHI`, `Y_CONST = 1 / (PI + 2/PI)`.

---

## `math_atlas.py` — *The Voxel Engine* (231 lines)

**Module docstring:**
> MathAtlas v4.0 — The Definitive Mathematical Substrate. Consolidated from v1.3, v2.0, and v3.0. "Every object is a recursive construction of its own history."

The voxel walker. Treats the `math` field as instructions for a 3-D Voxel Walker starting at origin (0,0,0), using four geometric primitives:

| Operator | Name | Direction | Color | Meaning |
| :--- | :--- | :--- | :--- | :--- |
| `D` | Distinction | Forward (+X) | Cyan | Positive magnitude |
| `X` | Crossing | Backward (−X) | Red | Negative magnitude / inversion |
| `N` | Nesting | Up (+Y) | Magenta | Hierarchical composition / rational division |
| `J` | Juxtaposition | Out (+Z) | Yellow | Parallel composition / list of dimensions |

Classes mirror those in `geometry.py` (this file is the canonical source); see above.

**Key insight:** Once the crystal is built, MathAtlas calculates Symmetry Tax and NRCI, then converts the 3-D voxel cloud to a 24-bit binary vector via a Merkle-style hash — assigning the object a permanent address in Λ₂₄. This is the bridge between *physical recipe* (math DNA) and *geometric identity* (24-bit address).

---

## `physics.py` — *Coherence & Holographic NRCI* (144 lines)

| Class | Role |
| :--- | :--- |
| **`CoherenceRegime`** (Enum) | Named regimes (e.g., NOISE, STABLE, COHERENT, OnBit). |
| **`UBPConstantsExact`** | `pi()`, `observer_fixed_point()` (= π + 2/π), `y_constant()` (= 1 / (π + 2/π)). |
| **`UBPObserverExact`** | The Observer. `get_base_cost()` (cost of frame existence), `calculate_realm_cost(realm_complexity, dimensions)`. |
| **`UBPCoherenceExact`** | `calculate_holographic_nrci(tax, constants)` implements **LAW_HOLO_BOUND_001 v6.4** Refined Holographic NRCI. `clamp01(x)`, `calculate_nrci(observed_variance, theoretical_variance)`, `get_regime(nrci_value, target)`. |
| **`UBPMetricsExact`** | `analyze_state(variance, realm, is_quantum)` — returns a full state report. |

**Module helpers:**
- `_cf_to_fraction(a)` — Convert continued-fraction coefficients to an exact `Fraction`.
- `pi_approx(terms)` — Deterministic rational approximation of π using `terms` CF coefficients.

**`_PI_CF`** constant: the first 26 continued-fraction coefficients of π, used for the float-free π.

---

## `ubp_electromagnetic_analog_compute_engine.py` — *Analog Test Suite v3* (235 lines)

**Module docstring:**
> UBP Electromagnetic Analog Compute Engine — Comprehensive Validation. (Renamed from `ubp_analog_test_suite_v3.py`.) Fixes: (1) scaling logic for MUL/DIV/SQRT to match physical domain transformations; (2) increased `V_REF` to 100.0 to handle larger chained values (e.g. 64.0) without clipping; (3) JSON serialization fix for Enum types.

Validates that UBP arithmetic can be performed via **orthogonal electromagnetic field interactions** — a physical implementation of the substrate.

| Class | Role |
| :--- | :--- |
| **`OpCategory`** (Enum) | Op categorization for the suite. |
| **`TestResult`** | Dataclass for a single test outcome. |
| **`UBPAnalogTestSuite`** | The validator. Public ops: `op_add`, `op_sub`, `op_mul`, `op_div`, `op_sqrt`, and the support `_to_analog(val)` (scale real → analog voltage [−1.0, 1.0]), `_from_analog(val)` (scale back), `_compute_symmetry(e, m, phase_diff)`. Each op encodes a geometric transformation: `op_add` is a 45° projection `(E+M)/√2`; `op_sub` is a 180° M-field phase inversion; `op_mul` is analog voltage multiplication. |

**Stack position:** Standalone validation. Confirms that UBP operations are physically realizable as EM field manipulations — important for downstream hardware speculation but not used at runtime by other modules.

---

# LAYER 2 — Semantic & Phenomenological Senses

These modules **read** the substrate (sensory data → 24-bit vectors) and **reflect** on it (lattice-snaps, internal dialogue, observer dynamics).

## `ubp_semantic_engine.py` — *Cosine-Resonance Semantic Engine v8.0* (177 lines)

| Class | Role |
| :--- | :--- |
| **`SemanticResult`** | Result of a semantic query. `summary()` produces a human-readable string. |
| **`UBPSemanticEngine`** | The engine. `load(system_path, lang_path)`, `_build_indexes()`, `_cosine_similarity(v1, v2)` (replaces raw Hamming distance — finds deep conceptual alignments even when bit-matches fail), `_reflect_meaning(vector)` (generates a textual "thinking trace"), `query(text, top_k)`, `query_display(text)`. |

**Inside `query`:**
- Builds a weighted bipolar "Query Chord" by averaging token vectors of n-grams.
- **Trigrams carry 9× the weight of unigrams** — ensures "Fine Structure Constant" resolves to its true Law rather than being scattered by `OP_LIGHT` or similar.
- Ranks all KB entries by Cosine Resonance with the chord.
- Output includes both the top matches *and* the identified Lexical Gaps where physical laws lack adequate human vocabulary.

---

## `ubp_semantic_sovereign.py` — *Sovereign Semantic Engine* (83 lines)

**Module docstring:**
> Absorbs the advanced Lattice-Snap and Triple Delta Protocol from the CritPt runner. Allows the Semantic Engine to verify the physical reality of queried concepts.

| Class | Role |
| :--- | :--- |
| **`SovereignSemanticAuditor`** | Performs the "Lattice Snap" on any mathematical/physical value. `to_gray_code(n, bits)`, `audit_value(value)` returns NRCI + snap distance + verdict. |
| **`TripleDeltaProjector`** | Implements the **Triple Delta Protocol (SOP_002 / LANGUAGE_SOP_004)**. `project_formula(signature_text, symbols_list)` partitions a 24-bit signature into blocks and generates a deterministic symbolic formula (e.g., `3α + 2β²`). Used by the Swarm during Lexical Genesis. |

**Stack position:** Bridge between Layer 2 (semantics) and Layer 4 (Swarm). The Swarm calls this when it discovers a Lexical Gap.

---

## `ubp_phenomenology.py` — *Phenomenology Engine v5.5 (Modular Core)* (106 lines)

| Class | Role |
| :--- | :--- |
| **`PhenomenonDefinition`** | Dataclass for a phenomenon descriptor (name + expected dimensions). |
| **`PhenomenologyEngine`** | Operates in two modes. **Scanner**: translates real-world data (RGB colors, sensor inputs, text) into stable 24-bit vectors using SHA-256 + Spatial Voxel Hashing. `process_phenomenon(definition, data)`, `_print_summary(res)`. |
| **`NoumenalProjector`** | Inverse mode. `manifest_intent(name, shadow_bits)` translates "Shadow Intent" (noumenal seeds) into the matter / informational states required to sustain that intent within the lattice. Implements the **B-Matrix** "Physics of Will" — calculates the metabolic cost (Symmetry Tax) required for an intent to manifest. Enforces the **Observer Threshold Y** and implements **Topological Folding** for frequencies. |

---

## `ubp_observer_dynamics.py` — *Observer Dynamics Engine v7.1* (95 lines)

**Module docstring:**
> Fixed `AttributeError` by implementing Columnar Hydration for v9.9 KB.

| Class | Role |
| :--- | :--- |
| **`ObserverDynamicsEngine`** | The "Consciousness as Buffer Access" implementation. `split_ontology_layers(vector)` decomposes the 24 bits into the four hexagrams (Reality / Information / Activation / Potential). `conscious_read(vector, nrci)` implements the **0.70 Conscious READ gate** — vectors below threshold remain in the Subliminal/Zombie state. `calculate_soc_energy(vector, nrci, toggle_rate_hz)` is the **1 THz Wall of Reality** check; above 10¹² Hz coherence decays exponentially. |

**Module function:** `run_observer_audit()` — full self-test routine.

**Key proofs implemented:**
- **Zombie State proof:** highly unstable particles (Top Quark, NRCI ≈ 0.68) compute high SOC Energy but fail the 0.70 threshold — they cannot transfer from the Potential buffer to the Reality register.
- **Wall of Reality:** frequencies > 1 THz suffer exponential coherence decay; SOC Energy collapses to zero.

---

## `ubp_internal_dialogue_semantic_description.py` — *Deep Semantic Mirror* (105 lines)

**Module functions:**
- `_get_vector(entry)` — extracts the 24-bit vector from a KB entry.
- `_hamming(v1, v2)` — Hamming distance between two 24-bit lists.
- `find_word_for_concept(law_vec)` — searches the Language KB for the closest semantic match to a physical vector.
- `deepest_internal_dialogue(query, max_depth, gap_threshold)` — the recursive internal monologue. Iteratively probes the lattice, snapping intermediate vectors back to Golay codewords, and emits the full reasoning trace including identified Lexical Gaps.

**Stack position:** Called by `auto_trigger.py` when the user requests deep semantic exploration. Outputs become the "Reasoning Chain" component of the prompt injected into the LLM.

---

## `auto_trigger.py` — *Reflexive Bridge v19.1 (Ultra-Compact Compatible)* (126 lines)

**Module docstring:**
> Fixed `IndexError` in `synth_context` by separating Metadata Fields from MOG Tensor Categories.

**Module functions:**
- `load_compact_kb(path)` — hydrates the v9.9 columnar `ubp_system_kb.json` using `_fields` dynamic index mapping.
- `reflexive_recall(query)` — searches `ID_TO_KEY`, `PHRASE_TO_KEYS`, `TAG_TO_KEYS` indexes for the strongest resonance match.
- `synth_context(recall_dict)` — constructs the three-part specialized prompt injected into the LLM:
  1. **Primary Resonance** — the most relevant concept found.
  2. **Reasoning Chain** — the steps taken to resolve the query (from `deepest_internal_dialogue`).
  3. **Synthesis Hint** — a pre-calculated summary anchoring the AI's response to the lattice.

**Module constants:**
- `KB_FILE = 'ubp_system_kb.json'`
- `ID_TO_KEY`, `PHRASE_TO_KEY`, `TAG_TO_KEYS` — runtime indexes.

**Stack position:** This is the live interface between the user and the system's memory. It enables **Chat with Memory** functionality — preventing the LLM from hallucinating physics by anchoring every response to concrete KB entries.

---

# LAYER 3 — Translation & Execution

These modules **compile** human intent (Python scripts, `.ubp` programs, natural-language descriptions) into geometric operations on the substrate.

## `ubp_python_engine.py` — *UBP Python Code Engine (UPCE) v2.2* (228 lines)

**Module docstring:**
> UBP PYTHON CODE ENGINE (UPCE) v2.2 — SELF-HEALING EDITION.

A code-generation pipeline that maps standard Python keywords to 24-bit physical laws and synthesizes scripts based on geometric stability.

| Class | Role |
| :--- | :--- |
| **`PyLawResult`** / **`CodeResult`** / **`ImprovementResult`** | Dataclasses for results. |
| **`PythonSemanticEngine`** | `query(text, top_k)` retrieves the `LAW_PY_DEF`, `LAW_PY_FOR`, etc. entries that match an English description. `_cosine(v1, v2)` for similarity. |
| **`ObserverWall`** | The 0.70 `CONSCIOUS_THRESHOLD` gate. `evaluate(law)` returns whether a candidate law crosses the wall; `filter_laws(laws)` keeps only those that pass. |
| **`PythonCodeGenerator`** | `_plan_script(intent)` plans the structure, `generate(intent, verbose)` produces the final script, `_synthesize(intent, laws)` merges selected laws into runnable Python. |
| **`PythonCodeImprover`** | `calculate_nrci(code)` scores existing code on geometric stability; `improve(code, verbose)` rewrites it to maximize NRCI. |
| **`UBPPythonEngine`** | Top-level façade. `write(intent, verbose)` returns generated code; `improve(code, verbose)` rewrites existing code. |

**Use case:** Ask the engine *"write a function that integrates `f(x) = sin(x)` from 0 to π"* — it queries the Python KB for `LAW_PY_DEF`, `LAW_PY_FOR`, `LAW_PY_INTEGRATE`, applies the Observer Wall filter, and synthesizes a script. Every line is grounded in a geometric law rather than statistical autocomplete.

---

## `ubp_sovereign_evolver.py` — *Sovereign Evolver v2.1 (AST Firewall)* (194 lines)

**Module docstring:**
> PHILOSOPHY: "Computational Sovereignty". UBP posits that reality is a deterministic, error-corrected projection of a 24-bit substrate. Relying on external C-based floating-point libraries (like Python's standard `math` module) introduces "Noumenal Leakage" — hardware-dependent artifacts.

| Class | Role |
| :--- | :--- |
| **`SovereignTransformer`** (extends `ast.NodeTransformer`) | The firewall. `visit_ImportFrom(node)` strips `from math import …` lines; `visit_Call(node)` (and other visitors) rewire `math.sin(x)` → `GRAND_ALU.sin(x)`, `math.exp(x)` → `GRAND_ALU.exp(x)`, etc. |

**Module functions:**
- `evolve_source(src)` — runs the transformer on a Python source string and returns the sovereign version.
- `audit_source(src)` — reports any remaining floating-point dependencies.

**Stack position:** Sits between the user's Python script and execution. Anything that wants to interact with the substrate must first pass through the Evolver. Together with `ubp_eml_alu_sovereign.py` it enforces the **float-free** invariant for runtime code (the substrate libraries are already float-free by construction).

---

## `ubp_py_runtime.py` — *UBP-Py Virtual Machine v2.3.4* (135 lines)

| Class | Role |
| :--- | :--- |
| **`CortexAtom`** | The fundamental unit of UBP-Py. Fields: `label`, `value` (`Fraction`), `vector` (24-bit list), `nrci`, `tax`, `tilt`, `tier`, `category`, `hierarchy`, `parent_lineage`. `to_dict()` for serialization. |
| **`MOGOntology`** | **LAW_SUBSTRATE_005** Tetradic MOG partition health. `calculate_health(vector)` evaluates the 4×6 array balance (Reality / Information / Activation / Potential). |
| **`UBPPyVM`** | The VM. `_load_kb()`, `let(label, val_str, tier, category)`, `synth(label, recipe_str, u_score)`, `audit(label)` (prints Tax, NRCI, Tilt, DQI, MOG Health), `to_scene_3d()` (projects 24-bit atoms into 3-D space for visualization — maps 8-bit blocks to X/Y/Z), `commit()`. |

**Constants:** `CONST = SUBSTRATE.get_constants(50)`, `Y_CONST = CONST['Y']`.

---

## `ubp_py_lang.py` — *UBP-Py Language Parser v2.0* (99 lines)

**Module function:** `execute_program(vm, text)` — parses a `.ubp` program string and dispatches each line to the appropriate `vm.method()` call. Supports the full command set: `LET, IMPORT, STATE, TRANSFORM, VOID, PULSE, SYNTH, SPIRAL, GATE, REFLEX, AUDIT, FOM, COMMIT, TRACE, VISUALIZE`. (Full syntax reference in [`ubp_files_and_usage.md`](ubp_files_and_usage.md) §5.)

---

## `ubppy.py` — *UBP-Py CLI Entry Point* (74 lines)

**Module docstring:**
> UBP-Py v2.3 (Standard) — Signature Alignment. Fixed `TypeError` by strictly matching the `UBPPyVM` signature defined in `ubp_py_runtime.py`.

**Module functions:**
- `load_program_file(path)` — reads a `.ubp` text file.
- `run_demo(vm)` — built-in demonstration of VM usage.
- `main()` — CLI argument parsing: `--program`, `--lattice`, `--trace`, `--env`, `--scene`.

Usage: `python ubppy.py --program myprogram.ubp --trace trace.json --scene scene.json`.

---

# LAYER 4 — Cognitive Orchestration

The Brain. Multi-agent loops, oracle bridges, executive analysis.

## `ubp_brain_consolidated.py` — *UBP Brain v7.2 (Precision Gating)* (181 lines)

**Module docstring:**
> UBP BRAIN CONSOLIDATED v7.2 — PRECISION GATING EDITION. **FIXES**: Domain Gating (prevents `OP_LIGHT` from intercepting `Speed of Light` queries); Identity Lock (prioritizes `PARTICLE_` and `ELEM_` prefixes for physical queries); N-Gram Weighting (trigrams 9× unigrams); Robust Loader (auto-detects and hydrates v9.9 Ultra-Compact KB).

| Class | Role |
| :--- | :--- |
| **`KBManager`** | `load(paths)`, `_index_entry(uid, entry)` builds the four runtime indexes (ID → key, phrase → keys, tag → keys, vector → key). |
| **`ReasoningResult`** | Dataclass for the output of `process_query`: primary resonance, candidates, reasoning chain, NRCI, Lexical Gaps. |
| **`UBPBrain`** | The deterministic recall engine. `initialize(kb_paths)` loads system + language KBs; `process_query(query)` is the core method — N-Gram tokenization, vector resonance, Cosine ranking, Domain Gating, Identity Lock, Coherence Snap. |

**Module helpers:** `extract_vector(entry)`, `extract_nrci(entry)`, `extract_name(entry)` — columnar accessors that work with the v9.9 `_fields` schema.

---

## `ubp_swarm_tct_v25.py` — *Genesis Swarm (TCT Edition)* (176 lines)

The active Swarm Orchestrator (Genesis Edition). Runs a multi-agent loop that integrates the **Oracle Bridge** and **Lexical Genesis**.

| Class | Role |
| :--- | :--- |
| **`SemanticResonator`** | `vectorize_text(text)` — converts a natural-language directive into a 24-bit Query Chord. |
| **`UBPSwarmGenesis_v25`** | The orchestrator. `run_directive(directive, prob_id, expected)` runs SOP_001 (Two-Track Solve) and SOP_002 (Lexical Genesis) on a single problem. `_generate_manifold_map(prob_id, res)` produces a 3-D scene from the result. `run(problem_file)` iterates over a problem set. |

**Module functions:** `_golay_snap(v)`, `_vec_to_pos(v)`.

**Use case:** Feed it `mathnet_problems.json` (an Olympiad problem set) and it will (a) extract the mathematical kernel from each problem via `MathNetKernelExtractor`, (b) solve it twice (native + SymPy), (c) on `BOTH_AGREE` snap the result to Λ₂₄ and record true NRCI, (d) invent new symbolic formulas for any Lexical Gaps it discovers.

---

## `ubp_v28_oracle.py` — *Two-Track Oracle (Native + SymPy)* (2,143 lines)

The logical calculator. Implements the **Two-Track Parallel Solve** and the **MathNet Kernel Extractor**.

| Class | Role |
| :--- | :--- |
| **`NativeMathEngine`** | Pure-integer / rational engine. `gcd`, `lcm`, `extended_gcd`, `is_prime` (substrate-native), `_pollard_rho`, `factorise`, `divisors`, `euler_phi`, `modinv`, `crt`, `isqrt`, `icbrt`, `is_perfect_square`, … (≈25 methods). |
| **`UBPPolynomial`** | Exact-arithmetic univariate polynomial. `from_string("ax^n + bx + c")`, `degree`, `differentiate`, `antiderivative`, `definite_integral`, `definite_integral_exact`, `evaluate`, `evaluate_exact`, `rational_roots`. Supports `+, −, ×`. |
| **`TopologicalALU`** | Gray Code / Golay / Leech Lattice arithmetic. `_weight_search(v_super, c_range, target_weights)` searches for `c` such that `Golay(v_super ⊕ Gray(c))` has weight in target_weights. Solves addition, subtraction, multiplication, magnitude, GCD, power, modulo, and **primality** entirely on the substrate via `primality_nrci(n)`. `attempt_solve(directive)` routes a directive to the right op. |
| **`NativeDynamicSolver`** | Routes problems through `NativeMathEngine` + `UBPPolynomial`. ≈30 specialized helpers: `_nums`, `_floats`, `_data`, `_poly`, `_parse_complex`, `_gcd`, `_lcm`, `_primality`, `_factorise`, `_euler_phi`, `_modinv`, `_crt`, … |
| **`SymPyOracle`** | SymPy as a semantic/oracle layer. Runs independently of UBP native. ≈20 specialized helpers: `_diff`, `_integrate`, `_limit`, `_series`, `_det`, `_eigen`, `_inv`, `_extract_expr`, `_extract_pt`, `_extract_wrt`, `_extract_matrix`. |
| **`MathNetKernelExtractor`** | MathNet (olympiad) problems have two parts: English fluff + mathematical kernel. `extract(problem, answer)` returns just the kernel. |
| **`ValidationBridge`** | The Two-Track Parallel Solve. `solve(directive, expected)` runs both tracks, compares, returns `BOTH_AGREE` / `NATIVE_ONLY` / `ORACLE_ONLY` / `BOTH_DISAGREE`. |
| **`UBPv28Runner`** | The runner. `run_standard(problems, label)` (CALC, LINALG, VEC, etc.); `run_mathnet(problems, label)` (Olympiad with kernel extraction + two-track); `write_report(run1, run2, outpath)`. |
| **`MathNetKernelSolver`** | Dispatches specialized kernel computations. Includes dedicated solvers for specific MathNet problems: `_mn_nt_001` (2ⁿ−1 divisible by 7 iff n ≡ 0 mod 3), `_mn_nt_003` (gcd(21n+4, 14n+3) = 1), `_mn_nt_004` (m²−n² = 2026 has no solution), `_mn_nt_005` (largest n divisible by all integers < ∛n), `_mn_comb_004` (subsets of {1..10} with sum divisible by 3), `_mn_comb_005` (f(f(n)) + f(n) = 2n+3 ⇒ f(n) = n+1), … |

**Module functions:** `to_gray_code(n, bits)`, `_golay_snap(v)`, `_nrci_of(v)`, `_fingerprint(val)` (Gray code for integers, hash for symbolic), `run_tests()`.

---

## `ubp_moe_cortex_v2.py` — *Mixture-of-Experts Cortex* (128 lines)

| Class | Role |
| :--- | :--- |
| **`UBPMoECortexV2`** | The router. `_train_linguist()` builds an internal word-to-vector index. `_get_vector(word)` retrieves it. `research(objective_str, max_words)` runs a multi-step research loop, generating candidate sentences and grading them by lattice coherence. `_propose_candidates(sentence, count)`. |

**Stack position:** Optional cognitive layer. Acts as a router that selects which expert (Brain / Swarm / Oracle / Semantic Engine) to invoke for a given query.

---

## `ubp_integrated_engine_v1.py` — *Integrated Engine v3.4 (Composite Scene)* (181 lines)

**Module docstring:**
> The high-level executive layer of the UBP Studio. Bridges the Semantic Brain, the 24D Micro-Core, and the 256D Macro-Bulk. REFINEMENT: Added 'Composite Query Detection' — if multiple entities are detected in the prompt, the engine bypasses the single-vector confidence threshold and automatically constructs a multi-object scene for the ViT Eyes. Added a `thermo_audit` section to the `analyze_query` output.

| Class | Role |
| :--- | :--- |
| **`VitEyesEngine`** | The Visual Cortex of the UBP. `_visual_hash(vec_24d)` hashes the *light* (vector) rather than the *DNA* (math). `observe_scene(objects)` produces a 3-D scene composed of multiple 24-bit objects. |
| **`UBPIntegratedEngine`** | The executive. `analyze_query(query)` performs a **Penta-Audit** on the query (semantic, geometric, particle-physics, MOG, thermo). |

**Module function:** `hex_to_bw256(hex_str)` — converts a 256-bit SHA-256 hash directly into a 256-D Barnes-Wall lattice coordinate. This is the bridge between the 24-D micro-core and the 256-D macro-bulk.

---

# SUPPORT TIER — Visualization · Infrastructure · Bridges

## `ubp_viz.py` — *Visual Bridge v2.0* (145 lines)

**Module docstring:**
> Handles the export of 3D geometric data from the Python Kernel to the React/Three.js Visualizer. **FEATURES**: Fraction-Aware (auto-converts UBP Fractions to floats for rendering); Primitives (helpers for Points, Spheres, Lines); Auto-Sync (writes to `scene_3d.json` which triggers the frontend update).

| Class | Role |
| :--- | :--- |
| **`UBPJSONEncoder`** | Custom `json.JSONEncoder` that handles UBP-specific types (especially `Fraction`). |

**Module functions:** `point(x, y, z, color, size)`, `sphere(x, y, z, r, color)`, `line(start, end, color, width)`, `save_scene_3d(data, filename='scene_3d.json')`, `demo()`.

## `ubp_rgdl.py` — *Resonance Geometry Definition Language v5.1* (121 lines)

**Module docstring:**
> The Standard Visualization Engine for the UBP System. Upgraded to use ExactMath and True Leech Lattice NRCI coloring. *"Geometry is the macroscopic manifestation of synchronized binary toggles."*

| Class | Role |
| :--- | :--- |
| **`RGDLEngine`** | `_get_nrci_color(x, y, z)` maps a 3-D coordinate to a 24-bit vector, snaps it to the lattice, and colors it by true NRCI (Cyan = stable, Magenta/Blue = unstable). `generate_sphere(radius)` (the Monad — voxelized sphere colored by NRCI); `generate_cube(size)` (the Matrix — voxelized cube colored by NRCI); `render(voxels, label)` injects the geometry into the visual cortex. |

**Module functions:** `to_gray_code(n, bits)`, `manifest_sphere(radius)`, `manifest_cube(size)`.

## `viz_loader.py` — *Visualization Loader* (43 lines)

**Module function:** `load_and_render()` — loads a JSON scene file from the workspace and pipes it to the visual cortex. Used by the app to inspect pre-built scenes.

## `viz_spatial_simplification.py` — *Manifold Simplifier* (51 lines)

**Module function:** `simplify_manifold()` — simplifies complex 3-D manifolds into stable geometric "Faces" with the Origin to prevent visual clutter. Reveals the underlying **Pyramid structures** (stable triadic relationships) that would otherwise be hidden in noisy clouds.

## `ubp_backend.py` — *Flask REST Bridge* (298 lines)

**Module docstring:**
> UBP SUBSTRATE BACKEND — Flask REST API for `core.py` v6.1. Wires the real Golay [24,12,8] + Leech Λ₂₄ engines into a lightweight HTTP API so the HTML calculator can use 50-term π, exact Fraction arithmetic, and the true Golay decoder instead of the JavaScript stub. **Usage:** `pip install flask flask-cors`, then `python ubp_backend.py` → starts on `http://localhost:5099`.

**Why it exists:** JavaScript in a standard web browser has performance and precision limits — it cannot natively run the 50-term continued-fraction π with infinite-precision `Fraction` arithmetic, nor can it run the full heavy Python-based Golay [24,12,8] and Leech Λ₂₄ search algorithms at scale. `ubp_backend.py` is the **Local Research Bridge**: when developing/testing new UBP algorithms locally in Python, point the local HTML file at `http://localhost:5099` to instantly verify that a new Python computation matches the frontend visualization.

**Module functions / endpoints:**
- `to_gray_code(n)` — Gray-code an integer into 24 bits.
- `classify_lattice(sw)` — classify a Hamming weight onto Golay/Leech.
- `compute_nrci(codeword_24)` — `NRCI = 10 / (10 + tax)` with `tax = hw·Y + norm²/8`.
- `fingerprint_number(n)` — full UBP fingerprint.
- `status()` (`GET /`) — health check + engine info.
- `fingerprint()` (`POST /fingerprint`) — fingerprint a single number.
- `fingerprint_batch()` (`POST /fingerprint/batch`) — bulk fingerprint.
- `compute()` (`POST /compute`) — perform a binary operation and fingerprint the result.
- `get_constants()` (`GET /constants`) — return UBP constants (exact Fractions as floats).

**Constants:**
- `CORE_PATH = Path(__file__).parent / 'ubp_unified_v5.py'`
- `CODEWORD_WEIGHTS = {0, 8, 12, 16, 24}` — the only Hamming weights allowed by Golay [24,12,8].

## `ubp_browser_engine.py` — *Browser Physics Loop* (64 lines)

**Module docstring:**
> UBP Browser Engine (V3) — Adapts the UBP Physics Engine to run directly inside the browser's animation loop, bypassing the need for FastAPI or WebSockets. **Instructions:** (1) Ensure the engine files (`ubp_space_v3.py`, etc.) are uploaded; (2) Run this script instead of `ubp_server_v3.py`; (3) Switch to the VISUAL tab to see the live simulation.

**Module function:** `game_loop()` — the requestAnimationFrame-driven main loop that ticks the Digital Twin Physics Engine inside the Pyodide kernel.

## `ubp_kb_architect.py` — *KB Architect v2.2 (SOP_002 + Gray Code)* (94 lines)

**Module docstring:**
> Now uses Binary-Reflected Gray Code for the 24-bit vector.

| Class | Role |
| :--- | :--- |
| **`KBArchitect`** | The factory for new KB entries. `generate_vector(math_dna, ubp_id)` (Gray-coded 24-bit), `calculate_metrics(math_dna, vector)` (NRCI + tax), `calculate_tilt(vector)` (angular deviation from Universal North in degrees), `create_entry(ubp_id, lexicon_name, definition, math_dna, hierarchy)` (full SOP_002-hardened entry). |

**Module function:** `to_gray_code(n, bits)`.

**Module constants:**
- `CONST = UBPUltimateSubstrate.get_constants(50)`
- `UNIVERSAL_NORTH = np.array([-0.30656966974248284, -0.9197090092274486, 0.2452557357939863])`
- `MOG_CATEGORIES` — the 24 MOG tensor categories (`M_Mass`, `M_Charge`, `M_Space`, `M_Time`, `M_Thermal`, `M_Count`, `I_Topology`, `I_Symmetry`, `I_Density`, `I_Connectivity`, `I_Dimension`, `I_Complexity`, `A_Energy`, `A_Force`, `A_Velocity`, `A_Flux`, `A_Resonance`, `A_Spin`, `P_Probability`, `P_Ratio`, `P_Limit`, `P_Tax`, `P_Coherence`, `P_Phase`).

## `ubp_ingest.py` — *Safe KB Ingestion* (129 lines)

**Module functions:**
- `get_mog_cat(key)` — map a `math` field key (e.g. `M`, `Z`, `BP`) to one of the 24 MOG categories.
- `run_safe_ingestion()` — ingest `proposed_*.json` files into the main KB after validation.

**Module constants:**
- `PROPOSED_FILES = ['proposed_chromatic_law.json', 'proposed_resonance_law.json']`
- `SOURCE_KB = 'ubp_system_kb.json'`, `OUTPUT_KB = 'ubp_system_kb_1.json'`
- `MAPPING = {'M': 'M_Mass', 'Mass': 'M_Mass', 'Z': 'M_Count', 'BP': 'M_Thermal', 'MP': 'M_Thermal', 'Rho': 'I_Density', 'Density': …}` — the canonical mapping from `math`-field keys to MOG categories.

## `hash_all_1.py` — *Hash Indexer v3.0 (Universal Merged Edition)* (103 lines)

**Module docstring:**
> Generates a unified `ubp_hash_memory_kb.json` index from all active Knowledge Base files (System + Language).

**Module function:** `run_indexing()` — walks every KB file, computes the SHA-256 fingerprint of each entry's `math` field, and writes the recall index. Output enables **O(1) lookups** for direct IDs and efficient recall for partial queries.

## `ubp_fom_system.py` & `ubp_fom_manager_v2.py` — *Frame-of-Mind System*

The Frame-of-Mind (FOM) system implements **dynamic NRCI weighting** and **Contextual Gravity** for the Belief Layer.

**`ubp_fom_system.py`** (76 lines):
| Class | Role |
| :--- | :--- |
| **`FrameOfMind`** | A single bias frame. `set_weight(ubp_id, nrci)`, `set_category_weight(category, nrci)`, `get_weight(ubp_id, category)`, `to_dict()`. |
| **`FOMManager`** | The registry. `load_index()`, `save_index()`, `switch_frame(frame_id)`, `get_active_frame()`, `get_mass(ubp_id, category)` (returns FOM-weighted "mass" for use in the Contextual Gravity formula). |

**Module constant:** `FOM_MANAGER = FOMManager()` — global singleton.

**`ubp_fom_manager_v2.py`** (109 lines): same `FrameOfMind` + a richer `GravitationalCortex` that uses the Gravity Formula `Pull = Mass / (Distance + 1)²` to resolve queries against belief anchors.

**Pre-configured frames** include `SCIENTIFIC_STRICT` (weights Substance at 0.9, Meaning at 0.1), `SEMANTIC_EXPLORER`, `ENTROPIC_FILTER`. Frames can be saved/loaded as JSON for persistent cognitive bias across sessions.

---

# Data Files in `/core/`

In addition to scripts, `/core/` contains four JSON data files that participate in the runtime:

| File | Size | Role |
| :--- | ---: | :--- |
| **`ubp_lang_kb_combined_v4.json`** | 2.2 MB | The combined Language KB (lexicon + Python KB + symbolic operator dictionary). Used by `ubp_semantic_engine.py`. |
| **`ubp_lexicon_v2_defs.json`** | 473 KB | Lexicon definitions for natural-language grounding. |
| **`ubp_python_kb.json`** | 117 KB | The Python Code Engine's law library (`LAW_PY_DEF`, `LAW_PY_FOR`, `LAW_PY_INTEGRATE`, …). Used by `ubp_python_engine.py`. |
| **`ubp_beliefs_kb.json`** | 19 KB | Belief manifolds and contextual structures (e.g. `BELIEF_WATER_001` — the Aqueous Stability manifold). |
| **`rational_cortex.json`** | 4 KB | Rational cortex configuration (weights, gates, thresholds). |

The main `ubp_system_kb.json` (1.7 MB, 746 entries, 420 Laws) lives in `/system_kb/`, not `/core/`, but is loaded by every Layer 2 and Layer 4 module.

---

# Archived Scripts

The following scripts were **archived on 22 May 2026** because their functionality was absorbed into `ubp_unified_v5.py`, `ubp_swarm_tct_v25.py`, or `ubp_genesis_boot.py`. They live in `archive_core/` and are kept for historical traceability:

```
ubp_code_evolver.py
ubp_prime_numbers.py
ubp_prime_numbers_1.py
ubp_master_runner_v6.py           ← Topological Tenacity absorbed into ubp_unified_v5.py
ubp_noisecore_v4_extensions.py    ← merged into ubp_unified_v5.py
ubp_noisecore_v4.py               ← merged into ubp_unified_v5.py
ubp_math_bridge_1.py
constants.py                      ← superseded by UBPUltimateSubstrate
core.py                           ← v6.1; merged into ubp_unified_v5.py
ubp_barnes_wall.py                ← merged into ubp_unified_v5.py (BarnesWallEngine)
ubp_core_v4_2_6_COMBINED.py
ubp_swarm_tct_v24.py              ← upgraded to v25
```

Renames performed in the same update:
- `ubp_analog_test_suite_v3.py` → **`ubp_electromagnetic_analog_compute_engine.py`**
- `bp_genesis_boot.py` → **`ubp_genesis_boot.py`**

---

# How the Layers Connect (Call Graph Summary)

A typical natural-language query (e.g. *"What is the binding energy of Water?"*) flows through the stack as follows:

```
User types query
      │
      ▼
[auto_trigger.py]                        ◀── reflexive scan
      │   load_compact_kb() · reflexive_recall(q) · synth_context(r)
      ▼
[ubp_brain_consolidated.py]              ◀── deterministic recall
      │   N-Gram tokenization → vector resonance → Domain Gating
      │   → returns ReasoningResult(primary, chain, NRCI, gaps)
      ▼
[ubp_semantic_engine.py] ←─── if gap detected ───▶ [ubp_semantic_sovereign.py]
      │   Cosine Resonance                              │   TripleDeltaProjector
      │                                                  ▼
      │                                          [ubp_swarm_tct_v25.py]
      │                                                  │   Lexical Genesis
      │                                                  ▼
      │                                          [ubp_v28_oracle.py]
      │                                                  │   Two-Track Solve
      ▼                                                  ▼
[ubp_unified_v5.py]   ◀──────────────────────────  primality / Golay / Leech
      │   GOLAY_ENGINE · LEECH_ENGINE · PARTICLE_PHYSICS
      ▼
[ubp_py_runtime.py]                      ◀── if .ubp execution requested
      │   UBPPyVM.synth("Water", "2xH + 1xO")
      ▼
[ubp_viz.py / ubp_rgdl.py]               ◀── to_scene_3d() → scene_3d.json
      │
      ▼
Browser (React + Three.js) renders the scene
```

Every step downward is float-free. Every step upward returns either a concrete codeword + NRCI + tax, or a Lexical Gap that triggers Genesis.

---

# Building the v7.2 Mindset

When working in this codebase, three principles keep you aligned:

1. **Math, Language, Script must phase-lock.** If a result is "true" mathematically but cannot be named in the lexicon, the answer is incomplete — invoke Lexical Genesis. If a script depends on `math.sin`, it must pass through the Sovereign Evolver first.
2. **Geometric Honesty over computational convenience.** Use `Fraction`, never `float`. Use Gray code, never SHA-256, for vector identity (SHA-256 is only for content-addressable storage of `math` fields). Use the Topological Tenacity primality test, never Miller-Rabin.
3. **Every object pays Symmetry Tax.** Even the Void costs `0.0110 × Y` to perceive. The 1.0000 NRCI ceiling is asymptotic — pure mathematical truth lives only at Gap 0. Everything else exists under Restorative Pressure from the substrate.

If a new contribution doesn't satisfy all three, it goes to `archive_core/` until it does.

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
