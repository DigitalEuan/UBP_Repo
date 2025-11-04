"""
================================================================================
Universal Binary Principle (UBP) Framework v3.3 - Pharmaceutical Realm
Author: Euan Craig, New Zealand
Date: November 2025
================================================================================

This module implements pharmaceutical realm calculations using UBP 3.3 framework.

The pharmaceutical realm is characterized by:
- Drug-target molecular interactions
- Pharmacological resonance patterns
- Therapeutic efficacy signatures
- Molecular complexity and drug-likeness

Key Features:
- SOC energy calculations for pharmaceutical compounds
- Molecular descriptor integration
- Therapeutic area classification
- Drug-likeness assessment via UBP signatures

Test Phenomena (verifiable against real data):
1. FDA-approved pharmaceutical compounds from ChEMBL
2. Molecular weight and LogP distributions
3. Therapeutic efficacy correlations
"""

import math
import numpy as np
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass

# UBP 3.3 modules
from system_constants import UBPConstants
from y_constants import get_y_correction_for_realm
from soc_energy import SOCCalculator, SOCEnergyResult
from observer_framework import get_default_realm_observer_costs
from wall_of_reality import WallOfReality


@dataclass
class PharmaceuticalState:
    """
    Represents a pharmaceutical compound state.
    
    Attributes:
        molecular_weight: Molecular weight (Da)
        logp: Lipophilicity (LogP)
        complexity: Bertz complexity index
        hbd: Hydrogen bond donors
        hba: Hydrogen bond acceptors
        tpsa: Topological polar surface area (Ų)
        rotatable_bonds: Number of rotatable bonds
        aromatic_rings: Number of aromatic rings
        heavy_atoms: Number of heavy atoms
        therapeutic_area: Therapeutic classification
    """
    molecular_weight: float
    logp: float
    complexity: float
    hbd: int
    hba: int
    tpsa: float
    rotatable_bonds: int
    aromatic_rings: int
    heavy_atoms: int
    therapeutic_area: str


class PharmaceuticalRealm:
    """
    Pharmaceutical realm calculator using UBP 3.3 framework.
    """
    
    # Realm-specific constants
    REALM_NAME = "pharmaceutical"
    BASE_CRV = UBPConstants.CRV_BIOLOGICAL_BASE  # π/e (similar to biological)
    TOGGLE_PROBABILITY = 0.6  # Higher than biological due to specific interactions
    
    # Pharmaceutical constants
    BOLTZMANN_CONSTANT = UBPConstants.BOLTZMANN_CONSTANT
    PHYSIOLOGICAL_TEMP_K = 310.15  # 37°C body temperature
    
    # Drug-likeness thresholds (Lipinski's Rule of 5)
    LIPINSKI_MW_MAX = 500.0
    LIPINSKI_LOGP_MAX = 5.0
    LIPINSKI_HBD_MAX = 5
    LIPINSKI_HBA_MAX = 10
    
    # Therapeutic area weights for CRV adjustment
    THERAPEUTIC_WEIGHTS = {
        'Oncology': 1.3,  # Higher complexity
        'CNS/Neurology': 1.2,  # Blood-brain barrier considerations
        'Cardiovascular': 1.1,
        'Anti-infective': 1.0,
        'Metabolic': 1.15,
        'Immunology': 1.25,
        'Pain/Inflammation': 0.95,
        'Other': 1.0
    }
    
    def __init__(self):
        """Initialize pharmaceutical realm calculator."""
        self.soc_calc = SOCCalculator()
        self.wall = WallOfReality()
        
        # Use biological realm Y correction as pharmaceutical is similar
        self.y_correction = get_y_correction_for_realm("biological")
        
        # Get realm-specific observer cost
        realm_costs = get_default_realm_observer_costs(UBPConstants.O_OBSERVER)
        self.observer_cost = realm_costs.get("biological", UBPConstants.O_OBSERVER)
    
    def calculate_pharmaceutical_energy_soc(
        self,
        pharm_state: PharmaceuticalState
    ) -> SOCEnergyResult:
        """
        Calculate pharmaceutical energy using SOC equation.
        
        The SOC (Spin-Orbit Coupling) energy equation captures the
        informational complexity and resonance of pharmaceutical compounds.
        
        Args:
            pharm_state: Pharmaceutical compound state
            
        Returns:
            SOCEnergyResult with energy, NRCI, and CRV
        """
        # Calculate M (information/mass term)
        # Normalize molecular weight to typical drug range (150-500 Da)
        normalized_mw = pharm_state.molecular_weight / 325.0  # Mean drug MW
        
        # Calculate C (characteristic frequency/rate)
        # Use complexity as a proxy for molecular vibration modes
        # Higher complexity → more vibrational modes → higher frequency
        complexity_factor = pharm_state.complexity / 1000.0  # Normalize Bertz CT
        characteristic_freq = complexity_factor * 1e12  # THz range for molecular vibrations
        
        # Calculate R (resonance strength)
        # Based on drug-likeness and molecular properties
        resonance = self._calculate_resonance_strength(pharm_state)
        
        # Calculate CRV (Computational Resonance Value)
        crv = self._calculate_crv(pharm_state)
        
        # Calculate NRCI (Non-Random Coherence Index)
        nrci = self._calculate_nrci(pharm_state)
        
        # Calculate modal sum from molecular properties
        # Use normalized descriptors as modal values
        weights = np.array([0.3, 0.25, 0.2, 0.15, 0.1])  # Weighted importance
        modes = np.array([
            normalized_mw,           # Molecular weight contribution
            resonance,               # Drug-likeness resonance
            complexity_factor,       # Structural complexity
            crv / self.BASE_CRV,    # CRV contribution (normalized)
            nrci - 0.99999          # NRCI contribution (scaled)
        ])
        
        modal_sum = self.soc_calc.calculate_modal_sum(weights, modes)
        
        # Use SOC calculator with correct API
        result = self.soc_calc.calculate_soc_energy(
            modal_sum=modal_sum
        )
        
        # Add pharmaceutical-specific attributes to result
        result.nrci = nrci
        result.crv = crv
        result.energy = result.energy_cu  # Add energy attribute for compatibility
        
        return result
    
    def _calculate_resonance_strength(self, pharm_state: PharmaceuticalState) -> float:
        """
        Calculate resonance strength based on drug-likeness.
        
        Higher resonance indicates better drug-like properties and
        potential for therapeutic efficacy.
        """
        # Lipinski violations penalty
        violations = 0
        if pharm_state.molecular_weight > self.LIPINSKI_MW_MAX:
            violations += 1
        if pharm_state.logp > self.LIPINSKI_LOGP_MAX:
            violations += 1
        if pharm_state.hbd > self.LIPINSKI_HBD_MAX:
            violations += 1
        if pharm_state.hba > self.LIPINSKI_HBA_MAX:
            violations += 1
        
        # Base resonance (0.5 to 1.0)
        base_resonance = 1.0 - (violations * 0.1)
        
        # Adjust for optimal ranges
        # LogP sweet spot: 2-3
        logp_factor = 1.0 - abs(pharm_state.logp - 2.5) / 5.0
        logp_factor = max(0.5, min(1.0, logp_factor))
        
        # TPSA sweet spot: 40-90 Ų
        tpsa_factor = 1.0 - abs(pharm_state.tpsa - 65.0) / 100.0
        tpsa_factor = max(0.5, min(1.0, tpsa_factor))
        
        # Rotatable bonds (flexibility): prefer 5-10
        rb_factor = 1.0 - abs(pharm_state.rotatable_bonds - 7.5) / 15.0
        rb_factor = max(0.5, min(1.0, rb_factor))
        
        # Aromatic rings (rigidity): prefer 2-3
        ar_factor = 1.0 - abs(pharm_state.aromatic_rings - 2.5) / 5.0
        ar_factor = max(0.5, min(1.0, ar_factor))
        
        # Combine factors
        resonance = base_resonance * logp_factor * tpsa_factor * rb_factor * ar_factor
        
        return max(0.1, min(1.0, resonance))
    
    def _calculate_crv(self, pharm_state: PharmaceuticalState) -> float:
        """
        Calculate Computational Resonance Value for pharmaceutical compound.
        
        CRV encodes the informational pattern and therapeutic potential.
        """
        # Base CRV from biological realm
        base_crv = self.BASE_CRV
        
        # Adjust for therapeutic area
        therapeutic_weight = self.THERAPEUTIC_WEIGHTS.get(
            pharm_state.therapeutic_area, 1.0
        )
        
        # Adjust for molecular complexity
        # Higher complexity → higher CRV (more information)
        complexity_factor = 1.0 + (pharm_state.complexity / 2000.0)
        
        # Adjust for heavy atom count (proxy for information content)
        heavy_atom_factor = 1.0 + (pharm_state.heavy_atoms / 100.0)
        
        crv = base_crv * therapeutic_weight * complexity_factor * heavy_atom_factor
        
        return crv
    
    def _calculate_nrci(self, pharm_state: PharmaceuticalState) -> float:
        """
        Calculate Non-Random Coherence Index for pharmaceutical compound.
        
        NRCI measures the coherence and non-randomness of the molecular pattern.
        Higher NRCI indicates more ordered, drug-like structure.
        """
        # Base coherence from drug-likeness
        drug_like_score = self._calculate_drug_likeness_score(pharm_state)
        
        # Structural coherence from aromatic content
        # Aromatic rings provide structural rigidity and coherence
        aromatic_coherence = min(1.0, pharm_state.aromatic_rings / 5.0)
        
        # Complexity coherence (normalized Bertz CT)
        # Moderate complexity is optimal (too low = too simple, too high = too complex)
        optimal_complexity = 900.0
        complexity_coherence = 1.0 - abs(pharm_state.complexity - optimal_complexity) / 1500.0
        complexity_coherence = max(0.5, min(1.0, complexity_coherence))
        
        # Combine coherence factors
        base_nrci = (drug_like_score * 0.4 + 
                     aromatic_coherence * 0.3 + 
                     complexity_coherence * 0.3)
        
        # Scale to UBP NRCI range (typically > 0.99999)
        # Pharmaceutical compounds are highly ordered, so high NRCI
        nrci = 0.99999 + (base_nrci * 0.000009)
        
        return nrci
    
    def _calculate_drug_likeness_score(self, pharm_state: PharmaceuticalState) -> float:
        """
        Calculate overall drug-likeness score (0-1).
        """
        # Lipinski violations
        violations = 0
        if pharm_state.molecular_weight > self.LIPINSKI_MW_MAX:
            violations += 1
        if pharm_state.logp > self.LIPINSKI_LOGP_MAX:
            violations += 1
        if pharm_state.hbd > self.LIPINSKI_HBD_MAX:
            violations += 1
        if pharm_state.hba > self.LIPINSKI_HBA_MAX:
            violations += 1
        
        # Score: 1.0 for 0 violations, decreasing by 0.2 per violation
        score = 1.0 - (violations * 0.2)
        
        return max(0.0, score)
    
    def analyze_compound(
        self,
        compound_data: Dict
    ) -> Dict:
        """
        Perform complete UBP analysis on a pharmaceutical compound.
        
        Args:
            compound_data: Dictionary with molecular descriptors
            
        Returns:
            Dictionary with UBP analysis results
        """
        # Create pharmaceutical state
        pharm_state = PharmaceuticalState(
            molecular_weight=compound_data['molecular_weight'],
            logp=compound_data['logp'],
            complexity=compound_data['complexity'],
            hbd=compound_data['hbd'],
            hba=compound_data['hba'],
            tpsa=compound_data['tpsa'],
            rotatable_bonds=compound_data['rotatable_bonds'],
            aromatic_rings=compound_data['aromatic_rings'],
            heavy_atoms=compound_data['heavy_atoms'],
            therapeutic_area=compound_data.get('therapeutic_area', 'Other')
        )
        
        # Calculate SOC energy
        soc_result = self.calculate_pharmaceutical_energy_soc(pharm_state)
        
        # Calculate additional metrics
        resonance = self._calculate_resonance_strength(pharm_state)
        drug_likeness = self._calculate_drug_likeness_score(pharm_state)
        
        # Compile results
        results = {
            'chembl_id': compound_data.get('chembl_id', 'Unknown'),
            'name': compound_data.get('name', 'Unknown'),
            'therapeutic_area': pharm_state.therapeutic_area,
            
            # UBP metrics
            'ubp_energy': soc_result.energy,
            'ubp_nrci': soc_result.nrci,
            'ubp_crv': soc_result.crv,
            'ubp_resonance': resonance,
            
            # Pharmaceutical metrics
            'drug_likeness_score': drug_likeness,
            'molecular_weight': pharm_state.molecular_weight,
            'logp': pharm_state.logp,
            'complexity': pharm_state.complexity,
            'heavy_atoms': pharm_state.heavy_atoms,
            'aromatic_rings': pharm_state.aromatic_rings,
            
            # Derived insights
            'ubp_therapeutic_potential': resonance * drug_likeness,
            'ubp_complexity_index': soc_result.crv / self.BASE_CRV
        }
        
        return results
    
    def batch_analyze_compounds(
        self,
        compounds_list: List[Dict]
    ) -> List[Dict]:
        """
        Analyze multiple compounds in batch.
        
        Args:
            compounds_list: List of compound dictionaries
            
        Returns:
            List of analysis result dictionaries
        """
        results = []
        
        for compound_data in compounds_list:
            try:
                result = self.analyze_compound(compound_data)
                results.append(result)
            except Exception as e:
                print(f"Error analyzing compound {compound_data.get('chembl_id', 'Unknown')}: {e}")
                # Add error result
                results.append({
                    'chembl_id': compound_data.get('chembl_id', 'Unknown'),
                    'error': str(e)
                })
        
        return results


def test_pharmaceutical_realm():
    """
    Test pharmaceutical realm with example compounds.
    """
    print("="*80)
    print("UBP 3.3 Pharmaceutical Realm Test")
    print("="*80 + "\n")
    
    # Example compounds
    test_compounds = [
        {
            'chembl_id': 'CHEMBL25',
            'name': 'Aspirin',
            'molecular_weight': 180.16,
            'logp': 1.19,
            'complexity': 212.0,
            'hbd': 1,
            'hba': 4,
            'tpsa': 63.6,
            'rotatable_bonds': 3,
            'aromatic_rings': 1,
            'heavy_atoms': 13,
            'therapeutic_area': 'Pain/Inflammation'
        },
        {
            'chembl_id': 'CHEMBL1201585',
            'name': 'Imatinib',
            'molecular_weight': 493.60,
            'logp': 4.45,
            'complexity': 1050.0,
            'hbd': 2,
            'hba': 7,
            'tpsa': 86.4,
            'rotatable_bonds': 9,
            'aromatic_rings': 4,
            'heavy_atoms': 36,
            'therapeutic_area': 'Oncology'
        }
    ]
    
    realm = PharmaceuticalRealm()
    
    for compound in test_compounds:
        print(f"\nAnalyzing: {compound['name']} ({compound['chembl_id']})")
        print("-" * 60)
        
        result = realm.analyze_compound(compound)
        
        print(f"Therapeutic Area: {result['therapeutic_area']}")
        print(f"Molecular Weight: {result['molecular_weight']:.2f} Da")
        print(f"LogP: {result['logp']:.2f}")
        print(f"Complexity: {result['complexity']:.1f}")
        print(f"\nUBP Metrics:")
        print(f"  Energy: {result['ubp_energy']:.6e} J")
        print(f"  NRCI: {result['ubp_nrci']:.10f}")
        print(f"  CRV: {result['ubp_crv']:.6f}")
        print(f"  Resonance: {result['ubp_resonance']:.4f}")
        print(f"\nDrug-likeness Score: {result['drug_likeness_score']:.4f}")
        print(f"Therapeutic Potential: {result['ubp_therapeutic_potential']:.4f}")
        print(f"Complexity Index: {result['ubp_complexity_index']:.4f}")


if __name__ == "__main__":
    test_pharmaceutical_realm()
