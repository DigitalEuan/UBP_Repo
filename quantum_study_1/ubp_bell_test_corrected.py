#!/usr/bin/env python3.11
"""
UBP Quantum Entanglement Analysis - Corrected Implementation
============================================================

This script implements a rigorous test of the Universal Binary Principle (UBP)
framework against quantum entanglement data from Bell inequality tests.

Key Corrections from Original Study:
1. Proper NRCI calculation independent of test weight
2. Realistic quantum correlation generation (cos²θ for polarization)
3. Statistical significance testing
4. Comparison to quantum mechanical predictions and classical bounds
5. Proper coherence pressure calculation with physical units

Author: UBP Research Team
Date: October 2025
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
from scipy.optimize import minimize_scalar
import json

# ============================================================================
# UBP Framework Constants (from updated paper)
# ============================================================================

# Core UBP Constants
Y_EMERGENT = 0.26467543040452696  # Simplified Observer Coherence (SOC)
W_TETRA_INVARIANT = np.pi / ((1 + np.sqrt(5)) / 2)  # π/φ ≈ 1.9416
PGCI_TARGET = 0.999997  # Global Coherence Invariant target
C_LIGHT = 299792458  # Speed of light (m/s) - master clock rate

# Experimental Parameters
DETECTION_EFFICIENCY = 0.75  # Realistic for loophole-free tests
NOISE_LEVEL = 0.02  # 2% measurement noise

# ============================================================================
# Quantum Mechanical Bell Test Data Generation
# ============================================================================

def generate_bell_test_data(n_trials=100000, settings_per_party=2, 
                           detection_eff=DETECTION_EFFICIENCY,
                           noise_level=NOISE_LEVEL):
    """
    Generate realistic Bell test data matching quantum mechanical predictions.
    
    Uses singlet state |ψ⟩ = (|01⟩ - |10⟩)/√2 with polarization measurements.
    
    Parameters:
    -----------
    n_trials : int
        Number of measurement trials
    settings_per_party : int
        Number of measurement settings (2 for CHSH)
    detection_eff : float
        Detection efficiency (must be > 2/3 for loophole-free)
    noise_level : float
        Measurement noise level
        
    Returns:
    --------
    dict : Bell test data with measurement outcomes and settings
    """
    
    # CHSH optimal angles (in radians)
    # Alice: 0, π/2
    # Bob: π/4, -π/4
    alice_angles = np.array([0, np.pi/2])
    bob_angles = np.array([np.pi/4, -np.pi/4])
    
    data = {
        'alice_outcomes': [],
        'bob_outcomes': [],
        'alice_settings': [],
        'bob_settings': [],
        'coincidences': []
    }
    
    for trial in range(n_trials):
        # Random setting choices
        a_setting = np.random.randint(0, settings_per_party)
        b_setting = np.random.randint(0, settings_per_party)
        
        # Angle difference
        theta_diff = alice_angles[a_setting] - bob_angles[b_setting]
        
        # For singlet state |ψ⟩ = (|01⟩ - |10⟩)/√2:
        # Correlation E(a,b) = -cos(2θ) where θ is angle difference
        # P(same) = sin²(θ), P(different) = cos²(θ)
        
        # Quantum mechanical prediction
        prob_same = np.sin(theta_diff)**2
        
        # Add noise
        prob_same = prob_same * (1 - noise_level) + 0.5 * noise_level
        
        # Generate outcomes
        alice_outcome = np.random.choice([0, 1])
        
        if np.random.rand() < prob_same:
            # Same outcome
            bob_outcome = alice_outcome
        else:
            # Different outcome (anti-correlated)
            bob_outcome = 1 - alice_outcome
        
        # Apply detection efficiency
        alice_detected = np.random.rand() < detection_eff
        bob_detected = np.random.rand() < detection_eff
        
        if alice_detected and bob_detected:
            data['alice_outcomes'].append(alice_outcome)
            data['bob_outcomes'].append(bob_outcome)
            data['alice_settings'].append(a_setting)
            data['bob_settings'].append(b_setting)
            data['coincidences'].append(1)
    
    # Convert to numpy arrays
    for key in data:
        data[key] = np.array(data[key])
    
    print(f"Generated {len(data['alice_outcomes'])} coincident events")
    print(f"Detection efficiency: {len(data['alice_outcomes'])/n_trials:.3f}")
    
    return data

def calculate_chsh_value(data):
    """
    Calculate CHSH value S = E(a0,b0) + E(a0,b1) + E(a1,b0) - E(a1,b1)
    
    Quantum prediction: S_max = 2√2 ≈ 2.828
    Classical bound: S ≤ 2
    """
    
    correlations = {}
    
    for a in [0, 1]:
        for b in [0, 1]:
            # Select trials with these settings
            mask = (data['alice_settings'] == a) & (data['bob_settings'] == b)
            
            if np.sum(mask) > 0:
                alice_vals = 2 * data['alice_outcomes'][mask] - 1  # Convert to ±1
                bob_vals = 2 * data['bob_outcomes'][mask] - 1
                
                # Correlation E(a,b) = ⟨A_a B_b⟩
                correlations[(a,b)] = np.mean(alice_vals * bob_vals)
            else:
                correlations[(a,b)] = 0
    
    # CHSH combination
    S = correlations[(0,0)] + correlations[(0,1)] + correlations[(1,0)] - correlations[(1,1)]
    
    return S, correlations

# ============================================================================
# Corrected NRCI Calculation
# ============================================================================

def calculate_nrci_corrected(data, weight=None):
    """
    Corrected NRCI calculation that is independent of the test weight.
    
    NRCI measures the coherence/fidelity of the correlations, not their magnitude.
    High NRCI (→1) indicates low noise and high pattern fidelity.
    
    This version uses the coefficient of variation approach:
    NRCI = 1 - (std_dev / mean) for anti-correlations
    """
    
    alice_outcomes = data['alice_outcomes']
    bob_outcomes = data['bob_outcomes']
    
    # XOR for anti-correlation (entangled singlet state)
    xor_values = np.bitwise_xor(alice_outcomes, bob_outcomes).astype(float)
    
    # For perfect anti-correlation, XOR should always be 1
    # NRCI measures deviation from this ideal
    
    mean_xor = np.mean(xor_values)
    std_xor = np.std(xor_values)
    
    if mean_xor > 0:
        # Coefficient of variation approach
        cv = std_xor / mean_xor
        nrci = 1.0 - cv
    else:
        nrci = 0.0
    
    # Clip to [0, 1]
    nrci = np.clip(nrci, 0, 1.0)
    
    return nrci

def calculate_nrci_weighted(data, weight, Y=Y_EMERGENT):
    """
    Alternative NRCI that incorporates UBP weight scaling.
    
    This version scales correlations by weight*Y before measuring coherence.
    The weight that maximizes NRCI should reveal geometric structure.
    """
    
    alice_outcomes = data['alice_outcomes']
    bob_outcomes = data['bob_outcomes']
    
    # Calculate correlations for each setting pair
    correlations = []
    
    for a in [0, 1]:
        for b in [0, 1]:
            mask = (data['alice_settings'] == a) & (data['bob_settings'] == b)
            
            if np.sum(mask) > 10:  # Minimum sample size
                alice_vals = 2 * data['alice_outcomes'][mask] - 1
                bob_vals = 2 * data['bob_outcomes'][mask] - 1
                corr = np.mean(alice_vals * bob_vals)
                correlations.append(corr)
    
    if len(correlations) == 0:
        return 0.0
    
    correlations = np.array(correlations)
    
    # Scale by UBP parameters
    scaled_corrs = correlations * weight * Y
    
    # Measure coherence as inverse of variance
    mean_corr = np.mean(np.abs(scaled_corrs))
    std_corr = np.std(scaled_corrs)
    
    if mean_corr > 0:
        nrci = 1.0 - (std_corr / mean_corr)
    else:
        nrci = 0.0
    
    return np.clip(nrci, 0, 1.0)

# ============================================================================
# Coherence Pressure Calculation
# ============================================================================

def calculate_coherence_pressure(data, weight=W_TETRA_INVARIANT, 
                                 distance_m=187.0):
    """
    Calculate Coherence Pressure (Ψ_p) - the computational stress of maintaining
    entanglement correlations.
    
    UBP predicts Ψ_p should be minimal (~10^-6) for true quantum entanglement
    and elevated for classical simulations.
    
    Parameters:
    -----------
    data : dict
        Bell test data
    weight : float
        Geometric weight (w_Ent)
    distance_m : float
        Spatial separation in meters (NIST: 187m, Delft: 1300m)
        
    Returns:
    --------
    float : Coherence pressure (dimensionless)
    """
    
    n_trials = len(data['alice_outcomes'])
    
    # Calculate correlation variance across setting combinations
    variances = []
    
    for a in [0, 1]:
        for b in [0, 1]:
            mask = (data['alice_settings'] == a) & (data['bob_settings'] == b)
            
            if np.sum(mask) > 10:
                alice_vals = 2 * data['alice_outcomes'][mask] - 1
                bob_vals = 2 * data['bob_outcomes'][mask] - 1
                corr_product = alice_vals * bob_vals
                variances.append(np.var(corr_product))
    
    if len(variances) == 0:
        return 0.0
    
    mean_variance = np.mean(variances)
    
    # UBP formula: Ψ_p ∝ variance / (weight * Y_emergent)
    # Normalized by number of trials and distance
    psi_p = mean_variance * Y_EMERGENT / weight
    
    # Normalize by trial count
    psi_p = psi_p / np.sqrt(n_trials)
    
    return psi_p

# ============================================================================
# Weight Optimization and Statistical Testing
# ============================================================================

def scan_weights(data, weight_range=(1.5, 2.5), n_points=100):
    """
    Scan over geometric weights to find the value that maximizes NRCI.
    
    UBP hypothesis: The optimal weight should be close to W_TETRA_INVARIANT.
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
    
    # Find optimal weight
    best_idx = np.argmax(nrci_scores)
    best_weight = weights[best_idx]
    max_nrci = nrci_scores[best_idx]
    
    # Calculate confidence interval (weights within 95% of max NRCI)
    threshold = 0.95 * max_nrci
    ci_mask = nrci_scores >= threshold
    ci_weights = weights[ci_mask]
    
    if len(ci_weights) > 0:
        ci_lower = ci_weights[0]
        ci_upper = ci_weights[-1]
    else:
        ci_lower = best_weight
        ci_upper = best_weight
    
    results = {
        'weights': weights,
        'nrci_scores': nrci_scores,
        'psi_p_scores': psi_p_scores,
        'best_weight': best_weight,
        'max_nrci': max_nrci,
        'ci_lower': ci_lower,
        'ci_upper': ci_upper,
        'w_tetra': W_TETRA_INVARIANT
    }
    
    return results

def statistical_significance_test(scan_results, n_bootstrap=1000):
    """
    Test whether the peak at W_TETRA is statistically significant.
    
    Null hypothesis: Weight scan shows no preference for W_TETRA.
    """
    
    weights = scan_results['weights']
    nrci_scores = scan_results['nrci_scores']
    best_weight = scan_results['best_weight']
    w_tetra = scan_results['w_tetra']
    
    # Deviation from tetrahedral invariant
    deviation = np.abs(best_weight - w_tetra)
    deviation_percent = 100 * deviation / w_tetra
    
    # Is W_TETRA within confidence interval?
    within_ci = (scan_results['ci_lower'] <= w_tetra <= scan_results['ci_upper'])
    
    # Bootstrap test: resample NRCI scores and find peak
    bootstrap_peaks = []
    
    for _ in range(n_bootstrap):
        # Resample with replacement
        indices = np.random.choice(len(nrci_scores), len(nrci_scores), replace=True)
        resampled_nrci = nrci_scores[indices]
        peak_idx = np.argmax(resampled_nrci)
        bootstrap_peaks.append(weights[peak_idx])
    
    bootstrap_peaks = np.array(bootstrap_peaks)
    
    # P-value: fraction of bootstrap peaks farther from W_TETRA than observed
    bootstrap_deviations = np.abs(bootstrap_peaks - w_tetra)
    p_value = np.mean(bootstrap_deviations >= deviation)
    
    significance = {
        'deviation_from_tetra': deviation,
        'deviation_percent': deviation_percent,
        'within_ci': within_ci,
        'p_value': p_value,
        'significant': p_value < 0.05,
        'bootstrap_mean': np.mean(bootstrap_peaks),
        'bootstrap_std': np.std(bootstrap_peaks)
    }
    
    return significance

# ============================================================================
# Classical vs Quantum Comparison
# ============================================================================

def generate_classical_fake_data(n_trials=100000, chsh_target=2.4):
    """
    Generate classical data that attempts to violate Bell inequality
    using local hidden variables (LHV) model.
    
    This should show elevated Ψ_p and lower NRCI compared to true quantum data.
    """
    
    # Classical correlation model with shared randomness
    data = {
        'alice_outcomes': [],
        'bob_outcomes': [],
        'alice_settings': [],
        'bob_settings': [],
        'coincidences': []
    }
    
    for trial in range(n_trials):
        # Shared hidden variable
        lambda_hidden = np.random.rand()
        
        a_setting = np.random.randint(0, 2)
        b_setting = np.random.randint(0, 2)
        
        # Classical deterministic strategy to maximize CHSH
        # This is a "fake" that tries to mimic quantum correlations
        
        # Threshold-based strategy
        if a_setting == 0:
            alice_outcome = 1 if lambda_hidden > 0.5 else 0
        else:
            alice_outcome = 1 if lambda_hidden > 0.3 else 0
        
        if b_setting == 0:
            bob_outcome = 1 if lambda_hidden > 0.6 else 0
        else:
            bob_outcome = 1 if lambda_hidden > 0.4 else 0
        
        # Add some noise
        if np.random.rand() < NOISE_LEVEL:
            alice_outcome = 1 - alice_outcome
        if np.random.rand() < NOISE_LEVEL:
            bob_outcome = 1 - bob_outcome
        
        # Detection efficiency
        if np.random.rand() < DETECTION_EFFICIENCY and np.random.rand() < DETECTION_EFFICIENCY:
            data['alice_outcomes'].append(alice_outcome)
            data['bob_outcomes'].append(bob_outcome)
            data['alice_settings'].append(a_setting)
            data['bob_settings'].append(b_setting)
            data['coincidences'].append(1)
    
    for key in data:
        data[key] = np.array(data[key])
    
    return data

# ============================================================================
# Visualization
# ============================================================================

def plot_weight_scan(scan_results, save_path=None):
    """
    Plot NRCI and Ψ_p as functions of weight.
    """
    
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))
    
    weights = scan_results['weights']
    nrci_scores = scan_results['nrci_scores']
    psi_p_scores = scan_results['psi_p_scores']
    best_weight = scan_results['best_weight']
    w_tetra = scan_results['w_tetra']
    
    # NRCI plot
    ax1.plot(weights, nrci_scores, 'b-', linewidth=2, label='NRCI Score')
    ax1.axvline(w_tetra, color='r', linestyle='--', linewidth=2, 
                label=f'W_Tetra = {w_tetra:.4f}')
    ax1.axvline(best_weight, color='g', linestyle='-', linewidth=2,
                label=f'Best Fit = {best_weight:.4f}')
    ax1.fill_between([scan_results['ci_lower'], scan_results['ci_upper']], 
                     0, 1, alpha=0.2, color='green', label='95% CI')
    ax1.set_xlabel('Geometric Weight (w)', fontsize=12)
    ax1.set_ylabel('NRCI Score', fontsize=12)
    ax1.set_title('Non-Random Coherence Index vs. Geometric Weight', fontsize=14)
    ax1.legend(fontsize=10)
    ax1.grid(True, alpha=0.3)
    
    # Ψ_p plot
    ax2.plot(weights, psi_p_scores, 'r-', linewidth=2, label='Coherence Pressure')
    ax2.axvline(w_tetra, color='r', linestyle='--', linewidth=2)
    ax2.axvline(best_weight, color='g', linestyle='-', linewidth=2)
    ax2.set_xlabel('Geometric Weight (w)', fontsize=12)
    ax2.set_ylabel('Coherence Pressure (Ψ_p)', fontsize=12)
    ax2.set_title('Coherence Pressure vs. Geometric Weight', fontsize=14)
    ax2.set_yscale('log')
    ax2.legend(fontsize=10)
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    
    return fig

# ============================================================================
# Main Analysis Pipeline
# ============================================================================

def run_complete_analysis(n_trials=100000, save_results=True):
    """
    Run complete UBP analysis on Bell test data.
    """
    
    print("="*70)
    print("UBP Quantum Entanglement Analysis - Corrected Implementation")
    print("="*70)
    
    # Generate quantum data
    print("\n1. Generating quantum Bell test data...")
    quantum_data = generate_bell_test_data(n_trials=n_trials)
    
    # Calculate CHSH
    print("\n2. Calculating CHSH value...")
    S_quantum, corrs_quantum = calculate_chsh_value(quantum_data)
    print(f"   CHSH value: S = {S_quantum:.4f}")
    print(f"   Quantum prediction: S_max = {2*np.sqrt(2):.4f}")
    print(f"   Classical bound: S ≤ 2.000")
    print(f"   Violation: {S_quantum > 2}")
    
    # Basic NRCI
    print("\n3. Calculating basic NRCI...")
    nrci_basic = calculate_nrci_corrected(quantum_data)
    print(f"   NRCI (unweighted): {nrci_basic:.6f}")
    
    # Weight scan
    print("\n4. Scanning geometric weights...")
    scan_results = scan_weights(quantum_data)
    print(f"   Best weight: {scan_results['best_weight']:.6f}")
    print(f"   W_Tetra invariant: {W_TETRA_INVARIANT:.6f}")
    print(f"   Deviation: {abs(scan_results['best_weight'] - W_TETRA_INVARIANT):.6f}")
    print(f"   Max NRCI: {scan_results['max_nrci']:.6f}")
    print(f"   95% CI: [{scan_results['ci_lower']:.6f}, {scan_results['ci_upper']:.6f}]")
    
    # Statistical significance
    print("\n5. Testing statistical significance...")
    significance = statistical_significance_test(scan_results)
    print(f"   Deviation from W_Tetra: {significance['deviation_percent']:.2f}%")
    print(f"   W_Tetra within CI: {significance['within_ci']}")
    print(f"   P-value: {significance['p_value']:.4f}")
    print(f"   Statistically significant: {significance['significant']}")
    
    # Coherence pressure
    print("\n6. Calculating coherence pressure...")
    psi_p_quantum = calculate_coherence_pressure(quantum_data, scan_results['best_weight'])
    print(f"   Ψ_p (quantum): {psi_p_quantum:.6e}")
    print(f"   UBP prediction: ~10^-6")
    
    # Classical comparison
    print("\n7. Generating classical fake data for comparison...")
    classical_data = generate_classical_fake_data(n_trials=n_trials)
    S_classical, _ = calculate_chsh_value(classical_data)
    scan_classical = scan_weights(classical_data)
    psi_p_classical = calculate_coherence_pressure(classical_data, scan_classical['best_weight'])
    
    print(f"   Classical CHSH: S = {S_classical:.4f}")
    print(f"   Classical best weight: {scan_classical['best_weight']:.6f}")
    print(f"   Classical max NRCI: {scan_classical['max_nrci']:.6f}")
    print(f"   Classical Ψ_p: {psi_p_classical:.6e}")
    
    print("\n8. Comparison:")
    print(f"   Quantum vs Classical NRCI: {scan_results['max_nrci']:.6f} vs {scan_classical['max_nrci']:.6f}")
    print(f"   Quantum vs Classical Ψ_p: {psi_p_quantum:.6e} vs {psi_p_classical:.6e}")
    print(f"   Ψ_p ratio (Classical/Quantum): {psi_p_classical/psi_p_quantum:.2f}")
    
    # Visualization
    print("\n9. Creating visualizations...")
    fig = plot_weight_scan(scan_results, save_path='/home/ubuntu/weight_scan_quantum.png')
    plt.close()
    
    fig_classical = plot_weight_scan(scan_classical, save_path='/home/ubuntu/weight_scan_classical.png')
    plt.close()
    
    # Save results
    if save_results:
        results_dict = {
            'quantum': {
                'chsh_value': float(S_quantum),
                'best_weight': float(scan_results['best_weight']),
                'max_nrci': float(scan_results['max_nrci']),
                'coherence_pressure': float(psi_p_quantum),
                'ci_lower': float(scan_results['ci_lower']),
                'ci_upper': float(scan_results['ci_upper']),
                'significance': {
                    'deviation_from_tetra': float(significance['deviation_from_tetra']),
                    'deviation_percent': float(significance['deviation_percent']),
                    'within_ci': bool(significance['within_ci']),
                    'p_value': float(significance['p_value']),
                    'significant': bool(significance['significant']),
                    'bootstrap_mean': float(significance['bootstrap_mean']),
                    'bootstrap_std': float(significance['bootstrap_std'])
                }
            },
            'classical': {
                'chsh_value': float(S_classical),
                'best_weight': float(scan_classical['best_weight']),
                'max_nrci': float(scan_classical['max_nrci']),
                'coherence_pressure': float(psi_p_classical)
            },
            'ubp_constants': {
                'Y_emergent': Y_EMERGENT,
                'W_tetra_invariant': W_TETRA_INVARIANT,
                'PGCI_target': PGCI_TARGET
            }
        }
        
        with open('/home/ubuntu/ubp_analysis_results.json', 'w') as f:
            json.dump(results_dict, f, indent=2)
        
        print("\n10. Results saved to:")
        print("    - ubp_analysis_results.json")
        print("    - weight_scan_quantum.png")
        print("    - weight_scan_classical.png")
    
    print("\n" + "="*70)
    print("Analysis complete!")
    print("="*70)
    
    return {
        'quantum_data': quantum_data,
        'classical_data': classical_data,
        'scan_quantum': scan_results,
        'scan_classical': scan_classical,
        'significance': significance
    }

if __name__ == "__main__":
    results = run_complete_analysis(n_trials=100000)

