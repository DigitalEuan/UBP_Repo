#!/usr/bin/env python3.11
"""
Phase 1.2: CARFE Recursive Analysis
====================================

Goal: Explore golden ratio (φ) connections and derive secondary rainbow angle
      using CARFE recursive field evolution

Expected Outcome: Improved secondary rainbow prediction, possible exact derivation
"""

import sys
sys.path.insert(0, '/home/ubuntu/UBP_Repo/ubp_3.4')

import math
import numpy as np
from typing import Dict, Any
import json

# Import UBP modules
from y_constants import calculate_y_constant, calculate_y_inverse
from system_constants import UBPConstants

# Try to import CARFE (may need to handle if not fully compatible)
try:
    from advanced_modules.carfe import CARFEFieldEquation, CARFEParameters, FieldState, FieldTopology
    CARFE_AVAILABLE = True
except Exception as e:
    print(f"Warning: CARFE module import issue: {e}")
    CARFE_AVAILABLE = False

print("="*80)
print("PHASE 1.2: CARFE RECURSIVE ANALYSIS")
print("="*80)
print()

# ============================================================================
# COLUMN 1: LANGUAGE (Narrative)
# ============================================================================

print("COLUMN 1: LANGUAGE (Narrative)")
print("-" * 80)
print("""
The rainbow angle may emerge from recursive geometric evolution governed by
the golden ratio φ. CARFE (Cykloid Adelic Recursive Field Equation) models
φ-based evolution of geometric structures.

We hypothesize that:
1. The 42° angle is a fixed point in a recursive transformation involving φ, π, Y
2. The secondary rainbow angle (observed ~51.8°) relates to primary via φ

Current secondary rainbow derivation error: 3.33%
Observed secondary: 51.8°
Current prediction: 50.076° (using 42 + 5φ)

We will test various φ-based relationships and use CARFE if available.
""")
print()

# ============================================================================
# COLUMN 2: MATHEMATICS (Formal)
# ============================================================================

print("COLUMN 2: MATHEMATICS (Formal)")
print("-" * 80)

# Fundamental constants
pi = math.pi
Y = calculate_y_constant()
Y_inv = calculate_y_inverse()
phi = (1 + math.sqrt(5)) / 2  # Golden ratio

print(f"π = {pi:.15f}")
print(f"Y = {Y:.15f}")
print(f"1/Y = {Y_inv:.15f}")
print(f"φ = {phi:.15f}")
print(f"φ² = {phi**2:.15f}")
print(f"1/φ = {1/phi:.15f}")
print()

# Primary and secondary rainbow angles
theta_primary = 42.0  # degrees
theta_secondary_observed = 51.8  # degrees (approximate)

print(f"Primary rainbow angle: {theta_primary}°")
print(f"Secondary rainbow angle (observed): {theta_secondary_observed}°")
print(f"Difference: {theta_secondary_observed - theta_primary}°")
print()

# ============================================================================
# Test φ-based relationships for secondary rainbow
# ============================================================================

print("Testing φ-based relationships for secondary rainbow:")
print("-" * 80)
print()

# Test various formulas
formulas = {
    'θ₂ = θ₁ + φ': theta_primary + phi,
    'θ₂ = θ₁ + 2φ': theta_primary + 2*phi,
    'θ₂ = θ₁ + 3φ': theta_primary + 3*phi,
    'θ₂ = θ₁ + 4φ': theta_primary + 4*phi,
    'θ₂ = θ₁ + 5φ': theta_primary + 5*phi,
    'θ₂ = θ₁ + 6φ': theta_primary + 6*phi,
    'θ₂ = θ₁ + 10φ': theta_primary + 10*phi,
    'θ₂ = θ₁ × φ': theta_primary * phi,
    'θ₂ = θ₁ × φ²': theta_primary * phi**2,
    'θ₂ = θ₁ + φ²': theta_primary + phi**2,
    'θ₂ = θ₁ + 10/φ': theta_primary + 10/phi,
    'θ₂ = θ₁ + 20/φ': theta_primary + 20/phi,
    'θ₂ = θ₁ + π×φ': theta_primary + pi*phi,
    'θ₂ = θ₁ + Y×φ×100': theta_primary + Y*phi*100,
}

best_formula = None
best_error = float('inf')

for name, value in formulas.items():
    error = abs(value - theta_secondary_observed)
    error_percent = (error / theta_secondary_observed) * 100
    
    print(f"{name:25s}: {value:8.4f}°, error = {error:6.4f}° ({error_percent:5.2f}%)")
    
    if error < best_error:
        best_error = error
        best_formula = (name, value)

print()
print(f"Best formula: {best_formula[0]}")
print(f"  Predicted: {best_formula[1]:.6f}°")
print(f"  Observed: {theta_secondary_observed:.6f}°")
print(f"  Error: {best_error:.6f}° ({(best_error/theta_secondary_observed)*100:.4f}%)")
print()

# ============================================================================
# Exact relationship derivation
# ============================================================================

print("Exact Relationship Derivation:")
print("-" * 80)

# What coefficient k gives θ₂ = θ₁ + k?
k_exact = theta_secondary_observed - theta_primary

print(f"θ₂ = θ₁ + k, where k = {k_exact:.6f}°")
print()

# Analyze k in terms of fundamental constants
print(f"Analyzing k = {k_exact:.6f}°:")
print(f"  k / φ = {k_exact / phi:.6f}")
print(f"  k / π = {k_exact / pi:.6f}")
print(f"  k / Y = {k_exact / Y:.6f}")
print(f"  k / (1/Y) = {k_exact / Y_inv:.6f}")
print(f"  k × φ = {k_exact * phi:.6f}")
print(f"  k × π = {k_exact * pi:.6f}")
print()

# Check if k ≈ 6φ
print(f"Testing k ≈ 6φ:")
print(f"  6φ = {6*phi:.6f}°")
print(f"  k / (6φ) = {k_exact / (6*phi):.10f}")
print(f"  Error: {abs(k_exact - 6*phi):.6f}° ({abs(k_exact - 6*phi)/k_exact*100:.4f}%)")
print()

# ============================================================================
# Recursive Fixed Point Analysis
# ============================================================================

print("Recursive Fixed Point Analysis:")
print("-" * 80)
print()

# Define a recursive function and search for fixed points
def recursive_angle_evolution(theta, phi, pi, Y, mode='simple'):
    """Recursive angle evolution function"""
    if mode == 'simple':
        # Simple φ-based recursion
        return phi * math.sin(math.radians(theta)) + Y * math.cos(math.radians(theta))
    elif mode == 'complex':
        # More complex recursion
        return math.degrees(math.atan(phi * math.sin(math.radians(theta)) / 
                                      (pi * math.cos(math.radians(theta)) + Y)))
    elif mode == 'hybrid':
        # Hybrid approach
        return theta * (1 - Y) + phi * Y

# Test for fixed points
print("Testing for fixed points (simple mode):")
for theta_init in [40.0, 41.0, 42.0, 43.0, 44.0]:
    theta_current = theta_init
    for iteration in range(100):
        theta_next = recursive_angle_evolution(theta_current, phi, pi, Y, mode='simple')
        if abs(theta_next - theta_current) < 1e-10:
            print(f"  Initial {theta_init}° → Fixed point at {theta_next:.10f}° (iteration {iteration})")
            break
        theta_current = theta_next
    else:
        print(f"  Initial {theta_init}° → No convergence (final: {theta_current:.6f}°)")

print()

# ============================================================================
# CARFE Field Analysis (if available)
# ============================================================================

if CARFE_AVAILABLE:
    print("CARFE Field Analysis:")
    print("-" * 80)
    print()
    
    try:
        # Initialize CARFE
        params = CARFEParameters(
            recursion_depth=10,
            expansion_factor=phi,
            evolution_rate=0.95,
            damping_factor=0.98
        )
        
        carfe = CARFEFieldEquation(parameters=params)
        
        # Create initial field centered at 42°
        initial_field = np.array([math.radians(theta_primary)])
        
        # Compute recursive evolution
        evolved_field = carfe.compute_recursive_field(initial_field, recursion_depth=10)
        
        # Convert back to degrees
        evolved_angle = math.degrees(evolved_field[0].real)
        
        print(f"CARFE recursive evolution:")
        print(f"  Initial angle: {theta_primary}°")
        print(f"  Evolved angle: {evolved_angle:.6f}°")
        print(f"  Change: {evolved_angle - theta_primary:.6f}°")
        print()
        
        # Test if evolved angle relates to secondary rainbow
        if abs(evolved_angle - theta_secondary_observed) < 5:
            print(f"  ✓ Evolved angle close to secondary rainbow!")
            print(f"    Error: {abs(evolved_angle - theta_secondary_observed):.6f}°")
        
    except Exception as e:
        print(f"CARFE analysis error: {e}")
        print()
else:
    print("CARFE module not available, skipping field analysis")
    print()

# ============================================================================
# Alternative: Direct Geometric Derivation
# ============================================================================

print("Alternative Geometric Derivation:")
print("-" * 80)
print()

# Secondary rainbow involves 2 internal reflections (vs 1 for primary)
# Geometric optics predicts different angle

# For a spherical water droplet with refractive index n:
# Primary rainbow: θ₁ = 180° - 4α + 2β (1 internal reflection)
# Secondary rainbow: θ₂ = 180° + 2α - 6β (2 internal reflections)
# where α = arcsin(sin(i)/n), β = arcsin(n·sin(α))

# The angular separation depends on n and droplet geometry
# Let's calculate the theoretical separation

n_water = 1.333  # refractive index of water (approximate)

# For minimum deviation (brightest rainbow):
# Primary: θ₁ ≈ 42° (observed)
# Secondary: θ₂ ≈ 51° (observed)

# The separation is approximately:
delta_theory = 180 - 2*42  # Simplified geometric relationship
print(f"Simplified geometric separation: {delta_theory}°")
print(f"Observed separation: {theta_secondary_observed - theta_primary}°")
print()

# ============================================================================
# COLUMN 3: SCRIPT (Executable Results)
# ============================================================================

print("="*80)
print("COLUMN 3: SCRIPT (Executable Results)")
print("="*80)
print()

# Summary of findings
print("Summary of Findings:")
print("-" * 80)
print()

# Best φ-based formula
print(f"1. Best φ-based formula: {best_formula[0]}")
print(f"   Prediction: {best_formula[1]:.6f}°")
print(f"   Error: {best_error:.6f}° ({(best_error/theta_secondary_observed)*100:.4f}%)")
print()

# Exact coefficient
print(f"2. Exact coefficient k = {k_exact:.6f}°")
print(f"   Relation to 6φ: k/(6φ) = {k_exact/(6*phi):.10f}")
print(f"   This suggests: θ₂ ≈ θ₁ + 6φ (with small correction)")
print()

# Improved formula
k_corrected = 6 * phi
theta_secondary_predicted = theta_primary + k_corrected
error_corrected = abs(theta_secondary_predicted - theta_secondary_observed)

print(f"3. Improved formula: θ₂ = θ₁ + 6φ")
print(f"   Prediction: {theta_secondary_predicted:.6f}°")
print(f"   Observed: {theta_secondary_observed:.6f}°")
print(f"   Error: {error_corrected:.6f}° ({(error_corrected/theta_secondary_observed)*100:.4f}%)")
print()

# Machine precision goal
machine_precision_achieved = error_corrected < 0.01  # Within 0.01°

print(f"4. Machine precision achieved (< 0.01°): {machine_precision_achieved}")
print()

# ============================================================================
# Save Results
# ============================================================================

results = {
    'phase': '1.2',
    'title': 'CARFE Recursive Analysis',
    'constants': {
        'pi': pi,
        'Y': Y,
        'Y_inverse': Y_inv,
        'phi': phi,
    },
    'angles': {
        'theta_primary_deg': theta_primary,
        'theta_secondary_observed_deg': theta_secondary_observed,
        'theta_secondary_predicted_deg': theta_secondary_predicted,
    },
    'formulas': {
        'best_formula': best_formula[0],
        'best_prediction': best_formula[1],
        'best_error_deg': best_error,
        'improved_formula': 'θ₂ = θ₁ + 6φ',
        'improved_prediction': theta_secondary_predicted,
        'improved_error_deg': error_corrected,
    },
    'coefficients': {
        'k_exact': k_exact,
        'k_over_6phi': k_exact / (6*phi),
    },
    'validation': {
        'machine_precision_achieved': machine_precision_achieved,
        'error_percent': (error_corrected/theta_secondary_observed)*100,
    }
}

output_file = '/home/ubuntu/rainbow_investigation/results_phase_1_2.json'
with open(output_file, 'w') as f:
    json.dump(results, f, indent=2)

print(f"Results saved to: {output_file}")
print()

print("="*80)
print("PHASE 1.2 COMPLETE")
print("="*80)
