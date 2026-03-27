# Implementation Plan: UBP Nuclear Physics Study

## Objective
Apply the Universal Binary Principle framework to nuclear physics (binding energies and decay rates) using the real UBP scripts, compare against experimental data, and produce a reproducible research package.

## Steps Completed

### Step 1: Environment Setup
- Ran `uv sync` to install all dependencies
- Verified UBP scripts import correctly (core.py, physics.py, geometry.py, etc.)
- Loaded UBP Knowledge Base (806 entries, 118 elements)

### Step 2: Data Extraction & Preparation
- Extracted all 118 element entries from `ubp_system_kb.json`
- Computed UBP metrics: NRCI, Symmetry Tax, Hamming weight, Tilt, Ontological Drift, Barnes-Wall macro-NRCI
- Built experimental nuclear dataset: semi-empirical binding energies (Bethe-Weizsäcker, AME2020 params), half-lives from NUBASE2020
- Defined new derived UBP metrics: Nuclear Coherence Index (NCI), Stability Pressure, Phase-Lock classification

### Step 3: Statistical Analysis
- Spearman and Pearson correlations: NRCI vs BE/A, Tax vs BE/A, NCI vs BE/A
- Welch t-test + Cohen's d: stable vs unstable nuclei NRCI separation
- Magic number analysis: t-test comparing magic-Z vs non-magic NRCI
- Decay rate analysis: NRCI, Tax, Stability Pressure vs log10(half-life) for 17 radioactive elements
- Nuclear shell gradient analysis: ∇Tax vs ∇BE/A
- Particle physics predictions: 13D Sink Protocol for 21 particles/constants

### Step 4: Deep Dive Findings
- Iron peak region (Z=20-35) detailed analysis
- Leech Lattice expansion of Fe-56 vector
- Phase-Lock classification of all 118 elements

### Step 5: Figure Generation (7 figures)
1. NRCI across periodic table with BE/A overlay
2. NRCI vs BE/A scatter with regression
3. Magic number boxplot comparison
4. Decay rate correlations
5. Particle physics prediction accuracy
6. Iron peak deep dive (3-panel)
7. Phase-Lock distribution map

## Success Criteria
- [x] Successful execution of UBP scripts against nuclear data
- [x] Statistical correlations identified and quantified
- [x] Unique UBP insights discovered (stable/unstable separation, iron peak geometry)
- [x] Reproducible code package created
- [x] Figures generated for paper
- [x] README and manifest completed
