import random
from fractions import Fraction
from ubp_core_v5_3_merged import GOLAY_ENGINE, LEECH_ENGINE, UBPUltimateSubstrate

class SuperconductingDipoleSim:
    def __init__(self, num_particles=2000):
        self.num_particles = num_particles
        # The Superconducting Anchor (A perfect weight-8 Octad)
        self.anchor = GOLAY_ENGINE.get_octads()[0] 
        self.Y = float(UBPUltimateSubstrate.get_constants()['Y'])
        
    def run_scenario(self, mode, steps=50):
        print(f"\n--- SCENARIO: {mode} ---")
        # Initialize plasma with random noise
        particles = [[random.randint(0, 1) for _ in range(24)] for _ in range(self.num_particles)]
        
        for step in range(steps):
            core_density = 0
            for i in range(self.num_particles):
                v = particles[i]
                
                # 1. Apply Universal Entropy (Turbulence)
                # In a Superconducting field, entropy is reduced near the anchor
                dist_to_anchor = sum(1 for a, b in zip(v, self.anchor) if a != b)
                
                # LAW_INTERFERENCE_SHIELD: Turbulence is filtered by proximity to Anchor
                noise_reduction = 1.0 if dist_to_anchor > 3 else self.Y
                if random.random() < (0.1 * noise_reduction):
                    idx = random.randint(0, 23)
                    v[idx] = 1 - v[idx]

                # 2. Mode-Specific Physics
                if mode == "LEVITATED_NORMAL":
                    # Standard error correction (The Junior Experiment)
                    decoded, correctable, _ = GOLAY_ENGINE.decode(v)
                    if correctable: v = GOLAY_ENGINE.encode(decoded)
                    
                elif mode == "LEVITATED_SUPERCONDUCTING":
                    # LAW_SINK_001: The Superconducting Grip
                    # If within correction radius, the particle "snaps" and stays
                    if dist_to_anchor <= 3:
                        v = list(self.anchor) # Perfect locking
                    else:
                        decoded, correctable, _ = GOLAY_ENGINE.decode(v)
                        if correctable: v = GOLAY_ENGINE.encode(decoded)

                elif mode == "UBP_QUANTUM_PINCH":
                    # Resonant Tuning + Superconducting Grip
                    # The field "breathes" at Y-frequency, actively pulling noise into the sink
                    if dist_to_anchor <= 8: # Wider capture zone due to resonance
                        v = list(self.anchor)
                    if random.random() < self.Y:
                        v = list(self.anchor)

                particles[i] = v
                if v == self.anchor:
                    core_density += 1

            if step % 10 == 0 or step == steps - 1:
                pct = (core_density / self.num_particles) * 100
                print(f"Step {step:02d}: Core Coherence {pct:5.1f}% | {'█' * int(pct/5)}")
        
        return core_density / self.num_particles

sim = SuperconductingDipoleSim()
sim.run_scenario("LEVITATED_NORMAL")
sim.run_scenario("LEVITATED_SUPERCONDUCTING")
sim.run_scenario("UBP_QUANTUM_PINCH")