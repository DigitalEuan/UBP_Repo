"""
UBP-Py v2.1 (Standard) - Adjusted Threshold
===========================================
LOWERED REFLEX THRESHOLD to 0.6 to allow spiral manifestation.
"""

import argparse
from fractions import Fraction
import os

from ubp_py_runtime import UBPPyVM
from ubp_py_lang import execute_program
from ubp_viz import save_scene_3d

def load_program_file(path):
    if not os.path.exists(path):
        return ""
    with open(path, 'r') as f:
        return f.read()

def run_demo(vm: UBPPyVM) -> None:
    """Demonstration of VM usage without the text language."""
    print("--- INITIALIZING UBP-PY v2.0 STANDARD (DEMO) ---")

    # 1. Create a starting value
    vm.let("START_VAL", "1/1", tier=0, category="QUANTITY")
    
    # 2. Run a spiral growth
    vm.spiral("START_VAL", iterations=4, transform_name="INC", label_prefix="START_VAL")
    
    # 3. Perform a self-healing audit
    # CHANGED: Threshold lowered from 7/10 (0.7) to 6/10 (0.6)
    # This allows the 0.6814 atoms to survive.
    vm.reflex(threshold=Fraction(6, 10))

    # 4. Save results
    vm.commit()
    vm.export_trace(vm.trace_path)
    vm.export_env("ubp_py_env.json")

    # 5. Update Visualization
    scene = vm.to_scene_3d()
    save_scene_3d(scene)
    print("[Visual] Demo scene exported to scene_3d.json")

def main() -> None:
    ap = argparse.ArgumentParser(prog="ubp_py_v2_standard")
    ap.add_argument("--program", type=str, default=None, help="Path to .ubp text program")
    ap.add_argument("--lattice", type=str, default="ubp_py_lattice.json")
    ap.add_argument("--trace", type=str, default="ubp_py_trace.json")
    ap.add_argument("--env", type=str, default="ubp_py_env.json")
    ap.add_argument("--scene", type=str, default="scene_3d.json")
    args = ap.parse_args()

    # Initialize VM
    vm = UBPPyVM(
        lattice_path=args.lattice, 
        trace_path=args.trace, 
        fom_index_path="ubp_py_fom_index.json"
    )

    if args.program is None:
        run_demo(vm)
        return

    # Execute from file
    text = load_program_file(args.program)
    if text:
        report = execute_program(vm, text)
        
        vm.commit()
        vm.export_trace(args.trace)
        vm.export_env(args.env)
        
        save_scene_3d(vm.to_scene_3d())

        print("--- UBP-Py Program Complete ---")
        print(f"Lattice saved to: {args.lattice}")
        print(f"Trace saved to: {args.trace}")
    else:
        print(f"Error: Program file '{args.program}' is empty or not found.")

if __name__ == "__main__":
    main()