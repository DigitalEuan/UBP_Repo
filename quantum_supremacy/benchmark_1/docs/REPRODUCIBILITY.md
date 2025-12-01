# Reproducibility Guide: UBP Benchmark Study

**Date:** November 25, 2025  
**Author:** E Craig

This document provides complete instructions to reproduce the results of the GPU UBP 3.6 benchmark study.

---

## 1. Environment Setup

### System Requirements
- **OS:** Ubuntu 22.04 or similar Linux distribution
- **Python:** 3.11+
- **Git:** Required to clone the repository

### Clone the Repository
```bash
git clone https://github.com/DigitalEuan/UBP_Repo.git
cd UBP_Repo/bulk/gpu_ubp_study_rigorous
```

### Install Dependencies
```bash
sudo pip3 install taichi qiskit qiskit-aer scipy matplotlib numpy
```

### Set Environment Variables
```bash
export PYTHONPATH="/home/ubuntu/UBP_Repo/gpu_ubp_system/03:/home/ubuntu/UBP_Repo/gpu_ubp_system/03/core:$PYTHONPATH"
```

---

## 2. Running the Benchmarks

All benchmarks are run from the `/home/ubuntu/UBP_Repo/gpu_ubp_system/03/dev_validation` directory.

### Benchmark 1: CHSH Quantum Entanglement

**Command:**
```bash
cd /home/ubuntu/UBP_Repo/gpu_ubp_system/03
python3.11 dev_validation/study_chsh_quantum.py --backend cpu --trials 100 --measurements 2000
```

- **Expected output:** Mean S ≈ -2.83, Mean NRCI ≈ 0.999997
- **Results file:** `chsh_quantum_results.json`

### Benchmark 2: Atomic Balmer Series

**Command:**
```bash
cd /home/ubuntu/UBP_Repo/gpu_ubp_system/03
python3.11 dev_validation/study_atomic_balmer.py
```

- **Expected output:** Mean error ≈ 0.023%, NRCI = 1.000000
- **Results file:** `study_atomic_balmer_results.json`

### Benchmark 3: Multi-Realm Validation

**Command:**
```bash
cd /home/ubuntu/UBP_Repo/gpu_ubp_system/03
python3.11 dev_validation/test_all_realms_complete.py
```

- **Expected output:** All 9 realms pass
- **Results file:** `multi_realm_validation_complete.json`

### Benchmark 4: Scaling Study

**Command:**
```bash
cd /home/ubuntu/UBP_Repo/bulk/gpu_ubp_study_rigorous/benchmarks
./run_scaling_study.py
```

- **Expected output:** Sub-linear scaling, throughput improving with size
- **Results files:** `results/06_scaling_study/`

---

## 3. Analyzing the Results

To generate all summary tables, plots, and analysis, run the comprehensive analysis script:

**Command:**
```bash
cd /home/ubuntu/UBP_Repo/bulk/gpu_ubp_study_rigorous
python3.11 analysis/analyze_all_results.py
```

- **Expected output:** Detailed analysis of all benchmarks, summary tables, and scaling plot
- **Results files:** `analysis/` directory

---

## 4. Expected Outcomes

After running all steps, you should have:

1. **Raw results data** for each benchmark in the `results/` subdirectories
2. **Comprehensive analysis** in the `analysis/` directory, including:
   - `SUMMARY.md` with high-level findings
   - `scaling_analysis.png` visualizing the sub-linear scaling
   - `complete_analysis.json` with all parsed data
3. **Full reproducibility** of all claims made in the research paper.

---

## 5. Troubleshooting

- **`ModuleNotFoundError`:** Ensure the `PYTHONPATH` is set correctly as described in section 1.
- **`Permission denied`:** Make sure scripts are executable (`chmod +x <script_name>`).
- **Qiskit errors:** Ensure Qiskit is installed correctly (`pip3 show qiskit`).

This guide ensures that any researcher can independently verify the findings of this study.
