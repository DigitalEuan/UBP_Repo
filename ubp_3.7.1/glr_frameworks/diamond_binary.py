"""
UBP 3.7.1 - Diamond Binary GLR Framework
=========================================

Diamond cubic lattice with binary OffBit toggle logic.

Lattice Structure:
- Diamond cubic structure (like carbon diamond)
- 4 nearest neighbors in tetrahedral arrangement
- Each site contains a 24-bit OffBit

The diamond lattice can be constructed as two interpenetrating FCC lattices.

Author: Euan R A Craig, New Zealand
Date: November 28, 2025
Version: 3.7.1
"""

from typing import Tuple
from .glr_base_binary import GLRFramework, LatticeSite
import sys; import os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "core")); from state import OffBit
from coherence_substrate import CoherenceState


class DiamondGLR(GLRFramework):
    """
    Diamond cubic lattice with binary toggle logic.
    
    Connectivity: 4 nearest neighbors (coordination number = 4)
    Tetrahedral bonding like carbon diamond.
    """
    
    def _create_lattice(self):
        """Create a diamond cubic lattice."""
        nx, ny, nz = self.dimensions
        
        # Diamond lattice: two interpenetrating FCC sublattices
        # Sublattice A: (i, j, k) where i+j+k is even
        # Sublattice B: (i, j, k) + (1,1,1)/4 (offset by quarter unit cell)
        
        for i in range(nx):
            for j in range(ny):
                for k in range(nz):
                    # Only include sites where i+j+k is even (sublattice A)
                    # and their offset partners (sublattice B)
                    if (i + j + k) % 2 == 0:
                        # Sublattice A site
                        coords_a = (i, j, k)
                        state_a = OffBit(self.initial_state)
                        coherence_a = CoherenceState(1.0)
                        
                        site_a = LatticeSite(
                            coordinates=coords_a,
                            state=state_a,
                            coherence=coherence_a,
                            neighbors=[]
                        )
                        
                        self.sites[coords_a] = site_a
    
    def _connect_neighbors(self):
        """Connect each site to its 4 tetrahedral neighbors."""
        nx, ny, nz = self.dimensions
        
        for coords, site in self.sites.items():
            i, j, k = coords
            
            # 4 tetrahedral neighbors at (±1, ±1, ±1)/2 relative positions
            # In integer coordinates, these are the 4 nearest sites with opposite parity
            neighbor_offsets = [
                (1, 1, 1),
                (1, -1, -1),
                (-1, 1, -1),
                (-1, -1, 1)
            ]
            
            for di, dj, dk in neighbor_offsets:
                ni, nj, nk = i + di, j + dj, k + dk
                
                # Periodic boundary conditions
                ni = ni % nx
                nj = nj % ny
                nk = nk % nz
                
                neighbor_coords = (ni, nj, nk)
                neighbor = self.sites.get(neighbor_coords)
                
                if neighbor is not None:
                    site.neighbors.append(neighbor)
