"""
UBP Auto-Trigger v10.0 (Bicameral Cortex)
=========================================
Merges:
1. Keyword/Vector Harvesting (v8.1) - Precision
2. Synthesis Navigation (v9.0) - Reasoning
3. Hemispheric Construction (v9.3) - Intuition

Goal: If we can't find the words, we build the geometry and look for neighbors.
"""
import json
import sys
from typing import List, Dict

# Import Core Systems
try:
    from hex_dictionary_v4_exact import HEX_DB_EXACT
    from ubp_core_v4_2_6_COMBINED import GOLAY_DECODER, BinaryLinearAlgebra
    from ubp_fom_system import FOM_MANAGER
    
    # Import the v9.3 Logic (Renamed/Aliased for clarity)
    # Assuming the file is named 'auto_trigger_v9.3.py' in the workspace
    import auto_trigger_v9_3 as bicameral
except ImportError as e:
    print(f"[Cortex] Import Error: {e}")
    # Mocking for standalone test if files missing
    bicameral = None

# --- HYDRATE ---
if not HEX_DB_EXACT.registry:
    HEX_DB_EXACT.load_memory()

def get_hamming_distance(v1, v2):
    return BinaryLinearAlgebra.hamming_distance(v1, v2)

def bicameral_scan(text: str) -> List[Dict]:
    """Uses v9.3 logic to construct a vector from raw text."""
    if not bicameral or not text: return []
    
    cortex = bicameral.RationalHemisphericCortex()
    # 1. Generate the 'Intuition' Vector
    res = cortex.process(text)
    
    # 2. Reconstruct the full 24-bit vector from LH + RH
    # Note: v9.3 returns LH and RH parts. We need the 'healed' vector.
    # The 'process' method in v9.3 calculates 'healed' internally but returns parts.
    # We will re-run the decode/encode here to be sure.
    raw_combined = res['lh'] + res['rh']
    decoded, _, _ = GOLAY_DECODER.decode(raw_combined)
    query_vec = GOLAY_DECODER.encode(decoded)
    
    # 3. Find Resonance in DB
    matches = []
    for fp, entry in HEX_DB_EXACT.registry.items():
        if not entry.get('vector'): continue
        dist = get_hamming_distance(query_vec, entry['vector'])
        
        # If the constructed thought is close to a memory (Dist <= 6)
        if dist <= 6:
            entry = entry.copy()
            entry['match_type'] = f"BICAMERAL_INTUITION (d={dist})"
            entry['domain_lock'] = res['domain']
            matches.append(entry)
            
    return matches

def reflexive_recall_v10(text, ai_vectors=None):
    print(f"[Cortex v10] Analyzing: '{text}'")
    
    # 1. Standard Harvest (Keywords/AI)
    # (Simplified for this demo, usually calls harvest_seeds from v8.1)
    seeds = [] 
    # ... [Insert v8.1 harvest logic here] ...
    
    # 2. If seeds are low, engage Bicameral Intuition
    if len(seeds) < 2:
        print("  > Keywords scarce. Engaging Hemispheric Cortex...")
        intuition_seeds = bicameral_scan(text)
        if intuition_seeds:
            print(f"  > Intuition found {len(intuition_seeds)} resonances.")
            seeds.extend(intuition_seeds)
    
    # 3. Synthesis & Expansion (v8.1 Logic)
    # ... [Insert Synthesis/Expansion logic here] ...
    
    # For demonstration, just print what Intuition found
    if seeds:
        print(json.dumps(seeds[:3], indent=2))
    else:
        print("  > No resonance found via Keyword or Intuition.")

if __name__ == "__main__":
    # Test with a phrase that might not have exact keywords but has strong "Physics" vibes
    reflexive_recall_v10("The fundamental vibration of the universe")
