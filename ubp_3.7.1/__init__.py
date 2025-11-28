"""
UBP 3.7 - Universal Binary Principal
====================================

A genuine, fully-functional implementation with real mathematical structures.

Version: 3.7.0
Date: November 28, 2025
"""

__version__ = "3.7.0"
__author__ = "UBP 3.7 Development"

# Core modules
from .core import coherence_substrate, y_constants, system_constants, state

# Error correction
from .error_correction import leech_lattice, vector_offbit

# Analysis
from .analysis import resonance_detector_fft, spectral_extraction, enhanced_nrci

# Simulation
from .simulation import simulation

__all__ = [
    'coherence_substrate',
    'y_constants',
    'system_constants',
    'state',
    'leech_lattice',
    'vector_offbit',
    'resonance_detector_fft',
    'spectral_extraction',
    'enhanced_nrci',
    'simulation',
]
