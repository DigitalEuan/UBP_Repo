# Probe 1 Learnings: Blood Types as Toggle Sets

## What We Executed

Treated all 8 blood types as pure toggle sets:
- O- = ∅ (empty set)
- O+ = {RhD}
- A- = {A}
- A+ = {A, RhD}
- B- = {B}
- B+ = {B, RhD}
- AB- = {A, B}
- AB+ = {A, B, RhD}

Computed Jaccard distance matrix for all pairs.

## What We Learned

### 1. Blood Types ARE 2^3 Toggle Combinations

The 8 blood types are exactly the 8 possible subsets of {A, B, RhD}. This is not a biological coincidence - it's a **mathematical necessity** if you have 3 independent binary toggles.

### 2. Jaccard Distance Reveals Information Structure

**Closest pairs** (d=0.33):
- A+ ↔ AB+: share {A, RhD}, differ only in B
- B+ ↔ AB+: share {B, RhD}, differ only in A  
- AB- ↔ AB+: share {A, B}, differ only in RhD

**Farthest pairs** (d=1.00):
- O- ↔ AB+: disjoint sets (empty vs full)
- A- ↔ B-: disjoint sets (no overlap)
- O+ ↔ AB-: disjoint sets

### 3. "Similarity" = Shared Toggle History

Two blood types are "similar" if they share toggles, **regardless of what those toggles biochemically mean**.

- A+ and B+ share RhD → d=0.67 (moderately similar)
- A+ and AB+ share {A, RhD} → d=0.33 (very similar)

This is **information geometry**, not chemistry.

### 4. The Empty Set (O-) is Maximally Different from Everything

O- has d=1.00 with all other blood types except itself. This makes sense: it shares NO toggles with anything.

### 5. Validation of Information-First Perspective

Blood types are not defined by:
- Antigen presence/absence (that's biochemistry)
- Hamming distance (that's bit-counting)

They're defined by:
- **Which toggles are in the set**
- **How much overlap exists between sets**

This is pure set theory. The OffBit information layer is **set-theoretic**, not geometric or spectral.

## Key Insight

**The HexDictionary doesn't need 8 methods. It needs ONE: Jaccard distance on toggle sets.**

## Next Question

What happens if we try a **forbidden 4th toggle**? 

If blood types are stable because they're 2^3 subsets, what happens when we try {A, B, RhD, X}?

Does the substrate reject it? Does GLR absorb it? Does NRCI collapse?

**Probe 2 will test this.**
