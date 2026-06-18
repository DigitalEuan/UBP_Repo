"""
Push #5 D.2 focused null — m_W = 13/L · 24·Y⁴ · π (4.85% error)

The Push #5 D.2 out-of-sample search found that the W boson mass (80.379 GeV)
is hit by 13/L · 24·Y⁴ · π = 76.48 GeV with 4.85% error.

This is a combined formula using BOTH surprising formulas (13/L for m_μ/m_e
and 24·Y⁴ for α_s). If it survives the focused null, it would be a strong
validation that the two formulas are physically meaningful, not just
statistically surprising in isolation.
"""
from __future__ import annotations
import json, sys, random
from fractions import Fraction
from pathlib import Path

sys.path.insert(0, "/home/z/my-project/scripts")
import ubp_unified_v5 as u

F = Fraction

pp = u.PARTICLE_PHYSICS
Y = pp.Y
L = pp.L
w = pp.wobble
pi = pp.pi

# Target: m_W = 80.379 GeV
target = F(80379, 1000)

# Prediction: 13/L · 24·Y⁴ · π
pred_real = F(13) / L * F(24) * Y**4 * pi
err_real = abs(pred_real - target) / target * 100

print("=" * 80)
print("Push #5 D.2 Focused Null — m_W = 13/L · 24·Y⁴ · π")
print("=" * 80)
print(f"\n  Target m_W = {float(target):.6f} GeV")
print(f"  Prediction (13/L)·(24·Y⁴)·π = {float(pred_real):.6f} GeV")
print(f"  Real error = {float(err_real):.4f}%")

# ─────────────────────────────────────────────────────────────────────────────
# Focused null: scramble Y and w (hence L = w/13), hold 13, 24, 4, π fixed
# ─────────────────────────────────────────────────────────────────────────────
print("\n" + "=" * 80)
print("Focused null: scramble Y AND w (both substrate-dependent)")
print("=" * 80)
print(f"  5000 trials; Y' = Y × uniform(0.1, 10), w' = w × uniform(0.1, 10)")
print(f"  Compute (13/L')·(24·Y'⁴)·π = (13·13/w')·(24·Y'⁴)·π = 169·24·Y'⁴·π/w'\n")

random.seed(50512)
N_TRIALS = 5000
null_errs = []
for trial in range(N_TRIALS):
    Y_mult = random.uniform(0.1, 10.0)
    w_mult = random.uniform(0.1, 10.0)
    Y_s = float(Y) * Y_mult
    w_s = float(w) * w_mult
    L_s = w_s / 13.0
    pred = (13.0 / L_s) * (24.0 * Y_s**4) * float(pi)
    err = abs(pred - float(target)) / float(target) * 100
    null_errs.append(err)

null_errs.sort()
hits_at_real = sum(1 for e in null_errs if e <= float(err_real))
fp_rate = hits_at_real / N_TRIALS * 100
real_percentile = (N_TRIALS - hits_at_real) / N_TRIALS * 100

print(f"  Real substrate error: {float(err_real):.4f}%")
print(f"  Null distribution ({N_TRIALS} trials):")
print(f"    min:    {null_errs[0]:.4f}%")
print(f"    p10:    {null_errs[N_TRIALS//10]:.4f}%")
print(f"    p25:    {null_errs[N_TRIALS//4]:.4f}%")
print(f"    p50:    {null_errs[N_TRIALS//2]:.4f}%")
print(f"    p75:    {null_errs[3*N_TRIALS//4]:.4f}%")
print(f"    p90:    {null_errs[9*N_TRIALS//10]:.4f}%")
print(f"    p99:    {null_errs[99*N_TRIALS//100]:.4f}%")
print(f"    max:    {null_errs[-1]:.4f}%")
print(f"    mean:   {sum(null_errs)/N_TRIALS:.4f}%")
print(f"  Trials with err ≤ real err: {hits_at_real}/{N_TRIALS} = {fp_rate:.2f}%")
print(f"  Real substrate's percentile: {real_percentile:.2f}%")

if fp_rate < 5:
    verdict = "SURPRISING — combined 13/L · 24·Y⁴ · π for m_W is statistically surprising"
elif fp_rate < 20:
    verdict = "MARGINALLY SURPRISING"
else:
    verdict = "NOT surprising — combined formula is grammar permissiveness"
print(f"\n  VERDICT: {verdict}")

# Also run focused null scrambling only Y (keeping w fixed)
print("\n" + "=" * 80)
print("Alternative: scramble Y only (keep w fixed)")
print("=" * 80)
random.seed(50513)
null_errs_y_only = []
for trial in range(N_TRIALS):
    Y_mult = random.uniform(0.1, 10.0)
    Y_s = float(Y) * Y_mult
    pred = (13.0 / float(L)) * (24.0 * Y_s**4) * float(pi)
    err = abs(pred - float(target)) / float(target) * 100
    null_errs_y_only.append(err)
null_errs_y_only.sort()
hits_y = sum(1 for e in null_errs_y_only if e <= float(err_real))
fp_y = hits_y / N_TRIALS * 100
print(f"  Real error: {float(err_real):.4f}%")
print(f"  Null min: {null_errs_y_only[0]:.4f}%  p50: {null_errs_y_only[N_TRIALS//2]:.4f}%")
print(f"  FP rate (Y only): {fp_y:.2f}% ({hits_y}/{N_TRIALS})")
print(f"  Verdict: {'SURPRISING' if fp_y < 5 else 'MARGINALLY' if fp_y < 20 else 'NOT surprising'}")

# And scrambling only w (keeping Y fixed)
print("\n" + "=" * 80)
print("Alternative: scramble w only (keep Y fixed)")
print("=" * 80)
random.seed(50514)
null_errs_w_only = []
for trial in range(N_TRIALS):
    w_mult = random.uniform(0.1, 10.0)
    w_s = float(w) * w_mult
    L_s = w_s / 13.0
    pred = (13.0 / L_s) * (24.0 * float(Y)**4) * float(pi)
    err = abs(pred - float(target)) / float(target) * 100
    null_errs_w_only.append(err)
null_errs_w_only.sort()
hits_w = sum(1 for e in null_errs_w_only if e <= float(err_real))
fp_w = hits_w / N_TRIALS * 100
print(f"  Real error: {float(err_real):.4f}%")
print(f"  Null min: {null_errs_w_only[0]:.4f}%  p50: {null_errs_w_only[N_TRIALS//2]:.4f}%")
print(f"  FP rate (w only): {fp_w:.2f}% ({hits_w}/{N_TRIALS})")
print(f"  Verdict: {'SURPRISING' if fp_w < 5 else 'MARGINALLY' if fp_w < 20 else 'NOT surprising'}")

# Save
outp = Path("/home/z/my-project/results/push5_d2_mW_null.json")
with open(outp, "w") as f:
    json.dump({
        "target_mW_GeV": float(target),
        "prediction": float(pred_real),
        "formula": "(13/L)·(24·Y⁴)·π",
        "real_err_pct": float(err_real),
        "focused_null_scramble_both": {
            "n_trials": N_TRIALS,
            "scrambling": "Y' = Y × uniform(0.1, 10), w' = w × uniform(0.1, 10)",
            "null_min_pct": null_errs[0],
            "null_p50_pct": null_errs[N_TRIALS//2],
            "null_max_pct": null_errs[-1],
            "hits_at_real": hits_at_real,
            "fp_rate_pct": fp_rate,
            "verdict": verdict,
        },
        "focused_null_scramble_Y_only": {
            "n_trials": N_TRIALS,
            "fp_rate_pct": fp_y,
            "null_min_pct": null_errs_y_only[0],
            "verdict": "SURPRISING" if fp_y < 5 else "MARGINALLY" if fp_y < 20 else "NOT surprising",
        },
        "focused_null_scramble_w_only": {
            "n_trials": N_TRIALS,
            "fp_rate_pct": fp_w,
            "null_min_pct": null_errs_w_only[0],
            "verdict": "SURPRISING" if fp_w < 5 else "MARGINALLY" if fp_w < 20 else "NOT surprising",
        },
    }, f, indent=2, default=str)
print(f"\n[ok] Results saved to {outp}")
