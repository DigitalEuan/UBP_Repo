/-
Universal Binary Principle — formally checked mathematical core
===============================================================

This file deliberately separates three kinds of statement:

  * THEOREM: proved below by Lean's kernel.
  * DEFINITION: a chosen model or score; consistency is provable, but choosing
    the definition does not make it a law of nature.
  * EMPIRICAL/PROVISIONAL: comparisons with measured constants in the Python
    companion.  Those comparisons are tests, not derivations from physics.

The formal core covers binary linear encoding/syndromes, Hamming distance,
Gray code, the rational NRCI score, weighted harmonic quality, and exact
rational identities used by the script.  It does not claim that a numerical
fit establishes a physical theory, nor that the reduced Leech/Monster labels
in the Python program construct those full mathematical objects.
-/

import Mathlib

open scoped BigOperators

namespace UBP

/-! ## 1. Binary arithmetic -/

/-- A bit is the field with two elements. Addition is XOR. -/
abbrev Bit := ZMod 2

/-- A fixed-width word. `Fin n` makes out-of-range indexing impossible. -/
abbrev Word (n : ℕ) := Fin n → Bit

/-- Hamming weight: the number of nonzero coordinates. -/
def hammingWeight {n : ℕ} (x : Word n) : ℕ :=
  (Finset.univ.filter fun i => x i ≠ 0).card

/-- Hamming distance is the weight of the coordinatewise difference. -/
def hammingDistance {n : ℕ} (x y : Word n) : ℕ :=
  hammingWeight (x - y)

/-- THEOREM: every word has distance zero from itself. -/
theorem hammingDistance_self {n : ℕ} (x : Word n) :
    hammingDistance x x = 0 := by
  simp [hammingDistance, hammingWeight]

/-- THEOREM: Hamming distance is symmetric. -/
theorem hammingDistance_comm {n : ℕ} (x y : Word n) :
    hammingDistance x y = hammingDistance y x := by
  simp only [hammingDistance, hammingWeight]
  congr 1
  ext i
  simp only [Finset.mem_filter, Finset.mem_univ, true_and,
    Pi.sub_apply, sub_ne_zero]
  exact ne_comm

/-! ## 2. A transparent systematic binary code

A codeword is represented as two `n`-bit halves.  Given a binary matrix `B`,
encoding is `[m | Bm]`.  The matching parity check computes `Bm + right`.
Because addition in `ZMod 2` is XOR, every encoded word has zero syndrome.
This theorem is generic: it does not rely on a hard-coded Golay matrix.
-/

structure Codeword (n : ℕ) where
  left : Word n
  right : Word n

/-- DEFINITION: systematic encoding `[m | Bm]`. -/
def encode {n : ℕ} (B : Matrix (Fin n) (Fin n) Bit) (m : Word n) :
    Codeword n :=
  ⟨m, B.mulVec m⟩

/-- DEFINITION: parity-check syndrome for the block matrix `[B | I]`. -/
def syndrome {n : ℕ} (B : Matrix (Fin n) (Fin n) Bit)
    (c : Codeword n) : Word n :=
  B.mulVec c.left + c.right

/-- THEOREM: systematic encoding always satisfies its matching parity check. -/
theorem syndrome_encode_zero {n : ℕ}
    (B : Matrix (Fin n) (Fin n) Bit) (m : Word n) :
    syndrome B (encode B m) = 0 := by
  ext i
  change B.mulVec m i + B.mulVec m i = 0
  have htwo : (2 : Bit) = 0 := by decide
  calc
    B.mulVec m i + B.mulVec m i = 2 • B.mulVec m i :=
      (two_nsmul (B.mulVec m i)).symm
    _ = (2 : Bit) * B.mulVec m i := nsmul_eq_mul 2 (B.mulVec m i)
    _ = 0 * B.mulVec m i := by rw [htwo]
    _ = 0 := zero_mul _

/-- THEOREM: encoding is injective because the message is retained verbatim. -/
theorem encode_injective {n : ℕ} (B : Matrix (Fin n) (Fin n) Bit) :
    Function.Injective (encode B) := by
  intro x y h
  have hleft := congrArg Codeword.left h
  simpa [encode] using hleft

/-! ## 3. Gray code

The executable Python uses `n XOR (n >> 1)`.  The natural-number definition
below is the same formula.  Concrete regression values are kernel checked.
-/

/-- DEFINITION: binary-reflected Gray encoding. -/
def gray (n : ℕ) : ℕ := n ^^^ (n >>> 1)

/-- THEOREM (finite exact checks): the first eight Gray values are standard. -/
theorem gray_first_eight :
    List.map gray (List.range 8) = [0, 1, 3, 2, 6, 7, 5, 4] := by
  native_decide

/-! ## 4. Rational stability score (NRCI)

`nrci α t = 10 / (10 + αt)` is a chosen dimensionless score.  The next
results prove its basic mathematical behavior for nonnegative tax and scale.
They do not prove that the score measures a physical quantity.
-/

/-- DEFINITION: exact rational NRCI used by the core script. -/
def nrci (alpha tax : ℚ) : ℚ := 10 / (10 + alpha * tax)

/-- THEOREM: NRCI is positive for nonnegative parameters. -/
theorem nrci_pos {alpha tax : ℚ} (ha : 0 ≤ alpha) (ht : 0 ≤ tax) :
    0 < nrci alpha tax := by
  rw [nrci]
  positivity

/-- THEOREM: NRCI never exceeds one for nonnegative parameters. -/
theorem nrci_le_one {alpha tax : ℚ} (ha : 0 ≤ alpha) (ht : 0 ≤ tax) :
    nrci alpha tax ≤ 1 := by
  rw [nrci]
  apply (div_le_one (by positivity : (0 : ℚ) < 10 + alpha * tax)).2
  nlinarith [mul_nonneg ha ht]

/-- THEOREM: with positive tax, increasing `alpha` strictly lowers NRCI. -/
theorem nrci_strictAnti_alpha {a b tax : ℚ}
    (ha : 0 ≤ a) (hab : a < b) (ht : 0 < tax) :
    nrci b tax < nrci a tax := by
  rw [nrci, nrci]
  have hda : 0 < (10 : ℚ) + a * tax := by positivity
  have hdb : 0 < (10 : ℚ) + b * tax := by
    have hb : 0 < b := lt_of_le_of_lt ha hab
    positivity
  apply (div_lt_div_iff₀ hdb hda).2
  nlinarith

/-- THEOREM: zero tax gives perfect score, independently of scale. -/
theorem nrci_zero_tax (alpha : ℚ) : nrci alpha 0 = 1 := by
  norm_num [nrci]

/-! ## 5. Weighted harmonic quality index

The weights 2/5, 2/5, 1/5 are design choices.  For positive component scores
at most one, the harmonic aggregate is itself positive and at most one.
-/

/-- DEFINITION: weighted harmonic mean used as the exact DQI core. -/
def dqi (n u g : ℚ) : ℚ :=
  1 / ((2 / 5 : ℚ) / n + (2 / 5 : ℚ) / u + (1 / 5 : ℚ) / g)

/-- THEOREM: the denominator of DQI is positive on positive inputs. -/
theorem dqi_den_pos {n u g : ℚ} (hn : 0 < n) (hu : 0 < u) (hg : 0 < g) :
    0 < (2 / 5 : ℚ) / n + (2 / 5 : ℚ) / u + (1 / 5 : ℚ) / g := by
  positivity

/-- THEOREM: DQI is positive on positive inputs. -/
theorem dqi_pos {n u g : ℚ} (hn : 0 < n) (hu : 0 < u) (hg : 0 < g) :
    0 < dqi n u g := by
  rw [dqi]
  exact one_div_pos.mpr (dqi_den_pos hn hu hg)

/-- THEOREM: if all three inputs are in `(0,1]`, then DQI is at most one. -/
theorem dqi_le_one {n u g : ℚ}
    (hn : 0 < n) (hn1 : n ≤ 1)
    (hu : 0 < u) (hu1 : u ≤ 1)
    (hg : 0 < g) (hg1 : g ≤ 1) :
    dqi n u g ≤ 1 := by
  rw [dqi, one_div]
  apply (inv_le_one₀ (dqi_den_pos hn hu hg)).2
  have hn' : 1 ≤ 1 / n := (le_div_iff₀ hn).2 (by simpa)
  have hu' : 1 ≤ 1 / u := (le_div_iff₀ hu).2 (by simpa)
  have hg' : 1 ≤ 1 / g := (le_div_iff₀ hg).2 (by simpa)
  calc
    1 = (2 / 5 : ℚ) * 1 + (2 / 5) * 1 + (1 / 5) * 1 := by norm_num
    _ ≤ (2 / 5) * (1 / n) + (2 / 5) * (1 / u) + (1 / 5) * (1 / g) := by
      gcongr
    _ = _ := by ring

/-- Exact regression check corresponding to scores 0.8, 0.7 and 0.9. -/
theorem dqi_regression : dqi (4 / 5) (7 / 10) (9 / 10) = 126 / 163 := by
  norm_num [dqi]

/-! ## 6. Exact rational geometry

The executable uses integer/rational coordinates so that geometric operations
such as squared norm are exact.  This is a sound way to avoid floating-point
drift.  A geometric representation still has to be distinguished from a
proof that the represented object has a claimed physical interpretation.
-/

/-- A point in exact 24-dimensional rational coordinate space. -/
abbrev Point24 := Fin 24 → ℚ

/-- DEFINITION: exact Euclidean squared norm; no square root or float needed. -/
def normSq24 (p : Point24) : ℚ := ∑ i, p i ^ 2

/-- A canonical support-eight point with coordinate `2` on its support. -/
def canonicalOctadPoint : Point24 := fun i => if i.val < 8 then 2 else 0

/-- THEOREM: its exact squared norm is `8 * 2² = 32`. -/
theorem canonicalOctadPoint_normSq : normSq24 canonicalOctadPoint = 32 := by
  native_decide

/-! ## 7. Exact arithmetic identities used by numerical routines -/

/-- THEOREM: the population variance of `[2,4,4,4,5,5,7,9]` is exactly 4. -/
theorem variance_regression :
    let xs : Fin 8 → ℚ := ![2, 4, 4, 4, 5, 5, 7, 9]
    let mean := (∑ i, xs i) / 8
    (∑ i, (xs i - mean) ^ 2) / 8 = 4 := by
  norm_num [Fin.sum_univ_succ]

/-- THEOREM: the integer-square-root regression used by the Python suite. -/
theorem sqrt_196560 : Nat.sqrt 196560 = 443 := by
  native_decide

/-- THEOREM: a representative modular-power regression. -/
theorem modpow_regression : 7 ^ 100 % 13 = 9 := by
  native_decide

/-! ## Scope boundary

The Python companion additionally contains:

  * exhaustive and randomized software tests of its concrete Golay table;
  * finite constructions labelled with Leech/Barnes–Wall/Monster terminology;
  * formula-to-observation comparisons called particle-physics predictions.

Those are not silently promoted to Lean theorems here.  A full formal proof
about the extended Golay code would require formalizing the concrete matrix
and proving its minimum distance.  A full Leech-lattice or Monster-group
claim would require their actual mathematical definitions.  Physical claims
require empirical methodology beyond proof of algebraic identities.
-/

end UBP
