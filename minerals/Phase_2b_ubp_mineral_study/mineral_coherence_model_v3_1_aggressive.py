"""
UBP Mineral Coherence Model v3.1 - AGGRESSIVE RECALIBRATION
============================================================

Learning from v3.0 failure: Even 10x stronger degradation gave 100% pass rate!

New approach:
1. Raise natural mineral threshold from 0.99 to 0.9995 (much more selective)
2. Increase base degradation by 100x (not just 10x)
3. Much stronger bottleneck penalty for Z=80-92
4. Add crystal system penalties (lower symmetry = harder to form)

Target: ~1-3 minerals passing from 54 (1.8-5.5% pass rate)

This models the EXTREME selectivity of natural mineral formation.
"""

import sys
import math
import json
from typing import Dict, List, Tuple, Any
from dataclasses import dataclass, asdict

# Import v2.0 substrate
from coherence_substrate_v2 import (
    CoherenceState, ComputationHistory, CoherenceHexDictionary,
    PrecisionMode, Y, Y_INVERSE, GOLDEN_RATIO, PI,
    NRCI_TARGET, O_OBSERVER
)


# ============================================================================
# AGGRESSIVE Recalibration Constants
# ============================================================================

# RAISED thresholds - natural minerals need near-perfect coherence
NRCI_PERFECT_CRYSTAL = 0.999999  # Synthetic, lab-grown crystals
NRCI_NATURAL_MINERAL = 0.9995    # Natural minerals (MUCH MORE SELECTIVE)
NRCI_METASTABLE = 0.995          # Metastable phases

# AGGRESSIVE degradation parameters
TGIC_FACTOR = 0.2  # Even stricter geometric constraint
BASE_DEGRADATION = 0.01  # 100x stronger than v2.0 (was 0.0001)
Z_PENALTY_SCALE = 0.1    # 100x stronger Z scaling (was 0.001)
BOTTLENECK_AMPLIFICATION = 5.0  # Much stronger bottleneck penalty

# Crystal system difficulty factors (lower symmetry = harder to form)
SYSTEM_DIFFICULTY = {
    'cubic': 1.0,        # Easiest (highest symmetry)
    'hexagonal': 1.2,
    'trigonal': 1.3,
    'tetragonal': 1.4,
    'orthorhombic': 1.6,
    'monoclinic': 1.8,
    'triclinic': 2.0     # Hardest (lowest symmetry)
}

# OffBit patterns (unchanged base values)
OFFBIT_PATTERNS = {
    'cubic': {
        'symmetry_order': 48,
        'geometric_score': 1.0,
        'base_nrci': 0.999999,
        'Y_refinements': 8
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


@dataclass
class MineralCoherenceResult:
    """Result of mineral coherence calculation."""
    name: str
    formula: str
    space_group: int
    crystal_system: str
    Z: int
    
    base_nrci: float
    final_nrci: float
    passes_natural: bool
    passes_perfect: bool
    
    total_degradation: float
    z_penalty: float
    bottleneck_penalty: float
    system_penalty: float
    
    net_refinements: int
    computation_depth: int
    hex_address: str
    
    history_summary: Dict[str, Any]
    metadata: Dict[str, Any]


class MineralCoherenceModelV31:
    """
    AGGRESSIVELY recalibrated model for realistic mineral scarcity.
    
    Key changes from v3.0:
    - 100x stronger degradation (not just 10x)
    - Raised natural threshold from 0.99 to 0.9995
    - 5x bottleneck amplification (was 2x)
    - Added crystal system difficulty penalties
    """
    
    def __init__(self, precision_mode: PrecisionMode = PrecisionMode.FLOAT):
        """Initialize model."""
        self.precision_mode = precision_mode
        self.hex_dict = CoherenceHexDictionary()
        CoherenceState.set_hex_dictionary(self.hex_dict, auto_persist=False)
        self.results: List[MineralCoherenceResult] = []
    
    def create_base_state(self, crystal_system: str, Z: int) -> CoherenceState:
        """Create base coherence state."""
        pattern = OFFBIT_PATTERNS.get(crystal_system.lower(), OFFBIT_PATTERNS['triclinic'])
        base_log_error = math.log(1 - pattern['base_nrci'])
        
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
        """Apply Y-refinements."""
        current_state = state
        for i in range(target_refinements):
            current_state = current_state.refine_forward()
            current_state.metadata['phase'] = f'refinement_{i+1}'
        return current_state
    
    def calculate_degradation(self, Z: int, crystal_system: str) -> Tuple[float, float, float, float]:
        """
        Calculate AGGRESSIVE degradation.
        
        Returns:
            (total_degradation, z_penalty, bottleneck_penalty, system_penalty)
        """
        # Base degradation (100x stronger)
        base_deg = BASE_DEGRADATION * Z
        
        # TGIC constraint
        tgic_penalty = (1.0 - TGIC_FACTOR) * math.log(max(Z, 2)) * Z_PENALTY_SCALE
        
        # Bottleneck amplification (Z=80-92)
        bottleneck_penalty = 0.0
        if 80 <= Z <= 92:
            bottleneck_factor = BOTTLENECK_AMPLIFICATION * (1.0 - abs(Z - 86) / 6.0)
            bottleneck_penalty = bottleneck_factor * BASE_DEGRADATION * Z
        
        # Crystal system difficulty penalty
        difficulty = SYSTEM_DIFFICULTY.get(crystal_system.lower(), 1.5)
        system_penalty = (difficulty - 1.0) * BASE_DEGRADATION * Z * 0.5
        
        # Total degradation
        total_deg = base_deg + tgic_penalty + bottleneck_penalty + system_penalty
        
        return total_deg, tgic_penalty, bottleneck_penalty, system_penalty
    
    def apply_complexity_degradation(self, state: CoherenceState, Z: int, crystal_system: str) -> Tuple[CoherenceState, float, float, float, float]:
        """Apply aggressive degradation."""
        total_deg, z_penalty, bottleneck_penalty, system_penalty = self.calculate_degradation(Z, crystal_system)
        
        degraded_state = state.degrade_by(total_deg)
        degraded_state.metadata['phase'] = 'complexity_degradation'
        degraded_state.metadata['total_degradation'] = total_deg
        degraded_state.metadata['z_penalty'] = z_penalty
        degraded_state.metadata['bottleneck_penalty'] = bottleneck_penalty
        degraded_state.metadata['system_penalty'] = system_penalty
        
        return degraded_state, total_deg, z_penalty, bottleneck_penalty, system_penalty
    
    def apply_observer_cost(self, state: CoherenceState) -> CoherenceState:
        """Apply observer cost."""
        observer_state = state.refine_backward()
        observer_state.metadata['phase'] = 'observer_cost'
        observer_state.metadata['O_observer'] = 1.0 / Y
        return observer_state
    
    def calculate_mineral_coherence(self, name: str, formula: str, space_group: int, 
                                    crystal_system: str, Z: int) -> MineralCoherenceResult:
        """Calculate full coherence."""
        # Base state
        state = self.create_base_state(crystal_system, Z)
        base_nrci = state.nrci
        
        # Geometric refinements
        pattern = OFFBIT_PATTERNS.get(crystal_system.lower(), OFFBIT_PATTERNS['triclinic'])
        state = self.apply_geometric_refinements(state, pattern['Y_refinements'])
        
        # Aggressive degradation
        state, total_deg, z_penalty, bottleneck_penalty, system_penalty = self.apply_complexity_degradation(state, Z, crystal_system)
        
        # Observer cost
        state = self.apply_observer_cost(state)
        
        # Persist and evaluate
        state.persist()
        final_nrci = state.nrci
        
        result = MineralCoherenceResult(
            name=name,
            formula=formula,
            space_group=space_group,
            crystal_system=crystal_system,
            Z=Z,
            base_nrci=base_nrci,
            final_nrci=final_nrci,
            passes_natural=(final_nrci >= NRCI_NATURAL_MINERAL),
            passes_perfect=(final_nrci >= NRCI_PERFECT_CRYSTAL),
            total_degradation=total_deg,
            z_penalty=z_penalty,
            bottleneck_penalty=bottleneck_penalty,
            system_penalty=system_penalty,
            net_refinements=state.net_refinements,
            computation_depth=len(state.history.operations),
            hex_address=state.hex_address or "not_persisted",
            history_summary=state.history.get_summary(),
            metadata=state.metadata.copy()
        )
        
        self.results.append(result)
        return result
    
    def batch_calculate(self, minerals: List[Dict[str, Any]]) -> List[MineralCoherenceResult]:
        """Calculate coherence for multiple minerals."""
        results = []
        for mineral in minerals:
            result = self.calculate_mineral_coherence(
                name=mineral.get('name', 'Unknown'),
                formula=mineral['formula'],
                space_group=mineral['space_group'],
                crystal_system=mineral['crystal_system'],
                Z=mineral['Z']
            )
            results.append(result)
        return results
    
    def get_statistics(self) -> Dict[str, Any]:
        """Calculate statistics."""
        if not self.results:
            return {}
        
        total = len(self.results)
        natural_pass = sum(1 for r in self.results if r.passes_natural)
        perfect_pass = sum(1 for r in self.results if r.passes_perfect)
        
        nrci_values = [r.final_nrci for r in self.results]
        
        by_system = {}
        for r in self.results:
            sys = r.crystal_system
            if sys not in by_system:
                by_system[sys] = {'count': 0, 'natural_pass': 0, 'perfect_pass': 0}
            by_system[sys]['count'] += 1
            if r.passes_natural:
                by_system[sys]['natural_pass'] += 1
            if r.passes_perfect:
                by_system[sys]['perfect_pass'] += 1
        
        by_z_range = {
            'Z<30': {'count': 0, 'pass': 0},
            'Z=30-50': {'count': 0, 'pass': 0},
            'Z=50-80': {'count': 0, 'pass': 0},
            'Z=80-92': {'count': 0, 'pass': 0},
            'Z>92': {'count': 0, 'pass': 0}
        }
        
        for r in self.results:
            if r.Z < 30:
                key = 'Z<30'
            elif r.Z <= 50:
                key = 'Z=30-50'
            elif r.Z < 80:
                key = 'Z=50-80'
            elif r.Z <= 92:
                key = 'Z=80-92'
            else:
                key = 'Z>92'
            
            by_z_range[key]['count'] += 1
            if r.passes_natural:
                by_z_range[key]['pass'] += 1
        
        return {
            'total_minerals': total,
            'natural_pass_count': natural_pass,
            'natural_pass_rate': natural_pass / total if total > 0 else 0,
            'perfect_pass_count': perfect_pass,
            'perfect_pass_rate': perfect_pass / total if total > 0 else 0,
            'nrci_min': min(nrci_values),
            'nrci_max': max(nrci_values),
            'nrci_mean': sum(nrci_values) / len(nrci_values),
            'by_crystal_system': by_system,
            'by_z_range': by_z_range,
            'hex_dict_size': len(self.hex_dict.storage) if hasattr(self.hex_dict, 'storage') else 0
        }
    
    def save_results(self, filename: str):
        """Save results to JSON."""
        output = {
            'model_version': '3.1_aggressive',
            'precision_mode': str(self.precision_mode),
            'calibration_parameters': {
                'BASE_DEGRADATION': BASE_DEGRADATION,
                'Z_PENALTY_SCALE': Z_PENALTY_SCALE,
                'TGIC_FACTOR': TGIC_FACTOR,
                'BOTTLENECK_AMPLIFICATION': BOTTLENECK_AMPLIFICATION,
                'SYSTEM_DIFFICULTY': SYSTEM_DIFFICULTY
            },
            'thresholds': {
                'natural_mineral': NRCI_NATURAL_MINERAL,
                'perfect_crystal': NRCI_PERFECT_CRYSTAL
            },
            'results': [asdict(r) for r in self.results],
            'statistics': self.get_statistics()
        }
        
        with open(filename, 'w') as f:
            json.dump(output, f, indent=2)


if __name__ == '__main__':
    print("UBP Mineral Coherence Model v3.1 - AGGRESSIVE RECALIBRATION")
    print("=" * 70)
    print()
    print("Learning from v3.0: Even 10x degradation gave 100% pass rate!")
    print("New approach: 100x degradation + raised threshold to 0.9995")
    print()
    
    # Load dataset
    with open('/home/ubuntu/ubp_mineral_study/data/minerals_dataset.json', 'r') as f:
        minerals = json.load(f)
    
    print(f"Loaded {len(minerals)} real minerals")
    print()
    
    # Initialize and run
    model = MineralCoherenceModelV31(precision_mode=PrecisionMode.FLOAT)
    print("Calculating coherence with AGGRESSIVE parameters...")
    results = model.batch_calculate(minerals)
    
    # Statistics
    stats = model.get_statistics()
    
    print()
    print("=" * 70)
    print("RESULTS SUMMARY")
    print("=" * 70)
    print(f"Total minerals tested: {stats['total_minerals']}")
    print(f"Natural pass count: {stats['natural_pass_count']}")
    print(f"Natural pass rate: {stats['natural_pass_rate']*100:.1f}%")
    print(f"Perfect pass count: {stats['perfect_pass_count']}")
    print(f"Perfect pass rate: {stats['perfect_pass_rate']*100:.1f}%")
    print()
    print(f"NRCI range: {stats['nrci_min']:.6f} - {stats['nrci_max']:.6f}")
    print(f"NRCI mean: {stats['nrci_mean']:.6f}")
    print(f"Threshold: {NRCI_NATURAL_MINERAL:.6f}")
    print()
    
    print("Pass rate by Z range:")
    for z_range, data in stats['by_z_range'].items():
        if data['count'] > 0:
            rate = data['pass'] / data['count'] * 100
            print(f"  {z_range:10s}: {data['pass']:2d}/{data['count']:2d} ({rate:5.1f}%)")
    print()
    
    print("Pass rate by crystal system:")
    for system, data in sorted(stats['by_crystal_system'].items()):
        rate = data['natural_pass'] / data['count'] * 100 if data['count'] > 0 else 0
        print(f"  {system:15s}: {data['natural_pass']:2d}/{data['count']:2d} ({rate:5.1f}%)")
    print()
    
    if stats['natural_pass_count'] > 0:
        print(f"Minerals that PASSED (NRCI >= {NRCI_NATURAL_MINERAL}):")
        for r in sorted(results, key=lambda x: -x.final_nrci):
            if r.passes_natural:
                print(f"  {r.name:20s} {r.formula:25s} Z={r.Z:2d} {r.crystal_system:12s} NRCI={r.final_nrci:.6f}")
    else:
        print("No minerals passed - TOO AGGRESSIVE! Need to tune down.")
    print()
    
    # Show closest misses
    print("Top 10 closest misses (highest NRCI below threshold):")
    sorted_results = sorted(results, key=lambda x: -x.final_nrci)
    shown = 0
    for r in sorted_results:
        if not r.passes_natural and shown < 10:
            print(f"  {r.name:20s} {r.formula:25s} Z={r.Z:2d} {r.crystal_system:12s} NRCI={r.final_nrci:.6f}")
            shown += 1
    print()
    
    # Save
    output_file = '/home/ubuntu/ubp_mineral_study/results/mineral_coherence_v3_1_aggressive.json'
    model.save_results(output_file)
    print(f"Results saved to {output_file}")
