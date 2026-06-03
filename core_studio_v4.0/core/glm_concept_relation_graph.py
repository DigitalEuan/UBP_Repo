"""
================================================================================
GLM CONCEPT RELATION GRAPH (CRG) v1.0
================================================================================
A typed-edge graph layered on top of the Leech-lattice adjacency.  Whereas
the original adjacency captures *geometric* closeness (Hamming distance),
the CRG captures *semantic* relations such as `is_a`, `commutes_with`,
`scales_as`, `is_dual_to`, `has_property`, `depends_on`.

These relations are how the engine answers questions of the form
"how does X relate to Y" — they cannot be inferred from the lattice alone,
because two concepts (e.g. 'parton' and 'pion') may be lattice-close yet
related by a specific physical relation that the bare distance ignores.

Design:
  * Edges are hand-curated for the CritPt domains.
  * The graph is small (~ 200 edges) by design — quality over quantity.
  * Every concept appearing in an edge MUST be present in the live
    vocabulary (verified at load time, mismatches reported).
  * Pure stdlib, no float, no external storage.

Edge labels and intended semantics:
  is_a            X is an instance/specialization of Y
  has_property    X possesses property Y
  depends_on      X is a function of (or sensitive to) Y
  commutes_with   [X, Y] = 0 (used by the constraint frame)
  scales_as       X ~ Y^n for some n
  is_dual_to      X and Y are related by a duality (e.g. AdS/CFT)
  generates       X is the generator of Y (Lie-algebra sense)
  measures        X is the observable that quantifies Y
================================================================================
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Dict, Tuple, Set, Iterable
from collections import defaultdict


EDGE_LABELS: Set[str] = {
    "is_a", "has_property", "depends_on", "commutes_with",
    "scales_as", "is_dual_to", "generates", "measures",
    "lattice_adjacent",
}


@dataclass
class CRGEdge:
    src: str
    label: str
    dst: str

    def reverse(self) -> "CRGEdge":
        # symmetric labels
        if self.label in ("commutes_with", "is_dual_to", "lattice_adjacent"):
            return CRGEdge(self.dst, self.label, self.src)
        return self


# ───────────────────────────────────────────────────────────────────────────────
# CURATED EDGES
# ───────────────────────────────────────────────────────────────────────────────
# Each edge uses lower-case vocabulary keys.  Multi-word keys are space-joined.
# Edges are deduplicated automatically by the loader.

_RAW_EDGES: List[Tuple[str, str, str]] = [
    # --- identities / classifications ---
    ("hamiltonian",            "is_a",           "operator"),
    ("lagrangian",             "is_a",           "functional"),
    ("propagator",             "is_a",           "function"),
    ("partition function",     "is_a",           "functional"),
    ("weyl anomaly",           "is_a",           "anomaly"),
    ("rayleigh number",        "is_a",           "number"),
    ("chern number",           "is_a",           "number"),
    ("parafermion",            "is_a",           "fermion"),
    ("majorana",               "is_a",           "fermion"),
    ("quark",                  "is_a",           "fermion"),
    ("gluon",                  "is_a",           "boson"),
    ("pion",                   "is_a",           "meson"),
    ("hadron",                 "is_a",           "particle"),
    ("matrix product",         "is_a",           "state"),
    ("ground state",           "is_a",           "state"),
    ("coherent state",         "is_a",           "state"),
    ("squeezed state",         "is_a",           "state"),
    ("density matrix",         "is_a",           "operator"),
    ("kraus operator",         "is_a",           "operator"),
    ("projector",              "is_a",           "operator"),
    ("commutator",             "is_a",           "operator"),
    ("anticommutator",         "is_a",           "operator"),
    ("tetrad",                 "is_a",           "connection"),
    ("ads",                    "is_a",           "manifold"),
    ("brane",                  "is_a",           "manifold"),
    ("quantum metric",         "is_a",           "metric"),
    ("hilbert space",          "is_a",           "manifold"),

    # --- has_property ---
    ("majorana",               "has_property",   "topological"),
    ("parafermion",            "has_property",   "topological"),
    ("chern number",           "has_property",   "topological"),
    ("weyl anomaly",           "has_property",   "conformal"),
    ("quark",                  "has_property",   "massive"),
    ("gluon",                  "has_property",   "massless"),
    ("photon",                 "has_property",   "massless"),
    ("hubbard",                "has_property",   "strong"),
    ("hatsugai-kohmoto",       "has_property",   "strong"),
    ("ads",                    "has_property",   "holographic"),
    ("squeezed state",         "has_property",   "quantum"),
    ("coherent state",         "has_property",   "quantum"),
    ("rayleigh number",        "has_property",   "critical"),
    ("convection",             "has_property",   "critical"),

    # --- depends_on ---
    ("beta",                   "depends_on",     "coupling"),
    ("beta",                   "depends_on",     "scaling"),
    ("anomaly",                "depends_on",     "dimension"),
    ("weyl anomaly",           "depends_on",     "metric"),
    ("weyl anomaly",           "depends_on",     "curvature"),
    ("renormalization",        "depends_on",     "regulator"),
    ("regularization",         "depends_on",     "dimension"),
    ("rayleigh number",        "depends_on",     "prandtl"),
    ("rayleigh number",        "depends_on",     "temperature"),
    ("convection",             "depends_on",     "rayleigh number"),
    ("efolds",                 "depends_on",     "scale factor"),
    ("growth rate",            "depends_on",     "gamma distribution"),
    ("growth rate",            "depends_on",     "waiting time"),
    ("holevo information",     "depends_on",     "density matrix"),
    ("spin squeezing",         "depends_on",     "variance"),
    ("wineland parameter",     "depends_on",     "spin squeezing"),
    ("dephasing",              "depends_on",     "dissipator"),
    ("dglap",                  "depends_on",     "coupling"),
    ("parton",                 "depends_on",     "scale"),
    ("hubbard",                "depends_on",     "tunneling"),
    ("hubbard",                "depends_on",     "interaction"),
    ("loop",                   "depends_on",     "regularization"),
    ("matching kernel",        "depends_on",     "coupling"),

    # --- commutes_with (symmetric) ---
    ("hamiltonian",            "commutes_with",  "symmetry"),
    ("projector",              "commutes_with",  "hamiltonian"),
    ("density matrix",         "commutes_with",  "hamiltonian"),
    ("number",                 "commutes_with",  "hamiltonian"),
    ("spin",                   "commutes_with",  "hamiltonian"),

    # --- scales_as ---
    ("rayleigh number",        "scales_as",      "temperature"),
    ("growth rate",            "scales_as",      "coupling"),
    ("propagator",             "scales_as",      "momentum"),
    ("hubbard",                "scales_as",      "tunneling"),
    ("dispersion",             "scales_as",      "wavenumber"),
    ("photocurrent",           "scales_as",      "power"),
    ("synchrotron",            "scales_as",      "energy"),

    # --- is_dual_to (symmetric) ---
    ("ads",                    "is_dual_to",     "bcft"),
    ("holographic",            "is_dual_to",     "conformal"),
    ("brane",                  "is_dual_to",     "boundary"),
    ("lamet",                  "is_dual_to",     "parton"),
    ("matrix product",         "is_dual_to",     "tensor"),

    # --- generates ---
    ("hamiltonian",            "generates",      "time"),
    ("momentum",               "generates",      "space"),
    ("symmetry",               "generates",      "anomaly"),
    ("renormalization",        "generates",      "beta"),
    ("dissipator",             "generates",      "dephasing"),

    # --- measures ---
    ("entropy",                "measures",       "dimension"),
    ("chern number",           "measures",       "topological"),
    ("holevo information",     "measures",       "information"),
    ("wineland parameter",     "measures",       "squeezing"),
    ("quantum metric",         "measures",       "curvature"),
    ("trace",                  "measures",       "density matrix"),
    ("expectation value",      "measures",       "operator"),
    ("variance",               "measures",       "dispersion"),
    ("rayleigh number",        "measures",       "instability"),
]


# ───────────────────────────────────────────────────────────────────────────────
# GRAPH IMPLEMENTATION
# ───────────────────────────────────────────────────────────────────────────────

class ConceptRelationGraph:
    """A small typed graph for physics concept relations."""

    def __init__(self):
        self.out: Dict[str, List[CRGEdge]] = defaultdict(list)
        self.into: Dict[str, List[CRGEdge]] = defaultdict(list)
        self.edges: List[CRGEdge] = []

    def add_edge(self, src: str, label: str, dst: str) -> bool:
        if label not in EDGE_LABELS:
            return False
        src, dst = src.lower().strip(), dst.lower().strip()
        if not src or not dst:
            return False
        edge = CRGEdge(src=src, label=label, dst=dst)
        self.edges.append(edge)
        self.out[src].append(edge)
        self.into[dst].append(edge)
        # symmetric labels: add reverse
        if label in ("commutes_with", "is_dual_to") and src != dst:
            rev = CRGEdge(src=dst, label=label, dst=src)
            self.edges.append(rev)
            self.out[dst].append(rev)
            self.into[src].append(rev)
        return True

    def neighbours(self, node: str, label: str = None) -> List[CRGEdge]:
        es = self.out.get(node.lower(), [])
        if label is None:
            return list(es)
        return [e for e in es if e.label == label]

    def relate(self, a: str, b: str) -> List[str]:
        """All edge labels directly connecting a -> b (or symmetric)."""
        a, b = a.lower(), b.lower()
        labels = []
        for e in self.out.get(a, []):
            if e.dst == b:
                labels.append(e.label)
        for e in self.out.get(b, []):
            if e.dst == a and e.label in ("commutes_with", "is_dual_to"):
                labels.append(e.label)
        return labels

    def shortest_path(self, src: str, dst: str, max_hops: int = 3
                      ) -> List[CRGEdge]:
        """BFS from src to dst over typed edges (ignores edge direction
        for symmetric labels)."""
        src, dst = src.lower(), dst.lower()
        if src == dst:
            return []
        from collections import deque
        visited = {src}
        queue = deque([(src, [])])
        while queue:
            node, path = queue.popleft()
            if len(path) >= max_hops:
                continue
            for e in self.out.get(node, []):
                if e.dst == dst:
                    return path + [e]
                if e.dst not in visited:
                    visited.add(e.dst)
                    queue.append((e.dst, path + [e]))
        return []

    def vocab_check(self, vocab_words: Set[str]) -> Tuple[int, List[str]]:
        """Verify every node referenced by an edge exists in the vocab.
        Returns (#edges_kept, [missing_concepts])."""
        nodes = set()
        for e in self.edges:
            nodes.add(e.src)
            nodes.add(e.dst)
        missing = sorted(n for n in nodes if n not in vocab_words)
        kept = sum(1 for e in self.edges
                   if e.src in vocab_words and e.dst in vocab_words)
        return kept, missing

    def stats(self) -> Dict[str, int]:
        from collections import Counter
        c = Counter(e.label for e in self.edges)
        return {"total_edges": len(self.edges),
                "by_label": dict(c),
                "nodes": len({n for e in self.edges for n in (e.src, e.dst)})}


def build_default_crg() -> ConceptRelationGraph:
    g = ConceptRelationGraph()
    for src, lbl, dst in _RAW_EDGES:
        g.add_edge(src, lbl, dst)
    return g


class LatticeConceptLinker:
    """
    Automatically links concepts in the CRG based on their geometric
    relationships in the 24-bit zoned lattice.
    """
    def __init__(self, vocab, crg: ConceptRelationGraph):
        self.vocab = vocab
        self.crg   = crg

    def auto_link(self, hamming_threshold: int = 4):
        """
        Scan all word pairs and add 'lattice_adjacent' edges if their
        Hamming distance is below threshold and they share MOG quadrants.
        """
        from ubp_unified_v5 import BinaryLinearAlgebra as BLA
        from glm_zoned_lattice_embedding import zone_signature

        words = list(self.vocab.words.items())
        links_added = 0

        for i, (name1, w1) in enumerate(words):
            for j in range(i + 1, len(words)):
                name2, w2 = words[j]

                # Check for geometric proximity
                d = BLA.hamming_distance(w1.vector, w2.vector)
                if d <= hamming_threshold:
                    # If they share the same dominant zone
                    if w1.home_zone == w2.home_zone:
                        self.crg.add_edge(name1, "lattice_adjacent", name2)
                        self.crg.add_edge(name2, "lattice_adjacent", name1)
                        links_added += 1

        return links_added


if __name__ == "__main__":
    g = build_default_crg()
    import json as _json
    print(_json.dumps(g.stats(), indent=2))
    # demo a shortest-path query
    p = g.shortest_path("hubbard", "interaction")
    print("hubbard -> interaction:", [(e.src, e.label, e.dst) for e in p])
    p = g.shortest_path("weyl anomaly", "metric")
    print("weyl anomaly -> metric:", [(e.src, e.label, e.dst) for e in p])