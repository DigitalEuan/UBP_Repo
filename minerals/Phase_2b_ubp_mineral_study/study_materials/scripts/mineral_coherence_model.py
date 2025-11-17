#!/usr/bin/env python3
"""
UBP Mineral Study - Script 3: Coherence Analysis
=================================================

Uses coherence_substrate.py to model crystalline OffBit patterns
and calculate NRCI for mineral-like configurations.

Tests UBP hypothesis: Stable minerals require high coherence (NRCI >= 0.999999)
"""

import sys
sys.path.insert(0, '.')

from coherence_substrate import *
import numpy as np
import matplotlib.pyplot as plt
import json
from typing import List, Tuple, Dict

# UBP Constants
Y_CONSTANT = np.pi / (np.pi**2 + 2)
OBSERVER_COST = 3.7782
NRCI_THRESHOLD = 0.999999


class MineralCoherenceModel:
    """Model minerals as coherent OffBit patterns in UBP substrate"""
    
    def __init__(self, size: int = 32):
        """Initialize with OffBit array size"""
        self.size = size
        self.substrate = CoherenceSubstrate(width=size)
    
    def encode_mineral_structure(self, Z: int, space_group_sym: float, 
                                 n_elements: int) -> OffBitArray:
        """
        Encode a mineral structure as an OffBit pattern.
        
        Parameters:
        - Z: Formula units (maps to pattern complexity)
        - space_group_sym: Symmetry index 0-1 (maps to pattern regularity)
        - n_elements: Number of distinct elements (maps to information entropy)
        """
        pattern = OffBitArray(size=self.size)
        
        # Set Reality layer based on Z (physical manifestation)
        # More formula units → more bits set in Reality
        n_reality_bits = min(self.size // 4, int(Z * 0.5))
        reality_indices = np.random.choice(self.size, size=n_reality_bits, replace=False)
        for idx in reality_indices:
            pattern.bits[idx] = toggle_bit(pattern.bits[idx], layer='reality')
        
        # Set Information layer based on space group symmetry
        # Higher symmetry → more regular pattern
        n_info_bits = int(self.size * space_group_sym * 0.25)
        info_indices = np.linspace(0, self.size-1, n_info_bits, dtype=int)
        for idx in info_indices:
            pattern.bits[idx] = toggle_bit(pattern.bits[idx], layer='information')
        
        # Set Activation layer based on number of elements
        # More elements → more activated states
        n_activation_bits = min(self.size // 4, n_elements * 2)
        activation_indices = np.random.choice(self.size, size=n_activation_bits, replace=False)
        for idx in activation_indices:
            pattern.bits[idx] = toggle_bit(pattern.bits[idx], layer='activation')
        
        return pattern
    
    def calculate_pattern_coherence(self, pattern: OffBitArray) -> float:
        """
        Calculate coherence of an OffBit pattern.
        
        Uses substrate's built-in coherence calculation.
        """
        # Store pattern in substrate
        key = f"mineral_test"
        self.substrate.store(key, pattern.to_bytes())
        
        # Calculate coherence
        coherence = self.substrate.calculate_coherence(pattern.to_bytes())
        
        return coherence
    
    def is_stable_mineral(self, pattern: OffBitArray, 
                         coherence_threshold: float = NRCI_THRESHOLD) -> bool:
        """
        Determine if pattern represents a stable mineral.
        
        Stability requires: NRCI >= threshold
        """
        coherence = self.calculate_pattern_coherence(pattern)
        return coherence >= coherence_threshold


def simulate_mineral_stability_space(n_samples: int = 1000) -> Dict:
    """
    Sample the (Z, symmetry, n_elements) space and test stability.
    
    This maps out which regions of parameter space produce stable minerals.
    """
    model = MineralCoherenceModel(size=32)
    
    results = {
        'samples': [],
        'stable_count': 0,
        'unstable_count': 0
    }
    
    for i in range(n_samples):
        # Sample parameters from realistic mineral distributions
        Z = np.random.choice([1, 2, 4, 8, 16], p=[0.25, 0.35, 0.25, 0.10, 0.05])
        symmetry = np.random.beta(2, 2)  # Peaked around 0.5
        n_elements = np.random.choice([1, 2, 3, 4], p=[0.05, 0.50, 0.35, 0.10])
        
        # Encode as OffBit pattern
        pattern = model.encode_mineral_structure(Z, symmetry, n_elements)
        
        # Calculate coherence
        coherence = model.calculate_pattern_coherence(pattern)
        is_stable = coherence >= NRCI_THRESHOLD
        
        results['samples'].append({
            'Z': int(Z),
            'symmetry': float(symmetry),
            'n_elements': int(n_elements),
            'coherence': float(coherence),
            'is_stable': bool(is_stable)
        })
        
        if is_stable:
            results['stable_count'] += 1
        else:
            results['unstable_count'] += 1
    
    results['stability_rate'] = results['stable_count'] / n_samples
    
    return results


def analyze_coherence_vs_complexity(n_samples: int = 500) -> Dict:
    """
    Analyze how coherence varies with mineral complexity.
    
    Tests hypothesis: Higher complexity → lower coherence → less likely stable
    """
    model = MineralCoherenceModel(size=32)
    
    # Define complexity as: I_cmplx ≈ Z * (1/symmetry) * n_elements
    results = {
        'complexity': [],
        'coherence': [],
        'Z_values': [],
        'is_stable': []
    }
    
    for i in range(n_samples):
        Z = np.random.choice([1, 2, 4, 8, 16, 32])
        symmetry = np.random.uniform(0.1, 1.0)
        n_elements = np.random.randint(1, 5)
        
        complexity = Z * (1.0 / symmetry) * n_elements
        
        pattern = model.encode_mineral_structure(Z, symmetry, n_elements)
        coherence = model.calculate_pattern_coherence(pattern)
        
        results['complexity'].append(float(complexity))
        results['coherence'].append(float(coherence))
        results['Z_values'].append(int(Z))
        results['is_stable'].append(bool(coherence >= NRCI_THRESHOLD))
    
    # Analyze correlation
    coherence_arr = np.array(results['coherence'])
    complexity_arr = np.array(results['complexity'])
    
    correlation = np.corrcoef(complexity_arr, coherence_arr)[0, 1]
    
    results['correlation'] = float(correlation)
    results['interpretation'] = "Negative correlation = higher complexity → lower coherence" if correlation < 0 else "Positive correlation"
    
    return results


def estimate_stable_mineral_count_from_coherence(N_geometric: float = 1.5e6) -> Dict:
    """
    Estimate how many geometrically feasible states are actually coherent.
    
    This provides the "coherence filter" factor for the final prediction.
    """
    # Run stability simulation
    print("    Running stability simulation (this may take a minute)...")
    n_test = 2000
    stability_results = simulate_mineral_stability_space(n_test)
    
    stability_rate = stability_results['stability_rate']
    
    # Apply to geometric states
    N_stable = N_geometric * stability_rate
    
    # Apply TGIC constraint (3-6-9 pattern)
    TGIC_factor = 0.3
    N_TGIC = N_stable * TGIC_factor
    
    # Observer cost
    observer_factor = 1.0 / OBSERVER_COST
    N_observable = N_TGIC * observer_factor
    
    # Y scaling
    N_final = N_observable / Y_CONSTANT
    
    return {
        'N_geometric': float(N_geometric),
        'stability_rate': float(stability_rate),
        'N_after_coherence': float(N_stable),
        'N_after_TGIC': float(N_TGIC),
        'N_after_observer': float(N_observable),
        'N_final_prediction': float(N_final),
        'observed_minerals': 5000,
        'prediction_vs_observed': float(N_final / 5000)
    }


def visualize_coherence_analysis(stability_results: Dict, complexity_results: Dict):
    """Create visualization of coherence analysis"""
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    # Plot 1: Coherence distribution
    ax = axes[0, 0]
    coherences = [s['coherence'] for s in stability_results['samples']]
    ax.hist(coherences, bins=50, color='blue', alpha=0.7, edgecolor='black')
    ax.axvline(NRCI_THRESHOLD, color='red', linestyle='--', linewidth=2, 
               label=f'Stability Threshold = {NRCI_THRESHOLD}')
    ax.set_xlabel('Coherence (NRCI)', fontsize=12)
    ax.set_ylabel('Count', fontsize=12)
    ax.set_title('Distribution of Mineral Pattern Coherence', fontsize=14, fontweight='bold')
    ax.legend(fontsize=10)
    ax.grid(True, alpha=0.3, axis='y')
    
    # Plot 2: Stability by Z
    ax = axes[0, 1]
    Z_values = sorted(set(s['Z'] for s in stability_results['samples']))
    stable_by_Z = {z: 0 for z in Z_values}
    total_by_Z = {z: 0 for z in Z_values}
    
    for s in stability_results['samples']:
        total_by_Z[s['Z']] += 1
        if s['is_stable']:
            stable_by_Z[s['Z']] += 1
    
    stability_rates = [stable_by_Z[z] / total_by_Z[z] for z in Z_values]
    
    ax.bar(Z_values, stability_rates, color='green', alpha=0.7, edgecolor='black')
    ax.set_xlabel('Formula Units (Z)', fontsize=12)
    ax.set_ylabel('Stability Rate', fontsize=12)
    ax.set_title('Stability Rate by Formula Units', fontsize=14, fontweight='bold')
    ax.set_ylim(0, 1)
    ax.grid(True, alpha=0.3, axis='y')
    
    # Plot 3: Coherence vs Complexity
    ax = axes[1, 0]
    complexity = np.array(complexity_results['complexity'])
    coherence = np.array(complexity_results['coherence'])
    is_stable = np.array(complexity_results['is_stable'])
    
    # Separate stable and unstable
    ax.scatter(complexity[~is_stable], coherence[~is_stable], 
               c='red', alpha=0.5, s=20, label='Unstable')
    ax.scatter(complexity[is_stable], coherence[is_stable], 
               c='green', alpha=0.7, s=20, label='Stable')
    ax.axhline(NRCI_THRESHOLD, color='orange', linestyle='--', linewidth=2, 
               label=f'Threshold = {NRCI_THRESHOLD}')
    
    ax.set_xlabel('Complexity (Z × 1/symmetry × n_elements)', fontsize=12)
    ax.set_ylabel('Coherence (NRCI)', fontsize=12)
    ax.set_title(f'Coherence vs Complexity (r = {complexity_results["correlation"]:.3f})', 
                 fontsize=14, fontweight='bold')
    ax.legend(fontsize=10)
    ax.grid(True, alpha=0.3)
    
    # Plot 4: Stability by symmetry
    ax = axes[1, 1]
    symmetries = [s['symmetry'] for s in stability_results['samples']]
    stable_mask = [s['is_stable'] for s in stability_results['samples']]
    
    sym_bins = np.linspace(0, 1, 11)
    stable_hist, _ = np.histogram([symmetries[i] for i in range(len(symmetries)) if stable_mask[i]], bins=sym_bins)
    total_hist, _ = np.histogram(symmetries, bins=sym_bins)
    
    bin_centers = (sym_bins[:-1] + sym_bins[1:]) / 2
    stability_by_sym = stable_hist / np.maximum(total_hist, 1)
    
    ax.plot(bin_centers, stability_by_sym, 'o-', color='purple', linewidth=2, markersize=8)
    ax.fill_between(bin_centers, 0, stability_by_sym, alpha=0.3, color='purple')
    ax.set_xlabel('Space Group Symmetry Index', fontsize=12)
    ax.set_ylabel('Stability Rate', fontsize=12)
    ax.set_title('Stability Rate by Symmetry', fontsize=14, fontweight='bold')
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.grid(True, alpha=0.3)
    
    # Add UBP annotation
    fig.text(0.5, 0.02, 
             f'UBP Coherence Model: Y = {Y_CONSTANT:.6f}, Observer Cost = {OBSERVER_COST:.4f}, NRCI Threshold = {NRCI_THRESHOLD}',
             ha='center', fontsize=10, style='italic', 
             bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.5))
    
    plt.tight_layout(rect=[0, 0.03, 1, 0.97])
    plt.savefig('mineral_coherence_analysis.png', dpi=150, bbox_inches='tight')
    print("[Visualization] Saved to: mineral_coherence_analysis.png")


def main():
    print("=" * 70)
    print("UBP MINERAL STUDY - COHERENCE ANALYSIS")
    print("=" * 70)
    print()
    
    print("[1] Testing mineral pattern coherence...")
    print(f"    NRCI threshold for stability: {NRCI_THRESHOLD}")
    print()
    
    # Simulate stability space
    print("[2] Simulating mineral stability space...")
    n_test = 1000
    stability_results = simulate_mineral_stability_space(n_test)
    print(f"    Samples tested: {n_test}")
    print(f"    Stable minerals: {stability_results['stable_count']}")
    print(f"    Unstable minerals: {stability_results['unstable_count']}")
    print(f"    Stability rate: {stability_results['stability_rate']*100:.2f}%")
    print()
    
    # Analyze coherence vs complexity
    print("[3] Analyzing coherence vs complexity...")
    complexity_results = analyze_coherence_vs_complexity(n_samples=500)
    print(f"    Correlation coefficient: {complexity_results['correlation']:.4f}")
    print(f"    {complexity_results['interpretation']}")
    print()
    
    # Estimate stable mineral count
    print("[4] Estimating stable mineral count from coherence...")
    N_geometric = 1.5e6  # From Script 1
    estimate = estimate_stable_mineral_count_from_coherence(N_geometric)
    print(f"    Geometric states: {estimate['N_geometric']:.2e}")
    print(f"    Stability rate: {estimate['stability_rate']*100:.2f}%")
    print(f"    After coherence filter: {estimate['N_after_coherence']:.0f}")
    print(f"    After TGIC constraint: {estimate['N_after_TGIC']:.0f}")
    print(f"    After observer cost: {estimate['N_after_observer']:.0f}")
    print(f"    Final Y-scaled prediction: {estimate['N_final_prediction']:.0f}")
    print(f"    Observed Earth minerals: {estimate['observed_minerals']}")
    print(f"    Prediction / Observed: {estimate['prediction_vs_observed']:.2f}x")
    print()
    
    # Save results
    results = {
        'stability_simulation': {
            'n_samples': n_test,
            'stable_count': stability_results['stable_count'],
            'stability_rate': stability_results['stability_rate']
        },
        'complexity_analysis': {
            'correlation': complexity_results['correlation'],
            'interpretation': complexity_results['interpretation']
        },
        'mineral_count_estimate': estimate
    }
    
    with open('coherence_results.json', 'w') as f:
        json.dump(results, f, indent=2)
    print("[5] Results saved to: coherence_results.json")
    print()
    
    # Visualize
    print("[6] Creating visualizations...")
    visualize_coherence_analysis(stability_results, complexity_results)
    print()
    
    print("=" * 70)
    print("COHERENCE CONCLUSIONS")
    print("=" * 70)
    print(f"1. Only {stability_results['stability_rate']*100:.1f}% of geometric states are coherent enough")
    print(f"2. Complexity and coherence are {'negatively' if complexity_results['correlation'] < 0 else 'positively'} correlated")
    print(f"3. Final UBP prediction: ~{estimate['N_final_prediction']:.0f} stable minerals possible")
    print(f"4. This is {estimate['prediction_vs_observed']:.2f}x the observed count")
    print(f"5. Coherence acts as critical 'information filter' for stability")
    print()
    
    return results


if __name__ == '__main__':
    results = main()
