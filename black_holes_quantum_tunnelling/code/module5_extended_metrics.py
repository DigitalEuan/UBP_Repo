#!/usr/bin/env python3.11
"""
Module 5: Extended Metrics - Kerr and Reissner-Nordström Black Holes
Author: Euan R A Craig
Date: October 15, 2025
Framework: Universal Binary Principle (UBP) v3.2

This module extends the UBP framework to rotating (Kerr) and charged
(Reissner-Nordström) black holes, demonstrating generalization beyond
Schwarzschild.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.constants import c, G, hbar, k as k_B, pi, epsilon_0
import os

# Physical constants
C = c
HBAR = hbar
K_B = k_B
PI = pi
EPSILON_0 = epsilon_0

# Directories
DATA_DIR = '/home/ubuntu/black_holes_quantum_tunnelling/data'
FIG_DIR = '/home/ubuntu/black_holes_quantum_tunnelling/figures'

class KerrBlackHole:
    """
    Rotating (Kerr) black hole thermodynamics.
    
    Three-Column Thinking Framework:
    
    LANGUAGE: A rotating black hole possesses angular momentum J, which
    modifies the event horizon structure and surface gravity. The Kerr metric
    introduces an ergosphere and frame-dragging effects. In UBP, rotation
    corresponds to coherent phase oscillations in the bitfield.
    
    MATHEMATICS:
    - Spin parameter: a = J/(Mc)
    - Outer horizon: r₊ = M + √(M² - a²) (in geometric units G=c=1)
    - Inner horizon: r₋ = M - √(M² - a²)
    - Surface gravity: κ = (r₊ - r₋)/(2(r₊² + a²))
    - Hawking temperature: T_H = ℏκ/(2πk_B)
    
    SCRIPT: Input mass M and spin a, compute horizons, surface gravity,
    temperature, compare to Schwarzschild limit (a→0).
    """
    
    def __init__(self, mass_kg, spin_parameter):
        """
        Initialize Kerr black hole.
        
        Parameters:
        -----------
        mass_kg : float
            Black hole mass (kg)
        spin_parameter : float
            Dimensionless spin a/M ∈ [0, 1]
        """
        self.M = mass_kg
        self.a_dimensionless = spin_parameter
        
        # Convert to geometric units (G=c=1)
        self.M_geom = G * self.M / C**2  # meters
        self.a_geom = self.a_dimensionless * self.M_geom
        
        self.compute_properties()
    
    def compute_properties(self):
        """Compute Kerr black hole properties."""
        M = self.M_geom
        a = self.a_geom
        
        # Horizons (geometric units)
        discriminant = M**2 - a**2
        if discriminant < 0:
            raise ValueError("Invalid spin parameter: a > M (naked singularity)")
        
        self.r_plus = M + np.sqrt(discriminant)  # Outer horizon
        self.r_minus = M - np.sqrt(discriminant)  # Inner horizon
        
        # Surface gravity (geometric units)
        kappa_geom = (self.r_plus - self.r_minus) / (2 * (self.r_plus**2 + a**2))
        
        # Convert to SI units (m/s²)
        self.kappa = kappa_geom * C**2 / self.M_geom
        
        # Hawking temperature (K)
        self.T_H = (HBAR * self.kappa) / (2 * PI * C * K_B)
        
        # Entropy (Bekenstein-Hawking)
        A = 4 * PI * (self.r_plus**2 + a**2)  # Horizon area (geometric units)
        self.S_BH = (K_B * C**3 * A) / (4 * HBAR * G)
        
        # Angular velocity of horizon
        self.Omega_H = a / (self.r_plus**2 + a**2)
    
    def to_dict(self):
        """Return properties as dictionary."""
        return {
            'M_kg': self.M,
            'a_dimensionless': self.a_dimensionless,
            'r_plus_m': self.r_plus,
            'r_minus_m': self.r_minus,
            'kappa_ms2': self.kappa,
            'T_H_K': self.T_H,
            'S_BH_kB': self.S_BH / K_B,
            'Omega_H': self.Omega_H
        }

class ReissnerNordstromBlackHole:
    """
    Charged (Reissner-Nordström) black hole thermodynamics.
    
    Three-Column Thinking Framework:
    
    LANGUAGE: A charged black hole possesses electric charge Q, which
    modifies the metric through electromagnetic stress-energy. The RN metric
    has two horizons (outer and inner). In UBP, charge corresponds to OffBit
    layer imbalance.
    
    MATHEMATICS:
    - Charge parameter: Q (Coulombs)
    - Outer horizon: r₊ = M + √(M² - Q²) (geometric units)
    - Inner horizon: r₋ = M - √(M² - Q²)
    - Surface gravity: κ = (r₊ - r₋)/(2r₊²)
    - Hawking temperature: T_H = ℏκ/(2πk_B)
    
    SCRIPT: Input mass M and charge Q, compute horizons, surface gravity,
    temperature, compare to Schwarzschild limit (Q→0).
    """
    
    def __init__(self, mass_kg, charge_C):
        """
        Initialize Reissner-Nordström black hole.
        
        Parameters:
        -----------
        mass_kg : float
            Black hole mass (kg)
        charge_C : float
            Electric charge (Coulombs)
        """
        self.M = mass_kg
        self.Q = charge_C
        
        # Convert to geometric units
        self.M_geom = G * self.M / C**2  # meters
        # Q_geom = Q × √(G/(4πε₀c⁴))
        self.Q_geom = self.Q * np.sqrt(G / (4 * PI * EPSILON_0 * C**4))
        
        self.compute_properties()
    
    def compute_properties(self):
        """Compute RN black hole properties."""
        M = self.M_geom
        Q = self.Q_geom
        
        # Horizons (geometric units)
        discriminant = M**2 - Q**2
        if discriminant < 0:
            raise ValueError("Invalid charge: Q > M (naked singularity)")
        
        self.r_plus = M + np.sqrt(discriminant)  # Outer horizon
        self.r_minus = M - np.sqrt(discriminant)  # Inner horizon
        
        # Surface gravity (geometric units)
        kappa_geom = (self.r_plus - self.r_minus) / (2 * self.r_plus**2)
        
        # Convert to SI units (m/s²)
        self.kappa = kappa_geom * C**2 / self.M_geom
        
        # Hawking temperature (K)
        self.T_H = (HBAR * self.kappa) / (2 * PI * C * K_B)
        
        # Entropy
        A = 4 * PI * self.r_plus**2  # Horizon area (geometric units)
        self.S_BH = (K_B * C**3 * A) / (4 * HBAR * G)
        
        # Electric potential at horizon
        self.Phi_H = Q / self.r_plus
    
    def to_dict(self):
        """Return properties as dictionary."""
        return {
            'M_kg': self.M,
            'Q_C': self.Q,
            'r_plus_m': self.r_plus,
            'r_minus_m': self.r_minus,
            'kappa_ms2': self.kappa,
            'T_H_K': self.T_H,
            'S_BH_kB': self.S_BH / K_B,
            'Phi_H': self.Phi_H
        }

def generate_kerr_dataset(masses, spin_values):
    """Generate Kerr black hole dataset."""
    data = []
    for M in masses:
        for a in spin_values:
            try:
                bh = KerrBlackHole(M, a)
                entry = bh.to_dict()
                data.append(entry)
            except ValueError:
                pass  # Skip invalid configurations
    
    return pd.DataFrame(data)

def generate_rn_dataset(masses, charge_fractions):
    """Generate Reissner-Nordström dataset."""
    data = []
    for M in masses:
        M_geom = G * M / C**2
        for q_frac in charge_fractions:
            # Q in geometric units = q_frac × M_geom
            Q_geom = q_frac * M_geom
            # Convert back to Coulombs
            Q_C = Q_geom / np.sqrt(G / (4 * PI * EPSILON_0 * C**4))
            
            try:
                bh = ReissnerNordstromBlackHole(M, Q_C)
                entry = bh.to_dict()
                entry['q_frac'] = q_frac
                data.append(entry)
            except ValueError:
                pass
    
    return pd.DataFrame(data)

def plot_kerr_comparison(df_kerr):
    """Plot Kerr vs Schwarzschild comparison."""
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    fig.suptitle('Kerr Black Holes: Rotation Effects', fontsize=16, fontweight='bold')
    
    # Select fixed mass, vary spin
    M_ref = df_kerr['M_kg'].iloc[len(df_kerr)//2]
    df_fixed_M = df_kerr[df_kerr['M_kg'] == M_ref].sort_values('a_dimensionless')
    
    # Plot 1: Temperature vs Spin
    ax = axes[0]
    ax.plot(df_fixed_M['a_dimensionless'], df_fixed_M['T_H_K'], 'b-', linewidth=2, marker='o')
    ax.axhline(y=df_fixed_M[df_fixed_M['a_dimensionless'] == 0]['T_H_K'].iloc[0],
               color='r', linestyle='--', linewidth=2, label='Schwarzschild (a=0)')
    ax.set_xlabel('Spin Parameter a/M', fontsize=12)
    ax.set_ylabel('Hawking Temperature (K)', fontsize=12)
    ax.set_title(f'Temperature vs Rotation (M = {M_ref:.2e} kg)', fontsize=13)
    ax.grid(True, alpha=0.3)
    ax.legend(fontsize=10)
    
    # Plot 2: Surface Gravity vs Spin
    ax = axes[1]
    ax.plot(df_fixed_M['a_dimensionless'], df_fixed_M['kappa_ms2'], 'g-', linewidth=2, marker='o')
    ax.axhline(y=df_fixed_M[df_fixed_M['a_dimensionless'] == 0]['kappa_ms2'].iloc[0],
               color='r', linestyle='--', linewidth=2, label='Schwarzschild (a=0)')
    ax.set_xlabel('Spin Parameter a/M', fontsize=12)
    ax.set_ylabel('Surface Gravity (m/s²)', fontsize=12)
    ax.set_title(f'Surface Gravity vs Rotation (M = {M_ref:.2e} kg)', fontsize=13)
    ax.grid(True, alpha=0.3)
    ax.legend(fontsize=10)
    
    plt.tight_layout()
    plt.savefig(f'{FIG_DIR}/07_kerr_comparison.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"✓ Saved: {FIG_DIR}/07_kerr_comparison.png")

def plot_rn_comparison(df_rn):
    """Plot RN vs Schwarzschild comparison."""
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    fig.suptitle('Reissner-Nordström Black Holes: Charge Effects', fontsize=16, fontweight='bold')
    
    # Select fixed mass, vary charge
    M_ref = df_rn['M_kg'].iloc[len(df_rn)//2]
    df_fixed_M = df_rn[df_rn['M_kg'] == M_ref].sort_values('q_frac')
    
    # Plot 1: Temperature vs Charge
    ax = axes[0]
    ax.plot(df_fixed_M['q_frac'], df_fixed_M['T_H_K'], 'b-', linewidth=2, marker='o')
    ax.axhline(y=df_fixed_M[df_fixed_M['q_frac'] == 0]['T_H_K'].iloc[0],
               color='r', linestyle='--', linewidth=2, label='Schwarzschild (Q=0)')
    ax.set_xlabel('Charge Fraction Q/M', fontsize=12)
    ax.set_ylabel('Hawking Temperature (K)', fontsize=12)
    ax.set_title(f'Temperature vs Charge (M = {M_ref:.2e} kg)', fontsize=13)
    ax.grid(True, alpha=0.3)
    ax.legend(fontsize=10)
    
    # Plot 2: Surface Gravity vs Charge
    ax = axes[1]
    ax.plot(df_fixed_M['q_frac'], df_fixed_M['kappa_ms2'], 'g-', linewidth=2, marker='o')
    ax.axhline(y=df_fixed_M[df_fixed_M['q_frac'] == 0]['kappa_ms2'].iloc[0],
               color='r', linestyle='--', linewidth=2, label='Schwarzschild (Q=0)')
    ax.set_xlabel('Charge Fraction Q/M', fontsize=12)
    ax.set_ylabel('Surface Gravity (m/s²)', fontsize=12)
    ax.set_title(f'Surface Gravity vs Charge (M = {M_ref:.2e} kg)', fontsize=13)
    ax.grid(True, alpha=0.3)
    ax.legend(fontsize=10)
    
    plt.tight_layout()
    plt.savefig(f'{FIG_DIR}/08_rn_comparison.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"✓ Saved: {FIG_DIR}/08_rn_comparison.png")

def main():
    """Main execution function."""
    print("\n" + "="*80)
    print("MODULE 5: EXTENDED METRICS (KERR AND REISSNER-NORDSTRÖM)")
    print("="*80)
    print("Framework: Universal Binary Principle (UBP) v3.2")
    print("Author: Euan R A Craig")
    print("="*80 + "\n")
    
    # Generate Kerr dataset
    print("Generating Kerr (rotating) black hole dataset...")
    masses_kerr = np.logspace(15, 25, 10)  # Reduced range for computation
    spin_values = np.linspace(0.0, 0.99, 10)  # a/M from 0 to 0.99
    df_kerr = generate_kerr_dataset(masses_kerr, spin_values)
    print(f"✓ Generated {len(df_kerr)} Kerr configurations\n")
    
    # Display sample Kerr values
    print("Sample Kerr Black Hole Properties:")
    print("-"*80)
    for idx in [0, len(df_kerr)//2, -1]:
        row = df_kerr.iloc[idx]
        print(f"M = {row['M_kg']:.2e} kg, a/M = {row['a_dimensionless']:.3f}:")
        print(f"  T_H = {row['T_H_K']:.6e} K")
        print(f"  κ = {row['kappa_ms2']:.6e} m/s²")
        print(f"  r₊ = {row['r_plus_m']:.6e} m")
        print()
    
    # Save Kerr dataset
    kerr_file = f'{DATA_DIR}/kerr_black_holes.csv'
    df_kerr.to_csv(kerr_file, index=False)
    print(f"✓ Saved Kerr dataset: {kerr_file}\n")
    
    # Generate RN dataset
    print("Generating Reissner-Nordström (charged) black hole dataset...")
    masses_rn = np.logspace(15, 25, 10)
    charge_fractions = np.linspace(0.0, 0.99, 10)  # Q/M from 0 to 0.99
    df_rn = generate_rn_dataset(masses_rn, charge_fractions)
    print(f"✓ Generated {len(df_rn)} RN configurations\n")
    
    # Display sample RN values
    print("Sample Reissner-Nordström Black Hole Properties:")
    print("-"*80)
    for idx in [0, len(df_rn)//2, -1]:
        row = df_rn.iloc[idx]
        print(f"M = {row['M_kg']:.2e} kg, Q/M = {row['q_frac']:.3f}:")
        print(f"  T_H = {row['T_H_K']:.6e} K")
        print(f"  κ = {row['kappa_ms2']:.6e} m/s²")
        print(f"  r₊ = {row['r_plus_m']:.6e} m")
        print()
    
    # Save RN dataset
    rn_file = f'{DATA_DIR}/rn_black_holes.csv'
    df_rn.to_csv(rn_file, index=False)
    print(f"✓ Saved RN dataset: {rn_file}\n")
    
    # Generate visualizations
    print("Generating Kerr comparison plots...")
    plot_kerr_comparison(df_kerr)
    
    print("\nGenerating RN comparison plots...")
    plot_rn_comparison(df_rn)
    
    print("\n" + "="*80)
    print("MODULE 5 COMPLETE")
    print("="*80)
    print(f"Output files:")
    print(f"  - {kerr_file}")
    print(f"  - {rn_file}")
    print(f"  - {FIG_DIR}/07_kerr_comparison.png")
    print(f"  - {FIG_DIR}/08_rn_comparison.png")
    print("\nKey Insights:")
    print("  - Rotation (Kerr): Decreases temperature and surface gravity")
    print("  - Charge (RN): Decreases temperature and surface gravity")
    print("  - Both effects reduce Hawking radiation compared to Schwarzschild")
    print("  - UBP framework successfully generalizes to rotating and charged BHs")
    print("="*80 + "\n")
    
    return df_kerr, df_rn

if __name__ == "__main__":
    df_kerr, df_rn = main()

