"""
UBP 3.7.1 - Binary GLR Frameworks Package
==========================================

Pure binary toggle logic implementations of Geometric Lattice Realm (GLR) frameworks.

All frameworks use 24-bit OffBit states and discrete toggle operations.
No continuous phases, vectors, or Platonic solids.

Available Frameworks:
- SimpleCubicGLR: Simple cubic lattice (6 neighbors)
- DiamondGLR: Diamond cubic lattice (4 neighbors, tetrahedral)
- FCCGLR: Face-centered cubic lattice (12 neighbors)
- H3IcosahedralGLR: H3 Coxeter group (icosahedral symmetry)
- H4120CellGLR: H4 Coxeter group (120-cell symmetry)

Author: Euan R A Craig, New Zealand
Date: November 28, 2025
Version: 3.7.1
"""

from .glr_base_binary import GLRFramework, LatticeSite
from .simple_cubic_binary import SimpleCubicGLR
from .diamond_binary import DiamondGLR
from .fcc_binary import FCCGLR
from .h3_icosahedral_binary import H3IcosahedralGLR
from .h4_120cell_binary import H4120CellGLR

__all__ = [
    'GLRFramework',
    'LatticeSite',
    'SimpleCubicGLR',
    'DiamondGLR',
    'FCCGLR',
    'H3IcosahedralGLR',
    'H4120CellGLR'
]
