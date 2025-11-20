"""
Integration test for kernels.py with UBP 3.6.2 system
"""

import kernels as k
from coherence_substrate import CoherenceState
from state import OffBit
import toggle_ops as tops


def test_kernels_with_coherence_substrate():
    """Test kernels integration with coherence_substrate."""
    print("=" * 60)
    print("TEST 1: Kernels + Coherence Substrate")
    print("=" * 60)
    
    # Create coherence states
    state1 = CoherenceState(1000.0)
    state2 = CoherenceState(2000.0)
    
    # Extract NRCI values as signals
    signal1 = [state1.nrci] * 10
    signal2 = [state2.nrci] * 10
    
    # Calculate coherence between states
    coherence = k.normalized_coherence(signal1, signal2)
    print(f"✓ Coherence between states: {coherence:.6f}")
    
    # Test resonance kernel with state frequencies
    resonance = k.resonance_kernel(state1.value * 1e-12)  # Convert to reasonable d
    print(f"✓ Resonance kernel for state: {resonance:.6f}")
    
    return True


def test_kernels_with_offbit():
    """Test kernels integration with OffBit."""
    print("=" * 60)
    print("TEST 2: Kernels + OffBit")
    print("=" * 60)
    
    offbit = OffBit(0x123456)
    
    # Test resonance interaction
    frequency = 1e12  # 1 THz
    time = 1e-9  # 1 ns
    
    interaction = k.resonance_interaction(float(offbit.value), frequency, time)
    print(f"✓ Resonance interaction: {interaction:.6e}")
    
    # Test resonance with OffBit values
    offbit1 = OffBit(0x100)
    offbit2 = OffBit(0x200)
    
    # Calculate resonance between two OffBit values
    distance = abs(float(offbit2.value) - float(offbit1.value))
    resonance = k.resonance_kernel(distance * 1e-6)  # Scale for reasonable d
    print(f"✓ Resonance between OffBits: {resonance:.6f}")
    
    return True


def test_kernels_with_toggle_ops():
    """Test kernels integration with toggle operations."""
    print("=" * 60)
    print("TEST 3: Kernels + Toggle Operations")
    print("=" * 60)
    
    offbit = OffBit(0x123456)
    
    # Perform resonance toggle
    frequency = 1e12
    time = 1.0  # 1 second
    toggled = tops.resonance_toggle(offbit, frequency, time, k=0.0002)
    
    # Calculate coherence between original and toggled
    signal_orig = [float(offbit.value)]
    signal_toggled = [float(toggled.value)]
    
    # Extend signals for coherence calculation
    signal_orig = signal_orig * 10
    signal_toggled = signal_toggled * 10
    
    coherence = k.normalized_coherence(signal_orig, signal_toggled)
    print(f"✓ Coherence after toggle: {coherence:.6f}")
    
    # Test resonance kernel with toggle frequency
    resonance = k.resonance_kernel(1.0 * frequency * 1e-12)
    print(f"✓ Resonance at toggle frequency: {resonance:.6f}")
    
    return True


def test_frequency_conversions_with_realms():
    """Test frequency/wavelength conversions with realm frequencies."""
    print("=" * 60)
    print("TEST 4: Frequency Conversions + Realms")
    print("=" * 60)
    
    # Test with optical realm frequencies (visible light)
    wavelength_red = 700.0  # nm
    wavelength_blue = 400.0  # nm
    
    freq_red = k.calculate_frequency_from_wavelength(wavelength_red)
    freq_blue = k.calculate_frequency_from_wavelength(wavelength_blue)
    
    print(f"✓ Red light: {wavelength_red:.1f} nm = {freq_red:.6e} Hz")
    print(f"✓ Blue light: {wavelength_blue:.1f} nm = {freq_blue:.6e} Hz")
    
    # Test special resonances
    pi_phi = k.pi_phi_resonance_frequency()
    print(f"✓ π-φ resonance: {pi_phi:.2f} Hz")
    
    return True


def test_signal_coherence_with_states():
    """Test signal coherence with multiple coherence states."""
    print("=" * 60)
    print("TEST 5: Signal Coherence + Multiple States")
    print("=" * 60)
    
    # Create sequence of coherence states
    states = [CoherenceState(100.0 * (i + 1)) for i in range(10)]
    
    # Extract NRCI values as signal
    signal = [s.nrci for s in states]
    
    # Generate reference oscillating signal
    ref_signal = k.generate_oscillating_signal(1.0, 0.0, 1.0, 10.0)
    
    # Calculate coherence
    coherence = k.normalized_coherence(signal, ref_signal)
    print(f"✓ Coherence with reference: {coherence:.6f}")
    
    # Test coherence matrix
    signals = [
        [s.nrci for s in states[:5]],
        [s.nrci for s in states[5:]],
        ref_signal[:5]
    ]
    
    matrix, pairs = k.calculate_signal_coherence_matrix(signals)
    print(f"✓ Coherence matrix: {len(matrix)}x{len(matrix[0])}")
    print(f"✓ Observable pairs: {len(pairs)}")
    
    return True


def run_integration_tests():
    """Run all integration tests."""
    print("\n" + "=" * 60)
    print("KERNELS INTEGRATION TEST SUITE")
    print("UBP 3.6.2 System Integration")
    print("=" * 60 + "\n")
    
    tests = [
        test_kernels_with_coherence_substrate,
        test_kernels_with_offbit,
        test_kernels_with_toggle_ops,
        test_frequency_conversions_with_realms,
        test_signal_coherence_with_states,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"✗ FAILED: {e}")
            import traceback
            traceback.print_exc()
            failed += 1
        print()
    
    print("=" * 60)
    print(f"RESULTS: {passed}/{len(tests)} tests passed")
    print("=" * 60)
    
    if failed == 0:
        print("✓ ALL INTEGRATION TESTS PASSED")
    else:
        print(f"✗ {failed} tests failed")
    
    return failed == 0


if __name__ == "__main__":
    success = run_integration_tests()
    exit(0 if success else 1)
