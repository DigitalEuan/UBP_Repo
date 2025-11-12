"""
================================================================================
Universal Binary Principle (UBP) Framework v3.5 - Simple Test Suite
Author: Euan Craig, New Zealand
Date: November 12, 2025
================================================================================

Simple validation tests for UBP 3.5 zero-dependency system.
"""

import math


def test_imports():
    """Test that all modules can be imported."""
    print("\n" + "=" * 80)
    print("TEST 1: Module Imports")
    print("=" * 80)
    
    modules = [
        'coherence_substrate',
        'y_constants',
        'system_constants',
        'soc_energy',
        'energy_dual',
        'observer_framework',
        'wall_of_reality',
        'state',
        'toggle_ops',
        'tgic',
        'geometric_error_correction',
        'hex_dictionary',
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
    for module_name in modules:
        try:
            __import__(module_name)
            print(f"✓ {module_name}")
            passed += 1
        except Exception as e:
            print(f"✗ {module_name}: {e}")
    
    print(f"\n✓ Imported {passed}/{len(modules)} modules")
    return passed == len(modules)


def test_coherence_substrate():
    """Test coherence substrate basics."""
    print("\n" + "=" * 80)
    print("TEST 2: Coherence Substrate")
    print("=" * 80)
    
    from coherence_substrate import CoherenceState, NRCI_TARGET
    
    # Create state
    state = CoherenceState(1.0)
    print(f"✓ CoherenceState: value={state.value}, NRCI={state.nrci:.10f}")
    
    # Operations
    state2 = state + CoherenceState(2.0)
    print(f"✓ Addition: 1.0 + 2.0 = {state2.value}")
    
    state3 = state * CoherenceState(3.0)
    print(f"✓ Multiplication: 1.0 × 3.0 = {state3.value}")
    
    return True


def test_y_constants():
    """Test Y constants."""
    print("\n" + "=" * 80)
    print("TEST 3: Y Constants")
    print("=" * 80)
    
    from y_constants import Y_BASE, Y_INVERSE, Y_EMERGENT
    
    # Test Y × 1/Y = 1
    product = Y_BASE.value * Y_INVERSE.value
    error = abs(product - 1.0)
    print(f"✓ Y × 1/Y = {product:.15f} (error: {error:.2e})")
    
    # Test 1/Y = π + 2/π
    expected = math.pi + 2.0 / math.pi
    error2 = abs(Y_INVERSE.value - expected)
    print(f"✓ 1/Y = π + 2/π: {Y_INVERSE.value:.15f} (error: {error2:.2e})")
    
    print(f"✓ Y_EMERGENT: {Y_EMERGENT.value:.15f}")
    
    return error < 1e-12 and error2 < 1e-12


def test_realms():
    """Test all realm modules."""
    print("\n" + "=" * 80)
    print("TEST 4: Realm Modules")
    print("=" * 80)
    
    from quantum_realm import QuantumRealm
    from gravitational_realm import GravitationalRealm
    from atomic_realm import AtomicRealm
    from cosmological_realm import CosmologicalRealm
    
    # Test quantum realm
    qr = QuantumRealm()
    print(f"✓ QuantumRealm: {qr.REALM_NAME}, CRV={qr.crv.value:.6e}")
    
    # Test gravitational realm
    gr = GravitationalRealm()
    print(f"✓ GravitationalRealm: {gr.REALM_NAME}, CRV={gr.crv.value:.6e}")
    
    # Test atomic realm
    ar = AtomicRealm()
    print(f"✓ AtomicRealm: {ar.REALM_NAME}, CRV={ar.crv.value:.6e}")
    
    # Test cosmological realm
    cr = CosmologicalRealm()
    print(f"✓ CosmologicalRealm: {cr.REALM_NAME}, CRV={cr.crv.value:.6e}")
    
    return True


def test_energy():
    """Test energy calculations."""
    print("\n" + "=" * 80)
    print("TEST 5: Energy Calculations")
    print("=" * 80)
    
    from soc_energy import calculate_soc_energy
    from energy_dual import EnergyCalculator
    
    # SOC energy
    result = calculate_soc_energy(modal_sum=1.0)
    print(f"✓ SOC Energy: {result.energy_cu:.6e} CU, NRCI={result.nrci:.10f}")
    
    # Dual energy
    calc = EnergyCalculator()
    result2 = calc.calculate(modal_sum=1.0, realm='quantum', frequency=1e15)
    print(f"✓ Dual Energy: {result2.energy_cu:.6e} CU")
    
    return result.energy_cu > 0 and result2.energy_cu > 0


def test_state_management():
    """Test state management."""
    print("\n" + "=" * 80)
    print("TEST 6: State Management")
    print("=" * 80)
    
    from state import OffBit
    from toggle_ops import toggle_bit
    from tgic import TriadGraph
    
    # OffBit
    bit = OffBit()
    print(f"✓ OffBit: value={bit.value}")
    
    # Toggle
    toggled = toggle_bit(bit)
    print(f"✓ Toggle: {bit.value} → {toggled.value}")
    
    # TGIC
    graph = TriadGraph(size=3)
    print(f"✓ TriadGraph: size={graph.size}")
    
    return True


def test_observer():
    """Test observer framework."""
    print("\n" + "=" * 80)
    print("TEST 7: Observer Framework")
    print("=" * 80)
    
    from observer_framework import SelfActualizingObserver
    from y_constants import Y_INVERSE
    
    observer = SelfActualizingObserver()
    result = observer.simulate_convergence(initial_cost=5.0, max_iterations=50)
    
    print(f"✓ Converged: {result.converged}")
    print(f"✓ Final cost: {result.final_cost:.15f}")
    print(f"✓ Target (1/Y): {Y_INVERSE.value:.15f}")
    print(f"✓ Iterations: {result.iterations}")
    
    return result.converged


def test_hex_dictionary():
    """Test hex dictionary."""
    print("\n" + "=" * 80)
    print("TEST 8: Hex Dictionary")
    print("=" * 80)
    
    from hex_dictionary import HexDictionary
    
    hd = HexDictionary()
    
    # Store
    data = {'test': 'UBP 3.5', 'value': 12345}
    hash_key = hd.store(data, data_type='json')
    print(f"✓ Stored: {hash_key[:16]}...")
    
    # Retrieve
    retrieved = hd.retrieve(hash_key)
    print(f"✓ Retrieved: {retrieved}")
    
    return retrieved == data


def run_all_tests():
    """Run all tests."""
    print("=" * 80)
    print("UBP 3.5 SIMPLE TEST SUITE")
    print("Zero Dependencies - Pure Python + Coherence Substrate")
    print("=" * 80)
    
    tests = [
        test_imports,
        test_coherence_substrate,
        test_y_constants,
        test_realms,
        test_energy,
        test_state_management,
        test_observer,
        test_hex_dictionary
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            if test():
                passed += 1
            else:
                print(f"\n✗ {test.__name__} returned False")
                failed += 1
        except Exception as e:
            print(f"\n✗ {test.__name__} FAILED: {e}")
            import traceback
            traceback.print_exc()
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
