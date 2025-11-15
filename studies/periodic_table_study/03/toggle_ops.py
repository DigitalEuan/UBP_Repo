================================================================================
Universal Binary Principle (UBP) Framework v3.5 - Toggle Operations
Author: Euan Craig, New Zealand
Date: November 12, 2025
================================================================================

Toggle operations as coherence transformations.

**Paradigm Shift in 3.5**:
Toggle operations aren't bit manipulations - they're coherence transformations.
Every toggle operation maintains and transforms the coherence state.

**Zero Dependencies**: Only Python stdlib + coherence_substrate + state
"""

import math
from typing import List, Union, Tuple
from state import OffBit
from coherence_substrate import CoherenceState, Y


# ============================================================================
# BASIC TOGGLE OPERATIONS (Coherence-Preserving)
# ============================================================================

def toggle_and(b_i: OffBit, b_j: OffBit) -> OffBit:
    """
    Perform AND toggle operation (coherence-preserving).
    
    Axiom: min(b_i, b_j)
    Coherence: Combined coherence of both inputs
    
    Args:
        b_i: First OffBit
        b_j: Second OffBit
        
    Returns:
        Result OffBit with combined coherence
        
    Example:
        >>> b1 = OffBit(0x123456)
        >>> b2 = OffBit(0xABCDEF)
        >>> result = toggle_and(b1, b2)
    """
    result_value = min(b_i.value, b_j.value)
    
    # Combine coherence states (multiply for AND - both must be coherent)
    combined_coherence = CoherenceState(
        result_value,