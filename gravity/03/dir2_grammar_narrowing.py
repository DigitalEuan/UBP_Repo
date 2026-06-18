"""
DIRECTION 2 (D.2) — Grammar-Narrowing Theory based on UBP Layers.

HYPOTHESIS
----------
The Push #2 structural null showed the broad grammar (10 bases × 2 × 50 scales
× 31 multipliers = 34 100 candidates) is too permissive — false-positive rates
of 23-47% on most targets. We need a UBP-internal rule that narrows the
grammar per target type.

User-proposed mapping (from Push #3 brief):
  • Gravity/Cosmology  →  Potential Layer (bits 18-23)  →  Y^18..Y^23, w
  • Mass Ratios        →  Reality Layer (bits 0-5)      →  L, L_s, U_e
  • Couplings (α)      →  Information Layer (bits 6-11) →  Y^3, π

We instantiate this as THREE narrow grammars and test each on appropriate
targets. If the layer-mapping is real, the narrow grammars should:
  (i) preserve the real substrate's hits on appropriate targets
  (ii) dramatically reduce the structural null's false-positive rate
       (because the narrow grammar has far fewer candidates)

We also extend the mapping by analogy:
  • Activation Layer (bits 12-17)  →  Y^6..Y^11  →  electroweak scale, W/Z bosons
  • Information Layer (bits 6-11)  →  Y^1..Y^5   →  couplings, α, α_s
  • Reality Layer (bits 0-5)       →  L, L_s, U_e, integer ratios  →  masses
  • Potential Layer (bits 18-23)   →  Y^18..Y^23, w, 39/29  →  gravity, cosmology

Narrow grammars:
  G_mass:       bases = {L, L_s, U_e}, scales = {1, 1/U_e, Y^0},
                multipliers = {1, 2, 3, 4, 8, 12, 13, 24, 29, 39, 169, 1/2, 1/3, 1/4, 1/8, 1/12, 1/13, 1/24, 1/29, 1/39, 1/169}
                → 3 bases × 2 × 3 scales × 20 multipliers = 360 candidates
  G_coupling:   bases = {Y, pi}, scales = {Y^1, Y^2, Y^3, Y^4, Y^5, Y^6, 1},
                multipliers = {1, 2, 3, 4, 8, 1/2, 1/3, 1/4, 1/8, 1/24, 24}
                → 2 bases × 2 × 7 scales × 11 multipliers = 308 candidates
  G_gravity:    bases = {Y, w}, scales = {Y^18, Y^19, Y^20, Y^21, Y^22, Y^23, 1},
                multipliers = {1, 2, 3, 4, 8, 12, 24, 29, 39, 1/2, 1/3, 1/4, 1/8, 1/24, 1/29, 1/39, 39/29, 29/24}
                → 2 bases × 2 × 7 scales × 18 multipliers = 504 candidates

Compare to broad grammar: 34 100 candidates. Narrow grammars are ~70-100× smaller.
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

# Sanity check
G_CODATA = F(667430, 10**16)
G_UBP = F(39, 29) * Y**18 / W
print(f"[sanity] G_UBP err = {float(abs(G_UBP - G_CODATA)/G_CODATA*100):.4f}%")

# ─────────────────────────────────────────────────────────────────────────────
# NARROW GRAMMARS PER LAYER
# ─────────────────────────────────────────────────────────────────────────────
SQRT2 = u.ExactMath.sqrt_frac(F(2, 1), prec=30)

GRAMMARS = {
    "G_mass (Reality layer)": {
        "bases": {"L": L, "L_s": L_s, "U_e": U_e},
        "scales": {"1": F(1,1), "1/U_e": F(1, U_e), "Y^0": F(1,1)},
        "multipliers": {
            "1": F(1,1), "2": F(2,1), "3": F(3,1), "4": F(4,1),
            "8": F(8,1), "12": F(12,1), "13": F(13,1), "24": F(24,1),
            "29": F(29,1), "39": F(39,1), "169": F(169,1),
            "1/2": F(1,2), "1/3": F(1,3), "1/4": F(1,4),
            "1/8": F(1,8), "1/12": F(1,12), "1/13": F(1,13),
            "1/24": F(1,24), "1/29": F(1,29), "1/39": F(1,39), "1/169": F(1,169),
        },
    },
    "G_coupling (Information layer)": {
        "bases": {"Y": Y, "pi": PI},
        "scales": {"Y^1": Y, "Y^2": Y**2, "Y^3": Y**3, "Y^4": Y**4, "Y^5": Y**5, "Y^6": Y**6, "1": F(1,1)},
        "multipliers": {
            "1": F(1,1), "2": F(2,1), "3": F(3,1), "4": F(4,1),
            "8": F(8,1), "1/2": F(1,2), "1/3": F(1,3),
            "1/4": F(1,4), "1/8": F(1,8), "1/24": F(1,24), "24": F(24,1),
        },
    },
    "G_gravity (Potential layer)": {
        "bases": {"Y": Y, "w": W},
        "scales": {
            "Y^18": Y**18, "Y^19": Y**19, "Y^20": Y**20,
            "Y^21": Y**21, "Y^22": Y**22, "Y^23": Y**23,
            "1": F(1,1),
        },
        "multipliers": {
            "1": F(1,1), "2": F(2,1), "3": F(3,1), "4": F(4,1),
            "8": F(8,1), "12": F(12,1), "24": F(24,1),
            "29": F(29,1), "39": F(39,1),
            "1/2": F(1,2), "1/3": F(1,3), "1/4": F(1,4),
            "1/8": F(1,8), "1/24": F(1,24),
            "1/29": F(1,29), "1/39": F(1,39),
            "39/29": F(39, 29), "29/24": F(29, 24),
        },
    },
}

# Compute grammar sizes
for name, g in GRAMMARS.items():
    size = len(g["bases"]) * 2 * len(g["scales"]) * len(g["multipliers"])
    print(f"  {name}: {size} candidates  ({len(g['bases'])} bases × 2 × {len(g['scales'])} scales × {len(g['multipliers'])} mults)")

# ─────────────────────────────────────────────────────────────────────────────
# TARGETS PER LAYER
# ─────────────────────────────────────────────────────────────────────────────
LAYER_TARGETS = {
    "G_mass (Reality layer)": {
        "m_mu/m_e":  F(2067682830, 10**7),
        "m_tau/m_e": F(3477228280, 10**6),  # corrected value
        "m_p/m_e":   F(183615267343, 10**8),
        "m_c/m_e":   F(1275, 1) / F(51099895, 100000000),  # 1275 MeV / 0.511 MeV
        "m_s/m_e":   F(934, 10) / F(51099895, 100000000),  # 93.4 MeV / 0.511 MeV
    },
    "G_coupling (Information layer)": {
        "alpha":      F(72973525643, 10**13),
        "alpha_inv":  F(137035999177, 10**9),
        "alpha_s":    F(118, 1000),    # strong coupling at M_Z ≈ 0.118
    },
    "G_gravity (Potential layer)": {
        "G":          F(667430, 10**16),
        "H0_midpoint": F((6736+7304), 200),  # 70.20 km/s/Mpc
    },
}

# ─────────────────────────────────────────────────────────────────────────────
# RUN NARROW GRAMMARS
# ─────────────────────────────────────────────────────────────────────────────
def run_grammar(grammar: dict, target_value: Fraction, top_k: int = 5):
    candidates = []
    for bn, bv in grammar["bases"].items():
        for sn, sv in grammar["scales"].items():
            for mn, mv in grammar["multipliers"].items():
                for fwd in (True, False):
                    try:
                        b = bv if fwd else (F(1)/bv if bv != 0 else None)
                        if b is None: continue
                        val = mv * b * sv
                        if val > 0:
                            err = abs(val - target_value) / target_value * 100
                            candidates.append({
                                "formula": f"{mn}{'*' if fwd else '/'}{bn}*{sn}",
                                "value": float(val),
                                "err_pct": float(err),
                            })
                    except: pass
    candidates.sort(key=lambda c: c["err_pct"])
    return {
        "n_candidates": len(candidates),
        "best_err_pct": candidates[0]["err_pct"] if candidates else None,
        "best_formula": candidates[0]["formula"] if candidates else None,
        "top_k": candidates[:top_k],
        "band_counts": {
            "le_0.01pct": sum(1 for c in candidates if c["err_pct"] <= 0.01),
            "le_0.05pct": sum(1 for c in candidates if c["err_pct"] <= 0.05),
            "le_0.13pct": sum(1 for c in candidates if c["err_pct"] <= 0.13),
            "le_0.50pct": sum(1 for c in candidates if c["err_pct"] <= 0.50),
            "le_1.00pct": sum(1 for c in candidates if c["err_pct"] <= 1.00),
            "le_5.00pct": sum(1 for c in candidates if c["err_pct"] <= 5.00),
        },
    }

print("\n" + "=" * 80)
print("Narrow-grammar results per layer")
print("=" * 80)
narrow_results = {}
for grammar_name, grammar in GRAMMARS.items():
    print(f"\n--- {grammar_name} ---")
    narrow_results[grammar_name] = {}
    for tname, tval in LAYER_TARGETS[grammar_name].items():
        r = run_grammar(grammar, tval)
        narrow_results[grammar_name][tname] = r
        print(f"  {tname:<14}  best = {r['best_err_pct']:.4f}%  ({r['best_formula']})  band≤0.13%: {r['band_counts']['le_0.13pct']}")

# ─────────────────────────────────────────────────────────────────────────────
# STRUCTURAL NULL ON NARROW GRAMMARS — does narrowing reduce false-positive rate?
# ─────────────────────────────────────────────────────────────────────────────
print("\n" + "=" * 80)
print("Structural null on narrow grammars (20 trials per target)")
print("=" * 80)
print("If the layer-mapping is real, narrow grammars should preserve real hits")
print("while dramatically reducing false-positive rates vs the broad grammar.\n")

random.seed(31415)
N_TRIALS = 20

null_narrow = {}
t_start = time.time()
for grammar_name, grammar in GRAMMARS.items():
    null_narrow[grammar_name] = {}
    for tname, tval in LAYER_TARGETS[grammar_name].items():
        real_best = narrow_results[grammar_name][tname]["best_err_pct"]
        hits = 0
        best_errs = []
        for trial in range(N_TRIALS):
            # Scramble each base by uniform(0.1, 10)
            bases_scrambled = {}
            for bk, bv in grammar["bases"].items():
                mult = random.uniform(0.1, 10.0)
                bases_scrambled[bk] = F(float(bv) * mult).limit_denominator(10**5)
            scrambled_grammar = {**grammar, "bases": bases_scrambled}
            r = run_grammar(scrambled_grammar, tval)
            if r["best_err_pct"] is not None:
                best_errs.append(r["best_err_pct"])
                if r["best_err_pct"] <= 0.13:
                    hits += 1
        null_narrow[grammar_name][tname] = {
            "real_best_pct": real_best,
            "null_min_pct": min(best_errs) if best_errs else None,
            "null_mean_pct": sum(best_errs)/len(best_errs) if best_errs else None,
            "hits_013": hits,
            "n_trials": N_TRIALS,
            "hit_rate_pct": hits / N_TRIALS * 100,
        }

print(f"  Total time: {time.time() - t_start:.1f}s\n")
print(f"{'Grammar':<32} {'Target':<14} {'Real best %':<14} {'Null min %':<14} {'Null hit ≤0.13%':>18}")
print("-" * 95)
for grammar_name in GRAMMARS:
    for tname in LAYER_TARGETS[grammar_name]:
        n = null_narrow[grammar_name][tname]
        print(f"{grammar_name:<32} {tname:<14} {n['real_best_pct']:<14.4f} "
              f"{n['null_min_pct']:<14.4f} {n['hits_013']:>10}/{N_TRIALS:<7}")

# ─────────────────────────────────────────────────────────────────────────────
# COMPARE TO BROAD GRAMMAR (Push #2 structural null rates)
# ─────────────────────────────────────────────────────────────────────────────
print("\n" + "=" * 80)
print("Comparison: narrow grammar vs broad grammar false-positive rates")
print("=" * 80)
# Push #2 structural null results (from nq2_structural_null.json)
broad_null = {
    "G":          6.7,
    "alpha":      40.0,
    "alpha_inv":  40.0,
    "mp/me":      6.7,
    "mmu/me":     43.3,
    "mtau/me":    6.7,
    "m_c/m_e":    None,
    "m_s/m_e":    None,
    "alpha_s":    None,
    "H0_midpoint": 23.3,
}
print(f"\n{'Target':<14} {'Broad FP rate %':<18} {'Narrow FP rate %':<18} {'Narrowing helps?':<20}")
print("-" * 70)
target_to_grammar = {
    "G":          "G_gravity (Potential layer)",
    "alpha":      "G_coupling (Information layer)",
    "alpha_inv":  "G_coupling (Information layer)",
    "alpha_s":    "G_coupling (Information layer)",
    "m_p/m_e":    "G_mass (Reality layer)",
    "m_mu/m_e":   "G_mass (Reality layer)",
    "m_tau/m_e":  "G_mass (Reality layer)",
    "m_c/m_e":    "G_mass (Reality layer)",
    "m_s/m_e":    "G_mass (Reality layer)",
    "H0_midpoint": "G_gravity (Potential layer)",
}
for tname, grammar_name in target_to_grammar.items():
    broad = broad_null.get(tname)
    if tname in narrow_results.get(grammar_name, {}):
        narrow = null_narrow[grammar_name][tname]["hit_rate_pct"]
    else:
        narrow = None
    if broad is None or narrow is None:
        print(f"{tname:<14} {'N/A':<18} {f'{narrow:.1f}' if narrow else 'N/A':<18} {'—':<20}")
    else:
        helps = "YES" if narrow < broad else ("same" if narrow == broad else "NO")
        print(f"{tname:<14} {broad:<18.1f} {narrow:<18.1f} {helps:<20}")

# Save
outp = Path("/home/z/my-project/results/dir2_grammar_narrowing.json")
with open(outp, "w") as f:
    json.dump({
        "grammars": {k: {"n_bases": len(v["bases"]), "n_scales": len(v["scales"]),
                          "n_multipliers": len(v["multipliers"]),
                          "size": len(v["bases"]) * 2 * len(v["scales"]) * len(v["multipliers"])}
                     for k, v in GRAMMARS.items()},
        "narrow_grammar_results": narrow_results,
        "structural_null_on_narrow": null_narrow,
        "broad_grammar_fp_rates_for_comparison": broad_null,
    }, f, indent=2, default=str)
print(f"\n[ok] Results saved to {outp}")
