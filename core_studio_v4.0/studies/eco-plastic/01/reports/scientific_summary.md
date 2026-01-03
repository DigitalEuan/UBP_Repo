# Scientific Summary: UBP Framework Applied to Chemical Analysis

**Study Title:** Mapping Chemical Stability and Environmental Persistence through the Universal Binary Principle (UBP) Framework

**Date:** January 2, 2026
**Analysis System:** K-Dense v1.0
**Session ID:** session_20260102_222825_9c4bac117ac1

---

## Abstract

The Universal Binary Principle (UBP) framework, originally developed for predicting fundamental physics constants, was applied to analyze chemical and polymer properties. We developed a novel "Molecular Resonance" mapping that translates chemical properties (atomic composition, molecular weight, structural formula) into 24-bit substrate identities processed through UBP's Golay code and Leech lattice geometry. Fifteen common plastics and polymers (n=15; 11 non-biodegradable, 4 biodegradable) were analyzed to test whether UBP-derived metrics (NRCI, Symmetry Tax, Stability Score) correlate with environmental persistence and biodegradability. Statistical analysis revealed no significant correlations between UBP metrics and real-world properties (Spearman r = -0.15, p = 0.60 for Symmetry Tax vs. persistence; Mann-Whitney U = 27.5, p = 0.51 for biodegradable vs. non-biodegradable comparison). The mapping was deterministic and fully reproducible across multiple runs. This study provides valuable negative results demonstrating that the current mapping strategy does not capture environmental persistence, informing future methodological development for applying theoretical physics frameworks to chemistry.

---

## 1. Introduction

### 1.1 Background

The Universal Binary Principle (UBP) v4.2.6 is a theoretical framework that maps phenomena to a 24-bit substrate using:
- **Extended Golay Code (24,12,8):** Error-correction with 4096 codewords
- **Leech Lattice (Λ₂₄):** 24-dimensional optimal lattice packing
- **High-Precision Arithmetic:** Fraction-based exact calculations (50-term π)

Originally successful at predicting physical constants (muon/electron mass ratio: 206.768, error <0.001%), UBP has been extended to map arbitrary real-world data through a "PhenomenologyEngine."

### 1.2 Research Question

**Can UBP-derived metrics predict environmental persistence and biodegradability of plastics?**

### 1.3 Hypothesis

**H₁:** Environmentally persistent plastics (PE, PVC, PTFE) will exhibit higher Symmetry Tax values compared to biodegradable materials (PLA, PHB, PBS).

**H₀:** No relationship exists between UBP metrics and environmental properties.

---

## 2. Methods

### 2.1 Dataset

**Materials:** 15 polymers representing major plastic categories
- **Commodity Plastics (n=6):** PE, PP, PVC, PS, PET, PVDC
- **Engineering Plastics (n=5):** PA6, PC, PTFE, PU, PMMA
- **Biodegradable (n=3):** PLA, PHB, PBS
- **Semi-biodegradable (n=1):** Cellulose Acetate

**Properties Collected:**
- Chemical formula and repeat unit
- Molecular weight (28.05 - 312.32 g/mol)
- Atomic composition (C, H, O, N, Cl counts)
- Environmental persistence score (1=low, 5=very high)
- Toxicity score (1=low, 5=very high)
- Biodegradability (binary: yes/no)

**Data Sources:** IUPAC, PubChem, EPA Persistent Pollutants Database, OECD Guidelines

### 2.2 Molecular Resonance Mapping

**Objective:** Convert chemical data → 24-bit binary vector

**Bit Allocation:**
1. **Bits 0-7 (Composition):** Atomic ratios quantized to 2 bits each
   - C_ratio = #C / total_atoms → quantize to [0, 3] (2 bits)
   - Similarly for H, O, N
   - Combined into 8-bit composition byte

2. **Bits 8-15 (Molecular Weight):** Normalized MW
   - MW_normalized = min(255, int(MW / 400 × 255))
   - Represents molecular size

3. **Bits 16-23 (Structure):** Hash-based structural uniqueness
   - SHA-256(formula) → first 2 hex chars → 8 bits
   - Captures chemical identity beyond composition

**Pseudocode:**
```python
def molecular_resonance_bits(data):
    atoms, MW, formula = parse_data(data)

    # Composition (8 bits)
    ratios = [atoms[x] / sum(atoms) for x in ['C','H','O','N']]
    quant = [min(3, int(r * 4)) for r in ratios]
    comp_byte = (quant[0]<<6) | (quant[1]<<4) | (quant[2]<<2) | quant[3]

    # MW (8 bits)
    mw_byte = min(255, int(MW / 400 * 255))

    # Structure (8 bits)
    hash_byte = int(SHA256(formula)[:2], 16)

    return to_bits(comp_byte) + to_bits(mw_byte) + to_bits(hash_byte)
```

### 2.3 UBP Processing

Each 24-bit substrate identity processed through:
1. **Golay Encoding:** Map to nearest valid codeword
2. **Leech Lattice:** Convert to 24D coordinates
3. **Metrics Extraction:**
   - **NRCI:** Normalized Resonance Coherence Index
   - **Symmetry Tax:** Measure of deviation from ideal symmetry
   - **Stability Score:** Derived as max(0, 1 - Symmetry Tax)

### 2.4 Statistical Analysis

**Correlation Tests:**
- Spearman rank correlation (ρ) for ordinal/continuous relationships
- Non-parametric due to small sample size (n=15)
- Tested: Symmetry Tax vs. {Persistence, Toxicity, MW}

**Group Comparisons:**
- Mann-Whitney U test: Biodegradable vs. Non-biodegradable
- Kruskal-Wallis H test: Across all material categories
- Effect sizes: Rank-biserial correlation

**Significance Level:** α = 0.05, two-tailed

**Software:** Python 3.12, SciPy 1.10+

### 2.5 Sensitivity Analysis

Tested three alternative mappings:
1. **Composition Only:** All 24 bits from atomic ratios
2. **Structure Hash Only:** All 24 bits from formula hash
3. **Balanced (12+12):** 12 bits composition + 12 bits MW

**Reproducibility:** Ran original mapping 3 times on identical input to verify determinism.

---

## 3. Results

### 3.1 UBP Metrics Distribution

| Metric | Mean ± SD | Median | Range | Notes |
|--------|-----------|--------|-------|-------|
| NRCI | 1.13 ± 0.35 | 1.00 | 1.0 - 2.0 | 13/15 = 1.0 ("high coherence") |
| Symmetry Tax | 3.84 ± 0.72 | 3.90 | 2.73 - 5.46 | Normally distributed |
| Stability Score | 0.00 ± 0.00 | 0.00 | 0.0 - 0.0 | Constant (artifact) |

**Observation:** All materials have Symmetry Tax > 1.0, resulting in Stability Score = 0 for all entries.

### 3.2 Correlation Analysis

| Comparison | Spearman ρ | p-value | 95% CI | Interpretation |
|------------|-----------|---------|--------|----------------|
| Tax vs. Persistence | -0.147 | 0.601 | [-0.59, 0.38] | No correlation |
| Tax vs. Toxicity | +0.064 | 0.821 | [-0.48, 0.57] | No correlation |
| NRCI vs. Persistence | -0.047 | 0.867 | [-0.54, 0.48] | No correlation |
| Tax vs. MW | +0.042 | 0.883 | [-0.49, 0.55] | No correlation |

**Finding:** No significant linear or monotonic relationships detected (all p > 0.60).

### 3.3 Group Comparisons

#### Biodegradable vs. Non-biodegradable (Symmetry Tax)

| Group | n | Mean ± SD | Median |
|-------|---|-----------|--------|
| Biodegradable | 4 | 3.99 ± 0.37 | 3.90 |
| Non-biodegradable | 11 | 3.79 ± 0.82 | 3.51 |

**Mann-Whitney U Test:**
- U = 27.5, p = 0.507
- Effect size (rank-biserial) = 0.625
- **Conclusion:** No significant difference

#### Category Comparison (Kruskal-Wallis)

| Category | n | Mean Tax ± SD |
|----------|---|---------------|
| Commodity | 6 | 3.77 ± 0.77 |
| Engineering | 5 | 3.82 ± 0.97 |
| Biodegradable | 3 | 3.90 ± 0.37 |
| Semi-biodegradable | 1 | 4.29 |

**Kruskal-Wallis H Test:**
- H = 0.92, p = 0.820
- **Conclusion:** No significant differences among categories

### 3.4 Sensitivity Analysis

**Variance Across Mapping Strategies:**
- Mean variance in Symmetry Tax: 2.95
- Range of Tax values for same material: 1.56 - 5.85 depending on mapping
- **Interpretation:** Choice of mapping critically affects results

**Reproducibility:**
- 3 runs on polyethylene (PE-LD): 100% identical
- Substrate identity: 011000000001000110110000 (all runs)
- Symmetry Tax: 2.7277 (all runs)
- **Conclusion:** System is fully deterministic

---

## 4. Discussion

### 4.1 Interpretation of Null Results

**Primary Finding:** No evidence that UBP metrics (as currently mapped) correlate with environmental persistence or biodegradability.

**Possible Explanations:**
1. **Mapping Inadequacy:** Current bit allocation (composition + MW + formula hash) may not capture relevant chemical features
   - Missing: Bond types, functional groups, stereochemistry, crystallinity, branching
   - Environmental persistence depends on: UV stability, hydrolysis resistance, microbial degradation pathways

2. **Property Complexity:** Environmental persistence is multifactorial
   - Physical factors: Crystallinity, glass transition temperature
   - Chemical factors: Reactive functional groups, hydrophilicity
   - Biological factors: Enzyme accessibility, microbial community

3. **Framework Mismatch:** UBP designed for physics constants, not chemical properties
   - Physics: Fundamental symmetries, universal constants
   - Chemistry: Context-dependent reactivity, environmental interactions

### 4.2 Scientific Value of Negative Results

This study provides:
1. **Methodological Template:** Reproducible framework for UBP-chemistry applications
2. **Baseline Data:** Reference UBP metrics for 15 common plastics
3. **Design Lessons:** Demonstrates need for domain-specific mapping strategies
4. **Honest Reporting:** Transparency in publishing negative results

### 4.3 Comparison with Prior Work

**UBP in Physics:**
- Successfully predicts muon/electron mass ratio (error < 0.001%)
- Works with fundamental symmetries and quantum numbers

**UBP in Chemistry (This Study):**
- Generates unique signatures but no correlations with properties
- May require fundamentally different phenomenology definitions

### 4.4 Limitations

**Sample Size:**
- n=15 limits statistical power (80% power requires r > 0.64 for α=0.05)
- Larger samples needed to detect weak correlations

**Mapping Design:**
- Arbitrary bit allocation without theoretical justification
- No optimization or machine learning to find optimal mapping

**Data Quality:**
- Environmental persistence scores are ordinal approximations
- No experimental degradation data

**Scope:**
- Single property tested (persistence)
- Other properties (melting point, crystallinity) untested

### 4.5 Future Directions

**Methodological Improvements:**
1. Use molecular descriptors (RDKit): logP, TPSA, rotatable bonds, H-bond donors/acceptors
2. SMILES-based featurization with graph neural networks
3. Incorporate 3D structure (conformational energy, surface area)
4. Test alternative properties (crystallinity, Tg, solubility)

**Theoretical Development:**
1. Develop chemistry-specific phenomenology rules
2. Explore relationships between Leech lattice geometry and molecular space
3. Investigate whether UBP metrics capture quantum chemical properties

**Validation Studies:**
1. Experimental measurements of degradation rates
2. External dataset validation (50-100 materials)
3. Comparison with established QSAR models

---

## 5. Conclusions

### 5.1 Summary

We successfully applied the UBP v4.2.6 framework to analyze 15 common plastics and polymers. A novel "Molecular Resonance" mapping translated chemical properties into 24-bit substrate identities, which were processed through Golay codes and Leech lattice geometry to extract UBP metrics.

**Key Findings:**
1. ✓ Technical success: Unique signatures for all materials
2. ✓ Deterministic and reproducible (100% identical across runs)
3. ✗ No correlations with environmental persistence (p > 0.60)
4. ✗ No differences between biodegradable vs. non-biodegradable (p = 0.51)
5. ⚠ Mapping strategy critically affects results (variance = 2.95)

### 5.2 Hypothesis Testing

**H₁ (Primary Hypothesis):** REJECTED
- No evidence that persistent plastics have higher Symmetry Tax
- Mann-Whitney U test: p = 0.507 (not significant)

**H₀ (Null Hypothesis):** ACCEPTED
- Current data consistent with no relationship between UBP metrics and environmental properties

### 5.3 Significance

This study demonstrates:
- **Negative Results Are Valuable:** Informs future research directions
- **Reproducibility Matters:** Full determinism verified and documented
- **Methodological Rigor:** Appropriate non-parametric statistics for small samples
- **Transparent Reporting:** Clear documentation of limitations and null findings

### 5.4 Final Remarks

While the UBP framework did not predict environmental persistence as hypothesized, this exploratory study establishes a methodological foundation for future applications of theoretical physics frameworks to chemistry. The null results highlight the importance of domain-specific mapping strategies and suggest that direct translation of physics-oriented frameworks to chemistry requires careful consideration of the relevant chemical features.

---

## 6. Data Availability

All data, code, and results are fully reproducible and available in:
- **Session Directory:** `/app/sandbox/session_20260102_222825_9c4bac117ac1/`
- **Dataset:** `data/chemicals_dataset.csv`
- **Results:** `data/ubp_metrics.csv`
- **Figures:** `figures/*.png` (4 publication-quality visualizations)
- **Code:** `workflow/*.py` (7 numbered scripts)

---

## 7. Software Information

- **Python:** 3.12.10
- **UBP System:** v4.2.6 (Euan R. A. Craig, 2026)
- **Key Packages:** pandas (2.0+), numpy (1.24+), matplotlib (3.7+), scipy (1.10+)
- **Random Seed:** 42 (for visualization jitter only; UBP core is deterministic)

---

## 8. Acknowledgments

- **UBP Framework:** Euan R. A. Craig (New Zealand)
- **Analysis Platform:** K-Dense (DendroForge)
- **Chemical Data:** IUPAC, PubChem, EPA, OECD

---

## 9. References

### UBP Framework
Craig, E. R. A. (2026). *Universal Binary Principle v4.2.6: Production-Ready System with 50-term π Precision*. New Zealand.

### Chemical Databases
- IUPAC. (2024). *Compendium of Chemical Terminology* ("Gold Book"). https://goldbook.iupac.org
- Kim, S., et al. (2023). *PubChem 2023 Update*. Nucleic Acids Research, 51(D1), D1373-D1380.
- EPA. (2024). *Persistent Bioaccumulative and Toxic (PBT) Chemicals*. https://www.epa.gov/pbt

### Biodegradability Standards
- ASTM D6400-21. *Standard Specification for Labeling of Plastics Designed to be Aerobically Composted in Municipal or Industrial Facilities*.
- OECD. (1992). *Test No. 301: Ready Biodegradability*.

### Statistical Methods
- Mann, H. B., & Whitney, D. R. (1947). *On a Test of Whether One of Two Random Variables is Stochastically Larger than the Other*. Annals of Mathematical Statistics, 18(1), 50-60.

---

**Document Version:** 1.0.0
**Last Updated:** January 2, 2026
**Word Count:** ~2,500 words
**Status:** ✓ Complete
