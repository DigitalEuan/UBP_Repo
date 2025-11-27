"""
Universal Binary Principle (UBP) Framework v3.7 - Wall of Reality
Author: Euan Craig, New Zealand
Date: 31 October 2025
================================================================================

This module implements the Wall of Reality detection and enforcement system.

The Wall of Reality is a fundamental computational limit at 10¹² Hz (1 THz),
beyond which the NRCI exhibits sharp, non-random collapse to zero. This is not
an arbitrary limit - it represents the maximum toggle rate before coherence
breakdown in the Bitfield.

Key Concepts:
- Wall Frequency: 10¹² Hz (1 THz)
- NRCI Collapse: Sharp drop to zero at/beyond wall
- Approach Warning: Triggered at 90% of wall frequency
- Computational Limit: Fundamental constraint of Bitfield dynamics

Physical Interpretation:
The wall represents the maximum information processing rate of the universal
computational substrate. Beyond this frequency, the Bitfield cannot maintain
coherent toggle states, resulting in reality breakdown.
"""

import math
import numpy as np
from typing import Dict, Optional, Tuple, List
from dataclasses import dataclass
from enum import Enum
import warnings


class WallProximity(Enum):
    """Proximity classification relative to Wall of Reality."""
    SAFE = "safe"                    # < 50% of wall frequency
    CAUTION = "caution"              # 50-80% of wall frequency
    WARNING = "warning"              # 80-90% of wall frequency
    DANGER = "danger"                # 90-99% of wall frequency
    CRITICAL = "critical"            # 99-100% of wall frequency
    BEYOND_WALL = "beyond_wall"      # >= 100% of wall frequency


@dataclass
class WallStatus:
    """
    Status report for Wall of Reality proximity.
    
    Attributes:
        frequency: Current frequency (Hz)
        wall_frequency: Wall of Reality frequency (Hz)
        distance_ratio: Ratio of current to wall frequency
        proximity: Proximity classification
        nrci_risk: Estimated NRCI collapse risk (0-1)
        is_safe: Whether operation is safe
        warnings: List of warning messages
    """
    frequency: float
    wall_frequency: float
    distance_ratio: float
    proximity: WallProximity
    nrci_risk: float
    is_safe: bool
    warnings: List[str]


class WallOfReality:
    """
    Wall of Reality detector and enforcement system.
    
    Monitors frequency operations and detects proximity to the fundamental
    computational limit at 10¹² Hz.
    """
    
    # Wall of Reality frequency (1 THz)
    WALL_FREQUENCY = 1e12  # Hz
    
    # Proximity thresholds (as fraction of wall frequency)
    THRESHOLD_SAFE = 0.5
    THRESHOLD_CAUTION = 0.8
    THRESHOLD_WARNING = 0.9
    THRESHOLD_DANGER = 0.99
    THRESHOLD_CRITICAL = 0.999
    
    # NRCI collapse parameters
    NRCI_COLLAPSE_THRESHOLD = 0.1  # NRCI below this indicates collapse
    NRCI_COLLAPSE_RATE = 10.0  # Exponential collapse rate near wall
    
    def __init__(
        self,
        wall_frequency: Optional[float] = None,
        enforce_limit: bool = False  # Changed to False - wall is theory/warning only, not enforcement
    ):
        """
        Initialize Wall of Reality detector.
        
        Args:
            wall_frequency: Wall frequency (defaults to 1 THz)
            enforce_limit: Whether to enforce frequency limits (default False - warning only)
        """
        self.wall_frequency = wall_frequency if wall_frequency is not None else self.WALL_FREQUENCY
        self.enforce_limit = enforce_limit
        
        self.detection_history: List[WallStatus] = []
    
    def check_frequency_limit(self, frequency: float) -> bool:
        """
        Check if frequency is within safe limits.
        
        Args:
            frequency: Frequency to check (Hz)
            
        Returns:
            True if frequency is safe (< wall frequency)
        """
        return frequency < self.wall_frequency
    
    def calculate_distance_ratio(self, frequency: float) -> float:
        """
        Calculate ratio of frequency to wall frequency.
        
        Args:
            frequency: Current frequency (Hz)
            
        Returns:
            Ratio (0-1 is safe, >1 is beyond wall)
        """
        return frequency / self.wall_frequency
    
    def classify_proximity(self, distance_ratio: float) -> WallProximity:
        """
        Classify proximity to wall based on distance ratio.
        
        Args:
            distance_ratio: Ratio of frequency to wall frequency
            
        Returns:
            WallProximity classification
        """
        if distance_ratio >= 1.0:
            return WallProximity.BEYOND_WALL
        elif distance_ratio >= self.THRESHOLD_CRITICAL:
            return WallProximity.CRITICAL
        elif distance_ratio >= self.THRESHOLD_DANGER:
            return WallProximity.DANGER
        elif distance_ratio >= self.THRESHOLD_WARNING:
            return WallProximity.WARNING
        elif distance_ratio >= self.THRESHOLD_CAUTION:
            return WallProximity.CAUTION
        else:
            return WallProximity.SAFE
    
    def calculate_nrci_collapse_risk(
        self,
        frequency: float,
        current_nrci: Optional[float] = None
    ) -> float:
        """
        Calculate NRCI collapse risk based on frequency proximity to wall.
        
        Risk increases exponentially as frequency approaches wall.
        
        Args:
            frequency: Current frequency (Hz)
            current_nrci: Current NRCI value (optional)
            
        Returns:
            Collapse risk (0-1, where 1 is certain collapse)
        """
        distance_ratio = self.calculate_distance_ratio(frequency)
        
        if distance_ratio >= 1.0:
            # Beyond wall - collapse is certain
            return 1.0
        
        # Exponential risk increase near wall
        # Risk = 1 - exp(-rate * (ratio - threshold))
        if distance_ratio > self.THRESHOLD_WARNING:
            excess = distance_ratio - self.THRESHOLD_WARNING
            risk = 1.0 - math.exp(-self.NRCI_COLLAPSE_RATE * excess)
        else:
            risk = 0.0
        
        # If current NRCI is provided, adjust risk based on actual coherence
        if current_nrci is not None:
            if current_nrci < self.NRCI_COLLAPSE_THRESHOLD:
                risk = max(risk, 0.9)  # High risk if NRCI already low
        
        return risk
    
    def detect_wall_approach(
        self,
        frequency: float,
        current_nrci: Optional[float] = None
    ) -> WallStatus:
        """
        Detect and analyze approach to Wall of Reality.
        
        Args:
            frequency: Current frequency (Hz)
            current_nrci: Current NRCI value (optional)
            
        Returns:
            WallStatus with detailed analysis
        """
        distance_ratio = self.calculate_distance_ratio(frequency)
        proximity = self.classify_proximity(distance_ratio)
        nrci_risk = self.calculate_nrci_collapse_risk(frequency, current_nrci)
        is_safe = proximity in [WallProximity.SAFE, WallProximity.CAUTION]
        
        # Generate warnings
        warnings_list = []
        
        if proximity == WallProximity.BEYOND_WALL:
            warnings_list.append(
                f"CRITICAL: Frequency {frequency:.2e} Hz exceeds Wall of Reality "
                f"({self.wall_frequency:.2e} Hz). NRCI collapse imminent."
            )
        elif proximity == WallProximity.CRITICAL:
            warnings_list.append(
                f"CRITICAL: Frequency {frequency:.2e} Hz is {distance_ratio*100:.1f}% "
                f"of Wall limit. Immediate action required."
            )
        elif proximity == WallProximity.DANGER:
            warnings_list.append(
                f"DANGER: Frequency {frequency:.2e} Hz approaching Wall of Reality. "
                f"NRCI collapse risk: {nrci_risk*100:.1f}%"
            )
        elif proximity == WallProximity.WARNING:
            warnings_list.append(
                f"WARNING: Frequency {frequency:.2e} Hz at {distance_ratio*100:.1f}% "
                f"of Wall limit. Reduce frequency."
            )
        elif proximity == WallProximity.CAUTION:
            warnings_list.append(
                f"CAUTION: Frequency {frequency:.2e} Hz at {distance_ratio*100:.1f}% "
                f"of Wall limit. Monitor closely."
            )
        
        if current_nrci is not None and current_nrci < self.NRCI_COLLAPSE_THRESHOLD:
            warnings_list.append(
                f"NRCI collapse detected: {current_nrci:.6f} < {self.NRCI_COLLAPSE_THRESHOLD}"
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
        operation_freq: float,
        raise_error: bool = True
    ) -> bool:
        """
        Enforce computational limit by preventing operations beyond wall.
        
        Args:
            operation_freq: Requested operation frequency (Hz)
            raise_error: Whether to raise exception if limit exceeded
            
        Returns:
            True if operation is allowed
            
        Raises:
            ValueError: If frequency exceeds limit and raise_error is True
        """
        if not self.enforce_limit:
            return True
        
        status = self.detect_wall_approach(operation_freq)
        
        if status.proximity == WallProximity.BEYOND_WALL:
            if raise_error:
                raise ValueError(
                    f"Operation frequency {operation_freq:.2e} Hz exceeds "
                    f"Wall of Reality ({self.wall_frequency:.2e} Hz). "
                    f"This violates fundamental computational limits. "
                    f"Maximum safe frequency: {self.wall_frequency * 0.9:.2e} Hz"
                )
            return False
        
        if status.proximity in [WallProximity.CRITICAL, WallProximity.DANGER]:
            warnings.warn(
                f"Operation frequency {operation_freq:.2e} Hz is dangerously "
                f"close to Wall of Reality. NRCI collapse risk: {status.nrci_risk*100:.1f}%",
                UserWarning
            )
        
        return True
    
    def get_wall_distance(self, current_freq: float) -> Dict[str, float]:
        """
        Get distance metrics to Wall of Reality.
        
        Args:
            current_freq: Current frequency (Hz)
            
        Returns:
            Dictionary with distance metrics
        """
        distance_ratio = self.calculate_distance_ratio(current_freq)
        distance_hz = self.wall_frequency - current_freq
        distance_percent = (1.0 - distance_ratio) * 100
        
        return {
            'current_frequency_hz': current_freq,
            'wall_frequency_hz': self.wall_frequency,
            'distance_hz': distance_hz,
            'distance_ratio': distance_ratio,
            'distance_percent': distance_percent,
            'safe_margin_hz': self.wall_frequency * 0.9 - current_freq
        }
    
    def get_safe_frequency_range(self) -> Tuple[float, float]:
        """
        Get safe frequency range for operations.
        
        Returns:
            Tuple of (min_safe_freq, max_safe_freq) in Hz
        """
        min_safe = 0.0  # No lower limit
        max_safe = self.wall_frequency * self.THRESHOLD_WARNING  # 90% of wall
        
        return min_safe, max_safe


def detect_wall_approach(
    frequency: float,
    threshold_ratio: float = 0.9
) -> Tuple[bool, float]:
    """
    Simple wall approach detection function.
    
    Args:
        frequency: Frequency to check (Hz)
        threshold_ratio: Warning threshold (default 0.9 = 90% of wall)
        
    Returns:
        Tuple of (is_approaching, distance_ratio)
    """
    wall = WallOfReality()
    distance_ratio = wall.calculate_distance_ratio(frequency)
    is_approaching = distance_ratio >= threshold_ratio
    
    return is_approaching, distance_ratio


def check_frequency_limit(frequency: float) -> bool:
    """
    Simple frequency limit check.
    
    Args:
        frequency: Frequency to check (Hz)
        
    Returns:
        True if frequency is safe
    """
    return frequency < WallOfReality.WALL_FREQUENCY


def demonstrate_wall_of_reality():
    """
    Demonstrate Wall of Reality detection and analysis.
    
    Returns:
        Dictionary with demonstration results
    """
    print("=" * 80)
    print("WALL OF REALITY DEMONSTRATION")
    print("=" * 80)
    
    wall = WallOfReality()
    
    print(f"\nWall of Reality Frequency: {wall.wall_frequency:.2e} Hz (1 THz)")
    print(f"Fundamental computational limit of the Bitfield")
    
    # Test frequencies at different proximities
    test_frequencies = [
        1e9,    # 1 GHz - safe
        1e11,   # 100 GHz - caution
        5e11,   # 500 GHz - warning
        9e11,   # 900 GHz - danger
        9.9e11, # 990 GHz - critical
        1.1e12, # 1.1 THz - beyond wall
    ]
    
    print("\n" + "-" * 80)
    print("Frequency Proximity Analysis:")
    print("-" * 80)
    
    results = []
    for freq in test_frequencies:
        status = wall.detect_wall_approach(freq)
        results.append(status)
        
        print(f"\nFrequency: {freq:.2e} Hz")
        print(f"  Distance Ratio: {status.distance_ratio:.4f} ({status.distance_ratio*100:.1f}%)")
        print(f"  Proximity: {status.proximity.value.upper()}")
        print(f"  NRCI Collapse Risk: {status.nrci_risk*100:.1f}%")
        print(f"  Safe: {status.is_safe}")
        
        if status.warnings:
            print(f"  Warnings:")
            for warning in status.warnings:
                print(f"    - {warning}")
    
    # Demonstrate safe frequency range
    print("\n" + "-" * 80)
    print("Safe Operating Range:")
    print("-" * 80)
    
    min_safe, max_safe = wall.get_safe_frequency_range()
    print(f"Minimum: {min_safe:.2e} Hz")
    print(f"Maximum: {max_safe:.2e} Hz ({max_safe/1e12*100:.1f}% of wall)")
    print(f"Recommended: Stay below {max_safe:.2e} Hz for safe operation")
    
    # Demonstrate distance metrics
    print("\n" + "-" * 80)
    print("Distance Metrics (for 500 GHz operation):")
    print("-" * 80)
    
    test_freq = 5e11
    distance = wall.get_wall_distance(test_freq)
    print(f"Current Frequency: {distance['current_frequency_hz']:.2e} Hz")
    print(f"Wall Frequency: {distance['wall_frequency_hz']:.2e} Hz")
    print(f"Distance: {distance['distance_hz']:.2e} Hz ({distance['distance_percent']:.1f}%)")
    print(f"Safe Margin: {distance['safe_margin_hz']:.2e} Hz")
    
    print("\n" + "=" * 80)
    
    return {
        'wall': wall,
        'test_results': results,
        'safe_range': (min_safe, max_safe),
        'distance_metrics': distance
    }


if __name__ == "__main__":
    # Run demonstration when module is executed directly
    results = demonstrate_wall_of_reality()
    
    print("\nWall of Reality demonstration complete.")
    print("The 1 THz limit is not arbitrary - it is where NRCI collapses.")
    print("This represents the fundamental computational limit of the Bitfield.")
    print("\nModule ready for import into UBP 3.4 system.")
