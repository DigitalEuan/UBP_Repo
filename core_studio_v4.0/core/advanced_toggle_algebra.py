"""
UBP Study 2: Advanced Toggle Algebra (Float-Free Port)
======================================================
Adapts legacy 'toggle_ops.py' to v4.2.6 Rational Standards.
Replaces transcendental functions with rational approximations.

E R A Craig, New Zealand
UBP Research Cortex v4.2.6
16 Jan 2026
"""
from fractions import Fraction
from ubp_core_v5_3_merged import UBPUltimateSubstrate, BinaryLinearAlgebra

class RationalMath:
    """Deterministic approximations for transcendental functions."""
    
    @staticmethod
    def e_approx(terms=10) -> Fraction:
        """Rational approximation of e using Taylor series."""
        e = Fraction(1, 1)
        fact = 1
        for i in range(1, terms + 1):
            fact *= i
            e += Fraction(1, fact)
        return e

    @staticmethod
    def exp_decay_rational(val: int, decay_factor: Fraction) -> int:
        """
        Approximates val * e^(-decay) using (1 - decay)^n expansion 
        or simple rational scaling for small decay.
        For v4.2.6, we use the linear approximation for stability: 
        val * (1 - decay)
        """
        if decay_factor >= 1: return 0
        res = int(val * (1 - decay_factor))
        return max(0, res)

class AdvancedToggleAlgebra:
    def __init__(self):
        self.constants = UBPUltimateSubstrate.get_constants()
        self.E = RationalMath.e_approx()
        self.MAX_VAL = 0xFFFFFF # 24-bit limit

    def resonance_toggle(self, b_i: int, freq: Fraction, time: Fraction) -> int:
        """
        Legacy: b_i * exp(-k * (t*f)^2)
        v4.2.6: b_i * (1 - (t*f*k_rational))
        """
        # Rational decay constant derived from Y (Observer Drag)
        k = self.constants['Y'] / 1000 
        d = (time * freq)
        decay = d * k
        return RationalMath.exp_decay_rational(b_i, decay)

    def entanglement_toggle(self, b_i: int, b_j: int, coherence: Fraction) -> int:
        """
        Legacy: b_i * b_j * C_ij
        v4.2.6: (b_i & b_j) scaled by coherence if C > 0.95
        """
        # Entanglement implies shared state (AND), not multiplication (which explodes values)
        # We use bitwise AND to represent the shared geometry
        shared = b_i & b_j
        if coherence >= Fraction(95, 100):
            return int(shared * coherence)
        return int(shared * coherence * Fraction(1, 10))

    def spin_transition(self, b_i: int, p_s: Fraction) -> int:
        """
        Legacy: b_i * ln(1/p_s)
        v4.2.6: b_i * (1/p_s - 1) approximation for entropy scaling
        Actually, ln(1/x) is roughly (1/x - 1) for x near 1, 
        but for small p_s (like e/12), we use a lookup or geometric series.
        
        Quantum Spin (p_s = e/12):
        1/p_s = 12/e approx 4.41
        ln(4.41) approx 1.48
        
        We will use the rational scalar directly.
        """
        # Calculate scalar: 1/p_s scaled down to log range
        # Simple rational map: scalar = (1/p_s) / e
        scalar = (Fraction(1, 1) / p_s) / self.E
        res = int(b_i * scalar)
        return min(res, self.MAX_VAL)

    def tgic_router(self, x: bool, y: bool, z: bool, b_i: int, b_j: int) -> int:
        """
        Routes operation based on 3D coordinate state (TGIC).
        """
        if x and y and z:
            # (1,1,1) -> Hybrid XOR (High Energy)
            # XOR then Decay
            xor_val = b_i ^ b_j
            return self.resonance_toggle(xor_val, Fraction(1,1), Fraction(1,1))
        elif x and y and not z:
            # (1,1,0) -> Resonance
            return self.resonance_toggle(b_i, Fraction(432, 1), Fraction(1, 100))
        elif x and not y and z:
            # (1,0,1) -> Entanglement
            return self.entanglement_toggle(b_i, b_j, Fraction(99, 100))
        else:
            # Default -> XOR
            return b_i ^ b_j

def run_study():
    print("--- UBP STUDY 2: ADVANCED TOGGLES (FLOAT-FREE) ---")
    ata = AdvancedToggleAlgebra()
    
    # Test Values (24-bit integers)
    val_a = 0b101010101010101010101010 # 11184810
    val_b = 0b110011001100110011001100 # 13421772
    
    # 1. Resonance
    res = ata.resonance_toggle(val_a, Fraction(10,1), Fraction(1,1))
    print(f"1. Resonance (Decay): {val_a} -> {res}")
    
    # 2. Entanglement
    ent = ata.entanglement_toggle(val_a, val_b, Fraction(99, 100))
    print(f"2. Entanglement (High C): {ent}")
    
    # 3. Spin Transition (Quantum)
    p_quantum = ata.E / 12
    spin = ata.spin_transition(val_a, p_quantum)
    print(f"3. Spin Transition (Quantum): {val_a} -> {spin}")
    
    # 4. TGIC Routing
    tgic_res = ata.tgic_router(True, False, True, val_a, val_b)
    print(f"4. TGIC (1,0,1 -> Entangle): {tgic_res}")

if __name__ == "__main__":
    run_study()