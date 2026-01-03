#!/usr/bin/env python3
"""
Step 4: UBP Analysis Pipeline
Processes all chemicals through UBP Core v4.2.6 and extracts metrics.
"""

import sys
from pathlib import Path
import pandas as pd
import json
import hashlib

# Add UBP system to path
ubp_path = Path("/app/sandbox/session_20260102_222825_9c4bac117ac1/user_data/UBP_v4.2.6_Polished/ubp_clean")
sys.path.insert(0, str(ubp_path))

from ubp_phenomenology_v4_2_6 import PhenomenologyEngine, PhenomenonDefinition

print("="*80)
print("STEP 4: UBP ANALYSIS PIPELINE")
print("="*80)

# Define the molecular resonance bit generator (same as step 3)
def molecular_resonance_bits(data: dict) -> list:
    """Convert chemical data to 24-bit substrate identity."""
    atoms = data.get('formula_atoms', {})
    mw = data.get('molecular_weight', 0)
    formula = data.get('repeat_unit', '')

    # Bits 0-7: Atomic Composition
    total_atoms = sum(atoms.get(a, 0) for a in ['C', 'H', 'O', 'N', 'Cl', 'S', 'F'])
    if total_atoms == 0:
        total_atoms = 1

    c_ratio = atoms.get('C', 0) / total_atoms
    h_ratio = atoms.get('H', 0) / total_atoms
    o_ratio = atoms.get('O', 0) / total_atoms
    n_ratio = atoms.get('N', 0) / total_atoms

    c_quant = min(3, int(c_ratio * 4))
    h_quant = min(3, int(h_ratio * 4))
    o_quant = min(3, int(o_ratio * 4))
    n_quant = min(3, int(n_ratio * 4))

    composition_byte = (c_quant << 6) | (h_quant << 4) | (o_quant << 2) | n_quant
    composition_bits = [(composition_byte >> i) & 1 for i in range(7, -1, -1)]

    # Bits 8-15: Molecular Weight
    max_mw = 400.0
    mw_normalized = min(255, int((mw / max_mw) * 255))
    mw_bits = [(mw_normalized >> i) & 1 for i in range(7, -1, -1)]

    # Bits 16-23: Structure Hash
    formula_hash = hashlib.sha256(formula.encode()).hexdigest()
    hash_byte = int(formula_hash[:2], 16)
    structure_bits = [(hash_byte >> i) & 1 for i in range(7, -1, -1)]

    return composition_bits + mw_bits + structure_bits

# Create phenomenon definition
DEF_MOLECULAR_RESONANCE = PhenomenonDefinition(
    name="Molecular Resonance",
    domain="Chemistry",
    bit_generator=molecular_resonance_bits,
    tags=["chemistry", "polymers", "materials"],
    version="1.0.0"
)

print("\n[1/4] Loading chemical dataset...")
dataset_path = Path("/app/sandbox/session_20260102_222825_9c4bac117ac1/data/chemicals_dataset.csv")
df = pd.read_csv(dataset_path)

# Parse formula_atoms back from string representation
df['formula_atoms'] = df['formula_atoms'].apply(eval)

print(f"  ✓ Loaded {len(df)} chemicals")

print("\n[2/4] Initializing UBP Phenomenology Engine...")
engine = PhenomenologyEngine()
print(f"  ✓ Engine initialized")

print("\n[3/4] Processing chemicals through UBP Core...")
results = []
full_results = []

for idx, row in df.iterrows():
    print(f"\n  [{idx+1}/{len(df)}] Processing: {row['material']} ({row['abbrev']})")

    # Prepare data for bit generator
    chemical_data = {
        'formula_atoms': row['formula_atoms'],
        'molecular_weight': row['molecular_weight'],
        'repeat_unit': row['repeat_unit']
    }

    # Process through UBP system
    result = engine.process_phenomenon(DEF_MOLECULAR_RESONANCE, chemical_data)

    # Store key metrics
    metrics_summary = {
        'material': row['material'],
        'abbrev': row['abbrev'],
        'repeat_unit': row['repeat_unit'],
        'molecular_weight': row['molecular_weight'],
        'category': row['category'],
        'biodegradable': row['biodegradable'],
        'environmental_persistence': row['environmental_persistence'],
        'persistence_score': row['persistence_score'],
        'toxicity_score': row['toxicity_score'],
        'substrate_identity': ''.join(map(str, result['substrate_identity'])),
        'nrci': float(result['metrics']['nrci']),
        'coherence_regime': result['metrics']['coherence'],
        'symmetry_tax': float(result['metrics']['symmetry_tax']),
        'stability_score': float(result['metrics']['stability_score']),
        'hex_id': result['memory']['hex_id'][:16]  # Shortened for readability
    }

    results.append(metrics_summary)
    full_results.append(result)

    # Progress indicator
    if (idx + 1) % 5 == 0:
        print(f"    Progress: {idx+1}/{len(df)} chemicals processed...")

print(f"\n  ✓ All {len(df)} chemicals processed successfully")

print("\n[4/4] Saving results...")

# Save metrics as CSV
metrics_df = pd.DataFrame(results)
metrics_csv = Path("/app/sandbox/session_20260102_222825_9c4bac117ac1/data/ubp_metrics.csv")
metrics_df.to_csv(metrics_csv, index=False)
print(f"  ✓ Metrics saved to: {metrics_csv}")

# Save full results as JSON
full_json = Path("/app/sandbox/session_20260102_222825_9c4bac117ac1/data/ubp_results_full.json")
with open(full_json, 'w') as f:
    # Convert numpy types to Python types for JSON serialization
    json_results = []
    for r in full_results:
        json_r = r.copy()
        json_r['metrics'] = {
            k: float(v) if isinstance(v, (int, float)) else str(v)
            for k, v in json_r['metrics'].items()
        }
        json_results.append(json_r)
    json.dump(json_results, f, indent=2)
print(f"  ✓ Full results saved to: {full_json}")

print("\n" + "="*80)
print("UBP ANALYSIS COMPLETE")
print("="*80)

print("\nKey Statistics:")
print(f"  • Total materials analyzed: {len(df)}")
print(f"  • NRCI range: {metrics_df['nrci'].min():.4f} - {metrics_df['nrci'].max():.4f}")
print(f"  • Symmetry Tax range: {metrics_df['symmetry_tax'].min():.4f} - {metrics_df['symmetry_tax'].max():.4f}")
print(f"  • Stability Score range: {metrics_df['stability_score'].min():.4f} - {metrics_df['stability_score'].max():.4f}")

print("\nTop 5 materials by Stability Score:")
top5 = metrics_df.nlargest(5, 'stability_score')[['material', 'abbrev', 'stability_score', 'biodegradable']]
print(top5.to_string(index=False))

print("\nBottom 5 materials by Stability Score:")
bottom5 = metrics_df.nsmallest(5, 'stability_score')[['material', 'abbrev', 'stability_score', 'biodegradable']]
print(bottom5.to_string(index=False))

print("\n✓ Ready for statistical analysis and visualization")
