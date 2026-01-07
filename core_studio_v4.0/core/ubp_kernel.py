"""
UBP KERNEL v2.0 (REFLEXIVE REASONING ENGINE)
============================================
The production-ready core of the Universal Binary Principle system.
Integrates Recursive Cortex, Hybrid Resonance, and Inner Dialogue.

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
# MODULE 1: NATIVE CORTEX V2 (Recursive Classifier)
# ==============================================================================
class NativeCortexV2:
    def __init__(self):
        self.golay = GOLAY_DECODER
        
        # UBP Lexicon: Hard-coded geometric anchors
        self.LEXICON = {
            # System Signals
            "control": ["CONTROL", "SYSTEM"],
            "feedback": ["CONTROL", "FEEDBACK"],
            "refinement": ["CONTROL", "REFINEMENT"],
            "orthogonal": ["GEOMETRY", "DIRECTION", "90_DEG"],
            "divergent": ["SYSTEM", "STATUS", "WARNING"],
            "coherent": ["SYSTEM", "STATUS", "STABLE"],
            "recall": ["MEMORY", "ACTION", "RETRIEVAL"],
            "near-field": ["GEOMETRY", "PROXIMITY", "FINE_TUNING"], # Added to fix your loop
            
            # Core Concepts
            "time": ["CONCEPT", "TEMPORAL", "FLOW"],
            "lattice": ["GEOMETRY", "STRUCTURE", "LEECH"],
            "golay": ["GEOMETRY", "CODE", "PERFECT"],
            "matter": ["PHYSICS", "SUBSTRATE", "PHENOMENAL"],
            "information": ["CONCEPT", "NOUMENAL", "DATA"],
            "codeword": ["GEOMETRY", "TARGET", "STABLE"],
            "error": ["SYSTEM", "METRIC", "SYNDROME"],
            "cost": ["SYSTEM", "METRIC", "HAMMING"],
            "nature": ["CONCEPT", "ONTOLOGY", "SOURCE"],
            "principle": ["LAW", "AXIOM", "TRUTH"]
        }

    def _hash_to_vector(self, tag: str) -> List[int]:
        """Maps a tag string to a 24-bit Golay codeword."""
        h = hashlib.sha256(tag.encode('utf-8')).hexdigest()
        val = int(h[:6], 16)
        raw = [(val >> i) & 1 for i in range(23, -1, -1)]
        corrected, _, _ = self.golay.decode(raw)
        return corrected

    def _analyze_content(self, text: str) -> Tuple[List[str], str]:
        """1st-Order Recursive Analysis."""
        text_lower = text.lower()
        tags = []
        
        # 1. Check for Control Signals (Critic Feedback)
        if ":" in text and (text.startswith("ORTHOGONAL") or text.startswith("DIVERGENT") or text.startswith("RECALL")):
            return ["CONTROL", "FEEDBACK", "REFINEMENT"], "SYSTEM"

        # 2. Check UBP Lexicon
        for key, specific_tags in self.LEXICON.items():
            if key in text_lower:
                tags.extend(specific_tags)
        
        # 3. Fallback / Augmentation
        if not tags:
            if text in keyword.kwlist: 
                tags = ["CODE", "KEYWORD"]
                return tags, "PYTHON"
            
            if " " in text: tags.append("PHRASE")
            else: tags.append("WORD")
            
            if text and text[0].isupper(): tags.append("PROPER_NOUN")
            else: tags.append("GENERAL")
            
        return list(set(tags)), "LANGUAGE"

    def process_concept(self, concept_input: Any) -> Dict[str, Any]:
        """Main processing pipeline with Identity Anchoring."""
        if isinstance(concept_input, str):
            tags, context = self._analyze_content(concept_input)
        elif isinstance(concept_input, (int, float)):
            tags, context = ["NUMBER", "QUANTITY"], "MATH"
        else:
            tags, context = ["DATA", "RAW"], "BINARY"

        # SYN (Syntax): Based on the primary category (first tag)
        v_syn = self._hash_to_vector(tags[0])
        
        # SEM (Semantics): Identity Anchor
        # XOR the content hash into the SEM vector to prevent collisions
        content_str = str(concept_input)
        content_hash = int(hashlib.sha256(content_str.encode()).hexdigest()[:6], 16)
        raw_sem_bits = [(content_hash >> i) & 1 for i in range(23, -1, -1)]
        
        # Snap identity to lattice
        v_sem, _, _ = self.golay.decode(raw_sem_bits) 

        return {"SYN": v_syn, "SEM": v_sem, "TAGS": tags, "CTX": context}

# ==============================================================================
# MODULE 2: HYBRID RESONANCE SCANNER
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
        """Hybrid Scan: Jaccard (Semantic) + Hamming (Geometric)."""
        input_tokens = self._tokenize(user_input)
        best_match = None
        highest_jaccard = 0.0
        
        # Jaccard Scan
        for entry_hash, entry in self.db.registry.items():
            entry_profile = set(entry.get("tags", [])).union(self._tokenize(entry.get("name", "")))
            if not input_tokens.union(entry_profile): continue
            jaccard = len(input_tokens.intersection(entry_profile)) / len(input_tokens.union(entry_profile))
            
            if jaccard > highest_jaccard:
                highest_jaccard = jaccard
                best_match = entry

        if not best_match or highest_jaccard < self.JACCARD_THRESHOLD:
            return None

        # Hamming Validation
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
# MODULE 3: INNER DIALOGUE (Reflexive Loop)
# ==============================================================================
class InnerDialogue:
    def __init__(self, kernel):
        self.kernel = kernel
        self.generator = kernel.cortex
        self.critic = kernel.physics
        self.monitor = kernel.monitor
        self.threshold = Fraction(3, 1)

    def deliberate(self, initial_query: str, max_turns: int = 5) -> str:
        current_input = initial_query
        
        print(f"\n[INNER DIALOGUE] Target: '{initial_query}'")
        
        for turn in range(1, max_turns + 1):
            # 1. Generate
            concept = self.generator.process_concept(current_input)
            
            # 2. Critique
            cost_val = self.critic.calculate_interaction_cost(concept['SYN'], concept['SEM'])
            cost = Fraction(cost_val, 1)
            
            print(f"   Turn {turn} | Cost: {cost} | Tags: {concept['TAGS']}")
            self.monitor.check(turn, f"Dialogue Turn {turn}")

            # 3. Converge
            if cost <= self.threshold:
                print("   [!] Convergence Detected.")
                return f"COHERENT: {current_input}"

            # 4. Refine
            if cost > 12:
                match = self.kernel.scanner.scan_and_trigger(current_input, self.generator)
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
# MODULE 4: UBP KERNEL V2
# ==============================================================================
class UBPKernelV2:
    def __init__(self):
        self.version = "2.0.0"
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
        
        # Load Memory
        self.memory.load_memory()
        count = len(self.memory.registry)
        print(f"   ✅ Memory Online: {count} Laws Mounted.")
        
        self.status = "READY"
        print(f"\n[SYSTEM] {self.status}.\n")

    def query(self, user_input: str):
        """The Reasoning Bridge: Connects Input -> Resonance -> Dialogue."""
        print(f">>> INPUT: '{user_input}'")
        
        # 1. Resonance Scan
        match = self.scanner.scan_and_trigger(user_input, self.cortex)
        
        if match:
            print(f"[RECALL: {match['ubp_id']}]")
            # If we have a strong match, we can return it, or use it to seed dialogue
            # For V2, we use it to seed dialogue if the user input was vague
            seed = f"{match['name']} {match['language']}"
        else:
            seed = user_input

        # 2. Reflexive Deliberation
        result = self.dialogue.deliberate(seed)
        print(f"\n[KERNEL OUTPUT] {result}")
        return result

# ==============================================================================
# MAIN EXECUTION
# ==============================================================================
if __name__ == "__main__":
    KERNEL = UBPKernelV2()
    KERNEL.boot()
    
    if KERNEL.status == "READY":
        # Test the full stack
        KERNEL.query("The nature of time")
