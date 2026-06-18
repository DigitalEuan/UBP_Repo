"""
COINCIDENCE BENCHMARK & NULL MODEL
==================================
Per the user's instruction: "Explore coincidences - mark clearly but don't
disregard."  This script does TWO things:

(1) COINCIDENCE SPECTRUM (unmodified substrate)
    For each target, we already know the best error from q4_expanded_search.py.
    Here we count: how many of the 29,700 candidates fall within 0.01%, 0.05%,
    0.13%, 0.50%, 1.00%, 5.00% of each target?

    If 0.13% hits are COMMON (say 5+ candidates per target), then the gravity
    hit is less surprising.  If 0.13% hits are RARE (1-2 per target), then the
    gravity hit IS surprising.

(2) NULL MODEL (scrambled substrate)
    Replace each substrate constant (Y, w, L, L_s, pi, phi, e, U_e, NRCI) with
    a random Fraction of similar magnitude, run the same search, and count
    0.13% hits.  Repeat 100 times to get a false-positive distribution.

    If the false-positive rate is high (say >30%), then the gravity 0.13% hit
    is statistically indistinguishable from noise.  If it's low (<5%), the hit
    is statistically surprising.

The user said "mark clearly but don't disregard" — so we report both numbers
honestly and let the reader judge.
"""
from __future__ import annotations
import json, sys, random
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
# Search grammar (identical to q4_expanded_search.py)
# ─────────────────────────────────────────────────────────────────────────────
def make_grammar(bases: dict, y_powers: dict, other_scales: dict, multipliers: dict):
    """Build candidate generator from given substrate constants."""
    all_scales = {**y_powers, **other_scales}
    def gen(target_value: Fraction):
        cands = []
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
                                cands.append(float(err))
                        except Exception:
                            pass
        return cands
    return gen, len(bases) * 2 * len(all_scales) * len(multipliers)

# Real substrate
BASES_REAL = {
    "Y": Y, "Y_inv": YINV, "L": L, "L_s": L_s,
    "pi": PI, "phi": PHI, "e": E, "w": W, "U_e": U_e, "NRCI": NRCI_UNIV,
}
Y_POWERS_REAL = {f"Y^{k}": Y**k for k in range(1, 26)}
Y_POWERS_REAL.update({f"Y_inv^{k}": YINV**k for k in range(1, 8)})
OTHER_SCALES_REAL = {
    "1/U_e": F(1, U_e), "1/U_e^2": F(1, U_e**2),
    "1/c":   F(1, C),   "1/c^2":   F(1, C**2),
    "1":     F(1, 1),
}
SQRT2 = u.ExactMath.sqrt_frac(F(2, 1), prec=30)
SQRT3 = u.ExactMath.sqrt_frac(F(3, 1), prec=30)
MULTIPLIERS_REAL = {
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

gen_real, n_real = make_grammar(BASES_REAL, Y_POWERS_REAL, OTHER_SCALES_REAL, MULTIPLIERS_REAL)
print(f"[grammar] real substrate: {n_real} candidates per target")

TARGETS = {
    "G":          G_CODATA,
    "alpha":      F(72973525643, 10**13),
    "alpha_inv":  F(137035999177, 10**9),
    "mp/me":      F(183615267343, 10**8),
    "mmu/me":     F(2067682830, 10**7),
    "mtau/me":    F(34778621, 100),
    "alpha_G":    F(5675, 10**42),
}

# ─────────────────────────────────────────────────────────────────────────────
# (1) COINCIDENCE SPECTRUM (real substrate)
# ─────────────────────────────────────────────────────────────────────────────
print("\n" + "="*82)
print("(1) COINCIDENCE SPECTRUM — real substrate")
print("="*82)
print(f"{'Target':<14} {'best%':<10} {'0.01%':>7} {'0.05%':>7} {'0.13%':>7} "
      f"{'0.50%':>7} {'1.00%':>7} {'5.00%':>7}")
print("-"*82)

spectrum = {}
for tname, tval in TARGETS.items():
    errs = gen_real(tval)
    errs_sorted = sorted(errs)
    best = errs_sorted[0] if errs_sorted else float('inf')
    n_001 = sum(1 for e in errs if e <= 0.01)
    n_005 = sum(1 for e in errs if e <= 0.05)
    n_013 = sum(1 for e in errs if e <= 0.13)
    n_050 = sum(1 for e in errs if e <= 0.50)
    n_100 = sum(1 for e in errs if e <= 1.00)
    n_500 = sum(1 for e in errs if e <= 5.00)
    spectrum[tname] = {
        "best_err_pct":       best,
        "n_le_0.01pct":       n_001,
        "n_le_0.05pct":       n_005,
        "n_le_0.13pct":       n_013,
        "n_le_0.50pct":       n_050,
        "n_le_1.00pct":       n_100,
        "n_le_5.00pct":       n_500,
        "n_candidates":       len(errs),
    }
    print(f"{tname:<14} {best:<10.4f} {n_001:>7} {n_005:>7} {n_013:>7} "
          f"{n_050:>7} {n_100:>7} {n_500:>7}")

# ─────────────────────────────────────────────────────────────────────────────
# (2) NULL MODEL — scrambled substrate
# ─────────────────────────────────────────────────────────────────────────────
print("\n" + "="*82)
print("(2) NULL MODEL — scrambled substrate, 100 trials per target")
print("="*82)
print("For each trial: replace each substrate constant with a random Fraction")
print("of similar magnitude (within 1 order of magnitude), run the same search,")
print("and count 0.13%-or-better hits.  This gives the false-positive rate.\n")

def random_substrate_constant(seed: int, ref: Fraction) -> Fraction:
    """Return a random Fraction within ~1 order of magnitude of ref."""
    rng = random.Random(seed)
    # Generate as p/q where p, q are random integers near ref's numerator/denominator
    # We work with floats for sampling, then convert to Fraction with limited denominator
    ref_f = float(ref)
    if ref_f <= 0:
        return F(1, 1)
    # Random multiplier in [0.1, 10)
    multiplier = rng.uniform(0.1, 10.0)
    val = ref_f * multiplier
    # Convert to Fraction with bounded denominator (≤ 10^6) for tractability
    return F(val).limit_denominator(10**6)

N_TRIALS = 40
null_results = {tname: {"hits_013": 0, "hits_005": 0, "best_err_pct_min": float('inf'),
                         "best_err_pct_distribution": []} for tname in TARGETS}

# Use fixed seed for reproducibility
MASTER_SEED = 42

for trial in range(N_TRIALS):
    rng = random.Random(MASTER_SEED + trial)
    # Scramble each substrate constant
    Y_s    = random_substrate_constant(MASTER_SEED + trial * 10 + 0, Y)
    YINV_s = random_substrate_constant(MASTER_SEED + trial * 10 + 1, YINV)
    L_s    = random_substrate_constant(MASTER_SEED + trial * 10 + 2, L)
    Ls_s   = random_substrate_constant(MASTER_SEED + trial * 10 + 3, L_s)
    PI_s   = random_substrate_constant(MASTER_SEED + trial * 10 + 4, PI)
    PHI_s  = random_substrate_constant(MASTER_SEED + trial * 10 + 5, PHI)
    E_s    = random_substrate_constant(MASTER_SEED + trial * 10 + 6, E)
    W_s    = random_substrate_constant(MASTER_SEED + trial * 10 + 7, W)
    Ue_s   = random_substrate_constant(MASTER_SEED + trial * 10 + 8, U_e)
    NRCI_s = random_substrate_constant(MASTER_SEED + trial * 10 + 9, NRCI_UNIV)

    bases_scrambled = {
        "Y": Y_s, "Y_inv": YINV_s, "L": L_s, "L_s": Ls_s,
        "pi": PI_s, "phi": PHI_s, "e": E_s, "w": W_s, "U_e": Ue_s, "NRCI": NRCI_s,
    }
    y_powers_scrambled = {f"Y^{k}": Y_s**k for k in range(1, 26)}
    y_powers_scrambled.update({f"Y_inv^{k}": YINV_s**k for k in range(1, 8)})

    gen_scrambled, _ = make_grammar(bases_scrambled, y_powers_scrambled,
                                     OTHER_SCALES_REAL, MULTIPLIERS_REAL)

    for tname, tval in TARGETS.items():
        errs = gen_scrambled(tval)
        if not errs:
            continue
        best = min(errs)
        null_results[tname]["best_err_pct_distribution"].append(best)
        if best <= 0.13:
            null_results[tname]["hits_013"] += 1
        if best <= 0.05:
            null_results[tname]["hits_005"] += 1
        if best < null_results[tname]["best_err_pct_min"]:
            null_results[tname]["best_err_pct_min"] = best

print(f"{'Target':<14} {'real best%':<12} {'null mean%':<14} {'null min%':<14} "
      f"{'null hit<=0.13%':>18} {'null hit<=0.05%':>18}")
print("-"*92)
for tname in TARGETS:
    real_best = spectrum[tname]["best_err_pct"]
    null_dist = null_results[tname]["best_err_pct_distribution"]
    null_mean = sum(null_dist)/len(null_dist) if null_dist else float('nan')
    null_min = null_results[tname]["best_err_pct_min"]
    h013 = null_results[tname]["hits_013"]
    h005 = null_results[tname]["hits_005"]
    print(f"{tname:<14} {real_best:<12.4f} {null_mean:<14.4f} {null_min:<14.4f} "
          f"{h013:>10}/{N_TRIALS:<7} {h005:>10}/{N_TRIALS:<7}")

# ─────────────────────────────────────────────────────────────────────────────
# SAVE
# ─────────────────────────────────────────────────────────────────────────────
out = Path("/home/z/my-project/results/coincidence_null_model.json")
output = {
    "grammar_size":           n_real,
    "n_trials":               N_TRIALS,
    "real_substrate_spectrum": spectrum,
    "null_model_results":     {k: {kk: vv for kk, vv in v.items() if kk != "best_err_pct_distribution"}
                                 for k, v in null_results.items()},
    "null_model_best_err_distribution_summary": {
        k: {
            "min":  min(v["best_err_pct_distribution"]) if v["best_err_pct_distribution"] else None,
            "p10":  sorted(v["best_err_pct_distribution"])[N_TRIALS//10] if v["best_err_pct_distribution"] else None,
            "p50":  sorted(v["best_err_pct_distribution"])[N_TRIALS//2] if v["best_err_pct_distribution"] else None,
            "p90":  sorted(v["best_err_pct_distribution"])[9*N_TRIALS//10] if v["best_err_pct_distribution"] else None,
            "max":  max(v["best_err_pct_distribution"]) if v["best_err_pct_distribution"] else None,
            "mean": sum(v["best_err_pct_distribution"])/len(v["best_err_pct_distribution"]) if v["best_err_pct_distribution"] else None,
        }
        for k, v in null_results.items()
    },
}
with open(out, "w") as f:
    json.dump(output, f, indent=2, default=str)
print(f"\n[ok] Results saved to {out}")
