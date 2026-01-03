#!/usr/bin/env python3
"""
OffBits Analysis - Generate Large Chemical Dataset
====================================================
Create a substantial dataset of chemicals with diverse properties
Focus on plastics, monomers, and environmental chemicals
"""

import sys
import json
import numpy as np
import pandas as pd
from pathlib import Path

BASE_DIR = Path("/app/sandbox/session_20260102_222825_9c4bac117ac1")

print("=" * 70)
print("GENERATING LARGE CHEMICAL DATASET FOR OFFBITS ANALYSIS")
print("=" * 70)

# Set random seed for reproducibility
np.random.seed(42)

# Comprehensive chemical database
# Including: plastics, monomers, solvents, toxics, biodegradables, etc.
chemicals_database = [
    # ===== COMMODITY PLASTICS =====
    {"name": "Polyethylene (PE)", "formula": "C2H4", "mw": 28.05, "carbon": 2, "hydrogen": 4, "oxygen": 0, "nitrogen": 0, "chlorine": 0, "fluorine": 0,
     "aromatic": 0, "ester": 0, "amide": 0, "ether": 0, "halogen": 0, "biodegradable": 0, "toxic": 0, "persistent": 1.0, "category": "plastic_commodity"},

    {"name": "Polypropylene (PP)", "formula": "C3H6", "mw": 42.08, "carbon": 3, "hydrogen": 6, "oxygen": 0, "nitrogen": 0, "chlorine": 0, "fluorine": 0,
     "aromatic": 0, "ester": 0, "amide": 0, "ether": 0, "halogen": 0, "biodegradable": 0, "toxic": 0, "persistent": 0.95, "category": "plastic_commodity"},

    {"name": "Polyvinyl chloride (PVC)", "formula": "C2H3Cl", "mw": 62.50, "carbon": 2, "hydrogen": 3, "oxygen": 0, "nitrogen": 0, "chlorine": 1, "fluorine": 0,
     "aromatic": 0, "ester": 0, "amide": 0, "ether": 0, "halogen": 1, "biodegradable": 0, "toxic": 0.7, "persistent": 1.0, "category": "plastic_commodity"},

    {"name": "Polystyrene (PS)", "formula": "C8H8", "mw": 104.15, "carbon": 8, "hydrogen": 8, "oxygen": 0, "nitrogen": 0, "chlorine": 0, "fluorine": 0,
     "aromatic": 1, "ester": 0, "amide": 0, "ether": 0, "halogen": 0, "biodegradable": 0, "toxic": 0.3, "persistent": 0.9, "category": "plastic_commodity"},

    {"name": "Polyethylene terephthalate (PET)", "formula": "C10H8O4", "mw": 192.17, "carbon": 10, "hydrogen": 8, "oxygen": 4, "nitrogen": 0, "chlorine": 0, "fluorine": 0,
     "aromatic": 1, "ester": 1, "amide": 0, "ether": 0, "halogen": 0, "biodegradable": 0.1, "toxic": 0.1, "persistent": 0.8, "category": "plastic_commodity"},

    {"name": "Polyvinyl chloride (PVDC)", "formula": "C2H2Cl2", "mw": 96.94, "carbon": 2, "hydrogen": 2, "oxygen": 0, "nitrogen": 0, "chlorine": 2, "fluorine": 0,
     "aromatic": 0, "ester": 0, "amide": 0, "ether": 0, "halogen": 1, "biodegradable": 0, "toxic": 0.8, "persistent": 1.0, "category": "plastic_commodity"},

    # ===== ENGINEERING PLASTICS =====
    {"name": "Nylon 6 (PA6)", "formula": "C6H11NO", "mw": 113.16, "carbon": 6, "hydrogen": 11, "oxygen": 1, "nitrogen": 1, "chlorine": 0, "fluorine": 0,
     "aromatic": 0, "ester": 0, "amide": 1, "ether": 0, "halogen": 0, "biodegradable": 0.3, "toxic": 0.1, "persistent": 0.6, "category": "plastic_engineering"},

    {"name": "Polycarbonate (PC)", "formula": "C16H14O3", "mw": 254.28, "carbon": 16, "hydrogen": 14, "oxygen": 3, "nitrogen": 0, "chlorine": 0, "fluorine": 0,
     "aromatic": 1, "ester": 1, "amide": 0, "ether": 0, "halogen": 0, "biodegradable": 0.05, "toxic": 0.4, "persistent": 0.85, "category": "plastic_engineering"},

    {"name": "Polytetrafluoroethylene (PTFE)", "formula": "C2F4", "mw": 100.02, "carbon": 2, "hydrogen": 0, "oxygen": 0, "nitrogen": 0, "chlorine": 0, "fluorine": 4,
     "aromatic": 0, "ester": 0, "amide": 0, "ether": 0, "halogen": 1, "biodegradable": 0, "toxic": 0.2, "persistent": 1.0, "category": "plastic_engineering"},

    {"name": "Polyurethane (PU)", "formula": "C3H6N2O2", "mw": 118.09, "carbon": 3, "hydrogen": 6, "oxygen": 2, "nitrogen": 2, "chlorine": 0, "fluorine": 0,
     "aromatic": 0, "ester": 0, "amide": 1, "ether": 0, "halogen": 0, "biodegradable": 0.4, "toxic": 0.3, "persistent": 0.5, "category": "plastic_engineering"},

    {"name": "Polymethyl methacrylate (PMMA)", "formula": "C5H8O2", "mw": 100.12, "carbon": 5, "hydrogen": 8, "oxygen": 2, "nitrogen": 0, "chlorine": 0, "fluorine": 0,
     "aromatic": 0, "ester": 1, "amide": 0, "ether": 0, "halogen": 0, "biodegradable": 0.15, "toxic": 0.2, "persistent": 0.75, "category": "plastic_engineering"},

    # ===== BIODEGRADABLE PLASTICS =====
    {"name": "Polylactic acid (PLA)", "formula": "C3H4O2", "mw": 72.06, "carbon": 3, "hydrogen": 4, "oxygen": 2, "nitrogen": 0, "chlorine": 0, "fluorine": 0,
     "aromatic": 0, "ester": 1, "amide": 0, "ether": 0, "halogen": 0, "biodegradable": 0.8, "toxic": 0, "persistent": 0.2, "category": "plastic_biodegradable"},

    {"name": "Polyhydroxybutyrate (PHB)", "formula": "C4H6O2", "mw": 86.09, "carbon": 4, "hydrogen": 6, "oxygen": 2, "nitrogen": 0, "chlorine": 0, "fluorine": 0,
     "aromatic": 0, "ester": 1, "amide": 0, "ether": 0, "halogen": 0, "biodegradable": 0.9, "toxic": 0, "persistent": 0.1, "category": "plastic_biodegradable"},

    {"name": "Polybutylene succinate (PBS)", "formula": "C8H12O4", "mw": 172.18, "carbon": 8, "hydrogen": 12, "oxygen": 4, "nitrogen": 0, "chlorine": 0, "fluorine": 0,
     "aromatic": 0, "ester": 1, "amide": 0, "ether": 0, "halogen": 0, "biodegradable": 0.75, "toxic": 0, "persistent": 0.25, "category": "plastic_biodegradable"},

    {"name": "Cellulose acetate", "formula": "C76H114O49", "mw": 1839.67, "carbon": 76, "hydrogen": 114, "oxygen": 49, "nitrogen": 0, "chlorine": 0, "fluorine": 0,
     "aromatic": 0, "ester": 1, "amide": 0, "ether": 1, "halogen": 0, "biodegradable": 0.6, "toxic": 0, "persistent": 0.3, "category": "plastic_biodegradable"},

    # ===== PLASTIC MONOMERS =====
    {"name": "Ethylene", "formula": "C2H4", "mw": 28.05, "carbon": 2, "hydrogen": 4, "oxygen": 0, "nitrogen": 0, "chlorine": 0, "fluorine": 0,
     "aromatic": 0, "ester": 0, "amide": 0, "ether": 0, "halogen": 0, "biodegradable": 0.5, "toxic": 0.2, "persistent": 0.3, "category": "monomer"},

    {"name": "Propylene", "formula": "C3H6", "mw": 42.08, "carbon": 3, "hydrogen": 6, "oxygen": 0, "nitrogen": 0, "chlorine": 0, "fluorine": 0,
     "aromatic": 0, "ester": 0, "amide": 0, "ether": 0, "halogen": 0, "biodegradable": 0.5, "toxic": 0.2, "persistent": 0.3, "category": "monomer"},

    {"name": "Styrene", "formula": "C8H8", "mw": 104.15, "carbon": 8, "hydrogen": 8, "oxygen": 0, "nitrogen": 0, "chlorine": 0, "fluorine": 0,
     "aromatic": 1, "ester": 0, "amide": 0, "ether": 0, "halogen": 0, "biodegradable": 0.4, "toxic": 0.6, "persistent": 0.5, "category": "monomer"},

    {"name": "Vinyl chloride", "formula": "C2H3Cl", "mw": 62.50, "carbon": 2, "hydrogen": 3, "oxygen": 0, "nitrogen": 0, "chlorine": 1, "fluorine": 0,
     "aromatic": 0, "ester": 0, "amide": 0, "ether": 0, "halogen": 1, "biodegradable": 0.3, "toxic": 0.9, "persistent": 0.7, "category": "monomer"},

    {"name": "Methyl methacrylate", "formula": "C5H8O2", "mw": 100.12, "carbon": 5, "hydrogen": 8, "oxygen": 2, "nitrogen": 0, "chlorine": 0, "fluorine": 0,
     "aromatic": 0, "ester": 1, "amide": 0, "ether": 0, "halogen": 0, "biodegradable": 0.4, "toxic": 0.3, "persistent": 0.4, "category": "monomer"},

    # ===== PLASTICIZERS (TOXIC ADDITIVES) =====
    {"name": "Diethylhexyl phthalate (DEHP)", "formula": "C24H38O4", "mw": 390.56, "carbon": 24, "hydrogen": 38, "oxygen": 4, "nitrogen": 0, "chlorine": 0, "fluorine": 0,
     "aromatic": 1, "ester": 1, "amide": 0, "ether": 0, "halogen": 0, "biodegradable": 0.3, "toxic": 0.9, "persistent": 0.8, "category": "plasticizer"},

    {"name": "Dibutyl phthalate (DBP)", "formula": "C16H22O4", "mw": 278.34, "carbon": 16, "hydrogen": 22, "oxygen": 4, "nitrogen": 0, "chlorine": 0, "fluorine": 0,
     "aromatic": 1, "ester": 1, "amide": 0, "ether": 0, "halogen": 0, "biodegradable": 0.4, "toxic": 0.8, "persistent": 0.7, "category": "plasticizer"},

    {"name": "Bisphenol A (BPA)", "formula": "C15H16O2", "mw": 228.29, "carbon": 15, "hydrogen": 16, "oxygen": 2, "nitrogen": 0, "chlorine": 0, "fluorine": 0,
     "aromatic": 1, "ester": 0, "amide": 0, "ether": 0, "halogen": 0, "biodegradable": 0.3, "toxic": 0.85, "persistent": 0.6, "category": "plasticizer"},

    # ===== PERSISTENT ORGANIC POLLUTANTS (POPs) =====
    {"name": "DDT", "formula": "C14H9Cl5", "mw": 354.49, "carbon": 14, "hydrogen": 9, "oxygen": 0, "nitrogen": 0, "chlorine": 5, "fluorine": 0,
     "aromatic": 1, "ester": 0, "amide": 0, "ether": 0, "halogen": 1, "biodegradable": 0.05, "toxic": 0.95, "persistent": 1.0, "category": "pollutant"},

    {"name": "PCB (Aroclor 1254)", "formula": "C12H5Cl5", "mw": 326.43, "carbon": 12, "hydrogen": 5, "oxygen": 0, "nitrogen": 0, "chlorine": 5, "fluorine": 0,
     "aromatic": 1, "ester": 0, "amide": 0, "ether": 0, "halogen": 1, "biodegradable": 0, "toxic": 1.0, "persistent": 1.0, "category": "pollutant"},

    {"name": "Dioxin (TCDD)", "formula": "C12H4Cl4O2", "mw": 321.97, "carbon": 12, "hydrogen": 4, "oxygen": 2, "nitrogen": 0, "chlorine": 4, "fluorine": 0,
     "aromatic": 1, "ester": 0, "amide": 0, "ether": 1, "halogen": 1, "biodegradable": 0, "toxic": 1.0, "persistent": 1.0, "category": "pollutant"},

    # ===== INDUSTRIAL SOLVENTS =====
    {"name": "Toluene", "formula": "C7H8", "mw": 92.14, "carbon": 7, "hydrogen": 8, "oxygen": 0, "nitrogen": 0, "chlorine": 0, "fluorine": 0,
     "aromatic": 1, "ester": 0, "amide": 0, "ether": 0, "halogen": 0, "biodegradable": 0.6, "toxic": 0.5, "persistent": 0.3, "category": "solvent"},

    {"name": "Benzene", "formula": "C6H6", "mw": 78.11, "carbon": 6, "hydrogen": 6, "oxygen": 0, "nitrogen": 0, "chlorine": 0, "fluorine": 0,
     "aromatic": 1, "ester": 0, "amide": 0, "ether": 0, "halogen": 0, "biodegradable": 0.5, "toxic": 0.8, "persistent": 0.4, "category": "solvent"},

    {"name": "Xylene", "formula": "C8H10", "mw": 106.17, "carbon": 8, "hydrogen": 10, "oxygen": 0, "nitrogen": 0, "chlorine": 0, "fluorine": 0,
     "aromatic": 1, "ester": 0, "amide": 0, "ether": 0, "halogen": 0, "biodegradable": 0.55, "toxic": 0.6, "persistent": 0.35, "category": "solvent"},

    {"name": "Acetone", "formula": "C3H6O", "mw": 58.08, "carbon": 3, "hydrogen": 6, "oxygen": 1, "nitrogen": 0, "chlorine": 0, "fluorine": 0,
     "aromatic": 0, "ester": 0, "amide": 0, "ether": 0, "halogen": 0, "biodegradable": 0.9, "toxic": 0.2, "persistent": 0.1, "category": "solvent"},

    {"name": "Methanol", "formula": "CH4O", "mw": 32.04, "carbon": 1, "hydrogen": 4, "oxygen": 1, "nitrogen": 0, "chlorine": 0, "fluorine": 0,
     "aromatic": 0, "ester": 0, "amide": 0, "ether": 0, "halogen": 0, "biodegradable": 0.95, "toxic": 0.4, "persistent": 0.05, "category": "solvent"},

    {"name": "Ethanol", "formula": "C2H6O", "mw": 46.07, "carbon": 2, "hydrogen": 6, "oxygen": 1, "nitrogen": 0, "chlorine": 0, "fluorine": 0,
     "aromatic": 0, "ester": 0, "amide": 0, "ether": 0, "halogen": 0, "biodegradable": 0.95, "toxic": 0.2, "persistent": 0.05, "category": "solvent"},

    # ===== PHARMACEUTICALS =====
    {"name": "Aspirin", "formula": "C9H8O4", "mw": 180.16, "carbon": 9, "hydrogen": 8, "oxygen": 4, "nitrogen": 0, "chlorine": 0, "fluorine": 0,
     "aromatic": 1, "ester": 1, "amide": 0, "ether": 0, "halogen": 0, "biodegradable": 0.7, "toxic": 0.3, "persistent": 0.2, "category": "pharmaceutical"},

    {"name": "Ibuprofen", "formula": "C13H18O2", "mw": 206.28, "carbon": 13, "hydrogen": 18, "oxygen": 2, "nitrogen": 0, "chlorine": 0, "fluorine": 0,
     "aromatic": 1, "ester": 0, "amide": 0, "ether": 0, "halogen": 0, "biodegradable": 0.6, "toxic": 0.4, "persistent": 0.3, "category": "pharmaceutical"},

    {"name": "Paracetamol", "formula": "C8H9NO2", "mw": 151.16, "carbon": 8, "hydrogen": 9, "oxygen": 2, "nitrogen": 1, "chlorine": 0, "fluorine": 0,
     "aromatic": 1, "ester": 0, "amide": 1, "ether": 0, "halogen": 0, "biodegradable": 0.7, "toxic": 0.3, "persistent": 0.25, "category": "pharmaceutical"},

    # ===== FLAME RETARDANTS =====
    {"name": "PBDE (DecaBDE)", "formula": "C12Br10O", "mw": 959.17, "carbon": 12, "hydrogen": 0, "oxygen": 1, "nitrogen": 0, "chlorine": 0, "fluorine": 0,
     "aromatic": 1, "ester": 0, "amide": 0, "ether": 1, "halogen": 1, "biodegradable": 0, "toxic": 0.9, "persistent": 1.0, "category": "flame_retardant"},

    {"name": "TBBPA", "formula": "C15H12Br4O2", "mw": 543.87, "carbon": 15, "hydrogen": 12, "oxygen": 2, "nitrogen": 0, "chlorine": 0, "fluorine": 0,
     "aromatic": 1, "ester": 0, "amide": 0, "ether": 0, "halogen": 1, "biodegradable": 0.1, "toxic": 0.8, "persistent": 0.9, "category": "flame_retardant"},
]

print(f"\n[1/3] Base chemical database: {len(chemicals_database)} compounds")

# Expand dataset with variations and additional compounds
expanded_dataset = []

# Add all base compounds
for chem in chemicals_database:
    expanded_dataset.append(chem.copy())

# Generate synthetic variations (different substituents, chain lengths, etc.)
print("\n[2/3] Generating synthetic variations...")

base_polymers = [
    {"prefix": "Polyethylene-", "base_c": 2, "base_h": 4, "variations": 10},
    {"prefix": "Polypropylene-", "base_c": 3, "base_h": 6, "variations": 8},
    {"prefix": "Polyester-", "base_c": 5, "base_h": 4, "base_o": 2, "variations": 12},
    {"prefix": "Polyamide-", "base_c": 6, "base_h": 11, "base_n": 1, "base_o": 1, "variations": 10},
]

for poly in base_polymers:
    for i in range(poly["variations"]):
        variation = {
            "name": f"{poly['prefix']}{i+1}",
            "formula": f"C{poly['base_c']+i}H{poly.get('base_h', 0)+2*i}",
            "mw": poly['base_c'] * 12 + poly.get('base_h', 0) * 1.008 + i * 14,
            "carbon": poly['base_c'] + i,
            "hydrogen": poly.get('base_h', 0) + 2 * i,
            "oxygen": poly.get('base_o', 0),
            "nitrogen": poly.get('base_n', 0),
            "chlorine": 0,
            "fluorine": 0,
            "aromatic": 0,
            "ester": 1 if 'ester' in poly['prefix'].lower() else 0,
            "amide": 1 if 'amide' in poly['prefix'].lower() else 0,
            "ether": 0,
            "halogen": 0,
            "biodegradable": 0.3 + 0.05 * i,
            "toxic": 0.2 - 0.02 * i,
            "persistent": 0.7 - 0.05 * i,
            "category": "synthetic_variation"
        }
        expanded_dataset.append(variation)

print(f"   Added {sum([p['variations'] for p in base_polymers])} polymer variations")

# Add halogenated variations of common compounds
halogen_bases = ["Ethylene", "Propylene", "Benzene", "Toluene"]
for base_name in halogen_bases:
    base_compound = next((c for c in chemicals_database if c["name"] == base_name), None)
    if base_compound:
        for n_cl in range(1, 4):
            halogenated = base_compound.copy()
            halogenated["name"] = f"{base_name}-Cl{n_cl}"
            halogenated["chlorine"] = n_cl
            halogenated["halogen"] = 1
            halogenated["toxic"] = min(1.0, base_compound["toxic"] + 0.2 * n_cl)
            halogenated["persistent"] = min(1.0, base_compound["persistent"] + 0.15 * n_cl)
            halogenated["biodegradable"] = max(0.0, base_compound["biodegradable"] - 0.2 * n_cl)
            halogenated["category"] = "halogenated"
            expanded_dataset.append(halogenated)

print(f"   Added halogenated variations")

# Final dataset
df = pd.DataFrame(expanded_dataset)

# Calculate additional descriptors
df['total_atoms'] = df['carbon'] + df['hydrogen'] + df['oxygen'] + df['nitrogen'] + df['chlorine'] + df['fluorine']
df['C_ratio'] = df['carbon'] / df['total_atoms']
df['H_ratio'] = df['hydrogen'] / df['total_atoms']
df['O_ratio'] = df['oxygen'] / df['total_atoms']
df['heteroatom_ratio'] = (df['nitrogen'] + df['oxygen'] + df['chlorine'] + df['fluorine']) / df['total_atoms']

print(f"\n[3/3] Final dataset statistics:")
print(f"   Total compounds: {len(df)}")
print(f"   Categories: {df['category'].nunique()}")
print(f"   Category distribution:")
for cat, count in df['category'].value_counts().items():
    print(f"      {cat}: {count}")

# Save dataset
output_file = BASE_DIR / "data" / "large_chemicals_dataset.csv"
df.to_csv(output_file, index=False)

print(f"\n✓ Dataset saved to: {output_file}")
print(f"   Shape: {df.shape}")
print(f"   Columns: {', '.join(df.columns)}")

# Generate summary statistics
summary_stats = {
    "total_compounds": len(df),
    "categories": df['category'].unique().tolist(),
    "category_counts": df['category'].value_counts().to_dict(),
    "molecular_weight_range": [float(df['mw'].min()), float(df['mw'].max())],
    "biodegradable_range": [float(df['biodegradable'].min()), float(df['biodegradable'].max())],
    "toxic_range": [float(df['toxic'].min()), float(df['toxic'].max())],
    "persistent_range": [float(df['persistent'].min()), float(df['persistent'].max())]
}

summary_file = BASE_DIR / "data" / "dataset_summary.json"
with open(summary_file, 'w') as f:
    json.dump(summary_stats, f, indent=2)

print(f"✓ Summary saved to: {summary_file}")
print("\n" + "=" * 70)
print("✓ DATASET GENERATION COMPLETE")
print("=" * 70)
print(f"\nNext: Run 03_offbits_mapping_strategies.py")
