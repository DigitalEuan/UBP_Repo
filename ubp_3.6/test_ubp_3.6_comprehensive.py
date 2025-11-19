"""
UBP 3.6 Comprehensive Test Suite
=================================

Tests all core functionality of UBP 3.6, including:
1. Coherence Substrate with Computational Grammar
2. Operator Registry and Composition
3. Coherence Field (NRCI+)
4. Operator Tracking and Analysis
5. Error Bounds and Warnings
6. Real-world use cases

Author: Euan R A Craig, New Zealand
Date: November 19, 2025
Version: 3.6.0
"""

import coherence_substrate as cs
import coherence_field as cf
import math

# ============================================================================
# TEST UTILITIES
# ============================================================================

class TestResult:
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.tests = []
    
    def add_test(self, name: str, passed: bool, message: str = ""):
        self.tests.append({
            'name': name,
            'passed': passed,
            'message': message
        })
        if passed:
            self.passed += 1
        else:
            self.failed += 1
    
    def print_summary(self):
        print("\n" + "="*80)
        print(f"TEST SUMMARY: {self.passed} passed, {self.failed} failed")
        print("="*80)
        
        if self.failed > 0:
            print("\nFailed tests:")
            for test in self.tests:
                if not test['passed']:
                    print(f"  ✗ {test['name']}: {test['message']}")
        
        print(f"\nOverall: {'✓ ALL TESTS PASSED' if self.failed == 0 else '✗ SOME TESTS FAILED'}")
        print("="*80)


def assert_close(a: float, b: float, tolerance: float = 1e-10, name: str = "") -> bool:
    """Assert that two values are close within tolerance."""
    if abs(a - b) < tolerance:
        return True
    else:
        print(f"  ✗ {name}: Expected {b:.10e}, got {a:.10e}, diff = {abs(a-b):.2e}")
        return False


# ============================================================================
# TEST SUITE
# ============================================================================

def run_all_tests():
    """Run all comprehensive tests for UBP 3.6."""
    results = TestResult()
    
    print("="*80)
    print("UBP 3.6 COMPREHENSIVE TEST SUITE")
    print("="*80)
    
    # ========================================================================
    # 1. COHERENCE SUBSTRATE TESTS
    # ========================================================================
    
    print("\n1. COHERENCE SUBSTRATE TESTS")
    print("-" * 80)
    
    # Test 1.1: Basic CoherenceState creation
    print("  1.1 CoherenceState Creation...")
    try:
        state = cs.CoherenceState(10.0)
        passed = (state.value == 10.0 and state.nrci > 0.999990)
        results.add_test("CoherenceState Creation", passed)
        if passed:
            print(f"    ✓ Created state with value={state.value}, nrci={state.nrci:.10f}")
    except Exception as e:
        results.add_test("CoherenceState Creation", False, str(e))
        print(f"    ✗ {e}")
    
    # Test 1.2: Y-refinement closure
    print("  1.2 Y-Refinement Closure...")
    try:
        x = cs.CoherenceState(100.0)
        y = x.refine_forward().refine_backward()
        error = abs(y.value - x.value) / x.value
        passed = error < 1e-12
        results.add_test("Y-Refinement Closure", passed, f"Error: {error:.2e}")
        if passed:
            print(f"    ✓ Closure error: {error:.2e}")
        else:
            print(f"    ✗ Closure error too large: {error:.2e}")
    except Exception as e:
        results.add_test("Y-Refinement Closure", False, str(e))
        print(f"    ✗ {e}")
    
    # Test 1.3: Arithmetic operations
    print("  1.3 Arithmetic Operations...")
    try:
        a = cs.CoherenceState(10.0)
        b = cs.CoherenceState(5.0)
        
        # Addition
        c = a + b
        passed_add = assert_close(c.value, 15.0, name="Addition")
        
        # Subtraction
        d = a - b
        passed_sub = assert_close(d.value, 5.0, name="Subtraction")
        
        # Multiplication
        e = a * b
        passed_mul = assert_close(e.value, 50.0, name="Multiplication")
        
        # Division
        f = a / b
        passed_div = assert_close(f.value, 2.0, name="Division")
        
        passed = passed_add and passed_sub and passed_mul and passed_div
        results.add_test("Arithmetic Operations", passed)
        if passed:
            print(f"    ✓ All arithmetic operations correct")
    except Exception as e:
        results.add_test("Arithmetic Operations", False, str(e))
        print(f"    ✗ {e}")
    
    # Test 1.4: Operator tracking
    print("  1.4 Operator Tracking...")
    try:
        x = cs.CoherenceState(2.0)
        y = x * x + x
        
        passed = ('+' in y.operator_sequence and '×' in y.operator_sequence)
        results.add_test("Operator Tracking", passed, f"Sequence: {y.operator_sequence}")
        if passed:
            print(f"    ✓ Operator sequence tracked: {y.operator_sequence}")
        else:
            print(f"    ✗ Operator tracking failed: {y.operator_sequence}")
    except Exception as e:
        results.add_test("Operator Tracking", False, str(e))
        print(f"    ✗ {e}")
    
    # ========================================================================
    # 2. OPERATOR REGISTRY TESTS
    # ========================================================================
    
    print("\n2. OPERATOR REGISTRY TESTS")
    print("-" * 80)
    
    # Test 2.1: Get primitive operators
    print("  2.1 Get Primitive Operators...")
    try:
        add_op = cs.get_operator_info('+')
        mul_op = cs.get_operator_info('×')
        
        passed = (add_op is not None and mul_op is not None and 
                 add_op.is_primitive and mul_op.is_primitive)
        results.add_test("Get Primitive Operators", passed)
        if passed:
            print(f"    ✓ Retrieved + (NRCI={add_op.nrci:.10f}) and × (NRCI={mul_op.nrci:.10f})")
    except Exception as e:
        results.add_test("Get Primitive Operators", False, str(e))
        print(f"    ✗ {e}")
    
    # Test 2.2: Operator composition
    print("  2.2 Operator Composition...")
    try:
        composed = cs.compose_operators('×', '+', 'arithmetic')
        
        passed = (composed.composition_depth == 1 and 
                 composed.nrci < 0.9999650000)  # Should be less than either primitive
        results.add_test("Operator Composition", passed, f"Composed NRCI: {composed.nrci:.10f}")
        if passed:
            print(f"    ✓ Composed (×∘+): NRCI={composed.nrci:.10f}, depth={composed.composition_depth}")
    except Exception as e:
        results.add_test("Operator Composition", False, str(e))
        print(f"    ✗ {e}")
    
    # Test 2.3: D6 composition model
    print("  2.3 D6 Composition Model...")
    try:
        op1 = cs.get_operator_info('×')
        op2 = cs.get_operator_info('+')
        composed = cs.compose_operators('×', '+', 'arithmetic')
        
        # D6 should follow non-linear model: D6(composed) = D6(op1) + D6(op2) * α
        expected_d6 = op1.d_variables['d6'] + op2.d_variables['d6'] * 0.9  # α = 0.9 for arithmetic
        actual_d6 = composed.d_variables['d6']
        
        passed = assert_close(actual_d6, expected_d6, tolerance=1e-6, name="D6 Composition")
        results.add_test("D6 Composition Model", passed, f"Expected: {expected_d6:.4f}, Got: {actual_d6:.4f}")
        if passed:
            print(f"    ✓ D6 composition follows non-linear model")
    except Exception as e:
        results.add_test("D6 Composition Model", False, str(e))
        print(f"    ✗ {e}")
    
    # ========================================================================
    # 3. COHERENCE FIELD TESTS
    # ========================================================================
    
    print("\n3. COHERENCE FIELD TESTS")
    print("-" * 80)
    
    # Test 3.1: Map state to coherence point
    print("  3.1 Map State to Coherence Point...")
    try:
        state = cs.CoherenceState(10.0) + cs.CoherenceState(5.0)
        point = cf.map_state(state)
        
        passed = (point.total_coherence > 0.999900 and 
                 point.composition_depth == 1)
        results.add_test("Map State to Coherence Point", passed)
        if passed:
            print(f"    ✓ Mapped state: coherence={point.total_coherence:.10f}, depth={point.composition_depth}")
    except Exception as e:
        results.add_test("Map State to Coherence Point", False, str(e))
        print(f"    ✗ {e}")
    
    # Test 3.2: Analyze computation
    print("  3.2 Analyze Computation...")
    try:
        state = cs.CoherenceState(2.0) * cs.CoherenceState(3.0) * cs.CoherenceState(4.0)
        analysis = cf.analyze(state)
        
        passed = ('operator_sequence' in analysis and 
                 'total_coherence' in analysis and
                 'error_bounds' in analysis)
        results.add_test("Analyze Computation", passed)
        if passed:
            print(f"    ✓ Analysis complete: depth={analysis['composition_depth']}, coherence={analysis['total_coherence']:.10f}")
    except Exception as e:
        results.add_test("Analyze Computation", False, str(e))
        print(f"    ✗ {e}")
    
    # Test 3.3: Error bounds computation
    print("  3.3 Error Bounds Computation...")
    try:
        state = cs.CoherenceState(100.0)
        error_low, error_high = cf.compute_error_bounds(state)
        
        passed = (error_low < 0 and error_high > 0 and abs(error_low) == abs(error_high))
        results.add_test("Error Bounds Computation", passed, f"Bounds: [{error_low:.2e}, {error_high:.2e}]")
        if passed:
            print(f"    ✓ Error bounds: [{error_low:.2e}, {error_high:.2e}]")
    except Exception as e:
        results.add_test("Error Bounds Computation", False, str(e))
        print(f"    ✗ {e}")
    
    # Test 3.4: Warnings for deep composition
    print("  3.4 Warnings for Deep Composition...")
    try:
        state = cs.CoherenceState(2.0)
        for _ in range(6):  # Create depth 6 composition
            state = state * cs.CoherenceState(2.0)
        
        analysis = cf.analyze(state)
        
        passed = (len(analysis['warnings']) > 0 and 
                 analysis['composition_depth'] > 5)
        results.add_test("Warnings for Deep Composition", passed, f"Warnings: {len(analysis['warnings'])}")
        if passed:
            print(f"    ✓ Warning generated for depth {analysis['composition_depth']}")
            for warning in analysis['warnings']:
                print(f"      - {warning}")
    except Exception as e:
        results.add_test("Warnings for Deep Composition", False, str(e))
        print(f"    ✗ {e}")
    
    # Test 3.5: State comparison
    print("  3.5 State Comparison...")
    try:
        path1 = cs.CoherenceState(10.0) + cs.CoherenceState(5.0)
        path2 = cs.CoherenceState(15.0)
        
        comparison = cf.compare_states(path1, path2)
        
        passed = ('comparison' in comparison and 
                 'better_coherence' in comparison['comparison'])
        results.add_test("State Comparison", passed)
        if passed:
            print(f"    ✓ Comparison: {comparison['comparison']['better_coherence']} has better coherence")
    except Exception as e:
        results.add_test("State Comparison", False, str(e))
        print(f"    ✗ {e}")
    
    # ========================================================================
    # 4. INTEGRATION TESTS
    # ========================================================================
    
    print("\n4. INTEGRATION TESTS")
    print("-" * 80)
    
    # Test 4.1: Complex calculation with full tracking
    print("  4.1 Complex Calculation with Full Tracking...")
    try:
        # Calculate (a + b) * (c - d) / e
        a = cs.CoherenceState(10.0)
        b = cs.CoherenceState(5.0)
        c = cs.CoherenceState(20.0)
        d = cs.CoherenceState(8.0)
        e = cs.CoherenceState(3.0)
        
        result = (a + b) * (c - d) / e
        
        expected_value = (10.0 + 5.0) * (20.0 - 8.0) / 3.0  # = 60.0
        
        passed = (assert_close(result.value, expected_value, name="Complex Calculation") and
                 result.composition_depth > 0)
        results.add_test("Complex Calculation", passed, f"Value: {result.value}, Depth: {result.composition_depth}")
        if passed:
            print(f"    ✓ Result: {result.value}, Coherence: {result.total_coherence:.10f}")
            print(f"      Operator sequence: {result.operator_sequence}")
    except Exception as e:
        results.add_test("Complex Calculation", False, str(e))
        print(f"    ✗ {e}")
    
    # Test 4.2: Y-refinement round-trip with tracking
    print("  4.2 Y-Refinement Round-Trip with Tracking...")
    try:
        original = cs.CoherenceState(1000.0)
        refined = original.refine_forward()
        restored = refined.refine_backward()
        
        error = abs(restored.value - original.value) / original.value
        
        passed = (error < 1e-12 and 
                 '⊗Y' in refined.operator_sequence and
                 '⊗Y⁻¹' in restored.operator_sequence)
        results.add_test("Y-Refinement Round-Trip", passed, f"Error: {error:.2e}")
        if passed:
            print(f"    ✓ Round-trip error: {error:.2e}")
            print(f"      Sequence: {restored.operator_sequence}")
    except Exception as e:
        results.add_test("Y-Refinement Round-Trip", False, str(e))
        print(f"    ✗ {e}")
    
    # Test 4.3: Coherence degradation with composition depth
    print("  4.3 Coherence Degradation with Composition Depth...")
    try:
        coherences = []
        state = cs.CoherenceState(2.0)
        
        for i in range(6):
            state = state * cs.CoherenceState(2.0)
            coherences.append(state.total_coherence)
        
        # Coherence should decrease monotonically
        passed = all(coherences[i] > coherences[i+1] for i in range(len(coherences)-1))
        results.add_test("Coherence Degradation", passed)
        if passed:
            print(f"    ✓ Coherence decreases with depth:")
            for i, coh in enumerate(coherences):
                print(f"      Depth {i+1}: {coh:.10f}")
    except Exception as e:
        results.add_test("Coherence Degradation", False, str(e))
        print(f"    ✗ {e}")
    
    # ========================================================================
    # 5. EDGE CASE TESTS
    # ========================================================================
    
    print("\n5. EDGE CASE TESTS")
    print("-" * 80)
    
    # Test 5.1: Division by near-zero
    print("  5.1 Division by Near-Zero...")
    try:
        a = cs.CoherenceState(10.0)
        b = cs.CoherenceState(1e-101)  # Below threshold of 1e-100
        
        try:
            result = a / b
            passed = False  # Should have raised an error
            results.add_test("Division by Near-Zero", False, "Should have raised ValueError")
            print(f"    ✗ Should have raised ValueError")
        except ValueError:
            passed = True
            results.add_test("Division by Near-Zero", True)
            print(f"    ✓ Correctly raised ValueError")
    except Exception as e:
        results.add_test("Division by Near-Zero", False, str(e))
        print(f"    ✗ Unexpected error: {e}")
    
    # Test 5.2: Very large values
    print("  5.2 Very Large Values...")
    try:
        a = cs.CoherenceState(1e100)
        b = cs.CoherenceState(1e100)
        c = a + b
        
        passed = assert_close(c.value, 2e100, tolerance=1e90, name="Large Values")
        results.add_test("Very Large Values", passed)
        if passed:
            print(f"    ✓ Handled large values: {c.value:.2e}")
    except Exception as e:
        results.add_test("Very Large Values", False, str(e))
        print(f"    ✗ {e}")
    
    # Test 5.3: Very small values
    print("  5.3 Very Small Values...")
    try:
        a = cs.CoherenceState(1e-100)
        b = cs.CoherenceState(1e-100)
        c = a + b
        
        passed = assert_close(c.value, 2e-100, tolerance=1e-110, name="Small Values")
        results.add_test("Very Small Values", passed)
        if passed:
            print(f"    ✓ Handled small values: {c.value:.2e}")
    except Exception as e:
        results.add_test("Very Small Values", False, str(e))
        print(f"    ✗ {e}")
    
    # ========================================================================
    # PRINT SUMMARY
    # ========================================================================
    
    results.print_summary()
    
    return results.failed == 0


# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    success = run_all_tests()
    exit(0 if success else 1)
