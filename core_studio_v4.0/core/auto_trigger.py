"""
UBP Auto-Trigger v4.2.1 (Resonance Scanner)
===========================================

Author: Euan R A Craig, New Zealand
Date: 06 January 2026

"""
import re
import hashlib
from hex_dictionary_v4_exact import HEX_DB_EXACT

class ResonanceScanner:
    def __init__(self, database):
        self.db = database
        self.JACCARD_THRESHOLD = 0.35  # Tuned for specific law resonance
        
    def _tokenize(self, text):
        clean = re.sub(r'[^a-zA-Z0-9\s]', '', text.lower())
        return set(clean.split())

    def scan_and_trigger(self, user_input):
        input_tokens = self._tokenize(user_input)
        best_match = None
        highest_resonance = 0.0
        
        # Scan for Semantic Resonance
        for entry_hash, entry in self.db.registry.items():
            entry_profile = set(entry.get("tags", [])).union(self._tokenize(entry.get("name", "")))
            resonance = len(input_tokens.intersection(entry_profile)) / len(input_tokens.union(entry_profile))
            
            if resonance > highest_resonance:
                highest_resonance = resonance
                best_match = entry

        if best_match and highest_resonance >= self.JACCARD_THRESHOLD:
            print(f"\n[MEMORY] !!! Resonance Detected !!!")
            print(f"         Target: {best_match['name']} ({best_match['ubp_id']})")
            print(f"         Score:  {highest_resonance:.2f}")
            return best_match
        return None

HM_KB = ResonanceScanner(HEX_DB_EXACT)
