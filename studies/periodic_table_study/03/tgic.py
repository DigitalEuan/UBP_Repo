================================================================================
Universal Binary Principle (UBP) Framework v3.5 - TGIC
Triad Graph Interaction Constraint
Author: Euan Craig, New Zealand
Date: November 12, 2025
================================================================================

TGIC as coherence geometry.

**Paradigm Shift in 3.5**:
TGIC isn't a "constraint system" - it's the natural geometric structure
that emerges from coherence. The 3-6-9 pattern is intrinsic to coherent
systems, not imposed.

**Zero Dependencies**: Only Python stdlib + coherence_substrate
"""

import math
from typing import Dict, List, Tuple, Optional, Set, Any
from dataclasses import dataclass, field
from enum import Enum

from coherence_substrate import CoherenceState, Y, Y_INVERSE, GOLDEN_RATIO


# ============================================================================
# TGIC GEOMETRY (Natural Coherence Structures)
# ============================================================================

class TGICGeometry(Enum):
    """
    Natural geometric structures that emerge in coherent systems.
    """
    CUBIC = "cubic"                    # 3×3×3 cubic (3-fold symmetry)
    DODECAHEDRAL = "dodecahedral"      # 20-node (pentagonal symmetry)
    ICOSAHEDRAL = "icosahedral"        # 12-node (triangular symmetry)
    LEECH_24D = "leech_24d"           # 24D Leech lattice
    TETRAHEDRAL = "tetrahedral"        # 4-node (simplest 3D)
    OCTAHEDRAL = "octahedral"          # 6-node (6-fold symmetry)


class InteractionType(Enum):
    """
    Types of coherence interactions in TGIC.
    """
    AXIS_ALIGNED = "axis_aligned"      # Along primary axes
    FACE_DIAGONAL = "face_diagonal"    # Across faces
    SPACE_DIAGONAL = "space_diagonal"  # Through volume
    EDGE_CONNECTED = "edge_connected"  # Edge connections
    VERTEX_SHARED = "vertex_shared"    # Vertex sharing
    HARMONIC = "harmonic"              # Harmonic resonance
    QUANTUM = "quantum"                # Quantum entanglement
    TEMPORAL = "temporal"              # Temporal coupling
    NONLOCAL = "nonlocal"             # Non-local correlations


# ============================================================================
# TGIC NODE (Coherence Point)
# ============================================================================

@dataclass
class TGICNode:
    """
    A node in the TGIC graph - represents a coherence point.
    
    In 3.5, nodes aren't just graph vertices - they're coherence states
    with geometric positions.
    """
    node_id: int
    position: List[float]  # 3D or higher dimensional position
    coherence: CoherenceState
    connections: Set[int] = field(default_factory=set)
    interaction_types: Dict[int, InteractionType] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def distance_to(self, other: 'TGICNode') -> float:
        """
        Calculate distance to another node.
        
        Args:
            other: Another TGICNode
            
        Returns:
            Euclidean distance
        """
        if len(self.position) != len(other.position):
            raise ValueError("Nodes must have same dimensionality")
        
        return math.sqrt(sum((a - b) ** 2 for a, b in zip(self.position, other.position)))
    
    def coherence_coupling(self, other: 'TGICNode') -> CoherenceState:
        """
        Calculate coherence coupling with another node.
        
        Coupling strength depends on distance and coherence quality.
        
        Args:
            other: Another TGICNode
            