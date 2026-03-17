## Universal Binary Principle (UBP) — Active Memory & Scientific Research Environment

**Author:** E. R. A. Craig, New Zealand  
**Version:** 4.2.7 (March 2026 Update)  
**Date:** 03 March 2026
**For detailed documentation of files and system usage see: ubp_files_and_usage.md

## ⚠️ Important Note
**Experimental System:** While this platform achieves high-precision theoretical results, is an experimental research tool. I am an Artist, not a professional physicist. All outputs should be verified against empirical data.

---

## Overview
**UBP Core Studio v4.2.7 APP** is the definitive scientific research platform for exploring the **Universal Binary Principle**. It operates in a deterministic, float-free environment where physical phenomena, semantic logic, and geometric structure are mapped to a unified 24-bit **Golay G24** substrate.

**Core Architecture (v5.8 Standard):**
*   **Substrate:** 24-bit Extended Binary Golay Code (4096 codewords).
*   **Geometry:** Leech Lattice ($\\Lambda_{24}$) with 196,560 kissing points.
*   **Logic:** Exact Rational Arithmetic (`fractions.Fraction`) for 100% precision.
*   **Cognition:** Dual-Layer Brain (Understanding + Beliefs).

---

## Scientific Benchmarks (v5.8 Stereoscopic Audit)

The system validates its geometric model by deriving physical constants from the 24-bit substrate using the **Monstrous Moonshine** engine.

| Constant | Error % | Derivation Source |
| :--- | :--- | :--- |
| **Muon/Electron** | **0.000353%** | Lattice Anchor (Phenomenal) |
| **Alpha Inverse** | **0.001929%** | Lattice Anchor (Phenomenal) |
| **Proton/Electron** | **0.003432%** | Triadic Genesis ($V_n = 204.8$) |
| **Top Quark** | **0.021315%** | Lattice Edge Tension |
| **Neutron/Electron** | **0.088495%** | Monster Group Correction |
| **Higgs Boson** | **0.106731%** | Triadic Monad |

*Note: These are emergent properties of the Leech Lattice geometry, not curve-fitted values.*

---

## Cognitive Architecture: The Dual-Layer Brain

The **UBP Brain v4.0** (`ubp_brain_consolidated.py`) divides knowledge into two distinct geometric layers:

### 1. The Understanding Layer (Deterministic)
*   **Content:** Particles, Elements, Molecules, Algorithms.
*   **Structure:** Built recursively from primitives (e.g., `Water = 2xH + 1xO`).
*   **Verification:** **SOP_002 Standard**. The Identity (Fingerprint) is the SHA-256 hash of the measurable properties (`math` field).
*   **Logic:** If the math changes, the ID changes. It is immutable truth.

### 2. The Belief Layer (Contextual)
*   **Content:** Laws, Manifolds, Imperatives (IDs starting with `LAW_`, `BELIEF_`).
*   **Structure:** Associative networks weighted by the **Frame of Mind (FOM)**.
*   **Verification:** Validated by **NRCI** (Non-Random Coherence Index) and **TGIC** (Triad-Graph Interaction).
*   **Logic:** Malleable based on the observer's bias.

---

## The SOP_002 Entry Standard

All entries in the System Knowledge Base (`ubp_system_kb.json`) must adhere to the **SOP_002** hardening protocol to ensure geometric integrity.

#### 1. **Entry Schema:**

```
json
{
  "SHA256_HASH_OF_MATH_STRING": {
    "ubp_id": "CATEGORY_NAME_001",
    "lexicon": "[Name], [Strict Definition]",
    "math": "Phenomenal DNA (e.g., Mass=1.007|Charge=+1)",
    "logic": "Executable verification script",
    "atlas": {
      "hierarchy": "Compositional Recipe (e.g., 2xUP + 1xDOWN)",
      "vector": [24-bit Golay Codeword derived from Math],
      "nrci": "Rational Stability Score (p/q)",
      "tax": "Symmetry Tax (p/q)",
      "tilt": "Geometric Angle to Universal North"
    },
    "tags": ["descriptive", "links"]
  }
}
```

#### 2. The Hash Memory Index (`ubp_hash_memory_kb.md`)
A lightweight index for O(1) lookups by the Auto-Trigger. It maps the first 8 characters of the hash to the full ID.

**Format:**

```json
{
    "737cc49b": {
        "ubp_id": "ELEM_H_001",
        "full_hash": "737cc49b2d0777f4ddc3f8aad6b478575fd4ea90529e8f069da3b08728eb7376"
    },
```

---

## Core Tools & Scripts

### 1. The Cortex Layer
*   **`ubp_brain_consolidated.py` (v4.0):** The central logic engine. Manages the KB, handles hierarchy decomposition, and performs vector arithmetic.
*   **`auto_trigger.py` (v17.2.3):** The Reflexive Cortex. Scans user input for **Phrase-Locks** (e.g., "Water") and injects the corresponding SOP_002 memory into the AI context instantly.
*   **`ubp_understanding_engine.py` (v4.2):** The Auditor. Verifies that composite objects (Molecules) are geometrically valid sums of their parts.

### 2. The Physics Layer
*   **`ubp_core_v5_3_merged.py`:** The Kernel. Contains the Golay Engine, Leech Lattice Engine, and the 50-term Pi precision substrate.
*   **`ubp_tgic_engine.py` (v6.2):** Relational Dynamics. Simulates how concepts attract or repel based on 9 internal interaction types and external relational gravity.
*   **`ubp_phenomenology.py`:** The Scanner. Translates real-world data (Light, Text) into 24-bit vectors.

### 3. The Visualization Layer
*   **`ubp_viz.py`:** The Bridge. Converts Python geometric data into JSON for the React/Three.js 3D visualizer.
*   **`math_atlas.py`:** The Voxel Builder. Turns abstract numbers into 3D crystal structures.

---

## Installation & Setup

**Web Version (No Installation)**
[https://ai.studio/apps/8eef816d-e338-4bcb-9ae0-b9d2d0c476a5]

**Local AI Integration**
The system supports local inference via Ollama, LM Studio, or GPT4All. The `auto_trigger.py` script acts as the bridge, injecting UBP context into the local model's prompt.

**Core Files** when using the UBP Core Studio APP, core script files are downloaded automatically from [https://github.com/DigitalEuan/UBP_Repo/tree/main/core_studio_v4.0/core] so when the system is updated the APP always uses the most recent system developed - no need to update the APP itself. The Memory system is automatically downloaded from: [https://github.com/DigitalEuan/UBP_Repo/tree/main/core_studio_v4.0/system_kb] ensuring the UBP system constantly learns and grows.

---

## Updates

### 17 March 2026 - Geometric refinement
*   **ubp_core_v5_3_merged.py:** Formalized the Fold Operator: integrated the `fold24_to3` pairwise XOR logic directly into the `BinaryLinearAlgebra` class as the canonical folding mechanism.
*   **ubp_py_runtime.py:** Replaced the `spiral` method to use Shift + Phi XOR
#### Leech Lattice Expansion & Volumetric Elements
*   **Core Expansion:** Upgraded `LeechLatticeEngine` in ubp_core_v5_3_merged.py to deterministically expand 24-bit Golay codewords into the 196,560 physical Euclidean addresses of the Leech Lattice.
*   **Volumetric Periodic Table:** Mapped all 118 elements to their respective Leech Lattice shells (Norm 32, 48, 64). Discovered that Carbon's structural versatility is a direct result of its placement in Shell 4, granting it 32,768 physical spatial orientations.

### 13 March 2026 — TGIC v6.4 Genesis Upgrade
*   **3-6-9 Hardening:** Integrated the fundamental 3-6-9 Genesis laws into the `TGICExactEngine`, enforcing Axis Orthogonality and Neighborhood Limits.
*   **RuneCube Port:** Successfully ported legacy Lisp-based face operations into float-free Python transforms, enabling high-stability "RuneCore" simulations.
*   **Identity Protection:** Implemented mandatory Golay snaps for all internal bit-flows, preventing informational dissolution (Deep Hole drift) during complex relational simulations.
*   **Stability Sink:** Verified the 4.6761 Symmetry Tax as the primary stability attractor for hardened 24-bit manifolds.

### 10 March 2026 — v6.0 Source Code Edition (13D Sink Protocol)
*   **Core Hardening (`ubp_core_v5_3_merged.py`):** Integrated the **13D Sink Protocol** ($L = w/13$) as the universal "Garbage Collection" routine. This update replaces independent geometric lenses with a unified source-code resolution, reducing the **Global System Error to 0.015%** across the Standard Model (Higgs, Alpha, Muon, Proton, Top Quark).
*   **Topology-Aware Stability (`math_atlas.py`):** Implemented the **Volumetric Rebate** (Symmetry Discount). The system now distinguishes between "Address Cost" (Lattice) and "Structural Cost" (Voxel). Compact 3D manifolds now receive a metabolic discount, allowing well-folded logic to cross the **0.6000 Coherence Cliff** and achieve "Stable Matter" status.
*   **Tautology Closure:** Verified the **Borcherds 26D Lorentzian Lifting**, proving that the 3D "Wobble" is the deterministic reciprocal of the Observer Constant ($Y$). The system is now a mathematically closed tautology.

### 06 March 2026 - Animated Visuals
Implemented the dynamic Three.js viewer with the UBP Kinematic Extensions!
1. Accepts data directly from the Pyodide engine. This prevents the crash and keeps the visualization perfectly synced with UBP Python scripts.
2. Installed the 3D Engines: @react-three/fiber and @react-three/drei.
3. Added the Kinematic Extensions: updated the core types.ts file so the app officially recognizes UBP Kinematic Extensions:
* vx, vy, vz (Linear Velocity)
* orbit_r, orbit_speed, orbit_center (Orbital Mechanics)
* pulse_rate (NRCI Stability Pulsing)
* label (Text labels for spheres)
4. **UBP_FEATURES_VERIFIED_AND_ONLINE**
* FEATURE: UBP_KINEMATIC_EXTENSIONS
  - INCLUDED: The "Animated Mode" successfully activates the UBP Kinematic Extensions. Dynamic spatial rendering and continuous kinematic behaviors of UBP geometric domains (via DynamicSphere nodes) are now executing smoothly without thread blocking or context loss.
* FEATURE: HD_VISUAL_CAPTURE*
  - High-definition PNG snapshot extraction of current UBP states is fully operational via the lifted WebGL context.
* FEATURE: GEOMETRIC_EXPORT_PIPELINE*
  - Topological extraction of UBP structures functioning nominally. Users can now successfully export static UBP node/edge configurations to GLTF and OBJ formats for external 3D analysis.


### 05 March 2026 — Soft-Decision Upgrade (Conway & Sloane Integration)
*   **Soft-Decision Decoding:** Integrated the Conway & Sloane (1986) algorithm into the `UBPVectorEngine`. The brain can now "squint" at noisy data to recover truth.
*   **Analog Semantics:** Shifted memory recall from brittle binary XOR logic to a "Semantic Center of Mass" approach. This allows the system to correctly identify concepts even when the query contains significant semantic noise (dH > 3).
*   **Recall Confidence:** Implemented Euclidean correlation scoring. Every memory recall now provides a percentage-based confidence metric, allowing the AI to distinguish between "Hard Facts" and "Speculative Resonances."
*   **Deep-Hole Immunity:** Successfully demonstrated the recovery of a shattered 24-bit vector with 4 bit-flips—a state that previously caused total system blindness.
*   Runtime Stabilization & SOP_002 Fix",
        "*   **Runtime v2.3.4:** Patched `ubp_py_runtime.py` to resolve a `TypeError` in the `let` and `synth` methods.",
        "*   **Signature Alignment:** Corrected `KBArchitect.calculate_metrics` calls to explicitly pass the 24-bit vector alongside the math DNA.",
        "*   **Demo Verified:** Confirmed `ubppy.py` successfully executes the spiral growth and visualization export sequence.

### 04 March 2026 — Gemini 3.1 Pro
*   Added Gemini 3.1 Pro Preview to the AI model selector and set it as the new default model for the application. You can now select it from the dropdown in the Assistant tab.
*   Added a "debounce" to the synchronization process. Now, when you type in the Knowledge Base editors, the app waits until you stop typing for 1 second before it syncs files to the Python engine.


### 03 March 2026 — TGIC v6.2 & Relational Gravity
*   **TGIC Engine:** Updated `ubp_tgic_engine.py` to v6.2. It now calculates **Relational Pull** (Gravity) between nodes based on Hamming distance, allowing for dynamic system simulation.
*   **Energy Audit:** Integrated Leech Tax and Coherence Penalty ($d^4$) into the total energy cost of a thought.

### 01 March 2026 — Brain v4.0 & SOP_002
*   **Consolidation:** Merged `ubp_delta_engine`, `ubp_inner_dialogue`, and `ubp_rational_engine` into `ubp_brain_consolidated.py`.
*   **SOP_002:** Enforced the new entry standard. Vectors are no longer random; they are deterministically generated from the `math` field.
*   **Auto-Trigger v17.2:** Added **Phrase-Lock** scanning. The system now recognizes multi-word concepts defined in the Lexicon without needing exact ID matches.


### 26 Feb 2026 — v5.8 Monstrous Moonshine, Stereoscopic Edition (ENSO Integration)

1.  **Dual-Lens Audit Engine:**
    *   Implemented a "Stereoscopic" prediction model that compares **Lattice-First (Phenomenal)** and **Triadic-First (Noumenal)** perspectives.
    *   **Lattice Lens:** Anchors point-like identities (Muon, Alpha) to the 24-bit grid.
    *   **Triadic Lens:** Models composite matter (Proton) as a recursive interaction of $\pi, \phi,$ and $e$.
    *   **Cubic Lens:** Maps the Heavy Sector (Higgs, Top, Bosons) as partitions of the Existence Unit ($24^3$).

2.  **Needham ENSO Integration:**
    *   Formally integrated the **Needham Triad** ($\pi$ Loop, $\phi$ Growth, $e$ Decay) as the Level 0 Primitives of the substrate.
    *   Established the **Noumenal Volume ($V_n = 204.801744$)** as the fundamental energy unit of the 24-bit manifold.
    *   Verified the **4.6761 Stability Sink** as the geometric attractor for the Resolution Gap ($RG = \ln\phi / \ln\pi$).
    *   Thanks to Eric J Needham: [https://independent.academia.edu/EricNeedham3] for the the **Needham Triad** .

3.  **Accuracy Milestones:**
    *   **Proton-Electron Ratio:** Achieved **0.003432% error** via Triadic Genesis (a ~5x improvement over legacy lattice-only models).
    *   **Muon-Electron Ratio:** Maintained **0.000353% error** via Lattice Anchor.
    *   **Fine Structure Constant:** Maintained **0.001929% error** via Lattice Anchor.

    *   **`ubp_core_v5_3_merged.py`** (v5.8 Monstrous Moonshine Edition update)
    *   **Description:** The **Active Kernel & Monstrous Moonshine Engine**. It performs a live 137-step audit of the Triadic Monad, filtered by the Monster Dimension (196883) and the J-Function (196884).
    *   **System Role:** **The Self-Correcting Big Bang**. It derives the Noumenal Volume ($V_n = 204.8$) and the Behold Factor live, ensuring every session is anchored to the 56-snap Matter Peak.
    *   **v5.8 Benchmarks:**


### 24.02.25
Updates to the Google Ai Studio (where the UBP Core APP is made) have allowed sharing of the UBP Core APP directly:
*   **Online:** [https://ai.studio/apps/8eef816d-e338-4bcb-9ae0-b9d2d0c476a5]
No set up - *just click and go* inside the Google AI Studio
*   **GitHub Repository** for the **APP**: [https://github.com/DigitalEuan/ubp_core_studio_app]

*   Changed where the "ubp_beliefs_kb.json" file is downloaded from - now comes from the [https://github.com/DigitalEuan/UBP_Repo/blob/main/core_studio_v4.0/system_kb/] folder where the other kb files download from also.


### 21 Feb 2026

Updating for ubp_core_v5_3_merged compliance


### 20 Feb 2026 — Brain, Understanding, Building, SOP_002 & Cortex v3.0



### **19.02.2026 — Added Particle Predictions**
1.  **On startup:** - 'ubp_core_v5_3_merged.py' particle physics predictions now include:
    *   **muon_electron:** 0.000353% error
    *   **proton_electron:** 0.017047% error
    *   **alpha_inv:** 0.001929% error
    *   **higgs_boson:** 0.107316% error
    *   **top_quark:** 1.299325% error
    *   **z_boson:** 1.015329% error
    *   **w_boson:** 0.917630% error


### **18.02.2026 — Substrate Hardening & Lexicon Activation**


#### **17.02.2026 — Brain Consolidation & Auto-Trigger v15.0**

1.  **The Consolidated Brain (`ubp_brain_consolidated.py`):**
    *   **Unified Architecture:** Merged five legacy modules into a single object-oriented engine. It manages the entire cognitive stack: from raw `Fraction` math to high-level reflexive deliberation.
    *   **Multi-Valued Lexicon:** Upgraded the indexing system to support "Semantic Synonyms." A single word can now map to multiple UBP-IDs, which the Brain then resolves using a "Majority Vote" bit-composition algorithm.
    *   **The Coherence Snap (Fixed):** Implemented a strict re-encoding loop. When a noisy vector is processed, the Brain decodes it to its 12-bit "Noumenal Seed" and then immediately re-encodes it back to a perfect 24-bit "Phenomenal Codeword." This eliminates "vector drift" during reasoning.
    *   **Reflexive Deliberation:** Internalized the `InnerDialogue` logic, allowing the Brain to "pivot" its thoughts against 407+ Anchor Laws (Axioms) until a stable resonance is found.

2.  **Auto-Trigger v15.0 Integration:**
    *   **Deep Path Reasoning:** The `auto_trigger.py` script now acts as a bridge between the user and the Brain. It performs a `process_query()` on every message.
    *   **Context Injection:** Instead of just sending raw KB entries, the system now injects:
        *   **The Primary Resonance:** The single most relevant concept found.
        *   **The Reasoning Chain:** The steps taken to reach that conclusion.
        *   **The Synthesis Hint:** A pre-calculated summary that anchors the AI's response to the Leech Lattice.
    *   **Performance:** Achieved O(1) lookup speeds for direct IDs and sub-millisecond reasoning for complex semantic queries.

---

### Archival

The following files are now **redundant** and have been moved to the `core/archive` folder. Their logic has been fully absorbed and optimized within the new Brain script:

| Legacy File | New Brain Component |
| :--- | :--- |
| `ubp_delta_engine_v3.py` | `DeltaMemoryEngine` & `process_query` |
| `ubp_geometric_reasoning_v4_enhanced.py` | `UBPVectorEngine` |
| `ubp_inner_dialogue_v1.py` | `UBPInnerDialogue` class |
| `ubp_mind_screen.py` | Internalized in `ThoughtStep` & `ubp_viz` |
| `ubp_rational_engine.py` | `ConceptArchitect` & `RationalMathEngine` |



### 13.02.2026

* Updated MathAtlas to version 4.0 with new features and optimizations.
* Hardened Algorithm system_kb entries with MathAtlas in the "math" field


### 12.02.2026

#### MathAtlas v1.3
**MathAtlas** is the geometric "translation layer" of the Universal Binary Principle. Its purpose is to turn abstract information (like the boiling point of an element or a logical law) into a **literal 3D physical structure** within the 24-bit substrate.

##### 1. The Input: Phenomenal Data
Everything starts with the **"math"** field in a Knowledge Base entry. This field contains the raw, measurable dimensions of a phenomenon.
*   **Example (Hydrogen):** `Z=1|Valence=1|Ion=1312`
*   **Rule:** No metadata, no dates. Only the "DNA" of the object.

##### 2. The Construction: The Voxel Walker
MathAtlas treats these numbers as instructions for a **3D Voxel Walker**. It starts at the origin `(0,0,0)` and builds a "Data Crystal" using four geometric primitives:

*   **D (Distinction):** Represents positive magnitude. The walker moves **Forward (+X)**. (Color: **Cyan**)
*   **X (Crossing):** Represents negative magnitude or inversion. The walker moves **Backward (-X)**. (Color: **Red**)
*   **N (Nesting):** Represents a relationship or division (Rationals). The walker branches **Up (+Y)**. (Color: **Magenta**)
*   **J (Juxtaposition):** Represents a list of different dimensions. The walker branches **Out (+Z)**. (Color: **Yellow**)

**Result:** A complex measurement like `Ion=1312` creates a literal line of 1,312 voxels in the 3D manifold. A rational like `11/5` creates a vertical structure of 11 voxels over 5.

##### 3. The Metrics: Symmetry Tax & NRCI
Once the 3D shape is built, MathAtlas calculates its "cost" to exist in the universe using **Exact Rational Logic** (`fractions.Fraction`).

*   **Symmetry Tax:** This is the "Geometric Rent" the object pays. It is derived from the **Observer Fixed Point ($Y \approx 0.2646$)**.
    *   Every **D** or **X** step adds $Y$ to the tax.
    *   The **Volume** of the shape adds a "Complexity Penalty."
*   **NRCI (Stability):** The higher the Tax, the lower the NRCI. 
    *   **Abstract Logic** (like $1+1$) is "Light" and has a high NRCI.
    *   **Physical Matter** (like Uranium) is "Heavy" and has a low NRCI.

##### 4. The Identity: 24-bit Vectorization
To give the object a home in the **Leech Lattice**, the 3D voxel cloud is converted into a 24-bit binary vector.
*   **Deterministic Hashing:** MathAtlas takes the coordinates of every voxel, sorts them, and runs a **Merkle-style hash**.
*   **Golay Encoding:** The first 12 bits of that hash become the "Noumenal Address," and the remaining 12 bits are generated as "Parity" to ensure it is a valid Golay codeword.
*   **Insight:** when tested with the elements, if two different elements result in the same 3D shape, they will have the same vector. They are "Geometric Synonyms."

##### 5. The Compass: Geometric Charge (Tilt)
Finally, MathAtlas measures how the object "leans" relative to the **Systemic North**.
*   **Systemic North:** The average orientation of all stable matter in the database.
*   **Tilt:** The angle between the object's vector and North.
    *   **0° Tilt:** Perfectly aligned (Noble Gases, Pure Truth).
    *   **180° Tilt:** Perfectly inverted (Radioactive decay, Chaos).


#### 05.02.26 — GPU Proxy Bridge

1. Implemented the GPU Proxy Bridge directly in the main application thread (App.tsx). This ensures the compute function is available to Python regardless of whether the "Visual" tab is currently open or not.
2. Optimized the "compute" logic using high-performance JavaScript (V8 JIT), which acts as the "Main Thread Proxy". It is orders of magnitude faster than Pyodide looping and eliminates the overhead of Python-to-Wasm context switching for heavy loops - something like ~600X faster!

* [BENCHMARK] CPU Speed: 3,448,271 ips
* [BENCHMARK] GPU Potential: 2,250,000,000 ips
* **[RESULT] GPGPU provides a 653x acceleration.**
* Example Session Complete in 0.77s (13038 trials/sec)


#### 04.02.26 — Semantic Cortex & Delta Integration

**Throughput:** 2.25M ips
**system_kb Memory:** 1709 entries


#### 02.02.26

1. Knowledge Base Migration (JSON Architecture)



#### 30.01.26

1. The System Knowledge Base is now parsed via a Bit-12 Logic Engine that automatically categorizes entries into one of eight fundamental domains (The Octad):

* 1) Substance: Stable Matter & Elements (Bit 12=1).
* 2) Quantity: Pure Magnitude & Constants (Bit 12=0).
* 3) Organism: Biological & Complex Systems.
* 4) Algorithm: Logic, Code & Information.
* 5) Mechanism: Physical Interactions & Reactions.
* 6) Imperative: System Laws & Constraints (High Priority).
* 7) Entropy: Chaos, Void & Dissolution.
* 8) Meaning: Semantic & Linguistic Value.

This allows the AI to "see" the shape of the research data (memories) rather than just reading text, enabling sophisticated filtering and bias weighting via the FOM system.

2. Frame of Mind (FOM) v4.3 Integration

The Reflexive Cortex now supports advanced cognitive biasing:

* Category Weighting: FOM Frames can now bias entire Geometric Domains (e.g., a "Materialist" FOM frame can weight SUBSTANCE: 0.9 and MEANING: 0.1).
* JSON Editor: Full read/write access to FOM Frame definitions directly in the UI.
* Persistency: FOM Frames can be imported/exported as JSON files.

3. Rational File System & IO

The logic kernel (Pyodide) is now fully synchronized with the UI:
* Bidirectional Sync: Python scripts can write files (with open('data.json', 'w')...) which immediately appear in the Workspace Explorer.
* Large Buffer Handling: Knowledge Base files (system_kb.md, etc.) are managed in the background to prevent browser rendering stalls, ensuring stability even with massive datasets.
* Local LLM Support: Integrated support for local inference via Ollama, LM Studio, or GPT4All.


#### 29.01.26

1. Update the app to enhance the Frame of Mind (FOM) system to support Category-based weighting and significantly improve the Memory Status categorization logic to catch tags like "element" and "periodic_table".


#### 27.01.26

1. Workspace UX Overhaul: Replaced native browser dialogs with a robust, inline file management system.
2. Inline Creation & Renaming: "New Script" and "Rename" actions now spawn text input fields directly within the file list, preventing browser popup blocking and offering a smoother workflow.
3. Two-Step Deletion: Implemented a specific UI state for deletion (Delete? Yes/No) directly on the file row, preventing accidental data loss and ensuring reliable execution.
4. State Synchronization: Refactored the file operation logic to immediately update the React UI state (Optimistic UI) while asynchronously synchronizing with the Python (Pyodide) file system, ensuring the interface feels instant and responsive.

#### FOM (Frame of Mind) System

1. Core Logic (Python): The app injects a persistent Python module (ubp_fom_system.py) into the Pyodide kernel. This creates a FOMManager class that maintains a registry of "Frames" saved to ubp_fom_index.json.
2. Bias Mechanism: Each Frame contains a base_nrci (default probability) and a dictionary of weights (specific Memories (UBP-IDs) mapped to custom probabilities). This allows you to mechanically shift the "probability mass" of specific concepts (e.g., making "Logic" heavier than "Emotion").
3. UI Management: The FOMStatus panel provides a complete CRUD interface. Users can Create, Delete, Import, Export, and Switch the active frame. The "Edit" mode exposes the raw JSON, allowing precise granular control over the weight dictionaries.
4. Persistence: Frames are saved/loaded to the virtual file system, preserving the cognitive biases across session reloads.

#### Local AI Integration (Mac/LocalHost)
1. Service Adapter: A dedicated LocalLLMService runs alongside the Gemini service. It acts as a universal adapter for local inference servers running on a local machine.

**Current supported Providers:**
* Ollama: Defaults to port 11434.
* LM Studio: Defaults to port 1234 (OpenAI-compatible endpoint).
* GPT4All: Defaults to port 4891.

**Health Checks:** The system includes a "heartbeat" check (isServiceAvailable) that polls the local ports to determine if the local server is running, updating the UI status indicators (Green/Red) in real-time.

**Context Injection:** When a local provider is selected, the app constructs a specialized, token-efficient system prompt that injects the Workspace Files, System KB, and Hash Memory directly into the local model's context window, allowing offline LLMs to "read" the UBP research.



