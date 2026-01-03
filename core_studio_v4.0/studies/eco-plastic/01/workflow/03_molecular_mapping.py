#!/usr/bin/env python3
"""
Step 3: Molecular Resonance Mapping
Creates a custom PhenomenonDefinition that maps chemical properties to 24-bit substrate.

Mapping Strategy:
- Bits 0-7:   Atomic composition (C, H, O, N ratios encoded)
- Bits 8-15:  Molecular weight (normalized to 0-255 range)
- Bits 16-23: Chemical structure hash (from formula string)
"""

import sys
from pathlib import Path
import hashlib
import json

# Add UBP system to path
ubp_path = Path("/app/sandbox/session_20260102_222825_9c4bac117ac1/user_data/UBP_v4.2.6_Polished/ubp_clean")
sys.path.insert(0, str(ubp_path))

from ubp_phenomenology_v4_2_6 import PhenomenonDefinition

print("="*80)
print("STEP 3: MOLECULAR RESONANCE MAPPING")
print("="*80)

def molecular_resonance_bits(data: dict) -> list:
    """
    Convert chemical data to 24-bit substrate identity.

    Args:
        data: Dictionary with keys:
            - formula_atoms: dict of atom counts (C, H, O, N, Cl, etc.)
            - molecular_weight: float
            - repeat_unit: string (chemical formula)

    Returns:
        List of 24 integers (0 or 1)
    """

    # Extract data
    atoms = data.get('formula_atoms', {})
    mw = data.get('molecular_weight', 0)
    formula = data.get('repeat_unit', '')

    # ==================================================================
    # BITS 0-7: Atomic Composition (8 bits)
    # Encode ratios of C, H, O, N into 2 bits each
    # ==================================================================

    total_atoms = sum(atoms.get(a, 0) for a in ['C', 'H', 'O', 'N', 'Cl', 'S', 'F'])
    if total_atoms == 0:
        total_atoms = 1

    # Calculate ratios (0.0 to 1.0)
    c_ratio = atoms.get('C', 0) / total_atoms
    h_ratio = atoms.get('H', 0) / total_atoms
    o_ratio = atoms.get('O', 0) / total_atoms
    n_ratio = atoms.get('N', 0) / total_atoms

    # Quantize to 2 bits each (0-3)
    c_quant = min(3, int(c_ratio * 4))  # 2 bits
    h_quant = min(3, int(h_ratio * 4))  # 2 bits
    o_quant = min(3, int(o_ratio * 4))  # 2 bits
    n_quant = min(3, int(n_ratio * 4))  # 2 bits

    # Convert to bits
    composition_byte = (c_quant << 6) | (h_quant << 4) | (o_quant << 2) | n_quant
    composition_bits = [(composition_byte >> i) & 1 for i in range(7, -1, -1)]

    # ==================================================================
    # BITS 8-15: Molecular Weight (8 bits)
    # Normalize MW to 0-255 range (assume max MW = 400 g/mol)
    # ==================================================================

    max_mw = 400.0  # Upper bound for normalization
    mw_normalized = min(255, int((mw / max_mw) * 255))
    mw_bits = [(mw_normalized >> i) & 1 for i in range(7, -1, -1)]

    # ==================================================================
    # BITS 16-23: Structure Hash (8 bits)
    # Hash the chemical formula string to capture structural uniqueness
    # ==================================================================

    formula_hash = hashlib.sha256(formula.encode()).hexdigest()
    hash_byte = int(formula_hash[:2], 16)  # Take first 2 hex chars = 8 bits
    structure_bits = [(hash_byte >> i) & 1 for i in range(7, -1, -1)]

    # ==================================================================
    # Combine all 24 bits
    # ==================================================================

    bits = composition_bits + mw_bits + structure_bits

    assert len(bits) == 24, f"Expected 24 bits, got {len(bits)}"
    return bits


print("\n[1/4] Creating Molecular Resonance definition...")

DEF_MOLECULAR_RESONANCE = PhenomenonDefinition(
    name="Molecular Resonance",
    domain="Chemistry",
    bit_generator=molecular_resonance_bits,
    tags=["chemistry", "polymers", "materials", "molecular"],
    version="1.0.0"
)

print(f"  ✓ Definition created: {DEF_MOLECULAR_RESONANCE.name}")
print(f"    Domain: {DEF_MOLECULAR_RESONANCE.domain}")
print(f"    Tags: {', '.join(DEF_MOLECULAR_RESONANCE.tags)}")

print("\n[2/4] Testing bit generator with sample chemicals...")

test_cases = [
    {
        "name": "Polyethylene (PE)",
        "data": {
            "formula_atoms": {"C": 2, "H": 4, "O": 0, "N": 0, "Cl": 0, "S": 0},
            "molecular_weight": 28.05,
            "repeat_unit": "C2H4"
        }
    },
    {
        "name": "Polyvinyl Chloride (PVC)",
        "data": {
            "formula_atoms": {"C": 2, "H": 3, "O": 0, "N": 0, "Cl": 1, "S": 0},
            "molecular_weight": 62.50,
            "repeat_unit": "C2H3Cl"
        }
    },
    {
        "name": "Polylactic Acid (PLA)",
        "data": {
            "formula_atoms": {"C": 3, "H": 4, "O": 2, "N": 0, "Cl": 0, "S": 0},
            "molecular_weight": 72.06,
            "repeat_unit": "C3H4O2"
        }
    }
]

results = []
for test in test_cases:
    bits = molecular_resonance_bits(test['data'])
    bit_string = ''.join(map(str, bits))

    # Decode for validation
    comp_bits = bits[0:8]
    mw_bits = bits[8:16]
    struct_bits = bits[16:24]

    comp_val = sum(comp_bits[i] * (2 ** (7-i)) for i in range(8))
    mw_val = sum(mw_bits[i] * (2 ** (7-i)) for i in range(8))
    struct_val = sum(struct_bits[i] * (2 ** (7-i)) for i in range(8))

    print(f"\n  {test['name']}:")
    print(f"    24-bit: {bit_string}")
    print(f"    Composition byte: {comp_val:3d} (bits 0-7)")
    print(f"    MW byte:          {mw_val:3d} (bits 8-15, MW={test['data']['molecular_weight']:.2f})")
    print(f"    Structure byte:   {struct_val:3d} (bits 16-23)")

    results.append({
        "material": test['name'],
        "bits": bit_string,
        "composition_value": comp_val,
        "mw_value": mw_val,
        "structure_value": struct_val
    })

print("\n[3/4] Validating bit diversity...")

# Check that different materials produce different bit patterns
unique_patterns = len(set(r['bits'] for r in results))
print(f"  ✓ Unique patterns: {unique_patterns}/{len(results)}")

if unique_patterns == len(results):
    print(f"  ✓ All test materials have unique 24-bit signatures")
else:
    print(f"  ! Warning: Some materials have identical signatures")

print("\n[4/4] Saving definition...")

# Save the definition code for reuse
definition_file = Path("/app/sandbox/session_20260102_222825_9c4bac117ac1/data/molecular_resonance_definition.json")
definition_data = {
    "name": DEF_MOLECULAR_RESONANCE.name,
    "domain": DEF_MOLECULAR_RESONANCE.domain,
    "tags": DEF_MOLECULAR_RESONANCE.tags,
    "version": DEF_MOLECULAR_RESONANCE.version,
    "mapping_strategy": {
        "bits_0_7": "Atomic composition (C, H, O, N ratios quantized to 2 bits each)",
        "bits_8_15": "Molecular weight (normalized to 0-255, max=400 g/mol)",
        "bits_16_23": "Chemical structure hash (SHA-256 of formula string)"
    },
    "test_results": results
}

with open(definition_file, 'w') as f:
    json.dump(definition_data, f, indent=2)

print(f"  ✓ Saved to: {definition_file}")

print("\n" + "="*80)
print("MOLECULAR RESONANCE MAPPING COMPLETE")
print("="*80)
print("\nMapping design:")
print("  • Bits 0-7:   Atomic composition (C/H/O/N ratios)")
print("  • Bits 8-15:  Molecular weight (normalized)")
print("  • Bits 16-23: Structure hash (formula uniqueness)")
print("\n✓ Ready for UBP analysis pipeline")

# Export the bit generator for use in next step
print("\n[INFO] To use this mapping in analysis:")
print("  from workflow.03_molecular_mapping import molecular_resonance_bits")
