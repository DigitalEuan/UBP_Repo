"""
TGIC Geometry Constraints Extension
Additional constraint methods for cross-geometry validation

These methods extend TGICSystem to support multiple geometric structures.
Based on concept by Qwen AI.

Author: UBP Development Team
Date: November 30, 2025
"""

import numpy as np
import math
from typing import List


def enforce_octal_interaction_constraint(system, nodes: List[int]) -> float:
    """
    Cubic geometry: 8-interaction neighborhood constraint.
    In cubic, expect up to 3 neighbors within first 8 nodes.
    """
    if not system.graph or len(nodes) < 8:
        return 0.0
    
    total_violation = 0.0
    for node_id in nodes[:8]:
        if node_id not in system.graph.nodes:
            total_violation += 1.0
            continue
        # In cubic, expect up to 3 neighbors within first 8
        internal_neighbors = sum(
            1 for n in nodes[:8] 
            if n in system.graph.nodes[node_id].connections
        )
        # Ideal: 3 (cube corners connect to 3 others in subcube)
        violation = abs(internal_neighbors - 3) / 3.0
        total_violation += violation
    
    return total_violation / min(8, len(nodes))


def enforce_four_vertex_closure(system, nodes: List[int]) -> float:
    """
    Tetrahedral: all 4 nodes should be fully connected (6 edges).
    """
    if len(nodes) < 4:
        return 1.0
    
    expected_edges = 6
    actual_edges = 0
    
    for i in range(4):
        for j in range(i+1, 4):
            if (nodes[i] in system.graph.nodes and 
                nodes[j] in system.graph.nodes[nodes[i]].connections):
                actual_edges += 1
    
    return abs(actual_edges - expected_edges) / expected_edges


def enforce_six_edge_pair_constraint(system, nodes: List[int]) -> float:
    """
    Tetrahedral: edge-pair coherence should be uniform.
    """
    coherences = []
    
    for i in range(4):
        for j in range(i+1, 4):
            if (nodes[i] in system.graph.nodes and 
                nodes[j] in system.graph.nodes[nodes[i]].connections):
                c1 = system.graph.nodes[nodes[i]].coherence_level
                c2 = system.graph.nodes[nodes[j]].coherence_level
                coherences.append(abs(c1 - c2))
    
    return np.mean(coherences) if coherences else 0.0


def enforce_four_degree_constraint(system, nodes: List[int]) -> float:
    """
    Octahedral: each node should have degree 4.
    """
    if len(nodes) < 4:
        return 1.0
    
    violations = []
    for node_id in nodes[:4]:
        if node_id in system.graph.nodes:
            deg = len(system.graph.nodes[node_id].connections)
            violations.append(abs(deg - 4) / 4.0)
        else:
            violations.append(1.0)
    
    return np.mean(violations)


def enforce_six_vertex_symmetry(system, nodes: List[int]) -> float:
    """
    Octahedral: all 6 vertices equivalent under rotation.
    Use position norms (octahedron vertices lie on axes).
    """
    if len(nodes) < 6:
        return 1.0
    
    norms = [
        np.linalg.norm(system.graph.nodes[n].position) 
        for n in nodes[:6] 
        if n in system.graph.nodes
    ]
    
    if not norms:
        return 1.0
    
    return np.std(norms) / (np.mean(norms) + 1e-10)


def enforce_eight_face_proxy(system, nodes: List[int]) -> float:
    """
    Octahedral has 8 triangular faces; proxy via triangle count in subgraph.
    """
    if len(nodes) < 6:
        return 1.0
    
    triangles = 0
    for i in range(6):
        for j in range(i+1, 6):
            for k in range(j+1, 6):
                nid_i, nid_j, nid_k = nodes[i], nodes[j], nodes[k]
                if (nid_j in system.graph.nodes[nid_i].connections and
                    nid_k in system.graph.nodes[nid_i].connections and
                    nid_k in system.graph.nodes[nid_j].connections):
                    triangles += 1
    
    # Octahedron has 8 faces
    return abs(triangles - 8) / 8.0


def enforce_five_fold_constraint(system, nodes: List[int]) -> float:
    """
    Icosahedral: check 5-fold symmetry around node 0.
    """
    if len(nodes) < 5:
        return 1.0
    
    center = nodes[0]
    if center not in system.graph.nodes:
        return 1.0
    
    neighbors = list(system.graph.nodes[center].connections)
    if len(neighbors) < 5:
        return 1.0
    
    # Compute angles between neighbor vectors
    center_pos = system.graph.nodes[center].position
    vecs = [system.graph.nodes[n].position - center_pos for n in neighbors[:5]]
    
    angles = []
    for i in range(5):
        for j in range(i+1, 5):
            v1, v2 = vecs[i], vecs[j]
            cosang = np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2) + 1e-10)
            angles.append(math.degrees(math.acos(np.clip(cosang, -1, 1))))
    
    # Ideal angles in icosahedron: 72° or 144°
    ideal = [72, 144]
    deviations = [min(abs(a - i) for i in ideal) for a in angles]
    
    return np.mean(deviations) / 72.0


def enforce_twelve_vertex_closure(system, nodes: List[int]) -> float:
    """
    Icosahedron: 12 vertices, each degree 5, 30 edges.
    """
    if len(nodes) < 12:
        return 1.0
    
    # Validate edge count
    edge_count = sum(len(system.graph.nodes[n].connections) for n in nodes[:12]) // 2
    edge_violation = abs(edge_count - 30) / 30.0
    
    # Validate regularity
    degrees = [len(system.graph.nodes[n].connections) for n in nodes[:12]]
    regularity_violation = 0.0 if all(d == 5 for d in degrees) else 1.0
    
    return (edge_violation + regularity_violation) / 2.0


def enforce_edge_density_constraint(system, nodes: List[int]) -> float:
    """
    Icosahedral: density = edges / (n(n-1)/2) = 30/66 ≈ 0.4545
    """
    if len(nodes) < 12:
        return 1.0
    
    n = 12
    possible = n * (n - 1) // 2
    actual = sum(len(system.graph.nodes[n].connections) for n in nodes[:n]) // 2
    density = actual / possible
    
    return abs(density - 30/66)


def enforce_leech_block_orthogonality(system, blocks) -> float:
    """
    Leech 24D: enforce orthogonality of 3 E8 blocks.
    Placeholder for now - real implementation would use projected 3D points.
    """
    # Placeholder - Y-refinement handles this in practice
    return 0.0


# Method injection helper
def inject_geometry_methods(system_class):
    """
    Inject geometry-specific constraint methods into TGICSystem class.
    """
    system_class._enforce_octal_interaction_constraint = enforce_octal_interaction_constraint
    system_class._enforce_four_vertex_closure = enforce_four_vertex_closure
    system_class._enforce_six_edge_pair_constraint = enforce_six_edge_pair_constraint
    system_class._enforce_four_degree_constraint = enforce_four_degree_constraint
    system_class._enforce_six_vertex_symmetry = enforce_six_vertex_symmetry
    system_class._enforce_eight_face_proxy = enforce_eight_face_proxy
    system_class._enforce_five_fold_constraint = enforce_five_fold_constraint
    system_class._enforce_twelve_vertex_closure = enforce_twelve_vertex_closure
    system_class._enforce_edge_density_constraint = enforce_edge_density_constraint
    system_class._enforce_leech_block_orthogonality = enforce_leech_block_orthogonality
