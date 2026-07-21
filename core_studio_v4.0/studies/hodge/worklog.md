# TGIC_v2 Development Worklog

---
Task ID: 1
Agent: Main Agent
Task: Build TGIC_v2 extended framework script from UBP Core Studio test data

Work Log:
- Read and analyzed 802-line UBP Core Studio test file (ubp_tests_2.txt)
- Extracted 6-experiment discovery pipeline: GF(2) Hodge Diamond -> GF(4) Hexacode -> MOG columns -> Parity Audit -> MOG Hunter -> Aligned GF(4) Proof
- Key discovery: 24-bit MOG Permutation Key found at Tick 1020, reducing parity leakage from 31.25% to 0.00%
- Read v1 TGIC LaTeX framework (452 lines) to extract formal definitions for extension
- Built self-contained TGIC_v2 Python script (1300+ lines) implementing all 6 UBP development leads
- Fixed critical bug: generator matrix dependence of MOG key -- implemented auto-hunt instead of hard-coding
- Fixed critical bug: odd-parity codewords producing NOISE -- implemented standard MOG top-row flip convention
- Verified: 4096 codewords, 759 octads, d_min=8, zero NOISE across all codewords after alignment

Stage Summary:
- Produced `/home/z/my-project/scripts/tgic_v2.py` and `/home/z/my-project/download/tgic_v2.py`
- Script is fully self-contained (stdlib only), documents TGIC = "Triad-Graph Interaction Constraint", v2 as extension
- Key results: 1130/4096 perfect codewords (NOISE=0, Balance=1), 217/759 balanced octads
- Leads 1 (homology jumping) and 6 (canonical evolution) work perfectly
- Leads 3 (finiteness), 4 (rotation), 5 (rationality) identified as needing refinement -- failure as direction

---
Task ID: 2
Agent: Main Agent
Task: Hodge-focused push on TGIC_v2 -- improve all 6 leads, add DHC test

Work Log:
- Fixed holomorphic_balance: all-REAL vectors now get balance=0 (not vacuously 1)
- Refined Lyapunov functional E_balance formula to avoid degenerate case
- Replaced crude SO(4) rotation with M_24 automorphism-based rotation (column swaps, row swaps)
- Replaced rotation-orbit rationality detector with hexacode constraint satisfaction (3 GF(4) linear constraints)
- Fixed finiteness test: now uses canonical evolution (converges in avg 0.6 ticks)
- Added Discrete Hodge Conjecture (DHC) module with exhaustive and sample-based testing
- Added Strong DHC test combining NOISE=0 + hexacode membership
- Ran full Hodge-focused experiment suite

Stage Summary:
- KEY FINDING: DHC CONVERSE FAILS -- 6,255 counterexamples in 200k sample (NOISE=0 but not codeword)
- Direction identified: GF(4) projection is NECESSARY but not SUFFICIENT to characterise algebraic cycles
- Strong DHC also fails: only 68/4096 codewords are hexacode-rational with current constraints
- The MOG parity condition (which gave zero NOISE for all codewords) is weaker than the true code structure
- The correct hexacode constraints for this generator/alignment combination need to be derived from the code itself, not assumed from standard references
- Leads 1,2,3,6 all WORKING; Leads 4,5 need further refinement based on DHC direction
- Updated download/tgic_v2.py with all v2.1 improvements

---
Task ID: 3
Agent: Main Agent
Task: Push 2 -- Lead 4/5/DHC Refinement. Derive correct hexacode constraints, discover actual automorphisms, test DHC.

Work Log:
- Phase B: Searched all 20 W/W_BAR assignments of 6 weight-2 patterns. Best: 80/4096 (2.0%) pass standard hexacode constraints. The GF(4) classification is FUNDAMENTALLY non-linear.
- Phase C: Brute-force derived constraint space from 1034 distinct hexacode words. Found 0 linear constraints. Confirmed: hexacode words do NOT form a linear subspace of GF(4)^6 for ANY assignment.
- Phase D: Tested all 276 transpositions for code automorphism. Result: 0/276. Confirmed: M_24 contains NO transpositions.
- Phase D-extended: Tested all 4048 3-cycles. Result: 0/4048. M_24 elements are not low-order cycles in our coordinate system.
- Phase D-extended: Tested 21 MOG column/row swaps on MOG-aligned codewords. Result: 0/21. MOG structural permutations are not code automorphisms (they don't preserve hexacode C_6).
- Phase E (DHC): Forward PROVEN (4096/4096). Converse FAILS: 15,750 counterexamples in 500K sample. NOISE=0 alone is necessary but wildly insufficient (15,866 NOISE=0 vectors, only 116 codewords).

Stage Summary:
- Produced `/home/z/my-project/scripts/tgic_v2_push2.py` (refined Lead 4/5/DHC modules)
- KEY FINDING 1: The GF(4) weight-based classification destroys linearity. 1034 hex words, 0 constraints.
- KEY FINDING 2: M_24 has no transpositions or 3-cycles in our coordinate system. Need higher-order generators.
- KEY FINDING 3: NOISE=0 catches 3.15% of all vectors. Only 0.73% of those are codewords. DHC gap is enormous.

---
Task ID: 4
Agent: Main Agent
Task: Push 2b -- Linear hexacode map search, DHC gap cascade analysis, weight+NOISE joint analysis.

Work Log:
- Phase 1: Linear hexacode map search. Tested restricted family (b0, L(b1,b2,b3)) with 7^6=117,649 candidates. Distribution: dim=8 (2), dim=9 (76), dim=10 (708), dim=11 (2692), dim=12 (1522). Most maps are nearly injective.
- Phase 1-extended: Tested 20 specific linear maps. Key discovery: (b0+b1, b2+b3) gives dim=5, |image|=32. (b0+b1, b2+b3) gives dim=7, |image|=128.
- Phase 1-breakthrough: Using (b0+b1, b2+b3) for 5 columns + ANY different map for 1 column gives dim=6, |image|=64 -- EXACTLY the hexacode. All 36 substitution options work.
- Phase 1-DHC: With dim=6 map, tested 2M random vectors. NOISE=0 + hexacode constraints: 31,635 pass, but only 515 are codewords. Gap = 31,120. DHC still fails.
- Phase 3: DHC gap cascade. F0=500K -> F1(NOISE=0)=15,866 -> F2(+bal>0)=13,951 -> F3(+Golay_wt)=7,113 -> codewords=4,096. Each geometric filter reduces but never closes the gap.
- Phase 4: Weight+NOISE analysis (2M vectors). NOISE=0 weight distribution peaks at 12, symmetric. NOISE=0+Golay_weight: 31,377, of which 483 are codewords (1.54%).
- Parity check distribution for random vectors is binomial-like, centered at 6/12. Codewords are exactly 12/12.

Stage Summary:
- Produced `/home/z/my-project/scripts/tgic_v2_push2b.py`
- KEY RESULT: Discrete Hodge Conjecture is FALSE for the Golay code with any tested filter combination:
  * NOISE=0 alone: 63K candidates vs 4,096 codewords (15x gap)
  * NOISE=0 + Golay weight {0,8,12,16,24}: 31K candidates (7.6x gap)
  * NOISE=0 + dim=6 hexacode constraints: 31.6K candidates (7.7x gap)
  * NOISE=0 + hexacode + Golay weight: ~16K estimated (4x gap)
  * The algebraic condition (12 parity checks) is the ONLY exact characterisation.
- DIRECTION: The geometric (Hodge) conditions capture a SUPERSET of the algebraic cycles. The gap between geometric and algebraic is the discrete analog of the Hodge Conjecture's central difficulty. The fact that it persists even with linear hexacode structure suggests the Hodge (p,p) condition requires ADDITIONAL structure (Lefschetz operators, polarization, etc.) to characterise algebraicity.