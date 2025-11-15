================================================================================
Universal Binary Principle (UBP) Framework v3.5 - State Management
Author: Euan Craig, New Zealand
Date: November 12, 2025
================================================================================

UBP State management with coherence-native OffBits.

**Paradigm Shift in 3.5**:
OffBits now carry their own coherence state. Every bit operation maintains
coherence tracking, making state management inherently coherence-aware.

**Zero Dependencies**: Only Python stdlib + coherence_substrate
"""

import math
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass
from coherence_substrate import CoherenceState, NRCI_TARGET


# ============================================================================
# OFFBIT - Coherence-Native 24-bit State
# ============================================================================

@dataclass(frozen=True)
class OffBit:
    """
    Immutable 24-bit UBP OffBit with intrinsic coherence.
    
    In 3.5, OffBits aren't just bit patterns - they're coherence states
    that happen to have a 24-bit representation.
    """
    value: int  # 24-bit value (0 to 0xFFFFFF)
    coherence: CoherenceState = None
    
    def __post_init__(self):
        # Ensure value is within 24-bit range
        if not (0 <= self.value <= 0xFFFFFF):
            object.__setattr__(self, 'value', self.value & 0xFFFFFF)
        
        # Initialize coherence if not provided
        if self.coherence is None:
            object.__setattr__(self, 'coherence', CoherenceState(
                float(self.value),
                log_nrci_error=math.log(1 - NRCI_TARGET)
            ))
    
    @property
    def layer(self) -> int:
        """Get the 24-bit layer value."""
        return self.value & 0xFFFFFF
    
    @property
    def bits(self) -> List[int]:
        """Get individual bits as a list."""
        return [(self.value >> i) & 1 for i in range(24)]
    
    @property
    def active_bits(self) -> int:
        """Count of active (1) bits."""
        return bin(self.value).count('1')
    
    @property
    def is_active(self) -> bool:
        """Check if OffBit has any active bits."""
        return self.value > 0
    
    @property
    def nrci(self) -> float:
        """Get NRCI of this OffBit."""
        return self.coherence.nrci
    
    def toggle(self) -> 'OffBit':
        """
        Create a new OffBit with toggled state.
        
        Toggling is a coherence transformation - it applies Y-refinement.
        
        Returns:
            New OffBit with inverted bits and refined coherence
        """
        new_value = self.value ^ 0xFFFFFF
        new_coherence = self.coherence.refine_forward()
        return OffBit(new_value, new_coherence)
    
    def toggle_bit(self, position: int) -> 'OffBit':
        """
        Create a new OffBit with a specific bit toggled.
        
        Args:
            position: Bit position to toggle (0-23)
        
        Returns:
            New OffBit with specified bit toggled
        """
        if not (0 <= position < 24):
            raise ValueError(f"Bit position {position} out of range [0, 23]")
        