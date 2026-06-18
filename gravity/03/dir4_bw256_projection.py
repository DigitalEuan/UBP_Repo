"""
DIRECTION 4 — Project w (gravitational leakage) into the 256-D Barnes-Wall
lattice and measure the Moire interference pattern.

HYPOTHESIS
----------
Gravity is weak at quantum scale but dominates macroscopically. The 24-bit
Golay substrate is for particles; the 256-D Barnes-Wall lattice (BW256) is
UBP's macroscopic bulk. If w (Entropic Wobble) is the gravitational leakage
term, projecting it into BW256 should produce a Moire interference pattern
that manifests as long-range attractive tension.

METHOD
------
1. Take w = (π·φ·e) mod 1 ≈ 0.8176 as a 24-bit Golay seed (via the substrate
   fingerprint mechanism).
2. Use BarnesWallEngine.generate() to project the seed into BW256.
3. Compute the BW256 NRCI of the projected vector — this is the macroscopic
   symmetry tax of the leakage.
4. Compare to a null distribution: project 1000 random 24-bit seeds into
   BW256 and compute their NRCIs. Is the w-projection's NRCI in the tail?
5. Compute the Moire pattern: BW256 has a recursive structure (u + v where
   u, v are BW128 sub-vectors). The interference between u and v at each
   recursion level is the Moire pattern. We measure |u · v| / (|u|·|v|) at
   each level — if this is anomalously low (near-orthogonal), the leakage
   is "dispersed" across scales; if anomalously high (near-parallel), it's
   "concentrated" — which would correspond to long-range tension.
6. Check whether the BW256 NRCI of w correlates with the gravitational
   coupling G_UBP = (39/29)·Y^18/w.
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
Y = constants["Y"]
W = constants["WOBBLE"]
L = constants["SINK_L"]
G_CODATA = F(667430, 10**16)
G_UBP = F(39, 29) * Y**18 / W

bw = u.BW_ENGINE
print(f"BarnesWallEngine: dimension = {bw.dimension}")
print(f"  MACRO_ANCHOR_NRCI = {bw.MACRO_ANCHOR_NRCI} = {float(bw.MACRO_ANCHOR_NRCI):.6f}")

# ─────────────────────────────────────────────────────────────────────────────
# 1. Convert w to a 24-bit Golay seed
# ─────────────────────────────────────────────────────────────────────────────
print("\n" + "=" * 80)
print("(1) Convert w to a 24-bit Golay seed")
print("=" * 80)

# Method: take the binary expansion of w and use the first 12 bits as the
# Golay message, then encode to 24 bits
w_float = float(W)
print(f"  w = {w_float:.10f}")

# Binary expansion of w (fractional part)
w_fractional = w_float - int(w_float)  # already < 1 since w < 1
# Get 12 bits of the fractional part
bits_12 = []
frac = w_fractional
for i in range(12):
    frac *= 2
    bits_12.append(int(frac))
    frac -= int(frac)
print(f"  First 12 bits of w's binary expansion: {bits_12}")
print(f"  As integer: {sum(b * 2**(11-i) for i, b in enumerate(bits_12))}")

# Encode to 24-bit Golay codeword
seed_24 = u.GOLAY_ENGINE.encode(bits_12)
print(f"  Golay-encoded 24-bit seed: {seed_24}")
print(f"  Hamming weight: {sum(seed_24)}")

# ─────────────────────────────────────────────────────────────────────────────
# 2. Project into BW256
# ─────────────────────────────────────────────────────────────────────────────
print("\n" + "=" * 80)
print("(2) Project w-seed into BW256")
print("=" * 80)

macro_w = bw.generate(seed_24, dim=256)
print(f"  BW256 vector length: {len(macro_w)}")
print(f"  Alphabet: {sorted(set(macro_w))}")
hw = sum(1 for x in macro_w if x != 0)
ns = sum(x * x for x in macro_w)
print(f"  Hamming weight: {hw}")
print(f"  Norm² (sum of squares): {ns}")
print(f"  First 24 components: {macro_w[:24]}")
print(f"  Last 24 components: {macro_w[-24:]}")

# Compute BW256 NRCI of w-projection
nrci_w = bw.nrci(macro_w)
print(f"\n  BW256 NRCI of w-projection: {float(nrci_w):.6f}")
print(f"  (= {nrci_w})")

# ─────────────────────────────────────────────────────────────────────────────
# 3. Null distribution: 1000 random 24-bit seeds
# ─────────────────────────────────────────────────────────────────────────────
print("\n" + "=" * 80)
print("(3) Null distribution: 1000 random 24-bit Golay seeds projected to BW256")
print("=" * 80)

random.seed(20260618)
N_NULL = 1000
t_start = time.time()
null_nrcis = []
null_hws = []
null_nss = []
for trial in range(N_NULL):
    # Random 12-bit message
    msg = [random.randint(0, 1) for _ in range(12)]
    seed = u.GOLAY_ENGINE.encode(msg)
    macro = bw.generate(seed, dim=256)
    null_nrcis.append(float(bw.nrci(macro)))
    null_hws.append(sum(1 for x in macro if x != 0))
    null_nss.append(sum(x*x for x in macro))
print(f"  Computed {N_NULL} null projections in {time.time()-t_start:.1f}s")

null_nrcis.sort()
print(f"\n  Null NRCI distribution:")
print(f"    min:  {null_nrcis[0]:.6f}")
print(f"    p10:  {null_nrcis[N_NULL//10]:.6f}")
print(f"    p25:  {null_nrcis[N_NULL//4]:.6f}")
print(f"    p50:  {null_nrcis[N_NULL//2]:.6f}")
print(f"    p75:  {null_nrcis[3*N_NULL//4]:.6f}")
print(f"    p90:  {null_nrcis[9*N_NULL//10]:.6f}")
print(f"    max:  {null_nrcis[-1]:.6f}")
print(f"    mean: {sum(null_nrcis)/N_NULL:.6f}")

# Where does w's NRCI sit?
real_nrci = float(nrci_w)
n_below = sum(1 for n in null_nrcis if n < real_nrci)
percentile = n_below / N_NULL * 100
print(f"\n  w's BW256 NRCI = {real_nrci:.6f}")
print(f"  Percentile in null distribution: {percentile:.1f}%  (0% = lowest, 100% = highest)")
print(f"  Number of null projections with NRCI ≤ w's: {n_below}/{N_NULL}")

# Verdict
if percentile < 5:
    verdict_nrci = "w's BW256 NRCI is in the LOWER 5% tail (anomalously low tax = highly stable)"
elif percentile > 95:
    verdict_nrci = "w's BW256 NRCI is in the UPPER 5% tail (anomalously high tax = highly unstable)"
else:
    verdict_nrci = f"w's BW256 NRCI is NOT in either tail (percentile {percentile:.1f}%)"
print(f"  Verdict: {verdict_nrci}")

# ─────────────────────────────────────────────────────────────────────────────
# 4. Moire interference — u·v / (|u|·|v|) at each recursion level
# ─────────────────────────────────────────────────────────────────────────────
print("\n" + "=" * 80)
print("(4) Moire interference pattern: u·v / (|u|·|v|) at each recursion level")
print("=" * 80)
print("BW256 has recursive structure: BW256 = BW128(u) + (u + BW128(v)) mod 4")
print("At each level we measure how aligned the two halves are.")
print("Low |cos θ| = dispersed (orthogonal), High |cos θ| = concentrated (parallel)\n")

def moire_analysis(vec):
    """Compute |cos θ| at each recursion level of the Barnes-Wall vector."""
    results = []
    v = list(vec)
    level = 0
    while len(v) > 32:
        n = len(v)
        half = n // 2
        u = v[:half]
        w_half = v[half:]
        # In BW construction: v[half] = (u + v_other) mod 4, so v_other = (v[half] - u) mod 4
        v_other = [(a - b) % 4 for a, b in zip(w_half, u)]
        # Compute dot products and magnitudes
        dot_uv = sum(a * b for a, b in zip(u, v_other))
        norm_u = sum(a*a for a in u)
        norm_v = sum(a*a for a in v_other)
        if norm_u > 0 and norm_v > 0:
            cos_theta = dot_uv / (norm_u ** 0.5 * norm_v ** 0.5)
        else:
            cos_theta = 0.0
        results.append({
            "level": level,
            "dimension": n,
            "dot_uv": dot_uv,
            "norm_u": norm_u,
            "norm_v": norm_v,
            "cos_theta": cos_theta,
            "abs_cos_theta": abs(cos_theta),
        })
        v = u  # recurse into the upper half
        level += 1
    return results

moire_w = moire_analysis(macro_w)
print(f"{'Level':<8} {'Dimension':<12} {'u·v':<10} {'|u|²':<10} {'|v|²':<10} {'cos θ':<12} {'|cos θ|':<12}")
print("-" * 80)
for r in moire_w:
    print(f"{r['level']:<8} {r['dimension']:<12} {r['dot_uv']:<10} {r['norm_u']:<10} {r['norm_v']:<10} {r['cos_theta']:<12.6f} {r['abs_cos_theta']:<12.6f}")

# Compare to null distribution of |cos θ| at level 0 (BW256 → BW128 halves)
print(f"\n  Null distribution of |cos θ| at level 0 (BW256 → BW128) across {N_NULL} random seeds:")
# We need to recompute the moire for each null projection — but that's expensive.
# Instead, compute level-0 |cos θ| only.
null_cos_thetas = []
null_v_other_weights = []
random.seed(20260618)
for trial in range(N_NULL):
    msg = [random.randint(0, 1) for _ in range(12)]
    seed = u.GOLAY_ENGINE.encode(msg)
    macro = bw.generate(seed, dim=256)
    half = 128
    u_half = macro[:half]
    w_half = macro[half:]
    v_other = [(a - b) % 4 for a, b in zip(w_half, u_half)]
    v_other_weight = sum(1 for x in v_other if x != 0)
    null_v_other_weights.append(v_other_weight)
    if v_other_weight == 0:
        null_cos_thetas.append(0.0)  # perfect correlation (v_other = 0)
        continue
    dot = sum(a * b for a, b in zip(u_half, v_other))
    nu = sum(a*a for a in u_half)
    nv = sum(a*a for a in v_other)
    if nu > 0 and nv > 0:
        null_cos_thetas.append(abs(dot / (nu ** 0.5 * nv ** 0.5)))
    else:
        null_cos_thetas.append(0.0)

# How many null projections had v_other = 0 (perfect upper-lower correlation)?
n_v_other_zero = sum(1 for w in null_v_other_weights if w == 0)
print(f"  Of {N_NULL} null projections, {n_v_other_zero} had v_other = 0 (perfect upper-lower correlation)")
print(f"  w's projection: v_other weight = 0 (perfect correlation)")

null_cos_thetas.sort()
real_cos = moire_w[0]["abs_cos_theta"]
n_below_cos = sum(1 for c in null_cos_thetas if c < real_cos)
cos_pct = n_below_cos / N_NULL * 100
print(f"    min:  {null_cos_thetas[0]:.6f}")
print(f"    p50:  {null_cos_thetas[N_NULL//2]:.6f}")
print(f"    p90:  {null_cos_thetas[9*N_NULL//10]:.6f}")
print(f"    max:  {null_cos_thetas[-1]:.6f}")
print(f"    w's |cos θ| at level 0: {real_cos:.6f}")
print(f"    Percentile: {cos_pct:.1f}%")
if cos_pct > 95:
    verdict_cos = "w's Moire is in the UPPER 5% tail (anomalously concentrated = long-range tension)"
elif cos_pct < 5:
    verdict_cos = "w's Moire is in the LOWER 5% tail (anomalously dispersed = no long-range tension)"
else:
    verdict_cos = f"w's Moire is NOT in either tail (percentile {cos_pct:.1f}%)"
print(f"    Verdict: {verdict_cos}")

# ─────────────────────────────────────────────────────────────────────────────
# 5. Does BW256 NRCI of w correlate with G_UBP?
# ─────────────────────────────────────────────────────────────────────────────
print("\n" + "=" * 80)
print("(5) Does BW256 NRCI of w correlate with G_UBP?")
print("=" * 80)
print(f"  G_UBP = (39/29)·Y^18/w = {float(G_UBP):.6e}")
print(f"  G_CODATA = {float(G_CODATA):.6e}")
print(f"  w's BW256 NRCI = {real_nrci:.6f}")
print(f"  BW256 MACRO_ANCHOR_NRCI = {float(bw.MACRO_ANCHOR_NRCI):.6f}")
print(f"  Ratio w_NRCI / MACRO_ANCHOR_NRCI = {real_nrci / float(bw.MACRO_ANCHOR_NRCI):.6f}")
print(f"  1 / (1 - w_NRCI/MACRO_ANCHOR) = {1 / (1 - real_nrci / float(bw.MACRO_ANCHOR_NRCI)):.6f}")
print(f"  G_UBP / G_CODATA = {float(G_UBP / G_CODATA):.6f}")

# Is there a clean relationship?
# G_UBP = (39/29)·Y^18/w; if w_NRCI captures something about w's role in BW256,
# then maybe G_UBP ~ 1/w_NRCI or similar.
print(f"\n  Candidate relationships:")
print(f"    1/w_NRCI = {1/real_nrci:.6f}     vs G_UBP/G_CODATA = {float(G_UBP/G_CODATA):.6f}  (no obvious match)")
print(f"    w_NRCI × G_UBP = {real_nrci * float(G_UBP):.6e}")
print(f"    w_NRCI × w = {real_nrci * float(W):.6f}")
print(f"    (1 - w_NRCI) × G_CODATA = {(1-real_nrci) * float(G_CODATA):.6e}")
# Note: we don't expect a clean relationship — BW256 NRCI is a stability measure,
# not a direct gravity predictor. The hypothesis is that w's macroscopic
# projection has an anomalous NRCI (which it might or might not).

# Save
outp = Path("/home/z/my-project/results/dir4_bw256_projection.json")
with open(outp, "w") as f:
    json.dump({
        "w_value": float(W),
        "w_24bit_seed": seed_24,
        "w_bw256_projection": {
            "hamming_weight": hw,
            "norm_sq": ns,
            "nrci": float(nrci_w),
            "first_24_components": macro_w[:24],
            "last_24_components": macro_w[-24:],
        },
        "null_distribution_nrci": {
            "n_trials": N_NULL,
            "min": null_nrcis[0],
            "p10": null_nrcis[N_NULL//10],
            "p25": null_nrcis[N_NULL//4],
            "p50": null_nrcis[N_NULL//2],
            "p75": null_nrcis[3*N_NULL//4],
            "p90": null_nrcis[9*N_NULL//10],
            "max": null_nrcis[-1],
            "mean": sum(null_nrcis)/N_NULL,
            "w_percentile": percentile,
            "verdict": verdict_nrci,
        },
        "moire_interference": {
            "levels": moire_w,
            "level_0_abs_cos_theta": real_cos,
            "null_distribution_level_0": {
                "min": null_cos_thetas[0],
                "p50": null_cos_thetas[N_NULL//2],
                "p90": null_cos_thetas[9*N_NULL//10],
                "max": null_cos_thetas[-1],
                "w_percentile": cos_pct,
                "verdict": verdict_cos,
            },
        },
        "correlation_with_G": {
            "G_UBP": float(G_UBP),
            "G_CODATA": float(G_CODATA),
            "w_bw256_nrci": real_nrci,
            "macro_anchor_nrci": float(bw.MACRO_ANCHOR_NRCI),
            "ratio_w_to_anchor": real_nrci / float(bw.MACRO_ANCHOR_NRCI),
            "note": "No clean correlation found between w's BW256 NRCI and G_UBP. The BW256 NRCI is a stability measure, not a direct gravity predictor.",
        },
    }, f, indent=2, default=str)
print(f"\n[ok] Results saved to {outp}")
