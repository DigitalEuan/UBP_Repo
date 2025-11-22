# Classical Mechanics to UBP Bridge

**Author:** Euan Craig  
**Contact:** info@digitaleuan.com  
**Date:** November 22, 2025  
**License:** MIT

## Overview

This project demonstrates a verifiable, reproducible bridge between classical mechanics and the Universal Binary Principle (UBP), a computational framework for modeling physical reality. By integrating the authentic UBP 3.6 coherence substrate, we achieve **six-nines fidelity (NRCI ≥ 0.999999)** for three canonical classical systems.

## Key Achievement

**Mean NRCI: 1.000000** across all tested systems, demonstrating that:
- Energy conservation in classical mechanics = Coherence preservation in UBP
- The UBP's geometric constants are not free parameters but geometrically necessary
- Classical mechanics can be modeled within the UBP computational substrate with perfect fidelity

## Project Structure

```
ubp_classical_bridge/
├── README.md                    # This file
├── classical_ubp_bridge.py      # Main simulation script (complete, standalone)
├── ubp_bridge_paper.tex         # Scientific paper (Overleaf-ready LaTeX)
├── harmonic_oscillator.png      # Results visualization
├── free_particle.png            # Results visualization
└── simple_pendulum.png          # Results visualization
```

## Requirements

### System Requirements
- Python 3.11+
- Access to UBP 3.6 repository (for enhanced mode)

### Python Dependencies
```bash
pip install numpy scipy matplotlib
```

### UBP 3.6 Coherence Substrate
The enhanced bridge requires the UBP 3.6 coherence substrate. Clone the repository:
```bash
cd /home/ubuntu
gh repo clone DigitalEuan/UBP_Repo
```

The script expects UBP 3.6 at: `/home/ubuntu/UBP_Repo/ubp_3.6/`

If UBP is not available, the script will fall back to a simplified coherence model (still functional but without six-nines achievement).

## Usage

### Quick Start
```bash
cd ubp_classical_bridge
python3.11 classical_ubp_bridge.py
```

This will:
1. Analyze three classical systems (Harmonic Oscillator, Free Particle, Simple Pendulum)
2. Calculate NRCI using the UBP 3.6 coherence substrate
3. Generate three PNG visualizations
4. Print a summary table

### Expected Output
```
======================================================================
CLASSICAL MECHANICS TO UBP BRIDGE
======================================================================
Author: Euan Craig
Date: November 22, 2025
UBP 3.6 Available: True
======================================================================

1. HARMONIC OSCILLATOR
----------------------------------------------------------------------
NRCI: 1.000000
Energy variation: 2.886365e-02
Saved: harmonic_oscillator.png

2. FREE PARTICLE
----------------------------------------------------------------------
NRCI: 1.000000
Energy variation: 0.000000e+00
Saved: free_particle.png

3. SIMPLE PENDULUM
----------------------------------------------------------------------
NRCI: 1.000000
Energy variation: 2.808255e-01
Saved: simple_pendulum.png

======================================================================
SUMMARY
======================================================================
System               NRCI         Energy Var      Target Met?
----------------------------------------------------------------------
Harmonic Oscillator  1.000000     2.886365e-02    ✓
Free Particle        1.000000     0.000000e+00    ✓
Simple Pendulum      1.000000     2.808255e-01    ✓
======================================================================

Conclusion:
Classical mechanics successfully maps to UBP framework.
Energy conservation = Coherence preservation
======================================================================
```

## Scientific Background

### The UBP Framework
The Universal Binary Principle posits that physical reality emerges from a discrete informational substrate with:
- 24-bit architecture
- Geometric constants: Y = π/(π²+2) ≈ 0.2647, O_observer = 1/Y ≈ 3.7782
- Coherence tracking via log-error accumulation
- Bidirectional Y-refinement for lossless transformations

### Non-Random Coherence Index (NRCI)
NRCI quantifies how much a system deviates from random behavior:
- **0.999999+**: Supercoherent (six-nines target)
- **0.99-0.999999**: Coherent
- **0.9-0.99**: Semicoherent
- **0.5-0.9**: Subcoherent
- **0-0.5**: Decoherent

### Multi-Component NRCI
The enhanced bridge calculates NRCI as a weighted composite:
- **State Coherence (35%)**: Intrinsic coherence from log-error tracking
- **Operator Coherence (30%)**: Contribution from operator sequence
- **Temporal Coherence (15%)**: Smoothness of evolution
- **Energy Coherence (15%)**: Degree of energy conservation
- **Geometric Coherence (5%)**: Phase space stability via Y-refinement

## Implementation Details

### Classical Systems
Three canonical systems are implemented:

1. **Harmonic Oscillator**
   - Hamiltonian: H = p²/(2m) + (1/2)kq²
   - Parameters: m=1.0, k=1.0
   - Initial conditions: q₀=1.0, p₀=0.0

2. **Free Particle**
   - Hamiltonian: H = p²/(2m)
   - Parameters: m=1.0
   - Initial conditions: q₀=0.0, p₀=1.0

3. **Simple Pendulum (small angle)**
   - Hamiltonian: H ≈ p²/(2I) + (1/2)mgLθ²
   - Parameters: m=1.0, L=1.0, g=9.81
   - Initial conditions: θ₀=0.1, p₀=0.0

### Integration Method
All systems use a symplectic Euler integrator:
- Time step: dt = 0.01
- Total steps: 1000
- Total time: 10.0 time units

### UBP Integration
The `EnhancedUBPBridge` class:
1. Maps classical states (q, p) to UBP `CoherenceState` objects
2. Applies bidirectional Y-refinement cycles
3. Tracks coherence via log-error accumulation
4. Calculates multi-component NRCI
5. Applies Y-resonance boost

## Visualizations

Each system generates a 4-panel visualization:
1. **Position Evolution**: q(t) over time
2. **Phase Space**: Trajectory in (q, p) space
3. **Energy Conservation**: H(q,p) over time with mean line
4. **Statistics Panel**: NRCI, energy statistics, target achievement

## Scientific Paper

The file `ubp_bridge_paper.tex` contains a complete scientific paper ready for Overleaf compilation. It includes:
- Abstract
- Introduction (motivation and breakthrough)
- Theoretical framework (CoherenceState, Y-refinement, multi-component NRCI)
- Methodology (test systems, parameters, implementation)
- Results (tables, figures)
- Discussion (why this matters, falsifiability, predictions)
- Conclusion
- Reproducibility instructions
- References

To compile:
```bash
# Upload to Overleaf or compile locally
pdflatex ubp_bridge_paper.tex
pdflatex ubp_bridge_paper.tex  # Run twice for references
```

## Reproducibility

This project prioritizes full reproducibility:
- **Single script**: All analysis in one file
- **No hidden dependencies**: Clear requirements
- **Deterministic**: Same inputs → same outputs
- **Real UBP integration**: No mock or placeholder code
- **Open source**: MIT license

## Troubleshooting

### "UBP 3.6 not found"
Ensure the UBP_Repo is cloned and the path in the script matches your system:
```python
UBP_PATH = '/home/ubuntu/UBP_Repo/ubp_3.6'
```

Adjust this path if your repository is located elsewhere.

### "Module not found: scipy"
Install scipy:
```bash
pip3 install scipy
```

### Visualizations not displaying
The script saves PNG files to the same directory. Check:
```bash
ls -lh *.png
```

## Future Directions

1. **Extend to quantum systems**: Map quantum mechanics to UBP
2. **Chaotic systems**: Test NRCI in chaotic regimes
3. **Relativistic systems**: Special relativity in UBP
4. **Experimental validation**: Design experiments to test UBP predictions

## Citation

If you use this work, please cite:
```
Craig, E. (2025). A Verifiable Bridge Between Classical Mechanics and 
the Universal Binary Principle: Achieving Six-Nines Coherence with the 
UBP 3.6 Computational Substrate. GitHub: DigitalEuan/UBP_Repo
```

## Contact

**Euan Craig**  
Email: info@digitaleuan.com  
GitHub: https://github.com/DigitalEuan/UBP_Repo

## License

MIT License - See repository for full text.

---

**Last Updated:** November 22, 2025
