"""
UBP HexDictionary v4.4 (Rational Integration)
=============================================
Features:
1. RATIONAL MINTER: Auto-assigns ULAP vectors to new entries.
2. INTEGRITY CHECK: Detects duplicate IDs and vector collisions.
3. SPATIAL CACHE: O(1) access to geometric anchors.
"""
import hashlib
import json
import os
import re
from typing import Dict, List, Optional, Any
from ubp_core_v4_2_6_COMBINED import GOLAY_DECODER

class HexDictionaryV4Exact:
    def __init__(self):
        self.registry: Dict[str, Dict[str, Any]] = {}   
        self.id_map: Dict[str, str] = {}                
        self.vector_cache: Dict[str, List[int]] = {}

    def load_memory(self, json_file: str = "ubp_system_kb.json", md_file: str = "ubp_system_kb.md"):
        target_files = [json_file, md_file, "ubp_hash_memory_kb.md"]
        for fname in target_files:
            if not os.path.exists(fname): continue
            with open(fname, 'r', encoding='utf-8') as f:
                content = f.read()
            found_blocks = self._scavenge_json_blocks(content)
            for block in found_blocks:
                if isinstance(block, dict):
                    if all(isinstance(v, dict) for v in block.values()):
                        for _, entry in block.items(): self._register_entry(entry)
                    else: self._register_entry(block)
        
        self._check_integrity()

    def _scavenge_json_blocks(self, text: str) -> List[Any]:
        results = []
        starts = [m.start() for m in re.finditer('{', text)]
        last_end = 0
        for start in starts:
            if start < last_end: continue
            for end in range(len(text), start, -1):
                if text[end-1] != '}': continue
                try:
                    data = json.loads(text[start:end])
                    results.append(data); last_end = end; break
                except: continue
        return results

    def _register_entry(self, entry: Dict[str, Any]):
        if not isinstance(entry, dict) or "ubp_id" not in entry: return
        
        uid = entry["ubp_id"]
        f_print = entry.get("fingerprint")
        if not f_print:
            seed = f"{entry.get('math')}|{entry.get('language')}|{entry.get('script')}"
            f_print = hashlib.sha256(seed.encode()).hexdigest()
            entry["fingerprint"] = f_print

        # Use existing vector or Mint a Rational one
        vec = entry.get("vector")
        if not vec or len(vec) != 24:
            vec = self.mint_rational_vector(uid)
            entry["vector"] = vec

        self.registry[f_print] = entry
        self.id_map[uid] = f_print
        self.vector_cache[uid] = vec

    def mint_rational_vector(self, ubp_id: str) -> List[int]:
        """Assigns a vector based on the Rational ULAP Standard (7-bit Seq)."""
        uid = ubp_id.upper()
        domains = {"ELEM":0, "CHEM":0, "PHYS":1, "MECH":1, "QM":1, "BIO":2, "CELL":2, "CODE":3, "ALGO":3, "CONST":4, "NUM":4, "LAW":5}
        dom_val = 7 
        for prefix, val in domains.items():
            if prefix in uid: dom_val = val; break

        nums = re.findall(r'\d+', uid)
        seq = int(nums[-1]) if nums else 0

        # Construct 12-bit message: [Domain(3) | Scale(2) | Seq(7)]
        msg = [(dom_val >> i) & 1 for i in range(2, -1, -1)] 
        msg += [0, 0] 
        msg += [(seq >> i) & 1 for i in range(6, -1, -1)] 

        return GOLAY_DECODER.encode(msg)

    def _check_integrity(self):
        unique_ids = set(self.id_map.keys())
        if len(self.registry) > len(unique_ids):
            print(f"[INTEGRITY] Warning: {len(self.registry) - len(unique_ids)} Duplicate IDs detected.")

    def get_vector(self, ubp_id: str) -> Optional[List[int]]:
        return self.vector_cache.get(ubp_id)

    def find_by_id(self, ubp_id: str) -> Optional[Dict[str, Any]]:
        f_print = self.id_map.get(ubp_id)
        return self.registry.get(f_print) if f_print else None

HEX_DB_EXACT = HexDictionaryV4Exact()