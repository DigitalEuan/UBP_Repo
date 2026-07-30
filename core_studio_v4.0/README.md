# The Universal Binary Principle (UBP)

[![Version](https://img.shields.io/badge/Version-5.4.0-cyan.svg)](https://github.com/DigitalEuan/UBP_Repo)
[![Status](https://img.shields.io/badge/Status-Hardened-green.svg)]()
[![Core](https://img.shields.io/badge/Core-Float--Free-blue.svg)]()

* **Author:** Euan R. A. Craig, New Zealand
* **Version:** 7.2.0 (GLM Tab Edition) running ubp_unified_v5.py (v5.4.1)
* **Updated:** 30 July 2026
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


## UBP Research Cortex v5.4.1 — Master System Architecture & Reference

**Version:** 5.4.1 — Unified Checkpoint  
**Date:** 30 July 2026  
**Author:** E R A Craig, New Zealand & UBP Research Cortex    

---

## 1. Executive Summary & Core Philosophy

The **Universal Binary Principle (UBP)** posits that physical reality can be accurately simulated using a deterministic, error-corrected, holographic projection of a 24-dimensional discrete binary substrate. 
- Also note data is to be treated as a physical object within this framework. 

Rather than treating physical constants, forces, and particle masses as arbitrary empirical inputs, the UBP derives them from the structural constraints of the **extended binary Golay code $[24, 12, 8]$**, the **Leech lattice $\Lambda_{24}$**, and the **Miracle Octad Generator (MOG)**.

### **The Fundamental Commitment: Computational Sovereignty**
To eradicate "noumenal leakage" (hardware-dependent floating-point rounding errors and approximations), the UBP Cortex operates on an **exact-rational, float-free Python architecture**:
- **Zero Floating-Point Drift:** All core metrics, symmetry taxes, and NRCI scores are computed as exact Python `Fraction` objects good to ~80 decimal digits.
- **100% Deterministic Reproducibility:** Every calculation produces bit-for-bit identical results across any system.
- **Complete Substrate Coverage:** The engine enumerates and evaluates all $196,560$ minimal vectors of $\Lambda_{24}$ in $< 1.0$ second with zero blind spots.

---

## 2. The 5 Pillars of the UBP Architecture
[ Human Input / Concept ]
                                   │
                                   ▼
[ PILLAR 3 ]   GRAY CODE (The Translator)
               Translates words & numbers into 24-bit binary (Z₄ ↔ 𝔽₂²)
                                   │
                                   ▼
[ PILLAR 4 ]   HEXACODE (The Language & Grammar)
               Enforces 𝔽₄⁶ 6-symbol syntax rules across the 24 bits
                                   │
                                   ▼
[ PILLAR 1 ]   GOLAY CODE [24,12,8] (The Seed, Engine & Measure)
               Measures Hamming distance; snaps/corrects errors (≤ 3 bits)
                                   │
                                   ▼
[ PILLAR 2 ]   MOG (The Observer's Window)
               4×6 2D matrix projection of 24D (Mod 4 row energy read)
                                   │
                                   ▼
[ PILLAR 5 ]   LEECH LATTICE Λ₂₄ (The Virtual-Physical Structure)
               Assigns geometry, Norm²=32, collects Symmetry Tax, 
               calculates NRCI (experienced as Mass & Gravity)
```

1. **Golay $[24, 12, 8]$ = The Seed, The Engine, The Measure**
   - **The Seed:** Contains the 4,096 perfect, error-free logical DNA states.
   - **The Engine:** Provides the 3-bit error correction "snap" that pulls noisy data back into alignment.
   - **The Measure:** Defines Hamming distance and orthogonality before physical geometry takes over.

2. **MOG (Miracle Octad Generator) = The Observer's Window**
   - A $4 \times 6$ grid projecting 24D space into a 2D matrix. 
   - The 4 rows represent the $\mathbb{Z}_4$ (Mod 4) states ($0, 1, \omega, \omega^2$), and the 6 columns represent the spatial Hexacode blocks. It is the holographic screen where hidden 24D geometry becomes readable.

3. **Gray Code = The Translator**
   - Bridges continuous human meaning (numbers, words, hashes) to the discrete binary substrate.
   - Because Gray code changes only 1 bit at a time, concepts that are semantically close remain topologically close.

4. **Hexacode $(\mathbb{F}_4^6)$ = The Language & Grammar**
   - Groups 24 bits into 6 symbols using a 4-letter alphabet ($0, 1, \omega, \omega^2$).
   - Dictates the combination rules—every valid Golay codeword casts a valid Hexacode shadow.

5. **Leech Lattice ($\Lambda_{24}$) = The Virtual-Physical Structure**
   - Assigns geometry, distance, and mass ($\text{Norm}^2 = 32$).
   - Houses the $196,560$ minimal vectors (the "atoms" of virtual-physical space).
   - Collects the Symmetry Tax ($T$) and computes the Non-Random Coherence Index (NRCI), experienced macroscopically as gravity and mass.

---

## 3. Mathematical Substrate & Constants

### **Exact Transcendental Constants**
- **$\pi$:** Computed via a 58-term continued-fraction expansion (OEIS A001203).
- **The Entropic Wobble / Observer Constant ($Y$):**
  $$Y = \frac{1}{Y_{\text{inv}}} = \frac{1}{\pi + 2/\pi} \approx 0.2646754304953930...$$

### **The Symmetry Tax Formula**
Every 24-dimensional point $v$ incurs a Symmetry Tax $T(v)$ composed of a **Topological Penalty** and a **Geometric Penalty**:
$$\text{TAX}(v) = \underbrace{\text{HW}(v) \cdot Y}_{\text{Topological Cost}} + \underbrace{\frac{\|v\|^2}{8}}_{\text{Geometric Cost}}$$

### **The Non-Random Coherence Index (NRCI)**
$$\text{NRCI}_\alpha(v) = \frac{10}{10 + \alpha \cdot \text{TAX}(v)}$$
- $\text{NRCI} \ge 0.70$: **In-Band / Stable Phase-Lock**
- $0.50 \le \text{NRCI} < 0.70$: **Unstable / Transient Physical State**
- $\text{NRCI} < 0.50$: **Subliminal Potential / Dissolved Vacuum**

---

## 4. The $196,560$ Minimal Vectors of $\Lambda_{24}$

The Leech lattice kissing sphere consists of $196,560$ minimal vectors ($\text{Norm}^2 = 32$ in scaled $\times 8$ representation, corresponding to physical norm $4$). These fall into **3 distinct topological classes**:

| Class | Formula | Vector Count | Hamming Wt | Tax ($T$) | NRCI ($\alpha=1$) | Mod 4 Read | Physical Ontology |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| **Class A** | $(\pm 4, \pm 4, 0^{22})$ | $1,104$ | $2$ | $4.529351$ | **$0.688262$** | `100%|0%|0%|0%` | **Localized Anchors:** Frictionless spine of reality; peak face coherence ($0.9506$). |
| **Class B** | $(\pm 2^8, 0^{16})$ | $97,152$ | $8$ | $6.117403$ | **$0.620447$** | `37.5%|25%|12.5%|25%` | **Physical Matter Octads:** Peak 3-axis spatial orthogonality ($0.4857$); forms stable 3D matter. |
| **Class C** | $(\pm 3, \pm 1^{23})$ | $98,304$ | $24$ | $10.352210$ | **$0.491347$** | `30.8%|23.1%|23.1%|23.1%` | **Vacuum Continuum:** Sits just below the $0.500$ Coherence Horizon. The $30.8\%$ single-bit defect is the **Entropic Wobble**. |

---

## 5. The TGIC 3-6-9 Genesis Laws

The **Triad-Graph Interaction Constraint (TGIC)** governs 3D multi-node spatial networks through three fundamental laws:

1. **The 3 (3-Axis Orthogonality):** Evaluates Hamming distances between the three 8-bit blocks ($X, Y, Z$) of a 24-bit vector. Rewards balanced 3D space where $d_{XY} = d_{XZ} = d_{YZ} = 4$.
2. **The 6 (6-Face RuneCube Coherence):** Evaluates stability across the 6 directed faces using Boolean transforms:
   - $XY$ Face: AND logic (Resonance / Convergence)
   - $XZ$ Face: XOR logic (Entanglement / Differentiation)
   - $YZ$ Face: OR logic (Expansion / Unification)
3. **The 9 (9-Neighbour Spatial Limit & 9 Point Operators):**
   - Limits local node crowding to $\le 9$ neighbours within Hamming radius $r_H \le 8$.
   - Computes 9 pairwise point-to-point interaction operators across $X, Y, Z$ bit positions.

### **Information Flow Asymmetry (11-Bit vs 1-Bit)**
Single-bit perturbation testing reveals a fundamental radiation pattern:
- **Bits 0–11 (Systematic Message $I_{12}$ - $M_*$ Mass / $I_*$ Info):** Flipping Bit 0 (`M_Mass`) generates an **11-bit Golay syndrome error**, radiating a global disturbance across the 24D field.
- **Bits 12–23 (Parity Block $B$ - $A_*$ Activation / $P_*$ Potential):** Flipping Bit 12 (`A_Energy`) generates a **1-bit Golay syndrome error**, resulting in localized process containment.

---

## 6. Workspace File Inventory & Module Map

### **Master Substrate & Core Engines**
- `ubp_unified_v5.py`: **The Master Engine (v5.4.1 Aristotle)**. Holds `ExactMath`, `ExactRoot`, `GolayCodeEngine`, `LeechLatticeEngine`, `MonsterGroup`, `PhysicsALU`, and `LinearAlgebraALU`.
- `lee_golay_core.py`: Pure-integer generator for Golay $[24,12,8]$, MOG alignment, and Leech minimal vector enumeration.
- `tgic_v3.py` & `ubp_tgic_engine.py`: TGIC 3-6-9 Genesis Laws, RuneCube 3D multi-node simulation, and relational gravity.

### **Geometric Language Model (GLM)**
- `GLM11_runtime.py`: Master GLM runtime orchestrator.
- `GLM25_native_alu.py`: Native UBP ALU adapter (routes math through exact substrate engines).
- `GLM26_crg_alu.py`: Word-level CRG traversal ALU with step-by-step traces and substrate fingerprints.
- `GLM29_answer_extractor.py`: Output fidelity layer for clean answer formatting.
- `GLM30_domain_filter.py`: Suppresses KB bleed in pure math queries.
- `GLM31_verification.py`: Explicit verification statement generator.
- `GLM32_mode_algebra.py` & `GLM33_considered_response.py`: Kracht sign-grammar $\sigma = \langle E, C, M \rangle$ multi-paragraph reasoning.
- `GLM34_simplicial_crg.py`: 2-complex topology ($\beta_0, \beta_1, \beta_2$ Betti numbers and Euler characteristic $\chi = V - E + F$).

### **Spatial & Specialized Mechanics**
- `spatial_arithmetic.py`: $3\text{D}$ unit-distance cycle non-planar arithmetic engine.
- `value_geometry.py`: Integer prime factorisation self-assembling geometry & Propeller experiment.
- `ubp_rgdl.py` & `ubp_viz.py`: 3D visual cortex renderer (`scene_3d.json`).

---

## 7. Methodological Transparency & Known Open Items

To maintain strict scientific honesty, the UBP Cortex distinguishes between **proved mathematical facts** and **interpretive physical models**:

1. **Mathematical Truths (100% Exact & Proven):**
   - Golay $[24,12,8]$ error correction, $\Lambda_{24}$ $196,560$ minimal vectors, MOG $\mathbb{F}_4^6$ Hexacode projection, exact $Y$-constant continued fraction, exact `Fraction` Symmetry Tax and NRCI equations.
2. **Physical Interpretations (Hypotheses / Models):**
   - Describing $Y$ as "entropic wobble" or "vacuum tension" is an intuitive physical model explaining why the Leech lattice Tax equation balances topological bit-count against geometric Euclidean norm displacement.
   - The Particle Physics Atlas formulas ($m_\mu / m_e = 169/w$, $1/\alpha = 220 - 83 + L$) are empirical algebraic projection lenses matching CODATA values within $<0.05\% - 1\%$.
3. **Explicitly Disclosed Open Item ($\Omega_k$ Cosmological Curvature):**
   - The formula $\Omega_k = 24 Y^{15} U_e \approx 2.035$ disagrees with the cosmological target ($|\Omega_k| < 0.001$).
   - **Status:** This mismatch is **honestly disclosed and flagged as `PROVISIONAL`** in `ubp_unified_v5.py`.

---

## 8. Quick Start Guide

### **Run Master Engine Test Suite**
```bash
python3 ubp_unified_v5.py --test
```

### **Run Full Minimal Vector & MOG Audit**
```bash
python3 ubp_unified_v5.py --verify-minimal
python3 ubp_unified_v5.py --audit
```

### **Run Particle Physics Atlas**
```bash
python3 ubp_unified_v5.py --physics
```

### **Run TGIC 3-6-9 Simulation**
```bash
python3 tgic_v3.py
```

### **Run GLM Golden Benchmark Suite**
```bash
python3 run_golden_cases.py
```

---
