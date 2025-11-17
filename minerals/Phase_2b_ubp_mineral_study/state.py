"""
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
        
        new_value = self.value ^ (1 << position)
        # Small toggle = small coherence change
        new_coherence = self.coherence.degrade_by(1e-8)
        return OffBit(new_value, new_coherence)
    
    def get_bit(self, position: int) -> int:
        """
        Get the value of a specific bit.
        
        Args:
            position: Bit position (0-23)
        
        Returns:
            Bit value (0 or 1)
        """
        if not (0 <= position < 24):
            raise ValueError(f"Bit position {position} out of range [0, 23]")
        
        return (self.value >> position) & 1
    
    def set_bit(self, position: int, bit_value: int) -> 'OffBit':
        """
        Create a new OffBit with a specific bit set.
        
        Args:
            position: Bit position (0-23)
            bit_value: Bit value (0 or 1)
        
        Returns:
            New OffBit with specified bit set
        """
        if not (0 <= position < 24):
            raise ValueError(f"Bit position {position} out of range [0, 23]")
        if bit_value not in (0, 1):
            raise ValueError(f"Bit value must be 0 or 1, got {bit_value}")
        
        if bit_value == 1:
            new_value = self.value | (1 << position)
        else:
            new_value = self.value & ~(1 << position)
        
        new_coherence = self.coherence.degrade_by(1e-8)
        return OffBit(new_value, new_coherence)
    
    def extract_data(self) -> int:
        """
        Extract 24-bit data.
        
        Returns:
            24-bit data value
        """
        return self.layer
    
    def __str__(self) -> str:
        return f"OffBit(0x{self.value:06X}, NRCI={self.nrci:.6f})"
    
    def __repr__(self) -> str:
        return f"OffBit(value={self.value}, layer=0x{self.layer:06X}, active_bits={self.active_bits}, nrci={self.nrci:.10f})"


# ============================================================================
# BITFIELD - Collection of Coherent OffBits
# ============================================================================

class MutableBitfield:
    """
    Mutable bitfield for UBP operations with coherence tracking.
    
    In 3.5, a bitfield isn't just a collection of bits - it's a
    coherence ensemble where collective coherence emerges.
    """
    
    def __init__(self, size: int = 1000):
        """
        Initialize mutable bitfield.
        
        Args:
            size: Number of OffBits to store
        """
        self.size = size
        self.offbits: List[OffBit] = [OffBit(0) for _ in range(size)]
        self._modification_count = 0
    
    def get(self, index: int) -> OffBit:
        """Get OffBit at index."""
        if not (0 <= index < self.size):
            raise IndexError(f"Index {index} out of range [0, {self.size})")
        return self.offbits[index]
    
    def set(self, index: int, offbit: OffBit):
        """Set OffBit at index."""
        if not (0 <= index < self.size):
            raise IndexError(f"Index {index} out of range [0, {self.size})")
        self.offbits[index] = offbit
        self._modification_count += 1
    
    def toggle(self, index: int):
        """Toggle OffBit at index."""
        self.offbits[index] = self.offbits[index].toggle()
        self._modification_count += 1
    
    def get_collective_coherence(self) -> CoherenceState:
        """
        Get collective coherence of the entire bitfield.
        
        Returns:
            CoherenceState representing ensemble coherence
        """
        if not self.offbits:
            return CoherenceState(0.0)
        
        # Average coherence across all OffBits
        total_value = sum(ob.coherence.value for ob in self.offbits)
        avg_value = total_value / len(self.offbits)
        
        total_log_error = sum(ob.coherence.log_nrci_error for ob in self.offbits)
        avg_log_error = total_log_error / len(self.offbits)
        
        return CoherenceState(avg_value, log_nrci_error=avg_log_error)
    
    def get_active_count(self) -> int:
        """Count of active OffBits."""
        return sum(1 for ob in self.offbits if ob.is_active)
    
    def get_total_active_bits(self) -> int:
        """Total count of active bits across all OffBits."""
        return sum(ob.active_bits for ob in self.offbits)
    
    def __len__(self) -> int:
        return self.size
    
    def __str__(self) -> str:
        collective = self.get_collective_coherence()
        return f"MutableBitfield(size={self.size}, active={self.get_active_count()}, nrci={collective.nrci:.6f})"


# ============================================================================
# UBP STATE - Complete System State
# ============================================================================

@dataclass
class UBPState:
    """
    Complete UBP system state with coherence tracking.
    
    In 3.5, system state is fundamentally a coherence configuration.
    """
    bitfield: MutableBitfield
    timestamp: float
    metadata: Dict[str, Any]
    
    @classmethod
    def create(cls, size: int = 1000, **metadata) -> 'UBPState':
        """
        Create a new UBPState.
        
        Args:
            size: Bitfield size
            **metadata: Additional metadata
        
        Returns:
            New UBPState
        """
        import time
        return cls(
            bitfield=MutableBitfield(size),
            timestamp=time.time(),
            metadata=metadata
        )
    
    def get_system_coherence(self) -> CoherenceState:
        """Get overall system coherence."""
        return self.bitfield.get_collective_coherence()
    
    def get_state_summary(self) -> Dict[str, Any]:
        """
        Get summary of system state.
        
        Returns:
            Dictionary with state statistics
        """
        coherence = self.get_system_coherence()
        
        return {
            'bitfield_size': self.bitfield.size,
            'active_offbits': self.bitfield.get_active_count(),
            'total_active_bits': self.bitfield.get_total_active_bits(),
            'system_nrci': coherence.nrci,
            'system_value': coherence.value,
            'timestamp': self.timestamp,
            'metadata': self.metadata
        }
    
    def __str__(self) -> str:
        coherence = self.get_system_coherence()
        return f"UBPState(size={self.bitfield.size}, nrci={coherence.nrci:.6f})"


# ============================================================================
# DEMONSTRATION
# ============================================================================

if __name__ == "__main__":
    print("=" * 80)
    print("UBP 3.5 STATE MANAGEMENT - Coherence-Native OffBits")
    print("=" * 80)
    
    # Create OffBit
    print("\n1. Creating OffBit:")
    offbit = OffBit(0x123456)
    print(f"   {offbit}")
    print(f"   Active bits: {offbit.active_bits}")
    print(f"   NRCI: {offbit.nrci:.10f}")
    
    # Toggle operations
    print("\n2. Toggle Operations:")
    toggled = offbit.toggle()
    print(f"   Original: {offbit}")
    print(f"   Toggled:  {toggled}")
    print(f"   NRCI change: {toggled.nrci - offbit.nrci:.10f}")
    
    # Bit operations
    print("\n3. Bit Operations:")
    bit_toggled = offbit.toggle_bit(5)
    print(f"   Bit 5 toggled: {bit_toggled}")
    print(f"   Bit 5 value: {bit_toggled.get_bit(5)}")
    
    # Bitfield
    print("\n4. Mutable Bitfield:")
    bitfield = MutableBitfield(size=100)
    for i in range(10):
        bitfield.set(i, OffBit(i * 0x1000))
    
    collective = bitfield.get_collective_coherence()
    print(f"   {bitfield}")
    print(f"   Collective NRCI: {collective.nrci:.10f}")
    print(f"   Active OffBits: {bitfield.get_active_count()}")
    
    # UBP State
    print("\n5. UBP System State:")
    state = UBPState.create(size=1000, realm='quantum', experiment='test')
    summary = state.get_state_summary()
    print(f"   {state}")
    print(f"   Summary: {summary}")
    
    print("\n" + "=" * 80)
    print("UBP 3.5: OffBits are Coherence States")
    print("Zero external dependencies - Pure coherence")
    print("=" * 80)
