import json
import hashlib
from fractions import Fraction
import sys
import os

# Add the core directory to path
sys.path.append('core_studio_v4.0/core')

# UBP Core Imports
try:
    from ubp_unified_v5 import GOLAY_ENGINE, LEECH_ENGINE
except ImportError:
    print("Error: Could not import ubp_unified_v5. Ensure you are running from the root.")
    sys.exit(1)

def generate_operator_entry(op_id, word, definition, math_dna):
    """SOP_002 compliant entry generator."""
    fp = hashlib.sha256(math_dna.encode()).hexdigest()
    # Generate a vector that represents 'Distance' logic (Weight 12 - Dodecad)
    # We use a specific seed for 'Relational' operators
    seed = [1,1,0,0, 1,1,0,0, 1,1,0,0] # 12-bit pattern for 'Connection'
    # GOLAY_ENGINE.encode expects a 12-bit seed
    vector = GOLAY_ENGINE.encode(seed)

    tax = LEECH_ENGINE.calculate_symmetry_tax(vector)
    # Use float for the final score if needed, but keeping user logic
    nrci = Fraction(10, 1) / (Fraction(10, 1) + tax)

    return fp, [
        op_id,
        f"[Operator: {word}], [{definition}]",
        ["OPERATOR", "RELATIONAL", "HARDENED", "SOP_002", "TOPOLOGICAL_V8"],
        vector,
        f"{nrci.numerator}/{nrci.denominator}",
        round(float(nrci), 6),
        f"{tax.numerator}/{tax.denominator}",
        [0] * 24 # Empty MOG Tensor for now
    ]

def run_glm_expansion():
    print("--- GLM EXPANSION: PHASE-LOCKING RELATIONSHIPS ---")

    kb_path = 'core_studio_v4.0/core/ubp_lang_kb_combined_v4.json'
    if not os.path.exists(kb_path):
        print(f"Error: {kb_path} not found.")
        return

    with open(kb_path, 'r') as f:
        lang_kb = json.load(f)

    # 1. Define 'relationship' and 'relationships'
    # Math DNA: D=8 (Octad distance) | X=4 (Correction radius)
    rel_dna = "Type=Operator|Logic=HammingDistance|Target=8"

    fp1, entry1 = generate_operator_entry("OP_RELATIONSHIP", "relationship",
        "The geometric distance and symmetry tax shared between two vectors.", rel_dna)

    fp2, entry2 = generate_operator_entry("OP_RELATIONSHIPS", "relationships",
        "Plural form of relationship. Maps multiple vector interactions.", rel_dna)

    # 2. Ingest into Language KB
    lang_kb["entries"][fp1] = entry1
    lang_kb["entries"][fp2] = entry2

    with open(kb_path, 'w') as f:
        json.dump(lang_kb, f, separators=(',', ':'))

    print(f"✅ Phase-Locked: 'relationship' ({fp1[:8]})")
    print(f"✅ Phase-Locked: 'relationships' ({fp2[:8]})")

    # 3. Identify further Gaps
    print("\n--- RECOMMENDED FOCUS AREAS ---")
    recommendations = [
        "1. OP_INTERACTION (How fields overlap)",
        "2. OP_BOND (Symmetry rebate between atoms)",
        "3. OP_SCALE (Mapping lattice units to MeV/eV)",
        "4. OP_STABILITY_COMPARE (Logic to check which NRCI is higher)",
        "5. OP_EVOLVE (Time-based bit-flipping)"
    ]
    for rec in recommendations:
        print(f"  {rec}")

if __name__ == "__main__":
    run_glm_expansion()
