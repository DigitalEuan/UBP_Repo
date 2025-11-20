"""
Test suite for geometric_error_correction.py v3.6.2
Tests both classic features and new Coherence Field ELITE integration.
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from coherence_substrate import CoherenceState, NRCI_TARGET
from state import OffBit
import geometric_error_correction as gec

def test_basic_functionality():
    """Test basic error correction functionality."""
    print("\n" + "="*60)
    print("TEST 1: Basic Functionality")
    print("="*60)
    
    try:
        # Create states
        state1 = CoherenceState(1000.0)
        state2 = CoherenceState(500.0, log_nrci_error=-5.0)
        
        # Analyze coherence
        analysis = gec.analyze_coherence(state1, realm='quantum')
        assert analysis.regime == gec.CoherenceRegime.SUPERCOHERENT
        assert analysis.geometry == gec.LatticeGeometry.DIAMOND
        
        print("✓ CoherenceState creation and analysis")
        
        # Test regime classification
        regime = gec.classify_regime(0.999998)
        assert regime == gec.CoherenceRegime.SUPERCOHERENT
        
        print("✓ Regime classification")
        
        # Test coherence quality
        quality = gec.calculate_coherence_quality(state1)
        assert 'nrci' in quality
        assert 'quality_score' in quality
        
        print("✓ Coherence quality calculation")
        
        return True
    except Exception as e:
        print(f"✗ FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_golay_patterns():
    """Test Golay pattern encoding/decoding."""
    print("\n" + "="*60)
    print("TEST 2: Golay Patterns")
    print("="*60)
    
    try:
        golay = gec.GolayPattern()
        state = CoherenceState(1000.0)
        
        # Encode
        encoded = golay.encode_state(state)
        assert encoded.nrci >= state.nrci * 0.99  # Should maintain coherence
        
        print("✓ Golay encoding")
        
        # Decode
        decoded, deviations = golay.decode_state(encoded)
        assert decoded.nrci >= state.nrci * 0.99
        
        print("✓ Golay decoding")
        print(f"  Deviations: {deviations}")
        
        return True
    except Exception as e:
        print(f"✗ FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_temporal_tracking():
    """Test temporal coherence tracking."""
    print("\n" + "="*60)
    print("TEST 3: Temporal Coherence Tracking")
    print("="*60)
    
    try:
        tracker = gec.TemporalCoherenceTracker()
        
        # Add states
        for i in range(20):
            state = CoherenceState(100.0 * (i + 1), log_nrci_error=-10.0 + i * 0.2)
            tracker.add_state(state)
        
        print(f"✓ Added {len(tracker.history)} states")
        
        # Compute temporal coherence
        temporal_state = tracker.compute_temporal_coherence()
        assert temporal_state.nrci > 0
        
        print(f"✓ Temporal coherence: {temporal_state.nrci:.10f}")
        
        # Get stability
        stability = tracker.get_regime_stability()
        assert 'stability_ratio' in stability
        
        print(f"✓ Stability ratio: {stability['stability_ratio']:.4f}")
        
        # Get trend
        trend = tracker.get_coherence_trend()
        assert trend in ['improving', 'degrading', 'stable', 'insufficient_data']
        
        print(f"✓ Coherence trend: {trend}")
        
        return True
    except Exception as e:
        print(f"✗ FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_resonance_detection():
    """Test resonance detection in error patterns (NEW in 3.6.2)."""
    print("\n" + "="*60)
    print("TEST 4: Resonance Detection (NEW in 3.6.2)")
    print("="*60)
    
    try:
        tracker = gec.TemporalCoherenceTracker()
        
        # Add states with potential resonance pattern
        for i in range(30):
            state = CoherenceState(100.0 * (i + 1), log_nrci_error=-10.0 + i * 0.1)
            tracker.add_state(state)
        
        # Detect resonances
        resonance = tracker.detect_error_resonances()
        
        print(f"✓ Resonance detection executed")
        if resonance:
            print(f"  Detected: {resonance.p}/{resonance.q} (confidence: {resonance.confidence:.1%})")
        else:
            print(f"  No strong resonance detected")
        
        return True
    except Exception as e:
        print(f"✗ FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_decoherence_detection():
    """Test decoherence point detection (NEW in 3.6.2)."""
    print("\n" + "="*60)
    print("TEST 5: Decoherence Detection (NEW in 3.6.2)")
    print("="*60)
    
    try:
        tracker = gec.TemporalCoherenceTracker()
        
        # Add states with decoherence events
        for i in range(20):
            if i == 10:
                # Inject decoherence
                state = CoherenceState(100.0, log_nrci_error=-5.0)
            else:
                state = CoherenceState(100.0 * (i + 1), log_nrci_error=-15.0)
            tracker.add_state(state)
        
        # Detect decoherence points
        decoherence_points = tracker.detect_decoherence_points(threshold=0.95)
        
        print(f"✓ Decoherence detection executed")
        print(f"  Decoherence points found: {len(decoherence_points)}")
        if decoherence_points:
            print(f"  Indices: {decoherence_points}")
        
        return True
    except Exception as e:
        print(f"✗ FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_resonance_aware_correction():
    """Test resonance-aware error correction (NEW in 3.6.2)."""
    print("\n" + "="*60)
    print("TEST 6: Resonance-Aware Correction (NEW in 3.6.2)")
    print("="*60)
    
    try:
        offbit = OffBit(0x123456)
        
        # Perform resonance-aware correction
        result = gec.correct_with_resonance_awareness(
            offbit,
            frequency=1e12,
            steps=30,
            k=0.0002
        )
        
        print(f"✓ Resonance-aware correction executed")
        print(f"  Corrections applied: {result['corrections_applied']}")
        print(f"  Final NRCI: {result['final_nrci']:.10f}")
        print(f"  Coherence trend: {result['coherence_trend']}")
        print(f"  Decoherence points: {len(result['decoherence_points'])}")
        
        # Verify result structure
        assert 'final_offbit' in result
        assert 'corrections_applied' in result
        assert 'coherence_trend' in result
        
        print("✓ Result structure verified")
        
        return True
    except Exception as e:
        print(f"✗ FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_error_pattern_analysis():
    """Test error pattern analysis (NEW in 3.6.2)."""
    print("\n" + "="*60)
    print("TEST 7: Error Pattern Analysis (NEW in 3.6.2)")
    print("="*60)
    
    try:
        # Create test states
        states = [CoherenceState(100.0 * (i + 1), log_nrci_error=-10.0 + i * 0.3) 
                  for i in range(20)]
        
        # Analyze error patterns
        analysis = gec.analyze_error_patterns(states, detect_resonances=True)
        
        print(f"✓ Error pattern analysis executed")
        print(f"  Error rate: {analysis['error_rate']:.4f}")
        print(f"  Regime transitions: {analysis['regime_transitions']}")
        print(f"  Decoherence events: {analysis['decoherence_count']}")
        print(f"  Resonance detected: {analysis['resonance_detected']}")
        print(f"  Avg NRCI: {analysis['avg_nrci']:.10f}")
        
        # Verify result structure
        assert 'error_rate' in analysis
        assert 'resonance_detected' in analysis
        assert 'decoherence_count' in analysis
        
        print("✓ Result structure verified")
        
        return True
    except Exception as e:
        print(f"✗ FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_global_coherence_management():
    """Test global coherence management."""
    print("\n" + "="*60)
    print("TEST 8: Global Coherence Management")
    print("="*60)
    
    try:
        manager = gec.GlobalCoherenceManager()
        
        # Register states
        state1 = CoherenceState(1000.0)
        state2 = CoherenceState(500.0, log_nrci_error=-5.0)
        manager.register_state("system1", state1)
        manager.register_state("system2", state2)
        
        print(f"✓ Registered {len(manager.states)} states")
        
        # Get global coherence
        global_state = manager.get_global_coherence()
        assert global_state.nrci > 0
        
        print(f"✓ Global NRCI: {global_state.nrci:.10f}")
        
        # Get system health
        health = manager.get_system_health()
        assert 'global_nrci' in health
        assert 'state_count' in health
        
        print(f"✓ System health: {health['global_regime']}")
        
        return True
    except Exception as e:
        print(f"✗ FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False


def run_all_tests():
    """Run all tests."""
    print("="*60)
    print("GEOMETRIC ERROR CORRECTION TEST SUITE")
    print("UBP 3.6.2 - Coherence Field ELITE Integration")
    print("="*60)
    
    tests = [
        test_basic_functionality,
        test_golay_patterns,
        test_temporal_tracking,
        test_resonance_detection,
        test_decoherence_detection,
        test_resonance_aware_correction,
        test_error_pattern_analysis,
        test_global_coherence_management
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        if test():
            passed += 1
        else:
            failed += 1
    
    print("\n" + "="*60)
    print(f"RESULTS: {passed}/{passed+failed} tests passed")
    print("="*60)
    
    if failed == 0:
        print("\n✓ ALL TESTS PASSED")
    else:
        print(f"\n✗ {failed} tests failed")
    
    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
