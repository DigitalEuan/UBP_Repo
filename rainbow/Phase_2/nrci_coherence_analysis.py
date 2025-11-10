#!/usr/bin/env python3.11
"""
Phase 2.5: NRCI Coherence Profile Analysis
==========================================
Calculate NRCI for all 200 rainbow orders to explain the 200-order limit
"""

import sys
sys.path.insert(0, '/home/ubuntu/UBP_Repo/ubp_3.4')

import numpy as np
import json
import matplotlib.pyplot as plt
from pathlib import Path

# Import UBP modules
from y_constants import calculate_y_constant, calculate_y_inverse
from system_constants import UBPConstants

# Constants
PHI = (1 + np.sqrt(5)) / 2
Y = calculate_y_constant()
Y_INV = calculate_y_inverse()

def calculate_fresnel_reflectance(n1, n2, angle_i):
    """
    Calculate Fresnel reflectance for internal reflection.
    
    Args:
        n1: Refractive index of first medium (water)
        n2: Refractive index of second medium (air)
        angle_i: Incident angle (radians)
    
    Returns:
        R: Reflectance (0-1)
    """
    # Snell's law
    sin_t = (n1 / n2) * np.sin(angle_i)
    
    if sin_t > 1.0:
        # Total internal reflection
        return 1.0
    
    angle_t = np.arcsin(sin_t)
    
    # Fresnel equations
    # s-polarization
    Rs = ((n1 * np.cos(angle_i) - n2 * np.cos(angle_t)) / 
          (n1 * np.cos(angle_i) + n2 * np.cos(angle_t)))**2
    
    # p-polarization
    Rp = ((n1 * np.cos(angle_t) - n2 * np.cos(angle_i)) / 
          (n1 * np.cos(angle_t) + n2 * np.cos(angle_i)))**2
    
    # Average for unpolarized light
    R = (Rs + Rp) / 2
    
    return R


def calculate_nrci_order_p(p, n_water=1.333, nrci_initial=0.999997):
    """
    Calculate NRCI for rainbow order p.
    
    Args:
        p: Rainbow order (number of internal reflections)
        n_water: Refractive index of water
        nrci_initial: Initial NRCI of sunlight
    
    Returns:
        nrci: Non-Random Coherence Index
    """
    # Each internal reflection causes:
    # 1. Intensity loss (Fresnel reflectance)
    # 2. Phase decoherence (path length variations)
    # 3. Polarization mixing
    
    # Fresnel reflectance for water-air interface
    # Approximate for grazing angle (~40-50°)
    angle_internal = np.radians(48)  # Typical internal reflection angle
    R = calculate_fresnel_reflectance(n_water, 1.0, angle_internal)
    
    # Intensity decay
    intensity_factor = R ** (p - 1)
    
    # Phase decoherence
    # Each reflection introduces path length variations
    # Model as exponential decay
    coherence_length = 250  # Characteristic coherence length in reflections
    phase_decoherence = np.exp(-p / coherence_length)
    
    # Polarization mixing
    # Each reflection partially mixes polarization states
    polarization_factor = np.exp(-p / 500)  # Slower decay
    
    # Combined NRCI
    nrci = nrci_initial * intensity_factor * phase_decoherence * polarization_factor
    
    return nrci


def main():
    """Main NRCI analysis"""
    print("=" * 80)
    print("NRCI COHERENCE PROFILE ANALYSIS")
    print("=" * 80)
    print()
    
    # Parameters
    max_order = 200
    orders = np.arange(1, max_order + 1)
    
    print(f"Calculating NRCI for orders 1-{max_order}...")
    print()
    
    # Calculate NRCI for each order
    nrci_values = []
    for p in orders:
        nrci = calculate_nrci_order_p(p)
        nrci_values.append(nrci)
    
    nrci_values = np.array(nrci_values)
    
    # Find detection thresholds
    threshold_human = 0.95  # Human eye
    threshold_photo = 0.70  # Photography
    threshold_lab = 0.001   # Laboratory detection
    
    # Find maximum observable orders
    idx_human = np.where(nrci_values < threshold_human)[0]
    idx_photo = np.where(nrci_values < threshold_photo)[0]
    idx_lab = np.where(nrci_values < threshold_lab)[0]
    
    max_human = idx_human[0] if len(idx_human) > 0 else max_order
    max_photo = idx_photo[0] if len(idx_photo) > 0 else max_order
    max_lab = idx_lab[0] if len(idx_lab) > 0 else max_order
    
    # Display results
    print("NRCI Profile Summary:")
    print("-" * 80)
    print(f"{'Order':<10} {'NRCI':<15} {'Intensity':<15} {'Visibility'}")
    print("-" * 80)
    
    for p in [1, 2, 3, 4, 5, 10, 20, 50, 100, 150, 200]:
        nrci = nrci_values[p-1]
        intensity = nrci / nrci_values[0]  # Relative to primary
        
        if nrci >= threshold_human:
            vis = "Human eye"
        elif nrci >= threshold_photo:
            vis = "Photography"
        elif nrci >= threshold_lab:
            vis = "Laboratory"
        else:
            vis = "Undetectable"
        
        print(f"{p:<10} {nrci:>13.9f}  {intensity:>13.6e}  {vis}")
    
    print("-" * 80)
    print()
    
    # Detection limits
    print("Detection Limits:")
    print("-" * 80)
    print(f"Human eye (NRCI > {threshold_human}):     Orders 1-{max_human}")
    print(f"Photography (NRCI > {threshold_photo}):   Orders 1-{max_photo}")
    print(f"Laboratory (NRCI > {threshold_lab}):      Orders 1-{max_lab}")
    print()
    
    # UBP Analysis
    print("UBP Coherence Analysis:")
    print("-" * 80)
    print(f"Initial NRCI (sunlight):  {nrci_values[0]:.9f}")
    print(f"Target NRCI (UBP):        {UBPConstants.PGCI_TARGET:.9f}")
    print(f"Y constant:               {Y:.9f}")
    print(f"1/Y (O_observer):         {Y_INV:.9f}")
    print()
    
    # Find where NRCI crosses UBP target
    idx_ubp = np.where(nrci_values < UBPConstants.PGCI_TARGET)[0]
    max_ubp = idx_ubp[0] if len(idx_ubp) > 0 else max_order
    print(f"NRCI < PGCI_TARGET at order: {max_ubp}")
    print()
    
    # Analyze 200-order limit
    print("200-Order Limit Analysis:")
    print("-" * 80)
    nrci_200 = nrci_values[199]
    print(f"NRCI at order 200:        {nrci_200:.9f}")
    print(f"Relative intensity:       {nrci_200/nrci_values[0]:.6e}")
    print(f"Detection possible:       {'Yes' if nrci_200 > threshold_lab else 'No'}")
    print()
    
    # Theoretical limit
    print("Theoretical Maximum Order:")
    print(f"  Based on NRCI > {threshold_lab}: ~{max_lab} orders")
    print(f"  Observed maximum (Ng et al.):    200 orders")
    print(f"  Agreement:                       {'Excellent' if abs(max_lab - 200) < 50 else 'Moderate'}")
    print()
    
    # OffBit connection
    print("OffBit Quantization:")
    print("-" * 80)
    print(f"  2^8 = 256 states")
    print(f"  Observed: 200 orders")
    print(f"  Ratio: 200/256 = {200/256:.6f}")
    print(f"  256 × Y = {256 * Y:.2f}")
    print(f"  256 × Y × φ = {256 * Y * PHI:.2f}")
    print(f"  256 × Y × φ × 3 = {256 * Y * PHI * 3:.2f}")
    print()
    
    # Save results
    results = {
        'orders': orders.tolist(),
        'nrci_values': nrci_values.tolist(),
        'thresholds': {
            'human': threshold_human,
            'photography': threshold_photo,
            'laboratory': threshold_lab,
            'ubp_target': UBPConstants.PGCI_TARGET
        },
        'max_orders': {
            'human': int(max_human),
            'photography': int(max_photo),
            'laboratory': int(max_lab),
            'ubp': int(max_ubp)
        },
        'ubp_constants': {
            'Y': Y,
            'Y_inverse': Y_INV,
            'phi': PHI
        }
    }
    
    output_file = Path("/home/ubuntu/rainbow_phase2/nrci_coherence_results.json")
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"✓ Results saved: {output_file}")
    print()
    
    # Create visualization
    print("Creating visualization...")
    create_plots(results)
    
    print("=" * 80)
    print("✓ NRCI ANALYSIS COMPLETE!")
    print("=" * 80)


def create_plots(results):
    """Create NRCI visualization"""
    
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle('NRCI Coherence Profile Analysis', fontsize=16, fontweight='bold')
    
    orders = np.array(results['orders'])
    nrci = np.array(results['nrci_values'])
    
    # Plot 1: NRCI vs Order (linear scale)
    ax1 = axes[0, 0]
    ax1.plot(orders, nrci, 'b-', linewidth=2, alpha=0.7)
    ax1.axhline(y=results['thresholds']['human'], color='green', linestyle='--', 
                linewidth=2, label=f"Human eye ({results['thresholds']['human']})")
    ax1.axhline(y=results['thresholds']['photography'], color='orange', linestyle='--', 
                linewidth=2, label=f"Photography ({results['thresholds']['photography']})")
    ax1.axhline(y=results['thresholds']['laboratory'], color='red', linestyle='--', 
                linewidth=2, label=f"Laboratory ({results['thresholds']['laboratory']})")
    ax1.set_xlabel('Order (p)', fontsize=12, fontweight='bold')
    ax1.set_ylabel('NRCI', fontsize=12, fontweight='bold')
    ax1.set_title('NRCI vs Order (Linear Scale)', fontsize=13, fontweight='bold')
    ax1.legend(fontsize=9)
    ax1.grid(True, alpha=0.3)
    ax1.set_ylim([0, 1.0])
    
    # Plot 2: NRCI vs Order (log scale)
    ax2 = axes[0, 1]
    ax2.semilogy(orders, nrci, 'b-', linewidth=2, alpha=0.7)
    ax2.axhline(y=results['thresholds']['laboratory'], color='red', linestyle='--', 
                linewidth=2, label=f"Detection limit ({results['thresholds']['laboratory']})")
    ax2.axvline(x=200, color='purple', linestyle=':', linewidth=2, alpha=0.7,
                label='Observed maximum (200)')
    ax2.set_xlabel('Order (p)', fontsize=12, fontweight='bold')
    ax2.set_ylabel('NRCI (log scale)', fontsize=12, fontweight='bold')
    ax2.set_title('NRCI vs Order (Log Scale)', fontsize=13, fontweight='bold')
    ax2.legend(fontsize=9)
    ax2.grid(True, alpha=0.3, which='both')
    
    # Plot 3: Relative intensity
    ax3 = axes[1, 0]
    intensity_rel = nrci / nrci[0]
    ax3.semilogy(orders, intensity_rel, 'purple', linewidth=2, alpha=0.7)
    ax3.axhline(y=0.001, color='red', linestyle='--', linewidth=2, 
                label='0.1% threshold')
    ax3.axvline(x=200, color='green', linestyle=':', linewidth=2, alpha=0.7,
                label='Order 200')
    ax3.set_xlabel('Order (p)', fontsize=12, fontweight='bold')
    ax3.set_ylabel('Relative Intensity (log scale)', fontsize=12, fontweight='bold')
    ax3.set_title('Intensity Decay', fontsize=13, fontweight='bold')
    ax3.legend(fontsize=9)
    ax3.grid(True, alpha=0.3, which='both')
    
    # Plot 4: Observable regions
    ax4 = axes[1, 1]
    
    # Color regions
    ax4.axvspan(1, results['max_orders']['human'], alpha=0.3, color='green', 
                label=f"Human eye (1-{results['max_orders']['human']})")
    ax4.axvspan(results['max_orders']['human'], results['max_orders']['photography'], 
                alpha=0.3, color='yellow', 
                label=f"Photography ({results['max_orders']['human']}-{results['max_orders']['photography']})")
    ax4.axvspan(results['max_orders']['photography'], results['max_orders']['laboratory'], 
                alpha=0.3, color='orange', 
                label=f"Laboratory ({results['max_orders']['photography']}-{results['max_orders']['laboratory']})")
    
    ax4.plot(orders, nrci, 'b-', linewidth=2, alpha=0.7)
    ax4.set_xlabel('Order (p)', fontsize=12, fontweight='bold')
    ax4.set_ylabel('NRCI', fontsize=12, fontweight='bold')
    ax4.set_title('Observable Regions', fontsize=13, fontweight='bold')
    ax4.legend(fontsize=9, loc='upper right')
    ax4.grid(True, alpha=0.3)
    ax4.set_ylim([0, 1.0])
    
    plt.tight_layout()
    
    output_path = Path("/home/ubuntu/rainbow_phase2/nrci_coherence_profile.png")
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"✓ Visualization saved: {output_path}")
    plt.close()


if __name__ == "__main__":
    main()
