"""
================================================================================
Test Suite for Resonance History Tracking
================================================================================

Tests the integration between toggle_ops.py resonance tracking and
Coherence Field ELITE's resonance detector.

Author: Euan R A Craig, New Zealand
Date: November 20, 2025
"""

import sys
import os

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


def test_basic_resonance_tracking():
    """Test basic resonance history tracking."""
    print("\n" + "=" * 80)
    print("TEST 1: Basic Resonance History Tracking")
    print("=" * 80)
    
    # Create OffBit
    b = OffBit(0x123456)
    print(f"Initial OffBit: {b}")
    print(f"Initial history length: {b.resonance_history_length}")
    
    # Apply resonance toggles
    for t in range(10):
        b = to.resonance_toggle(b, frequency=1e9, time=t * 1e-9)
    
    print(f"\nAfter 10 resonance toggles:")
    print(f"History length: {b.resonance_history_length}")
    print(f"Final NRCI: {b.nrci:.10f}")
    
    # Get statistics
    stats = b.get_resonance_statistics()
    print(f"\nResonance Statistics:")
    print(f"  Time range: {stats['time_range']}")
    print(f"  Frequency range: {stats['frequency_range']}")
    print(f"  Avg resonance factor: {stats['avg_resonance_factor']:.6f}")
    print(f"  Min resonance factor: {stats['min_resonance_factor']:.6f}")
    print(f"  Max resonance factor: {stats['max_resonance_factor']:.6f}")
    
    # Verify history
    assert b.resonance_history_length == 10, "History length should be 10"
    assert b.has_resonance_history, "Should have resonance history"
    assert stats['history_length'] == 10, "Stats should show 10 entries"
    
    print("\n✓ Basic resonance tracking working correctly")
    return True


def test_history_limit():
    """Test that history respects max_history limit."""
    print("\n" + "=" * 80)
    print("TEST 2: History Limit Enforcement")
    print("=" * 80)
    
    # Create OffBit
    b = OffBit(0x100000)
    
    # Apply 150 resonance toggles with max_history=100
    for t in range(150):
        b = to.resonance_toggle(b, frequency=1e9, time=t * 1e-9, max_history=100)
    
    print(f"After 150 toggles with max_history=100:")
    print(f"History length: {b.resonance_history_length}")
    
    # Verify limit
    assert b.resonance_history_length == 100, "History should be limited to 100"
    
    # Verify we kept the most recent entries
    last_time = b.resonance_history[-1][0]
    print(f"Last time in history: {last_time:.9f}s")
    assert last_time == 149 * 1e-9, "Should keep most recent entries"
    
    print("\n✓ History limit working correctly")
    return True


def test_history_to_states_conversion():
    """Test conversion of history to CoherenceState sequence."""
    print("\n" + "=" * 80)
    print("TEST 3: History to CoherenceState Conversion")
    print("=" * 80)
    
    # Create OffBit with resonance history
    b = OffBit(0x123456)
    for t in range(50):
        b = to.resonance_toggle(b, frequency=1e9, time=t * 1e-9)
    
    print(f"Created OffBit with {b.resonance_history_length} history entries")
    
    # Convert to states
    states = to.resonance_history_to_states(b)
    
    print(f"Converted to {len(states)} CoherenceState objects")
    print(f"First state: value={states[0].value:.6f}, NRCI={states[0].nrci:.10f}")
    print(f"Last state: value={states[-1].value:.6f}, NRCI={states[-1].nrci:.10f}")
    
    # Verify conversion
    assert len(states) == b.resonance_history_length, "Should have same number of states"
    assert all(hasattr(s, 'nrci') for s in states), "All should be CoherenceState objects"
    
    print("\n✓ Conversion working correctly")
    return True


def test_coherence_field_integration():
    """Test integration with Coherence Field ELITE."""
    print("\n" + "=" * 80)
    print("TEST 4: Coherence Field ELITE Integration")
    print("=" * 80)
    
    if not COHERENCE_FIELD_AVAILABLE:
        print("⊘ Skipped - coherence_field.py not available")
        return True
    
    # Create OffBit with clear resonance pattern
    b = OffBit(0x123456)
    
    # Apply resonance toggles with 4π/3 pattern
    import math
    for t in range(100):
        # Create 2/3 resonance pattern
        phase = t * (4 * math.pi / 3) / 100
        b = to.resonance_toggle(b, frequency=1e9, time=phase)
    
    print(f"Created OffBit with {b.resonance_history_length} history entries")
    
    # Analyze with Coherence Field ELITE
    analysis = to.analyze_resonance_history(b)
    
    print(f"\nCoherence Field Analysis:")
    print(f"  Coherence Field available: {analysis.get('coherence_field_available', False)}")
    print(f"  History length: {analysis['history_length']}")
    print(f"  Avg resonance factor: {analysis['avg_resonance_factor']:.6f}")
    
    if analysis.get('resonance_detected'):
        res = analysis['resonance']
        print(f"\n  Resonance detected: {res.p}/{res.q}")
        print(f"  Confidence: {res.confidence:.1%}")
        print(f"  Frequency: {res.frequency:.6f}")
        print(f"  Error: {res.error:.6f}")
    else:
        print(f"\n  No resonance detected")
    
    # Verify analysis
    assert 'history_length' in analysis, "Should have history length"
    assert 'avg_resonance_factor' in analysis, "Should have avg resonance factor"
    
    print("\n✓ Coherence Field integration working")
    return True


def test_parameter_optimization():
    """Test resonance parameter optimization."""
    print("\n" + "=" * 80)
    print("TEST 5: Resonance Parameter Optimization")
    print("=" * 80)
    
    # Create OffBit
    b = OffBit(0x100000)
    
    # Optimize k for target frequency
    print("Optimizing k parameter for frequency=1e9 Hz...")
    result = to.optimize_resonance_parameters(b, target_frequency=1e9, time_steps=50)
    
    print(f"\nOptimization Results:")
    print(f"  Optimal k: {result['optimal_k']}")
    print(f"  Optimal NRCI: {result['optimal_nrci']:.10f}")
    print(f"  Optimal avg resonance: {result['optimal_avg_resonance']:.6f}")
    print(f"  Target frequency: {result['target_frequency']:.2e} Hz")
    
    print(f"\nAll tested k values:")
    for r in result['all_results']:
        print(f"    k={r['k']:.4f}: NRCI={r['final_nrci']:.10f}, "
              f"avg_resonance={r['avg_resonance_factor']:.6f}")
    
    # Verify optimization
    assert 'optimal_k' in result, "Should have optimal k"
    assert 'optimal_nrci' in result, "Should have optimal NRCI"
    assert len(result['all_results']) > 0, "Should have tested multiple k values"
    
    print("\n✓ Parameter optimization working")
    return True


def test_visualization():
    """Test text-based visualization."""
    print("\n" + "=" * 80)
    print("TEST 6: Resonance History Visualization")
    print("=" * 80)
    
    # Create OffBit with varying resonance
    b = OffBit(0x123456)
    
    # Apply resonance toggles with varying k
    import math
    for t in range(60):
        # Vary k to create interesting pattern
        k = 0.0002 + 0.0001 * math.sin(t * 0.1)
        b = to.resonance_toggle(b, frequency=1e9, time=t * 1e-9, k=k)
    
    # Visualize
    viz = to.visualize_resonance_history(b, width=70)
    print(viz)
    
    # Verify visualization
    assert "RESONANCE HISTORY VISUALIZATION" in viz, "Should have title"
    assert "History length:" in viz, "Should show history length"
    assert "█" in viz or len(b.resonance_history) == 0, "Should have bars (if history exists)"
    
    print("\n✓ Visualization working")
    return True


def test_immutability():
    """Test that OffBit immutability is preserved."""
    print("\n" + "=" * 80)
    print("TEST 7: OffBit Immutability with History")
    print("=" * 80)
    
    # Create OffBit
    b1 = OffBit(0x123456)
    print(f"Original: {b1}")
    print(f"Original history length: {b1.resonance_history_length}")
    
    # Apply resonance toggle
    b2 = to.resonance_toggle(b1, frequency=1e9, time=1e-9)
    print(f"\nAfter toggle:")
    print(f"  Original history length: {b1.resonance_history_length}")
    print(f"  New history length: {b2.resonance_history_length}")
    
    # Verify immutability
    assert b1.resonance_history_length == 0, "Original should be unchanged"
    assert b2.resonance_history_length == 1, "New should have history"
    assert b1.value == 0x123456, "Original value unchanged"
    
    print("\n✓ Immutability preserved")
    return True


def test_empty_history():
    """Test handling of empty history."""
    print("\n" + "=" * 80)
    print("TEST 8: Empty History Handling")
    print("=" * 80)
    
    # Create OffBit with no history
    b = OffBit(0x123456)
    
    print(f"OffBit with no history:")
    print(f"  Has history: {b.has_resonance_history}")
    print(f"  History length: {b.resonance_history_length}")
    
    # Get statistics
    stats = b.get_resonance_statistics()
    print(f"\nStatistics for empty history:")
    print(f"  {stats}")
    
    # Convert to states
    states = to.resonance_history_to_states(b)
    print(f"\nStates from empty history: {len(states)}")
    
    # Analyze
    analysis = to.analyze_resonance_history(b)
    print(f"\nAnalysis of empty history:")
    print(f"  {analysis}")
    
    # Verify handling
    assert not b.has_resonance_history, "Should not have history"
    assert b.resonance_history_length == 0, "Length should be 0"
    assert stats['history_length'] == 0, "Stats should show 0"
    assert len(states) == 0, "Should have no states"
    
    print("\n✓ Empty history handled correctly")
    return True


# ============================================================================
# RUN ALL TESTS
# ============================================================================

def run_all_tests():
    """Run all tests."""
    print("=" * 80)
    print("RESONANCE HISTORY TRACKING TEST SUITE")
    print("=" * 80)
    print(f"Coherence Field ELITE available: {COHERENCE_FIELD_AVAILABLE}")
    
    tests = [
        test_basic_resonance_tracking,
        test_history_limit,
        test_history_to_states_conversion,
        test_coherence_field_integration,
        test_parameter_optimization,
        test_visualization,
        test_immutability,
        test_empty_history
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
