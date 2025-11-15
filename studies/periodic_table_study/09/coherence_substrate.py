"""
UBP Coherence Substrate v1.0 - First Principles Implementation
===============================================================

This is NOT a numerical library. This is a **trust substrate** where all operations
emerge from information geometry.

**Core First Principles**:
1. Y-refinement: π/(π²+2) = 0.264675... (geometric resonance)
2. Observer cost: 1/Y = π + 2/π = 3.778212... (emerges from geometry)
3. NRCI: The primary computational signal (not a "metric")
4. Bidirectional closure: Y × (1/Y) = 1 (perfect round-trip)

**Key Insight**: Every value is a CoherenceState that carries its own quality measure.
NRCI is maintained *during* computation, not measured after.

Author: Euan R A Craig, New Zealand
Date: November 11, 2025
Version: 1.0.0
"""

import math
from typing import Tuple, Callable, Any, Dict, List

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
# COHERENCE STATE: Every value carries its own coherence
# ============================================================================

class CoherenceState:
    """
    A value in the UBP substrate isn't just a number - it's a coherence state.
    
    **Critical Fix (from feedback)**: Uses log-NRCI space for accurate error accumulation.
    Instead of multiplicative degradation (which decays too fast), we track the
    logarithm of coherence error, allowing linear accumulation of true fidelity loss.
    
    Every value knows:
    - Its magnitude
    - Its log_nrci_error (smaller = better coherence)
    - Its net_refinements (tracks Y^n for closure testing)
    
    This is information-first computation.
    """
    
    def __init__(self, value: float, log_nrci_error: float = None, net_refinements: int = 0):
        """
        Initialize a coherence state.
        
        Args:
            value: The numerical value
            log_nrci_error: log(1 - nrci), smaller is better (default: None → NRCI = 0.999997)
            net_refinements: Net Y-refinements applied (positive = forward, negative = backward)
        """
        self.value = value
        # Default to target NRCI (0.999997) if not specified
        if log_nrci_error is None:
            self.log_nrci_error = math.log(1 - NRCI_TARGET)  # ≈ -13.7
        else:
            self.log_nrci_error = log_nrci_error
        self.net_refinements = net_refinements
    
    @property
    def nrci(self) -> float:
        """Compute NRCI from log-error space."""
        # Clamp to avoid numerical issues
        return max(0.0, min(1.0, 1.0 - math.exp(self.log_nrci_error)))
    
    def degrade_by(self, delta_log_error: float) -> 'CoherenceState':
        """
        Degrade coherence by adding to log-error.
        
        This is the correct way to accumulate error - linearly in log space,
        not multiplicatively in NRCI space.
        """
        return CoherenceState(
            self.value,
            self.log_nrci_error + delta_log_error,
            self.net_refinements
        )
    
    def refine_forward(self) -> 'CoherenceState':
        """
        Apply Y-refinement (geometry → observer).
        