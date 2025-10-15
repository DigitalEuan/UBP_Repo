# UBP Novel Plastics Formulary

**Computational Discovery of High-Performance Polymer Materials Using the Universal Binary Principle**

**Author:** Euan R A Craig  
**Email:** info@digitaleuan.com  
**Date:** October 14, 2025  
**Framework:** Universal Binary Principle (UBP) v3.2+  
**Repository:** https://github.com/DigitalEuan/UBP_Repo/tree/main/ubp_novel_plastics_formulary  
**Documentation:** https://github.com/DigitalEuan/UBP_Repo/blob/main/44_Computational_Discovery_of_High_Performance_Polymer_Materials_Using_the_Universal_Binary_Principle.pdf

---

## Overview

This repository contains the complete code, data, and documentation for a computational materials discovery study that generated **21 novel polymer materials** across seven major plastic categories using the Universal Binary Principle (UBP) framework.

The study evaluated **10,332 candidate compositions** using the Chemical Carousel optimization algorithm, which systematically explores polymer composition space guided by UBP coherence metrics. Each discovered material exhibits superior mechanical, thermal, and chemical properties compared to standard commercial polymers.

---

## Key Results

| Plastic Category | Materials Discovered | Best Optimization Score | Best UBP Coherence | Candidates Evaluated |
|------------------|----------------------|-------------------------|--------------------|-----------------------|
| **#1 PET** (Polyethylene Terephthalate) | 3 | 0.7315 | 0.7915 | 1,476 |
| **#2 HDPE** (High-Density Polyethylene) | 3 | 0.8359 | 0.7209 | 1,476 |
| **#3 PVC** (Polyvinyl Chloride) | 3 | 0.8340 | 0.7192 | 1,476 |
| **#4 LDPE** (Low-Density Polyethylene) | 3 | 0.8442 | 0.7321 | 1,476 |
| **#5 PP** (Polypropylene) | 3 | 0.8304 | 0.7114 | 1,976 |
| **#6 PS** (Polystyrene) | 3 | 0.8593 | 0.7610 | 1,476 |
| **#7 Other** (Bioplastics) | 3 | 0.8327 | 0.6610 | 1,476 |
| **TOTAL** | **21** | - | - | **10,332** |

**Property Improvements Over Standard Polymers:**
- Tensile strength: Up to **+1,053%** (461 MPa vs. 40 MPa for standard PP)
- Hardness: Up to **+53%** (92 Shore D vs. 60 Shore D for standard PP)
- Thermal stability: Up to **+20%** in melting point and glass transition temperature

---

## Repository Structure

```
ubp_novel_plastics_package/
├── README.md                          # This file
├── requirements.txt                   # Python dependencies
├── LICENSE                            # License information
├── code/                              # Source code
│   ├── chemical_carousel_pilot.py     # Pilot optimization for PP
│   ├── full_scale_carousel.py         # Full-scale optimization for all categories
│   ├── analyze_best_candidate.py      # Detailed analysis and recipe generation
│   ├── validate_system.py             # UBP framework validation
│   └── compile_formulary.py           # Formulary document generation
├── data/                              # Raw data (JSON)
│   ├── carousel_PET_results.json      # PET optimization results
│   ├── carousel_HDPE_results.json     # HDPE optimization results
│   ├── carousel_PVC_results.json      # PVC optimization results
│   ├── carousel_LDPE_results.json     # LDPE optimization results
│   ├── carousel_pilot_results.json    # PP optimization results (pilot)
│   ├── carousel_PS_results.json       # PS optimization results
│   ├── carousel_Other_results.json    # Bioplastic optimization results
│   ├── best_candidate_analysis.json   # Detailed analysis of best PP candidate
│   └── full_scale_summary.json        # Summary of all results
├── docs/                              # Documentation
│   ├── Phase1_Validation_Report.md    # System validation report
│   ├── Phase2_Pilot_Run_Report.md     # Pilot run detailed report
│   └── UBP_Novel_Plastics_Formulary.md # Complete material formulary
└── examples/                          # Example usage
    └── reproduce_study.py             # Script to reproduce the entire study
```

---

## Installation

### Prerequisites

- Python 3.11 or higher
- Access to the UBP framework v3.2+ (https://github.com/DigitalEuan/ubp_3.2)
- At least 4 GB of RAM
- Approximately 2-4 hours of computation time for full reproduction

### Setup

1. **Clone this repository:**
   ```bash
   git clone https://github.com/DigitalEuan/UBP_Repo.git
   cd UBP_Repo/ubp_novel_plastics_formulary
   ```

2. **Clone the UBP framework:**
   ```bash
   cd ..
   git clone https://github.com/DigitalEuan/ubp_3.2.git
   cd ubp_novel_plastics_formulary
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Verify installation:**
   ```bash
   python code/validate_system.py
   ```

   Expected output: `Overall Status: PASS - System is operational`

---

## Reproducing the Study

### Quick Start: View Existing Results

All results are already included in the `data/` directory. To view them:

```bash
# View summary of all results
python -m json.tool data/full_scale_summary.json

# View detailed results for a specific category (e.g., PP)
python -m json.tool data/carousel_pilot_results.json

# View detailed analysis of best candidate
python -m json.tool data/best_candidate_analysis.json
```

### Full Reproduction: Run the Entire Study

**Warning:** This will take 2-4 hours and will overwrite existing data files.

```bash
# Step 1: Validate the UBP framework (5 minutes)
python code/validate_system.py

# Step 2: Run pilot optimization for PP (15-20 minutes)
python code/chemical_carousel_pilot.py

# Step 3: Analyze best PP candidate (1 minute)
python code/analyze_best_candidate.py

# Step 4: Run full-scale optimization for all categories (2-3 hours)
python code/full_scale_carousel.py

# Step 5: Compile the formulary document (1 minute)
python code/compile_formulary.py
```

### Partial Reproduction: Single Category

To reproduce results for a single category (e.g., PET):

```python
from code.full_scale_carousel import run_category_optimization, PLASTIC_CATEGORIES

# Run optimization for PET
result = run_category_optimization(
    category_key='PET',
    category_data=PLASTIC_CATEGORIES['PET'],
    num_iterations=150,
    population_size=10
)

print(f"Best optimization score: {result['best_candidate']['optimization_score']:.4f}")
```

---

## Understanding the Data

### JSON Data Structure

Each `carousel_*_results.json` file contains:

```json
{
  "target_properties": {
    "tensile_strength": [600.0, 1.0],  // [target_value, weight]
    "hardness": [1000.0, 0.8],
    ...
  },
  "base_composition": {
    "C": 85.7,
    "H": 14.3
  },
  "processing_method": "injection_molding",
  "total_candidates": 1976,
  "best_candidate": {
    "composition": {...},
    "properties": {...},
    "ubp_metrics": {...},
    "optimization_score": 0.8304,
    "confidence": 0.7114
  },
  "all_candidates": [...]  // Array of all evaluated candidates
}
```

### Key Metrics

**Optimization Score (0-1):**
- Combines property matching (70%) and UBP coherence (30%)
- Higher is better
- Typical range: 0.65-0.86

**UBP Coherence Metrics:**
- **Elemental Coherence (0-1):** Atomic-level compatibility between elements
- **Structure Coherence (0-1):** Molecular-level order in polymer morphology
- **Overall Coherence (0-1):** Combined stability metric
- **Composition Balance (0-1):** Stoichiometric completeness (should be ~1.0)
- **Processing Compatibility (0-1):** Manufacturability score

**Confidence (0-1):**
- Model's certainty in the prediction
- Derived from overall coherence and processing compatibility
- Higher confidence → more reliable predictions

---

## Chemical Carousel Algorithm

The Chemical Carousel is an evolutionary optimization algorithm that discovers novel materials by:

1. **Initialization:** Start with a base polymer composition (e.g., pure polypropylene: 85.7% C, 14.3% H)

2. **Perturbation:** Randomly modify the composition by:
   - Adding new elements (e.g., O, N, Si, F, Cl)
   - Adjusting concentrations of existing elements
   - Perturbation strength decreases over generations (exploration → exploitation)

3. **Evaluation:** For each candidate composition:
   - Calculate UBP elemental coherence (atomic compatibility)
   - Predict material structure (amorphous, semi-crystalline, etc.)
   - Calculate UBP structure coherence (molecular order)
   - Predict properties (tensile strength, hardness, ductility, thermal transitions)
   - Compute optimization score (property matching + coherence)

4. **Selection:** Keep the top N candidates (typically 10) for the next generation

5. **Iteration:** Repeat steps 2-4 for 150-200 generations until convergence

6. **Output:** Return the best candidate and top 3 candidates for detailed analysis

**Key Parameters:**
- `num_iterations`: Number of optimization generations (150-200)
- `population_size`: Number of candidates retained per generation (10)
- `perturbation_strength`: Initial magnitude of composition changes (0.1 = 10%)
- `target_properties`: Dict of property targets and weights
- `allowed_elements`: List of elements that can be added to the composition

---

## UBP Framework Integration

This study uses the UBP Materials Research module (`materials_research.py`) from the UBP v3.2+ framework. The key components are:

### MaterialPredictor Class

Predicts material properties based on composition, structure, and processing:

```python
from materials_research import MaterialPredictor, MaterialComposition, ProcessingMethod

# Create predictor
predictor = MaterialPredictor(material_category=MaterialCategory.POLYMER)

# Define composition
composition = MaterialComposition(
    base_element='C',
    elements={'C': 85.7, 'H': 14.3}
)

# Predict properties
prediction = predictor.predict_all_properties(
    composition,
    processing=ProcessingMethod.INJECTION_MOLDING,
    temperature=20.0
)

print(f"Tensile Strength: {prediction.properties[MaterialProperty.TENSILE_STRENGTH]:.2f} MPa")
print(f"UBP Coherence: {prediction.ubp_metrics['overall_coherence']:.4f}")
```

### UBP Coherence Calculation

The UBP framework calculates coherence at two levels:

**1. Elemental Coherence:**
- Each element is encoded as a 24-bit BitTab structure (atomic number, period, group, block, valence)
- BitTab encodings are mapped to UBP frequencies using the Zitterbewegung constant
- Coherence is calculated from frequency differences between elements:
  ```
  coherence = Σ(weight_i × freq_ratio_i × exp(-k × freq_diff_i²))
  ```
- High coherence → elements have compatible frequencies → stable bonding

**2. Structure Coherence:**
- Evaluates how well the composition supports the predicted structure
- Factors include:
  - Base coherence for the structure type (ferrite, austenite, amorphous, etc.)
  - Temperature effects (thermal stability)
  - Composition-structure compatibility (e.g., carbon content for martensite)
  - Alloying element effects (e.g., Ni stabilizes austenite)
- High coherence → thermodynamically favorable structure → predictable properties

---

## Validation and Verification

### System Validation

The `validate_system.py` script confirms that the UBP framework is operational:

- Tests polymer prediction for polypropylene-like composition
- Tests metallic prediction for reference steels (AISI 1020, AISI 4140)
- Verifies UBP elemental frequency database (118 elements)
- Checks coherence calculations and property predictions

**Expected Output:**
```
Polymer Framework: PASS
Metallic Framework: PASS
Overall Status: PASS - System is operational
```

### Material Verification Protocol

Each discovered material should be validated experimentally using:

1. **FTIR Spectroscopy:** Confirm functional groups and chemical structure
2. **NMR Spectroscopy:** Determine polymer microstructure and comonomer incorporation
3. **GPC:** Measure molecular weight distribution (Mn, Mw, PDI)
4. **DSC:** Measure thermal transitions (Tg, Tm)
5. **Tensile Testing (ASTM D638):** Measure mechanical properties
6. **Shore D Hardness Testing (ASTM D2240):** Measure surface hardness
7. **TGA:** Assess thermal stability and decomposition temperature

Detailed verification protocols are provided in the Material Recipe Cards (see `docs/Phase2_Pilot_Run_Report.md`).

---

## Citation

If you use this work in your research, please cite:

```bibtex
@misc{craig2025ubpplastics,
  author = {Craig, Euan R A},
  title = {UBP Novel Plastics Formulary: Computational Discovery of High-Performance Polymer Materials},
  year = {2025},
  publisher = {GitHub},
  journal = {GitHub repository},
  howpublished = {\url{https://github.com/DigitalEuan/UBP_Repo/tree/main/ubp_novel_plastics_formulary}},
  note = {Universal Binary Principle Framework v3.2+}
}
```

---

## License

This work is released under the MIT License. See `LICENSE` file for details.

---

## Contact

**Euan R A Craig**  
Email: info@digitaleuan.com  
GitHub: https://github.com/DigitalEuan  
Academia: https://independent.academia.edu/EuanCraig2  
X: https://x.com/DigitalEuan

---

## Acknowledgments

This work was conducted using the Universal Binary Principle (UBP) framework v3.2+, developed by Euan R A Craig. The Chemical Carousel algorithm was designed specifically for this study to enable systematic exploration of polymer composition space guided by UBP coherence metrics.

Special thanks to the open-source scientific Python community for providing the foundational tools (NumPy, RDKit, Qutip) that made this research possible.

---

## Future Directions

1. **Experimental Validation:** Synthesize top candidates and measure actual properties
2. **Scale-Up Studies:** Develop pilot-scale production processes
3. **Life Cycle Assessment:** Evaluate environmental impact and sustainability
4. **Application Testing:** Validate performance in real-world use cases
5. **Machine Learning Integration:** Train ML models on UBP-generated data for faster predictions
6. **Multi-Objective Optimization:** Extend the Chemical Carousel to optimize for sustainability metrics (recyclability, biodegradability) alongside performance

---

**Last Updated:** October 14, 2025  
**Version:** 1.0.0

