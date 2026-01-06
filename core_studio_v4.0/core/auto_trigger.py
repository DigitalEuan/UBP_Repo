"""
UBP Auto-Trigger v4.3.0 (Hybrid Resonance)
===========================================
Combines Jaccard (Semantic) and Hamming (Geometric) metrics.

Euan Craig, New Zealand 
6 Jan 2026
"""
import re
import hashlib
from hex_dictionary_v4_exact import HEX_DB_EXACT
from ubp_core_v4_2_6_COMBINED import BinaryLinearAlgebra

class ResonanceScanner:
    def __init__(self, database):
        self.db = database
        self.JACCARD_THRESHOLD = 0.30  # Broad semantic net
        self.HAMMING_THRESHOLD = 6     # Geometric tension limit

    def _tokenize(self, text):
        clean = re.sub(r'[^a-zA-Z0-9\s]', '', text.lower())
        return set(clean.split())

    def _get_hamming_cost(self, vec_a, vec_b):
        return BinaryLinearAlgebra.hamming_distance(list(vec_a), list(vec_b))

    def scan_and_trigger(self, user_input, cortex=None):
        """
        Performs a Hybrid Scan:
        1. Jaccard: Finds the best semantic match in HEX_DB.
        2. Hamming: If a match is found, checks the geometric 'fit'.
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
            return None

        # --- STEP 2: HAMMING GEOMETRIC VALIDATION ---
        # If we have a cortex, we check if the query 'snaps' to the match
        if cortex:
            query_chord = cortex.process_concept(user_input)
            match_chord = cortex.process_concept(best_match['name'])
            
            h_dist = self._get_hamming_cost(query_chord['SYN'], match_chord['SYN'])
            
            print(f"\n[RESONANCE] Match: {best_match['ubp_id']}")
            print(f"            Jaccard: {highest_jaccard:.2f} (Semantic)")
            print(f"            Hamming: {h_dist} (Geometric)")

            if h_dist > self.HAMMING_THRESHOLD:
                print(f"            ⚠️  High Tension: Query is geometrically 'off-bit'.")
                # This is where the InnerDialogue would be triggered to refine
            else:
                print(f"            ✅ Deep Coherence: Query is lattice-aligned.")

        return best_match

HM_KB = ResonanceScanner(HEX_DB_EXACT)