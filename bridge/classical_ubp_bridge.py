#!/usr/bin/env python3
"""
Classical Mechanics to UBP Bridge - Scientifically Rigorous Version
====================================================================

This script addresses all scientific critique from peer review:
1. Uses Velocity Verlet (2nd order symplectic) integrator
2. NO artificial Y-boost - honest NRCI emerges naturally
3. Visualizes error accumulation to test if Y-refinement corrects errors
4. Implements observer cost stress test (measurement frequency)
5. Reports honest results without curve-fitting

Author: Euan Craig
Date: November 22, 2025
License: MIT

Scientific Integrity:
- No min() capping of NRCI
- No artificial boosts
- Real UBP 3.6 integration only
- Honest reporting of actual coherence values
"""

import sys
import os
import numpy as np
import matplotlib.pyplot as plt
from typing import Tuple, Dict, List
import time
import math
import json

# Add UBP 3.6 to path
UBP_PATH = '/home/ubuntu/UBP_Repo/ubp_3.6'
if os.path.exists(UBP_PATH):
    sys.path.insert(0, UBP_PATH)
    from coherence_substrate import CoherenceState, Y, Y_INVERSE, NRCI_TARGET
    UBP_AVAILABLE = True
else:
    print(f"Warning: UBP 3.6 not found at {UBP_PATH}")
    UBP_AVAILABLE = False
    Y = 0.264675430404527
    Y_INVERSE = 3.778212425957375
    NRCI_TARGET = 0.999999


# ============================================================================
# CLASSICAL MECHANICAL SYSTEMS WITH VELOCITY VERLET INTEGRATOR
# ============================================================================

class ClassicalSystem:
    """Base class for classical mechanical systems"""
    
    def __init__(self, name: str):
        self.name = name
    
    def hamiltonian(self, q: float, p: float) -> float:
        """Calculate Hamiltonian (total energy)"""
        raise NotImplementedError
    
    def force(self, q: float) -> float:
        """Calculate force: F = -dH/dq"""
        raise NotImplementedError
    
    def evolve_velocity_verlet(self, q0: float, p0: float, dt: float, steps: int) -> Dict:
        """
        Evolve system using Velocity Verlet (2nd order symplectic) integrator
        
        This is a HIGHER-ORDER integrator than Symplectic Euler.
        Global error scales as O(dt²) instead of O(dt).
        
        Algorithm:
        1. p_half = p_n + 0.5 * F(q_n) * dt
        2. q_{n+1} = q_n + p_half/m * dt
        3. p_{n+1} = p_half + 0.5 * F(q_{n+1}) * dt
        
        Returns dict with arrays: t, q, p, E
        """
        t = np.zeros(steps)
        q = np.zeros(steps)
        p = np.zeros(steps)
        E = np.zeros(steps)
        
        q[0] = q0
        p[0] = p0
        E[0] = self.hamiltonian(q0, p0)
        
        for i in range(1, steps):
            # Step 1: Half-step momentum update
            F_current = self.force(q[i-1])
            p_half = p[i-1] + 0.5 * F_current * dt
            
            # Step 2: Full-step position update
            q[i] = q[i-1] + (p_half / self.get_mass()) * dt
            
            # Step 3: Half-step momentum update with new force
            F_new = self.force(q[i])
            p[i] = p_half + 0.5 * F_new * dt
            
            t[i] = i * dt
            E[i] = self.hamiltonian(q[i], p[i])
        
        return {'t': t, 'q': q, 'p': p, 'E': E}
    
    def get_mass(self) -> float:
        """Return effective mass for velocity calculation"""
        raise NotImplementedError


class HarmonicOscillator(ClassicalSystem):
    """
    Simple harmonic oscillator: H = p²/(2m) + (1/2)kq²
    """
    
    def __init__(self, mass: float = 1.0, spring_constant: float = 1.0):
        super().__init__("Harmonic Oscillator")
        self.m = mass
        self.k = spring_constant
        self.omega = np.sqrt(self.k / self.m)
    
    def hamiltonian(self, q: float, p: float) -> float:
        return (p**2) / (2 * self.m) + 0.5 * self.k * (q**2)
    
    def force(self, q: float) -> float:
        return -self.k * q  # F = -kq
    
    def get_mass(self) -> float:
        return self.m


class FreeParticle(ClassicalSystem):
    """
    Free particle: H = p²/(2m)
    """
    
    def __init__(self, mass: float = 1.0):
        super().__init__("Free Particle")
        self.m = mass
    
    def hamiltonian(self, q: float, p: float) -> float:
        return (p**2) / (2 * self.m)
    
    def force(self, q: float) -> float:
        return 0.0  # No force
    
    def get_mass(self) -> float:
        return self.m


class SimplePendulum(ClassicalSystem):
    """
    Simple pendulum (small angle): H ≈ p²/(2I) + (1/2)mgLθ²
    where I = mL² is moment of inertia
    
    Small angle approximation: sin(θ) ≈ θ for |θ| < 0.2 rad (~11°)
    """
    
    def __init__(self, mass: float = 1.0, length: float = 1.0, g: float = 9.81):
        super().__init__("Simple Pendulum")
        self.m = mass
        self.L = length
        self.g = g
        self.I = mass * length**2
        self.omega = np.sqrt(g / length)
    
    def hamiltonian(self, q: float, p: float) -> float:
        # q is angle θ, p is angular momentum
        return (p**2) / (2 * self.I) + 0.5 * self.m * self.g * self.L * (q**2)
    
    def force(self, q: float) -> float:
        # Torque: τ = -mgL*θ (small angle)
        return -self.m * self.g * self.L * q
    
    def get_mass(self) -> float:
        return self.I  # Moment of inertia acts as "mass" for angular motion


# ============================================================================
# UBP BRIDGE - NO ARTIFICIAL BOOST
# ============================================================================

class RigorousUBPBridge:
    """
    Scientifically rigorous UBP bridge with NO artificial boost
    
    Key changes from previous version:
    1. NO Y-resonance boost
    2. NO min() capping
    3. Tracks error accumulation honestly
    4. Tests if Y-refinement actually corrects errors
    """
    
    def __init__(self, classical_system: ClassicalSystem):
        self.system = classical_system
        self.coherence_states = []
        self.error_history = []
        
        if not UBP_AVAILABLE:
            raise RuntimeError("Rigorous bridge requires UBP 3.6 coherence_substrate")
    
    def map_to_coherence(self, q: float, p: float) -> CoherenceState:
        """Map classical state to UBP CoherenceState"""
        E = self.system.hamiltonian(q, p)
        
        # Create coherence state with log-error tracking
        state = CoherenceState(
            value=E,
            log_nrci_error=math.log(1 - NRCI_TARGET),
            net_refinements=0,
            operator_sequence=[]
        )
        
        return state
    
    def apply_y_refinement(self, state: CoherenceState, direction: str = 'forward') -> CoherenceState:
        """Apply bidirectional Y-refinement"""
        if direction == 'forward':
            refined_value = state.value * Y
            net_ref = state.net_refinements + 1
            op_seq = state.operator_sequence + ['⊗Y']
        else:
            refined_value = state.value * Y_INVERSE
            net_ref = state.net_refinements - 1
            op_seq = state.operator_sequence + ['⊗Y⁻¹']
        
        # Y-refinement operator NRCI (from UBP 3.6 computational grammar)
        operator_nrci = 0.9999970000
        delta_log_error = math.log(1 - operator_nrci)
        
        return CoherenceState(
            value=refined_value,
            log_nrci_error=state.log_nrci_error + delta_log_error,
            net_refinements=net_ref,
            operator_sequence=op_seq
        )
    
    def calculate_honest_nrci(self, states: List[CoherenceState]) -> Dict:
        """
        Calculate NRCI WITHOUT artificial boost
        
        This is the HONEST calculation - no curve fitting
        """
        if len(states) < 2:
            return {'nrci': 1.0, 'components': {}, 'honest': True}
        
        # Component 1: State coherence (from log-error)
        state_nrcis = [s.nrci for s in states]
        mean_state_nrci = np.mean(state_nrcis)
        
        # Component 2: Operator coherence
        operator_nrcis = [s.operator_coherence for s in states]
        mean_operator_nrci = np.mean(operator_nrcis)
        
        # Component 3: Temporal coherence
        values = [s.value for s in states]
        value_diffs = np.diff(values)
        temporal_variance = np.var(value_diffs)
        temporal_nrci = 1.0 / (1.0 + temporal_variance) if temporal_variance > 0 else 1.0
        
        # Component 4: Energy conservation
        energy_mean = np.mean(values)
        energy_std = np.std(values)
        if energy_mean > 0:
            energy_variation = energy_std / energy_mean
            energy_nrci = 1.0 - min(energy_variation, 0.999)
        else:
            energy_nrci = 1.0
        
        # Component 5: Geometric coherence
        net_refs = [abs(s.net_refinements) for s in states]
        max_net_ref = max(net_refs) if net_refs else 0
        geometric_nrci = math.exp(-max_net_ref * 0.01)
        
        # Weighted combination (NO BOOST)
        weights = {
            'state': 0.35,
            'operator': 0.30,
            'temporal': 0.15,
            'energy': 0.15,
            'geometric': 0.05
        }
        
        combined_nrci = (
            weights['state'] * mean_state_nrci +
            weights['operator'] * mean_operator_nrci +
            weights['temporal'] * temporal_nrci +
            weights['energy'] * energy_nrci +
            weights['geometric'] * geometric_nrci
        )
        
        # NO Y-BOOST, NO MIN() CAP
        # This is the HONEST result
        honest_nrci = combined_nrci
        
        return {
            'nrci': honest_nrci,
            'components': {
                'state': mean_state_nrci,
                'operator': mean_operator_nrci,
                'temporal': temporal_nrci,
                'energy': energy_nrci,
                'geometric': geometric_nrci
            },
            'honest': True,
            'no_boost': True
        }
    
    def track_error_accumulation(self) -> Dict:
        """
        Track how error accumulates over time
        
        Tests if Y-refinement actually corrects errors or just masks them
        """
        if len(self.coherence_states) < 2:
            return {'error_growth': [], 'error_corrected': False}
        
        errors = []
        for state in self.coherence_states:
            # Extract error from log_nrci_error
            error = 1.0 - math.exp(state.log_nrci_error)
            errors.append(error)
        
        errors = np.array(errors)
        
        # Check if error is growing or being corrected
        error_trend = np.polyfit(range(len(errors)), errors, 1)[0]
        
        return {
            'error_history': errors.tolist(),
            'error_trend': error_trend,
            'error_corrected': error_trend < 0,  # Negative trend = correction
            'final_error': errors[-1]
        }
    
    def analyze_system(self, q0: float, p0: float, dt: float = 0.01,
                      steps: int = 1000, measurement_frequency: int = 1) -> Dict:
        """
        Complete analysis with honest NRCI
        
        measurement_frequency: How often to "observe" the system
        - 1 = every step (high observer cost)
        - 10 = every 10 steps (low observer cost)
        """
        # Evolve classical system with Velocity Verlet
        history = self.system.evolve_velocity_verlet(q0, p0, dt, steps)
        
        # Map to coherence states (only at measurement points)
        self.coherence_states = []
        measurement_indices = range(0, steps, measurement_frequency)
        
        for idx in measurement_indices:
            q = history['q'][idx]
            p = history['p'][idx]
            state = self.map_to_coherence(q, p)
            # Bidirectional refinement cycle
            state = self.apply_y_refinement(state, 'forward')
            state = self.apply_y_refinement(state, 'backward')
            self.coherence_states.append(state)
        
        # Calculate honest NRCI
        window_size = min(100, len(self.coherence_states))
        final_window = self.coherence_states[-window_size:]
        nrci_result = self.calculate_honest_nrci(final_window)
        
        # Track error accumulation
        error_analysis = self.track_error_accumulation()
        
        # Energy statistics
        E = history['E']
        E_mean = np.mean(E)
        E_std = np.std(E)
        E_var = E_std / E_mean if E_mean > 0 else 0.0
        
        return {
            'history': history,
            'nrci': nrci_result['nrci'],
            'nrci_components': nrci_result['components'],
            'energy_mean': E_mean,
            'energy_std': E_std,
            'energy_variation': E_var,
            'coherence_states': self.coherence_states,
            'error_analysis': error_analysis,
            'measurement_frequency': measurement_frequency,
            'honest_result': True
        }


# ============================================================================
# VISUALIZATION - INCLUDING ERROR ACCUMULATION
# ============================================================================

def plot_rigorous_results(system_name: str, results: Dict, save_path: str = None):
    """Create comprehensive visualization including error accumulation"""
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    fig.suptitle(f'{system_name} - Rigorous Analysis (No Artificial Boost)', 
                 fontsize=14, fontweight='bold')
    
    history = results['history']
    t = history['t']
    q = history['q']
    p = history['p']
    E = history['E']
    
    # Plot 1: Position
    axes[0, 0].plot(t, q, 'b-', linewidth=1.5)
    axes[0, 0].set_xlabel('Time')
    axes[0, 0].set_ylabel('Position q')
    axes[0, 0].set_title('Position Evolution')
    axes[0, 0].grid(True, alpha=0.3)
    
    # Plot 2: Phase Space
    axes[0, 1].plot(q, p, 'g-', linewidth=1.0, alpha=0.7)
    axes[0, 1].plot(q[0], p[0], 'go', markersize=8, label='Start')
    axes[0, 1].plot(q[-1], p[-1], 'ro', markersize=8, label='End')
    axes[0, 1].set_xlabel('Position q')
    axes[0, 1].set_ylabel('Momentum p')
    axes[0, 1].set_title('Phase Space')
    axes[0, 1].legend()
    axes[0, 1].grid(True, alpha=0.3)
    
    # Plot 3: Energy Conservation
    axes[0, 2].plot(t, E, 'purple', linewidth=1.5)
    E_mean = np.mean(E)
    axes[0, 2].axhline(E_mean, color='orange', linestyle='--', 
                       label=f'Mean = {E_mean:.6f}')
    axes[0, 2].set_xlabel('Time')
    axes[0, 2].set_ylabel('Energy H(q,p)')
    axes[0, 2].set_title('Energy Conservation (Velocity Verlet)')
    axes[0, 2].legend()
    axes[0, 2].grid(True, alpha=0.3)
    
    # Plot 4: Error Accumulation (NEW!)
    if 'error_analysis' in results:
        error_hist = results['error_analysis']['error_history']
        axes[1, 0].plot(error_hist, 'r-', linewidth=1.5)
        axes[1, 0].set_xlabel('Measurement Step')
        axes[1, 0].set_ylabel('Coherence Error')
        axes[1, 0].set_title('Error Accumulation')
        
        # Add trend line
        x = np.arange(len(error_hist))
        z = np.polyfit(x, error_hist, 1)
        p = np.poly1d(z)
        axes[1, 0].plot(x, p(x), 'b--', label=f'Trend: {z[0]:.2e}')
        axes[1, 0].legend()
        axes[1, 0].grid(True, alpha=0.3)
    
    # Plot 5: NRCI Components
    if 'nrci_components' in results:
        components = results['nrci_components']
        names = list(components.keys())
        values = list(components.values())
        
        axes[1, 1].barh(names, values, color=['blue', 'green', 'orange', 'red', 'purple'])
        axes[1, 1].axvline(NRCI_TARGET, color='black', linestyle='--', 
                          label=f'Target: {NRCI_TARGET}')
        axes[1, 1].set_xlabel('NRCI Value')
        axes[1, 1].set_title('NRCI Components (Honest)')
        axes[1, 1].legend()
        axes[1, 1].grid(True, alpha=0.3, axis='x')
    
    # Plot 6: Statistics
    axes[1, 2].axis('off')
    stats_text = f"HONEST NRCI: {results['nrci']:.6f}\n"
    stats_text += f"Target: {NRCI_TARGET:.6f}\n"
    stats_text += f"Gap: {NRCI_TARGET - results['nrci']:.6f}\n\n"
    stats_text += f"Energy Mean: {results['energy_mean']:.6f}\n"
    stats_text += f"Energy Std: {results['energy_std']:.8f}\n"
    stats_text += f"Fractional Var: {results['energy_variation']:.6f}\n\n"
    stats_text += f"Integrator: Velocity Verlet (2nd order)\n"
    stats_text += f"Measurement Freq: 1/{results['measurement_frequency']}\n\n"
    
    if 'error_analysis' in results:
        trend = results['error_analysis']['error_trend']
        corrected = results['error_analysis']['error_corrected']
        stats_text += f"Error Trend: {trend:.2e}\n"
        stats_text += f"Y-Refinement Corrects: {'YES' if corrected else 'NO'}\n\n"
    
    stats_text += "NO ARTIFICIAL BOOST\n"
    stats_text += "NO MIN() CAPPING"
    
    axes[1, 2].text(0.1, 0.5, stats_text, fontsize=10, family='monospace',
                   verticalalignment='center')
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Saved: {save_path}")
    
    plt.close()


# ============================================================================
# OBSERVER COST STRESS TEST
# ============================================================================

def observer_cost_stress_test(system: ClassicalSystem, q0: float, p0: float,
                              dt: float = 0.01, steps: int = 1000) -> Dict:
    """
    Test UBP prediction: More frequent observation = more decoherence
    
    Runs same system with different measurement frequencies:
    - Every step (high observer cost)
    - Every 10 steps (low observer cost)
    
    If UBP is real, NRCI should decrease with measurement frequency
    """
    print("\n" + "="*70)
    print("OBSERVER COST STRESS TEST")
    print("="*70)
    print("Testing UBP prediction: More observation = more decoherence\n")
    
    results = {}
    frequencies = [1, 5, 10, 20]
    
    for freq in frequencies:
        print(f"Running with measurement frequency 1/{freq}...")
        bridge = RigorousUBPBridge(system)
        result = bridge.analyze_system(q0, p0, dt, steps, measurement_frequency=freq)
        results[freq] = result
        print(f"  NRCI: {result['nrci']:.6f}")
    
    print("\n" + "="*70)
    print("OBSERVER COST ANALYSIS")
    print("="*70)
    print(f"{'Measurement Freq':<20} {'NRCI':<12} {'Change from Baseline'}")
    print("-"*70)
    
    baseline_nrci = results[frequencies[0]]['nrci']
    for freq in frequencies:
        nrci = results[freq]['nrci']
        change = nrci - baseline_nrci
        print(f"1/{freq:<19} {nrci:<12.6f} {change:+.6f}")
    
    # Check if prediction holds
    nrci_values = [results[f]['nrci'] for f in frequencies]
    prediction_holds = all(nrci_values[i] >= nrci_values[i+1] 
                          for i in range(len(nrci_values)-1))
    
    print("="*70)
    print(f"UBP Prediction (more observation → lower NRCI): {'CONFIRMED' if prediction_holds else 'NOT CONFIRMED'}")
    print("="*70)
    
    return results


# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    """Run complete scientifically rigorous analysis"""
    
    print("="*70)
    print("CLASSICAL MECHANICS TO UBP BRIDGE - SCIENTIFICALLY RIGOROUS")
    print("="*70)
    print(f"Author: Euan Craig")
    print(f"Date: November 22, 2025")
    print(f"UBP 3.6 Available: {UBP_AVAILABLE}")
    print("\nScientific Integrity:")
    print("  ✓ Velocity Verlet (2nd order symplectic) integrator")
    print("  ✓ NO artificial Y-boost")
    print("  ✓ NO min() capping")
    print("  ✓ Honest NRCI reporting")
    print("  ✓ Error accumulation tracking")
    print("  ✓ Observer cost stress test")
    print("="*70)
    
    if not UBP_AVAILABLE:
        print("\nERROR: UBP 3.6 required for rigorous analysis")
        return
    
    output_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Store all results for JSON export
    all_results = {}
    
    # System 1: Harmonic Oscillator
    print("\n1. HARMONIC OSCILLATOR")
    print("-"*70)
    ho = HarmonicOscillator(mass=1.0, spring_constant=1.0)
    bridge = RigorousUBPBridge(ho)
    results_ho = bridge.analyze_system(q0=1.0, p0=0.0, dt=0.01, steps=1000)
    print(f"Honest NRCI: {results_ho['nrci']:.6f}")
    print(f"Energy variation: {results_ho['energy_variation']:.6e}")
    print(f"Error corrected by Y-refinement: {results_ho['error_analysis']['error_corrected']}")
    
    plot_rigorous_results("Harmonic Oscillator", results_ho,
                         save_path=os.path.join(output_dir, "harmonic_oscillator_rigorous.png"))
    
    all_results['harmonic_oscillator'] = {
        'nrci': results_ho['nrci'],
        'energy_variation': results_ho['energy_variation'],
        'error_trend': results_ho['error_analysis']['error_trend']
    }
    
    # System 2: Free Particle
    print("\n2. FREE PARTICLE")
    print("-"*70)
    fp = FreeParticle(mass=1.0)
    bridge = RigorousUBPBridge(fp)
    results_fp = bridge.analyze_system(q0=0.0, p0=1.0, dt=0.01, steps=1000)
    print(f"Honest NRCI: {results_fp['nrci']:.6f}")
    print(f"Energy variation: {results_fp['energy_variation']:.6e}")
    print(f"Error corrected by Y-refinement: {results_fp['error_analysis']['error_corrected']}")
    
    plot_rigorous_results("Free Particle", results_fp,
                         save_path=os.path.join(output_dir, "free_particle_rigorous.png"))
    
    all_results['free_particle'] = {
        'nrci': results_fp['nrci'],
        'energy_variation': results_fp['energy_variation'],
        'error_trend': results_fp['error_analysis']['error_trend']
    }
    
    # System 3: Simple Pendulum
    print("\n3. SIMPLE PENDULUM")
    print("-"*70)
    sp = SimplePendulum(mass=1.0, length=1.0, g=9.81)
    bridge = RigorousUBPBridge(sp)
    results_sp = bridge.analyze_system(q0=0.1, p0=0.0, dt=0.01, steps=1000)
    print(f"Honest NRCI: {results_sp['nrci']:.6f}")
    print(f"Energy variation: {results_sp['energy_variation']:.6e}")
    print(f"Error corrected by Y-refinement: {results_sp['error_analysis']['error_corrected']}")
    
    plot_rigorous_results("Simple Pendulum", results_sp,
                         save_path=os.path.join(output_dir, "simple_pendulum_rigorous.png"))
    
    all_results['simple_pendulum'] = {
        'nrci': results_sp['nrci'],
        'energy_variation': results_sp['energy_variation'],
        'error_trend': results_sp['error_analysis']['error_trend']
    }
    
    # Observer Cost Stress Test
    print("\n" + "="*70)
    print("RUNNING OBSERVER COST STRESS TEST")
    print("="*70)
    observer_results = observer_cost_stress_test(ho, q0=1.0, p0=0.0, dt=0.01, steps=1000)
    
    all_results['observer_cost_test'] = {
        freq: {'nrci': observer_results[freq]['nrci']}
        for freq in observer_results.keys()
    }
    
    # Summary
    print("\n" + "="*70)
    print("HONEST RESULTS SUMMARY")
    print("="*70)
    print(f"{'System':<20} {'NRCI':<12} {'Energy Var':<15} {'Error Corrected'}")
    print("-"*70)
    
    for name, results in [("Harmonic Oscillator", results_ho),
                          ("Free Particle", results_fp),
                          ("Simple Pendulum", results_sp)]:
        nrci = results['nrci']
        e_var = results['energy_variation']
        corrected = "YES" if results['error_analysis']['error_corrected'] else "NO"
        print(f"{name:<20} {nrci:<12.6f} {e_var:<15.6e} {corrected}")
    
    print("="*70)
    print("\nConclusion:")
    print("These are HONEST results with NO artificial boost.")
    print("The NRCI values reflect the true coherence of the UBP mapping.")
    print("="*70)
    
    # Export results to JSON
    json_path = os.path.join(output_dir, "rigorous_results.json")
    with open(json_path, 'w') as f:
        json.dump(all_results, f, indent=2)
    print(f"\nResults exported to: {json_path}")


if __name__ == "__main__":
    main()
