# Installation & Usage Instructions

## UBP Antibiotic Discovery Study - Complete Package

This package contains everything needed to reproduce and extend the UBP antibiotic discovery study.

---

## Package Contents

```
ubp_antibiotics_package/
├── README.md                    # Main documentation
├── INSTALLATION.md              # This file
│
├── scripts/                     # All Python scripts (7 files)
│   ├── antibiotic_realm.py
│   ├── bitfield_explorer.py
│   ├── study_antibiotic_discovery.py
│   ├── reverse_engineer_antibiotics.py
│   ├── analyze_superrabbits.py
│   ├── verify_candidates.py
│   └── quick_demo.py
│
├── docs/                        # Documentation & paper
│   ├── DESIGN.md
│   ├── STUDY_SUMMARY.md
│   ├── paper.tex               # LaTeX paper (Overleaf-ready)
│   └── requirements.txt
│
└── results/                     # Study results
    ├── top_antibiotic_candidates.json
    └── reverse_engineering_results.json
```

---

## Installation Steps

### 1. Prerequisites

You need:
- **GPU UBP 3.6 system** (from the main UBP_Repo)
- **Python 3.11+**
- **Standard Python libraries** (no additional packages needed)

### 2. Extract the Package

```bash
# If you have the tarball
tar -xzf ubp_antibiotics_package.tar.gz
cd ubp_antibiotics_package
```

### 3. Set Up UBP Core Link

The scripts require access to the GPU UBP 3.6 core modules. You have two options:

**Option A: Place in UBP Repository** (Recommended)
```bash
# Copy the entire package to your UBP repository
cp -r ubp_antibiotics_package /path/to/UBP_Repo/

# Create symlink to UBP core
cd /path/to/UBP_Repo/ubp_antibiotics_package/scripts
ln -s ../../gpu_ubp_system/03/core ubp_core
```

**Option B: Standalone Installation**
```bash
# Clone the UBP repository if you don't have it
gh repo clone DigitalEuan/UBP_Repo

# Create symlink from your package to UBP core
cd ubp_antibiotics_package/scripts
ln -s /path/to/UBP_Repo/gpu_ubp_system/03/core ubp_core
```

### 4. Verify Installation

```bash
cd scripts
python3.11 quick_demo.py
```

Expected output:
```
✓ Found 10 super-rabbits in ~2 seconds
✓ Top candidate: 0x... (NRCI: 0.999999...)
```

---

## Usage

### Quick Demonstration

```bash
cd scripts
python3.11 quick_demo.py
```

Runs a fast 10,000-pattern scan to verify everything works.

### Reverse Engineering Known Antibiotics

```bash
python3.11 reverse_engineer_antibiotics.py
```

Analyzes 8 FDA-approved antibiotics and searches for similar patterns.

### Full Discovery Study

```bash
python3.11 study_antibiotic_discovery.py
```

Runs the complete 1 million pattern exploration (~2.5 hours).

### Analyze Results

```bash
python3.11 analyze_superrabbits.py
```

Parses the study log and ranks candidates by antibiotic-likeness.

### Verify Candidates

```bash
python3.11 verify_candidates.py
```

Performs deep verification of top candidates.

---

## Scientific Paper

### Compile Locally

If you have LaTeX installed:

```bash
cd docs
pdflatex paper.tex
bibtex paper
pdflatex paper.tex
pdflatex paper.tex
```

### Use Overleaf

1. Go to [Overleaf](https://www.overleaf.com/)
2. Create new project → Upload Project
3. Upload `docs/paper.tex`
4. Compile

---

## Customization

### Modify Search Parameters

Edit `study_antibiotic_discovery.py`:

```python
# Line ~200: Change number of patterns
total_patterns = 1_000_000  # Change to 10_000_000 for larger search

# Line ~210: Change NRCI threshold
nrci_threshold = 0.9999992  # Adjust for more/fewer candidates
```

### Add New Known Antibiotics

Edit `reverse_engineer_antibiotics.py`:

```python
# Line ~30: Add to KNOWN_ANTIBIOTICS dictionary
KNOWN_ANTIBIOTICS = {
    "YourDrug": {
        "pattern": 0xABCDEF,  # Your 24-bit pattern
        "year": 2024,
        "mechanism": "Your mechanism"
    },
    # ... existing drugs
}
```

---

## Troubleshooting

### "ModuleNotFoundError: No module named 'ubp_core'"

**Solution:** The symlink to UBP core is missing. Follow step 3 above.

### "ImportError: cannot import name 'CoherenceState'"

**Solution:** You're using an old version of UBP. This study requires **GPU UBP 3.6**.

### Study runs but finds 0 super-rabbits

**Solution:** Check that the NRCI threshold isn't too high. Default is 0.9999992.

### Results file not found

**Solution:** The study hasn't completed yet. Check `study_output.log` for progress.

---

## Next Steps

1. **Run the full study** to completion (1M patterns)
2. **Analyze the top 100 candidates** in detail
3. **Generate structural predictions** for synthesis
4. **Extend the search** to 10M or 100M patterns
5. **Develop mechanism prediction** models
6. **Integrate with experimental validation** pipeline

---

## Support

For questions or issues:
- **GitHub:** [DigitalEuan/UBP_Repo](https://github.com/DigitalEuan/UBP_Repo)
- **Study Location:** `/ubp_antibiotics_study/`

---

## Citation

```bibtex
@article{craig2025ubp_antibiotics,
  title={Discovering Novel Antibiotic Candidates via the Universal Binary Principal Coherence Framework},
  author={Craig, Euan and Manus AI},
  year={2025},
  note={GitHub: DigitalEuan/UBP_Repo/ubp_antibiotics_study}
}
```

---

*Ready to discover antibiotics from the Bitfield!*
