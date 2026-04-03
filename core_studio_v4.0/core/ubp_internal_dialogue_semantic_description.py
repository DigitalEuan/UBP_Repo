import json
import os
import re
from ubp_semantic_engine import UBPSemanticEngine

# --- 1. LOCAL HELPERS (Fixes the ImportError) ---

def _get_vector(entry):
    """Extracts the 24-bit vector from a KB entry."""
    v = entry.get('vector')
    if not v and 'atlas' in entry:
        v = entry['atlas'].get('vector')
    return v

def _hamming(v1, v2):
    """Calculates Hamming distance between two 24-bit lists."""
    if not v1 or not v2: return 99
    return sum(1 for a, b in zip(v1, v2) if a != b)

# --- 2. INITIALIZATION ---

engine = UBPSemanticEngine()
# Load both system and language KBs
engine.load('ubp_system_kb.json', 'ubp_lang_kb_combined_v4.json')

def find_word_for_concept(law_vec):
    """Searches the Language KB for the closest semantic match to a physical vector."""
    best_match = None
    best_d = 999
   
    for uid, entry in engine.lang_kb.items():
        v = _get_vector(entry)
        if v is not None:
            d = _hamming(law_vec, v)
            if d < best_d:
                best_d = d
                best_match = entry
               
    return best_match, best_d

# --- 3. THE DIALOGUE ENGINE ---

def deepest_internal_dialogue(query, max_depth=4, gap_threshold=6):
    print(f"\n{'═'*95}")
    print(f"[Depth 0] Initial Pondering: '{query}'")
    
    current_phrase = query
    chain = []
    seen_physical = set()
    gaps = []
    
    for depth in range(1, max_depth + 1):
        print(f"\n[Depth {depth}] Reflecting on: '{current_phrase[:80]}...'")
        
        # A. Physical Grounding
        results = engine.query(current_phrase, top_k=3)
        
        if not results:
            print("   → [Null Resonance] No physical grounding found.")
            break
        
        # Select top unseen result
        top_res = next((r for r in results if r.ubp_id not in seen_physical), results[0])
        law_id = top_res.ubp_id
        law_entry = engine.system_kb[law_id]
        law_vec = _get_vector(law_entry)
        seen_physical.add(law_id)
        
        print(f"   → [Physical Root] {law_id} (Resonance: {top_res.resonance_score:.4f})")
        
        # B. Lexical Mapping
        word_entry, word_d = find_word_for_concept(law_vec)
        if word_entry:
            word_lex = word_entry.get('lexicon', '')
            word_clean = word_lex.split(']')[0].replace('[', '').split(':')[-1].strip()
            
            if word_d <= gap_threshold:
                print(f"   → [VOCABULARY FOUND] '{word_clean}' (d={word_d})")
                current_phrase = f"How does {word_clean} explain the mechanism of {law_id}?"
            else:
                print(f"   → [LEXICAL GAP] Closest match '{word_clean}' is too far (d={word_d}).")
                gaps.append({"law_id": law_id, "concept": top_res.lexicon})
                current_phrase = top_res.lexicon # Fallback to raw law text
            
            chain.append({"depth": depth, "law": law_id, "word": word_clean, "d": word_d})
        else:
            break

    # --- FINAL SYNTHESIS ---
    print(f"\n{'═'*95}")
    print("[FINAL SYNTHESIS]")
    print("\nThese words mean this:")
    for step in chain:
        if step['d'] <= gap_threshold:
            print(f"  • {step['word']}: Grounded in {step['law']}")
            
    if gaps:
        print("\nThese things need words to be defined like this:")
        for g in gaps:
            print(f"  • For {g['law_id']}: \"{g['concept'][:100]}...\"")
    print(f"{'═'*95}\n")

# --- TEST ---
if __name__ == "__main__":
    deepest_internal_dialogue("What is the relationship between electricity and stability?")