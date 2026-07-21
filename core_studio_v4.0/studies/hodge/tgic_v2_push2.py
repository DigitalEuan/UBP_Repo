  
#!/usr/bin/env python3
"""
TGIC_v2 Push 2: Lead 4 / Lead 5 / DHC Refinement
====================================================

PURPOSE: Refine the three failing components of TGIC_v2 and push
  directly at the Discrete Hodge Conjecture (DHC).

  Lead 4 (Rotation) -- FAILED at 4.2% preservation.
    Problem: MOG column/row swaps don't all live in M_24 for our generator.
    Fix: Discover actual automorphisms by testing all 276 transpositions
         against the full code, then build the group from generators.

  Lead 5 (Rationality) -- FAILED: only 68/4096 codewords pass hexacode.
    Problem: Our GF(4) W/W_BAR assignment doesn't match the code's structure.
    Fix: Search all 20 possible W/W_BAR assignments of the 6 weight-2
         patterns. Then brute-force derive the actual constraint space.

  DHC (Discrete Hodge Conjecture) -- The real target.
    Forward:  codeword => NOISE=0 AND hexacode-constraints  (proven v2)
    Converse: NOISE=0 AND hexacode-constraints => codeword?  (test now)
    Key: use DERIVED constraints (not assumed standard ones).

STANDING RULE: "Failure is direction, not defeat." -- UBP Research Principle

DEPENDENCIES: Python 3.8+ stdlib only.  Imports core from tgic_v2.py.
DATE: 2026-07-21
"""

from __future__ import annotations
import sys
import os
import random
from fractions import Fraction
from itertools import combinations, product
from typing import List, Tuple, Dict, Optional, Set, FrozenSet

# Import core from tgic_v2
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tgic_v2 import (
    get_all_codewords, get_octads, get_dodecads,
    apply_mog_permutation, set_mog_key, auto_hunt_mog_key, get_mog_key,
    project_to_hexacode, holomorphic_balance, xor,
    HomologyJumpOperator, InformationFunctional, CanonicalEvolution,
    _GF4_ADD, _gf4_add, _gf4_eq,
)


# ================================================================
# MODULE A:  COMPLETE GF(4) ARITHMETIC
# ================================================================
"""
GF(4) = {0, 1, W, W_BAR}  where  W^2 + W + 1 = 0.

Addition (polynomial addition mod 2):
  0+x = x,  x+x = 0,
  W + W_BAR = 1,  W + 1 = W_BAR,  W_BAR + 1 = W.

Multiplication:
  0*x = 0,  1*x = x,
  W*W = W_BAR,  W*W_BAR = 1,  W_BAR*W_BAR = W.
"""

_GF4_ELEMS = ["0", "1", "W", "W_BAR"]

# Complete addition table
_GF4_ADD_FULL = {
    ("0", "0"): "0", ("0", "1"): "1", ("0", "W"): "W", ("0", "W_BAR"): "W_BAR",
    ("1", "0"): "1", ("1", "1"): "0", ("1", "W"): "W_BAR", ("1", "W_BAR"): "W",
    ("W", "0"): "W", ("W", "1"): "W_BAR", ("W", "W"): "0", ("W", "W_BAR"): "1",
    ("W_BAR", "0"): "W_BAR", ("W_BAR", "1"): "W", ("W_BAR", "W"): "1", ("W_BAR", "W_BAR"): "0",
}

# Complete multiplication table
_GF4_MUL = {
    ("0", "0"): "0", ("0", "1"): "0", ("0", "W"): "0", ("0", "W_BAR"): "0",
    ("1", "0"): "0", ("1", "1"): "1", ("1", "W"): "W", ("1", "W_BAR"): "W_BAR",
    ("W", "0"): "0", ("W", "1"): "W", ("W", "W"): "W_BAR", ("W", "W_BAR"): "1",
    ("W_BAR", "0"): "0", ("W_BAR", "1"): "W_BAR", ("W_BAR", "W"): "1", ("W_BAR", "W_BAR"): "W",
}


def gf4_add(a: str, b: str) -> str:
    return _GF4_ADD_FULL.get((a, b), "NOISE")


def gf4_mul(a: str, b: str) -> str:
    return _GF4_MUL.get((a, b), "NOISE")


def gf4_dot(coeffs: List[str], word: List[str]) -> str:
    """Compute the GF(4) dot product sum(coeffs_i * word_i)."""
    s = "0"
    for a, h in zip(coeffs, word):
        prod = gf4_mul(a, h)
        if prod == "NOISE":
            return "NOISE"
        s = gf4_add(s, prod)
        if s == "NOISE":
            return "NOISE"
    return s


# ================================================================
# MODULE B:  LEAD 5 REFINED  --  GF(4) ASSIGNMENT SEARCH
# ================================================================
"""
The GF(4) mapping assigns weight-2 patterns of a 4-bit MOG column to
W (holomorphic) or W_BAR (anti-holomorphic).  There are 6 weight-2
patterns and we must split them into two groups of 3.

C(6,3) = 20 possible splits.  Only ONE of these (up to Frobenius
automorphism W<->W_BAR) produces hexacode words that form a linear
subspace of GF(4)^6.  We search exhaustively.
"""

_WEIGHT2_PATTERNS: List[Tuple[int, ...]] = [
    (1, 1, 0, 0), (1, 0, 1, 0), (1, 0, 0, 1),
    (0, 1, 1, 0), (0, 1, 0, 1), (0, 0, 1, 1),
]


def project_with_assignment(vec: List[int],
                              w_set: FrozenSet[Tuple[int, ...]],
                              wb_set: FrozenSet[Tuple[int, ...]]) -> List[str]:
    """
    Project a 24-bit vector to a 6-element GF(4) hexacode word
    using a SPECIFIED W/W_BAR assignment.
    """
    v = apply_mog_permutation(vec)
    cols = [[v[i], v[i + 6], v[i + 12], v[i + 18]] for i in range(6)]
    parities = [sum(c) % 2 for c in cols]

    # Top-row flip for odd-parity columns
    if all(p == 1 for p in parities):
        for i in range(6):
            cols[i][0] ^= 1

    word = []
    for c in cols:
        w = sum(c)
        if w == 0:
            word.append("0")
        elif w == 4:
            word.append("1")
        elif tuple(c) in w_set:
            word.append("W")
        elif tuple(c) in wb_set:
            word.append("W_BAR")
        else:
            word.append("NOISE")
    return word


def check_standard_hexacode(hx: List[str]) -> bool:
    """Check the standard 3 hexacode constraints."""
    if "NOISE" in hx:
        return False
    c1 = gf4_add(gf4_add(hx[0], hx[1]), hx[2]) == "0"  # h0+h1+h2=0
    c2 = gf4_add(gf4_add(hx[0], hx[3]), hx[4]) == "0"  # h0+h3+h4=0
    c3 = gf4_add(gf4_add(hx[1], hx[3]), hx[5]) == "0"  # h1+h3+h5=0
    return c1 and c2 and c3


def search_gf4_assignments(codewords: List[List[int]]) -> List[Dict]:
    """
    Search all 20 W/W_BAR assignments.  For each, count codewords
    whose hexacode projection satisfies the standard constraints.
    Returns results sorted by pass count (best first).
    """
    results = []
    pattern_indices = list(range(6))

    for w_indices in combinations(pattern_indices, 3):
        w_set = frozenset(_WEIGHT2_PATTERNS[i] for i in w_indices)
        wb_set = frozenset(_WEIGHT2_PATTERNS[i] for i in pattern_indices
                          if i not in w_indices)

        pass_count = 0
        noise_count = 0
        hex_words: Set[Tuple[str, ...]] = set()

        for cw in codewords:
            hx = project_with_assignment(cw, w_set, wb_set)
            hw_tuple = tuple(hx)
            if "NOISE" in hx:
                noise_count += 1
            else:
                hex_words.add(hw_tuple)
                if check_standard_hexacode(hx):
                    pass_count += 1

        results.append({
            "w_patterns": sorted([list(p) for p in w_set], key=str),
            "pass_count": pass_count,
            "total": len(codewords),
            "pass_rate": Fraction(pass_count, len(codewords)),
            "noise_count": noise_count,
            "distinct_hex_words": len(hex_words),
            "w_set": w_set,
            "wb_set": wb_set,
        })

    results.sort(key=lambda r: r["pass_count"], reverse=True)
    return results


# ================================================================
# MODULE C:  LEAD 5 REFINED  --  BRUTE-FORCE CONSTRAINT DERIVATION
# ================================================================
"""
Instead of assuming the standard hexacode constraints, we DERIVE the
actual linear constraints from the code's GF(4) projections.

For each candidate coefficient vector a = (a_0,...,a_5) in GF(4)^6,
  check if  sum(a_i * h_i) = 0  for ALL hexacode words h in H.

Those a that pass form the constraint space (dual of H).

If H has GF(4)-dimension k, the constraint space has dimension 6-k.
For the standard hexacode, k=3, constraints=3.
"""


def derive_constraint_space(hex_words: List[Tuple[str, ...]]) -> List[List[str]]:
    """
    Brute-force derive all GF(4) linear constraints satisfied by
    the given hexacode words.  Returns list of constraint coefficient
    vectors (each a 6-element list of GF(4) element strings).
    """
    constraints = []

    for coeffs in product(_GF4_ELEMS, repeat=6):
        # Skip trivial zero constraint
        if all(c == "0" for c in coeffs):
            continue

        valid = True
        for hw in hex_words:
            s = gf4_dot(list(coeffs), list(hw))
            if s != "0":
                valid = False
                break

        if valid:
            constraints.append(list(coeffs))

    return constraints


def constraint_space_dimension(constraints: List[List[str]]) -> int:
    """
    Compute the GF(4)-dimension of the constraint space using
    Gaussian elimination over GF(4).
    Returns the number of independent constraints.
    """
    if not constraints:
        return 0

    # Convert to row-echelon form over GF(4)
    rows = [list(c) for c in constraints]
    n_cols = len(rows[0])
    pivot_cols = []

    for col in range(n_cols):
        # Find pivot
        pivot_row = None
        for r in range(len(rows)):
            if rows[r][col] != "0" and not any(
                rows[r][pc] != "0" for pc in pivot_cols
            ):
                pivot_row = r
                break

        if pivot_row is None:
            # Try any row not yet used as pivot
            for r in range(len(rows)):
                if rows[r][col] != "0":
                    used = any(rows[r][pc] != "0" for pc in pivot_cols)
                    if not used:
                        pivot_row = r
                        break

        if pivot_row is not None:
            pivot_cols.append(col)
            # Scale pivot row
            scale = rows[pivot_row][col]
            if scale != "1":
                inv = _gf4_inverse(scale)
                rows[pivot_row] = [gf4_mul(inv, x) for x in rows[pivot_row]]

            # Eliminate
            for r in range(len(rows)):
                if r != pivot_row and rows[r][col] != "0":
                    factor = rows[r][col]
                    rows[r] = [
                        gf4_add(rows[r][c], gf4_mul(factor, rows[pivot_row][c]))
                        for c in range(n_cols)
                    ]

    return len(pivot_cols)


def _gf4_inverse(a: str) -> str:
    """Multiplicative inverse in GF(4)."""
    if a == "0":
        return "NOISE"  # undefined
    if a == "1":
        return "1"
    if a == "W":
        return "W_BAR"  # W * W_BAR = 1
    if a == "W_BAR":
        return "W"  # W_BAR * W = 1
    return "NOISE"


def find_independent_constraints(constraints: List[List[str]],
                                   max_count: int = 5) -> List[List[str]]:
    """
    Extract a maximal independent set of constraints via GF(4) Gaussian
    elimination. Returns at most max_count independent constraints.
    """
    if not constraints:
        return []

    rows = [list(c) for c in constraints]
    n_cols = len(rows[0])
    independent = []
    pivot_cols = set()

    for row in rows:
        # Check if this row is independent of existing pivots
        reduced = list(row)
        is_new = False

        for pc in sorted(pivot_cols):
            if reduced[pc] != "0":
                factor = reduced[pc]
                pivot_row = None
                for ir in independent:
                    if ir[pc] == "1":
                        pivot_row = ir
                        break
                if pivot_row is None:
                    for ir in independent:
                        if ir[pc] != "0":
                            pivot_row = ir
                            inv = _gf4_inverse(ir[pc])
                            break
                if pivot_row is not None:
                    if pivot_row[pc] != "1":
                        inv = _gf4_inverse(pivot_row[pc])
                        scaled = [gf4_mul(inv, x) for x in pivot_row]
                    else:
                        scaled = pivot_row
                    reduced = [
                        gf4_add(reduced[c], gf4_mul(factor, scaled[c]))
                        for c in range(n_cols)
                    ]

        # Find leading non-zero column
        for c in range(n_cols):
            if reduced[c] != "0" and c not in pivot_cols:
                # Normalize so leading entry is 1
                if reduced[c] != "1":
                    inv = _gf4_inverse(reduced[c])
                    reduced = [gf4_mul(inv, x) for x in reduced]
                independent.append(reduced)
                pivot_cols.add(c)
                is_new = True
                break

        if len(independent) >= max_count:
            break

    return independent


def check_derived_constraints(hx: List[str],
                                constraints: List[List[str]]) -> bool:
    """Check if a hexacode word satisfies all derived constraints."""
    if "NOISE" in hx:
        return False
    for coeffs in constraints:
        if gf4_dot(coeffs, hx) != "0":
            return False
    return True


# ================================================================
# MODULE D:  LEAD 4 REFINED  --  ACTUAL AUTOMORPHISM DISCOVERY
# ================================================================
"""
Discover the actual automorphism group of our Golay code.

Method: test all 276 transpositions (i,j) for i<j in {0,...,23}.
A transposition is an automorphism iff swapping coordinates i and j
maps every codeword to another codeword.

Then generate the group from the transposition generators by closure.
"""


def discover_transposition_autos(codewords: List[List[int]],
                                   verbose: bool = True) -> List[Tuple[int, int]]:
    """
    Test all C(24,2)=276 transpositions.  Two-pass: sample then full.
    Returns list of (i,j) pairs that are code automorphisms.
    """
    cw_set = {tuple(cw) for cw in codewords}
    sample = random.sample(codewords, min(200, len(codewords)))

    candidates = []
    if verbose:
        print("  Pass 1: Quick test on 200-sample...")

    for i in range(24):
        for j in range(i + 1, 24):
            ok = True
            for cw in sample:
                s = cw[:]
                s[i], s[j] = s[j], s[i]
                if tuple(s) not in cw_set:
                    ok = False
                    break
            if ok:
                candidates.append((i, j))

    if verbose:
        print(f"    {len(candidates)} candidates from quick test")

    # Full verification
    autos = []
    if verbose:
        print("  Pass 2: Full verification on all 4096 codewords...")

    for idx, (i, j) in enumerate(candidates):
        full_ok = True
        for cw in codewords:
            s = cw[:]
            s[i], s[j] = s[j], s[i]
            if tuple(s) not in cw_set:
                full_ok = False
                break
        if full_ok:
            autos.append((i, j))

    if verbose:
        print(f"    {len(autos)} / 276 transpositions are true automorphisms")

    return autos


def build_auto_group(transpositions: List[Tuple[int, int]],
                      max_composite: int = 5,
                      verbose: bool = True) -> Set[Tuple[int, ...]]:
    """
    Build the automorphism group by composing transposition generators.
    Returns the set of all permutations (as tuples) generated.
    """
    identity = tuple(range(24))
    group = {identity}
    frontier = [list(identity)]

    for depth in range(max_composite):
        new_frontier = []
        for perm in frontier:
            for (i, j) in transpositions:
                new_perm = perm[:]
                new_perm[i], new_perm[j] = new_perm[j], new_perm[i]
                key = tuple(new_perm)
                if key not in group:
                    group.add(key)
                    new_frontier.append(new_perm)
        if verbose:
            print(f"    Depth {depth + 1}: +{len(new_frontier)} new, "
                  f"total |G| = {len(group)}")
        if not new_frontier:
            break
        frontier = new_frontier

    return group


def test_auto_hodge_preservation(codewords: List[List[int]],
                                   group: Set[Tuple[int, ...]],
                                   sample_size: int = 50,
                                   max_perms_tested: int = 100) -> Dict:
    """
    Test whether discovered automorphisms preserve Hodge structure
    (NOISE count, holomorphic balance, hexacode membership).
    """
    sample = random.sample(codewords, min(sample_size, len(codewords)))
    perms_to_test = list(group)[:max_perms_tested]
    # Remove identity
    perms_to_test = [p for p in perms_to_test if p != tuple(range(24))]

    noise_ok = 0
    balance_ok = 0
    weight_ok = 0
    total = 0

    for cw in sample:
        orig_hex = project_to_hexacode(cw)
        orig_m = holomorphic_balance(orig_hex)
        orig_wt = sum(cw)

        for perm in perms_to_test:
            mapped = [cw[perm[i]] for i in range(24)]
            mapped_hex = project_to_hexacode(mapped)
            mapped_m = holomorphic_balance(mapped_hex)

            total += 1
            if mapped_m["NOISE"] == orig_m["NOISE"]:
                noise_ok += 1
            if mapped_m["balance"] == orig_m["balance"]:
                balance_ok += 1
            if sum(mapped) == orig_wt:
                weight_ok += 1

    return {
        "automorphisms_tested": len(perms_to_test),
        "codewords_tested": len(sample),
        "total_checks": total,
        "noise_preserved": noise_ok,
        "noise_rate": Fraction(noise_ok, total) if total else Fraction(0),
        "balance_preserved": balance_ok,
        "balance_rate": Fraction(balance_ok, total) if total else Fraction(0),
        "weight_preserved": weight_ok,
        "weight_rate": Fraction(weight_ok, total) if total else Fraction(0),
    }


# ================================================================
# MODULE E:  DHC REFINED  --  VERIFICATION WITH DERIVED CONSTRAINTS
# ================================================================
"""
The Discrete Hodge Conjecture (Refined):

  DEFINITION: A 24-bit vector S is a "Hodge class" iff:
    (H1) NOISE(S) = 0  (MOG-aligned GF(4) projection has no NOISE columns)
    (H2) hex(S) satisfies the DERIVED hexacode constraints

  DHC-REFINED:
    (Forward)  Every algebraic cycle (codeword) is a Hodge class.
    (Converse) Every Hodge class is an algebraic cycle (codeword).

  If both hold, NOISE=0 + derived-constraints PERFECTLY CHARACTERISES
  algebraic cycles -- the discrete analog of the Hodge Conjecture.
"""


def dhc_refined_forward(codewords: List[List[int]],
                          w_set: FrozenSet, wb_set: FrozenSet,
                          constraints: List[List[str]]) -> Dict:
    """
    DHC Forward: every codeword should be a Hodge class.
    Tests all 4096 codewords.
    """
    fwd_pass = 0
    fail_noise = 0
    fail_constraints = 0
    failures = []

    for cw in codewords:
        hx = project_with_assignment(cw, w_set, wb_set)
        has_noise = "NOISE" in hx
        sat = check_derived_constraints(hx, constraints) if not has_noise else False

        if not has_noise and sat:
            fwd_pass += 1
        else:
            if has_noise:
                fail_noise += 1
            else:
                fail_constraints += 1
            if len(failures) < 5:
                failures.append({
                    "cw": cw,
                    "hex": hx,
                    "reason": "NOISE" if has_noise else "constraints",
                })

    return {
        "total": len(codewords),
        "pass": fwd_pass,
        "fail_noise": fail_noise,
        "fail_constraints": fail_constraints,
        "rate": Fraction(fwd_pass, len(codewords)),
        "failures_sample": failures,
    }


def dhc_refined_converse(codewords: List[List[int]],
                           w_set: FrozenSet, wb_set: FrozenSet,
                           constraints: List[List[str]],
                           sample_size: int = 500000) -> Dict:
    """
    DHC Converse: every Hodge class should be a codeword.
    Tests on a large random sample of 24-bit vectors.
    """
    cw_set = {tuple(cw) for cw in codewords}
    hodge_count = 0
    in_code_count = 0
    counterexamples = []

    for _ in range(sample_size):
        vec = [random.randint(0, 1) for _ in range(24)]
        hx = project_with_assignment(vec, w_set, wb_set)
        if "NOISE" in hx:
            continue
        if not check_derived_constraints(hx, constraints):
            continue
        hodge_count += 1
        if tuple(vec) in cw_set:
            in_code_count += 1
        elif len(counterexamples) < 20:
            counterexamples.append({
                "vec": vec,
                "hex": hx,
                "weight": sum(vec),
            })

    return {
        "sample_size": sample_size,
        "hodge_class_count": hodge_count,
        "in_code_count": in_code_count,
        "counterexample_count": hodge_count - in_code_count,
        "rate": Fraction(in_code_count, hodge_count) if hodge_count else None,
        "dhc_holds": (in_code_count == hodge_count),
        "counterexamples_sample": counterexamples[:5],
    }


def dhc_exhaustive_converse(codewords: List[List[int]],
                               w_set: FrozenSet, wb_set: FrozenSet,
                               constraints: List[List[str]]) -> Dict:
    """
    Exhaustive DHC converse test: scan ALL 2^24 = 16,777,216 vectors.
    Takes ~60-120 seconds.  The definitive test.
    """
    cw_set = {tuple(cw) for cw in codewords}
    hodge_count = 0
    in_code_count = 0
    counterexamples = []
    total = 1 << 24

    for n in range(total):
        vec = [(n >> i) & 1 for i in range(24)]
        hx = project_with_assignment(vec, w_set, wb_set)
        if "NOISE" in hx:
            continue
        if not check_derived_constraints(hx, constraints):
            continue
        hodge_count += 1
        if tuple(vec) in cw_set:
            in_code_count += 1
        elif len(counterexamples) < 20:
            counterexamples.append(vec)

        if (n + 1) % 2_000_000 == 0:
            pct = (n + 1) / total * 100
            ce = hodge_count - in_code_count
            print(f"    ... {pct:.0f}%  (Hodge: {hodge_count}, "
                  f"in code: {in_code_count}, counterexamples: {ce})")

    return {
        "total_vectors": total,
        "hodge_class_count": hodge_count,
        "in_code_count": in_code_count,
        "counterexample_count": hodge_count - in_code_count,
        "dhc_holds": (in_code_count == hodge_count),
        "counterexamples_sample": counterexamples[:5],
    }


# ================================================================
# MODULE F:  HODGE DIAMOND  ANALYSIS  (from v2, reused)
# ================================================================


def compute_hodge_tensor(vec: List[int]) -> List[List[Fraction]]:
    """4x4 NRCI Hodge tensor from sextet weights."""
    sextets = [vec[i:i + 6] for i in range(0, 24, 6)]
    weights = [sum(s) for s in sextets]
    tensor = []
    for p in range(4):
        row = []
        for q in range(4):
            diff = abs(weights[p] - weights[q])
            row.append(Fraction(6 - diff, 6))
        tensor.append(row)
    return tensor


def diagonalization_ratio(tensor: List[List[Fraction]]) -> Fraction:
    """Measure (p,p) diagonal concentration."""
    diag_sum = sum(tensor[i][i] for i in range(4))
    off_sum = sum(tensor[p][q] for p in range(4) for q in range(4) if p != q)
    total = diag_sum + off_sum
    if total == 0:
        return Fraction(0)
    return diag_sum / total


# ================================================================
# MODULE G:  MASTER  EXPERIMENT  RUNNER  --  PUSH 2
# ================================================================


def run_push2():
    """
    Master runner for the Lead 4/5/DHC refinement push.
    Five phases:
      Phase A: Code generation + MOG alignment
      Phase B: Lead 5 -- GF(4) Assignment Search
      Phase C: Lead 5 -- Derived Constraint Space
      Phase D: Lead 4 -- Automorphism Discovery
      Phase E: DHC -- Refined Verification
    """
    print("=" * 72)
    print("TGIC_v2  PUSH 2:  Lead 4 / Lead 5 / DHC  Refinement")
    print('"Failure is direction, not defeat."  -- UBP Research Principle')
    print("=" * 72)

    # ── Phase A: Code + MOG ──
    print("\n[PHASE A] Golay Code Generation + MOG Alignment")
    print("-" * 50)
    codewords = get_all_codewords()
    octads = get_octads()
    print(f"  Codewords: {len(codewords)}  Octads: {len(octads)}")

    # Auto-hunt MOG key
    key = auto_hunt_mog_key(codewords, seed=42, max_iter=8000)
    print(f"  MOG key: {key}")

    # Quick NOISE verification
    noise_total = 0
    for cw in codewords:
        hx = project_to_hexacode(cw)
        noise_total += hx.count("NOISE")
    print(f"  Total NOISE across all codewords: {noise_total}  (expect 0)")

    # ── Phase B: GF(4) Assignment Search ──
    print("\n[PHASE B] Lead 5 Refinement: GF(4) Assignment Search")
    print("-" * 50)
    print("  Searching all 20 W/W_BAR splits of 6 weight-2 patterns...")
    results = search_gf4_assignments(codewords)

    print(f"\n  RESULTS (sorted by pass count, top 5):")
    for rank, r in enumerate(results[:5]):
        print(f"    #{rank + 1}: pass={r['pass_count']}/{r['total']} "
              f"({float(r['pass_rate']) * 100:.1f}%)  "
              f"distinct_hex={r['distinct_hex_words']}  "
              f"noise_cw={r['noise_count']}  "
              f"W={r['w_patterns']}")

    best = results[0]
    w_set_best = best["w_set"]
    wb_set_best = best["wb_set"]

    if best["pass_count"] == len(codewords):
        print(f"\n  >>> PERFECT MATCH: assignment #{1} gives 4096/4096!")
        print(f"  >>> Standard hexacode constraints work with this assignment.")
    else:
        print(f"\n  >>> Best assignment: {best['pass_count']}/4096 "
              f"({float(best['pass_rate']) * 100:.1f}%)")
        print(f"  >>> Standard hexacode constraints do NOT fully characterise.")
        print(f"  >>> Proceeding to brute-force constraint derivation...")

    # Collect hexacode words with best assignment
    all_hex_words = set()
    for cw in codewords:
        hx = project_with_assignment(cw, w_set_best, wb_set_best)
        if "NOISE" not in hx:
            all_hex_words.add(tuple(hx))
    all_hex_list = sorted(all_hex_words)

    print(f"\n  With best assignment: {len(all_hex_words)} distinct hexacode words")
    print(f"  (Standard hexacode C_6 has 64 words)")

    # ── Phase C: Derived Constraint Space ──
    print("\n[PHASE C] Lead 5 Refinement: Brute-Force Constraint Derivation")
    print("-" * 50)
    print(f"  Searching 4^6 = 4096 candidate constraint vectors...")
    print(f"  Against {len(all_hex_list)} distinct hexacode words...")

    constraints = derive_constraint_space(all_hex_list)
    print(f"  Found {len(constraints)} total constraint vectors")

    # Get independent constraints
    indep = find_independent_constraints(constraints, max_count=6)
    dim = len(indep)
    print(f"  Independent constraints (GF(4)-dimension): {dim}")

    for i, c in enumerate(indep):
        print(f"    C{i + 1}: {c}")
        # Show what this constraint means in words
        nonzero = [(j, c[j]) for j in range(6) if c[j] != "0"]
        terms = " + ".join(f"{v}*h{j}" for j, v in nonzero)
        print(f"         {terms} = 0")

    # Cross-check: how many codewords satisfy derived constraints?
    print(f"\n  Cross-check: applying derived constraints to all codewords...")
    derived_pass = 0
    for cw in codewords:
        hx = project_with_assignment(cw, w_set_best, wb_set_best)
        if "NOISE" not in hx and check_derived_constraints(hx, indep):
            derived_pass += 1
    print(f"  Codewords passing derived constraints: {derived_pass} / {len(codewords)}")

    if derived_pass == len(codewords):
        print(f"  >>> ALL 4096 codewords satisfy the derived constraints.")
    else:
        print(f"  >>> WARNING: {len(codewords) - derived_pass} codewords FAIL.")
        print(f"  >>> The derived constraints are too restrictive.")
        print(f"  >>> Need to re-examine the GF(4) assignment.")

    # ── Phase D: Automorphism Discovery ──
    print("\n[PHASE D] Lead 4 Refinement: Actual Automorphism Discovery")
    print("-" * 50)
    random.seed(99)
    trans_autos = discover_transposition_autos(codewords)
    print(f"  Transposition automorphisms: {len(trans_autos)} / 276")

    if trans_autos:
        # Build group
        group = build_auto_group(trans_autos, max_composite=5)
        print(f"  Generated group size: |G| = {len(group)}")
        print(f"  (M_24 has order 244,823,040)")

        # Hodge preservation test
        print(f"\n  Testing Hodge structure preservation...")
        hodge_test = test_auto_hodge_preservation(codewords, group,
                                                   sample_size=30,
                                                   max_perms_tested=100)
        print(f"    Checks: {hodge_test['total_checks']}")
        print(f"    NOISE preserved: {hodge_test['noise_ok']}/{hodge_test['total_checks']} "
              f"({float(hodge_test['noise_rate']) * 100:.1f}%)")
        print(f"    Balance preserved: {hodge_test['balance_ok']}/{hodge_test['total_checks']} "
              f"({float(hodge_test['balance_rate']) * 100:.1f}%)")
        print(f"    Weight preserved: {hodge_test['weight_ok']}/{hodge_test['total_checks']} "
              f"({float(hodge_test['weight_rate']) * 100:.1f}%)")

        if float(hodge_test['noise_rate']) == 100.0:
            print(f"  >>> ALL automorphisms preserve Hodge structure!")
        else:
            print(f"  >>> Some automorphisms do NOT preserve Hodge structure.")
            print(f"  >>> The GF(4) assignment may need adjustment for full M_24 action.")
    else:
        print(f"  >>> NO transposition automorphisms found.")
        print(f"  >>> The code's automorphism group is not generated by transpositions.")
        print(f"  >>> Need higher-order permutation generators.")
        group = set()

    # ── Phase E: DHC Refined Verification ──
    print("\n" + "#" * 72)
    print("[PHASE E] DISCRETE HODGE CONJECTURE  --  REFINED VERIFICATION")
    print("#" * 72)

    if derived_pass < len(codewords):
        print("\n  *** Cannot proceed: derived constraints don't cover all codewords.")
        print("  *** The GF(4) assignment needs further investigation.")
        print("  *** This IS the direction -- we've identified the precise failure.")
        print("\n  DIRECTION: The mapping from 4-bit columns to GF(4) elements")
        print("  is not a homomorphism. The hexacode words of codewords")
        print("  may not form a linear subspace for ANY W/W_BAR assignment.")
        print("  This suggests the discrete Hodge structure requires a")
        print("  RICHER algebraic object than GF(4)^6.")
    else:
        # Forward test
        print(f"\n  DHC-Refined Forward: codeword => Hodge class?")
        fwd = dhc_refined_forward(codewords, w_set_best, wb_set_best, indep)
        print(f"    Result: {fwd['pass']} / {fwd['total']}  "
              f"({float(fwd['rate']) * 100:.1f}%)")
        if fwd["fail_noise"] > 0:
            print(f"    Failed (NOISE): {fwd['fail_noise']}")
        if fwd["fail_constraints"] > 0:
            print(f"    Failed (constraints): {fwd['fail_constraints']}")

        # Converse test (sample)
        print(f"\n  DHC-Refined Converse: Hodge class => codeword?")
        print(f"    (Testing 500,000 random vectors...)")
        random.seed(777)
        conv = dhc_refined_converse(codewords, w_set_best, wb_set_best,
                                     indep, sample_size=500000)
        print(f"    Vectors with NOISE=0 + constraints: {conv['hodge_class_count']}")
        print(f"    Of those in Golay code: {conv['in_code_count']}")
        print(f"    Counterexamples: {conv['counterexample_count']}")
        if conv['rate'] is not None:
            print(f"    Converse rate: {float(conv['rate']) * 100:.1f}%")

        if conv["dhc_holds"]:
            print(f"\n    >>> DHC CONVERSE HOLDS ON SAMPLE! <<<")
            print(f"    >>> Recommending EXHAUSTIVE test for definitive proof.")
            print(f"    >>> Run: python tgic_v2_push2.py exhaustive_dhc")
        else:
            print(f"\n    >>> DHC converse FAILS on sample.")
            print(f"    >>> {conv['counterexample_count']} counterexamples found.")
            print(f"    >>> NOISE=0 + derived-constraints is NECESSARY but not SUFFICIENT.")
            if conv["counterexamples_sample"]:
                print(f"\n    Sample counterexample:")
                ce = conv["counterexamples_sample"][0]
                print(f"      vec = {ce['vec']}")
                print(f"      hex = {ce['hex']}")
                print(f"      weight = {ce['weight']}")

    # ── SUMMARY ──
    print("\n" + "=" * 72)
    print("PUSH 2  SUMMARY")
    print("=" * 72)
    print(f"  Lead 5 (GF(4) Assignment):")
    print(f"    Best standard-constraint pass rate: {best['pass_count']}/{best['total']}")
    print(f"    Distinct hexacode words: {len(all_hex_words)}")
    print(f"    Derived constraint dimension: {dim}")
    print(f"    Codewords satisfying derived constraints: {derived_pass}/4096")
    print(f"")
    print(f"  Lead 4 (Automorphisms):")
    print(f"    Transposition autos: {len(trans_autos)}/276")
    group_size = len(group) if trans_autos else 0
    print(f"    Generated group |G|: {group_size}")
    if trans_autos:
        print(f"    Hodge preservation: NOISE={float(hodge_test['noise_rate'])*100:.1f}% "
              f"Balance={float(hodge_test['balance_rate'])*100:.1f}%")
    print(f"")
    print(f"  DHC (Discrete Hodge Conjecture):")
    if derived_pass == len(codewords):
        fwd_ok = "PROVEN" if fwd["pass"] == len(codewords) else "PARTIAL"
        conv_ok = "HOLDS" if ("conv" in dir() and conv["dhc_holds"]) else "FAILS"
        print(f"    Forward: {fwd_ok}")
        print(f"    Converse: {conv_ok}")
    else:
        print(f"    BLOCKED: derived constraints don't cover all codewords")
        print(f"    This is the KEY DIRECTION for next push.")
    print(f"")
    print(f"  WHAT'S NEXT:")
    if derived_pass < len(codewords):
        print(f"    1. Investigate WHY the GF(4) mapping isn't a homomorphism.")
        print(f"       The 4-bit-column-to-GF(4) map is inherently non-linear.")
        print(f"       Direction: find a LINEAR projection GF(2)^24 -> GF(4)^6")
        print(f"       that restricts to an isomorphism on the code.")
        print(f"    2. Alternative: work in GF(2)^12 directly (forget GF(4))")
        print(f"       and find the constraint space there.")
        print(f"    3. The failure itself is informative: it tells us the")
        print(f"       Hodge structure of the Golay code is more subtle")
        print(f"       than a simple GF(4)^6 linear subspace.")
    else:
        if "conv" in dir() and conv["dhc_holds"]:
            print(f"    1. Run EXHAUSTIVE DHC (all 2^24 vectors) for proof.")
            print(f"    2. Formalize the discrete Hodge theorem.")
            print(f"    3. Connect back to continuous Hodge Conjecture.")
        else:
            print(f"    1. Analyze the counterexamples -- what extra structure")
            print(f"       do codewords have that Hodge-classes lack?")
            print(f"    2. The gap between necessary and sufficient is the")
            print(f"       discrete analog of the Hodge conjecture's difficulty.")
            print(f"    3. Consider higher-order invariants (weight, orbit structure)")
            print(f"       as additional filters.")

    print(f"")
    print(f"  'Failure is direction, not defeat.'  -- UBP Research Principle")
    print("=" * 72)

    return {
        "best_assignment": best,
        "derived_constraints": indep,
        "constraint_dimension": dim,
        "transposition_autos": trans_autos,
        "group_size": group_size if 'group' in dir() else 0,
    }


def run_exhaustive_dhc():
    """Run the exhaustive DHC converse test (all 2^24 vectors)."""
    print("=" * 72)
    print("EXHAUSTIVE DHC CONVERSE TEST  (2^24 = 16,777,216 vectors)")
    print("=" * 72)

    codewords = get_all_codewords()
    key = auto_hunt_mog_key(codewords, seed=42, max_iter=8000)

    # Use best GF(4) assignment
    results = search_gf4_assignments(codewords)
    best = results[0]
    w_set = best["w_set"]
    wb_set = best["wb_set"]

    # Collect hexacode words and derive constraints
    all_hex = set()
    for cw in codewords:
        hx = project_with_assignment(cw, w_set, wb_set)
        if "NOISE" not in hx:
            all_hex.add(tuple(hx))
    all_hex_list = sorted(all_hex)

    constraints = derive_constraint_space(all_hex_list)
    indep = find_independent_constraints(constraints, max_count=6)

    print(f"  Assignment pass rate: {best['pass_count']}/4096")
    print(f"  Distinct hex words: {len(all_hex_list)}")
    print(f"  Derived constraints: {indep}")
    print(f"  Starting exhaustive scan...\n")

    result = dhc_exhaustive_converse(codewords, w_set, wb_set, indep)

    print(f"\n{'#' * 72}")
    print(f"  EXHAUSTIVE DHC RESULT:")
    print(f"    Total vectors scanned: {result['total_vectors']:,}")
    print(f"    Hodge classes found: {result['hodge_class_count']}")
    print(f"    In Golay code: {result['in_code_count']}")
    print(f"    Counterexamples: {result['counterexample_count']}")
    print(f"    DHC HOLDS: {result['dhc_holds']}")
    if result['counterexamples_sample']:
        print(f"    Sample counterexample: {result['counterexamples_sample'][0]}")
    print(f"{'#' * 72}")

    return result


# ================================================================
# MODULE H:  DEEPER ANALYSIS  --  WHY THE MAPPING ISN'T A HOMOMORPHISM
# ================================================================
"""
When the GF(4) assignment search and constraint derivation reveal that
no standard-constraint assignment gives 4096/4096, we investigate WHY.

The root cause: the map from a 4-bit column to GF(4) is NOT linear.
It's a CLASSIFICATION (weight-based), not a homomorphism.

To get a LINEAR projection, we need to map each 4-bit column to a
pair of bits (GF(2)^2, i.e., a GF(4) element represented linearly).

The standard MOG construction uses a specific linear map:
  column (a, b, c, d) -> (a, b+c, a+b+d)  or similar.

We search for the linear map that makes the hexacode words linear.
"""


def search_linear_hexacode_map(codewords: List[List[int]]) -> Dict:
    """
    Search for a LINEAR map GF(2)^24 -> GF(4)^6 (equivalently
    GF(2)^24 -> GF(2)^12) that maps the Golay code to a linear
    subspace of GF(2)^12.

    The map has the form: for each MOG column i (4 bits), compute
    2 linear functions of the 4 bits to get 2 output bits.

    We parametrize the map for column i as:
      f_i(b0, b1, b2, b3) = (c00*b0 + c01*b1 + c02*b2 + c03*b3,
                               c10*b0 + c11*b1 + c12*b2 + c13*b3)
    where c_xy in GF(2) and the 8 coefficients per column define the map.

    Total parameters: 6 columns * 8 params = 48 bits.
    Exhaustive search is 2^48 -- infeasible.

    Instead, we use a STRUCTURED search: the map must be invertible
    on each column (so the 2 output bits determine the column pattern
    up to the kernel).  We restrict to maps of the form:
      (b0, b1, b2, b3) -> (b0, f(b1, b2, b3))
    where f is a linear function of 3 bits: 8 possibilities.
    Total: 8^6 = 262,144 -- feasible.

    For each such map, we check if the image of the code is a
    linear subspace of GF(2)^12, and if so, its dimension.
    """
    # Generate the MOG-aligned codewords
    aligned = [apply_mog_permutation(cw) for cw in codewords]

    # For each column, the 4 bits are (row0, row1, row2, row3)
    # Map: (b0, b1, b2, b3) -> (b0, L(b1,b2,b3))
    # where L is one of 8 linear functions of 3 bits.
    # L is determined by 3 coefficients (a1, a2, a3) in GF(2)^3.

    def column_map(col_bits, a1, a2, a3):
        """Map 4-bit column to 2-bit GF(4) representation."""
        b0, b1, b2, b3 = col_bits
        out0 = b0
        out1 = (a1 * b1 + a2 * b2 + a3 * b3) % 2
        return (out0, out1)

    def full_map(vec, col_params):
        """Map 24-bit MOG vector to 12-bit GF(2) vector."""
        cols = [[vec[i], vec[i + 6], vec[i + 12], vec[i + 18]]
                for i in range(6)]
        out = []
        for i, c in enumerate(cols):
            a1, a2, a3 = col_params[i]
            pair = column_map(c, a1, a2, a3)
            out.extend(pair)
        return tuple(out)

    # Convert aligned codewords to column form
    cw_cols = []
    for cw in aligned:
        cols = [[cw[i], cw[i + 6], cw[i + 12], cw[i + 18]]
                for i in range(6)]
        cw_cols.append(cols)

    best_map = None
    best_dim = -1
    best_params = None
    total_searched = 0

    print("  Searching 8^6 = 262,144 linear map candidates...")

    # Full search over all 8^6 = 262,144 column param combinations
    from itertools import product as iprod

    for params in iprod(range(8), repeat=6):
        col_params = []
        for p in params:
            a1 = (p >> 2) & 1
            a2 = (p >> 1) & 1
            a3 = p & 1
            col_params.append((a1, a2, a3))

        # Compute image of all codewords under this map
        image_set = set()
        for cols in cw_cols:
            out = []
            for i, c in enumerate(cols):
                a1, a2, a3 = col_params[i]
                pair = column_map(c, a1, a2, a3)
                out.extend(pair)
            image_set.add(tuple(out))

        # Check if image is a linear subspace
        # Quick test: 0 vector should be in image, and
        # for any two elements, their XOR should also be in image
        img_list = list(image_set)
        is_linear = True
        img_set_fast = set(img_list)

        # Check closure under XOR (sample-based for speed)
        zero = tuple([0] * 12)
        if zero not in img_set_fast:
            is_linear = False
        else:
            # Sample 50 pairs
            sample_size = min(50, len(img_list))
            sample_idx = random.sample(range(len(img_list)), sample_size)
            for ii in range(sample_size):
                for jj in range(ii + 1, sample_size):
                    xored = tuple(a ^ b for a, b in
                                   zip(img_list[sample_idx[ii]],
                                       img_list[sample_idx[jj]]))
                    if xored not in img_set_fast:
                        is_linear = False
                        break
                if not is_linear:
                    break

        if is_linear and len(image_set) > best_dim:
            # Compute GF(2) dimension
            # The image is a GF(2)-linear subspace.  Find its dimension
            # by building a basis via Gaussian elimination.
            basis = []
            for v in img_list:
                w = list(v)
                for b in basis:
                    for k in range(12):
                        if w[k]:
                            w = [w[j] ^ b[j] for j in range(12)]
                            break
                if any(w):
                    basis.append(w)

            dim = len(basis)
            if dim > best_dim:
                best_dim = dim
                best_map = image_set
                best_params = col_params
                total_searched += 1

                if total_searched <= 10 or dim >= 6:
                    print(f"    Map params: {col_params}  "
                          f"|image|={len(image_set)}  dim={dim}")

    print(f"\n  Total maps searched: 262,144")
    print(f"  Best linear image dimension: {best_dim} / 12")
    if best_params:
        print(f"  Best column params: {best_params}")
        print(f"  Best image size: {len(best_map)}")
        print(f"  (Golay code dim over GF(2) = 12, "
              f"hexacode dim over GF(4) = 3 = 6 over GF(2))")

    return {
        "best_dimension": best_dim,
        "best_params": best_params,
        "best_image_size": len(best_map) if best_map else 0,
        "maps_searched": 262144,
    }


# ================================================================
# MAIN ENTRY POINT
# ================================================================

if __name__ == "__main__":
    if len(sys.argv) > 1:
        arg = sys.argv[1].lower()
        if arg == "exhaustive_dhc":
            run_exhaustive_dhc()
        elif arg == "linear_search":
            print("=== Deep Analysis: Linear Hexacode Map Search ===")
            codewords = get_all_codewords()
            auto_hunt_mog_key(codewords, seed=42, max_iter=8000)
            result = search_linear_hexacode_map(codewords)
            print(f"\n  Result: {result}")
        elif arg == "assignment_search":
            print("=== Lead 5: GF(4) Assignment Search ===")
            codewords = get_all_codewords()
            auto_hunt_mog_key(codewords, seed=42, max_iter=8000)
            results = search_gf4_assignments(codewords)
            for i, r in enumerate(results[:10]):
                print(f"  #{i + 1}: pass={r['pass_count']}/4096  "
                      f"hex_words={r['distinct_hex_words']}  "
                      f"noise_cw={r['noise_count']}")
                print(f"       W = {r['w_patterns']}")
        elif arg == "auto_discover":
            print("=== Lead 4: Automorphism Discovery ===")
            codewords = get_all_codewords()
            auto_hunt_mog_key(codewords, seed=42, max_iter=8000)
            autos = discover_transposition_autos(codewords)
            print(f"  Automorphisms: {autos}")
            if autos:
                group = build_auto_group(autos)
                print(f"  Group size: {len(group)}")
        else:
            print(f"Usage: python tgic_v2_push2.py [push2|exhaustive_dhc|"
                  f"linear_search|assignment_search|auto_discover]")
    else:
        run_push2()
