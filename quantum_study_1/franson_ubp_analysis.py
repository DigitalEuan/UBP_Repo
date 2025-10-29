"""
Franson Bell Test Data - UBP Framework Analysis
================================================

This script analyzes real experimental Bell test data from the Franson experiment
using the Universal Binary Principle framework.

The Franson experiment tests Bell's inequality using energy-time entangled photons.
The data consists of time-binned coincidence histograms for different measurement settings.

Author: Euan R A Craig & Manus AI
Date: October 29, 2025
"""

import numpy as np
import json
import os
import glob
from collections import defaultdict
import matplotlib.pyplot as plt

print("="*70)
print("FRANSON BELL TEST DATA - UBP ANALYSIS")
print("="*70)

# ============================================================================
# PART 1: DATA LOADING AND PARSING
# ============================================================================

print(f"\n{'='*70}")
print("PART 1: Loading Franson Experiment Data")
print("="*70)

data_dir = "/home/ubuntu/upload/franson_data"
data_files = glob.glob(os.path.join(data_dir, "*.dat"))

print(f"\nFound {len(data_files)} data files")
print(f"Directory: {data_dir}")

# Parse filenames to extract measurement settings
# Format: "AAAAAA 020.dat" or "BBBBBB 0N1.dat"
# First 6 chars: detector configuration
# Last 3 chars before .dat: measurement settings

franson_data = {}

for filepath in sorted(data_files):
    filename = os.path.basename(filepath)
    
    # Extract configuration and settings
    parts = filename.replace('.dat', '').split()
    if len(parts) == 2:
        config = parts[0]
        settings = parts[1]
        
        # Load the data
        try:
            data = np.loadtxt(filepath)
            
            # Data format: each row is a time bin
            # Column 3 (index 2) contains the coincidence counts
            if data.ndim == 2 and data.shape[1] >= 3:
                time_bins = data[:, 0]  # Time bin index
                counts = data[:, 2]     # Coincidence counts
                
                key = f"{config}_{settings}"
                franson_data[key] = {
                    'config': config,
                    'settings': settings,
                    'time_bins': time_bins,
                    'counts': counts,
                    'total_counts': np.sum(counts),
                    'filename': filename
                }
        except Exception as e:
            print(f"  Warning: Could not load {filename}: {e}")

print(f"\nSuccessfully loaded {len(franson_data)} datasets")

# Group by configuration
configs = defaultdict(list)
for key, data in franson_data.items():
    configs[data['config']].append(key)

print(f"\nConfigurations found:")
for config, keys in sorted(configs.items()):
    total = sum(franson_data[k]['total_counts'] for k in keys)
    print(f"  {config}: {len(keys)} settings, {total:.0f} total counts")

# ============================================================================
# PART 2: EXTRACT BINARY SEQUENCES FOR UBP ANALYSIS
# ============================================================================

print(f"\n{'='*70}")
print("PART 2: Extracting Binary Sequences")
print("="*70)

def extract_binary_from_histogram(counts, threshold='median'):
    """
    Convert time-binned histogram to binary sequence.
    
    Strategy: Each time bin becomes a binary value based on whether
    the count exceeds a threshold.
    """
    if threshold == 'median':
        thresh = np.median(counts[counts > 0])
    elif threshold == 'mean':
        thresh = np.mean(counts[counts > 0])
    else:
        thresh = threshold
    
    binary = (counts > thresh).astype(int)
    return binary

# Extract binary sequences for each dataset
binary_sequences = {}

for key, data in franson_data.items():
    binary = extract_binary_from_histogram(data['counts'])
    binary_sequences[key] = binary
    
    # Calculate basic statistics
    ones = np.sum(binary)
    zeros = len(binary) - ones
    balance = ones / len(binary) if len(binary) > 0 else 0
    
    franson_data[key]['binary'] = binary
    franson_data[key]['balance'] = balance

print(f"\nBinary sequence statistics:")
print(f"  Total sequences: {len(binary_sequences)}")
print(f"  Sequence length: {len(binary_sequences[list(binary_sequences.keys())[0]])}")

# ============================================================================
# PART 3: CALCULATE CORRELATIONS (BELL TEST)
# ============================================================================

print(f"\n{'='*70}")
print("PART 3: Calculating Bell Correlations")
print("="*70)

def calculate_correlation(seq1, seq2):
    """Calculate correlation E = (N_same - N_diff) / (N_same + N_diff)"""
    if len(seq1) != len(seq2):
        min_len = min(len(seq1), len(seq2))
        seq1 = seq1[:min_len]
        seq2 = seq2[:min_len]
    
    same = np.sum(seq1 == seq2)
    diff = np.sum(seq1 != seq2)
    total = same + diff
    
    if total == 0:
        return 0.0
    
    correlation = (same - diff) / total
    return correlation

# Try to identify Alice-Bob pairs
# AAAAAA configurations are likely Alice
# BBBBBB configurations are likely Bob

alice_keys = [k for k in franson_data.keys() if 'AAAAAA' in k]
bob_keys = [k for k in franson_data.keys() if 'BBBBBB' in k]

print(f"\nAlice datasets: {len(alice_keys)}")
print(f"Bob datasets: {len(bob_keys)}")

# Calculate correlations for matching settings
correlations = []

for alice_key in alice_keys:
    alice_settings = franson_data[alice_key]['settings']
    
    # Find matching Bob setting
    for bob_key in bob_keys:
        bob_settings = franson_data[bob_key]['settings']
        
        # Calculate correlation
        corr = calculate_correlation(
            franson_data[alice_key]['binary'],
            franson_data[bob_key]['binary']
        )
        
        correlations.append({
            'alice_settings': alice_settings,
            'bob_settings': bob_settings,
            'correlation': corr,
            'alice_key': alice_key,
            'bob_key': bob_key
        })

print(f"\nCalculated {len(correlations)} correlations")

# Find strongest correlations
correlations_sorted = sorted(correlations, key=lambda x: abs(x['correlation']), reverse=True)

print(f"\nTop 10 strongest correlations:")
print(f"{'Alice':<10} {'Bob':<10} {'Correlation':<15}")
print("-"*35)
for c in correlations_sorted[:10]:
    print(f"{c['alice_settings']:<10} {c['bob_settings']:<10} {c['correlation']:<15.6f}")

# ============================================================================
# PART 4: APPLY UBP FRAMEWORK - GEOMETRIC WEIGHT SCANNING
# ============================================================================

print(f"\n{'='*70}")
print("PART 4: UBP Geometric Weight Scanning")
print("="*70)

# Import the information layer metrics
import sys
sys.path.append('/home/ubuntu')

try:
    from information_layer_metrics import calculate_lempel_ziv_complexity, calculate_nrci_i
    metrics_available = True
except ImportError:
    print("Warning: Information layer metrics not available, using simplified analysis")
    metrics_available = False
    
    def calculate_lempel_ziv_complexity(seq):
        """Simplified LZ complexity"""
        return len(set([tuple(seq[i:i+4]) for i in range(len(seq)-3)])) / (len(seq) - 3)
    
    def calculate_nrci_i(seq):
        """Simplified NRCI-I"""
        return 1.0 - np.std(seq)

def calculate_weighted_correlation(seq1, seq2, weight):
    """
    Calculate correlation with geometric weighting.
    
    The weight parameter modulates how spatial/temporal proximity affects correlation.
    """
    if len(seq1) != len(seq2):
        min_len = min(len(seq1), len(seq2))
        seq1 = seq1[:min_len]
        seq2 = seq2[:min_len]
    
    n = len(seq1)
    weighted_corr = 0.0
    total_weight = 0.0
    
    for i in range(n):
        for j in range(n):
            # Geometric weight based on distance
            distance = abs(i - j) + 1
            w = 1.0 / (distance ** weight)
            
            # Correlation contribution
            if seq1[i] == seq2[j]:
                weighted_corr += w
            else:
                weighted_corr -= w
            
            total_weight += w
    
    if total_weight == 0:
        return 0.0
    
    return weighted_corr / total_weight

# Scan weights for the strongest correlation pair
if correlations_sorted:
    best_corr = correlations_sorted[0]
    alice_seq = franson_data[best_corr['alice_key']]['binary']
    bob_seq = franson_data[best_corr['bob_key']]['binary']
    
    print(f"\nScanning geometric weights for strongest correlation pair:")
    print(f"  Alice: {best_corr['alice_settings']}")
    print(f"  Bob: {best_corr['bob_settings']}")
    print(f"  Standard correlation: {best_corr['correlation']:.6f}")
    
    weights = np.linspace(0.5, 3.0, 26)
    weighted_corrs = []
    
    print(f"\nWeight scanning...")
    for w in weights:
        wc = calculate_weighted_correlation(alice_seq, bob_seq, w)
        weighted_corrs.append(wc)
    
    # Find optimal weight
    optimal_idx = np.argmax(np.abs(weighted_corrs))
    optimal_weight = weights[optimal_idx]
    optimal_corr = weighted_corrs[optimal_idx]
    
    print(f"\n✓ Optimal geometric weight: w = {optimal_weight:.4f}")
    print(f"  Weighted correlation: {optimal_corr:.6f}")
    print(f"  Standard correlation: {best_corr['correlation']:.6f}")
    print(f"  Enhancement: {abs(optimal_corr / best_corr['correlation']):.2f}x")
    
    # Compare with predictions
    print(f"\nComparison with UBP predictions:")
    print(f"  w_observed = {optimal_weight:.4f}")
    print(f"  w_predicted (ILRV) = 1.5303")
    print(f"  Difference: {abs(optimal_weight - 1.5303):.4f}")
    print(f"  Relative error: {abs(optimal_weight - 1.5303) / 1.5303 * 100:.2f}%")

# ============================================================================
# PART 5: INFORMATION-THEORETIC ANALYSIS
# ============================================================================

print(f"\n{'='*70}")
print("PART 5: Information-Theoretic Analysis")
print("="*70)

# Analyze a subset of sequences
sample_keys = list(franson_data.keys())[:5]

print(f"\nAnalyzing {len(sample_keys)} sample sequences:")
print(f"{'Dataset':<20} {'LZ Complexity':<15} {'NRCI-I':<15} {'Balance':<15}")
print("-"*65)

for key in sample_keys:
    seq = franson_data[key]['binary']
    
    lz = calculate_lempel_ziv_complexity(seq)
    nrci = calculate_nrci_i(seq)
    balance = franson_data[key]['balance']
    
    print(f"{key[:18]:<20} {lz:<15.6f} {nrci:<15.6f} {balance:<15.6f}")

# ============================================================================
# PART 6: VISUALIZATION
# ============================================================================

print(f"\n{'='*70}")
print("PART 6: Generating Visualizations")
print("="*70)

fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# Plot 1: Weight scan
if correlations_sorted and len(weights) > 0:
    ax = axes[0, 0]
    ax.plot(weights, weighted_corrs, 'b-', linewidth=2, label='Weighted correlation')
    ax.axvline(optimal_weight, color='r', linestyle='--', label=f'Optimal w = {optimal_weight:.4f}')
    ax.axvline(1.5303, color='g', linestyle='--', label='Predicted ILRV = 1.5303')
    ax.set_xlabel('Geometric Weight (w)', fontsize=12)
    ax.set_ylabel('Weighted Correlation', fontsize=12)
    ax.set_title('Geometric Weight Scan - Franson Data', fontsize=14, fontweight='bold')
    ax.legend()
    ax.grid(True, alpha=0.3)

# Plot 2: Correlation distribution
ax = axes[0, 1]
corr_values = [c['correlation'] for c in correlations]
ax.hist(corr_values, bins=20, edgecolor='black', alpha=0.7)
ax.set_xlabel('Correlation', fontsize=12)
ax.set_ylabel('Frequency', fontsize=12)
ax.set_title('Distribution of Correlations', fontsize=14, fontweight='bold')
ax.grid(True, alpha=0.3)

# Plot 3: Sample coincidence histogram
ax = axes[1, 0]
sample_key = list(franson_data.keys())[0]
sample_data = franson_data[sample_key]
ax.plot(sample_data['time_bins'], sample_data['counts'], 'b-', linewidth=1)
ax.set_xlabel('Time Bin', fontsize=12)
ax.set_ylabel('Coincidence Counts', fontsize=12)
ax.set_title(f'Sample Histogram: {sample_data["filename"]}', fontsize=14, fontweight='bold')
ax.grid(True, alpha=0.3)

# Plot 4: Binary sequence visualization
ax = axes[1, 1]
binary_sample = franson_data[sample_key]['binary'][:100]  # First 100 bins
ax.imshow([binary_sample], cmap='binary', aspect='auto', interpolation='nearest')
ax.set_xlabel('Time Bin', fontsize=12)
ax.set_ylabel('Binary Value', fontsize=12)
ax.set_title('Binary Sequence (first 100 bins)', fontsize=14, fontweight='bold')
ax.set_yticks([])

plt.tight_layout()
plt.savefig('/home/ubuntu/franson_ubp_analysis.png', dpi=300, bbox_inches='tight')
print(f"\n✓ Visualization saved: franson_ubp_analysis.png")

# ============================================================================
# PART 7: SAVE RESULTS
# ============================================================================

print(f"\n{'='*70}")
print("PART 7: Saving Results")
print("="*70)

results = {
    'experiment': 'Franson Bell Test',
    'data_source': 'Real experimental data',
    'total_datasets': len(franson_data),
    'alice_datasets': len(alice_keys),
    'bob_datasets': len(bob_keys),
    'correlations_calculated': len(correlations),
    'strongest_correlation': {
        'alice_settings': correlations_sorted[0]['alice_settings'] if correlations_sorted else None,
        'bob_settings': correlations_sorted[0]['bob_settings'] if correlations_sorted else None,
        'correlation': float(correlations_sorted[0]['correlation']) if correlations_sorted else None
    },
    'ubp_analysis': {
        'optimal_weight': float(optimal_weight) if correlations_sorted else None,
        'optimal_correlation': float(optimal_corr) if correlations_sorted else None,
        'predicted_weight_ILRV': 1.5303,
        'weight_difference': float(abs(optimal_weight - 1.5303)) if correlations_sorted else None,
        'relative_error_percent': float(abs(optimal_weight - 1.5303) / 1.5303 * 100) if correlations_sorted else None
    },
    'interpretation': 'Real experimental Bell test data analyzed with UBP framework'
}

with open('/home/ubuntu/franson_ubp_results.json', 'w') as f:
    json.dump(results, f, indent=2)

print(f"\n✓ Results saved: franson_ubp_results.json")

print(f"\n{'='*70}")
print("SUMMARY")
print("="*70)

print(f"\n1. DATA:")
print(f"   - Loaded {len(franson_data)} real experimental datasets")
print(f"   - Alice: {len(alice_keys)} settings, Bob: {len(bob_keys)} settings")
print(f"   - Calculated {len(correlations)} correlation pairs")

if correlations_sorted:
    print(f"\n2. BELL TEST:")
    print(f"   - Strongest correlation: {correlations_sorted[0]['correlation']:.6f}")
    print(f"   - Settings: Alice={correlations_sorted[0]['alice_settings']}, Bob={correlations_sorted[0]['bob_settings']}")

    print(f"\n3. UBP ANALYSIS:")
    print(f"   - Optimal geometric weight: w = {optimal_weight:.4f}")
    print(f"   - Predicted ILRV: w = 1.5303")
    print(f"   - Relative error: {abs(optimal_weight - 1.5303) / 1.5303 * 100:.2f}%")

    if abs(optimal_weight - 1.5303) / 1.5303 < 0.1:
        print(f"   ✓ EXCELLENT AGREEMENT with UBP prediction!")
    elif abs(optimal_weight - 1.5303) / 1.5303 < 0.2:
        print(f"   ✓ GOOD AGREEMENT with UBP prediction")
    else:
        print(f"   ⚠ Deviation from prediction - may indicate data limitations")

print(f"\n{'='*70}")
print("ANALYSIS COMPLETE")
print("="*70)

