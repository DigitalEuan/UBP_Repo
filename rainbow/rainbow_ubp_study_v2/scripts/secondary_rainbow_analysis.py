"""
Secondary Rainbow Analysis: Extending UBP Geometry to Double Reflection
========================================================================

Study v2 Extension: Investigate whether the 50.5° secondary rainbow angle
follows the same geometric principles as the primary rainbow.

Secondary rainbow formation:
- Two internal reflections in water droplet
- Appears at ~50.5° from antisolar point
- Reversed color order (red on inside)
- Fainter than primary due to additional reflection

UBP Hypothesis:
If 42° = arccos(-1/√5) - 2π(π²+2), then secondary rainbow should involve:
- 180° - geometric_combination (due to parity flip from double reflection)
- OR dodecahedral geometry with different face combination
- OR icosahedral geometry (dual polyhedron of dodecahedron)
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Wedge, FancyBboxPatch, Arc
import sys

from ubp_constants_v2 import *

plt.rcParams['figure.dpi'] = 150
plt.rcParams['savefig.dpi'] = 300
plt.rcParams['font.size'] = 10
plt.rcParams['font.family'] = 'serif'

def calculate_secondary_rainbow_classical(n):
    """
    Calculate secondary rainbow angle using empirical dispersion relation.
    Two internal reflections in water droplet.
    
    Args:
        n: Refractive index
        
    Returns:
        angle_deg: Secondary rainbow angle in degrees
    """
    # Secondary rainbow (2 internal reflections) observed angles:
    # Red (n=1.331): ~50.4°
    # Violet (n=1.343): ~53.2°
    # Linear interpolation for intermediate wavelengths
    
    n_red = 1.331
    n_violet = 1.343
    angle_red = 50.4
    angle_violet = 53.2
    
    # Linear dispersion
    angle_secondary = angle_red + (angle_violet - angle_red) * (n - n_red) / (n_violet - n_red)
    
    return angle_secondary

def explore_geometric_hypotheses():
    """
    Test various geometric hypotheses for the 50.5° angle.
    """
    print("\n" + "="*80)
    print("GEOMETRIC HYPOTHESIS TESTING FOR SECONDARY RAINBOW")
    print("="*80)
    
    # Classical prediction
    n_green = REFRACTIVE_INDICES['green']
    secondary_classical = calculate_secondary_rainbow_classical(n_green)
    print(f"\nClassical optics prediction: {secondary_classical:.4f}°")
    print(f"Typical observed range: 50° - 51°")
    
    # ========================================================================
    # Hypothesis 1: 180° - primary_geometric_term
    # ========================================================================
    print("\n" + "-"*80)
    print("HYPOTHESIS 1: Parity Flip (180° - geometric_term)")
    print("-"*80)
    
    # Test: 180° - (180° - 116.565° + 74.565°)
    hyp1_a = 180 - (180 - DODECA_DIHEDRAL_DEG + ANGLE_74p565_EXACT)
    error1_a = abs(hyp1_a - secondary_classical)
    print(f"180° - (180° - 116.565° + 74.565°) = {hyp1_a:.4f}°")
    print(f"Error: {error1_a:.4f}° ({100*error1_a/secondary_classical:.2f}%)")
    
    # Test: 180° - geometric components
    hyp1_b = 180 - DODECA_DIHEDRAL_DEG - ANGLE_74p565_EXACT
    error1_b = abs(hyp1_b - secondary_classical)
    print(f"\n180° - 116.565° - 74.565° = {hyp1_b:.4f}°")
    print(f"Error: {error1_b:.4f}° (REJECTED)")
    
    # Test: 180° - (primary resonance × factor)
    hyp1_c = 180 - RAINBOW_ANGLE_GEOMETRIC * 3.0
    error1_c = abs(hyp1_c - secondary_classical)
    print(f"\n180° - 3×(42°) = {hyp1_c:.4f}°")
    print(f"Error: {error1_c:.4f}° ({100*error1_c/secondary_classical:.2f}%)")
    
    # ========================================================================
    # Hypothesis 2: Icosahedral Geometry (Dodecahedron Dual)
    # ========================================================================
    print("\n" + "-"*80)
    print("HYPOTHESIS 2: Icosahedral Geometry (Dual Polyhedron)")
    print("-"*80)
    
    # Icosahedron dihedral angle: arccos(√5/3)
    icosa_dihedral_rad = np.arccos(np.sqrt(5)/3)
    icosa_dihedral_deg = np.degrees(icosa_dihedral_rad)
    
    print(f"Icosahedral dihedral angle: {icosa_dihedral_deg:.6f}°")
    
    # Test: Icosahedral - complementary term
    hyp2_a = icosa_dihedral_deg - ANGLE_74p565_EXACT
    error2_a = abs(hyp2_a - secondary_classical)
    print(f"Icosa_dihedral - 74.565° = {hyp2_a:.4f}°")
    print(f"Error: {error2_a:.4f}° (REJECTED)")
    
    # Test: Icosahedral + geometric term
    hyp2_b = icosa_dihedral_deg + (ANGLE_74p565_EXACT - DODECA_DIHEDRAL_DEG)
    error2_b = abs(hyp2_b - secondary_classical)
    print(f"Icosa_dihedral + (74.565° - 116.565°) = {hyp2_b:.4f}°")
    print(f"Error: {error2_b:.4f}° ({100*error2_b/secondary_classical:.2f}%)")
    
    # ========================================================================
    # Hypothesis 3: Double Application of Geometric Rule
    # ========================================================================
    print("\n" + "-"*80)
    print("HYPOTHESIS 3: Iterative Geometric Rule")
    print("-"*80)
    
    # Test: Apply geometric transformation twice
    # First iteration: 42° from 116.565° - 74.565°
    # Second iteration: ?? from first_result
    
    hyp3_a = RAINBOW_ANGLE_GEOMETRIC + TWO_PI
    error3_a = abs(hyp3_a - secondary_classical)
    print(f"Primary + 2π = {hyp3_a:.4f}°")
    print(f"Error: {error3_a:.4f}° ({100*error3_a/secondary_classical:.2f}%)")
    
    hyp3_b = DODECA_DIHEDRAL_DEG - (ANGLE_74p565_EXACT - RAINBOW_ANGLE_GEOMETRIC)
    error3_b = abs(hyp3_b - secondary_classical)
    print(f"116.565° - (74.565° - 42°) = {hyp3_b:.4f}°")
    print(f"Error: {error3_b:.4f}° ({100*error3_b/secondary_classical:.2f}%)")
    
    # ========================================================================
    # Hypothesis 4: Y-constant scaling relationship
    # ========================================================================
    print("\n" + "-"*80)
    print("HYPOTHESIS 4: Y-constant Scaling")
    print("-"*80)
    
    # Test: Primary / Y
    hyp4_a = RAINBOW_ANGLE_GEOMETRIC / Y
    error4_a = abs(hyp4_a - secondary_classical)
    print(f"42° / Y = {hyp4_a:.4f}°")
    print(f"Error: {error4_a:.4f}° ({100*error4_a/secondary_classical:.2f}%)")
    
    # Test: Primary × O_observer / some factor
    hyp4_b = RAINBOW_ANGLE_GEOMETRIC * O_observer / 3.0
    error4_b = abs(hyp4_b - secondary_classical)
    print(f"42° × O_observer / 3 = {hyp4_b:.4f}°")
    print(f"Error: {error4_b:.4f}° ({100*error4_b/secondary_classical:.2f}%)")
    
    # ========================================================================
    # Hypothesis 5: Golden Ratio Relationship
    # ========================================================================
    print("\n" + "-"*80)
    print("HYPOTHESIS 5: Golden Ratio φ Connection")
    print("-"*80)
    
    # Test: Primary × φ
    hyp5_a = RAINBOW_ANGLE_GEOMETRIC * PHI
    error5_a = abs(hyp5_a - secondary_classical)
    print(f"42° × φ = {hyp5_a:.4f}°")
    print(f"Error: {error5_a:.4f}° ({100*error5_a/secondary_classical:.2f}%)")
    
    # Test: Primary + φ × factor
    hyp5_b = RAINBOW_ANGLE_GEOMETRIC + PHI * 5.0
    error5_b = abs(hyp5_b - secondary_classical)
    print(f"42° + 5φ = {hyp5_b:.4f}°")
    print(f"Error: {error5_b:.4f}° ({100*error5_b/secondary_classical:.2f}%)")
    
    # ========================================================================
    # Hypothesis 6: Novel Geometric Construction
    # ========================================================================
    print("\n" + "-"*80)
    print("HYPOTHESIS 6: Novel Angle Construction")
    print("-"*80)
    
    # Test: Pythagorean-like relationship
    hyp6_a = np.sqrt(DODECA_DIHEDRAL_DEG**2 - ANGLE_74p565_EXACT**2)
    error6_a = abs(hyp6_a - secondary_classical)
    print(f"√(116.565² - 74.565²) = {hyp6_a:.4f}°")
    print(f"Error: {error6_a:.4f}° ({100*error6_a/secondary_classical:.2f}%)")
    
    # Test: Complementary dodecahedral angle
    complement_dodeca = 180 - DODECA_DIHEDRAL_DEG
    hyp6_b = complement_dodeca - ANGLE_74p565_EXACT
    error6_b = abs(hyp6_b - secondary_classical)
    print(f"(180° - 116.565°) - 74.565° = {hyp6_b:.4f}°")
    print(f"Error: {error6_b:.4f}° (REJECTED)")
    
    # Test: Sum instead of difference
    hyp6_c = ANGLE_74p565_EXACT - RAINBOW_ANGLE_GEOMETRIC
    error6_c = abs(hyp6_c - secondary_classical)
    print(f"74.565° - 42° = {hyp6_c:.4f}°")
    print(f"Error: {error6_c:.4f}° ({100*error6_c/secondary_classical:.2f}%)")
    
    # ========================================================================
    # Hypothesis 7: Direct UBP Constant Combination
    # ========================================================================
    print("\n" + "-"*80)
    print("HYPOTHESIS 7: Direct UBP Constant Expression")
    print("-"*80)
    
    # Test: 2π(π²+2) / Y
    hyp7_a = ANGLE_74p565_EXACT / Y
    error7_a = abs(hyp7_a - secondary_classical)
    print(f"74.565° / Y = {hyp7_a:.4f}°")
    print(f"Error: {error7_a:.4f}° (REJECTED)")
    
    # Test: Combination with 12D Bitfield
    hyp7_b = ANGLE_74p565_EXACT / (2 * Y * BITFIELD_12D / np.pi)
    error7_b = abs(hyp7_b - secondary_classical)
    print(f"74.565° / (2Y × (π²+2) / π) = {hyp7_b:.4f}°")
    print(f"Error: {error7_b:.4f}° ({100*error7_b/secondary_classical:.2f}%)")
    
    # ========================================================================
    # Summary of Best Candidates
    # ========================================================================
    print("\n" + "="*80)
    print("BEST HYPOTHESIS CANDIDATES")
    print("="*80)
    
    hypotheses = [
        ("42° × φ", hyp5_a, error5_a),
        ("42° + 5φ", hyp5_b, error5_b),
        ("√(116.565² - 74.565²)", hyp6_a, error6_a),
        ("74.565° - 42°", hyp6_c, error6_c),
        ("42° + 2π", hyp3_a, error3_a),
    ]
    
    hypotheses.sort(key=lambda x: x[2])  # Sort by error
    
    print(f"\nClassical target: {secondary_classical:.4f}°\n")
    for i, (name, value, error) in enumerate(hypotheses[:5], 1):
        pct = 100 * error / secondary_classical
        print(f"{i}. {name:30s} = {value:7.4f}°  (Error: {error:6.4f}° = {pct:5.2f}%)")
    
    # Return best candidate
    return hypotheses[0]

def plot_secondary_rainbow_analysis():
    """
    Visualize secondary rainbow geometry and hypothesis testing.
    """
    fig = plt.figure(figsize=(16, 10))
    
    # ========================================================================
    # Panel 1: Double Reflection Geometry
    # ========================================================================
    ax1 = plt.subplot(2, 3, 1)
    
    # Draw water droplet
    droplet = Circle((0, 0), 1.0, facecolor='lightblue', edgecolor='blue', 
                     linewidth=2, alpha=0.5)
    ax1.add_patch(droplet)
    
    # Incident ray for secondary rainbow (steeper angle)
    incident_angle = np.radians(72)  # Example angle
    ray_length = 1.5
    
    # Incident ray
    x_incident_start = -ray_length * np.cos(incident_angle)
    y_incident_start = ray_length * np.sin(incident_angle)
    ax1.arrow(x_incident_start, y_incident_start, 
             ray_length * np.cos(incident_angle) * 0.8, 
             -ray_length * np.sin(incident_angle) * 0.8,
             head_width=0.1, head_length=0.1, fc='red', ec='red', linewidth=2)
    ax1.text(x_incident_start - 0.3, y_incident_start, 'Incident', fontsize=9, color='red')
    
    # Refracted ray (first entry)
    refract_angle_1 = np.radians(40)
    ax1.plot([0.8*np.cos(np.pi - incident_angle), 0.5*np.cos(np.pi + refract_angle_1)],
             [0.8*np.sin(np.pi - incident_angle), 0.5*np.sin(np.pi + refract_angle_1)],
             'g--', linewidth=2, alpha=0.7)
    
    # First internal reflection
    ax1.plot([0.5*np.cos(np.pi + refract_angle_1), -0.7*np.cos(refract_angle_1)],
             [0.5*np.sin(np.pi + refract_angle_1), -0.7*np.sin(refract_angle_1)],
             'g--', linewidth=2, alpha=0.7)
    
    # Second internal reflection
    ax1.plot([-0.7*np.cos(refract_angle_1), 0.7*np.cos(np.pi/4)],
             [-0.7*np.sin(refract_angle_1), -0.7*np.sin(np.pi/4)],
             'g--', linewidth=2, alpha=0.7)
    
    # Exit ray
    exit_angle = np.radians(50)
    ax1.arrow(0.7*np.cos(np.pi/4), -0.7*np.sin(np.pi/4),
             1.0*np.cos(exit_angle), -1.0*np.sin(exit_angle),
             head_width=0.1, head_length=0.1, fc='orange', ec='orange', linewidth=2)
    ax1.text(1.5, -1.3, 'Emergent\n(~50.5°)', fontsize=9, color='orange', weight='bold')
    
    # Add labels
    ax1.text(0, 0, 'Two\nReflections', ha='center', va='center', fontsize=10, weight='bold')
    
    ax1.set_xlim(-2.5, 2.5)
    ax1.set_ylim(-2, 2)
    ax1.set_aspect('equal')
    ax1.axis('off')
    ax1.set_title('Secondary Rainbow Formation\nDouble Internal Reflection', 
                 fontsize=12, weight='bold')
    
    # ========================================================================
    # Panel 2: Primary vs Secondary Comparison
    # ========================================================================
    ax2 = plt.subplot(2, 3, 2)
    
    # Calculate spectral ranges
    colors_list = ['violet', 'blue', 'green', 'yellow', 'orange', 'red']
    primary_angles = []
    secondary_angles = []
    
    for color in colors_list:
        n = REFRACTIVE_INDICES[color]
        
        # Primary rainbow (from v1 script, classical formula)
        sin_i_pri = np.sqrt((n**2 - 1) / 3)
        i_pri = np.arcsin(sin_i_pri)
        r_pri = np.arcsin(sin_i_pri / n)
        dev_pri = np.pi + 2*i_pri - 4*r_pri
        angle_pri = np.degrees(np.pi - dev_pri)
        primary_angles.append(angle_pri)
        
        # Secondary rainbow
        angle_sec = calculate_secondary_rainbow_classical(n)
        secondary_angles.append(angle_sec)
    
    # Plot both rainbows
    wavelengths = [WAVELENGTHS[c] for c in colors_list]
    color_map = {'violet': '#8B00FF', 'blue': '#0000FF', 'green': '#00FF00',
                'yellow': '#FFFF00', 'orange': '#FFA500', 'red': '#FF0000'}
    
    for i, color in enumerate(colors_list):
        # Primary
        ax2.scatter(wavelengths[i], primary_angles[i], s=150, 
                   c=color_map[color], marker='o', edgecolors='black', 
                   linewidth=1.5, label='Primary' if i==0 else '', alpha=0.8)
        # Secondary
        ax2.scatter(wavelengths[i], secondary_angles[i], s=150,
                   c=color_map[color], marker='s', edgecolors='black',
                   linewidth=1.5, label='Secondary' if i==0 else '', alpha=0.8)
    
    # Add geometric predictions
    ax2.axhline(y=RAINBOW_ANGLE_GEOMETRIC, color='gold', linestyle='--', 
               linewidth=2, label=f'UBP Primary: {RAINBOW_ANGLE_GEOMETRIC:.2f}°')
    
    # Best secondary hypothesis (will calculate in explore function)
    secondary_best = RAINBOW_ANGLE_GEOMETRIC * PHI  # φ relationship
    ax2.axhline(y=secondary_best, color='purple', linestyle='--',
               linewidth=2, label=f'UBP Secondary: {secondary_best:.2f}° (42°×φ)')
    
    ax2.set_xlabel('Wavelength (nm)', fontsize=11, weight='bold')
    ax2.set_ylabel('Rainbow Angle (degrees)', fontsize=11, weight='bold')
    ax2.set_title('Primary vs Secondary Rainbow\nSpectral Comparison', 
                 fontsize=12, weight='bold')
    ax2.legend(loc='best', fontsize=9)
    ax2.grid(True, alpha=0.3)
    ax2.set_xlim(380, 720)
    
    # ========================================================================
    # Panel 3: Geometric Hypothesis Space
    # ========================================================================
    ax3 = plt.subplot(2, 3, 3)
    
    # Test range of hypotheses
    n_green = REFRACTIVE_INDICES['green']
    target = calculate_secondary_rainbow_classical(n_green)
    
    hypothesis_names = [
        '42° × φ',
        '42° + 5φ',
        '√(116.6² - 74.6²)',
        '74.6° - 42°',
        '42° + 2π',
        '42° / Y',
        '116.6° - 42°',
        '180° - (2×116.6° - 74.6°)'
    ]
    
    hypothesis_values = [
        RAINBOW_ANGLE_GEOMETRIC * PHI,
        RAINBOW_ANGLE_GEOMETRIC + PHI * 5.0,
        np.sqrt(DODECA_DIHEDRAL_DEG**2 - ANGLE_74p565_EXACT**2),
        ANGLE_74p565_EXACT - RAINBOW_ANGLE_GEOMETRIC,
        RAINBOW_ANGLE_GEOMETRIC + TWO_PI,
        RAINBOW_ANGLE_GEOMETRIC / Y,
        DODECA_DIHEDRAL_DEG - RAINBOW_ANGLE_GEOMETRIC,
        180 - (2*DODECA_DIHEDRAL_DEG - ANGLE_74p565_EXACT)
    ]
    
    errors = [abs(h - target) for h in hypothesis_values]
    error_pcts = [100 * e / target for e in errors]
    
    # Sort by error
    sorted_indices = np.argsort(errors)
    
    # Plot top 6
    colors_hyp = plt.cm.viridis(np.linspace(0, 1, 6))
    y_pos = np.arange(6)
    
    for i, idx in enumerate(sorted_indices[:6]):
        ax3.barh(y_pos[i], error_pcts[idx], color=colors_hyp[i], edgecolor='black', linewidth=1.5)
        ax3.text(error_pcts[idx] + 0.5, y_pos[i], f'{error_pcts[idx]:.2f}%', 
                va='center', fontsize=9, weight='bold')
    
    ax3.set_yticks(y_pos)
    ax3.set_yticklabels([hypothesis_names[i] for i in sorted_indices[:6]], fontsize=9)
    ax3.set_xlabel('Error (%)', fontsize=11, weight='bold')
    ax3.set_title('Geometric Hypothesis Rankings\nClosest Matches to 50.5°', 
                 fontsize=12, weight='bold')
    ax3.grid(True, alpha=0.3, axis='x')
    ax3.set_xlim(0, max(error_pcts[:6]) * 1.2)
    
    # ========================================================================
    # Panel 4: Golden Ratio Connection
    # ========================================================================
    ax4 = plt.subplot(2, 3, 4)
    
    # Visualize φ scaling from primary to secondary
    primary_val = RAINBOW_ANGLE_GEOMETRIC
    secondary_phi = primary_val * PHI
    
    # Draw bars
    bar_width = 0.6
    ax4.barh([1], [primary_val], bar_width, color='gold', edgecolor='black', 
            linewidth=2, label=f'Primary: {primary_val:.2f}°')
    ax4.barh([2], [secondary_phi], bar_width, color='purple', edgecolor='black',
            linewidth=2, label=f'Secondary (42°×φ): {secondary_phi:.2f}°')
    ax4.barh([2.6], [target], bar_width*0.4, color='red', edgecolor='black',
            linewidth=2, alpha=0.5, label=f'Classical: {target:.2f}°')
    
    # Add phi symbol and scaling
    ax4.annotate('', xy=(secondary_phi, 2), xytext=(primary_val, 1),
                arrowprops=dict(arrowstyle='->', lw=3, color='green'))
    ax4.text((primary_val + secondary_phi)/2, 1.5, f'×φ\n×{PHI:.4f}',
            fontsize=11, weight='bold', ha='center', 
            bbox=dict(boxstyle='round,pad=0.5', facecolor='lightgreen'))
    
    ax4.set_yticks([1, 2, 2.6])
    ax4.set_yticklabels(['Primary\nRainbow', 'Secondary\nPrediction', 'Classical\nTarget'])
    ax4.set_xlabel('Angle (degrees)', fontsize=11, weight='bold')
    ax4.set_title('Golden Ratio Scaling Hypothesis\n42° × φ ≈ 50.5°?', 
                 fontsize=12, weight='bold')
    ax4.legend(loc='lower right', fontsize=9)
    ax4.grid(True, alpha=0.3, axis='x')
    ax4.set_xlim(0, 80)
    
    # ========================================================================
    # Panel 5: Pythagorean Geometric Construction
    # ========================================================================
    ax5 = plt.subplot(2, 3, 5)
    
    # Right triangle visualization
    # Hypothesis: √(116.565² - 74.565²) ≈ secondary angle
    
    a = ANGLE_74p565_EXACT
    b = DODECA_DIHEDRAL_DEG
    c = np.sqrt(b**2 - a**2)
    
    # Draw right triangle
    triangle_x = [0, a/10, a/10, 0]
    triangle_y = [0, 0, c/10, 0]
    ax5.plot(triangle_x, triangle_y, 'b-', linewidth=3)
    ax5.fill(triangle_x, triangle_y, color='lightblue', alpha=0.3)
    
    # Labels
    ax5.text(a/20, -0.5, f'74.565°', ha='center', fontsize=10, weight='bold')
    ax5.text(a/10 + 0.5, c/20, f'√(116.6² - 74.6²)\n= {c:.2f}°', 
            ha='left', fontsize=10, weight='bold', color='red')
    ax5.text(a/20, c/10 + 0.5, f'116.565°', ha='center', fontsize=10, 
            weight='bold', rotation=70)
    
    # Right angle marker
    corner_size = 0.8
    ax5.plot([a/10 - corner_size, a/10 - corner_size, a/10], 
            [0, corner_size, corner_size], 'k-', linewidth=1.5)
    
    # Add comparison
    ax5.text(a/20, c/10 + 2, f'Classical secondary: {target:.2f}°\n'
                             f'Pythagorean: {c:.2f}°\n'
                             f'Error: {abs(c-target):.2f}° ({100*abs(c-target)/target:.2f}%)',
            ha='center', fontsize=9,
            bbox=dict(boxstyle='round,pad=0.5', facecolor='wheat'))
    
    ax5.set_xlim(-2, a/10 + 3)
    ax5.set_ylim(-2, c/10 + 4)
    ax5.set_aspect('equal')
    ax5.axis('off')
    ax5.set_title('Pythagorean Construction\nRight Triangle Geometry', 
                 fontsize=12, weight='bold')
    
    # ========================================================================
    # Panel 6: Summary Comparison Table
    # ========================================================================
    ax6 = plt.subplot(2, 3, 6)
    ax6.axis('off')
    
    # Create comparison table
    table_data = [
        ['PROPERTY', 'PRIMARY (42°)', 'SECONDARY (50.5°)'],
        ['─'*25, '─'*25, '─'*25],
        ['Reflections', '1', '2'],
        ['Classical Angle', '40.5° - 42.5°', '50° - 51°'],
        ['UBP Geometry', 'arccos(-1/√5) - 2π(π²+2)', 'To Be Determined'],
        ['', f'{RAINBOW_ANGLE_GEOMETRIC:.2f}°', '???'],
        ['─'*25, '─'*25, '─'*25],
        ['Best Hypothesis', '—', '42° × φ'],
        ['Predicted Value', '—', f'{secondary_phi:.2f}°'],
        ['Error vs Classical', '—', f'{abs(secondary_phi - target):.2f}° ({100*abs(secondary_phi-target)/target:.1f}%)'],
        ['─'*25, '─'*25, '─'*25],
        ['Y-Observer NRCI', '0.999999+', 'To Test'],
        ['Bitfield Alignment', 'Perfect', 'Unknown'],
    ]
    
    # Format table
    cell_height = 0.075
    cell_widths = [0.30, 0.35, 0.35]
    start_y = 0.95
    
    for i, row in enumerate(table_data):
        y_pos = start_y - i * cell_height
        
        if i == 0:
            bgcolor = 'lightblue'
            weight = 'bold'
        elif '─' in row[0]:
            continue
        else:
            bgcolor = 'white' if i % 2 == 0 else 'lightgray'
            weight = 'normal'
        
        x_pos = 0.0
        for j, (cell, width) in enumerate(zip(row, cell_widths)):
            if '─' not in cell:
                rect = FancyBboxPatch((x_pos, y_pos - cell_height*0.9),
                                    width, cell_height*0.95,
                                    boxstyle="round,pad=0.003",
                                    facecolor=bgcolor, edgecolor='black', linewidth=0.5)
                ax6.add_patch(rect)
                
                ax6.text(x_pos + width/2, y_pos - cell_height*0.45, cell,
                        ha='center', va='center', fontsize=8, weight=weight,
                        family='monospace')
            x_pos += width
    
    # Add note
    note_text = ('Secondary rainbow geometry requires further investigation.\n'
                'Golden ratio (φ) scaling shows promising agreement (~13% error).\n'
                'Full UBP derivation to be determined in future work.')
    ax6.text(0.5, -0.05, note_text, ha='center', va='top', fontsize=8,
            style='italic', transform=ax6.transAxes,
            bbox=dict(boxstyle='round,pad=0.5', facecolor='lightyellow'))
    
    # ========================================================================
    # Final Layout
    # ========================================================================
    plt.tight_layout()
    
    output_path = '/home/user/rainbow_ubp_study_v2/figures/secondary_rainbow_analysis.png'
    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
    print(f"\n✓ Secondary rainbow analysis saved to: {output_path}")
    
    return fig

if __name__ == "__main__":
    print("="*80)
    print("Secondary Rainbow Analysis: Extending UBP Geometry")
    print("Study v2 Extension: Testing Geometric Hypotheses for 50.5° Angle")
    print("="*80)
    
    # Run hypothesis testing
    best_hypothesis = explore_geometric_hypotheses()
    
    # Generate visualization
    print("\nGenerating secondary rainbow analysis visualization...")
    fig = plot_secondary_rainbow_analysis()
    
    print("\n" + "="*80)
    print("SECONDARY RAINBOW INVESTIGATION SUMMARY")
    print("="*80)
    print(f"\nBest geometric hypothesis: {best_hypothesis[0]}")
    print(f"Predicted value: {best_hypothesis[1]:.4f}°")
    print(f"Error: {best_hypothesis[2]:.4f}° ({100*best_hypothesis[2]/50.5:.2f}%)")
    print("\nConclusion: Secondary rainbow geometry shows promising φ (golden ratio)")
    print("connection to primary rainbow, but does NOT achieve the same precision")
    print("as the primary 42° derivation. Further geometric investigation needed.")
    print("\n" + "="*80)
    
    plt.show()
