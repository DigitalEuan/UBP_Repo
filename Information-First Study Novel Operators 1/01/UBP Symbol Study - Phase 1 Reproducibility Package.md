# UBP Symbol Study - Phase 1 Reproducibility Package

## Overview

This package contains the complete implementation and results of the UBP Symbol Study Phase 1, an information-first analysis of 200 mathematical symbols using the Universal Binary Principal (UBP) 3.5 framework.

## Directory Structure

```
ubp_symbol_study_phase1/
├── data/                              # All datasets
│   ├── symbols_dataset.json           # Raw symbol dataset (200 symbols)
│   ├── symbols_encoded.json           # Encoded symbols (3-layer encoding)
│   ├── symbols_processed.json         # Processed symbols with coherence features
│   └── calibration_config.json        # Calibrated refinement/degradation scales
├── scripts/                           # All analysis scripts
│   ├── generate_symbol_dataset.py     # Dataset generation
│   ├── symbol_encoding.py             # Three-layer encoding implementation
│   ├── symbol_coherence_model.py      # UBP coherence computation
│   ├── calibrate_scales.py            # Scale calibration
│   ├── statistical_analysis.py        # Comprehensive statistical analysis
│   └── create_visualizations.py       # Visualization generation
├── results/                           # All results and visualizations
│   ├── statistical_analysis_results.json  # Complete analysis results
│   ├── nrci_distribution.png          # NRCI distribution by category
│   ├── pca_projection.png             # PCA projection (2D)
│   ├── tsne_embedding.png             # t-SNE embedding (2D)
│   ├── clustering_metrics.png         # K-Means clustering metrics
│   ├── hierarchical_dendrogram.png    # Hierarchical clustering dendrogram
│   ├── category_distance_heatmap.png  # Inter-category distance matrix
│   └── feature_importance.png         # PCA feature importance
├── ubp_3.5/                           # UBP 3.5 framework
│   └── coherence_substrate_v2.py      # UBP 3.5 coherence substrate (dependency-free)
├── final_report.md                    # Final report
└── README.md                          # This file
```

## Reproduction Instructions

### Prerequisites

- Python 3.11+
- Required packages: numpy, matplotlib, scipy, scikit-learn

### Step-by-Step Reproduction

1. **Generate Dataset**
   ```bash
   python3.11 scripts/generate_symbol_dataset.py
   ```
   Output: `data/symbols_dataset.json` (200 symbols)

2. **Encode Symbols**
   ```bash
   python3.11 scripts/symbol_encoding.py
   ```
   Output: `data/symbols_encoded.json` (three-layer encoding)

3. **Calibrate Scales** (optional, already done)
   ```bash
   python3.11 scripts/calibrate_scales.py
   ```
   Output: `data/calibration_config.json`

4. **Compute Coherence Features**
   ```bash
   python3.11 scripts/symbol_coherence_model.py
   ```
   Output: `data/symbols_processed.json` (coherence features)

5. **Run Statistical Analysis**
   ```bash
   python3.11 scripts/statistical_analysis.py
   ```
   Output: `results/statistical_analysis_results.json`

6. **Generate Visualizations**
   ```bash
   python3.11 scripts/create_visualizations.py
   ```
   Output: All PNG files in `results/`

## Key Results

### Dataset Statistics
- **Total symbols**: 200
- **Categories**: 9 (algebra, arithmetic, calculus, information, logic, miscellaneous, probability, quantum, set_theory)
- **Largest category**: algebra (45 symbols)
- **Smallest category**: information (6 symbols)

### Encoding Statistics
- **Unicode seed range**: [0.000030, 0.107820]
- **Bitfield magnitude range**: [1.99, 5.10]
- **Initial NRCI**: 0.999997 (all symbols start at target NRCI)

### Coherence Statistics
- **NRCI range**: [0.9807, 0.9999]
- **NRCI std**: 0.00218
- **Refinement score range**: [0.10, 2.10]
- **Degradation score range**: [342.6, 877.1]
- **Net refinements range**: [0, 2]

### Statistical Findings
- **ANOVA**: F = 2.26, p = 0.025 (significant category separation)
- **Kruskal-Wallis**: H = 26.77, p = 0.0008 (highly significant)
- **Optimal clustering**: k = 9 clusters, silhouette = 0.89 (excellent)
- **PCA**: First PC explains 99.98% of variance
- **Significant pairwise difference**: algebra vs arithmetic (t = 3.46, p = 0.0009)

## Methodology Summary

### Three-Layer Encoding

1. **Layer 1: Unicode Seed**
   - Deterministic seed from Unicode codepoint
   - Normalized to [0, 1] range

2. **Layer 2: Property Bitfield (8D)**
   - D1: Arity (nullary=0, unary=1, binary=2, ternary=3)
   - D2: Formal Role (operand=0, operator=1, relation=2, quantifier=3)
   - D3: Invertibility (none=0, partial=1, full=2)
   - D4: Commutativity (no=0, partial=1, yes=2)
   - D5: Meaning Count (log scale)
   - D6: Dependency Depth (compositional complexity)
   - D7: Closure Degree (low=0, medium=1, high=2)
   - D8: Overloading Index (log scale)

3. **Layer 3: CoherenceState Initialization**
   - Combined value from unicode seed and bitfield magnitude
   - Initialized with UBP 3.5 CoherenceState

### UBP Coherence Model

- **Refinement operations**: Based on closure, invertibility, commutativity
- **Degradation operations**: Based on ambiguity, complexity, overloading
- **Calibrated scales**: refinement_scale = 1.0, degradation_scale = 500.0

## Citation

If you use this work, please cite:

```
UBP Symbol Study: An Information-First Analysis of Mathematical Symbols
Manus AI, 2025
https://github.com/DigitalEuan/UBP_Repo
```

## License

This work is part of the UBP research project. All rights reserved.

## Contact

For questions or issues, please refer to the UBP repository: https://github.com/DigitalEuan/UBP_Repo
