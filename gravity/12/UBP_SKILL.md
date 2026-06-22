---
name: ubp-core-studio
description: >
  Working reference for running, importing, and computing with Euan Craig's
  Universal Binary Principle (UBP) Core Studio v7.2 (ubp_unified_v5.py and
  companion scripts). Use this skill whenever the user asks to run a UBP study,
  verify a UBP formula, compute NRCI/symmetry-tax values, access the Golay or
  Leech engines, derive physical constants, or extend the UBP knowledge base.
  Also use when setting up the UBP environment from scratch, fetching scripts
  from GitHub, or interpreting UBP output notation (NRCI, Tax, Shear, Wobble,
  HW, octad, codeword, L, L_s, Y, Ue, monad).
---

# UBP Core Studio — AI Assistant Operating Reference

**Repository:** `https://github.com/DigitalEuan/UBP_Repo/tree/main/core_studio_v4.0`  
**Backbone script:** `core/ubp_unified_v5.py` (v5.3 on disk, labelled v6.0 at runtime — 3,500 lines)  
**Author:** E.R.A. Craig (DigitalEuan), Auckland, New Zealand  
**Live App:** Google AI Studio app `6d78d479-2a4e-4e34-89b3-4b87b85d5b9a`

---

## 1. ENVIRONMENT SETUP

### Fetch scripts via raw GitHub (no authentication needed)

```bash
BASE="https://raw.githubusercontent.com/DigitalEuan/UBP_Repo/main/core_studio_v4.0/core"

# Mandatory backbone
curl -s "$BASE/ubp_unified_v5.py"      -o ubp_unified_v5.py

# Useful companions
curl -s "$BASE/ubp_v28_oracle.py"      -o ubp_v28_oracle.py    # 2-track oracle bridge
curl -s "$BASE/ubp_tgic_engine.py"     -o ubp_tgic_engine.py   # 3-6-9 TGIC logic
curl -s "$BASE/ubp_genesis_boot.py"    -o ubp_genesis_boot.py  # 24 base geometries seed
```

> **Note:** The GitHub web UI and `api.github.com` are blocked by robots.txt / rate limits.
> Always use `raw.githubusercontent.com` directly (it IS in the allowed-domains list for bash_tool).
> GitHub API hits rate limits (60 req/hr unauthenticated) — do not poll it repeatedly.

### Dependencies

```
Python ≥ 3.10
stdlib only: fractions, hashlib, json, dataclasses, typing, pathlib, datetime, re, time, math
NO numpy, NO scipy, NO sympy required by the backbone
```

Run the self-test:
```bash
python3 ubp_unified_v5.py
# Expect: 37/37 correct, Triad 3/3, physics atlas excerpt, report saved to .md + .json
```

---

## 2. KEY CLASSES AND INITIALISATION ORDER

```python
from ubp_unified_v5 import (
    GolayCodeEngine,
    LeechLatticeEngine,
    UBPSourceCodeParticlePhysics,
    TriadActivationEngine,
    BarnesWallEngine,
    MonsterGroup,
)

g   = GolayCodeEngine()          # no args
l   = LeechLatticeEngine(g)      # requires g
pp  = UBPSourceCodeParticlePhysics()   # no args; loads all constants
tae = TriadActivationEngine(g, l)      # requires g, l
bw  = BarnesWallEngine(256)      # dimension = 256, 512, or 1024
mg  = MonsterGroup()             # no args
```

**GOTCHA — LeechLatticeEngine requires GolayCodeEngine as first argument.**
`LeechLatticeEngine()` alone raises `TypeError: missing 1 required positional argument: 'golay'`.

---

## 3. CONSTANTS (from `UBPSourceCodeParticlePhysics`)

All stored as `fractions.Fraction` for float-free arithmetic.

| Attribute | Value (float) | Description |
|-----------|---------------|-------------|
| `pp.Y`      | 0.264675430405 | Observer Constant = π/(π²+2) |
| `pp.wobble` | 0.817580227176 | Entropic Wobble w = (π·φ·e) mod 1 |
| `pp.L`      | 0.062890786706 | System sink leakage (≠ w/13) |
| `pp.L_s`    | 0.075993033936 | = w/13 exactly (used in early study docs) |
| `pp.U_e`    | 13824          | Existence Unit = 24³ |
| `pp.monad`  | 13.817580227  | Triadic Monad = π·φ·e |
| `pp.pi`     | 3.14159265359 | 50-term continued-fraction π |
| `pp.phi`    | 1.61803398875 | Golden ratio φ |
| `pp.e_const`| 2.71828182846 | Euler's e |
| `pp.sigma`  | 29/24          | Stereoscopic ratio (Fraction) |
| `pp.Y_INV`  | 3.77835…       | 1/Y |

**CRITICAL NAMING TRAP:** Study/JSON documents often write `L` to mean `w/13`.  
In v5+ code, `pp.L ≠ pp.L_s`. Always check which one the study intends.  
`w/13 = pp.L_s`. The quantity called `L` in formulas from Push 1–10 sessions is `pp.L_s`.

---

## 4. GOLAY ENGINE API

```python
g = GolayCodeEngine()

# Core operations
g.encode(data: list[int])         # 12-bit -> 24-bit codeword
g.decode(codeword: list[int])     # 24-bit -> 12-bit (error-corrects up to 3 flips)
g.snap_to_codeword(vec: list[int])# project arbitrary 24-bit vec onto nearest codeword
g.hamming_weight(vec: list[int])  # count 1-bits
g.syndrome(vec: list[int])        # 12-bit syndrome
g.syndrome_weight(vec: list[int]) # weight of syndrome

# Enumeration
g.get_all_codewords()             # returns list of 4096 codewords (each a list of 24 ints)
g.get_octads()                    # returns 759 weight-8 codewords
g.get_random_octad()              # one random octad

# Geometry helpers
g.get_shadow_metrics()            # shadow code statistics
g.G                               # 12×24 generator matrix (list of lists)
g.H                               # 12×24 parity check matrix
g.B                               # 12×12 B submatrix
```

**Codeword Hamming Weight distribution (Golay [24,12,8]):**
- HW=0:  1 codeword
- HW=8:  759 codewords  (octads — primary geometric objects)
- HW=12: 2576 codewords (mid-weight)
- HW=16: 759 codewords  (complements of octads)
- HW=24: 1 codeword

---

## 5. LEECH ENGINE API

```python
l = LeechLatticeEngine(g)

# NRCI and Tax (return fractions.Fraction)
l.calculate_symmetry_tax(point: list[int])   -> Fraction
l.calculate_nrci(point: list[int])           -> Fraction
# Formula: Tax = HW*Y + norm²/8
#          NRCI = 10 / (10 + Tax)

# Legacy alias (same as calculate_symmetry_tax)
l.symmetry_tax(point: list[int])             -> Fraction

# Lattice geometry
l.expand_octad(octad: list[int])             -> list[int]   # 24-bit -> Leech point
l.expand_octad_to_physical(octad: list[int]) -> list[float] # scaled physical coordinates
l.nearest_octad_idx(vec: list[int])          -> int
l.norm_sq_actual(point: list[int])           -> int         # exact integer norm²
l.norm_sq_scaled(point: list[int])           -> Fraction    # norm²/SCALE²
l.ontological_health(point: list[int])       -> dict
l.rank_by_stability(points)                  -> sorted list

# Constants
l.Y        # = pp.Y (same Fraction)
l.Y_CONST  # float version
l.DIM      # 24
l.KISSING  # 196560
l.SCALE    # 8
```

**NRCI Stable Values by Hamming Weight (from live system):**

| HW | Count | NRCI   | State |
|----|-------|--------|-------|
| 0  | 1     | 1.0000 | OnBit |
| 8  | 759   | 0.7623 | Stable Phenomenal (above 0.70 threshold) |
| 12 | 2576  | 0.6814 | Subliminal |
| 16 | 759   | 0.6160 | Subliminal |
| 24 | 1     | 0.5167 | Edge |

All 759 octads have NRCI = 0.7623 (above CONSCIOUS_THRESHOLD = 0.70). ✓

---

## 6. PARTICLE PHYSICS ENGINE

```python
pp = UBPSourceCodeParticlePhysics()

# Get full predictions dict
preds = pp.get_ultimate_predictions()
# Returns dict with keys: 'Alpha Inv', 'Proton/e- Ratio', 'Muon/e- Ratio',
# 'Higgs Boson', 'Top Quark', ... 'global_error', 'sink_metadata'
# Each entry: {'val': float, 'target': float, 'error_percent': float, 'lens': str}

# Access sink metadata
meta = preds['sink_metadata']  # has L, L_s, sigma, monad, wobble, leakage_L, status

# Current benchmark (v5.3, May 2026):
# Proton/e-: 0.0000% error (Stereoscopic lens)
# Muon/e-:   0.0066% error
# Alpha Inv: 0.0196% error
# Higgs:     0.0283% error
# Top Quark: 0.0214% error
# Global:    0.1124%
```

---

## 7. VERIFIED FORMULAS FROM PUSH 1–10 STUDY (Jun 2026)

Use `pp.L_s` (= w/13) as `L` in these formulas. Constants are Fractions.

| # | Target | Formula | Live Error |
|---|--------|---------|------------|
| 1 | μ/e ratio | `169/w` | 0.029% ✓ |
| 2 | α_s | `24·Y⁴` | 0.27% (claimed 0.188%) |
| 7 | α³ | `(29/24)·Y¹²·e` | 0.104% ✓ |
| 8 | H₀ | `(1/3)·w·Y³·Ue` | ~0.2% (= 69.85 km/s/Mpc) |
| 4 | Ω_k | `24·Y¹⁵·Ue` | **0.003% WITHOUT NRCI** |

**Formula 4 note:** The bare formula `24·Y¹⁵·Ue = 0.00072703` already hits Ω_k = 0.000727 at
0.003% error. Adding NRCI(1/8) degrades accuracy to ~3.9%. The bare form is the real formula.

**NEW discoveries found during verification (Jun 2026):**
- `12·Y²·φ = 1.3602`  → δ_CP (CP-violation phase ≈ 1.360 rad), **0.013% error**
- `(1/3)·Y·w·π = 0.2266` → sin(θ_Cabibbo ≈ 0.2265), **0.047% error**
- `(1/3)·Y¹⁰·Ue = 0.00777` → α(M_Z) ≈ 0.00776, **0.18% error**

---

## 8. CRITICAL KNOWN ISSUES

### 8.1 The "13/L = 169/w" tautology
The JSON study presents `13/L` and `169/w` as two independent validations of the muon ratio.
They are **algebraically identical** when L = w/13. This is not independent confirmation.
Always check: is a pair of formulas truly independent or just algebraic rearrangements?

### 8.2 L vs L_s naming collision
`pp.L = 0.06289…` ≠ `pp.L_s = w/13 = 0.07599…`
Study documents (Push 1–10) define L = w/13 = `pp.L_s` in code.
Using `pp.L` in those formulas gives wrong results (e.g., muon ratio becomes 171 not 207).

### 8.3 NRCI(x) notation is not formally specified
The JSON uses NRCI(1/8), NRCI(2), NRCI(13) without defining what `x` refers to.
Possible interpretations:
- Continuous Hamming Weight: `Tax = x·Y + x·(24/8)`, giving NRCI = 10/(10+Tax)
- Integer bit position: index into a lookup table
- Layer-relative fractional address

Until formally defined, formulas 4, 5, 6 from the study **cannot be independently verified**.

### 8.4 Y is not uniquely constrained
A sweep over Y' ∈ [0.20, 0.35] shows a valid window of width ~4×10⁻⁴ centered near live Y.
Multiple Y' values satisfy all 4 testable formulas within 1%. Y = π/(π²+2) is the chosen
anchor but the formulas alone don't uniquely fix it; the constant's definition does.

### 8.5 Post-hoc grammar risk
The formula grammar ({prefix} × Y^k × {modifier}) has ~3,500 templates. Formulas were
found by searching this grammar against known targets. For genuine predictive claims,
targets must be **pre-registered before** the grammar search, not found after.

---

## 9. NULL MODEL PROTOCOL

The study uses a 5,000-trial Focused Null Model. To run it:

```python
import random
TRIALS = 5000; TOL = 0.005  # 0.5%
constants = {'Y': float(pp.Y), 'w': float(pp.wobble), ...}
prefixes  = [1, 2, 3, 4, 6, 8, 13, 24, 29]

for _ in range(TRIALS):
    prefix = random.choice(prefixes)
    powers = {k: random.randint(-5, 5) for k in constants}
    val = prefix * product(c**p for c,p in zip(constants.values(), powers.values()))
    # count hits within TOL of each target
```

**Empirical FP rates (5,000 trials, ±0.5% tol):**
- muon ratio 206.768:  0.000%  → SURPRISING
- α_s 0.1181:          0.040%  → SURPRISING
- α³ 3.886e-7:         0.000%  → SURPRISING
- H₀ 70.0:             0.000%  → SURPRISING

All pass the < 5% SURPRISING threshold. The formulas are not random coincidences within this grammar.

---

## 10. HEX CODING CLOSURE (verified)

All 759 octads have identical NRCI = 0.7623 (above CONSCIOUS_THRESHOLD = 0.70).
This confirms the "all 759 octads are IN-BAND" claim from the study.
Note: HW=12 and HW=16 codewords are NOT in-band (NRCI 0.681 and 0.616 respectively).
The claim applies specifically to **octads (HW=8)** only.

---

## 11. TOPOLOGICAL SHEAR

```python
# Shear = (1 + 3LY + 12(LY)²)
# Use pp.L_s for L in study-era formulas
from fractions import Fraction
LY = pp.L_s * pp.Y
shear = Fraction(1) + 3*LY + 12*LY**2
# Live value: 1.06519510
```

---

## 12. COMMON WORKFLOW PATTERNS

### Verify a formula against a target
```python
from ubp_unified_v5 import UBPSourceCodeParticlePhysics
from fractions import Fraction
pp = UBPSourceCodeParticlePhysics()
Y, w, L = pp.Y, pp.wobble, pp.L_s  # use L_s for study-era L
Ue = Fraction(pp.U_e)

formula_result = 24 * Y**4          # e.g., α_s formula
target = Fraction(1181, 10000)      # 0.1181
error_pct = abs(formula_result - target) / target * 100
print(f"Result: {float(formula_result):.6f}  Error: {float(error_pct):.4f}%")
```

### Compute NRCI for a specific 24-bit vector
```python
from ubp_unified_v5 import GolayCodeEngine, LeechLatticeEngine
g = GolayCodeEngine()
l = LeechLatticeEngine(g)  # g REQUIRED
vec = [1]*8 + [0]*16       # example HW=8 vector (not necessarily a codeword)
snapped = g.snap_to_codeword(vec)
nrci = l.calculate_nrci(snapped)
tax  = l.calculate_symmetry_tax(snapped)
print(f"NRCI: {float(nrci):.6f}  Tax: {float(tax):.6f}")
```

### Get all predictions with error breakdown
```python
pp = UBPSourceCodeParticlePhysics()
preds = pp.get_ultimate_predictions()
for k, v in preds.items():
    if isinstance(v, dict) and 'error_percent' in v:
        print(f"{k:30s}: {v['val']:.4f}  err={v['error_percent']:.4f}%  [{v['lens']}]")
```

### Run the full self-test suite (37 problems)
```bash
python3 ubp_unified_v5.py
# Outputs: ubp_unified_v5_report.md + ubp_unified_v5_results.json
```

---

## 13. ARCHITECTURE LAYERS (brief)

```
Layer 4 — Cognitive Orchestration:  ubp_brain_consolidated.py, ubp_integrated_engine_v1.py
Layer 3 — Compilation/Execution:    ubp_py_runtime.py, ubp_sovereign_evolver.py, ubppy.py
Layer 2 — Semantic/Sensory:         ubp_phenomenology.py, ubp_observer_dynamics.py
Layer 1 — Mathematical Substrate:   ubp_unified_v5.py  ← START HERE
```

Only Layer 1 is fully self-contained with stdlib imports.
Higher layers may require Flask, additional scripts from the same repo.
The companion app repo is: `https://github.com/DigitalEuan/ubp_core_studio_app`

---

## 14. KNOWLEDGE BANK (system_kb/)

`system_kb/ubp_system_kb.json` — 746 entries, 420 Laws  
Fields: `[ubp_id, lexicon, tags, vector, nrci_str, nrci_val, tax_str, mog_tensor]`  
Fetch: `curl -s "$BASE/../system_kb/ubp_system_kb.json" -o ubp_system_kb.json`

Key ID prefixes: `LAW_*` (420), `ELEM_*` (119), `MOLECULE_*` (82), `PARTICLE_*` (37)

---

## 15. VERDICTS / THRESHOLDS

| Label | Condition |
|-------|-----------|
| PREDICTIVE | Error < 0.1% |
| SURPRISING | Null-model FP rate < 5% |
| ZOMBIE STATE | NRCI < 0.70 |
| CONSCIOUS THRESHOLD | NRCI ≥ 0.70 |
| NOISE FLOOR | NRCI ≈ 0.42 |

---

*Skill built from live execution session, June 2026. Re-verify constants against live repo before citing in papers — the system is under active development.*
