#!/usr/bin/env python3
"""
UBP Python API Example

Demonstrates how to use the UBP system programmatically from Python.
This example shows direct API usage without the DSL.
"""

import sys
import os
import json
import numpy as np
import matplotlib.pyplot as plt

# Add UBP to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ubp_vm import Runtime
from ubp_semantics import (
    OffBit, Bitfield, energy, nrci, coherence,
    toggle_xor, resonance_toggle, entanglement_toggle,
    get_realm_constants, PI, PHI, EULER_E
)


def demonstrate_offbit_operations():
    """Demonstrate OffBit creation and manipulation."""
    print("=== OffBit Operations Demo ===")
    
    # Create OffBits
    offbit1 = OffBit(0x123456)  # 24-bit value
    offbit2 = OffBit(0x654321)
    
    print(f"OffBit 1: {offbit1}")
    print(f"OffBit 2: {offbit2}")
    
    # Manipulate layers
    offbit1.reality_layer = 42
    offbit1.information_layer = 21
    offbit1.activation_layer = 15
    offbit1.unactivated_layer = 8
    
    print(f"Modified OffBit 1: {offbit1}")
    print(f"Toggle state: {offbit1.toggle_state}")
    
    # Toggle operations
    and_result = toggle_xor(offbit1, offbit2)
    print(f"XOR result: {and_result}")
    
    print()


def demonstrate_energy_calculation():
    """Demonstrate UBP energy equation calculation."""
    print("=== Energy Calculation Demo ===")
    
    # Calculate energy with different parameters
    M_values = [100, 1000, 10000]  # Active OffBits
    
    for M in M_values:
        E = energy(M=M)
        print(f"Energy for M={M}: {E:.2e}")
    
    # Calculate energy for different realms
    realms = ["quantum", "electromagnetic", "gravitational"]
    
    for realm_name in realms:
        try:
            realm = get_realm_constants(realm_name)
            print(f"\n{realm['name']}:")
            print(f"  CRV: {realm['main_crv']}")
            print(f"  Frequency: {realm.get('frequency', 'N/A')} Hz")
            print(f"  Wavelength: {realm.get('wavelength', 'N/A')} nm")
            print(f"  NRCI Baseline: {realm.get('nrci_baseline', 'N/A')}")
        except KeyError:
            print(f"Realm {realm_name} not found")
    
    print()


def demonstrate_coherence_analysis():
    """Demonstrate coherence analysis between signals."""
    print("=== Coherence Analysis Demo ===")
    
    # Generate test signals
    t = np.linspace(0, 1, 100)
    
    # Signal 1: Pure sine wave
    freq1 = 10.0  # Hz
    signal1 = np.cos(2 * PI * freq1 * t).tolist()
    
    # Signal 2: Same frequency with noise
    signal2 = (np.cos(2 * PI * freq1 * t) + 0.1 * np.random.randn(len(t))).tolist()
    
    # Signal 3: Different frequency
    freq3 = 15.0  # Hz
    signal3 = np.cos(2 * PI * freq3 * t).tolist()
    
    # Calculate coherence
    coherence_12 = coherence(signal1, signal2)
    coherence_13 = coherence(signal1, signal3)
    coherence_11 = coherence(signal1, signal1)
    
    print(f"Coherence (signal1, signal2): {coherence_12:.4f}")
    print(f"Coherence (signal1, signal3): {coherence_13:.4f}")
    print(f"Coherence (signal1, signal1): {coherence_11:.4f}")
    
    # Check observability threshold
    threshold = 0.5
    print(f"\nObservability (threshold={threshold}):")
    print(f"  Signal1-Signal2: {'Observable' if abs(coherence_12) >= threshold else 'Not observable'}")
    print(f"  Signal1-Signal3: {'Observable' if abs(coherence_13) >= threshold else 'Not observable'}")
    
    print()


def demonstrate_runtime_simulation():
    """Demonstrate runtime simulation with metrics tracking."""
    print("=== Runtime Simulation Demo ===")
    
    # Initialize runtime
    runtime = Runtime("desktop_8gb")
    print(f"Runtime initialized: {runtime.hardware_profile}")
    
    # Set realm and initialize Bitfield
    runtime.set_realm("quantum")
    runtime.initialize_bitfield("quantum_bias", density=0.01, seed=42)
    
    print(f"Bitfield initialized: {runtime.bitfield}")
    print(f"Active realm: {runtime.state.active_realm}")
    
    # Run simulation
    print("\nRunning simulation...")
    result = runtime.run_simulation(
        steps=20,
        operations_per_step=10,
        record_timeline=True
    )
    
    print(f"Simulation completed in {result.execution_time:.4f} seconds")
    print(f"Final NRCI: {result.final_state.nrci_value:.6f}")
    print(f"Total toggles: {result.final_state.total_toggles}")
    
    # Display metrics
    print("\nFinal Metrics:")
    for key, value in result.metrics.items():
        if isinstance(value, float):
            print(f"  {key}: {value:.6f}")
        else:
            print(f"  {key}: {value}")
    
    # Plot timeline if matplotlib is available
    try:
        plot_simulation_timeline(result)
    except ImportError:
        print("Matplotlib not available for plotting")
    
    print()


def plot_simulation_timeline(result):
    """Plot simulation timeline metrics."""
    print("Generating timeline plot...")
    
    # Extract timeline data
    time_steps = [state.time_step for state in result.timeline]
    energy_values = [state.energy_value for state in result.timeline]
    nrci_values = [state.nrci_value for state in result.timeline]
    
    # Create plots
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))
    
    # Energy plot
    ax1.plot(time_steps, energy_values, 'b-', linewidth=2, label='Energy')
    ax1.set_xlabel('Time Step')
    ax1.set_ylabel('Energy')
    ax1.set_title('UBP System Energy Over Time')
    ax1.grid(True, alpha=0.3)
    ax1.legend()
    
    # NRCI plot
    ax2.plot(time_steps, nrci_values, 'r-', linewidth=2, label='NRCI')
    ax2.axhline(y=0.999999, color='g', linestyle='--', alpha=0.7, label='Target (6 nines)')
    ax2.set_xlabel('Time Step')
    ax2.set_ylabel('NRCI')
    ax2.set_title('Non-Random Coherence Index Over Time')
    ax2.grid(True, alpha=0.3)
    ax2.legend()
    
    plt.tight_layout()
    plt.savefig('ubp_simulation_timeline.png', dpi=150, bbox_inches='tight')
    print("Timeline plot saved as 'ubp_simulation_timeline.png'")
    plt.close()


def demonstrate_realm_switching():
    """Demonstrate switching between different realms."""
    print("=== Realm Switching Demo ===")
    
    runtime = Runtime("desktop_8gb")
    
    realms_to_test = ["quantum", "electromagnetic", "gravitational", "biological"]
    results = {}
    
    for realm_name in realms_to_test:
        print(f"\nTesting {realm_name} realm...")
        
        # Switch realm and initialize
        runtime.reset()
        runtime.set_realm(realm_name)
        runtime.initialize_bitfield("realm_specific", density=0.005, seed=42)
        
        # Run short simulation
        result = runtime.run_simulation(steps=10, operations_per_step=5)
        
        results[realm_name] = {
            'nrci': result.final_state.nrci_value,
            'energy': result.final_state.energy_value,
            'coherence_pressure': result.final_state.coherence_pressure,
            'execution_time': result.execution_time
        }
        
        print(f"  NRCI: {result.final_state.nrci_value:.6f}")
        print(f"  Energy: {result.final_state.energy_value:.2e}")
        print(f"  Execution time: {result.execution_time:.4f}s")
    
    # Compare results
    print("\n=== Realm Comparison ===")
    print(f"{'Realm':<15} {'NRCI':<10} {'Energy':<12} {'Time (s)':<10}")
    print("-" * 50)
    
    for realm, metrics in results.items():
        print(f"{realm:<15} {metrics['nrci']:<10.6f} {metrics['energy']:<12.2e} {metrics['execution_time']:<10.4f}")
    
    print()


def demonstrate_nrci_validation():
    """Demonstrate NRCI calculation and validation."""
    print("=== NRCI Validation Demo ===")
    
    # Generate test data
    np.random.seed(42)
    
    # Perfect correlation case
    target_perfect = [1.0, 2.0, 3.0, 4.0, 5.0]
    simulated_perfect = target_perfect.copy()
    nrci_perfect = nrci(simulated_perfect, target_perfect)
    
    # Good correlation case
    target_good = [1.0, 2.0, 3.0, 4.0, 5.0]
    simulated_good = [1.01, 1.98, 3.02, 3.97, 5.01]
    nrci_good = nrci(simulated_good, target_good)
    
    # Poor correlation case
    target_poor = [1.0, 2.0, 3.0, 4.0, 5.0]
    simulated_poor = [1.5, 2.8, 2.1, 4.9, 3.2]
    nrci_poor = nrci(simulated_poor, target_poor)
    
    print(f"Perfect correlation NRCI: {nrci_perfect:.6f}")
    print(f"Good correlation NRCI: {nrci_good:.6f}")
    print(f"Poor correlation NRCI: {nrci_poor:.6f}")
    
    # Validation against target
    target_nrci = 0.999999  # Six nines
    print(f"\nTarget NRCI: {target_nrci}")
    print(f"Perfect meets target: {nrci_perfect >= target_nrci}")
    print(f"Good meets target: {nrci_good >= target_nrci}")
    print(f"Poor meets target: {nrci_poor >= target_nrci}")
    
    print()


def save_example_results():
    """Save example results to JSON file."""
    print("=== Saving Example Results ===")
    
    # Run a complete simulation
    runtime = Runtime("desktop_8gb")
    runtime.set_realm("quantum")
    runtime.initialize_bitfield("quantum_bias", density=0.01, seed=42)
    
    result = runtime.run_simulation(steps=50, operations_per_step=10)
    
    # Save to file
    output_file = "python_api_example_results.json"
    with open(output_file, 'w') as f:
        json.dump(result.to_dict(), f, indent=2)
    
    print(f"Results saved to {output_file}")
    print(f"File size: {os.path.getsize(output_file)} bytes")
    
    print()


def main():
    """Run all demonstration functions."""
    print("UBP Python API Demonstration")
    print("=" * 50)
    
    try:
        demonstrate_offbit_operations()
        demonstrate_energy_calculation()
        demonstrate_coherence_analysis()
        demonstrate_runtime_simulation()
        demonstrate_realm_switching()
        demonstrate_nrci_validation()
        save_example_results()
        
        print("All demonstrations completed successfully!")
        
    except Exception as e:
        print(f"Error during demonstration: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()

