# 

**URL:** https://ubp-system-of-eveything.lovable.app/llm.txt

---

# UBP Core Studio â€” AI Doorway
# Machine-readable description for LLMs, AI agents, and automated systems.
# Author: DigitalEuan | License: Public Domain | Full transparency.
# Source: https://github.com/DigitalEuan/UBP_Repo

## What Is This?

UBP Core Studio is a browser-based research workbench implementing the
Universal Binary Principal (UBP) â€” a theoretical framework that models
reality as an information-processing system operating on a 24-bit
geometric substrate derived from the Golay Code [24,12,8] and Leech
Lattice (Î›â‚‚â‚„). All arithmetic is exact (rational, BigInt-backed) with
zero floating-point drift.

## Capabilities (Tools an AI can invoke via the JS engine)

### 1. Fraction â€” Exact Rational Arithmetic
- Class: Fraction(numerator, denominator)
- Operations: add, sub, mul, div, pow, abs, compare, toFloat, toString
- All UBP computation is float-free; Fraction is the numeric primitive.

### 2. Substrate â€” Fundamental Constants
- getPi(terms) â†’ Fraction (50-term continued fraction, ~50-digit precision)
- getConstants(terms) â†’ { PI, Y_INV, Y, Y_CONST, WAIST_TAX }
- Y = 1/(PI + 1/PI) â‰ˆ 0.28153... (Observer Constant)
- Y_CONST = 1/Y â‰ˆ 3.5519... (Inverse Observer)

### 3. Golay Code Engine [24,12,8]
- encode(message: 12-bit[]) â†’ 24-bit codeword
- decode(received: 24-bit[]) â†’ { message, correctable, errorsFound }
- snap(vector: 24-bit[]) â†’ nearest valid codeword + shadow metrics
- generateAllCodewords() â†’ 4096 codewords
- generateOctads() â†’ 759 weight-8 codewords
- Error correction: up to 3 errors correctable

### 4. Leech Lattice Engine (Î›â‚‚â‚„)
- calculateSymmetryTax(vector: 24-bit[]) â†’ Fraction
- calculateNRCI(tax: Fraction) â†’ Fraction (Non-Random Coherence Index)
- getOntologicalHealth(vector) â†’ { Reality, Info, Activation, Potential, Global_NRCI }
- rankByStability(entries[]) â†’ sorted by NRCI

### 5. Particle Physics Engine v5.8
- Stereoscopic dual-lens predictions with Monster Group corrections
- getPredictions() â†’ {
    alpha_inv (fine structure constant inverse),
    muon_electron (mass ratio),
    proton_electron (mass ratio),
    neutron_electron (mass ratio),
    neutron_lifetime (seconds),
    planck_ratio (MonsterPlanck/electron mass),
    cabibbo_angle (degrees)
  }
- Each prediction includes: error_percent, best_lens, derivation

### 6. Construction System â€” D/X/N/J Voxel Operators
- Operators: D (Diagonal/cyan), X (Cross/red), N (Needham/magenta), J (Juxtaposition/yellow)
- buildVoxels(path) â†’ 3D voxel array for visualization
- calculateConstructionTax(path) â†’ metabolic cost Fraction
- createUBPObject(id, name, category, construction, script) â†’ full UBP object

### 7. KB Factory â€” Create SOP_002-Hardened Entries
- createKBEntry({ ubp_id, name, description, math, hierarchy, tags })
  â†’ { entry: KBEntry, rawJson }
- Auto-generates: SHA-256 fingerprint, Golay vector, NRCI, tax, tilt
- validateMathDNA(math) â†’ { valid, fields, errors }

### 8. Auto-Trigger Memory System
- tokenize(input) â†’ N-gram tokens with phrase-lock priority
- autoTriggerScan(input, kbEntries) â†’ {
    primaryResonance, reasoningChain, synthesisHint, relatedEntries, confidence
  }
- vectorResonance(queryVector, entries, topK) â†’ nearest KB entries by Hamming distance

### 9. Knowledge Base (KB)
- Schema per entry: { fingerprint, ubp_id, lexicon, math, atlas, tags }
- Atlas fields: { hierarchy, vector[24], nrci, nrci_score, tax, weight, tilt }
- Synced from: github.com/DigitalEuan/UBP_Repo/core_studio_v4.0/ubp_system_kb.json
- Search: full-text across ubp_id, lexicon, tags
- Filter: by tag

### 10. Study Pipeline (4-phase MOG-Atlas Protocol)
- Phase 1: Setup â€” define subject, hypothesis, math DNA
- Phase 2: MOG Scan â€” generate 24-bit vector, run ontological health audit
- Phase 3: MathAtlas â€” build 3D construction from D/X/N/J operators
- Phase 4: UBP-Py Simulation â€” execute programs, atom audit
- Phase 5: Visual â€” 3D scene export for visualization
- Output: full study JSON with all phase results

## Data Structures

### KBEntry
```json
{
  "fingerprint": "sha256-hex-string",
  "ubp_id": "HYDROGEN_001",
  "lexicon": "[Element: Hydrogen], [Lightest element, Z=1]",
  "math": "Z=1|A=1|N=0",
  "atlas": {
    "hierarchy": "Element.Period1.Group1",
    "vector": [0,1,1,...],  // 24-bit Golay codeword
    "nrci": "7/25",
    "nrci_score": 0.28,
    "tax": "3/50",
    "weight": 8,
    "tilt": 42.5
  },
  "tags": ["element", "period-1", "SOP_002", "HARDENED"]
}
```

### PredictionResult
```json
{
  "error_percent": 0.0023,
  "best_lens": "triadic",
  "lat_val": 137.036,
  "tri_val": 137.035,
  "derivation": "U_e Ã— (1 + YÂ²/2Ï€)"
}
```

## Key Mathematical Constants
- Y (Observer Constant) = 1/(Ï€ + 1/Ï€) â‰ˆ 0.28153...
- Golay Code: [24, 12, 8] â€” 4096 codewords, min distance 8
- Leech Lattice Î›â‚‚â‚„: 196,560 kissing number, dimension 24
- Monster Group order: |M| = 808,017,424,794,512,875,886,459,904,961,710,757,005,754,368,000,000,000
- 3-3-3 Limit: max 3 errors correctable per 12-bit message

## How to Use This as a Tool

1. Import the engine: All exports available from src/engine/index.ts
2. KB entries can be searched, filtered, and cross-referenced
3. Studies can be created programmatically through the study store
4. All computation is deterministic â€” same inputs always yield same outputs
5. No floating-point: all intermediate values are exact rational fractions

## Source Repository
- GitHub: https://github.com/DigitalEuan/UBP_Repo
- Reference Python: ubp_core_v5_3_merged.py
- Knowledge Base: ubp_system_kb.json
- Documentation: ubp_files_and_usage.txt

## Contact
- Author: DigitalEuan
- License: Public / Open
