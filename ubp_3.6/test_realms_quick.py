"""Quick functional test for all 9 realms with Coherence Field ELITE integration."""

import sys
import os
import math

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from coherence_substrate import CoherenceState, NRCI_TARGET
from state import OffBit

# Import all realms
import atomic_realm, biological_realm, cosmological_realm, electromagnetic_realm
import gravitational_realm, nuclear_realm, optical_realm, plasma_realm, quantum_realm

REALMS = {
    'atomic': (atomic_realm.AtomicRealm, 1e13),
    'biological': (biological_realm.BiologicalRealm, 1e9),
    'cosmological': (cosmological_realm.CosmologicalRealm, 1e-18),
    'electromagnetic': (electromagnetic_realm.ElectromagneticRealm, 1e12),
    'gravitational': (gravitational_realm.GravitationalRealm, 1e-15),
    'nuclear': (nuclear_realm.NuclearRealm, 1e20),
    'optical': (optical_realm.OpticalRealm, 1e15),
    'plasma': (plasma_realm.PlasmaRealm, 1e10),
    'quantum': (quantum_realm.QuantumRealm, 1e15)
}

def test_realm(name, cls, freq):
    """Test a single realm."""
    print(f"\n{'='*60}")
    print(f"Testing {name.upper()} Realm")
    print('='*60)
    
    try:
        # Initialize
        realm = cls()
        print(f"✓ Initialized: {realm.REALM_NAME}")
        
        # Test detect_resonances
        states = [CoherenceState(1.0 + i*0.01, log_nrci_error=math.log(1 - NRCI_TARGET*(1-i*0.001))) 
                  for i in range(10)]
        resonance = realm.detect_resonances(states)
        print(f"✓ detect_resonances: {'detected' if resonance else 'no resonance'}")
        
        # Test analyze_temporal_evolution
        offbit = OffBit(0x123456)
        result = realm.analyze_temporal_evolution(offbit, freq, steps=20, k=0.0002)
        print(f"✓ analyze_temporal_evolution: {result['history_length']} steps tracked")
        
        # Test optimize_parameters
        opt_result = realm.optimize_parameters(states[:5], 'frequency')
        print(f"✓ optimize_parameters: optimal_index={opt_result.get('optimal_index', 'N/A')}")
        
        return True
    except Exception as e:
        print(f"✗ FAILED: {e}")
        return False

def main():
    print("="*60)
    print("QUICK FUNCTIONAL TEST - ALL 9 REALMS")
    print("UBP 3.6.2 Coherence Field ELITE Integration")
    print("="*60)
    
    passed = 0
    failed = 0
    
    for name, (cls, freq) in REALMS.items():
        if test_realm(name, cls, freq):
            passed += 1
        else:
            failed += 1
    
    print(f"\n{'='*60}")
    print(f"RESULTS: {passed}/{passed+failed} realms passed")
    print('='*60)
    
    if failed == 0:
        print("\n✓ ALL REALMS FULLY FUNCTIONAL")
    else:
        print(f"\n✗ {failed} realms failed")
    
    return failed == 0

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
