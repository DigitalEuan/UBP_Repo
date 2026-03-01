"""
================================================================================
UBP-Py v2.0 (Standard) - NATIVE GEOMETRIC INTERPRETER
================================================================================

This is the runnable entrypoint for the UBP-Py v2 runtime.

Two execution modes:
1) Python API mode: construct UBPPyVM and call methods.
2) UBP-Py Language mode: provide a .ubp program file and execute it.

Strict rules:
- Internal math is Fraction/int only.
- Golay vectors are always snapped to valid codewords.
- Every state transition is written into a deterministic trace.

Outputs (default names):
- ubp_py_lattice.json  : persistent append-only lattice store
- ubp_py_trace.json    : deterministic step-by-step execution trace
- ubp_py_env.json      : exported environment snapshot
- scene_3d.json        : Three.js bridge (floats allowed for rendering only)

Author: Euan & UBP Research Cortex (assistant extension)
Date: 24 Feb 2026 (UTC)
================================================================================
"""

from __future__ import annotations

import argparse
from fractions import Fraction

from ubp_py_runtime import UBPPyVM
from ubp_py_lang import execute_program, load_program_file
from ubp_viz import save_scene_3d


def run_demo(vm: UBPPyVM) -> None:
    """Demonstration of VM usage without the text language."""

    print("--- INITIALIZING UBP-PY v2.0 STANDARD (DEMO) ---")

    vm.let("START_VAL", "1/1", tier=0, category="QUANTITY")
    vm.spiral("START_VAL", iterations=4, transform_name="INC", label_prefix="START_VAL")
    vm.reflex(threshold=Fraction(7, 10))

    vm.commit()
    vm.export_trace("ubp_py_trace.json")
    vm.export_env("ubp_py_env.json")

    scene = vm.to_scene_3d()
    save_scene_3d(scene, filename="scene_3d.json")


def main() -> None:
    ap = argparse.ArgumentParser(prog="ubp_py_v2_standard")
    ap.add_argument("--program", type=str, default=None, help="Path to .ubp text program")
    ap.add_argument("--lattice", type=str, default="ubp_py_lattice.json")
    ap.add_argument("--trace", type=str, default="ubp_py_trace.json")
    ap.add_argument("--env", type=str, default="ubp_py_env.json")
    ap.add_argument("--scene", type=str, default="scene_3d.json")
    args = ap.parse_args()

    vm = UBPPyVM(lattice_path=args.lattice, trace_path=args.trace, fom_index_path="ubp_py_fom_index.json")

    if args.program is None:
        run_demo(vm)
        return

    text = load_program_file(args.program)
    report = execute_program(vm, text, scene_path=args.scene, default_trace_path=args.trace)

    vm.commit()
    vm.export_trace(args.trace)
    vm.export_env(args.env)
    save_scene_3d(vm.to_scene_3d(), filename=args.scene)

    print("--- UBP-Py Program Complete ---")
    print("final_label:", report.get("final_label"))
    print("env_labels:", report.get("env_labels"))
    print("lattice_count:", report.get("lattice_count"))
    print("trace:", args.trace)
    print("env:", args.env)
    print("scene:", args.scene)


if __name__ == "__main__":
    main()
