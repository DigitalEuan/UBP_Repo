"""
UBP RATIONAL ENGINE v2.0 (Master Monolith)
==========================================
Combines Standards, Architect, and expanded Population logic.
This is the core 'Brain' of the Rational UBP system.
"""
import json
import os
from ubp_core_v4_2_6_COMBINED import GOLAY_DECODER, BinaryLinearAlgebra

# --- 1. STANDARDS ---
class UBPStandards:
    DOMAINS = {
        "SUBSTANCE": 0, "MECHANISM": 1, "ORGANISM": 2, "ALGORITHM": 3,
        "QUANTITY": 4, "IMPERATIVE": 5, "ENTROPY": 6, "MEANING": 7
    }
    GRAY_3BIT = [0b000, 0b001, 0b011, 0b010, 0b110, 0b111, 0b101, 0b100]
    GRAY_5BIT = [0, 1, 3, 2, 6, 7, 5, 4, 12, 13, 15, 14, 10, 11, 9, 8,
                 24, 25, 27, 26, 30, 31, 29, 28, 20, 21, 23, 22, 18, 19, 17, 16]

    @staticmethod
    def get_domain_bits(domain_name):
        val = UBPStandards.DOMAINS.get(domain_name.upper(), 0)
        return [(val >> i) & 1 for i in range(2, -1, -1)]

    @staticmethod
    def get_gray_bits(value, width=3):
        limit = (1 << width) - 1
        idx = max(0, min(limit, value))
        table = UBPStandards.GRAY_3BIT if width == 3 else UBPStandards.GRAY_5BIT
        code = table[idx] if idx < len(table) else idx
        return [(code >> i) & 1 for i in range(width-1, -1, -1)]

# --- 2. ARCHITECT ---
class ConceptArchitect:
    def __init__(self, registry_file='ubp_rational_memory.json'):
        self.golay = GOLAY_DECODER
        self.registry_file = registry_file
        self.memory = {}

    def mint(self, name, domain, p1, p2, p3=0):
        dom_bits = UBPStandards.get_domain_bits(domain)
        p1_bits = UBPStandards.get_gray_bits(p1, 3)
        p2_bits = UBPStandards.get_gray_bits(p2, 5)
        p3_bits = [p3 & 1]
        msg = dom_bits + p1_bits + p2_bits + p3_bits
        vec = self.golay.encode(msg)
        self.memory[name] = {"name": name, "domain": domain, "params": [p1, p2, p3], "vector": vec}
        return vec

    def save(self):
        with open(self.registry_file, 'w') as f:
            json.dump(self.memory, f, indent=2)

# --- 3. CORTEX ---
class RationalCortex:
    def __init__(self):
        self.arch = ConceptArchitect()
        self._populate()

    def _populate(self):
        print("[CORTEX] Expanding Rational Memory...")
        # A. Elements (Substance)
        for z in range(1, 20): # First 3 periods
            self.arch.mint(f"Element_{z}", "SUBSTANCE", (z//8), (z%18))
        
        # B. Physics (Mechanism)
        self.arch.mint("Mass", "MECHANISM", 0, 0, 0)
        self.arch.mint("Force", "MECHANISM", 0, 31, 0)
        self.arch.mint("Energy", "MECHANISM", 0, 0, 1)
        
        # C. Actions (Meaning/Imperative)
        self.arch.mint("ACTION_BIND", "MEANING", 0, 10, 1)
        self.arch.mint("ACTION_BREAK", "MEANING", 0, 10, 0)
        
        # D. Math (Quantity)
        self.arch.mint("Zero", "QUANTITY", 0, 0, 0)
        self.arch.mint("One", "QUANTITY", 0, 1, 0)
        self.arch.mint("Pi", "QUANTITY", 7, 31, 0)
        
        self.arch.save()
        print(f"✅ Memory Density Increased: {len(self.arch.memory)} concepts.")

if __name__ == "__main__":
    RationalCortex()