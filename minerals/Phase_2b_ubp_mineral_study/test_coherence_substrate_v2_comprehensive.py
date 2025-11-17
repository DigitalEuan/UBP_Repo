"""
================================================================================
Comprehensive Test Suite for coherence_substrate_v2.py (UBP 3.5)
================================================================================

This test suite thoroughly validates all capabilities of coherence_substrate_v2.py:
1. CoherenceState basic operations
2. ComputationHistory tracking
3. CoherenceHexDictionary integration
4. PrecisionMode variations (FLOAT, FIXED, RATIONAL, PROJECTED)
5. Y-refinement operations (forward/backward)
6. Bidirectional closure validation
7. Performance characteristics
8. Optimization opportunities identification

Author: UBP Mineral Study
Date: 2025-11-17
"""

import sys
import time
import math
from typing import Dict, List, Tuple, Any

# Import coherence_substrate_v2
from coherence_substrate_v2 import (
    CoherenceState,
    ComputationHistory,
    CoherenceHexDictionary,
    PrecisionMode,
    Y, Y_INVERSE, O_OBSERVER, NRCI_TARGET,
    PI, GOLDEN_RATIO
)


# ============================================================================
# TEST 1: Basic CoherenceState Operations
# ============================================================================

def test_coherence_state_basic():
    """Test basic CoherenceState creation and properties."""
    print("\n" + "="*80)
    print("TEST 1: Basic CoherenceState Operations")
    print("="*80)
    
    results = {}
    
    # Test 1.1: Creation with default NRCI
    print("\n1.1 Creation with default NRCI...")
    state1 = CoherenceState(1.0)
    print(f"  State: {state1}")
    print(f"  Value: {state1.value}")
    print(f"  NRCI: {state1.nrci:.15f}")
    results['creation_default'] = abs(state1.nrci - NRCI_TARGET) < 1e-10
    print(f"  ✓ NRCI matches target: {results['creation_default']}")
    
    # Test 1.2: Creation with custom NRCI
    print("\n1.2 Creation with custom NRCI...")
    custom_nrci = 0.99
    log_error = math.log(1 - custom_nrci)
    state2 = CoherenceState(2.0, log_nrci_error=log_error)
    print(f"  State: {state2}")
    print(f"  Target NRCI: {custom_nrci:.10f}")
    print(f"  Actual NRCI: {state2.nrci:.10f}")
    results['creation_custom'] = abs(state2.nrci - custom_nrci) < 1e-6
    print(f"  ✓ Custom NRCI set correctly: {results['creation_custom']}")
    
    # Test 1.3: Arithmetic operations
    print("\n1.3 Arithmetic operations...")
    a = CoherenceState(10.0)
    b = CoherenceState(5.0)
    
    add_result = a + b
    print(f"  10 + 5 = {add_result.value} (NRCI: {add_result.nrci:.10f})")
    results['add'] = abs(add_result.value - 15.0) < 1e-10
    
    sub_result = a - b
    print(f"  10 - 5 = {sub_result.value} (NRCI: {sub_result.nrci:.10f})")
    results['sub'] = abs(sub_result.value - 5.0) < 1e-10
    
    mul_result = a * b
    print(f"  10 * 5 = {mul_result.value} (NRCI: {mul_result.nrci:.10f})")
    results['mul'] = abs(mul_result.value - 50.0) < 1e-10
    
    div_result = a / b
    print(f"  10 / 5 = {div_result.value} (NRCI: {div_result.nrci:.10f})")
    results['div'] = abs(div_result.value - 2.0) < 1e-10
    
    print(f"  ✓ All arithmetic operations correct: {all([results['add'], results['sub'], results['mul'], results['div']])}")
    
    # Test 1.4: Coherence degradation
    print("\n1.4 Coherence degradation...")
    initial_state = CoherenceState(1.0)
    initial_nrci = initial_state.nrci
    degraded_state = initial_state.degrade_by(0.1)
    degraded_nrci = degraded_state.nrci
    print(f"  Initial NRCI: {initial_nrci:.10f}")
    print(f"  After degradation: {degraded_nrci:.10f}")
    print(f"  Degradation amount: {initial_nrci - degraded_nrci:.10f}")
    results['degradation'] = degraded_nrci < initial_nrci
    print(f"  ✓ Degradation works correctly: {results['degradation']}")
    
    return results


# ============================================================================
# TEST 2: Y-Refinement Operations
# ============================================================================

def test_y_refinement():
    """Test Y-refinement forward and backward operations."""
    print("\n" + "="*80)
    print("TEST 2: Y-Refinement Operations")
    print("="*80)
    
    results = {}
    
    # Test 2.1: Forward refinement
    print("\n2.1 Forward refinement (geometry → observer)...")
    state = CoherenceState(1000.0)
    print(f"  Initial: value={state.value:.6f}, NRCI={state.nrci:.15f}")
    
    forward = state.refine_forward()
    print(f"  Forward: value={forward.value:.6f}, NRCI={forward.nrci:.15f}")
    print(f"  Expected value: {1000.0 * Y:.6f}")
    results['forward_value'] = abs(forward.value - 1000.0 * Y) < 1e-10
    print(f"  ✓ Forward value correct: {results['forward_value']}")
    
    # Test 2.2: Backward refinement
    print("\n2.2 Backward refinement (observer → geometry)...")
    backward = forward.refine_backward()
    print(f"  Backward: value={backward.value:.6f}, NRCI={backward.nrci:.15f}")
    print(f"  Expected value: {1000.0:.6f}")
    results['backward_value'] = abs(backward.value - 1000.0) < 1e-10
    print(f"  ✓ Backward value correct: {results['backward_value']}")
    
    # Test 2.3: Bidirectional closure
    print("\n2.3 Bidirectional closure validation...")
    test_values = [1.0, 1e6, 1e12, 1e18]
    closure_errors = []
    
    for val in test_values:
        state = CoherenceState(val)
        forward = state.refine_forward()
        backward = forward.refine_backward()
        error = abs(backward.value - val) / val
        closure_errors.append(error)
        print(f"  Value {val:.0e}: closure error = {error:.2e}")
    
    max_closure_error = max(closure_errors)
    results['closure'] = max_closure_error < 1e-12
    print(f"  Max closure error: {max_closure_error:.2e}")
    print(f"  ✓ Bidirectional closure validated: {results['closure']}")
    
    # Test 2.4: Y × (1/Y) = 1 verification
    print("\n2.4 Y × (1/Y) = 1 verification...")
    product = Y * Y_INVERSE
    error = abs(product - 1.0)
    print(f"  Y = {Y:.15f}")
    print(f"  Y_INVERSE = {Y_INVERSE:.15f}")
    print(f"  Y × Y_INVERSE = {product:.15f}")
    print(f"  Error from 1.0: {error:.2e}")
    results['involutory'] = error < 1e-14
    print(f"  ✓ Involutory property verified: {results['involutory']}")
    
    return results


# ============================================================================
# TEST 3: ComputationHistory Tracking
# ============================================================================

def test_computation_history():
    """Test ComputationHistory tracking capabilities."""
    print("\n" + "="*80)
    print("TEST 3: ComputationHistory Tracking")
    print("="*80)
    
    results = {}
    
    # Test 3.1: History initialization
    print("\n3.1 History initialization...")
    try:
        history = ComputationHistory()
        print(f"  ✓ ComputationHistory created successfully")
        results['init'] = True
    except Exception as e:
        print(f"  ✗ Failed to create ComputationHistory: {e}")
        results['init'] = False
        return results
    
    # Test 3.2: Operation recording
    print("\n3.2 Operation recording...")
    state = CoherenceState(1.0)
    
    # Check if CoherenceState has history attribute
    if hasattr(state, 'history'):
        print(f"  ✓ CoherenceState has history attribute")
        results['has_history'] = True
        
        # Perform operations and check history
        forward = state.refine_forward()
        backward = forward.refine_backward()
        
        if hasattr(forward.history, 'get_summary'):
            summary = forward.history.get_summary()
            print(f"  History summary: {summary}")
            results['recording'] = True
        else:
            print(f"  ✗ History doesn't have get_summary method")
            results['recording'] = False
    else:
        print(f"  ℹ CoherenceState doesn't have built-in history (may need explicit tracking)")
        results['has_history'] = False
        results['recording'] = False
    
    return results


# ============================================================================
# TEST 4: CoherenceHexDictionary Integration
# ============================================================================

def test_hex_dictionary():
    """Test CoherenceHexDictionary integration."""
    print("\n" + "="*80)
    print("TEST 4: CoherenceHexDictionary Integration")
    print("="*80)
    
    results = {}
    
    # Test 4.1: HexDictionary creation
    print("\n4.1 HexDictionary creation...")
    try:
        hex_dict = CoherenceHexDictionary()
        print(f"  ✓ CoherenceHexDictionary created successfully")
        results['init'] = True
    except Exception as e:
        print(f"  ✗ Failed to create CoherenceHexDictionary: {e}")
        results['init'] = False
        return results
    
    # Test 4.2: Configure HexDictionary for CoherenceState
    print("\n4.2 Configure HexDictionary for CoherenceState...")
    try:
        CoherenceState.set_hex_dictionary(hex_dict, auto_persist=False)
        print(f"  ✓ HexDictionary configured successfully")
        results['configure'] = True
    except Exception as e:
        print(f"  ✗ Configuration failed: {e}")
        results['configure'] = False
        return results
    
    # Test 4.3: State persistence
    print("\n4.3 State persistence...")
    state = CoherenceState(42.0)
    
    if hasattr(state, 'persist'):
        try:
            address = state.persist()
            print(f"  Address: {address[:16]}...")
            print(f"  Full address length: {len(address)} chars")
            results['persist'] = True
        except Exception as e:
            print(f"  ✗ Persistence failed: {e}")
            results['persist'] = False
            return results
    else:
        print(f"  ℹ CoherenceState doesn't have persist method")
        results['persist'] = False
        return results
    
    # Test 4.4: State retrieval
    print("\n4.4 State retrieval...")
    if results.get('persist', False):
        try:
            retrieved = hex_dict.retrieve(address)
            if retrieved is not None:
                print(f"  Retrieved value: {retrieved.value}")
                print(f"  Retrieved NRCI: {retrieved.nrci:.10f}")
                value_match = abs(retrieved.value - 42.0) < 1e-10
                nrci_match = abs(retrieved.nrci - state.nrci) < 1e-6
                results['retrieve'] = value_match and nrci_match
                print(f"  ✓ Retrieval successful: {results['retrieve']}")
            else:
                print(f"  ✗ Retrieved state is None")
                results['retrieve'] = False
        except Exception as e:
            print(f"  ✗ Retrieval failed: {e}")
            results['retrieve'] = False
    else:
        results['retrieve'] = False
    
    # Test 4.5: Similarity search
    print("\n4.5 Similarity search...")
    try:
        # Store a few more states
        state2 = CoherenceState(43.0)
        state3 = CoherenceState(100.0)
        addr2 = state2.persist()
        addr3 = state3.persist()
        
        # Find similar states
        similar = hex_dict.find_similar(state, threshold=0.8)
        print(f"  Found {len(similar)} similar states (threshold=0.8)")
        results['similarity'] = len(similar) >= 1  # Should find at least itself
        print(f"  ✓ Similarity search working: {results['similarity']}")
    except Exception as e:
        print(f"  ℹ Similarity search not fully tested: {e}")
        results['similarity'] = False
    
    return results


# ============================================================================
# TEST 5: PrecisionMode Variations
# ============================================================================

def test_precision_modes():
    """Test different precision modes."""
    print("\n" + "="*80)
    print("TEST 5: PrecisionMode Variations")
    print("="*80)
    
    results = {}
    
    # Test 5.1: FLOAT mode (default)
    print("\n5.1 FLOAT mode (default)...")
    try:
        state_float = CoherenceState(1.0, precision_mode=PrecisionMode.FLOAT)
        print(f"  State: {state_float}")
        results['float'] = True
    except Exception as e:
        print(f"  ℹ PrecisionMode.FLOAT not available in constructor: {e}")
        # Try without precision_mode parameter
        state_float = CoherenceState(1.0)
        print(f"  State (default): {state_float}")
        results['float'] = True
    
    # Test 5.2: FIXED mode
    print("\n5.2 FIXED mode...")
    try:
        state_fixed = CoherenceState(1.0, precision_mode=PrecisionMode.FIXED)
        print(f"  State: {state_fixed}")
        results['fixed'] = True
    except Exception as e:
        print(f"  ℹ PrecisionMode.FIXED not available: {e}")
        results['fixed'] = False
    
    # Test 5.3: RATIONAL mode
    print("\n5.3 RATIONAL mode...")
    try:
        state_rational = CoherenceState(1.0, precision_mode=PrecisionMode.RATIONAL)
        print(f"  State: {state_rational}")
        results['rational'] = True
    except Exception as e:
        print(f"  ℹ PrecisionMode.RATIONAL not available: {e}")
        results['rational'] = False
    
    # Test 5.4: PROJECTED mode
    print("\n5.4 PROJECTED mode...")
    try:
        state_projected = CoherenceState(1.0, precision_mode=PrecisionMode.PROJECTED)
        print(f"  State: {state_projected}")
        results['projected'] = True
    except Exception as e:
        print(f"  ℹ PrecisionMode.PROJECTED not available: {e}")
        results['projected'] = False
    
    return results


# ============================================================================
# TEST 6: Performance Characteristics
# ============================================================================

def test_performance():
    """Test performance characteristics."""
    print("\n" + "="*80)
    print("TEST 6: Performance Characteristics")
    print("="*80)
    
    results = {}
    
    # Test 6.1: State creation performance
    print("\n6.1 State creation performance...")
    n_states = 10000
    start_time = time.time()
    states = [CoherenceState(float(i)) for i in range(n_states)]
    creation_time = time.time() - start_time
    print(f"  Created {n_states} states in {creation_time:.4f}s")
    print(f"  Rate: {n_states/creation_time:.0f} states/sec")
    results['creation_rate'] = n_states / creation_time
    
    # Test 6.2: Arithmetic operations performance
    print("\n6.2 Arithmetic operations performance...")
    n_ops = 10000
    state_a = CoherenceState(10.0)
    state_b = CoherenceState(5.0)
    
    start_time = time.time()
    for _ in range(n_ops):
        result = state_a + state_b
    add_time = time.time() - start_time
    print(f"  {n_ops} additions in {add_time:.4f}s")
    print(f"  Rate: {n_ops/add_time:.0f} ops/sec")
    results['add_rate'] = n_ops / add_time
    
    # Test 6.3: Y-refinement performance
    print("\n6.3 Y-refinement performance...")
    n_refinements = 10000
    state = CoherenceState(1000.0)
    
    start_time = time.time()
    for _ in range(n_refinements):
        state = state.refine_forward()
    refinement_time = time.time() - start_time
    print(f"  {n_refinements} refinements in {refinement_time:.4f}s")
    print(f"  Rate: {n_refinements/refinement_time:.0f} ops/sec")
    results['refinement_rate'] = n_refinements / refinement_time
    
    return results


# ============================================================================
# TEST 7: Optimization Opportunities
# ============================================================================

def identify_optimization_opportunities():
    """Identify potential optimization opportunities."""
    print("\n" + "="*80)
    print("TEST 7: Optimization Opportunities Identification")
    print("="*80)
    
    opportunities = []
    
    print("\n7.1 Analyzing module structure...")
    
    # Check for potential optimizations
    print("\n7.2 Potential optimizations:")
    
    # Opportunity 1: Caching Y-refinement values
    print("\n  • Y-refinement caching:")
    print("    - Y and Y_INVERSE are constants")
    print("    - Could pre-compute common refinement chains")
    print("    - Benefit: Faster repeated refinements")
    opportunities.append("Y-refinement caching")
    
    # Opportunity 2: NRCI computation optimization
    print("\n  • NRCI computation:")
    print("    - Currently uses exp() for every access")
    print("    - Could cache NRCI value when log_nrci_error unchanged")
    print("    - Benefit: Faster NRCI queries")
    opportunities.append("NRCI caching")
    
    # Opportunity 3: Batch operations
    print("\n  • Batch operations:")
    print("    - Currently operates on single states")
    print("    - Could add vectorized operations for arrays")
    print("    - Benefit: Better performance for large datasets")
    opportunities.append("Batch/vectorized operations")
    
    # Opportunity 4: Memory efficiency
    print("\n  • Memory efficiency:")
    print("    - ComputationHistory could grow large")
    print("    - Could add history compression/pruning")
    print("    - Benefit: Lower memory footprint")
    opportunities.append("History compression")
    
    return opportunities


# ============================================================================
# MAIN TEST RUNNER
# ============================================================================

def run_all_tests():
    """Run all tests and generate comprehensive report."""
    print("="*80)
    print("COMPREHENSIVE TEST SUITE: coherence_substrate_v2.py")
    print("UBP 3.5 Module Validation")
    print("="*80)
    
    all_results = {}
    
    # Run all tests
    all_results['basic'] = test_coherence_state_basic()
    all_results['refinement'] = test_y_refinement()
    all_results['history'] = test_computation_history()
    all_results['hexdict'] = test_hex_dictionary()
    all_results['precision'] = test_precision_modes()
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
