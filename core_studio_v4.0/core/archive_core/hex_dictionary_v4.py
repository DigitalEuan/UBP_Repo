"""
UBP HexDictionary v4.0 (Resonant Memory Controller)
Description: Content-addressable storage with Jaccard Similarity 
             and Triadic Verification.
"""
import hashlib
import json
from metrics import METRICS

class HexDictionaryV4:
    def __init__(self):
        self.registry = {}  # Hash -> {Math, Language, Script, Meta}
        self.id_map = {}    # UBP_ID -> Hash (The Fingerprint Bridge)
        self.tag_index = {} # Tag -> set(Hashes)

    def _generate_triadic_hash(self, math_str, lang_str, script_str):
        """Generates a unique hash for the Triadic Identity."""
        combined = f"{math_str}|{lang_str}|{script_str}".encode('utf-8')
        return hashlib.sha256(combined).hexdigest()

    def store_law(self, ubp_id, name, math, lang, script, tags):
        """Stores a law with Triadic Verification."""
        analysis = METRICS.analyze_state(0.0) 
        entry_hash = self._generate_triadic_hash(math, lang, script)
        
        entry = {
            "ubp_id": ubp_id,
            "name": name,
            "math": math,
            "language": lang,
            "script": script,
            "tags": tags,
            "nrci": analysis['nrci']
        }
        
        self.registry[entry_hash] = entry
        self.id_map[ubp_id] = entry_hash
        
        for tag in tags:
            if tag not in self.tag_index:
                self.tag_index[tag] = set()
            self.tag_index[tag].add(entry_hash)
            
        print(f"[HEX_STORE] Law {ubp_id} locked. Hash: {entry_hash[:8]}")
        return entry_hash

    def get_law_by_id(self, ubp_id):
        """Retrieves the full triadic payload by UBP_ID."""
        entry_hash = self.id_map.get(ubp_id)
        return self.registry.get(entry_hash) if entry_hash else None

    def jaccard_alert(self, current_tags):
        """Triggers an alert if current research overlaps with existing KB."""
        alerts = []
        for entry_hash, entry in self.registry.items():
            stored_tags = set(entry['tags'])
            query_tags = set(current_tags)
            intersection = len(stored_tags & query_tags)
            union = len(stored_tags | query_tags)
            j_index = intersection / union if union > 0 else 0
            if j_index > 0.6:
                alerts.append((entry['name'], entry['ubp_id'], j_index))
        return alerts

# Initialize Global Substrate Memory
HEX_DB = HexDictionaryV4()
