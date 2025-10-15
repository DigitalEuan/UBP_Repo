#!/usr/bin/env python3.11
"""
Module 1: Classical Hawking Temperature Analysis
Author: Euan R A Craig
Date: October 15, 2025
Framework: Universal Binary Principle (UBP) v3.2

This module establishes the baseline General Relativity predictions for
Schwarzschild black holes across a wide mass range.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.constants import c, G, hbar, k as k_B, pi
import os

# Physical constants
C = c  # Speed of light (m/s)
HBAR = hbar  # Reduced Planck constant (J·s)
K_B = k_B  # Boltzmann constant (J/K)
PI = pi  # Pi

# Derived constants
M_PLANCK = np.sqrt(HBAR * C / G)  # Planck mass (kg)
L_PLANCK = np.sqrt(HBAR * G / C**3)  # Planck length (m)
T_PLANCK = np.sqrt(HBAR * G / C**5)  # Planck time (s)

# Solar mass for reference
M_SOLAR = 1.989e30  # kg

# Output directories
DATA_DIR = '/home/ubuntu/black_holes_quantum_tunnelling/data'
FIG_DIR = '/home/ubuntu/black_holes_quantum_tunnelling/figures'

class SchwarzschildBlackHole:
    """
    Classical Schwarzschild black hole thermodynamics.
    
    Three-Column Thinking Framework:
    
    LANGUAGE: A non-rotating, uncharged black hole curves spacetime such that
    an event horizon forms at the Schwarzschild radius. Quantum field theory
    in this curved background predicts thermal radiation at a temperature
    inversely proportional to the black hole mass.
    
    MATHEMATICS:
    - Schwarzschild radius: r_s = 2GM/c²
    - Surface gravity: κ = c⁴/(4GM)
    - Hawking temperature: T_H = ℏc³/(8πGMk_B)
    - Bekenstein-Hawking entropy: S_BH = (k_B c³/4ℏG) × A = πk_B(2GM/c²)²
    - Evaporation timescale: t_evap = (5120πG²M³)/(ℏc⁴)
    
    SCRIPT: Initialize with mass M, compute all thermodynamic quantities,
    store in structured format for analysis and visualization.
    """
    
    def __init__(self, mass_kg):
        """
        Initialize black hole with given mass.
        
        Parameters:
        -----------
        mass_kg : float
            Black hole mass in kilograms
        """
        self.M = mass_kg
        self.compute_properties()
    
    def compute_properties(self):
        """Compute all thermodynamic properties."""
        # Schwarzschild radius (m)
        self.r_s = 2 * G * self.M / C**2
        
        # Surface gravity (m/s²)
        self.kappa = C**4 / (4 * G * self.M)
        
        # Hawking temperature (K)
        self.T_H = (HBAR * C**3) / (8 * PI * G * self.M * K_B)
        
        # Bekenstein-Hawking entropy (dimensionless, in units of k_B)
        # S = k_B × (A c³)/(4 ℏ G) = k_B × π(2GM/c²)²/(ℏG/c³)
        self.S_BH = (PI * K_B * (2 * G * self.M / C**2)**2) / (HBAR * G / C**3)
        
        # Evaporation timescale (seconds)
        self.t_evap = (5120 * PI * G**2 * self.M**3) / (HBAR * C**4)
        
        # Luminosity (Watts) - Stefan-Boltzmann for black body
        # L = σ A T⁴, but for BH: L ≈ ℏc⁶/(15360πG²M²)
        self.L = (HBAR * C**6) / (15360 * PI * G**2 * self.M**2)
        
        # Event horizon area (m²)
        self.A = 4 * PI * self.r_s**2
        
    def to_dict(self):
        """Return properties as dictionary."""
        return {
            'M_kg': self.M,
            'M_solar': self.M / M_SOLAR,
            'r_s_m': self.r_s,
            'r_s_km': self.r_s / 1000,
            'kappa_ms2': self.kappa,
            'T_H_K': self.T_H,
            'S_BH_kB': self.S_BH / K_B,  # In units of k_B
            't_evap_s': self.t_evap,
            't_evap_yr': self.t_evap / (365.25 * 24 * 3600),
            'L_W': self.L,
            'A_m2': self.A
        }

def generate_mass_range(M_min=1e10, M_max=1e30, n_points=100):
    """
    Generate logarithmically spaced mass range.
    
    Parameters:
    -----------
    M_min : float
        Minimum mass (kg)
    M_max : float
        Maximum mass (kg)
    n_points : int
        Number of sample points
        
    Returns:
    --------
    masses : ndarray
        Array of masses in kg
    """
    return np.logspace(np.log10(M_min), np.log10(M_max), n_points)

def compute_classical_dataset(masses):
    """
    Compute classical Hawking properties for array of masses.
    
    Parameters:
    -----------
    masses : ndarray
        Array of black hole masses (kg)
        
    Returns:
    --------
    df : DataFrame
        Complete dataset of BH properties
    """
    data = []
    for M in masses:
        bh = SchwarzschildBlackHole(M)
        data.append(bh.to_dict())
    
    return pd.DataFrame(data)

def plot_classical_properties(df):
    """
    Generate comprehensive visualization of classical BH properties.
    
    Parameters:
    -----------
    df : DataFrame
        Classical BH dataset
    """
    fig, axes = plt.subplots(2, 3, figsize=(18, 12))
    fig.suptitle('Classical Schwarzschild Black Hole Thermodynamics', 
                 fontsize=16, fontweight='bold')
    
    # Plot 1: Hawking Temperature vs Mass
    ax = axes[0, 0]
    ax.loglog(df['M_kg'], df['T_H_K'], 'b-', linewidth=2, label='$T_H = \\frac{\\hbar c^3}{8\\pi G M k_B}$')
    ax.set_xlabel('Mass M (kg)', fontsize=12)
    ax.set_ylabel('Hawking Temperature $T_H$ (K)', fontsize=12)
    ax.set_title('Temperature Scaling: $T_H \\propto M^{-1}$', fontsize=13)
    ax.grid(True, alpha=0.3)
    ax.legend(fontsize=10)
    
    # Add reference points
    M_solar_idx = np.argmin(np.abs(df['M_solar'] - 1.0))
    ax.plot(df['M_kg'].iloc[M_solar_idx], df['T_H_K'].iloc[M_solar_idx], 
            'ro', markersize=10, label=f'Solar mass: {df["T_H_K"].iloc[M_solar_idx]:.2e} K')
    ax.legend(fontsize=9)
    
    # Plot 2: Surface Gravity vs Mass
    ax = axes[0, 1]
    ax.loglog(df['M_kg'], df['kappa_ms2'], 'g-', linewidth=2, label='$\\kappa = \\frac{c^4}{4GM}$')
    ax.set_xlabel('Mass M (kg)', fontsize=12)
    ax.set_ylabel('Surface Gravity $\\kappa$ (m/s²)', fontsize=12)
    ax.set_title('Surface Gravity Scaling: $\\kappa \\propto M^{-1}$', fontsize=13)
    ax.grid(True, alpha=0.3)
    ax.legend(fontsize=10)
    
    # Plot 3: Entropy vs Mass
    ax = axes[0, 2]
    ax.loglog(df['M_kg'], df['S_BH_kB'], 'r-', linewidth=2, label='$S_{BH} \\propto M^2$')
    ax.set_xlabel('Mass M (kg)', fontsize=12)
    ax.set_ylabel('Entropy $S_{BH}$ (units of $k_B$)', fontsize=12)
    ax.set_title('Entropy Scaling: $S_{BH} \\propto M^2$', fontsize=13)
    ax.grid(True, alpha=0.3)
    ax.legend(fontsize=10)
    
    # Plot 4: Schwarzschild Radius vs Mass
    ax = axes[1, 0]
    ax.loglog(df['M_kg'], df['r_s_km'], 'm-', linewidth=2, label='$r_s = \\frac{2GM}{c^2}$')
    ax.set_xlabel('Mass M (kg)', fontsize=12)
    ax.set_ylabel('Schwarzschild Radius $r_s$ (km)', fontsize=12)
    ax.set_title('Horizon Radius Scaling: $r_s \\propto M$', fontsize=13)
    ax.grid(True, alpha=0.3)
    ax.legend(fontsize=10)
    
    # Plot 5: Evaporation Time vs Mass
    ax = axes[1, 1]
    ax.loglog(df['M_kg'], df['t_evap_yr'], 'c-', linewidth=2, label='$t_{evap} \\propto M^3$')
    ax.set_xlabel('Mass M (kg)', fontsize=12)
    ax.set_ylabel('Evaporation Time $t_{evap}$ (years)', fontsize=12)
    ax.set_title('Evaporation Timescale: $t_{evap} \\propto M^3$', fontsize=13)
    ax.grid(True, alpha=0.3)
    ax.legend(fontsize=10)
    
    # Plot 6: Luminosity vs Mass
    ax = axes[1, 2]
    ax.loglog(df['M_kg'], df['L_W'], 'orange', linewidth=2, label='$L \\propto M^{-2}$')
    ax.set_xlabel('Mass M (kg)', fontsize=12)
    ax.set_ylabel('Luminosity L (W)', fontsize=12)
    ax.set_title('Hawking Luminosity: $L \\propto M^{-2}$', fontsize=13)
    ax.grid(True, alpha=0.3)
    ax.legend(fontsize=10)
    
    plt.tight_layout()
    plt.savefig(f'{FIG_DIR}/01_classical_hawking_properties.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"✓ Saved: {FIG_DIR}/01_classical_hawking_properties.png")

def verify_scaling_laws(df):
    """
    Verify power-law scaling relationships.
    
    Parameters:
    -----------
    df : DataFrame
        Classical BH dataset
        
    Returns:
    --------
    scaling_results : dict
        Fitted exponents and R² values
    """
    from scipy.stats import linregress
    
    log_M = np.log10(df['M_kg'])
    
    # T_H ∝ M^(-1)
    log_T = np.log10(df['T_H_K'])
    slope_T, intercept_T, r_T, p_T, se_T = linregress(log_M, log_T)
    
    # κ ∝ M^(-1)
    log_kappa = np.log10(df['kappa_ms2'])
    slope_kappa, intercept_kappa, r_kappa, p_kappa, se_kappa = linregress(log_M, log_kappa)
    
    # S ∝ M^2
    log_S = np.log10(df['S_BH_kB'])
    slope_S, intercept_S, r_S, p_S, se_S = linregress(log_M, log_S)
    
    # r_s ∝ M^1
    log_rs = np.log10(df['r_s_m'])
    slope_rs, intercept_rs, r_rs, p_rs, se_rs = linregress(log_M, log_rs)
    
    # t_evap ∝ M^3
    log_tevap = np.log10(df['t_evap_s'])
    slope_tevap, intercept_tevap, r_tevap, p_tevap, se_tevap = linregress(log_M, log_tevap)
    
    results = {
        'T_H': {'expected': -1.0, 'fitted': slope_T, 'R2': r_T**2, 'error': abs(slope_T + 1.0)},
        'kappa': {'expected': -1.0, 'fitted': slope_kappa, 'R2': r_kappa**2, 'error': abs(slope_kappa + 1.0)},
        'S_BH': {'expected': 2.0, 'fitted': slope_S, 'R2': r_S**2, 'error': abs(slope_S - 2.0)},
        'r_s': {'expected': 1.0, 'fitted': slope_rs, 'R2': r_rs**2, 'error': abs(slope_rs - 1.0)},
        't_evap': {'expected': 3.0, 'fitted': slope_tevap, 'R2': r_tevap**2, 'error': abs(slope_tevap - 3.0)}
    }
    
    return results

def print_scaling_verification(results):
    """Print scaling law verification results."""
    print("\n" + "="*80)
    print("SCALING LAW VERIFICATION")
    print("="*80)
    print(f"{'Quantity':<15} {'Expected':<12} {'Fitted':<12} {'R²':<12} {'Error':<12}")
    print("-"*80)
    
    for qty, res in results.items():
        print(f"{qty:<15} {res['expected']:>11.6f} {res['fitted']:>11.6f} {res['R2']:>11.9f} {res['error']:>11.2e}")
    
    print("="*80)
    
    # Check if all scaling laws are verified
    all_verified = all(res['R2'] > 0.999999 for res in results.values())
    if all_verified:
        print("✓ All scaling laws verified with R² > 0.999999")
    else:
        print("⚠ Some scaling laws show deviations")
    print()

def main():
    """Main execution function."""
    print("\n" + "="*80)
    print("MODULE 1: CLASSICAL HAWKING TEMPERATURE ANALYSIS")
    print("="*80)
    print("Framework: Universal Binary Principle (UBP) v3.2")
    print("Author: Euan R A Craig")
    print("="*80 + "\n")
    
    # Generate mass range
    print("Generating mass range: M ∈ [10¹⁰, 10³⁰] kg, 100 logarithmic points...")
    masses = generate_mass_range(M_min=1e10, M_max=1e30, n_points=100)
    print(f"✓ Generated {len(masses)} mass points")
    print(f"  Range: {masses[0]:.2e} kg to {masses[-1]:.2e} kg")
    print(f"  Solar mass: {M_SOLAR:.3e} kg\n")
    
    # Compute classical dataset
    print("Computing classical Schwarzschild black hole properties...")
    df = compute_classical_dataset(masses)
    print(f"✓ Computed {len(df)} black hole configurations\n")
    
    # Display sample values
    print("Sample values:")
    print("-"*80)
    sample_indices = [0, len(df)//4, len(df)//2, 3*len(df)//4, -1]
    for idx in sample_indices:
        row = df.iloc[idx]
        print(f"M = {row['M_kg']:.2e} kg ({row['M_solar']:.2e} M☉):")
        print(f"  T_H = {row['T_H_K']:.6e} K")
        print(f"  κ = {row['kappa_ms2']:.6e} m/s²")
        print(f"  r_s = {row['r_s_km']:.6e} km")
        print(f"  S_BH = {row['S_BH_kB']:.6e} k_B")
        print(f"  t_evap = {row['t_evap_yr']:.6e} years")
        print()
    
    # Verify scaling laws
    print("Verifying power-law scaling relationships...")
    scaling_results = verify_scaling_laws(df)
    print_scaling_verification(scaling_results)
    
    # Save dataset
    output_file = f'{DATA_DIR}/classical_hawking_dataset.csv'
    df.to_csv(output_file, index=False)
    print(f"✓ Saved dataset: {output_file}\n")
    
    # Generate visualizations
    print("Generating visualizations...")
    plot_classical_properties(df)
    
    # Save scaling results
    scaling_df = pd.DataFrame(scaling_results).T
    scaling_file = f'{DATA_DIR}/classical_scaling_verification.csv'
    scaling_df.to_csv(scaling_file)
    print(f"✓ Saved scaling verification: {scaling_file}\n")
    
    print("="*80)
    print("MODULE 1 COMPLETE")
    print("="*80)
    print(f"Output files:")
    print(f"  - {output_file}")
    print(f"  - {scaling_file}")
    print(f"  - {FIG_DIR}/01_classical_hawking_properties.png")
    print("="*80 + "\n")
    
    return df, scaling_results

if __name__ == "__main__":
    df, scaling_results = main()

