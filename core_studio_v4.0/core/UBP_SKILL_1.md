---
name: UBP Core Studio — AI Assistant Operating Reference
description: Working with the Universal Binary Principal (UBP).
license: Complete terms in LICENSE.txt
---

# UBP Core Studio — AI Assistant Operating Reference
*Sourced from: live execution (23 June 2026) + UBP_Master_Document.docx v1.8*
*Edition: Gravity Update Edition*

**Repository:** `https://github.com/DigitalEuan/UBP_Repo/tree/main/core_studio_v4.0`
**Backbone script:** `core/ubp_unified_v5.py` (v5.4.0 on disk — 3,500 lines)
**Gravity study scripts:** `https://github.com/DigitalEuan/UBP_Repo/tree/main/gravity`
**Author:** E.R.A. Craig (DigitalEuan), Auckland, New Zealand

---

## 1. ENVIRONMENT SETUP

### Fetch scripts via raw GitHub (no authentication, no robots.txt block)

```bash
BASE="https://raw.githubusercontent.com/DigitalEuan/UBP_Repo/main/core_studio_v4.0/core"

# Mandatory backbone (do this first)
curl -s "$BASE/ubp_unified_v5.py"      -o ubp_unified_v5.py

# Useful companions
curl -s "$BASE/ubp_v28_oracle.py"      -o ubp_v28_oracle.py    # primality_nrci, Gray code
curl -s "$BASE/ubp_tgic_engine.py"     -o ubp_tgic_engine.py   # 3-6-9 TGIC logic
curl -s "$BASE/ubp_genesis_boot.py"    -o ubp_genesis_boot.py  # 24 base geometry seeds
```

> **GitHub access rules:**
> - `raw.githubusercontent.com` — WORKS (in allowed-domains for bash_tool)
> - `github.com` web UI — BLOCKED by robots.txt, do not try web_fetch
> - `api.github.com` — hits rate limits very quickly (60 req/hr unauthenticated), avoid
> - Always use `raw.githubusercontent.com` for file fetches

### Dependencies

```
Python ≥ 3.10
stdlib only: fractions, hashlib, json, dataclasses, typing, pathlib, datetime, re, time, math
NO numpy, NO scipy, NO sympy required by the backbone.
```

Run the self-test:
```bash
python3 ubp_unified_v5.py
# Expect: 37/37 correct, Triad 3/3, particle atlas output
# Saves: ubp_unified_v5_report.md + ubp_unified_v5_results.json
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

g   = GolayCodeEngine()                # no args
l   = LeechLatticeEngine(g)            # REQUIRES g as first argument
pp  = UBPSourceCodeParticlePhysics()   # no args; loads all constants as Fractions
tae = TriadActivationEngine(g, l)      # requires g, l
bw  = BarnesWallEngine(256)            # dimension = 256, 512, or 1024
mg  = MonsterGroup()                   # no args
```

**GOTCHA — LeechLatticeEngine requires GolayCodeEngine as first argument.**
`LeechLatticeEngine()` alone → `TypeError: missing 1 required positional argument: 'golay'`

---

## 3. CONSTANTS (from `UBPSourceCodeParticlePhysics`)

All stored as `fractions.Fraction` for exact arithmetic. Use `float(pp.X)` for display only.

| Attribute | Value (float) | Description |
|-----------|---------------|-------------|
| `pp.Y`      | 0.264675430405 | Observer Constant = 1/(π + 2/π) = π/(π²+2) |
| `pp.Y_INV`  | 3.77835…       | 1/Y = π + 2/π |
| `pp.wobble` | 0.817580227176 | Entropic Wobble w = (π·φ·e) mod 1 |
| `pp.L`      | 0.062890786706 | D-Sink Leakage = **w/13** |
| `pp.L_s`    | 0.075993033936 | Stereoscopic Sink = L × σ = L × (29/24) |
| `pp.sigma`  | 29/24 = 1.2083… | Stereoscopic Sink coefficient (Fraction) |
| `pp.U_e`    | 13824          | Existence Unit = 24³ (int, not Fraction) |
| `pp.monad`  | 13.817580227…  | Triadic Monad = π·φ·e (before floor) |
| `pp.pi`     | 3.14159265359  | 50-term continued-fraction π |
| `pp.phi`    | 1.61803398875  | Golden ratio φ |
| `pp.e_const`| 2.71828182846  | Euler's e |

---

## 4. ⚠ CRITICAL NAMING TRAP: L vs L_s

**This has caused errors in multiple prior sessions. Read carefully.**

The master document and all study scripts define:
- **L = w/13** — the D-Sink Leakage. In code: **`pp.L`** (= 0.06289…)
- **L_s = L × (29/24)** — the Stereoscopic Sink. In code: **`pp.L_s`** (= 0.07599…)

The subscript "s" in `L_s` stands for "stereoscopic", not for "standard" or "study".

**Verification:** `pp.wobble / 13 == float(pp.L)` → True (0.06289…)

**When reading gravity study formulas:** L always means `pp.L`. Use `pp.L_s` only when the formula explicitly writes L_s or "stereoscopic leakage". The proton mass formula uses L_s; the eight canonical formulas all use L.

---

## 5. GOLAY ENGINE API

```python
g = GolayCodeEngine()

g.encode(data: list[int])          # 12-bit → 24-bit codeword
g.decode(codeword: list[int])      # 24-bit → 12-bit (error-corrects up to 3 flips)
                                   # Returns 3-tuple: (data, corrected_cw, n_errors)
g.snap_to_codeword(vec: list[int]) # Project arbitrary 24-bit vec onto nearest codeword
g.hamming_weight(vec: list[int])   # Count 1-bits
g.syndrome(vec: list[int])         # 12-bit syndrome
g.syndrome_weight(vec: list[int])  # Weight of syndrome

g.get_all_codewords()  # List of all 4096 codewords (each: list of 24 ints, 0 or 1)
g.get_octads()         # 759 weight-8 codewords
g.get_random_octad()   # One random octad
g.get_shadow_metrics() # Shadow code statistics
g.G                    # 12×24 generator matrix
g.H                    # 12×24 parity check matrix
g.B                    # 12×12 B submatrix
```

**Codeword Hamming Weight (HW) distribution — Golay [24,12,8]:**

| HW | Count | NRCI (α=1) | Status |
|----|-------|------------|--------|
| 0  | 1     | 1.0000     | OnBit (identity) |
| 8  | 759   | 0.7623     | ✅ IN-BAND (above threshold 0.70) |
| 12 | 2576  | 0.6814     | Subliminal |
| 16 | 759   | 0.6160     | Subliminal |
| 24 | 1     | 0.5167     | Edge |

All 759 octads (HW=8) are IN-BAND. HW=12 and HW=16 are NOT.

---

## 6. LEECH ENGINE API

```python
l = LeechLatticeEngine(g)   # g IS REQUIRED

# Tax and NRCI — return fractions.Fraction
l.calculate_symmetry_tax(point: list[int]) -> Fraction
l.calculate_nrci(point: list[int])         -> Fraction
l.symmetry_tax(point: list[int])           -> Fraction  # legacy alias

# Lattice geometry
l.expand_octad(octad: list[int])                    # 24-bit → Leech point (128 coords)
l.expand_octad_to_physical(octad: list[int])        # scaled physical coordinates
l.nearest_octad_idx(vec: list[int]) -> int
l.norm_sq_actual(point: list[int])  -> int          # exact integer Norm²
l.norm_sq_scaled(point: list[int])  -> Fraction     # Norm²/SCALE²
l.ontological_health(point: list[int]) -> dict      # per-layer NRCI breakdown
l.rank_by_stability(points) -> list                 # sort by NRCI

# Constants
l.Y        # = pp.Y (Fraction)
l.Y_CONST  # float version
l.DIM      # 24
l.KISSING  # 196560
l.SCALE    # 8
```

---

## 7. NRCI (Non-Random Coherence Index) — FULL SPECIFICATION

Source: UBP_Master_Document.docx, Section 2.3

### Tax formula (internal, exact)
```
tax(v) = HW(v) × Y + Norm²(v) / 8
```
where:
- `HW(v)` = Hamming weight (count of non-zero elements)
- `Norm²(v)` = sum of squares of all elements (= HW for binary 0/1 vectors)
- `Y` = Observer Constant (Fraction, exact)

**For a canonical Golay octad (HW=8, Norm²=8):**
```
tax = 8 × Y + 8/8 = 8 × 0.26468… + 1 ≈ 3.118
```

### Standard NRCI (α = 1, used for all diagnostics and thresholds)
```
NRCI(v) = 10 / (10 + tax(v))
```

### Parameterised NRCIα (used in Potential-layer formulas)
```
NRCIα(v) = 10 / (10 + α × tax(v))
```
The `α` parameter is a multiplicative weight on the tax. Higher α = more cooling = smaller NRCI.

**NRCIα at canonical octad (tax ≈ 3.118) by confirmed α values:**

| α | NRCI_α | Formula target | Structural meaning |
|---|--------|----------------|-------------------|
| 1/8 | ≈ 0.9625 | Ω_k | Octad-anchored (1/sw where sw=8) |
| 2   | ≈ 0.6160 | n_γ/n_b | Triad − 1 (baryon category) |
| 13  | ≈ 0.1981 | V_ub² | D-Sink dimension (quark mixing) |
| 24  | (predicted) | Higgs potential | Leech rank |
| 3   | (predicted) | Higgs potential alt | Triad |

> **Open issue (June 2026):** The master document states NRCI(α=1/8) ≈ 0.762 (close to
> canonical octad value), but the formula `10/(10 + (1/8)×3.118)` gives 0.9625.
> The exact codeword `v` used in each formula's NRCIα call is not explicitly specified
> in the document. Until resolved: treat NRCIα values as needing direct code verification
> rather than analytical computation from the canonical octad.

### Reference thresholds
| Value | Label | Meaning |
|-------|-------|---------|
| ≈ 0.42 | Noise floor | Empirical NRCI of random 24-bit vectors |
| 0.60 | Anomaly threshold | Below this = structural anomaly flagged |
| 0.70 | Consciousness threshold (θ) | Below this = SUBLIMINAL, not manifested |
| 0.7623 | Canonical octad NRCI | Signature of all 759 Golay octads |
| 1.00 | Identity NRCI | HW=0, tax=0 |

### Where NRCI is NOT used (α correction excluded)
Per the α allocation rule, NRCI cooling **does not apply** to:
- Mass ratios (m_p/m_e, m_μ/m_e) — use D-Sink L directly
- Couplings (α, α_s) — Information-layer, pre-cooled
- Boson masses (m_W, m_Z) — use Topological Shear instead
- Hubble constant H₀ — w-based stochastic arm, pre-manifested
- Gravitational constant G — Phase-4 search result, no NRCI

NRCI cooling **only applies** to Potential-layer formulas that cross the
Potential → Manifest boundary via the Existence Unit U_e.

---

## 8. TOPOLOGICAL SHEAR (Friction)

Source: Section 2.2 of master document. L here means `pp.L` (= w/13).

```python
LY = pp.L * pp.Y   # ≈ 0.016641 at live constants

# First-order shear (Triad-mediated, coefficient = 3)
Shear_1 = 1 + 3 * LY                    # ≈ 1.04992

# Second-order shear (Leech-mediated, adds coefficient = 12 = Leech/2)
Shear_2 = 1 + 3 * LY + 12 * LY**2      # ≈ 1.05324
```

**Which correction applies to which formula:**

| Correction | Formula | Structural justification |
|-----------|---------|--------------------------|
| None | m_μ/m_e, α_s, α³, H₀, G | Near k=0 or pre-manifested |
| Shear_1 | m_W | Cross-layer, one-loop Triad friction |
| Shear_2 + NRCIα(2) | n_γ/n_b | Potential-layer, two-loop friction + cooling |
| NRCIα(1/8) only | Ω_k | Potential-layer, no friction needed |
| NRCIα(13) only | V_ub² | Potential-layer, no friction needed |

---

## 9. THE UNIVERSAL GENERATOR FUNCTION Φ

Source: Section 2.5 of master document. Defined at gravity/10/11_bonus/push11_framework.py:362–399.

### Signature
```
Φ(k, arm, layer, C, correction) → physical constant prediction
```

### Parameters

**k** — Clock position (cycle tick): `{0, 3, 6, 9, 12, 15, 18, 21, 24}`
- Step size Δk = 3 (Triad step)
- k=0: pre-manifest; k=12: self-pairing peak; k=24: cycle return

**arm** — Computational drive:
- `det` — deterministic, Y-driven
- `sto` — stochastic, w-driven

**layer** — Ontological assignment:
- `Reality` — bits 0–5, large values, Base = Y_inv^k (growing)
- `Information` — bits 6–11, small couplings, Base = Y^k (decaying)
- `Activation` — bits 12–17, midpoint, Base = Y^k or Y^(24−k)
- `Potential` — bits 18–23, very small, Base = Y^(24−k) × U_e
- `Cross` — crosses Reality↔Information boundary, Base = Y^k × π
- `w-source` — consumes Wobble in denominator, Base = C/w
- `w-based` — uses Wobble as primary driver, Base = C × w × Y^k × U_e

**C** — Multiplicative constant drawn from structural integers:
`{1, 2, 3, 4, 8, 12, 13, 24, 1/2, 1/3, 1/4, 1/8, 1/12, 1/24, 29/24, 169, 13/L}`

**correction** — Friction/cooling applied to Base:
- `none` — identity
- `shear_1` — × (1 + 3·L·Y)
- `shear_2` — × (1 + 3·L·Y + 12·(L·Y)²)
- `nrci(α)` — × NRCIα(v)
- `shear_2+nrci(α)` — both

### Grammar search space
~8,100 candidate formulas per target (reduced from ~29,700 by Φ typing rules).

---

## 10. CANONICAL FORMULA TABLE (all 8 + G)

Source: Section 4.1 master document. **L = pp.L = w/13 throughout.**

| # | Target | k | arm | layer | C | correction | Err % | FP % | Push |
|---|--------|---|-----|-------|---|-----------|------|------|------|
| 1 | m_μ/m_e | 1 | sto | w-source | 169 | none | 0.029 | 0.0 | #1 |
| 2 | α_s | 4 | det | Info | 24 | none | 0.188 | 0.0 | #4 |
| 3 | m_W | 4 | det | Cross | (13/L)·24·π | shear_1 | 0.094 | 0.0 | #6 |
| 4 | Ω_k | 15 | det | Potential | 24 | nrci(1/8) | 0.035 | 0.0 | #6 |
| 5 | n_γ/n_b | 21 | det | Potential | 1/4 | shear_2+nrci(2) | 0.055 | 0.0 | #10 |
| 6 | V_ub² | 12 | det | Potential | 1/24 | nrci(13) | 0.032 | 0.0 | #7 |
| 7 | α³ | 12 | det | Potential* | 29/24 | none (e replaces U_e) | 0.104 | 0.0 | #8 |
| 8 | H₀ | 3 | sto | w-based | 1/3 | none | 0.495 | 0.02 | #9 |
| G | G_gravity | 18 | det | Potential† | 39/29 | none (Y¹⁸/w) | 0.133 | n/a | #1 |

*Formula 7: Potential with `e` (Euler's number) replacing U_e in the Base term.
†G is NOT a clean Φ instantiation: the 39/29 coefficient came from Phase-4 combinatorial search, not the Layer-to-Grammar theorem. Presented separately.

### Explicit formula expressions

```
1.  m_μ/m_e = 169 / w                                              [= 13/L, tautologically]
2.  α_s      = 24 · Y⁴
3.  m_W      = (13/L) · 24 · Y⁴ · π · (1 + 3·L·Y)               [in GeV, unit bridge implicit]
4.  Ω_k      = 24 · Y¹⁵ · U_e · NRCIα=1/8(v)
5.  n_γ/n_b  = (1/4) · Y²¹ · U_e · Shear_2 · NRCIα=2(v)
6.  V_ub²    = (1/24) · Y¹² · U_e · NRCIα=13(v)
7.  α³       = (29/24) · Y¹² · e
8.  H₀       = (1/3) · w · Y³ · U_e                               [in km/s/Mpc]
    G_UBP    = (39/29) · Y¹⁸ / w                                  [SI units, implicit]
```

**Note on Formula 1:** `13/L = 13/(w/13) = 169/w` — algebraically identical. They are NOT two independent confirmations. One formula.

---

## 11. PARTICLE PHYSICS ENGINE

```python
pp = UBPSourceCodeParticlePhysics()
preds = pp.get_ultimate_predictions()

# preds is a dict. Key entries:
# 'Alpha Inv', 'Proton/e- Ratio', 'Muon/e- Ratio', 'Electron (e-)',
# 'Higgs Boson', 'Top Quark', charmed baryons…, 'global_error', 'sink_metadata'
#
# Each physical entry: {'val': float, 'target': float, 'error_percent': float, 'lens': str}
# sink_metadata: dict with L, L_s, sigma, monad, wobble, leakage_L, status

# Quick benchmark read:
for k, v in preds.items():
    if isinstance(v, dict) and 'error_percent' in v:
        print(f"{k:30s}: pred={v['val']:.4f}  err={v['error_percent']:.4f}%  [{v['lens']}]")
```

**Live benchmark (v5.4.0, June 2026):**

| Particle | Error | Lens |
|----------|-------|------|
| Proton/e⁻ ratio | 0.0000% | Stereoscopic (29/24) |
| Muon/e⁻ ratio | 0.0294% | Pure Inverse (13-D Sink) |
| Gravity (G) | 0.1327% | Topological Resonance |
| 1/α (fine structure inv) | 0.0196% | Core Ratio |
| Higgs boson | 0.0283% | Core Ratio |
| Top quark | 0.0214% | Core Ratio |
| **Global** | **0.112%** | |

---

## 12. PRIMALITY_NRCI AND HEX-CODING PIPELINE

Source: Section 2.4, 3.2 of master document. Implemented at `ubp_v28_oracle.py:561–579`.

### Four-step pipeline
```
Integer n
  → 6-digit hex representation
  → 24-bit Gray code (binary-reflected: Gray(n) ⊕ Gray(n+1) = single bit flip)
  → Golay snap (nearest codeword, corrects ≤ 3 errors)
  → NRCI test against prime band [0.60, 0.95]
  → Miller-Rabin primality (12 witnesses: {2,3,5,7,11,13,17,19,23,29,31,37})
  → 4-way verdict
```

### Four-way verdict
| Verdict | Meaning |
|---------|---------|
| PRIME-IN-BAND | Arithmetically prime AND NRCI ∈ [0.60, 0.95] |
| PRIME-ANOMALY | Arithmetically prime BUT NRCI outside band |
| COMPOSITE-IN-BAND | Composite but structurally coherent |
| COMPOSITE-OUT | Composite and incoherent — noise category |

### Octad priming set: {137, 169, 2197, 28561}
All four integers share:
- NRCI = 0.7623 (canonical octad value)
- Syndrome weight sw = 8
- Gray-coded → snaps to same Information-layer Golay octad

```
137    = prime     → PRIME-IN-BAND
169    = 13²       → COMPOSITE-IN-BAND
2197   = 13³       → COMPOSITE-IN-BAND
28561  = 13⁴       → COMPOSITE-IN-BAND
```

This is why 13, 169, 13² etc. recur in UBP formulas — they all activate the same Information-layer structural unit.

**24 is OUT-OF-BAND** (not a power of 13, does not snap to that octad) but appears as a "scaffold" — it provides dimensional context (Leech rank) rather than octad priming.

**Prime band [0.60, 0.95]** is flagged as "provisional — need calibration" at `ubp_v28_oracle.py:565`. The bounds were selected post-hoc to include the octad NRCI and exclude noise/identity.

---

## 13. ONTOLOGICAL LAYERS AND LAYER-TO-GRAMMAR THEOREM

Source: Section 1.4, 3.1 of master document. Implemented at `ubp_observer_dynamics.py:11–17`.

### Layer partition (4 × 6 bits)
```
Bits 0–5   → Reality layer    → Growing powers Y_inv^k   → Large mass ratios
Bits 6–11  → Information layer → Decaying powers Y^k      → Small couplings
Bits 12–17 → Activation layer  → k=12 self-pairing peak   → Transition dynamics
Bits 18–23 → Potential layer   → Y^(24−k) × U_e           → Cosmological constants
```

### Layer-to-Grammar theorem (Push #10, axiomatic)
Derived from three axioms:
1. The 4×6 bit partition (postulate)
2. Y < 1, so Y^k decays and Y_inv^k grows
3. Physical constants span ~160 orders of magnitude

**Conclusion:** Reality → Y_inv^k; Information → Y^k; Potential → Y^(24−k)·U_e

**Muon exception:** m_μ/m_e uses D-Sink L (not Y-power) because the muon sits at the Weak Horizon boundary — the "Law of the Weak Force = layer-crossing boundary."

### Manifestation mechanism
```python
# Implemented at ubp_observer_dynamics.py:19–25
# If NRCI(v) ≥ 0.70: MANIFESTED → Potential bits become new Reality layer
# If NRCI(v) < 0.70: SUBLIMINAL → new Reality layer = all zeros
```

---

## 14. KNOWN FAILURES (documented in master document)

These targets were tested and failed the UBP grammar:

| Target | Best UBP error | Status |
|--------|---------------|--------|
| Cosmological constant Λ·ℓ_P² | 3.08 × 10¹⁰²% | CATASTROPHIC FAILURE |
| α_G (gravitational fine structure) | 5.9 × 10¹⁷% | CATASTROPHIC FAILURE |
| m_Z (Z boson mass) | 15.8% | NOT SURPRISING |
| sin²θ_W (Weinberg angle) | 34.6% | NOT SURPRISING |

Λ·ℓ_P² and α_G catastrophic failures are the substrate's "principal falsification evidence" — they show the grammar is not arbitrarily flexible.

---

## 15. PRE-REGISTERED OUT-OF-SAMPLE PREDICTIONS (Section 7.3)

| Target | Predicted α | Status |
|--------|------------|--------|
| Ω_DM (dark matter density) | α = 1/8 | Pre-registered, untested |
| Neutrino mass scale | α = 13 | Pre-registered, untested |
| Higgs self-coupling / potential | α = 24 or 3 | Pre-registered, untested |

---

## 16. NULL MODEL PROTOCOL

### Study protocol (5,000-trial Focused Null Model)
```python
import random
TRIALS = 5000; TOL = 0.005   # 0.5% tolerance

# Grammar mirrors Φ parameter space
prefixes   = [1, 2, 3, 4, 6, 8, 13, 24, 29, 1/2, 1/3, 1/4, 1/8, 1/24]
constants  = {'Y': float(pp.Y), 'w': float(pp.wobble), 'L': float(pp.L),
              'Ue': float(pp.U_e), 'pi': float(pp.pi), 'e': float(pp.e_const)}
powers_range = range(-5, 6)

for _ in range(TRIALS):
    prefix = random.choice(prefixes)
    powers = {k: random.choice(powers_range) for k in constants}
    val = prefix * product(c**p for c,p in zip(constants.values(), powers.values()))
    # Count hits within TOL of each target
```

### Empirical FP rates (confirmed June 2026 runs)
| Target | FP rate | Verdict |
|--------|---------|---------|
| μ/e ratio 206.768 | 0.000% | SURPRISING ✓ |
| α_s 0.1181 | 0.040% | SURPRISING ✓ |
| α³ 3.886×10⁻⁷ | 0.000% | SURPRISING ✓ |
| H₀ 70.0 km/s/Mpc | 0.000% | SURPRISING ✓ |

### Verdict thresholds
| Threshold | Label |
|-----------|-------|
| FP < 5% | SURPRISING |
| 5% ≤ FP < 20% | MARGINAL |
| FP ≥ 20% | NOT SURPRISING |
| Formula error < 0.1% | PREDICTIVE (accuracy tier) |
| Formula error < 1% | SURPRISING (accuracy tier) |
| Formula error ≥ 1% | PROVISIONAL |

---

## 17. COMPUTATIONAL SELF-CONSISTENCY CHECKS

The system performs these at `ubp_unified_v5.py:411–416`:
```python
assert pp.Y * pp.Y_INV == 1          # Exact Fraction identity
assert 0 < float(pp.wobble) < 1      # Wobble is valid fractional residue
assert float(pp.L) < float(pp.Y)     # D-Sink leakage < decay rate
assert pp.U_e > 1                    # Amplifier amplifies
```

---

## 18. COMMON WORKFLOW PATTERNS

### Verify a formula against a target
```python
from ubp_unified_v5 import UBPSourceCodeParticlePhysics
from fractions import Fraction

pp = UBPSourceCodeParticlePhysics()
Y = pp.Y
w = pp.wobble
L = pp.L          # ← always pp.L for gravity study formulas (= w/13)
L_s = pp.L_s      # ← only if formula explicitly uses L_s (stereoscopic)
Ue = Fraction(pp.U_e)
e_ = pp.e_const

# Example: α_s formula
formula = 24 * Y**4
target  = Fraction(1181, 10000)
error   = abs(formula - target) / target * 100
print(f"α_s = {float(formula):.6f}  target = {float(target):.6f}  error = {float(error):.4f}%")
```

### Compute NRCI for a specific vector
```python
from ubp_unified_v5 import GolayCodeEngine, LeechLatticeEngine

g = GolayCodeEngine()
l = LeechLatticeEngine(g)   # g REQUIRED

vec     = [1]*8 + [0]*16    # example HW=8 vector
snapped = g.snap_to_codeword(vec)
nrci    = l.calculate_nrci(snapped)
tax     = l.calculate_symmetry_tax(snapped)
print(f"NRCI: {float(nrci):.6f}  Tax: {float(tax):.6f}")
```

### Run primality_nrci on a structural integer
```python
from ubp_v28_oracle import TopologicalALU   # adjust import path as needed
alu = TopologicalALU(g, l)
result = alu.primality_nrci(169)
# Returns: (is_prime: bool, nrci: float, syndrome_weight: int, verdict: str)
print(result)   # e.g. (False, 0.7623, 8, 'COMPOSITE-IN-BAND')
```

### Get all predictions with error breakdown
```python
pp = UBPSourceCodeParticlePhysics()
preds = pp.get_ultimate_predictions()
for k, v in preds.items():
    if isinstance(v, dict) and 'error_percent' in v:
        print(f"{k:30s}: {v['val']:.4f}  err={v['error_percent']:.4f}%  [{v['lens']}]")
```

---

## 19. STRUCTURAL CONSTANTS QUICK REFERENCE

| Constant | Value | Why it appears |
|----------|-------|---------------|
| 24 | Golay/Leech/Monster dimension | U_e = 24³, σ = 29/24, k ↔ 24−k |
| 759 | Golay octads | E_bind = (11/12)·759, self-validation |
| 13 | D-Sink dimension | L = w/13, 196560 = 13×15120 |
| 196560 | Leech kissing number | 13 × 15120, justifies D-Sink = 13 |
| 29 | Leech theta-series prime | σ = 29/24, G = (39/29)·Y¹⁸/w |
| 169 = 13² | Priming integer | m_μ/m_e numerator |
| 2197 = 13³ | Priming integer | Sub-bit priming |
| 28561 = 13⁴ | Priming integer | Sub-bit priming |
| 137 | Priming integer (prime) | 1/α signature |

---

## 20. FALSIFICATION HORIZONS

| Prediction | UBP Value | Test | Timeline |
|-----------|-----------|------|----------|
| Ω_k (spatial curvature) | ≈ 7.27×10⁻⁴ | CMB-S4 | ~2027 |
| n_γ/n_b (baryon asymmetry) | ≈ 1.684×10⁻⁹ | CMB spectral distortions | ~2028+ |
| H₀ | 69.85 km/s/Mpc | DESI/Euclid resolving H₀ tension | 2025–2027 |
| dα/dt (α drift) | exactly 0 | Atomic clocks / quasar spectra | Ongoing |

---

## 21. ARCHITECTURE LAYERS (brief)

```
Layer 4 — Cognitive Orchestration:  ubp_brain_consolidated.py, ubp_integrated_engine_v1.py
Layer 3 — Compilation/Execution:    ubp_py_runtime.py, ubp_sovereign_evolver.py, ubppy.py
Layer 2 — Semantic/Sensory:         ubp_phenomenology.py, ubp_observer_dynamics.py
Layer 1 — Mathematical Substrate:   ubp_unified_v5.py  ← START HERE
```

Only Layer 1 is fully self-contained with stdlib imports. Higher layers may require Flask.

---

## 22. KNOWN OPEN ISSUES (June 2026)

1. **NRCI(α) exact codeword not specified.** The master document gives NRCIα(v) = 10/(10 + α·tax(v)) but does not explicitly state which 24-bit codeword `v` is used in each formula. The canonical octad gives NRCI(α=1/8) ≈ 0.9625, but the document states ≈ 0.762. This discrepancy requires direct code inspection of each push script to resolve.

2. **m_W unit bridge underdocumented.** The formula output (~80.3) matches m_W in GeV without any explicit unit conversion being stated.

3. **G formula is Phase-4 search, not Φ.** The coefficient 39/29 = 3×13/29 was found by combinatorial search over 2,400 candidates, not derived from Layer-to-Grammar. It is consistent with the framework but not a clean instantiation.

4. **Prime band [0.60, 0.95] is provisional.** Flagged in source at `ubp_v28_oracle.py:565`. Pre-registration of band bounds is an open methodological issue.

5. **Priming set {137, 169, 2197, 28561} is not exhaustive.** Other integers may also prime the Information-layer octad via the same Gray-code pipeline; enumeration is an open task.

---

*Built from live execution (June 2026) + UBP_Master_Document.docx v1.8 (Section 2.3, 3.x, 4.x sourced directly). Verify constants against live repo before citing in papers — system is under active development.*