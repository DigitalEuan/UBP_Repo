import json
import numpy as np
from ubp_semantic_engine import UBPSemanticEngine, _get_vector, _hamming

# Initialize the Semantic Engine
engine = UBPSemanticEngine()
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

def deepest_internal_dialogue(query, max_depth=6, gap_threshold=6):
    """
    Fixed + enhanced version:
    - Anti-loop logic is now bullet-proof (no more KeyError)
    - When all top results are seen, safely re-uses first path instead of crashing
    - NEW FINAL OUTPUT SECTION exactly as you asked:
      "These words mean this and these things need words to be defined like this"
    """
    print(f"\n{'═'*95}")
    print(f"[Depth 0] Initial Pondering: '{query}'")
    
    current_phrase = query
    chain = []
    seen_physical = set()
    seen_words = set()
    gaps = []                     # NEW: track lexical gaps for final output
    
    for depth in range(1, max_depth + 1):
        print(f"\n[Depth {depth}] Reflecting deeper on: '{current_phrase[:95]}...'")
        
        # 1. Physical grounding with safe anti-loop
        parsed, results = engine.query(current_phrase, top_k=3, max_hamming=14)  # increased to 3 for better fallback
        
        if not results:
            print("   → [Null Resonance] No physical grounding found at this depth.")
            break
        
        # Choose first unseen result; if none, safely reuse the first (prevents KeyError)
        top_res = None
        for res in results:
            if getattr(res, 'ubp_id', None) not in seen_physical:
                top_res = res
                break
        if top_res is None and results:
            top_res = results[0]   # safe fallback
            print("   → [All top paths already seen — safely reusing first resonance]")
        
        law_id = top_res.ubp_id
        law_lex = top_res.lexicon.split(']')[1].strip() if ']' in top_res.lexicon else top_res.lexicon
        law_entry = engine.system_kb[law_id]
        law_vec = _get_vector(law_entry)
        
        seen_physical.add(law_id)
        
        chain.append({
            "depth": depth,
            "type": "physical",
            "id": law_id,
            "lex": law_lex[:220],
            "hamming": top_res.hamming_distance
        })
        
        print(f"   → [Physical Root] {law_id} (d={top_res.hamming_distance})")
        print(f"      {law_lex[:170]}...")
        
        # 2. Lexicalize
        word_entry, word_d = find_word_for_concept(law_vec)
        word_clean = None
        if word_entry:
            word_lex = word_entry.get('lexicon', word_entry.get('ubp_id', ''))
            word_clean = word_lex.split(']')[0].replace('[', '') if ']' in word_lex else word_entry.get('ubp_id', 'Unknown')
            
            seen_words.add(word_clean)
            
            chain.append({
                "depth": depth,
                "type": "lexical",
                "word": word_clean,
                "lex": word_lex[:220],
                "d": word_d
            })
            
            if word_d <= gap_threshold:
                print(f"   → [VOCABULARY FOUND] '{word_clean}' (d={word_d})")
                print(f"      {word_lex[:170]}...")
            else:
                print(f"   → [LEXICAL GAP DETECTED] Closest '{word_clean}' (d={word_d}) — real thinking required.")
                gaps.append({"law_id": law_id, "concept": law_lex[:180]})  # NEW: record gap
        else:
            print("   → [No lexical match]")
        
        # 3. Smarter next pondering phrase (prevents echo loops)
        if word_clean and word_d <= gap_threshold:
            next_phrase = f"How does the idea of {word_clean} connect to {law_id} when thinking about {query}?"
        elif word_clean:
            next_phrase = f"What deeper layer of meaning does {word_clean} reveal when we examine {law_lex[:80]}?"
        else:
            next_phrase = law_lex[:200]
        
        current_phrase = next_phrase
        
        # Early safety stop
        if depth > 3 and len(set([c.get("id") for c in chain if c["type"]=="physical"])) < 3:
            print("   → [Cycle broken — moving to synthesis]")
            break
    
    # ====================== FINAL OUTPUT SECTION ======================
    print(f"\n{'═'*95}")
    print("[FINAL OUTPUT — These words mean this and these things need words to be defined like this]")
    
    physicals = [c for c in chain if c["type"] == "physical"]
    words = [c for c in chain if c["type"] == "lexical"]
    
    # 1. These words mean this
    print("\nThese words mean this:")
    if words:
        for w in words[:6]:  # limit to keep it readable
            print(f"  • {w['word']}: {w['lex'][:130]}...")
    else:
        print("  • (No words surfaced in this chain)")
    
    # 2. These things need words to be defined like this
    print("\nThese things need words to be defined like this:")
    if gaps:
        for g in gaps:
            print(f"  • For {g['law_id']}: \"{g['concept'][:130]}...\"")
    else:
        print("  • No lexical gaps — the vocabulary covered everything perfectly.")
    
    # Bonus: quick synthesis summary
    print(f"\nOverall insight reached after {len(chain)//2} layers of reflection:")
    if physicals:
        print(f"   Core anchor → {physicals[-1]['id']}  |  {physicals[-1]['lex'][:140]}...")
    
    print(f"\n{'═'*95}")
    print("End of deepest thinking session.\n")

# === TEST QUERIES ===
QUERIES = [
    "how does gold form?",
    "what happens when iron heats?",
    "why is gold stable?",
    "how does energy transfer?",
    "what makes carbon the backbone of life?"
]

print("\n🚀 Initiating FIXED + ENHANCED DEEPEST Recursive Semantic Resolution Loop...")
for q in QUERIES:
    deepest_internal_dialogue(q, max_depth=6, gap_threshold=6)