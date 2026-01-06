"""
UBP HexDictionary v4.x

Version: 4
Author: Euan R A Craig, New Zealand
Date: 02 January 2026

------------------------------
"""
from __future__ import annotations
import hashlib
import json
import os
from fractions import Fraction
from typing import Dict, List, Tuple, Optional, Any
from metrics_exact import METRICS_EXACT

class HexDictionaryV4Exact:
    def __init__(self):
        self.registry: Dict[str, Dict[str, Any]] = {}   
        self.id_map: Dict[str, str] = {}                
        self.tag_index: Dict[str, set[str]] = {}        

    def load_from_json(self, filename: str = "ubp_system_kb.json"):
        """Syncs the Python instance with the manual KB file."""
        if not os.path.exists(filename):
            print(f"[WARNING] {filename} not found. Starting with empty registry.")
            return
        with open(filename, "r") as f:
            data = json.load(f)
            for ubp_id, entry in data.items():
                # Ensure fingerprint is present
                if "fingerprint" not in entry:
                    entry["fingerprint"] = self._generate_triadic_hash(
                        entry["math"], entry["language"], entry["script"]
                    )
                self.registry[entry["fingerprint"]] = entry
                self.id_map[ubp_id] = entry["fingerprint"]
                for tag in entry.get("tags", []):
                    self.tag_index.setdefault(tag, set()).add(entry["fingerprint"])
        print(f"[SYSTEM] HEX_DB Synchronized: {len(self.id_map)} laws loaded.")

    @staticmethod
    def _generate_triadic_hash(math_str: str, lang_str: str, script_str: str) -> str:
        combined = f"{math_str}|{lang_str}|{script_str}".encode("utf-8")
        return hashlib.sha256(combined).hexdigest()

    def store_law(self, ubp_id: str, name: str, math: str, lang: str, script: str, tags: List[str]) -> str:
        analysis = METRICS_EXACT.analyze_state(Fraction(0,1))
        entry_hash = self._generate_triadic_hash(math, lang, script)
        entry = {
            "ubp_id": ubp_id,
            "name": name,
            "math": math,
            "language": lang,
            "script": script,
            "tags": list(tags),
            "nrci": f"{analysis['nrci'].numerator}/{analysis['nrci'].denominator}",
            "fingerprint": entry_hash
        }
        self.registry[entry_hash] = entry
        self.id_map[ubp_id] = entry_hash
        for tag in tags:
            self.tag_index.setdefault(tag, set()).add(entry_hash)
        return entry_hash

    def get_law_by_id(self, ubp_id: str) -> Optional[Dict[str, Any]]:
        entry_hash = self.id_map.get(ubp_id)
        return self.registry.get(entry_hash) if entry_hash else None

HEX_DB_EXACT = HexDictionaryV4Exact()
