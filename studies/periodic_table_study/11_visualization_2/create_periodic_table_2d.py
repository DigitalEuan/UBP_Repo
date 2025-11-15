#!/usr/bin/env python3.11
"""
2D Periodic Table Visualization with All 172 Elements

Creates a traditional periodic table layout showing all 118 known elements
plus 54 predicted elements (Z=119-172) in their proper positions.
"""

import sys
sys.path.insert(0, '/home/ubuntu/periodic_table_hexdictionary')

from periodic_table_data import get_all_elements
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import matplotlib.patches as mpatches

def get_element_position(z):
    """
    Get the (period, group) position for an element.
    Returns (row, col) for plotting.
    """
    # Standard periodic table positions for Z=1-118
    positions = {
        # Period 1
        1: (1, 1),    # H
        2: (1, 18),   # He
        
        # Period 2
        3: (2, 1), 4: (2, 2),                                           # Li, Be
        5: (2, 13), 6: (2, 14), 7: (2, 15), 8: (2, 16), 9: (2, 17), 10: (2, 18),  # B-Ne
        
        # Period 3
        11: (3, 1), 12: (3, 2),                                         # Na, Mg
        13: (3, 13), 14: (3, 14), 15: (3, 15), 16: (3, 16), 17: (3, 17), 18: (3, 18),  # Al-Ar
        
        # Period 4
        19: (4, 1), 20: (4, 2),                                         # K, Ca
        21: (4, 3), 22: (4, 4), 23: (4, 5), 24: (4, 6), 25: (4, 7),    # Sc-Mn
        26: (4, 8), 27: (4, 9), 28: (4, 10), 29: (4, 11), 30: (4, 12), # Fe-Zn
        31: (4, 13), 32: (4, 14), 33: (4, 15), 34: (4, 16), 35: (4, 17), 36: (4, 18),  # Ga-Kr
        
        # Period 5
        37: (5, 1), 38: (5, 2),                                         # Rb, Sr
        39: (5, 3), 40: (5, 4), 41: (5, 5), 42: (5, 6), 43: (5, 7),    # Y-Tc
        44: (5, 8), 45: (5, 9), 46: (5, 10), 47: (5, 11), 48: (5, 12), # Ru-Cd
        49: (5, 13), 50: (5, 14), 51: (5, 15), 52: (5, 16), 53: (5, 17), 54: (5, 18),  # In-Xe
        
        # Period 6
        55: (6, 1), 56: (6, 2),                                         # Cs, Ba
        57: (6, 3),                                                     # La (placeholder)
        72: (6, 4), 73: (6, 5), 74: (6, 6), 75: (6, 7), 76: (6, 8),    # Hf-Os
        77: (6, 9), 78: (6, 10), 79: (6, 11), 80: (6, 12),             # Ir-Hg
        81: (6, 13), 82: (6, 14), 83: (6, 15), 84: (6, 16), 85: (6, 17), 86: (6, 18),  # Tl-Rn
        
        # Period 7
        87: (7, 1), 88: (7, 2),                                         # Fr, Ra
        89: (7, 3),                                                     # Ac (placeholder)
        104: (7, 4), 105: (7, 5), 106: (7, 6), 107: (7, 7), 108: (7, 8),  # Rf-Hs
        109: (7, 9), 110: (7, 10), 111: (7, 11), 112: (7, 12),         # Mt-Cn
        113: (7, 13), 114: (7, 14), 115: (7, 15), 116: (7, 16), 117: (7, 17), 118: (7, 18),  # Nh-Og
        
        # Lanthanides (Period 6, f-block) - displayed separately
        57: (9, 3), 58: (9, 4), 59: (9, 5), 60: (9, 6), 61: (9, 7), 62: (9, 8),  # La-Sm
        63: (9, 9), 64: (9, 10), 65: (9, 11), 66: (9, 12), 67: (9, 13), 68: (9, 14),  # Eu-Er
        69: (9, 15), 70: (9, 16), 71: (9, 17),  # Tm-Lu
        
        # Actinides (Period 7, f-block) - displayed separately
        89: (10, 3), 90: (10, 4), 91: (10, 5), 92: (10, 6), 93: (10, 7), 94: (10, 8),  # Ac-Cm
        95: (10, 9), 96: (10, 10), 97: (10, 11), 98: (10, 12), 99: (10, 13), 100: (10, 14),  # Am-Fm
        101: (10, 15), 102: (10, 16), 103: (10, 17),  # Md-Lr
    }
    
    # Predicted elements (Z=119-172) - extend period 8, 9, 10
    if z >= 119:
        # Period 8: Z=119-168 (50 elements)
        if z <= 168:
            period = 8
            if z <= 120:  # s-block
                col = z - 118
            elif z <= 138:  # f-block (superactinides) - separate row
                return (11, z - 120 + 3)  # Row 11 for superactinides
            elif z <= 148:  # d-block
                col = z - 138 + 3
            else:  # p-block
                col = z - 148 + 13
            return (period, col)
        # Period 9: Z=169-172 (partial)
        else:
            period = 9
            col = z - 168
            return (period, col)
    
    return positions.get(z, (0, 0))

def get_element_color(z, elements):
    """
    Get color for element based on its block.
    """
    symbol, name, config = elements[z]
    
    # Determine block from last orbital
    last_orbital = config[-1] if config else ""
    
    if z <= 118:
        # Known elements
        if 's' in last_orbital:
            return '#FFB6C1'  # Light pink - s-block
        elif 'p' in last_orbital:
            return '#87CEEB'  # Sky blue - p-block
        elif 'd' in last_orbital:
            return '#FFD700'  # Gold - d-block
        elif 'f' in last_orbital:
            return '#98FB98'  # Pale green - f-block
        else:
            return '#D3D3D3'  # Light gray - unknown
    else:
        # Predicted elements
        if z <= 120:
            return '#FFE4E1'  # Misty rose - predicted s-block
        elif z <= 138:
            return '#E0FFE0'  # Light green - predicted f-block (superactinides)
        elif z <= 148:
            return '#FFF8DC'  # Cornsilk - predicted d-block
        else:
            return '#E6F3FF'  # Light blue - predicted p-block

def create_2d_periodic_table():
    """
    Create a traditional 2D periodic table with all 172 elements.
    """
    print("\nCreating 2D periodic table with 172 elements...")
    
    elements = get_all_elements()
    
    # Create figure
    fig, ax = plt.subplots(figsize=(24, 16))
    ax.set_xlim(0, 19)
    ax.set_ylim(0, 12)
    ax.set_aspect('equal')
    ax.axis('off')
    
    # Title
    ax.text(9.5, 11.5, 'Extended Periodic Table of Elements (Z=1-172)', 
            ha='center', va='top', fontsize=20, fontweight='bold')
    ax.text(9.5, 11.0, '118 Known + 54 Predicted Elements', 
            ha='center', va='top', fontsize=14, style='italic')
    
    # Draw elements
    for z in range(1, 173):
        if z not in elements:
            continue
        
        symbol, name, config = elements[z]
        row, col = get_element_position(z)
        
        if row == 0:  # Skip if position not defined
            continue
        
        # Convert to plot coordinates (invert y-axis)
        x = col - 0.5
        y = 12 - row - 0.5
        
        # Get color
        color = get_element_color(z, elements)
        
        # Draw box
        rect = Rectangle((x, y), 0.9, 0.9, 
                         facecolor=color, edgecolor='black', linewidth=1)
        ax.add_patch(rect)
        
        # Add text
        # Atomic number (top)
        ax.text(x + 0.45, y + 0.75, str(z), 
               ha='center', va='center', fontsize=6, fontweight='bold')
        
        # Symbol (center)
        ax.text(x + 0.45, y + 0.45, symbol, 
               ha='center', va='center', fontsize=10, fontweight='bold')
        
        # Name (bottom)
        name_short = name[:8] if len(name) > 8 else name
        ax.text(x + 0.45, y + 0.15, name_short, 
               ha='center', va='center', fontsize=5)
        
        # Mark predicted elements with asterisk
        if z > 118:
            ax.text(x + 0.85, y + 0.85, '*', 
                   ha='center', va='center', fontsize=8, color='red', fontweight='bold')
    
    # Add legend
    legend_elements = [
        mpatches.Patch(facecolor='#FFB6C1', edgecolor='black', label='s-block (known)'),
        mpatches.Patch(facecolor='#87CEEB', edgecolor='black', label='p-block (known)'),
        mpatches.Patch(facecolor='#FFD700', edgecolor='black', label='d-block (known)'),
        mpatches.Patch(facecolor='#98FB98', edgecolor='black', label='f-block (known)'),
        mpatches.Patch(facecolor='#FFE4E1', edgecolor='black', label='s-block (predicted)'),
        mpatches.Patch(facecolor='#E0FFE0', edgecolor='black', label='f-block (predicted)'),
        mpatches.Patch(facecolor='#FFF8DC', edgecolor='black', label='d-block (predicted)'),
        mpatches.Patch(facecolor='#E6F3FF', edgecolor='black', label='p-block (predicted)'),
    ]
    ax.legend(handles=legend_elements, loc='upper left', fontsize=10, 
             bbox_to_anchor=(0, 0.95), framealpha=0.9)
    
    # Add labels for special rows
    ax.text(0.5, 12 - 9 - 0.5, 'Lanthanides', ha='right', va='center', 
           fontsize=10, fontweight='bold', style='italic')
    ax.text(0.5, 12 - 10 - 0.5, 'Actinides', ha='right', va='center', 
           fontsize=10, fontweight='bold', style='italic')
    ax.text(0.5, 12 - 11 - 0.5, 'Superactinides*', ha='right', va='center', 
           fontsize=10, fontweight='bold', style='italic', color='red')
    
    # Add note
    ax.text(9.5, 0.2, '* Predicted elements (Z=119-172) based on electron configuration extrapolation', 
           ha='center', va='bottom', fontsize=8, style='italic')
    
    plt.tight_layout()
    plt.savefig('/home/ubuntu/FINAL_DELIVERABLES/periodic_table_2d_full.png', 
               dpi=300, bbox_inches='tight', facecolor='white')
    print("✓ 2D periodic table saved to: periodic_table_2d_full.png")

def main():
    print("\n" + "="*80)
    print("2D PERIODIC TABLE GENERATOR")
    print("="*80)
    
    create_2d_periodic_table()
    
    print("\n" + "="*80)
    print("✓ Visualization complete!")
    print("="*80)

if __name__ == "__main__":
    main()
