import json
from core import GOLAY_ENGINE, LEECH_ENGINE

def hex_to_rgb(h):
    h = h.lstrip('#')
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

def rgb_to_bits(r, g, b):
    val = (r << 16) | (g << 8) | b
    return [(val >> i) & 1 for i in range(23, -1, -1)]

def test_light_interference():
    print("--- STUDY: CHROMATIC INTERFERENCE (Light vs Logic) ---")
    
    with open('elemental_chromatic_data.json', 'r') as f:
        elements = {el['ubp_id']: el for el in json.load(f)}

    h = elements['ELEM_H_001']
    o = elements['ELEM_O_008']

    print(f"Subject A: {h['name']} ({h['hex_color']})")
    print(f"Subject B: {o['name']} ({o['hex_color']})")

    # 1. METHOD A: XOR Logic (The Old Way)
    xor_bits = [h['vector'][i] ^ o['vector'][i] for i in range(24)]
    xor_snapped, _ = GOLAY_ENGINE.snap_to_codeword(xor_bits)
    xor_tax = LEECH_ENGINE.calculate_symmetry_tax(xor_snapped)
    xor_nrci = 10 / (10 + float(xor_tax))

    # 2. METHOD B: Additive Light (The New Way)
    # We average the RGB values (H2O = (H+H+O)/3)
    mix_r = int((h['rgb']['r'] + h['rgb']['r'] + o['rgb']['r']) / 3)
    mix_g = int((h['rgb']['g'] + h['rgb']['g'] + o['rgb']['g']) / 3)
    mix_b = int((h['rgb']['b'] + h['rgb']['b'] + o['rgb']['b']) / 3)
    
    light_bits = rgb_to_bits(mix_r, mix_g, mix_b)
    light_snapped, _ = GOLAY_ENGINE.snap_to_codeword(light_bits)
    light_tax = LEECH_ENGINE.calculate_symmetry_tax(light_snapped)
    light_nrci = 10 / (10 + float(light_tax))

    print(f"\n[RESULTS: H2O Synthesis]")
    print(f"  XOR Logic NRCI:   {xor_nrci:.4f}")
    print(f"  Light Blend NRCI: {light_nrci:.4f}")
    
    if light_nrci > xor_nrci:
        print("\n✅ HYPOTHESIS CONFIRMED: Matter behaves like Light Interference.")
    else:
        print("\n❌ HYPOTHESIS FAILED: Logic is more stable than Light.")

    results = {
        "xor_nrci": xor_nrci,
        "light_nrci": light_nrci,
        "winner": "LIGHT" if light_nrci > xor_nrci else "LOGIC"
    }
    with open('light_interference_results.json', 'w') as f:
        json.dump(results, f, indent=2)

if __name__ == "__main__":
    test_light_interference()