# UBP Core Studio v4.2.6
## Universal Binary Principle (UBP) — Resonant Memory & Phenomenology Environment

![Version](https://img.shields.io/badge/version-4.2.6-purple.svg)
![Status](https://img.shields.io/badge/Status-Production_Ready-green.svg)
![Origin](https://img.shields.io/badge/Origin-New_Zealand-white.svg)

**Author:** E. R. A. Craig, New Zealand  
**Version:** 4.2.6 (Combined Ultimate)  
**Date:** 19 January 2026

---

## Overview
**UBP Core Studio v4.2.6** is the definitive scientific research platform for exploring the **Universal Binary Principle**. It provides a deterministic, float-free environment where physical phenomena, semantic logic, and geometric structure are mapped to a unified 24-bit **Golay G24** substrate.

Unlike probabilistic models, this system operates on **Exact Rational Logic** (`fractions.Fraction`), eliminating floating-point aliasing errors. It integrates a **Reflexive Cortex** for active reasoning and a **Three.js** bridge for real-time manifold visualization.

---

## ⚠️ Important Note
**Experimental System:** While this platform achieves high-precision theoretical results (e.g., 0.000% error on Muon/Electron mass ratio), it is an experimental research tool. I am a researcher, not a professional physicist. All outputs should be verified against empirical data.

---

## Core Capabilities (v4.2.6)

### 1. The Integrated Cortex
The Studio is driven by a hybrid intelligence system that "thinks before it speaks," operating across three distinct cognitive layers:

*   **Reflexive Supervisor (Logic):** A Python kernel that validates geometric logic before text generation. It rejects any assertion that violates the 24-bit parity check.
*   **Auto-Trigger v6.3 (Memory):** Scans user input for `UBP_ID` fingerprints and retrieves context from the HexDB in O(1) time, bypassing vector search latency.
*   **Inner Dialogue (Reasoning):** Recursively refines semantic vectors until they snap to the Leech Lattice (Hamming Distance ≤ 3).
*   **Visual Cortex (Phenomenology):** A dedicated **Three.js** bridge (`ubp_viz`) that renders noumenal data structures as 3D manifolds. This allows the researcher to *see* resonance tunnels and lattice spines in real-time.

### 2. Zero-Float Rigor
All fundamental constants are derived as rational fractions of the **Observer Fixed Point** ($Y \approx 0.2646$):
- $\pi$ is calculated via a 50-term integer continued fraction.
- Physical constants ($c$, $h$, $G$) are treated as geometric scaling factors, not arbitrary measurements.

### 3. Hardened Storage (UBP Drive)
Includes **UBP Drive v3.1.1**, a digital alchemy tool that:
- Expands data 1:2 into Golay Codewords.
- Heals up to 3 bit-flips per 24-bit block (Self-Healing).
- Uses **SHAKE256** for substrate-agnostic key derivation.

---

## System Architecture

The v4.2.6 architecture unifies previously separate modules into a single `COMBINED` core for maximum throughput (~170k identities/sec).

```text
┌─────────────────────────────────────────────────────────┐
│  UBP CORE v4.2.6 (COMBINED)                             │
├─────────────────────────────────────────────────────────┤
│  [KERNEL LAYER]                                         │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐   │
│  │ Golay Engine │  │ Leech        │  │ Particle     │   │
│  │ (4096 CW)    │  │ Lattice      │  │ Physics      │   │
│  └──────────────┘  └──────────────┘  └──────────────┘   │
│         ▲                 ▲                 ▲           │
│         └─────────┬───────┴───────┬─────────┘           │
│                   │ FRACTION MATH │                     │
│                   └───────┬───────┘                     │
│                           ▼                             │
│  [APPLICATION LAYER]                                    │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐   │
│  │ TGIC Engine  │  │ UBP Drive    │  │ RGDL Viz     │   │
│  │ (Dynamics)   │  │ (Storage)    │  │ (3D Geometry)│   │
│  └──────────────┘  └──────────────┘  └──────────────┘   │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

---

## Scientific Benchmarks

The system validates its geometric model by deriving physical constants from the 24-bit substrate.

| Prediction | UBP Value | Experimental Value | Error |
| :--- | :--- | :--- | :--- |
| **Muon/Electron Ratio** | 206.767552 | 206.768 | **0.000%** |
| **Proton/Electron Ratio** | 1836.460768 | 1836.153 | 0.017% |
| **Fine Structure ($\alpha^{-1}$)** | 137.038643 | 137.036 | 0.002% |

*Note: These are not curve-fitted values but emergent properties of the Leech Lattice geometry.*

---

## Geometric Reasoning: The Engine of Truth

The UBP Core Studio does not "think" in the traditional sense; it performs **Topological Navigation** within the 24-bit Golay substrate. Every concept, query, or phenomenon is treated as a coordinate in a 24-dimensional hypercube.

### 1. The Vectorization Protocol
Unlike vector databases that use floating-point embeddings (e.g., 1536 dimensions), the UBP uses a strict **24-bit Integer Hash**.
*   **Input:** "Energy"
*   **Process:** SHA-256 $\rightarrow$ First 24 bits $\rightarrow$ Golay Decode $\rightarrow$ **Codeword**.
*   **Result:** A deterministic geometric location in the Leech Lattice.

### 2. The Truth Metric (Hamming Distance)
Validity is not determined by probability, but by **Geometric Proximity** to established Laws (Anchors).
*   **$d_H = 0$ (Resonance):** The concept is a fundamental truth (e.g., `UNITY`, `VOID`).
*   **$d_H \le 3$ (Coherence):** The concept is a valid variation or projection (within the Error-Correction Radius).
*   **$d_H > 3$ (Dissonance):** The concept is unstable noise or a "Deep Hole" requiring recursive correction.

### 3. Reflexive Logic (The Self-Correction Loop)
When the Cortex encounters a dissonant vector (e.g., a logical fallacy or physical impossibility), it applies the **Law of Geometric Reflexivity**:
$$Repair(v) = Encode(Decode(v))$$
This forces the noisy vector to "snap" to the nearest valid geometric truth, effectively auto-correcting hallucinations before they are output to the user.

---

### Included Tools
The Studio includes a suite of standalone Python tools for specialized research:

1.  **`ubp_drive.py`** (Storage):
    *   *Function:* Creates immutable, self-healing data archives using the Golay G24 code.
    *   *Capability:* Heals up to 3 bit-flips per block; uses SHAKE256 for key derivation.
2.  **`ubp_rgdl.py`** (Geometry):
    *   *Function:* The **Resonance Geometry Definition Language** engine.
    *   *Capability:* Generates voxelized 3D primitives (Spheres, Cubes) based on Coherence Pressure and exports them for the Visual Cortex.
3.  **`auto_trigger.py`** (Context):
    *   *Function:* The standalone semantic scanner.
    *   *Capability:* Analyzes text for geometric resonance and retrieves associated Laws from the Knowledge Base.
4.  **`ubp_handshake_v4_2_6.py`** (Validation):
    *   *Function:* System integrity validator.
    *   *Capability:* Benchmarks the Python kernel and verifies the 50-term $\pi$ precision.


---

### Research Protocol (SOP v4.2.0)

The system enforces a rigorous five-phase methodology to ensure data integrity:

1.  **PHASE 1: INITIATION (The Seed):** 
    *   Define the `PhenomenonDefinition`.
    *   Map identities to the Alpha-Omega Axis (237/83).
2.  **PHASE 2: DEVELOPMENT (The Bridge):** 
    *   Write 100% Float-Free Python using `fractions.Fraction`.
    *   Resolve noisy identities through the Golay-Leech Resonance (GLR) engine.
3.  **PHASE 3: DISTILLATION (The Metric):** 
    *   Analyze the **NRCI** (Non-Random Coherence Index).
    *   *OnBit:* NRCI ≥ 0.99 | *Coherent:* NRCI ≥ 0.50 | *Subcoherent:* NRCI < 0.10.
4.  **PHASE 4: PROMOTION (The Gate):** 
    *   Findings must pass the stability threshold to be considered "Phenomenally Real."
5.  **PHASE 5: ARCHIVAL (The Lock):** 
    *   Generate the **Triadic Hash** (SHA-256).
    *   Format the entry as a strict JSON block.
    *   Commit to `ubp_system_kb.md` and update the Index in `ubp_hash_memory_kb.md`.

---

### Memory Architecture (HexDB)

The UBP memory system is **Content-Addressable** and **Format-Strict**. It relies on two synchronized knowledge bases.

#### 1. The System Knowledge Base (`ubp_system_kb.md`)
Contains the full semantic and executable data for every Law, Constant, and Primitive.
**Format:**
```json
{
    "737cc49b2d0777f4ddc3f8aad6b478575fd4ea90529e8f069da3b08728eb7376": {
        "ubp_id": "ELEM_H_001",
        "name": "Element: Hydrogen (H)",
        "math": "Z=1 | M=1.008 | Config=1s1",
        "language": "Hydrogen is element 1 in the periodic table with atomic mass 1.008. Electron configuration: 1s1. Category: nonmetal. Common oxidation states: [1, -1]. Distance from Omega anchor (Bi-83): 82 positions.",
        "script": "element = {'symbol': 'H', 'name': 'Hydrogen', 'Z': 1, 'mass': 1.008, 'config': '1s1', 'category': 'nonmetal', 'oxidation': [1, -1]}; omega_distance = abs(1 - 83)",
        "tags": [
            "element",
            "periodic_table",
            "nonmetal",
            "period_1"
        ],
        "nrci": "1/1",
        "fingerprint": "737cc49b2d0777f4ddc3f8aad6b478575fd4ea90529e8f069da3b08728eb7376",
        "vector": [
            1,
            0,
            1,
            0,
            0,
            0,
            0,
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
            1,
            1,
            1,
            1,
            0,
            0
        ]
    },
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

**CRITICAL:** Do not manually edit these files unless you are performing a **Phase 5 Archival**. Corruption of the JSON structure will blind the Cortex.

---

## 🛠️ Installation & Setup

### Prerequisites
*   Node.js v18+
*   A Google Cloud Project with the **Gemini API** enabled.

### Quick Start
1.  **Clone the Repo:**
    ```bash
    git clone https://github.com/DigitalEuan/UBP_Repo.git
    cd UBP_Repo/core_studio_v4.0
    ```
2.  **Install Dependencies:**
    ```bash
    npm install
    ```
3.  **Configure API Key:**
    Create a `.env` file in the root:
    ```env
    API_KEY=your_google_gemini_api_key
    ```
4.  **Launch:**
    ```bash
    npm run dev
    ```

### Usage
*   **Interactive Mode:** Run the Studio interface (if available) or interact via the `auto_trigger.py` CLI.
*   **Batch Mode:** Use `ubp_kernel.py` to process large datasets or semantic queries.

---

**"The universe does not calculate; it resolves symmetries within the 24-bit manifold."**
