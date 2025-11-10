#!/usr/bin/env python3.11
"""
Phase 2.3: Calculate Rainbow Angles for Orders 1-200
Using Descartes rainbow theory - CORRECTED
"""

import numpy as np
import json
import matplotlib.pyplot as plt
from pathlib import Path
from scipy.optimize import minimize_scalar

def sellmeier_water(wavelength_nm):
    """Calculate refractive index of water"""
    lam_um = wavelength_nm / 1000.0
    lam2 = lam_um ** 2
    
    # Sellmeier coefficients for water
    a1 = 5.684027565e-1
    a2 = 1.726177391e-1
    a3 = 2.086189578e-2
    a4 = 1.130748688e-1
    
    n_squared = 1.0 + (a1 * lam2) / (lam2 - a2) + (a3 * lam2) / (lam2 - a4)
    n = np.sqrt(np.abs(n_squared))  # Abs to handle numerical issues
    
    return n


def rainbow_deviation_angle(incident_angle, n, p):
    """
    Calculate deviation angle for p internal reflections.
    
    D = (incident - refracted) + (incident - refracted) + p*(π - 2*refracted)
    D = 2*incident + (p-2)*π - 2*(p+1)*refracted
    
    For p=1 (primary): D = 2i + π - 4r = π + 2i - 4r
    For p=2 (secondary): D = 2i - 6r
    """
    i = incident_angle
    
    # Snell's law: n1*sin(i) = n2*sin(r)
    # Air to water: sin(i) = n*sin(r)
    sin_r = np.sin(i) / n
    
    if abs(sin_r) > 1.0:
        return np.inf  # Total internal reflection
    
    r = np.arcsin(sin_r)
    
    # Deviation angle
    if p == 1:
        # Primary rainbow
        D = np.pi + 2*i - 4*r
    elif p == 2:
        # Secondary rainbow  
        D = 2*np.pi + 2*i - 6*r
    else:
        # General formula
        D = p*np.pi + 2*i - 2*(p+1)*r
    
    return D


def find_rainbow_angle(n, p):
    """
    Find rainbow angle by minimizing |dD/di|.
    
    Rainbow occurs at extremum of deviation angle.
    """
    # Find extremum of deviation angle
    result = minimize_scalar(
        lambda i: rainbow_deviation_angle(i, n, p),
        bounds=(0, np.pi/2),
        method='bounded'
    )
    
    if not result.success:
        return np.nan
    
    D_rainbow = result.fun
    
    # Convert deviation to observable angle
    # Primary: angle from antisolar point = 180° - D
    # Secondary: angle from antisolar point = D - 180°
    
    if p == 1:
        # Primary: 180° - D
        angle = np.pi - D_rainbow
    elif p == 2:
        # Secondary: D - 180°
        angle = D_rainbow - np.pi
    elif p % 2 == 1:
        # Odd orders: on solar side
        # Angle from sun = D - p*180°
        angle = D_rainbow - p*np.pi
    else:
        # Even orders: on antisolar side
        # Angle from antisolar point = |D - p*180°|
        angle = abs(D_rainbow - p*np.pi)
    
    angle_deg = np.degrees(angle)
    
    return abs(angle_deg)


def main():
    """Main calculation"""
    print("=" * 70)
    print("Phase 2.3: Higher-Order Rainbow Angles (v3 - CORRECTED)")
    print("=" * 70)
    print()
    
    # Wavelengths
    wavelengths = np.arange(400, 701, 10)  # Every 10 nm
    
    # Orders
    max_order = 200
    orders = list(range(1, max_order + 1))
    
    print(f"Wavelengths: {len(wavelengths)} points ({wavelengths[0]}-{wavelengths[-1]} nm)")
    print(f"Orders: {len(orders)} ({orders[0]}-{orders[-1]})")
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
    print("Calculating...")
    for p in orders:
        if p % 25 == 0 or p <= 5:
            print(f"  Order {p}...")
        
        angles_p = []
        valid = False
        
        for wl in wavelengths:
            n = sellmeier_water(wl)
            angle = find_rainbow_angle(n, p)
            
            if not np.isnan(angle) and angle < 360:
                angles_p.append(angle)
                valid = True
            else:
                angles_p.append(None)
        
        results['angles'][str(p)] = angles_p
        
        if valid:
            results['valid_orders'].append(p)
            # Get angle at 583 nm
            idx_583 = np.argmin(np.abs(wavelengths - 583))
            results['reference_583nm'][str(p)] = angles_p[idx_583]
        else:
            results['reference_583nm'][str(p)] = None
    
    print()
    print(f"Valid orders: {len(results['valid_orders'])}/{len(orders)}")
    print()
    
    # Display results
    print("Key Results (λ = 583 nm):")
    print("-" * 70)
    print(f"{'Order':<8} {'Angle':<12} {'Side':<12} {'Visibility'}")
    print("-" * 70)
    
    for p in [1, 2, 3, 4, 5, 10, 20, 50, 100, 150, 200]:
        if p in results['valid_orders']:
            angle = results['reference_583nm'][str(p)]
            if angle is not None:
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
                
                print(f"{p:<8} {angle:>10.3f}°  {side:<12} {vis}")
    
    print("-" * 70)
    print()
    
    # Summary
    if 1 in results['valid_orders'] and 2 in results['valid_orders']:
        a1 = results['reference_583nm']['1']
        a2 = results['reference_583nm']['2']
        print(f"Primary (p=1):   {a1:.6f}°")
        print(f"Secondary (p=2): {a2:.6f}°")
        print(f"Separation:      {a2-a1:.6f}°")
        print()
        
        # Compare to Phase 1 results
        print("Comparison to Phase 1:")
        print(f"  Phase 1 primary: 42.000000°")
        print(f"  Phase 2 primary: {a1:.6f}°")
        print(f"  Difference:      {abs(a1-42.0):.6f}°")
        print()
    
    # Save
    output_file = Path("/home/ubuntu/rainbow_phase2/higher_order_angles_v3.json")
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"Saved: {output_file}")
    print()
    
    # Visualize
    print("Creating plots...")
    create_plots(results)
    
    print("=" * 70)
    print("Phase 2.3 Complete!")
    print("=" * 70)


def create_plots(results):
    """Create visualizations"""
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle('Higher-Order Rainbow Angles (Corrected)', fontsize=16, fontweight='bold')
    
    valid_orders = results['valid_orders'][:50]  # First 50 orders
    angles = [results['reference_583nm'][str(p)] for p in valid_orders if results['reference_583nm'][str(p)] is not None]
    orders_plot = [p for p in valid_orders if results['reference_583nm'][str(p)] is not None]
    
    # Plot 1: Angle vs Order
    ax = axes[0, 0]
    ax.plot(orders_plot, angles, 'b-', linewidth=1.5)
    ax.scatter([1, 2, 3, 4], [angles[0], angles[1], angles[2], angles[3]], 
               c='red', s=100, zorder=5, label='Orders 1-4')
    ax.set_xlabel('Order (p)', fontsize=12)
    ax.set_ylabel('Angle (degrees)', fontsize=12)
    ax.set_title('Rainbow Angle vs Order (λ=583nm)', fontsize=13)
    ax.grid(True, alpha=0.3)
    ax.legend()
    
    # Plot 2: Orders 1-10 zoomed
    ax = axes[0, 1]
    orders_zoom = orders_plot[:10]
    angles_zoom = angles[:10]
    ax.plot(orders_zoom, angles_zoom, 'b-o', linewidth=2, markersize=8)
    ax.scatter([1, 2], [angles_zoom[0], angles_zoom[1]], 
               c='red', s=150, zorder=5, edgecolors='black', linewidths=2)
    for i, p in enumerate([1, 2]):
        ax.annotate(f'p={p}\n{angles_zoom[i]:.1f}°',
                   xy=(p, angles_zoom[i]),
                   xytext=(p+0.5, angles_zoom[i]+5),
                   fontsize=10,
                   bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.7),
                   arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0.2'))
    ax.set_xlabel('Order (p)', fontsize=12)
    ax.set_ylabel('Angle (degrees)', fontsize=12)
    ax.set_title('Orders 1-10 (Zoomed)', fontsize=13)
    ax.grid(True, alpha=0.3)
    
    # Plot 3: Separation between orders
    ax = axes[1, 0]
    if len(angles) > 1:
        seps = [angles[i+1] - angles[i] for i in range(len(angles)-1)]
        ax.plot(orders_plot[1:], seps, 'g-', linewidth=1.5)
        ax.set_xlabel('Order (p)', fontsize=12)
        ax.set_ylabel('Δθ (degrees)', fontsize=12)
        ax.set_title('Angular Separation Between Orders', fontsize=13)
        ax.grid(True, alpha=0.3)
        ax.axhline(y=0, color='k', linestyle='--', alpha=0.3)
    
    # Plot 4: Spectral dispersion
    ax = axes[1, 1]
    wavelengths = np.array(results['wavelengths_nm'])
    
    for p, color, label in [(1, 'blue', 'Primary'), (2, 'green', 'Secondary'),
                             (3, 'orange', 'Tertiary'), (4, 'red', 'Quaternary')]:
        if p in results['valid_orders']:
            angles_p = [a for a in results['angles'][str(p)] if a is not None]
            wls_p = [wavelengths[i] for i, a in enumerate(results['angles'][str(p)]) if a is not None]
            if len(angles_p) > 0:
                ax.plot(wls_p, angles_p, linewidth=2, label=f'{label} (p={p})', color=color, alpha=0.8)
    
    ax.set_xlabel('Wavelength (nm)', fontsize=12)
    ax.set_ylabel('Angle (degrees)', fontsize=12)
    ax.set_title('Spectral Dispersion (Orders 1-4)', fontsize=13)
    ax.legend(fontsize=10)
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    output_path = Path("/home/ubuntu/rainbow_phase2/higher_order_angles_v3.png")
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"Saved: {output_path}")
    plt.close()


if __name__ == "__main__":
    main()
