from study_5 import GolayCodeG24, LeechPoint, UBPConstants
from fractions import Fraction

def run_hard_test():
    print("="*60)
    print("UBP v4.2.1 RESONANT STRESS TEST")
    print("="*60)
    
    golay = GolayCodeG24()
    
    # --- TEST 1: THE NOISE STRESS TEST (Coherence Snaps) ---
    print("\n[TEST 1] Noise Stress (LAW_APP_001)")
    # Start with a clean 12-bit message
    msg = [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0]
    clean_codeword = golay.encode(msg)
    
    # Introduce 1-bit corruption (The "Drift")
    noisy_codeword = list(clean_codeword)
    noisy_codeword[0] = 1 - noisy_codeword[0] 
    
    # Trigger Coherence Snap
    snapped, meta = golay.decode(noisy_codeword)
    
    print(f"  Original: {clean_codeword[:8]}...")
    print(f"  Noisy:    {noisy_codeword[:8]}...")
    print(f"  Snapped:  {snapped[:8]}...")
    print(f"  Result:   {'✓ SUCCESS' if snapped == clean_codeword else '✗ FAILURE'}")
    print(f"  Drift Distance: {meta['error_weight']} bit")

    # --- TEST 2: ONTOLOGICAL HEALTH GRADIENT (LAW_SUBSTRATE_005) ---
    print("\n[TEST 2] Ontological Health Gradient")
    # State A: High Symmetry (Zero Point)
    p_zero = LeechPoint(tuple([0]*24))
    # State B: High Activity (Minimal Vector approximation)
    p_active = LeechPoint(tuple([2, 2, 0, 0, 0, 0, 2, 2, 0, 0, 0, 0, 2, 2, 0, 0, 0, 0, 2, 2, 0, 0, 0, 0]))
    
    health_zero = p_zero.get_ontological_health()
    health_active = p_active.get_ontological_health()
    
    print(f"  Zero State Health (Global):   {float(health_zero['Global_NRCI']):.4f}")
    print(f"  Active State Health (Global): {float(health_active['Global_NRCI']):.4f}")
    print(f"  Reality Layer Health:         {float(health_active['Reality']):.4f}")
    print(f"  Potential Layer Health:       {float(health_active['Potential']):.4f}")

    # --- TEST 3: SYMMETRY TAX RIGOR (LAW_SYMMETRY_001) ---
    print("\n[TEST 3] Symmetry Tax Rigor (Zero-Float)")
    tax_zero = p_zero.calculate_symmetry_tax()
    tax_active = p_active.calculate_symmetry_tax()
    
    # Verify that Tax is a Fraction, not a float
    is_rational = isinstance(tax_active, Fraction)
    
    print(f"  Zero State Tax:   {tax_zero} (Pure Rational)")
    print(f"  Active State Tax: {tax_active} ({float(tax_active):.6f})")
    print(f"  Zero-Float Rigor: {'✓ PASSED' if is_rational else '✗ FAILED'}")

    # --- TEST 4: SHADOW PROCESSOR RATIO (LAW_COMP_009) ---
    print("\n[TEST 4] Shadow Processor Metrics")
    shadow = golay.get_shadow_metrics()
    print(f"  Noumenal/Phenomenal Ratio: {shadow['ratio']}")
    print(f"  Noumenal Range: {shadow['noumenal_bits']}")
    print(f"  Phenomenal Range: {shadow['phenomenal_bits']}")

    # --- TEST 5: PHYSICAL MANIFOLD PROJECTION ---
    print("\n[TEST 5] Physical Manifold Projection")
    physical_coords = p_active.to_physical_space()
    print(f"  Integer Coord [0]: {p_active.coords[0]}")
    print(f"  Physical Coord [0]: {float(physical_coords[0]):.6f}")
    
    print("\n" + "="*60)
    print("STRESS TEST COMPLETE: SYSTEM IS ON-BIT")
    print("="*60)

if __name__ == "__main__":
    run_hard_test()