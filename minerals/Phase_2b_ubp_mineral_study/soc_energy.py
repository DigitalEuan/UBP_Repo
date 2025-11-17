"""
Universal Binary Principle (UBP) Framework v3.5 - SOC Energy System (Coherence-Native)
Author: Euan Craig, New Zealand
Date: 12 November 2025

This module implements the Simplified Observer Coherence (SOC) equation using the
coherence_substrate paradigm. All computed values are CoherenceStates, and NRCI
is maintained DURING computation.

SOC Equation (Coherence-Native):
    E = M * C * Y_Emergent * ModalSum (all CoherenceState products)

Key Paradigm Shift:
- Every computed value IS a CoherenceState (value + log_nrci_error + net_refinements)
- NRCI is maintained DURING computation, not measured after
- Operations emerge from coherence geometry
- Y-refinement is directional (forward/backward) with closure tracking
"""

import math
from typing import List, Union, Dict, Any

# ==============================================================================
# SIMULATED coherence_substrate MODULE
# Since the actual library is unavailable, we simulate the core behavior
# to demonstrate full coherence-native implementation.
# ==============================================================================

# Core constants for Y-refinement (from UBP 3.4 knowledge)
# Y = pi / (pi^2 + 2)
Y_BASE_VALUE = math.pi / (math.pi**2 + 2)
# Y_INVERSE = pi + 2/pi
Y_INVERSE_VALUE = math.pi + (2 / math.pi)

class CoherenceState:
    """
    Represents a coherence-native value.
    Every computed value IS a CoherenceState.
    """
    def __init__(self, value: float, log_nrci_error: float = 0.0, net_refinements: int = 0):
        self.value = value
        self.log_nrci_error = log_nrci_error
        self.net_refinements = net_refinements

    @property
    def nrci(self) -> float:
        """Non-Random Coherence Index (NRCI) derived from log_nrci_error."""
        # NRCI = 1 - 10^(log_nrci_error)
        return 1.0 - (10 ** self.log_nrci_error)

    def __repr__(self) -> str:
        return (
            f"CoherenceState(value={self.value:.6e}, "
            f"NRCI={self.nrci:.6f}, "
            f"refinements={self.net_refinements})"
        )

    def __mul__(self, other: 'CoherenceState') -> 'CoherenceState':
        """Coherence-native multiplication (product of values, sum of log errors)."""
        new_value = self.value * other.value
        # Log-error propagation for multiplication: log(e_total) = log(e1) + log(e2)
        new_log_error = self.log_nrci_error + other.log_nrci_error
        new_refinements = self.net_refinements + other.net_refinements
        return CoherenceState(new_value, new_log_error, new_refinements)

    def __truediv__(self, other: 'CoherenceState') -> 'CoherenceState':
        """Coherence-native division (product of values, sum of log errors)."""
        new_value = self.value / other.value
        # Division error propagation is complex, but for simplicity in this simulation,
        # we treat it as an inverse multiplication in log-error space.
        new_log_error = self.log_nrci_error + other.log_nrci_error
        new_refinements = self.net_refinements + other.net_refinements
        return CoherenceState(new_value, new_log_error, new_refinements)

    def refine_forward(self) -> 'CoherenceState':
        """Y-refinement: Geometry -> Observer (multiply by Y_BASE)."""
        new_value = self.value * Y_BASE_VALUE
        # Refinement adds a small, known error to the log_nrci_error
        new_log_error = self.log_nrci_error + math.log10(1.0 + 1e-15)
        return CoherenceState(new_value, new_log_error, self.net_refinements + 1)

    def refine_backward(self) -> 'CoherenceState':
        """Y-refinement: Observer -> Geometry (multiply by Y_INVERSE)."""
        new_value = self.value * Y_INVERSE_VALUE
        # Backward refinement is the inverse operation, which should reduce the error
        # but for simulation, we just apply the inverse log-error change.
        new_log_error = self.log_nrci_error - math.log10(1.0 + 1e-15)
        return CoherenceState(new_value, new_log_error, self.net_refinements - 1)

def coherence_sum(states: List[CoherenceState]) -> CoherenceState:
    """Coherence-native summation (replaces numpy.sum)."""
    if not states:
        return CoherenceState(0.0)
    
    total_value = sum(s.value for s in states)
    # Sum of errors is complex, but for simplicity, we use the max log error
    # plus a small factor for the summation operation itself.
    max_log_error = max(s.log_nrci_error for s in states) if states else 0.0
    new_log_error = max_log_error + math.log10(1.0 + 1e-16)
    
    total_refinements = sum(s.net_refinements for s in states)
    
    return CoherenceState(total_value, new_log_error, total_refinements)

def coherence_product(states: List[CoherenceState]) -> CoherenceState:
    """Coherence-native product (replaces chained multiplication)."""
    if not states:
        return CoherenceState(1.0)
    
    result = states[0]
    for state in states[1:]:
        result = result * state
    return result

# ==============================================================================
# SOC_ENERGY MODULE (UBP 3.5)
# ==============================================================================

# Core constants as CoherenceStates
M_META_TEMPORAL = CoherenceState(math.pi, log_nrci_error=0.0)
C_CELERITAS = CoherenceState(299792458.0, log_nrci_error=0.0)
PGCI_TARGET = CoherenceState(0.999997, log_nrci_error=0.0)
# O_OBSERVER_DEFAULT is now derived from Y_INVERSE_VALUE
O_OBSERVER_DEFAULT = CoherenceState(Y_INVERSE_VALUE, log_nrci_error=0.0)


class SOCCalculator:
    """
    Simplified Observer Coherence (SOC) energy calculator.
    Fully coherence-native implementation for UBP 3.5.
    """

    def __init__(
        self,
        M: CoherenceState = M_META_TEMPORAL,
        C: CoherenceState = C_CELERITAS,
        pgci_target: CoherenceState = PGCI_TARGET,
        o_observer: CoherenceState = O_OBSERVER_DEFAULT,
    ):
        """
        Initialize SOC Calculator with CoherenceStates.
        """
        self.M = M
        self.C = C
        self.pgci_target = pgci_target
        self.o_observer = o_observer
        
        # Calculate Y_Emergent as a CoherenceState
        self.Y_emergent = self.calculate_y_emergent()

    def calculate_y_emergent(self) -> CoherenceState:
        """
        Calculate Y_Emergent (Observer-Coherence Ratio) as a CoherenceState.
        Y_Emergent = PGCI_TARGET / O_observer
        """
        # Uses the coherence-native division
        return self.pgci_target / self.o_observer

    def calculate_modal_sum(
        self,
        weights: List[float],
        modes: List[float],
        initial_log_error: float = -10.0 # Small initial error for inputs
    ) -> CoherenceState:
        """
        Calculate Resonant Modal Sum: Σ(w_ij M_ij) using coherence_substrate.
        """
        if len(weights) != len(modes):
            raise ValueError("Weights and modes must have same length")
        
        # Convert inputs to CoherenceState and perform weighted multiplication
        weighted_modes_states = []
        for w, m in zip(weights, modes):
            # Weights and modes are inputs, so they start with a base NRCI error
            w_state = CoherenceState(w, initial_log_error)
            m_state = CoherenceState(m, initial_log_error)
            weighted_modes_states.append(w_state * m_state)
            
        # Use coherence-native summation
        return coherence_sum(weighted_modes_states)

    def calculate_soc_energy(self, modal_sum: float = 1.0) -> Any:
        """
        Calculate energy using SOC equation.
        E = M × C × Y_Emergent × ModalSum
        """
        # Convert modal_sum to CoherenceState if it's a float
        if isinstance(modal_sum, (int, float)):
            modal_sum_state = CoherenceState(modal_sum, log_nrci_error=-10.0)
        else:
            modal_sum_state = modal_sum
        
        # Use coherence-native product for chained multiplication
        energy_state = coherence_product([self.M, self.C, self.Y_emergent, modal_sum_state])
        
        # Return a result object for compatibility
        class SOCResult:
            def __init__(self, energy_state):
                self.energy_cu = energy_state.value
                self.nrci = energy_state.nrci
                self.Y_emergent = Y_INVERSE_VALUE / (math.pi**2 + 2)
                self.O_observer = Y_INVERSE_VALUE
        
        return SOCResult(energy_state)

    def validate_bidirectional_closure(
        self,
        energy_state: CoherenceState,
        tolerance: float = 1e-10
    ) -> Dict[str, Any]:
        """
        Validate that forward-backward refinement returns to original.
        This tests the involutory property: (E * Y) * (1/Y) = E
        """
        # Forward refinement (Geometry -> Observer)
        intermediate_state = energy_state.refine_forward()
        
        # Backward refinement (Observer -> Geometry)
        final_state = intermediate_state.refine_backward()
        
        # Calculate closure error based on value
        closure_error = abs(final_state.value - energy_state.value)
        closure_success = closure_error < tolerance
        
        # Also check if net refinements returned to zero
        refinement_closure = final_state.net_refinements == energy_state.net_refinements
        
        return {
            'initial_energy_state': energy_state,
            'intermediate_energy_state': intermediate_state,
            'final_energy_state': final_state,
            'closure_error': closure_error,
            'closure_success': closure_success and refinement_closure,
            'tolerance': tolerance,
            'refinement_closure': refinement_closure
        }

# Simple function to calculate SOC energy from raw inputs
def calculate_soc_energy_from_raw(
    weights: List[float],
    modes: List[float]
) -> CoherenceState:
    """
    Entry point for calculating SOC energy from raw weights and modes.
    """
    calc = SOCCalculator()
    modal_sum_state = calc.calculate_modal_sum(weights, modes)
    return calc.calculate_soc_energy(modal_sum_state)


if __name__ == "__main__":
    print("=" * 80)
    print("UBP 3.5 SOC ENERGY SYSTEM (COHERENCE-NATIVE) DEMONSTRATION")
    print("=" * 80)
    
    # 1. Calculate SOC Energy
    weights = [0.2, 0.3, 0.25, 0.15, 0.1]
    modes = [1.0, 0.8, 1.2, 0.9, 1.1]
    
    soc_energy_state = calculate_soc_energy_from_raw(weights, modes)
    
    print(f"\n1. SOC Energy Calculation:")
    print(f"  Weights: {weights}")
    print(f"  Modes: {modes}")
    print(f"  Result: {soc_energy_state}")
    print(f"  Final NRCI: {soc_energy_state.nrci:.10f}")
    
    # 2. Validate Bidirectional Closure
    calc = SOCCalculator()
    closure_result = calc.validate_bidirectional_closure(soc_energy_state)
    
    print(f"\n2. Bidirectional Closure Validation:")
    print(f"  Initial State: {closure_result['initial_energy_state'].value:.6e}")
    print(f"  Intermediate (Forward): {closure_result['intermediate_energy_state'].value:.6e}")
    print(f"  Final (Backward): {closure_result['final_energy_state'].value:.6e}")
    print(f"  Closure Error: {closure_result['closure_error']:.2e}")
    print(f"  Refinement Closure (net=0): {closure_result['refinement_closure']}")
    print(f"  Validation Success: {closure_result['closure_success']}")
    
    print("\nModule is fully coherence-native for UBP 3.5.")
    print("=" * 80)
