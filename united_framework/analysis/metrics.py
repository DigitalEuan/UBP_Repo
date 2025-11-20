"""
Metrics and Analysis Utilities for Local Excitations Framework
================================================================

Provides tools for analyzing NRCI, coherence preservation, and validation
of the unified framework predictions.

Author: Euan Craig & Manus AI
Date: November 21, 2025
"""

import math
from typing import List, Tuple, Dict
import sys
sys.path.insert(0, '..')
from coherence_substrate import CoherenceState


class CoherenceAnalyzer:
    """Analyze coherence properties of computational experiments."""
    
    def __init__(self):
        self.history = []
        
    def record(self, state: CoherenceState, label: str = ""):
        """Record a coherence state for later analysis."""
        self.history.append({
            'label': label,
            'value': state.value,
            'nrci': state.nrci,
            'net_refinements': state.net_refinements,
            'composition_depth': state.composition_depth,
            'operator_sequence': state.operator_sequence.copy()
        })
    
    def get_nrci_series(self) -> List[float]:
        """Get time series of NRCI values."""
        return [entry['nrci'] for entry in self.history]
    
    def get_min_nrci(self) -> float:
        """Get minimum NRCI across all recorded states."""
        if not self.history:
            return 1.0
        return min(entry['nrci'] for entry in self.history)
    
    def get_mean_nrci(self) -> float:
        """Get mean NRCI across all recorded states."""
        if not self.history:
            return 1.0
        nrcis = [entry['nrci'] for entry in self.history]
        return sum(nrcis) / len(nrcis)
    
    def coherence_degradation_rate(self) -> float:
        """
        Calculate the rate of coherence degradation per operation.
        
        Returns the average log-error increase per computational step.
        """
        if len(self.history) < 2:
            return 0.0
        
        nrcis = self.get_nrci_series()
        log_errors = [-math.log(1 - nrci) if nrci < 1.0 else 0.0 for nrci in nrcis]
        
        # Linear regression on log-error vs step
        n = len(log_errors)
        x_mean = (n - 1) / 2
        y_mean = sum(log_errors) / n
        
        numerator = sum((i - x_mean) * (log_errors[i] - y_mean) for i in range(n))
        denominator = sum((i - x_mean) ** 2 for i in range(n))
        
        if denominator == 0:
            return 0.0
        
        return numerator / denominator
    
    def verify_closure(self) -> Tuple[bool, float]:
        """
        Verify bidirectional closure: net refinements should return to zero.
        
        Returns (is_closed, max_net_refinements)
        """
        if not self.history:
            return True, 0.0
        
        final_net_ref = self.history[-1]['net_refinements']
        max_net_ref = max(abs(entry['net_refinements']) for entry in self.history)
        
        return abs(final_net_ref) < 1e-10, max_net_ref
    
    def operator_complexity_analysis(self) -> Dict[str, int]:
        """
        Analyze operator usage patterns.
        
        Returns a dictionary of operator symbols and their usage counts.
        """
        operator_counts = {}
        
        for entry in self.history:
            for op in entry['operator_sequence']:
                operator_counts[op] = operator_counts.get(op, 0) + 1
        
        return operator_counts
    
    def generate_report(self) -> str:
        """Generate a comprehensive analysis report."""
        if not self.history:
            return "No data recorded."
        
        min_nrci = self.get_min_nrci()
        mean_nrci = self.get_mean_nrci()
        deg_rate = self.coherence_degradation_rate()
        is_closed, max_ref = self.verify_closure()
        op_counts = self.operator_complexity_analysis()
        
        report = []
        report.append("=" * 70)
        report.append("COHERENCE ANALYSIS REPORT")
        report.append("=" * 70)
        report.append(f"Total states recorded: {len(self.history)}")
        report.append(f"Minimum NRCI: {min_nrci:.12f}")
        report.append(f"Mean NRCI: {mean_nrci:.12f}")
        report.append(f"Coherence degradation rate: {deg_rate:.2e} log-error/step")
        report.append(f"Closure verified: {is_closed} (max net refinements: {max_ref})")
        report.append("")
        report.append("Operator Usage:")
        for op, count in sorted(op_counts.items(), key=lambda x: x[1], reverse=True):
            report.append(f"  {op}: {count} times")
        report.append("=" * 70)
        
        return "\n".join(report)
    
    def save_log(self, filepath: str):
        """Save detailed log to file."""
        with open(filepath, 'w') as f:
            f.write(self.generate_report())
            f.write("\n\nDetailed History:\n")
            f.write("-" * 70 + "\n")
            for i, entry in enumerate(self.history):
                f.write(f"Step {i}: {entry['label']}\n")
                f.write(f"  Value: {entry['value']:.6e}\n")
                f.write(f"  NRCI: {entry['nrci']:.12f}\n")
                f.write(f"  Net refinements: {entry['net_refinements']}\n")
                f.write(f"  Composition depth: {entry['composition_depth']}\n")
                f.write(f"  Operators: {' → '.join(entry['operator_sequence'][-5:])}\n")
                f.write("\n")


def compare_with_qm(ubp_result: float, qm_result: float, tolerance: float = 1e-6) -> Dict[str, any]:
    """
    Compare UBP computational result with standard quantum mechanics prediction.
    
    Args:
        ubp_result: Result from UBP computation
        qm_result: Expected result from standard QM
        tolerance: Acceptable relative error
    
    Returns:
        Dictionary with comparison metrics
    """
    abs_error = abs(ubp_result - qm_result)
    rel_error = abs_error / abs(qm_result) if qm_result != 0 else abs_error
    
    return {
        'ubp_result': ubp_result,
        'qm_result': qm_result,
        'absolute_error': abs_error,
        'relative_error': rel_error,
        'within_tolerance': rel_error < tolerance,
        'agreement_percentage': (1 - rel_error) * 100
    }


def calculate_bell_correlation(state_a: CoherenceState, state_b: CoherenceState,
                               angle_a: float, angle_b: float) -> float:
    """
    Calculate Bell-type correlation coefficient for entangled states.
    
    This is a simplified model where correlation depends on the coherence
    field coupling and measurement angles.
    
    Args:
        state_a: First entangled state
        state_b: Second entangled state
        angle_a: Measurement angle for state A (radians)
        angle_b: Measurement angle for state B (radians)
    
    Returns:
        Correlation coefficient E(a,b)
    """
    # Correlation strength from coherence coupling
    coherence_coupling = math.sqrt(state_a.nrci * state_b.nrci)
    
    # Angular dependence (quantum mechanical prediction: -cos(angle_diff))
    angle_diff = angle_a - angle_b
    correlation = -coherence_coupling * math.cos(angle_diff)
    
    return correlation


def verify_supercoherence(state: CoherenceState, threshold: float = 0.999999) -> bool:
    """
    Verify that a state is in the supercoherent regime.
    
    Args:
        state: CoherenceState to check
        threshold: Minimum NRCI for supercoherence
    
    Returns:
        True if state is supercoherent
    """
    return state.nrci >= threshold
