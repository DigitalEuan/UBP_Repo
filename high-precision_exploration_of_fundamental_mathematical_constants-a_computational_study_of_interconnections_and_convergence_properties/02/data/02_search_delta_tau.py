#!/usr/bin/env python3
"""
Systematic Search for δ_τ (Tau Correction Factor)

Target: δ_τ ≈ 0.0825268035
Hypothesis: Should be expressible using π, e, Y, and simple integer ratios

Strategy:
1. Test simple expressions of Y, π, e
2. Test products and ratios
3. Test powers and roots
4. Use optimization for best fits
"""

import mpmath as mp
import json
import time
from pathlib import Path
from typing import Dict, List, Tuple

# Set ultra-high precision
mp.mp.dps = 200

print("="*80)
print("SYSTEMATIC SEARCH FOR δ_τ (TAU CORRECTION FACTOR)")
print("="*80)

# =============================================================================
# SETUP CONSTANTS
# =============================================================================
PI = mp.pi
E = mp.e
Y = PI / (PI**2 + mp.mpf('2'))
Y_INV = mp.mpf('1') / Y
PHI = (1 + mp.sqrt(5)) / 2  # Golden ratio

# Load target from validation
with open('/app/sandbox/session_20251215_122025_664f88889fdc/results/ubp_v4_validation.json', 'r') as f:
    validation = json.load(f)

TARGET_DELTA_TAU = mp.mpf(str(validation['phase_2_targets']['delta_tau']['value']))

print(f"\n🎯 Target: δ_τ = {float(TARGET_DELTA_TAU):.10f}")
print(f"\nFundamental Constants:")
print(f"  Y = {float(Y):.10f}")
print(f"  π = {float(PI):.10f}")
print(f"  e = {float(E):.10f}")
print(f"  φ = {float(PHI):.10f}")

# =============================================================================
# CANDIDATE EXPRESSIONS LIBRARY
# =============================================================================
def generate_candidates() -> Dict[str, mp.mpf]:
    """Generate library of candidate expressions."""
    candidates = {}

    # Direct constants
    candidates['Y'] = Y
    candidates['π'] = PI
    candidates['e'] = E
    candidates['φ'] = PHI

    # Powers of Y
    for n in range(1, 6):
        candidates[f'Y^{n}'] = Y**n
        candidates[f'Y^(-{n})'] = Y**(-n)
        candidates[f'Y^(1/{n})'] = Y**(mp.mpf(1)/mp.mpf(n))

    # Y combinations
    candidates['Y/π'] = Y / PI
    candidates['Y/e'] = Y / E
    candidates['Y/φ'] = Y / PHI
    candidates['Y²/π'] = (Y**2) / PI
    candidates['Y*π'] = Y * PI
    candidates['Y*e'] = Y * E
    candidates['Y/(1+Y)'] = Y / (1 + Y)
    candidates['Y/(1-Y)'] = Y / (1 - Y)

    # Ratios with integers
    for n in range(1, 11):
        for d in range(1, 11):
            if n != d:
                candidates[f'{n}Y/{d}'] = (mp.mpf(n) * Y) / mp.mpf(d)
                candidates[f'Y^{n}/{d}'] = (Y**n) / mp.mpf(d)

    # π and e combinations
    candidates['π/e'] = PI / E
    candidates['e/π'] = E / PI
    candidates['1/π'] = mp.mpf(1) / PI
    candidates['1/e'] = mp.mpf(1) / E
    candidates['π-e'] = PI - E
    candidates['e-π'] = E - PI

    # Special combinations
    candidates['Y/(Y+1)'] = Y / (Y + 1)
    candidates['Y/(Y+2)'] = Y / (Y + 2)
    candidates['Y/(Y+π)'] = Y / (Y + PI)
    candidates['Y²/Y_inv'] = (Y**2) / Y_INV
    candidates['Y*e/π'] = (Y * E) / PI
    candidates['Y*π/e'] = (Y * PI) / E

    # Transcendental combinations
    candidates['ln(Y)'] = mp.log(Y)
    candidates['exp(Y)'] = mp.exp(Y)
    candidates['exp(-Y)'] = mp.exp(-Y)
    candidates['sin(Y)'] = mp.sin(Y)
    candidates['cos(Y)'] = mp.cos(Y)

    # More complex
    candidates['Y/(π²+2)'] = Y * (PI**2 + 2)  # This should equal π
    candidates['√(Y)'] = mp.sqrt(Y)
    candidates['√(Y/π)'] = mp.sqrt(Y / PI)
    candidates['Y/√π'] = Y / mp.sqrt(PI)

    return candidates

# =============================================================================
# SEARCH AND RANK
# =============================================================================
print(f"\n{'='*80}")
print("Generating candidate expressions...")
start_time = time.time()

candidates = generate_candidates()
print(f"Generated {len(candidates)} candidates in {time.time()-start_time:.2f}s")

# Calculate errors
results = []
for expr, value in candidates.items():
    error = abs((value - TARGET_DELTA_TAU) / TARGET_DELTA_TAU) * 100
    results.append({
        'expression': expr,
        'value': float(value),
        'error_percent': float(error)
    })

# Sort by error
results.sort(key=lambda x: x['error_percent'])

# Display top 50 candidates
print(f"\n{'='*80}")
print("TOP 50 CANDIDATES (Ranked by Error)")
print('='*80)
print(f"{'Rank':<6}{'Expression':<25}{'Value':<18}{'Error %':<12}{'Status'}")
print('-'*80)

for i, result in enumerate(results[:50], 1):
    status = "✅✅✅" if result['error_percent'] < 0.001 else \
             "✅✅" if result['error_percent'] < 0.01 else \
             "✅" if result['error_percent'] < 0.1 else \
             "⚠️" if result['error_percent'] < 1.0 else ""

    print(f"{i:<6}{result['expression']:<25}{result['value']:<18.10f}{result['error_percent']:<12.6f}{status}")

    if i % 10 == 0:
        print()  # Add spacing every 10 rows

# =============================================================================
# OPTIMIZATION: FIND BEST INTEGER RATIO
# =============================================================================
print(f"\n{'='*80}")
print("OPTIMIZATION: Best Integer Ratio for Y")
print('='*80)

best_ratio = None
best_ratio_error = float('inf')

print("Searching n/d ratios where n,d ∈ [1,100]...")
count = 0
for n in range(1, 101):
    for d in range(1, 101):
        if count % 1000 == 0:
            print(f"Progress: {count}/10000 ratios tested...")

        ratio_value = (mp.mpf(n) / mp.mpf(d)) * Y
        error = abs((ratio_value - TARGET_DELTA_TAU) / TARGET_DELTA_TAU) * 100

        if error < best_ratio_error:
            best_ratio_error = error
            best_ratio = (n, d, float(ratio_value))

        count += 1

print(f"\n🎯 Best Integer Ratio:")
if best_ratio:
    n, d, val = best_ratio
    print(f"   δ_τ ≈ ({n}/{d}) × Y = {val:.10f}")
    print(f"   Error: {float(best_ratio_error):.6f}%")

# =============================================================================
# OPTIMIZATION: FIND BEST POWER LAW
# =============================================================================
print(f"\n{'='*80}")
print("OPTIMIZATION: Best Power Law")
print('='*80)

# Test Y^α for various α
print("Testing Y^α for α ∈ [-5, 5]...")
alpha_candidates = []
for alpha_int in range(-50, 51):  # Test α from -5 to 5 in steps of 0.1
    alpha = mp.mpf(alpha_int) / 10
    value = Y ** alpha
    error = abs((value - TARGET_DELTA_TAU) / TARGET_DELTA_TAU) * 100
    alpha_candidates.append((float(alpha), float(value), float(error)))

    if alpha_int % 10 == 0:
        print(f"  α = {float(alpha):.1f}: Y^α = {float(value):.10f}, error = {float(error):.6f}%")

# Find best alpha
best_alpha = min(alpha_candidates, key=lambda x: x[2])
print(f"\n🎯 Best Power Law:")
print(f"   δ_τ ≈ Y^{best_alpha[0]:.2f} = {best_alpha[1]:.10f}")
print(f"   Error: {best_alpha[2]:.6f}%")

# =============================================================================
# SAVE RESULTS
# =============================================================================
output = {
    "target": float(TARGET_DELTA_TAU),
    "top_50_candidates": results[:50],
    "best_integer_ratio": {
        "numerator": best_ratio[0] if best_ratio else None,
        "denominator": best_ratio[1] if best_ratio else None,
        "value": best_ratio[2] if best_ratio else None,
        "error_percent": float(best_ratio_error) if best_ratio else None
    },
    "best_power_law": {
        "alpha": best_alpha[0],
        "value": best_alpha[1],
        "error_percent": best_alpha[2]
    },
    "search_stats": {
        "total_candidates_tested": len(candidates),
        "integer_ratios_tested": 10000,
        "power_laws_tested": 101
    }
}

output_path = Path("/app/sandbox/session_20251215_122025_664f88889fdc/results/delta_tau_search.json")
with open(output_path, 'w') as f:
    json.dump(output, f, indent=2)

print(f"\n{'='*80}")
print(f"✅ Search complete")
print(f"📁 Results saved to: {output_path}")
print('='*80)
