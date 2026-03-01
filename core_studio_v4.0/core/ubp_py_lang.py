import shlex
from ubp_py_runtime import UBPPyVM
from ubp_viz import save_scene_3d

def execute_program(vm, text):
    lines = [l.strip() for l in text.splitlines() if l.strip() and not l.startswith("#")]
    
    for line in lines:
        tokens = shlex.split(line)
        if not tokens: continue
        op = tokens[0].upper()

        try:
            if op == "LET":
                # LET <label> <value> [TIER <n>] [CAT <cat>]
                tier = 0
                cat = "QUANTITY"
                if "TIER" in tokens: tier = int(tokens[tokens.index("TIER")+1])
                if "CAT" in tokens: cat = tokens[tokens.index("CAT")+1]
                vm.let(tokens[1], tokens[2], tier, cat)
                
            elif op == "IMPORT":
                # IMPORT <ubp_id> [AS <alias>]
                alias = None
                if "AS" in tokens: alias = tokens[tokens.index("AS")+1]
                vm.import_atom(tokens[1], alias)

            elif op == "SYNTH":
                # SYNTH <out> FROM <recipe>
                # Example: SYNTH Water FROM "2xH + 1xO"
                recipe_idx = tokens.index("FROM") + 1
                recipe = " ".join(tokens[recipe_idx:])
                vm.synth(tokens[1], recipe)

            elif op == "AUDIT":
                label = tokens[1]
                if label in vm.env:
                    a = vm.env[label]
                    print(f"--- AUDIT: {a.label} ---")
                    print(f"  Tax:  {float(a.tax):.4f}")
                    print(f"  NRCI: {float(a.nrci):.4f}")
                    print(f"  Tilt: {a.tilt:.2f}°")
                    print(f"  Vec:  {a.vector}")

            elif op == "VISUALIZE":
                save_scene_3d(vm.to_scene_3d())
                print("[Visual] Scene updated.")

        except Exception as e:
            print(f"Error executing '{line}': {e}")

    return {"status": "done"}