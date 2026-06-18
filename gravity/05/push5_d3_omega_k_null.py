"""
Push #5 D.3 focused null — Ω_k = 24·Y^15·U_e (3.86% error)

The Push #5 D.3 search found a Y^15-scale hit: Ω_k (cosmological curvature
parameter) ≈ 0.0007 is hit by 24·Y^15·U_e = 0.00073 with 3.86% error.

This is the Y^15 bit-inversion partner predicted by Push #4's hypothesis:
Y_inv⁹ (m_τ/m_e, Reality layer) ↔ Y^15 (Potential layer).

If this hit survives a focused null model, the bit-inversion pairing is
VALIDATED as a derived rule — converting Push #4's empirical heuristic
into a structural prediction.
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
U_e = pp.U_e

# Target: Ω_k = 7e-4 (Planck 2018)
target = F(7, 10000)  # 0.0007

# Prediction: 24·Y^15·U_e
pred_real = F(24) * Y**15 * U_e
err_real = abs(pred_real - target) / target * 100

print("=" * 80)
print("Push #5 D.3 Focused Null — Ω_k = 24·Y^15·U_e")
print("=" * 80)
print(f"\n  Target Ω_k = {float(target):.6e}")
print(f"  Prediction 24·Y^15·U_e = {float(pred_real):.6e}")
print(f"  Real error = {float(err_real):.4f}%")

# ─────────────────────────────────────────────────────────────────────────────
# Focused null: scramble Y, hold 24, 15, U_e fixed
# ─────────────────────────────────────────────────────────────────────────────
print("\n" + "=" * 80)
print("Focused null model: scramble Y, hold 24, 15, U_e fixed")
print("=" * 80)
print(f"  5000 trials; Y' = Y × uniform(0.1, 10); compute 24·Y'^15·U_e\n")

random.seed(50505)
N_TRIALS = 5000
null_errs = []
for trial in range(N_TRIALS):
    mult = random.uniform(0.1, 10.0)
    Y_s = float(Y) * mult
    pred = 24.0 * Y_s**15 * float(U_e)
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
    verdict = "SURPRISING — Ω_k = 24·Y^15·U_e is the THIRD statistically surprising formula"
elif fp_rate < 20:
    verdict = "MARGINALLY SURPRISING"
else:
    verdict = "NOT surprising"
print(f"\n  VERDICT: {verdict}")

# ─────────────────────────────────────────────────────────────────────────────
# Compare to the two known surprising formulas
# ─────────────────────────────────────────────────────────────────────────────
print("\n" + "=" * 80)
print("Comparison to the two known surprising formulas")
print("=" * 80)
print(f"\n  13/L for m_μ/m_e:        0.0294% err, 0% FP over 5000 trials (Push #2)")
print(f"  24·Y⁴ for α_s:           0.19% err,  0% FP over 5000 trials (Push #4)")
print(f"  24·Y^15·U_e for Ω_k:    {float(err_real):.4f}% err, {fp_rate:.2f}% FP over {N_TRIALS} trials (Push #5)")

# Save
outp = Path("/home/z/my-project/results/push5_d3_omega_k_null.json")
with open(outp, "w") as f:
    json.dump({
        "target": float(target),
        "prediction": float(pred_real),
        "formula": "24·Y^15·U_e",
        "real_err_pct": float(err_real),
        "focused_null_model": {
            "n_trials": N_TRIALS,
            "scrambling": "Y' = Y × uniform(0.1, 10)",
            "integers_held_fixed": [24, 15],
            "U_e_held_fixed": True,
            "null_min_pct": null_errs[0],
            "null_p10_pct": null_errs[N_TRIALS//10],
            "null_p25_pct": null_errs[N_TRIALS//4],
            "null_p50_pct": null_errs[N_TRIALS//2],
            "null_p75_pct": null_errs[3*N_TRIALS//4],
            "null_p90_pct": null_errs[9*N_TRIALS//10],
            "null_p99_pct": null_errs[99*N_TRIALS//100],
            "null_max_pct": null_errs[-1],
            "null_mean_pct": sum(null_errs)/N_TRIALS,
            "hits_at_real": hits_at_real,
            "false_positive_rate_pct": fp_rate,
            "real_percentile": real_percentile,
            "verdict": verdict,
        },
        "comparison_to_other_surprising_formulas": {
            "13_L_for_m_mu_over_m_e": {"err_pct": 0.0294, "fp_rate_pct": 0.0, "push": "Push #2"},
            "24_Y4_for_alpha_s": {"err_pct": 0.19, "fp_rate_pct": 0.0, "push": "Push #4"},
            "24_Y15_Ue_for_omega_k": {"err_pct": float(err_real), "fp_rate_pct": fp_rate, "push": "Push #5"},
        },
        "bit_inversion_pairing_status": "VALIDATED" if fp_rate < 5 else "PARTIALLY VALIDATED" if fp_rate < 20 else "FALSIFIED",
    }, f, indent=2, default=str)
print(f"\n[ok] Results saved to {outp}")
