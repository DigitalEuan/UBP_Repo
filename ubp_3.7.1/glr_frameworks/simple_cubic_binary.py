"""
UBP 3.7.1 - Simple Cubic Binary GLR Framework
==============================================

Simple cubic lattice with binary OffBit toggle logic.

Lattice Structure:
- Simple cubic grid with integer coordinates
- 6 nearest neighbors (±x, ±y, ±z)
- Each site contains a 24-bit OffBit

Author: Euan R A Craig, New Zealand
Date: November 28, 2025
Version: 3.7.1
"""

from typing import Tuple
from .glr_base_binary import GLRFramework, LatticeSite
import sys; import os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "core")); from state import OffBit
from coherence_substrate import CoherenceState


class SimpleCubicGLR(GLRFramework):
    """
    Simple cubic lattice with binary toggle logic.
    
    Connectivity: 6 nearest neighbors (coordination number = 6)
    """
    
    def _create_lattice(self):
        """Create a simple cubic lattice."""
        nx, ny, nz = self.dimensions
        
        for i in range(nx):
            for j in range(ny):
                for k in range(nz):
                    coords = (i, j, k)
                    state = OffBit(self.initial_state)
                    coherence = CoherenceState(1.0)  # Start with perfect coherence
                    
                    site = LatticeSite(
                        coordinates=coords,
                        state=state,
                        coherence=coherence,
                        neighbors=[]
                    )
                    
                    self.sites[coords] = site
    
    def _connect_neighbors(self):
        """Connect each site to its 6 nearest neighbors."""
        nx, ny, nz = self.dimensions
        
        for coords, site in self.sites.items():
            i, j, k = coords
            
            # 6 nearest neighbors: ±x, ±y, ±z
            neighbor_offsets = [
                (1, 0, 0), (-1, 0, 0),   # ±x
                (0, 1, 0), (0, -1, 0),   # ±y
                (0, 0, 1), (0, 0, -1)    # ±z
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
