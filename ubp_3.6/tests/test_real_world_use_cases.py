"""
UBP 3.6 Real-World Use Case Tests
==================================

Tests UBP 3.6 with realistic computational scenarios to validate
accuracy, coherence tracking, and practical utility.

Use Cases:
1. Physics: Energy calculations with Y-refinement
2. Finance: Compound interest with error bounds
3. Signal Processing: Fourier-like transformations
4. Optimization: Finding optimal paths with coherence guidance
5. Scientific Computing: Numerical integration

Author: Euan R A Craig, New Zealand
Date: November 19, 2025
Version: 3.6.0
"""

import coherence_substrate as cs
import coherence_field as cf
import math

# ============================================================================
# USE CASE 1: PHYSICS - ENERGY CALCULATIONS
# ============================================================================

def test_physics_energy_calculation():
    """
    Test energy calculations with Y-refinement.
    
    Scenario: Calculate kinetic energy E = (1/2)mv² with coherence tracking.
    """
    print("\n" + "="*80)
    print("USE CASE 1: PHYSICS - ENERGY CALCULATIONS")
    print("="*80)
    
    # Constants
    mass = cs.CoherenceState(10.0)  # 10 kg
    velocity = cs.CoherenceState(5.0)  # 5 m/s
    half = cs.CoherenceState(0.5)
    
    # Calculate kinetic energy: E = (1/2)mv²
    v_squared = velocity * velocity
    energy = half * mass * v_squared
    
    # Analyze
    analysis = cf.analyze(energy, detailed=True)
    
    print(f"\nInput:")
    print(f"  Mass: {mass.value} kg")
    print(f"  Velocity: {velocity.value} m/s")
    
    print(f"\nResult:")
    print(f"  Kinetic Energy: {energy.value} J")
    print(f"  Expected: {0.5 * 10.0 * 5.0**2} J")
    print(f"  Error: {abs(energy.value - 125.0):.2e} J")
    
    print(f"\nCoherence Analysis:")
    print(f"  Operator sequence: {analysis['operator_sequence']}")
    print(f"  Composition depth: {analysis['composition_depth']}")
    print(f"  Total coherence: {analysis['total_coherence']:.10f}")
    print(f"  Error bounds: [{analysis['error_bounds'][0]:.2e}, {analysis['error_bounds'][1]:.2e}]")
    
    if analysis['warnings']:
        print(f"\n  Warnings:")
        for warning in analysis['warnings']:
            print(f"    - {warning}")
    
    # Test Y-refinement for energy scale transformation
    print(f"\nY-Refinement Test:")
    refined_energy = energy.refine_forward()
    print(f"  Original energy: {energy.value:.6f} J")
    print(f"  Refined energy: {refined_energy.value:.6f} J")
    print(f"  Refinement factor: {refined_energy.value / energy.value:.10f}")
    print(f"  Expected Y: {cs.Y:.10f}")
    print(f"  Match: {abs(refined_energy.value / energy.value - cs.Y) < 1e-10}")
    
    return abs(energy.value - 125.0) < 1e-10


# ============================================================================
# USE CASE 2: FINANCE - COMPOUND INTEREST
# ============================================================================

def test_finance_compound_interest():
    """
    Test compound interest calculations with error bounds.
    
    Scenario: Calculate A = P(1 + r)^n with coherence tracking.
    """
    print("\n" + "="*80)
    print("USE CASE 2: FINANCE - COMPOUND INTEREST")
    print("="*80)
    
    # Initial investment
    principal = cs.CoherenceState(10000.0)  # $10,000
    rate = cs.CoherenceState(1.05)  # 5% annual return
    years = 10
    
    # Calculate compound interest: A = P * (1 + r)^n
    amount = principal
    for year in range(years):
        amount = amount * rate
    
    # Analyze
    analysis = cf.analyze(amount)
    
    print(f"\nInput:")
    print(f"  Principal: ${principal.value:,.2f}")
    print(f"  Annual rate: {(rate.value - 1.0) * 100:.1f}%")
    print(f"  Years: {years}")
    
    print(f"\nResult:")
    print(f"  Final amount: ${amount.value:,.2f}")
    
    expected = 10000.0 * (1.05 ** 10)
    print(f"  Expected: ${expected:,.2f}")
    print(f"  Error: ${abs(amount.value - expected):.2e}")
    
    print(f"\nCoherence Analysis:")
    print(f"  Composition depth: {analysis['composition_depth']}")
    print(f"  Total coherence: {analysis['total_coherence']:.10f}")
    
    # Compute monetary error bounds
    error_low, error_high = cf.compute_error_bounds(amount)
    monetary_error = abs(error_high * amount.value)
    
    print(f"  Error bounds: ±${monetary_error:.2f}")
    print(f"  Relative error: ±{abs(error_high) * 100:.4f}%")
    
    if analysis['warnings']:
        print(f"\n  Warnings:")
        for warning in analysis['warnings']:
            print(f"    - {warning}")
    
    return abs(amount.value - expected) < 1e-6


# ============================================================================
# USE CASE 3: SIGNAL PROCESSING - FOURIER-LIKE TRANSFORMATION
# ============================================================================

def test_signal_processing():
    """
    Test signal processing with coherence tracking.
    
    Scenario: Compute discrete cosine-like transformation.
    """
    print("\n" + "="*80)
    print("USE CASE 3: SIGNAL PROCESSING - FOURIER-LIKE TRANSFORMATION")
    print("="*80)
    
    # Create a simple signal
    signal = [cs.CoherenceState(math.cos(2 * math.pi * i / 8)) for i in range(8)]
    
    print(f"\nInput Signal (8 samples):")
    for i, s in enumerate(signal):
        print(f"  s[{i}] = {s.value:+.6f}")
    
    # Compute sum (simplified "DC component")
    dc_component = signal[0]
    for s in signal[1:]:
        dc_component = dc_component + s
    
    dc_component = dc_component / cs.CoherenceState(8.0)
    
    # Analyze
    analysis = cf.analyze(dc_component)
    
    print(f"\nResult:")
    print(f"  DC component: {dc_component.value:.6f}")
    print(f"  Expected: ~0.0 (cosine has zero mean)")
    
    print(f"\nCoherence Analysis:")
    print(f"  Composition depth: {analysis['composition_depth']}")
    print(f"  Total coherence: {analysis['total_coherence']:.10f}")
    
    if analysis['warnings']:
        print(f"\n  Warnings:")
        for warning in analysis['warnings']:
            print(f"    - {warning}")
    
    return abs(dc_component.value) < 0.1  # Should be close to zero


# ============================================================================
# USE CASE 4: OPTIMIZATION - PATH FINDING WITH COHERENCE
# ============================================================================

def test_optimization_path_finding():
    """
    Test optimization using coherence as a guide.
    
    Scenario: Find the computational path with highest coherence.
    """
    print("\n" + "="*80)
    print("USE CASE 4: OPTIMIZATION - PATH FINDING WITH COHERENCE")
    print("="*80)
    
    # Goal: Compute 100 using different paths
    target = 100.0
    
    # Path 1: Direct
    path1 = cs.CoherenceState(100.0)
    
    # Path 2: 50 + 50
    path2 = cs.CoherenceState(50.0) + cs.CoherenceState(50.0)
    
    # Path 3: 10 * 10
    path3 = cs.CoherenceState(10.0) * cs.CoherenceState(10.0)
    
    # Path 4: 200 / 2
    path4 = cs.CoherenceState(200.0) / cs.CoherenceState(2.0)
    
    # Path 5: (5 * 5) * 4
    path5 = (cs.CoherenceState(5.0) * cs.CoherenceState(5.0)) * cs.CoherenceState(4.0)
    
    paths = [
        ("Direct", path1),
        ("50 + 50", path2),
        ("10 × 10", path3),
        ("200 ÷ 2", path4),
        ("(5 × 5) × 4", path5)
    ]
    
    print(f"\nTarget value: {target}")
    print(f"\nComparing {len(paths)} computational paths:\n")
    
    best_path = None
    best_coherence = 0.0
    
    for name, path in paths:
        analysis = cf.analyze(path)
        print(f"  {name:15s}: value={path.value:6.1f}, coherence={analysis['total_coherence']:.10f}, depth={analysis['composition_depth']}")
        
        if analysis['total_coherence'] > best_coherence:
            best_coherence = analysis['total_coherence']
            best_path = name
    
    print(f"\nOptimal path: {best_path} (coherence = {best_coherence:.10f})")
    print(f"\nInsight: Direct assignment has highest coherence (no operations = no degradation)")
    
    return best_path == "Direct"


# ============================================================================
# USE CASE 5: SCIENTIFIC COMPUTING - NUMERICAL INTEGRATION
# ============================================================================

def test_scientific_computing_integration():
    """
    Test numerical integration with coherence tracking.
    
    Scenario: Integrate f(x) = x² from 0 to 10.
    """
    print("\n" + "="*80)
    print("USE CASE 5: SCIENTIFIC COMPUTING - NUMERICAL INTEGRATION")
    print("="*80)
    
    # Define function
    def f(x):
        return x ** 2
    
    # Integration bounds
    a = 0.0
    b = 10.0
    
    print(f"\nIntegrating f(x) = x² from {a} to {b}")
    
    # Use UBP's coherent integration
    result, metadata = cs.integrate_coherent(f, a, b)
    
    # Analytical result: ∫x² dx = x³/3, so ∫₀¹⁰ x² dx = 1000/3 ≈ 333.333
    expected = (b**3 - a**3) / 3.0
    
    print(f"\nResult:")
    print(f"  Numerical: {result.value:.6f}")
    print(f"  Analytical: {expected:.6f}")
    print(f"  Error: {abs(result.value - expected):.6f}")
    print(f"  Relative error: {abs(result.value - expected) / expected * 100:.4f}%")
    
    print(f"\nCoherence Analysis:")
    print(f"  Final NRCI: {result.nrci:.10f}")
    print(f"  Samples used: {metadata['n_samples']}")
    
    # Analyze the result
    analysis = cf.analyze(result)
    
    if analysis['warnings']:
        print(f"\n  Warnings:")
        for warning in analysis['warnings']:
            print(f"    - {warning}")
    
    return abs(result.value - expected) / expected < 0.01  # Within 1%


# ============================================================================
# USE CASE 6: COMPARATIVE ANALYSIS
# ============================================================================

def test_comparative_analysis():
    """
    Test comparative analysis of different computational approaches.
    
    Scenario: Compare standard Python vs UBP for a complex calculation.
    """
    print("\n" + "="*80)
    print("USE CASE 6: COMPARATIVE ANALYSIS - PYTHON VS UBP")
    print("="*80)
    
    # Complex calculation: ((a + b) * c - d) / e
    a_val, b_val, c_val, d_val, e_val = 10.0, 5.0, 3.0, 20.0, 5.0
    
    # Standard Python
    python_result = ((a_val + b_val) * c_val - d_val) / e_val
    
    # UBP
    a = cs.CoherenceState(a_val)
    b = cs.CoherenceState(b_val)
    c = cs.CoherenceState(c_val)
    d = cs.CoherenceState(d_val)
    e = cs.CoherenceState(e_val)
    
    ubp_result = ((a + b) * c - d) / e
    
    print(f"\nCalculation: ((a + b) × c − d) ÷ e")
    print(f"  where a={a_val}, b={b_val}, c={c_val}, d={d_val}, e={e_val}")
    
    print(f"\nResults:")
    print(f"  Python: {python_result:.10f}")
    print(f"  UBP:    {ubp_result.value:.10f}")
    print(f"  Match:  {abs(python_result - ubp_result.value) < 1e-10}")
    
    # UBP provides additional information
    analysis = cf.analyze(ubp_result)
    
    print(f"\nUBP Additional Information:")
    print(f"  Operator sequence: {analysis['operator_sequence']}")
    print(f"  Composition depth: {analysis['composition_depth']}")
    print(f"  Total coherence: {analysis['total_coherence']:.10f}")
    
    error_low, error_high = cf.compute_error_bounds(ubp_result)
    print(f"  Error bounds: [{ubp_result.value + error_low:.6f}, {ubp_result.value + error_high:.6f}]")
    
    print(f"\nInsight: UBP provides the same numerical result as Python,")
    print(f"         but with additional coherence tracking and error bounds.")
    
    return abs(python_result - ubp_result.value) < 1e-10


# ============================================================================
# MAIN TEST RUNNER
# ============================================================================

def run_all_use_cases():
    """Run all real-world use case tests."""
    print("="*80)
    print("UBP 3.6 REAL-WORLD USE CASE TESTS")
    print("="*80)
    
    results = []
    
    # Run all use cases
    use_cases = [
        ("Physics - Energy Calculations", test_physics_energy_calculation),
        ("Finance - Compound Interest", test_finance_compound_interest),
        ("Signal Processing", test_signal_processing),
        ("Optimization - Path Finding", test_optimization_path_finding),
        ("Scientific Computing - Integration", test_scientific_computing_integration),
        ("Comparative Analysis", test_comparative_analysis),
    ]
    
    for name, test_func in use_cases:
        try:
            passed = test_func()
            results.append((name, passed))
        except Exception as e:
            print(f"\n✗ {name} FAILED: {e}")
            results.append((name, False))
    
    # Print summary
    print("\n" + "="*80)
    print("REAL-WORLD USE CASE TEST SUMMARY")
    print("="*80)
    
    passed_count = sum(1 for _, passed in results if passed)
    total_count = len(results)
    
    for name, passed in results:
        status = "✓ PASSED" if passed else "✗ FAILED"
        print(f"  {status}: {name}")
    
    print(f"\nTotal: {passed_count}/{total_count} passed")
    print("="*80)
    
    return passed_count == total_count


# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    success = run_all_use_cases()
    exit(0 if success else 1)
