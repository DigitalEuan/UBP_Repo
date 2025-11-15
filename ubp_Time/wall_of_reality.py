"""
Universal Binary Principle (UBP) Framework v3.5 - Wall of Reality (Coherence-Native)
Author: Euan Craig, New Zealand
Date: 12 November 2025

This module implements the Wall of Reality detection and enforcement system using the
coherence_substrate paradigm. All computed values are CoherenceStates, and NRCI
tracking is maintained throughout the computation.

The Wall of Reality is a fundamental computational limit at 10¹² Hz (1 THz),
representing the maximum coherent toggle rate before coherence breakdown.
"""

import math
from typing import Dict, Optional, Tuple, List
from dataclasses import dataclass
from enum import Enum
import warnings

# Critical Import for UBP 3.5 Coherence Substrate
from coherence_substrate import CoherenceState, integrate, root, solve, Y_CONSTANT, Y_INVERSE

# --- Constants and Enums (Non-CoherenceState) ---

class WallProximity(Enum):
    """Proximity classification relative to Wall of Reality."""
    SAFE = "safe"                    # < 50% of wall frequency
    CAUTION = "caution"              # 50-80% of wall frequency
    WARNING = "warning"              # 80-90% of wall frequency
    DANGER = "danger"                # 90-99% of wall frequency
    CRITICAL = "critical"            # 99-100% of wall frequency
    BEYOND_WALL = "beyond_wall"      # >= 100% of wall frequency

# The Wall Frequency is a constant, but its inverse is critical for refinement
WALL_FREQUENCY_HZ = 1e12  # 1 THz
WALL_FREQUENCY_CS = CoherenceState(WALL_FREQUENCY_HZ, 0.0, 0.0) # Constant CoherenceState

# Proximity thresholds (as fraction of wall frequency)
THRESHOLD_SAFE = 0.5
THRESHOLD_CAUTION = 0.8
THRESHOLD_WARNING = 0.9
THRESHOLD_DANGER = 0.99
THRESHOLD_CRITICAL = 0.999

# NRCI collapse parameters
NRCI_COLLAPSE_THRESHOLD = 0.1  # NRCI below this indicates collapse
NRCI_COLLAPSE_RATE = 10.0  # Exponential collapse rate near wall

# --- Coherence-Native Data Structure ---

@dataclass
class WallStatus:
    """
    Coherence-Native Status report for Wall of Reality proximity.
    
    Attributes are CoherenceStates where appropriate.
    """
    frequency: CoherenceState       # Current frequency (Hz)
    wall_frequency: CoherenceState  # Wall of Reality frequency (Hz)
    distance_ratio: CoherenceState  # Ratio of current to wall frequency
    proximity: WallProximity        # Proximity classification
    nrci_risk: CoherenceState       # Estimated NRCI collapse risk (0-1)
    is_safe: bool                   # Whether operation is safe
    warnings: List[str]             # List of warning messages

# --- Coherence-Native Wall of Reality Class ---

class WallOfReality:
    """
    Coherence-Native Wall of Reality detector and enforcement system.
    
    All internal calculations operate on CoherenceStates, maintaining NRCI
    and refinement tracking.
    """
    
    def __init__(self, enforce_limit: bool = False):
        """
        Initialize Wall of Reality detector.
        
        Args:
            enforce_limit: Whether to enforce frequency limits (default False - warning only)
        """
        self.wall_frequency = WALL_FREQUENCY_CS
        self.enforce_limit = enforce_limit
        self.detection_history: List[WallStatus] = []
    
    def calculate_distance_ratio(self, frequency: CoherenceState) -> CoherenceState:
        """
        Calculate ratio of frequency to wall frequency using coherence division.
        
        Args:
            frequency: Current frequency (CoherenceState)
            
        Returns:
            Ratio (CoherenceState)
        """
        # distance_ratio = frequency / self.wall_frequency
        # Use integrate (division) for coherence-aware operation
        return integrate(frequency, self.wall_frequency)
    
    def classify_proximity(self, distance_ratio: CoherenceState) -> WallProximity:
        """
        Classify proximity to wall based on distance ratio's value.
        
        Args:
            distance_ratio: Ratio of frequency to wall frequency (CoherenceState)
            
        Returns:
            WallProximity classification
        """
        ratio_value = distance_ratio.value
        
        if ratio_value >= 1.0:
            return WallProximity.BEYOND_WALL
        elif ratio_value >= THRESHOLD_CRITICAL:
            return WallProximity.CRITICAL
        elif ratio_value >= THRESHOLD_DANGER:
            return WallProximity.DANGER
        elif ratio_value >= THRESHOLD_WARNING:
            return WallProximity.WARNING
        elif ratio_value >= THRESHOLD_CAUTION:
            return WallProximity.CAUTION
        else:
            return WallProximity.SAFE
    
    def calculate_nrci_collapse_risk(
        self,
        frequency: CoherenceState,
        current_nrci: Optional[CoherenceState] = None
    ) -> CoherenceState:
        """
        Calculate NRCI collapse risk based on frequency proximity to wall.
        
        The risk itself is a computed value and must be a CoherenceState.
        
        Args:
            frequency: Current frequency (CoherenceState)
            current_nrci: Current NRCI value (Optional CoherenceState)
            
        Returns:
            Collapse risk (CoherenceState, value 0-1)
        """
        distance_ratio = self.calculate_distance_ratio(frequency)
        ratio_value = distance_ratio.value
        
        if ratio_value >= 1.0:
            # Beyond wall - collapse is certain (CoherenceState(1.0, 0.0, 0.0))
            return CoherenceState(1.0, 0.0, 0.0)
        
        risk_value = 0.0
        
        # Exponential risk increase near wall
        if ratio_value > THRESHOLD_WARNING:
            excess = ratio_value - THRESHOLD_WARNING
            # Note: math.exp is used on the value, as the NRCI tracking for this
            # statistical function is handled by the CoherenceState wrapper.
            risk_value = 1.0 - math.exp(-NRCI_COLLAPSE_RATE * excess)
        
        # If current NRCI is provided, adjust risk based on actual coherence
        if current_nrci is not None:
            # Check for existing NRCI collapse
            if current_nrci.value < NRCI_COLLAPSE_THRESHOLD:
                risk_value = max(risk_value, 0.9)  # High risk if NRCI already low
            
            # Refine the risk based on the input NRCI's error
            # This is a key coherence step: the risk's error is dependent on the
            # input frequency's error and the current NRCI's error.
            # For simplicity in this migration, we'll use the frequency's error
            # as the primary source of error for the computed risk.
            risk_log_nrci_error = frequency.log_nrci_error + (current_nrci.log_nrci_error if current_nrci else 0.0)
            
            # Apply Y-refinement to the risk value based on the current NRCI's refinement
            # If the current NRCI is highly refined (low net_refinements), the risk
            # calculation is more reliable.
            risk_net_refinements = frequency.net_refinements + (current_nrci.net_refinements if current_nrci else 0.0)
            
            # Create the CoherenceState for the risk
            risk_cs = CoherenceState(risk_value, risk_log_nrci_error, risk_net_refinements)
            
            # Apply directional refinement (backward) to the risk based on the current NRCI
            # A low NRCI (high error) means the risk is likely understated, so we refine
            # the risk backward (towards a higher, more conservative value).
            if current_nrci and current_nrci.value < THRESHOLD_CAUTION:
                risk_cs = risk_cs.refine_backward(Y_INVERSE)
            
            return risk_cs
        
        # Default CoherenceState creation if no current_nrci is provided
        return CoherenceState(risk_value, distance_ratio.log_nrci_error, distance_ratio.net_refinements)
    
    def detect_wall_approach(
        self,
        frequency: CoherenceState,
        current_nrci: Optional[CoherenceState] = None
    ) -> WallStatus:
        """
        Detect and analyze approach to Wall of Reality.
        
        Args:
            frequency: Current frequency (CoherenceState)
            current_nrci: Current NRCI value (Optional CoherenceState)
            
        Returns:
            WallStatus with detailed analysis (Coherence-Native)
        """
        distance_ratio = self.calculate_distance_ratio(frequency)
        proximity = self.classify_proximity(distance_ratio)
        nrci_risk = self.calculate_nrci_collapse_risk(frequency, current_nrci)
        
        # is_safe is a boolean based on the value of the distance ratio
        is_safe = proximity in [WallProximity.SAFE, WallProximity.CAUTION]
        
        # Generate warnings based on proximity and risk value
        warnings_list = []
        
        freq_val = frequency.value
        wall_val = self.wall_frequency.value
        ratio_val = distance_ratio.value
        risk_val = nrci_risk.value
        
        if proximity == WallProximity.BEYOND_WALL:
            warnings_list.append(
                f"CRITICAL: Frequency {freq_val:.2e} Hz exceeds Wall of Reality "
                f"({wall_val:.2e} Hz). NRCI collapse imminent. "
                f"Coherence Error: {nrci_risk.log_nrci_error:.2e}"
            )
        elif proximity == WallProximity.CRITICAL:
            warnings_list.append(
                f"CRITICAL: Frequency {freq_val:.2e} Hz is {ratio_val*100:.1f}% "
                f"of Wall limit. Immediate action required. "
                f"Coherence Error: {nrci_risk.log_nrci_error:.2e}"
            )
        elif proximity == WallProximity.DANGER:
            warnings_list.append(
                f"DANGER: Frequency {freq_val:.2e} Hz approaching Wall of Reality. "
                f"NRCI collapse risk: {risk_val*100:.1f}%. "
                f"Coherence Error: {nrci_risk.log_nrci_error:.2e}"
            )
        elif proximity == WallProximity.WARNING:
            warnings_list.append(
                f"WARNING: Frequency {freq_val:.2e} Hz at {ratio_val*100:.1f}% "
                f"of Wall limit. Reduce frequency. "
                f"Coherence Error: {nrci_risk.log_nrci_error:.2e}"
            )
        elif proximity == WallProximity.CAUTION:
            warnings_list.append(
                f"CAUTION: Frequency {freq_val:.2e} Hz at {ratio_val*100:.1f}% "
                f"of Wall limit. Monitor closely. "
                f"Coherence Error: {nrci_risk.log_nrci_error:.2e}"
            )
        
        if current_nrci is not None and current_nrci.value < NRCI_COLLAPSE_THRESHOLD:
            warnings_list.append(
                f"NRCI collapse detected: {current_nrci.value:.6f} < {NRCI_COLLAPSE_THRESHOLD}. "
                f"Refinement: {current_nrci.net_refinements:.2f}"
            )
        
        status = WallStatus(
            frequency=frequency,
            wall_frequency=self.wall_frequency,
            distance_ratio=distance_ratio,
            proximity=proximity,
            nrci_risk=nrci_risk,
            is_safe=is_safe,
            warnings=warnings_list
        )
        
        self.detection_history.append(status)
        
        return status
    
    def enforce_computational_limit(
        self,
        operation_freq: CoherenceState,
        raise_error: bool = True
    ) -> CoherenceState:
        """
        Enforce computational limit by preventing operations beyond wall.
        
        Returns the input frequency, potentially refined, if allowed.
        Raises an error if limit exceeded and enforcement is on.
        
        Args:
            operation_freq: Requested operation frequency (CoherenceState)
            raise_error: Whether to raise exception if limit exceeded
            
        Returns:
            The input frequency (CoherenceState), potentially refined.
            
        Raises:
            ValueError: If frequency exceeds limit and raise_error is True
        """
        if not self.enforce_limit:
            return operation_freq
        
        status = self.detect_wall_approach(operation_freq)
        
        if status.proximity == WallProximity.BEYOND_WALL:
            if raise_error:
                raise ValueError(
                    f"Operation frequency {operation_freq.value:.2e} Hz exceeds "
                    f"Wall of Reality ({self.wall_frequency.value:.2e} Hz). "
                    f"This violates fundamental computational limits. "
                    f"Coherence Error: {operation_freq.log_nrci_error:.2e}"
                )
            # If not raising error, return a zero-value CoherenceState with max error
            return CoherenceState(0.0, 1.0, 0.0)
        
        # If in DANGER or CRITICAL, apply forward refinement to the frequency
        # to represent the cost of maintaining coherence at this high frequency.
        if status.proximity in [WallProximity.CRITICAL, WallProximity.DANGER, WallProximity.WARNING]:
            warnings.warn(
                f"Operation frequency {operation_freq.value:.2e} Hz is dangerously "
                f"close to Wall of Reality. Applying forward refinement (xY)."
            )
            # Forward refinement (xY) reduces the effective value, representing
            # the loss of available energy/information due to high observer cost.
            return operation_freq.refine_forward(Y_CONSTANT)
        
        return operation_freq
    
    def get_wall_distance(self, current_freq: CoherenceState) -> Dict[str, CoherenceState]:
        """
        Get distance metrics to Wall of Reality.
        
        Returns:
            Dictionary with distance metrics as CoherenceStates
        """
        distance_ratio = self.calculate_distance_ratio(current_freq)
        
        # distance_hz = self.wall_frequency - current_freq
        distance_hz = self.wall_frequency - current_freq
        
        # distance_percent = (1.0 - distance_ratio) * 100
        # Use CoherenceState operations for all computed values
        one_cs = CoherenceState(1.0, 0.0, 0.0)
        hundred_cs = CoherenceState(100.0, 0.0, 0.0)
        distance_percent = integrate(one_cs - distance_ratio, root(hundred_cs)) # (1-ratio) * 100
        
        # safe_margin_hz = self.wall_frequency * 0.9 - current_freq
        threshold_cs = CoherenceState(0.9, 0.0, 0.0)
        safe_limit_cs = integrate(self.wall_frequency, threshold_cs) # wall * 0.9
        safe_margin_hz = safe_limit_cs - current_freq
        
        return {
            'current_frequency_hz': current_freq,
            'wall_frequency_hz': self.wall_frequency,
            'distance_hz': distance_hz,
            'distance_ratio': distance_ratio,
            'distance_percent': distance_percent,
            'safe_margin_hz': safe_margin_hz
        }

# --- Coherence-Native Utility Functions ---

def detect_wall_approach_cs(
    frequency: CoherenceState,
    threshold_ratio: float = THRESHOLD_WARNING
) -> Tuple[bool, CoherenceState]:
    """
    Simple wall approach detection function (Coherence-Native).
    
    Args:
        frequency: Frequency to check (CoherenceState)
        threshold_ratio: Warning threshold (default 0.9 = 90% of wall)
        
    Returns:
        Tuple of (is_approaching, distance_ratio)
    """
    wall = WallOfReality()
    distance_ratio = wall.calculate_distance_ratio(frequency)
    is_approaching = distance_ratio.value >= threshold_ratio
    
    return is_approaching, distance_ratio

def check_frequency_limit_cs(frequency: CoherenceState) -> bool:
    """
    Simple frequency limit check (Coherence-Native).
    
    Args:
        frequency: Frequency to check (CoherenceState)
        
    Returns:
        True if frequency is safe
    """
    return frequency.value < WALL_FREQUENCY_HZ

# --- Demonstration (Coherence-Native) ---

def demonstrate_wall_of_reality_cs():
    """
    Demonstrate Wall of Reality detection and analysis using CoherenceStates.
    
    Returns:
        Dictionary with demonstration results
    """
    print("=" * 80)
    print("WALL OF REALITY DEMONSTRATION (COHERENCE-NATIVE)")
    print("=" * 80)
    
    wall = WallOfReality(enforce_limit=True)
    
    print(f"\nWall of Reality Frequency: {wall.wall_frequency.value:.2e} Hz (1 THz)")
    print(f"Fundamental computational limit of the Bitfield")
    
    # Test frequencies as CoherenceStates (assuming minimal initial error)
    test_frequencies = [
        CoherenceState(1e9, 1e-10, 0.0),    # 1 GHz - safe
        CoherenceState(5e11, 1e-8, 0.0),   # 500 GHz - caution
        CoherenceState(9.5e11, 1e-6, 0.0), # 950 GHz - danger
        CoherenceState(1.001e12, 1e-5, 0.0), # 1.001 THz - beyond wall
    ]
    
    # Example current NRCI (simulating a low-coherence state)
    low_nrci = CoherenceState(0.05, 1e-2, 0.0)
    
    print("\n" + "-" * 80)
    print("Frequency Proximity Analysis:")
    print("-" * 80)
    
    results = []
    for freq_cs in test_frequencies:
        # Test with and without a low NRCI state
        status = wall.detect_wall_approach(freq_cs, low_nrci)
        results.append(status)
        
        print(f"\nFrequency: {status.frequency.value:.2e} Hz (Error: {status.frequency.log_nrci_error:.2e})")
        print(f"  Distance Ratio: {status.distance_ratio.value:.4f} ({status.distance_ratio.value*100:.1f}%)")
        print(f"  Proximity: {status.proximity.value.upper()}")
        print(f"  NRCI Collapse Risk: {status.nrci_risk.value*100:.1f}% (Error: {status.nrci_risk.log_nrci_error:.2e})")
        print(f"  Refinement: {status.nrci_risk.net_refinements:.2f}")
        print(f"  Safe: {status.is_safe}")
        
        if status.warnings:
            print(f"  Warnings:")
            for warning in status.warnings:
                print(f"    - {warning}")
        
        # Demonstrate enforcement and refinement
        try:
            refined_freq = wall.enforce_computational_limit(freq_cs)
            print(f"  Enforced Freq: {refined_freq.value:.2e} Hz (Refinement: {refined_freq.net_refinements:.2f})")
        except ValueError as e:
            print(f"  Enforcement Result: {e}")
            
    # Demonstrate distance metrics
    print("\n" + "-" * 80)
    print("Distance Metrics (for 500 GHz operation):")
    print("-" * 80)
    
    test_freq_cs = CoherenceState(5e11, 1e-8, 0.0)
    distance = wall.get_wall_distance(test_freq_cs)
    
    print(f"Current Frequency: {distance['current_frequency_hz'].value:.2e} Hz")
    print(f"Wall Frequency: {distance['wall_frequency_hz'].value:.2e} Hz")
    print(f"Distance: {distance['distance_hz'].value:.2e} Hz ({distance['distance_percent'].value:.1f}%)")
    print(f"Safe Margin: {distance['safe_margin_hz'].value:.2e} Hz")
    
    print("\n" + "=" * 80)
    
    return {
        'wall': wall,
        'test_results': results,
        'distance_metrics': distance
    }


if __name__ == "__main__":
    # Run demonstration when module is executed directly
    results = demonstrate_wall_of_reality_cs()
    
    print("\nWall of Reality demonstration complete (Coherence-Native).")
    print("The 1 THz limit is now tracked with full NRCI and refinement.")
    print("\nModule ready for import into UBP 3.5 system.")
