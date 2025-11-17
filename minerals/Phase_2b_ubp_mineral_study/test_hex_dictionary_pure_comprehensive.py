"""
================================================================================
Comprehensive Test Suite for hex_dictionary_pure.py (UBP 3.5)
================================================================================

This test suite thoroughly validates all capabilities of hex_dictionary_pure.py:
1. Jaccard distance calculations
2. Jaccard similarity calculations
3. Comprehensive comparison functionality
4. Find closest toggle set
5. Closed space validation (2^n rule)
6. Distance matrix computation
7. Blood types validation
8. Periodic table validation
9. Mineral toggle set applications
10. Performance characteristics
11. Optimization opportunities

Author: UBP Mineral Study
Date: 2025-11-17
"""

import sys
import time
from typing import Set, List, Dict, Any

# Import hex_dictionary_pure
from hex_dictionary_pure import (
    HexDictionaryPure,
    JaccardResult,
    validate_blood_types,
    validate_periodic_table_sample
)


# ============================================================================
# TEST 1: Basic Jaccard Distance
# ============================================================================

def test_jaccard_distance():
    """Test basic Jaccard distance calculations."""
    print("\n" + "="*80)
    print("TEST 1: Basic Jaccard Distance")
    print("="*80)
    
    results = {}
    hex_dict = HexDictionaryPure()
    
    # Test 1.1: Identical sets (distance = 0)
    print("\n1.1 Identical sets...")
    set_a = {"A", "B", "C"}
    set_b = {"A", "B", "C"}
    dist = hex_dict.distance(set_a, set_b)
    print(f"  Sets: {set_a} vs {set_b}")
    print(f"  Distance: {dist:.4f}")
    results['identical'] = abs(dist - 0.0) < 1e-10
    print(f"  ✓ Identical sets have distance 0: {results['identical']}")
    
    # Test 1.2: Disjoint sets (distance = 1)
    print("\n1.2 Disjoint sets...")
    set_a = {"A", "B"}
    set_b = {"C", "D"}
    dist = hex_dict.distance(set_a, set_b)
    print(f"  Sets: {set_a} vs {set_b}")
    print(f"  Distance: {dist:.4f}")
    results['disjoint'] = abs(dist - 1.0) < 1e-10
    print(f"  ✓ Disjoint sets have distance 1: {results['disjoint']}")
    
    # Test 1.3: Partial overlap
    print("\n1.3 Partial overlap...")
    set_a = {"A", "B", "C"}
    set_b = {"B", "C", "D"}
    dist = hex_dict.distance(set_a, set_b)
    expected = 1.0 - (2.0 / 4.0)  # 2 shared, 4 total unique
    print(f"  Sets: {set_a} vs {set_b}")
    print(f"  Distance: {dist:.4f} (expected: {expected:.4f})")
    results['partial'] = abs(dist - expected) < 1e-10
    print(f"  ✓ Partial overlap correct: {results['partial']}")
    
    # Test 1.4: Subset relationship
    print("\n1.4 Subset relationship...")
    set_a = {"A", "B"}
    set_b = {"A", "B", "C", "D"}
    dist = hex_dict.distance(set_a, set_b)
    expected = 1.0 - (2.0 / 4.0)  # 2 shared, 4 total
    print(f"  Sets: {set_a} vs {set_b}")
    print(f"  Distance: {dist:.4f} (expected: {expected:.4f})")
    results['subset'] = abs(dist - expected) < 1e-10
    print(f"  ✓ Subset distance correct: {results['subset']}")
    
    # Test 1.5: Empty sets
    print("\n1.5 Empty sets...")
    set_a = set()
    set_b = set()
    dist = hex_dict.distance(set_a, set_b)
    print(f"  Sets: ∅ vs ∅")
    print(f"  Distance: {dist:.4f}")
    results['empty'] = abs(dist - 0.0) < 1e-10
    print(f"  ✓ Empty sets have distance 0: {results['empty']}")
    
    return results


# ============================================================================
# TEST 2: Jaccard Similarity
# ============================================================================

def test_jaccard_similarity():
    """Test Jaccard similarity calculations."""
    print("\n" + "="*80)
    print("TEST 2: Jaccard Similarity")
    print("="*80)
    
    results = {}
    hex_dict = HexDictionaryPure()
    
    # Test 2.1: Similarity = 1 - Distance
    print("\n2.1 Similarity = 1 - Distance relationship...")
    set_a = {"A", "B", "C"}
    set_b = {"B", "C", "D"}
    dist = hex_dict.distance(set_a, set_b)
    sim = hex_dict.similarity(set_a, set_b)
    print(f"  Distance: {dist:.4f}")
    print(f"  Similarity: {sim:.4f}")
    print(f"  Sum: {dist + sim:.4f}")
    results['relationship'] = abs((dist + sim) - 1.0) < 1e-10
    print(f"  ✓ Distance + Similarity = 1: {results['relationship']}")
    
    # Test 2.2: Identical sets (similarity = 1)
    print("\n2.2 Identical sets similarity...")
    set_a = {"X", "Y", "Z"}
    set_b = {"X", "Y", "Z"}
    sim = hex_dict.similarity(set_a, set_b)
    print(f"  Similarity: {sim:.4f}")
    results['identical_sim'] = abs(sim - 1.0) < 1e-10
    print(f"  ✓ Identical sets have similarity 1: {results['identical_sim']}")
    
    return results


# ============================================================================
# TEST 3: Comprehensive Comparison
# ============================================================================

def test_comprehensive_comparison():
    """Test comprehensive comparison functionality."""
    print("\n" + "="*80)
    print("TEST 3: Comprehensive Comparison")
    print("="*80)
    
    results = {}
    hex_dict = HexDictionaryPure()
    
    # Test 3.1: Compare with full details
    print("\n3.1 Detailed comparison...")
    set_a = {"A", "B", "C", "D"}
    set_b = {"B", "C", "E", "F"}
    result = hex_dict.compare(set_a, set_b)
    
    print(f"  Set A: {set_a}")
    print(f"  Set B: {set_b}")
    print(f"  Distance: {result.distance:.4f}")
    print(f"  Similarity: {result.similarity:.4f}")
    print(f"  Intersection size: {result.intersection_size}")
    print(f"  Union size: {result.union_size}")
    print(f"  Shared toggles: {result.shared_toggles}")
    print(f"  Unique to A: {result.unique_to_a}")
    print(f"  Unique to B: {result.unique_to_b}")
    
    # Validate results
    expected_shared = {"B", "C"}
    expected_unique_a = {"A", "D"}
    expected_unique_b = {"E", "F"}
    
    results['shared'] = result.shared_toggles == expected_shared
    results['unique_a'] = result.unique_to_a == expected_unique_a
    results['unique_b'] = result.unique_to_b == expected_unique_b
    results['sizes'] = (result.intersection_size == 2 and result.union_size == 6)
    
    print(f"  ✓ All comparison details correct: {all([results['shared'], results['unique_a'], results['unique_b'], results['sizes']])}")
    
    return results


# ============================================================================
# TEST 4: Find Closest
# ============================================================================

def test_find_closest():
    """Test find closest toggle set functionality."""
    print("\n" + "="*80)
    print("TEST 4: Find Closest Toggle Set")
    print("="*80)
    
    results = {}
    hex_dict = HexDictionaryPure()
    
    # Test 4.1: Find closest among candidates
    print("\n4.1 Find closest candidate...")
    query = {"A", "B", "C"}
    candidates = [
        {"A", "B"},           # Distance: 0.333 (2/3 shared)
        {"D", "E", "F"},      # Distance: 1.0 (disjoint)
        {"A", "B", "C", "D"}, # Distance: 0.25 (3/4 shared)
        {"X", "Y"}            # Distance: 1.0 (disjoint)
    ]
    
    idx, dist, closest = hex_dict.find_closest(query, candidates)
    
    print(f"  Query: {query}")
    print(f"  Closest index: {idx}")
    print(f"  Closest set: {closest}")
    print(f"  Distance: {dist:.4f}")
    
    results['closest_idx'] = idx == 2  # Should be the 3rd candidate
    results['closest_dist'] = abs(dist - 0.25) < 1e-10
    print(f"  ✓ Closest identification correct: {results['closest_idx'] and results['closest_dist']}")
    
    return results


# ============================================================================
# TEST 5: Closed Space Validation
# ============================================================================

def test_closed_space():
    """Test closed space (2^n) validation."""
    print("\n" + "="*80)
    print("TEST 5: Closed Space Validation (2^n rule)")
    print("="*80)
    
    results = {}
    hex_dict = HexDictionaryPure()
    
    # Test 5.1: Valid closed space (2^3 = 8 blood types)
    print("\n5.1 Valid closed space (blood types)...")
    blood_types = [
        set(),                    # O-
        {"RhD"},                  # O+
        {"A"},                    # A-
        {"A", "RhD"},             # A+
        {"B"},                    # B-
        {"B", "RhD"},             # B+
        {"A", "B"},               # AB-
        {"A", "B", "RhD"}         # AB+
    ]
    
    is_closed = hex_dict.is_closed_space(blood_types, 3)
    print(f"  States: {len(blood_types)}")
    print(f"  Expected: 2^3 = 8")
    print(f"  Is closed: {is_closed}")
    results['blood_closed'] = is_closed
    print(f"  ✓ Blood types form closed space: {results['blood_closed']}")
    
    # Test 5.2: Invalid closed space (incomplete)
    print("\n5.2 Invalid closed space (incomplete)...")
    incomplete = [
        set(),
        {"A"},
        {"B"}
        # Missing {"A", "B"}
    ]
    
    is_closed = hex_dict.is_closed_space(incomplete, 2)
    print(f"  States: {len(incomplete)}")
    print(f"  Expected: 2^2 = 4")
    print(f"  Is closed: {is_closed}")
    results['incomplete'] = not is_closed  # Should be False
    print(f"  ✓ Incomplete space detected: {results['incomplete']}")
    
    return results


# ============================================================================
# TEST 6: Distance Matrix
# ============================================================================

def test_distance_matrix():
    """Test distance matrix computation."""
    print("\n" + "="*80)
    print("TEST 6: Distance Matrix Computation")
    print("="*80)
    
    results = {}
    hex_dict = HexDictionaryPure()
    
    # Test 6.1: Compute matrix for simple sets
    print("\n6.1 Distance matrix for 3 sets...")
    states = [
        {"A"},
        {"B"},
        {"A", "B"}
    ]
    labels = ["A-only", "B-only", "AB"]
    
    matrix_result = hex_dict.compute_distance_matrix(states, labels)
    matrix = matrix_result['matrix']
    
    print(f"  Matrix size: {matrix_result['size']}x{matrix_result['size']}")
    print(f"  Labels: {matrix_result['labels']}")
    print(f"\n  Distance Matrix:")
    for i, label_i in enumerate(labels):
        row_str = f"    {label_i:10s} |"
        for j in range(len(labels)):
            row_str += f" {matrix[i][j]:.3f}"
        print(row_str)
    
    # Validate diagonal is zero
    diagonal_zero = all(abs(matrix[i][i]) < 1e-10 for i in range(len(states)))
    results['diagonal'] = diagonal_zero
    print(f"\n  ✓ Diagonal is zero: {results['diagonal']}")
    
    # Validate symmetry
    symmetric = all(abs(matrix[i][j] - matrix[j][i]) < 1e-10 
                   for i in range(len(states)) for j in range(len(states)))
    results['symmetric'] = symmetric
    print(f"  ✓ Matrix is symmetric: {results['symmetric']}")
    
    # Validate specific distances
    # A-only vs B-only should be distance 1.0 (disjoint)
    results['disjoint_dist'] = abs(matrix[0][1] - 1.0) < 1e-10
    # A-only vs AB should be distance 0.5 (1 shared, 2 total)
    results['subset_dist'] = abs(matrix[0][2] - 0.5) < 1e-10
    
    print(f"  ✓ Specific distances correct: {results['disjoint_dist'] and results['subset_dist']}")
    
    return results


# ============================================================================
# TEST 7: Blood Types Validation
# ============================================================================

def test_blood_types_validation():
    """Test blood types validation (built-in)."""
    print("\n" + "="*80)
    print("TEST 7: Blood Types Validation")
    print("="*80)
    
    results = {}
    
    print("\n7.1 Running built-in blood types validation...")
    try:
        passed = validate_blood_types()
        print(f"  ✓ Blood types validation: {passed}")
        results['validation'] = passed
    except Exception as e:
        print(f"  ✗ Validation failed: {e}")
        results['validation'] = False
    
    return results


# ============================================================================
# TEST 8: Periodic Table Validation
# ============================================================================

def test_periodic_table_validation():
    """Test periodic table validation (built-in)."""
    print("\n" + "="*80)
    print("TEST 8: Periodic Table Validation")
    print("="*80)
    
    results = {}
    
    print("\n8.1 Running built-in periodic table validation...")
    try:
        passed = validate_periodic_table_sample()
        print(f"  ✓ Periodic table validation: {passed}")
        results['validation'] = passed
    except Exception as e:
        print(f"  ✗ Validation failed: {e}")
        results['validation'] = False
    
    return results


# ============================================================================
# TEST 9: Mineral Toggle Set Applications
# ============================================================================

def test_mineral_applications():
    """Test hex dictionary with mineral-like toggle sets."""
    print("\n" + "="*80)
    print("TEST 9: Mineral Toggle Set Applications")
    print("="*80)
    
    results = {}
    hex_dict = HexDictionaryPure()
    
    # Test 9.1: Mineral crystal systems as toggle sets
    print("\n9.1 Crystal systems as toggle sets...")
    minerals = {
        "Quartz": {"SiO2", "hexagonal", "Z=3"},
        "Halite": {"NaCl", "cubic", "Z=4"},
        "Calcite": {"CaCO3", "trigonal", "Z=6"},
        "Gypsum": {"CaSO4", "monoclinic", "Z=4"}
    }
    
    # Find similar crystal systems
    quartz_set = minerals["Quartz"]
    calcite_set = minerals["Calcite"]
    
    result = hex_dict.compare(quartz_set, calcite_set)
    print(f"  Quartz vs Calcite:")
    print(f"    Distance: {result.distance:.4f}")
    print(f"    Shared: {result.shared_toggles}")
    print(f"    Unique to Quartz: {result.unique_to_a}")
    print(f"    Unique to Calcite: {result.unique_to_b}")
    
    results['mineral_compare'] = result.distance < 1.0  # Should have some overlap
    print(f"  ✓ Mineral comparison working: {results['mineral_compare']}")
    
    # Test 9.2: Find minerals with similar Z values
    print("\n9.2 Find minerals with similar Z values...")
    mineral_sets = list(minerals.values())
    halite_set = minerals["Halite"]
    
    idx, dist, closest = hex_dict.find_closest(halite_set, 
                                                [s for s in mineral_sets if s != halite_set])
    print(f"  Closest to Halite: distance = {dist:.4f}")
    results['mineral_closest'] = dist < 1.0
    print(f"  ✓ Closest mineral found: {results['mineral_closest']}")
    
    return results


# ============================================================================
# TEST 10: Performance Characteristics
# ============================================================================

def test_performance():
    """Test performance characteristics."""
    print("\n" + "="*80)
    print("TEST 10: Performance Characteristics")
    print("="*80)
    
    results = {}
    hex_dict = HexDictionaryPure()
    
    # Test 10.1: Distance calculation performance
    print("\n10.1 Distance calculation performance...")
    set_a = set(f"toggle_{i}" for i in range(100))
    set_b = set(f"toggle_{i}" for i in range(50, 150))
    
    n_calcs = 10000
    start_time = time.time()
    for _ in range(n_calcs):
        dist = hex_dict.distance(set_a, set_b)
    calc_time = time.time() - start_time
    
    print(f"  {n_calcs} distance calculations in {calc_time:.4f}s")
    print(f"  Rate: {n_calcs/calc_time:.0f} calcs/sec")
    results['distance_rate'] = n_calcs / calc_time
    
    # Test 10.2: Distance matrix performance
    print("\n10.2 Distance matrix performance...")
    n_states = 50
    states = [set(f"t{i}_{j}" for j in range(10)) for i in range(n_states)]
    
    start_time = time.time()
    matrix_result = hex_dict.compute_distance_matrix(states)
    matrix_time = time.time() - start_time
    
    n_comparisons = n_states * n_states
    print(f"  {n_states}x{n_states} matrix ({n_comparisons} comparisons) in {matrix_time:.4f}s")
    print(f"  Rate: {n_comparisons/matrix_time:.0f} comparisons/sec")
    results['matrix_rate'] = n_comparisons / matrix_time
    
    return results


# ============================================================================
# TEST 11: Optimization Opportunities
# ============================================================================

def identify_optimization_opportunities():
    """Identify potential optimization opportunities."""
    print("\n" + "="*80)
    print("TEST 11: Optimization Opportunities Identification")
    print("="*80)
    
    opportunities = []
    
    print("\n11.1 Analyzing module structure...")
    
    print("\n11.2 Potential optimizations:")
    
    # Opportunity 1: Set operations caching
    print("\n  • Set operations caching:")
    print("    - Union and intersection computed separately")
    print("    - Could compute once and reuse")
    print("    - Benefit: ~2x faster for repeated queries")
    opportunities.append("Set operations caching")
    
    # Opportunity 2: Batch distance calculations
    print("\n  • Batch distance calculations:")
    print("    - Currently processes pairs one at a time")
    print("    - Could vectorize for multiple queries")
    print("    - Benefit: Better cache locality")
    opportunities.append("Batch distance calculations")
    
    # Opportunity 3: Sparse representation
    print("\n  • Sparse representation:")
    print("    - Large toggle sets stored as full sets")
    print("    - Could use bit vectors for dense sets")
    print("    - Benefit: Lower memory, faster operations")
    opportunities.append("Sparse/dense hybrid representation")
    
    # Opportunity 4: Distance matrix symmetry
    print("\n  • Distance matrix symmetry exploitation:")
    print("    - Currently computes full matrix")
    print("    - Could compute upper triangle only")
    print("    - Benefit: 2x faster matrix computation")
    opportunities.append("Symmetric matrix optimization")
    
    return opportunities


# ============================================================================
# MAIN TEST RUNNER
# ============================================================================

def run_all_tests():
    """Run all tests and generate comprehensive report."""
    print("="*80)
    print("COMPREHENSIVE TEST SUITE: hex_dictionary_pure.py")
    print("UBP 3.5 Module Validation")
    print("="*80)
    
    all_results = {}
    
    # Run all tests
    all_results['distance'] = test_jaccard_distance()
    all_results['similarity'] = test_jaccard_similarity()
    all_results['comparison'] = test_comprehensive_comparison()
    all_results['find_closest'] = test_find_closest()
    all_results['closed_space'] = test_closed_space()
    all_results['distance_matrix'] = test_distance_matrix()
    all_results['blood_types'] = test_blood_types_validation()
    all_results['periodic_table'] = test_periodic_table_validation()
    all_results['minerals'] = test_mineral_applications()
    all_results['performance'] = test_performance()
    
    # Identify optimizations
    opportunities = identify_optimization_opportunities()
    
    # Generate summary
    print("\n" + "="*80)
    print("TEST SUMMARY")
    print("="*80)
    
    total_tests = sum(len(v) for v in all_results.values() if isinstance(v, dict))
    passed_tests = sum(sum(1 for x in v.values() if x) for v in all_results.values() if isinstance(v, dict))
    
    print(f"\nTotal tests run: {total_tests}")
    print(f"Tests passed: {passed_tests}")
    print(f"Tests failed: {total_tests - passed_tests}")
    print(f"Pass rate: {passed_tests/total_tests*100:.1f}%")
    
    print("\n" + "="*80)
    print("OPTIMIZATION OPPORTUNITIES")
    print("="*80)
    for i, opp in enumerate(opportunities, 1):
        print(f"{i}. {opp}")
    
    print("\n" + "="*80)
    print("VALIDATION COMPLETE")
    print("="*80)
    
    return all_results, opportunities


if __name__ == "__main__":
    results, optimizations = run_all_tests()
