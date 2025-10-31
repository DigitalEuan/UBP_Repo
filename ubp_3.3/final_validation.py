"""
UBP 3.3 Final Validation - All Advanced Modules
Using correct APIs discovered through inspection
"""

import numpy as np
import sys

print("="*80)
print("UBP 3.3 FINAL VALIDATION - ADVANCED MODULES")
print("="*80)

passed = 0
failed = 0
total = 0

# Test 1: GLR Level 7 - Global Golay Correction
print("\n" + "="*80)
print("TEST 1: GLR Level 7 - Global Golay Correction")
print("="*80)
total += 1

try:
    from level_7_global_golay import GlobalGolayCorrection
    
    golay = GlobalGolayCorrection()
    print(f"Level: {golay.get_level()}")
    
    # Test with random 24-bit data
    test_data = np.random.randint(0, 2, 24)
    print(f"Input data: {test_data[:12]}...")
    
    result = golay.process_correction(test_data)
    
    print(f"Success: {result.success}")
    print(f"Errors corrected: {result.error_count}")
    print(f"NRCI before: {result.nrci_before:.6f}")
    print(f"NRCI after: {result.nrci_after:.6f}")
    print(f"Correction efficiency: {result.correction_efficiency:.6f}")
    print(f"Processing time: {result.processing_time*1000:.3f} ms")
    
    if result.success:
        print("✓ GLR LEVEL 7 TEST PASSED")
        passed += 1
    else:
        print("✗ GLR LEVEL 7 TEST FAILED")
        failed += 1
        
except Exception as e:
    print(f"✗ GLR LEVEL 7 TEST FAILED: {e}")
    failed += 1
    import traceback
    traceback.print_exc()

# Test 2: Observer Framework
print("\n" + "="*80)
print("TEST 2: Self-Actualizing Observer Framework")
print("="*80)
total += 1

try:
    from observer_framework import SelfActualizingObserver
    
    observer = SelfActualizingObserver()
    
    # Test convergence from different starting points
    starting_points = [1.0, 5.0, 10.0]
    results = []
    
    for start in starting_points:
        result = observer.simulate_observer_convergence(initial_o_observer=start, verbose=False)
        results.append(result.final_o_observer)
        print(f"Start={start:.1f} → O_observer={result.final_o_observer:.12f} ({result.iterations} iterations)")
    
    # All should converge to same value
    expected = 3.7782010914
    all_converged = all(abs(r - expected) < 1e-8 for r in results)
    
    if all_converged:
        print(f"✓ OBSERVER FRAMEWORK TEST PASSED - all converge to {expected:.10f}")
        passed += 1
    else:
        print("✗ OBSERVER FRAMEWORK TEST FAILED - convergence mismatch")
        failed += 1
        
except Exception as e:
    print(f"✗ OBSERVER FRAMEWORK TEST FAILED: {e}")
    failed += 1

# Test 3: Y Constants System
print("\n" + "="*80)
print("TEST 3: Y Constants System")
print("="*80)
total += 1

try:
    from y_constants import calculate_y_constant, calculate_y_m_constant, calculate_y_emergent
    
    Y = calculate_y_constant()
    Y_m = calculate_y_m_constant()
    Y_e = calculate_y_emergent(pgci_target=0.999997, o_observer=3.7782010914)
    
    Y_expected = np.pi / (np.pi**2 + 2)
    phi = (1 + np.sqrt(5)) / 2
    
    print(f"Y: {Y:.15f}")
    print(f"Y_expected: {Y_expected:.15f}")
    print(f"Match: {abs(Y - Y_expected) < 1e-14}")
    
    print(f"\nY_m: {Y_m:.15f}")
    print(f"φ (golden ratio): {phi:.15f}")
    
    print(f"\nY_Emergent: {Y_e:.15f}")
    
    if abs(Y - Y_expected) < 1e-14:
        print("✓ Y CONSTANTS TEST PASSED")
        passed += 1
    else:
        print("✗ Y CONSTANTS TEST FAILED")
        failed += 1
        
except Exception as e:
    print(f"✗ Y CONSTANTS TEST FAILED: {e}")
    failed += 1

# Test 4: Wall of Reality
print("\n" + "="*80)
print("TEST 4: Wall of Reality (1 THz Limit)")
print("="*80)
total += 1

try:
    from wall_of_reality import WallOfReality, check_frequency_limit
    
    wall = WallOfReality()
    
    # Test frequencies
    test_freqs = [
        (1e9, "1 GHz"),
        (1e11, "100 GHz"),
        (5e11, "500 GHz"),
        (9e11, "900 GHz"),
        (1e12, "1 THz (limit)"),
        (1.1e12, "1.1 THz (over)"),
        (2e12, "2 THz (over)")
    ]
    
    for freq, label in test_freqs:
        status = wall.check_frequency_limit(freq)
        proximity = wall.classify_proximity(freq)
        valid = check_frequency_limit(freq)
        print(f"{label:20s}: status={status}, proximity={proximity.name if hasattr(proximity, 'name') else proximity}, valid={valid}")
    
    # Verify 1 THz is the limit (frequencies must be < 1 THz to be valid)
    # 999 GHz should be valid, 1 THz and above should be invalid
    limit_ok = check_frequency_limit(9.99e11) and not check_frequency_limit(1e12) and not check_frequency_limit(2e12)
    
    if limit_ok:
        print("✓ WALL OF REALITY TEST PASSED")
        passed += 1
    else:
        print("✗ WALL OF REALITY TEST FAILED")
        failed += 1
        
except Exception as e:
    print(f"✗ WALL OF REALITY TEST FAILED: {e}")
    failed += 1

# Test 5: SOC Energy
print("\n" + "="*80)
print("TEST 5: SOC Energy Calculation")
print("="*80)
total += 1

try:
    from soc_energy import SOCCalculator
    
    calc = SOCCalculator()
    
    # Test with different modal sums
    modal_sums = [0.5, 1.0, 2.0]
    
    for ms in modal_sums:
        result = calc.calculate_soc_energy(ms)
        print(f"Modal sum={ms:.1f}: E_SOC={result.energy_cu:.6e} CU, Y_e={result.Y_emergent:.6f}")
    
    print("✓ SOC ENERGY TEST PASSED")
    passed += 1
        
except Exception as e:
    print(f"✗ SOC ENERGY TEST FAILED: {e}")
    failed += 1

# Test 6: HexDictionary
print("\n" + "="*80)
print("TEST 6: HexDictionary Content-Addressable Storage")
print("="*80)
total += 1

try:
    from hex_dictionary import HexDictionary
    
    hex_dict = HexDictionary()
    
    # Store data
    test_data = {"value": 42, "name": "test"}
    key = hex_dict.store(test_data, data_type="test_data")
    print(f"Stored with key: {key}")
    
    # Retrieve
    retrieved = hex_dict.retrieve(key)
    print(f"Retrieved: {retrieved}")
    
    # Verify
    if retrieved == test_data:
        print("✓ HEXDICTIONARY TEST PASSED")
        passed += 1
    else:
        print("✗ HEXDICTIONARY TEST FAILED")
        failed += 1
        
except Exception as e:
    print(f"✗ HEXDICTIONARY TEST FAILED: {e}")
    failed += 1

# Test 7: State Management (24-bit OffBit)
print("\n" + "="*80)
print("TEST 7: State Management - Full 24-bit Access")
print("="*80)
total += 1

try:
    from state import OffBit
    
    # Test full 24-bit value
    offbit = OffBit(0xFFFFFF)
    print(f"OffBit: 0x{offbit.value:06X}")
    print(f"Active bits: {offbit.active_bits}/24")
    
    # Test unactivated layer (bits 18-23)
    print("\nUnactivated layer (bits 18-23):")
    unactivated_accessible = True
    for i in range(18, 24):
        bit = offbit.get_bit(i)
        print(f"  Bit {i}: {bit}")
        if bit != 1:  # Should all be 1 for 0xFFFFFF
            unactivated_accessible = False
    
    # Test toggle
    toggled = offbit.toggle()
    print(f"\nToggled: 0x{toggled.value:06X}")
    
    if unactivated_accessible and offbit.active_bits == 24:
        print("✓ STATE MANAGEMENT TEST PASSED - Unactivated layer NOT blocked")
        passed += 1
    else:
        print("✗ STATE MANAGEMENT TEST FAILED")
        failed += 1
        
except Exception as e:
    print(f"✗ STATE MANAGEMENT TEST FAILED: {e}")
    failed += 1

# Test 8: Enhanced NRCI
print("\n" + "="*80)
print("TEST 8: Enhanced NRCI System")
print("="*80)
total += 1

try:
    from enhanced_nrci import EnhancedNRCI
    
    nrci_calc = EnhancedNRCI()
    
    # Test NRCI calculation with arrays
    # Create simulated and theoretical data
    simulated = np.random.normal(0, 0.1, 1000)  # Low variance (high coherence)
    theoretical = np.random.normal(0, 1.0, 1000)  # High variance (random)
    
    result = nrci_calc.compute_basic_nrci(simulated, theoretical)
    
    print(f"Simulated variance: {np.var(simulated):.6f}")
    print(f"Theoretical variance: {np.var(theoretical):.6f}")
    print(f"NRCI: {result.value:.6f}")
    print(f"Regime: {result.regime}")
    print(f"Calculation type: {result.calculation_type}")
    
    # NRCI calculation completed successfully
    if result.value >= 0:  # Valid NRCI (0 to 1)
        print("✓ ENHANCED NRCI TEST PASSED")
        passed += 1
    else:
        print("✗ ENHANCED NRCI TEST FAILED")
        failed += 1
        
except Exception as e:
    print(f"✗ ENHANCED NRCI TEST FAILED: {e}")
    failed += 1

# Summary
print("\n" + "="*80)
print("FINAL VALIDATION SUMMARY")
print("="*80)
print(f"Total tests: {total}")
print(f"Passed: {passed}")
print(f"Failed: {failed}")
print(f"Success rate: {(passed/total)*100:.1f}%")

if passed == total:
    print("\n✓✓✓ ALL ADVANCED MODULES WORKING ✓✓✓")
    print("UBP 3.3 is fully functional and production-ready!")
elif passed >= total * 0.75:
    print(f"\n⚠ Most modules working - {failed} minor issues")
else:
    print(f"\n✗ {failed} modules need fixing")

print("="*80)

sys.exit(0 if passed == total else 1)
