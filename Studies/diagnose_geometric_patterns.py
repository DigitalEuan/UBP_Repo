"""
Diagnostic script to analyze differences between pure geometric and hybrid operations.
"""

import sys
sys.path.insert(0, '/home/ubuntu/UBP_Repo/ubp_3.4')

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy.fft import fft2, fftshift

from geometric_codex import GeometricCodex
from geometric_operations import GeometricUBP
from y_constants import calculate_y_constant, calculate_y_inverse

# Initialize
codex = GeometricCodex(grid_size=128)
geo_ubp = GeometricUBP(grid_size=128)

# Test with Y_constant
Y = calculate_y_constant()
print(f"Testing with Y_constant = {Y:.15f}")

# Generate initial pattern
pattern, sig = codex.value_to_geometry(Y, "dimensionless")
print(f"\nInitial pattern:")
print(f"  Shape: {pattern.shape}")
print(f"  Mean: {np.mean(pattern):.6f}")
print(f"  Std: {np.std(pattern):.6f}")
print(f"  Min: {np.min(pattern):.6f}")
print(f"  Max: {np.max(pattern):.6f}")

# Apply forward refinement - PURE GEOMETRIC
print("\n" + "="*80)
print("FORWARD REFINEMENT (×Y)")
print("="*80)

pure_result = geo_ubp.apply_y_refinement(pattern, 'forward', mode='pure_geometric')
print(f"\nPure Geometric Result:")
print(f"  Mean: {np.mean(pure_result.output_pattern):.6f}")
print(f"  Std: {np.std(pure_result.output_pattern):.6f}")
print(f"  Quality: {pure_result.pattern_quality:.6f}")
print(f"  Closure: {pure_result.closure_quality:.6f}")
print(f"  NRCI: {pure_result.nrci_estimate:.6f}")

# Apply forward refinement - HYBRID
hybrid_result = geo_ubp.apply_y_refinement(pattern, 'forward', mode='hybrid')
print(f"\nHybrid Result:")
print(f"  Input value: {hybrid_result.input_value:.6e}")
print(f"  Output value: {hybrid_result.output_value:.6e}")
print(f"  Mean: {np.mean(hybrid_result.output_pattern):.6f}")
print(f"  Std: {np.std(hybrid_result.output_pattern):.6f}")
print(f"  Quality: {hybrid_result.pattern_quality:.6f}")
print(f"  Closure: {hybrid_result.closure_quality:.6f}")

# Analyze frequency content
print("\n" + "="*80)
print("FREQUENCY ANALYSIS")
print("="*80)

def analyze_frequency(pattern, name):
    fft_pattern = fftshift(fft2(pattern))
    magnitude = np.abs(fft_pattern)
    
    # Get central region (low frequencies)
    center = magnitude.shape[0] // 2
    low_freq = magnitude[center-10:center+10, center-10:center+10]
    
    # Get edge region (high frequencies)
    high_freq = magnitude.copy()
    high_freq[center-10:center+10, center-10:center+10] = 0
    
    print(f"\n{name}:")
    print(f"  Total power: {np.sum(magnitude):.6e}")
    print(f"  Low freq power: {np.sum(low_freq):.6e}")
    print(f"  High freq power: {np.sum(high_freq):.6e}")
    print(f"  High/Low ratio: {np.sum(high_freq)/(np.sum(low_freq)+1e-10):.6f}")
    
    return magnitude

mag_original = analyze_frequency(pattern, "Original Pattern")
mag_pure = analyze_frequency(pure_result.output_pattern, "Pure Geometric")
mag_hybrid = analyze_frequency(hybrid_result.output_pattern, "Hybrid")

# Compare patterns directly
print("\n" + "="*80)
print("PATTERN COMPARISON")
print("="*80)

# Normalized cross-correlation
p1_norm = (pure_result.output_pattern - np.mean(pure_result.output_pattern)) / (np.std(pure_result.output_pattern) + 1e-10)
p2_norm = (hybrid_result.output_pattern - np.mean(hybrid_result.output_pattern)) / (np.std(hybrid_result.output_pattern) + 1e-10)

correlation = np.mean(p1_norm * p2_norm)
similarity = (correlation + 1) / 2

print(f"\nPattern Similarity: {similarity:.6f}")
print(f"Correlation: {correlation:.6f}")

# Pixel-wise difference
diff = np.abs(pure_result.output_pattern - hybrid_result.output_pattern)
print(f"\nPixel-wise difference:")
print(f"  Mean: {np.mean(diff):.6f}")
print(f"  Max: {np.max(diff):.6f}")
print(f"  Relative: {np.mean(diff)/(np.std(pattern)+1e-10):.6f}")

# Frequency domain difference
freq_diff = np.abs(mag_pure - mag_hybrid)
print(f"\nFrequency domain difference:")
print(f"  Mean: {np.mean(freq_diff):.6e}")
print(f"  Max: {np.max(freq_diff):.6e}")

# Visualize
fig, axes = plt.subplots(2, 3, figsize=(15, 10))

axes[0, 0].imshow(pattern, cmap='RdBu_r')
axes[0, 0].set_title('Original Pattern')
axes[0, 0].axis('off')

axes[0, 1].imshow(pure_result.output_pattern, cmap='RdBu_r')
axes[0, 1].set_title(f'Pure Geometric (×Y)\nQuality: {pure_result.pattern_quality:.3f}')
axes[0, 1].axis('off')

axes[0, 2].imshow(hybrid_result.output_pattern, cmap='RdBu_r')
axes[0, 2].set_title(f'Hybrid (×Y)\nQuality: {hybrid_result.pattern_quality:.3f}')
axes[0, 2].axis('off')

axes[1, 0].imshow(np.log10(mag_original + 1), cmap='viridis')
axes[1, 0].set_title('Original FFT')
axes[1, 0].axis('off')

axes[1, 1].imshow(np.log10(mag_pure + 1), cmap='viridis')
axes[1, 1].set_title('Pure Geometric FFT')
axes[1, 1].axis('off')

axes[1, 2].imshow(np.log10(mag_hybrid + 1), cmap='viridis')
axes[1, 2].set_title('Hybrid FFT')
axes[1, 2].axis('off')

plt.tight_layout()
plt.savefig('/home/ubuntu/UBP_Repo/Studies/pattern_diagnostic.png', dpi=150, bbox_inches='tight')
print(f"\nVisualization saved to: pattern_diagnostic.png")

# Test the REAL question: Do they encode the same VALUE?
print("\n" + "="*80)
print("VALUE EXTRACTION TEST")
print("="*80)

# Extract values from both result patterns
pure_extracted, pure_conf = codex.geometry_to_value(pure_result.output_pattern, "dimensionless")
hybrid_extracted, hybrid_conf = codex.geometry_to_value(hybrid_result.output_pattern, "dimensionless")

print(f"\nValue extraction from results:")
print(f"  Pure geometric: {pure_extracted:.6e} (confidence: {pure_conf:.3f})")
print(f"  Hybrid: {hybrid_extracted:.6e} (confidence: {hybrid_conf:.3f})")
print(f"  Expected (Y×Y): {Y*Y:.6e}")
print(f"  Ratio (pure/expected): {pure_extracted/(Y*Y):.6f}")
print(f"  Ratio (hybrid/expected): {hybrid_extracted/(Y*Y):.6f}")

print("\n" + "="*80)
print("CONCLUSION")
print("="*80)

if abs(pure_extracted - hybrid_extracted) / (hybrid_extracted + 1e-10) < 0.1:
    print("✓ Both methods encode similar VALUES despite different patterns!")
    print("  This suggests they are geometrically equivalent representations.")
else:
    print("✗ Methods encode different values - operation mismatch.")
