#!/usr/bin/env python3
"""
UBP 3.7 - Comprehensive Validation Suite
========================================

REAL VALIDATION of all UBP 3.7 components.

This addresses the audit criticism about "limited physical validation."

This module provides:
- Component-level tests
- Integration tests
- Physics validation
- Performance benchmarks
- Regression tests

Author: UBP 3.7 Development
Date: November 28, 2025
Version: 3.7.0
"""

import numpy as np
import sys
import os
from typing import List, Dict, Tuple
from dataclasses import dataclass
import time

# Add parent directories to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'core'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'error_correction'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'analysis'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'simulation'))


@dataclass
class ValidationResult:
    """Result of a validation test."""
    test_name: str
    passed: bool
    message: str
    execution_time: float
    details: Dict = None
    
    def __repr__(self):
        status = "✓ PASS" if self.passed else "✗ FAIL"
        return f"{status} | {self.test_name} ({self.execution_time:.3f}s): {self.message}"


class ValidationSuite:
    """
    Comprehensive validation suite for UBP 3.7.
    """
    
    def __init__(self):
        self.results: List[ValidationResult] = []
    
    def run_test(self, test_name: str, test_func) -> ValidationResult:
        """Run a single test and record result."""
        start_time = time.time()
        
        try:
            passed, message, details = test_func()
            execution_time = time.time() - start_time
            
            result = ValidationResult(
                test_name=test_name,
                passed=passed,
                message=message,
                execution_time=execution_time,
                details=details
            )
        except Exception as e:
            execution_time = time.time() - start_time
            result = ValidationResult(
                test_name=test_name,
                passed=False,
                message=f"Exception: {str(e)}",
                execution_time=execution_time
            )
        
        self.results.append(result)
        return result
    
    def run_all_tests(self) -> Tuple[int, int]:
        """
        Run all validation tests.
        
        Returns:
            (passed_count, total_count)
        """
        print("="*70)
        print("UBP 3.7 COMPREHENSIVE VALIDATION SUITE")
        print("="*70)
        
        # Component tests
        print("\n[1] COMPONENT TESTS")
        print("-" * 70)
        self.run_test("Y-Constant Mathematical Closure", self.test_y_constant)
        self.run_test("Golay Code Error Correction", self.test_golay_code)
        self.run_test("Leech Lattice Structure", self.test_leech_lattice)
        self.run_test("VectorOffBit Operations", self.test_vector_offbit)
        self.run_test("Coherence Preservation", self.test_coherence)
        self.run_test("FFT Resonance Detection", self.test_resonance_fft)
        self.run_test("Physics Simulation", self.test_physics_simulation)
        
        # Integration tests
        print("\n[2] INTEGRATION TESTS")
        print("-" * 70)
        self.run_test("Golay-Leech Integration", self.test_golay_leech_integration)
        self.run_test("VectorOffBit-Golay Integration", self.test_vector_golay_integration)
        self.run_test("Coherence-Simulation Integration", self.test_coherence_simulation)
        
        # Physics validation
        print("\n[3] PHYSICS VALIDATION")
        print("-" * 70)
        self.run_test("Energy Conservation", self.test_energy_conservation)
        self.run_test("Analytical Solution Agreement", self.test_analytical_agreement)
        
        # Performance benchmarks
        print("\n[4] PERFORMANCE BENCHMARKS")
        print("-" * 70)
        self.run_test("Golay Encoding Performance", self.test_golay_performance)
        self.run_test("FFT Performance", self.test_fft_performance)
        self.run_test("Simulation Performance", self.test_simulation_performance)
        
        # Summary
        print("\n" + "="*70)
        print("VALIDATION SUMMARY")
        print("="*70)
        
        passed = sum(1 for r in self.results if r.passed)
        total = len(self.results)
        
        for result in self.results:
            print(result)
        
        print("="*70)
        print(f"TOTAL: {passed}/{total} tests passed ({100*passed/total:.1f}%)")
        print("="*70)
        
        return passed, total
    
    # ========================================================================
    # COMPONENT TESTS
    # ========================================================================
    
    def test_y_constant(self) -> Tuple[bool, str, Dict]:
        """Test Y-constant mathematical closure."""
        from y_constants_simple import Y, Y_INVERSE
        
        product = Y * Y_INVERSE
        error = abs(product - 1.0)
        
        passed = error < 1e-10
        message = f"Y × Y_INVERSE = {product:.15f}, error = {error:.2e}"
        details = {"product": product, "error": error}
        
        return passed, message, details
    
    def test_golay_code(self) -> Tuple[bool, str, Dict]:
        """Test Golay code error correction."""
        try:
            from golay_code import GolayG24
            
            golay = GolayG24()
            
            # Test encoding and error correction
            message = np.array([1,0,1,0,1,0,1,0,1,0,1,0])
            codeword = golay.encode(message)
            
            # Introduce error
            corrupted = codeword.copy()
            corrupted[5] = 1 - corrupted[5]  # Flip one bit
            
            # Correct
            corrected = golay.correct_errors(corrupted)
            
            # Check if correction worked
            passed = np.array_equal(corrected, codeword)
            message = f"Error correction: {'SUCCESS' if passed else 'FAILED'}"
            details = {"original": codeword, "corrupted": corrupted, "corrected": corrected}
            
            return passed, message, details
        except Exception as e:
            return False, f"Import or execution failed: {e}", {}
    
    def test_leech_lattice(self) -> Tuple[bool, str, Dict]:
        """Test Leech lattice structure."""
        try:
            from leech_lattice import LeechLattice
            
            lattice = LeechLattice()
            
            # Test dimension
            dim_ok = lattice.dimension == 24
            
            # Test kissing number
            kissing_ok = lattice.kissing_number == 196560
            
            # Test minimal vectors
            minimal = lattice.generate_shell(norm_squared=4, max_points=100)
            minimal_ok = len(minimal) > 0 and all(p.norm_squared == 4 for p in minimal)
            
            passed = dim_ok and kissing_ok and minimal_ok
            message = f"Dim={lattice.dimension}, Kissing={lattice.kissing_number}, Minimal={len(minimal)}"
            details = {"dimension": lattice.dimension, "kissing_number": lattice.kissing_number}
            
            return passed, message, details
        except Exception as e:
            return False, f"Import or execution failed: {e}", {}
    
    def test_vector_offbit(self) -> Tuple[bool, str, Dict]:
        """Test VectorOffBit operations."""
        try:
            from vector_offbit import VectorOffBit
            
            # Test creation
            v1 = VectorOffBit.from_binary(0b101010101010101010101010)
            v2 = VectorOffBit.from_binary(0b110011001100110011001100)
            
            # Test operations
            v_sum = v1 + v2
            dot_product = v1.dot(v2)
            norm1 = v1.norm()
            
            # Test conversion
            scalar = v1.to_scalar()
            v_recovered = VectorOffBit.from_binary(scalar)
            
            passed = (v1 == v_recovered) and norm1 > 0
            message = f"Norm={norm1:.4f}, Dot={dot_product:.4f}, Conversion={'OK' if v1 == v_recovered else 'FAIL'}"
            details = {"norm": norm1, "dot_product": dot_product}
            
            return passed, message, details
        except Exception as e:
            return False, f"Import or execution failed: {e}", {}
    
    def test_coherence(self) -> Tuple[bool, str, Dict]:
        """Test coherence preservation."""
        try:
            from core.coherence_substrate import CoherenceState
            
            # Test log-error tracking
            c1 = CoherenceState(1.0)
            c2 = c1.degrade_by(1e-6)
            
            # Check that coherence degrades correctly
            degraded = c2.nrci < c1.nrci
            
            # Test Y-refinement
            c3 = c1.refine_forward()
            c4 = c3.refine_backward()
            
            # Check round-trip
            roundtrip_error = abs(c4.value - c1.value)
            roundtrip_ok = roundtrip_error < 1e-10
            
            passed = degraded and roundtrip_ok
            message = f"Degradation={'OK' if degraded else 'FAIL'}, Roundtrip error={roundtrip_error:.2e}"
            details = {"nrci_initial": c1.nrci, "nrci_degraded": c2.nrci, "roundtrip_error": roundtrip_error}
            
            return passed, message, details
        except Exception as e:
            return False, f"Import or execution failed: {e}", {}
    
    def test_resonance_fft(self) -> Tuple[bool, str, Dict]:
        """Test FFT-based resonance detection."""
        try:
            from resonance_detector_fft import ResonanceDetectorFFT
            
            detector = ResonanceDetectorFFT(sample_rate=1000.0)
            
            # Create test signal with known frequency
            t = np.linspace(0, 1, 1000)
            signal = np.sin(2 * np.pi * 50 * t)
            
            analysis = detector.analyze_spectrum(signal)
            
            # Check if 50 Hz peak was detected
            if analysis.peaks:
                detected_freq = analysis.peaks[0].frequency
                freq_error = abs(detected_freq - 50.0)
                passed = freq_error < 1.0
                message = f"Detected {detected_freq:.2f} Hz (expected 50 Hz), error={freq_error:.2f} Hz"
                details = {"detected_frequency": detected_freq, "error": freq_error}
            else:
                passed = False
                message = "No peaks detected"
                details = {}
            
            return passed, message, details
        except Exception as e:
            return False, f"Import or execution failed: {e}", {}
    
    def test_physics_simulation(self) -> Tuple[bool, str, Dict]:
        """Test physics simulation engine."""
        try:
            from simulation import PhysicsSimulator, HarmonicOscillator, SimulationState
            from core.coherence_substrate import CoherenceState
            
            oscillator = HarmonicOscillator(k=1.0, m=1.0)
            simulator = PhysicsSimulator(dimension=1, integration_method='rk4')
            
            initial_state = SimulationState(
                time=0.0,
                position=np.array([1.0]),
                velocity=np.array([0.0]),
                energy=0.0,
                coherence=CoherenceState(1.0)
            )
            
            result = simulator.simulate(
                initial_state=initial_state,
                force_func=oscillator.force,
                energy_func=oscillator.energy,
                t_final=10.0,
                dt=0.01
            )
            
            # Check energy conservation
            energy_ok = result.energy_conservation < 1e-6
            
            passed = result.success and energy_ok
            message = f"Steps={result.total_steps}, Energy drift={result.energy_conservation:.2e}"
            details = {"energy_drift": result.energy_conservation, "steps": result.total_steps}
            
            return passed, message, details
        except Exception as e:
            return False, f"Import or execution failed: {e}", {}
    
    # ========================================================================
    # INTEGRATION TESTS
    # ========================================================================
    
    def test_golay_leech_integration(self) -> Tuple[bool, str, Dict]:
        """Test Golay-Leech integration."""
        try:
            from golay_code import GolayG24
            from leech_lattice import golay_to_leech, LeechLattice
            
            golay = GolayG24()
            lattice = LeechLattice()
            
            # Create Golay codeword
            message = np.array([1,0,1,0,1,0,1,0,1,0,1,0])
            codeword = golay.encode(message)
            
            # Convert to Leech point
            leech_point = golay_to_leech(codeword)
            
            # Check if it's in the lattice
            in_lattice = lattice.is_in_lattice(leech_point)
            
            passed = in_lattice
            message = f"Golay→Leech conversion: {'SUCCESS' if in_lattice else 'FAILED'}"
            details = {"in_lattice": in_lattice, "norm_squared": leech_point.norm_squared}
            
            return passed, message, details
        except Exception as e:
            return False, f"Import or execution failed: {e}", {}
    
    def test_vector_golay_integration(self) -> Tuple[bool, str, Dict]:
        """Test VectorOffBit-Golay integration."""
        try:
            from vector_offbit import VectorOffBit
            
            # Create VectorOffBit
            v = VectorOffBit.from_binary(0b101010101010101010101010)
            
            # Convert to Golay codeword
            golay_word = v.to_golay_codeword()
            
            # Convert back
            v_recovered = VectorOffBit.from_golay_codeword(golay_word)
            
            passed = v == v_recovered
            message = f"VectorOffBit↔Golay conversion: {'SUCCESS' if passed else 'FAILED'}"
            details = {}
            
            return passed, message, details
        except Exception as e:
            return False, f"Import or execution failed: {e}", {}
    
    def test_coherence_simulation(self) -> Tuple[bool, str, Dict]:
        """Test coherence-simulation integration."""
        try:
            from simulation import PhysicsSimulator, HarmonicOscillator, SimulationState
            from core.coherence_substrate import CoherenceState
            
            oscillator = HarmonicOscillator(k=1.0, m=1.0)
            simulator = PhysicsSimulator(dimension=1, integration_method='rk4')
            
            # Create initial state with coherence tracking
            initial_coherence = CoherenceState(1.0)
            initial_state = SimulationState(
                time=0.0,
                position=np.array([1.0]),
                velocity=np.array([0.0]),
                energy=0.0,
                coherence=initial_coherence
            )
            
            result = simulator.simulate(
                initial_state=initial_state,
                force_func=oscillator.force,
                energy_func=oscillator.energy,
                t_final=5.0,
                dt=0.01
            )
            
            # Check that coherence is tracked throughout
            coherence_tracked = all(s.coherence is not None for s in result.states)
            
            passed = coherence_tracked
            message = f"Coherence tracking: {'SUCCESS' if passed else 'FAILED'}"
            details = {}
            
            return passed, message, details
        except Exception as e:
            return False, f"Import or execution failed: {e}", {}
    
    # ========================================================================
    # PHYSICS VALIDATION
    # ========================================================================
    
    def test_energy_conservation(self) -> Tuple[bool, str, Dict]:
        """Test energy conservation in simulations."""
        try:
            from simulation import PhysicsSimulator, HarmonicOscillator, SimulationState
            from core.coherence_substrate import CoherenceState
            
            oscillator = HarmonicOscillator(k=1.0, m=1.0)
            simulator = PhysicsSimulator(dimension=1, integration_method='rk4')
            
            initial_state = SimulationState(
                time=0.0,
                position=np.array([1.0]),
                velocity=np.array([0.0]),
                energy=0.0,
                coherence=CoherenceState(1.0)
            )
            
            result = simulator.simulate(
                initial_state=initial_state,
                force_func=oscillator.force,
                energy_func=oscillator.energy,
                t_final=100.0,  # Long simulation
                dt=0.01
            )
            
            # Check energy conservation over long time
            passed = result.energy_conservation < 1e-6
            message = f"Energy drift over 100s: {result.energy_conservation:.2e}"
            details = {"energy_drift": result.energy_conservation}
            
            return passed, message, details
        except Exception as e:
            return False, f"Import or execution failed: {e}", {}
    
    def test_analytical_agreement(self) -> Tuple[bool, str, Dict]:
        """Test agreement with analytical solutions."""
        try:
            from simulation import PhysicsSimulator, HarmonicOscillator, SimulationState
            from core.coherence_substrate import CoherenceState
            
            oscillator = HarmonicOscillator(k=1.0, m=1.0)
            simulator = PhysicsSimulator(dimension=1, integration_method='rk4')
            
            initial_state = SimulationState(
                time=0.0,
                position=np.array([1.0]),
                velocity=np.array([0.0]),
                energy=0.0,
                coherence=CoherenceState(1.0)
            )
            
            result = simulator.simulate(
                initial_state=initial_state,
                force_func=oscillator.force,
                energy_func=oscillator.energy,
                t_final=10.0,
                dt=0.001  # Small timestep for accuracy
            )
            
            # Compare with analytical solution at t=5.0
            t_test = 5.0
            q_analytical, v_analytical = oscillator.analytical_solution(t_test, 1.0, 0.0)
            
            idx = np.argmin(np.abs(result.times - t_test))
            q_numerical = result.states[idx].position[0]
            
            error = abs(q_analytical - q_numerical)
            passed = error < 0.01
            message = f"Error at t=5.0: {error:.2e}"
            details = {"error": error, "analytical": q_analytical, "numerical": q_numerical}
            
            return passed, message, details
        except Exception as e:
            return False, f"Import or execution failed: {e}", {}
    
    # ========================================================================
    # PERFORMANCE BENCHMARKS
    # ========================================================================
    
    def test_golay_performance(self) -> Tuple[bool, str, Dict]:
        """Benchmark Golay encoding performance."""
        try:
            from golay_code import GolayG24
            
            golay = GolayG24()
            message = np.array([1,0,1,0,1,0,1,0,1,0,1,0])
            
            n_iterations = 1000
            start = time.time()
            for _ in range(n_iterations):
                codeword = golay.encode(message)
            elapsed = time.time() - start
            
            rate = n_iterations / elapsed
            passed = rate > 100  # At least 100 encodings/sec
            message = f"{rate:.0f} encodings/sec"
            details = {"rate": rate}
            
            return passed, message, details
        except Exception as e:
            return False, f"Import or execution failed: {e}", {}
    
    def test_fft_performance(self) -> Tuple[bool, str, Dict]:
        """Benchmark FFT performance."""
        try:
            from resonance_detector_fft import ResonanceDetectorFFT
            
            detector = ResonanceDetectorFFT(sample_rate=1000.0)
            signal = np.random.randn(1000)
            
            n_iterations = 100
            start = time.time()
            for _ in range(n_iterations):
                analysis = detector.analyze_spectrum(signal)
            elapsed = time.time() - start
            
            rate = n_iterations / elapsed
            passed = rate > 10  # At least 10 FFTs/sec
            message = f"{rate:.0f} FFTs/sec"
            details = {"rate": rate}
            
            return passed, message, details
        except Exception as e:
            return False, f"Import or execution failed: {e}", {}
    
    def test_simulation_performance(self) -> Tuple[bool, str, Dict]:
        """Benchmark simulation performance."""
        try:
            from simulation import PhysicsSimulator, HarmonicOscillator, SimulationState
            from core.coherence_substrate import CoherenceState
            
            oscillator = HarmonicOscillator(k=1.0, m=1.0)
            simulator = PhysicsSimulator(dimension=1, integration_method='rk4')
            
            initial_state = SimulationState(
                time=0.0,
                position=np.array([1.0]),
                velocity=np.array([0.0]),
                energy=0.0,
                coherence=CoherenceState(1.0)
            )
            
            start = time.time()
            result = simulator.simulate(
                initial_state=initial_state,
                force_func=oscillator.force,
                energy_func=oscillator.energy,
                t_final=10.0,
                dt=0.001  # 10,000 steps
            )
            elapsed = time.time() - start
            
            rate = result.total_steps / elapsed
            passed = rate > 1000  # At least 1000 steps/sec
            message = f"{rate:.0f} steps/sec"
            details = {"rate": rate, "steps": result.total_steps}
            
            return passed, message, details
        except Exception as e:
            return False, f"Import or execution failed: {e}", {}


# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    suite = ValidationSuite()
    passed, total = suite.run_all_tests()
    
    # Exit with appropriate code
    sys.exit(0 if passed == total else 1)
