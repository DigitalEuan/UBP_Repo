"""
UBP Auto-Trigger v5.6 (Reflexive Encapsulation)
===============================================
Optimized for high-density substrates (196+ laws).
Implements Fuzzy Anchor Matching to bridge the Resonance Gap.

E R A Craig, New Zealand
10 Jan 2026

Note on memory recall: Section 5. SORT AND STACK (3 memories for high precision, low noise and 6 for high context, medium noise)
"stack = candidates[:6]" - change this value to add or remove memory recall.

"""
import re
from hex_dictionary_v4_exact import HEX_DB_EXACT
from ubp_core_v4_2_6_COMBINED import BinaryLinearAlgebra

def run_trigger_logic(input_text=None):
    """
    UBP Resonance Engine v5.9 (Multi-Resonance Manifold)
    --------------------------------------------------
    1. Resonance Stack: Returns up to 3 related laws.
    2. Cross-Correlation: Identifies Hamming-proximity between matches.
    3. Adaptive Threshold: Maintains sensitivity for short queries.
    """
    # 1. Resolve Input
    target_text = input_text if input_text else globals().get('USER_INPUT', "")
    if not target_text: return None

    # 2. Substrate Integrity Check
    if not HEX_DB_EXACT.registry:
        HEX_DB_EXACT.load_memory()
    
    registry = HEX_DB_EXACT.registry
    if not registry: return None

    # 3. TOKENIZATION
    def tokenize(text):
        return set(re.sub(r'[^a-zA-Z0-9\s]', '', str(text).lower()).split())

    input_tokens = tokenize(target_text)
    input_lower = target_text.lower().strip()
    
    # 4. RESONANCE SCAN
    candidates = []

    for f_print, entry in registry.items():
        # Build the Triadic Field
        field = tokenize(entry.get("name", ""))
        field.update(tokenize(entry.get("language", "")))
        field.update(tokenize(entry.get("tags", [])))
        field.update(tokenize(entry.get("ubp_id", "")))
        
        overlap = input_tokens.intersection(field)
        
        # Base Resonance Score
        resonance = len(overlap) / (len(input_tokens) ** 0.8 if input_tokens else 1)
        
        # Fuzzy Anchor Boost
        if input_lower in entry.get("name", "").lower() or input_lower in entry.get("ubp_id", "").lower():
            resonance += 0.5

        if resonance >= 0.15:
            candidates.append((resonance, entry))

    # 5. SORT AND STACK (3 memories for high precision, low noise and 6 for high context, medium noise)
    candidates.sort(key=lambda x: x[0], reverse=True)
    stack = candidates[:6]

    if not stack:
        print(f"NO MATCH FOUND (Substrate Size: {len(registry)} laws).")
        return None

    # 6. CROSS-CORRELATION (Relational Logic)
    results = [item[1] for item in stack]
    print(f"\n[RESONANCE STACK: {len(results)} Laws Found]")
    
    for i, entry in enumerate(results):
        print(f"  {i+1}. [RECALL: {entry['ubp_id']}] (R:{stack[i][0]:.2f})")

    if len(results) > 1:
        # Check for Hamming Proximity between the first two matches
        # This identifies if they are "Geometric Neighbors" in the substrate
        # We use the fingerprint (hash) as the coordinate proxy
        h_dist = sum(1 for a, b in zip(results[0]['fingerprint'], results[1]['fingerprint']) if a != b)
        if h_dist < 32: # Arbitrary threshold for hash-space proximity
            print(f"  [!] RELATION DETECTED: High Geometric Proximity between matches.")
        
        # Check for Tag Overlap
        common_tags = set(results[0].get('tags', [])).intersection(set(results[1].get('tags', [])))
        if common_tags:
            print(f"  [!] RELATION DETECTED: Shared Semantic Anchors: {list(common_tags)}")

    return results[0] # Return primary match for system compatibility

if __name__ == "__main__":
    USER_INPUT = globals().get('USER_INPUT', "water omega anchor")
    run_trigger_logic(USER_INPUT)
