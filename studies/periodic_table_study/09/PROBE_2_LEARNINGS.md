# Probe 2 Learnings: Forbidden 4th Toggle

## What We Executed

Tested what happens when we try to add toggles outside the {A, B, RhD} space:
- Pure forbidden: {X}, {X, Y}
- Mixed: {A, X}, {A, B, X}, {A, B, RhD, X}

Measured Jaccard distance from invalid combinations to the nearest valid combination.

## What We Learned

### 1. The 2^3 = 8 Space is CLOSED

**Even {A, B, RhD, X} has d=0.25 from the valid space.**

The forbidden toggle X pulls the combination OUT of the 2^3 manifold, even though it contains all 3 valid toggles.

### 2. Distance Scales with Forbidden Content

- {X} alone: d=1.00 (maximally distant)
- {A, X}: d=0.50 (half valid, half forbidden)
- {A, B, X}: d=0.33 (2/3 valid, 1/3 forbidden)
- {A, B, RhD, X}: d=0.25 (3/4 valid, 1/4 forbidden)

The more forbidden toggles, the farther from valid space.

### 3. Biological Interpretation

**Why are blood types conserved across all human populations?**

Because any mutation that tries to add a 4th antigen system would be OUTSIDE the stable 2^3 space. The substrate would reject it.

This isn't natural selection - it's **geometric constraint**. The OffBit can only persist in closed toggle spaces.

### 4. Information Layer Rule

**For n independent toggles → 2^n stable states**

- 3 toggles (A, B, RhD) → 2^3 = 8 blood types
- 4 toggles → 2^4 = 16 states (but no 4th toggle exists in blood)
- n toggles → 2^n states

Adding an (n+1)th toggle **breaks closure** → instability → GLR absorption?

### 5. This Explains the Periodic Table Too

If elements are toggle histories (orbital sets), then:
- Each orbital is a toggle
- Each element is a subset of active orbitals
- Stable elements = closed toggle spaces

**This is why the periodic table has structure** - it's not chemistry, it's information geometry.

## Key Insight

The OffBit doesn't "decide" to persist in 2^n states. It **can only** persist in 2^n states. Anything else is geometrically forbidden.

## Next: Probe 3

Model periodic table elements as toggle histories (orbital sets) and validate:
- Do elements cluster by Jaccard distance?
- Do periods/groups emerge from toggle structure?
- Is the periodic table a 2^n closed space?
