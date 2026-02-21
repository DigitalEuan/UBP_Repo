# UBP CORE STUDIO v4.2.7 — SYSTEM FILE MANIFEST (v5.3 STANDARD)

### 1. THE KERNEL LAYER (Source of Truth)
*These files define the mathematical laws and constants. They are the dependencies for all other scripts.*

*   **`ubp_core_v5_3_merged.py`**
    *   **Description:** The Monolith. Contains `UBPUltimateSubstrate` (50-term Pi), `GOLAY_ENGINE` (4096 codewords), `LEECH_ENGINE` (Lattice geometry), and `PARTICLE_PHYSICS`.
    *   **System Role:** **The Kernel**. The absolute mathematical authority.
    *   **Research Usage:** Imported by other scripts. Do not edit directly.

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

*   **`ubp_brain_consolidated.py`**
    *   **Description:** Manages the `ubp_system_kb.json`. Handles the Hierarchy of Matter (Quarks -> Atoms) and Tax Analysis.
    *   **System Role:** **Librarian & Architect**.
    *   **Research Usage:** Used to decompose complex objects or query the lineage of a concept.

*   **`auto_trigger.py`**
    *   **Description:** Scans user input for UBP-IDs/keywords and fetches context from the Brain.
    *   **System Role:** **Reflexive Cortex**.
    *   **Research Usage:** Enables "Chat with Memory," allowing the AI to recall UBP concepts without hallucination.

*   **`ubp_understanding_engine.py`**
    *   **Description:** Performs deep traversal, pathfinding, and insight generation on the knowledge graph.
    *   **System Role:** **The Analyst**.
    *   **Research Usage:** Generates reports on relationships between memories (e.g., "Find all objects with Symmetry Tax similar to Gold").

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
    *   **Research Usage:** The starting point for new studies (e.g., "Map the concept of 'Justice' to the grid").

*   **`ubp_discovery_engine.py`**
    *   **Description:** Generates random concept interactions (XOR), snaps them to Golay codewords, and checks for emergent resonance.
    *   **System Role:** **The Collider**.
    *   **Research Usage:** Automated research to find "Hidden Resonances" between existing concepts.

*   **`ubp_tgic_engine.py`**
    *   **Description:** Triad-Graph Interaction Constraint. Simulates dynamic behavior and time evolution using Deterministic Flux.
    *   **System Role:** **Lattice Physics Simulator**.
    *   **Research Usage:** Simulates how concepts interact over time (e.g., "Do Logic and Emotion merge or repel?").

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

### 6. DATA FILES (JSON)
*   **`ubp_system_kb.json`**: The Main Memory (Laws, Elements, Constants).
*   **`ubp_beliefs_kb.json`**: Complex belief structures and manifolds.
*   **`ubp_lexicon_v2_defs.json`**: Dictionary definitions for semantic grounding.
*   **`rational_cortex.json`**: Output data for 3D visualization.
*   **`README.md`**: System Documentation.


# UBP RESEARCH PROTOCOL: STUDY WORKFLOW (v5.3)

### PHASE 1: INITIATION (The Seed)
Every study begins by defining a phenomenon and mapping it to the 24-bit substrate.
1.  **Define the Phenomenon:** Identify what you are studying (e.g., a chemical reaction, a linguistic concept, or a physical force).
2.  **Use `ubp_phenomenology.py`:** Create a `PhenomenonDefinition`. This script is your **Scanner**. It translates your data (RGB values, text strings, or magnitudes) into a 24-bit vector.
3.  **Initial Mapping:** Run the script to see where the concept "lands" on the lattice.
    *   *Insight:* Check the initial **Symmetry Tax**. High tax means the concept is "heavy" and complex; low tax means it is "light" and fundamental.

### PHASE 2: PERSPECTIVE SHIFTING (The Bias)
Reality in UBP is influenced by the observer's frame.
1.  **Activate FOM:** Use the **FOM Panel** or **`ubp_fom_manager_v2.py`** to switch "Frames of Mind."
2.  **Test Stability:** Observe how the **NRCI (Stability)** of your phenomenon changes across different frames (e.g., `SCIENTIFIC_STRICT` vs. `POETIC_MEANING`).
3.  **Identify the Domain:** Determine which of the **Octad Domains** (Substance, Algorithm, etc.) provides the highest resonance for your data.
    *   *Insight:* If a concept is only stable in a specific FOM, it is a "Contextual Variant." If it is stable in all frames, it is a "Universal Anchor."

### PHASE 3: VISUALIZATION (The Lens)
Use the 3D manifold to see the "shape" of your data.
1.  **Import `ubp_viz.py`:** Generate a 3D scene of your study.
2.  **Look for "Geometric Charge" (Tilt):**
    *   **0° Tilt:** The concept is perfectly aligned with **Systemic North**. It is a fundamental truth.
    *   **180° Tilt:** The concept is an inversion (Entropy/Chaos).
3.  **Simplify the View:** If the manifold is too cluttered, run **`viz_spatial_simplification.py`**. This will only draw lines that form stable "Faces" with the Origin (0,0,0), revealing the hidden geometry of your study.

### PHASE 4: ITERATION & DYNAMICS (The Simulation)
Test how your concept behaves over "time" or through interaction.
1.  **Run `ubp_tgic_engine.py`:** This is your **Lattice Physics Simulator**.
2.  **Simulate Interaction:** Smash your concept against an existing Law (XOR operation).
3.  **Observe the "Snap":** Does the resulting vector "snap" to a valid Golay codeword, or does it fall into a **Deep Hole** ($d_H=4$)?
    *   *Insight:* A concept that consistently "snaps" to stable codewords during interaction is "Phenomenally Real."

### PHASE 5: VALIDATION (The Audit)
Before a discovery is promoted to memory, it must pass a rigorous audit.
1.  **Calculate Final NRCI:** Use **`ubp_nrci_calculator.py`**.
    *   **NRCI $\ge 0.99$:** Hard Truth (OnBit).
    *   **NRCI $\ge 0.50$:** Coherent Phenomenon.
    *   **NRCI $< 0.10$:** Subcoherent Noise (Reject).
2.  **Cross-Reference:** Run **`ubp_comprehensive_tests.py`** to ensure your results don't violate established particle physics or elemental constants.

### PHASE 6: ARCHIVAL (The Lock)
If the result is stable and provides new insight, commit it to the system memory.
1.  **Propose a Candidate:** Output a code block labeled `SYSTEM_KB_CANDIDATE`.
    ```json
    {
      "ubp_id": "LAW_YOURNAME_001",
      "name": "Title of Discovery",
      "math": "The raw DNA/Measurements",
      "lexicon": "[Name], [Instructional definition for the AI]",
      "atlas": { "vector": [24 bits], "nrci": "p/q", "tax": "p/q" },
      "tags": ["DOMAIN", "STUDY_NAME"]
    }
    ```
2.  **Sync the Index:** Run **`hash_all_1.py`**. This ensures the **`ubp_hash_memory_kb.json`** is updated so the **`auto_trigger.py`** can "remember" your discovery in future chats.

---

### SUMMARY OF TOOLS FOR STUDIES
*   **To Start:** `ubp_phenomenology.py` (Map data to bits).
*   **To Perceive:** `ubp_fom_manager_v2.py` (Change cognitive bias).
*   **To See:** `ubp_viz.py` (Render 3D manifold).
*   **To Interact:** `ubp_tgic_engine.py` (Simulate dynamics).
*   **To Prove:** `ubp_nrci_calculator.py` (Verify stability).
*   **To Save:** `hash_all_1.py` (Update memory index).