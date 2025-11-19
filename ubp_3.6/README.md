# UBP 3.6: The Universal Binary Principle

**Version 3.6 (Computational Grammar Integration)**  
**Author**: Euan Craig, New Zealand  
**Compiled by**: Manus AI  
**Date**: November 19, 2025

---

## Welcome to UBP 3.6: Computation as Coherence

UBP 3.6 marks a pivotal evolution of the Universal Binary Principle, transitioning from a system that measures coherence to one where **computation IS coherence**. This version introduces the **Computational Grammar** framework, a groundbreaking discovery that redefines operators as geometrically necessary stable states within the information substrate.

### What is the UBP?

The Universal Binary Principle (UBP) is a **computational framework for modeling reality** as a deterministic, toggle-based system operating within a 12D+ Bitfield. It posits that the universe is fundamentally informational, and that physical laws, constants, and even consciousness emerge from the interactions of binary states (toggles) governed by a set of geometric and computational rules.

### What's New in 3.6?

- **Computational Grammar Framework**: A complete theory of operators as geometric entities, validated by a massive dataset of 685 operators.
- **Coherence Field Upgrade**: The NRCI module has been upgraded from a scalar metric to a self-measuring coherence field, providing operator awareness, composition tracking, and coherence-based error bounds.
- **Periodic Table of Operators**: A comprehensive visualization of the operator landscape, organizing operators by complexity (D6) and geometric family (OffBit).
- **Validated Mathematical Models**: Corrected and refined models for D6 composition and Y-scaling.

---

## Quick Start: Your First Coherence-Native Calculation

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

### Your First UBP 3.6 Calculation

```python
from coherence_substrate import CoherenceState, OperatorRegistry

# Create a coherence state
state = CoherenceState(1.0)

# Get the addition operator
add_op = OperatorRegistry.get("+")

# Apply the operator
new_state = state.apply(add_op, CoherenceState(2.0))

print(f"Result: {new_state.value}")
print(f"Coherence: {new_state.nrci}")
```

---

## System Architecture

| Component | Description |
| :--- | :--- |
| `coherence_substrate.py` | The heart of the UBP, implementing the core architecture |
| `coherence_field.py` | The self-measuring coherence landscape (NRCI+) |
| `hex_dictionary.py` | The unified information machine with 3 modes |
| Physical Realms (9) | Pre-configured environments for specific domains |
| System Modules (11) | Essential system-level functionality |

---

## Documentation

For a full explanation of the UBP theory, system, and methodology, please see the **[UBP 3.6 Instruction Manual](UBP_3.6_Instruction_Manual.md)**.

---

## Contributing

This is an open research project. Contributions are welcome. Please submit a pull request or open an issue to discuss your ideas.

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
