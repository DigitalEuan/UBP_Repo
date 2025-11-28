"""
UBP 3.7.1 - Binary GLR Framework Base
======================================

Pure binary toggle logic foundation for all GLR (Geometric Lattice Realm) frameworks.

This module provides the abstract base class and core data structures for implementing
GLR frameworks using OffBit (24-bit binary) states instead of continuous/vector/phase mathematics.

Key Principles:
- Every lattice site contains a 24-bit OffBit
- All state changes are discrete toggle operations
- No continuous phases, vectors, or Platonic solids
- Geometry defined by lattice connectivity, not embedding

Author: Euan R A Craig, New Zealand
Date: November 28, 2025
Version: 3.7.1
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Tuple, List, Dict, Optional
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'core'))

from state import OffBit
from coherence_substrate import CoherenceState


@dataclass
class LatticeSite:
    """
    A single point in a GLR lattice.
    
    Attributes:
        coordinates: Integer coordinates (i, j, k) in the lattice
        state: 24-bit binary state (OffBit)
        coherence: Coherence tracking for this site
        neighbors: List of connected neighboring sites
    """
    coordinates: Tuple[int, int, int]
    state: OffBit
    coherence: CoherenceState
    neighbors: List["LatticeSite"] = field(default_factory=list)
    
    def __hash__(self):
        return hash(self.coordinates)
    
    def __eq__(self, other):
        if not isinstance(other, LatticeSite):
            return False
        return self.coordinates == other.coordinates


class GLRFramework(ABC):
    """
    Abstract base class for all binary GLR frameworks.
    
    This class defines the common interface and core functionality for GLR frameworks
    that use pure binary toggle logic.
    """
    
    def __init__(self, dimensions: Tuple[int, int, int], initial_state: Optional[int] = None):
        """
        Initialize the GLR framework.
        
        Args:
            dimensions: (nx, ny, nz) - number of sites in each dimension
            initial_state: Initial 24-bit state for all sites (default: 0)
        """
        self.dimensions = dimensions
        self.initial_state = initial_state if initial_state is not None else 0
        self.sites: Dict[Tuple[int, int, int], LatticeSite] = {}
        
        # Create the lattice
        self._create_lattice()
        
        # Connect neighbors
        self._connect_neighbors()
    
    @abstractmethod
    def _create_lattice(self):
        """
        Create the lattice sites.
        
        This method must be implemented by each concrete GLR framework to define
        the specific lattice structure.
        """
        pass
    
    @abstractmethod
    def _connect_neighbors(self):
        """
        Connect neighboring sites.
        
        This method must be implemented by each concrete GLR framework to define
        the specific neighbor connectivity pattern.
        """
        pass
    
    def get_site(self, coordinates: Tuple[int, int, int]) -> Optional[LatticeSite]:
        """
        Get a lattice site by coordinates.
        
        Args:
            coordinates: (i, j, k) coordinates
            
        Returns:
            LatticeSite if it exists, None otherwise
        """
        return self.sites.get(coordinates)
    
    def toggle_site(self, coordinates: Tuple[int, int, int], toggle_pattern: int):
        """
        Toggle a site's state using XOR with a toggle pattern.
        
        Args:
            coordinates: (i, j, k) coordinates of the site
            toggle_pattern: 24-bit pattern to XOR with the site's state
        """
        site = self.get_site(coordinates)
        if site is None:
            raise ValueError(f"No site at coordinates {coordinates}")
        
        # Perform XOR toggle
        new_value = site.state.value ^ toggle_pattern
        site.state = OffBit(new_value, site.coherence)
    
    def evolve(self):
        """
        Evolve the lattice by one time step using binary toggle rules.
        
        The default rule is: XOR each site with the XOR of all its neighbors.
        This can be overridden by subclasses for different toggle rules.
        """
        # Calculate new states for all sites
        new_states = {}
        
        for coords, site in self.sites.items():
            # XOR all neighbor states
            neighbor_xor = 0
            for neighbor in site.neighbors:
                neighbor_xor ^= neighbor.state.value
            
            # XOR site with neighbors
            new_value = site.state.value ^ neighbor_xor
            new_states[coords] = new_value
        
        # Apply new states
        for coords, new_value in new_states.items():
            site = self.sites[coords]
            site.state = OffBit(new_value, site.coherence)
    
    def get_total_hamming_weight(self) -> int:
        """
        Get the total Hamming weight (number of 1-bits) across all sites.
        
        Returns:
            Total number of 1-bits in the entire lattice
        """
        total = 0
        for site in self.sites.values():
            total += site.state.hamming_weight()
        return total
    
    def get_lattice_coherence(self) -> float:
        """
        Get the average coherence across all sites.
        
        Returns:
            Average coherence value
        """
        if not self.sites:
            return 0.0
        
        total_coherence = sum(site.coherence.value for site in self.sites.values())
        return total_coherence / len(self.sites)
    
    def __repr__(self):
        return (f"{self.__class__.__name__}(dimensions={self.dimensions}, "
                f"sites={len(self.sites)}, coherence={self.get_lattice_coherence():.6f})")
