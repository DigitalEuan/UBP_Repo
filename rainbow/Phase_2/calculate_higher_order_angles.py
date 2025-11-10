#!/usr/bin/env python3.11
"""
Phase 2.3: Calculate Rainbow Angles for Orders 1-200
Using geometric optics and Sell

meier dispersion equation
"""

import numpy as np
import json
import matplotlib.pyplot as plt
from pathlib import Path

# Constants
C = 299792458  # Speed of light (m/s)

def sellmeier_water(wavelength_nm):
    """
    Calculate refractive index of water using Sellmeier equation.
    
    Parameters:
    -----------
    wavelength_nm : float or array
        Wavelength in nanometers
    
    Returns:
    --------
    n : float or array
        Refractive index
    
    Reference: Daimon & Masumura (2007)
    """
    lam = wavelength_nm / 1000.0  # Convert to micrometers
    lam2 = lam ** 2
    
    # Sellmeier coefficients for water (visible range)
    A = 0.5684
    B = 0.1726
    C = 0.02062
    D = 0.1138
    
    n_squared = 1 + A * lam2 / (lam2 - B) + C * lam2 / (lam2 - D)
    n = np.sqrt(n_squared)
    
    return n


def calculate_rainbow_angle(n, order):
    """
    Calculate rainbow angle for a given order using geometric optics.
    
    Parameters:
    -----------
    n : float
        Refractive index
    order : int
        Rainbow order (1 = primary, 2 = secondary, etc.)
    
    Returns:
    --------
    angle_deg : float
        Rainbow angle in degrees (from antisolar point for even orders,
        from solar point for odd orders > 1)
    
    Theory:
    -------
    For order k, light undergoes k-1 internal reflections.
    The deviation angle D is minimized at a specific incident angle.
    
    For primary (k=1): θ = 2*arcsin(sin(i)/n) - 4i + π
    For secondary (k=2): θ = 2*arcsin(sin(i)/n) - 6i + 2π
    General: θ = 2(k+1)*arcsin(sin(i)/n) - 2k*i + (k-1)*π
    
    We find the incident angle i that minimizes |dθ/di|.
    """
    k = order
    
    # Find incident angle for minimum deviation
    # Use numerical optimization
    def deviation_angle(i_rad):
        """Calculate deviation angle for given incident angle"""
        if np.sin(i_rad) / n > 1.0 or np.sin(i_rad) / n < -1.0:
            return np.inf
        
        refracted = np.arcsin(np.sin(i_rad) / n)
        D = 2 * (k + 1) * refracted - 2 * k * i_rad + (k - 1) * np.pi
        return D
    
    # Search for minimum deviation
    i_values = np.linspace(0, np.pi/2, 10000)
    D_values = np.array([deviation_angle(i) for i in i_values])
    
    # Find extremum (minimum for odd k, maximum for even k)
    if k % 2 == 1:  # Odd order (primary, tertiary, etc.)
        idx = np.argmin(D_values)
    else:  # Even order (secondary, quaternary, etc.)
        idx = np.argmax(D_values[D_values < np.inf])
    
    D_min = D_values[idx]
    
    # Convert to observable angle
    # For even orders: angle from antisolar point
    # For odd orders > 1: angle from solar point
    if k == 1:
        # Primary: 180° - D
        angle_rad = np.pi - D_min
    elif k % 2 == 0:
        # Even orders: D - 180°
        angle_rad = D_min - np.pi
    else:
        # Odd orders > 1: D - 180°
        angle_rad = D_min - np.pi
    
    angle_deg = np.degrees(angle_rad)
    
    # Ensure angle is positive
    if angle_deg < 0:
        angle_deg = abs(angle_deg)
    
    return angle_deg


def main():
    """Main calculation function"""
    print("=" * 70)
    print("Phase 2.3: Higher-Order Rainbow Angle Calculation")
    print("=" * 70)
    print()
    
    # Define wavelength range
    wavelengths = np.arange(400, 701, 1)  # 400-700 nm, 1 nm steps
    
    # Define orders to calculate
    orders = list(range(1, 201))  # Orders 1-200
    
    print(f"Calculating rainbow angles for:")
    print(f"  - Wavelengths: {wavelengths[0]}-{wavelengths[-1]} nm ({len(wavelengths)} points)")
    print(f"  - Orders: {orders[0]}-{orders[-1]} ({len(orders)} orders)")
    print(f"  - Total calculations: {len(wavelengths) * len(orders):,}")
    print()
    
    # Storage for results
    results = {
        'wavelengths_nm': wavelengths.tolist(),
        'orders': orders,
        'angles': {},  # angles[order][wavelength_idx] = angle_deg
        'reference_wavelength_583nm': {},  # angles at 583 nm for each order
    }
    
    # Calculate for each order
    for order in orders:
        if order % 10 == 0 or order <= 5:
            print(f"Calculating order {order}...")
        
        angles_for_order = []
        
        for wl in wavelengths:
            n = sellmeier_water(wl)
            angle = calculate_rainbow_angle(n, order)
            angles_for_order.append(angle)
        
        results['angles'][str(order)] = angles_for_order
        
        # Store angle at 583 nm (reference wavelength from Phase 1)
        idx_583 = np.argmin(np.abs(wavelengths - 583))
        results['reference_wavelength_583nm'][str(order)] = angles_for_order[idx_583]
    
    print()
    print("Calculation complete!")
    print()
    
    # Display key results
    print("Key Results:")
    print("-" * 70)
    print(f"{'Order':<8} {'Angle @ 583nm':<15} {'Side':<12} {'Visibility'}")
    print("-" * 70)
    
    for order in [1, 2, 3, 4, 5, 10, 20, 50, 100, 200]:
        angle = results['reference_wavelength_583nm'][str(order)]
        
        if order == 1:
            side = "Antisolar"
            vis = "Always"
        elif order == 2:
            side = "Antisolar"
            vis = "Common"
        elif order == 3:
            side = "Solar"
            vis = "Very rare"
        elif order == 4:
            side = "Antisolar"
            vis = "Extremely rare"
        else:
            side = "Both" if order % 2 == 0 else "Both"
            vis = "Lab only"
        
        print(f"{order:<8} {angle:>12.3f}°   {side:<12} {vis}")
    
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
    angle_1 = results['reference_wavelength_583nm']['1']
    angle_2 = results['reference_wavelength_583nm']['2']
    angle_3 = results['reference_wavelength_583nm']['3']
    angle_4 = results['reference_wavelength_583nm']['4']
    
    print(f"Primary rainbow (order 1):   {angle_1:.6f}°")
    print(f"Secondary rainbow (order 2): {angle_2:.6f}°")
    print(f"Separation (2 - 1):          {angle_2 - angle_1:.6f}°")
    print()
    print(f"Tertiary rainbow (order 3):  {angle_3:.6f}°")
    print(f"Quaternary rainbow (order 4): {angle_4:.6f}°")
    print(f"Separation (4 - 3):          {angle_4 - angle_3:.6f}°")
    print()
    
    # Calculate angular range for each order
    for order in [1, 2, 3, 4]:
        angles_order = results['angles'][str(order)]
        angle_min = min(angles_order)
        angle_max = max(angles_order)
        angle_range = angle_max - angle_min
        print(f"Order {order} angular spread: {angle_range:.3f}° ({angle_min:.2f}° to {angle_max:.2f}°)")
    
    print("=" * 70)
    print("Phase 2.3 Complete!")
    print("=" * 70)


def create_visualization(results):
    """Create visualization of rainbow angles vs. order"""
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle('Higher-Order Rainbow Angles (Orders 1-200)', fontsize=16, fontweight='bold')
    
    orders = results['orders']
    angles_583 = [results['reference_wavelength_583nm'][str(o)] for o in orders]
    
    # Plot 1: Angles vs. Order (all 200 orders)
    ax = axes[0, 0]
    ax.plot(orders, angles_583, 'b-', linewidth=1, alpha=0.7)
    ax.scatter([1, 2, 3, 4], [angles_583[0], angles_583[1], angles_583[2], angles_583[3]], 
               c='red', s=100, zorder=5, label='Orders 1-4')
    ax.set_xlabel('Rainbow Order', fontsize=12)
    ax.set_ylabel('Angle (degrees)', fontsize=12)
    ax.set_title('Rainbow Angle vs. Order (λ = 583 nm)', fontsize=13)
    ax.grid(True, alpha=0.3)
    ax.legend()
    
    # Plot 2: Angles vs. Order (orders 1-20, zoomed)
    ax = axes[0, 1]
    orders_zoom = orders[:20]
    angles_zoom = angles_583[:20]
    ax.plot(orders_zoom, angles_zoom, 'b-o', linewidth=2, markersize=6)
    ax.scatter([1, 2, 3, 4], [angles_583[0], angles_583[1], angles_583[2], angles_583[3]], 
               c='red', s=150, zorder=5, edgecolors='black', linewidths=2)
    ax.set_xlabel('Rainbow Order', fontsize=12)
    ax.set_ylabel('Angle (degrees)', fontsize=12)
    ax.set_title('Rainbow Angle vs. Order (Orders 1-20, Zoomed)', fontsize=13)
    ax.grid(True, alpha=0.3)
    
    # Annotate key orders
    for order in [1, 2, 3, 4]:
        ax.annotate(f'Order {order}\n{angles_583[order-1]:.1f}°', 
                   xy=(order, angles_583[order-1]),
                   xytext=(order+1, angles_583[order-1]+5),
                   fontsize=9,
                   bbox=dict(boxstyle='round,pad=0.3', facecolor='yellow', alpha=0.7),
                   arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0.3'))
    
    # Plot 3: Angular separation between consecutive orders
    ax = axes[1, 0]
    separations = [angles_583[i+1] - angles_583[i] for i in range(len(angles_583)-1)]
    ax.plot(orders[1:], separations, 'g-', linewidth=1.5)
    ax.set_xlabel('Rainbow Order', fontsize=12)
    ax.set_ylabel('Angular Separation (degrees)', fontsize=12)
    ax.set_title('Angular Separation Between Consecutive Orders', fontsize=13)
    ax.grid(True, alpha=0.3)
    ax.axhline(y=0, color='k', linestyle='--', alpha=0.3)
    
    # Plot 4: Spectral dispersion for orders 1-4
    ax = axes[1, 1]
    wavelengths = np.array(results['wavelengths_nm'])
    colors_wl = wavelengths
    
    for order in [1, 2, 3, 4]:
        angles = results['angles'][str(order)]
        if order == 1:
            label = f'Primary (order {order})'
            color = 'blue'
        elif order == 2:
            label = f'Secondary (order {order})'
            color = 'green'
        elif order == 3:
            label = f'Tertiary (order {order})'
            color = 'orange'
        else:
            label = f'Quaternary (order {order})'
            color = 'red'
        
        ax.plot(wavelengths, angles, linewidth=2, label=label, color=color, alpha=0.8)
    
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
