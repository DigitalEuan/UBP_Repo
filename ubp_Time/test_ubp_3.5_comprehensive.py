"""
================================================================================
Universal Binary Principle (UBP) Framework v3.5 - Comprehensive Test Suite
Author: Euan Craig, New Zealand
Date: November 12, 2025
================================================================================

Comprehensive tests for UBP 3.5 zero-dependency system.
"""

import math


def test_coherence_substrate():
    """Test coherence_substrate module."""
    print("\n" + "=" * 80)
    print("TEST 1: Coherence Substrate")
    print("=" * 80)
    
    from coherence_substrate import CoherenceState, integrate, solve_linear, NRCI_TARGET
    
    # Test CoherenceState
    state = CoherenceState(1.0)
    assert state.value == 1.0
    assert state.nrci >= NRCI_TARGET * 0.99
    print(f"✓ CoherenceState creation: value={state.value}, NRCI={state.nrci:.10f}")
    
    # Test operations
    state2 = state + CoherenceState(2.0)
    assert abs(state2.value - 3.0) < 1e-10
    print(f"✓ Addition: {state.value} + 2.0 = {state2.value}")
    
    # Test integration
    result = integrate(lambda x: x ** 2, 0, 1, n=100)
    expected = 1.0 / 3.0
    error = abs(result.value - expected) / expected
    assert error < 0.01
    print(f"✓ Integration: ∫x²dx from 0 to 1 = {result.value:.6f} (expected {expected:.6f})")
    
    # Test linear solver
    A = [[2, 1], [1, 3]]
    b = [1, 2]
    x = solve_linear(A, b)
    assert len(x) == 2
    print(f"✓ Linear solver: Ax=b solved, x=[{x[0].value:.6f}, {x[1].value:.6f}]")
    
    print("✓ Coherence Substrate: PASSED")
    return True


def test_y_constants():
    """Test y_constants module."""
    print("\n" + "=" * 80)
    print("TEST 2: Y Constants")
    print("=" * 80)
    
    from y_constants import Y_BASE, Y_INVERSE, Y_EMERGENT
    
    # Test Y × 1/Y = 1
    product = Y_BASE.value * Y_INVERSE.value
    assert abs(product - 1.0) < 1e-12
    print(f"✓ Y × 1/Y = {product:.15f} (error: {abs(product - 1.0):.2e})")
    
    # Test 1/Y = π + 2/π
    expected_inverse = math.pi + 2.0 / math.pi
    error = abs(Y_INVERSE.value - expected_inverse)
    assert error < 1e-12
    print(f"✓ 1/Y = π + 2/π: {Y_INVERSE.value:.15f} (error: {error:.2e})")
    
    # Test Y_EMERGENT
    assert Y_EMERGENT.value > 0
    assert Y_EMERGENT.nrci >= 0.999
    print(f"✓ Y_EMERGENT: {Y_EMERGENT.value:.15f}, NRCI: {Y_EMERGENT.nrci:.10f}")
    
    print("✓ Y Constants: PASSED")
    return True


def test_system_constants():
    """Test system_constants module."""
    print("\n" + "=" * 80)
    print("TEST 3: System Constants")
    print("=" * 80)
    
    from system_constants import PhysicalConstants, get_crv_for_realm
    
    # Test physical constants
    assert PhysicalConstants.SPEED_OF_LIGHT == 299792458.0
    assert PhysicalConstants.PLANCK_CONSTANT > 0
    print(f"✓ Physical constants loaded")
    
    # Test CRV for realms
    quantum_crv = get_crv_for_realm('quantum')
    assert quantum_crv.value > 0
    assert quantum_crv.nrci >= 0.999
    print(f"✓ Quantum CRV: {quantum_crv.value:.6e}, NRCI: {quantum_crv.nrci:.6f}")
    
    print("✓ System Constants: PASSED")
    return True


def test_energy_calculations():
    """Test energy calculation modules."""
    print("\n" + "=" * 80)
    print("TEST 4: Energy Calculations")
    print("=" * 80)
    
    from soc_energy import calculate_soc_energy
    from energy_dual import EnergyCalculator
    
    # Test SOC energy
    soc_result = calculate_soc_energy(modal_sum=1.0)
    assert soc_result.energy_cu > 0
    assert soc_result.nrci >= 0.999
    print(f"✓ SOC Energy: {soc_result.energy_cu:.6e} CU, NRCI: {soc_result.nrci:.10f}")
    
    # Test dual energy
    calc = EnergyCalculator()
    dual_result = calc.calculate(modal_sum=1.0, realm='quantum', frequency=1e15)
    assert dual_result.energy_cu > 0
    print(f"✓ Dual Energy: {dual_result.energy_cu:.6e} CU")
    
    print("✓ Energy Calculations: PASSED")
    return True


def test_realm_modules():
    """Test all 9 realm modules."""
    print("\n" + "=" * 80)
    print("TEST 5: Realm Modules")
    print("=" * 80)
    
    realms = [
        'quantum_realm',
        'atomic_realm',
        'electromagnetic_realm',
        'optical_realm',
        'nuclear_realm',
        'gravitational_realm',
        'biological_realm',
        'plasma_realm',
        'cosmological_realm'
    ]
    
    passed = 0
    for realm_name in realms:
        try:
            module = __import__(realm_name)
            print(f"✓ {realm_name}: imported successfully")
            passed += 1
        except Exception as e:
            print(f"✗ {realm_name}: {e}")
    
    assert passed == len(realms)
    print(f"✓ All {passed}/{len(realms)} Realm Modules: PASSED")
    return True


def test_error_correction():
    """Test error correction module."""
    print("\n" + "=" * 80)
    print("TEST 6: Error Correction")
    print("=" * 80)
    
    from geometric_error_correction import GeometricErrorCorrection, create_error_state
    
    # Create error correction system
    gec = GeometricErrorCorrection()
    
    # Test error state creation
    error_state = create_error_state(error_magnitude=0.01)
    assert error_state.value >= 0
    print(f"✓ Error state created: magnitude={error_state.value:.6e}")
    
    # Test correction
    corrected = gec.correct_error(error_state)
    assert corrected.nrci > error_state.nrci
    print(f"✓ Error corrected: NRCI {error_state.nrci:.6f} → {corrected.nrci:.6f}")
    
    print("✓ Error Correction: PASSED")
    return True


def test_state_management():
    """Test state management modules."""
    print("\n" + "=" * 80)
    print("TEST 7: State Management")
    print("=" * 80)
    
    from state import OffBit
    from toggle_ops import toggle_bit
    from tgic import TriadGraph
    
    # Test OffBit
    bit = OffBit()
    assert bit.value in [0, 1]
    print(f"✓ OffBit created: value={bit.value}")
    
    # Test toggle
    toggled = toggle_bit(bit)
    assert toggled.value != bit.value
    print(f"✓ Toggle: {bit.value} → {toggled.value}")
    
    # Test TGIC
    graph = TriadGraph(size=3)
    assert graph.size == 3
    print(f"✓ TriadGraph created: size={graph.size}")
    
    print("✓ State Management: PASSED")
    return True


def test_observer_framework():
    """Test observer framework."""
    print("\n" + "=" * 80)
    print("TEST 8: Observer Framework")
    print("=" * 80)
    
    from observer_framework import SelfActualizingObserver
    from y_constants import Y_INVERSE
    
    # Create observer
    observer = SelfActualizingObserver()
    
    # Test convergence
    result = observer.simulate_convergence(initial_cost=5.0, max_iterations=50)
    assert result.converged
    assert abs(result.final_cost - Y_INVERSE.value) < 0.01
    print(f"✓ Observer converged to: {result.final_cost:.15f}")
    print(f"✓ Target (1/Y): {Y_INVERSE.value:.15f}")
    print(f"✓ Iterations: {result.iterations}")
    
    print("✓ Observer Framework: PASSED")
    return True


def test_hex_dictionary():
    """Test hex dictionary."""
    print("\n" + "=" * 80)
    print("TEST 9: Hex Dictionary")
    print("=" * 80)
    
    from hex_dictionary import HexDictionary
    
    # Create dictionary
    hex_dict = HexDictionary()
    
    # Store and retrieve
    test_data = {'test': 'data', 'value': 123}
    hash_key = hex_dict.store(test_data, data_type='json')
    retrieved = hex_dict.retrieve(hash_key)
    
    assert retrieved == test_data
    print(f"✓ Stored and retrieved: {test_data}")
    print(f"✓ Hash: {hash_key[:16]}...")
    
    print("✓ Hex Dictionary: PASSED")
    return True


def run_all_tests():
    """Run all tests."""
    print("=" * 80)
    print("UBP 3.5 COMPREHENSIVE TEST SUITE")
    print("Zero Dependencies - Pure Python + Coherence Substrate")
    print("=" * 80)
    
    tests = [
        test_coherence_substrate,
        test_y_constants,
        test_system_constants,
        test_energy_calculations,
        test_realm_modules,
        test_error_correction,
        test_state_management,
        test_observer_framework,
        test_hex_dictionary
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"\n✗ {test.__name__} FAILED: {e}")
            failed += 1
    
    print("\n" + "=" * 80)
    print("TEST SUMMARY")
    print("=" * 80)
    print(f"Passed: {passed}/{len(tests)}")
    print(f"Failed: {failed}/{len(tests)}")
    
    if failed == 0:
        print("\n🎉 ALL TESTS PASSED - UBP 3.5 IS READY!")
        print("=" * 80)
        return True
    else:
        print("\n⚠️  SOME TESTS FAILED")
        print("=" * 80)
        return False


if __name__ == "__main__":
    success = run_all_tests()
    exit(0 if success else 1)
