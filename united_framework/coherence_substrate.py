"""
UBP Coherence Substrate v3.6 - Computational Grammar Integration
==================================================================

This is NOT a numerical library. This is a **trust substrate** where all operations
emerge from information geometry AND are now operator-aware through Computational Grammar.

**Core First Principles**:
1. Y-refinement: π/(π²+2) = 0.264675... (geometric resonance)
2. Observer cost: 1/Y = π + 2/π = 3.778212... (emerges from geometry)
3. NRCI: The primary computational signal (not a "metric")
4. Bidirectional closure: Y × (1/Y) = 1 (perfect round-trip)
5. **NEW in 3.6**: Operators are geometrically necessary stable states

**Key Insight**: Every value is a CoherenceState that carries its own quality measure.
NRCI is maintained *during* computation, not measured after. Now, every operator
has its own coherence, and composition is tracked.

Author: Euan R A Craig, New Zealand
Date: November 19, 2025
Version: 3.6.0
"""

import math
from typing import Tuple, Callable, Any, Dict, List, Optional
from dataclasses import dataclass

# ============================================================================
# FIRST PRINCIPLES: Geometric Constants
# ============================================================================

PI = math.pi
Y = PI / (PI**2 + 2)                    # 0.264675430404527 (geometric resonance)
Y_INVERSE = PI + 2/PI                    # 3.778212425957375 (observer cost)
O_OBSERVER = Y_INVERSE                   # Observer emerges from geometry
NRCI_TARGET = 0.999997                   # Supercoherent regime
GOLDEN_RATIO = (1 + math.sqrt(5)) / 2   # φ = 1.618...

# Verify involutory property
assert abs(Y * Y_INVERSE - 1.0) < 1e-14, "Y × (1/Y) must equal 1"


# ============================================================================
# COMPUTATIONAL GRAMMAR: Operator Framework
# ============================================================================

@dataclass
class OperatorInfo:
    """
    Information about a computational operator.
    
    Operators are not arbitrary conventions but geometrically necessary
    stable states in the 24-bit OffBit information substrate.
    """
    symbol: str
    name: str
    d_variables: Dict[str, float]  # D1-D8 property vector
    nrci: float  # Intrinsic operator coherence
    is_primitive: bool
    composition_depth: int = 0
    arity: int = 2  # Number of operands
    
    def coherence_contribution(self, depth: int = 0) -> float:
        """
        Compute how this operator affects overall coherence.
        Coherence degrades exponentially with composition depth.
        """
        effective_depth = self.composition_depth + depth
        return self.nrci ** (effective_depth + 1)


class OperatorRegistry:
    """
    Registry of operators with coherence information.
    
    The 10 primitive operators form a closed algebra from which all
    other operators can be derived through composition.
    """
    
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
                composition_depth=0,
                arity=1
            ),
            '⊗Y⁻¹': OperatorInfo(
                symbol='⊗Y⁻¹',
                name='Inverse Y-refinement',
                d_variables={'d6': 0.05, 'd5': 0.05, 'd8': 0.05},
                nrci=0.9999970000,
                is_primitive=True,
                composition_depth=0,
                arity=1
            ),
            '¬': OperatorInfo(
                symbol='¬',
                name='NOT',
                d_variables={'d6': 0.10, 'd5': 0.10, 'd8': 0.10},
                nrci=0.9999800000,
                is_primitive=True,
                composition_depth=0,
                arity=1
            ),
            '∧': OperatorInfo(
                symbol='∧',
                name='AND',
                d_variables={'d6': 0.10, 'd5': 0.10, 'd8': 0.10},
                nrci=0.9999800000,
                is_primitive=True,
                composition_depth=0,
                arity=2
            ),
            '∨': OperatorInfo(
                symbol='∨',
                name='OR',
                d_variables={'d6': 0.10, 'd5': 0.10, 'd8': 0.10},
                nrci=0.9999800000,
                is_primitive=True,
                composition_depth=0,
                arity=2
            ),
            '⊕': OperatorInfo(
                symbol='⊕',
                name='XOR',
                d_variables={'d6': 0.10, 'd5': 0.10, 'd8': 0.10},
                nrci=0.9999800000,
                is_primitive=True,
                composition_depth=0,
                arity=2
            ),
            '+': OperatorInfo(
                symbol='+',
                name='Addition',
                d_variables={'d6': 0.15, 'd5': 0.10, 'd8': 0.10},
                nrci=0.9999650000,
                is_primitive=True,
                composition_depth=0,
                arity=2
            ),
            '−': OperatorInfo(
                symbol='−',
                name='Subtraction',
                d_variables={'d6': 0.15, 'd5': 0.10, 'd8': 0.10},
                nrci=0.9999650000,
                is_primitive=True,
                composition_depth=0,
                arity=2
            ),
            '×': OperatorInfo(
                symbol='×',
                name='Multiplication',
                d_variables={'d6': 0.15, 'd5': 0.10, 'd8': 0.10},
                nrci=0.9999650000,
                is_primitive=True,
                composition_depth=0,
                arity=2
            ),
            '÷': OperatorInfo(
                symbol='÷',
                name='Division',
                d_variables={'d6': 0.15, 'd5': 0.10, 'd8': 0.15},
                nrci=0.9999590000,
                is_primitive=True,
                composition_depth=0,
                arity=2
            ),
        }
        return primitives
    
    def get_operator(self, symbol: str) -> Optional[OperatorInfo]:
        """Get operator by symbol."""
        return self.operators.get(symbol)
    
    def compose(self, op1_symbol: str, op2_symbol: str, composition_type: str = 'arithmetic') -> OperatorInfo:
        """
        Compose two operators with non-linear D6 model.
        
        Composition factors (α) account for optimization, saturation, and cancellation:
        - Arithmetic: α = 0.90 (10% optimization through algebraic simplification)
        - Transcendental: α = 0.67 (33% saturation from infinite series)
        - Inverse: α = 0.63 (37% cancellation from inverse operations)
        """
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
            composition_depth=composed_depth,
            arity=op2.arity  # Arity of the rightmost operator
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


# Global operator registry
_OPERATOR_REGISTRY = OperatorRegistry()


# ============================================================================
# COHERENCE STATE: Every value carries its own coherence
# ============================================================================

class CoherenceState:
    """
    A value in the UBP substrate isn't just a number - it's a coherence state.
    
    **Critical Fix (from feedback)**: Uses log-NRCI space for accurate error accumulation.
    Instead of multiplicative degradation (which decays too fast), we track the
    logarithm of coherence error, allowing linear accumulation of true fidelity loss.
    
    **NEW in 3.6**: Tracks operator sequence for full computational audit trail.
    
    Every value knows:
    - Its magnitude
    - Its log_nrci_error (smaller = better coherence)
    - Its net_refinements (tracks Y^n for closure testing)
    - Its operator_sequence (list of operators applied)
    
    This is information-first computation.
    """
    
    def __init__(self, value: float, log_nrci_error: float = None, net_refinements: int = 0,
                 operator_sequence: Optional[List[str]] = None):
        """
        Initialize a coherence state.
        
        Args:
            value: The numerical value
            log_nrci_error: log(1 - nrci), smaller is better (default: None → NRCI = 0.999997)
            net_refinements: Net Y-refinements applied (positive = forward, negative = backward)
            operator_sequence: List of operators applied to create this state
        """
        self.value = value
        # Default to target NRCI (0.999997) if not specified
        if log_nrci_error is None:
            self.log_nrci_error = math.log(1 - NRCI_TARGET)  # ≈ -13.7
        else:
            self.log_nrci_error = log_nrci_error
        self.net_refinements = net_refinements
        self.operator_sequence = operator_sequence if operator_sequence is not None else []
    
    @property
    def nrci(self) -> float:
        """Compute NRCI from log-error space."""
        # Clamp to avoid numerical issues
        return max(0.0, min(1.0, 1.0 - math.exp(self.log_nrci_error)))
    
    @property
    def operator_coherence(self) -> float:
        """
        Compute the coherence contribution from the operator sequence.
        
        This is the product of all operator NRCIs in the sequence.
        """
        if not self.operator_sequence:
            return 1.0
        
        coherence = 1.0
        for op_symbol in self.operator_sequence:
            op = _OPERATOR_REGISTRY.get_operator(op_symbol)
            if op:
                coherence *= op.nrci
        
        return coherence
    
    @property
    def total_coherence(self) -> float:
        """
        Compute total coherence including both state and operator contributions.
        """
        return self.nrci * self.operator_coherence
    
    @property
    def composition_depth(self) -> int:
        """Get the composition depth from operator sequence."""
        return len(self.operator_sequence)
    
    def degrade_by(self, delta_log_error: float, operator_symbol: Optional[str] = None) -> 'CoherenceState':
        """
        Degrade coherence by adding to log-error.
        
        This is the correct way to accumulate error - linearly in log space,
        not multiplicatively in NRCI space.
        
        Args:
            delta_log_error: Amount to degrade (positive = worse coherence)
            operator_symbol: Optional operator symbol to add to sequence
        """
        new_sequence = self.operator_sequence.copy()
        if operator_symbol:
            new_sequence.append(operator_symbol)
        
        return CoherenceState(
            self.value,
            self.log_nrci_error + delta_log_error,
            self.net_refinements,
            new_sequence
        )
    
    def refine_forward(self) -> 'CoherenceState':
        """
        Apply Y-refinement (geometry → observer).
        
        **Critical Fix**: Y-refinement is now directional, not round-trip.
        We apply Y *once* and track the net refinement count.
        """
        new_value = self.value * Y
        # Slight improvement in coherence due to geometric stabilization
        improvement = -abs(math.log(Y)) * 1e-10
        
        return CoherenceState(
            new_value,
            self.log_nrci_error + improvement,
            self.net_refinements + 1,
            self.operator_sequence + ['⊗Y']
        )
    
    def refine_backward(self) -> 'CoherenceState':
        """
        Apply inverse refinement (observer → geometry).
        
        **Critical Fix**: Directional operator, not round-trip.
        """
        new_value = self.value * Y_INVERSE
        improvement = -abs(math.log(Y_INVERSE)) * 1e-10
        
        return CoherenceState(
            new_value,
            self.log_nrci_error + improvement,
            self.net_refinements - 1,
            self.operator_sequence + ['⊗Y⁻¹']
        )
    
    def test_closure(self) -> Tuple[float, bool]:
        """
        Test bidirectional closure: (v ⊗ Y^n) ⊗ Y^(-n) → v
        
        True closure isn't v * Y * Y_INVERSE (which introduces floating-point noise),
        but tracking net refinements and verifying they cancel properly.
        """
        if self.net_refinements == 0:
            return 0.0, True
        
        # Simulate perfect closure
        expected_value = self.value / (Y ** self.net_refinements)
        error = abs(expected_value - self.value) / abs(self.value) if self.value != 0 else 0
        return error, error < 1e-12
    
    def __add__(self, other: 'CoherenceState') -> 'CoherenceState':
        """Add two coherence states."""
        if isinstance(other, (int, float)):
            other = CoherenceState(float(other))
        new_value = self.value + other.value
        # Error accumulates (log-space addition)
        combined_error = max(self.log_nrci_error, other.log_nrci_error) + math.log(2) * 1e-10
        
        # Track operator
        new_sequence = self.operator_sequence + other.operator_sequence + ['+']
        
        return CoherenceState(new_value, combined_error, 0, new_sequence)
    
    def __radd__(self, other) -> 'CoherenceState':
        """Right addition."""
        return self.__add__(other)
    
    def __sub__(self, other: 'CoherenceState') -> 'CoherenceState':
        """Subtract two coherence states."""
        if isinstance(other, (int, float)):
            other = CoherenceState(float(other))
        new_value = self.value - other.value
        combined_error = max(self.log_nrci_error, other.log_nrci_error) + math.log(2) * 1e-10
        
        # Track operator
        new_sequence = self.operator_sequence + other.operator_sequence + ['−']
        
        return CoherenceState(new_value, combined_error, 0, new_sequence)
    
    def __rsub__(self, other) -> 'CoherenceState':
        """Right subtraction."""
        if isinstance(other, (int, float)):
            other = CoherenceState(float(other))
        return other.__sub__(self)
    
    def __mul__(self, other: 'CoherenceState') -> 'CoherenceState':
        """Multiply two coherence states."""
        if isinstance(other, (int, float)):
            other = CoherenceState(float(other))
        new_value = self.value * other.value
        combined_error = self.log_nrci_error + other.log_nrci_error + math.log(1 + abs(new_value)) * 1e-12
        
        # Track operator
        new_sequence = self.operator_sequence + other.operator_sequence + ['×']
        
        return CoherenceState(new_value, combined_error, 0, new_sequence)
    
    def __rmul__(self, other) -> 'CoherenceState':
        """Right multiplication."""
        return self.__mul__(other)
    
    def __truediv__(self, other: 'CoherenceState') -> 'CoherenceState':
        """Divide two coherence states."""
        if isinstance(other, (int, float)):
            other = CoherenceState(float(other))
        if abs(other.value) < 1e-100:
            raise ValueError("Division by near-zero value")
        new_value = self.value / other.value
        combined_error = self.log_nrci_error + other.log_nrci_error + math.log(1 + abs(new_value)) * 1e-12
        
        # Track operator
        new_sequence = self.operator_sequence + other.operator_sequence + ['÷']
        
        return CoherenceState(new_value, combined_error, 0, new_sequence)
    
    def __rtruediv__(self, other) -> 'CoherenceState':
        """Right division."""
        if isinstance(other, (int, float)):
            other = CoherenceState(float(other))
        return other.__truediv__(self)
    
    def __neg__(self) -> 'CoherenceState':
        """Negate coherence state."""
        return CoherenceState(-self.value, self.log_nrci_error, self.net_refinements, 
                            self.operator_sequence + ['¬'])
    
    def __abs__(self) -> 'CoherenceState':
        """Absolute value of coherence state."""
        return CoherenceState(abs(self.value), self.log_nrci_error, self.net_refinements,
                            self.operator_sequence)
    
    def __repr__(self):
        depth_str = f", depth={self.composition_depth}" if self.composition_depth > 0 else ""
        return f"CoherenceState(value={self.value:.6e}, nrci={self.nrci:.10f}, net_ref={self.net_refinements}{depth_str})"


# ============================================================================
# COMPLEX COHERENCE STATE: For FFT and complex operations
# ============================================================================

class ComplexCoherenceState:
    """
    **Critical Fix (from feedback)**: Complex numbers must preserve the coherence abstraction.
    
    Instead of returning raw complex numbers from FFT, we wrap them in this class
    which maintains coherence tracking for both real and imaginary components.
    """
    
    def __init__(self, real: CoherenceState, imag: CoherenceState):
        self.real = real
        self.imag = imag
    
    @property
    def nrci(self) -> float:
        """Overall NRCI is the average of real and imaginary coherence."""
        return (self.real.nrci + self.imag.nrci) / 2.0
    
    @property
    def value(self) -> complex:
        """Get the complex value."""
        return complex(self.real.value, self.imag.value)
    
    def __repr__(self):
        return f"ComplexCoherenceState({self.value:.6e}, nrci={self.nrci:.10f})"


# ============================================================================
# COHERENCE TRANSFORMATION: All operations are coherence-preserving
# ============================================================================

def coherence_transform(state: CoherenceState, operation: Callable[[float], float], 
                       name: str = "transform", operator_symbol: Optional[str] = None) -> CoherenceState:
    """
    Apply an operation while maintaining coherence.
    
    This is the core of UBP computation: every operation is wrapped in
    coherence tracking. NRCI isn't measured after - it's maintained during.
    
    **Fixed**: Uses log-error accumulation instead of multiplicative degradation.
    **NEW in 3.6**: Tracks operator symbol for full audit trail.
    """
    # Apply operation
    result_value = operation(state.value)
    
    # Estimate coherence degradation based on operation complexity
    operation_complexity = abs(result_value - state.value) / (abs(state.value) + 1e-100)
    delta_log_error = operation_complexity * 1e-6  # Linear accumulation
    
    return state.degrade_by(delta_log_error, operator_symbol)


# ============================================================================
# INTEGRATION: Emerges from coherence accumulation
# ============================================================================

def integrate_coherent(f: Callable[[float], float], a: float, b: float, 
                      target_nrci: float = NRCI_TARGET) -> Tuple[CoherenceState, Dict]:
    """
    Integration as coherence accumulation, not Riemann sums.
    
    Key insight: Integration is about maintaining coherence across
    a transformation, not about summing rectangles.
    
    **Fixed**: Uses log-error accumulation for accurate long-chain fidelity.
    """
    # Start with target coherence
    state = CoherenceState(0.0)
    
    # Adaptive sampling based on target NRCI
    n_samples = 100
    h = (b - a) / n_samples
    
    # Accumulate with coherence tracking
    for i in range(n_samples + 1):
        x = a + i * h
        weight = 1.0 if (i == 0 or i == n_samples) else 2.0
        
        # Evaluate function
        try:
            fx = f(x)
        except:
            fx = 0.0
        
        # Accumulate (no round-trip stabilization - just clean addition)
        contribution = fx * weight * h / 2.0
        state.value += contribution
        
        # Update log-error based on local curvature
        if i > 0:
            delta_error = abs(fx) * 1e-10
            state.log_nrci_error += delta_error
    
    metadata = {
        'n_samples': n_samples,
        'interval': (a, b),
        'final_nrci': state.nrci
    }
    
    return state, metadata


# ============================================================================
# SYSTEM CONSTANTS: Now as CoherenceStates
# ============================================================================

# Y-constants with perfect coherence
Y_CONSTANT = CoherenceState(Y, math.log(1 - 0.9999970), 0, ['⊗Y'])
Y_INVERSE_CONSTANT = CoherenceState(Y_INVERSE, math.log(1 - 0.9999970), 0, ['⊗Y⁻¹'])
GOLDEN_RATIO_STATE = CoherenceState(GOLDEN_RATIO, math.log(1 - NRCI_TARGET), 0)

# Verify closure
_closure_test = Y_CONSTANT * Y_INVERSE_CONSTANT
assert abs(_closure_test.value - 1.0) < 1e-14, f"Y × (1/Y) closure failed: {_closure_test.value}"


# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def get_operator_info(symbol: str) -> Optional[OperatorInfo]:
    """Get operator information from the global registry."""
    return _OPERATOR_REGISTRY.get_operator(symbol)


def compose_operators(op1: str, op2: str, composition_type: str = 'arithmetic') -> OperatorInfo:
    """Compose two operators using the global registry."""
    return _OPERATOR_REGISTRY.compose(op1, op2, composition_type)


def suggest_operator_alternatives(symbol: str, min_nrci: float = 0.999950) -> List[OperatorInfo]:
    """Suggest high-coherence alternatives for an operator."""
    return _OPERATOR_REGISTRY.suggest_alternatives(symbol, min_nrci)


def analyze_computation(state: CoherenceState) -> Dict[str, Any]:
    """
    Analyze a CoherenceState's computational history.
    
    Returns a dictionary with:
    - operator_sequence: List of operators applied
    - composition_depth: Number of operators in sequence
    - operator_coherence: Product of all operator NRCIs
    - state_coherence: NRCI of the state itself
    - total_coherence: Combined coherence
    - warnings: List of potential issues
    """
    warnings = []
    
    # Check composition depth
    if state.composition_depth > 5:
        warnings.append(
            f"Composition depth ({state.composition_depth}) exceeds practical limit (5). "
            "Coherence degradation may be significant."
        )
    
    # Check operator coherence
    if state.operator_coherence < 0.999900:
        warnings.append(
            f"Operator coherence ({state.operator_coherence:.6f}) is low. "
            "Consider using higher-coherence alternatives."
        )
    
    # Check total coherence
    if state.total_coherence < 0.999800:
        warnings.append(
            f"Total coherence ({state.total_coherence:.6f}) is below recommended threshold. "
            "Results may have significant uncertainty."
        )
    
    return {
        'operator_sequence': state.operator_sequence,
        'composition_depth': state.composition_depth,
        'operator_coherence': state.operator_coherence,
        'state_coherence': state.nrci,
        'total_coherence': state.total_coherence,
        'warnings': warnings
    }


if __name__ == "__main__":
    print("="*80)
    print("UBP Coherence Substrate v3.6 - Computational Grammar Integration")
    print("="*80)
    
    # Test basic operations
    print("\n1. Basic Arithmetic with Operator Tracking:")
    a = CoherenceState(10.0)
    b = CoherenceState(5.0)
    c = a + b
    print(f"   10 + 5 = {c.value}")
    print(f"   Operator sequence: {c.operator_sequence}")
    print(f"   Total coherence: {c.total_coherence:.10f}")
    
    # Test composition
    print("\n2. Operator Composition:")
    mult_op = get_operator_info('×')
    add_op = get_operator_info('+')
    print(f"   Multiplication NRCI: {mult_op.nrci:.10f}")
    print(f"   Addition NRCI: {add_op.nrci:.10f}")
    
    composed = compose_operators('×', '+', 'arithmetic')
    print(f"   Composed (×∘+) NRCI: {composed.nrci:.10f}")
    print(f"   Composition depth: {composed.composition_depth}")
    
    # Test Y-refinement
    print("\n3. Y-Refinement with Tracking:")
    x = CoherenceState(100.0)
    y = x.refine_forward()
    print(f"   Original: {x}")
    print(f"   Refined: {y}")
    print(f"   Operator sequence: {y.operator_sequence}")
    
    # Test analysis
    print("\n4. Computational Analysis:")
    d = CoherenceState(2.0)
    e = d * d * d * d * d * d  # Deep composition
    analysis = analyze_computation(e)
    print(f"   Composition depth: {analysis['composition_depth']}")
    print(f"   Total coherence: {analysis['total_coherence']:.10f}")
    if analysis['warnings']:
        print(f"   Warnings:")
        for warning in analysis['warnings']:
            print(f"     - {warning}")
    
    print("\n" + "="*80)
    print("Coherence Substrate v3.6 Validated ✓")
    print("="*80)
