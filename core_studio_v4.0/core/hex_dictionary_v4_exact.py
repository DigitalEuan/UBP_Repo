UBP HexDictionary v4.x (Exact)
------------------------------

Float-free content-addressable memory controller.

Changes vs hex_dictionary_v4.py:
- Uses METRICS_EXACT (Fraction-based), not METRICS.analyze_state(0.0).
- Jaccard similarity returned as Fraction.
"""
from __future__ import annotations

import hashlib
import json
from fractions import Fraction
from typing import Dict, List, Tuple, Optional, Any

from metrics_exact import METRICS_EXACT

class HexDictionaryV4Exact:
    def __init__(self):
        self.registry: Dict[str, Dict[str, Any]] = {}   # Hash -> entry
        self.id_map: Dict[str, str] = {}                # UBP_ID -> Hash
        self.tag_index: Dict[str, set[str]] = {}        # Tag -> set(Hashes)

    @staticmethod
    def _generate_triadic_hash(math_str: str, lang_str: str, script_str: str) -> str:
        combined = f"{math_str}|{lang_str}|{script_str}".encode("utf-8")
        return hashlib.sha256(combined).hexdigest()

    def store_law(self, ubp_id: str, name: str, math: str, lang: str, script: str, tags: List[str]) -> str:
        # In exact mode, "variance" must be a Fraction.
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
        }
        self.registry[entry_hash] = entry
        self.id_map[ubp_id] = entry_hash

        for tag in tags:
            self.tag_index.setdefault(tag, set()).add(entry_hash)

        return entry_hash

    def get_law_by_id(self, ubp_id: str) -> Optional[Dict[str, Any]]:
        entry_hash = self.id_map.get(ubp_id)
        return self.registry.get(entry_hash) if entry_hash else None

    def jaccard_alert(self, current_tags: List[str], threshold: Fraction = Fraction(3,5)) -> List[Tuple[str, str, Fraction]]:
        """
        Returns alerts when Jaccard(tags) > threshold.
        Default threshold = 3/5 (=0.6), exact.
        """
        alerts: List[Tuple[str, str, Fraction]] = []
        q = set(current_tags)
        for entry_hash, entry in self.registry.items():
            s = set(entry.get("tags", []))
            inter = len(s & q)
            uni = len(s | q)
            j = Fraction(inter, uni) if uni else Fraction(0,1)
            if j > threshold:
                alerts.append((entry["name"], entry["ubp_id"], j))
        return alerts

# Global instance
HEX_DB_EXACT = HexDictionaryV4Exact()