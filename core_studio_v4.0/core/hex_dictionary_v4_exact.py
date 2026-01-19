"""
UBP HexDictionary v4.3 (Spatial Cache & Vector Prioritization)
=============================================================
Optimized for high-density substrates (900+ anchors).
Features:
1. SPATIAL CACHE: O(1) access to geometric vectors.
2. SOURCE OF TRUTH: Prioritizes explicit 'vector' fields over derived hashes.
3. RECURSIVE SCAVENGER: Improved JSON recovery for large .md files.

Author: Euan R A Craig, New Zealand
UBP Research Cortex v4.2.7
Date: 19 January 2026
"""
from __future__ import annotations
import hashlib
import json
import os
import re
from typing import Dict, List, Tuple, Optional, Any

class HexDictionaryV4Exact:
    def __init__(self):
        self.registry: Dict[str, Dict[str, Any]] = {}   
        self.id_map: Dict[str, str] = {}                
        self.tag_index: Dict[str, set[str]] = {}
        self.vector_cache: Dict[str, List[int]] = {} # NEW: Spatial Cache

    def load_memory(self, json_file: str = "ubp_system_kb.json", md_file: str = "ubp_system_kb.md"):
        """Scavenges all JSON blocks and populates the Spatial Cache."""
        target_files = [json_file, md_file, "ubp_hash_memory_kb.md"]
        for fname in target_files:
            if not os.path.exists(fname): continue
            
            with open(fname, 'r', encoding='utf-8') as f:
                content = f.read()
            
            found_blocks = self._scavenge_json_blocks(content)
            if found_blocks:
                for block in found_blocks:
                    if isinstance(block, dict):
                        # Handle nested dictionary (keyed by hash)
                        if all(isinstance(v, dict) for v in block.values()):
                            for _, entry in block.items():
                                self._register_entry(entry)
                        else:
                            self._register_entry(block)
        
        print(f"[HEX_DB] Synchronized: {len(self.registry)} Entries | {len(self.vector_cache)} Geometric Anchors.")

    def _scavenge_json_blocks(self, text: str) -> List[Any]:
        """Finds all valid JSON objects within a string."""
        results = []
        starts = [m.start() for m in re.finditer('{', text)]
        last_end = 0
        for start in starts:
            if start < last_end: continue
            for end in range(len(text), start, -1):
                if text[end-1] != '}': continue
                candidate = text[start:end]
                try:
                    data = json.loads(candidate)
                    results.append(data)
                    last_end = end
                    break
                except: continue
        return results

    def _register_entry(self, entry: Dict[str, Any]):
        if not isinstance(entry, dict) or "ubp_id" not in entry: return
        
        # 1. Content Integrity
        f_print = entry.get("fingerprint")
        if not f_print:
            # Derive fingerprint if missing
            seed = f"{entry.get('math')}|{entry.get('language')}|{entry.get('script')}"
            f_print = hashlib.sha256(seed.encode()).hexdigest()
            entry["fingerprint"] = f_print

        self.registry[f_print] = entry
        self.id_map[entry["ubp_id"]] = f_print
        
        # 2. Spatial Cache Registration (The Source of Truth)
        vec = entry.get("vector")
        if isinstance(vec, list) and len(vec) == 24:
            self.vector_cache[entry["ubp_id"]] = [int(b) for b in vec]
        
        # 3. Tag Indexing
        for tag in entry.get("tags", []):
            self.tag_index.setdefault(str(tag).lower(), set()).add(f_print)

    def get_vector(self, ubp_id: str) -> Optional[List[int]]:
        """O(1) retrieval of geometric identity."""
        return self.vector_cache.get(ubp_id)

    def find_by_id(self, ubp_id: str) -> Optional[Dict[str, Any]]:
        f_print = self.id_map.get(ubp_id)
        return self.registry.get(f_print) if f_print else None

HEX_DB_EXACT = HexDictionaryV4Exact()
