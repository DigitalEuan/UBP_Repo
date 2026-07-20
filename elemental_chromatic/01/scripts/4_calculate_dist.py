import json
import math
import itertools
import numpy as np

def calculate_dist(p1, p2):
    return math.sqrt(sum((a - b)**2 for a, b in zip(p1, p2)))

def run_permutation_study():
    print("--- UBP CHROMATIC PERMUTATION STUDY ---")
    
    with open('elemental_chromatic_data.json', 'r') as f:
        elements = json.load(f)
    
    # Define Chemical Groups for Cohesion Testing
    noble_z = [2, 10, 18, 36, 54, 86, 118]
    alkali_z = [3, 11, 19, 37, 55, 87]
    
    channels = ['r', 'g', 'b']
    permutations = list(itertools.permutations(channels))
    
    results = []

    for perm in permutations:
        # Map RGB to XYZ based on current permutation
        coords = []
        for el in elements:
            # Center the values around 0 (128 is mid-point)
            x = el['rgb'][perm[0]] - 128
            y = el['rgb'][perm[1]] - 128
            z = el['rgb'][perm[2]] - 128
            coords.append((x, y, z, el['z'], el['nrci']))

        # Metric 1: Z-Path Smoothness (Avg distance between Z and Z+1)
        path_distances = []
        for i in range(len(coords) - 1):
            path_distances.append(calculate_dist(coords[i][:3], coords[i+1][:3]))
        avg_smoothness = np.mean(path_distances)

        # Metric 2: Noble Gas Cohesion (StdDev of Noble positions)
        nobles = [c[:3] for c in coords if c[3] in noble_z]
        noble_center = np.mean(nobles, axis=0)
        noble_spread = np.mean([calculate_dist(n, noble_center) for n in nobles])

        # Metric 3: NRCI-Spatial Correlation
        # Does distance from origin (Saturation) correlate with NRCI?
        saturations = [calculate_dist(c[:3], (0,0,0)) for c in coords]
        nrcis = [c[4] for c in coords]
        correlation = np.corrcoef(saturations, nrcis)[0, 1]

        results.append({
            "mapping": f"X={perm[0].upper()}, Y={perm[1].upper()}, Z={perm[2].upper()}",
            "smoothness": round(float(avg_smoothness), 2),
            "noble_spread": round(float(noble_spread), 2),
            "nrci_corr": round(float(correlation), 4)
        })

    # Sort by Noble Spread (Finding the Stability Anchor)
    results.sort(key=lambda x: x['noble_spread'])

    print(f"\n{'Mapping':<15} | {'Z-Smoothness':<12} | {'Noble Spread':<12} | {'NRCI Corr'}")
    print("-" * 60)
    for r in results:
        print(f"{r['mapping']:<15} | {r['smoothness']:<12} | {r['noble_spread']:<12} | {r['nrci_corr']}")

    best = results[0]
    print(f"\n[WINNING MAPPING]: {best['mapping']}")
    print(f"Reason: This mapping creates the tightest clustering of Noble Gases ({best['noble_spread']}).")

    with open('permutation_study_results.json', 'w') as f:
        json.dump(results, f, indent=2)

if __name__ == "__main__":
    run_permutation_study()