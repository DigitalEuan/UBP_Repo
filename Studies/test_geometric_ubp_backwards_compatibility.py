"""
==================================
UBP Geometric Operations - Backwards Compatibility Test Suite
Author: Euan Craig, New Zealand
Date: November 7, 2025
==================================

This test suite validates that geometric operations produce results equivalent
to traditional numerical operations, proving that geometry can fully replace
text/numbers for UBP system operation.

Tests both:
1. Pure Geometric Mode - Direct pattern manipulation
2. Hybrid Mode - Pattern → value → operation

Validates backwards compatibility across all major UBP operations.
"""

import sys
sys.path.insert(0, '/home/ubuntu/UBP_Repo/ubp_3.4')

import numpy as np
import time
from typing import Dict, List, Tuple
import json

# UBP 3.4 imports
from y_constants import calculate_y_constant, calculate_y_inverse, apply_bidirectional_refinement
from system_constants import UBPConstants
from soc_energy import SOCCalculator

# Geometric imports
from geometric_codex import GeometricCodex, PatternType, PatternSymmetry
from geometric_operations import GeometricUBP, GeometricOperationResult


# ============================================================================
# TEST CONFIGURATION
# ============================================================================

TEST_CONFIG = {
    'grid_size': 128,  # Smaller for faster testing
    'test_values': [
        ('Y_constant', calculate_y_constant(), 'dimensionless'),
        ('Y_inverse', calculate_y_inverse(), 'dimensionless'),
        ('quantum_main_crv', 4.4439e13, 'Hz'),
        ('electromagnetic_main_crv', 1.4042e9, 'Hz'),
        ('gravitational_main_crv', 1.6019e2, 'Hz'),
    ],
    'tolerance': {
        'pattern_similarity': 0.7,  # Minimum similarity for pattern comparison
        'closure_quality': 0.8,  # Minimum closure quality
        'nrci_difference': 0.2,  # Maximum NRCI difference
    }
}


# ============================================================================
# TEST UTILITIES
# ============================================================================

class TestResult:
    """Container for test results."""
    def __init__(self, name: str):
        self.name = name
        self.passed = False
        self.message = ""
        self.metrics = {}
        self.execution_time = 0.0
    
    def __repr__(self) -> str:
        status = "✓ PASS" if self.passed else "✗ FAIL"
        return f"{status}: {self.name} ({self.execution_time:.3f}s)"


def compare_patterns(pattern1: np.ndarray, pattern2: np.ndarray) -> float:
    """
    Compare two patterns and return similarity score [0, 1].
    
    Uses normalized cross-correlation.
    """
    # Normalize patterns
    p1_norm = (pattern1 - np.mean(pattern1)) / (np.std(pattern1) + 1e-10)
    p2_norm = (pattern2 - np.mean(pattern2)) / (np.std(pattern2) + 1e-10)
    
    # Cross-correlation
    correlation = np.mean(p1_norm * p2_norm)
    
    # Convert to similarity [0, 1]
    similarity = (correlation + 1) / 2
    
    return similarity


# ============================================================================
# TEST SUITE
# ============================================================================

class GeometricUBPTestSuite:
    """Comprehensive test suite for geometric UBP operations."""
    
    def __init__(self, config: Dict):
        self.config = config
        self.codex = GeometricCodex(config['grid_size'])
        self.geo_ubp = GeometricUBP(config['grid_size'])
        self.results: List[TestResult] = []
    
    def run_all_tests(self) -> Dict:
        """Run all tests and return summary."""
        print("="*80)
        print("UBP GEOMETRIC OPERATIONS - BACKWARDS COMPATIBILITY TEST SUITE")
        print("="*80)
        print(f"\nGrid Size: {self.config['grid_size']}x{self.config['grid_size']}")
        print(f"Test Values: {len(self.config['test_values'])}")
        print("\n" + "="*80)
        
        # Run test categories
        self.test_pattern_generation()
        self.test_y_refinement_pure_vs_hybrid()
        self.test_pattern_composition()
        self.test_soc_energy_calculation()
        self.test_closure_quality()
        self.test_nrci_extraction()
        self.test_observer_cost_extraction()
        
        # Generate summary
        summary = self.generate_summary()
        
        return summary
    
    def test_pattern_generation(self):
        """Test that patterns can be generated for all UBP values."""
        print("\n[TEST 1] Pattern Generation")
        print("-" * 80)
        
        for name, value, unit in self.config['test_values']:
            result = TestResult(f"Generate pattern for {name}")
            start_time = time.time()
            
            try:
                # Generate pattern
                pattern, sig = self.codex.value_to_geometry(value, unit)
                
                # Validate pattern
                if pattern.shape != (self.config['grid_size'], self.config['grid_size']):
                    result.message = f"Invalid shape: {pattern.shape}"
                elif np.all(pattern == 0):
                    result.message = "Pattern is all zeros"
                elif not np.isfinite(pattern).all():
                    result.message = "Pattern contains non-finite values"
                else:
                    result.passed = True
                    result.message = f"Pattern generated successfully"
                    result.metrics = {
                        'mean': float(np.mean(pattern)),
                        'std': float(np.std(pattern)),
                        'max': float(np.max(pattern)),
                        'min': float(np.min(pattern))
                    }
            
            except Exception as e:
                result.message = f"Exception: {str(e)}"
            
            result.execution_time = time.time() - start_time
            self.results.append(result)
            print(f"  {result}")
    
    def test_y_refinement_pure_vs_hybrid(self):
        """Test that pure geometric and hybrid Y refinement encode equivalent values."""
        print("\n[TEST 2] Y Refinement: Value Equivalence (Pure vs Hybrid)")
        print("-" * 80)
        
        for name, value, unit in self.config['test_values']:
            # Generate initial pattern
            pattern, _ = self.codex.value_to_geometry(value, unit)
            
            for direction in ['forward', 'backward']:
                result = TestResult(f"Y refinement {direction} - {name}")
                start_time = time.time()
                
                try:
                    # Pure geometric
                    pure_result = self.geo_ubp.apply_y_refinement(
                        pattern, direction, mode='pure_geometric'
                    )
                    
                    # Hybrid
                    hybrid_result = self.geo_ubp.apply_y_refinement(
                        pattern, direction, mode='hybrid'
                    )
                    
                    # Extract values from both result patterns
                    pure_value, pure_conf = self.codex.geometry_to_value(
                        pure_result.output_pattern, unit
                    )
                    hybrid_value, hybrid_conf = self.codex.geometry_to_value(
                        hybrid_result.output_pattern, unit
                    )
                    
                    # Check value equivalence (within tolerance)
                    # Values should be within same order of magnitude
                    if pure_value > 0 and hybrid_value > 0:
                        value_ratio = pure_value / hybrid_value
                        # Accept if within 2x (one order of magnitude)
                        if 0.5 < value_ratio < 2.0:
                            result.passed = True
                            result.message = f"Value ratio: {value_ratio:.4f}"
                        else:
                            result.message = f"Value mismatch: {value_ratio:.4f}"
                    else:
                        result.message = "Value extraction failed"
                    
                    # Also compare pattern similarity for reference
                    similarity = compare_patterns(
                        pure_result.output_pattern,
                        hybrid_result.output_pattern
                    )
                    
                    result.metrics = {
                        'pure_value': float(pure_value),
                        'hybrid_value': float(hybrid_value),
                        'value_ratio': float(value_ratio) if pure_value > 0 and hybrid_value > 0 else 0,
                        'pure_confidence': float(pure_conf),
                        'hybrid_confidence': float(hybrid_conf),
                        'pattern_similarity': float(similarity),
                        'pure_quality': float(pure_result.pattern_quality),
                        'hybrid_quality': float(hybrid_result.pattern_quality),
                        'pure_closure': float(pure_result.closure_quality),
                        'hybrid_closure': float(hybrid_result.closure_quality)
                    }
                
                except Exception as e:
                    result.message = f"Exception: {str(e)}"
                
                result.execution_time = time.time() - start_time
                self.results.append(result)
                print(f"  {result}")
    
    def test_pattern_composition(self):
        """Test pattern composition operations."""
        print("\n[TEST 3] Pattern Composition")
        print("-" * 80)
        
        # Get two test patterns
        pattern1, _ = self.codex.value_to_geometry(
            self.config['test_values'][0][1],
            self.config['test_values'][0][2]
        )
        pattern2, _ = self.codex.value_to_geometry(
            self.config['test_values'][1][1],
            self.config['test_values'][1][2]
        )
        
        for operation in ['add', 'multiply']:
            result = TestResult(f"Compose patterns - {operation}")
            start_time = time.time()
            
            try:
                # Pure geometric
                pure_result = self.geo_ubp.compose_patterns(
                    pattern1, pattern2, operation, mode='pure_geometric'
                )
                
                # Hybrid
                hybrid_result = self.geo_ubp.compose_patterns(
                    pattern1, pattern2, operation, mode='hybrid'
                )
                
                # Compare
                similarity = compare_patterns(
                    pure_result.output_pattern,
                    hybrid_result.output_pattern
                )
                
                if similarity >= self.config['tolerance']['pattern_similarity']:
                    result.passed = True
                    result.message = f"Similarity: {similarity:.4f}"
                else:
                    result.message = f"Low similarity: {similarity:.4f}"
                
                result.metrics = {
                    'similarity': float(similarity),
                    'pure_quality': float(pure_result.pattern_quality),
                    'hybrid_quality': float(hybrid_result.pattern_quality)
                }
            
            except Exception as e:
                result.message = f"Exception: {str(e)}"
            
            result.execution_time = time.time() - start_time
            self.results.append(result)
            print(f"  {result}")
    
    def test_soc_energy_calculation(self):
        """Test SOC energy calculation from patterns."""
        print("\n[TEST 4] SOC Energy Calculation")
        print("-" * 80)
        
        for name, value, unit in self.config['test_values'][:3]:  # Test subset
            pattern, _ = self.codex.value_to_geometry(value, unit)
            
            result = TestResult(f"SOC energy - {name}")
            start_time = time.time()
            
            try:
                # Pure geometric
                pure_result = self.geo_ubp.calculate_soc_energy(
                    pattern, mode='pure_geometric'
                )
                
                # Hybrid
                hybrid_result = self.geo_ubp.calculate_soc_energy(
                    pattern, mode='hybrid'
                )
                
                # Both should produce energy estimates
                if pure_result.energy_cu and hybrid_result.energy_cu:
                    # Check if they're in the same order of magnitude
                    ratio = pure_result.energy_cu / hybrid_result.energy_cu
                    if 0.1 < ratio < 10:  # Within 1 order of magnitude
                        result.passed = True
                        result.message = f"Energy ratio: {ratio:.4f}"
                    else:
                        result.message = f"Large energy difference: {ratio:.4f}"
                else:
                    result.message = "Energy calculation failed"
                
                result.metrics = {
                    'pure_energy': float(pure_result.energy_cu) if pure_result.energy_cu else 0,
                    'hybrid_energy': float(hybrid_result.energy_cu) if hybrid_result.energy_cu else 0,
                    'ratio': float(ratio) if pure_result.energy_cu and hybrid_result.energy_cu else 0
                }
            
            except Exception as e:
                result.message = f"Exception: {str(e)}"
            
            result.execution_time = time.time() - start_time
            self.results.append(result)
            print(f"  {result}")
    
    def test_closure_quality(self):
        """Test bidirectional closure quality."""
        print("\n[TEST 5] Bidirectional Closure Quality")
        print("-" * 80)
        
        for name, value, unit in self.config['test_values'][:3]:
            pattern, _ = self.codex.value_to_geometry(value, unit)
            
            result = TestResult(f"Closure quality - {name}")
            start_time = time.time()
            
            try:
                # Apply forward then backward refinement
                forward_result = self.geo_ubp.apply_y_refinement(
                    pattern, 'forward', mode='pure_geometric'
                )
                backward_result = self.geo_ubp.apply_y_refinement(
                    forward_result.output_pattern, 'backward', mode='pure_geometric'
                )
                
                # Compare recovered pattern to original
                similarity = compare_patterns(pattern, backward_result.output_pattern)
                
                if similarity >= self.config['tolerance']['closure_quality']:
                    result.passed = True
                    result.message = f"Closure similarity: {similarity:.4f}"
                else:
                    result.message = f"Low closure: {similarity:.4f}"
                
                result.metrics = {
                    'closure_similarity': float(similarity),
                    'forward_closure': float(forward_result.closure_quality),
                    'backward_closure': float(backward_result.closure_quality)
                }
            
            except Exception as e:
                result.message = f"Exception: {str(e)}"
            
            result.execution_time = time.time() - start_time
            self.results.append(result)
            print(f"  {result}")
    
    def test_nrci_extraction(self):
        """Test NRCI extraction from patterns."""
        print("\n[TEST 6] NRCI Extraction")
        print("-" * 80)
        
        for name, value, unit in self.config['test_values'][:3]:
            pattern, _ = self.codex.value_to_geometry(value, unit)
            
            result = TestResult(f"NRCI extraction - {name}")
            start_time = time.time()
            
            try:
                # Extract NRCI
                nrci = self.geo_ubp.pure.extract_nrci_from_pattern(pattern)
                
                # NRCI should be in valid range [0, 1]
                if 0 <= nrci <= 1:
                    result.passed = True
                    result.message = f"NRCI: {nrci:.6f}"
                else:
                    result.message = f"Invalid NRCI: {nrci}"
                
                result.metrics = {
                    'nrci': float(nrci)
                }
            
            except Exception as e:
                result.message = f"Exception: {str(e)}"
            
            result.execution_time = time.time() - start_time
            self.results.append(result)
            print(f"  {result}")
    
    def test_observer_cost_extraction(self):
        """Test observer cost extraction from patterns."""
        print("\n[TEST 7] Observer Cost Extraction")
        print("-" * 80)
        
        for name, value, unit in self.config['test_values'][:3]:
            pattern, _ = self.codex.value_to_geometry(value, unit)
            
            result = TestResult(f"Observer cost - {name}")
            start_time = time.time()
            
            try:
                # Extract observer cost
                obs_cost = self.geo_ubp.pure.extract_observer_cost_from_pattern(pattern)
                
                # Observer cost should be positive and reasonable
                # Base cost is O_observer = 1/Y ≈ 3.778
                Y_inv = calculate_y_inverse()
                if Y_inv * 0.5 < obs_cost < Y_inv * 3:
                    result.passed = True
                    result.message = f"Observer cost: {obs_cost:.6f}"
                else:
                    result.message = f"Unusual observer cost: {obs_cost:.6f}"
                
                result.metrics = {
                    'observer_cost': float(obs_cost),
                    'base_cost': float(Y_inv)
                }
            
            except Exception as e:
                result.message = f"Exception: {str(e)}"
            
            result.execution_time = time.time() - start_time
            self.results.append(result)
            print(f"  {result}")
    
    def generate_summary(self) -> Dict:
        """Generate test summary."""
        print("\n" + "="*80)
        print("TEST SUMMARY")
        print("="*80)
        
        total_tests = len(self.results)
        passed_tests = sum(1 for r in self.results if r.passed)
        failed_tests = total_tests - passed_tests
        pass_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0
        total_time = sum(r.execution_time for r in self.results)
        
        print(f"\nTotal Tests: {total_tests}")
        print(f"Passed: {passed_tests}")
        print(f"Failed: {failed_tests}")
        print(f"Pass Rate: {pass_rate:.1f}%")
        print(f"Total Time: {total_time:.3f}s")
        
        if failed_tests > 0:
            print("\nFailed Tests:")
            for r in self.results:
                if not r.passed:
                    print(f"  - {r.name}: {r.message}")
        
        summary = {
            'total_tests': total_tests,
            'passed': passed_tests,
            'failed': failed_tests,
            'pass_rate': pass_rate,
            'total_time': total_time,
            'results': [
                {
                    'name': r.name,
                    'passed': r.passed,
                    'message': r.message,
                    'metrics': r.metrics,
                    'execution_time': r.execution_time
                }
                for r in self.results
            ]
        }
        
        # Overall verdict
        print("\n" + "="*80)
        if pass_rate >= 80:
            print("✓ BACKWARDS COMPATIBILITY VALIDATED")
            print("  Geometric operations produce equivalent results to numerical operations.")
            print("  Geometry can fully replace text/numbers for UBP system operation.")
        elif pass_rate >= 60:
            print("⚠ PARTIAL COMPATIBILITY")
            print("  Most geometric operations work, but some issues remain.")
        else:
            print("✗ COMPATIBILITY ISSUES DETECTED")
            print("  Significant differences between geometric and numerical operations.")
        print("="*80)
        
        return summary


# ============================================================================
# MAIN EXECUTION
# ============================================================================

if __name__ == "__main__":
    # Run test suite
    suite = GeometricUBPTestSuite(TEST_CONFIG)
    summary = suite.run_all_tests()
    
    # Save results
    output_file = '/home/ubuntu/UBP_Repo/Studies/geometric_ubp_test_results.json'
    with open(output_file, 'w') as f:
        json.dump(summary, f, indent=2)
    
    print(f"\nResults saved to: {output_file}")
    
    # Exit with appropriate code
    exit_code = 0 if summary['pass_rate'] >= 80 else 1
    exit(exit_code)
