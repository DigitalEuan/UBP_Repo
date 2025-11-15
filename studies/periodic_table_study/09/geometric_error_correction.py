================================================================================
Universal Binary Principle (UBP) Framework v3.5 - Geometric Error Correction
Author: Euan Craig, New Zealand
Date: November 12, 2025
================================================================================

This module consolidates the entire error correction framework into a unified
coherence-native system. In UBP 3.5, error correction isn't a separate layer -
it's the intrinsic coherence maintenance of the computational substrate.

**Paradigm Shift**:
- GLR levels are coherence regimes (not correction layers)
- Golay codes are coherence patterns (not error correction codes)
- NRCI is the primary signal (not a metric)
- "Error correction" is coherence maintenance (not post-processing)

**Consolidates** (from UBP 3.4):
- glr_base.py (GLR framework)
- level_7_global_golay.py (Golay codes)
- enhanced_nrci.py (NRCI calculations)
- metrics.py (Core metrics)
- global_coherence.py (Coherence management)

**Zero Dependencies**: Only Python stdlib (math module) + coherence_substrate
"""

import math
from typing import Dict, List, Tuple, Optional, Union, Any
from dataclasses import dataclass
from enum import Enum
from collections import deque
import time

from coherence_substrate import CoherenceState, NRCI_TARGET, Y, Y_INVERSE, integrate, root


# ============================================================================
# COHERENCE REGIMES (formerly GLR Levels)
# ============================================================================

class CoherenceRegime(Enum):
    """
    Coherence regimes in the UBP substrate.
    
    These are NOT error correction levels - they're natural regimes where
    different coherence dynamics dominate.
    """
    SUPERCOHERENT = "SuperCoherent"      # NRCI ≥ 0.999997 (OnBit regime)
    COHERENT = "Coherent"                # 0.99 ≤ NRCI < 0.999997
    SEMICOHERENT = "SemiCoherent"        # 0.9 ≤ NRCI < 0.99
    SUBCOHERENT = "SubCoherent"          # 0.5 ≤ NRCI < 0.9
    TRANSITIONAL = "Transitional"        # 0.1 ≤ NRCI < 0.5
    DECOHERENT = "Decoherent"            # NRCI < 0.1


class LatticeGeometry(Enum):
    """
    Geometric structures that emerge in different coherence regimes.
    
    These correspond to the old GLR levels, but now understood as
    natural geometric patterns of coherence.
    """
    CUBIC = "cubic"                      # Simple cubic (EM realm)
    DIAMOND = "diamond"                  # Diamond (Quantum realm)
    FCC = "fcc"                         # Face-centered cubic (Gravitational)
    H4_120CELL = "h4_120cell"           # H4 120-cell (Biological)
    H3_ICOSAHEDRAL = "h3_icosahedral"   # H3 Icosahedral (Cosmological)
    GOLAY_PATTERN = "golay_pattern"     # Golay[23,12] pattern
    LEECH_LATTICE = "leech_24d"         # Leech lattice (24D)
    TEMPORAL = "temporal"                # Temporal coherence structure


# ============================================================================
# COHERENCE STATE ANALYSIS
# ============================================================================

@dataclass
class CoherenceAnalysis:
    """
    Analysis of a CoherenceState's quality and regime.
    
    This replaces the old GLRResult - instead of "correction results",
    we have "coherence analysis".
    """
    state: CoherenceState
    regime: CoherenceRegime
    geometry: LatticeGeometry
    quality_score: float  # 0 to 1
    net_refinements: int
    timestamp: float
    metadata: Dict[str, Any]


def classify_regime(nrci: float) -> CoherenceRegime:
    """
    Classify coherence regime based on NRCI value.
    
    Args:
        nrci: NRCI value (0 to 1)