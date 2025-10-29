#!/usr/bin/env python3.11
"""
Proper Quantum Bell Test Data Generator

Generates data that correctly violates the CHSH inequality according to
quantum mechanical predictions for the singlet state.
"""

import numpy as np
import json

def generate_proper_bell_data(n_trials=100000, detection_eff=0.75, noise=0.02):
    """
    Generate Bell test data with proper quantum correlations.
    
    For the singlet state |ψ⟩ = (|↑↓⟩ - |↓↑⟩)/√2 and polarization measurements:
    
    Correlation: E(a,b) = -cos(2(θ_a - θ_b))
    
    CHSH optimal angles:
    - Alice: a0 = 0°, a1 = 45°
    - Bob: b0 = 22.5°, b1 = -22.5° (or 67.5°)
    
    This gives: S = E(a0,b0) + E(a0,b1) + E(a1,b0) - E(a1,b1) = 2√2 ≈ 2.828
    """
    
    # CHSH optimal angles (in radians)
    alice_angles = np.array([0, np.pi/4])  # 0°, 45°
    bob_angles = np.array([np.pi/8, -np.pi/8])  # 22.5°, -22.5°
    
    data = {
        'alice_outcomes': [],
        'bob_outcomes': [],
        'alice_settings': [],
        'bob_settings': []
    }
    
    for _ in range(n_trials):
        # Random settings
        a_idx = np.random.randint(0, 2)
        b_idx = np.random.randint(0, 2)
        
        theta_a = alice_angles[a_idx]
        theta_b = bob_angles[b_idx]
        
        # Angle difference
        delta = theta_a - theta_b
        
        # For singlet state, correlation is E(a,b) = -cos(2δ)
        # This means: P(same) = sin²(δ), P(different) = cos²(δ)
        
        # Generate Alice's outcome randomly
        alice_result = np.random.choice([0, 1])
        
        # Bob's outcome is correlated according to QM
        # P(Bob = Alice) = sin²(δ)
        prob_same = np.sin(delta)**2
        
        # Add noise
        prob_same = prob_same * (1 - noise) + 0.5 * noise
        
        if np.random.rand() < prob_same:
            bob_result = alice_result
        else:
            bob_result = 1 - alice_result
        
        # Apply detection efficiency
        if np.random.rand() < detection_eff and np.random.rand() < detection_eff:
            data['alice_outcomes'].append(alice_result)
            data['bob_outcomes'].append(bob_result)
            data['alice_settings'].append(a_idx)
            data['bob_settings'].append(b_idx)
    
    # Convert to arrays
    for key in data:
        data[key] = np.array(data[key])
    
    return data

def calculate_chsh(data):
    """Calculate CHSH value."""
    
    # Calculate E(a,b) for each setting combination
    E = {}
    
    for a in [0, 1]:
        for b in [0, 1]:
            mask = (data['alice_settings'] == a) & (data['bob_settings'] == b)
            
            if np.sum(mask) > 0:
                # Convert to ±1
                A = 2 * data['alice_outcomes'][mask] - 1
                B = 2 * data['bob_outcomes'][mask] - 1
                
                # Correlation
                E[(a,b)] = np.mean(A * B)
            else:
                E[(a,b)] = 0
    
    # CHSH combination
    S = E[(0,0)] + E[(0,1)] + E[(1,0)] - E[(1,1)]
    
    return S, E

# Test the generator
if __name__ == "__main__":
    print("Testing quantum Bell data generator...")
    print("="*60)
    
    data = generate_proper_bell_data(n_trials=100000)
    
    print(f"Generated {len(data['alice_outcomes'])} coincident events")
    print(f"Detection efficiency: {len(data['alice_outcomes'])/100000:.3f}")
    
    S, correlations = calculate_chsh(data)
    
    print(f"\nCHSH value: S = {S:.4f}")
    print(f"Quantum prediction: S_max = {2*np.sqrt(2):.4f}")
    print(f"Classical bound: S ≤ 2.000")
    print(f"Violation: {S > 2}")
    
    print(f"\nIndividual correlations:")
    for key, val in correlations.items():
        print(f"  E{key} = {val:.4f}")
    
    # Save data
    data_to_save = {k: v.tolist() for k, v in data.items()}
    with open('/home/ubuntu/proper_bell_data.json', 'w') as f:
        json.dump(data_to_save, f)
    
    print(f"\nData saved to proper_bell_data.json")

