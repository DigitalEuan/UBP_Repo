"""
UBP VIROLOGY VISUALIZATIONS
============================
Generates all scientific figures for the UBP Virology study paper.

Figures:
1. Protein NRCI Landscape (bar chart)
2. Leech Tax Comparison (variant evolution)
3. Tilt Angle Polar Plot (Universal North alignment)
4. 24-bit Vector Heatmap (all 12 proteins)
5. TGIC Energy Landscape (all 2-node interactions)
6. Antibody Efficacy Matrix (Hamming distance heatmap)
7. Cytokine Storm Intervention (before/after Tax)
8. Variant Evolution Timeline (Tax + Tilt progression)
9. Golay Code Capture Zone (interaction network)
10. UBP vs Clinical Validation Summary

Author: Manus AI for Euan Craig (UBP Research)
"""

import json
import sys
import math
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.gridspec import GridSpec
from matplotlib.colors import LinearSegmentedColormap
import matplotlib.patheffects as pe
from fractions import Fraction

# Load data
with open('/home/ubuntu/virology_kb_entries_v2.json', 'r') as f:
    kb = json.load(f)

with open('/home/ubuntu/ubp_virology_full_report_v2.json', 'r') as f:
    report = json.load(f)

with open('/home/ubuntu/ubp_validation_report.json', 'r') as f:
    validation = json.load(f)

# Color scheme
UBP_BLUE = '#1a3a5c'
UBP_CYAN = '#00b4d8'
UBP_GREEN = '#06d6a0'
UBP_RED = '#ef233c'
UBP_ORANGE = '#f77f00'
UBP_PURPLE = '#7209b7'
UBP_GOLD = '#ffd60a'
UBP_DARK = '#0d1b2a'
UBP_LIGHT = '#e8f4f8'

plt.rcParams.update({
    'font.family': 'DejaVu Sans',
    'font.size': 10,
    'axes.titlesize': 12,
    'axes.labelsize': 10,
    'figure.facecolor': UBP_DARK,
    'axes.facecolor': '#0d2137',
    'axes.edgecolor': UBP_CYAN,
    'text.color': 'white',
    'axes.labelcolor': 'white',
    'xtick.color': 'white',
    'ytick.color': 'white',
    'grid.color': '#1a3a5c',
    'grid.alpha': 0.5
})

os_path = '/home/ubuntu/ubp_virology_figures'
import os
os.makedirs(os_path, exist_ok=True)

# ============================================================
# FIGURE 1: PROTEIN NRCI LANDSCAPE
# ============================================================
def fig1_nrci_landscape():
    entries = list(kb.values())
    names = [e['ubp_id'].replace('PROTEIN_', '').replace('_001', '').replace('VIRAL_', '').replace('HOST_', '').replace('ANTIBODY_', 'Ab_') for e in entries]
    nrci_vals = [e['atlas']['nrci_score'] for e in entries]
    tax_vals = [float(Fraction(e['atlas']['tax'])) for e in entries]
    
    # Color by category
    colors = []
    for e in entries:
        tags = e.get('tags', [])
        if 'ANTIBODY' in tags:
            colors.append(UBP_GREEN)
        elif 'HOST' in tags:
            colors.append(UBP_CYAN)
        elif 'OMICRON' in tags or 'DELTA' in tags:
            colors.append(UBP_RED)
        else:
            colors.append(UBP_BLUE)
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7))
    fig.suptitle('Figure 1: UBP Protein NRCI & Leech Tax Landscape\nAll 12 Viral Proteins (SOP_002 Standard)', 
                 color='white', fontsize=14, fontweight='bold', y=1.02)
    
    # NRCI bars
    bars = ax1.barh(range(len(names)), nrci_vals, color=colors, edgecolor=UBP_CYAN, linewidth=0.5, alpha=0.85)
    ax1.set_yticks(range(len(names)))
    ax1.set_yticklabels(names, fontsize=8)
    ax1.set_xlabel('NRCI Score (Hyperbolic Coherence)', color='white')
    ax1.set_title('NRCI — Normalized Resonance Coherence Index', color=UBP_CYAN, fontweight='bold')
    ax1.axvline(x=0.7, color=UBP_GOLD, linestyle='--', alpha=0.7, label='Stability threshold')
    ax1.set_xlim(0, 1.0)
    ax1.legend(facecolor=UBP_DARK, edgecolor=UBP_CYAN, labelcolor='white')
    
    # Add value labels
    for i, (bar, val) in enumerate(zip(bars, nrci_vals)):
        ax1.text(val + 0.01, i, f'{val:.4f}', va='center', fontsize=7, color='white')
    
    # Tax bars
    bars2 = ax2.barh(range(len(names)), tax_vals, color=colors, edgecolor=UBP_CYAN, linewidth=0.5, alpha=0.85)
    ax2.set_yticks(range(len(names)))
    ax2.set_yticklabels(names, fontsize=8)
    ax2.set_xlabel('Leech Lattice Symmetry Tax', color='white')
    ax2.set_title('Symmetry Tax — Geometric Complexity Cost', color=UBP_CYAN, fontweight='bold')
    
    for i, (bar, val) in enumerate(zip(bars2, tax_vals)):
        ax2.text(val + 0.02, i, f'{val:.4f}', va='center', fontsize=7, color='white')
    
    # Legend
    legend_patches = [
        mpatches.Patch(color=UBP_BLUE, label='SARS-CoV-2 Proteins'),
        mpatches.Patch(color=UBP_RED, label='Variants (Delta/Omicron)'),
        mpatches.Patch(color=UBP_GREEN, label='Antibodies'),
        mpatches.Patch(color=UBP_CYAN, label='Host Receptor (ACE2)'),
    ]
    ax2.legend(handles=legend_patches, facecolor=UBP_DARK, edgecolor=UBP_CYAN, labelcolor='white', loc='lower right')
    
    plt.tight_layout()
    path = f'{os_path}/fig1_nrci_landscape.png'
    plt.savefig(path, dpi=150, bbox_inches='tight', facecolor=UBP_DARK)
    plt.close()
    print(f"  Saved: {path}")
    return path

# ============================================================
# FIGURE 2: VARIANT EVOLUTION (TAX + TILT)
# ============================================================
def fig2_variant_evolution():
    variants = report['sections']['2_variant_evolution']
    
    names = list(variants.keys())
    taxes = [variants[n]['leech_tax'] for n in names]
    tilts = [variants[n]['tilt_degrees'] for n in names]
    nrcis = [variants[n]['nrci'] for n in names]
    
    fig, axes = plt.subplots(1, 3, figsize=(16, 6))
    fig.suptitle('Figure 2: SARS-CoV-2 Variant Evolution — UBP Geometric Metrics\nWT → Delta → Omicron Progression', 
                 color='white', fontsize=14, fontweight='bold')
    
    colors_v = [UBP_BLUE, UBP_ORANGE, UBP_RED]
    
    # Tax comparison
    bars = axes[0].bar(names, taxes, color=colors_v, edgecolor=UBP_CYAN, linewidth=1.5, alpha=0.9, width=0.6)
    axes[0].set_title('Leech Tax (Geometric Complexity)\nLower = Higher Evolutionary Fitness', color=UBP_CYAN, fontweight='bold')
    axes[0].set_ylabel('Symmetry Tax Value', color='white')
    for bar, val in zip(bars, taxes):
        axes[0].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.05, f'{val:.4f}', 
                    ha='center', va='bottom', fontsize=11, color='white', fontweight='bold')
    axes[0].set_ylim(0, max(taxes) * 1.25)
    
    # Arrow showing evolution direction
    axes[0].annotate('', xy=(2, min(taxes) + 0.2), xytext=(0, max(taxes) - 0.2),
                    arrowprops=dict(arrowstyle='->', color=UBP_GREEN, lw=2))
    axes[0].text(1.5, (min(taxes) + max(taxes))/2, 'Evolution\ndirection', 
                ha='center', color=UBP_GREEN, fontsize=9)
    
    # Tilt comparison
    bars2 = axes[1].bar(names, tilts, color=colors_v, edgecolor=UBP_CYAN, linewidth=1.5, alpha=0.9, width=0.6)
    axes[1].set_title('Tilt from Universal North (°)\nLower = More Geometrically Aligned', color=UBP_CYAN, fontweight='bold')
    axes[1].set_ylabel('Tilt Angle (degrees)', color='white')
    for bar, val in zip(bars2, tilts):
        axes[1].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1, f'{val:.1f}°', 
                    ha='center', va='bottom', fontsize=11, color='white', fontweight='bold')
    axes[1].axhline(y=90, color=UBP_GOLD, linestyle='--', alpha=0.7, label='90° equator')
    axes[1].legend(facecolor=UBP_DARK, edgecolor=UBP_CYAN, labelcolor='white')
    
    # NRCI comparison
    bars3 = axes[2].bar(names, nrcis, color=colors_v, edgecolor=UBP_CYAN, linewidth=1.5, alpha=0.9, width=0.6)
    axes[2].set_title('NRCI Score\nCoherence Index', color=UBP_CYAN, fontweight='bold')
    axes[2].set_ylabel('NRCI', color='white')
    for bar, val in zip(bars3, nrcis):
        axes[2].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.005, f'{val:.4f}', 
                    ha='center', va='bottom', fontsize=11, color='white', fontweight='bold')
    axes[2].set_ylim(0, 1.0)
    
    plt.tight_layout()
    path = f'{os_path}/fig2_variant_evolution.png'
    plt.savefig(path, dpi=150, bbox_inches='tight', facecolor=UBP_DARK)
    plt.close()
    print(f"  Saved: {path}")
    return path

# ============================================================
# FIGURE 3: 24-BIT VECTOR HEATMAP
# ============================================================
def fig3_vector_heatmap():
    entries = list(kb.values())
    names = [e['ubp_id'].replace('PROTEIN_', '').replace('_001', '').replace('VIRAL_', '').replace('HOST_', '').replace('ANTIBODY_', 'Ab_') for e in entries]
    vectors = np.array([e['atlas']['vector'] for e in entries])
    
    fig, ax = plt.subplots(figsize=(18, 8))
    fig.suptitle('Figure 3: UBP 24-Bit Golay Vector Heatmap\nAll 12 Viral Proteins — Geometric Fingerprints', 
                 color='white', fontsize=14, fontweight='bold')
    
    cmap = LinearSegmentedColormap.from_list('ubp', [UBP_DARK, UBP_BLUE, UBP_CYAN, UBP_GREEN])
    
    im = ax.imshow(vectors, cmap=cmap, aspect='auto', interpolation='nearest')
    
    ax.set_yticks(range(len(names)))
    ax.set_yticklabels(names, fontsize=9)
    ax.set_xticks(range(24))
    ax.set_xticklabels([f'B{i+1}' for i in range(24)], fontsize=8, rotation=45)
    ax.set_xlabel('Bit Position (Golay [24,12,8] Codeword)', color='white')
    ax.set_title('Each row is a unique 24-bit geometric fingerprint derived from physicochemical properties', 
                color=UBP_CYAN, fontsize=10)
    
    # Add bit values as text
    for i in range(len(entries)):
        for j in range(24):
            val = vectors[i, j]
            ax.text(j, i, str(val), ha='center', va='center', 
                   fontsize=7, color='white' if val == 1 else UBP_CYAN, fontweight='bold')
    
    # Colorbar
    cbar = plt.colorbar(im, ax=ax, fraction=0.02, pad=0.04)
    cbar.set_label('Bit Value (0/1)', color='white')
    cbar.ax.yaxis.set_tick_params(color='white')
    plt.setp(cbar.ax.yaxis.get_ticklabels(), color='white')
    
    # Highlight Golay octads (positions 0-7, 8-15, 16-23)
    for x in [7.5, 15.5]:
        ax.axvline(x=x, color=UBP_GOLD, linewidth=2, alpha=0.7, linestyle='--')
    ax.text(3.5, -1, 'Octad 1', ha='center', color=UBP_GOLD, fontsize=9)
    ax.text(11.5, -1, 'Octad 2', ha='center', color=UBP_GOLD, fontsize=9)
    ax.text(19.5, -1, 'Octad 3', ha='center', color=UBP_GOLD, fontsize=9)
    
    plt.tight_layout()
    path = f'{os_path}/fig3_vector_heatmap.png'
    plt.savefig(path, dpi=150, bbox_inches='tight', facecolor=UBP_DARK)
    plt.close()
    print(f"  Saved: {path}")
    return path

# ============================================================
# FIGURE 4: TGIC ENERGY LANDSCAPE
# ============================================================
def fig4_energy_landscape():
    landscape = validation['energy_landscape']
    
    names = [l['interaction'] for l in landscape]
    energies = [l['energy'] for l in landscape]
    contexts = [l['biological_context'] for l in landscape]
    
    # Color by biological significance
    colors_e = []
    for ctx in contexts:
        if 'entry' in ctx.lower() or 'entry' in ctx.lower():
            colors_e.append(UBP_RED)
        elif 'neutralization' in ctx.lower():
            colors_e.append(UBP_GREEN)
        elif 'assembly' in ctx.lower():
            colors_e.append(UBP_ORANGE)
        elif 'cross-virus' in ctx.lower():
            colors_e.append(UBP_PURPLE)
        else:
            colors_e.append(UBP_BLUE)
    
    fig, ax = plt.subplots(figsize=(16, 8))
    fig.suptitle('Figure 4: TGIC Relational Gravity — Energy Landscape\nAll Biologically Relevant 2-Node Interactions', 
                 color='white', fontsize=14, fontweight='bold')
    
    bars = ax.barh(range(len(names)), energies, color=colors_e, edgecolor=UBP_CYAN, linewidth=0.5, alpha=0.85)
    ax.set_yticks(range(len(names)))
    ax.set_yticklabels(names, fontsize=9)
    ax.set_xlabel('TGIC Total System Energy (lower = more favorable)', color='white')
    ax.set_title('Lower energy = stronger geometric affinity between proteins', color=UBP_CYAN)
    
    for i, (bar, val) in enumerate(zip(bars, energies)):
        ax.text(val + 0.5, i, f'{val:.2f}', va='center', fontsize=8, color='white')
    
    # Highlight key interactions
    min_e = min(energies)
    max_e = max(energies)
    ax.axvline(x=np.mean(energies), color=UBP_GOLD, linestyle='--', alpha=0.7, label=f'Mean energy ({np.mean(energies):.1f})')
    ax.legend(facecolor=UBP_DARK, edgecolor=UBP_CYAN, labelcolor='white')
    
    legend_patches = [
        mpatches.Patch(color=UBP_RED, label='Viral Entry'),
        mpatches.Patch(color=UBP_GREEN, label='Antibody Neutralization'),
        mpatches.Patch(color=UBP_ORANGE, label='Viral Assembly'),
        mpatches.Patch(color=UBP_PURPLE, label='Cross-virus (control)'),
        mpatches.Patch(color=UBP_BLUE, label='Other'),
    ]
    ax.legend(handles=legend_patches, facecolor=UBP_DARK, edgecolor=UBP_CYAN, labelcolor='white', loc='lower right')
    
    plt.tight_layout()
    path = f'{os_path}/fig4_energy_landscape.png'
    plt.savefig(path, dpi=150, bbox_inches='tight', facecolor=UBP_DARK)
    plt.close()
    print(f"  Saved: {path}")
    return path

# ============================================================
# FIGURE 5: ANTIBODY EFFICACY MATRIX
# ============================================================
def fig5_antibody_matrix():
    ab_data = report['sections']['5_antibody_efficacy']
    
    antibodies = ['CR3022', 'S309']
    antigens = ['WT_Spike', 'Delta_Spike', 'Omicron_Spike']
    
    hamming_matrix = np.zeros((2, 3))
    gap_matrix = np.zeros((2, 3))
    nrci_matrix = np.zeros((2, 3))
    
    for i, ab in enumerate(antibodies):
        for j, ag in enumerate(antigens):
            key = f"{ab}_vs_{ag}"
            if key in ab_data:
                hamming_matrix[i, j] = ab_data[key]['hamming_distance']
                gap_matrix[i, j] = ab_data[key]['gap_score']
                nrci_matrix[i, j] = ab_data[key]['interaction_nrci']
    
    fig, axes = plt.subplots(1, 3, figsize=(16, 5))
    fig.suptitle('Figure 5: Antibody Efficacy Matrix\nUBP Geometric Predictions vs Clinical IC50 Data', 
                 color='white', fontsize=14, fontweight='bold')
    
    cmap_h = LinearSegmentedColormap.from_list('hamming', [UBP_GREEN, UBP_GOLD, UBP_RED])
    cmap_n = LinearSegmentedColormap.from_list('nrci', [UBP_RED, UBP_GOLD, UBP_GREEN])
    
    # Hamming distance matrix
    im1 = axes[0].imshow(hamming_matrix, cmap=cmap_h, aspect='auto', vmin=0, vmax=24)
    axes[0].set_xticks(range(3))
    axes[0].set_xticklabels(['WT', 'Delta', 'Omicron'], fontsize=10)
    axes[0].set_yticks(range(2))
    axes[0].set_yticklabels(antibodies, fontsize=10)
    axes[0].set_title('Hamming Distance\n(lower = more similar = higher affinity)', color=UBP_CYAN)
    for i in range(2):
        for j in range(3):
            axes[0].text(j, i, f'd={int(hamming_matrix[i,j])}', ha='center', va='center', 
                        fontsize=14, color='white', fontweight='bold')
    plt.colorbar(im1, ax=axes[0]).ax.yaxis.set_tick_params(color='white')
    
    # Gap score matrix
    im2 = axes[1].imshow(gap_matrix, cmap=cmap_h, aspect='auto', vmin=0, vmax=12)
    axes[1].set_xticks(range(3))
    axes[1].set_xticklabels(['WT', 'Delta', 'Omicron'], fontsize=10)
    axes[1].set_yticks(range(2))
    axes[1].set_yticklabels(antibodies, fontsize=10)
    axes[1].set_title('Gap Score\n(0 = Perfect Resonance)', color=UBP_CYAN)
    for i in range(2):
        for j in range(3):
            axes[1].text(j, i, f'gap={int(gap_matrix[i,j])}', ha='center', va='center', 
                        fontsize=14, color='white', fontweight='bold')
    plt.colorbar(im2, ax=axes[1]).ax.yaxis.set_tick_params(color='white')
    
    # Clinical IC50 overlay
    ic50_data = {
        'CR3022_vs_WT': 6.3,
        'S309_vs_WT': 0.6,
        'S309_vs_Omicron': 8.2
    }
    ic50_matrix = np.full((2, 3), np.nan)
    ic50_matrix[0, 0] = 6.3  # CR3022 vs WT
    ic50_matrix[1, 0] = 0.6  # S309 vs WT
    ic50_matrix[1, 2] = 8.2  # S309 vs Omicron
    
    im3 = axes[2].imshow(ic50_matrix, cmap=cmap_h, aspect='auto', vmin=0, vmax=15)
    axes[2].set_xticks(range(3))
    axes[2].set_xticklabels(['WT', 'Delta', 'Omicron'], fontsize=10)
    axes[2].set_yticks(range(2))
    axes[2].set_yticklabels(antibodies, fontsize=10)
    axes[2].set_title('Clinical IC50 (nM)\n(lower = stronger neutralization)', color=UBP_CYAN)
    for i in range(2):
        for j in range(3):
            val = ic50_matrix[i, j]
            if not np.isnan(val):
                axes[2].text(j, i, f'{val} nM', ha='center', va='center', 
                            fontsize=13, color='white', fontweight='bold')
            else:
                axes[2].text(j, i, 'N/A', ha='center', va='center', 
                            fontsize=12, color='gray')
    plt.colorbar(im3, ax=axes[2]).ax.yaxis.set_tick_params(color='white')
    
    plt.tight_layout()
    path = f'{os_path}/fig5_antibody_matrix.png'
    plt.savefig(path, dpi=150, bbox_inches='tight', facecolor=UBP_DARK)
    plt.close()
    print(f"  Saved: {path}")
    return path

# ============================================================
# FIGURE 6: CYTOKINE STORM INTERVENTION
# ============================================================
def fig6_cytokine_storm():
    cs = report['sections']['3_cytokine_storm']
    
    states = ['Mild\nInfection', 'Cytokine\nStorm', 'Dexamethasone', 'Tocilizumab', 'Baricitinib']
    taxes = [
        cs['mild_state']['tax'],
        cs['cytokine_storm_state']['tax'],
        cs['interventions'][0]['treated_tax'],
        cs['interventions'][1]['treated_tax'],
        cs['interventions'][2]['treated_tax']
    ]
    nrcis = [
        cs['mild_state']['nrci'],
        cs['cytokine_storm_state']['nrci'],
        cs['interventions'][0]['treated_nrci'],
        cs['interventions'][1]['treated_nrci'],
        cs['interventions'][2]['treated_nrci']
    ]
    
    colors_cs = [UBP_GREEN, UBP_RED, UBP_CYAN, UBP_BLUE, UBP_PURPLE]
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    fig.suptitle('Figure 6: Cytokine Storm Modeling — UBP Geometric State Analysis\nClinical Interventions as Tax Reduction Operations', 
                 color='white', fontsize=14, fontweight='bold')
    
    bars1 = ax1.bar(states, taxes, color=colors_cs, edgecolor=UBP_CYAN, linewidth=1.5, alpha=0.9, width=0.6)
    ax1.set_title('Leech Tax per Inflammatory State\n(lower = more geometric order)', color=UBP_CYAN, fontweight='bold')
    ax1.set_ylabel('Symmetry Tax', color='white')
    for bar, val in zip(bars1, taxes):
        ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.05, f'{val:.4f}', 
                ha='center', va='bottom', fontsize=9, color='white', fontweight='bold')
    
    bars2 = ax2.bar(states, nrcis, color=colors_cs, edgecolor=UBP_CYAN, linewidth=1.5, alpha=0.9, width=0.6)
    ax2.set_title('NRCI per Inflammatory State\n(higher = more coherent)', color=UBP_CYAN, fontweight='bold')
    ax2.set_ylabel('NRCI Score', color='white')
    ax2.set_ylim(0, 1.0)
    for bar, val in zip(bars2, nrcis):
        ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01, f'{val:.4f}', 
                ha='center', va='bottom', fontsize=9, color='white', fontweight='bold')
    
    # Add clinical efficacy annotations
    clinical = ['Baseline', 'Severe COVID-19', '28% mortality\nreduction', '12% mortality\nreduction', '38% mortality\nreduction']
    for i, (ax, bars) in enumerate([(ax1, bars1), (ax2, bars2)]):
        for j, (bar, label) in enumerate(zip(bars, clinical)):
            ax.text(bar.get_x() + bar.get_width()/2, 0.3, label, 
                   ha='center', va='bottom', fontsize=6, color=UBP_GOLD, rotation=90, alpha=0.8)
    
    plt.tight_layout()
    path = f'{os_path}/fig6_cytokine_storm.png'
    plt.savefig(path, dpi=150, bbox_inches='tight', facecolor=UBP_DARK)
    plt.close()
    print(f"  Saved: {path}")
    return path

# ============================================================
# FIGURE 7: TILT POLAR PLOT
# ============================================================
def fig7_tilt_polar():
    entries = list(kb.values())
    
    fig, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(polar=True))
    fig.suptitle('Figure 7: UBP Tilt Angles — Alignment to Universal North\nAll 12 Viral Proteins on the Geometric Sphere', 
                 color='white', fontsize=14, fontweight='bold')
    ax.set_facecolor(UBP_DARK)
    
    colors_p = {
        'SARS_COV2': UBP_BLUE,
        'OMICRON': UBP_RED,
        'DELTA': UBP_ORANGE,
        'ANTIBODY': UBP_GREEN,
        'HOST': UBP_CYAN,
        'INFLUENZA': UBP_PURPLE,
        'HIV': UBP_GOLD,
    }
    
    for entry in entries:
        tilt = entry['atlas']['tilt']
        nrci = entry['atlas']['nrci_score']
        tags = entry.get('tags', [])
        name = entry['ubp_id'].replace('PROTEIN_', '').replace('_001', '')
        
        # Determine color
        color = UBP_BLUE
        for k, v in colors_p.items():
            if k in entry['ubp_id']:
                color = v
                break
        
        # Plot: theta = tilt angle in radians, r = NRCI
        theta = math.radians(tilt)
        r = nrci
        
        ax.scatter(theta, r, s=200, color=color, alpha=0.9, zorder=5, edgecolors='white', linewidths=1)
        
        # Short label
        short = name.split('_')[-2] if len(name.split('_')) > 2 else name
        ax.annotate(short[:10], (theta, r), textcoords='offset points', 
                   xytext=(5, 5), fontsize=7, color='white', alpha=0.9)
    
    # Universal North marker
    ax.scatter(0, 1.0, s=400, color=UBP_GOLD, marker='*', zorder=10, label='Universal North')
    ax.text(0.1, 0.95, 'Universal\nNorth', color=UBP_GOLD, fontsize=9, fontweight='bold')
    
    ax.set_rticks([0.2, 0.4, 0.6, 0.8, 1.0])
    ax.set_rlabel_position(45)
    ax.tick_params(colors='white')
    ax.set_title('r = NRCI, θ = Tilt from Universal North', color=UBP_CYAN, pad=20)
    
    # Legend
    legend_patches = [
        mpatches.Patch(color=UBP_BLUE, label='SARS-CoV-2 WT'),
        mpatches.Patch(color=UBP_RED, label='Omicron'),
        mpatches.Patch(color=UBP_ORANGE, label='Delta'),
        mpatches.Patch(color=UBP_GREEN, label='Antibodies'),
        mpatches.Patch(color=UBP_CYAN, label='ACE2 (Host)'),
        mpatches.Patch(color=UBP_PURPLE, label='Influenza HA'),
        mpatches.Patch(color=UBP_GOLD, label='HIV gp120'),
    ]
    ax.legend(handles=legend_patches, facecolor=UBP_DARK, edgecolor=UBP_CYAN, labelcolor='white', 
             loc='lower right', bbox_to_anchor=(1.3, 0.0))
    
    plt.tight_layout()
    path = f'{os_path}/fig7_tilt_polar.png'
    plt.savefig(path, dpi=150, bbox_inches='tight', facecolor=UBP_DARK)
    plt.close()
    print(f"  Saved: {path}")
    return path

# ============================================================
# FIGURE 8: VALIDATION SUMMARY
# ============================================================
def fig8_validation_summary():
    validations = validation['validations']
    
    fig, ax = plt.subplots(figsize=(14, 8))
    fig.suptitle('Figure 8: UBP Clinical Validation Summary\nUBP Geometric Predictions vs Known Experimental Data', 
                 color='white', fontsize=14, fontweight='bold')
    
    ax.set_xlim(0, 10)
    ax.set_ylim(0, len(validations) + 1)
    ax.axis('off')
    
    result_colors = {
        'CONFIRMED': UBP_GREEN,
        'REFUTED': UBP_RED,
        'PARTIAL': UBP_ORANGE,
        'INFORMATIONAL': UBP_CYAN,
        'NOVEL_PREDICTION': UBP_GOLD
    }
    
    for i, v in enumerate(reversed(validations)):
        y = i + 0.5
        color = result_colors.get(v['result'], UBP_BLUE)
        
        # Result badge
        ax.add_patch(mpatches.FancyBboxPatch((0, y - 0.3), 1.8, 0.6, 
                                              boxstyle="round,pad=0.1", 
                                              facecolor=color, edgecolor='white', alpha=0.9))
        ax.text(0.9, y, v['result'], ha='center', va='center', 
               fontsize=9, color='white', fontweight='bold')
        
        # Validation name
        ax.text(2.1, y + 0.1, v['validation'], ha='left', va='center', 
               fontsize=10, color='white', fontweight='bold')
        
        # Interpretation (truncated)
        interp = v['interpretation'][:100] + '...' if len(v['interpretation']) > 100 else v['interpretation']
        ax.text(2.1, y - 0.2, interp, ha='left', va='center', 
               fontsize=8, color=UBP_LIGHT, alpha=0.85)
        
        # Separator
        ax.axhline(y=y + 0.4, xmin=0.02, xmax=0.98, color=UBP_BLUE, alpha=0.5, linewidth=0.5)
    
    # Summary stats
    confirmed = validation['validation_summary']['confirmed']
    total = validation['validation_summary']['total_checkable']
    ax.text(5, len(validations) + 0.7, 
           f'Confirmed: {confirmed}/{total} ({validation["validation_summary"]["accuracy_pct"]}%)', 
           ha='center', va='center', fontsize=14, color=UBP_GREEN, fontweight='bold')
    
    plt.tight_layout()
    path = f'{os_path}/fig8_validation_summary.png'
    plt.savefig(path, dpi=150, bbox_inches='tight', facecolor=UBP_DARK)
    plt.close()
    print(f"  Saved: {path}")
    return path

# ============================================================
# MAIN
# ============================================================
if __name__ == "__main__":
    print("Generating UBP Virology Figures...")
    print("=" * 50)
    
    paths = []
    paths.append(fig1_nrci_landscape())
    paths.append(fig2_variant_evolution())
    paths.append(fig3_vector_heatmap())
    paths.append(fig4_energy_landscape())
    paths.append(fig5_antibody_matrix())
    paths.append(fig6_cytokine_storm())
    paths.append(fig7_tilt_polar())
    paths.append(fig8_validation_summary())
    
    print(f"\nAll {len(paths)} figures saved to: {os_path}/")
    print("Done!")
