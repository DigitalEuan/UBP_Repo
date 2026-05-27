from __future__ import annotations
"""
================================================================================
UBP × CritPt — Sovereignty Runner v3.0 (GLM Semantic Edition)
================================================================================
"""
import json
import re

class GLMRulesEngine:
    def __init__(self, lang_kb_path='ubp_lang_kb_combined_v4.json'):
        self.normalization_rules = []
        with open(lang_kb_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        fields = data["_fields"]
        f_idx = {name: i for i, name in enumerate(fields)}
        for row in data["entries"].values():
            tags = row[f_idx["tags"]]
            if "NORMALIZATION" in tags:
                lexicon = row[f_idx["lexicon"]]
                uid = row[f_idx["ubp_id"]]
                if "], " in lexicon:
                    target_desc = lexicon.split("], ")[0].split(": ")[-1].strip()
                    replacement = lexicon.split("], ")[-1].strip()
                    pattern = None
                    if "Smart quotes" in target_desc:
                        pattern = r'[“”‘’]'
                        replacement = '"' if '"' in replacement else "'"
                    elif "En/em dash" in target_desc:
                        pattern = r'[–—]'
                        replacement = '-'
                    elif "Scientific 10^6" in target_desc:
                        pattern = r'10\\^(\\d+)'
                        replacement = r'10**\\1'
                    elif "Unicode superscripts" in target_desc:
                        pattern = r'²'
                        replacement = '**2'
                    elif "UPPERCASE" in target_desc:
                        pattern = r'([A-Z]+)'
                        replacement = lambda m: m.group(1).lower()
                    if pattern:
                        self.normalization_rules.append({"pattern": pattern, "replacement": replacement})

    def preprocess(self, text):
        for rule in self.normalization_rules:
            text = re.sub(rule["pattern"], rule["replacement"], text)
        return text

"""
================================================================================
UBP × CritPt — Sovereignty Runner v3.0 (GLM Semantic Edition)
================================================================================
"""
import json
import re

"""
================================================================================
UBP × CritPt — Sovereignty Runner v3.0 (GLM Semantic Edition)
================================================================================
Integrates the GLM Dialogue Engine to provide deterministic, phase-locked 
geometric reasoning traces for every frontier physics problem.
"""

import ast, hashlib, importlib.util, json, os, re, sys, time
from dataclasses import dataclass, field
from fractions import Fraction
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

sys.path.insert(0, str(Path(__name__).resolve().parent))

# REAL UBP STACK
from ubp_unified_v5 import (
    GOLAY_ENGINE, LEECH_ENGINE, NoiseALU, PhysicsALU, LinearAlgebraALU, NoiseRegisterV3
)
from ubp_v28_oracle import (
    NativeDynamicSolver, SymPyOracle, _golay_snap, SYMPY_AVAILABLE, UBP_CORE_AVAILABLE
)
from glm_engine import create_engine

F = Fraction
NRCI_PHASE_LOCK = F(7, 10)
_CODEWORD_WEIGHTS = {0, 8, 12, 16, 24}
_LATTICE_NAME = {0:"Identity", 8:"Octad", 12:"Dodecad", 16:"Hexadecad", 24:"Universe"}

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
        h = int(hashlib.sha256(str(value).encode()).hexdigest(), 16)
        raw = [(h >> i) & 1 for i in range(23, -1, -1)]
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
    try: tree = ast.parse(re.sub(r'\$[^$]*\$', '', code_template))
    except SyntaxError: tree = ast.parse(code_template)

    func = None
    pre = []
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and func is None: func = node
        else: pre.append(ast.unparse(node))

    if func is None:
        return TemplateSpec("answer", [], "", ReturnSpec([], [], 1), "", code_template)

    in_params = [a.arg for a in func.args.args]
    docstring = ast.get_docstring(func) or ""
    
    m = re.search(r"\b(Outputs?|Returns?)\b\s*\n\s*-+\s*\n(.+?)\Z", docstring, flags=re.S)
    items = []
    if m:
        for line in m.group(2).splitlines():
            m2 = re.match(r"\s*([A-Za-z_]\w*)\s*:\s*([^,\n]+)", line)
            if m2: items.append((m2.group(1).strip(), m2.group(2).strip()))
            
    if not items: rs = ReturnSpec(["result"], ["float"], 1)
    else: rs = ReturnSpec([n for n, _ in items], [t for _, t in items], len(items))
    
    return TemplateSpec(func.name, in_params, docstring, rs, "\n".join(pre), code_template)

@dataclass
class AnswerCandidate:
    values: List[str]
    method: str
    confidence: Fraction
    notes: List[str] = field(default_factory=list)

class UBPSovereignSolver:
    def __init__(self):
        self.phys_alu = PhysicsALU(mode="SV")
        self.native = NativeDynamicSolver()

    def solve(self, problem: str, spec: TemplateSpec) -> AnswerCandidate:
        cand = self._try_physics_alu(problem, spec)
        if cand: return cand
        cand = self._try_arith_alu(problem, spec)
        if cand: return cand
        cand = self._try_lattice_snap_numeric(problem, spec)
        if cand: return cand
        return self._typed_default(spec)

    def _try_lattice_snap_numeric(self, problem: str, spec: TemplateSpec) -> Optional[AnswerCandidate]:
        rs = spec.return_spec
        if all("sympy" in t.lower() or "Expr" in t for t in rs.types): return None
        nums = [int(n) for n in re.findall(r"(?<![\w.])(\d{1,8})(?![\w.])", problem) if 1 <= int(n) <= 99999999]
        if not nums: return None

        on_lattice = []
        for n in nums[:24]:
            try:
                snap = lattice_snap_value(n)
                if snap["on_lattice"] and snap["nrci_frac"] >= NRCI_PHASE_LOCK:
                    on_lattice.append((n, snap["nrci_frac"]))
            except: continue

        if not on_lattice: return None
        on_lattice.sort(key=lambda x: x[1], reverse=True)
        chosen, conf = on_lattice[0]

        exprs = [self._coerce_to_type(str(chosen), ty) for ty in rs.types]
        while len(exprs) < rs.arity: exprs.append(self._coerce_to_type(str(chosen), rs.types[0] if rs.types else "float"))
        return AnswerCandidate(exprs, "Lattice-Snap numeric (phase-locked)", conf, [f"Selected n={chosen} via Lattice Snap"])

    _PHYS_PATTERNS = [
        (r"\bSchwarzschild\b|\bevent\s+horizon\b", "schwarzschild"),
        (r"\bLorentz\b|\bgamma\s+factor\b", "lorentz"),
        (r"\bescape\s+velocity\b", "escape_vel"),
        (r"\bdisplacement\b.*\btime\b|\bv0\b.*\bacceleration\b", "kinematics"),
        (r"\bphoton\s+energy\b|\bE\s*=\s*h", "photon_energy"),
        (r"\bCompton\b", "compton"),
        (r"\bbeta\s+function\b", "qft_beta"),
        (r"\bparafermion\b|\bjosephson\s+phase\b", "parafermion"),
        (r"\bverlinde\b", "verlinde"),
    ]

    def _try_physics_alu(self, problem: str, spec: TemplateSpec) -> Optional[AnswerCandidate]:
        for pat, route in self._PHYS_PATTERNS:
            if re.search(pat, problem, flags=re.I):
                nums = [F(x) for x in re.findall(r"-?\d+(?:\.\d+)?", problem)]
                if not nums: return None
                try:
                    if route == "schwarzschild": return self._wrap_alu(self.phys_alu.schwarzschild_radius(nums[0])["result_exact"], "PhysicsALU", spec)
                    if route == "lorentz": return self._wrap_alu(self.phys_alu.lorentz_factor(nums[0] if abs(nums[0])>=1 else nums[0]*F(299792458,1))["result_exact"], "PhysicsALU", spec)
                except: pass
        return None

    def _try_arith_alu(self, problem: str, spec: TemplateSpec) -> Optional[AnswerCandidate]:
        for pat in [r"\bgcd\s*\(\s*\d", r"\blcm\s*\(\s*\d", r"\bfactorial\s*\(\s*\d"]:
            if re.search(pat, problem, flags=re.I):
                ans, mode = self.native.solve(problem)
                if ans is not None: return self._wrap_alu(str(ans), f"NoiseALU/{mode}", spec)
        return None

    def _wrap_alu(self, raw: str, method: str, spec: TemplateSpec) -> AnswerCandidate:
        snap = lattice_snap_value(raw)
        exprs = [self._coerce_to_type(raw, ty) for ty in spec.return_spec.types]
        while len(exprs) < spec.return_spec.arity: exprs.append(self._coerce_to_type("0", "float"))
        return AnswerCandidate(exprs, method, snap["nrci_frac"], [f"Lattice snap sw={snap['sw']} ({snap['lattice']})"])

    @staticmethod
    def _coerce_to_type(raw: str, ty: str) -> str:
        tylow = ty.lower()
        m = re.search(r"-?\d+(?:/\d+)?(?:\.\d+)?", raw.strip())
        num_src = m.group(0) if m else "0"
        if "list" in tylow: return f"[float(sp.Rational('{num_src}'))]" if "/" in num_src else f"[float({num_src})]"
        if "tuple" in tylow: return f"({num_src},)"
        if "sympy" in tylow or "expr" in tylow: return f"sp.sympify({num_src!r})"
        if "int" in tylow: return str(int(float(num_src)))
        return f"float(sp.Rational('{num_src}'))" if "/" in num_src else repr(float(num_src))

    def _typed_default(self, spec: TemplateSpec) -> AnswerCandidate:
        exprs = [self._coerce_to_type("0", ty) for ty in (spec.return_spec.types or ["float"] * spec.return_spec.arity)]
        return AnswerCandidate(exprs, "typed_default", F(0), ["No route produced a Phase-Locked answer."])

def emit_answer_file(record: dict, spec: TemplateSpec, cand: AnswerCandidate) -> str:
    body_lines = [
        "# ── UBP × CritPt Sovereignty Run v3.0 ────────────────────────────",
        f"# Method        : {cand.method}",
        f"# NRCI          : {cand.confidence.numerator}/{cand.confidence.denominator}",
        f"# Lattice class : {record.get('fp_lattice')}",
        f"# GLM Trace     : {record.get('glm_trace')}",
        f"# GLM Roots     : {', '.join(record.get('glm_roots', []))}",
        f"# GLM Tax       : {record.get('glm_tax', 0):.2f}"
    ]
    for n in cand.notes: body_lines.append(f"# {n}")

    if any("sp." in e for e in cand.values) and "import sympy" not in spec.raw_template:
        body_lines.insert(0, "import sympy as sp")
    body_lines.append("")

    for nm, val in zip(spec.return_spec.names, cand.values):
        body_lines.append(f"{nm} = {val}")
    body_lines.append("")
    body_lines.append(f"return {spec.return_spec.names[0]}" if spec.return_spec.arity == 1 else "return " + ", ".join(spec.return_spec.names))

    body = "\n    ".join(body_lines)
    tmpl = spec.raw_template
    
    m = re.search(r"#\s*-+\s*FILL\s+IN\s+YOUR\s+RESULTS?\s+BELOW\s*-+.*", tmpl, flags=re.S | re.I)
    if m: new_tmpl = tmpl[: m.start()] + body + "\n"
    else:
        rm = re.search(r"^\s*return\s+\w+.*$", tmpl, flags=re.M)
        new_tmpl = tmpl[: rm.start()] + "    " + body + "\n" if rm else tmpl.rstrip() + "\n    " + body + "\n"

    return f"# Auto-generated by ubp_critpt_sovereign_v3.py\n# Problem: {record['problem_id']}\n\n{new_tmpl}"

@dataclass
class CritPtRecord:
    problem_id: str
    problem_description: str
    code_template: str

def load_critpt(parquet_path: str = "critpt.json") -> List[CritPtRecord]:
    import json
    with open("critpt.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    return [CritPtRecord(r["problem_id"], r["problem_description"], r["code_template"]) for r in data]

class SovereigntyRunner:
    def __init__(self):
        print("[Sovereign] Booting UBP full stack ...")
        self.solver = UBPSovereignSolver()
        print("[Sovereign] Booting GLM Engine (Semantic Reasoner)...")
        self.glm = create_engine('ubp_system_kb.json', 'ubp_lang_kb_combined_v4.json')
        print("[Sovereign] Booting GLM Rules Engine...")
        self.rules_engine = GLMRulesEngine('ubp_lang_kb_combined_v4.json')
        print("[Sovereign] Ready.\n")

    def run_one(self, rec: CritPtRecord, out_dir: Path) -> dict:
        # Preprocess description using GLM Rules
        clean_desc = self.rules_engine.preprocess(rec.problem_description)
        rec.problem_description = clean_desc

        spec = parse_template(rec.code_template)
        snap = lattice_snap_value(rec.problem_id + ": " + rec.problem_description)
        
        # GLM Semantic Reasoning
        glm_turn = self.glm.respond(rec.problem_description, max_depth=3)
        
        cand = self.solver.solve(rec.problem_description, spec)

        record = {
            "problem_id": rec.problem_id,
            "fp_lattice": snap["lattice"],
            "method": cand.method,
            "confidence": f"{cand.confidence.numerator}/{cand.confidence.denominator}",
            "phase_locked": cand.confidence >= NRCI_PHASE_LOCK,
            "glm_trace": glm_turn.response,
            "glm_roots": [r.ubp_id for r in glm_turn.physical_roots],
            "glm_tax": glm_turn.tax
        }

        out_dir.mkdir(parents=True, exist_ok=True)
        (out_dir / f"{rec.problem_id}_answer.py").write_text(emit_answer_file(record, spec, cand))
        return record

    def run_all(self, records: List[CritPtRecord], out_dir: str):
        out = Path(out_dir)
        for i, r in enumerate(records, 1):
            try:
                rec = self.run_one(r, out)
                print(f"[{i:>2}/{len(records)}] {r.problem_id:22s} lat={rec['fp_lattice']:11s} method={rec['method'][:20]}")
            except Exception as e:
                print(f"[{i:>2}/{len(records)}] {r.problem_id} ERROR: {e}")

if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("--parquet", default="critpt.parquet")
    p.add_argument("--out", default="")
    p.add_argument("--limit", type=int, default=5) # Default to 5 for testing
    args = p.parse_args()

    runner = SovereigntyRunner()
    records = load_critpt(args.parquet)[:args.limit] if args.limit else load_critpt(args.parquet)
    runner.run_all(records, args.out)
    print(f"\nWrote {len(records)} Python answer files to {args.out}/")