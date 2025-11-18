#!/usr/bin/env python3.11
"""
Re-normalize Baseline Dataset
UBP Symbol Study Phase 2 (Refined)

This script re-processes the original 1006-symbol baseline dataset
using the new, rigorous D-variable definitions from features_spec.md.

This ensures an apples-to-apples comparison between the baseline
and the novel candidates.

Author: Manus AI
Date: Nov 18, 2025
"""

import json
import math
import numpy as np
from typing import Dict, List

# --- D-Variable Computation Functions (from features_spec.md) ---

def compute_d1_arity(arity_str: str) -> float:
    arity_map = {"nullary": 0, "unary": 1, "binary": 2, "ternary": 3}
    arity_raw = arity_map.get(arity_str.lower(), 2)
    return min(arity_raw / 2.0, 1.0)

def compute_d2_formal_role(role: str) -> float:
    role_map = {"operand": 0.0, "relation": 0.25, "operator": 0.5, "quantifier": 0.75, "meta": 1.0}
    return role_map.get(role.lower(), 0.5)

def compute_d3_invertibility(has_inverse: bool, partial: bool = False) -> float:
    return 1.0 if has_inverse else 0.5 if partial else 0.0

def compute_d4_commutativity(is_commutative: bool, arity: str) -> float:
    return 1.0 if arity.lower() in ["binary", "ternary"] and is_commutative else 0.0

def compute_d5_meaning_count(meaning_count: int) -> float:
    return min(meaning_count, 10) / 10.0

def compute_d6_dependency_depth(depth: int, vocab_size: int = 1006) -> float:
    return depth / math.log2(vocab_size) if depth > 0 else 0.0

def compute_d7_closure_degree(closure_type: str) -> float:
    closure_map = {"full": 1.0, "partial": 0.5, "none": 0.0}
    return closure_map.get(closure_type.lower(), 0.5)

def compute_d8_overloading_index(d5: float, symbol_entropy: float = 0.1) -> float:
    return 0.5 * symbol_entropy + 0.5 * d5

def compute_bitfield_for_symbol(symbol: Dict) -> List[float]:
    """Compute the full 8D bitfield for a symbol from the baseline dataset."""
    d1 = compute_d1_arity(symbol.get("arity", "binary"))
    d2 = compute_d2_formal_role(symbol.get("formal_role", "operator"))
    d3 = compute_d3_invertibility(symbol.get("has_inverse", False), symbol.get("partial_inverse", False))
    d4 = compute_d4_commutativity(symbol.get("is_commutative", False), symbol.get("arity", "binary"))
    d5 = compute_d5_meaning_count(symbol.get("meaning_count", 1))
    d6 = compute_d6_dependency_depth(symbol.get("dependency_depth", 1))
    d7 = compute_d7_closure_degree(symbol.get("closure_type", "full"))
    d8 = compute_d8_overloading_index(d5, symbol.get("symbol_entropy", 0.1))
    return [d1, d2, d3, d4, d5, d6, d7, d8]

def main():
    """Load, re-normalize, and save the baseline dataset."""
    print("="*70)
    print("RE-NORMALIZING BASELINE DATASET")
    print("="*70)

    # Load original raw dataset
    original_path = "/home/ubuntu/ubp_symbol_study_phase2/data/symbols_dataset_phase2.json"
    with open(original_path, 'r') as f:
        original_data = json.load(f)
    print(f"Loaded {len(original_data)} symbols from original dataset.")

    # Load processed dataset to get the NRCI values
    processed_path = "/home/ubuntu/ubp_symbol_study_phase2/data/symbols_processed.json"
    with open(processed_path, 'r') as f:
        processed_data = {item["name"]: item for item in json.load(f)}
    print(f"Loaded {len(processed_data)} symbols with NRCI values.")

    normalized_baseline = []
    for symbol in original_data:
        symbol_id = symbol["name"]
        if symbol_id not in processed_data:
            continue

        # Compute new, rigorous bitfield
        new_bitfield = compute_bitfield_for_symbol(symbol)
        
        # Create the new record
        new_record = processed_data[symbol_id].copy()
        
        # Update bitfield_d* keys
        for i, val in enumerate(new_bitfield):
            new_record[f"bitfield_d{i+1}"] = val
        
        normalized_baseline.append(new_record)

    print(f"\nSuccessfully re-normalized {len(normalized_baseline)} symbols.")

    # Save the new normalized baseline
    output_path = "/home/ubuntu/ubp_symbol_study_phase2_refined/data/baseline_normalized.json"
    with open(output_path, 'w') as f:
        json.dump(normalized_baseline, f, indent=2)
    print(f"Saved normalized baseline to: {output_path}")

    # Verify D-values
    df = pd.DataFrame(normalized_baseline)
    print("\nVerification of D-variable ranges in new baseline:")
    for i in range(8):
        col = f"bitfield_d{i+1}"
        print(f"  {col}: min={df[col].min():.3f}, max={df[col].max():.3f}")

    print("\n" + "="*70)
    print("NORMALIZATION COMPLETE")
    print("="*70)

if __name__ == "__main__":
    import pandas as pd
    main()
