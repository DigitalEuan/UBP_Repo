"""
================================================================================
Comprehensive Test Suite for All 9 Realm Scripts (UBP 3.6.2)
================================================================================

Tests all realm scripts with their new Coherence Field ELITE integration:
- Basic realm functionality
- Resonance detection
- Temporal evolution with resonance tracking
- Parameter optimization
- Integration with OffBit and toggle operations

Author: Euan R A Craig, New Zealand
Date: November 20, 2025
"""

import sys
import os
import math

# Add ubp_3.6 to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from coherence_substrate import CoherenceState, NRCI_TARGET
from state import OffBit
import coherence_field as cf

# Import all realm modules
import atomic_realm as atomic
import biological_realm as biological
import cosmological_realm as cosmological
import electromagnetic_realm as electromagnetic
import gravitational_realm as gravitational
import nuclear_realm as nuclear
import optical_realm as optical
import plasma_realm as plasma
import quantum_realm as quantum


# ============================================================================
# TEST CONFIGURATION
# ============================================================================

REALMS = {
    'atomic': (atomic.AtomicRealm, 1e13),
    'biological': (biological.BiologicalRealm, 1e9),
    'cosmological': (cosmological.CosmologicalRealm, 1e-18),
    'electromagnetic': (electromagnetic.ElectromagneticRealm, 1e12),
    'gravitational': (gravitational.GravitationalRealm, 1e-15),
    'nuclear': (nuclear.NuclearRealm, 1e20),
    'optical': (optical.OpticalRealm, 1e15),
    'plasma': (plasma.PlasmaRealm, 1e10),
    'quantum': (quantum.QuantumRealm, 1e15)
}


# ============================================================================
# TEST FUNCTIONS
# ============================================================================

def test_realm_initialization(realm_name, realm_class):
    """Test that realm can be initialized."""
    print(f"\n{'='*80}")
    print(f"TEST 1: {realm_name.upper()} REALM - Initialization")
    print('='*80)
    
    try:
        realm = realm_class()
        print(f"✓ {realm_name.capitalize()} realm initialized")
        print(f"  Realm name: {realm.REALM_NAME}")
        print(f"  CRV: {realm.crv.value:.6e}, NRCI: {realm.crv.nrci:.6f}")
        return True
    except Exception as e:
        print(f"✗ Failed to initialize {realm_name} realm: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_detect_resonances(realm_name, realm_class, frequency):
    """Test resonance detection method."""
    print(f"\n{'='*80}")
    print(f"TEST 2: {realm_name.upper()} REALM - Resonance Detection")
    print('='*80)
    
    try:
        realm = realm_class()
        
        # Create test states with varying coherence
        states = []
        for i in range(20):
            # Create states with slight variations
            value = 1.0 + i * 0.01
            nrci = NRCI_TARGET * (1.0 - i * 0.001)
            log_error = math.log(1.0 - nrci)
            state = CoherenceState(value, log_nrci_error=log_error)
            states.append(state)
        
        # Detect resonances
        resonance = realm.detect_resonances(states)
        
        print(f"✓ Resonance detection executed")
        print(f"  Test states: {len(states)}")
        if resonance:
            print(f"  Resonance detected: {resonance.p}/{resonance.q}")
            print(f"  Confidence: {resonance.confidence:.1%}")
        else:
            print(f"  No strong resonance detected (expected for random data)")
        
        return True
    except Exception as e:
        print(f"✗ Resonance detection failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_temporal_evolution(realm_name, realm_class, frequency):
    """Test temporal evolution with resonance tracking."""
    print(f"\n{'='*80}")
    print(f"TEST 3: {realm_name.upper()} REALM - Temporal Evolution")
    print('='*80)
    
    try:
        realm = realm_class()
        
        # Create initial OffBit
        offbit = OffBit(0x123456)
        
        # Analyze temporal evolution
        result = realm.analyze_temporal_evolution(
            offbit, 
            frequency=frequency, 
            steps=50,
            k=0.0002
        )
        
        print(f"✓ Temporal evolution executed")
        print(f"  Evolution steps: 50")
        print(f"  History length: {result['history_length']}")
        print(f"  Resonance detected: {result['resonance_detected']}")
        print(f"  Reset points: {len(result['reset_points'])}")
        print(f"  Coherence valleys: {len(result['coherence_valleys'])}")
        
        if result['statistics']['history_length'] > 0:
            stats = result['statistics']
            print(f"  Avg resonance factor: {stats['avg_resonance_factor']:.6f}")
            print(f"  Min resonance factor: {stats['min_resonance_factor']:.6f}")
            print(f"  Max resonance factor: {stats['max_resonance_factor']:.6f}")
        
        # Verify result structure
        assert 'final_state' in result, "Missing final_state"
        assert 'resonance_analysis' in result, "Missing resonance_analysis"
        assert 'reset_points' in result, "Missing reset_points"
        assert 'coherence_valleys' in result, "Missing coherence_valleys"
        assert 'statistics' in result, "Missing statistics"
        
        return True
    except Exception as e:
        print(f"✗ Temporal evolution failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_optimize_parameters(realm_name, realm_class, frequency):
    """Test parameter optimization method."""
    print(f"\n{'='*80}")
    print(f"TEST 4: {realm_name.upper()} REALM - Parameter Optimization")
    print('='*80)
    
    try:
        realm = realm_class()
        
        # Create test states
        states = []
        for i in range(15):
            value = 1.0 + i * 0.05
            nrci = NRCI_TARGET * (1.0 - i * 0.002)
            log_error = math.log(1.0 - nrci)
            state = CoherenceState(value, log_nrci_error=log_error)
            states.append(state)
        
        # Optimize parameters
        result = realm.optimize_parameters(states, target_param='frequency')
        
        print(f"✓ Parameter optimization executed")
        print(f"  Test states: {len(states)}")
        
        if 'error' in result:
            print(f"  Result: {result['error']}")
        else:
            print(f"  Optimization result keys: {list(result.keys())}")
        
        return True
    except Exception as e:
        print(f"✗ Parameter optimization failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_integration_completeness(realm_name, realm_class):
    """Test that all integration methods exist."""
    print(f"\n{'='*80}")
    print(f"TEST 5: {realm_name.upper()} REALM - Integration Completeness")
    print('='*80)
    
    try:
        realm = realm_class()
        
        # Check for required methods
        required_methods = [
            'detect_resonances',
            'analyze_temporal_evolution',
            'optimize_parameters'
        ]
        
        missing = []
        for method_name in required_methods:
            if not hasattr(realm, method_name):
                missing.append(method_name)
        
        if missing:
            print(f"✗ Missing methods: {missing}")
            return False
        
        print(f"✓ All integration methods present")
        for method_name in required_methods:
            method = getattr(realm, method_name)
            print(f"  - {method_name}: {type(method)}")
        
        return True
    except Exception as e:
        print(f"✗ Integration completeness check failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def run_realm_tests(realm_name, realm_class, frequency):
    """Run all tests for a single realm."""
    print(f"\n\n{'#'*80}")
    print(f"# TESTING {realm_name.upper()} REALM")
    print(f"# Characteristic frequency: {frequency:.2e} Hz")
    print(f"{'#'*80}")
    
    tests = [
        (test_realm_initialization, [realm_name, realm_class]),
        (test_detect_resonances, [realm_name, realm_class, frequency]),
        (test_temporal_evolution, [realm_name, realm_class, frequency]),
        (test_optimize_parameters, [realm_name, realm_class, frequency]),
        (test_integration_completeness, [realm_name, realm_class])
    ]
    
    passed = 0
    failed = 0
    
    for test_func, args in tests:
        try:
            if test_func(*args):
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"\n✗ Test crashed: {e}")
            import traceback
            traceback.print_exc()
            failed += 1
    
    print(f"\n{'-'*80}")
    print(f"{realm_name.upper()} REALM SUMMARY: {passed}/{passed+failed} tests passed")
    print(f"{'-'*80}")
    
    return passed, failed


# ============================================================================
# MAIN TEST RUNNER
# ============================================================================

def run_all_tests():
    """Run tests for all 9 realms."""
    print("="*80)
    print("COMPREHENSIVE REALM INTEGRATION TEST SUITE")
    print("UBP 3.6.2 - Coherence Field ELITE Integration")
    print("="*80)
    print(f"\nTesting {len(REALMS)} realms with 5 tests each")
    print(f"Total tests: {len(REALMS) * 5}")
    
    total_passed = 0
    total_failed = 0
    realm_results = {}
    
    for realm_name, (realm_class, frequency) in REALMS.items():
        passed, failed = run_realm_tests(realm_name, realm_class, frequency)
        total_passed += passed
        total_failed += failed
        realm_results[realm_name] = (passed, failed)
    
    # Final summary
    print("\n\n" + "="*80)
    print("FINAL TEST SUMMARY")
    print("="*80)
    
    print(f"\nRealm-by-Realm Results:")
    for realm_name, (passed, failed) in realm_results.items():
        total = passed + failed
        pct = (passed / total * 100) if total > 0 else 0
        status = "✓" if failed == 0 else "✗"
        print(f"  {status} {realm_name.capitalize():20s}: {passed}/{total} ({pct:.1f}%)")
    
    print(f"\nOverall Results:")
    print(f"  Total tests: {total_passed + total_failed}")
    print(f"  Passed: {total_passed}")
    print(f"  Failed: {total_failed}")
    
    total_tests = total_passed + total_failed
    pass_rate = (total_passed / total_tests * 100) if total_tests > 0 else 0
    print(f"  Pass rate: {pass_rate:.1f}%")
    
    if total_failed == 0:
        print("\n✓ ALL TESTS PASSED")
        print("\nAll 9 realms successfully integrated with Coherence Field ELITE!")
    else:
        print(f"\n✗ {total_failed} TESTS FAILED")
    
    print("="*80)
    
    return total_failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
