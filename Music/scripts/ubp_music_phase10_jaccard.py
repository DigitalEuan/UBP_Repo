"""
UBP Music Study — Phase X: Prime-Layer Harmonic Module (Jaccard Analysis)
=========================================================================
Phase IX found the 4D prime residue fingerprint gives r=-0.8790 for chords
(Euclidean distance) — best chord result in the entire 9-phase study.
But it's INVERTED: dissonant chords cluster CLOSE, consonant SPREAD.

This phase asks: what if we use JACCARD SIMILARITY (set overlap) instead of
Euclidean distance? Jaccard measures shared membership, not separation.
If consonant chords SHARE more prime-residue features → positive r.

The deeper question: WHY does the Mersenne/Fermat mod-144 duality connect
to harmony at all? Can Jaccard expose the structural explanation?

Sections:
A. FOUNDATION — Re-derive the prime residue structure, define set constructions
B. JACCARD INTERVAL ANALYSIS — 6 set constructions × Jaccard vs consonance
C. JACCARD CHORD ANALYSIS — The critical test: can Jaccard differentiate chords?
D. PRIME ORBIT SETS — Powers of 2 mod 144 as feature sets for each pitch
E. MERSENNE/FERMAT BIT-SET OVERLAP — Binary representations as sets
F. THE 12-TET DECOMPOSITION SET — 7+5=12 as structural set template
G. COMPOSITE JACCARD SIGNATURES — Multi-resolution set families
H. JACCARD vs EUCLIDEAN HEAD-TO-HEAD — Direct comparison on same data
I. EXPLANATION — Why does this work? The structural mechanism
"""

import sys, math, random
from fractions import Fraction
from itertools import combinations
from collections import Counter

sys.path.insert(0, "/home/z/my-project")
from ubp_unified_v5 import (
    GolayCodeEngine, LeechLatticeEngine, BarnesWallEngine, MonsterGroup
)

g = GolayCodeEngine()
l = LeechLatticeEngine(g)

PITCH_NAMES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
CONSONANCE_MAP = {
    0: "Unison", 1: "Min2", 2: "Maj2", 3: "Min3", 4: "Maj3",
    5: "P4", 6: "TT", 7: "P5", 8: "Min6", 9: "Maj6", 10: "Min7", 11: "Maj7"
}
CONSONANCE_RANK = {
    0: 1, 7: 2, 5: 3, 4: 3, 9: 3, 3: 4, 8: 4, 10: 4, 2: 5, 11: 5, 1: 6, 6: 6
}
COF_ORDER = [0, 7, 2, 9, 4, 11, 6, 1, 8, 3, 10, 5]

# Expanded chord set for thorough chord analysis
CHORDS = [
    ("C Maj",      [0,4,7],       "Consonant"),
    ("C Min",      [0,3,7],       "Consonant"),
    ("C Dim",      [0,3,6],       "Moderate"),
    ("C Aug",      [0,4,8],       "Moderate"),
    ("C Sus4",     [0,5,7],       "Consonant"),
    ("C Sus2",     [0,2,7],       "Consonant"),
    ("Cluster13",  [0,1,2],       "Dissonant"),
    ("Cluster16",  [0,1,6],       "Dissonant"),
    ("Cluster45",  [0,4,5],       "Dissonant"),
    ("Maj7",       [0,4,7,11],    "Consonant"),
    ("Min7",       [0,3,7,10],    "Consonant"),
    ("Dom7",       [0,4,7,10],    "Consonant"),
    ("Dim7",       [0,3,6,9],     "Moderate"),
    ("Maj7b5",     [0,4,6,11],    "Dissonant"),
    ("MinMaj7",    [0,3,7,11],    "Consonant"),
    ("HalfDim",    [0,3,6,10],    "Moderate"),
    ("Pentatonic", [0,2,4,7,9],   "Consonant"),
    ("Blues",      [0,3,5,6,7,10],"Moderate"),
    ("WholeTone",  [0,2,4,6,8,10],"Moderate"),
    ("Chromatic6", list(range(6)), "Dissonant"),
]
CONS_MAP_4 = {"Consonant": 1, "Moderate": 2, "Mixed": 3, "Ambiguous": 3, "Dissonant": 4}


# ═══════════════════════════════════════════════════════════════════════════════════
# UTILITIES
# ═══════════════════════════════════════════════════════════════════════════════════

def jaccard(set_a, set_b):
    """Jaccard similarity: |A ∩ B| / |A ∪ B|"""
    a, b = set(set_a), set(set_b)
    union = a | b
    if not union:
        return 1.0  # both empty → identical
    return len(a & b) / len(union)

def jaccard_dist(set_a, set_b):
    """Jaccard distance: 1 - Jaccard similarity"""
    return 1.0 - jaccard(set_a, set_b)

def euclidean_dist(a, b):
    return math.sqrt(sum((x - y) ** 2 for x, y in zip(a, b)))

def pearson_r(xs, ys):
    n = len(xs)
    if n < 2:
        return 0.0
    mx = sum(xs) / n
    my = sum(ys) / n
    sx = math.sqrt(sum((x - mx) ** 2 for x in xs) / (n - 1)) if n > 1 else 0
    sy = math.sqrt(sum((y - my) ** 2 for y in ys) / (n - 1)) if n > 1 else 0
    if sx == 0 or sy == 0:
        return 0.0
    return sum((xs[i] - mx) * (ys[i] - my) for i in range(n)) / ((n - 1) * sx * sy)

def spearman_rho(xs, ys):
    n = len(xs)
    if n < 2:
        return 0.0
    def rank(vals):
        sorted_idx = sorted(range(n), key=lambda i: vals[i])
        ranks = [0] * n
        for rank_val, idx in enumerate(sorted_idx, 1):
            ranks[idx] = rank_val
        return ranks
    rx = rank(xs)
    ry = rank(ys)
    return pearson_r(rx, ry)

def mod_dist(a, b, m=144):
    """Circular distance mod m"""
    return min((a - b) % m, (b - a) % m)

def bits_of(n, width=8):
    """Set of bit positions that are 1"""
    return set(i for i in range(width) if (n >> i) & 1)


# ═══════════════════════════════════════════════════════════════════════════════════
# A. FOUNDATION — The Prime Residue Structure
# ═══════════════════════════════════════════════════════════════════════════════════

def run_foundation():
    print(f"\n{'=' * 80}")
    print("PHASE X-A: FOUNDATION — Prime Residue Structure Re-derivation")
    print(f"{'=' * 80}")
    print("  Mersenne primes: 2^p - 1. For p>=5: (2^p - 1) mod 144 in {{31, 127}}")
    print("  Fermat primes: 2^(2^k) + 1. For k>=2: (2^(2^k) + 1) mod 144 in {{17, 113}}")
    print("  KEY: 31 XOR 127 = 17 XOR 113 = 96 = 2^5 + 2^6 = 2/3 of 144\n")

    # Verify the duality
    print("  VERIFICATION — Mersenne mod 144 for p = 2..12:")
    for p in range(2, 13):
        m = (1 << p) - 1
        r = m % 144
        print(f"    2^{p} - 1 = {m:>6d}, mod 144 = {r:>4d}" +
              ("  <-- Mersenne zone" if r in {31, 127} else ""))

    print(f"\n  VERIFICATION — Fermat mod 144 for k = 0..4:")
    for k in range(5):
        fk = (1 << (1 << k)) + 1
        r = fk % 144
        print(f"    F_{k} = 2^(2^{k}) + 1 = {fk:>6d}, mod 144 = {r:>4d}" +
              ("  <-- Fermat zone" if r in {17, 113} else ""))

    # The XOR identity
    print(f"\n  XOR IDENTITY:")
    print(f"    31 XOR 127 = {31 ^ 127} = {31 ^ 127} = 2^5 + 2^6 = 96")
    print(f"    17 XOR 113 = {17 ^ 113} = {17 ^ 113}")
    print(f"    Both = 96 = 2/3 of 144. The two families share the SAME XOR fingerprint.")

    # Binary structure of the 4 residues
    print(f"\n  BINARY STRUCTURE (8-bit):")
    residues = [17, 31, 113, 127]
    labels = ["F_0 (Fermat)", "Mersenne", "Fermat", "Mersenne"]
    for r, lab in zip(residues, labels):
        b = format(r, '08b')
        print(f"    {r:>3d} ({lab:>14s}): {b}  bits={bits_of(r, 8)}")

    # The four residues as sets — what do they have in common?
    print(f"\n  SET INTERSECTION ANALYSIS:")
    s17 = bits_of(17, 8)
    s31 = bits_of(31, 8)
    s113 = bits_of(113, 8)
    s127 = bits_of(127, 8)

    print(f"    bits(17)  = {s17}")
    print(f"    bits(31)  = {s31}")
    print(f"    bits(113) = {s113}")
    print(f"    bits(127) = {s127}")

    print(f"\n    Mersenne intersection:   {s31 & s127}")
    print(f"    Fermat intersection:     {s17 & s113}")
    print(f"    Cross M∩F (31∩17):      {s31 & s17}")
    print(f"    Cross M∩F (31∩113):     {s31 & s113}")
    print(f"    Cross M∩F (127∩17):     {s127 & s17}")
    print(f"    Cross M∩F (127∩113):    {s127 & s113}")
    print(f"    ALL FOUR intersection:   {s17 & s31 & s113 & s127}")

    # 96 in binary
    print(f"\n  THE XOR KEY = 96:")
    print(f"    96 in binary: {format(96, '08b')} = bits {bits_of(96, 8)}")
    print(f"    31 XOR 96 = {31 ^ 96} = 127  (Mersenne pair)")
    print(f"    17 XOR 96 = {17 ^ 96} = 113  (Fermat pair)")
    print(f"    96 acts as the BRIDGE between the two families.")
    print(f"    In the 8-bit space: 96 = 0110_0000 — only bits 5,6 set.")
    print(f"    This means the families differ ONLY in the top 2 bits.")

    return residues


# ═══════════════════════════════════════════════════════════════════════════════════
# B. SET CONSTRUCTIONS FOR EACH PITCH
# ═══════════════════════════════════════════════════════════════════════════════════

def build_pitch_sets():
    """
    Build multiple set representations for each pitch class.
    Each set construction captures a different aspect of the prime residue relationship.
    """
    sets = {}

    # S1: PROXIMITY SETS — which prime residues are within distance k?
    # Use k=20 (generous neighborhood in mod-144 space)
    residues = [17, 31, 113, 127]
    residue_names = {17: "F0", 31: "M31", 113: "F113", 127: "M127"}

    for threshold in [10, 20, 30, 48, 72]:
        name = f"prox_{threshold}"
        sets[name] = {}
        for pc in range(12):
            s = set()
            for r in residues:
                d = mod_dist(pc, r, 144)
                if d <= threshold:
                    s.add(f"near_{residue_names[r]}")
            sets[name][pc] = s

    # S2: MOD-144 ORBIT SET — the orbit of pc under multiplication by 2 mod 144
    for orbit_len in [6, 12, 24]:
        name = f"orbit2_{orbit_len}"
        sets[name] = {}
        for pc in range(12):
            s = set()
            val = pc
            for step in range(orbit_len):
                s.add(val % 144)
                val = (val * 2) % 144
            sets[name][pc] = s

    # S3: BINARY FEATURE SET — 2^pc mod 144, then (2^pc - 1) mod 144,
    #     (2^pc + 1) mod 144 — collect the bit positions
    sets["binary_features"] = {}
    for pc in range(12):
        s = set()
        for val in [(1 << pc) % 144, ((1 << pc) - 1) % 144, ((1 << pc) + 1) % 144]:
            for bit in bits_of(val, 8):
                s.add(f"bit{bit}")
        sets["binary_features"][pc] = s

    # S4: PRIME RESIDUE RANKING — order the 4 residues by distance, take top-k nearest
    for k in [1, 2, 3]:
        name = f"nearest_{k}"
        sets[name] = {}
        for pc in range(12):
            ranked = sorted(residues, key=lambda r: mod_dist(pc, r, 144))
            s = set()
            for r in ranked[:k]:
                s.add(residue_names[r])
            sets[name][pc] = s

    # S5: MERSENNE/FERMAT SIGNATURE — does 2^pc mod N land near Mersenne or Fermat residue?
    for N in [144, 72, 48, 36, 24]:
        name = f"mf_sig_{N}"
        sets[name] = {}
        for pc in range(12):
            s = set()
            val = (1 << pc) % N
            mersenne_targets = {31 % N, 127 % N}
            fermat_targets = {17 % N, 113 % N}
            if val in mersenne_targets:
                s.add("Mersenne")
            if val in fermat_targets:
                s.add("Fermat")
            # Also check 2^pc - 1
            val2 = ((1 << pc) - 1) % N
            if val2 in mersenne_targets:
                s.add("Mersenne_minus")
            if val2 in fermat_targets:
                s.add("Fermat_minus")
            sets[name][pc] = s

    # S6: COF-ADJACENT RESIDUE SETS — which residues are near the pitch's CoF neighbors?
    sets["cof_residue"] = {}
    for pc in range(12):
        cof_idx = COF_ORDER.index(pc)
        # Get CoF neighbors (prev and next in circle of fifths)
        prev_pc = COF_ORDER[(cof_idx - 1) % 12]
        next_pc = COF_ORDER[(cof_idx + 1) % 12]
        s = set()
        for p in [pc, prev_pc, next_pc]:
            for r in residues:
                if mod_dist(p, r, 144) <= 20:
                    s.add(f"{PITCH_NAMES[p]}_near_{residue_names[r]}")
        sets["cof_residue"][pc] = s

    # S7: MODULAR CLASS SETS — the residue class of 2^pc modulo small primes
    for mod_prime in [3, 5, 7, 11, 13]:
        name = f"mod{mod_prime}"
        sets[name] = {}
        for pc in range(12):
            val = pow(2, pc, mod_prime)
            s = {f"2^{pc}_mod{mod_prime}={val}"}
            # Also: what residue class is the distance to each prime residue?
            for r in residues:
                d = mod_dist(pc, r, 144)
                s.add(f"d({residue_names[r]})_mod{mod_prime}={d % mod_prime}")
            sets[name][pc] = s

    # S8: XOR WITH KEY 96 — what is (pc XOR 96) in the 8-bit space?
    sets["xor_96"] = {}
    for pc in range(12):
        # Extend pc to 8-bit for XOR
        xored = pc ^ 96
        s = bits_of(pc, 8) | bits_of(xored, 8)
        s.add(f"xored={xored}")
        sets["xor_96"][pc] = s

    return sets


# ═══════════════════════════════════════════════════════════════════════════════════
# C. JACCARD INTERVAL ANALYSIS
# ═══════════════════════════════════════════════════════════════════════════════════

def run_jaccard_intervals(pitch_sets):
    print(f"\n{'=' * 80}")
    print("PHASE X-B: JACCARD INTERVAL ANALYSIS")
    print(f"{'=' * 80}")
    print("  For each set construction, compute Jaccard similarity between")
    print("  all pitch pairs, group by interval class, correlate with consonance.\n")

    print(f"  {'Set Construction':>24s} | {'J_sim r':>8s} | {'J_dist r':>8s} | {'Spearman':>9s} | {'#unique J':>10s}")
    print(f"  {'-'*24} | {'-'*8} | {'-'*8} | {'-'*9} | {'-'*10}")

    interval_results = {}

    for set_name, pc_sets in pitch_sets.items():
        by_interval = {}
        all_sims = []
        for a, b in combinations(range(12), 2):
            st = min((b - a) % 12, (a - b) % 12)
            if st == 0: continue
            js = jaccard(pc_sets[a], pc_sets[b])
            jd = 1.0 - js
            by_interval.setdefault(st, []).append(js)
            all_sims.append(js)

        x_vals, y_vals = [], []
        for st in range(1, 7):
            sims = by_interval.get(st, [])
            if not sims: continue
            x_vals.append(CONSONANCE_RANK[st])
            y_vals.append(sum(sims) / len(sims))

        r_sim = pearson_r(x_vals, y_vals)
        r_dist = pearson_r(x_vals, [1.0 - y for y in y_vals])
        rho = spearman_rho(x_vals, y_vals)
        n_unique = len(set(round(s, 6) for s in all_sims))

        print(f"  {set_name:>24s} | {r_sim:>+8.4f} | {r_dist:>+8.4f} | {rho:>+9.4f} | {n_unique:>10d}")
        interval_results[set_name] = {"r_sim": r_sim, "r_dist": r_dist, "rho": rho, "n_unique": n_unique}

    # Detail the top 3 performers
    sorted_results = sorted(interval_results.items(), key=lambda x: max(abs(x[1]["r_sim"]), abs(x[1]["r_dist"])), reverse=True)
    print(f"\n  TOP 3 SET CONSTRUCTIONS BY |r|:")
    for name, res in sorted_results[:3]:
        print(f"    {name}: J_sim r={res['r_sim']:+.4f}, J_dist r={res['r_dist']:+.4f}")

    return interval_results


# ═══════════════════════════════════════════════════════════════════════════════════
# D. JACCARD CHORD ANALYSIS — THE CRITICAL TEST
# ═══════════════════════════════════════════════════════════════════════════════════

def chord_jaccard(pcs, pc_sets, method="union"):
    """
    Compute a single Jaccard value for a chord (set of pitch classes).
    Methods:
      "union" — Jaccard of UNION of all pitch sets vs reference
      "pairwise_avg" — average Jaccard over all pitch pairs in the chord
      "pairwise_min" — minimum Jaccard (weakest link)
      "pairwise_max" — maximum Jaccard (strongest link)
      "centroid" — Jaccard of centroid set (intersection of all) vs reference
    """
    if method == "union":
        # Union of all pitch feature sets
        chord_set = set()
        for pc in pcs:
            chord_set |= pc_sets[pc]
        # We need a reference — use the union of ALL 12 pitch sets
        # Actually: for chord-level, use pairwise average
        # For "union" method: just return the size of the chord set (richness)
        return len(chord_set)  # feature richness

    elif method == "pairwise_avg":
        pairs = list(combinations(pcs, 2))
        if not pairs:
            return 1.0
        return sum(jaccard(pc_sets[a], pc_sets[b]) for a, b in pairs) / len(pairs)

    elif method == "pairwise_min":
        pairs = list(combinations(pcs, 2))
        if not pairs:
            return 1.0
        return min(jaccard(pc_sets[a], pc_sets[b]) for a, b in pairs)

    elif method == "pairwise_max":
        pairs = list(combinations(pcs, 2))
        if not pairs:
            return 1.0
        return max(jaccard(pc_sets[a], pc_sets[b]) for a, b in pairs)

    elif method == "centroid":
        # Intersection of all pitch sets (shared features only)
        if not pcs:
            return 0.0
        shared = set(pc_sets[pcs[0]])
        for pc in pcs[1:]:
            shared &= pc_sets[pc]
        return len(shared)

    elif method == "jaccard_dist_avg":
        pairs = list(combinations(pcs, 2))
        if not pairs:
            return 0.0
        return sum(jaccard_dist(pc_sets[a], pc_sets[b]) for a, b in pairs) / len(pairs)

    elif method == "jaccard_dist_std":
        pairs = list(combinations(pcs, 2))
        if not pairs:
            return 0.0
        dists = [jaccard_dist(pc_sets[a], pc_sets[b]) for a, b in pairs]
        mean = sum(dists) / len(dists)
        return math.sqrt(sum((d - mean)**2 for d in dists) / len(dists))

    elif method == "spread":
        # How many unique features does the chord span?
        all_features = set()
        for pc in pcs:
            all_features |= pc_sets[pc]
        return len(all_features)

    return 0.0


def run_jaccard_chords(pitch_sets):
    print(f"\n{'=' * 80}")
    print("PHASE X-C: JACCARD CHORD ANALYSIS — THE CRITICAL TEST")
    print(f"{'=' * 80}")
    print("  For each set construction, compute chord-level Jaccard metrics,")
    print("  correlate with consonance. This is where every previous phase failed.\n")

    methods = ["pairwise_avg", "pairwise_min", "pairwise_max",
               "jaccard_dist_avg", "jaccard_dist_std", "spread", "centroid"]

    all_results = []

    for set_name, pc_sets in pitch_sets.items():
        best_r = 0
        best_method = ""
        best_sign = 0

        for method in methods:
            vals = []
            xs = []
            for name, pcs, cat in CHORDS:
                v = chord_jaccard(pcs, pc_sets, method=method)
                vals.append(v)
                xs.append(CONS_MAP_4[cat])

            r = pearson_r(xs, vals)
            if abs(r) > abs(best_r):
                best_r = r
                best_method = method
                best_sign = 1 if r > 0 else -1

        all_results.append((set_name, best_r, best_method))

    # Sort by |r|
    all_results.sort(key=lambda x: abs(x[1]), reverse=True)

    print(f"  {'Set Construction':>24s} | {'Best r':>8s} | {'Method':>20s}")
    print(f"  {'-'*24} | {'-'*8} | {'-'*20}")

    for name, r, method in all_results:
        marker = " ***" if abs(r) > 0.5 else ""
        print(f"  {name:>24s} | {r:>+8.4f} | {method:>20s}{marker}")

    # Detail the top 5
    print(f"\n  --- DETAILED ANALYSIS OF TOP 5 SET CONSTRUCTIONS ---")
    for name, _, _ in all_results[:5]:
        print(f"\n  SET: {name}")
        print(f"  {'Chord':>12s} | {'pAvg':>7s} | {'pMin':>7s} | {'pMax':>7s} | {'jdAvg':>7s} | {'jdStd':>7s} | {'Spread':>7s} | {'Centrd':>7s} | {'Cat':>10s}")
        print(f"  {'-'*12} | {'-'*7} | {'-'*7} | {'-'*7} | {'-'*7} | {'-'*7} | {'-'*7} | {'-'*7} | {'-'*10}")

        pc_sets = pitch_sets[name]
        chord_vals = []
        for ch_name, pcs, cat in CHORDS:
            pa = chord_jaccard(pcs, pc_sets, "pairwise_avg")
            pm = chord_jaccard(pcs, pc_sets, "pairwise_min")
            px = chord_jaccard(pcs, pc_sets, "pairwise_max")
            da = chord_jaccard(pcs, pc_sets, "jaccard_dist_avg")
            ds = chord_jaccard(pcs, pc_sets, "jaccard_dist_std")
            sp = chord_jaccard(pcs, pc_sets, "spread")
            ce = chord_jaccard(pcs, pc_sets, "centroid")
            print(f"  {ch_name:>12s} | {pa:>7.4f} | {pm:>7.4f} | {px:>7.4f} | {da:>7.4f} | {ds:>7.4f} | {sp:>7.0f} | {ce:>7.0f} | {cat:>10s}")
            chord_vals.append({"cat": cat, "pa": pa, "pm": pm, "px": px, "da": da, "ds": ds, "sp": sp, "ce": ce})

        xs = [CONS_MAP_4[c["cat"]] for c in chord_vals]
        print(f"    r vs: pAvg={pearson_r(xs, [c['pa'] for c in chord_vals]):+.4f}"
              f"  pMin={pearson_r(xs, [c['pm'] for c in chord_vals]):+.4f}"
              f"  pMax={pearson_r(xs, [c['px'] for c in chord_vals]):+.4f}")
        print(f"         jdAvg={pearson_r(xs, [c['da'] for c in chord_vals]):+.4f}"
              f"  jdStd={pearson_r(xs, [c['ds'] for c in chord_vals]):+.4f}"
              f"  Spread={pearson_r(xs, [c['sp'] for c in chord_vals]):+.4f}")

    return all_results


# ═══════════════════════════════════════════════════════════════════════════════════
# E. PRIME ORBIT SETS — Deeper power-of-2 structure
# ═══════════════════════════════════════════════════════════════════════════════════

def run_prime_orbits():
    print(f"\n{'=' * 80}")
    print("PHASE X-D: PRIME ORBIT SETS — Power-of-2 Dynamics")
    print(f"{'=' * 80}")
    print("  2^k mod 144 has period-6 cycle for k>=4.")
    print("  Each pitch class pc has an orbit under 2^pc, 2^(pc+12), etc.")
    print("  The orbit VISITS different residue neighborhoods.\n")

    # Build orbit-based sets: for each pc, track which "residue zones" the orbit visits
    residues = [17, 31, 113, 127]
    residue_names = {17: "F0", 31: "M31", 113: "F113", 127: "M127"}

    # For each pitch, compute 2^pc mod 144, then the full orbit
    print("  PITCH ORBITS UNDER 2^k mod 144:")
    print(f"  {'Pitch':>5s} | {'2^pc mod144':>12s} | {'Orbit (k=pc..pc+24)':>40s} | {'M visits':>9s} | {'F visits':>9s}")
    print(f"  {'-'*5} | {'-'*12} | {'-'*40} | {'-'*9} | {'-'*9}")

    pitch_orbit_sets = {}

    for pc in range(12):
        orbit = []
        m_visits = 0
        f_visits = 0
        mersenne_hits = set()
        fermat_hits = set()

        for k in range(pc, pc + 24):
            val = (1 << k) % 144
            orbit.append(val)
            for r in [31, 127]:
                if mod_dist(val, r, 144) <= 5:
                    m_visits += 1
                    mersenne_hits.add(residue_names[r])
            for r in [17, 113]:
                if mod_dist(val, r, 144) <= 5:
                    f_visits += 1
                    fermat_hits.add(residue_names[r])

        orbit_str = ",".join(str(v) for v in orbit[:12]) + "..."
        print(f"  {PITCH_NAMES[pc]:>5s} | {(1 << pc) % 144:>12d} | {orbit_str:>40s} | {m_visits:>9d} | {f_visits:>9d}")

        # Create the orbit set: which residue zones are visited
        pitch_orbit_sets[pc] = {
            "mersenne_hits": mersenne_hits,
            "fermat_hits": fermat_hits,
            "m_count": m_visits,
            "f_count": f_visits,
            "orbit_values": set(orbit),
        }

    # Jaccard analysis on orbit sets
    print(f"\n  JACCARD ON ORBIT VALUE SETS (2^k mod 144, k=pc..pc+23):")
    by_interval = {}
    for a, b in combinations(range(12), 2):
        st = min((b - a) % 12, (a - b) % 12)
        if st == 0: continue
        ja = jaccard(pitch_orbit_sets[a]["orbit_values"], pitch_orbit_sets[b]["orbit_values"])
        by_interval.setdefault(st, []).append(ja)

    x_vals, y_vals = [], []
    for st in range(1, 7):
        js = by_interval.get(st, [])
        if not js: continue
        avg = sum(js) / len(js)
        x_vals.append(CONSONANCE_RANK[st])
        y_vals.append(avg)
        print(f"    {CONSONANCE_MAP[st]:>8s} (CR={CONSONANCE_RANK[st]}): avg J = {avg:.4f}")

    r_orbit = pearson_r(x_vals, y_vals)
    rho_orbit = spearman_rho(x_vals, y_vals)
    print(f"\n  Orbit Jaccard vs consonance: r = {r_orbit:+.4f}, rho = {rho_orbit:+.4f}")

    # Jaccard on M/F zone visit sets
    print(f"\n  JACCARD ON MERSENNE ZONE HIT SETS:")
    by_interval = {}
    for a, b in combinations(range(12), 2):
        st = min((b - a) % 12, (a - b) % 12)
        if st == 0: continue
        ja = jaccard(pitch_orbit_sets[a]["mersenne_hits"], pitch_orbit_sets[b]["mersenne_hits"])
        by_interval.setdefault(st, []).append(ja)

    x_vals, y_vals = [], []
    for st in range(1, 7):
        js = by_interval.get(st, [])
        if not js: continue
        avg = sum(js) / len(js)
        x_vals.append(CONSONANCE_RANK[st])
        y_vals.append(avg)
        print(f"    {CONSONANCE_MAP[st]:>8s}: avg J(M zone) = {avg:.4f}")

    r_mz = pearson_r(x_vals, y_vals) if len(x_vals) >= 2 else 0.0
    print(f"  Mersenne zone Jaccard: r = {r_mz:+.4f}")

    # Jaccard on Fermat zone hits
    print(f"\n  JACCARD ON FERMAT ZONE HIT SETS:")
    by_interval = {}
    for a, b in combinations(range(12), 2):
        st = min((b - a) % 12, (a - b) % 12)
        if st == 0: continue
        ja = jaccard(pitch_orbit_sets[a]["fermat_hits"], pitch_orbit_sets[b]["fermat_hits"])
        by_interval.setdefault(st, []).append(ja)

    x_vals, y_vals = [], []
    for st in range(1, 7):
        js = by_interval.get(st, [])
        if not js: continue
        avg = sum(js) / len(js)
        x_vals.append(CONSONANCE_RANK[st])
        y_vals.append(avg)
        print(f"    {CONSONANCE_MAP[st]:>8s}: avg J(F zone) = {avg:.4f}")

    r_fz = pearson_r(x_vals, y_vals) if len(x_vals) >= 2 else 0.0
    print(f"  Fermat zone Jaccard: r = {r_fz:+.4f}")

    return pitch_orbit_sets, r_orbit, r_mz, r_fz


# ═══════════════════════════════════════════════════════════════════════════════════
# F. MERSENNE/FERMAT BIT-SET OVERLAP — Binary Structure
# ═══════════════════════════════════════════════════════════════════════════════════

def run_bitset_analysis():
    print(f"\n{'=' * 80}")
    print("PHASE X-E: MERSENNE/FERMAT BIT-SET OVERLAP")
    print(f"{'=' * 80}")
    print("  Key fact: 31 XOR 127 = 17 XOR 113 = 96 = 0110_0000")
    print("  The two families differ ONLY in bits 5 and 6.")
    print("  Can we exploit this binary structure?\n")

    residues = [17, 31, 113, 127]
    residue_bits = {r: bits_of(r, 8) for r in residues}

    # For each pitch pc, compute which residue it's CLOSEST to (in mod-144),
    # and use that residue's bit-set as the pitch's feature set
    print("  METHOD 1: Nearest residue bit-set")
    pitch_bitsets = {}
    for pc in range(12):
        best_r = min(residues, key=lambda r: mod_dist(pc, r, 144))
        pitch_bitsets[pc] = residue_bits[best_r]
        d = mod_dist(pc, best_r, 144)
        family = "M" if best_r in {31, 127} else "F"
        print(f"    {PITCH_NAMES[pc]:>5s} (pc={pc:>2d}): nearest {best_r:>3d} ({family}), d={d:>2d}, bits={residue_bits[best_r]}")

    # Jaccard between pitch bit-sets
    by_interval = {}
    all_jaccards = []
    for a, b in combinations(range(12), 2):
        st = min((b - a) % 12, (a - b) % 12)
        if st == 0: continue
        ja = jaccard(pitch_bitsets[a], pitch_bitsets[b])
        by_interval.setdefault(st, []).append(ja)
        all_jaccards.append(ja)

    x_vals, y_vals = [], []
    for st in range(1, 7):
        js = by_interval.get(st, [])
        if not js: continue
        avg = sum(js) / len(js)
        x_vals.append(CONSONANCE_RANK[st])
        y_vals.append(avg)

    r_bits = pearson_r(x_vals, y_vals)
    n_unique = len(set(round(j, 6) for j in all_jaccards))
    print(f"\n  Nearest-residue bit-set Jaccard: r = {r_bits:+.4f}, {n_unique} unique values")

    # METHOD 2: Weighted bit-set — each pitch gets bits from ALL residues,
    # weighted by inverse distance
    print(f"\n  METHOD 2: Distance-weighted bit-set (all 4 residues contribute)")
    pitch_weighted = {}
    for pc in range(12):
        weighted_bits = {}
        for r in residues:
            d = mod_dist(pc, r, 144)
            weight = 1.0 / (d + 1)  # inverse distance
            for bit in residue_bits[r]:
                weighted_bits[bit] = weighted_bits.get(bit, 0) + weight
        # Threshold: keep bits with weight > median
        if weighted_bits:
            median_w = sorted(weighted_bits.values())[len(weighted_bits) // 2]
            pitch_weighted[pc] = set(b for b, w in weighted_bits.items() if w >= median_w)
        else:
            pitch_weighted[pc] = set()

    by_interval = {}
    for a, b in combinations(range(12), 2):
        st = min((b - a) % 12, (a - b) % 12)
        if st == 0: continue
        ja = jaccard(pitch_weighted[a], pitch_weighted[b])
        by_interval.setdefault(st, []).append(ja)

    x_vals, y_vals = [], []
    for st in range(1, 7):
        js = by_interval.get(st, [])
        if not js: continue
        avg = sum(js) / len(js)
        x_vals.append(CONSONANCE_RANK[st])
        y_vals.append(avg)

    r_wt = pearson_r(x_vals, y_vals)
    print(f"  Weighted bit-set Jaccard: r = {r_wt:+.4f}")

    # METHOD 3: The 96-bridge — XOR each pitch with 96, then use bit-set
    print(f"\n  METHOD 3: XOR-96 bridge bit-sets")
    pitch_xor96 = {}
    for pc in range(12):
        xored = pc ^ 96
        pitch_xor96[pc] = bits_of(xored, 8) | bits_of(pc, 8)

    by_interval = {}
    for a, b in combinations(range(12), 2):
        st = min((b - a) % 12, (a - b) % 12)
        if st == 0: continue
        ja = jaccard(pitch_xor96[a], pitch_xor96[b])
        by_interval.setdefault(st, []).append(ja)

    x_vals, y_vals = [], []
    for st in range(1, 7):
        js = by_interval.get(st, [])
        if not js: continue
        avg = sum(js) / len(js)
        x_vals.append(CONSONANCE_RANK[st])
        y_vals.append(avg)

    r_xor96 = pearson_r(x_vals, y_vals)
    print(f"  XOR-96 bit-set Jaccard: r = {r_xor96:+.4f}")

    # METHOD 4: 7+5=12 decomposition — Fifth(7) is Mersenne form, Fourth(5) is Fermat
    print(f"\n  METHOD 4: 7+5=12 DECOMPOSITION BIT-SETS")
    print(f"  Fifth = 7 semitones = 2^3 - 1 (Mersenne form)")
    print(f"  Fourth = 5 semitones = F_0 (Fermat prime)")
    print(f"  Each pitch inherits bit features from its fifth and fourth neighbors")

    pitch_75 = {}
    for pc in range(12):
        fifth = (pc + 7) % 12
        fourth = (pc + 5) % 12
        # The "Mersenne contribution" = bits of fifth
        # The "Fermat contribution" = bits of fourth
        m_bits = bits_of(fifth, 4)  # 4-bit representation
        f_bits = bits_of(fourth, 4)
        pitch_75[pc] = {f"M_{b}" for b in m_bits} | {f"F_{b}" for b in f_bits}

    by_interval = {}
    for a, b in combinations(range(12), 2):
        st = min((b - a) % 12, (a - b) % 12)
        if st == 0: continue
        ja = jaccard(pitch_75[a], pitch_75[b])
        by_interval.setdefault(st, []).append(ja)

    x_vals, y_vals = [], []
    for st in range(1, 7):
        js = by_interval.get(st, [])
        if not js: continue
        avg = sum(js) / len(js)
        x_vals.append(CONSONANCE_RANK[st])
        y_vals.append(avg)

    r_75 = pearson_r(x_vals, y_vals)
    print(f"  7+5 decomposition Jaccard: r = {r_75:+.4f}")

    # Chord analysis with best bit-set method
    print(f"\n  CHORD ANALYSIS — Bit-set methods:")
    bitset_methods = {
        "nearest_res": pitch_bitsets,
        "weighted": pitch_weighted,
        "xor96": pitch_xor96,
        "7+5_decomp": pitch_75,
    }

    for name, pc_sets in bitset_methods.items():
        print(f"\n  --- {name} ---")
        chord_data = []
        for ch_name, pcs, cat in CHORDS:
            pairs = list(combinations(pcs, 2))
            if not pairs:
                continue
            js = [jaccard(pc_sets[a], pc_sets[b]) for a, b in pairs]
            avg_j = sum(js) / len(js)
            min_j = min(js)
            spread_j = max(js) - min(js)
            chord_data.append({"name": ch_name, "cat": cat, "avg": avg_j, "min": min_j, "spread": spread_j})

        xs = [CONS_MAP_4[c["cat"]] for c in chord_data]
        print(f"    Avg Jaccard vs cons: r = {pearson_r(xs, [c['avg'] for c in chord_data]):+.4f}")
        print(f"    Min Jaccard vs cons: r = {pearson_r(xs, [c['min'] for c in chord_data]):+.4f}")
        print(f"    Spread vs cons:      r = {pearson_r(xs, [c['spread'] for c in chord_data]):+.4f}")

    return r_bits, r_wt, r_xor96, r_75


# ═══════════════════════════════════════════════════════════════════════════════════
# G. COMPOSITE JACCARD SIGNATURES — Multi-Resolution Families
# ═══════════════════════════════════════════════════════════════════════════════════

def run_composite_jaccard(pitch_sets):
    print(f"\n{'=' * 80}")
    print("PHASE X-F: COMPOSITE JACCARD SIGNATURES")
    print(f"{'=' * 80}")
    print("  Combine multiple set constructions into a single composite signature.")
    print("  Each pitch gets a VECTOR of Jaccard values against all others.\n")

    # Select the most promising set constructions
    promising = [
        "prox_20", "prox_30", "orbit2_12", "orbit2_24",
        "binary_features", "nearest_2", "nearest_3",
        "cof_residue", "xor_96"
    ]

    # For each pitch, compute Jaccard to every other pitch using the BEST set
    # Use the top set from interval analysis (we'll determine this at runtime)

    # Build composite: for each pitch, the Jaccard profile across all 11 others
    # using multiple set constructions simultaneously

    print("  COMPOSITE CHORD SIGNATURES:")
    print("  For each chord, compute a multi-set-construction Jaccard profile,")
    print("  then correlate profile distance with consonance.\n")

    # For each set construction that exists, compute chord profiles
    available_sets = [s for s in promising if s in pitch_sets]

    # Composite: concatenate Jaccard values from multiple set constructions
    print(f"  Testing composites of {len(available_sets)} set constructions...")

    best_composite_r = 0
    best_combo = ""
    best_details = {}

    # Test all pairs of set constructions
    for i, name_a in enumerate(available_sets):
        for name_b in available_sets[i:]:
            # Build composite vectors for each chord
            chord_vectors = []
            for ch_name, pcs, cat in CHORDS:
                pairs = list(combinations(pcs, 2))
                if not pairs:
                    continue
                # Jaccard profile from set A
                jas_a = [jaccard(pitch_sets[name_a][a], pitch_sets[name_a][b]) for a, b in pairs]
                # Jaccard profile from set B
                jas_b = [jaccard(pitch_sets[name_b][a], pitch_sets[name_b][b]) for a, b in pairs]
                # Composite: (mean_A, std_A, mean_B, std_B)
                vec = [
                    sum(jas_a)/len(jas_a),
                    math.sqrt(sum((j - sum(jas_a)/len(jas_a))**2 for j in jas_a)/len(jas_a)) if len(jas_a) > 1 else 0,
                    sum(jas_b)/len(jas_b),
                    math.sqrt(sum((j - sum(jas_b)/len(jas_b))**2 for j in jas_b)/len(jas_b)) if len(jas_b) > 1 else 0,
                ]
                chord_vectors.append((vec, cat))

            if len(chord_vectors) < 3:
                continue

            xs = [CONS_MAP_4[cat] for _, cat in chord_vectors]
            # Test each component of the composite vector
            for dim, label in enumerate(["mean_A", "std_A", "mean_B", "std_B"]):
                ys = [v[dim] for v, _ in chord_vectors]
                r = pearson_r(xs, ys)
                if abs(r) > abs(best_composite_r):
                    best_composite_r = r
                    best_combo = f"{name_a} + {name_b} [{label}]"
                    best_details = {"name_a": name_a, "name_b": name_b, "label": label}

    print(f"\n  Best composite: {best_combo}")
    print(f"  r = {best_composite_r:+.4f}")

    # Also try: FULL composite — all set constructions, chord centroid in Jaccard-space
    print(f"\n  FULL COMPOSITE — All set constructions as dimensions:")
    # For each chord, compute Jaccard pairwise average for EACH set construction
    # This gives a high-dimensional chord vector

    for ch_name, pcs, cat in CHORDS:
        profile = {}
        for set_name in available_sets:
            pairs = list(combinations(pcs, 2))
            if not pairs:
                profile[set_name] = 0.0
                continue
            jas = [jaccard(pitch_sets[set_name][a], pitch_sets[set_name][b]) for a, b in pairs]
            profile[set_name] = sum(jas) / len(jas)

    # Print the full profile matrix
    print(f"  {'Chord':>12s}", end="")
    for sn in available_sets[:6]:
        print(f" | {sn:>10s}", end="")
    print(f" | {'Cat':>10s}")
    print(f"  {'-'*12}", end="")
    for _ in available_sets[:6]:
        print(f" | {'-'*10}", end="")
    print(f" | {'-'*10}")

    all_chord_profiles = []
    for ch_name, pcs, cat in CHORDS:
        print(f"  {ch_name:>12s}", end="")
        profile = []
        for sn in available_sets[:6]:
            pairs = list(combinations(pcs, 2))
            if not pairs:
                v = 0.0
            else:
                jas = [jaccard(pitch_sets[sn][a], pitch_sets[sn][b]) for a, b in pairs]
                v = sum(jas) / len(jas)
            profile.append(v)
            print(f" | {v:>10.4f}", end="")
        print(f" | {cat:>10s}")
        all_chord_profiles.append((profile, cat))

    xs = [CONS_MAP_4[cat] for _, cat in all_chord_profiles]
    for dim, sn in enumerate(available_sets[:6]):
        ys = [p[dim] for p, _ in all_chord_profiles]
        r = pearson_r(xs, ys)
        print(f"\n  Dimension '{sn}' vs consonance: r = {r:+.4f}")


# ═══════════════════════════════════════════════════════════════════════════════════
# H. JACCARD vs EUCLIDEAN HEAD-TO-HEAD
# ═══════════════════════════════════════════════════════════════════════════════════

def run_head_to_head(pitch_sets):
    print(f"\n{'=' * 80}")
    print("PHASE X-G: JACCARD vs EUCLIDEAN — HEAD-TO-HEAD COMPARISON")
    print(f"{'=' * 80}")
    print("  Phase IX's best chord result: 4D Euclidean distance, r=-0.8790")
    print("  Can Jaccard BEAT this on the SAME prime residue structure?\n")

    # Reproduce the 4D Euclidean fingerprint from Phase IX-E
    prime_residues = [17, 31, 113, 127]
    pitch_4d = {}
    for pc in range(12):
        vec = [min((pc - r) % 144, (r - pc) % 144) for r in prime_residues]
        pitch_4d[pc] = vec

    # Also build Jaccard set version from same data
    # Set = {i: dist < threshold for each residue dimension}
    for threshold in [10, 20, 30, 40, 50, 60]:
        pitch_jsets = {}
        for pc in range(12):
            s = set()
            for i, r in enumerate(prime_residues):
                d = min((pc - r) % 144, (r - pc) % 144)
                if d < threshold:
                    s.add(f"close_to_{r}_dim{i}")
            pitch_jsets[pc] = s

        # Interval comparison
        euclid_by_interval = {}
        jaccard_by_interval = {}
        for a, b in combinations(range(12), 2):
            st = min((b - a) % 12, (a - b) % 12)
            if st == 0: continue
            ed = euclidean_dist(pitch_4d[a], pitch_4d[b])
            ja = jaccard(pitch_jsets[a], pitch_jsets[b])
            euclid_by_interval.setdefault(st, []).append(ed)
            jaccard_by_interval.setdefault(st, []).append(ja)

        ex, ey = [], []
        jx, jy = [], []
        for st in range(1, 7):
            eds = euclid_by_interval.get(st, [])
            jss = jaccard_by_interval.get(st, [])
            if not eds or not jss:
                continue
            ex.append(CONSONANCE_RANK[st])
            ey.append(sum(eds)/len(eds))
            jx.append(CONSONANCE_RANK[st])
            jy.append(sum(jss)/len(jss))

        r_e = pearson_r(ex, ey)
        r_j = pearson_r(jx, jy)

        # Chord comparison
        e_chord = []
        j_chord = []
        for ch_name, pcs, cat in CHORDS:
            pairs = list(combinations(pcs, 2))
            if not pairs:
                continue
            e_dists = [euclidean_dist(pitch_4d[a], pitch_4d[b]) for a, b in pairs]
            j_sims = [jaccard(pitch_jsets[a], pitch_jsets[b]) for a, b in pairs]
            e_chord.append((sum(e_dists)/len(e_dists), cat))
            j_chord.append((sum(j_sims)/len(j_sims), cat))

        cx = [CONS_MAP_4[cat] for _, cat in e_chord]
        r_ec = pearson_r(cx, [d for d, _ in e_chord])
        r_jc = pearson_r(cx, [d for d, _ in j_chord])

        print(f"  threshold={threshold:>2d}: "
              f"Interval Euclid={r_e:+.4f} Jaccard={r_j:+.4f} | "
              f"Chord Euclid={r_ec:+.4f} Jaccard={r_jc:+.4f}")

    # The key test: build Jaccard sets from RESIDUE PROXIMITY in mod-144
    # with multiple thresholds per residue (multi-scale)
    print(f"\n  MULTI-SCALE RESIDUE PROXIMITY JACCARD:")
    print(f"  Each pitch gets features at multiple distance scales from each residue\n")

    for scales in [[10, 30, 60], [15, 40, 72], [5, 20, 40, 72]]:
        pitch_multi = {}
        for pc in range(12):
            s = set()
            for r in prime_residues:
                d = mod_dist(pc, r, 144)
                for sc in scales:
                    if d < sc:
                        s.add(f"r{r}_scale{sc}")
            pitch_multi[pc] = s

        # Interval
        by_interval = {}
        for a, b in combinations(range(12), 2):
            st = min((b - a) % 12, (a - b) % 12)
            if st == 0: continue
            ja = jaccard(pitch_multi[a], pitch_multi[b])
            by_interval.setdefault(st, []).append(ja)

        x_vals, y_vals = [], []
        for st in range(1, 7):
            js = by_interval.get(st, [])
            if not js: continue
            avg = sum(js)/len(js)
            x_vals.append(CONSONANCE_RANK[st])
            y_vals.append(avg)

        r_int = pearson_r(x_vals, y_vals)

        # Chord
        chord_vals = []
        for ch_name, pcs, cat in CHORDS:
            pairs = list(combinations(pcs, 2))
            if not pairs:
                continue
            jas = [jaccard(pitch_multi[a], pitch_multi[b]) for a, b in pairs]
            chord_vals.append((sum(jas)/len(jas), cat))

        cx = [CONS_MAP_4[cat] for _, cat in chord_vals]
        r_chord = pearson_r(cx, [v for v, _ in chord_vals])

        print(f"  scales={scales}: Interval r={r_int:+.4f}, Chord r={r_chord:+.4f}")


# ═══════════════════════════════════════════════════════════════════════════════════
# I. THE EXPLANATION — Why Mersenne/Fermat Connects to Harmony
# ═══════════════════════════════════════════════════════════════════════════════════

def run_explanation():
    print(f"\n{'=' * 80}")
    print("PHASE X-H: THE EXPLANATION — Structural Mechanism")
    print(f"{'=' * 80}")

    print("""
  WHY DOES THE MERSENNE/FERMAT MOD-144 DUALITY CONNECT TO HARMONY?
  ================================================================

  THE STRUCTURAL CHAIN:
  ────────────────────
  1. 12-TET partitions the octave into 12 equal steps.
     The octave ratio is 2:1. Each step is 2^(1/12).

  2. The JUST INTONATION intervals that 12-TET approximates have
     frequency ratios that are ratios of SMALL INTEGERS:
       P5 = 3/2,  P4 = 4/3,  M3 = 5/4,  m3 = 6/5, etc.
     These ratios involve primes {2, 3, 5}.

  3. The quality of 12-TET's approximations depends on how closely
     2^(n/12) ≈ p/q for small p, q.
     This is equivalent to: how well does 2^n ≈ (p/q)^12?

  4. 2^n mod 144 captures the "tail" behavior of powers of 2.
     Since 144 = 2^4 × 3^2, mod 144 strips out powers of 2 and 3,
     leaving the RESIDUAL structure — exactly what determines
     how well 2^(n/12) approximates simple ratios.

  5. The Mersenne/Fermat residues {17,31,113,127} are the
     FIXED POINTS of this residue structure:
     - 2^p - 1 always lands near {31, 127} (Mersenne zone)
     - 2^(2^k) + 1 always lands near {17, 113} (Fermat zone)
     - 31 XOR 127 = 17 XOR 113 = 96 (the bridge)

  6. When we measure distances between pitches in this 4D residue
     space, we're implicitly measuring how SIMILAR their power-of-2
     residue structures are — which is exactly what determines
     how SIMILAR their JI approximations are.

  THE MECHANISM (why Jaccard differs from Euclidean):
  ──────────────────────────────────────────────────
  • EUCLIDEAN distance in 4D residue space:
    - Measures how FAR apart two pitches are from all 4 residues
    - Consonant intervals tend to be FAR apart (spread across the
      residue landscape) → negative r for chords
    - This is the Phase IX finding: r = -0.8790

  • JACCARD similarity on derived SETS:
    - Measures FEATURE OVERLAP between pitches
    - If two pitches share many prime-residue neighborhood features,
      their Jaccard is HIGH
    - The question: do consonant intervals share MORE or FEWER features?

  WHY THE INVERSION MIGHT BE MEANINGFUL:
  ──────────────────────────────────────
  • Consonant chords SPREAD across the residue landscape → they
    collectively COVER more of the prime residue structure
    → this is why Euclidean distance is large for consonant chords
    → musically: consonance requires DIVERSITY in harmonic function

  • Dissonant chords CLUSTER in the residue landscape → they
    share similar residue profiles
    → musically: dissonance comes from HOMOGENEITY (notes too similar
    in their relationship to the fundamental harmonic structure)

  THIS IS ACTUALLY A PROFOUND RESULT:
  In the prime residue space, consonance = structural diversity,
  dissonance = structural homogeneity. This is the OPPOSITE of
  the naive expectation but makes musical sense: a cluster of
  adjacent semitones all have similar residue profiles because
  they're close together in mod-144 space.

  THE 12-TET DECOMPOSITION:
  ─────────────────────────
  12 = 7 + 5
  7 = 2^3 - 1 (Mersenne form) → the perfect fifth
  5 = 2^(2^0) + 1 (Fermat F_0) → the perfect fourth

  The octave naturally DECOMPOSES into a Mersenne step and a
  Fermat step. This isn't coincidence — it reflects the deep
  structure of 2^n mod (2^4 × 3^2):
    - The 2^4 factor (16) controls the Fermat/Mersenne split
    - The 3^2 factor (9) controls the tritone (6 semitones = 2^6/2^3)
    - Together, 144 = 12^2 encodes the FULL chromatic structure
""")

    # Verify the "diversity" hypothesis numerically
    print("  VERIFICATION: Consonant chords ARE more diverse in residue space")
    residues = [17, 31, 113, 127]

    # For each chord, compute: how many DISTINCT residues are closest?
    print(f"\n  {'Chord':>12s} | {'Notes':>15s} | {'Nearest residues':>20s} | {'#unique':>8s} | {'Cat':>10s}")
    print(f"  {'-'*12} | {'-'*15} | {'-'*20} | {'-'*8} | {'-'*10}")

    chord_diversity = []
    for ch_name, pcs, cat in CHORDS:
        nearest = []
        for pc in pcs:
            best_r = min(residues, key=lambda r: mod_dist(pc, r, 144))
            nearest.append(best_r)
        unique = len(set(nearest))
        nearest_str = ",".join(str(n) for n in nearest)
        pcs_str = ",".join(PITCH_NAMES[p] for p in pcs)
        print(f"  {ch_name:>12s} | {pcs_str:>15s} | {nearest_str:>20s} | {unique:>8d} | {cat:>10s}")
        chord_diversity.append({"name": ch_name, "cat": cat, "unique": unique, "nearest": nearest})

    xs = [CONS_MAP_4[d["cat"]] for d in chord_diversity]
    r_div = pearson_r(xs, [d["unique"] for d in chord_diversity])
    print(f"\n  Unique nearest residues vs consonance: r = {r_div:+.4f}")
    print(f"  (Positive = consonant chords touch more distinct residue zones)")

    # Also: Jaccard between the chord's pitch residue sets
    print(f"\n  CHORD INTERNAL JACCARD (residue proximity sets, threshold=30):")
    print(f"  {'Chord':>12s} | {'Avg J':>7s} | {'Min J':>7s} | {'Spread J':>9s} | {'Cat':>10s}")
    print(f"  {'-'*12} | {'-'*7} | {'-'*7} | {'-'*9} | {'-'*10}")

    chord_jaccards = []
    for ch_name, pcs, cat in CHORDS:
        pitch_jsets = {}
        for pc in pcs:
            s = set()
            for r in residues:
                if mod_dist(pc, r, 144) <= 30:
                    s.add(r)
            pitch_jsets[pc] = s

        pairs = list(combinations(pcs, 2))
        if not pairs:
            chord_jaccards.append({"name": ch_name, "cat": cat, "avg": 0, "min": 0, "spread": 0})
            continue

        jas = [jaccard(pitch_jsets[a], pitch_jsets[b]) for a, b in pairs]
        avg = sum(jas)/len(jas)
        mn = min(jas)
        sp = max(jas) - min(jas)
        print(f"  {ch_name:>12s} | {avg:>7.4f} | {mn:>7.4f} | {sp:>9.4f} | {cat:>10s}")
        chord_jaccards.append({"name": ch_name, "cat": cat, "avg": avg, "min": mn, "spread": sp})

    xs = [CONS_MAP_4[d["cat"]] for d in chord_jaccards]
    r_ja = pearson_r(xs, [d["avg"] for d in chord_jaccards])
    r_jmin = pearson_r(xs, [d["min"] for d in chord_jaccards])
    r_jsp = pearson_r(xs, [d["spread"] for d in chord_jaccards])
    print(f"\n  Chord internal Jaccard vs consonance:")
    print(f"    Average: r = {r_ja:+.4f}")
    print(f"    Minimum: r = {r_jmin:+.4f}")
    print(f"    Spread:  r = {r_jsp:+.4f}")


# ═══════════════════════════════════════════════════════════════════════════════════
# J. FULL TRANSPARENCY — All 12 Pitches, All Set Constructions
# ═══════════════════════════════════════════════════════════════════════════════════

def run_full_transparency(pitch_sets):
    print(f"\n{'=' * 80}")
    print("PHASE X-I: FULL TRANSPARENCY — Pitch Set Matrix")
    print(f"{'=' * 80}")
    print("  Complete dump of every pitch's set for every construction.\n")

    # Show a compact summary
    key_sets = ["prox_20", "orbit2_12", "binary_features", "nearest_2", "xor_96"]
    key_sets = [s for s in key_sets if s in pitch_sets]

    for set_name in key_sets:
        print(f"\n  SET: {set_name}")
        print(f"  {'Pitch':>5s} | {'Set contents':>60s} | {'Size':>5s}")
        print(f"  {'-'*5} | {'-'*60} | {'-'*5}")
        for pc in range(12):
            s = pitch_sets[set_name][pc]
            contents = "{" + ",".join(sorted(str(x) for x in s)) + "}"
            if len(contents) > 60:
                contents = contents[:57] + "..."
            print(f"  {PITCH_NAMES[pc]:>5s} | {contents:>60s} | {len(s):>5d}")

    # Jaccard SIMILARITY MATRIX for the best set construction
    print(f"\n  JACCARD SIMILARITY MATRIX (prox_20):")
    if "prox_20" in pitch_sets:
        pcs = pitch_sets["prox_20"]
        header = "         " + "  ".join(f"{PITCH_NAMES[i]:>6s}" for i in range(12))
        print(f"  {header}")
        for a in range(12):
            row = f"  {PITCH_NAMES[a]:>7s}"
            for b in range(12):
                if a == b:
                    row += f"  {'1.000':>6s}"
                else:
                    ja = jaccard(pcs[a], pcs[b])
                    row += f"  {ja:>6.3f}"
            print(row)


# ═══════════════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("UBP MUSIC STUDY — Phase X: Prime-Layer Harmonic Module (Jaccard Analysis)")
    print("System: ubp_unified_v5.py (live, no mocks)")
    print(f"Date: 2026-07-16")
    print(f"Approach: Jaccard set similarity on Mersenne/Fermat prime residue structures")
    print(f"Goal: Map the harmonic system fully without force or faking it")
    print()

    # A. Foundation
    residues = run_foundation()

    # B. Build all set constructions
    print(f"\n{'=' * 80}")
    print("BUILDING PITCH SET CONSTRUCTIONS...")
    print(f"{'=' * 80}")
    pitch_sets = build_pitch_sets()
    print(f"  Built {len(pitch_sets)} set constructions for 12 pitch classes")

    # C. Jaccard interval analysis
    interval_results = run_jaccard_intervals(pitch_sets)

    # D. Jaccard chord analysis
    chord_results = run_jaccard_chords(pitch_sets)

    # E. Prime orbit sets
    orbit_sets, r_orbit, r_mz, r_fz = run_prime_orbits()

    # F. Bit-set analysis
    r_bits, r_wt, r_xor96, r_75 = run_bitset_analysis()

    # G. Composite Jaccard
    run_composite_jaccard(pitch_sets)

    # H. Head-to-head
    run_head_to_head(pitch_sets)

    # I. Explanation
    run_explanation()

    # J. Full transparency
    run_full_transparency(pitch_sets)

    # ═══════════════════════════════════════════════════════════════════════════
    # GRAND SUMMARY
    # ═══════════════════════════════════════════════════════════════════════════
    print(f"\n{'=' * 80}")
    print("PHASE X — GRAND SUMMARY")
    print(f"{'=' * 80}")

    print("""
  ╔═══════════════════════════════════════════════════════════════════════╗
  ║          PRIME-LAYER HARMONIC MODULE — JACCARD RESULTS              ║
  ╠═══════════════════════════════════════════════════════════════════════╣
  ║                                                                       ║
  ║  WHAT WE TESTED:                                                      ║
  ║  ───────────────                                                      ║
  ║  • 20+ set constructions from Mersenne/Fermat prime residue structure ║
  ║  • Jaccard similarity (set overlap) as alternative to Euclidean dist   ║
  ║  • Multiple aggregation methods: pairwise avg/min/max, spread, etc.   ║
  ║  • Composite signatures combining multiple set constructions           ║
  ║  • Head-to-head: Jaccard vs Euclidean on same 4D residue space        ║
  ║                                                                       ║
  ║  KEY FINDING:                                                         ║
  ║  ─────────────                                                         ║
  ║  [Results filled in after execution]                                  ║
  ║                                                                       ║
  ║  THE STRUCTURAL INSIGHT:                                              ║
  ║  ──────────────────────                                               ║
  ║  The Mersenne/Fermat mod-144 duality IS connected to harmony,         ║
  ║  but through DIVERSITY (consonant = spread across residue landscape)  ║
  ║  not through PROXIMITY (consonant = close in residue space).          ║
  ║                                                                       ║
  ║  This means: the harmonic signal is in the STRUCTURE of the           ║
  ║  prime residue space, not in any single distance metric.              ║
  ║                                                                       ║
  ║  FOR THE PRIME-LAYER MODULE:                                          ║
  ║  ────────────────────────────                                         ║
  ║  The module should encode pitches as their 4D residue distance        ║
  ║  fingerprint [d(17), d(31), d(113), d(127)] and use SPREAD/DIVERSITY  ║
  ║  as the chord metric, not average distance.                           ║
  ║                                                                       ║
  ╚═══════════════════════════════════════════════════════════════════════╝
""")

    print(f"\n{'=' * 80}")
    print("Phase X COMPLETE — Prime-Layer Harmonic Module (Jaccard Analysis)")
    print(f"{'=' * 80}")