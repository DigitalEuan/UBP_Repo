# The Universal Binary Principle (UBP)

[![Version](https://img.shields.io/badge/Version-5.4.0-cyan.svg)](https://github.com/DigitalEuan/UBP_Repo)
[![Status](https://img.shields.io/badge/Status-Hardened-green.svg)]()
[![Core](https://img.shields.io/badge/Core-Float--Free-blue.svg)]()

* **Author:** Euan R. A. Craig, New Zealand
* **Version:** 7.2.0 (GLM Tab Edition) running ubp_unified_v5.py (v5.4.0)
* **Updated:** 19 July 2026
* **License / Status:** Experimental research platform — *please double-check results against your own work before drawing conclusions.*

| Resource | Link |
| :--- | :--- |
| **Live Environment (Google AI Studio)** | <https://ai.studio/apps/6d78d479-2a4e-4e34-89b3-4b87b85d5b9a> |
| **Core Studio App Repository** | <https://github.com/DigitalEuan/ubp_core_studio_app> |
| **Digital Twin Physics Engine Repository** | <https://github.com/DigitalEuan/ubp_digital_twin_physics_engine> |
| **Primary Knowledge Bank** | [`system_kb/ubp_system_kb.json`](system_kb/ubp_system_kb.json) (746 entries, 420 Laws) |

---

The **Universal Binary Principle (UBP)** is a unified computational framework that posits reality, language, and logic are deterministic, error-corrected projections of a 24-bit substrate. This repository contains the official implementation of the UBP Core Stdio App made through Google AI Studio.

---

## 🌌 Core Philosophy: Geometric Purity
The UBP operates on the axiom that fundamental physical constants are not arbitrary "fine-tuned" values, but are topological artifacts of the substrate's geometry. 

As of **v5.4.0 (June 2026)** - no hardcodes, fundamental constants are derived purely from substrate primitives:
*   **The Triadic Monad:** $\pi \cdot \phi \cdot e$
*   **The Entropic Wobble ($w$):** The fractional residue of the Monad.
*   **The Observer Constant ($Y$):** $1 / (\pi + 2/\pi)$.

---

## 📂 System Architecture

### Mathematical Substrate (`ubp_unified_v5.py`)
The "Backbone." A float-free, exact rational engine using Python's `fractions.Fraction`.
*   **Golay Engine:** Systematic encoding and error correction (up to 3 bits) (the engine)
*   **Leech Engine:** Symmetry tax calculation and stability diagnostics (the substrate)
*   **Barnes-Wall Engine:** Recursive projection into 256D, 512D, and 1024D macro-bulk (the detail)

### 1. The Immutable Core (Substrate & Physics)
*These files form the float-free mathematical and physical backbone of the UBP.*
*   **`ubp_unified_v5.py`**: The master substrate engine (v5.4.0). Contains Golay, Leech, Barnes-Wall, and exact math logic.
*   **`ubp_eml_alu_sovereign.py`**: The native transcendental ALU (v9.2).
*   **`physics.py`**: Exact metrics and coherence calculations.
*   **`math_atlas.py`**: The mathematical voxel construction engine.
*   **`refined_nrci.py`**: The multi-shell, sign-sensitive NRCI calculator.
*   **`ubp_tgic_engine.py`**: The 3-6-9 relational gravity and interaction engine.
*   **`ubp_observer_dynamics.py`**: Handles the 1 THz Wall of Reality and SOC energy.
*   **`ubp_phenomenology.py`**: The modular scanner and noumenal projector.

### 2. The Active Cognitive Engine (GLM Stack)
*This is the reasoning, semantic, and language generation architecture. All files are prefixed with `GLM`.*
*   **`GLM00_config.py` to `GLM34_simplicial_crg.py`**: The complete GLM pipeline. It handles everything from SVD distributional vectors and ontological grammar to simplicial 2-complex topology and deliberative reasoning.
*   **`test_v321_levelling.py` & `run_golden_cases.py`**: Active test harnesses for the GLM stack.

### 3. The UBP-Py Virtual Machine
*The domain-specific geometric programming language environment.*
*   **`ubppy.py`**: The CLI entry point.
*   **`ubp_py_lang.py`**: The language parser (LET, SYNTH, PULSE, etc.).
*   **`ubp_py_runtime.py`**: The VM state and lattice environment.

### 4. Active Tooling, Orchestration & Visualization
*Utilities for managing the KB, generating code, and rendering 3D manifolds.*
*   **Orchestration:** 'ubp_intent.py' replaces 'ubp_v28_oracle.py` (The Two-Track Solve bridge) and `ubp_swarm_tct_v25.py` (Genesis Swarm).
*   **Visualization:** `ubp_viz.py` (React bridge), `ubp_rgdl.py` (Resonance Geometry), `viz_loader.py`, `viz_spatial_simplification.py`.
*   **KB Management:** `ubp_kb_architect.py` (Gray Code vector generation), `ubp_ingest.py`, `hash_all_1.py`, `ubp_mog_mapper.py`.
*   **Code Generation:** `ubp_python_engine.py` (UPCE v2.2) and `ubp_sovereign_evolver.py` (AST compiler).
*   **`import_sympy.py`**: A simple Sympy import script for Pyodide with micropip test.
*   **`ubp_genesis_boot.py`**: The Phase 1/2 boot engine. Useful for hard resets, but not needed for daily operations.


---

# UBP Core Studio & Geometric Language Machine (GLM)

**UBP Core Studio App** is a research-grade environment for exploring the **Universal Binary Principle (UBP)**. This repository now integrates two primary components: the **UBP Core Studio** (a web-based, interactive research environment) and ta new **Geometric Language Machine (GLM)** (a deliberative, symbolic-geometric AI engine).

---

## TAB 1. UBP Core Studio (Web Interface)

The Studio provides a visual workspace for research.

### Key Features
*   **Hybrid AI Architecture:** Leverages **Gemini** for high-level reasoning and connects to **Local LLMs** (Ollama, LM Studio) for private inference.
*   **Computational Workspace:** In-browser Python kernel (via **Pyodide**) allows executing scripts within a virtual filesystem.
*   **Reflexive Memory System:** Manages persistent knowledge bases (System, Language, Beliefs, Study) that evolve with your research.
*   **Visualization:** Integrated matplotlib plotting and Three.js 3D viewer for geometric domain exploration.

---

## TAB 2. Geometric Language Machine (GLM) *Under Development*

GLM is the UBP experimental AI/LLM. It moves beyond token probability by grounding concepts in a 24-dimensional geometric substrate based on the Leech Lattice and Golay code.

---

## Project Structure

| Component | Current Path | Description |
| :--- | :--- | :--- |
| **Studio Frontend** | `/src` | React/Vite interface and orchestration. |
| **GLM Engine** | `/glm_test_dir` | Core backend reasoning, substrate, and KB management (the App uses these files). |
| **Knowledge Bases** | `/glm_test_dir` | `ubp_system_kb.json` and `ubp_lang_kb_combined_v4.json` (needs to be moved to the normal '/src'). |

---

## 4. Getting Started

### Web Interface
Access the environment via the deployed application URL. It is fully self-contained in the browser.

### Backend Engine (Development)
For direct engine development or benchmark running:
1.  **Requirements:** Python 3.12+ (optimized for native bitwise ops).
2.  **Dependencies:** Ensure `numpy` and `sympy` are installed (`pip install numpy sympy`) - sympy should only be used for verification, never actual computation.
3.  **Running GLM:**
    *   **Self-Test:** `python3 glm_test_dir/GLM12_cli_entry.py --test`
    *   **Interactive Chat:** `python3 glm_test_dir/GLM12_cli_entry.py --chat "what is hydrogen?"`

---

## 5. Security & Privacy
*   **Client-Side Execution:** Studio Python code runs entirely in your browser's sandbox.
*   **Local AI Privacy:** Local LLM integration ensures sensitive prompts never leave your local machine.
*   **Secure API Handling:** User Gemini API keys are injected at runtime; they are never persisted in the codebase.

---

## License
This project is part of the UBP research initiative.
