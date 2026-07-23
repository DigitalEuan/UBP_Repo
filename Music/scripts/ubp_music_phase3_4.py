"""
UBP Music Study — Phase III: Chordal Synthesis & Phase IV: Encoding Search
===========================================================================
Phase III: Triads as geometric objects in the Golay space.
  - XOR-based chord representation (chord = XOR of its pitch codewords)
  - Measure: XOR weight, NRCI, tax, and hex colour for each chord
  - Compare: Major, Minor, Diminished, Augmented triads vs dissonant clusters

Phase IV: Why does Circle-of-Fifths Gray work?
  - Exhaustive search over all 12! permutations of pitch-to-seed mapping
  - (Feasible because we only need to test correlation for each permutation)
  - Also: test all 2048 possible 12-bit seed assignments directly

Uses ONLY the live UBP system.
"""

import sys, math, random, time
from fractions import Fraction
from itertools import combinations, permutations

sys.path.insert(0, "/home/z/my-project")
from ubp_unified_v5 import GolayCodeEngine, LeechLatticeEngine

g = GolayCodeEngine()
l = LeechLatticeEngine(g)

# ── Reuse encoding helpers from Phase I ──────────────────────────────────────────

def gray_code(n: int, bits: int) -> list:
    gc = n ^ (n >> 1)
    return [(gc >> (bits - 1 - i)) & 1 for i in range(bits)]

COF_POSITION = {0:0, 7:1, 2:2, 9:3, 4:4, 11:5, 6:6, 1:7, 8:8, 3:9, 10:10, 5:11}

def fifths_12bit(pitch: int) -> list:
    return gray_code(COF_POSITION[pitch], 12)

def vec_to_hex(v24: list) -> str:
    r = sum((1 << (7 - i)) for i in range(8) if v24[i])
    gg = sum((1 << (7 - i)) for i in range(8) if v24[8 + i])
    b = sum((1 << (7 - i)) for i in range(8) if v24[16 + i])
    return f"#{r:02x}{gg:02x}{b:02x}"

PITCH_NAMES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
CONSONANCE_MAP = {
    0: "Unison", 1: "Minor 2nd", 2: "Major 2nd", 3: "Minor 3rd",
    4: "Major 3rd", 5: "Perfect 4th", 6: "Tritone", 7: "Perfect 5th",
    8: "Minor 6th", 9: "Major 6th", 10: "Minor 7th", 11: "Major 7th"
}
CONSONANCE_RANK = {
    0: 1, 7: 2, 5: 3, 4: 3, 9: 3, 3: 4, 8: 4, 10: 4, 2: 5, 11: 5, 1: 6, 6: 6
}


def pearson_r(x_vals, y_vals):
    n = len(x_vals)
    if n < 2:
        return 0.0
    mx = sum(x_vals) / n
    my = sum(y_vals) / n
    cov = sum((x - mx) * (y - my) for x, y in zip(x_vals, y_vals))
    vx = sum((x - mx)**2 for x in x_vals)
    vy = sum((y - my)**2 for y in y_vals)
    if vx == 0 or vy == 0:
        return 0.0
    return cov / math.sqrt(vx * vy)


# ═══════════════════════════════════════════════════════════════════════════════════
# PHASE III: CHORDAL SYNTHESIS
# ═══════════════════════════════════════════════════════════════════════════════════

def encode_all_pitches(enc_func):
    """Encode all 12 pitch classes, return dict of pc -> 24-bit codeword."""
    pitch_cw = {}
    for pc in range(12):
        seed12 = enc_func(pc)
        cw24 = g.encode(seed12)
        pitch_cw[pc] = cw24
    return pitch_cw


def xor_chord(pitches, pitch_cw):
    """XOR all pitch codewords together to get a chord codeword."""
    result = list(pitch_cw[pitches[0]])
    for pc in pitches[1:]:
        result = [a ^ b for a, b in zip(result, pitch_cw[pc])]
    return result


def chord_pairwise_avg_hd(pitches, pitch_cw):
    """Average Hamming distance between all pairs of pitches in the chord."""
    if len(pitches) < 2:
        return 0.0
    total = 0
    count = 0
    for a, b in combinations(pitches, 2):
        total += sum(x ^ y for x, y in zip(pitch_cw[a], pitch_cw[b]))
        count += 1
    return total / count


def run_phase3():
    print("=" * 80)
    print("PHASE III: CHORDAL SYNTHESIS — Triads as Geometric Objects")
    print("=" * 80)
    print("\n  Using Circle-of-Fifths Gray encoding (best performer from Phase II)")
    print("  Chord = XOR of constituent pitch codewords (linear code property)")

    pitch_cw = encode_all_pitches(fifths_12bit)

    # Define chords: (name, pitch_classes, expected_consonance)
    chords = [
        ("C Major",       [0, 4, 7],    "Consonant"),
        ("C Minor",       [0, 3, 7],    "Consonant"),
        ("C Diminished",  [0, 3, 6],    "Moderate"),
        ("C Augmented",   [0, 4, 8],    "Moderate"),
        ("C Sus4",        [0, 5, 7],    "Consonant"),
        ("Cluster 0-1-2", [0, 1, 2],    "Dissonant"),
        ("Cluster 0-1-6", [0, 1, 6],    "Dissonant"),
        ("Trichord 0-1-7",[0, 1, 7],    "Mixed"),
        ("Major 7th",     [0, 4, 7, 11],"Consonant"),
        ("Dom 7th",       [0, 4, 7, 10],"Consonant"),
        ("Dim 7th",       [0, 3, 6, 9], "Moderate"),
        ("Whole Tone",    [0, 2, 4, 6, 8, 10], "Ambiguous"),
        ("Chromatic 6",   [0, 1, 2, 3, 4, 5],  "Dissonant"),
        ("Diatonic",      [0, 2, 4, 5, 7, 9, 11], "Consonant"),
    ]

    print(f"\n  {'Chord':>20s} | {'Pitches':>20s} | {'XOR HW':>7s} | {'NRCI':>7s} | {'Tax':>7s} | {'Avg dH':>7s} | {'Hex':>9s} | {'Expect':>10s}")
    print(f"  {'-'*20} | {'-'*20} | {'-'*7} | {'-'*7} | {'-'*7} | {'-'*7} | {'-'*9} | {'-'*10}")

    results = []
    for name, pcs, expected in chords:
        xor_cw = xor_chord(pcs, pitch_cw)
        xor_hw = g.hamming_weight(xor_cw)
        xor_tax = l.calculate_symmetry_tax(xor_cw)
        xor_nrci = l.calculate_nrci(xor_cw)
        xor_hex = vec_to_hex(xor_cw)
        avg_hd = chord_pairwise_avg_hd(pcs, pitch_cw)

        pcs_str = "-".join(PITCH_NAMES[p] for p in pcs)
        print(f"  {name:>20s} | {pcs_str:>20s} | {xor_hw:>7d} | {float(xor_nrci):>7.4f} | {float(xor_tax):>7.4f} | {avg_hd:>7.2f} | {xor_hex:>9s} | {expected:>10s}")
        results.append({
            "name": name, "pcs": pcs, "expected": expected,
            "xor_hw": xor_hw, "nrci": float(xor_nrci), "tax": float(xor_tax),
            "avg_hd": avg_hd, "hex": xor_hex
        })

    # Analysis: Do consonant chords have lower XOR weight?
    print(f"\n  {'─' * 60}")
    print("  ANALYSIS: Expected Consonance vs XOR Weight")
    cons_map = {"Consonant": 1, "Moderate": 2, "Mixed": 3, "Ambiguous": 3, "Dissonant": 4}
    x_vals = [cons_map[r["expected"]] for r in results]
    y_vals = [r["xor_hw"] for r in results]
    r = pearson_r(x_vals, y_vals)
    print(f"  Pearson r = {r:.4f} (higher XOR weight → more dissonant?)")

    # Also: NRCI of chord codeword
    x2 = [cons_map[r["expected"]] for r in results]
    y2 = [r["nrci"] for r in results]
    r2 = pearson_r(x2, y2)
    print(f"  Consonance vs Chord NRCI: r = {r2:.4f} (higher NRCI → more consonant?)")

    # All triads (3-note chords) — complete survey
    print(f"\n  {'─' * 60}")
    print("  COMPLETE TRIAD SURVEY: All 220 unique 3-note pitch-class sets")
    print(f"  (categorized by standard music theory)")
    triad_types = {
        "Major": [], "Minor": [], "Diminished": [], "Augmented": [],
        "Other consonant": [], "Dissonant cluster": []
    }
    for combo in combinations(range(12), 3):
        intervals = sorted([
            min((b - a) % 12, (a - b) % 12)
            for a, b in combinations(combo, 2)
        ])
        xor_cw = xor_chord(combo, pitch_cw)
        xor_hw = g.hamming_weight(xor_cw)
        xor_nrci = float(l.calculate_nrci(xor_cw))

        # Classify
        if intervals in [[3, 4, 7], [4, 5, 8]]:  # Major: M3+m3 or m3+M3 wrapping
            # Actually, let's be more precise
            pass
        # Simpler: check interval content
        iv_set = set(intervals)
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

    print(f"\n  {'Triad Type':>20s} | {'Count':>5s} | {'Avg XOR HW':>10s} | {'Min HW':>7s} | {'Max HW':>7s} | {'% Octad(8)':>10s}")
    print(f"  {'-'*20} | {'-'*5} | {'-'*10} | {'-'*7} | {'-'*7} | {'-'*10}")
    for tname, hws in triad_types.items():
        if not hws:
            continue
        avg = sum(hws) / len(hws)
        pct_octad = sum(1 for h in hws if h == 8) / len(hws) * 100
        print(f"  {tname:>20s} | {len(hws):>5d} | {avg:>10.2f} | {min(hws):>7d} | {max(hws):>7d} | {pct_octad:>9.0f}%")

    return results, triad_types


# ═══════════════════════════════════════════════════════════════════════════════════
# PHASE IV: WHY DOES CIRCLE-OF-FIFTHS WORK? — Exhaustive Search
# ═══════════════════════════════════════════════════════════════════════════════════

def compute_correlation_for_mapping(cw_map):
    """
    Given a dict {pitch_class: 24-bit_codeword}, compute Pearson r
    between consonance rank and Hamming distance for all 66 intervals.
    Only considers intervals 1-6 semitones (unordered).
    """
    by_interval = {}
    for pc_a, pc_b in combinations(range(12), 2):
        st = min((pc_b - pc_a) % 12, (pc_a - pc_b) % 12)
        if st == 0:
            continue
        hd = sum(x ^ y for x, y in zip(cw_map[pc_a], cw_map[pc_b]))
        by_interval.setdefault(st, []).append(hd)

    x_vals, y_vals = [], []
    for st in range(1, 12):
        hds = by_interval.get(st, [])
        if not hds:
            continue
        x_vals.append(CONSONANCE_RANK[st])
        y_vals.append(sum(hds) / len(hds))

    return pearson_r(x_vals, y_vals)


def run_phase4_seed_search():
    """
    Phase IV-A: Instead of searching 12! permutations, we note that the
    encoding function maps pitch -> 12-bit seed -> 24-bit codeword.
    The seed determines everything. There are 4096 possible 12-bit seeds,
    but we only use 12 of them (one per pitch). The KEY variable is which
    12 seeds we choose and how we assign them to pitches.

    Strategy: Search over a large sample of random 12-seed assignments,
    measure correlation each time.
    """
    print("=" * 80)
    print("PHASE IV: WHY DOES CIRCLE-OF-FIFTHS GRAY WORK?")
    print("=" * 80)

    # IV-A: How much of the correlation comes from the Gray code structure
    # vs the Circle-of-Fifths ordering?
    print(f"\n  {'─' * 60}")
    print("  IV-A: Sensitivity to pitch ordering (fixed Gray code, permute assignment)")
    print(f"  {'─' * 60}")

    # Test specific orderings with Gray code
    orderings = {
        "Chromatic (C,C#,D,...)": list(range(12)),
        "Circle of Fifths": [0, 7, 2, 9, 4, 11, 6, 1, 8, 3, 10, 5],
        "Circle of Fourths": [0, 5, 10, 3, 8, 1, 6, 11, 4, 9, 2, 7],
        "Major Thirds": [0, 4, 8, 1, 5, 9, 2, 6, 10, 3, 7, 11],
        "Minor Thirds": [0, 3, 6, 9, 1, 4, 7, 10, 2, 5, 8, 11],
        "Tritone Split": [0, 6, 1, 7, 2, 8, 3, 9, 4, 10, 5, 11],
        "Reverse Chromatic": list(range(11, -1, -1)),
    }

    print(f"\n  {'Ordering':>30s} | {'Pearson r':>9s} | {'R²':>7s} | {'Assessment':>15s}")
    print(f"  {'-'*30} | {'-'*9} | {'-'*7} | {'-'*15}")

    best_r = -2
    best_name = ""
    for name, ordering in orderings.items():
        # Map: pitch_class -> position_in_ordering -> gray_code -> codeword
        cw_map = {}
        for pitch_class in range(12):
            pos = ordering.index(pitch_class)
            seed = gray_code(pos, 12)
            cw_map[pitch_class] = g.encode(seed)

        r = compute_correlation_for_mapping(cw_map)
        strength = "STRONG" if abs(r) > 0.7 else "moderate" if abs(r) > 0.4 else "weak"
        print(f"  {name:>30s} | {r:>+9.4f} | {r**2:>7.4f} | {strength:>15s}")
        if abs(r) > abs(best_r):
            best_r = r
            best_name = name

    print(f"\n  Best ordering: {best_name} (r = {best_r:+.4f})")

    # IV-B: Random permutation search
    print(f"\n  {'─' * 60}")
    print("  IV-B: Random permutation search (10,000 samples)")
    print(f"  {'─' * 60}")

    random.seed(42)
    n_samples = 10000
    r_values = []
    r_abs_values = []
    count_above_07 = 0
    count_above_08 = 0
    count_above_086 = 0  # our CoF baseline
    best_perm_r = -2
    best_perm = None

    base_order = list(range(12))
    for i in range(n_samples):
        perm = list(base_order)
        random.shuffle(perm)
        cw_map = {}
        for pitch_class in range(12):
            pos = perm.index(pitch_class)
            seed = gray_code(pos, 12)
            cw_map[pitch_class] = g.encode(seed)

        r = compute_correlation_for_mapping(cw_map)
        r_values.append(r)
        r_abs_values.append(abs(r))
        if abs(r) > 0.7: count_above_07 += 1
        if abs(r) > 0.8: count_above_08 += 1
        if abs(r) > 0.86: count_above_086 += 1
        if abs(r) > abs(best_perm_r):
            best_perm_r = r
            best_perm = perm

    print(f"\n  Distribution of |r| over {n_samples} random permutations:")
    print(f"    Mean |r|:   {sum(r_abs_values)/len(r_abs_values):.4f}")
    print(f"    Median |r|: {sorted(r_abs_values)[n_samples//2]:.4f}")
    print(f"    Max |r|:    {max(r_abs_values):.4f}")
    print(f"    |r| > 0.7:  {count_above_07}/{n_samples} ({count_above_07/n_samples*100:.1f}%)")
    print(f"    |r| > 0.8:  {count_above_08}/{n_samples} ({count_above_08/n_samples*100:.1f}%)")
    print(f"    |r| > 0.86: {count_above_086}/{n_samples} ({count_above_086/n_samples*100:.1f}%)")

    if best_perm:
        perm_names = [PITCH_NAMES[p] for p in best_perm]
        print(f"\n  Best random permutation (r={best_perm_r:+.4f}):")
        print(f"    Order: {perm_names}")
        # Check what musical structure this is
        # Compute intervals between consecutive elements
        intervals = [(best_perm[(i+1) % 12] - best_perm[i]) % 12 for i in range(12)]
        interval_names = [CONSONANCE_MAP[iv] for iv in intervals]
        print(f"    Step intervals: {intervals}")
        print(f"    Step names:     {interval_names}")

    # IV-C: What if we use raw binary (not Gray code)?
    print(f"\n  {'─' * 60}")
    print("  IV-C: Raw binary vs Gray code (Circle-of-Fifths ordering)")
    print(f"  {'─' * 60}")

    cof_order = [0, 7, 2, 9, 4, 11, 6, 1, 8, 3, 10, 5]

    # Gray code
    cw_map_gray = {}
    for pitch_class in range(12):
        pos = cof_order.index(pitch_class)
        seed = gray_code(pos, 12)
        cw_map_gray[pitch_class] = g.encode(seed)
    r_gray = compute_correlation_for_mapping(cw_map_gray)
    print(f"  Gray code (CoF):        r = {r_gray:+.4f}")

    # Raw binary
    cw_map_raw = {}
    for pitch_class in range(12):
        pos = cof_order.index(pitch_class)
        seed = [(pos >> (11 - i)) & 1 for i in range(12)]
        cw_map_raw[pitch_class] = g.encode(seed)
    r_raw = compute_correlation_for_mapping(cw_map_raw)
    print(f"  Raw binary (CoF):       r = {r_raw:+.4f}")

    # IV-D: Hex colour analysis for CoF encoding
    print(f"\n  {'─' * 60}")
    print("  IV-D: HEX COLOUR MAP (Circle-of-Fifths Gray encoding)")
    print(f"  {'─' * 60}")
    print(f"\n  Visualizing the 12 pitch classes as colours on the CoF wheel:\n")
    print(f"  Position | Pitch | Hex Colour    | NRCI   | HW")
    print(f"  -------- | ----- | ------------- | ------ | --")
    for pos in range(12):
        pc = cof_order[pos]
        seed = gray_code(pos, 12)
        cw = g.encode(seed)
        hw = g.hamming_weight(cw)
        nrci = float(l.calculate_nrci(cw))
        hex_col = vec_to_hex(cw)
        print(f"  {pos:>8d} | {PITCH_NAMES[pc]:>5s} | {hex_col:>13s} | {nrci:.4f} | {hw:>2d}")


# ═══════════════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("UBP MUSIC STUDY — Phase III & IV")
    print("System: ubp_unified_v5.py (live, no mocks)")
    print()

    chord_results, triad_survey = run_phase3()
    run_phase4_seed_search()

    print(f"\n{'=' * 80}")
    print("Phase III & IV COMPLETE")
    print(f"{'=' * 80}")