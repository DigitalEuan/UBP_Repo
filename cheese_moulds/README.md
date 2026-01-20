# UBP Cheese Mould Study

## A Geometric Model of Mycological Metabolism in Dairy Fermentation

![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Origin](https://img.shields.io/badge/Origin-New_Zealand-white.svg)

**Author:** E. R. A. Craig, New Zealand  
**Date:** 21 January 2026

---

## Overview

This repository contains a reproducible scientific study applying the **Universal Binary Principle (UBP)** to predict the stability of flavor compounds and mycotoxins in cheese. The study demonstrates that fungal metabolites can be classified based on their geometric properties within a 24-dimensional information space defined by the Golay G₂₄ error-correcting code.

### Key Findings

- **88.9% classification accuracy** distinguishing toxins from flavors using a simple Mass Shell threshold (N ≥ 3.8)
- **Strong statistical separation** between compound classes (Cohen's d = 3.246 for Mass Shell)
- **Predictive decay model** demonstrating how high-NRCI compounds persist longer during aging


---

## Quick Start

### Prerequisites

- Python 3.9+
- pip

### Installation

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/ubp_cheese_mould_study.git
cd ubp_cheese_mould_study

# Install dependencies
pip install -r requirements.txt

# Run the main analysis
python run_analysis.py
```

### Expected Output

The script will:
1. Verify the UBP core system integrity
2. Analyze 18 cheese metabolites (10 flavors, 8 toxins)
3. Generate statistical summaries and classification results
4. Produce visualization figures in the `figures/` directory

---

## The Universal Binary Principle (UBP)

The UBP is a theoretical framework that models reality as a discrete, error-correcting computational system. Key concepts include:

### Golay Code (G₂₄)
A set of 4096 unique 24-bit codewords with a minimum Hamming distance of 8. Can correct up to 3 bit-errors. In the UBP, these represent the most stable states of existence.

### Non-Random Coherence Index (NRCI)
A metric (0.0 to 1.0) measuring the geometric stability of a 24-bit vector. Higher NRCI = greater stability and persistence.

### Mass Shell (N)
A logarithmic mass metric based on the fundamental constant Y ≈ 0.2646:

```
N = log_{1/Y}(M / M_H)
```

Where M is molecular mass and M_H is the mass of hydrogen.

---

## Methodology

### Molecular Vectorization

Each molecule is converted to a 24-bit vector by partitioning atomic counts into four 6-bit segments:

| Bits 0-5 | Bits 6-11 | Bits 12-17 | Bits 18-23 |
|----------|-----------|------------|------------|
| Carbon   | Hydrogen  | Nitrogen   | Oxygen     |

### Classification Rule

The optimal classification rule identified in this study:

```
IF Mass_Shell >= 3.8 THEN TOXIN ELSE FLAVOR
```

This achieves:
- **Accuracy:** 88.9%
- **Precision:** 87.5%
- **Recall:** 87.5%
- **F1 Score:** 0.88

---

## Results Summary

### Statistical Comparison

| Metric | Flavor (n=10) | Toxin (n=8) | Cohen's d |
|--------|---------------|-------------|-----------|
| Mass Shell (N) | 3.531 ± 0.162 | 4.229 ± 0.257 | 3.246 |
| NRCI | 0.708 ± 0.081 | 0.797 ± 0.117 | 0.880 |
| Mass (Da) | 112.8 ± 24.9 | 293.6 ± 87.6 | 2.808 |

### Compound Dataset

**Flavor Compounds:**
- 2-Heptanone, 2-Nonanone, 2-Pentanone (Blue cheese ketones)
- 1-Octen-3-ol (Mushroom note)
- Butyric Acid, Hexanoic Acid (Fatty acids)
- Diacetyl, Acetoin (Buttery notes)
- Ethyl Butyrate (Fruity)
- Methyl Cinnamate (Balsamic)

**Mycotoxins:**
- Ochratoxin A, Roquefortine C, Cyclopiazonic Acid
- Sterigmatocystin, Mycophenolic Acid
- Patulin, Citrinin, Penicillic Acid

---

## Academic Paper

The full academic paper is provided in PDF format: `85_A_Geometric_Model_of_Mycological_Metabolism_in_Dairy_Fermentation__Predicting_Flavor_and_Toxin_Stability_with_the_Universal_Binary_Principle.pdf`.

---

## Citation

If you use this work in your research, please cite:

```bibtex
@article{craig2026ubp_cheese,
  title={A Geometric Model of Mycological Metabolism in Dairy Fermentation: 
         Predicting Flavor and Toxin Stability with the Universal Binary Principle},
  author={Craig, E. R. A.},
  year={2026},
  note={New Zealand}
}
```

---

## License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## Acknowledgments

- Cheese chemistry data compiled from peer-reviewed literature
- Visualization generated with matplotlib

---

## Contact

For questions or collaboration inquiries, please open an issue in this repository.
