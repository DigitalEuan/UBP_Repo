#!/usr/bin/env python3
"""
UBP 3.7 - Edge Case Testing
===========================

Brutal testing of edge cases, boundary conditions, and error handling.

This script tests all the ways things could break.

Author: UBP 3.7 Development
Date: November 28, 2025
Version: 3.7.0
"""

import numpy as np
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'error_correction'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'core'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'analysis'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'simulation'))


def test_golay_edge_cases():
    """Test Golay code with edge cases."""
    from golay_code import GolayG24
    
    print("\n" + "="*70)
    print("EDGE CASE TEST: GOLAY CODE")
    print("="*70)
    
    golay = GolayG24()
    issues = []
    
    # Test 1: All zeros
    msg_zeros = np.zeros(12, dtype=int)
    cw_zeros = golay.encode(msg_zeros)
    if not golay.is_codeword(cw_zeros):
        issues.append("All-zeros message doesn't produce valid codeword")
    print(f"✓ All-zeros message: {np.sum(cw_zeros)} bits set")
    
    # Test 2: All ones
    msg_ones = np.ones(12, dtype=int)
    cw_ones = golay.encode(msg_ones)
    if not golay.is_codeword(cw_ones):
        issues.append("All-ones message doesn't produce valid codeword")
    print(f"✓ All-ones message: {np.sum(cw_ones)} bits set")
    
    # Test 3: 4-bit errors (should NOT correct)
    test_cw = golay.encode(np.array([1,0,1,0,1,0,1,0,1,0,1,0]))
    corrupted_4 = test_cw.copy()
    corrupted_4[[0,5,10,15]] = 1 - corrupted_4[[0,5,10,15]]
    corrected_4 = golay.correct_errors(corrupted_4)
    # Should NOT match original (too many errors)
    if np.array_equal(corrected_4, test_cw):
        issues.append("Incorrectly 'corrected' 4-bit errors")
    print(f"✓ 4-bit errors: correctly NOT corrected")
    
    # Test 4: Invalid input sizes
    try:
        golay.encode(np.array([1,0,1]))  # Too short
        issues.append("Accepted wrong message length")
    except ValueError:
        print(f"✓ Rejects wrong message length")
    
    # Test 5: Non-binary input
    msg_nonbinary = np.array([1,0,2,0,1,0,1,0,1,0,1,0])
    cw_nonbinary = golay.encode(msg_nonbinary)  # Should mod 2
    if not golay.is_codeword(cw_nonbinary):
        issues.append("Non-binary input not handled correctly")
    print(f"✓ Non-binary input handled (mod 2)")
    
    # Test 6: Round-trip with random messages
    for _ in range(10):
        msg = np.random.randint(0, 2, 12)
        cw = golay.encode(msg)
        decoded = golay.decode(cw)
        if not np.array_equal(msg, decoded):
            issues.append("Round-trip failed for random message")
            break
    print(f"✓ Round-trip encoding/decoding works")
    
    if issues:
        print(f"\n✗ ISSUES FOUND:")
        for issue in issues:
            print(f"  - {issue}")
        return False
    else:
        print(f"\n✓ PASS: All edge cases handled correctly")
        return True


def test_leech_edge_cases():
    """Test Leech lattice with edge cases."""
    from leech_lattice import LeechLattice, LeechLatticePoint
    
    print("\n" + "="*70)
    print("EDGE CASE TEST: LEECH LATTICE")
    print("="*70)
    
    lattice = LeechLattice()
    issues = []
    
    # Test 1: Zero vector
    zero_point = LeechLatticePoint(np.zeros(24))
    if not lattice.is_in_lattice(zero_point):
        issues.append("Zero vector not in lattice")
    print(f"✓ Zero vector in lattice")
    
    # Test 2: Very large coordinates
    large_coords = np.array([1000.0] * 24)
    nearest = lattice.nearest_lattice_point(large_coords)  # Pass numpy array
    if nearest.norm_squared < 0:
        issues.append("Large coordinates cause negative norm")
    print(f"✓ Large coordinates handled: norm²={nearest.norm_squared}")
    
    # Test 3: Negative coordinates
    neg_coords = np.array([-1.0, 1.0] * 12)
    neg_point = LeechLatticePoint(neg_coords)
    if not lattice.is_in_lattice(neg_point):
        issues.append("Negative coordinates rejected incorrectly")
    print(f"✓ Negative coordinates handled")
    
    # Test 4: Non-integer coordinates
    float_coords = np.array([0.5] * 24)
    nearest_float = lattice.nearest_lattice_point(float_coords)  # Pass numpy array
    # Should find nearest lattice point
    if not lattice.is_in_lattice(nearest_float):
        issues.append("Nearest lattice point is not in lattice")
    print(f"✓ Non-integer coordinates: nearest point found")
    
    # Test 5: Point arithmetic
    p1 = LeechLatticePoint(np.array([1.0] * 24))
    p2 = LeechLatticePoint(np.array([2.0] * 24))
    p_sum = p1 + p2
    p_diff = p2 - p1
    if not isinstance(p_sum, LeechLatticePoint):
        issues.append("Point addition doesn't return LeechLatticePoint")
    print(f"✓ Point arithmetic works")
    
    if issues:
        print(f"\n✗ ISSUES FOUND:")
        for issue in issues:
            print(f"  - {issue}")
        return False
    else:
        print(f"\n✓ PASS: All edge cases handled correctly")
        return True


def test_vector_offbit_edge_cases():
    """Test VectorOffBit with edge cases."""
    from vector_offbit import VectorOffBit
    from coherence_substrate import CoherenceState
    
    print("\n" + "="*70)
    print("EDGE CASE TEST: VECTOROFFBIT")
    print("="*70)
    
    issues = []
    
    # Test 1: All zeros
    v_zeros = VectorOffBit.from_binary(0)
    if v_zeros.norm() != 0:
        issues.append("Zero vector has non-zero norm")
    print(f"✓ Zero vector: norm={v_zeros.norm()}")
    
    # Test 2: All ones
    v_ones = VectorOffBit.from_binary(0b111111111111111111111111)
    expected_norm = np.sqrt(24)
    if abs(v_ones.norm() - expected_norm) > 0.01:
        issues.append(f"All-ones vector has wrong norm: {v_ones.norm()} vs {expected_norm}")
    print(f"✓ All-ones vector: norm={v_ones.norm():.4f}")
    
    # Test 3: Single bit
    v_single = VectorOffBit.from_binary(0b000000000000000000000001)
    if v_single.norm() != 1.0:
        issues.append("Single-bit vector has wrong norm")
    print(f"✓ Single-bit vector: norm={v_single.norm()}")
    
    # Test 4: Dot product properties
    v1 = VectorOffBit.from_binary(0b101010101010101010101010)
    v2 = VectorOffBit.from_binary(0b010101010101010101010101)
    dot = v1.dot(v2)
    # These are orthogonal in binary space
    if dot != 0:
        issues.append(f"Orthogonal vectors have non-zero dot product: {dot}")
    print(f"✓ Orthogonal vectors: dot={dot}")
    
    # Test 5: Conversion round-trip
    for _ in range(10):
        original_scalar = np.random.randint(0, 2**24)
        v = VectorOffBit.from_binary(original_scalar)
        recovered_scalar = v.to_scalar()
        if original_scalar != recovered_scalar:
            issues.append(f"Conversion round-trip failed: {original_scalar} != {recovered_scalar}")
            break
    print(f"✓ Conversion round-trip works")
    
    # Test 6: Normalization
    v_unnorm = VectorOffBit(np.array([3.0, 4.0] + [0.0] * 22), CoherenceState(1.0))
    v_norm = v_unnorm.normalize()
    if abs(v_norm.norm() - 1.0) > 0.01:
        issues.append(f"Normalized vector has wrong norm: {v_norm.norm()}")
    print(f"✓ Normalization works: norm={v_norm.norm():.6f}")
    
    if issues:
        print(f"\n✗ ISSUES FOUND:")
        for issue in issues:
            print(f"  - {issue}")
        return False
    else:
        print(f"\n✓ PASS: All edge cases handled correctly")
        return True


def test_fft_edge_cases():
    """Test FFT resonance detector with edge cases."""
    from resonance_detector_fft import ResonanceDetectorFFT
    
    print("\n" + "="*70)
    print("EDGE CASE TEST: FFT RESONANCE DETECTOR")
    print("="*70)
    
    detector = ResonanceDetectorFFT(sample_rate=1000.0)
    issues = []
    
    # Test 1: DC signal (all same value)
    dc_signal = np.ones(1000)
    analysis_dc = detector.analyze_spectrum(dc_signal)
    print(f"✓ DC signal: {len(analysis_dc.peaks)} peaks detected")
    
    # Test 2: Pure noise
    noise = np.random.randn(1000)
    analysis_noise = detector.analyze_spectrum(noise)
    print(f"✓ Pure noise: {len(analysis_noise.peaks)} peaks detected")
    
    # Test 3: Nyquist frequency
    t = np.linspace(0, 1, 1000)
    nyquist_signal = np.sin(2 * np.pi * 500 * t)  # Nyquist = sample_rate/2
    analysis_nyquist = detector.analyze_spectrum(nyquist_signal)
    print(f"✓ Nyquist frequency: {len(analysis_nyquist.peaks)} peaks detected")
    
    # Test 4: Very short signal
    short_signal = np.sin(2 * np.pi * 50 * np.linspace(0, 0.1, 10))
    try:
        analysis_short = detector.analyze_spectrum(short_signal)
        print(f"✓ Short signal (10 samples): handled")
    except:
        issues.append("Short signal causes crash")
    
    # Test 5: Empty signal
    try:
        empty_signal = np.array([])
        analysis_empty = detector.analyze_spectrum(empty_signal)
        issues.append("Empty signal should raise error")
    except:
        print(f"✓ Empty signal: correctly rejected")
    
    # Test 6: Constant signal (zero amplitude)
    zero_signal = np.zeros(1000)
    analysis_zero = detector.analyze_spectrum(zero_signal)
    print(f"✓ Zero signal: {len(analysis_zero.peaks)} peaks detected")
    
    if issues:
        print(f"\n✗ ISSUES FOUND:")
        for issue in issues:
            print(f"  - {issue}")
        return False
    else:
        print(f"\n✓ PASS: All edge cases handled correctly")
        return True


def test_simulation_edge_cases():
    """Test physics simulator with edge cases."""
    from simulation import PhysicsSimulator, HarmonicOscillator, SimulationState
    from coherence_substrate import CoherenceState
    
    print("\n" + "="*70)
    print("EDGE CASE TEST: PHYSICS SIMULATOR")
    print("="*70)
    
    oscillator = HarmonicOscillator(k=1.0, m=1.0)
    simulator = PhysicsSimulator(dimension=1, integration_method='rk4')
    issues = []
    
    # Test 1: Zero initial conditions
    state_zero = SimulationState(
        time=0.0,
        position=np.array([0.0]),
        velocity=np.array([0.0]),
        energy=0.0,
        coherence=CoherenceState(0.0)
    )
    result_zero = simulator.simulate(
        initial_state=state_zero,
        force_func=oscillator.force,
        energy_func=oscillator.energy,
        t_final=1.0,
        dt=0.01
    )
    if not result_zero.success:
        issues.append("Zero initial conditions cause failure")
    print(f"✓ Zero initial conditions: E_drift={result_zero.energy_conservation:.2e}")
    
    # Test 2: Very high energy
    state_high = SimulationState(
        time=0.0,
        position=np.array([100.0]),
        velocity=np.array([100.0]),
        energy=0.0,
        coherence=CoherenceState(1.0)
    )
    result_high = simulator.simulate(
        initial_state=state_high,
        force_func=oscillator.force,
        energy_func=oscillator.energy,
        t_final=1.0,
        dt=0.01
    )
    if not result_high.success:
        issues.append("High energy causes failure")
    print(f"✓ High energy: E_drift={result_high.energy_conservation:.2e}")
    
    # Test 3: Very small timestep
    state_normal = SimulationState(
        time=0.0,
        position=np.array([1.0]),
        velocity=np.array([0.0]),
        energy=0.0,
        coherence=CoherenceState(1.0)
    )
    result_small_dt = simulator.simulate(
        initial_state=state_normal,
        force_func=oscillator.force,
        energy_func=oscillator.energy,
        t_final=0.1,
        dt=0.0001  # Very small
    )
    if not result_small_dt.success:
        issues.append("Small timestep causes failure")
    print(f"✓ Small timestep (0.0001): E_drift={result_small_dt.energy_conservation:.2e}")
    
    # Test 4: Large timestep (should be less accurate)
    result_large_dt = simulator.simulate(
        initial_state=state_normal,
        force_func=oscillator.force,
        energy_func=oscillator.energy,
        t_final=10.0,
        dt=0.5  # Large
    )
    if not result_large_dt.success:
        issues.append("Large timestep causes failure")
    print(f"✓ Large timestep (0.5): E_drift={result_large_dt.energy_conservation:.2e}")
    
    if issues:
        print(f"\n✗ ISSUES FOUND:")
        for issue in issues:
            print(f"  - {issue}")
        return False
    else:
        print(f"\n✓ PASS: All edge cases handled correctly")
        return True


# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    print("="*70)
    print("UBP 3.7 EDGE CASE TESTING")
    print("="*70)
    print("\nTesting all components with edge cases and boundary conditions...")
    
    results = []
    
    results.append(("Golay Code", test_golay_edge_cases()))
    results.append(("Leech Lattice", test_leech_edge_cases()))
    results.append(("VectorOffBit", test_vector_offbit_edge_cases()))
    results.append(("FFT Resonance Detector", test_fft_edge_cases()))
    results.append(("Physics Simulator", test_simulation_edge_cases()))
    
    # Summary
    print("\n" + "="*70)
    print("EDGE CASE TEST SUMMARY")
    print("="*70)
    
    for name, passed in results:
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{status} | {name}")
    
    passed_count = sum(1 for _, p in results if p)
    total_count = len(results)
    
    print("="*70)
    print(f"TOTAL: {passed_count}/{total_count} components passed ({100*passed_count/total_count:.1f}%)")
    print("="*70)
    
    sys.exit(0 if passed_count == total_count else 1)
