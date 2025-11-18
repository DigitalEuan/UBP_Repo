# UBP Symbol Study - Phase 2 Reproducibility Package

This package contains all the code, data, and results for Phase 2 of the UBP Symbol Study.

## Contents

- `data/`: Contains the raw, encoded, and processed symbol datasets.
- `scripts/`: Contains all Python scripts for data generation, encoding, coherence computation, analysis, and modeling.
- `results/`: Contains all generated visualizations and JSON results files.
- `ubp_3.5/`: Contains the core UBP 3.5 coherence substrate.
- `final_report_phase2.md`: The complete final report for this phase.
- `theoretical_framework.md`: The theoretical framework document.

## How to Reproduce

1.  **Environment**: The scripts are designed to run in a standard Python 3.11 environment. You will need to install `numpy`, `scikit-learn`, and `matplotlib`.
2.  **Execution Order**: The scripts should be run in the following order:
    1.  `scripts/generate_final_dataset.py`: Generates the 1006-symbol dataset.
    2.  `scripts/symbol_encoding.py`: Encodes the dataset.
    3.  `scripts/symbol_coherence_model.py`: Computes coherence features.
    4.  `scripts/bitfield_analysis.py`: Performs bitfield analysis.
    5.  `scripts/predictive_models.py`: Trains and validates predictive models.
    6.  `scripts/novel_symbol_generator.py`: Generates and tests novel symbols.

All output files will be saved to the `data/` and `results/` directories.
