#!/usr/bin/env python3.11
"""
Phase 2: Complete 200-Order Rainbow Analysis
============================================
Calculate all 200 rainbow orders and analyze geometric patterns
"""

import numpy as np
import json
import matplotlib.pyplot as plt
from pathlib import Path

# Golden ratio
PHI = (1 + np.sqrt(5)) / 2

def refractive_index_water(wavelength_nm):
    """Calculate refractive index using Sellmeier equation"""
    lam_um = wavelength_nm / 1000.0
    
    n_sq = 1.0 + \
           (5.684027565e-1 * lam_um**2) / (lam_um**2 - 5.101829712e-3) + \
           (1.726177391e-1 * lam_um**2) / (lam_um**2 - 1.821153936e-2) + \
           (2.086189578e-2 * lam_um**2) / (lam_um**2 - 2.620722293e-2) + \
           (1.130748688e-1 * lam_um**2) / (lam_um**2 - 1.069792721e1)
    
    return np.sqrt(n_sq)


def rainbow_angle_order_p(wavelength_nm, p):
    """
    Calculate rainbow angle for p internal reflections.
    
    Returns:
        angle_deg: Observable angle (0-360°)
        deviation_deg: Deviation angle D
        valid: Boolean indicating if rainbow exists
    """
    n = refractive_index_water(wavelength_nm)
    
    # Discriminant for optimal incident angle
    discriminant = ((p+1)**2 - n**2) / (p * (p+2))
    
    if discriminant < 0 or discriminant > 1.0:
        return None, None, False
    
    sin_i = np.sqrt(discriminant)
    
    if sin_i > 1.0:
        return None, None, False
    
    i = np.arcsin(sin_i)
    r = np.arcsin(sin_i / n)
    
    # Deviation angle
    D = 2*i - 2*(p+1)*r + p*np.pi
    D_deg = np.degrees(D)
    
    # Observable angle
    if p == 1:
        theta = np.pi - D
    elif p == 2:
        theta = D - np.pi
    else:
        theta = np.abs(D - p*np.pi)
    
    theta_deg = np.degrees(theta) % 360
    
    return theta_deg, D_deg, True


def main():
    """Main analysis"""
    print("=" * 80)
    print("COMPLETE 200-ORDER RAINBOW ANALYSIS")
    print("=" * 80)
    print()
    
    # Parameters
    wavelengths = np.arange(400, 701, 5)  # Every 5 nm
    max_order = 200
    orders = list(range(1, max_order + 1))
    
    print(f"Wavelengths: {len(wavelengths)} points ({wavelengths[0]}-{wavelengths[-1]} nm)")
    print(f"Orders: {len(orders)} (p=1 to p={max_order})")
    print()
    
    # Storage
    results = {
        'wavelengths_nm': wavelengths.tolist(),
        'orders': orders,
        'angles_583nm': [],  # Observable angles at 583 nm
        'deviations_583nm': [],  # Deviation angles at 583 nm
        'valid_orders': [],
        'angles_full': {},  # Full spectral data
    }
    
    # Calculate
    print("Calculating all orders...")
    idx_583 = np.argmin(np.abs(wavelengths - 583))
    
    for p in orders:
        if p % 25 == 0 or p <= 5:
            print(f"  Order {p}...")
        
        # Get angle at 583 nm
        angle, deviation, valid = rainbow_angle_order_p(583, p)
        
        if valid:
            results['angles_583nm'].append(angle)
            results['deviations_583nm'].append(deviation)
            results['valid_orders'].append(p)
            
            # Calculate full spectrum for this order
            angles_spectrum = []
            for wl in wavelengths:
                a, _, v = rainbow_angle_order_p(wl, p)
                angles_spectrum.append(a if v else None)
            results['angles_full'][str(p)] = angles_spectrum
        else:
            results['angles_583nm'].append(None)
            results['deviations_583nm'].append(None)
    
    print()
    print(f"✓ Valid orders: {len(results['valid_orders'])}/{max_order}")
    print()
    
    # === PATTERN ANALYSIS ===
    print("=" * 80)
    print("PATTERN ANALYSIS")
    print("=" * 80)
    print()
    
    valid_orders = results['valid_orders']
    angles = [results['angles_583nm'][p-1] for p in valid_orders]
    
    # Display first 20 orders
    print("First 20 Orders (λ = 583 nm):")
    print("-" * 80)
    print(f"{'p':<5} {'θ (deg)':<12} {'Δθ':<12} {'θ/360':<12} {'Side'}")
    print("-" * 80)
    
    for i, p in enumerate(valid_orders[:20]):
        angle = angles[i]
        delta = angles[i] - angles[i-1] if i > 0 else 0
        cycles = angle / 360.0
        
        if p == 1:
            side = "Antisolar"
        elif p == 2:
            side = "Antisolar"
        elif p == 3:
            side = "Solar"
        elif p == 4:
            side = "Antisolar"
        else:
            side = "Mixed"
        
        print(f"{p:<5} {angle:>10.3f}°  {delta:>10.3f}°  {cycles:>10.3f}  {side}")
    
    print("-" * 80)
    print()
    
    # === GOLDEN RATIO ANALYSIS ===
    print("Golden Ratio (φ) Analysis:")
    print("-" * 80)
    
    if len(angles) >= 2:
        sep_1_2 = angles[1] - angles[0]
        predicted_6phi = 6 * PHI
        
        print(f"φ = {PHI:.9f}")
        print(f"6φ = {predicted_6phi:.9f}°")
        print()
        print(f"θ₁ (primary) = {angles[0]:.6f}°")
        print(f"θ₂ (secondary) = {angles[1]:.6f}°")
        print(f"Δθ (2-1) = {sep_1_2:.6f}°")
        print(f"Error from 6φ: {abs(sep_1_2 - predicted_6phi):.6f}° ({abs(sep_1_2 - predicted_6phi)/predicted_6phi*100:.3f}%)")
        print()
        
        # Test if pattern continues
        print("Testing φ-based pattern for higher orders:")
        print(f"{'p':<5} {'θ_actual':<15} {'θ_predicted':<15} {'Error':<15}")
        print("-" * 60)
        
        for i in range(min(10, len(angles))):
            p = valid_orders[i]
            theta_actual = angles[i]
            
            # Model 1: Linear φ progression
            theta_pred_linear = (angles[0] + i * predicted_6phi) % 360
            error_linear = abs(theta_actual - theta_pred_linear)
            
            print(f"{p:<5} {theta_actual:>13.3f}°  {theta_pred_linear:>13.3f}°  {error_linear:>13.3f}°")
        
        print("-" * 60)
        print()
    
    # === 360° CYCLE ANALYSIS ===
    print("360° Cycle Analysis:")
    print("-" * 80)
    
    # How many complete cycles?
    if len(angles) > 0:
        max_angle = max(angles)
        cycles = max_angle / 360.0
        print(f"Maximum angle: {max_angle:.2f}°")
        print(f"Complete 360° cycles: {int(cycles)}")
        print()
        
        # Analyze angle distribution within 360° cycle
        angles_mod360 = [a % 360 for a in angles]
        
        # Find clustering
        bins = np.linspace(0, 360, 37)  # 10° bins
        hist, _ = np.histogram(angles_mod360, bins=bins)
        
        print("Angle distribution (mod 360°):")
        print(f"  0-90°:    {sum(1 for a in angles_mod360 if 0 <= a < 90)} orders")
        print(f"  90-180°:  {sum(1 for a in angles_mod360 if 90 <= a < 180)} orders")
        print(f"  180-270°: {sum(1 for a in angles_mod360 if 180 <= a < 270)} orders")
        print(f"  270-360°: {sum(1 for a in angles_mod360 if 270 <= a < 360)} orders")
        print()
    
    # === DODECAHEDRAL CONNECTION ===
    print("Dodecahedral Geometry Connection:")
    print("-" * 80)
    
    dihedral_angle = np.degrees(np.arccos(-1/np.sqrt(5)))
    print(f"Dodecahedral dihedral angle: {dihedral_angle:.6f}°")
    print(f"Primary rainbow: {angles[0]:.6f}°")
    print(f"Relationship: {dihedral_angle:.6f}° - 74.565° = {dihedral_angle - 74.565:.6f}°")
    print()
    
    # Check if higher orders relate to dodecahedral angles
    dodec_angles = [dihedral_angle, 108.0, 72.0, 36.0]  # Key dodecahedral angles
    print("Proximity to dodecahedral angles:")
    for i, p in enumerate(valid_orders[:10]):
        angle = angles[i]
        angle_mod = angle % 360
        
        # Find closest dodecahedral angle
        closest = min(dodec_angles, key=lambda x: abs(angle_mod - x))
        diff = abs(angle_mod - closest)
        
        if diff < 5:  # Within 5°
            print(f"  p={p}: {angle_mod:.2f}° ≈ {closest:.0f}° (diff: {diff:.2f}°)")
    print()
    
    # === OFFBIT QUANTIZATION ===
    print("OffBit Quantization Analysis:")
    print("-" * 80)
    
    print(f"Valid orders: {len(valid_orders)}")
    print(f"2^8 = 256")
    print(f"Ratio: {len(valid_orders)}/256 = {len(valid_orders)/256:.4f}")
    print()
    
    # Check if 200 relates to UBP constants
    Y = np.pi / (np.pi**2 + 2)
    Y_inv = np.pi + 2/np.pi
    
    print(f"Y = {Y:.9f}")
    print(f"1/Y = {Y_inv:.9f}")
    print(f"256 × Y = {256 * Y:.2f}")
    print(f"256 × Y × φ = {256 * Y * PHI:.2f}")
    print(f"200 / (256 × Y) = {200 / (256 * Y):.4f}")
    print()
    
    # Save results
    output_file = Path("/home/ubuntu/rainbow_phase2/complete_200_order_results.json")
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"✓ Results saved: {output_file}")
    print()
    
    # Create visualizations
    print("Creating visualizations...")
    create_comprehensive_plots(results)
    
    print("=" * 80)
    print("✓ ANALYSIS COMPLETE!")
    print("=" * 80)


def create_comprehensive_plots(results):
    """Create comprehensive visualization suite"""
    
    fig = plt.figure(figsize=(18, 12))
    gs = fig.add_gridspec(3, 3, hspace=0.35, wspace=0.35)
    
    valid_orders = results['valid_orders']
    angles = [results['angles_583nm'][p-1] for p in valid_orders]
    
    # Plot 1: Angle vs Order (linear)
    ax1 = fig.add_subplot(gs[0, 0])
    ax1.plot(valid_orders, angles, 'b-', linewidth=1.5, alpha=0.7)
    ax1.scatter(valid_orders[:4], angles[:4], c='red', s=100, zorder=5, edgecolors='black', linewidths=2)
    ax1.set_xlabel('Order (p)', fontsize=11, fontweight='bold')
    ax1.set_ylabel('Angle (degrees)', fontsize=11, fontweight='bold')
    ax1.set_title('Rainbow Angle vs Order', fontsize=12, fontweight='bold')
    ax1.grid(True, alpha=0.3)
    
    # Plot 2: Angle mod 360
    ax2 = fig.add_subplot(gs[0, 1])
    angles_mod = [a % 360 for a in angles]
    ax2.scatter(valid_orders, angles_mod, c=valid_orders, cmap='viridis', s=30, alpha=0.7)
    ax2.axhline(y=42, color='red', linestyle='--', linewidth=2, alpha=0.7, label='Primary (42°)')
    ax2.axhline(y=51, color='green', linestyle='--', linewidth=2, alpha=0.7, label='Secondary (51°)')
    ax2.set_xlabel('Order (p)', fontsize=11, fontweight='bold')
    ax2.set_ylabel('Angle mod 360° (degrees)', fontsize=11, fontweight='bold')
    ax2.set_title('Angle Distribution (mod 360°)', fontsize=12, fontweight='bold')
    ax2.legend(fontsize=9)
    ax2.grid(True, alpha=0.3)
    
    # Plot 3: Polar plot (mod 360)
    ax3 = fig.add_subplot(gs[0, 2], projection='polar')
    angles_rad = [np.radians(a % 360) for a in angles]
    ax3.scatter(angles_rad, valid_orders, c=valid_orders, cmap='viridis', s=30, alpha=0.7)
    ax3.set_title('Polar Distribution', fontsize=12, fontweight='bold', pad=20)
    
    # Plot 4: Angular separation
    ax4 = fig.add_subplot(gs[1, 0])
    if len(angles) > 1:
        seps = [angles[i+1] - angles[i] for i in range(len(angles)-1)]
        ax4.plot(valid_orders[1:], seps, 'g-', linewidth=1.5, alpha=0.7)
        ax4.axhline(y=6*PHI, color='red', linestyle=':', linewidth=2, label=f'6φ = {6*PHI:.2f}°')
        ax4.set_xlabel('Order (p)', fontsize=11, fontweight='bold')
        ax4.set_ylabel('Δθ (degrees)', fontsize=11, fontweight='bold')
        ax4.set_title('Angular Separation', fontsize=12, fontweight='bold')
        ax4.legend(fontsize=9)
        ax4.grid(True, alpha=0.3)
    
    # Plot 5: Spectral dispersion (orders 1-4)
    ax5 = fig.add_subplot(gs[1, 1])
    wavelengths = np.array(results['wavelengths_nm'])
    colors = {1: 'blue', 2: 'green', 3: 'orange', 4: 'red'}
    labels = {1: 'Primary', 2: 'Secondary', 3: 'Tertiary', 4: 'Quaternary'}
    
    for p in [1, 2, 3, 4]:
        if str(p) in results['angles_full']:
            angles_p = results['angles_full'][str(p)]
            wls = [wavelengths[i] for i, a in enumerate(angles_p) if a is not None]
            vals = [a for a in angles_p if a is not None]
            if len(vals) > 0:
                ax5.plot(wls, vals, linewidth=2.5, color=colors[p], alpha=0.8, label=f'{labels[p]} (p={p})')
    
    ax5.set_xlabel('Wavelength (nm)', fontsize=11, fontweight='bold')
    ax5.set_ylabel('Angle (degrees)', fontsize=11, fontweight='bold')
    ax5.set_title('Spectral Dispersion', fontsize=12, fontweight='bold')
    ax5.legend(fontsize=9)
    ax5.grid(True, alpha=0.3)
    
    # Plot 6: Histogram (mod 360)
    ax6 = fig.add_subplot(gs[1, 2])
    ax6.hist(angles_mod, bins=36, color='purple', alpha=0.7, edgecolor='black')
    ax6.set_xlabel('Angle mod 360° (degrees)', fontsize=11, fontweight='bold')
    ax6.set_ylabel('Count', fontsize=11, fontweight='bold')
    ax6.set_title('Angle Distribution Histogram', fontsize=12, fontweight='bold')
    ax6.grid(True, alpha=0.3, axis='y')
    
    # Plot 7: Deviation angle
    ax7 = fig.add_subplot(gs[2, 0])
    deviations = [results['deviations_583nm'][p-1] for p in valid_orders]
    ax7.plot(valid_orders, deviations, 'purple', linewidth=1.5, alpha=0.7)
    ax7.set_xlabel('Order (p)', fontsize=11, fontweight='bold')
    ax7.set_ylabel('Deviation Angle D (degrees)', fontsize=11, fontweight='bold')
    ax7.set_title('Deviation Angle vs Order', fontsize=12, fontweight='bold')
    ax7.grid(True, alpha=0.3)
    
    # Plot 8: Intensity model
    ax8 = fig.add_subplot(gs[2, 1])
    R = 0.96
    intensity = [R**(p-1) for p in valid_orders[:100]]
    ax8.semilogy(valid_orders[:100], intensity, 'orange', linewidth=2, alpha=0.7)
    ax8.axhline(y=0.001, color='red', linestyle='--', linewidth=2, label='Detection threshold')
    ax8.set_xlabel('Order (p)', fontsize=11, fontweight='bold')
    ax8.set_ylabel('Relative Intensity (log)', fontsize=11, fontweight='bold')
    ax8.set_title('Intensity Decay: I(p) = 0.96^(p-1)', fontsize=12, fontweight='bold')
    ax8.legend(fontsize=9)
    ax8.grid(True, alpha=0.3, which='both')
    
    # Plot 9: φ-based prediction
    ax9 = fig.add_subplot(gs[2, 2])
    if len(angles) >= 2:
        # Predict using 6φ pattern
        predicted = [(angles[0] + i * 6 * PHI) % 360 for i in range(len(angles))]
        ax9.scatter(predicted[:20], angles_mod[:20], c='blue', s=50, alpha=0.7, label='Actual vs Predicted')
        ax9.plot([0, 360], [0, 360], 'r--', linewidth=2, alpha=0.5, label='Perfect match')
        ax9.set_xlabel('Predicted (6φ model, mod 360°)', fontsize=11, fontweight='bold')
        ax9.set_ylabel('Actual (mod 360°)', fontsize=11, fontweight='bold')
        ax9.set_title('φ-Pattern Validation', fontsize=12, fontweight='bold')
        ax9.legend(fontsize=9)
        ax9.grid(True, alpha=0.3)
        ax9.set_xlim([0, 360])
        ax9.set_ylim([0, 360])
    
    plt.suptitle('Complete 200-Order Rainbow Analysis', fontsize=16, fontweight='bold', y=0.995)
    
    output_path = Path("/home/ubuntu/rainbow_phase2/complete_200_order_analysis.png")
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"✓ Visualization saved: {output_path}")
    plt.close()


if __name__ == "__main__":
    main()
