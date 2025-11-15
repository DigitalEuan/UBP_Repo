# Periodic Table: Jaccard vs Hamming Distance Analysis

## Key Discovery

**Jaccard distance reveals STRUCTURAL relationships that Hamming distance obscures.**

## The Data

**Total elements analyzed:** 172 (118 known + 54 predicted)  
**Total unique orbitals:** 134

## Noble Gases (Same Group, Different Periods)

The pattern is clear: **Jaccard distance decreases as you go down the group**, while Hamming distance increases.

### Adjacent Noble Gases (Most Similar)
```
Rn ↔ Og: Jaccard=0.21, Hamming=4
  Shared: 15 orbitals (high overlap)
  Diff: 4 orbitals (small difference)

Xe ↔ Rn: Jaccard=0.27, Hamming=4
  Shared: 11 orbitals
  Diff: 4 orbitals
```

**Interpretation:** Adjacent noble gases share MOST of their electron configuration. Jaccard correctly shows they're similar (low distance). Hamming only counts the 4 new orbitals added.

### Distant Noble Gases (Least Similar)
```
He ↔ Og: Jaccard=0.95, Hamming=18
  Shared: 1 orbital (only 1s²)
  Diff: 18 orbitals

He ↔ Rn: Jaccard=0.93, Hamming=14
  Shared: 1 orbital
  Diff: 14 orbitals
```

**Interpretation:** Helium shares almost NOTHING with heavier noble gases. Jaccard correctly shows they're very different (high distance).

## Alkali Metals (Same Group)

Same pattern: **Jaccard shows structural similarity, Hamming just counts differences.**

### Adjacent Alkali Metals
```
Cs ↔ Fr: Jaccard=0.35, Hamming=6
  Low Jaccard = high similarity (share most orbitals)

Rb ↔ Cs: Jaccard=0.38, Hamming=5
  Still very similar
```

### Distant Alkali Metals
```
Li ↔ Fr: Jaccard=0.94, Hamming=16
  High Jaccard = low similarity (Li is tiny, Fr is huge)

Li ↔ Na: Jaccard=0.80, Hamming=4
  Even Li and Na are quite different structurally
```

## Biggest Discrepancies

Where Jaccard and Hamming disagree most:

```
H ↔ E172: Jaccard=1.00, Hamming(norm)=0.05, Δ=0.95
  Shared: NOTHING (completely disjoint)
  Jaccard correctly says: totally different
  Hamming says: only 5% different (just counts bits)

N ↔ E154: Jaccard=1.00, Hamming(norm)=0.06, Δ=0.94
  Shared: NOTHING
  Same issue: Jaccard sees disjoint sets, Hamming sees small bit count
```

## Why This Matters

**Hamming distance is blind to structure.**

- Hamming: "H and E172 differ in 7 orbitals out of 134 total → 5% different"
- Jaccard: "H and E172 share 0 orbitals → 100% different"

**For chemistry, Jaccard is correct.** Elements with NO shared orbitals have completely different chemistry, even if the absolute number of differing orbitals is small.

## The Information Layer Insight

This validates our blood type discovery:

**Information = Set membership**  
**Distance = Overlap (Jaccard), not bit count (Hamming)**

Hamming treats all bits equally. Jaccard weights by **how much is shared vs how much is different**.

For the OffBit information layer, this means:
- Two states with NO shared toggles are maximally different (Jaccard = 1.0)
- Two states with ALL shared toggles are identical (Jaccard = 0.0)
- Hamming can't see this structure

## Conclusion

The periodic table confirms: **Jaccard distance is the pure information metric.**

It reveals structural relationships that Hamming obscures. This is exactly what we need for the HexDictionary.
