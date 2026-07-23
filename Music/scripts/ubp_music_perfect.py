"""
UBP Music Study — The Perfect Mapping (r=1.0)
==============================================
Analysis D found r=+1.0000 with random 12-bit seeds.
This script finds it again, prints the exact seed assignment,
and investigates what structure it has.
"""

import sys, math, random
from fractions import Fraction
from itertools import combinations

sys.path.insert(0, "/home/z/my-project")
from ubp_unified_v5 import GolayCodeEngine, LeechLatticeEngine

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


def pearson_r(x_vals, y_vals):
    n = len(x_vals)
    if n < 2: return 0.0
    mx, my = sum(x_vals)/n, sum(y_vals)/n
    cov = sum((x-mx)*(y-my) for x,y in zip(x_vals, y_vals))
    vx = sum((x-mx)**2 for x in x_vals)
    vy = sum((y-my)**2 for y in y_vals)
    if vx == 0 or vy == 0: return 0.0
    return cov / math.sqrt(vx * vy)


def measure_corr(cw_map):
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
    return pearson_r(x_vals, y_vals), by_interval


def vec_to_hex(v24):
    r = sum((1 << (7 - i)) for i in range(8) if v24[i])
    gg = sum((1 << (7 - i)) for i in range(8) if v24[8 + i])
    b = sum((1 << (7 - i)) for i in range(8) if v24[16 + i])
    return f"#{r:02x}{gg:02x}{b:02x}"


print("=" * 80)
print("FINDING THE PERFECT MAPPING (r = 1.0)")
print("=" * 80)

# Use the same seed as before
random.seed(42)
best_r = 0
best_seeds = None
best_cw_map = None

print("\n  Searching 100,000 trials...")
for trial in range(100000):
    seeds = set()
    while len(seeds) < 12:
        seeds.add(random.randint(0, 4095))
    seeds = list(seeds)

    cw_map = {}
    for pc in range(12):
        seed_bits = [(seeds[pc] >> (11 - i)) & 1 for i in range(12)]
        cw_map[pc] = g.encode(seed_bits)

    r, _ = measure_corr(cw_map)
    if r > best_r:
        best_r = r
        best_seeds = list(seeds)
        best_cw_map = dict(cw_map)
        if r >= 1.0:
            break

print(f"  Best r = {best_r:.6f}")

if best_r >= 0.95 and best_cw_map:
    print(f"\n  {'='*60}")
    print(f"  SEED ASSIGNMENT FOR THE NEAR-PERFECT MAPPING (r={best_r:.4f})")
    print(f"  {'='*60}")

    print(f"\n  {'Pitch':>5s} | {'Seed (dec)':>10s} | {'Seed (hex)':>10s} | {'CW HW':>6s} | {'NRCI':>7s} | {'Hex':>9s}")
    print(f"  {'-'*5} | {'-'*10} | {'-'*10} | {'-'*6} | {'-'*7} | {'-'*9}")

    for pc in range(12):
        cw = best_cw_map[pc]
        hw = g.hamming_weight(cw)
        nrci = float(l.calculate_nrci(cw))
        hex_col = vec_to_hex(cw)
        print(f"  {PITCH_NAMES[pc]:>5s} | {best_seeds[pc]:>10d} | {best_seeds[pc]:>#10x} | {hw:>6d} | {nrci:>7.4f} | {hex_col:>9s}")

    # Detailed interval breakdown
    r_val, by_interval = measure_corr(best_cw_map)

    print(f"\n  INTERVAL BREAKDOWN:")
    print(f"  {'Interval':>8s} | {'CR':>3s} | {'Avg dH':>7s} | {'Min':>4s} | {'Max':>4s} | {'Var':>6s} | {'All same?':>10s}")
    print(f"  {'-'*8} | {'-'*3} | {'-'*7} | {'-'*4} | {'-'*4} | {'-'*6} | {'-'*10}")

    for st in range(1, 7):
        hds = by_interval.get(st, [])
        if not hds: continue
        avg = sum(hds)/len(hds)
        var = sum((h-avg)**2 for h in hds)/len(hds)
        all_same = len(set(hds)) == 1
        name = CONSONANCE_MAP[st]
        cr = CONSONANCE_RANK[st]
        print(f"  {name:>8s} | {cr:>3d} | {avg:>7.2f} | {min(hds):>4d} | {max(hds):>4d} | {var:>6.2f} | {'YES' if all_same else 'no':>10s}")

    # Check: are the seeds related to a permutation of some structure?
    print(f"\n  SEED STRUCTURE ANALYSIS:")
    print(f"  Seed values: {sorted(best_seeds)}")
    print(f"  Spacings between sorted seeds:")
    sorted_seeds = sorted(best_seeds)
    spacings = [sorted_seeds[i+1] - sorted_seeds[i] for i in range(11)]
    print(f"  {spacings}")

    # Check if it's a multiplicative group structure
    print(f"\n  Checking for multiplicative structure...")
    for modulus in [4096, 2048, 1024, 512, 256, 128, 64, 48, 36, 24, 16, 13, 12]:
        if modulus < max(best_seeds) + 1:
            continue
        for gen in range(2, modulus):
            if math.gcd(gen, modulus) != 1:
                continue
            generated = set()
            curr = 1
            for _ in range(12):
                generated.add(curr % modulus)
                curr = (curr * gen) % modulus
            if generated == set(best_seeds):
                print(f"  FOUND: Multiplicative group mod {modulus}, generator {gen}")
                print(f"  Generated set: {sorted(generated)}")
                break

    # Check: do the seed values, when interpreted as positions in some ordering,
    # correspond to a known musical structure?
    print(f"\n  HAMMING WEIGHT OF EACH SEED:")
    for pc in range(12):
        hw = bin(best_seeds[pc]).count('1')
        print(f"    {PITCH_NAMES[pc]:>5s}: seed={best_seeds[pc]:>4d} ({best_seeds[pc]:>4x}), HW={hw}")

    # Now: test this mapping with CHORDS
    print(f"\n  {'='*60}")
    print(f"  CHORD TEST WITH PERFECT MAPPING")
    print(f"  {'='*60}")

    chords = [
        ("C Maj",  [0,4,7],     "Consonant"),
        ("C Min",  [0,3,7],     "Consonant"),
        ("C Dim",  [0,3,6],     "Moderate"),
        ("C Aug",  [0,4,8],     "Moderate"),
        ("Cluster",[0,1,2],     "Dissonant"),
        ("Maj7",   [0,4,7,11],  "Consonant"),
        ("Dom7",   [0,4,7,10],  "Consonant"),
        ("Dim7",   [0,3,6,9],   "Moderate"),
        ("Diatonic",[0,2,4,5,7,9,11], "Consonant"),
        ("Chrom6", list(range(6)), "Dissonant"),
    ]

    print(f"\n  {'Chord':>12s} | {'#notes':>6s} | {'Avg dH':>7s} | {'dH Var':>7s} | {'Min dH':>7s} | {'Max dH':>7s} | {'XOR HW':>7s} | {'XOR NRCI':>8s} | {'Expect':>10s}")
    print(f"  {'-'*12} | {'-'*6} | {'-'*7} | {'-'*7} | {'-'*7} | {'-'*7} | {'-'*7} | {'-'*8} | {'-'*10}")

    for name, pcs, expected in chords:
        # Pairwise dH
        distances = []
        for a, b in combinations(pcs, 2):
            hd = sum(x ^ y for x, y in zip(best_cw_map[a], best_cw_map[b]))
            distances.append(hd)
        avg = sum(distances)/len(distances) if distances else 0
        var = sum((d-avg)**2 for d in distances)/len(distances) if distances else 0

        # XOR chord
        xor_cw = list(best_cw_map[pcs[0]])
        for pc in pcs[1:]:
            xor_cw = [a ^ b for a, b in zip(xor_cw, best_cw_map[pc])]
        xor_hw = g.hamming_weight(xor_cw)
        xor_nrci = float(l.calculate_nrci(xor_cw))

        print(f"  {name:>12s} | {len(pcs):>6d} | {avg:>7.2f} | {var:>7.2f} | {min(distances) if distances else 0:>7d} | {max(distances) if distances else 0:>7d} | {xor_hw:>7d} | {xor_nrci:>8.4f} | {expected:>10s}")

    # Triad-level analysis
    print(f"\n  FULL TRIAD SURVEY WITH PERFECT MAPPING:")
    triad_types = {
        "Major": [], "Minor": [], "Diminished": [], "Augmented": [],
        "Other consonant": [], "Dissonant cluster": []
    }
    for combo in combinations(range(12), 3):
        iv_set = set(sorted([min((b-a)%12, (a-b)%12) for a, b in combinations(combo, 2)]))
        xor_cw = list(best_cw_map[combo[0]])
        for pc in combo[1:]:
            xor_cw = [a ^ b for a, b in zip(xor_cw, best_cw_map[pc])]
        xor_hw = g.hamming_weight(xor_cw)

        has_min3 = 3 in iv_set
        has_maj3 = 4 in iv_set
        has_p5 = 7 in iv_set
        has_dim5 = 6 in iv_set
        has_aug5 = 8 in iv_set

        if has_maj3 and has_p5:
            triad_types["Major"].append(xor_hw)
        elif has_min3 and has_p5:
            triad_types["Minor"].append(xor_hw)
        elif has_min3 and has_dim5:
            triad_types["Diminished"].append(xor_hw)
        elif has_maj3 and has_aug5:
            triad_types["Augmented"].append(xor_hw)
        elif has_min3 or has_maj3:
            triad_types["Other consonant"].append(xor_hw)
        else:
            triad_types["Dissonant cluster"].append(xor_hw)

    print(f"\n  {'Triad Type':>20s} | {'Count':>5s} | {'Avg XOR HW':>10s} | {'Min HW':>7s} | {'Max HW':>7s} | {'%Octad':>7s}")
    print(f"  {'-'*20} | {'-'*5} | {'-'*10} | {'-'*7} | {'-'*7} | {'-'*7}")
    for tname, hws in triad_types.items():
        if not hws: continue
        avg = sum(hws)/len(hws)
        pct = sum(1 for h in hws if h == 8)/len(hws)*100
        print(f"  {tname:>20s} | {len(hws):>5d} | {avg:>10.2f} | {min(hws):>7d} | {max(hws):>7d} | {pct:>6.0f}%")

print(f"\n{'=' * 80}")
print("DONE")
print(f"{'=' * 80}")