# UBP 3.4
"""
Universal Binary Principle (UBP) Framework v3.7.1 - UBP State Management Module
Author: Euan Craig, New Zealand
Date: 28 November 2025
======================================

Defines core state classes for the Universal Binary Principle system,
including OffBit, MutableBitfield, and UBPState.
"""

import numpy as np
from typing import Dict, List, Tuple, Optional, Any, Union
from dataclasses import dataclass, field
import time
import math
# Imports for Golay/Leech integration
from error_correction.golay_code import GolayG24
from error_correction.leech_lattice import LeechLatticePoint

# Import UBPConfig and get_config for constant loading
# NOTE: Imports are moved inside functions to break circular dependency with utils/
# from utils.ubp_config import get_config, UBPConfig

# _config: UBPConfig = get_config() # Initialize configuration


@dataclass(frozen=True)
class OffBit:
    """
    Immutable 24-bit UBP OffBit with Golay code and Leech lattice integration.
    
    Represents a fundamental unit of UBP computation with 24-bit data
    and layer-based access patterns, now enhanced with error correction properties.
    """
    value: int
    
    # Internal caches for performance
    _golay_valid: Optional[bool] = field(init=False, default=None)
    _leech_point: Optional[np.ndarray] = field(init=False, default=None)
    
    def __post_init__(self):
        # FIXED 3.7.1: Raise ValueError instead of silently masking invalid input
        # This prevents bugs from being hidden and enforces correct usage
        if not (0 <= self.value <= 0xFFFFFF):
            raise ValueError(
                f"OffBit value must be in range [0, 0xFFFFFF] (24-bit), "
                f"got {self.value:#x} ({self.value}). "
                f"Use (value & 0xFFFFFF) to explicitly mask if needed."
            )
        # Initialize caches
        object.__setattr__(self, '_golay_valid', None)
        object.__setattr__(self, '_leech_point', None)
    
    @property
    def layer(self) -> int:
        """Get the 24-bit layer value."""
        return self.value & 0xFFFFFF
    
    @property
    def bits(self) -> List[int]:
        """Get individual bits as a list (position 0 is LSB)."""
        return [(self.value >> i) & 1 for i in range(24)]
    
    @property
    def active_bits(self) -> int:
        """Count of active (1) bits (Hamming weight)."""
        return bin(self.value).count('1')
    
    def hamming_weight(self) -> int:
        """Calculate the Hamming weight (number of 1 bits)."""
        return self.active_bits
    
    @property
    def is_active(self) -> bool:
        """Check if OffBit has any active bits."""
        return self.value > 0
    
    def toggle(self) -> 'OffBit':
        """
        Create a new OffBit with toggled state.
        
        Returns:
            New OffBit with inverted bits
        """
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
    
    def set_bit(self, position: int, value: int) -> 'OffBit':
        """
        Create a new OffBit with a specific bit set.
        
        Args:
            position: Bit position (0-23)
            value: Bit value (0 or 1)
        
        Returns:
            New OffBit with specified bit set
        """
        if not (0 <= position < 24):
            raise ValueError(f"Bit position {position} out of range [0, 23]")
        if value not in (0, 1):
            raise ValueError(f"Bit value must be 0 or 1, got {value}")
        
        if value == 1:
            return OffBit(self.value | (1 << position))
        else:
            return OffBit(self.value & ~(1 << position))
    
    def extract_data(self) -> int:
        """
        Extract 24-bit data for Golay correction.
        
        Returns:
            24-bit data value
        """
        return self.layer
    
    @property
    def is_golay_codeword(self) -> bool:
        """
        Check if this OffBit's bits form a valid extended Golay codeword (G24).
        
        G24 is a [24, 12, 8] code. Codewords have Hamming weight 0, 8, 12, 16, or 24.
        """
        if self._golay_valid is None:
            weight = self.active_bits
            object.__setattr__(self, '_golay_valid', weight in {0, 8, 12, 16, 24})
        return self._golay_valid
    
    def to_leech_point(self) -> np.ndarray:
        """
        Convert OffBit to 24D Leech lattice point (simplified construction).
        
        Construction: Uses the Golay code structure embedded in the OffBit.
        """
        if self._leech_point is not None:
            return self._leech_point
        
        # Get binary representation as 24 bits
        bits = self.bits
        
        # Convert to Leech lattice coordinates (simple construction: 2*b - 1 gives ±1)
        leech_coords = np.array([2 * b - 1 for b in bits], dtype=np.float64)
        
        # Leech lattice has minimum norm² = 32. We check the current norm.
        current_norm_sq = np.sum(leech_coords**2)
        
        # In the simplified construction, the norm squared is always 24 (24 * (±1)^2).
        # A full Leech lattice construction is complex. We use the simplified
        # construction as the base and ensure the point is a valid vector in R^24.
        # The full Leech lattice properties are handled by the LeechLatticeProjection module.
        
        # Automatic Mapping: If the OffBit is a Golay codeword, it is a Leech vector.
        # If not, it is automatically mapped to the nearest Leech vector (Construction A).
        if not self.is_golay_codeword:
            # Use Golay correction to find the nearest codeword (Construction A)
            from error_correction.golay_code import GolayG24
            golay_encoder = GolayG24()
            corrected_bits = golay_encoder.correct_errors(np.array(bits, dtype=int))
            leech_coords = np.array([2 * b - 1 for b in corrected_bits], dtype=np.float64)
        
        object.__setattr__(self, '_leech_point', leech_coords)
        return self._leech_point
    
    def golay_parity(self) -> int:
        """
        Compute Golay code parity (syndrome) for error detection/correction.
        
        Returns:
            Parity pattern (0 = valid G24 codeword)
        """
        # For extended Golay code G24, all codewords have weight divisible by 4.
        weight = self.active_bits
        parity = weight % 4
        return parity
    
    def correct_with_aecn(self, realm_id: str = "DEFAULT") -> Tuple['OffBit', str]:
        """
        Process the OffBit through the Automatic Error Correction Network (AECN)
        for a specific realm, or the best realm if not specified.
        
        Args:
            realm_id: The realm to use for correction. If "BEST", the AECN
                      will select the realm that yields the highest coherence.
        
        Returns:
            Tuple of (Corrected OffBit, Realm ID Used)
        """
        from error_correction.aecn import AECN
        
        # NOTE: AECN is initialized once per call for simplicity, but should be
        # a singleton in a full UBP runtime environment.
        aecn = AECN(realms=[realm_id] if realm_id != "BEST" else ["DEFAULT", "QUANTUM", "GRAVITY"])
        
        result = aecn.process_offbit(self)
        
        return result.corrected_offbit, result.realm_id
        
    def correct_with_golay(self) -> 'OffBit':
        """
        Attempt to correct bit errors using Golay code error correction.
        
        Returns:
            Corrected OffBit (or self if no correction is attempted/needed)
        """
        # This is now a legacy method, deferring to AECN for full logic.
        return self.correct_with_aecn(realm_id="DEFAULT")[0]
    
    def __str__(self) -> str:
        return f"OffBit(0x{self.value:06X})"
    
    def __repr__(self) -> str:
        return f"OffBit(value={self.value}, layer=0x{self.layer:06X}, active_bits={self.active_bits}, is_golay={self.is_golay_codeword})"


class MutableBitfield:
    """
    Mutable bitfield for UBP operations.
    
    Provides efficient storage and manipulation of large collections of OffBits.
    """
    
    def __init__(self, size: int = 1000):
        """
        Initialize mutable bitfield.
        
        Args:
            size: Number of OffBits to store
        """
        self.size = size
        self.data = np.zeros(size, dtype=np.uint32)
        self.active_count = 0
        self.last_modified = time.time()
    
    @property
    def current_sparsity(self) -> float:
        """Calculate the current sparsity of the bitfield."""
        if self.size == 0:
            return 1.0 # Fully sparse if no capacity
        return (self.size - self.active_count) / self.size

    def get_offbit(self, index: int) -> OffBit:
        """
        Get OffBit at specified index.
        
        Args:
            index: Index in the bitfield
        
        Returns:
            OffBit at the specified index
        """
        if not (0 <= index < self.size):
            raise IndexError(f"Index {index} out of range [0, {self.size})")
        
        return OffBit(int(self.data[index]) & 0xFFFFFF)
    
    def set_offbit(self, index: int, offbit: OffBit) -> None:
        """
        Set OffBit at specified index.
        
        Args:
            index: Index in the bitfield
            offbit: OffBit to set
        """
        if not (0 <= index < self.size):
            raise IndexError(f"Index {index} out of range [0, {self.size})")
        
        old_value = self.data[index]
        new_value = offbit.value & 0xFFFFFF
        
        self.data[index] = new_value
        
        # Update active count
        if old_value == 0 and new_value != 0:
            self.active_count += 1
        elif old_value != 0 and new_value == 0:
            self.active_count -= 1
        
        self.last_modified = time.time()
    
    def toggle_offbit(self, index: int) -> None:
        """
        Toggle OffBit at specified index.
        
        Args:
            index: Index in the bitfield
        """
        current_offbit = self.get_offbit(index)
        toggled_offbit = current_offbit.toggle()
        self.set_offbit(index, toggled_offbit)
    
    def get_active_offbits(self) -> List[Tuple[int, OffBit]]:
        """
        Get all active OffBits.
        
        Returns:
            List of (index, OffBit) tuples for active OffBits
        """
        active_offbits = []
        for i in range(self.size):
            if self.data[i] != 0:
                active_offbits.append((i, self.get_offbit(i)))
        return active_offbits
    
    def get_coherence(self) -> float:
        """
        Compute bitfield coherence.
        
        Returns:
            Coherence value (0 to 1)
        """
        if self.size == 0:
            return 1.0
        
        # Compute statistical coherence
        active_ratio = self.active_count / self.size
        
        # Compute spatial coherence (clustering)
        if self.active_count > 1:
            active_indices = np.where(self.data != 0)[0]
            if len(active_indices) > 1:
                distances = np.diff(active_indices)
                mean_distance = np.mean(distances)
                std_distance = np.std(distances)
                
                # Lower standard deviation = higher coherence
                spatial_coherence = 1.0 / (1.0 + std_distance / (mean_distance + 1e-10))
            else:
                spatial_coherence = 1.0
        else:
            spatial_coherence = 1.0
        
        # Combine coherence measures
        total_coherence = 0.5 * active_ratio + 0.5 * spatial_coherence
        
        return min(1.0, total_coherence)
    
    def compute_nrci(self, target_bitfield: 'MutableBitfield') -> float:
        """
        Compute Non-Random Coherence Index with target bitfield.
        
        Args:
            target_bitfield: Target bitfield for comparison
        
        Returns:
            NRCI value (0 to 1)
        """
        if self.size != target_bitfield.size:
            raise ValueError("Bitfields must have the same size for NRCI calculation")
        
        # Convert to float arrays for better precision
        data1 = self.data.astype(np.float64)
        data2 = target_bitfield.data.astype(np.float64)
        
        # Compute correlation coefficient
        if np.std(data1) == 0 or np.std(data2) == 0:
            # If either dataset has no variation, use exact match
            exact_matches = np.sum(data1 == data2)
            return exact_matches / self.size
        
        # Compute Pearson correlation coefficient
        correlation = np.corrcoef(data1, data2)[0, 1]
        
        # Handle NaN correlation (when one or both arrays are constant)
        if np.isnan(correlation):
            exact_matches = np.sum(data1 == data2)
            return exact_matches / self.size
        
        # Convert correlation to NRCI (0 to 1 scale)
        # Perfect correlation (1.0) = NRCI 1.0
        # No correlation (0.0) = NRCI 0.5
        # Perfect anti-correlation (-1.0) = NRCI 0.0
        nrci = (correlation + 1.0) / 2.0
        
        return max(0.0, min(1.0, nrci))
    
    def resize(self, new_size: int) -> None:
        """
        Resize the bitfield.
        
        Args:
            new_size: New size for the bitfield
        """
        if new_size <= 0:
            raise ValueError("New size must be positive")
        
        old_data = self.data
        self.data = np.zeros(new_size, dtype=np.uint32)
        
        # Copy existing data
        copy_size = min(self.size, new_size)
        self.data[:copy_size] = old_data[:copy_size]
        
        # Update size and active count
        self.size = new_size
        self.active_count = np.count_nonzero(self.data)
        self.last_modified = time.time()
    
    def clear(self) -> None:
        """Clear all OffBits in the bitfield."""
        self.data.fill(0)
        self.active_count = 0
        self.last_modified = time.time()
    
    def copy(self) -> 'MutableBitfield':
        """
        Create a copy of the bitfield.
        
        Returns:
            Copy of the bitfield
        """
        new_bitfield = MutableBitfield(self.size)
        new_bitfield.data = self.data.copy()
        new_bitfield.active_count = self.active_count
        new_bitfield.last_modified = self.last_modified
        return new_bitfield
    
    def __len__(self) -> int:
        return self.size
    
    def __str__(self) -> str:
        return f"MutableBitfield(size={self.size}, active={self.active_count}, coherence={self.get_coherence():.4f})"
    
    def __repr__(self) -> str:
        return f"MutableBitfield(size={self.size}, active_count={self.active_count}, last_modified={self.last_modified})"


@dataclass
class UBPState:
    """
    Complete UBP system state.
    
    Represents the full state of a UBP system including bitfields,
    coherence metrics, and temporal information.
    """
    bitfield: MutableBitfield
    timestamp: float = field(default_factory=time.time)
    realm: str = "quantum"
    coherence: float = 0.0
    nrci: float = 0.0
    energy: float = 0.0
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self):
        """Update coherence after initialization."""
        self.update_coherence()
    
    def update_coherence(self) -> None:
        """Update coherence metrics."""
        self.coherence = self.bitfield.get_coherence()
        self.timestamp = time.time()
    
    def compute_energy(self) -> float:
        """
        Compute UBP energy for the current state.
        
        Returns:
            UBP energy value
        """
        # Get energy parameters directly from config
        from utils.ubp_config import get_config
        _config = get_config()
        
        M = self.bitfield.active_count
        C = _config.constants.SPEED_OF_LIGHT
        
        # These constants are no longer in UBP_ENERGY_PARAMS, use direct config lookup
        R_0 = 0.95 # Default from resonance_strength
        H_t = 0.05 # Default from resonance_strength
        R = R_0 * (1 - H_t / math.log(4)) # resonance_strength calculation
        
        S_opt_default = 0.98 # Default from structural_optimality
        S_opt = S_opt_default
        
        # Simplified energy calculation (matching the current energy function's structure for basic use)
        # Note: A full energy calculation would involve P_GCI, O_observer, c_infinity etc.
        # This is a simplified proxy for `UBPState` to track its own energy.
        self.energy = M * C * R * S_opt * self.coherence
        
        return self.energy
    
    def evolve(self, delta_t: float = 0.001) -> None:
        """
        Evolve the UBP state over time.
        
        Args:
            delta_t: Time step for evolution
        """
        from utils.ubp_config import get_config
        _config = get_config()
        
        # Get toggle probability for the current realm from config
        toggle_prob = _config.constants.UBP_TOGGLE_PROBABILITIES.get(self.realm, 0.5)
        
        # Determine how many OffBits to toggle
        num_toggles = int(self.bitfield.size * toggle_prob * delta_t)
        
        # Randomly select OffBits to toggle
        if num_toggles > 0:
            indices = np.random.choice(self.bitfield.size, size=min(num_toggles, self.bitfield.size), replace=False)
            
            for index in indices:
                self.bitfield.toggle_offbit(index)
        
        # Update state
        self.update_coherence()
        self.compute_energy()
        self.timestamp = time.time()
    
    def copy(self) -> 'UBPState':
        """
        Create a copy of the UBP state.
        
        Returns:
            Copy of the UBP state
        """
        return UBPState(
            bitfield=self.bitfield.copy(),
            timestamp=self.timestamp,
            realm=self.realm,
            coherence=self.coherence,
            nrci=self.nrci,
            energy=self.energy,
            metadata=self.metadata.copy()
        )
    
    def __str__(self) -> str:
        return f"UBPState(realm={self.realm}, coherence={self.coherence:.4f}, nrci={self.nrci:.6f}, energy={self.energy:.2e})"


def create_test_bitfield(size: int = 1000, active_ratio: float = 0.1) -> MutableBitfield:
    """
    Create a test bitfield with specified parameters.
    
    Args:
        size: Size of the bitfield
        active_ratio: Ratio of active OffBits
    
    Returns:
        Test bitfield
    """
    bitfield = MutableBitfield(size)
    
    # Randomly activate OffBits
    num_active = int(size * active_ratio)
    active_indices = np.random.choice(size, size=num_active, replace=False)
    
    for index in active_indices:
        # Create random OffBit value
        value = np.random.randint(1, 0xFFFFFF)
        offbit = OffBit(value)
        bitfield.set_offbit(index, offbit)
    
    return bitfield


def create_test_state(size: int = 1000, realm: str = "quantum") -> UBPState:
    """
    Create a test UBP state.
    
    Args:
        size: Size of the bitfield
        realm: UBP realm
    
    Returns:
        Test UBP state
    """
    bitfield = create_test_bitfield(size)
    state = UBPState(bitfield=bitfield, realm=realm)
    state.compute_energy()
    return state


if __name__ == "__main__":
    # Test OffBit functionality
    print("Testing OffBit...")
    
    offbit = OffBit(0xABCDEF)
    print(f"OffBit: {offbit}")
    print(f"Layer: 0x{offbit.layer:06X}")
    print(f"Active bits: {offbit.active_bits}")
    print(f"Bit 0: {offbit.get_bit(0)}")
    print(f"Bit 23: {offbit.get_bit(23)}")
    
    toggled = offbit.toggle()
    print(f"Toggled: {toggled}")
    
    # Test MutableBitfield
    print(f"\nTesting MutableBitfield...")
    
    bitfield = create_test_bitfield(100, 0.2)
    print(f"Bitfield: {bitfield}")
    print(f"Active OffBits: {len(bitfield.get_active_offbits())}")
    print(f"Coherence: {bitfield.get_coherence():.4f}")
    
    # Test UBPState
    print(f"\nTesting UBPState...")
    
    state = create_test_state(100, "quantum")
    print(f"State: {state}")
    
    # Evolve state
    print(f"\nEvolving state...")
    for i in range(5):
        state.evolve(0.01)
        print(f"Step {i+1}: coherence={state.coherence:.4f}, energy={state.energy:.2e}")
    
    print(f"\nUBP state management tests completed.")
