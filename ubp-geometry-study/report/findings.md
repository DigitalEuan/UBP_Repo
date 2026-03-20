# UBP Geometry Investigatory Study (Platonic 3D, Folding, UBP-Py, Symmetry Tax)

**System used:** UBP Core Studio v4.0 (UBP Core v5.7 “Pure Geometry”) from your repo: https://github.com/DigitalEuan/UBP_Repo/tree/main/core_studio_v4.0 [Source](https://github.com/DigitalEuan/UBP_Repo/tree/main/core_studio_v4.0)

**Primary objective:** probe whether the UBP substrate (Golay(24,12,8) + Leech-based “symmetry tax” + UBP-Py dynamics) yields interesting structural *geometry-like* phenomena that could be interpreted as platonic / folding / tax insights worth deeper analysis.

**What’s included in the ZIP:** reproducible scripts, raw CSV/JSON outputs, and figures. (See `data/` and `figures/`.)

---

## 1) Key UBP primitives used (so the study is grounded in your system)

### 1.1 Symmetry Tax (as implemented)
In UBP Core, the Leech engine defines:

> **Tax = (HammingWeight × Y) + (Norm² / 8)**

For binary (0/1) 24-vectors, **Norm² = HammingWeight**, so within the Golay codebook the tax collapses to:

> **Tax(binary codeword) = weight × (Y + 1/8)**

This matters because it implies *within the pure Golay codeword set*, “tax” is determined by **weight only**, not by *which* codeword you pick. That forces “interesting tax-geometry” to emerge either from:
1) leaving the strict 0/1 Golay set, or
2) studying relational structure (triads/closures), not single-codeword tax.

Tax definition is documented in your UBP Core Studio docs and code [Source](https://github.com/DigitalEuan/UBP_Repo/blob/main/core_studio_v4.0/core/ubp_files_and_usage.md).

### 1.2 UBP-Py “spiral” dynamic used for testing
The UBP-Py VM spiral step flips even bit indices then snaps back to Golay via decode→encode [Source](https://github.com/DigitalEuan/UBP_Repo/blob/main/core_studio_v4.0/core/ubp_py_runtime.py).

I implemented the same step as a deterministic map **f: Golay→Golay** and analyzed its orbit structure.

---

## 2) Insight A (deep test): the octads form a *highly rigid triadic closure geometry*

### 2.1 What was tested
You emphasize **759 octads** (weight-8 Golay codewords) as a privileged family. In your KB you also mention **“functional logic triads”** built from octads.

Test: treat each octad as a 24-bit bitmask. For octads A and B, compute **A ⊕ B**. If **A ⊕ B is also an octad**, then {A,B,A⊕B} forms a closed triad.

### 2.2 What was found
Across the 759 octads:

- **Number of XOR-closed triads:** **35,420** (`data/octad_triads.json`)
- The induced undirected graph (edge if two octads share a triad) has:
  - **Nodes:** 759
  - **Edges:** 106,260
  - **Degree:** **exactly 280 for every node** (perfect regularity)

This is already a strong “platonic-like” signature: uniform local connectivity everywhere.

### 2.3 Stronger rigidity: constant common-neighbor counts (SRG probe)
I additionally probed **common-neighbor counts**:

- For **adjacent** nodes (connected by an edge): sampled pairs all had **exactly 140** common neighbors.
- For **non-adjacent** nodes: sampled pairs had **either 85 or 28** common neighbors.

That looks like an “almost strongly-regular” structure, except non-edges appear to split into at least two classes (85 vs 28). This is a good candidate for deeper group-theoretic investigation.

**Artifacts:**
- `figures/octad_degree_hist.png`
- `figures/octad_triads_subgraph.png`
- `data/octad_graph_srg_probe.json`

---

## 3) Insight B (deep test): a concrete “3-fold” compression produces a *4-symbol* core-tension alphabet

### 3.1 Motivation
Your KB includes **LAW_GEO_FOLD_001**:

> *Fold(24) -> 12 -> 6 -> 3 | Limit = 3 Folds*

But in the codebase, I didn’t find a canonical folding operator implementation. So I tested one natural candidate consistent with the statement: **pairwise XOR folding** (adjacent bits):

- Fold1: 24→12 by `v'[i] = v[2i] ⊕ v[2i+1]`
- Fold2: 12→6 similarly
- Fold3: 6→3 similarly

### 3.2 Result: only 4 fold-states appear for the entire Golay codebook
For **all 4096 Golay codewords**, the folded 3-bit outputs are exactly four patterns:

- 000, 011, 101, 110

And each appears **exactly 1024 times**.

This is extremely “clean”: a 4096-state universe compresses to a perfectly balanced 4-symbol “core-tension” alphabet under 3 folds.

### 3.3 Octads are slightly biased away from 000
For octads only:

- 000 occurs 183 times
- the other three states occur 192 times each

So octads are “almost uniform” across these 4 folded states, but with a measurable depletion of the all-zero fold-state.

**Artifacts:**
- `data/fold3_string_distribution.json`
- `figures/fold3_weight_by_weight.png`

---

## 4) Insight C (deep test): the UBP-Py spiral map is an *involution* over the Golay codebook

### 4.1 What was tested
Using the UBP-Py-inspired step:

1) flip even indices
2) Golay decode→encode snap

I measured cycle lengths.

### 4.2 Result
Across **all 4096 codewords**, the dynamics partitions into:

- **2048 disjoint 2-cycles**
- **0 fixed points**
- no longer orbits (max orbit size = 2)

So the step is an **involution** on the Golay codebook: applying it twice returns you to the start.

This is a surprisingly strong property. It suggests this spiral operator is closer to a **reflection / parity operator** than to a “growth” mechanism.

**Artifacts:**
- `data/spiral_orbit_summary.json`
- `data/spiral_period_samples.csv` (sampled)
- `figures/spiral_period_hist.png`

---

## 5) “Platonic geometry” angle: what did *not* appear (and why that’s useful)

A naive “Platonic mapping” might expect weight families like 4 (tetra), 6 (octa), 8 (cube) to exist as **Golay codeword weights**.

But the extended binary Golay code’s weight distribution (as realized in your implementation) is strictly:

- weights present: **0, 8, 12, 16, 24**
- counts: 1, 759, 2576, 759, 1

So “tetra/octa” aren’t literal codeword-weight classes in Golay.

This is still informative: it implies that if your KB laws talk about tetrahedral or octahedral families, they likely refer to **derived structures** (octads, dodecads, MOG partitions, or non-binary Leech coordinates), not to raw Golay weight classes.

**Artifacts:**
- `data/golay_weight_distribution.csv`
- `figures/weight_distribution.png`

---

## 6) Recommendations for your next deeper analysis

If you want to push this into a more “platonic 3D folding” direction inside UBP, the highest-yield next steps look like:

1) **Prove / classify the octad triad graph**
   - Determine whether it is a known object (strongly regular graph, association scheme, or related to Mathieu group actions on octads).
   - The observed constants (degree=280; edge common neighbors=140; nonedge common neighbors splitting into {85,28}) are strong invariants.

2) **Define an official fold operator in UBP-Py / core**
   - My XOR fold gives a striking 4-symbol alphabet.
   - If you define a fold operator consistent with your KB, you can test whether different fold definitions correspond to different “core tensions” and whether those correlate with NRCI, tilt, or domain tags.

3) **Modify the spiral operator if “growth” is intended**
   - The current even-bit flip + snap behaves as a reflection (2-cycles only).
   - Introducing a second transform (e.g., phase-shifted flips, octad injection, or MOG-layer coupling) may produce richer orbit structure.

---

## Appendix: file map of outputs

- `data/golay_codeword_metrics.csv` — per-codeword metrics (weight, tax, nrci, tilt, fold3)
- `data/golay_weight_distribution.csv` — weight distribution
- `data/octad_triads.json` — triad count and sample triads
- `data/octad_graph_degree.csv` — degree distribution (uniform)
- `data/octad_graph_srg_probe.json` — common-neighbor probe
- `data/fold3_string_distribution.json` — 3-bit fold alphabet distribution
- `data/spiral_orbit_summary.json` — orbit decomposition result (all 2-cycles)

Figures:
- `figures/weight_distribution.png`
- `figures/tilt_hist_platonic_weights.png` (note: 4/6 weights are empty in Golay; plot focuses on present weights)
- `figures/fold3_weight_by_weight.png`
- `figures/octad_degree_hist.png`
- `figures/octad_triads_subgraph.png`
- `figures/spiral_period_hist.png`
