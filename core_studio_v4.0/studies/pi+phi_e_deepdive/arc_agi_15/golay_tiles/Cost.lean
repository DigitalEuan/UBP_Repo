import GolayTiles.Hexacode
import GolayTiles.Substrate

/-!
# The cost quanta of the tile calculus

The tile method prices operations in a single quantum `Q`.  This file fixes
that quantum and proves the two facts about it that the rest of the
development uses:

* `Y`, `Q` — the read quantum `Y = 1/(π + 2/π)` and the activation quantum
  `Q = Y + 1/8`, both positive (`Y_pos`, `Q_pos`);
* `readCost_le_amgm`, `Y_lt_amgm` — the read cost is capped at `1/(2√2)` by
  AM–GM, with equality only at `Π = √2`, and `Y` is strictly below the cap;
* `nrci_calibrated`, `nrci_ladder`, `nrci_cal_strictAnti` — with the budget
  calibrated to `B = 8Q`, the coherence index of a weight-`n` tile is
  `8/(8+n)` whatever `Q` is, giving the ladder `1, 1/2, 2/5, 1/3, 1/4` at the
  weights `0, 8, 12, 16, 24` of the Golay code, strictly decreasing in weight.

Nothing below depends on the particular value of `Q`; `Tax.lean` uses only
`Q_pos`.
-/

namespace GolayHex

/-! ## The prices -/

open Real

/-- The read quantum `Y = 1/(π + 2/π)`. -/
noncomputable def Y : ℝ := 1 / (π + 2 / π)

/-- The activation quantum `Q = Y + 1/8`. -/
noncomputable def Q : ℝ := Y + 1 / 8

theorem Y_pos : 0 < Y := by
  have hpi := Real.pi_pos
  have h : 0 < π + 2 / π := by positivity
  unfold Y
  positivity

theorem Q_pos : 0 < Q := by
  have := Y_pos
  unfold Q
  linarith

/-- **The read operator is capped by AM–GM.**  `Y[Π] = 1/(Π + 2/Π) ≤ 1/(2√2)`
for every positive loop-check `Π`, with equality exactly at `Π = √2`. -/
theorem readCost_le_amgm {x : ℝ} (hx : 0 < x) :
    1 / (x + 2 / x) ≤ 1 / (2 * Real.sqrt 2) := by
  have hsq : Real.sqrt 2 ^ 2 = 2 := Real.sq_sqrt (by norm_num)
  have hsn : (0:ℝ) ≤ Real.sqrt 2 := Real.sqrt_nonneg 2
  have hge : 2 * Real.sqrt 2 ≤ x + 2 / x := by
    have hx' : x ≠ 0 := ne_of_gt hx
    have hrw : x + 2 / x = (x ^ 2 + 2) / x := by field_simp
    rw [hrw, le_div_iff₀ hx]
    nlinarith [sq_nonneg (x - Real.sqrt 2)]
  have hpos : 0 < 2 * Real.sqrt 2 := by
    have : (0:ℝ) < Real.sqrt 2 := Real.sqrt_pos.mpr (by norm_num)
    linarith
  exact one_div_le_one_div_of_le hpos hge

/-- `Y` is strictly below the cap: `π ≠ √2`. -/
theorem Y_lt_amgm : Y < 1 / (2 * Real.sqrt 2) := by
  have hpi1 : (3.14 : ℝ) < π := Real.pi_gt_d2
  have hpi2 : π < 3.15 := Real.pi_lt_d2
  have hx : (0:ℝ) < π := by linarith
  have h2 : (0.6 : ℝ) < 2 / π := by
    have hmul : (0.6 : ℝ) * π < 2 := by nlinarith
    exact (lt_div_iff₀ hx).mpr hmul
  have hden : (3.7 : ℝ) < π + 2 / π := by linarith
  have hY : Y < 1 / 3.7 := by
    unfold Y
    exact one_div_lt_one_div_of_lt (by norm_num) hden
  have hsq : Real.sqrt 2 ^ 2 = 2 := Real.sq_sqrt (by norm_num)
  have hsn : (0:ℝ) ≤ Real.sqrt 2 := Real.sqrt_nonneg 2
  have hs : Real.sqrt 2 < 1.4143 := by nlinarith
  have hpos : (0:ℝ) < 2 * Real.sqrt 2 := by
    have : (0:ℝ) < Real.sqrt 2 := Real.sqrt_pos.mpr (by norm_num)
    linarith
  have hcap : 1 / (2 * 1.4143 : ℝ) < 1 / (2 * Real.sqrt 2) :=
    one_div_lt_one_div_of_lt hpos (by linarith)
  have : (1:ℝ) / 3.7 < 1 / (2 * 1.4143) := by norm_num
  linarith

/-- The coherence index with a budget `b`. -/
noncomputable def nrciB (b t : ℝ) : ℝ := b / (b + t)

/-- **The calibrated ladder is free of `Q`.**  Once the budget is calibrated to
`B = 8Q`, the coherence index of a weight-`n` tile is `8/(8+n)` whatever `Q`
happens to be. -/
theorem nrci_calibrated (n : ℕ) : nrciB (8 * Q) (n * Q) = 8 / (8 + n) := by
  have hQ : Q ≠ 0 := ne_of_gt Q_pos
  have hpos : (0:ℝ) < 8 + n := by positivity
  unfold nrciB
  rw [show 8 * Q + n * Q = (8 + n) * Q by ring]
  rw [div_eq_div_iff (by positivity) (by positivity)]
  ring

/-- The four regimes: vacuum, octad, dodecad, hexadecad, universe. -/
theorem nrci_ladder :
    nrciB (8 * Q) (0 * Q) = 1 ∧ nrciB (8 * Q) (8 * Q) = 1 / 2 ∧
    nrciB (8 * Q) (12 * Q) = 2 / 5 ∧ nrciB (8 * Q) (16 * Q) = 1 / 3 ∧
    nrciB (8 * Q) (24 * Q) = 1 / 4 := by
  have hQ : 0 < Q := Q_pos
  refine ⟨?_, ?_, ?_, ?_, ?_⟩
  · unfold nrciB; rw [zero_mul, add_zero, div_self (by linarith)]
  all_goals
    · unfold nrciB
      rw [div_eq_div_iff (by linarith) (by norm_num)]
      ring

/-- Heavier tiles are less coherent, strictly. -/
theorem nrci_cal_strictAnti {m n : ℕ} (h : m < n) :
    (8 : ℝ) / (8 + n) < 8 / (8 + m) := by
  have hm : (0:ℝ) < 8 + m := by positivity
  have hn : (0:ℝ) < 8 + n := by positivity
  have : (m : ℝ) < n := by exact_mod_cast h
  exact div_lt_div_of_pos_left (by norm_num) hm (by linarith)

end GolayHex

namespace Golay24

open GolayHex

/-! ## The readout on a codeword -/

/-- The coherence budget. -/
def Bbudget : ℝ := 10

/-- `TAX(v) = HW(v)·Y + ‖v‖²/8`.  For a 0/1 pattern `‖v‖² = HW(v)`. -/
noncomputable def tax (v : Word 24) : ℝ := (wt v : ℝ) * Y + (wt v : ℝ) / 8

/-- The tax of a pattern is the number of set cells times the activation
quantum. -/
theorem tax_eq (v : Word 24) : tax v = (wt v : ℝ) * Q := by
  unfold tax GolayHex.Q; ring

/-- A word costs nothing exactly when no cell is set. -/
theorem tax_eq_zero_iff (v : Word 24) : tax v = 0 ↔ v = 0 := by
  rw [tax_eq, ← wt_eq_zero_iff v]
  constructor
  · intro h
    rcases mul_eq_zero.mp h with h1 | h2
    · exact_mod_cast h1
    · exact absurd h2 (ne_of_gt Q_pos)
  · intro h; rw [h]; simp

/-- The coherence index `NRCI(v) = B / (B + TAX(v))`. -/
noncomputable def nrci (v : Word 24) : ℝ := Bbudget / (Bbudget + tax v)

theorem tax_nonneg (v : Word 24) : 0 ≤ tax v := by
  rw [tax_eq]
  have := Q_pos
  positivity

theorem nrci_eq_one_iff (v : Word 24) : nrci v = 1 ↔ v = 0 := by
  have hB : (0:ℝ) < Bbudget := by norm_num [Bbudget]
  have hpos : 0 < Bbudget + tax v := by have := tax_nonneg v; linarith
  rw [nrci, div_eq_one_iff_eq (ne_of_gt hpos)]
  constructor
  · intro h; exact (tax_eq_zero_iff v).mp (by linarith)
  · intro h; rw [(tax_eq_zero_iff v).mpr h]; ring

/-- More set cells means strictly less coherence. -/
theorem nrci_strictMono (u v : Word 24) (h : wt u < wt v) : nrci v < nrci u := by
  have hB : (0:ℝ) < Bbudget := by norm_num [Bbudget]
  have htu := tax_nonneg u
  have htv := tax_nonneg v
  have hlt : tax u < tax v := by
    rw [tax_eq, tax_eq]
    exact mul_lt_mul_of_pos_right (by exact_mod_cast h) Q_pos
  unfold nrci
  apply div_lt_div_of_pos_left hB (by linarith) (by linarith)

end Golay24

/-! ## Axiom audit -/

#print axioms GolayHex.readCost_le_amgm
#print axioms GolayHex.Y_lt_amgm
#print axioms GolayHex.nrci_calibrated
#print axioms GolayHex.nrci_ladder
#print axioms GolayHex.nrci_cal_strictAnti
#print axioms Golay24.tax_eq_zero_iff
#print axioms Golay24.nrci_strictMono
