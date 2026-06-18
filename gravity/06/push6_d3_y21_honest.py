"""
Push #6 D.3 — Focused null on m_ν/m_P = 3·Y^21·Y (0.3058% error).

The Y^21 hunt found a real (non-tautological) hit:
  m_ν/m_P ≈ 6.0e-13  (sum of neutrino masses ~0.06 eV / Planck mass 1.22e28 eV)
  3·Y^21·Y = 3·Y^22 = 6.0e-13  (0.3058% error)

This is the Y^21 bit-inversion partner of α⁻¹'s Y_inv³, validating the
bit-inversion pairing rule for the 3rd time.

If it survives the focused null, it becomes the 5th statistically surprising
formula.
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
pi = pp.pi

# Target: m_ν/m_P
# m_ν ≈ 0.06 eV (sum of neutrino masses, Planck 2018 constraint)
# m_P = 1.2209e19 GeV = 1.2209e28 eV
# m_ν/m_P = 0.06 / 1.2209e28 ≈ 4.9e-30
# But Push #6 used 6e-13 — let me re-check what target was used

# Actually looking at the script: F(6, 10**13) = 6e-13
# This was meant to be 0.06 eV / 1e19 GeV = 0.06 / (1e19 * 1e9) = 0.06 / 1e28 = 6e-30
# So the target 6e-13 in the script was WRONG. Let me use the correct value.

# m_ν/m_P = 0.06 eV / 1.2209e28 eV = 4.913e-30
# But 3·Y^22 = 3·Y^21·Y = 3 * 7.53e-13 * 0.2647 = 5.98e-13
# So the formula gives 6e-13, not 5e-30. The "hit" was against the wrong target.

# Let me check what the actual ratio should be:
m_nu_eV = 0.06  # eV (sum of neutrino masses, Planck 2018 upper limit ~0.12, central ~0.06)
m_P_eV = 1.2209e28  # eV (Planck mass)
m_nu_over_m_P = m_nu_eV / m_P_eV
print(f"Correct m_ν/m_P = {m_nu_over_m_P:.4e}")
print(f"3·Y^22 = {float(3 * Y**22):.4e}")
print(f"These are NOT close — the Push #6 'hit' was against a wrong target value.")

# So the m_ν/m_P "hit" is also a bug, like Push #1's m_τ/m_e bug.
# Let me search for the actual Y^21-scale constant more carefully.

# 3·Y^22 = 5.98e-13. What physical constant is at this scale?
# - Λ (cosmological constant) in SI: 1.1e-52 s⁻² — wrong units
# - Λ in m⁻²: 1.1e-52 / (3e8)² = 1.2e-69 m⁻² — wrong
# - Some dimensionless CMB ratio?

# Let me check: 5.98e-13 is approximately 6e-13. Known constants at this scale:
# - Electron-to-Planck-mass ratio: m_e/m_P = 0.511 MeV / 1.22e19 GeV = 4.2e-23 (wrong)
# - Some cosmological density parameter?

# Actually, what if the formula 3·Y^22 corresponds to a different physical quantity?
# 3·Y^22 ≈ 6e-13. Let me check known dimensionless quantities:
# - Dark energy density / critical density × (some factor)?

# Let me just be honest: the Y^21 hunt did NOT find a clear partner.
# The "hits" were either tautological (24·Y^21·U_e predicting itself) or buggy
# (m_ν/m_P using wrong target value).

# Let me do a clean re-test of m_ν/m_P with the correct target:
target_correct = F(6, 10**30)  # 6e-30 (correct m_ν/m_P)
pred = F(3) * Y**22
err = abs(float(pred) - float(target_correct)) / float(target_correct) * 100
print(f"\nWith CORRECT target m_ν/m_P = 6e-30:")
print(f"  3·Y^22 = {float(pred):.4e}")
print(f"  Error: {err:.2f}%  (NOT a hit)")

# So the Y^21 hunt is INCONCLUSIVE. Let me run the focused null on the
# tautological "24·Y^21·U_e" hit anyway — even though the prediction is
# tautological, the focused null tells us whether the formula's STRUCTURE
# is surprising (i.e., whether random Y values would also produce values
# close to 24·Y^21·U_e).

# Actually, the focused null on a tautological prediction doesn't make sense.
# The real test is whether 24·Y^21·U_e matches some PHYSICAL constant.
# Let me check: is 24·Y^21·U_e ≈ 2.5e-7 close to any known constant?

val_24_Y21_Ue = float(F(24) * Y**21 * U_e)
print(f"\n24·Y^21·U_e = {val_24_Y21_Ue:.4e}")
# 2.5e-7 — known constants at this scale:
# - α_G (gravitational coupling) = 5.7e-39 (way smaller)
# - G in natural units? 
# - Some neutrino-related ratio?
# - Electron-to-Higgs-VEV ratio: m_e/v = 0.511 MeV / 246 GeV = 2.08e-6 (close-ish, factor ~8)
# - m_e/m_Higgs = 0.511 MeV / 125250 MeV = 4.08e-6 (factor ~16)

# Actually 2.5e-7 is the approximate value of:
# - (m_e/m_Higgs)²/2 ≈ (4.08e-6)²/2 ≈ 8.3e-12 (wrong)
# - Some Yukawa coupling squared?

# Let me test 24·Y^21·U_e against electron Yukawa coupling:
# y_e = m_e/v = 0.511 MeV / 246 GeV = 2.08e-6
# y_e² = 4.3e-12
# 24·Y^21·U_e = 2.5e-7 — doesn't match y_e or y_e²

# What about the electron Yukawa × some factor?
y_e = F(51099895, 100000000) / F(246000, 1)  # m_e (MeV) / v (MeV)
y_e_val = float(y_e)
print(f"\ny_e = m_e/v = {y_e_val:.4e}")
print(f"24·Y^21·U_e / y_e = {val_24_Y21_Ue / y_e_val:.4f}")
print(f"24·Y^21·U_e / y_e² = {val_24_Y21_Ue / y_e_val**2:.4e}")

# Hmm, 24·Y^21·U_e / y_e² ≈ 5.8e4 — not a clean integer.
# What about 24·Y^21·U_e × y_e = ?
print(f"24·Y^21·U_e × y_e = {val_24_Y21_Ue * y_e_val:.4e}")
# 5.2e-13 — close to Y^21 scale (7.5e-13) but not exact.

# Let me check the NRCI-corrected version:
val_24_Y21_Ue_nrci = float(F(24) * Y**21 * U_e * (F(10)/(F(10)+F(1,8)*3.117)))
print(f"\n24·Y^21·U_e × NRCI(1/8) = {val_24_Y21_Ue_nrci:.4e}")
# Should be ~2.4e-7

# I'll just report the inconclusive result honestly.

# ─────────────────────────────────────────────────────────────────────────────
# Honest focused null on the strongest candidate (even if imperfect)
# ─────────────────────────────────────────────────────────────────────────────
# The best non-tautological candidate from the Y^21 hunt was n_γ/n_b (photon-to-baryon ratio)
# at 5.1% error with formula 1/4·Y^21·U_e·NRCI(2). Let me run a focused null on this.

print("\n" + "=" * 80)
print("Focused null on n_γ/n_b = 1/4·Y^21·U_e·NRCI(2)  (5.1% error)")
print("=" * 80)

target = F(169, 10**11)  # 1.69e-9 (photon-to-baryon ratio, Planck 2018)
pred_real = F(1, 4) * Y**21 * U_e * (F(10) / (F(10) + F(2) * 3.117))
err_real = abs(float(pred_real) - float(target)) / float(target) * 100

print(f"  Target n_γ/n_b = {float(target):.4e}")
print(f"  Prediction = {float(pred_real):.4e}")
print(f"  Real error = {err_real:.4f}%")

random.seed(60606)
N_TRIALS = 5000
null_errs = []
for trial in range(N_TRIALS):
    Y_mult = random.uniform(0.1, 10.0)
    Y_s = float(Y) * Y_mult
    Y21_s = Y_s ** 21
    # Recompute NRCI with scrambled Y
    tax_s = 8 * Y_s + 1  # canonical octad tax with scrambled Y
    nrci_s = 10.0 / (10.0 + 2.0 * tax_s)
    pred = 0.25 * Y21_s * float(U_e) * nrci_s
    err = abs(pred - float(target)) / float(target) * 100
    null_errs.append(err)

null_errs.sort()
hits = sum(1 for e in null_errs if e <= err_real)
fp_rate = hits / N_TRIALS * 100
print(f"\n  Null distribution ({N_TRIALS} trials):")
print(f"    min: {null_errs[0]:.4f}%   p10: {null_errs[N_TRIALS//10]:.4f}%   "
      f"p50: {null_errs[N_TRIALS//2]:.4f}%   p90: {null_errs[9*N_TRIALS//10]:.4f}%")
print(f"  Trials with err ≤ real ({err_real:.4f}%): {hits}/{N_TRIALS} = {fp_rate:.2f}%")
if fp_rate < 5:
    verdict = "SURPRISING — n_γ/n_b is the 5th surprising formula"
elif fp_rate < 20:
    verdict = "MARGINALLY SURPRISING"
else:
    verdict = "NOT surprising"
print(f"  VERDICT: {verdict}")

# Save
outp = Path("/home/z/my-project/results/push6_d3_y21_hunt_honest.json")
with open(outp, "w") as f:
    json.dump({
        "y21_value": float(Y**21),
        "y22_value": float(Y**22),
        "val_24_Y21_Ue": val_24_Y21_Ue,
        "val_24_Y21_Ue_nrci": val_24_Y21_Ue_nrci,
        "m_nu_over_m_P_correct": float(target_correct),
        "m_nu_over_m_P_pred_3Y22": float(F(3) * Y**22),
        "m_nu_over_m_P_err_with_correct_target": float(err),
        "n_gamma_over_n_b_focused_null": {
            "target": float(target),
            "pred": float(pred_real),
            "err_pct": float(err_real),
            "n_trials": N_TRIALS,
            "null_min_pct": null_errs[0],
            "null_p50_pct": null_errs[N_TRIALS//2],
            "hits_at_real": hits,
            "fp_rate_pct": fp_rate,
            "verdict": verdict,
        },
        "honest_assessment": "The Y^21 hunt did NOT find a clean partner for α⁻¹'s Y_inv³. The '24·Y^21·U_e' hit was tautological (predicting itself). The 'm_ν/m_P' hit used a wrong target value (6e-13 instead of 6e-30). The strongest non-tautological candidate is n_γ/n_b (photon-to-baryon ratio) at 5.1% error. The focused null on this candidate is reported above. The bit-inversion pairing rule therefore achieves 2 of 4 confirmations (Y_inv⁶↔Y^18, Y_inv⁹↔Y^15), NOT 3. The Y^21 partner remains unconfirmed.",
    }, f, indent=2, default=str)
print(f"\n[ok] Results saved to {outp}")
