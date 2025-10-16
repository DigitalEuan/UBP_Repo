"""
UBP Axiom Validation Tests

Unit tests that validate the mathematical axioms defined in spec/axioms.md.
These tests ensure the core semantic functions implement the correct formulas.
"""

import unittest
import math
from typing import List

# Import UBP semantic functions
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ubp_semantics import (
    OffBit, Bitfield, 
    resonance_kernel, coherence, global_coherence_invariant,
    energy, resonance_strength, structural_optimality,
    toggle_and, toggle_xor, toggle_or,
    resonance_toggle, entanglement_toggle, superposition_toggle,
    hybrid_xor_resonance, spin_transition,
    nrci, coherence_pressure_spatial, coherence_pressure_temporal,
    fractal_dimension, PI, PHI, E as EULER_E, C
)


class TestMathematicalAxioms(unittest.TestCase):
    """Test core mathematical axioms and formulas."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.tolerance = 1e-10
    
    def test_resonance_kernel_axiom(self):
        """Test resonance kernel: f(d) = exp(-k * d²)"""
        # Test with known values
        d = 2.0
        k = 0.0002
        expected = math.exp(-k * d * d)
        result = resonance_kernel(d, k)
        
        self.assertAlmostEqual(result, expected, places=10)
        
        # Test edge cases
        self.assertEqual(resonance_kernel(0, k), 1.0)  # exp(0) = 1
        self.assertLess(resonance_kernel(10, k), resonance_kernel(1, k))  # Decay with distance
    
    def test_coherence_axiom(self):
        """Test coherence: C_ij = (1/N) * Σ(s_i(t_k) * s_j(t_k))"""
        # Test with known signals
        s_i = [1.0, 2.0, 3.0, 4.0]
        s_j = [2.0, 4.0, 6.0, 8.0]
        
        # Manual calculation
        N = len(s_i)
        expected = sum(s_i[k] * s_j[k] for k in range(N)) / N
        result = coherence(s_i, s_j)
        
        self.assertAlmostEqual(result, expected, places=10)
        
        # Test perfect correlation
        perfect_coherence = coherence([1, 2, 3], [1, 2, 3])
        self.assertAlmostEqual(perfect_coherence, (1 + 4 + 9) / 3, places=10)
    
    def test_energy_equation_axiom(self):
        """Test energy equation: E = M × C × (R × S_opt) × P_GCI × O_observer × c_∞ × I_spin × w_sum"""
        # Test with known values
        M = 1000
        C_speed = 299792458
        R = 0.965885
        S_opt = 0.98
        P_GCI = 0.827046
        O_observer = 1.0
        c_infinity = 38.8328157095971
        I_spin = 1.0
        w_sum = 0.1
        
        expected = M * C_speed * (R * S_opt) * P_GCI * O_observer * c_infinity * I_spin * w_sum
        result = energy(M, C_speed, R, S_opt, P_GCI, O_observer, c_infinity, I_spin, w_sum)
        
        self.assertAlmostEqual(result, expected, places=5)
    
    def test_resonance_strength_axiom(self):
        """Test resonance strength: R = R_0 × (1 - H_t / ln(4))"""
        R_0 = 0.95
        H_t = 0.05
        
        expected = R_0 * (1 - H_t / math.log(4))
        result = resonance_strength(R_0, H_t)
        
        self.assertAlmostEqual(result, expected, places=10)
    
    def test_structural_optimality_axiom(self):
        """Test S_opt = 0.7 × (1 - Σd_i / √Σd_max²) + 0.3 × (Σb_j / 12)"""
        distances = [1.0, 2.0, 3.0]
        max_distance = 5.0
        active_bits = [6, 8, 10]  # Sum = 24, so 24/12 = 2.0
        
        # Manual calculation
        sum_distances = sum(distances)
        sqrt_sum_max_squared = math.sqrt(len(distances) * max_distance * max_distance)
        spatial_term = 1.0 - (sum_distances / sqrt_sum_max_squared)
        bit_term = sum(active_bits) / 12
        expected = 0.7 * spatial_term + 0.3 * bit_term
        
        result = structural_optimality(distances, max_distance, active_bits)
        
        self.assertAlmostEqual(result, expected, places=10)
    
    def test_global_coherence_invariant_axiom(self):
        """Test P_GCI = cos(2π * f_avg * Δt)"""
        f_avg = 1000.0
        delta_t = 0.318309886
        
        expected = math.cos(2 * PI * f_avg * delta_t)
        result = global_coherence_invariant(f_avg, delta_t)
        
        self.assertAlmostEqual(result, expected, places=10)
    
    def test_nrci_axiom(self):
        """Test NRCI = 1 - (RMSE(S, T) / σ(T))"""
        simulated = [1.0, 2.0, 3.0, 4.0, 5.0]
        target = [1.1, 1.9, 3.1, 3.9, 5.1]
        
        # Manual calculation
        squared_errors = [(s - t) ** 2 for s, t in zip(simulated, target)]
        rmse = math.sqrt(sum(squared_errors) / len(squared_errors))
        
        target_mean = sum(target) / len(target)
        target_variance = sum((t - target_mean) ** 2 for t in target) / len(target)
        target_std = math.sqrt(target_variance)
        
        expected = 1.0 - (rmse / target_std)
        result = nrci(simulated, target)
        
        self.assertAlmostEqual(result, expected, places=10)
    
    def test_fractal_dimension_axiom(self):
        """Test D = log(m) / log(s)"""
        sub_clusters = 8
        scale_factor = 2.0
        
        expected = math.log(sub_clusters) / math.log(scale_factor)
        result = fractal_dimension(sub_clusters, scale_factor)
        
        self.assertAlmostEqual(result, expected, places=10)


class TestToggleAlgebraAxioms(unittest.TestCase):
    """Test toggle algebra operation axioms."""
    
    def test_toggle_and_axiom(self):
        """Test AND: min(b_i, b_j)"""
        b_i = OffBit(100)
        b_j = OffBit(200)
        
        result = toggle_and(b_i, b_j)
        expected = min(b_i.value, b_j.value)
        
        self.assertEqual(result.value, expected)
        
        # Test with integers
        result_int = toggle_and(100, 200)
        self.assertEqual(result_int, 100)
    
    def test_toggle_xor_axiom(self):
        """Test XOR: |b_i - b_j|"""
        b_i = OffBit(100)
        b_j = OffBit(200)
        
        result = toggle_xor(b_i, b_j)
        expected = abs(b_i.value - b_j.value)
        
        self.assertEqual(result.value, expected)
        
        # Test with integers
        result_int = toggle_xor(100, 200)
        self.assertEqual(result_int, 100)
    
    def test_toggle_or_axiom(self):
        """Test OR: max(b_i, b_j)"""
        b_i = OffBit(100)
        b_j = OffBit(200)
        
        result = toggle_or(b_i, b_j)
        expected = max(b_i.value, b_j.value)
        
        self.assertEqual(result.value, expected)
        
        # Test with integers
        result_int = toggle_or(100, 200)
        self.assertEqual(result_int, 200)
    
    def test_resonance_toggle_axiom(self):
        """Test resonance: b_i × exp(-k × (t × f)²)"""
        b_i = OffBit(1000)
        frequency = 100.0
        time = 0.1
        k = 0.0002
        
        d = time * frequency
        expected_factor = math.exp(-k * d * d)
        expected_value = int(b_i.value * expected_factor)
        
        result = resonance_toggle(b_i, frequency, time, k)
        
        self.assertEqual(result.value, expected_value)
    
    def test_entanglement_toggle_axiom(self):
        """Test entanglement: b_i × b_j × C_ij (where C_ij ≥ 0.95)"""
        b_i = OffBit(100)
        b_j = OffBit(200)
        coherence_val = 0.96
        
        expected_value = int(b_i.value * b_j.value * coherence_val)
        result = entanglement_toggle(b_i, b_j, coherence_val)
        
        self.assertEqual(result.value, expected_value)
        
        # Test weak entanglement (< 0.95)
        weak_coherence = 0.5
        weak_result = entanglement_toggle(b_i, b_j, weak_coherence)
        expected_weak = int(b_i.value * b_j.value * weak_coherence * 0.1)
        self.assertEqual(weak_result.value, expected_weak)
    
    def test_superposition_toggle_axiom(self):
        """Test superposition: Σ(states × weights) where Σ weights = 1"""
        states = [OffBit(100), OffBit(200), OffBit(300)]
        weights = [0.2, 0.3, 0.5]
        
        expected_value = int(sum(state.value * weight for state, weight in zip(states, weights)))
        result = superposition_toggle(states, weights)
        
        self.assertEqual(result.value, expected_value)
        
        # Test weight normalization
        unnormalized_weights = [1.0, 2.0, 3.0]  # Sum = 6
        normalized_result = superposition_toggle(states, unnormalized_weights)
        
        # Should normalize to [1/6, 2/6, 3/6]
        expected_normalized = int(100 * (1/6) + 200 * (2/6) + 300 * (3/6))
        self.assertEqual(normalized_result.value, expected_normalized)
    
    def test_hybrid_xor_resonance_axiom(self):
        """Test hybrid XOR resonance: |b_i - b_j| × exp(-k × d²)"""
        b_i = OffBit(300)
        b_j = OffBit(100)
        d = 2.0
        k = 0.0002
        
        xor_value = abs(b_i.value - b_j.value)
        resonance_factor = math.exp(-k * d * d)
        expected_value = int(xor_value * resonance_factor)
        
        result = hybrid_xor_resonance(b_i, b_j, d, k)
        
        self.assertEqual(result.value, expected_value)
    
    def test_spin_transition_axiom(self):
        """Test spin transition: b_i × ln(1/p_s)"""
        b_i = OffBit(1000)
        p_s = 0.2265234857  # e/12
        
        transition_factor = math.log(1.0 / p_s)
        expected_value = int(b_i.value * transition_factor)
        
        result = spin_transition(b_i, p_s)
        
        self.assertEqual(result.value, expected_value)


class TestOffBitStructure(unittest.TestCase):
    """Test OffBit 24-bit layer structure."""
    
    def test_layer_structure(self):
        """Test 24-bit OffBit layer organization."""
        offbit = OffBit(0)
        
        # Test layer boundaries
        offbit.reality_layer = 63  # 6-bit max
        self.assertEqual(offbit.reality_layer, 63)
        
        offbit.information_layer = 63
        self.assertEqual(offbit.information_layer, 63)
        
        offbit.activation_layer = 63
        self.assertEqual(offbit.activation_layer, 63)
        
        offbit.unactivated_layer = 63
        self.assertEqual(offbit.unactivated_layer, 63)
        
        # Test full value
        expected_value = (63 << 18) | (63 << 12) | (63 << 6) | 63
        self.assertEqual(offbit.value, expected_value)
    
    def test_toggle_state(self):
        """Test toggle state (bit 12 of activation layer)."""
        offbit = OffBit(0)
        
        # Set toggle state
        offbit.toggle_state = True
        self.assertTrue(offbit.toggle_state)
        self.assertEqual(offbit.activation_layer & 1, 1)
        
        offbit.toggle_state = False
        self.assertFalse(offbit.toggle_state)
        self.assertEqual(offbit.activation_layer & 1, 0)
    
    def test_layer_bits(self):
        """Test individual bit manipulation within layers."""
        offbit = OffBit(0)
        
        # Set specific bit pattern
        bits = [1, 0, 1, 0, 1, 0]
        offbit.set_layer_bits('reality', bits)
        
        retrieved_bits = offbit.get_layer_bits('reality')
        self.assertEqual(retrieved_bits, bits)
        
        # Test value calculation
        expected_value = sum(bit << i for i, bit in enumerate(bits))
        self.assertEqual(offbit.reality_layer, expected_value)


class TestBitfieldStructure(unittest.TestCase):
    """Test Bitfield 6D structure and operations."""
    
    def setUp(self):
        """Set up test Bitfield."""
        self.bitfield = Bitfield("desktop_8gb")
    
    def test_coordinate_validation(self):
        """Test 6D coordinate validation."""
        # Valid coordinates
        valid_coord = (0, 0, 0, 0, 0, 0)
        self.assertTrue(self.bitfield.is_valid_coordinate(valid_coord))
        
        valid_coord_max = (169, 169, 169, 4, 1, 1)
        self.assertTrue(self.bitfield.is_valid_coordinate(valid_coord_max))
        
        # Invalid coordinates
        invalid_coord = (170, 0, 0, 0, 0, 0)  # Out of bounds
        self.assertFalse(self.bitfield.is_valid_coordinate(invalid_coord))
        
        invalid_coord_short = (0, 0, 0, 0, 0)  # Wrong dimension count
        self.assertFalse(self.bitfield.is_valid_coordinate(invalid_coord_short))
    
    def test_offbit_storage(self):
        """Test OffBit storage and retrieval."""
        coord = (10, 20, 30, 1, 0, 1)
        offbit = OffBit(12345)
        
        # Store OffBit
        self.bitfield.set_offbit(coord, offbit)
        
        # Retrieve OffBit
        retrieved = self.bitfield.get_offbit(coord)
        self.assertEqual(retrieved.value, offbit.value)
        
        # Test default OffBit for empty coordinates
        empty_coord = (0, 0, 0, 0, 0, 0)
        empty_offbit = self.bitfield.get_offbit(empty_coord)
        self.assertEqual(empty_offbit.value, 0)
    
    def test_sparsity_maintenance(self):
        """Test sparse storage (only non-zero OffBits stored)."""
        coord = (5, 5, 5, 0, 0, 0)
        
        # Set non-zero OffBit
        offbit = OffBit(1000)
        self.bitfield.set_offbit(coord, offbit)
        self.assertEqual(self.bitfield.total_offbits, 1)
        
        # Set zero OffBit (should be removed)
        zero_offbit = OffBit(0)
        self.bitfield.set_offbit(coord, zero_offbit)
        self.assertEqual(self.bitfield.total_offbits, 0)
    
    def test_neighbor_finding(self):
        """Test neighbor finding algorithm."""
        center_coord = (10, 10, 10, 1, 0, 0)
        neighbor_coord = (11, 10, 10, 1, 0, 0)
        
        # Set OffBits
        self.bitfield.set_offbit(center_coord, OffBit(100))
        self.bitfield.set_offbit(neighbor_coord, OffBit(200))
        
        # Find neighbors
        neighbors = self.bitfield.get_neighbors(center_coord, radius=1)
        
        # Should find the neighbor
        neighbor_coords = [coord for coord, offbit in neighbors]
        self.assertIn(neighbor_coord, neighbor_coords)


class TestConstantValues(unittest.TestCase):
    """Test that constants match specification values."""
    
    def test_fundamental_constants(self):
        """Test fundamental mathematical constants."""
        self.assertAlmostEqual(PI, 3.141592653589793, places=10)
        self.assertAlmostEqual(PHI, 1.618033988749895, places=10)
        self.assertAlmostEqual(EULER_E, 2.718281828459045, places=10)
        self.assertEqual(C, 299792458)
    
    def test_derived_constants(self):
        """Test derived UBP constants."""
        # Quantum CRV: e/12
        quantum_crv = EULER_E / 12
        self.assertAlmostEqual(quantum_crv, 0.2265234857, places=9)
        
        # Cosmological CRV: π^φ
        cosmological_crv = PI ** PHI
        self.assertAlmostEqual(cosmological_crv, 0.83203682, places=7)


if __name__ == '__main__':
    # Run all tests
    unittest.main(verbosity=2)

