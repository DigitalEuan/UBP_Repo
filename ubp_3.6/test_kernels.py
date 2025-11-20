"""
Test suite for UBP 3.6.2 Mathematical Kernels
"""

import kernels as k
import math


def test_resonance_kernel():
    """Test resonance kernel function."""
    print("=" * 60)
    print("TEST 1: Resonance Kernel")
    print("=" * 60)
    
    # Test perfect resonance
    assert k.resonance_kernel(0.0) == 1.0
    print("✓ Perfect resonance at d=0")
    
    # Test decay
    r1 = k.resonance_kernel(1.0)
    r10 = k.resonance_kernel(10.0)
    assert r1 > r10  # Should decay with distance
    print(f"✓ Decay: r(1)={r1:.6f} > r(10)={r10:.6f}")
    
    # Test custom k
    r_default = k.resonance_kernel(5.0)
    r_custom = k.resonance_kernel(5.0, k=0.001)
    assert r_custom < r_default  # Larger k = faster decay
    print(f"✓ Custom k: r(k=0.001)={r_custom:.6f} < r(k=0.0002)={r_default:.6f}")
    
    return True


def test_coherence():
    """Test coherence functions."""
    print("=" * 60)
    print("TEST 2: Coherence Calculations")
    print("=" * 60)
    
    # Test identical signals
    s1 = [1.0, 2.0, 3.0, 4.0, 5.0]
    c = k.coherence(s1, s1)
    assert c > 0
    print(f"✓ Self-coherence: {c:.6f}")
    
    # Test normalized coherence
    nc = k.normalized_coherence(s1, s1)
    assert abs(nc - 1.0) < 1e-10  # Should be exactly 1.0
    print(f"✓ Normalized self-coherence: {nc:.6f}")
    
    # Test anti-correlated signals
    s2 = [5.0, 4.0, 3.0, 2.0, 1.0]
    nc2 = k.normalized_coherence(s1, s2)
    assert 0 <= nc2 <= 1
    print(f"✓ Anti-correlated coherence: {nc2:.6f}")
    
    # Test empty signals
    assert k.coherence([], []) == 0.0
    print("✓ Empty signals return 0")
    
    # Test error on mismatched lengths
    try:
        k.coherence([1, 2], [1, 2, 3])
        assert False, "Should raise ValueError"
    except ValueError:
        print("✓ Raises ValueError on mismatched lengths")
    
    return True


def test_signal_generation():
    """Test signal generation."""
    print("=" * 60)
    print("TEST 3: Signal Generation")
    print("=" * 60)
    
    # Generate 1 Hz signal for 1 second at 100 Hz sample rate
    signal = k.generate_oscillating_signal(1.0, 0.0, 1.0, 100.0)
    
    # Should have 100 samples
    assert len(signal) == 100
    print(f"✓ Generated {len(signal)} samples")
    
    # First sample should be cos(0) = 1.0
    assert abs(signal[0] - 1.0) < 1e-10
    print(f"✓ First sample: {signal[0]:.6f}")
    
    # Test with phase offset
    signal_phase = k.generate_oscillating_signal(1.0, math.pi/2, 1.0, 100.0)
    assert abs(signal_phase[0] - 0.0) < 1e-10  # cos(π/2) = 0
    print(f"✓ Phase offset works: {signal_phase[0]:.6f}")
    
    return True


def test_frequency_wavelength():
    """Test frequency/wavelength conversions."""
    print("=" * 60)
    print("TEST 4: Frequency/Wavelength Conversions")
    print("=" * 60)
    
    # Test round-trip conversion
    wavelength = 500.0  # nm (green light)
    freq = k.calculate_frequency_from_wavelength(wavelength)
    wavelength_back = k.calculate_wavelength_from_frequency(freq)
    
    assert abs(wavelength - wavelength_back) < 1e-6
    print(f"✓ Round-trip: {wavelength:.1f} nm → {freq:.6e} Hz → {wavelength_back:.1f} nm")
    
    # Test known values
    # 500 nm should be ~6e14 Hz
    assert 5e14 < freq < 7e14
    print(f"✓ Green light frequency in expected range")
    
    return True


def test_special_resonances():
    """Test special resonance frequencies."""
    print("=" * 60)
    print("TEST 5: Special Resonance Frequencies")
    print("=" * 60)
    
    # π-φ resonance
    pi_phi = k.pi_phi_resonance_frequency()
    assert pi_phi > 0
    print(f"✓ π-φ resonance: {pi_phi:.2f} Hz")
    
    # Planck-Euler resonance
    planck_euler = k.planck_euler_resonance_frequency()
    assert planck_euler > 0
    print(f"✓ Planck-Euler resonance: {planck_euler:.6e} Hz")
    
    # Euclidean π-resonance
    euclidean = k.euclidean_geometry_pi_resonance()
    assert euclidean == 95366637.6
    print(f"✓ Euclidean π-resonance: {euclidean:.1f} Hz")
    
    return True


def test_carfe_recursion():
    """Test CARFE recursion."""
    print("=" * 60)
    print("TEST 6: CARFE Recursion")
    print("=" * 60)
    
    # Test Fibonacci-like sequence
    offbit_0 = 1.0
    offbit_1 = 1.0
    K = 1.0
    
    offbit_2 = k.carfe_recursion(offbit_1, offbit_0, K)
    
    # Should be φ * 1 + 1 * 1 = φ + 1 ≈ 2.618
    expected = k.PHI + 1.0
    assert abs(offbit_2 - expected) < 1e-6
    print(f"✓ CARFE(1, 1, 1) = {offbit_2:.6f} (expected {expected:.6f})")
    
    # Test with custom phi
    offbit_custom = k.carfe_recursion(1.0, 1.0, 1.0, phi=2.0)
    assert offbit_custom == 3.0  # 2*1 + 1*1 = 3
    print(f"✓ Custom φ works: {offbit_custom:.6f}")
    
    return True


def test_coherence_matrix():
    """Test coherence matrix calculation."""
    print("=" * 60)
    print("TEST 7: Coherence Matrix")
    print("=" * 60)
    
    # Create test signals
    signals = [
        [1.0, 2.0, 3.0, 4.0, 5.0],
        [1.0, 2.0, 3.0, 4.0, 5.0],  # Identical to first
        [5.0, 4.0, 3.0, 2.0, 1.0],  # Reverse
    ]
    
    matrix, pairs = k.calculate_signal_coherence_matrix(signals, threshold=0.5)
    
    # Matrix should be 3x3
    assert len(matrix) == 3
    assert len(matrix[0]) == 3
    print(f"✓ Matrix is 3x3")
    
    # Diagonal should be 1.0
    for i in range(3):
        assert abs(matrix[i][i] - 1.0) < 1e-10
    print(f"✓ Diagonal is 1.0")
    
    # Signals 0 and 1 should be highly coherent
    assert matrix[0][1] > 0.9
    print(f"✓ Identical signals coherent: {matrix[0][1]:.6f}")
    
    # Should have observable pairs
    assert len(pairs) > 0
    print(f"✓ Found {len(pairs)} observable pairs")
    
    return True


def test_utility_functions():
    """Test utility functions."""
    print("=" * 60)
    print("TEST 8: Utility Functions")
    print("=" * 60)
    
    # Test toggle rate
    rate = k.calculate_toggle_rate(100, 1.0)
    assert rate == 100.0
    print(f"✓ Toggle rate: {rate:.1f} toggles/s")
    
    # Test coherence pressure mitigation
    mitigated = k.coherence_pressure_mitigation(1.0)
    assert 0 < mitigated < 1.0
    print(f"✓ Coherence pressure mitigation: {mitigated:.6f}")
    
    # Test coherence threshold validation
    assert k.validate_coherence_threshold(0.7) == True
    assert k.validate_coherence_threshold(0.3) == False
    print(f"✓ Coherence threshold validation works")
    
    # Test resonance interaction
    interaction = k.resonance_interaction(1.0, 1e12, 1e-9)
    assert 0 < interaction <= 1.0
    print(f"✓ Resonance interaction: {interaction:.6f}")
    
    return True


def run_all_tests():
    """Run all tests."""
    print("\n" + "=" * 60)
    print("UBP 3.6.2 KERNELS TEST SUITE")
    print("=" * 60 + "\n")
    
    tests = [
        test_resonance_kernel,
        test_coherence,
        test_signal_generation,
        test_frequency_wavelength,
        test_special_resonances,
        test_carfe_recursion,
        test_coherence_matrix,
        test_utility_functions,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"✗ FAILED: {e}")
            failed += 1
        print()
    
    print("=" * 60)
    print(f"RESULTS: {passed}/{len(tests)} tests passed")
    print("=" * 60)
    
    if failed == 0:
        print("✓ ALL TESTS PASSED")
    else:
        print(f"✗ {failed} tests failed")
    
    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    exit(0 if success else 1)
