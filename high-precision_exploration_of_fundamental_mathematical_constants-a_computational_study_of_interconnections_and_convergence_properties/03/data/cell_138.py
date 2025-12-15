# Cell 138 from UBP_UNIFIED_SYSTEM_1.ipynb

# @title Resonance Finder Script
import mpmath as mp
import itertools

# 1. SETUP CONSTANTS
mp.mp.dps = 50

def compute_pi():
    return mp.pi

PI = compute_pi()
Y = PI / (PI**2 + mp.mpf('2'))
Y_INV = mp.mpf('1') / Y
Ref_e = mp.mpf('0.5109989461')    # Electron (Base Unit 1)
Ref_p = mp.mpf('938.27208816')    # Proton (Base Unit 2)

print(f"CONSTANTS:")
print(f"  π   = {mp.nstr(PI, 10)}")
print(f"  Y   = {mp.nstr(Y, 10)}")
print(f"  1/Y = {mp.nstr(Y_INV, 10)}")
print("-" * 60)

# 2. DEFINE TARGETS (The particles we need to fix)
targets = {
    'Neutron (n)': 939.5654,
    'Up (u)': 2.16,
    'Down (d)': 4.67,
    'Strange (s)': 93.5,
    'Charm (c)': 1273.0,
    'Bottom (b)': 4183.0
}

# 3. DEFINE BUILDING BLOCKS
# We look for multipliers made of Y, PI, and small integers
components = {
    'Y': Y,
    '1/Y': Y_INV,
    'PI': PI,
    '1/PI': 1/PI,
    '2': mp.mpf('2'),
    '3': mp.mpf('3'),
    '4': mp.mpf('4'),
    'sqrt(2)': mp.sqrt(2),
    'ln(1/Y)': mp.log(Y_INV)
}

# 4. SEARCH FUNCTION
def find_resonance(target_mass, tolerance=0.01): # 1% tolerance
    best_match = None
    best_error = float('inf')

    # BASES: We try scaling from Electron, Proton, or Unity (1 MeV)
    bases = [('e', Ref_e), ('p', Ref_p), ('1MeV', mp.mpf(1))]

    print(f"\n🔍 Searching for: {target_mass} MeV")

    # A. Simple Multipliers (Base * A * B)
    # We test combinations of up to 3 components
    keys = list(components.keys())

    # We iterate through combinations of constants
    for base_name, base_val in bases:
        # Depth 1: Base * A
        for k1 in keys:
            val = base_val * components[k1]
            err = abs(val - target_mass) / target_mass
            if err < best_error:
                best_error = err
                best_match = f"{base_name} * {k1}"

        # Depth 2: Base * A * B
        for k1 in keys:
            for k2 in keys:
                val = base_val * components[k1] * components[k2]
                err = abs(val - target_mass) / target_mass
                if err < best_error:
                    best_error = err
                    best_match = f"{base_name} * {k1} * {k2}"

        # Depth 3: Base * A * B^n (Power Laws)
        for k1 in keys:
            for power in [2, 3, 0.5, 1.5]:
                val = base_val * (components[k1] ** power)
                err = abs(val - target_mass) / target_mass
                if err < best_error:
                    best_error = err
                    best_match = f"{base_name} * {k1}^{power}"

    print(f"  ✓ Found Match: {best_match}")
    print(f"  -> Error: {float(best_error)*100:.4f}%")
    return best_match

# 5. EXECUTE SEARCH
print("STARTING GEOMETRIC BRUTE FORCE SEARCH...")
results = {}
for name, mass in targets.items():
    results[name] = find_resonance(mass)

print("\n" + "="*60)
print("RECOMMENDED FORMULA UPDATES")
print("="*60)
for name, formula in results.items():
    print(f"{name:12} : {formula}")