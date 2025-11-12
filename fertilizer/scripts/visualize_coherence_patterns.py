#!/usr/bin/env python3
"""
Visualize Coherence Patterns
Create comprehensive graphs showing how fertilizer coherence works
"""

import json
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm


def load_data():
    """Load the coherence pattern data"""
    with open('/home/ubuntu/ubp_fertilizer_chemical_study/outputs/coherence_patterns.json') as f:
        return json.load(f)


def plot_parameter_importance(patterns):
    """Plot 1: Parameter importance bar chart"""
    fig, ax = plt.subplots(figsize=(10, 6))
    
    params = list(patterns['parameter_importance'].keys())
    correlations = list(patterns['parameter_importance'].values())
    
    # Shorten names for display
    param_labels = ['Molecular\nCoherence', 'Chemical\nPurity', 'Release\nSynchrony']
    
    colors = ['#ff6361' if c > 0.6 else '#ffa600' if c > 0.5 else '#3cba54' for c in correlations]
    bars = ax.bar(param_labels, correlations, color=colors, edgecolor='black', linewidth=1.5)
    
    ax.set_ylabel('Correlation with NRCI', fontsize=12, fontweight='bold')
    ax.set_title('Figure 4: Parameter Importance for Fertilizer Coherence', fontsize=14, fontweight='bold')
    ax.set_ylim(0, 0.8)
    ax.grid(axis='y', linestyle='--', alpha=0.7)
    
    # Add value labels on bars
    for bar, val in zip(bars, correlations):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + 0.02,
                f'{val:.3f}', ha='center', va='bottom', fontweight='bold', fontsize=11)
    
    plt.tight_layout()
    fig.savefig('/home/ubuntu/ubp_fertilizer_chemical_study/docs/figure4_parameter_importance.png', dpi=300)
    print("Generated Figure 4: Parameter Importance")


def plot_optimal_ranges(patterns):
    """Plot 2: Optimal parameter ranges"""
    if 'optimal_ranges' not in patterns:
        print("Skipping optimal ranges plot (no data)")
        return
    
    fig, ax = plt.subplots(figsize=(12, 7))
    
    params = list(patterns['optimal_ranges'].keys())
    param_labels = ['Molecular Coherence', 'Chemical Purity', 'Release Synchrony']
    
    mins = [patterns['optimal_ranges'][p]['min'] for p in params]
    maxs = [patterns['optimal_ranges'][p]['max'] for p in params]
    means = [patterns['optimal_ranges'][p]['mean'] for p in params]
    
    x = np.arange(len(params))
    width = 0.6
    
    # Plot ranges as error bars
    ax.errorbar(x, means, yerr=[np.array(means) - np.array(mins), np.array(maxs) - np.array(means)],
                fmt='o', markersize=12, capsize=10, capthick=3, linewidth=3,
                color='#ff6361', ecolor='#003f5c', label='Optimal Range')
    
    ax.set_xticks(x)
    ax.set_xticklabels(param_labels, fontsize=11)
    ax.set_ylabel('Parameter Value', fontsize=12, fontweight='bold')
    ax.set_title('Figure 5: Optimal Parameter Ranges for High Coherence (NRCI > 0.990)', 
                 fontsize=14, fontweight='bold')
    ax.set_ylim(0.85, 1.0)
    ax.grid(axis='y', linestyle='--', alpha=0.7)
    ax.legend(fontsize=11)
    
    # Add value labels
    for i, (mn, mx, m) in enumerate(zip(mins, maxs, means)):
        ax.text(i, m + 0.005, f'Mean: {m:.3f}', ha='center', fontsize=9, fontweight='bold')
        ax.text(i, mn - 0.005, f'{mn:.3f}', ha='center', fontsize=8, va='top')
        ax.text(i, mx + 0.005, f'{mx:.3f}', ha='center', fontsize=8, va='bottom')
    
    plt.tight_layout()
    fig.savefig('/home/ubuntu/ubp_fertilizer_chemical_study/docs/figure5_optimal_ranges.png', dpi=300)
    print("Generated Figure 5: Optimal Parameter Ranges")


def plot_3d_coherence_landscape(param_data):
    """Plot 3: 3D surface showing NRCI landscape"""
    fig = plt.figure(figsize=(14, 10))
    ax = fig.add_subplot(111, projection='3d')
    
    # Extract data
    data = np.array([[r['molecular_coherence'], r['release_synchrony'], r['nrci']] 
                     for r in param_data if 0.88 < r['chemical_purity'] < 0.92])  # Fix purity at ~0.90
    
    # Create grid
    mol_coh = data[:, 0]
    rel_syn = data[:, 1]
    nrci = data[:, 2]
    
    # Create meshgrid for surface
    mol_unique = np.unique(mol_coh)
    syn_unique = np.unique(rel_syn)
    
    if len(mol_unique) > 1 and len(syn_unique) > 1:
        MOL, SYN = np.meshgrid(mol_unique, syn_unique)
        NRCI = np.zeros_like(MOL)
        
        for i, m in enumerate(mol_unique):
            for j, s in enumerate(syn_unique):
                mask = (np.abs(mol_coh - m) < 0.01) & (np.abs(rel_syn - s) < 0.01)
                if np.any(mask):
                    NRCI[j, i] = np.mean(nrci[mask])
        
        # Plot surface
        surf = ax.plot_surface(MOL, SYN, NRCI, cmap=cm.viridis, alpha=0.8, edgecolor='none')
        
        ax.set_xlabel('Molecular Coherence', fontsize=11, fontweight='bold')
        ax.set_ylabel('Release Synchrony', fontsize=11, fontweight='bold')
        ax.set_zlabel('System NRCI', fontsize=11, fontweight='bold')
        ax.set_title('Figure 6: Coherence Landscape\n(Chemical Purity fixed at 0.90)', 
                     fontsize=14, fontweight='bold')
        
        fig.colorbar(surf, ax=ax, shrink=0.5, aspect=5, label='NRCI')
        
        plt.tight_layout()
        fig.savefig('/home/ubuntu/ubp_fertilizer_chemical_study/docs/figure6_coherence_landscape.png', dpi=300)
        print("Generated Figure 6: 3D Coherence Landscape")


def plot_blend_composition_effects(blend_2comp):
    """Plot 4: Blend composition effects"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
    
    # Plot 1: Quality gap effect
    data_50_50 = [r for r in blend_2comp if abs(r['ratio'] - 0.50) < 0.01]
    gaps = [r['quality_gap'] for r in data_50_50]
    nrcis = [r['nrci'] for r in data_50_50]
    
    ax1.scatter(gaps, nrcis, alpha=0.6, s=50, color='#ff6361', edgecolors='black')
    ax1.set_xlabel('Quality Gap (High - Low)', fontsize=11, fontweight='bold')
    ax1.set_ylabel('System NRCI', fontsize=11, fontweight='bold')
    ax1.set_title('Effect of Quality Gap\n(50/50 blend)', fontsize=12, fontweight='bold')
    ax1.grid(True, linestyle='--', alpha=0.7)
    
    # Add trend line
    z = np.polyfit(gaps, nrcis, 1)
    p = np.poly1d(z)
    ax1.plot(sorted(gaps), p(sorted(gaps)), "r--", linewidth=2, label=f'Trend: {z[0]:.2f}x + {z[1]:.2f}')
    ax1.legend()
    
    # Plot 2: Ratio effect for fixed quality gap
    data_fixed_gap = [r for r in blend_2comp if 0.18 < r['quality_gap'] < 0.22]  # ~0.20 gap
    ratios = [r['ratio'] for r in data_fixed_gap]
    nrcis2 = [r['nrci'] for r in data_fixed_gap]
    
    ax2.scatter(ratios, nrcis2, alpha=0.6, s=50, color='#3cba54', edgecolors='black')
    ax2.set_xlabel('High Quality Ratio', fontsize=11, fontweight='bold')
    ax2.set_ylabel('System NRCI', fontsize=11, fontweight='bold')
    ax2.set_title('Effect of Blend Ratio\n(Quality gap ~0.20)', fontsize=12, fontweight='bold')
    ax2.grid(True, linestyle='--', alpha=0.7)
    
    # Add trend line
    z2 = np.polyfit(ratios, nrcis2, 1)
    p2 = np.poly1d(z2)
    ax2.plot(sorted(ratios), p2(sorted(ratios)), "r--", linewidth=2, label=f'Trend: {z2[0]:.2f}x + {z2[1]:.2f}')
    ax2.legend()
    
    fig.suptitle('Figure 7: Blend Composition Effects on Coherence', fontsize=14, fontweight='bold', y=1.02)
    plt.tight_layout()
    fig.savefig('/home/ubuntu/ubp_fertilizer_chemical_study/docs/figure7_blend_composition.png', dpi=300)
    print("Generated Figure 7: Blend Composition Effects")


def plot_design_guidelines(patterns):
    """Plot 5: Design guidelines flowchart-style"""
    fig, ax = plt.subplots(figsize=(14, 10))
    ax.axis('off')
    
    # Title
    ax.text(0.5, 0.95, 'Figure 8: Fertilizer Coherence Design Guidelines', 
            ha='center', fontsize=16, fontweight='bold', transform=ax.transAxes)
    
    # Box 1: Start
    ax.add_patch(plt.Rectangle((0.35, 0.85), 0.3, 0.06, facecolor='#003f5c', edgecolor='black', linewidth=2))
    ax.text(0.5, 0.88, 'START: Design High-Coherence Fertilizer', 
            ha='center', va='center', fontsize=11, fontweight='bold', color='white', transform=ax.transAxes)
    
    # Arrow
    ax.arrow(0.5, 0.85, 0, -0.04, head_width=0.02, head_length=0.01, fc='black', ec='black', transform=ax.transAxes)
    
    # Box 2: Parameter Selection
    ax.add_patch(plt.Rectangle((0.05, 0.68), 0.9, 0.12, facecolor='#ff6361', edgecolor='black', linewidth=2, alpha=0.3))
    ax.text(0.5, 0.78, 'STEP 1: Optimize Individual Parameters', 
            ha='center', fontsize=12, fontweight='bold', transform=ax.transAxes)
    ax.text(0.5, 0.74, '• Release Synchrony: 0.894 - 0.960 (MOST IMPORTANT)', 
            ha='center', fontsize=10, transform=ax.transAxes)
    ax.text(0.5, 0.71, '• Molecular Coherence: 0.928 - 0.990', 
            ha='center', fontsize=10, transform=ax.transAxes)
    ax.text(0.5, 0.68, '• Chemical Purity: 0.925 - 0.995', 
            ha='center', fontsize=10, transform=ax.transAxes)
    
    # Arrow
    ax.arrow(0.5, 0.68, 0, -0.04, head_width=0.02, head_length=0.01, fc='black', ec='black', transform=ax.transAxes)
    
    # Box 3: Blend Composition
    ax.add_patch(plt.Rectangle((0.05, 0.48), 0.9, 0.15, facecolor='#ffa600', edgecolor='black', linewidth=2, alpha=0.3))
    ax.text(0.5, 0.61, 'STEP 2: Design Blend Composition', 
            ha='center', fontsize=12, fontweight='bold', transform=ax.transAxes)
    ax.text(0.5, 0.57, '• MINIMIZE quality gaps between components', 
            ha='center', fontsize=10, transform=ax.transAxes)
    ax.text(0.5, 0.54, '• Use higher ratios of high-quality components', 
            ha='center', fontsize=10, transform=ax.transAxes)
    ax.text(0.5, 0.51, '• Keep component variance LOW (consistency matters)', 
            ha='center', fontsize=10, transform=ax.transAxes)
    ax.text(0.5, 0.48, '• Fewer, higher-quality components > many mixed-quality components', 
            ha='center', fontsize=10, transform=ax.transAxes)
    
    # Arrow
    ax.arrow(0.5, 0.48, 0, -0.04, head_width=0.02, head_length=0.01, fc='black', ec='black', transform=ax.transAxes)
    
    # Box 4: Target NRCI
    ax.add_patch(plt.Rectangle((0.05, 0.32), 0.9, 0.11, facecolor='#3cba54', edgecolor='black', linewidth=2, alpha=0.3))
    ax.text(0.5, 0.41, 'STEP 3: Validate Against Target', 
            ha='center', fontsize=12, fontweight='bold', transform=ax.transAxes)
    ax.text(0.5, 0.37, '• Target NRCI: > 0.990 (approaching PGCI of 0.999997)', 
            ha='center', fontsize=10, transform=ax.transAxes)
    ax.text(0.5, 0.34, '• Expected improvement: 4-5% over baseline products', 
            ha='center', fontsize=10, transform=ax.transAxes)
    ax.text(0.5, 0.31, '• Synergy factor: aim for ≥ 1.00 (neutral to positive)', 
            ha='center', fontsize=10, transform=ax.transAxes)
    
    # Arrow
    ax.arrow(0.5, 0.31, 0, -0.04, head_width=0.02, head_length=0.01, fc='black', ec='black', transform=ax.transAxes)
    
    # Box 5: Manufacturing
    ax.add_patch(plt.Rectangle((0.05, 0.15), 0.9, 0.11, facecolor='#bc5090', edgecolor='black', linewidth=2, alpha=0.3))
    ax.text(0.5, 0.24, 'STEP 4: Manufacturing Considerations', 
            ha='center', fontsize=12, fontweight='bold', transform=ax.transAxes)
    ax.text(0.5, 0.20, '• Use pharmaceutical-grade or technical-grade chemicals', 
            ha='center', fontsize=10, transform=ax.transAxes)
    ax.text(0.5, 0.17, '• Apply controlled-release coatings (polymer, sulfur)', 
            ha='center', fontsize=10, transform=ax.transAxes)
    ax.text(0.5, 0.14, '• Maintain crystalline structure during processing', 
            ha='center', fontsize=10, transform=ax.transAxes)
    
    # Arrow
    ax.arrow(0.5, 0.14, 0, -0.04, head_width=0.02, head_length=0.01, fc='black', ec='black', transform=ax.transAxes)
    
    # Box 6: Result
    ax.add_patch(plt.Rectangle((0.3, 0.03), 0.4, 0.06, facecolor='#003f5c', edgecolor='black', linewidth=2))
    ax.text(0.5, 0.06, 'RESULT: High-Coherence Fertilizer', 
            ha='center', va='center', fontsize=11, fontweight='bold', color='white', transform=ax.transAxes)
    
    plt.tight_layout()
    fig.savefig('/home/ubuntu/ubp_fertilizer_chemical_study/docs/figure8_design_guidelines.png', dpi=300)
    print("Generated Figure 8: Design Guidelines")


def main():
    """Generate all visualizations"""
    print("="*80)
    print("GENERATING COHERENCE PATTERN VISUALIZATIONS")
    print("="*80)
    
    data = load_data()
    
    plot_parameter_importance(data['patterns'])
    plot_optimal_ranges(data['patterns'])
    plot_3d_coherence_landscape(data['parameter_space'])
    plot_blend_composition_effects(data['blend_2component'])
    plot_design_guidelines(data['patterns'])
    
    print("\n" + "="*80)
    print("ALL VISUALIZATIONS COMPLETE")
    print("="*80)


if __name__ == '__main__':
    main()
