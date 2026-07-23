"""
UBP Music Study — Phase VI: Leech Lattice & Barnes-Wall 256
=============================================================
Golay codewords are binary {0,1}^24 — only 3 distances (8,12,16).
The Leech lattice gives REAL 24D coordinates (0, ±2) — Euclidean distances.
Barnes-Wall 256 gives quaternary 256D vectors — even finer resolution.

Tests:
A. Leech expand_octad_to_physical: Euclidean distance between pitch points
B. Leech ontological_health: per-layer NRCI as chord coherence metric
C. Barnes-Wall 256D: generate pitch vectors, measure Euclidean distances
D. Can Leech 24D Euclidean distance differentiate chords?
"""

import sys, math, random
from fractions import Fraction
from itertools import combinations

sys.path.insert(0, "/home/z/my-project")
from ubp_unified_v5 import GolayCodeEngine, LeechLatticeEngine, BarnesWallEngine

g = GolayCodeEngine()
l = LeechLatticeEngine(g)
bw = BarnesWallEngine(g, dimension=256)

PITCH_NAMES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
CONSONANCE_MAP = {
    0: "Unison", 1: "Min2", 2: "Maj2", 3: "Min3", 4: "Maj3",
    5: "P4", 6: "TT", 7: "P5", 8: "Min6", 9: "Maj6", 10: "Min7", 11: "Maj7"
}
CONSONANCE_RANK = {
    0: 1, 7: 2, 5: 3, 4: 3, 9: 3, 3: 4, 8: 4, 10: 4, 2: 5, 11: 5, 1: 6, 6: 6
}
COF_ORDER = [0, 7, 2, 9, 4, 11, 6, 1, 8, 3, 10, 5]


def gray_code(n, bits=12):
    gc = n ^ (n >> 1)
    return [(gc >> (bits - 1 - i)) & 1 for i in range(bits)]


def encode_cof_cw_map():
    """Circle-of-Fifths Gray encoding: pitch_class -> 24-bit Golay codeword."""
    cw_map = {}
    for pc in range(12):
        pos = COF_ORDER.index(pc)
        seed = gray_code(pos, 12)
        cw_map[pc] = g.encode(seed)
    return cw_map


def euclidean_dist(a, b):
    return math.sqrt(sum((x - y) ** 2 for x, y in zip(a, b)))


def pearson_r(x_vals, y_vals):
    n = len(x_vals)
    if n < 2: return 0.0
    mx, my = sum(x_vals)/n, sum(y_vals)/n
    cov = sum((x-mx)*(y-my) for x,y in zip(x_vals, y_vals))
    vx = sum((x-mx)**2 for x in x_vals)
    vy = sum((y-my)**2 for y in y_vals)
    if vx == 0 or vy == 0: return 0.0
    return cov / math.sqrt(vx * vy)


# ═══════════════════════════════════════════════════════════════════════════════════
# A. LEECH LATTICE: EXPAND OCTAD TO PHYSICAL (24D REAL COORDINATES)
# ═══════════════════════════════════════════════════════════════════════════════════

def run_leech_intervals():
    print("=" * 80)
    print("PHASE VI-A: LEECH LATTICE 24D EUCLIDEAN DISTANCES")
    print("=" * 80)

    cw_map = encode_cof_cw_map()

    # For each pitch, expand its octad to 128 Leech points
    # (Only octads — HW=8 codewords — can be expanded. C has HW=0, can't expand.)
    print("\n  Expanding octads to 128 Leech points each...")
    print("  (C has HW=0 — not an octad, cannot expand. Using its nearest octad.)")

    pitch_leech_points = {}
    for pc in range(12):
        cw = cw_map[pc]
        hw = g.hamming_weight(cw)
        if hw == 8:
            points = l.expand_octad_to_physical(cw)
            pitch_leech_points[pc] = points
            print(f"  {PITCH_NAMES[pc]:>5s} (HW={hw}): {len(points)} Leech points")
        else:
            # Find nearest octad
            nearest = l.nearest_octad_idx(cw)
            octads = g.get_octads()
            octad = octads[nearest["idx"]]
            points = l.expand_octad_to_physical(octad)
            pitch_leech_points[pc] = points
            print(f"  {PITCH_NAMES[pc]:>5s} (HW={hw}): using nearest octad (d={nearest['distance']}), {len(points)} points")

    # Now compute Euclidean distances between Leech point sets
    # For each interval, compute MIN, MAX, AVG Euclidean distance across all point pairs
    print(f"\n  EUCLIDEAN DISTANCE BETWEEN PITCH LEECH POINT SETS:")
    print(f"  (Sampling 50 random point pairs per interval for speed)")

    by_interval = {}
    for pc_a, pc_b in combinations(range(12), 2):
        st = min((pc_b - pc_a) % 12, (pc_a - pc_b) % 12)
        if st == 0: continue

        pts_a = pitch_leech_points[pc_a]
        pts_b = pitch_leech_points[pc_b]
        random.seed(42 + pc_a * 12 + pc_b)
        dists = []
        for _ in range(50):
            pa = pts_a[random.randint(0, 127)]
            pb = pts_b[random.randint(0, 127)]
            dists.append(euclidean_dist(pa, pb))
        by_interval.setdefault(st, []).extend(dists)

    print(f"\n  {'Interval':>8s} | {'CR':>3s} | {'Avg Euc':>9s} | {'Min Euc':>9s} | {'Max Euc':>9s} | {'Std':>7s}")
    print(f"  {'-'*8} | {'-'*3} | {'-'*9} | {'-'*9} | {'-'*9} | {'-'*7}")

    x_vals, y_vals = [], []
    for st in range(1, 7):
        dists = by_interval.get(st, [])
        if not dists: continue
        avg = sum(dists) / len(dists)
        std = math.sqrt(sum((d - avg)**2 for d in dists) / len(dists))
        name = CONSONANCE_MAP[st]
        cr = CONSONANCE_RANK[st]
        x_vals.append(cr)
        y_vals.append(avg)
        print(f"  {name:>8s} | {cr:>3d} | {avg:>9.3f} | {min(dists):>9.3f} | {max(dists):>9.3f} | {std:>7.3f}")

    r = pearson_r(x_vals, y_vals)
    print(f"\n  Leech Euclidean: Pearson r = {r:.4f} (cf. Golay Hamming r = 0.8674)")

    # FULL SAMPLE: compute all 128×128 distances for a few key intervals
    print(f"\n  DENSE SAMPLING: All 128×128 = 16384 pairs for key intervals:")
    for st in [4, 7, 6, 1]:  # Maj3, P5, TT, Min2
        dists_full = []
        for pc_a, pc_b in combinations(range(12), 2):
            st_actual = min((pc_b - pc_a) % 12, (pc_a - pc_b) % 12)
            if st_actual != st: continue
            for pa in pitch_leech_points[pc_a]:
                for pb in pitch_leech_points[pc_b]:
                    dists_full.append(euclidean_dist(pa, pb))
        if dists_full:
            avg = sum(dists_full) / len(dists_full)
            std = math.sqrt(sum((d - avg)**2 for d in dists_full) / len(dists_full))
            name = CONSONANCE_MAP[st]
            cr = CONSONANCE_RANK[st]
            # Distance distribution
            dist_set = sorted(set(round(d, 2) for d in dists_full))
            print(f"    {name} (CR={cr}): avg={avg:.3f}, std={std:.3f}, "
                  f"range=[{min(dists_full):.1f}, {max(dists_full):.1f}], "
                  f"distinct distances: {len(dist_set)}")

    return pitch_leech_points


# ═══════════════════════════════════════════════════════════════════════════════════
# B. ONTOLOGICAL HEALTH: PER-LAYER NRCI AS CHORD COHERENCE METRIC
# ═══════════════════════════════════════════════════════════════════════════════════

def run_ontological_chords():
    print(f"\n{'=' * 80}")
    print("PHASE VI-B: ONTOLOGICAL HEALTH — Per-Layer NRCI for Chords")
    print(f"{'=' * 80}")
    print("  Each Leech point has 4 layers (Reality, Info, Activation, Potential).")
    print("  ontological_health returns per-layer NRCI. We test whether chord")
    print("  coherence (uniformity across layers) differs between consonant/dissonant.")

    cw_map = encode_cof_cw_map()

    # For each pitch, get ONE representative Leech point (the first expanded point)
    pitch_point = {}
    for pc in range(12):
        cw = cw_map[pc]
        hw = g.hamming_weight(cw)
        if hw == 8:
            points = l.expand_octad_to_physical(cw)
            pitch_point[pc] = points[0]
        else:
            nearest = l.nearest_octad_idx(cw)
            octad = g.get_octads()[nearest["idx"]]
            points = l.expand_octad_to_physical(octad)
            pitch_point[pc] = points[0]

    # Compute ontological health for each pitch
    print(f"\n  PITCH ONTOLOGICAL HEALTH:")
    print(f"  {'Pitch':>5s} | {'Reality':>8s} | {'Info':>8s} | {'Activation':>10s} | {'Potential':>9s} | {'Global':>7s} | {'Layer Std':>10s}")
    print(f"  {'-'*5} | {'-'*8} | {'-'*8} | {'-'*10} | {'-'*9} | {'-'*7} | {'-'*10}")

    pitch_health = {}
    for pc in range(12):
        h = l.ontological_health(pitch_point[pc])
        vals = [float(h["Reality"]), float(h["Info"]), float(h["Activation"]), float(h["Potential"])]
        layer_std = math.sqrt(sum((v - sum(vals)/4)**2 for v in vals) / 4)
        pitch_health[pc] = h
        print(f"  {PITCH_NAMES[pc]:>5s} | {float(h['Reality']):>8.4f} | {float(h['Info']):>8.4f} | "
              f"{float(h['Activation']):>10.4f} | {float(h['Potential']):>9.4f} | "
              f"{float(h['Global_NRCI']):>7.4f} | {layer_std:>10.4f}")

    # Now test chords: "chord point" = centroid of constituent pitch points
    # Then measure its ontological health
    chords = [
        ("C Maj",    [0,4,7],     "Consonant"),
        ("C Min",    [0,3,7],     "Consonant"),
        ("C Dim",    [0,3,6],     "Moderate"),
        ("C Aug",    [0,4,8],     "Moderate"),
        ("Cluster",  [0,1,2],     "Dissonant"),
        ("Cluster2", [0,1,6],     "Dissonant"),
        ("Maj7",     [0,4,7,11],  "Consonant"),
        ("Dom7",     [0,4,7,10],  "Consonant"),
        ("Dim7",     [0,3,6,9],   "Moderate"),
        ("Diatonic", [0,2,4,5,7,9,11], "Consonant"),
        ("Chrom6",   list(range(6)), "Dissonant"),
        ("WT 6",     [0,2,4,6,8,10], "Ambiguous"),
        ("Pentatonic",[0,2,4,7,9], "Consonant"),
        ("Blues",    [0,3,5,6,7,10], "Mixed"),
    ]

    print(f"\n  CHORD CENTROID ONTOLOGICAL ANALYSIS:")
    print(f"  (Centroid = arithmetic mean of pitch Leech points)")
    print(f"\n  {'Chord':>12s} | {'#n':>3s} | {'Reality':>8s} | {'Info':>8s} | {'Act':>8s} | {'Pot':>8s} | {'Global':>7s} | {'L.Std':>6s} | {'Tax':>7s} | {'NRCI':>7s} | {'Expect':>10s}")
    print(f"  {'-'*12} | {'-'*3} | {'-'*8} | {'-'*8} | {'-'*8} | {'-'*8} | {'-'*7} | {'-'*6} | {'-'*7} | {'-'*7} | {'-'*10}")

    results = []
    for name, pcs, expected in chords:
        # Compute centroid (may not be integer — need to handle)
        centroid = [0.0] * 24
        for pc in pcs:
            for i in range(24):
                centroid[i] += pitch_point[pc][i]
        n = len(pcs)
        centroid = [c / n for c in centroid]

        # For ontological_health we need integers. Round to nearest even integer (Leech points are even)
        centroid_int = [round(c / 2) * 2 for c in centroid]

        # Clamp to valid Leech range
        centroid_int = [max(-2, min(2, x)) for x in centroid_int]

        h = l.ontological_health(centroid_int)
        tax = float(l.calculate_symmetry_tax(centroid_int))
        nrci = float(l.calculate_nrci(centroid_int))
        vals = [float(h["Reality"]), float(h["Info"]), float(h["Activation"]), float(h["Potential"])]
        layer_std = math.sqrt(sum((v - sum(vals)/4)**2 for v in vals) / 4)

        print(f"  {name:>12s} | {n:>3d} | {float(h['Reality']):>8.4f} | {float(h['Info']):>8.4f} | "
              f"{float(h['Activation']):>8.4f} | {float(h['Potential']):>8.4f} | "
              f"{float(h['Global_NRCI']):>7.4f} | {layer_std:>6.3f} | {tax:>7.3f} | {nrci:>7.4f} | {expected:>10s}")
        results.append({"name": name, "expected": expected, "nrci": nrci, "tax": tax,
                        "layer_std": layer_std, "global": float(h["Global_NRCI"])})

    # Correlation
    cons_map = {"Consonant": 1, "Moderate": 2, "Mixed": 3, "Ambiguous": 3, "Dissonant": 4}
    xs = [cons_map[r["expected"]] for r in results]
    ys_nrci = [r["nrci"] for r in results]
    ys_tax = [r["tax"] for r in results]
    ys_lstd = [r["layer_std"] for r in results]
    print(f"\n  CORRELATIONS (centroid-based Leech points):")
    print(f"    Consonance vs NRCI:          r = {pearson_r(xs, ys_nrci):+.4f}")
    print(f"    Consonance vs Tax:           r = {pearson_r(xs, ys_tax):+.4f}")
    print(f"    Consonance vs Layer Std:     r = {pearson_r(xs, ys_lstd):+.4f}")

    # ALSO: try chord as VECTOR SUM (not centroid) — more like "The Flow"
    print(f"\n  CHORD VECTOR SUM (The Flow approach):")
    print(f"  {'Chord':>12s} | {'#n':>3s} | {'NormSq':>7s} | {'HW':>4s} | {'Tax':>7s} | {'NRCI':>7s} | {'L.Std':>6s} | {'Expect':>10s}")
    print(f"  {'-'*12} | {'-'*3} | {'-'*7} | {'-'*4} | {'-'*7} | {'-'*7} | {'-'*6} | {'-'*10}")

    flow_results = []
    for name, pcs, expected in chords:
        vec_sum = [0] * 24
        for pc in pcs:
            for i in range(24):
                vec_sum[i] += pitch_point[pc][i]

        # The sum won't be a valid Leech point (values can be >2 or <-2)
        # Measure it anyway using symmetry_tax (which counts non-zero entries)
        hw = sum(1 for x in vec_sum if x != 0)
        tax = float(l.calculate_symmetry_tax(vec_sum))
        nrci = float(l.calculate_nrci(vec_sum))
        h = l.ontological_health(vec_sum)
        vals = [float(h["Reality"]), float(h["Info"]), float(h["Activation"]), float(h["Potential"])]
        layer_std = math.sqrt(sum((v - sum(vals)/4)**2 for v in vals) / 4)

        print(f"  {name:>12s} | {len(pcs):>3d} | {sum(x*x for x in vec_sum):>7d} | {hw:>4d} | {tax:>7.3f} | {nrci:>7.4f} | {layer_std:>6.3f} | {expected:>10s}")
        flow_results.append({"name": name, "expected": expected, "nrci": nrci, "tax": tax, "layer_std": layer_std})

    xs = [cons_map[r["expected"]] for r in flow_results]
    ys = [r["nrci"] for r in flow_results]
    print(f"\n  Flow Consonance vs NRCI: r = {pearson_r(xs, ys):+.4f}")


# ═══════════════════════════════════════════════════════════════════════════════════
# C. BARNES-WALL 256D
# ═══════════════════════════════════════════════════════════════════════════════════

def run_barnes_wall():
    print(f"\n{'=' * 80}")
    print("PHASE VI-C: BARNES-WALL 256D — Quaternary vectors for pitches")
    print(f"{'=' * 80}")
    print("  BW256 generates 256-dimensional vectors with entries in {0,1,2,3}.")
    print("  Uses recursive |u|u+v| construction from 24-bit Golay seeds.")

    cw_map = encode_cof_cw_map()

    # Generate 256D vectors for each pitch
    print(f"\n  Generating 256D Barnes-Wall vectors for 12 pitches...")
    pitch_bw = {}
    for pc in range(12):
        seed = cw_map[pc]
        vec256 = bw.generate(seed, 256)
        pitch_bw[pc] = vec256
        hw = sum(1 for x in vec256 if x != 0)
        norm_sq = sum(x * x for x in vec256)
        print(f"  {PITCH_NAMES[pc]:>5s}: HW={hw:>3d}, NormSq={norm_sq:>5d}, NRCI={float(bw.nrci(vec256)):.4f}")

    # Interval Euclidean distances
    print(f"\n  BARNES-WALL 256D EUCLIDEAN DISTANCES:")
    print(f"  {'Interval':>8s} | {'CR':>3s} | {'Avg Euc':>9s} | {'Min Euc':>9s} | {'Max Euc':>9s} | {'Std':>7s}")
    print(f"  {'-'*8} | {'-'*3} | {'-'*9} | {'-'*9} | {'-'*9} | {'-'*7}")

    by_interval = {}
    for pc_a, pc_b in combinations(range(12), 2):
        st = min((pc_b - pc_a) % 12, (pc_a - pc_b) % 12)
        if st == 0: continue
        d = euclidean_dist(pitch_bw[pc_a], pitch_bw[pc_b])
        by_interval.setdefault(st, []).append(d)

    x_vals, y_vals = [], []
    for st in range(1, 7):
        dists = by_interval.get(st, [])
        if not dists: continue
        avg = sum(dists) / len(dists)
        std = math.sqrt(sum((d - avg)**2 for d in dists) / len(dists))
        name = CONSONANCE_MAP[st]
        cr = CONSONANCE_RANK[st]
        x_vals.append(cr)
        y_vals.append(avg)
        print(f"  {name:>8s} | {cr:>3d} | {avg:>9.3f} | {min(dists):>9.3f} | {max(dists):>9.3f} | {std:>7.3f}")

    r = pearson_r(x_vals, y_vals)
    print(f"\n  BW256 Euclidean: Pearson r = {r:.4f}")

    # Chord analysis with BW vectors
    print(f"\n  CHORD ANALYSIS WITH BW256:")
    chords = [
        ("C Maj",    [0,4,7],     "Consonant"),
        ("C Min",    [0,3,7],     "Consonant"),
        ("C Dim",    [0,3,6],     "Moderate"),
        ("C Aug",    [0,4,8],     "Moderate"),
        ("Cluster",  [0,1,2],     "Dissonant"),
        ("Cluster2", [0,1,6],     "Dissonant"),
        ("Maj7",     [0,4,7,11],  "Consonant"),
        ("Dom7",     [0,4,7,10],  "Consonant"),
        ("Dim7",     [0,3,6,9],   "Moderate"),
        ("Diatonic", [0,2,4,5,7,9,11], "Consonant"),
        ("Chrom6",   list(range(6)), "Dissonant"),
        ("Pentatonic",[0,2,4,7,9], "Consonant"),
    ]

    print(f"\n  {'Chord':>12s} | {'#n':>3s} | {'Avg Euc':>9s} | {'Euc Var':>8s} | {'BW NRCI':>8s} | {'Expect':>10s}")
    print(f"  {'-'*12} | {'-'*3} | {'-'*9} | {'-'*8} | {'-'*8} | {'-'*10}")

    chord_results = []
    for name, pcs, expected in chords:
        dists = []
        for a, b in combinations(pcs, 2):
            dists.append(euclidean_dist(pitch_bw[a], pitch_bw[b]))
        avg = sum(dists) / len(dists) if dists else 0
        var = sum((d - avg)**2 for d in dists) / len(dists) if dists else 0

        # Chord as centroid
        centroid = [0] * 256
        for pc in pcs:
            for i in range(256):
                centroid[i] += pitch_bw[pc][i]
        centroid = [c // len(pcs) for c in centroid]  # integer division for BW
        bw_nrci = float(bw.nrci(centroid))

        print(f"  {name:>12s} | {len(pcs):>3d} | {avg:>9.3f} | {var:>8.3f} | {bw_nrci:>8.4f} | {expected:>10s}")
        chord_results.append({"name": name, "expected": expected, "avg_euc": avg, "bw_nrci": bw_nrci})

    # Correlations
    cons_map = {"Consonant": 1, "Moderate": 2, "Mixed": 3, "Ambiguous": 3, "Dissonant": 4}
    xs = [cons_map[r["expected"]] for r in chord_results]
    print(f"\n  BW256 CHORD CORRELATIONS:")
    print(f"    Consonance vs Avg Euclidean: r = {pearson_r(xs, [r['avg_euc'] for r in chord_results]):+.4f}")
    print(f"    Consonance vs BW NRCI:       r = {pearson_r(xs, [r['bw_nrci'] for r in chord_results]):+.4f}")

    # BW256 NRCI for snapped chord vectors
    print(f"\n  BW256 SNAPPED CHORD ANALYSIS:")
    print(f"  (Generate full chord vector, snap it, measure NRCI)")
    print(f"  {'Chord':>12s} | {'#n':>3s} | {'Noisy NRCI':>11s} | {'Snapped NRCI':>12s} | {'Decoder Gain':>13s} | {'Expect':>10s}")
    print(f"  {'-'*12} | {'-'*3} | {'-'*11} | {'-'*12} | {'-'*13} | {'-'*10}")

    snap_results = []
    for name, pcs, expected in chords:
        # Build a 256D "chord vector" by summing pitch vectors
        chord_vec = [0] * 256
        for pc in pcs:
            for i in range(256):
                chord_vec[i] = (chord_vec[i] + pitch_bw[pc][i]) % 4

        noisy_nrci = float(bw.nrci(chord_vec))
        snapped = bw.snap(chord_vec)
        snapped_nrci = float(bw.nrci(snapped))
        gain = snapped_nrci - noisy_nrci

        print(f"  {name:>12s} | {len(pcs):>3d} | {noisy_nrci:>11.4f} | {snapped_nrci:>12.4f} | {gain:>+13.4f} | {expected:>10s}")
        snap_results.append({"name": name, "expected": expected, "gain": gain, "snapped_nrci": snapped_nrci})

    xs = [cons_map[r["expected"]] for r in snap_results]
    print(f"\n    Consonance vs Decoder Gain:  r = {pearson_r(xs, [r['gain'] for r in snap_results]):+.4f}")
    print(f"    Consonance vs Snapped NRCI:   r = {pearson_r(xs, [r['snapped_nrci'] for r in snap_results]):+.4f}")


# ═══════════════════════════════════════════════════════════════════════════════════
# D. LEECH FULL TRIAD SURVEY WITH EUCLIDEAN METRICS
# ═══════════════════════════════════════════════════════════════════════════════════

def run_leech_triad_survey(pitch_leech_sets):
    print(f"\n{'=' * 80}")
    print("PHASE VI-D: COMPLETE TRIAD SURVEY — Leech Euclidean Metrics")
    print(f"{'=' * 80}")

    # Use first Leech point from each pitch's expanded set
    pitch_point = {}
    for pc in range(12):
        pitch_point[pc] = pitch_leech_sets[pc][0]

    print(f"\n  Testing ALL 220 triads using Leech 24D Euclidean distances...")

    triad_types = {
        "Major": [], "Minor": [], "Diminished": [], "Augmented": [],
        "Other consonant": [], "Dissonant cluster": []
    }

    for combo in combinations(range(12), 3):
        iv_set = set(sorted([min((b-a)%12, (a-b)%12) for a, b in combinations(combo, 2)]))

        # Euclidean metrics
        dists = [euclidean_dist(pitch_point[a], pitch_point[b]) for a, b in combinations(combo, 2)]
        avg_euc = sum(dists) / 3
        euc_var = sum((d - avg_euc)**2 for d in dists) / 3

        # Centroid-based NRCI
        centroid = [0.0] * 24
        for pc in combo:
            for i in range(24):
                centroid[i] += pitch_point[pc][i]
        centroid = [c / 3 for c in centroid]
        centroid_int = [max(-2, min(2, round(c / 2) * 2)) for c in centroid]
        nrci = float(l.calculate_nrci(centroid_int))
        tax = float(l.calculate_symmetry_tax(centroid_int))

        # Also: "spread" = max distance - min distance (regularity measure)
        spread = max(dists) - min(dists)

        # Classify
        has_min3 = 3 in iv_set
        has_maj3 = 4 in iv_set
        has_p5 = 7 in iv_set
        has_dim5 = 6 in iv_set
        has_aug5 = 8 in iv_set

        if has_maj3 and has_p5:
            triad_types["Major"].append((avg_euc, euc_var, spread, nrci, tax))
        elif has_min3 and has_p5:
            triad_types["Minor"].append((avg_euc, euc_var, spread, nrci, tax))
        elif has_min3 and has_dim5:
            triad_types["Diminished"].append((avg_euc, euc_var, spread, nrci, tax))
        elif has_maj3 and has_aug5:
            triad_types["Augmented"].append((avg_euc, euc_var, spread, nrci, tax))
        elif has_min3 or has_maj3:
            triad_types["Other consonant"].append((avg_euc, euc_var, spread, nrci, tax))
        else:
            triad_types["Dissonant cluster"].append((avg_euc, euc_var, spread, nrci, tax))

    print(f"\n  {'Triad Type':>20s} | {'#':>3s} | {'Avg Euc':>8s} | {'Euc Std':>8s} | {'Spread':>8s} | {'NRCI':>7s} | {'Tax':>7s}")
    print(f"  {'-'*20} | {'-'*3} | {'-'*8} | {'-'*8} | {'-'*8} | {'-'*7} | {'-'*7}")

    for tname, entries in triad_types.items():
        if not entries: continue
        avg_e = sum(e[0] for e in entries) / len(entries)
        std_e = math.sqrt(sum((e[0]-avg_e)**2 for e in entries) / len(entries))
        avg_sp = sum(e[2] for e in entries) / len(entries)
        avg_nrci = sum(e[3] for e in entries) / len(entries)
        avg_tax = sum(e[4] for e in entries) / len(entries)
        print(f"  {tname:>20s} | {len(entries):>3d} | {avg_e:>8.3f} | {std_e:>8.3f} | {avg_sp:>8.3f} | {avg_nrci:>7.4f} | {avg_tax:>7.4f}")

    # Statistical significance: can we separate consonant triads from clusters?
    consonant_eucs = [e[0] for e in triad_types["Major"] + triad_types["Minor"]]
    dissonant_eucs = [e[0] for e in triad_types["Dissonant cluster"]]
    if consonant_eucs and dissonant_eucs:
        mean_c = sum(consonant_eucs) / len(consonant_eucs)
        mean_d = sum(dissonant_eucs) / len(dissonant_eucs)
        print(f"\n  SEPARATION TEST (Euclidean distance):")
        print(f"    Consonant triads (Maj+Min): mean Euc = {mean_c:.3f}")
        print(f"    Dissonant clusters:           mean Euc = {mean_d:.3f}")
        print(f"    Difference: {abs(mean_c - mean_d):.3f}")
        if mean_c < mean_d:
            print(f"    → Consonant triads are CLOSER in Leech space ✓")
        else:
            print(f"    → Consonant triads are FARTHER in Leech space ✗")


# ═══════════════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("UBP MUSIC STUDY — Phase VI: Leech Lattice & Barnes-Wall 256")
    print("System: ubp_unified_v5.py (live, no mocks)")
    print()

    pitch_leech_sets = run_leech_intervals()
    run_ontological_chords()
    run_barnes_wall()
    run_leech_triad_survey(pitch_leech_sets)

    print(f"\n{'=' * 80}")
    print("Phase VI COMPLETE")
    print(f"{'=' * 80}")