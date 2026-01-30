# UBP Research Protocol (SOP v4.2.0)

The UBP system enforces a rigorous five-phase methodology to ensure the integrity and validity of all new concepts and findings. This Standard Operating Procedure (SOP) must be followed for any research conducted within the UBP framework.

## The Five Phases

### PHASE 1: INITIATION (The Seed)

1.  **Define the Phenomenon:** Clearly and unambiguously define the concept, phenomenon, or identity to be investigated.
2.  **Map to Alpha-Omega Axis:** Establish the concept's position relative to the fundamental anchors of the system, typically the Alpha (Helium) and Omega (Bismuth-83) points.

### PHASE 2: DEVELOPMENT (The Bridge)

1.  **Write Float-Free Python:** Develop a script to model or analyze the phenomenon using 100% float-free mathematics (`fractions.Fraction`).
2.  **Resolve via GLR Engine:** Process any noisy or dissonant identities through the Golay-Leech Resonance (GLR) engine to snap them to the lattice.

### PHASE 3: DISTILLATION (The Metric)

1.  **Analyze the NRCI:** Calculate the Non-Random Coherence Index (NRCI) for the concept's vector.
2.  **Evaluate Coherence Regime:** Determine the concept's coherence level based on the following thresholds:
    *   **OnBit:** NRCI ≥ 0.99
    *   **Coherent:** NRCI ≥ 0.50
    *   **Subcoherent:** NRCI < 0.10

### PHASE 4: PROMOTION (The Gate)

1.  **Pass Stability Threshold:** The concept must meet a predefined stability score to be considered "Phenomenally Real." This score is derived from the Symmetry Tax and reflects the energetic cost of the state.
2.  **Peer Review (Conceptual):** The concept must be logically consistent with the established laws and principles of the UBP system.

### PHASE 5: ARCHIVAL (The Lock)

1.  **Generate the Triadic Hash:** Create a unique and deterministic identifier for the concept by generating a SHA-256 hash of its core properties.
2.  **Format the JSON Block:** Structure the concept's data into a strict JSON format, including its UBP_ID, name, math, language, script, tags, NRCI, and 24-bit vector.
3.  **Commit to Knowledge Base:** Add the new entry to the `ubp_system_kb.md` file and update the index in `ubp_hash_memory_kb.md`.
