"""
UBP Auto-Trigger v4.2 (Resonance Scanner)
-----------------------------------------
Implements Jaccard Similarity for semantic recall and 
Hamming Distance for fingerprint error-correction.
"""
import re
from hex_dictionary_v4_exact import HEX_DB_EXACT

class ResonanceScanner:
    def __init__(self, database):
        self.db = database
        self.JACCARD_THRESHOLD = 0.3  # 30% overlap required to trigger
        self.HAMMING_TOLERANCE = 0    # Exact hex match for now (safety)

    def _tokenize(self, text):
        """Converts text to a set of unique lowercase words."""
        # Remove non-alphanumeric characters and split
        clean = re.sub(r'[^a-zA-Z0-9\s]', '', text.lower())
        return set(clean.split())

    def _calculate_jaccard(self, set_a, set_b):
        """Intersection over Union."""
        if not set_a or not set_b:
            return 0.0
        intersection = len(set_a.intersection(set_b))
        union = len(set_a.union(set_b))
        return intersection / union

    def scan_and_trigger(self, user_input):
        """
        Scans input for:
        1. Semantic Resonance (Tags) via Jaccard
        2. Direct Fingerprint (Hex) via Exact Match
        """
        input_tokens = self._tokenize(user_input)
        best_match = None
        highest_resonance = 0.0
        trigger_type = None

        # 1. Scan HEX_DB for Semantic Resonance
        for entry_hash, entry in self.db.registry.items():
            # Create a set of tags + name tokens for the entry
            entry_tags = set(entry.get("tags", []))
            name_tokens = self._tokenize(entry.get("name", ""))
            entry_profile = entry_tags.union(name_tokens)

            # Calculate Resonance
            resonance = self._calculate_jaccard(input_tokens, entry_profile)
            
            if resonance > highest_resonance:
                highest_resonance = resonance
                best_match = entry
                trigger_type = "SEMANTIC (Jaccard)"

        # 2. Scan for Direct Hex Fingerprints (Regex)
        # Looks for 8-char hex strings like "45eaf185"
        hex_matches = re.findall(r'\b[0-9a-f]{8}\b', user_input.lower())
        for hex_str in hex_matches:
            # Check if this hex exists in DB (or is a prefix)
            for entry_hash, entry in self.db.registry.items():
                if entry_hash.startswith(hex_str):
                    # Direct override if explicit hash is found
                    best_match = entry
                    highest_resonance = 1.0
                    trigger_type = "DIRECT (Hex)"
                    break

        # 3. Trigger Decision
        if best_match and highest_resonance >= self.JACCARD_THRESHOLD:
            print(f"\n[MEMORY] !!! Resonance Detected ({trigger_type}) !!!")
            print(f"         Target: {best_match['name']} (ID: {best_match['ubp_id']})")
            print(f"         Score:  {highest_resonance:.2f}")
            print(f"         [RECALLING] >> {best_match['math']}")
            return best_match

        return None

# Initialize the Scanner
HM_KB = ResonanceScanner(HEX_DB_EXACT)
