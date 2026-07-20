import json
import numpy as np
from fractions import Fraction
from core import LEECH_ENGINE, SUBSTRATE

def run_chromatic_lattice_audit():
    print("--- UBP v7.2: CHROMATIC-LATTICE CORRELATION AUDIT ---")
    
    # 1. Load your existing chromatic data
    try:
        with open('elemental_chromatic_data.json', 'r') as f:
            elements = json.load(f)
    except FileNotFoundError:
        print("❌ Error: 'elemental_chromatic_data.json' not found. Please ensure it is in the workspace.")
        return

    correlations = []
    
    print(f"{'Element':<15} | {'Saturation':<10} | {'Symmetry Tax':<15} | {'NRCI'}")
    print("-" * 60)

    results_data = []

    for el in elements:
        # Calculate Chromatic Saturation (Distance from Gray 128,128,128)
        r, g, b = el['rgb']['r'], el['rgb']['g'], el['rgb']['b']
        avg = (r + g + b) / 3
        saturation = np.sqrt((r-avg)**2 + (g-avg)**2 + (b-avg)**2)
        
        # Calculate v7.2 Substrate Metrics
        # We use the vector provided in your data
        vec = el['vector']
        tax = LEECH_ENGINE.calculate_symmetry_tax(vec)
        nrci = Fraction(10, 1) / (Fraction(10, 1) + tax)
        
        results_data.append({
            "symbol": el['name'],
            "sat": float(saturation),
            "tax": float(tax),
            "nrci": float(nrci)
        })
        
        if el['z'] % 20 == 0 or el['z'] in [1, 2, 26, 118]: # Sample output
            print(f"{el['name']:<15} | {saturation:>10.2f} | {float(tax):>15.4f} | {float(nrci):.4f}")

    # 2. Statistical Analysis
    sats = [d['sat'] for d in results_data]
    taxes = [d['tax'] for d in results_data]
    nrcis = [d['nrci'] for d in results_data]
    
    corr_sat_tax = np.corrcoef(sats, taxes)[0, 1]
    corr_sat_nrci = np.corrcoef(sats, nrcis)[0, 1]

    print("\n[STATISTICAL INFERENCE]")
    print(f"  Correlation (Saturation vs Tax):  {corr_sat_tax:.4f}")
    print(f"  Correlation (Saturation vs NRCI): {corr_sat_nrci:.4f}")

    if abs(corr_sat_nrci) > 0.7:
        print("\n✅ STRONG COUPLING: Chromatic Saturation is a valid proxy for Substrate Stability.")
    else:
        print("\n⚠️ WEAK COUPLING: Chromatic data and Lattice stability are partially decoupled.")

    # 3. Save findings
    with open('chromatic_lattice_correlation.json', 'w') as f:
        json.dump({
            "correlations": {
                "sat_vs_tax": corr_sat_tax,
                "sat_vs_nrci": corr_sat_nrci
            },
            "summary": "Audit of 118 elements comparing RGB saturation to Leech Lattice Symmetry Tax."
        }, f, indent=2)

if __name__ == "__main__":
    run_chromatic_lattice_audit()