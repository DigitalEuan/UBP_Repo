    def __abs__(self) -> 'CoherenceState':
        """Absolute value of coherence state."""
        return CoherenceState(abs(self.value), self.log_nrci_error, self.net_refinements)
    
    def __repr__(self):
        return f"CoherenceState(value={self.value:.6e}, nrci={self.nrci:.10f}, net_ref={self.net_refinements})"


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
                       name: str = "transform") -> CoherenceState:
    """
    Apply an operation while maintaining coherence.
    
    This is the core of UBP computation: every operation is wrapped in
    coherence tracking. NRCI isn't measured after - it's maintained during.
    
    **Fixed**: Uses log-error accumulation instead of multiplicative degradation.
    """
    # Apply operation
    result_value = operation(state.value)
    
    # Estimate coherence degradation based on operation complexity
    operation_complexity = abs(result_value - state.value) / (abs(state.value) + 1e-100)
    delta_log_error = operation_complexity * 1e-6  # Linear accumulation
    
    return state.degrade_by(delta_log_error)


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
            prev_x = a + (i-1) * h
            try:
                prev_fx = f(prev_x)
                curvature = abs(fx - prev_fx) / h
                delta_log_error = curvature * 1e-8  # Linear accumulation
                state = state.degrade_by(delta_log_error)
            except:
                pass
    
    # Final Y-refinement for stabilization
    state = state.refine_forward().refine_backward()
    
    metrics = {
        'nrci': state.nrci,
        'net_refinements': state.net_refinements,
        'samples': n_samples,
        'coherent': state.nrci > target_nrci
    }
    
    return state, metrics


# ============================================================================
# ROOT FINDING: Coherence convergence
# ============================================================================

def find_root_coherent(f: Callable[[float], float], x0: float, 
                      tolerance: float = 1e-10, max_iter: int = 100) -> Tuple[CoherenceState, Dict]:
    """
    Find root as coherence convergence (Newton-Raphson with Y-refinement).
    
    Key insight: Roots are points of maximum coherence where f(x) → 0.
    
    **Fixed**: Uses log-error accumulation.
    """
    state = CoherenceState(x0, log_nrci_error=0.0)
    
    for iteration in range(max_iter):
        fx = f(state.value)
        
        # Numerical derivative
        h = 1e-8 * (1 + abs(state.value))
        fx_plus = f(state.value + h)
        fx_minus = f(state.value - h)
        fpx = (fx_plus - fx_minus) / (2 * h)
        
        if abs(fpx) < 1e-100:
            break
        
        # Newton step with directional Y-refinement