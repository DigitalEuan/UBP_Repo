import json
import math
import itertools
from core import GOLAY_ENGINE

def calculate_saturation(r, g, b):
    avg = (r + g + b) / 3
    return math.sqrt((r-avg)**2 + (g-avg)**2 + (b-avg)**2)

def bits_to_rgb(bits):
    val = 0
    for bit in bits: val = (val << 1) | bit
    return (val >> 16) & 0xFF, (val >> 8) & 0xFF, val & 0xFF

def run_landscape_audit():
    print("--- STUDY: CHROMATIC STRUCTURE OF MATTER (Phase 2.1 - Landscape) ---")
    
    with open('elemental_chromatic_data.json', 'r') as f:
        elements = json.load(f)
    
    # Focus on the first 20 elements (H through Ca)
    basis = [el for el in elements if el['z'] <= 20]
    noble_z = [2, 10, 18]
    nobles = [el for el in basis if el['z'] in noble_z]
    avg_noble_sat = sum(calculate_saturation(*el['rgb'].values()) for el in nobles) / len(nobles)
    
    print(f"Noble Saturation Target (Stability): {avg_noble_sat:.2f}")
    print(f"Auditing {len(basis)} elements ({len(list(itertools.combinations(basis, 2)))} pairs)...")

    results = []
    convergence_count = 0 # Pairs that move toward Noble Saturation

    for el_a, el_b in itertools.combinations(basis, 2):
        # 1. Parent Metrics
        sat_a = calculate_saturation(*el_a['rgb'].values())
        sat_b = calculate_saturation(*el_b['rgb'].values())
        avg_parent_sat = (sat_a + sat_b) / 2
        
        # 2. Simulate Bond (XOR + Snap)
        combined_raw = [el_a['vector'][i] ^ el_b['vector'][i] for i in range(24)]
        snapped_bits, _ = GOLAY_ENGINE.snap_to_codeword(combined_raw)
        
        # 3. Result Metrics
        r, g, b = bits_to_rgb(snapped_bits)
        res_sat = calculate_saturation(r, g, b)
        
        # 4. Check Convergence: Did the bond move closer to the Noble Saturation?
        dist_parents = abs(avg_parent_sat - avg_noble_sat)
        dist_result = abs(res_sat - avg_noble_sat)
        
        converged = dist_result < dist_parents
        if converged: convergence_count += 1
        
        results.append({
            "pair": f"{el_a['name']}+{el_b['name']}",
            "parent_sat": round(avg_parent_sat, 2),
            "result_sat": round(res_sat, 2),
            "converged_to_noble": converged
        })

    # Statistical Summary
    total_pairs = len(results)
    convergence_rate = (convergence_count / total_pairs) * 100
    
    print(f"\n[LANDSCAPE RESULTS]")
    print(f"  Total Pairs Tested: {total_pairs}")
    print(f"  Noble Convergence Rate: {convergence_rate:.2f}%")
    
    # Find the "Perfect Bond" (Closest to Noble Saturation)
    perfect = min(results, key=lambda x: abs(x['result_sat'] - avg_noble_sat))
    print(f"  Most Stable Predicted Bond: {perfect['pair']} (Sat: {perfect['result_sat']})")

    with open('chromatic_landscape_results.json', 'w') as f:
        json.dump({
            "noble_target": round(avg_noble_sat, 2),
            "convergence_rate": round(convergence_rate, 2),
            "top_bonds": sorted(results, key=lambda x: abs(x['result_sat'] - avg_noble_sat))[:10]
        }, f, indent=2)

if __name__ == "__main__":
    run_landscape_audit()