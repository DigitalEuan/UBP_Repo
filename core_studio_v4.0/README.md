# UBP Core Studio v4.0 Ultimate
> **Universal Binary Principle (UBP) — Research & Phenomenology Environment**

![Version](https://img.shields.io/badge/version-4.0.0-blue.svg)
![Status](https://img.shields.io/badge/Status-Research_Phase-orange.svg)
![Location](https://img.shields.io/badge/Origin-New_Zealand-white.svg)

**Author:** Euan R. A. Craig  
**Version:** 4.0.0  
**Date:** December 2025

---

## 🔬 Overview
**UBP Core Studio** is a research platform designed to provide a new scientific perspective on information and phenomena through the **Universal Binary Principle (UBP)**. 

The application integrates a deterministic mathematical core with an advanced phenomenological simulation engine. By utilizing an embedded **Python kernel (Pyodide)**, the system ensures that all calculations—from Golay Code syndromes to Leech Lattice coordinates—are executed with exact arithmetic, bypassing the floating-point errors inherent in standard computing.

---

## 📑 Table of Contents
* [The v4.0 Research Pipeline](#1-the-v40-research-pipeline)
* [Embedded Python Kernel](#2-embedded-python-kernel-pyodide)
* [Integrated Research Assistant](#3-integrated-research-assistant-ai)
* [Knowledge Base Management](#4-knowledge-base-kb-management)
* [Multi-Modal Visualization](#5-multi-modal-visualization)
* [Core Architecture](#core-architecture)
* [Getting Started](#getting-started)

---

## Key Features

### 1. The v4.0 Research Pipeline
The Studio guides researchers through a rigorous, five-phase scientific process:
1.  **Phase 1: Initiation** — Define the Phenomenon Definition and seed the ontological field.
2.  **Phase 2: Development** — The "Info-Pheno Loop" where **Layer A** (Information Core) and **Layer B** (Phenomenology) are analyzed in parallel.
3.  **Phase 3: Distillation** — Cross-layer synthesis to identify anomalies and formulate "Domain Laws."
4.  **Phase 4: Promotion** — Evaluating findings for promotion to the System Knowledge Base as universal invariants.
5.  **Phase 5: Archival** — Locking the study for historical record and workspace clearing.

### 2. Embedded Python Kernel (Pyodide)
* **Exact Arithmetic:** Native support for `fractions.Fraction` to maintain absolute precision.
* **Scientific Stack:** Pre-loaded with `NumPy`, `Pandas`, `SciPy`, and `Matplotlib`.
* **Virtual Filesystem:** Persistent workspace at `/home/pyodide` for scripts, datasets, and logs.

### 3. Integrated Research Assistant (AI)
* **Grounded Reasoning:** Powered by **Google Gemini**, hard-coded with the v4.0 Pipeline Protocol.
* **Context Aware:** Automatically ingests the System KB, Study KB, and attached research documents.
* **Code Generation:** Capability to write, debug, and "inject" Python scripts directly into the Studio editor.

### 4. Knowledge Base (KB) Management
* **System KB:** The "Persistent Intelligence" of the app. Synchronizes with the Global UBP Repository.
* **Study KB:** Active session-based storage for domain-specific observations (e.g., Hematology, Atomic physics).
* **Anti-Bloat Strategy:** Strict rules define the threshold between a "Universal Law" and a "Subject Observation."

### 5. Multi-Modal Visualization
* **3D Visuals:** Interactive **Three.js** viewer for 24-D Leech Lattice projections and 6D Bitfield distributions.
* **2D Analytics:** Integrated Matplotlib rendering for resonance charts and statistical analysis.

---

## 🏗 Core Architecture

### Layer A: Information Core (`ubp_core.py`)
The non-negotiable mathematical substrate.
* **Binary Golay Code (G24):** 12-bit message to 24-bit codeword encoding/decoding.
* **Leech Lattice (L24):** Scaled-integer representation of the 24-dimensional lattice.
* **CanonicalRecord:** The immutable informational identity of any observable.

### Layer B: Phenomenology Engine (`ubp_phenomenology_runner.py`)
The execution layer for simulated reality.
* **OffBit24:** The 24-bit ontological "atom."
* **Bitfield6D:** A sparse, discrete spatial substrate ($x, y, z, t, type, state$).
* **TGIC:** The Triad Graph Interaction Constraint—the guardian of physical plausibility.

---

## ⚠️ Limitations
This implementation represents a functional framework for development. Currently, the ability to accurately model all scales of reality is not complete. Additional mechanisms for precision can be introduced by the user during specific studies.

---

## 🚀 Getting Started

### Access
* **Web Version:** [Launch UBP Core Studio](https://ai.studio/apps/drive/12WTBHvu_PHgzyM7_sAvXUOiKwG8jNG07)

### Setup
1.  **Initialize Kernel:** The Pyodide kernel loads automatically. Wait for the `[SYSTEM] Ready` signal in the console.
2.  **API Key:** If using a local version, provide a **Google Gemini API Key** in the header to activate the Research Assistant.
3.  **Sync KB:** The Studio will attempt to pull the latest System KB from GitHub. It defaults to local baseline if offline.
4.  **Attach Documents:** Use the **paperclip icon** in the Chat Interface to upload PDF/TXT research papers.
5.  **Run Study:** Select `study_1.py` and click **RUN** to execute the baseline initiation.

---

## 🔗 Resources
* **Official Repository:** [GitHub - DigitalEuan/UBP_Repo](https://github.com/DigitalEuan/UBP_Repo)
* **Subject Studies:** [/studies](https://github.com/DigitalEuan/UBP_Repo/tree/main/core_studio_v4.0/studies)
* **Version History:** [/versions](https://github.com/DigitalEuan/UBP_Repo/tree/main/core_studio_v4.0/versions)
