"""
Deep diagnostic to understand what values are encoded in Y-refined patterns.
"""

import sys
sys.path.insert(0, '/home/ubuntu/UBP_Repo/ubp_3.4')

import numpy as np
from geometric_codex import GeometricCodex
from geometric_operations import GeometricUBP
from y_constants import calculate_y_constant, calculate_y_inverse, apply_bidirectional_refinement

# Initialize
codex = GeometricCodex(grid_size=128)
geo_ubp = GeometricUBP(grid_size=128)

Y = calculate_y_constant()
Y_inv = calculate_y_inverse()

print("="*80)
print("DEEP VALUE DIAGNOSTIC: What do transformed patterns encode?")
print("="*80)

# Test with Y_constant
test_value = Y
print(f"\nTest value: Y = {test_value:.15f}")

# Generate initial pattern
pattern_0, _ = codex.value_to_geometry(test_value, "dimensionless")
print(f"\nInitial pattern generated")

# Extract value from initial pattern
extracted_0, conf_0 = codex.geometry_to_value(pattern_0, "dimensionless")
print(f"  Extracted from initial: {extracted_0:.15f} (confidence: {conf_0:.3f})")
print(f"  Match: {abs(extracted_0 - test_value) / test_value < 0.01}")

# Apply forward Y-refinement (pure geometric)
print(f"\n{'='*80}")
print("FORWARD REFINEMENT (×Y)")
print("="*80)

result_forward = geo_ubp.apply_y_refinement(pattern_0, 'forward', mode='pure_geometric')
pattern_forward = result_forward.output_pattern

# Extract value from forward-refined pattern
extracted_forward, conf_forward = codex.geometry_to_value(pattern_forward, "dimensionless")
print(f"\nExtracted from forward-refined pattern: {extracted_forward:.15f} (confidence: {conf_forward:.3f})")

# What should it be?
print(f"\nPossible interpretations:")
print(f"  1. Original value: {test_value:.15f} (ratio: {extracted_forward/test_value:.6f})")
print(f"  2. Y × original: {test_value * Y:.15f} (ratio: {extracted_forward/(test_value*Y):.6f})")
print(f"  3. Y itself: {Y:.15f} (ratio: {extracted_forward/Y:.6f})")
print(f"  4. 1/Y (O_obs): {Y_inv:.15f} (ratio: {extracted_forward/Y_inv:.6f})")
print(f"  5. Y²: {Y**2:.15f} (ratio: {extracted_forward/(Y**2):.6f})")

# Apply backward refinement to forward result
print(f"\n{'='*80}")
print("BACKWARD REFINEMENT (×1/Y) on forward result")
print("="*80)

result_backward = geo_ubp.apply_y_refinement(pattern_forward, 'backward', mode='pure_geometric')
pattern_backward = result_backward.output_pattern

# Extract value from recovered pattern
extracted_backward, conf_backward = codex.geometry_to_value(pattern_backward, "dimensionless")
print(f"\nExtracted from recovered pattern: {extracted_backward:.15f} (confidence: {conf_backward:.3f})")
print(f"  Match to original: {abs(extracted_backward - test_value) / test_value < 0.01}")
print(f"  Ratio to original: {extracted_backward / test_value:.6f}")

# Now test with a frequency value
print(f"\n{'='*80}")
print("TEST WITH FREQUENCY VALUE")
print("="*80)

freq_value = 1.4042e9  # Electromagnetic main CRV
print(f"\nTest value: {freq_value:.6e} Hz")

# Generate pattern
pattern_freq_0, _ = codex.value_to_geometry(freq_value, "Hz")

# Extract
extracted_freq_0, conf_freq_0 = codex.geometry_to_value(pattern_freq_0, "Hz")
print(f"Extracted from initial: {extracted_freq_0:.6e} Hz (confidence: {conf_freq_0:.3f})")
print(f"  Ratio: {extracted_freq_0 / freq_value:.6f}")

# Forward refinement
result_freq_forward = geo_ubp.apply_y_refinement(pattern_freq_0, 'forward', mode='pure_geometric')
extracted_freq_forward, conf_freq_forward = codex.geometry_to_value(
    result_freq_forward.output_pattern, "Hz"
)
print(f"\nExtracted from forward-refined: {extracted_freq_forward:.6e} Hz (confidence: {conf_freq_forward:.3f})")
print(f"  Ratio to original: {extracted_freq_forward / freq_value:.6f}")
print(f"  Ratio to Y×original: {extracted_freq_forward / (freq_value * Y):.6f}")

# Backward refinement
result_freq_backward = geo_ubp.apply_y_refinement(
    result_freq_forward.output_pattern, 'backward', mode='pure_geometric'
)
extracted_freq_backward, conf_freq_backward = codex.geometry_to_value(
    result_freq_backward.output_pattern, "Hz"
)
print(f"\nExtracted from recovered: {extracted_freq_backward:.6e} Hz (confidence: {conf_freq_backward:.3f})")
print(f"  Ratio to original: {extracted_freq_backward / freq_value:.6f}")

# Summary
print(f"\n{'='*80}")
print("SUMMARY")
print("="*80)
print(f"\nPattern encoding behavior:")
print(f"  - Initial pattern encodes: THE INPUT VALUE")
print(f"  - Forward-refined pattern encodes: ???")
print(f"  - Recovered pattern encodes: ???")
print(f"\nClosure quality:")
print(f"  - Dimensionless: {abs(extracted_backward - test_value) / test_value:.6f}")
print(f"  - Frequency: {abs(extracted_freq_backward - freq_value) / freq_value:.6f}")
