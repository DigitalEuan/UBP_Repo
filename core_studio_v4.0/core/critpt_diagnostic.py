"""
CritPt Diagnostic Script
========================
Evaluates GLM grounding coverage and reasoning success for CritPt problems.
"""
import json
import re
from glm_lang_database import LANG_DB
from ubp_grammatical_diffusion import GrammaticalDiffusionReasoner
from glm_multi_token_lexer import build_lexer_from_vocab

from dataclasses import dataclass

@dataclass
class MockRoot:
    ubp_id: str
    resonance: float
    nrci: float
    vector: list
    lexicon: str = ""

def run_diagnostic():
    with open('critpt.json', 'r') as f:
        critpt_data = json.load(f)

    gdr = GrammaticalDiffusionReasoner(LANG_DB)
    lexer = build_lexer_from_vocab(LANG_DB)
    results = []

    print(f"{'Problem ID':20s} | {'Grounding %':12s} | {'Path Success'}")
    print("-" * 50)

    for entry in critpt_data[:10]: # Test first 10
        pid = entry['problem_id']
        desc = entry['problem_description']

        # 1. Check Grounding using the MultiTokenLexer
        tokens = lexer.tokenise(desc)
        unique_tokens = set(tokens)
        grounded = [t for t in unique_tokens if LANG_DB.get(t)]
        grounding_pct = len(grounded) / len(unique_tokens) if unique_tokens else 0

        # 2. Test reasoning between first two grounded nouns
        nouns = [t for t in grounded if LANG_DB.get(t).role == "NOUN"]
        success = False
        if len(nouns) >= 2:
            trace = gdr.reason(nouns[0], nouns[1])
            success = trace.target_reached

        print(f"{pid:20s} | {grounding_pct:12.2%} | {success}")

        results.append({
            "pid": pid,
            "grounding_pct": grounding_pct,
            "success": success,
            "grounded": grounded
        })

    return results

if __name__ == "__main__":
    run_diagnostic()
