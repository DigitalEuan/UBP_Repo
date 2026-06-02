"""
================================================================================
GLM RUNTIME v1.0 — Single Entrypoint for the Geometric Language Machine
================================================================================
Purpose
-------
Boot the entire GLM stack in one call.  Two usage modes:

    >>> from glm_runtime import GLMRuntime
    >>> rt = GLMRuntime()                       # boots everything once

    # Mode A — natural-language chat (deterministic, grounded, KB-anchored)
    >>> rt.chat("What is the beta function of QED?")
    'The beta function is ...'

    # Mode B — full CritPt benchmark or single MathNet problem
    >>> rt.solve_critpt(limit=5)
    [{'problem_id': 'Challenge_1_main', ...}, ...]
    >>> rt.solve_mathnet("gcd(54, 24)")
    AnswerCandidate(values=['6.0'], method='NoiseALU/native', ...)

Boot order (matters)
--------------------
1.  Import `glm_grammar_patch`   -> monkey-patches `GLMDialogueEngine`
                                    (v2.0 disambiguation rules).
2.  Build `GLMSemanticEngine`    -> v3.1 with lexer + frames + CRG + pack.
3.  Construct `UBPSovereignSolver` (auto-runs `critpt_glm_patch` at import).
4.  Construct `SovereigntyRunner` for CritPt batch runs.

Design notes
------------
*   No randomness anywhere — every step is deterministic.
*   The runtime is lazy where it can be: heavy KB files are only opened
    when the corresponding subsystem is first used.
*   `chat()` always returns a string; the full structured turn is
    available via `last_turn()`.
================================================================================
"""

from __future__ import annotations
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

_HERE = Path(__file__).resolve().parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))


# ── 1. grammar patch (MUST come before any engine construction) ────────────
import glm_grammar_patch  # noqa: F401  (side-effect import)


# ── 2. engines & solver ────────────────────────────────────────────────────
try:
    from glm_engine_v31 import create_semantic_engine, GLMSemanticEngine  # noqa: F401
    _HAS_V31 = True
except Exception as _e:                                                      # pragma: no cover
    create_semantic_engine = None
    GLMSemanticEngine = None
    _HAS_V31 = False
    print(f"[GLMRuntime] v3.1 engine unavailable ({_e}); using v3.0")

from glm_engine import create_engine as _create_v30_engine, GLMDialogueEngine  # noqa: F401

from ubp_critpt_sovereign_v3 import (
    SovereigntyRunner, UBPSovereignSolver, GLMRulesEngine,
    parse_template, load_critpt, lattice_snap_value,
    NRCI_PHASE_LOCK,
)


# ════════════════════════════════════════════════════════════════════════════════
# GLM RUNTIME
# ════════════════════════════════════════════════════════════════════════════════

class GLMRuntime:
    """High-level facade that owns one configured GLM engine, one Sovereign
    solver, and (lazily) one SovereigntyRunner.  Use it instead of wiring
    the individual pieces yourself."""

    def __init__(self,
                 system_kb_path: str = "ubp_system_kb.json",
                 lang_kb_path:   str = "ubp_lang_kb_combined_v4.json",
                 use_v31: bool = True,
                 boot_runner: bool = False):
        self.system_kb_path = system_kb_path
        self.lang_kb_path   = lang_kb_path

        # ── GLM ENGINE ─────────────────────────────────────────────────────
        if use_v31 and _HAS_V31:
            print("[GLMRuntime] booting GLM v3.1 (semantic edition) ...")
            self.glm, self._glm_report = create_semantic_engine(
                system_kb_path, lang_kb_path)
            self._engine_version = "v3.1"
        else:
            print("[GLMRuntime] booting GLM v3.0 (dialogue) ...")
            self.glm = _create_v30_engine(system_kb_path, lang_kb_path)
            self._glm_report = None
            self._engine_version = "v3.0"

        # ── RULES (text normalisation) ────────────────────────────────────
        self.rules = GLMRulesEngine(lang_kb_path)

        # ── SOLVER (lazy run-time pipeline for CritPt / MathNet) ──────────
        self.solver = UBPSovereignSolver()

        # ── RUNNER (only when needed) ─────────────────────────────────────
        self._runner: Optional[SovereigntyRunner] = None
        if boot_runner:
            self._runner = SovereigntyRunner(
                system_kb_path=system_kb_path,
                lang_kb_path=lang_kb_path,
                use_v31=use_v31,
            )

        # State.
        self._last_turn: Optional[Any] = None
        print(f"[GLMRuntime] ready ({self._engine_version}).")

    # ── chat / dialogue ────────────────────────────────────────────────────

    def chat(self, query: str, max_depth: int = 3) -> str:
        """One natural-language turn.  Returns the response text only;
        the structured turn is cached on `self._last_turn`."""
        clean = self.rules.preprocess(query)
        if hasattr(self.glm, "respond_semantic"):
            turn = self.glm.respond_semantic(clean, max_depth=max_depth)
        else:
            turn = self.glm.respond(clean, max_depth=max_depth)
        self._last_turn = turn
        return getattr(turn, "response", "")

    def last_turn(self) -> Optional[Any]:
        """Return the full DialogueTurn / SemanticTurn from the most recent
        `chat()` call (or None)."""
        return self._last_turn

    def explain(self, a: str, b: str) -> str:
        """If the engine exposes a CRG-aware relation explainer, use it.
        Otherwise return a one-line geometric description."""
        if hasattr(self.glm, "explain_relation"):
            return self.glm.explain_relation(a, b)
        return f"(v3.0 engine has no explain_relation; lattice distance only)"

    # ── single-problem solving (deterministic MathNet) ─────────────────────

    def solve_mathnet(self, problem_text: str):
        """Solve a single MathNet-style problem deterministically.  Returns
        the AnswerCandidate."""
        clean = self.rules.preprocess(problem_text)
        # Synthesise a minimal TemplateSpec — solve() only needs return_spec.
        from ubp_critpt_sovereign_v3 import ReturnSpec, TemplateSpec
        spec = TemplateSpec(
            func_name="answer", in_params=[], docstring="",
            return_spec=ReturnSpec(["result"], ["float"], 1),
            pre_imports="", raw_template="def answer():\n    return 0",
        )
        # Provide a GLM turn so the seeded route is reachable.
        if hasattr(self.glm, "respond_semantic"):
            turn = self.glm.respond_semantic(clean, max_depth=2)
        else:
            turn = self.glm.respond(clean, max_depth=2)
        return self.solver.solve(clean, spec, turn)

    # ── CritPt batch run ───────────────────────────────────────────────────

    def solve_critpt(self,
                     critpt_path: str = "critpt.json",
                     out_dir:     str = "out_sovereign",
                     limit:       int = 0) -> List[Dict[str, Any]]:
        """Run the full (or first-N) CritPt benchmark.  Returns the per-record
        result dicts produced by the SovereigntyRunner."""
        if self._runner is None:
            self._runner = SovereigntyRunner(
                system_kb_path=self.system_kb_path,
                lang_kb_path=self.lang_kb_path,
                use_v31=(self._engine_version == "v3.1"),
            )
        records = load_critpt(critpt_path)
        if limit:
            records = records[: limit]
        return self._runner.run_all(records, out_dir)

    # ── diagnostics ────────────────────────────────────────────────────────

    def stats(self) -> Dict[str, Any]:
        out: Dict[str, Any] = {
            "engine_version": self._engine_version,
            "glm_report":     self._glm_report,
            "rules_loaded":   len(self.rules.normalization_rules),
        }
        if hasattr(self.glm, "extension_stats"):
            out["extensions"] = self.glm.extension_stats()
        return out


# ── tiny CLI for quick interaction ──────────────────────────────────────────────

def _cli() -> int:
    import argparse
    p = argparse.ArgumentParser(description="GLM runtime CLI")
    sub = p.add_subparsers(dest="cmd")

    p_chat = sub.add_parser("chat", help="single natural-language query")
    p_chat.add_argument("query", nargs="+")

    p_explain = sub.add_parser("explain", help="explain relation between two terms")
    p_explain.add_argument("a"); p_explain.add_argument("b")

    p_critpt = sub.add_parser("critpt", help="batch-solve CritPt")
    p_critpt.add_argument("--critpt", default="critpt.json")
    p_critpt.add_argument("--out",    default="out_sovereign")
    p_critpt.add_argument("--limit",  type=int, default=5)

    sub.add_parser("stats", help="dump engine extension stats")

    args = p.parse_args()
    rt = GLMRuntime()

    if args.cmd == "chat":
        print(rt.chat(" ".join(args.query)))
    elif args.cmd == "explain":
        print(rt.explain(args.a, args.b))
    elif args.cmd == "critpt":
        results = rt.solve_critpt(args.critpt, args.out, args.limit)
        print(f"\n{len(results)} records processed -> {args.out}/")
    elif args.cmd == "stats":
        import json
        print(json.dumps(rt.stats(), indent=2, default=str))
    else:
        p.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(_cli())
