"""
Proper Toggle Algebra Implementation for UBP

This module implements the toggle algebra operations based on the UBP theoretical
framework, including realm-specific resonances, coherence calculations, and
physics-based interactions.

Author: Manus AI
Date: September 23, 2025
"""

import numpy as np
from . import constants as const

class ToggleAlgebra:
    """
    Implements the proper toggle algebra for the UBP framework.
    """
    
    def __init__(self):
        # Core Resonance Values (CRVs) from UBP specification
        self.CRVs = {
            'quantum': const.CRV_QUANTUM[1],      # 4.58e14 Hz (655 nm)
            'electromagnetic': const.CRV_ELECTROMAGNETIC[1],  # π Hz (635 nm)
            'gravitational': const.CRV_GRAVITATIONAL[1],      # 100 Hz (1000 nm)
            'biological': const.CRV_BIOLOGICAL[1],            # 10 Hz (700 nm)
            'cosmological': const.CRV_COSMOLOGICAL[1],        # 1e-11 Hz (800 nm)
            'nuclear': const.CRV_NUCLEAR[1],      # 1e16-1e20 Hz
            'optical': const.CRV_OPTICAL[1]       # 5e14 Hz (600 nm)
        }
        
        # Toggle biases from UBP specification
        self.toggle_biases = {
            'quantum': const.TOGGLE_BIAS_QUANTUM,      # e/12 ≈ 0.2265234857
            'cosmological': const.TOGGLE_BIAS_COSMOLOGICAL  # π^φ ≈ 0.83203682
        }
        
        # Coherent Synchronization Cycle period
        self.csc_period = const.CSC_BASE_PERIOD  # 1/π ≈ 0.318309886 s
    
    def calculate_coherence(self, offbit_i, offbit_j, time_step):
        """
        Calculate coherence between two OffBits using the UBP formula:
        C_ij = (1/N) * Σ s_i(t_k) * s_j(t_k)
        where s_i(t) = cos(2π * f_i * t + φ_i)
        """
        # Extract frequencies based on realm (simplified mapping)
        f_i = self._get_frequency_for_offbit(offbit_i)
        f_j = self._get_frequency_for_offbit(offbit_j)
        
        # Calculate phase-based signals
        t = time_step * self.csc_period
        s_i = np.cos(2 * np.pi * f_i * t + offbit_i.get_state() / 1000.0)
        s_j = np.cos(2 * np.pi * f_j * t + offbit_j.get_state() / 1000.0)
        
        return s_i * s_j
    
    def _get_frequency_for_offbit(self, offbit):
        """Map OffBit to its realm frequency based on toggle bias."""
        if abs(offbit.toggle_bias - self.toggle_biases['quantum']) < 0.01:
            return self.CRVs['quantum']
        elif abs(offbit.toggle_bias - self.toggle_biases['cosmological']) < 0.01:
            return self.CRVs['cosmological']
        else:
            return self.CRVs['biological']  # Default to biological
    
    def resonance_operation(self, offbit, time_step, realm='biological'):
        """
        Apply resonance operation: b_i * exp(-0.0002 * d^2)
        where d = t * f_i
        """
        f_i = self.CRVs[realm]
        t = time_step * self.csc_period
        d = t * f_i
        
        resonance_factor = np.exp(-0.0002 * d**2)
        new_state = int(offbit.get_state() * resonance_factor) % (2**24)
        
        return new_state
    
    def entanglement_operation(self, offbit_i, offbit_j, time_step):
        """
        Apply entanglement operation based on coherence.
        If C_ij >= 0.95, apply strong entanglement (XOR).
        Otherwise, apply weak interaction.
        """
        coherence = self.calculate_coherence(offbit_i, offbit_j, time_step)
        
        if abs(coherence) >= 0.95:
            # Strong entanglement - XOR operation
            return offbit_i.get_state() ^ offbit_j.get_state()
        else:
            # Weak interaction - weighted combination
            weight = abs(coherence)
            combined = int(weight * offbit_i.get_state() + (1 - weight) * offbit_j.get_state())
            return combined % (2**24)
    
    def superposition_operation(self, offbits, weights=None):
        """
        Apply superposition: Σ(states * w_ij) where Σw_ij = 1
        """
        if weights is None:
            weights = np.ones(len(offbits)) / len(offbits)
        
        if len(weights) != len(offbits):
            raise ValueError("Number of weights must match number of OffBits")
        
        if abs(sum(weights) - 1.0) > 1e-6:
            weights = np.array(weights) / sum(weights)  # Normalize
        
        superposed_state = sum(w * offbit.get_state() for w, offbit in zip(weights, offbits))
        return int(superposed_state) % (2**24)
    
    def hybrid_prom_operation(self, offbit_i, offbit_j, time_step, realm='biological'):
        """
        Hybrid PROM: |b_i - b_j| * exp(-0.0002 * d^2)
        Combines XOR-like operation with resonance.
        """
        xor_result = offbit_i.get_state() ^ offbit_j.get_state()
        
        # Apply resonance to the XOR result
        f_i = self.CRVs[realm]
        t = time_step * self.csc_period
        d = t * f_i
        
        resonance_factor = np.exp(-0.0002 * d**2)
        return int(xor_result * resonance_factor) % (2**24)
    
    def spin_transition_operation(self, offbit, realm='quantum'):
        """
        Apply spin transition: b_i * ln(1 / p_s)
        where p_s is the toggle bias for the realm.
        """
        if realm == 'quantum':
            p_s = self.toggle_biases['quantum']
        elif realm == 'cosmological':
            p_s = self.toggle_biases['cosmological']
        else:
            p_s = self.toggle_biases['quantum']  # Default
        
        if p_s <= 0 or p_s >= 1:
            return offbit.get_state()  # Avoid log issues
        
        spin_factor = np.log(1 / p_s)
        return int(offbit.get_state() * spin_factor) % (2**24)
    
    def apply_tgic_operation(self, offbit, neighbors, time_step):
        """
        Apply Triad Graph Interaction Constraint operation.
        This enforces the 3,6,9 structure through neighbor interactions.
        """
        if not neighbors:
            return offbit.get_state()
        
        # Calculate weighted interaction with neighbors
        total_influence = 0
        total_weight = 0
        
        for neighbor in neighbors:
            coherence = self.calculate_coherence(offbit, neighbor, time_step)
            weight = abs(coherence)
            total_influence += weight * neighbor.get_state()
            total_weight += weight
        
        if total_weight == 0:
            return offbit.get_state()
        
        # Apply TGIC constraint: blend own state with neighbor influence
        tgic_factor = 0.1  # Strength of TGIC influence
        neighbor_influence = total_influence / total_weight
        
        new_state = int((1 - tgic_factor) * offbit.get_state() + 
                       tgic_factor * neighbor_influence)
        
        return new_state % (2**24)
    
    def calculate_nrci(self, actual_states, theoretical_states):
        """
        Calculate Non-Random Coherence Index:
        NRCI = 1 - (RMSE / σ(T))
        """
        actual = np.array(actual_states, dtype=float)
        theoretical = np.array(theoretical_states, dtype=float)
        
        if len(actual) != len(theoretical):
            min_len = min(len(actual), len(theoretical))
            actual = actual[:min_len]
            theoretical = theoretical[:min_len]
        
        # Calculate RMSE
        rmse = np.sqrt(np.mean((actual - theoretical)**2))
        
        # Calculate standard deviation of theoretical states
        sigma_t = np.std(theoretical)
        
        if sigma_t == 0:
            return 1.0 if rmse == 0 else 0.0
        
        nrci = 1 - (rmse / sigma_t)
        return nrci

def test_toggle_algebra():
    """Test the toggle algebra implementation."""
    from .bitfield import OffBit
    
    print("Testing Proper Toggle Algebra Implementation")
    print("=" * 50)
    
    algebra = ToggleAlgebra()
    
    # Create test OffBits
    offbit1 = OffBit(initial_state=0b101010101010101010101010, 
                     toggle_bias=const.TOGGLE_BIAS_QUANTUM)
    offbit2 = OffBit(initial_state=0b110011001100110011001100, 
                     toggle_bias=const.TOGGLE_BIAS_COSMOLOGICAL)
    
    print(f"OffBit 1 initial state: {bin(offbit1.get_state())}")
    print(f"OffBit 2 initial state: {bin(offbit2.get_state())}")
    print()
    
    # Test coherence calculation
    coherence = algebra.calculate_coherence(offbit1, offbit2, time_step=1)
    print(f"Coherence between OffBits: {coherence:.6f}")
    print()
    
    # Test resonance operation
    resonance_result = algebra.resonance_operation(offbit1, time_step=1, realm='biological')
    print(f"Resonance operation result: {bin(resonance_result)}")
    print()
    
    # Test entanglement operation
    entanglement_result = algebra.entanglement_operation(offbit1, offbit2, time_step=1)
    print(f"Entanglement operation result: {bin(entanglement_result)}")
    print()
    
    # Test NRCI calculation
    actual = [offbit1.get_state(), offbit2.get_state()]
    theoretical = [offbit1.get_state() + 100, offbit2.get_state() + 200]
    nrci = algebra.calculate_nrci(actual, theoretical)
    print(f"NRCI calculation: {nrci:.6f}")

if __name__ == "__main__":
    test_toggle_algebra()
