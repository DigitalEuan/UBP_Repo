# Feature Specification: D-Variables for Symbol Coherence Analysis

**Document Version**: 1.0  
**Date**: Nov 18, 2025  
**Author**: Manus AI  
**Study**: UBP Symbol Study Phase 2 (Refined)

---

## Overview

This document provides **precise, operational definitions** for the 8-dimensional feature vector (D1–D8) used to characterize mathematical and computational symbols in the UBP Symbol Study. All definitions are normalized to the range [0, 1] for modeling consistency.

These definitions are **deterministic and replicable**: given a symbol's metadata and formal definition, any researcher can compute identical D-values.

---

## D1: Arity (Normalized)

**Definition**: The number of arguments a symbol accepts, normalized to [0, 1].

**Computation**:
```
arity_raw = count of arguments (0, 1, 2, 3, ...)
D1 = min(arity_raw / 2.0, 1.0)
```

**Mapping**:
- Nullary (constants): D1 = 0.0
- Unary (functions of one argument): D1 = 0.5
- Binary (functions of two arguments): D1 = 1.0
- Ternary and higher: D1 = 1.0 (capped)

**Example**:
- `π` (constant): D1 = 0.0
- `sin(x)`: D1 = 0.5
- `a + b`: D1 = 1.0
- `if(cond, then, else)`: D1 = 1.0

**Rationale**: Arity reflects structural complexity. Higher arity generally correlates with increased cognitive load.

---

## D2: Formal Role (Categorical → Numeric)

**Definition**: The syntactic category of the symbol within formal expressions, mapped to a numeric scale.

**Mapping** (fixed, deterministic):
```
{
  "operand":    0.00,  # Constants, variables
  "relation":   0.25,  # Equality, inequality, membership
  "operator":   0.50,  # Arithmetic, logical, algebraic operators
  "quantifier": 0.75,  # ∀, ∃, Σ, ∏
  "meta":       1.00   # Proof operators, type constructors
}
```

**Computation**:
```
D2 = role_map[symbol.formal_role]
```

**Example**:
- `x` (variable): D2 = 0.00
- `=` (equality): D2 = 0.25
- `+` (addition): D2 = 0.50
- `∀` (universal quantifier): D2 = 0.75
- `⊢` (entailment): D2 = 1.00

**Rationale**: Formal role reflects the symbol's position in the syntactic hierarchy. Higher roles (quantifiers, meta-operators) impose greater interpretive demands.

---

## D3: Invertibility (Reversibility Fraction)

**Definition**: The fraction of contexts in which the symbol admits an inverse operation.

**Computation**:
```
contexts_total = count of formal contexts where symbol appears
contexts_invertible = count where inverse exists and is well-defined
D3 = contexts_invertible / contexts_total
```

**Practical Approximation** (for this study):
```
if symbol has well-defined inverse (e.g., +/−, ×/÷, ∧/¬∧):
    D3 = 1.0
elif symbol is partially invertible (e.g., √ for non-negative reals):
    D3 = 0.5
else:
    D3 = 0.0
```

**Example**:
- `+` (addition): D3 = 1.0 (inverse: subtraction)
- `×` (multiplication): D3 = 1.0 (inverse: division, excluding zero)
- `√` (square root): D3 = 0.5 (only for non-negative reals)
- `∧` (logical AND): D3 = 0.0 (no unique inverse)

**Rationale**: Invertibility reflects informational reversibility. Symbols with inverses allow bidirectional reasoning, reducing ambiguity.

---

## D4: Commutativity (Binary Indicator)

**Definition**: Whether the symbol's operation is commutative (order-independent).

**Computation**:
```
if symbol.arity >= 2 and symbol.is_commutative:
    D4 = 1.0
else:
    D4 = 0.0
```

**Example**:
- `+` (addition): D4 = 1.0 (a + b = b + a)
- `×` (multiplication): D4 = 1.0 (a × b = b × a)
- `−` (subtraction): D4 = 0.0 (a − b ≠ b − a)
- `÷` (division): D4 = 0.0 (a ÷ b ≠ b ÷ a)

**Rationale**: Commutativity reduces the number of distinct interpretations, lowering cognitive load.

---

## D5: Meaning Count (Ambiguity, Log-Normalized)

**Definition**: The number of distinct formal definitions or semantic meanings assigned to the symbol across mathematical and computational contexts.

**Computation**:
```
meaning_count_raw = count of distinct definitions in:
  - LaTeX packages (e.g., amsmath, amssymb)
  - Unicode annotations (Unicode Consortium database)
  - Mathematical dictionaries (e.g., MathWorld, Wikipedia)
  - Programming language specifications (for computational symbols)

meaning_count_capped = min(meaning_count_raw, 10)
D5 = meaning_count_capped / 10.0
```

**Example**:
- `⊕` (novel operator, single meaning): D5 = 0.1
- `+` (addition, 1 primary meaning): D5 = 0.1
- `*` (multiplication, convolution, pointer dereference): D5 = 0.3
- `|` (absolute value, divides, pipe operator, bitwise OR): D5 = 0.4

**Rationale**: Semantic ambiguity directly increases informational entropy. Multiple meanings require context-dependent disambiguation.

---

## D6: Dependency Depth (Compositional Complexity, Log-Normalized)

**Definition**: The average depth of the symbol's formal definition in terms of more primitive symbols, normalized by the vocabulary size.

**Computation**:
```
1. Parse the symbol's formal definition into a dependency tree.
2. Compute the depth of each leaf node (primitive symbol).
3. Average the depths across all leaves.
4. Normalize by log2(V), where V = total vocabulary size.

dependency_depth_raw = mean(depth of all primitive dependencies)
V = vocabulary_size (e.g., 1006 for this study)
D6 = dependency_depth_raw / log2(V)
```

**Example**:
- `+` (primitive, no dependencies): D6 = 0.0
- `⊕` (defined as `(a*b + b*a)/2`, depth = 2): D6 = 2 / log2(1006) ≈ 0.20
- `∇²` (Laplacian, defined via `∂²/∂x² + ∂²/∂y² + ...`, depth = 3): D6 = 3 / log2(1006) ≈ 0.30

**Rationale**: Compositional depth reflects the cognitive cost of unpacking a symbol's meaning. Deeper dependencies require more inferential steps.

---

## D7: Closure Degree (Normalized)

**Definition**: The degree to which the symbol's operation produces results within the same algebraic structure as its inputs.

**Computation**:
```
closure_contexts = count of contexts where output type = input type
total_contexts = count of all formal contexts
D7 = closure_contexts / total_contexts
```

**Practical Approximation** (for this study):
```
if symbol always produces same-type output (e.g., + on ℝ → ℝ):
    D7 = 1.0
elif symbol sometimes produces same-type output:
    D7 = 0.5
else:
    D7 = 0.0
```

**Example**:
- `+` (addition on ℝ): D7 = 1.0 (ℝ + ℝ → ℝ)
- `√` (square root): D7 = 0.5 (ℝ → ℝ≥0, partial closure)
- `∈` (set membership): D7 = 0.0 (element ∈ set → boolean, different type)

**Rationale**: Closure simplifies reasoning by maintaining type consistency. Lack of closure introduces type-checking overhead.

---

## D8: Overloading Index (Composite Metric, Normalized)

**Definition**: A composite measure of semantic overloading, combining symbol entropy and meaning count.

**Computation**:
```
# Symbol Entropy (H_sym): Shannon entropy of symbol usage across corpora
token_counts = [count of symbol in corpus_i for all corpora]
probabilities = token_counts / sum(token_counts)
H_sym_raw = -sum(p * log2(p) for p in probabilities if p > 0)
H_sym_normalized = H_sym_raw / log2(len(corpora))

# Composite Overloading Index
D8 = 0.5 * H_sym_normalized + 0.5 * D5
```

**Example**:
- `⊕` (novel, single meaning, rare): D8 ≈ 0.05
- `+` (common, single meaning): D8 ≈ 0.15
- `*` (common, multiple meanings): D8 ≈ 0.35
- `|` (very common, highly overloaded): D8 ≈ 0.50

**Rationale**: Overloading combines frequency-based ambiguity (entropy) with semantic ambiguity (meaning count). High overloading increases disambiguation cost.

---

## Implementation Notes

### Determinism and Reproducibility

All D-variable computations must be:
1. **Deterministic**: Given the same input metadata, produce identical output.
2. **Versioned**: Changes to definitions require version increments.
3. **Auditable**: Log all intermediate values for verification.

### Random Seed

All stochastic processes (e.g., bootstrapping for CIs) use:
```python
RANDOM_SEED = 42
```

### Validation

Each D-variable must pass:
1. **Range check**: 0.0 ≤ D_i ≤ 1.0
2. **Type check**: D_i is float64
3. **Null check**: No NaN or Inf values

---

## References

- Unicode Consortium. (2024). *Unicode Character Database*. https://unicode.org/ucd/
- Wolfram MathWorld. (2024). *Mathematical Notation*. https://mathworld.wolfram.com/
- LaTeX Project. (2024). *Comprehensive LaTeX Symbol List*. https://ctan.org/pkg/comprehensive

---

**End of Specification**
