import Mathlib

/-!
# Verified arithmetic identities used by `spatial_arithmetic.py`

The Python implementation performs floating-point geometry, so its tolerance
behaviour is tested in Python.  This file kernel-checks the exact algebraic
claims on which the node-count encoding and EML definition rely.
-/

set_option autoImplicit false

namespace SpatialArithmetic

/-- Number of vertices used for a non-negative integer operand. -/
def nonnegativeNodeCount (n : ℕ) : ℕ := 2 * n + 4

/-- Removing the two four-vertex offsets from two non-negative encodings
recovers the sum of their represented values. -/
theorem nodeCount_addition_identity (a b : ℕ) :
    (nonnegativeNodeCount a + nonnegativeNodeCount b - 8) / 2 = a + b := by
  change ((2 * a + 4) + (2 * b + 4) - 8) / 2 = a + b
  omega

/-- The non-negative vertex-count encoding is injective. -/
theorem nonnegativeNodeCount_injective : Function.Injective nonnegativeNodeCount := by
  intro a b h
  simp [nonnegativeNodeCount] at h
  exact h

/-- The real-valued exp-minus-log operator. -/
noncomputable def eml (x y : ℝ) : ℝ := Real.exp x - Real.log y

/-- EML at `(x, 1)` is the ordinary real exponential. -/
theorem eml_one_right (x : ℝ) : eml x 1 = Real.exp x := by
  simp [eml]

/-- EML at `(0, y)` is `1 - log y`. -/
theorem eml_zero_left (y : ℝ) : eml 0 y = 1 - Real.log y := by
  simp [eml]

end SpatialArithmetic

/-!
# Coordinate projection facts

These are the exact algebraic facts used by `dimension_projection.py`.
A coordinate projection selects entries using an explicit coordinate map; no
physical interpretation is part of these statements.
-/

namespace DimensionProjection

/-- Select coordinates from a finite binary vector. -/
def project {m n : ℕ} (coordinates : Fin n → Fin m) (x : Fin m → Bool) :
    Fin n → Bool := fun i => x (coordinates i)

/-- Coordinate projection commutes with pointwise XOR. -/
theorem project_xor {m n : ℕ} (coordinates : Fin n → Fin m)
    (x y : Fin m → Bool) :
    project coordinates (fun i => xor (x i) (y i)) =
      fun i => xor (project coordinates x i) (project coordinates y i) := by
  rfl

/-- Successive coordinate selections compose to one coordinate selection. -/
theorem project_comp {l m n : ℕ} (outer : Fin n → Fin m)
    (inner : Fin m → Fin l) (x : Fin l → Bool) :
    project outer (project inner x) = project (inner ∘ outer) x := by
  rfl

/-- An injective coordinate selection cannot increase Hamming weight. -/
theorem project_weight_le {m n : ℕ} (coordinates : Fin n → Fin m)
    (hinj : Function.Injective coordinates) (x : Fin m → Bool) :
    Fintype.card {i : Fin n // project coordinates x i = true} ≤
      Fintype.card {i : Fin m // x i = true} := by
  -- Define a function from {i : Fin n | project coordinates x i = true} to {i : Fin m | x i = true}
  -- For i with project coordinates x i = true, we have x (coordinates i) = true
  apply Fintype.card_le_of_injective (fun ⟨i, hi⟩ => ⟨coordinates i, by simp [project] at hi; exact hi⟩)
  intro ⟨i, hi⟩ ⟨j, hj⟩ h
  simp at h
  exact Subtype.ext (hinj h)

end DimensionProjection

/-!
# Hamming-lens facts

These facts justify reducing nearest-codeword questions by translation inside a
binary linear code: applying the same XOR translation to both vectors preserves
exactly the coordinates on which they differ.
-/

namespace DimensionMapping

/-- Coordinates on which two finite binary vectors differ. -/
def hammingSupport {n : ℕ} (x y : Fin n → Bool) : Finset (Fin n) :=
  Finset.univ.filter fun i => x i != y i

/-- A common XOR translation preserves the full Hamming support, not merely its
cardinality. -/
theorem hammingSupport_xor_translate {n : ℕ} (x y c : Fin n → Bool) :
    hammingSupport (fun i => xor (x i) (c i)) (fun i => xor (y i) (c i)) =
      hammingSupport x y := by
  ext i
  simp only [hammingSupport, Finset.mem_filter, Finset.mem_univ, true_and]
  cases x i <;> cases y i <;> cases c i <;> decide

/-- Consequently, a common XOR translation preserves Hamming distance. -/
theorem hammingDistance_xor_translate {n : ℕ} (x y c : Fin n → Bool) :
    (hammingSupport (fun i => xor (x i) (c i))
      (fun i => xor (y i) (c i))).card = (hammingSupport x y).card := by
  rw [hammingSupport_xor_translate]

end DimensionMapping

/-!
# MOG/Leech coordinate-address facts

These statements verify the exact indexing and family-count arithmetic used by
`mog_leech.py`.  They deliberately do not identify an arbitrary 4×6 layout
with a canonical historical MOG labelling.
-/

namespace MogLeech

/-- Row-major address of a coordinate in a 4×6 observer grid. -/
def row (i : Fin 24) : Fin 4 := ⟨i.val / 6, by omega⟩

def column (i : Fin 24) : Fin 6 := ⟨i.val % 6, Nat.mod_lt _ (by omega)⟩

/-- Decoding a row-major address recovers the original coordinate. -/
theorem address_roundtrip (i : Fin 24) :
    6 * (row i).val + (column i).val = i.val := by
  simpa [row, column, Nat.mul_comm] using (Nat.div_add_mod i.val 6)

/-- There are 1,104 signed minimal-vector numerators supported on pairs. -/
theorem pair_type_count : Nat.choose 24 2 * 4 = 1104 := by
  native_decide

/-- There are 97,152 signed octad-type numerators. -/
theorem octad_type_count : 759 * 128 = 97152 := by
  norm_num

/-- There are 98,304 odd-type numerators indexed by a codeword and coordinate. -/
theorem odd_type_count : 4096 * 24 = 98304 := by
  norm_num

/-- The three standard minimal-vector families total the kissing number. -/
theorem minimal_type_total : 1104 + 97152 + 98304 = 196560 := by
  norm_num

end MogLeech
