#!/usr/bin/env python3.11
"""
Phase 2.3: Calculate Rainbow Angles for Orders 1-200
Using correct Descartes formula from Phase 1
"""

import numpy as np
import json
import matplotlib.pyplot as plt
from pathlib import Path

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
    
    Args:
        wavelength_nm: Wavelength in nm
        p: Number of internal reflections (1=primary, 2=secondary, etc.)
    
    Returns:
        Rainbow angle in degrees (from antisolar point for even p, from solar point for odd p>1)
    """
    n = refractive_index_water(wavelength_nm)
    
    # For p internal reflections:
    # Deviation angle: D = 2i - 2(p+1)r + pπ
    # For minimum deviation: sin(i) = sqrt((n²(p+1)² - 1) / (p(p+2)))
    
    # Calculate discriminant
    discriminant = (n**2 * (p+1)**2 - 1) / (p * (p+2))
    
    if discriminant < 0 or discriminant > 1:
        return np.nan
    
    sin_i_opt = np.sqrt(discriminant)
    
    if sin_i_opt > 1.0:
        return np.nan
    
    i_opt = np.arcsin(sin_i_opt)
    
    # Snell's law: sin(r) = sin(i) / n
    sin_r = sin_i_opt / n
    
    if abs(sin_r) > 1.0:
        return np.nan
    
    r_opt = np.arcsin(sin_r)
    
    # Deviation angle
    D_min = 2*i_opt - 2*(p+1)*r_opt + p*np.pi
    
    # Convert to observable angle
    if p == 1:
        # Primary: angle from antisolar point = 180° - D
        theta_rainbow = np.pi - D_min
    elif p == 2:
        # Secondary: angle from antisolar point = D - 180°
        theta_rainbow = D_min - np.pi
    elif p % 2 == 1:
        # Odd p > 1: on solar side, angle from sun
        theta_rainbow = np.pi - D_min
    else:
        # Even p > 2: on antisolar side
        theta_rainbow = D_min - p*np.pi
    
    angle_deg = np.degrees(theta_rainbow)
    
    return abs(angle_deg)


def main():
    """Main calculation"""
    print("=" * 80)
    print("Phase 2.3: Higher-Order Rainbow Angles (FINAL - Correct Formula)")
    print("=" * 80)
    print()
    
    # Wavelengths
    wavelengths = np.arange(400, 701, 1)  # Every 1 nm for accuracy
    
    # Orders
    max_order = 200
    orders = list(range(1, max_order + 1))
    
    print(f"Wavelengths: {len(wavelengths)} points ({wavelengths[0]}-{wavelengths[-1]} nm)")
    print(f"Orders: {len(orders)} (p={orders[0]} to p={orders[-1]})")
    print(f"Total calculations: {len(wavelengths) * len(orders):,}")
    print()
    
    # Results storage
    results = {
        'wavelengths_nm': wavelengths.tolist(),
        'orders': orders,
        'angles': {},
        'reference_583nm': {},
        'valid_orders': [],
    }
    
    # Calculate
    print("Calculating rainbow angles...")
    for p in orders:
        if p % 25 == 0 or p <= 5:
            print(f"  Order p={p}...")
        
        angles_p = []
        valid = False
        
        for wl in wavelengths:
            angle = rainbow_angle_order_p(wl, p)
            
            if not np.isnan(angle):
                angles_p.append(angle)
                valid = True
            else:
                angles_p.append(None)
        
        results['angles'][str(p)] = angles_p
        
        if valid:
            results['valid_orders'].append(p)
            # Get angle at 583 nm (reference from Phase 1)
            idx_583 = np.argmin(np.abs(wavelengths - 583))
            results['reference_583nm'][str(p)] = angles_p[idx_583]
        else:
            results['reference_583nm'][str(p)] = None
    
    print()
    print(f"✓ Valid orders: {len(results['valid_orders'])}/{len(orders)}")
    print()
    
    # Display key results
    print("Key Results (λ = 583 nm):")
    print("-" * 80)
    print(f"{'Order':<8} {'Angle':<15} {'Side':<12} {'Visibility'}")
    print("-" * 80)
    
    for p in [1, 2, 3, 4, 5, 10, 20, 50, 100, 150, 200]:
        if p in results['valid_orders'] and results['reference_583nm'][str(p)] is not None:
            angle = results['reference_583nm'][str(p)]
            
            if p == 1:
                side, vis = "Antisolar", "Always"
            elif p == 2:
                side, vis = "Antisolar", "Common"
            elif p == 3:
                side, vis = "Solar", "Very rare"
            elif p == 4:
                side, vis = "Antisolar", "Extremely rare"
            else:
                side, vis = "Both", "Lab only"
            
            print(f"{p:<8} {angle:>12.6f}°  {side:<12} {vis}")
        else:
            print(f"{p:<8} {'N/A':<15} {'---':<12} {'No rainbow'}")
    
    print("-" * 80)
    print()
    
    # Summary statistics
    if 1 in results['valid_orders'] and 2 in results['valid_orders']:
        a1 = results['reference_583nm']['1']
        a2 = results['reference_583nm']['2']
        
        print("Summary Statistics:")
        print("-" * 80)
        print(f"Primary rainbow (p=1):       {a1:.9f}°")
        print(f"Secondary rainbow (p=2):     {a2:.9f}°")
        print(f"Separation (Δθ = θ₂ - θ₁):   {a2-a1:.9f}°")
        print()
        
        # Compare to Phase 1
        print("Validation Against Phase 1:")
        print(f"  Phase 1 primary:   42.000000000°")
        print(f"  Phase 2 primary:   {a1:.9f}°")
        print(f"  Difference:        {abs(a1-42.0):.9f}°")
        print(f"  Error:             {abs(a1-42.0)/42.0*100:.6f}%")
        print()
        
        # Golden ratio analysis
        phi = (1 + np.sqrt(5)) / 2
        sep_predicted = 6 * phi  # From Phase 1: θ₂ = θ₁ + 6φ
        sep_actual = a2 - a1
        
        print("Golden Ratio Analysis:")
        print(f"  φ (golden ratio):  {phi:.9f}")
        print(f"  6φ:                {sep_predicted:.9f}°")
        print(f"  Actual separation: {sep_actual:.9f}°")
        print(f"  Difference:        {abs(sep_actual - sep_predicted):.9f}°")
        print(f"  Error:             {abs(sep_actual - sep_predicted)/sep_predicted*100:.6f}%")
        print()
    
    if 3 in results['valid_orders'] and 4 in results['valid_orders']:
        a3 = results['reference_583nm']['3']
        a4 = results['reference_583nm']['4']
        
        if a3 is not None and a4 is not None:
            print("Higher Orders:")
            print(f"  Tertiary (p=3):    {a3:.6f}°")
            print(f"  Quaternary (p=4):  {a4:.6f}°")
            print(f"  Separation (4-3):  {a4-a3:.6f}°")
            print()
    
    # Spectral range for each order
    print("Spectral Dispersion (Angular Spread):")
    print("-" * 80)
    for p in [1, 2, 3, 4]:
        if p in results['valid_orders']:
            angles_p = [a for a in results['angles'][str(p)] if a is not None]
            if len(angles_p) > 0:
                angle_min = min(angles_p)
                angle_max = max(angles_p)
                spread = angle_max - angle_min
                print(f"  Order {p}: {spread:.3f}° (from {angle_min:.2f}° to {angle_max:.2f}°)")
    print()
    
    # Save results
    output_file = Path("/home/ubuntu/rainbow_phase2/rainbow_orders_final.json")
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"✓ Results saved: {output_file}")
    print()
    
    # Create visualizations
    print("Creating visualizations...")
    create_plots(results)
    
    print("=" * 80)
    print("✓ Phase 2.3 Complete!")
    print("=" * 80)


def create_plots(results):
    """Create comprehensive visualizations"""
    fig = plt.figure(figsize=(16, 12))
    gs = fig.add_gridspec(3, 2, hspace=0.3, wspace=0.3)
    
    valid_orders = results['valid_orders']
    wavelengths = np.array(results['wavelengths_nm'])
    
    # Prepare data
    orders_plot = [p for p in valid_orders if results['reference_583nm'][str(p)] is not None]
    angles_583 = [results['reference_583nm'][str(p)] for p in orders_plot]
    
    # Plot 1: Angle vs Order (all valid orders)
    ax1 = fig.add_subplot(gs[0, 0])
    ax1.plot(orders_plot, angles_583, 'b-', linewidth=1.5, alpha=0.8)
    if len(orders_plot) >= 4:
        ax1.scatter([1, 2, 3, 4], angles_583[:4], 
                   c='red', s=120, zorder=5, edgecolors='black', linewidths=2,
                   label='Orders 1-4 (observable)')
    ax1.set_xlabel('Order (p = internal reflections)', fontsize=12, fontweight='bold')
    ax1.set_ylabel('Rainbow Angle (degrees)', fontsize=12, fontweight='bold')
    ax1.set_title('Rainbow Angle vs Order (λ=583nm)', fontsize=14, fontweight='bold')
    ax1.grid(True, alpha=0.3)
    ax1.legend(fontsize=10)
    
    # Plot 2: Orders 1-10 (zoomed)
    ax2 = fig.add_subplot(gs[0, 1])
    orders_zoom = [p for p in orders_plot if p <= 10]
    angles_zoom = [a for p, a in zip(orders_plot, angles_583) if p <= 10]
    
    if len(orders_zoom) > 0:
        ax2.plot(orders_zoom, angles_zoom, 'b-o', linewidth=2.5, markersize=10, alpha=0.7)
        if len(orders_zoom) >= 2:
            ax2.scatter([1, 2], [angles_zoom[0], angles_zoom[1]], 
                       c='red', s=200, zorder=5, edgecolors='black', linewidths=2.5)
            
            # Annotate primary and secondary
            ax2.annotate(f'Primary\np=1\n{angles_zoom[0]:.2f}°',
                       xy=(1, angles_zoom[0]),
                       xytext=(1.5, angles_zoom[0]-8),
                       fontsize=11,
                       fontweight='bold',
                       bbox=dict(boxstyle='round,pad=0.5', facecolor='yellow', alpha=0.8),
                       arrowprops=dict(arrowstyle='->', lw=2, connectionstyle='arc3,rad=0.2'))
            
            ax2.annotate(f'Secondary\np=2\n{angles_zoom[1]:.2f}°',
                       xy=(2, angles_zoom[1]),
                       xytext=(2.5, angles_zoom[1]+8),
                       fontsize=11,
                       fontweight='bold',
                       bbox=dict(boxstyle='round,pad=0.5', facecolor='lightgreen', alpha=0.8),
                       arrowprops=dict(arrowstyle='->', lw=2, connectionstyle='arc3,rad=-0.2'))
    
    ax2.set_xlabel('Order (p)', fontsize=12, fontweight='bold')
    ax2.set_ylabel('Rainbow Angle (degrees)', fontsize=12, fontweight='bold')
    ax2.set_title('Orders 1-10 (Zoomed View)', fontsize=14, fontweight='bold')
    ax2.grid(True, alpha=0.3)
    
    # Plot 3: Angular separation between consecutive orders
    ax3 = fig.add_subplot(gs[1, 0])
    if len(angles_583) > 1:
        seps = [angles_583[i+1] - angles_583[i] for i in range(len(angles_583)-1)]
        ax3.plot(orders_plot[1:], seps, 'g-', linewidth=2, alpha=0.7)
        ax3.axhline(y=0, color='k', linestyle='--', alpha=0.5, linewidth=1.5)
        
        # Highlight 6φ
        phi = (1 + np.sqrt(5)) / 2
        ax3.axhline(y=6*phi, color='red', linestyle=':', alpha=0.7, linewidth=2, 
                   label=f'6φ = {6*phi:.3f}°')
        
    ax3.set_xlabel('Order (p)', fontsize=12, fontweight='bold')
    ax3.set_ylabel('Δθ = θₚ - θₚ₋₁ (degrees)', fontsize=12, fontweight='bold')
    ax3.set_title('Angular Separation Between Consecutive Orders', fontsize=14, fontweight='bold')
    ax3.grid(True, alpha=0.3)
    ax3.legend(fontsize=10)
    
    # Plot 4: Spectral dispersion (orders 1-4)
    ax4 = fig.add_subplot(gs[1, 1])
    
    colors_map = {1: 'blue', 2: 'green', 3: 'orange', 4: 'red'}
    labels_map = {1: 'Primary', 2: 'Secondary', 3: 'Tertiary', 4: 'Quaternary'}
    
    for p in [1, 2, 3, 4]:
        if p in results['valid_orders']:
            angles_p = results['angles'][str(p)]
            wls_p = [wavelengths[i] for i, a in enumerate(angles_p) if a is not None]
            angles_p_valid = [a for a in angles_p if a is not None]
            
            if len(angles_p_valid) > 0:
                ax4.plot(wls_p, angles_p_valid, linewidth=3, 
                        label=f'{labels_map[p]} (p={p})', 
                        color=colors_map[p], alpha=0.8)
    
    ax4.set_xlabel('Wavelength (nm)', fontsize=12, fontweight='bold')
    ax4.set_ylabel('Rainbow Angle (degrees)', fontsize=12, fontweight='bold')
    ax4.set_title('Spectral Dispersion (Orders 1-4)', fontsize=14, fontweight='bold')
    ax4.legend(fontsize=11, loc='best')
    ax4.grid(True, alpha=0.3)
    
    # Plot 5: Intensity decay model (conceptual)
    ax5 = fig.add_subplot(gs[2, :])
    
    # Model intensity as I(p) = I₀ × R^(p-1) where R ≈ 0.96 (Fresnel reflectance)
    R = 0.96  # Approximate Fresnel reflectance for water-air interface
    orders_intensity = orders_plot[:50]  # First 50 orders
    intensity = [R**(p-1) for p in orders_intensity]
    
    ax5.semilogy(orders_intensity, intensity, 'purple', linewidth=2.5, alpha=0.7)
    ax5.axhline(y=0.001, color='red', linestyle='--', linewidth=2, alpha=0.7,
               label='Detection threshold (~0.1%)')
    
    # Mark observable orders
    ax5.axvspan(1, 2, alpha=0.2, color='green', label='Commonly observable (1-2)')
    ax5.axvspan(3, 4, alpha=0.2, color='yellow', label='Rarely observable (3-4)')
    ax5.axvspan(5, 200, alpha=0.1, color='red', label='Lab only (5+)')
    
    ax5.set_xlabel('Order (p)', fontsize=12, fontweight='bold')
    ax5.set_ylabel('Relative Intensity (log scale)', fontsize=12, fontweight='bold')
    ax5.set_title('Intensity Decay Model: I(p) = I₀ × 0.96^(p-1)', fontsize=14, fontweight='bold')
    ax5.legend(fontsize=10, loc='upper right')
    ax5.grid(True, alpha=0.3, which='both')
    
    plt.suptitle('Higher-Order Rainbow Analysis (Orders 1-200)', 
                fontsize=18, fontweight='bold', y=0.995)
    
    # Save
    output_path = Path("/home/ubuntu/rainbow_phase2/rainbow_orders_final.png")
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"✓ Visualization saved: {output_path}")
    plt.close()


if __name__ == "__main__":
    main()
