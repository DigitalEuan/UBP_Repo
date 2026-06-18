"""
NQ2 — Structural null model.

Push #1's null model scrambled substrate CONSTANTS but kept the GRAMMAR fixed
(bases, multipliers, Y-power ranges). This is conservative: scrambling the
grammar too would increase the false-positive rate.

This script scrambles BOTH:
  - Substrate constants (same as Push #1): each multiplied by uniform(0.1, 10)
  - Grammar: random subset of bases, random subset of multipliers,
    random Y-power range

For each (substrate × grammar) trial we record:
  - Best error per target
  - Whether ≤0.13% threshold was hit

Then we compare the real substrate's hit rate to the 2D null distribution.

We also test a stronger null: fully random grammar + fully random substrate
constants (each drawn from uniform(0.001, 1000)).
"""
from __future__ import annotations
import json, sys, random, time
from fractions import Fraction
from pathlib import Path

sys.path.insert(0, "/home/z/my-project/scripts")
import ubp_unified_v5 as u

F = Fraction

sub = u.SUBSTRATE
constants = sub.get_v6_constants()
PI   = constants["PI"]
PHI  = constants["PHI"]
E    = constants["E"]
Y    = constants["Y"]
YINV = constants["Y_INV"]
W    = constants["WOBBLE"]
L    = constants["SINK_L"]
L_s  = u.PARTICLE_PHYSICS.L_s
U_e  = u.PARTICLE_PHYSICS.U_e
C    = F(299792458, 1)

try:
    nrci_univ_raw = u.LEECH_ENGINE.calculate_nrci(list(u.LEECH_ENGINE.golay.get_octads()[0]))
    NRCI_UNIV = F(nrci_univ_raw) if not isinstance(nrci_univ_raw, Fraction) else nrci_univ_raw
    NRCI_UNIV = F(NRCI_UNIV.numerator, NRCI_UNIV.denominator).limit_denominator(10**6)
except Exception:
    NRCI_UNIV = F(7623, 10000)

G_CODATA = F(667430, 10**16)

# ─────────────────────────────────────────────────────────────────────────────
# Real substrate and grammar (from Push #1, Phase B)
# ─────────────────────────────────────────────────────────────────────────────
REAL_BASES = {
    "Y": Y, "Y_inv": YINV, "L": L, "L_s": L_s,
    "pi": PI, "phi": PHI, "e": E, "w": W, "U_e": U_e, "NRCI": NRCI_UNIV,
}
REAL_Y_POWERS = {f"Y^{k}": Y**k for k in range(1, 26)}
REAL_Y_POWERS.update({f"Y_inv^{k}": YINV**k for k in range(1, 8)})
REAL_OTHER_SCALES = {
    "1/U_e": F(1, U_e), "1/U_e^2": F(1, U_e**2),
    "1/c":   F(1, C),   "1/c^2":   F(1, C**2),
    "1":     F(1, 1),
}
SQRT2 = u.ExactMath.sqrt_frac(F(2, 1), prec=30)
SQRT3 = u.ExactMath.sqrt_frac(F(3, 1), prec=30)
REAL_MULTIPLIERS = {
    "1": F(1,1), "2": F(2,1), "3": F(3,1), "4": F(4,1),
    "8": F(8,1), "12": F(12,1), "24": F(24,1),
    "1/2": F(1,2), "1/3": F(1,3), "1/4": F(1,4),
    "1/8": F(1,8), "1/12": F(1,12), "1/24": F(1,24),
    "sqrt2": SQRT2, "sqrt3": SQRT3,
    "5": F(5,1), "6": F(6,1), "7": F(7,1),
    "1/5": F(1,5), "1/6": F(1,6), "1/7": F(1,7),
    "29": F(29,1), "39": F(39,1), "13": F(13,1),
    "1/29": F(1,29), "1/39": F(1,39), "1/13": F(1,13),
}

TARGETS = {
    "G":          G_CODATA,
    "alpha":      F(72973525643, 10**13),
    "alpha_inv":  F(137035999177, 10**9),
    "mp/me":      F(183615267343, 10**8),
    "mmu/me":     F(2067682830, 10**7),
    "mtau/me":    F(3477228280, 10**6),  # CORRECTED (Push #1 had 100x bug)
}

# ─────────────────────────────────────────────────────────────────────────────
# Candidate generator
# ─────────────────────────────────────────────────────────────────────────────
def gen_candidates(bases: dict, y_powers: dict, other_scales: dict, multipliers: dict,
                   target_value: Fraction):
    """Generate all candidates and return list of errors."""
    all_scales = {**y_powers, **other_scales}
    errs = []
    for bn, bv in bases.items():
        for sn, sv in all_scales.items():
            for mn, mv in multipliers.items():
                for fwd in (True, False):
                    try:
                        b = bv if fwd else (F(1)/bv if bv != 0 else None)
                        if b is None:
                            continue
                        val = mv * b * sv
                        if val > 0:
                            err = abs(val - target_value) / target_value * 100
                            errs.append(float(err))
                    except Exception:
                        pass
    return errs

# ─────────────────────────────────────────────────────────────────────────────
# (1) Real substrate + real grammar — baseline
# ─────────────────────────────────────────────────────────────────────────────
print("=" * 78)
print("(1) Baseline — real substrate × real grammar")
print("=" * 78)
real_grammar_size = len(REAL_BASES) * 2 * (len(REAL_Y_POWERS) + len(REAL_OTHER_SCALES)) * len(REAL_MULTIPLIERS)
print(f"Grammar size: {real_grammar_size} candidates per target\n")

baseline = {}
for tname, tval in TARGETS.items():
    errs = gen_candidates(REAL_BASES, REAL_Y_POWERS, REAL_OTHER_SCALES, REAL_MULTIPLIERS, tval)
    best = min(errs) if errs else float('inf')
    n013 = sum(1 for e in errs if e <= 0.13)
    baseline[tname] = {"best_err_pct": best, "n_le_0.13pct": n013, "n_candidates": len(errs)}
    print(f"  {tname:<14}  best err = {best:.4f}%   n≤0.13% = {n013}")

# ─────────────────────────────────────────────────────────────────────────────
# (2) Structural null — scramble grammar (subset of bases/multipliers/scales) AND substrate
# ─────────────────────────────────────────────────────────────────────────────
print("\n" + "=" * 78)
print("(2) Structural null model — scramble grammar AND substrate")
print("=" * 78)
print("For each trial:")
print("  - Sample 5-10 bases (from 10 real bases)")
print("  - Sample 10-20 multipliers (from 27 real multipliers)")
print("  - Sample Y-power range [k_min, k_max] with k_min in [1,5], k_max in [k_min+5, k_min+20]")
print("  - Scramble each chosen base by uniform(0.1, 10)")
print("  - Run full grammar, count ≤0.13% hits per target\n")

random.seed(2026)
N_TRIALS = 30  # each trial is expensive; keep small
real_base_keys = list(REAL_BASES.keys())
real_mult_keys = list(REAL_MULTIPLIERS.keys())

null_results_2d = {tname: {"hits_013": 0, "best_err_pct_min": float('inf'),
                            "best_err_distribution": []} for tname in TARGETS}

t_start = time.time()
for trial in range(N_TRIALS):
    # Sample grammar subset
    n_bases = random.randint(5, 10)
    n_mults = random.randint(10, 20)
    chosen_base_keys = random.sample(real_base_keys, n_bases)
    chosen_mult_keys = random.sample(real_mult_keys, n_mults)

    # Sample Y-power range
    k_min = random.randint(1, 5)
    k_max = k_min + random.randint(5, 20)
    y_powers_subset = {f"Y^{k}": Y**k for k in range(k_min, k_max+1)}
    y_powers_subset.update({f"Y_inv^{k}": YINV**k for k in range(1, min(8, k_max - k_min + 2))})

    # Scramble chosen bases
    bases_scrambled = {}
    for bk in chosen_base_keys:
        mult = random.uniform(0.1, 10.0)
        bases_scrambled[bk] = F(float(REAL_BASES[bk]) * mult).limit_denominator(10**5)

    multipliers_subset = {k: REAL_MULTIPLIERS[k] for k in chosen_mult_keys}

    # For each target, run the grammar
    for tname, tval in TARGETS.items():
        errs = gen_candidates(bases_scrambled, y_powers_subset, REAL_OTHER_SCALES,
                              multipliers_subset, tval)
        if not errs:
            continue
        best = min(errs)
        null_results_2d[tname]["best_err_distribution"].append(best)
        if best <= 0.13:
            null_results_2d[tname]["hits_013"] += 1
        if best < null_results_2d[tname]["best_err_pct_min"]:
            null_results_2d[tname]["best_err_pct_min"] = best

    if (trial + 1) % 5 == 0:
        elapsed = time.time() - t_start
        print(f"  ... {trial+1}/{N_TRIALS} trials done ({elapsed:.1f}s elapsed)")

print(f"\n  Total time: {time.time() - t_start:.1f}s\n")

print(f"{'Target':<14} {'Real best %':<14} {'Null min %':<14} {'Null mean %':<14} "
      f"{'Null hit ≤0.13%':>18}")
print("-" * 86)
for tname in TARGETS:
    real_best = baseline[tname]["best_err_pct"]
    dist = null_results_2d[tname]["best_err_distribution"]
    if not dist:
        print(f"  {tname}: no data")
        continue
    null_min = null_results_2d[tname]["best_err_pct_min"]
    null_mean = sum(dist) / len(dist)
    h013 = null_results_2d[tname]["hits_013"]
    print(f"{tname:<14} {real_best:<14.4f} {null_min:<14.4f} {null_mean:<14.4f} "
          f"{h013:>10}/{N_TRIALS:<7}")

# ─────────────────────────────────────────────────────────────────────────────
# (3) Fully random null — random grammar + random substrate constants
# ─────────────────────────────────────────────────────────────────────────────
print("\n" + "=" * 78)
print("(3) Fully random null — random grammar + random substrate constants")
print("=" * 78)
print("Stronger test: substrate constants drawn from uniform(0.001, 1000),")
print("grammar randomly sampled as above.\n")

null_results_full = {tname: {"hits_013": 0, "best_err_pct_min": float('inf'),
                              "best_err_distribution": []} for tname in TARGETS}

t_start = time.time()
for trial in range(N_TRIALS):
    n_bases = random.randint(5, 10)
    n_mults = random.randint(10, 20)
    chosen_base_keys = random.sample(real_base_keys, n_bases)
    chosen_mult_keys = random.sample(real_mult_keys, n_mults)

    k_min = random.randint(1, 5)
    k_max = k_min + random.randint(5, 20)
    # Generate fresh random Y, Y_inv
    Y_random = F(random.uniform(0.001, 1000)).limit_denominator(10**4)
    YINV_random = F(1) / Y_random if Y_random != 0 else F(1)
    y_powers_subset = {f"Y^{k}": Y_random**k for k in range(k_min, k_max+1)}
    y_powers_subset.update({f"Y_inv^{k}": YINV_random**k for k in range(1, min(8, k_max - k_min + 2))})

    # Random substrate constants
    bases_random = {}
    for bk in chosen_base_keys:
        val = random.uniform(0.001, 1000)
        bases_random[bk] = F(val).limit_denominator(10**4)

    multipliers_subset = {k: REAL_MULTIPLIERS[k] for k in chosen_mult_keys}

    for tname, tval in TARGETS.items():
        errs = gen_candidates(bases_random, y_powers_subset, REAL_OTHER_SCALES,
                              multipliers_subset, tval)
        if not errs:
            continue
        best = min(errs)
        null_results_full[tname]["best_err_distribution"].append(best)
        if best <= 0.13:
            null_results_full[tname]["hits_013"] += 1
        if best < null_results_full[tname]["best_err_pct_min"]:
            null_results_full[tname]["best_err_pct_min"] = best

    if (trial + 1) % 5 == 0:
        elapsed = time.time() - t_start
        print(f"  ... {trial+1}/{N_TRIALS} trials done ({elapsed:.1f}s elapsed)")

print(f"\n  Total time: {time.time() - t_start:.1f}s\n")

print(f"{'Target':<14} {'Real best %':<14} {'Null min %':<14} {'Null mean %':<14} "
      f"{'Null hit ≤0.13%':>18}")
print("-" * 86)
for tname in TARGETS:
    real_best = baseline[tname]["best_err_pct"]
    dist = null_results_full[tname]["best_err_distribution"]
    if not dist:
        print(f"  {tname}: no data")
        continue
    null_min = null_results_full[tname]["best_err_pct_min"]
    null_mean = sum(dist) / len(dist)
    h013 = null_results_full[tname]["hits_013"]
    print(f"{tname:<14} {real_best:<14.4f} {null_min:<14.4f} {null_mean:<14.4f} "
          f"{h013:>10}/{N_TRIALS:<7}")

# ─────────────────────────────────────────────────────────────────────────────
# SAVE
# ─────────────────────────────────────────────────────────────────────────────
def summarise(dist, hits, n_trials):
    if not dist:
        return None
    s = sorted(dist)
    return {
        "n_trials":     n_trials,
        "hits_013":     hits,
        "min_pct":      s[0],
        "p10_pct":      s[n_trials // 10],
        "p50_pct":      s[n_trials // 2],
        "p90_pct":      s[9 * n_trials // 10],
        "max_pct":      s[-1],
        "mean_pct":     sum(dist) / len(dist),
        "hit_rate_pct": hits / n_trials * 100,
    }

out = {
    "baseline_real_substrate_real_grammar": {
        tname: baseline[tname] for tname in TARGETS
    },
    "real_grammar_size": real_grammar_size,
    "structural_null_summary": {
        tname: summarise(null_results_2d[tname]["best_err_distribution"],
                         null_results_2d[tname]["hits_013"], N_TRIALS)
        for tname in TARGETS
    },
    "fully_random_null_summary": {
        tname: summarise(null_results_full[tname]["best_err_distribution"],
                         null_results_full[tname]["hits_013"], N_TRIALS)
        for tname in TARGETS
    },
}
outp = Path("/home/z/my-project/results/nq2_structural_null.json")
with open(outp, "w") as f:
    json.dump(out, f, indent=2, default=str)
print(f"\n[ok] Results saved to {outp}")
