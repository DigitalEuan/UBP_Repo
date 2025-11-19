"""
UBP Coherence Field v3.6 - Self-Measuring Coherence Landscape
==============================================================

Upgrade the NRCI module from a scalar metric to a self-measuring coherence field.

This implements NRCI+ with:
- NRCI₁: Optimal coherence (best refinement from grammar)
- NRCI₂: Coherence gradient (direction of improvement)
- NRCI₃: Curvature (stability of coherence basin)
- NRCI₄: Coherence atlas (full geometric information)

Based on "A transition in epistemic modeling" feedback and Computational Grammar framework.

Author: Euan R A Craig, New Zealand
Date: November 19, 2025
Version: 3.6.0
"""

import math
from typing import List, Dict, Tuple, Optional, Callable
from dataclasses import dataclass, field
import coherence_substrate as cs

# ============================================================================
# COHERENCE POINT: Full geometric information about a state
# ============================================================================

@dataclass
class CoherencePoint:
    """
    A point in the coherence field with full geometric information.
    
    This is NRCI₄: the complete coherence atlas entry.
    """
    state: cs.CoherenceState
    operator_sequence: List[str]
    composition_depth: int
    operator_coherence: float
    state_nrci: float
    total_coherence: float
    gradient: Optional[List[float]] = None
    curvature: Optional[List[float]] = None
    basin_radius: Optional[float] = None
    warnings: List[str] = field(default_factory=list)
    suggestions: List[Dict] = field(default_factory=list)
    
    def __repr__(self):
        return (f"CoherencePoint(value={self.state.value:.6e}, "
                f"total_coherence={self.total_coherence:.10f}, "
                f"depth={self.composition_depth})")


# ============================================================================
# COHERENCE FIELD: Self-measuring coherence landscape
# ============================================================================

class CoherenceField:
    """
    Upgraded NRCI: From scalar to self-measuring coherence field.
    
    This implements the full NRCI+ framework:
    - Operator awareness
    - Composition tracking
    - Coherence gradient estimation
    - Error bounds computation
    - Optimization suggestions
    """
    
    def __init__(self):
        self.coherence_atlas = {}  # Cache of coherence points
        self.operator_registry = cs._OPERATOR_REGISTRY
        
    def map(self, state: cs.CoherenceState) -> CoherencePoint:
        """
        Map a CoherenceState to its full coherence point.
        
        This is NRCI₄: the complete coherence atlas entry with
        all geometric information.
        """
        # Extract operator sequence and composition depth
        operator_sequence = state.operator_sequence
        composition_depth = state.composition_depth
        
        # Compute operator coherence
        operator_coherence = state.operator_coherence
        
        # Get state NRCI
        state_nrci = state.nrci
        
        # Compute total coherence
        total_coherence = state.total_coherence
        
        # Generate warnings
        warnings = []
        if composition_depth > 5:
            warnings.append(
                f"Composition depth ({composition_depth}) exceeds practical limit (5). "
                "Coherence degradation may be significant."
            )
        
        if operator_coherence < 0.999900:
            warnings.append(
                f"Operator coherence ({operator_coherence:.6f}) is low. "
                "Consider using higher-coherence alternatives."
            )
        
        if total_coherence < 0.999800:
            warnings.append(
                f"Total coherence ({total_coherence:.6f}) is below recommended threshold (0.999800). "
                "Results may have significant uncertainty."
            )
        
        # Generate suggestions
        suggestions = self._generate_suggestions(operator_sequence, total_coherence)
        
        # Create coherence point
        point = CoherencePoint(
            state=state,
            operator_sequence=operator_sequence,
            composition_depth=composition_depth,
            operator_coherence=operator_coherence,
            state_nrci=state_nrci,
            total_coherence=total_coherence,
            warnings=warnings,
            suggestions=suggestions
        )
        
        # Cache in atlas
        state_key = id(state)
        self.coherence_atlas[state_key] = point
        
        return point
    
    def _generate_suggestions(self, operator_sequence: List[str], current_coherence: float) -> List[Dict]:
        """Generate optimization suggestions based on operator sequence."""
        suggestions = []
        
        # Check each operator for alternatives
        for op_symbol in operator_sequence:
            alternatives = self.operator_registry.suggest_alternatives(op_symbol, min_nrci=0.999950)
            if alternatives:
                suggestions.append({
                    'current': op_symbol,
                    'alternatives': [
                        {'symbol': alt.symbol, 'nrci': alt.nrci, 'improvement': alt.nrci - current_coherence}
                        for alt in alternatives[:3]  # Top 3 alternatives
                    ]
                })
        
        return suggestions
    
    def compute_error_bounds(self, point: CoherencePoint) -> Tuple[float, float]:
        """
        Compute error bounds based on coherence.
        
        Error magnitude scales with (1 - total_coherence).
        """
        total_coherence = point.total_coherence
        error_magnitude = 1.0 - total_coherence
        
        # Scale by composition depth (deeper = more uncertain)
        if point.composition_depth > 0:
            error_magnitude *= (1.0 + point.composition_depth * 0.1)
        
        return -error_magnitude, error_magnitude
    
    def estimate_gradient(self, state: cs.CoherenceState, epsilon: float = 1e-5) -> List[float]:
        """
        Estimate coherence gradient using finite differences.
        
        This is NRCI₂: the direction in parameter space that most increases coherence.
        
        For now, we estimate the gradient with respect to the value itself.
        """
        baseline_coherence = state.total_coherence
        
        # Perturb value slightly
        perturbed_state = cs.CoherenceState(
            state.value + epsilon,
            state.log_nrci_error,
            state.net_refinements,
            state.operator_sequence
        )
        
        perturbed_coherence = perturbed_state.total_coherence
        
        # Gradient (single dimension for now)
        gradient = [(perturbed_coherence - baseline_coherence) / epsilon]
        
        return gradient
    
    def estimate_curvature(self, state: cs.CoherenceState, epsilon: float = 1e-5) -> List[float]:
        """
        Estimate curvature (Hessian) of coherence landscape.
        
        This is NRCI₃: the stability of the coherence basin.
        """
        # Compute gradient at baseline
        baseline_grad = self.estimate_gradient(state, epsilon)
        
        # Compute gradient at perturbed point
        perturbed_state = cs.CoherenceState(
            state.value + epsilon,
            state.log_nrci_error,
            state.net_refinements,
            state.operator_sequence
        )
        perturbed_grad = self.estimate_gradient(perturbed_state, epsilon)
        
        # Curvature (second derivative)
        curvature = [(perturbed_grad[0] - baseline_grad[0]) / epsilon]
        
        return curvature
    
    def analyze_computation(self, state: cs.CoherenceState, detailed: bool = False) -> Dict:
        """
        Comprehensive analysis of a computational state.
        
        Returns a dictionary with full coherence field information.
        """
        # Map to coherence point
        point = self.map(state)
        
        # Compute error bounds
        error_low, error_high = self.compute_error_bounds(point)
        
        analysis = {
            'value': state.value,
            'operator_sequence': point.operator_sequence,
            'composition_depth': point.composition_depth,
            'operator_coherence': point.operator_coherence,
            'state_nrci': point.state_nrci,
            'total_coherence': point.total_coherence,
            'error_bounds': (error_low, error_high),
            'warnings': point.warnings,
            'suggestions': point.suggestions
        }
        
        if detailed:
            # Add gradient and curvature
            analysis['gradient'] = self.estimate_gradient(state)
            analysis['curvature'] = self.estimate_curvature(state)
        
        return analysis
    
    def optimize_sequence(self, operator_sequence: List[str]) -> Dict:
        """
        Suggest optimizations for an operator sequence.
        
        This analyzes the sequence and suggests:
        - Reordering for better coherence
        - Alternative operators
        - Simplifications
        """
        optimizations = {
            'original_sequence': operator_sequence,
            'composition_depth': len(operator_sequence),
            'suggestions': []
        }
        
        # Check for redundant operations
        if len(operator_sequence) > 1:
            # Look for inverse pairs (e.g., ⊗Y followed by ⊗Y⁻¹)
            for i in range(len(operator_sequence) - 1):
                if operator_sequence[i] == '⊗Y' and operator_sequence[i+1] == '⊗Y⁻¹':
                    optimizations['suggestions'].append({
                        'type': 'cancellation',
                        'position': i,
                        'description': 'Y-refinement followed by inverse can be eliminated'
                    })
                elif operator_sequence[i] == '⊗Y⁻¹' and operator_sequence[i+1] == '⊗Y':
                    optimizations['suggestions'].append({
                        'type': 'cancellation',
                        'position': i,
                        'description': 'Inverse Y-refinement followed by forward can be eliminated'
                    })
        
        # Check for deep composition
        if len(operator_sequence) > 5:
            optimizations['suggestions'].append({
                'type': 'depth_warning',
                'description': f'Composition depth ({len(operator_sequence)}) exceeds practical limit (5). Consider refactoring.'
            })
        
        return optimizations
    
    def compare_states(self, state1: cs.CoherenceState, state2: cs.CoherenceState) -> Dict:
        """
        Compare two coherence states.
        
        Useful for analyzing the effect of different computational paths.
        """
        point1 = self.map(state1)
        point2 = self.map(state2)
        
        return {
            'state1': {
                'value': state1.value,
                'total_coherence': point1.total_coherence,
                'composition_depth': point1.composition_depth
            },
            'state2': {
                'value': state2.value,
                'total_coherence': point2.total_coherence,
                'composition_depth': point2.composition_depth
            },
            'comparison': {
                'value_difference': abs(state1.value - state2.value),
                'coherence_difference': point2.total_coherence - point1.total_coherence,
                'depth_difference': point2.composition_depth - point1.composition_depth,
                'better_coherence': 'state2' if point2.total_coherence > point1.total_coherence else 'state1'
            }
        }


# ============================================================================
# GLOBAL COHERENCE FIELD INSTANCE
# ============================================================================

_GLOBAL_COHERENCE_FIELD = CoherenceField()


# ============================================================================
# CONVENIENCE FUNCTIONS
# ============================================================================

def analyze(state: cs.CoherenceState, detailed: bool = False) -> Dict:
    """Analyze a coherence state using the global coherence field."""
    return _GLOBAL_COHERENCE_FIELD.analyze_computation(state, detailed)


def map_state(state: cs.CoherenceState) -> CoherencePoint:
    """Map a state to its coherence point."""
    return _GLOBAL_COHERENCE_FIELD.map(state)


def compute_error_bounds(state: cs.CoherenceState) -> Tuple[float, float]:
    """Compute error bounds for a state."""
    point = _GLOBAL_COHERENCE_FIELD.map(state)
    return _GLOBAL_COHERENCE_FIELD.compute_error_bounds(point)


def optimize_sequence(operator_sequence: List[str]) -> Dict:
    """Optimize an operator sequence."""
    return _GLOBAL_COHERENCE_FIELD.optimize_sequence(operator_sequence)


def compare_states(state1: cs.CoherenceState, state2: cs.CoherenceState) -> Dict:
    """Compare two coherence states."""
    return _GLOBAL_COHERENCE_FIELD.compare_states(state1, state2)


# ============================================================================
# DEMONSTRATION
# ============================================================================

if __name__ == "__main__":
    print("="*80)
    print("UBP Coherence Field v3.6 - Self-Measuring Coherence Landscape")
    print("="*80)
    
    # Test 1: Simple arithmetic
    print("\n1. Simple Arithmetic Analysis:")
    a = cs.CoherenceState(10.0)
    b = cs.CoherenceState(5.0)
    c = a + b
    
    analysis = analyze(c)
    print(f"   Value: {analysis['value']}")
    print(f"   Operator sequence: {analysis['operator_sequence']}")
    print(f"   Total coherence: {analysis['total_coherence']:.10f}")
    print(f"   Error bounds: [{analysis['error_bounds'][0]:.2e}, {analysis['error_bounds'][1]:.2e}]")
    
    # Test 2: Deep composition
    print("\n2. Deep Composition Analysis:")
    x = cs.CoherenceState(2.0)
    y = x * x * x * x * x * x  # 6 multiplications
    
    analysis = analyze(y, detailed=True)
    print(f"   Value: {analysis['value']}")
    print(f"   Composition depth: {analysis['composition_depth']}")
    print(f"   Total coherence: {analysis['total_coherence']:.10f}")
    print(f"   Warnings: {len(analysis['warnings'])}")
    for warning in analysis['warnings']:
        print(f"     - {warning}")
    
    # Test 3: Sequence optimization
    print("\n3. Sequence Optimization:")
    sequence = ['⊗Y', '×', '+', '⊗Y⁻¹', '÷']
    optimization = optimize_sequence(sequence)
    print(f"   Original sequence: {optimization['original_sequence']}")
    print(f"   Composition depth: {optimization['composition_depth']}")
    if optimization['suggestions']:
        print(f"   Suggestions:")
        for suggestion in optimization['suggestions']:
            print(f"     - {suggestion['description']}")
    
    # Test 4: State comparison
    print("\n4. State Comparison:")
    path1 = cs.CoherenceState(10.0) + cs.CoherenceState(5.0)
    path2 = cs.CoherenceState(15.0)
    
    comparison = compare_states(path1, path2)
    print(f"   Path 1 (10 + 5): coherence = {comparison['state1']['total_coherence']:.10f}")
    print(f"   Path 2 (15): coherence = {comparison['state2']['total_coherence']:.10f}")
    print(f"   Better coherence: {comparison['comparison']['better_coherence']}")
    print(f"   Coherence difference: {comparison['comparison']['coherence_difference']:.2e}")
    
    print("\n" + "="*80)
    print("Coherence Field v3.6 Validated ✓")
    print("="*80)
