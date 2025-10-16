"""
Universal Binary Principle (UBP) - Improved Sparse Bitfield Implementation
Author: Euan Craig, New Zealand
Date: September 17, 2025

This module implements a sparse 6D Bitfield for efficient storage and manipulation
of large collections of OffBits. The implementation uses scipy.sparse matrices
and custom indexing to handle the 6D structure efficiently.
"""

import numpy as np
import scipy.sparse as sp
import time
import math
from typing import Dict, List, Tuple, Optional, Iterator, Union
from dataclasses import dataclass, field
from collections import defaultdict
import pickle
import gzip

from .offbit import OffBit, create_quantum_offbit


@dataclass
class BitfieldConfig:
    """Configuration for Bitfield dimensions and parameters."""
    # 6D dimensions (x, y, z, w, v, u)
    dimensions: Tuple[int, int, int, int, int, int] = (170, 170, 170, 5, 2, 2)
    
    # Hardware-specific sizing
    max_offbits: int = 1000000  # Default for 8GB systems
    sparsity_target: float = 0.01  # Target sparsity (1% active)
    
    # Performance parameters
    chunk_size: int = 1000  # For batch operations
    cache_size: int = 10000  # LRU cache for frequently accessed OffBits
    
    @property
    def total_capacity(self) -> int:
        """Calculate total theoretical capacity."""
        return np.prod(self.dimensions)
    
    @property
    def linear_size(self) -> int:
        """Get the linear size for sparse matrix representation."""
        return min(self.total_capacity, self.max_offbits)


class SparseBitfield:
    """
    Sparse 6D Bitfield for efficient UBP operations.
    
    Uses scipy.sparse.dok_matrix for efficient sparse storage and
    custom 6D-to-linear indexing for spatial operations.
    """
    
    def __init__(self, config: Optional[BitfieldConfig] = None):
        """
        Initialize sparse bitfield.
        
        Args:
            config: Bitfield configuration, uses default if None
        """
        self.config = config or BitfieldConfig()
        
        # Sparse storage using dictionary of keys format
        self._data = sp.dok_matrix((self.config.linear_size, 1), dtype=np.uint32)
        
        # Metadata tracking
        self.active_count = 0
        self.last_modified = time.time()
        self.access_count = 0
        
        # 6D coordinate mapping
        self._coord_cache = {}  # Cache for coordinate conversions
        self._reverse_cache = {}  # Cache for reverse lookups
        
        # Statistics
        self.stats = {
            'gets': 0,
            'sets': 0,
            'cache_hits': 0,
            'cache_misses': 0
        }
    
    def _coord_to_linear(self, coord: Tuple[int, int, int, int, int, int]) -> int:
        """
        Convert 6D coordinates to linear index.
        
        Args:
            coord: 6D coordinate tuple (x, y, z, w, v, u)
        
        Returns:
            Linear index for sparse matrix
        """
        x, y, z, w, v, u = coord
        dims = self.config.dimensions
        
        # Validate coordinates
        if not all(0 <= c < d for c, d in zip(coord, dims)):
            raise IndexError(f"Coordinate {coord} out of bounds for dimensions {dims}")
        
        # Check cache first
        if coord in self._coord_cache:
            self.stats['cache_hits'] += 1
            return self._coord_cache[coord]
        
        # Calculate linear index using row-major order
        linear_idx = (
            x * dims[1] * dims[2] * dims[3] * dims[4] * dims[5] +
            y * dims[2] * dims[3] * dims[4] * dims[5] +
            z * dims[3] * dims[4] * dims[5] +
            w * dims[4] * dims[5] +
            v * dims[5] +
            u
        )
        
        # Ensure within bounds
        linear_idx = linear_idx % self.config.linear_size
        
        # Cache the result
        if len(self._coord_cache) < self.config.cache_size:
            self._coord_cache[coord] = linear_idx
            self._reverse_cache[linear_idx] = coord
        
        self.stats['cache_misses'] += 1
        return linear_idx
    
    def _linear_to_coord(self, linear_idx: int) -> Tuple[int, int, int, int, int, int]:
        """
        Convert linear index back to 6D coordinates.
        
        Args:
            linear_idx: Linear index
        
        Returns:
            6D coordinate tuple
        """
        if linear_idx in self._reverse_cache:
            return self._reverse_cache[linear_idx]
        
        dims = self.config.dimensions
        
        # Reverse the linear indexing calculation
        remaining = linear_idx
        coords = []
        
        for i in range(6):
            if i < 5:
                stride = np.prod(dims[i+1:])
                coord = remaining // stride
                remaining = remaining % stride
            else:
                coord = remaining
            coords.append(coord)
        
        coord_tuple = tuple(coords)
        
        # Cache if space available
        if len(self._reverse_cache) < self.config.cache_size:
            self._reverse_cache[linear_idx] = coord_tuple
            self._coord_cache[coord_tuple] = linear_idx
        
        return coord_tuple
    
    def get_offbit(self, coord: Tuple[int, int, int, int, int, int]) -> OffBit:
        """
        Get OffBit at specified 6D coordinates.
        
        Args:
            coord: 6D coordinate tuple
        
        Returns:
            OffBit at the specified coordinates
        """
        self.stats['gets'] += 1
        linear_idx = self._coord_to_linear(coord)
        
        value = self._data[linear_idx, 0]
        return OffBit(int(value))
    
    def set_offbit(self, coord: Tuple[int, int, int, int, int, int], offbit: OffBit) -> None:
        """
        Set OffBit at specified 6D coordinates.
        
        Args:
            coord: 6D coordinate tuple
            offbit: OffBit to set
        """
        self.stats['sets'] += 1
        linear_idx = self._coord_to_linear(coord)
        
        old_value = self._data[linear_idx, 0]
        new_value = offbit.value
        
        self._data[linear_idx, 0] = new_value
        
        # Update active count
        if old_value == 0 and new_value != 0:
            self.active_count += 1
        elif old_value != 0 and new_value == 0:
            self.active_count -= 1
        
        self.last_modified = time.time()
        self.access_count += 1
    
    def toggle_offbit(self, coord: Tuple[int, int, int, int, int, int]) -> None:
        """
        Toggle OffBit at specified 6D coordinates.
        
        Args:
            coord: 6D coordinate tuple
        """
        current_offbit = self.get_offbit(coord)
        toggled_offbit = current_offbit.toggle()
        self.set_offbit(coord, toggled_offbit)
    
    def get_active_offbits(self) -> List[Tuple[Tuple[int, int, int, int, int, int], OffBit]]:
        """
        Get all active OffBits with their coordinates.
        
        Returns:
            List of (coordinate, OffBit) tuples for active OffBits
        """
        active_offbits = []
        
        # Iterate through sparse matrix non-zero elements
        for linear_idx in self._data.keys():
            if isinstance(linear_idx, tuple):
                linear_idx = linear_idx[0]  # Extract row index
            
            value = self._data[linear_idx, 0]
            if value != 0:
                coord = self._linear_to_coord(linear_idx)
                offbit = OffBit(int(value))
                active_offbits.append((coord, offbit))
        
        return active_offbits
    
    def get_region(self, 
                   start_coord: Tuple[int, int, int, int, int, int],
                   end_coord: Tuple[int, int, int, int, int, int]) -> Dict[Tuple[int, int, int, int, int, int], OffBit]:
        """
        Get all OffBits in a 6D region.
        
        Args:
            start_coord: Starting coordinates (inclusive)
            end_coord: Ending coordinates (exclusive)
        
        Returns:
            Dictionary mapping coordinates to OffBits
        """
        region_offbits = {}
        
        # Generate all coordinates in the region
        ranges = [range(start, end) for start, end in zip(start_coord, end_coord)]
        
        for x in ranges[0]:
            for y in ranges[1]:
                for z in ranges[2]:
                    for w in ranges[3]:
                        for v in ranges[4]:
                            for u in ranges[5]:
                                coord = (x, y, z, w, v, u)
                                offbit = self.get_offbit(coord)
                                if offbit.is_active:
                                    region_offbits[coord] = offbit
        
        return region_offbits
    
    def apply_operation_to_region(self,
                                  start_coord: Tuple[int, int, int, int, int, int],
                                  end_coord: Tuple[int, int, int, int, int, int],
                                  operation: callable) -> None:
        """
        Apply an operation to all OffBits in a region.
        
        Args:
            start_coord: Starting coordinates (inclusive)
            end_coord: Ending coordinates (exclusive)
            operation: Function that takes an OffBit and returns a new OffBit
        """
        ranges = [range(start, end) for start, end in zip(start_coord, end_coord)]
        
        for x in ranges[0]:
            for y in ranges[1]:
                for z in ranges[2]:
                    for w in ranges[3]:
                        for v in ranges[4]:
                            for u in ranges[5]:
                                coord = (x, y, z, w, v, u)
                                current_offbit = self.get_offbit(coord)
                                new_offbit = operation(current_offbit)
                                self.set_offbit(coord, new_offbit)
    
    @property
    def current_sparsity(self) -> float:
        """Calculate the current sparsity of the bitfield."""
        if self.config.linear_size == 0:
            return 1.0
        return 1.0 - (self.active_count / self.config.linear_size)
    
    @property
    def memory_usage(self) -> int:
        """Estimate memory usage in bytes."""
        # Sparse matrix memory + cache memory
        sparse_memory = self._data.nnz * (4 + 8)  # 4 bytes for value, 8 for index
        cache_memory = len(self._coord_cache) * (6 * 4 + 4)  # 6 coords + linear index
        return sparse_memory + cache_memory
    
    def get_coherence(self) -> float:
        """
        Compute bitfield coherence based on spatial clustering and layer alignment.
        
        Returns:
            Coherence value between 0 and 1
        """
        if self.active_count == 0:
            return 1.0
        
        active_offbits = self.get_active_offbits()
        
        if len(active_offbits) < 2:
            return 1.0
        
        # Calculate spatial coherence (clustering)
        coords = [coord for coord, _ in active_offbits]
        spatial_coherence = self._calculate_spatial_coherence(coords)
        
        # Calculate layer coherence (alignment across OffBits)
        offbits = [offbit for _, offbit in active_offbits]
        layer_coherence = self._calculate_layer_coherence(offbits)
        
        # Combine coherence measures
        total_coherence = 0.6 * spatial_coherence + 0.4 * layer_coherence
        return min(1.0, total_coherence)
    
    def _calculate_spatial_coherence(self, coords: List[Tuple[int, int, int, int, int, int]]) -> float:
        """Calculate spatial coherence based on coordinate clustering."""
        if len(coords) < 2:
            return 1.0
        
        # Calculate pairwise distances in 6D space
        distances = []
        for i in range(len(coords)):
            for j in range(i + 1, len(coords)):
                dist = math.sqrt(sum((a - b) ** 2 for a, b in zip(coords[i], coords[j])))
                distances.append(dist)
        
        # Lower variance in distances indicates better clustering
        mean_dist = sum(distances) / len(distances)
        variance = sum((d - mean_dist) ** 2 for d in distances) / len(distances)
        
        # Convert variance to coherence
        coherence = 1.0 / (1.0 + variance / (mean_dist + 1e-10))
        return min(1.0, coherence)
    
    def _calculate_layer_coherence(self, offbits: List[OffBit]) -> float:
        """Calculate coherence based on layer alignment across OffBits."""
        if len(offbits) < 2:
            return 1.0
        
        # Calculate average layer coherence
        layer_coherences = [offbit.layer_coherence for offbit in offbits]
        avg_layer_coherence = sum(layer_coherences) / len(layer_coherences)
        
        # Calculate inter-OffBit coherence
        inter_coherences = []
        for i in range(len(offbits)):
            for j in range(i + 1, len(offbits)):
                coherence = offbits[i].coherence_with(offbits[j])
                inter_coherences.append(coherence)
        
        avg_inter_coherence = sum(inter_coherences) / len(inter_coherences) if inter_coherences else 1.0
        
        # Combine internal and inter-OffBit coherence
        return 0.5 * avg_layer_coherence + 0.5 * avg_inter_coherence
    
    def compute_nrci(self, target_bitfield: 'SparseBitfield') -> float:
        """
        Compute Non-Random Coherence Index with target bitfield.
        
        Args:
            target_bitfield: Target bitfield for comparison
        
        Returns:
            NRCI value between 0 and 1
        """
        # Get active OffBits from both bitfields
        self_active = dict(self.get_active_offbits())
        target_active = dict(target_bitfield.get_active_offbits())
        
        # Find all coordinates that are active in either bitfield
        all_coords = set(self_active.keys()) | set(target_active.keys())
        
        if not all_coords:
            return 1.0  # Both empty = perfect coherence
        
        # Calculate correlation between the two bitfields
        matches = 0
        total = len(all_coords)
        
        for coord in all_coords:
            self_value = self_active.get(coord, OffBit(0)).value
            target_value = target_active.get(coord, OffBit(0)).value
            
            # Calculate similarity (inverse of normalized difference)
            if self_value == 0 and target_value == 0:
                similarity = 1.0
            else:
                max_val = max(self_value, target_value, 1)
                similarity = 1.0 - abs(self_value - target_value) / max_val
            
            matches += similarity
        
        nrci = matches / total
        return max(0.0, min(1.0, nrci))
    
    def resize(self, new_config: BitfieldConfig) -> None:
        """
        Resize the bitfield with new configuration.
        
        Args:
            new_config: New configuration for the bitfield
        """
        # Save current active OffBits
        active_offbits = self.get_active_offbits()
        
        # Update configuration
        old_config = self.config
        self.config = new_config
        
        # Create new sparse matrix
        self._data = sp.dok_matrix((self.config.linear_size, 1), dtype=np.uint32)
        
        # Clear caches
        self._coord_cache.clear()
        self._reverse_cache.clear()
        
        # Restore OffBits that fit in new dimensions
        self.active_count = 0
        for coord, offbit in active_offbits:
            try:
                if all(c < d for c, d in zip(coord, self.config.dimensions)):
                    self.set_offbit(coord, offbit)
            except IndexError:
                # Skip OffBits that don't fit in new dimensions
                continue
        
        self.last_modified = time.time()
    
    def clear(self) -> None:
        """Clear all OffBits in the bitfield."""
        self._data = sp.dok_matrix((self.config.linear_size, 1), dtype=np.uint32)
        self.active_count = 0
        self.last_modified = time.time()
        self._coord_cache.clear()
        self._reverse_cache.clear()
    
    def copy(self) -> 'SparseBitfield':
        """
        Create a copy of the bitfield.
        
        Returns:
            Copy of the bitfield
        """
        new_bitfield = SparseBitfield(self.config)
        new_bitfield._data = self._data.copy()
        new_bitfield.active_count = self.active_count
        new_bitfield.last_modified = self.last_modified
        new_bitfield.access_count = self.access_count
        new_bitfield.stats = self.stats.copy()
        return new_bitfield
    
    def save_to_file(self, filepath: str, compress: bool = True) -> None:
        """
        Save bitfield to file.
        
        Args:
            filepath: Path to save file
            compress: Whether to compress the file
        """
        data = {
            'config': self.config,
            'sparse_data': self._data,
            'active_count': self.active_count,
            'last_modified': self.last_modified,
            'stats': self.stats
        }
        
        if compress:
            with gzip.open(filepath, 'wb') as f:
                pickle.dump(data, f)
        else:
            with open(filepath, 'wb') as f:
                pickle.dump(data, f)
    
    @classmethod
    def load_from_file(cls, filepath: str, compressed: bool = True) -> 'SparseBitfield':
        """
        Load bitfield from file.
        
        Args:
            filepath: Path to load file
            compressed: Whether the file is compressed
        
        Returns:
            Loaded SparseBitfield
        """
        if compressed:
            with gzip.open(filepath, 'rb') as f:
                data = pickle.load(f)
        else:
            with open(filepath, 'rb') as f:
                data = pickle.load(f)
        
        bitfield = cls(data['config'])
        bitfield._data = data['sparse_data']
        bitfield.active_count = data['active_count']
        bitfield.last_modified = data['last_modified']
        bitfield.stats = data['stats']
        
        return bitfield
    
    def __len__(self) -> int:
        return self.config.linear_size
    
    def __str__(self) -> str:
        return (f"SparseBitfield(size={self.config.linear_size}, "
                f"active={self.active_count}, "
                f"sparsity={self.current_sparsity:.4f}, "
                f"coherence={self.get_coherence():.4f})")
    
    def __repr__(self) -> str:
        return (f"SparseBitfield(dimensions={self.config.dimensions}, "
                f"active_count={self.active_count}, "
                f"memory_usage={self.memory_usage} bytes)")


# Factory functions for creating bitfields with specific configurations
def create_mobile_bitfield() -> SparseBitfield:
    """Create a bitfield optimized for mobile devices (4GB RAM)."""
    config = BitfieldConfig(
        dimensions=(50, 50, 50, 3, 2, 2),
        max_offbits=10000,
        sparsity_target=0.005,
        cache_size=1000
    )
    return SparseBitfield(config)


def create_desktop_bitfield() -> SparseBitfield:
    """Create a bitfield optimized for desktop systems (8GB RAM)."""
    config = BitfieldConfig(
        dimensions=(170, 170, 170, 5, 2, 2),
        max_offbits=1000000,
        sparsity_target=0.01,
        cache_size=10000
    )
    return SparseBitfield(config)


def create_server_bitfield() -> SparseBitfield:
    """Create a bitfield optimized for server systems (unlimited RAM)."""
    config = BitfieldConfig(
        dimensions=(300, 300, 300, 10, 5, 5),
        max_offbits=10000000,
        sparsity_target=0.02,
        cache_size=100000
    )
    return SparseBitfield(config)


if __name__ == "__main__":
    # Test the SparseBitfield implementation
    print("Testing SparseBitfield implementation...")
    
    # Create test bitfield
    bitfield = create_desktop_bitfield()
    print(f"Created bitfield: {bitfield}")
    
    # Test basic operations
    coord1 = (10, 20, 30, 1, 0, 1)
    coord2 = (11, 21, 31, 1, 0, 1)
    
    offbit1 = create_quantum_offbit(100, 150, 200)
    offbit2 = create_quantum_offbit(110, 160, 210)
    
    bitfield.set_offbit(coord1, offbit1)
    bitfield.set_offbit(coord2, offbit2)
    
    print(f"Set 2 OffBits, active count: {bitfield.active_count}")
    print(f"Sparsity: {bitfield.current_sparsity:.6f}")
    print(f"Memory usage: {bitfield.memory_usage} bytes")
    
    # Test retrieval
    retrieved = bitfield.get_offbit(coord1)
    print(f"Retrieved OffBit: {retrieved}")
    print(f"Matches original: {retrieved.value == offbit1.value}")
    
    # Test coherence
    coherence = bitfield.get_coherence()
    print(f"Bitfield coherence: {coherence:.4f}")
    
    # Test region operations
    region = bitfield.get_region((10, 20, 30, 1, 0, 1), (12, 22, 32, 2, 1, 2))
    print(f"Region contains {len(region)} active OffBits")
    
    # Test statistics
    print(f"Statistics: {bitfield.stats}")
    
    print("\nSparseBitfield implementation test completed successfully!")

