#!/usr/bin/env python3.11
"""
Comprehensive Real Data Analysis: UBP Time & Dissident Horizon Study
Using actual 84-nutrient dataset from the Nutrition study

This script performs REAL validation of:
1. Frequency Coherence Hypothesis
2. Dissident state detection in biological systems
3. Advanced pattern analysis methods

All data is REAL - no synthetic generation.
"""

import sys
import json
import math
import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict
from dataclasses import dataclass
from typing import List, Dict, Tuple

sys.path.insert(0, '/home/ubuntu/UBP_Repo/nutrition')
sys.path.insert(0, '/home/ubuntu/UBP_Repo/ubp_3.5')

from expanded_nutrient_database import ExpandedNutrientDatabase
from coherence_substrate import CoherenceState

print("=" * 80)
print("COMPREHENSIVE REAL DATA ANALYSIS")
print("UBP Time & Dissident Horizon Study")
print("=" * 80)
print()

# Load real nutrient data
print("Loading real 84-nutrient dataset...")
nutrients = ExpandedNutrientDatabase.get_all_nutrients()
print(f"✓ Loaded {len(nutrients)} real nutrients")
print()

# ==============================================================================
# PART 1: FREQUENCY COHERENCE HYPOTHESIS VALIDATION
# ==============================================================================

print("=" * 80)
print("PART 1: FREQUENCY COHERENCE HYPOTHESIS")
print("Testing if nutrient interactions correlate with frequency ratios")
print("=" * 80)
print()

# Extract all documented synergies and antagonisms from the dataset
synergies = []
antagonisms = []

for name, nutrient in nutrients.items():
    for synergist in nutrient.synergists:
        if synergist in nutrients:
            pair = tuple(sorted([name, synergist]))
            if pair not in [tuple(sorted([s[0], s[1]])) for s in synergies]:
                synergies.append((name, synergist))
    
    for antagonist in nutrient.antagonists:
        if antagonist in nutrients:
            pair = tuple(sorted([name, antagonist]))
            if pair not in [tuple(sorted([a[0], a[1]])) for a in antagonisms]:
                antagonisms.append((name, antagonist))

print(f"Found {len(synergies)} documented synergies")
print(f"Found {len(antagonisms)} documented antagonisms")
print()

# Calculate frequency ratios for all interactions
synergy_ratios = []
antagonism_ratios = []

print("Synergies (frequency ratios):")
for n1, n2 in synergies[:10]:  # Show first 10
    freq1 = nutrients[n1].coherence_frequency
    freq2 = nutrients[n2].coherence_frequency
    ratio = max(freq1, freq2) / min(freq1, freq2)
    synergy_ratios.append(ratio)
    print(f"  {n1:20s} + {n2:20s}: {ratio:.2f}")

print()
print("Antagonisms (frequency ratios):")
for n1, n2 in antagonisms[:10]:  # Show first 10
    freq1 = nutrients[n1].coherence_frequency
    freq2 = nutrients[n2].coherence_frequency
    ratio = max(freq1, freq2) / min(freq1, freq2)
    antagonism_ratios.append(ratio)
    print(f"  {n1:20s} vs {n2:20s}: {ratio:.2f}")

# Calculate all ratios
for n1, n2 in synergies[10:]:
    freq1 = nutrients[n1].coherence_frequency
    freq2 = nutrients[n2].coherence_frequency
    ratio = max(freq1, freq2) / min(freq1, freq2)
    synergy_ratios.append(ratio)

for n1, n2 in antagonisms[10:]:
    freq1 = nutrients[n1].coherence_frequency
    freq2 = nutrients[n2].coherence_frequency
    ratio = max(freq1, freq2) / min(freq1, freq2)
    antagonism_ratios.append(ratio)

# Statistical analysis
synergy_mean = np.mean(synergy_ratios)
synergy_std = np.std(synergy_ratios)
antagonism_mean = np.mean(antagonism_ratios)
antagonism_std = np.std(antagonism_ratios)

print()
print("Statistical Analysis:")
print(f"  Synergies:    {synergy_mean:.2f} ± {synergy_std:.2f} (n={len(synergy_ratios)})")
print(f"  Antagonisms:  {antagonism_mean:.2f} ± {antagonism_std:.2f} (n={len(antagonism_ratios)})")
print()

# Effect size (Cohen's d)
pooled_std = math.sqrt((synergy_std**2 + antagonism_std**2) / 2)
cohens_d = (synergy_mean - antagonism_mean) / pooled_std if pooled_std > 0 else 0

print(f"  Effect Size (Cohen's d): {cohens_d:.3f}")
if abs(cohens_d) < 0.2:
    effect_interpretation = "negligible"
elif abs(cohens_d) < 0.5:
    effect_interpretation = "small"
elif abs(cohens_d) < 0.8:
    effect_interpretation = "medium"
else:
    effect_interpretation = "large"
print(f"  Interpretation: {effect_interpretation}")
print()

# ==============================================================================
# PART 2: COHERENCE DEFICIT ANALYSIS (DISSIDENT DETECTION)
# ==============================================================================

print("=" * 80)
print("PART 2: COHERENCE DEFICIT ANALYSIS")
print("Detecting dissident states in biological nutrient system")
print("=" * 80)
print()

# Calculate NRCI (bioavailability) statistics
nrci_values = [nutrient.bioavailability for nutrient in nutrients.values()]
nrci_mean = np.mean(nrci_values)
nrci_std = np.std(nrci_values)

print(f"NRCI Statistics (n={len(nrci_values)}):")
print(f"  Mean: {nrci_mean:.4f}")
print(f"  Std:  {nrci_std:.4f}")
print(f"  Min:  {min(nrci_values):.4f}")
print(f"  Max:  {max(nrci_values):.4f}")
print()

# Identify potential dissidents (low bioavailability = trapped in suboptimal state)
dissident_threshold = nrci_mean - nrci_std
dissidents = [(name, n.bioavailability) for name, n in nutrients.items() 
              if n.bioavailability < dissident_threshold]
dissidents.sort(key=lambda x: x[1])

print(f"Potential Dissidents (NRCI < {dissident_threshold:.4f}):")
for name, nrci in dissidents[:15]:
    print(f"  {name:20s}: NRCI = {nrci:.4f}")
print()

# Calculate coherence deficit
# Expected coherence for optimal state
expected_nrci = 0.999997  # UBP optimal coherence
actual_mean_nrci = nrci_mean

# Delta deficit
delta_deficit = 1.0 - actual_mean_nrci
delta_deficit_percent = delta_deficit * 100

print(f"Coherence Deficit Analysis:")
print(f"  Expected NRCI (optimal): {expected_nrci:.6f}")
print(f"  Actual mean NRCI:        {actual_mean_nrci:.6f}")
print(f"  Delta deficit (δ):       {delta_deficit:.6f} ({delta_deficit_percent:.2f}%)")
print()

# Compare to theoretical 0.15% from Time study
theoretical_deficit = 0.0015
ratio_to_theory = delta_deficit / theoretical_deficit

print(f"  Theoretical δ (Time study): {theoretical_deficit:.6f} (0.15%)")
print(f"  Ratio (actual/theory):      {ratio_to_theory:.2f}×")
print()

if ratio_to_theory > 100:
    print("  ⚠ Biological systems show MUCH larger deficit than cosmological")
    print("    This suggests different dissident mechanisms or scales")
elif ratio_to_theory > 10:
    print("  ⚠ Biological deficit is significantly larger than cosmological")
elif ratio_to_theory > 0.5:
    print("  ✓ Biological deficit is in same order of magnitude as cosmological")
else:
    print("  ⚠ Biological deficit is smaller than cosmological prediction")
print()

# ==============================================================================
# PART 3: CATEGORY-BASED ANALYSIS
# ==============================================================================

print("=" * 80)
print("PART 3: CATEGORY-BASED ANALYSIS")
print("Analyzing coherence patterns by nutrient category")
print("=" * 80)
print()

# Group by category
category_data = defaultdict(list)
for name, nutrient in nutrients.items():
    category_data[nutrient.category.name].append({
        'name': name,
        'nrci': nutrient.bioavailability,
        'frequency': nutrient.coherence_frequency
    })

# Analyze each category
category_stats = {}
for category, items in category_data.items():
    nrcis = [item['nrci'] for item in items]
    freqs = [item['frequency'] for item in items]
    
    category_stats[category] = {
        'count': len(items),
        'nrci_mean': np.mean(nrcis),
        'nrci_std': np.std(nrcis),
        'freq_mean': np.mean(freqs),
        'freq_std': np.std(freqs),
        'freq_cv': np.std(freqs) / np.mean(freqs) if np.mean(freqs) > 0 else 0
    }

print("Category Statistics:")
print(f"{'Category':<20} {'Count':>6} {'NRCI Mean':>12} {'Freq CV':>12}")
print("-" * 60)
for category in sorted(category_stats.keys()):
    stats = category_stats[category]
    print(f"{category:<20} {stats['count']:>6} {stats['nrci_mean']:>12.4f} {stats['freq_cv']:>12.4f}")
print()

# ==============================================================================
# PART 4: TEMPORAL TRAP ANALYSIS
# ==============================================================================

print("=" * 80)
print("PART 4: TEMPORAL TRAP ANALYSIS")
print("Calculating time dilation in dissident states")
print("=" * 80)
print()

# For each dissident, calculate implied time dilation
# From Time study: time dilation ≈ 1 + δ
print("Time Dilation for Dissidents:")
print(f"{'Nutrient':<20} {'NRCI':>8} {'δ-deficit':>12} {'Time Dilation':>15}")
print("-" * 65)

time_dilations = []
for name, nrci in dissidents[:10]:
    deficit = 1.0 - nrci
    time_dilation = 1.0 + deficit
    time_dilations.append(time_dilation)
    print(f"{name:<20} {nrci:>8.4f} {deficit:>12.6f} {time_dilation:>15.6f}")

print()
print(f"Mean time dilation: {np.mean(time_dilations):.6f}")
print(f"This means time flows ~{(np.mean(time_dilations)-1)*100:.2f}% slower in these states")
print()

# ==============================================================================
# SAVE ALL RESULTS
# ==============================================================================

print("=" * 80)
print("SAVING RESULTS")
print("=" * 80)
print()

results = {
    'frequency_coherence': {
        'synergies': {
            'count': len(synergy_ratios),
            'mean_ratio': float(synergy_mean),
            'std_ratio': float(synergy_std),
            'ratios': [float(r) for r in synergy_ratios]
        },
        'antagonisms': {
            'count': len(antagonism_ratios),
            'mean_ratio': float(antagonism_mean),
            'std_ratio': float(antagonism_std),
            'ratios': [float(r) for r in antagonism_ratios]
        },
        'effect_size': float(cohens_d),
        'effect_interpretation': effect_interpretation
    },
    'coherence_deficit': {
        'nrci_mean': float(nrci_mean),
        'nrci_std': float(nrci_std),
        'delta_deficit': float(delta_deficit),
        'delta_deficit_percent': float(delta_deficit_percent),
        'theoretical_deficit': float(theoretical_deficit),
        'ratio_to_theory': float(ratio_to_theory)
    },
    'dissidents': {
        'count': len(dissidents),
        'threshold': float(dissident_threshold),
        'list': [(name, float(nrci)) for name, nrci in dissidents]
    },
    'temporal_trap': {
        'mean_time_dilation': float(np.mean(time_dilations)),
        'time_slowdown_percent': float((np.mean(time_dilations)-1)*100)
    },
    'category_stats': {cat: {k: float(v) if isinstance(v, (int, float, np.number)) else v 
                             for k, v in stats.items()} 
                      for cat, stats in category_stats.items()}
}

with open('comprehensive_real_analysis_results.json', 'w') as f:
    json.dump(results, f, indent=2)

print("✓ Saved comprehensive_real_analysis_results.json")
print()

print("=" * 80)
print("ANALYSIS COMPLETE")
print("=" * 80)
print()
print("Key Findings:")
print(f"1. Frequency Coherence: {effect_interpretation} effect (d={cohens_d:.3f})")
print(f"2. Biological δ-deficit: {delta_deficit_percent:.2f}% ({ratio_to_theory:.1f}× cosmological)")
print(f"3. Dissidents identified: {len(dissidents)} nutrients")
print(f"4. Time dilation in dissidents: ~{(np.mean(time_dilations)-1)*100:.2f}% slower")
print()
