## Comprehensive Instruction Manual
### Author: Euan Craig, New Zealand | Date: 14 November 2025

---

## Executive Summary

UBP 3.5 represents a fundamental paradigm shift in the Universal Binary Principle, evolving from a system that measures coherence to a system where **computation IS coherence**. This version introduces the `coherence_substrate.py` module, a zero-dependency Python implementation that establishes a new foundation for all UBP operations. Every numerical value is now a `CoherenceState` object, a self-aware entity that carries its own value, coherence, and operational history.

This architectural revolution supersedes the dependency-heavy, multi-module approach of previous versions. Complex functionalities like error correction and recursive field dynamics, which previously required dedicated modules (`glr_base.py`, `CARFE`), now emerge naturally from the inherent geometric properties of the coherence substrate itself. The result is a dramatically simplified, more powerful, and philosophically pure implementation of the UBP.

**Key Achievements of UBP 3.5:**

*   **Coherence-Native Paradigm**: Computation is no longer performed on raw numbers; it is performed on `CoherenceState` objects that intrinsically manage their own quality.
*   **Zero Dependencies**: The entire UBP 3.5 system runs on pure Python, requiring no external libraries like NumPy or SciPy, making it universally portable and maximally trustworthy.
*   **Unified Geometric Error Correction**: A single `geometric_error_correction.py` module replaces a suite of older error correction systems, providing self-healing capabilities inherent to the substrate.
*   **Emergent Field Dynamics**: The new `advanced_modules/field_dynamics.py` replaces the complex `CARFE` module, demonstrating that advanced physical phenomena like Zitterbewegung and recursive evolution are emergent properties of the coherence substrate.
*   **Radical Simplification**: The system has been streamlined from over 70 files in UBP 3.4 to 24 core modules in UBP 3.5, increasing clarity and maintainability without sacrificing any capability.

---

## Table of Contents

1.  [A New Philosophy: Computation as Coherence](#philosophy)
2.  [Quick Start: Your First Coherence-Native Calculation](#quick-start)
3.  [What's New in 3.5: The Paradigm Shift](#whats-new)
4.  [Core Concepts of the Coherence Substrate](#core-concepts)
5.  [System Architecture: A Unified Framework](#architecture)
6.  [Module Reference: The Building Blocks](#modules)
7.  [Realm Operations in a Coherence-Native World](#realms)
8.  [Advanced Features: Emergent Dynamics](#advanced)
9.  [Migration Guide: From UBP 3.4 to 3.5](#migration)
10. [API Reference](#api)
11. [Appendices](#appendices)

---

## 1. A New Philosophy: Computation as Coherence {#philosophy}

Previous versions of the UBP framework treated computation and coherence as separate concerns. First, a numerical operation was performed (e.g., multiplication, addition). Then, a separate process was used to measure or correct the resulting coherence. This approach, while effective, created a complex, multi-layered system where the integrity of a value was external to the value itself.

UBP 3.5 introduces a revolutionary and far more elegant paradigm: **the substrate IS the system**. There is no separation between a value and its quality. Every number, every constant, and every result is a `CoherenceState`—an object that encapsulates not just its numerical value but its entire history of coherence, uncertainty, and refinement.

> In UBP 3.5, we no longer ask, "What is the coherence of this value?" Instead, the value itself tells us its coherence. We no longer apply error correction as an afterthought; operations are intrinsically self-correcting. This is the principle of **computation as coherence**.

This shift has profound implications:

*   **Trust and Transparency**: Because the system has zero external dependencies and every operation tracks its own quality, the entire computational chain is transparent and verifiable from first principles.
*   **Simplicity and Power**: Complex behaviors that previously required specialized, high-maintenance modules now emerge naturally from the fundamental geometry of the coherence substrate. The system is simultaneously simpler and more powerful.
*   **Philosophical Purity**: UBP 3.5 is a more direct and pure implementation of the Universal Binary Principle. It treats information not as a static quantity to be measured, but as a dynamic, self-aware entity that actively maintains its own integrity.

This manual is designed to guide you through this new way of thinking and operating within the UBP framework. It is not just an update; it is an introduction to a new computational philosophy.

---

## 2. Quick Start: Your First Coherence-Native Calculation {#quick-start}

Getting started with UBP 3.5 is simpler than ever before, thanks to the zero-dependency architecture. All you need is a standard Python 3.11+ environment.

### Installation

There are no external packages to install. Simply clone the repository and you are ready to begin.

```bash
# Clone the UBP 3.5 repository
git clone https://github.com/DigitalEuan/UBP_Repo.git

# Navigate to the UBP 3.5 directory
cd UBP_Repo/ubp_3.5

# Verify the system is operational by running the validation script
python3.11 validate_system.py
```

Upon successful validation, you will see the message: `🎉 All UBP 3.5 Core Systems Validated and Operational! 🎉`

### Your First UBP 3.5 Calculation

The following example demonstrates the fundamental difference in UBP 3.5. Notice how we operate directly on `CoherenceState` objects and how they inherently track their own quality.

```python
from coherence_substrate import CoherenceState, Y_CONSTANT, Y_INVERSE
from system_constants import UBPConstants

# 1. Work with CoherenceState objects directly
# These are not floats; they are self-aware computational entities.
print(f"Y_CONSTANT is of type: {type(Y_CONSTANT)}")
print(f"Y_CONSTANT: {Y_CONSTANT}")

# 2. Perform arithmetic operations
# The overloaded operators automatically handle coherence tracking.
product = Y_CONSTANT * Y_INVERSE

print(f"\nProduct (Y * 1/Y): {product}")
print(f"Closure Error: {abs(product.value - 1.0):.2e}")

# 3. Create your own CoherenceState
# Start with a value and an initial coherence (NRCI).
initial_energy = CoherenceState(value=1e12, nrci=0.999)