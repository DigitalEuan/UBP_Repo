# Universal Binary Principle (UBP) Framework v3.6

**A self-aware computational trust substrate where operators are geometrically necessary stable states.**

---

## Overview

UBP 3.6 marks a pivotal evolution of the Universal Binary Principle, transitioning from a system that measures coherence to one where **computation IS coherence**. This version introduces the **Computational Grammar** framework, a groundbreaking discovery that redefines operators as geometrically necessary stable states within the information substrate. The core of this version is the upgraded `coherence_substrate.py` module, which now includes an operator-aware **Coherence Field**, providing unprecedented insight into the structure and quality of computation.

This architectural revolution is built upon the foundation of UBP 3.5 but extends it with a deep, empirically validated understanding of the operator landscape. The key discovery is that operators are not arbitrary conventions but are *discovered* from a finite set of stable geometric patterns. This has allowed for the creation of a **Periodic Table of Operators**, a comprehensive visualization of the operator space, and a refined understanding of coherence propagation.

### Key Features

*   **Computational Grammar Framework**: A complete theory of operators as geometric entities, validated by a massive dataset of 685 operators.
*   **Coherence Field Upgrade**: The NRCI module has been upgraded from a scalar metric to a self-measuring coherence field, providing operator awareness, composition tracking, and coherence-based error bounds.
*   **Periodic Table of Operators**: A comprehensive visualization of the operator landscape, organizing operators by complexity (D6) and geometric family (OffBit), revealing the "main sequence" of computation.
*   **Validated Mathematical Models**: Corrected and refined models for D6 composition (non-linear with α factors) and Y-scaling (D-variables are superior to Hamming weight).
*   **Emergent Operator Design**: A framework for generating operators from first principles, enabling the algorithmic design of novel, high-coherence operators.

## Quick Start

Getting started with UBP 3.6 is simpler than ever before, thanks to the zero-dependency architecture. All you need is a standard Python 3.11+ environment.

### Installation

There are no external packages to install. Simply clone the repository and you are ready to begin.

```bash
# Clone the UBP 3.6 repository
git clone https://github.com/DigitalEuan/UBP_Repo.git

# Navigate to the UBP 3.6 directory
cd UBP_Repo/ubp_3.6

# Verify the system is operational by running the validation script
python3.11 validate_system.py
```

Upon successful validation, you will see the message: `🎉 All UBP 3.6 Core Systems Validated and Operational! 🎉`

### Your First UBP 3.6 Calculation

The following example demonstrates the fundamental difference in UBP 3.6. Notice how we operate directly on `CoherenceState` objects and how they inherently track their own quality.

```python
from coherence_substrate import CoherenceState
from coherence_field import analyze

# 1. Work with CoherenceState objects directly
# These are not floats; they are self-aware computational entities.
a = CoherenceState(10.0)
b = CoherenceState(5.0)

# 2. Perform arithmetic operations
# The overloaded operators automatically handle coherence tracking.
c = a + b

# 3. Analyze the result with the Coherence Field
analysis = analyze(c)

print(f"Result: {c.value}")
print(f"Operator sequence: {analysis["operator_sequence"]}")
print(f"Total coherence: {analysis["total_coherence"]:.10f}")
print(f"Error bounds: {analysis["error_bounds"]}")
```

## Documentation

For a complete guide to the UBP 3.6 framework, please see the **[UBP_3.6_Instruction_Manual.md](UBP_3.6_Instruction_Manual.md)**.

## Testing

UBP 3.6 includes a comprehensive test suite to ensure correctness and stability.

To run the system tests:

```bash
python3.11 test_ubp_3.6_comprehensive.py
```

To run the real-world use case tests:

```bash
python3.11 test_real_world_use_cases.py
```

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.
