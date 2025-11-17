#!/usr/bin/env python3.11
"""
Process Kaggle Comprehensive Minerals Database for UBP Analysis
Converts raw data into format compatible with mineral_coherence_model_v3_1
"""

import pandas as pd
import numpy as np
import json
from pathlib import Path

# Crystal system mapping (0-6 encoding)
CRYSTAL_SYSTEMS = {
    0.0: 'triclinic',
    1.0: 'monoclinic',
    2.0: 'orthorhombic',
    3.0: 'tetragonal',
    4.0: 'trigonal',
    5.0: 'hexagonal',
    6.0: 'cubic'
}

# Symmetry operations for each crystal system (typical values)
SYMMETRY_OPERATIONS = {
    'triclinic': 1,      # P1
    'monoclinic': 2,     # P2/m
    'orthorhombic': 4,   # Pmmm
    'tetragonal': 8,     # P4/mmm
    'trigonal': 6,       # P-3m
    'hexagonal': 12,     # P6/mmm
    'cubic': 48          # Pm-3m
}

# Atomic numbers for Z calculation
ATOMIC_NUMBERS = {
    'Hydrogen': 1, 'Helium': 2, 'Lithium': 3, 'Beryllium': 4, 'Boron': 5,
    'Carbon': 6, 'Nitrogen': 7, 'Oxygen': 8, 'Fluorine': 9, 'Neon': 10,
    'Sodium': 11, 'Magnesium': 12, 'Aluminium': 13, 'Silicon': 14, 'Phosphorus': 15,
    'Sulfur': 16, 'Chlorine': 17, 'Argon': 18, 'Potassium': 19, 'Calcium': 20,
    'Scandium': 21, 'Titanium': 22, 'Vanadium': 23, 'Chromium': 24, 'Manganese': 25,
    'Iron': 26, 'Cobalt': 27, 'Nickel': 28, 'Copper': 29, 'Zinc': 30,
    'Gallium': 31, 'Germanium': 32, 'Arsenic': 33, 'Selenium': 34, 'Bromine': 35,
    'Krypton': 36, 'Rubidium': 37, 'Strontium': 38, 'Yttrium': 39, 'Zirconium': 40,
    'Niobium': 41, 'Molybdenum': 42, 'Technetium': 43, 'Ruthenium': 44, 'Rhodium': 45,
    'Palladium': 46, 'Silver': 47, 'Cadmium': 48, 'Indium': 49, 'Tin': 50,
    'Antimony': 51, 'Tellurium': 52, 'Iodine': 53, 'Xenon': 54, 'Cesium': 55,
    'Barium': 56, 'Lanthanum': 57, 'Cerium': 58, 'Praseodymium': 59, 'Neodymium': 60,
    'Promethium': 61, 'Samarium': 62, 'Europium': 63, 'Gadolinium': 64, 'Terbium': 65,
    'Dysprosium': 66, 'Holmium': 67, 'Erbium': 68, 'Thulium': 69, 'Ytterbium': 70,
    'Lutetium': 71, 'Hafnium': 72, 'Tantalum': 73, 'Tungsten': 74, 'Rhenium': 75,
    'Osmium': 76, 'Iridium': 77, 'Platinum': 78, 'Gold': 79, 'Mercury': 80,
    'Thallium': 81, 'Lead': 82, 'Bismuth': 83, 'Polonium': 84, 'Astatine': 85,
    'Radon': 86, 'Francium': 87, 'Radium': 88, 'Actinium': 89, 'Thorium': 90,
    'Protactinium': 91, 'Uranium': 92
}

def calc_z_max(row, element_columns):
    """Calculate maximum atomic number (Z) present in mineral"""
    z_max = 0
    for elem in element_columns:
        if elem in ATOMIC_NUMBERS and row[elem] > 0:
            z_max = max(z_max, ATOMIC_NUMBERS[elem])
    return z_max

def calc_element_count(row, element_columns):
    """Count number of different elements in mineral"""
    count = 0
    for elem in element_columns:
        if elem in ATOMIC_NUMBERS and row[elem] > 0:
            count += 1
    return count

def generate_chemical_formula(row, element_columns):
    """Generate simplified chemical formula from elemental composition"""
    elements = []
    for elem in element_columns:
        if elem in ATOMIC_NUMBERS and row[elem] > 0:
            count = row[elem]
            if count == 1:
                elements.append(elem[:2])  # First 2 letters (e.g., Ca, Si)
            else:
                elements.append(f"{elem[:2]}{int(count)}")
    return "".join(elements[:10])  # Limit to first 10 elements for readability

def main():
    print("="*80)
    print("PROCESSING KAGGLE COMPREHENSIVE MINERALS DATABASE")
    print("="*80)
    
    # Load dataset
    print("\n[1/5] Loading Minerals_Database.csv...")
    df = pd.read_csv('data/Minerals_Database.csv')
    print(f"   Loaded {len(df)} minerals")
    
    # Identify element columns
    excluded_cols = ['Unnamed: 0', 'Name', 'Crystal Structure', 'Mohs Hardness', 
                     'Diaphaneity', 'Specific Gravity', 'Optical', 'Refractive Index', 
                     'Dispersion', 'Cyanide', 'Nitrate', 'Hydroxyl', 'Acetate', 
                     'Phosphate', 'Sulphate', 'Carbonate', 'Ammonium', 'Hydrated Water', 
                     'count', 'Molar Mass', 'Molar Volume', 'Calculated Density']
    element_columns = [col for col in df.columns if col not in excluded_cols]
    print(f"   Found {len(element_columns)} element columns")
    
    # Process data
    print("\n[2/5] Calculating Z_max and element counts...")
    df['Z_max'] = df.apply(lambda row: calc_z_max(row, element_columns), axis=1)
    df['element_count'] = df.apply(lambda row: calc_element_count(row, element_columns), axis=1)
    print(f"   Z_max range: {df['Z_max'].min()} to {df['Z_max'].max()}")
    print(f"   Element count range: {df['element_count'].min()} to {df['element_count'].max()}")
    
    # Map crystal systems
    print("\n[3/5] Mapping crystal systems...")
    df['crystal_system'] = df['Crystal Structure'].map(CRYSTAL_SYSTEMS)
    df['symmetry_operations'] = df['crystal_system'].map(SYMMETRY_OPERATIONS)
    print(f"   Crystal system distribution:")
    for system, count in df['crystal_system'].value_counts().sort_index().items():
        print(f"      {system:15s}: {count:4d} minerals ({count/len(df)*100:5.2f}%)")
    
    # Generate formulas
    print("\n[4/5] Generating chemical formulas...")
    df['formula'] = df.apply(lambda row: generate_chemical_formula(row, element_columns), axis=1)
    
    # Create output dataset
    print("\n[5/5] Creating output dataset...")
    output_data = []
    for idx, row in df.iterrows():
        mineral = {
            'name': row['Name'],
            'formula': row['formula'],
            'crystal_system': row['crystal_system'],
            'symmetry_operations': int(row['symmetry_operations']),
            'Z_max': int(row['Z_max']),
            'element_count': int(row['element_count']),
            'molar_mass': float(row['Molar Mass']),
            'density': float(row['Calculated Density']),
            'mohs_hardness': float(row['Mohs Hardness']) if not pd.isna(row['Mohs Hardness']) else None
        }
        output_data.append(mineral)
    
    # Save to JSON
    output_file = 'data/minerals_processed_3112.json'
    with open(output_file, 'w') as f:
        json.dump(output_data, f, indent=2)
    print(f"   Saved to {output_file}")
    
    # Statistics
    print("\n" + "="*80)
    print("PROCESSING COMPLETE - STATISTICS")
    print("="*80)
    print(f"Total minerals processed: {len(output_data)}")
    print(f"\nZ_max distribution:")
    print(f"   Mean: {df['Z_max'].mean():.2f}")
    print(f"   Median: {df['Z_max'].median():.2f}")
    print(f"   Std: {df['Z_max'].std():.2f}")
    print(f"\nBottleneck zone (Z=80-92): {len(df[df['Z_max'].between(80, 92)])} minerals ({len(df[df['Z_max'].between(80, 92)])/len(df)*100:.2f}%)")
    print(f"\nSymmetry distribution:")
    for sym, count in df['symmetry_operations'].value_counts().sort_index().items():
        print(f"   {sym:2d} operations: {count:4d} minerals ({count/len(df)*100:5.2f}%)")
    
    print(f"\n✓ Dataset ready for UBP coherence analysis!")
    print(f"✓ Output: {output_file}")

if __name__ == '__main__':
    main()
