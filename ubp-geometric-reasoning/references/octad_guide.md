# The Octad: 8 Geometric Domains of Existence

In the UBP system, all concepts are categorized into one of eight fundamental domains, known as **The Octad**. This categorization is not arbitrary but is determined by the geometric properties of the concept's 24-bit vector, particularly the state of its 12th bit.

This guide provides a reference for each of the eight domains.

| Domain | Bit 12 | Description | Examples |
|---|---|---|---|
| **SUBSTANCE** | 1 | Stable matter, elements, and physical objects. The foundational building blocks of reality. | `ELEM_H_001` (Hydrogen), `MATTER_H2O_001` (Water) |
| **QUANTITY** | 0 | Pure magnitude, mathematical constants, and numerical relationships. The abstract measures of the system. | `CONST_PI_001` (Pi), `MATH_UNITY_001` (Unity) |
| **ORGANISM** | N/A | Biological systems, complex adaptive systems, and living entities. | `BIO_DNA_001` (DNA), `SYS_ECO_001` (Ecosystem) |
| **ALGORITHM** | N/A | Logic, code, information processing, and computational procedures. | `ALGO_SHA256_001` (SHA-256), `LOGIC_IF_THEN_001` (If-Then) |
| **MECHANISM** | N/A | Physical interactions, reactions, forces, and processes. The dynamics of the system. | `FORCE_GRAVITY_001` (Gravity), `REACT_FUSION_001` (Fusion) |
| **IMPERATIVE** | N/A | System laws, constraints, fundamental principles, and axioms. The rules of the game. | `LAW_COMP_002` (Computational Symmetry), `AXIOM_NON_CONTRADICTION_001` |
| **ENTROPY** | N/A | Chaos, void, dissolution, noise, and randomness. The forces of decoherence. | `STATE_CHAOS_001` (Chaos), `CONCEPT_VOID_001` (The Void) |
| **MEANING** | N/A | Semantic value, linguistic concepts, symbols, and interpretations. The layer of abstraction. | `SYMBOL_ALPHA_001` (Alpha), `CONCEPT_LOVE_001` (Love) |

## Geometric Categorization

The `auto_trigger.py` script and the `MemoryStatus.tsx` component in the UBP Core Studio work together to perform this categorization:

1.  **Bit-12 Logic:** The primary determinant for **SUBSTANCE** (Bit 12=1) vs. **QUANTITY** (Bit 12=0).
2.  **ID Prefix Mapping:** UBP IDs are often prefixed with a category hint (e.g., `ELEM_`, `ALGO_`, `LAW_`), which is used for initial categorization.
3.  **Keyword & Tag Analysis:** The system scans the `tags` and `name` fields of a memory entry for keywords (e.g., "element", "physics", "biology") to refine the categorization.

This multi-layered approach allows the AI to "see" the shape of the research data, enabling more sophisticated filtering, analysis, and cognitive biasing through the Frame of Mind (FOM) system.
