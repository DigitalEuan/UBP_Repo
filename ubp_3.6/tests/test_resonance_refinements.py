"""
================================================================================
Test Suite for Resonance History Refinements
================================================================================

Tests the refined resonance history features:
- add_resonance_record() method
- detect_perception_reset_points() method
- get_coherence_valleys() method
- to_coherence_states() method
- analyze_with_coherence_field() method

Author: Euan R A Craig, New Zealand
Date: November 20, 2025
"""

import sys
import os
import math

# Add ubp_3.6 to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from state import OffBit
import toggle_ops as to

# Try to import coherence_field
try:
    import coherence_field as cf
    COHERENCE_FIELD_AVAILABLE = True
except ImportError:
    COHERENCE_FIELD_AVAILABLE = False
    print("Warning: coherence_field.py not available - some tests will be skipped")


def test_add_resonance_record():
    """Test add_resonance_record method."""
    print("\n" + "=" * 80)
    print("TEST 1: add_resonance_record() Method")
    print("=" * 80)
    
    # Create OffBit
    b = OffBit(0x123456)
    print(f"Initial: {b}")
    print(f"Initial history length: {b.resonance_history_length}")
    
    # Add records manually
    b = b.add_resonance_record(1e-9, 1e9, 0.999)
    b = b.add_resonance_record(2e-9, 1e9, 0.998)
    b = b.add_resonance_record(3e-9, 1e9, 0.997)
    
    print(f"\nAfter adding 3 records:")
    print(f"History length: {b.resonance_history_length}")
    
    # Verify
    assert b.resonance_history_length == 3, "Should have 3 records"
    assert b.resonance_history[0] == (1e-9, 1e9, 0.999), "First record correct"
    assert b.resonance_history[2] == (3e-9, 1e9, 0.997), "Last record correct"
    
    print("\n✓ add_resonance_record() working correctly")
    return True


def test_add_resonance_record_size_limit():
    """Test add_resonance_record with size limit."""
    print("\n" + "=" * 80)
    print("TEST 2: add_resonance_record() Size Limit")
    print("=" * 80)
    
    # Create OffBit
    b = OffBit(0x100000)
    
    # Add 15 records with max_history=10
    for i in range(15):
        b = b.add_resonance_record(i * 1e-9, 1e9, 0.99, max_history=10)
    
    print(f"After adding 15 records with max_history=10:")
    print(f"History length: {b.resonance_history_length}")
    
    # Verify limit
    assert b.resonance_history_length == 10, "Should be limited to 10"
    
    # Verify we kept most recent
    assert abs(b.resonance_history[0][0] - 5e-9) < 1e-15, "Should start at record 5"
    assert abs(b.resonance_history[-1][0] - 14e-9) < 1e-15, "Should end at record 14"
    
    print("\n✓ Size limit working correctly")
    return True


def test_detect_perception_reset_points():
    """Test detect_perception_reset_points method."""
    print("\n" + "=" * 80)
    print("TEST 3: detect_perception_reset_points() Method")
    print("=" * 80)
    
    # Create OffBit with varying resonance factors
    b = OffBit(0x123456)
    
    # Add records with some below threshold
    factors = [0.99, 0.98, 0.92, 0.95, 0.88, 0.97, 0.99, 0.91, 0.96]
    for i, factor in enumerate(factors):
        b = b.add_resonance_record(i * 1e-9, 1e9, factor)
    
    print(f"Created history with {b.resonance_history_length} records")
    print(f"Factors: {factors}")
    
    # Detect reset points (threshold 0.95)
    reset_points = b.detect_perception_reset_points(threshold=0.95)
    
    print(f"\nReset points (threshold=0.95): {reset_points}")
    print(f"Number of reset points: {len(reset_points)}")
    
    # Verify
    expected = [2, 4, 7]  # Indices where factor < 0.95
    assert reset_points == expected, f"Expected {expected}, got {reset_points}"
    
    # Check actual values
    for idx in reset_points:
        time, freq, factor = b.resonance_history[idx]
        print(f"  Reset at index {idx}: t={time:.9f}s, factor={factor:.2f}")
        assert factor < 0.95, "All reset points should be below threshold"
    
    print("\n✓ detect_perception_reset_points() working correctly")
    return True


def test_get_coherence_valleys():
    """Test get_coherence_valleys method."""
    print("\n" + "=" * 80)
    print("TEST 4: get_coherence_valleys() Method")
    print("=" * 80)
    
    # Create OffBit with valley pattern
    b = OffBit(0x123456)
    
    # Create pattern with valleys: high, low, high, low, high
    factors = [0.99, 0.98, 0.97, 0.92, 0.95, 0.96, 0.97, 0.88, 0.93, 0.95, 0.96]
    for i, factor in enumerate(factors):
        b = b.add_resonance_record(i * 1e-9, 1e9, factor)
    
    print(f"Created history with {b.resonance_history_length} records")
    print(f"Factors: {factors}")
    
    # Find valleys
    valleys = b.get_coherence_valleys(window_size=3)
    
    print(f"\nCoherence valleys (window_size=3):")
    for idx, factor in valleys:
        time, freq, _ = b.resonance_history[idx]
        print(f"  Valley at index {idx}: t={time:.9f}s, factor={factor:.2f}")
    
    # Verify valleys are local minima
    assert len(valleys) > 0, "Should find at least one valley"
    
    for idx, factor in valleys:
        # Check it's actually a local minimum
        if idx > 0 and idx < len(factors) - 1:
            assert factor <= factors[idx - 1], "Should be <= left neighbor"
            assert factor <= factors[idx + 1], "Should be <= right neighbor"
    
    print(f"\n✓ get_coherence_valleys() working correctly (found {len(valleys)} valleys)")
    return True


def test_to_coherence_states():
    """Test to_coherence_states method."""
    print("\n" + "=" * 80)
    print("TEST 5: to_coherence_states() Method")
    print("=" * 80)
    
    # Create OffBit with history
    b = OffBit(0x123456)
    for i in range(20):
        b = b.add_resonance_record(i * 1e-9, 1e9, 0.99 - i * 0.001)
    
    print(f"Created history with {b.resonance_history_length} records")
    
    # Convert to states
    states = b.to_coherence_states()
    
    print(f"Converted to {len(states)} CoherenceState objects")
    print(f"First state: value={states[0].value:.6f}, NRCI={states[0].nrci:.10f}")
    print(f"Last state: value={states[-1].value:.6f}, NRCI={states[-1].nrci:.10f}")
    
    # Verify
    assert len(states) == b.resonance_history_length, "Should have same length"
    assert all(hasattr(s, 'nrci') for s in states), "All should be CoherenceState"
    
    # Verify NRCI decreases as resonance_factor decreases
    nrcis = [s.nrci for s in states]
    print(f"\nNRCI trend: {nrcis[0]:.10f} -> {nrcis[-1]:.10f}")
    assert nrcis[0] > nrcis[-1], "NRCI should decrease as resonance factor decreases"
    
    print("\n✓ to_coherence_states() working correctly")
    return True


def test_analyze_with_coherence_field():
    """Test analyze_with_coherence_field method."""
    print("\n" + "=" * 80)
    print("TEST 6: analyze_with_coherence_field() Method")
    print("=" * 80)
    
    if not COHERENCE_FIELD_AVAILABLE:
        print("⊘ Skipped - coherence_field.py not available")
        return True
    
    # Create OffBit with resonance pattern
    b = OffBit(0x123456)
    
    # Create 4π/3 pattern
    for t in range(100):
        phase = t * (4 * math.pi / 3) / 100
        b = b.add_resonance_record(phase, 1e9, 0.99 - t * 0.0001)
    
    print(f"Created history with {b.resonance_history_length} records")
    
    # Analyze
    analysis = b.analyze_with_coherence_field()
    
    print(f"\nAnalysis results:")
    print(f"  History length: {analysis['history_length']}")
    print(f"  Avg resonance factor: {analysis['avg_resonance_factor']:.6f}")
    print(f"  Resonance detected: {analysis.get('resonance_detected', False)}")
    
    if analysis.get('resonance_detected'):
        print(f"  Resonance: {analysis['resonance_p']}/{analysis['resonance_q']}")
        print(f"  Confidence: {analysis['resonance_confidence']:.1%}")
    
    # Verify structure
    assert 'history_length' in analysis, "Should have history_length"
    assert 'avg_resonance_factor' in analysis, "Should have avg_resonance_factor"
    assert 'coherence_states' in analysis, "Should have coherence_states"
    
    print("\n✓ analyze_with_coherence_field() working correctly")
    return True


def test_integration_with_resonance_toggle():
    """Test that new methods work with resonance_toggle."""
    print("\n" + "=" * 80)
    print("TEST 7: Integration with resonance_toggle()")
    print("=" * 80)
    
    # Use resonance_toggle (which uses internal tracking)
    b = OffBit(0x123456)
    for t in range(50):
        b = to.resonance_toggle(b, frequency=1e9, time=t * 1e-9)
    
    print(f"After 50 resonance_toggle calls:")
    print(f"History length: {b.resonance_history_length}")
    
    # Now use new methods
    reset_points = b.detect_perception_reset_points(threshold=0.95)
    print(f"Reset points: {len(reset_points)}")
    
    valleys = b.get_coherence_valleys(window_size=5)
    print(f"Coherence valleys: {len(valleys)}")
    
    states = b.to_coherence_states()
    print(f"Coherence states: {len(states)}")
    
    # Verify all work
    assert b.resonance_history_length == 50, "Should have 50 records"
    assert len(states) == 50, "Should have 50 states"
    
    print("\n✓ Integration working correctly")
    return True


def test_empty_history_handling():
    """Test that new methods handle empty history gracefully."""
    print("\n" + "=" * 80)
    print("TEST 8: Empty History Handling")
    print("=" * 80)
    
    # Create OffBit with no history
    b = OffBit(0x123456)
    
    print(f"OffBit with no history:")
    print(f"  History length: {b.resonance_history_length}")
    
    # Test all new methods
    reset_points = b.detect_perception_reset_points()
    print(f"  Reset points: {reset_points}")
    
    valleys = b.get_coherence_valleys()
    print(f"  Valleys: {valleys}")
    
    states = b.to_coherence_states()
    print(f"  States: {len(states)}")
    
    analysis = b.analyze_with_coherence_field()
    print(f"  Analysis: {analysis}")
    
    # Verify all return empty/appropriate values
    assert reset_points == [], "Should return empty list"
    assert valleys == [], "Should return empty list"
    assert states == [], "Should return empty list"
    assert analysis is not None, "Should return dict"
    
    print("\n✓ Empty history handled correctly")
    return True


# ============================================================================
# RUN ALL TESTS
# ============================================================================

def run_all_tests():
    """Run all tests."""
    print("=" * 80)
    print("RESONANCE HISTORY REFINEMENTS TEST SUITE")
    print("=" * 80)
    print(f"Coherence Field ELITE available: {COHERENCE_FIELD_AVAILABLE}")
    
    tests = [
        test_add_resonance_record,
        test_add_resonance_record_size_limit,
        test_detect_perception_reset_points,
        test_get_coherence_valleys,
        test_to_coherence_states,
        test_analyze_with_coherence_field,
        test_integration_with_resonance_toggle,
        test_empty_history_handling
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"\n✗ Test failed: {e}")
            import traceback
            traceback.print_exc()
            failed += 1
    
    print("\n" + "=" * 80)
    print("TEST SUMMARY")
    print("=" * 80)
    print(f"Total: {passed + failed} tests")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    print(f"Pass rate: {passed / (passed + failed) * 100:.1f}%")
    
    if failed == 0:
        print("\n✓ ALL TESTS PASSED")
    else:
        print(f"\n✗ {failed} TESTS FAILED")
    
    print("=" * 80)
    
    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
