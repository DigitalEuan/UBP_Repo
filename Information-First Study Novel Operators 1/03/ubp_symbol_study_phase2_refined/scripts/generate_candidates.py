#!/usr/bin/env python3.11
"""
Rigorous Candidate Symbol Generation
UBP Symbol Study Phase 2 (Refined)

Generates N=100 novel symbol candidates optimized for high predicted coherence
following the three core principles:
1. Zero Ambiguity (single meaning)
2. Minimal Compositionality (≤1 base symbol dependency)
3. High Structural Regularity (fixed arity, clear role)

All generation is deterministic (RANDOM_SEED=42) for reproducibility.
"""

import json
import random
import hashlib
from typing import Dict, List
import math

# Reproducibility
RANDOM_SEED = 42
random.seed(RANDOM_SEED)

# Feature computation functions (matching features_spec.md)

def compute_d1_arity(arity_str: str) -> float:
    """D1: Arity (normalized)"""
    arity_map = {
        "nullary": 0,
        "unary": 1,
        "binary": 2,
        "ternary": 3
    }
    arity_raw = arity_map.get(arity_str, 2)
    return min(arity_raw / 2.0, 1.0)

def compute_d2_formal_role(role: str) -> float:
    """D2: Formal Role (categorical → numeric)"""
    role_map = {
        "operand": 0.00,
        "relation": 0.25,
        "operator": 0.50,
        "quantifier": 0.75,
        "meta": 1.00
    }
    return role_map.get(role, 0.50)

def compute_d3_invertibility(has_inverse: bool, partial: bool = False) -> float:
    """D3: Invertibility (reversibility fraction)"""
    if has_inverse:
        return 1.0
    elif partial:
        return 0.5
    else:
        return 0.0

def compute_d4_commutativity(is_commutative: bool, arity: str) -> float:
    """D4: Commutativity (binary indicator)"""
    if arity in ["binary", "ternary"] and is_commutative:
        return 1.0
    else:
        return 0.0

def compute_d5_meaning_count(meaning_count: int) -> float:
    """D5: Meaning Count (ambiguity, log-normalized)"""
    meaning_count_capped = min(meaning_count, 10)
    return meaning_count_capped / 10.0

def compute_d6_dependency_depth(depth: int, vocab_size: int = 1006) -> float:
    """D6: Dependency Depth (compositional complexity, log-normalized)"""
    if depth == 0:
        return 0.0
    return depth / math.log2(vocab_size)

def compute_d7_closure_degree(closure_type: str) -> float:
    """D7: Closure Degree (normalized)"""
    closure_map = {
        "full": 1.0,
        "partial": 0.5,
        "none": 0.0
    }
    return closure_map.get(closure_type, 0.5)

def compute_d8_overloading_index(d5: float, symbol_entropy: float) -> float:
    """D8: Overloading Index (composite metric)"""
    # For novel symbols, entropy is minimal
    return 0.5 * symbol_entropy + 0.5 * d5

def compute_bitfield(candidate: Dict) -> List[float]:
    """Compute full 8D bitfield for a candidate"""
    d1 = compute_d1_arity(candidate["arity"])
    d2 = compute_d2_formal_role(candidate["formal_role"])
    d3 = compute_d3_invertibility(candidate["has_inverse"], candidate.get("partial_inverse", False))
    d4 = compute_d4_commutativity(candidate["is_commutative"], candidate["arity"])
    d5 = compute_d5_meaning_count(candidate["meaning_count"])
    d6 = compute_d6_dependency_depth(candidate["dependency_depth"])
    d7 = compute_d7_closure_degree(candidate["closure_type"])
    d8 = compute_d8_overloading_index(d5, candidate.get("symbol_entropy", 0.01))
    
    return [d1, d2, d3, d4, d5, d6, d7, d8]

# Candidate generation templates

def generate_commutative_binary_operator(i: int) -> Dict:
    """
    Generate a commutative binary operator with minimal ambiguity.
    Principle 1: Single meaning (meaning_count=1)
    Principle 2: Minimal composition (dependency_depth=1)
    Principle 3: High regularity (fixed arity=binary, commutative=True)
    """
    # Use extended Unicode mathematical operators
    glyphs = ["⊕", "⊗", "⊙", "⊚", "⊛", "⊜", "⊝", "⊞", "⊟", "⊠",
              "⊡", "⋄", "⋆", "⋇", "⋈", "⋉", "⋊", "⋋", "⋌", "⋍"]
    
    glyph = glyphs[i % len(glyphs)] + f"_{i//len(glyphs)}" if i >= len(glyphs) else glyphs[i]
    
    # Define operation using minimal base symbols
    operations = [
        ("symmetric_sum", "a ⊕ b := (a + b) / 2", "Symmetric arithmetic mean"),
        ("symmetric_product", "a ⊗ b := √(a × b)", "Geometric mean"),
        ("harmonic_combine", "a ⊙ b := 2ab/(a + b)", "Harmonic mean"),
        ("balanced_max", "a ⊚ b := (a + b + |a - b|) / 2", "Maximum via absolute value"),
        ("balanced_min", "a ⊛ b := (a + b - |a - b|) / 2", "Minimum via absolute value"),
    ]
    
    op_name, op_def, op_desc = operations[i % len(operations)]
    
    return {
        "id": f"cand_{i:03d}",
        "glyph": glyph,
        "latex": f"\\newop{{{op_name}_{i}}}",
        "name": f"{op_name}_{i}",
        "meaning": f"{op_desc} (novel operator {i})",
        "definition": op_def,
        "arity": "binary",
        "formal_role": "operator",
        "has_inverse": False,
        "partial_inverse": False,
        "is_commutative": True,
        "meaning_count": 1,  # Single, well-defined meaning
        "dependency_depth": 1,  # Uses only +, ×, /, √ (depth=1)
        "closure_type": "full",  # ℝ × ℝ → ℝ
        "symbol_entropy": 0.01,  # Novel symbol, minimal corpus presence
        "category": "novel_high_coherence"
    }

def generate_non_commutative_binary_operator(i: int) -> Dict:
    """
    Generate a non-commutative binary operator with minimal ambiguity.
    Tests whether commutativity affects coherence as predicted.
    """
    glyphs = ["⊲", "⊳", "⊴", "⊵", "⋐", "⋑", "⋒", "⋓", "⋔", "⋕"]
    
    glyph = glyphs[i % len(glyphs)] + f"_{i//len(glyphs)}" if i >= len(glyphs) else glyphs[i]
    
    operations = [
        ("left_weighted_mean", "a ⊲ b := (2a + b) / 3", "Left-weighted arithmetic mean"),
        ("right_weighted_mean", "a ⊳ b := (a + 2b) / 3", "Right-weighted arithmetic mean"),
        ("forward_difference", "a ⊴ b := (b - a) / a", "Normalized forward difference"),
        ("backward_difference", "a ⊵ b := (a - b) / b", "Normalized backward difference"),
    ]
    
    op_name, op_def, op_desc = operations[i % len(operations)]
    
    return {
        "id": f"cand_{i:03d}",
        "glyph": glyph,
        "latex": f"\\newop{{{op_name}_{i}}}",
        "name": f"{op_name}_{i}",
        "meaning": f"{op_desc} (novel operator {i})",
        "definition": op_def,
        "arity": "binary",
        "formal_role": "operator",
        "has_inverse": False,
        "partial_inverse": False,
        "is_commutative": False,
        "meaning_count": 1,
        "dependency_depth": 1,
        "closure_type": "full",
        "symbol_entropy": 0.01,
        "category": "novel_high_coherence"
    }

def generate_unary_operator(i: int) -> Dict:
    """
    Generate a unary operator with minimal ambiguity.
    Lower arity should correlate with higher coherence.
    """
    glyphs = ["◯", "◉", "◎", "●", "◐", "◑", "◒", "◓", "◔", "◕"]
    
    glyph = glyphs[i % len(glyphs)] + f"_{i//len(glyphs)}" if i >= len(glyphs) else glyphs[i]
    
    operations = [
        ("double", "◯(a) := 2a", "Doubling function"),
        ("half", "◉(a) := a/2", "Halving function"),
        ("square_plus_one", "◎(a) := a² + 1", "Square plus one"),
        ("reciprocal_plus_one", "●(a) := 1/a + 1", "Reciprocal plus one"),
    ]
    
    op_name, op_def, op_desc = operations[i % len(operations)]
    
    return {
        "id": f"cand_{i:03d}",
        "glyph": glyph,
        "latex": f"\\newop{{{op_name}_{i}}}",
        "name": f"{op_name}_{i}",
        "meaning": f"{op_desc} (novel operator {i})",
        "definition": op_def,
        "arity": "unary",
        "formal_role": "operator",
        "has_inverse": False,
        "partial_inverse": False,
        "is_commutative": False,  # N/A for unary
        "meaning_count": 1,
        "dependency_depth": 1,
        "closure_type": "full",
        "symbol_entropy": 0.01,
        "category": "novel_high_coherence"
    }

def generate_relation(i: int) -> Dict:
    """
    Generate a binary relation with minimal ambiguity.
    Relations have different formal role (D2=0.25).
    """
    glyphs = ["≈", "≋", "≌", "≍", "≎", "≏", "≐", "≑", "≒", "≓"]
    
    glyph = glyphs[i % len(glyphs)] + f"_{i//len(glyphs)}" if i >= len(glyphs) else glyphs[i]
    
    relations = [
        ("epsilon_equal", "a ≈ b ⟺ |a - b| < ε", "Epsilon-equality relation"),
        ("ratio_close", "a ≋ b ⟺ |a/b - 1| < δ", "Ratio-closeness relation"),
        ("sum_equal", "a ≌ b ⟺ a + b = 2c (for fixed c)", "Sum-equality relation"),
        ("product_equal", "a ≍ b ⟺ a × b = k (for fixed k)", "Product-equality relation"),
    ]
    
    rel_name, rel_def, rel_desc = relations[i % len(relations)]
    
    return {
        "id": f"cand_{i:03d}",
        "glyph": glyph,
        "latex": f"\\newrel{{{rel_name}_{i}}}",
        "name": f"{rel_name}_{i}",
        "meaning": f"{rel_desc} (novel relation {i})",
        "definition": rel_def,
        "arity": "binary",
        "formal_role": "relation",
        "has_inverse": False,
        "partial_inverse": False,
        "is_commutative": True,  # Most relations are symmetric
        "meaning_count": 1,
        "dependency_depth": 1,
        "closure_type": "none",  # Relations return boolean
        "symbol_entropy": 0.01,
        "category": "novel_high_coherence"
    }

def generate_all_candidates(n: int = 100) -> List[Dict]:
    """
    Generate N candidates with balanced distribution across types.
    
    Distribution:
    - 40% commutative binary operators
    - 30% non-commutative binary operators
    - 20% unary operators
    - 10% relations
    """
    candidates = []
    
    # Commutative binary operators (40)
    for i in range(40):
        candidates.append(generate_commutative_binary_operator(i))
    
    # Non-commutative binary operators (30)
    for i in range(30):
        candidates.append(generate_non_commutative_binary_operator(i))
    
    # Unary operators (20)
    for i in range(20):
        candidates.append(generate_unary_operator(i))
    
    # Relations (10)
    for i in range(10):
        candidates.append(generate_relation(i))
    
    # Reindex IDs
    for idx, cand in enumerate(candidates):
        cand["id"] = f"cand_{idx:03d}"
    
    # Compute bitfields
    for cand in candidates:
        bitfield = compute_bitfield(cand)
        cand["bitfield"] = bitfield
        cand["D1"] = bitfield[0]
        cand["D2"] = bitfield[1]
        cand["D3"] = bitfield[2]
        cand["D4"] = bitfield[3]
        cand["D5"] = bitfield[4]
        cand["D6"] = bitfield[5]
        cand["D7"] = bitfield[6]
        cand["D8"] = bitfield[7]
    
    return candidates

def compute_deterministic_hash(candidate: Dict) -> str:
    """Compute deterministic hash for candidate verification"""
    # Hash based on definition and bitfield
    hash_input = f"{candidate['definition']}|{candidate['bitfield']}"
    return hashlib.sha256(hash_input.encode()).hexdigest()[:16]

def main():
    """Generate and save candidates"""
    print("="*60)
    print("RIGOROUS CANDIDATE GENERATION")
    print("="*60)
    print(f"Random seed: {RANDOM_SEED}")
    print(f"Target count: 100 candidates")
    print()
    
    # Generate candidates
    candidates = generate_all_candidates(100)
    
    # Add hashes for verification
    for cand in candidates:
        cand["verification_hash"] = compute_deterministic_hash(cand)
    
    # Statistics
    print(f"Generated {len(candidates)} candidates")
    print()
    print("Distribution:")
    print(f"  Commutative binary operators: {sum(1 for c in candidates if c['is_commutative'] and c['arity'] == 'binary')}")
    print(f"  Non-commutative binary operators: {sum(1 for c in candidates if not c['is_commutative'] and c['arity'] == 'binary')}")
    print(f"  Unary operators: {sum(1 for c in candidates if c['arity'] == 'unary')}")
    print(f"  Relations: {sum(1 for c in candidates if c['formal_role'] == 'relation')}")
    print()
    
    # Feature statistics
    print("Feature statistics (D1-D8):")
    for i in range(8):
        values = [c[f"D{i+1}"] for c in candidates]
        print(f"  D{i+1}: mean={sum(values)/len(values):.3f}, min={min(values):.3f}, max={max(values):.3f}")
    print()
    
    # Save to JSON
    output_path = "/home/ubuntu/ubp_symbol_study_phase2_refined/candidates/candidates_n100.json"
    with open(output_path, 'w') as f:
        json.dump(candidates, f, indent=2)
    
    print(f"Saved to: {output_path}")
    print()
    print("="*60)
    print("GENERATION COMPLETE")
    print("="*60)

if __name__ == "__main__":
    main()
