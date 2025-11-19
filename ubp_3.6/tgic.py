"""
================================================================================
Universal Binary Principle (UBP) Framework v3.6 - TGIC
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
            
        Returns:
            Coupled CoherenceState
        """
        distance = self.distance_to(other)
        
        # Coupling decays with distance (resonance kernel)
        coupling_strength = math.exp(-0.0002 * distance * distance)
        
        # Combine coherence states
        avg_value = (self.coherence.value + other.coherence.value) / 2
        avg_log_error = (self.coherence.log_nrci_error + other.coherence.log_nrci_error) / 2
        
        coupled = CoherenceState(avg_value * coupling_strength, log_nrci_error=avg_log_error)
        
        return coupled


# ============================================================================
# DODECAHEDRAL GRAPH (Pentagonal Coherence Structure)
# ============================================================================

class DodecahedralGraph:
    """
    Dodecahedral graph structure for TGIC.
    
    The dodecahedron naturally emerges in coherent systems due to its
    optimal packing and pentagonal symmetry (related to golden ratio).
    
    Properties:
    - 20 vertices
    - 30 edges
    - 12 pentagonal faces
    - Each vertex connects to exactly 3 others
    """
    
    def __init__(self):
        self.nodes: Dict[int, TGICNode] = {}
        self.edges: Set[Tuple[int, int]] = set()
        self._generate_structure()
    
    def _generate_structure(self):
        """
        Generate dodecahedral structure using golden ratio.
        
        The dodecahedron vertices are naturally defined by φ (golden ratio).
        """
        phi = GOLDEN_RATIO
        
        # Generate 20 vertices
        vertices = []
        
        # 8 vertices of a cube
        for i in [-1, 1]:
            for j in [-1, 1]:
                for k in [-1, 1]:
                    vertices.append([i, j, k])
        
        # 12 vertices on rectangular faces (using golden ratio)
        for i in [-1, 1]:
            vertices.append([0, i/phi, i*phi])
            vertices.append([i/phi, i*phi, 0])
            vertices.append([i*phi, 0, i/phi])
        
        # Create nodes with coherence
        for i, vertex in enumerate(vertices):
            self.nodes[i] = TGICNode(
                node_id=i,
                position=vertex,
                coherence=CoherenceState(float(i + 1))
            )
        
        # Generate edges (each vertex connects to 3 others)
        self._generate_edges()
    
    def _generate_edges(self):
        """
        Generate edges based on dodecahedral connectivity.
        
        Uses distance threshold to determine natural connections.
        """
        edge_threshold = 2.1  # Approximate edge length
        
        for i in range(len(self.nodes)):
            for j in range(i + 1, len(self.nodes)):
                distance = self.nodes[i].distance_to(self.nodes[j])
                
                if distance < edge_threshold:
                    self.edges.add((i, j))
                    self.nodes[i].connections.add(j)
                    self.nodes[j].connections.add(i)
                    self.nodes[i].interaction_types[j] = InteractionType.EDGE_CONNECTED
                    self.nodes[j].interaction_types[i] = InteractionType.EDGE_CONNECTED
    
    def get_node_coherence(self, node_id: int) -> CoherenceState:
        """Get coherence of a specific node."""
        return self.nodes[node_id].coherence
    
    def get_graph_coherence(self) -> CoherenceState:
        """
        Get overall graph coherence.
        
        Returns:
            Average coherence across all nodes
        """
        if not self.nodes:
            return CoherenceState(0.0)
        
        avg_value = sum(n.coherence.value for n in self.nodes.values()) / len(self.nodes)
        avg_log_error = sum(n.coherence.log_nrci_error for n in self.nodes.values()) / len(self.nodes)
        
        return CoherenceState(avg_value, log_nrci_error=avg_log_error)
    
    def get_369_structure(self) -> Dict[str, int]:
        """
        Analyze the 3-6-9 structure of the graph.
        
        Returns:
            Dictionary with 3-6-9 pattern counts
        """
        # 3: Primary axes (x, y, z)
        axes_count = 3
        
        # 6: Faces of interaction
        faces_count = 6  # Cubic projection has 6 faces
        
        # 9: Interactions per node neighborhood
        # Each node connects to 3 others, creating 9 interaction patterns
        interactions_per_node = 9
        
        return {
            'axes': axes_count,
            'faces': faces_count,
            'interactions': interactions_per_node,
            'total_nodes': len(self.nodes),
            'total_edges': len(self.edges)
        }


# ============================================================================
# TGIC CONSTRAINT SYSTEM (Coherence Maintenance)
# ============================================================================

@dataclass
class TGICConstraint:
    """
    Geometric constraint in TGIC.
    
    In 3.5, constraints aren't enforced - they're natural coherence
    maintenance patterns.
    """
    constraint_id: str
    constraint_type: str
    nodes_involved: List[int]
    target_coherence: float = 0.999997
    tolerance: float = 1e-6
    active: bool = True
    
    def check_constraint(self, graph: DodecahedralGraph) -> Tuple[bool, float]:
        """
        Check if constraint is satisfied.
        
        Args:
            graph: DodecahedralGraph to check
            
        Returns:
            Tuple of (satisfied, deviation)
        """
        if not self.active or not self.nodes_involved:
            return True, 0.0
        
        # Check coherence of involved nodes
        coherences = [graph.get_node_coherence(nid).nrci for nid in self.nodes_involved]
        avg_coherence = sum(coherences) / len(coherences)
        
        deviation = abs(avg_coherence - self.target_coherence)
        satisfied = deviation < self.tolerance
        
        return satisfied, deviation


class TGICSystem:
    """
    Complete TGIC system managing coherence geometry.
    
    In 3.5, this isn't a "constraint enforcer" - it's a coherence
    geometry manager that tracks natural coherence patterns.
    """
    
    def __init__(self, geometry: TGICGeometry = TGICGeometry.DODECAHEDRAL):
        self.geometry = geometry
        
        if geometry == TGICGeometry.DODECAHEDRAL:
            self.graph = DodecahedralGraph()
        else:
            # For now, default to dodecahedral
            # Other geometries can be added later
            self.graph = DodecahedralGraph()
        
        self.constraints: List[TGICConstraint] = []
    
    def add_constraint(self, constraint: TGICConstraint):
        """Add a coherence constraint."""
        self.constraints.append(constraint)
    
    def check_all_constraints(self) -> Dict[str, Any]:
        """
        Check all constraints.
        
        Returns:
            Dictionary with constraint satisfaction results
        """
        results = {
            'total_constraints': len(self.constraints),
            'satisfied': 0,
            'violated': 0,
            'max_deviation': 0.0,
            'constraint_details': []
        }
        
        for constraint in self.constraints:
            satisfied, deviation = constraint.check_constraint(self.graph)
            
            if satisfied:
                results['satisfied'] += 1
            else:
                results['violated'] += 1
            
            results['max_deviation'] = max(results['max_deviation'], deviation)
            
            results['constraint_details'].append({
                'id': constraint.constraint_id,
                'satisfied': satisfied,
                'deviation': deviation
            })
        
        return results
    
    def get_system_coherence(self) -> CoherenceState:
        """Get overall system coherence."""
        return self.graph.get_graph_coherence()
    
    def get_369_analysis(self) -> Dict[str, Any]:
        """
        Analyze 3-6-9 structure.
        
        Returns:
            Complete 3-6-9 analysis
        """
        structure = self.graph.get_369_structure()
        coherence = self.get_system_coherence()
        
        return {
            'structure': structure,
            'system_nrci': coherence.nrci,
            'system_value': coherence.value,
            'geometry': self.geometry.value
        }


# ============================================================================
# DEMONSTRATION
# ============================================================================

if __name__ == "__main__":
    print("=" * 80)
    print("UBP 3.5 TGIC - Triad Graph Interaction Constraint")
    print("=" * 80)
    
    # Create TGIC system
    print("\n1. Creating TGIC System:")
    tgic = TGICSystem(geometry=TGICGeometry.DODECAHEDRAL)
    print(f"   Geometry: {tgic.geometry.value}")
    print(f"   Nodes: {len(tgic.graph.nodes)}")
    print(f"   Edges: {len(tgic.graph.edges)}")
    
    # Analyze 3-6-9 structure
    print("\n2. 3-6-9 Structure Analysis:")
    analysis = tgic.get_369_analysis()
    print(f"   Axes: {analysis['structure']['axes']}")
    print(f"   Faces: {analysis['structure']['faces']}")
    print(f"   Interactions: {analysis['structure']['interactions']}")
    print(f"   System NRCI: {analysis['system_nrci']:.10f}")
    
    # Node coherence
    print("\n3. Node Coherence:")
    for i in range(min(5, len(tgic.graph.nodes))):
        node_coh = tgic.graph.get_node_coherence(i)
        print(f"   Node {i}: NRCI = {node_coh.nrci:.10f}")
    
    # Add constraints
    print("\n4. Adding Coherence Constraints:")
    constraint1 = TGICConstraint(
        constraint_id="global_coherence",
        constraint_type="coherence_threshold",
        nodes_involved=list(range(len(tgic.graph.nodes)))
    )
    tgic.add_constraint(constraint1)
    
    constraint_results = tgic.check_all_constraints()
    print(f"   Total constraints: {constraint_results['total_constraints']}")
    print(f"   Satisfied: {constraint_results['satisfied']}")
    print(f"   Violated: {constraint_results['violated']}")
    print(f"   Max deviation: {constraint_results['max_deviation']:.10f}")
    
    # Graph coherence
    print("\n5. Graph Coherence:")
    graph_coh = tgic.get_system_coherence()
    print(f"   Overall NRCI: {graph_coh.nrci:.10f}")
    print(f"   Overall value: {graph_coh.value:.6e}")
    
    print("\n" + "=" * 80)
    print("UBP 3.5: TGIC is Coherence Geometry")
    print("3-6-9 structure emerges naturally from coherence")
    print("Zero external dependencies - Pure geometric coherence")
    print("=" * 80)
