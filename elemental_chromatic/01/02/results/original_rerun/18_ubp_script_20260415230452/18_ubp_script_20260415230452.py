import json
from fractions import Fraction
from core import LEECH_ENGINE, GOLAY_ENGINE

def rgb_to_bits(r, g, b):
    val = (r << 16) | (g << 8) | b
    return [(val >> i) & 1 for i in range(23, -1, -1)]

def bits_to_rgb(bits):
    val = 0
    for bit in bits: val = (val << 1) | bit
    return (val >> 16) & 0xFF, (val >> 8) & 0xFF, val & 0xFF

def run_chromatic_synthesis():
    print("--- UBP v7.2: CHROMATIC MOLECULAR SYNTHESIS ---")
    
    with open('elemental_chromatic_data.json', 'r') as f:
        elements = {el['ubp_id']: el for el in json.load(f)}

    # Define Synthesis Recipes
    recipes = [
        {"name": "Water (H2O)", "components": [("ELEM_H_001", 2), ("ELEM_O_008", 1)]},
        {"name": "Salt (NaCl)", "components": [("ELEM_Na_011", 1), ("ELEM_Cl_017", 1)]},
        {"name": "Methane (CH4)", "components": [("ELEM_C_006", 1), ("ELEM_H_001", 4)]}
    ]

    results = []

    for recipe in recipes:
        print(f"\nSynthesizing: {recipe['name']}")
        
        total_r = total_g = total_b = total_atoms = 0
        
        for uid, count in recipe['components']:
            el = elements[uid]
            total_r += el['rgb']['r'] * count
            total_g += el['rgb']['g'] * count
            total_b += el['rgb']['b'] * count
            total_atoms += count
            print(f"  + Added {count}x {el['name']} ({el['hex_color']})")

        # 1. Calculate the "Interference Color" (Average RGB)
        avg_r, avg_g, avg_b = total_r // total_atoms, total_g // total_atoms, total_b // total_atoms
        interference_hex = f"#{avg_r:02x}{avg_g:02x}{avg_b:02x}"
        
        # 2. Convert to Bits and "Snap" to the nearest Lattice Point
        raw_bits = rgb_to_bits(avg_r, avg_g, avg_b)
        snapped_bits, _ = GOLAY_ENGINE.snap_to_codeword(raw_bits)
        
        # 3. Calculate Stability (NRCI)
        tax = LEECH_ENGINE.calculate_symmetry_tax(snapped_bits)
        nrci = Fraction(10, 1) / (Fraction(10, 1) + tax)
        
        # 4. Get the "Physical Color" (The color of the stable state)
        pr, pg, pb = bits_to_rgb(snapped_bits)
        physical_hex = f"#{pr:02x}{pg:02x}{pb:02x}"

        print(f"  [RESULT]")
        print(f"  Interference Color: {interference_hex}")
        print(f"  Physical Color:     {physical_hex} (Lattice Snapped)")
        print(f"  Bond Stability:     {float(nrci):.4f} NRCI")
        
        results.append({
            "molecule": recipe['name'],
            "nrci": float(nrci),
            "color": physical_hex
        })

    with open('chromatic_synthesis_results.json', 'w') as f:
        json.dump(results, f, indent=2)

if __name__ == "__main__":
    run_chromatic_synthesis()