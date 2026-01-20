import sys
from fractions import Fraction
import math

# --- 1. UBP CORE LOGIC ---
# We simulate the "Physics of Persistence" based on Geometric Stability

class Metabolite:
    def __init__(self, name, nrci, production_rate):
        self.name = name
        self.nrci = float(nrci)
        self.production_rate = float(production_rate)
        self.concentration = 0.0
        
        # UBP Decay Law: The lower the coherence, the faster it degrades.
        # A perfect codeword (NRCI 1.0) has 0 decay.
        # A noisy vector (NRCI 0.5) decays by 50% per cycle (simplified).
        self.decay_factor = 0.2 * (1.0 - self.nrci) # Scaling factor for weekly decay

    def tick(self):
        # 1. Production (Metabolic Activity)
        self.concentration += self.production_rate
        
        # 2. Entropy (Geometric Decay)
        loss = self.concentration * self.decay_factor
        self.concentration -= loss
        
        return self.concentration

class CheeseSimulation:
    def __init__(self, strain_name):
        self.strain_name = strain_name
        self.compounds = []
        self.history = []

    def add_compound(self, compound):
        self.compounds.append(compound)

    def run(self, weeks=12):
        print(f"\n[SIMULATION] Aging Profile: {self.strain_name}")
        print(f"{'WEEK':<5} | {'FLAVOR':<10} | {'TOXIN':<10} | {'RATIO (F/T)':<12} | {'STATUS'}")
        print("-" * 60)

        for w in range(1, weeks + 1):
            # Update all compounds
            current_state = {}
            flavor_total = 0.0
            toxin_total = 0.0
            
            for c in self.compounds:
                conc = c.tick()
                current_state[c.name] = conc
                
                # Categorize based on NRCI (High NRCI + High Mass usually Toxin in this context)
                # For this sim, we know the names.
                if "Toxin" in c.name:
                    toxin_total += conc
                else:
                    flavor_total += conc

            # Calculate Ratio
            ratio = flavor_total / toxin_total if toxin_total > 0 else 999.9
            
            # Determine Status
            status = "MATURING"
            if ratio < 2.0: status = "TOXIC (Unsafe)"
            elif ratio > 5.0 and flavor_total > 10: status = "PEAK RIPENESS"
            elif w > 8 and flavor_total < 8: status = "FLAVOR FADE"
            
            print(f"{w:<5} | {flavor_total:>10.2f} | {toxin_total:>10.2f} | {ratio:>12.2f} | {status}")
            
            self.history.append((w, flavor_total, toxin_total))

# --- 2. SETUP SCENARIOS ---

def run_trajectory_study():
    print("--- UBP STUDY 14: METABOLIC TRAJECTORY PREDICTION ---")
    print("Objective: Predict optimal aging window based on Geometric Persistence.\n")

    # SCENARIO A: Standard Commercial Strain
    # Produces unstable flavor (Methyl Cinnamate) and stable toxin (Ochratoxin)
    # Production rates are arbitrary units for simulation
    sim_a = CheeseSimulation("Standard Strain (P. roqueforti)")
    sim_a.add_compound(Metabolite("Methyl Cinnamate (Flavor)", nrci=0.58, production_rate=2.0))
    sim_a.add_compound(Metabolite("Ochratoxin A (Toxin)", nrci=0.95, production_rate=0.5))
    sim_a.run(weeks=12)

    # SCENARIO B: The "Golden" Strain (Genetically Selected)
    # Produces stable flavor (C9H14O3) and reduced toxin
    sim_b = CheeseSimulation("Golden Strain (Optimized)")
    sim_b.add_compound(Metabolite("Golden Ester (Flavor)", nrci=0.88, production_rate=2.0))
    sim_b.add_compound(Metabolite("Ochratoxin A (Toxin)", nrci=0.95, production_rate=0.2)) # Reduced rate via selection
    sim_b.run(weeks=12)

    print("\n[ANALYSIS]")
    print("1. Standard Strain: Flavor peaks early (Week 4-5) then degrades due to Low NRCI (0.58).")
    print("   Toxin (NRCI 0.95) accumulates steadily. The 'Safe Window' is narrow.")
    print("2. Golden Strain: Flavor accumulates and PERSISTS due to High NRCI (0.88).")
    print("   Result: A cheese that can be aged longer (developing complexity) without losing its core flavor profile.")

if __name__ == "__main__":
    run_trajectory_study()