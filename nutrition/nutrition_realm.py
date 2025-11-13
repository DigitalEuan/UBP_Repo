"""
================================================================================
Universal Binary Principle (UBP) Framework v3.5 - Nutrition Realm
Author: Manus AI (based on Euan Craig's UBP framework)
Date: November 13, 2025
================================================================================

Nutrition realm as coherence dynamics and information geometry.

**Core Insight**: Nutrition is not just chemistry - it's information transformation.
Food carries coherence, digestion mixes information, absorption filters coherence,
and metabolism utilizes information.

**Paradigm Shift**:
- Nutrients are CoherenceStates (value + NRCI)
- Bioavailability IS coherence (NRCI)
- Interactions are coherence operations
- Timing is temporal coherence alignment
- Competition is geometric error

**Zero Dependencies**: Only Python stdlib + coherence_substrate + core UBP 3.5
"""

import math
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass, field
from enum import Enum

from coherence_substrate import CoherenceState, NRCI_TARGET, Y, Y_INVERSE, GOLDEN_RATIO
from system_constants import UBPConstants
from geometric_error_correction import restore_coherence, maintain_coherence


# ============================================================================
# NUTRIENT TYPES AND CATEGORIES
# ============================================================================

class NutrientCategory(Enum):
    """Nutrient categories by coherence frequency"""
    MACROMINERAL = "macromineral"      # Low frequency, high amplitude (Ca, Mg, P)
    TRACE_ELEMENT = "trace_element"    # Medium frequency (Fe, Zn, Cu, Mn)
    ULTRATRACE = "ultratrace"          # High frequency, low amplitude (Se, Cr, Mo)
    VITAMIN_WATER = "vitamin_water"    # Water-soluble vitamins (C, B-complex)
    VITAMIN_FAT = "vitamin_fat"        # Fat-soluble vitamins (A, D, E, K)
    MACRONUTRIENT = "macronutrient"    # Protein, carbs, fats


class InteractionType(Enum):
    """Types of nutrient interactions"""
    SYNERGISTIC = "synergistic"        # Enhances absorption/utilization
    ANTAGONISTIC = "antagonistic"      # Inhibits absorption/utilization
    COMPETITIVE = "competitive"        # Competes for same pathways
    NEUTRAL = "neutral"                # No significant interaction


# ============================================================================
# NUTRIENT STATE: Coherence-Native
# ============================================================================

@dataclass
class NutrientState:
    """
    A nutrient as a coherence state.
    
    In UBP 3.5, a nutrient isn't just an amount - it's a coherence state
    carrying information about bioavailability, processing, and context.
    """
    name: str
    element_symbol: str
    coherence: CoherenceState
    category: NutrientCategory
    
    # Absorption properties
    absorption_site: str = "small_intestine"
    transport_protein: str = "unknown"
    
    # Interaction lists
    antagonists: List[str] = field(default_factory=list)
    synergists: List[str] = field(default_factory=list)
    
    # Temporal properties
    circadian_peak: str = "morning"  # morning, afternoon, evening, night
    
    # Coherence frequency (Hz) - reflects metabolic timescale
    coherence_frequency: float = 1e12
    
    @property
    def amount(self) -> float:
        """Amount in mg or appropriate unit"""
        return self.coherence.value
    
    @property
    def bioavailability(self) -> float:
        """Bioavailability is coherence (NRCI)"""
        return self.coherence.nrci
    
    @property
    def is_bioavailable(self) -> bool:
        """Check if nutrient is in bioavailable regime"""
        return self.bioavailability >= 0.50
    
    def __repr__(self):
        return f"NutrientState({self.name}, {self.amount:.2f}mg, NRCI={self.bioavailability:.4f})"


# ============================================================================
# NUTRIENT DATABASE: Essential Nutrients
# ============================================================================

class NutrientDatabase:
    """
    Database of essential nutrients with coherence properties.
    """
    
    @staticmethod
    def create_nutrient(
        name: str,
        element_symbol: str,
        amount: float,
        bioavailability: float,
        category: NutrientCategory,
        **kwargs
    ) -> NutrientState:
        """
        Create a nutrient state.
        
        Args:
            name: Nutrient name
            element_symbol: Chemical symbol
            amount: Amount in mg
            bioavailability: Bioavailability fraction (0-1)
            category: NutrientCategory
            **kwargs: Additional properties
            
        Returns:
            NutrientState
        """
        # Create coherence state with bioavailability as NRCI
        log_error = math.log(1 - bioavailability) if bioavailability < 1.0 else math.log(1e-10)
        coherence = CoherenceState(amount, log_nrci_error=log_error)
        
        return NutrientState(
            name=name,
            element_symbol=element_symbol,
            coherence=coherence,
            category=category,
            **kwargs
        )
    
    @staticmethod
    def get_essential_nutrients() -> Dict[str, NutrientState]:
        """
        Get database of essential nutrients with typical bioavailabilities.
        
        Returns:
            Dictionary of nutrient name -> NutrientState
        """
        nutrients = {}
        
        # Macrominerals
        nutrients['calcium'] = NutrientDatabase.create_nutrient(
            name='calcium',
            element_symbol='Ca',
            amount=1000.0,  # RDA mg
            bioavailability=0.30,  # 30% typical absorption
            category=NutrientCategory.MACROMINERAL,
            absorption_site='small_intestine',
            transport_protein='calbindin',
            antagonists=['iron', 'zinc', 'magnesium', 'phytate', 'oxalate'],
            synergists=['vitamin_d', 'vitamin_k'],
            circadian_peak='morning',
            coherence_frequency=1e12
        )
        
        nutrients['magnesium'] = NutrientDatabase.create_nutrient(
            name='magnesium',
            element_symbol='Mg',
            amount=400.0,
            bioavailability=0.50,
            category=NutrientCategory.MACROMINERAL,
            absorption_site='small_intestine',
            transport_protein='TRPM6/7',
            antagonists=['calcium', 'phosphate'],
            synergists=['vitamin_d', 'vitamin_b6'],
            circadian_peak='evening',
            coherence_frequency=1.2e12
        )
        
        nutrients['phosphorus'] = NutrientDatabase.create_nutrient(
            name='phosphorus',
            element_symbol='P',
            amount=700.0,
            bioavailability=0.70,
            category=NutrientCategory.MACROMINERAL,
            absorption_site='small_intestine',
            transport_protein='NaPi-IIb',
            antagonists=['calcium', 'magnesium'],
            synergists=['vitamin_d'],
            circadian_peak='morning',
            coherence_frequency=1.1e12
        )
        
        # Trace Elements
        nutrients['iron_heme'] = NutrientDatabase.create_nutrient(
            name='iron_heme',
            element_symbol='Fe',
            amount=18.0,
            bioavailability=0.25,  # Heme iron ~25%
            category=NutrientCategory.TRACE_ELEMENT,
            absorption_site='duodenum',
            transport_protein='transferrin',
            antagonists=['calcium', 'zinc', 'tannins', 'phytate'],
            synergists=['vitamin_c', 'vitamin_a', 'copper'],
            circadian_peak='morning',
            coherence_frequency=5e13
        )
        
        nutrients['iron_nonheme'] = NutrientDatabase.create_nutrient(
            name='iron_nonheme',
            element_symbol='Fe',
            amount=18.0,
            bioavailability=0.10,  # Non-heme iron ~10%
            category=NutrientCategory.TRACE_ELEMENT,
            absorption_site='duodenum',
            transport_protein='transferrin',
            antagonists=['calcium', 'zinc', 'tannins', 'phytate', 'polyphenols'],
            synergists=['vitamin_c', 'vitamin_a', 'copper', 'meat_factor'],
            circadian_peak='morning',
            coherence_frequency=5e13
        )
        
        nutrients['zinc'] = NutrientDatabase.create_nutrient(
            name='zinc',
            element_symbol='Zn',
            amount=11.0,
            bioavailability=0.30,
            category=NutrientCategory.TRACE_ELEMENT,
            absorption_site='small_intestine',
            transport_protein='ZIP4',
            antagonists=['calcium', 'iron', 'copper', 'phytate'],
            synergists=['protein', 'vitamin_a'],
            circadian_peak='morning',
            coherence_frequency=6e13
        )
        
        nutrients['copper'] = NutrientDatabase.create_nutrient(
            name='copper',
            element_symbol='Cu',
            amount=0.9,
            bioavailability=0.55,
            category=NutrientCategory.TRACE_ELEMENT,
            absorption_site='stomach_duodenum',
            transport_protein='CTR1',
            antagonists=['zinc', 'iron', 'molybdenum'],
            synergists=['protein'],
            circadian_peak='morning',
            coherence_frequency=6.5e13
        )
        
        nutrients['manganese'] = NutrientDatabase.create_nutrient(
            name='manganese',
            element_symbol='Mn',
            amount=2.3,
            bioavailability=0.05,
            category=NutrientCategory.TRACE_ELEMENT,
            absorption_site='small_intestine',
            transport_protein='DMT1',
            antagonists=['iron', 'calcium'],
            synergists=[],
            circadian_peak='morning',
            coherence_frequency=5.5e13
        )
        
        # Ultratrace Elements
        nutrients['selenium'] = NutrientDatabase.create_nutrient(
            name='selenium',
            element_symbol='Se',
            amount=0.055,
            bioavailability=0.80,
            category=NutrientCategory.ULTRATRACE,
            absorption_site='duodenum',
            transport_protein='selenoprotein_P',
            antagonists=['heavy_metals'],
            synergists=['vitamin_e'],
            circadian_peak='morning',
            coherence_frequency=1e14
        )
        
        nutrients['chromium'] = NutrientDatabase.create_nutrient(
            name='chromium',
            element_symbol='Cr',
            amount=0.035,
            bioavailability=0.02,
            category=NutrientCategory.ULTRATRACE,
            absorption_site='small_intestine',
            transport_protein='transferrin',
            antagonists=[],
            synergists=['vitamin_c', 'niacin'],
            circadian_peak='morning',
            coherence_frequency=1.2e14
        )
        
        nutrients['molybdenum'] = NutrientDatabase.create_nutrient(
            name='molybdenum',
            element_symbol='Mo',
            amount=0.045,
            bioavailability=0.75,
            category=NutrientCategory.ULTRATRACE,
            absorption_site='stomach_small_intestine',
            transport_protein='unknown',
            antagonists=['copper', 'sulfate'],
            synergists=[],
            circadian_peak='morning',
            coherence_frequency=1.1e14
        )
        
        # Vitamins (selected examples)
        nutrients['vitamin_c'] = NutrientDatabase.create_nutrient(
            name='vitamin_c',
            element_symbol='C6H8O6',
            amount=90.0,
            bioavailability=0.90,
            category=NutrientCategory.VITAMIN_WATER,
            absorption_site='small_intestine',
            transport_protein='SVCT1',
            antagonists=[],
            synergists=['iron', 'vitamin_e'],
            circadian_peak='morning',
            coherence_frequency=2e13
        )
        
        nutrients['vitamin_d'] = NutrientDatabase.create_nutrient(
            name='vitamin_d',
            element_symbol='C27H44O',
            amount=0.020,  # 20 mcg = 800 IU
            bioavailability=0.80,
            category=NutrientCategory.VITAMIN_FAT,
            absorption_site='small_intestine',
            transport_protein='DBP',
            antagonists=[],
            synergists=['calcium', 'magnesium', 'fat'],
            circadian_peak='morning',
            coherence_frequency=3e13
        )
        
        return nutrients


# ============================================================================
# NUTRIENT INTERACTIONS: Coherence Operations
# ============================================================================

class NutrientInteractions:
    """
    Model nutrient interactions as coherence operations.
    """
    
    @staticmethod
    def synergistic_interaction(
        nutrient1: NutrientState,
        nutrient2: NutrientState,
        enhancement_factor: float = 1.5
    ) -> Tuple[NutrientState, NutrientState]:
        """
        Model synergistic interaction (e.g., Vitamin C + Iron).
        
        Mechanism: Y-refinement increases coherence (bioavailability).
        
        Args:
            nutrient1: First nutrient (typically the enhanced one)
            nutrient2: Second nutrient (the enhancer)
            enhancement_factor: Strength of enhancement
            
        Returns:
            Tuple of enhanced nutrient states
        """
        # Nutrient 1 gets enhanced through Y-refinement
        enhanced_coherence = nutrient1.coherence.refine_forward()
        
        # Apply enhancement factor
        if enhancement_factor > 1.0:
            # Additional coherence boost
            boost = math.log(enhancement_factor)
            enhanced_coherence = enhanced_coherence.degrade_by(-boost)  # Negative = improvement
        
        enhanced_nutrient1 = NutrientState(
            name=nutrient1.name,
            element_symbol=nutrient1.element_symbol,
            coherence=enhanced_coherence,
            category=nutrient1.category,
            absorption_site=nutrient1.absorption_site,
            transport_protein=nutrient1.transport_protein,
            antagonists=nutrient1.antagonists,
            synergists=nutrient1.synergists,
            circadian_peak=nutrient1.circadian_peak,
            coherence_frequency=nutrient1.coherence_frequency
        )
        
        # Nutrient 2 slightly depleted (used in enhancement)
        depleted_coherence = nutrient2.coherence.degrade_by(0.01)
        
        enhanced_nutrient2 = NutrientState(
            name=nutrient2.name,
            element_symbol=nutrient2.element_symbol,
            coherence=depleted_coherence,
            category=nutrient2.category,
            absorption_site=nutrient2.absorption_site,
            transport_protein=nutrient2.transport_protein,
            antagonists=nutrient2.antagonists,
            synergists=nutrient2.synergists,
            circadian_peak=nutrient2.circadian_peak,
            coherence_frequency=nutrient2.coherence_frequency
        )
        
        return enhanced_nutrient1, enhanced_nutrient2
    
    @staticmethod
    def antagonistic_interaction(
        nutrient1: NutrientState,
        nutrient2: NutrientState,
        inhibition_factor: float = 0.5
    ) -> Tuple[NutrientState, NutrientState]:
        """
        Model antagonistic interaction (e.g., Calcium vs Iron).
        
        Mechanism: Coherence degradation through competition.
        
        Args:
            nutrient1: First nutrient (inhibited)
            nutrient2: Second nutrient (inhibitor)
            inhibition_factor: Strength of inhibition (0-1)
            
        Returns:
            Tuple of degraded nutrient states
        """
        # Both nutrients degrade due to interference
        degradation = math.log(1 / inhibition_factor) if inhibition_factor > 0 else 1.0
        
        degraded_coherence1 = nutrient1.coherence.degrade_by(degradation)
        degraded_coherence2 = nutrient2.coherence.degrade_by(degradation * 0.5)  # Asymmetric
        
        degraded_nutrient1 = NutrientState(
            name=nutrient1.name,
            element_symbol=nutrient1.element_symbol,
            coherence=degraded_coherence1,
            category=nutrient1.category,
            absorption_site=nutrient1.absorption_site,
            transport_protein=nutrient1.transport_protein,
            antagonists=nutrient1.antagonists,
            synergists=nutrient1.synergists,
            circadian_peak=nutrient1.circadian_peak,
            coherence_frequency=nutrient1.coherence_frequency
        )
        
        degraded_nutrient2 = NutrientState(
            name=nutrient2.name,
            element_symbol=nutrient2.element_symbol,
            coherence=degraded_coherence2,
            category=nutrient2.category,
            absorption_site=nutrient2.absorption_site,
            transport_protein=nutrient2.transport_protein,
            antagonists=nutrient2.antagonists,
            synergists=nutrient2.synergists,
            circadian_peak=nutrient2.circadian_peak,
            coherence_frequency=nutrient2.coherence_frequency
        )
        
        return degraded_nutrient1, degraded_nutrient2
    
    @staticmethod
    def competitive_interaction(
        nutrients: List[NutrientState],
        competition_strength: float = 0.3
    ) -> List[NutrientState]:
        """
        Model competitive interaction among multiple nutrients.
        
        Mechanism: Geometric error from competition for transport proteins.
        
        Args:
            nutrients: List of competing nutrients
            competition_strength: Strength of competition
            
        Returns:
            List of nutrients with competition effects
        """
        if len(nutrients) <= 1:
            return nutrients
        
        # Competition creates geometric error proportional to number of competitors
        n_competitors = len(nutrients)
        competition_error = competition_strength * math.log(n_competitors)
        
        competed_nutrients = []
        for nutrient in nutrients:
            # Each nutrient degrades based on competition
            competed_coherence = nutrient.coherence.degrade_by(competition_error)
            
            # Attempt geometric error correction (body's adaptation)
            restored_coherence, _ = restore_coherence(competed_coherence)
            
            competed_nutrient = NutrientState(
                name=nutrient.name,
                element_symbol=nutrient.element_symbol,
                coherence=restored_coherence,
                category=nutrient.category,
                absorption_site=nutrient.absorption_site,
                transport_protein=nutrient.transport_protein,
                antagonists=nutrient.antagonists,
                synergists=nutrient.synergists,
                circadian_peak=nutrient.circadian_peak,
                coherence_frequency=nutrient.coherence_frequency
            )
            
            competed_nutrients.append(competed_nutrient)
        
        return competed_nutrients


# ============================================================================
# NUTRITION REALM CALCULATOR
# ============================================================================

class NutritionRealm:
    """
    Nutrition realm calculator for UBP 3.5.
    
    Models nutrition as coherence dynamics and information geometry.
    """
    
    def __init__(self):
        """Initialize nutrition realm."""
        self.nutrient_db = NutrientDatabase()
        self.interactions = NutrientInteractions()
    
    def calculate_meal_coherence(
        self,
        nutrients: List[NutrientState]
    ) -> Dict[str, Any]:
        """
        Calculate overall coherence of a meal.
        
        Args:
            nutrients: List of nutrients in meal
            
        Returns:
            Dictionary with meal coherence metrics
        """
        if not nutrients:
            return {'mean_nrci': 0.0, 'total_amount': 0.0, 'coherence_score': 0.0}
        
        # Mean NRCI (bioavailability)
        mean_nrci = sum(n.bioavailability for n in nutrients) / len(nutrients)
        
        # Total nutrient amount
        total_amount = sum(n.amount for n in nutrients)
        
        # Coherence score (weighted by amount)
        coherence_score = sum(n.amount * n.bioavailability for n in nutrients) / (total_amount + 1e-10)
        
        # Category distribution
        categories = {}
        for nutrient in nutrients:
            cat = nutrient.category.value
            if cat not in categories:
                categories[cat] = {'count': 0, 'total_amount': 0.0, 'mean_nrci': 0.0}
            categories[cat]['count'] += 1
            categories[cat]['total_amount'] += nutrient.amount
            categories[cat]['mean_nrci'] += nutrient.bioavailability
        
        for cat in categories:
            categories[cat]['mean_nrci'] /= categories[cat]['count']
        
        return {
            'mean_nrci': mean_nrci,
            'total_amount': total_amount,
            'coherence_score': coherence_score,
            'n_nutrients': len(nutrients),
            'categories': categories
        }
    
    def apply_interactions(
        self,
        nutrients: Dict[str, NutrientState]
    ) -> Dict[str, NutrientState]:
        """
        Apply all nutrient interactions.
        
        Args:
            nutrients: Dictionary of nutrient name -> NutrientState
            
        Returns:
            Dictionary of nutrients after interactions
        """
        result = nutrients.copy()
        
        # Apply synergistic interactions
        if 'vitamin_c' in result and 'iron_nonheme' in result:
            enhanced_iron, depleted_c = self.interactions.synergistic_interaction(
                result['iron_nonheme'],
                result['vitamin_c'],
                enhancement_factor=2.0  # Vitamin C doubles non-heme iron absorption
            )
            result['iron_nonheme'] = enhanced_iron
            result['vitamin_c'] = depleted_c
        
        # Apply antagonistic interactions
        if 'calcium' in result and 'iron_nonheme' in result:
            inhibited_iron, _ = self.interactions.antagonistic_interaction(
                result['iron_nonheme'],
                result['calcium'],
                inhibition_factor=0.6  # Calcium reduces iron absorption by ~40%
            )
            result['iron_nonheme'] = inhibited_iron
        
        # Apply competitive interactions for minerals
        competing_minerals = []
        mineral_names = []
        for name, nutrient in result.items():
            if nutrient.category in [NutrientCategory.MACROMINERAL, NutrientCategory.TRACE_ELEMENT]:
                competing_minerals.append(nutrient)
                mineral_names.append(name)
        
        if len(competing_minerals) > 1:
            competed = self.interactions.competitive_interaction(
                competing_minerals,
                competition_strength=0.2
            )
            for name, nutrient in zip(mineral_names, competed):
                result[name] = nutrient
        
        return result


# ============================================================================
# DEMONSTRATION
# ============================================================================

if __name__ == "__main__":
    print("=" * 80)
    print("UBP 3.5 NUTRITION REALM - Nutrition as Coherence Dynamics")
    print("=" * 80)
    
    # Create nutrition realm
    print("\n1. Creating Nutrition Realm:")
    realm = NutritionRealm()
    print(f"   Nutrient database loaded")
    
    # Get essential nutrients
    print("\n2. Essential Nutrients:")
    nutrients = NutrientDatabase.get_essential_nutrients()
    print(f"   Total nutrients: {len(nutrients)}")
    for name, nutrient in list(nutrients.items())[:5]:
        print(f"   {nutrient}")
    
    # Test synergistic interaction (Vitamin C + Iron)
    print("\n3. Synergistic Interaction (Vitamin C + Iron):")
    iron = nutrients['iron_nonheme']
    vit_c = nutrients['vitamin_c']
    print(f"   Before: {iron.name} NRCI={iron.bioavailability:.4f}")
    enhanced_iron, _ = NutrientInteractions.synergistic_interaction(iron, vit_c, enhancement_factor=2.0)
    print(f"   After:  {enhanced_iron.name} NRCI={enhanced_iron.bioavailability:.4f}")
    print(f"   Enhancement: {(enhanced_iron.bioavailability / iron.bioavailability):.2f}x")
    
    # Test antagonistic interaction (Calcium vs Iron)
    print("\n4. Antagonistic Interaction (Calcium vs Iron):")
    calcium = nutrients['calcium']
    print(f"   Before: {iron.name} NRCI={iron.bioavailability:.4f}")
    inhibited_iron, _ = NutrientInteractions.antagonistic_interaction(iron, calcium, inhibition_factor=0.6)
    print(f"   After:  {inhibited_iron.name} NRCI={inhibited_iron.bioavailability:.4f}")
    print(f"   Inhibition: {(inhibited_iron.bioavailability / iron.bioavailability):.2f}x")
    
    # Test competitive interaction
    print("\n5. Competitive Interaction (Ca, Fe, Zn, Mg):")
    competitors = [nutrients['calcium'], nutrients['iron_nonheme'], nutrients['zinc'], nutrients['magnesium']]
    for c in competitors:
        print(f"   Before: {c.name} NRCI={c.bioavailability:.4f}")
    competed = NutrientInteractions.competitive_interaction(competitors, competition_strength=0.3)
    for c in competed:
        print(f"   After:  {c.name} NRCI={c.bioavailability:.4f}")
    
    # Calculate meal coherence
    print("\n6. Meal Coherence Analysis:")
    meal = [nutrients['iron_nonheme'], nutrients['vitamin_c'], nutrients['calcium'], nutrients['zinc']]
    coherence = realm.calculate_meal_coherence(meal)
    print(f"   Mean NRCI: {coherence['mean_nrci']:.4f}")
    print(f"   Coherence Score: {coherence['coherence_score']:.4f}")
    print(f"   Nutrients: {coherence['n_nutrients']}")
    
    print("\n" + "=" * 80)
    print("UBP 3.5: Nutrition IS Coherence Dynamics")
    print("Bioavailability IS NRCI - Information Geometry in Action")
    print("=" * 80)
