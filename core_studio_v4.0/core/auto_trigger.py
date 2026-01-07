"""
UBP Auto-Trigger v5.2 (Tiered Recall)
=====================================
Implements a three-tier resonance scan:
1. Keyword Anchor (Deterministic)
2. Jaccard Semantic (Probabilistic)
3. Hamming Geometric (Structural)

Author: Euan Craig, New Zealand with UBP Research Cortex v4.2.6
8 Jan 2026
"""
import re
from hex_dictionary_v4_exact import HEX_DB_EXACT
from ubp_core_v4_2_6_COMBINED import BinaryLinearAlgebra

class ResonanceScanner:
    def __init__(self, database):
        self.db = database
        self.JACCARD_THRESHOLD = 0.30
        self.HAMMING_THRESHOLD = 6

    def _tokenize(self, text):
        """Cleans and tokenizes input for semantic analysis."""
        clean = re.sub(r'[^a-zA-Z0-9\s]', '', text.lower())
        return set(clean.split())

    def scan_and_trigger(self, user_input, cortex=None):
        input_tokens = self._tokenize(user_input)
        input_lower = user_input.lower()
        
        # --- TIER 1: KEYWORD ANCHOR (Deterministic) ---
        # If the user mentions the name or ID directly, trigger immediately.
        for entry_hash, entry in self.db.registry.items():
            name = entry.get("name", "").lower()
            ubp_id = entry.get("ubp_id", "").lower()
            if input_lower in name or input_lower in ubp_id:
                print(f"[RECALL: {entry['ubp_id']}] via Keyword Anchor.")
                return entry

        # --- TIER 2: JACCARD SEMANTIC SCAN (Probabilistic) ---
        best_match = None
        highest_jaccard = 0.0
        for entry_hash, entry in self.db.registry.items():
            # Combine tags and name tokens for the profile
            entry_profile = set(entry.get("tags", [])).union(self._tokenize(entry.get("name", "")))
            
            intersection = input_tokens.intersection(entry_profile)
            union = input_tokens.union(entry_profile)
            
            if not union: continue
            jaccard = len(intersection) / len(union)
            
            if jaccard > highest_jaccard:
                highest_jaccard = jaccard
                best_match = entry

        # --- TIER 3: HAMMING GEOMETRIC VALIDATION ---
        if best_match and highest_jaccard >= self.JACCARD_THRESHOLD:
            if cortex:
                # Map query and match to vectors to check structural alignment
                query_chord = cortex.process_concept(user_input)
                match_chord = cortex.process_concept(best_match['name'])
                h_dist = BinaryLinearAlgebra.hamming_distance(query_chord['SYN'], match_chord['SYN'])
                
                if h_dist <= self.HAMMING_THRESHOLD:
                    print(f"[RECALL: {best_match['ubp_id']}] via Geometric Resonance (J:{highest_jaccard:.2f}, H:{h_dist}).")
                    return best_match
            else:
                print(f"[RECALL: {best_match['ubp_id']}] via Semantic Resonance (J:{highest_jaccard:.2f}).")
                return best_match

        return None

# Global Instance for the Kernel
HM_KB = ResonanceScanner(HEX_DB_EXACT)
