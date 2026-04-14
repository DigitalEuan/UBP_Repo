# UBP Thermodynamics Study — Reproducible Archive

**Paper:** The Pantograph Projection: A Deterministic Geometric Theory of Thermodynamics Under the Universal Binary Principle  
**Author:** E. R. A. Craig, New Zealand  
**Framework:** Universal Binary Principle (UBP) v7.2 — Core Studio v4.0  
**Date:** April 2026

---

## Contents

```
ubp_thermo_study/
├── README.md                          ← This file
├── UBP_Thermodynamics_Paper.md        ← Full paper (Markdown)
├── UBP_Thermodynamics_Paper.pdf       ← Full paper (PDF, rendered)
├── UBP_Thermodynamics_Paper.tex       ← Full paper (LaTeX / Overleaf-ready)
├── ubp_thermo_audit.py                ← Main computational audit script
├── generate_figures.py                ← Figure generation script
├── ubp_thermo_results.json            ← All raw computed results
└── figures/
    ├── fig1_pantograph.png            ← Pantograph projection diagram
    ├── fig2_four_laws.png             ← Four Laws summary
    ├── fig3_phase_change.png          ← Phase transition (Lattice Snap)
    ├── fig4_nernst_iron.png           ← Nernst audit / specific heat floor
    ├── fig5_coupling.png              ← Universal coupling constant
    ├── fig6_brownian.png              ← Brownian motion as aliasing jitter
    └── fig7_survey.png                ← Multi-element thermodynamic survey
```

---

## Reproducibility Instructions

### Prerequisites

- Python 3.11+
- The UBP Core Studio v4.0 repository cloned locally

### Step 1: Clone the UBP Repository

```bash
gh repo clone DigitalEuan/UBP_Repo
```

### Step 2: Run the Computational Audit

```bash
cd ubp_thermo_study
PYTHONPATH=/path/to/UBP_Repo/core_studio_v4.0/core python3 ubp_thermo_audit.py
```

This will regenerate `ubp_thermo_results.json` with all computed values.

### Step 3: Regenerate Figures

```bash
PYTHONPATH=/path/to/UBP_Repo/core_studio_v4.0/core python3 generate_figures.py
```

This will regenerate all 7 figures in the `figures/` directory.

### Step 4: Compile the LaTeX Paper (Optional)

Upload `UBP_Thermodynamics_Paper.tex` and the `figures/` directory to [Overleaf](https://www.overleaf.com) and compile with pdflatex.

---

## Experiments Performed

| # | Experiment | Elements | Key Result |
|---|---|---|---|
| 1 | Four Laws Audit — Hydrogen | H | Phase-Lock, NRCI=0.7647 |
| 2 | Four Laws Audit — Gold | Au | Shearing, NRCI=0.6206 |
| 3 | Phase Change — Gold | Au | Lattice Snap at d=4, shear=0.0327 rads |
| 4 | Phase Change — Iron | Fe | Lattice Snap at d=4, shear=0.0327 rads |
| 5 | Nernst Audit — Iron | Fe | Cv_min = 0.534521 J/K-equiv |
| 6 | Universal Coupling Constant | H, Au | Cu = 1404.06, error < 0.0001% |
| 7 | Multi-Element Survey | 10 elements | Discrete Hamming Weight clustering |
| 8 | Carnot Analogue | Au–H engine | η = 99.22%, RG ceiling = 42.04% |
| 9 | Brownian Motion | H, Fe, Au | Jitter = W·T_base / 2π |
| 10 | Equation of State | H | V_EoS / V_Panto = 0.9151 |

---

## Key System Constants (UBP Core v7.2)

| Constant | Symbol | Value |
|---|---|---|
| Triadic Wobble | W | 0.8175802271764946 |
| 13D Sink Leakage | L | 0.0628907867058842 |
| Scale Factor | k | 1.8175802271764945 |
| Resolution Gap | RG | 0.4203715050836670 |
| Pi (50-term) | π | 3.1415926535897932 |

---

## Falsifiable Predictions

1. **Iron specific heat floor:** Cv(Fe) ≥ 0.534521 J/K-equiv at T < 1 nano-Kelvin
2. **Hydrogen specific heat floor:** Cv(H) ≥ 0.356347 J/K-equiv at T < 1 nano-Kelvin
3. **Universal Lattice Snap threshold:** Phase transitions occur at exactly d=4 Hamming bits for all elements

---

*All results are generated from the real UBP Core v7.2 engine. No placeholder or mock data was used.*
