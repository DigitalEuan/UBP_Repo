import GolayTiles.Substrate

/-!
# Selectional slots on the code

The linguistic layer that sits on the Golay substrate: a verb's requirements
for one argument slot as sets of MOG cells, and the *violation pattern* they
produce, which is a word of the code.  This is not part of the tile
mathematics — `GolayTiles/` holds that — but it is what the rest of the
language development means by a violation.

* `licensed_iff` — a slot is licensed (empty violation set) exactly when the
  argument meets every requirement and supplies nothing forbidden.
-/

namespace GLM

open Golay24

/-! ## 7. The semantic layer -/

/-- What a verb expects of one argument slot, and what the argument supplies.
All three are sets of MOG cells. -/
structure Slot where
  /-- cells the verb needs the argument to carry -/
  required : Finset (Fin 24)
  /-- cells the verb never takes in this slot -/
  forbidden : Finset (Fin 24)
  /-- cells the argument actually carries -/
  provision : Finset (Fin 24)

/-- The violated cells: what the verb needs and the argument lacks, together
with what the argument brings and the verb refuses. -/
def Slot.violated (s : Slot) : Finset (Fin 24) :=
  (s.required \ s.provision) ∪ (s.provision ∩ s.forbidden)

/-- The violation pattern as a word of the substrate. -/
def Slot.pattern (s : Slot) : Word 24 := fun j => if j ∈ s.violated then 1 else 0

theorem Slot.wt_pattern (s : Slot) : wt s.pattern = s.violated.card := by
  classical
  unfold wt Slot.pattern
  congr 1
  ext j
  by_cases h : j ∈ s.violated <;> simp [h]

/-- A slot is licensed exactly when the argument meets every requirement and
supplies nothing forbidden. -/
theorem licensed_iff (s : Slot) :
    s.violated = ∅ ↔ s.required ⊆ s.provision ∧ Disjoint s.provision s.forbidden := by
  constructor
  · intro h
    rw [Slot.violated, Finset.union_eq_empty] at h
    obtain ⟨h1, h2⟩ := h
    refine ⟨?_, ?_⟩
    · intro x hx
      by_contra hn
      exact absurd (Finset.mem_sdiff.mpr ⟨hx, hn⟩) (by simp [h1])
    · rw [Finset.disjoint_iff_inter_eq_empty]; exact h2
  · rintro ⟨h1, h2⟩
    rw [Slot.violated, Finset.union_eq_empty]
    constructor
    · rw [Finset.sdiff_eq_empty_iff_subset]; exact h1
    · rwa [← Finset.disjoint_iff_inter_eq_empty]

end GLM

/-! ## Axiom audit -/

#print axioms GLM.licensed_iff
