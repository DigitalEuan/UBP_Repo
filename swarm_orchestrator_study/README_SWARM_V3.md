# UBP Swarm Orchestrator V3 — Reproducible Research Bundle

**Study:** Multi-Agent Swarm Scaling for UBP Document Synthesis  
**Date:** 20 April 2026  
**System:** UBP Core Studio v4.0 (core_studio_v4.0)  
**Author:** Manus AI (on behalf of DigitalEuan)  
**Repo:** [DigitalEuan/UBP_Repo](https://github.com/DigitalEuan/UBP_Repo)

---

## Overview

This bundle contains the complete research package for the UBP Swarm Orchestrator scaling study. Starting from the original `ubp_swarm_orchestrator.py` concept, three progressively more powerful versions were developed and 8 experiments were executed across 6 different topic domains, deploying between 13 and 51 agents per run.

The study investigates:
1. How agent count affects document size (word count)
2. Whether the NRCI geometric stability metric scales with agent count
3. Whether the Writer-Critic iterative feedback loop improves acceptance rates
4. How different topic domains affect resonance scoring behaviour
5. What the fundamental bottlenecks and limitations of the UBP MoE text engine are

---

## File Structure

```
ubp_swarm_v2/
├── core.py                          # UBP Core v5.7 (Golay + Leech engines)
├── ubp_moe_cortex_v2.py             # MoE Cortex v2 (n-gram manifold + Golay scoring)
├── ubp_semantic_engine.py           # Semantic Engine (KB query + cosine resonance)
│
├── ubp_swarm_orchestrator_v1.py     # V1: Original concept (3-5 agents, no feedback)
├── ubp_swarm_orchestrator_v2.py     # V2: Dual-gate + basic feedback (10 agents)
├── ubp_swarm_orchestrator_v3.py     # V3: Five-tier swarm (13-51 agents, full feedback)
│
├── run_experiments_fast.py          # Batch runner for all 8 experiments
├── experiments_v3.json              # Experiment configuration file
├── analyze_results.py               # Analysis + chart generation script
│
├── results_v3/                      # All experiment outputs
│   ├── exp01_thermodynamics_v1_baseline.{json,md}
│   ├── exp02_thermodynamics_v2_dual_gate.{json,md}
│   ├── exp03_thermodynamics_v3_large.{json,md}
│   ├── exp04_quantum_coherence.{json,md}
│   ├── exp05_chemical_bonding.{json,md}
│   ├── exp06_particle_physics.{json,md}
│   ├── exp07_large_swarm_30agents.{json,md}
│   ├── exp08_information_geometry.{json,md}
│   └── experiment_summary.json
│
└── analysis_v3/                     # Analysis outputs
    ├── agent_scaling.png
    ├── nrci_trajectories.png
    ├── resonance_distribution.png
    ├── retry_analysis.png
    └── analysis_report.md
```

---

## How to Reproduce

### Prerequisites

The following files from `core_studio_v4.0` must be present in the same directory:

```
core.py                   # From: core_studio_v4.0/core/core.py
ubp_moe_cortex_v2.py      # From: core_studio_v4.0/core/ubp_moe_cortex_v2.py
ubp_semantic_engine.py    # From: core_studio_v4.0/core/ubp_semantic_engine.py
ubp_system_kb.json        # From: core_studio_v4.0/system_kb/ubp_system_kb.json
ubp_language_kb.json      # From: core_studio_v4.0/system_kb/ubp_language_kb.json
```

Python dependencies:
```bash
pip3 install numpy
```

### Run All 8 Experiments

```bash
cd ubp_swarm_v2/
python3 run_experiments_fast.py
```

Expected runtime: ~45-60 minutes (sequential, CPU-bound).

### Run a Single Experiment

```python
from ubp_swarm_orchestrator_v3 import UBPSwarmOrchestratorV3

orch = UBPSwarmOrchestratorV3(
    directive="Your topic here",
    num_sections=4,
    paragraphs_per_section=3,
    min_nrci=0.65,
    min_resonance=0.3,
    max_retries=5,
    words_per_paragraph=22,
    seed=42
)
result = orch.run()
```

### Reproduce Analysis Charts

```bash
python3 analyze_results.py
```

---

## Experiment Summary

| # | Name | Agents | Sections | Paras | Words | Macro NRCI | Time(s) |
|---|------|--------|----------|-------|-------|------------|---------|
| E1 | Thermodynamics v1 baseline | 13 | 2 | 4 | 35 | 0.7623 | 66 |
| E2 | Thermodynamics v2 dual-gate | 25 | 3 | 9 | 62 | 0.6814 | 151 |
| E3 | Thermodynamics v3 large | 41 | 4 | 16 | 121 | 0.6814 | 298 |
| E4 | Quantum coherence | 33 | 3 | 12 | 97 | 0.6814 | 287 |
| E5 | Chemical bonding | 33 | 3 | 12 | 101 | 0.6814 | 410 |
| E6 | Particle physics | 33 | 3 | 12 | 100 | 0.6814 | 325 |
| E7 | Large swarm (51 agents) | 51 | 5 | 20 | 132 | 0.6814 | 353 |
| E8 | Information geometry | 41 | 4 | 16 | 94 | 0.6814 | 332 |

---

## Architecture: Five-Tier Swarm (V3)

```
TIER 0: DIRECTOR (1 agent)
  └─ Creates master outline (sections × topics)
  
TIER 1: SECTION ARCHITECTS (N agents, one per section)
  └─ Refines each section plan using KB semantic queries
  
TIER 2: WRITERS (N×M agents, one per paragraph)
  └─ Drafts paragraph text via MoE research() call
  └─ Accepts feedback tokens from Critic on retry
  
TIER 3: CRITICS (N×M agents, paired with each Writer)
  └─ Dual-gate: NRCI ≥ threshold AND TopicResonance ≥ threshold
  └─ On REJECT: generates feedback tokens for Writer retry
  └─ Updates Macro NRCI (document-level geometric stability)
  
TIER 4: EDITORS (N agents, one per section)
  └─ Synthesizes section header + paragraph assembly
  └─ Computes section-level statistics
```

**Total agents per run** = 1 + S + (S × P) + (S × P) + S  
where S = sections, P = paragraphs per section.

For E7 (5 sections × 4 paragraphs): 1 + 5 + 20 + 20 + 5 = **51 agents**

---

## Key Findings

### 1. Agent Scaling → Document Size (Linear)

Agent count scales linearly with document size. Each additional Writer agent produces ~6-7 words. The relationship is deterministic: more agents = more paragraphs = more words. There is no emergent quality improvement from adding agents alone.

### 2. NRCI Attractor Collapse

The Macro NRCI does not improve with more agents. After the first few paragraphs, it converges to one of three Golay attractor values: **0.6160, 0.6814, or 0.7623**. This is a fundamental property of the Golay code's discrete structure — the XOR of any two valid codewords is itself a valid codeword, so the macro vector always lands on a codeword with one of these NRCI values.

**Implication:** The NRCI gate is a necessary but insufficient quality criterion. It cannot distinguish between a coherent document and a random one, because all valid Golay codewords pass the threshold.

### 3. Critic Feedback Loop Works

The Writer-Critic feedback loop demonstrably triggers retries. Across all experiments, 15% of paragraphs required 2 attempts and 3% required 3 attempts. The feedback tokens (e.g., `STABLE THE`, `RELEVANT`) appended to the Writer's objective do modify the MoE's KB probe selection, producing different text on retry.

### 4. Topic Drift is Structural

All directives, regardless of topic domain, produce similar text fragments because the KB anchor selection is dominated by high-weight entries (e.g., `LAW_HYBRID_STEREOSCOPY_002` with w=8.0 always wins for "the law" queries). This is not a bug in the swarm — it is a property of the KB weighting system.

### 5. Binary Resonance Distribution

The 24-bit Golay cosine similarity produces near-binary scores (0.0 or 1.0) rather than a continuous distribution. This is because the Golay code's discrete geometry means two vectors are either orthogonal or identical in the relevant subspace.

---

## Recommended Next Steps (V4)

1. **Parallel Writer agents** — Use `multiprocessing.Pool` to run all Writers in a section simultaneously. Expected speedup: N× (where N = paragraphs per section).

2. **Cached manifold** — Pre-compute and pickle the n-gram manifold once, load it for all experiments. Expected speedup: 10-50×.

3. **KB diversity sampling** — Implement a `used_anchors` set to prevent the same KB entry from dominating multiple paragraphs. This is the most impactful change for document coherence.

4. **Continuous resonance scoring** — Replace binary Golay cosine with Leech lattice float-vector cosine for smoother quality gradients.

5. **Grammar completion agent (Tier 5)** — Post-process each accepted paragraph to complete it to a grammatically valid sentence using the KB entry's full definition text.

6. **Cross-document NRCI** — Instead of XOR-accumulating all paragraphs into a single macro vector, track a rolling window NRCI to detect local geometric drift.

---

## Version History

| Version | Agents | Key Innovation |
|---------|--------|----------------|
| V1 (original) | 3-5 | Single-tier, NRCI gate only |
| V2 | 10 | Dual-gate (NRCI + Resonance), basic feedback |
| V3 | 13-51 | Five-tier hierarchy, iterative Writer-Critic loop, shared cortex |
| V4 (planned) | 50-200+ | Parallel Writers, cached manifold, KB diversity, grammar completion |

---

*Generated by Manus AI — UBP Swarm Orchestrator Study, April 2026*
