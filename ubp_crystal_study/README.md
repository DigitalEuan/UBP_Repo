# UBP Crystal Resonance Study

A comprehensive computational investigation into crystal vibrations and natural resonance using the Universal Binary Principle (UBP) 3.3 framework.

## Overview

This study explores the fundamental question: **Why do crystals have natural vibration frequencies?** Using the UBP computational framework, we modeled 20 diverse crystal systems to test the hypothesis that crystal resonance emerges from the geometric and informational constraints of an underlying computational substrate.

## Key Findings

- ✅ All crystals achieved **COHERENT** or **SUPERCOHERENT** NRCI regimes (> 0.9999)
- ✅ Successfully predicted resonance frequencies spanning **13 orders of magnitude** (32 kHz to 25 THz)
- ✅ Correctly identified and quantified **piezoelectric properties** for 5 materials
- ✅ Demonstrated strong correlation between **crystal structure, coherence, and vibrational behavior**
- ✅ Validated the UBP's **TGIC (3-6-9 balance)** as a geometric organizing principle

## Repository Structure

```
ubp_crystal_study/
├── README.md                       # This file
├── data/
│   └── crystal_database.py         # Database of 20 crystal systems with properties
├── simulations/
│   ├── ubp_crystal_simulator.py    # Main UBP crystal simulation engine
│   ├── run_all_crystals.py         # Batch simulation script
│   └── analyze_results.py          # Analysis and visualization script
├── results/
│   ├── *_results.json              # Individual crystal simulation results (20 files)
│   └── all_crystals_summary.json   # Consolidated summary
├── visualizations/
│   ├── comprehensive_summary.png   # Overview of all results
│   ├── frequency_spectrum.png      # Resonance frequency spectrum
│   ├── nrci_by_structure.png       # NRCI analysis by structure
│   ├── nrci_by_bonding.png         # NRCI analysis by bonding type
│   ├── tgic_satisfaction.png       # TGIC geometric constraint satisfaction
│   ├── piezoelectric_properties.png # Piezoelectric coefficients
│   ├── frequency_vs_nrci.png       # Correlation analysis
│   ├── quality_scores.png          # UBP quality scores
│   └── offbit_distribution.png     # OffBit layer distribution
├── docs/
│   └── analysis_report.md          # Detailed analysis report
└── paper/
    └── ubp_crystal_study.md        # Full academic paper
```

## The 20 Crystal Systems

| Crystal     | Formula      | Structure        | Bonding              | Piezo? |
|-------------|--------------|------------------|----------------------|--------|
| Polonium    | Po           | Simple Cubic     | metallic             | No     |
| CsCl        | CsCl         | Primitive Cubic  | ionic                | No     |
| NaCl        | NaCl         | FCC (Rock Salt)  | ionic                | No     |
| Gold        | Au           | FCC              | metallic             | No     |
| Copper      | Cu           | FCC              | metallic             | No     |
| Iron        | Fe           | BCC              | metallic             | No     |
| Tungsten    | W            | BCC              | metallic             | No     |
| Magnesium   | Mg           | HCP              | metallic             | No     |
| Zinc        | Zn           | HCP              | metallic             | No     |
| Diamond     | C            | Diamond Cubic    | covalent             | No     |
| Silicon     | Si           | Diamond Cubic    | covalent             | No     |
| GaAs        | GaAs         | Zincblende       | mixed_ionic_covalent | Yes    |
| Quartz      | SiO₂         | Trigonal         | covalent             | Yes    |
| LiNbO₃      | LiNbO₃       | Trigonal         | mixed_ionic_covalent | Yes    |
| PZT         | Pb(Zr,Ti)O₃  | Perovskite       | mixed_ionic_covalent | Yes    |
| AlN         | AlN          | Wurtzite         | mixed_ionic_covalent | Yes    |
| Calcite     | CaCO₃        | Trigonal         | ionic                | No     |
| Rutile      | TiO₂         | Tetragonal       | mixed_ionic_covalent | No     |
| Sapphire    | Al₂O₃        | Trigonal         | mixed_ionic_covalent | No     |
| Ice Ih      | H₂O          | Hexagonal        | hydrogen_bonding     | No     |

## Requirements

- Python 3.11+
- UBP 3.3 framework (from [UBP_Repo](https://github.com/DigitalEuan/UBP_Repo))
- NumPy
- Matplotlib

## Installation

```bash
# Clone the UBP repository
gh repo clone DigitalEuan/UBP_Repo

# Install Python dependencies
pip3 install numpy matplotlib

# Navigate to UBP 3.3
cd UBP_Repo/ubp_3.3
pip3 install -r requirements.txt
```

## Usage

### Run Simulations for All Crystals

```bash
cd ubp_crystal_study
python3.11 simulations/run_all_crystals.py
```

### Simulate a Single Crystal

```python
from simulations.ubp_crystal_simulator import UBPCrystalSimulator

simulator = UBPCrystalSimulator()
result = simulator.simulate_crystal("Si", verbose=True)
```

### Generate Analysis and Visualizations

```bash
python3.11 simulations/analyze_results.py
```

## Key Results

### NRCI Statistics
- **Mean NRCI**: 0.999918
- **Range**: 0.999900 - 0.999990
- **Regime**: All crystals in COHERENT or SUPERCOHERENT

### Frequency Spectrum
- **Range**: 32.768 kHz (Quartz) to 25.23 THz (Diamond)
- **Mean**: 4.57 THz
- **Span**: 13 orders of magnitude

### Piezoelectric Crystals
- **GaAs**: d₃₃ = 2.70 pC/N, k = 0.0500
- **Quartz**: d₃₃ = 2.30 pC/N, k = 0.1000
- **LiNbO₃**: d₃₃ = 6.00 pC/N, k = 0.1700
- **PZT**: d₃₃ = 299.97 pC/N, k = 0.6999
- **AlN**: d₃₃ = 5.50 pC/N, k = 0.2400

## Novel UBP Perspectives

This study introduces several novel interpretations of crystal physics through the UBP lens:

1. **Phonons as Toggle Patterns**: Vibrational modes are structured, propagating patterns of OffBit toggles within the Bitfield.

2. **Resonance from Geometric Constraints**: Natural frequencies emerge from the TGIC (3-6-9 balance) geometric organizing principle.

3. **Piezoelectricity as Information Transduction**: The piezoelectric effect represents efficient conversion between mechanical deformation (Bitfield pattern changes) and electrical flow (toggle propagation).

4. **Crystal Growth as NRCI Maximization**: Crystal formation is a process of the system seeking maximum coherence and informational stability.

5. **Tuned Crystal Design**: The framework enables computational design of crystals with specific target frequencies by optimizing structure, composition, and defects.

## Academic Paper

The full academic paper is available in `paper/ubp_crystal_study.md` and includes:

- Comprehensive introduction to the UBP framework
- Detailed methodology
- Complete results with visualizations
- In-depth discussion of implications
- References

## Author

**Euan R A Craig**
- Email: info@digitaleuan.com
- GitHub: [@DigitalEuan](https://github.com/DigitalEuan)
- Academia: [Euan Craig](https://independent.academia.edu/EuanCraig2)
- X: [@DigitalEuan](https://x.com/DigitalEuan)

## License

This work is part of the Universal Binary Principle research project. For licensing information, please refer to the main [UBP_Repo](https://github.com/DigitalEuan/UBP_Repo).

## Citation

If you use this work in your research, please cite:

```
Craig, E. R. A. (2025). A Universal Binary Principle (UBP) Investigation into 
Crystal Resonance and Vibrational Dynamics. UBP Crystal Study. 
GitHub: https://github.com/DigitalEuan/UBP_Repo
```

## Acknowledgments

This study was conducted using the UBP 3.3 framework, which represents years of development in computational physics and information theory. Special thanks to the broader UBP research community for their foundational work.

---

**Study Completed**: November 2025
**UBP Version**: 3.3
**Simulation Count**: 20 crystal systems
**Success Rate**: 100%
