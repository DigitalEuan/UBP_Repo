# Real Experimental Data Acquisition Summary

**Date**: October 29, 2025  
**Purpose**: Identify and acquire real experimental datasets for UBP framework validation

---

## 1. Quantum Entanglement Data

### NIST Bell Test Data (2015)

**Source**: https://www.nist.gov/pml/applied-physics-division/bell-test-research-software-and-data/repository-bell-test-research-3

**Status**: ✓ AVAILABLE - Public repository on Amazon S3

**Description**: Raw data from the NIST loophole-free Bell test experiment (Shalm et al., 2015). This is one of the three landmark experiments that definitively closed all major loopholes in Bell tests.

**Data Structure**:
- Separate data for Alice and Bob measurement stations
- Time-tagged detection events
- Multiple runs with different configurations
- File format: `.dat.zip` (compressed binary data)

**Available Datasets**:

| Run Name | Alice Size | Bob Size | Description |
|:---------|:-----------|:---------|:------------|
| `00_44_CH_pockel_100kHz.run3` | 346.6 MB | 361.5 MB | Early calibration run |
| `02_54_CH_pockel_100kHz.run4.afterTimingfix2` | 1.8 GB | 1.8 GB | Main run after timing corrections |
| `03_31_CH_pockel_100kHz.run4.afterTimingfix2_training` | 247.9 MB | 250.6 MB | Training dataset |
| `03_43_CH_pockel_100kHz.run4.afterTimingfix2_afterfixingModeLocking` | 913.5 MB | 933.8 MB | After mode-locking fix |
| `19_45_CH_pockel_100kHz.run.nolightconeshift` | 1.5 GB | 1.6 GB | No light-cone shift |
| `21_15_CH_pockel_100kHz.run.200nsadditiondelay_lightconeshift` | 1.5 GB | ~1.5 GB | With delay |
| `23_55_CH_pockel_100kHz.run.ClassicalRNGXOR` | 1.5 GB | ~1.5 GB | Classical RNG control |

**Recommended for Analysis**: 
- **Training dataset** (247.9 MB + 250.6 MB = ~500 MB total) - manageable size, good quality
- **Main run** (1.8 GB + 1.8 GB = 3.6 GB) - full experimental data

**Data Format**: Time-tagged photon detection events with measurement settings

**Challenges**:
- Binary format requires parsing
- Large file sizes (GB-scale)
- Need to understand data structure and extract coincidence events

---

## 2. Magnetic Materials Data

### Option A: Complex Spin Structure Data (4TU.ResearchData)

**Source**: https://data.4tu.nl/datasets/a8fc2b7d-1cb7-4499-a486-930ff5117f96

**Status**: ✓ AVAILABLE - Public dataset

**Description**: Original experimental data for "Complex Spin Structure and Magnetic Phase Transition of Mn₃₋ₓFeₓSn Alloys"

**Content**: Magnetic phase transition data including temperature-dependent measurements

**Format**: ZIP download with multiple data files

### Option B: JuHemd Database (Materials Cloud)

**Source**: https://archive.materialscloud.org/records/7q2n7-ezx08

**Status**: ✓ AVAILABLE - Public database

**Description**: Jülich-Heusler-magnetic-database of magnetic phase transition types and transition temperatures (Tc) for Heusler materials

**Content**: 
- Magnetic phase transition temperatures
- Transition types (ferromagnetic, antiferromagnetic, etc.)
- Experimentally documented materials

**Advantages**:
- Curated database
- Multiple materials
- Clear phase transition data

---

## 3. Recommended Acquisition Strategy

Given time and computational constraints, I recommend a **focused approach**:

### Priority 1: NIST Bell Test Data (Quantum Entanglement)
- **Download**: Training dataset (~500 MB total)
- **Rationale**: 
  - Real loophole-free Bell test data
  - Manageable size
  - Well-documented experiment
  - Direct test of w ≈ 1.53 prediction

### Priority 2: Magnetic Materials Database
- **Download**: JuHemd database or Mn₃₋ₓFeₓSn dataset
- **Rationale**:
  - Phase transition data
  - Test w = 1.0 → 2.5 prediction
  - Multiple materials for robustness

### Priority 3: Additional Domain (if time permits)
- Search for superconductivity transition data
- Or use high-quality simulated data based on experimental parameters

---

## 4. Data Processing Requirements

### For NIST Bell Test Data:
1. **Parser**: Need to write binary data parser for `.dat` format
2. **Extraction**: Extract Alice-Bob coincidence events
3. **Conversion**: Convert to binary sequences for NRCI-I analysis
4. **Analysis**: Apply geometric weight scanning

### For Magnetic Data:
1. **Parser**: Read magnetization vs. temperature data
2. **Binarization**: Convert continuous magnetization to binary (spin up/down)
3. **Phase Detection**: Identify critical temperature
4. **Analysis**: Apply NRCI-I and weight scanning across temperature range

---

## 5. Expected Outcomes

If the UBP framework is correct, we should observe:

**Quantum Entanglement (NIST Data)**:
- Optimal geometric weight **w ≈ 1.53**
- High NRCI-I values (~0.99)
- High Lempel-Ziv complexity
- Strong violation of CHSH inequality (S > 2)

**Magnetic Phase Transitions**:
- **Below Tc (ordered)**: w ≈ 1.0, low NRCI-I, low complexity
- **At Tc (critical)**: w ≈ 2.5, intermediate NRCI-I
- **Above Tc (disordered)**: w ≈ 2.5, low NRCI-I, moderate complexity

---

## 6. Implementation Plan

1. **Download NIST training dataset** (Alice + Bob, ~500 MB)
2. **Develop binary data parser** for NIST format
3. **Extract and analyze** quantum entanglement data
4. **Download magnetic materials dataset**
5. **Process and analyze** magnetic phase transition data
6. **Compare results** with simulation predictions
7. **Document findings** in Study 3 paper

---

## 7. Alternative: High-Fidelity Synthetic Data

If data acquisition/parsing proves too time-consuming, we can use **high-fidelity synthetic data** parameterized from published experimental results:

**Advantages**:
- Known ground truth
- Controlled parameters
- Faster iteration
- Still scientifically valid for framework testing

**Disadvantages**:
- Not "real" data
- Potential for confirmation bias
- Less convincing for publication

**Recommendation**: Attempt real data first, fall back to synthetic if necessary.

---

## Status: Ready to Proceed

**Next Steps**:
1. Attempt to download NIST training dataset
2. Develop parser and run analysis
3. Proceed with magnetic data if successful
4. Document all findings for Study 3 paper

