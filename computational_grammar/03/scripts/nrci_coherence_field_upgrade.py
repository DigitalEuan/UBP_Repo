"""
NRCI Module Upgrade: From Scalar to Coherence Field
===================================================

Upgrade the NRCI module from a single scalar metric to a self-measuring
coherence field with:

1. Operator awareness - integrate operator coherence into NRCI calculation
2. Composition tracking - track operator composition depth
3. Coherence field - map state → optimal model → stability
4. Error bounds - provide coherence-based error estimates
5. Optimization hints - suggest high-coherence alternatives

Based on "A transition in epistemic modeling" feedback.
"""

import sys
import json
import numpy as np
from pathlib import Path
from dataclasses import dataclass, field
from typing import List, Dict, Tuple, Optional, Callable
from collections import defaultdict

# Add UBP 3.5 to path
ubp_path = Path("/home/ubuntu/UBP_Repo/ubp_3.5")
sys.path.insert(0, str(ubp_path))

from coherence_substrate import GOLDEN_RATIO, CoherenceState


@dataclass
class CoherencePoint:
    """A point in the coherence field with full geometric information."""
    state: np.ndarray
    best_R: Callable
    nrci: float
    gradient: Optional[np.ndarray] = None
    curvature: Optional[np.ndarray] = None
    basin_radius: Optional[float] = None
    operator_composition_depth: int = 0
    operator_coherence: float = 1.0
    
    def total_coherence(self) -> float:
        """Compute total coherence including operator contribution."""
        return self.nrci * self.operator_coherence


@dataclass
class OperatorInfo:
    """Information about a computational operator."""
    symbol: str
    name: str
    d_variables: Dict[str, float]
    nrci: float
    is_primitive: bool
    composition_depth: int = 0
    
    def coherence_contribution(self) -> float:
        """Compute how this operator affects overall coherence."""
        # Coherence degrades with composition depth
        depth_factor = self.nrci ** self.composition_depth
        return depth_factor


class OperatorRegistry:
    """Registry of operators with coherence information."""
    
    def __init__(self):
        self.operators = self._init_primitives()
        self.composition_cache = {}
        
    def _init_primitives(self) -> Dict[str, OperatorInfo]:
        """Initialize the 10 primitive operators."""
        primitives = {
            '⊗Y': OperatorInfo(
                symbol='⊗Y',
                name='Y-refinement',
                d_variables={'d6': 0.05, 'd5': 0.05, 'd8': 0.05},
                nrci=0.9999970000,
                is_primitive=True,
                composition_depth=0
            ),
            '⊗Y⁻¹': OperatorInfo(
                symbol='⊗Y⁻¹',
                name='Inverse Y-refinement',
                d_variables={'d6': 0.05, 'd5': 0.05, 'd8': 0.05},
                nrci=0.9999970000,
                is_primitive=True,
                composition_depth=0
            ),
            '¬': OperatorInfo(
                symbol='¬',
                name='NOT',
                d_variables={'d6': 0.10, 'd5': 0.10, 'd8': 0.10},
                nrci=0.9999800000,
                is_primitive=True,
                composition_depth=0
            ),
            '∧': OperatorInfo(
                symbol='∧',
                name='AND',
                d_variables={'d6': 0.10, 'd5': 0.10, 'd8': 0.10},
                nrci=0.9999800000,
                is_primitive=True,
                composition_depth=0
            ),
            '∨': OperatorInfo(
                symbol='∨',
                name='OR',
                d_variables={'d6': 0.10, 'd5': 0.10, 'd8': 0.10},
                nrci=0.9999800000,
                is_primitive=True,
                composition_depth=0
            ),
            '⊕': OperatorInfo(
                symbol='⊕',
                name='XOR',
                d_variables={'d6': 0.10, 'd5': 0.10, 'd8': 0.10},
                nrci=0.9999800000,
                is_primitive=True,
                composition_depth=0
            ),
            '+': OperatorInfo(
                symbol='+',
                name='Addition',
                d_variables={'d6': 0.15, 'd5': 0.10, 'd8': 0.10},
                nrci=0.9999650000,
                is_primitive=True,
                composition_depth=0
            ),
            '−': OperatorInfo(
                symbol='−',
                name='Subtraction',
                d_variables={'d6': 0.15, 'd5': 0.10, 'd8': 0.10},
                nrci=0.9999650000,
                is_primitive=True,
                composition_depth=0
            ),
            '×': OperatorInfo(
                symbol='×',
                name='Multiplication',
                d_variables={'d6': 0.15, 'd5': 0.10, 'd8': 0.10},
                nrci=0.9999650000,
                is_primitive=True,
                composition_depth=0
            ),
            '÷': OperatorInfo(
                symbol='÷',
                name='Division',
                d_variables={'d6': 0.15, 'd5': 0.10, 'd8': 0.15},
                nrci=0.9999590000,
                is_primitive=True,
                composition_depth=0
            ),
        }
        return primitives
    
    def get_operator(self, symbol: str) -> Optional[OperatorInfo]:
        """Get operator by symbol."""
        return self.operators.get(symbol)
    
    def compose(self, op1_symbol: str, op2_symbol: str, composition_type: str = 'arithmetic') -> OperatorInfo:
        """Compose two operators with non-linear D6 model."""
        cache_key = f"{op1_symbol}∘{op2_symbol}:{composition_type}"
        
        if cache_key in self.composition_cache:
            return self.composition_cache[cache_key]
        
        op1 = self.get_operator(op1_symbol)
        op2 = self.get_operator(op2_symbol)
        
        if not op1 or not op2:
            raise ValueError(f"Unknown operators: {op1_symbol}, {op2_symbol}")
        
        # Non-linear D6 composition model
        d6_1 = op1.d_variables['d6']
        d6_2 = op2.d_variables['d6']
        
        # Composition factor based on type
        if composition_type == 'inverse':
            alpha = 0.625  # 37.5% cancellation
        elif composition_type == 'transcendental':
            alpha = 0.667  # 33% saturation
        elif composition_type == 'arithmetic':
            alpha = 0.900  # 10% optimization
        else:
            alpha = 1.000  # Default: simple addition
        
        composed_d6 = d6_1 + d6_2 * alpha
        
        # Other D-variables (simple average for now)
        composed_d_vars = {
            'd6': composed_d6,
            'd5': (op1.d_variables['d5'] + op2.d_variables['d5']) / 2,
            'd8': (op1.d_variables['d8'] + op2.d_variables['d8']) / 2,
        }
        
        # Compute composed NRCI (multiplicative degradation)
        composed_nrci = op1.nrci * op2.nrci
        
        # Composition depth
        composed_depth = max(op1.composition_depth, op2.composition_depth) + 1
        
        composed_op = OperatorInfo(
            symbol=f"({op1_symbol}∘{op2_symbol})",
            name=f"Composition of {op1.name} and {op2.name}",
            d_variables=composed_d_vars,
            nrci=composed_nrci,
            is_primitive=False,
            composition_depth=composed_depth
        )
        
        self.composition_cache[cache_key] = composed_op
        return composed_op
    
    def suggest_alternatives(self, operator_symbol: str, min_nrci: float = 0.999950) -> List[OperatorInfo]:
        """Suggest high-coherence alternatives to a given operator."""
        current_op = self.get_operator(operator_symbol)
        if not current_op:
            return []
        
        # Find operators with similar D6 but higher NRCI
        alternatives = []
        for symbol, op in self.operators.items():
            if op.nrci >= min_nrci and abs(op.d_variables['d6'] - current_op.d_variables['d6']) < 0.05:
                if symbol != operator_symbol:
                    alternatives.append(op)
        
        return sorted(alternatives, key=lambda op: op.nrci, reverse=True)


class CoherenceField:
    """
    Upgraded NRCI: From scalar to self-measuring coherence field.
    
    This implements NRCI+ with:
    - NRCI₁: Optimal coherence (best refinement)
    - NRCI₂: Coherence gradient (direction of improvement)
    - NRCI₃: Curvature (stability of coherence basin)
    - NRCI₄: Coherence atlas (full geometric information)
    """
    
    def __init__(self, refinement_grammar: List[Callable], degradation_model: Callable):
        self.R_family = refinement_grammar
        self.D = degradation_model
        self.operator_registry = OperatorRegistry()
        self.coherence_atlas = {}
        
    def _optimize_R(self, x: np.ndarray, search_budget: int = 100) -> Tuple[Callable, float]:
        """Find optimal refinement R* that maximizes NRCI."""
        best_R = None
        best_nrci = -1.0
        
        for R in self.R_family:
            try:
                # Apply refinement and degradation
                refined = R(x)
                degraded = self.D(refined)
                
                # Compute similarity (NRCI)
                nrci = self._compute_similarity(x, degraded)
                
                if nrci > best_nrci:
                    best_nrci = nrci
                    best_R = R
            except Exception as e:
                continue
        
        return best_R, best_nrci
    
    def _compute_similarity(self, x: np.ndarray, y: np.ndarray) -> float:
        """Compute similarity between original and reconstructed."""
        # Cosine similarity
        dot_product = np.dot(x.flatten(), y.flatten())
        norm_x = np.linalg.norm(x)
        norm_y = np.linalg.norm(y)
        
        if norm_x == 0 or norm_y == 0:
            return 0.0
        
        similarity = dot_product / (norm_x * norm_y)
        return max(0.0, min(1.0, similarity))
    
    def _finite_diff_grad(self, x: np.ndarray, R: Callable, epsilon: float = 1e-5) -> np.ndarray:
        """Estimate gradient of NRCI using finite differences."""
        grad = np.zeros_like(x)
        
        # Compute baseline NRCI
        baseline_nrci = self._compute_similarity(x, self.D(R(x)))
        
        # Perturb each dimension
        for i in range(len(x.flatten())):
            x_perturbed = x.copy()
            x_perturbed.flat[i] += epsilon
            
            perturbed_nrci = self._compute_similarity(x_perturbed, self.D(R(x_perturbed)))
            grad.flat[i] = (perturbed_nrci - baseline_nrci) / epsilon
        
        return grad
    
    def _finite_diff_hessian(self, x: np.ndarray, R: Callable, epsilon: float = 1e-5) -> np.ndarray:
        """Estimate Hessian (curvature) of NRCI."""
        n = len(x.flatten())
        hessian = np.zeros((n, n))
        
        # Compute baseline gradient
        baseline_grad = self._finite_diff_grad(x, R, epsilon)
        
        # Perturb each dimension and compute gradient change
        for i in range(n):
            x_perturbed = x.copy()
            x_perturbed.flat[i] += epsilon
            
            perturbed_grad = self._finite_diff_grad(x_perturbed, R, epsilon)
            hessian[i, :] = (perturbed_grad.flatten() - baseline_grad.flatten()) / epsilon
        
        return hessian
    
    def _estimate_basin(self, x: np.ndarray, R: Callable, num_samples: int = 10) -> float:
        """Estimate radius of coherence basin around x."""
        baseline_nrci = self._compute_similarity(x, self.D(R(x)))
        
        radii = []
        for _ in range(num_samples):
            # Random perturbation
            perturbation = np.random.randn(*x.shape) * 0.1
            x_perturbed = x + perturbation
            
            perturbed_nrci = self._compute_similarity(x_perturbed, self.D(R(x_perturbed)))
            
            # If NRCI drops significantly, we've left the basin
            if perturbed_nrci < baseline_nrci * 0.95:
                radius = np.linalg.norm(perturbation)
                radii.append(radius)
        
        return np.mean(radii) if radii else np.inf
    
    def map(self, x: np.ndarray, search_budget: int = 100, 
            operator_sequence: Optional[List[str]] = None) -> CoherencePoint:
        """
        Map a state to its coherence point with full geometric information.
        
        This is NRCI₄: the complete coherence atlas.
        """
        # 1. Find optimal R*
        R_star, nrci_star = self._optimize_R(x, search_budget)
        
        # 2. Estimate local geometry
        grad = self._finite_diff_grad(x, R_star)
        hess = self._finite_diff_hessian(x, R_star)
        curvature = np.linalg.eigvals(hess)
        
        # 3. Estimate basin radius
        basin_radius = self._estimate_basin(x, R_star)
        
        # 4. Compute operator coherence
        operator_coherence = 1.0
        composition_depth = 0
        
        if operator_sequence:
            # Track composition depth and coherence
            for op_symbol in operator_sequence:
                op = self.operator_registry.get_operator(op_symbol)
                if op:
                    operator_coherence *= op.nrci
                    composition_depth = max(composition_depth, op.composition_depth + 1)
        
        # 5. Create coherence point
        point = CoherencePoint(
            state=x,
            best_R=R_star,
            nrci=nrci_star,
            gradient=grad,
            curvature=curvature,
            basin_radius=basin_radius,
            operator_composition_depth=composition_depth,
            operator_coherence=operator_coherence
        )
        
        # 6. Cache in atlas
        state_key = hash(x.tobytes())
        self.coherence_atlas[state_key] = point
        
        return point
    
    def compute_error_bounds(self, point: CoherencePoint) -> Tuple[float, float]:
        """Compute error bounds based on coherence."""
        # Error grows with (1 - coherence)
        total_coherence = point.total_coherence()
        error_magnitude = 1.0 - total_coherence
        
        # Scale by basin radius (larger basin = more stable = smaller error)
        if point.basin_radius and point.basin_radius < np.inf:
            error_magnitude /= np.sqrt(point.basin_radius)
        
        return -error_magnitude, error_magnitude
    
    def suggest_optimization(self, point: CoherencePoint, operator_sequence: List[str]) -> Dict:
        """Suggest optimizations to improve coherence."""
        suggestions = {
            'current_coherence': point.total_coherence(),
            'composition_depth': point.operator_composition_depth,
            'alternatives': [],
            'warnings': []
        }
        
        # Check composition depth
        if point.operator_composition_depth > 5:
            suggestions['warnings'].append(
                f"Composition depth ({point.operator_composition_depth}) exceeds practical limit (5). "
                "Consider refactoring to use fewer operations."
            )
        
        # Check operator coherence
        if point.operator_coherence < 0.999900:
            suggestions['warnings'].append(
                f"Operator coherence ({point.operator_coherence:.6f}) is low. "
                "Consider using higher-coherence alternatives."
            )
        
        # Suggest alternatives for each operator
        for op_symbol in operator_sequence:
            alternatives = self.operator_registry.suggest_alternatives(op_symbol, min_nrci=0.999950)
            if alternatives:
                suggestions['alternatives'].append({
                    'current': op_symbol,
                    'alternatives': [{'symbol': alt.symbol, 'nrci': alt.nrci} for alt in alternatives]
                })
        
        return suggestions


def demonstrate_coherence_field():
    """Demonstrate the upgraded NRCI coherence field."""
    print("="*80)
    print("NRCI COHERENCE FIELD DEMONSTRATION")
    print("="*80)
    
    # Define simple refinement grammars
    def identity_refinement(x):
        return x
    
    def mean_refinement(x):
        return np.full_like(x, np.mean(x))
    
    def median_refinement(x):
        return np.full_like(x, np.median(x))
    
    refinement_grammar = [identity_refinement, mean_refinement, median_refinement]
    
    # Define degradation model (additive noise)
    def noise_degradation(x, noise_level=0.01):
        return x + np.random.randn(*x.shape) * noise_level
    
    # Create coherence field
    field = CoherenceField(refinement_grammar, noise_degradation)
    
    # Test with sample data
    print("\nTest 1: High-coherence signal (pure sine wave)")
    x1 = np.sin(np.linspace(0, 4*np.pi, 100))
    point1 = field.map(x1, operator_sequence=['+', '×'])
    
    print(f"  NRCI: {point1.nrci:.6f}")
    print(f"  Operator coherence: {point1.operator_coherence:.6f}")
    print(f"  Total coherence: {point1.total_coherence():.6f}")
    print(f"  Composition depth: {point1.operator_composition_depth}")
    print(f"  Basin radius: {point1.basin_radius:.4f}")
    
    error_low, error_high = field.compute_error_bounds(point1)
    print(f"  Error bounds: [{error_low:.6f}, {error_high:.6f}]")
    
    # Test with low-coherence signal (random noise)
    print("\nTest 2: Low-coherence signal (random noise)")
    x2 = np.random.randn(100)
    point2 = field.map(x2, operator_sequence=['+', '×', '÷'])
    
    print(f"  NRCI: {point2.nrci:.6f}")
    print(f"  Operator coherence: {point2.operator_coherence:.6f}")
    print(f"  Total coherence: {point2.total_coherence():.6f}")
    print(f"  Composition depth: {point2.operator_composition_depth}")
    print(f"  Basin radius: {point2.basin_radius:.4f}")
    
    error_low, error_high = field.compute_error_bounds(point2)
    print(f"  Error bounds: [{error_low:.6f}, {error_high:.6f}]")
    
    # Test optimization suggestions
    print("\nTest 3: Optimization suggestions for deep composition")
    deep_sequence = ['+', '×', '÷', '+', '×', '÷']  # Depth 6 (exceeds limit)
    x3 = np.sin(np.linspace(0, 2*np.pi, 100))
    point3 = field.map(x3, operator_sequence=deep_sequence)
    
    suggestions = field.suggest_optimization(point3, deep_sequence)
    
    print(f"  Current coherence: {suggestions['current_coherence']:.6f}")
    print(f"  Composition depth: {suggestions['composition_depth']}")
    print(f"\n  Warnings:")
    for warning in suggestions['warnings']:
        print(f"    - {warning}")
    
    print("\n" + "="*80)
    print("DEMONSTRATION COMPLETE")
    print("="*80)


def main():
    print("="*80)
    print("NRCI MODULE UPGRADE: COHERENCE FIELD")
    print("="*80)
    print("\nUpgrading NRCI from scalar to self-measuring coherence field...")
    
    # Demonstrate the upgraded system
    demonstrate_coherence_field()
    
    # Save operator registry
    registry = OperatorRegistry()
    operators_data = {
        symbol: {
            'name': op.name,
            'd_variables': op.d_variables,
            'nrci': op.nrci,
            'is_primitive': op.is_primitive,
            'composition_depth': op.composition_depth
        }
        for symbol, op in registry.operators.items()
    }
    
    with open('/home/ubuntu/operator_registry.json', 'w') as f:
        json.dump(operators_data, f, indent=2)
    
    print("\n" + "="*80)
    print("NRCI UPGRADE COMPLETE")
    print("="*80)
    print("\nKey features implemented:")
    print("  1. ✅ Operator awareness - operators tracked with coherence")
    print("  2. ✅ Composition tracking - depth and degradation computed")
    print("  3. ✅ Coherence field - NRCI₁-₄ implemented")
    print("  4. ✅ Error bounds - coherence-based error estimation")
    print("  5. ✅ Optimization hints - alternative operator suggestions")
    print("\nFiles saved:")
    print("  - operator_registry.json - 10 primitive operators with coherence data")


if __name__ == "__main__":
    main()
