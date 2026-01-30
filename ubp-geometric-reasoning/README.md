# UBP Skill: Geometric Rational Reasoning

**Version:** 1.0  
**Author:** E. R. A. Craig / Manus AI  
**Date:** January 30, 2026

## Overview

The **UBP Geometric Rational Reasoning** skill is a complete, production-ready implementation of the Universal Binary Principle (UBP) system for deterministic, float-free geometric reasoning. It provides AI agents and researchers with a rigorous framework for topological navigation within the 24-dimensional Leech Lattice, leveraging the error-correcting properties of the Golay code.

This skill is designed for use within the Manus AI environment and can be integrated into the UBP Core Studio or used as a standalone reasoning engine.

## Key Features

- **Complete Implementation:** No simplifications, placeholders, or mock objects. Every component is a faithful implementation of the UBP system.
- **Float-Free Mathematics:** All operations use Python's `fractions.Fraction` for absolute precision.
- **Deterministic Reasoning:** Hash-based seeding ensures reproducible results.
- **Self-Aware Cortex:** Includes an embedded observer that recursively evaluates system state and rejects geometric hallucinations.
- **Comprehensive Validation:** Includes a 28-test validation suite that verifies all capabilities.

## Structure

```
ubp-geometric-reasoning/
├── SKILL.md                  # Skill documentation and usage examples
├── README.md                 # This file
├── scripts/                  # Core UBP scripts and main interface
│   ├── ubp_geometric_reasoning_main.py  # Main interface (8 capabilities)
│   ├── ubp_skill_validator.py           # Validation suite (28 tests)
│   ├── ubp_core_v4_2_6_COMBINED.py      # Golay, Leech, Particle Physics
│   ├── ubp_rational_engine.py           # Concept minting
│   ├── ubp_tgic_engine.py               # Dynamics engine
│   ├── hex_dictionary_v4_exact.py       # Vector lookup
│   ├── auto_trigger.py                  # Memory retrieval
│   ├── ubp_integrated_engine_v1.py      # Self-aware cortex
│   ├── ubp_nrci_calculator.py           # Coherence calculation
│   ├── ubp_integration_adapter.py       # Module coordination
│   ├── metrics_exact.py                 # Geometric metrics
│   └── rational_cortex.json             # Knowledge base
├── references/               # Reference documentation for AI/users
│   ├── ubp_laws.md           # Core UBP laws
│   ├── octad_guide.md        # 8 geometric domains
│   └── research_protocol.md  # 5-phase validation workflow
└── templates/                # JSON templates
    ├── concept_template.json
    └── kb_entry_template.json
```

## Installation

1. Clone or copy the `ubp-geometric-reasoning` directory to your Manus skills folder:
   ```bash
   cp -r ubp-geometric-reasoning /path/to/manus/skills/
   ```

2. Ensure Python 3.10+ is installed.

3. No additional dependencies are required—all UBP core modules are bundled.

## Quick Start

```python
from scripts.ubp_geometric_reasoning_main import get_reasoning_engine

# Initialize the engine
ubp = get_reasoning_engine()

# Example 1: Vectorize a concept
result = ubp.vectorize_concept("Energy")
print(f"Vector: {result['vector']}")
print(f"Domain: {result['domain']}")
print(f"NRCI: {result['nrci']:.4f}")

# Example 2: Reason about a query
result = ubp.reason_about("What is the nature of time?")
print(f"Status: {result['status']}")
print(f"Resonance: {result['resonance']}")

# Example 3: Calculate coherence
vector = [1, 0, 1, 0] * 6  # 24-bit vector
coherence = ubp.calculate_coherence(vector)
print(f"NRCI: {coherence['nrci']:.4f}")
print(f"Regime: {coherence['regime']}")
```

## Eight Key Capabilities

| Capability | Description |
|---|---|
| `vectorize_concept(concept)` | Convert concepts to 24-bit vectors via SHA-256 + Golay encoding |
| `reason_about(query)` | Execute full reasoning pipeline with Observer validation |
| `find_counterpart(concept, domain)` | Find geometric equivalents across Octad domains |
| `calculate_coherence(vector)` | Deep NRCI and tetradic health analysis |
| `snap_to_lattice(noisy_vector)` | Apply reflexive error correction |
| `query_memory(search_term)` | Hash-based O(1) retrieval with Hamming clustering |
| `validate_concept(concept_data)` | Run 5-phase research protocol |
| `archive_to_kb(concept_data)` | Format concepts for knowledge base archival |

## Validation

Run the comprehensive validation suite to verify system integrity:

```bash
cd scripts
python3.11 ubp_skill_validator.py
```

**Expected Output:**
```
================================================================================
VALIDATION SUMMARY
================================================================================
  Total Tests: 28
  Passed: 28 ✓
  Failed: 0 ✗

  ✓ ALL TESTS PASSED - SKILL IS READY FOR USE
================================================================================
```

## Documentation

- **SKILL.md**: Complete skill documentation with usage examples
- **references/ubp_laws.md**: Core laws of the UBP system
- **references/octad_guide.md**: The 8 geometric domains of existence
- **references/research_protocol.md**: 5-phase validation workflow

## Integration with UBP Core Studio

This skill can be integrated into the UBP Core Studio v4.2.7 by:

1. Copying the `scripts/` directory contents to the Core Studio's `core/` folder
2. Importing the main interface in your Studio scripts:
   ```python
   from ubp_geometric_reasoning_main import get_reasoning_engine
   ```

## License & Attribution

This skill is based on the Universal Binary Principle (UBP) system developed by E. R. A. Craig, New Zealand.

## Version History

- **v1.0** (January 30, 2026): Initial release with all 8 capabilities and 28 validation tests
