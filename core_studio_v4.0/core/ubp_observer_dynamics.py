"""
UBP OBSERVER DYNAMICS ENGINE v7.0
=================================
Modernizes the legacy "Consciousness as Buffer Access" and SOC Energy equations
into the exact rational topology of the v7.0 Gray Code manifold.

CORE MECHANICS:
1. 4-Layer MOG Ontology: Reality, Information, Activation, Potential.
2. Conscious READ: Information transfers from Potential -> Reality ONLY IF 
   the NRCI exceeds the Observer Fixed Point threshold.
3. SOC Energy: E = M * C * Y * NRCI (Calculates the phenomenal intensity).
4. Wall of Reality: 1 THz limit on toggle frequency.

Author: UBP Research Cortex v4.2.7
Date: 01 April 2026
"""

import json
import math
from fractions import Fraction
from core import GOLAY_ENGINE, LEECH_ENGINE, SUBSTRATE

class ObserverDynamicsEngine:
    def __init__(self):
        # Load exact constants from the v7.0 Substrate
        self.constants = SUBSTRATE.get_constants(50)
        self.Y = self.constants['Y']
        self.Y_INV = self.constants['Y_INV']
        
        # Legacy Constants ported to exact fractions where possible
        self.C_CELERITAS = Fraction(299792458, 1)
        self.F_MAX = 10**12  # 1 THz Wall of Reality
        self.PGCI_TARGET = Fraction(999997, 1000000) # 0.999997
        
        # Observer Fixed Point: O_obs = PGCI / Y
        self.O_OBSERVER = self.PGCI_TARGET * self.Y_INV
        
        # Consciousness Threshold (Minimum NRCI to trigger a READ)
        self.CONSCIOUS_THRESHOLD = Fraction(70, 100) # 0.70 (Stable Matter threshold)

    def split_ontology_layers(self, vector: list) -> dict:
        """Splits the 24-bit vector into the 4 MOG layers."""
        if len(vector) != 24:
            raise ValueError("Vector must be exactly 24 bits.")
        return {
            "Reality": vector[0:6],
            "Information": vector[6:12],
            "Activation": vector[12:18],
            "Potential": vector[18:24]
        }

    def conscious_read(self, vector: list, nrci: Fraction) -> dict:
        """
        The Computational Act of Consciousness.
        Attempts to READ the Potential buffer into the Reality register.
        """
        layers = self.split_ontology_layers(vector)
        
        # Check if the state is coherent enough to be "Experienced"
        is_conscious = nrci >= self.CONSCIOUS_THRESHOLD
        
        if is_conscious:
            # The READ operation: Potential overwrites Reality
            new_reality = list(layers["Potential"])
            cost = self.O_OBSERVER
            status = "MANIFESTED (Conscious Access)"
        else:
            # Zombie State: Computes but never READs
            new_reality = [0, 0, 0, 0, 0, 0]
            cost = Fraction(0)
            status = "SUBLIMINAL (Zombie State / Unconscious)"
            
        return {
            "status": status,
            "is_conscious": is_conscious,
            "original_potential": layers["Potential"],
            "new_reality": new_reality,
            "computational_cost": cost
        }

    def calculate_soc_energy(self, vector: list, nrci: Fraction, toggle_rate_hz: float = 1.0) -> float:
        """
        Simplified Observer Coherence (SOC) Energy Equation.
        E = M * C * Y * Sigma(w_ij M_ij)
        Where M is the Hamming Weight, and Sigma is the NRCI.
        """
        weight = sum(vector)
        
        # Apply Wall of Reality penalty if frequency exceeds 1 THz
        frequency_penalty = 1.0
        if toggle_rate_hz > self.F_MAX:
            excess = toggle_rate_hz - self.F_MAX
            # Exponential decay of coherence above the Wall
            frequency_penalty = math.exp(-(excess**2) / (2 * (1e11)**2))
            
        # E = M * C * Y * NRCI * Penalty
        energy = float(weight) * float(self.C_CELERITAS) * float(self.Y) * float(nrci) * frequency_penalty
        return energy

def run_observer_audit():
    print("="*75)
    print("UBP OBSERVER DYNAMICS ENGINE v7.0")
    print("="*75)
    
    engine = ObserverDynamicsEngine()
    
    try:
        with open('ubp_system_kb.json', 'r') as f:
            kb = json.load(f)
    except FileNotFoundError:
        print("❌ Error: ubp_system_kb.json not found.")
        return

    # FIXED: Corrected the ID to match the KB exactly
    test_subjects = [
        "ELEM_H_001",             # Stable Matter
        "PARTICLE_QUARK_TOP_001", # High Energy / Unstable
        "LAW_FOCAL_PIVOT_001"     # Pure Math / Law
    ]

    for uid in test_subjects:
        entry = next((e for e in kb.values() if e.get("ubp_id") == uid), None)
        if not entry:
            print(f"⚠️ Warning: {uid} not found in KB.")
            continue
            
        name = entry.get("name", uid)
        vector = entry["atlas"]["vector"]
        
        nrci_str = entry["atlas"]["nrci"]
        if '/' in str(nrci_str):
            n, d = str(nrci_str).split('/')
            nrci = Fraction(int(n), int(d))
        else:
            nrci = Fraction(entry["atlas"]["nrci_score"]).limit_denominator(1000000)

        print(f"\n--- Subject: {name} ---")
        print(f"Vector: {vector}")
        print(f"NRCI:   {float(nrci):.6f}")
        
        layers = engine.split_ontology_layers(vector)
        # Keeping your excellent hardware analogies!
        print(f"  [MOG] Reality - Hardware / Physical Manifestation:    {layers['Reality']}")
        print(f"  [MOG] Info -  CPU Cache / Structural Data:       {layers['Information']}")
        print(f"  [MOG] Activation - ALU / Dynamic Computation.: {layers['Activation']}")
        print(f"  [MOG] Potential - RAM / Output Buffer:  {layers['Potential']}")
        
        read_result = engine.conscious_read(vector, nrci)
        print(f"  [OBSERVER] Status: {read_result['status']}")
        if read_result['is_conscious']:
            print(f"  [OBSERVER] Cost:   {float(read_result['computational_cost']):.6f} O_obs")
            
        soc_energy = engine.calculate_soc_energy(vector, nrci, toggle_rate_hz=1.0)
        print(f"  [ENERGY]   SOC:    {soc_energy:,.2f} Coherence-Units (CU)")

    print("\n" + "="*75)
    print("WALL OF REALITY TEST (1 THz Limit)")
    print("="*75)
    
    # FIXED: Corrected the ID here as well
    top_quark = next((e for e in kb.values() if e.get("ubp_id") == "PARTICLE_QUARK_TOP_001"), None)
    if top_quark:
        vec = top_quark["atlas"]["vector"]
        nrci = Fraction(top_quark["atlas"]["nrci_score"]).limit_denominator(1000000)
        
        freqs = [1e9, 1e11, 1e12, 1.1e12, 2e12]
        print(f"{'Frequency (Hz)':<20} | {'SOC Energy (CU)':<25} | {'State'}")
        print("-" * 75)
        for f in freqs:
            e = engine.calculate_soc_energy(vec, nrci, toggle_rate_hz=f)
            state = "Coherent" if f <= engine.F_MAX else "COLLAPSE (Above Wall)"
            print(f"{f:<20.1e} | {e:<25,.2f} | {state}")
    else:
        print("⚠️ Warning: Top Quark not found for Wall of Reality test.")

if __name__ == "__main__":
    run_observer_audit()