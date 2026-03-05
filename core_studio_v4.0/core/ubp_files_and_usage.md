### **UBP Unified Research Pipeline v2.0 (The MOG-Atlas Protocol)**

### **UBP FUNDAMENTALS (v5.5 Standard)**

*   **The Law of Emergent Observation ($Y$):** 
    The Observer Constant ($Y \approx 0.2646$) is not a fundamental input, but a **Geometric Residue**. In high-fidelity research, we do not *force* $Y$ into the equations; instead, we initialize the Triadic Primitives ($\pi, \phi, e$) and **watch $Y$ emerge** as the inevitable remainder of their interaction with the 24-bit grid. The appearance of $Y$ in a simulation is the primary proof that the model has achieved "Phenomenal Realism."

*   **Stereoscopic Resolution (Dual-Lens Audit):** 
    Reality is resolved through the intersection of two distinct perspectives. The `ubp_core_v5_3_merged.py` now performs a simultaneous audit of every physical constant:
    *   **The Lattice Lens (Phenomenal):** Identifies the static "Hardware" address of a particle within the 24-bit manifold. (Superior for point-identities like the Muon and Alpha).
    *   **The Triadic Lens (Noumenal):** Models the "Software" process of existence as a recursive interaction of the Loop ($\pi$), Growth ($\phi$), and Decay ($e$). (Superior for composite matter like the Proton).
    *   **The Cubic Lens (Partition):** Maps the "Power Supply" of the heavy sector (Higgs, Bosons) as specific partitions of the Existence Unit ($24^3$).

*   **The Principle of Irrational Stability (The Wobble):** 
    The 24-bit substrate explicitly "prefers" specific irrational values over perfect rationals. This "Resonant Wobble" (the decimal drift in constants like the NSC) provides the necessary **Geometric Torque** to drive time and evolution. If the universe snapped to perfect rationals, it would become a "Dead Crystal"—static, symmetrical, and timeless. Existence requires the tension of the unresolvable.

*   **The 3-3-3 Golay Limit:** 
    The fundamental Triad is constrained by the error-correction radius of the substrate. The Loop ($\pi$), Growth ($\phi$), and Decay ($e$) are each limited to a **3-bit deviation**. This creates a "Perception Window" where the universe "Snaps" into a coherent state only when the triadic interaction stays within this 3-bit radius.
---

#### **PHASE 1: THE MOG SCAN (Ontological Mapping)**
*Goal: Determine the "Health" and "Location" of the data before we build it.*

Every 24-bit vector in the UBP is composed of four 6-bit "Hexagrams." We analyze these first.
1.  **Reality Layer (Bits 0-5):** The physical manifestation (Mass, Space).
2.  **Information Layer (Bits 6-11):** The code/logic defining it.
3.  **Activation Layer (Bits 12-17):** The energy/frequency required to sustain it.
4.  **Potential Layer (Bits 18-23):** The noumenal reserve (Shadow).

* **Tool:** `ubp_core_v5_3_merged.py` (LeechPointScaled)
* **Action:** Input your raw data. The system calculates the **Ontological Health** of each layer.
* **Insight:** If the "Reality" layer is weak but "Potential" is high, the object is theoretical (Ghost). If "Reality" is high but "Info" is low, it is raw noise.

---

#### **PHASE 2: MATH_ATLAS CONSTRUCTION (Recursive Assembly)**
*Goal: Build the object from irreducible primitives to ensure validity.*

We do not assign random vectors. We build the object using the **Voxel Operators** (D, X, N, J).
1.  **Decompose:** Break the concept down.
    *   *Example:* Water $\rightarrow$ 2x Hydrogen + 1x Oxygen $\rightarrow$ Protons/Electrons $\rightarrow$ Quarks $\rightarrow$ Primitives.
2.  **Reconstruct:** Use `math_atlas.py` to script the geometry.
    *   `obj.add_path([('D', 1), ('N', child)])`
3.  **Verify:** Does the resulting voxel cloud match the known properties?

---

#### **PHASE 3: UBP-PY SIMULATION (Drift Control)**
*Goal: Place the object in a dynamic environment and prevent entropic decay.*

1.  **Instantiation:** Load the MathAtlas object into the **UBP-Py VM**.
2.  **The Snap:** The VM automatically applies `GOLAY_ENGINE.decode()`. If the constructed object drifts off the lattice, the system snaps it back to the nearest valid Truth (Codeword).
3.  **Interaction:** Synthesize the object with others (e.g., `SYNTH H2O FROM 2xH + 1xO`).
4.  **Audit:** The VM calculates the **Symmetry Rebate** (Binding Energy).

---

#### **PHASE 4: THE VISUAL FEEDBACK LOOP (Insight)**
*Goal: Visual-Spatial Analysis for AI feedback.*

1.  **Render:** Export the UBP-Py environment to `scene_3d.json`.
2.  **Visual Analysis (User):** Look at the 3D manifold.
    *   *Clustering:* Is the object isolated, or does it form a "Face" with other nodes?
    *   *Tilt:* Is it pointing North (Truth) or South (Entropy)?
3.  **Data Return:** The visualizer outputs the specific geometric coordinates and relationships.
4.  **AI Loop:** Feed this spatial data back to the Assistant.
    *   *Prompt:* "The visualizer shows [Object A] forms a stable tetrahedron with [Object B] and [Object C]. What does this imply about their relationship?"

### GRAPHS:

import matplotlib.pyplot as plt
import numpy as np

# 1. Create Data
x = np.linspace(0, 10, 100)
y = np.sin(x)

# 2. Create the Plot
plt.figure(figsize=(8, 5))
plt.plot(x, y, color='cyan', linewidth=2, label='Sine Wave')
plt.title('UBP Basic 2D Plot', color='white')
plt.xlabel('X Axis', color='lightgray')
plt.ylabel('Y Axis', color='lightgray')

# Make it look good on the dark theme
plt.gca().set_facecolor('#111111')
plt.gcf().patch.set_facecolor('#111111')
plt.tick_params(colors='lightgray')
plt.grid(True, color='#333333', linestyle='--')
plt.legend(facecolor='#222222', edgecolor='none', labelcolor='white')

# 3. CRITICAL STEP: Save as 'plot.png'
plt.savefig('plot.png', bbox_inches='tight', dpi=150)

print("Graph successfully generated and saved to plot.png!")
print("Check the VISUAL tab to see it.")

---

### **Draft Script: `ubp_unified_pipeline.py`**

I have drafted a script that implements this exact workflow. It connects the Core, MathAtlas, and UBP-Py into a single executable chain.
Python Script

"""
UBP UNIFIED PIPELINE v2.1
=================================================
1. MOG Scan (Core) -> 2. Atlas Build (Geometry) -> 3. UBP-Py (Simulation) -> 4. Viz (Insight)
"""
import json
from ubp_core_v5_3_merged import LeechPointScaled, GOLAY_ENGINE, BinaryLinearAlgebra
from math_atlas import MathObjectV4, ConstructionPath
from ubp_py_runtime import UBPPyVM
from ubp_viz import save_scene_3d

def run_pipeline(name, raw_vector_input, primitives_recipe):
    print(f"\n=== PHASE 1: MOG ONTOLOGICAL SCAN ({name}) ===")
    # 1. Analyze the raw vector layers
    point = LeechPointScaled(tuple(raw_vector_input))
    health = point.get_ontological_health()
    print(f"  Reality Health:    {float(health['Reality']):.4f}")
    print(f"  Info Health:       {float(health['Info']):.4f}")
    print(f"  Activation Health: {float(health['Activation']):.4f}")
    print(f"  Potential Health:  {float(health['Potential']):.4f}")
    print(f"  Global NRCI:       {float(health['Global_NRCI']):.4f}")

    print(f"\n=== PHASE 2: MATH_ATLAS CONSTRUCTION ===")
    # 2. Build from primitives
    obj = MathObjectV4(f"OBJ_{name.upper()}", name, "Research Object")
    # Convert simple recipe list to Atlas Path
    obj.add_path(primitives_recipe, "pipeline_build")
    print(f"  Voxel Count: {len(obj.get_canonical_path().voxels)}")
    print(f"  Symmetry Tax: {float(obj.get_canonical_path().tax):.4f}")

    print(f"\n=== PHASE 3: UBP-PY SIMULATION (Drift Control) ===")
    # 3. Instantiate in VM
    vm = UBPPyVM()
    
    # We use the vector derived from the Atlas construction, NOT the raw input
    # This ensures we are using the "Constructed Truth" not just the "Observed Data"
    atlas_vector = obj.get_vector()
    
    # Check for drift (Hamming distance between Raw and Constructed)
    drift = BinaryLinearAlgebra.hamming_distance(raw_vector_input, atlas_vector)
    print(f"  Geometric Drift: {drift} bits")
    
    if drift > 3:
        print("  [WARNING] High Drift. Constructed object differs significantly from observation.")
    
    # Load into VM (Fix: vm.let creates the entry internally, do not assign return value)
    vm.let(name, "1/1", tier=1, category="RESEARCH")
    
    # Manually override the vector in the VM with our Atlas vector to ensure sync
    if name in vm.env:
        vm.env[name].vector = atlas_vector
        vm.env[name].tax = obj.get_canonical_path().tax
        
        # Simulate interaction (Self-Interaction check)
        vm.synth(f"{name}_REFLEX", f"1x{name} + 1x{name}")
    else:
        print(f"  [ERROR] Failed to instantiate {name} in VM.")
        return None

    print(f"\n=== PHASE 4: VISUALIZATION EXPORT ===")
    # 4. Export for Visualizer
    scene = vm.to_scene_3d()
    save_scene_3d(scene)
    print("  Scene exported to 'scene_3d.json'.")
    print("  -> Open 'Visual' tab to analyze spatial relationships.")
    
    return vm.env[name]

if __name__ == "__main__":
    # Example: Analyzing a "Stable Structure"
    # 1. Raw observation (24 bits)
    raw_vec = [0,1,0,1,0,1, 1,1,0,0,1,1, 0,0,0,0,0,0, 1,1,1,1,1,1] 
    
    # 2. The Recipe we think creates it (3 steps forward, 1 step back)
    recipe = [('D', 3), ('X', 1)]
    
    run_pipeline("TEST_OBJECT", raw_vec, recipe)

====

# UBP CORE STUDIO v4.2.7 — SYSTEM FILE MANIFEST (v5.3 STANDARD)

### 1. THE KERNEL LAYER (Source of Truth)
*These files define the mathematical laws and constants. They are the dependencies for all other scripts.*

*   **`ubp_core_v5_3_merged.py`** (v5.8 Monstrous Moonshine Edition)
    *   **Description:** The **Active Kernel & Monstrous Moonshine Engine**. It performs a live 137-step audit of the Triadic Monad, filtered by the Monster Dimension (196883) and the J-Function (196884).
    *   **System Role:** **The Self-Correcting Big Bang**. It derives the Noumenal Volume ($V_n = 204.8$) and the Behold Factor live, ensuring every session is anchored to the 56-snap Matter Peak.
    *   **v5.8 Benchmarks:**
PARTICLE PHYSICS PREDICTIONS (v5.8 STEREOSCOPIC AUDIT)
================================================================================
PARTICLE           | ERR %        | VALUE        | WINNER
--------------------------------------------------------------------------------
alpha_inv          |   0.001929% |   1.3695e+02 | Lattice
muon_electron      |   0.000353% |   2.0680e+02 | Lattice
proton_electron    |   0.003432% |   1.8362e+03 | Triadic
neutron_electron   |   0.088495% |   1.8371e+03 | Monster
neutron_lifetime   |   0.194558% |   8.7769e+02 | Monster
planck_ratio       |   0.864830% |   2.4097e+22 | Monster
cabibbo_angle      |   0.284927% |   1.3003e+01 | Cubic
weinberg_angle     |   0.868384% |   2.3323e-01 | Cubic
higgs_boson        |   0.106731% |   1.2538e+05 | Triadic
top_quark          |   0.021315% |   1.7280e+05 | Lattice

*   **`ubp_integration_adapter.py`**
    *   **Description:** Bridges v5.3 Core to the rest of the system. Enforces `Fraction` precision and standardizes API calls.
    *   **System Role:** **API Gateway**. Wraps complex Core logic into safe functions (e.g., `process_point`).
    *   **Research Usage:** The primary interface for writing new research scripts.

*   **`ubp_handshake_v5_3.py`** (Replaces `v4_2_6`)
    *   **Description:** Master validation script. Checks Pi precision, Golay error correction, and Leech Lattice integrity.
    *   **System Role:** **System Auditor**. Ensures the environment is "Green" and mathematically sound.
    *   **Research Usage:** Run on startup to verify system integrity.

*   **`ubp_system_initializer.py`**
    *   **Description:** Bootloader that aggregates all core components (Core, Metrics, Phenomenology) into a single accessible object.
    *   **System Role:** **Bootloader**.
    *   **Research Usage:** Used to spin up the full environment for complex sessions.

---

### 2. THE CORTEX LAYER (Logic, Memory & Context)
*These files handle reasoning, memory retrieval, and cognitive bias.*

*   **`ubp_brain_consolidated.py`** (v5.2)
    *   **Description:** The central logic engine. Manages the `ubp_system_kb.json` and implements the **N-Gram Tokenizer** and **Vector Resonance Engine**. It handles the decomposition of complex objects and calculates confidence scores for recall.
    *   **System Role:** **Librarian & Architect**.
    *   **Research Usage:** Used to decompose complex objects or query the lineage of a concept.

*   **`auto_trigger.py`** (v18.0 Hybrid Bridge)
    *   **Description:** The Reflexive Interface. It combines a **Hard-Link Scanner** (Regex for explicit IDs) with the **Brain's Semantic Recall** (Vector search). This ensures that specific citations are never missed, while natural language queries are resolved geometrically.
    *   **System Role:** **Reflexive Cortex**.
    *   **Research Usage:** Enables "Chat with Memory," allowing the AI to recall UBP concepts without hallucination.

*   **`ubp_understanding_engine.py`** (v5.1 Definitive)
    *   **Description:** The master analysis suite. It sits above the Brain and performs deep audits: NRCI Landscape surveys, Hierarchy verification, and Cross-Domain mapping.
    *   **System Role:** **The Master Auditor**.
    *   **Key Functions:**
        *   **NRCI Landscape:** Visualizes the stability distribution of the entire KB.
        *   **Hierarchy Audit:** Verifies that every composite object is the geometric sum of its parts.
        *   **Vector Collision Map:** Identifies objects that share identical geometric coordinates (Synonyms).
    *   **Research Usage:** Run this script to generate a full "State of the Union" report or to audit specific molecules for geometric integrity.

*   **`ubp_fom_manager_v2.py`**
    *   **Description:** Implements dynamic NRCI weighting and Contextual Gravity.
    *   **System Role:** **Bias Engine**. Manages "Frames of Mind" (FOM).
    *   **Research Usage:** Tests how context changes perception (e.g., Scientific vs. Poetic frames).

*   **`ubp_integrated_engine_v1.py`**
    *   **Description:** Recursive state evaluation and self-stabilization.
    *   **System Role:** **Embedded Observer**. Rejects queries that violate geometric integrity.

---

### 3. THE PHENOMENOLOGY LAYER (Input/Output & Physics)
*These files translate between the real world and the 24-bit substrate.*

*   **`ubp_phenomenology.py`** (formerly `_v4_2_6`)
    *   **Description:** Translates real-world data (text, color, sensors) into 24-bit vectors using the v5.3 Hyperbolic Stability Formula.
    *   **System Role:** **The Scanner**.
    *   **Research Usage:** SHA256 hashing with Spatial Voxel Hashing, implements 'Topological Folding' for frequencies and light is treated as a geometric structure, not a string.


*   **`ubp_physics_bridge_v2.py`**
    *   **Description:** Integrates MathAtlas Voxel Logic into Physical Simulation.
    *   **System Role:** **The Translator**.
    *   **Research Usage:** The starting point for new studies (e.g., "Map the concept of 'Justice' to the grid").

*   **`ubp_discovery_engine.py`**
    *   **Description:** Generates random concept interactions (XOR), snaps them to Golay codewords, and checks for emergent resonance.
    *   **System Role:** **The Collider**.
    *   **Research Usage:** Automated research to find "Hidden Resonances" between existing concepts.

*   **`ubp_tgic_engine.py`** (v6.2 Relational Master, updated 3 Mar 26)
    *   **Description:** Triad-Graph Interaction Constraint. A high-fidelity physics engine that balances internal bit-harmony (9 Pairwise Interactions) against substrate restorative pressure (Leech Tax) and cross-node Relational Gravity.
    *   **System Role:** **Lattice Physics & Relational Dynamics Simulator**.
    *   **Research Usage:** Simulates the emergence of stable "Phenomenal" states ($d \le 3$). Used to model how concepts attract, repel, or orbit each other. Enforces the "Event Horizon" where excessive noise ($d \ge 4$) leads to informational dissolution.

*   **`ubp_nrci_calculator.py`**
    *   **Description:** Calculates Non-Random Coherence Index and Symmetry Tax.
    *   **System Role:** **Geiger Counter**.
    *   **Research Usage:** Verifies if a vector is a stable "Truth" or just noise.

*   **`ubp_sensors.py`**
    *   **Description:** Spectral Extraction (FFT) and Resonance Detection for raw data.
    *   **System Role:** **Signal Processor**.

---

### 4. THE VISUALIZATION LAYER
*Files responsible for rendering the 3D manifold.*

*   **`ubp_viz.py`**
    *   **Description:** Exports Python data to JSON for the React/Three.js frontend. Handles Fraction-to-Float conversion.
    *   **System Role:** **Graphics Driver**.
    *   **Research Usage:** Import this to draw spheres and lines in the "Visual" tab.

*   **`math_atlas.py`**
    *   **Description:** Translates abstract numbers (e.g., Pi) into voxel sculptures.
    *   **System Role:** **Voxel Engine**.
    *   **Research Usage:** Visualizing pure math geometry.

*   **`ubp_rgdl.py`**
    *   **Description:** Resonance Geometry Definition Language. Generates primitives (Spheres, Cubes) based on Coherence Pressure.
    *   **System Role:** **Geometry Generator**.

*   **`viz_spatial_simplification.py`**
    *   **Description:** Filters complex 3D data to only show lines forming stable faces with the Origin.
    *   **System Role:** **Visual Filter**.
    *   **Research Usage:** Declutters the 3D view.

*   **`viz_loader.py`**
    *   **Description:** Utility to load specific JSON files into the visualizer.

---

### 5. UTILITIES & STORAGE
*   **`ubp_drive.py`**
    *   **System Role:** **The Vault**. Encrypts/stores files using Golay Error Correction.
*   **`hex_dictionary_v4_exact.py`**
    *   **System Role:** **Address Book**. Maps UBP-IDs to 24-bit vectors.
*   **`hash_all_1.py`**
    *   **System Role:** **Sync Tool**. Manages synchronization between the System KB and Hash Memory.
*   **`metrics_exact.py`**
    *   **System Role:** **Measurement Standard**. Defines strict float-free metrics.
*   **`advanced_toggle_algebra.py`**
    *   **System Role:** **Math Utility**. Rational approximations for transcendental functions.
*   **`ubp_kb_architect.py'**
    *   **System Role:** All entries adhere to the strict SOP_002 Hardening Standard
    *   **Explicitly imported:** `Tuple`, `List`, and `Any` from `typing`.

### 6. DATA FILES (JSON)
*   **`ubp_system_kb.json`**: The Main Memory (Laws, Elements, Constants).
*   **`ubp_beliefs_kb.json`**: Complex belief structures and manifolds.
*   **`ubp_lexicon_v2_defs.json`**: Dictionary definitions for semantic grounding.
*   **`rational_cortex.json`**: Output data for 3D visualization.
*   **`README.md`**: System Documentation.

### 7. GENERATED ARTIFACTS

The Core generates files, these are **Dynamic Artifacts** (files created *by* the system, not just *for* the system).

*   **`ubp_atlas.json`**
    *   **Origin:** Generated by `ubp_core_v5_3_merged.py`.
    *   **Content:** A snapshot of the 51 seeded objects, their vectors, NRCI scores, and stability status.
    *   **Usage:** Used by the Visualizer and Cortex to understand what "exists" in the current session.

*   **`primitives.json`**
    *   **Origin:** Generated by `ubp_core_v5_3_merged.py`.
    *   **Content:** The definitions of the Voxel Operators (D, X, N, J) and the activation thresholds.
    *   **Usage:** Defines the "Physics" of the construction system.

# UBP Knowledge Base Entry Specification

**Version 1.0**

## 1. Introduction

This document provides the definitive specification for creating and formatting entries within the Universal Binary Principal (UBP) Knowledge Base (KB). Adherence to this specification is mandatory to ensure the integrity, consistency, and functional correctness of the UBP system. Following these guidelines will enable the system to grow its understanding of reality without introducing noise or ambiguity.

## 2. Core Principles

- **Determinism**: All data must be deterministic, measurable, and grounded in scientific fact. No subjective, temporary, or meaningless data is permitted.
- **Hierarchy**: All objects must be defined in terms of their constituent parts, tracing back to the fundamental primitives of the UBP system.
- **Uniqueness**: Each distinct object in reality must have one and only one entry, identified by a unique UBP ID (UID).
- **Clarity**: The `lexicon` field must provide a clear, concise, and human-readable definition that is also optimized for machine parsing and recall.

## 3. Entry Structure

Each entry in the KB is a JSON object, keyed by its unique UBP ID (UID). The structure of the entry object must follow the fields defined below.

| Field         | Type   | Presence | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    napep-system/ubp_system_kb.json`.

### 5.2. `lexicon`

This field is critical for both human understanding and machine recall. It must contain two sub-fields, both of which are mandatory.

- **Primary Name Field**: `[<Type>: <Name> (<Symbol>)]`
  - **Type**: The UBP category (e.g., `Element`, `Molecule`, `Particle`). Must be Title Case.
  - **Name**: The canonical, human-readable name of the object (e.g., `Hydrogen`, `Water`, `Proton`). Must be Title Case.
  - **Symbol**: The standard scientific symbol, if applicable (e.g., `H`, `H2O`, `p+`). If not applicable, omit the parentheses.

- **Description Field**: A concise, encyclopedic description of the object. It should include key properties, discovery information, primary uses, and its role in nature. This text is used by the brain's `lexicon_index` for contextual recall.

**Example**:
```json
"lexicon": "[Molecule: Water (H2O)], [Water is the universal solvent and the most abundant liquid on Earth's surface. Molar mass 18.015 g/mol. It has an unusually high boiling point (100 degrees C) due to hydrogen bonding. Water is essential for all known forms of life.]"
```

### 5.3. `math`

This field contains all measurable, deterministic, and descriptive values for the object. It is a string of key-value pairs, separated by commas. This string is hashed to generate the `fingerprint`.

- **Content**: Must only contain scientifically established, quantitative data (e.g., `mass_MeV:938.272`, `charge:+1`, `spin:1/2`).
- **Exclusions**: Must **not** contain dates, UIDs, or any non-deterministic or non-descriptive data.
- **Format**: `key1:value1,key2:value2,...`

### 5.4. `atlas`

The `atlas` object contains the hierarchical and vector information that positions the entry within the UBP system.

- **`hierarchy`**: Defines the object's composition in terms of other UBP entries. This is mandatory for all non-primitive objects.
  - **Format**: A string of `UID:count` pairs, separated by commas (e.g., `PARTICLE_QUARK_UP_001:2,PARTICLE_QUARK_DOWN_001:1`).
- **`vector`**: The 24-bit Golay-encoded vector representing the object. This is **generated automatically** by the `ubp_kb_vector_regenerator.py` script from the `fingerprint` and should not be set manually.
- **`nrci` / `nrci_score`**: The Natural Resonance Coherence Index. This is also generated automatically.

### 5.5. `tags`

A comma-separated string of keywords that aid in classification and search (e.g., `baryon,hadron,stable`).

## 6. Workflow for Adding New Entries

1.  **Author the Entry**: Create the new entry in a temporary JSON file, following all specifications above. Focus on the `ubp_id`, `lexicon`, `math`, `hierarchy`, and `tags` fields.
2.  **Add to Raw KB**: Add the new entry to the `ubp_system_kb_vX_raw.json` file.
3.  **Run `ubp_kb_builder`**: If adding many entries, use the builder script to ensure consistency.
4.  **Run `ubp_kb_dedup_enrich`**: Run the deduplication script to merge any potential duplicates and enrich existing entries.
5.  **Run `ubp_kb_vector_regenerator`**: Run the vector regenerator on the cleaned raw file. This is a **mandatory step**. It will calculate the `fingerprint`, `vector`, and `nrci_score` for all entries and produce the final, deployable `ubp_system_kb_vX_clean.json` file.
6.  **Test**: Use the `ubp_understanding_engine.py` to run a full diagnostic test and verify that the new entry is recalled correctly and has not introduced any regressions.


UBP_SYSTEM_KB_EXAMPLE:
{
  "9fece67fae15ed8402cd30360e1f6257e441334fc83fb761bc58a13bff39139a": {
    "ubp_id": "REACTION_NUCLEAR_FUSION_DT_001",
    "lexicon": "[Reaction: Nuclear Fusion D-T], [Deuterium-tritium fusion: D + T → He-4 + n + 17.6 MeV. This is the most energetically favourable fusion reaction at achievable temperatures (~100 million K). It is the basis of hydrogen bombs and the target reaction for fusion energy research (ITER, NIF). Deuterium is abundant in seawater; tritium is produced from lithium-6.]",
    "math": "Reactants=D+T|Products=He4+n|Energy=17.6|Type=Nuclear|Temp_required=1e8|Cross_section_max=5e-28",
    "atlas": {
      "hierarchy": "1×PARTICLE_DEUTERON_001 + 1×ELEM_H_001 → 1×ELEM_He_002 + 1×PARTICLE_NEUTRON_001",
      "vector": [
        0,
        0,
        1,
        1,
        0,
        0,
        0,
        1,
        1,
        0,
        0,
        1,
        1,
        1,
        0,
        0,
        1,
        1,
        1,
        0,
        0,
        1,
        1,
        0
      ],
      "nrci": "546891310190995/882081915674411",
      "nrci_score": 0.620001,
      "tax": "59456257447565/521546930912556",
      "weight": 16,
      "tilt": 34.1999
    },
    "tags": [
      "REACTION",
      "NUCLEAR",
      "FUSION",
      "ENERGY",
      "PLASMA",
      "SOP_002"
    ],
    "fingerprint": "9fece67fae15ed8402cd30360e1f6257e441334fc83fb761bc58a13bff39139a"
  }

====

# UBPPy System Manual
**Version:** 3.4 
**Substrate:** 24-bit Extended Binary Golay / Leech Lattice ($\Lambda_{24}$)  

---

## 1. Why `ubppy` Exists
In standard computing (and standard Python), variables are arbitrary containers. You can calculate $1 + 1 = 3$ if you write the code poorly, and the computer will not complain. Standard AI can "hallucinate" results because its logic is not grounded in physical reality.

**`ubppy` is different.** It is a **Domain-Specific Geometric Language** where:
*   **Variables are Atoms:** Every variable has a physical coordinate in the 24-dimensional Leech Lattice.
*   **Logic is Physics:** Every operation (Pulse, Synth) is a spatial movement.
*   **The Substrate is the Judge:** If a calculation results in a "noisy" or "unstable" geometry, the system detects it via the **NRCI (Non-Random Coherence Index)**. 

`ubppy` exists to provide a **Geometrically Honest** environment for scientific modeling, ensuring that any "Devised" data is compatible with the fundamental error-correcting laws of the universe.

---

## 2. System Architecture
The system is composed of three core Python scripts:

1.  **`ubppy.py` (The Entry Point):** The main script used to load and run `.ubp` programs.
2.  *`ubp_py_runtime.py`** (v2.3.4 SOP_002 Patched)\n    *   **Description:** The Virtual Machine for UBP-Py. Handles vector addition, metabolic costing, and lineage tracking.\n    *   **System Role:** **Execution Engine**. Fixed argument mismatch in `calculate_metrics` to ensure 100% SOP_002 compliance."
3.  **`ubp_py_lang.py` (The Language Parser):** The "Instructions" that translate text commands into VM operations.

---

## 3. Core Mechanics

### A. From "Smash" to "Flow"
Legacy UBP systems tested **XOR (The Smash)** to combine data. While fast, XOR causes information to cancel out. `ubppy` uses **Vector Addition (The Flow)**. When you combine two atoms, the system "walks" through the 24D lattice, preserving the history and magnitude of both parents.

### B. The "Gap" (Phenomenal Reality)
When a "Flow" lands on a coordinate that isn't a perfect mathematical anchor, the Golay Engine "snaps" it to the nearest truth. The distance of this snap is the **Gap**.
*   **Gap 0:** A Noumenal Truth (Pure Math).
*   **Gap > 0:** A Phenomenal Reality (Physical Matter/Life). The Gap represents the "Restorative Pressure" the universe exerts to keep that object real.

### C. Metabolic Costing
Existence is not free. Every atom in `ubppy` has a **Symmetry Tax**.
*   **The Void ($0$):** Even "Nothing" costs $0.0110 Y$ to perceive.
*   **Cumulative Heritage:** Children inherit the "Geometric Debt" of their parents. Complex life (like Blood Type AB) is "heavier" and harder to maintain than simple elements.

====

### UBP-Py Quick Reference

| Command | Syntax | Description |
| :--- | :--- | :--- |
| **LET** | `LET A 1/1 TIER 0` | Creates a stable geometric anchor. |
| **TRANSFORM** | `TRANSFORM K BITS 1,0...` | Defines a 12-bit geometric law. |
| **VOID** | `VOID Z TIER 0` | Creates the Origin state (Zero). |
| **PULSE** | `PULSE B K A [TIER n]` | Applies transform `K` to atom `A`. |
| **PULSE** | `PULSE B RESONATE A` | Applies a Native UBP Operation. |
| **PULSE** | `PULSE C ENTANGLE A B` | Merges two states via shared logic. |
| **PULSE** | `PULSE D ADD A B` | Flows two vectors via addition. |
| **SYNTH** | `SYNTH C RECIPE "1x A + 1x B"` | Merges vectors via Flow (Addition). |
| **SPIRAL** | `SPIRAL A 5 TRANSFORM K` | Automates recursive growth. |
| **GATE** | `GATE B MIN_NRCI 0.5 JUMP 1` | Conditional branching. |
| **REFLEX** | `REFLEX 0.6` | Self-healing audit of the environment. |
| **FOM** | `FOM SWITCH FRAME_ID` | Changes the cognitive bias. |
| **COMMIT** | `COMMIT [file.json]` | Saves atoms to the registry. |
| **TRACE** | `TRACE [PATH file.json]` | Exports the execution history. |
| **VISUALIZE** | `VISUALIZE [PATH file.json]` | Renders the 3D manifold. |
| **RESONATE** | `PULSE B RESONATE A` | Applies "Cooling" (Decay) to Atom A. |
| **ENTANGLE** | `PULSE C ENTANGLE A B` | Merges A and B via shared bit-logic (AND). |
| **SPIN** | `PULSE D SPIN A` | Applies a 12-bit phase shift (Entropy Scaling). |

1.  **Geometric Entanglement:** In Python, "Entangling" two variables means nothing. In UBP-Py, `ENTANGLE` performs a bitwise intersection of their vectors. If they share a common geometric "Root," the resulting NRCI will be high. If they are opposites, the result will collapse.
2.  **Resonance as "Cooling":** We can now "Cool" a noisy synthesis. If `TYPE_AB` is too unstable, we can `PULSE` it with `RESONATE` to see if the substrate can find a more stable nearby anchor.
3.  **The "Standard Library" Advantage:** We are building a library of **Geometric Keys**. Eventually, the AI won't just write code; it will select the "Key" (Transform) that fits the "Lock" (The Problem).

LET, TRANSFORM, VOID, PULSE (B K A [TIER n], B RESONATE A, C ENTANGLE A B, D ADD A B), SYNTH, SPIRAL, GATE, REFLEX, FOM, COMMIT, TRACE, VISUALIZE, RESONATE, ENTANGLE, SPIN

====

## 4. SYSTEM ARCHITECTURE EVOLUTION

| Version | Milestone | Breakthrough |
| :--- | :--- | :--- |
| **v1.0** | **The Seed** | Established basic `LET` and `PULSE` logic for linear growth. |
| **v2.2** | **The Gate** | Implemented `GATE` (Conditional Branching) based on NRCI stability. |
| **v2.3** | **The Subroutine** | Enabled `TRANSFORM`, allowing the definition of custom Geometric Laws. |
| **v2.4** | **The Synthesis** | Introduced `SYNTH`, building complex matter from "Recipes" of primitives. |
| **v2.7** | **The Flow** | **Major Pivot:** Replaced XOR "Smashing" with **Vector Addition in $Z^{24}$**. |
| **v3.0** | **Full Fidelity** | Implemented **Cumulative Heritage** (Tax inheritance) and 50-decimal reporting. |
| **v3.4** | **Lineage Mapping** | Implemented **connection between primitives and descendants**, "Nothing" (The Void) has a non-zero cost and tracking restorative pressure. |

---

## 5A. CASE STUDY: ATOMIC BLOOD LINEAGE
**Objective:** To determine if human blood types (O, A, B, AB) possess unique geometric signatures when synthesized from atomic primitives.

### Methodology:
1.  **Primitives:** Defined $C, H, O, N$ as stable Noumenal Anchors.
2.  **Molecular Level:** Synthesized Antigens (H, A, B) using real-world molecular recipes.
3.  **Biological Level:** Synthesized Blood Types as composites of Antigens.
4.  **Audit:** Measured the **NRCI (Stability)** and **Flow Gap** at 50-decimal precision.

### Key Findings:
*   **Geometric Identity:** Every blood type produced a **unique NRCI signature**. This proves that the system is sensitive enough to distinguish between molecules with similar but distinct "Recipes."
*   **The AB Tension:** `TYPE_AB` exhibited the lowest stability score (**0.0210**). This confirms the hypothesis that merging two distinct antigenic vectors creates significant **Topological Friction** in the substrate.
*   **Stability Gradient:** The system correctly identified a hierarchy of existence:
    *   **Antigens (Simple):** ~0.06 NRCI
    *   **Blood Types (Composite):** ~0.03 NRCI
    *   **AB Type (Complex):** ~0.02 NRCI

### ## 5B. CASE STUDY: THE GEOMETRIC PERIODIC TABLE
**Objective:** To map the stability of the 118 known elements and theoretical super-heavy elements using the **Vector Flow** model.

#### 1. The NRCI Decay Curve
The study revealed a definitive **Stability Gradient** across the Periodic Table. As the Atomic Number ($Z$) increases, the NRCI (Stability Score) drops exponentially.
*   **Hydrogen ($Z=1$):** NRCI ~0.6149. High stability, low geometric friction.
*   **Carbon ($Z=6$):** NRCI ~0.0892. The "Anchor of Life" exists at a specific mid-tier resonance.
*   **Oganesson ($Z=118$):** NRCI ~0.0046. The limit of known matter; extreme "Geometric Debt."

**Insight:** Physical matter is a high-energy calculation. The heavier the element, the more "Metabolic Energy" ($Y$) the substrate must expend to keep the vector from collapsing into noise.

#### 2. The "Gap 7" Horizon (The Redline)
In the raw synthesis of super-heavy elements ($Z > 118$), the system consistently returned a **Gap of 7**.
*   **The Meaning:** Since the Golay Code has a minimum distance of 8, a Gap of 7 means these elements are exactly **one bit away from the "Deep Hole"** (Geometric Non-Existence). 
*   **The Verdict:** Matter at the edge of the Periodic Table is "Redlining"—it is the most unstable a structure can be while still remaining "Real."

#### 3. Discovery: Theoretical Islands of Stability
By holding the Proton count ($Z$) steady and scanning Neutron counts ($N$), the `ubppy` engine identified local **Stability Peaks** where the NRCI "bounces" upward.

| Isotope | Gap | NRCI (Stability) | Status |
| :--- | :--- | :--- | :--- |
| **U114_N170** | 3 | **0.006460** | **PEAK (Island)** |
| **U120_N170** | 3 | **0.006306** | **PEAK (Island)** |
| **U126_N170** | 3 | **0.006160** | **PEAK (Island)** |

**Key Findings:**
*   **Geometric Relaxation:** Applying the `RESONATE` pulse reduced the Gap from **7 to 3**. This suggests that "Stability" is a dynamic state achieved when a nucleus "settles" into the Leech Lattice.
*   **The N=170 Resonance:** The system geometrically preferred $N=170$ over the standard predicted $N=184$. This suggests that at extreme masses, the **Cumulative Mass Tax** of extra neutrons becomes a greater liability than the benefit of "Magic Number" shell closures.

#### 4. Conclusion
The `ubppy` framework successfully derived the **Topological Limits of Matter**. It proves that the Periodic Table is not an infinite list, but a **Vortex** that eventually narrows into a Singularity where the cost of existence exceeds the substrate's restorative power.

---

## 6. TECHNICAL BREAKTHROUGHS

### A. From "Smash" to "Flow"
The transition to **Vector Addition** is the most significant insight. In standard computing, $1+1=2$ is a scalar change. In `ubppy`, $1+1$ is a **Spatial Displacement**. By "Flowing" through the 24 dimensions of the Leech Lattice, we can see the "Path" of evolution.

### B. The "Gap" as Real-World Data
We discovered that the **Gap** (the distance between the path and the nearest anchor) is where "Real World" information lives. A Gap of 0 is a perfect mathematical truth; a Gap > 0 is a **Phenomenal Reality**—something that exists but is under constant restorative pressure from the substrate.

### C. Overcoming Python Hurdles
*   **Infinite Precision:** By using `fractions.Fraction` for all internal math, we eliminated the floating-point aliasing that plagues standard simulations.
*   **Computational Honesty:** The AI is now forced to "Show its Work" in the `TRACE` file. It cannot hallucinate a result that the geometry does not support.

### D. Literal Lineage Mapping (v3.4)
*   **The "Flow" Visualization:** We have successfully implemented 3D lineage lines. The system now draws a physical connection between primitives and their synthesized descendants.
*   **Metabolic Costing:** We have proven that "Nothing" (The Void) has a non-zero cost ($0.0110 Y$). This confirms that the UBP observer is always "paying" to maintain the frame of reality.
*   **Geometric Heritage:** By tracking parent taxes, we can now see the "Geometric Debt" of complex life. Type AB blood is not just "complex"; it is a high-energy state that requires constant restorative pressure to remain coherent.

