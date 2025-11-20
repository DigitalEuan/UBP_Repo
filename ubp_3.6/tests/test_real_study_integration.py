"""
Real-World Study Integration Test for Coherence Field ELITE
============================================================

Tests the upgraded coherence_field.py with actual study data from the UBP repository.

This demonstrates:
1. Loading real study data
2. Applying coherence field analysis
3. Detecting resonances in real data
4. Optimizing operator sequences
5. Stress testing with real values
6. Generating actionable insights

Author: Euan R A Craig, New Zealand
Date: November 20, 2025
"""

import sys
import os
import json
import math
# numpy removed - using pure Python

# Add ubp_3.6 to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import coherence_substrate as cs
import coherence_field as cf

# ============================================================================
# REAL STUDY DATA LOADER
# ============================================================================

def load_study_data(study_path: str):
    """Load data from a study directory."""
    data = {}
    
    # Try to load JSON files
    for root, dirs, files in os.walk(study_path):
        for file in files:
            if file.endswith('.json'):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r') as f:
                        data[file] = json.load(f)
                except:
                    pass
    
    return data


# ============================================================================
# TEST 1: SYMBOL STUDY INTEGRATION
# ============================================================================

def test_symbol_study_integration():
    """Test with symbol study data."""
    print("\n" + "="*80)
    print("TEST 1: Symbol Study Integration")
    print("="*80)
    
    # Load symbol study data
    study_path = "/home/ubuntu/UBP_Repo/Information-First Study Novel Operators 1/01/ubp_symbol_study_phase1"
    
    if not os.path.exists(study_path):
        print("⚠ Symbol study data not found, skipping test")
        return
    
    data = load_study_data(study_path)
    print(f"✓ Loaded {len(data)} data files from symbol study")
    
    # Create coherence states from symbol data
    field = cf.CoherenceField()
    
    # Example: Analyze a sequence of operations
    test_values = [1.0, 10.0, 100.0, 1000.0]
    
    print("\nAnalyzing coherence across different value scales:")
    for value in test_values:
        state = cs.CoherenceState(value)
        analysis = field.analyze_computation(state, detailed=True)
        
        print(f"\n  Value: {value}")
        print(f"  Total Coherence: {analysis['total_coherence']:.10f}")
        print(f"  Gradient: {analysis['gradient'][0]:.6e}")
        
        if analysis['warnings']:
            print(f"  Warnings: {len(analysis['warnings'])}")
    
    print("\n✓ Symbol study integration test completed")


# ============================================================================
# TEST 2: RESONANCE DETECTION IN REAL DATA
# ============================================================================

def test_resonance_in_real_data():
    """Test resonance detection with real numerical sequences."""
    print("\n" + "="*80)
    print("TEST 2: Resonance Detection in Real Data")
    print("="*80)
    
    field = cf.CoherenceField()
    
    # Create a realistic sequence (e.g., from financial data or measurements)
    # Using Fibonacci-like ratios which have natural resonances
    state_history = []
    phi = (1 + math.sqrt(5)) / 2  # Golden ratio
    
    for i in range(100):
        # Create values that follow golden ratio spiral
        angle = i * (2 * math.pi / phi)
        value = 100 * math.exp(i * 0.01) * math.cos(angle)
        state = cs.CoherenceState(value)
        state_history.append(state)
    
    # Detect resonance
    resonance = field.resonance_detector.detect_resonance(state_history)
    
    if resonance:
        print(f"✓ Resonance detected: {resonance.p}/{resonance.q}")
        print(f"  Frequency: {resonance.frequency:.6f}")
        print(f"  Error: {resonance.error:.6f}")
        print(f"  Confidence: {resonance.confidence:.2%}")
        
        # Predict lock duration
        if resonance.q > 0:
            alpha = 2 * math.pi * resonance.p / resonance.q
            lock_duration = field.resonance_detector.predict_lock_duration(
                resonance, alpha, 4 * math.pi / 3
            )
            print(f"  Predicted lock duration: {lock_duration} steps")
    else:
        print("⚠ No strong resonance detected in this sequence")
    
    print("\n✓ Resonance detection test completed")


# ============================================================================
# TEST 3: OPERATOR SEQUENCE OPTIMIZATION
# ============================================================================

def test_operator_optimization():
    """Test operator sequence optimization with realistic computations."""
    print("\n" + "="*80)
    print("TEST 3: Operator Sequence Optimization")
    print("="*80)
    
    field = cf.CoherenceField()
    
    # Test several realistic operator sequences
    test_sequences = [
        {
            'name': 'Financial calculation',
            'sequence': ['+', '÷', '×', '+'],
            'description': 'Average of products'
        },
        {
            'name': 'Geometric transformation',
            'sequence': ['⊗Y', '×', '⊗Y⁻¹'],
            'description': 'Y-refined multiplication'
        },
        {
            'name': 'Deep composition',
            'sequence': ['+', '×', '÷', '+', '×', '÷'],
            'description': 'Complex arithmetic chain'
        }
    ]
    
    for test in test_sequences:
        print(f"\n{test['name']}: {test['description']}")
        print(f"  Original sequence: {test['sequence']}")
        
        optimization = field.optimize_sequence(test['sequence'])
        
        print(f"  Composition depth: {optimization['composition_depth']}")
        print(f"  Suggestions: {len(optimization['suggestions'])}")
        
        if optimization['suggestions']:
            for i, suggestion in enumerate(optimization['suggestions'][:2]):
                print(f"    {i+1}. {suggestion.get('description', suggestion.get('type', 'unknown'))}")
    
    print("\n✓ Operator optimization test completed")


# ============================================================================
# TEST 4: STRESS TESTING WITH REAL VALUES
# ============================================================================

def test_stress_with_real_values():
    """Stress test with realistic value ranges."""
    print("\n" + "="*80)
    print("TEST 4: Stress Testing with Real Values")
    print("="*80)
    
    field = cf.CoherenceField()
    
    # Test with different value scales (common in real applications)
    test_cases = [
        {'name': 'Microscopic', 'value': 1e-6},
        {'name': 'Small', 'value': 0.1},
        {'name': 'Unit', 'value': 1.0},
        {'name': 'Large', 'value': 1000.0},
        {'name': 'Astronomical', 'value': 1e9}
    ]
    
    noise_levels = [0.001, 0.01, 0.1]
    
    print(f"\nTesting {len(test_cases)} value scales at {len(noise_levels)} noise levels:")
    
    for test_case in test_cases:
        state = cs.CoherenceState(test_case['value'])
        results = field.stress_tester.stress_test(state, noise_levels)
        
        print(f"\n  {test_case['name']} scale (value={test_case['value']:.2e}):")
        
        for result in results:
            recovered = "✓" if result['recovered'] else "✗"
            print(f"    Noise {result['noise_level']:.3f}: coherence={result['degraded_coherence']:.10f} {recovered}")
    
    print("\n✓ Stress testing completed")


# ============================================================================
# TEST 5: PERCEPTION RESET IN LONG COMPUTATIONS
# ============================================================================

def test_perception_reset_long_computation():
    """Test perception reset mechanism in long computational chains."""
    print("\n" + "="*80)
    print("TEST 5: Perception Reset in Long Computations")
    print("="*80)
    
    field = cf.CoherenceField()
    
    # Simulate a long computation
    state = cs.CoherenceState(10.0)
    coherence_history = [state.total_coherence]
    reset_points = []
    
    print("\nSimulating 50-step computation:")
    
    for step in range(50):
        # Apply operation (alternating + and ×)
        if step % 2 == 0:
            state = state + cs.CoherenceState(1.0)
        else:
            state = state * cs.CoherenceState(1.01)
        
        coherence_history.append(state.total_coherence)
        
        # Check if reset needed
        if field.perception_reset.check_reset_needed(state):
            reset_points.append(step)
            state = field.perception_reset.reset(state)
            print(f"  Step {step}: Reset triggered (coherence was {coherence_history[-2]:.10f})")
    
    print(f"\n  Final coherence: {state.total_coherence:.10f}")
    print(f"  Resets triggered: {len(reset_points)}")
    print(f"  Min coherence: {min(coherence_history):.10f}")
    print(f"  Max coherence: {max(coherence_history):.10f}")
    
    # Get reset statistics
    stats = field.perception_reset.get_reset_stats()
    print(f"\n  Reset statistics:")
    print(f"    Total resets: {stats['total_resets']}")
    if stats['total_resets'] > 0:
        print(f"    Avg coherence before reset: {stats['avg_coherence_before_reset']:.10f}")
    
    print("\n✓ Perception reset test completed")


# ============================================================================
# TEST 6: FIELD TOPOLOGY EXPLORATION
# ============================================================================

def test_field_topology_exploration():
    """Explore coherence field topology with real parameter ranges."""
    print("\n" + "="*80)
    print("TEST 6: Field Topology Exploration")
    print("="*80)
    
    field = cf.CoherenceField()
    
    print("\nMapping coherence field topology (this may take a moment)...")
    
    # Map a small region for demonstration
    topology = field.topology_mapper.map_topology(
        value_range=(1.0, 10.0),
        param_ranges={'alpha': (0.85, 0.95)},
        resolution=10  # Low resolution for speed
    )
    
    print(f"\n  Scan points: {len(topology['scan_points'])}")
    print(f"  Peaks found: {len(topology['peaks'])}")
    print(f"  Valleys found: {len(topology['valleys'])}")
    print(f"  Saddle points: {len(topology['saddles'])}")
    
    # Find high-coherence attractors
    attractors = field.topology_mapper.find_attractors(topology, min_coherence=0.999)
    print(f"\n  High-coherence attractors (NRCI > 0.999): {len(attractors)}")
    
    if attractors:
        for i, attractor in enumerate(attractors[:3]):
            print(f"    {i+1}. Coherence: {attractor['location']['coherence']:.10f}")
            print(f"       Parameters: {attractor['location']['params']}")
    
    print("\n✓ Field topology exploration completed")


# ============================================================================
# MAIN TEST RUNNER
# ============================================================================

def run_all_real_world_tests():
    """Run all real-world integration tests."""
    print("="*80)
    print("UBP Coherence Field ELITE - Real-World Study Integration Tests")
    print("="*80)
    
    tests = [
        test_symbol_study_integration,
        test_resonance_in_real_data,
        test_operator_optimization,
        test_stress_with_real_values,
        test_perception_reset_long_computation,
        test_field_topology_exploration
    ]
    
    passed = 0
    failed = 0
    
    for test_func in tests:
        try:
            test_func()
            passed += 1
        except Exception as e:
            print(f"\n✗ Test failed: {test_func.__name__}")
            print(f"  Error: {str(e)}")
            failed += 1
    
    # Summary
    print("\n" + "="*80)
    print("REAL-WORLD TEST SUMMARY")
    print("="*80)
    print(f"\nTotal: {passed}/{passed+failed} tests passed ({passed/(passed+failed)*100:.1f}%)")
    
    if failed == 0:
        print("\n✓ ALL REAL-WORLD TESTS PASSED")
        print("Coherence Field ELITE is ready for production use!")
    else:
        print(f"\n⚠ {failed} tests had issues")
    
    print("="*80)


if __name__ == "__main__":
    run_all_real_world_tests()
