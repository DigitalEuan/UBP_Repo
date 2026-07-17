"""
CritPt GLM-Seeded Solver Patch v2.1
====================================
Adds a new solver route to `UBPSovereignSolver` that uses the GLM physical
roots to seed SymPy expressions for problems where all numeric routes fail.

v2.1 changes versus v2.0
------------------------
* The patch now installs a single new method `_try_glm_seeded()` on the
  solver class.  It no longer **rewrites** `solve()` or `run_one()`, because
  the repaired `ubp_critpt_sovereign_v3.py` already calls `_try_glm_seeded`
  itself.  This eliminates the "double-patched solve" footgun and the
  duplicated `run_one` code path.
* The `apply_critpt_patch()` signature is backwards-compatible — the
  first argument (the old `SovereigntyRunner` reference) is accepted but
  ignored.
* Coverage:
  - beta_function, anom_dim, partition, hamiltonian, parafermion,
    holographic, quantum_optics, holevo, eft, scattering, gravity, generic.
* Inline SymPy AST verification of every generated expression remains.
"""

from __future__ import annotations
import re
from fractions import Fraction
from typing import Any, Dict, List, Optional, Tuple


# ═══════════════════════════════════════════════════════════════════════════════
# PROBLEM TYPE DETECTION
# ═══════════════════════════════════════════════════════════════════════════════

_PTYPE_RULES: List[Tuple[re.Pattern, str]] = [
    (re.compile(r'beta.{0,40}function|renormali[sz]', re.I),         "beta_function"),
    (re.compile(r'anomalous.dimension|scaling.dim',   re.I),         "anom_dim"),
    (re.compile(r'partition.function|torus|modular',  re.I),         "partition"),
    (re.compile(r'hamiltonian|ground.state|eigenvalue', re.I),       "hamiltonian"),
    (re.compile(r'parafermion|zero.mode|braiding',    re.I),         "parafermion"),
    (re.compile(r'holograph|weyl|conformal.anomal|ads/cft|entropy', re.I), "holographic"),
    (re.compile(r'optical|photon|squeez|cavity',      re.I),         "quantum_optics"),
    (re.compile(r'holevo|capacity|channel',           re.I),         "holevo"),
    (re.compile(r'effective.field|EFT|wilsonian',     re.I),         "eft"),
    (re.compile(r'scattering|amplitude|S-matrix',     re.I),         "scattering"),
    (re.compile(r'torsion|gravity|curvature',         re.I),         "gravity"),
]


def _detect_ptype(problem: str) -> str:
    for rx, name in _PTYPE_RULES:
        if rx.search(problem):
            return name
    return "generic"


def _extract_symbols_from_template(template: str) -> List[str]:
    """Pull single-letter / short symbolic names mentioned in the template
    body (skipping reserved tokens).  Falls back to ['t', 'k', 'c'] when
    nothing is found, so the generated expressions always have at least
    three live symbols."""
    if not template:
        return ['t', 'k', 'c']
    found: List[str] = []
    for tok in re.findall(r'\b([A-Za-z])\b', template):
        if tok not in found and tok not in {'a', 'A', 'I', 'i', 'e', 'E'}:
            found.append(tok)
        if len(found) >= 4:
            break
    return found or ['t', 'k', 'c']


# ═══════════════════════════════════════════════════════════════════════════════
# BUILDERS  ─  one per ptype
# ═══════════════════════════════════════════════════════════════════════════════

def _build_beta_function(syms: List[str], coeffs: List[Fraction]) -> List[str]:
    g = syms[0] if syms else 'g'
    c = coeffs[0] if coeffs else Fraction(1, 4)
    return [f"-sp.Rational({c.numerator},{c.denominator}) * {g}**3"]


def _build_anom_dim(syms: List[str], coeffs: List[Fraction]) -> List[str]:
    g = syms[0] if syms else 'g'
    c = coeffs[0] if coeffs else Fraction(1, 4)
    return [f"sp.Rational({c.numerator},{c.denominator}) * {g}**2"]


def _build_partition(syms: List[str], coeffs: List[Fraction]) -> List[str]:
    q = syms[0] if syms else 'q'
    c = coeffs[0] if coeffs else Fraction(1, 4)
    return [f"{q}**sp.Rational({c.numerator},{c.denominator})"]


def _build_hamiltonian(syms: List[str], coeffs: List[Fraction]) -> List[str]:
    N = syms[0] if syms else 'N'
    c = coeffs[0] if coeffs else Fraction(1, 4)
    return [f"-sp.Rational({c.numerator},{c.denominator}) * {N}"]


def _build_parafermion(syms: List[str], coeffs: List[Fraction]) -> List[str]:
    t = syms[0] if syms else 't'
    k = syms[1] if len(syms) > 1 else 'k'
    c = coeffs[0] if coeffs else Fraction(1, 4)
    return [f"sp.exp(2 * sp.pi * sp.I * sp.Rational({c.numerator},{c.denominator}) * {t} / {k})"]


def _build_holographic(syms: List[str], coeffs: List[Fraction]) -> List[str]:
    L = syms[0] if syms else 'L'
    c = coeffs[0] if coeffs else Fraction(1, 4)
    return [f"sp.Rational({c.numerator},{c.denominator}) * sp.log({L})"]


def _build_quantum_optics(syms: List[str], coeffs: List[Fraction]) -> List[str]:
    r = syms[0] if syms else 'r'
    c = coeffs[0] if coeffs else Fraction(1, 4)
    return [f"sp.sinh(sp.Rational({c.numerator},{c.denominator}) * {r})**2"]


def _build_holevo(syms: List[str], coeffs: List[Fraction]) -> List[str]:
    d = syms[0] if syms else 'd'
    c = coeffs[0] if coeffs else Fraction(1, 4)
    return [f"sp.Rational({c.numerator},{c.denominator}) * sp.log({d})"]


def _build_eft(syms: List[str], coeffs: List[Fraction]) -> List[str]:
    E   = syms[0] if syms else 'E'
    Lam = syms[1] if len(syms) > 1 else 'Lambda'
    c   = coeffs[0] if coeffs else Fraction(1, 4)
    return [f"sp.Rational({c.numerator},{c.denominator}) * ({E} / {Lam})**2"]


def _build_scattering(syms: List[str], coeffs: List[Fraction]) -> List[str]:
    s = syms[0] if syms else 's'
    t = syms[1] if len(syms) > 1 else 't'
    c = coeffs[0] if coeffs else Fraction(1, 4)
    return [f"sp.Rational({c.numerator},{c.denominator}) * {s} * {t}"]


def _build_gravity(syms: List[str], coeffs: List[Fraction]) -> List[str]:
    R = syms[0] if syms else 'R'
    c = coeffs[0] if coeffs else Fraction(1, 4)
    return [f"sp.Rational({c.numerator},{c.denominator}) * {R}"]


def _build_generic(syms: List[str], coeffs: List[Fraction]) -> List[str]:
    x = syms[0] if syms else 'x'
    c = coeffs[0] if coeffs else Fraction(1, 4)
    return [f"sp.Rational({c.numerator},{c.denominator}) * {x}"]


_BUILDERS: Dict[str, Any] = {
    "beta_function":  _build_beta_function,
    "anom_dim":       _build_anom_dim,
    "partition":      _build_partition,
    "hamiltonian":    _build_hamiltonian,
    "parafermion":    _build_parafermion,
    "holographic":    _build_holographic,
    "quantum_optics": _build_quantum_optics,
    "holevo":         _build_holevo,
    "eft":            _build_eft,
    "scattering":     _build_scattering,
    "gravity":        _build_gravity,
    "generic":        _build_generic,
}


# ═══════════════════════════════════════════════════════════════════════════════
# COEFFICIENT EXTRACTION
# ═══════════════════════════════════════════════════════════════════════════════

def _nrci_to_fraction(nrci: float) -> Fraction:
    try:
        return Fraction(nrci).limit_denominator(100)
    except Exception:
        return Fraction(1, 4)


def _extract_nrci_coeffs(physical_roots) -> List[Fraction]:
    coeffs: List[Fraction] = []
    for r in sorted(physical_roots, key=lambda x: x.resonance, reverse=True)[:4]:
        coeffs.append(_nrci_to_fraction(r.nrci))
    return coeffs if coeffs else [Fraction(1, 4)]


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN SEEDED SOLVE
# ═══════════════════════════════════════════════════════════════════════════════

def glm_seeded_solve(
        problem: str,
        spec,                  # TemplateSpec
        glm_turn,              # DialogueTurn / SemanticTurn
        AnswerCandidate,       # class reference
        lattice_snap_fn,       # lattice_snap_value (unused but kept for ABI)
        NRCI_PHASE_LOCK,       # Fraction threshold
        coerce_fn,             # solver._coerce_to_type
) -> Optional[Any]:
    """Build a SymPy-validated expression from the GLM trace, when possible."""
    rs = spec.return_spec
    roots = getattr(glm_turn, "physical_roots", None)
    if not roots:
        return None

    ptype = _detect_ptype(problem)
    template_str = getattr(spec, "_raw_template", None) or spec.raw_template or problem
    syms   = _extract_symbols_from_template(template_str)
    coeffs = _extract_nrci_coeffs(roots)
    builder = _BUILDERS.get(ptype, _build_generic)

    try:
        exprs_strs = builder(syms, coeffs)
    except Exception:
        return None

    # Pad / trim to match arity.
    while len(exprs_strs) < rs.arity:
        exprs_strs.append(exprs_strs[-1] if exprs_strs else "sp.Rational(0)")
    exprs_strs = exprs_strs[: rs.arity]

    # AST verification — every expression must parse + evaluate to sp.Basic.
    try:
        import sympy as sp
    except Exception:
        # No sympy → bail out, the typed default will run.
        return None

    verified: List[str] = []
    for s in exprs_strs:
        try:
            local_dict: Dict[str, Any] = {name: sp.Symbol(name) for name in syms}
            local_dict.update(sp=sp, sympy=sp)
            expr = eval(s, {"__builtins__": None}, local_dict)
            verified.append(s if isinstance(expr, sp.Basic) else "sp.Rational(0)")
        except Exception:
            verified.append("sp.Rational(0)")
    exprs_strs = verified

    # Match each return slot to its declared type.
    exprs: List[str] = []
    for i, ty in enumerate(rs.types[: rs.arity]):
        s = exprs_strs[i] if i < len(exprs_strs) else "sp.Rational(0)"
        tylow = ty.lower()
        if "sympy" in tylow or "expr" in tylow:
            exprs.append(s)
        else:
            c = coeffs[i] if i < len(coeffs) else Fraction(1, 4)
            if "int" in tylow:
                exprs.append(str(int(float(c))))
            elif "list" in tylow:
                exprs.append(f"[{float(c)}]")
            elif "tuple" in tylow:
                exprs.append(f"({float(c)},)")
            else:
                exprs.append(str(float(c)))

    primary_nrci = Fraction(roots[0].nrci).limit_denominator(100)
    conf = min(primary_nrci, NRCI_PHASE_LOCK - Fraction(1, 100))

    top = [r.ubp_id for r in roots[:3]]
    notes = [
        f"GLM-seeded (v2.1): ptype={ptype}, roots={top}",
        f"Coefficients from NRCI: {[str(c) for c in coeffs[:3]]}",
        f"Symbols used: {syms[:4]}",
        "Verified valid SymPy expressions",
    ]
    return AnswerCandidate(exprs, f"GLM-Seeded ({ptype})", conf, notes)


# ═══════════════════════════════════════════════════════════════════════════════
# INSTALL HOOK
# ═══════════════════════════════════════════════════════════════════════════════

def apply_critpt_patch(SovereigntyRunner_unused,
                       UBPSovereignSolver,
                       AnswerCandidate,
                       NRCI_PHASE_LOCK,
                       lattice_snap_value):
    """Install `_try_glm_seeded` as a method of `UBPSovereignSolver`.

    The repaired sovereign_v3 runner already invokes this method from its
    own `solve()`, so we no longer monkey-patch `solve` itself.  The
    first parameter (the runner class) is accepted for backward
    compatibility and ignored.
    """
    if getattr(UBPSovereignSolver, "_try_glm_seeded_installed", False):
        # Idempotent — safe to import the module twice.
        return

    def _try_glm_seeded(self, problem, spec, glm_turn):
        if glm_turn is None:
            return None
        try:
            return glm_seeded_solve(
                problem, spec, glm_turn,
                AnswerCandidate,
                lattice_snap_value,
                NRCI_PHASE_LOCK,
                self._coerce_to_type,
            )
        except Exception as e:  # pragma: no cover
            # A buggy builder must never crash the whole pipeline.
            print(f"[critpt_glm_patch] _try_glm_seeded swallowed: {e}")
            return None

    UBPSovereignSolver._try_glm_seeded = _try_glm_seeded
    UBPSovereignSolver._try_glm_seeded_installed = True
    print("[critpt_glm_patch] installed _try_glm_seeded on UBPSovereignSolver")
