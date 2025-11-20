"""
Visualization Utilities for Local Excitations Framework
========================================================

Provides plotting and visualization tools for experimental results.

Author: Euan Craig & Manus AI
Date: November 21, 2025
"""

import math
from typing import List, Tuple, Optional
import sys
sys.path.insert(0, '..')
from coherence_substrate import CoherenceState


def save_data_csv(filepath: str, data: List[Tuple], headers: List[str]):
    """
    Save numerical data to CSV file.
    
    Args:
        filepath: Output file path
        data: List of tuples containing data rows
        headers: Column headers
    """
    with open(filepath, 'w') as f:
        f.write(','.join(headers) + '\n')
        for row in data:
            f.write(','.join(str(x) for x in row) + '\n')


def plot_interference_pattern(x_positions: List[float], intensities: List[float],
                              nrcis: List[float], output_path: str):
    """
    Plot double-slit interference pattern with coherence overlay.
    
    Args:
        x_positions: Screen positions
        intensities: Intensity at each position
        nrcis: NRCI values at each position
        output_path: Where to save the plot
    """
    try:
        import matplotlib.pyplot as plt
        
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8), sharex=True)
        
        # Intensity pattern
        ax1.plot(x_positions, intensities, 'b-', linewidth=2, label='Intensity')
        ax1.set_ylabel('Intensity (arbitrary units)', fontsize=12)
        ax1.set_title('Double-Slit Interference Pattern from Coherence Field', fontsize=14, fontweight='bold')
        ax1.grid(True, alpha=0.3)
        ax1.legend()
        
        # NRCI coherence
        ax2.plot(x_positions, nrcis, 'r-', linewidth=2, label='NRCI')
        ax2.axhline(y=0.999999, color='g', linestyle='--', alpha=0.5, label='Supercoherence threshold')
        ax2.set_xlabel('Position (arbitrary units)', fontsize=12)
        ax2.set_ylabel('NRCI', fontsize=12)
        ax2.set_title('Coherence Preservation Across Field', fontsize=12)
        ax2.grid(True, alpha=0.3)
        ax2.legend()
        
        plt.tight_layout()
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"Interference pattern saved to {output_path}")
        
    except ImportError:
        print("matplotlib not available, saving data only")
        # Save raw data as CSV
        csv_path = output_path.replace('.png', '.csv')
        save_data_csv(csv_path, 
                     list(zip(x_positions, intensities, nrcis)),
                     ['position', 'intensity', 'nrci'])
        print(f"Data saved to {csv_path}")


def plot_coherence_evolution(time_steps: List[int], nrci_values: List[float],
                             output_path: str, title: str = "Coherence Evolution"):
    """
    Plot NRCI evolution over time/iterations.
    
    Args:
        time_steps: Time step indices
        nrci_values: NRCI at each time step
        output_path: Where to save the plot
        title: Plot title
    """
    try:
        import matplotlib.pyplot as plt
        
        plt.figure(figsize=(10, 6))
        plt.plot(time_steps, nrci_values, 'b-', linewidth=2, label='NRCI')
        plt.axhline(y=0.999999, color='g', linestyle='--', alpha=0.5, label='Supercoherence threshold')
        plt.xlabel('Time Step / CSC Iteration', fontsize=12)
        plt.ylabel('NRCI', fontsize=12)
        plt.title(title, fontsize=14, fontweight='bold')
        plt.grid(True, alpha=0.3)
        plt.legend()
        plt.tight_layout()
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"Coherence evolution plot saved to {output_path}")
        
    except ImportError:
        csv_path = output_path.replace('.png', '.csv')
        save_data_csv(csv_path,
                     list(zip(time_steps, nrci_values)),
                     ['time_step', 'nrci'])
        print(f"Data saved to {csv_path}")


def plot_field_propagation(x_grid: List[float], y_grid: List[float],
                           field_values: List[List[float]], output_path: str,
                           title: str = "Coherence Field"):
    """
    Plot 2D coherence field as heatmap.
    
    Args:
        x_grid: X coordinates
        y_grid: Y coordinates
        field_values: 2D array of field values
        output_path: Where to save the plot
        title: Plot title
    """
    try:
        import matplotlib.pyplot as plt
        
        plt.figure(figsize=(10, 8))
        
        # Create meshgrid for contour plot
        X, Y = [], []
        for y in y_grid:
            X.append(x_grid)
            Y.append([y] * len(x_grid))
        
        plt.contourf(X, Y, field_values, levels=50, cmap='viridis')
        plt.colorbar(label='Field Amplitude')
        plt.xlabel('X Position', fontsize=12)
        plt.ylabel('Y Position', fontsize=12)
        plt.title(title, fontsize=14, fontweight='bold')
        plt.tight_layout()
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"Field propagation plot saved to {output_path}")
        
    except ImportError:
        # Save as CSV grid
        csv_path = output_path.replace('.png', '.csv')
        with open(csv_path, 'w') as f:
            f.write('x,y,field_value\n')
            for i, y in enumerate(y_grid):
                for j, x in enumerate(x_grid):
                    f.write(f"{x},{y},{field_values[i][j]}\n")
        print(f"Data saved to {csv_path}")


def plot_entanglement_correlation(angles: List[float], correlations: List[float],
                                  qm_predictions: Optional[List[float]],
                                  output_path: str):
    """
    Plot entanglement correlation vs measurement angle.
    
    Args:
        angles: Measurement angle differences (radians)
        correlations: UBP correlation coefficients
        qm_predictions: Standard QM predictions (optional)
        output_path: Where to save the plot
    """
    try:
        import matplotlib.pyplot as plt
        
        plt.figure(figsize=(10, 6))
        plt.plot(angles, correlations, 'bo-', linewidth=2, markersize=8, label='UBP Prediction')
        
        if qm_predictions:
            plt.plot(angles, qm_predictions, 'r--', linewidth=2, label='Standard QM')
        
        plt.axhline(y=0, color='k', linestyle='-', alpha=0.3)
        plt.xlabel('Angle Difference (radians)', fontsize=12)
        plt.ylabel('Correlation Coefficient E(a,b)', fontsize=12)
        plt.title('Entanglement Correlation: UBP vs Quantum Mechanics', fontsize=14, fontweight='bold')
        plt.grid(True, alpha=0.3)
        plt.legend()
        plt.tight_layout()
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"Entanglement correlation plot saved to {output_path}")
        
    except ImportError:
        csv_path = output_path.replace('.png', '.csv')
        if qm_predictions:
            save_data_csv(csv_path,
                         list(zip(angles, correlations, qm_predictions)),
                         ['angle', 'ubp_correlation', 'qm_prediction'])
        else:
            save_data_csv(csv_path,
                         list(zip(angles, correlations)),
                         ['angle', 'ubp_correlation'])
        print(f"Data saved to {csv_path}")


def plot_transformation_pathway(states: List[CoherenceState], labels: List[str],
                               output_path: str):
    """
    Plot particle transformation as coherence pathway.
    
    Args:
        states: Sequence of coherence states during transformation
        labels: Labels for each state
        output_path: Where to save the plot
    """
    try:
        import matplotlib.pyplot as plt
        
        nrcis = [s.nrci for s in states]
        depths = [s.composition_depth for s in states]
        
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8), sharex=True)
        
        # NRCI evolution
        ax1.plot(range(len(states)), nrcis, 'bo-', linewidth=2, markersize=8)
        ax1.axhline(y=0.999999, color='g', linestyle='--', alpha=0.5, label='Supercoherence')
        ax1.set_ylabel('NRCI', fontsize=12)
        ax1.set_title('Particle Transformation: Coherence Pathway', fontsize=14, fontweight='bold')
        ax1.grid(True, alpha=0.3)
        ax1.legend()
        
        # Composition depth
        ax2.plot(range(len(states)), depths, 'ro-', linewidth=2, markersize=8)
        ax2.set_xlabel('Transformation Step', fontsize=12)
        ax2.set_ylabel('Operator Composition Depth', fontsize=12)
        ax2.set_title('Computational Complexity', fontsize=12)
        ax2.grid(True, alpha=0.3)
        
        # Set x-axis labels
        ax2.set_xticks(range(len(labels)))
        ax2.set_xticklabels(labels, rotation=45, ha='right')
        
        plt.tight_layout()
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"Transformation pathway plot saved to {output_path}")
        
    except ImportError:
        csv_path = output_path.replace('.png', '.csv')
        save_data_csv(csv_path,
                     list(zip(labels, nrcis, depths)),
                     ['state', 'nrci', 'composition_depth'])
        print(f"Data saved to {csv_path}")
