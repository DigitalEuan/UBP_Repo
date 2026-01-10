"""
UBP Auto-Trigger v5.6 (Reflexive Encapsulation)
===============================================
Optimized for high-density substrates (196+ laws).
Implements Fuzzy Anchor Matching to bridge the Resonance Gap.

E R A Craig, New Zealand
10 Jan 2026
"""
import re
import json
from hex_dictionary_v4_exact import HEX_DB_EXACT

def run_trigger_logic(input_text=None):
    """
    Encapsulated logic for UBP Resonance Scanning.
    Variables are local to this scope to prevent namespace pollution.
    """
    # 1. Resolve Input (Global injection or direct argument)
    target_text = input_text if input_text else globals().get('USER_INPUT', "")
    if not target_text:
        return None

    # 2. Substrate Integrity Check
    if not HEX_DB_EXACT.registry:
        HEX_DB_EXACT.load_memory()
    
    registry = HEX_DB_EXACT.registry
    if not registry:
        print("[!] CRITICAL: Substrate is empty.")
        return None

    # 3. Pre-Processing
    def tokenize(text):
        return set(re.sub(r'[^a-zA-Z0-9\s]', '', text.lower()).split())

    input_lower = target_text.lower().strip()
    input_tokens = tokenize(input_lower)
    
    # 4. TIER 1: FUZZY ANCHOR SCAN (Highest Priority)
    # Checks for partial matches in ID or Name (e.g., "baryon" matches "LAW_BARYON_001")
    for f_print, entry in registry.items():
        name = entry.get("name", "").lower()
        ubp_id = entry.get("ubp_id", "").lower()
        
        if input_lower in name or input_lower in ubp_id:
            print(f"[RECALL: {entry['ubp_id']}] via Fuzzy Anchor.")
            return entry

    # 5. TIER 2: SEMANTIC RESONANCE (Jaccard)
    # Fallback for conceptual queries that don't share keywords with the title
    best_match = None
    highest_jaccard = 0.0
    ADAPTIVE_THRESHOLD = 0.12 # Lowered for short queries

    for f_print, entry in registry.items():
        # Build profile from tags, name, and ID
        profile = set(entry.get("tags", []))
        profile.update(tokenize(entry.get("name", "")))
        profile.update(tokenize(entry.get("ubp_id", "")))
        
        intersection = input_tokens.intersection(profile)
        union = input_tokens.union(profile)
        
        if not union: continue
        score = len(intersection) / len(union)
        
        if score > highest_jaccard:
            highest_jaccard = score
            best_match = entry

    # 6. Final Resolution
    if best_match and highest_jaccard >= ADAPTIVE_THRESHOLD:
        print(f"[RECALL: {best_match['ubp_id']}] via Semantic Resonance (J:{highest_jaccard:.2f}).")
        return best_match

    # 7. Failsafe: Substrate Size Diagnostic
    print(f"NO MATCH FOUND (Substrate Size: {len(registry)} laws).")
    return None

# --- Execution Bridge ---
if __name__ == "__main__":
    # The app injects USER_INPUT globally.
    USER_INPUT = globals().get('USER_INPUT', "periodic singularity")
    run_trigger_logic(USER_INPUT)
