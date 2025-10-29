"""
Double-Slit Interference Data - UBP Framework Analysis
=======================================================

This script analyzes real experimental double-slit interference data
using the Universal Binary Principle framework to test the hypothesis
that light exhibits Information ↔ Activation layer fluctuation.

Author: Euan R A Craig & Manus AI
Date: October 29, 2025
"""

import numpy as np
import pandas as pd
import json
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
from scipy.fft import fft, fftfreq

print("="*70)
print("DOUBLE-SLIT INTERFERENCE - UBP ANALYSIS")
print("="*70)

# ============================================================================
# PART 1: LOAD DATA
# ============================================================================

print(f"\n{'='*70}")
print("PART 1: Loading Double-Slit Interference Data")
print("="*70)

data_file = "/home/ubuntu/nist_real_data/Data_D2He_DoubleSlitScattering.xlsx"

# Load all three sheets
sheet_names = ['45°', '135°', 'X']
datasets = {}

for sheet in sheet_names:
    try:
        df = pd.read_excel(data_file, sheet_name=sheet)
        datasets[sheet] = df
        print(f"\n✓ Loaded {sheet}: {len(df)} data points")
        print(f"  Columns: {list(df.columns)}")
    except Exception as e:
        print(f"  Error loading {sheet}: {e}")

# ============================================================================
# PART 2: ANALYZE INTERFERENCE PATTERNS
# ============================================================================

print(f"\n{'='*70}")
print("PART 2: Analyzing Interference Patterns")
print("="*70)

def analyze_interference_pattern(angles, counts, label):
    """Analyze an interference pattern"""
    
    # Find peaks (maxima)
    peaks, properties = find_peaks(counts, height=np.mean(counts))
    
    # Find troughs (minima)
    troughs, _ = find_peaks(-counts, height=-np.mean(counts))
    
    # Calculate visibility (contrast)
    if len(peaks) > 0 and len(troughs) > 0:
        I_max = np.mean(counts[peaks])
        I_min = np.mean(counts[troughs])
        visibility = (I_max - I_min) / (I_max + I_min) if (I_max + I_min) > 0 else 0
    else:
        visibility = 0
    
    # Calculate fringe spacing
    if len(peaks) > 1:
        peak_angles = angles[peaks]
        fringe_spacing = np.mean(np.diff(peak_angles))
    else:
        fringe_spacing = 0
    
    # FFT to find dominant frequencies
    fft_vals = np.abs(fft(counts - np.mean(counts)))
    freqs = fftfreq(len(counts), d=np.mean(np.diff(angles)))
    
    # Find dominant frequency (excluding DC component)
    dominant_freq_idx = np.argmax(fft_vals[1:len(fft_vals)//2]) + 1
    dominant_freq = np.abs(freqs[dominant_freq_idx])
    
    results = {
        'label': label,
        'num_peaks': len(peaks),
        'num_troughs': len(troughs),
        'visibility': visibility,
        'fringe_spacing': fringe_spacing,
        'dominant_frequency': dominant_freq,
        'mean_intensity': np.mean(counts),
        'std_intensity': np.std(counts),
        'peak_positions': angles[peaks].tolist() if len(peaks) > 0 else [],
        'trough_positions': angles[troughs].tolist() if len(troughs) > 0 else []
    }
    
    return results, peaks, troughs

# Analyze each dataset
analysis_results = {}

for sheet, df in datasets.items():
    # Extract columns (assuming first column is angle, second is counts)
    angles = df.iloc[:, 0].values
    counts = df.iloc[:, 1].values
    
    results, peaks, troughs = analyze_interference_pattern(angles, counts, sheet)
    analysis_results[sheet] = results
    
    print(f"\n{sheet}:")
    print(f"  Peaks: {results['num_peaks']}, Troughs: {results['num_troughs']}")
    print(f"  Visibility: {results['visibility']:.4f}")
    print(f"  Fringe spacing: {results['fringe_spacing']:.6f}°")
    print(f"  Dominant frequency: {results['dominant_frequency']:.6f} cycles/degree")

# ============================================================================
# PART 3: EXTRACT BINARY SEQUENCES FROM INTERFERENCE
# ============================================================================

print(f"\n{'='*70}")
print("PART 3: Extracting Binary Sequences")
print("="*70)

def extract_binary_from_interference(counts):
    """Convert interference pattern to binary sequence"""
    threshold = np.median(counts)
    binary = (counts > threshold).astype(int)
    return binary

binary_sequences = {}

for sheet, df in datasets.items():
    counts = df.iloc[:, 1].values
    binary = extract_binary_from_interference(counts)
    binary_sequences[sheet] = binary
    
    ones = np.sum(binary)
    balance = ones / len(binary)
    
    print(f"\n{sheet}:")
    print(f"  Binary length: {len(binary)}")
    print(f"  Balance (ones): {balance:.4f}")

# ============================================================================
# PART 4: UBP GEOMETRIC WEIGHT SCANNING
# ============================================================================

print(f"\n{'='*70}")
print("PART 4: UBP Geometric Weight Scanning")
print("="*70)

def calculate_weighted_autocorrelation(seq, weight):
    """
    Calculate autocorrelation with geometric weighting.
    
    This tests how spatial structure changes with different geometric weights.
    """
    n = len(seq)
    weighted_corr = 0.0
    total_weight = 0.0
    
    for lag in range(1, min(n//2, 50)):  # Limit lag to avoid edge effects
        for i in range(n - lag):
            # Geometric weight based on lag distance
            w = 1.0 / (lag ** weight)
            
            # Correlation contribution
            if seq[i] == seq[i + lag]:
                weighted_corr += w
            else:
                weighted_corr -= w
            
            total_weight += w
    
    if total_weight == 0:
        return 0.0
    
    return weighted_corr / total_weight

# Scan weights for each dataset
weights = np.linspace(0.5, 3.0, 26)
weight_scan_results = {}

for sheet, binary in binary_sequences.items():
    weighted_corrs = []
    
    for w in weights:
        wc = calculate_weighted_autocorrelation(binary, w)
        weighted_corrs.append(wc)
    
    # Find optimal weight
    optimal_idx = np.argmax(np.abs(weighted_corrs))
    optimal_weight = weights[optimal_idx]
    optimal_corr = weighted_corrs[optimal_idx]
    
    weight_scan_results[sheet] = {
        'weights': weights.tolist(),
        'correlations': weighted_corrs,
        'optimal_weight': optimal_weight,
        'optimal_correlation': optimal_corr
    }
    
    print(f"\n{sheet}:")
    print(f"  Optimal weight: w = {optimal_weight:.4f}")
    print(f"  Optimal correlation: {optimal_corr:.6f}")

# Calculate average optimal weight
avg_optimal_weight = np.mean([r['optimal_weight'] for r in weight_scan_results.values()])

print(f"\n{'='*70}")
print(f"AVERAGE OPTIMAL WEIGHT: w = {avg_optimal_weight:.4f}")
print(f"{'='*70}")

# Compare with predictions
print(f"\nComparison with UBP predictions:")
print(f"  w_observed = {avg_optimal_weight:.4f}")
print(f"  w_predicted (ILRV) = 1.5303 (Information Layer)")
print(f"  w_predicted (Magnetic) = 2.5 (Unactivated Layer)")
print(f"  Difference from ILRV: {abs(avg_optimal_weight - 1.5303):.4f}")
print(f"  Difference from Magnetic: {abs(avg_optimal_weight - 2.5):.4f}")

# Determine which layer signature is closer
if abs(avg_optimal_weight - 1.5303) < abs(avg_optimal_weight - 2.5):
    print(f"\n  ✓ CLOSER TO INFORMATION LAYER SIGNATURE")
    print(f"    Supports hypothesis: Light exhibits Information Layer resonance")
else:
    print(f"\n  ✓ CLOSER TO UNACTIVATED LAYER SIGNATURE")
    print(f"    Suggests: Interference involves stored coherence states")

# ============================================================================
# PART 5: LAYER FLUCTUATION ANALYSIS
# ============================================================================

print(f"\n{'='*70}")
print("PART 5: Layer Fluctuation Analysis")
print("="*70)

# Compare biaxial (XSARP) vs uniaxial states
# According to UBP theory, biaxial should show stronger layer coupling

if 'X' in analysis_results and '45°' in analysis_results:
    biaxial_vis = analysis_results['X']['visibility']
    uniaxial_vis = (analysis_results['45°']['visibility'] + 
                    analysis_results['135°']['visibility']) / 2
    
    print(f"\nInterference Visibility:")
    print(f"  Biaxial (XSARP): {biaxial_vis:.4f}")
    print(f"  Uniaxial (avg): {uniaxial_vis:.4f}")
    print(f"  Ratio: {biaxial_vis / uniaxial_vis:.4f}")
    
    if biaxial_vis > uniaxial_vis:
        print(f"\n  ✓ Biaxial shows STRONGER interference")
        print(f"    Consistent with enhanced Information ↔ Activation coupling")
    
    # Compare geometric weights
    biaxial_w = weight_scan_results['X']['optimal_weight']
    uniaxial_w = (weight_scan_results['45°']['optimal_weight'] + 
                  weight_scan_results['135°']['optimal_weight']) / 2
    
    print(f"\nGeometric Weights:")
    print(f"  Biaxial (XSARP): w = {biaxial_w:.4f}")
    print(f"  Uniaxial (avg): w = {uniaxial_w:.4f}")
    print(f"  Difference: {abs(biaxial_w - uniaxial_w):.4f}")

# ============================================================================
# PART 6: VISUALIZATION
# ============================================================================

print(f"\n{'='*70}")
print("PART 6: Generating Visualizations")
print("="*70)

fig, axes = plt.subplots(2, 3, figsize=(18, 10))

# Plot interference patterns
for idx, (sheet, df) in enumerate(datasets.items()):
    ax = axes[0, idx]
    angles = df.iloc[:, 0].values
    counts = df.iloc[:, 1].values
    
    ax.plot(angles, counts, 'b-', linewidth=2)
    
    # Mark peaks and troughs
    results = analysis_results[sheet]
    if len(results['peak_positions']) > 0:
        peak_angles = np.array(results['peak_positions'])
        peak_idx = [np.argmin(np.abs(angles - pa)) for pa in peak_angles]
        ax.plot(angles[peak_idx], counts[peak_idx], 'ro', markersize=8, label='Peaks')
    
    if len(results['trough_positions']) > 0:
        trough_angles = np.array(results['trough_positions'])
        trough_idx = [np.argmin(np.abs(angles - ta)) for ta in trough_angles]
        ax.plot(angles[trough_idx], counts[trough_idx], 'go', markersize=8, label='Troughs')
    
    ax.set_xlabel('Scattering Angle (degrees)', fontsize=11)
    ax.set_ylabel('Counts', fontsize=11)
    ax.set_title(f'{sheet}\nVisibility: {results["visibility"]:.3f}', 
                 fontsize=12, fontweight='bold')
    ax.grid(True, alpha=0.3)
    ax.legend()

# Plot weight scans
for idx, (sheet, results) in enumerate(weight_scan_results.items()):
    ax = axes[1, idx]
    weights_arr = np.array(results['weights'])
    corrs = results['correlations']
    
    ax.plot(weights_arr, corrs, 'b-', linewidth=2, label='Weighted correlation')
    ax.axvline(results['optimal_weight'], color='r', linestyle='--', 
               label=f'Optimal w = {results["optimal_weight"]:.4f}')
    ax.axvline(1.5303, color='g', linestyle='--', label='ILRV = 1.5303')
    ax.axvline(2.5, color='orange', linestyle='--', label='Magnetic = 2.5')
    
    ax.set_xlabel('Geometric Weight (w)', fontsize=11)
    ax.set_ylabel('Weighted Autocorrelation', fontsize=11)
    ax.set_title(f'{sheet} Weight Scan', fontsize=12, fontweight='bold')
    ax.legend(fontsize=9)
    ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('/home/ubuntu/double_slit_ubp_analysis.png', dpi=300, bbox_inches='tight')
print(f"\n✓ Visualization saved: double_slit_ubp_analysis.png")

# ============================================================================
# PART 7: SAVE RESULTS
# ============================================================================

print(f"\n{'='*70}")
print("PART 7: Saving Results")
print("="*70)

results_summary = {
    'experiment': 'Double-Slit Interference (Molecular Scattering)',
    'data_source': 'Zhou et al., 2021 - Dryad Repository',
    'datasets': list(datasets.keys()),
    'interference_analysis': analysis_results,
    'ubp_weight_analysis': {
        'average_optimal_weight': float(avg_optimal_weight),
        'predicted_ILRV': 1.5303,
        'predicted_magnetic': 2.5,
        'difference_from_ILRV': float(abs(avg_optimal_weight - 1.5303)),
        'difference_from_magnetic': float(abs(avg_optimal_weight - 2.5)),
        'closest_prediction': 'ILRV' if abs(avg_optimal_weight - 1.5303) < abs(avg_optimal_weight - 2.5) else 'Magnetic',
        'individual_weights': {sheet: float(r['optimal_weight']) for sheet, r in weight_scan_results.items()}
    },
    'layer_fluctuation': {
        'biaxial_visibility': float(analysis_results['X']['visibility']) if 'X' in analysis_results else None,
        'uniaxial_avg_visibility': float((analysis_results['45°']['visibility'] + analysis_results['135°']['visibility']) / 2) if '45°' in analysis_results else None
    },
    'interpretation': 'Double-slit interference analyzed with UBP framework to test light layer-fluctuation hypothesis'
}

with open('/home/ubuntu/double_slit_ubp_results.json', 'w') as f:
    json.dump(results_summary, f, indent=2)

print(f"\n✓ Results saved: double_slit_ubp_results.json")

print(f"\n{'='*70}")
print("SUMMARY")
print("="*70)

print(f"\n1. INTERFERENCE PATTERNS:")
for sheet, results in analysis_results.items():
    print(f"   {sheet}: {results['num_peaks']} peaks, visibility = {results['visibility']:.4f}")

print(f"\n2. UBP GEOMETRIC WEIGHTS:")
for sheet, results in weight_scan_results.items():
    print(f"   {sheet}: w = {results['optimal_weight']:.4f}")
print(f"   Average: w = {avg_optimal_weight:.4f}")

print(f"\n3. COMPARISON WITH PREDICTIONS:")
print(f"   Observed: w = {avg_optimal_weight:.4f}")
print(f"   ILRV (Information): w = 1.5303")
print(f"   Magnetic (Unactivated): w = 2.5")

error_ilrv = abs(avg_optimal_weight - 1.5303) / 1.5303 * 100
error_mag = abs(avg_optimal_weight - 2.5) / 2.5 * 100

print(f"   Error from ILRV: {error_ilrv:.2f}%")
print(f"   Error from Magnetic: {error_mag:.2f}%")

if error_ilrv < error_mag:
    print(f"\n   ✓ BEST MATCH: Information Layer (ILRV)")
    print(f"     Supports: Light as Information ↔ Activation resonance")
else:
    print(f"\n   ✓ BEST MATCH: Unactivated Layer")
    print(f"     Suggests: Interference involves coherence storage")

print(f"\n{'='*70}")
print("ANALYSIS COMPLETE")
print("="*70)

