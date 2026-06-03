"""
GLM Language Database — Priority Vocabulary v2.2
================================================
Grounded entries related to mathematical and substrate concepts.
Expanded with Tiers 10 and 11 (Structural and Physical Parameters).
"""
from glm_zoned_lattice_embedding import ZonedVocabulary

def build_priority_vocabulary() -> ZonedVocabulary:
    vocab = ZonedVocabulary()

    # Tier 1 — Boolean Primitives (math_equivalent defined)
    vocab.add("zero",    "NOUN", "M_Count",      math_equivalent=0)
    vocab.add("one",     "NOUN", "M_Count",      math_equivalent=1)
    vocab.add("true",    "NOUN", "P_Coherence",  math_equivalent=1)
    vocab.add("false",   "NOUN", "P_Coherence",  math_equivalent=0)
    vocab.add("yes",     "NOUN", "P_Coherence",  math_equivalent=1)
    vocab.add("no",      "NOUN", "P_Coherence",  math_equivalent=0)

    # Tier 2 — Arithmetic Operators (math_equivalent = op code)
    vocab.add("equals",       "OPERATOR", "P_Coherence",     math_equivalent=0)
    vocab.add("plus",         "OPERATOR", "A_Energy",        math_equivalent=1)
    vocab.add("minus",        "OPERATOR", "A_Energy",        math_equivalent=2)
    vocab.add("times",        "OPERATOR", "A_Force",         math_equivalent=3)
    vocab.add("divided_by",   "OPERATOR", "P_Ratio",         math_equivalent=4)
    vocab.add("greater_than", "OPERATOR", "P_Limit",         math_equivalent=5)
    vocab.add("less_than",    "OPERATOR", "P_Limit",         math_equivalent=6)
    vocab.add("not",          "OPERATOR", "P_Coherence",     math_equivalent=7)
    vocab.add("and",          "OPERATOR", "I_Connectivity",  math_equivalent=8)
    vocab.add("or",           "OPERATOR", "I_Connectivity",  math_equivalent=9)

    # Tier 3 — Substrate-Native Nouns (already grounded in UBP)
    vocab.add("golay",    "NOUN", "I_Symmetry")
    vocab.add("leech",    "NOUN", "I_Dimension")
    vocab.add("octad",    "NOUN", "M_Count")
    vocab.add("dodecad",  "NOUN", "M_Count")
    vocab.add("prime",    "NOUN", "I_Topology")
    vocab.add("nrci",     "NOUN", "P_Coherence")
    vocab.add("codeword", "NOUN", "I_Symmetry")
    vocab.add("weight",   "NOUN", "M_Count")
    vocab.add("lattice",  "NOUN", "I_Dimension")
    vocab.add("triad",    "NOUN", "A_Resonance")

    # Tier 4 — Substrate Verbs (FSM-critical connectives)
    vocab.add("is",       "VERB", "P_Coherence")
    vocab.add("has",      "VERB", "I_Connectivity")
    vocab.add("equals_v", "VERB", "P_Coherence")
    vocab.add("contains", "VERB", "I_Connectivity")
    vocab.add("requires", "VERB", "A_Force")

    # Tier 5 — Grounded Extensions (Logic / Meta)
    vocab.add("addition",       "NOUN", "A_Energy")
    vocab.add("subtraction",    "NOUN", "A_Energy")
    vocab.add("multiplication", "NOUN", "A_Force")
    vocab.add("division",       "NOUN", "P_Ratio")
    vocab.add("result",      "NOUN", "P_Phase")
    vocab.add("value",       "NOUN", "M_Count")
    vocab.add("stable",      "ADJECTIVE", "P_Coherence")
    vocab.add("coherent",    "ADJECTIVE", "P_Coherence")
    vocab.add("pure",        "ADJECTIVE", "I_Symmetry")
    vocab.add("measure",     "VERB", "P_Ratio")
    vocab.add("defines",     "VERB", "P_Coherence")
    vocab.add("produces",    "VERB", "A_Energy")
    vocab.add("links",       "VERB", "I_Connectivity")
    vocab.add("stabilizes",  "VERB", "P_Coherence")
    vocab.add("identity",    "NOUN", "I_Symmetry")
    vocab.add("symmetry",    "NOUN", "I_Symmetry")
    vocab.add("topology",    "NOUN", "I_Topology")
    vocab.add("dimension",   "NOUN", "I_Dimension")
    vocab.add("correct",     "ADJECTIVE", "P_Coherence")
    vocab.add("valid",       "ADJECTIVE", "P_Coherence")
    vocab.add("unstable",    "ADJECTIVE", "P_Tax")

    # Tier 6 — Substrate Physics Nouns
    vocab.add("electron",    "NOUN", "M_Mass")
    vocab.add("proton",      "NOUN", "M_Charge")
    vocab.add("photon",      "NOUN", "A_Energy")
    vocab.add("neutron",     "NOUN", "M_Mass")
    vocab.add("mass",        "NOUN", "M_Mass")
    vocab.add("charge",      "NOUN", "M_Charge")
    vocab.add("energy",      "NOUN", "A_Energy")
    vocab.add("force",       "NOUN", "A_Force")
    vocab.add("velocity",    "NOUN", "A_Velocity")
    vocab.add("resonance",   "NOUN", "A_Resonance")
    vocab.add("particle",    "NOUN", "M_Mass")
    vocab.add("coupling",    "NOUN", "I_Connectivity")
    vocab.add("entropy",     "NOUN", "P_Tax")
    vocab.add("quantum",     "ADJECTIVE", "I_Topology")
    vocab.add("atomic",      "ADJECTIVE", "M_Charge")
    vocab.add("strong",      "ADJECTIVE", "A_Force")
    vocab.add("weak",        "ADJECTIVE", "A_Force")
    vocab.add("high",        "ADJECTIVE", "A_Energy")
    vocab.add("low",         "ADJECTIVE", "M_Thermal")
    vocab.add("interacts",   "VERB", "I_Connectivity")
    vocab.add("affects",     "VERB", "A_Force")
    vocab.add("increases",   "VERB", "A_Energy")
    vocab.add("decreases",   "VERB", "M_Thermal")
    vocab.add("exists",      "VERB", "P_Phase")
    vocab.add("encodes",     "VERB", "I_Symmetry")

    # Tier 7 — CritPt Core Objects
    vocab.add("state",       "NOUN", "P_Phase")
    vocab.add("equation",    "NOUN", "I_Symmetry")
    vocab.add("hamiltonian", "NOUN", "A_Energy")
    vocab.add("field",       "NOUN", "M_Space")
    vocab.add("function",    "NOUN", "I_Complexity")
    vocab.add("momentum",    "NOUN", "A_Velocity")
    vocab.add("spin",        "NOUN", "A_Spin")
    vocab.add("boundary",    "NOUN", "P_Limit")
    vocab.add("theory",      "NOUN", "I_Complexity")

    # Tier 8 — CritPt Domain Primitives
    vocab.add("weyl",        "NOUN", "I_Symmetry")
    vocab.add("anomaly",     "NOUN", "P_Tax")
    vocab.add("metric",      "NOUN", "I_Topology")
    vocab.add("partition",   "NOUN", "M_Count")
    vocab.add("conformal",   "ADJECTIVE", "I_Symmetry")
    vocab.add("temperature", "NOUN", "M_Thermal")
    vocab.add("cavity",      "NOUN", "M_Space")
    vocab.add("tunneling",   "NOUN", "A_Flux")
    vocab.add("braiding",    "NOUN", "I_Topology")

    # Tier 9 — CritPt Meta-Connectives
    vocab.add("consider",    "VERB", "P_Probability")
    vocab.add("assume",      "VERB", "P_Probability")
    vocab.add("describe",    "VERB", "I_Complexity")
    vocab.add("defines_v",   "VERB", "P_Coherence")
    vocab.add("calculates",  "VERB", "M_Count")

    # Tier 10 — Physical Parameters (LaTeX common targets)
    vocab.add("lambda",      "NOUN", "P_Ratio")
    vocab.add("sigma",       "NOUN", "M_Count")
    vocab.add("alpha",       "NOUN", "P_Coherence")
    vocab.add("delta",       "NOUN", "P_Limit")
    vocab.add("omega",       "NOUN", "A_Resonance")
    vocab.add("beta",        "NOUN", "P_Ratio")
    vocab.add("gamma",       "NOUN", "A_Flux")
    vocab.add("epsilon",     "NOUN", "P_Tax")
    vocab.add("theta",       "NOUN", "P_Phase")
    vocab.add("vartheta",    "NOUN", "P_Phase")

    # Tier 11 — Structural/Meta Context
    vocab.add("system",      "NOUN", "I_Complexity")
    vocab.add("interaction", "NOUN", "I_Connectivity")
    vocab.add("space",       "NOUN", "M_Space")
    vocab.add("terms",       "NOUN", "M_Count")
    vocab.add("form",        "NOUN", "I_Topology")
    vocab.add("setup",       "NOUN", "I_Complexity")
    vocab.add("given",       "ADJECTIVE", "P_Probability")
    vocab.add("follows",     "VERB", "P_Phase")
    vocab.add("determines",  "VERB", "I_Complexity")
    vocab.add("relates",     "VERB", "I_Connectivity")

    # Tier 12 — Mathematical Operations
    vocab.add("integral",    "NOUN", "M_Space")
    vocab.add("derivative",  "NOUN", "A_Velocity")
    vocab.add("matrix",      "NOUN", "I_Dimension")
    vocab.add("vector_n",    "NOUN", "I_Dimension")
    vocab.add("tensor",      "NOUN", "I_Complexity")
    vocab.add("logarithm",   "NOUN", "P_Ratio")
    vocab.add("transformation", "NOUN", "P_Phase")

    return vocab

# Export singleton instance
LANG_DB = build_priority_vocabulary()

if __name__ == "__main__":
    print(f"Grounded {len(LANG_DB.words)} priority entries.")
    for lemma in ["lambda", "system", "integral", "matrix"]:
        w = LANG_DB.get(lemma)
        if w:
            print(f"  {lemma:12s} role={w.role:10s} zone={w.home_zone} "
                  f"id={w.lemma_id} nrci={float(w.nrci):.4f}")
