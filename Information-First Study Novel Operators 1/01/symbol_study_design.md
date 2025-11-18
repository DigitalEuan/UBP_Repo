# UBP Symbol Study - Phase 1: Implementation Design

**Title**: Foundations of Symbolic Information Geometry  
**Author**: Manus AI  
**Date**: November 18, 2025  
**Version**: 1.0

---

## Executive Summary

This document provides a complete, actionable implementation design for the UBP Symbol Study Phase 1, building directly on the validated methodology from the minerals study. The design addresses the critical challenge of encoding abstract mathematical symbols into the UBP substrate while maintaining the rigorous, information-first principles that led to the minerals study's success.

**Key Innovation**: A three-layer encoding system (Unicode seed → Property bitfield → CoherenceState) that preserves intrinsic symbol properties while enabling full UBP substrate computation.

---

## 1. Study Architecture Overview

### 1.1 Three-Phase Implementation

**Phase 1A: Dataset & Encoding Design** (Foundation)
- Curate 200-300 symbol dataset
- Design intrinsic property encoding
- Validate encoding consistency
- **Duration**: ~2-3 days
- **Critical Success Factor**: Encoding must be intrinsic, deterministic, label-independent

**Phase 1B: UBP Pipeline Implementation** (Computation)
- Implement symbol_coherence_model.py
- Compute all UBP features via coherence_substrate_v2.py
- Generate coherence distributions
- **Duration**: ~3-4 days
- **Critical Success Factor**: Full UBP implementation, no shortcuts

**Phase 1C: Statistical Analysis & Validation** (Discovery)
- GMM, bootstrap, clustering, ML classification
- Foundational principle analysis
- Reproducibility package
- **Duration**: ~3-4 days
- **Critical Success Factor**: Data-driven thresholds, no a priori decisions

### 1.2 Success Metrics

The study succeeds if it produces:
1. A stable, interpretable NRCI distribution for symbols
2. Natural clustering in coherence space (if it exists)
3. Learnable classification boundaries (if they exist)
4. Statistically significant relationships to UBP constants
5. Complete reproducibility (reproduce.sh passes)
6. Emergent structure (not imposed by encoding)

---

## 2. Phase 1A: Dataset & Encoding Design

### 2.1 Symbol Dataset Construction

**Target**: 200-300 mathematical symbols across 9 categories

**Category Distribution** (balanced sampling):

| Category | Target Count | Examples | Rationale |
|----------|--------------|----------|-----------|
| Arithmetic | 20-25 | +, −, ×, ÷, √, ∑, ∏ | Basic operations, high closure |
| Algebra | 30-35 | =, ≠, ≡, ≈, ∝, <, >, ≤, ≥ | Relations, medium closure |
| Logic | 25-30 | ∧, ∨, ¬, →, ↔, ⊕, ⊤, ⊥ | Boolean operators, high invertibility |
| Set Theory | 30-35 | ∈, ⊆, ⊂, ∪, ∩, ∅, ℘, × | Foundational, medium ambiguity |
| Calculus | 25-30 | ∂, ∇, ∫, ∮, d, Δ, lim | Differential/integral, low closure |
| Quantum | 20-25 | σ_x, σ_y, σ_z, \|ψ⟩, ⟨ψ\|, ⊗, ⊕ | Specialized, low ambiguity |
| Probability | 20-25 | ℙ, 𝔼, ~, \|, ←, σ², μ | Statistical, medium overloading |
| Information | 15-20 | H, I, S, D_KL, ρ, log | Information theory, low overloading |
| Miscellaneous | 15-20 | ∘, ⊗, ⊕, ∇, ∂, ∞, ∅ | Cross-domain, variable properties |

**Metadata Fields** (per symbol):

```json
{
  "symbol": "∫",
  "unicode": "U+222B",
  "latex": "\\int",
  "name": "integral",
  "category": "calculus",
  "arity": "unary",
  "formal_role": "operator",
  "meaning_count": 3,
  "dependency_depth": 2,
  "invertibility": "partial",
  "commutativity": "no",
  "associativity": "no",
  "identity_exists": "no",
  "inverse_exists": "partial",
  "closure_degree": "low",
  "overloading_contexts": ["definite", "indefinite", "line_integral"]
}
```

**Data Sources**:
1. Unicode Mathematical Operators (U+2200 to U+22FF)
2. LaTeX symbol reference (comprehensive.tex)
3. MathWorld symbol database
4. ISO 80000-2 mathematical notation standard

### 2.2 Three-Layer Encoding System

**Layer 1: Unicode Seed** (Deterministic Base)
```python
def unicode_seed(symbol: str) -> float:
    """Convert Unicode codepoint to normalized float [0, 1]."""
    codepoint = ord(symbol)
    # Normalize to [0, 1] range (Unicode math symbols: U+0000 to U+1FFFF)
    return codepoint / 0x1FFFF
```

**Layer 2: Property Bitfield** (8D Intrinsic Encoding)

Design an 8-dimensional bitfield matching the minerals study structure:

| Dimension | Property | Encoding | Range | Rationale |
|-----------|----------|----------|-------|-----------|
| **D1** | Arity | 0=nullary, 1=unary, 2=binary, 3=ternary+ | [0, 3] | Structural complexity |
| **D2** | Formal Role | 0=operand, 1=operator, 2=relation, 3=quantifier | [0, 3] | Syntactic function |
| **D3** | Invertibility | 0=none, 1=partial, 2=full | [0, 2] | Closure property |
| **D4** | Commutativity | 0=no, 1=partial, 2=yes | [0, 2] | Algebraic property |
| **D5** | Meaning Count | log₂(count + 1) | [0, ~4] | Ambiguity measure |
| **D6** | Dependency Depth | Tree depth in formula | [0, ~5] | Compositional complexity |
| **D7** | Closure Degree | 0=low, 1=medium, 2=high | [0, 2] | Logical completeness |
| **D8** | Overloading Index | log₂(contexts + 1) | [0, ~4] | Semantic ambiguity |

**Normalization**: Each dimension normalized to [0, 1] for geometric consistency

**Layer 3: CoherenceState Initialization**
```python
def symbol_to_coherence_state(symbol_data: dict) -> CoherenceState:
    """
    Convert symbol to initial CoherenceState.
    
    Combines Unicode seed with property bitfield.
    """
    # Layer 1: Unicode seed
    seed_value = unicode_seed(symbol_data['symbol'])
    
    # Layer 2: Property bitfield (8D)
    bitfield = compute_bitfield(symbol_data)
    
    # Layer 3: Initialize CoherenceState
    # Use geometric mean of seed and bitfield magnitude
    bitfield_magnitude = np.linalg.norm(bitfield)
    initial_value = (seed_value * bitfield_magnitude) ** 0.5
    
    state = CoherenceState(
        value=initial_value,
        log_nrci_error=None,  # Default to NRCI_TARGET
        net_refinements=0,
        precision_mode=PrecisionMode.FLOAT,
        metadata={
            'symbol': symbol_data['symbol'],
            'unicode': symbol_data['unicode'],
            'category': symbol_data['category'],
            'bitfield': bitfield.tolist(),
            'seed_value': seed_value
        }
    )
    
    return state
```

### 2.3 Intrinsic Property Quantification

**Critical Challenge**: How to measure abstract properties objectively?

**Approach**: Use formal mathematical definitions + cross-validation

#### 2.3.1 Invertibility

**Definition**: Existence of inverse operation

**Encoding**:
- `0 (none)`: No inverse exists (e.g., ∫ has no general inverse)
- `1 (partial)`: Inverse exists in restricted domain (e.g., √ for non-negative)
- `2 (full)`: Inverse always exists (e.g., + has −)

**Validation**: Cross-check with group theory (inverse element existence)

#### 2.3.2 Commutativity

**Definition**: a ⊕ b = b ⊕ a

**Encoding**:
- `0 (no)`: Never commutative (e.g., −, ÷, →)
- `1 (partial)`: Commutative in some contexts (e.g., ⊗ for tensors)
- `2 (yes)`: Always commutative (e.g., +, ×, ∧, ∨)

**Validation**: Check algebraic structure tables

#### 2.3.3 Meaning Count (Ambiguity)

**Definition**: Number of distinct mathematical meanings

**Encoding**: log₂(count + 1)

**Examples**:
- `|` (bar): 5 meanings (absolute value, divides, conditional, cardinality, restriction) → log₂(6) ≈ 2.58
- `∫` (integral): 3 meanings (definite, indefinite, line) → log₂(4) = 2.0
- `σ` (sigma): 4 meanings (summation, standard deviation, Pauli matrix, stress tensor) → log₂(5) ≈ 2.32

**Validation**: Count meanings across 3 sources (MathWorld, Wikipedia, ISO 80000-2)

#### 2.3.4 Overloading Index

**Definition**: Number of distinct contexts where symbol is used

**Encoding**: log₂(contexts + 1)

**Examples**:
- `+`: 6 contexts (arithmetic, vector, matrix, set union, logical OR, complex) → log₂(7) ≈ 2.81
- `∇`: 4 contexts (gradient, divergence, curl, del operator) → log₂(5) ≈ 2.32
- `σ_x`: 1 context (Pauli X matrix) → log₂(2) = 1.0

**Validation**: Cross-check with LaTeX package usage (amsmath, amssymb, physics)

#### 2.3.5 Closure Degree

**Definition**: Degree to which operation is closed under composition

**Encoding**:
- `0 (low)`: Rarely closed (e.g., ∫, ∂ - require limits/domains)
- `1 (medium)`: Conditionally closed (e.g., √ - closed for non-negative)
- `2 (high)`: Always closed (e.g., +, ×, ∧, ∨)

**Validation**: Check closure under repeated application

#### 2.3.6 Dependency Depth

**Definition**: Average depth in formula parse trees

**Encoding**: Measured from corpus of 1000+ mathematical formulas

**Method**:
1. Parse LaTeX formulas from arXiv math papers
2. Build abstract syntax trees (AST)
3. Compute average depth of symbol in AST
4. Normalize to [0, 5] range

**Examples**:
- `+`: Depth ≈ 2 (appears at all levels)
- `∫`: Depth ≈ 1 (usually outermost)
- `∂`: Depth ≈ 1.5 (outer or mid-level)
- `²`: Depth ≈ 3 (usually innermost)

### 2.4 Encoding Validation Tests

**Test 1: Consistency Check**
- Same symbol → same encoding (deterministic)
- Different symbols → different encodings (injective)

**Test 2: No Privileged Placement**
- Bitfield distribution should be approximately uniform
- No dimension should be dominated by single value

**Test 3: Label Independence**
- Encoding computed without using category labels
- Category used only for post-hoc interpretation

**Test 4: Closure Invariance**
- Symbols with high closure degree should have high refinement potential
- Symbols with high ambiguity should have high degradation

---

## 3. Phase 1B: UBP Pipeline Implementation

### 3.1 Symbol Coherence Model Architecture

**File**: `symbol_coherence_model.py`

**Structure** (analogous to mineral_coherence_model_v3_recalibrated.py):

```python
"""
UBP Symbol Coherence Model v1.0
================================

Information-first analysis of mathematical symbols using UBP 3.5.

Based on the validated methodology from the UBP Mineral Study Phase 2.
"""

import math
import json
from typing import Dict, List, Tuple, Any
from dataclasses import dataclass, asdict
import numpy as np

from coherence_substrate_v2 import (
    CoherenceState, ComputationHistory, CoherenceHexDictionary,
    PrecisionMode, Y, Y_INVERSE, GOLDEN_RATIO, PI,
    NRCI_TARGET, O_OBSERVER
)

# ============================================================================
# Symbol Coherence Constants
# ============================================================================

# Refinement scaling factors (to be calibrated)
INVERTIBILITY_REFINEMENT_SCALE = 1.0
COMMUTATIVITY_REFINEMENT_SCALE = 0.8
CLOSURE_REFINEMENT_SCALE = 1.2

# Degradation scaling factors (to be calibrated)
AMBIGUITY_DEGRADATION_SCALE = 0.01
OVERLOADING_DEGRADATION_SCALE = 0.008
DEPENDENCY_DEGRADATION_SCALE = 0.005

# ============================================================================
# Symbol Coherence Result
# ============================================================================

@dataclass
class SymbolCoherenceResult:
    """Complete coherence analysis result for a symbol."""
    symbol: str
    unicode: str
    latex: str
    name: str
    category: str
    
    # Bitfield encoding
    bitfield: List[float]
    seed_value: float
    
    # UBP features
    base_nrci: float
    final_nrci: float
    total_refinements: int
    total_degradation: float
    net_refinements: int
    
    # Detailed metrics
    invertibility_refinements: int
    commutativity_refinements: int
    closure_refinements: int
    ambiguity_degradation: float
    overloading_degradation: float
    dependency_degradation: float
    
    # Metadata
    computation_depth: int
    hex_address: str
    history_summary: Dict[str, Any]
    metadata: Dict[str, Any]

# ============================================================================
# Symbol Coherence Model
# ============================================================================

class SymbolCoherenceModel:
    """
    Full UBP coherence model for mathematical symbols.
    
    Workflow:
    1. Load symbol dataset
    2. Encode symbols (Unicode seed + property bitfield)
    3. Initialize CoherenceStates
    4. Apply refinements (invertibility, commutativity, closure)
    5. Apply degradation (ambiguity, overloading, dependency)
    6. Apply observer cost
    7. Compute final NRCI
    8. Persist to HexDictionary
    """
    
    def __init__(self, storage_dir: str = "./hex_storage_symbols/"):
        self.hex_dict = CoherenceHexDictionary(storage_dir)
        CoherenceState.set_hex_dictionary(self.hex_dict, auto_persist=False)
        self.results: List[SymbolCoherenceResult] = []
    
    def compute_bitfield(self, symbol_data: dict) -> np.ndarray:
        """Compute 8D property bitfield for symbol."""
        bitfield = np.zeros(8)
        
        # D1: Arity
        arity_map = {'nullary': 0, 'unary': 1, 'binary': 2, 'ternary': 3}
        bitfield[0] = arity_map.get(symbol_data.get('arity', 'unary'), 1) / 3.0
        
        # D2: Formal Role
        role_map = {'operand': 0, 'operator': 1, 'relation': 2, 'quantifier': 3}
        bitfield[1] = role_map.get(symbol_data.get('formal_role', 'operator'), 1) / 3.0
        
        # D3: Invertibility
        inv_map = {'none': 0, 'partial': 1, 'full': 2}
        bitfield[2] = inv_map.get(symbol_data.get('invertibility', 'none'), 0) / 2.0
        
        # D4: Commutativity
        comm_map = {'no': 0, 'partial': 1, 'yes': 2}
        bitfield[3] = comm_map.get(symbol_data.get('commutativity', 'no'), 0) / 2.0
        
        # D5: Meaning Count (log scale)
        meaning_count = symbol_data.get('meaning_count', 1)
        bitfield[4] = min(math.log2(meaning_count + 1) / 4.0, 1.0)
        
        # D6: Dependency Depth
        depth = symbol_data.get('dependency_depth', 2)
        bitfield[5] = min(depth / 5.0, 1.0)
        
        # D7: Closure Degree
        closure_map = {'low': 0, 'medium': 1, 'high': 2}
        bitfield[6] = closure_map.get(symbol_data.get('closure_degree', 'medium'), 1) / 2.0
        
        # D8: Overloading Index (log scale)
        overloading = len(symbol_data.get('overloading_contexts', []))
        bitfield[7] = min(math.log2(overloading + 1) / 4.0, 1.0)
        
        return bitfield
    
    def create_base_state(self, symbol_data: dict) -> CoherenceState:
        """Create initial CoherenceState for symbol."""
        # Layer 1: Unicode seed
        seed_value = ord(symbol_data['symbol']) / 0x1FFFF
        
        # Layer 2: Property bitfield
        bitfield = self.compute_bitfield(symbol_data)
        bitfield_magnitude = np.linalg.norm(bitfield)
        
        # Layer 3: Initialize CoherenceState
        initial_value = (seed_value * bitfield_magnitude) ** 0.5
        
        state = CoherenceState(
            value=initial_value,
            log_nrci_error=None,
            net_refinements=0,
            precision_mode=PrecisionMode.FLOAT,
            metadata={
                'symbol': symbol_data['symbol'],
                'unicode': symbol_data['unicode'],
                'category': symbol_data['category'],
                'bitfield': bitfield.tolist(),
                'seed_value': seed_value,
                'phase': 'initialization'
            }
        )
        
        return state
    
    def apply_refinements(self, state: CoherenceState, symbol_data: dict) -> Tuple[CoherenceState, int, int, int]:
        """
        Apply Y-refinements based on symbol properties.
        
        Returns:
            (refined_state, invertibility_refs, commutativity_refs, closure_refs)
        """
        current_state = state
        
        # Invertibility refinements
        inv_map = {'none': 0, 'partial': 1, 'full': 2}
        inv_refs = int(inv_map.get(symbol_data.get('invertibility', 'none'), 0) * INVERTIBILITY_REFINEMENT_SCALE)
        
        for i in range(inv_refs):
            current_state = current_state.refine_forward()
            current_state.metadata['phase'] = f'invertibility_refinement_{i+1}'
        
        # Commutativity refinements
        comm_map = {'no': 0, 'partial': 1, 'yes': 2}
        comm_refs = int(comm_map.get(symbol_data.get('commutativity', 'no'), 0) * COMMUTATIVITY_REFINEMENT_SCALE)
        
        for i in range(comm_refs):
            current_state = current_state.refine_forward()
            current_state.metadata['phase'] = f'commutativity_refinement_{i+1}'
        
        # Closure refinements
        closure_map = {'low': 0, 'medium': 1, 'high': 2}
        closure_refs = int(closure_map.get(symbol_data.get('closure_degree', 'medium'), 1) * CLOSURE_REFINEMENT_SCALE)
        
        for i in range(closure_refs):
            current_state = current_state.refine_forward()
            current_state.metadata['phase'] = f'closure_refinement_{i+1}'
        
        return current_state, inv_refs, comm_refs, closure_refs
    
    def apply_degradation(self, state: CoherenceState, symbol_data: dict) -> Tuple[CoherenceState, float, float, float]:
        """
        Apply coherence degradation based on symbol complexity.
        
        Returns:
            (degraded_state, ambiguity_deg, overloading_deg, dependency_deg)
        """
        # Ambiguity degradation
        meaning_count = symbol_data.get('meaning_count', 1)
        ambiguity_deg = math.log2(meaning_count + 1) * AMBIGUITY_DEGRADATION_SCALE
        
        # Overloading degradation
        overloading = len(symbol_data.get('overloading_contexts', []))
        overloading_deg = math.log2(overloading + 1) * OVERLOADING_DEGRADATION_SCALE
        
        # Dependency degradation
        depth = symbol_data.get('dependency_depth', 2)
        dependency_deg = depth * DEPENDENCY_DEGRADATION_SCALE
        
        # Total degradation
        total_deg = ambiguity_deg + overloading_deg + dependency_deg
        
        degraded_state = state.degrade_by(total_deg)
        degraded_state.metadata['phase'] = 'complexity_degradation'
        degraded_state.metadata['total_degradation'] = total_deg
        degraded_state.metadata['ambiguity_degradation'] = ambiguity_deg
        degraded_state.metadata['overloading_degradation'] = overloading_deg
        degraded_state.metadata['dependency_degradation'] = dependency_deg
        
        return degraded_state, ambiguity_deg, overloading_deg, dependency_deg
    
    def apply_observer_cost(self, state: CoherenceState) -> CoherenceState:
        """Apply observer measurement cost (1/Y refinement)."""
        observer_state = state.refine_backward()
        observer_state.metadata['phase'] = 'observer_cost'
        observer_state.metadata['O_observer'] = O_OBSERVER
        
        return observer_state
    
    def calculate_symbol_coherence(self, symbol_data: dict) -> SymbolCoherenceResult:
        """
        Calculate full coherence for a mathematical symbol.
        
        Workflow:
        1. Create base state (Unicode + bitfield encoding)
        2. Apply refinements (invertibility, commutativity, closure)
        3. Apply degradation (ambiguity, overloading, dependency)
        4. Apply observer cost
        5. Compute final NRCI
        6. Persist to HexDictionary
        """
        # Step 1: Base state
        state = self.create_base_state(symbol_data)
        base_nrci = state.nrci
        seed_value = state.metadata['seed_value']
        bitfield = state.metadata['bitfield']
        
        # Step 2: Refinements
        state, inv_refs, comm_refs, closure_refs = self.apply_refinements(state, symbol_data)
        total_refs = inv_refs + comm_refs + closure_refs
        
        # Step 3: Degradation
        state, ambig_deg, overload_deg, depend_deg = self.apply_degradation(state, symbol_data)
        total_deg = ambig_deg + overload_deg + depend_deg
        
        # Step 4: Observer cost
        state = self.apply_observer_cost(state)
        
        # Step 5: Persist
        state.persist()
        final_nrci = state.nrci
        
        result = SymbolCoherenceResult(
            symbol=symbol_data['symbol'],
            unicode=symbol_data['unicode'],
            latex=symbol_data['latex'],
            name=symbol_data['name'],
            category=symbol_data['category'],
            bitfield=bitfield,
            seed_value=seed_value,
            base_nrci=base_nrci,
            final_nrci=final_nrci,
            total_refinements=total_refs,
            total_degradation=total_deg,
            net_refinements=state.net_refinements,
            invertibility_refinements=inv_refs,
            commutativity_refinements=comm_refs,
            closure_refinements=closure_refs,
            ambiguity_degradation=ambig_deg,
            overloading_degradation=overload_deg,
            dependency_degradation=depend_deg,
            computation_depth=len(state.history.operations),
            hex_address=state.hex_address or "not_persisted",
            history_summary=state.history.get_summary(),
            metadata=state.metadata.copy()
        )
        
        self.results.append(result)
        return result
    
    def batch_calculate(self, symbols: List[Dict[str, Any]]) -> List[SymbolCoherenceResult]:
        """Calculate coherence for multiple symbols."""
        results = []
        for symbol_data in symbols:
            result = self.calculate_symbol_coherence(symbol_data)
            results.append(result)
        return results
    
    def export_results(self, output_path: str):
        """Export results to JSON."""
        results_dict = [asdict(r) for r in self.results]
        with open(output_path, 'w') as f:
            json.dump(results_dict, f, indent=2)
```

### 3.2 Calibration Strategy

**Challenge**: Refinement and degradation scales are not known a priori

**Approach**: Iterative calibration (similar to minerals study)

**Calibration Goals**:
1. NRCI distribution should be interpretable (not all 0 or all 1)
2. Distribution should show structure (not uniform noise)
3. Variance should be sufficient for ML classification (if structure exists)

**Calibration Parameters**:
- `INVERTIBILITY_REFINEMENT_SCALE`: [0.5, 2.0]
- `COMMUTATIVITY_REFINEMENT_SCALE`: [0.5, 2.0]
- `CLOSURE_REFINEMENT_SCALE`: [0.5, 2.0]
- `AMBIGUITY_DEGRADATION_SCALE`: [0.001, 0.1]
- `OVERLOADING_DEGRADATION_SCALE`: [0.001, 0.1]
- `DEPENDENCY_DEGRADATION_SCALE`: [0.001, 0.1]

**Calibration Procedure**:
1. Run model with initial parameters (all 1.0 for refinement, 0.01 for degradation)
2. Analyze NRCI distribution (mean, std, range)
3. Adjust parameters to achieve target distribution:
   - Mean NRCI: ~0.95-0.98 (coherent but not perfect)
   - Std NRCI: ~0.02-0.05 (sufficient variance)
   - Range: [0.85, 0.995] (interpretable spread)
4. Iterate until distribution is stable and interpretable

---

## 4. Phase 1C: Statistical Analysis & Validation

### 4.1 Analysis Pipeline

**Exactly following the minerals study methodology**:

#### 4.1.1 Distribution Analysis

**Script**: `analyze_symbol_distribution.py`

**Tasks**:
1. Load symbol coherence results
2. Compute NRCI distribution statistics
3. Test for bimodality (GMM with BIC)
4. Identify natural thresholds (percentiles, gaps)
5. Bootstrap confidence intervals (n=2000)

**Outputs**:
- `symbol_nrci_distribution.png`
- `symbol_nrci_statistics.json`
- `symbol_gmm_analysis.json`

#### 4.1.2 Geometric Analysis

**Script**: `analyze_symbol_geometry.py`

**Tasks**:
1. Extract 8D bitfield features
2. PCA (primary reference, 3 components)
3. UMAP (nonlinear manifold, 2D and 3D)
4. t-SNE (local structure, 2D)
5. Spectral clustering
6. Separability metrics

**Outputs**:
- `symbol_pca_projection.png`
- `symbol_umap_projection.png`
- `symbol_tsne_projection.png`
- `symbol_geometric_metrics.json`

#### 4.1.3 Classification Analysis

**Script**: `classify_symbol_boundaries.py`

**Tasks**:
1. Prepare features (8D bitfield + NRCI + refinements + degradation)
2. Train classifiers:
   - Random Forest (n_estimators=100)
   - SVM with RBF kernel
   - Neural Network (2 hidden layers, 64 units)
3. Stratified 5-fold cross-validation
4. Permutation tests (n=1000)
5. Confusion matrices, ROC, PR curves
6. Permutation importance (n=50)
7. Ablation studies

**Outputs**:
- `symbol_classification_results.json`
- `symbol_confusion_matrices.png`
- `symbol_roc_curves.png`
- `symbol_feature_importance.png`

#### 4.1.4 Foundational Principle Analysis

**Script**: `analyze_symbol_principles.py`

**Tasks**:
1. Test threshold / O_observer ≈ Y relationship
2. Analyze NRCI vs refinement/degradation correlations
3. Test for geometric scaling patterns
4. Investigate inversion/negation symbols (¬, −, ⁻¹)
5. Compare symbol categories in coherence space

**Outputs**:
- `symbol_ubp_constants_analysis.json`
- `symbol_correlation_matrix.png`
- `symbol_category_comparison.png`

### 4.2 Reproducibility Package

**Structure**:
```
ubp_symbol_study_phase1/
├── README.md
├── reproduce.sh
├── requirements.txt
├── data/
│   ├── symbols_dataset.json
│   ├── symbols_processed.json
│   └── symbols_metadata.json
├── scripts/
│   ├── symbol_coherence_model.py
│   ├── analyze_symbol_distribution.py
│   ├── analyze_symbol_geometry.py
│   ├── classify_symbol_boundaries.py
│   └── analyze_symbol_principles.py
├── results/
│   ├── symbol_nrci_distribution.png
│   ├── symbol_pca_projection.png
│   ├── symbol_classification_results.json
│   └── ... (all outputs)
└── ubp_3.5/
    ├── coherence_substrate_v2.py
    └── ... (UBP system)
```

**reproduce.sh**:
```bash
#!/bin/bash
set -e

echo "======================================================================="
echo "UBP Symbol Study - Phase 1 Reproducibility Script"
echo "======================================================================="

# Step 1: Compute symbol coherence
echo "Step 1: Computing symbol coherence..."
python3.11 scripts/symbol_coherence_model.py

# Step 2: Distribution analysis
echo "Step 2: Analyzing NRCI distribution..."
python3.11 scripts/analyze_symbol_distribution.py

# Step 3: Geometric analysis
echo "Step 3: Analyzing geometric structure..."
python3.11 scripts/analyze_symbol_geometry.py

# Step 4: Classification analysis
echo "Step 4: Training classifiers..."
python3.11 scripts/classify_symbol_boundaries.py

# Step 5: Foundational principles
echo "Step 5: Analyzing UBP principles..."
python3.11 scripts/analyze_symbol_principles.py

echo "======================================================================="
echo "✅ ALL ANALYSES COMPLETE"
echo "======================================================================="
```

---

## 5. Expected Outcomes & Hypotheses

### 5.1 Testable Hypotheses

**H1: Natural Clustering**
- **Hypothesis**: Symbols will cluster by category (arithmetic, logic, calculus, etc.) in coherence space without using category labels.
- **Test**: Unsupervised clustering (GMM, spectral) should recover categories with >70% purity.
- **Rationale**: Similar to minerals clustering by crystal system, symbols with similar properties should occupy similar coherence regions.

**H2: Coherence Threshold**
- **Hypothesis**: A natural NRCI threshold will separate "fundamental" symbols (high closure, low ambiguity) from "composite" symbols (low closure, high ambiguity).
- **Test**: GMM should detect bimodal distribution; threshold should be learnable by ML.
- **Rationale**: Analogous to minerals, only certain symbols are "stable" in information space.

**H3: Degradation Dominance**
- **Hypothesis**: Ambiguity and overloading (degradation) will be more predictive than closure and invertibility (refinement).
- **Test**: Permutation importance should rank degradation features higher.
- **Rationale**: Minerals study found degradation (Z_max) dominated; symbol ambiguity may play analogous role.

**H4: UBP Constant Relationships**
- **Hypothesis**: threshold / O_observer ≈ Y (within 5%)
- **Test**: Bootstrap confidence interval for threshold, compute ratio.
- **Rationale**: Minerals study found this relationship; testing for universality.

**H5: Inversion Symmetry**
- **Hypothesis**: Inversion/negation symbols (¬, −, ⁻¹) will have special geometric properties (closer to Y-related curves).
- **Test**: Compute NRCI distribution for inversion symbols vs others.
- **Rationale**: These symbols represent fundamental information operations.

### 5.2 Potential Discoveries

**Discovery 1: Symbolic Coherence Basin**
- Similar to minerals, symbols may occupy a distinct "coherence basin" in 8D space.
- Visualization: PCA/UMAP should show tight clustering of viable symbols.

**Discovery 2: Minimal Symbol Set**
- A small subset of symbols (e.g., {+, ×, ¬, ∈}) may generate others through composition.
- Test: Analyze refinement chains to identify "generator" symbols.

**Discovery 3: Category Emergence**
- Symbol categories (arithmetic, logic, etc.) may emerge as natural clusters without labels.
- Test: Compare unsupervised clustering to ground-truth categories.

**Discovery 4: Ambiguity Bottleneck**
- Highly ambiguous symbols (e.g., |, ∘) may form a "bottleneck" analogous to Z=80-92 in minerals.
- Test: Analyze NRCI distribution for high-ambiguity symbols.

---

## 6. Risk Mitigation

### 6.1 Key Risks

**Risk 1: Encoding Subjectivity**
- **Issue**: Property quantification (invertibility, closure) may be subjective.
- **Mitigation**: Use formal definitions, cross-validate with 3 sources, document all assumptions.

**Risk 2: Label Leakage**
- **Issue**: Category labels may inadvertently influence encoding.
- **Mitigation**: Compute all features before assigning categories; validate encoding independence.

**Risk 3: Insufficient Variance**
- **Issue**: All symbols may have similar NRCI (no structure).
- **Mitigation**: Calibrate refinement/degradation scales iteratively; if no structure emerges, report null result (still valid science).

**Risk 4: Overfitting**
- **Issue**: ML models may overfit small dataset (200-300 symbols).
- **Mitigation**: Use stratified CV, permutation tests, report confidence intervals.

### 6.2 Fallback Strategies

**If no natural clustering emerges**:
- Report null result (symbols do not cluster in coherence space)
- Analyze why (insufficient variance, encoding issues, or genuine lack of structure)
- Still valuable: establishes limits of UBP framework

**If no threshold emerges**:
- Report continuous distribution (no bimodality)
- Analyze correlations instead of classification
- Focus on relative coherence (which symbols are more coherent than others)

**If ML classification fails**:
- Report baseline performance (no learnable boundary)
- Analyze feature importance (which properties matter most)
- Focus on geometric analysis (PCA, UMAP) instead

---

## 7. Timeline & Milestones

### Week 1: Dataset & Encoding
- **Day 1-2**: Curate 200-300 symbol dataset with metadata
- **Day 3-4**: Implement encoding functions (bitfield, CoherenceState)
- **Day 5**: Validate encoding (consistency, no privileged placement)
- **Milestone**: `symbols_dataset.json` complete and validated

### Week 2: UBP Pipeline
- **Day 1-2**: Implement `symbol_coherence_model.py`
- **Day 3**: Run initial coherence computation, analyze distribution
- **Day 4**: Calibrate refinement/degradation scales
- **Day 5**: Finalize coherence computation, export results
- **Milestone**: `symbols_processed.json` with full UBP features

### Week 3: Statistical Analysis
- **Day 1**: Distribution analysis (GMM, bootstrap)
- **Day 2**: Geometric analysis (PCA, UMAP, t-SNE)
- **Day 3**: Classification analysis (RF, SVM, NN)
- **Day 4**: Foundational principle analysis
- **Day 5**: Reproducibility package, final report
- **Milestone**: Complete Phase 1 report + reproduce.sh

---

## 8. Conclusion

This design provides a complete, actionable roadmap for the UBP Symbol Study Phase 1, directly building on the validated methodology from the minerals study. The three-layer encoding system (Unicode seed → Property bitfield → CoherenceState) addresses the critical challenge of encoding abstract symbols while maintaining the rigorous, information-first principles that led to the minerals study's success.

**Key Innovations**:
1. **Intrinsic property quantification** using formal mathematical definitions
2. **Three-layer encoding** preserving both seed value and structural properties
3. **Calibration strategy** for unknown refinement/degradation scales
4. **Testable hypotheses** enabling falsifiable predictions
5. **Risk mitigation** with fallback strategies for null results

**Next Action**: Begin Phase 1A (Dataset & Encoding) with user approval.
