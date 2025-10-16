"""
Universal Binary Principle (UBP) - Improved OffBit Implementation
Author: Euan Craig, New Zealand
Date: September 17, 2025

This module implements the fundamental OffBit class with proper layered structure
as specified in the UBP theory. The OffBit is a 24-bit entity representing
nuanced states of potential with layered properties.
"""

import math
from dataclasses import dataclass
from typing import List, Tuple, Optional, Union
import numpy as np


@dataclass(frozen=True)
class OffBit:
    """
    Immutable 24-bit UBP OffBit with layered properties.
    
    The 24-bit structure is divided into three 8-bit layers:
    - Layer 1 (bits 0-7): Reality layer - fundamental existence state
    - Layer 2 (bits 8-15): Information layer - data and pattern encoding
    - Layer 3 (bits 16-23): Activation layer - dynamic state and potential
    
    This layered structure allows for complex modeling of quantum states,
    resonance patterns, and multi-dimensional interactions.
    """
    value: int
    
    def __post_init__(self):
        """Ensure value is within 24-bit range."""
        if not (0 <= self.value <= 0xFFFFFF):
            object.__setattr__(self, 'value', self.value & 0xFFFFFF)
    
    # Layer Properties
    @property
    def reality_layer(self) -> int:
        """Get the reality layer (bits 0-7) - fundamental existence state."""
        return (self.value >> 0) & 0xFF
    
    @property
    def information_layer(self) -> int:
        """Get the information layer (bits 8-15) - data and pattern encoding."""
        return (self.value >> 8) & 0xFF
    
    @property
    def activation_layer(self) -> int:
        """Get the activation layer (bits 16-23) - dynamic state and potential."""
        return (self.value >> 16) & 0xFF
    
    @property
    def layers(self) -> Tuple[int, int, int]:
        """Get all three layers as a tuple (reality, information, activation)."""
        return (self.reality_layer, self.information_layer, self.activation_layer)
    
    # Bit-level operations
    @property
    def bits(self) -> List[int]:
        """Get individual bits as a list (LSB first)."""
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
    def layer_coherence(self) -> float:
        """
        Calculate coherence between layers.
        
        Returns:
            Coherence value between 0 and 1, where 1 indicates perfect layer alignment
        """
        if self.value == 0:
            return 1.0
        
        # Calculate bit density in each layer
        reality_density = bin(self.reality_layer).count('1') / 8
        info_density = bin(self.information_layer).count('1') / 8
        activation_density = bin(self.activation_layer).count('1') / 8
        
        # Calculate variance in densities (lower variance = higher coherence)
        densities = [reality_density, info_density, activation_density]
        mean_density = sum(densities) / 3
        variance = sum((d - mean_density) ** 2 for d in densities) / 3
        
        # Convert variance to coherence (0 variance = 1 coherence)
        coherence = 1.0 / (1.0 + variance * 10)  # Scale factor for sensitivity
        return min(1.0, coherence)
    
    # Toggle operations
    def toggle(self) -> 'OffBit':
        """Create a new OffBit with all bits toggled."""
        return OffBit(self.value ^ 0xFFFFFF)
    
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
        
        return OffBit(self.value ^ (1 << position))
    
    def toggle_layer(self, layer: int) -> 'OffBit':
        """
        Create a new OffBit with a specific layer toggled.
        
        Args:
            layer: Layer to toggle (1=reality, 2=information, 3=activation)
        
        Returns:
            New OffBit with specified layer toggled
        """
        if layer == 1:
            return OffBit(self.value ^ 0x0000FF)
        elif layer == 2:
            return OffBit(self.value ^ 0x00FF00)
        elif layer == 3:
            return OffBit(self.value ^ 0xFF0000)
        else:
            raise ValueError(f"Layer {layer} out of range [1, 3]")
    
    # Bit access and manipulation
    def get_bit(self, position: int) -> int:
        """Get the value of a specific bit."""
        if not (0 <= position < 24):
            raise ValueError(f"Bit position {position} out of range [0, 23]")
        
        return (self.value >> position) & 1
    
    def set_bit(self, position: int, value: int) -> 'OffBit':
        """Create a new OffBit with a specific bit set."""
        if not (0 <= position < 24):
            raise ValueError(f"Bit position {position} out of range [0, 23]")
        if value not in (0, 1):
            raise ValueError(f"Bit value must be 0 or 1, got {value}")
        
        if value == 1:
            return OffBit(self.value | (1 << position))
        else:
            return OffBit(self.value & ~(1 << position))
    
    def set_layer(self, layer: int, value: int) -> 'OffBit':
        """
        Create a new OffBit with a specific layer set.
        
        Args:
            layer: Layer to set (1=reality, 2=information, 3=activation)
            value: 8-bit value for the layer
        
        Returns:
            New OffBit with specified layer set
        """
        if not (1 <= layer <= 3):
            raise ValueError(f"Layer {layer} out of range [1, 3]")
        if not (0 <= value <= 0xFF):
            raise ValueError(f"Layer value {value} out of range [0, 255]")
        
        if layer == 1:
            return OffBit((self.value & 0xFFFF00) | value)
        elif layer == 2:
            return OffBit((self.value & 0xFF00FF) | (value << 8))
        else:  # layer == 3
            return OffBit((self.value & 0x00FFFF) | (value << 16))
    
    # UBP-specific operations
    def resonance_factor(self, frequency: float, time: float, k: float = 0.0002) -> float:
        """
        Calculate resonance factor for this OffBit.
        
        Args:
            frequency: Resonance frequency (Hz)
            time: Time parameter (s)
            k: Decay constant
        
        Returns:
            Resonance factor between 0 and 1
        """
        d = time * frequency
        return math.exp(-k * d * d)
    
    def coherence_with(self, other: 'OffBit') -> float:
        """
        Calculate coherence with another OffBit.
        
        Args:
            other: Another OffBit to compare with
        
        Returns:
            Coherence value between 0 and 1
        """
        if self.value == 0 and other.value == 0:
            return 1.0
        
        # XOR to find differences
        diff = self.value ^ other.value
        diff_bits = bin(diff).count('1')
        
        # Coherence is inversely related to differences
        coherence = 1.0 - (diff_bits / 24.0)
        return max(0.0, coherence)
    
    def entanglement_strength(self, other: 'OffBit') -> float:
        """
        Calculate entanglement strength with another OffBit.
        
        Args:
            other: Another OffBit to calculate entanglement with
        
        Returns:
            Entanglement strength between 0 and 1
        """
        # Calculate layer-wise correlations
        correlations = []
        for i in range(3):
            layer1 = (self.value >> (i * 8)) & 0xFF
            layer2 = (other.value >> (i * 8)) & 0xFF
            
            if layer1 == 0 and layer2 == 0:
                correlations.append(1.0)
            else:
                # Calculate normalized correlation
                correlation = 1.0 - abs(layer1 - layer2) / 255.0
                correlations.append(correlation)
        
        # Average correlation across layers
        return sum(correlations) / 3
    
    # Data extraction for error correction
    def extract_golay_data(self) -> int:
        """Extract 24-bit data for Golay[24,12] error correction."""
        return self.value
    
    def extract_hamming_data(self) -> List[int]:
        """Extract data for Hamming[7,4] error correction (per layer)."""
        return [
            self.reality_layer & 0x0F,      # 4 bits from reality layer
            self.information_layer & 0x0F,   # 4 bits from information layer
            self.activation_layer & 0x0F     # 4 bits from activation layer
        ]
    
    # String representations
    def __str__(self) -> str:
        return f"OffBit(0x{self.value:06X})"
    
    def __repr__(self) -> str:
        return (f"OffBit(value=0x{self.value:06X}, "
                f"layers=({self.reality_layer}, {self.information_layer}, {self.activation_layer}), "
                f"active_bits={self.active_bits}, coherence={self.layer_coherence:.3f})")
    
    def to_binary_string(self) -> str:
        """Return binary representation with layer separators."""
        binary = f"{self.value:024b}"
        return f"{binary[16:24]}|{binary[8:16]}|{binary[0:8]}"  # activation|information|reality


# Factory functions for creating specific OffBit types
def create_quantum_offbit(reality: int = 0, information: int = 0, activation: int = 0) -> OffBit:
    """Create an OffBit optimized for quantum realm operations."""
    # Apply quantum bias (e/12 ≈ 0.2265234857)
    quantum_bias = int(0.2265234857 * 255)
    
    reality = reality or quantum_bias
    information = information or (quantum_bias >> 1)
    activation = activation or (quantum_bias >> 2)
    
    value = (activation << 16) | (information << 8) | reality
    return OffBit(value)


def create_electromagnetic_offbit(reality: int = 0, information: int = 0, activation: int = 0) -> OffBit:
    """Create an OffBit optimized for electromagnetic realm operations."""
    # Apply π-resonance bias
    pi_bias = int((math.pi / 10) * 255)  # Scale π to 8-bit range
    
    reality = reality or pi_bias
    information = information or (pi_bias >> 1)
    activation = activation or (pi_bias >> 2)
    
    value = (activation << 16) | (information << 8) | reality
    return OffBit(value)


def create_cosmological_offbit(reality: int = 0, information: int = 0, activation: int = 0) -> OffBit:
    """Create an OffBit optimized for cosmological realm operations."""
    # Apply π^φ bias (≈ 0.83203682)
    phi = (1 + math.sqrt(5)) / 2  # Golden ratio
    cosmic_bias = int((math.pi ** (1/phi)) * 255 / 10)  # Scale to 8-bit range
    
    reality = reality or cosmic_bias
    information = information or (cosmic_bias >> 1)
    activation = activation or (cosmic_bias >> 2)
    
    value = (activation << 16) | (information << 8) | reality
    return OffBit(value)


# Utility functions
def offbits_from_array(data: np.ndarray) -> List[OffBit]:
    """Convert numpy array to list of OffBits."""
    return [OffBit(int(val) & 0xFFFFFF) for val in data.flatten()]


def offbits_to_array(offbits: List[OffBit]) -> np.ndarray:
    """Convert list of OffBits to numpy array."""
    return np.array([offbit.value for offbit in offbits], dtype=np.uint32)


if __name__ == "__main__":
    # Test the OffBit implementation
    print("Testing OffBit implementation...")
    
    # Create test OffBits
    offbit1 = OffBit(0xABCDEF)
    offbit2 = create_quantum_offbit()
    offbit3 = create_electromagnetic_offbit()
    
    print(f"OffBit 1: {offbit1}")
    print(f"  Layers: {offbit1.layers}")
    print(f"  Binary: {offbit1.to_binary_string()}")
    print(f"  Coherence: {offbit1.layer_coherence:.3f}")
    
    print(f"\nQuantum OffBit: {offbit2}")
    print(f"  Layers: {offbit2.layers}")
    print(f"  Coherence: {offbit2.layer_coherence:.3f}")
    
    print(f"\nElectromagnetic OffBit: {offbit3}")
    print(f"  Layers: {offbit3.layers}")
    print(f"  Coherence: {offbit3.layer_coherence:.3f}")
    
    # Test operations
    print(f"\nCoherence between quantum and EM: {offbit2.coherence_with(offbit3):.3f}")
    print(f"Entanglement strength: {offbit2.entanglement_strength(offbit3):.3f}")
    
    # Test layer manipulation
    modified = offbit1.set_layer(2, 0x55)
    print(f"\nOriginal: {offbit1}")
    print(f"Modified layer 2: {modified}")
    
    print("\nOffBit implementation test completed successfully!")

