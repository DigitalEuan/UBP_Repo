#!/usr/bin/env python3
"""
UBP 3.4 Chemical Coherence Framework for Fertilizers
Author: Euan Craig, New Zealand
Date: November 2025

Direct application of UBP 3.4 core principles to fertilizer chemistry:
- Molecular coherence (crystalline structure, bond stability)
- Chemical purity and homogeneity
- Nutrient release kinetics
- System-level synergy

NO REALM ANALOGIES - just pure UBP: SOC energy, NRCI, Y constants
"""

import sys
sys.path.append('/home/ubuntu/UBP_Repo/ubp_3.4')

from dataclasses import dataclass
from typing import List, Dict
import numpy as np

# UBP 3.4 core
from soc_energy import SOCCalculator
from y_constants import (
    calculate_y_constant,
    calculate_y_inverse,
    apply_bidirectional_refinement,
    calculate_y_emergent
)
from system_constants import UBPConstants


@dataclass
class FertilizerComponent:
    """
    A single chemical component in a fertilizer blend
    
    UBP Analysis Parameters:
    - molecular_coherence: Crystalline perfection, bond stability (0-1)
    - chemical_purity: Freedom from contaminants (0-1)
    - release_synchrony: Temporal coherence of nutrient release (0-1)
    - concentration: Percentage in blend (0-100)
    """
    name: str
    formula: str
    npk_contribution: tuple  # (N%, P%, K%)
    
    # UBP coherence parameters
    molecular_coherence: float  # 0-1: crystalline structure quality
    chemical_purity: float      # 0-1: freedom from contaminants
    release_synchrony: float    # 0-1: temporal coherence
    concentration: float        # 0-100: % in blend
    
    # Calculated
    nrci: float = 0.0
    soc_energy: float = 0.0


class UBPChemicalFramework:
    """
    Direct UBP 3.4 analysis of fertilizer chemistry
    
    WHY THIS WORKS:
    - Crystalline fertilizers have HIGH molecular coherence
    - Pure compounds have HIGH chemical purity
    - Synchronized release has HIGH temporal coherence
    - UBP naturally rewards these properties with high NRCI
    """
    
    def __init__(self):
        self.soc_calc = SOCCalculator()
        self.Y = calculate_y_constant()
        self.Y_inv = calculate_y_inverse()
        self.O_observer = UBPConstants.O_OBSERVER
        self.PGCI_target = UBPConstants.PGCI_TARGET
        
    def calculate_component_nrci(self, component: FertilizerComponent) -> FertilizerComponent:
        """
        Calculate NRCI for a single fertilizer component
        
        METHODOLOGY:
        1. Modal sum = product of coherence parameters
        2. SOC energy from modal sum
        3. NRCI from SOC energy
        4. Bidirectional refinement for scale optimization
        
        This is PURE UBP - no analogies, just direct calculation
        """
        
        print(f"\n--- Analyzing {component.name} ({component.formula}) ---")
        print(f"Concentration: {component.concentration:.1f}%")
        print(f"NPK contribution: N={component.npk_contribution[0]:.1f}%, "
              f"P={component.npk_contribution[1]:.1f}%, K={component.npk_contribution[2]:.1f}%")
        
        # STEP 1: Modal sum from coherence parameters
        # This represents the "organized structure" of the chemical
        modal_sum = (
            component.molecular_coherence *
            component.chemical_purity *
            component.release_synchrony *
            (component.concentration / 100.0)  # Weight by concentration
        )
        
        print(f"\n[1] MODAL SUM CALCULATION:")
        print(f"  modal_sum = {modal_sum:.6f}")
        print(f"    = molecular_coherence ({component.molecular_coherence:.3f})")
        print(f"    × chemical_purity ({component.chemical_purity:.3f})")
        print(f"    × release_synchrony ({component.release_synchrony:.3f})")
        print(f"    × concentration_weight ({component.concentration/100.0:.3f})")
        
        # STEP 2: Calculate SOC energy
        soc_result = self.soc_calc.calculate_soc_energy(modal_sum=modal_sum)
        
        print(f"\n[2] SOC ENERGY:")
        print(f"  E_SOC = {soc_result.energy_cu:.6e} CU")
        print(f"  Y_emergent = {soc_result.Y_emergent:.15f}")
        
        # STEP 3: Calculate NRCI directly from coherence parameters
        # NRCI = geometric mean of coherence parameters
        # This is the CORRECT approach: coherence parameters → NRCI → SOC energy
        
        nrci_base = (
            component.molecular_coherence *
            component.chemical_purity *
            component.release_synchrony
        ) ** (1/3)  # Geometric mean
        
        # Scale to realistic NRCI range (0.9-0.999)
        # Perfect coherence (1.0, 1.0, 1.0) → NRCI = 0.999
        # Poor coherence (0.5, 0.5, 0.5) → NRCI = 0.900
        nrci = 0.900 + (nrci_base - 0.5) / 0.5 * 0.099
        nrci = max(0.900, min(0.999, nrci))  # Clamp to range
        
        print(f"\n[3] NRCI CALCULATION:")
        print(f"  Coherence parameters geometric mean = {nrci_base:.6f}")
        print(f"  Scaled NRCI = {nrci:.6f}")
        print(f"  (Range: 0.900 for poor quality → 0.999 for perfect quality)")
        
        # STEP 4: Bidirectional refinement for optimization
        # Forward: Geometry → Observer
        nrci_obs = apply_bidirectional_refinement(nrci, 'forward')
        # Backward: Observer → Geometry
        nrci_refined = apply_bidirectional_refinement(nrci_obs, 'backward')
        
        print(f"\n[4] BIDIRECTIONAL REFINEMENT:")
        print(f"  Original NRCI = {nrci:.6f}")
        print(f"  Forward (×Y) = {nrci_obs:.6f}")
        print(f"  Backward (×1/Y) = {nrci_refined:.6f}")
        print(f"  Closure error = {abs(nrci_refined - nrci):.2e}")
        
        # Use refined NRCI
        component.nrci = nrci_refined
        component.soc_energy = soc_result.energy_cu
        
        return component
    
    def analyze_fertilizer_blend(self, components: List[FertilizerComponent]) -> Dict:
        """
        Analyze a complete fertilizer blend
        
        System NRCI = weighted geometric mean of component NRCIs
        Weights = concentration percentages
        """
        
        print("\n" + "="*80)
        print("FERTILIZER BLEND ANALYSIS")
        print("="*80)
        
        # Analyze each component
        analyzed_components = []
        for comp in components:
            analyzed = self.calculate_component_nrci(comp)
            analyzed_components.append(analyzed)
        
        print("\n" + "="*80)
        print("SYSTEM-LEVEL ANALYSIS")
        print("="*80)
        
        # System NRCI: weighted geometric mean
        weights = np.array([c.concentration / 100.0 for c in analyzed_components])
        nrcis = np.array([c.nrci for c in analyzed_components])
        
        # Weighted geometric mean: (∏ NRCI_i^w_i)
        system_nrci = np.prod(nrcis ** weights)
        
        print(f"\nSystem NRCI = {system_nrci:.6f}")
        print(f"  (Weighted geometric mean of {len(analyzed_components)} components)")
        
        # Coherence capacity
        coherence_capacity = (self.PGCI_target - system_nrci) / self.PGCI_target
        print(f"\nCoherence Capacity = {coherence_capacity:.2%}")
        print(f"  (Distance from PGCI target: {self.PGCI_target:.6f})")
        
        # Component contributions
        print(f"\nComponent Contributions:")
        for comp in analyzed_components:
            print(f"  {comp.name:<30} NRCI={comp.nrci:.6f}  Weight={comp.concentration:.1f}%")
        
        # Synergy analysis
        avg_nrci = np.mean(nrcis)
        synergy_factor = system_nrci / avg_nrci
        
        print(f"\nSynergy Factor = {synergy_factor:.4f}")
        if synergy_factor > 1.05:
            print(f"  ✓ POSITIVE SYNERGY (components enhance each other)")
        elif synergy_factor < 0.95:
            print(f"  ✗ NEGATIVE SYNERGY (components interfere)")
        else:
            print(f"  ~ NEUTRAL (independent components)")
        
        return {
            'components': analyzed_components,
            'system_nrci': system_nrci,
            'coherence_capacity': coherence_capacity,
            'synergy_factor': synergy_factor,
            'avg_component_nrci': avg_nrci
        }


def main():
    """Demonstration"""
    
    print("="*80)
    print("UBP 3.4 CHEMICAL COHERENCE FRAMEWORK DEMONSTRATION")
    print("="*80)
    
    framework = UBPChemicalFramework()
    
    # Example: High-quality crystalline fertilizer
    components = [
        FertilizerComponent(
            name="Urea (high-grade crystalline)",
            formula="CO(NH2)2",
            npk_contribution=(46.0, 0.0, 0.0),
            molecular_coherence=0.95,  # Excellent crystalline structure
            chemical_purity=0.98,      # Very pure
            release_synchrony=0.85,    # Moderate release synchrony
            concentration=50.0
        ),
        FertilizerComponent(
            name="Monoammonium phosphate (MAP)",
            formula="NH4H2PO4",
            npk_contribution=(11.0, 52.0, 0.0),
            molecular_coherence=0.92,
            chemical_purity=0.96,
            release_synchrony=0.88,
            concentration=30.0
        ),
        FertilizerComponent(
            name="Potassium chloride (Muriate of potash)",
            formula="KCl",
            npk_contribution=(0.0, 0.0, 60.0),
            molecular_coherence=0.98,  # Excellent crystal structure
            chemical_purity=0.99,      # Very pure
            release_synchrony=0.92,    # Good release
            concentration=20.0
        )
    ]
    
    result = framework.analyze_fertilizer_blend(components)
    
    print("\n" + "="*80)
    print("DEMONSTRATION COMPLETE")
    print("="*80)
    print(f"\nFinal System NRCI: {result['system_nrci']:.6f}")
    print(f"This is {result['system_nrci']/0.999997*100:.2f}% of PGCI target")
    
    return result


if __name__ == '__main__':
    result = main()
