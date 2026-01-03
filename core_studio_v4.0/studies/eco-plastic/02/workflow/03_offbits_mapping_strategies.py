#!/usr/bin/env python3
"""
OffBits Mapping Strategies - The Revolutionary Approach
=========================================================
Focus on what's MISSING (OffBits = 0) rather than what's present (OnBits = 1)

This is the core innovation: Traditional fingerprints ask "What features does
this molecule have?" OffBits ask "What features is this molecule MISSING?"

For environmental persistence, biodegradability, and toxicity, what matters
is often what's ABSENT (protective groups, degradable linkages, reactive sites)
"""

import sys
import json
import numpy as np
import pandas as pd
from pathlib import Path
from typing import Dict, List, Tuple
import hashlib

BASE_DIR = Path("/app/sandbox/session_20260102_222825_9c4bac117ac1")

print("=" * 70)
print("OFFBITS MAPPING STRATEGIES")
print("=" * 70)

# Load dataset
df = pd.read_csv(BASE_DIR / "data" / "large_chemicals_dataset.csv")
print(f"\nLoaded {len(df)} compounds")

# Set random seed
np.random.seed(42)

# ============================================================================
# STRATEGY 1: ABSENT FUNCTIONAL GROUPS (24-bit)
# ============================================================================
# Bit = 1 if functional group is PRESENT, Bit = 0 if ABSENT
# We analyze OffBits (the 0s) to understand what's missing

def strategy_1_absent_functional_groups(row: pd.Series) -> np.ndarray:
    """
    24-bit fingerprint based on presence/absence of functional groups.
    OffBits (0s) = ABSENT features
    OnBits (1s) = PRESENT features

    Bits 0-23 represent 24 common chemical features
    """
    bits = np.zeros(24, dtype=int)

    # Bits 0-5: Element presence
    bits[0] = 1 if row['carbon'] > 0 else 0
    bits[1] = 1 if row['hydrogen'] > 0 else 0
    bits[2] = 1 if row['oxygen'] > 0 else 0
    bits[3] = 1 if row['nitrogen'] > 0 else 0
    bits[4] = 1 if row['chlorine'] > 0 else 0
    bits[5] = 1 if row['fluorine'] > 0 else 0

    # Bits 6-11: Functional group presence
    bits[6] = row['aromatic']
    bits[7] = row['ester']
    bits[8] = row['amide']
    bits[9] = row['ether']
    bits[10] = row['halogen']
    bits[11] = 1 if row['mw'] > 100 else 0  # High molecular weight

    # Bits 12-17: Structural characteristics (inferred)
    bits[12] = 1 if row['C_ratio'] > 0.5 else 0  # Carbon-rich
    bits[13] = 1 if row['H_ratio'] > 0.5 else 0  # Hydrogen-rich
    bits[14] = 1 if row['heteroatom_ratio'] > 0.2 else 0  # Heteroatom-rich
    bits[15] = 1 if row['carbon'] > 6 else 0  # Large carbon skeleton
    bits[16] = 1 if row['mw'] > 200 else 0  # Very high MW
    bits[17] = 1 if row['total_atoms'] > 15 else 0  # Complex structure

    # Bits 18-23: Property indicators
    bits[18] = 1 if row['biodegradable'] < 0.3 else 0  # Persistent (NOT biodegradable)
    bits[19] = 1 if row['toxic'] > 0.5 else 0  # Toxic
    bits[20] = 1 if row['persistent'] > 0.7 else 0  # Environmentally persistent
    bits[21] = 1 if row['aromatic'] == 1 and row['halogen'] == 1 else 0  # Aromatic + Halogen (very persistent)
    bits[22] = 1 if row['ester'] == 1 or row['amide'] == 1 else 0  # Has degradable linkages
    bits[23] = 1 if row['oxygen'] > 0 or row['nitrogen'] > 0 else 0  # Has heteroatoms (potential reactivity)

    return bits


# ============================================================================
# STRATEGY 2: INVERTED PROTECTION FEATURES (focus on LACK of protective groups)
# ============================================================================

def strategy_2_lack_of_protection(row: pd.Series) -> np.ndarray:
    """
    24-bit fingerprint specifically designed to capture ABSENCE of protective features.
    OffBits (0s) = Protective features that are MISSING

    Hypothesis: Persistent/toxic chemicals LACK protective mechanisms
    """
    bits = np.zeros(24, dtype=int)

    # Bits 0-7: LACK of degradation pathways (OffBit = lacks pathway)
    bits[0] = 0 if row['ester'] == 1 else 1  # LACKS ester linkage (hydrolyzable)
    bits[1] = 0 if row['amide'] == 1 else 1  # LACKS amide linkage
    bits[2] = 0 if row['ether'] == 1 else 1  # LACKS ether linkage
    bits[3] = 0 if row['oxygen'] > 0 else 1  # LACKS oxygen (oxidation sites)
    bits[4] = 0 if row['nitrogen'] > 0 else 1  # LACKS nitrogen (reactive sites)
    bits[5] = 0 if row['H_ratio'] > 0.4 else 1  # LACKS hydrogen (metabolic handle)
    bits[6] = 0 if row['aromatic'] == 0 else 1  # HAS aromatic (stable, hard to degrade)
    bits[7] = 0 if row['halogen'] == 0 else 1  # HAS halogen (persistent, toxic)

    # Bits 8-15: LACK of reactivity indicators
    bits[8] = 0 if (row['oxygen'] + row['nitrogen']) > 2 else 1  # LACKS multiple heteroatoms
    bits[9] = 0 if row['heteroatom_ratio'] > 0.25 else 1  # LACKS heteroatom diversity
    bits[10] = 0 if row['carbon'] < 10 else 1  # HAS long carbon chain (lipophilic)
    bits[11] = 0 if row['mw'] < 150 else 1  # HAS high MW (hard to eliminate)
    bits[12] = 1 if row['halogen'] == 1 and row['aromatic'] == 1 else 0  # Worst combo
    bits[13] = 1 if row['halogen'] == 1 and row['carbon'] > 6 else 0  # Halogenated organic
    bits[14] = 1 if row['persistent'] > 0.8 else 0  # Known to be persistent
    bits[15] = 1 if row['toxic'] > 0.7 else 0  # Known to be toxic

    # Bits 16-23: Molecular simplicity/complexity (affects biodegradation)
    bits[16] = 1 if row['total_atoms'] < 5 else 0  # Too simple
    bits[17] = 1 if row['total_atoms'] > 30 else 0  # Too complex
    bits[18] = 1 if row['C_ratio'] > 0.7 else 0  # Carbon-dominated (lipophilic)
    bits[19] = 1 if row['oxygen'] == 0 and row['nitrogen'] == 0 else 0  # Pure hydrocarbon/halogenated
    bits[20] = 1 if row['biodegradable'] < 0.2 else 0  # Very persistent
    bits[21] = 1 if row['category'] in ['pollutant', 'flame_retardant'] else 0  # Known bad actors
    bits[22] = 1 if row['chlorine'] > 2 else 0  # Heavily chlorinated
    bits[23] = 1 if row['fluorine'] > 2 else 0  # Heavily fluorinated

    return bits


# ============================================================================
# STRATEGY 3: BALANCED OnBit/OffBit RATIO (UBP-aligned)
# ============================================================================

def strategy_3_balanced_substrate(row: pd.Series) -> np.ndarray:
    """
    24-bit fingerprint designed to create balanced patterns.
    Inspired by UBP's Golay code balance (Hamming Weight ~12)
    """
    bits = np.zeros(24, dtype=int)

    # Hash-based distribution for balance
    hash_input = f"{row['name']}_{row['formula']}_{row['mw']}"
    hash_obj = hashlib.sha256(hash_input.encode())
    hash_bytes = hash_obj.digest()

    # First 12 bits: Molecular features
    bits[0] = 1 if row['carbon'] > 3 else 0
    bits[1] = 1 if row['hydrogen'] > 6 else 0
    bits[2] = 1 if row['oxygen'] > 0 else 0
    bits[3] = 1 if row['nitrogen'] > 0 else 0
    bits[4] = 1 if row['halogen'] == 1 else 0
    bits[5] = 1 if row['aromatic'] == 1 else 0
    bits[6] = 1 if row['ester'] == 1 or row['amide'] == 1 else 0
    bits[7] = 1 if row['mw'] > 100 else 0
    bits[8] = 1 if row['total_atoms'] > 10 else 0
    bits[9] = 1 if row['heteroatom_ratio'] > 0.2 else 0
    bits[10] = 1 if row['persistent'] > 0.5 else 0
    bits[11] = 1 if row['toxic'] > 0.4 else 0

    # Last 12 bits: Hash-based (for diversity and balance)
    for i in range(12):
        bits[12 + i] = hash_bytes[i] % 2

    return bits


# ============================================================================
# STRATEGY 4: ENVIRONMENTAL PERSISTENCE SIGNATURE
# ============================================================================

def strategy_4_persistence_signature(row: pd.Series) -> np.ndarray:
    """
    24-bit fingerprint specifically tuned for environmental persistence.
    OffBits represent LACK of degradation mechanisms.
    """
    bits = np.zeros(24, dtype=int)

    # Bits 0-7: Degradation resistance factors (1 = has resistance factor)
    bits[0] = 1 if row['aromatic'] == 1 else 0  # Aromatic = stable
    bits[1] = 1 if row['halogen'] == 1 else 0  # Halogenated = persistent
    bits[2] = 1 if row['chlorine'] > 0 else 0  # Chlorinated
    bits[3] = 1 if row['fluorine'] > 0 else 0  # Fluorinated (extremely stable)
    bits[4] = 1 if row['ester'] == 0 and row['amide'] == 0 else 0  # No degradable links
    bits[5] = 1 if row['oxygen'] == 0 else 0  # No oxygen (oxidation resistance)
    bits[6] = 1 if row['C_ratio'] > 0.6 else 0  # Carbon-rich (hydrophobic)
    bits[7] = 1 if row['mw'] > 150 else 0  # High MW (harder to eliminate)

    # Bits 8-15: Degradation pathways present (1 = has pathway, 0 = lacks it)
    bits[8] = 1 if row['ester'] == 1 else 0  # Ester hydrolysis
    bits[9] = 1 if row['amide'] == 1 else 0  # Amide hydrolysis
    bits[10] = 1 if row['ether'] == 1 else 0  # Ether cleavage
    bits[11] = 1 if row['oxygen'] > 1 else 0  # Multiple oxygen attack sites
    bits[12] = 1 if row['nitrogen'] > 0 else 0  # Nitrogen metabolic handle
    bits[13] = 1 if row['H_ratio'] > 0.5 else 0  # Hydrogen-rich (metabolizable)
    bits[14] = 1 if row['heteroatom_ratio'] > 0.3 else 0  # Heteroatom-rich
    bits[15] = 1 if row['aromatic'] == 0 else 0  # Aliphatic (more degradable)

    # Bits 16-23: Known persistence indicators
    bits[16] = 1 if row['persistent'] > 0.8 else 0
    bits[17] = 1 if row['persistent'] > 0.6 else 0
    bits[18] = 1 if row['persistent'] > 0.4 else 0
    bits[19] = 1 if row['biodegradable'] < 0.2 else 0
    bits[20] = 1 if row['biodegradable'] < 0.4 else 0
    bits[21] = 1 if row['biodegradable'] < 0.6 else 0
    bits[22] = 1 if row['category'] in ['pollutant', 'plastic_commodity', 'flame_retardant'] else 0
    bits[23] = 1 if row['halogen'] == 1 and row['aromatic'] == 1 else 0  # Worst combination

    return bits


# ============================================================================
# APPLY ALL STRATEGIES
# ============================================================================

print("\n[1/3] Applying mapping strategies...")

strategies = {
    "strategy_1_functional_groups": strategy_1_absent_functional_groups,
    "strategy_2_lack_protection": strategy_2_lack_of_protection,
    "strategy_3_balanced": strategy_3_balanced_substrate,
    "strategy_4_persistence": strategy_4_persistence_signature,
}

results = {}
for strategy_name, strategy_func in strategies.items():
    print(f"   Applying {strategy_name}...")
    fingerprints = []
    offbit_counts = []
    onbit_counts = []

    for idx, row in df.iterrows():
        bits = strategy_func(row)
        fingerprints.append(bits)
        offbit_counts.append(np.sum(bits == 0))  # Count of 0s (OffBits)
        onbit_counts.append(np.sum(bits == 1))  # Count of 1s (OnBits)

    results[strategy_name] = {
        "fingerprints": np.array(fingerprints),
        "offbit_counts": np.array(offbit_counts),
        "onbit_counts": np.array(onbit_counts)
    }

    print(f"      OffBits (0s): mean={np.mean(offbit_counts):.2f}, std={np.std(offbit_counts):.2f}")
    print(f"      OnBits (1s): mean={np.mean(onbit_counts):.2f}, std={np.std(onbit_counts):.2f}")

# ============================================================================
# SAVE FINGERPRINTS
# ============================================================================

print("\n[2/3] Saving fingerprints...")
for strategy_name, data in results.items():
    # Save as numpy array
    np_file = BASE_DIR / "data" / "fingerprints" / f"{strategy_name}.npy"
    np.save(np_file, data["fingerprints"])

    # Save bit counts to CSV
    bit_counts_df = pd.DataFrame({
        "compound_id": df.index,
        "compound_name": df["name"],
        "offbits": data["offbit_counts"],
        "onbits": data["onbit_counts"],
        "hamming_weight": data["onbit_counts"],  # Same as onbits
    })
    csv_file = BASE_DIR / "data" / "fingerprints" / f"{strategy_name}_counts.csv"
    bit_counts_df.to_csv(csv_file, index=False)
    print(f"   ✓ {strategy_name}: {np_file.name}")

# ============================================================================
# GENERATE SUMMARY
# ============================================================================

print("\n[3/3] Generating summary...")
summary = {
    "num_compounds": len(df),
    "strategies": {}
}

for strategy_name, data in results.items():
    fps = data["fingerprints"]
    summary["strategies"][strategy_name] = {
        "fingerprint_shape": fps.shape,
        "offbits_mean": float(np.mean(data["offbit_counts"])),
        "offbits_std": float(np.std(data["offbit_counts"])),
        "onbits_mean": float(np.mean(data["onbit_counts"])),
        "onbits_std": float(np.std(data["onbit_counts"])),
        "unique_fingerprints": int(len(np.unique(fps, axis=0))),
        "diversity": float(len(np.unique(fps, axis=0)) / len(fps))
    }

summary_file = BASE_DIR / "data" / "fingerprints" / "strategies_summary.json"
with open(summary_file, 'w') as f:
    json.dump(summary, f, indent=2)

print(f"✓ Summary saved to: {summary_file}")
print("\n" + "=" * 70)
print("✓ OFFBITS MAPPING COMPLETE")
print("=" * 70)
print(f"\nGenerated {len(strategies)} fingerprint strategies for {len(df)} compounds")
print("Next: Run 04_jaccard_hamming_analysis.py")
