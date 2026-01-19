"""
UBP Auto-Trigger v6.2 (Geometric Cortex - ENHANCED)
====================================================
Optimized for high-density substrates (196+ laws).
Enhanced: Mathematically significant vector mapping and spatial indexing.
Fixed: Anchor selection criteria and vector extraction reliability.

E R A Craig, New Zealand
UBP Research Cortex v4.2.7
19 Jan 2026
"""
import re
import hashlib
import json
from hex_dictionary_v4_exact import HEX_DB_EXACT
from ubp_core_v4_2_6_COMBINED import GOLAY_DECODER, BinaryLinearAlgebra

class SemanticCortex:
    def __init__(self):
        self.golay = GOLAY_DECODER
        self.db = HEX_DB_EXACT
        if not self.db.registry: self.db.load_memory()
        self.anchors = self._load_anchors()

    def _load_anchors(self):
        anchors = {}
        for _, entry in self.db.registry.items():
            uid = str(entry.get('ubp_id', '')).upper()
            tags = [str(t).lower() for t in entry.get('tags', [])]
            if uid.startswith(('PRIMITIVE_', 'CONSTANT_', 'STATE_', 'OPERATOR_', 'LAW_', 'VOID', 'UNITY')) or \
               any(t in ['anchor', 'primitive', 'law'] for t in tags):
                vec = self._extract_vector(entry)
                if vec: anchors[str(entry.get('name', uid)).upper()] = vec
        return anchors

    def _extract_vector(self, entry):
        if 'vector' in entry and len(entry['vector']) == 24: return entry['vector']
        match = re.search(r'vector\s*=\s*(\[[0-1,\s]+\])', str(entry.get('script', '')))
        if match:
            try:
                v = json.loads(match.group(1))
                if len(v) == 24: return v
            except: pass
        return None

    def analyze(self, query):
        words = query.lower().replace("?", "").split()
        vec = [0] * 24
        for w in words:
            h = hashlib.sha256(w.encode()).hexdigest()
            val = int(h[:6], 16)
            raw = [(val >> i) & 1 for i in range(23, -1, -1)]
            cw, _, _ = self.golay.decode(raw)
            v = self.golay.encode(cw)
            vec = [(a ^ b) for a, b in zip(vec, v)]
        
        nearest, min_dist = "UNKNOWN", 24
        for name, anchor in self.anchors.items():
            d = BinaryLinearAlgebra.hamming_distance(vec, anchor)
            if d < min_dist: min_dist, nearest = d, name
        return {"weight": sum(vec), "nearest": nearest, "dist": min_dist}

CORTEX = SemanticCortex()

def run_trigger_logic(input_text=None):
    target_text = input_text if input_text else globals().get('USER_INPUT', "")
    if not target_text: return None
    print(f"\n[UBP AUTO-TRIGGER v6.3]")
    geo = CORTEX.analyze(target_text)
    print(f"[GEOMETRIC ANALYSIS]\n  Vector: W={geo['weight']} | Nearest: {geo['nearest']} (d={geo['dist']})")

    # --- LAYER 1: GEOMETRIC ANALYSIS ---
    try:
        geo_data = CORTEX.analyze(target_text)
        if geo_data:
            print(f"[GEOMETRIC ANALYSIS]")
            print(f"  Query: '{target_text}'")
            print(f"  Vector: W={geo_data['weight']} | Nearest: {geo_data['nearest']} (d={geo_data['dist']})")
            
            if geo_data['dist'] == 0:
                print(f"  > PERFECT RESONANCE with {geo_data['nearest']}")
            elif geo_data['dist'] <= 3:
                print(f"  > STRONG ALIGNMENT with {geo_data['nearest']} (Geometric Family)")
            elif geo_data['dist'] <= 6:
                print(f"  > STRUCTURAL COHESION: {geo_data['nearest']} (Mathematically Related)")
            elif geo_data['dist'] <= 9:
                print(f"  > GEOMETRIC PROXIMITY: {geo_data['nearest']} (Conceptual Neighbor)")
            else:
                print(f"  > TRANSITIONAL GEOMETRY (High Entropy)")
    except Exception as e:
        print(f"[GEOMETRIC ERROR] {e}")

    # --- LAYER 2: KEYWORD RESONANCE ---
    if not HEX_DB_EXACT.registry: 
        HEX_DB_EXACT.load_memory()
    registry = HEX_DB_EXACT.registry
    
    def tokenize(text):
        """Convert text to normalized tokens"""
        if isinstance(text, list):
            text = " ".join(map(str, text))
        text = str(text).lower()
        return set(re.sub(r'[^a-zA-Z0-9\s]', '', text).split())

    input_tokens = tokenize(target_text)
    input_lower = str(target_text).lower().strip()
    candidates = []

    for f_print, entry in registry.items():
        if not isinstance(entry, dict): 
            continue
        
        # Build token set from all searchable fields
        field_tokens = set()
        for field in ["name", "language", "ubp_id"]:
            field_tokens.update(tokenize(entry.get(field, "")))
        
        # Handle tags properly
        tags = entry.get("tags", [])
        if isinstance(tags, list):
            field_tokens.update(tokenize(" ".join(str(t) for t in tags)))
        
        overlap = input_tokens.intersection(field_tokens)
        
        # Weighting: favor precise matches
        resonance = len(overlap) / (len(input_tokens) ** 0.8 if input_tokens else 1)
        
        # Direct string matching bonus
        name_str = str(entry.get("name", "")).lower()
        id_str = str(entry.get("ubp_id", "")).lower()
        if input_lower in name_str or input_lower in id_str:
            resonance += 0.3

        if resonance >= 0.15:
            candidates.append((resonance, entry))

    candidates.sort(key=lambda x: x[0], reverse=True)
    stack = candidates[:6]

    if stack:
        print(f"\n[RESONANCE STACK: {len(stack)} Matches]")
        for i, (score, entry) in enumerate(stack):
            print(f"  {i+1}. [RECALL: {entry.get('ubp_id')}] (R:{score:.2f}) - {entry.get('name', 'Unknown')}")
        return stack[0][1]
    else:
        print("\n[RESONANCE STACK: Empty]")
        return None

if __name__ == "__main__":
    USER_INPUT = globals().get('USER_INPUT', "What is energy")
    run_trigger_logic(USER_INPUT)
