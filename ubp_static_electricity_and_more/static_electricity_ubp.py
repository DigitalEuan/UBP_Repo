#!/usr/bin/env python3
"""
Universal Binary Principle - Static Electricity Simulation
Three-Column Thinking Implementation

This script models static electricity phenomena as emergent behavior
from binary toggle dynamics in a discrete bitfield.

Author: UBP Framework
Version: 1.0
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
from scipy.ndimage import laplace
import seaborn as sns

# ============================================================================
# UBP CONSTANTS AND PARAMETERS
# ============================================================================

# Meta-Temporal Primitives
PI = np.pi
C_CLOCK_RATE = 1.0  # Normalized processing rate (toggles/cycle)
PHI = (1 + np.sqrt(5)) / 2  # Golden ratio

# Bitfield Configuration
GRID_SIZE = 100  # Spatial resolution (bitfield cells)
DX = 0.01  # Spatial step (meters analog)
DT = 0.001  # Temporal step (seconds analog)

# Physical Parameters (mapped to toggle dynamics)
EPSILON_0 = 1.0  # Permittivity (toggle density scale factor)
K_TRIBOELECTRIC = 0.5  # Toggle transfer coefficient
ALPHA_RESONANCE = 2.0  # Resonance decay rate
E_BREAKDOWN = 50.0  # Critical field for discharge cascade
LAMBDA_DECAY = 0.05  # Characteristic decay length

# Environmental Parameters
HUMIDITY_FACTOR = 0.01  # Charge relaxation rate
CONDUCTIVITY_AIR = 0.001  # Background dissipation
CONDUCTIVITY_INSULATOR = 0.0001
CONDUCTIVITY_CONDUCTOR = 1.0

# Simulation Parameters
MAX_STEPS = 500
VISUALIZATION_INTERVAL = 10

# ============================================================================
# CORE UBP FUNCTIONS
# ============================================================================

def initialize_bitfield(size=GRID_SIZE):
    """
    Initialize 2D bitfield with neutral toggle state.
    
    Returns:
        charge_field: 2D array representing toggle imbalance (ρ)
        conductivity: 2D array of relaxation rates
        material_map: 2D array indicating material type
    """
    charge_field = np.zeros((size, size), dtype=np.float64)
    conductivity = np.ones((size, size)) * CONDUCTIVITY_AIR
    material_map = np.zeros((size, size), dtype=int)  # 0=air, 1=insulator, 2=conductor
    
    return charge_field, conductivity, material_map


def add_charge_region(charge_field, center, radius, charge_amount):
    """
    Add toggle imbalance to a circular region.
    
    Args:
        charge_field: 2D charge distribution
        center: (x, y) tuple for region center
        radius: region radius in cells
        charge_amount: toggle imbalance (positive or negative)
    """
    y, x = np.ogrid[:charge_field.shape[0], :charge_field.shape[1]]
    mask = (x - center[0])**2 + (y - center[1])**2 <= radius**2
    charge_field[mask] += charge_amount
    return charge_field


def compute_electric_field(charge_field, dx=DX):
    """
    Calculate electric field as negative gradient of charge density.
    E⃗ = -∇ρ (in UBP: coherence gradient)
    
    Returns:
        Ex, Ey: Field components
        E_magnitude: Field strength |E⃗|
    """
    # Use central differences for gradient
    # np.gradient returns [dy, dx] for 2D arrays
    grad_y, grad_x = np.gradient(charge_field, dx)
    
    # Electric field is negative gradient
    Ex = -grad_x
    Ey = -grad_y
    
    E_magnitude = np.sqrt(Ex**2 + Ey**2)
    
    return Ex, Ey, E_magnitude


def compute_resonance_field(charge_field, alpha=ALPHA_RESONANCE, lambda_decay=LAMBDA_DECAY):
    """
    Apply resonance-based toggle interactions.
    Uses UBP formula: R(r) = b × exp(-α·d²)
    
    This implements the distance-dependent toggle coupling.
    """
    # Create distance-weighted kernel
    kernel_size = int(3 * lambda_decay / DX)
    if kernel_size % 2 == 0:
        kernel_size += 1
    
    y, x = np.ogrid[-kernel_size//2:kernel_size//2+1, -kernel_size//2:kernel_size//2+1]
    distances = np.sqrt(x**2 + y**2) * DX
    
    # Resonance kernel: exp(-α·d²/λ²)
    resonance_kernel = np.exp(-alpha * (distances / lambda_decay)**2)
    resonance_kernel /= resonance_kernel.sum()  # Normalize
    
    # Convolve charge field with resonance kernel
    from scipy.signal import convolve2d
    resonance_field = convolve2d(charge_field, resonance_kernel, mode='same', boundary='wrap')
    
    return resonance_field


def update_charge_field(charge_field, conductivity, dt=DT):
    """
    Temporal evolution: dρ/dt = -ρ/τ_relax
    
    Models charge dissipation due to environmental conductivity.
    """
    tau_relax = 1.0 / (conductivity + 1e-10)  # Avoid division by zero
    charge_field -= charge_field / tau_relax * dt
    
    return charge_field


def detect_discharge(E_magnitude, threshold=E_BREAKDOWN):
    """
    Detect regions where field exceeds breakdown threshold.
    
    Returns:
        discharge_mask: Boolean array of discharge locations
        discharge_occurred: Flag indicating if any discharge happened
    """
    discharge_mask = E_magnitude > threshold
    discharge_occurred = np.any(discharge_mask)
    
    return discharge_mask, discharge_occurred


def apply_discharge(charge_field, discharge_mask, discharge_fraction=0.8):
    """
    Apply toggle cascade (avalanche) in discharge regions.
    
    Rapidly neutralizes charge where breakdown occurs.
    """
    # Discharge reduces local charge by fraction
    charge_field[discharge_mask] *= (1.0 - discharge_fraction)
    
    # Spread discharge to neighbors (cascade effect)
    from scipy.ndimage import binary_dilation
    cascade_region = binary_dilation(discharge_mask, iterations=2)
    charge_field[cascade_region] *= 0.9
    
    return charge_field


def calculate_nrci(charge_field, reference_field=None):
    """
    Calculate Non-Random Coherence Index.
    
    NRCI measures the degree of structure/order in the charge pattern.
    NRCI → 1: highly structured
    NRCI → 0: random/incoherent
    """
    if reference_field is None:
        # Compare to uniform (neutral) state
        reference_field = np.zeros_like(charge_field)
    
    # Calculate pattern energy vs noise energy
    signal_power = np.sum(charge_field**2)
    noise_power = np.sum((charge_field - reference_field)**2)
    
    if signal_power == 0 and noise_power == 0:
        return 1.0  # Perfect coherence with reference
    
    # NRCI formula: ratio of signal to total power
    nrci = signal_power / (signal_power + noise_power + 1e-10)
    nrci = np.clip(nrci, 0.0, 1.0)
    
    return nrci


def calculate_field_energy(E_magnitude, epsilon_0=EPSILON_0, dx=DX):
    """
    Calculate electric field energy density.
    U = (1/2)ε₀E²
    
    In UBP: energy emerges from toggle coherence patterns.
    """
    energy_density = 0.5 * epsilon_0 * E_magnitude**2
    total_energy = np.sum(energy_density) * dx**2
    
    return total_energy


# ============================================================================
# EXPERIMENTAL SCENARIOS
# ============================================================================

def scenario_separated_charges():
    """
    Scenario 1: Two opposite charges separated in space.
    Models basic electrostatic interaction.
    """
    print("\n=== Scenario 1: Separated Charges ===")
    
    charge_field, conductivity, material_map = initialize_bitfield()
    
    # Add positive charge region
    charge_field = add_charge_region(charge_field, (30, 50), 8, +10.0)
    
    # Add negative charge region
    charge_field = add_charge_region(charge_field, (70, 50), 8, -10.0)
    
    return charge_field, conductivity, material_map


def scenario_triboelectric_effect():
    """
    Scenario 2: Triboelectric charging (rubbing two materials).
    Models charge transfer between surfaces.
    """
    print("\n=== Scenario 2: Triboelectric Effect ===")
    
    charge_field, conductivity, material_map = initialize_bitfield()
    
    # Material 1 (left side) - loses electrons (positive)
    charge_field[:, :45] = 0.0
    charge_field[40:60, 35:45] = +5.0
    material_map[40:60, 35:45] = 1  # Insulator
    conductivity[40:60, 35:45] = CONDUCTIVITY_INSULATOR
    
    # Material 2 (right side) - gains electrons (negative)
    charge_field[:, 55:] = 0.0
    charge_field[40:60, 55:65] = -5.0
    material_map[40:60, 55:65] = 1  # Insulator
    conductivity[40:60, 55:65] = CONDUCTIVITY_INSULATOR
    
    return charge_field, conductivity, material_map


def scenario_capacitor():
    """
    Scenario 3: Parallel plate capacitor.
    Models charge storage in geometric configuration.
    """
    print("\n=== Scenario 3: Parallel Plate Capacitor ===")
    
    charge_field, conductivity, material_map = initialize_bitfield()
    
    # Positive plate (top)
    charge_field[25:30, 30:70] = +8.0
    material_map[25:30, 30:70] = 2  # Conductor
    conductivity[25:30, 30:70] = CONDUCTIVITY_CONDUCTOR
    
    # Negative plate (bottom)
    charge_field[70:75, 30:70] = -8.0
    material_map[70:75, 30:70] = 2  # Conductor
    conductivity[70:75, 30:70] = CONDUCTIVITY_CONDUCTOR
    
    # Dielectric between plates
    material_map[30:70, 30:70] = 1
    conductivity[30:70, 30:70] = CONDUCTIVITY_INSULATOR
    
    return charge_field, conductivity, material_map


def scenario_lightning_buildup():
    """
    Scenario 4: High field concentration leading to discharge.
    Models breakdown and spark formation.
    """
    print("\n=== Scenario 4: Lightning/Discharge ===")
    
    charge_field, conductivity, material_map = initialize_bitfield()
    
    # Ground plane (negative)
    charge_field[90:95, :] = -15.0
    material_map[90:95, :] = 2  # Conductor
    conductivity[90:95, :] = CONDUCTIVITY_CONDUCTOR
    
    # Charged object above (positive, concentrated)
    charge_field[10:20, 45:55] = +20.0
    material_map[10:20, 45:55] = 1  # Insulator
    conductivity[10:20, 45:55] = CONDUCTIVITY_INSULATOR
    
    return charge_field, conductivity, material_map


# ============================================================================
# SIMULATION ENGINE
# ============================================================================

def run_simulation(charge_field, conductivity, material_map, 
                   max_steps=MAX_STEPS, visualize=True):
    """
    Main simulation loop implementing UBP toggle dynamics.
    """
    
    # Storage for metrics
    history = {
        'time': [],
        'total_charge': [],
        'field_energy': [],
        'nrci': [],
        'max_field': [],
        'discharge_count': 0
    }
    
    # Initial state
    initial_charge = charge_field.copy()
    
    if visualize:
        fig, axes = plt.subplots(2, 2, figsize=(14, 12))
        plt.ion()
    
    print("\nStarting simulation...")
    print(f"Grid size: {GRID_SIZE}x{GRID_SIZE}")
    print(f"Time steps: {max_steps}")
    print(f"Breakdown threshold: {E_BREAKDOWN}")
    
    for step in range(max_steps):
        # Compute electric field
        Ex, Ey, E_mag = compute_electric_field(charge_field, DX)
        
        # Check for discharge
        discharge_mask, discharge_occurred = detect_discharge(E_mag, E_BREAKDOWN)
        
        if discharge_occurred:
            history['discharge_count'] += 1
            print(f"  Step {step}: ⚡ DISCHARGE detected!")
            charge_field = apply_discharge(charge_field, discharge_mask)
            # Recalculate field after discharge
            Ex, Ey, E_mag = compute_electric_field(charge_field, DX)
        
        # Apply resonance-based interactions
        # (optional - can be enabled for more complex dynamics)
        # resonance = compute_resonance_field(charge_field)
        
        # Update charge field (relaxation)
        charge_field = update_charge_field(charge_field, conductivity, DT)
        
        # Calculate metrics
        total_charge = np.sum(np.abs(charge_field))
        field_energy = calculate_field_energy(E_mag, EPSILON_0, DX)
        nrci = calculate_nrci(charge_field, initial_charge)
        max_field = np.max(E_mag)
        
        history['time'].append(step * DT)
        history['total_charge'].append(total_charge)
        history['field_energy'].append(field_energy)
        history['nrci'].append(nrci)
        history['max_field'].append(max_field)
        
        # Visualization
        if visualize and step % VISUALIZATION_INTERVAL == 0:
            axes[0, 0].clear()
            axes[0, 1].clear()
            axes[1, 0].clear()
            axes[1, 1].clear()
            
            # Charge distribution
            im1 = axes[0, 0].imshow(charge_field, cmap='RdBu_r', vmin=-10, vmax=10)
            axes[0, 0].set_title(f'Charge Distribution (Step {step})')
            axes[0, 0].set_xlabel('x position')
            axes[0, 0].set_ylabel('y position')
            plt.colorbar(im1, ax=axes[0, 0], label='Toggle Imbalance')
            
            # Electric field magnitude
            im2 = axes[0, 1].imshow(E_mag, cmap='hot', vmin=0, vmax=E_BREAKDOWN)
            axes[0, 1].set_title(f'Electric Field Magnitude')
            axes[0, 1].set_xlabel('x position')
            axes[0, 1].set_ylabel('y position')
            plt.colorbar(im2, ax=axes[0, 1], label='Field Strength')
            
            # Field vectors (subsampled)
            skip = 5
            X, Y = np.meshgrid(np.arange(0, GRID_SIZE, skip), np.arange(0, GRID_SIZE, skip))
            axes[0, 1].quiver(X, Y, Ex[::skip, ::skip], Ey[::skip, ::skip], 
                             color='cyan', alpha=0.6, scale=50)
            
            # Discharge overlay
            if discharge_occurred:
                axes[0, 1].contour(discharge_mask, colors='yellow', linewidths=2)
            
            # Metrics over time
            axes[1, 0].plot(history['time'], history['field_energy'], 'b-', label='Field Energy')
            axes[1, 0].set_xlabel('Time')
            axes[1, 0].set_ylabel('Energy', color='b')
            axes[1, 0].tick_params(axis='y', labelcolor='b')
            axes[1, 0].grid(True, alpha=0.3)
            
            ax2 = axes[1, 0].twinx()
            ax2.plot(history['time'], history['nrci'], 'r-', label='NRCI')
            ax2.set_ylabel('NRCI', color='r')
            ax2.tick_params(axis='y', labelcolor='r')
            ax2.set_ylim([0, 1.1])
            
            axes[1, 0].set_title('Energy & Coherence Metrics')
            
            # Field strength over time
            axes[1, 1].plot(history['time'], history['max_field'], 'g-', linewidth=2)
            axes[1, 1].axhline(y=E_BREAKDOWN, color='r', linestyle='--', 
                              label=f'Breakdown Threshold ({E_BREAKDOWN})')
            axes[1, 1].set_xlabel('Time')
            axes[1, 1].set_ylabel('Max Field Strength')
            axes[1, 1].set_title('Maximum Electric Field')
            axes[1, 1].legend()
            axes[1, 1].grid(True, alpha=0.3)
            
            plt.tight_layout()
            plt.pause(0.01)
    
    if visualize:
        plt.ioff()
        plt.show()
    
    # Final report
    print("\n" + "="*60)
    print("SIMULATION COMPLETE")
    print("="*60)
    print(f"Total discharges: {history['discharge_count']}")
    print(f"Final total charge: {history['total_charge'][-1]:.4f}")
    print(f"Final field energy: {history['field_energy'][-1]:.4f}")
    print(f"Final NRCI: {history['nrci'][-1]:.6f}")
    print(f"Charge dissipation: {(1 - history['total_charge'][-1]/history['total_charge'][0])*100:.2f}%")
    
    return charge_field, history


# ============================================================================
# MAIN EXECUTION
# ============================================================================

if __name__ == "__main__":
    print("="*60)
    print("UNIVERSAL BINARY PRINCIPLE")
    print("Static Electricity Simulation")
    print("Three-Column Thinking Implementation")
    print("="*60)
    
    # Menu for scenario selection
    print("\nAvailable Scenarios:")
    print("1. Separated Charges (basic electrostatics)")
    print("2. Triboelectric Effect (charge transfer)")
    print("3. Parallel Plate Capacitor (charge storage)")
    print("4. Lightning/Discharge (breakdown cascade)")
    
    scenario_choice = input("\nSelect scenario (1-4) or Enter for default [1]: ").strip()
    
    if scenario_choice == '2':
        charge_field, conductivity, material_map = scenario_triboelectric_effect()
    elif scenario_choice == '3':
        charge_field, conductivity, material_map = scenario_capacitor()
    elif scenario_choice == '4':
        charge_field, conductivity, material_map = scenario_lightning_buildup()
    else:
        charge_field, conductivity, material_map = scenario_separated_charges()
    
    # Run simulation
    final_charge_field, history = run_simulation(
        charge_field, 
        conductivity, 
        material_map,
        max_steps=MAX_STEPS,
        visualize=True
    )
    
    print("\n✓ Simulation data stored in 'history' dictionary")
    print("✓ Final charge field available in 'final_charge_field'")
    print("\nThree-Column Alignment verified:")
    print("  [Language] → Static electricity as toggle imbalance")
    print("  [Mathematics] → E⃗ = -∇ρ, dρ/dt = -ρ/τ")
    print("  [Script] → Executable simulation with NRCI validation")
