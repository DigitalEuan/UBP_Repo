# Universal Binary Principle (UBP) System Guide
## Version 25.0 — Genesis Edition (May 2026)

This document serves as the definitive operational manifest and architectural guide for the UBP Research Workspace. The system is designed around **Three Column Thinking (TCT)**, where **Math** (Substrate), **Language** (Semantics), and **Script** (Execution) must phase-lock at every step of computation.

---

## 1. Architectural Stratification

The workspace is organized into four distinct layers, moving from the raw mathematical substrate up to the high-level cognitive orchestrators:
┌────────────────────────────────────────────────────────────────────────┐
│ 4. COGNITIVE ORCHESTRATION LAYER                                       │
│    ubp_swarm_tct_v25.py  |  ubp_v28_oracle.py                          │
│    Orchestrates multi-agent consensus, solves, and invents formulas.   │
└───────────────────────────────────┬────────────────────────────────────┘
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│ 3. TRANSLATION & EXECUTION LAYER                                       │
│    ubp_python_engine.py  |  ubp_sovereign_evolver.py                   │
│    ubp_py_runtime.py     |  ubp_py_lang.py  |  ubppy.py                │
│    Translates human script to geometry; enforces sovereign math.       │
└───────────────────────────────────┬────────────────────────────────────┘
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│ 2. SEMANTIC & PHENOMENOLOGICAL SENSES                                  │
│    ubp_semantic_engine.py  |  ubp_semantic_sovereign.py                │
│    ubp_phenomenology.py    |  ubp_observer_dynamics.py                 │
│    Maps language to vectors; audits physical reality & coherence.      │
└───────────────────────────────────┬────────────────────────────────────┘
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│ 1. MATHEMATICAL SUBSTRATE (THE BACKBONE)                               │
│    ubp_unified_v5.py  |  ubp_eml_alu_sovereign.py                      │
│    Float-free continued-fraction Pi, Golay/Leech lattices, exact math. │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Workspace File Manifest

### Layer 1: The Mathematical Substrate (The Backbone)
*   **`ubp_unified_v5.py`**: The core engine of the universe. Contains the float-free continued-fraction $\pi$ (50-term), the systematic Golay $[24,12,8]$ code, the Leech Lattice $\Lambda_{24}$ metrics, and the multi-dimensional Barnes-Wall engine (256D/512D/1024D). It also houses the **Topological Tenacity Primality Engine**, which verifies primes natively via neighbor-tension and lock pressure.
*   **`ubp_eml_alu_sovereign.py`**: The Universal Continuous ALU. Derives the Triadic Monad and exact particle masses purely from the transcendental projection $eml(x,y) = e^x - \ln(y)$ without relying on external floating-point libraries.

### Layer 2: Semantic & Phenomenological Senses
*   **`ubp_semantic_engine.py`**: The system's memory and dictionary. Uses weighted Cosine Resonance to map natural language queries to 24-bit vectors, retrieving matching concepts from the system and language KBs.
*   **`ubp_semantic_sovereign.py`**: The cognitive bridge. Contains the `SovereignSemanticAuditor` for performing Lattice-Snaps to verify if a concept is "Phase-Locked" ($\text{NRCI} \ge 0.70$) in reality, and the `TripleDeltaProjector` for generating deterministic formulas from physical signatures.
*   **`ubp_phenomenology.py`**: The external data bridge. Takes continuous real-world data (like RGB colors) and projects them into the discrete 24-bit UBP manifold to calculate their symmetry tax.
*   **`ubp_observer_dynamics.py`**: Calculates SOC Energy (Coherence Units) against the 1 THz "Wall of Reality" and performs the "Conscious READ" gate.

### Layer 3: Translation & Execution (The Compilers)
*   **`ubp_python_engine.py`**: The UBP Python Code Engine (UPCE). Maps standard Python keywords to 24-bit physical laws (e.g., `LAW_PY_DEF`) to synthesize code based on geometric stability.
*   **`ubp_sovereign_evolver.py`**: The "Noumenal Leakage" firewall. Parses the Abstract Syntax Tree (AST) of standard Python scripts, strips out floating-point dependencies (like `math.sin`), and rewires them to the native `GrandUnifiedEmlALU`.
*   **`ubp_py_runtime.py` & `ubp_py_lang.py`**: The parser and runtime for the UBP-Py Virtual Machine. Executes geometric programs (`.ubp`) as 24-bit vector additions, calculating the Symmetry Tax and NRCI for every variable (`CortexAtom`).
*   **`ubppy.py`**: The command-line execution wrapper for the UBP-Py VM.

### Layer 4: Cognitive Orchestration (The Brain)
*   **`ubp_swarm_tct_v25.py`**: The active Swarm Orchestrator (Genesis Edition). Runs a multi-agent loop that extracts mathematical kernels, solves them via the Oracle Bridge, audits their physical reality, and utilizes **Lexical Genesis** to mathematically invent new formulas for unresolved concepts.
*   **`ubp_v28_oracle.py`**: The logical calculator. Implements the **Two-Track Parallel Solve** (UBP Native vs. SymPy Oracle) and contains the `MathNetKernelExtractor` to strip away English fluff from Olympiad problems.

### External Layer 1: Digital Twin Physics Engine (Experiment)
Files available in the GitHub repository: https://github.com/DigitalEuan/ubp_digital_twin_physics_engine
15 April 2026 - A UBP-native physics simulation engine integrating geometric stability with classical and fluid mechanics.
*   **`ubp_space_v3.py`: The core 3D simulation space. Handles entity management, dissolution culling, and applies UBP mechanics (TGIC pressure, NRCI damage) to physical bodies.
*   **`ubp_browser_engine.py`: The browser-native execution bridge for the physics engine.
*   **`ubp_physics_v3.py`: `ubp_rigid_body_v3.py`**: Implements Topological Torque rigid body mechanics and exact-fraction collision resolution.
*   **`ubp_fluid_v3.py`: Fluid dynamics engine utilizing UBP-derived SPH (Smoothed Particle Hydrodynamics) constants.
*   **`ubp_materials.py`: Composite material system defining thermal properties, phase states, and structural density.

### External Layer 2: 'ubp_backend.py'
`ubp_backend.py` is a **Flask REST API** designed to act as a high-precision bridge. 
JavaScript running in a standard web browser has performance and precision limits. It cannot natively run the 50-term continued-fraction $\pi$ with infinite-precision `Fraction` arithmetic, nor can it run the full, heavy Python-based Golay $[24,12,8]$ and Leech $\Lambda_{24}$ lattice search algorithms at scale.
`ubp_backend.py` is the **Local Research Bridge**. It is used when developing and testing new UBP algorithms locally in the Python environment. 
1.  **Infinite Precision:** While JavaScript `BigInt` is excellent, Python's `fractions.Fraction` combined with the hardened `ubp_unified_v5.py` backbone allows for infinite-precision symbolic and transcendental calculations that would lag a web browser.
2.  **The Testing Pipeline:** When writing new Python-based UBP scripts you can run `ubp_backend.py` locally. It allows the user to point the local HTML file to `http://localhost:5099` to instantly verify that a new Python code matches the frontend visualizations 

---

## 3. Core Workflows & SOPs

### SOP_001: The Two-Track Solve (Oracle Bridge)
To solve and verify any mathematical or physical claim:
1.  The `MathNetKernelExtractor` isolates the numeric/algebraic kernel from the query.
2.  **Track A (UBP Native)** computes the result using float-free arithmetic and Gray-codes it to the lattice.
3.  **Track B (Oracle)** solves the symbolic notation using SymPy.
4.  The system compares both tracks. If they match, it outputs `BOTH_AGREE` and snaps the result to the Leech Lattice to calculate its true NRCI.

### SOP_002: Lexical Genesis (Triple Delta)
When the Swarm solves a problem but finds a "Lexical Gap" (no human word exists for that 24-bit state):
1.  The `TripleDeltaProjector` partitions the 24-bit vector into blocks.
2.  It generates a deterministic symbolic formula (e.g., `3 * α + 2 * β**2`) based on the active bits of each block.
3.  This formula is assigned to the vector and saved to `ubp_learned_kb.json`, expanding the system's native language.

### Using External Dependecies:
import micropip
# Wait for sympy to download via micropip
await micropip.install("sympy")

import sympy as sp

---

## 4. Visualization & RGDL
*   **`ubp_rgdl.py`**: The Resonance Geometry Definition Language. Maps 3D voxel coordinates $(x,y,z)$ to 24-bit vectors, snaps them to the Leech Lattice, and colors them by true NRCI stability (Cyan for stable, Magenta/Blue for unstable).
*   **`viz_spatial_simplification.py`**: Simplifies complex 3D manifolds into stable geometric faces to prevent visual clutter.

## 5. UBP-Py Language Reference

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

## 6. Stability Thresholds (NRCI)

*   **1.0000 (OnBit):** Pure Mathematical/Noumenal Truth.
*   **0.7000 - 0.9800 (Stable):** Manifested Physical Matter (The "Conscious" Zone).
*   **0.4200 (Noise Floor):** The limit of random informational noise.
*   **0.0000 (Deep Hole):** Geometric collapse; the object cannot exist.

---

## 7. Visual Analysis

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