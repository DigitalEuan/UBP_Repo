"""
UBP CORE v4.0 - Unified Metrics Module
Distilled from Observer Framework v3.7.1 and Enhanced NRCI.
Author: UBP Research Assistant (v3.9 Ultimate) / Euan Craig, New Zealand
Date: 22 December 2025

### UBP Metrics SOP: Best Use Instructions

#### 1. The Global Instance Protocol
**Instruction:** Always import the global METRICS instance rather than creating new class instances.
Python Script:
from metrics import METRICS
base_cost = METRICS.observer.get_base_cost()

#### 2. The Normalization Requirement
**Instruction:** Before calling analyze_state(), ensure your variance is normalized.

#### 3. Dimensional Scaling (The Realm Rule)
**Instruction:** Use the calculate_realm_cost function for spatial vs substrate scaling.

#### 4. Interpreting the NRCI (The Regime Guide)
**Instruction:** Use the CoherenceRegime enum to automate logic.

#### 5. The GLR Toggle Check
**Instruction:** For discrete operations use calculate_glr_nrci.
"""

import math
import numpy as np
from dataclasses import dataclass
from enum import Enum

class CoherenceRegime(Enum):
    ONBIT = "OnBit"              # NRCI >= 0.9999999 (v4.0 Standard)
    COHERENT = "Coherent"        # 0.5 <= NRCI < 0.9999999
    TRANSITIONAL = "Transitional" # 0.1 <= NRCI < 0.5
    SUBCOHERENT = "Subcoherent"  # NRCI < 0.1

@dataclass
class UBPConstants:
    # The Geometric Origin of the Observer
    OBSERVER_FIXED_POINT = math.pi + (2 / math.pi) # 3.7782010913...
    Y_CONSTANT = 1 / OBSERVER_FIXED_POINT          # 0.264675386...
    PGCI_TARGET = 0.9999999                        # v4.0 Coherence Target

class UBPObserver:
    @staticmethod
    def get_base_cost():
        return UBPConstants.OBSERVER_FIXED_POINT

    @staticmethod
    def calculate_realm_cost(realm_complexity=1.0, dimensions=6.0):
        base = UBPConstants.OBSERVER_FIXED_POINT
        return base * realm_complexity * (dimensions / 6.0)

class UBPCoherence:
    @staticmethod
    def calculate_nrci(observed_variance, theoretical_variance=1.0):
        nrci = 1.0 - (observed_variance / theoretical_variance)
        return max(0.0, min(1.0, nrci))

    @staticmethod
    def calculate_glr_nrci(error_sum, n_toggles):
        denominator = 9 * n_toggles
        nrci = 1.0 - (error_sum / denominator)
        return max(0.0, min(1.0, nrci))

    @staticmethod
    def get_regime(nrci_value):
        if nrci_value >= UBPConstants.PGCI_TARGET:
            return CoherenceRegime.ONBIT
        elif nrci_value >= 0.5:
            return CoherenceRegime.COHERENT
        elif nrci_value >= 0.1:
            return CoherenceRegime.TRANSITIONAL
        else:
            return CoherenceRegime.SUBCOHERENT

class UBPMetrics:
    def __init__(self):
        self.observer = UBPObserver()
        self.coherence = UBPCoherence()
        self.constants = UBPConstants()

    def analyze_state(self, variance, realm="standard"):
        nrci = self.coherence.calculate_nrci(variance)
        regime = self.coherence.get_regime(nrci)
        
        return {
            "nrci": nrci,
            "regime": regime.value,
            "observer_cost": self.observer.get_base_cost(),
            "is_stable": nrci >= 0.5
        }

# Global Instance
METRICS = UBPMetrics()
