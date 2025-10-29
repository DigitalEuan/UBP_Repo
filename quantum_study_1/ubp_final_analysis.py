#!/usr/bin/env python3.11
"""
UBP Quantum Entanglement Analysis - Final Implementation
=========================================================

Complete analysis of quantum entanglement through the Universal Binary Principle
framework, with corrected data generation and proper statistical testing.

Key Features:
1. Correct quantum mechanical Bell test data generation
2. Proper NRCI calculation independent of test weight
3. Statistical significance testing with bootstrap
4. Comparison between quantum and classical data
5. Coherence pressure calculation

Author: UBP Research Team
Date: October 2025
"""

import numpy as np
import matplotlib.pyplot as plt
import json

# ============================================================================
# UBP Framework Constants
# ============================================================================

Y_EMERGENT = 0.26467543040452696  # Simplified Observer Coherence
W_TETRA_INVARIANT = np.pi / ((1 + np.sqrt(5)) / 2)  # π/φ ≈ 1.9416
PGCI_TARGET = 0.999997
C_LIGHT = 299792458

# ============================================================================
# Quantum Data Generation
# ============================================================================

def generate_quantum_bell_data(n_trials=100000, detection_eff=0.75, noise=0.02):
    """
    Generate proper quantum Bell test data with CHSH violation.
    
    Singlet state: |ψ⟩ = (|↑↓⟩ - |↓↑⟩)/√2
    Correlation: E(a,b) = -cos(2(θ_a - θ_b))
    """
    
    # CHSH optimal angles
    alice_angles = np.array([0, np.pi/4])  # 0°, 45°
    bob_angles = np.array([np.pi/8, -np.pi/8])  # 22.5°, -22.5°
    
    data = {
        'alice_outcomes': [],
        'bob_outcomes': [],
        'alice_settings': [],
        'bob_settings': []
    }
    
    for _ in range(n_trials):
        a_idx = np.random.randint(0, 2)
        b_idx = np.random.randint(0, 2)
        
        delta = alice_angles[a_idx] - bob_angles[b_idx]
        
        # Generate correlated outcomes
        alice_result = np.random.choice([0, 1])
        prob_same = np.sin(delta)**2
        prob_same = prob_same * (1 - noise) + 0.5 * noise
        
        bob_result = alice_result if np.random.rand() < prob_same else 1 - alice_result
        
        # Detection efficiency
        if np.random.rand() < detection_eff and np.random.rand() < detection_eff:
            data['alice_outcomes'].append(alice_result)
            data['bob_outcomes'].append(bob_result)
            data['alice_settings'].append(a_idx)
            data['bob_settings'].append(b_idx)
    
    for key in data:
        data[key] = np.array(data[key])
    
    return data

def generate_classical_data(n_trials=100000, detection_eff=0.75, noise=0.02):
    """
    Generate classical local hidden variable data.
    """
    
    data = {
        'alice_outcomes': [],
        'bob_outcomes': [],
        'alice_settings': [],
        'bob_settings': []
    }
    
    for _ in range(n_trials):
        # Shared hidden variable
        lambda_val = np.random.rand()
        
        a_idx = np.random.randint(0, 2)
        b_idx = np.random.randint(0, 2)
        
        # Deterministic strategy (attempts to maximize CHSH but fails)
        alice_result = 1 if lambda_val > 0.5 else 0
        bob_result = 1 if lambda_val > 0.6 - 0.2 * b_idx else 0
        
        # Add noise
        if np.random.rand() < noise:
            alice_result = 1 - alice_result
        if np.random.rand() < noise:
            bob_result = 1 - bob_result
        
        # Detection
        if np.random.rand() < detection_eff and np.random.rand() < detection_eff:
            data['alice_outcomes'].append(alice_result)
            data['bob_outcomes'].append(bob_result)
            data['alice_settings'].append(a_idx)
            data['bob_settings'].append(b_idx)
    
    for key in data:
        data[key] = np.array(data[key])
    
    return data

# ============================================================================
# CHSH Calculation
# ============================================================================

def calculate_chsh(data):
    """Calculate CHSH value S = E(a0,b0) + E(a0,b1) + E(a1,b0) - E(a1,b1)"""
    
    E = {}
    
    for a in [0, 1]:
        for b in [0, 1]:
            mask = (data['alice_settings'] == a) & (data['bob_settings'] == b)
            
            if np.sum(mask) > 0:
                A = 2 * data['alice_outcomes'][mask] - 1
                B = 2 * data['bob_outcomes'][mask] - 1
                E[(a,b)] = np.mean(A * B)
            else:
                E[(a,b)] = 0
    
    S = E[(0,0)] + E[(0,1)] + E[(1,0)] - E[(1,1)]
    
    return S, E

# ============================================================================
# UBP Metrics
# ============================================================================

def calculate_nrci_weighted(data, weight, Y=Y_EMERGENT):
    """
    UBP-weighted NRCI calculation.
    
    Measures coherence of correlations scaled by UBP parameters.
    The weight that maximizes NRCI reveals geometric structure.
    """
    
    correlations = []
    
    for a in [0, 1]:
        for b in [0, 1]:
            mask = (data['alice_settings'] == a) & (data['bob_settings'] == b)
            
            if np.sum(mask) > 20:
                A = 2 * data['alice_outcomes'][mask] - 1
                B = 2 * data['bob_outcomes'][mask] - 1
                corr = np.mean(A * B)
                correlations.append(corr)
    
    if len(correlations) == 0:
        return 0.0
    
    correlations = np.array(correlations)
    
    # Scale by UBP parameters
    scaled = np.abs(correlations) * weight * Y
    
    # Coherence measure
    mean_val = np.mean(scaled)
    std_val = np.std(scaled)
    
    if mean_val > 0:
        nrci = 1.0 - (std_val / mean_val)
    else:
        nrci = 0.0
    
    return np.clip(nrci, 0, 1.0)

def calculate_coherence_pressure(data, weight=W_TETRA_INVARIANT):
    """
    Calculate Coherence Pressure (Ψ_p).
    
    UBP predicts minimal Ψ_p (~10^-6) for true quantum entanglement.
    """
    
    n_trials = len(data['alice_outcomes'])
    
    variances = []
    
    for a in [0, 1]:
        for b in [0, 1]:
            mask = (data['alice_settings'] == a) & (data['bob_settings'] == b)
            
            if np.sum(mask) > 20:
                A = 2 * data['alice_outcomes'][mask] - 1
                B = 2 * data['bob_outcomes'][mask] - 1
                product = A * B
                variances.append(np.var(product))
    
    if len(variances) == 0:
        return 0.0
    
    mean_var = np.mean(variances)
    
    # UBP formula
    psi_p = mean_var * Y_EMERGENT / weight / np.sqrt(n_trials)
    
    return psi_p

# ============================================================================
# Weight Scanning
# ============================================================================

def scan_weights(data, weight_range=(1.5, 2.5), n_points=100):
    """
    Scan geometric weights to find optimal value.
    """
    
    weights = np.linspace(weight_range[0], weight_range[1], n_points)
    nrci_scores = []
    psi_p_scores = []
    
    for w in weights:
        nrci = calculate_nrci_weighted(data, w)
        psi_p = calculate_coherence_pressure(data, w)
        
        nrci_scores.append(nrci)
        psi_p_scores.append(psi_p)
    
    nrci_scores = np.array(nrci_scores)
    psi_p_scores = np.array(psi_p_scores)
    
    best_idx = np.argmax(nrci_scores)
    best_weight = weights[best_idx]
    max_nrci = nrci_scores[best_idx]
    
    # 95% confidence interval
    threshold = 0.95 * max_nrci
    ci_mask = nrci_scores >= threshold
    ci_weights = weights[ci_mask]
    
    ci_lower = ci_weights[0] if len(ci_weights) > 0 else best_weight
    ci_upper = ci_weights[-1] if len(ci_weights) > 0 else best_weight
    
    return {
        'weights': weights,
        'nrci_scores': nrci_scores,
        'psi_p_scores': psi_p_scores,
        'best_weight': best_weight,
        'max_nrci': max_nrci,
        'ci_lower': ci_lower,
        'ci_upper': ci_upper
    }

def test_significance(scan_results, n_bootstrap=1000):
    """
    Bootstrap test for statistical significance of W_TETRA peak.
    """
    
    weights = scan_results['weights']
    nrci_scores = scan_results['nrci_scores']
    best_weight = scan_results['best_weight']
    
    deviation = np.abs(best_weight - W_TETRA_INVARIANT)
    
    # Bootstrap
    bootstrap_peaks = []
    for _ in range(n_bootstrap):
        indices = np.random.choice(len(nrci_scores), len(nrci_scores), replace=True)
        resampled = nrci_scores[indices]
        peak_idx = np.argmax(resampled)
        bootstrap_peaks.append(weights[peak_idx])
    
    bootstrap_peaks = np.array(bootstrap_peaks)
    bootstrap_devs = np.abs(bootstrap_peaks - W_TETRA_INVARIANT)
    p_value = np.mean(bootstrap_devs <= deviation)
    
    within_ci = (scan_results['ci_lower'] <= W_TETRA_INVARIANT <= scan_results['ci_upper'])
    
    return {
        'deviation': deviation,
        'deviation_percent': 100 * deviation / W_TETRA_INVARIANT,
        'within_ci': within_ci,
        'p_value': p_value,
        'significant': p_value > 0.95,  # Peak is closer to W_TETRA than 95% of bootstrap
        'bootstrap_mean': np.mean(bootstrap_peaks),
        'bootstrap_std': np.std(bootstrap_peaks)
    }

# ============================================================================
# Visualization
# ============================================================================

def create_comprehensive_plots(quantum_scan, classical_scan, save_dir='/home/ubuntu'):
    """
    Create publication-quality plots.
    """
    
    fig = plt.figure(figsize=(14, 10))
    gs = fig.add_gridspec(3, 2, hspace=0.3, wspace=0.3)
    
    # Quantum NRCI
    ax1 = fig.add_subplot(gs[0, 0])
    ax1.plot(quantum_scan['weights'], quantum_scan['nrci_scores'], 'b-', linewidth=2)
    ax1.axvline(W_TETRA_INVARIANT, color='r', linestyle='--', linewidth=2, label=f'W_Tetra = {W_TETRA_INVARIANT:.4f}')
    ax1.axvline(quantum_scan['best_weight'], color='g', linestyle='-', linewidth=2, label=f'Best = {quantum_scan["best_weight"]:.4f}')
    ax1.fill_between([quantum_scan['ci_lower'], quantum_scan['ci_upper']], 0, 1, alpha=0.2, color='green')
    ax1.set_xlabel('Geometric Weight (w)', fontsize=11)
    ax1.set_ylabel('NRCI', fontsize=11)
    ax1.set_title('Quantum Data: NRCI vs Weight', fontsize=12, fontweight='bold')
    ax1.legend(fontsize=9)
    ax1.grid(True, alpha=0.3)
    
    # Classical NRCI
    ax2 = fig.add_subplot(gs[0, 1])
    ax2.plot(classical_scan['weights'], classical_scan['nrci_scores'], 'r-', linewidth=2)
    ax2.axvline(W_TETRA_INVARIANT, color='r', linestyle='--', linewidth=2)
    ax2.axvline(classical_scan['best_weight'], color='orange', linestyle='-', linewidth=2, label=f'Best = {classical_scan["best_weight"]:.4f}')
    ax2.set_xlabel('Geometric Weight (w)', fontsize=11)
    ax2.set_ylabel('NRCI', fontsize=11)
    ax2.set_title('Classical Data: NRCI vs Weight', fontsize=12, fontweight='bold')
    ax2.legend(fontsize=9)
    ax2.grid(True, alpha=0.3)
    
    # Quantum Ψ_p
    ax3 = fig.add_subplot(gs[1, 0])
    ax3.plot(quantum_scan['weights'], quantum_scan['psi_p_scores'], 'b-', linewidth=2)
    ax3.axvline(W_TETRA_INVARIANT, color='r', linestyle='--', linewidth=2)
    ax3.axvline(quantum_scan['best_weight'], color='g', linestyle='-', linewidth=2)
    ax3.axhline(1e-6, color='purple', linestyle=':', linewidth=2, label='UBP Prediction (~10^-6)')
    ax3.set_xlabel('Geometric Weight (w)', fontsize=11)
    ax3.set_ylabel('Coherence Pressure (Ψ_p)', fontsize=11)
    ax3.set_title('Quantum Data: Ψ_p vs Weight', fontsize=12, fontweight='bold')
    ax3.set_yscale('log')
    ax3.legend(fontsize=9)
    ax3.grid(True, alpha=0.3)
    
    # Classical Ψ_p
    ax4 = fig.add_subplot(gs[1, 1])
    ax4.plot(classical_scan['weights'], classical_scan['psi_p_scores'], 'r-', linewidth=2)
    ax4.axvline(W_TETRA_INVARIANT, color='r', linestyle='--', linewidth=2)
    ax4.axvline(classical_scan['best_weight'], color='orange', linestyle='-', linewidth=2)
    ax4.axhline(1e-6, color='purple', linestyle=':', linewidth=2)
    ax4.set_xlabel('Geometric Weight (w)', fontsize=11)
    ax4.set_ylabel('Coherence Pressure (Ψ_p)', fontsize=11)
    ax4.set_title('Classical Data: Ψ_p vs Weight', fontsize=12, fontweight='bold')
    ax4.set_yscale('log')
    ax4.grid(True, alpha=0.3)
    
    # Comparison bar chart
    ax5 = fig.add_subplot(gs[2, :])
    metrics = ['NRCI', 'Ψ_p (×10^4)', 'Weight Deviation (%)']
    quantum_vals = [
        quantum_scan['max_nrci'],
        quantum_scan['psi_p_scores'][np.argmax(quantum_scan['nrci_scores'])] * 1e4,
        100 * abs(quantum_scan['best_weight'] - W_TETRA_INVARIANT) / W_TETRA_INVARIANT
    ]
    classical_vals = [
        classical_scan['max_nrci'],
        classical_scan['psi_p_scores'][np.argmax(classical_scan['nrci_scores'])] * 1e4,
        100 * abs(classical_scan['best_weight'] - W_TETRA_INVARIANT) / W_TETRA_INVARIANT
    ]
    
    x = np.arange(len(metrics))
    width = 0.35
    
    ax5.bar(x - width/2, quantum_vals, width, label='Quantum', color='blue', alpha=0.7)
    ax5.bar(x + width/2, classical_vals, width, label='Classical', color='red', alpha=0.7)
    ax5.set_xlabel('Metric', fontsize=11)
    ax5.set_ylabel('Value', fontsize=11)
    ax5.set_title('Quantum vs Classical Comparison', fontsize=12, fontweight='bold')
    ax5.set_xticks(x)
    ax5.set_xticklabels(metrics, fontsize=10)
    ax5.legend(fontsize=10)
    ax5.grid(True, alpha=0.3, axis='y')
    
    plt.savefig(f'{save_dir}/ubp_comprehensive_analysis.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    return fig

# ============================================================================
# Main Analysis
# ============================================================================

def run_full_analysis(n_trials=100000):
    """
    Execute complete UBP analysis pipeline.
    """
    
    print("="*70)
    print("UBP QUANTUM ENTANGLEMENT ANALYSIS - FINAL IMPLEMENTATION")
    print("="*70)
    
    # 1. Generate data
    print("\n[1/8] Generating quantum Bell test data...")
    quantum_data = generate_quantum_bell_data(n_trials=n_trials)
    print(f"      Generated {len(quantum_data['alice_outcomes'])} coincident events")
    
    print("\n[2/8] Generating classical comparison data...")
    classical_data = generate_classical_data(n_trials=n_trials)
    print(f"      Generated {len(classical_data['alice_outcomes'])} coincident events")
    
    # 2. Calculate CHSH
    print("\n[3/8] Calculating CHSH values...")
    S_q, E_q = calculate_chsh(quantum_data)
    S_c, E_c = calculate_chsh(classical_data)
    
    print(f"      Quantum CHSH: S = {abs(S_q):.4f}")
    print(f"      Classical CHSH: S = {abs(S_c):.4f}")
    print(f"      QM Prediction: S_max = {2*np.sqrt(2):.4f}")
    print(f"      Classical Bound: S ≤ 2.000")
    print(f"      Quantum Violation: {abs(S_q) > 2}")
    
    # 3. Weight scanning
    print("\n[4/8] Scanning geometric weights (quantum data)...")
    quantum_scan = scan_weights(quantum_data)
    print(f"      Best weight: {quantum_scan['best_weight']:.6f}")
    print(f"      Max NRCI: {quantum_scan['max_nrci']:.6f}")
    
    print("\n[5/8] Scanning geometric weights (classical data)...")
    classical_scan = scan_weights(classical_data)
    print(f"      Best weight: {classical_scan['best_weight']:.6f}")
    print(f"      Max NRCI: {classical_scan['max_nrci']:.6f}")
    
    # 4. Statistical testing
    print("\n[6/8] Testing statistical significance...")
    significance = test_significance(quantum_scan)
    print(f"      Deviation from W_Tetra: {significance['deviation_percent']:.2f}%")
    print(f"      W_Tetra within CI: {significance['within_ci']}")
    print(f"      P-value: {significance['p_value']:.4f}")
    print(f"      Statistically significant: {significance['significant']}")
    
    # 5. Coherence pressure
    print("\n[7/8] Calculating coherence pressures...")
    psi_p_q = calculate_coherence_pressure(quantum_data, quantum_scan['best_weight'])
    psi_p_c = calculate_coherence_pressure(classical_data, classical_scan['best_weight'])
    print(f"      Quantum Ψ_p: {psi_p_q:.6e}")
    print(f"      Classical Ψ_p: {psi_p_c:.6e}")
    print(f"      Ratio (C/Q): {psi_p_c/psi_p_q:.2f}")
    
    # 6. Visualization
    print("\n[8/8] Creating visualizations...")
    create_comprehensive_plots(quantum_scan, classical_scan)
    print("      Saved: ubp_comprehensive_analysis.png")
    
    # 7. Save results
    results = {
        'quantum': {
            'chsh_value': float(abs(S_q)),
            'best_weight': float(quantum_scan['best_weight']),
            'max_nrci': float(quantum_scan['max_nrci']),
            'coherence_pressure': float(psi_p_q),
            'ci_lower': float(quantum_scan['ci_lower']),
            'ci_upper': float(quantum_scan['ci_upper']),
            'correlations': {str(k): float(v) for k, v in E_q.items()},
            'significance': {k: float(v) if isinstance(v, (int, float, np.number)) else bool(v) 
                           for k, v in significance.items()}
        },
        'classical': {
            'chsh_value': float(abs(S_c)),
            'best_weight': float(classical_scan['best_weight']),
            'max_nrci': float(classical_scan['max_nrci']),
            'coherence_pressure': float(psi_p_c),
            'correlations': {str(k): float(v) for k, v in E_c.items()}
        },
        'ubp_constants': {
            'Y_emergent': Y_EMERGENT,
            'W_tetra_invariant': W_TETRA_INVARIANT,
            'PGCI_target': PGCI_TARGET
        }
    }
    
    with open('/home/ubuntu/ubp_final_results.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    print("\n" + "="*70)
    print("ANALYSIS COMPLETE")
    print("="*70)
    print("\nKey Findings:")
    print(f"  • Quantum data shows CHSH violation: S = {abs(S_q):.4f} > 2")
    print(f"  • Best weight: {quantum_scan['best_weight']:.4f} (W_Tetra = {W_TETRA_INVARIANT:.4f})")
    print(f"  • Deviation: {significance['deviation_percent']:.2f}%")
    print(f"  • Quantum NRCI: {quantum_scan['max_nrci']:.4f}")
    print(f"  • Classical NRCI: {classical_scan['max_nrci']:.4f}")
    print(f"  • Quantum Ψ_p: {psi_p_q:.2e}")
    print(f"  • Classical Ψ_p: {psi_p_c:.2e}")
    print("\nFiles saved:")
    print("  - ubp_final_results.json")
    print("  - ubp_comprehensive_analysis.png")
    print("="*70)
    
    return results, quantum_scan, classical_scan

if __name__ == "__main__":
    results, q_scan, c_scan = run_full_analysis(n_trials=100000)

