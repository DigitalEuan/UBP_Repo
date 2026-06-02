"""
Final Verification Script for GLM v2.0
======================================
Verifies the integration of the 30 priority words, the FSM-guided reasoner,
and the response composition logic.
"""
import sys
from pathlib import Path
from fractions import Fraction

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

from glm_zoned_lattice_embedding import ZonedVocabulary, dominant_zone
from glm_lang_database import LANG_DB
from ubp_grammatical_diffusion import GrammaticalDiffusionReasoner
from glm_grammar_patch import build_glm_response

def test_vocabulary_grounding():
    print("--- Testing Vocabulary Grounding ---")
    words_to_check = ["zero", "plus", "is", "golay", "true", "equals", "addition", "stable", "measure"]
    for lemma in words_to_check:
        w = LANG_DB.get(lemma)
        if w:
            z = dominant_zone(w.vector)
            print(f"  {lemma:12s} role={w.role:10s} zone={z} nrci={float(w.nrci):.4f} pure={w.is_zone_pure}")
        else:
            print(f"  {lemma:12s} MISSING")

def test_diffusion_reasoning():
    print("\n--- Testing Diffusion Reasoning ---")
    gdr = GrammaticalDiffusionReasoner(LANG_DB)
    queries = [
        ("zero", "one"),
        ("true", "false"),
        ("golay", "leech"),
        ("addition", "value")
    ]
    for start, target in queries:
        trace = gdr.reason(start, target)
        path_str = " -> ".join(s.word for s in trace.path)
        print(f"  {start} to {target}: success={trace.target_reached} path=[{path_str}]")

def test_response_composition():
    print("\n--- Testing Response Composition ---")
    from dataclasses import dataclass
    @dataclass
    class MockRoot:
        ubp_id: str
        resonance: float
        nrci: float
        lexicon: str
        vector: list

    roots = [MockRoot("PARTICLE_ELECTRON_001", 1.0, 0.7857, "electron", [0]*24)]

    response = build_glm_response(roots, [], "What is an electron?")
    print(f"  Query: What is an electron?\n  Response: {response}")

if __name__ == "__main__":
    test_vocabulary_grounding()
    test_diffusion_reasoning()
    test_response_composition()
