# Cell 38 from UBP_UNIFIED_SYSTEM_1.ipynb

# @title
#!/usr/bin/env python3
"""
================================================================================
UBP UNIFIED SYSTEM: Golay G₂₄ + Leech Λ₂₄ + Geometric Integration
================================================================================

The Universal Binary Principle (UBP) System - First Principles Implementation
Author: Euan R A Craig, New Zealand
Date: 11 December 2025

MISSION: Real, exact, no simplification. No floats in calculations.
- Golay G₂₄ error correction (0-3 bits) with geometric spring mechanism
- Leech Λ₂₄ lattice coherence validation
- Bidirectional Observable ↔ Information-First flow
- Real data encoding/transmission with error correction

NO NUMPY. Pure Python. Exact integer/half-integer arithmetic throughout.
================================================================================
"""

from typing import Tuple, List, Optional, Dict, Union
from dataclasses import dataclass
import random
from fractions import Fraction


# ============================================================================
# SECTION 1: PURE PYTHON ARITHMETIC & MATRIX OPERATIONS
# ============================================================================
# No floats in calculations. Exact integer/half-integer arithmetic.

class ExactNumber:
    """
    Represents exact numbers as integers or half-integers.
    Internally stored as 2*value to maintain integer arithmetic.
    """
    def __init__(self, value: Union[int, float, Fraction, 'ExactNumber']):
        if isinstance(value, ExactNumber):
            self.doubled = value.doubled
        elif isinstance(value, Fraction):
            # Fraction with denominator 2
            if value.denominator == 1:
                self.doubled = value.numerator * 2
            elif value.denominator == 2:
                self.doubled = value.numerator
            else:
                raise ValueError(f