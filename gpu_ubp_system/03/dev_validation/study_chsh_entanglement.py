"""
CHSH Entanglement Test Study
=============================

A complete scientific study using the GPU UBP system to investigate
Bell inequality violations through the CHSH (Clauser-Horne-Shimony-Holt) test.

**Research Question:**
Can UBP coherence states exhibit correlations that violate the CHSH inequality,
suggesting quantum-like entanglement emerges from geometric coherence?

**CHSH Inequality:**
Classical bound: |S| ≤ 2
Quantum bound (Tsirelson): |S| ≤ 2√2 ≈ 2.828

Where S = E(a,b) - E(a,b') + E(a',b) + E(a',b')
E(a,b) = correlation between measurements at angles a and b

**UBP Implementation:**
- Entangled pair: Two TGIC nodes with resonance coupling
- Measurement angles: Rotation in coherence phase space
- Correlation: Coherence product after measurement

Author: Euan Craig, New Zealand
Date: November 21, 2025
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'ubp_core'))

from typing import Dict, List, Tuple, Any
import math
import random
import time
import json

from coherence_substrate import CoherenceState
from tgic import DodecahedralGraph, TGICNode
from kernels import resonance_kernel
from gpu_ubp_sim import GPUUBPSimulation


class CHSHEntanglementStudy:
    """
    CHSH Entanglement Test using GPU UBP system.
    """
    
    def __init__(self, backend: str = 'cpu'):
        """
        Initialize CHSH study.
        
        Args:
            backend: Taichi backend ('cpu' or 'metal')
        """
        self.backend = backend
        self.sim = GPUUBPSimulation(backend=backend, enable_visualization=False)
        
        # CHSH measurement angles (in radians)
        # Optimal angles for maximum violation: 0, π/4, π/8, 3π/8
        self.angle_a = 0.0
        self.angle_a_prime = math.pi / 2
        self.angle_b = math.pi / 4
        self.angle_b_prime = 3 * math.pi / 4
        
        # Results storage
        self.correlations: Dict[str, List[float]] = {
            'ab': [],
            'ab_prime': [],
            'a_prime_b': [],
            'a_prime_b_prime': []
        }
        
        self.chsh_values: List[float] = []
        self.nrci_history: List[float] = []
        
        print("=" * 70)
        print("CHSH ENTANGLEMENT TEST STUDY")
        print("=" * 70)
        print(f"Backend: {backend}")
        print(f"Measurement angles:")
        print(f"  a  = {self.angle_a:.4f} rad")
        print(f"  a' = {self.angle_a_prime:.4f} rad")
        print(f"  b  = {self.angle_b:.4f} rad")
        print(f"  b' = {self.angle_b_prime:.4f} rad")
        print()
    
    def create_entangled_pair(self) -> Tuple[TGICNode, TGICNode]:
        """
        Create an entangled pair of TGIC nodes.
        
        In UBP, entanglement emerges from resonance coupling between
        nodes with high coherence.
        
        Returns:
            Tuple of (node_a, node_b)
        """
        # Select two connected nodes from TGIC graph
        node_ids = list(self.sim.graph.nodes.keys())
        node_a_id = random.choice(node_ids)
        node_b_id = random.choice(list(self.sim.graph.nodes[node_a_id].connections))
        
        node_a = self.sim.graph.nodes[node_a_id]
        node_b = self.sim.graph.nodes[node_b_id]
        
        # Prepare nodes in supercoherent state (entanglement precondition)
        node_a.coherence = CoherenceState(1.0, log_nrci_error=math.log(1 - 0.999997))
        node_b.coherence = CoherenceState(1.0, log_nrci_error=math.log(1 - 0.999997))
        
        # Apply resonance coupling to create entanglement
        coupled_state = node_a.coherence_coupling(node_b)
        
        # Update both nodes with coupled state (entangled)
        node_a.coherence = coupled_state
        node_b.coherence = coupled_state
        
        return node_a, node_b
    
    def measure_at_angle(self, state: CoherenceState, angle: float) -> float:
        """
        Perform measurement at given angle in coherence phase space.
        
        In UBP, measurement is a projection operator that rotates
        the coherence state in phase space.
        
        Args:
            state: CoherenceState to measure
            angle: Measurement angle (radians)
            
        Returns:
            Measurement outcome (-1 or +1, weighted by coherence)
        """
        # Measurement operator: rotation in phase space
        # Result depends on coherence projection
        phase = state.value * math.cos(angle)
        
        # Measurement outcome: sign of projection
        # Weighted by NRCI (higher coherence = more deterministic)
        threshold = (1.0 - state.nrci) * random.random()
        
        if phase > threshold:
            return +1.0
        else:
            return -1.0
    
    def calculate_correlation(self, angle_a: float, angle_b: float, 
                            num_measurements: int = 1000) -> float:
        """
        Calculate correlation E(a,b) between measurements at angles a and b.
        
        E(a,b) = average of (measurement_a × measurement_b)
        
        Args:
            angle_a: Measurement angle for particle A
            angle_b: Measurement angle for particle B
            num_measurements: Number of measurement pairs
            
        Returns:
            Correlation value E(a,b)
        """
        products = []
        
        for _ in range(num_measurements):
            # Create entangled pair
            node_a, node_b = self.create_entangled_pair()
            
            # Measure both particles
            result_a = self.measure_at_angle(node_a.coherence, angle_a)
            result_b = self.measure_at_angle(node_b.coherence, angle_b)
            
            # Calculate product
            product = result_a * result_b
            products.append(product)
            
            # Track NRCI
            self.nrci_history.append(node_a.coherence.nrci)
        
        # Correlation is average of products
        correlation = sum(products) / len(products)
        return correlation
    
    def run_chsh_test(self, num_measurements: int = 1000) -> Dict[str, Any]:
        """
        Run complete CHSH test.
        
        Calculates S = E(a,b) - E(a,b') + E(a',b) + E(a',b')
        
        Classical bound: |S| ≤ 2
        Quantum bound: |S| ≤ 2√2 ≈ 2.828
        
        Args:
            num_measurements: Number of measurements per correlation
            
        Returns:
            Dictionary with CHSH results
        """
        print(f"Running CHSH test with {num_measurements} measurements per correlation...")
        print()
        
        start_time = time.time()
        
        # Calculate all four correlations
        print("Calculating E(a,b)...")
        E_ab = self.calculate_correlation(self.angle_a, self.angle_b, num_measurements)
        self.correlations['ab'].append(E_ab)
        print(f"  E(a,b) = {E_ab:.6f}")
        
        print("Calculating E(a,b')...")
        E_ab_prime = self.calculate_correlation(self.angle_a, self.angle_b_prime, num_measurements)
        self.correlations['ab_prime'].append(E_ab_prime)
        print(f"  E(a,b') = {E_ab_prime:.6f}")
        
        print("Calculating E(a',b)...")
        E_a_prime_b = self.calculate_correlation(self.angle_a_prime, self.angle_b, num_measurements)
        self.correlations['a_prime_b'].append(E_a_prime_b)
        print(f"  E(a',b) = {E_a_prime_b:.6f}")
        
        print("Calculating E(a',b')...")
        E_a_prime_b_prime = self.calculate_correlation(self.angle_a_prime, self.angle_b_prime, num_measurements)
        self.correlations['a_prime_b_prime'].append(E_a_prime_b_prime)
        print(f"  E(a',b') = {E_a_prime_b_prime:.6f}")
        
        # Calculate CHSH parameter S
        S = E_ab - E_ab_prime + E_a_prime_b + E_a_prime_b_prime
        self.chsh_values.append(S)
        
        elapsed = time.time() - start_time
        
        # Determine violation
        classical_bound = 2.0
        quantum_bound = 2.0 * math.sqrt(2.0)  # Tsirelson bound
        
        violates_classical = abs(S) > classical_bound
        violates_quantum = abs(S) > quantum_bound
        
        print()
        print("=" * 70)
        print("CHSH TEST RESULTS")
        print("=" * 70)
        print(f"S = E(a,b) - E(a,b') + E(a',b) + E(a',b')")
        print(f"S = {E_ab:.6f} - {E_ab_prime:.6f} + {E_a_prime_b:.6f} + {E_a_prime_b_prime:.6f}")
        print(f"S = {S:.6f}")
        print()
        print(f"Classical bound: |S| ≤ {classical_bound:.6f}")
        print(f"Quantum bound (Tsirelson): |S| ≤ {quantum_bound:.6f}")
        print()
        print(f"Violates classical bound: {violates_classical}")
        print(f"Violates quantum bound: {violates_quantum}")
        print()
        print(f"Mean NRCI: {sum(self.nrci_history) / len(self.nrci_history):.6f}")
        print(f"Elapsed time: {elapsed:.2f} seconds")
        print("=" * 70)
        print()
        
        return {
            'S': S,
            'E_ab': E_ab,
            'E_ab_prime': E_ab_prime,
            'E_a_prime_b': E_a_prime_b,
            'E_a_prime_b_prime': E_a_prime_b_prime,
            'classical_bound': classical_bound,
            'quantum_bound': quantum_bound,
            'violates_classical': violates_classical,
            'violates_quantum': violates_quantum,
            'mean_nrci': sum(self.nrci_history) / len(self.nrci_history),
            'num_measurements': num_measurements,
            'elapsed_time': elapsed
        }
    
    def run_statistical_study(self, num_trials: int = 10, 
                            measurements_per_trial: int = 1000) -> Dict[str, Any]:
        """
        Run multiple CHSH tests for statistical analysis.
        
        Args:
            num_trials: Number of independent CHSH tests
            measurements_per_trial: Measurements per correlation per trial
            
        Returns:
            Statistical results
        """
        print("=" * 70)
        print("STATISTICAL CHSH STUDY")
        print("=" * 70)
        print(f"Trials: {num_trials}")
        print(f"Measurements per trial: {measurements_per_trial}")
        print()
        
        all_results = []
        
        for trial in range(num_trials):
            print(f"Trial {trial + 1}/{num_trials}")
            print("-" * 70)
            
            result = self.run_chsh_test(measurements_per_trial)
            all_results.append(result)
        
        # Statistical analysis
        S_values = [r['S'] for r in all_results]
        mean_S = sum(S_values) / len(S_values)
        variance_S = sum((s - mean_S) ** 2 for s in S_values) / len(S_values)
        std_S = math.sqrt(variance_S)
        
        violation_rate = sum(1 for r in all_results if r['violates_classical']) / len(all_results)
        
        print("=" * 70)
        print("STATISTICAL SUMMARY")
        print("=" * 70)
        print(f"Mean S: {mean_S:.6f}")
        print(f"Std S: {std_S:.6f}")
        print(f"Min S: {min(S_values):.6f}")
        print(f"Max S: {max(S_values):.6f}")
        print(f"Violation rate: {violation_rate * 100:.1f}%")
        print("=" * 70)
        print()
        
        return {
            'num_trials': num_trials,
            'measurements_per_trial': measurements_per_trial,
            'mean_S': mean_S,
            'std_S': std_S,
            'min_S': min(S_values),
            'max_S': max(S_values),
            'violation_rate': violation_rate,
            'all_results': all_results
        }
    
    def export_results(self, results: Dict[str, Any], filename: str):
        """Export study results to JSON."""
        with open(filename, 'w') as f:
            json.dump(results, f, indent=2)
        
        print(f"✅ Results exported to {filename}")


def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description='CHSH Entanglement Test Study')
    parser.add_argument('--backend', choices=['cpu', 'metal'], default='cpu',
                        help='Taichi backend')
    parser.add_argument('--trials', type=int, default=10,
                        help='Number of CHSH test trials')
    parser.add_argument('--measurements', type=int, default=1000,
                        help='Measurements per correlation per trial')
    parser.add_argument('--export', type=str, default='chsh_results.json',
                        help='Export filename')
    
    args = parser.parse_args()
    
    # Create study
    study = CHSHEntanglementStudy(backend=args.backend)
    
    # Run statistical study
    results = study.run_statistical_study(
        num_trials=args.trials,
        measurements_per_trial=args.measurements
    )
    
    # Export results
    study.export_results(results, args.export)
    
    # Print conclusion
    print()
    print("=" * 70)
    print("CONCLUSION")
    print("=" * 70)
    
    if results['violation_rate'] > 0.5:
        print("✅ UBP coherence states exhibit quantum-like correlations")
        print("   that violate the CHSH inequality, suggesting entanglement")
        print("   emerges from geometric coherence in the UBP framework.")
    else:
        print("❌ No significant CHSH violation detected.")
        print("   Classical correlations dominate in this regime.")
    
    print()
    print(f"Mean S = {results['mean_S']:.6f} ± {results['std_S']:.6f}")
    print(f"Classical bound: 2.0")
    print(f"Quantum bound: {2 * math.sqrt(2):.6f}")
    print("=" * 70)


if __name__ == '__main__':
    main()
