from __future__ import annotations
"""
================================================================================
UBP × CritPt — Sovereignty Runner v3.1 (GLM Semantic Edition, repaired)
================================================================================
Integrates the GLM Dialogue Engine to provide deterministic, phase-locked
geometric reasoning traces for every frontier physics problem.

v3.1 changes versus the original v3.0 file
------------------------------------------
* FIX  : `sys.path` bootstrap used `__name__` instead of `__file__`
        (would silently inject "." into sys.path on every run).
* FIX  : `load_critpt()` ignored its `path` argument and hard-coded
        "critpt.json"; argparse default was the wrong extension (.parquet).
* FIX  : `UBPSovereignSolver.solve()` is now `solve(problem, spec, glm_turn=None)`
        so the GLM trace can actually feed the seeded SymPy fallback that
        `critpt_glm_patch` injects.  Previously the runner passed three args
        to a two-arg method -> TypeError on every problem.
* FIX  : `emit_answer_file()` could leave `new_tmpl` unbound when neither
        the "FILL IN" marker nor a trailing `return` was found.
* FIX  : `critpt_glm_patch.apply_critpt_patch()` is now applied exactly once,
        at module load time, instead of every `SovereigntyRunner()`
        instantiation (which led to nested monkey-patch layers).
* FIX  : Removed the three duplicated module-level docstrings.
* WIRE : The runner now uses **glm_engine_v31.create_semantic_engine** so the
        four v2.0/v3.1 extensions (multi-token lexer, semantic frames, CRG,
        physics vocab pack) are actually attached.  The grammar-patch's
        v2.0 disambiguation rules still apply because v3.1 inherits from
        the v3.0 engine that the patch monkey-patches.
* WIRE : New helper `respond_best(query)` calls `respond_semantic()` when
        available and falls back to `respond()` so existing call sites that
        only know about `.respond()` keep working.
"""

import argparse
import ast
import hashlib
import json
import os
import re
import sys
import time
from dataclasses import dataclass, field
from fractions import Fraction
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

# ── PATH BOOTSTRAP ────────────────────────────────────────────────────────────
# (was: sys.path.insert(0, str(Path(__name__).resolve().parent))  # BUG)
_HERE = Path(__file__).resolve().parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))

# ── REAL UBP STACK ────────────────────────────────────────────────────────────
from ubp_unified_v5 import (
    GOLAY_ENGINE, LEECH_ENGINE,
    NoiseALU, PhysicsALU, LinearAlgebraALU, NoiseRegisterV3,
)
from ubp_v28_oracle import (
    NativeDynamicSolver, SymPyOracle, _golay_snap,
    SYMPY_AVAILABLE, UBP_CORE_AVAILABLE,
)

# ── GLM STACK (v3.1 semantic edition) ─────────────────────────────────────────
# importing glm_grammar_patch triggers the v2.0 disambiguation patch on
# GLMDialogueEngine; v3.1 inherits from that class so the patch composes.
import glm_grammar_patch  # noqa: F401  (side-effect: monkey-patches GLMDialogueEngine)
try:
    from glm_engine_v31 import create_semantic_engine, GLMDialogueEngine
    _HAS_V31 = True
except Exception as _e:  # pragma: no cover  (v3.1 not yet installed)
    create_semantic_engine = None
    GLMDialogueEngine = None
    _HAS_V31 = False
    print(f"[Sovereign] v3.1 engine unavailable ({_e}); falling back to v3.0")

def _create_v30_engine(system_kb, lang_kb):
    from glm_strict_lang_builder import build_vocabulary
    from glm_engine_v31 import GLMDialogueEngine
    return GLMDialogueEngine(build_vocabulary(system_kb, lang_kb))

# ═══════════════════════════════════════════════════════════════════════════════
# 1.  GLM RULES ENGINE  (text normalisation)
# ═══════════════════════════════════════════════════════════════════════════════

class GLMRulesEngine:
    """Loads NORMALIZATION-tagged rows from the combined lang KB and runs them
    as ordered regex substitutions on incoming problem descriptions."""

    def __init__(self, lang_kb_path: str = 'ubp_lang_kb_combined_v4.json'):
        self.normalization_rules: List[Dict[str, Any]] = []
        try:
            with open(lang_kb_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except FileNotFoundError:
            # Allow the runner to boot even if the (very large) combined KB
            # isn't present; downstream code will just see un-normalised text.
            print(f"[GLMRules] {lang_kb_path} not found - rules disabled")
            return

        fields = data["_fields"]
        f_idx = {name: i for i, name in enumerate(fields)}
        for row in data["entries"].values():
            tags = row[f_idx["tags"]]
            if "NORMALIZATION" not in tags:
                continue
            lexicon = row[f_idx["lexicon"]]
            if "], " not in lexicon:
                continue
            target_desc = lexicon.split("], ")[0].split(": ")[-1].strip()
            replacement = lexicon.split("], ")[-1].strip()
            pattern: Optional[str] = None
            if "Smart quotes" in target_desc:
                pattern = r'[\u201c\u201d\u2018\u2019]'
                replacement = '"' if '"' in replacement else "'"
            elif "En/em dash" in target_desc:
                pattern = r'[\u2013\u2014]'
                replacement = '-'
            elif "Scientific 10^6" in target_desc:
                pattern = r'10\^(\d+)'
                replacement = r'10**\1'
            elif "Unicode superscripts" in target_desc:
                pattern = r'\u00b2'
                replacement = '**2'
            elif "UPPERCASE" in target_desc:
                pattern = r'([A-Z]+)'
                replacement = lambda m: m.group(1).lower()
            if pattern:
                self.normalization_rules.append({"pattern": pattern,
                                                 "replacement": replacement})

    def preprocess(self, text: str) -> str:
        for rule in self.normalization_rules:
            text = re.sub(rule["pattern"], rule["replacement"], text)
        return text


# ═══════════════════════════════════════════════════════════════════════════════
# 2.  LATTICE-SNAP UTILITIES
# ═══════════════════════════════════════════════════════════════════════════════

F = Fraction
NRCI_PHASE_LOCK = F(7, 10)
_CODEWORD_WEIGHTS = {0, 8, 12, 16, 24}
_LATTICE_NAME = {0: "Identity", 8: "Octad", 12: "Dodecad",
                 16: "Hexadecad", 24: "Universe"}


def nrci_fraction(v24: List[int]) -> Fraction:
    tax = LEECH_ENGINE.calculate_symmetry_tax(v24)
    tax_f = tax if isinstance(tax, Fraction) else Fraction(tax)
    return F(10, 1) / (F(10, 1) + tax_f)


def lattice_snap_value(value: Any) -> Dict[str, Any]:
    try:
        n = abs(int(value)) & 0xFFFFFF
        gray = n ^ (n >> 1)
        raw = [(gray >> i) & 1 for i in range(23, -1, -1)]
    except Exception:
        h = int(hashlib.sha256(str(value).encode()).hexdigest(), 16) & 0xFFFFFF
        gray = h ^ (h >> 1)
        raw = [(gray >> i) & 1 for i in range(23, -1, -1)]
    snapped = _golay_snap(raw)
    sw = sum(snapped)
    nrci = nrci_fraction(snapped)
    return {
        "vector": snapped, "sw": sw, "nrci_frac": nrci,
        "nrci_repr": f"{nrci.numerator}/{nrci.denominator}",
        "on_lattice": sw in _CODEWORD_WEIGHTS,
        "lattice": _LATTICE_NAME.get(sw, "Off-lattice"),
        "phase_locked": nrci >= NRCI_PHASE_LOCK,
    }


# ═══════════════════════════════════════════════════════════════════════════════
# 3.  TEMPLATE PARSING
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass
class ReturnSpec:
    names: List[str]
    types: List[str]
    arity: int


@dataclass
class TemplateSpec:
    func_name: str
    in_params: List[str]
    docstring: str
    return_spec: ReturnSpec
    pre_imports: str
    raw_template: str


def parse_template(code_template: str) -> TemplateSpec:
    try:
        tree = ast.parse(re.sub(r'\$[^$]*\$', '', code_template))
    except SyntaxError:
        tree = ast.parse(code_template)

    func: Optional[ast.FunctionDef] = None
    pre: List[str] = []
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and func is None:
            func = node
        else:
            pre.append(ast.unparse(node))

    if func is None:
        return TemplateSpec("answer", [], "", ReturnSpec([], [], 1), "",
                            code_template)

    in_params = [a.arg for a in func.args.args]
    docstring = ast.get_docstring(func) or ""

    m = re.search(r"\b(Outputs?|Returns?)\b\s*\n\s*-+\s*\n(.+?)\Z",
                  docstring, flags=re.S)
    items: List[Tuple[str, str]] = []
    if m:
        for line in m.group(2).splitlines():
            m2 = re.match(r"\s*([A-Za-z_]\w*)\s*:\s*([^,\n]+)", line)
            if m2:
                items.append((m2.group(1).strip(), m2.group(2).strip()))

    if not items:
        rs = ReturnSpec(["result"], ["float"], 1)
    else:
        rs = ReturnSpec([n for n, _ in items], [t for _, t in items], len(items))

    return TemplateSpec(func.name, in_params, docstring, rs,
                        "\n".join(pre), code_template)


# ═══════════════════════════════════════════════════════════════════════════════
# 4.  ANSWER CANDIDATE  &  SOVEREIGN SOLVER
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass
class AnswerCandidate:
    values: List[str]
    method: str
    confidence: Fraction
    notes: List[str] = field(default_factory=list)


class UBPSovereignSolver:
    """Routes a problem through (1) Physics ALU, (2) Arith ALU,
    (3) Lattice-Snap numeric, (4) GLM-seeded SymPy (added by
    `critpt_glm_patch.apply_critpt_patch`), (5) typed default.

    The solve() signature now accepts an optional `glm_turn` argument so the
    GLM-seeded fallback can read the grounded roots produced by the
    dialogue engine.  This is the contract the seeded patch expects.
    """

    def __init__(self):
        self.phys_alu = PhysicsALU(mode="SV")
        self.native = NativeDynamicSolver()

    def solve(self, problem: str, spec: TemplateSpec,
              glm_turn: Optional[Any] = None) -> AnswerCandidate:
        cand = self._try_physics_alu(problem, spec)
        if cand:
            return cand
        cand = self._try_arith_alu(problem, spec)
        if cand:
            return cand
        cand = self._try_lattice_snap_numeric(problem, spec)
        if cand:
            return cand
        # The GLM-seeded route is monkey-patched onto this class by
        # critpt_glm_patch.apply_critpt_patch().  When present it returns
        # an AnswerCandidate; when absent (or it returns None) we fall
        # through to the typed default.
        seeded = getattr(self, "_try_glm_seeded", None)
        if seeded is not None:
            cand = seeded(problem, spec, glm_turn)
            if cand:
                return cand
        return self._typed_default(spec)

    # ── route 1 : physics ALU ─────────────────────────────────────────────────
    _PHYS_PATTERNS = [
        (r"\bSchwarzschild\b|\bevent\s+horizon\b", "schwarzschild"),
        (r"\bLorentz\b|\bgamma\s+factor\b",        "lorentz"),
        (r"\bescape\s+velocity\b",                  "escape_vel"),
        (r"\bdisplacement\b.*\btime\b|\bv0\b.*\bacceleration\b", "kinematics"),
        (r"\bphoton\s+energy\b|\bE\s*=\s*h",        "photon_energy"),
        (r"\bCompton\b",                             "compton"),
        (r"\bbeta\s+function\b",                     "qft_beta"),
        (r"\bparafermion\b|\bjosephson\s+phase\b",  "parafermion"),
        (r"\bverlinde\b",                            "verlinde"),
    ]

    def _try_physics_alu(self, problem: str, spec: TemplateSpec) -> Optional[AnswerCandidate]:
        for pat, route in self._PHYS_PATTERNS:
            if re.search(pat, problem, flags=re.I):
                nums = [F(x) for x in re.findall(r"-?\d+(?:\.\d+)?", problem)]
                if not nums:
                    return None
                try:
                    if route == "schwarzschild":
                        return self._wrap_alu(
                            self.phys_alu.schwarzschild_radius(nums[0])["result_exact"],
                            "PhysicsALU", spec)
                    if route == "lorentz":
                        v = nums[0] if abs(nums[0]) >= 1 else nums[0] * F(299792458, 1)
                        return self._wrap_alu(
                            self.phys_alu.lorentz_factor(v)["result_exact"],
                            "PhysicsALU", spec)
                except Exception:
                    pass
        return None

    # ── route 2 : arithmetic ALU ──────────────────────────────────────────────
    def _try_arith_alu(self, problem: str, spec: TemplateSpec) -> Optional[AnswerCandidate]:
        for pat in [r"\bgcd\s*\(\s*\d", r"\blcm\s*\(\s*\d", r"\bfactorial\s*\(\s*\d"]:
            if re.search(pat, problem, flags=re.I):
                ans, mode = self.native.solve(problem)
                if ans is not None:
                    return self._wrap_alu(str(ans), f"NoiseALU/{mode}", spec)
        return None

    # ── route 3 : lattice-snap numeric ───────────────────────────────────────
    def _try_lattice_snap_numeric(self, problem: str, spec: TemplateSpec) -> Optional[AnswerCandidate]:
        rs = spec.return_spec
        if all("sympy" in t.lower() or "Expr" in t for t in rs.types):
            return None
        nums = [int(n) for n in re.findall(r"(?<![\w.])(\d{1,8})(?![\w.])", problem)
                if 1 <= int(n) <= 99999999]
        if not nums:
            return None

        on_lattice: List[Tuple[int, Fraction]] = []
        for n in nums[:24]:
            try:
                snap = lattice_snap_value(n)
                if snap["on_lattice"] and snap["nrci_frac"] >= NRCI_PHASE_LOCK:
                    on_lattice.append((n, snap["nrci_frac"]))
            except Exception:
                continue

        if not on_lattice:
            return None
        on_lattice.sort(key=lambda x: x[1], reverse=True)
        chosen, conf = on_lattice[0]

        exprs = [self._coerce_to_type(str(chosen), ty) for ty in rs.types]
        while len(exprs) < rs.arity:
            exprs.append(self._coerce_to_type(
                str(chosen), rs.types[0] if rs.types else "float"))
        return AnswerCandidate(exprs, "Lattice-Snap numeric (phase-locked)",
                               conf, [f"Selected n={chosen} via Lattice Snap"])

    # ── route 5 : typed default ──────────────────────────────────────────────
    def _typed_default(self, spec: TemplateSpec) -> AnswerCandidate:
        types = spec.return_spec.types or ["float"] * spec.return_spec.arity
        exprs = [self._coerce_to_type("0", ty) for ty in types]
        return AnswerCandidate(exprs, "typed_default", F(0),
                               ["No route produced a Phase-Locked answer."])

    # ── helpers ───────────────────────────────────────────────────────────────
    def _wrap_alu(self, raw: str, method: str, spec: TemplateSpec) -> AnswerCandidate:
        snap = lattice_snap_value(raw)
        exprs = [self._coerce_to_type(raw, ty) for ty in spec.return_spec.types]
        while len(exprs) < spec.return_spec.arity:
            exprs.append(self._coerce_to_type("0", "float"))
        return AnswerCandidate(exprs, method, snap["nrci_frac"],
                               [f"Lattice snap sw={snap['sw']} ({snap['lattice']})"])

    @staticmethod
    def _coerce_to_type(raw: str, ty: str) -> str:
        tylow = ty.lower()
        m = re.search(r"-?\d+(?:/\d+)?(?:\.\d+)?", raw.strip())
        num_src = m.group(0) if m else "0"
        if "list" in tylow:
            return (f"[float(sp.Rational('{num_src}'))]"
                    if "/" in num_src else f"[float({num_src})]")
        if "tuple" in tylow:
            return f"({num_src},)"
        if "sympy" in tylow or "expr" in tylow:
            return f"sp.sympify({num_src!r})"
        if "int" in tylow:
            return str(int(float(num_src)))
        return (f"float(sp.Rational('{num_src}'))"
                if "/" in num_src else repr(float(num_src)))


# ═══════════════════════════════════════════════════════════════════════════════
# 5.  EMIT ANSWER FILE
# ═══════════════════════════════════════════════════════════════════════════════

def emit_answer_file(record: dict, spec: TemplateSpec,
                     cand: AnswerCandidate) -> str:
    body_lines = [
        "# ── UBP × CritPt Sovereignty Run v3.1 ────────────────────────────",
        f"# Method        : {cand.method}",
        f"# NRCI          : {cand.confidence.numerator}/{cand.confidence.denominator}",
        f"# Lattice class : {record.get('fp_lattice')}",
        f"# GLM Trace     : {record.get('glm_trace')}",
        f"# GLM Roots     : {', '.join(record.get('glm_roots', []))}",
        f"# GLM Tax       : {record.get('glm_tax', 0):.2f}",
    ]
    for n in cand.notes:
        body_lines.append(f"# {n}")

    if any("sp." in e for e in cand.values) and "import sympy" not in spec.raw_template:
        body_lines.insert(0, "import sympy as sp")
    body_lines.append("")

    for nm, val in zip(spec.return_spec.names, cand.values):
        body_lines.append(f"{nm} = {val}")
    body_lines.append("")
    if spec.return_spec.arity == 1:
        body_lines.append(f"return {spec.return_spec.names[0]}")
    else:
        body_lines.append("return " + ", ".join(spec.return_spec.names))

    body = "\n    ".join(body_lines)
    tmpl = spec.raw_template

    # Try the explicit "FILL IN" marker first, then a trailing `return`,
    # otherwise append the body to the end of the file.  (Original code
    # could leave `new_tmpl` unbound in the third branch.)
    m = re.search(r"#\s*-+\s*FILL\s+IN\s+YOUR\s+RESULTS?\s+BELOW\s*-+.*",
                  tmpl, flags=re.S | re.I)
    if m:
        new_tmpl = tmpl[: m.start()] + body + "\n"
    else:
        rm = re.search(r"^\s*return\s+\w+.*$", tmpl, flags=re.M)
        if rm:
            new_tmpl = tmpl[: rm.start()] + "    " + body + "\n"
        else:
            new_tmpl = tmpl.rstrip() + "\n    " + body + "\n"

    return (f"# Auto-generated by ubp_critpt_sovereign_v3.py\n"
            f"# Problem: {record['problem_id']}\n\n{new_tmpl}")


# ═══════════════════════════════════════════════════════════════════════════════
# 6.  CritPt RECORD LOADER
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass
class CritPtRecord:
    problem_id: str
    problem_description: str
    code_template: str


def load_critpt(path: str = "critpt.json") -> List[CritPtRecord]:
    """Load the CritPt benchmark from a JSON file.  Accepts any path the
    caller supplies; defaults to ./critpt.json if unspecified.
    """
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return [CritPtRecord(r["problem_id"],
                         r["problem_description"],
                         r["code_template"])
            for r in data]


# ═══════════════════════════════════════════════════════════════════════════════
# 7.  ONE-SHOT critpt_glm_patch APPLICATION
# ═══════════════════════════════════════════════════════════════════════════════
#
# Apply at import time so re-instantiating `SovereigntyRunner` doesn't stack
# patches on top of each other.

import critpt_glm_patch as _critpt_glm_patch  # noqa: E402
_critpt_glm_patch.apply_critpt_patch(
    None,                  # SovereigntyRunner ref no longer needed by patch
    UBPSovereignSolver,
    AnswerCandidate,
    NRCI_PHASE_LOCK,
    lattice_snap_value,
)


# ═══════════════════════════════════════════════════════════════════════════════
# 8.  SOVEREIGNTY RUNNER
# ═══════════════════════════════════════════════════════════════════════════════

class SovereigntyRunner:
    """Top-level orchestrator.  Boots the UBP stack, the GLM (v3.1 if
    available, else v3.0), and the GLM rules engine, and dispatches each
    CritPt record through them.
    """

    def __init__(self,
                 system_kb_path: str = "ubp_system_kb.json",
                 lang_kb_path:   str = "ubp_lang_kb_combined_v4.json",
                 use_v31: bool = True):
        print("[Sovereign] Booting UBP full stack ...")
        self.solver = UBPSovereignSolver()

        if use_v31 and _HAS_V31:
            print("[Sovereign] Booting GLM v3.1 Semantic Engine ...")
            self.glm, self._glm_report = create_semantic_engine(
                system_kb_path, lang_kb_path)
            print(f"[Sovereign] GLM v3.1 ready: "
                  f"+{self._glm_report['added_to_vocab']} pack terms, "
                  f"{self._glm_report['pack_gaps']} pack gaps")
        else:
            print("[Sovereign] Booting GLM v3.0 Dialogue Engine ...")
            self.glm = _create_v30_engine(system_kb_path, lang_kb_path)
            self._glm_report = None

        print("[Sovereign] Booting GLM Rules Engine ...")
        self.rules_engine = GLMRulesEngine(lang_kb_path)
        print("[Sovereign] Ready.\n")

    # Single point of contact for GLM — picks the best-available .respond*.
    def _respond_best(self, query: str, max_depth: int = 3):
        if hasattr(self.glm, "respond_semantic"):
            return self.glm.respond_semantic(query, max_depth=max_depth)
        return self.glm.respond(query, max_depth=max_depth)

    def run_one(self, rec: CritPtRecord, out_dir: Path) -> dict:
        # Normalise the description.
        rec.problem_description = self.rules_engine.preprocess(rec.problem_description)

        spec = parse_template(rec.code_template)
        snap = lattice_snap_value(rec.problem_id + ": " + rec.problem_description)

        # GLM semantic reasoning.
        glm_turn = self._respond_best(rec.problem_description, max_depth=3)

        cand = self.solver.solve(rec.problem_description, spec, glm_turn)

        record = {
            "problem_id":   rec.problem_id,
            "fp_lattice":   snap["lattice"],
            "method":       cand.method,
            "confidence":   f"{cand.confidence.numerator}/{cand.confidence.denominator}",
            "phase_locked": cand.confidence >= NRCI_PHASE_LOCK,
            "glm_trace":    getattr(glm_turn, "response", ""),
            "glm_roots":    [r.ubp_id for r in getattr(glm_turn, "physical_roots", [])],
            "glm_tax":      float(getattr(glm_turn, "tax", 0.0)),
        }

        out_dir.mkdir(parents=True, exist_ok=True)
        (out_dir / f"{rec.problem_id}_answer.py").write_text(
            emit_answer_file(record, spec, cand))
        return record

    def run_all(self, records: List[CritPtRecord], out_dir: str) -> List[dict]:
        out = Path(out_dir or "out_sovereign")
        results: List[dict] = []
        for i, r in enumerate(records, 1):
            try:
                rec = self.run_one(r, out)
                print(f"[{i:>2}/{len(records)}] {r.problem_id:22s} "
                      f"lat={rec['fp_lattice']:11s} method={rec['method'][:20]}")
                results.append(rec)
            except Exception as e:
                print(f"[{i:>2}/{len(records)}] {r.problem_id} ERROR: {e}")
        return results


# ═══════════════════════════════════════════════════════════════════════════════
# 9.  CLI
# ═══════════════════════════════════════════════════════════════════════════════

def main(argv: Optional[List[str]] = None) -> int:
    p = argparse.ArgumentParser(
        description="UBP × CritPt sovereignty runner v3.1")
    p.add_argument("--critpt", default="critpt.json",
                   help="path to the CritPt benchmark JSON")
    p.add_argument("--system-kb", default="ubp_system_kb.json")
    p.add_argument("--lang-kb",   default="ubp_lang_kb_combined_v4.json")
    p.add_argument("--out", default="out_sovereign",
                   help="directory to write generated answer files into")
    p.add_argument("--limit", type=int, default=0,
                   help="0 = run the whole benchmark, N = first N records")
    p.add_argument("--no-v31", action="store_true",
                   help="force the legacy v3.0 dialogue engine")
    args = p.parse_args(argv)

    runner = SovereigntyRunner(
        system_kb_path=args.system_kb,
        lang_kb_path=args.lang_kb,
        use_v31=not args.no_v31,
    )
    records = load_critpt(args.critpt)
    if args.limit:
        records = records[: args.limit]
    runner.run_all(records, args.out)
    print(f"\nWrote {len(records)} Python answer files to {args.out}/")
    return 0


if __name__ == "__main__":
    sys.exit(main())
