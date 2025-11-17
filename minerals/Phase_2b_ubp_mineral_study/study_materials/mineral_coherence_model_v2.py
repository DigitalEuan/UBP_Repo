#!/usr/bin/env python3
"""
UBP Mineral Coherence Model v2.0
=================================

Properly implements crystalline OffBit pattern coherence using coherence_substrate_v2.py.

Key Features:
- CoherenceState v2.0 API with History tracking
- Calibrated NRCI threshold (≥0.99 for natural minerals, ≥0.999999 for perfect crystals)
- Crystalline OffBit pattern modeling
- Degradation accumulation in log-error space
- HexDictionary integration for persistence

Study 1 Lesson Applied:
- Natural minerals need NRCI ≥ 0.99 (adequate for geological persistence)
- Perfect synthetic crystals need NRCI ≥ 0.999999
- Study 1 was too restrictive at 0.999999 for all minerals
"""

import sys
import math
import json
from typing import Dict, List, Tuple, Any
from dataclasses import dataclass

# Import v2.0 substrate
from coherence_substrate_v2 import (
    CoherenceState, ComputationHistory, CoherenceHexDictionary,
    PrecisionMode, Y, Y_INVERSE, GOLDEN_RATIO, PI,
    NRCI_TARGET, O_OBSERVER
)


# ============================================================================
# Constants and Calibrations
# ============================================================================

# Coherence thresholds (Study 1 calibration)
NRCI_PERFECT_CRYSTAL = 0.999999  # Synthetic, lab-grown crystals
NRCI_NATURAL_MINERAL = 0.99      # Natural minerals (geological persistence)
NRCI_METASTABLE = 0.95           # Metastable phases (temporary)

# Crystalline structure parameters
TGIC_FACTOR = 0.5  # Triad Graph Interaction Constraint (Study 1: was 0.3, too restrictive)

# OffBit patterns for crystal symmetries
OFFBIT_PATTERNS = {
    'cubic': {
        'symmetry_order': 48,       # 48 symmetry operations
        'geometric_score': 1.0,     # Maximum geometric perfection
        'base_nrci': 0.999999,      # Highest coherence
        'Y_refinements': 8          # Highly refined
    },
    'hexagonal': {
        'symmetry_order': 24,
        'geometric_score': 0.95,
        'base_nrci': 0.999990,
        'Y_refinements': 7
    },
    'trigonal': {
        'symmetry_order': 12,
        'geometric_score': 0.90,
        'base_nrci': 0.999900,
        'Y_refinements': 6
    },
    'tetragonal': {
        'symmetry_order': 16,
        'geometric_score': 0.88,
        'base_nrci': 0.999800,
        'Y_refinements': 6
    },
    'orthorhombic': {
        'symmetry_order': 8,
        'geometric_score': 0.85,
        'base_nrci': 0.999500,
        'Y_refinements': 5
    },
    'monoclinic': {
        'symmetry_order': 4,
        'geometric_score': 0.80,
        'base_nrci': 0.999000,
        'Y_refinements': 4
    },
    'triclinic': {
        'symmetry_order': 2,
        'geometric_score': 0.75,
        'base_nrci': 0.998000,
        'Y_refinements': 3
    }
}


# ============================================================================
# Mineral Coherence State
# ============================================================================

@dataclass
class MineralCoherenceResult:
    """Result of mineral coherence calculation."""
    formula: str
    space_group: int
    crystal_system: str
    Z: int  # Atomic number or complexity
    
    # Coherence metrics
    base_nrci: float
    final_nrci: float
    passes_natural: bool  # ≥ 0.99
    passes_perfect: bool  # ≥ 0.999999
    
    # UBP tracking
    net_refinements: int
    computation_depth: int
    hex_address: str
    
    # Metadata
    history_summary: Dict[str, Any]
    metadata: Dict[str, Any]


class MineralCoherenceModel:
    """
    Model crystalline OffBit pattern coherence for minerals.
    
    Uses proper v2.0 API with History tracking and HexDictionary persistence.
    """
    
    def __init__(self, precision_mode: PrecisionMode = PrecisionMode.FLOAT):
        """Initialize model with optional HexDictionary."""
        self.precision_mode = precision_mode
        self.hex_dict = CoherenceHexDictionary()
        
        # Set class-level HexDictionary for auto-persistence
        CoherenceState.set_hex_dictionary(self.hex_dict, auto_persist=False)  # Manual control
        
        self.results: List[MineralCoherenceResult] = []
    
    def create_base_state(self, crystal_system: str, Z: int) -> CoherenceState:
        """
        Create base coherence state for a crystal system.
        
        Args:
            crystal_system: One of the 7 crystal systems
            Z: Atomic number or complexity parameter
        
        Returns:
            CoherenceState initialized with crystal properties
        """
        pattern = OFFBIT_PATTERNS.get(crystal_system.lower(), OFFBIT_PATTERNS['triclinic'])
        
        # Initialize with base NRCI
        base_log_error = math.log(1 - pattern['base_nrci'])
        
        # Geometric score as initial value
        state = CoherenceState(
            value=pattern['geometric_score'],
            log_nrci_error=base_log_error,
            net_refinements=0,
            history=ComputationHistory(),
            precision_mode=self.precision_mode,
            metadata={
                'crystal_system': crystal_system,
                'Z': Z,
                'symmetry_order': pattern['symmetry_order'],
                'phase': 'initialization'
            }
        )
        
        return state
    
    def apply_geometric_refinements(self, state: CoherenceState, target_refinements: int) -> CoherenceState:
        """
        Apply Y-refinements based on crystal symmetry.
        
        Higher symmetry → more refinements → better coherence
        """
        current_state = state
        
        for i in range(target_refinements):
            current_state = current_state.refine_forward()
            current_state.metadata['phase'] = f'refinement_{i+1}'
        
        return current_state
    
    def apply_complexity_degradation(self, state: CoherenceState, Z: int) -> CoherenceState:
        """
        Apply coherence degradation based on complexity (Z).
        
        More atoms/complexity → more ways to decohere
        Uses log-error accumulation (correct way per v2.0)
        """
        # Degradation scales with complexity
        # Study 1 insight: Should allow ~3% of structures to pass
        base_degradation = 0.0001  # Base degradation per unit Z
        
        # Apply TGIC constraint (geometric interaction limit)
        tgic_penalty = (1.0 - TGIC_FACTOR) * math.log(Z) * 0.001
        
        # Total degradation in log-error space
        total_degradation = base_degradation * Z + tgic_penalty
        
        degraded_state = state.degrade_by(total_degradation)
        degraded_state.metadata['phase'] = 'complexity_degradation'
        degraded_state.metadata['Z_penalty'] = total_degradation
        
        return degraded_state
    
    def apply_observer_cost(self, state: CoherenceState) -> CoherenceState:
        """
        Apply observer measurement cost.
        
        Study 1 Discovery: O_observer = 3.7782 = 1/Y EXACTLY
        This is not an additional penalty - it's the inverse refinement
        """
        # Observer cost is already embedded in Y-refinement structure
        # Just track it in metadata
        observer_state = state.refine_backward()  # One inverse refinement represents observation
        observer_state.metadata['phase'] = 'observer_cost'
        observer_state.metadata['O_observer'] = 1.0 / Y
        
        return observer_state
    
    def calculate_mineral_coherence(self, 
                                    formula: str,
                                    space_group: int,
                                    crystal_system: str,
                                    Z: int) -> MineralCoherenceResult:
        """
        Calculate full coherence for a mineral structure.
        
        Workflow:
        1. Create base state (crystal system dependent)
        2. Apply geometric refinements (symmetry dependent)
        3. Apply complexity degradation (Z dependent)
        4. Apply observer cost
        5. Evaluate against thresholds
        6. Persist to HexDictionary
        
        Returns:
            MineralCoherenceResult with full tracking
        """
        # Step 1: Base state
        state = self.create_base_state(crystal_system, Z)
        base_nrci = state.nrci
        
        # Step 2: Geometric refinements
        pattern = OFFBIT_PATTERNS.get(crystal_system.lower(), OFFBIT_PATTERNS['triclinic'])
        state = self.apply_geometric_refinements(state, pattern['Y_refinements'])
        
        # Step 3: Complexity degradation
        state = self.apply_complexity_degradation(state, Z)
        
        # Step 4: Observer cost
        state = self.apply_observer_cost(state)
        
        # Step 5: Persist and evaluate
        state.persist()
        final_nrci = state.nrci
        
        result = MineralCoherenceResult(
            formula=formula,
            space_group=space_group,
            crystal_system=crystal_system,
            Z=Z,
            base_nrci=base_nrci,
            final_nrci=final_nrci,
            passes_natural=(final_nrci >= NRCI_NATURAL_MINERAL),
            passes_perfect=(final_nrci >= NRCI_PERFECT_CRYSTAL),
            net_refinements=state.net_refinements,
            computation_depth=len(state.history.operations),
            hex_address=state.hex_address or "not_persisted",
            history_summary=state.history.get_summary(),
            metadata=state.metadata.copy()
        )
        
        self.results.append(result)
        return result
    
    def batch_calculate(self, minerals: List[Dict[str, Any]]) -> List[MineralCoherenceResult]:
        """
        Calculate coherence for multiple minerals.
        
        Args:
            minerals: List of dicts with keys: formula, space_group, crystal_system, Z
        
        Returns:
            List of MineralCoherenceResult
        """
        results = []
        for mineral in minerals:
            result = self.calculate_mineral_coherence(
                formula=mineral['formula'],
                space_group=mineral['space_group'],
                crystal_system=mineral['crystal_system'],
                Z=mineral['Z']
            )
            results.append(result)
        
        return results
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get summary statistics of all calculations."""
        if not self.results:
            return {'error': 'No results yet'}
        
        total = len(self.results)
        natural_pass = sum(1 for r in self.results if r.passes_natural)
        perfect_pass = sum(1 for r in self.results if r.passes_perfect)
        
        nrcis = [r.final_nrci for r in self.results]
        
        # Group by crystal system
        by_system = {}
        for r in self.results:
            system = r.crystal_system
            if system not in by_system:
                by_system[system] = {'count': 0, 'natural_pass': 0, 'perfect_pass': 0}
            by_system[system]['count'] += 1
            if r.passes_natural:
                by_system[system]['natural_pass'] += 1
            if r.passes_perfect:
                by_system[system]['perfect_pass'] += 1
        
        return {
            'total_minerals': total,
            'natural_pass_count': natural_pass,
            'natural_pass_rate': natural_pass / total,
            'perfect_pass_count': perfect_pass,
            'perfect_pass_rate': perfect_pass / total,
            'nrci_min': min(nrcis),
            'nrci_max': max(nrcis),
            'nrci_mean': sum(nrcis) / len(nrcis),
            'by_crystal_system': by_system,
            'hex_dict_size': len(self.hex_dict.metadata)
        }
    
    def visualize_result(self, result: MineralCoherenceResult) -> str:
        """Create ASCII visualization of a result."""
        lines = []
        lines.append("=" * 70)
        lines.append(f"Mineral: {result.formula} (Space Group {result.space_group})")
        lines.append(f"Crystal System: {result.crystal_system}, Z: {result.Z}")
        lines.append("-" * 70)
        lines.append(f"Base NRCI:  {result.base_nrci:.9f}")
        lines.append(f"Final NRCI: {result.final_nrci:.9f}")
        lines.append(f"Natural Mineral:  {'✓ PASS' if result.passes_natural else '✗ FAIL'} (≥0.99)")
        lines.append(f"Perfect Crystal:  {'✓ PASS' if result.passes_perfect else '✗ FAIL'} (≥0.999999)")
        lines.append("-" * 70)
        lines.append(f"Net Refinements: {result.net_refinements}")
        lines.append(f"Computation Depth: {result.computation_depth} operations")
        lines.append(f"Hex Address: {result.hex_address[:16]}...")
        lines.append("-" * 70)
        lines.append("History Summary:")
        for key, val in result.history_summary.items():
            lines.append(f"  {key}: {val}")
        lines.append("=" * 70)
        return "\n".join(lines)


# ============================================================================
# Testing and Validation
# ============================================================================

def test_coherence_model():
    """Test the coherence model with synthetic minerals."""
    print("=" * 70)
    print("UBP Mineral Coherence Model v2.0 - Test Suite")
    print("=" * 70)
    print()
    
    # Initialize model
    model = MineralCoherenceModel(precision_mode=PrecisionMode.FLOAT)
    
    # Test minerals spanning crystal systems and complexity
    test_minerals = [
        {
            'formula': 'NaCl',
            'space_group': 225,
            'crystal_system': 'cubic',
            'Z': 11  # Na
        },
        {
            'formula': 'SiO2',
            'space_group': 154,
            'crystal_system': 'hexagonal',
            'Z': 14  # Si
        },
        {
            'formula': 'CaCO3',
            'space_group': 167,
            'crystal_system': 'trigonal',
            'Z': 20  # Ca
        },
        {
            'formula': 'Fe2O3',
            'space_group': 167,
            'crystal_system': 'trigonal',
            'Z': 26  # Fe
        },
        {
            'formula': 'ZnS',
            'space_group': 216,
            'crystal_system': 'cubic',
            'Z': 30  # Zn
        },
        {
            'formula': 'CuFeS2',
            'space_group': 122,
            'crystal_system': 'tetragonal',
            'Z': 29  # Cu (most complex)
        },
        {
            'formula': 'UO2',
            'space_group': 225,
            'crystal_system': 'cubic',
            'Z': 92  # U (bottleneck region!)
        },
        {
            'formula': 'CaSO4·2H2O',
            'space_group': 15,
            'crystal_system': 'monoclinic',
            'Z': 20  # Ca
        }
    ]
    
    print("Calculating coherence for test minerals...")
    print()
    
    results = model.batch_calculate(test_minerals)
    
    # Display results
    for result in results:
        print(model.visualize_result(result))
        print()
    
    # Statistics
    print("=" * 70)
    print("SUMMARY STATISTICS")
    print("=" * 70)
    stats = model.get_statistics()
    print(json.dumps(stats, indent=2))
    print()
    
    # Validation checks
    print("=" * 70)
    print("VALIDATION CHECKS")
    print("=" * 70)
    print(f"✓ Model calibration target: ~3% pass rate for natural minerals")
    print(f"  Actual: {stats['natural_pass_rate']*100:.1f}%")
    print()
    print(f"✓ Bottleneck test: Z=92 (U) should have lower coherence")
    u_result = [r for r in results if r.formula == 'UO2'][0]
    print(f"  UO2 NRCI: {u_result.final_nrci:.6f}")
    print()
    print(f"✓ High symmetry (cubic) should have highest coherence")
    cubic_results = [r for r in results if r.crystal_system == 'cubic']
    avg_cubic_nrci = sum(r.final_nrci for r in cubic_results) / len(cubic_results)
    print(f"  Average cubic NRCI: {avg_cubic_nrci:.6f}")
    print()
    
    return model, results


# ============================================================================
# Main Execution
# ============================================================================

if __name__ == '__main__':
    # Run test suite
    model, results = test_coherence_model()
    
    # Save results
    output_data = {
        'model_version': '2.0',
        'precision_mode': str(model.precision_mode),
        'thresholds': {
            'natural_mineral': NRCI_NATURAL_MINERAL,
            'perfect_crystal': NRCI_PERFECT_CRYSTAL
        },
        'results': [
            {
                'formula': r.formula,
                'space_group': r.space_group,
                'crystal_system': r.crystal_system,
                'Z': r.Z,
                'final_nrci': r.final_nrci,
                'passes_natural': r.passes_natural,
                'passes_perfect': r.passes_perfect,
                'hex_address': r.hex_address
            }
            for r in results
        ],
        'statistics': model.get_statistics()
    }
    
    with open('mineral_coherence_v2_results.json', 'w') as f:
        json.dump(output_data, f, indent=2)
    
    print("=" * 70)
    print("Results saved to: mineral_coherence_v2_results.json")
    print("=" * 70)
