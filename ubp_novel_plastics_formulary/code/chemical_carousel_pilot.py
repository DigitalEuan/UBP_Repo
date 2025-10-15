#!/usr/bin/env python3
"""
Chemical Carousel - Pilot Run for Polypropylene Optimization
UBP-driven material discovery using composition space exploration

This script implements a systematic exploration of the polymer composition space
to discover novel polypropylene variants with enhanced properties.

Author: Euan R A Craig, New Zealand
Date: October 14, 2025
"""
import sys
import os
import json
import numpy as np
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass, asdict

# Add the UBP directory to the path
sys.path.insert(0, '/home/ubuntu/ubp_3.2')

from materials_research import (
    MaterialPredictor, MaterialComposition, MaterialCategory,
    ProcessingMethod, MaterialProperty, PolymerStructure
)

@dataclass
class CarouselCandidate:
    """Represents a candidate material from the carousel"""
    composition: Dict[str, float]
    properties: Dict[str, float]
    ubp_metrics: Dict[str, float]
    structure: str
    processing: str
    confidence: float
    optimization_score: float
    generation: int
    
    def to_dict(self):
        """Convert to dictionary for JSON serialization"""
        return {
            'composition': self.composition,
            'properties': self.properties,
            'ubp_metrics': self.ubp_metrics,
            'structure': self.structure,
            'processing': self.processing,
            'confidence': self.confidence,
            'optimization_score': self.optimization_score,
            'generation': self.generation
        }


class ChemicalCarousel:
    """
    Chemical Carousel optimizer for polymer materials.
    
    Uses UBP coherence metrics to guide exploration of composition space,
    seeking materials with optimal property combinations.
    """
    
    def __init__(self, target_properties: Dict[str, Tuple[float, float]],
                 base_composition: Dict[str, float],
                 allowed_elements: List[str],
                 processing_method: ProcessingMethod = ProcessingMethod.INJECTION_MOLDING):
        """
        Initialize the Chemical Carousel.
        
        Args:
            target_properties: Dict of property names to (target_value, weight) tuples
            base_composition: Starting composition (e.g., pure PP)
            allowed_elements: Elements that can be added/modified
            processing_method: Manufacturing process to simulate
        """
        self.target_properties = target_properties
        self.base_composition = base_composition
        self.allowed_elements = allowed_elements
        self.processing_method = processing_method
        
        self.predictor = MaterialPredictor(material_category=MaterialCategory.POLYMER)
        self.candidates: List[CarouselCandidate] = []
        self.best_candidate: Optional[CarouselCandidate] = None
        
    def normalize_composition(self, comp: Dict[str, float]) -> Dict[str, float]:
        """Normalize composition to sum to 100%"""
        total = sum(comp.values())
        if total == 0:
            return comp
        return {k: (v / total) * 100.0 for k, v in comp.items()}
    
    def calculate_optimization_score(self, properties: Dict[str, float],
                                    ubp_metrics: Dict[str, float]) -> float:
        """
        Calculate optimization score based on target properties and UBP coherence.
        
        Higher score = better match to optimization goals.
        """
        score = 0.0
        
        # Property matching component (70% of score)
        property_score = 0.0
        total_weight = 0.0
        
        for prop_name, (target_value, weight) in self.target_properties.items():
            if prop_name in properties:
                actual_value = properties[prop_name]
                # Normalized difference (0 = perfect match, 1 = far from target)
                diff = abs(actual_value - target_value) / max(target_value, 1.0)
                # Convert to score (1 = perfect, 0 = very different)
                prop_score = max(0.0, 1.0 - diff)
                property_score += prop_score * weight
                total_weight += weight
        
        if total_weight > 0:
            property_score /= total_weight
        
        # UBP coherence component (30% of score)
        coherence_score = ubp_metrics.get('overall_coherence', 0.0)
        
        # Combined score
        score = 0.7 * property_score + 0.3 * coherence_score
        
        return score
    
    def perturb_composition(self, comp: Dict[str, float], 
                          generation: int,
                          perturbation_strength: float = 0.1) -> Dict[str, float]:
        """
        Create a perturbed version of a composition.
        
        Perturbation strategy:
        - Early generations: larger random changes (exploration)
        - Later generations: smaller targeted changes (exploitation)
        """
        new_comp = comp.copy()
        
        # Adaptive perturbation strength (decreases with generation)
        adaptive_strength = perturbation_strength * (1.0 - 0.5 * (generation / 200.0))
        
        # Select 1-3 elements to perturb
        num_perturbations = np.random.randint(1, min(4, len(self.allowed_elements) + 1))
        elements_to_perturb = np.random.choice(self.allowed_elements, 
                                              size=num_perturbations, 
                                              replace=False)
        
        for elem in elements_to_perturb:
            if elem in new_comp:
                # Modify existing element
                current_value = new_comp[elem]
                # Random change: ±adaptive_strength * current_value
                delta = np.random.uniform(-adaptive_strength, adaptive_strength) * current_value
                new_comp[elem] = max(0.0, current_value + delta)
            else:
                # Add new element at small concentration
                new_comp[elem] = np.random.uniform(0.1, 2.0)
        
        # Normalize to 100%
        new_comp = self.normalize_composition(new_comp)
        
        # Remove elements below threshold (0.01%)
        new_comp = {k: v for k, v in new_comp.items() if v >= 0.01}
        
        return new_comp
    
    def evaluate_composition(self, comp: Dict[str, float], 
                           generation: int) -> CarouselCandidate:
        """
        Evaluate a composition using the UBP predictor.
        """
        # Create MaterialComposition object
        # For polymers, we use 'C' as the base element
        base_elem = 'C'
        material_comp = MaterialComposition(base_element=base_elem, elements=comp)
        
        # Predict properties
        prediction = self.predictor.predict_all_properties(
            material_comp,
            processing=self.processing_method,
            temperature=20.0
        )
        
        # Extract properties
        properties = {
            'tensile_strength': prediction.properties.get(MaterialProperty.TENSILE_STRENGTH, 0.0),
            'hardness': prediction.properties.get(MaterialProperty.HARDNESS, 0.0),
            'ductility': prediction.properties.get(MaterialProperty.DUCTILITY, 0.0),
            'glass_transition_temp': prediction.properties.get(MaterialProperty.GLASS_TRANSITION_TEMP, 0.0),
            'melting_point': prediction.properties.get(MaterialProperty.MELTING_POINT, 0.0),
        }
        
        # Calculate optimization score
        opt_score = self.calculate_optimization_score(properties, prediction.ubp_metrics)
        
        # Create candidate
        candidate = CarouselCandidate(
            composition=comp,
            properties=properties,
            ubp_metrics=prediction.ubp_metrics,
            structure=str(prediction.structure),
            processing=self.processing_method.value,
            confidence=prediction.confidence,
            optimization_score=opt_score,
            generation=generation
        )
        
        return candidate
    
    def run_carousel(self, num_iterations: int = 200, 
                    population_size: int = 10,
                    verbose: bool = True) -> List[CarouselCandidate]:
        """
        Run the Chemical Carousel optimization.
        
        Args:
            num_iterations: Number of optimization iterations
            population_size: Number of candidates to maintain in each generation
            verbose: Print progress updates
        
        Returns:
            List of all evaluated candidates
        """
        if verbose:
            print(f"\n{'='*80}")
            print(f"CHEMICAL CAROUSEL - PILOT RUN")
            print(f"{'='*80}")
            print(f"Target Material: Enhanced Polypropylene")
            print(f"Optimization Iterations: {num_iterations}")
            print(f"Population Size: {population_size}")
            print(f"Processing Method: {self.processing_method.value}")
            print(f"{'='*80}\n")
        
        # Initialize with base composition
        if verbose:
            print(f"Evaluating base composition...")
        
        base_candidate = self.evaluate_composition(self.base_composition, generation=0)
        self.candidates.append(base_candidate)
        self.best_candidate = base_candidate
        
        if verbose:
            print(f"  Base Score: {base_candidate.optimization_score:.4f}")
            print(f"  Base Coherence: {base_candidate.ubp_metrics['overall_coherence']:.4f}")
            print(f"  Base Tensile Strength: {base_candidate.properties['tensile_strength']:.2f} MPa\n")
        
        # Maintain a population of best candidates
        population = [base_candidate]
        
        # Main optimization loop
        for gen in range(1, num_iterations + 1):
            # Generate new candidates by perturbing population
            new_candidates = []
            
            for parent in population:
                # Create perturbed composition
                new_comp = self.perturb_composition(parent.composition, gen)
                
                # Evaluate
                candidate = self.evaluate_composition(new_comp, generation=gen)
                new_candidates.append(candidate)
                self.candidates.append(candidate)
                
                # Update best candidate
                if candidate.optimization_score > self.best_candidate.optimization_score:
                    self.best_candidate = candidate
                    if verbose and gen % 20 == 0:
                        print(f"  Gen {gen}: New best! Score={candidate.optimization_score:.4f}, "
                              f"Coherence={candidate.ubp_metrics['overall_coherence']:.4f}, "
                              f"TS={candidate.properties['tensile_strength']:.2f} MPa")
            
            # Selection: keep top candidates for next generation
            all_candidates = population + new_candidates
            all_candidates.sort(key=lambda x: x.optimization_score, reverse=True)
            population = all_candidates[:population_size]
            
            # Progress update
            if verbose and gen % 50 == 0:
                avg_score = np.mean([c.optimization_score for c in population])
                print(f"Gen {gen}/{num_iterations}: Avg Score={avg_score:.4f}, "
                      f"Best Score={self.best_candidate.optimization_score:.4f}")
        
        if verbose:
            print(f"\n{'='*80}")
            print(f"CAROUSEL COMPLETE")
            print(f"{'='*80}")
            print(f"Total Candidates Evaluated: {len(self.candidates)}")
            print(f"Best Optimization Score: {self.best_candidate.optimization_score:.4f}")
            print(f"Best Overall Coherence: {self.best_candidate.ubp_metrics['overall_coherence']:.4f}")
            print(f"{'='*80}\n")
        
        return self.candidates
    
    def get_top_candidates(self, n: int = 5) -> List[CarouselCandidate]:
        """Get the top N candidates by optimization score"""
        sorted_candidates = sorted(self.candidates, 
                                  key=lambda x: x.optimization_score, 
                                  reverse=True)
        return sorted_candidates[:n]
    
    def save_results(self, filepath: str):
        """Save all candidates to JSON file"""
        results = {
            'target_properties': self.target_properties,
            'base_composition': self.base_composition,
            'processing_method': self.processing_method.value,
            'total_candidates': len(self.candidates),
            'best_candidate': self.best_candidate.to_dict() if self.best_candidate else None,
            'all_candidates': [c.to_dict() for c in self.candidates]
        }
        
        with open(filepath, 'w') as f:
            json.dump(results, f, indent=2)
        
        print(f"Results saved to: {filepath}")


def main():
    """
    Main pilot run for polypropylene optimization.
    """
    print("\n" + "="*80)
    print("UBP CHEMICAL CAROUSEL - POLYPROPYLENE PILOT RUN")
    print("="*80)
    print("Objective: Discover novel polypropylene variants with enhanced properties")
    print("="*80 + "\n")
    
    # Define base polypropylene composition (C3H6)n
    # Weight percentages: C ≈ 85.7%, H ≈ 14.3%
    base_pp_composition = {
        'C': 85.7,
        'H': 14.3
    }
    
    # Define optimization targets
    # We want to maximize tensile strength and thermal stability
    # while maintaining good ductility
    target_properties = {
        'tensile_strength': (600.0, 1.0),      # Target 600 MPa (weight=1.0)
        'hardness': (1000.0, 0.8),             # Target 1000 Shore D (weight=0.8)
        'ductility': (80.0, 0.6),              # Target 80% elongation (weight=0.6)
        'melting_point': (200.0, 0.5),         # Target 200°C (weight=0.5)
    }
    
    # Define allowed elements for composition perturbation
    # We'll allow common polymer additives and functional groups
    allowed_elements = [
        'C',   # Carbon (backbone)
        'H',   # Hydrogen
        'O',   # Oxygen (ester, ether groups)
        'N',   # Nitrogen (amide groups)
        'Si',  # Silicon (siloxane groups for flexibility)
        'F',   # Fluorine (for chemical resistance)
        'Cl',  # Chlorine (for rigidity)
    ]
    
    print("Base Composition (Polypropylene):")
    for elem, pct in sorted(base_pp_composition.items()):
        print(f"  {elem}: {pct:.2f}%")
    
    print("\nOptimization Targets:")
    for prop, (target, weight) in target_properties.items():
        print(f"  {prop}: {target:.2f} (weight={weight:.2f})")
    
    print(f"\nAllowed Elements: {', '.join(allowed_elements)}")
    print(f"\nProcessing Method: Injection Molding")
    print(f"\n{'='*80}\n")
    
    # Create and run carousel
    carousel = ChemicalCarousel(
        target_properties=target_properties,
        base_composition=base_pp_composition,
        allowed_elements=allowed_elements,
        processing_method=ProcessingMethod.INJECTION_MOLDING
    )
    
    # Run pilot with 200 iterations
    candidates = carousel.run_carousel(num_iterations=200, population_size=10, verbose=True)
    
    # Get top 5 candidates
    top_candidates = carousel.get_top_candidates(n=5)
    
    print("\n" + "="*80)
    print("TOP 5 CANDIDATES")
    print("="*80)
    
    for i, candidate in enumerate(top_candidates, 1):
        print(f"\n{'-'*80}")
        print(f"Rank #{i}")
        print(f"{'-'*80}")
        print(f"Optimization Score: {candidate.optimization_score:.4f}")
        print(f"Generation: {candidate.generation}")
        print(f"\nComposition:")
        for elem, pct in sorted(candidate.composition.items(), key=lambda x: x[1], reverse=True):
            if pct >= 0.1:  # Only show elements > 0.1%
                print(f"  {elem}: {pct:.2f}%")
        print(f"\nUBP Metrics:")
        for metric, value in candidate.ubp_metrics.items():
            print(f"  {metric}: {value:.6f}")
        print(f"\nPredicted Properties:")
        for prop, value in candidate.properties.items():
            print(f"  {prop}: {value:.2f}")
        print(f"\nStructure: {candidate.structure}")
        print(f"Confidence: {candidate.confidence:.4f}")
    
    # Save results
    output_file = '/home/ubuntu/carousel_pilot_results.json'
    carousel.save_results(output_file)
    
    print(f"\n{'='*80}")
    print(f"PILOT RUN COMPLETE")
    print(f"{'='*80}")
    print(f"Best candidate will be analyzed in detail for Material Recipe Card.")
    print(f"{'='*80}\n")
    
    return carousel.best_candidate


if __name__ == "__main__":
    best = main()

