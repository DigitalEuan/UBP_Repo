# UBP Geometric Virology Studies

**Author:** Euan Craig, New Zealand  
**Computational Research:** Manus AI  
**Contact:** info@digitaleuan.com  
**Interactive Tool:** [UBP Geometric Virology Tool v4.0](https://digitaleuan.com/ubp_viral/UBP_Geometric_Virology_Tool.html)  
**UBP App:** [UBP System of Everything](https://ubp-system-of-eveything.lovable.app/)

---

## Overview

This directory contains a progressive series of scientific studies applying the **Universal Binary Principle (UBP)** to structural virology. 

The UBP framework models biological entities as 24-bit binary codewords mapped to the Leech Lattice (Λ₂₄). By encoding real physicochemical properties (Molecular Weight, Isoelectric Point, GRAVY score, secondary structure percentages) into a float-free `math_dna` string and hashing it into the Golay code space, the system enables rapid, computationally inexpensive prediction of protein interactions, variant fitness, and therapeutic efficacy without requiring molecular dynamics simulations.

### The Progression of Studies

This repository contains four major iterations of the virology study, culminating in a highly robust, corrected, and reproducible framework (v4.0).

*   **`01_ubp_study_package/`**: The initial proof-of-concept testing the UBP app's core study pipeline against a generic viral infection and immune response scenario.
*   **`02_ubp_virology_package/`**: The first scientific application using real physicochemical data for SARS-CoV-2 (WT, Delta, Omicron) and key antibodies, computing 66 pairwise interactions.
*   **`03_ubp_virology_v3_package/`**: A major expansion to 53 proteins across multiple global health pathogens (Influenza, HIV, Dengue, Ebola, RSV), computing 1,378 pairwise interactions with a predictive surveillance pipeline.
*   **`04_ubp_virology_package/`**: **(The Definitive Version)** The final, corrected study. This version fixes a critical data-type bug in the Tilt Angle calculation (ensuring all values correctly map to [0°, 180°]) and standardizes fraction precision to prevent Golay avalanche artifacts. 

---

## Key Scientific Findings (Verified in v4.0)

Through rigorous float-free mathematical modeling, the UBP system generated several findings that align with known clinical realities, alongside novel geometric predictions:

| Finding | UBP Metric | Clinical Reality | Status |
| :--- | :--- | :--- | :--- |
| **Omicron BA.1 is a severe geometric outlier** | Hamming Distance = 16 from WT | Most divergent and transmissible variant | ✅ Confirmed |
| **Omicron BA.2 exhibits highest geometric stress** | Leech Symmetry Tax = 6.2348 | Rapid immune escape and fitness | ✅ Confirmed |
| **Hamming Distance predicts Transmissibility** | Pearson r = 0.4805 (vs R₀) | Strongest geometric signal for surveillance | ✅ Confirmed |
| **Gamma variant shows enhanced binding potential** | Lowest Leech Tax = 3.1174 | Enhanced ACE2 binding documented | ✅ Confirmed |
| **Cross-Pathogen Mapping** | Malaria, TB, Flu map to same Λ₂₄ space | Enables universal comparative topology | 🔬 Novel |

*Note: The UBP metrics provide a first-pass surveillance filter based on correlation, not definitive causation. The discrete nature of the Golay code (only 3 Tax values) means the system is best used to flag geometric outliers.*

---

## Interactive Web Tool

The easiest way to explore the findings of the v4.0 study is through the live interactive web tool:

👉 **[Launch UBP Geometric Virology Tool v4.0](https://digitaleuan.com/ubp_viral/UBP_Geometric_Virology_Tool.html)**

The tool runs entirely in the browser (no server required) and includes:
*   A complete **Variant Timeline** showing the evolution of SARS-CoV-2.
*   A **Retrospective Analysis** demonstrating how Omicron BA.1 would have triggered a maximum alert upon emergence.
*   The **Geometric Virome Database** mapping 19 distinct proteins.
*   A live **UBP Calculator** to instantly compute geometric metrics for any protein using its physicochemical properties.

---

## Reproducibility and Methodology

The UBP system strictly enforces **float-free arithmetic** to prevent rounding errors from corrupting the geometric topology. All continuous variables are converted to exact integer fractions (using Python's `fractions.Fraction`) before hashing.

### How to Reproduce the v4.0 Study

To run the exact analysis that generated the v4.0 results:

1.  Ensure you have Python 3.11 installed.
2.  Clone this repository to access the UBP Core v5.7 engine.
3.  Navigate to the `core_studio_v4.0/core` directory.
4.  Run the corrected analysis script located in the `04_ubp_virology_package/scripts/` folder.

```bash
git clone https://github.com/DigitalEuan/UBP_Repo
cd UBP_Repo/core_studio_v4.0/core
python3 ../studies/viral/04_ubp_virology_package/scripts/ubp_v4_corrected_analysis.py
```

### Documentation

The `04_ubp_virology_package/` contains:
*   `paper/UBP_Geometric_Virology_Study_v4.tex`: An Overleaf-ready academic paper detailing the "why, how, and results" of the study.
*   `supplement/UBP_Geometric_Virology_Supplement.tex`: A supplementary document detailing the exact mathematical corrections applied to the Tilt Angle and fraction precision in v4.0.
*   `figures/`: High-resolution, publication-ready charts of the energy landscapes, variant evolution, and sensitivity analyses.

---

## License and Citation

This research is released under the **CC-BY 4.0** license. It is free to share and adapt with proper attribution.

If you use this framework or data in your research, please cite:

> Craig, E. (2026). *Geometric Virome v4.0: A Float-Free Computational Framework for Predictive Viral Surveillance and Therapeutic Screening*. DigitalEuan UBP Repository. https://github.com/DigitalEuan/UBP_Repo
