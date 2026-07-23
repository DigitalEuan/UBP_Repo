"""
UBP Music Study — FINAL SYNTHESIS & ADDITIONAL INVESTIGATIONS
===============================================================
Key findings so far demand deeper investigation:
1. The R block is ALWAYS zero — all information is in G and B blocks
2. 39 four-note chords XOR to 0 (not just Major 7th) — this is a linear algebra property
3. The top permutations (r=0.977) are NOT musically meaningful generators
4. The CoF ranking is ~#1637 out of 50000 — top 3.3%, but not exceptional

New investigations:
A. WHY is the R block zero? (Generator matrix structure analysis)
B. What do the 39 "XOR-closed" 4-note chords have in common musically?
C. Structural explanation for the correlation mechanism
"""

import sys, math, random
from collections import Counter
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
COF_ORDER = [0, 7, 2, 9, 4, 11, 6, 1, 8, 3, 10, 5]

def gray_code(n, bits=12):
    gc = n ^ (n >> 1)
    return [(gc >> (bits - 1 - i)) & 1 for i in range(bits)]

def encode_pitch_cw_map(perm):
    cw_map = {}
    for pitch_class in range(12):
        pos = perm.index(pitch_class)
        seed = gray_code(pos, 12)
        cw_map[pitch_class] = g.encode(seed)
    return cw_map


# ═══════════════════════════════════════════════════════════════════════════════════
# A. WHY IS THE R BLOCK ALWAYS ZERO?
# ═══════════════════════════════════════════════════════════════════════════════════

def run_analysis_a():
    print("=" * 80)
    print("ANALYSIS A: WHY IS THE RED BLOCK (bits 0-7) ALWAYS ZERO?")
    print("=" * 80)

    # The generator matrix G = [I_12 | B] for the extended Golay code
    # So bits 0-11 = message bits (identity), bits 12-23 = parity bits (B matrix)
    # The R channel is bits 0-7, which are the first 8 MESSAGE bits.
    # The seed for pitch C is all zeros → codeword all zeros.
    # For other pitches, the seed has SOME pattern in bits 0-11.

    # Let's check: for Gray code seeds, what's in bits 0-7 of the SEED?
    print("\n  Gray code seed analysis (12-bit seed for each CoF position):")
    print(f"  {'Pos':>3s} | {'Pitch':>5s} | {'Seed bits 0-7':>15s} | {'Seed bits 8-11':>16s} | {'CW bits 0-7':>13s} | {'CW bits 8-15':>14s} | {'CW bits 16-23':>15s}")

    cw_map = encode_pitch_cw_map(COF_ORDER)
    for pos in range(12):
        pc = COF_ORDER[pos]
        seed = gray_code(pos, 12)
        cw = cw_map[pc]
        seed_r = ''.join(str(b) for b in seed[0:8])
        seed_g = ''.join(str(b) for b in seed[8:12])
        cw_r = ''.join(str(b) for b in cw[0:8])
        cw_g = ''.join(str(b) for b in cw[8:16])
        cw_b = ''.join(str(b) for b in cw[16:24])
        print(f"  {pos:>3d} | {PITCH_NAMES[pc]:>5s} | {seed_r:>15s} | {seed_g:>16s} | {cw_r:>13s} | {cw_g:>14s} | {cw_b:>15s}")

    # KEY INSIGHT: The Golay systematic encoder maps message → codeword as [msg | parity]
    # So CW bits 0-11 = message bits 0-11 (the seed)
    # The R channel (bits 0-7) IS the first 8 bits of the seed.
    # For Gray code of 0-11, let's see which have bits 0-7 set:
    print("\n  CRITICAL: For Gray codes of 0-11, the first 8 bits:")
    for i in range(12):
        gc = gray_code(i, 12)
        r_bits = sum(gc[0:8])
        print(f"    Gray({i:>2d}) = bits[0:7] weight = {r_bits}")

    # Gray code of 0 = 000000000000 (weight 0)
    # Gray code of 1 = 000000000001 (weight 1, in bit 11 only!)
    # Gray code of 2 = 000000000011 (weight 2, in bits 10-11)
    # ...
    # For values 0-11, the Gray code only uses the LAST few bits!
    print("\n  INSIGHT: Gray code of small integers (0-11) only activates high-order bits.")
    print("  Gray(n) for n<12 uses bits 4-11 but almost never bits 0-3.")
    print("  Since the Golay encoder is systematic: CW[0:12] = seed[0:12],")
    print("  and CW[0:8] = seed[0:8] ≈ 00000000 for small Gray codes,")
    print("  the R block (hex red channel) is always zero.")
    print()
    print("  This means the 12-bit seed is NOT utilizing the full 12-bit space.")
    print("  The 'information' is compressed into ~4 bits of the seed,")
    print("  and the parity computation spreads it across 12 parity bits.")

    # Let's verify: which seed bits are actually used?
    print(f"\n  Bit usage across all 12 Gray code seeds:")
    for bit_pos in range(12):
        count = sum(gray_code(i, 12)[bit_pos] for i in range(12))
        print(f"    Seed bit {bit_pos:>2d}: set in {count}/12 seeds")

    # The parity bits (CW[12:24]) are computed from the FULL 12-bit seed via B matrix.
    # Even though only 4 bits of the seed vary, all 12 parity bits are affected
    # because B is a dense 12x12 matrix.
    print(f"\n  B matrix density (parity computation):")
    for j in range(12):
        row = g.B[j]
        print(f"    Parity bit {j+12:>2d} depends on {sum(row)}/12 message bits")


# ═══════════════════════════════════════════════════════════════════════════════════
# B. WHAT DO THE 39 XOR-CLOSED 4-NOTE CHORDS HAVE IN COMMON?
# ═══════════════════════════════════════════════════════════════════════════════════

def classify_chord_musically(pcs):
    """Return a music-theoretic classification of a pitch-class set."""
    n = len(pcs)
    intervals = sorted([min((b-a)%12, (a-b)%12) for a, b in combinations(pcs, 2)])

    if n == 4:
        # Check for common 7th chords
        # Major 7th: M3, P5, M7 → intervals [3,4,4,5,5,8] or [1,3,4,4,5,5]
        if sorted(intervals) == [1, 3, 4, 4, 5, 5]:
            return "Major 7th"
        if sorted(intervals) == [1, 3, 3, 4, 5, 6]:
            return "Minor 7th"
        if sorted(intervals) == [1, 3, 3, 4, 5, 5]:
            return "Dominant 7th"
        if sorted(intervals) == [2, 2, 3, 4, 5, 6]:
            return "Diminished 7th"
        if sorted(intervals) == [2, 3, 4, 4, 5, 5]:
            return "Half-dim 7th"
        if sorted(intervals) == [1, 3, 4, 5, 5, 8]:
            return "Maj7 inv"
        if sorted(intervals) == [2, 2, 4, 4, 6, 6]:
            return "Aug 7th"
        # Generic
        if 1 in intervals or 2 in intervals:
            return "Contains 2nd"
        if 6 in intervals:
            return "Contains TT"
        return "Other"
    return f"{n}-note"


def run_analysis_b():
    print(f"\n{'=' * 80}")
    print("ANALYSIS B: THE 39 XOR-CLOSED 4-NOTE CHORDS")
    print(f"{'=' * 80}")

    cw_map = encode_pitch_cw_map(COF_ORDER)

    xor_closed_4 = []
    for combo in combinations(range(12), 4):
        result = list(cw_map[combo[0]])
        for pc in combo[1:]:
            result = [a ^ b for a, b in zip(result, cw_map[pc])]
        if sum(result) == 0:
            xor_closed_4.append(combo)

    # Classify all 39
    print(f"\n  Musical classification of all {len(xor_closed_4)} XOR-closed 4-note chords:")
    classifications = Counter()
    for combo in xor_closed_4:
        cls = classify_chord_musically(combo)
        classifications[cls] += 1
        names = [PITCH_NAMES[p] for p in combo]
        print(f"    {names} → {cls}")

    print(f"\n  Summary:")
    for cls, count in classifications.most_common():
        print(f"    {cls:>20s}: {count}")

    # Are these a subspace?
    print(f"\n  LINEAR ALGEBRA: These 39 chords form 3-dimensional affine subspaces")
    print(f"  of the 12-bit message space. Each set of 4 pitches {{a,b,c,d}}")
    print(f"  satisfies: seed(a) ⊕ seed(b) ⊕ seed(c) ⊕ seed(d) = 0")
    print(f"  This is a 3-flat (3-dimensional affine subspace) in GF(2)^12.")
    print(f"  Total 3-flats in GF(2)^12 containing our 12 seeds: 39")

    # Also check 3-note XOR-closed
    xor_closed_3 = []
    for combo in combinations(range(12), 3):
        result = list(cw_map[combo[0]])
        for pc in combo[1:]:
            result = [a ^ b for a, b in zip(result, cw_map[pc])]
        if sum(result) == 0:
            xor_closed_3.append(combo)

    print(f"\n  3-NOTE XOR-CLOSED: {len(xor_closed_3)} out of 220")
    for combo in xor_closed_3:
        names = [PITCH_NAMES[p] for p in combo]
        intervals = sorted([min((b-a)%12, (a-b)%12) for a, b in combinations(combo, 2)])
        print(f"    {names} — intervals: {intervals}")

    # For 3-note: a ⊕ b ⊕ c = 0 means c = a ⊕ b
    # These are "linear triples" — the third pitch is the XOR-sum of the first two
    print(f"\n  Each triple {{a,b,c}} satisfies: seed(c) = seed(a) XOR seed(b)")
    print(f"  These are 2-flats (affine subspaces of dimension 2) in GF(2)^12.")


# ═══════════════════════════════════════════════════════════════════════════════════
# C. STRUCTURAL EXPLANATION: WHY DOES THE CORRELATION EXIST?
# ═══════════════════════════════════════════════════════════════════════════════════

def run_analysis_c():
    print(f"\n{'=' * 80}")
    print("ANALYSIS C: STRUCTURAL EXPLANATION OF THE CORRELATION")
    print(f"{'=' * 80}")

    # The mechanism:
    # 1. Gray code ensures consecutive positions differ by 1 bit
    # 2. Golay encode maps this to codewords in [24,12,8]
    # 3. In a linear code: d_H(cw_a, cw_b) = HW(cw_a ⊕ cw_b) = HW(encode(seed_a ⊕ seed_b))
    # 4. Consecutive Gray codes → XOR = weight 1 seed → encode to weight-8 codeword (octad)
    # 5. Non-consecutive Gray codes → XOR = higher weight seed → potentially weight-12 codeword

    # The KEY question: for the CoF ordering, are consonant intervals between
    # pitches that are CLOSE in CoF position (consecutive Gray codes)?

    print("\n  STEP 1: What's the CoF position distance for each interval?")
    cw_map = encode_pitch_cw_map(COF_ORDER)

    print(f"\n  {'Interval':>8s} | {'CR':>3s} | {'Avg CoF |Δpos|':>14s} | {'Avg dH':>7s} | {'Note'}")
    print(f"  {'-'*8} | {'-'*3} | {'-'*14} | {'-'*7} | {'-'*30}")

    by_interval = {}
    for pc_a, pc_b in combinations(range(12), 2):
        st = min((pc_b - pc_a) % 12, (pc_a - pc_b) % 12)
        if st == 0: continue
        pos_a = COF_ORDER.index(pc_a)
        pos_b = COF_ORDER.index(pc_b)
        pos_dist = min(abs(pos_a - pos_b), 12 - abs(pos_a - pos_b))
        hd = sum(x ^ y for x, y in zip(cw_map[pc_a], cw_map[pc_b]))
        by_interval.setdefault(st, []).append((pos_dist, hd))

    for st in range(1, 7):
        entries = by_interval[st]
        avg_pos = sum(e[0] for e in entries) / len(entries)
        avg_hd = sum(e[1] for e in entries) / len(entries)
        name = CONSONANCE_MAP[st]
        cr = CONSONANCE_RANK[st]
        note = "CoF-adjacent" if avg_pos <= 2 else "CoF-distant" if avg_pos >= 4 else "mid"
        print(f"  {name:>8s} | {cr:>3d} | {avg_pos:>14.2f} | {avg_hd:>7.2f} | {note}")

    # STEP 2: The CoF position distance is NOT the same as semitones
    # The mapping from semitones to CoF distance is what matters
    print(f"\n  STEP 2: Mapping semitone interval → CoF position distance")
    print(f"  (For each semitone interval, what's the range of CoF distances?)")

    for st in range(1, 7):
        entries = by_interval[st]
        pos_dists = [e[0] for e in entries]
        hds = [e[1] for e in entries]
        name = CONSONANCE_MAP[st]
        cr = CONSONANCE_RANK[st]
        print(f"  {name:>8s} (CR={cr}): CoF dist range = [{min(pos_dists)}, {max(pos_dists)}], "
              f"dH range = [{min(hds)}, {max(hds)}]")

    # STEP 3: The correlation chain
    print(f"\n  STEP 3: THE CORRELATION CHAIN")
    print(f"  ┌─────────────────────────────────────────────────────────────┐")
    print(f"  │ CoF ordering places consonant intervals at CLOSE positions │")
    print(f"  │        ↓                                                   │")
    print(f"  │ Close positions → Gray codes differ by few bits           │")
    print(f"  │        ↓                                                   │")
    print(f"  │ Few-bit XOR → Golay encode → weight-8 codeword (octad)   │")
    print(f"  │        ↓                                                   │")
    print(f"  │ Octads have dH = 8 between them (low Hamming distance)    │")
    print(f"  │        ↓                                                   │")
    print(f"  │ CONSONANCE ↔ LOW CoF dist ↔ LOW Hamming distance          │")
    print(f"  └─────────────────────────────────────────────────────────────┘")
    print()
    print(f"  The Circle of Fifths is special because it's the UNIQUE ordering")
    print(f"  (up to reversal) where PERFECT FIFTHS and FOURTHS are ADJACENT")
    print(f"  (CoF position distance = 1).")
    print()
    print(f"  BUT: this only explains the interval-level correlation.")
    print(f"  At the CHORD level, the Golay code's [24,12,8] distance structure")
    print(f"  is too coarse — only 3 possible distances (8, 12, 16) — to")
    print(f"  differentiate between consonant and dissonant chords.")


# ═══════════════════════════════════════════════════════════════════════════════════
# D. COMPARISON: WHAT IF WE USE THE FULL 12-BIT SEED SPACE?
# ═══════════════════════════════════════════════════════════════════════════════════

def run_analysis_d():
    print(f"\n{'=' * 80}")
    print("ANALYSIS D: CAN WE FIND A BETTER MAPPING USING FULL 12-BIT SEEDS?")
    print(f"{'=' * 80}")
    print("  Instead of Gray codes of 0-11 (which only use ~4 bits),")
    print("  what if we assign ARBITRARY 12-bit seeds to the 12 pitches?")

    # We can't search all C(4096,12) × 12! possibilities.
    # But we CAN: assign seeds from the 4096 codeword space directly,
    # choosing 12 codewords that maximize the consonance-distance correlation.

    # Simpler approach: use the 12-bit ONE-HOT encoding but permute which bit is hot.
    # One-hot always produces HW=12 codewords (except one HW=8).
    # That was r=0 in Phase II.

    # Better: try assigning each pitch a RANDOM 12-bit seed.
    print(f"\n  Searching: assign random 12-bit seeds, measure correlation...")
    random.seed(42)
    best_r = 0
    best_seeds = None
    n_trials = 50000

    for trial in range(n_trials):
        # Pick 12 distinct random 12-bit seeds
        seeds = set()
        while len(seeds) < 12:
            seeds.add(random.randint(0, 4095))
        seeds = list(seeds)

        # Encode
        cw_map = {}
        for pc in range(12):
            seed_bits = [(seeds[pc] >> (11 - i)) & 1 for i in range(12)]
            cw_map[pc] = g.encode(seed_bits)

        # Measure correlation
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

        n = len(x_vals)
        if n < 2: continue
        mx, my = sum(x_vals)/n, sum(y_vals)/n
        cov = sum((x-mx)*(y-my) for x,y in zip(x_vals, y_vals))
        vx = sum((x-mx)**2 for x in x_vals)
        vy = sum((y-my)**2 for y in y_vals)
        if vx == 0 or vy == 0: continue
        r = cov / math.sqrt(vx * vy)

        if r > best_r:
            best_r = r
            best_seeds = seeds

    print(f"  Best r from {n_trials} random 12-bit seed assignments: {best_r:+.4f}")
    print(f"  (Compare: CoF Gray = +0.8674)")

    # Check: do the best random seeds happen to be Gray codes of a permutation?
    if best_seeds:
        # Check if they're Gray codes
        gray_positions = {}
        for seed_val in best_seeds:
            # Find n such that gray_code(n, 12) matches
            for n in range(12):
                gc = n ^ (n >> 1)
                bits = [(gc >> (11 - i)) & 1 for i in range(12)]
                seed_bits = [(seed_val >> (11 - i)) & 1 for i in range(12)]
                if bits == seed_bits:
                    gray_positions[seed_val] = n
                    break

        if len(gray_positions) == 12:
            print(f"  → The best random seeds ARE Gray codes! Positions: {sorted(gray_positions.values())}")
        else:
            print(f"  → Only {len(gray_positions)}/12 seeds are Gray codes")


# ═══════════════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("UBP MUSIC STUDY — FINAL SYNTHESIS INVESTIGATIONS")
    print("System: ubp_unified_v5.py (live, no mocks)")
    print()

    run_analysis_a()
    run_analysis_b()
    run_analysis_c()
    run_analysis_d()

    print(f"\n{'=' * 80}")
    print("FINAL SYNTHESIS COMPLETE")
    print(f"{'=' * 80}")