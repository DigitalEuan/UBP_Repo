"""
DIRECTION 1 (D.1) — Second-Generation Mass Scale Test.

HYPOTHESIS
----------
If 13/L = 13²/w = D-Sink²/Wobble is the structural mass scale for second-
generation leptons (muon), then the same skeleton should apply to second-
generation QUARKS:

    Charm quark:   m_c ≈ 1275 MeV       →  m_c/m_e ≈ 2495.16
    Strange quark: m_s ≈ 95 MeV (MS-bar) →  m_s/m_e ≈ 185.91

We test the EXACT 13/L family (no random search):
    13^k / L      for k = 0..5
    3·13^k / L    for k = 0..5   (Triad variant)
    13^k / L_s    for k = 0..5   (Spectroscopic Sink variant)
    13^k / w      for k = 0..5   (direct Wobble variant — equivalent to 13^(k+1)/L)

Total: 24 candidates per target. NO Y-powers, NO π/φ/e, NO arbitrary multipliers.
This is the narrowest possible grammar.

We also run a focused null model: for each candidate that hits, scramble w
and count false-positive rate.

We test against m_μ/m_e (control — should reproduce 13/L hit) and the two
new second-generation quark masses.
"""
from __future__ import annotations
import json, sys, random
from fractions import Fraction
from pathlib import Path

sys.path.insert(0, "/home/z/my-project/scripts")
import ubp_unified_v5 as u

F = Fraction

pp = u.PARTICLE_PHYSICS
L = pp.L
w = pp.wobble
L_s = pp.L_s
Y = pp.Y

# ─────────────────────────────────────────────────────────────────────────────
# TARGETS
# ─────────────────────────────────────────────────────────────────────────────
# All masses in MeV/c²; ratios dimensionless
m_e_MeV   = F(51099895, 100000000)       # 0.51099895 MeV (CODATA 2022)
m_mu_MeV  = F(1056583745, 10000000)      # 105.6583745 MeV (PDG 2024)
m_tau_MeV = F(1776861, 1000)             # 1776.861 MeV (PDG 2024)
# Quark masses — PDG 2024 MS-bar values
m_c_MeV   = F(1275, 1)                   # 1275 ± 25 MeV (MS-bar, μ = m_c)
m_s_MeV   = F(95, 1)                     # 95 ± 5 MeV (MS-bar, μ = 2 GeV) -- some sources say 93.4
# Use the more common PDG value 93.4 MeV for strange
m_s_MeV   = F(934, 10)                   # 93.4 MeV (PDG 2024 MS-bar)

TARGETS = {
    "m_mu/m_e  (CONTROL — should hit 13/L)":  m_mu_MeV  / m_e_MeV,    # ≈ 206.768
    "m_c/m_e   (Charm quark, 2nd gen)":       m_c_MeV   / m_e_MeV,    # ≈ 2495.16
    "m_s/m_e   (Strange quark, 2nd gen)":     m_s_MeV   / m_e_MeV,    # ≈ 182.78
    "m_tau/m_e (3rd gen — control, should NOT hit)": m_tau_MeV / m_e_MeV,  # ≈ 3477.23
}

print("=" * 80)
print("DIRECTION 1 — Second-Generation Mass Scale Test")
print("=" * 80)
print("\nTargets (all dimensionless mass ratios to m_e):")
for name, val in TARGETS.items():
    print(f"  {name:<55} = {float(val):.6f}")

# ─────────────────────────────────────────────────────────────────────────────
# NARROW GRAMMAR — only the 13/L family
# ─────────────────────────────────────────────────────────────────────────────
def build_candidates():
    cands = []
    for k in range(0, 6):
        # 13^k / L  =  13^(k+1) / w
        cands.append((f"13^{k}/L  =  13^{k+1}/w",  F(13)**k / L))
        # 3·13^k / L  (Triad variant)
        cands.append((f"3·13^{k}/L",                F(3) * F(13)**k / L))
        # 13^k / L_s  (Spectroscopic Sink variant)
        cands.append((f"13^{k}/L_s",                F(13)**k / L_s))
        # 13^k / w  (direct Wobble — same as 13^(k+1)/L, but listed for clarity)
        # skip duplicate
    return cands

candidates = build_candidates()
print(f"\nNarrow grammar: {len(candidates)} candidates per target (no Y-powers, no π/φ/e, no arbitrary multipliers)")

# ─────────────────────────────────────────────────────────────────────────────
# TEST EACH TARGET
# ─────────────────────────────────────────────────────────────────────────────
results = {}
for tname, tval in TARGETS.items():
    print(f"\n--- {tname} ---")
    print(f"    target = {float(tval):.6f}")
    scored = []
    for name, pred in candidates:
        if pred > 0:
            err = abs(float(pred) - float(tval)) / float(tval) * 100
            scored.append((name, float(pred), err))
    scored.sort(key=lambda x: x[2])
    print(f"    {'Formula':<35} {'Value':<14} {'Error %':<10}")
    print(f"    {'-'*35} {'-'*14} {'-'*10}")
    for name, val, err in scored[:8]:  # top 8
        marker = "  <-- HIT" if err < 1.0 else ""
        print(f"    {name:<35} {val:<14.4f} {err:<10.4f}{marker}")
    results[tname] = {
        "target": float(tval),
        "top_candidates": [
            {"formula": name, "value": val, "err_pct": err}
            for name, val, err in scored[:8]
        ],
        "best_err_pct": scored[0][2] if scored else None,
        "best_formula": scored[0][0] if scored else None,
        "n_sub_1pct": sum(1 for _, _, e in scored if e < 1.0),
        "n_sub_013pct": sum(1 for _, _, e in scored if e < 0.13),
    }

# ─────────────────────────────────────────────────────────────────────────────
# FOCUSED NULL MODEL — for any sub-1% hit, run 5000-trial w-scramble
# ─────────────────────────────────────────────────────────────────────────────
print("\n" + "=" * 80)
print("Focused null model on sub-1% hits (5000 trials, scramble w only)")
print("=" * 80)

random.seed(424242)
N_TRIALS = 5000

null_results = {}
for tname, tdata in results.items():
    if tdata["n_sub_1pct"] == 0:
        print(f"\n{tname}: no sub-1% hits, skipping null model")
        continue
    print(f"\n{tname}: testing {tdata['n_sub_1pct']} sub-1% candidate(s)")
    # Test the best candidate
    best_formula = tdata["best_formula"]
    best_err = tdata["best_err_pct"]
    print(f"  Best formula: {best_formula}  (err {best_err:.4f}%)")

    # Extract the integer k from the formula and the family type
    # Formulas are like "13^1/L  =  13^2/w" or "3·13^1/L" or "13^1/L_s"
    # We need to know what to compute under scrambled w
    # All variants reduce to (integer_coefficient) / w under w-scrambling:
    #   13^k/L = 13^(k+1)/w
    #   3·13^k/L = 3·13^(k+1)/w
    #   13^k/L_s = 13^k / (29w/312) = 312·13^k / (29·w) = (312/29)·13^k / w
    import re
    m = re.search(r"13\^(\d+)/L_s", best_formula)
    if m:
        k = int(m.group(1))
        coeff = F(312, 29) * F(13)**k
        family = "L_s"
    else:
        m = re.search(r"3·13\^(\d+)/L", best_formula)
        if m:
            k = int(m.group(1))
            coeff = F(3) * F(13)**(k+1)
            family = "Triad"
        else:
            m = re.search(r"13\^(\d+)/L", best_formula)
            if m:
                k = int(m.group(1))
                coeff = F(13)**(k+1)
                family = "L"
            else:
                print(f"    could not parse formula: {best_formula}")
                continue

    print(f"  Under w-scrambling: formula reduces to {float(coeff):.4f} / w_scrambled")
    print(f"  Family: {family}, k = {k}")

    target_val = TARGETS[tname]
    null_errs = []
    for trial in range(N_TRIALS):
        multiplier = random.uniform(0.1, 10.0)
        w_scrambled = float(w) * multiplier
        pred = float(coeff) / w_scrambled
        err = abs(pred - float(target_val)) / float(target_val) * 100
        null_errs.append(err)
    null_errs.sort()
    hits_at_real = sum(1 for e in null_errs if e <= best_err)
    fp_rate = hits_at_real / N_TRIALS * 100
    real_percentile = (N_TRIALS - hits_at_real) / N_TRIALS * 100

    print(f"  Real substrate error: {best_err:.4f}%")
    print(f"  Null min: {null_errs[0]:.4f}%   p10: {null_errs[N_TRIALS//10]:.4f}%   "
          f"p50: {null_errs[N_TRIALS//2]:.4f}%   p90: {null_errs[9*N_TRIALS//10]:.4f}%   "
          f"max: {null_errs[-1]:.4f}%")
    print(f"  Trials with err ≤ real: {hits_at_real}/{N_TRIALS} = {fp_rate:.2f}%")
    print(f"  Real substrate percentile: {real_percentile:.2f}%  (100% = best possible)")

    if fp_rate < 5:
        verdict = "SURPRISING (< 5% null hit rate)"
    elif fp_rate < 20:
        verdict = "MARGINALLY SURPRISING (5-20%)"
    else:
        verdict = "NOT surprising (≥ 20%)"
    print(f"  VERDICT: {verdict}")

    null_results[tname] = {
        "best_formula": best_formula,
        "best_err_pct": best_err,
        "family": family,
        "k": k,
        "coefficient": float(coeff),
        "n_trials": N_TRIALS,
        "null_min_pct": null_errs[0],
        "null_p10_pct": null_errs[N_TRIALS//10],
        "null_p50_pct": null_errs[N_TRIALS//2],
        "null_p90_pct": null_errs[9*N_TRIALS//10],
        "null_max_pct": null_errs[-1],
        "null_mean_pct": sum(null_errs)/len(null_errs),
        "hits_at_real": hits_at_real,
        "false_positive_rate_pct": fp_rate,
        "real_percentile": real_percentile,
        "verdict": verdict,
    }

# ─────────────────────────────────────────────────────────────────────────────
# GENERALISATION SUMMARY
# ─────────────────────────────────────────────────────────────────────────────
print("\n" + "=" * 80)
print("GENERALISATION SUMMARY — second-generation fermions")
print("=" * 80)
print(f"\n{'Target':<35} {'Best formula':<30} {'Best err %':<12} {'Verdict':<30}")
print("-" * 110)
for tname, tdata in results.items():
    best_f = tdata["best_formula"] or "—"
    best_e = tdata["best_err_pct"]
    if best_e is None:
        verdict = "—"
    elif tname in null_results:
        verdict = null_results[tname]["verdict"]
    elif best_e < 1.0:
        verdict = "(null not run)"
    else:
        verdict = "no sub-1% hit"
    print(f"{tname:<35} {best_f:<30} {best_e:<12.4f} {verdict:<30}")

# Save
outp = Path("/home/z/my-project/results/dir1_second_gen_quarks.json")
with open(outp, "w") as f:
    json.dump({
        "targets": {k: float(v) for k, v in TARGETS.items()},
        "candidates": [{"formula": n, "value": float(v)} for n, v in candidates],
        "results": results,
        "null_model": null_results,
    }, f, indent=2, default=str)
print(f"\n[ok] Results saved to {outp}")
