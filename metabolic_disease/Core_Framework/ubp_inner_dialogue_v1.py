"""
UBP Inner Dialogue Module v1.0
==============================
Implements a reflexive loop between the Semantic Cortex (Generator) 
and the TGIC Physics Engine (Critic).
"""
from fractions import Fraction

class InnerDialogue:
    def __init__(self, kernel):
        self.kernel = kernel
        self.generator = kernel.cortex
        self.critic = kernel.physics
        self.monitor = kernel.monitor
        self.threshold = Fraction(3, 1) # Convergence at Hamming Distance <= 3

    def deliberate(self, initial_query, max_turns=8):
        current_input = initial_query
        dialogue_log = [("INIT", initial_query)]
        
        print(f"\n[INNER DIALOGUE] Target: '{initial_query}'")
        
        for turn in range(1, max_turns + 1):
            # 1. GENERATION: Map input to Semantic Chord
            concept = self.generator.process_concept(current_input)
            
            # 2. CRITIQUE: Calculate Geometric Interaction Cost
            # Cost = Hamming Distance between SYN (Syntax) and SEM (Semantics)
            cost_val = self.critic.calculate_interaction_cost(concept['SYN'], concept['SEM'])
            cost = Fraction(cost_val, 1)
            
            dialogue_log.append(("CORTEX", f"Chord: {concept['TAGS']} | Cost: {cost}"))
            print(f"  Turn {turn} | Cost: {cost} | Tags: {concept['TAGS']}")

            # 3. HORIZON CHECK: Ensure we aren't hitting a Genomic/Binary limit
            self.monitor.check(turn, f"Dialogue Turn {turn}")

            # 4. CONVERGENCE LOGIC
            if cost <= self.threshold:
                dialogue_log.append(("CRITIC", "✅ COHERENCE REACHED: Snapped to valid lattice point."))
                print("  [!] Convergence Detected.")
                break

            # 5. REFINEMENT / RECALL
            if cost > 12:
                # Divergence: Trigger Memory Scavenger
                match = self.kernel.scanner.scan_and_trigger(current_input)
                if match:
                    refinement = f"RECALL TRIGGERED: {match['ubp_id']} ({match['name']})"
                else:
                    refinement = "DIVERGENCE: Re-orienting to vacuum state."
            elif cost > 6:
                refinement = f"ORTHOGONAL: Narrowing semantics for {concept['TAGS'][0]}."
            else:
                refinement = "NEAR-FIELD: Fine-tuning parity bits."

            current_input = refinement
            dialogue_log.append(("CRITIC", refinement))

        return dialogue_log[-1]