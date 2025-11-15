"""
================================================================================
Periodic Table Visualization with Predicted Elements (Z=119-126)
================================================================================

Creates a comprehensive periodic table visualization showing:
- All 118 known elements
- 8 predicted superheavy elements (Z=119-126)
- Color-coded by element type
- Includes atomic number, symbol, and name

Author: Euan Craig, New Zealand
Date: November 15, 2025
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import json

# Load predictions
with open('../results/superheavy_predictions.json', 'r') as f:
    predictions = json.load(f)

# Element data (118 known + 8 predicted)
# Format: Z: (Symbol, Name, Group, Period, Type)
elements = {
    # Period 1
    1: ('H', 'Hydrogen', 1, 1, 'nonmetal'),
    2: ('He', 'Helium', 18, 1, 'noble_gas'),
    
    # Period 2
    3: ('Li', 'Lithium', 1, 2, 'alkali'),
    4: ('Be', 'Beryllium', 2, 2, 'alkaline_earth'),
    5: ('B', 'Boron', 13, 2, 'metalloid'),
    6: ('C', 'Carbon', 14, 2, 'nonmetal'),
    7: ('N', 'Nitrogen', 15, 2, 'nonmetal'),
    8: ('O', 'Oxygen', 16, 2, 'nonmetal'),
    9: ('F', 'Fluorine', 17, 2, 'halogen'),
    10: ('Ne', 'Neon', 18, 2, 'noble_gas'),
    
    # Period 3
    11: ('Na', 'Sodium', 1, 3, 'alkali'),
    12: ('Mg', 'Magnesium', 2, 3, 'alkaline_earth'),
    13: ('Al', 'Aluminum', 13, 3, 'post_transition'),
    14: ('Si', 'Silicon', 14, 3, 'metalloid'),
    15: ('P', 'Phosphorus', 15, 3, 'nonmetal'),
    16: ('S', 'Sulfur', 16, 3, 'nonmetal'),
    17: ('Cl', 'Chlorine', 17, 3, 'halogen'),
    18: ('Ar', 'Argon', 18, 3, 'noble_gas'),
    
    # Period 4
    19: ('K', 'Potassium', 1, 4, 'alkali'),
    20: ('Ca', 'Calcium', 2, 4, 'alkaline_earth'),
    21: ('Sc', 'Scandium', 3, 4, 'transition'),
    22: ('Ti', 'Titanium', 4, 4, 'transition'),
    23: ('V', 'Vanadium', 5, 4, 'transition'),
    24: ('Cr', 'Chromium', 6, 4, 'transition'),
    25: ('Mn', 'Manganese', 7, 4, 'transition'),
    26: ('Fe', 'Iron', 8, 4, 'transition'),
    27: ('Co', 'Cobalt', 9, 4, 'transition'),
    28: ('Ni', 'Nickel', 10, 4, 'transition'),
    29: ('Cu', 'Copper', 11, 4, 'transition'),
    30: ('Zn', 'Zinc', 12, 4, 'transition'),
    31: ('Ga', 'Gallium', 13, 4, 'post_transition'),
    32: ('Ge', 'Germanium', 14, 4, 'metalloid'),
    33: ('As', 'Arsenic', 15, 4, 'metalloid'),
    34: ('Se', 'Selenium', 16, 4, 'nonmetal'),
    35: ('Br', 'Bromine', 17, 4, 'halogen'),
    36: ('Kr', 'Krypton', 18, 4, 'noble_gas'),
    
    # Period 5
    37: ('Rb', 'Rubidium', 1, 5, 'alkali'),
    38: ('Sr', 'Strontium', 2, 5, 'alkaline_earth'),
    39: ('Y', 'Yttrium', 3, 5, 'transition'),
    40: ('Zr', 'Zirconium', 4, 5, 'transition'),
    41: ('Nb', 'Niobium', 5, 5, 'transition'),
    42: ('Mo', 'Molybdenum', 6, 5, 'transition'),
    43: ('Tc', 'Technetium', 7, 5, 'transition'),
    44: ('Ru', 'Ruthenium', 8, 5, 'transition'),
    45: ('Rh', 'Rhodium', 9, 5, 'transition'),
    46: ('Pd', 'Palladium', 10, 5, 'transition'),
    47: ('Ag', 'Silver', 11, 5, 'transition'),
    48: ('Cd', 'Cadmium', 12, 5, 'transition'),
    49: ('In', 'Indium', 13, 5, 'post_transition'),
    50: ('Sn', 'Tin', 14, 5, 'post_transition'),
    51: ('Sb', 'Antimony', 15, 5, 'metalloid'),
    52: ('Te', 'Tellurium', 16, 5, 'metalloid'),
    53: ('I', 'Iodine', 17, 5, 'halogen'),
    54: ('Xe', 'Xenon', 18, 5, 'noble_gas'),
    
    # Period 6
    55: ('Cs', 'Cesium', 1, 6, 'alkali'),
    56: ('Ba', 'Barium', 2, 6, 'alkaline_earth'),
    57: ('La', 'Lanthanum', 3, 6, 'lanthanide'),  # Start lanthanides
    72: ('Hf', 'Hafnium', 4, 6, 'transition'),
    73: ('Ta', 'Tantalum', 5, 6, 'transition'),
    74: ('W', 'Tungsten', 6, 6, 'transition'),
    75: ('Re', 'Rhenium', 7, 6, 'transition'),
    76: ('Os', 'Osmium', 8, 6, 'transition'),
    77: ('Ir', 'Iridium', 9, 6, 'transition'),
    78: ('Pt', 'Platinum', 10, 6, 'transition'),
    79: ('Au', 'Gold', 11, 6, 'transition'),
    80: ('Hg', 'Mercury', 12, 6, 'transition'),
    81: ('Tl', 'Thallium', 13, 6, 'post_transition'),
    82: ('Pb', 'Lead', 14, 6, 'post_transition'),
    83: ('Bi', 'Bismuth', 15, 6, 'post_transition'),
    84: ('Po', 'Polonium', 16, 6, 'post_transition'),
    85: ('At', 'Astatine', 17, 6, 'halogen'),
    86: ('Rn', 'Radon', 18, 6, 'noble_gas'),
    
    # Period 7
    87: ('Fr', 'Francium', 1, 7, 'alkali'),
    88: ('Ra', 'Radium', 2, 7, 'alkaline_earth'),
    89: ('Ac', 'Actinium', 3, 7, 'actinide'),  # Start actinides
    104: ('Rf', 'Rutherfordium', 4, 7, 'transition'),
    105: ('Db', 'Dubnium', 5, 7, 'transition'),
    106: ('Sg', 'Seaborgium', 6, 7, 'transition'),
    107: ('Bh', 'Bohrium', 7, 7, 'transition'),
    108: ('Hs', 'Hassium', 8, 7, 'transition'),
    109: ('Mt', 'Meitnerium', 9, 7, 'transition'),
    110: ('Ds', 'Darmstadtium', 10, 7, 'transition'),
    111: ('Rg', 'Roentgenium', 11, 7, 'transition'),
    112: ('Cn', 'Copernicium', 12, 7, 'transition'),
    113: ('Nh', 'Nihonium', 13, 7, 'post_transition'),
    114: ('Fl', 'Flerovium', 14, 7, 'post_transition'),
    115: ('Mc', 'Moscovium', 15, 7, 'post_transition'),
    116: ('Lv', 'Livermorium', 16, 7, 'post_transition'),
    117: ('Ts', 'Tennessine', 17, 7, 'halogen'),
    118: ('Og', 'Oganesson', 18, 7, 'noble_gas'),
    
    # Lanthanides (Period 6, separate row)
    58: ('Ce', 'Cerium', 3, 8.5, 'lanthanide'),
    59: ('Pr', 'Praseodymium', 3, 8.5, 'lanthanide'),
    60: ('Nd', 'Neodymium', 3, 8.5, 'lanthanide'),
    61: ('Pm', 'Promethium', 3, 8.5, 'lanthanide'),
    62: ('Sm', 'Samarium', 3, 8.5, 'lanthanide'),
    63: ('Eu', 'Europium', 3, 8.5, 'lanthanide'),
    64: ('Gd', 'Gadolinium', 3, 8.5, 'lanthanide'),
    65: ('Tb', 'Terbium', 3, 8.5, 'lanthanide'),
    66: ('Dy', 'Dysprosium', 3, 8.5, 'lanthanide'),
    67: ('Ho', 'Holmium', 3, 8.5, 'lanthanide'),
    68: ('Er', 'Erbium', 3, 8.5, 'lanthanide'),
    69: ('Tm', 'Thulium', 3, 8.5, 'lanthanide'),
    70: ('Yb', 'Ytterbium', 3, 8.5, 'lanthanide'),
    71: ('Lu', 'Lutetium', 3, 8.5, 'lanthanide'),
    
    # Actinides (Period 7, separate row)
    90: ('Th', 'Thorium', 3, 9.5, 'actinide'),
    91: ('Pa', 'Protactinium', 3, 9.5, 'actinide'),
    92: ('U', 'Uranium', 3, 9.5, 'actinide'),
    93: ('Np', 'Neptunium', 3, 9.5, 'actinide'),
    94: ('Pu', 'Plutonium', 3, 9.5, 'actinide'),
    95: ('Am', 'Americium', 3, 9.5, 'actinide'),
    96: ('Cm', 'Curium', 3, 9.5, 'actinide'),
    97: ('Bk', 'Berkelium', 3, 9.5, 'actinide'),
    98: ('Cf', 'Californium', 3, 9.5, 'actinide'),
    99: ('Es', 'Einsteinium', 3, 9.5, 'actinide'),
    100: ('Fm', 'Fermium', 3, 9.5, 'actinide'),
    101: ('Md', 'Mendelevium', 3, 9.5, 'actinide'),
    102: ('No', 'Nobelium', 3, 9.5, 'actinide'),
    103: ('Lr', 'Lawrencium', 3, 9.5, 'actinide'),
    
    # PREDICTED ELEMENTS (Period 8)
    119: ('Uue', 'Ununennium', 1, 8, 'predicted_alkali'),
    120: ('Ubn', 'Unbinilium', 2, 8, 'predicted_alkaline'),
    121: ('Ubu', 'Unbiunium', 3, 8, 'predicted_superactinide'),
    122: ('Ubb', 'Unbibium', 4, 8, 'predicted_transition'),
    123: ('Ubt', 'Unbitrium', 5, 8, 'predicted_transition'),
    124: ('Ubq', 'Unbiquadium', 6, 8, 'predicted_transition'),
    125: ('Ubp', 'Unbipentium', 7, 8, 'predicted_transition'),
    126: ('Ubh', 'Unbihexium', 8, 8, 'predicted_transition'),
}

# Color scheme
colors = {
    'alkali': '#FF6B6B',
    'alkaline_earth': '#FFD93D',
    'lanthanide': '#6BCB77',
    'actinide': '#4D96FF',
    'transition': '#95E1D3',
    'post_transition': '#C4C4C4',
    'metalloid': '#F38181',
    'nonmetal': '#AA96DA',
    'halogen': '#FCBAD3',
    'noble_gas': '#A8D8EA',
    'predicted_alkali': '#FF1744',  # Darker red
    'predicted_alkaline': '#FFC400',  # Darker yellow
    'predicted_superactinide': '#2962FF',  # Darker blue
    'predicted_transition': '#00BFA5',  # Darker teal
}

# Create figure
fig, ax = plt.subplots(figsize=(24, 14))
ax.set_xlim(0, 19)
ax.set_ylim(0, 11)
ax.set_aspect('equal')
ax.axis('off')

# Title
ax.text(9.5, 10.5, 'Periodic Table of Elements with UBP Predictions (Z=119-126)',
        ha='center', va='center', fontsize=20, fontweight='bold')

# Draw elements
for z, (symbol, name, group, period, elem_type) in elements.items():
    # Calculate position
    if period <= 7:
        x = group - 0.5
        y = 10 - period
    elif period == 8.5:  # Lanthanides
        x = (z - 57) + 3.5
        y = 10 - 8.5
    elif period == 9.5:  # Actinides
        x = (z - 89) + 3.5
        y = 10 - 9.5
    elif period == 8:  # Predicted Period 8
        x = group - 0.5
        y = 10 - 8
    
    # Draw box
    color = colors.get(elem_type, '#FFFFFF')
    rect = patches.Rectangle((x, y), 0.9, 0.9, 
                             linewidth=1.5 if z <= 118 else 2.5,
                             edgecolor='black' if z <= 118 else 'red',
                             facecolor=color,
                             linestyle='-' if z <= 118 else '--')
    ax.add_patch(rect)
    
    # Add text
    # Atomic number
    ax.text(x + 0.1, y + 0.75, str(z), 
           fontsize=7, ha='left', va='top', fontweight='bold')
    
    # Symbol
    ax.text(x + 0.45, y + 0.5, symbol, 
           fontsize=14 if z <= 118 else 12, 
           ha='center', va='center', 
           fontweight='bold',
           color='black' if z <= 118 else 'red')
    
    # Name (smaller for predicted)
    ax.text(x + 0.45, y + 0.15, name, 
           fontsize=5 if z <= 118 else 4.5, 
           ha='center', va='center',
           style='italic' if z > 118 else 'normal')

# Add legend
legend_y = 1.5
legend_items = [
    ('Alkali Metals', 'alkali'),
    ('Alkaline Earth', 'alkaline_earth'),
    ('Transition Metals', 'transition'),
    ('Post-transition', 'post_transition'),
    ('Metalloids', 'metalloid'),
    ('Nonmetals', 'nonmetal'),
    ('Halogens', 'halogen'),
    ('Noble Gases', 'noble_gas'),
    ('Lanthanides', 'lanthanide'),
    ('Actinides', 'actinide'),
    ('Predicted (UBP)', 'predicted_transition'),
]

for i, (label, elem_type) in enumerate(legend_items):
    x_pos = 0.5 + (i % 6) * 3
    y_pos = legend_y - (i // 6) * 0.5
    
    rect = patches.Rectangle((x_pos, y_pos), 0.4, 0.3, 
                             linewidth=1,
                             edgecolor='black',
                             facecolor=colors[elem_type])
    ax.add_patch(rect)
    
    ax.text(x_pos + 0.6, y_pos + 0.15, label, 
           fontsize=8, ha='left', va='center')

# Add note about predicted elements
ax.text(9.5, 0.3, 
       'Predicted elements (Z=119-126) shown with dashed borders and red text\n' +
       'Predictions based on UBP HexDictionary ensemble method (95.1% confidence)',
       ha='center', va='center', fontsize=9, style='italic',
       bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

# Add credit
ax.text(18.5, 0.1, 'UBP Study 2025\nEuan Craig, NZ', 
       ha='right', va='bottom', fontsize=7, style='italic')

plt.tight_layout()
plt.savefig('../visualizations/periodic_table_with_predictions.png', 
           dpi=300, bbox_inches='tight')
print("✓ Saved: periodic_table_with_predictions.png")

plt.savefig('../visualizations/periodic_table_with_predictions_highres.png', 
           dpi=600, bbox_inches='tight')
print("✓ Saved: periodic_table_with_predictions_highres.png (high resolution)")

plt.close()

print("\n✓ Periodic table visualization complete!")
print(f"  - 118 known elements")
print(f"  - 8 predicted elements (Z=119-126)")
print(f"  - Color-coded by element type")
print(f"  - Predicted elements marked with dashed borders and red text")
