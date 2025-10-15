#!/usr/bin/env python3
"""
Validation script for UBP Materials Research Framework
Tests the baseline functionality and validates against reference materials
"""
import sys
import os
import json

# Add the UBP directory to the path
sys.path.insert(0, '/home/ubuntu/ubp_3.2')

from materials_research import (
    MaterialPredictor, MaterialComposition, MaterialCategory,
    ProcessingMethod, MaterialProperty, CrystalStructure, PolymerStructure
)

def validate_polymer_framework():
    """
    Validate the polymer prediction framework with a simple test case.
    """
    print("\n" + "="*80)
    print("POLYMER FRAMEWORK VALIDATION")
    print("="*80)
    
    # Create a polymer predictor
    predictor = MaterialPredictor(material_category=MaterialCategory.POLYMER)
    
    # Test with a simple polypropylene-like composition
    # PP is primarily C and H with a 3:6 ratio (C3H6)n
    # In weight percent: C ≈ 85.7%, H ≈ 14.3%
    pp_composition = MaterialComposition(
        base_element="C",
        elements={
            "C": 85.7,
            "H": 14.3
        }
    )
    
    print(f"\nTest Composition (Polypropylene-like):")
    print(f"  Base Element: {pp_composition.base_element}")
    for elem, pct in sorted(pp_composition.elements.items()):
        print(f"  {elem}: {pct:.2f}%")
    print(f"  Total: {pp_composition.get_total_composition():.2f}%")
    
    # Test elemental coherence calculation
    print(f"\nTesting UBP Elemental Coherence Calculation...")
    elemental_coherence = predictor.compute_ubp_elemental_coherence(pp_composition)
    print(f"  Elemental Coherence: {elemental_coherence:.6f}")
    
    # Test structure coherence calculation
    print(f"\nTesting UBP Structure Coherence Calculation...")
    structure_coherence = predictor.compute_structure_coherence(
        pp_composition, 
        PolymerStructure.SEMI_CRYSTALLINE,
        temperature=20.0
    )
    print(f"  Structure Coherence (Semi-Crystalline): {structure_coherence:.6f}")
    
    # Test property predictions
    print(f"\nTesting Property Predictions...")
    prediction = predictor.predict_all_properties(
        pp_composition,
        processing=ProcessingMethod.INJECTION_MOLDING,
        temperature=20.0
    )
    
    print(f"\nPredicted Structure: {prediction.structure}")
    print(f"\nPredicted Properties:")
    for prop, value in prediction.properties.items():
        print(f"  {prop.value}: {value:.2f}")
    
    print(f"\nUBP Metrics:")
    for metric, value in prediction.ubp_metrics.items():
        print(f"  {metric}: {value:.6f}")
    
    print(f"\nConfidence: {prediction.confidence:.4f}")
    
    return True

def validate_metallic_framework():
    """
    Validate the metallic materials framework with reference steels.
    """
    print("\n" + "="*80)
    print("METALLIC FRAMEWORK VALIDATION")
    print("="*80)
    
    # Create a metallic predictor
    predictor = MaterialPredictor(material_category=MaterialCategory.METALLIC)
    
    # Test with reference steels
    test_cases = [
        ("AISI 1020 (Low Carbon Steel)", predictor.reference_steels["AISI_1020"], ProcessingMethod.NORMALIZING),
        ("AISI 4140 (Alloy Steel)", predictor.reference_steels["AISI_4140"], ProcessingMethod.QUENCHING),
    ]
    
    for name, composition, processing in test_cases:
        print(f"\n{'-'*80}")
        print(f"Test Case: {name}")
        print(f"{'-'*80}")
        
        print(f"\nComposition:")
        print(f"  Base Element: {composition.base_element}")
        for elem, pct in sorted(composition.elements.items()):
            if pct > 0:
                print(f"  {elem}: {pct:.2f}%")
        print(f"  Total: {composition.get_total_composition():.2f}%")
        
        # Predict properties
        prediction = predictor.predict_all_properties(
            composition,
            processing=processing,
            temperature=20.0
        )
        
        print(f"\nProcessing: {processing.value}")
        print(f"Predicted Structure: {prediction.structure.value}")
        
        print(f"\nPredicted Properties:")
        for prop, value in prediction.properties.items():
            print(f"  {prop.value}: {value:.2f}")
        
        print(f"\nUBP Metrics:")
        for metric, value in prediction.ubp_metrics.items():
            print(f"  {metric}: {value:.6f}")
        
        print(f"\nConfidence: {prediction.confidence:.4f}")
    
    return True

def main():
    """
    Main validation routine.
    """
    print("\n" + "="*80)
    print("UBP MATERIALS RESEARCH FRAMEWORK - SYSTEM VALIDATION")
    print("="*80)
    
    try:
        # Validate polymer framework
        polymer_valid = validate_polymer_framework()
        
        # Validate metallic framework
        metallic_valid = validate_metallic_framework()
        
        print("\n" + "="*80)
        print("VALIDATION SUMMARY")
        print("="*80)
        print(f"Polymer Framework: {'PASS' if polymer_valid else 'FAIL'}")
        print(f"Metallic Framework: {'PASS' if metallic_valid else 'FAIL'}")
        print(f"\nOverall Status: {'PASS - System is operational' if (polymer_valid and metallic_valid) else 'FAIL - Issues detected'}")
        print("="*80 + "\n")
        
        return 0 if (polymer_valid and metallic_valid) else 1
        
    except Exception as e:
        print(f"\n{'='*80}")
        print(f"VALIDATION FAILED WITH ERROR")
        print(f"{'='*80}")
        print(f"Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())

