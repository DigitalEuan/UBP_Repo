"""
NQ3-bis — Null model sanity check on the best out-of-sample predictions.

The NQ3 results are striking (m_W/m_Z at 0.035%, α drift bound at 0.006%,
λ_QCD/m_e at 0.074%, etc.). Before claiming these as out-of-sample successes,
we must check whether the structural null model from NQ2 would also produce
comparable hits for these targets.

We apply the structural null from NQ2 (scramble substrate constants × grammar)
to the four most interesting NQ3 targets.
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
PI = constants["PI"]; PHI = constants["PHI"]; E = constants["E"]
Y = constants["Y"]; YINV = constants["Y_INV"]
W = constants["WOBBLE"]; L = constants["SINK_L"]
L_s = u.PARTICLE_PHYSICS.L_s; U_e = u.PARTICLE_PHYSICS.U_e
C = F(299792458, 1)
NRCI_UNIV = F(7623, 10000)

REAL_BASES = {
    "Y": Y, "Y_inv": YINV, "L": L, "L_s": L_s,
    "pi": PI, "phi": PHI, "e": E, "w": W, "U_e": U_e, "NRCI": NRCI_UNIV,
}
REAL_Y_POWERS = {f"Y^{k}": Y**k for k in range(1, 41)}
REAL_Y_POWERS.update({f"Y_inv^{k}": YINV**k for k in range(1, 11)})
REAL_OTHER_SCALES = {
    "1/U_e": F(1, U_e), "1/U_e^2": F(1, U_e**2),
    "1/c": F(1, C), "1/c^2": F(1, C**2),
    "1": F(1, 1),
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
    "169": F(169,1), "2197": F(2197,1),
    "1/169": F(1,169), "1/2197": F(1,2197),
}

# The four most interesting NQ3 targets
TARGETS = {
    "H0_midpoint":     F((6736+7304), 200),  # 70.20
    "mW/mZ":           F(80379, 911876),     # 0.088153
    "lambda_QCD_over_me": F(200000, 511),    # 391.4
    "alpha_drift_bound": F(1, 10**17),       # 1e-17
    "mn-mp_over_me":   F(1293, 511),         # 2.530
    "g-2_anomaly_mu":  F(251, 10**9),        # 2.51e-9 (corrected: was e-7 in script; bound is e-9)
}

# Note: g-2 anomaly script had a bug too — let me re-check.
# Fermilab 2021: a_mu = (g-2)/2 - (g-2)/2|SM = 251 × 10^-11 = 2.51e-9
# So 2.51e-9 is correct.
# But the script used F(251, 10**9) = 2.51e-7. Let me check.
# Actually 251/10^9 = 2.51e-7. That's WRONG. Should be 251/10^11 = 2.51e-9.
# But for null-model purposes the magnitude matters, so we'll recompute properly below.

# Use the correct g-2 anomaly value
TARGETS["g-2_anomaly_mu"] = F(251, 10**11)  # 2.51e-9 (Fermilab 2021)
print(f"Corrected g-2_anomaly_mu target: {float(TARGETS['g-2_anomaly_mu']):.4e}")

# ─────────────────────────────────────────────────────────────────────────────
# Real substrate baseline
# ─────────────────────────────────────────────────────────────────────────────
def gen_candidates(bases, y_powers, other_scales, multipliers, target_value):
    all_scales = {**y_powers, **other_scales}
    errs = []
    for bn, bv in bases.items():
        for sn, sv in all_scales.items():
            for mn, mv in multipliers.items():
                for fwd in (True, False):
                    try:
                        b = bv if fwd else (F(1)/bv if bv != 0 else None)
                        if b is None: continue
                        val = mv * b * sv
                        if val > 0:
                            err = abs(val - target_value) / target_value * 100
                            errs.append(float(err))
                    except: pass
    return errs

print("\nBaseline (real substrate × real grammar):")
baseline = {}
for tname, tval in TARGETS.items():
    errs = gen_candidates(REAL_BASES, REAL_Y_POWERS, REAL_OTHER_SCALES, REAL_MULTIPLIERS, tval)
    best = min(errs) if errs else float('inf')
    n013 = sum(1 for e in errs if e <= 0.13)
    baseline[tname] = {"best_err_pct": best, "n_le_0.13pct": n013}
    print(f"  {tname:<25} best={best:.4f}%  n≤0.13%={n013}")

# ─────────────────────────────────────────────────────────────────────────────
# Structural null (scramble substrate × grammar) — same as NQ2
# ─────────────────────────────────────────────────────────────────────────────
print("\n" + "=" * 78)
print("Structural null model (scramble substrate × grammar) — 30 trials")
print("=" * 78)

random.seed(31337)
N_TRIALS = 30
real_base_keys = list(REAL_BASES.keys())
real_mult_keys = list(REAL_MULTIPLIERS.keys())

null_results = {tname: {"hits_013": 0, "best_err_pct_min": float('inf'),
                         "best_err_distribution": []} for tname in TARGETS}

t_start = time.time()
for trial in range(N_TRIALS):
    n_bases = random.randint(5, 10)
    n_mults = random.randint(10, 20)
    chosen_base_keys = random.sample(real_base_keys, n_bases)
    chosen_mult_keys = random.sample(real_mult_keys, n_mults)

    k_min = random.randint(1, 5)
    k_max = k_min + random.randint(5, 35)  # extended to match NQ3's Y^1..40 range
    y_powers_subset = {f"Y^{k}": Y**k for k in range(k_min, k_max+1)}
    y_powers_subset.update({f"Y_inv^{k}": YINV**k for k in range(1, min(11, k_max - k_min + 2))})

    bases_scrambled = {}
    for bk in chosen_base_keys:
        mult = random.uniform(0.1, 10.0)
        bases_scrambled[bk] = F(float(REAL_BASES[bk]) * mult).limit_denominator(10**5)

    multipliers_subset = {k: REAL_MULTIPLIERS[k] for k in chosen_mult_keys}

    for tname, tval in TARGETS.items():
        errs = gen_candidates(bases_scrambled, y_powers_subset, REAL_OTHER_SCALES,
                              multipliers_subset, tval)
        if not errs: continue
        best = min(errs)
        null_results[tname]["best_err_distribution"].append(best)
        if best <= 0.13:
            null_results[tname]["hits_013"] += 1
        if best < null_results[tname]["best_err_pct_min"]:
            null_results[tname]["best_err_pct_min"] = best

    if (trial + 1) % 5 == 0:
        print(f"  ... {trial+1}/{N_TRIALS} trials done ({time.time()-t_start:.1f}s)")

print(f"\nTotal time: {time.time()-t_start:.1f}s\n")
print(f"{'Target':<25} {'Real best %':<14} {'Null min %':<14} {'Null mean %':<14} {'Null hit ≤0.13%':>18}")
print("-" * 90)
for tname in TARGETS:
    real_best = baseline[tname]["best_err_pct"]
    dist = null_results[tname]["best_err_distribution"]
    if not dist: continue
    null_min = null_results[tname]["best_err_pct_min"]
    null_mean = sum(dist)/len(dist)
    h013 = null_results[tname]["hits_013"]
    pct = h013/N_TRIALS*100
    surprising = " <-- SURPRISING" if pct < 5 else (" <-- marginal" if pct < 20 else "")
    print(f"{tname:<25} {real_best:<14.4f} {null_min:<14.4f} {null_mean:<14.4f} "
          f"{h013:>10}/{N_TRIALS:<7} ({pct:.1f}%){surprising}")

# Save
out = {
    "targets": {k: float(v) for k, v in TARGETS.items()},
    "baseline_real_substrate": baseline,
    "structural_null_summary": {
        tname: {
            "n_trials": N_TRIALS,
            "hits_013": null_results[tname]["hits_013"],
            "hit_rate_pct": null_results[tname]["hits_013"]/N_TRIALS*100,
            "min_pct": null_results[tname]["best_err_pct_min"],
            "mean_pct": sum(null_results[tname]["best_err_distribution"])/len(null_results[tname]["best_err_distribution"]),
            "p10_pct": sorted(null_results[tname]["best_err_distribution"])[N_TRIALS//10],
            "p50_pct": sorted(null_results[tname]["best_err_distribution"])[N_TRIALS//2],
            "p90_pct": sorted(null_results[tname]["best_err_distribution"])[9*N_TRIALS//10],
        }
        for tname in TARGETS
    },
    "note_on_g2_anomaly_bug": "Push #2's nq3_out_of_sample.py used F(251, 10**9) = 2.51e-7 for the muon g-2 anomaly, but the correct value is 2.51e-9 (Fermilab 2021). This null-model re-test uses the correct value F(251, 10**11).",
}
outp = Path("/home/z/my-project/results/nq3_null_check.json")
with open(outp, "w") as f:
    json.dump(out, f, indent=2, default=str)
print(f"\n[ok] Results saved to {outp}")
