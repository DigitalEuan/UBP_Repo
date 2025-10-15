#!/usr/bin/env python3
"""
Full-Scale Chemical Carousel for All Seven Plastic Categories
UBP-driven material discovery across the complete plastic classification system

Author: Euan R A Craig, New Zealand
Date: October 14, 2025
"""
import sys
import os
import json
import numpy as np
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass

# Add the UBP directory to the path
sys.path.insert(0, '/home/ubuntu/ubp_3.2')

from chemical_carousel_pilot import ChemicalCarousel, CarouselCandidate
from materials_research import ProcessingMethod

# Define all seven plastic categories with their base compositions and optimization targets
PLASTIC_CATEGORIES = {
    'PET': {
        'name': 'Polyethylene Terephthalate',
        'base_composition': {'C': 62.5, 'H': 4.2, 'O': 33.3},  # (C10H8O4)n
        'target_properties': {
            'tensile_strength': (700.0, 1.0),
            'hardness': (1100.0, 0.9),
            'ductility': (100.0, 0.5),
            'melting_point': (260.0, 0.7),
        },
        'allowed_elements': ['C', 'H', 'O', 'N', 'Si', 'F', 'S'],
        'processing': ProcessingMethod.INJECTION_MOLDING,
        'description': 'High-strength polyester for bottles and fibers'
    },
    'HDPE': {
        'name': 'High-Density Polyethylene',
        'base_composition': {'C': 85.7, 'H': 14.3},  # (C2H4)n
        'target_properties': {
            'tensile_strength': (500.0, 1.0),
            'hardness': (900.0, 0.8),
            'ductility': (150.0, 0.7),
            'melting_point': (140.0, 0.5),
        },
        'allowed_elements': ['C', 'H', 'O', 'N', 'Si', 'F', 'Cl'],
        'processing': ProcessingMethod.EXTRUSION,
        'description': 'Rigid polyethylene for containers and pipes'
    },
    'PVC': {
        'name': 'Polyvinyl Chloride',
        'base_composition': {'C': 38.4, 'H': 4.8, 'Cl': 56.8},  # (C2H3Cl)n
        'target_properties': {
            'tensile_strength': (600.0, 1.0),
            'hardness': (1000.0, 0.9),
            'ductility': (50.0, 0.4),
            'melting_point': (180.0, 0.6),
        },
        'allowed_elements': ['C', 'H', 'Cl', 'O', 'N', 'S', 'F'],
        'processing': ProcessingMethod.EXTRUSION,
        'description': 'Chlorinated polymer for construction and packaging'
    },
    'LDPE': {
        'name': 'Low-Density Polyethylene',
        'base_composition': {'C': 85.7, 'H': 14.3},  # (C2H4)n
        'target_properties': {
            'tensile_strength': (400.0, 0.8),
            'hardness': (700.0, 0.6),
            'ductility': (300.0, 1.0),
            'melting_point': (115.0, 0.5),
        },
        'allowed_elements': ['C', 'H', 'O', 'N', 'Si'],
        'processing': ProcessingMethod.EXTRUSION,
        'description': 'Flexible polyethylene for films and bags'
    },
    'PP': {
        'name': 'Polypropylene',
        'base_composition': {'C': 85.7, 'H': 14.3},  # (C3H6)n
        'target_properties': {
            'tensile_strength': (600.0, 1.0),
            'hardness': (1000.0, 0.8),
            'ductility': (80.0, 0.6),
            'melting_point': (200.0, 0.5),
        },
        'allowed_elements': ['C', 'H', 'O', 'N', 'Si', 'F', 'Cl'],
        'processing': ProcessingMethod.INJECTION_MOLDING,
        'description': 'Versatile polypropylene for containers and automotive parts'
    },
    'PS': {
        'name': 'Polystyrene',
        'base_composition': {'C': 92.3, 'H': 7.7},  # (C8H8)n
        'target_properties': {
            'tensile_strength': (550.0, 1.0),
            'hardness': (950.0, 0.8),
            'ductility': (60.0, 0.5),
            'melting_point': (240.0, 0.6),
        },
        'allowed_elements': ['C', 'H', 'O', 'N', 'Br', 'F'],
        'processing': ProcessingMethod.INJECTION_MOLDING,
        'description': 'Aromatic polymer for packaging and insulation'
    },
    'Other': {
        'name': 'Advanced Bioplastic',
        'base_composition': {'C': 50.0, 'H': 6.0, 'O': 40.0, 'N': 4.0},  # Bio-based blend
        'target_properties': {
            'tensile_strength': (500.0, 0.9),
            'hardness': (850.0, 0.7),
            'ductility': (120.0, 0.8),
            'melting_point': (170.0, 0.5),
        },
        'allowed_elements': ['C', 'H', 'O', 'N', 'S', 'P'],
        'processing': ProcessingMethod.INJECTION_MOLDING,
        'description': 'Biodegradable multi-functional polymer'
    }
}


def run_category_optimization(category_key: str, category_data: Dict, 
                              num_iterations: int = 150,
                              population_size: int = 10) -> Dict:
    """
    Run Chemical Carousel optimization for a single plastic category.
    """
    print(f"\n{'='*80}")
    print(f"CATEGORY: {category_data['name']} ({category_key})")
    print(f"{'='*80}")
    print(f"Description: {category_data['description']}")
    print(f"Base Composition: {category_data['base_composition']}")
    print(f"Processing: {category_data['processing'].value}")
    print(f"{'='*80}\n")
    
    # Create carousel
    carousel = ChemicalCarousel(
        target_properties=category_data['target_properties'],
        base_composition=category_data['base_composition'],
        allowed_elements=category_data['allowed_elements'],
        processing_method=category_data['processing']
    )
    
    # Run optimization
    candidates = carousel.run_carousel(
        num_iterations=num_iterations,
        population_size=population_size,
        verbose=True
    )
    
    # Get top 3 candidates
    top_3 = carousel.get_top_candidates(n=3)
    
    # Save results for this category
    output_file = f'/home/ubuntu/carousel_{category_key}_results.json'
    carousel.save_results(output_file)
    
    print(f"\n{'='*80}")
    print(f"TOP 3 CANDIDATES FOR {category_key}")
    print(f"{'='*80}\n")
    
    for i, candidate in enumerate(top_3, 1):
        print(f"Rank #{i}:")
        print(f"  Optimization Score: {candidate.optimization_score:.4f}")
        print(f"  Overall Coherence: {candidate.ubp_metrics['overall_coherence']:.4f}")
        print(f"  Tensile Strength: {candidate.properties['tensile_strength']:.2f} MPa")
        print(f"  Hardness: {candidate.properties['hardness']:.2f}")
        print(f"  Ductility: {candidate.properties['ductility']:.2f}%")
        print()
    
    return {
        'category_key': category_key,
        'category_name': category_data['name'],
        'total_candidates': len(candidates),
        'best_candidate': carousel.best_candidate.to_dict(),
        'top_3_candidates': [c.to_dict() for c in top_3],
        'output_file': output_file
    }


def main():
    """
    Main full-scale optimization routine for all seven plastic categories.
    """
    print("\n" + "="*80)
    print("UBP CHEMICAL CAROUSEL - FULL-SCALE MATERIAL GENERATION")
    print("="*80)
    print("Objective: Generate optimized materials for all seven plastic categories")
    print("Categories: PET, HDPE, PVC, LDPE, PP, PS, Other")
    print("="*80 + "\n")
    
    # We already have PP results from pilot run, so we'll process the other 6
    categories_to_process = ['PET', 'HDPE', 'PVC', 'LDPE', 'PS', 'Other']
    
    all_results = {}
    
    for category_key in categories_to_process:
        category_data = PLASTIC_CATEGORIES[category_key]
        
        try:
            result = run_category_optimization(
                category_key=category_key,
                category_data=category_data,
                num_iterations=150,  # Slightly fewer iterations for efficiency
                population_size=10
            )
            all_results[category_key] = result
            
        except Exception as e:
            print(f"\n{'='*80}")
            print(f"ERROR in category {category_key}")
            print(f"{'='*80}")
            print(f"Error: {str(e)}")
            import traceback
            traceback.print_exc()
            all_results[category_key] = {'error': str(e)}
    
    # Add PP results from pilot run
    all_results['PP'] = {
        'category_key': 'PP',
        'category_name': 'Polypropylene',
        'note': 'Results from pilot run',
        'output_file': '/home/ubuntu/carousel_pilot_results.json'
    }
    
    # Save summary
    summary_file = '/home/ubuntu/full_scale_summary.json'
    with open(summary_file, 'w') as f:
        json.dump(all_results, f, indent=2)
    
    print(f"\n{'='*80}")
    print(f"FULL-SCALE GENERATION COMPLETE")
    print(f"{'='*80}")
    print(f"Categories Processed: {len(all_results)}")
    print(f"Summary saved to: {summary_file}")
    print(f"{'='*80}\n")
    
    return all_results


if __name__ == "__main__":
    results = main()

