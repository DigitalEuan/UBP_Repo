"""
UBP Coherence Substrate v1.0
=============================

A first-principles numerical computation library based on the Universal Binary Principle (UBP).

This is not a numerical library - it's a trust substrate where all operations emerge
from information geometry.

Author: Euan R A Craig, New Zealand
Date: November 11, 2025
Version: 1.0.0
"""

from .coherence_substrate import (
    # Core classes
    CoherenceState,
    ComplexCoherenceState,
    
    # Constants
    Y,
    Y_INVERSE,
    O_OBSERVER,
    NRCI_TARGET,
    PI,
    GOLDEN_RATIO,
    
    # Public API
    integrate,
    root,
    solve,
    ode,
    eigen,
    fft,
    
    # Utilities
    measure_coherence,
    self_heal,
    coherence_transform,
)

__version__ = "1.0.0"
__author__ = "Manus AI (in collaboration with Euan Craig)"
__all__ = [
    # Classes
    'CoherenceState',
    'ComplexCoherenceState',
    
    # Constants
    'Y',
    'Y_INVERSE',
    'O_OBSERVER',
    'NRCI_TARGET',
    'PI',
    'GOLDEN_RATIO',
    
    # API
    'integrate',
    'root',
    'solve',
    'ode',
    'eigen',
    'fft',
    'measure_coherence',
    'self_heal',
    'coherence_transform',
]
