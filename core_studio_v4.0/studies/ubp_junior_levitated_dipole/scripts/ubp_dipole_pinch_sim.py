import random
from fractions import Fraction
from ubp_core_v5_3_merged import GOLAY_ENGINE, LEECH_ENGINE, UBPUltimateSubstrate

class DipolePinchSimulator:
    def __init__(self, num_particles=1000):
        self.num_particles = num_particles
        self.particles = []
        self.ideal_state = GOLAY_ENGINE.get_octads()[0] # The "Core"
        self.Y = UBPUltimateSubstrate.get_constants()['Y']
        
        # Initialize random plasma (high entropy)
        for _ in range(num_particles):
            self.particles.append([random.randint(0, 1) for _ in range(24)])

    def _apply_turbulence(self, vector, intensity=0.1):
        """Simulates thermal noise/turbulence."""
        new_vec = list(vector)
        for i in range(24):
            if random.random() < intensity:
                new_vec[i] = 1 - new_vec[i] # Bit flip
        return new_vec

    def _apply_supports(self, vector):
        """Simulates mechanical supports (Grounding/Loss)."""
        # Supports physically touch the plasma, resetting coherence.
        # If a particle hits a support (random chance), it is lost/randomized.
        if random.random() < 0.3: # 30% loss probability per step
            return [random.randint(0, 1) for _ in range(24)]
        return vector

    def _apply_pinch(self, vector, efficiency=1.0):
        """
        The 'Pinch' is the Golay Engine correcting errors.
        It pulls noisy vectors back to the Ideal State.
        """
        # Decode: Find the nearest valid geometric state
        decoded, correctable, _ = GOLAY_ENGINE.decode(vector)
        
        if correctable and random.random() < efficiency:
            # Snap to the grid (Centripetal Force)
            return GOLAY_ENGINE.encode(decoded)
        return vector

    def run_scenario(self, mode, steps=50):
        print(f"\n--- RUNNING SCENARIO: {mode} ---")
        # Reset plasma
        self.particles = [[random.randint(0, 1) for _ in range(24)] for _ in range(self.num_particles)]
        
        for step in range(steps):
            core_density = 0
            
            for i in range(self.num_particles):
                # 1. Turbulence (Universal)
                self.particles[i] = self._apply_turbulence(self.particles[i])
                
                # 2. Mode-Specific Physics
                if mode == "SUPPORTED":
                    self.particles[i] = self._apply_supports(self.particles[i])
                    # Weak Pinch (Interrupted by supports)
                    self.particles[i] = self._apply_pinch(self.particles[i], efficiency=0.2)
                    
                elif mode == "LEVITATED":
                    # No supports. Strong Pinch.
                    self.particles[i] = self._apply_pinch(self.particles[i], efficiency=0.8)
                    
                elif mode == "UBP_RESONANT":
                    # Tuned Levitation: The field oscillates at Y-Frequency.
                    # This creates a "Pump" effect, increasing pinch efficiency to near 100%
                    # and actively guiding vectors to the specific Ideal State.
                    self.particles[i] = self._apply_pinch(self.particles[i], efficiency=0.99)
                    
                    # Harmonic Tuning: Bias towards the specific Ideal Octad
                    if random.random() < float(self.Y):
                        self.particles[i] = list(self.ideal_state)

                # 3. Measure Coherence (Is it the Ideal State?)
                if self.particles[i] == self.ideal_state:
                    core_density += 1
            
            # Report periodically
            if step % 10 == 0 or step == steps - 1:
                density_pct = (core_density / self.num_particles) * 100
                bar = "█" * int(density_pct / 5)
                print(f"Step {step:02d}: Density {density_pct:5.1f}% | {bar}")
        
        return core_density / self.num_particles

def main():
    sim = DipolePinchSimulator(num_particles=2000)
    
    # 1. The "Junior" Baseline (Supported)
    d_supp = sim.run_scenario("SUPPORTED")
    
    # 2. The "Junior" Breakthrough (Levitated)
    d_lev = sim.run_scenario("LEVITATED")
    
    # 3. The UBP Proposal (Resonant)
    d_res = sim.run_scenario("UBP_RESONANT")
    
    print("\n=== FINAL ANALYSIS ===")
    print(f"1. Supported Density: {d_supp:.1%} (Entropy Dominates)")
    print(f"2. Levitated Density: {d_lev:.1%} (The 'Pinch' Effect)")
    print(f"3. UBP Resonant Density: {d_res:.1%} (Harmonic Tuning)")
    
    gain_lev = d_lev / d_supp if d_supp > 0 else 0
    gain_ubp = d_res / d_lev if d_lev > 0 else 0
    
    print(f"\n>> Gain from Levitation: {gain_lev:.1f}x")
    print(f">> Potential Gain from UBP Tuning: {gain_ubp:.1f}x")

if __name__ == "__main__":
    main()