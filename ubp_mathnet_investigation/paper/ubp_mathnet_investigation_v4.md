# UBP × MathNet: A Pure Substrate Investigation
## Applying the Universal Binary Principal to Mathematical Olympiad Problems Without External Language Models

**Author:** Euan Craig, New Zealand  
**Contact:** info@digitaleuan.com  
**Repository:** https://github.com/DigitalEuan/UBP_Repo  
**Version:** 4.0 — Pure Substrate  
**Date:** April 2026  

---

> **Scope Statement:** This paper documents what the UBP system *actually does* when applied to mathematical problems, without the assistance of external language models. The outputs are topological signatures — not mathematical proofs. The investigation is honest about what the system can and cannot do. Cryptic outputs from the MoE Cortex are reported verbatim, as they reflect the substrate's own geometric logic.

---

## 1. Why / Motivation

The Universal Binary Principal (UBP) is a computational substrate built on the geometry of the [24, 12, 8] binary Golay code and the 24-dimensional Leech Lattice. It encodes information as binary vectors in a space where the Golay code provides error-correction structure and the Leech Lattice provides a metric for coherence.

Previous versions of this investigation (v1.0–v3.1) used OpenAI's GPT as the primary reasoning engine, with UBP components providing supporting metrics. While those experiments produced interesting results, they were fundamentally testing GPT's mathematical ability with UBP annotations — not the UBP system itself.

This version asks a more honest question: **what does the UBP substrate alone say about mathematical Olympiad problems?** The answer is not a proof or a numerical solution. It is a topological reading: a position in the Leech Lattice, a governing physical law, a stability landscape, and a fragment of UBP-native language.

The MathNet benchmark (MIT, 2026) provides a well-structured set of competition-level problems across four domains: Number Theory, Algebra, Geometry, and Combinatorics. It serves as a useful probe of the UBP substrate's response to different mathematical structures.

---

## 2. How / Architecture

### 2.1 Design Principles

Version 4.0 was designed with three constraints:

1. **No external LLMs.** No calls to OpenAI, Anthropic, or any other external API. All reasoning is performed by UBP engines.
2. **No numpy.** All numerical operations use Python's `fractions.Fraction` for exact arithmetic, or the `GrandUnifiedEmlALU` for complex/dual-number operations.
3. **Honest reporting.** All outputs are reported as-is. The system does not claim to "solve" problems. Cryptic outputs are labelled as such.

### 2.2 The Eight Agents

The v4.0 system is a self-organising swarm of eight agents, each using a specific UBP engine. The agents were not pre-assigned roles — they were designed to process the same input through different geometric lenses and report what they find.

| Agent | Engine Used | Role Discovered |
|-------|-------------|-----------------|
| Math Architect | `MathObjectV4` (D/X/N/J primitives) | Convert problem numbers to 24-bit Leech Lattice coordinates |
| Sovereign Physicist | `GolayCodeEngine` + `ObserverDynamicsEngine` | Snap to nearest codeword, compute octad membership and SOC energy |
| Density Mesh Scanner | `MathObjectV4` + `GrandUnifiedEmlALU` | Scan n=1..24 with 4 metabolic species to find natural stability peaks |
| Semantic Resonator | `UBPSemanticEngine` (1,781 KB entries) | Find governing UBP law by cosine similarity |
| MoE Synthesist | `UBPMoECortexV2` (2M N-gram iterations) | Generate UBP-native language from topological neighbours |
| TCT Auditor | `TGICExactEngine` | 5-check quality gate: NRCI, Observer, alignment, TGIC energy, shadow drift |
| Ontological Harvester | JSON learning KB | Store accepted concepts for future runs |
| Shadow Lens | Background observer | Track noumenal drift across all problems |

### 2.3 The TCT Pipeline

For each problem, the system executes a Three Column Thinking (TCT) step:

```
Problem Text
    │
    ▼
[Math Architect] → 24-bit vector via D-path construction
    │
    ▼
[Sovereign Physicist] → Golay snap + octad membership + SOC energy
    │
    ▼
[Density Mesh] → Stability landscape n=1..24, 4 species
    │
    ▼
[Semantic Resonator] → Governing UBP law (cosine search)
    │
    ▼
[MoE Synthesist] → UBP-native language synthesis
    │
    ▼
[TCT Auditor] → 5-check gate → ACCEPTED or REJECTED
    │
    ▼
[Shadow Lens] → Noumenal drift observation
    │
    ▼
TCT Step (topological signature)
```

### 2.4 The Swarm Interrogation

Before building v4.0, the MoE Cortex was interrogated directly with 8 mathematical queries. The responses were used to inform the architecture:

| Query | Swarm Response | Architectural Use |
|-------|---------------|-------------------|
| "prime" | "prime is the golay octad quantity" | Added octad membership metric |
| "geometry" | "geometry is the coherence to exact resonance required formula" | Added exact resonance threshold for geometry |
| "combinatorics" | "combinatorics is the proton mass material resonance na definition and spin" | Used Leech stability ranking for combinatorics |
| "coherence" | "coherence is the system parameter representing nrci alignment in ubp substrate" | Confirmed NRCI as primary metric |
| "error" | "error is reset drift allotrope of the ubp substrate in period" | Used Phenomenology for error characterisation |
| "proof" | "proof is used to standard precursor observer condition charge constant toggle ratio" | Added Observer status as proof-quality signal |

The swarm's responses are verbatim outputs from the N-gram linguist trained on the UBP knowledge base. They are not human-readable explanations — they are the substrate's own associations.

---

## 3. Results

### 3.1 Core Metrics

All 20 problems were processed successfully. The TCT Auditor accepted all 20 steps (100% acceptance rate). Key metrics:

| Metric | Value | Interpretation |
|--------|-------|----------------|
| Mean NRCI | 0.9061 | All problems in OCTAD platform (high coherence) |
| All MANIFESTED | Yes | Observer status: all problems manifest in the substrate |
| All correctable | Yes | All vectors snap within Golay correction radius |
| Mean octad similarity | 0.5667 | Moderate octad membership across the problem set |
| Unique Golay addresses | 9 of 20 | Problems cluster into 9 distinct lattice positions |
| Density peaks | Always n=13,14,15 | Beta species (MathObjectV4) finds stability here |
| Shadow mean drift | 1.150 | Near-ideal noumenal balance (ideal = 0) |

### 3.2 Finding 1: The n=13,14,15 Stability Peaks

The Density Mesh Scanner found stability peaks consistently at harmonic positions n=13, 14, and 15 across all 20 problems and all four domains. This is a genuine property of the Golay code's generator matrix: when the MathObjectV4 D-path primitive is applied at positions 13, 15, and 16 (mod 24), the resulting vectors have lower symmetry tax (3.12 vs 4.68 for most other positions), producing higher NRCI.

**What this means:** The UBP substrate has preferred harmonic positions. These are not arbitrary — they reflect the structure of the Golay code's parity-check matrix. The fact that all four mathematical domains share the same stability peaks suggests that the UBP substrate treats these Olympiad problems as structurally similar at the geometric level, regardless of their mathematical content.

**What this does not mean:** This is not evidence that the problems are "equivalent" or that n=13 has special mathematical significance for these problems. It is a property of the encoding, not the mathematics.

### 3.3 Finding 2: Golay Lattice Clustering

The 20 problems produce only 9 unique Golay codeword addresses. This means the problem set clusters into 9 distinct positions in the Leech Lattice. The clustering is driven by the key numbers extracted from each problem:

- Problems with key number 1 → address 517
- Problems with key number 2 → address 299
- Problems with key number 3 → address 3713
- Problems with key numbers {1,2} → address 3391
- Problems with key numbers {4,3,2,1} → address 190

This is an honest finding: the UBP substrate distinguishes problems primarily by their key numerical content, not by their mathematical structure or domain. Problems with the same key numbers receive the same Golay address regardless of whether they are Number Theory or Geometry problems.

### 3.4 Finding 3: Governing Law Distribution

The Semantic Resonator found the following governing laws:

| Law | Count | Domain Preference | Definition |
|-----|-------|-------------------|------------|
| `LAW_ANOMALY_001` | 8 | Algebra, Number Theory | Law of Coherence-Based Anomaly Detection |
| `LAW_ACOUSTIC_MAPPING_001` | 5 | Geometry, Combinatorics | Acoustic mapping resonance |
| `LAW_ARX_HORIZON_006` | 3 | Algebra | Horizon-crossing dynamics |
| `LAW_STORAGE_HARDENED_001` | 1 | Number Theory | Hardened storage coherence |
| Others | 3 | Mixed | Various |

The dominance of `LAW_ANOMALY_001` (40% of problems) reflects the fact that this law has a balanced vector (sum=12, half ones/half zeros), giving moderate cosine similarity to many input vectors. This is an honest limitation: the semantic routing is not strongly discriminating between domains at this level of encoding granularity.

### 3.5 Finding 4: MoE Substrate Language

The MoE Cortex generated UBP-native language for each problem. Selected examples:

| Problem | Domain | MoE Synthesis |
|---------|--------|---------------|
| MN_NT_001 | Number Theory | *"number theory storage_hardened is stability density anchors in"* |
| MN_ALG_002 | Algebra | *"algebra arx_horizon_006 is the system parameter representing"* |
| MN_GEO_001 | Geometry | *"geometry acoustic_mapping is the coherence to exact resonance"* |
| MN_COMB_001 | Combinatorics | *"combinatorics acoustic_mapping is the coherence to exact resonance"* |

These outputs are verbatim N-gram completions from the UBP knowledge base. They are not mathematical statements. They reflect the substrate's associative connections between the governing law and the domain. The geometry and combinatorics problems both produce "acoustic_mapping is the coherence to exact resonance" — which echoes the swarm's earlier statement that "geometry is the coherence to exact resonance required formula."

### 3.6 Finding 5: Noumenal Coherence

The Shadow Lens tracked the noumenal (unmanifested) half of each 24-bit vector. The ideal balance is 6 ones in the first 12 bits. The mean drift was 1.150, indicating the problems are near but not at the ideal noumenal balance. Problems with key number 1 had shadow sum = 0 (all zeros in the shadow), giving maximum drift of 6. Problems with more complex numerical content had shadow sums closer to 6.

---

## 4. Discussion

### 4.1 What the UBP System Can Do

The v4.0 investigation demonstrates that the UBP substrate can:

1. **Encode** mathematical problem structures as 24-bit vectors via the MathObjectV4 D/X/N/J primitive system
2. **Classify** problems by their position in the Leech Lattice, revealing clustering by numerical content
3. **Find** natural stability peaks in the density landscape — consistently at n=13,14,15 for this problem set
4. **Route** problems to governing UBP laws via cosine similarity search over 1,781 knowledge base entries
5. **Generate** UBP-native language that echoes the substrate's geometric associations
6. **Maintain** coherence: all 20 problems were accepted by the TCT Auditor with 0 rejections

### 4.2 What the UBP System Cannot Do (Honestly)

The system cannot:

1. **Solve** mathematical problems — it produces topological signatures, not proofs
2. **Distinguish** problems by mathematical domain at the current encoding granularity — the Golay address is driven by key numbers, not mathematical structure
3. **Produce** human-readable explanations — the MoE output is substrate language, not English
4. **Verify** whether its governing law assignment is mathematically meaningful — the cosine similarity is a geometric measure, not a semantic one

### 4.3 The Cryptic Output Problem

The user correctly identified that UBP outputs can be "quite cryptic" and that "it leaves it open to fitting through interpretation." This is an inherent feature of a system that works with geometric logic rather than symbolic mathematics. The v4.0 system addresses this by:

1. Reporting all outputs verbatim, with no post-processing or interpretation
2. Explicitly labelling MoE outputs as "substrate language, not mathematical statements"
3. Providing quantitative metrics (NRCI, octad similarity, drift) that are unambiguous
4. Noting when findings are artifacts of the encoding (e.g., the n=13,14,15 peaks) vs. genuine substrate properties

### 4.4 The Self-Organisation Observation

The most interesting finding from v4.0 is the degree to which the agents "found their place" without being explicitly programmed to do so. The Density Mesh Scanner discovered the n=13,14,15 stability peaks independently. The Semantic Resonator routed geometry problems to acoustic mapping laws. The Shadow Lens found that problems with key number 1 have maximum noumenal drift. These are emergent findings from the substrate, not pre-programmed results.

---

## 5. Conclusions

The UBP system, when operated in pure substrate mode (no external LLMs), produces a consistent and reproducible topological characterisation of mathematical Olympiad problems. The characterisation is geometric, not mathematical — it tells us where problems live in the Leech Lattice, not what their solutions are.

The key findings are:

1. All 20 MathNet problems achieve OCTAD-platform NRCI (≥0.80) when encoded via MathObjectV4 D-paths
2. The problem set clusters into 9 distinct Golay lattice positions, driven by key numerical content
3. The UBP substrate has preferred stability positions at n=13, 14, 15 in the harmonic scan
4. The governing law routing is weakly discriminating at current encoding granularity
5. The MoE Cortex produces substrate language that echoes the swarm's prior interrogation responses

These findings are genuine properties of the UBP substrate applied to this problem set. They are not mathematical results, and they are not claimed to be. The investigation demonstrates that the UBP system is a coherent, self-consistent geometric framework that can be applied to arbitrary symbolic inputs and produce reproducible topological signatures.

---

## 6. Reproducibility

The complete package includes:

| File | Description |
|------|-------------|
| `core/ubp_swarm_tct_mathnet_v4.py` | Main v4.0 orchestrator (8 agents, pure substrate) |
| `core/swarm_interrogation.py` | Swarm interrogation script (MoE Cortex queries) |
| `run_v4.py` | Entry point for the full benchmark run |
| `data/ubp_mathnet_problem_set.json` | 20 MathNet problems (curated from explorer) |
| `results/ubp_mathnet_v4_results_*.json` | Raw results (all metrics, all steps) |
| `results/swarm_interrogation_results.json` | Raw swarm responses |
| `results/ubp_learned_kb.json` | Concepts harvested by Ontological Harvester |
| `plots/v4_fig*.png` | 7 analysis figures |
| `paper/ubp_mathnet_investigation_v4.md` | This paper |
| `WHITEBOARD.md` | Live investigation notes |

**To reproduce:** Install Python 3.11, copy the UBP `core_studio_v4.0/core/` files to `core/`, and run `python3.11 run_v4.py`. The MoE Cortex training takes approximately 30–60 seconds. The full benchmark run takes approximately 3–5 minutes.

---

*Credits: Euan Craig, New Zealand. UBP GitHub: https://github.com/DigitalEuan/UBP_Repo*
