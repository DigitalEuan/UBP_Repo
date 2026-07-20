import json
import math
from core import GOLAY_ENGINE, BinaryLinearAlgebra

def calculate_saturation(r, g, b):
    avg = (r + g + b) / 3
    return math.sqrt((r-avg)**2 + (g-avg)**2 + (b-avg)**2)

def bits_to_rgb(bits):
    val = 0
    for bit in bits: val = (val << 1) | bit
    return (val >> 16) & 0xFF, (val >> 8) & 0xFF, val & 0xFF

def test_chromatic_bonding():
    print("--- STUDY: CHROMATIC STRUCTURE OF MATTER (Phase 2) ---")
    
    # Load data safely
    with open('elemental_chromatic_data.json', 'r') as f:
        raw_list = json.load(f)
    
    elements = {el['ubp_id']: el for el in raw_list}

    # 1. Fetch Parents (Sodium and Chlorine)
    if 'ELEM_Na_011' not in elements or 'ELEM_Cl_017' not in elements:
        print("❌ Error: Parent elements not found in data.")
        return

    na = elements['ELEM_Na_011']
    cl = elements['ELEM_Cl_017']

    na_sat = calculate_saturation(na['rgb']['r'], na['rgb']['g'], na['rgb']['b'])
    cl_sat = calculate_saturation(cl['rgb']['r'], cl['rgb']['g'], cl['rgb']['b'])

    print(f"Parent A: {na['name']} | Color: {na['hex_color']} | Saturation: {na_sat:.2f}")
    print(f"Parent B: {cl['name']} | Color: {cl['hex_color']} | Saturation: {cl_sat:.2f}")

    # 2. Simulate Interaction (The Flow)
    # Binary XOR represents the 'Superposition' of the two states
    combined_raw = [na['vector'][i] ^ cl['vector'][i] for i in range(24)]
    
    # 3. Projective Snap (The Lens)
    # Force the result back to the nearest stable coordinate on the manifold
    snapped_bits, meta = GOLAY_ENGINE.snap_to_codeword(combined_raw)
    
    # 4. Analyze Result (NaCl)
    r, g, b = bits_to_rgb(snapped_bits)
    res_hex = f"#{r:02x}{g:02x}{b:02x}"
    res_sat = calculate_saturation(r, g, b)
    
    avg_parent_sat = (na_sat + cl_sat) / 2
    sat_drop = avg_parent_sat - res_sat

    print(f"\n[BOND RESULT: NaCl]")
    print(f"  Resulting Color: {res_hex}")
    print(f"  Result Saturation: {res_sat:.2f}")
    print(f"  Chromatic Neutralization (Saturation Drop): {sat_drop:.2f}")

    # 5. Verification against Noble Equilibrium
    he = elements['ELEM_He_002']
    he_sat = calculate_saturation(he['rgb']['r'], he['rgb']['g'], he['rgb']['b'])
    print(f"  Noble Baseline (Helium) Saturation: {he_sat:.2f}")

    results = {
        "bond": "Na+Cl",
        "parent_avg_sat": round(avg_parent_sat, 2),
        "result_sat": round(res_sat, 2),
        "neutralization_score": round(sat_drop, 2),
        "is_stabilized": res_sat < avg_parent_sat
    }
    
    with open('chromatic_bonding_results.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    print("\nResults saved to 'chromatic_bonding_results.json'")

if __name__ == "__main__":
    test_chromatic_bonding()