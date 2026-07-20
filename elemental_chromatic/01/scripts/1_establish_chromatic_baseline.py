import json
import numpy as np
from fractions import Fraction

def establish_chromatic_baseline():
    print("--- STUDY: CHROMATIC STRUCTURE OF MATTER (Phase 1) ---")
    
    with open('elemental_chromatic_data.json', 'r') as f:
        elements = json.load(f)

    r_vals = [el['rgb']['r'] for el in elements]
    g_vals = [el['rgb']['g'] for el in elements]
    b_vals = [el['rgb']['b'] for el in elements]

    # 1. Calculate Mean and StdDev
    mean_rgb = (np.mean(r_vals), np.mean(g_vals), np.mean(b_vals))
    std_rgb = (np.std(r_vals), np.std(g_vals), np.std(b_vals))

    # 2. Calculate "Chromatic Saturation" (Distance from Gray)
    # Gray is where R=G=B. Saturation measures how 'extreme' an element is.
    saturations = []
    for el in elements:
        r, g, b = el['rgb']['r'], el['rgb']['g'], el['rgb']['b']
        avg = (r + g + b) / 3
        dist = math.sqrt((r-avg)**2 + (g-avg)**2 + (b-avg)**2)
        saturations.append(dist)

    # 3. Identify the "Purest" Elements (Highest Saturation in one channel)
    pure_red = max(elements, key=lambda x: x['rgb']['r'] - (x['rgb']['g'] + x['rgb']['b'])/2)
    pure_green = max(elements, key=lambda x: x['rgb']['g'] - (x['rgb']['r'] + x['rgb']['b'])/2)
    pure_blue = max(elements, key=lambda x: x['rgb']['b'] - (x['rgb']['r'] + x['rgb']['g'])/2)

    results = {
        "mean_rgb": [round(x, 2) for x in mean_rgb],
        "std_rgb": [round(x, 2) for x in std_rgb],
        "avg_saturation": round(float(np.mean(saturations)), 2),
        "anchors": {
            "Reality_Anchor": pure_red['ubp_id'],
            "Info_Anchor": pure_green['ubp_id'],
            "Potential_Anchor": pure_blue['ubp_id']
        }
    }

    print(f"\n[RESULTS]")
    print(f"  Universal Mean Color: R={results['mean_rgb'][0]} G={results['mean_rgb'][1]} B={results['mean_rgb'][2]}")
    print(f"  Chromatic Saturation: {results['avg_saturation']} (Avg distance from Gray)")
    print(f"  Reality Anchor (Red): {results['anchors']['Reality_Anchor']}")
    print(f"  Info Anchor (Green):  {results['anchors']['Info_Anchor']}")
    print(f"  Potential Anchor (Blue): {results['anchors']['Potential_Anchor']}")

    with open('chromatic_baseline.json', 'w') as f:
        json.dump(results, f, indent=2)

if __name__ == "__main__":
    import math
    establish_chromatic_baseline()