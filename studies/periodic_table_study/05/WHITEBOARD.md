# Blood Types as Information-Layer Probe - Whiteboard

## Study Goal (CORRECTED)

**NOT**: Explain blood types biologically  
**YES**: Use blood types as a **computational probe** to:
1. Test Advanced HexDictionary as an **information-layer decoder** (not similarity engine)
2. Investigate **OffBit information dynamics** - watch how an OffBit becomes "A+"

## Core Insight

Blood types are **fossilized toggle sequences** - the substrate's memory of what it cannot forget.

## The Real Question

**What is the OffBit "up to" before it becomes a biological object?**

## Study Architecture

### Phase 1: bit_to_blood.py
Pure OffBit lifecycle simulation (<30 lines):
```python
bit = OffBit()  # Start: Potential
bit = toggle(bit)  # Toggle A-antigen
bit, absorbed = restore_coherence(bit, Y_CONSTANT)
# If absorbed=False and δ < 0.001 → bit.history = "A-toggle"
bit = toggle(bit)  # Toggle RhD
bit, absorbed = restore_coherence(bit, Y_CONSTANT)
# If absorbed=False and δ < 0.001 → bit.history = "A-toggle, RhD-toggle"
bit = bit * O_OBSERVER  # Observer binding
# Output: "I am A+"
```

### Phase 2: hex_dictionary_decoder.py
Refactor HexDictionary to decode toggle history:
```python
hex_dict.decode("A+")
# → ToggleHistory([
#      ("A-gene", "toggle", δ=0.0009, absorbed=False),
#      ("RhD",   "toggle", δ=0.0009, absorbed=False),
#      ("OBS",   "bind",   cost=O_observer)
#    ])
```

Each of the 8 HexDictionary methods becomes a different lens on the same history:
- **Hamming**: raw bit flips
- **Spectral**: toggle rhythm
- **Topological**: persistence of δ-deficit
- **Coherence-Aware**: which steps survived GLR
- etc.

### Phase 3: Why Only 8?
Test hypothesis: Only 8 toggle patterns (3 binary toggles: A, B, RhD) survive `restore_coherence()` without GLR absorption at δ < 0.001.

This is the substrate's native instruction set for stable dissidence.

## Key Concepts from UBP 3.5

### CoherenceState
Every value is a `CoherenceState` object - self-aware, carries:
- value
- NRCI (Non-Random Coherence Index)
- operational history

### OffBit
24-bit coherence-native state. Not just a bit pattern - a coherence state with 24-bit representation.

### Toggle Operation
Not just bit flip - a **coherence transformation** that applies Y-refinement.

### restore_coherence()
The critical filter - determines if a toggle pattern survives or gets absorbed by GLR.

## Expected Findings

1. **8 Patterns Survive**: Only A-on/off, B-on/off, RhD-on/off combinations maintain δ < 0.001
2. **HexDictionary as Decoder**: Each method reveals different aspect of toggle history
3. **Substrate Syntax**: Blood types prove the substrate has a native instruction set
4. **Biology as Fluent Reader**: Biology didn't invent blood types - it discovered them

## Paper Structure

**Title**: "Blood Types as Fossilized Toggle Sequences: Decoding the OffBit's Information Layer"

**Abstract**: 
> This study uses the human ABO/Rh system as a computational probe of the OffBit's information layer. We do not analyze blood types as biological phenotypes, but as fossilized toggle sequences in the coherence substrate. Using the upgraded HexDictionary—not as a similarity engine, but as a toggle-history decoder—we reconstruct the minimal information pathway from OffBit() to stable antigen expression.
> 
> Our analysis reveals that all eight blood types correspond to the only eight 3-bit toggle patterns that survive restore_coherence() without triggering GLR absorption at δ < 0.001. This is not a biological classification—it is the substrate's native instruction set for stable dissidence.
> 
> In this view, the HexDictionary's eight methods are not analytical tools, but eight perspectives on the same geometric truth: how the substrate remembers what it cannot forget.

## Progress Tracker

- [x] Phase 1: Re-read UBP 3.5 Manual
- [ ] Phase 2: Create bit_to_blood.py
- [ ] Phase 3: Create hex_dictionary_decoder.py
- [ ] Phase 4: Analyze all 8 blood types as toggle sequences
- [ ] Phase 5: Test why only 8 survive
- [ ] Phase 6: Write substrate-first paper
- [ ] Phase 7: Compile final deliverables
