"""
================================================================================
GLM Integration Smoke Test — runs the runner against stubbed UBP backbone
================================================================================
This test injects minimal fake `ubp_unified_v5` and `ubp_v28_oracle` modules
into `sys.modules` BEFORE importing `ubp_critpt_sovereign_v3`, so we can
verify the wiring of:

    *  `parse_template` recovers the return spec
    *  `emit_answer_file` always returns a non-empty file body
    *  `load_critpt(path)` honours its `path` argument (the v3.0 bug)
    *  `UBPSovereignSolver.solve(problem, spec, glm_turn=None)` runs all
       four routes without crashing
    *  `critpt_glm_patch._try_glm_seeded` is correctly attached to the
       solver class at import time
    *  `SovereigntyRunner.run_one()` produces a record AND writes a file

Run as:   python test_glm_integration.py
================================================================================
"""

from __future__ import annotations
import json
import sys
import tempfile
import types
import unittest
from dataclasses import dataclass, field
from fractions import Fraction
from pathlib import Path
from typing import Any, List


# ── 0. STUB BACKBONE — must be installed BEFORE any glm imports ─────────────────

def _install_stub_backbone():
    """Build minimal stand-ins for the heavy modules the runner imports."""
    # ubp_unified_v5
    if "ubp_unified_v5" not in sys.modules:
        m = types.ModuleType("ubp_unified_v5")

        class _LE:
            @staticmethod
            def calculate_symmetry_tax(v):
                # Symmetry tax proxy: half the Hamming weight, as a Fraction.
                return Fraction(sum(v), 2)

            @staticmethod
            def calculate_nrci(v):
                return Fraction(7, 10)

        class _GE:
            @staticmethod
            def snap_to_codeword(v):
                return list(v), {"syndrome_weight": 0, "anchor_distance": 0}

        class _NoiseALU: pass
        class _PhysicsALU:
            def __init__(self, mode="SV"): pass
            def schwarzschild_radius(self, x):
                return {"result_exact": str(x)}
            def lorentz_factor(self, v):
                return {"result_exact": str(v)}
        class _LAALU: pass
        class _NR3: pass

        m.LEECH_ENGINE = _LE()
        m.GOLAY_ENGINE = _GE()
        m.NoiseALU = _NoiseALU
        m.PhysicsALU = _PhysicsALU
        m.LinearAlgebraALU = _LAALU
        m.NoiseRegisterV3 = _NR3
        # extras some glm modules import:
        class _BLA:
            @staticmethod
            def hamming_distance(a, b):
                return sum(int(x) ^ int(y) for x, y in zip(a, b))
            @staticmethod
            def fold24_to3(v):
                return [sum(v[:8]) & 1, sum(v[8:16]) & 1, sum(v[16:]) & 1]
            @staticmethod
            def hamming_weight(v):
                return sum(v)
        m.BinaryLinearAlgebra = _BLA
        m.MOG_CATEGORIES = tuple(f"S{i}" for i in range(24))
        m.SUBSTRATE = object()
        m.BarnesWallEngine = type("BWE", (), {})
        m.GolayCodeEngine = type("GCE", (), {})
        m.LeechLatticeEngine = type("LLE", (), {})
        m.UBPUltimateSubstrate = type("UUS", (), {})
        m.to_gray_code = staticmethod(lambda n, bits: [(n ^ (n >> 1)) >> i & 1
                                                       for i in range(bits - 1, -1, -1)])
        m.ontological_position_to_vector = staticmethod(lambda *a, **k: [0] * 24)
        sys.modules["ubp_unified_v5"] = m

    # ubp_v28_oracle
    if "ubp_v28_oracle" not in sys.modules:
        m = types.ModuleType("ubp_v28_oracle")
        class _NDS:
            def solve(self, problem):
                if "gcd" in problem:
                    return 6, "native"
                return None, "none"
        class _SO: pass
        m.NativeDynamicSolver = _NDS
        m.SymPyOracle = _SO
        m._golay_snap = staticmethod(lambda v: list(v))
        m.SYMPY_AVAILABLE = True
        m.UBP_CORE_AVAILABLE = True
        sys.modules["ubp_v28_oracle"] = m

    # glm_grammar_patch — heavy, side-effect import. Stub it as a no-op
    # so we can isolate the runner wiring without the 11MB zoned vocab.
    if "glm_grammar_patch" not in sys.modules:
        m = types.ModuleType("glm_grammar_patch")
        sys.modules["glm_grammar_patch"] = m

    # glm_engine — provide a minimal create_engine + DialogueTurn-shaped class.
    if "glm_engine" not in sys.modules:
        m = types.ModuleType("glm_engine")

        @dataclass
        class PhysicalRoot:
            ubp_id: str
            vector: List[int]
            lexicon: str
            resonance: float
            nrci: float

        @dataclass
        class _Turn:
            query: str = ""
            response: str = "stub trace"
            physical_roots: List[Any] = field(default_factory=list)
            tax: float = 0.0

        class _Engine:
            def respond(self, query, max_depth=3):
                return _Turn(query=query, response=f"echo: {query}",
                             physical_roots=[PhysicalRoot(
                                 "LAW_TEST_001", [0]*24, query, 1.0, 0.55)])

        def create_engine(sys_kb, lang_kb):
            return _Engine()

        m.PhysicalRoot = PhysicalRoot
        m.GLMDialogueEngine = _Engine
        m.create_engine = create_engine
        sys.modules["glm_engine"] = m

    # glm_engine_v31 — optional; mark as absent so the runner gracefully
    # falls back to v3.0.  (Setting the module to a stub that raises on
    # `create_semantic_engine` would also work; absence is cleaner.)


_install_stub_backbone()


# ── now import the modules under test ──────────────────────────────────────────
from ubp_critpt_sovereign_v3 import (
    UBPSovereignSolver, SovereigntyRunner,
    parse_template, load_critpt, emit_answer_file,
    AnswerCandidate, ReturnSpec, TemplateSpec,
    NRCI_PHASE_LOCK,
)


class WiringTests(unittest.TestCase):

    def test_solver_has_seeded_route(self):
        self.assertTrue(hasattr(UBPSovereignSolver, "_try_glm_seeded"),
                        "critpt_glm_patch must install _try_glm_seeded on the solver")

    def test_solver_solve_signature(self):
        # solve() must accept (self, problem, spec, glm_turn=None)
        import inspect
        sig = inspect.signature(UBPSovereignSolver.solve)
        params = list(sig.parameters)
        # 'self' + at minimum two named params; glm_turn must be optional.
        self.assertIn("problem", params)
        self.assertIn("spec",    params)
        self.assertIn("glm_turn", params)

    def test_solve_runs_to_typed_default(self):
        solver = UBPSovereignSolver()
        spec = TemplateSpec(
            func_name="answer", in_params=[], docstring="",
            return_spec=ReturnSpec(["result"], ["float"], 1),
            pre_imports="", raw_template="def answer():\n    return 0",
        )
        cand = solver.solve("nothing matches here", spec, glm_turn=None)
        self.assertIsInstance(cand, AnswerCandidate)
        # With no GLM trace and no numeric route, this should be typed_default.
        self.assertIn(cand.method, {"typed_default", "Lattice-Snap numeric (phase-locked)"})


class ParseAndEmitTests(unittest.TestCase):

    def test_parse_recovers_return_spec(self):
        tmpl = (
            "def solve(g):\n"
            "    \"\"\"Compute the beta function.\n"
            "\n"
            "    Outputs\n"
            "    -------\n"
            "    beta : sympy.Expr\n"
            "    \"\"\"\n"
            "    # ----- FILL IN YOUR RESULT BELOW -----\n"
            "    return beta\n"
        )
        spec = parse_template(tmpl)
        self.assertEqual(spec.func_name, "solve")
        self.assertEqual(spec.return_spec.names, ["beta"])
        self.assertEqual(spec.return_spec.types, ["sympy.Expr"])

    def test_emit_handles_missing_marker(self):
        tmpl = "def solve():\n    return 0\n"          # no FILL marker
        spec = parse_template(tmpl)
        cand = AnswerCandidate(["0"], "test", Fraction(0))
        text = emit_answer_file(
            {"problem_id": "T", "fp_lattice": "Identity", "glm_trace": "",
             "glm_roots": [], "glm_tax": 0.0},
            spec, cand,
        )
        self.assertGreater(len(text), 0)
        self.assertIn("Auto-generated by ubp_critpt_sovereign_v3.py", text)


class LoaderTests(unittest.TestCase):

    def test_loader_honours_path(self):
        records = [{
            "problem_id":          "TestA_main",
            "problem_description": "compute gcd",
            "code_template":       "def f():\n    return 1\n",
        }]
        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as fp:
            json.dump(records, fp); name = fp.name
        recs = load_critpt(name)
        self.assertEqual(recs[0].problem_id, "TestA_main")


class RunnerTests(unittest.TestCase):

    def test_run_one_emits_file(self):
        runner = SovereigntyRunner.__new__(SovereigntyRunner)  # bypass __init__
        runner.solver = UBPSovereignSolver()

        from glm_engine import create_engine
        runner.glm = create_engine("x", "y")
        runner._glm_report = None

        class _NoRules:
            normalization_rules = []
            def preprocess(self, x): return x
        runner.rules_engine = _NoRules()

        # Minimal record
        from ubp_critpt_sovereign_v3 import CritPtRecord
        rec = CritPtRecord(
            problem_id="T_main",
            problem_description="compute gcd(54,24)",
            code_template="def f():\n    \"\"\"r: float\"\"\"\n    return 0\n",
        )
        with tempfile.TemporaryDirectory() as d:
            out_dir = Path(d)
            result = runner.run_one(rec, out_dir)
            written = list(out_dir.glob("*.py"))
            self.assertEqual(len(written), 1)
            self.assertIn("problem_id", result)
            self.assertIn("method",      result)


if __name__ == "__main__":
    unittest.main(verbosity=2)
