#!/usr/bin/env python3.11
"""
================================================================================
UBP 3.6 Proper OffBit Resonance Toggle Simulation
Author: Euan Craig, New Zealand
Date: November 20, 2025
================================================================================

Implements the CORRECT resonance_toggle methodology from UBP 3.6 Manual Section 4:
- 1000-step simulation (not 50 or 100)
- k = 0.0002 ± 0.00006 sinusoidal fluctuation
- 24-bit quantization of input → OffBit streams
- 14-28 THz frequency range (not 8-28 THz)
- Target NRCI > 99.99% (0.9999)

This is the foundation for both viral and thermal analyses.
"""

import math
import json
from typing import List, Tuple, Dict, Any
from state import OffBit
from toggle_ops import resonance_toggle, resonance_kernel
from coherence_substrate import CoherenceState

# ============================================================================
# CRITICAL PARAMETERS (From User Requirements)
# ============================================================================

SIMULATION_STEPS = 1000  # 1000-step simulation (non-negotiable)
K_BASE = 0.0002          # Base decay constant
K_FLUCTUATION = 0.00006  # ± fluctuation amplitude
FREQ_MIN_THZ = 14.0      # 14 THz minimum (not 8 THz)
FREQ_MAX_THZ = 28.0      # 28 THz maximum
TARGET_NRCI = 0.9999     # 99.99% target (not 99.9997%)
TIME_STEP_NS = 1e-9      # 1 nanosecond time steps

# ============================================================================
# 24-BIT QUANTIZATION
# ============================================================================

def quantize_to_24bit(value: float, min_val: float, max_val: float) -> int:
    """
    Quantize a float value to 24-bit integer (0 to 0xFFFFFF).
    
    This is the critical step that converts continuous values
    (genome sequences, temperature gradients) into OffBit streams.
    
    Args:
        value: Value to quantize
        min_val: Minimum value in range
        max_val: Maximum value in range
        
    Returns:
        24-bit integer (0 to 16777215)
    """
    # Normalize to [0, 1]
    normalized = (value - min_val) / (max_val - min_val)
    normalized = max(0.0, min(1.0, normalized))  # Clamp
    
    # Scale to 24-bit range
    quantized = int(normalized * 0xFFFFFF)
    
    return quantized


def dequantize_from_24bit(quantized: int, min_val: float, max_val: float) -> float:
    """
    Dequantize a 24-bit integer back to float value.
    
    Args:
        quantized: 24-bit integer
        min_val: Minimum value in range
        max_val: Maximum value in range
        
    Returns:
        Dequantized float value
    """
    # Normalize from 24-bit range
    normalized = quantized / 0xFFFFFF
    
    # Scale back to original range
    value = min_val + normalized * (max_val - min_val)
    
    return value


# ============================================================================
# SINUSOIDAL K FLUCTUATION
# ============================================================================

def get_k_with_fluctuation(step: int, total_steps: int) -> float:
    """
    Calculate k with sinusoidal fluctuation.
    
    k(t) = k_base + k_fluctuation × sin(2π × t / T)
    
    Args:
        step: Current step (0 to total_steps-1)
        total_steps: Total number of steps
        
    Returns:
        k value with fluctuation
    """
    # Sinusoidal fluctuation over the full simulation
    phase = 2.0 * math.pi * step / total_steps
    fluctuation = K_FLUCTUATION * math.sin(phase)
    
    k = K_BASE + fluctuation
    
    return k


# ============================================================================
# 1000-STEP RESONANCE TOGGLE SIMULATION
# ============================================================================

def run_resonance_simulation(
    initial_value: int,
    frequency_thz: float,
    steps: int = SIMULATION_STEPS,
    verbose: bool = False
) -> Tuple[OffBit, Dict[str, Any]]:
    """
    Run full 1000-step resonance_toggle simulation.
    
    This is the CORRECT implementation per UBP 3.6 Manual Section 4.
    
    Args:
        initial_value: Initial 24-bit value (0 to 0xFFFFFF)
        frequency_thz: Frequency in THz (14-28 THz)
        steps: Number of simulation steps (default 1000)
        verbose: Print progress
        
    Returns:
        Tuple of (final_offbit, statistics_dict)
    """
    # Convert frequency from THz to Hz
    frequency_hz = frequency_thz * 1e12
    
    # Initialize OffBit
    offbit = OffBit(initial_value)
    
    # Track statistics
    nrci_history = [offbit.nrci]
    k_history = []
    resonance_factor_history = []
    
    # Run 1000-step simulation
    for step in range(steps):
        # CRITICAL FIX: Use phase (0 to 1) instead of absolute time
        # This prevents the distance parameter from growing unbounded
        # Phase represents position in the resonance cycle
        phase = step / steps  # 0 to 1 over simulation
        
        # Time parameter for resonance_toggle (calibrated for coherence valleys)
        # Target: Create 0.01-0.15% deficits while maintaining NRCI > 99.99%
        # Use attosecond scale (10^-18 s) for subtle coherence variations
        # This is 1000x smaller than femtoseconds, allowing fine-grained control
        time_s = phase * 1e-13  # 0 to 0.1 picoseconds (100 femtoseconds)
        
        # Get k with sinusoidal fluctuation
        k = get_k_with_fluctuation(step, steps)
        k_history.append(k)
        
        # Apply resonance_toggle
        offbit = resonance_toggle(
            offbit,
            frequency=frequency_hz,
            time=time_s,
            k=k,
            max_history=steps  # Keep full history
        )
        
        # Track NRCI
        nrci_history.append(offbit.nrci)
        
        # Track resonance factor
        if offbit.resonance_history:
            _, _, rf = offbit.resonance_history[-1]
            resonance_factor_history.append(rf)
        
        # Progress
        if verbose and (step + 1) % 100 == 0:
            print(f"  Step {step+1}/{steps}: NRCI = {offbit.nrci:.10f}")
    
    # Calculate coherence valley deficit (peak-to-valley)
    # This is the KEY metric for the isomorphism study
    rf_max = max(resonance_factor_history)
    rf_min = min(resonance_factor_history)
    coherence_valley_deficit = rf_max - rf_min
    coherence_valley_deficit_percent = 100.0 * coherence_valley_deficit
    
    # Calculate statistics
    stats = {
        'initial_value': initial_value,
        'frequency_thz': frequency_thz,
        'steps': steps,
        'final_nrci': offbit.nrci,
        'initial_nrci': nrci_history[0],
        'nrci_degradation': nrci_history[0] - offbit.nrci,
        'nrci_degradation_percent': 100.0 * (nrci_history[0] - offbit.nrci) / nrci_history[0],
        'min_nrci': min(nrci_history),
        'max_nrci': max(nrci_history),
        'avg_nrci': sum(nrci_history) / len(nrci_history),
        'k_min': min(k_history),
        'k_max': max(k_history),
        'k_avg': sum(k_history) / len(k_history),
        'resonance_factor_min': min(resonance_factor_history),
        'resonance_factor_max': max(resonance_factor_history),
        'resonance_factor_avg': sum(resonance_factor_history) / len(resonance_factor_history),
        'coherence_valley_deficit': coherence_valley_deficit,
        'coherence_valley_deficit_percent': coherence_valley_deficit_percent,
        'resonance_history_length': offbit.resonance_history_length,
        'target_nrci_met': offbit.nrci >= TARGET_NRCI
    }
    
    return offbit, stats


# ============================================================================
# COHERENCE VALLEY DETECTION
# ============================================================================

def detect_coherence_valleys(offbit: OffBit, window_size: int = 5) -> List[Dict[str, Any]]:
    """
    Detect coherence valleys in resonance history.
    
    Uses the OffBit.get_coherence_valleys() method from UBP 3.6.
    
    Args:
        offbit: OffBit with resonance history
        window_size: Window size for local minimum detection
        
    Returns:
        List of valley dictionaries with detailed information
    """
    valleys = offbit.get_coherence_valleys(window_size=window_size)
    
    valley_details = []
    for idx, resonance_factor in valleys:
        time, frequency, _ = offbit.resonance_history[idx]
        
        valley_details.append({
            'index': idx,
            'time_ns': time * 1e9,
            'frequency_thz': frequency / 1e12,
            'resonance_factor': resonance_factor,
            'coherence_deficit_percent': 100.0 * (1.0 - resonance_factor)
        })
    
    return valley_details


# ============================================================================
# EXAMPLE USAGE
# ============================================================================

def test_proper_resonance_toggle():
    """
    Test the proper resonance_toggle implementation.
    """
    print("=" * 80)
    print("UBP 3.6 Proper Resonance Toggle Simulation")
    print("=" * 80)
    print()
    
    # Test parameters
    test_value = 0x800000  # Mid-range 24-bit value
    test_frequency = 21.0  # THz (middle of 14-28 THz range)
    
    print(f"Initial value: 0x{test_value:06X} ({test_value})")
    print(f"Frequency: {test_frequency} THz")
    print(f"Simulation steps: {SIMULATION_STEPS}")
    print(f"k_base: {K_BASE}")
    print(f"k_fluctuation: ±{K_FLUCTUATION}")
    print(f"Target NRCI: {TARGET_NRCI} (99.99%)")
    print()
    
    # Run simulation
    print("Running 1000-step simulation...")
    offbit, stats = run_resonance_simulation(
        test_value,
        test_frequency,
        verbose=True
    )
    
    print()
    print("=" * 80)
    print("SIMULATION RESULTS")
    print("=" * 80)
    print(f"Final NRCI: {stats['final_nrci']:.10f}")
    print(f"Initial NRCI: {stats['initial_nrci']:.10f}")
    print(f"NRCI degradation: {stats['nrci_degradation']:.10f} ({stats['nrci_degradation_percent']:.6f}%)")
    print(f"Target NRCI met: {stats['target_nrci_met']}")
    print()
    print(f"NRCI range: [{stats['min_nrci']:.10f}, {stats['max_nrci']:.10f}]")
    print(f"Average NRCI: {stats['avg_nrci']:.10f}")
    print()
    print(f"k range: [{stats['k_min']:.6f}, {stats['k_max']:.6f}]")
    print(f"Average k: {stats['k_avg']:.6f}")
    print()
    print(f"Resonance factor range: [{stats['resonance_factor_min']:.10f}, {stats['resonance_factor_max']:.10f}]")
    print(f"Average resonance factor: {stats['resonance_factor_avg']:.10f}")
    print()
    print(f"COHERENCE VALLEY DEFICIT: {stats['coherence_valley_deficit_percent']:.6f}%")
    print(f"  (Peak-to-valley difference in resonance factors)")
    print()
    
    # Detect valleys
    print("=" * 80)
    print("COHERENCE VALLEY DETECTION")
    print("=" * 80)
    valleys = detect_coherence_valleys(offbit, window_size=5)
    print(f"Detected {len(valleys)} coherence valleys")
    print()
    
    if valleys:
        print("Top 10 valleys (by deficit):")
        sorted_valleys = sorted(valleys, key=lambda v: v['coherence_deficit_percent'], reverse=True)
        for i, valley in enumerate(sorted_valleys[:10], 1):
            print(f"  {i}. Step {valley['index']:4d}: "
                  f"deficit = {valley['coherence_deficit_percent']:.6f}%, "
                  f"RF = {valley['resonance_factor']:.10f}")
    
    print()
    print("=" * 80)
    print("Test complete!")
    print("=" * 80)
    
    return offbit, stats, valleys


if __name__ == "__main__":
    test_proper_resonance_toggle()
