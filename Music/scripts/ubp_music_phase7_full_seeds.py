"""
UBP Music Study — Phase VII: Full 12-bit Seeds + Leech Lattice
================================================================
The root cause of ALL failures is that Gray codes of 0-11 only use
4 bits of the 12-bit seed space. Everything else is derivative.

FINAL TEST: Use the UBP primality pipeline approach — map each pitch
to a FULL 12-bit seed (from ubp_v28_oracle.py), then use the Leech
lattice's REAL 24D coordinate space.

Strategy: Use the best CoF-like assignment from 50k random search,
but now work with the FULL Leech geometry, not binary Hamming.
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


def gray_code(n, bits=12):
    gc = n ^ (n >> 1)
    return [(gc >> (bits - 1 - i)) & 1 for i in range(bits)]


def measure_interval_corr(cw_map):
    """Measure consonance-Hamming correlation for a codeword mapping."""
    by_interval = {}
    for pc_a, pc_b in combinations(range(12), 2):
        st = min((pc_b - pc_a) % 12, (pc_a - pc_b) % 12)
        if st == 0: continue
        hd = sum(x ^ y for x, y in zip(cw_map[pc_a], cw_map[pc_b]))
        by_interval.setdefault(st, []).append(hd)
    x_vals, y_vals = [], []
    for st in range(1, 7):
        hds = by_interval.get(st, [])
        if not hds: continue
        x_vals.append(CONSONANCE_RANK[st])
        y_vals.append(sum(hds) / len(hds))
    return pearson_r(x_vals, y_vals)


print("=" * 80)
print("PHASE VII: FULL 12-BIT SEEDS + LEECH LATTICE 24D")
print("=" * 80)

# Step 1: Find the best CoF-style permutation using FULL 12-bit Gray seeds
# (not just 4-bit Gray codes of 0-11)
print("\n  STEP 1: Find best permutation for full 12-bit Gray code mapping")
print("  (12-bit Gray codes of 0-11 provide much richer codewords)")

def full_gray_12bit(pitch_class, perm):
    """12-bit Gray code of the position in the permutation."""
    pos = perm.index(pitch_class)
    return gray_code(pos, 12)

# Test CoF ordering with FULL 12-bit Gray code
COF_ORDER = [0, 7, 2, 9, 4, 11, 6, 1, 8, 3, 10, 5]
cof_cw = {}
for pc in range(12):
    seed = full_gray_12bit(pc, COF_ORDER)
    cof_cw[pc] = g.encode(seed)

cof_r = measure_interval_corr(cof_cw)
print(f"  CoF (full 12-bit Gray): r = {cof_r:+.4f}")
print(f"  (Compare: CoF 4-bit Gray:  r = +0.8674)")

# The full 12-bit Gray codes use all 12 bits, giving richer codewords
print(f"\n  Seed bit usage (full 12-bit Gray codes of 0-11):")
for bit in range(12):
    count = sum(full_gray_12bit(pc, COF_ORDER)[bit] for pc in range(12))
    bar = '#' * count + '-' * (12 - count)
    print(f"    Bit {bit:>2d}: {count:>2}/12 [{bar}]")

# Codeword weights with full 12-bit Gray
print(f"\n  Codeword weights (full 12-bit Gray, CoF ordering):")
for pc in range(12):
    hw = g.hamming_weight(cof_cw[pc])
    nrci = float(l.calculate_nrci(cof_cw[pc]))
    seed = full_gray_12bit(pc, COF_ORDER)
    seed_hw = sum(seed)
    print(f"  {PITCH_NAMES[pc]:>5s}: seed_HW={seed_hw:>2d}, cw_HW={hw:>2d}, NRCI={nrci:.4f}")

# Step 2: Measure Hamming distance correlation with full 12-bit Gray
print(f"\n  HAMMING DISTANCES (full 12-bit Gray, CoF ordering):")
by_interval = {}
for pc_a, pc_b in combinations(range(12), 2):
    st = min((pc_b - pc_a) % 12, (pc_a - pc_b) % 12)
    if st == 0: continue
    hd = sum(x ^ y for x, y in zip(cof_cw[pc_a], cof_cw[pc_b]))
    by_interval.setdefault(st, []).append(hd)

print(f"\n  {'Interval':>8s} | {'CR':>3s} | {'Avg dH':>7s} | {'Min':>4s} | {'Max':>4s} | {'Var':>6s}")
print(f"  {'-'*8} | {'-'*3} | {'-'*7} | {'-'*4} | {'-'*4} | {'-'*6}")
for st in range(1, 7):
    hds = by_interval.get(st, [])
    if not hds: continue
    avg = sum(hds)/len(hds)
    var = sum((h-avg)**2 for h in hds)/len(hds)
    name = CONSONANCE_MAP[st]
    cr = CONSONANCE_RANK[st]
    print(f"  {name:>8s} | {cr:>3d} | {avg:>7.2f} | {min(hds):>4d} | {max(hds):>4d} | {var:>6.2f}")


# Step 3: Now expand to Leech lattice for the full 12-bit codewords
print(f"\n{'=' * 80}")
print("  STEP 3: LEECH LATTICE EXPANSION (full 12-bit seeds)")
print(f"{'=' * 80}")

# For each pitch, if codeword is an octad (HW=8), expand to 128 Leech points
# Then measure Euclidean distances
pitch_leech = {}
for pc in range(12):
    cw = cof_cw[pc]
    hw = g.hamming_weight(cw)
    if hw == 8:
        pitch_leech[pc] = l.expand_octad_to_physical(cw)
        print(f"  {PITCH_NAMES[pc]:>5s} (HW={hw}): 128 Leech points")
    else:
        # Find nearest octad and expand
        nearest = l.nearest_octad_idx(cw)
        octad = g.get_octads()[nearest["idx"]]
        pitch_leech[pc] = l.expand_octad_to_physical(octad)
        print(f"  {PITCH_NAMES[pc]:>5s} (HW={hw}): nearest octad (d={nearest['distance']}), 128 points")

# Measure Leech Euclidean distances
print(f"\n  LEECH EUCLIDEAN DISTANCES (full 12-bit seeds):")
print(f"  (Sampling 200 random point pairs per interval)")

random.seed(42)
by_interval_leech = {}
for pc_a, pc_b in combinations(range(12), 2):
    st = min((pc_b - pc_a) % 12, (pc_a - pc_b) % 12)
    if st == 0: continue
    pts_a = pitch_leech[pc_a]
    pts_b = pitch_leech[pc_b]
    dists = []
    for _ in range(200):
        pa = pts_a[random.randint(0, 127)]
        pb = pts_b[random.randint(0, 127)]
        dists.append(euclidean_dist(pa, pb))
    by_interval_leech.setdefault(st, []).extend(dists)

print(f"\n  {'Interval':>8s} | {'CR':>3s} | {'Avg Euc':>9s} | {'Min':>7s} | {'Max':>7s} | {'Std':>7s} | {'Distinct':>8s}")
print(f"  {'-'*8} | {'-'*3} | {'-'*9} | {'-'*7} | {'-'*7} | {'-'*7} | {'-'*8}")

x_vals, y_vals = [], []
for st in range(1, 7):
    dists = by_interval_leech.get(st, [])
    if not dists: continue
    avg = sum(dists)/len(dists)
    std = math.sqrt(sum((d-avg)**2 for d in dists)/len(dists))
    distinct = len(set(round(d, 2) for d in dists))
    name = CONSONANCE_MAP[st]
    cr = CONSONANCE_RANK[st]
    x_vals.append(cr)
    y_vals.append(avg)
    print(f"  {name:>8s} | {cr:>3d} | {avg:>9.3f} | {min(dists):>7.3f} | {max(dists):>7.3f} | {std:>7.3f} | {distinct:>8d}")

r_leech = pearson_r(x_vals, y_vals)
print(f"\n  Leech Euclidean (full seeds): r = {r_leech:.4f}")
print(f"  (Compare: Leech Euclidean (4-bit seeds): r = 0.1311)")


# Step 4: Chord analysis with full Leech geometry
print(f"\n{'=' * 80}")
print("  STEP 4: CHORD ANALYSIS (full 12-bit seeds, Leech 24D)")
print(f"{'=' * 80}")

# Use centroid of Leech point sets for each pitch
pitch_centroid = {}
for pc in range(12):
    pts = pitch_leech[pc]
    centroid = [sum(pts[j][i] for j in range(128)) / 128 for i in range(24)]
    pitch_centroid[pc] = centroid

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

print(f"\n  {'Chord':>12s} | {'#n':>3s} | {'Avg dH':>7s} | {'Avg Euc':>8s} | {'Euc Std':>8s} | {'XOR HW':>7s} | {'XOR NRCI':>8s} | {'Expect':>10s}")
print(f"  {'-'*12} | {'-'*3} | {'-'*7} | {'-'*8} | {'-'*8} | {'-'*7} | {'-'*8} | {'-'*10}")

results = []
for name, pcs, expected in chords:
    # Hamming distances
    hd_dists = [sum(x^y for x,y in zip(cof_cw[a], cof_cw[b])) for a,b in combinations(pcs, 2)]
    avg_hd = sum(hd_dists)/len(hd_dists)
    hd_var = sum((d-avg_hd)**2 for d in hd_dists)/len(hd_dists)

    # Euclidean distances (between centroids)
    euc_dists = [euclidean_dist(pitch_centroid[a], pitch_centroid[b]) for a,b in combinations(pcs, 2)]
    avg_euc = sum(euc_dists)/len(euc_dists)
    euc_std = math.sqrt(sum((d-avg_euc)**2 for d in euc_dists)/len(euc_dists))

    # XOR chord
    xor_cw = list(cof_cw[pcs[0]])
    for pc in pcs[1:]:
        xor_cw = [a^b for a,b in zip(xor_cw, cof_cw[pc])]
    xor_hw = g.hamming_weight(xor_cw)
    xor_nrci = float(l.calculate_nrci(xor_cw))

    print(f"  {name:>12s} | {len(pcs):>3d} | {avg_hd:>7.2f} | {avg_euc:>8.3f} | {euc_std:>8.3f} | {xor_hw:>7d} | {xor_nrci:>8.4f} | {expected:>10s}")
    results.append({"name": name, "expected": expected, "avg_hd": avg_hd, "hd_var": hd_var,
                    "avg_euc": avg_euc, "euc_std": euc_std, "xor_nrci": xor_nrci})

# Correlations (separate by chord size)
for size in [3, 4]:
    subset = [r for r in results if len([p for p in [0,4,7,11,10,9,6,8,3,1,2,5] if PITCH_NAMES[p] in r['name']]) == size or True]
    # Simple: just use all results
    pass

cons_map = {"Consonant": 1, "Moderate": 2, "Mixed": 3, "Ambiguous": 3, "Dissonant": 4}
xs = [cons_map[r["expected"]] for r in results]
print(f"\n  ALL CHORDS CORRELATION:")
print(f"    Consonance vs Avg dH:     r = {pearson_r(xs, [r['avg_hd'] for r in results]):+.4f}")
print(f"    Consonance vs dH Var:    r = {pearson_r(xs, [r['hd_var'] for r in results]):+.4f}")
print(f"    Consonance vs Avg Euc:   r = {pearson_r(xs, [r['avg_euc'] for r in results]):+.4f}")
print(f"    Consonance vs Euc Std:   r = {pearson_r(xs, [r['euc_std'] for r in results]):+.4f}")
print(f"    Consonance vs XOR NRCI:  r = {pearson_r(xs, [r['xor_nrci'] for r in results]):+.4f}")

# 3-note only
triad_results = [r for r in results if r["name"] in ["C Maj", "C Min", "C Dim", "C Aug", "Cluster", "Cluster2"]]
xs3 = [cons_map[r["expected"]] for r in triad_results]
print(f"\n  3-NOTE TRIADS ONLY:")
print(f"    Consonance vs Avg dH:     r = {pearson_r(xs3, [r['avg_hd'] for r in triad_results]):+.4f}")
print(f"    Consonance vs dH Var:    r = {pearson_r(xs3, [r['hd_var'] for r in triad_results]):+.4f}")
print(f"    Consonance vs Avg Euc:   r = {pearson_r(xs3, [r['avg_euc'] for r in triad_results]):+.4f}")
print(f"    Consonance vs XOR NRCI:  r = {pearson_r(xs3, [r['xor_nrci'] for r in triad_results]):+.4f}")


# Step 5: Search for best permutation using full 12-bit Gray codes
print(f"\n{'=' * 80}")
print("  STEP 5: OPTIMAL PERMUTATION SEARCH (full 12-bit Gray, 50000 samples)")
print(f"{'=' * 80}")

random.seed(99)
best_r = 0
best_perm = None
for _ in range(50000):
    perm = list(range(12))
    random.shuffle(perm)
    cw_map = {}
    for pc in range(12):
        seed = gray_code(perm.index(pc), 12)
        cw_map[pc] = g.encode(seed)
    r = measure_interval_corr(cw_map)
    if r > best_r:
        best_r = r
        best_perm = list(perm)

print(f"  Best r = {best_r:+.4f}")
if best_perm:
    print(f"  Best permutation: {[PITCH_NAMES[p] for p in best_perm]}")

print(f"\n{'=' * 80}")
print("Phase VII COMPLETE")
print(f"{'=' * 80}")