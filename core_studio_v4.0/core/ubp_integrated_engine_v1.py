"""
UBP Integrated Reflexive Engine v1.0
====================================
Combines:
- ReflexiveVM: Self-healing virtual machine using Golay codewords as opcodes
- SemanticCortex: Multi-modal concept learner with Golay-snapped chords
- HorizonMonitor: Topological diagnostic for system stability

All components now live in a single file for easy development and demonstration.
A unified demo at the bottom shows each part working and lightly integrated.

Author: Euan R A Craig, New Zealand
Date: 06 January 2026

"""

import hashlib
import math
import keyword
# NOTE: These imports assume your existing ubp_core_v4_2_6_COMBINED module is available
#       It must provide: GOLAY_DECODER and BinaryLinearAlgebra
from ubp_core_v4_2_6_COMBINED import GOLAY_DECODER, BinaryLinearAlgebra


# =============================================================================
# 1. Reflexive Virtual Machine (Self-Healing Execution)
# =============================================================================
class ReflexiveVM:
    def __init__(self):
        self.decoder = GOLAY_DECODER
        self.codewords = self.decoder.get_all_codewords()
        
        # Fixed ISA using selected codewords
        self.ISA = {
            tuple(self.codewords[10]): self._add,
            tuple(self.codewords[50]): self._sub,
            tuple(self.codewords[100]): self._mul
        }
        
        self.OP_NAMES = {
            tuple(self.codewords[10]): "ADD",
            tuple(self.codewords[50]): "SUB",
            tuple(self.codewords[100]): "MUL"
        }

    def _add(self, a, b): return a + b
    def _sub(self, a, b): return a - b
    def _mul(self, a, b): return a * b

    def execute(self, instruction_vector, a, b):
        vec_list = list(instruction_vector)
        _, _, syndrome = self.decoder.decode(vec_list)
        
        print(f"[VM] Syndrome: {syndrome}")
        
        if syndrome > 0:
            print(f"   ⚠️  CORRUPTION DETECTED → Repairing...")
            message, correctable, _ = self.decoder.decode(vec_list)
            
            if not correctable:
                print(f"   ❌  FATAL: Unrepairable (syndrome > 3)")
                return None
                
            healed_vec = self.decoder.encode(message)
            print(f"   ✅  REPAIRED → Snapped to valid opcode")
            final_vec = tuple(healed_vec)
        else:
            print(f"   ✅  Instruction valid")
            final_vec = tuple(vec_list)

        if final_vec in self.ISA:
            op_name = self.OP_NAMES[final_vec]
            result = self.ISA[final_vec](a, b)
            print(f"   [EXEC] {op_name}({a}, {b}) = {result}")
            return result
        else:
            print(f"   ❌  Unknown opcode (even after repair)")
            return None


# =============================================================================
# 2. Semantic Cortex (Concept Learning & Resonance)
# =============================================================================
class SemanticCortex:
    def __init__(self):
        self.golay = GOLAY_DECODER
        self.memory = {}

    def _generate_vector(self, tag_string):
        h = hashlib.sha256(tag_string.encode('utf-8')).hexdigest()
        val = int(h[:6], 16)
        raw_vec = [(val >> i) & 1 for i in range(23, -1, -1)]
        corrected, _, _ = self.golay.decode(raw_vec)
        return corrected

    def _analyze_number(self, n):
        tags = ["NUMBER"]
        if n % 2 == 0: tags.append("EVEN")
        else: tags.append("ODD")
        if n > 1:
            is_prime = all(n % i != 0 for i in range(2, int(math.sqrt(n)) + 1))
            if is_prime: tags.append("PRIME")
        return tags, "MATH"

    def _analyze_word(self, word):
        tags = ["WORD"]
        w = word.lower()
        if w.endswith("ing"): tags.append("VERB_PARTICIPLE")
        elif w.endswith("ed"): tags.append("VERB_PAST")
        elif w.endswith("ly"): tags.append("ADVERB")
        elif w in ["the", "a", "an"]: tags.append("DETERMINER")
        else: tags.append("NOUN_DEFAULT")
        return tags, "LANGUAGE"

    def _analyze_code(self, token):
        tags = ["CODE"]
        if keyword.iskeyword(token):
            tags.append("KEYWORD")
            if token in ["if", "else", "elif", "while", "for"]:
                tags.append("CONTROL_FLOW")
            elif token in ["def", "class", "return"]:
                tags.append("STRUCTURE")
        else:
            tags.append("IDENTIFIER")
        return tags, "PYTHON"

    def process(self, input_data):
        if isinstance(input_data, int):
            tags, context = self._analyze_number(input_data)
            label = str(input_data)
        elif isinstance(input_data, str):
            if input_data in keyword.kwlist or "(" in input_data:
                tags, context = self._analyze_code(input_data)
            else:
                tags, context = self._analyze_word(input_data)
            label = input_data
        else:
            return None

        v_syn = self._generate_vector(tags[0])
        sem_tag = tags[1] if len(tags) > 1 else tags[0]
        v_sem = self._generate_vector(sem_tag)
        v_ctx = self._generate_vector(context)

        chord = {"SYN": v_syn, "SEM": v_sem, "CTX": v_ctx, "TAGS": tags}
        self.memory[label] = chord
        return chord

    def compare(self, label_a, label_b):
        if label_a not in self.memory or label_b not in self.memory:
            return "Unknown Concept"
            
        cA = self.memory[label_a]
        cB = self.memory[label_b]
        
        d_syn = BinaryLinearAlgebra.hamming_distance(cA["SYN"], cB["SYN"])
        d_sem = BinaryLinearAlgebra.hamming_distance(cA["SEM"], cB["SEM"])
        d_ctx = BinaryLinearAlgebra.hamming_distance(cA["CTX"], cB["CTX"])
        
        total = d_syn + d_sem + d_ctx
        resonance = "HIGH" if total < 12 else "MEDIUM" if total < 24 else "LOW"
        
        return {
            "A": label_a, "B": label_b,
            "d_SYN": d_syn, "d_SEM": d_sem, "d_CTX": d_ctx,
            "total_hamming": total,
            "Resonance": resonance
        }


# =============================================================================
# 3. Horizon Monitor (System Diagnostics)
# =============================================================================
class HorizonMonitor:
    def __init__(self):
        self.HORIZONS = {
            "GENOMIC (Base-4)": 6.0,
            "BINARY (Base-2)": 12.0,
            "BIOLOGIC (Phi)": 18.0
        }
        self.Y = 0.264675
        self.SAFE_LOAD = 1.0 - self.Y

    def check(self, value, name="Metric"):
        if value <= 0: return
        
        print(f"\n[HORIZON CHECK] {name}: {value}")
        
        densities = {
            "GENOMIC": math.log(value, 4),
            "BINARY": math.log(value, 2),
            "BIOLOGIC": math.log(value, 1.61803398875)
        }
        
        for h_name, limit in self.HORIZONS.items():
            current = densities[h_name.split()[0]]
            load_pct = (current / limit) * 100
            
            if current > limit:
                status = "CRITICAL (Post-Horizon)"
                color = "RED"
            elif current > limit - 0.1:
                status = "CONTACT (Singularity)"
                color = "FLASHING RED"
            elif load_pct > self.SAFE_LOAD * 100:
                status = "WARNING (High Pressure)"
                color = "YELLOW"
            else:
                status = "STABLE"
                color = "GREEN"
                
            print(f"  > {h_name:<16} | Load: {load_pct:5.1f}% | {color} {status}")


# =============================================================================
# Unified Demonstration
# =============================================================================
def run_integrated_demo():
    print("="*50)
    print("UBP INTEGRATED REFLEXIVE ENGINE v1.0 DEMO")
    print("="*50)
    
    # Initialise components
    vm = ReflexiveVM()
    cortex = SemanticCortex()
    monitor = HorizonMonitor()
    
    # --- Semantic Cortex Growth ---
    print("\n1. SEMANTIC CORTEX: Learning concepts")
    inputs = [
        "dog", "running", "quickly", "the",
        137, 42, 2,
        "def", "return", "add", "sub", "mul"
    ]
    
    for item in inputs:
        chord = cortex.process(item)
        if chord:
            print(f"   Learned: {str(item):<10} Tags: {chord['TAGS']}")
    
    # Cortex comparisons
    print("\n   Resonance checks:")
    print("   ", cortex.compare("dog", 42))
    print("   ", cortex.compare(137, 2))
    print("   ", cortex.compare("def", "return"))
    print("   ", cortex.compare("add", "mul"))
    
    # --- Reflexive VM Tests ---
    print("\n2. REFLEXIVE VM: Self-healing execution")
    valid_add = list(vm.ISA.keys())[0]
    
    print("\n   Normal:")
    vm.execute(valid_add, 20, 7)
    
    print("\n   1-bit corruption (healed):")
    noisy = list(valid_add)
    noisy[0] = 1 - noisy[0]
    vm.execute(noisy, 20, 7)
    
    print("\n   3-bit corruption (limit - healed):")
    severe = list(valid_add)
    for i in [0, 5, 10]:
        severe[i] = 1 - severe[i]
    vm.execute(severe, 20, 7)
    
    # --- Horizon Monitoring ---
    print("\n3. HORIZON MONITOR: System diagnostics")
    monitor.check(len(cortex.memory), "Cortex Lexicon Size")
    monitor.check(137, "Fine Structure Constant")
    monitor.check(4096, "Golay Horizon")
    monitor.check(196560, "Leech Kissing Number")

if __name__ == "__main__":
    run_integrated_demo()
