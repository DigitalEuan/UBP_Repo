# UBP 3.6 Core Engine (Frozen Reference)

This directory contains a frozen snapshot of the UBP 3.6 core modules used by the visual proof generators.

## Purpose

These files serve as a **verified, stable reference** for the visual proofs. They are copied from `../../ubp_3.6/` to ensure:

1. **Reproducibility** - The visualizations will always use the same UBP version
2. **Transparency** - Anyone can inspect the exact code used
3. **Independence** - Visual proofs package is self-contained

## Files

- `coherence_substrate.py` - Core coherence state and Y-refinement implementation
- `state.py` - OffBit state representation
- `toggle_ops.py` - Toggle operations (AND, OR, XOR, resonance)
- `tgic.py` - Toggle Grammar Interaction Constraints
- Additional UBP 3.6 modules as needed

## Version

**UBP Version:** 3.6.0  
**Date:** November 2025  
**Author:** Euan R A Craig, New Zealand

## Usage

The visualizer scripts import from this directory to ensure consistency:

```python
import sys
sys.path.insert(0, '../core_engine')

from coherence_substrate import CoherenceState, Y, NRCI_TARGET
from state import OffBit
from toggle_ops import resonance_toggle
```

## Do Not Modify

These files are **frozen** for this visual proofs package. Any updates to UBP 3.6 should be made in the main `../../ubp_3.6/` directory, and a new visual proofs package should be created if needed.
