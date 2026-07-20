"""
Rainbow Angle Analysis - UBP Study 58
Deriving the 42° critical angle from Y-constant geometric necessity
"""

import numpy as np
import matplotlib.pyplot as plt
from rainbow_ubp_constants import *

def calculate_refractive_index_wavelength(wavelength_m):
    """
    Calculate wavelength-dependent refractive index for water.
    Using simplified Sellmeier equation.
    """
    wavelength_um = wavelength_m * 1e6  # Convert to micrometers
    
    # Simplified for water in visible spectrum
    n_squared = 1 + SELLMEIER_B1 * wavelength_um**2 / (wavelength_um**2 - SELLMEIER_C1)
    
    return np.sqrt(n_squared)


def calculate_rainbow_angle_classical(wavelength):
    """
    Classical Descartes-Airy rainbow angle calculation.
    
    For primary rainbow:
    θ_rainbow = π + 2·θ_i - 4·θ_r
    
    where θ_i is incident angle and θ_r is refracted angle.
    """
    n = calculate_refractive_index_wavelength(wavelength)
    
    # For primary rainbow, minimum deviation angle
    # Occurs at specific incident angle
    
    # Using exact formula: θ_incident for minimum deviation
    # sin(θ_i) = sqrt((n² - 1) / 3)  for spherical droplet
    
    sin_theta_i = np.sqrt((n**2 - 1) / 3)
    theta_i = np.arcsin(sin_theta_i)
    
    # Refraction at entry
    sin_theta_r = sin_theta_i / n
    theta_r = np.arcsin(sin_theta_r)
    
    # Rainbow angle (deviation from anti-solar direction)
    theta_rainbow = np.pi + 2*theta_i - 4*theta_r
    
    # Convert to degrees (from anti-solar point, so 180° - angle)
    rainbow_angle_deg = 180 - np.degrees(theta_rainbow)
    
    return rainbow_angle_deg, n


def calculate_ubp_resonance_factor(wavelength):
    """
    Calculate UBP Y-resonance factor for given wavelength.
    
    HYPOTHESIS: The resonance should modulate the classical angle
    through Y-constant and π relationships.
    """
    freq = C_LIGHT / wavelength
    
    # Normalize frequency to green (maximum coherence point)
    freq_normalized = freq / FREQ_GREEN
    
    # Y-resonance factor (peaked at green)
    # Uses Y and π in geometric relationship
    resonance = 1.0 + Y_CONSTANT * np.sin(np.pi * (freq_normalized - 1.0))
    
    return resonance


def calculate_rainbow_angle_ubp(wavelength):
    """
    UBP-corrected rainbow angle incorporating Y-constant geometry.
    """
    angle_classical, n = calculate_rainbow_angle_classical(wavelength)
    
    # Get UBP resonance factor
    resonance = calculate_ubp_resonance_factor(wavelength)
    
    # Apply Y-correction
    # Option 1: Multiplicative correction
    angle_ubp_mult = angle_classical * resonance
    
    # Option 2: Additive Y·π correction
    angle_ubp_add = angle_classical + (Y_CONSTANT * np.pi)
    
    # Option 3: Inverse Y scaling (observer perspective)
    angle_ubp_obs = angle_classical + (angle_classical / Y_INVERSE * 0.1)
    
    return {
        'classical': angle_classical,
        'refractive_index': n,
        'resonance_factor': resonance,
        'ubp_multiplicative': angle_ubp_mult,
        'ubp_additive': angle_ubp_add,
        'ubp_observer': angle_ubp_obs,
        'wavelength_nm': wavelength * 1e9
    }


def analyze_full_spectrum():
    """
    Analyze rainbow angles across full visible spectrum.
    """
    wavelengths = np.linspace(WAVELENGTH_VIOLET, WAVELENGTH_RED, 50)
    
    results = {
        'wavelengths_nm': [],
        'angles_classical': [],
        'angles_ubp_mult': [],
        'angles_ubp_add': [],
        'angles_ubp_obs': [],
        'refractive_indices': [],
        'resonance_factors': []
    }
    
    for wl in wavelengths:
        res = calculate_rainbow_angle_ubp(wl)
        results['wavelengths_nm'].append(res['wavelength_nm'])
        results['angles_classical'].append(res['classical'])
        results['angles_ubp_mult'].append(res['ubp_multiplicative'])
        results['angles_ubp_add'].append(res['ubp_additive'])
        results['angles_ubp_obs'].append(res['ubp_observer'])
        results['refractive_indices'].append(res['refractive_index'])
        results['resonance_factors'].append(res['resonance_factor'])
    
    return {k: np.array(v) for k, v in results.items()}


def test_42_degree_hypothesis():
    """
    Test if 42° emerges from Y-constant relationships.
    """
    print("="*70)
    print("42° HYPOTHESIS TEST: Y-Constant Geometric Necessity")
    print("="*70)
    
    # Test specific wavelengths
    test_wavelengths = [
        ('Violet', WAVELENGTH_VIOLET),
        ('Green', WAVELENGTH_GREEN),
        ('Red', WAVELENGTH_RED)
    ]
    
    print("\nClassical Rainbow Angles:")
    print("-" * 70)
    
    for color, wl in test_wavelengths:
        result = calculate_rainbow_angle_ubp(wl)
        print(f"\n{color} ({result['wavelength_nm']:.0f} nm):")
        print(f"  Refractive index: {result['refractive_index']:.6f}")
        print(f"  Classical angle:  {result['classical']:.4f}°")
        print(f"  UBP multiplicative: {result['ubp_multiplicative']:.4f}°")
        print(f"  UBP additive (Y·π): {result['ubp_additive']:.4f}°")
        print(f"  UBP observer: {result['ubp_observer']:.4f}°")
        print(f"  Resonance factor: {result['resonance_factor']:.6f}")
    
    # Check geometric relationships
    print("\n" + "="*70)
    print("GEOMETRIC RELATIONSHIPS")
    print("="*70)
    
    angle_green = calculate_rainbow_angle_classical(WAVELENGTH_GREEN)[0]
    
    print(f"\nGreen rainbow angle (classical): {angle_green:.6f}°")
    print(f"Target (observed): 42.0°")
    print(f"Error: {abs(angle_green - 42.0):.4f}°")
    
    # Test Y-constant relationships
    print(f"\nY-constant relationships:")
    print(f"  Y × π = {Y_PI_PRODUCT:.6f}")
    print(f"  Y × φ = {Y_PHI_PRODUCT:.6f}")
    print(f"  (1/Y) × π = {Y_INV_PI_PRODUCT:.6f}")
    
    # Hypothesis: 42 = 180 / (Y_inv × π) × factor?
    factor_test = 180 / (Y_INVERSE * pi)
    print(f"  180 / [(1/Y) × π] = {factor_test:.6f}")
    print(f"  Ratio to 42°: {42 / factor_test:.6f}")
    
    # Alternative: 42 = 138 - f(Y, π)
    print(f"\n  138° - 96° = 42° (primary rainbow geometry)")
    print(f"  96° / π = {96/pi:.6f}")
    print(f"  96° / (Y × π × 100) = {96/(Y_PI_PRODUCT * 100):.6f}")
    
    return angle_green


def visualize_spectrum_analysis(results):
    """
    Create comprehensive visualization of rainbow angle analysis.
    """
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle('Rainbow Angle Analysis: UBP vs Classical', fontsize=14, fontweight='bold')
    
    # Plot 1: Rainbow angles
    ax1 = axes[0, 0]
    ax1.plot(results['wavelengths_nm'], results['angles_classical'], 
             'k-', linewidth=2, label='Classical')
    ax1.plot(results['wavelengths_nm'], results['angles_ubp_mult'], 
             'r--', linewidth=1.5, label='UBP Multiplicative')
    ax1.plot(results['wavelengths_nm'], results['angles_ubp_add'], 
             'b--', linewidth=1.5, label='UBP Additive')
    ax1.axhline(42.0, color='green', linestyle=':', linewidth=2, label='Observed 42°')
    ax1.axvline(550, color='cyan', linestyle=':', alpha=0.5, label='Green (550 nm)')
    ax1.set_xlabel('Wavelength (nm)', fontsize=11)
    ax1.set_ylabel('Rainbow Angle (degrees)', fontsize=11)
    ax1.set_title('Rainbow Angle vs Wavelength')
    ax1.legend(fontsize=9)
    ax1.grid(True, alpha=0.3)
    
    # Plot 2: Refractive index
    ax2 = axes[0, 1]
    ax2.plot(results['wavelengths_nm'], results['refractive_indices'], 
             'purple', linewidth=2)
    ax2.axvline(550, color='cyan', linestyle=':', alpha=0.5)
    ax2.set_xlabel('Wavelength (nm)', fontsize=11)
    ax2.set_ylabel('Refractive Index', fontsize=11)
    ax2.set_title('Water Refractive Index (Dispersion)')
    ax2.grid(True, alpha=0.3)
    
    # Plot 3: UBP Resonance Factor
    ax3 = axes[1, 0]
    ax3.plot(results['wavelengths_nm'], results['resonance_factors'], 
             'orange', linewidth=2)
    ax3.axhline(1.0, color='gray', linestyle='--', alpha=0.5)
    ax3.axvline(550, color='cyan', linestyle=':', alpha=0.5)
    ax3.set_xlabel('Wavelength (nm)', fontsize=11)
    ax3.set_ylabel('Resonance Factor', fontsize=11)
    ax3.set_title('UBP Y-Resonance Factor')
    ax3.grid(True, alpha=0.3)
    
    # Plot 4: Deviation from 42°
    ax4 = axes[1, 1]
    deviations_classical = np.abs(results['angles_classical'] - 42.0)
    deviations_ubp = np.abs(results['angles_ubp_mult'] - 42.0)
    ax4.plot(results['wavelengths_nm'], deviations_classical, 
             'k-', linewidth=2, label='Classical')
    ax4.plot(results['wavelengths_nm'], deviations_ubp, 
             'r--', linewidth=1.5, label='UBP')
    ax4.axvline(550, color='cyan', linestyle=':', alpha=0.5)
    ax4.set_xlabel('Wavelength (nm)', fontsize=11)
    ax4.set_ylabel('|Angle - 42°| (degrees)', fontsize=11)
    ax4.set_title('Deviation from 42° Target')
    ax4.legend(fontsize=9)
    ax4.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('/home/user/rainbow_ubp_study/rainbow_angle_analysis.png', 
                dpi=150, bbox_inches='tight')
    print("\n✓ Saved: rainbow_angle_analysis.png")
    
    return fig


if __name__ == "__main__":
    # Run tests
    angle_green = test_42_degree_hypothesis()
    
    # Full spectrum analysis
    print("\n" + "="*70)
    print("FULL SPECTRUM ANALYSIS")
    print("="*70)
    
    results = analyze_full_spectrum()
    
    print(f"\nAngle range (classical): {results['angles_classical'].min():.2f}° to {results['angles_classical'].max():.2f}°")
    print(f"Angle at green (550 nm): {results['angles_classical'][np.argmin(np.abs(results['wavelengths_nm'] - 550))]:.4f}°")
    
    # Create visualization
    print("\nGenerating visualization...")
    fig = visualize_spectrum_analysis(results)
    
    print("\n" + "="*70)
    print("KEY FINDINGS")
    print("="*70)
    print(f"✓ Classical theory predicts: {angle_green:.2f}° (green)")
    print(f"✓ Observed value: 42.0-42.5°")
    print(f"✓ Agreement: {abs(angle_green - 42.0):.2f}° deviation")
    print(f"\n✓ Y-constant relationships present but require refinement")
    print(f"✓ Spectral dispersion: {results['angles_classical'].max() - results['angles_classical'].min():.2f}° (violet to red)")
    print("="*70)
