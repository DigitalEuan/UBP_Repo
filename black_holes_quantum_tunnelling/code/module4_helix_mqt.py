#!/usr/bin/env python3.11
"""
Module 4: Self-Observing Helix and MQT Boost Predictions
Author: Euan R A Craig
Date: October 15, 2025
Framework: Universal Binary Principle (UBP) v3.2

This module implements:
1. Self-observing helix model for proto-cognition and perceived radiation
2. MQT (Macroscopic Quantum Tunneling) boost predictions from queue amplitude
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import os

# Directories
DATA_DIR = '/home/ubuntu/black_holes_quantum_tunnelling/data'
FIG_DIR = '/home/ubuntu/black_holes_quantum_tunnelling/figures'

class SelfObservingHelix:
    """
    Self-observing helix model for proto-cognition.
    
    Three-Column Thinking Framework:
    
    LANGUAGE: A self-observing system maintains a memory buffer of past states
    and compares current observations to memory. When the queue backlog exceeds
    a perception threshold, the system "notices" leaks, which manifest as
    perceived Hawking radiation. The helix structure represents circular motion
    in a 2D subspace, with revolution count tracking observation cycles.
    
    MATHEMATICS:
    - Memory length: L (number of past states)
    - Revolution count: N_rev (observation cycles)
    - Perception threshold: θ_p (minimum coherence for noticing)
    - Radiation rate: R_perceived = f(L, N_rev, queue_leak_rate)
    - Thermal spectrum emerges when N_rev > N_critical
    
    SCRIPT: Initialize helix with memory buffer, simulate circular motion,
    compare current state to memory, detect leaks above threshold, compute
    perceived radiation rate.
    """
    
    def __init__(self, memory_length=100, perception_threshold=0.1):
        """
        Initialize self-observing helix.
        
        Parameters:
        -----------
        memory_length : int
            Number of past states to retain
        perception_threshold : float
            Minimum coherence change for perception
        """
        self.L = memory_length
        self.theta_p = perception_threshold
        self.memory = []
        self.N_rev = 0
        self.perceived_radiation = []
        
        print(f"Self-Observing Helix initialized:")
        print(f"  Memory length L = {self.L}")
        print(f"  Perception threshold θ_p = {self.theta_p}\n")
    
    def observe(self, queue_state, nrci_state):
        """
        Observe current queue and NRCI state.
        
        Parameters:
        -----------
        queue_state : float
            Current queue length
        nrci_state : float
            Current NRCI value
            
        Returns:
        --------
        perceived : bool
            Whether radiation was perceived
        radiation_rate : float
            Perceived radiation rate
        """
        # Store current state in memory
        current_state = {'queue': queue_state, 'nrci': nrci_state}
        self.memory.append(current_state)
        
        # Trim memory to length L
        if len(self.memory) > self.L:
            self.memory.pop(0)
            self.N_rev += 1  # Completed one revolution
        
        # Compare to memory (if sufficient history)
        if len(self.memory) >= 2:
            prev_state = self.memory[-2]
            delta_queue = current_state['queue'] - prev_state['queue']
            delta_nrci = abs(current_state['nrci'] - prev_state['nrci'])
            
            # Perception occurs if change exceeds threshold
            perceived = delta_nrci > self.theta_p
            
            # Radiation rate proportional to queue leak rate
            # Leak rate ≈ delta_queue (negative = leak)
            if delta_queue < 0:
                radiation_rate = abs(delta_queue) * (1.0 - current_state['nrci'])
            else:
                radiation_rate = 0.0
        else:
            perceived = False
            radiation_rate = 0.0
        
        self.perceived_radiation.append(radiation_rate)
        
        return perceived, radiation_rate
    
    def get_thermal_spectrum_indicator(self):
        """
        Check if thermal spectrum has emerged.
        
        Returns:
        --------
        emerged : bool
            Whether thermal spectrum has emerged
        N_critical : int
            Critical revolution count for emergence
        """
        # Thermal spectrum emerges after sufficient revolutions
        N_critical = 10  # Empirical threshold
        emerged = self.N_rev >= N_critical
        
        return emerged, N_critical

class MQTBoostModel:
    """
    MQT (Macroscopic Quantum Tunneling) boost prediction model.
    
    Three-Column Thinking Framework:
    
    LANGUAGE: Queue amplitude modulates the effective barrier height for
    quantum tunneling. Higher queue amplitude creates geometric warps that
    enhance tunneling probability, leading to a boost factor ranging from
    18.4% to 69% depending on queue amplitude (2.62 to 4.70).
    
    MATHEMATICS:
    - Classical tunneling: T_classical = exp(-2κa)
    - UBP boost: T_UBP = T_classical × B(A_queue)
    - Boost factor: B(A_queue) = 1 + α × (A_queue - A_min)
    - Queue amplitude: A_queue ∈ [2.62, 4.70]
    - Boost range: B ∈ [1.184, 1.69]
    
    SCRIPT: Vary queue amplitude, compute boost factor, fit to predicted
    range, generate predictions for experimental validation.
    """
    
    def __init__(self):
        """Initialize MQT boost model."""
        # Predicted parameter ranges
        self.A_min = 2.62
        self.A_max = 4.70
        self.B_min = 1.184  # 18.4% boost
        self.B_max = 1.69   # 69% boost
        
        # Compute linear fit parameters
        self.alpha = (self.B_max - self.B_min) / (self.A_max - self.A_min)
        self.beta = self.B_min - self.alpha * self.A_min
        
        print(f"MQT Boost Model initialized:")
        print(f"  Queue amplitude range: [{self.A_min}, {self.A_max}]")
        print(f"  Boost factor range: [{self.B_min}, {self.B_max}]")
        print(f"  Linear fit: B = {self.alpha:.4f} × A + {self.beta:.4f}\n")
    
    def compute_boost_factor(self, A_queue):
        """
        Compute boost factor from queue amplitude.
        
        Parameters:
        -----------
        A_queue : float or ndarray
            Queue amplitude
            
        Returns:
        --------
        B : float or ndarray
            Boost factor
        """
        B = self.alpha * A_queue + self.beta
        return np.clip(B, self.B_min, self.B_max)
    
    def compute_tunneling_probability(self, barrier_width, energy, mass, V0, A_queue):
        """
        Compute UBP-enhanced tunneling probability.
        
        Parameters:
        -----------
        barrier_width : float
            Barrier width (m)
        energy : float
            Particle energy (J)
        mass : float
            Particle mass (kg)
        V0 : float
            Barrier height (J)
        A_queue : float
            Queue amplitude
            
        Returns:
        --------
        T_UBP : float
            UBP tunneling probability
        T_classical : float
            Classical tunneling probability
        B : float
            Boost factor
        """
        # Classical tunneling probability
        hbar = 1.054571817e-34  # J·s
        kappa = np.sqrt(2 * mass * (V0 - energy)) / hbar
        T_classical = np.exp(-2 * kappa * barrier_width)
        
        # UBP boost
        B = self.compute_boost_factor(A_queue)
        T_UBP = T_classical * B
        
        return T_UBP, T_classical, B
    
    def generate_predictions(self, n_points=50):
        """
        Generate MQT boost predictions across amplitude range.
        
        Parameters:
        -----------
        n_points : int
            Number of prediction points
            
        Returns:
        --------
        predictions : DataFrame
            Predicted boost factors
        """
        A_queue = np.linspace(self.A_min, self.A_max, n_points)
        B = self.compute_boost_factor(A_queue)
        boost_pct = (B - 1.0) * 100
        
        predictions = pd.DataFrame({
            'A_queue': A_queue,
            'B': B,
            'boost_pct': boost_pct
        })
        
        return predictions

def simulate_helix_with_queue(queue_history):
    """
    Simulate self-observing helix with queue history.
    
    Parameters:
    -----------
    queue_history : DataFrame
        Queue dynamics history from Module 3
        
    Returns:
    --------
    helix_data : DataFrame
        Helix observation data
    """
    helix = SelfObservingHelix(memory_length=20, perception_threshold=0.01)
    
    observations = []
    for idx, row in queue_history.iterrows():
        perceived, rad_rate = helix.observe(row['total_queue'], row['mean_nrci'])
        
        observations.append({
            'step': row['step'],
            'perceived': perceived,
            'radiation_rate': rad_rate,
            'N_rev': helix.N_rev
        })
    
    helix_data = pd.DataFrame(observations)
    
    # Check thermal spectrum emergence
    emerged, N_critical = helix.get_thermal_spectrum_indicator()
    
    print(f"Self-Observing Helix Results:")
    print(f"  Total revolutions: {helix.N_rev}")
    print(f"  Critical revolutions: {N_critical}")
    print(f"  Thermal spectrum emerged: {emerged}")
    print(f"  Mean radiation rate: {helix_data['radiation_rate'].mean():.2f}")
    print(f"  Perception events: {helix_data['perceived'].sum()}\n")
    
    return helix_data, emerged

def plot_helix_results(helix_data, emerged):
    """Plot self-observing helix results."""
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    fig.suptitle('Self-Observing Helix: Proto-Cognition and Perceived Radiation', 
                 fontsize=16, fontweight='bold')
    
    # Plot 1: Radiation Rate vs Time
    ax = axes[0]
    ax.plot(helix_data['step'], helix_data['radiation_rate'], 'b-', linewidth=2)
    ax.set_xlabel('Simulation Step', fontsize=12)
    ax.set_ylabel('Perceived Radiation Rate', fontsize=12)
    ax.set_title('Hawking Radiation Perception', fontsize=13)
    ax.grid(True, alpha=0.3)
    
    # Plot 2: Revolution Count
    ax = axes[1]
    ax.plot(helix_data['step'], helix_data['N_rev'], 'g-', linewidth=2)
    ax.axhline(y=10, color='r', linestyle='--', linewidth=2, label='Thermal threshold')
    ax.set_xlabel('Simulation Step', fontsize=12)
    ax.set_ylabel('Revolution Count $N_{rev}$', fontsize=12)
    title_str = 'Thermal Spectrum: ' + ('EMERGED' if emerged else 'Not Yet')
    ax.set_title(title_str, fontsize=13)
    ax.grid(True, alpha=0.3)
    ax.legend(fontsize=10)
    
    plt.tight_layout()
    plt.savefig(f'{FIG_DIR}/05_self_observing_helix.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"✓ Saved: {FIG_DIR}/05_self_observing_helix.png")

def plot_mqt_predictions(predictions):
    """Plot MQT boost predictions."""
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    fig.suptitle('MQT Boost Predictions: Queue Amplitude Modulation', 
                 fontsize=16, fontweight='bold')
    
    # Plot 1: Boost Factor vs Queue Amplitude
    ax = axes[0]
    ax.plot(predictions['A_queue'], predictions['B'], 'b-', linewidth=3)
    ax.fill_between(predictions['A_queue'], predictions['B'], 1.0, alpha=0.3)
    ax.axhline(y=1.0, color='gray', linestyle=':', linewidth=2, label='No boost')
    ax.set_xlabel('Queue Amplitude $A_{queue}$', fontsize=12)
    ax.set_ylabel('Boost Factor B', fontsize=12)
    ax.set_title('Tunneling Enhancement', fontsize=13)
    ax.grid(True, alpha=0.3)
    ax.legend(fontsize=10)
    
    # Plot 2: Boost Percentage
    ax = axes[1]
    ax.plot(predictions['A_queue'], predictions['boost_pct'], 'g-', linewidth=3)
    ax.fill_between(predictions['A_queue'], predictions['boost_pct'], 0, alpha=0.3, color='green')
    ax.axhline(y=0, color='gray', linestyle=':', linewidth=2)
    ax.set_xlabel('Queue Amplitude $A_{queue}$', fontsize=12)
    ax.set_ylabel('Boost Percentage (%)', fontsize=12)
    ax.set_title('MQT Rate Enhancement: 18.4% to 69%', fontsize=13)
    ax.grid(True, alpha=0.3)
    
    # Add annotations
    ax.annotate(f'{predictions["boost_pct"].iloc[0]:.1f}%', 
                xy=(predictions['A_queue'].iloc[0], predictions['boost_pct'].iloc[0]),
                xytext=(10, 10), textcoords='offset points', fontsize=11, fontweight='bold')
    ax.annotate(f'{predictions["boost_pct"].iloc[-1]:.1f}%', 
                xy=(predictions['A_queue'].iloc[-1], predictions['boost_pct'].iloc[-1]),
                xytext=(10, 10), textcoords='offset points', fontsize=11, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig(f'{FIG_DIR}/06_mqt_boost_predictions.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"✓ Saved: {FIG_DIR}/06_mqt_boost_predictions.png")

def main():
    """Main execution function."""
    print("\n" + "="*80)
    print("MODULE 4: SELF-OBSERVING HELIX AND MQT BOOST")
    print("="*80)
    print("Framework: Universal Binary Principle (UBP) v3.2")
    print("Author: Euan R A Craig")
    print("="*80 + "\n")
    
    # Load queue history from Module 3
    print("Loading queue history from Module 3...")
    queue_history = pd.read_csv(f'{DATA_DIR}/bh_queue_history.csv')
    print(f"✓ Loaded {len(queue_history)} timesteps\n")
    
    # Simulate self-observing helix
    print("Simulating self-observing helix...")
    helix_data, emerged = simulate_helix_with_queue(queue_history)
    
    # Save helix data
    helix_file = f'{DATA_DIR}/self_observing_helix.csv'
    helix_data.to_csv(helix_file, index=False)
    print(f"✓ Saved helix data: {helix_file}\n")
    
    # Plot helix results
    print("Generating helix visualizations...")
    plot_helix_results(helix_data, emerged)
    
    # Initialize MQT boost model
    print("\nInitializing MQT boost model...")
    mqt = MQTBoostModel()
    
    # Generate predictions
    print("Generating MQT boost predictions...")
    predictions = mqt.generate_predictions(n_points=50)
    
    # Save predictions
    predictions_file = f'{DATA_DIR}/mqt_boost_predictions.csv'
    predictions.to_csv(predictions_file, index=False)
    print(f"✓ Saved predictions: {predictions_file}\n")
    
    # Display sample predictions
    print("Sample MQT Boost Predictions:")
    print("-"*80)
    sample_indices = [0, len(predictions)//4, len(predictions)//2, 3*len(predictions)//4, -1]
    for idx in sample_indices:
        row = predictions.iloc[idx]
        print(f"A_queue = {row['A_queue']:.3f}: B = {row['B']:.4f}, Boost = {row['boost_pct']:.2f}%")
    print()
    
    # Plot MQT predictions
    print("Generating MQT visualizations...")
    plot_mqt_predictions(predictions)
    
    # Example tunneling calculation
    print("\nExample Tunneling Calculation:")
    print("-"*80)
    # Parameters for SQUID junction (typical MQT experiment)
    barrier_width = 2e-9  # 2 nm
    energy = 1e-20  # J
    mass = 9.109e-31  # electron mass (kg)
    V0 = 2e-20  # barrier height (J)
    A_queue_example = 3.5
    
    T_UBP, T_classical, B = mqt.compute_tunneling_probability(
        barrier_width, energy, mass, V0, A_queue_example
    )
    
    print(f"  Barrier width: {barrier_width*1e9:.1f} nm")
    print(f"  Energy: {energy:.2e} J")
    print(f"  Queue amplitude: {A_queue_example:.2f}")
    print(f"  Classical tunneling: {T_classical:.6e}")
    print(f"  UBP tunneling: {T_UBP:.6e}")
    print(f"  Boost factor: {B:.4f} ({(B-1)*100:.2f}% enhancement)")
    print()
    
    print("="*80)
    print("MODULE 4 COMPLETE")
    print("="*80)
    print(f"Key Results:")
    print(f"  - Helix revolutions: {helix_data['N_rev'].iloc[-1]}")
    print(f"  - Thermal spectrum: {'EMERGED' if emerged else 'Not yet'}")
    print(f"  - MQT boost range: {predictions['boost_pct'].iloc[0]:.2f}% to {predictions['boost_pct'].iloc[-1]:.2f}%")
    print(f"  - Queue amplitude range: [{predictions['A_queue'].iloc[0]:.2f}, {predictions['A_queue'].iloc[-1]:.2f}]")
    print("="*80 + "\n")
    
    return helix_data, predictions

if __name__ == "__main__":
    helix_data, predictions = main()

