"""
UBP Music Study — Phase I & II
================================
Phase I:  Ontological Mapping — Encode 12 pitch classes into 24-bit Golay codewords
          using multiple encoding strategies (chromatic, circle-of-fifths, one-hot).
Phase II: Interval Dynamics — Measure Hamming distance for all 66 unordered intervals
          and test whether geometric distance on the Leech lattice correlates with
          acoustic consonance.

Uses ONLY the live UBP system (no mocks, no stubs).
"""

import sys, json, math, random
from fractions import Fraction
from itertools import combinations

# ── UBP imports ──────────────────────────────────────────────────────────────────
sys.path.insert(0, "/home/z/my-project")
from ubp_unified_v5 import GolayCodeEngine, LeechLatticeEngine

g = GolayCodeEngine()
l = LeechLatticeEngine(g)

# ── Encoding helpers ─────────────────────────────────────────────────────────────

def gray_code(n: int, bits: int) -> list:
    """n-bit binary-reflected Gray code for integer n."""
    gc = n ^ (n >> 1)
    return [(gc >> (bits - 1 - i)) & 1 for i in range(bits)]

def one_hot(index: int, total: int = 12) -> list:
    """One-hot encoding: only bit `index` is 1."""
    return [1 if i == index else 0 for i in range(total)]

def chromatic_12bit(pitch: int) -> list:
    """Sequential Gray code: C=0, C#=1, D=2, ..."""
    return gray_code(pitch, 12)

# Circle of Fifths: C=0, G=7, D=2, A=9, E=4, B=11, F#=6, Db=1, Ab=8, Eb=3, Bb=10, F=5
# Position in CoF:  C->0, G->1, D->2, A->3, E->4, B->5, F#->6, Db->7, Ab->8, Eb->9, Bb->10, F->11
COF_POSITION = {0:0, 7:1, 2:2, 9:3, 4:4, 11:5, 6:6, 1:7, 8:8, 3:9, 10:10, 5:11}

def fifths_12bit(pitch: int) -> list:
    """Circle-of-Fifths ordering via Gray code."""
    pos = COF_POSITION[pitch]
    return gray_code(pos, 12)

def onehot_12bit(pitch: int) -> list:
    return one_hot(pitch, 12)

# ── Hex colour from 24-bit vector ────────────────────────────────────────────────

def vec_to_hex(v24: list) -> str:
    r = sum((1 << (7 - i)) for i in range(8) if v24[i])
    gg = sum((1 << (7 - i)) for i in range(8) if v24[8 + i])
    b = sum((1 << (7 - i)) for i in range(8) if v24[16 + i])
    return f"#{r:02x}{gg:02x}{b:02x}"

# ── Hamming distance ─────────────────────────────────────────────────────────────

def hamming(a: list, b: list) -> int:
    return sum(x ^ y for x, y in zip(a, b))

# ── Music theory reference ────────────────────────────────────────────────────────
CONSONANCE_MAP = {
    0: "Unison", 1: "Minor 2nd", 2: "Major 2nd", 3: "Minor 3rd",
    4: "Major 3rd", 5: "Perfect 4th", 6: "Tritone", 7: "Perfect 5th",
    8: "Minor 6th", 9: "Major 6th", 10: "Minor 7th", 11: "Major 7th"
}
# Lower rank = more consonant
CONSONANCE_RANK = {
    0: 1, 7: 2, 5: 3, 4: 3, 9: 3, 3: 4, 8: 4, 10: 4, 2: 5, 11: 5, 1: 6, 6: 6
}
PITCH_NAMES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]


# ═══════════════════════════════════════════════════════════════════════════════════
# PHASE I: PITCH CLASS MANIFOLD
# ═══════════════════════════════════════════════════════════════════════════════════

def run_phase1():
    print("=" * 80)
    print("PHASE I: PITCH CLASS MANIFOLD — Three Encoding Strategies")
    print("=" * 80)

    encodings = {
        "Chromatic Gray":       chromatic_12bit,
        "Circle-of-Fifths Gray": fifths_12bit,
        "One-Hot":              onehot_12bit,
    }

    all_results = {}

    for enc_name, enc_func in encodings.items():
        print(f"\n{'─' * 60}")
        print(f"  Encoding: {enc_name}")
        print(f"{'─' * 60}")

        pitch_data = {}
        for pc in range(12):
            seed12 = enc_func(pc)
            cw24 = g.encode(seed12)
            hw = g.hamming_weight(cw24)
            tax = l.calculate_symmetry_tax(cw24)
            nrci = l.calculate_nrci(cw24)
            hex_col = vec_to_hex(cw24)
            synd_w = g.syndrome_weight(cw24)

            pitch_data[pc] = {
                "seed12": seed12,
                "cw24": cw24,
                "hamming_weight": hw,
                "nrci": float(nrci),
                "tax": float(tax),
                "hex": hex_col,
                "syndrome_weight": synd_w,
            }
            print(f"  {PITCH_NAMES[pc]:>2s} (pc={pc:2d}) | HW={hw:2d} | "
                  f"NRCI={float(nrci):.4f} | Tax={float(tax):.4f} | "
                  f"Hex={hex_col} | SyndW={synd_w}")

        all_results[enc_name] = pitch_data

    # Validation
    print(f"\n{'═' * 60}")
    print("  VALIDATION SUMMARY")
    print(f"{'═' * 60}")
    for enc_name, pd in all_results.items():
        all_valid = all(v["syndrome_weight"] == 0 for v in pd.values())
        nrci_vals = [v["nrci"] for v in pd.values()]
        hw_vals = [v["hamming_weight"] for v in pd.values()]
        unique_nrci = sorted(set(round(v, 6) for v in nrci_vals))
        unique_hw = sorted(set(hw_vals))
        print(f"  {enc_name:25s}: Valid={all_valid} | "
              f"NRCIs: {unique_nrci} | HWs: {unique_hw}")

    return all_results


# ═══════════════════════════════════════════════════════════════════════════════════
# PHASE II: INTERVAL DYNAMICS
# ═══════════════════════════════════════════════════════════════════════════════════

def pearson_r(x_vals, y_vals):
    n = len(x_vals)
    mean_x = sum(x_vals) / n
    mean_y = sum(y_vals) / n
    cov = sum((x - mean_x) * (y - mean_y) for x, y in zip(x_vals, y_vals))
    vx = sum((x - mean_x)**2 for x in x_vals)
    vy = sum((y - mean_y)**2 for y in y_vals)
    if vx == 0 or vy == 0:
        return 0.0
    return cov / math.sqrt(vx * vy)


def run_phase2(all_results):
    print(f"\n{'=' * 80}")
    print("PHASE II: INTERVAL DYNAMICS — Hamming Distance vs Acoustic Consonance")
    print(f"{'=' * 80}")

    for enc_name, pitch_data in all_results.items():
        print(f"\n{'─' * 60}")
        print(f"  Encoding: {enc_name}")
        print(f"{'─' * 60}")

        # Collect all 66 unordered intervals
        by_interval = {}
        for pc_a, pc_b in combinations(range(12), 2):
            st = min((pc_b - pc_a) % 12, (pc_a - pc_b) % 12)
            hd = hamming(pitch_data[pc_a]["cw24"], pitch_data[pc_b]["cw24"])
            by_interval.setdefault(st, []).append(hd)

        print(f"\n  {'Interval':>12s} | {'Cons':>4s} | {'Avg HD':>7s} | {'Min HD':>7s} | {'Max HD':>7s} | {'# Pairs':>7s} | {'Var':>7s}")
        print(f"  {'-'*12} | {'-'*4} | {'-'*7} | {'-'*7} | {'-'*7} | {'-'*7} | {'-'*7}")

        x_vals, y_vals = [], []
        for st in range(1, 12):
            hds = by_interval.get(st, [])
            if not hds:
                continue
            avg_hd = sum(hds) / len(hds)
            var_hd = sum((h - avg_hd)**2 for h in hds) / len(hds)
            name = CONSONANCE_MAP[st]
            cr = CONSONANCE_RANK[st]
            x_vals.append(cr)
            y_vals.append(avg_hd)
            print(f"  {name:>12s} | {cr:>4d} | {avg_hd:>7.2f} | {min(hds):>7d} | {max(hds):>7d} | {len(hds):>7d} | {var_hd:>7.2f}")

        r = pearson_r(x_vals, y_vals)
        direction = "POSITIVE" if r > 0 else "NEGATIVE"
        strength = "strong" if abs(r) > 0.7 else "moderate" if abs(r) > 0.4 else "weak"
        print(f"\n  Pearson r = {r:.4f} | R² = {r**2:.4f} ({r**2*100:.1f}%)")
        print(f"  → {strength} {direction} correlation")

    # Reference: Golay inter-codeword distance distribution
    print(f"\n  REFERENCE: Golay [24,12,8] inter-codeword Hamming distances (sample):")
    cws = g.get_all_codewords()
    random.seed(42)
    sample_hds = []
    for _ in range(500):
        a, b = random.sample(range(4096), 2)
        sample_hds.append(hamming(cws[a], cws[b]))
    hd_dist = {}
    for h in sample_hds:
        hd_dist[h] = hd_dist.get(h, 0) + 1
    for h in sorted(hd_dist):
        print(f"    d_H={h:2d}: {hd_dist[h]:3d}/500 pairs ({hd_dist[h]/5:.0f}%)")


# ═══════════════════════════════════════════════════════════════════════════════════
# PHASE II-B: DIRECT INTERVAL ENCODING
# ═══════════════════════════════════════════════════════════════════════════════════

def run_phase2b():
    print(f"\n{'=' * 80}")
    print("PHASE II-B: DIRECT INTERVAL ENCODING — Encoding interval width as seed")
    print(f"{'=' * 80}")

    print(f"\n  {'Semi':>4s} | {'Interval':>12s} | {'Cons':>4s} | {'HW':>3s} | {'NRCI':>7s} | {'Tax':>7s} | {'Hex':>9s}")
    print(f"  {'-'*4} | {'-'*12} | {'-'*4} | {'-'*3} | {'-'*7} | {'-'*7} | {'-'*9}")

    x_vals, y_vals = [], []
    for st in range(12):
        seed = gray_code(st, 12)
        cw = g.encode(seed)
        hw = g.hamming_weight(cw)
        tax = l.calculate_symmetry_tax(cw)
        nrci = l.calculate_nrci(cw)
        hex_col = vec_to_hex(cw)
        name = CONSONANCE_MAP[st]
        cr = CONSONANCE_RANK[st]
        x_vals.append(cr)
        y_vals.append(hw)
        print(f"  {st:>4d} | {name:>12s} | {cr:>4d} | {hw:>3d} | {float(nrci):>7.4f} | {float(tax):>7.4f} | {hex_col:>9s}")

    r = pearson_r(x_vals, y_vals)
    print(f"\n  Consonance Rank vs Codeword HW: r = {r:.4f}")


# ═══════════════════════════════════════════════════════════════════════════════════
# PHASE II-C: XOR STRUCTURE
# ═══════════════════════════════════════════════════════════════════════════════════

def run_phase2c(all_results):
    print(f"\n{'=' * 80}")
    print("PHASE II-C: XOR STRUCTURE — Consonance vs XOR Codeword Weight")
    print(f"{'=' * 80}")
    print("  (In linear Golay [24,12,8]: XOR of two codewords is a codeword)")
    print("  (Possible weights: 0, 8, 12, 16, 24 — weight 8 = octad = most symmetric)")

    for enc_name, pitch_data in all_results.items():
        print(f"\n  {'─' * 50}")
        print(f"  Encoding: {enc_name}")
        print(f"  {'─' * 50}")

        by_interval_xor = {}
        for pc_a, pc_b in combinations(range(12), 2):
            st = min((pc_b - pc_a) % 12, (pc_a - pc_b) % 12)
            xor_cw = [a ^ b for a, b in zip(pitch_data[pc_a]["cw24"], pitch_data[pc_b]["cw24"])]
            xor_wt = g.hamming_weight(xor_cw)
            by_interval_xor.setdefault(st, []).append(xor_wt)

        print(f"\n  {'Interval':>12s} | {'Cons':>4s} | {'Avg XOR Wt':>10s} | {'Min':>4s} | {'Max':>4s} | {'Status':>15s}")
        print(f"  {'-'*12} | {'-'*4} | {'-'*10} | {'-'*4} | {'-'*4} | {'-'*15}")

        x_vals, y_vals = [], []
        for st in range(1, 12):
            wts = by_interval_xor.get(st, [])
            if not wts:
                continue
            avg_wt = sum(wts) / len(wts)
            name = CONSONANCE_MAP[st]
            cr = CONSONANCE_RANK[st]
            all_octad = all(w == 8 for w in wts)
            status = "ALL OCTAD" if all_octad else f"avg={avg_wt:.1f}"
            x_vals.append(cr)
            y_vals.append(avg_wt)
            print(f"  {name:>12s} | {cr:>4d} | {avg_wt:>10.2f} | {min(wts):>4d} | {max(wts):>4d} | {status:>15s}")

        r = pearson_r(x_vals, y_vals)
        print(f"\n  Consonance vs XOR Weight: r = {r:.4f}")


# ═══════════════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("UBP MUSIC STUDY — Phase I & II")
    print("System: ubp_unified_v5.py (live, no mocks)")
    print()

    all_results = run_phase1()
    run_phase2(all_results)
    run_phase2b()
    run_phase2c(all_results)

    print(f"\n{'=' * 80}")
    print("Phase I & II COMPLETE")
    print(f"{'=' * 80}")