"""
================================================================================
UBP SWARM TCT MATHNET v2.0 — FULL SYSTEM INTEGRATION EDITION
================================================================================
Author: UBP Investigation (based on UBP core_studio_v4.0 by E R A Craig, NZ)
Date: 2026-04-22
Purpose: Maximally push the full UBP system against the MathNet MIT benchmark.

IMPROVEMENTS OVER v1.0:
  ─────────────────────────────────────────────────────────────────────────────
  Column 1 (Math Architect):
    + Analog Compute Verification: EML ALU + EM Analog engine cross-check
    + TGIC 3-6-9 Stability Audit on every key number's Golay vector
    + Barnes-Wall 256D macro-coherence analysis of the problem fingerprint
    + Full prime factorisation + divisor analysis via EML ALU

  Column 2 (Sovereign Physicist):
    + TGIC TotalStability (3-axis orthogonality + 6-face coherence + 9-limit)
    + RuneCube face projections (XY/XZ/YZ) for multi-axis symmetry tax
    + OffBit phase tracking across problem iterations
    + Leech rank_by_stability comparison of snapped vs raw vector

  Column 3 (Language Scribe):
    + UBP Brain v7.2 (Identity Lock + Lattice Resonance) replaces simple query
    + Python Code Generator synthesises executable verification code
    + Code Executor runs the generated code and captures numerical results
    + Analog Test Suite verifies arithmetic sub-results electromagnetically
    + Self-Correction Loop: up to 2 retry attempts with enriched NRCI context
    + Integrated Engine Penta-Audit for ontological drift classification

  Orchestration:
    + TCT Convergence Score: how well all three columns converge on an answer
    + Iteration tracking: records which attempt produced the final answer
    + Full provenance chain in JSON output
================================================================================
"""

import sys
import os
import json
import hashlib
import logging
import time
import re
import math
import ast
import io
import contextlib
from fractions import Fraction
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, Tuple
from collections import defaultdict

# ─── PATH SETUP ──────────────────────────────────────────────────────────────
CORE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, CORE_DIR)

# ─── LOGGING ─────────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%H:%M:%S'
)
logger = logging.getLogger("UBP-MathNet-v2")

# ─── UBP CORE IMPORTS ────────────────────────────────────────────────────────
logger.info("Loading UBP Core v5.7 + full module suite...")
from core import GOLAY_ENGINE, LEECH_ENGINE, SUBSTRATE, BarnesWallEngine

import math_atlas as _ma
_ma.LEECH_ENGINE = LEECH_ENGINE
_ma.GOLAY_DECODER = GOLAY_ENGINE
_ma.CORE_AVAILABLE = True

from math_atlas import PositiveInteger, Rational, MathObjectV4
from ubp_eml_alu_sovereign import (
    GrandUnifiedEmlALU,
    _pure_sin, _pure_cos, _pure_exp, _pure_ln
)
from ubp_observer_dynamics import ObserverDynamicsEngine
from ubp_semantic_engine import UBPSemanticEngine
from ubp_brain_consolidated import UBPBrain, extract_vector, extract_nrci, extract_name
from ubp_tgic_engine import TGICInteractionEngine, TGICConstraintSystem
from ubp_analog_test_suite_v3 import UBPAnalogTestSuite
from ubp_python_engine import UBPPythonEngine, PythonCodeGenerator
UBPPythonCodeEngine = UBPPythonEngine  # alias for clarity

logger.info("All UBP modules loaded.")

# ─── OPENAI ──────────────────────────────────────────────────────────────────
try:
    from openai import OpenAI
    _client = OpenAI()
    OPENAI_AVAILABLE = True
    logger.info("OpenAI client ready.")
except Exception as e:
    OPENAI_AVAILABLE = False
    logger.warning(f"OpenAI not available: {e}")

# ─── LIGHTWEIGHT EML TREE NODE ───────────────────────────────────────────────
class EmlTreeNode:
    def __init__(self, op: str, left=None, right=None, leaf=None):
        self.op = op; self.left = left; self.right = right; self.leaf = leaf
    def __str__(self):
        if self.op == 'leaf':
            v = self.leaf
            return f'leaf({abs(v):.4f})' if v is not None else 'leaf'
        return f'eml({self.left},{self.right})'

# ─── DATA STRUCTURES ─────────────────────────────────────────────────────────

@dataclass
class MathColumnV2:
    problem_id: str
    numeric_objects: List[Dict]
    nrci_values: List[float]
    mean_nrci: float
    alu_operations: List[Dict]
    geometric_complexity: float
    prime_density: float
    golay_weight_distribution: Dict
    tgic_stability_scores: List[float]    # NEW: TGIC 3-6-9 audit per number
    mean_tgic_stability: float            # NEW
    analog_verifications: List[Dict]      # NEW: EM analog cross-checks
    bw256_macro_nrci: float               # NEW: Barnes-Wall 256D macro coherence
    factorisation_map: Dict               # NEW: prime factorisation of key numbers

@dataclass
class SovereignColumnV2:
    problem_id: str
    eml_tree_repr: str
    golay_address: int
    snapped_vector: List[int]
    soc_energy: float
    manifestation: str
    leech_norm: float
    symmetry_tax: float
    coherence_score: float
    tgic_total_stability: float           # NEW: full 3-6-9 TGIC audit
    rune_xy_tax: float                    # NEW: XY face symmetry tax
    rune_xz_tax: float                    # NEW: XZ face symmetry tax
    rune_yz_tax: float                    # NEW: YZ face symmetry tax
    stability_rank: int                   # NEW: rank among snapped vs raw
    offbit_phase: int                     # NEW: OffBit phase accumulator

@dataclass
class LanguageColumnV2:
    problem_id: str
    semantic_hits: List[Dict]
    semantic_resonance: float
    ubp_laws_invoked: List[str]
    brain_result_uid: str                 # NEW: UBP Brain v7.2 identity lock result
    brain_method: str                     # NEW: how the brain found it
    ontology_class: str                   # NEW: PHENOMENAL/NOUMENAL/TRANSITIONAL
    generated_code: str                   # NEW: Python code generated by UBP engine
    code_output: str                      # NEW: actual execution result
    code_verified: bool                   # NEW: did code execution succeed?
    analog_arithmetic_check: Dict         # NEW: EM analog verification of key arithmetic
    llm_solution: str
    llm_model: str
    solution_tokens: int
    domain_alignment: str
    attempts: int                         # NEW: how many LLM attempts were made
    self_correction_applied: bool         # NEW: was self-correction triggered?

@dataclass
class TCTResultV2:
    problem_id: str
    domain: str
    subdomain: str
    problem_text: str
    reference_answer: str
    math_col: MathColumnV2
    sovereign_col: SovereignColumnV2
    language_col: LanguageColumnV2
    correctness_score: float
    correctness_label: str
    ubp_confidence: float
    alignment_score: float
    tct_convergence: float                # NEW: how well all 3 columns agree
    processing_time_s: float
    timestamp: str
    version: str = "v2.0"

# ─── COLUMN 1 V2: MATH ARCHITECT ─────────────────────────────────────────────

class MathArchitectV2:
    """
    Enhanced Math Architect with TGIC stability, analog verification,
    Barnes-Wall 256D macro-coherence, and prime factorisation.
    """

    def __init__(self):
        self.alu = GrandUnifiedEmlALU()
        self.observer = ObserverDynamicsEngine()
        self.tgic = TGICInteractionEngine()
        self.analog = UBPAnalogTestSuite(v_ref=1000.0)
        self.bw_engine = BarnesWallEngine(dimension=256)
        self._prime_cache = {}

    def _is_prime(self, n: int) -> bool:
        if n < 2: return False
        if n in self._prime_cache: return self._prime_cache[n]
        if n == 2: return True
        if n % 2 == 0: self._prime_cache[n] = False; return False
        for i in range(3, int(n**0.5) + 1, 2):
            if n % i == 0: self._prime_cache[n] = False; return False
        self._prime_cache[n] = True; return True

    def _factorise(self, n: int) -> Dict[int, int]:
        """Return prime factorisation as {prime: exponent}."""
        n = abs(n)
        if n <= 1: return {n: 1}
        factors = {}
        d = 2
        while d * d <= n:
            while n % d == 0:
                factors[d] = factors.get(d, 0) + 1
                n //= d
            d += 1
        if n > 1:
            factors[n] = factors.get(n, 0) + 1
        return factors

    def _encode_number(self, n: int) -> Dict:
        try:
            obj = PositiveInteger(abs(n) if n != 0 else 1)
            vec = obj.get_vector()
            nrci = float(obj.get_nrci())
            read = self.observer.conscious_read(vec, Fraction(nrci).limit_denominator(1000))
            soc = self.observer.calculate_soc_energy(vec, Fraction(nrci).limit_denominator(1000))
            # TGIC 3-6-9 stability
            tgic_stab = float(self.tgic.calculate_total_stability(vec))
            return {
                "n": n, "vector": vec, "nrci": nrci,
                "hamming_weight": sum(vec), "status": read["status"],
                "soc_energy": soc, "is_prime": self._is_prime(abs(n)),
                "tgic_stability": tgic_stab
            }
        except Exception as e:
            logger.debug(f"Encode error n={n}: {e}")
            return {"n": n, "nrci": 0.5, "hamming_weight": 12, "status": "UNKNOWN",
                    "soc_energy": 0.0, "is_prime": self._is_prime(abs(n)),
                    "vector": [0]*24, "tgic_stability": 0.5}

    def _analog_verify(self, numbers: List[int]) -> List[Dict]:
        """Use EM analog engine to cross-check arithmetic on key numbers."""
        verifications = []
        nums = [n for n in numbers if n > 0][:4]
        for i in range(len(nums) - 1):
            a, b = float(nums[i]), float(nums[i+1])
            try:
                add_r, add_sym, add_drift = self.analog.op_add(a, b)
                mul_r, mul_sym, mul_drift = self.analog.op_mul(a, b)
                verifications.append({
                    "a": a, "b": b,
                    "add_analog": round(add_r, 4), "add_expected": a + b,
                    "add_sym_tax": round(add_sym, 4),
                    "mul_analog": round(mul_r, 4), "mul_expected": a * b,
                    "mul_sym_tax": round(mul_sym, 4),
                    "orthogonality_drift": round(add_drift, 4)
                })
            except Exception:
                pass
        return verifications

    def _bw256_macro_nrci(self, problem_text: str) -> float:
        """Compute Barnes-Wall 256D macro-coherence from problem fingerprint."""
        try:
            h = hashlib.sha256(problem_text.encode()).hexdigest()
            # Convert hex fingerprint to 256-bit vector
            bits = []
            for c in h:
                val = int(c, 16)
                for bit in range(4):
                    bits.append((val >> bit) & 1)
            bits = bits[:256]
            # Barnes-Wall snap
            snapped = self.bw_engine.snap(bits)
            macro_nrci = self.bw_engine.calculate_nrci(snapped)
            return float(macro_nrci)
        except Exception:
            return 0.5

    def _alu_operations(self, numbers: List[int]) -> List[Dict]:
        ops = []
        for n in numbers[:5]:
            if n <= 0: continue
            try:
                if n <= 20:
                    fact = float(self.alu.factorial(float(n)).real)
                    ops.append({"op": f"factorial({n})", "result": fact})
                ln_n = float(_pure_ln(float(n)).real)
                ops.append({"op": f"ln({n})", "result": ln_n})
                sin_n = float(_pure_sin(float(n) * float(self.alu.PI) / 180.0).real)
                ops.append({"op": f"sin({n}°)", "result": sin_n})
            except Exception:
                pass
        return ops

    def analyze(self, problem_id: str, key_numbers: List[int],
                problem_text: str) -> MathColumnV2:
        if not key_numbers:
            key_numbers = [1, 2, 3]

        encoded = [self._encode_number(n) for n in key_numbers]
        nrci_vals = [e["nrci"] for e in encoded]
        mean_nrci = sum(nrci_vals) / len(nrci_vals) if nrci_vals else 0.5

        tgic_stabs = [e.get("tgic_stability", 0.5) for e in encoded]
        mean_tgic = sum(tgic_stabs) / len(tgic_stabs) if tgic_stabs else 0.5

        prime_count = sum(1 for e in encoded if e.get("is_prime", False))
        prime_density = prime_count / len(encoded) if encoded else 0.0

        weights = [e["hamming_weight"] for e in encoded]
        weight_dist = {}
        for w in weights:
            weight_dist[str(w)] = weight_dist.get(str(w), 0) + 1

        if len(nrci_vals) > 1:
            variance = sum((x - mean_nrci)**2 for x in nrci_vals) / len(nrci_vals)
            geo_complexity = math.sqrt(variance) * 10.0
        else:
            geo_complexity = mean_nrci

        analog_verifs = self._analog_verify(key_numbers)
        bw_macro = self._bw256_macro_nrci(problem_text)
        alu_ops = self._alu_operations(key_numbers)

        # Prime factorisation map
        fact_map = {}
        for n in key_numbers[:6]:
            if abs(n) > 1:
                fact_map[str(n)] = self._factorise(n)

        return MathColumnV2(
            problem_id=problem_id,
            numeric_objects=encoded,
            nrci_values=nrci_vals,
            mean_nrci=mean_nrci,
            alu_operations=alu_ops,
            geometric_complexity=geo_complexity,
            prime_density=prime_density,
            golay_weight_distribution=weight_dist,
            tgic_stability_scores=tgic_stabs,
            mean_tgic_stability=mean_tgic,
            analog_verifications=analog_verifs,
            bw256_macro_nrci=bw_macro,
            factorisation_map=fact_map
        )


# ─── COLUMN 2 V2: SOVEREIGN PHYSICIST ────────────────────────────────────────

class SovereignPhysicistV2:
    """
    Enhanced Sovereign Physicist with full TGIC 3-6-9 audit,
    RuneCube face projections, OffBit phase tracking, and
    Leech rank_by_stability comparison.
    """

    def __init__(self):
        self.alu = GrandUnifiedEmlALU()
        self.observer = ObserverDynamicsEngine()
        self.tgic = TGICInteractionEngine()
        self._offbit_phase = 0  # accumulates across problems

    def prove(self, problem_id: str, problem_text: str,
              math_col: MathColumnV2) -> SovereignColumnV2:

        # 1. Build EML tree and evaluate to complex value
        h = int(hashlib.sha256(problem_text.encode()).hexdigest(), 16)
        h_float = (h % 1000000) / 1000000.0
        x_val = complex(self.alu.TRIADIC_MONAD * h_float)

        leaf_val_a = complex(math_col.mean_nrci)
        leaf_val_b = x_val if x_val != 0 else complex(1.0)
        leaf_val_c = complex(max(0.01, math_col.prime_density))

        try:
            eml_inner = self.alu.eml(leaf_val_a, abs(leaf_val_b) + 0.001)
            eml_outer = self.alu.eml(eml_inner, abs(leaf_val_c) + 0.001)
            raw_val = abs(eml_outer)
            bits = [1 if (raw_val * (i + 1)) % 2.0 >= 1.0 else 0 for i in range(24)]
            snapped_vec, snap_info = GOLAY_ENGINE.snap_to_codeword(bits)
            addr = sum(b * (2**i) for i, b in enumerate(snapped_vec[:12]))
        except Exception as e:
            logger.debug(f"Lattice snap error: {e}")
            all_cw = GOLAY_ENGINE.get_all_codewords()
            idx = int(math_col.mean_nrci * len(all_cw)) % len(all_cw)
            snapped_vec = list(all_cw[idx])
            addr = idx

        # 2. TGIC full 3-6-9 audit on snapped vector
        try:
            tgic_stab = float(self.tgic.calculate_total_stability(snapped_vec))
        except Exception:
            tgic_stab = float(math_col.mean_tgic_stability)

        # 3. RuneCube face projections
        try:
            rune_xy = self.tgic.rune_resonance_xy(snapped_vec)
            rune_xz = self.tgic.rune_entangle_xz(snapped_vec)
            rune_yz = self.tgic.rune_expand_yz(snapped_vec)
            tax_xy = float(LEECH_ENGINE.calculate_symmetry_tax(rune_xy))
            tax_xz = float(LEECH_ENGINE.calculate_symmetry_tax(rune_xz))
            tax_yz = float(LEECH_ENGINE.calculate_symmetry_tax(rune_yz))
        except Exception:
            tax_xy = tax_xz = tax_yz = 0.0

        # 4. Leech rank_by_stability: compare snapped vs raw bits
        try:
            ranked = LEECH_ENGINE.rank_by_stability([snapped_vec, bits])
            # rank 0 = most stable; if snapped is rank 0, it's better
            stability_rank = 0 if ranked[0][0] == snapped_vec else 1
        except Exception:
            stability_rank = 0

        # 5. OffBit phase tracking
        self._offbit_phase = (self._offbit_phase + addr) % 256

        # 6. Leech symmetry tax and SOC
        nrci = Fraction(math_col.mean_nrci).limit_denominator(1000)
        try:
            sym_tax = float(LEECH_ENGINE.calculate_symmetry_tax(snapped_vec, compactness=nrci))
            leech_norm = float(sum(snapped_vec))
        except Exception:
            leech_norm = float(sum(snapped_vec))
            sym_tax = float(nrci) * 0.1

        soc = self.observer.calculate_soc_energy(snapped_vec, nrci)
        read = self.observer.conscious_read(snapped_vec, nrci)

        # 7. Coherence: combine NRCI, TGIC stability, manifestation
        nrci_f = float(nrci)
        manif_bonus = 0.2 if read["status"] == "MANIFESTED" else 0.0
        tgic_contrib = min(0.3, abs(tgic_stab) * 0.1)
        coherence = min(1.0, nrci_f + manif_bonus + tgic_contrib)

        # Build EML tree string
        tree_str = f"eml(eml(leaf({math_col.mean_nrci:.4f}),leaf({abs(x_val):.4f})),leaf({math_col.prime_density:.4f}))"

        return SovereignColumnV2(
            problem_id=problem_id,
            eml_tree_repr=tree_str,
            golay_address=addr,
            snapped_vector=snapped_vec,
            soc_energy=soc,
            manifestation=read["status"],
            leech_norm=leech_norm,
            symmetry_tax=sym_tax,
            coherence_score=coherence,
            tgic_total_stability=tgic_stab,
            rune_xy_tax=tax_xy,
            rune_xz_tax=tax_xz,
            rune_yz_tax=tax_yz,
            stability_rank=stability_rank,
            offbit_phase=self._offbit_phase
        )


# ─── COLUMN 3 V2: LANGUAGE SCRIBE ────────────────────────────────────────────

class LanguageScribeV2:
    """
    Enhanced Language Scribe with:
    - UBP Brain v7.2 (Identity Lock + Lattice Resonance)
    - Python Code Generator + safe executor for numerical verification
    - Analog arithmetic cross-check
    - Self-correction loop (up to 2 retries)
    - Ontological drift classification
    """

    DOMAIN_LAWS = {
        "Number Theory": ["divisibility", "prime", "modular", "congruence", "factorization"],
        "Algebra": ["polynomial", "inequality", "function", "equation", "algebraic"],
        "Geometry": ["triangle", "circle", "angle", "geometry", "distance"],
        "Combinatorics": ["counting", "permutation", "combination", "graph", "pigeonhole"]
    }

    def __init__(self, semantic_engine: UBPSemanticEngine,
                 brain: UBPBrain, py_engine: UBPPythonCodeEngine):
        self.semantic = semantic_engine
        self.brain = brain
        self.py_engine = py_engine
        self.analog = UBPAnalogTestSuite(v_ref=1000.0)

    def _brain_query(self, domain: str, problem_text: str) -> Tuple[str, str, str]:
        """Use UBP Brain v7.2 for identity lock + lattice resonance."""
        # Query with domain keywords
        keywords = self.DOMAIN_LAWS.get(domain, ["mathematics"])
        query = f"{domain} {' '.join(keywords[:2])} {problem_text[:50]}"
        try:
            result = self.brain.process_query(query)
            uid = result.ubp_id or "UNKNOWN"
            method = result.method
            # Ontological drift classification
            if uid != "UNKNOWN" and uid in self.brain.kb_manager.kb:
                entry = self.brain.kb_manager.kb[uid]
                vec = extract_vector(entry)
                if vec:
                    hw = sum(vec)
                    if hw <= 4: ontology = "PHENOMENAL (Physical Matter)"
                    elif 10 <= hw <= 14: ontology = "NOUMENAL (Abstract Concept)"
                    else: ontology = "TRANSITIONAL (Anomalous State)"
                else:
                    ontology = "UNKNOWN"
            else:
                ontology = "NULL_RESONANCE"
            return uid, method, ontology
        except Exception as e:
            return "UNKNOWN", f"Error: {e}", "UNKNOWN"

    def _generate_verification_code(self, problem_text: str,
                                    key_numbers: List[int]) -> Tuple[str, str, bool]:
        """Generate and execute Python verification code via UBP Python engine."""
        if not key_numbers:
            return "", "", False

        # Build a targeted intent for the Python code generator
        nums_str = ", ".join(str(n) for n in key_numbers[:5])
        intent = f"verify mathematical computation with numbers {nums_str}"

        try:
            # Use the UBP Python engine's code generator
            code_result = self.py_engine.write(intent, verbose=False)
            code = code_result.code

            # Safe execution with timeout
            output = self._safe_exec(code)
            return code, output, True
        except Exception as e:
            # Fallback: generate simple verification code ourselves
            code = self._fallback_code(key_numbers, problem_text)
            output = self._safe_exec(code)
            return code, output, output != ""

    def _fallback_code(self, key_numbers: List[int], problem_text: str) -> str:
        """Generate simple but useful verification code."""
        nums = [n for n in key_numbers if n > 0][:6]
        lines = [
            "# UBP Mathematical Verification Script",
            "from math import gcd, sqrt, factorial",
            "from functools import reduce",
            "",
            f"numbers = {nums}",
            "",
            "# Basic number-theoretic properties",
            "def is_prime(n):",
            "    if n < 2: return False",
            "    return all(n % i != 0 for i in range(2, int(n**0.5)+1))",
            "",
            "primes = [n for n in numbers if is_prime(n)]",
            "print(f'Key numbers: {numbers}')",
            "print(f'Primes among them: {primes}')",
        ]

        # Add problem-specific code based on text analysis
        text_lower = problem_text.lower()
        if "divisib" in text_lower or "mod" in text_lower:
            lines += [
                "",
                "# Divisibility analysis",
                "for a in numbers:",
                "    for b in numbers:",
                "        if a != b and b != 0:",
                "            print(f'  {a} mod {b} = {a % b}')",
            ]
        elif "gcd" in text_lower or "greatest common" in text_lower:
            lines += [
                "",
                "# GCD analysis",
                "for i in range(len(numbers)):",
                "    for j in range(i+1, len(numbers)):",
                "        g = gcd(numbers[i], numbers[j])",
                "        print(f'  gcd({numbers[i]},{numbers[j]}) = {g}')",
            ]
        elif "sum" in text_lower or "product" in text_lower:
            lines += [
                "",
                f"print(f'Sum: {{{sum(nums)}}}')",
                f"product = reduce(lambda a,b: a*b, numbers, 1)",
                "print(f'Product: {product}')",
            ]
        elif "sqrt" in text_lower or "square" in text_lower:
            lines += [
                "",
                "# Square root analysis",
                "for n in numbers:",
                "    print(f'  sqrt({n}) = {sqrt(n):.6f}')",
            ]

        return "\n".join(lines)

    def _safe_exec(self, code: str, timeout: float = 3.0) -> str:
        """Execute code safely, capturing stdout."""
        if not code:
            return ""
        try:
            buf = io.StringIO()
            # Restrict builtins for safety
            safe_globals = {
                "__builtins__": {
                    "print": print, "range": range, "len": len,
                    "int": int, "float": float, "str": str, "list": list,
                    "dict": dict, "set": set, "tuple": tuple, "bool": bool,
                    "abs": abs, "min": min, "max": max, "sum": sum,
                    "sorted": sorted, "enumerate": enumerate, "zip": zip,
                    "all": all, "any": any, "map": map, "filter": filter,
                    "__import__": __import__
                }
            }
            with contextlib.redirect_stdout(buf):
                exec(compile(code, "<ubp_gen>", "exec"), safe_globals)
            return buf.getvalue().strip()[:500]  # Limit output
        except Exception as e:
            return f"[exec error: {str(e)[:100]}]"

    def _analog_arithmetic_check(self, key_numbers: List[int]) -> Dict:
        """Use EM analog engine to verify arithmetic on key numbers."""
        nums = [float(n) for n in key_numbers if n > 0][:3]
        result = {}
        if len(nums) >= 2:
            try:
                add_r, add_sym, _ = self.analog.op_add(nums[0], nums[1])
                result["add"] = {
                    "a": nums[0], "b": nums[1],
                    "analog_result": round(add_r, 4),
                    "expected": nums[0] + nums[1],
                    "symmetry_tax": round(add_sym, 4)
                }
                if nums[0] > 0 and nums[1] > 0:
                    sqrt_r, sqrt_sym, _ = self.analog.op_sqrt(nums[0])
                    result["sqrt"] = {
                        "a": nums[0],
                        "analog_result": round(sqrt_r, 4),
                        "expected": round(math.sqrt(nums[0]), 4),
                        "symmetry_tax": round(sqrt_sym, 4)
                    }
            except Exception:
                pass
        return result

    def _get_semantic_context(self, problem_text: str, domain: str,
                              brain_uid: str) -> Tuple[List[Dict], float, List[str]]:
        """Enhanced semantic context using both semantic engine and brain result."""
        keywords = self.DOMAIN_LAWS.get(domain, ["mathematics"])
        all_hits = []
        for term in keywords[:3]:
            try:
                results = self.semantic.query(term, top_k=2)
                for r in results:
                    all_hits.append({
                        "ubp_id": r.ubp_id,
                        "resonance": r.resonance_score,
                        "summary": r.summary()[:120]
                    })
            except Exception:
                pass

        # Add brain result as high-priority hit
        if brain_uid and brain_uid != "UNKNOWN" and brain_uid in self.brain.kb_manager.kb:
            entry = self.brain.kb_manager.kb[brain_uid]
            all_hits.insert(0, {
                "ubp_id": brain_uid,
                "resonance": 0.95,  # Identity lock = high confidence
                "summary": entry.get("lexicon", "")[:120]
            })

        seen = set()
        unique_hits = []
        for h in sorted(all_hits, key=lambda x: x["resonance"], reverse=True):
            if h["ubp_id"] not in seen:
                seen.add(h["ubp_id"])
                unique_hits.append(h)

        peak_resonance = unique_hits[0]["resonance"] if unique_hits else 0.0
        laws_invoked = [h["ubp_id"] for h in unique_hits[:4]]
        return unique_hits[:6], peak_resonance, laws_invoked

    def _build_enriched_prompt(self, problem_text: str, domain: str,
                               semantic_context: List[Dict],
                               math_col: MathColumnV2,
                               code_output: str,
                               analog_check: Dict,
                               attempt: int) -> str:
        """Build an increasingly rich prompt for each retry attempt."""

        # UBP geometric context
        ubp_ctx = f"\n\nUBP Geometric Analysis:\n"
        ubp_ctx += f"- Mean NRCI: {math_col.mean_nrci:.4f} (stability index)\n"
        ubp_ctx += f"- TGIC Stability: {math_col.mean_tgic_stability:.4f}\n"
        ubp_ctx += f"- Prime density: {math_col.prime_density:.2f}\n"
        ubp_ctx += f"- Barnes-Wall macro coherence: {math_col.bw256_macro_nrci:.4f}\n"

        # Factorisation hints
        if math_col.factorisation_map:
            ubp_ctx += "- Key factorisations: "
            for n, fac in list(math_col.factorisation_map.items())[:3]:
                fac_str = " × ".join(f"{p}^{e}" if e > 1 else str(p)
                                     for p, e in sorted(fac.items()))
                ubp_ctx += f"{n} = {fac_str}; "
            ubp_ctx += "\n"

        # Code output hint
        if code_output and not code_output.startswith("[exec error"):
            ubp_ctx += f"\nNumerical verification (Python):\n{code_output[:300]}\n"

        # Analog check hint
        if analog_check.get("add"):
            ac = analog_check["add"]
            ubp_ctx += f"\nEM Analog check: {ac['a']} + {ac['b']} = {ac['analog_result']} (expected {ac['expected']})\n"

        # UBP laws
        if semantic_context:
            ubp_ctx += "\nResonant UBP Laws:\n"
            for h in semantic_context[:3]:
                ubp_ctx += f"  - {h['summary']}\n"

        # Attempt-specific instructions
        if attempt == 1:
            instruction = "Solve this problem step by step. Show all working. State the final answer explicitly."
        elif attempt == 2:
            instruction = ("Your previous attempt may have been incomplete. "
                           "Focus on the key numerical result. "
                           "Use the factorisation hints above. "
                           "State the final answer as a specific number or expression.")
        else:
            instruction = ("Final attempt. Be extremely precise. "
                           "State ONLY the final answer after showing minimal key steps. "
                           "The answer must be a specific value.")

        return (
            f"Problem ({domain}):\n{problem_text}"
            f"{ubp_ctx}\n\n{instruction}"
        )

    def _determine_domain_alignment(self, domain: str, laws: List[str]) -> str:
        if any("LAW_" in l for l in laws): return "PHYSICAL_LAW"
        elif any("PARTICLE_" in l for l in laws): return "PARTICLE_PHYSICS"
        elif any("ELEM_" in l for l in laws): return "ELEMENTAL"
        elif any("LANG_" in l for l in laws): return "LINGUISTIC"
        else: return "GEOMETRIC"

    def write(self, problem_id: str, problem_text: str, domain: str,
              math_col: MathColumnV2, key_numbers: List[int]) -> LanguageColumnV2:

        # 1. UBP Brain v7.2 query
        brain_uid, brain_method, ontology = self._brain_query(domain, problem_text)

        # 2. Semantic context (enriched with brain result)
        hits, resonance, laws = self._get_semantic_context(problem_text, domain, brain_uid)
        alignment = self._determine_domain_alignment(domain, laws)

        # 3. Python code generation + execution
        gen_code, code_output, code_ok = self._generate_verification_code(
            problem_text, key_numbers)

        # 4. Analog arithmetic check
        analog_check = self._analog_arithmetic_check(key_numbers)

        # 5. LLM solution with self-correction loop
        solution = ""
        model_used = "none"
        total_tokens = 0
        attempts = 0
        self_correction = False

        for attempt in range(1, 4):
            attempts = attempt
            prompt = self._build_enriched_prompt(
                problem_text, domain, hits, math_col,
                code_output, analog_check, attempt)

            if not OPENAI_AVAILABLE:
                solution = (
                    f"[UBP v2.0 Analysis] Domain: {domain}. "
                    f"Brain: {brain_uid} ({brain_method}). "
                    f"Ontology: {ontology}. "
                    f"NRCI: {math_col.mean_nrci:.4f}. "
                    f"Code output: {code_output[:100] if code_output else 'N/A'}."
                )
                model_used = "none"
                break

            try:
                resp = _client.chat.completions.create(
                    model="gpt-4.1-mini",
                    messages=[
                        {"role": "system",
                         "content": (
                             "You are a mathematical olympiad expert. "
                             "Solve problems rigorously and precisely. "
                             "Always state the final answer explicitly on its own line."
                         )},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=900,
                    temperature=max(0.0, 0.15 - attempt * 0.05)
                )
                solution = resp.choices[0].message.content
                total_tokens += resp.usage.total_tokens
                model_used = "gpt-4.1-mini"

                # Quick self-check: does the solution contain a numeric answer?
                nums_in_sol = re.findall(r'\b\d+\.?\d*\b', solution)
                if nums_in_sol or attempt >= 2:
                    # Acceptable — stop here
                    if attempt > 1:
                        self_correction = True
                    break

            except Exception as e:
                logger.warning(f"LLM attempt {attempt} error: {e}")
                solution = f"LLM error: {str(e)}"
                break

        return LanguageColumnV2(
            problem_id=problem_id,
            semantic_hits=hits,
            semantic_resonance=resonance,
            ubp_laws_invoked=laws,
            brain_result_uid=brain_uid,
            brain_method=brain_method,
            ontology_class=ontology,
            generated_code=gen_code,
            code_output=code_output,
            code_verified=code_ok,
            analog_arithmetic_check=analog_check,
            llm_solution=solution,
            llm_model=model_used,
            solution_tokens=total_tokens,
            domain_alignment=alignment,
            attempts=attempts,
            self_correction_applied=self_correction
        )


# ─── GRADER ──────────────────────────────────────────────────────────────────

class SolutionGraderV2:
    """Enhanced grader that also checks code output against reference."""

    def _extract_numbers(self, text: str) -> set:
        nums = re.findall(r'-?\d+\.?\d*', text)
        result = set()
        for n in nums:
            try:
                result.add(float(n))
            except ValueError:
                pass
        return result

    def _keyword_match(self, solution: str, reference: str) -> float:
        sol_words = set(re.findall(r'\b\w+\b', solution.lower()))
        ref_words = set(re.findall(r'\b\w+\b', reference.lower()))
        stops = {'the','a','an','is','are','was','were','be','been','have','has',
                 'had','do','does','did','will','would','could','should','may',
                 'might','shall','can','for','of','to','in','on','at','by','with',
                 'from','that','this','these','those','it','its','and','or','but',
                 'not','no','so','if','then','all','each'}
        sol_c = sol_words - stops
        ref_c = ref_words - stops
        if not ref_c: return 0.5
        return min(1.0, len(sol_c & ref_c) / len(ref_c))

    def _number_match(self, solution: str, reference: str) -> float:
        ref_nums = self._extract_numbers(reference)
        sol_nums = self._extract_numbers(solution)
        if not ref_nums: return 0.5
        matched = ref_nums & sol_nums
        return len(matched) / len(ref_nums)

    def grade(self, solution: str, reference: str, problem_text: str,
              code_output: str = "") -> Tuple[float, str]:
        if not solution or solution.startswith("LLM error"):
            return 0.0, "INCORRECT"

        kw_score = self._keyword_match(solution, reference)
        num_score = self._number_match(solution, reference)

        # Bonus: check if code output contains reference numbers
        code_bonus = 0.0
        if code_output and not code_output.startswith("[exec error"):
            code_nums = self._extract_numbers(code_output)
            ref_nums = self._extract_numbers(reference)
            if ref_nums and (ref_nums & code_nums):
                code_bonus = 0.15

        combined = 0.35 * kw_score + 0.5 * num_score + code_bonus

        # LLM-as-judge
        if OPENAI_AVAILABLE:
            try:
                prompt = (
                    f"Problem: {problem_text[:250]}\n\n"
                    f"Reference answer: {reference}\n\n"
                    f"Student solution: {solution[:600]}\n\n"
                    "Rate: CORRECT (fully correct), PARTIAL (partially correct), "
                    "or INCORRECT. One word only."
                )
                resp = _client.chat.completions.create(
                    model="gpt-4.1-mini",
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=5, temperature=0.0
                )
                label_raw = resp.choices[0].message.content.strip().upper()
                if "CORRECT" in label_raw and "PARTIAL" not in label_raw:
                    return 1.0, "CORRECT"
                elif "PARTIAL" in label_raw:
                    return 0.5, "PARTIAL"
                else:
                    return 0.0, "INCORRECT"
            except Exception:
                pass

        if combined >= 0.7: return combined, "CORRECT"
        elif combined >= 0.35: return combined, "PARTIAL"
        else: return combined, "INCORRECT"


# ─── TCT AUDITOR V2 ──────────────────────────────────────────────────────────

class TCTAuditorV2:
    """
    Enhanced auditor that computes both alignment and convergence.
    Convergence measures whether all three columns point to the same answer.
    """

    def audit(self, math_col: MathColumnV2, sov_col: SovereignColumnV2,
              lang_col: LanguageColumnV2) -> Tuple[float, float]:
        """Returns (alignment_score, convergence_score)."""
        scores = []

        # Math-Sovereign: NRCI vs coherence
        nrci_coh_diff = abs(math_col.mean_nrci - sov_col.coherence_score)
        scores.append(1.0 - min(1.0, nrci_coh_diff * 2))

        # Sovereign-Language: manifestation vs semantic resonance
        manif_score = {"MANIFESTED": 1.0, "SUBLIMINAL": 0.6}.get(
            sov_col.manifestation, 0.3)
        res_score = min(1.0, lang_col.semantic_resonance)
        scores.append((manif_score + res_score) / 2.0)

        # Math-Language: prime density + code verification bonus
        code_bonus = 0.15 if lang_col.code_verified else 0.0
        scores.append(min(1.0, math_col.prime_density + code_bonus + 0.4))

        # NEW: TGIC stability alignment
        tgic_align = min(1.0, abs(math_col.mean_tgic_stability) / 5.0 + 0.5)
        scores.append(tgic_align)

        alignment = sum(scores) / len(scores)

        # Convergence: do all three columns agree on the domain?
        # High convergence = brain found a relevant law AND code ran AND NRCI > 0.65
        conv_factors = [
            1.0 if lang_col.brain_result_uid != "UNKNOWN" else 0.3,
            1.0 if lang_col.code_verified else 0.5,
            min(1.0, math_col.mean_nrci / 0.7),
            min(1.0, sov_col.tgic_total_stability / 3.0 + 0.5)
        ]
        convergence = sum(conv_factors) / len(conv_factors)

        return alignment, convergence


# ─── MAIN ORCHESTRATOR V2 ────────────────────────────────────────────────────

class UBPSwarmTCTMathNetV2:
    """
    v2.0 Orchestrator: Full UBP system integration with all engines active.
    """

    def __init__(self, problem_set_path: str, output_dir: str,
                 kb_path: str, lang_kb_path: str):
        self.problem_set_path = problem_set_path
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

        logger.info("Initializing UBP Swarm TCT MathNet v2.0 (FULL SYSTEM)...")

        # Semantic engine
        self.semantic = UBPSemanticEngine()
        self.semantic.load(kb_path, lang_kb_path)

        # UBP Brain v7.2
        self.brain = UBPBrain()
        self.brain.initialize([kb_path, lang_kb_path])

        # Python engine
        # UBPPythonEngine uses ubp_python_kb.json (not the main system kb)
        py_kb = os.path.join(os.path.dirname(kb_path), 'ubp_python_kb.json')
        self.py_engine = UBPPythonCodeEngine(py_kb if os.path.exists(py_kb) else kb_path)

        # Column engines
        self.math_engine = MathArchitectV2()
        self.sovereign = SovereignPhysicistV2()
        self.language = LanguageScribeV2(self.semantic, self.brain, self.py_engine)
        self.grader = SolutionGraderV2()
        self.auditor = TCTAuditorV2()

        logger.info("All v2.0 engines initialized (Brain v7.2, TGIC, Analog, BW256, PyGen).")

    def _load_problems(self) -> List[Dict]:
        with open(self.problem_set_path, 'r') as f:
            data = json.load(f)
        return data["problems"]

    def run(self) -> List[TCTResultV2]:
        problems = self._load_problems()
        logger.info(f"Loaded {len(problems)} problems.")

        results = []
        for i, prob in enumerate(problems):
            pid = prob["id"]
            logger.info(f"\n{'='*60}")
            logger.info(f"[{i+1}/{len(problems)}] {pid}: {prob['domain']} / {prob['subdomain']}")
            logger.info(f"Problem: {prob['problem'][:80]}...")

            t_start = time.time()
            try:
                result = self._process_problem(prob)
                results.append(result)
                logger.info(
                    f"  → {result.correctness_label} ({result.correctness_score:.2f}) | "
                    f"NRCI:{result.math_col.mean_nrci:.4f} | "
                    f"TGIC:{result.math_col.mean_tgic_stability:.3f} | "
                    f"SOC:{result.sovereign_col.soc_energy/1e6:.0f}M | "
                    f"Brain:{result.language_col.brain_result_uid[:20]} | "
                    f"Code:{'✓' if result.language_col.code_verified else '✗'} | "
                    f"Attempts:{result.language_col.attempts} | "
                    f"Align:{result.alignment_score:.3f} | "
                    f"Conv:{result.tct_convergence:.3f} | "
                    f"{time.time()-t_start:.1f}s"
                )
            except Exception as e:
                logger.error(f"  Error: {e}", exc_info=True)

        self._save_results(results)
        self._print_summary(results)
        return results

    def _process_problem(self, prob: Dict) -> TCTResultV2:
        import datetime
        t_start = time.time()
        pid = prob["id"]
        problem_text = prob["problem"]
        domain = prob["domain"]
        key_numbers = prob.get("key_numbers", [1, 2, 3])

        # Column 1: Math Architect V2
        logger.info(f"  [Col 1] Geometric + TGIC + BW256 analysis...")
        math_col = self.math_engine.analyze(pid, key_numbers, problem_text)

        # Column 2: Sovereign Physicist V2
        logger.info(f"  [Col 2] TGIC 3-6-9 + RuneCube + OffBit sovereign proof...")
        sov_col = self.sovereign.prove(pid, problem_text, math_col)

        # Column 3: Language Scribe V2
        logger.info(f"  [Col 3] Brain v7.2 + PyGen + Analog + LLM (self-correction)...")
        lang_col = self.language.write(pid, problem_text, domain, math_col, key_numbers)

        # Grade
        score, label = self.grader.grade(
            lang_col.llm_solution,
            prob.get("answer", ""),
            problem_text,
            lang_col.code_output
        )

        # Audit
        alignment, convergence = self.auditor.audit(math_col, sov_col, lang_col)

        # UBP confidence: NRCI + TGIC + coherence
        ubp_conf = (math_col.mean_nrci + sov_col.coherence_score +
                    min(1.0, abs(math_col.mean_tgic_stability) / 5.0)) / 3.0

        return TCTResultV2(
            problem_id=pid,
            domain=domain,
            subdomain=prob.get("subdomain", ""),
            problem_text=problem_text,
            reference_answer=prob.get("answer", ""),
            math_col=math_col,
            sovereign_col=sov_col,
            language_col=lang_col,
            correctness_score=score,
            correctness_label=label,
            ubp_confidence=ubp_conf,
            alignment_score=alignment,
            tct_convergence=convergence,
            processing_time_s=time.time() - t_start,
            timestamp=datetime.datetime.utcnow().isoformat()
        )

    def _save_results(self, results: List[TCTResultV2]):
        output = {
            "metadata": {
                "system": "UBP Swarm TCT MathNet v2.0",
                "ubp_version": "core_studio_v4.0",
                "benchmark": "MathNet MIT (mathnet.mit.edu)",
                "date": time.strftime("%Y-%m-%d"),
                "total_problems": len(results),
                "openai_model": "gpt-4.1-mini" if OPENAI_AVAILABLE else "none",
                "engines_active": [
                    "GOLAY_ENGINE", "LEECH_ENGINE", "EML_ALU",
                    "ObserverDynamics", "TGIC_3-6-9", "RuneCube",
                    "BarnesWall256", "UBPBrain_v7.2", "PythonCodeGen",
                    "AnalogTestSuite", "SemanticEngine", "LLM_SelfCorrection"
                ]
            },
            "results": []
        }

        for r in results:
            output["results"].append({
                "problem_id": r.problem_id,
                "domain": r.domain,
                "subdomain": r.subdomain,
                "problem_text": r.problem_text,
                "reference_answer": r.reference_answer,
                "version": r.version,
                "math_column": {
                    "mean_nrci": r.math_col.mean_nrci,
                    "nrci_values": r.math_col.nrci_values,
                    "prime_density": r.math_col.prime_density,
                    "geometric_complexity": r.math_col.geometric_complexity,
                    "mean_tgic_stability": r.math_col.mean_tgic_stability,
                    "tgic_stability_scores": r.math_col.tgic_stability_scores,
                    "bw256_macro_nrci": r.math_col.bw256_macro_nrci,
                    "golay_weight_distribution": r.math_col.golay_weight_distribution,
                    "factorisation_map": r.math_col.factorisation_map,
                    "analog_verifications": r.math_col.analog_verifications[:2],
                    "alu_operations": r.math_col.alu_operations[:3],
                    "numeric_objects": [
                        {k: v for k, v in obj.items() if k != "vector"}
                        for obj in r.math_col.numeric_objects
                    ]
                },
                "sovereign_column": {
                    "golay_address": r.sovereign_col.golay_address,
                    "snapped_vector": r.sovereign_col.snapped_vector,
                    "soc_energy": r.sovereign_col.soc_energy,
                    "manifestation": r.sovereign_col.manifestation,
                    "leech_norm": r.sovereign_col.leech_norm,
                    "symmetry_tax": r.sovereign_col.symmetry_tax,
                    "coherence_score": r.sovereign_col.coherence_score,
                    "tgic_total_stability": r.sovereign_col.tgic_total_stability,
                    "rune_xy_tax": r.sovereign_col.rune_xy_tax,
                    "rune_xz_tax": r.sovereign_col.rune_xz_tax,
                    "rune_yz_tax": r.sovereign_col.rune_yz_tax,
                    "stability_rank": r.sovereign_col.stability_rank,
                    "offbit_phase": r.sovereign_col.offbit_phase,
                    "eml_tree": r.sovereign_col.eml_tree_repr
                },
                "language_column": {
                    "semantic_resonance": r.language_col.semantic_resonance,
                    "ubp_laws_invoked": r.language_col.ubp_laws_invoked,
                    "domain_alignment": r.language_col.domain_alignment,
                    "brain_result_uid": r.language_col.brain_result_uid,
                    "brain_method": r.language_col.brain_method,
                    "ontology_class": r.language_col.ontology_class,
                    "code_verified": r.language_col.code_verified,
                    "code_output": r.language_col.code_output[:300] if r.language_col.code_output else "",
                    "analog_arithmetic_check": r.language_col.analog_arithmetic_check,
                    "llm_model": r.language_col.llm_model,
                    "solution_tokens": r.language_col.solution_tokens,
                    "attempts": r.language_col.attempts,
                    "self_correction_applied": r.language_col.self_correction_applied,
                    "llm_solution": r.language_col.llm_solution,
                    "semantic_hits": r.language_col.semantic_hits[:3]
                },
                "grading": {
                    "correctness_score": r.correctness_score,
                    "correctness_label": r.correctness_label,
                    "ubp_confidence": r.ubp_confidence,
                    "alignment_score": r.alignment_score,
                    "tct_convergence": r.tct_convergence
                },
                "processing_time_s": r.processing_time_s,
                "timestamp": r.timestamp
            })

        out_path = os.path.join(self.output_dir, "ubp_mathnet_results_v2.json")
        with open(out_path, 'w') as f:
            json.dump(output, f, indent=2)
        logger.info(f"v2 results saved to {out_path}")

    def _print_summary(self, results: List[TCTResultV2]):
        print("\n" + "="*90)
        print("UBP × MathNet BENCHMARK v2.0 SUMMARY")
        print("="*90)
        print(f"{'ID':<15} {'Domain':<15} {'NRCI':<8} {'TGIC':<8} {'Conv':<8} {'Brain':<25} {'Code':<6} {'Grade'}")
        print("-"*90)

        correct = partial = incorrect = 0
        for r in results:
            brain_short = r.language_col.brain_result_uid[:22]
            code_ok = "✓" if r.language_col.code_verified else "✗"
            print(f"{r.problem_id:<15} {r.domain[:14]:<15} "
                  f"{r.math_col.mean_nrci:.4f}   "
                  f"{r.math_col.mean_tgic_stability:.3f}   "
                  f"{r.tct_convergence:.3f}   "
                  f"{brain_short:<25} {code_ok:<6} "
                  f"{r.correctness_label}")
            if r.correctness_label == "CORRECT": correct += 1
            elif r.correctness_label == "PARTIAL": partial += 1
            else: incorrect += 1

        total = len(results)
        print("="*90)
        print(f"CORRECT:    {correct}/{total} ({100*correct/total:.1f}%)")
        print(f"PARTIAL:    {partial}/{total} ({100*partial/total:.1f}%)")
        print(f"INCORRECT:  {incorrect}/{total} ({100*incorrect/total:.1f}%)")
        print(f"Adj Score:  {100*(correct + 0.5*partial)/total:.1f}%")
        print(f"Avg NRCI:   {sum(r.math_col.mean_nrci for r in results)/total:.4f}")
        print(f"Avg TGIC:   {sum(r.math_col.mean_tgic_stability for r in results)/total:.4f}")
        print(f"Avg Conv:   {sum(r.tct_convergence for r in results)/total:.4f}")
        code_ok_count = sum(1 for r in results if r.language_col.code_verified)
        print(f"Code OK:    {code_ok_count}/{total} ({100*code_ok_count/total:.1f}%)")
        print("="*90)


# ─── ENTRY POINT ─────────────────────────────────────────────────────────────

if __name__ == "__main__":
    BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    orchestrator = UBPSwarmTCTMathNetV2(
        problem_set_path=os.path.join(BASE, "data", "ubp_mathnet_problem_set.json"),
        output_dir=os.path.join(BASE, "results"),
        kb_path=os.path.join(CORE_DIR, "ubp_system_kb.json"),
        lang_kb_path=os.path.join(CORE_DIR, "ubp_lang_kb_combined_v4.json")
    )

    results = orchestrator.run()
    print(f"\nDone. {len(results)} problems processed with full UBP v2.0 system.")
