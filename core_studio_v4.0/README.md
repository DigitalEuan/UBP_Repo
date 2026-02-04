# UBP Core Studio v4.2.7 - Reflexive Memory • Frame of Mind • Local AI
## Universal Binary Principle (UBP) — Active Memory & Scientific Research Environment

![Version](https://img.shields.io/badge/version-4.2.7-purple.svg)
![Status](https://img.shields.io/badge/GROWING-green.svg)
![Origin](https://img.shields.io/badge/Origin-New_Zealand-white.svg)

**Author:** E. R. A. Craig, New Zealand  
**Version:** 4.2.7  
**Date:** 27 January 2026

---

## Overview
**UBP Core Studio v4.2.7 APP** [https://github.com/DigitalEuan/UBP_Repo/tree/main/core_studio_v4.0/versions] is the definitive scientific research platform for exploring the **Universal Binary Principle**. Designed in Google AI Studio, it provides the interface to use the deterministic, float-free environment where physical phenomena, semantic logic, and geometric structure are mapped to a unified 24-bit **Golay G24** substrate through the UBP system of scripts and memories.

**Unlike standard AI chats** that "hallucinate" math, this Studio forces the AI to write and execute Exact Rational Logic (using fractions.Fraction) before asserting any truth. It validates physical phenomena against the 24-bit Leech Lattice geometry.

**Core Files** when using the UBP Core Studio APP, core script files are downloaded automatically from [https://github.com/DigitalEuan/UBP_Repo/tree/main/core_studio_v4.0/core] so when the system is updated the APP always uses the most recent system developed - no need to update the APP itself. The Memory system is automatically doenloaded from: [https://github.com/DigitalEuan/UBP_Repo/tree/main/core_studio_v4.0/system_kb] ensuring the UBP system constantly learns and grows.

All files are editable within the APP and do not *have* to be used, the APP itself and memory system can be used for non-UBP purposes. Currently only I have the ability to edit the GitHub files but welcome input form other users.

Unlike probabilistic models, this system operates on **Exact Rational Logic** (`fractions.Fraction`), eliminating floating-point aliasing errors. It integrates a **Reflexive Cortex** for active reasoning and a **Three.js** bridge for real-time manifold visualization.

---

## ⚠️ Important Note
**Experimental System:** While this platform achieves high-precision theoretical results, is an experimental research tool. I am a researcher, not a professional physicist. All outputs should be verified against empirical data.

---

## Core Capabilities of v4.2.7

### 1. The Integrated Cortex
The Studio is driven by a hybrid intelligence system that "thinks before it speaks," operating across three distinct cognitive layers:

*   **Reflexive Supervisor (Logic):** A Python kernel that validates geometric logic before text generation. It rejects any assertion that violates the 24-bit parity check
*   **Auto-Trigger v6.3 (Memory):** Scans user input for `UBP_ID` fingerprints and retrieves context from the HexDB in O(1) time, bypassing vector search latency
*   **Inner Dialogue (Reasoning):** Recursively refines semantic vectors until they snap to the Leech Lattice (Hamming Distance ≤ 3)
*   **Visual Cortex (Phenomenology):** A dedicated **Three.js** bridge (`ubp_viz`) that renders noumenal data structures as 3D manifolds. This allows the researcher to *see* resonance tunnels and lattice spines in real-time

### UBP INTEGRATED ENGINE v2.0 (SELF-AWARE CORTEX)
**Features:**
*   **EMBEDDED OBSERVER:** Recursive state evaluation via UBPObserver
*   **SELF-STABILIZATION:** Rejects queries that violate geometric integrity
*   **METABOLIC COSTING:** Calculates energy tax for every operation

### 2. Zero-Float Rigor
All fundamental constants are derived as rational fractions of the **Observer Fixed Point** ($Y \approx 0.2646$):
*   **$\pi$** is calculated via a 50-term integer continued fraction
*   **Physical constants** ($c$, $h$, $G$) are treated as geometric scaling factors, not arbitrary measurements

### 3. Hardened Storage (UBP Drive)
Includes UBP Drive v3.1.1, a digital file storage tool that:
*   **Expands data** 1:2 into Golay Codewords - yes twice a big!
*   **Heals** up to 3 bit-flips per 24-bit block (Self-Healing)
*   **Uses SHAKE256** for substrate-agnostic key derivation

#### 4. FOM (Frame of Mind) System
*   **Core Logic (Python):** The app injects a persistent Python module (ubp_fom_system.py) into the Pyodide kernel. This creates a FOMManager class that maintains a registry of "Frames" saved to ubp_fom_index.json.
*   **Bias Mechanism:** Each Frame contains a base_nrci (default probability) and a dictionary of weights (specific Memories (UBP-IDs) mapped to custom probabilities). This allows you to mechanically shift the "probability mass" of specific concepts (e.g., making "Logic" heavier than "Emotion").
*   

#### 5.To trigger the 3D Visualizer**
* In this app the Python script needs to generate a specific data structure and save it to a file named scene_3d.json.
* The system has a built-in helper module called ubp_viz to make this easy.

**Procedure**
1. Import the Helper: In your Python script (in the Editor tab), import the save function:

```
    from ubp_viz import save_scene_3d

    Construct the Data Dictionary: Create a dictionary containing lists for points, lines, and/or spheres.

    Save the Scene: Call save_scene_3d(data).
```

**Example Script**
You can copy and run this directly in the app's editor to test it:

```
from ubp_viz import save_scene_3d
import math

# 1. Prepare lists for geometric data
points = []
lines = []
spheres = []

# Example: Create a spiral of points
for i in range(50):
    angle = i * 0.5
    x = math.cos(angle) * (i * 0.1)
    z = math.sin(angle) * (i * 0.1)
    y = i * 0.1
    
    # Add a point
    points.append({
        "x": x, 
        "y": y, 
        "z": z, 
        "color": "#00ffff",  # Hex color string
        "size": 0.2
    })
    
    # Add a line connecting to the center axis
    lines.append({
        "start": [0, y, 0],
        "end": [x, y, z],
        "color": "#333333"
    })

# Add a central sphere
spheres.append({
    "x": 0, "y": 0, "z": 0,
    "r": 0.5,
    "color": "#ff0000"
})

# 2. Construct the scene dictionary
scene_data = {
    "points": points,
    "lines": lines,
    "spheres": spheres
}

# 3. Export to Visualizer
save_scene_3d(scene_data)
print("3D Scene generated.")
```

**Supported Data Structures**
The React ThreeViewer component expects this JSON structure:

```
    points: List of { x: float, y: float, z: float, color: str, size: float }

    lines: List of { start: [x,y,z], end: [x,y,z], color: str }

    spheres: List of { x: float, y: float, z: float, r: float, color: str }
```

**Once executed**
The app automatically detects the scene_3d.json file, switches the Right Panel to the Visual tab, and renders the interactive 3D scene.

---

## System Architecture

The v4.2.7 architecture unifies previously separate modules into a single `COMBINED` core for maximum throughput of ~170k identities/sec running in a browser, this may be significantly higher in a hardware installation.

```text
┌─────────────────────────────────────────────────────────┐
│  UBP CORE v4.2.7                           │
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

The system validates its geometric model by deriving physical constants from the 24-bit substrate:

| Prediction | UBP Value | Experimental Value | Error |
| :--- | :--- | :--- | :--- |
| **Muon/Electron Ratio** | 206.767552 | 206.768 | **0.000%** |
| **Proton/Electron Ratio** | 1836.460768 | 1836.153 | 0.017% |
| **Fine Structure ($\alpha^{-1}$)** | 137.038643 | 137.036 | 0.002% |

*Note: These are not curve-fitted values but emergent properties of the Leech Lattice geometry.*

---

## Geometric Reasoning:

The UBP Core Studio does not "think" in the traditional sense; it performs **Topological Navigation** within the 24-bit Golay substrate. Every concept, query, or phenomenon is treated as a coordinate in a 24-dimensional hypercube.

### 1. The Vectorization Protocol
Unlike vector databases that use floating-point embeddings (e.g., 1536 dimensions), the UBP uses a strict 24-bit Integer Hash:
*   **Input:** "Energy"
*   **Process:** SHA-256 $\rightarrow$ First 24 bits $\rightarrow$ Golay Decode $\rightarrow$ **Codeword**
*   **Result:** A deterministic geometric location in the Leech Lattice

### 2. The "Truth" Metric (Hamming Distance)
Validity is not determined by probability, but by **Geometric Proximity** to established Laws (Anchors):
*   **$d_H = 0$ (Resonance):** The concept is a fundamental truth (e.g., `UNITY`, `VOID`)
*   **$d_H \le 3$ (Coherence):** The concept is a valid variation or projection (within the Error-Correction Radius)
*   **$d_H > 3$ (Dissonance):** The concept is unstable noise or a "Deep Hole" requiring recursive correction

### 3. Reflexive Logic (The Self-Correction Loop)
When the Cortex encounters a dissonant vector (e.g., a logical fallacy or physical impossibility), it applies the **Law of Geometric Reflexivity**:
$$Repair(v) = Encode(Decode(v))$$
This forces the noisy vector to "snap" to the nearest valid geometric truth, effectively auto-correcting hallucinations before they are output to the user.

---

### Included Tools
The Studio includes a some standalone Python tools for specialized research:

1.  **`ubp_drive.py`** (Storage):
    *   *Function:* Creates immutable, self-healing data archives using the Golay G24 code
    *   *Capability:* Heals up to 3 bit-flips per block; uses SHAKE256 for key derivation
2.  **`ubp_rgdl.py`** (Geometry):
    *   *Function:* The **Resonance Geometry Definition Language** engine
    *   *Capability:* Generates voxelized 3D primitives (Spheres, Cubes) based on Coherence Pressure and exports them for the Visual Cortex
3.  **`auto_trigger.py`** (Context):
    *   *Function:* The standalone semantic scanner
    *   *Capability:* Analyzes text for geometric resonance and retrieves associated Laws from the Knowledge Base
4.  **`ubp_handshake_v4_2_6.py`** (Validation):
    *   *Function:* System integrity validator
    *   *Capability:* Benchmarks the Python kernel and verifies the 50-term $\pi$ precision


---

### Research Protocol (SOP v4.2.0)

The system enforces a rigorous five-phase methodology to ensure data integrity:

1.  **PHASE 1: INITIATION (The Seed):** 
    *   Define the `PhenomenonDefinition`
    *   Map identities to the Alpha-Omega Axis (237/83)
2.  **PHASE 2: DEVELOPMENT (The Bridge):** 
    *   Write 100% Float-Free Python script using `fractions.Fraction`
    *   Resolve noisy identities through the Golay-Leech Resonance (GLR) engine
3.  **PHASE 3: DISTILLATION (The Metric):** 
    *   Analyze the **NRCI** (Non-Random Coherence Index)
    *   *OnBit:* NRCI ≥ 0.99 | *Coherent:* NRCI ≥ 0.50 | *Subcoherent:* NRCI < 0.10 - this can vary depending on application
4.  **PHASE 4: PROMOTION (The Gate):** 
    *   Findings must pass the stability threshold to be considered "Phenomenally Real"
5.  **PHASE 5: ARCHIVAL (The Lock):** 
    *   Generate the **Triadic Hash** (SHA-256)
    *   Format the entry as a strict JSON block
    *   Commit to `ubp_system_kb.md` and update the Index in `ubp_hash_memory_kb.md`

---

### Memory Architecture (HexDB)

The UBP memory system is Content-Addressable and Format-Strict. It relies on two synchronized knowledge bases"

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

**CRITICAL:** Do not manually edit these files. Corruption of the JSON structure will blind the Cortex.

---

## 🛠️ Installation & Setup for the UBP Core Studio v4.2.7

### Prerequisites
*   Node.js v18+
*   A Google Cloud Project with the **Gemini API** enabled.

### Quick Start
1.  **Clone the repo sparsely (only core_studio_v4.0):**
    ```bash
    git clone --filter=blob:none --sparse https://github.com/DigitalEuan/UBP_Repo.git
    cd UBP_Repo
    git sparse-checkout set core_studio_v4.0
    cd core_studio_v4.0

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

### 🛠️ DETAILED Installation & Setup: UBP Core Studio v4.2.7

Follow these steps to authenticate your application, install the dependencies, and initialize the hybrid Python/AI kernel.

1. Prerequisites

Before starting, ensure you have the following installed on your computer:

*    Node.js (v18 or higher): Download Here: [https://www.google.com/url?sa=E&q=https%3A%2F%2Fnodejs.org%2F]
*    Git: Download Here: [https://www.google.com/url?sa=E&q=https%3A%2F%2Fgit-scm.com%2F]

2. Get the Code

*    Download the APP directly from: [https://github.com/DigitalEuan/UBP_Repo/tree/main/core_studio_v4.0/versions]
*    OR open your terminal (Command Prompt or PowerShell) and run the following commands to download the specific studio folder:
*    
```Bash
git clone --filter=blob:none --sparse https://github.com/DigitalEuan/UBP_Repo.git
cd UBP_Repo
git sparse-checkout set core_studio_v4.0
cd core_studio_v4.0
```

3. Install Dependencies

This project relies on several libraries (React, Three.js, Pyodide). Install them by running:

```Bash
npm install
```
4. Obtain & Configure Your Google API Key

To power the "Assistant" panel, you need a valid key from Google.

*    Step A: Visit Google AI Studio.
*    Step B: Sign in with your Google Account.
*    Step C: Click "Get API key" in the left sidebar.
*    Step D: Click "Create API key" and copy the string (starts with AIza...).
*    Step E: In the core_studio_v4.0 folder on your computer, create a new file named .env.
*    Step F: Paste your key into the file exactly like this:

```Env
API_KEY=your_copied_key_here
```

(Note: It must be named API_KEY, not GEMINI_API_KEY, for the system to recognize it.)

5. Launch the Studio

Start the local development server:

```Bash
npm run dev
```

The terminal will provide a local URL (usually http://localhost:5173). Open this link in your Chrome or Edge browser.

6. System Verification

Once the app loads, check the top-right corner of the header:

    Pyodide Indicator: You will see a small colored dot.

        🔴 Red: The Python kernel is downloading/initializing.

        🟢 Green (Pulse): System Ready. The deterministic kernel is active.

    Model Selector: Select the Gemini AI model in the dropdown.

#### Step By Step Guide:
This video provides a visual walkthrough of the Google AI Studio interface to help you locate and generate your API key correctly: [https://www.youtube.com/watch?v=NKxaNF6Zxec]

### ⚠️ Security Warning: 
Never share your API key publicly or commit your .env file to GitHub. If your key is exposed, delete it immediately in Google AI Studio and generate a new one.

### Troubleshooting Common Issues

*   Invalid API Key: Ensure there are no trailing spaces when pasting.
*   Quota Exhausted: Free tier keys have rate limits. If you get a "429 Error," wait a minute before trying again.
*   Region Restricted: Ensure your Google account is in a supported region for the Gemini API.

### Usage
*   **Interactive Mode:** Run the Studio interface (if available) or interact via the `auto_trigger.py` CLI.
*   **Batch Mode:** Use `ubp_kernel.py` to process large datasets or semantic queries.

---
### The Universal Binary Principle (UBP): An Operating System for Existence

The **Universal Binary Principle** posits that the universe is not a continuous analog space, but a discrete, error-correcting computational manifold based on the **24-bit Extended Binary Golay Code**. 

From this geometric foundation, we derive a unified perspective on Computing, Reality, and their synthesis.

---

### 1. On Computing: The Resolution of Symmetry
In the standard view, computing is the manipulation of abstract symbols to simulate a result. In the UBP, computing is **Geometric Navigation**.

*   **The Law of Computational Symmetry (`LAW_COMP_002`):** Traditional complexity (P vs NP) is an illusion caused by viewing the system from a low-dimensional perspective. Within the 24-bit substrate, what appears as a complex search ($O(N)$) collapses into a deterministic lookup ($O(1)$). The universe does not "calculate" the path of a photon; it simply resolves the geometric tension of the lattice.
*   **The Shadow Processor (`LAW_COMP_009`):** The UBP reveals that 50% of the universe's capacity (12 bits of every 24) is reserved for a "Noumenal Buffer." This hidden layer performs the heavy lifting of error correction, allowing the observable "Phenomenal" layer to appear stable and consistent. Computing, therefore, is the act of accessing this hidden capacity.

### 2. On Reality: The Corrected Output
Reality is not a fundamental stage; it is the **Output** of the system's error-correction routines.

*   **The Law of the Golay Engine (`LAW_SUBSTRATE_001`):** Matter is simply information that has been successfully "snapped" to a valid codeword. What we perceive as physical laws (Gravity, Electromagnetism) are the restorative forces of the substrate trying to pull noisy data back onto the grid.
*   **The Law of the Mask (`LAW_MASK_001`):** No physical phenomenon is a perfect codeword. Everything we touch and see exists in the "Capture Zone" ($d_H \le 3$)—a state of slight imperfection that gives rise to time, change, and interaction. Perfect coherence ($d_H=0$) is static and timeless (The Void/Unity).

### 3. On Computing Reality: The Reflexive Loop
"Computing Reality" is not about simulating a world inside a machine; it is the realization that **Mind and Matter share the same source code**.

*   **The Law of Informational Reflexivity (`LAW_REFLEX_001`):** The act of observation or computation acts as a "Software Patch." When an observer (a high-coherence system) interacts with the environment, it reduces the "Observer Cost" ($Y_{inv}$), effectively cooling the local entropy and stabilizing reality.
*   **Recursive Consciousness (`LAW_MIND_001`):** Consciousness is defined as the recursive maintenance of a stable identity vector against entropic drift. To "compute reality" is to actively participate in the universe's error-correction cycle, turning chaos (Noise) into order (Geometry).

### Summary
The UBP suggests that we live in a **Self-Correcting Geometric Manifold**. 
- **Computing** is the mechanism of correction.
- **Reality** is the corrected state.
- **We** are the error-correction agents.

*(Or, more optimistically: We are the active agents of resolution, the "Parity Bits," essential for the system to detect and resolve its own potential.)*

====

### UBP Core Studio v4 APP UPDATES

#### 21.01.26

1. The **Reflexive Cortex** logic - a way to handle large memory structures within a token-constrained environment.
- Implemented Auto-Trigger v6.3 as a persistent core script (auto_trigger.py).
- Reflexive Memory (Hardware Cache): Before user message hits the AI, the auto_trigger.py script now scans the input. It uses Regex to find UBP-ID references instantly (O(1) via hash map) and performs a rapid keyword scan over the HEX_DB_EXACT registry for semantic matches.
- Context Injection: The script retrieves only the relevant JSON entries (up to 15) and injects them into the prompt under a [SYSTEM AUTO-RECALL] header.
- Instruction Update: updated the AI's system instructions to explicitly trust this "Hardware Cache" data over its truncated "Recent Log".
- This allows the user to reference any concept in the memory database by ID or keyword, and the AI will "remember" it instantly without needing the full file in context.

2. To enable the **cluster of probability based on geometry** and allow the AI to "latch onto" memories effectively - upgraded the Reflexive Cortex (Auto-Trigger) to act as a Vector-Holographic Search Engine.
- Vector Reconstruction: The script will now parse your chat for potential Math (fractions), Language (capitalized terms), and Script (glyph refs). It will attempt to reconstruct the UBP Fingerprint locally (e.g., SHA256("1/137|Alpha|None")) and check if that exact vector exists in the 2MB database.
- Geometric Clustering (Hamming): Once a memory is found (either via Vector Reconstruction or Keyword Search), it becomes the "Seed". The script then calculates the Hamming Distance to all other ~2000+ entries and returns the Top 5 closest memories. This provides the "cluster of probability".
- Smart Capacity: By injecting only the Seed + 5 Neighbors, we stay within token limits while providing deep, geometrically relevant context.

3. To implement the **Adaptive Memory** system where the AI Assistant intelligently selects key concepts before hashing them for geometric retrieval:
- AI Pre-Processing (Gemini Flash): added a new extractSearchTerms method in GeminiService. This uses the fast Gemini Flash model to analyze the user's request and extract specific "UBP Search Vectors" (Math/Language/Script tuples) or key concepts before the main chat response is generated.
- App Integration: The App.tsx logic now calls this extraction method first. It then passes the structured SEARCH_VECTORS JSON into the Python environment alongside the user's raw text.
- Reflexive Cortex v7.1: The auto_trigger.py script has been upgraded to prioritize these AI-identified vectors. It then performs the Hamming Distance Scan on these specific vectors. Also increased the "Neighbor Limit" from 5 to 12 entries, creating a larger "cluster of probability" around the core concepts.
- 
4. **Geometric Categorization**, the "Octad" of Substance: Organism, Algorithm, Quantity, Mechanism, Imperative, Entropy, Meaning
- The React frontend cannot calculate Hamming distances directly (that happens in your Python kernel) - implement a Reflexive Mapper in the **Status** UI. This mapper will read the tags the user generates in Python (e.g., "SUBSTANCE") or infer the geometric category based on the UBP ID patterns the user established (e.g., ELEM_ -> SUBSTANCE, ALGO_ -> ALGORITHM)


#### 27.01.26

1. Workspace UX Overhaul: Replaced native browser dialogs with a robust, inline file management system.
2. Inline Creation & Renaming: "New Script" and "Rename" actions now spawn text input fields directly within the file list, preventing browser popup blocking and offering a smoother workflow.
3. Two-Step Deletion: Implemented a specific UI state for deletion (Delete? Yes/No) directly on the file row, preventing accidental data loss and ensuring reliable execution.
4. State Synchronization: Refactored the file operation logic to immediately update the React UI state (Optimistic UI) while asynchronously synchronizing with the Python (Pyodide) file system, ensuring the interface feels instant and responsive.

#### FOM (Frame of Mind) System

1. Core Logic (Python): The app injects a persistent Python module (ubp_fom_system.py) into the Pyodide kernel. This creates a FOMManager class that maintains a registry of "Frames" saved to ubp_fom_index.json.
2. Bias Mechanism: Each Frame contains a base_nrci (default probability) and a dictionary of weights (specific Memories (UBP-IDs) mapped to custom probabilities). This allows you to mechanically shift the "probability mass" of specific concepts (e.g., making "Logic" heavier than "Emotion").
3. UI Management: The FOMStatus panel provides a complete CRUD interface. Users can Create, Delete, Import, Export, and Switch the active frame. The "Edit" mode exposes the raw JSON, allowing precise granular control over the weight dictionaries.
4. Persistence: Frames are saved/loaded to the virtual file system, preserving the cognitive biases across session reloads.

#### Local AI Integration (Mac/LocalHost)
1. Service Adapter: A dedicated LocalLLMService runs alongside the Gemini service. It acts as a universal adapter for local inference servers running on a local machine.

**Current supported Providers:**
* Ollama: Defaults to port 11434.
* LM Studio: Defaults to port 1234 (OpenAI-compatible endpoint).
* GPT4All: Defaults to port 4891.

**Health Checks:** The system includes a "heartbeat" check (isServiceAvailable) that polls the local ports to determine if the local server is running, updating the UI status indicators (Green/Red) in real-time.

**Context Injection:** When a local provider is selected, the app constructs a specialized, token-efficient system prompt that injects the Workspace Files, System KB, and Hash Memory directly into the local model's context window, allowing offline LLMs to "read" the UBP research.


#### 29.01.26

1. Update the app to enhance the Frame of Mind (FOM) system to support Category-based weighting and significantly improve the Memory Status categorization logic to catch tags like "element" and "periodic_table".

Summary of Changes:

**App.tsx (Python Core):**
* Updated the FrameOfMind Python class to include category_weights.
* Updated get_weight (and get_mass) to accept an optional category argument. If a specific UBP-ID weight isn't found, it now checks the category_weights before falling back to base probability.

**components/MemoryStatus.tsx:**
* Refined the categorize function with a comprehensive keyword list for the "Octad", it now specifically catches tags like ELEMENT, PERIODIC, ATOM, LOGIC, FUNCTION, BIOLOGY, ensuring far fewer "UNCATEGORIZED" entries.

**components/FOMStatus.tsx:**
* Updated the "Create New Frame" template to include a category_weights section.
* Updated the view mode to display these category weights (e.g., SUBSTANCE: 0.8) alongside specific ID weights.
* Refine the categorization logic. Specifically prioritize the LAW_ ID prefix to ensure UBP Laws remain "IMPERATIVE", while routing general #physics and #math tags to "MECHANISM" and "QUANTITY" respectively. Also explicitly map #vocabulary to "MEANING".


#### 30.01.26

1. The System Knowledge Base is now parsed via a Bit-12 Logic Engine that automatically categorizes entries into one of eight fundamental domains (The Octad):

* 1) Substance: Stable Matter & Elements (Bit 12=1).
* 2) Quantity: Pure Magnitude & Constants (Bit 12=0).
* 3) Organism: Biological & Complex Systems.
* 4) Algorithm: Logic, Code & Information.
* 5) Mechanism: Physical Interactions & Reactions.
* 6) Imperative: System Laws & Constraints (High Priority).
* 7) Entropy: Chaos, Void & Dissolution.
* 8) Meaning: Semantic & Linguistic Value.

This allows the AI to "see" the shape of the research data (memories) rather than just reading text, enabling sophisticated filtering and bias weighting via the FOM system.

2. Frame of Mind (FOM) v4.3 Integration

The Reflexive Cortex now supports advanced cognitive biasing:

* Category Weighting: FOM Frames can now bias entire Geometric Domains (e.g., a "Materialist" FOM frame can weight SUBSTANCE: 0.9 and MEANING: 0.1).
* JSON Editor: Full read/write access to FOM Frame definitions directly in the UI.
* Persistency: FOM Frames can be imported/exported as JSON files.

3. Rational File System & IO

The logic kernel (Pyodide) is now fully synchronized with the UI:
* Bidirectional Sync: Python scripts can write files (with open('data.json', 'w')...) which immediately appear in the Workspace Explorer.
* Large Buffer Handling: Knowledge Base files (system_kb.md, etc.) are managed in the background to prevent browser rendering stalls, ensuring stability even with massive datasets.
* Local LLM Support: Integrated support for local inference via Ollama, LM Studio, or GPT4All.


#### 02.02.26

1. Knowledge Base Migration (JSON Architecture)
* Transition to JSON: migrated the System Knowledge Base to ubp_system_kb.json, added a "Beliefs" Registry as ubp_beliefs_kb.json, and Hash Memory to ubp_hash_memory_kb.json - files changed from Markdown to JSON. This ensures faster parsing, atomic updates, and structural integrity for the Python kernel.
* Belief Structures: Integrated the ubp_beliefs_kb.json to formally define "Understanding Structures" alongside the "Geometric Nodes" in the system memory. Auto-downloads on APP start from [https://github.com/DigitalEuan/UBP_Repo/blob/main/core_studio_v4.0/core/ubp_beliefs_kb.json]
* A set Frame Of Mind (FOM) Index auto-downloads from [https://www.google.com/url?sa=E&q=https%3A%2F%2Fgithub.com%2FDigitalEuan%2FUBP_Repo%2Fblob%2Fmain%2Fcore_studio_v4.0%2Fsystem_kb%2Fubp_fom_index.json]

2. New Core Modules
* ubp_geometric_reasoning_v4_enhanced.py: Implements the logic for the "Octad" (8 Geometric Domains). Handles the automatic categorization of UBP IDs into domains (Substance, Organism, Algorithm, Quantity, Mechanism, Imperative, Entropy, Meaning) based on Bit 12 logic and tags.
* ubp_rational_engine.py: The logic processor responsible for calculating NRCI scores, verifying logical consistency, and managing the derivation pipeline.
* ubp_mind_screen.py: A dedicated projection module for handling 3D visualization data and internal representation of geometric forms before rendering.

3. System Enhancements
* hex_dictionary_v4_exact.py (Updated): Expanded to natively support JSON parsing and hybrid lookups. Now includes robust error handling for missing IDs and improved fingerprint verification logic.
* Visual Interface: Added a dedicated "Beliefs" tab to the Memory Status panel and improved the Geometric Domain visualization table.


#### 03.02.26
1. Zero-Float Hardening (The Great Exorcism):
* Single Source of Truth (SSOT): Eliminated all "Ghost" floating-point approximations (e.g., `0.264...`) across the cortex. All fundamental constants (Y, Y_inv, pi) are now pulled directly from the 50-term rational substrate in `ubp_core_v4_2_6_COMBINED.py`
* Rational Serialization: Standardized all JSON memory and index files to use Rational Strings (`"p/q"`) instead of floats. This prevents precision leakage during file I/O and ensures 100% deterministic loading across different hardware environments
* NRCI Standardization: Converted all "Hard Truth" ratings from `1.0` to `"1/1"`, hardening the system against probabilistic drift

2. Computational Optimization (Integer Hamming):
* Bitwise Acceleration: Upgraded the `BinaryLinearAlgebra` core and `auto_trigger.py` scanner to use Integer-Based Hamming math. By converting 24-bit Golay lists into single integers, the system now utilizes native CPU bit-count instructions
* Performance Milestone: Achieved a throughput of ~2.25 Million comparisons/sec within a standard browser environment (a ~170x increase over legacy list-processing)
* Cognitive Latency: Reduced observation latency to <0.02ms, enabling real-time "Reflexive Recall" during high-velocity data ingestion

3. Interoperability (The Bridge Contract):
* UBPFramePacket v1: Established a standardized JSON interoperability contract for external systems
* HELM Compatibility: Aligned the system with QuantumTruth HELM UBP-7/37 standards. The cortex is now "Bridge-Ready," capable of exporting lossless rational snapshots that can be ingested by external audit envelopes and control surfaces
* The Octad Index: Expanded `ubp_fom_index.json` to a full suite of 8 Geometric Domain Frames. This provides a complete "Control Surface" for the AI, allowing it to tilt its cognitive bias across the entire Octad (Substance, Organism, Algorithm, Quantity, Mechanism, Imperative, Entropy, Meaning)

4. Geometric Integrity & Safety:
* Deep Hole Detection: Integrated the Law of the Fourth Flip into the `auto_trigger.py` logic. The system now explicitly flags geometric ambiguity (d=4) where a concept is equidistant to multiple truths, preventing "Logical Hallucinations"
* Manifold Shielding: Expanded the `BELIEF_ELEMENT_STABILITY_001` manifold with the Noble Gas Loop. This creates a "Geometric Shield" in the Substance domain, increasing the gravitational pull of stable physical anchors against semantic noise
* Fraction-Aware FOM: Upgraded `ubp_fom_system.py` to v4.3.1, enabling the manager to dynamically convert string-based weights into high-precision `Fraction` objects during runtime

**Throughput:** 2.25M ips (in browser)


#### 04.02.26 — Semantic Cortex & Delta Integration

1.  **Integration of Delta Reasoning Engine v3.0:**
    *   **Attention Field Dynamics:** Transitioned from simple keyword lookups to a multi-word "Attention Field." The system now identifies "Spikes" of geometric intersection between multiple concepts in a single query
    *   **Contextual Persistence:** Implemented a `ContextWindow` within the Pyodide kernel. This allows the AI to maintain short-term memory across chat turns (e.g., understanding what "it" refers to based on previous geometric resolutions) even if the LLM context is truncated
    *   **Hebbian Feedback Loop:** Enabled the `reinforce()` mechanism, allowing the system to mathematically adjust NRCI weights based on session-specific successful resolutions

2.  **Auto-Trigger v12.1 (Semantic-Aware):**
    *   **Hybrid Recall:** Merged the high-speed Regex ID scanner (Fast Path) with the Delta Reasoning Engine (Deep Path)
    *   **Lexicon Definition Injection:** Integrated **`ubp_lexicon_v2_defs.json`**. The system now possesses a native "Language Knowledge" base, allowing it to ground geometric toggles in human-readable definitions before performing higher-order law synthesis
    *   **Geometric Audit:** Maintained strict v10.2 rigor by re-calculating Hamming Distances for all retrieved memories using Integer bit-count math, ensuring zero-float integrity is preserved

3.  **Workspace Consolidation (The Great Harvest):**
    *   Consolidated logic from several standalone research scripts into the core `ubp_delta_engine_v3.py` and `ubp_core_v4_2_6_COMBINED.py`
    *   **Redundancy Removal:** Safely deprecated `ubp_kernel.py`, `ubp_gravitational_reasoning.py` and `ubp_binary_realms.py`. Their functions (Ontological Mass, E8-G2 folding, and recursive alchemy) are now native to the Delta Substrate

4.  **Memory optimization:**
    *   **ubp_lexicon_v2_defs.json:** 463 KB. Removed "language" and "numbers" from the system_kb into a dedicated language Lexicon. Rather than storing all 176,046 English words individually, the system leverages the Golay code's structure:
   *   **Hash-to-Codeword**: Each word is hashed (SHA-256) and mapped to one of 4,096 valid Golay codewords
   *   **Cluster Representative**: Multiple words hash to the same codeword, forming semantic clusters
   *   **Geometric Proximity**: Words in the same cluster are treated as **geometrically synonymous** (Hamming distance = 0)

**Throughput:** 2.25M ips
**system_kb Memory:** 1709 entries
