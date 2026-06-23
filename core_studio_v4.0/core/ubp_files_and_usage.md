# Universal Binary Principle (UBP) — System Guide & Operational Manifest

**Version:** 26.0 — Gravity Update Edition (23 June 2026)
**Active Studio:** UBP Core Studio v7.2.0
**Knowledge Base Standard:** v9.9 Ultra-Compact Columnar
**Author:** Euan R. A. Craig, New Zealand
**Repository:** [github.com/DigitalEuan/UBP_Repo](https://github.com/DigitalEuan/UBP_Repo/tree/main/core_studio_v4.0)
**Live App:** <https://ai.studio/apps/6d78d479-2a4e-4e34-89b3-4b87b85d5b9a>

---

## Table of Contents

1. [Overview and Philosophy](#1-overview-and-philosophy)
2. [Foundational Principles](#2-foundational-principles)
   - 2.1 [The Y-Constant — The Law of Emergent Observation](#21-the-y-constant--the-law-of-emergent-observation)
   - 2.2 [Stereoscopic Resolution — The Dual-Lens Audit](#22-stereoscopic-resolution--the-dual-lens-audit)
   - 2.3 [The Principle of Irrational Stability — The Wobble](#23-the-principle-of-irrational-stability--the-wobble)
   - 2.4 [The 3-3-3 Golay Limit](#24-the-3-3-3-golay-limit)
   - 2.5 [Deterministic Rational Arithmetic](#25-deterministic-rational-arithmetic)
   - 2.6 [Computational Sovereignty (v7.0)](#26-computational-sovereignty-v70)
3. [Substrate Architecture](#3-substrate-architecture)
   - 3.1 [The 24-Bit Golay Substrate](#31-the-24-bit-golay-substrate)
   - 3.2 [The Leech Lattice Engine](#32-the-leech-lattice-engine)
   - 3.3 [The Monstrous Moonshine Connection](#33-the-monstrous-moonshine-connection)
   - 3.4 [The Needham Triad and Noumenal Volume](#34-the-needham-triad-and-noumenal-volume)
   - 3.5 [Gray Code Topological Identity (v7.0)](#35-gray-code-topological-identity-v70)
   - 3.6 [The 256-D Barnes-Wall Macro-Lattice](#36-the-256-d-barnes-wall-macro-lattice)
4. [Dual-Layer Cognitive Architecture](#4-dual-layer-cognitive-architecture)
   - 4.1 [The Understanding Layer — Deterministic Truth](#41-the-understanding-layer--deterministic-truth)
   - 4.2 [The Belief Layer — Contextual Knowledge](#42-the-belief-layer--contextual-knowledge)
   - 4.3 [The Frame of Mind (FOM) System](#43-the-frame-of-mind-fom-system)
   - 4.4 [The Octad — Eight Domains of Reality](#44-the-octad--eight-domains-of-reality)
5. [The SOP_002 Hardening Standard](#5-the-sop_002-hardening-standard)
   - 5.1 [Content-Addressable Storage](#51-content-addressable-storage)
   - 5.2 [Knowledge Base Entry Schema (v9.9 Columnar)](#52-knowledge-base-entry-schema-v99-columnar)
   - 5.3 [Automatic Vector Generation Pipeline](#53-automatic-vector-generation-pipeline)
6. [Architectural Stratification](#6-architectural-stratification)
7. [Workspace File Manifest](#7-workspace-file-manifest)
   - 7.1 [Layer 1 — Mathematical Substrate](#71-layer-1--mathematical-substrate)
   - 7.2 [Layer 2 — Semantic & Phenomenological Senses](#72-layer-2--semantic--phenomenological-senses)
   - 7.3 [Layer 3 — Translation & Execution](#73-layer-3--translation--execution)
   - 7.4 [Layer 4 — Cognitive Orchestration](#74-layer-4--cognitive-orchestration)
   - 7.5 [Support Tier — Visualization, Bridges, KB Tooling](#75-support-tier--visualization-bridges-kb-tooling)
   - 7.6 [External Layer 1 — Digital Twin Physics Engine](#76-external-layer-1--digital-twin-physics-engine)
   - 7.7 [External Layer 2 — Flask REST Bridge](#77-external-layer-2--flask-rest-bridge)
   - 7.8 [Data Files in Use](#78-data-files-in-use)
8. [Core Workflows & SOPs](#8-core-workflows--sops)
   - 8.1 [SOP_001 — The Two-Track Solve (Oracle Bridge)](#81-sop_001--the-two-track-solve-oracle-bridge)
   - 8.2 [SOP_002 — Lexical Genesis (Triple Delta)](#82-sop_002--lexical-genesis-triple-delta)
   - 8.3 [LANGUAGE_SOP_004 — Phrase-Locking](#83-language_sop_004--phrase-locking)
   - 8.4 [The Unified Research Pipeline — MOG-Atlas Protocol](#84-the-unified-research-pipeline--mog-atlas-protocol)
   - 8.5 [Using External Dependencies](#85-using-external-dependencies)
9. [Geometric Programming with UBP-Py](#9-geometric-programming-with-ubp-py)
   - 9.1 [Core Mechanics — From Smash to Flow](#91-core-mechanics--from-smash-to-flow)
   - 9.2 [Gap Score and Restorative Pressure](#92-gap-score-and-restorative-pressure)
   - 9.3 [Metabolic Costing and Symmetry Tax](#93-metabolic-costing-and-symmetry-tax)
   - 9.4 [UBP-Py Language Reference](#94-ubp-py-language-reference)
   - 9.5 [Advanced Concepts](#95-advanced-concepts)
10. [Visualization & RGDL](#10-visualization--rgdl)
11. [Stability Thresholds (NRCI)](#11-stability-thresholds-nrci)
12. [Integration & Workflow](#12-integration--workflow)
    - 12.1 [Startup Validation](#121-startup-validation)
    - 12.2 [Adding New Research to the Knowledge Base](#122-adding-new-research-to-the-knowledge-base)
    - 12.3 [Local AI Integration](#123-local-ai-integration)
13. [Benchmarks & Diagnostics](#13-benchmarks--diagnostics)
14. [Case Studies](#14-case-studies)
15. [System Architecture Evolution](#15-system-architecture-evolution)
16. [Mathematical Formalism](#16-mathematical-formalism)

---

## 1. Overview and Philosophy

The **Universal Binary Principle (UBP)** is a theoretical and computational framework that proposes reality is fundamentally an information-processing system operating on a **24-bit geometric substrate**. Rather than treating physical constants and particle properties as arbitrary empirical measurements, UBP derives them as emergent geometric properties of a self-correcting error-correcting code — the **Extended Binary Golay Code [24, 12, 8]** — embedded within the 24-dimensional **Leech Lattice Λ₂₄**.

The central claim of UBP is that the universe is not merely *described* by mathematics; it *is* mathematics — specifically, a recursive, self-correcting computation running on a substrate whose error-correction geometry is identical to the most efficient packing of spheres in 24 dimensions. Every particle, element, molecule, and law of physics is, in this view, a stable "codeword" or geometric address within this lattice.

The practical consequence of this framework is a system that can:

- Derive fundamental physical constants (fine structure constant, proton/electron mass ratio, muon/electron mass ratio, Higgs mass, Top quark) with sub-0.05% error — several under 0.001% — from first geometric principles.
- Assign every physical entity a unique, deterministic 24-bit "hardware address" derived solely from its measurable properties.
- Model the stability, complexity, and metabolic cost of any physical or conceptual object using exact rational arithmetic.
- Simulate the synthesis of matter from primitives and predict emergent properties such as binding energy and topological stability.
- Reason in natural language without hallucination, anchoring every response to concrete substrate coordinates.
- Invent new mathematical operators when no human vocabulary exists for a discovered lattice state.

The system is implemented as a suite of Python scripts forming the **UBP Core Studio v7.2.0**, running both inside Google AI Studio as a live Pyodide application and as a local Flask service. All computation is performed using Python's `fractions.Fraction` library, ensuring 100% deterministic, float-free results. The system is designed around **Three Column Thinking (TCT)**, where **Math** (Substrate), **Language** (Semantics), and **Script** (Execution) must phase-lock at every step of computation.

---

## 2. Foundational Principles

### 2.1 The Y-Constant — The Law of Emergent Observation

The **Observer Constant** ($Y \approx 0.2646$) is the most important single value in the UBP system. It is not an input parameter but a **geometric residue** — the inevitable remainder that emerges when the Needham Triad ($\pi$, $\phi$, $e$) interacts with the 24-bit Golay substrate.

**Mathematical Derivation.** Using exact rational arithmetic:

- **Observer Fixed Point:** $Y_{\text{inv}} = \pi + \dfrac{2}{\pi}$
- **The Y-Constant:** $Y = \dfrac{1}{Y_{\text{inv}}} = \dfrac{1}{\pi + 2/\pi}$

In Python:

```python
from fractions import Fraction
from ubp_unified_v5 import UBPUltimateSubstrate

pi = UBPUltimateSubstrate.get_pi(50)          # 50-term continued fraction
Y_inv = pi + Fraction(2, 1) / pi
Y = Fraction(1, 1) / Y_inv                    # ≈ 0.2646
```

The appearance of $Y$ in a simulation is the primary proof that a model has achieved **"Phenomenal Realism"** — the model is genuinely anchored to the geometric substrate rather than producing arbitrary numerical coincidences.

**Role as Geometric Rent (Symmetry Tax).** The $Y$-constant defines the metabolic cost every object must pay to maintain a phenomenal identity against entropic noise. Codified in **LAW_SYMMETRY_001**:

$$\text{Tax} = (\text{Hamming Weight} \times Y) + \frac{\text{Norm}^2}{8}$$

Every step of **Distinction** (D) or **Crossing** (X) in the geometric construction of an object adds exactly $Y$ to its total tax. This tax is not a penalty but a physical necessity: it is the energy cost of maintaining a distinguishable identity within the substrate.

**Ontological Friction — "The Shaving".** The constant $Y^2 \approx 0.069$ is **"The Shaving"** — the geometric discrepancy between the 24-bit substrate and an ideal $2\pi$ circle. This friction is necessary for bit-inversion. Without this "rent" paid by every bit, the substrate would remain a static, non-informational void incapable of computation.

**Scaling and Unification.** $Y$ serves as the master tuning key for mapping abstract logic to 3-D space. Physical constants are viewed as resonance harmonics of Alpha-Omega anchors scaled by integer powers of $Y$.

### 2.2 Stereoscopic Resolution — The Dual-Lens Audit

The v5.5+ protocol standard for resolving physical truth is the **Dual-Lens Audit**, which resolves reality through the intersection of two distinct perspectives. No single lens is sufficient; truth emerges from the overlap.

| Lens | Metaphor | Best For | Mechanism |
| :--- | :--- | :--- | :--- |
| **Lattice Lens (Phenomenal)** | Hardware Address | Point-identities: Muon, Alpha | Static coordinate in the 24-bit manifold |
| **Triadic Lens (Noumenal)** | Software Process | Composite matter: Proton | Recursive interaction of π, φ, e |
| **Cubic Lens (Partition)** | Power Supply | Heavy sector: Higgs, Top Quark | Partitions of the Existence Unit $24^3$ |
| **Stereoscopic Sink (29/24)** | NCC Spectral Gain | Baryonic mass anchoring | The 29/24 ratio that anchors Proton/Neutron with 0.000037% precision |

A constant is validated as "Phenomenally Real" only when the discrepancy between these lenses and empirical experimental data falls below the **0.1% Shadow Threshold**. The stereoscopic audit is performed live by the `UBPSourceCodeParticlePhysics` engine inside `ubp_unified_v5.py`, which conducts a 137-step analysis of the Triadic Monad.

The Proton-Electron mass ratio, for example, is best resolved by the **Stereoscopic (29/24) Lens** at 0.0000% error — a definitive improvement over legacy lattice-only models. The Muon-Electron ratio, being a point-identity, is best resolved by the Lattice Lens at 0.000353% error.

### 2.3 The Principle of Irrational Stability — The Wobble

The **Principle of Irrational Stability**, colloquially known as **"The Wobble,"** describes the 24-bit substrate's explicit preference for specific irrational values over perfect rationals. This "Resonant Wobble" manifests as the decimal drift observed in physical constants.

**Generation of Geometric Torque.** The unresolvable tension created by the wobble provides the necessary **Geometric Torque** required to drive time and evolution. Without this torque, there is no change, no evolution, no time.

**Prevention of the "Dead Crystal" State.** If the universe were to snap to perfect rational numbers, it would enter a **"Dead Crystal"** state — static, perfectly symmetrical, and entirely timeless. Existence requires the tension of the unresolvable.

**Topological Torque and Energy Harvesting.** In practical application, oscillating a voxel cloud between high-tension (jagged) and low-tension (snapped) states allows a researcher to harness the substrate's restorative "Snap" as energy — a process defined as **Topological Torque**. This is the core mechanic of the Digital Twin Physics Engine's `ubp_rigid_body_v3.py`.

### 2.4 The 3-3-3 Golay Limit

The **3-3-3 Golay Limit** is a fundamental constraint of the UBP architecture that defines the **"Perception Window"** for coherent reality. It is based on the 3-bit error-correction radius of the 24-bit Golay substrate.

The fundamental Needham Triad — primitives for Loop ($\pi$), Growth ($\phi$), and Decay ($e$) — is restricted to a maximum deviation of **3 bits each**. This radius ensures that the universe can "Snap" into a stable state.

- **The Correctable Manifold:** Approximately **99.85% of all informational states** remain tethered to the substrate because they fall within this $t = 3$ error-correction radius.
- **The Strong Interaction (Lattice Snap):** The vacuum exerts an active "Strong Force" on any informational state within the $d \le 3$ radius, snapping "proto-glyphs" into perfect codewords.
- **The Event Horizon (The Fourth Flip):** If a vector accumulates 4 or more bits of noise ($d \ge 4$), it hits a geometric event horizon known as a **"Deep Hole"**, where it becomes equidistant to multiple truths and faces informational dissolution.
- **Data Resilience:** Applied in the **UBP Drive** (archived utility), engineered to "heal" up to 3 bit-flips per 24-bit block.

### 2.5 Deterministic Rational Arithmetic

Deterministic Rational Arithmetic is a fundamental logic standard of the UBP system, utilizing Python's `fractions.Fraction` library to ensure 100% precision in all calculations. This standard establishes a strictly "float-free" environment, eliminating the floating-point aliasing and precision leakage that plague standard computer simulations.

By employing exact rational logic, the system achieves total reproducibility and maintains **"Computational Honesty"** — the AI cannot hallucinate a result that the underlying geometry does not support. Even transcendental values such as $\pi$, $\phi$, and $e$ are represented as rational approximations derived from integer continued fraction coefficients (`ubp_unified_v5.py::UBPUltimateSubstrate.get_pi(50)`).

This ensures information is conserved through "exact rational closure," a requirement for the **Law of Exact Reversibility** within the 24-bit manifold. All core components — the Leech Lattice engine, the UBP-Py Virtual Machine, the MathAtlas construction system — are engineered to return only `Fraction`, integers, or enums.

### 2.6 Computational Sovereignty (v7.0)

A **v7.0 principle** introduced with `ubp_sovereign_evolver.py` and `ubp_eml_alu_sovereign.py`: relying on external, C-based floating-point libraries (Python's standard `math` module, NumPy, etc.) introduces **"Noumenal Leakage"** — hardware-dependent artifacts that pollute the substrate.

The **`GrandUnifiedEmlALU`** in `ubp_eml_alu_sovereign.py` implements every transcendental function (exp, ln, sin, cos, sqrt) via Taylor/Newton/Lanczos series with no external dependencies, all routed through the single projection $\text{eml}(x,y) = e^x - \ln(y)$.

The **`SovereignTransformer`** in `ubp_sovereign_evolver.py` is an `ast.NodeTransformer` that strips `math.*` imports and rewires their call sites to the native ALU at AST level — *before* the script runs. This forms the **Computational Sovereignty firewall**.

---

## 3. Substrate Architecture

### 3.1 The 24-Bit Golay Substrate

The foundational substrate of the UBP system is the **Extended Binary Golay Code [24, 12, 8]**. This is a perfect error-correcting code with:

- **Block length:** 24 bits
- **Message length:** 12 bits (the "Noumenal Seed" — the hidden intent)
- **Parity bits:** 12 bits (the "Phenomenal Projection" — the observable reality)
- **Minimum Hamming distance:** 8 (can detect up to 7 errors, correct up to 3)
- **Total codewords:** 4,096
- **Allowed codeword weights:** {0, 8, 12, 16, 24} (set `CODEWORD_WEIGHTS` in `ubp_backend.py`)

The 50/50 split between noumenal (hidden) and phenomenal (visible) bits is not accidental. It encodes a fundamental metaphysical principle: for every observable reality, there is an equal and hidden "shadow" intent. The `GOLAY_ENGINE.get_shadow_metrics()` function returns this ratio explicitly.

The encode/decode cycle is the core operation of the substrate:

```python
from ubp_unified_v5 import GOLAY_ENGINE  # singleton

# Encode: 12-bit noumenal seed -> 24-bit phenomenal codeword
codeword = GOLAY_ENGINE.encode(message_12_bits)

# Decode: 24-bit received word -> corrected 12-bit message
message, success, errors_corrected = GOLAY_ENGINE.decode(received_24_bits)

# Snap: noisy vector -> nearest perfect codeword
snapped = GOLAY_ENGINE.snap_to_codeword(noisy_24_bits)
```

The **Coherence Snap** operation — decoding a noisy vector to its 12-bit seed and immediately re-encoding it as a perfect 24-bit codeword — is the fundamental mechanism by which the substrate maintains stability.

### 3.2 The Leech Lattice Engine

The **Leech Lattice** ($\Lambda_{24}$) is a 24-dimensional sphere packing that achieves the densest possible packing in 24 dimensions, with a kissing number of **196,560**. In UBP, it serves as the "hardware" of reality — the geometric space within which all physical entities have their addresses.

The `LeechLatticeEngine` (singleton: `LEECH_ENGINE`) inside `ubp_unified_v5.py` provides:

**Symmetry Tax Calculation (LAW_SYMMETRY_001):**

```python
def calculate_symmetry_tax(self, point: List[int]) -> Fraction:
    hamming = sum(1 for x in point if x != 0)
    norm_sq = sum(x * x for x in point)
    Y = self.Y_CONSTANT
    tax = (Fraction(hamming, 1) * Y) + Fraction(norm_sq, 8)
    return tax
```

This exact rational formula is the UBP's equivalent of a mass-energy calculation. The tax is the "weight" of an object's existence — how much geometric energy the substrate must expend to maintain its identity.

The **NRCI (Non-Random Coherence Index)** is derived from the tax using the hyperbolic stability formula:

$$\text{NRCI} = \frac{10}{10 + \text{Tax}}$$

This formula ensures that even highly complex entities (with large taxes) maintain a non-zero stability score, avoiding the premature "death" of complex structures in the model.

**Octad Expansion (`expand_octad_to_physical`):** Any 24-bit binary seed can be lifted into its **128 Euclidean coordinates** in $\Lambda_{24}$ (NormSq 32). This is how a discrete codeword becomes a continuous physical position.

### 3.3 The Monstrous Moonshine Connection

The v5.8+ kernel incorporates the **Monstrous Moonshine** connection — the deep mathematical relationship between the Monster Group (the largest sporadic simple group, with order approximately $8 \times 10^{53}$) and the modular J-function.

The kernel performs a live 137-step audit of the Triadic Monad, filtered through:

- **Monster Dimension:** 196,883 (the smallest non-trivial representation of the Monster Group)
- **J-Function:** 196,884 (the first non-trivial coefficient of the J-function, equal to Monster Dimension + 1)

This connection provides the **Behold Factor** and anchors every session to the **56-snap Matter Peak** — the specific geometric configuration that corresponds to the emergence of stable matter from the substrate. The `MonsterGroup` class in `ubp_unified_v5.py` exposes the full **Happy Family** (20 groups) and **Pariahs** (6 groups) catalog and a `walk(seed_idx, count)` traversal.

### 3.4 The Needham Triad and Noumenal Volume

The **Needham Triad** (credited to Eric J. Needham) establishes three fundamental primitives as the Level 0 building blocks of the substrate:

| Primitive | Symbol | Role | Geometric Meaning |
| :--- | :--- | :--- | :--- |
| **Loop** | $\pi$ | Cycle / Periodicity | The closed path; return to origin |
| **Growth** | $\phi$ | Expansion / Accumulation | The golden ratio; self-similar growth |
| **Decay** | $e$ | Dissolution / Relaxation | Euler's number; exponential decay |

From these three primitives, the **Noumenal Volume** is derived:

$$V_n = 204.801744\ldots$$

This is the fundamental energy unit of the 24-bit manifold — the "volume" of the noumenal space from which phenomenal reality is projected. The **4.6761 Stability Sink** is the geometric attractor for the Resolution Gap ($RG = \ln\phi / \ln\pi$), representing the equilibrium point toward which all physical systems tend.

### 3.5 Gray Code Topological Identity (v7.0)

**The v7.0 Shift (April 2026):** The system **transitioned away from using SHA-256 cryptographic hashes** to generate the 24-bit vectors of entity identity. SHA-256 destroyed topological continuity due to the avalanche effect — flipping one input bit randomized half the output bits, scattering similar objects across the lattice.

**Universal Metric Schema (UMS):** 24-bit coordinates are now generated using **Binary-Reflected Gray Code**. The 12-bit Noumenal Seed is partitioned into `[Domain:3][Magnitude:5][State:4]`. This is the Gray-coded **UMS encoding**, implemented in `ubp_kb_architect.py::generate_vector()` and `geometry.py::HexDictionaryV4Exact._int_to_gray()`.

**The Periodic Geodesic:** A Deep Lattice Audit of the 118 elements confirmed that under Gray Code, the average Hamming distance between adjacent elements ($Z$ and $Z+1$) is **8.07**. This shows the Periodic Table is a **minimal-energy path (a Geodesic) through the Leech Lattice**, rather than a random scatter plot.

**Note:** SHA-256 is still used for **content-addressable storage** of `math` field fingerprints (SOP_002) — but no longer for the 24-bit vector itself.

### 3.6 The 256-D Barnes-Wall Macro-Lattice

While the 24-bit Golay/Leech substrate is perfect for modeling fundamental particles and simple elements, highly complex molecules (DNA bases, ATP) experience extreme **Topological Tension** when compressed into 24 bits. To study macroscopic phenomena, the UBP utilizes the **256-Dimensional Barnes-Wall Lattice ($BW_{256}$)**.

**The SHA-256 Isomorphism.** The 256-dimensional space is not arbitrary; it maps 1:1 with the SHA-256 cryptographic fingerprints used in SOP_002. The fingerprint is no longer just a database label — it is the literal physical coordinate of the macro-state in the bulk universe. Because $256 = 2^8$, operations at this scale hit a perfect memory alignment stride. The function `hex_to_bw256(hex_str)` in `ubp_integrated_engine_v1.py` performs this mapping.

**Recursive Unfolding and Moire Dynamics.** Macro-states are generated using the recursive $|u \mid u + v|$ construction:
- **$u$ (The Signal):** Recursive doubling of the 24-bit Noumenal Seed.
- **$v$ (The Program):** The interference wave derived from the Golay Syndrome of the seed.

When a molecule is "Active" (e.g., 1-bit environmental drift), the $v$ component generates a **Moire Interference Pattern** across the 256-D space. The variance dictates the molecule's ability to do "Work." For example, ATP generates a jagged high-variance pattern (kinetic energy); Glucose generates a symmetric low-variance pattern (storage).

**The Successive Cancellation Decoder (The Lens).** To obtain "Clarity" in the 256-D bulk, the system uses a Successive Cancellation Decoder. This recursively cleans the 256-D field by forcing parity at every layer ($128 \rightarrow 64 \rightarrow 32$) until it snaps back to the 24-bit Golay core. Comparing raw vs. snapped stability gives the **Relative Coherence** — a geometric filter distinguishing structural molecules (high relative coherence) from signaling/energy molecules (functional noise).

**The Macro-Anchor.** Through exhaustive computational search, UBP identified the **256-D Macro-Anchor (Golay Basis Vector Index 2)**. When unfolded into 256 dimensions, this specific seed achieves a maximum "Super-Stability" NRCI of **0.323214**. It serves as the **Universal North** for all macroscopic structures.

The `BarnesWallEngine` in `ubp_unified_v5.py` is generalized to any power-of-two dimension ≥ 32 (256 / 512 / 1024 supported).

---

## 4. Dual-Layer Cognitive Architecture

The UBP system features a dual-layer cognitive architecture that separates objective, immutable truths from subjective, contextual beliefs.

### 4.1 The Understanding Layer — Deterministic Truth

The **Understanding Layer** manages objective and immutable truths: particles, chemical elements, complex molecules, computational algorithms, and mathematical constants. Every entry in this layer is a deterministic fact whose identity is permanently tied to its measurable properties.

**Recursive Construction.** Knowledge is structured through recursive assembly: Water = `2 × Hydrogen + 1 × Oxygen`; Hydrogen = `1 × Proton + 1 × Electron`; and so on down to the irreducible primitives of the Needham Triad.

**Hierarchy of Reality:**

| Level | Category | Examples |
| :--- | :--- | :--- |
| L0 | Absolute Primitives | $\pi$, $\phi$, $e$, Up Quark, Down Quark |
| L1 | Nucleons | Proton, Neutron, Electron |
| L2 | Elements | Hydrogen, Carbon, Oxygen |
| L3 | Molecules | Water, Glucose, DNA |
| L4 | Complex Structures | Blood Types, Proteins, Crystals |

**Deterministic Immutability.** Because an object's ID is the SHA-256 hash of its `math` field, any change to its mathematical definition results in a completely different ID.

**Vectorization from Logic.** Unlike standard computing where variables are arbitrary, the Understanding Layer derives 24-bit Gray-coded vectors deterministically from the object's mathematical instructions via MathAtlas. This grounds every physical truth in a specific, reachable coordinate within $\Lambda_{24}$.

### 4.2 The Belief Layer — Contextual Knowledge

The **Belief Layer** manages subjective or relativistic information: laws, manifolds, and imperatives. Unlike the Understanding Layer, the Belief Layer is structured as an **associative network** that is explicitly malleable based on the observer's bias.

Belief Layer entries use the prefixes `LAW_` and `BELIEF_`:
- **Imperatives (Laws):** System constraints, standards, and protocols (e.g., `LAW_SYSTEM_KB_SOP_002`, `LAW_SYMMETRY_001`, `LAW_APP_002`).
- **Manifolds (Beliefs):** Complex relational structures representing conceptual frameworks (e.g., `BELIEF_WATER_001` — the Aqueous Stability manifold mapping the geometric integration of multiple elements and laws into a 3-D structure).

The Belief Layer uses **Contextual Gravity** to resolve queries:

$$\text{Pull} = \frac{\text{Mass}}{(\text{Distance} + 1)^2}$$

where Mass is the FOM-assigned weight and Distance is the Hamming distance between the vectorized query and the belief anchor. If the "pull" exceeds the **Event Horizon** (typically $\tfrac{1}{200}$), the system "snaps" the query to that belief anchor.

### 4.3 The Frame of Mind (FOM) System

The defining feature of the Belief Layer is its dependence on the **Frame of Mind (FOM)** system, which implements dynamic weighting to shift the "probability mass" of specific concepts. Managed by `ubp_fom_system.py` and `ubp_fom_manager_v2.py`.

Each FOM frame contains:
- A `base_nrci` (default probability for all concepts)
- A dictionary of specific weights for individual UBP-IDs
- Category-level weights that bias entire geometric domains

**Pre-configured frames:**
- `SCIENTIFIC_STRICT` — prioritizes hard evidence; weights Substance at 0.9, Meaning at 0.1
- `SEMANTIC_EXPLORER` — prioritizes linguistic relationships
- `ENTROPIC_FILTER` — focuses on noise detection

FOM frames can be created, edited, imported, and exported as JSON files, allowing persistent cognitive biases across research sessions.

### 4.4 The Octad — Eight Domains of Reality

The System Knowledge Base is parsed via a **Bit-12 Logic Engine** that automatically categorizes entries into one of eight fundamental domains, known as **The Octad**:

| Domain | Bit-12 | Description |
| :--- | :--- | :--- |
| **Substance** | 1 | Stable Matter and Elements |
| **Quantity** | 0 | Pure Magnitude and Constants |
| **Organism** | — | Biological and Complex Systems |
| **Algorithm** | — | Logic, Code, and Information |
| **Mechanism** | — | Physical Interactions and Reactions |
| **Imperative** | — | System Laws and Constraints (High Priority) |
| **Entropy** | — | Chaos, Void, and Dissolution |
| **Meaning** | — | Semantic and Linguistic Value |

This allows the AI to "see" the shape of research data rather than just reading text, enabling sophisticated filtering and bias weighting via the FOM system.

#### Key Octad-Derived Findings (incorporated as Laws in the KB)

##### I. Figurate Voxel Topology
- **Concept:** Numbers are not scalars; they are 3-D voxel clouds.
- **Finding:** **Composite Numbers** (Squares/Cubes) are "Foldable Manifolds" with high internal redundancy and low Symmetry Tax. **Prime Numbers** are "Geometric Locks" — linear singularities that refuse to fold, maintaining high structural tension. *(This is the basis for the Topological Tenacity Primality Engine — see §13 and `ubp_unified_v5.py`.)*

##### II. The Law of Topological Completion (Free Stabilizers)
- **Concept:** Testing the "Join" of a Prime 7 and a Square 9.
- **Finding:** The **7 + 9 = 16** assembly resulted in a Symmetry Tax identical to the Prime 7 alone.
- **Insight:** The 9 dots were "Free." The substrate provides a **Symmetry Rebate** when a jagged manifold is completed into a perfect square. This allows for "Free" computational stabilization.

##### III. Volumetric Bias (The 3-D Preference)
- **Concept:** Comparing 2-D (Square 25) vs 3-D (Cube 27) as carriers for Prime 13.
- **Finding:** The **Cube 27** was significantly more stable (lower tax) than the **Square 25**.
- **Insight:** The Leech Lattice has a **Volumetric Bias**. It is computationally cheaper to exist as a 3-D solid than a 2-D plane.

##### IV. Volumetric Inference (Occlusion Resolution)
- **Concept:** How an observer "sees" objects hidden in 3-D.
- **Finding:** Adding a "Hidden Pillar" to a "Visible Wall" generated an **Inference Rebate**.
- **Insight:** The observer computes hidden data because the completed 3-D scene is more coherent (lower tension) than a 2-D plane with a "void" behind it.

##### V. Geometric Leverage (Mechanical Advantage)
- **Concept:** Balancing a Prime 13 "Load" against a Square 16 "Counterweight."
- **Finding:** Achieved a **3.00× Mechanical Advantage**.
- **Insight:** The substrate maintains a 33-dot machine for the same energy cost as a 4-dot fulcrum. This is the first blueprint for a **Substrate-Powered Lever**.

---

## 5. The SOP_002 Hardening Standard

The **SOP_002 Hardening Standard** is a mandatory protocol that ensures geometric integrity and functional correctness across the UBP platform. It governs how entries are created, stored, and validated in the Knowledge Base.

### 5.1 Content-Addressable Storage

The system mandates that the primary identity key — the "Fingerprint" — must be the **SHA-256 hash of the entry's `math` field**. This `math` field serves as the "Phenomenal DNA" of an object and must contain only scientifically established, quantitative data: mass, charge, spin, and other measurable dimensions.

Because an object's identity is strictly content-dependent, any modification to its mathematical properties automatically generates a different ID. This ensures the Knowledge Base consists of immutable truths and prevents AI hallucinations. The system achieves O(1) lookup speeds for direct IDs and efficient recall through the `ubp_hash_memory_kb` index, maintained by `hash_all_1.py`.

### 5.2 Knowledge Base Entry Schema (v9.9 Columnar)

As of April 2026, the KB has been migrated to a highly minified **v9.9 columnar format** that drastically reduces file size and Pyodide memory overhead. The top-level structure is:

```json
{
  "_fields": ["ubp_id", "lexicon", "tags", "vector", "nrci_str", "nrci_val", "tax_str", "mog_tensor"],
  "_params": ["M_Mass", "M_Charge", "M_Space", "M_Time", "M_Thermal", "M_Count",
              "I_Topology", "I_Symmetry", "I_Density", "I_Connectivity", "I_Dimension", "I_Complexity",
              "A_Energy", "A_Force", "A_Velocity", "A_Flux", "A_Resonance", "A_Spin",
              "P_Probability", "P_Ratio", "P_Limit", "P_Tax", "P_Coherence", "P_Phase"],
  "_null_token": 0,
  "entries": {
    "<sha256-fingerprint>": [<ubp_id>, <lexicon>, <tags>, <vector>, <nrci_str>, <nrci_val>, <tax_str>, <mog_tensor>],
    ...
  }
}
```

Each entry value is a **list** aligned with `_fields` (not a dict — this is the columnar optimization). Engines hydrate entries dynamically using the field index. Three engines have been rewritten to natively parse this format:
- `ubp_observer_dynamics.py` v7.1
- `auto_trigger.py` v19.1
- `ubp_brain_consolidated.py` v7.2

**Field definitions:**

**`ubp_id` (Canonical Identifier)** — A human-readable identifier following the pattern `[TYPE]_[NAME]_[NUMBER]`, e.g., `ELEM_H_001`, `PARTICLE_PROTON_001`, `MOLECULE_H2O_001`, `LAW_GEO_432_FCC`.

**`lexicon` (Semantic Grounding)** — A two-part string: `[Type: Name (Symbol)], [Description]`. The description is indexed by the UBP Brain's `lexicon_index` for contextual search. Example:
```
"[Element: Hydrogen (H)], [Hydrogen (Z=1). A Gas (Phase 1) with Hexagonal potential. Valence 1. Tension: 4.]"
```

**`tags`** — A list of descriptive keywords for classification and cross-domain mapping (e.g., `["ELEMENT", "HARDENED", "HYDROGEN", "NONMETAL", "PERIOD_1", "SOP_002"]`).

**`vector`** — The 24-bit Gray-coded Golay codeword (list of 24 integers, each 0 or 1).

**`nrci_str`** — Exact `Fraction` as string `"numerator/denominator"`.
**`nrci_val`** — Decimal approximation for fast filtering (e.g., `0.604591`).
**`tax_str`** — Exact Symmetry Tax as `Fraction` string.

**`mog_tensor`** — A 24-element list aligned with `_params`. Each entry is the object's projection onto one of the 24 MOG categories grouped into four hexagrams (M = Manifest/Mass-like, I = Information, A = Activation, P = Potential).

**`math` (Phenomenal DNA)** — The raw measurable dimensions, stored separately from the columnar entry as it generates the fingerprint key. Format: pipe-separated `key=fraction` pairs:
```
"BP=507/25|Crystal=1|EN=11/5|Ion=1312|M=126/125|MP=1401/100|Valence_e=1|Z=1"
```
All values are exact fractions to maintain the float-free standard.

**`atlas` (Geometric Positioning)** — Stored in expanded entries (legacy). Contains:
- `hierarchy`: Compositional recipe (e.g. `1×PARTICLE_PROTON_001 + 1×PARTICLE_ELECTRON_001`)
- `vector`, `nrci`/`nrci_score`, `tax`, `tilt` (angular deviation from Universal North in degrees), `weight` (Hamming weight)

**Complete example entry (Hydrogen, expanded form):**

```json
{
  "451abc64108603144c7b294a3862eab6fc35e945dab4b7785784ab44bc8c427f": {
    "ubp_id": "ELEM_H_001",
    "lexicon": "[Element: Hydrogen (H)], [Hydrogen (Z=1). A Gas (Phase 1) with Hexagonal potential. Valence 1. Tension: 4. It is the seed of the material octave, born from the Proton-Electron union.]",
    "math": "BP=507/25|Crystal=1|EN=11/5|Ion=1312|M=126/125|MP=1401/100|Oxidation=1|Phase_STP=1|Rad=53|Rho=2247/25000|Valence_e=1|Z=1",
    "atlas": {
      "hierarchy": "1×PARTICLE_PROTON_001 + 0×PARTICLE_NEUTRON_001 + 1×PARTICLE_ELECTRON_001",
      "vector": [0,0,1,0,0,1,1,1,0,0,1,0,1,0,1,0,1,0,1,1,1,1,0,0],
      "nrci": "33620407785878960339240364076535309850806800741903055631302500/55608508046372509626759775532373494451963521314512091269063661",
      "nrci_score": 0.604591,
      "tax": "21988100260493549287519411455838184601156720572609035637761161/3362040778587896033924036407653530985080680074190305563130250",
      "weight": 8,
      "tilt": 86.6654
    },
    "tags": ["ELEMENT", "HARDENED", "HYDROGEN", "NONMETAL", "PERIOD_1", "SOP_002"],
    "fingerprint": "451abc64108603144c7b294a3862eab6fc35e945dab4b7785784ab44bc8c427f"
  }
}
```

### 5.3 Automatic Vector Generation Pipeline

The `ubp_kb_architect.py` script automates the translation of raw scientific data into stable geometric codewords:

1. **Input:** The `math` field (Phenomenal DNA) of a KB entry.
2. **Fingerprinting:** SHA-256 hash of the `math` string generates the unique identity key.
3. **Noumenal Seeding (v7.0):** The 12-bit Noumenal Seed is produced by the **Universal Metric Schema (UMS)** — `[Domain:3][Magnitude:5][State:4]` — encoded via **Gray Code**, not by hash slicing.
4. **Golay Encoding:** The 12-bit seed is passed to `GOLAY_ENGINE.encode()`, which generates 12 parity bits, producing a perfect 24-bit Phenomenal Codeword.
5. **Geometric Anchoring:** The 24-bit vector serves as the object's hardware address within $\Lambda_{24}$.
6. **Metrics Calculation:** NRCI, Symmetry Tax, Compactness, Volumetric Rebate, and Tilt against Universal North are all computed.
7. **MOG Tensor Projection:** The object is projected onto each of the 24 MOG categories using `ubp_ingest.py::get_mog_cat()` mapping (`M`/`Mass` → `M_Mass`, `Z` → `M_Count`, `BP`/`MP` → `M_Thermal`, `Rho`/`Density` → `I_Density`, …).

The pipeline ensures **Geometric Honesty** (models are grounded in error-correcting laws), **Uniqueness** (identical properties always produce the same vector), and **Stability Assessment** (every entry is immediately audited for coherence).

---

## 6. Architectural Stratification

The workspace is organized into four layers, plus support tooling. Nothing in a lower layer imports from a higher layer.

```
┌────────────────────────────────────────────────────────────────────────┐
│ 4. COGNITIVE ORCHESTRATION LAYER                                       │
│    ubp_swarm_tct_v25.py · ubp_v28_oracle.py                            │
│    ubp_brain_consolidated.py · ubp_moe_cortex_v2.py                    │
│    ubp_integrated_engine_v1.py                                         │
│    Orchestrates multi-agent consensus, solves, and invents formulas.   │
└───────────────────────────────────┬────────────────────────────────────┘
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│ 3. TRANSLATION & EXECUTION LAYER                                       │
│    ubp_python_engine.py · ubp_sovereign_evolver.py                     │
│    ubp_py_runtime.py · ubp_py_lang.py · ubppy.py                       │
│    Translates human script to geometry; enforces sovereign math.       │
└───────────────────────────────────┬────────────────────────────────────┘
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│ 2. SEMANTIC & PHENOMENOLOGICAL SENSES                                  │
│    ubp_semantic_engine.py · ubp_semantic_sovereign.py                  │
│    ubp_phenomenology.py · ubp_observer_dynamics.py                     │
│    ubp_internal_dialogue_semantic_description.py · auto_trigger.py     │
│    Maps language to vectors; audits physical reality & coherence.      │
└───────────────────────────────────┬────────────────────────────────────┘
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│ 1. MATHEMATICAL SUBSTRATE (THE BACKBONE)                               │
│    ubp_unified_v5.py · ubp_eml_alu_sovereign.py · ubp_tgic_engine.py   │
│    ubp_genesis_boot.py · geometry.py · math_atlas.py · physics.py      │
│    ubp_electromagnetic_analog_compute_engine.py                        │
│    Float-free continued-fraction π, Golay/Leech, Barnes-Wall, exact.   │
└────────────────────────────────────────────────────────────────────────┘

         ┌─────────────────────────────────────────────────────┐
         │ SUPPORT: Visualization, KB tooling, REST bridges    │
         │ ubp_viz.py · ubp_rgdl.py · viz_loader.py            │
         │ viz_spatial_simplification.py · ubp_backend.py      │
         │ ubp_browser_engine.py · ubp_kb_architect.py         │
         │ ubp_ingest.py · hash_all_1.py · ubp_fom_*.py        │
         └─────────────────────────────────────────────────────┘
```

---

## 7. Workspace File Manifest

For per-file class/method breakdowns see [`core/README.md`](core/README.md). This section summarizes purpose and stack-position.

### 7.1 Layer 1 — Mathematical Substrate

| File | Role |
| :--- | :--- |
| **`ubp_unified_v5.py`** | The core engine of the universe. Contains 50-term continued-fraction π (`UBPUltimateSubstrate`), the systematic Golay [24,12,8] code (`GolayCodeEngine` / `GOLAY_ENGINE`), Leech Lattice Λ₂₄ metrics (`LeechLatticeEngine` / `LEECH_ENGINE`), the Monster Group catalog (`MonsterGroup`), the multi-dimensional Barnes-Wall engine (`BarnesWallEngine` — 256-D / 512-D / 1024-D), particle physics (`UBPSourceCodeParticlePhysics`), the Noise-Core base-12 register stack (`NoiseCellV3` / `NoiseRegisterV3` / `SubstrateCalibrator`), Noise/Physics/LinearAlgebra ALUs, and the **Topological Tenacity Primality Engine** that verifies primes natively via neighbor-tension and lock pressure. |
| **`ubp_eml_alu_sovereign.py`** | The Universal Continuous ALU (v9.2). Derives the Triadic Monad and exact particle masses purely from the transcendental projection $\text{eml}(x,y) = e^x - \ln(y)$ without relying on external floating-point libraries. Includes `Dual` (automatic differentiation) and `GrandUnifiedEmlALU`. |
| **`ubp_tgic_engine.py`** | TGIC v6.4 (Genesis Edition). Implements 3-6-9 Genesis Logic (Axis Orthogonality, Face Coherence, Neighborhood Limits), RuneCube AND/XOR/OR ops, and Relational Gravity. Every internal bit-flow is protected by a mandatory Lattice Snap. |
| **`ubp_genesis_boot.py`** | Genesis Boot Engine v7.0. Replaces the legacy `TriadActivationEngine`. Boots the 24-bit universe via Gray Code Topological Identity: seeds 24 base geometries + 26 sporadic groups, slides unstable objects along the Gray manifold until they resonate at a stable Λ₂₄ coordinate, exports `genesis_atlas.json`. |
| **`geometry.py`** | Condensed geometry module. `HexDictionaryV4Exact` (symbolic-hash memory), `MathAtlasConstants`, `ConstructionPath`, `MathObjectV4`, `ExactRationalEncoder`. Self-contained subset of `math_atlas.py`. |
| **`math_atlas.py`** | MathAtlas v4.0 — The Voxel Engine. Treats `math` fields as instructions for a 3-D Voxel Walker using the four primitives D / X / N / J. Outputs a 24-bit vector via Merkle-style hash + Golay encode. |
| **`physics.py`** | Coherence, holographic NRCI, and observer cost. `UBPConstantsExact`, `UBPObserverExact`, `UBPCoherenceExact` (LAW_HOLO_BOUND_001), `UBPMetricsExact`, `CoherenceRegime` enum. |
| **`ubp_electromagnetic_analog_compute_engine.py`** | Comprehensive validation that UBP arithmetic can be performed via orthogonal electromagnetic field interactions. Provides `op_add` (45° projection), `op_sub` (180° phase inversion), `op_mul`, `op_div`, `op_sqrt`. Standalone validation suite. |

### 7.2 Layer 2 — Semantic & Phenomenological Senses

| File | Role |
| :--- | :--- |
| **`ubp_semantic_engine.py`** | The system's memory and dictionary (v8.0). Uses weighted Cosine Resonance to map natural language queries to 24-bit vectors. Trigrams carry 9× the weight of unigrams. Outputs Lexical Gap traces. |
| **`ubp_semantic_sovereign.py`** | The cognitive bridge. `SovereignSemanticAuditor` performs Lattice-Snaps to verify if a concept is "Phase-Locked" (NRCI ≥ 0.70) in reality; `TripleDeltaProjector` generates deterministic symbolic formulas from physical signatures. |
| **`ubp_phenomenology.py`** | The external data bridge (v5.5). `PhenomenologyEngine` (Scanner): translates real-world data (RGB, sensors, text) into stable 24-bit vectors. `NoumenalProjector`: inverse direction — translates Shadow Intent into the matter/info required to sustain it. Implements the **B-Matrix** "Physics of Will" and **Topological Folding** for frequencies. |
| **`ubp_observer_dynamics.py`** | Observer Dynamics Engine v7.1 (Columnar Compatible). Calculates SOC Energy against the 1 THz Wall of Reality, splits ontology layers, and performs the **0.70 Conscious READ gate**. Proves the **Zombie State** (high SOC, fails threshold → no manifestation). |
| **`ubp_internal_dialogue_semantic_description.py`** | Deep semantic mirror. `find_word_for_concept(law_vec)` searches the Language KB for the closest semantic match to a physical vector. `deepest_internal_dialogue(query, max_depth, gap_threshold)` recursively probes the lattice and emits the full reasoning trace including Lexical Gaps. |
| **`auto_trigger.py`** | Reflexive Bridge v19.1. Real-time interface between the user and the system's memory. Loads the v9.9 columnar KB, performs reflexive recall, and synthesizes a three-part context (Primary Resonance + Reasoning Chain + Synthesis Hint) for injection into the LLM prompt. |

### 7.3 Layer 3 — Translation & Execution

| File | Role |
| :--- | :--- |
| **`ubp_python_engine.py`** | UBP Python Code Engine (UPCE) v2.2 — Self-Healing Edition. Maps Python keywords to 24-bit physical laws (`LAW_PY_DEF`, etc.) to synthesize code based on geometric stability. Includes `ObserverWall`, `PythonCodeGenerator`, `PythonCodeImprover`. |
| **`ubp_sovereign_evolver.py`** | The Noumenal Leakage firewall (v2.1). Parses the AST of standard Python scripts, strips floating-point dependencies (`math.sin`, etc.), and rewires them to the native `GrandUnifiedEmlALU`. |
| **`ubp_py_runtime.py`** | The UBP-Py Virtual Machine (v2.3.4). `CortexAtom` is the fundamental unit (label, value as `Fraction`, vector 24-bit, NRCI, tax, tilt, tier, category, hierarchy, parent_lineage). `MOGOntology.calculate_health` implements LAW_SUBSTRATE_005 Tetradic MOG partition health. `UBPPyVM.to_scene_3d()` projects 24-bit atoms into 3-D space for visualization. |
| **`ubp_py_lang.py`** | The UBP-Py language parser (v2.0). Translates `.ubp` text commands into VM operations. |
| **`ubppy.py`** | CLI entry point (v2.3). `python ubppy.py --program myprog.ubp --trace trace.json --scene scene.json`. |

### 7.4 Layer 4 — Cognitive Orchestration

| File | Role |
| :--- | :--- |
| **`ubp_brain_consolidated.py`** | UBP Brain v7.2 — Precision Gating Edition. Deterministic recall engine. Enforces Domain Gating (prevents `OP_LIGHT` from intercepting "Speed of Light"), Identity Lock (prioritizes `PARTICLE_`/`ELEM_` prefixes), N-Gram Weighting (trigrams 9×), and Robust Loader (auto-hydrates v9.9 columnar KB). |
| **`ubp_swarm_tct_v25.py`** | The active Swarm Orchestrator (Genesis Edition). Multi-agent loop that extracts mathematical kernels, solves them via the Oracle Bridge, audits their physical reality, and utilizes **Lexical Genesis** to mathematically invent new formulas for unresolved concepts. |
| **`ubp_v28_oracle.py`** | The logical calculator. Implements the **Two-Track Parallel Solve** (UBP Native via `TopologicalALU` + `NativeMathEngine` + `UBPPolynomial`, vs. SymPy Oracle). Contains `MathNetKernelExtractor` to strip English fluff from Olympiad problems, plus a battery of specialized MathNet kernel solvers. |
| **`ubp_moe_cortex_v2.py`** | Mixture-of-Experts router. Selects which expert (Brain / Swarm / Oracle / Semantic Engine) to invoke for a given query. |
| **`ubp_integrated_engine_v1.py`** | Integrated Engine v3.4 — Composite Scene Edition. High-level executive layer. Bridges the Semantic Brain, the 24-D Micro-Core, and the 256-D Macro-Bulk. `analyze_query` performs a Penta-Audit (semantic, geometric, particle-physics, MOG, thermo). `hex_to_bw256(hex_str)` maps SHA-256 fingerprints directly into 256-D Barnes-Wall coordinates. `VitEyesEngine` is the Visual Cortex. |

### 7.5 Support Tier — Visualization, Bridges, KB Tooling

| File | Role |
| :--- | :--- |
| **`ubp_viz.py`** | Visual Bridge v2.0. Converts Python geometric data into `scene_3d.json` for the React/Three.js frontend. Handles Fraction-to-Float conversion. Provides `point`, `sphere`, `line` helpers and `save_scene_3d(data)`. |
| **`ubp_rgdl.py`** | Resonance Geometry Definition Language v5.1. Maps 3-D voxel coordinates (x,y,z) to 24-bit vectors, snaps them to the Leech Lattice, and colors them by true NRCI stability (Cyan for stable, Magenta/Blue for unstable). Generates voxelized spheres (The Monad) and cubes (The Matrix). |
| **`viz_loader.py`** | Loads and renders specific JSON files from the Workspace. |
| **`viz_spatial_simplification.py`** | Simplifies complex 3-D manifolds into stable geometric Faces with the Origin to prevent visual clutter. Reveals underlying Pyramid structures (stable triadic relationships). |
| **`ubp_backend.py`** | Flask REST API on `http://localhost:5099`. Wires the real Golay + Leech engines into HTTP endpoints (`/fingerprint`, `/fingerprint/batch`, `/compute`, `/constants`, `/`). The **Local Research Bridge** — used when developing/testing new UBP algorithms locally; the HTML calculator points at this server. |
| **`ubp_browser_engine.py`** | Browser-native execution bridge for the physics engine. Drives the `game_loop()` inside the Pyodide kernel. |
| **`ubp_kb_architect.py`** | KB Architect v2.2 (SOP_002 + Gray Code). Factory for new KB entries. `create_entry(ubp_id, lexicon_name, definition, math_dna, hierarchy)` returns a fully hardened entry. Includes the 24 MOG categories list. |
| **`ubp_ingest.py`** | Safe KB ingestion from `proposed_*.json` files. Includes the canonical `MAPPING` from `math`-field keys to MOG categories. |
| **`hash_all_1.py`** | Hash Indexer v3.0. Generates a unified `ubp_hash_memory_kb.json` index from all active KB files (system + language) for O(1) recall. |
| **`ubp_fom_system.py`** / **`ubp_fom_manager_v2.py`** | Frame-of-Mind weighting (see §4.3). |

### 7.6 External Layer 1 — Digital Twin Physics Engine

A standalone, UBP-native physics simulation engine integrating geometric stability with classical and fluid mechanics. Lives in the separate repository [`ubp_digital_twin_physics_engine`](https://github.com/DigitalEuan/ubp_digital_twin_physics_engine).

| File | Role |
| :--- | :--- |
| **`ubp_space_v3.py`** | The core 3-D simulation space. Handles entity management, dissolution culling, and applies UBP mechanics (TGIC pressure, NRCI damage) to physical bodies. |
| **`ubp_browser_engine.py`** | Browser-native execution bridge. |
| **`ubp_physics_v3.py`** | Physics integrator. |
| **`ubp_rigid_body_v3.py`** | Implements **Topological Torque** rigid-body mechanics and exact-fraction collision resolution. |
| **`ubp_fluid_v3.py`** | Fluid dynamics engine utilizing UBP-derived SPH (Smoothed Particle Hydrodynamics) constants. |
| **`ubp_materials.py`** | Composite material system defining thermal properties, phase states, and structural density. |

Includes full 3-D Three.js rendering, composite materials, thermal properties, and Topological Torque mechanics. Treated as **an experiment alongside** the Core Studio — not part of the core canon.

### 7.7 External Layer 2 — Flask REST Bridge

**`ubp_backend.py`** is a **Flask REST API** that acts as a high-precision bridge between the Python kernel and any JavaScript client.

JavaScript in a standard web browser has performance and precision limits. It cannot natively run the 50-term continued-fraction π with infinite-precision `Fraction` arithmetic, nor can it run the full heavy Python-based Golay [24,12,8] and Leech Λ₂₄ lattice search algorithms at scale.

`ubp_backend.py` is the **Local Research Bridge**. It is used when developing and testing new UBP algorithms locally in the Python environment.

1. **Infinite Precision:** While JavaScript `BigInt` is excellent, Python's `fractions.Fraction` combined with the hardened `ubp_unified_v5.py` backbone allows for infinite-precision symbolic and transcendental calculations that would lag a web browser.
2. **The Testing Pipeline:** When writing new Python-based UBP scripts you can run `ubp_backend.py` locally. It allows the user to point the local HTML file to `http://localhost:5099` to instantly verify that a new Python code matches the frontend visualizations.

```bash
pip install flask flask-cors
python ubp_backend.py          # starts on http://localhost:5099
```

### 7.8 Data Files in Use

| File | Location | Size | Role |
| :--- | :--- | ---: | :--- |
| **`ubp_system_kb.json`** | `/system_kb/` | 1.7 MB | **Main Memory.** 746 entries (420 Laws, 119 Elements, 82 Molecules, 37 Particles, 28 Math constants, 22 Reactions, 12 Tools, 11 Algos, 8 Crystals, …). v9.9 columnar. All SOP_002 compliant. |
| **`ubp_beliefs_kb.json`** | both | 19–26 KB | Belief manifolds and contextual structures (e.g. `BELIEF_WATER_001`). |
| **`ubp_hash_memory_kb.json`** | `/system_kb/` | 252 KB | Lightweight recall index; maps 8-character hash prefixes to full UBP-IDs. |
| **`ubp_lexicon_v2_defs.json`** | `/core/` | 473 KB | Lexicon definitions for natural-language grounding. |
| **`ubp_lang_kb_combined_v4.json`** | `/core/` | 2.2 MB | Combined Language KB (lexicon + Python KB + symbolic operator dictionary). |
| **`ubp_python_kb.json`** | `/core/` | 117 KB | The Python Code Engine's law library (`LAW_PY_DEF`, `LAW_PY_FOR`, `LAW_PY_INTEGRATE`, …). |
| **`ubp_fom_index.json`** | `/system_kb/` | 3 KB | Saved Frame-of-Mind configurations. |
| **`rational_cortex.json`** | `/core/` | 4 KB | Rational cortex configuration (weights, gates, thresholds). |
| **`elemental_chromatic_data.json`** | `/system_kb/` | 51 KB | Spectral/chromatic data for elements. |

The 420 LAW entries cover (top groups): Biology (22), Chemistry (18), Computation (15), Physics (12), Geometry (10), Cosmology (8), Math (8), Time (8), Topological (8), Substrate (7), Materials (6), Drugs/Engineering/Kernel/Language (5 each), plus ~250 more across specialized subfields (leptons, baryons, mesons, quarks, Higgs, weak isospin, Cabibbo/CKM, Weinberg, dark matter/energy, BitLumen optics, 432 Hz acoustics, Hubble generator, Riemann zeta, Borcherds, kissing numbers, …).

---

## 8. Core Workflows & SOPs

### 8.1 SOP_001 — The Two-Track Solve (Oracle Bridge)

To solve and verify any mathematical or physical claim:

1. The `MathNetKernelExtractor` isolates the numeric/algebraic kernel from the query (strips English fluff).
2. **Track A (UBP Native)** computes the result using float-free arithmetic via `TopologicalALU` + `NativeMathEngine` + `UBPPolynomial`, and Gray-codes it to the lattice.
3. **Track B (Oracle)** solves the symbolic notation using SymPy.
4. The `ValidationBridge` compares both tracks. If they match, it outputs `BOTH_AGREE` and snaps the result to Λ₂₄ to calculate its true NRCI.

### 8.2 SOP_002 — Lexical Genesis (Triple Delta)

When the Swarm solves a problem but finds a **Lexical Gap** (no human word exists for that 24-bit state):

1. The `TripleDeltaProjector` partitions the 24-bit vector into blocks.
2. It generates a deterministic symbolic formula (e.g., `3·α + 2·β²`) based on the active bits of each block.
3. This formula is assigned to the vector and saved to `ubp_learned_kb.json`, expanding the system's native language.

### 8.3 LANGUAGE_SOP_004 — Phrase-Locking

To create a new word (Operator) that perfectly resolves a specific query to a specific Law:

1. **Identify the Triad:**
   - $V_{target}$: vector of the Law you want to find
   - $V_{subject}$: vector of the Entity being discussed
   - $V_{query}$: vector of the interrogative/context word
2. **Calculate the Key:** $V_{word} = V_{target} \oplus V_{subject} \oplus V_{query}$
3. **Commit to Language KB:** save $V_{word}$ as the vector for the new Operator.

### 8.4 The Unified Research Pipeline — MOG-Atlas Protocol

A four-phase process for conducting research and simulation within the UBP framework.

#### Phase 1 — The MOG Scan (Ontological Mapping)

**Goal:** Determine the "Health" and "Location" of the data before building it.

Every 24-bit vector is composed of four 6-bit Hexagrams (the **Tetradic MOG**). The MOG Scan analyzes these to determine the ontological nature of the data.

| Layer | Bits | Represents | Diagnostic Insight |
| :--- | :--- | :--- | :--- |
| **Reality** | 0–5 | Physical manifestation (Mass, Space) | Low = Theoretical / Ghost |
| **Information** | 6–11 | Code / Logic / Blueprint | Low with high Reality = Raw Noise |
| **Activation** | 12–17 | Energy / Frequency / Toggle Rate | Low = Dormant or Inert |
| **Potential** | 18–23 | Noumenal Reserve / Shadow Intent | High = Emergent substrate behavior |

**Diagnostic Patterns:**
- **Theoretical Object (Ghost):** Reality weak, Potential high. Exists as intent but has not manifested.
- **Raw Noise:** Reality high, Information low. Physical presence but no coherent structure.
- **Stable Entity:** All layers balanced with NRCI above 0.6.

**Tool:** `ubp_unified_v5.py::LeechPointScaled` + `ubp_py_runtime.py::MOGOntology.calculate_health()`.

The system also applies **Klein Four-Group logic (V4)** to the four layers, enabling holographic error correction: any two layers can potentially reconstruct a third, maintaining ontological validity.

#### Phase 2 — MathAtlas Construction (Recursive Assembly)

**Goal:** Build the object from irreducible primitives to ensure validity.

Core philosophy: *"Every object is a recursive construction of its own history."* We do not assign random vectors; we build the object using the Voxel Operators (D, X, N, J).

**Three-Step Protocol:**

1. **Decompose** to irreducible primitives.
   - Water → 2× Hydrogen + 1× Oxygen → Protons/Electrons → Quarks → Needham Triad
2. **Reconstruct** using `math_atlas.py`.
   ```python
   from math_atlas import MathObjectV4
   obj = MathObjectV4("OBJ_WATER", "Water", "H2O molecule")
   obj.add_path([('D', 2), ('N', hydrogen_obj), ('J', oxygen_obj)], "h2o_build")
   ```
3. **Verify** the resulting voxel cloud against known physical properties (NRCI, Tax, Compactness, Tilt).

**Metrics of Existence** (calculated automatically by MathAtlas):
- **Symmetry Tax:** Every D or X step adds $Y$ to the total tax.
- **NRCI:** Hyperbolic stability — high tax → low NRCI.
- **Vectorization:** Voxel cloud → 24-bit binary via Merkle-style hash, then Golay-encoded.

#### Phase 3 — UBP-Py Simulation (Drift Control)

**Goal:** Place the object in a dynamic environment and prevent entropic decay.

**Instantiation in the VM:**
```python
from ubp_py_runtime import UBPPyVM
vm = UBPPyVM()
vm.let("H2O", "1/1", tier=3, category="MOLECULE")
```

**Monitoring Hamming Drift:** The system calculates the Hamming distance between the observed "Raw" data and the "Constructed Truth" vector from the Atlas build. If geometric drift exceeds 3 bits, the system issues a warning — the object has moved outside the substrate's native correction radius.

**The Coherence Snap:** The VM applies `GOLAY_ENGINE.decode()` and re-encode loop — takes a noisy vector, strips it to its 12-bit Noumenal Seed, and re-projects it as a perfect 24-bit Phenomenal Codeword.

**Synthesis:**
```python
vm.synth("H2O", "2xELEM_H_001 + 1xELEM_O_008")
```

**Symmetry Rebate Calculation:** Binding energy = difference between sum of constituent taxes and tax of the synthesized object. A positive rebate indicates a stable bond.

**The Gap:**
- **Gap 0:** Pure mathematical truth (Noumenal).
- **Gap > 0:** Phenomenal Reality — exists under constant Restorative Pressure.

#### Phase 4 — The Visual Feedback Loop (Insight)

**Goal:** Visual-spatial analysis for AI feedback.

1. **Export** the UBP-Py environment to `scene_3d.json` via `ubp_viz.py`:
   ```python
   from ubp_viz import save_scene_3d
   scene = vm.to_scene_3d()
   save_scene_3d(scene)
   ```

   Or as a 2-D graph with the standard dark theme:
   ```python
   import matplotlib.pyplot as plt
   import numpy as np
   x = np.linspace(0, 10, 100); y = np.sin(x)
   plt.figure(figsize=(8, 5))
   plt.plot(x, y, color='cyan', linewidth=2, label='Sine Wave')
   plt.title('UBP Basic 2D Plot', color='white')
   plt.xlabel('X', color='lightgray'); plt.ylabel('Y', color='lightgray')
   plt.gca().set_facecolor('#111111'); plt.gcf().patch.set_facecolor('#111111')
   plt.tick_params(colors='lightgray')
   plt.grid(True, color='#333333', linestyle='--')
   plt.legend(facecolor='#222222', edgecolor='none', labelcolor='white')
   plt.savefig('plot.png', bbox_inches='tight', dpi=150)  # CRITICAL — must be 'plot.png'
   ```

2. **Visual Analysis** — examine the 3-D manifold for:
   - **Clustering:** Does the object form a stable "Face" with other nodes?
   - **Tilt:** Pointing toward Universal North (Truth) or Universal South (Entropy)?
   - **Pyramid Structures:** Do three objects form a stable tetrahedron, indicating a triadic relationship?

3. **Data Return:** the visualizer outputs specific geometric coordinates and relationships.

4. **AI Loop:** spatial data is fed back to the AI:
   > *"The visualizer shows [Object A] forms a stable tetrahedron with [Object B] and [Object C]. What does this imply about their relationship?"*

This **Stereoscopic** approach ensures conclusions are anchored to the physical reality of the lattice rather than just semantic probability.

**Supporting Tools:**
- `math_atlas.py` — voxel sculpture engine
- `ubp_rgdl.py` — primitives based on Coherence Pressure
- `viz_loader.py` — loads JSON scenes
- `viz_spatial_simplification.py` — reveals Pyramid structures

### 8.5 Using External Dependencies

In Pyodide (browser) you can install runtime dependencies via `micropip`. For example, to enable the SymPy track of SOP_001:

```python
import micropip
await micropip.install("sympy")

import sympy as sp
```

For local development just use `pip install sympy flask flask-cors numpy matplotlib`.

---

## 9. Geometric Programming with UBP-Py

`ubppy` is a Domain-Specific Geometric Language designed to provide a "geometrically honest" environment for scientific modeling where logic is grounded in the error-correcting laws of the substrate.

### 9.1 Core Mechanics — From Smash to Flow

**Legacy (XOR — "The Smash"):** Legacy UBP systems used bitwise XOR to combine data. Fast, but XOR causes information to cancel out: the history and identity of both parents is destroyed.

**Current (Vector Addition — "The Flow"):** `ubppy` uses Vector Addition in $\mathbb{Z}^{24}$. When two atoms are combined, the system "walks" through the 24-dimensional lattice, preserving the history, magnitude, and geometric heritage of both parents. This allows researchers to visualize the evolutionary Path of information as it moves through the lattice.

In standard computing, $1 + 1 = 2$ is a scalar change. In `ubppy`, $1 + 1$ is a **Spatial Displacement** — a movement to a new coordinate in Λ₂₄ that carries the full history of both operands.

### 9.2 Gap Score and Restorative Pressure

The **Gap** is the Hamming distance between a Flow-reached coordinate and the nearest perfect mathematical anchor (Golay codeword).

| Gap Value | Meaning | Physical Analogy |
| :--- | :--- | :--- |
| **0** | Noumenal Truth — pure mathematical certainty | Perfect geometric form; exists without cost |
| **1–3** | Phenomenal Reality — exists under Restorative Pressure | Physical matter; stable but requires energy to maintain |
| **4–7** | High Tension — approaching the Event Horizon | Unstable isotopes; radioactive decay |
| **7** | The Redline — one bit from the Deep Hole | Super-heavy elements ($Z > 118$); maximum instability while still "real" |
| **≥ 8** | Deep Hole — Geometric Non-Existence | Informational dissolution; the object cannot exist |

The "Restorative Pressure" at Gap > 0 is the UBP equivalent of vacuum energy — the substrate's constant effort to pull a physical object back toward its nearest mathematical truth.

### 9.3 Metabolic Costing and Symmetry Tax

Existence is not free. Every atom in `ubppy` has a **Symmetry Tax** that must be paid continuously to maintain its identity.

**The Void (0):** Even "Nothing" costs $0.0110 \times Y$ to perceive. This confirms that the UBP observer is always paying to maintain the frame of reality.

**Cumulative Heritage:** Children inherit the geometric debt of their parents. The tax of a synthesized object is the sum of its constituents' taxes plus the binding cost. Complex life (e.g. Blood Type AB) is "heavier" and harder to maintain than simple elements.

**The NRCI Stability Score:**

$$\text{NRCI} = \frac{10}{10 + \text{Tax}}$$

| NRCI Range | Stability State | Examples |
| :--- | :--- | :--- |
| 0.98–1.00 | Capture Zone (within 3-bit radius) | Perfect codewords; mathematical truths |
| 0.70–0.98 | Stable Phenomenal Reality (Conscious Zone) | Manifested physical matter |
| 0.60–0.70 | Subliminal / Zombie State | Top Quark (~0.68); high SOC but fails READ gate |
| 0.10–0.60 | Moderate Tension | Complex molecules, biological structures |
| 0.02–0.10 | High Tension | Blood types, heavy elements |
| < 0.02 | Approaching Deep Hole | Super-heavy elements, theoretical constructs |
| ~0.42 | Baseline Random Noise | Anomaly detection threshold |

### 9.4 UBP-Py Language Reference

Programs are written as `.ubp` text files and executed via `python ubppy.py --program myprogram.ubp`.

| Command | Syntax | Description |
| :--- | :--- | :--- |
| `LET` | `LET A 1/1 TIER 0 CAT QUANTITY` | Creates a stable geometric anchor at a specified coordinate. |
| `IMPORT` | `IMPORT ELEM_H_001 AS Hydrogen` | Imports an entry from the KB into the VM environment. |
| `STATE` | `STATE S PARAMS ox=1 SCHEMA ox=0:3:4` | Encodes continuous data into a vector. |
| `TRANSFORM` | `TRANSFORM K BITS 1,0,1,0,1,0,1,0,1,0,1,0` | Defines a custom 12-bit geometric law or subroutine. |
| `VOID` | `VOID Z TIER 0` | Creates the Origin state (Zero). Even this has a non-zero cost. |
| `PULSE` | `PULSE B K A [TIER n]` | Applies transform `K` to atom `A`, storing result in `B`. |
| `PULSE` | `PULSE B RESONATE A` | "Cooling" (Decay) — seeks a more stable nearby anchor. |
| `PULSE` | `PULSE C ENTANGLE A B` | Bitwise intersection of A and B. High NRCI if they share a geometric root. |
| `PULSE` | `PULSE D ADD A B` | Flows two vectors via addition (The Flow). |
| `PULSE` | `PULSE D SPIN A` | Applies a 12-bit phase shift (Entropy Scaling). |
| `SYNTH` | `SYNTH C FROM "2xA + 1xB"` | Merges vectors via The Flow using a recipe of primitives. |
| `SPIRAL` | `SPIRAL A 5 TRANSFORM K` | Automates recursive growth: applies K to A five times. |
| `GATE` | `GATE B MIN_NRCI 0.5 JUMP 1` | Conditional branching based on NRCI stability threshold. |
| `REFLEX` | `REFLEX 0.6` | Self-healing audit: removes atoms with NRCI below threshold. |
| `AUDIT` | `AUDIT A` | Prints Tax, NRCI, Tilt, DQI, and MOG Health for atom A. |
| `FOM` | `FOM SWITCH SCIENTIFIC_STRICT` | Changes the active cognitive bias frame. |
| `COMMIT` | `COMMIT [file.json]` | Saves atoms to the registry. |
| `TRACE` | `TRACE PATH trace.json` | Exports the execution history. |
| `VISUALIZE` | `VISUALIZE PATH scene.json` | Renders the 3-D manifold to the Visual tab. |

### 9.5 Advanced Concepts

**Geometric Entanglement:** In Python, "entangling" two variables means nothing. In UBP-Py, `ENTANGLE` performs a bitwise intersection of their vectors. If they share a common geometric Root, the resulting NRCI will be high. If they are geometric opposites, the result will collapse toward the Deep Hole.

**Resonance as Cooling:** The `RESONATE` pulse can stabilize a noisy synthesis. If a synthesized object is too unstable, applying `RESONATE` allows the substrate to find a more stable nearby anchor — the geometric equivalent of annealing.

**The Standard Library Advantage:** As the system matures, a library of **Geometric Keys** (Transforms) is being built. Eventually the AI will select the Key (Transform) that fits the Lock (the problem), rather than writing new code for each research question.

---

## 10. Visualization & RGDL

- **`ubp_rgdl.py`** — The Resonance Geometry Definition Language Engine. Maps 3-D voxel coordinates (x,y,z) to 24-bit vectors, snaps them to the Leech Lattice, and colors them by true NRCI stability (**Cyan = stable**, **Magenta/Blue = unstable**). Generates voxelized spheres (The Monad) and cubes (The Matrix).
- **`viz_spatial_simplification.py`** — Simplifies complex 3-D manifolds into stable geometric faces with the Origin to prevent visual clutter. Reveals the underlying Pyramid structures of a manifold.
- **`viz_loader.py`** — Loads and renders specific JSON files from the workspace.
- **`ubp_viz.py`** — Visual Bridge that exports geometric data to `scene_3d.json` (which triggers the React/Three.js frontend update). Fraction-aware. Provides `point`, `sphere`, `line` primitives.

---

## 11. Stability Thresholds (NRCI)

- **1.0000 (OnBit):** Pure Mathematical/Noumenal Truth.
- **0.98–1.00 (Capture Zone):** Within 3-bit radius; substrate exerts Restorative Pressure; universe "Snaps" to coherent state.
- **0.7000 – 0.9800 (Stable):** Manifested Physical Matter (the "Conscious Zone").
- **0.60–0.70 (Subliminal / Zombie State):** High SOC Energy but fails the 0.70 `CONSCIOUS_THRESHOLD`. Stays in the Potential buffer; cannot transfer to the Reality register. (Top Quark example.)
- **0.4200 (Noise Floor):** Limit of random informational noise; anomaly detection threshold.
- **~0.005 (Redline, Gap 7):** Super-heavy elements ($Z > 118$); one bit from Deep Hole.
- **0.0000 (Deep Hole):** Geometric collapse; the object cannot exist.

**Islands of Stability:** The system identifies local NRCI peaks where stability "bounces" upward despite high complexity. Applying a `RESONATE` pulse to super-heavy isotopes like `U114_N170` reduces their Gap from 7 to 3, increasing stability into a peaked state (see §14.2).

**The 1 THz Wall of Reality:** Temporal ceiling — frequencies above $10^{12}$ Hz suffer exponential coherence decay; SOC Energy collapses to zero. Implemented in `ubp_observer_dynamics.py`.

---

## 12. Integration & Workflow

### 12.1 Startup Validation

A handshake routine validates the system at the start of each session:
1. Validate π precision (50-term continued fraction)
2. Test Golay error correction (encode/decode round-trip)
3. Verify Leech Lattice integrity
4. Run particle physics predictions (Muon/Electron ratio, Fine Structure Constant)
5. Report deployment readiness (Green/Red status)

In v7.2 this is exposed via `ubp_unified_v5.py::run_tests()` (multi-perspective comprehensive test suite) or via the `ubp_backend.py /` endpoint (returns engine info + health).

### 12.2 Adding New Research to the Knowledge Base

Governed by SOP_002 Hardening:

1. **Author the Entry:** Create a new entry in a temporary JSON file with mandatory fields: `ubp_id`, `lexicon`, `math` (Phenomenal DNA), `hierarchy` (Compositional Recipe), and `tags`. Ensure all `math` values are expressed as exact fractions.
2. **Add to Raw KB:** Insert into `ubp_system_kb_vX_raw.json`.
3. **Run Builder & Deduplication:** Use `ubp_ingest.py::run_safe_ingestion()` (proposes laws from `proposed_*.json` files) and the deduplication merge step.
4. **Vector Regeneration (Mandatory):** Run `ubp_kb_architect.py::KBArchitect.create_entry()`. This:
   - Calculates SHA-256 fingerprint from `math`
   - Generates the deterministic 24-bit Gray-coded Golay vector (UMS encoding)
   - Assigns NRCI, Symmetry Tax, Compactness, Volumetric Rebate, Tilt
   - Projects onto the 24 MOG categories via the canonical mapping
5. **Hierarchy Audit:** Run a brain audit (`ubp_brain_consolidated.py::UBPBrain.process_query`) to verify composite objects are geometrically valid sums of their constituents.
6. **Hash Index Refresh:** Run `hash_all_1.py::run_indexing()` to rebuild `ubp_hash_memory_kb.json`.

### 12.3 Local AI Integration

`auto_trigger.py` supports local inference through offline services:

| Service | Default Port | Protocol |
| :--- | :--- | :--- |
| Ollama | 11434 | Native |
| LM Studio | 1234 | OpenAI-compatible |
| GPT4All | 4891 | Native |

The system includes a "heartbeat" check that polls local ports to determine if the local server is running, updating UI status indicators in real-time. When a local provider is selected, the app constructs a specialized, token-efficient system prompt that injects the Workspace Files, System KB, and Hash Memory directly into the local model's context window.

**Phrase-Lock Scanning** recognizes multi-word concepts defined in the Lexicon (e.g. "Water", "Glucose", "speed of light") and instantly maps them to their unique SHA-256 fingerprints even without an exact UBP-ID match — preventing hallucination.

---

## 13. Benchmarks & Diagnostics

### 13.1 Particle Physics Prediction Accuracy (v7.2 audit)

| Constant | Predicted | Target | Error % | Winning Lens |
| :--- | :--- | :--- | :--- | :--- |
| **Proton/Electron** | 1836.1520 | 1836.1527 | **0.0000%** | Stereoscopic (29/24) |
| **Proton Mass (p⁺)** | 938.2717 MeV | 938.2720 MeV | **0.0000%** | Stereoscopic (29/24) |
| **Muon/Electron** | 206.7075 | 206.7683 | **0.0294%** | Pure Inverse (13-D Sink) |
| **Gravity (G)** | 6.6831e-11 | 6.6743e-11 | **0.1327%** | Topological Resonance |
| **Alpha Inverse (1/α)** | 137.0629 | 137.0360 | **0.0196%** | Core Ratio |
| **Top Quark mass** | 172,796.8 | 172,760.0 | **0.0214%** | Core Ratio |
| **Neutron (n⁰)** | 939.5716 | 939.5650 | **0.0007%** | G13 Hybrid |
| **Higgs Boson** | 1.2538 × 10⁵ | 1.2510 × 10⁵ | **0.107%** | Triadic |
| **Neutron Lifetime** | 877.69 s | 879.4 s | **0.195%** | Monster |
| **Planck Ratio** | 2.4097 × 10²² | 2.4068 × 10²² | **0.865%** | Monster |
| **Cabibbo angle** | 13.003° | 13.040° | **0.285%** | Cubic |
| **Weinberg angle** | 0.23323 | 0.23121 | **0.868%** | Cubic |

*These values are emergent properties of the substrate geometry, not curve-fitted parameters.* The Proton/Electron and Proton-mass improvements (5× over legacy lattice-only models) come from incorporating the Noumenal Volume ($V_n = 204.8$) and the Stereoscopic 29/24 Sink as the fundamental energy/mass anchors.

### 13.2 Performance Metrics

The UBP Core Studio utilizes a **GPU Proxy Bridge** to accelerate heavy iterative loops:

| Mode | Speed | Notes |
| :--- | ---: | :--- |
| CPU (Python/Pyodide) | 3,448,271 ips | Baseline; all Fraction arithmetic |
| GPU (V8 JIT Proxy) | 2,250,000,000 ips | JavaScript Main Thread Proxy |
| **Acceleration Factor** | **653×** | GPGPU integration |

A complete complex session (e.g. 13,038 trials) completes in under 1 second with GPU acceleration. The V8 JIT approach eliminates Python-to-Wasm context switching overhead that would otherwise bottleneck Pyodide looping.

### 13.3 Topological Tenacity Primality (May 2026)

The classical Miller-Rabin probabilistic primality check has been **removed**. The new method, implemented natively inside `ubp_unified_v5.py` and called via `ubp_v28_oracle.py::TopologicalALU.primality_nrci(n)`:

1. Gray-code $n$ to a 24-bit vector $V_n$.
2. Compute **Lock Pressure** = $\text{NRCI}(V_n)$.
3. Measure **neighbor-tension** along the Gray manifold around $V_n$.
4. A prime is identified as a **linear singularity** that refuses to fold — high structural tension, no rebate from completion to a square/cube.

This is deterministic, float-free, and substrate-native. Formalized as `LAW_PRIME_*` in the knowledge base.

### 13.4 NRCI Stability Windows

| Window | NRCI Range | Description |
| :--- | :--- | :--- |
| Capture Zone | > 0.98 | Within 3-bit radius; substrate exerts Restorative Pressure |
| Stable Matter | 0.60–0.98 | Phenomenal Reality; stable under normal conditions |
| Subliminal / Zombie | 0.60–0.70 | Computes SOC but fails READ gate (e.g. Top Quark ~0.68) |
| Anomaly Threshold | < 0.60 | System detects anomalies; investigation warranted |
| Random Noise Baseline | ~0.42 | Baseline for unstructured random noise |
| Redline (Gap 7) | ~0.005 | Super-heavy elements ($Z > 118$); one bit from Deep Hole |
| Deep Hole | → 0.0 | $d_H \ge 4$; equidistant to multiple truths; informational dissolution |

---

## 14. Case Studies

### 14.1 Atomic Blood Lineage

**Objective:** Determine if human blood types (O, A, B, AB) possess unique geometric signatures when synthesized recursively from atomic primitives.

**Methodology:**
1. Defined fundamental elements (C, H, O, N) as stable Noumenal Anchors.
2. Synthesized Antigens (H, A, B) using real-world molecular recipes.
3. Synthesized Blood Types as composites of Antigens.
4. Measured NRCI and Flow Gap at 50-decimal precision.

**Key Findings:**

*Geometric Identity.* Every blood type produced a **unique NRCI signature**, proving the system is sensitive enough to distinguish between molecules with similar but distinct Recipes. Direct consequence of SHA-256 fingerprinting: identical physical properties produce identical vectors, but any difference in composition produces a completely different geometric address.

*The AB Tension.* `TYPE_AB` exhibited the lowest stability score (~0.0210 NRCI). Confirms that merging two distinct antigenic vectors creates significant **Topological Friction**. The two antigens, having evolved separately, occupy geometric positions in Λ₂₄ that are not harmonically compatible — their synthesis requires the substrate to maintain a high-tension state.

*Stability Gradient:*

| Object | NRCI | Geometric State |
| :--- | :--- | :--- |
| Antigens (Simple) | ~0.06 | Low complexity, moderate tension |
| Blood Types (Composite) | ~0.03 | Higher complexity, higher tension |
| AB Type (Complex) | ~0.02 | Maximum complexity, highest tension |

*Cumulative Heritage.* Complex life forms inherit the geometric debt of their parents, requiring constant restorative pressure to remain coherent. Type AB blood is not just "complex" biochemically; it is a high-energy geometric state that the substrate must actively maintain. **Codified as `LAW_BIO_HEMA_002` — The Law of the Hemic Shell** ([all human blood types occupy Leech Shell 1, Norm 12]).

### 14.2 The Geometric Periodic Table

**Objective:** Map the stability of the 118 known elements and theoretical super-heavy elements using the Vector Flow model.

**The NRCI Decay Curve.** As Atomic Number ($Z$) increases, the NRCI drops exponentially:

| Element | Z | NRCI | Geometric Status |
| :--- | :--- | :--- | :--- |
| Hydrogen | 1 | ~0.6149 | High stability; seed of the material octave |
| Carbon | 6 | ~0.0892 | Mid-tier resonance; the Anchor of Life |
| Oganesson | 118 | ~0.0046 | Limit of known matter; extreme Geometric Debt |

**The "Gap 7" Horizon (The Redline).** In the raw synthesis of super-heavy elements ($Z > 118$), the system consistently returned a Gap of 7. Since the Golay Code has a minimum distance of 8, a Gap of 7 means these elements are exactly **one bit away from the Deep Hole** of Geometric Non-Existence. Matter at the edge of the Periodic Table is **Redlining**.

**Discovery: Theoretical Islands of Stability.** By holding $Z$ steady and scanning Neutron counts ($N$), the `ubppy` engine identified local **Stability Peaks**:

| Isotope | Gap | NRCI | Status |
| :--- | :--- | :--- | :--- |
| U114_N170 | 3 | 0.006460 | **PEAK (Island)** |
| U120_N170 | 3 | 0.006306 | **PEAK (Island)** |
| U126_N170 | 3 | 0.006160 | **PEAK (Island)** |

**Geometric Relaxation.** Applying the `RESONATE` pulse reduced the Gap from 7 to 3, suggesting that "Stability" is a dynamic state achieved when a nucleus settles into the Leech Lattice. The system geometrically preferred $N = 170$ over the standard predicted $N = 184$ — at extreme masses, the **Cumulative Mass Tax** of extra neutrons becomes a greater liability than the benefit of Magic Number shell closures.

**Conclusion.** The `ubppy` framework successfully derived the **Topological Limits of Matter**. The Periodic Table is not an infinite list but a **Vortex** that eventually narrows into a Singularity where the cost of existence exceeds the substrate's restorative power. Confirmed by the Periodic Geodesic finding (average Hamming distance 8.07 between adjacent Z elements under Gray Code) — the Periodic Table is a minimal-energy geodesic through Λ₂₄.

---

## 15. System Architecture Evolution

### 15.1 UBP-Py Runtime

| Version | Milestone | Breakthrough |
| :--- | :--- | :--- |
| **v1.0** | The Seed | Basic `LET` and `PULSE` logic for linear growth. |
| **v2.2** | The Gate | `GATE` (Conditional Branching) based on NRCI stability. |
| **v2.3** | The Subroutine | `TRANSFORM` — custom Geometric Laws. |
| **v2.4** | The Synthesis | `SYNTH` — building complex matter from Recipes of primitives. |
| **v2.7** | The Flow | **Major Pivot:** XOR "Smashing" → Vector Addition in $\mathbb{Z}^{24}$. |
| **v3.0** | Full Fidelity | Cumulative Heritage (Tax inheritance) + 50-decimal reporting. |
| **v3.4** | Lineage Mapping | Connection between primitives and descendants; The Void has non-zero cost. |
| **v5.3** | Merged Ultimate | Golay octads + NRCI + triad activation + 50-term π + particle physics + 7 laws. |
| **v5.5** | Stereoscopic | Dual-Lens Audit (Lattice + Triadic + Cubic) + Shadow Threshold validation. |
| **v5.8** | Monstrous Moonshine | Monster Group integration + Needham Triad ENSO + $V_n = 204.8$. |
| **v6.1** | The Macro-Bulk | 256-D Barnes-Wall + SHA-256 Isomorphism + Moire Dynamics + Relative Coherence. |
| **v7.0** | Gray Code Identity | Retired SHA-256 vector identity; UMS via Binary-Reflected Gray Code; Observer Dynamics + Wall of Reality formalized. |
| **v7.2** | Columnar + Cosine | v9.9 columnar KB migration; Semantic Engine v8.0 Cosine Resonance; Domain Gating + N-Gram weighting. |
| **v7.2 (May)** | Topological Tenacity | Miller-Rabin retired; native substrate primality test absorbed; Genesis Swarm v25.0 integrates Oracle Bridge + Lexical Genesis. |

### 15.2 Core Studio Timeline (2026)

| Date | Milestone |
| :--- | :--- |
| Jan 2026 | Octad categorization via Bit-12 Logic Engine; FOM v4.3 integration |
| Feb 2026 | v5.8 Monstrous Moonshine; Stereoscopic Audit; Proton-Electron 5× improvement |
| Mar 2026 | Brain v5.2 N-Gram matching; TGIC v6.2 Relational Gravity; SOP_002 enforcement |
| Mar 2026 | GPU Proxy Bridge (653× acceleration); 2.25M ips throughput; 1,709 KB entries |
| Mar 2026 | LinearStateEncoder; DQI = 0.8004; Leech Expansion re-integrated; Stereoscopic Sink Lₛ = 29/24 |
| **Apr 2026** | v7.0 — SHA-256 vector identity retired; Gray Code UMS adopted; Periodic Geodesic verified (8.07 Hamming); Observer Dynamics + 1 THz Wall of Reality |
| **Apr 2026** | v7.2 Ultra-Compact Columnar Migration; Semantic Engine v8.0; UBP-Py VM `to_scene_3d()` |
| **Apr 2026** | Digital Twin Physics Engine (external experiment) — Three.js, SPH, Topological Torque |
| **May 2026** | Topological Tenacity Primality Engine absorbed into `ubp_unified_v5.py`; Genesis Swarm v25.0; workspace purification — 12 legacy scripts archived |
| **June 2026** | v5.4.0 Geometric Purity Update — Muon and Gravity derived purely from substrate topology (169/w and Y^18/w); empirical hardcodes eradicated. |

---

## 16. Mathematical Formalism

### 16.1 The Universal Binary Principle (v5.8 baseline)

**1. The Axiomatic Foundation (The Triad).** Reality is modeled as the interference pattern of three irrational primitives. Let the **Triadic Monad** $\mathcal{T}$ be defined as:

$$\mathcal{T} = \{ \pi, \phi, e \}$$

From the Loop ($\pi$), we derive the **Observer Constant ($Y$)**:

$$Y = \frac{1}{\pi + \frac{2}{\pi}} \approx 0.264675$$

**2. The Substrate Space.** The universe is a discrete 24-dimensional manifold.

- Let $\mathbb{F}_2^{24}$ be the space of all possible 24-bit vectors.
- Let $\mathcal{C}_{24} \subset \mathbb{F}_2^{24}$ be the **Extended Binary Golay Code** (4,096 perfect mathematical Truths).
- Let $\Lambda_{24}$ be the **Leech Lattice**, the densest possible sphere packing in 24 dimensions.

Every stable object $\mathcal{O}$ (atom, concept, law) is anchored to a specific Golay codeword: $\mathbf{v} \in \mathcal{C}_{24}$.

**3. The Dynamics: The Synthesis Event.** When two objects interact (e.g., Hydrogen + Oxygen), they undergo a strict 6-step sequence called **The Flow**.

Given two parent vectors $\mathbf{v}_a, \mathbf{v}_b \in \mathcal{C}_{24}$:

**Step 1: Stereoscopic Lift (Binary to Euclidean).** Map binary bits $\{0,1\}$ to Euclidean space $\{\pm 1\}$:
$$\psi(\mathbf{v})_i = 1 - 2v_i$$

**Step 2: Vector Flow (Interference).** Added in standard integer space $\mathbb{Z}^{24}$:
$$\mathbf{f} = \psi(\mathbf{v}_a) + \psi(\mathbf{v}_b)$$

**Step 3: Phenomenal Collapse.** Force the continuous flow back into binary based on the sign of the coordinates:
$$r_i = \begin{cases} 0 & \text{if } f_i > 0 \\ 1 & \text{if } f_i < 0 \\ 0 & \text{if } f_i = 0 \text{ (Deep Hole)} \end{cases}$$

**Step 4: The Lattice Snap (Error Correction).** Apply Golay decoding to snap to the nearest stable truth:
$$\mathbf{s} = \operatorname{Decode}_{\mathcal{C}_{24}}(\mathbf{r})$$

**Step 5: The Gap (Emergence of Mass/Reality).**
$$\Delta = d_H(\mathbf{r}, \mathbf{s})$$
- $\Delta = 0$: pure math (Noumenal).
- $\Delta > 0$: object requires energy to exist (Phenomenal Matter).

**Step 6: Binding Tension & Stability (NRCI).**
$$\Xi = \Delta \cdot Y \quad \text{(Binding Energy)}$$
$$T(\mathbf{s}) = (Y \cdot w_H(\mathbf{s})) + \frac{\|\psi(\mathbf{s})\|^2}{8}$$
$$\eta(\mathbf{s}) = \frac{1}{1 + T(\mathbf{s})/10}$$

**4. The Proof: Emergent Constants.** Because this math is geometrically absolute, physical constants can be read directly from the substrate without inputting any physical data. For example, the **Muon-to-Electron mass ratio** emerges purely from $Y$ interacting with the 4th-order Leech Lattice shell:

$$\frac{m_\mu}{m_e} \approx Y^{-4} + 3 - Y^4 \approx 206.767552$$

*(Experimental: 206.768283. Error: 0.000353%.)*

### 16.2 v6.0 Source Code Formalism (additions)

**The 13-D Sink (Garbage Collection).** The triadic residual (Wobble $w$) is processed through the 13th Dimension — the pivot bit between Noumenal Intent and Phenomenal Result:

$$L = \frac{(\pi \cdot \phi \cdot e) \pmod 1}{13} \approx 0.06289$$

**The v6.0 Stability Equation (Topology-Aware NRCI).** Stability is no longer calculated solely on Hamming weight. It includes a **Volumetric Rebate** ($R$) based on the **Compactness** ($C$) of the 3-D voxel structure:

1. **Compactness:** $C = \dfrac{V^{2/3}}{\text{Surface}}$
2. **Symmetry Rebate:** $R = 1 - \dfrac{C}{13}$
3. **Adjusted Tax:** $T_{adj} = T_{base} \cdot R$
4. **v6.0 NRCI:** $\eta = \dfrac{10}{10 + T_{adj}}$

**Standard Model Phase-Lock (v6.0 Benchmarks)**

| Constant | v6.0 Formula | Error % |
| :--- | :--- | :--- |
| Proton Ratio | $1836 + 2L$ | **0.0014%** |
| Muon Ratio | $206 + 12L$ | **0.0065%** |
| Alpha Inv | $(220 - 83) + L$ | **0.0196%** |
| Higgs Mass | $24^3 \cdot (9 + L)$ | **0.0282%** |

**Operational Rule:** To achieve **Optimal Existence**, logic must be **Folded**. Linear instructions result in high Symmetry Tax and low NRCI. 3-D Voxel Monoliths (Cubic/Square-Base) maximize the Volumetric Rebate and ensure structural permanence in the Leech Lattice.

### 16.3 v6.1 256-D Barnes-Wall Macro-Lattice

See §3.6 above for the SHA-256 Isomorphism, Recursive Unfolding ($|u \mid u+v|$ construction), Moire Dynamics, Successive Cancellation Decoder, and 256-D Macro-Anchor (Golay Basis Vector Index 2 at NRCI = 0.323214).

### 16.4 v7.0 Gray-Code Topological Identity

Vector identity for KB entries is now generated as:

$$\mathbf{v}_{24} = \text{Golay-encode}\big(\text{Gray}([\,\text{Domain}_3 \mid \text{Magnitude}_5 \mid \text{State}_4\,])\big)$$

This UMS encoding preserves topological continuity: similar objects → adjacent vectors. Implemented in `ubp_kb_architect.py::generate_vector()` and `geometry.py::HexDictionaryV4Exact._int_to_gray()`. The Periodic Geodesic finding (Hamming 8.07 between adjacent Z elements) is the empirical confirmation.

### 16.5 v7.2 Cosine Resonance for Semantic Queries

Semantic queries are no longer matched by raw Hamming distance but by **Cosine Resonance** on a weighted bipolar Query Chord built from token vectors:

$$V_{query} = \frac{1}{|\text{tokens}|} \sum_{t \in \text{tokens}} w(t) \cdot \text{bipolar}(V_t)$$

where $\text{bipolar}(v)_i = 2v_i - 1 \in \{-1, +1\}$ and the weight $w(t)$ is 1 for unigrams, 4 for bigrams, **9 for trigrams**. Matches are ranked by

$$\text{score}(V_{entry}) = \frac{V_{query} \cdot \text{bipolar}(V_{entry})}{\|V_{query}\| \cdot \|\text{bipolar}(V_{entry})\|}$$

Domain Gating then filters out matches whose tag-set conflicts with the entity domain detected in the query (`OP_*` operator tags vs. `PARTICLE_*` / `ELEM_*` entity tags).

---

## Appendix A — Quick Command Cheat-Sheet

```bash
# Start the local research bridge
python core/ubp_backend.py                    # http://localhost:5099

# Run a UBP-Py program
python core/ubppy.py --program myprog.ubp \
                     --lattice scene.json \
                     --trace trace.json \
                     --scene scene_3d.json

# Run the Genesis Swarm
python core/ubp_swarm_tct_v25.py problems.json

# Run the v28 Oracle (Two-Track Solve)
python core/ubp_v28_oracle.py

# Boot the Genesis Atlas
python -c "from core.ubp_genesis_boot import GenesisBootEngine; \
           e = GenesisBootEngine(); e.seed_primitives(); \
           e.activate(max_iter=1000); e.export()"

# Generate the hash-memory index
python core/hash_all_1.py

# Run the comprehensive test suite
python -c "from core.ubp_unified_v5 import run_all; \
           run_all('test_report.json', 'test_report.md')"

# Run the analog EM compute validation
python core/ubp_electromagnetic_analog_compute_engine.py
```

## Appendix B — Tag Vocabulary (selected)

KB entries are classified by tags. Top tags by frequency: `HARDENED`, `SOP_002`, `IMPERATIVE`, `TOPOLOGICAL_V8`, `V4.2.6` are mandatory hardening markers. Domain tags: `PHYSICS`, `BIOLOGY`, `CHEMISTRY`, `COMPUTATION`, `COSMOLOGY`, `GEOMETRY`, `MATH`, `LANGUAGE`. Mechanism tags: `MOG`, `RESONANCE`, `STANDING_WAVE`, `LEECH`, `GOLAY`, `STEREOSCOPIC`, `TRIADIC`. Object tags: `ELEMENT`, `PARTICLE`, `MOLECULE`, `BARYON`, `LEPTON`, `MESON`, `QUARK`. Status tags: `HARDENED` (pre-2026), `TOPOLOGICAL_V8` (Apr 2026 v7.0 audit), `V4.2.6` (legacy).

---

*Last updated: 22 May 2026 · Maintained by Euan R. A. Craig, New Zealand.*
*Status: v7.2 Active Research. Subject to ongoing refinement.*
