# Advanced Black Hole Quantum Tunneling Study (UBP v3.2)

**Author:** Euan R A Craig, New Zealand  
**Email:** info@digitaleuan.com  
**Date:** October 15, 2025

---

## Overview

This repository contains the complete computational study, data, and documentation for an advanced investigation into black hole thermodynamics and quantum tunneling, grounded in the **Universal Binary Principle (UBP) v3.2** framework.

The study demonstrates a high-precision calibration between General Relativity (GR) and the UBP, models the event horizon as a computational phenomenon, and derives a set of specific, falsifiable predictions that distinguish the UBP from other theories of quantum gravity.

For a full narrative and analysis of the results, please see the comprehensive scientific paper located at:
`docs/UBP_Black_Hole_Quantum_Tunneling_Study.md`

## Repository Structure

```
black_holes_quantum_tunnelling/
├── code/                     # All Python source code modules
│   ├── module1_classical_hawking.py
│   ├── module2_ubp_calibration.py
│   ├── module3_bh_queue_model.py
│   ├── module4_helix_mqt.py
│   ├── module5_extended_metrics.py
│   └── run_all_modules.sh      # Master script to execute the full study
├── data/                     # All generated CSV data files
│   ├── classical_hawking_dataset.csv
│   ├── ubp_calibrated_dataset.csv
│   ├── bh_queue_history.csv
│   ├── golay_parity_statistics.csv
│   ├── self_observing_helix.csv
│   ├── mqt_boost_predictions.csv
│   ├── kerr_black_holes.csv
│   └── rn_black_holes.csv
├── docs/                     # Documentation and scientific papers
│   └── UBP_Black_Hole_Quantum_Tunneling_Study.md
├── figures/                  # All generated plots and visualizations
│   ├── 01_classical_hawking_properties.png
│   ├── 02_ubp_calibration_results.png
│   ├── 03_bh_queue_dynamics.png
│   ├── 04_golay_parity_statistics.png
│   ├── 05_self_observing_helix.png
│   ├── 06_mqt_boost_predictions.png
│   ├── 07_kerr_comparison.png
│   └── 08_rn_comparison.png
└── README.md                 # This file
```

## Key Findings

1.  **Perfect GR-UBP Correspondence**: The UBP framework reproduces classical Hawking temperature with a fractional residual below **10⁻¹³** and a correlation of **R² = 1.000000000000000**.

2.  **Computational Event Horizon**: A 6D bitfield simulation models the event horizon as an information processing bottleneck where the Non-Random Coherence Index (NRCI) saturates below a critical threshold of **0.01**.

3.  **Falsifiable Predictions**:
    *   **Golay Parity Signatures**: Escaping radiation should exhibit a slight bias towards even parity (predicted: 52-58.33%).
    *   **MQT Boost**: Black hole queue amplitude should boost Macroscopic Quantum Tunneling rates by **18.4% to 69%**, providing a testable laboratory prediction.

4.  **Generalization**: The framework is successfully extended to include rotating (Kerr) and charged (Reissner-Nordström) black holes, correctly predicting the suppression of Hawking radiation due to spin and charge.

## How to Run the Study

### Prerequisites

-   Python 3.11+
-   Required libraries: `numpy`, `pandas`, `matplotlib`, `scipy`

You can install the dependencies using pip:
```bash
pip install numpy pandas matplotlib scipy
```

### Execution

To run the entire analysis from start to finish, execute the master script from the project root directory:

```bash
cd /path/to/black_holes_quantum_tunnelling
./code/run_all_modules.sh
```

This script will execute all five modules sequentially, regenerate all data files in the `data/` directory, and save all figures to the `figures/` directory. The full run takes approximately 2-3 minutes on a standard machine.

Alternatively, you can run each module individually:

```bash
python3.11 code/module1_classical_hawking.py
python3.11 code/module2_ubp_calibration.py
# ... and so on
```

---

This study was generated with the assistance of Manus AI, an autonomous AI agent.

