from fractions import Fraction
from ubp_unified_v5 import GOLAY_ENGINE

def map_to_gf4(block):
    """Maps a 4-bit block to a GF(4) element or NOISE."""
    w = sum(block)
    if w == 0: return "0"
    if w == 4: return "1"
    if w == 2:
        # Holomorphic (W) vs Anti-Holomorphic (W_BAR) split
        # These specific parity patterns define the complex conjugation in the MOG
        if block in ([1, 1, 0, 0], [0, 0, 1, 1], [1, 0, 0, 1]):
            return "W"
        elif block in ([1, 0, 1, 0], [0, 1, 0, 1], [0, 1, 1, 0]):
            return "W_BAR"
    # Odd weights break the complex structure
    return "NOISE" 

def project_to_hexacode(vec):
    """Projects a 24-bit vector into 6 GF(4) coordinates."""
    blocks = [vec[i:i+4] for i in range(0, 24, 4)]
    return [map_to_gf4(b) for b in blocks]

def analyze_holomorphic_balance(hexacode):
    """Analyzes the balance of W and W_BAR in the hexacode."""
    w_count = hexacode.count("W")
    w_bar_count = hexacode.count("W_BAR")
    noise_count = hexacode.count("NOISE")
    real_count = hexacode.count("0") + hexacode.count("1")
    
    # Balance ratio: 1.0 means perfectly balanced (or purely real), 0.0 means completely imbalanced
    total_complex = w_count + w_bar_count
    if total_complex == 0:
        # If there are no complex parts, it is perfectly diagonal (p,p) UNLESS there is noise
        balance = Fraction(1, 1) if noise_count == 0 else Fraction(0, 1)
    else:
        diff = abs(w_count - w_bar_count)
        balance = Fraction(total_complex - diff, total_complex)
        
    return {
        "W": w_count,
        "W_BAR": w_bar_count,
        "REAL": real_count,
        "NOISE": noise_count,
        "balance": balance
    }

def run_gf4_experiment():
    print("=== UBP GF(4) Hexacode: Holomorphic Balance Experiment ===")
    
    # 1. Test an Algebraic Cycle (A perfect Golay Octad)
    octad = GOLAY_ENGINE.get_octads()[0]
    print("\n[Test 1] Algebraic Cycle (Golay Octad)")
    print(f"Vector: {octad}")
    
    hex_alg = project_to_hexacode(octad)
    print(f"GF(4) Projection: {hex_alg}")
    
    metrics_alg = analyze_holomorphic_balance(hex_alg)
    print(f"Metrics: {metrics_alg}")
    print(f"Holomorphic Balance: {float(metrics_alg['balance']):.4f} (Exact: {metrics_alg['balance']})")
    
    # 2. Test a Non-Algebraic Class (Noise / Unstable Vector)
    # We create a vector with broken parities and imbalanced complex forms
    noisy_vec = [1,1,1,1,  1,1,1,0,  0,0,0,0,  0,0,0,0,  1,1,0,0,  0,0,0,0]
    print("\n[Test 2] Non-Algebraic Class (Imbalanced Noise)")
    print(f"Vector: {noisy_vec}")
    
    hex_noise = project_to_hexacode(noisy_vec)
    print(f"GF(4) Projection: {hex_noise}")
    
    metrics_noise = analyze_holomorphic_balance(hex_noise)
    print(f"Metrics: {metrics_noise}")
    print(f"Holomorphic Balance: {float(metrics_noise['balance']):.4f} (Exact: {metrics_noise['balance']})")
    
    print("\n=== CONCLUSION ===")
    print("If the Algebraic Cycle shows zero NOISE and a high/perfect Holomorphic Balance,")
    print("we have successfully mapped the Hodge (p,p) condition to the GF(4) Hexacode.")

if __name__ == "__main__":
    run_gf4_experiment()