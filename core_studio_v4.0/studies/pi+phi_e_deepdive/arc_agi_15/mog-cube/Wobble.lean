import GolayTiles.Cost

/-!
# The wobble and the thirteen sinks

Two side claims from the original brief that are *not* part of the Golay tile
mathematics, kept here so that the standalone tile set (`GolayTiles/`) contains
only the code, the tiling and their prices.

* `sinks_balance` — thirteen sinks carry the wobble `frac(π·φ·e)` exactly.  The
  number thirteen is a stipulation of the brief, not a consequence of the code,
  of `M₂₄`, or of the tiling.
* `no_algebraic_growth_of_e` — `e` is not the growth ratio of a finite integer
  substitution, given its transcendence as an explicit hypothesis (Mathlib does
  not carry that fact).
-/

open Real

namespace GolayHex

/-! ## The thirteen sinks -/

/-- The wobble: the amount by which the compound loop `π·φ·e` fails to close. -/
noncomputable def wobble : ℝ := Int.fract (π * goldenRatio * Real.exp 1)

/-- The charge carried by each of the thirteen sinks. -/
noncomputable def sinkL : ℝ := wobble / 13

/-- The conservation law of the tiling: thirteen sinks carry the wobble
exactly.  (That the number is thirteen is a stipulation; nothing in the code,
in `M₂₄`, or in the tiling forces it.) -/
theorem sinks_balance : 13 * sinkL = wobble := by
  unfold sinkL; ring

theorem wobble_mem : 0 ≤ wobble ∧ wobble < 1 :=
  ⟨Int.fract_nonneg _, Int.fract_lt_one _⟩

/-! ## What `e` would have to be -/

/-- **`e` cannot be an assembly growth ratio while it is transcendental.**  A
growth ratio of a finite integer substitution is a root of the characteristic
polynomial of an integer matrix, hence algebraic.  Mathlib does not (yet) carry
the transcendence of `e`, so it is an explicit hypothesis here: the label
`[open]` stays on it. -/
theorem no_algebraic_growth_of_e
    (he : Transcendental ℚ (Real.exp 1))
    (p : Polynomial ℚ) (hp : p ≠ 0) :
    Polynomial.aeval (Real.exp 1) p ≠ 0 := by
  intro h
  exact he ⟨p, hp, h⟩

end GolayHex

/-! ## Axiom audit -/

#print axioms GolayHex.sinks_balance
#print axioms GolayHex.wobble_mem
#print axioms GolayHex.no_algebraic_growth_of_e
