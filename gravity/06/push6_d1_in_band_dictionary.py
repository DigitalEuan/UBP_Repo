"""
Push #6 D.1 (Option C / NQ26) — IN-BAND Pre-Screen Utility and Dictionary.

OBJECTIVE
---------
Per the UBP Core Studio AI's strategic plan:
  "I can extract the `primality_nrci` logic into a standalone, high-speed Python
   utility. We can use this to scan thousands of integers to build a complete
   'Dictionary of IN-BAND Primes,' giving us the exact building blocks for all
   future formulas before we even run a null test."

This script:
  1. Scans integers 1..10000 via TopologicalALU.primality_nrci
  2. Classifies each as PRIME-ANOMALY / COMPOSITE-OUT / PRIME-IN-BAND / COMPOSITE-IN-BAND
  3. Builds a complete Dictionary of IN-BAND integers
  4. Tests the IN-BAND criterion's reliability:
     - For each surprising formula's priming integer, confirm IN-BAND
     - For each empirical atlas integer, confirm OUT
     - Spot-check a sample of IN-BAND integers not yet tested in formulas
  5. Identifies the "D-Sink power family" (13^k for k=1..6) and checks each
  6. Identifies UBP-canonical integers (3, 12, 13, 24, 29, 39, 137, 169, 2197,
     28561, etc.) and classifies each
"""
from __future__ import annotations
import json, sys, time
from fractions import Fraction
from pathlib import Path

sys.path.insert(0, "/home/z/my-project/scripts")
import ubp_unified_v5 as u
import ubp_v28_oracle as oracle

F = Fraction
topo = oracle.TopologicalALU()

# ─────────────────────────────────────────────────────────────────────────────
# 1. Scan integers 1..10000
# ─────────────────────────────────────────────────────────────────────────────
print("=" * 80)
print("Push #6 D.1 — IN-BAND Pre-Screen Utility and Dictionary")
print("=" * 80)
print("\nScanning integers 1..10000 via TopologicalALU.primality_nrci...\n")

N_SCAN = 10000
t_start = time.time()
results = {}
counts = {"PRIME-ANOMALY": 0, "COMPOSITE-OUT": 0, "PRIME-IN-BAND": 0, "COMPOSITE-IN-BAND": 0}
in_band_list = []
prime_in_band_list = []
composite_in_band_list = []

for n in range(1, N_SCAN + 1):
    r = topo.primality_nrci(n)
    results[n] = r
    counts[r["verdict"]] += 1
    if r["verdict"] in ("PRIME-IN-BAND", "COMPOSITE-IN-BAND"):
        in_band_list.append(n)
        if r["verdict"] == "PRIME-IN-BAND":
            prime_in_band_list.append(n)
        else:
            composite_in_band_list.append(n)

elapsed = time.time() - t_start
print(f"Scan complete in {elapsed:.1f}s")
print(f"\nCounts (1..{N_SCAN}):")
for v, c in counts.items():
    pct = c / N_SCAN * 100
    print(f"  {v}: {c} ({pct:.2f}%)")

print(f"\nTotal IN-BAND: {len(in_band_list)} ({len(in_band_list)/N_SCAN*100:.2f}%)")
print(f"  PRIME-IN-BAND: {len(prime_in_band_list)}")
print(f"  COMPOSITE-IN-BAND: {len(composite_in_band_list)}")

# ─────────────────────────────────────────────────────────────────────────────
# 2. Dictionary of IN-BAND integers
# ─────────────────────────────────────────────────────────────────────────────
print("\n" + "=" * 80)
print("(2) Dictionary of IN-BAND integers (1..10000)")
print("=" * 80)
print(f"\nFirst 50 IN-BAND integers:")
print(f"  {in_band_list[:50]}")
print(f"\nLast 20 IN-BAND integers (near 10000):")
print(f"  {in_band_list[-20:]}")

# Check the D-Sink power family
print(f"\n--- D-Sink power family (13^k) ---")
for k in range(1, 8):
    n = 13 ** k
    if n <= N_SCAN:
        r = results[n]
        print(f"  13^{k} = {n}: {r['verdict']}  (NRCI={r['nrci']:.4f}, sw={r['sw']})")
    else:
        # Compute separately
        r = topo.primality_nrci(n)
        print(f"  13^{k} = {n}: {r['verdict']}  (NRCI={r['nrci']:.4f}, sw={r['sw']})  [computed separately]")

# Check UBP-canonical integers
print(f"\n--- UBP-canonical integers ---")
ubp_canonical = [1, 2, 3, 4, 5, 6, 7, 8, 11, 12, 13, 17, 19, 23, 24, 29, 31, 39, 41, 47,
                 59, 71, 137, 169, 2197, 28561, 206, 1836, 36, 48, 96, 192, 384]
for n in ubp_canonical:
    if n <= N_SCAN:
        r = results[n]
    else:
        r = topo.primality_nrci(n)
    marker = ""
    if n in (137, 169, 2197, 28561): marker = "  <-- IN-BAND (used in surprising formulas)"
    elif n in (206, 1836): marker = "  <-- OUT (empirical atlas integers)"
    elif n in (13, 29): marker = "  <-- PRIME-ANOMALY (UBP structural primes)"
    elif n == 24: marker = "  <-- COMPOSITE-OUT (Leech rank, scaffolding)"
    print(f"  {n:6d}: {r['verdict']:<20}  (NRCI={r['nrci']:.4f}, sw={r['sw']}){marker}")

# ─────────────────────────────────────────────────────────────────────────────
# 3. Reliability test: confirm known formulas' priming integers
# ─────────────────────────────────────────────────────────────────────────────
print("\n" + "=" * 80)
print("(3) Reliability test — known formulas' priming integers")
print("=" * 80)
print(f"\n{'Formula':<30} {'Priming int':<14} {'Verdict':<20} {'Predicted surprising?':<25} {'Actual?':<15}")
print("-" * 110)

reliability_rows = [
    ("13/L (m_μ/m_e)",          169,    "IN-BAND",  "YES",  "YES (Push #2)"),
    ("24·Y⁴ (α_s)",             24,     "OUT",      "(scaffolding)", "YES (Push #4) — exception"),
    ("(13/L)·(24·Y⁴)·π (m_W)", 169,    "IN-BAND",  "YES",  "YES (Push #5)"),
    ("24·Y^15·U_e (Ω_k)",      24,     "OUT",      "(scaffolding)", "YES (Push #5) — exception"),
    ("8/π·Y_inv³ (α⁻¹)",       137,    "IN-BAND",  "YES (predicted)", "Push #6 should test"),
    ("206 + 12·L (atlas m_μ)",  206,    "OUT",      "NO (empirical)",  "Atlas formula (not surprising)"),
    ("1836 + 2·L_s (atlas m_p)", 1836,  "OUT",      "NO (empirical)",  "Atlas formula (not surprising)"),
    ("39/29·Y^18/w (G_UBP)",    39,     "OUT",      "NO (predicted)",  "NOT surprising (Push #2, 20% FP)"),
    ("184/137 (best G ratio)",  184,    "?",        "?",   "Push #6 should check"),
    ("184/137 (best G ratio)",  137,    "IN-BAND",  "YES (predicted)", "Push #6 should check"),
]
for formula, n, predicted_verdict, predicted_surp, actual in reliability_rows:
    if n <= N_SCAN:
        r = results[n]
    else:
        r = topo.primality_nrci(n)
    actual_verdict = r["verdict"]
    match = "✓" if actual_verdict == predicted_verdict else "✗"
    print(f"  {formula:<28} {n:<14} {actual_verdict:<20} {predicted_surp:<25} {actual:<15} {match}")

# ─────────────────────────────────────────────────────────────────────────────
# 4. Identify IN-BAND integers that are NOT yet used in formulas — candidates for new formulas
# ─────────────────────────────────────────────────────────────────────────────
print("\n" + "=" * 80)
print("(4) IN-BAND integers NOT yet used in surprising formulas — candidates for Push #7")
print("=" * 80)

# Already used: 137, 169, 2197, 28561
used_in_band = {137, 169, 2197, 28561}
unused_in_band = [n for n in in_band_list if n not in used_in_band]
print(f"\nTotal IN-BAND integers: {len(in_band_list)}")
print(f"Already used in surprising formulas: {len(used_in_band)} ({sorted(used_in_band)})")
print(f"Unused IN-BAND integers (candidates): {len(unused_in_band)}")
print(f"\nFirst 30 unused IN-BAND candidates:")
print(f"  {unused_in_band[:30]}")

# Categorize unused IN-BAND integers by structure
print(f"\n--- Unused IN-BAND integers by structural category ---")

# Primes
unused_primes = [n for n in unused_in_band if results[n]["verdict"] == "PRIME-IN-BAND"]
print(f"  PRIME-IN-BAND (unused): {len(unused_primes)}")
print(f"    First 20: {unused_primes[:20]}")

# Composites that are perfect powers
unused_composites = [n for n in unused_in_band if results[n]["verdict"] == "COMPOSITE-IN-BAND"]
print(f"  COMPOSITE-IN-BAND (unused): {len(unused_composites)}")
print(f"    First 20: {unused_composites[:20]}")

# Check which unused IN-BAND integers are perfect powers
print(f"\n--- Perfect powers among unused IN-BAND composites ---")
def is_perfect_power(n):
    """Check if n = a^b for some a, b > 1."""
    if n < 4: return None
    # Check squares, cubes, etc.
    for b in range(2, 20):
        a = round(n ** (1.0 / b))
        for candidate in [a-1, a, a+1]:
            if candidate > 1 and candidate ** b == n:
                return (candidate, b)
    return None

perfect_powers_in_band = []
for n in unused_composites:
    pp = is_perfect_power(n)
    if pp:
        perfect_powers_in_band.append((n, pp))
print(f"  Perfect powers among unused IN-BAND composites: {len(perfect_powers_in_band)}")
for n, (base, exp) in perfect_powers_in_band[:20]:
    print(f"    {n} = {base}^{exp}")

# Check which are multiples of 13 (D-Sink family extensions)
multiples_of_13 = [n for n in unused_in_band if n % 13 == 0]
print(f"\n--- Multiples of 13 (D-Sink family extensions) among IN-BAND ---")
print(f"  Count: {len(multiples_of_13)}")
print(f"  First 20: {multiples_of_13[:20]}")

# ─────────────────────────────────────────────────────────────────────────────
# 5. Density analysis — how does IN-BAND density vary with magnitude?
# ─────────────────────────────────────────────────────────────────────────────
print("\n" + "=" * 80)
print("(5) Density analysis — IN-BAND density by magnitude")
print("=" * 80)
print(f"\n{'Range':<18} {'IN-BAND count':<16} {'Density %':<12}")
print("-" * 50)
ranges = [(1, 100), (101, 500), (501, 1000), (1001, 2000), (2001, 5000), (5001, 10000)]
for lo, hi in ranges:
    count = sum(1 for n in in_band_list if lo <= n <= hi)
    total = hi - lo + 1
    density = count / total * 100
    print(f"  {lo:5d}-{hi:5d}    {count:<16} {density:<12.2f}")

# ─────────────────────────────────────────────────────────────────────────────
# 6. Save the Dictionary of IN-BAND integers
# ─────────────────────────────────────────────────────────────────────────────
outp = Path("/home/z/my-project/results/push6_d1_in_band_dictionary.json")
with open(outp, "w") as f:
    json.dump({
        "scan_range": [1, N_SCAN],
        "scan_time_seconds": elapsed,
        "verdict_counts": counts,
        "total_in_band": len(in_band_list),
        "prime_in_band_count": len(prime_in_band_list),
        "composite_in_band_count": len(composite_in_band_list),
        "in_band_integers_1_to_10000": in_band_list,
        "prime_in_band_integers": prime_in_band_list,
        "composite_in_band_integers": composite_in_band_list,
        "d_sink_power_family": {
            f"13^{k}": {"value": 13**k,
                         "verdict": (results[13**k] if 13**k <= N_SCAN else topo.primality_nrci(13**k))["verdict"],
                         "nrci": (results[13**k] if 13**k <= N_SCAN else topo.primality_nrci(13**k))["nrci"],
                         "sw": (results[13**k] if 13**k <= N_SCAN else topo.primality_nrci(13**k))["sw"]}
            for k in range(1, 8)
        },
        "ubp_canonical_classification": {
            str(n): {"verdict": (results[n] if n <= N_SCAN else topo.primality_nrci(n))["verdict"],
                      "nrci": (results[n] if n <= N_SCAN else topo.primality_nrci(n))["nrci"],
                      "sw": (results[n] if n <= N_SCAN else topo.primality_nrci(n))["sw"]}
            for n in ubp_canonical
        },
        "reliability_test": [
            {"formula": formula, "priming_int": n,
             "verdict": (results[n] if n <= N_SCAN else topo.primality_nrci(n))["verdict"],
             "predicted_surprising": pred, "actual": actual}
            for formula, n, _, pred, actual in reliability_rows
        ],
        "unused_in_band_candidates": {
            "count": len(unused_in_band),
            "first_50": unused_in_band[:50],
            "prime_in_band_unused_count": len(unused_primes),
            "composite_in_band_unused_count": len(unused_composites),
            "perfect_powers": [{"n": n, "base": base, "exp": exp} for n, (base, exp) in perfect_powers_in_band[:30]],
            "multiples_of_13": multiples_of_13[:30],
        },
        "density_by_magnitude": [
            {"range": [lo, hi], "in_band_count": sum(1 for n in in_band_list if lo <= n <= hi),
             "density_pct": sum(1 for n in in_band_list if lo <= n <= hi) / (hi - lo + 1) * 100}
            for lo, hi in ranges
        ],
    }, f, indent=2, default=str)
print(f"\n[ok] Results saved to {outp}")
