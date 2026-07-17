"""
CritPt Diagnostic Script
========================
Evaluates GLM grounding coverage and reasoning success for CritPt problems.
"""
import json
import re
from glm_lang_database import LANG_DB
from ubp_grammatical_diffusion import GrammaticalDiffusionReasoner

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
    results = []

    print(f"{'Problem ID':20s} | {'Grounding %':12s} | {'Path Success'}")
    print("-" * 50)

    for entry in critpt_data[:10]: # Test first 10
        pid = entry['problem_id']
        desc = entry['problem_description']

        # 1. Check Grounding
        words = re.findall(r'\b[a-zA-Z]{4,}\b', desc.lower())
        unique_words = set(words)
        grounded = [w for w in unique_words if LANG_DB.get(w)]
        grounding_pct = len(grounded) / len(unique_words) if unique_words else 0

        # 2. Test reasoning between first two grounded nouns
        nouns = [w for w in grounded if LANG_DB.get(w).role == "NOUN"]
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
