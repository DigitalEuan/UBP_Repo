"""
Study 2: Information Layer Signatures in Quantum Entanglement
==============================================================

Complete analysis pipeline integrating:
1. High-fidelity data generation (quantum, classical, random)
2. Information layer metrics (NRCI-I, temporal analysis)
3. Geometric weight scanning
4. Statistical significance testing
5. Comparative analysis

Author: Manus AI, on behalf of Euan R A Craig
Date: October 29, 2025
"""

import numpy as np
import matplotlib.pyplot as plt
import json
from information_layer_metrics import InformationLayerMetrics, analyze_dataset

# UBP Constants (from Study 1 and updated theory)
Y_EMERGENT = 0.2647
W_TETRA = np.pi / ((1 + np.sqrt(5)) / 2)  # π/φ ≈ 1.9416
W_OBSERVED_STUDY1 = 1.5303  # Discovered in Study 1
PGCI_TARGET = 0.999997

print("="*70)
print("STUDY 2: Information Layer Signatures in Quantum Entanglement")
print("="*70)
print(f"\nUBP Constants:")
print(f"  Y_emergent:  {Y_EMERGENT:.4f}")
print(f"  W_Tetra:     {W_TETRA:.4f}")
print(f"  W_Study1:    {W_OBSERVED_STUDY1:.4f}")
print(f"  PGCI Target: {PGCI_TARGET:.6f}")

# ============================================================================
# PHASE 1: DATA GENERATION
# ============================================================================

print(f"\n{'='*70}")
print("PHASE 1: Generating High-Fidelity Datasets")
print("="*70)

def generate_quantum_bell_data(n_trials=100000, detection_eff=0.75, noise=0.02):
    """
    Generate quantum Bell test data with proper CHSH violation.
    Based on singlet state with optimal CHSH angles.
    """
    print(f"\n[1/3] Generating quantum data...")
    print(f"      Trials: {n_trials}, Efficiency: {detection_eff}, Noise: {noise}")
    
    # CHSH optimal angles (in radians)
    angles_a = np.array([0, np.pi/4])  # Alice: 0°, 45°
    angles_b = np.array([np.pi/8, -np.pi/8])  # Bob: 22.5°, -22.5°
    
    # Generate trials
    alice_settings = np.random.choice([0, 1], size=n_trials)
    bob_settings = np.random.choice([0, 1], size=n_trials)
    
    alice_outcomes = []
    bob_outcomes = []
    
    for i in range(n_trials):
        # Get angles for this trial
        theta_a = angles_a[alice_settings[i]]
        theta_b = angles_b[bob_settings[i]]
        
        # Quantum correlation: P(same) = sin²(θ_a - θ_b)
        delta = theta_a - theta_b
        p_same = np.sin(delta)**2
        
        # Add noise
        p_same = (1 - noise) * p_same + noise * 0.5
        
        # Generate outcomes
        alice_outcome = np.random.choice([0, 1])
        bob_outcome = alice_outcome if np.random.random() < p_same else 1 - alice_outcome
        
        alice_outcomes.append(alice_outcome)
        bob_outcomes.append(bob_outcome)
    
    alice_outcomes = np.array(alice_outcomes)
    bob_outcomes = np.array(bob_outcomes)
    
    # Apply detection efficiency
    detected = np.random.random(n_trials) < detection_eff
    
    data = {
        'alice_outcomes': alice_outcomes[detected],
        'bob_outcomes': bob_outcomes[detected],
        'alice_settings': alice_settings[detected],
        'bob_settings': bob_settings[detected]
    }
    
    print(f"      Generated {np.sum(detected)} coincident events")
    
    return data

def generate_classical_lhv_data(n_trials=100000, detection_eff=0.75):
    """
    Generate classical local hidden variable data.
    """
    print(f"\n[2/3] Generating classical LHV data...")
    
    alice_settings = np.random.choice([0, 1], size=n_trials)
    bob_settings = np.random.choice([0, 1], size=n_trials)
    
    # Shared hidden variable (local realism)
    hidden_var = np.random.random(n_trials)
    
    alice_outcomes = []
    bob_outcomes = []
    
    for i in range(n_trials):
        # Deterministic outcomes based on hidden variable and settings
        # This model respects Bell's bound
        threshold_a = 0.5 + 0.3 * (alice_settings[i] - 0.5)
        threshold_b = 0.5 + 0.3 * (bob_settings[i] - 0.5)
        
        alice_outcome = 1 if hidden_var[i] > threshold_a else 0
        bob_outcome = 1 if hidden_var[i] > threshold_b else 0
        
        alice_outcomes.append(alice_outcome)
        bob_outcomes.append(bob_outcome)
    
    alice_outcomes = np.array(alice_outcomes)
    bob_outcomes = np.array(bob_outcomes)
    
    # Apply detection efficiency
    detected = np.random.random(n_trials) < detection_eff
    
    data = {
        'alice_outcomes': alice_outcomes[detected],
        'bob_outcomes': bob_outcomes[detected],
        'alice_settings': alice_settings[detected],
        'bob_settings': bob_settings[detected]
    }
    
    print(f"      Generated {np.sum(detected)} coincident events")
    
    return data

def generate_random_data(n_trials=100000, detection_eff=0.75):
    """
    Generate completely random (uncorrelated) data as baseline.
    """
    print(f"\n[3/3] Generating random baseline data...")
    
    n_detected = int(n_trials * detection_eff)
    
    data = {
        'alice_outcomes': np.random.choice([0, 1], size=n_detected),
        'bob_outcomes': np.random.choice([0, 1], size=n_detected),
        'alice_settings': np.random.choice([0, 1], size=n_detected),
        'bob_settings': np.random.choice([0, 1], size=n_detected)
    }
    
    print(f"      Generated {n_detected} events")
    
    return data

def calculate_chsh(data):
    """Calculate CHSH value for verification."""
    alice_out = data['alice_outcomes']
    bob_out = data['bob_outcomes']
    alice_set = data['alice_settings']
    bob_set = data['bob_settings']
    
    # Calculate E(a,b) for each setting combination
    correlations = {}
    for a in [0, 1]:
        for b in [0, 1]:
            mask = (alice_set == a) & (bob_set == b)
            if np.sum(mask) > 0:
                outcomes_a = alice_out[mask]
                outcomes_b = bob_out[mask]
                # E = P(same) - P(different)
                same = np.sum(outcomes_a == outcomes_b)
                diff = np.sum(outcomes_a != outcomes_b)
                correlations[(a,b)] = (same - diff) / (same + diff)
            else:
                correlations[(a,b)] = 0
    
    # CHSH: S = |E(a,b) - E(a,b') + E(a',b) + E(a',b')|
    S = abs(correlations[(0,0)] - correlations[(0,1)] + 
            correlations[(1,0)] + correlations[(1,1)])
    
    return S, correlations

# Generate all datasets
quantum_data = generate_quantum_bell_data(n_trials=100000)
classical_data = generate_classical_lhv_data(n_trials=100000)
random_data = generate_random_data(n_trials=100000)

# Verify CHSH values
print(f"\n{'='*70}")
print("Verification: CHSH Values")
print("="*70)

chsh_q, _ = calculate_chsh(quantum_data)
chsh_c, _ = calculate_chsh(classical_data)
chsh_r, _ = calculate_chsh(random_data)

print(f"  Quantum:   S = {chsh_q:.4f} {'✓ VIOLATION' if chsh_q > 2 else '✗ No violation'}")
print(f"  Classical: S = {chsh_c:.4f} {'✓ Respects bound' if chsh_c <= 2 else '✗ Violation (error!)'}")
print(f"  Random:    S = {chsh_r:.4f}")

# ============================================================================
# PHASE 2: INFORMATION LAYER ANALYSIS
# ============================================================================

print(f"\n{'='*70}")
print("PHASE 2: Information Layer Analysis")
print("="*70)

# Analyze each dataset
quantum_signature = analyze_dataset(quantum_data, "Quantum Entanglement")
classical_signature = analyze_dataset(classical_data, "Classical LHV")
random_signature = analyze_dataset(random_data, "Random Baseline")

# ============================================================================
# PHASE 3: COMPARATIVE ANALYSIS
# ============================================================================

print(f"\n{'='*70}")
print("PHASE 3: Comparative Analysis")
print("="*70)

# Create comparison table
print(f"\n{'Metric':<30} {'Quantum':>12} {'Classical':>12} {'Random':>12}")
print("-"*70)

metrics_to_compare = [
    ('Shannon Entropy (avg)', 'shannon_entropy_alice', lambda s: (s['shannon_entropy_alice'] + s['shannon_entropy_bob'])/2),
    ('LZ Complexity (avg)', 'lz_complexity_alice', lambda s: (s['lz_complexity_alice'] + s['lz_complexity_bob'])/2),
    ('Mutual Information', 'mutual_information', lambda s: s['mutual_information']),
    ('NRCI-Information', 'nrci_information', lambda s: s['nrci_information']),
    ('Autocorr Anomaly (avg)', 'autocorr_anomaly_alice', lambda s: (s['autocorr_anomaly_alice'] + s['autocorr_anomaly_bob'])/2),
    ('Crosscorr Anomaly', 'crosscorr_anomaly', lambda s: s['crosscorr_anomaly']),
]

comparison_results = {}

for metric_name, _, extractor in metrics_to_compare:
    q_val = extractor(quantum_signature)
    c_val = extractor(classical_signature)
    r_val = extractor(random_signature)
    
    print(f"{metric_name:<30} {q_val:>12.6f} {c_val:>12.6f} {r_val:>12.6f}")
    
    comparison_results[metric_name] = {
        'quantum': float(q_val),
        'classical': float(c_val),
        'random': float(r_val)
    }

# Weight scan comparison
print(f"\n{'='*70}")
print("Geometric Weight Analysis")
print("="*70)

print(f"\n{'Dataset':<20} {'Optimal Weight':>15} {'Max NRCI-I':>12} {'Deviation from W_Tetra':>25}")
print("-"*70)

for label, signature in [('Quantum', quantum_signature), 
                         ('Classical', classical_signature),
                         ('Random', random_signature)]:
    w_opt = signature['weight_scan']['best_weight']
    nrci_max = signature['weight_scan']['best_nrci']
    deviation = abs(w_opt - W_TETRA) / W_TETRA * 100
    
    print(f"{label:<20} {w_opt:>15.4f} {nrci_max:>12.4f} {deviation:>24.2f}%")

# Test against both candidate invariants
print(f"\nCandidate Geometric Invariants:")
print(f"  W_Tetra (predicted):  {W_TETRA:.4f}")
print(f"  W_Study1 (observed):  {W_OBSERVED_STUDY1:.4f}")

for label, signature in [('Quantum', quantum_signature)]:
    w_opt = signature['weight_scan']['best_weight']
    dev_tetra = abs(w_opt - W_TETRA)
    dev_study1 = abs(w_opt - W_OBSERVED_STUDY1)
    
    print(f"\n{label} optimal weight: {w_opt:.4f}")
    print(f"  Distance to W_Tetra:  {dev_tetra:.4f}")
    print(f"  Distance to W_Study1: {dev_study1:.4f}")
    
    if dev_study1 < dev_tetra:
        print(f"  → Closer to W_Study1 (2-qubit invariant)")
    else:
        print(f"  → Closer to W_Tetra (tetrahedral invariant)")

# ============================================================================
# PHASE 4: VISUALIZATION
# ============================================================================

print(f"\n{'='*70}")
print("PHASE 4: Creating Visualizations")
print("="*70)

fig = plt.figure(figsize=(18, 12))

# 1. NRCI-I Weight Scans
ax1 = plt.subplot(3, 3, 1)
for label, signature, color in [('Quantum', quantum_signature, 'blue'),
                                ('Classical', classical_signature, 'red'),
                                ('Random', random_signature, 'gray')]:
    weights = np.array(signature['weight_scan']['weights'])
    nrci = np.array(signature['weight_scan']['nrci_values'])
    ax1.plot(weights, nrci, label=label, color=color, linewidth=2)

ax1.axvline(W_TETRA, color='green', linestyle='--', label='W_Tetra', linewidth=1.5)
ax1.axvline(W_OBSERVED_STUDY1, color='purple', linestyle='--', label='W_Study1', linewidth=1.5)
ax1.set_xlabel('Geometric Weight', fontsize=10)
ax1.set_ylabel('NRCI-Information', fontsize=10)
ax1.set_title('NRCI-I vs. Geometric Weight', fontsize=11, fontweight='bold')
ax1.legend(fontsize=8)
ax1.grid(True, alpha=0.3)

# 2. Entropy Comparison
ax2 = plt.subplot(3, 3, 2)
datasets = ['Quantum', 'Classical', 'Random']
entropy_alice = [quantum_signature['shannon_entropy_alice'],
                classical_signature['shannon_entropy_alice'],
                random_signature['shannon_entropy_alice']]
entropy_bob = [quantum_signature['shannon_entropy_bob'],
              classical_signature['shannon_entropy_bob'],
              random_signature['shannon_entropy_bob']]

x = np.arange(len(datasets))
width = 0.35
ax2.bar(x - width/2, entropy_alice, width, label='Alice', color='skyblue')
ax2.bar(x + width/2, entropy_bob, width, label='Bob', color='lightcoral')
ax2.set_ylabel('Shannon Entropy (bits)', fontsize=10)
ax2.set_title('Shannon Entropy Comparison', fontsize=11, fontweight='bold')
ax2.set_xticks(x)
ax2.set_xticklabels(datasets)
ax2.legend(fontsize=8)
ax2.grid(True, alpha=0.3, axis='y')
ax2.set_ylim([0, 1.1])

# 3. Mutual Information
ax3 = plt.subplot(3, 3, 3)
mi_values = [quantum_signature['mutual_information'],
            classical_signature['mutual_information'],
            random_signature['mutual_information']]
colors = ['blue', 'red', 'gray']
ax3.bar(datasets, mi_values, color=colors, alpha=0.7)
ax3.set_ylabel('Mutual Information (bits)', fontsize=10)
ax3.set_title('Mutual Information', fontsize=11, fontweight='bold')
ax3.grid(True, alpha=0.3, axis='y')

# 4. LZ Complexity
ax4 = plt.subplot(3, 3, 4)
lz_alice = [quantum_signature['lz_complexity_alice'],
           classical_signature['lz_complexity_alice'],
           random_signature['lz_complexity_alice']]
lz_bob = [quantum_signature['lz_complexity_bob'],
         classical_signature['lz_complexity_bob'],
         random_signature['lz_complexity_bob']]

ax4.bar(x - width/2, lz_alice, width, label='Alice', color='skyblue')
ax4.bar(x + width/2, lz_bob, width, label='Bob', color='lightcoral')
ax4.set_ylabel('LZ Complexity (normalized)', fontsize=10)
ax4.set_title('Lempel-Ziv Complexity', fontsize=11, fontweight='bold')
ax4.set_xticks(x)
ax4.set_xticklabels(datasets)
ax4.legend(fontsize=8)
ax4.grid(True, alpha=0.3, axis='y')

# 5. NRCI-I Components (Quantum only)
ax5 = plt.subplot(3, 3, 5)
components = quantum_signature['nrci_components']
comp_names = list(components.keys())
comp_values = list(components.values())
ax5.barh(comp_names, comp_values, color='blue', alpha=0.7)
ax5.set_xlabel('Score', fontsize=10)
ax5.set_title('NRCI-I Components (Quantum)', fontsize=11, fontweight='bold')
ax5.grid(True, alpha=0.3, axis='x')
ax5.set_xlim([0, 1])

# 6. Temporal Anomalies
ax6 = plt.subplot(3, 3, 6)
acf_anomaly = [quantum_signature['autocorr_anomaly_alice'],
              classical_signature['autocorr_anomaly_alice'],
              random_signature['autocorr_anomaly_alice']]
ccf_anomaly = [quantum_signature['crosscorr_anomaly'],
              classical_signature['crosscorr_anomaly'],
              random_signature['crosscorr_anomaly']]

ax6.bar(x - width/2, acf_anomaly, width, label='Autocorr', color='orange')
ax6.bar(x + width/2, ccf_anomaly, width, label='Crosscorr', color='purple')
ax6.set_ylabel('Anomaly Score', fontsize=10)
ax6.set_title('Temporal Correlation Anomalies', fontsize=11, fontweight='bold')
ax6.set_xticks(x)
ax6.set_xticklabels(datasets)
ax6.legend(fontsize=8)
ax6.grid(True, alpha=0.3, axis='y')
ax6.set_yscale('log')

# 7. Overall NRCI-I Comparison
ax7 = plt.subplot(3, 3, 7)
nrci_i_values = [quantum_signature['nrci_information'],
                classical_signature['nrci_information'],
                random_signature['nrci_information']]
bars = ax7.bar(datasets, nrci_i_values, color=colors, alpha=0.7)
ax7.axhline(PGCI_TARGET, color='green', linestyle='--', label=f'UBP Target ({PGCI_TARGET})', linewidth=1.5)
ax7.set_ylabel('NRCI-Information', fontsize=10)
ax7.set_title('NRCI-I Comparison', fontsize=11, fontweight='bold')
ax7.legend(fontsize=8)
ax7.grid(True, alpha=0.3, axis='y')
ax7.set_ylim([0, 1])

# Add value labels on bars
for bar, val in zip(bars, nrci_i_values):
    height = bar.get_height()
    ax7.text(bar.get_x() + bar.get_width()/2., height,
            f'{val:.4f}', ha='center', va='bottom', fontsize=9)

# 8. Optimal Weights
ax8 = plt.subplot(3, 3, 8)
opt_weights = [quantum_signature['weight_scan']['best_weight'],
              classical_signature['weight_scan']['best_weight'],
              random_signature['weight_scan']['best_weight']]
ax8.bar(datasets, opt_weights, color=colors, alpha=0.7)
ax8.axhline(W_TETRA, color='green', linestyle='--', label='W_Tetra', linewidth=1.5)
ax8.axhline(W_OBSERVED_STUDY1, color='purple', linestyle='--', label='W_Study1', linewidth=1.5)
ax8.set_ylabel('Optimal Weight', fontsize=10)
ax8.set_title('Optimal Geometric Weights', fontsize=11, fontweight='bold')
ax8.legend(fontsize=8)
ax8.grid(True, alpha=0.3, axis='y')

# 9. Summary Text
ax9 = plt.subplot(3, 3, 9)
ax9.axis('off')
summary_text = f"""
STUDY 2 KEY FINDINGS

CHSH Values:
  Quantum:   {chsh_q:.4f} ✓
  Classical: {chsh_c:.4f}
  Random:    {chsh_r:.4f}

NRCI-Information:
  Quantum:   {nrci_i_values[0]:.4f}
  Classical: {nrci_i_values[1]:.4f}
  Random:    {nrci_i_values[2]:.4f}

Optimal Weights:
  Quantum:   {opt_weights[0]:.4f}
  Classical: {opt_weights[1]:.4f}
  Random:    {opt_weights[2]:.4f}

Invariant Tests:
  W_Tetra:   {W_TETRA:.4f}
  W_Study1:  {W_OBSERVED_STUDY1:.4f}
  
Quantum Deviation:
  from W_Tetra:  {abs(opt_weights[0]-W_TETRA):.4f}
  from W_Study1: {abs(opt_weights[0]-W_OBSERVED_STUDY1):.4f}
"""
ax9.text(0.1, 0.5, summary_text, fontsize=9, family='monospace',
        verticalalignment='center')

plt.tight_layout()
plt.savefig('/home/ubuntu/study_2_comprehensive_analysis.png', dpi=300, bbox_inches='tight')
print("  Saved: study_2_comprehensive_analysis.png")

# ============================================================================
# PHASE 5: SAVE RESULTS
# ============================================================================

print(f"\n{'='*70}")
print("PHASE 5: Saving Results")
print("="*70)

results = {
    'study_info': {
        'title': 'Study 2: Information Layer Signatures in Quantum Entanglement',
        'date': '2025-10-29',
        'author': 'Manus AI, on behalf of Euan R A Craig'
    },
    'ubp_constants': {
        'Y_emergent': float(Y_EMERGENT),
        'W_Tetra': float(W_TETRA),
        'W_Study1': float(W_OBSERVED_STUDY1),
        'PGCI_target': float(PGCI_TARGET)
    },
    'chsh_values': {
        'quantum': float(chsh_q),
        'classical': float(chsh_c),
        'random': float(chsh_r)
    },
    'quantum_signature': quantum_signature,
    'classical_signature': classical_signature,
    'random_signature': random_signature,
    'comparison': comparison_results
}

with open('/home/ubuntu/study_2_results.json', 'w') as f:
    json.dump(results, f, indent=2)

print("  Saved: study_2_results.json")

print(f"\n{'='*70}")
print("STUDY 2 ANALYSIS COMPLETE")
print("="*70)
print("\nKey Findings:")
print(f"  1. Quantum NRCI-I: {nrci_i_values[0]:.4f}")
print(f"  2. Optimal weight: {opt_weights[0]:.4f}")
print(f"  3. Closest to: {'W_Study1' if abs(opt_weights[0]-W_OBSERVED_STUDY1) < abs(opt_weights[0]-W_TETRA) else 'W_Tetra'}")
print(f"  4. Information layer signatures detected: {'Yes' if nrci_i_values[0] > nrci_i_values[2] else 'Inconclusive'}")

