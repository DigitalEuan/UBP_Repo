#!/usr/bin/env python3.11
"""
Real Validation: Advanced HexDictionary vs Hamming Distance
Using actual nutrient data from the Nutrition study

This tests whether the Advanced HexDictionary can detect synergies and
antagonisms better than simple Hamming distance.
"""

import sys
import json
import math
import numpy as np
import matplotlib.pyplot as plt

sys.path.insert(0, '/home/ubuntu/UBP_Repo/ubp_3.5')
sys.path.insert(0, '/home/ubuntu/dissident_horizon_study')

from coherence_substrate import CoherenceState
from hex_dictionary_advanced import AdvancedHexDictionaryAnalyzer

# Load real nutrient data
with open('real_nutrient_data.json', 'r') as f:
    nutrients = json.load(f)

print("=" * 80)
print("REAL VALIDATION: Advanced HexDictionary on Nutrition Study Data")
print("=" * 80)
print(f"\nLoaded {len(nutrients)} real nutrients")
print()

# Create analyzer
analyzer = AdvancedHexDictionaryAnalyzer()

# Test on known synergies and antagonisms
known_synergies = [
    ('vitamin_c', 'iron_nonheme'),  # Vitamin C enhances iron absorption
    ('vitamin_d', 'calcium'),  # Vitamin D enhances calcium absorption
    ('vitamin_b2', 'iron_heme'),  # B2 enhances iron
    ('vitamin_k2', 'calcium'),  # K2 works with calcium
    ('copper', 'iron_heme'),  # Copper aids iron metabolism
]

known_antagonisms = [
    ('calcium', 'iron_heme'),  # Calcium blocks iron
    ('calcium', 'zinc'),  # Calcium blocks zinc
    ('iron_heme', 'zinc'),  # Iron and zinc compete
    ('calcium', 'magnesium'),  # Compete for absorption
]

# Generate hashes for all nutrients
print("Generating hashes for all nutrients...")
nutrient_hashes = {}
nutrient_states = {}

for name, data in nutrients.items():
    # Create hash from coherence frequency and bioavailability
    freq = data['coherence_frequency']
    bio = data['bioavailability']
    
    # Simple hash: convert to hex string
    hash_val = f"{int(freq):016x}{int(bio*1000):04x}"
    nutrient_hashes[name] = hash_val
    
    # Create coherence state
    log_error = math.log(1 - data['coherence']['nrci'])
    state = CoherenceState(freq, log_error, 0)
    nutrient_states[name] = [state]

print(f"✓ Generated {len(nutrient_hashes)} hashes")
print()

# Test synergies
print("=" * 80)
print("TESTING KNOWN SYNERGIES")
print("=" * 80)

synergy_results = []

for n1, n2 in known_synergies:
    if n1 not in nutrients or n2 not in nutrients:
        print(f"⚠ Skipping {n1}-{n2}: not in dataset")
        continue
    
    # Create data arrays from frequency
    data1 = np.array([nutrients[n1]['coherence_frequency']] * 10)
    data2 = np.array([nutrients[n2]['coherence_frequency']] * 10)
    
    # Hamming distance
    hash1 = nutrient_hashes[n1]
    hash2 = nutrient_hashes[n2]
    hamming_dist = sum(c1 != c2 for c1, c2 in zip(hash1, hash2)) / len(hash1)
    hamming_sim = 1.0 - hamming_dist
    
    # Advanced analysis
    analysis = analyzer.analyze_similarity(
        hash1, hash2,
        data1, data2,
        nutrient_states[n1], nutrient_states[n2]
    )
    
    synergy_results.append({
        'pair': f"{n1}-{n2}",
        'type': 'synergy',
        'hamming_similarity': hamming_sim,
        'advanced_similarity': analysis.overall_similarity,
        'freq_ratio': nutrients[n1]['coherence_frequency'] / nutrients[n2]['coherence_frequency']
    })
    
    print(f"\n{n1} + {n2}:")
    print(f"  Hamming similarity: {hamming_sim:.3f}")
    print(f"  Advanced similarity: {analysis.overall_similarity:.3f}")
    print(f"  Frequency ratio: {synergy_results[-1]['freq_ratio']:.2f}")

# Test antagonisms
print("\n" + "=" * 80)
print("TESTING KNOWN ANTAGONISMS")
print("=" * 80)

antagonism_results = []

for n1, n2 in known_antagonisms:
    if n1 not in nutrients or n2 not in nutrients:
        print(f"⚠ Skipping {n1}-{n2}: not in dataset")
        continue
    
    # Create data arrays
    data1 = np.array([nutrients[n1]['coherence_frequency']] * 10)
    data2 = np.array([nutrients[n2]['coherence_frequency']] * 10)
    
    # Hamming distance
    hash1 = nutrient_hashes[n1]
    hash2 = nutrient_hashes[n2]
    hamming_dist = sum(c1 != c2 for c1, c2 in zip(hash1, hash2)) / len(hash1)
    hamming_sim = 1.0 - hamming_dist
    
    # Advanced analysis
    analysis = analyzer.analyze_similarity(
        hash1, hash2,
        data1, data2,
        nutrient_states[n1], nutrient_states[n2]
    )
    
    antagonism_results.append({
        'pair': f"{n1}-{n2}",
        'type': 'antagonism',
        'hamming_similarity': hamming_sim,
        'advanced_similarity': analysis.overall_similarity,
        'freq_ratio': nutrients[n1]['coherence_frequency'] / nutrients[n2]['coherence_frequency']
    })
    
    print(f"\n{n1} vs {n2}:")
    print(f"  Hamming similarity: {hamming_sim:.3f}")
    print(f"  Advanced similarity: {analysis.overall_similarity:.3f}")
    print(f"  Frequency ratio: {antagonism_results[-1]['freq_ratio']:.2f}")

# Calculate discriminative power
print("\n" + "=" * 80)
print("DISCRIMINATIVE POWER ANALYSIS")
print("=" * 80)

syn_hamming = [r['hamming_similarity'] for r in synergy_results]
syn_advanced = [r['advanced_similarity'] for r in synergy_results]

ant_hamming = [r['hamming_similarity'] for r in antagonism_results]
ant_advanced = [r['advanced_similarity'] for r in antagonism_results]

# Separation = difference between synergy and antagonism means
hamming_separation = np.mean(syn_hamming) - np.mean(ant_hamming)
advanced_separation = np.mean(syn_advanced) - np.mean(ant_advanced)

discriminative_power = advanced_separation / hamming_separation if hamming_separation != 0 else float('inf')

print(f"\nSynergies (should have HIGH similarity):")
print(f"  Hamming: {np.mean(syn_hamming):.3f} ± {np.std(syn_hamming):.3f}")
print(f"  Advanced: {np.mean(syn_advanced):.3f} ± {np.std(syn_advanced):.3f}")

print(f"\nAntagonisms (should have LOW similarity):")
print(f"  Hamming: {np.mean(ant_hamming):.3f} ± {np.std(ant_hamming):.3f}")
print(f"  Advanced: {np.mean(ant_advanced):.3f} ± {np.std(ant_advanced):.3f}")

print(f"\nSeparation:")
print(f"  Hamming: {hamming_separation:.3f}")
print(f"  Advanced: {advanced_separation:.3f}")
print(f"  Discriminative Power: {discriminative_power:.1f}× improvement")

# Save results
results = {
    'synergies': synergy_results,
    'antagonisms': antagonism_results,
    'summary': {
        'synergy_hamming_mean': float(np.mean(syn_hamming)),
        'synergy_advanced_mean': float(np.mean(syn_advanced)),
        'antagonism_hamming_mean': float(np.mean(ant_hamming)),
        'antagonism_advanced_mean': float(np.mean(ant_advanced)),
        'hamming_separation': float(hamming_separation),
        'advanced_separation': float(advanced_separation),
        'discriminative_power': float(discriminative_power)
    }
}

with open('hexdictionary_real_validation.json', 'w') as f:
    json.dump(results, f, indent=2)

print(f"\n✓ Results saved to hexdictionary_real_validation.json")

# Generate comparison plot
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

# Plot 1: Hamming vs Advanced for Synergies
ax1.scatter(syn_hamming, syn_advanced, c='green', s=100, alpha=0.6, label='Synergies')
ax1.scatter(ant_hamming, ant_advanced, c='red', s=100, alpha=0.6, label='Antagonisms')
ax1.plot([0, 1], [0, 1], 'k--', alpha=0.3, label='y=x')
ax1.set_xlabel('Hamming Similarity', fontsize=12)
ax1.set_ylabel('Advanced Similarity', fontsize=12)
ax1.set_title('Hamming vs Advanced HexDictionary\n(Real Nutrient Data)', fontsize=14, fontweight='bold')
ax1.legend()
ax1.grid(True, alpha=0.3)

# Plot 2: Separation comparison
methods = ['Hamming\nDistance', 'Advanced\nHexDictionary']
separations = [hamming_separation, advanced_separation]
colors = ['#ff6b6b', '#4ecdc4']

bars = ax2.bar(methods, separations, color=colors, alpha=0.7, edgecolor='black', linewidth=2)
ax2.set_ylabel('Separation (Synergy - Antagonism)', fontsize=12)
ax2.set_title(f'Discriminative Power\n{discriminative_power:.1f}× Improvement', fontsize=14, fontweight='bold')
ax2.grid(True, alpha=0.3, axis='y')

# Add value labels on bars
for bar, val in zip(bars, separations):
    height = bar.get_height()
    ax2.text(bar.get_x() + bar.get_width()/2., height,
             f'{val:.3f}',
             ha='center', va='bottom', fontsize=12, fontweight='bold')

plt.tight_layout()
plt.savefig('hexdictionary_real_validation.png', dpi=300, bbox_inches='tight')
print(f"✓ Plot saved to hexdictionary_real_validation.png")

print("\n" + "=" * 80)
print("VALIDATION COMPLETE")
print("=" * 80)
