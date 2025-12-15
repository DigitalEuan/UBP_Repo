#!/usr/bin/env python3
"""
Investigation of CKM Matrix and Fine Structure Constant

Investigate if these fundamental observables have geometric relationships
with the UBP constants (Y, π, e).

CKM Matrix: Quark mixing angles (Cabibbo-Kobayashi-Maskawa)
Fine Structure Constant: α ≈ 1/137.036
"""

import mpmath as mp
import json
from pathlib import Path
from typing import Dict, List

# Set ultra-high precision
mp.mp.dps = 200

print("="*80)
print("INVESTIGATION: CKM Matrix & Fine Structure Constant")
print("="*80)

# =============================================================================
# SETUP CONSTANTS
# =============================================================================
PI = mp.pi
E = mp.e
Y = PI / (PI**2 + mp.mpf('2'))
Y_INV = mp.mpf('1') / Y

# PDG 2024 - CKM Matrix elements (magnitudes)
CKM_PDG = {
    'V_ud': mp.mpf('0.97435'),  # Up-Down
    'V_us': mp.mpf('0.22500'),  # Up-Strange (Cabibbo angle)
    'V_ub': mp.mpf('0.00382'),  # Up-Bottom
    'V_cd': mp.mpf('0.22486'),  # Charm-Down
    'V_cs': mp.mpf('0.97349'),  # Charm-Strange
    'V_cb': mp.mpf('0.04221'),  # Charm-Bottom
    'V_td': mp.mpf('0.00849'),  # Top-Down
    'V_ts': mp.mpf('0.04053'),  # Top-Strange
    'V_tb': mp.mpf('0.99910'),  # Top-Bottom
}

# Cabibbo angle (most precisely measured)
THETA_C = mp.asin(CKM_PDG['V_us'])  # radians
THETA_C_DEG = THETA_C * 180 / PI

# Fine structure constant
ALPHA_EM = mp.mpf('1') / mp.mpf('137.035999206')
ALPHA_INV = mp.mpf('137.035999206')

print(f"\nCKM Matrix (PDG 2024):")
print("  | V_ud       V_us       V_ub    |")
print(f"  | {float(CKM_PDG['V_ud']):.5f}    {float(CKM_PDG['V_us']):.5f}    {float(CKM_PDG['V_ub']):.5f} |")
print(f"  | {float(CKM_PDG['V_cd']):.5f}    {float(CKM_PDG['V_cs']):.5f}    {float(CKM_PDG['V_cb']):.5f} |")
print(f"  | {float(CKM_PDG['V_td']):.5f}    {float(CKM_PDG['V_ts']):.5f}    {float(CKM_PDG['V_tb']):.5f} |")

print(f"\nCabibbo Angle:")
print(f"  θ_c = {float(THETA_C_DEG):.6f}°")
print(f"  sin(θ_c) = V_us = {float(CKM_PDG['V_us']):.6f}")

print(f"\nFine Structure Constant:")
print(f"  α = {float(ALPHA_EM):.12f}")
print(f"  1/α = {float(ALPHA_INV):.12f}")

# =============================================================================
# CKM MATRIX INVESTIGATION
# =============================================================================
print(f"\n{'='*80}")
print("CKM MATRIX INVESTIGATION")
print('='*80)

def test_ckm_expression(expr_name, expr_value, target_value, target_name):
    """Test if an expression matches a CKM element."""
    error = abs((expr_value - target_value) / target_value) * 100
    status = "✅✅✅" if error < 0.1 else "✅✅" if error < 1.0 else "✅" if error < 5.0 else "❌"
    return {
        'expression': expr_name,
        'target': target_name,
        'value': float(expr_value),
        'target_value': float(target_value),
        'error_percent': float(error),
        'status': status
    }

ckm_results = []

print("\nTesting geometric expressions against CKM elements...")

# Test V_us (Cabibbo angle) - most precisely measured
print("\n1. V_us (Cabibbo Angle) Tests:")
candidates_vus = {
    'Y': Y,
    'Y/π': Y/PI,
    'Y²': Y**2,
    '√Y': mp.sqrt(Y),
    'Y/e': Y/E,
    '1/4': mp.mpf('0.25'),
    '2/9': mp.mpf(2)/mp.mpf(9),
    'sin(Y)': mp.sin(Y),
    'sin(π/14)': mp.sin(PI/14),
    'sin(π/13)': mp.sin(PI/13),
    'Y^0.8': Y**mp.mpf('0.8'),
}

for name, value in candidates_vus.items():
    result = test_ckm_expression(name, value, CKM_PDG['V_us'], 'V_us')
    ckm_results.append(result)
    if result['error_percent'] < 10:
        print(f"   {name:15s} = {result['value']:.6f}  (Error: {result['error_percent']:.3f}%) {result['status']}")

# Test V_ud (nearly 1)
print("\n2. V_ud Tests (Close to Unity):")
candidates_vud = {
    '1 - Y/4': 1 - Y/4,
    '1 - Y²/10': 1 - (Y**2)/10,
    'cos(π/14)': mp.cos(PI/14),
    'cos(π/13)': mp.cos(PI/13),
    '√(1-Y²)': mp.sqrt(1 - Y**2),
}

for name, value in candidates_vud.items():
    result = test_ckm_expression(name, value, CKM_PDG['V_ud'], 'V_ud')
    ckm_results.append(result)
    if result['error_percent'] < 5:
        print(f"   {name:15s} = {result['value']:.6f}  (Error: {result['error_percent']:.3f}%) {result['status']}")

# Test Cabibbo angle itself
print("\n3. Cabibbo Angle θ_c Tests:")
angle_candidates = {
    'π/24': float(PI/24 * 180/PI),
    'π/23': float(PI/23 * 180/PI),
    'π/22': float(PI/22 * 180/PI),
    'Y×50': float(Y * 50),
    'arcsin(Y)': float(mp.asin(Y) * 180/PI),
}

for name, value in angle_candidates.items():
    error = abs((value - float(THETA_C_DEG)) / float(THETA_C_DEG)) * 100
    status = "✅" if error < 5 else "❌"
    print(f"   {name:15s} = {value:.6f}°  (Target: {float(THETA_C_DEG):.6f}°, Error: {error:.3f}%) {status}")

# =============================================================================
# FINE STRUCTURE CONSTANT INVESTIGATION
# =============================================================================
print(f"\n{'='*80}")
print("FINE STRUCTURE CONSTANT (α) INVESTIGATION")
print('='*80)

alpha_results = []

print("\nTesting geometric expressions against 1/α = 137.036...")

candidates_alpha = {
    '4π²': 4 * PI**2,
    '4π² + 1': 4 * PI**2 + 1,
    '4π² - 1': 4 * PI**2 - 1,
    'π^4': PI**4,
    'e^4 + π': E**4 + PI,
    '(π+e)^3': (PI + E)**3,
    '5π² + e²': 5 * (PI**2) + E**2,
    '137': mp.mpf('137'),
    'π^4 + π² + 1': PI**4 + PI**2 + 1,
    '(1/Y)^3 * 10': (Y_INV**3) * 10,
}

for name, value in candidates_alpha.items():
    error = abs((value - ALPHA_INV) / ALPHA_INV) * 100
    status = "✅✅✅" if float(error) < 0.1 else "✅✅" if float(error) < 1.0 else "✅" if float(error) < 5.0 else "❌"
    alpha_results.append({
        'expression': name,
        'value': float(value),
        'target': float(ALPHA_INV),
        'error_percent': float(error),
        'status': status
    })
    if float(error) < 20:
        print(f"   {name:25s} = {float(value):.6f}  (Error: {float(error):.3f}%) {status}")

# =============================================================================
# ANALYSIS & CONCLUSIONS
# =============================================================================
print(f"\n{'='*80}")
print("ANALYSIS & CONCLUSIONS")
print('='*80)

# Find best CKM matches
ckm_sorted = sorted(ckm_results, key=lambda x: x['error_percent'])
print("\nBest CKM Matrix Matches:")
for i, result in enumerate(ckm_sorted[:5], 1):
    print(f"  {i}. {result['target']:6s}: {result['expression']:15s} = {result['value']:.6f}  "
          f"(Error: {result['error_percent']:.3f}%) {result['status']}")

# Find best alpha matches
alpha_sorted = sorted(alpha_results, key=lambda x: x['error_percent'])
print("\nBest 1/α Matches:")
for i, result in enumerate(alpha_sorted[:5], 1):
    print(f"  {i}. {result['expression']:25s} = {result['value']:.6f}  "
          f"(Error: {result['error_percent']:.3f}%) {result['status']}")

# Overall conclusions
print(f"\n{'='*80}")
print("SCIENTIFIC CONCLUSIONS:")
print('-'*80)

# Check if we found any strong matches
ckm_strong_matches = [r for r in ckm_results if r['error_percent'] < 1.0]
alpha_strong_matches = [r for r in alpha_results if r['error_percent'] < 1.0]

if len(ckm_strong_matches) > 0:
    print("\n✅ CKM Matrix: Found geometric relationships!")
    for match in ckm_strong_matches:
        print(f"   • {match['target']} ≈ {match['expression']} (Error: {match['error_percent']:.3f}%)")
else:
    print("\n⚠️  CKM Matrix: No strong geometric relationships found (<1% error).")
    print("   The CKM matrix elements may not directly follow from Y, π, e.")
    print("   This suggests quark mixing is governed by different dynamics.")

if len(alpha_strong_matches) > 0:
    print("\n✅ Fine Structure Constant: Found geometric relationships!")
    for match in alpha_strong_matches:
        print(f"   • 1/α ≈ {match['expression']} (Error: {match['error_percent']:.3f}%)")
else:
    print("\n⚠️  Fine Structure Constant: No strong geometric relationships found (<1% error).")
    print("   The value 1/α ≈ 137.036 does not appear to directly follow from Y, π, e.")
    print("   This is consistent with α being an independent electromagnetic coupling.")

# =============================================================================
# SAVE RESULTS
# =============================================================================
output = {
    "ckm_matrix": {
        "pdg_values": {k: float(v) for k, v in CKM_PDG.items()},
        "cabibbo_angle_deg": float(THETA_C_DEG),
        "test_results": ckm_sorted,
        "strong_matches": ckm_strong_matches
    },
    "fine_structure_constant": {
        "alpha": float(ALPHA_EM),
        "alpha_inverse": float(ALPHA_INV),
        "test_results": alpha_sorted,
        "strong_matches": alpha_strong_matches
    },
    "conclusions": {
        "ckm_has_geometric_basis": len(ckm_strong_matches) > 0,
        "alpha_has_geometric_basis": len(alpha_strong_matches) > 0
    }
}

output_path = Path("/app/sandbox/session_20251215_122025_664f88889fdc/results/ckm_alpha_analysis.json")
with open(output_path, 'w') as f:
    json.dump(output, f, indent=2)

print(f"\n{'='*80}")
print(f"✅ Investigation complete")
print(f"📁 Results saved to: {output_path}")
print('='*80)
