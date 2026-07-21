from fractions import Fraction
from ubp_unified_v5 import GOLAY_ENGINE

def map_to_gf4(block):
    """Maps a 4-bit MOG column to a GF(4) element or NOISE."""
    w = sum(block)
    if w == 0: return "0"
    if w == 4: return "1"
    if w == 2:
        # Holomorphic (W) vs Anti-Holomorphic (W_BAR) split
        # Standard MOG parity rules for GF(4) mapping
        if block in ([1, 1, 0, 0], [0, 0, 1, 1], [1, 0, 0, 1]):
            return "W"
        elif block in ([1, 0, 1, 0], [0, 1, 0, 1], [0, 1, 1, 0]):
            return "W_BAR"
    return "NOISE" 

def project_to_hexacode_mog(vec):
    """Projects a 24-bit vector into 6 GF(4) coordinates using the 4x6 MOG grid."""
    # The UBP MOG: 4 rows (Reality, Info, Activation, Potential), 6 columns
    # We extract the 6 columns. Each column has 4 bits (one from each row).
    columns = [[vec[i], vec[i+6], vec[i+12], vec[i+18]] for i in range(6)]
    return [map_to_gf4(col) for col in columns]

def analyze_holomorphic_balance(hexacode):
    w_count = hexacode.count("W")
    w_bar_count = hexacode.count("W_BAR")
    noise_count = hexacode.count("NOISE")
    real_count = hexacode.count("0") + hexacode.count("1")
    
    total_complex = w_count + w_bar_count
    if total_complex == 0:
        balance = Fraction(1, 1) if noise_count == 0 else Fraction(0, 1)
    else:
        diff = abs(w_count - w_bar_count)
        balance = Fraction(total_complex - diff, total_complex)
        
    return {
        "W": w_count, "W_BAR": w_bar_count, "REAL": real_count,
        "NOISE": noise_count, "balance": balance
    }

def run_mog_gf4_experiment():
    print("=== UBP GF(4) Hexacode: MOG-Mapped Holomorphic Balance ===")
    
    octad = GOLAY_ENGINE.get_octads()[0]
    print("\n[Test 1] Algebraic Cycle (Golay Octad)")
    print(f"Vector: {octad}")
    
    hex_alg = project_to_hexacode_mog(octad)
    print(f"MOG GF(4) Projection: {hex_alg}")
    metrics_alg = analyze_holomorphic_balance(hex_alg)
    print(f"Metrics: {metrics_alg}")
    print(f"Holomorphic Balance: {float(metrics_alg['balance']):.4f}")
    
    # We create a vector with highly imbalanced sextets
    noisy_vec = [1,1,1,1,1,1,  1,0,0,0,0,0,  0,0,0,0,0,0,  1,1,0,0,0,0]
    print("\n[Test 2] Non-Algebraic Class (Imbalanced Noise)")
    print(f"Vector: {noisy_vec}")
    
    hex_noise = project_to_hexacode_mog(noisy_vec)
    print(f"MOG GF(4) Projection: {hex_noise}")
    metrics_noise = analyze_holomorphic_balance(hex_noise)
    print(f"Metrics: {metrics_noise}")
    print(f"Holomorphic Balance: {float(metrics_noise['balance']):.4f}")

if __name__ == "__main__":
    run_mog_gf4_experiment()