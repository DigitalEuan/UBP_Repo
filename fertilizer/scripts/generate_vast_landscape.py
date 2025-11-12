#!/usr/bin/env python3
"""
Generate Vast Coherence Landscape
Explore the full theoretical parameter space from poor to perfect coherence
"""

import sys
sys.path.append('/home/ubuntu/ubp_fertilizer_chemical_study/scripts')

from ubp_chemical_framework import UBPChemicalFramework, FertilizerComponent
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
import json


def generate_vast_landscape():
    """Generate comprehensive landscape data across full theoretical range"""
    
    framework = UBPChemicalFramework()
    
    # VASTLY EXPANDED RANGES
    # From poor quality (0.30) to theoretical perfect (0.999)
    mol_coh_range = np.linspace(0.30, 0.999, 50)  # 50 points
    rel_syn_range = np.linspace(0.30, 0.999, 50)  # 50 points
    chem_pur_fixed = 0.90  # Fix purity for 3D visualization
    
    print("="*80)
    print("GENERATING VAST COHERENCE LANDSCAPE")
    print("="*80)
    print(f"Molecular Coherence range: {mol_coh_range[0]:.3f} - {mol_coh_range[-1]:.3f}")
    print(f"Release Synchrony range: {rel_syn_range[0]:.3f} - {rel_syn_range[-1]:.3f}")
    print(f"Chemical Purity (fixed): {chem_pur_fixed:.3f}")
    print(f"Total combinations: {len(mol_coh_range) * len(rel_syn_range)}")
    print("="*80)
    
    # Create meshgrid
    MOL, SYN = np.meshgrid(mol_coh_range, rel_syn_range)
    NRCI = np.zeros_like(MOL)
    
    # Calculate NRCI for each combination
    total = len(mol_coh_range) * len(rel_syn_range)
    count = 0
    
    for i, mol_coh in enumerate(mol_coh_range):
        for j, rel_syn in enumerate(rel_syn_range):
            count += 1
            if count % 250 == 0:
                print(f"Progress: {count}/{total} ({100*count/total:.1f}%)")
            
            component = FertilizerComponent(
                name="Test",
                formula="Test",
                npk_contribution=(20.0, 10.0, 10.0),
                molecular_coherence=mol_coh,
                chemical_purity=chem_pur_fixed,
                release_synchrony=rel_syn,
                concentration=100.0
            )
            
            result = framework.analyze_fertilizer_blend([component])
            NRCI[j, i] = result['system_nrci']
    
    print(f"Complete! Generated {total} data points")
    
    # Save data
    data = {
        'molecular_coherence': mol_coh_range.tolist(),
        'release_synchrony': rel_syn_range.tolist(),
        'chemical_purity_fixed': chem_pur_fixed,
        'nrci_grid': NRCI.tolist(),
        'nrci_min': float(np.min(NRCI)),
        'nrci_max': float(np.max(NRCI)),
        'nrci_mean': float(np.mean(NRCI))
    }
    
    with open('/home/ubuntu/ubp_fertilizer_chemical_study/outputs/vast_landscape_data.json', 'w') as f:
        json.dump(data, f, indent=2)
    
    print(f"\nNRCI Statistics:")
    print(f"  Minimum: {np.min(NRCI):.6f}")
    print(f"  Maximum: {np.max(NRCI):.6f}")
    print(f"  Mean: {np.mean(NRCI):.6f}")
    print(f"  Range: {np.max(NRCI) - np.min(NRCI):.6f}")
    
    return MOL, SYN, NRCI, data


def create_vast_landscape_visualizations(MOL, SYN, NRCI, data):
    """Create comprehensive visualizations of the vast landscape"""
    
    print("\n" + "="*80)
    print("CREATING VISUALIZATIONS")
    print("="*80)
    
    # Figure 1: Main 3D Surface
    fig1 = plt.figure(figsize=(16, 12))
    ax1 = fig1.add_subplot(111, projection='3d')
    
    surf = ax1.plot_surface(MOL, SYN, NRCI, cmap=cm.viridis, alpha=0.9, 
                            edgecolor='none', antialiased=True)
    
    ax1.set_xlabel('Molecular Coherence', fontsize=13, fontweight='bold', labelpad=10)
    ax1.set_ylabel('Release Synchrony', fontsize=13, fontweight='bold', labelpad=10)
    ax1.set_zlabel('System NRCI', fontsize=13, fontweight='bold', labelpad=10)
    ax1.set_title('Figure 9: The Vast Coherence Landscape\n' + 
                  f'Full Theoretical Range (Chemical Purity = {data["chemical_purity_fixed"]:.2f})',
                  fontsize=15, fontweight='bold', pad=20)
    
    # Add colorbar
    cbar = fig1.colorbar(surf, ax=ax1, shrink=0.5, aspect=10, pad=0.1)
    cbar.set_label('System NRCI', fontsize=11, fontweight='bold')
    
    # Set viewing angle
    ax1.view_init(elev=25, azim=45)
    
    # Add grid
    ax1.grid(True, alpha=0.3)
    
    plt.tight_layout()
    fig1.savefig('/home/ubuntu/ubp_fertilizer_chemical_study/docs/figure9_vast_landscape_3d.png', dpi=300, bbox_inches='tight')
    print("Generated Figure 9: Vast 3D Landscape")
    
    # Figure 2: Contour Plot (Top-Down View)
    fig2, ax2 = plt.subplots(figsize=(14, 12))
    
    # Create filled contour plot
    levels = np.linspace(np.min(NRCI), np.max(NRCI), 20)
    contourf = ax2.contourf(MOL, SYN, NRCI, levels=levels, cmap=cm.viridis, alpha=0.9)
    contour = ax2.contour(MOL, SYN, NRCI, levels=levels, colors='black', alpha=0.3, linewidths=0.5)
    
    # Add contour labels
    ax2.clabel(contour, inline=True, fontsize=8, fmt='%.3f')
    
    # Mark current fertilizer region
    current_region_x = [0.92, 0.99, 0.99, 0.92, 0.92]
    current_region_y = [0.85, 0.85, 0.96, 0.96, 0.85]
    ax2.plot(current_region_x, current_region_y, 'r-', linewidth=3, label='Current Fertilizers')
    ax2.fill(current_region_x, current_region_y, color='red', alpha=0.2)
    
    # Mark theoretical maximum region
    max_region_x = [0.96, 0.999, 0.999, 0.96, 0.96]
    max_region_y = [0.94, 0.94, 0.999, 0.999, 0.94]
    ax2.plot(max_region_x, max_region_y, 'g--', linewidth=3, label='Theoretical Maximum')
    ax2.fill(max_region_x, max_region_y, color='green', alpha=0.1)
    
    ax2.set_xlabel('Molecular Coherence', fontsize=13, fontweight='bold')
    ax2.set_ylabel('Release Synchrony', fontsize=13, fontweight='bold')
    ax2.set_title('Figure 10: Coherence Landscape Contour Map\n' +
                  'Showing Current vs. Theoretical Maximum Regions',
                  fontsize=15, fontweight='bold', pad=15)
    
    cbar2 = fig2.colorbar(contourf, ax=ax2, label='System NRCI')
    cbar2.set_label('System NRCI', fontsize=11, fontweight='bold')
    
    ax2.legend(fontsize=11, loc='lower left')
    ax2.grid(True, alpha=0.3, linestyle='--')
    
    plt.tight_layout()
    fig2.savefig('/home/ubuntu/ubp_fertilizer_chemical_study/docs/figure10_vast_landscape_contour.png', dpi=300, bbox_inches='tight')
    print("Generated Figure 10: Contour Map with Regions")
    
    # Figure 3: Cross-Sections
    fig3, ((ax3a, ax3b), (ax3c, ax3d)) = plt.subplots(2, 2, figsize=(16, 14))
    
    # Cross-section 1: High release synchrony (0.95)
    idx_high_syn = np.argmin(np.abs(data['release_synchrony'] - np.array([0.95])))
    ax3a.plot(data['molecular_coherence'], NRCI[idx_high_syn, :], 'b-', linewidth=2)
    ax3a.axvline(0.95, color='red', linestyle='--', linewidth=2, label='Current Products')
    ax3a.set_xlabel('Molecular Coherence', fontweight='bold')
    ax3a.set_ylabel('System NRCI', fontweight='bold')
    ax3a.set_title('Cross-Section: High Release Synchrony (0.95)', fontweight='bold')
    ax3a.grid(True, alpha=0.3)
    ax3a.legend()
    
    # Cross-section 2: Medium release synchrony (0.70)
    idx_med_syn = np.argmin(np.abs(data['release_synchrony'] - np.array([0.70])))
    ax3b.plot(data['molecular_coherence'], NRCI[idx_med_syn, :], 'orange', linewidth=2)
    ax3b.axvline(0.95, color='red', linestyle='--', linewidth=2, label='Current Products')
    ax3b.set_xlabel('Molecular Coherence', fontweight='bold')
    ax3b.set_ylabel('System NRCI', fontweight='bold')
    ax3b.set_title('Cross-Section: Medium Release Synchrony (0.70)', fontweight='bold')
    ax3b.grid(True, alpha=0.3)
    ax3b.legend()
    
    # Cross-section 3: High molecular coherence (0.95)
    idx_high_mol = np.argmin(np.abs(data['molecular_coherence'] - np.array([0.95])))
    ax3c.plot(data['release_synchrony'], NRCI[:, idx_high_mol], 'g-', linewidth=2)
    ax3c.axvline(0.92, color='red', linestyle='--', linewidth=2, label='Current Products')
    ax3c.set_xlabel('Release Synchrony', fontweight='bold')
    ax3c.set_ylabel('System NRCI', fontweight='bold')
    ax3c.set_title('Cross-Section: High Molecular Coherence (0.95)', fontweight='bold')
    ax3c.grid(True, alpha=0.3)
    ax3c.legend()
    
    # Cross-section 4: Poor molecular coherence (0.50)
    idx_poor_mol = np.argmin(np.abs(data['molecular_coherence'] - np.array([0.50])))
    ax3d.plot(data['release_synchrony'], NRCI[:, idx_poor_mol], 'purple', linewidth=2)
    ax3d.axvline(0.92, color='red', linestyle='--', linewidth=2, label='Current Products')
    ax3d.set_xlabel('Release Synchrony', fontweight='bold')
    ax3d.set_ylabel('System NRCI', fontweight='bold')
    ax3d.set_title('Cross-Section: Poor Molecular Coherence (0.50)', fontweight='bold')
    ax3d.grid(True, alpha=0.3)
    ax3d.legend()
    
    fig3.suptitle('Figure 11: Cross-Sectional Views of the Coherence Landscape', 
                  fontsize=15, fontweight='bold', y=0.995)
    plt.tight_layout()
    fig3.savefig('/home/ubuntu/ubp_fertilizer_chemical_study/docs/figure11_cross_sections.png', dpi=300, bbox_inches='tight')
    print("Generated Figure 11: Cross-Sections")
    
    print("="*80)
    print("ALL VISUALIZATIONS COMPLETE")
    print("="*80)


def main():
    """Main execution"""
    MOL, SYN, NRCI, data = generate_vast_landscape()
    create_vast_landscape_visualizations(MOL, SYN, NRCI, data)
    
    print("\nData saved to: /home/ubuntu/ubp_fertilizer_chemical_study/outputs/vast_landscape_data.json")
    print("Figures saved to: /home/ubuntu/ubp_fertilizer_chemical_study/docs/")


if __name__ == '__main__':
    main()
