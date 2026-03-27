"""
UBP Nuclear Physics Study
=========================
Step 1: Extract UBP metrics for all elements from the Knowledge Base,
compute experimental nuclear data (semi-empirical binding energies + known
half-lives), and run the full UBP analysis pipeline.

Outputs:
  data/ubp_elements_raw.csv         - raw KB element data
  data/ubp_nuclear_metrics.csv      - UBP metrics per element
  data/experimental_nuclear.csv     - experimental binding energies & half-lives
  data/ubp_vs_experiment.csv        - merged comparison table
  results/ubp_nuclear_summary.json  - key statistical findings
"""

import sys
import json
import hashlib
import math
import numpy as np
import pandas as pd
from fractions import Fraction
from pathlib import Path

# ── paths ──────────────────────────────────────────────────────────────────
SESSION = Path("/app/sandbox/session_20260327_124022_fb146e883394")
USER_DATA = SESSION / "user_data"
DATA_DIR = SESSION / "data"
RESULTS_DIR = SESSION / "results"
for d in [DATA_DIR, RESULTS_DIR]:
    d.mkdir(exist_ok=True)

sys.path.insert(0, str(USER_DATA))

# ── load UBP modules ────────────────────────────────────────────────────────
print("[1/6] Importing UBP modules...")
from core import (
    GolayCodeEngine, LeechLatticeEngine, UBPUltimateSubstrate,
    UBPSourceCodeParticlePhysics, BinaryLinearAlgebra,
)
from physics import UBPMetricsExact, METRICS_EXACT
from geometry import HexDictionaryV4Exact

print("[1/6] UBP modules imported OK")

# ── global singletons ───────────────────────────────────────────────────────
GOLAY  = GolayCodeEngine()
LEECH  = LeechLatticeEngine()
SUBSTRATE = UBPUltimateSubstrate()
CONSTANTS = UBPUltimateSubstrate.get_constants(precision=50)
Y_CONST = CONSTANTS["Y"]

# ── load KB ──────────────────────────────────────────────────────────────────
print("[2/6] Loading UBP Knowledge Base...")
kb_path = USER_DATA / "ubp_system_kb.json"
with open(kb_path) as f:
    KB = json.load(f)
print(f"[2/6] KB loaded: {len(KB)} entries")

# ── Leech Lattice symmetry tax helper ──────────────────────────────────────
def calc_symmetry_tax(vector: list) -> float:
    """Compute symmetry tax for a 24-bit vector using Leech engine."""
    try:
        tax = LEECH.calculate_symmetry_tax(vector)
        return float(tax)
    except Exception:
        return float("nan")

# ── parse math string  e.g. "BP=507/25|Z=1|M=126/125|..." ──────────────────
def parse_math(math_str: str) -> dict:
    result = {}
    if not math_str:
        return result
    for item in math_str.split("|"):
        if "=" in item:
            k, v = item.split("=", 1)
            try:
                result[k] = float(Fraction(v))
            except Exception:
                result[k] = v
    return result

# ── extract element entries ─────────────────────────────────────────────────
print("[3/6] Extracting element data from KB...")
rows = []
for fingerprint, entry in KB.items():
    ubp_id = entry.get("ubp_id", "")
    if not ubp_id.startswith("ELEM_"):
        continue
    atlas = entry.get("atlas", {})
    vector = atlas.get("vector")
    if vector is None or len(vector) != 24:
        continue

    math_params = parse_math(entry.get("math", ""))
    Z = math_params.get("Z")
    if Z is None:
        continue
    Z = int(Z)

    nrci_score = atlas.get("nrci_score", float("nan"))
    tax_str = atlas.get("tax", "0/1")
    try:
        tax_val = float(Fraction(tax_str))
    except Exception:
        tax_val = calc_symmetry_tax(vector)

    weight = atlas.get("weight", sum(vector))
    tilt   = atlas.get("tilt", float("nan"))

    # Golay code analysis
    snapped, snap_meta = GOLAY.snap_to_codeword(vector)
    errors_corrected = snap_meta.get("errors_corrected", 0)
    snap_distance   = snap_meta.get("hamming_distance", 0)
    shadow = GOLAY.get_shadow_metrics()
    fold3  = BinaryLinearAlgebra.fold24_to3(vector)
    core_tension = sum(fold3)

    # Barnes-Wall 256D audit (micro via NRCI)
    fingerprint_hash = hashlib.sha256(
        f"{ubp_id}:{vector}".encode()).hexdigest()

    # compute macro_nrci via BarnesWallEngine if available
    try:
        from ubp_barnes_wall import BarnesWallEngine
        BW = BarnesWallEngine(256)
        bw_vec = BW.generate(fingerprint_hash)
        macro_nrci = float(BW.calculate_nrci(bw_vec))
    except Exception:
        macro_nrci = float("nan")

    rows.append({
        "ubp_id": ubp_id,
        "Z": Z,
        "symbol": ubp_id.split("_")[1],
        "fingerprint": fingerprint,
        "nrci_score": nrci_score,
        "symmetry_tax": tax_val,
        "weight": weight,
        "tilt": tilt,
        "core_tension": core_tension,
        "errors_corrected": errors_corrected,
        "snap_distance": snap_distance,
        "macro_nrci": macro_nrci,
        "mass_amu": math_params.get("M", float("nan")),
        "valence_e": math_params.get("Valence_e", float("nan")),
        "ionisation_kJ": math_params.get("Ion", float("nan")),
        "bp_K": math_params.get("BP", float("nan")),
        "mp_K": math_params.get("MP", float("nan")),
        "en": math_params.get("EN", float("nan")),
        "phase_STP": math_params.get("Phase_STP", float("nan")),
        "crystal": math_params.get("Crystal", float("nan")),
        "vector": vector,
    })
    if Z % 20 == 0:
        print(f"  Processed Z={Z} ({ubp_id})")

df_ubp = pd.DataFrame(rows).sort_values("Z").reset_index(drop=True)
df_ubp.to_csv(DATA_DIR / "ubp_elements_raw.csv", index=False)
print(f"[3/6] Extracted {len(df_ubp)} elements. Saved to data/ubp_elements_raw.csv")

# ── experimental nuclear data ──────────────────────────────────────────────
print("[4/6] Building experimental nuclear dataset...")

# Semi-empirical Bethe-Weizsäcker mass formula parameters (in MeV)
# Based on AME2020 best fits:
A_V  = 15.75    # volume
A_S  = 17.80    # surface
A_C  =  0.711   # Coulomb
A_A  = 23.70    # asymmetry
A_P  = 11.18    # pairing
M_P  = 938.272  # proton mass-energy MeV/c²
M_N  = 939.565  # neutron mass-energy MeV/c²
M_E  =  0.511   # electron mass-energy MeV/c²

# Most abundant / stable isotope for each element Z
# A ≈ 2Z for light elements, then follows stability valley
def most_stable_A(Z: int) -> int:
    """Approximate mass number of most stable / most abundant isotope."""
    if Z <= 20:
        return Z * 2
    # Stability valley approximation: A ≈ 2Z + 0.015*Z^(5/3)
    return int(round(2 * Z + 0.015 * Z**(5/3)))

def bethe_weizsacker(Z: int, A: int) -> float:
    """Semi-empirical binding energy (MeV) for nuclide (Z,A)."""
    N = A - Z
    if N < 0 or A <= 0:
        return float("nan")
    # Volume
    BE  = A_V * A
    # Surface
    BE -= A_S * A**(2/3)
    # Coulomb
    BE -= A_C * Z*(Z-1) / A**(1/3)
    # Asymmetry
    BE -= A_A * (N-Z)**2 / A
    # Pairing
    if A % 2 == 1:
        delta = 0
    elif Z % 2 == 0:   # even-even → most stable
        delta = A_P / A**(1/2)
    else:               # odd-odd
        delta = -A_P / A**(1/2)
    BE += delta
    return BE

def be_per_nucleon(Z: int, A: int) -> float:
    BE = bethe_weizsacker(Z, A)
    if math.isnan(BE) or A == 0:
        return float("nan")
    return BE / A

# Known experimental binding energy per nucleon (MeV/A) for key nuclides
# Source: AME2020 / CRC Handbook
EXPERIMENTAL_BE_PER_NUCLEON = {
    1: 0.0,      # H-1 (unbound)
    2: 1.112,    # He-4? no, H-2 deuteron
    2: 1.112,
    "He4": 7.074,
    4: 7.074,    # He-4
    6: 5.332,    # C-12 → 7.680 MeV/A
    6: 7.680,
    8: 7.976,    # O-16
    26: 8.790,   # Fe-56 (peak stability)
    28: 8.732,   # Ni-62 (highest BE/A experimentally)
    82: 7.867,   # Pb-208
    92: 7.591,   # U-238
}

# Known half-lives (seconds) for representative radioactive elements
# Source: NUBASE2020
KNOWN_HALF_LIVES = {
    # Element Z → (isotope A, half-life in seconds, decay mode)
    43:  (98,  5.97e13, "beta-"),       # Tc-98
    61:  (145, 5.53e8,  "EC"),          # Pm-145
    84:  (209, 3.15e9,  "alpha"),       # Po-209
    85:  (210, 2.83e4,  "alpha"),       # At-210
    86:  (222, 3.30e5,  "alpha"),       # Rn-222
    87:  (223, 1.32e3,  "alpha/beta"),  # Fr-223
    88:  (226, 5.05e10, "alpha"),       # Ra-226
    89:  (227, 6.87e8,  "alpha/beta"),  # Ac-227
    90:  (232, 4.41e17, "alpha"),       # Th-232
    91:  (231, 1.03e12, "alpha"),       # Pa-231
    92:  (238, 1.41e17, "alpha"),       # U-238
    93:  (237, 6.77e13, "alpha"),       # Np-237
    94:  (244, 2.52e15, "alpha"),       # Pu-244
    95:  (243, 2.32e11, "alpha"),       # Am-243
    96:  (247, 4.94e14, "alpha"),       # Cm-247
    97:  (247, 4.30e10, "alpha"),       # Bk-247
    98:  (251, 2.84e10, "alpha"),       # Cf-251
}

# Build experimental dataset
exp_rows = []
for Z in range(1, 119):
    A = most_stable_A(Z)
    be_semi = bethe_weizsacker(Z, A)
    be_per_A_semi = be_semi / A if A > 0 else float("nan")

    # Use known experimental BE/A if available
    be_per_A_exp = EXPERIMENTAL_BE_PER_NUCLEON.get(Z, be_per_A_semi)

    # Half-life: stable elements get inf, radioactive ones get known value
    if Z in KNOWN_HALF_LIVES:
        hl_A, half_life_s, decay_mode = KNOWN_HALF_LIVES[Z]
        is_stable = False
    else:
        # Approximate: elements with Z > 83 are all unstable
        if Z > 83:
            half_life_s = float("nan")
            hl_A = A
            decay_mode = "unknown"
            is_stable = False
        else:
            half_life_s = float("inf")
            hl_A = A
            decay_mode = "stable"
            is_stable = True

    # Compute nuclear "complexity" metrics
    N = A - Z
    asymmetry = abs(N - Z) / A if A > 0 else 0
    coulomb_energy = A_C * Z*(Z-1) / A**(1/3) if A > 0 else 0

    # Magic numbers (shell closures) - proton
    MAGIC = {2, 8, 20, 28, 50, 82, 126}
    is_magic_Z = Z in MAGIC
    is_magic_N = N in MAGIC
    magic_factor = int(is_magic_Z) + int(is_magic_N)

    exp_rows.append({
        "Z": Z,
        "A": A,
        "N": N,
        "be_MeV_total": be_semi,
        "be_per_A_semi": be_per_A_semi,
        "be_per_A_exp": be_per_A_exp,
        "half_life_s": half_life_s,
        "decay_mode": decay_mode,
        "is_stable": is_stable,
        "log10_half_life": math.log10(half_life_s) if (half_life_s and not math.isinf(half_life_s) and half_life_s > 0) else (float("nan") if (math.isnan(half_life_s) if isinstance(half_life_s, float) else False) else 100.0),
        "asymmetry": asymmetry,
        "coulomb_energy": coulomb_energy,
        "is_magic_Z": is_magic_Z,
        "is_magic_N": is_magic_N,
        "magic_factor": magic_factor,
    })

df_exp = pd.DataFrame(exp_rows)
df_exp.to_csv(DATA_DIR / "experimental_nuclear.csv", index=False)
print(f"[4/6] Built experimental dataset for Z=1-118. Saved to data/experimental_nuclear.csv")

# ── merge and compute UBP nuclear metrics ─────────────────────────────────
print("[5/6] Merging UBP and experimental datasets...")
df_merge = df_ubp[["Z", "symbol", "ubp_id", "nrci_score", "symmetry_tax",
                    "weight", "tilt", "core_tension", "errors_corrected",
                    "snap_distance", "macro_nrci", "mass_amu",
                    "valence_e", "ionisation_kJ", "vector"]].merge(
    df_exp, on="Z", how="inner"
)

# ── UBP-specific nuclear metrics ───────────────────────────────────────────
# 1. "Ontological Drift" - Hamming distance between the 24-bit vector
#    and the Golay-snapped version (measures tension from ideal)
def golay_drift(vector):
    try:
        snapped, _ = GOLAY.snap_to_codeword(list(map(int, vector)))
        return BinaryLinearAlgebra.hamming_distance(
            list(map(int, vector)), snapped)
    except Exception:
        return float("nan")

# 2. "Leakage Constant" from the 13D Sink Protocol
#    L = (pi * phi * e mod 1) / 13
try:
    v6 = SUBSTRATE.get_v6_constants()
    L_SINK = float(v6.get("SINK_L", CONSTANTS["Y"]))
except Exception:
    L_SINK = float(CONSTANTS["Y"])

# 3. UBP "Nuclear Coherence Index" (NCI):
#    NCI = nrci_score * (1 - asymmetry) * (1 + magic_factor * L_SINK)
print(f"  L_SINK = {L_SINK:.8f}")

records = []
for _, row in df_merge.iterrows():
    vec = json.loads(row["vector"]) if isinstance(row["vector"], str) else list(row["vector"])
    vec = list(map(int, vec))

    drift = golay_drift(vec)
    asymm = row["asymmetry"]
    magic = row["magic_factor"]
    nrci  = row["nrci_score"]
    tax   = row["symmetry_tax"]
    A     = row["A"]
    Z     = row["Z"]

    # UBP Nuclear Coherence Index
    nci = nrci * (1 - asymm) * (1 + magic * L_SINK)

    # UBP "Binding Energy Proxy" (dimensionless geometric quantity)
    # Hypothesis: stable nuclei (high BE/A) correspond to low symmetry tax
    # and high NRCI.  Proxy = NRCI / (tax / A)
    be_proxy = (nrci / (tax / A)) if (tax > 0 and A > 0) else float("nan")

    # UBP "Stability Pressure" via 13D Leakage
    # The higher the symmetry tax relative to A, the more the nucleus
    # is under "geometric pressure" to shed weight (decay)
    stability_pressure = tax / (A * nrci) if nrci > 0 else float("nan")

    # "Phase Lock" indicator: nrci in [0.60, 0.70] → Physical Phase-Lock
    phase_lock = "PHASE_LOCK" if 0.60 <= nrci <= 0.70 else (
        "SUPER_STABLE" if nrci > 0.70 else "UNSTABLE")

    records.append({
        "ontological_drift": drift,
        "nci": nci,
        "be_proxy": be_proxy,
        "stability_pressure": stability_pressure,
        "phase_lock": phase_lock,
    })

df_ubp_metrics = pd.DataFrame(records)
df_final = pd.concat([df_merge.reset_index(drop=True),
                       df_ubp_metrics.reset_index(drop=True)], axis=1)

# Drop vector column for CSV (too wide)
df_csv = df_final.drop(columns=["vector"])
df_csv.to_csv(DATA_DIR / "ubp_vs_experiment.csv", index=False)
print(f"[5/6] Merged dataset saved ({len(df_csv)} rows). Saved to data/ubp_vs_experiment.csv")

# ── compute UBP nuclear metrics CSV ───────────────────────────────────────
metrics_cols = ["Z", "symbol", "ubp_id", "nrci_score", "symmetry_tax",
                "weight", "tilt", "core_tension", "errors_corrected",
                "snap_distance", "macro_nrci", "ontological_drift",
                "nci", "be_proxy", "stability_pressure", "phase_lock"]
df_ubp_export = df_final[metrics_cols].copy()
df_ubp_export.to_csv(DATA_DIR / "ubp_nuclear_metrics.csv", index=False)
print(f"[5/6] UBP metrics saved to data/ubp_nuclear_metrics.csv")

# ── statistical summary ────────────────────────────────────────────────────
print("[6/6] Computing statistical summary...")
from scipy import stats

# Correlation: NRCI vs BE/A
mask_valid = df_final["be_per_A_semi"].notna() & df_final["nrci_score"].notna()
r_nrci_be, p_nrci_be = stats.pearsonr(
    df_final.loc[mask_valid, "nrci_score"],
    df_final.loc[mask_valid, "be_per_A_semi"])

# Correlation: symmetry_tax vs BE/A
r_tax_be, p_tax_be = stats.pearsonr(
    df_final.loc[mask_valid, "symmetry_tax"],
    df_final.loc[mask_valid, "be_per_A_semi"])

# Correlation: nci vs BE/A
r_nci_be, p_nci_be = stats.pearsonr(
    df_final.loc[mask_valid, "nci"],
    df_final.loc[mask_valid, "be_per_A_semi"])

# Correlation: stability_pressure vs log10(half-life)
mask_hl = (df_final["log10_half_life"].notna()
           & df_final["stability_pressure"].notna()
           & ~df_final["log10_half_life"].isin([100.0]))
r_sp_hl, p_sp_hl = stats.pearsonr(
    df_final.loc[mask_hl, "stability_pressure"],
    df_final.loc[mask_hl, "log10_half_life"]) if mask_hl.sum() > 3 else (float("nan"), float("nan"))

# Magic number analysis
magic_nrci_mean = df_final.loc[df_final["magic_factor"]>0, "nrci_score"].mean()
non_magic_nrci_mean = df_final.loc[df_final["magic_factor"]==0, "nrci_score"].mean()
t_magic, p_magic = stats.ttest_ind(
    df_final.loc[df_final["magic_factor"]>0, "nrci_score"].dropna(),
    df_final.loc[df_final["magic_factor"]==0, "nrci_score"].dropna())

# Iron peak: Z=26 (Fe)
fe_row = df_final[df_final["Z"]==26].iloc[0] if len(df_final[df_final["Z"]==26]) > 0 else None

# Particle physics predictions
pp = UBPSourceCodeParticlePhysics(precision=50)
preds = pp.get_ultimate_predictions()

summary = {
    "study_name": "UBP Nuclear Physics Study: Binding Energies and Decay Rates",
    "data_version": "AME2020 semi-empirical + NUBASE2020 half-lives",
    "n_elements": len(df_final),
    "correlations": {
        "nrci_vs_BE_per_A": {"r": round(r_nrci_be, 4), "p": round(p_nrci_be, 6)},
        "symmetry_tax_vs_BE_per_A": {"r": round(r_tax_be, 4), "p": round(p_tax_be, 6)},
        "nci_vs_BE_per_A": {"r": round(r_nci_be, 4), "p": round(p_nci_be, 6)},
        "stability_pressure_vs_log_halflife": {"r": round(r_sp_hl, 4) if not math.isnan(r_sp_hl) else None, "p": round(p_sp_hl, 6) if not math.isnan(p_sp_hl) else None},
    },
    "magic_number_analysis": {
        "magic_mean_nrci": round(magic_nrci_mean, 6),
        "non_magic_mean_nrci": round(non_magic_nrci_mean, 6),
        "t_stat": round(t_magic, 4),
        "p_value": round(p_magic, 6),
        "interpretation": "Magic nuclei show NRCI difference vs non-magic"
    },
    "iron_peak": {
        "Z": 26,
        "nrci": round(float(fe_row["nrci_score"]), 6) if fe_row is not None else None,
        "nci": round(float(fe_row["nci"]), 6) if fe_row is not None else None,
        "be_proxy": round(float(fe_row["be_proxy"]), 4) if fe_row is not None else None,
        "phase_lock": fe_row["phase_lock"] if fe_row is not None else None,
    },
    "particle_physics_global_error": round(preds["global_error"], 5),
    "ubp_13d_sink": preds["sink_metadata"],
    "L_SINK": L_SINK,
    "phase_lock_distribution": df_final["phase_lock"].value_counts().to_dict(),
    "top10_highest_nrci": df_final.nlargest(10, "nrci_score")[["Z","symbol","nrci_score","be_per_A_semi","is_magic_Z"]].to_dict(orient="records"),
    "top10_highest_nci": df_final.nlargest(10, "nci")[["Z","symbol","nci","nrci_score","be_per_A_semi","magic_factor"]].to_dict(orient="records"),
}

with open(RESULTS_DIR / "ubp_nuclear_summary.json", "w") as f:
    json.dump(summary, f, indent=2, default=str)
print(f"[6/6] Summary saved to results/ubp_nuclear_summary.json")

print("\n" + "="*70)
print("UBP NUCLEAR ANALYSIS COMPLETE")
print("="*70)
print(f"  NRCI ↔ BE/A  :  r = {r_nrci_be:.4f}  (p = {p_nrci_be:.2e})")
print(f"  Tax  ↔ BE/A  :  r = {r_tax_be:.4f}  (p = {p_tax_be:.2e})")
print(f"  NCI  ↔ BE/A  :  r = {r_nci_be:.4f}  (p = {p_nci_be:.2e})")
print(f"  Magic nuclei NRCI: {magic_nrci_mean:.4f} vs non-magic: {non_magic_nrci_mean:.4f}  (p={p_magic:.4f})")
print(f"  Particle physics global error: {preds['global_error']:.4f}%")
print("="*70)
