# ══════════════════════════════════════════════════════════════════════════════
# §09  TOOLS LAYER — ANALYTICAL ENGINE (v3.7.6 Hardened)
# ══════════════════════════════════════════════════════════════════════════════
from __future__ import annotations
import re
import math
from typing import List, Dict, Optional, Tuple, Any

# Attempt to load SymPy for symbolic logic
try:
    import sympy as sp
    _HAS_SYMPY = True
except ImportError:
    _HAS_SYMPY = False

# IMPORT NUMBER WORDS FOR GROUNDING
from GLM04_number_vocab import NUMBER_WORDS

# ── 1. REGEX PATTERNS (The Detectors) ──────────────────────────────────
_GCD_RE       = re.compile(r'gcd\s*\(\s*(\d+)\s*,\s*(\d+)\s*\)', re.I)
_LCM_RE       = re.compile(r'lcm\s*\(\s*(\d+)\s*,\s*(\d+)\s*\)', re.I)
_SQRT_RE      = re.compile(r'(?:sqrt|√)\s*\(\s*(\d+(?:\.\d+)?)\s*\)', re.I)
_FACTORIAL_RE = re.compile(r'(\d+)\s*!', re.I)
_ARITH_RE     = re.compile(r'(\d+(?:\.\d+)?)\s*([+\-*/×÷])\s*(\d+(?:\.\d+)?)')

# Symbolic Patterns (v3.7)
_DIFF_RE      = re.compile(r'(?:differentiate|derivative of|d/dx)\s+(.+?)(?:\s+with respect to\s+(\w+))?(?:[\?\.]|$)', re.I)
_SOLVE_RE      = re.compile(r'solve\s+(.+?)(?:\s+for\s+(\w+))?(?:[\?\.]|$)', re.I)

# ── 2. NUMERIC DETECTION & EVALUATION ──────────────────────────────────
def detect_compute(query: str) -> Optional[Dict[str, Any]]:
    """Detects if a query contains a computable numeric expression."""
    q = query.strip().replace('`', '')
    if len(q) > 500: return None

    m = _GCD_RE.search(q)
    if m: return {"kind":"gcd", "expr":f"gcd({m.group(1)},{m.group(2)})", "operands":[int(m.group(1)), int(m.group(2))]}
    
    m = _SQRT_RE.search(q)
    if m: return {"kind":"sqrt", "expr":f"sqrt({m.group(1)})", "operands":[float(m.group(1))]}
    
    m = _ARITH_RE.search(q)
    if m:
        op_map = {"×":"*", "÷":"/", "+":"+", "-":"-", "*":"*", "/":"/"}
        return {"kind":"arith", "expr":f"{m.group(1)}{op_map[m.group(2)]}{m.group(3)}", "operands":[float(m.group(1)), m.group(2), float(m.group(3))]}
    
    return None

def evaluate_numeric(comp: Dict[str, Any]) -> Dict[str, Any]:
    """Evaluates a detected numeric computation."""
    if not _HAS_SYMPY: return {"value": None, "error": "SymPy not installed", "exact": "N/A", "approx": 0.0}
    try:
        val = sp.sympify(comp["expr"])
        approx = float(val.evalf())
        return {"value": val, "exact": str(val), "approx": approx}
    except Exception as e:
        return {"value": None, "error": str(e), "exact": "Error", "approx": 0.0}

# ── 3. SYMBOLIC DETECTION & EVALUATION ─────────────────────────────────
def detect_symbolic(query: str) -> Optional[Dict[str, Any]]:
    """Detects if a query contains a symbolic math operation."""
    if not _HAS_SYMPY: return None
    q = query.strip().replace('`', '')

    m = _DIFF_RE.search(q)
    if m:
        return {"kind":"differentiate", "expr": m.group(1).strip(), "var": m.group(2) or "x"}
    
    m = _SOLVE_RE.search(q)
    if m:
        return {"kind":"solve", "expr": m.group(1).strip(), "var": m.group(2) or "x"}
    
    return None

def evaluate_symbolic(comp: Dict[str, Any]) -> Dict[str, Any]:
    """Evaluates a detected symbolic operation."""
    if not _HAS_SYMPY: return {"value": None, "error": "SymPy not installed", "exact": "N/A"}
    try:
        x = sp.Symbol(comp["var"])
        # Pre-process expression for SymPy
        clean_expr = comp["expr"].replace('^', '**')
        
        if comp["kind"] == "differentiate":
            expr = sp.sympify(clean_expr)
            result = sp.diff(expr, x)
        elif comp["kind"] == "solve":
            if '=' in clean_expr:
                parts = clean_expr.split('=')
                eq = sp.Eq(sp.sympify(parts[0].strip()), sp.sympify(parts[1].strip()))
                result = sp.solve(eq, x)
            else:
                expr = sp.sympify(clean_expr)
                result = sp.solve(expr, x)
        else:
            return {"value": None, "error": "Unknown symbolic kind", "exact": "N/A"}
            
        return {"value": result, "exact": str(result)}
    except Exception as e:
        return {"value": None, "error": str(e), "exact": "Error"}

# ── 4. GROUNDING (Connecting Math to the Substrate) ────────────────────
def ground_result(approx: float, vocab: Any) -> Optional[Tuple[str, Any]]:
    """Attempts to snap a numeric result to a known number-word in the vocab."""
    try:
        if abs(approx - round(approx)) < 1e-7:
            n = int(round(approx))
            if n in NUMBER_WORDS:
                word = NUMBER_WORDS[n]
                target_dict = vocab.words if hasattr(vocab, 'words') else vocab
                if word in target_dict:
                    return (word, target_dict[word])
    except: pass
    return None


def _normalize_math(s: str) -> str:
    """Surgically fix implicit multiplication: 5x -> 5*x, 21n -> 21*n"""
    s = s.replace('^', '**')
    # Insert * between a number and a letter
    s = re.sub(r'(\d)([a-zA-Z])', r'\1*\2', s)
    return s

def evaluate_numeric(comp: Dict[str, Any]) -> Dict[str, Any]:
    if not _HAS_SYMPY: return {"value": None, "error": "SymPy not installed", "exact": "N/A", "approx": 0.0}
    try:
        # Normalize before sympifying
        clean_expr = _normalize_math(comp["expr"])
        val = sp.sympify(clean_expr)
        approx = float(val.evalf())
        return {"value": val, "exact": str(val), "approx": approx}
    except Exception as e:
        return {"value": None, "error": str(e), "exact": "Error", "approx": 0.0}

def evaluate_symbolic(comp: Dict[str, Any]) -> Dict[str, Any]:
    if not _HAS_SYMPY: return {"value": None, "error": "SymPy not installed", "exact": "N/A"}
    try:
        x = sp.Symbol(comp["var"])
        clean_expr = _normalize_math(comp["expr"])
        
        if comp["kind"] == "differentiate":
            result = sp.diff(sp.sympify(clean_expr), x)
        elif comp["kind"] == "solve":
            if '=' in clean_expr:
                parts = clean_expr.split('=')
                eq = sp.Eq(sp.sympify(_normalize_math(parts[0])), sp.sympify(_normalize_math(parts[1])))
                result = sp.solve(eq, x)
            else:
                result = sp.solve(sp.sympify(clean_expr), x)
        else: return {"value": None, "error": "Unknown kind", "exact": "N/A"}
        return {"value": result, "exact": str(result)}
    except Exception as e:
        return {"value": None, "error": str(e), "exact": f"Error: {e}"}

# ── 5. ISOLATION TEST ──────────────────────────────────────────────────
if __name__ == "__main__":
    print("=== Testing Module 09: Tools Layer ===")
    
    # Test Numeric
    q1 = "What is gcd(54, 24)?"
    comp1 = detect_compute(q1)
    if comp1:
        res1 = evaluate_numeric(comp1)
        print(f"✅ Numeric: {comp1['expr']} = {res1.get('exact', 'Error')} (Approx: {res1.get('approx', 0)})")
    
    # Test Symbolic
    if _HAS_SYMPY:
        q2 = "differentiate x**2 + 5*x"
        comp2 = detect_symbolic(q2)
        if comp2:
            res2 = evaluate_symbolic(comp2)
            print(f"✅ Symbolic: d/dx({comp2['expr']}) = {res2.get('exact', 'Error')}")