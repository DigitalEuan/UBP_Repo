from typing import Dict, List

# Canonical UBP harmonic ratios
CANONICAL_RATIOS: List[float] = [0.354, 0.500, 0.707, 1.000]

# UBP constant signatures
UBP_SIGNATURES: Dict[str, Dict] = {
    "c": {
        "ratios": [1.000, 0.354, 0.354],
        "rune_match": ["Fehu", "Uruz"],
        "geometric_family": "Kinetic Diagonal",
    },
    "mu0": {
        "ratios": [1.000, 1.000],
        "rune_match": ["Gebo", "Hagalaz"],
        "geometric_family": "Cubic/Octahedral",
    },
    "G": {
        "ratios": [0.500, 0.500, 0.500, 0.500],
        "rune_match": ["Ingwaz"],
        "geometric_family": "Structural Enclosure",
    },
    "hybrid": {
        "ratios": [1.000, 0.354, 0.500],
        "rune_match": ["Fehu", "Ingwaz"],
        "geometric_family": "Multi-Constant Fusion",
    },
}


def expected_signature_for_trigger(trigger_class: str) -> Dict:
    return UBP_SIGNATURES.get(trigger_class, {})
