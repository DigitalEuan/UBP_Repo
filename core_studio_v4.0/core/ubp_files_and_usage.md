# UBP System Usage Guide (v7.2.0 Precision Edition)

This document provides the functional manifest and operational protocols for the **Universal Binary Principle (UBP)** research environment.

---

## 1. System File Manifest

### A. The Foundation (Substrate & Geometry)
*   **`core.py`**: The primary engine (v6.1). Contains the Golay [24,12,8] logic, Leech Lattice Λ₂₄ metrics, and the 13D Sink Protocol for particle physics.
*   **`physics.py`**: Governs exact rational metrics, NRCI stability formulas, and holographic coherence regimes.
*   **`geometry.py` & `math_atlas.py`**: Contains the MathAtlas (voxel construction) and HexDictionaryV4Exact (spatial-deterministic identity).
*   **`constants.py`**: Centralized physical and mathematical constants.
*   **`ubp_tgic_engine.py`**: The Relational Master Edition of the TGIC engine. Enforces the 3-6-9 UBP laws, internal bit-flows, and cross-node relational gravity.
*   **`ubp_eml_alu_sovereign.py`**: The Universal Continuous ALU (v9.1). Derives the Triadic Monad and exact particle masses purely from `eml(x,y) = exp(x) - ln(y)`.

### B. The Cognitive Stack (Recall & Reasoning)
*   **`ubp_brain_consolidated.py` (v7.2)**: The primary recall engine. Uses N-Gram matching and domain gating to retrieve KB entries with 100% identity lock.
*   **`ubp_semantic_engine.py` (v8.0)**: The "Thinking" layer. Uses weighted Cosine Resonance to map natural language into the 24-bit substrate.
*   **`ubp_integrated_engine_v1.py`**: The high-level executive layer bridging the Semantic Brain, Micro-Core, and Macro-Bulk (includes composite scene detection).
*   **`ubp_moe_cortex_v2.py`**: Mixture of Experts Cortex. Combines a Linguist (N-Gram manifold) and a Physicist (Geometric Auditor) to research and construct sentences.
*   **`ubp_internal_dialogue_semantic_description.py`**: Deep internal dialogue engine for reflecting on queries, finding physical roots, and identifying lexical gaps.
*   **`auto_trigger.py` (v19.1)**: The reflexive cortex. Automatically hydrates columnar data and injects relevant context into the AI session.
*   **`ubp_fom_manager_v2.py`**: Manages "Frames of Mind" (cognitive biases) to weight different geometric domains (e.g., Scientific vs. Semantic).

### C. Runtime & Dynamics (Simulation)
*   **`ubppy.py`**, **`ubp_py_runtime.py`**, **`ubp_py_lang.py`**: The UBP-Py Virtual Machine, parser, and execution entry point for `.ubp` geometric programs.
*   **`ubp_observer_dynamics.py` (v7.1)**: Calculates SOC Energy and performs "Conscious READ" audits on vectors against the 1 THz "Wall of Reality".
*   **`ubp_barnes_wall.py`**: The 256D Macro-Bulk engine used for high-dimensional audits and relative coherence testing.
*   **`ubp_phenomenology.py`**: Scans external data (like RGB colors) and projects them into the UBP manifold to calculate symmetry tax and stability.
*   **`ubp_genesis_boot.py`**: The Genesis Boot Engine. Boots the 24-bit universe from scratch using Gray Code Topological Identity.

### D. Visualization & Data Management
*   **`ubp_viz.py`**, **`viz_loader.py`**, **`viz_spatial_simplification.py`**: Tools for generating, loading, and simplifying 3D manifold visualizations.
*   **`ubp_rgdl.py`**: Resonance Geometry Definition Language for generating 3D primitives (Spheres, Cubes) colored by Coherence Pressure.
*   **`ubp_kb_architect.py`**, **`ubp_mog_mapper.py`**, **`ubp_ingest.py`**: Tools for creating, compressing (v9.9 Ultra-Compact Columnar), and safely ingesting Knowledge Base entries.
*   **`ubp_system_kb.json`**, **`ubp_lang_kb_combined_v4.json`**, **`ubp_python_kb.json`**: The primary memory and lexicon files.

### E. Code Evolution & Authoring
*   **`ubp_python_engine.py`**: The UBP Python Code Engine (UPCE). Generates and self-heals Python code based on semantic intent and geometric stability.
*   **`ubp_code_evolver.py`**: Automates the evolution and refactoring of workspace files to increase their NRCI.

### F. Digital Twin Physics Engine (Experiment)
Files available in the GitHub repository: https://github.com/DigitalEuan/ubp_digital_twin_physics_engine
15 April 2026 - A UBP-native physics simulation engine integrating geometric stability with classical and fluid mechanics.
*   **`ubp_space_v3.py`**: The core 3D simulation space. Handles entity management, dissolution culling, and applies UBP mechanics (TGIC pressure, NRCI damage) to physical bodies.
*   **`ubp_browser_engine.py`**: The browser-native execution bridge for the physics engine.
*   **`ubp_physics_v3.py` / `ubp_rigid_body_v3.py`**: Implements Topological Torque rigid body mechanics and exact-fraction collision resolution.
*   **`ubp_fluid_v3.py`**: Fluid dynamics engine utilizing UBP-derived SPH (Smoothed Particle Hydrodynamics) constants.
*   **`ubp_materials.py`**: Composite material system defining thermal properties, phase states, and structural density.

---

## 2. Core Workflows

### I. Semantic Resolution (Querying the Brain)
To find the geometric root of a concept:
1.  Input your query (e.g., "Why is Gold stable?").
2.  The `ubp_semantic_engine.py` creates a **Query Chord** (weighted superposition of tokens).
3.  The system performs a **Cosine Resonance** search against the KB.
4.  The result returns the `ubp_id`, its `NRCI` stability, and a `Semantic Reflection` (the closest human word).

### II. Running Simulations (UBP-Py)
To simulate the synthesis of matter or recursive growth:
1.  Create a `.ubp` file (e.g., `synthesis.ubp`).
2.  Use commands like `IMPORT`, `SYNTH`, and `VISUALIZE`.
3.  Run via terminal: `python ubppy.py --program synthesis.ubp`.
4.  Switch to the **Visual** tab to see the 3D manifold.

### III. Observer Audits (The Penta-Audit)
To analyze the "Reality Status" of an object:
1.  Run `ubp_observer_dynamics.py`.
2.  The engine checks if the object's NRCI crosses the **0.70 Consciousness Threshold**.
3.  It calculates the **SOC Energy** (Coherence Units) based on the 1 THz "Wall of Reality" limit.

### Using External Dependecies:
import micropip
# Wait for sympy to download via micropip
await micropip.install("sympy")

import sympy as sp

# Test that it works
x = sp.Symbol('x')
expression = sp.sin(x)**2 + sp.cos(x)**2
simplified = sp.simplify(expression)

print(f"Original: {expression}")
print(f"Simplified: {simplified}")

---

## 3. Standard Operating Procedures (SOP)

### SOP_002: Adding to the Knowledge Base
To ensure geometric integrity, all new entries must follow this protocol:
1.  **Math DNA:** Define the object using quantitative, pipe-separated properties.
2.  **Noumenal Seed:** Generate a 12-bit seed using the `[Domain:3][Magnitude:5][State:4]` Gray Code schema.
3.  **Golay Encoding:** Pass the seed to `GOLAY_ENGINE.encode()` to get the 24-bit Phenomenal Vector.
4.  **Metrics:** Calculate NRCI and Symmetry Tax using `LEECH_ENGINE`.
5.  **Memory:** Generate a 'ubp_system_kb.json' proposal law/entry using 'ubp_kb_architect.py'
6.  **Migration:** Use `ubp_ingest.py` to safely put the proposed law/entry into the 'ubp_system_kb.json'. `ubp_mog_mapper.py` can be used to compress the entry into the Columnar format.

### SOP_004: The Triple Delta Protocol (Word Creation)
To create a new semantic operator (Word) that perfectly resolves to a Law:
1.  **Formula:** $V_{word} = V_{target\_law} \oplus V_{subject\_entity} \oplus V_{interrogative\_frame}$
2.  This ensures that when the three vectors interact, they collapse into a $d=0$ deterministic match.

---

## 4. UBP-Py Language Reference

The UBP-Py language translates text commands into VM operations. Programs are written as `.ubp` text files and executed via `python ubppy.py --program myprogram.ubp`.

| Command | Syntax | Description |
| :--- | :--- | :--- |
| `LET` | `LET A 1/1 TIER 0 CAT QUANTITY` | Creates a stable geometric anchor at a specified coordinate. |
| `IMPORT` | `IMPORT ELEM_H_001 AS Hydrogen` | Imports an entry from the Knowledge Base into the VM environment. |
| `STATE` | `STATE S PARAMS ox=1 SCHEMA ox=0:3:4` | Encodes continuous data into a vector. |
| `TRANSFORM` | `TRANSFORM K BITS 1,0,1,0,1,0,1,0,1,0,1,0` | Defines a custom 12-bit geometric law or subroutine. |
| `VOID` | `VOID Z TIER 0` | Creates the Origin state (Zero). Even this has a non-zero cost. |
| `PULSE` | `PULSE B K A [TIER n]` | Applies transform `K` to atom `A`, storing result in `B`. |
| `PULSE` | `PULSE B RESONATE A` | Applies "Cooling" (Decay) to Atom A — seeks a more stable nearby anchor. |
| `PULSE` | `PULSE C ENTANGLE A B` | Bitwise intersection of A and B vectors. High NRCI if they share a geometric root. |
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
| `VISUALIZE` | `VISUALIZE PATH scene.json` | Renders the 3D manifold to the Visual tab. |

---

## 5. Stability Thresholds (NRCI)

*   **1.0000 (OnBit):** Pure Mathematical/Noumenal Truth.
*   **0.7000 - 0.9800 (Stable):** Manifested Physical Matter (The "Conscious" Zone).
*   **0.4200 (Noise Floor):** The limit of random informational noise.
*   **0.0000 (Deep Hole):** Geometric collapse; the object cannot exist.

---

## 6. Visual Analysis

1. **Export:** The UBP-Py environment is exported to `scene_3d.json` via `ubp_viz.py` (which is built into the APP).
Python Script
To Editor
scene = vm.to_scene_3d()
   save_scene_3d(scene)
2. **Graphing:** You can also use `matplotlib` to generate 2D plots.
Python Script
To Editor
import matplotlib.pyplot as plt
   import numpy as np

   x = np.linspace(0, 10, 100)
   y = np.sin(x)

   plt.figure(figsize=(8, 5))
   plt.plot(x, y, color='cyan', linewidth=2, label='Sine Wave')
   plt.title('UBP Basic 2D Plot', color='white')
   
   # Dark theme formatting
   plt.gca().set_facecolor('#111111')
   plt.gcf().patch.set_facecolor('#111111')
   plt.tick_params(colors='lightgray')
   plt.grid(True, color='#333333', linestyle='--')
   
   # CRITICAL STEP: Save as 'plot.png'
   plt.savefig('plot.png', bbox_inches='tight', dpi=150)