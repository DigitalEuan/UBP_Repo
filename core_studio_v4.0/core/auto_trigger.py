"""
UBP Auto-Trigger v15.0 (Brain-Consolidated)
============================================
INTEGRATION: Swaps legacy Delta Engine for UBPBrain Consolidated v2.
Provides high-coherence context injection using v5.3 Merged Core.

Author: E R A Craig, New Zealand
Date: 17 Feb 2026
"""
import json
import sys
import re
import os
import hashlib
from typing import List, Dict, Any

# --- CORE BRAIN IMPORT ---
try:
    from ubp_brain_consolidated import UBPBrain
    from hex_dictionary_v4_exact import HEX_DB_EXACT
    from ubp_core_v5_3_merged import GOLAY_ENGINE
    
    # Initialize the Consolidated Brain
    BRAIN = UBPBrain()
    kb_files = ['ubp_system_kb.json']
    if os.path.exists('ubp_atlas.json'):
        kb_files.append('ubp_atlas.json')
    
    BRAIN.initialize(kb_files)
    print(f"[Cortex v15.0] Brain Initialized with {len(BRAIN.memory.kb)} entries.")

except ImportError as e:
    print(f"[Reflexive Cortex] CRITICAL IMPORT ERROR: {e}")
    sys.exit(0)

def reflexive_recall(text):
    print(f"[Cortex v15.0] Processing Input via Consolidated Brain...")
    memories = []

    # 1. Fast Path: Direct IDs (Regex)
    ids = re.findall(r'\b[A-Z]+_[A-Z0-9_]+_\d+\b', text)
    for uid in ids:
        entry = HEX_DB_EXACT.find_by_id(uid)
        if entry:
            e = entry.copy()
            e['match_type'] = "DIRECT_ID_REF"
            memories.append(e)

    # 2. Deep Path: Consolidated Brain Reasoning
    # This replaces the old Delta Engine loop
    brain_result = BRAIN.process_query(text)
    
    # Inject the primary concept found by the brain
    if brain_result.primary_concept:
        concept = brain_result.primary_concept.to_dict()
        concept['match_type'] = "BRAIN_PRIMARY_RESONANCE"
        memories.append(concept)

    # Inject the reasoning chain steps as contextual memories
    for step in brain_result.reasoning_chain:
        step_mem = step.concept.to_dict()
        step_mem['match_type'] = f"BRAIN_CHAIN_{step.operation.upper()}"
        memories.append(step_mem)

    # 3. Deduplicate and Format for AI Context
    seen_ids = set()
    final_context = []
    
    # Add the Brain's synthesized response as a system hint
    final_context.append({
        "ubp_id": "SYS_BRAIN_SYNTHESIS",
        "name": "Brain Synthesis Hint",
        "language": brain_result.response,
        "nrci": str(brain_result.final_nrci),
        "warnings": brain_result.warnings
    })

    for m in memories:
        uid = m.get('ubp_id', 'UNK')
        if uid not in seen_ids:
            final_context.append(m)
            seen_ids.add(uid)

    print(f"--- REFLEXIVE MEMORY: {len(final_context)} ENTRIES INJECTED ---")
    # In the real App, this JSON is what gets injected into the prompt
    return final_context

if __name__ == "__main__":
    # Test with the query that started it all
    u_input = globals().get('USER_INPUT', "What is the relationship between an electron and logic?")
    results = reflexive_recall(u_input)
    print(json.dumps(results, indent=2))