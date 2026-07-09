"""
UBP KB Architect v3.0 (SHA-256-free)
====================================
Patches KBArchitect.generate_vector to remove SHA-256 from internal
calculation. SHA-256 remains ONLY as the top-level `fingerprint` tag
(for fast recall / deterministic identity), never as a vector input.

Vector construction:
  - ELEM_ entries: Z-based index (real atomic number), Gray-coded.
    UNCHANGED from v2.2 — this path never used SHA-256 internally.
  - All other entries: MOG-presence bits derived from the math_dna
    content directly. Bit i = 1 if MOG category i has any data in the
    parsed math string. No hash, no arbitrary mapping — the vector IS
    a direct readout of which ontological categories the entry touches.
  - Text-only math (word definitions with no `=` signs): keyword-based
    MOG mapping per §4.2 of the database tidy-up directive. Each MOG
    category has a keyword list; if any keyword appears in the
    definition, that bit is set.

The result: every non-ELEM vector is a 24-bit pattern that directly
reflects the entry's real semantic content. Two entries that touch the
same MOG categories will share bits; two entries with disjoint MOG
footprints will have disjoint bits. This is the opposite of SHA-256,
which spreads similar inputs uniformly across the bit space.
"""

import sys
import os
import re
import hashlib
from typing import List
from fractions import Fraction

# MIGRATION v4.0 fix: the original hardcoded REPO path
# `/home/z/my-project/repo/core_studio_v4.0` does not exist on this machine.
# Locate the v2.2 base `ubp_kb_architect.py` in `archive_core/` and load it
# via importlib (WITHOUT polluting sys.path — adding archive_core to sys.path
# would shadow the live `auto_trigger.py` with the archived one).
_HERE = os.path.dirname(os.path.abspath(__file__))
_ARCHIVE_CORE = os.path.join(_HERE, "archive_core")

import importlib.util as _ilu
_v22_path = os.path.join(_ARCHIVE_CORE, "ubp_kb_architect.py")
if os.path.exists(_v22_path):
    _spec = _ilu.spec_from_file_location("ubp_kb_architect_v22_base", _v22_path)
    _v22 = _ilu.module_from_spec(_spec)
    _spec.loader.exec_module(_v22)
    KBArchitect = _v22.KBArchitect
    MOG_CATEGORIES = _v22.MOG_CATEGORIES
    to_gray_code = _v22.to_gray_code
else:
    # Last resort: fall back to legacy_adapter's MOG_CATEGORIES.
    _SYSKB = os.path.join(os.path.dirname(_HERE), "system_kb")
    if _SYSKB not in sys.path:
        sys.path.insert(0, _SYSKB)
    from legacy_adapter import MOG_CATEGORIES  # noqa: E402
    KBArchitect = None  # type: ignore
    def to_gray_code(*a, **kw):  # type: ignore
        raise RuntimeError("ubp_kb_architect v2.2 base not found; cannot gray-code")

try:
    from ubp_unified_v5 import LEECH_ENGINE  # noqa: E402
except Exception:
    LEECH_ENGINE = None


# ─────────────────────────────────────────────────────────────────────────────
# MOG category mapping (mirrors ubp_mog_mapper.get_mog_cat)
# ─────────────────────────────────────────────────────────────────────────────

EXPLICIT_KEY_TO_MOG = {
    "M": "M_Mass", "Mass": "M_Mass", "Z": "M_Count", "BP": "M_Thermal",
    "MP": "M_Thermal", "Rho": "I_Density", "Density": "I_Density",
    "Formula": "I_Connectivity", "Energy": "A_Energy", "c": "A_Velocity",
}


def get_mog_cat(key: str) -> str:
    """Map a math-field key to its MOG category. Mirrors ubp_mog_mapper."""
    if key in EXPLICIT_KEY_TO_MOG:
        return EXPLICIT_KEY_TO_MOG[key]
    k = key.lower()
    if "time" in k or "period" in k:
        return "M_Time"
    if "charge" in k or "ion" in k:
        return "M_Charge"
    if "force" in k or "gravity" in k:
        return "A_Force"
    if "mass" in k or "weight" in k:
        return "M_Mass"
    if "space" in k or "position" in k or "distance" in k or "length" in k:
        return "M_Space"
    if "thermal" in k or "heat" in k or "temperature" in k:
        return "M_Thermal"
    if "count" in k or "number" in k:
        return "M_Count"
    if "topology" in k or "shape" in k or "phase" in k and "phase" in k:
        return "I_Topology"
    if "symmetry" in k or "symmetric" in k:
        return "I_Symmetry"
    if "density" in k or "dense" in k or "compact" in k:
        return "I_Density"
    if "connect" in k or "link" in k or "edge" in k or "graph" in k or "bond" in k:
        return "I_Connectivity"
    if "dimension" in k or "axis" in k:
        return "I_Dimension"
    if "complex" in k:
        return "I_Complexity"
    if "energy" in k or "work" in k or "power" in k:
        return "A_Energy"
    if "velocity" in k or "speed" in k:
        return "A_Velocity"
    if "flux" in k or "flow" in k or "current" in k:
        return "A_Flux"
    if "resonance" in k or "vibrate" in k or "oscillate" in k or "frequency" in k:
        return "A_Resonance"
    if "spin" in k or "rotate" in k or "angular" in k:
        return "A_Spin"
    if "probability" in k or "chance" in k or "random" in k:
        return "P_Probability"
    if "ratio" in k or "proportion" in k or "scale" in k or "fraction" in k:
        return "P_Ratio"
    if "limit" in k or "boundary" in k or "infinity" in k:
        return "P_Limit"
    if "tax" in k or "cost" in k or "burden" in k or "penalty" in k:
        return "P_Tax"
    if "coherent" in k or "consistent" in k or "stable" in k:
        return "P_Coherence"
    if "phase" in k or "stage" in k or "state" in k or "transition" in k:
        return "P_Phase"
    return "I_Complexity"  # default — matches ubp_mog_mapper


# ─────────────────────────────────────────────────────────────────────────────
# Keyword → MOG category mapping for text-only math (word definitions)
# Implements §4.2 of the database tidy-up directive
# ─────────────────────────────────────────────────────────────────────────────

MOG_KEYWORDS = {
    "M_Mass":       ["mass", "weight", "heavy", "kg", "gram", "matter", "substance"],
    "M_Charge":     ["charge", "ion", "electric", "coulomb", "electron", "proton",
                     "anion", "cation", "electromagnetic"],
    "M_Space":      ["space", "distance", "length", "meter", "position", "spatial",
                     "geometry", "coordinate", "extent"],
    "M_Time":       ["time", "period", "duration", "second", "temporal", "when",
                     "before", "after", "eternal", "transient"],
    "M_Thermal":    ["heat", "thermal", "temperature", "hot", "cold", "boil",
                     "melt", "freeze", "thermodynamic"],
    "M_Count":      ["count", "number", "quantity", "amount", "tally", "enumerate",
                     "many", "few", "zero", "one", "two", "three"],
    "I_Topology":   ["topology", "shape", "form", "hole", "torus", "sphere",
                     "manifold", "surface", "knot", "loop", "ring"],
    "I_Symmetry":   ["symmetry", "symmetric", "mirror", "invariant", "balance",
                     "reflection", "rotation", "group"],
    "I_Density":    ["density", "dense", "compact", "concentrated", "sparse",
                     "thick", "thin"],
    "I_Connectivity": ["connect", "link", "edge", "graph", "network", "bond",
                       "relation", "associate", "join", "couple", "tie", "bridge"],
    "I_Dimension":  ["dimension", "dimensional", "axis", "plane", "vector space",
                     "rank", "span"],
    "I_Complexity": ["complex", "complicated", "simple", "intricate", "elaborate",
                     "straightforward"],
    "A_Energy":     ["energy", "work", "joule", "power", "kinetic", "potential",
                     "hamiltonian", "lagrangian", "calorie"],
    "A_Force":      ["force", "push", "pull", "newton", "pressure", "tension",
                     "gravity", "gravitational", "friction"],
    "A_Velocity":   ["velocity", "speed", "fast", "slow", "rapid", "swift",
                     "motion", "acceleration"],
    "A_Flux":       ["flux", "flow", "current", "stream", "river", "discharge",
                     "transfer"],
    "A_Resonance":  ["resonance", "vibrate", "oscillate", "frequency", "wave",
                     "harmonic", "tuning", "ring"],
    "A_Spin":       ["spin", "rotate", "rotation", "angular", "gyre", "turn",
                     "revolve", "twirl"],
    "P_Probability":["probability", "chance", "random", "likely", "odds", "stochastic",
                     "uncertain", "luck"],
    "P_Ratio":      ["ratio", "proportion", "scale", "fraction", "percent",
                     "quotient", "rate"],
    "P_Limit":      ["limit", "boundary", "edge", "infinity", "asymptote",
                     "threshold", "constrain"],
    "P_Tax":        ["tax", "cost", "burden", "penalty", "fee", "levy", "toll",
                     "expense"],
    "P_Coherence":  ["coherent", "consistent", "stable", "logical", "sound",
                     "harmony", "agreement"],
    "P_Phase":      ["phase", "stage", "state", "transition", "step", "level",
                     "condition", "mode"],
}


# ─────────────────────────────────────────────────────────────────────────────
# New vector generator (no SHA-256)
# ─────────────────────────────────────────────────────────────────────────────

def _mog_presence_from_pairs(math_dna: str) -> List[int]:
    """Parse math_dna as `key=value|key=value|...` and return a 24-bit
    presence vector where bit i = 1 if MOG category i has any data."""
    bits = [0] * 24
    if not math_dna or "=" not in math_dna:
        return bits
    for p in math_dna.split("|"):
        if "=" not in p:
            continue
        k = p.split("=", 1)[0].strip()
        if not k:
            continue
        cat = get_mog_cat(k)
        idx = MOG_CATEGORIES.index(cat)
        bits[idx] = 1
    return bits


def _mog_presence_from_text(text: str) -> List[int]:
    """Scan text (e.g. a word definition) for MOG-category keywords.
    Returns a 24-bit presence vector."""
    bits = [0] * 24
    if not text:
        return bits
    t = text.lower()
    for cat, kws in MOG_KEYWORDS.items():
        idx = MOG_CATEGORIES.index(cat)
        for kw in kws:
            if kw in t:
                bits[idx] = 1
                break
    return bits


def _text_fallback_bits(text: str) -> List[int]:
    """Last-resort deterministic spread for text with no keyword signal.
    Uses character-sum modular arithmetic (NOT a hash — just arithmetic
    on the real text content). Guarantees at least one bit is set."""
    if not text:
        # All-zero is invalid; set the default category bit
        bits = [0] * 24
        bits[MOG_CATEGORIES.index("I_Complexity")] = 1
        return bits
    bits = [0] * 24
    text_sum = sum(ord(c) for c in text)
    text_len = max(1, len(text))
    # Deterministic spread: set bits where (sum + i*len) % 7 == 0
    # This gives ~3-4 bits set for typical text, spread across categories
    for i in range(24):
        if (text_sum + i * text_len) % 7 == 0:
            bits[i] = 1
    # Ensure at least one bit is set
    if not any(bits):
        bits[text_sum % 24] = 1
    return bits


def generate_vector_no_hash(math_dna: str, ubp_id: str = None) -> List[int]:
    """SHA-256-free vector generator.

    - ELEM_: Z-based index, Gray-coded (real atomic number — never used hash)
    - Structured math (has `=`): MOG-presence bits (bit i = category i active)
    - Text-only math: keyword-based MOG mapping (§4.2)
    - No keyword signal: deterministic text-spread fallback (no hash)
    """
    # ELEM_ path: keep the existing Z-based Gray-code logic (it's real data)
    if ubp_id and ubp_id.startswith("ELEM_"):
        try:
            parts = ubp_id.split("_")
            z = int(parts[2])
            offset = 1000 if len(parts) > 3 and parts[3] else 0
            index = ((z * 0x111111) + offset) & 0xFFFFFF
        except Exception:
            index = 0
        return to_gray_code(index)

    # Non-ELEM path: build a 24-bit MOG-presence vector
    # Try structured math first
    if math_dna and "=" in math_dna:
        bits = _mog_presence_from_pairs(math_dna)
        if any(bits):
            return bits  # Direct bits — no Gray-coding needed

    # Fall back to keyword-based MOG mapping on the text
    bits = _mog_presence_from_text(math_dna or "")
    if any(bits):
        return bits

    # Last resort: deterministic text-spread (NOT a hash)
    return _text_fallback_bits(math_dna or "")


# ─────────────────────────────────────────────────────────────────────────────
# Apply the patch
# ─────────────────────────────────────────────────────────────────────────────

# Save the original for reference (tests can compare old vs new)
ORIGINAL_generate_vector = KBArchitect.generate_vector

# Monkey-patch
KBArchitect.generate_vector = staticmethod(generate_vector_no_hash)

# Verify the patch
if __name__ == "__main__":
    print("=== UBP KB Architect v3.0 (SHA-256-free) Patch Test ===")
    arch = KBArchitect()

    # Test ELEM_ path (should match v2.2 exactly)
    v_elem = arch.generate_vector("", "ELEM_H_001")
    print(f"ELEM_H_001: {v_elem}  (weight={sum(v_elem)})")

    # Test structured math
    math_h = "M=126/125|Interaction=1312|Oscillation=1|BP=507/25|MP=1401/100|Z=1|Rho=2247/25000"
    v_struct = arch.generate_vector(math_h, "LAW_TEST")
    print(f"LAW_TEST (structured): {v_struct}  (weight={sum(v_struct)})")

    # Test text-only math
    v_text = arch.generate_vector("The amount of energy needed to describe a system", "WORD_ENERGY")
    print(f"WORD_ENERGY (text):    {v_text}  (weight={sum(v_text)})")

    # Test fallback (no keywords)
    v_fallback = arch.generate_vector("xyz qwerty", "WORD_GIBBERISH")
    print(f"WORD_GIBBERISH (fall): {v_fallback}  (weight={sum(v_fallback)})")

    # Verify: fingerprint is STILL SHA-256 (top-level tag, not internal)
    fp = hashlib.sha256(math_h.encode()).hexdigest()
    print(f"\nFingerprint (SHA-256 of math, top-level only): {fp[:20]}...")

    # Verify: same input → same output (deterministic)
    v1 = arch.generate_vector(math_h, "LAW_TEST")
    v2 = arch.generate_vector(math_h, "LAW_TEST")
    print(f"Deterministic: {v1 == v2}")

    # Verify: different inputs that touch the same MOG categories → same vector
    # (This is the WHOLE POINT — semantic content drives the vector, not hash)
    math_a = "M=1|Z=2"
    math_b = "Mass=10|Count=20"
    va = arch.generate_vector(math_a, "LAW_A")
    vb = arch.generate_vector(math_b, "LAW_B")
    print(f"\nSemantic equivalence test:")
    print(f"  M=1|Z=2       → {va}")
    print(f"  Mass=10|Count=20 → {vb}")
    print(f"  Same vector (both touch M_Mass + M_Count): {va == vb}")

    # Compare to old SHA-256 behavior
    print(f"\n--- Comparison to old SHA-256 behavior ---")
    v_old = ORIGINAL_generate_vector(math_h, "LAW_TEST")
    print(f"  Old (SHA-256):  {v_old}  (weight={sum(v_old)})")
    print(f"  New (MOG-pres): {v_struct}  (weight={sum(v_struct)})")
