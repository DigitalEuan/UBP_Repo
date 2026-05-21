import micropip
await micropip.install("sympy")
import sympy as sp
import json
import hashlib
import math
from datetime import datetime
from fractions import Fraction
from ubp_unified_v5 import GOLAY_ENGINE, LEECH_ENGINE
from ubp_tgic_engine import TGICExactEngine, OffBit

# Ensure SymPy is available for the 'Skill' layer
try:
    import sympy as sp
    from sympy import symbols, diff, integrate, exp, pi, I, sin, cos, limit
    x, t = symbols('x t')
    SYMPY_READY = True
except ImportError:
    SYMPY_READY = False

def to_gray(n: int) -> list:
    """Converts integer to 24-bit Gray Code."""
    gray = int(n) ^ (int(n) >> 1)
    return [(gray >> i) & 1 for i in range(23, -1, -1)]

def audit_value(val):
    """Generates the UBP Fingerprint for any value (numeric or symbolic)."""
    # If it's a number, use Gray Code; if symbolic, use Hash
    try:
        n = abs(int(float(val))) & 0xFFFFFF
        vec = to_gray(n)
    except:
        h = int(hashlib.sha256(str(val).encode()).hexdigest(), 16)
        vec = [(h >> i) & 1 for i in range(23, -1, -1)]
    
    decoded, _, _ = GOLAY_ENGINE.decode(vec)
    snapped = GOLAY_ENGINE.encode(decoded)
    tax = float(LEECH_ENGINE.calculate_symmetry_tax(snapped))
    nrci = float(Fraction(10, 1) / (Fraction(10, 1) + Fraction(str(tax))))
    return {"nrci": round(nrci, 4), "sw": sum(snapped), "vector": snapped}

def run_complex_master():
    print("--- UBP COMPLEX MATHEMATICS MASTER-BRIDGE ---")
    if not SYMPY_READY:
        print("SymPy not found. Aborting.")
        return

    # 1. DEFINE COMPLEX MISSIONS
    missions = [
        {
            "id": "CALC_DIFF_001",
            "directive": "Find the derivative of sin(x^2) at x=pi.",
            "expr": diff(sin(x**2), x).subs(x, pi)
        },
        {
            "id": "CALC_INT_001",
            "directive": "Integrate e^(-x) from 0 to infinity.",
            "expr": integrate(exp(-x), (x, 0, sp.oo))
        },
        {
            "id": "COMPLEX_ROOT_001",
            "directive": "Find the principal square root of -16i.",
            "expr": sp.sqrt(-16*I)
        }
    ]

    results = []
    spheres = []

    for m in missions:
        print(f"\nProcessing: {m['directive']}")
        
        # A. Solve via Skill
        ans = m['expr']
        ans_eval = ans.evalf()
        print(f"  [Skill] Result: {ans} (≈ {ans_eval})")

        # B. Audit via Substrate
        fp = audit_value(ans_eval)
        print(f"  [Audit] NRCI: {fp['nrci']} | Weight: {fp['sw']}")

        # C. Prepare for Visualization
        # Map the 24-bit vector to 3D space
        v = fp['vector']
        pos = [(sum(v[0:8])-4)*2, (sum(v[8:16])-4)*2, (sum(v[16:24])-4)*2]
        spheres.append({
            "x": pos[0], "y": pos[1], "z": pos[2],
            "r": fp['nrci'] * 1.5,
            "color": "#00ffff" if fp['nrci'] > 0.7 else "#ff00ff",
            "label": m['id']
        })

        results.append({
            "ubp_id": f"SOVEREIGN_{m['id']}",
            "directive": m['directive'],
            "result": str(ans),
            "nrci_fingerprint": fp['nrci'],
            "status": "MANIFESTED",
            "timestamp": datetime.now().isoformat()
        })

    # 2. ANCHOR TO MEMORY
    kb_path = "ubp_learned_kb.json"
    try:
        with open(kb_path, "r") as f:
            kb = json.load(f)
            if isinstance(kb, list): kb = {item['ubp_id']: item for item in kb}
    except: kb = {}

    for r in results:
        kb[r['ubp_id']] = r

    with open(kb_path, "w") as f:
        json.dump(kb, f, indent=2)

    # 3. GENERATE 3D MANIFOLD MAP
    with open('scene_3d.json', 'w') as f:
        json.dump({"spheres": spheres}, f)

    print(f"\n✅ Master Bridge Complete. {len(results)} complex truths anchored.")
    print("Check 'Visual' tab for the Complex Manifold Map.")

if __name__ == "__main__":
    run_complex_master()