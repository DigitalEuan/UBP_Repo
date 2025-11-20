#!/usr/bin/env python3.11
"""
================================================================================
UBP 3.6 Turbine Blade Thermal Coherence Valley Analysis
Author: Euan Craig, New Zealand
Date: November 20, 2025
================================================================================

Analyzes turbine blade thermal gradients using IDENTICAL methodology to viral analysis:
- 24-bit quantization of ΔT (temperature gradients)
- 1000-step resonance_toggle simulation
- k = 0.0002 ± 0.00006 sinusoidal fluctuation
- 14-28 THz frequency range
- Target NRCI > 99.99%

CRITICAL: This uses the EXACT SAME pipeline as viral analysis to demonstrate isomorphism.
"""

import os
import json
import numpy as np
from typing import List, Dict, Any, Tuple
import sys
sys.path.insert(0, '.')
import importlib
resonance_sim = importlib.import_module('01_proper_resonance_toggle_simulation')

# Import functions
quantize_to_24bit = resonance_sim.quantize_to_24bit
run_resonance_simulation = resonance_sim.run_resonance_simulation
detect_coherence_valleys = resonance_sim.detect_coherence_valleys
FREQ_MIN_THZ = resonance_sim.FREQ_MIN_THZ
FREQ_MAX_THZ = resonance_sim.FREQ_MAX_THZ

# ============================================================================
# TURBINE BLADE CONFIGURATIONS (Based on NASA/GE/Rolls-Royce Data)
# ============================================================================

BLADE_CONFIGURATIONS = [
    {
        "name": "NASA_PWA1480_Standard",
        "description": "NASA PWA1480 single crystal superalloy",
        "T_hot_K": 1673,  # 1400°C hot section
        "T_cool_K": 873,  # 600°C cooled section
        "gradient_zones": 10,  # Number of thermal zones
        "material": "PWA1480",
        "cooling": "Internal passages"
    },
    {
        "name": "GE_Film_Cooled",
        "description": "GE film-cooled turbine blade",
        "T_hot_K": 1773,  # 1500°C hot section
        "T_cool_K": 773,  # 500°C film cooled
        "gradient_zones": 12,
        "material": "René N5",
        "cooling": "Film cooling + internal"
    },
    {
        "name": "RR_Single_Crystal",
        "description": "Rolls-Royce single crystal blade",
        "T_hot_K": 1723,  # 1450°C
        "T_cool_K": 823,  # 550°C
        "gradient_zones": 10,
        "material": "CMSX-4",
        "cooling": "Serpentine passages"
    },
    {
        "name": "High_Stress_Configuration",
        "description": "High thermal stress configuration",
        "T_hot_K": 1873,  # 1600°C extreme
        "T_cool_K": 723,  # 450°C aggressive cooling
        "gradient_zones": 15,
        "material": "CMSX-10",
        "cooling": "Advanced multi-pass"
    },
    {
        "name": "Ceramic_Coated",
        "description": "Thermal barrier coated blade",
        "T_hot_K": 1973,  # 1700°C with TBC
        "T_cool_K": 1073,  # 800°C substrate
        "gradient_zones": 8,
        "material": "René N6 + YSZ TBC",
        "cooling": "TBC + internal"
    },
    {
        "name": "Advanced_Cooling",
        "description": "Next-gen cooling architecture",
        "T_hot_K": 1823,  # 1550°C
        "T_cool_K": 773,  # 500°C
        "gradient_zones": 20,  # Fine-grained cooling
        "material": "CMSX-486",
        "cooling": "Micro-channel array"
    }
]

# ============================================================================
# THERMAL GRADIENT GENERATION
# ============================================================================

def generate_thermal_gradient(T_hot: float, T_cool: float, zones: int) -> np.ndarray:
    """
    Generate realistic thermal gradient across blade.
    
    Uses exponential decay model typical of turbine blade cooling:
    T(x) = T_cool + (T_hot - T_cool) * exp(-λx)
    
    Args:
        T_hot: Hot section temperature (K)
        T_cool: Cooled section temperature (K)
        zones: Number of thermal zones
        
    Returns:
        Array of temperatures (K)
    """
    # Exponential decay constant (typical for turbine blades)
    lambda_decay = 3.0
    
    # Position along blade (0 to 1)
    x = np.linspace(0, 1, zones)
    
    # Exponential temperature profile
    T = T_cool + (T_hot - T_cool) * np.exp(-lambda_decay * x)
    
    return T


def calculate_temperature_gradients(temperatures: np.ndarray) -> np.ndarray:
    """
    Calculate temperature gradients (ΔT) between adjacent zones.
    
    Args:
        temperatures: Array of temperatures (K)
        
    Returns:
        Array of temperature gradients (K)
    """
    # Calculate differences between adjacent zones
    gradients = np.diff(temperatures)
    
    # Take absolute values (magnitude of gradient)
    gradients = np.abs(gradients)
    
    return gradients


def temperature_gradient_to_frequency(delta_T: float, T_min: float, T_max: float,
                                     freq_min_thz: float = FREQ_MIN_THZ,
                                     freq_max_thz: float = FREQ_MAX_THZ) -> float:
    """
    Map temperature gradient to frequency in THz range.
    
    Physical basis: Thermal phonon frequencies scale with temperature.
    Higher gradients → higher phonon frequencies.
    
    Args:
        delta_T: Temperature gradient (K)
        T_min: Minimum gradient in dataset (K)
        T_max: Maximum gradient in dataset (K)
        freq_min_thz: Minimum frequency (THz)
        freq_max_thz: Maximum frequency (THz)
        
    Returns:
        Frequency (THz)
    """
    # Normalize gradient to [0, 1]
    normalized = (delta_T - T_min) / (T_max - T_min)
    normalized = max(0.0, min(1.0, normalized))
    
    # Map to frequency range
    frequency = freq_min_thz + normalized * (freq_max_thz - freq_min_thz)
    
    return frequency


# ============================================================================
# BLADE THERMAL COHERENCE ANALYSIS
# ============================================================================

def analyze_blade_configuration(config: Dict[str, Any], verbose: bool = False) -> Dict[str, Any]:
    """
    Analyze a single turbine blade configuration for coherence valleys.
    
    Uses IDENTICAL pipeline to viral analysis:
    1. Generate thermal gradient (ΔT)
    2. Quantize to 24-bit
    3. Run 1000-step resonance_toggle
    4. Detect coherence valleys
    
    Args:
        config: Blade configuration dictionary
        verbose: Print progress
        
    Returns:
        Dictionary with analysis results
    """
    if verbose:
        print(f"\nAnalyzing: {config['name']}")
        print(f"  Description: {config['description']}")
        print(f"  T_hot: {config['T_hot_K']} K")
        print(f"  T_cool: {config['T_cool_K']} K")
        print(f"  Zones: {config['gradient_zones']}")
    
    # Generate thermal gradient
    temperatures = generate_thermal_gradient(
        config['T_hot_K'],
        config['T_cool_K'],
        config['gradient_zones']
    )
    
    # Calculate temperature gradients (ΔT)
    delta_T = calculate_temperature_gradients(temperatures)
    
    if verbose:
        print(f"  ΔT range: {delta_T.min():.1f} - {delta_T.max():.1f} K")
        print(f"  Mean ΔT: {delta_T.mean():.1f} K")
    
    # Find global min/max for normalization
    T_min = delta_T.min()
    T_max = delta_T.max()
    
    # Convert gradients to frequencies
    frequencies = [temperature_gradient_to_frequency(dt, T_min, T_max) 
                   for dt in delta_T]
    avg_frequency = sum(frequencies) / len(frequencies)
    
    if verbose:
        print(f"  Frequency range: {min(frequencies):.2f} - {max(frequencies):.2f} THz")
        print(f"  Average frequency: {avg_frequency:.2f} THz")
    
    # Run resonance simulation for each gradient
    results = []
    for i, (dt, freq_thz) in enumerate(zip(delta_T, frequencies)):
        # Quantize ΔT to 24-bit (CRITICAL: same as viral analysis)
        quantized = quantize_to_24bit(dt, T_min, T_max)
        
        # Run 1000-step resonance_toggle (IDENTICAL to viral)
        offbit, stats = run_resonance_simulation(quantized, freq_thz, verbose=False)
        
        results.append(stats)
        
        if verbose and (i + 1) % 5 == 0:
            print(f"    Processed {i+1}/{len(delta_T)} gradients")
    
    # Aggregate results
    avg_deficit = sum(r['coherence_valley_deficit_percent'] for r in results) / len(results)
    min_deficit = min(r['coherence_valley_deficit_percent'] for r in results)
    max_deficit = max(r['coherence_valley_deficit_percent'] for r in results)
    avg_nrci = sum(r['final_nrci'] for r in results) / len(results)
    
    analysis = {
        'blade_name': config['name'],
        'description': config['description'],
        'T_hot_K': config['T_hot_K'],
        'T_cool_K': config['T_cool_K'],
        'delta_T_K': config['T_hot_K'] - config['T_cool_K'],
        'gradient_zones': config['gradient_zones'],
        'material': config['material'],
        'cooling': config['cooling'],
        'average_frequency_thz': avg_frequency,
        'samples_analyzed': len(results),
        'coherence_valley_deficit_percent': avg_deficit,
        'deficit_min': min_deficit,
        'deficit_max': max_deficit,
        'average_final_nrci': avg_nrci,
        'nrci_target_met': avg_nrci >= 0.9999,
        'detailed_results': results
    }
    
    if verbose:
        print(f"  Coherence valley deficit: {avg_deficit:.6f}%")
        print(f"  Average final NRCI: {avg_nrci:.10f}")
        print(f"  Target met: {analysis['nrci_target_met']}")
    
    return analysis


# ============================================================================
# BATCH ANALYSIS
# ============================================================================

def analyze_all_blade_configurations(output_file: str) -> List[Dict[str, Any]]:
    """
    Analyze all turbine blade configurations.
    
    Args:
        output_file: Path to save results JSON
        
    Returns:
        List of analysis results
    """
    print("=" * 80)
    print(f"Analyzing {len(BLADE_CONFIGURATIONS)} turbine blade configurations")
    print("=" * 80)
    
    all_results = []
    
    for i, config in enumerate(BLADE_CONFIGURATIONS, 1):
        print(f"\n[{i}/{len(BLADE_CONFIGURATIONS)}] {config['name']}")
        
        try:
            result = analyze_blade_configuration(config, verbose=True)
            all_results.append(result)
        except Exception as e:
            print(f"  ERROR: {e}")
            import traceback
            traceback.print_exc()
            continue
    
    # Save results
    print()
    print("=" * 80)
    print("Saving results")
    print("=" * 80)
    
    # Remove detailed_results for summary (too large)
    summary_results = []
    for result in all_results:
        summary = {k: v for k, v in result.items() if k != 'detailed_results'}
        summary_results.append(summary)
    
    with open(output_file, 'w') as f:
        json.dump(summary_results, f, indent=2)
    
    print(f"Saved: {output_file}")
    
    # Print summary statistics
    print()
    print("=" * 80)
    print("SUMMARY STATISTICS")
    print("=" * 80)
    
    deficits = [r['coherence_valley_deficit_percent'] for r in all_results]
    nrcis = [r['average_final_nrci'] for r in all_results]
    
    print(f"Total blade configurations analyzed: {len(all_results)}")
    print()
    print(f"Coherence valley deficit:")
    print(f"  Mean: {sum(deficits)/len(deficits):.6f}%")
    print(f"  Min: {min(deficits):.6f}%")
    print(f"  Max: {max(deficits):.6f}%")
    print(f"  Std dev: {(sum((d - sum(deficits)/len(deficits))**2 for d in deficits) / len(deficits))**0.5:.6f}%")
    print()
    print(f"Average final NRCI:")
    print(f"  Mean: {sum(nrcis)/len(nrcis):.10f}")
    print(f"  Min: {min(nrcis):.10f}")
    print(f"  Max: {max(nrcis):.10f}")
    print()
    print(f"NRCI > 99.99% target met: {sum(1 for r in all_results if r['nrci_target_met'])}/{len(all_results)}")
    
    return all_results


# ============================================================================
# MAIN
# ============================================================================

def main():
    """
    Main execution function.
    """
    # Setup directories
    results_dir = "../results"
    os.makedirs(results_dir, exist_ok=True)
    
    # Analyze blade configurations
    results = analyze_all_blade_configurations(
        os.path.join(results_dir, "turbine_blade_coherence_valleys.json")
    )
    
    print()
    print("=" * 80)
    print("Analysis complete!")
    print("=" * 80)


if __name__ == "__main__":
    main()
