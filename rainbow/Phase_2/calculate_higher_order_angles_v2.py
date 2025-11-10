#!/usr/bin/env python3.11
"""
Phase 2.3: Calculate Rainbow Angles for Orders 1-200
Using geometric optics - Corrected formula
"""

import numpy as np
import json
import matplotlib.pyplot as plt
from pathlib import Path

# Constants
C = 299792458  # Speed of light (m/s)

def sellmeier_water(wavelength_nm):
    """
    Calculate refractive index of water using simplified Sellmeier equation.
    
    Parameters:
    -----------
    wavelength_nm : float or array
        Wavelength in nanometers
    
    Returns:
    --------
    n : float or array
        Refractive index
    """
    # Simplified model for visible range
    # n(λ) ≈ 1.32 + A/λ² (empirical fit)
    lam_um = wavelength_nm / 1000.0
    
    # More accurate Sellmeier for water (Daimon & Masumura 2007)
    # Valid for 0.2-1.1 μm
    lam2 = lam_um ** 2
    
    # Coefficients
    a0 = 1.0
    a1 = 5.684027565e-1
    a2 = 1.726177391e-1
    a3 = 2.086189578e-2
    a4 = 1.130748688e-1
    
    n_squared = a0 + (a1 * lam2) / (lam2 - a2) + (a3 * lam2) / (lam2 - a4)
    n = np.sqrt(n_squared)
    
    return n


def calculate_rainbow_angle_order_n(n, p):
    """
    Calculate rainbow angle for order p using Descartes-Snell theory.
    
    Parameters:
    -----------
    n : float
        Refractive index
    p : int
        Number of internal reflections (p=1 for primary, p=2 for secondary)
    
    Returns:
    --------
    angle_deg : float
        Rainbow angle in degrees
    
    Theory:
    -------
    For p internal reflections, the scattering angle θ_s is:
    θ_s = 2*i - 2(p+1)*r + p*π
    
    where i is incident angle, r is refraction angle (Snell: sin(i) = n*sin(r))
    
    Rainbow occurs at dθ_s/di = 0, which gives:
    cos(i_rainbow) = sqrt((n² - 1) / (p*(p+2)))
    
    Observable angle from antisolar point:
    - For odd p: angle = |180° - θ_s|
    - For even p: angle = |θ_s - 180°|
    """
    # Find incident angle for rainbow (minimum deviation)
    # Condition: cos(i) = sqrt((n² - 1) / (p*(p+2)))
    
    discriminant = (n**2 - 1) / (p * (p + 2))
    
    if discriminant < 0 or discriminant > 1:
        # No rainbow for this combination
        return np.nan
    
    cos_i = np.sqrt(discriminant)
    i = np.arccos(cos_i)
    
    # Calculate refraction angle using Snell's law
    sin_r = np.sin(i) / n
    if abs(sin_r) > 1:
        return np.nan
    r = np.arcsin(sin_r)
    
    # Calculate scattering angle
    theta_s = 2*i - 2*(p+1)*r + p*np.pi
    
    # Convert to observable angle
    # Primary (p=1): 180° - θ_s
    # Secondary (p=2): θ_s - 180°
    # General pattern alternates
    
    if p == 1:
        angle = np.pi - theta_s
    elif p == 2:
        angle = theta_s - np.pi
    elif p % 2 == 1:  # Odd p > 1
        angle = np.pi - theta_s
    else:  # Even p > 2
        angle = theta_s - np.pi
    
    angle_deg = np.degrees(angle)
    
    # Ensure positive angle
    angle_deg = abs(angle_deg)
    
    return angle_deg


def main():
    """Main calculation function"""
    print("=" * 70)
    print("Phase 2.3: Higher-Order Rainbow Angle Calculation (v2)")
    print("=" * 70)
    print()
    
    # Define wavelength range
    wavelengths = np.arange(400, 701, 5)  # 400-700 nm, 5 nm steps (faster)
    
    # Define orders to calculate (p = number of internal reflections)
    orders = list(range(1, 201))  # p=1 to p=200
    
    print(f"Calculating rainbow angles for:")
    print(f"  - Wavelengths: {wavelengths[0]}-{wavelengths[-1]} nm ({len(wavelengths)} points)")
    print(f"  - Orders (internal reflections): {orders[0]}-{orders[-1]} ({len(orders)} orders)")
    print(f"  - Total calculations: {len(wavelengths) * len(orders):,}")
    print()
    
    # Storage for results
    results = {
        'wavelengths_nm': wavelengths.tolist(),
        'orders': orders,
        'angles': {},  # angles[order][wavelength_idx] = angle_deg
        'reference_wavelength_583nm': {},  # angles at 583 nm for each order
        'valid_orders': [],  # Orders that produce real rainbows
    }
    
    # Calculate for each order
    valid_count = 0
    for p in orders:
        if p % 20 == 0 or p <= 5:
            print(f"Calculating order p={p} (rainbow {p})...")
        
        angles_for_order = []
        valid_angles = 0
        
        for wl in wavelengths:
            n = sellmeier_water(wl)
            angle = calculate_rainbow_angle_order_n(n, p)
            angles_for_order.append(angle if not np.isnan(angle) else None)
            if not np.isnan(angle):
                valid_angles += 1
        
        results['angles'][str(p)] = angles_for_order
        
        # Check if this order produces valid rainbows
        if valid_angles > 0:
            results['valid_orders'].append(p)
            valid_count += 1
            
            # Store angle at 583 nm (reference wavelength from Phase 1)
            idx_583 = np.argmin(np.abs(wavelengths - 583))
            angle_583 = angles_for_order[idx_583]
            results['reference_wavelength_583nm'][str(p)] = angle_583 if angle_583 is not None else np.nan
        else:
            results['reference_wavelength_583nm'][str(p)] = np.nan
    
    print()
    print(f"Calculation complete! Valid orders: {valid_count}/{len(orders)}")
    print()
    
    # Display key results
    print("Key Results:")
    print("-" * 70)
    print(f"{'Order':<8} {'Angle @ 583nm':<15} {'Side':<12} {'Visibility'}")
    print("-" * 70)
    
    for p in [1, 2, 3, 4, 5, 10, 20, 50, 100, 150, 200]:
        if p in results['valid_orders']:
            angle = results['reference_wavelength_583nm'][str(p)]
            
            if np.isnan(angle):
                print(f"{p:<8} {'N/A':<15} {'---':<12} {'No rainbow'}")
                continue
            
            if p == 1:
                side = "Antisolar"
                vis = "Always"
            elif p == 2:
                side = "Antisolar"
                vis = "Common"
            elif p == 3:
                side = "Solar"
                vis = "Very rare"
            elif p == 4:
                side = "Antisolar"
                vis = "Extremely rare"
            else:
                side = "Both"
                vis = "Lab only"
            
            print(f"{p:<8} {angle:>12.3f}°   {side:<12} {vis}")
        else:
            print(f"{p:<8} {'N/A':<15} {'---':<12} {'No rainbow'}")
    
    print("-" * 70)
    print()
    
    # Save results to JSON
    output_file = Path("/home/ubuntu/rainbow_phase2/higher_order_angles.json")
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"Results saved to: {output_file}")
    print()
    
    # Create visualization
    print("Creating visualization...")
    create_visualization(results)
    print()
    
    # Summary statistics
    print("Summary Statistics:")
    print("-" * 70)
    
    if 1 in results['valid_orders'] and 2 in results['valid_orders']:
        angle_1 = results['reference_wavelength_583nm']['1']
        angle_2 = results['reference_wavelength_583nm']['2']
        
        print(f"Primary rainbow (p=1):       {angle_1:.6f}°")
        print(f"Secondary rainbow (p=2):     {angle_2:.6f}°")
        print(f"Separation (2 - 1):          {angle_2 - angle_1:.6f}°")
        print()
    
    if 3 in results['valid_orders'] and 4 in results['valid_orders']:
        angle_3 = results['reference_wavelength_583nm']['3']
        angle_4 = results['reference_wavelength_583nm']['4']
        
        if not np.isnan(angle_3) and not np.isnan(angle_4):
            print(f"Tertiary rainbow (p=3):      {angle_3:.6f}°")
            print(f"Quaternary rainbow (p=4):    {angle_4:.6f}°")
            print(f"Separation (4 - 3):          {angle_4 - angle_3:.6f}°")
            print()
    
    # Calculate angular range for first few orders
    for p in [1, 2, 3, 4]:
        if p in results['valid_orders']:
            angles_order = [a for a in results['angles'][str(p)] if a is not None]
            if len(angles_order) > 0:
                angle_min = min(angles_order)
                angle_max = max(angles_order)
                angle_range = angle_max - angle_min
                print(f"Order {p} angular spread: {angle_range:.3f}° ({angle_min:.2f}° to {angle_max:.2f}°)")
    
    print()
    print(f"Maximum valid order: {max(results['valid_orders'])}")
    print(f"Total valid orders: {len(results['valid_orders'])}")
    
    print("=" * 70)
    print("Phase 2.3 Complete!")
    print("=" * 70)


def create_visualization(results):
    """Create visualization of rainbow angles vs. order"""
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle('Higher-Order Rainbow Angles', fontsize=16, fontweight='bold')
    
    valid_orders = results['valid_orders']
    angles_583 = [results['reference_wavelength_583nm'][str(o)] for o in valid_orders]
    
    # Remove NaN values
    valid_pairs = [(o, a) for o, a in zip(valid_orders, angles_583) if not np.isnan(a)]
    if len(valid_pairs) == 0:
        print("Warning: No valid angles to plot!")
        return
    
    valid_orders_plot, angles_583_plot = zip(*valid_pairs)
    
    # Plot 1: Angles vs. Order (all valid orders)
    ax = axes[0, 0]
    ax.plot(valid_orders_plot, angles_583_plot, 'b-', linewidth=1, alpha=0.7)
    if len(valid_orders_plot) >= 4:
        ax.scatter([1, 2, 3, 4], [angles_583_plot[0], angles_583_plot[1], 
                                   angles_583_plot[2], angles_583_plot[3]], 
                   c='red', s=100, zorder=5, label='Orders 1-4')
    ax.set_xlabel('Rainbow Order (p)', fontsize=12)
    ax.set_ylabel('Angle (degrees)', fontsize=12)
    ax.set_title('Rainbow Angle vs. Order (λ = 583 nm)', fontsize=13)
    ax.grid(True, alpha=0.3)
    ax.legend()
    
    # Plot 2: Angles vs. Order (orders 1-20, zoomed)
    ax = axes[0, 1]
    orders_zoom = [o for o in valid_orders_plot if o <= 20]
    angles_zoom = [a for o, a in zip(valid_orders_plot, angles_583_plot) if o <= 20]
    
    if len(orders_zoom) > 0:
        ax.plot(orders_zoom, angles_zoom, 'b-o', linewidth=2, markersize=6)
        if len(orders_zoom) >= 4:
            ax.scatter([1, 2, 3, 4], angles_zoom[:4], 
                       c='red', s=150, zorder=5, edgecolors='black', linewidths=2)
            
            # Annotate key orders
            for i, p in enumerate([1, 2, 3, 4]):
                if p <= len(angles_zoom):
                    ax.annotate(f'p={p}\n{angles_zoom[i]:.1f}°', 
                               xy=(p, angles_zoom[i]),
                               xytext=(p+1.5, angles_zoom[i]+3),
                               fontsize=9,
                               bbox=dict(boxstyle='round,pad=0.3', facecolor='yellow', alpha=0.7),
                               arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0.3'))
    
    ax.set_xlabel('Rainbow Order (p)', fontsize=12)
    ax.set_ylabel('Angle (degrees)', fontsize=12)
    ax.set_title('Rainbow Angle vs. Order (Orders 1-20, Zoomed)', fontsize=13)
    ax.grid(True, alpha=0.3)
    
    # Plot 3: Angular separation between consecutive orders
    ax = axes[1, 0]
    if len(angles_583_plot) > 1:
        separations = [angles_583_plot[i+1] - angles_583_plot[i] for i in range(len(angles_583_plot)-1)]
        ax.plot(list(valid_orders_plot)[1:], separations, 'g-', linewidth=1.5)
        ax.set_xlabel('Rainbow Order (p)', fontsize=12)
        ax.set_ylabel('Angular Separation (degrees)', fontsize=12)
        ax.set_title('Angular Separation Between Consecutive Orders', fontsize=13)
        ax.grid(True, alpha=0.3)
        ax.axhline(y=0, color='k', linestyle='--', alpha=0.3)
    
    # Plot 4: Spectral dispersion for orders 1-4
    ax = axes[1, 1]
    wavelengths = np.array(results['wavelengths_nm'])
    
    for p in [1, 2, 3, 4]:
        if p in results['valid_orders']:
            angles = [a for a in results['angles'][str(p)] if a is not None]
            wls = [wavelengths[i] for i, a in enumerate(results['angles'][str(p)]) if a is not None]
            
            if len(angles) > 0:
                if p == 1:
                    label = f'Primary (p={p})'
                    color = 'blue'
                elif p == 2:
                    label = f'Secondary (p={p})'
                    color = 'green'
                elif p == 3:
                    label = f'Tertiary (p={p})'
                    color = 'orange'
                else:
                    label = f'Quaternary (p={p})'
                    color = 'red'
                
                ax.plot(wls, angles, linewidth=2, label=label, color=color, alpha=0.8)
    
    ax.set_xlabel('Wavelength (nm)', fontsize=12)
    ax.set_ylabel('Rainbow Angle (degrees)', fontsize=12)
    ax.set_title('Spectral Dispersion (Orders 1-4)', fontsize=13)
    ax.legend(fontsize=10)
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    # Save figure
    output_path = Path("/home/ubuntu/rainbow_phase2/higher_order_angles_plot.png")
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"Visualization saved to: {output_path}")
    
    plt.close()


if __name__ == "__main__":
    main()
