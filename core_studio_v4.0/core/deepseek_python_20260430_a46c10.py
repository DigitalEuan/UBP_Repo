"""
================================================================================
UBP SUBSTRATE BACKEND — Flask REST API for core.py v6.1
================================================================================
Wires the real Golay [24,12,8] + Leech Λ₂₄ engines into a lightweight HTTP API
so the HTML calculator can use 50-term π, exact Fraction arithmetic, and
the true Golay decoder instead of the JavaScript stub.

Usage:
    pip install flask flask-cors
    python ubp_backend.py          # starts on http://localhost:5099

Author: Euan R A Craig, New Zealand
Date:   30 April 2026
================================================================================
"""

import json
import sys
import os
from pathlib import Path
from fractions import Fraction

# ── Ensure we can find core.py ───────────────────────────────────────────────
# Adjust this path if core.py lives elsewhere:
CORE_PATH = Path(__file__).parent / "core.py"
if not CORE_PATH.exists():
    # Try the GitHub repo structure
    CORE_PATH = Path(__file__).parent / "core_studio_v4.0" / "core" / "core.py"

if CORE_PATH.exists():
    sys.path.insert(0, str(CORE_PATH.parent))
    print(f"[UBP Backend] Loading core from: {CORE_PATH}")
else:
    print("[UBP Backend] WARNING: core.py not found. Falling back to stub.")
    # We'll handle the fallback below

try:
    from core import GOLAY_ENGINE, LEECH_ENGINE, UBPUltimateSubstrate, BinaryLinearAlgebra
    REAL_ENGINE = True
    print("[UBP Backend] ✓ Real Golay/Leech engines loaded.")
    print(f"            Golay codewords: {len(GOLAY_ENGINE.get_all_codewords())}")
    print(f"            Octads:           {len(GOLAY_ENGINE.get_octads())}")
    constants = UBPUltimateSubstrate.get_constants(50)
    print(f"            π (50-term):      {float(constants['PI']):.15f}")
    print(f"            Y_CONST:          {float(constants['Y_CONST']):.15f}")
except ImportError as e:
    REAL_ENGINE = False
    print(f"[UBP Backend] Could not import core.py: {e}")
    print("            Running in STUB mode (JS-level accuracy).")

from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Allow the HTML page (any origin) to call us

# ══════════════════════════════════════════════════════════════════════════════
# HELPERS
# ══════════════════════════════════════════════════════════════════════════════

CODEWORD_WEIGHTS = {0, 8, 12, 16, 24}

def to_gray_code_24(n: int) -> list:
    """Gray-code an integer into 24 bits."""
    val = abs(int(n)) & 0xFFFFFF
    gray = val ^ (val >> 1)
    return [(gray >> i) & 1 for i in range(23, -1, -1)]

def classify_lattice(sw: int) -> dict:
    """Classify a Hamming weight onto the Golay/Leech lattice."""
    return {
        0:  {"type": "Identity",   "color": "#e0e0e0"},
        8:  {"type": "Octad",      "color": "#00bcd4"},
        12: {"type": "Dodecad",    "color": "#ffd740"},
        16: {"type": "Hexadecad",  "color": "#b388ff"},
        24: {"type": "Universe",   "color": "#ffffff"},
    }.get(sw, {"type": "Off-lattice", "color": "#ff5252"})

def compute_nrci(codeword_24: list) -> float:
    """NRCI = 10 / (10 + tax), where tax = hw * Y_const + norm_sq/8."""
    if REAL_ENGINE:
        point = [int(x) for x in codeword_24]
        tax = LEECH_ENGINE.calculate_symmetry_tax(point)
        nrci = Fraction(10, 1) / (Fraction(10, 1) + tax)
        return float(nrci)
    else:
        hw = sum(codeword_24)
        Y_const = 0.2646750901311604  # stub fallback
        tax = hw * Y_const + hw / 8.0
        return round(10.0 / (10.0 + tax), 6)

def fingerprint_number(n) -> dict:
    """Full UBP fingerprint for a number."""
    gray = to_gray_code_24(n)
    if REAL_ENGINE:
        snapped, meta = GOLAY_ENGINE.snap_to_codeword(gray)
        sw = BinaryLinearAlgebra.hamming_weight(snapped)
        nrci = compute_nrci(snapped)
        return {
            "value": n,
            "gray_bits": gray,
            "snapped": snapped,
            "hamming_weight": sw,
            "nrci": round(nrci, 6),
            "lattice": classify_lattice(sw),
            "on_lattice": sw in CODEWORD_WEIGHTS,
            "syndrome_weight": meta["syndrome_weight"],
            "snap_distance": meta["anchor_distance"],
            "correctable": meta["correctable"],
            "engine": "REAL (50-term π, Golay [24,12,8])"
        }
    else:
        hw = sum(gray)
        snapped = gray  # stub: no real decode
        nrci = compute_nrci(gray)
        return {
            "value": n,
            "gray_bits": gray,
            "snapped": snapped,
            "hamming_weight": hw,
            "nrci": round(nrci, 6),
            "lattice": classify_lattice(hw),
            "on_lattice": hw in CODEWORD_WEIGHTS,
            "syndrome_weight": 0,
            "snap_distance": 0,
            "correctable": True,
            "engine": "STUB (no core.py loaded)"
        }


# ══════════════════════════════════════════════════════════════════════════════
# API ENDPOINTS
# ══════════════════════════════════════════════════════════════════════════════

@app.route("/api/status", methods=["GET"])
def status():
    """Health check + engine info."""
    return jsonify({
        "status": "online",
        "engine": "REAL" if REAL_ENGINE else "STUB",
        "golay_codewords": 4096,
        "golay_octads": 759,
        "leech_kissing_number": 196560,
        "precision": "50-term π (Fraction-based, float-free)" if REAL_ENGINE else "JS stub",
    })

@app.route("/api/fingerprint", methods=["POST"])
def fingerprint():
    """Fingerprint a single number."""
    data = request.get_json(force=True)
    n = data.get("value", 0)
    try:
        n = int(float(str(n)))
    except (ValueError, TypeError):
        return jsonify({"error": "Invalid number"}), 400
    return jsonify(fingerprint_number(n))

@app.route("/api/fingerprint-batch", methods=["POST"])
def fingerprint_batch():
    """Fingerprint multiple numbers at once."""
    data = request.get_json(force=True)
    values = data.get("values", [])
    results = []
    for v in values:
        try:
            n = int(float(str(v)))
            results.append(fingerprint_number(n))
        except (ValueError, TypeError):
            results.append({"error": f"Invalid: {v}"})
    return jsonify({"results": results})

@app.route("/api/compute", methods=["POST"])
def compute():
    """
    Perform a binary operation and fingerprint the result.
    Supported ops: +, -, *, /, mod, pow, gcd, lcm, comb, fact, isprime, fib, sqrt
    """
    data = request.get_json(force=True)
    op = data.get("op", "+")
    a = data.get("a", 0)
    b = data.get("b", 0)

    try:
        a = float(str(a)) if a is not None else 0
        b = float(str(b)) if b is not None else 0
    except (ValueError, TypeError):
        return jsonify({"error": "Invalid operands"}), 400

    import math
    result = None
    error = None
    try:
        if op == "+":   result = a + b
        elif op == "-": result = a - b
        elif op == "*": result = a * b
        elif op == "/": result = a / b if b != 0 else None
        elif op == "mod":
            result = int(a) % int(b) if int(b) != 0 else None
        elif op == "pow": result = math.pow(a, b)
        elif op == "gcd":
            result = math.gcd(int(abs(a)), int(abs(b)))
        elif op == "lcm":
            result = abs(int(a) * int(b)) // math.gcd(int(abs(a)), int(abs(b))) if a and b else 0
        elif op == "comb":
            result = math.comb(int(abs(a)), int(abs(b)))
        elif op == "fact":
            result = math.factorial(int(abs(a)))
        elif op == "isprime":
            n = int(abs(a))
            if n < 2: result = "No (composite)"
            else:
                for i in range(2, int(math.sqrt(n)) + 1):
                    if n % i == 0:
                        result = "No (composite)"
                        break
                else:
                    result = "Yes (prime)"
        elif op == "fib":
            n = int(abs(a))
            x, y = 0, 1
            for _ in range(n):
                x, y = y, x + y
            result = x
        elif op == "sqrt":
            result = math.sqrt(a) if a >= 0 else None
        else:
            error = f"Unknown op: {op}"
    except Exception as e:
        error = str(e)

    if error:
        return jsonify({"error": error}), 400
    if result is None:
        return jsonify({"error": "Invalid operation (e.g. division by zero)"}), 400

    # Fingerprint the result
    fp = fingerprint_number(result) if isinstance(result, (int, float)) else {
        "value": str(result),
        "engine": "REAL" if REAL_ENGINE else "STUB",
        "note": "Non-numeric result, no fingerprint"
    }

    # Also fingerprint both operands
    fp_a = fingerprint_number(int(a)) if isinstance(a, (int, float)) and a == int(a) else None
    fp_b = fingerprint_number(int(b)) if isinstance(b, (int, float)) and b == int(b) else None

    return jsonify({
        "operation": op,
        "a": a,
        "b": b,
        "result": result if isinstance(result, (int, float)) else str(result),
        "fingerprint": fp,
        "fingerprint_a": fp_a,
        "fingerprint_b": fp_b,
        "trace": f"{a} {op} {b} → {result}",
    })

@app.route("/api/constants", methods=["GET"])
def get_constants():
    """Return the UBP constants (exact Fractions as floats)."""
    if REAL_ENGINE:
        c = UBPUltimateSubstrate.get_constants(50)
        return jsonify({
            "PI": float(c["PI"]),
            "Y_INV": float(c["Y_INV"]),
            "Y": float(c["Y"]),
            "Y_CONST": float(c["Y_CONST"]),
            "precision_terms": c["precision_terms"],
            "engine": "REAL (50-term π)"
        })
    return jsonify({
        "PI": 3.141592653589793,
        "Y_INV": 3.778302513177149,
        "Y": 0.2646750901311604,
        "Y_CONST": 0.2234304062047951,
        "precision_terms": "JS stub (math.pi)",
        "engine": "STUB"
    })


# ══════════════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("=" * 65)
    print(" UBP SUBSTRATE BACKEND")
    print(f" Engine: {'REAL Golay/Leech' if REAL_ENGINE else 'STUB (JS fallback)'}")
    print(" Endpoints:")
    print("   GET  /api/status       — engine health")
    print("   POST /api/fingerprint   — fingerprint a number")
    print("   POST /api/fingerprint-batch — fingerprint many numbers")
    print("   POST /api/compute       — compute + fingerprint result")
    print("   GET  /api/constants     — UBP fundamental constants")
    print("=" * 65)
    app.run(host="0.0.0.0", port=5099, debug=True)