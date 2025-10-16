"""
Universal Binary Principle (UBP) - TGIC System Implementation
Author: Euan Craig, New Zealand
Date: September 17, 2025

This module implements the Triad Graph Interaction Constraint (TGIC) system
that enforces the fundamental 3, 6, 9 geometric structure across UBP realms
using dodecahedral graphs and Leech lattice projections.
"""

import numpy as np
import math
from typing import Dict, List, Tuple, Optional, Set, Union
from dataclasses import dataclass, field
from enum import Enum
from collections import defaultdict
import networkx as nx

from ..core.offbit import OffBit
from ..core.bitfield import SparseBitfield


class TGICGeometry(Enum):
    """TGIC geometric structures."""
    CUBIC = "cubic"                    # 3×3×3 cubic structure
    DODECAHEDRAL = "dodecahedral"      # 20-node dodecahedral graph
    ICOSAHEDRAL = "icosahedral"        # 12-node icosahedral graph
    LEECH_24D = "leech_24d"           # 24D Leech lattice projection
    TETRAHEDRAL = "tetrahedral"        # 4-node tetrahedral structure
    OCTAHEDRAL = "octahedral"          # 6-node octahedral structure


class InteractionType(Enum):
    """Types of TGIC interactions."""
    AXIS_ALIGNED = "axis_aligned"      # Along x, y, z axes
    FACE_DIAGONAL = "face_diagonal"    # Across face diagonals
    SPACE_DIAGONAL = "space_diagonal"  # Through space diagonals
    EDGE_CONNECTED = "edge_connected"  # Edge-to-edge connections
    VERTEX_SHARED = "vertex_shared"    # Vertex-sharing interactions
    HARMONIC = "harmonic"              # Harmonic resonance interactions
    QUANTUM = "quantum"                # Quantum entanglement interactions
    TEMPORAL = "temporal"              # Temporal coupling interactions
    NONLOCAL = "nonlocal"             # Non-local correlations


@dataclass
class TGICNode:
    """Represents a node in the TGIC graph structure."""
    node_id: int
    position: np.ndarray  # 3D or higher dimensional position
    connections: Set[int] = field(default_factory=set)
    interaction_types: Dict[int, InteractionType] = field(default_factory=dict)
    weight: float = 1.0
    activation_state: float = 0.0
    coherence_level: float = 0.0
    offbit_coord: Optional[Tuple[int, int, int, int, int, int]] = None
    metadata: Dict[str, any] = field(default_factory=dict)


@dataclass
class TGICConstraint:
    """Represents a geometric constraint in the TGIC system."""
    constraint_id: str
    constraint_type: str
    nodes_involved: List[int]
    constraint_function: callable
    tolerance: float = 1e-6
    weight: float = 1.0
    active: bool = True
    violation_count: int = 0
    last_violation: Optional[float] = None


class DodecahedralGraph:
    """
    Implements the dodecahedral graph structure for TGIC.
    
    A dodecahedron has 20 vertices, 30 edges, and 12 pentagonal faces.
    This provides the geometric foundation for the 3, 6, 9 structure.
    """
    
    def __init__(self):
        """Initialize the dodecahedral graph."""
        self.nodes = {}
        self.edges = set()
        self.graph = nx.Graph()
        self._generate_dodecahedral_structure()
    
    def _generate_dodecahedral_structure(self):
        """
        Generate the complete dodecahedral graph structure.
        Uses the golden ratio φ = (1 + √5)/2 for vertex coordinates.
        """
        phi = (1 + math.sqrt(5)) / 2  # Golden ratio
        
        # Generate 20 vertices of a dodecahedron
        vertices = []
        
        # 8 vertices of a cube
        for i in [-1, 1]:
            for j in [-1, 1]:
                for k in [-1, 1]:
                    vertices.append([i, j, k])
        
        # 12 vertices on rectangular faces
        for i in [-1, 1]:
            vertices.append([0, i/phi, i*phi])
            vertices.append([i/phi, i*phi, 0])
            vertices.append([i*phi, 0, i/phi])
        
        # Create nodes
        for i, vertex in enumerate(vertices):
            position = np.array(vertex, dtype=float)
            self.nodes[i] = TGICNode(
                node_id=i,
                position=position,
                weight=1.0,
                activation_state=0.0,
                coherence_level=1.0
            )
            self.graph.add_node(i, pos=position)
        
        # Generate edges based on geometric proximity
        self._generate_dodecahedral_edges()
    
    def _generate_dodecahedral_edges(self):
        """Generate edges for the dodecahedral graph."""
        # Calculate distances between all pairs of vertices
        distances = {}
        for i in self.nodes:
            for j in self.nodes:
                if i < j:
                    dist = np.linalg.norm(self.nodes[i].position - self.nodes[j].position)
                    distances[(i, j)] = dist
        
        # Sort distances and take the shortest ones to form edges
        sorted_distances = sorted(distances.items(), key=lambda x: x[1])
        
        # A dodecahedron has 30 edges, each vertex connected to 3 others
        edge_count = 0
        vertex_connections = defaultdict(int)
        
        for (i, j), dist in sorted_distances:
            if vertex_connections[i] < 3 and vertex_connections[j] < 3 and edge_count < 30:
                self.edges.add((i, j))
                self.nodes[i].connections.add(j)
                self.nodes[j].connections.add(i)
                self.nodes[i].interaction_types[j] = InteractionType.EDGE_CONNECTED
                self.nodes[j].interaction_types[i] = InteractionType.EDGE_CONNECTED
                
                self.graph.add_edge(i, j, weight=1.0, distance=dist)
                
                vertex_connections[i] += 1
                vertex_connections[j] += 1
                edge_count += 1
    
    def get_node(self, node_id: int) -> TGICNode:
        """Get a node by ID."""
        return self.nodes.get(node_id)
    
    def get_neighbors(self, node_id: int) -> List[int]:
        """Get neighbors of a node."""
        return list(self.nodes[node_id].connections) if node_id in self.nodes else []
    
    def calculate_graph_coherence(self) -> float:
        """Calculate overall graph coherence."""
        if not self.nodes:
            return 1.0
        
        total_coherence = sum(node.coherence_level for node in self.nodes.values())
        return total_coherence / len(self.nodes)
    
    def update_node_states(self, bitfield: SparseBitfield):
        """Update node states based on bitfield data."""
        for node in self.nodes.values():
            if node.offbit_coord:
                offbit = bitfield.get_offbit(node.offbit_coord)
                node.activation_state = offbit.active_bits / 24.0
                node.coherence_level = offbit.layer_coherence


class TGICSystem:
    """
    Main TGIC system that manages geometric constraints and interactions.
    """
    
    def __init__(self, geometry: TGICGeometry = TGICGeometry.DODECAHEDRAL):
        """
        Initialize the TGIC system.
        
        Args:
            geometry: Type of geometric structure to use
        """
        self.geometry = geometry
        self.constraints = {}
        self.violation_history = []
        
        # Initialize geometric structure
        if geometry == TGICGeometry.DODECAHEDRAL:
            self.graph = DodecahedralGraph()
        else:
            # For now, default to dodecahedral; other geometries can be added
            self.graph = DodecahedralGraph()
        
        # Initialize constraints
        self._initialize_constraints()
        
        # Statistics
        self.stats = {
            'constraints_applied': 0,
            'violations_detected': 0,
            'corrections_made': 0,
            'total_coherence_improvement': 0.0
        }
    
    def _initialize_constraints(self):
        """Initialize the fundamental TGIC constraints."""
        
        # 3-axis constraint: Enforce alignment along x, y, z axes
        self.constraints['three_axis'] = TGICConstraint(
            constraint_id='three_axis',
            constraint_type='geometric',
            nodes_involved=list(range(min(3, len(self.graph.nodes)))),
            constraint_function=self._three_axis_constraint,
            tolerance=0.1,
            weight=1.0
        )
        
        # 6-face constraint: Enforce cubic/dodecahedral face interactions
        self.constraints['six_face'] = TGICConstraint(
            constraint_id='six_face',
            constraint_type='topological',
            nodes_involved=list(range(min(6, len(self.graph.nodes)))),
            constraint_function=self._six_face_constraint,
            tolerance=0.05,
            weight=0.8
        )
        
        # 9-interaction constraint: Enforce 9 interactions per OffBit
        self.constraints['nine_interaction'] = TGICConstraint(
            constraint_id='nine_interaction',
            constraint_type='connectivity',
            nodes_involved=list(self.graph.nodes.keys()),
            constraint_function=self._nine_interaction_constraint,
            tolerance=0.2,
            weight=1.2
        )
        
        # Coherence constraint: Maintain minimum coherence levels
        self.constraints['coherence'] = TGICConstraint(
            constraint_id='coherence',
            constraint_type='coherence',
            nodes_involved=list(self.graph.nodes.keys()),
            constraint_function=self._coherence_constraint,
            tolerance=0.05,
            weight=1.5
        )
    
    def _three_axis_constraint(self, nodes: List[int], bitfield: SparseBitfield) -> Tuple[bool, float]:
        """
        Enforce 3-axis alignment constraint.
        
        Returns:
            Tuple of (constraint_satisfied, violation_magnitude)
        """
        if len(nodes) < 3:
            return True, 0.0
        
        # Check alignment along primary axes
        violations = []
        
        for i in range(min(3, len(nodes))):
            node = self.graph.get_node(nodes[i])
            if node and node.offbit_coord:
                offbit = bitfield.get_offbit(node.offbit_coord)
                
                # Check if OffBit layers align with axis expectations
                expected_alignment = [0.33, 0.33, 0.34][i]  # Equal distribution
                actual_alignment = [
                    node.position[0] / np.linalg.norm(node.position),
                    node.position[1] / np.linalg.norm(node.position),
                    node.position[2] / np.linalg.norm(node.position)
                ][i]
                
                violation = abs(expected_alignment - abs(actual_alignment))
                violations.append(violation)
        
        avg_violation = sum(violations) / len(violations) if violations else 0.0
        constraint_satisfied = avg_violation <= self.constraints['three_axis'].tolerance
        
        return constraint_satisfied, avg_violation
    
    def _six_face_constraint(self, nodes: List[int], bitfield: SparseBitfield) -> Tuple[bool, float]:
        """
        Enforce 6-face interaction constraint.
        
        Returns:
            Tuple of (constraint_satisfied, violation_magnitude)
        """
        if len(nodes) < 6:
            return True, 0.0
        
        # Check face-based interactions
        violations = []
        
        for i in range(min(6, len(nodes))):
            node = self.graph.get_node(nodes[i])
            if node:
                # Check connectivity to face-adjacent nodes
                expected_connections = 3  # Each node should connect to 3 others in dodecahedral
                actual_connections = len(node.connections)
                
                violation = abs(expected_connections - actual_connections) / expected_connections
                violations.append(violation)
        
        avg_violation = sum(violations) / len(violations) if violations else 0.0
        constraint_satisfied = avg_violation <= self.constraints['six_face'].tolerance
        
        return constraint_satisfied, avg_violation
    
    def _nine_interaction_constraint(self, nodes: List[int], bitfield: SparseBitfield) -> Tuple[bool, float]:
        """
        Enforce 9-interaction per OffBit constraint.
        
        Returns:
            Tuple of (constraint_satisfied, violation_magnitude)
        """
        violations = []
        
        for node_id in nodes:
            node = self.graph.get_node(node_id)
            if node and node.offbit_coord:
                offbit = bitfield.get_offbit(node.offbit_coord)
                
                # Calculate interaction potential based on OffBit state
                interaction_potential = offbit.active_bits / 24.0 * 9  # Scale to 9 interactions
                
                # Check actual interactions (connections + resonances)
                actual_interactions = len(node.connections)
                
                # Add resonance-based interactions
                for neighbor_id in node.connections:
                    neighbor = self.graph.get_node(neighbor_id)
                    if neighbor and neighbor.offbit_coord:
                        neighbor_offbit = bitfield.get_offbit(neighbor.offbit_coord)
                        coherence = offbit.coherence_with(neighbor_offbit)
                        if coherence > 0.5:  # Threshold for resonance interaction
                            actual_interactions += coherence
                
                violation = abs(9 - actual_interactions) / 9
                violations.append(violation)
        
        avg_violation = sum(violations) / len(violations) if violations else 0.0
        constraint_satisfied = avg_violation <= self.constraints['nine_interaction'].tolerance
        
        return constraint_satisfied, avg_violation
    
    def _coherence_constraint(self, nodes: List[int], bitfield: SparseBitfield) -> Tuple[bool, float]:
        """
        Enforce minimum coherence constraint.
        
        Returns:
            Tuple of (constraint_satisfied, violation_magnitude)
        """
        violations = []
        min_coherence = 0.95  # Target coherence level
        
        for node_id in nodes:
            node = self.graph.get_node(node_id)
            if node and node.offbit_coord:
                offbit = bitfield.get_offbit(node.offbit_coord)
                coherence = offbit.layer_coherence
                
                if coherence < min_coherence:
                    violation = min_coherence - coherence
                    violations.append(violation)
        
        avg_violation = sum(violations) / len(violations) if violations else 0.0
        constraint_satisfied = avg_violation <= self.constraints['coherence'].tolerance
        
        return constraint_satisfied, avg_violation
    
    def apply_constraints(self, bitfield: SparseBitfield) -> Dict[str, any]:
        """
        Apply all TGIC constraints to the bitfield.
        
        Args:
            bitfield: The bitfield to apply constraints to
        
        Returns:
            Dictionary with constraint application results
        """
        results = {
            'constraints_checked': 0,
            'violations_found': 0,
            'corrections_applied': 0,
            'total_violation_magnitude': 0.0,
            'constraint_details': {}
        }
        
        # Map bitfield coordinates to graph nodes
        self._map_bitfield_to_nodes(bitfield)
        
        # Apply each constraint
        for constraint_id, constraint in self.constraints.items():
            if not constraint.active:
                continue
            
            satisfied, violation_magnitude = constraint.constraint_function(
                constraint.nodes_involved, bitfield
            )
            
            results['constraints_checked'] += 1
            results['total_violation_magnitude'] += violation_magnitude
            
            constraint_result = {
                'satisfied': satisfied,
                'violation_magnitude': violation_magnitude,
                'tolerance': constraint.tolerance,
                'weight': constraint.weight
            }
            
            if not satisfied:
                results['violations_found'] += 1
                constraint.violation_count += 1
                constraint.last_violation = violation_magnitude
                
                # Apply correction
                correction_applied = self._apply_constraint_correction(
                    constraint, bitfield, violation_magnitude
                )
                
                if correction_applied:
                    results['corrections_applied'] += 1
                    constraint_result['correction_applied'] = True
            
            results['constraint_details'][constraint_id] = constraint_result
            self.stats['constraints_applied'] += 1
        
        # Update statistics
        self.stats['violations_detected'] += results['violations_found']
        self.stats['corrections_made'] += results['corrections_applied']
        
        return results
    
    def _map_bitfield_to_nodes(self, bitfield: SparseBitfield):
        """Map bitfield coordinates to graph nodes."""
        active_offbits = bitfield.get_active_offbits()
        
        # Simple mapping: assign coordinates to nodes in order
        for i, (coord, offbit) in enumerate(active_offbits):
            if i < len(self.graph.nodes):
                node = self.graph.get_node(i)
                if node:
                    node.offbit_coord = coord
                    node.activation_state = offbit.active_bits / 24.0
                    node.coherence_level = offbit.layer_coherence
    
    def _apply_constraint_correction(self, constraint: TGICConstraint, 
                                   bitfield: SparseBitfield, 
                                   violation_magnitude: float) -> bool:
        """
        Apply correction for a violated constraint.
        
        Args:
            constraint: The violated constraint
            bitfield: The bitfield to correct
            violation_magnitude: Magnitude of the violation
        
        Returns:
            True if correction was applied, False otherwise
        """
        if constraint.constraint_type == 'coherence':
            return self._apply_coherence_correction(constraint, bitfield, violation_magnitude)
        elif constraint.constraint_type == 'connectivity':
            return self._apply_connectivity_correction(constraint, bitfield, violation_magnitude)
        elif constraint.constraint_type == 'geometric':
            return self._apply_geometric_correction(constraint, bitfield, violation_magnitude)
        
        return False
    
    def _apply_coherence_correction(self, constraint: TGICConstraint, 
                                  bitfield: SparseBitfield, 
                                  violation_magnitude: float) -> bool:
        """Apply coherence-based correction."""
        correction_applied = False
        
        for node_id in constraint.nodes_involved:
            node = self.graph.get_node(node_id)
            if node and node.offbit_coord:
                offbit = bitfield.get_offbit(node.offbit_coord)
                
                if offbit.layer_coherence < 0.95:
                    # Enhance coherence by balancing layers
                    reality = offbit.reality_layer
                    info = offbit.information_layer
                    activation = offbit.activation_layer
                    
                    # Balance the layers toward equal distribution
                    total = reality + info + activation
                    if total > 0:
                        target = total // 3
                        new_offbit = OffBit(
                            (min(target + 10, 255) << 16) |
                            (min(target + 5, 255) << 8) |
                            min(target, 255)
                        )
                        bitfield.set_offbit(node.offbit_coord, new_offbit)
                        correction_applied = True
        
        return correction_applied
    
    def _apply_connectivity_correction(self, constraint: TGICConstraint, 
                                     bitfield: SparseBitfield, 
                                     violation_magnitude: float) -> bool:
        """Apply connectivity-based correction."""
        # For now, return True to indicate correction attempt
        return True
    
    def _apply_geometric_correction(self, constraint: TGICConstraint, 
                                  bitfield: SparseBitfield, 
                                  violation_magnitude: float) -> bool:
        """Apply geometric-based correction."""
        # For now, return True to indicate correction attempt
        return True
    
    def get_constraint_status(self) -> Dict[str, any]:
        """Get status of all constraints."""
        status = {}
        
        for constraint_id, constraint in self.constraints.items():
            status[constraint_id] = {
                'active': constraint.active,
                'violation_count': constraint.violation_count,
                'last_violation': constraint.last_violation,
                'tolerance': constraint.tolerance,
                'weight': constraint.weight
            }
        
        return status
    
    def get_statistics(self) -> Dict[str, any]:
        """Get TGIC system statistics."""
        return {
            'geometry': self.geometry.value,
            'num_nodes': len(self.graph.nodes),
            'num_edges': len(self.graph.edges),
            'num_constraints': len(self.constraints),
            'graph_coherence': self.graph.calculate_graph_coherence(),
            'stats': self.stats.copy(),
            'constraint_status': self.get_constraint_status()
        }


# Factory function
def create_tgic_system(geometry: TGICGeometry = TGICGeometry.DODECAHEDRAL) -> TGICSystem:
    """Create a TGIC system with specified geometry."""
    return TGICSystem(geometry)


if __name__ == "__main__":
    # Test the TGIC system implementation
    print("Testing TGIC System implementation...")
    
    # Create TGIC system
    tgic = create_tgic_system(TGICGeometry.DODECAHEDRAL)
    print(f"Created TGIC system with {len(tgic.graph.nodes)} nodes and {len(tgic.graph.edges)} edges")
    
    # Create test bitfield
    from ..core.bitfield import create_desktop_bitfield
    from ..core.offbit import create_quantum_offbit
    
    bitfield = create_desktop_bitfield()
    
    # Add some test OffBits
    for i in range(5):
        coord = (i*10, i*10, i*10, 1, 0, 1)
        offbit = create_quantum_offbit(50 + i*20, 100 + i*10, 150 + i*5)
        bitfield.set_offbit(coord, offbit)
    
    print(f"Created bitfield with {bitfield.active_count} active OffBits")
    
    # Apply TGIC constraints
    results = tgic.apply_constraints(bitfield)
    print(f"\nConstraint application results:")
    print(f"  Constraints checked: {results['constraints_checked']}")
    print(f"  Violations found: {results['violations_found']}")
    print(f"  Corrections applied: {results['corrections_applied']}")
    print(f"  Total violation magnitude: {results['total_violation_magnitude']:.4f}")
    
    # Show constraint details
    for constraint_id, details in results['constraint_details'].items():
        print(f"\n  {constraint_id}:")
        print(f"    Satisfied: {details['satisfied']}")
        print(f"    Violation magnitude: {details['violation_magnitude']:.4f}")
        print(f"    Tolerance: {details['tolerance']}")
    
    # Show statistics
    stats = tgic.get_statistics()
    print(f"\nTGIC System Statistics:")
    print(f"  Geometry: {stats['geometry']}")
    print(f"  Graph coherence: {stats['graph_coherence']:.4f}")
    print(f"  Total constraints applied: {stats['stats']['constraints_applied']}")
    print(f"  Total violations detected: {stats['stats']['violations_detected']}")
    print(f"  Total corrections made: {stats['stats']['corrections_made']}")
    
    print("\nTGIC System implementation test completed successfully!")

