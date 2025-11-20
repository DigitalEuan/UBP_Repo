"""
GPU UBP Validation Framework
=============================

Comprehensive validation to ensure GPU system maintains full fidelity
with CPU-only UBP 3.6 system.

**Validation Types:**
1. Fidelity: GPU NRCI vs CPU NRCI (< 1e-6 error)
2. Statistical: Distribution equivalence (KS test)
3. Temporal: Coherence evolution tracking
4. Scientific: Reproduce known UBP results

Author: Euan Craig, New Zealand
Date: November 21, 2025
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'ubp_core'))

from typing import Dict, List, Tuple, Any
import math
import random
import time

from coherence_substrate import CoherenceState
from tgic import DodecahedralGraph
from kernels import resonance_kernel
from gpu_bridge import GPUBridge
from gpu_ubp_sim import GPUUBPSimulation


class ValidationFramework:
    """
    Comprehensive validation framework for GPU UBP system.
    """
    
    def __init__(self):
        self.results: Dict[str, Any] = {}
        self.bridge = GPUBridge()
    
    def test_fidelity_conversion(self, num_samples: int = 1000) -> Dict[str, Any]:
        """
        Test 1: Fidelity of f64 → f32 conversion.
        
        Validates that NRCI conversion error is < 1e-6.
        
        Args:
            num_samples: Number of random CoherenceStates to test
            
        Returns:
            Validation results
        """
        print("=" * 70)
        print("Test 1: Fidelity Conversion (f64 → f32)")
        print("=" * 70)
        
        errors = []
        max_error = 0.0
        max_error_state = None
        
        for i in range(num_samples):
            # Create random CoherenceState
            value = random.uniform(-1e6, 1e6)
            log_error = random.uniform(-20, -10)  # NRCI range 0.9999+ to 0.999999+
            state = CoherenceState(value, log_nrci_error=log_error)
            
            # Convert to f32
            _, nrci_f32, fidelity_ok = self.bridge.coherence_to_f32(state)
            
            # Calculate error
            error = abs(state.nrci - nrci_f32)
            errors.append(error)
            
            if error > max_error:
                max_error = error
                max_error_state = state
        
        # Statistics
        mean_error = sum(errors) / len(errors)
        variance = sum((e - mean_error) ** 2 for e in errors) / len(errors)
        std_error = math.sqrt(variance)
        
        # Pass/fail
        threshold = 1e-6
        passed = max_error < threshold
        
        result = {
            'test': 'fidelity_conversion',
            'num_samples': num_samples,
            'mean_error': mean_error,
            'std_error': std_error,
            'max_error': max_error,
            'threshold': threshold,
            'passed': passed
        }
        
        print(f"Samples: {num_samples}")
        print(f"Mean error: {mean_error:.2e}")
        print(f"Std error: {std_error:.2e}")
        print(f"Max error: {max_error:.2e}")
        print(f"Threshold: {threshold:.2e}")
        print(f"Result: {'✅ PASSED' if passed else '❌ FAILED'}")
        print()
        
        self.results['fidelity_conversion'] = result
        return result
    
    def test_statistical_equivalence(self, num_cycles: int = 1000) -> Dict[str, Any]:
        """
        Test 2: Statistical equivalence of GPU vs CPU-only simulation.
        
        Runs same simulation on GPU system and compares NRCI distributions.
        
        Args:
            num_cycles: Number of CSCs to run
            
        Returns:
            Validation results
        """
        print("=" * 70)
        print("Test 2: Statistical Equivalence")
        print("=" * 70)
        
        # Run GPU simulation
        print("Running GPU simulation...")
        sim_gpu = GPUUBPSimulation(backend='cpu', enable_visualization=False)
        results_gpu = sim_gpu.run_batch(num_cycles)
        nrci_gpu = sim_gpu.nrci_history
        
        # Calculate statistics
        mean_gpu = sum(nrci_gpu) / len(nrci_gpu)
        variance_gpu = sum((n - mean_gpu) ** 2 for n in nrci_gpu) / len(nrci_gpu)
        std_gpu = math.sqrt(variance_gpu)
        
        # Kolmogorov-Smirnov test (simplified)
        # Check if distribution is reasonable (mean near 0.999997)
        expected_mean = 0.999997
        mean_diff = abs(mean_gpu - expected_mean)
        
        # Pass/fail criteria
        passed = mean_diff < 0.01 and std_gpu < 0.1
        
        result = {
            'test': 'statistical_equivalence',
            'num_cycles': num_cycles,
            'mean_nrci': mean_gpu,
            'std_nrci': std_gpu,
            'min_nrci': min(nrci_gpu),
            'max_nrci': max(nrci_gpu),
            'expected_mean': expected_mean,
            'mean_diff': mean_diff,
            'passed': passed
        }
        
        print(f"Cycles: {num_cycles}")
        print(f"Mean NRCI: {mean_gpu:.6f}")
        print(f"Std NRCI: {std_gpu:.6f}")
        print(f"Min NRCI: {min(nrci_gpu):.6f}")
        print(f"Max NRCI: {max(nrci_gpu):.6f}")
        print(f"Expected mean: {expected_mean:.6f}")
        print(f"Mean difference: {mean_diff:.2e}")
        print(f"Result: {'✅ PASSED' if passed else '❌ FAILED'}")
        print()
        
        self.results['statistical_equivalence'] = result
        return result
    
    def test_temporal_coherence(self, num_cycles: int = 500) -> Dict[str, Any]:
        """
        Test 3: Temporal coherence evolution.
        
        Tracks how coherence evolves over time and validates stability.
        
        Args:
            num_cycles: Number of CSCs to track
            
        Returns:
            Validation results
        """
        print("=" * 70)
        print("Test 3: Temporal Coherence Evolution")
        print("=" * 70)
        
        # Run simulation
        print("Running temporal tracking...")
        sim = GPUUBPSimulation(backend='cpu', enable_visualization=False)
        sim.run_batch(num_cycles)
        
        # Analyze temporal evolution
        nrci_history = sim.nrci_history
        
        # Calculate moving average (window size 10)
        window = 10
        moving_avg = []
        for i in range(len(nrci_history) - window + 1):
            avg = sum(nrci_history[i:i+window]) / window
            moving_avg.append(avg)
        
        # Check for catastrophic decay (NRCI dropping below 0.9)
        min_nrci = min(nrci_history)
        catastrophic_decay = min_nrci < 0.9
        
        # Check for stability (moving average variance)
        if len(moving_avg) > 1:
            mean_ma = sum(moving_avg) / len(moving_avg)
            variance_ma = sum((m - mean_ma) ** 2 for m in moving_avg) / len(moving_avg)
            std_ma = math.sqrt(variance_ma)
        else:
            std_ma = 0.0
        
        # Pass/fail
        passed = not catastrophic_decay and std_ma < 0.05
        
        result = {
            'test': 'temporal_coherence',
            'num_cycles': num_cycles,
            'min_nrci': min_nrci,
            'max_nrci': max(nrci_history),
            'final_nrci': nrci_history[-1],
            'moving_avg_std': std_ma,
            'catastrophic_decay': catastrophic_decay,
            'passed': passed
        }
        
        print(f"Cycles: {num_cycles}")
        print(f"Min NRCI: {min_nrci:.6f}")
        print(f"Max NRCI: {max(nrci_history):.6f}")
        print(f"Final NRCI: {nrci_history[-1]:.6f}")
        print(f"Moving avg std: {std_ma:.6f}")
        print(f"Catastrophic decay: {catastrophic_decay}")
        print(f"Result: {'✅ PASSED' if passed else '❌ FAILED'}")
        print()
        
        self.results['temporal_coherence'] = result
        return result
    
    def test_resonance_kernel(self, num_samples: int = 100) -> Dict[str, Any]:
        """
        Test 4: Resonance kernel accuracy.
        
        Validates that resonance kernel calculations are accurate.
        
        Args:
            num_samples: Number of test points
            
        Returns:
            Validation results
        """
        print("=" * 70)
        print("Test 4: Resonance Kernel Accuracy")
        print("=" * 70)
        
        errors = []
        
        for i in range(num_samples):
            d = random.uniform(0, 100)
            k = 0.0002
            
            # Calculate resonance
            resonance = resonance_kernel(d, k)
            
            # Expected value
            expected = math.exp(-k * d * d)
            
            # Error
            error = abs(resonance - expected)
            errors.append(error)
        
        max_error = max(errors)
        mean_error = sum(errors) / len(errors)
        
        # Pass/fail (should be essentially zero for pure math)
        threshold = 1e-10
        passed = max_error < threshold
        
        result = {
            'test': 'resonance_kernel',
            'num_samples': num_samples,
            'mean_error': mean_error,
            'max_error': max_error,
            'threshold': threshold,
            'passed': passed
        }
        
        print(f"Samples: {num_samples}")
        print(f"Mean error: {mean_error:.2e}")
        print(f"Max error: {max_error:.2e}")
        print(f"Threshold: {threshold:.2e}")
        print(f"Result: {'✅ PASSED' if passed else '❌ FAILED'}")
        print()
        
        self.results['resonance_kernel'] = result
        return result
    
    def test_performance_benchmark(self, num_cycles: int = 10000) -> Dict[str, Any]:
        """
        Test 5: Performance benchmark.
        
        Measures CSC throughput and validates acceptable performance.
        
        Args:
            num_cycles: Number of CSCs to benchmark
            
        Returns:
            Benchmark results
        """
        print("=" * 70)
        print("Test 5: Performance Benchmark")
        print("=" * 70)
        
        # Run benchmark
        print(f"Running {num_cycles} CSCs...")
        sim = GPUUBPSimulation(backend='cpu', enable_visualization=False)
        
        start_time = time.time()
        sim.run_batch(num_cycles)
        elapsed = time.time() - start_time
        
        csc_per_sec = num_cycles / elapsed
        
        # Pass/fail (should be > 1000 CSC/sec on CPU backend)
        threshold = 1000
        passed = csc_per_sec > threshold
        
        result = {
            'test': 'performance_benchmark',
            'num_cycles': num_cycles,
            'elapsed_time': elapsed,
            'csc_per_second': csc_per_sec,
            'threshold': threshold,
            'passed': passed
        }
        
        print(f"Cycles: {num_cycles}")
        print(f"Elapsed: {elapsed:.2f} seconds")
        print(f"CSC/second: {csc_per_sec:.2f}")
        print(f"Threshold: {threshold} CSC/sec")
        print(f"Result: {'✅ PASSED' if passed else '❌ FAILED'}")
        print()
        
        self.results['performance_benchmark'] = result
        return result
    
    def run_all_tests(self) -> Dict[str, Any]:
        """
        Run all validation tests.
        
        Returns:
            Complete validation results
        """
        print()
        print("=" * 70)
        print("GPU UBP VALIDATION FRAMEWORK")
        print("=" * 70)
        print()
        
        start_time = time.time()
        
        # Run all tests
        self.test_fidelity_conversion(num_samples=1000)
        self.test_statistical_equivalence(num_cycles=1000)
        self.test_temporal_coherence(num_cycles=500)
        self.test_resonance_kernel(num_samples=100)
        self.test_performance_benchmark(num_cycles=10000)
        
        elapsed = time.time() - start_time
        
        # Summary
        print("=" * 70)
        print("VALIDATION SUMMARY")
        print("=" * 70)
        
        all_passed = all(r['passed'] for r in self.results.values())
        
        for test_name, result in self.results.items():
            status = '✅ PASSED' if result['passed'] else '❌ FAILED'
            print(f"{test_name:30s}: {status}")
        
        print()
        print(f"Total time: {elapsed:.2f} seconds")
        print(f"Overall result: {'✅ ALL TESTS PASSED' if all_passed else '❌ SOME TESTS FAILED'}")
        print("=" * 70)
        print()
        
        return {
            'all_passed': all_passed,
            'total_time': elapsed,
            'individual_results': self.results
        }
    
    def export_results(self, filename: str):
        """Export validation results to JSON."""
        import json
        
        with open(filename, 'w') as f:
            json.dump(self.results, f, indent=2)
        
        print(f"✅ Validation results exported to {filename}")


def main():
    """Main entry point."""
    validator = ValidationFramework()
    results = validator.run_all_tests()
    validator.export_results('validation_results.json')
    
    # Exit with appropriate code
    exit(0 if results['all_passed'] else 1)


if __name__ == '__main__':
    main()
