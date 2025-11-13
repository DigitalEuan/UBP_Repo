"""
Standard Python Nutrition Study
================================

Traditional biochemical modeling approach using:
- NumPy for numerical operations
- Simple linear models for interactions
- Statistical methods for validation

This provides a baseline for comparison against UBP 3.5 coherence substrate.
"""

import json
import time
import math
import numpy as np
from typing import Dict, List, Tuple


# ============================================================================
# NUTRIENT DATABASE (Standard Approach)
# ============================================================================

class StandardNutrient:
    """Traditional nutrient representation"""
    def __init__(self, name: str, amount: float, bioavailability: float):
        self.name = name
        self.amount = amount  # mg
        self.bioavailability = bioavailability  # fraction 0-1
    
    def __repr__(self):
        return f"StandardNutrient({self.name}, {self.amount:.2f}mg, bio={self.bioavailability:.4f})"


def get_standard_nutrients() -> Dict[str, StandardNutrient]:
    """Get standard nutrient database"""
    return {
        'calcium': StandardNutrient('calcium', 1000.0, 0.30),
        'magnesium': StandardNutrient('magnesium', 400.0, 0.50),
        'phosphorus': StandardNutrient('phosphorus', 700.0, 0.70),
        'iron_heme': StandardNutrient('iron_heme', 18.0, 0.25),
        'iron_nonheme': StandardNutrient('iron_nonheme', 18.0, 0.10),
        'zinc': StandardNutrient('zinc', 11.0, 0.30),
        'copper': StandardNutrient('copper', 0.9, 0.55),
        'manganese': StandardNutrient('manganese', 2.3, 0.05),
        'selenium': StandardNutrient('selenium', 0.055, 0.80),
        'chromium': StandardNutrient('chromium', 0.035, 0.02),
        'molybdenum': StandardNutrient('molybdenum', 0.045, 0.75),
        'vitamin_c': StandardNutrient('vitamin_c', 90.0, 0.90),
        'vitamin_d': StandardNutrient('vitamin_d', 0.020, 0.80),
    }


# ============================================================================
# VALIDATION DATA (Same as UBP study)
# ============================================================================

class ValidationData:
    """Real-world bioavailability data from literature"""
    IRON_ALONE_ABSORPTION = 0.10
    IRON_WITH_VITC_ABSORPTION = 0.18
    IRON_NO_CALCIUM = 0.10
    IRON_WITH_CALCIUM = 0.06
    ZINC_OPTIMAL_RATIO = 0.30
    ZINC_EXCESS_RATIO = 0.25
    COPPER_OPTIMAL_RATIO = 0.55
    COPPER_EXCESS_ZN = 0.35
    MORNING_ABSORPTION_BOOST = 1.15
    EVENING_ABSORPTION_PENALTY = 0.90


# ============================================================================
# INTERACTION MODELS (Traditional Biochemistry)
# ============================================================================

def synergistic_interaction(nutrient1: StandardNutrient, nutrient2: StandardNutrient,
                           enhancement_factor: float = 1.8) -> StandardNutrient:
    """
    Model synergistic interaction using simple multiplication.
    
    Traditional approach: bioavailability multiplied by enhancement factor.
    """
    enhanced_bio = min(1.0, nutrient1.bioavailability * enhancement_factor)
    return StandardNutrient(nutrient1.name, nutrient1.amount, enhanced_bio)


def antagonistic_interaction(nutrient1: StandardNutrient, nutrient2: StandardNutrient,
                            inhibition_factor: float = 0.6) -> StandardNutrient:
    """
    Model antagonistic interaction using simple multiplication.
    
    Traditional approach: bioavailability multiplied by inhibition factor.
    """
    inhibited_bio = nutrient1.bioavailability * inhibition_factor
    return StandardNutrient(nutrient1.name, nutrient1.amount, inhibited_bio)


def competitive_interaction(nutrients: List[StandardNutrient],
                           competition_strength: float = 0.2) -> List[StandardNutrient]:
    """
    Model competitive interaction using Michaelis-Menten-like kinetics.
    
    Traditional approach: Each nutrient's absorption reduced by presence of competitors.
    """
    n_competitors = len(nutrients)
    if n_competitors <= 1:
        return nutrients
    
    # Competition factor based on number of competitors
    competition_factor = 1.0 / (1.0 + competition_strength * (n_competitors - 1))
    
    competed_nutrients = []
    for nutrient in nutrients:
        competed_bio = nutrient.bioavailability * competition_factor
        competed_nutrients.append(
            StandardNutrient(nutrient.name, nutrient.amount, competed_bio)
        )
    
    return competed_nutrients


# ============================================================================
# TEMPORAL DYNAMICS (Traditional Approach)
# ============================================================================

def circadian_modulation(nutrient: StandardNutrient, time_of_day: str) -> StandardNutrient:
    """
    Apply circadian rhythm modulation to nutrient absorption.
    
    Traditional approach: Simple multiplicative factor based on time of day.
    """
    if time_of_day == 'morning':
        factor = ValidationData.MORNING_ABSORPTION_BOOST
    elif time_of_day == 'evening':
        factor = ValidationData.EVENING_ABSORPTION_PENALTY
    else:
        factor = 1.0
    
    modulated_bio = nutrient.bioavailability * factor
    return StandardNutrient(nutrient.name, nutrient.amount, modulated_bio)


def time_restricted_eating_effect(nutrients: List[StandardNutrient],
                                  window_hours: int = 8) -> List[StandardNutrient]:
    """
    Model time-restricted eating effect.
    
    Traditional approach: Concentration effect from compressed eating window.
    """
    # Assume 16-hour baseline eating window
    baseline_window = 16
    concentration_factor = baseline_window / window_hours
    
    # TRE improves absorption efficiency (empirical factor)
    tre_boost = 1.0 + 0.1 * (concentration_factor - 1.0)
    
    tre_nutrients = []
    for nutrient in nutrients:
        tre_bio = min(1.0, nutrient.bioavailability * tre_boost)
        tre_nutrients.append(
            StandardNutrient(nutrient.name, nutrient.amount, tre_bio)
        )
    
    return tre_nutrients


# ============================================================================
# STUDY 1: NUTRIENT INTERACTIONS
# ============================================================================

def study_nutrient_interactions():
    """Test nutrient interactions using standard models"""
    print("\n" + "=" * 80)
    print("STUDY 1: NUTRIENT INTERACTIONS (Standard Python)")
    print("=" * 80)
    
    nutrients = get_standard_nutrients()
    results = []
    
    # Test 1: Iron + Vitamin C
    print("\n1. Iron + Vitamin C Enhancement")
    print("-" * 40)
    
    iron = nutrients['iron_nonheme']
    vit_c = nutrients['vitamin_c']
    
    print(f"   Baseline iron absorption: {iron.bioavailability:.4f}")
    print(f"   Validation data: {ValidationData.IRON_ALONE_ABSORPTION:.4f}")
    
    enhanced_iron = synergistic_interaction(iron, vit_c, enhancement_factor=1.8)
    
    print(f"   Enhanced iron absorption: {enhanced_iron.bioavailability:.4f}")
    print(f"   Validation data: {ValidationData.IRON_WITH_VITC_ABSORPTION:.4f}")
    
    error = abs(enhanced_iron.bioavailability - ValidationData.IRON_WITH_VITC_ABSORPTION)
    print(f"   Prediction error: {error:.4f} ({error/ValidationData.IRON_WITH_VITC_ABSORPTION*100:.1f}%)")
    
    results.append({
        'test': 'iron_vitamin_c_synergy',
        'predicted': enhanced_iron.bioavailability,
        'actual': ValidationData.IRON_WITH_VITC_ABSORPTION,
        'error': error,
        'error_percent': error/ValidationData.IRON_WITH_VITC_ABSORPTION*100
    })
    
    # Test 2: Calcium vs Iron
    print("\n2. Calcium vs Iron Competition")
    print("-" * 40)
    
    iron = nutrients['iron_nonheme']
    calcium = nutrients['calcium']
    
    print(f"   Baseline iron absorption: {iron.bioavailability:.4f}")
    
    inhibited_iron = antagonistic_interaction(iron, calcium, inhibition_factor=0.6)
    
    print(f"   Inhibited iron absorption: {inhibited_iron.bioavailability:.4f}")
    print(f"   Validation data: {ValidationData.IRON_WITH_CALCIUM:.4f}")
    
    error = abs(inhibited_iron.bioavailability - ValidationData.IRON_WITH_CALCIUM)
    print(f"   Prediction error: {error:.4f} ({error/ValidationData.IRON_WITH_CALCIUM*100:.1f}%)")
    
    results.append({
        'test': 'calcium_iron_antagonism',
        'predicted': inhibited_iron.bioavailability,
        'actual': ValidationData.IRON_WITH_CALCIUM,
        'error': error,
        'error_percent': error/ValidationData.IRON_WITH_CALCIUM*100
    })
    
    # Test 3: Multi-element Competition
    print("\n3. Multi-Element Competition (Ca, Fe, Zn, Mg)")
    print("-" * 40)
    
    competitors = [
        nutrients['calcium'],
        nutrients['iron_nonheme'],
        nutrients['zinc'],
        nutrients['magnesium']
    ]
    
    print("   Before competition:")
    for c in competitors:
        print(f"      {c.name:15s} bio={c.bioavailability:.4f}")
    
    competed = competitive_interaction(competitors, competition_strength=0.2)
    
    print("   After competition:")
    for c in competed:
        print(f"      {c.name:15s} bio={c.bioavailability:.4f}")
    
    results.append({
        'test': 'multi_element_competition',
        'nutrients': [c.name for c in competed],
        'bioavailability_values': [c.bioavailability for c in competed]
    })
    
    return results


# ============================================================================
# STUDY 2: TEMPORAL DYNAMICS
# ============================================================================

def study_temporal_dynamics():
    """Test temporal dynamics using standard models"""
    print("\n" + "=" * 80)
    print("STUDY 2: TEMPORAL DYNAMICS (Standard Python)")
    print("=" * 80)
    
    nutrients = get_standard_nutrients()
    results = []
    
    # Morning vs Evening
    print("\n1. Circadian Timing Effects")
    print("-" * 40)
    
    temporal_nutrients = [
        nutrients['iron_nonheme'],
        nutrients['calcium'],
        nutrients['magnesium'],
        nutrients['zinc']
    ]
    
    print("\n   Morning Absorption:")
    morning_nutrients = [circadian_modulation(n, 'morning') for n in temporal_nutrients]
    morning_mean = np.mean([n.bioavailability for n in morning_nutrients])
    
    for n in morning_nutrients:
        print(f"      {n.name:15s} absorption: {n.bioavailability:.4f}")
    print(f"      Mean absorption: {morning_mean:.4f}")
    
    print("\n   Evening Absorption:")
    evening_nutrients = [circadian_modulation(n, 'evening') for n in temporal_nutrients]
    evening_mean = np.mean([n.bioavailability for n in evening_nutrients])
    
    for n in evening_nutrients:
        print(f"      {n.name:15s} absorption: {n.bioavailability:.4f}")
    print(f"      Mean absorption: {evening_mean:.4f}")
    
    ratio = morning_mean / evening_mean if evening_mean > 0 else 1.0
    print(f"\n   Morning/Evening ratio: {ratio:.2f}x")
    print(f"   Validation data suggests: {ValidationData.MORNING_ABSORPTION_BOOST/ValidationData.EVENING_ABSORPTION_PENALTY:.2f}x")
    
    results.append({
        'test': 'circadian_timing',
        'morning_mean': morning_mean,
        'evening_mean': evening_mean,
        'ratio': ratio,
        'validation_ratio': ValidationData.MORNING_ABSORPTION_BOOST/ValidationData.EVENING_ABSORPTION_PENALTY
    })
    
    # Time-restricted eating
    print("\n2. Time-Restricted Eating (8-hour window)")
    print("-" * 40)
    
    tre_nutrients = time_restricted_eating_effect(temporal_nutrients, window_hours=8)
    tre_mean = np.mean([n.bioavailability for n in tre_nutrients])
    baseline_mean = np.mean([n.bioavailability for n in temporal_nutrients])
    
    print(f"      TRE mean absorption: {tre_mean:.4f}")
    print(f"      Baseline mean absorption: {baseline_mean:.4f}")
    print(f"      TRE improvement: {tre_mean/baseline_mean:.2f}x")
    
    results.append({
        'test': 'time_restricted_eating',
        'tre_mean': tre_mean,
        'baseline_mean': baseline_mean,
        'improvement_ratio': tre_mean/baseline_mean
    })
    
    return results


# ============================================================================
# STUDY 3: MEAL COMPOSITION
# ============================================================================

def study_meal_composition():
    """Analyze meal compositions using standard models"""
    print("\n" + "=" * 80)
    print("STUDY 3: MEAL COMPOSITION ANALYSIS (Standard Python)")
    print("=" * 80)
    
    nutrients = get_standard_nutrients()
    results = []
    
    # Meal 1: Iron + Vitamin C
    print("\n1. Iron-Rich Meal with Vitamin C (Optimal)")
    print("-" * 40)
    
    iron = nutrients['iron_nonheme']
    vit_c = nutrients['vitamin_c']
    enhanced_iron = synergistic_interaction(iron, vit_c, enhancement_factor=1.8)
    
    meal1_nutrients = [enhanced_iron, vit_c]
    meal1_mean = np.mean([n.bioavailability for n in meal1_nutrients])
    meal1_score = np.sum([n.amount * n.bioavailability for n in meal1_nutrients]) / np.sum([n.amount for n in meal1_nutrients])
    
    print(f"   Mean bioavailability: {meal1_mean:.4f}")
    print(f"   Weighted score: {meal1_score:.4f}")
    
    results.append({
        'meal': 'iron_with_vitamin_c',
        'mean_bio': meal1_mean,
        'score': meal1_score
    })
    
    # Meal 2: Iron + Calcium
    print("\n2. Iron-Rich Meal with Calcium (Suboptimal)")
    print("-" * 40)
    
    iron = nutrients['iron_nonheme']
    calcium = nutrients['calcium']
    inhibited_iron = antagonistic_interaction(iron, calcium, inhibition_factor=0.6)
    
    meal2_nutrients = [inhibited_iron, calcium]
    meal2_mean = np.mean([n.bioavailability for n in meal2_nutrients])
    meal2_score = np.sum([n.amount * n.bioavailability for n in meal2_nutrients]) / np.sum([n.amount for n in meal2_nutrients])
    
    print(f"   Mean bioavailability: {meal2_mean:.4f}")
    print(f"   Weighted score: {meal2_score:.4f}")
    
    results.append({
        'meal': 'iron_with_calcium',
        'mean_bio': meal2_mean,
        'score': meal2_score
    })
    
    # Meal 3: Balanced
    print("\n3. Balanced Multi-Nutrient Meal")
    print("-" * 40)
    
    meal3_base = [
        nutrients['iron_nonheme'],
        nutrients['vitamin_c'],
        nutrients['zinc'],
        nutrients['magnesium'],
        nutrients['vitamin_d']
    ]
    
    # Apply interactions
    iron = nutrients['iron_nonheme']
    vit_c = nutrients['vitamin_c']
    enhanced_iron = synergistic_interaction(iron, vit_c, enhancement_factor=1.8)
    
    meal3_nutrients = [enhanced_iron, vit_c, nutrients['zinc'], nutrients['magnesium'], nutrients['vitamin_d']]
    meal3_mean = np.mean([n.bioavailability for n in meal3_nutrients])
    meal3_score = np.sum([n.amount * n.bioavailability for n in meal3_nutrients]) / np.sum([n.amount for n in meal3_nutrients])
    
    print(f"   Mean bioavailability: {meal3_mean:.4f}")
    print(f"   Weighted score: {meal3_score:.4f}")
    
    results.append({
        'meal': 'balanced_multi_nutrient',
        'mean_bio': meal3_mean,
        'score': meal3_score
    })
    
    # Compare
    print("\n4. Meal Comparison")
    print("-" * 40)
    print(f"   Meal 1 (Iron+VitC) score: {meal1_score:.4f}")
    print(f"   Meal 2 (Iron+Ca) score: {meal2_score:.4f}")
    print(f"   Meal 3 (Balanced) score: {meal3_score:.4f}")
    
    return results


# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    print("=" * 80)
    print("STANDARD PYTHON NUTRITION STUDY")
    print("Traditional Biochemical Modeling Approach")
    print("=" * 80)
    
    start_time = time.time()
    
    # Run all studies
    interaction_results = study_nutrient_interactions()
    temporal_results = study_temporal_dynamics()
    meal_results = study_meal_composition()
    
    end_time = time.time()
    execution_time = end_time - start_time
    
    # Compile results
    all_results = {
        'execution_time_seconds': execution_time,
        'interaction_study': interaction_results,
        'temporal_study': temporal_results,
        'meal_study': meal_results
    }
    
    # Save results
    with open('/home/ubuntu/nutrition_study/results/standard_study_results.json', 'w') as f:
        json.dump(all_results, f, indent=2)
    
    # Summary
    print("\n" + "=" * 80)
    print("STUDY SUMMARY")
    print("=" * 80)
    print(f"Total execution time: {execution_time:.3f} seconds")
    print(f"\nInteraction Tests: {len(interaction_results)}")
    print(f"Temporal Tests: {len(temporal_results)}")
    print(f"Meal Composition Tests: {len(meal_results)}")
    
    # Calculate average error
    validation_tests = [r for r in interaction_results if 'error_percent' in r]
    if validation_tests:
        avg_error = sum(r['error_percent'] for r in validation_tests) / len(validation_tests)
        print(f"\nAverage prediction error: {avg_error:.1f}%")
    
    print(f"\nResults saved to: /home/ubuntu/nutrition_study/results/standard_study_results.json")
    print("=" * 80)


if __name__ == "__main__":
    main()
