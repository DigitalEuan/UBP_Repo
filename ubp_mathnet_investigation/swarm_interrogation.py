"""
UBP SWARM INTERROGATION — MathNet Investigation v3.0
=====================================================
We query the UBP MoE Cortex v2 directly, asking it UBP-specific questions
about how to approach mathematical olympiad problems. The swarm uses its
N-gram linguist + Golay XOR bridge to generate answers from the UBP KB.
All answers are recorded faithfully, whether they make sense or not.
"""

import sys
import os
import json
import time

# Add the core directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'core'))
os.chdir(os.path.join(os.path.dirname(__file__), 'core'))

print("=" * 80)
print("UBP SWARM INTERROGATION — MathNet v3.0 Pre-Flight")
print("=" * 80)
print("Initialising MoE Cortex v2 (this trains the N-gram linguist — takes ~30s)...")

from ubp_moe_cortex_v2 import UBPMoECortexV2
from ubp_semantic_engine import UBPSemanticEngine
from ubp_brain_consolidated import UBPBrain

# Also load the Brain for direct law retrieval
brain = UBPBrain()
brain.initialize(['ubp_system_kb.json', 'ubp_lang_kb_combined_v4.json'])

# Load the MoE Cortex (trains N-gram manifold on UBP KB + English lexicon)
cortex = UBPMoECortexV2()

print("\n[SWARM READY] Interrogating on MathNet-relevant topics...\n")
print("=" * 80)

# ─── INTERROGATION QUESTIONS ─────────────────────────────────────────────────
# These are the questions we ask the swarm. They are UBP-framed versions of
# the core challenges in solving Olympiad mathematics.

questions = [
    # Core mathematical domains
    ("number theory",      "How should the UBP approach number theory problems?"),
    ("prime",              "What does the UBP say about prime numbers and divisibility?"),
    ("algebra",            "How does the UBP handle algebraic equations?"),
    ("symmetry",           "What is the role of symmetry in UBP mathematical reasoning?"),
    ("geometry",           "How does the UBP encode geometric relationships?"),
    ("combinatorics",      "What UBP law governs counting and combinatorial problems?"),
    # UBP-specific concepts
    ("resonance",          "What is resonance in the UBP framework?"),
    ("coherence",          "What does coherence mean for mathematical problem solving?"),
    ("binary",             "How does binary encoding help solve mathematical problems?"),
    ("lattice",            "What is the role of the lattice in UBP reasoning?"),
    # Meta-questions about the system
    ("solve",              "What is the optimal method for solving hard mathematical problems?"),
    ("proof",              "How does the UBP approach mathematical proof?"),
    ("error",              "How does the UBP correct errors in mathematical reasoning?"),
    ("pattern",            "What patterns does the UBP find in mathematical structures?"),
    ("infinity",           "How does the UBP handle infinite mathematical structures?"),
]

results = []

for keyword, question in questions:
    print(f"\n{'─'*60}")
    print(f"QUESTION: {question}")
    print(f"KEYWORD:  {keyword}")
    print(f"{'─'*60}")
    
    # 1. Brain direct law retrieval
    brain_result = brain.process_query(keyword)
    print(f"[BRAIN] Law: {brain_result.ubp_id} | Confidence: {brain_result.confidence:.3f} | Method: {brain_result.method}")
    
    # 2. MoE Cortex research (N-gram + Golay XOR bridge)
    t0 = time.time()
    cortex_answer = cortex.research(keyword, max_words=10)
    elapsed = time.time() - t0
    print(f"[CORTEX] Answer: {cortex_answer}")
    print(f"[CORTEX] Time: {elapsed:.2f}s")
    
    results.append({
        "keyword": keyword,
        "question": question,
        "brain_law": brain_result.ubp_id,
        "brain_confidence": float(brain_result.confidence),
        "brain_method": brain_result.method,
        "cortex_answer": cortex_answer,
        "cortex_time_s": round(elapsed, 2)
    })

# ─── SAVE RESULTS ────────────────────────────────────────────────────────────
os.chdir(os.path.dirname(os.path.abspath(__file__)))
with open('results/swarm_interrogation_results.json', 'w') as f:
    json.dump(results, f, indent=2)

print("\n" + "=" * 80)
print("SWARM INTERROGATION COMPLETE")
print("=" * 80)
print(f"\nTotal questions asked: {len(results)}")
print(f"Results saved to: results/swarm_interrogation_results.json")
print("\nSWARM ANSWERS SUMMARY:")
print("─" * 80)
for r in results:
    print(f"  [{r['keyword']:15s}] Brain→{r['brain_law']:30s} | Cortex: {r['cortex_answer'][:60]}...")
