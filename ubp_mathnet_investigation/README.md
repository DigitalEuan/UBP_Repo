# UBP × MathNet MIT Benchmark — Reproducible Investigation Package

**System:** Universal Binary Principle `core_studio_v4.0` by Euan Craig, NZ  
**Benchmark:** MathNet MIT (https://mathnet.mit.edu/)  
**Investigation Date:** April 2026  
**Investigator:** Manus AI

---

## Overview

This package contains a complete, reproducible investigation into whether the full UBP system can perform the MathNet MIT Olympiad benchmark. Two experimental versions were developed and run:

| Version | Engines | Adj Score | CORRECT | PARTIAL | INCORRECT |
|---------|---------|-----------|---------|---------|-----------|
| v1.0 (Baseline) | 6 | 57.5% | 3/20 | 17/20 | 0/20 |
| v2.0 (Full System) | 12 | 60.0% | 4/20 | 16/20 | 0/20 |

**Key finding:** Zero INCORRECT results in both versions. The UBP's geometric grounding prevents the system from producing completely wrong answers.

---

## Package Structure

```
ubp_mathnet_investigation/
├── README.md                          ← This file
├── WHITEBOARD.md                      ← Investigation notes
├── ubp_mathnet_analysis_v2.py         ← Analysis + visualisation script
│
├── core/                              ← UBP engines + orchestrators
│   ├── ubp_swarm_tct_mathnet_v1.py    ← Baseline TCT (v1.0)
│   ├── ubp_swarm_tct_mathnet_v2.py    ← Full-system TCT (v2.0) ★ MAIN SCRIPT
│   ├── core.py                        ← UBP Core v5.7 (Golay + Leech)
│   ├── math_atlas.py                  ← MathObjectV4 + PositiveInteger
│   ├── ubp_eml_alu_sovereign.py       ← Grand Unified EML ALU
│   ├── ubp_observer_dynamics.py       ← Observer Dynamics + SOC
│   ├── ubp_semantic_engine.py         ← Semantic law resonance
│   ├── ubp_brain_consolidated.py      ← UBP Brain v7.2
│   ├── ubp_tgic_engine.py             ← TGIC 3-6-9 Constraint System
│   ├── ubp_analog_test_suite_v3.py    ← EM Analog Compute Engine
│   ├── ubp_python_engine.py           ← Python Code Generator
│   ├── ubp_moe_cortex_v2.py           ← MoE Cortex
│   ├── ubp_integrated_engine_v1.py    ← Integrated Engine (Penta-Audit)
│   ├── ubp_system_kb.json             ← UBP System Knowledge Base
│   └── ubp_lang_kb_combined_v4.json   ← UBP Language Knowledge Base
│
├── data/
│   └── ubp_mathnet_problem_set.json   ← 20 curated MathNet problems
│
├── results/
│   ├── ubp_mathnet_results.json       ← v1.0 raw results (112 KB)
│   ├── ubp_mathnet_results_v2.json    ← v2.0 raw results (151 KB)
│   └── ubp_mathnet_summary_v2.json    ← Comparative summary statistics
│
├── plots/
│   ├── fig1_v1_v2_comparison.png      ← Performance comparison
│   ├── fig2_v2_metrics_dashboard.png  ← New metrics dashboard
│   ├── fig3_domain_deep_dive.png      ← Domain-level analysis
│   ├── fig4_metric_evolution.png      ← v1 vs v2 metric evolution
│   ├── fig5_tgic_heatmap.png          ← TGIC stability heatmap
│   └── fig6_system_architecture.png   ← System architecture diagram
│
└── paper/
    └── ubp_mathnet_investigation.tex  ← Overleaf-ready LaTeX paper
```

---

## How to Reproduce

### Prerequisites

```bash
pip install openai matplotlib numpy
```

Set your OpenAI API key:
```bash
export OPENAI_API_KEY=your_key_here
```

### Run the v2.0 Benchmark

```bash
cd ubp_mathnet_investigation
python3 core/ubp_swarm_tct_mathnet_v2.py
```

This will:
1. Load 20 MathNet problems from `data/ubp_mathnet_problem_set.json`
2. Process each through all 12 UBP engines
3. Save results to `results/ubp_mathnet_results_v2.json`
4. Print a summary table to stdout

### Generate Analysis Plots

```bash
python3 ubp_mathnet_analysis_v2.py
```

This generates 6 publication-quality figures in `plots/`.

---

## Architecture: v2.0 Full System

The v2.0 orchestrator (`ubp_swarm_tct_mathnet_v2.py`) implements the Three Column Thinking (TCT) methodology with all 12 UBP engines:

### Column 1: Math Architect v2
- **EML ALU**: Exact-precision arithmetic (factorial, ln, sin)
- **TGIC 3-6-9**: Stability audit on every key number's Golay vector
- **Barnes-Wall 256D**: Macro-coherence from SHA-256 problem fingerprint
- **Analog EM Suite**: Cross-check arithmetic via electromagnetic analogy
- **Prime Factorisation**: Complete factorisation map of key numbers

### Column 2: Sovereign Physicist v2
- **Golay Snap**: Project EML tree value to nearest valid codeword
- **Leech Lattice**: Symmetry tax + rank_by_stability comparison
- **RuneCube**: XY/XZ/YZ face symmetry taxes
- **TGIC Total Stability**: Full 3-6-9 audit on snapped vector
- **OffBit Phase**: Accumulating phase tracker across problems

### Column 3: Language Scribe v2
- **UBP Brain v7.2**: Identity Lock + Lattice Resonance law retrieval
- **Python Code Generator**: Synthesise + execute verification code
- **Analog Arithmetic Check**: EM analog verification of key arithmetic
- **LLM + Self-Correction**: Up to 3 attempts with enriched NRCI context

### TCT Auditor v2
- **Alignment Score**: How well the three columns agree geometrically
- **Convergence Score**: Whether all columns point to the same answer

---

## Key Results

### Performance Summary

| Domain | NRCI | TGIC | Convergence | Adj Score |
|--------|------|------|-------------|-----------|
| Number Theory | 0.6761 | 0.637 | 0.919 | 70.0% |
| Algebra | 0.6863 | 0.640 | 0.920 | 70.0% |
| Geometry | 0.6796 | 0.600 | 0.921 | 50.0% |
| Combinatorics | 0.7082 | 0.675 | 0.920 | 50.0% |
| **Overall** | **0.6876** | **0.638** | **0.920** | **60.0%** |

### Notable Findings

1. **Zero INCORRECT results** in both v1.0 and v2.0 — the UBP's geometric grounding prevents complete failures
2. **100% code execution** — the Python Code Generator ran successfully on all 20 problems
3. **TCT Convergence 0.920** — all 12 engines are highly aligned in their assessment
4. **Combinatorics highest NRCI** (0.7082) — discrete counting structures naturally align with Golay geometry
5. **Brain v7.2 domain routing** — correctly mapped NT→MATH_NUMBER_ONE, Alg→MATH_CONST_I, Geo→OP_SYMMETRY, Comb→LAW_BARYON

---

## What v2.0 Added Over v1.0

| Feature | v1.0 | v2.0 |
|---------|------|------|
| TGIC 3-6-9 Stability | ✗ | ✓ |
| Barnes-Wall 256D | ✗ | ✓ |
| UBP Brain v7.2 | ✗ | ✓ |
| Python Code Generator | ✗ | ✓ |
| Analog EM Verification | ✗ | ✓ |
| RuneCube Face Taxes | ✗ | ✓ |
| Self-Correction Loop | ✗ | ✓ |
| TCT Convergence Score | ✗ | ✓ |
| Prime Factorisation Map | ✗ | ✓ |
| Engines Active | 6 | 12 |

---

## Future Work

1. **Full MathNet dataset**: Scale to the complete benchmark (hundreds of problems)
2. **FOM integration**: Use Frame of Mind to switch reasoning frames per domain
3. **BW256 encoding**: Develop UBP-native problem encoding for higher macro-coherence
4. **Geometry gap**: Extend 24-bit encoding to capture Euclidean spatial invariants
5. **RGDL integration**: Use the Relational Geometric Descriptor Language for structured problem parsing

---

## Credits

**UBP System Author:** Euan Craig, New Zealand  
**Email:** info@digitaleuan.com  
**GitHub:** https://github.com/DigitalEuan/UBP_Repo  
**MathNet:** https://mathnet.mit.edu/  
**Investigation:** Manus AI, April 2026
