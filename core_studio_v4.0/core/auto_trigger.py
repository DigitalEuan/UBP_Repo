"""
UBP Auto-Trigger v5.1 (Layered Integration)
===========================================
Combines Jaccard (Semantic) and Hamming (Geometric) metrics.
Now features a Reflexive Kernel Layer for resolving high-tension queries.

Euan Craig, New Zealand
7 Jan 2026

"""
import re
import hashlib
from hex_dictionary_v4_exact import HEX_DB_EXACT
from ubp_core_v4_2_6_COMBINED import BinaryLinearAlgebra

# --- LAYER ADDITION: Import the V2 Kernel ---
try:
    from ubp_kernel import UBPKernelV2
    KERNEL_AVAILABLE = True
except ImportError:
    print("[WARNING] UBPKernelV2 not found. Deep reasoning layer disabled.")
    KERNEL_AVAILABLE = False

class ResonanceScanner:
    def __init__(self, database):
        self.db = database
        self.JACCARD_THRESHOLD = 0.30  # Broad semantic net
        self.HAMMING_THRESHOLD = 6     # Geometric tension limit
        
        # --- LAYER ADDITION: Initialize Kernel ---
        if KERNEL_AVAILABLE:
            print("[AUTO-TRIGGER] Mounting Reflexive Kernel Layer...")
            self.kernel = UBPKernelV2()
            self.kernel.boot()
        else:
            self.kernel = None

    def _tokenize(self, text):
        clean = re.sub(r'[^a-zA-Z0-9\s]', '', text.lower())
        return set(clean.split())

    def _get_hamming_cost(self, vec_a, vec_b):
        return BinaryLinearAlgebra.hamming_distance(list(vec_a), list(vec_b))

    def scan_and_trigger(self, user_input, cortex=None):
        """
        Performs a Hybrid Scan with Reflexive Fallback:
        1. Jaccard: Finds the best semantic match.
        2. Hamming: Checks geometric 'fit'.
        3. Kernel: If High Tension, triggers Inner Dialogue.
        """
        input_tokens = self._tokenize(user_input)
        best_match = None
        highest_jaccard = 0.0
        
        # --- STEP 1: JACCARD SEMANTIC SCAN ---
        for entry_hash, entry in self.db.registry.items():
            entry_profile = set(entry.get("tags", [])).union(self._tokenize(entry.get("name", "")))
            jaccard = len(input_tokens.intersection(entry_profile)) / len(input_tokens.union(entry_profile))
            
            if jaccard > highest_jaccard:
                highest_jaccard = jaccard
                best_match = entry

        if not best_match or highest_jaccard < self.JACCARD_THRESHOLD:
            # If no match found, we can optionally ask the Kernel to hallucinate a path
            # But for now, we return None to respect legacy behavior
            return None

        # --- STEP 2: HAMMING GEOMETRIC VALIDATION ---
        if cortex:
            query_chord = cortex.process_concept(user_input)
            match_chord = cortex.process_concept(best_match['name'])
            
            h_dist = self._get_hamming_cost(query_chord['SYN'], match_chord['SYN'])
            
            print(f"\n[RESONANCE] Match: {best_match['ubp_id']}")
            print(f"            Jaccard: {highest_jaccard:.2f} (Semantic)")
            print(f"            Hamming: {h_dist} (Geometric)")

            if h_dist > self.HAMMING_THRESHOLD:
                print(f"            ⚠️  High Tension: Query is geometrically 'off-bit'.")
                
                # --- STEP 3: REFLEXIVE KERNEL LAYER ---
                if self.kernel:
                    print(f"            ⚙️  Engaging Inner Dialogue to resolve tension...")
                    # We use the match as a seed for the dialogue
                    seed = f"{best_match['name']} {best_match['language']}"
                    resolution = self.kernel.dialogue.deliberate(seed)
                    print(f"            ✅  Kernel Resolution: {resolution}")
                    
                    # Optional: We could return a 'refined' match object here
                    # For now, we return the original match but with the resolution logged
            else:
                print(f"            ✅ Deep Coherence: Query is lattice-aligned.")

        return best_match

HM_KB = ResonanceScanner(HEX_DB_EXACT)
