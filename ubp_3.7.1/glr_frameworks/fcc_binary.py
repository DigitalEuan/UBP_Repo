"""
UBP 3.7.1 - FCC Binary GLR Framework
=====================================

Face-Centered Cubic (FCC) lattice with binary OffBit toggle logic.

Lattice Structure:
- FCC structure (like copper, aluminum, gold)
- 12 nearest neighbors
- Each site contains a 24-bit OffBit

Author: Euan R A Craig, New Zealand
Date: November 28, 2025
Version: 3.7.1
"""

from typing import Tuple
from .glr_base_binary import GLRFramework, LatticeSite
import sys; import os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "core")); from state import OffBit
from coherence_substrate import CoherenceState


class FCCGLR(GLRFramework):
    """
    Face-Centered Cubic lattice with binary toggle logic.
    
    Connectivity: 12 nearest neighbors (coordination number = 12)
    """
    
    def _create_lattice(self):
        """Create an FCC lattice."""
        nx, ny, nz = self.dimensions
        
        # FCC lattice: corner sites + face-centered sites
        for i in range(nx):
            for j in range(ny):
                for k in range(nz):
                    # Corner site
                    coords = (2*i, 2*j, 2*k)
                    state = OffBit(self.initial_state)
                    coherence = CoherenceState(1.0)
                    
                    site = LatticeSite(
                        coordinates=coords,
                        state=state,
                        coherence=coherence,
                        neighbors=[]
                    )
                    
                    self.sites[coords] = site
                    
                    # Face-centered sites (3 per unit cell)
                    face_offsets = [
                        (1, 1, 0),  # xy face
                        (1, 0, 1),  # xz face
                        (0, 1, 1)   # yz face
                    ]
                    
                    for di, dj, dk in face_offsets:
                        face_coords = (2*i + di, 2*j + dj, 2*k + dk)
                        face_state = OffBit(self.initial_state)
                        face_coherence = CoherenceState(1.0)
                        
                        face_site = LatticeSite(
                            coordinates=face_coords,
                            state=face_state,
                            coherence=face_coherence,
                            neighbors=[]
                        )
                        
                        self.sites[face_coords] = face_site
    
    def _connect_neighbors(self):
        """Connect each site to its 12 nearest neighbors."""
        # For FCC, each site has 12 nearest neighbors
        # These are at distance √2 in units of the primitive lattice constant
        
        for coords, site in self.sites.items():
            i, j, k = coords
            
            # 12 nearest neighbors for FCC
            neighbor_offsets = [
                # Face diagonal neighbors
                (1, 1, 0), (1, -1, 0), (-1, 1, 0), (-1, -1, 0),  # xy plane
                (1, 0, 1), (1, 0, -1), (-1, 0, 1), (-1, 0, -1),  # xz plane
                (0, 1, 1), (0, 1, -1), (0, -1, 1), (0, -1, -1)   # yz plane
            ]
            
            for di, dj, dk in neighbor_offsets:
                ni, nj, nk = i + di, j + dj, k + dk
                
                neighbor_coords = (ni, nj, nk)
                neighbor = self.sites.get(neighbor_coords)
                
                if neighbor is not None:
                    site.neighbors.append(neighbor)
