"""
Corrected Functional Test for All UBP 3.7 Modules
==================================================

This test verifies that all modules can be imported and have working APIs.
"""

import sys
sys.path.insert(0, '/home/ubuntu/UBP_Repo/ubp_3.7')

def test_all_modules():
    """Test all modules with correct APIs."""
    results = []
    
    # Test 1: CoherenceState with apply_y_refinement
    try:
        from core.coherence_substrate import CoherenceState
        cs = CoherenceState(value=1.0)
        refined = cs.apply_y_refinement()
        assert refined is not None
        results.append(("CoherenceState", True, ""))
    except Exception as e:
        results.append(("CoherenceState", False, str(e)))
    
    # Test 2: OffBit with hamming_weight
    try:
        from core.state import OffBit
        ob = OffBit(pattern=0b101010)
        hw = ob.hamming_weight()
        assert hw == 3
        results.append(("OffBit", True, ""))
    except Exception as e:
        results.append(("OffBit", False, str(e)))
    
    # Test 3: LeechLatticePoint with __len__
    try:
        from error_correction.leech_lattice import LeechLattice
        import numpy as np
        lattice = LeechLattice()
        point = lattice.nearest_lattice_point(np.zeros(24))
        length = len(point)
        assert length == 24
        results.append(("LeechLattice", True, ""))
    except Exception as e:
        results.append(("LeechLattice", False, str(e)))
    
    # Test 4-11: All realms
    realms = [
        ("atomic_realm", "AtomicRealm"),
        ("electromagnetic_realm", "ElectromagneticRealm"),
        ("optical_realm", "OpticalRealm"),
        ("nuclear_realm", "NuclearRealm"),
        ("gravitational_realm", "GravitationalRealm"),
        ("biological_realm", "BiologicalRealm"),
        ("plasma_realm", "PlasmaRealm"),
        ("cosmological_realm", "CosmologicalRealm"),
    ]
    
    for module_name, class_name in realms:
        try:
            module = __import__(f"realms.{module_name}", fromlist=[class_name])
            RealmClass = getattr(module, class_name)
            realm = RealmClass()
            results.append((class_name, True, ""))
        except Exception as e:
            results.append((class_name, False, str(e)))
    
    # Test 12: ResonanceDetectorFFT (correct name)
    try:
        from analysis.resonance_detector_fft import ResonanceDetectorFFT
        import numpy as np
        detector = ResonanceDetectorFFT()
        signal = np.sin(2 * np.pi * 10 * np.linspace(0, 1, 1000))
        result = detector.detect_resonances(signal, sample_rate=1000)
        results.append(("ResonanceDetectorFFT", True, ""))
    except Exception as e:
        results.append(("ResonanceDetectorFFT", False, str(e)))
    
    # Test 13: PhysicsSimulator (correct API)
    try:
        from simulation.simulation import PhysicsSimulator, SimulationState
        import numpy as np
        
        sim = PhysicsSimulator()
        initial = SimulationState(position=np.array([1.0, 0.0]), velocity=np.array([0.0, 1.0]))
        
        def force(state):
            return -state.position  # Harmonic oscillator
        
        def energy(state):
            return 0.5 * (np.dot(state.velocity, state.velocity) + np.dot(state.position, state.position))
        
        result = sim.simulate(initial, force, energy, t_final=1.0, dt=0.01)
        results.append(("PhysicsSimulator", True, ""))
    except Exception as e:
        results.append(("PhysicsSimulator", False, str(e)))
    
    # Test 14: Reversible modules
    try:
        from reversible.reversible_coherence_state import ReversibleCoherenceState
        rcs = ReversibleCoherenceState(value=1.0)
        results.append(("ReversibleCoherenceState", True, ""))
    except Exception as e:
        results.append(("ReversibleCoherenceState", False, str(e)))
    
    # Print results
    print("\n" + "="*70)
    print("CORRECTED FUNCTIONAL TEST RESULTS")
    print("="*70)
    
    passed = sum(1 for _, success, _ in results if success)
    total = len(results)
    
    for name, success, error in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status:10} {name:30} {error[:40]}")
    
    print("="*70)
    print(f"TOTAL: {passed}/{total} passing ({100*passed/total:.1f}%)")
    print("="*70)
    
    return passed == total

if __name__ == "__main__":
    success = test_all_modules()
    sys.exit(0 if success else 1)
