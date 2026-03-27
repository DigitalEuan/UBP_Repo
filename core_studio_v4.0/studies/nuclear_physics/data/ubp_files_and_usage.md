# UBP System Usage Guide (v6.0 Modular Edition)

This document provides the functional manifest and operational protocols for the **Universal Binary Principle (UBP)** research environment.

---

## 1. System File Manifest

### A. The Foundation (The "Source of Truth")
*   **`constants.py`**: Centralized physical and mathematical constants (Planck, Alpha, etc.).
*   **`core.py`**: The primary engine. Contains the Golay [24,12,8] logic, Leech Lattice Λ₂₄ metrics, and the 13D Sink Protocol for particle physics.
*   **`physics.py`**: Governs exact rational metrics, NRCI stability formulas, and coherence regimes.
*   **`geometry.py`**: Contains the MathAtlas (voxel construction) and HexDictionary (spatial-deterministic mapping).

### B. The Cognitive Stack (Reasoning & Memory)
*   **`ubp_brain_consolidated.py`**: The primary recall engine. Uses N-Gram matching and vector similarity to retrieve Knowledge Base entries.
*   **`auto_trigger.py`**: The reflexive cortex. Automatically injects relevant KB context into the AI chat based on your input.
*   **`ubp_integrated_engine_v1.py`**: The executive layer. Performs the **Penta-Audit** (Micro, Macro, and Visual analysis) on any query.
*   **`ubp_fom_system.py` / `ubp_fom_index.json`**: Manages "Frames of Mind" (cognitive biases) that weight different geometric domains.

### C. Runtime & Dynamics (Simulation)
*   **`ubppy.py`**: The entry point for running `.ubp` geometric programs.
*   **`ubp_py_runtime.py`**: The Virtual Machine that executes vector addition, synthesis, and lineage tracking.
*   **`ubp_tgic_engine.py`**: Governs the 3-6-9 Genesis logic and relational gravity between concepts.
*   **`ubp_barnes_wall.py`**: The 256D Macro-Bulk engine used for high-dimensional audits and relative coherence testing.

### D. Visualization & Data
*   **`ubp_viz.py`**: The bridge that exports `scene_3d.json` for the 3D Visual tab.
*   **`ubp_rgdl.py`**: The Resonance Geometry Definition Language for generating 3D primitives (Spheres, Cubes).
*   **`ubp_system_kb.json`**: The primary memory file containing all verified SOP_002 entries.
*   **`ubp_hash_memory_kb.json`**: Lightweight index for O(1) hash-based recall.
*   **`ubp_kb_architect.py`** automates the translation of raw scientific data into stable geometric codewords

---

## 2. Core Workflows

### I. Querying the Brain (The Penta-Audit)
To analyze a concept or compare multiple entities, run `ubp_integrated_engine_v1.py`.
1.  **Semantic Resolution:** Finds the closest match in the KB.
2.  **Micro-Stability:** Checks the 24D NRCI score.
3.  **Ontological Drift:** Determines if the object is Phenomenal (Matter) or Noumenal (Math).
4.  **Macro-Audit:** Tests the object's resilience in the 256D Barnes-Wall bulk.
5.  **Imagination Sandbox:** Generates a 3D visual tension map.

### II. Running Simulations (UBP-Py)
To simulate the synthesis of matter or recursive growth:
1.  Create a `.ubp` file (e.g., `test.ubp`).
2.  Use commands like `IMPORT`, `SYNTH`, and `SPIRAL`.
3.  Run via terminal: `python ubppy.py --program test.ubp`.
4.  Check the **Visual** tab to see the resulting manifold.

### III. Real-Time Scanning (Phenomenology)
To translate real-world data (like an RGB color or a sensor reading) into a 24-bit vector:
1.  Define the bit-generator in `ubp_phenomenology.py`.
2.  Run the script to see the resulting NRCI and Symmetry Tax.

---

## 3. Standard Operating Procedures (SOP)

### SOP_002: Adding to the Knowledge Base
To ensure geometric integrity, all new entries must follow this protocol:
1.  **Math DNA:** Define the object using only quantitative, measurable properties (pipes-separated).
2.  **Fingerprinting:** The entry key must be `SHA256(math_string)`.
3.  **Vectorization:** Generate the 24-bit vector by encoding the first 12 bits of the hash.
4.  **Indexing:** Run `hash_all_1.py` after adding entries to update the recall index.

A complete 'ubp_system_kb.json' example entry (Hydrogen):

```json
{
  "451abc64108603144c7b294a3862eab6fc35e945dab4b7785784ab44bc8c427f": {
    "ubp_id": "ELEM_H_001",
    "lexicon": "[Element: Hydrogen (H)], [Hydrogen (Z=1). A Gas (Phase 1) with Hexagonal potential. Valence 1. Tension: 4. It is the seed of the material octave, born from the Proton-Electron union.]",
    "math": "BP=507/25|Crystal=1|EN=11/5|Ion=1312|M=126/125|MP=1401/100|Oxidation=1|Phase_STP=1|Rad=53|Rho=2247/25000|Valence_e=1|Z=1",
    "atlas": {
      "hierarchy": "1×PARTICLE_PROTON_001 + 0×PARTICLE_NEUTRON_001 + 1×PARTICLE_ELECTRON_001",
      "vector": [
        0,
        0,
        1,
        0,
        0,
        1,
        1,
        1,
        0,
        0,
        1,
        0,
        1,
        0,
        1,
        0,
        1,
        0,
        1,
        1,
        1,
        1,
        0,
        0
      ],
      "nrci": "33620407785878960339240364076535309850806800741903055631302500/55608508046372509626759775532373494451963521314512091269063661",
      "nrci_score": 0.604591,
      "tax": "21988100260493549287519411455838184601156720572609035637761161/3362040778587896033924036407653530985080680074190305563130250",
      "weight": 8,
      "tilt": 86.6654
    },
    "tags": [
      "ELEMENT",
      "HARDENED",
      "HYDROGEN",
      "NONMETAL",
      "PERIOD_1",
      "SOP_002"
    ],
    "fingerprint": "451abc64108603144c7b294a3862eab6fc35e945dab4b7785784ab44bc8c427f"
  }
```

### Automatic Vector Generation Pipeline

The `ubp_kb_architect.py` script automates the translation of raw scientific data into stable geometric codewords through the following pipeline:

1. **Input:** The `math` field (Phenomenal DNA) of a Knowledge Base entry.
2. **Fingerprinting:** SHA-256 hash of the `math` string generates the unique identity key.
3. **Noumenal Seeding:** The first 12 bits of the hash serve as the "Noumenal Seed" — the core informational intent of the object.
4. **Golay Encoding:** The 12-bit seed is passed to `GOLAY_ENGINE.encode()`, which generates 12 parity bits, resulting in a perfect 24-bit Phenomenal Codeword.
5. **Geometric Anchoring:** The 24-bit vector serves as the object's hardware address within $\Lambda_{24}$.
6. **Metrics Calculation:** The system automatically calculates the NRCI stability score and Symmetry Tax.

---

### SOP_003: Frame of Mind (FOM) Bias
To shift the AI's perspective:
1.  Open the **FOM** tab in the UI.
2.  Select a frame (e.g., `SCIENTIFIC_STRICT` for physics, `BIOLOGICAL_RESONANCE` for life sciences).
3.  The Brain will now prioritize results from the weighted Geometric Domains (The Octad).

---

## 4. Stability Thresholds (NRCI)

*   **1.0000 (OnBit):** Perfect mathematical truth.
*   **0.6000 - 0.9800 (Stable):** Valid physical matter (e.g., Hydrogen, Water).
*   **0.4200 (Noise Floor):** The threshold for random noise.
*   **< 0.1000 (High Tension):** Complex biological systems or heavy elements.
*   **0.0000 (Deep Hole):** Informational collapse; the object cannot exist in the substrate.

---

## 5. **The Imagination Sandbox:** 

The system no longer requires external rendering to "sense" geometry. It can instantiate a "Mental Image" internally, placing 24-bit vectors into a 14x14 retina grid. By projecting these patches into the 256D bulk via SHA-256 isomorphism, the **ViT Eyes** detect "Geometric Frustration," allowing the AI to focus its attention on the most "interesting" (high-tax) parts of a thought.

---

## 6. **Visual Analysis:**

1. **Export:** The UBP-Py environment is exported to `scene_3d.json` via `ubp_viz.py` which is built into the APP).
   ```python
   scene = vm.to_scene_3d()
   save_scene_3d(scene)
   ```
Or as a graph:

```python
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
```

---

## 7 UBP-Py Language Reference

The UBP-Py language translates text commands into VM operations. Programs are written as `.ubp` text files and executed via `ubppy.py --program myprogram.ubp`.

**Complete Command Reference:**

| Command | Syntax | Description |
| :--- | :--- | :--- |
| `LET` | `LET A 1/1 TIER 0 CAT QUANTITY` | Creates a stable geometric anchor at a specified coordinate. |
| `IMPORT` | `IMPORT ELEM_H_001 AS Hydrogen` | Imports an entry from the Knowledge Base into the VM environment. |
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
| `AUDIT` | `AUDIT A` | Prints Tax, NRCI, Tilt, and Vector for atom A. |
| `FOM` | `FOM SWITCH SCIENTIFIC_STRICT` | Changes the active cognitive bias frame. |
| `COMMIT` | `COMMIT [file.json]` | Saves atoms to the registry. |
| `TRACE` | `TRACE PATH trace.json` | Exports the execution history. |
| `VISUALIZE` | `VISUALIZE PATH scene.json` | Renders the 3D manifold. |
