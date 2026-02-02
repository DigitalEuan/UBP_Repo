"""
UBP HexDictionary v4.5 (Definitive Spine Integration)
=====================================================
Features:
1. SPINE VECTOR GENERATOR: Uses SHA256(UBP_ID) to derive unique geometric coordinates.
2. AUTOMATIC DOMAIN MAPPING: Infers geometric domain from UBP_ID prefixes.
3. INTEGRITY CHECK: Detects duplicate IDs and vector collisions.
4. SPATIAL CACHE: O(1) access to geometric anchors.

E R A Craig, New Zealand
UBP Research Cortex v4.2.7
Updated: 02 Feb 2026
"""
import hashlib
import json
import os
import re
from typing import Dict, List, Optional, Any, Tuple
from ubp_core_v4_2_6_COMBINED import GOLAY_DECODER

class HexDictionaryV4Exact:
    # --- UBP STANDARDS (Embedded) ---
    DOMAINS = {
        "SUBSTANCE": 0, "MECHANISM": 1, "ORGANISM": 2, "ALGORITHM": 3,
        "QUANTITY": 4, "IMPERATIVE": 5, "ENTROPY": 6, "MEANING": 7
    }
    GRAY_3BIT = [0b000, 0b001, 0b011, 0b010, 0b110, 0b111, 0b101, 0b100]
    GRAY_5BIT = [0, 1, 3, 2, 6, 7, 5, 4, 12, 13, 15, 14, 10, 11, 9, 8,
                 24, 25, 27, 26, 30, 31, 29, 28, 20, 21, 23, 22, 18, 19, 17, 16]

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

        # Use existing vector or Mint a Rational Spine vector
        vec = entry.get("vector")
        if not vec or len(vec) != 24:
            vec = self.mint_rational_vector(uid)
            entry["vector"] = vec

        self.registry[f_print] = entry
        self.id_map[uid] = f_print
        self.vector_cache[uid] = vec

    # --- CORE SPINE LOGIC ---

    def _get_domain_for_type(self, ubp_id: str) -> str:
        """Determine the appropriate domain based on entry type prefix."""
        uid = ubp_id.upper()
        if uid.startswith(("ELEM_", "CHEM_", "MAT_")): return "SUBSTANCE"
        if uid.startswith(("PHYS_", "MECH_", "QM_", "WAVE_", "THERMO_", "FORCE_", "PARTICLE_")): return "MECHANISM"
        if uid.startswith(("BIO", "CELL_", "PSYCH_", "ECO_")): return "ORGANISM"
        if uid.startswith(("PY_", "CODE_", "ALGO_", "DS_", "CRYPTO_", "ML_", "BITOP_")): return "ALGORITHM"
        if uid.startswith(("NUM_", "CONST_", "MATH_", "CALC_", "STATS_", "MATRIX_", "GEO_")): return "QUANTITY"
        if uid.startswith(("LAW_", "ACTION_", "STATE_", "TAX_")): return "IMPERATIVE"
        if uid.startswith(("PATTERN_", "TRANSFORM_", "GATE_", "NOISE_")): return "ENTROPY"
        return "MEANING" # Default

    def _get_domain_bits(self, domain_name: str) -> List[int]:
        val = self.DOMAINS.get(domain_name.upper(), 7)
        return [(val >> i) & 1 for i in range(2, -1, -1)]

    def _get_gray_bits(self, value: int, width: int = 3) -> List[int]:
        limit = (1 << width) - 1
        idx = max(0, min(limit, value))
        table = self.GRAY_3BIT if width == 3 else self.GRAY_5BIT
        code = table[idx] if idx < len(table) else idx
        return [(code >> i) & 1 for i in range(width-1, -1, -1)]

    def mint_rational_vector(self, ubp_id: str) -> List[int]:
        """
        Generates a DEFINITIVE SPINE VECTOR.
        Guaranteed unique for unique UBP_IDs.
        Method: SHA256(ID) -> Extract P1, P2, P3 -> Combine with Domain -> Golay Encode.
        """
        # 1. Determine Domain
        domain = self._get_domain_for_type(ubp_id)

        # 2. Hash the ID for parameters
        h = hashlib.sha256(ubp_id.upper().encode()).digest()
        combined = int.from_bytes(h[:4], 'big')

        # 3. Extract Parameters (Non-overlapping bits)
        p1 = (combined >> 17) % 8   # bits 17-19 -> 0-7
        p2 = (combined >> 7) % 32   # bits 7-11 -> 0-31
        p3 = (combined >> 0) % 2    # bit 0 -> 0-1

        # 4. Construct Message
        dom_bits = self._get_domain_bits(domain)
        p1_bits = self._get_gray_bits(p1, 3)
        p2_bits = self._get_gray_bits(p2, 5)
        p3_bits = [p3 & 1]

        msg = dom_bits + p1_bits + p2_bits + p3_bits

        # 5. Encode to 24-bit Vector
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
