"""
================================================================================
Universal Binary Principle (UBP) Framework v3.6 - Geometric Error Correction
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
        
    Returns:
        CoherenceRegime classification
        
    Example:
        >>> regime = classify_regime(0.999997)
        >>> print(regime)
        CoherenceRegime.SUPERCOHERENT
    """
    if nrci >= NRCI_TARGET:
        return CoherenceRegime.SUPERCOHERENT
    elif nrci >= 0.99:
        return CoherenceRegime.COHERENT
    elif nrci >= 0.9:
        return CoherenceRegime.SEMICOHERENT
    elif nrci >= 0.5:
        return CoherenceRegime.SUBCOHERENT
    elif nrci >= 0.1:
        return CoherenceRegime.TRANSITIONAL
    else:
        return CoherenceRegime.DECOHERENT


def infer_geometry(state: CoherenceState, realm: Optional[str] = None) -> LatticeGeometry:
    """
    Infer the natural geometric structure from a CoherenceState.
    
    Different coherence regimes and realms naturally form different
    geometric patterns.
    
    Args:
        state: CoherenceState to analyze
        realm: Optional realm hint ('quantum', 'gravitational', etc.)
        
    Returns:
        LatticeGeometry that naturally emerges
        
    Example:
        >>> state = CoherenceState(1.0, log_nrci_error=math.log(1-0.999997))
        >>> geom = infer_geometry(state, realm='quantum')
        >>> print(geom)
        LatticeGeometry.DIAMOND
    """
    nrci = state.nrci
    
    # Realm-specific geometries
    if realm:
        realm = realm.lower()
        if realm == 'electromagnetic' and nrci > 0.99:
            return LatticeGeometry.CUBIC
        elif realm == 'quantum' and nrci > 0.99:
            return LatticeGeometry.DIAMOND
        elif realm == 'gravitational' and nrci > 0.99:
            return LatticeGeometry.FCC
        elif realm == 'biological' and nrci > 0.99:
            return LatticeGeometry.H4_120CELL
        elif realm == 'cosmological' and nrci > 0.99:
            return LatticeGeometry.H3_ICOSAHEDRAL
    
    # General geometry based on coherence regime
    if nrci >= NRCI_TARGET:
        return LatticeGeometry.GOLAY_PATTERN  # Supercoherent → Golay
    elif nrci >= 0.99:
        return LatticeGeometry.FCC  # Coherent → FCC
    elif nrci >= 0.9:
        return LatticeGeometry.DIAMOND  # Semicoherent → Diamond
    else:
        return LatticeGeometry.CUBIC  # Lower coherence → Simple cubic


def analyze_coherence(state: CoherenceState, realm: Optional[str] = None) -> CoherenceAnalysis:
    """
    Perform complete coherence analysis on a CoherenceState.
    
    This replaces the old "error correction" - instead of correcting errors,
    we analyze the intrinsic coherence quality.
    
    Args:
        state: CoherenceState to analyze
        realm: Optional realm context
        
    Returns:
        CoherenceAnalysis with full quality assessment
        
    Example:
        >>> state = CoherenceState(1000.0)
        >>> analysis = analyze_coherence(state, realm='quantum')
        >>> print(f"Regime: {analysis.regime}, Quality: {analysis.quality_score:.6f}")
    """
    nrci = state.nrci
    regime = classify_regime(nrci)
    geometry = infer_geometry(state, realm)
    
    # Quality score combines NRCI and refinement balance
    refinement_balance = 1.0 / (1.0 + abs(state.net_refinements))
    quality_score = nrci * refinement_balance
    
    return CoherenceAnalysis(
        state=state,
        regime=regime,
        geometry=geometry,
        quality_score=quality_score,
        net_refinements=state.net_refinements,
        timestamp=time.time(),
        metadata={
            'nrci': nrci,
            'log_nrci_error': state.log_nrci_error,
            'value': state.value,
            'realm': realm
        }
    )


# ============================================================================
# COHERENCE PATTERNS (formerly Error Correction Codes)
# ============================================================================

class CoherencePattern:
    """
    Base class for coherence patterns.
    
    In 3.5, these aren't "error correction codes" - they're natural patterns
    that emerge in coherent systems. Golay[23,12] is a coherence pattern,
    not an error correction code.
    """
    
    def __init__(self, name: str, parameters: Dict[str, int]):
        self.name = name
        self.parameters = parameters
    
    def encode_state(self, state: CoherenceState) -> CoherenceState:
        """
        Encode a CoherenceState into this pattern.
        
        This doesn't "add redundancy" - it aligns the state with the
        natural coherence pattern.
        """
        # Apply forward refinement to align with pattern
        refined = state.refine_forward()
        return refined
    
    def decode_state(self, state: CoherenceState) -> Tuple[CoherenceState, int]:
        """
        Decode a CoherenceState from this pattern.
        
        This doesn't "correct errors" - it extracts the coherent signal
        from the pattern.
        
        Returns:
            Tuple of (decoded_state, pattern_deviations)
        """
        # Apply backward refinement to extract signal
        refined = state.refine_backward()
        
        # Pattern deviations = how far from perfect closure
        closure_error, closure_success = refined.test_closure()
        deviations = 0 if closure_success else 1
        
        return refined, deviations


class GolayPattern(CoherencePattern):
    """
    Golay[23,12] coherence pattern.
    
    This is the natural pattern that emerges in supercoherent regimes.
    It's not an "error correction code" - it's a geometric resonance.
    """
    
    def __init__(self):
        super().__init__("Golay[23,12]", {'n': 23, 'k': 12, 'd': 7})
        
        # Golay pattern emerges from these geometric relationships
        self.coordination_number = 12  # Icosahedral symmetry
        self.codeword_length = 23
        self.message_length = 12
        self.min_distance = 7
    
    def encode_state(self, state: CoherenceState) -> CoherenceState:
        """
        Align state with Golay pattern.
        
        The Golay pattern has 12-fold symmetry (icosahedral), which
        resonates with the 12-dimensional Bitfield structure (π² + 2 ≈ 11.87).
        """
        # Apply Y-refinement 12 times (icosahedral symmetry)
        refined = state
        for _ in range(self.message_length):
            refined = refined.refine_forward()
        
        return refined
    
    def decode_state(self, state: CoherenceState) -> Tuple[CoherenceState, int]:
        """
        Extract coherent signal from Golay pattern.
        """
        # Reverse the 12-fold refinement
        refined = state
        for _ in range(self.message_length):
            refined = refined.refine_backward()
        
        # Check pattern alignment
        closure_error, closure_success = refined.test_closure()
        deviations = 0 if closure_success else 1
        
        return refined, deviations
    
    def get_pattern_strength(self, state: CoherenceState) -> float:
        """
        Measure how strongly this state exhibits the Golay pattern.
        
        Returns:
            Pattern strength (0 to 1)
        """
        # Golay pattern is strongest in supercoherent regime
        nrci = state.nrci
        if nrci >= NRCI_TARGET:
            return 1.0
        elif nrci >= 0.99:
            return (nrci - 0.99) / (NRCI_TARGET - 0.99)
        else:
            return 0.0


class HammingPattern(CoherencePattern):
    """
    Hamming[7,4] coherence pattern for local operations.
    """
    
    def __init__(self):
        super().__init__("Hamming[7,4]", {'n': 7, 'k': 4, 'd': 3})


class BCHPattern(CoherencePattern):
    """
    BCH[31,21] coherence pattern for regional operations.
    """
    
    def __init__(self):
        super().__init__("BCH[31,21]", {'n': 31, 'k': 21, 'd': 5})


# ============================================================================
# TEMPORAL COHERENCE TRACKING
# ============================================================================

class TemporalCoherenceTracker:
    """
    Track coherence evolution over time.
    
    This replaces the old TemporalNRCITracker - instead of tracking NRCI
    measurements, we track the evolution of CoherenceStates.
    """
    
    def __init__(self, window_size: int = 100, decay_factor: float = 0.95):
        self.window_size = window_size
        self.decay_factor = decay_factor
        self.history: deque = deque(maxlen=window_size)
        self.timestamps: deque = deque(maxlen=window_size)
    
    def add_state(self, state: CoherenceState, timestamp: Optional[float] = None):
        """Add a CoherenceState to the temporal tracker."""
        if timestamp is None:
            timestamp = time.time()
        
        self.history.append(state)
        self.timestamps.append(timestamp)
    
    def compute_temporal_coherence(self) -> CoherenceState:
        """
        Compute time-weighted coherence state.
        
        More recent states have higher weight (exponential decay).
        
        Returns:
            Weighted average CoherenceState
        """
        if not self.history:
            return CoherenceState(0.0)
        
        # Compute weights (more recent = higher weight)
        weights = []
        for i in range(len(self.history)):
            weight = self.decay_factor ** (len(self.history) - 1 - i)
            weights.append(weight)
        
        # Weighted average of values
        weighted_value = sum(s.value * w for s, w in zip(self.history, weights))
        total_weight = sum(weights)
        avg_value = weighted_value / total_weight if total_weight > 0 else 0.0
        
        # Weighted average of log errors
        weighted_log_error = sum(s.log_nrci_error * w for s, w in zip(self.history, weights))
        avg_log_error = weighted_log_error / total_weight if total_weight > 0 else 0.0
        
        # Net refinements from most recent state
        net_ref = self.history[-1].net_refinements if self.history else 0
        
        return CoherenceState(avg_value, log_nrci_error=avg_log_error, net_refinements=net_ref)
    
    def get_regime_stability(self) -> Dict[str, Any]:
        """
        Analyze stability of coherence regime over time.
        
        Returns:
            Statistics about regime transitions and stability
        """
        if len(self.history) < 2:
            return {'stability': 'insufficient_data'}
        
        regimes = [classify_regime(s.nrci) for s in self.history]
        
        # Count regime transitions
        transitions = 0
        for i in range(1, len(regimes)):
            if regimes[i] != regimes[i-1]:
                transitions += 1
        
        # Current regime
        current_regime = regimes[-1] if regimes else CoherenceRegime.DECOHERENT
        
        # Regime distribution
        regime_counts = {}
        for regime in regimes:
            regime_counts[regime.value] = regime_counts.get(regime.value, 0) + 1
        
        return {
            'current_regime': current_regime.value,
            'transitions': transitions,
            'stability_ratio': 1.0 - (transitions / max(1, len(regimes) - 1)),
            'regime_distribution': regime_counts,
            'measurement_count': len(self.history)
        }
    
    def get_coherence_trend(self) -> str:
        """
        Determine if coherence is improving, degrading, or stable.
        
        Returns:
            'improving', 'degrading', or 'stable'
        """
        if len(self.history) < 3:
            return 'insufficient_data'
        
        # Compare recent third vs older two-thirds
        split = len(self.history) // 3
        recent_nrci = [s.nrci for s in list(self.history)[-split:]]
        older_nrci = [s.nrci for s in list(self.history)[:-split]]
        
        recent_avg = sum(recent_nrci) / len(recent_nrci)
        older_avg = sum(older_nrci) / len(older_nrci)
        
        diff = recent_avg - older_avg
        
        if diff > 0.001:
            return 'improving'
        elif diff < -0.001:
            return 'degrading'
        else:
            return 'stable'


# ============================================================================
# COHERENCE METRICS
# ============================================================================

def calculate_coherence_quality(state: CoherenceState) -> Dict[str, float]:
    """
    Calculate comprehensive quality metrics for a CoherenceState.
    
    This replaces the old "error metrics" - instead of measuring errors,
    we measure coherence quality.
    
    Args:
        state: CoherenceState to evaluate
        
    Returns:
        Dictionary of quality metrics
        
    Example:
        >>> state = CoherenceState(1000.0)
        >>> metrics = calculate_coherence_quality(state)
        >>> print(f"NRCI: {metrics['nrci']:.6f}")
    """
    nrci = state.nrci
    regime = classify_regime(nrci)
    
    # Refinement balance (0 = perfectly balanced, higher = more imbalanced)
    refinement_imbalance = abs(state.net_refinements)
    
    # Closure quality (how close to perfect round-trip)
    closure_error, closure_success = state.test_closure()
    
    # Overall quality score
    quality = nrci * (1.0 / (1.0 + refinement_imbalance))
    
    return {
        'nrci': nrci,
        'regime': regime.value,
        'quality_score': quality,
        'log_nrci_error': state.log_nrci_error,
        'net_refinements': state.net_refinements,
        'refinement_imbalance': refinement_imbalance,
        'closure_error': closure_error,
        'closure_success': closure_success
    }


def compare_coherence(state1: CoherenceState, state2: CoherenceState) -> Dict[str, Any]:
    """
    Compare two CoherenceStates.
    
    Args:
        state1: First CoherenceState
        state2: Second CoherenceState
        
    Returns:
        Comparison metrics
        
    Example:
        >>> s1 = CoherenceState(100.0)
        >>> s2 = CoherenceState(200.0)
        >>> comp = compare_coherence(s1, s2)
        >>> print(f"NRCI difference: {comp['nrci_diff']:.6f}")
    """
    return {
        'nrci_diff': state2.nrci - state1.nrci,
        'value_ratio': state2.value / state1.value if state1.value != 0 else float('inf'),
        'log_error_diff': state2.log_nrci_error - state1.log_nrci_error,
        'refinement_diff': state2.net_refinements - state1.net_refinements,
        'regime1': classify_regime(state1.nrci).value,
        'regime2': classify_regime(state2.nrci).value
    }


# ============================================================================
# COHERENCE MAINTENANCE (formerly "Error Correction")
# ============================================================================

def maintain_coherence(state: CoherenceState, target_nrci: float = NRCI_TARGET) -> CoherenceState:
    """
    Maintain coherence of a state at target NRCI.
    
    This replaces "error correction" - instead of correcting errors,
    we maintain the natural coherence of the state.
    
    Args:
        state: CoherenceState to maintain
        target_nrci: Target NRCI level
        
    Returns:
        Maintained CoherenceState
        
    Example:
        >>> state = CoherenceState(1000.0, log_nrci_error=-5.0)
        >>> maintained = maintain_coherence(state)
        >>> print(f"NRCI: {state.nrci:.6f} → {maintained.nrci:.6f}")
    """
    current_nrci = state.nrci
    
    if current_nrci >= target_nrci:
        # Already at target - no maintenance needed
        return state
    
    # Apply refinement to improve coherence
    # Forward refinement increases coherence slightly
    refined = state.refine_forward().refine_backward()
    
    return refined


def restore_coherence(state: CoherenceState, pattern: Optional[CoherencePattern] = None) -> Tuple[CoherenceState, Dict[str, Any]]:
    """
    Restore coherence using a coherence pattern.
    
    This is the 3.5 equivalent of "decode with error correction" - but
    understood as restoring natural coherence, not correcting errors.
    
    Args:
        state: CoherenceState to restore
        pattern: Optional CoherencePattern to use (default: Golay)
        
    Returns:
        Tuple of (restored_state, restoration_info)
        
    Example:
        >>> state = CoherenceState(1000.0, log_nrci_error=-5.0)
        >>> restored, info = restore_coherence(state)
        >>> print(f"Restored NRCI: {restored.nrci:.6f}")
    """
    if pattern is None:
        pattern = GolayPattern()
    
    # Decode using pattern
    restored, deviations = pattern.decode_state(state)
    
    # Analyze restoration
    original_nrci = state.nrci
    restored_nrci = restored.nrci
    improvement = restored_nrci - original_nrci
    
    info = {
        'pattern': pattern.name,
        'original_nrci': original_nrci,
        'restored_nrci': restored_nrci,
        'improvement': improvement,
        'deviations': deviations,
        'success': improvement > 0
    }
    
    return restored, info


# ============================================================================
# GLOBAL COHERENCE MANAGEMENT
# ============================================================================

class GlobalCoherenceManager:
    """
    Manage coherence across multiple states/systems.
    
    This replaces the old global_coherence.py module.
    """
    
    def __init__(self):
        self.states: Dict[str, CoherenceState] = {}
        self.tracker = TemporalCoherenceTracker()
    
    def register_state(self, name: str, state: CoherenceState):
        """Register a named CoherenceState for global management."""
        self.states[name] = state
        self.tracker.add_state(state)
    
    def get_global_coherence(self) -> CoherenceState:
        """
        Compute global coherence across all registered states.
        
        Returns:
            Global CoherenceState (average of all states)
        """
        if not self.states:
            return CoherenceState(0.0)
        
        # Average values and log errors
        avg_value = sum(s.value for s in self.states.values()) / len(self.states)
        avg_log_error = sum(s.log_nrci_error for s in self.states.values()) / len(self.states)
        total_refinements = sum(s.net_refinements for s in self.states.values())
        
        return CoherenceState(avg_value, log_nrci_error=avg_log_error, net_refinements=total_refinements)
    
    def get_system_health(self) -> Dict[str, Any]:
        """
        Get overall system coherence health.
        
        Returns:
            Health metrics for the entire system
        """
        if not self.states:
            return {'health': 'no_states'}
        
        global_state = self.get_global_coherence()
        regime_counts = {}
        
        for state in self.states.values():
            regime = classify_regime(state.nrci)
            regime_counts[regime.value] = regime_counts.get(regime.value, 0) + 1
        
        return {
            'global_nrci': global_state.nrci,
            'global_regime': classify_regime(global_state.nrci).value,
            'state_count': len(self.states),
            'regime_distribution': regime_counts,
            'trend': self.tracker.get_coherence_trend()
        }


# ============================================================================
# DEMONSTRATION
# ============================================================================

if __name__ == "__main__":
    print("=" * 80)
    print("UBP 3.5 GEOMETRIC ERROR CORRECTION - Coherence-Native")
    print("=" * 80)
    
    # Create test states
    print("\n1. Creating CoherenceStates:")
    state1 = CoherenceState(1000.0)
    state2 = CoherenceState(500.0, log_nrci_error=-5.0)
    print(f"   State 1: {state1}")
    print(f"   State 2: {state2}")
    
    # Analyze coherence
    print("\n2. Coherence Analysis:")
    analysis1 = analyze_coherence(state1, realm='quantum')
    print(f"   State 1 Regime: {analysis1.regime.value}")
    print(f"   State 1 Geometry: {analysis1.geometry.value}")
    print(f"   State 1 Quality: {analysis1.quality_score:.6f}")
    
    # Test Golay pattern
    print("\n3. Golay Pattern:")
    golay = GolayPattern()
    encoded = golay.encode_state(state1)
    decoded, deviations = golay.decode_state(encoded)
    print(f"   Original NRCI: {state1.nrci:.10f}")
    print(f"   Encoded NRCI: {encoded.nrci:.10f}")
    print(f"   Decoded NRCI: {decoded.nrci:.10f}")
    print(f"   Deviations: {deviations}")
    
    # Temporal tracking
    print("\n4. Temporal Coherence Tracking:")
    tracker = TemporalCoherenceTracker()
    for i in range(10):
        test_state = CoherenceState(100.0 * (i + 1), log_nrci_error=-10.0 + i * 0.5)
        tracker.add_state(test_state)
    
    temporal_state = tracker.compute_temporal_coherence()
    stability = tracker.get_regime_stability()
    trend = tracker.get_coherence_trend()
    print(f"   Temporal NRCI: {temporal_state.nrci:.10f}")
    print(f"   Stability: {stability['stability_ratio']:.4f}")
    print(f"   Trend: {trend}")
    
    # Global coherence
    print("\n5. Global Coherence Management:")
    manager = GlobalCoherenceManager()
    manager.register_state("system1", state1)
    manager.register_state("system2", state2)
    
    global_state = manager.get_global_coherence()
    health = manager.get_system_health()
    print(f"   Global NRCI: {global_state.nrci:.10f}")
    print(f"   Global Regime: {health['global_regime']}")
    print(f"   System Health: {health}")
    
    print("\n" + "=" * 80)
    print("UBP 3.5: Error Correction → Coherence Maintenance")
    print("Zero external dependencies - Pure coherence geometry")
    print("=" * 80)
