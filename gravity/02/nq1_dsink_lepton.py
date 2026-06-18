"""
NQ1 — D-Sink^k / L generalisation test (lepton generations).

HYPOTHESIS (from Push #1, §8 NQ1)
---------------------------------
Push #1 found that m_μ/m_e is hit by  13/L = 169/w  with 0.0294% error.
This is structurally clean: 13 = D-Sink dimension, L = w/13 = D-Sink leakage,
so 13/L = 13²/w = 169/w. No Y-power, no integer close to the target.

The natural generalisation is:
    m_μ/m_e    ≈  13/L  =  13²/w  =  169/w         (k=1: D-Sink^1 / L)
    m_τ/m_e    ≈  39/L  =  3·13/L  =  507/w        (k=2: 3·D-Sink / L = Triad·D-Sink/L)
                 OR  169/L  =  13²/L  =  2197/w    (k=2: D-Sink² / L)
                 OR  Y^k · (13/L) for various k
    m_p/m_e    ≈  ?      (test multiple patterns)

This script:
  1. Computes 13/L, 39/L, 169/L, 13·Y^k/L for k=1..6 against the lepton ratios
  2. Runs a FOCUSED null model: scramble ONLY w (keeping 13 fixed as integer)
     to test whether 13/L's accuracy is statistically surprising
  3. Tests whether the D-Sink^k/L pattern generalises across generations
  4. Compares against the existing PARTICLE_PHYSICS atlas lens formulas
"""
from __future__ import annotations
import json, sys, random, math
from fractions import Fraction
from pathlib import Path

sys.path.insert(0, "/home/z/my-project/scripts")
import ubp_unified_v5 as u

F = Fraction

pp = u.PARTICLE_PHYSICS
L = pp.L
w = pp.wobble
Y = pp.Y
Y_inv = pp.Y_INV
pi = pp.pi
phi = pp.phi
e_const = pp.e_const
L_s = pp.L_s
U_e = pp.U_e

# ─────────────────────────────────────────────────────────────────────────────
# CORRECT TARGETS  (Push #1 had a 100x bug on m_tau/m_e — fixing here)
# ─────────────────────────────────────────────────────────────────────────────
# All CODATA 2022 / PDG 2024 values, dimensionless
TARGETS = {
    "m_e/m_e":         F(1, 1),                                # trivial — for self-check
    "m_mu/m_e":        F(2067682830, 10**7),                   # 206.7682830  (PDG)
    "m_tau/m_e":       F(3477228280, 10**6),                   # 3477.228280  (PDG) -- CORRECT, not 347786!
    "m_p/m_e":         F(183615267343, 10**8),                 # 1836.15267343 (CODATA 2022)
    "m_n/m_e":         F(18386831610, 10**7),                  # 1838.6831610 (calc from m_n - m_p + L_s approx)
    "m_p/m_mu":        F(183615267343, 10**8) / F(2067682830, 10**7),  # m_p/m_mu
}

print("=" * 78)
print("NQ1 — D-Sink^k / L generalisation test")
print("=" * 78)
print("\nCorrected targets:")
for name, val in TARGETS.items():
    print(f"  {name:<14} = {float(val):.6f}")

# ─────────────────────────────────────────────────────────────────────────────
# 1. Direct predictions of D-Sink^k/L family
# ─────────────────────────────────────────────────────────────────────────────
print("\n" + "=" * 78)
print("(1) D-Sink^k / L family — direct predictions")
print("=" * 78)

# Family: 13^k / L for k = 1, 2, 3, ...
# Also: (Triad * D-Sink^k) / L = (3 * 13^k) / L for k = 0, 1, 2, ...
# Also: 13^k / L_s for k = 1, 2, ...

family_predictions = []
for k in range(0, 7):
    pred_13k_L   = F(13)**k / L              # 13^k / L  =  13^(k+1) / w  · 13  =  13^(k+2) / w (if L=w/13)
    # actually 13^k / L = 13^k / (w/13) = 13^(k+1) / w
    pred_3_13k_L = F(3) * F(13)**k / L       # 3·13^k / L  =  3·13^(k+1) / w
    pred_13k_Ls  = F(13)**k / L_s            # 13^k / L_s
    family_predictions.append({
        "k": k,
        "13^k/L": pred_13k_L,
        "3·13^k/L": pred_3_13k_L,
        "13^k/L_s": pred_13k_Ls,
    })

# Pretty print
print(f"\n{'k':<3} {'13^k/L':<18} {'3·13^k/L':<18} {'13^k/L_s':<18}")
for p in family_predictions:
    print(f"{p['k']:<3} {float(p['13^k/L']):<18.6f} {float(p['3·13^k/L']):<18.6f} {float(p['13^k/L_s']):<18.6f}")

# Find best match for each target
print("\n" + "-" * 78)
print("Best D-Sink^k/L match per target:")
print("-" * 78)
print(f"{'Target':<14} {'Best formula':<22} {'Value':<14} {'Target val':<14} {'Error %':<10}")
print("-" * 78)

best_matches = {}
for tname, tval in TARGETS.items():
    if tname == "m_e/m_e":
        continue
    candidates = []
    for p in family_predictions:
        candidates.append((f"13^{p['k']}/L",     p["13^k/L"]))
        candidates.append((f"3·13^{p['k']}/L",   p["3·13^k/L"]))
        candidates.append((f"13^{p['k']}/L_s",   p["13^k/L_s"]))
    best = min(candidates, key=lambda c: abs(float(c[1]) - float(tval))/float(tval))
    err = abs(float(best[1]) - float(tval))/float(tval) * 100
    best_matches[tname] = (best[0], float(best[1]), float(tval), err)
    print(f"{tname:<14} {best[0]:<22} {float(best[1]):<14.4f} {float(tval):<14.4f} {err:<10.4f}")

# ─────────────────────────────────────────────────────────────────────────────
# 2. Generalisation check — is m_mu/me really 13/L?
# ─────────────────────────────────────────────────────────────────────────────
print("\n" + "=" * 78)
print("(2) m_μ/m_e — confirm 13/L = 169/w formula and compare to PARTICLE_PHYSICS atlas")
print("=" * 78)

# Push #1 finding: m_mu/m_e ≈ 13/L
pred_13_L = F(13) / L
target_mu = TARGETS["m_mu/m_e"]
err_13_L = abs(pred_13_L - target_mu) / target_mu * 100
print(f"  13/L              = {float(pred_13_L):.6f}")
print(f"  m_μ/m_e (target)  = {float(target_mu):.6f}")
print(f"  Error             = {float(err_13_L):.4f}%")

# Existing atlas formula: m_mu_ratio = 206 + 12*L
pred_atlas = F(206) + 12 * L
err_atlas = abs(pred_atlas - target_mu) / target_mu * 100
print(f"\n  Atlas formula 206 + 12L  = {float(pred_atlas):.6f}  (err {float(err_atlas):.4f}%)")

# Alternative: what if we DON'T round to 206? Try (206 + 12*L) vs (13/L)?
# Both are substrate-internal, both should be tested under null model.

# ─────────────────────────────────────────────────────────────────────────────
# 3. Focused null model — scramble ONLY w, keep integer 13 fixed
# ─────────────────────────────────────────────────────────────────────────────
print("\n" + "=" * 78)
print("(3) Focused null model — scramble ONLY w, keep integer 13 fixed")
print("=" * 78)
print("Tests whether 13/L's accuracy on m_μ/m_e is statistically surprising.")
print("Null hypothesis: w is a random fraction in [w/10, 10·w]; 13/L is computed.")
print("If real w's hit is in the lower tail of null distribution, it's surprising.\n")

random.seed(12345)
N_TRIALS = 5000  # cheap because we only compute one formula per trial

null_errors = []
for trial in range(N_TRIALS):
    # Scramble w by uniform(0.1, 10)
    multiplier = random.uniform(0.1, 10.0)
    w_scrambled = float(w) * multiplier
    L_scrambled = w_scrambled / 13.0
    pred = 13.0 / L_scrambled  # = 169 / w_scrambled
    err = abs(pred - float(target_mu)) / float(target_mu) * 100
    null_errors.append(err)

null_errors.sort()
real_err = float(err_13_L)
hits_at_real = sum(1 for e in null_errors if e <= real_err)
p10 = null_errors[N_TRIALS // 10]
p25 = null_errors[N_TRIALS // 4]
p50 = null_errors[N_TRIALS // 2]
p75 = null_errors[3 * N_TRIALS // 4]
p90 = null_errors[9 * N_TRIALS // 10]
p99 = null_errors[99 * N_TRIALS // 100]
min_err = null_errors[0]
mean_err = sum(null_errors) / N_TRIALS

print(f"  Real substrate 13/L error on m_μ/m_e: {real_err:.4f}%")
print(f"  Null distribution ({N_TRIALS} trials, scramble w only):")
print(f"    min:    {min_err:.4f}%")
print(f"    p10:    {p10:.4f}%")
print(f"    p25:    {p25:.4f}%")
print(f"    p50:    {p50:.4f}%")
print(f"    p75:    {p75:.4f}%")
print(f"    p90:    {p90:.4f}%")
print(f"    p99:    {p99:.4f}%")
print(f"    mean:   {mean_err:.4f}%")
print(f"  Trials with err ≤ real_err: {hits_at_real}/{N_TRIALS} = {hits_at_real/N_TRIALS*100:.2f}%")
print(f"  Real substrate's percentile: {(N_TRIALS - hits_at_real)/N_TRIALS*100:.2f}%  (100% = best possible)")

if hits_at_real / N_TRIALS < 0.05:
    verdict = "REAL substrate is SURPRISING (< 5% null hit rate)"
elif hits_at_real / N_TRIALS < 0.20:
    verdict = "REAL substrate is MARGINALLY SURPRISING (5-20% null hit rate)"
else:
    verdict = "REAL substrate is NOT surprising (≥ 20% null hit rate)"
print(f"\n  VERDICT: {verdict}")

# ─────────────────────────────────────────────────────────────────────────────
# 4. Same null model on m_τ/m_e — does 39/L work?
# ─────────────────────────────────────────────────────────────────────────────
print("\n" + "=" * 78)
print("(4) m_τ/m_e — does the D-Sink^k/L pattern predict the correct value?")
print("=" * 78)

target_tau = TARGETS["m_tau/m_e"]
print(f"  Correct target m_τ/m_e = {float(target_tau):.6f}  (NOT 347786 as in Push #1)")
print()

# Test all members of the family
print(f"  {'Formula':<20} {'Value':<14} {'Error %':<10}")
print(f"  {'-'*20} {'-'*14} {'-'*10}")
tau_candidates = [
    ("13/L",      F(13)/L),
    ("39/L",      F(39)/L),       # 3 * 13 / L  -- triad × D-Sink
    ("169/L",     F(169)/L),      # 13^2 / L
    ("507/L",     F(507)/L),      # 3 * 13^2 / L
    ("13·Y/L",    F(13)*Y/L),
    ("13·Y²/L",   F(13)*Y**2/L),
    ("13·Y⁻¹/L",  F(13)*Y_inv/L),
    ("13·Y⁻²/L",  F(13)*Y_inv**2/L),
    ("13·phi/L",  F(13)*phi/L),
    ("13·e/L",    F(13)*e_const/L),
    ("13·pi/L",   F(13)*pi/L),
    ("13/L·Y^3",  F(13)*Y**3/L),
    ("39/L_s",    F(39)/L_s),
    ("169/L_s",   F(169)/L_s),
    ("3·13/L_s",  F(3)*F(13)/L_s),
]
for name, pred in tau_candidates:
    err = abs(float(pred) - float(target_tau)) / float(target_tau) * 100
    print(f"  {name:<20} {float(pred):<14.4f} {err:<10.4f}")

# Atlas formula for tau (Push #1 source)
m_e_target_MeV = F(51099895, 100000000)  # 0.51099895 MeV
tau_atlas_pred = (F(17)*Y_inv**4 + (F(2)*Y_inv + Y) + (Y_inv*F(24,23) + F(8)*Y)) * m_e_target_MeV
# Convert this mass (in MeV) to a ratio by dividing by m_e
tau_atlas_ratio = tau_atlas_pred / m_e_target_MeV
err_tau_atlas = abs(tau_atlas_ratio - target_tau) / target_tau * 100
print(f"\n  Atlas formula (24D MPG Lever) = {float(tau_atlas_ratio):.6f}  (err {float(err_tau_atlas):.4f}%)")
print(f"  Note: atlas uses m_e_target in MeV, so the prediction is dimensionally mass in MeV;")
print(f"        when normalised by m_e it gives the dimensionless ratio above.")

# ─────────────────────────────────────────────────────────────────────────────
# 5. Generalisation across generations — pattern detection
# ─────────────────────────────────────────────────────────────────────────────
print("\n" + "=" * 78)
print("(5) Generalisation pattern across lepton generations")
print("=" * 78)
print("If D-Sink^k/L generalises, we expect a smooth progression in k.")
print("Generational ratios:")
print(f"  m_μ/m_e    = {float(TARGETS['m_mu/m_e']):.4f}    (k=1 candidate: 13/L = {float(F(13)/L):.4f})")
print(f"  m_τ/m_e    = {float(TARGETS['m_tau/m_e']):.4f}    (k=2 candidate: ?)")
print(f"  m_τ/m_μ    = {float(TARGETS['m_tau/m_e']/TARGETS['m_mu/m_e']):.4f}")
print(f"  13·(m_τ/m_μ) = {float(13 * TARGETS['m_tau/m_e']/TARGETS['m_mu/m_e']):.4f}")
print(f"  (m_τ/m_μ)² · 13 = {float(13 * (TARGETS['m_tau/m_e']/TARGETS['m_mu/m_e'])**2):.4f}")
print(f"  log(m_τ/m_μ)/log(13) = {math.log(float(TARGETS['m_tau/m_e']/TARGETS['m_mu/m_e']))/math.log(13):.4f}")
print(f"  log(m_p/m_μ)/log(13) = {math.log(float(TARGETS['m_p/m_e']/TARGETS['m_mu/m_e']))/math.log(13):.4f}")
print(f"  log(m_p/m_e)/log(13) = {math.log(float(TARGETS['m_p/m_e']))/math.log(13):.4f}")
print(f"  log(m_μ/m_e)/log(13) = {math.log(float(TARGETS['m_mu/m_e']))/math.log(13):.4f}")
print(f"  log(m_τ/m_e)/log(13) = {math.log(float(TARGETS['m_tau/m_e']))/math.log(13):.4f}")

# If m_μ/m_e = 13/L (k=1), then m_τ/m_e would be at "k=?" along same family
# 13^k / L = m_target  =>  k = log(m_target · L) / log(13)
k_for_tau  = math.log(float(target_tau) * float(L)) / math.log(13)
k_for_mu   = math.log(float(target_mu) * float(L)) / math.log(13)
k_for_proton = math.log(float(TARGETS['m_p/m_e']) * float(L)) / math.log(13)
print(f"\n  Implied k for 13^k/L = m_target:")
print(f"    m_μ/m_e   k = {k_for_mu:.4f}  (close to 1.0 — confirms 13/L formula)")
print(f"    m_τ/m_e   k = {k_for_tau:.4f}  (would generalise if ≈ 2.0)")
print(f"    m_p/m_e   k = {k_for_proton:.4f}  (would generalise if integer or simple fraction)")

# ─────────────────────────────────────────────────────────────────────────────
# 6. Same null model on m_τ/m_e for the BEST candidate
# ─────────────────────────────────────────────────────────────────────────────
print("\n" + "=" * 78)
print("(6) Null model for m_τ/m_e — best D-Sink^k/L candidate")
print("=" * 78)

# Find best candidate
best_tau = min(tau_candidates, key=lambda c: abs(float(c[1]) - float(target_tau))/float(target_tau))
best_tau_err = abs(float(best_tau[1]) - float(target_tau)) / float(target_tau) * 100
print(f"  Best candidate: {best_tau[0]} = {float(best_tau[1]):.4f}  (err {best_tau_err:.4f}%)")

# Run null model — but now the integer structure differs
# If best is 39/L: scramble w, integer 39 stays fixed, predict 39/L_scrambled
# If best is 169/L: same idea but integer is 169
# Extract integer from formula name
import re
m = re.match(r"(\d+)", best_tau[0])
if m:
    int_part = int(m.group(1))
    print(f"  Running null model: scramble w, keep integer {int_part} fixed")
    null_errors_tau = []
    for trial in range(N_TRIALS):
        multiplier = random.uniform(0.1, 10.0)
        w_scrambled = float(w) * multiplier
        L_scrambled = w_scrambled / 13.0
        pred = int_part / L_scrambled
        err = abs(pred - float(target_tau)) / float(target_tau) * 100
        null_errors_tau.append(err)
    null_errors_tau.sort()
    hits_at_real_tau = sum(1 for e in null_errors_tau if e <= best_tau_err)
    print(f"  Real substrate error: {best_tau_err:.4f}%")
    print(f"  Null min: {null_errors_tau[0]:.4f}%   p10: {null_errors_tau[N_TRIALS//10]:.4f}%   "
          f"p50: {null_errors_tau[N_TRIALS//2]:.4f}%   p90: {null_errors_tau[9*N_TRIALS//10]:.4f}%")
    print(f"  Trials with err ≤ real: {hits_at_real_tau}/{N_TRIALS} = {hits_at_real_tau/N_TRIALS*100:.2f}%")

# ─────────────────────────────────────────────────────────────────────────────
# SAVE
# ─────────────────────────────────────────────────────────────────────────────
out = {
    "targets": {k: float(v) for k, v in TARGETS.items()},
    "push1_bug_note": "Push #1 used m_tau/m_e = 347786.21 (100x too large). Correct value is 3477.228280. Push #1's m_tau hit was against the wrong target.",
    "family_predictions_table": [
        {"k": p["k"],
         "13^k/L": float(p["13^k/L"]),
         "3·13^k/L": float(p["3·13^k/L"]),
         "13^k/L_s": float(p["13^k/L_s"])}
        for p in family_predictions
    ],
    "best_matches_per_target": {
        tname: {"formula": m[0], "value": m[1], "target": m[2], "err_pct": m[3]}
        for tname, m in best_matches.items()
    },
    "m_mu_confirm": {
        "formula_13_L": "13/L = 169/w",
        "pred": float(pred_13_L),
        "target": float(target_mu),
        "err_pct": float(err_13_L),
        "atlas_pred": float(pred_atlas),
        "atlas_err_pct": float(err_atlas),
    },
    "null_model_m_mu_13_over_L": {
        "n_trials": N_TRIALS,
        "real_err_pct": real_err,
        "null_min_pct": min_err,
        "null_p10_pct": p10,
        "null_p25_pct": p25,
        "null_p50_pct": p50,
        "null_p75_pct": p75,
        "null_p90_pct": p90,
        "null_p99_pct": p99,
        "null_mean_pct": mean_err,
        "trials_le_real": hits_at_real,
        "false_positive_rate_pct": hits_at_real / N_TRIALS * 100,
        "real_percentile": (N_TRIALS - hits_at_real) / N_TRIALS * 100,
        "verdict": verdict,
    },
    "m_tau_candidates": [
        {"formula": name, "value": float(pred), "err_pct": float(abs(float(pred) - float(target_tau))/float(target_tau)*100)}
        for name, pred in tau_candidates
    ],
    "tau_atlas_pred": float(tau_atlas_ratio),
    "tau_atlas_err_pct": float(err_tau_atlas),
    "implied_k_for_13k_over_L": {
        "m_mu/m_e":  k_for_mu,
        "m_tau/m_e": k_for_tau,
        "m_p/m_e":   k_for_proton,
    },
}
outp = Path("/home/z/my-project/results/nq1_dsink_lepton.json")
with open(outp, "w") as f:
    json.dump(out, f, indent=2, default=str)
print(f"\n[ok] Results saved to {outp}")
