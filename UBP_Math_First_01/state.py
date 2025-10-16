"""
UBP State Classes

Defines the core data structures for the UBP system:
- OffBit: 24-bit fundamental unit with 4 ontological layers
- Bitfield: 6D sparse array of OffBits
"""

from dataclasses import dataclass
from typing import List, Tuple, Dict, Optional, Union
import numpy as np
from .constants import get_bitfield_config, get_hardware_profile


@dataclass
class OffBit:
    """
    24-bit fundamental unit of the UBP system, padded to 32-bit.
    
    Structure:
    - Reality Layer (bits 0-5): Observable properties
    - Information Layer (bits 6-11): Data processing, constants
    - Activation Layer (bits 12-17): Dynamic states, energy
    - Unactivated Layer (bits 18-23): Potential/latent states
    """
    
    value: int = 0  # 24-bit value (stored as 32-bit int)
    
    def __post_init__(self):
        """Ensure value is within 24-bit range."""
        if not (0 <= self.value <= 0xFFFFFF):
            raise ValueError(f"OffBit value must be 24-bit (0-{0xFFFFFF}), got {self.value}")
    
    @property
    def reality_layer(self) -> int:
        """Get Reality Layer (bits 0-5)."""
        return self.value & 0x3F  # 0b111111
    
    @reality_layer.setter
    def reality_layer(self, value: int):
        """Set Reality Layer (bits 0-5)."""
        if not (0 <= value <= 0x3F):
            raise ValueError(f"Reality layer must be 6-bit (0-63), got {value}")
        self.value = (self.value & ~0x3F) | value
    
    @property
    def information_layer(self) -> int:
        """Get Information Layer (bits 6-11)."""
        return (self.value >> 6) & 0x3F
    
    @information_layer.setter
    def information_layer(self, value: int):
        """Set Information Layer (bits 6-11)."""
        if not (0 <= value <= 0x3F):
            raise ValueError(f"Information layer must be 6-bit (0-63), got {value}")
        self.value = (self.value & ~(0x3F << 6)) | (value << 6)
    
    @property
    def activation_layer(self) -> int:
        """Get Activation Layer (bits 12-17)."""
        return (self.value >> 12) & 0x3F
    
    @activation_layer.setter
    def activation_layer(self, value: int):
        """Set Activation Layer (bits 12-17)."""
        if not (0 <= value <= 0x3F):
            raise ValueError(f"Activation layer must be 6-bit (0-63), got {value}")
        self.value = (self.value & ~(0x3F << 12)) | (value << 12)
    
    @property
    def unactivated_layer(self) -> int:
        """Get Unactivated Layer (bits 18-23)."""
        return (self.value >> 18) & 0x3F
    
    @unactivated_layer.setter
    def unactivated_layer(self, value: int):
        """Set Unactivated Layer (bits 18-23)."""
        if not (0 <= value <= 0x3F):
            raise ValueError(f"Unactivated layer must be 6-bit (0-63), got {value}")
        self.value = (self.value & ~(0x3F << 18)) | (value << 18)
    
    @property
    def is_active(self) -> bool:
        """Check if OffBit is active (any bit in activation layer is set)."""
        return self.activation_layer > 0
    
    @property
    def toggle_state(self) -> bool:
        """Get the primary toggle state (bit 12 of activation layer)."""
        return bool(self.activation_layer & 1)
    
    @toggle_state.setter
    def toggle_state(self, state: bool):
        """Set the primary toggle state (bit 12 of activation layer)."""
        if state:
            self.activation_layer |= 1
        else:
            self.activation_layer &= ~1
    
    def get_layer_bits(self, layer: str) -> List[int]:
        """
        Get individual bits of a layer as a list.
        
        Args:
            layer: Layer name ('reality', 'information', 'activation', 'unactivated')
            
        Returns:
            List of 6 bits (0 or 1)
        """
        layer_map = {
            'reality': self.reality_layer,
            'information': self.information_layer,
            'activation': self.activation_layer,
            'unactivated': self.unactivated_layer
        }
        
        if layer not in layer_map:
            raise ValueError(f"Invalid layer '{layer}'. Must be one of: {list(layer_map.keys())}")
        
        layer_value = layer_map[layer]
        return [(layer_value >> i) & 1 for i in range(6)]
    
    def set_layer_bits(self, layer: str, bits: List[int]):
        """
        Set individual bits of a layer from a list.
        
        Args:
            layer: Layer name ('reality', 'information', 'activation', 'unactivated')
            bits: List of 6 bits (0 or 1)
        """
        if len(bits) != 6:
            raise ValueError(f"Layer must have exactly 6 bits, got {len(bits)}")
        
        if not all(bit in (0, 1) for bit in bits):
            raise ValueError("All bits must be 0 or 1")
        
        # Convert bit list to integer
        layer_value = sum(bit << i for i, bit in enumerate(bits))
        
        # Set the layer
        if layer == 'reality':
            self.reality_layer = layer_value
        elif layer == 'information':
            self.information_layer = layer_value
        elif layer == 'activation':
            self.activation_layer = layer_value
        elif layer == 'unactivated':
            self.unactivated_layer = layer_value
        else:
            raise ValueError(f"Invalid layer '{layer}'")
    
    def copy(self) -> 'OffBit':
        """Create a copy of this OffBit."""
        return OffBit(self.value)
    
    def __str__(self) -> str:
        """String representation showing layer structure."""
        return (f"OffBit(0x{self.value:06X}: "
                f"R={self.reality_layer:02d} "
                f"I={self.information_layer:02d} "
                f"A={self.activation_layer:02d} "
                f"U={self.unactivated_layer:02d})")
    
    def __repr__(self) -> str:
        return f"OffBit({self.value})"


class Bitfield:
    """
    6D sparse array of OffBits representing the UBP computational substrate.
    
    Dimensions: [170, 170, 170, 5, 2, 2] = ~2.3M cells
    Sparsity: ~0.01 (1% active)
    """
    
    def __init__(self, hardware_profile: str = "desktop_8gb"):
        """
        Initialize Bitfield with specified hardware profile.
        
        Args:
            hardware_profile: Hardware configuration to use
        """
        self.config = get_bitfield_config()
        self.hardware = get_hardware_profile(hardware_profile)
        
        # Bitfield dimensions
        self.dimensions = tuple(self.config["dimensions"])
        self.total_cells = self.config["total_cells"]
        self.sparsity = self.config["sparsity"]
        
        # Hardware constraints
        self.max_offbits = self.hardware["max_offbits"]
        
        # Sparse storage: only store active OffBits
        # Key: 6D coordinate tuple, Value: OffBit
        self._offbits: Dict[Tuple[int, int, int, int, int, int], OffBit] = {}
        
        # Statistics
        self._active_count = 0
        self._toggle_count = 0
    
    def get_coordinate_bounds(self) -> Tuple[Tuple[int, int], ...]:
        """Get the bounds for each dimension."""
        return tuple((0, dim) for dim in self.dimensions)
    
    def is_valid_coordinate(self, coord: Tuple[int, int, int, int, int, int]) -> bool:
        """Check if coordinate is within Bitfield bounds."""
        if len(coord) != 6:
            return False
        
        for i, (c, dim) in enumerate(zip(coord, self.dimensions)):
            if not (0 <= c < dim):
                return False
        
        return True
    
    def get_offbit(self, coord: Tuple[int, int, int, int, int, int]) -> OffBit:
        """
        Get OffBit at specified coordinate.
        
        Args:
            coord: 6D coordinate tuple
            
        Returns:
            OffBit at coordinate (default OffBit(0) if not set)
        """
        if not self.is_valid_coordinate(coord):
            raise ValueError(f"Invalid coordinate {coord} for dimensions {self.dimensions}")
        
        return self._offbits.get(coord, OffBit(0))
    
    def set_offbit(self, coord: Tuple[int, int, int, int, int, int], offbit: OffBit):
        """
        Set OffBit at specified coordinate.
        
        Args:
            coord: 6D coordinate tuple
            offbit: OffBit to set
        """
        if not self.is_valid_coordinate(coord):
            raise ValueError(f"Invalid coordinate {coord} for dimensions {self.dimensions}")
        
        if len(self._offbits) >= self.max_offbits and coord not in self._offbits:
            raise RuntimeError(f"Maximum OffBits ({self.max_offbits}) exceeded for hardware profile")
        
        # Update statistics
        was_active = coord in self._offbits and self._offbits[coord].is_active
        is_active = offbit.is_active
        
        if offbit.value == 0:
            # Remove zero OffBits to maintain sparsity
            if coord in self._offbits:
                del self._offbits[coord]
                if was_active:
                    self._active_count -= 1
        else:
            self._offbits[coord] = offbit.copy()
            if is_active and not was_active:
                self._active_count += 1
            elif not is_active and was_active:
                self._active_count -= 1
    
    def toggle_offbit(self, coord: Tuple[int, int, int, int, int, int]):
        """
        Toggle the state of OffBit at coordinate.
        
        Args:
            coord: 6D coordinate tuple
        """
        offbit = self.get_offbit(coord)
        offbit.toggle_state = not offbit.toggle_state
        self.set_offbit(coord, offbit)
        self._toggle_count += 1
    
    def get_active_offbits(self) -> Dict[Tuple[int, int, int, int, int, int], OffBit]:
        """Get all active OffBits."""
        return {coord: offbit for coord, offbit in self._offbits.items() if offbit.is_active}
    
    def get_neighbors(self, coord: Tuple[int, int, int, int, int, int], 
                     radius: int = 1) -> List[Tuple[Tuple[int, int, int, int, int, int], OffBit]]:
        """
        Get neighboring OffBits within specified radius.
        
        Args:
            coord: Center coordinate
            radius: Search radius
            
        Returns:
            List of (coordinate, OffBit) tuples
        """
        neighbors = []
        
        # Generate all coordinates within radius
        for dx in range(-radius, radius + 1):
            for dy in range(-radius, radius + 1):
                for dz in range(-radius, radius + 1):
                    for da in range(-radius, radius + 1):
                        for db in range(-radius, radius + 1):
                            for dc in range(-radius, radius + 1):
                                if dx == dy == dz == da == db == dc == 0:
                                    continue  # Skip center
                                
                                neighbor_coord = (
                                    coord[0] + dx, coord[1] + dy, coord[2] + dz,
                                    coord[3] + da, coord[4] + db, coord[5] + dc
                                )
                                
                                if self.is_valid_coordinate(neighbor_coord):
                                    offbit = self.get_offbit(neighbor_coord)
                                    if offbit.value != 0:  # Only include non-zero OffBits
                                        neighbors.append((neighbor_coord, offbit))
        
        return neighbors
    
    def get_subfield(self, start_coord: Tuple[int, int, int, int, int, int],
                    end_coord: Tuple[int, int, int, int, int, int]) -> 'Bitfield':
        """
        Extract a sub-region of the Bitfield.
        
        Args:
            start_coord: Starting coordinate (inclusive)
            end_coord: Ending coordinate (exclusive)
            
        Returns:
            New Bitfield containing the sub-region
        """
        # Create new Bitfield with adjusted dimensions
        sub_dimensions = tuple(end_coord[i] - start_coord[i] for i in range(6))
        
        # For simplicity, create with same hardware profile
        subfield = Bitfield(hardware_profile="desktop_8gb")  # Will be overridden
        subfield.dimensions = sub_dimensions
        subfield.total_cells = np.prod(sub_dimensions)
        
        # Copy relevant OffBits with adjusted coordinates
        for coord, offbit in self._offbits.items():
            # Check if coordinate is within sub-region
            if all(start_coord[i] <= coord[i] < end_coord[i] for i in range(6)):
                # Adjust coordinate to sub-region space
                sub_coord = tuple(coord[i] - start_coord[i] for i in range(6))
                subfield._offbits[sub_coord] = offbit.copy()
        
        subfield._active_count = sum(1 for offbit in subfield._offbits.values() if offbit.is_active)
        
        return subfield
    
    @property
    def active_count(self) -> int:
        """Number of active OffBits."""
        return self._active_count
    
    @property
    def total_offbits(self) -> int:
        """Total number of stored OffBits (non-zero)."""
        return len(self._offbits)
    
    @property
    def toggle_count(self) -> int:
        """Total number of toggle operations performed."""
        return self._toggle_count
    
    @property
    def current_sparsity(self) -> float:
        """Current sparsity ratio (active / total_cells)."""
        return self.total_offbits / self.total_cells if self.total_cells > 0 else 0.0
    
    def reset_statistics(self):
        """Reset toggle count and recalculate active count."""
        self._toggle_count = 0
        self._active_count = sum(1 for offbit in self._offbits.values() if offbit.is_active)
    
    def clear(self):
        """Clear all OffBits from the Bitfield."""
        self._offbits.clear()
        self._active_count = 0
        self._toggle_count = 0
    
    def __str__(self) -> str:
        """String representation of Bitfield statistics."""
        return (f"Bitfield({self.dimensions}, "
                f"active={self.active_count}, "
                f"total={self.total_offbits}, "
                f"sparsity={self.current_sparsity:.4f}, "
                f"toggles={self.toggle_count})")
    
    def __repr__(self) -> str:
        return f"Bitfield(dimensions={self.dimensions}, offbits={len(self._offbits)})"

