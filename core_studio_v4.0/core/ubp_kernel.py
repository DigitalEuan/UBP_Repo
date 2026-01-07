"""
UBP KERNEL v2.1.1 (STABLE PRODUCTION)
=====================================
Integrates:
1. NativeCortex V2 (Recursive, Dimensional Integrity)
2. Hybrid Resonance (Jaccard + Hamming)
3. Inner Dialogue (Discrete Thresholds, Loop Breaking)

Author: Euan R. A. Craig, New Zealand
Date: 07 January 2026
"""

import sys
import hashlib
import re
import keyword
from fractions import Fraction
from typing import List, Dict, Any, Tuple, Optional

# --- CORE DEPENDENCIES ---
try:
    from ubp_core_v4_2_6_COMBINED import GOLAY_DECODER, BinaryLinearAlgebra
    from hex_dictionary_v4_exact import HEX_DB_EXACT
    from ubp_tgic_engine import TGICExactEngine
    from ubp_horizon_monitor import HorizonMonitor
    IMPORTS_OK = True
except ImportError as e:
    print(f"[KERNEL PANIC] Critical Import Failed: {e}")
    IMPORTS_OK = False

# ==============================================================================
# MODULE 1: MOG OFFBIT STRUCTURE
# ==============================================================================
class OffBitMOG:
    def __init__(self, vector_24: List[int]):
        if len(vector_24) != 24:
            vector_24 = (vector_24 + [0]*24)[:24]
        self.vector = vector_24
        self.layers = {
            "REALITY": vector_24[0:6],
            "INFO":    vector_24[6:12],
            "ACTIVE":  vector_24[12:18],
            "POTENT":  vector_24[18:24]
        }

    def get_health_report(self) -> Dict[str, Any]:
        report = {}
        for name, bits in self.layers.items():
            weight = sum(bits)
            status = "STABLE" if weight <= 3 else "ACTIVE/NOISY"
            report[name] = {"weight": weight, "status": status}
        
        col_parity = []
        for i in range(6):
            col_sum = sum(self.layers[L][i] for L in self.layers)
            col_parity.append(col_sum % 2)
        report["VERTICAL_PARITY"] = col_parity
        report["IS_BALANCED"] = sum(col_parity) == 0
        return report

# ==============================================================================
# MODULE 2: NATIVE CORTEX V2
# ==============================================================================
class NativeCortexV2:
    def __init__(self):
        self.golay = GOLAY_DECODER
        self.LEXICON = {
            "control": ["CONTROL", "SYSTEM"],
            "feedback": ["CONTROL", "FEEDBACK"],
            "refinement": ["CONTROL", "REFINEMENT"],
            "orthogonal": ["GEOMETRY", "DIRECTION", "90_DEG"],
            "divergent": ["SYSTEM", "STATUS", "WARNING"],
            "coherent": ["SYSTEM", "STATUS", "STABLE"],
            "recall": ["MEMORY", "ACTION", "RETRIEVAL"],
            "near-field": ["GEOMETRY", "PROXIMITY", "FINE_TUNING"],
            "time": ["CONCEPT", "TEMPORAL", "FLOW"],
            "lattice": ["GEOMETRY", "STRUCTURE", "LEECH"],
            "golay": ["GEOMETRY", "CODE", "PERFECT"],
            "matter": ["PHYSICS", "SUBSTRATE", "PHENOMENAL"],
            "information": ["CONCEPT", "NOUMENAL", "DATA"],
            "codeword": ["GEOMETRY", "TARGET", "STABLE"],
            "error": ["SYSTEM", "METRIC", "SYNDROME"],
            "cost": ["SYSTEM", "METRIC", "HAMMING"],
            "nature": ["CONCEPT", "ONTOLOGY", "SOURCE"],
            "principle": ["LAW", "AXIOM", "TRUTH"],
            "reality": ["REALITY", "PHYSICS", "EXISTENCE"],
            "system": ["SYSTEM", "STRUCTURE", "ORDER"]
        }

    def _hash_to_vector(self, tag: str) -> List[int]:
        h = hashlib.sha256(tag.encode('utf-8')).hexdigest()
        val = int(h[:6], 16)
        raw = [(val >> i) & 1 for i in range(23, -1, -1)]
        # LAW_KERNEL_DIMENSION_001: Encode(Decode(Raw))
        seed, _, _ = self.golay.decode(raw)
        return self.golay.encode(seed)

    def _analyze_content(self, text: str) -> Tuple[List[str], str]:
        text_lower = text.lower()
        tags = []
        if ":" in text and (text.startswith("ORTHOGONAL") or text.startswith("DIVERGENT") or text.startswith("RECALL")):
            return ["CONTROL", "FEEDBACK", "REFINEMENT"], "SYSTEM"
        for key, specific_tags in self.LEXICON.items():
            if key in text_lower: tags.extend(specific_tags)
        if not tags:
            if text in keyword.kwlist: return ["CODE", "KEYWORD"], "PYTHON"
            tags.append("PHRASE" if " " in text else "WORD")
            tags.append("PROPER_NOUN" if text and text[0].isupper() else "GENERAL")
        return list(set(tags)), "LANGUAGE"

    def process_concept(self, concept_input: Any) -> Dict[str, Any]:
        if isinstance(concept_input, str):
            tags, context = self._analyze_content(concept_input)
        elif isinstance(concept_input, (int, float)):
            tags, context = ["NUMBER", "QUANTITY"], "MATH"
        else:
            tags, context = ["DATA", "RAW"], "BINARY"

        v_syn = self._hash_to_vector(tags[0])
        content_str = str(concept_input)
        content_hash = int(hashlib.sha256(content_str.encode()).hexdigest()[:6], 16)
        raw_sem_bits = [(content_hash >> i) & 1 for i in range(23, -1, -1)]
        # Identity Anchor
        seed, _, _ = self.golay.decode(raw_sem_bits) 
        v_sem = self.golay.encode(seed)

        return {"SYN": v_syn, "SEM": v_sem, "TAGS": tags, "CTX": context}

# ==============================================================================
# MODULE 3: HYBRID RESONANCE SCANNER
# ==============================================================================
class ResonanceScanner:
    def __init__(self, database):
        self.db = database
        self.JACCARD_THRESHOLD = 0.30
        self.HAMMING_THRESHOLD = 6

    def _tokenize(self, text: str) -> set:
        clean = re.sub(r'[^a-zA-Z0-9\s]', '', text.lower())
        return set(clean.split())

    def scan_and_trigger(self, user_input: str, cortex: Optional[NativeCortexV2] = None) -> Optional[Dict[str, Any]]:
        input_tokens = self._tokenize(user_input)
        best_match = None
        highest_jaccard = 0.0
        
        for entry_hash, entry in self.db.registry.items():
            entry_profile = set(entry.get("tags", [])).union(self._tokenize(entry.get("name", "")))
            if not input_tokens.union(entry_profile): continue
            jaccard = len(input_tokens.intersection(entry_profile)) / len(input_tokens.union(entry_profile))
            if jaccard > highest_jaccard:
                highest_jaccard = jaccard
                best_match = entry

        if not best_match or highest_jaccard < self.JACCARD_THRESHOLD:
            return None

        if cortex:
            query_chord = cortex.process_concept(user_input)
            match_chord = cortex.process_concept(best_match['name'])
            h_dist = BinaryLinearAlgebra.hamming_distance(query_chord['SYN'], match_chord['SYN'])
            print(f"   [RESONANCE] Match: {best_match['ubp_id']} | Jaccard: {highest_jaccard:.2f} | Hamming: {h_dist}")
            if h_dist > self.HAMMING_THRESHOLD:
                print(f"   ⚠️  High Tension: Query is geometrically 'off-bit'.")
            else:
                print(f"   ✅ Deep Coherence: Query is lattice-aligned.")

        return best_match

# ==============================================================================
# MODULE 4: INNER DIALOGUE
# ==============================================================================
class InnerDialogue:
    def __init__(self, kernel):
        self.kernel = kernel
        self.generator = kernel.cortex
        self.critic = kernel.physics
        self.monitor = kernel.monitor
        # LAW_KERNEL_THRESHOLDS_001: 8 = Neighbor, 12 = Orthogonal
        self.threshold = Fraction(8, 1)

    def deliberate(self, initial_query: str, max_turns: int = 5) -> str:
        current_input = initial_query
        print(f"\n[INNER DIALOGUE] Target: '{initial_query}'")
        
        for turn in range(1, max_turns + 1):
            concept = self.generator.process_concept(current_input)
            cost_val = self.critic.calculate_interaction_cost(concept['SYN'], concept['SEM'])
            cost = Fraction(cost_val, 1)
            
            print(f"   Turn {turn} | Cost: {cost} | Tags: {concept['TAGS']}")
            self.monitor.check(turn, f"Dialogue Turn {turn}")

            if cost <= self.threshold:
                print("   [!] Convergence Detected.")
                return f"COHERENT: {current_input}"

            # Loop Breaking Logic
            if cost >= 12:
                # If Orthogonal, try to find a law matching the TAGS, not the content
                search_query = " ".join(concept['TAGS'])
                match = self.kernel.scanner.scan_and_trigger(search_query, self.generator)
                if match:
                    refinement = f"RECALL: {match['name']}"
                else:
                    refinement = "DIVERGENT: Re-orienting to vacuum state."
            elif cost > 6:
                refinement = f"ORTHOGONAL: Narrowing semantics for {concept['TAGS'][0]}."
            else:
                refinement = f"NEAR-FIELD: Fine-tuning {concept['TAGS'][0]}."

            current_input = refinement

        return f"DIVERGENT: {current_input}"

# ==============================================================================
# MODULE 5: UBP KERNEL V2.1.1
# ==============================================================================
class UBPKernelV2:
    def __init__(self):
        self.version = "2.1.1"
        self.status = "INIT"
        self.memory = HEX_DB_EXACT
        self.cortex = NativeCortexV2()
        self.scanner = ResonanceScanner(self.memory)
        self.physics = TGICExactEngine()
        self.monitor = HorizonMonitor()
        self.dialogue = InnerDialogue(self)

    def boot(self):
        print("\n" + "="*60 + f"\n   UBP KERNEL v{self.version} - INITIALIZING\n" + "="*60)
        if not IMPORTS_OK: return
        self.memory.load_memory()
        count = len(self.memory.registry)
        print(f"   ✅ Memory Online: {count} Laws Mounted.")
        self.status = "READY"
        print(f"\n[SYSTEM] {self.status}.\n")

    def query(self, user_input: str):
        print(f">>> INPUT: '{user_input}'")
        match = self.scanner.scan_and_trigger(user_input, self.cortex)
        seed = f"{match['name']} {match['language']}" if match else user_input
        result = self.dialogue.deliberate(seed)
        print(f"\n[KERNEL OUTPUT] {result}")
        return result

    def inspect_concept(self, text: str) -> Dict[str, Any]:
        chord = self.cortex.process_concept(text)
        mog = OffBitMOG(chord['SEM'])
        return {"concept": text, "tags": chord['TAGS'], "mog_health": mog.get_health_report()}

if __name__ == "__main__":
    KERNEL = UBPKernelV2()
    KERNEL.boot()
    if KERNEL.status == "READY":
        KERNEL.query("The nature of time")
        print("\n[INSPECTION] Analyzing 'Time' Ontology...")
        report = KERNEL.inspect_concept("Time")
        for layer, data in report['mog_health'].items():
            if isinstance(data, dict):
                print(f"  {layer:<8}: W={data['weight']} ({data['status']})")
            else:
                print(f"  {layer:<8}: {data}")
