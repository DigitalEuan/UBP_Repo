"""
Study: UBP Master Engine v4.1.60 (Consolidated)
Description: The definitive float-free implementation of the Extended G24 Substrate.
Consolidates: study_11, study_12, study_13, study_14, and study_15.
"""
import ubp_core
from ubp_core import save_scene_3d
from metrics import METRICS

class UBPMasterEngine:
    def __init__(self):
        self.G24_POLY = 0xC75 # Standard Golay Generator

    def manifest(self, data_12bit):
        """Manifests 12-bit data into a 24-bit OnBit codeword (Tension 0)."""
        data = data_12bit & 0xFFF
        # 1. Calculate G23 Parity (11 bits)
        reg = data << 11
        for i in range(12):
            if reg & (1 << (22 - i)):
                reg ^= (self.G24_POLY << (11 - i))
        
        # 2. Combine to 23-bit word and add 24th-bit Overall Parity
        codeword_23 = (data << 11) | reg
        parity_bit = 1 if (bin(codeword_23).count('1') % 2 != 0) else 0
        return (codeword_23 << 1) | parity_bit

    def verify_tension(self, codeword):
        """Returns the informational tension (0 = Perfect Codeword)."""
        # Check G23 remainder
        c23 = codeword >> 1
        reg = c23
        for i in range(12):
            if reg & (1 << (22 - i)):
                reg ^= (self.G24_POLY << (11 - i))
        # Check overall parity (must be even)
        weight_check = bin(codeword).count('1') % 2
        return reg + weight_check

    def analyze_identity(self, name, value):
        """Splits a 24-bit word into Phenom/Noumenal layers and checks stability."""
        data_layer = value >> 12
        shadow_layer = value & 0xFFF
        tension = self.verify_tension(value)
        
        return {
            "name": name,
            "value": value,
            "data": data_layer,
            "shadow": shadow_layer,
            "tension": tension,
            "status": "ON-BIT" if tension == 0 else "TRANSITIONAL"
        }

    def render_mog_grid(self, results):
        """Maps results to the 4x6 Miracle Octad Generator (MOG) 3D grid."""
        points = []
        for i, res in enumerate(results):
            val_bin = bin(res['value'])[2:].zfill(24)
            for bit_idx, bit in enumerate(val_bin):
                if bit == '1':
                    # Color: Cyan for stable, Red for noisy
                    color = "#00ffff" if res['status'] == "ON-BIT" else "#ff3300"
                    points.append({
                        "x": (bit_idx % 6) - 2.5,
                        "y": (bit_idx // 6) - 1.5 + (i * 5),
                        "z": res['tension'] * 0.2,
                        "color": color,
                        "size": 0.4,
                        "label": f"{res['name']} Bit {bit_idx}"
                    })
        save_scene_3d({"points": points})

def run_master_test():
    engine = UBPMasterEngine()
    
    # Test 1: Manifesting Seeds (Physics, Chem, Bio)
    seeds = [("Feynman", 137), ("Lead", 82), ("Thymine", 126)]
    manifested_results = []
    
    print(f"{'Identity':<12} | {'Manifested (Hex)':<18} | {'Tension'} | {'Status'}")
    print("-" * 65)
    
    for name, seed in seeds:
        codeword = engine.manifest(seed)
        analysis = engine.analyze_identity(name, codeword)
        manifested_results.append(analysis)
        print(f"{analysis['name']:<12} | {hex(analysis['value']):<18} | {analysis['tension']:<7} | {analysis['status']}")

    # Test 2: Lattice Integrity Check
    print("\n--- Lattice Integrity (Min Distance >= 8) ---")
    for i in range(len(manifested_results)):
        for j in range(i + 1, len(manifested_results)):
            dist = bin(manifested_results[i]['value'] ^ manifested_results[j]['value']).count('1')
            print(f"Dist({manifested_results[i]['name']}, {manifested_results[j]['name']}): {dist} bits")

    engine.render_mog_grid(manifested_results)
    print("\n[STATUS] Master Engine Test Complete. 3D Manifold updated.")

if __name__ == "__main__":
    run_master_test()