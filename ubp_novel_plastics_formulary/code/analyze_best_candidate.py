#!/usr/bin/env python3
"""
Detailed Analysis of Best Carousel Candidate
Generates proxy SMILES, calculates molecular properties, and formulates synthesis recipe

Author: Euan R A Craig, New Zealand
Date: October 14, 2025
"""
import sys
import json
import numpy as np
from typing import Dict, List, Tuple

# RDKit imports
try:
    from rdkit import Chem
    from rdkit.Chem import Descriptors, AllChem, rdMolDescriptors
    RDKIT_AVAILABLE = True
except ImportError:
    print("Warning: RDKit not available. Molecular analysis will be limited.")
    RDKIT_AVAILABLE = False


def load_best_candidate(filepath: str) -> Dict:
    """Load the best candidate from carousel results"""
    with open(filepath, 'r') as f:
        data = json.load(f)
    return data['best_candidate']


def composition_to_empirical_formula(composition: Dict[str, float]) -> str:
    """
    Convert elemental composition (weight %) to empirical formula.
    
    This is a simplified approximation for polymer repeat units.
    """
    # Convert weight % to molar ratios
    atomic_weights = {
        'C': 12.011, 'H': 1.008, 'O': 15.999, 'N': 14.007,
        'Si': 28.085, 'F': 18.998, 'Cl': 35.45, 'S': 32.06,
        'P': 30.974, 'Br': 79.904
    }
    
    molar_ratios = {}
    for elem, wt_pct in composition.items():
        if elem in atomic_weights and wt_pct > 0:
            molar_ratios[elem] = wt_pct / atomic_weights[elem]
    
    # Normalize to smallest ratio
    if not molar_ratios:
        return "Unknown"
    
    min_ratio = min(molar_ratios.values())
    normalized = {elem: ratio / min_ratio for elem, ratio in molar_ratios.items()}
    
    # Round to nearest integer for empirical formula
    empirical = {}
    for elem, ratio in normalized.items():
        count = round(ratio)
        if count > 0:
            empirical[elem] = count
    
    # Format as chemical formula
    formula_parts = []
    # Standard order: C, H, then alphabetical
    if 'C' in empirical:
        formula_parts.append(f"C{empirical['C']}" if empirical['C'] > 1 else "C")
    if 'H' in empirical:
        formula_parts.append(f"H{empirical['H']}" if empirical['H'] > 1 else "H")
    for elem in sorted(empirical.keys()):
        if elem not in ['C', 'H']:
            count = empirical[elem]
            formula_parts.append(f"{elem}{count}" if count > 1 else elem)
    
    return ''.join(formula_parts)


def generate_proxy_smiles(composition: Dict[str, float]) -> Tuple[str, str]:
    """
    Generate a proxy SMILES string for the polymer based on composition.
    
    Returns: (monomer_smiles, polymer_description)
    
    This is a heuristic approach based on the elemental composition.
    """
    C_pct = composition.get('C', 0)
    H_pct = composition.get('H', 0)
    O_pct = composition.get('O', 0)
    N_pct = composition.get('N', 0)
    Cl_pct = composition.get('Cl', 0)
    F_pct = composition.get('F', 0)
    Si_pct = composition.get('Si', 0)
    
    # Base structure determination
    if C_pct > 80 and H_pct > 10 and O_pct < 1 and N_pct < 1:
        # Hydrocarbon polymer (PP-like)
        if Cl_pct > 0.3:
            # Chlorinated hydrocarbon
            smiles = "CC(Cl)C"
            description = "Chlorinated polypropylene-like structure"
        elif F_pct > 0.3:
            # Fluorinated hydrocarbon
            smiles = "CC(F)C"
            description = "Fluorinated polypropylene-like structure"
        else:
            # Standard PP
            smiles = "CC(C)C"
            description = "Polypropylene-like structure"
    
    elif O_pct > 5:
        # Oxygen-containing polymer
        if N_pct > 2:
            # Polyamide-like
            smiles = "CC(=O)NCCCC"
            description = "Polyamide-like structure with ether/ester groups"
        else:
            # Polyester or polyether
            smiles = "CC(=O)OCC"
            description = "Polyester-like structure"
    
    elif N_pct > 5:
        # Nitrogen-rich polymer
        smiles = "CC(C)NC(=O)C"
        description = "Polyamide-like structure"
    
    elif Si_pct > 1:
        # Siloxane-containing
        smiles = "C[Si](C)(C)O[Si](C)(C)C"
        description = "Siloxane-modified polymer"
    
    else:
        # Default to modified PP
        smiles = "CC(C)C"
        description = "Modified polypropylene structure"
    
    return smiles, description


def calculate_molecular_properties(smiles: str) -> Dict[str, float]:
    """
    Calculate molecular descriptors using RDKit.
    """
    if not RDKIT_AVAILABLE:
        return {
            'molecular_weight': 0.0,
            'logP': 0.0,
            'tpsa': 0.0,
            'h_bond_donors': 0,
            'h_bond_acceptors': 0,
            'rotatable_bonds': 0,
            'aromatic_rings': 0
        }
    
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        print(f"Warning: Could not parse SMILES: {smiles}")
        return {}
    
    properties = {
        'molecular_weight': Descriptors.MolWt(mol),
        'logP': Descriptors.MolLogP(mol),
        'tpsa': Descriptors.TPSA(mol),
        'h_bond_donors': Descriptors.NumHDonors(mol),
        'h_bond_acceptors': Descriptors.NumHAcceptors(mol),
        'rotatable_bonds': Descriptors.NumRotatableBonds(mol),
        'aromatic_rings': Descriptors.NumAromaticRings(mol)
    }
    
    return properties


def formulate_synthesis_recipe(composition: Dict[str, float],
                               empirical_formula: str,
                               properties: Dict[str, float]) -> Dict[str, any]:
    """
    Generate a detailed synthesis recipe based on composition and properties.
    
    This uses polymer chemistry principles to suggest realistic synthesis routes.
    """
    C_pct = composition.get('C', 0)
    H_pct = composition.get('H', 0)
    O_pct = composition.get('O', 0)
    N_pct = composition.get('N', 0)
    Cl_pct = composition.get('Cl', 0)
    F_pct = composition.get('F', 0)
    Si_pct = composition.get('Si', 0)
    
    # Determine synthesis route
    if C_pct > 80 and H_pct > 10 and O_pct < 1 and N_pct < 1:
        # Polyolefin route (Ziegler-Natta or metallocene catalysis)
        synthesis_method = "Ziegler-Natta Catalyzed Polymerization"
        
        # Calculate monomer ratios for 100g batch
        # Assume propylene as base monomer
        propylene_mass = 85.0  # g (base)
        
        reagents = [
            {
                'name': 'Propylene',
                'formula': 'C3H6',
                'mass': propylene_mass,
                'role': 'Primary monomer'
            }
        ]
        
        # Add functional monomers based on heteroatoms
        if Cl_pct > 0.1:
            chlorinated_monomer_mass = (Cl_pct / 100.0) * 100.0 * 2.5  # Scale factor
            reagents.append({
                'name': '3-Chloro-1-propene (Allyl chloride)',
                'formula': 'C3H5Cl',
                'mass': min(chlorinated_monomer_mass, 5.0),
                'role': 'Chlorinated comonomer'
            })
        
        if F_pct > 0.1:
            fluorinated_monomer_mass = (F_pct / 100.0) * 100.0 * 2.5
            reagents.append({
                'name': 'Vinylidene fluoride',
                'formula': 'C2H2F2',
                'mass': min(fluorinated_monomer_mass, 3.0),
                'role': 'Fluorinated comonomer'
            })
        
        if O_pct > 0.1:
            oxygen_monomer_mass = (O_pct / 100.0) * 100.0 * 3.0
            reagents.append({
                'name': 'Maleic anhydride',
                'formula': 'C4H2O3',
                'mass': min(oxygen_monomer_mass, 2.0),
                'role': 'Oxygen-containing comonomer (grafting agent)'
            })
        
        if N_pct > 0.1:
            nitrogen_monomer_mass = (N_pct / 100.0) * 100.0 * 3.0
            reagents.append({
                'name': 'Acrylonitrile',
                'formula': 'C3H3N',
                'mass': min(nitrogen_monomer_mass, 2.0),
                'role': 'Nitrogen-containing comonomer'
            })
        
        if Si_pct > 0.1:
            silane_mass = (Si_pct / 100.0) * 100.0 * 2.0
            reagents.append({
                'name': 'Vinyltrimethoxysilane',
                'formula': 'C5H12O3Si',
                'mass': min(silane_mass, 1.5),
                'role': 'Silane coupling agent'
            })
        
        # Catalyst system
        reagents.extend([
            {
                'name': 'Titanium tetrachloride (TiCl4)',
                'formula': 'TiCl4',
                'mass': 0.5,
                'role': 'Ziegler-Natta catalyst component'
            },
            {
                'name': 'Triethylaluminum (TEA)',
                'formula': 'Al(C2H5)3',
                'mass': 0.3,
                'role': 'Cocatalyst'
            },
            {
                'name': 'Hexane',
                'formula': 'C6H14',
                'mass': 200.0,
                'role': 'Solvent (anhydrous)'
            }
        ])
        
        # Synthesis steps
        steps = [
            {
                'number': 1,
                'title': 'Catalyst Preparation',
                'description': 'In a glove box under inert atmosphere (nitrogen or argon), prepare the Ziegler-Natta catalyst system by combining TiCl4 and TEA in anhydrous hexane. Stir for 30 minutes at room temperature to activate the catalyst.',
                'conditions': 'Inert atmosphere, room temperature, 30 min',
                'equipment': 'Glove box, magnetic stirrer'
            },
            {
                'number': 2,
                'title': 'Reactor Setup',
                'description': 'Transfer the catalyst solution to a 1L stainless steel autoclave reactor. Purge the reactor with nitrogen three times to remove all oxygen and moisture.',
                'conditions': 'Nitrogen atmosphere, room temperature',
                'equipment': '1L autoclave reactor with pressure gauge and temperature control'
            },
            {
                'number': 3,
                'title': 'Monomer Addition and Polymerization',
                'description': 'Cool the reactor to 0°C. Add the monomer mixture (propylene and comonomers) slowly through a pressure-regulated feed line. Heat the reactor to 60-70°C and maintain pressure at 5-10 bar. Allow polymerization to proceed for 4-6 hours with continuous stirring (300 rpm).',
                'conditions': '60-70°C, 5-10 bar, 4-6 hours, 300 rpm stirring',
                'equipment': 'Autoclave with temperature and pressure control, overhead stirrer'
            },
            {
                'number': 4,
                'title': 'Quenching and Precipitation',
                'description': 'After polymerization is complete, cool the reactor to room temperature and carefully vent excess pressure. Add 500 mL of acidified methanol (1% HCl) to quench the catalyst and precipitate the polymer. Stir for 1 hour.',
                'conditions': 'Room temperature, 1 hour',
                'equipment': 'Fume hood, large beaker'
            },
            {
                'number': 5,
                'title': 'Purification',
                'description': 'Filter the precipitated polymer through a Buchner funnel. Wash thoroughly with methanol (3 × 200 mL) to remove catalyst residues, then with deionized water (2 × 200 mL). Dry the polymer in a vacuum oven at 60°C for 24 hours.',
                'conditions': '60°C, vacuum, 24 hours',
                'equipment': 'Buchner funnel, vacuum oven'
            },
            {
                'number': 6,
                'title': 'Post-Processing (Optional)',
                'description': 'For improved properties, the dried polymer can be melt-blended with stabilizers and antioxidants using a twin-screw extruder at 180-200°C. Pelletize the extrudate for injection molding.',
                'conditions': '180-200°C, twin-screw extruder',
                'equipment': 'Twin-screw extruder, pelletizer'
            }
        ]
        
    else:
        # Default to free radical polymerization for more complex compositions
        synthesis_method = "Free Radical Polymerization"
        
        reagents = [
            {
                'name': 'Vinyl monomer mixture',
                'formula': empirical_formula,
                'mass': 80.0,
                'role': 'Monomer blend'
            },
            {
                'name': 'Azobisisobutyronitrile (AIBN)',
                'formula': 'C8H12N4',
                'mass': 0.5,
                'role': 'Free radical initiator'
            },
            {
                'name': 'Toluene',
                'formula': 'C7H8',
                'mass': 150.0,
                'role': 'Solvent'
            }
        ]
        
        steps = [
            {
                'number': 1,
                'title': 'Monomer Preparation',
                'description': 'Combine all monomers in the specified ratios in a clean, dry flask. Degas by bubbling nitrogen through the mixture for 30 minutes.',
                'conditions': 'Room temperature, nitrogen purge, 30 min',
                'equipment': '500 mL three-neck round-bottom flask'
            },
            {
                'number': 2,
                'title': 'Polymerization',
                'description': 'Add AIBN initiator to the degassed monomer mixture. Heat to 70°C under nitrogen atmosphere with continuous stirring. Allow polymerization to proceed for 8-12 hours.',
                'conditions': '70°C, nitrogen atmosphere, 8-12 hours',
                'equipment': 'Oil bath, reflux condenser, magnetic stirrer'
            },
            {
                'number': 3,
                'title': 'Precipitation and Purification',
                'description': 'Pour the reaction mixture into 1L of cold methanol to precipitate the polymer. Filter, wash with methanol, and dry in vacuum oven at 50°C for 24 hours.',
                'conditions': '50°C, vacuum, 24 hours',
                'equipment': 'Buchner funnel, vacuum oven'
            }
        ]
    
    recipe = {
        'synthesis_method': synthesis_method,
        'batch_size': '100g polymer (theoretical yield)',
        'reagents': reagents,
        'synthesis_steps': steps,
        'safety_notes': [
            'All polymerization reactions must be conducted in a well-ventilated fume hood.',
            'Organometallic catalysts (TiCl4, TEA) are highly reactive with moisture and oxygen. Handle only in inert atmosphere.',
            'Monomers are flammable and may be toxic. Use appropriate PPE (gloves, safety glasses, lab coat).',
            'High-pressure reactors require proper training and safety protocols.',
            'Dispose of all chemical waste according to institutional guidelines.'
        ]
    }
    
    return recipe


def generate_verification_protocol(properties: Dict[str, float],
                                   ubp_metrics: Dict[str, float]) -> List[Dict]:
    """
    Generate analytical verification tests for the synthesized polymer.
    """
    tests = [
        {
            'technique': 'Fourier Transform Infrared Spectroscopy (FTIR)',
            'purpose': 'Confirm functional groups and chemical structure',
            'expected_peaks': [
                '2950-2850 cm⁻¹: C-H stretching (alkyl)',
                '1460-1370 cm⁻¹: C-H bending',
                '1730 cm⁻¹: C=O stretching (if O present)',
                '1650 cm⁻¹: C=C stretching (if unsaturation present)',
                '750-650 cm⁻¹: C-Cl stretching (if Cl present)',
                '1100-1000 cm⁻¹: C-F stretching (if F present)'
            ],
            'acceptance_criteria': 'Spectrum matches expected functional groups based on composition'
        },
        {
            'technique': 'Nuclear Magnetic Resonance (NMR) Spectroscopy',
            'purpose': 'Determine polymer microstructure and comonomer incorporation',
            'method': '¹H NMR and ¹³C NMR in CDCl₃ or d₆-DMSO',
            'expected_signals': 'Signals consistent with propylene backbone and comonomer units',
            'acceptance_criteria': 'Integration ratios match expected composition within ±5%'
        },
        {
            'technique': 'Gel Permeation Chromatography (GPC)',
            'purpose': 'Determine molecular weight and polydispersity',
            'expected_results': f'Mn: 50,000-150,000 g/mol, PDI: 2.0-4.0 (typical for Ziegler-Natta)',
            'acceptance_criteria': 'Molecular weight distribution is monomodal'
        },
        {
            'technique': 'Differential Scanning Calorimetry (DSC)',
            'purpose': 'Measure thermal transitions (Tg, Tm)',
            'expected_results': f'Tg ≈ {properties.get("glass_transition_temp", 80):.0f}°C, Tm ≈ {properties.get("melting_point", 180):.0f}°C',
            'acceptance_criteria': 'Thermal transitions within ±10°C of predicted values'
        },
        {
            'technique': 'Tensile Testing (ASTM D638)',
            'purpose': 'Measure mechanical properties',
            'method': 'Injection-molded dog-bone specimens, tested at 23°C, 50% RH, 50 mm/min strain rate',
            'expected_results': f'Tensile Strength ≥ {properties.get("tensile_strength", 450):.0f} MPa, Elongation at Break ≈ {properties.get("ductility", 80):.0f}%',
            'acceptance_criteria': 'Tensile strength within ±15% of predicted value'
        },
        {
            'technique': 'Shore D Hardness Testing (ASTM D2240)',
            'purpose': 'Measure surface hardness',
            'expected_results': f'Shore D ≈ {properties.get("hardness", 900)/10:.0f}',  # Convert to Shore D scale
            'acceptance_criteria': 'Hardness within ±5 Shore D units of predicted value'
        },
        {
            'technique': 'Thermogravimetric Analysis (TGA)',
            'purpose': 'Assess thermal stability and decomposition temperature',
            'expected_results': 'Onset of decomposition > 300°C, 5% weight loss temperature > 350°C',
            'acceptance_criteria': 'Thermal stability suitable for processing at 180-200°C'
        }
    ]
    
    return tests


def main():
    """
    Main analysis routine for best carousel candidate.
    """
    print("\n" + "="*80)
    print("DETAILED ANALYSIS OF BEST CAROUSEL CANDIDATE")
    print("="*80 + "\n")
    
    # Load best candidate
    candidate = load_best_candidate('/home/ubuntu/carousel_pilot_results.json')
    
    composition = candidate['composition']
    properties = candidate['properties']
    ubp_metrics = candidate['ubp_metrics']
    
    print("Candidate Overview:")
    print(f"  Optimization Score: {candidate['optimization_score']:.4f}")
    print(f"  Overall Coherence: {ubp_metrics['overall_coherence']:.4f}")
    print(f"  Generation: {candidate['generation']}")
    print(f"  Confidence: {candidate['confidence']:.4f}\n")
    
    # Generate empirical formula
    print("Calculating empirical formula...")
    empirical_formula = composition_to_empirical_formula(composition)
    print(f"  Empirical Formula: {empirical_formula}\n")
    
    # Generate proxy SMILES
    print("Generating proxy molecular structure...")
    smiles, description = generate_proxy_smiles(composition)
    print(f"  Proxy SMILES: {smiles}")
    print(f"  Description: {description}\n")
    
    # Calculate molecular properties
    print("Calculating molecular descriptors...")
    mol_properties = calculate_molecular_properties(smiles)
    if mol_properties:
        print(f"  Molecular Weight: {mol_properties.get('molecular_weight', 0):.2f} g/mol")
        print(f"  LogP (Hydrophobicity): {mol_properties.get('logP', 0):.2f}")
        print(f"  TPSA (Polar Surface Area): {mol_properties.get('tpsa', 0):.2f} Ų")
        print(f"  H-Bond Donors: {mol_properties.get('h_bond_donors', 0)}")
        print(f"  H-Bond Acceptors: {mol_properties.get('h_bond_acceptors', 0)}")
        print(f"  Rotatable Bonds: {mol_properties.get('rotatable_bonds', 0)}\n")
    
    # Formulate synthesis recipe
    print("Formulating synthesis recipe...")
    recipe = formulate_synthesis_recipe(composition, empirical_formula, properties)
    print(f"  Synthesis Method: {recipe['synthesis_method']}")
    print(f"  Number of Steps: {len(recipe['synthesis_steps'])}\n")
    
    # Generate verification protocol
    print("Generating verification protocol...")
    verification = generate_verification_protocol(properties, ubp_metrics)
    print(f"  Number of Verification Tests: {len(verification)}\n")
    
    # Save complete analysis
    analysis = {
        'candidate_info': candidate,
        'empirical_formula': empirical_formula,
        'proxy_smiles': smiles,
        'structure_description': description,
        'molecular_properties': mol_properties,
        'synthesis_recipe': recipe,
        'verification_protocol': verification
    }
    
    output_file = '/home/ubuntu/best_candidate_analysis.json'
    with open(output_file, 'w') as f:
        json.dump(analysis, f, indent=2)
    
    print(f"Complete analysis saved to: {output_file}")
    print(f"\n{'='*80}")
    print(f"ANALYSIS COMPLETE")
    print(f"{'='*80}\n")
    
    return analysis


if __name__ == "__main__":
    analysis = main()

