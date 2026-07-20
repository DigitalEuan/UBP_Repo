import json
import numpy as np
from fractions import Fraction
from ubp_eml_alu_sovereign import GrandUnifiedEmlALU
from core import LEECH_ENGINE

def run_pantograph_study():
    print("--- UBP v7.2: PANTOGRAPH CHROMATIC PROJECTION ---")
    alu = GrandUnifiedEmlALU()
    
    with open('elemental_chromatic_data.json', 'r') as f:
        elements = json.load(f)

    print(f"{'Element':<15} | {'Saturation':<10} | {'EML Wobble (W)':<15} | {'Panto-NRCI'}")
    print("-" * 65)

    panto_results = []

    for el in elements:
        # 1. Inputs
        r, g, b = el['rgb']['r'], el['rgb']['g'], el['rgb']['b']
        sat = np.sqrt((r-128)**2 + (g-128)**2 + (b-128)**2) / 128.0 # Normalized
        tax = float(LEECH_ENGINE.calculate_symmetry_tax(el['vector']))
        
        # 2. EML Operator: Projecting Color onto Tax
        # We use the ALU to find the transcendental resonance between the two
        wobble_dual = alu.eml(sat, tax)
        W = abs(wobble_dual.real) % 1.0 # The "Triadic Wobble" residue
        
        # 3. Pantograph Scaling (LAW_PANTOGRAPH_THERMODYNAMICS_001)
        # Macroscopic NRCI = Base_NRCI * (1 - Wobble/Pi)
        base_nrci = float(Fraction(10, 1) / (Fraction(10, 1) + Fraction(int(tax*1000), 1000)))
        panto_nrci = base_nrci * (1.0 - (W / float(alu.PI)))

        panto_results.append({
            "name": el['name'],
            "sat": sat,
            "wobble": W,
            "panto_nrci": panto_nrci
        })

        if el['z'] in [1, 2, 26, 118]: # Sample output
            print(f"{el['name']:<15} | {sat:>10.4f} | {W:>15.6f} | {panto_nrci:.4f}")

    # 4. Re-calculate Correlation
    sats = [d['sat'] for d in panto_results]
    nrcis = [d['panto_nrci'] for d in panto_results]
    new_corr = np.corrcoef(sats, nrcis)[0, 1]

    print("\n[PANTOGRAPH INFERENCE]")
    print(f"  New Correlation (Saturation vs Panto-NRCI): {new_corr:.4f}")
    
    if abs(new_corr) > 0.5:
        print("✅ COUPLING ACHIEVED: The EML Wobble bridges the Chromatic-Lattice gap.")
    else:
        print("❌ DECOUPLED: The Pantograph requires a higher-dimensional (256D) anchor.")

    with open('pantograph_chromatic_results.json', 'w') as f:
        json.dump(panto_results, f, indent=2)

if __name__ == "__main__":
    run_pantograph_study()