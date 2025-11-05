# UBP Comprehensive Ceramic and Composite Materials Study

**Author:** Euan R A Craig  
**Date:** November 4, 2025  
**Version:** 1.0  
**Framework:** Universal Binary Principle (UBP) v3.3

---

## Overview

This repository contains a comprehensive computational study of advanced materials using the Universal Binary Principle (UBP) framework. The investigation expands upon initial concrete research to encompass a broad spectrum of ceramics, composites, and geopolymers. Over 350 simulations were performed, including massive-scale screening, detailed dosage-response analysis, and focused refinement of top-performing materials.

## Project Structure

```
ubp_study/
├── README_FINAL.md                          # This file
├── final_report.md                          # Comprehensive study report
├── ubp_ceramic_study.py                     # Main UBP analysis script
├── materials_database_expanded.csv          # Full database of 160+ materials
├── ubp_ceramic_study_full_results.csv       # Results from massive-scale simulation
├── ubp_dosage_response_results.csv          # Results from dosage-response analysis
├── plot1_strength_distribution.png          # Visualization: Strength by category
├── plot2_nrci_vs_toughness.png              # Visualization: NRCI vs. toughness
├── plot3_success_vs_failure.png             # Visualization: Success vs. failure
├── plot4_dosage_response_curves.png         # Visualization: Dosage curves
├── plot5_correlation_heatmap.png            # Visualization: Correlation matrix
└── plot6_category_distribution.png          # Visualization: Category distribution
```

## Key Files

### Data Files

- **materials_database_expanded.csv**: Input database containing 160+ material definitions with composition, processing parameters, and notes.
- **ubp_ceramic_study_full_results.csv**: Complete simulation results for all 160+ materials, including UBP metrics and simulated mechanical properties.
- **ubp_dosage_response_results.csv**: Detailed dosage-response data for 10 additive-matrix systems (200 simulations).

### Scripts

- **ubp_ceramic_study.py**: Main Python script for running UBP simulations. Interfaces with UBP v3.3 modules to analyze material properties.

### Visualizations

Six key plots are provided to illustrate the findings:
1. **plot1_strength_distribution.png**: Violin plot of compressive strength distribution by material category.
2. **plot2_nrci_vs_toughness.png**: Scatter plot showing the relationship between NRCI and fracture toughness.
3. **plot3_success_vs_failure.png**: Box plot comparing success cases vs. intentional failure cases.
4. **plot4_dosage_response_curves.png**: Multi-panel plot of dosage-response curves for 10 systems.
5. **plot5_correlation_heatmap.png**: Correlation matrix of UBP metrics and material properties.
6. **plot6_category_distribution.png**: Pie chart of material category distribution.

### Report

- **final_report.md**: Comprehensive markdown report detailing the study objectives, methodology, results, and conclusions.

## How to Use

### Prerequisites

- Python 3.11+
- Required packages: `pandas`, `numpy`, `matplotlib`, `seaborn`, `scikit-learn`
- UBP v3.3 framework (available at [https://github.com/DigitalEuan/UBP_Repo/tree/main/ubp_3.3](https://github.com/DigitalEuan/UBP_Repo/tree/main/ubp_3.3))

### Running the Simulation

1. Clone the UBP_Repo and ensure the `ubp_3.3` directory is accessible.
2. Place the `materials_database_expanded.csv` file in the working directory.
3. Run the main simulation script:

```bash
python3.11 ubp_ceramic_study.py
```

4. The script will generate `ubp_ceramic_study_full_results.csv` with the simulation results.

### Analyzing the Results

The provided CSV files can be opened in any spreadsheet software or analyzed further using Python/R. The visualizations provide a quick overview of the key findings.

## Key Findings

- **Top Performers**: C-Fiber/SiC-Matrix composites and WC-Co cermets exhibited the highest simulated performance.
- **Coherence Matters**: A strong positive correlation was observed between NRCI (coherence) and mechanical properties.
- **Optimal Dosages**: Dosage-response curves revealed non-linear effects, with optimal concentrations typically at intermediate levels.
- **Failure Analysis**: Intentional failure cases showed significantly lower performance, validating the UBP model.

## Reproducibility

All data, scripts, and visualizations are provided to ensure full reproducibility. The methodology is detailed in the final report, and the UBP framework is open-source and available on GitHub.

## Contact

**Euan R A Craig**  
Email: info@digitaleuan.com  
GitHub: [https://github.com/DigitalEuan](https://github.com/DigitalEuan)  
Academia: [https://independent.academia.edu/EuanCraig2](https://independent.academia.edu/EuanCraig2)  
X: [https://x.com/DigitalEuan](https://x.com/DigitalEuan)

---

**License:** This work is provided for research and educational purposes. Please cite appropriately if used in publications.
