#!/usr/bin/env python3.11
"""
3D Periodic Table Visualization

Creates a 3D scatter plot of all 172 elements positioned by:
- X-axis: Atomic Number (Z)
- Y-axis: Period
- Z-axis: Group

Color-coded by block (s, p, d, f) and size by number of electrons.
"""

import sys
sys.path.insert(0, '/home/ubuntu/periodic_table_hexdictionary')

from periodic_table_data import get_all_elements
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

def get_period(z):
    """Get period number for element Z."""
    if z <= 2: return 1
    elif z <= 10: return 2
    elif z <= 18: return 3
    elif z <= 36: return 4
    elif z <= 54: return 5
    elif z <= 86: return 6
    elif z <= 118: return 7
    elif z <= 168: return 8
    else: return 9

def get_group(z):
    """Get group number for element Z (1-18)."""
    # Simplified group assignment
    groups = {
        1: 1, 2: 18,  # H, He
        3: 1, 4: 2, 5: 13, 6: 14, 7: 15, 8: 16, 9: 17, 10: 18,  # Period 2
        11: 1, 12: 2, 13: 13, 14: 14, 15: 15, 16: 16, 17: 17, 18: 18,  # Period 3
    }
    
    if z in groups:
        return groups[z]
    
    # For transition metals and beyond, use modular arithmetic
    period = get_period(z)
    
    if period == 4:
        if z <= 20: return z - 18
        elif z <= 30: return z - 18  # d-block
        else: return z - 18
    elif period == 5:
        if z <= 38: return z - 36
        elif z <= 48: return z - 36
        else: return z - 36
    elif period == 6:
        if z <= 56: return z - 54
        elif z <= 71: return 3  # Lanthanides (f-block)
        elif z <= 80: return z - 68
        else: return z - 68
    elif period == 7:
        if z <= 88: return z - 86
        elif z <= 103: return 3  # Actinides (f-block)
        elif z <= 112: return z - 100
        else: return z - 100
    elif period == 8:
        if z <= 120: return z - 118
        elif z <= 138: return 3  # Superactinides (f-block)
        elif z <= 148: return z - 135
        else: return z - 135
    else:
        return z - 168

def get_block(z, elements):
    """Determine block (s, p, d, f) for element Z."""
    if z not in elements:
        return 's'
    
    symbol, name, config = elements[z]
    if not config:
        return 's'
    
    last_orbital = config[-1]
    if 's' in last_orbital:
        return 's'
    elif 'p' in last_orbital:
        return 'p'
    elif 'd' in last_orbital:
        return 'd'
    elif 'f' in last_orbital:
        return 'f'
    else:
        return 's'

def create_3d_periodic_table():
    """
    Create a 3D visualization of the periodic table.
    """
    print("\nCreating 3D periodic table visualization...")
    
    elements = get_all_elements()
    
    # Prepare data
    z_values = []
    periods = []
    groups = []
    blocks = []
    sizes = []
    labels = []
    
    for z in range(1, 173):
        if z not in elements:
            continue
        
        symbol, name, config = elements[z]
        
        z_values.append(z)
        periods.append(get_period(z))
        groups.append(get_group(z))
        blocks.append(get_block(z, elements))
        sizes.append(z * 2)  # Size proportional to atomic number
        labels.append(symbol)
    
    # Convert to numpy arrays
    z_values = np.array(z_values)
    periods = np.array(periods)
    groups = np.array(groups)
    
    # Create figure
    fig = plt.figure(figsize=(20, 16))
    ax = fig.add_subplot(111, projection='3d')
    
    # Color mapping
    color_map = {
        's': '#FFB6C1',  # Pink
        'p': '#87CEEB',  # Sky blue
        'd': '#FFD700',  # Gold
        'f': '#98FB98',  # Pale green
    }
    
    colors = [color_map.get(b, '#D3D3D3') for b in blocks]
    
    # Create scatter plot
    scatter = ax.scatter(z_values, periods, groups, 
                        c=colors, s=sizes, alpha=0.7, edgecolors='black', linewidth=0.5)
    
    # Add labels for selected elements
    label_elements = [1, 2, 6, 8, 26, 79, 92, 118, 119, 172]  # H, He, C, O, Fe, Au, U, Og, 119, 172
    for i, z in enumerate(z_values):
        if z in label_elements:
            ax.text(z, periods[i], groups[i], f'  {labels[i]}', 
                   fontsize=8, fontweight='bold')
    
    # Set labels
    ax.set_xlabel('Atomic Number (Z)', fontsize=12, fontweight='bold')
    ax.set_ylabel('Period', fontsize=12, fontweight='bold')
    ax.set_zlabel('Group', fontsize=12, fontweight='bold')
    ax.set_title('3D Periodic Table: 172 Elements in Property Space\n(118 Known + 54 Predicted)', 
                fontsize=16, fontweight='bold', pad=20)
    
    # Set axis limits
    ax.set_xlim(0, 180)
    ax.set_ylim(0, 10)
    ax.set_zlim(0, 20)
    
    # Add legend
    from matplotlib.patches import Patch
    legend_elements = [
        Patch(facecolor='#FFB6C1', edgecolor='black', label='s-block'),
        Patch(facecolor='#87CEEB', edgecolor='black', label='p-block'),
        Patch(facecolor='#FFD700', edgecolor='black', label='d-block'),
        Patch(facecolor='#98FB98', edgecolor='black', label='f-block'),
    ]
    ax.legend(handles=legend_elements, loc='upper left', fontsize=10)
    
    # Adjust viewing angle
    ax.view_init(elev=20, azim=45)
    
    plt.tight_layout()
    plt.savefig('/home/ubuntu/FINAL_DELIVERABLES/periodic_table_3d.png', 
               dpi=300, bbox_inches='tight', facecolor='white')
    print("✓ 3D periodic table saved to: periodic_table_3d.png")
    
    # Create a second view from different angle
    ax.view_init(elev=30, azim=135)
    plt.savefig('/home/ubuntu/FINAL_DELIVERABLES/periodic_table_3d_alt_view.png', 
               dpi=300, bbox_inches='tight', facecolor='white')
    print("✓ Alternative 3D view saved to: periodic_table_3d_alt_view.png")

def create_3d_jaccard_space():
    """
    Create a 3D visualization based on Jaccard distance clustering.
    """
    print("\nCreating 3D Jaccard distance space visualization...")
    
    elements = get_all_elements()
    
    # We'll use PCA-like projection based on orbital sets
    # For simplicity, use: X = # of s-orbitals, Y = # of p-orbitals, Z = # of d-orbitals
    
    z_values = []
    s_count = []
    p_count = []
    d_count = []
    blocks = []
    labels = []
    
    for z in range(1, 173):
        if z not in elements:
            continue
        
        symbol, name, config = elements[z]
        
        # Count orbital types
        s_orbs = sum(1 for orb in config if 's' in orb)
        p_orbs = sum(1 for orb in config if 'p' in orb)
        d_orbs = sum(1 for orb in config if 'd' in orb)
        
        z_values.append(z)
        s_count.append(s_orbs)
        p_count.append(p_orbs)
        d_count.append(d_orbs)
        blocks.append(get_block(z, elements))
        labels.append(symbol)
    
    # Convert to numpy arrays
    z_values = np.array(z_values)
    s_count = np.array(s_count)
    p_count = np.array(p_count)
    d_count = np.array(d_count)
    
    # Create figure
    fig = plt.figure(figsize=(20, 16))
    ax = fig.add_subplot(111, projection='3d')
    
    # Color mapping
    color_map = {
        's': '#FFB6C1',  # Pink
        'p': '#87CEEB',  # Sky blue
        'd': '#FFD700',  # Gold
        'f': '#98FB98',  # Pale green
    }
    
    colors = [color_map.get(b, '#D3D3D3') for b in blocks]
    sizes = z_values * 2
    
    # Create scatter plot
    scatter = ax.scatter(s_count, p_count, d_count, 
                        c=colors, s=sizes, alpha=0.7, edgecolors='black', linewidth=0.5)
    
    # Add labels for selected elements
    label_elements = [1, 2, 6, 8, 10, 18, 26, 36, 54, 79, 86, 92, 118, 119, 172]
    for i, z in enumerate(z_values):
        if z in label_elements:
            ax.text(s_count[i], p_count[i], d_count[i], f'  {labels[i]}', 
                   fontsize=8, fontweight='bold')
    
    # Set labels
    ax.set_xlabel('Number of s-orbitals', fontsize=12, fontweight='bold')
    ax.set_ylabel('Number of p-orbitals', fontsize=12, fontweight='bold')
    ax.set_zlabel('Number of d-orbitals', fontsize=12, fontweight='bold')
    ax.set_title('3D Orbital Space: Elements Positioned by Toggle Sets\n(Jaccard Distance Geometry)', 
                fontsize=16, fontweight='bold', pad=20)
    
    # Add legend
    from matplotlib.patches import Patch
    legend_elements = [
        Patch(facecolor='#FFB6C1', edgecolor='black', label='s-block'),
        Patch(facecolor='#87CEEB', edgecolor='black', label='p-block'),
        Patch(facecolor='#FFD700', edgecolor='black', label='d-block'),
        Patch(facecolor='#98FB98', edgecolor='black', label='f-block'),
    ]
    ax.legend(handles=legend_elements, loc='upper left', fontsize=10)
    
    # Adjust viewing angle
    ax.view_init(elev=20, azim=45)
    
    plt.tight_layout()
    plt.savefig('/home/ubuntu/FINAL_DELIVERABLES/periodic_table_3d_jaccard_space.png', 
               dpi=300, bbox_inches='tight', facecolor='white')
    print("✓ 3D Jaccard space saved to: periodic_table_3d_jaccard_space.png")
    
    # Alternative view
    ax.view_init(elev=30, azim=135)
    plt.savefig('/home/ubuntu/FINAL_DELIVERABLES/periodic_table_3d_jaccard_space_alt.png', 
               dpi=300, bbox_inches='tight', facecolor='white')
    print("✓ Alternative Jaccard space view saved to: periodic_table_3d_jaccard_space_alt.png")

def main():
    print("\n" + "="*80)
    print("3D PERIODIC TABLE GENERATOR")
    print("="*80)
    
    create_3d_periodic_table()
    create_3d_jaccard_space()
    
    print("\n" + "="*80)
    print("✓ All 3D visualizations complete!")
    print("="*80)
    print("\nGenerated files:")
    print("  1. periodic_table_3d.png (Property space)")
    print("  2. periodic_table_3d_alt_view.png (Property space, alt angle)")
    print("  3. periodic_table_3d_jaccard_space.png (Orbital toggle space)")
    print("  4. periodic_table_3d_jaccard_space_alt.png (Orbital toggle space, alt angle)")

if __name__ == "__main__":
    main()
