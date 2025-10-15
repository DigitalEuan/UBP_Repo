#!/usr/bin/env python3.11
"""
Module 3: 6D Bitfield Black Hole Queue Model
Author: Euan R A Craig
Date: October 15, 2025
Framework: Universal Binary Principle (UBP) v3.2

This module implements a 6D bitfield simulation of a black hole as an information
backlog queue. When influx exceeds processing capacity, NRCI saturates (< 0.01),
defining the computational event horizon.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.spatial.distance import cdist
from scipy.stats import norm
import os

# Directories
DATA_DIR = '/home/ubuntu/black_holes_quantum_tunnelling/data'
FIG_DIR = '/home/ubuntu/black_holes_quantum_tunnelling/figures'

class OffBit:
    """
    24-bit OffBit structure (padded to 32-bit).
    
    Ontological layers:
    - Reality (bits 0-5): Physical phenomena
    - Information (bits 6-11): Data and patterns
    - Activation (bits 12-17): Energy and processes
    - Unactivated (bits 18-23): Potential states
    """
    
    def __init__(self, state=0):
        """Initialize OffBit with 24-bit state (padded to 32-bit)."""
        self.state = np.uint32(state & 0xFFFFFF)  # Mask to 24 bits
    
    def get_layer(self, layer):
        """Extract 6-bit layer (0-3)."""
        return (self.state >> (layer * 6)) & 0x3F
    
    def set_layer(self, layer, value):
        """Set 6-bit layer (0-3)."""
        mask = ~(0x3F << (layer * 6))
        self.state = (self.state & mask) | ((value & 0x3F) << (layer * 6))
    
    def toggle(self, bit_index):
        """Toggle specific bit."""
        self.state ^= (1 << bit_index)
    
    def hamming_weight(self):
        """Count number of 1 bits (Hamming weight)."""
        return bin(self.state).count('1')
    
    def is_even_parity(self):
        """Check if Hamming weight is even."""
        return self.hamming_weight() % 2 == 0

class Bitfield6D:
    """
    6D Bitfield for black hole queue simulation.
    
    Three-Column Thinking Framework:
    
    LANGUAGE: The bitfield is a 6D computational substrate where OffBits reside.
    A black hole forms when information influx overwhelms processing capacity,
    creating a backlog queue. The event horizon is the boundary where coherence
    collapses (NRCI < 0.01), and information becomes "trapped" in the queue.
    
    MATHEMATICS:
    - Grid: 170 × 170 × 170 × 5 × 2 × 2 (reduced for computation: 50×50×50×3×2×2)
    - Influx rate: I = 10,000 OffBits/step
    - Processing capacity: P = P_max × NRCI
    - Queue: Q(t+1) = Q(t) + I - P(t)
    - NRCI: Non-Random Coherence Index ∈ [0, 1]
    - Horizon: r_h where NRCI(r_h) = 0.01
    
    SCRIPT: Initialize grid, place BH at center, inject OffBits at influx rate,
    compute local NRCI, process queue, track saturation, identify horizon.
    """
    
    def __init__(self, shape=(50, 50, 50, 3, 2, 2)):
        """
        Initialize 6D bitfield.
        
        Parameters:
        -----------
        shape : tuple
            6D grid dimensions (reduced from 170^3 for computational efficiency)
        """
        self.shape = shape
        self.n_cells = np.prod(shape)
        
        # Initialize OffBit states (random initial configuration)
        self.offbits = np.random.randint(0, 2**24, size=shape, dtype=np.uint32)
        
        # Queue length at each cell
        self.queue = np.zeros(shape, dtype=np.float64)
        
        # NRCI at each cell (start at high coherence)
        self.nrci = np.ones(shape, dtype=np.float64)
        
        # Center of grid (BH location)
        self.center = tuple(s // 2 for s in shape)
        
        print(f"Initialized 6D Bitfield:")
        print(f"  Shape: {shape}")
        print(f"  Total cells: {self.n_cells:,}")
        print(f"  BH center: {self.center}")
        print(f"  Memory: ~{self.n_cells * 4 * 3 / 1e6:.1f} MB\n")
    
    def compute_distance_from_center(self):
        """Compute Euclidean distance of each cell from BH center."""
        indices = np.indices(self.shape)
        distances = np.zeros(self.shape)
        
        for i, (idx, c) in enumerate(zip(indices, self.center)):
            distances += (idx - c)**2
        
        return np.sqrt(distances)
    
    def compute_local_nrci(self, distances, queue):
        """
        Compute Non-Random Coherence Index based on queue backlog.
        
        NRCI decreases as queue builds up, modeling loss of coherence.
        
        Parameters:
        -----------
        distances : ndarray
            Distance from BH center
        queue : ndarray
            Queue length at each cell
            
        Returns:
        --------
        nrci : ndarray
            NRCI values ∈ [0, 1]
        """
        # NRCI decay function: exponential decay with queue length
        # NRCI = exp(-queue / Q_critical)
        Q_critical = 1000.0  # Critical queue length for NRCI collapse
        
        nrci = np.exp(-queue / Q_critical)
        
        # Additional distance-based modulation (closer to BH → lower NRCI)
        r_horizon = 10.0  # Approximate horizon radius in grid units
        distance_factor = 1.0 / (1.0 + np.exp(-2 * (distances - r_horizon)))
        
        nrci *= distance_factor
        
        # Clamp to [0, 1]
        nrci = np.clip(nrci, 0.0, 1.0)
        
        return nrci
    
    def simulate_queue_dynamics(self, n_steps=100, influx_rate=10000, P_max=8000):
        """
        Simulate black hole queue dynamics over time.
        
        Parameters:
        -----------
        n_steps : int
            Number of simulation steps
        influx_rate : float
            OffBits influx per step
        P_max : float
            Maximum processing capacity per step
            
        Returns:
        --------
        history : dict
            Time series of queue, NRCI, horizon radius
        """
        distances = self.compute_distance_from_center()
        
        # History tracking
        history = {
            'step': [],
            'total_queue': [],
            'mean_nrci': [],
            'min_nrci': [],
            'horizon_radius': [],
            'leaked_offbits': []
        }
        
        print(f"Simulating queue dynamics:")
        print(f"  Steps: {n_steps}")
        print(f"  Influx rate: {influx_rate:,} OffBits/step")
        print(f"  Max processing: {P_max:,} OffBits/step")
        print(f"  Net accumulation: {influx_rate - P_max:,} OffBits/step\n")
        
        for step in range(n_steps):
            # Inject OffBits near center (Gaussian distribution)
            injection_mask = np.exp(-distances**2 / (2 * 5**2))  # σ = 5 grid units
            injection_mask /= injection_mask.sum()
            self.queue += influx_rate * injection_mask
            
            # Compute NRCI
            self.nrci = self.compute_local_nrci(distances, self.queue)
            
            # Processing capacity depends on NRCI
            processing = P_max * self.nrci
            
            # Process queue (remove processed OffBits)
            processed = np.minimum(self.queue, processing)
            self.queue -= processed
            
            # Stochastic leakage (Hawking radiation proxy)
            # Leak probability ∝ queue length × (1 - NRCI)
            leak_prob = 0.001 * self.queue * (1.0 - self.nrci)
            leaked = np.random.poisson(leak_prob)
            self.queue = np.maximum(0, self.queue - leaked)
            
            # Find horizon radius (where NRCI < 0.01)
            horizon_mask = self.nrci < 0.01
            if horizon_mask.any():
                horizon_distances = distances[horizon_mask]
                horizon_radius = horizon_distances.min()
            else:
                horizon_radius = 0.0
            
            # Record history
            history['step'].append(step)
            history['total_queue'].append(self.queue.sum())
            history['mean_nrci'].append(self.nrci.mean())
            history['min_nrci'].append(self.nrci.min())
            history['horizon_radius'].append(horizon_radius)
            history['leaked_offbits'].append(leaked.sum())
            
            if step % 20 == 0:
                print(f"  Step {step:3d}: Queue = {self.queue.sum():12,.0f}, "
                      f"NRCI_mean = {self.nrci.mean():.6f}, "
                      f"NRCI_min = {self.nrci.min():.6f}, "
                      f"r_h = {horizon_radius:.2f}")
        
        print(f"\n✓ Simulation complete\n")
        
        return history
    
    def compute_golay_parity_statistics(self, n_samples=10000):
        """
        Compute Golay code parity statistics for escaped OffBits.
        
        Returns:
        --------
        stats : dict
            Parity statistics
        """
        # Sample OffBits from low-NRCI regions (near horizon)
        low_nrci_mask = self.nrci < 0.1
        if not low_nrci_mask.any():
            print("⚠ No low-NRCI regions found for parity analysis")
            return None
        
        low_nrci_offbits = self.offbits[low_nrci_mask]
        
        # Sample subset
        if len(low_nrci_offbits) > n_samples:
            sampled = np.random.choice(low_nrci_offbits, size=n_samples, replace=False)
        else:
            sampled = low_nrci_offbits
        
        # Compute Hamming weights
        hamming_weights = np.array([bin(x).count('1') for x in sampled])
        
        # Parity statistics
        even_parity = (hamming_weights % 2 == 0)
        even_pct = even_parity.mean() * 100
        
        stats = {
            'n_samples': len(sampled),
            'mean_hamming_weight': hamming_weights.mean(),
            'std_hamming_weight': hamming_weights.std(),
            'even_parity_pct': even_pct,
            'variance': hamming_weights.var(),
            'expected_even_pct': 50.0,
            'parity_bias': even_pct - 50.0
        }
        
        return stats, hamming_weights

def plot_queue_dynamics(history):
    """Plot queue dynamics time series."""
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle('6D Bitfield Black Hole Queue Dynamics', fontsize=16, fontweight='bold')
    
    steps = history['step']
    
    # Plot 1: Total Queue Length
    ax = axes[0, 0]
    ax.plot(steps, history['total_queue'], 'b-', linewidth=2)
    ax.set_xlabel('Simulation Step', fontsize=12)
    ax.set_ylabel('Total Queue Length (OffBits)', fontsize=12)
    ax.set_title('Information Backlog Growth', fontsize=13)
    ax.grid(True, alpha=0.3)
    ax.ticklabel_format(style='scientific', axis='y', scilimits=(0,0))
    
    # Plot 2: Mean NRCI
    ax = axes[0, 1]
    ax.plot(steps, history['mean_nrci'], 'g-', linewidth=2, label='Mean NRCI')
    ax.plot(steps, history['min_nrci'], 'r--', linewidth=2, label='Min NRCI')
    ax.axhline(y=0.01, color='orange', linestyle=':', linewidth=2, label='Horizon threshold')
    ax.set_xlabel('Simulation Step', fontsize=12)
    ax.set_ylabel('NRCI', fontsize=12)
    ax.set_title('Coherence Collapse', fontsize=13)
    ax.set_ylim([0, 1.1])
    ax.grid(True, alpha=0.3)
    ax.legend(fontsize=10)
    
    # Plot 3: Horizon Radius
    ax = axes[1, 0]
    ax.plot(steps, history['horizon_radius'], 'm-', linewidth=2)
    ax.set_xlabel('Simulation Step', fontsize=12)
    ax.set_ylabel('Horizon Radius (grid units)', fontsize=12)
    ax.set_title('Event Horizon Formation (NRCI < 0.01)', fontsize=13)
    ax.grid(True, alpha=0.3)
    
    # Plot 4: Leaked OffBits (Hawking radiation proxy)
    ax = axes[1, 1]
    ax.plot(steps, history['leaked_offbits'], 'c-', linewidth=2)
    ax.set_xlabel('Simulation Step', fontsize=12)
    ax.set_ylabel('Leaked OffBits per Step', fontsize=12)
    ax.set_title('Hawking Radiation Proxy', fontsize=13)
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(f'{FIG_DIR}/03_bh_queue_dynamics.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"✓ Saved: {FIG_DIR}/03_bh_queue_dynamics.png")

def plot_parity_statistics(stats, hamming_weights):
    """Plot Golay parity statistics."""
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    fig.suptitle('Golay Parity Signatures in Escaped OffBits', fontsize=16, fontweight='bold')
    
    # Plot 1: Hamming Weight Distribution
    ax = axes[0]
    ax.hist(hamming_weights, bins=25, color='purple', alpha=0.7, edgecolor='black', density=True)
    
    # Overlay binomial distribution (null hypothesis)
    x = np.arange(0, 25)
    binomial_pmf = norm.pdf(x, loc=12, scale=np.sqrt(6))  # n=24, p=0.5
    ax.plot(x, binomial_pmf, 'r--', linewidth=2, label='Binomial (null)')
    
    ax.set_xlabel('Hamming Weight', fontsize=12)
    ax.set_ylabel('Probability Density', fontsize=12)
    ax.set_title(f'Hamming Weight Distribution (n={stats["n_samples"]:,})', fontsize=13)
    ax.grid(True, alpha=0.3, axis='y')
    ax.legend(fontsize=10)
    
    # Plot 2: Parity Bias
    ax = axes[1]
    categories = ['Even Parity', 'Odd Parity']
    percentages = [stats['even_parity_pct'], 100 - stats['even_parity_pct']]
    colors = ['green', 'orange']
    bars = ax.bar(categories, percentages, color=colors, alpha=0.7, edgecolor='black')
    
    # Add reference line at 50%
    ax.axhline(y=50, color='red', linestyle='--', linewidth=2, label='Random (50%)')
    
    # Add percentage labels on bars
    for bar, pct in zip(bars, percentages):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{pct:.2f}%', ha='center', va='bottom', fontsize=12, fontweight='bold')
    
    ax.set_ylabel('Percentage', fontsize=12)
    ax.set_title(f'Parity Bias: {stats["parity_bias"]:+.2f}%', fontsize=13)
    ax.set_ylim([0, 100])
    ax.grid(True, alpha=0.3, axis='y')
    ax.legend(fontsize=10)
    
    plt.tight_layout()
    plt.savefig(f'{FIG_DIR}/04_golay_parity_statistics.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"✓ Saved: {FIG_DIR}/04_golay_parity_statistics.png")

def main():
    """Main execution function."""
    print("\n" + "="*80)
    print("MODULE 3: 6D BITFIELD BLACK HOLE QUEUE MODEL")
    print("="*80)
    print("Framework: Universal Binary Principle (UBP) v3.2")
    print("Author: Euan R A Craig")
    print("="*80 + "\n")
    
    # Initialize bitfield (reduced size for computational efficiency)
    print("Initializing 6D bitfield...")
    bitfield = Bitfield6D(shape=(50, 50, 50, 3, 2, 2))
    
    # Simulate queue dynamics
    print("Running black hole queue simulation...")
    history = bitfield.simulate_queue_dynamics(
        n_steps=100,
        influx_rate=10000,
        P_max=8000
    )
    
    # Save history
    history_df = pd.DataFrame(history)
    history_file = f'{DATA_DIR}/bh_queue_history.csv'
    history_df.to_csv(history_file, index=False)
    print(f"✓ Saved queue history: {history_file}\n")
    
    # Plot dynamics
    print("Generating queue dynamics visualizations...")
    plot_queue_dynamics(history)
    
    # Compute Golay parity statistics
    print("\nComputing Golay parity statistics...")
    stats, hamming_weights = bitfield.compute_golay_parity_statistics(n_samples=10000)
    
    if stats:
        print("\nGolay Parity Statistics:")
        print("-"*80)
        print(f"  Samples analyzed: {stats['n_samples']:,}")
        print(f"  Mean Hamming weight: {stats['mean_hamming_weight']:.4f}")
        print(f"  Std Hamming weight: {stats['std_hamming_weight']:.4f}")
        print(f"  Variance: {stats['variance']:.4f}")
        print(f"  Even parity %: {stats['even_parity_pct']:.2f}%")
        print(f"  Expected (random): {stats['expected_even_pct']:.2f}%")
        print(f"  Parity bias: {stats['parity_bias']:+.2f}%")
        
        # Check if within predicted range (52-58.33%)
        if 52 <= stats['even_parity_pct'] <= 58.33:
            print(f"  ✓ Within predicted range [52%, 58.33%]")
        else:
            print(f"  ⚠ Outside predicted range [52%, 58.33%]")
        
        # Save statistics
        stats_df = pd.DataFrame([stats])
        stats_file = f'{DATA_DIR}/golay_parity_statistics.csv'
        stats_df.to_csv(stats_file, index=False)
        print(f"\n✓ Saved parity statistics: {stats_file}\n")
        
        # Plot parity statistics
        print("Generating parity visualizations...")
        plot_parity_statistics(stats, hamming_weights)
    
    print("\n" + "="*80)
    print("MODULE 3 COMPLETE")
    print("="*80)
    print(f"Key Results:")
    print(f"  - Final queue length: {history['total_queue'][-1]:,.0f} OffBits")
    print(f"  - Final mean NRCI: {history['mean_nrci'][-1]:.6f}")
    print(f"  - Final min NRCI: {history['min_nrci'][-1]:.6f}")
    print(f"  - Horizon radius: {history['horizon_radius'][-1]:.2f} grid units")
    if stats:
        print(f"  - Parity bias: {stats['parity_bias']:+.2f}%")
    print("="*80 + "\n")
    
    return bitfield, history, stats

if __name__ == "__main__":
    bitfield, history, stats = main()

