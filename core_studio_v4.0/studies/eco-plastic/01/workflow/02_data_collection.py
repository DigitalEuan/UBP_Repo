#!/usr/bin/env python3
"""
Step 2: Chemical Data Collection
Creates a comprehensive dataset of plastics and chemicals with their properties.
"""

import pandas as pd
import json
from pathlib import Path

print("="*80)
print("STEP 2: CHEMICAL DATA COLLECTION")
print("="*80)

# Comprehensive dataset of common plastics and materials
chemicals_data = [
    {
        "material": "Polyethylene (LDPE)",
        "abbrev": "PE-LD",
        "repeat_unit": "C2H4",
        "formula_atoms": {"C": 2, "H": 4, "O": 0, "N": 0, "Cl": 0, "S": 0},
        "molecular_weight": 28.05,
        "category": "Commodity Plastic",
        "biodegradable": False,
        "environmental_persistence": "High",
        "persistence_score": 5,  # 1=low, 5=very high
        "toxicity": "Low",
        "toxicity_score": 1,  # 1=low, 5=very high
        "notes": "Most common plastic, very stable, takes 500+ years to degrade"
    },
    {
        "material": "Polypropylene (PP)",
        "abbrev": "PP",
        "repeat_unit": "C3H6",
        "formula_atoms": {"C": 3, "H": 6, "O": 0, "N": 0, "Cl": 0, "S": 0},
        "molecular_weight": 42.08,
        "category": "Commodity Plastic",
        "biodegradable": False,
        "environmental_persistence": "High",
        "persistence_score": 5,
        "toxicity": "Low",
        "toxicity_score": 1,
        "notes": "Second most common plastic, resistant to degradation"
    },
    {
        "material": "Polyvinyl Chloride (PVC)",
        "abbrev": "PVC",
        "repeat_unit": "C2H3Cl",
        "formula_atoms": {"C": 2, "H": 3, "O": 0, "N": 0, "Cl": 1, "S": 0},
        "molecular_weight": 62.50,
        "category": "Commodity Plastic",
        "biodegradable": False,
        "environmental_persistence": "Very High",
        "persistence_score": 5,
        "toxicity": "High",
        "toxicity_score": 4,
        "notes": "Contains chlorine, releases toxic compounds when burned"
    },
    {
        "material": "Polystyrene (PS)",
        "abbrev": "PS",
        "repeat_unit": "C8H8",
        "formula_atoms": {"C": 8, "H": 8, "O": 0, "N": 0, "Cl": 0, "S": 0},
        "molecular_weight": 104.15,
        "category": "Commodity Plastic",
        "biodegradable": False,
        "environmental_persistence": "High",
        "persistence_score": 5,
        "toxicity": "Moderate",
        "toxicity_score": 3,
        "notes": "Aromatic polymer, slow degradation, styrene monomer is toxic"
    },
    {
        "material": "Polyethylene Terephthalate (PET)",
        "abbrev": "PET",
        "repeat_unit": "C10H8O4",
        "formula_atoms": {"C": 10, "H": 8, "O": 4, "N": 0, "Cl": 0, "S": 0},
        "molecular_weight": 192.17,
        "category": "Commodity Plastic",
        "biodegradable": False,
        "environmental_persistence": "High",
        "persistence_score": 4,
        "toxicity": "Low",
        "toxicity_score": 2,
        "notes": "Common in bottles, takes 450+ years to degrade"
    },
    {
        "material": "Polylactic Acid (PLA)",
        "abbrev": "PLA",
        "repeat_unit": "C3H4O2",
        "formula_atoms": {"C": 3, "H": 4, "O": 2, "N": 0, "Cl": 0, "S": 0},
        "molecular_weight": 72.06,
        "category": "Biodegradable Plastic",
        "biodegradable": True,
        "environmental_persistence": "Low",
        "persistence_score": 2,
        "toxicity": "Very Low",
        "toxicity_score": 1,
        "notes": "Bio-based from corn starch, degrades in 6-24 months under composting"
    },
    {
        "material": "Polyhydroxybutyrate (PHB)",
        "abbrev": "PHB",
        "repeat_unit": "C4H6O2",
        "formula_atoms": {"C": 4, "H": 6, "O": 2, "N": 0, "Cl": 0, "S": 0},
        "molecular_weight": 86.09,
        "category": "Biodegradable Plastic",
        "biodegradable": True,
        "environmental_persistence": "Very Low",
        "persistence_score": 1,
        "toxicity": "Very Low",
        "toxicity_score": 1,
        "notes": "Bacterial polyester, degrades in weeks to months"
    },
    {
        "material": "Polybutylene Succinate (PBS)",
        "abbrev": "PBS",
        "repeat_unit": "C8H12O4",
        "formula_atoms": {"C": 8, "H": 12, "O": 4, "N": 0, "Cl": 0, "S": 0},
        "molecular_weight": 172.18,
        "category": "Biodegradable Plastic",
        "biodegradable": True,
        "environmental_persistence": "Low",
        "persistence_score": 2,
        "toxicity": "Very Low",
        "toxicity_score": 1,
        "notes": "Bio-based polyester, degrades in months"
    },
    {
        "material": "Nylon-6 (Polyamide)",
        "abbrev": "PA6",
        "repeat_unit": "C6H11NO",
        "formula_atoms": {"C": 6, "H": 11, "O": 1, "N": 1, "Cl": 0, "S": 0},
        "molecular_weight": 113.16,
        "category": "Engineering Plastic",
        "biodegradable": False,
        "environmental_persistence": "High",
        "persistence_score": 4,
        "toxicity": "Low",
        "toxicity_score": 2,
        "notes": "Contains amide bonds, more resistant to degradation"
    },
    {
        "material": "Polycarbonate (PC)",
        "abbrev": "PC",
        "repeat_unit": "C16H14O3",
        "formula_atoms": {"C": 16, "H": 14, "O": 3, "N": 0, "Cl": 0, "S": 0},
        "molecular_weight": 254.28,
        "category": "Engineering Plastic",
        "biodegradable": False,
        "environmental_persistence": "High",
        "persistence_score": 4,
        "toxicity": "Moderate",
        "toxicity_score": 3,
        "notes": "Contains BPA, controversial due to hormone disruption"
    },
    {
        "material": "Polytetrafluoroethylene (PTFE/Teflon)",
        "abbrev": "PTFE",
        "repeat_unit": "C2F4",
        "formula_atoms": {"C": 2, "H": 0, "O": 0, "N": 0, "Cl": 0, "F": 4, "S": 0},
        "molecular_weight": 100.02,
        "category": "Engineering Plastic",
        "biodegradable": False,
        "environmental_persistence": "Very High",
        "persistence_score": 5,
        "toxicity": "Moderate",
        "toxicity_score": 3,
        "notes": "Forever chemical, extremely stable C-F bonds"
    },
    {
        "material": "Cellulose Acetate",
        "abbrev": "CA",
        "repeat_unit": "C12H16O8",
        "formula_atoms": {"C": 12, "H": 16, "O": 8, "N": 0, "Cl": 0, "S": 0},
        "molecular_weight": 288.25,
        "category": "Semi-Biodegradable",
        "biodegradable": True,
        "environmental_persistence": "Moderate",
        "persistence_score": 3,
        "toxicity": "Low",
        "toxicity_score": 1,
        "notes": "Semi-synthetic from cellulose, degrades in 2-5 years"
    },
    {
        "material": "Polyvinylidene Chloride (PVDC)",
        "abbrev": "PVDC",
        "repeat_unit": "C2H2Cl2",
        "formula_atoms": {"C": 2, "H": 2, "O": 0, "N": 0, "Cl": 2, "S": 0},
        "molecular_weight": 96.94,
        "category": "Commodity Plastic",
        "biodegradable": False,
        "environmental_persistence": "Very High",
        "persistence_score": 5,
        "toxicity": "High",
        "toxicity_score": 4,
        "notes": "Contains 2 chlorine atoms, used in cling film, toxic when burned"
    },
    {
        "material": "Polyurethane (PU)",
        "abbrev": "PU",
        "repeat_unit": "C17H16N2O4",
        "formula_atoms": {"C": 17, "H": 16, "O": 4, "N": 2, "Cl": 0, "S": 0},
        "molecular_weight": 312.32,
        "category": "Engineering Plastic",
        "biodegradable": False,
        "environmental_persistence": "Moderate",
        "persistence_score": 3,
        "toxicity": "Moderate",
        "toxicity_score": 2,
        "notes": "Contains urethane linkages, foam degrades but base polymer persists"
    },
    {
        "material": "Polymethyl Methacrylate (PMMA/Acrylic)",
        "abbrev": "PMMA",
        "repeat_unit": "C5H8O2",
        "formula_atoms": {"C": 5, "H": 8, "O": 2, "N": 0, "Cl": 0, "S": 0},
        "molecular_weight": 100.12,
        "category": "Engineering Plastic",
        "biodegradable": False,
        "environmental_persistence": "High",
        "persistence_score": 4,
        "toxicity": "Low",
        "toxicity_score": 1,
        "notes": "Transparent polymer, used in displays and optical applications"
    }
]

print(f"\n[1/3] Creating dataset with {len(chemicals_data)} materials...")

# Create DataFrame
df = pd.DataFrame(chemicals_data)

# Calculate total atoms per repeat unit
df['total_atoms'] = df['formula_atoms'].apply(
    lambda x: sum([v for k, v in x.items() if k != 'F'])
)

# Calculate atomic ratios (normalized by total atoms)
for atom in ['C', 'H', 'O', 'N', 'Cl']:
    df[f'{atom}_ratio'] = df['formula_atoms'].apply(
        lambda x: x.get(atom, 0) / max(sum([v for k, v in x.items() if k != 'F']), 1)
    )

print(f"  ✓ Dataset created with {len(df)} materials")
print(f"  ✓ Categories: {df['category'].nunique()} ({', '.join(df['category'].unique())})")
print(f"  ✓ Biodegradable: {df['biodegradable'].sum()}/{len(df)}")

print(f"\n[2/3] Dataset statistics:")
print(f"  - Molecular Weight range: {df['molecular_weight'].min():.2f} - {df['molecular_weight'].max():.2f} g/mol")
print(f"  - Persistence scores: {df['persistence_score'].min()} - {df['persistence_score'].max()}")
print(f"  - Toxicity scores: {df['toxicity_score'].min()} - {df['toxicity_score'].max()}")

print(f"\n  Material categories breakdown:")
for cat, count in df['category'].value_counts().items():
    print(f"    • {cat}: {count} materials")

print(f"\n[3/3] Saving dataset...")
output_csv = Path("/app/sandbox/session_20260102_222825_9c4bac117ac1/data/chemicals_dataset.csv")
output_json = Path("/app/sandbox/session_20260102_222825_9c4bac117ac1/data/chemicals_dataset.json")

df.to_csv(output_csv, index=False)
print(f"  ✓ Saved to: {output_csv}")

# Also save as JSON for reference
with open(output_json, 'w') as f:
    json.dump(chemicals_data, f, indent=2)
print(f"  ✓ Saved to: {output_json}")

print("\n" + "="*80)
print("CHEMICAL DATA COLLECTION COMPLETE")
print("="*80)

# Display sample
print("\nDataset preview (first 5 materials):")
print(df[['material', 'abbrev', 'repeat_unit', 'molecular_weight', 'biodegradable', 'persistence_score']].head().to_string(index=False))

print(f"\n✓ Ready for molecular mapping and UBP analysis")
