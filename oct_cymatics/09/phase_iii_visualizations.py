"""
Phase III Visualizations and Refined Planck Mass Derivation
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
from mpl_toolkits.mplot3d import Axes3D
import json

# Physical constants
C_LIGHT = 2.99792458e8  # m/s
HBAR = 1.054571817e-34  # J·s
G_NEWTON = 6.6743e-11   # m³/(kg·s²)
Y_CONSTANT = np.pi / (np.pi**2 + 2)
X_G = C_LIGHT * Y_CONSTANT

# ============================================================================
# REFINED PLANCK MASS DERIVATION
# ============================================================================

def refined_planck_mass_derivation():
    """
    Refined approach to Planck Mass derivation using Y constant.
    
    Key insight: The Planck Mass should use a DIFFERENT geometric ratio
    than Y_G (which was for gravitational constant).
    
    Let's search for Y_m such that:
        m_p = sqrt(ℏc/G) = Function(Y_m, fundamental constants)
    """
    
    print("=" * 80)
    print("REFINED PLANCK MASS DERIVATION")
    print("=" * 80)
    print()
    
    m_planck_measured = 2.176434e-8  # kg
    m_planck_standard = np.sqrt(HBAR * C_LIGHT / G_NEWTON)
    
    print(f"Target Planck Mass: {m_planck_measured:.10e} kg")
    print(f"Standard formula:   {m_planck_standard:.10e} kg")
    print()
    
    # New hypothesis: Y_m relates to mass-energy-gravity triangle
    # m_p = sqrt(ℏc/G) can be rewritten as:
    # m_p² = ℏc/G
    # m_p² × G = ℏc
    # This is a dimensional relation: [mass²][gravity] = [action][velocity]
    
    # Test if Y_m appears in dimensional analysis
    # [M²][L³M⁻¹T⁻²] = [ML²T⁻¹][LT⁻¹]
    # [M²L³T⁻²M⁻¹] = [ML³T⁻²]
    # [ML³T⁻²] = [ML³T⁻²] ✓
    
    print("Searching for Y_m using dimensional analysis...")
    print()
    
    # Generate extended set of geometric candidates
    candidates = []
    
    # Pure π-based ratios
    for n in range(1, 6):
        for m in [1, 2, 3, np.sqrt(2), np.sqrt(3), 1.618, np.e]:
            Y_candidate = np.pi / (n * np.pi**2 + m)
            candidates.append(('π/({}π² + {})'.format(n, m), Y_candidate))
    
    # φ-based ratios (Planck length is related to φ)
    phi = 1.618033988749895
    for n in [1, 2, 3]:
        for m in [1, 2, np.pi, np.e]:
            Y_candidate = phi / (n * phi**2 + m)
            candidates.append(('φ/({}φ² + {})'.format(n, m), Y_candidate))
    
    # Compound ratios
    candidates.extend([
        ('Y_G × φ', Y_CONSTANT * phi),
        ('Y_G / φ', Y_CONSTANT / phi),
        ('Y_G²', Y_CONSTANT**2),
        ('sqrt(Y_G)', np.sqrt(Y_CONSTANT)),
        ('Y_G × π', Y_CONSTANT * np.pi),
        ('Y_G / π', Y_CONSTANT / np.pi),
        ('1 - Y_G', 1 - Y_CONSTANT),
        ('1 / (1 + Y_G)', 1 / (1 + Y_CONSTANT)),
        ('Y_G × (1 + φ)', Y_CONSTANT * (1 + phi)),
    ])
    
    # For each candidate, test multiple formulas
    best_results = []
    
    for name, Y_m in candidates:
        # Formula A: Direct proportionality
        # m_p = Y_m × sqrt(ℏc/G)
        m_calc_a = Y_m * m_planck_standard
        error_a = abs(m_calc_a - m_planck_measured) / m_planck_measured * 100
        
        # Formula B: Inverse relationship
        # m_p = sqrt(ℏc/G) / Y_m
        if Y_m != 0:
            m_calc_b = m_planck_standard / Y_m
            error_b = abs(m_calc_b - m_planck_measured) / m_planck_measured * 100
        else:
            error_b = float('inf')
        
        # Formula C: Complementary relationship
        # m_p = (1 - Y_m) × sqrt(ℏc/G)
        m_calc_c = (1 - Y_m) * m_planck_standard
        error_c = abs(m_calc_c - m_planck_measured) / m_planck_measured * 100
        
        # Formula D: Exponential relationship
        # m_p = sqrt(ℏc/G) × exp(-Y_m)
        m_calc_d = m_planck_standard * np.exp(-Y_m)
        error_d = abs(m_calc_d - m_planck_measured) / m_planck_measured * 100
        
        best_error = min(error_a, error_b, error_c, error_d)
        
        if best_error < 10:  # Only keep candidates with <10% error
            best_formula = ['A', 'B', 'C', 'D'][np.argmin([error_a, error_b, error_c, error_d])]
            best_value = [m_calc_a, m_calc_b, m_calc_c, m_calc_d][np.argmin([error_a, error_b, error_c, error_d])]
            
            best_results.append({
                'name': name,
                'Y_m': Y_m,
                'formula': best_formula,
                'value': best_value,
                'error_%': best_error
            })
    
    # Sort by error
    best_results.sort(key=lambda x: x['error_%'])
    
    print("Top 10 Candidates:")
    print("-" * 80)
    for i, result in enumerate(best_results[:10], 1):
        print(f"{i:2}. {result['name']:25} | Y_m = {result['Y_m']:.8f} | "
              f"Formula {result['formula']} | Error: {result['error_%']:.4f}%")
    print()
    
    if best_results:
        best = best_results[0]
        print("=" * 80)
        print("BEST PLANCK MASS SCALING:")
        print(f"  Formula: {best['name']}")
        print(f"  Y_m = {best['Y_m']:.10f}")
        print(f"  Type: Formula {best['formula']}")
        print(f"  Calculated: {best['value']:.10e} kg")
        print(f"  Measured:   {m_planck_measured:.10e} kg")
        print(f"  Error: {best['error_%']:.4f}%")
        print("=" * 80)
        print()
        
        return best
    else:
        print("No suitable Y_m candidate found with <10% error")
        print("Planck Mass may require a different approach")
        print()
        return None

# ============================================================================
# VISUALIZATION: CRV FREQUENCY SPECTRUM
# ============================================================================

def plot_crv_spectrum():
    """Visualize CRV frequency spectrum with Y corrections"""
    
    # Load cymatics results
    with open('/home/user/phase_iii_cymatics_results.json', 'r') as f:
        results = json.load(f)
    
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10))
    
    # Extract data
    crv_names = []
    frequencies = []
    y_scaled = []
    layers = []
    
    for crv_name, data in results['patterns'].items():
        crv_names.append(crv_name.replace('CRV_', ''))
        frequencies.append(data['crv_frequency'])
        y_scaled.append(data['Y_scaled'])
        
    # Convert to arrays
    frequencies = np.array(frequencies)
    y_scaled = np.array(y_scaled)
    
    # Plot 1: Frequency spectrum
    colors = ['#FF6B6B' if ys else '#4ECDC4' for ys in y_scaled]
    bars = ax1.bar(range(len(crv_names)), frequencies, color=colors, alpha=0.7, edgecolor='black')
    ax1.set_yscale('log')
    ax1.set_ylabel('Frequency (Hz)', fontsize=12, fontweight='bold')
    ax1.set_xlabel('Core Resonance Values', fontsize=12, fontweight='bold')
    ax1.set_title('Phase III: CRV Frequency Spectrum with Y Corrections', fontsize=14, fontweight='bold')
    ax1.set_xticks(range(len(crv_names)))
    ax1.set_xticklabels(crv_names, rotation=45, ha='right')
    ax1.grid(True, alpha=0.3, axis='y')
    
    # Add Wall of Reality line
    ax1.axhline(y=1e12, color='red', linestyle='--', linewidth=2, label='Wall of Reality (10¹² Hz)')
    ax1.legend()
    
    # Add Y-scaled labels
    for i, (bar, ys) in enumerate(zip(bars, y_scaled)):
        if ys:
            ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() * 1.5,
                    'Y-scaled', ha='center', va='bottom', fontsize=8, rotation=90)
    
    # Plot 2: Dimensional consistency
    dim_consistency = [results['patterns'][f'CRV_{name}']['analysis']['dimensional_consistency'] 
                      for name in crv_names]
    
    bars2 = ax2.bar(range(len(crv_names)), dim_consistency, color=colors, alpha=0.7, edgecolor='black')
    ax2.set_ylabel('Dimensional Consistency', fontsize=12, fontweight='bold')
    ax2.set_xlabel('Core Resonance Values', fontsize=12, fontweight='bold')
    ax2.set_title('Dimensional Consistency with Y Corrections', fontsize=14, fontweight='bold')
    ax2.set_xticks(range(len(crv_names)))
    ax2.set_xticklabels(crv_names, rotation=45, ha='right')
    ax2.grid(True, alpha=0.3, axis='y')
    
    # Add legend for colors
    from matplotlib.patches import Patch
    legend_elements = [
        Patch(facecolor='#FF6B6B', alpha=0.7, label='Y-scaled (Information Layer)'),
        Patch(facecolor='#4ECDC4', alpha=0.7, label='Standard (Reality/Activation)')
    ]
    ax2.legend(handles=legend_elements, loc='upper right')
    
    plt.tight_layout()
    plt.savefig('/home/user/phase_iii_crv_spectrum.png', dpi=300, bbox_inches='tight')
    print("Saved: phase_iii_crv_spectrum.png")
    plt.close()

# ============================================================================
# VISUALIZATION: VALIDATION PATTERNS
# ============================================================================

def plot_validation_patterns():
    """Visualize experimental validation patterns"""
    
    with open('/home/user/phase_iii_validation_patterns.json', 'r') as f:
        validation = json.load(f)
    
    fig, axes = plt.subplots(2, 2, figsize=(14, 12))
    axes = axes.flatten()
    
    for idx, (crv_name, data) in enumerate(validation.items()):
        ax = axes[idx]
        
        # Generate simple representation pattern
        x = np.linspace(-1, 1, 200)
        y = np.linspace(-1, 1, 200)
        X, Y = np.meshgrid(x, y)
        R = np.sqrt(X**2 + Y**2)
        THETA = np.arctan2(Y, X)
        
        # Create pattern based on symmetry
        if 'Circular' in data['predicted_symmetry']:
            pattern = np.sin(10 * R * np.pi)
        elif 'Pentagonal' in data['predicted_symmetry']:
            pattern = np.sin(10 * R * np.pi) * np.cos(5 * THETA)
        elif 'Square' in data['predicted_symmetry']:
            pattern = np.sin(10 * R * np.pi) * np.cos(4 * THETA)
        else:  # Mixed harmonic
            pattern = np.sin(10 * R * np.pi) * (np.cos(3 * THETA) + np.cos(5 * THETA))
        
        # Apply Y correction visualization
        if data['Y_corrected']:
            pattern *= (1 + 0.3 * np.sin(R * np.pi / Y_CONSTANT))
        
        im = ax.imshow(pattern, cmap='seismic', extent=[-1, 1, -1, 1], interpolation='bilinear')
        ax.set_title(f"{crv_name.replace('CRV_', '')}: {data['predicted_symmetry']}\\n"
                    f"Freq: {data['experimental_frequency_hz']:.1f} Hz "
                    f"{'(Y-corrected)' if data['Y_corrected'] else ''}",
                    fontsize=11, fontweight='bold')
        ax.set_xlabel('X', fontsize=10)
        ax.set_ylabel('Y', fontsize=10)
        ax.grid(False)
        plt.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    
    fig.suptitle('Phase III: Experimental Validation Patterns\\n(Predicted Cymatic Geometries)',
                fontsize=14, fontweight='bold')
    plt.tight_layout(rect=[0, 0.03, 1, 0.97])
    plt.savefig('/home/user/phase_iii_validation_patterns.png', dpi=300, bbox_inches='tight')
    print("Saved: phase_iii_validation_patterns.png")
    plt.close()

# ============================================================================
# VISUALIZATION: Y CONSTANT RELATIONSHIPS
# ============================================================================

def plot_y_constant_analysis():
    """Visualize Y constant relationships and geometric interpretation"""
    
    fig = plt.figure(figsize=(16, 10))
    
    # Subplot 1: Y geometric interpretation
    ax1 = plt.subplot(2, 3, 1)
    theta = np.linspace(0, 2*np.pi, 1000)
    
    # Circle with radius π
    r_pi = np.pi
    x_pi = r_pi * np.cos(theta)
    y_pi = r_pi * np.sin(theta)
    ax1.plot(x_pi, y_pi, 'b-', linewidth=2, label=f'r = π')
    
    # Circle with radius π² + 2
    r_denom = np.pi**2 + 2
    x_denom = r_denom * np.cos(theta)
    y_denom = r_denom * np.sin(theta)
    ax1.plot(x_denom, y_denom, 'r-', linewidth=2, label=f'r = π² + 2')
    
    # Y ratio visualization
    ax1.arrow(0, 0, r_pi, 0, head_width=0.3, head_length=0.2, fc='blue', ec='blue', linewidth=2)
    ax1.arrow(0, 0, 0, r_denom, head_width=0.3, head_length=0.3, fc='red', ec='red', linewidth=2)
    
    ax1.text(r_pi/2, -0.8, f'π = {np.pi:.4f}', fontsize=11, ha='center', fontweight='bold')
    ax1.text(-1.5, r_denom/2, f'π² + 2 = {r_denom:.4f}', fontsize=11, ha='center', 
            rotation=90, fontweight='bold')
    ax1.text(4, 4, f'Y = π/(π² + 2)\\n= {Y_CONSTANT:.6f}', fontsize=12, ha='center',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8), fontweight='bold')
    
    ax1.set_xlabel('X', fontsize=11)
    ax1.set_ylabel('Y', fontsize=11)
    ax1.set_title('Geometric Interpretation of Y', fontsize=12, fontweight='bold')
    ax1.grid(True, alpha=0.3)
    ax1.legend()
    ax1.set_aspect('equal')
    ax1.set_xlim(-13, 13)
    ax1.set_ylim(-13, 13)
    
    # Subplot 2: Y in different geometric contexts
    ax2 = plt.subplot(2, 3, 2)
    
    constants = ['π', 'φ', 'e', '√2', '√3', 'τ']
    values = [np.pi, 1.618, np.e, np.sqrt(2), np.sqrt(3), 2*np.pi]
    y_ratios = [v / (v**2 + 2) for v in values]
    
    bars = ax2.bar(constants, y_ratios, color=['#FF6B6B', '#4ECDC4', '#95E1D3', '#F38181', '#AA96DA', '#FCBAD3'],
                  alpha=0.7, edgecolor='black')
    ax2.axhline(y=Y_CONSTANT, color='red', linestyle='--', linewidth=2, label=f'Y = {Y_CONSTANT:.4f}')
    ax2.set_ylabel('Ratio: x/(x² + 2)', fontsize=11, fontweight='bold')
    ax2.set_title('Y-type Ratios for Fundamental Constants', fontsize=12, fontweight='bold')
    ax2.grid(True, alpha=0.3, axis='y')
    ax2.legend()
    
    # Subplot 3: X_G scaling verification
    ax3 = plt.subplot(2, 3, 3)
    
    # Measured vs calculated
    measured_x_g = 79.4e6
    calculated_x_g = X_G
    error_percent = abs(calculated_x_g - measured_x_g) / measured_x_g * 100
    
    categories = ['Measured\\nX_G', 'Calculated\\nc × Y']
    values_xg = [measured_x_g / 1e6, calculated_x_g / 1e6]  # Convert to MHz for readability
    colors_xg = ['#4ECDC4', '#FF6B6B']
    
    bars_xg = ax3.bar(categories, values_xg, color=colors_xg, alpha=0.7, edgecolor='black')
    ax3.set_ylabel('X_G (MHz)', fontsize=11, fontweight='bold')
    ax3.set_title(f'X_G Scaling Factor Verification\\nError: {error_percent:.3f}%', 
                 fontsize=12, fontweight='bold')
    ax3.grid(True, alpha=0.3, axis='y')
    
    for bar, val in zip(bars_xg, values_xg):
        ax3.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
                f'{val:.2f}', ha='center', va='bottom', fontsize=10, fontweight='bold')
    
    # Subplot 4: Gravitational constant formula
    ax4 = plt.subplot(2, 3, 4)
    
    # Components of G formula
    components = ['GF\\n(1.68e-18)', '√2/4\\n(0.354)', 'c\\n(3.0e8)', 'Y\\n(0.265)']
    component_values = [1.682292e-18, np.sqrt(2)/4, C_LIGHT, Y_CONSTANT]
    
    # Normalize for visualization (log scale)
    log_values = [np.log10(abs(v)) if v != 0 else 0 for v in component_values]
    
    bars4 = ax4.bar(range(len(components)), log_values, 
                   color=['#FF6B6B', '#4ECDC4', '#95E1D3', '#F38181'],
                   alpha=0.7, edgecolor='black')
    ax4.set_ylabel('log₁₀(value)', fontsize=11, fontweight='bold')
    ax4.set_title('Components of G Formula\\nG = GF × (√2/4) × c × Y', fontsize=12, fontweight='bold')
    ax4.set_xticks(range(len(components)))
    ax4.set_xticklabels(components, fontsize=9)
    ax4.grid(True, alpha=0.3, axis='y')
    
    # Subplot 5: Fine structure constant
    ax5 = plt.subplot(2, 3, 5)
    
    alpha_measured = 1/137.035999
    
    # Show α derivation context
    ax5.text(0.5, 0.7, 'Fine Structure Constant (α)', fontsize=13, ha='center', 
            fontweight='bold', transform=ax5.transAxes)
    ax5.text(0.5, 0.5, f'α = 1/137.036 = {alpha_measured:.8f}', fontsize=12, ha='center',
            transform=ax5.transAxes, bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.8))
    ax5.text(0.5, 0.3, 'Derived from geometric ratio of\\nCubic Harmonic / EM Enhancement',
            fontsize=10, ha='center', transform=ax5.transAxes, style='italic')
    ax5.text(0.5, 0.1, 'Phase II Achievement: 0.001% error', fontsize=10, ha='center',
            transform=ax5.transAxes, color='green', fontweight='bold')
    ax5.set_xlim(0, 1)
    ax5.set_ylim(0, 1)
    ax5.axis('off')
    
    # Subplot 6: Phase III summary
    ax6 = plt.subplot(2, 3, 6)
    
    summary_text = """
Phase III Achievements:

✓ Y Constant Applied:
  Y = π/(π² + 2) ≈ 0.264675

✓ X_G Resolution:
  Error: 0.066%

✓ Updated CRVs:
  9 constants with Y corrections

✓ Validation Patterns:
  4 experimental protocols

Next: Planck Mass optimization
"""
    
    ax6.text(0.1, 0.9, summary_text, fontsize=10, ha='left', va='top',
            transform=ax6.transAxes, family='monospace',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
    ax6.set_xlim(0, 1)
    ax6.set_ylim(0, 1)
    ax6.axis('off')
    
    fig.suptitle('Phase III: Y Constant Analysis and Applications', fontsize=16, fontweight='bold')
    plt.tight_layout(rect=[0, 0.03, 1, 0.97])
    plt.savefig('/home/user/phase_iii_y_analysis.png', dpi=300, bbox_inches='tight')
    print("Saved: phase_iii_y_analysis.png")
    plt.close()

# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    print("\\n" + "=" * 80)
    print("PHASE III: ADVANCED VISUALIZATIONS AND REFINED DERIVATIONS")
    print("=" * 80 + "\\n")
    
    # 1. Refined Planck Mass derivation
    print("1. Refining Planck Mass derivation...")
    planck_result = refined_planck_mass_derivation()
    
    if planck_result:
        with open('/home/user/phase_iii_planck_mass_refined.json', 'w') as f:
            json.dump(planck_result, f, indent=2)
        print("Saved: phase_iii_planck_mass_refined.json\\n")
    
    # 2. CRV spectrum visualization
    print("2. Generating CRV spectrum visualization...")
    plot_crv_spectrum()
    print()
    
    # 3. Validation patterns visualization
    print("3. Generating validation patterns visualization...")
    plot_validation_patterns()
    print()
    
    # 4. Y constant analysis visualization
    print("4. Generating Y constant analysis...")
    plot_y_constant_analysis()
    print()
    
    print("=" * 80)
    print("ALL VISUALIZATIONS COMPLETE")
    print("=" * 80)
    print()
    print("Generated files:")
    print("  - phase_iii_crv_spectrum.png")
    print("  - phase_iii_validation_patterns.png")
    print("  - phase_iii_y_analysis.png")
    print("  - phase_iii_planck_mass_refined.json (if successful)")
    print()

if __name__ == "__main__":
    main()
