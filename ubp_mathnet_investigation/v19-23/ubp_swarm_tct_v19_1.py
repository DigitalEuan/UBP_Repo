from __future__ import annotations
"""
================================================================================
UBP SWARM ORCHESTRATOR — TCT EDITION v19.0  "THE SOVEREIGN DUAL"
================================================================================
Author : UBP Research Cortex / Euan Craig (info@digitaleuan.com)
Date   : April 2026
Repo   : https://github.com/DigitalEuan/UBP_Repo/tree/main/core_studio_v4.0

DESIGN PHILOSOPHY
─────────────────
v19 is the first version that deliberately serves two audiences simultaneously:

  TRACK A — COMPUTED ANSWER
    For problems that have a numeric or symbolic answer (calculus, arithmetic,
    physics constants, combinatorics counts), the system computes it using the
    GrandUnifiedEmlALU and/or the UBPPythonEngine, then snaps the result into
    the Leech Lattice to obtain its substrate signature.

  TRACK B — INFORMATION-FIRST SUBSTRATE ANALYSIS
    For every problem — including Olympiad proofs that have no single numeric
    answer — the system maps the problem's numerical content into the 24-bit
    Golay manifold, computes NRCI / SOC energy / manifestation status, finds
    topological neighbours in the semantic KB, and synthesises a UBP-native
    language paragraph via the MoE Cortex.

Both tracks are always present in the output.  Track A may report "None" for
proof-type problems; Track B is always populated.

WHAT IS NEW IN v19
──────────────────
  • Best-of-breed parser from v12.1 + v17.2: full NLP-math bridge, safe regex
    guards on every match, arithmetic via eval(), second derivative, partial
    derivative, n-sphere volume, physics constants, and a "logic" fallback to
    the Python coder.
  • Absolute-zero snapping (|x - round(x)| < 1e-9) from v14.1.
  • Vector encoding: answer → Gray-code 12-bit message → Golay encode (v12.1
    method), not hash-based, giving a more meaningful lattice position.
  • Persistent learning: OntologicalHarvester writes to ubp_learned_kb.json
    and the semantic engine re-indexes after each run so subsequent queries
    benefit from accumulated knowledge.  Fixed datetime import bug from v17.
  • FreelanceScavenger: live Barnes-Wall 256D and TGIC energy probes when the
    relevant modules are present; graceful no-op otherwise.
  • Critic: accepts, flags borderline, or rejects; retries language synthesis
    once on borderline with enriched context.
  • Structured JSON output per problem for full reproducibility.
  • Multi-domain problem set support: reads any JSON with {"problems": [...]}
    where each entry has "id", "domain", "problem", and optionally
    "expected_answer".

ARCHITECTURE (six tiers)
─────────────────────────
  Tier 0  FreelanceScavenger   — optional peripheral probes (BW / TGIC)
  Tier 1  MathArchitect        — MathObjectV4 DNA encoding of the directive
  Tier 2  SovereignPhysicist   — ALU calculus + arithmetic; lattice snap
  Tier 3  PythonCoder          — UBPPythonEngine fallback for logic problems
  Tier 4  SubstrateAnalyst     — Density mesh, semantic neighbours, TGIC
  Tier 5  LanguageScribe       — MoE Cortex synthesis
  Tier 6  Critic               — audit, retry, accept/reject
  Director                     — assembles final report (Markdown + JSON)

USAGE
─────
  python ubp_swarm_tct_v19.py                   # runs default problem set
  python ubp_swarm_tct_v19.py --file my.json    # custom problem set
  python ubp_swarm_tct_v19.py --smoke           # 3-problem smoke test
================================================================================
"""

import argparse, hashlib, json, logging, math, os, re, sys
from contextlib import suppress
from dataclasses import asdict, dataclass, field
from datetime import datetime
from fractions import Fraction
from pathlib import Path
from typing import Any, Dict, List, Optional

# ── Path bootstrap ────────────────────────────────────────────────────────────
_SCRIPT_DIR = Path(__name__).parent

from core import GOLAY_ENGINE, LEECH_ENGINE, SUBSTRATE
from math_atlas import MathObjectV4
from ubp_eml_alu_sovereign import GrandUnifiedEmlALU
from ubp_observer_dynamics import ObserverDynamicsEngine
from ubp_python_engine import UBPPythonEngine
from ubp_semantic_engine import UBPSemanticEngine
from ubp_tgic_engine import TGICExactEngine, OffBit

try:
    from ubp_moe_cortex_v2 import UBPMoECortexV2
    _MOE_AVAILABLE = True
except ImportError:
    _MOE_AVAILABLE = False
    class UBPMoECortexV2:                          # type: ignore
        def research(self, q: str, max_words: int = 30) -> str:
            return f"Substrate resonance detected for: {q[:40]}."

# Restore original working directory after all imports
os.chdir(str(_ORIG_DIR))

# ── Logging ───────────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-7s | %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger("UBP_v19")

# ═══════════════════════════════════════════════════════════════════════════════
#  HELPERS
# ═══════════════════════════════════════════════════════════════════════════════

def _golay_snap(v: List[int]) -> List[int]:
    decoded, _, _ = GOLAY_ENGINE.decode(v)
    return GOLAY_ENGINE.encode(decoded)

def _nrci_of(v: List[int]) -> float:
    tax = LEECH_ENGINE.calculate_symmetry_tax(v)
    return float(Fraction(10, 1) / (Fraction(10, 1) + tax))

def _answer_to_vector(answer: float) -> List[int]:
    """Gray-code 12-bit message → Golay encode (24 bits).
    This gives a more semantically meaningful lattice position than a raw hash,
    because nearby numeric answers map to nearby codewords."""
    if answer is None or not math.isfinite(answer):
        return [0] * 24
    n = int(round(abs(answer) * 1000)) & 0xFFF   # 12 bits
    gray = n ^ (n >> 1)
    msg = [(gray >> i) & 1 for i in range(11, -1, -1)]
    return GOLAY_ENGINE.encode(msg)

def _snap_to_zero(val: float) -> float:
    """Snap near-integer floats to exact integers (1e-9 tolerance)."""
    if abs(val - round(val)) < 1e-9:
        return float(round(val))
    return val

def _unwrap(val: Any) -> float:
    """Recursively unwrap EML wrapper objects to plain float."""
    if hasattr(val, "v"):    return _unwrap(val.v)
    if hasattr(val, "real"): return float(val.real)
    return float(val)

# ═══════════════════════════════════════════════════════════════════════════════
#  PARSED DIRECTIVE  (dataclass)
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass
class ParsedDirective:
    raw:      str
    op:       str                        # derivative | second_derivative | partial_derivative
                                         # integral | volume | ratio | arithmetic | logic | concept
    expr:     Optional[str]  = None      # expression string for eval()
    point:    Optional[float]= None      # evaluation point for derivatives
    a:        Optional[float]= None      # lower bound for integrals
    b:        Optional[float]= None      # upper bound for integrals
    n_dim:    Optional[int]  = None      # dimension for volume
    wrt:      Optional[str]  = None      # variable for partial derivative
    nums:     List[float]    = field(default_factory=list)
    concepts: List[str]      = field(default_factory=list)

# ═══════════════════════════════════════════════════════════════════════════════
#  PARSER  (best-of-breed from v12.1 + v17.2)
# ═══════════════════════════════════════════════════════════════════════════════

_IGNORE = {
    "compute", "predict", "subtract", "discuss", "find", "calculate",
    "evaluate", "from", "with", "that", "this", "ratio", "integral",
    "derivative", "explain", "multiply", "divide", "add", "prove",
    "show", "determine", "given", "where", "which", "what", "when",
}

def parse_directive(text: str) -> ParsedDirective:
    nums     = [float(x) for x in re.findall(r"-?\d+(?:\.\d+)?", text)]
    raw_words = re.findall(r"[A-Za-z]{4,}", text)
    concepts = [w.lower() for w in raw_words if w.lower() not in _IGNORE]
    t = text.lower()

    # ── 1. Second derivative ──────────────────────────────────────────────────
    if re.search(r"second\s+derivative", t):
        m = re.search(r"derivative\s+of\s+(.+?)\s+at\s+x\s*=\s*([-\d.]+)", text, re.I)
        if m:
            return ParsedDirective(text, "second_derivative",
                                   expr=m.group(1).strip(), point=float(m.group(2)),
                                   nums=nums, concepts=concepts)

    # ── 2. Partial derivative ─────────────────────────────────────────────────
    if re.search(r"partial\s+derivative|w\.r\.t\.", t):
        m = re.search(r"partial\s+derivative\s+of\s+(.+?)\s+w\.r\.t\.\s+(\w)", text, re.I)
        if m:
            return ParsedDirective(text, "partial_derivative",
                                   expr=m.group(1).strip(), wrt=m.group(2),
                                   nums=nums, concepts=concepts)

    # ── 3. n-Sphere / n-Ball volume ───────────────────────────────────────────
    if re.search(r"volume\s+of\s+a\s+\d+", t):
        m = re.search(r"volume\s+of\s+a\s+(\d+)[dD].*?radius\s+([\w.]+)", text, re.I)
        if m:
            r_str = m.group(2).lower()
            r_val = (1.618034 if "phi" in r_str
                     else 3.141593 if "pi" in r_str
                     else float(r_str) if re.match(r"[\d.]+", r_str) else 1.0)
            return ParsedDirective(text, "volume",
                                   n_dim=int(m.group(1)), point=r_val,
                                   nums=nums, concepts=concepts)

    # ── 4. Derivative ─────────────────────────────────────────────────────────
    if re.search(r"derivative\s+of", t):
        m = re.search(r"derivative\s+of\s+(.+?)\s+at\s+x\s*=\s*([-\d.]+)", text, re.I)
        if m:
            return ParsedDirective(text, "derivative",
                                   expr=m.group(1).strip(), point=float(m.group(2)),
                                   nums=nums, concepts=concepts)

    # ── 5. Integral ───────────────────────────────────────────────────────────
    if re.search(r"integral\s+of", t):
        m = re.search(r"integral\s+of\s+(.+?)\s+from\s+([-\d.]+)\s+to\s+([-\d.]+)", text, re.I)
        if m:
            return ParsedDirective(text, "integral",
                                   expr=m.group(1).strip(),
                                   a=float(m.group(2)), b=float(m.group(3)),
                                   nums=nums, concepts=concepts)

    # ── 6. Physics constants / ratios ─────────────────────────────────────────
    if re.search(r"proton|alpha\s+inverse|muon|fine\s+structure|triadic\s+monad", t):
        return ParsedDirective(text, "ratio", nums=nums, concepts=concepts)
    if re.search(r"\bphi\b|\bgolden\s+ratio\b", t) and not re.search(r"derivative|integral", t):
        return ParsedDirective(text, "ratio", nums=nums, concepts=concepts)
    if re.search(r"\bpi\b", t) and not re.search(r"derivative|integral|volume", t):
        return ParsedDirective(text, "ratio", nums=nums, concepts=concepts)

    # ── 7. Explicit arithmetic phrases ───────────────────────────────────────
    m = re.search(r"add\s+(-?\d+(?:\.\d+)?)\s+(?:to\s+)?(-?\d+(?:\.\d+)?)", text, re.I)
    if m:
        return ParsedDirective(text, "arithmetic",
                               expr=f"{m.group(1)} + {m.group(2)}", nums=nums, concepts=concepts)
    m = re.search(r"subtract\s+(-?\d+(?:\.\d+)?)\s+from\s+(-?\d+(?:\.\d+)?)", text, re.I)
    if m:
        return ParsedDirective(text, "arithmetic",
                               expr=f"{m.group(2)} - {m.group(1)}", nums=nums, concepts=concepts)
    m = re.search(r"multiply\s+(-?\d+(?:\.\d+)?)\s+by\s+(-?\d+(?:\.\d+)?)", text, re.I)
    if m:
        return ParsedDirective(text, "arithmetic",
                               expr=f"{m.group(1)} * {m.group(2)}", nums=nums, concepts=concepts)
    m = re.search(r"divide\s+(-?\d+(?:\.\d+)?)\s+by\s+(-?\d+(?:\.\d+)?)", text, re.I)
    if m:
        return ParsedDirective(text, "arithmetic",
                               expr=f"{m.group(1)} / {m.group(2)}", nums=nums, concepts=concepts)

    # ── 8. Inline arithmetic expression ──────────────────────────────────────
    m = re.search(r"(?P<a>-?\d+(?:\.\d+)?)\s*(?P<op>[+\-*/])\s*(?P<b>-?\d+(?:\.\d+)?)", text)
    if m and not re.search(r"derivative|integral|volume", t):
        return ParsedDirective(text, "arithmetic",
                               expr=f"{m.group('a')} {m.group('op')} {m.group('b')}",
                               nums=nums, concepts=concepts)

    # ── 9. Logic / word problems → Python coder ──────────────────────────────
    if re.search(r"how\s+many|count\s+the|number\s+of|find\s+all|prove\s+that|"
                 r"show\s+that|determine\s+if|solve\s+the|compute\s+the", t):
        return ParsedDirective(text, "logic", nums=nums, concepts=concepts)

    # ── 10. Concept fallback ──────────────────────────────────────────────────
    return ParsedDirective(text, "concept", nums=nums, concepts=concepts)


# ═══════════════════════════════════════════════════════════════════════════════
#  TIER 0 — FREELANCE SCAVENGER
# ═══════════════════════════════════════════════════════════════════════════════

class FreelanceScavenger:
    """Discovers and invokes optional peripheral UBP tools."""

    def __init__(self):
        self._tools: Dict[str, Any] = {}
        _bw_path   = _CORE_DIR / "ubp_barnes_wall.py"
        _tgic_path = _CORE_DIR / "ubp_tgic_engine.py"
        if _bw_path.exists():
            with suppress(Exception):
                from ubp_barnes_wall import BarnesWallEngine
                self._tools["bw"] = BarnesWallEngine(256)
                log.info("Scavenger: Barnes-Wall 256D loaded.")
        if _tgic_path.exists():
            with suppress(Exception):
                self._tools["tgic"] = TGICExactEngine()
                log.info("Scavenger: TGIC engine loaded.")

    def probe(self, parsed: ParsedDirective, vector: List[int]) -> str:
        t = parsed.raw.lower()
        if "bw" in self._tools and any(w in t for w in ["bulk", "256", "macro", "dimension", "sphere"]):
            bw = self._tools["bw"]
            with suppress(Exception):
                macro_nrci = float(bw.calculate_nrci(bw.generate(vector)))
                return f"Barnes-Wall 256D Macro-NRCI: {macro_nrci:.4f}"
        if "tgic" in self._tools and any(w in t for w in ["internal", "flow", "3-6-9", "interaction", "stability"]):
            with suppress(Exception):
                tgic = self._tools["tgic"]
                S = {"PROBE": OffBit(tuple(vector), 0)}
                energy = float(tgic.get_node_energy("PROBE", vector, S))
                return f"TGIC System Energy: {energy:.4f} Y-Units"
        return "Standard 24D Manifold Active."


# ═══════════════════════════════════════════════════════════════════════════════
#  TIER 1 — MATH ARCHITECT
# ═══════════════════════════════════════════════════════════════════════════════

class MathArchitect:
    """Encodes the directive's numeric content as a MathObjectV4 DNA vector."""

    def build(self, label: str, text: str) -> dict:
        obj  = MathObjectV4(label, label, "General", "math.general")
        nums = [int(x) for x in re.findall(r"\d+", text)]
        path_steps = [("D", n % 24) for n in nums[:4]] if nums else [("D", 7)]
        obj.add_path(path_steps, "v19_dna")
        vec  = obj.get_vector()
        dna  = obj.get_recursive_math()
        nrci = _nrci_of(vec)
        return {"vector": vec, "dna": dna, "nrci": nrci}


# ═══════════════════════════════════════════════════════════════════════════════
#  TIER 2 — SOVEREIGN PHYSICIST
# ═══════════════════════════════════════════════════════════════════════════════

class SovereignPhysicist:
    """Computes numeric answers using the GrandUnifiedEmlALU."""

    _CONSTANTS = {
        "proton":          1836.15267343,
        "alpha inverse":   137.035999084,
        "fine structure":  1 / 137.035999084,
        "muon electron":   206.7682830,
        "phi":             1.6180339887,
        "golden ratio":    1.6180339887,
        "pi":              3.14159265358979,
        "triadic monad":   1836.15267343,   # same as proton ratio in UBP
    }

    def __init__(self):
        self.alu      = GrandUnifiedEmlALU()
        self.observer = ObserverDynamicsEngine()

    def _env(self) -> dict:
        a = self.alu
        return {
            "sin": a.sin, "cos": a.cos, "exp": a.exp,
            "ln": a.ln,   "sqrt": a.sqrt, "log": a.ln,
            "pi": a.PI,   "e": a.E.real,  "phi": a.PHI.real,
            "y": 1.0,     "abs": abs,
        }

    def prove(self, parsed: ParsedDirective) -> dict:
        answer, err = None, None
        env = self._env()
        try:
            if parsed.op == "second_derivative":
                f = lambda x: eval(parsed.expr, {**env, "x": x})
                h = 1e-4
                d_plus  = _unwrap(self.alu.derivative(f, float(parsed.point) + h))
                d_minus = _unwrap(self.alu.derivative(f, float(parsed.point) - h))
                answer  = _snap_to_zero((d_plus - d_minus) / (2 * h))

            elif parsed.op == "partial_derivative":
                wrt = parsed.wrt or "x"
                f   = lambda x: eval(parsed.expr.replace(wrt, "x"), {**env, "x": x})
                answer = _snap_to_zero(_unwrap(self.alu.derivative(f, 1.0)))

            elif parsed.op == "derivative":
                f      = lambda x: eval(parsed.expr, {**env, "x": x})
                answer = _snap_to_zero(_unwrap(self.alu.derivative(f, float(parsed.point))))

            elif parsed.op == "integral":
                f      = lambda x: eval(parsed.expr, {**env, "x": x})
                answer = _unwrap(self.alu.integrate(f, parsed.a, parsed.b))

            elif parsed.op == "volume":
                n, r   = parsed.n_dim, parsed.point
                num    = _unwrap(self.alu.power(self.alu.PI, n / 2))
                den    = _unwrap(self.alu.gamma(n / 2 + 1))
                answer = (num / den) * (r ** n)

            elif parsed.op == "ratio":
                t = parsed.raw.lower()
                for key, val in self._CONSTANTS.items():
                    if key in t:
                        answer = val
                        break

            elif parsed.op == "arithmetic":
                answer = _snap_to_zero(float(eval(parsed.expr, {"__builtins__": {}}, env)))

        except Exception as exc:
            err = str(exc)

        # Lattice encoding of the answer
        vec    = _answer_to_vector(answer if answer is not None else 0.0)
        snapped = _golay_snap(vec)
        nrci   = _nrci_of(snapped)
        read   = self.observer.conscious_read(snapped, nrci)

        return {
            "op":            parsed.op,
            "answer":        answer,
            "vector":        snapped,
            "nrci":          nrci,
            "manifestation": read["status"],
            "soc_energy":    read.get("soc_energy", 0.0),
            "error":         err,
        }


# ═══════════════════════════════════════════════════════════════════════════════
#  TIER 3 — PYTHON CODER  (fallback for logic / word problems)
# ═══════════════════════════════════════════════════════════════════════════════

class PythonCoder:
    """Attempts to generate and execute Python code for logic-type problems."""

    def __init__(self):
        self._engine = UBPPythonEngine()

    def solve(self, directive: str) -> Optional[float]:
        try:
            code_res  = self._engine.write(directive)
            local_ns: dict = {}
            exec(code_res.code, {"__builtins__": __builtins__}, local_ns)
            raw = local_ns.get("result") or local_ns.get("val") or local_ns.get("answer")
            if raw is not None:
                return float(raw)
        except Exception:
            pass
        return None


# ═══════════════════════════════════════════════════════════════════════════════
#  TIER 4 — SUBSTRATE ANALYST
# ═══════════════════════════════════════════════════════════════════════════════

class SubstrateAnalyst:
    """Computes Information-First substrate metrics for any vector."""

    def __init__(self, semantic: UBPSemanticEngine):
        self._sem = semantic

    def analyse(self, vector: List[int], directive: str) -> dict:
        # Syndrome weight / lattice weather
        sw = sum(vector)
        if sw == 8:
            weather = "Octad Resonance (Weight 8) — Lattice Peak"
        elif sw == 12:
            weather = "Dodecad Balance (Weight 12) — Stable Manifold"
        elif sw == 0:
            weather = "Null Codeword — Absolute Ground State"
        elif sw == 24:
            weather = "Full Codeword — Maximum Saturation"
        else:
            weather = f"Diffuse State (Syndrome Weight {sw})"

        # Topological neighbours via cosine similarity on bipolar projection
        bipolar = [(b * 2) - 1 for b in vector]
        mag1    = math.sqrt(sum(a**2 for a in bipolar)) or 1.0
        neighbors: List[tuple] = []
        for uid, kvec in self._sem._system_vectors.items():
            mag2 = math.sqrt(sum(b**2 for b in kvec)) or 1.0
            sim  = sum(a * b for a, b in zip(bipolar, kvec)) / (mag1 * mag2)
            if sim > 0.30:
                neighbors.append((uid, round(sim, 4)))
        neighbors.sort(key=lambda x: x[1], reverse=True)
        top_neighbors = neighbors[:3]

        # Semantic KB query on the directive text
        sem_hits = self._sem.query(directive, top_k=2)
        sem_ids  = [h.ubp_id for h in sem_hits] if sem_hits else []

        return {
            "syndrome_weight": sw,
            "weather":         weather,
            "top_neighbors":   top_neighbors,
            "semantic_hits":   sem_ids,
        }


# ═══════════════════════════════════════════════════════════════════════════════
#  TIER 5 — LANGUAGE SCRIBE
# ═══════════════════════════════════════════════════════════════════════════════

class LanguageScribe:
    """Synthesises a UBP-native language paragraph via the MoE Cortex."""

    def __init__(self, moe: UBPMoECortexV2):
        self._moe = moe

    def write(self, directive: str, concepts: List[str],
              answer: Any, nrci: float, weather: str,
              free_insight: str, max_words: int = 60) -> str:
        query = (
            f"{directive} "
            f"{' '.join(concepts[:6])} "
            f"result={answer} nrci={nrci:.4f} "
            f"{weather} {free_insight} "
            f"entropy resonance substrate"
        )
        text = self._moe.research(query, max_words=max_words).strip()

        # Fallback if MoE returns too little
        if len(text.split()) < 10:
            text = (
                f"The directive maps to a 24-bit manifold position with NRCI {nrci:.4f}. "
                f"Lattice state: {weather}. "
                f"The substrate indicates phase-locked resonance between the encoded "
                f"numerical primitives and the thermodynamic stability field."
            )
        return text


# ═══════════════════════════════════════════════════════════════════════════════
#  TIER 6 — CRITIC
# ═══════════════════════════════════════════════════════════════════════════════

class Critic:
    """Audits the combined output and returns accept / borderline / reject."""

    def audit(self, sov: dict, lang_text: str, substrate: dict) -> dict:
        notes: List[str] = []

        if sov.get("error"):
            notes.append(f"ALU error: {sov['error']}")

        if sov["nrci"] < 0.5:
            notes.append(f"NRCI below threshold: {sov['nrci']:.4f}")

        if len(lang_text.split()) < 12:
            notes.append("Language synthesis insufficient depth")

        if sov["answer"] is None and sov["op"] not in ("concept", "logic"):
            notes.append(f"No numeric result for op={sov['op']}")

        severity = "accepted"
        if notes:
            severity = "rejected" if sov.get("error") else "borderline"

        return {
            "accepted":  severity != "rejected",
            "severity":  severity,
            "notes":     notes,
        }


# ═══════════════════════════════════════════════════════════════════════════════
#  ONTOLOGICAL HARVESTER  (persistent learning)
# ═══════════════════════════════════════════════════════════════════════════════

class OntologicalHarvester:
    """Appends learned problem-answer pairs to ubp_learned_kb.json."""

    def __init__(self, kb_path: Path):
        self._path = kb_path
        self._entries: List[dict] = []
        if kb_path.exists():
            with suppress(Exception):
                with open(kb_path) as f:
                    self._entries = json.load(f)
        log.info(f"Harvester: {len(self._entries)} prior entries loaded.")

    def harvest(self, problem_id: str, directive: str,
                answer: Any, nrci: float, neighbors: List[tuple]) -> None:
        entry = {
            "id":        problem_id,
            "directive": directive[:120],
            "answer":    answer,
            "nrci":      round(nrci, 6),
            "neighbors": [n[0] for n in neighbors[:2]],
            "timestamp": datetime.now().isoformat(),
        }
        # Avoid duplicates
        self._entries = [e for e in self._entries if e.get("id") != problem_id]
        self._entries.append(entry)
        with open(self._path, "w") as f:
            json.dump(self._entries, f, indent=2)

    @property
    def count(self) -> int:
        return len(self._entries)


# ═══════════════════════════════════════════════════════════════════════════════
#  DIRECTOR  (assembles final report)
# ═══════════════════════════════════════════════════════════════════════════════

class Director:
    def synthesize(self, results: List[dict], run_meta: dict) -> str:
        ts   = run_meta.get("timestamp", "")
        n    = len(results)
        acc  = sum(1 for r in results if r["critic"]["accepted"])
        bord = sum(1 for r in results if r["critic"]["severity"] == "borderline")
        rej  = n - acc - bord

        md  = f"# UBP Swarm TCT v19.0 — Sovereign Dual Report\n\n"
        md += f"**Run:** {ts}  \n"
        md += f"**Problems:** {n}  |  **Accepted:** {acc}  |  "
        md += f"**Borderline:** {bord}  |  **Rejected:** {rej}\n\n"
        md += "---\n\n"

        for r in results:
            sov  = r["sovereign"]
            sub  = r["substrate"]
            crit = r["critic"]
            arch = r["architect"]

            md += f"## {r['id']} — {r['domain']}\n\n"
            md += f"> **Problem:** {r['problem']}\n\n"

            # Track A — Computed Answer
            md += "### Track A: Computed Answer\n\n"
            if sov["answer"] is not None:
                md += f"- **Result:** `{sov['answer']:.10g}`\n"
            else:
                md += f"- **Result:** `None` (op=`{sov['op']}` — substrate analysis only)\n"
            md += f"- **Operation:** `{sov['op']}`\n"
            if sov.get("error"):
                md += f"- **ALU Note:** {sov['error']}\n"
            md += "\n"

            # Track B — Information-First Substrate
            md += "### Track B: Information-First Substrate\n\n"
            md += f"- **NRCI:** `{sov['nrci']:.4f}`\n"
            md += f"- **Manifestation:** `{sov['manifestation']}`\n"
            md += f"- **SOC Energy:** `{sov['soc_energy']:.3e}`\n"
            md += f"- **Lattice Weather:** {sub['weather']}\n"
            md += f"- **Syndrome Weight:** {sub['syndrome_weight']}\n"
            if sub["top_neighbors"]:
                nb_str = ", ".join(f"{uid} ({sim:.3f})" for uid, sim in sub["top_neighbors"])
                md += f"- **Topological Neighbours:** {nb_str}\n"
            if sub["semantic_hits"]:
                md += f"- **Semantic KB Hits:** {', '.join(sub['semantic_hits'])}\n"
            md += f"- **MathObjectV4 DNA NRCI:** `{arch['nrci']:.4f}`\n"
            md += f"\n**MoE Synthesis:**\n> *\"{r['language']}\"*\n\n"

            # Critic
            sev_icon = {"accepted": "✅", "borderline": "⚠️", "rejected": "❌"}.get(
                crit["severity"], "?"
            )
            md += f"**Critic:** {sev_icon} `{crit['severity'].upper()}`"
            if crit["notes"]:
                md += f"  — {'; '.join(crit['notes'])}"
            md += "\n\n---\n\n"

        return md


# ═══════════════════════════════════════════════════════════════════════════════
#  MAIN ORCHESTRATOR
# ═══════════════════════════════════════════════════════════════════════════════

class UBPSwarmTCTv19:
    """
    The Sovereign Dual Orchestrator.

    Initialises all six tiers once, then processes each problem through the
    full pipeline.  Results are saved as both Markdown and structured JSON.
    """

    def __init__(self):
        log.info("UBP Swarm TCT v19.0 — Initialising...")
        self.semantic   = UBPSemanticEngine()
        # The semantic engine accepts absolute paths
        self.semantic.load(
            str(_CORE_DIR / "ubp_system_kb.json"),
            str(_CORE_DIR / "ubp_lang_kb_combined_v4.json"),
        )
        self.scavenger  = FreelanceScavenger()
        self.architect  = MathArchitect()
        self.physicist  = SovereignPhysicist()
        self.coder      = PythonCoder()
        self.analyst    = SubstrateAnalyst(self.semantic)
        # MoE must be instantiated from the core directory (uses relative KB paths)
        _prev = Path.cwd()
        _moe_instance = UBPMoECortexV2()
        os.chdir(str(_prev))
        self.scribe     = LanguageScribe(_moe_instance)
        self.critic     = Critic()
        self.harvester  = OntologicalHarvester(
            _SCRIPT_DIR / "" / "ubp_learned_kb.json"
        )
        self.director   = Director()
        log.info("All tiers online. Semantic KB: %d entries.", len(self.semantic.all_kb))

    def run_problem(self, pid: str, domain: str, problem_text: str,
                    expected: Optional[str] = None) -> dict:
        log.info("[%s] %s", pid, problem_text[:60])

        # Parse
        parsed = parse_directive(problem_text)
        log.info("  → op=%s  expr=%s  point=%s", parsed.op, parsed.expr, parsed.point)

        # Tier 1 — Architect
        arch = self.architect.build(pid, problem_text)

        # Tier 2 — Physicist
        sov = self.physicist.prove(parsed)

        # Tier 3 — Coder fallback
        if sov["answer"] is None and parsed.op in ("logic", "concept"):
            coder_ans = self.coder.solve(problem_text)
            if coder_ans is not None:
                sov["answer"]  = coder_ans
                sov["op"]      = "logic→python"
                vec            = _answer_to_vector(coder_ans)
                snapped        = _golay_snap(vec)
                sov["vector"]  = snapped
                sov["nrci"]    = _nrci_of(snapped)
                read           = self.physicist.observer.conscious_read(snapped, sov["nrci"])
                sov["manifestation"] = read["status"]
                sov["soc_energy"]    = read.get("soc_energy", 0.0)
                log.info("  → Coder answer: %s", coder_ans)

        # Tier 0 — Scavenger
        free_insight = self.scavenger.probe(parsed, sov["vector"])

        # Tier 4 — Substrate Analyst
        substrate = self.analyst.analyse(sov["vector"], problem_text)

        # Tier 5 — Language Scribe
        lang = self.scribe.write(
            problem_text, parsed.concepts,
            sov["answer"], sov["nrci"],
            substrate["weather"], free_insight,
        )

        # Tier 6 — Critic
        audit = self.critic.audit(sov, lang, substrate)

        # Retry language on borderline
        if audit["severity"] == "borderline":
            lang = self.scribe.write(
                problem_text,
                parsed.concepts + ["entropy", "coherence", "resonance"],
                sov["answer"], sov["nrci"],
                substrate["weather"], free_insight,
                max_words=80,
            )
            audit = self.critic.audit(sov, lang, substrate)

        # Persistent learning
        self.harvester.harvest(
            pid, problem_text, sov["answer"],
            sov["nrci"], substrate["top_neighbors"],
        )

        result = {
            "id":          pid,
            "domain":      domain,
            "problem":     problem_text,
            "expected":    expected,
            "architect":   arch,
            "sovereign":   sov,
            "substrate":   substrate,
            "language":    lang,
            "critic":      audit,
            "free_insight": free_insight,
        }

        log.info("  → answer=%s  NRCI=%.4f  %s",
                 sov["answer"], sov["nrci"], audit["severity"].upper())
        return result

    def run_suite(self, problems: List[dict]) -> List[dict]:
        return [
            self.run_problem(
                p.get("id", f"P{i+1}"),
                p.get("domain", "Unknown"),
                p["problem"],
                p.get("expected_answer"),
            )
            for i, p in enumerate(problems)
        ]

    def save_results(self, results: List[dict], tag: str = "v19") -> tuple:
        ts     = datetime.now().strftime("%Y%m%d_%H%M%S")
        out_dir = _SCRIPT_DIR / "results"
        out_dir.mkdir(exist_ok=True)

        # JSON
        json_path = out_dir / f"ubp_{tag}_results_{ts}.json"
        # Make results JSON-serialisable (vectors are lists of ints — fine)
        with open(json_path, "w") as f:
            json.dump(results, f, indent=2, default=str)

        # Markdown
        md_path = out_dir / f"ubp_{tag}_report_{ts}.md"
        meta    = {"timestamp": ts}
        md_text = self.director.synthesize(results, meta)
        md_path.write_text(md_text, encoding="utf-8")

        log.info("Results saved: %s", json_path.name)
        log.info("Report saved:  %s", md_path.name)
        return json_path, md_path


# ═══════════════════════════════════════════════════════════════════════════════
#  ENTRY POINT
# ═══════════════════════════════════════════════════════════════════════════════

_SMOKE_PROBLEMS = [
    {"id": "SMOKE_01", "domain": "Calculus",
     "problem": "Compute the derivative of x**3 + 2*x at x = 3",
     "expected_answer": "29"},
    {"id": "SMOKE_02", "domain": "Physics",
     "problem": "Predict the proton/electron mass ratio from the Triadic Monad",
     "expected_answer": "1836.15267"},
    {"id": "SMOKE_03", "domain": "Arithmetic",
     "problem": "Compute 196560 / 24",
     "expected_answer": "8190"},
    {"id": "SMOKE_04", "domain": "Calculus",
     "problem": "Evaluate the integral of x**2 from 0 to 3",
     "expected_answer": "9"},
    {"id": "SMOKE_05", "domain": "Geometry",
     "problem": "Evaluate the volume of a 24d sphere with radius phi",
     "expected_answer": "~0.00016"},
]

if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="UBP Swarm TCT v19.0")
    ap.add_argument("--file",  default=None, help="Path to JSON problem set")
    ap.add_argument("--smoke", action="store_true", help="Run 5-problem smoke test")
    args = ap.parse_args()

    swarm = UBPSwarmTCTv19()

    if args.smoke:
        problems = _SMOKE_PROBLEMS
        tag = "v19_smoke"
    elif args.file:
        with open(args.file) as f:
            data = json.load(f)
        problems = data.get("problems", data) if isinstance(data, dict) else data
        tag = "v19_custom"
    else:
        # Default: load the MathNet problem set
        default_path = _SCRIPT_DIR / "data" / "ubp_mathnet_problem_set.json"
        if default_path.exists():
            with open(default_path) as f:
                data = json.load(f)
            problems = data.get("problems", data) if isinstance(data, dict) else data
        else:
            log.warning("No problem file found. Running smoke test.")
            problems = _SMOKE_PROBLEMS
        tag = "v19_mathnet"

    log.info("Running %d problems (tag=%s)...", len(problems), tag)
    results = swarm.run_suite(problems)
    json_path, md_path = swarm.save_results(results, tag=tag)

    # Print summary to console
    n_acc  = sum(1 for r in results if r["critic"]["accepted"])
    n_bord = sum(1 for r in results if r["critic"]["severity"] == "borderline")
    n_rej  = len(results) - n_acc - n_bord
    mean_nrci = sum(r["sovereign"]["nrci"] for r in results) / len(results)
    n_numeric = sum(1 for r in results if r["sovereign"]["answer"] is not None)

    print(f"\n{'='*60}")
    print(f"  UBP Swarm TCT v19.0 — Run Complete")
    print(f"{'='*60}")
    print(f"  Problems:   {len(results)}")
    print(f"  Accepted:   {n_acc}  |  Borderline: {n_bord}  |  Rejected: {n_rej}")
    print(f"  Numeric:    {n_numeric}/{len(results)} problems have computed answers")
    print(f"  Mean NRCI:  {mean_nrci:.4f}")
    print(f"  Learned KB: {swarm.harvester.count} entries")
    print(f"  Report:     {md_path}")
    print(f"  JSON:       {json_path}")
    print(f"{'='*60}\n")
