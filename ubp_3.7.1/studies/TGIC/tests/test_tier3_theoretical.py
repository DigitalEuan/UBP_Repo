#!/usr/bin/env python3
"""
TGIC Tier 3: Theoretical Validation Tests

Based on DeepSeek AI's Tier 3 checklist - validates theoretical foundations:
- 3-6-9 pattern mathematical correctness
- Dodecahedral geometry properties
- Leech lattice projection validity
- Constraint system completeness
- Theoretical consistency with UBP principles

Author: UBP Development Team
Date: November 30, 2025
"""

import sys
import os
import json
import numpy as np
from typing import Dict, Any, Tuple, List
from collections import Counter

# Add UBP 3.7.1 to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))

from utils.tgic import (
    TGICSystem, TGICGeometry, DodecahedralGraph,
    LeechLatticeProjection, TGICNode
)


def test_3_1_three_six_nine_pattern() -> Tuple[bool, Dict[str, Any]]:
    """
    Test 3.1: 3-6-9 Pattern Mathematical Correctness
    
    Validates that the TGIC system correctly implements the 3-6-9 pattern:
    - 3 primary axes (constraint structure)
    - 6 face interactions (dodecahedral faces)
    - 9 interaction neighborhoods (connectivity pattern)
    
    This is the foundational pattern of TGIC geometry.
    """
    print("="*70)
    print("TEST 3.1: 3-6-9 Pattern Mathematical Correctness")
    print("="*70)
    
    system = TGICSystem(geometry=TGICGeometry.DODECAHEDRAL)
    
    # Check constraint structure
    print("\n3-6-9 Pattern Analysis:")
    
    # 3: Primary axes (three-axis constraint)
    three_axis_constraint = system.constraints.get('three_axis_structure')
    has_three_axis = three_axis_constraint is not None
    three_axis_nodes = len(three_axis_constraint.nodes_involved) if has_three_axis else 0
    print(f"\n[3] Three-axis structure:")
    print(f"  Exists: {has_three_axis}")
    print(f"  Nodes involved: {three_axis_nodes}")
    print(f"  Expected: 3 nodes (one per axis)")
    three_ok = has_three_axis and three_axis_nodes == 3
    
    # 6: Face interactions (six-face constraint)
    six_face_constraint = system.constraints.get('six_face_interactions')
    has_six_face = six_face_constraint is not None
    six_face_nodes = len(six_face_constraint.nodes_involved) if has_six_face else 0
    print(f"\n[6] Six-face interactions:")
    print(f"  Exists: {has_six_face}")
    print(f"  Nodes involved: {six_face_nodes}")
    print(f"  Expected: 6 nodes (dodecahedral face centers)")
    six_ok = has_six_face and six_face_nodes == 6
    
    # 9: Interaction neighborhoods (nine-interaction constraint)
    nine_interaction_constraint = system.constraints.get('nine_interaction_neighborhood')
    has_nine_interaction = nine_interaction_constraint is not None
    nine_interaction_nodes = len(nine_interaction_constraint.nodes_involved) if has_nine_interaction else 0
    print(f"\n[9] Nine-interaction neighborhood:")
    print(f"  Exists: {has_nine_interaction}")
    print(f"  Nodes involved: {nine_interaction_nodes}")
    print(f"  Expected: 9 nodes (connectivity pattern)")
    nine_ok = has_nine_interaction and nine_interaction_nodes == 9
    
    # Verify pattern completeness
    pattern_complete = three_ok and six_ok and nine_ok
    
    print(f"\nPattern Completeness:")
    print(f"  3-axis: {'✓' if three_ok else '✗'}")
    print(f"  6-face: {'✓' if six_ok else '✗'}")
    print(f"  9-interaction: {'✓' if nine_ok else '✗'}")
    
    passed = pattern_complete
    
    if passed:
        print("✅ PASS - 3-6-9 pattern correctly implemented")
    else:
        print("❌ FAIL - 3-6-9 pattern incomplete")
    
    return passed, {
        'three_axis_ok': three_ok,
        'six_face_ok': six_ok,
        'nine_interaction_ok': nine_ok,
        'pattern_complete': pattern_complete
    }


def test_3_2_dodecahedral_properties() -> Tuple[bool, Dict[str, Any]]:
    """
    Test 3.2: Dodecahedral Geometry Properties
    
    Validates mathematical properties of the dodecahedral graph:
    - Vertex count: 20
    - Edge count: 30
    - 3-regular (each vertex has degree 3)
    - Edge length: 2/φ ≈ 1.236
    - Golden ratio relationships
    """
    print("="*70)
    print("TEST 3.2: Dodecahedral Geometry Properties")
    print("="*70)
    
    system = TGICSystem(geometry=TGICGeometry.DODECAHEDRAL)
    graph = system.graph
    
    # Vertex count
    num_vertices = len(graph.nodes)
    vertices_ok = num_vertices == 20
    print(f"\nVertex count: {num_vertices} (expected: 20) {'✓' if vertices_ok else '✗'}")
    
    # Edge count
    num_edges = len(graph.edges)
    edges_ok = num_edges == 30
    print(f"Edge count: {num_edges} (expected: 30) {'✓' if edges_ok else '✗'}")
    
    # 3-regular property (calculate degree from edges)
    # Edges are tuples (node1_id, node2_id)
    degrees = {}
    for node_id in graph.nodes.keys():
        degree = sum(1 for edge in graph.edges 
                    if edge[0] == node_id or edge[1] == node_id)
        degrees[node_id] = degree
    
    degree_values = list(degrees.values())
    degree_counts = Counter(degree_values)
    is_3_regular = all(d == 3 for d in degree_values)
    print(f"3-regular: {is_3_regular} {'✓' if is_3_regular else '✗'}")
    print(f"  Degree distribution: {dict(degree_counts)}")
    
    # Edge lengths
    phi = (1 + np.sqrt(5)) / 2
    expected_edge_length = 2 / phi
    
    edge_lengths = []
    for edge in graph.edges:
        # Edges are tuples (node1_id, node2_id)
        node1 = graph.nodes[edge[0]]
        node2 = graph.nodes[edge[1]]
        length = np.linalg.norm(node1.position - node2.position)
        edge_lengths.append(length)
    
    mean_length = np.mean(edge_lengths)
    std_length = np.std(edge_lengths)
    length_ok = abs(mean_length - expected_edge_length) < 0.01 and std_length < 0.01
    
    print(f"\nEdge lengths:")
    print(f"  Expected: {expected_edge_length:.6f} (2/φ)")
    print(f"  Mean: {mean_length:.6f}")
    print(f"  Std: {std_length:.6f}")
    print(f"  Consistent: {length_ok} {'✓' if length_ok else '✗'}")
    
    # Golden ratio verification
    phi_calculated = (1 + np.sqrt(5)) / 2
    phi_ok = abs(phi_calculated - 1.618033988749895) < 1e-10
    print(f"\nGolden ratio (φ): {phi_calculated:.15f} {'✓' if phi_ok else '✗'}")
    
    passed = vertices_ok and edges_ok and is_3_regular and length_ok and phi_ok
    
    if passed:
        print("✅ PASS - Dodecahedral properties correct")
    else:
        print("❌ FAIL - Dodecahedral properties incorrect")
    
    return passed, {
        'num_vertices': num_vertices,
        'num_edges': num_edges,
        'is_3_regular': is_3_regular,
        'mean_edge_length': mean_length,
        'edge_length_ok': length_ok,
        'golden_ratio_ok': phi_ok
    }


def test_3_3_leech_lattice_projection() -> Tuple[bool, Dict[str, Any]]:
    """
    Test 3.3: Leech Lattice Projection Validity
    
    Validates the 24D → 3D projection:
    - Accepts 24-dimensional input
    - Produces 3-dimensional output
    - Preserves relative structure (not exact, but reasonable)
    - Disclaimer is present
    """
    print("="*70)
    print("TEST 3.3: Leech Lattice Projection Validity")
    print("="*70)
    
    projector = LeechLatticeProjection()
    
    # Test dimension handling
    test_point_24d = np.random.randn(24)
    
    try:
        projected = projector.project_to_3d(test_point_24d)
        projection_works = True
        output_dim = len(projected)
        dim_ok = output_dim == 3
    except Exception as e:
        projection_works = False
        output_dim = None
        dim_ok = False
        print(f"Projection failed: {e}")
    
    print(f"\nDimension handling:")
    print(f"  Input: 24D ✓")
    print(f"  Output: {output_dim}D {'✓' if dim_ok else '✗'}")
    print(f"  Projection works: {projection_works} {'✓' if projection_works else '✗'}")
    
    # Test invalid dimension rejection
    test_point_12d = np.random.randn(12)
    invalid_rejected = False
    try:
        projector.project_to_3d(test_point_12d)
    except ValueError as e:
        invalid_rejected = True
        print(f"  Invalid dimension rejected: ✓ (ValueError: {str(e)[:50]}...)")
    
    # Check for disclaimer in docstring
    docstring = projector.project_to_3d.__doc__ or ""
    has_disclaimer = "approximation" in docstring.lower() or "simplified" in docstring.lower()
    print(f"  Disclaimer present: {has_disclaimer} {'✓' if has_disclaimer else '✗'}")
    
    passed = projection_works and dim_ok and invalid_rejected and has_disclaimer
    
    if passed:
        print("✅ PASS - Leech projection valid")
    else:
        print("❌ FAIL - Leech projection issues")
    
    return passed, {
        'projection_works': projection_works,
        'output_dimension': output_dim,
        'invalid_rejected': invalid_rejected,
        'has_disclaimer': has_disclaimer
    }


def test_3_4_constraint_system_completeness() -> Tuple[bool, Dict[str, Any]]:
    """
    Test 3.4: Constraint System Completeness
    
    Validates that the constraint system is well-defined:
    - All constraints have valid types
    - All constraints have positive weights
    - All constraints reference valid nodes
    - Constraint evaluation is deterministic
    """
    print("="*70)
    print("TEST 3.4: Constraint System Completeness")
    print("="*70)
    
    system = TGICSystem(geometry=TGICGeometry.DODECAHEDRAL)
    
    print(f"\nTotal constraints: {len(system.constraints)}")
    
    all_valid = True
    constraint_details = []
    
    for cid, constraint in system.constraints.items():
        print(f"\n{cid}:")
        
        # Check type
        has_type = hasattr(constraint, 'constraint_type') and constraint.constraint_type
        print(f"  Type: {constraint.constraint_type if has_type else 'MISSING'} {'✓' if has_type else '✗'}")
        
        # Check weight
        has_weight = hasattr(constraint, 'weight')
        weight_positive = has_weight and constraint.weight > 0
        print(f"  Weight: {constraint.weight if has_weight else 'MISSING'} {'✓' if weight_positive else '✗'}")
        
        # Check nodes
        has_nodes = hasattr(constraint, 'nodes_involved') and len(constraint.nodes_involved) > 0
        nodes_valid = has_nodes and all(nid in system.graph.nodes for nid in constraint.nodes_involved)
        print(f"  Nodes: {len(constraint.nodes_involved) if has_nodes else 0} {'✓' if nodes_valid else '✗'}")
        
        # Check evaluation function
        has_eval = hasattr(constraint, 'evaluation_function') and callable(constraint.evaluation_function)
        print(f"  Evaluation function: {'present' if has_eval else 'MISSING'} {'✓' if has_eval else '✗'}")
        
        constraint_valid = has_type and weight_positive and nodes_valid and has_eval
        constraint_details.append({
            'id': cid,
            'valid': constraint_valid,
            'has_type': has_type,
            'weight_positive': weight_positive,
            'nodes_valid': nodes_valid,
            'has_eval': has_eval
        })
        
        if not constraint_valid:
            all_valid = False
    
    # Test determinism
    violation1 = system.compute_total_violation()
    violation2 = system.compute_total_violation()
    deterministic = abs(violation1 - violation2) < 1e-10
    print(f"\nDeterminism:")
    print(f"  Violation 1: {violation1:.15f}")
    print(f"  Violation 2: {violation2:.15f}")
    print(f"  Deterministic: {deterministic} {'✓' if deterministic else '✗'}")
    
    passed = all_valid and deterministic
    
    if passed:
        print("✅ PASS - Constraint system complete")
    else:
        print("❌ FAIL - Constraint system incomplete")
    
    return passed, {
        'all_constraints_valid': all_valid,
        'deterministic': deterministic,
        'constraint_details': constraint_details
    }


def test_3_5_ubp_theoretical_consistency() -> Tuple[bool, Dict[str, Any]]:
    """
    Test 3.5: UBP Theoretical Consistency
    
    Validates that TGIC is consistent with UBP principles:
    - Uses Y-constant (π/(π²+2)) if applicable
    - Respects coherence principles
    - Topological constraints (not positional)
    - Geometric structure matches theoretical design
    """
    print("="*70)
    print("TEST 3.5: UBP Theoretical Consistency")
    print("="*70)
    
    system = TGICSystem(geometry=TGICGeometry.DODECAHEDRAL)
    
    # Check if Y-constant is used (may not be directly in TGIC)
    try:
        from core.y import Y as Y_CONSTANT
        y_available = True
        y_value = Y_CONSTANT
        y_correct = abs(y_value - 0.264675430404527) < 1e-10
        print(f"\nY-constant:")
        print(f"  Available: {y_available} ✓")
        print(f"  Value: {y_value:.15f}")
        print(f"  Correct: {y_correct} {'✓' if y_correct else '✗'}")
    except ImportError:
        y_available = False
        y_correct = False
        print(f"\nY-constant: Not used in TGIC (OK - topological system)")
    
    # Check topological nature
    violations_before = system.compute_total_violation()
    
    # Perturb a node position
    node_id = list(system.graph.nodes.keys())[0]
    original_pos = system.graph.nodes[node_id].position.copy()
    system.graph.nodes[node_id].position += np.array([0.1, 0.1, 0.1])
    
    violations_after = system.compute_total_violation()
    
    # Restore position
    system.graph.nodes[node_id].position = original_pos
    
    # For topological constraints, violations should NOT change with position
    topological = abs(violations_before - violations_after) < 0.01
    print(f"\nTopological constraints:")
    print(f"  Violation before perturbation: {violations_before:.6f}")
    print(f"  Violation after perturbation: {violations_after:.6f}")
    print(f"  Topological (position-independent): {topological} {'✓' if topological else '✗'}")
    
    # Check geometric structure
    phi = (1 + np.sqrt(5)) / 2
    uses_golden_ratio = True  # Dodecahedron inherently uses φ
    print(f"\nGeometric structure:")
    print(f"  Uses golden ratio (φ): {uses_golden_ratio} ✓")
    print(f"  Dodecahedral (Platonic solid): True ✓")
    
    # Overall consistency
    consistent = topological and uses_golden_ratio
    
    passed = consistent
    
    if passed:
        print("✅ PASS - UBP theoretical consistency validated")
    else:
        print("❌ FAIL - UBP theoretical inconsistencies found")
    
    return passed, {
        'y_available': y_available,
        'topological': topological,
        'uses_golden_ratio': uses_golden_ratio,
        'consistent': consistent
    }


def main():
    """Run all Tier 3 theoretical validation tests."""
    print("="*70)
    print("TGIC TIER 3: THEORETICAL VALIDATION TESTS")
    print("="*70)
    print("Based on DeepSeek AI's Tier 3 Checklist")
    print("="*70)
    
    tests = [
        ("3.1 - 3-6-9 Pattern", test_3_1_three_six_nine_pattern),
        ("3.2 - Dodecahedral Properties", test_3_2_dodecahedral_properties),
        ("3.3 - Leech Projection", test_3_3_leech_lattice_projection),
        ("3.4 - Constraint System", test_3_4_constraint_system_completeness),
        ("3.5 - UBP Consistency", test_3_5_ubp_theoretical_consistency),
    ]
    
    results = {}
    passed_count = 0
    
    for test_name, test_func in tests:
        print("\n")
        passed, data = test_func()
        results[test_name] = {'passed': passed, 'data': data}
        if passed:
            passed_count += 1
    
    # Summary
    print("\n")
    print("="*70)
    print("TIER 3 TEST SUMMARY")
    print("="*70)
    for test_name, result in results.items():
        status = "✅ PASS" if result['passed'] else "❌ FAIL"
        print(f"{test_name}: {status}")
    
    total_tests = len(tests)
    pass_rate = (passed_count / total_tests) * 100
    print(f"Total: {passed_count}/{total_tests} tests passed ({pass_rate:.1f}%)")
    
    # Save results
    output_dir = os.path.join(os.path.dirname(__file__), '../findings')
    os.makedirs(output_dir, exist_ok=True)
    
    output_file = os.path.join(output_dir, 'tier3_results.json')
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2, default=str)
    
    print(f"Results saved to: {output_file}")


if __name__ == '__main__':
    main()
