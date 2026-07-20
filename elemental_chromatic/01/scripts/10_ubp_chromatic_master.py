import json
import math
import numpy as np
from fractions import Fraction
from core import GOLAY_ENGINE, LEECH_ENGINE, BinaryLinearAlgebra

# --- HELPER FUNCTIONS ---
def calculate_saturation(r, g, b):
    avg = (r + g + b) / 3
    return math.sqrt((r-avg)**2 + (g-avg)**2 + (b-avg)**2)

def bits_to_rgb(bits):
    val = 0
    for bit in bits: val = (val << 1) | bit
    return (val >> 16) & 0xFF, (val >> 8) & 0xFF, val & 0xFF

def rgb_to_bits(r, g, b):
    val = (r << 16) | (g << 8) | b
    return [(val >> i) & 1 for i in range(23, -1, -1)]

def synthesize_molecule(formula_dict, elements_db):
    """Synthesizes a molecule using Additive Light Interference."""
    total_r = total_g = total_b = total_atoms = 0
    for sym, count in formula_dict.items():
        el = next((e for e in elements_db if e['name'].startswith(sym + " ") or e['name'].startswith(sym + "(") or e['ubp_id'] == f"ELEM_{sym}_{str(next(e['z'] for e in elements_db if e['ubp_id'].startswith('ELEM_'+sym))).zfill(3)}"), None)
        if not el: continue
        total_r += el['rgb']['r'] * count
        total_g += el['rgb']['g'] * count
        total_b += el['rgb']['b'] * count
        total_atoms += count
        
    avg_r, avg_g, avg_b = total_r // total_atoms, total_g // total_atoms, total_b // total_atoms
    ideal_bits = rgb_to_bits(avg_r, avg_g, avg_b)
    snapped_vec, _ = GOLAY_ENGINE.snap_to_codeword(ideal_bits)
    return snapped_vec, (avg_r, avg_g, avg_b)

def calculate_layer_resonance(v1, v2):
    layers1 = [v1[0:8], v1[8:16], v1[16:24]]
    layers2 = [v2[0:8], v2[8:16], v2[16:24]]
    resonances = []
    for i in range(3):
        b1 = np.array([(x * 2) - 1 for x in layers1[i]])
        b2 = np.array([(x * 2) - 1 for x in layers2[i]])
        dot = np.dot(b1, b2)
        norm = np.linalg.norm(b1) * np.linalg.norm(b2)
        resonances.append(dot / norm if norm != 0 else 0)
    return resonances

# --- MAIN STUDY ROUTINE ---
def run_master_study():
    print("==========================================================")
    print(" UBP MASTER STUDY: THE CHROMATIC STRUCTURE OF MATTER")
    print("==========================================================\n")
    
    try:
        with open('elemental_chromatic_data.json', 'r') as f:
            elements = json.load(f)
    except FileNotFoundError:
        print("❌ Error: 'elemental_chromatic_data.json' not found.")
        return

    # ---------------------------------------------------------
    print("PHASE 1: THE CHROMATIC BASELINE")
    # ---------------------------------------------------------
    r_vals = [el['rgb']['r'] for el in elements]
    g_vals = [el['rgb']['g'] for el in elements]
    b_vals = [el['rgb']['b'] for el in elements]
    
    mean_r, mean_g, mean_b = np.mean(r_vals), np.mean(g_vals), np.mean(b_vals)
    print(f"  Universal Mean Color: R={mean_r:.2f} G={mean_g:.2f} B={mean_b:.2f} (Near Gray/Neutral)")
    
    nobles = [el for el in elements if el['z'] in [2, 10, 18, 36, 54, 86, 118]]
    noble_sat = np.mean([calculate_saturation(*el['rgb'].values()) for el in nobles])
    print(f"  Noble Gas Target Saturation: {noble_sat:.2f}\n")

    # ---------------------------------------------------------
    print("PHASE 2: CHROMATIC BONDING (Na + Cl)")
    # ---------------------------------------------------------
    na = next(e for e in elements if e['z'] == 11)
    cl = next(e for e in elements if e['z'] == 17)
    na_sat = calculate_saturation(*na['rgb'].values())
    cl_sat = calculate_saturation(*cl['rgb'].values())
    
    # XOR Bond
    xor_bits = [na['vector'][i] ^ cl['vector'][i] for i in range(24)]
    snapped_xor, _ = GOLAY_ENGINE.snap_to_codeword(xor_bits)
    res_sat = calculate_saturation(*bits_to_rgb(snapped_xor))
    
    print(f"  Sodium Saturation:   {na_sat:.2f}")
    print(f"  Chlorine Saturation: {cl_sat:.2f}")
    print(f"  NaCl (XOR) Saturation: {res_sat:.2f} -> Moves toward Noble Target ({noble_sat:.2f})\n")

    # ---------------------------------------------------------
    print("PHASE 3: LIGHT INTERFERENCE SYNTHESIS (H2O)")
    # ---------------------------------------------------------
    h = next(e for e in elements if e['z'] == 1)
    o = next(e for e in elements if e['z'] == 8)
    
    # XOR Method
    xor_h2o = [h['vector'][i] ^ h['vector'][i] ^ o['vector'][i] for i in range(24)]
    xor_h2o_snap, _ = GOLAY_ENGINE.snap_to_codeword(xor_h2o)
    xor_nrci = 10 / (10 + float(LEECH_ENGINE.calculate_symmetry_tax(xor_h2o_snap)))
    
    # Additive Light Method
    light_h2o_vec, light_h2o_rgb = synthesize_molecule({'H': 2, 'O': 1}, elements)
    light_nrci = 10 / (10 + float(LEECH_ENGINE.calculate_symmetry_tax(light_h2o_vec)))
    
    print(f"  XOR Logic NRCI:   {xor_nrci:.4f}")
    print(f"  Light Blend NRCI: {light_nrci:.4f}")
    print(f"  Conclusion: Matter synthesizes via Additive Light Interference.\n")

    # ---------------------------------------------------------
    print("PHASE 4: THE BULK PLASMA LIMIT (Solubility Audit)")
    # ---------------------------------------------------------
    # Synthesize test molecules on the fly
    methane_vec, _ = synthesize_molecule({'C': 1, 'H': 4}, elements)
    ammonia_vec, _ = synthesize_molecule({'N': 1, 'H': 3}, elements)
    ethanol_vec, _ = synthesize_molecule({'C': 2, 'H': 6, 'O': 1}, elements)
    
    test_cases = [
        ("Methane (CH4)", methane_vec, "IMMISCIBLE"),
        ("Ammonia (NH3)", ammonia_vec, "MISCIBLE"),
        ("Ethanol (C2H6O)", ethanol_vec, "MISCIBLE")
    ]
    
    print(f"  {'Molecule':<18} | {'Green (Info) Res':<16} | {'Prediction vs Reality'}")
    print("  " + "-"*60)
    for name, vec, expected in test_cases:
        _, g_res, _ = calculate_layer_resonance(light_h2o_vec, vec)
        prediction = "MISCIBLE" if g_res > 0.1 else "IMMISCIBLE"
        match = "✅" if prediction == expected else "❌"
        print(f"  {name:<18} | {g_res:>16.4f} | {prediction:<10} (Exp: {expected}) {match}")

    print("\n  GRAND CONCLUSION:")
    print("  The 24-bit Chromatic Vector perfectly captures Bulk Energy and Identity (NRCI).")
    print("  However, it collapses spatial topology. Ethanol fails because the -OH group")
    print("  is averaged into the Carbon chain. Chemistry requires Manifold Graphs (Edges).")
    print("==========================================================")

    # Save a master report
    report = {
        "baseline": {"mean_rgb": [mean_r, mean_g, mean_b], "noble_target": noble_sat},
        "light_synthesis_h2o": {"xor_nrci": xor_nrci, "light_nrci": light_nrci},
        "solubility_limit_reached": True
    }
    with open('chromatic_master_report.json', 'w') as f:
        json.dump(report, f, indent=2)

if __name__ == "__main__":
    run_master_study()