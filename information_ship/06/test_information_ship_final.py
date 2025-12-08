#!/usr/bin/env python3
"""
Comprehensive Validation Test Suite for Information Ship Final

This test suite validates all aspects of the Information Ship:
- Mathematical correctness
- First-principles integrity
- Edge cases and error handling
- Performance characteristics
- Scientific honesty
"""

import sys
import math
from fractions import Fraction

# Import the Information Ship
from information_ship_final import (
    CoherenceState,
    LeechLatticeGeometry,
    UntwistedSectorMassPredictor,
    accumulate_log_nrci,
    run_honesty_audit,
    Y, Y_INVERSE, PI
)

def test_y_constants_mathematical_properties():
    """Test mathematical properties of Y-constants."""
    print("Testing Y-constant mathematical properties...")
    
    # Y = π/(π² + 2)
    expected_y = PI / (PI * PI + 2)
    assert abs(float(Y - expected_y)) < 1e-10, "Y formula incorrect"
    
    # Y⁻¹ = π + 2/π
    expected_y_inv = PI + 2 / PI
    assert abs(float(Y_INVERSE - expected_y_inv)) < 1e-10, "Y_INVERSE formula incorrect"
    
    # Y * Y⁻¹ should be close to (π² + 2)/π * (π + 2/π) = π + 2/π + 2 + 2/π² 
    # Actually, let's verify the relationship differently
    # From Y = π/(π² + 2), we get Y(π² + 2) = π
    product = float(Y) * (float(PI)**2 + 2)
    assert abs(product - float(PI)) < 1e-6, f"Y relationship broken: {product} ≠ π"
    
    print("  ✓ Y-constant mathematical properties verified")
    return True

def test_coherence_state_exact_arithmetic():
    """Test that CoherenceState maintains exact arithmetic."""
    print("Testing CoherenceState exact arithmetic...")
    
    # Create state with exact fraction
    state = CoherenceState(value=Fraction(1, 3))
    assert isinstance(state.value, Fraction), "Value not a Fraction"
    assert state.value == Fraction(1, 3), "Value corrupted"
    
    # Refinement should maintain Fraction type
    refined = state.refine(Fraction(2, 3), steps=1)
    assert isinstance(refined.value, Fraction), "Refined value not a Fraction"
    
    print("  ✓ Exact arithmetic maintained")
    return True

def test_nrci_monotonic_degradation():
    """Test that NRCI degrades monotonically with operations."""
    print("Testing NRCI monotonic degradation...")
    
    state = CoherenceState(value=Fraction(1, 2))
    initial_nrci = state.nrci()
    
    # Perform refinements
    for i in range(10):
        state = state.refine(Fraction(3, 4), steps=1)
        new_nrci = state.nrci()
        assert new_nrci <= initial_nrci, f"NRCI increased at step {i}: {new_nrci} > {initial_nrci}"
        initial_nrci = new_nrci
    
    print("  ✓ NRCI degrades monotonically")
    return True

def test_leech_shell_densities_correct():
    """Test that Leech lattice shell densities are correct."""
    print("Testing Leech lattice shell densities...")
    
    leech = LeechLatticeGeometry()
    
    # Known exact values
    assert leech.get_shell_density(0) == 1, "Origin density wrong"
    assert leech.get_shell_density(4) == 196560, "Shell 4 density wrong"
    assert leech.get_shell_density(6) == 16773120, "Shell 6 density wrong"
    assert leech.get_shell_density(8) == 398034000, "Shell 8 density wrong"
    
    # Non-existent shell
    assert leech.get_shell_density(2) == 0, "Non-existent shell should return 0"
    
    print("  ✓ Leech shell densities correct")
    return True

def test_mass_prediction_formula_consistency():
    """Test that mass prediction formula is internally consistent."""
    print("Testing mass prediction formula consistency...")
    
    leech = LeechLatticeGeometry()
    predictor = UntwistedSectorMassPredictor(leech)
    
    # Reference (electron) should give ratio 1.0
    ratio_e = predictor.predict_mass_ratio(4)
    assert abs(ratio_e - 1.0) < 1e-10, f"Electron ratio should be 1.0, got {ratio_e}"
    
    # Muon ratio should be Y_INVERSE^((6-4)/2) = Y_INVERSE^1
    ratio_mu = predictor.predict_mass_ratio(6)
    expected_mu = float(Y_INVERSE)
    assert abs(ratio_mu - expected_mu) < 1e-6, f"Muon ratio inconsistent: {ratio_mu} ≠ {expected_mu}"
    
    # Tau ratio should be Y_INVERSE^((8-4)/2) = Y_INVERSE^2
    ratio_tau = predictor.predict_mass_ratio(8)
    expected_tau = float(Y_INVERSE) ** 2
    assert abs(ratio_tau - expected_tau) < 1e-6, f"Tau ratio inconsistent: {ratio_tau} ≠ {expected_tau}"
    
    print("  ✓ Mass prediction formula consistent")
    return True

def test_geometric_delta_derivation():
    """Test geometric δ derivation from shell densities."""
    print("Testing geometric δ derivation...")
    
    leech = LeechLatticeGeometry()
    delta = leech.derive_delta_geometric()
    
    # δ should be positive and reasonable
    assert delta > 0, f"δ should be positive, got {delta}"
    assert 0.1 < delta < 0.5, f"δ out of reasonable range: {delta}"
    
    # Verify it's derived from shell densities
    ratio_8_6 = leech.get_shell_density_ratio(6, 8)
    expected_delta = abs(math.log(ratio_8_6) / math.log(float(Y_INVERSE)) - 2.0)
    assert abs(delta - expected_delta) < 1e-10, "δ derivation formula incorrect"
    
    print("  ✓ Geometric δ derivation correct")
    return True

def test_nrci_accumulation_helper():
    """Test NRCI accumulation helper function."""
    print("Testing NRCI accumulation helper...")
    
    # Single operation
    log_error_1 = accumulate_log_nrci(['addition'])
    assert log_error_1 > 0, "Log error should be positive"
    
    # Multiple operations should accumulate
    log_error_2 = accumulate_log_nrci(['addition', 'multiplication'])
    assert log_error_2 > log_error_1, "Errors should accumulate"
    
    # More expensive operations should contribute more
    log_error_exp = accumulate_log_nrci(['exponentiation'])
    log_error_add = accumulate_log_nrci(['addition'])
    assert log_error_exp > log_error_add, "Exponentiation should have larger error than addition"
    
    print("  ✓ NRCI accumulation helper correct")
    return True

def test_honesty_audit_completeness():
    """Test that honesty audit covers all components."""
    print("Testing honesty audit completeness...")
    
    audit = run_honesty_audit()
    
    # Check required fields
    assert 'timestamp' in audit, "Missing timestamp"
    assert 'version' in audit, "Missing version"
    assert 'components' in audit, "Missing components"
    assert 'overall' in audit, "Missing overall assessment"
    
    # Check critical components are audited
    required_components = [
        'exact_arithmetic',
        'y_constants',
        'leech_lattice',
        'golay_g24',
        'mass_prediction',
        'delta_parameter'
    ]
    
    for component in required_components:
        assert component in audit['components'], f"Missing component: {component}"
        assert 'status' in audit['components'][component], f"Missing status for {component}"
        assert 'limitations' in audit['components'][component], f"Missing limitations for {component}"
    
    # Check that mass_prediction is flagged as incomplete
    mass_pred_status = audit['components']['mass_prediction']['status']
    assert 'INCOMPLETE' in mass_pred_status, "Mass prediction should be flagged as incomplete"
    
    # Check overall assessment
    assert audit['overall']['first_principles_core'] == 'YES', "Should confirm first-principles core"
    assert 'MAINTAINED' in audit['overall']['scientific_integrity'], "Should confirm scientific integrity"
    
    print("  ✓ Honesty audit complete and accurate")
    return True

def test_edge_cases():
    """Test edge cases and error handling."""
    print("Testing edge cases...")
    
    # CoherenceState with zero
    try:
        state_zero = CoherenceState(value=Fraction(0, 1))
        assert state_zero.nrci() == 1.0, "Zero state should have NRCI = 1.0"
    except Exception as e:
        print(f"  ✗ Zero state failed: {e}")
        return False
    
    # CoherenceState with large denominator
    try:
        state_large = CoherenceState(value=Fraction(1, 10**15))
        assert state_large.nrci() == 1.0, "Large denominator state should have NRCI = 1.0"
    except Exception as e:
        print(f"  ✗ Large denominator failed: {e}")
        return False
    
    # Refinement with steps = 0
    try:
        state = CoherenceState(value=Fraction(1, 2))
        refined = state.refine(Fraction(3, 4), steps=0)
        assert refined.value == state.value, "Zero steps should not change value"
    except Exception as e:
        print(f"  ✗ Zero steps refinement failed: {e}")
        return False
    
    print("  ✓ Edge cases handled correctly")
    return True

def test_performance_characteristics():
    """Test performance characteristics."""
    print("Testing performance characteristics...")
    
    import time
    
    # Test coherence state creation performance
    start = time.time()
    for i in range(1000):
        state = CoherenceState(value=Fraction(i, 1000))
    elapsed = time.time() - start
    assert elapsed < 1.0, f"Coherence state creation too slow: {elapsed:.3f}s for 1000 states"
    
    # Test mass prediction performance
    leech = LeechLatticeGeometry()
    predictor = UntwistedSectorMassPredictor(leech)
    
    start = time.time()
    for i in range(1000):
        predictor.predict_mass_ratio(6)
    elapsed = time.time() - start
    assert elapsed < 0.1, f"Mass prediction too slow: {elapsed:.3f}s for 1000 predictions"
    
    print("  ✓ Performance characteristics acceptable")
    return True

def run_all_validation_tests():
    """Run all validation tests."""
    print("=" * 80)
    print("COMPREHENSIVE VALIDATION TEST SUITE")
    print("=" * 80)
    print()
    
    tests = [
        ("Y-constant mathematical properties", test_y_constants_mathematical_properties),
        ("CoherenceState exact arithmetic", test_coherence_state_exact_arithmetic),
        ("NRCI monotonic degradation", test_nrci_monotonic_degradation),
        ("Leech shell densities", test_leech_shell_densities_correct),
        ("Mass prediction formula consistency", test_mass_prediction_formula_consistency),
        ("Geometric δ derivation", test_geometric_delta_derivation),
        ("NRCI accumulation helper", test_nrci_accumulation_helper),
        ("Honesty audit completeness", test_honesty_audit_completeness),
        ("Edge cases", test_edge_cases),
        ("Performance characteristics", test_performance_characteristics),
    ]
    
    passed = 0
    failed = 0
    
    for name, test_func in tests:
        try:
            if test_func():
                passed += 1
            else:
                failed += 1
                print(f"  ✗ {name} FAILED")
        except Exception as e:
            failed += 1
            print(f"  ✗ {name} FAILED with exception: {e}")
    
    print()
    print("=" * 80)
    print(f"VALIDATION RESULTS: {passed}/{len(tests)} tests passed")
    print("=" * 80)
    
    if failed == 0:
        print("✅ ALL VALIDATION TESTS PASSED")
        print("✅ Information Ship Final is PRODUCTION-READY")
        return True
    else:
        print(f"⚠️  {failed} tests failed")
        print("⚠️  Review failures before production use")
        return False

if __name__ == "__main__":
    success = run_all_validation_tests()
    sys.exit(0 if success else 1)
