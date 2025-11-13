"""
Expanded Nutrient Database for UBP 3.5 Nutrition Study
=======================================================

Comprehensive database of ~100 nutrients spanning:
- Macrominerals (7)
- Trace elements (15)
- Ultratrace elements (10)
- Water-soluble vitamins (9)
- Fat-soluble vitamins (4)
- Amino acids (20)
- Fatty acids (15)
- Phytonutrients (20+)

Each nutrient has unique coherence frequency based on metabolic timescale.
"""

import math
from typing import Dict
from nutrition_realm import NutrientDatabase, NutrientState, NutrientCategory


class ExpandedNutrientDatabase:
    """Comprehensive nutrient database with ~100 nutrients"""
    
    @staticmethod
    def get_all_nutrients() -> Dict[str, NutrientState]:
        """Get comprehensive database of ~100 nutrients"""
        nutrients = {}
        
        # ================================================================
        # MACROMINERALS (7) - Coherence frequency: 1e12 Hz range
        # ================================================================
        
        nutrients['calcium'] = NutrientDatabase.create_nutrient(
            'calcium', 'Ca', 1000.0, 0.30, NutrientCategory.MACROMINERAL,
            absorption_site='small_intestine', transport_protein='calbindin',
            antagonists=['iron', 'zinc', 'magnesium', 'phytate'],
            synergists=['vitamin_d', 'vitamin_k2'],
            circadian_peak='morning', coherence_frequency=1.0e12
        )
        
        nutrients['phosphorus'] = NutrientDatabase.create_nutrient(
            'phosphorus', 'P', 700.0, 0.70, NutrientCategory.MACROMINERAL,
            absorption_site='small_intestine', transport_protein='NaPi-IIb',
            antagonists=['calcium', 'magnesium', 'aluminum'],
            synergists=['vitamin_d'], circadian_peak='morning',
            coherence_frequency=1.1e12
        )
        
        nutrients['magnesium'] = NutrientDatabase.create_nutrient(
            'magnesium', 'Mg', 400.0, 0.50, NutrientCategory.MACROMINERAL,
            absorption_site='small_intestine', transport_protein='TRPM6/7',
            antagonists=['calcium', 'phosphate'], synergists=['vitamin_d', 'vitamin_b6'],
            circadian_peak='evening', coherence_frequency=1.2e12
        )
        
        nutrients['sodium'] = NutrientDatabase.create_nutrient(
            'sodium', 'Na', 2300.0, 0.95, NutrientCategory.MACROMINERAL,
            absorption_site='small_intestine', transport_protein='ENaC',
            antagonists=['potassium'], synergists=['chloride'],
            circadian_peak='morning', coherence_frequency=0.9e12
        )
        
        nutrients['potassium'] = NutrientDatabase.create_nutrient(
            'potassium', 'K', 3500.0, 0.90, NutrientCategory.MACROMINERAL,
            absorption_site='small_intestine', transport_protein='ROMK',
            antagonists=['sodium'], synergists=['magnesium'],
            circadian_peak='evening', coherence_frequency=0.95e12
        )
        
        nutrients['chloride'] = NutrientDatabase.create_nutrient(
            'chloride', 'Cl', 2300.0, 0.95, NutrientCategory.MACROMINERAL,
            absorption_site='small_intestine', transport_protein='CFTR',
            antagonists=[], synergists=['sodium'],
            circadian_peak='morning', coherence_frequency=0.92e12
        )
        
        nutrients['sulfur'] = NutrientDatabase.create_nutrient(
            'sulfur', 'S', 800.0, 0.80, NutrientCategory.MACROMINERAL,
            absorption_site='small_intestine', transport_protein='various',
            antagonists=[], synergists=['methionine', 'cysteine'],
            circadian_peak='morning', coherence_frequency=1.15e12
        )
        
        # ================================================================
        # TRACE ELEMENTS (15) - Coherence frequency: 5e13 Hz range
        # ================================================================
        
        nutrients['iron_heme'] = NutrientDatabase.create_nutrient(
            'iron_heme', 'Fe', 18.0, 0.25, NutrientCategory.TRACE_ELEMENT,
            absorption_site='duodenum', transport_protein='transferrin',
            antagonists=['calcium', 'zinc', 'tannins'],
            synergists=['vitamin_c', 'copper'], circadian_peak='morning',
            coherence_frequency=5.0e13
        )
        
        nutrients['iron_nonheme'] = NutrientDatabase.create_nutrient(
            'iron_nonheme', 'Fe', 18.0, 0.10, NutrientCategory.TRACE_ELEMENT,
            absorption_site='duodenum', transport_protein='transferrin',
            antagonists=['calcium', 'zinc', 'phytate', 'tannins'],
            synergists=['vitamin_c', 'vitamin_a'], circadian_peak='morning',
            coherence_frequency=5.0e13
        )
        
        nutrients['zinc'] = NutrientDatabase.create_nutrient(
            'zinc', 'Zn', 11.0, 0.30, NutrientCategory.TRACE_ELEMENT,
            absorption_site='small_intestine', transport_protein='ZIP4',
            antagonists=['calcium', 'iron', 'copper', 'phytate'],
            synergists=['protein'], circadian_peak='morning',
            coherence_frequency=6.0e13
        )
        
        nutrients['copper'] = NutrientDatabase.create_nutrient(
            'copper', 'Cu', 0.9, 0.55, NutrientCategory.TRACE_ELEMENT,
            absorption_site='stomach_duodenum', transport_protein='CTR1',
            antagonists=['zinc', 'iron', 'molybdenum'],
            synergists=['protein'], circadian_peak='morning',
            coherence_frequency=6.5e13
        )
        
        nutrients['manganese'] = NutrientDatabase.create_nutrient(
            'manganese', 'Mn', 2.3, 0.05, NutrientCategory.TRACE_ELEMENT,
            absorption_site='small_intestine', transport_protein='DMT1',
            antagonists=['iron', 'calcium'], synergists=[],
            circadian_peak='morning', coherence_frequency=5.5e13
        )
        
        nutrients['iodine'] = NutrientDatabase.create_nutrient(
            'iodine', 'I', 0.150, 0.92, NutrientCategory.TRACE_ELEMENT,
            absorption_site='stomach_small_intestine', transport_protein='NIS',
            antagonists=['fluoride', 'bromide'], synergists=['selenium'],
            circadian_peak='morning', coherence_frequency=7.0e13
        )
        
        nutrients['fluoride'] = NutrientDatabase.create_nutrient(
            'fluoride', 'F', 4.0, 0.90, NutrientCategory.TRACE_ELEMENT,
            absorption_site='stomach', transport_protein='passive',
            antagonists=['calcium', 'magnesium'], synergists=[],
            circadian_peak='morning', coherence_frequency=6.8e13
        )
        
        nutrients['cobalt'] = NutrientDatabase.create_nutrient(
            'cobalt', 'Co', 0.001, 0.30, NutrientCategory.TRACE_ELEMENT,
            absorption_site='small_intestine', transport_protein='DMT1',
            antagonists=['iron'], synergists=['vitamin_b12'],
            circadian_peak='morning', coherence_frequency=5.8e13
        )
        
        nutrients['nickel'] = NutrientDatabase.create_nutrient(
            'nickel', 'Ni', 0.005, 0.27, NutrientCategory.TRACE_ELEMENT,
            absorption_site='small_intestine', transport_protein='DMT1',
            antagonists=['iron', 'zinc'], synergists=[],
            circadian_peak='morning', coherence_frequency=5.9e13
        )
        
        nutrients['silicon'] = NutrientDatabase.create_nutrient(
            'silicon', 'Si', 5.0, 0.50, NutrientCategory.TRACE_ELEMENT,
            absorption_site='small_intestine', transport_protein='unknown',
            antagonists=[], synergists=['calcium', 'vitamin_d'],
            circadian_peak='morning', coherence_frequency=6.2e13
        )
        
        nutrients['boron'] = NutrientDatabase.create_nutrient(
            'boron', 'B', 3.0, 0.90, NutrientCategory.TRACE_ELEMENT,
            absorption_site='small_intestine', transport_protein='passive',
            antagonists=[], synergists=['calcium', 'magnesium', 'vitamin_d'],
            circadian_peak='morning', coherence_frequency=6.3e13
        )
        
        nutrients['vanadium'] = NutrientDatabase.create_nutrient(
            'vanadium', 'V', 0.010, 0.05, NutrientCategory.TRACE_ELEMENT,
            absorption_site='small_intestine', transport_protein='unknown',
            antagonists=[], synergists=[],
            circadian_peak='morning', coherence_frequency=6.1e13
        )
        
        nutrients['lithium'] = NutrientDatabase.create_nutrient(
            'lithium', 'Li', 0.001, 0.90, NutrientCategory.TRACE_ELEMENT,
            absorption_site='small_intestine', transport_protein='passive',
            antagonists=['sodium'], synergists=[],
            circadian_peak='evening', coherence_frequency=5.7e13
        )
        
        nutrients['strontium'] = NutrientDatabase.create_nutrient(
            'strontium', 'Sr', 2.0, 0.25, NutrientCategory.TRACE_ELEMENT,
            absorption_site='small_intestine', transport_protein='calcium_channels',
            antagonists=['calcium'], synergists=[],
            circadian_peak='morning', coherence_frequency=5.6e13
        )
        
        nutrients['aluminum'] = NutrientDatabase.create_nutrient(
            'aluminum', 'Al', 0.001, 0.01, NutrientCategory.TRACE_ELEMENT,
            absorption_site='small_intestine', transport_protein='DMT1',
            antagonists=['iron', 'calcium'], synergists=[],
            circadian_peak='morning', coherence_frequency=5.4e13
        )
        
        # ================================================================
        # ULTRATRACE ELEMENTS (10) - Coherence frequency: 1e14 Hz range
        # ================================================================
        
        nutrients['selenium'] = NutrientDatabase.create_nutrient(
            'selenium', 'Se', 0.055, 0.80, NutrientCategory.ULTRATRACE,
            absorption_site='duodenum', transport_protein='selenoprotein_P',
            antagonists=['heavy_metals'], synergists=['vitamin_e'],
            circadian_peak='morning', coherence_frequency=1.0e14
        )
        
        nutrients['chromium'] = NutrientDatabase.create_nutrient(
            'chromium', 'Cr', 0.035, 0.02, NutrientCategory.ULTRATRACE,
            absorption_site='small_intestine', transport_protein='transferrin',
            antagonists=[], synergists=['vitamin_c', 'niacin'],
            circadian_peak='morning', coherence_frequency=1.2e14
        )
        
        nutrients['molybdenum'] = NutrientDatabase.create_nutrient(
            'molybdenum', 'Mo', 0.045, 0.75, NutrientCategory.ULTRATRACE,
            absorption_site='stomach_small_intestine', transport_protein='unknown',
            antagonists=['copper', 'sulfate'], synergists=[],
            circadian_peak='morning', coherence_frequency=1.1e14
        )
        
        nutrients['arsenic'] = NutrientDatabase.create_nutrient(
            'arsenic', 'As', 0.00125, 0.50, NutrientCategory.ULTRATRACE,
            absorption_site='small_intestine', transport_protein='aquaglyceroporins',
            antagonists=['selenium'], synergists=[],
            circadian_peak='morning', coherence_frequency=1.15e14
        )
        
        nutrients['bromine'] = NutrientDatabase.create_nutrient(
            'bromine', 'Br', 0.001, 0.85, NutrientCategory.ULTRATRACE,
            absorption_site='small_intestine', transport_protein='chloride_channels',
            antagonists=['iodine'], synergists=[],
            circadian_peak='morning', coherence_frequency=1.05e14
        )
        
        nutrients['rubidium'] = NutrientDatabase.create_nutrient(
            'rubidium', 'Rb', 0.001, 0.90, NutrientCategory.ULTRATRACE,
            absorption_site='small_intestine', transport_protein='potassium_channels',
            antagonists=['potassium'], synergists=[],
            circadian_peak='morning', coherence_frequency=0.98e14
        )
        
        nutrients['germanium'] = NutrientDatabase.create_nutrient(
            'germanium', 'Ge', 0.0015, 0.30, NutrientCategory.ULTRATRACE,
            absorption_site='small_intestine', transport_protein='unknown',
            antagonists=[], synergists=[],
            circadian_peak='morning', coherence_frequency=1.08e14
        )
        
        nutrients['tin'] = NutrientDatabase.create_nutrient(
            'tin', 'Sn', 0.0017, 0.10, NutrientCategory.ULTRATRACE,
            absorption_site='small_intestine', transport_protein='unknown',
            antagonists=[], synergists=[],
            circadian_peak='morning', coherence_frequency=1.03e14
        )
        
        nutrients['cadmium'] = NutrientDatabase.create_nutrient(
            'cadmium', 'Cd', 0.00001, 0.05, NutrientCategory.ULTRATRACE,
            absorption_site='small_intestine', transport_protein='DMT1',
            antagonists=['zinc', 'iron'], synergists=[],
            circadian_peak='morning', coherence_frequency=1.07e14
        )
        
        nutrients['lead'] = NutrientDatabase.create_nutrient(
            'lead', 'Pb', 0.00001, 0.01, NutrientCategory.ULTRATRACE,
            absorption_site='small_intestine', transport_protein='DMT1',
            antagonists=['calcium', 'iron'], synergists=[],
            circadian_peak='morning', coherence_frequency=1.04e14
        )
        
        # ================================================================
        # WATER-SOLUBLE VITAMINS (9) - Coherence frequency: 2e13 Hz range
        # ================================================================
        
        nutrients['vitamin_c'] = NutrientDatabase.create_nutrient(
            'vitamin_c', 'C6H8O6', 90.0, 0.90, NutrientCategory.VITAMIN_WATER,
            absorption_site='small_intestine', transport_protein='SVCT1',
            antagonists=[], synergists=['iron', 'vitamin_e'],
            circadian_peak='morning', coherence_frequency=2.0e13
        )
        
        nutrients['vitamin_b1'] = NutrientDatabase.create_nutrient(
            'vitamin_b1', 'C12H17N4OS', 1.2, 0.90, NutrientCategory.VITAMIN_WATER,
            absorption_site='small_intestine', transport_protein='SLC19A2',
            antagonists=['alcohol'], synergists=['magnesium'],
            circadian_peak='morning', coherence_frequency=2.1e13
        )
        
        nutrients['vitamin_b2'] = NutrientDatabase.create_nutrient(
            'vitamin_b2', 'C17H20N4O6', 1.3, 0.95, NutrientCategory.VITAMIN_WATER,
            absorption_site='small_intestine', transport_protein='RFVT',
            antagonists=[], synergists=['vitamin_b3', 'vitamin_b6'],
            circadian_peak='morning', coherence_frequency=2.15e13
        )
        
        nutrients['vitamin_b3'] = NutrientDatabase.create_nutrient(
            'vitamin_b3', 'C6H5NO2', 16.0, 0.90, NutrientCategory.VITAMIN_WATER,
            absorption_site='small_intestine', transport_protein='passive',
            antagonists=[], synergists=['chromium'],
            circadian_peak='morning', coherence_frequency=2.2e13
        )
        
        nutrients['vitamin_b5'] = NutrientDatabase.create_nutrient(
            'vitamin_b5', 'C9H17NO5', 5.0, 0.85, NutrientCategory.VITAMIN_WATER,
            absorption_site='small_intestine', transport_protein='SMVT',
            antagonists=[], synergists=['vitamin_b1', 'vitamin_b2'],
            circadian_peak='morning', coherence_frequency=2.25e13
        )
        
        nutrients['vitamin_b6'] = NutrientDatabase.create_nutrient(
            'vitamin_b6', 'C8H11NO3', 1.7, 0.75, NutrientCategory.VITAMIN_WATER,
            absorption_site='small_intestine', transport_protein='passive',
            antagonists=[], synergists=['magnesium', 'zinc'],
            circadian_peak='morning', coherence_frequency=2.3e13
        )
        
        nutrients['vitamin_b7'] = NutrientDatabase.create_nutrient(
            'vitamin_b7', 'C10H16N2O3S', 0.030, 0.90, NutrientCategory.VITAMIN_WATER,
            absorption_site='small_intestine', transport_protein='SMVT',
            antagonists=['avidin'], synergists=[],
            circadian_peak='morning', coherence_frequency=2.35e13
        )
        
        nutrients['vitamin_b9'] = NutrientDatabase.create_nutrient(
            'vitamin_b9', 'C19H19N7O6', 0.400, 0.50, NutrientCategory.VITAMIN_WATER,
            absorption_site='small_intestine', transport_protein='PCFT',
            antagonists=['alcohol'], synergists=['vitamin_b12', 'vitamin_c'],
            circadian_peak='morning', coherence_frequency=2.4e13
        )
        
        nutrients['vitamin_b12'] = NutrientDatabase.create_nutrient(
            'vitamin_b12', 'C63H88CoN14O14P', 0.0024, 0.50, NutrientCategory.VITAMIN_WATER,
            absorption_site='ileum', transport_protein='intrinsic_factor',
            antagonists=['potassium'], synergists=['calcium', 'vitamin_b9'],
            circadian_peak='morning', coherence_frequency=2.45e13
        )
        
        # ================================================================
        # FAT-SOLUBLE VITAMINS (4) - Coherence frequency: 3e13 Hz range
        # ================================================================
        
        nutrients['vitamin_a'] = NutrientDatabase.create_nutrient(
            'vitamin_a', 'C20H30O', 0.900, 0.70, NutrientCategory.VITAMIN_FAT,
            absorption_site='small_intestine', transport_protein='RBP',
            antagonists=[], synergists=['zinc', 'fat', 'vitamin_e'],
            circadian_peak='morning', coherence_frequency=3.0e13
        )
        
        nutrients['vitamin_d'] = NutrientDatabase.create_nutrient(
            'vitamin_d', 'C27H44O', 0.020, 0.80, NutrientCategory.VITAMIN_FAT,
            absorption_site='small_intestine', transport_protein='DBP',
            antagonists=[], synergists=['calcium', 'magnesium', 'fat'],
            circadian_peak='morning', coherence_frequency=3.1e13
        )
        
        nutrients['vitamin_e'] = NutrientDatabase.create_nutrient(
            'vitamin_e', 'C29H50O2', 15.0, 0.75, NutrientCategory.VITAMIN_FAT,
            absorption_site='small_intestine', transport_protein='lipoprotein',
            antagonists=[], synergists=['vitamin_c', 'selenium', 'fat'],
            circadian_peak='morning', coherence_frequency=3.2e13
        )
        
        nutrients['vitamin_k'] = NutrientDatabase.create_nutrient(
            'vitamin_k', 'C31H46O2', 0.120, 0.80, NutrientCategory.VITAMIN_FAT,
            absorption_site='small_intestine', transport_protein='lipoprotein',
            antagonists=['warfarin'], synergists=['calcium', 'vitamin_d', 'fat'],
            circadian_peak='morning', coherence_frequency=3.3e13
        )
        
        # ================================================================
        # ESSENTIAL AMINO ACIDS (9) - Coherence frequency: 4e13 Hz range
        # ================================================================
        
        nutrients['leucine'] = NutrientDatabase.create_nutrient(
            'leucine', 'C6H13NO2', 39.0, 0.95, NutrientCategory.MACRONUTRIENT,
            absorption_site='small_intestine', transport_protein='LAT1',
            antagonists=[], synergists=['isoleucine', 'valine'],
            circadian_peak='morning', coherence_frequency=4.0e13
        )
        
        nutrients['isoleucine'] = NutrientDatabase.create_nutrient(
            'isoleucine', 'C6H13NO2', 20.0, 0.95, NutrientCategory.MACRONUTRIENT,
            absorption_site='small_intestine', transport_protein='LAT1',
            antagonists=[], synergists=['leucine', 'valine'],
            circadian_peak='morning', coherence_frequency=4.05e13
        )
        
        nutrients['valine'] = NutrientDatabase.create_nutrient(
            'valine', 'C5H11NO2', 26.0, 0.95, NutrientCategory.MACRONUTRIENT,
            absorption_site='small_intestine', transport_protein='LAT1',
            antagonists=[], synergists=['leucine', 'isoleucine'],
            circadian_peak='morning', coherence_frequency=4.1e13
        )
        
        nutrients['lysine'] = NutrientDatabase.create_nutrient(
            'lysine', 'C6H14N2O2', 38.0, 0.90, NutrientCategory.MACRONUTRIENT,
            absorption_site='small_intestine', transport_protein='b0,+AT',
            antagonists=['arginine'], synergists=['vitamin_c'],
            circadian_peak='morning', coherence_frequency=4.15e13
        )
        
        nutrients['methionine'] = NutrientDatabase.create_nutrient(
            'methionine', 'C5H11NO2S', 19.0, 0.90, NutrientCategory.MACRONUTRIENT,
            absorption_site='small_intestine', transport_protein='LAT1',
            antagonists=[], synergists=['vitamin_b6', 'vitamin_b12'],
            circadian_peak='morning', coherence_frequency=4.2e13
        )
        
        nutrients['phenylalanine'] = NutrientDatabase.create_nutrient(
            'phenylalanine', 'C9H11NO2', 33.0, 0.90, NutrientCategory.MACRONUTRIENT,
            absorption_site='small_intestine', transport_protein='LAT1',
            antagonists=['tyrosine'], synergists=[],
            circadian_peak='morning', coherence_frequency=4.25e13
        )
        
        nutrients['threonine'] = NutrientDatabase.create_nutrient(
            'threonine', 'C4H9NO3', 20.0, 0.90, NutrientCategory.MACRONUTRIENT,
            absorption_site='small_intestine', transport_protein='B0AT1',
            antagonists=[], synergists=[],
            circadian_peak='morning', coherence_frequency=4.3e13
        )
        
        nutrients['tryptophan'] = NutrientDatabase.create_nutrient(
            'tryptophan', 'C11H12N2O2', 5.0, 0.85, NutrientCategory.MACRONUTRIENT,
            absorption_site='small_intestine', transport_protein='LAT1',
            antagonists=['other_amino_acids'], synergists=['vitamin_b6'],
            circadian_peak='evening', coherence_frequency=4.35e13
        )
        
        nutrients['histidine'] = NutrientDatabase.create_nutrient(
            'histidine', 'C6H9N3O2', 14.0, 0.90, NutrientCategory.MACRONUTRIENT,
            absorption_site='small_intestine', transport_protein='PAT1',
            antagonists=[], synergists=[],
            circadian_peak='morning', coherence_frequency=4.4e13
        )
        
        # ================================================================
        # CONDITIONALLY ESSENTIAL AMINO ACIDS (6)
        # ================================================================
        
        nutrients['arginine'] = NutrientDatabase.create_nutrient(
            'arginine', 'C6H14N4O2', 25.0, 0.90, NutrientCategory.MACRONUTRIENT,
            absorption_site='small_intestine', transport_protein='CAT1',
            antagonists=['lysine'], synergists=['citrulline'],
            circadian_peak='morning', coherence_frequency=4.45e13
        )
        
        nutrients['cysteine'] = NutrientDatabase.create_nutrient(
            'cysteine', 'C3H7NO2S', 4.1, 0.85, NutrientCategory.MACRONUTRIENT,
            absorption_site='small_intestine', transport_protein='EAAT3',
            antagonists=[], synergists=['methionine', 'vitamin_b6'],
            circadian_peak='morning', coherence_frequency=4.5e13
        )
        
        nutrients['tyrosine'] = NutrientDatabase.create_nutrient(
            'tyrosine', 'C9H11NO3', 25.0, 0.90, NutrientCategory.MACRONUTRIENT,
            absorption_site='small_intestine', transport_protein='LAT1',
            antagonists=['phenylalanine'], synergists=['copper', 'vitamin_c'],
            circadian_peak='morning', coherence_frequency=4.55e13
        )
        
        nutrients['glutamine'] = NutrientDatabase.create_nutrient(
            'glutamine', 'C5H10N2O3', 30.0, 0.95, NutrientCategory.MACRONUTRIENT,
            absorption_site='small_intestine', transport_protein='ASCT2',
            antagonists=[], synergists=[],
            circadian_peak='morning', coherence_frequency=4.6e13
        )
        
        nutrients['glycine'] = NutrientDatabase.create_nutrient(
            'glycine', 'C2H5NO2', 10.0, 0.95, NutrientCategory.MACRONUTRIENT,
            absorption_site='small_intestine', transport_protein='GlyT1',
            antagonists=[], synergists=['collagen'],
            circadian_peak='evening', coherence_frequency=4.65e13
        )
        
        nutrients['proline'] = NutrientDatabase.create_nutrient(
            'proline', 'C5H9NO2', 15.0, 0.90, NutrientCategory.MACRONUTRIENT,
            absorption_site='small_intestine', transport_protein='PAT1',
            antagonists=[], synergists=['vitamin_c'],
            circadian_peak='morning', coherence_frequency=4.7e13
        )
        
        # ================================================================
        # ESSENTIAL FATTY ACIDS (4) - Coherence frequency: 3.5e13 Hz range
        # ================================================================
        
        nutrients['omega3_ala'] = NutrientDatabase.create_nutrient(
            'omega3_ala', 'C18H30O2', 1.6, 0.10, NutrientCategory.MACRONUTRIENT,
            absorption_site='small_intestine', transport_protein='lipoprotein',
            antagonists=['omega6'], synergists=['vitamin_e'],
            circadian_peak='morning', coherence_frequency=3.5e13
        )
        
        nutrients['omega3_epa'] = NutrientDatabase.create_nutrient(
            'omega3_epa', 'C20H30O2', 0.250, 0.95, NutrientCategory.MACRONUTRIENT,
            absorption_site='small_intestine', transport_protein='lipoprotein',
            antagonists=['omega6'], synergists=['vitamin_e', 'vitamin_d'],
            circadian_peak='morning', coherence_frequency=3.55e13
        )
        
        nutrients['omega3_dha'] = NutrientDatabase.create_nutrient(
            'omega3_dha', 'C22H32O2', 0.250, 0.95, NutrientCategory.MACRONUTRIENT,
            absorption_site='small_intestine', transport_protein='lipoprotein',
            antagonists=['omega6'], synergists=['vitamin_e', 'phosphatidylserine'],
            circadian_peak='morning', coherence_frequency=3.6e13
        )
        
        nutrients['omega6_la'] = NutrientDatabase.create_nutrient(
            'omega6_la', 'C18H32O2', 17.0, 0.95, NutrientCategory.MACRONUTRIENT,
            absorption_site='small_intestine', transport_protein='lipoprotein',
            antagonists=['omega3'], synergists=[],
            circadian_peak='morning', coherence_frequency=3.52e13
        )
        
        # ================================================================
        # PHYTONUTRIENTS (20+) - Coherence frequency: 2.5e13 Hz range
        # ================================================================
        
        nutrients['quercetin'] = NutrientDatabase.create_nutrient(
            'quercetin', 'C15H10O7', 0.250, 0.20, NutrientCategory.VITAMIN_WATER,
            absorption_site='small_intestine', transport_protein='passive',
            antagonists=[], synergists=['vitamin_c', 'bromelain'],
            circadian_peak='morning', coherence_frequency=2.5e13
        )
        
        nutrients['resveratrol'] = NutrientDatabase.create_nutrient(
            'resveratrol', 'C14H12O3', 0.050, 0.20, NutrientCategory.VITAMIN_WATER,
            absorption_site='small_intestine', transport_protein='passive',
            antagonists=[], synergists=['quercetin'],
            circadian_peak='evening', coherence_frequency=2.52e13
        )
        
        nutrients['curcumin'] = NutrientDatabase.create_nutrient(
            'curcumin', 'C21H20O6', 0.500, 0.01, NutrientCategory.VITAMIN_WATER,
            absorption_site='small_intestine', transport_protein='passive',
            antagonists=[], synergists=['piperine', 'fat'],
            circadian_peak='morning', coherence_frequency=2.54e13
        )
        
        nutrients['epigallocatechin'] = NutrientDatabase.create_nutrient(
            'epigallocatechin', 'C22H18O11', 0.300, 0.15, NutrientCategory.VITAMIN_WATER,
            absorption_site='small_intestine', transport_protein='passive',
            antagonists=['iron'], synergists=['vitamin_c'],
            circadian_peak='morning', coherence_frequency=2.56e13
        )
        
        nutrients['sulforaphane'] = NutrientDatabase.create_nutrient(
            'sulforaphane', 'C6H11NOS2', 0.100, 0.80, NutrientCategory.VITAMIN_WATER,
            absorption_site='small_intestine', transport_protein='passive',
            antagonists=[], synergists=['myrosinase'],
            circadian_peak='morning', coherence_frequency=2.58e13
        )
        
        nutrients['lycopene'] = NutrientDatabase.create_nutrient(
            'lycopene', 'C40H56', 0.015, 0.30, NutrientCategory.VITAMIN_FAT,
            absorption_site='small_intestine', transport_protein='lipoprotein',
            antagonists=[], synergists=['fat', 'vitamin_e'],
            circadian_peak='morning', coherence_frequency=2.6e13
        )
        
        nutrients['beta_carotene'] = NutrientDatabase.create_nutrient(
            'beta_carotene', 'C40H56', 0.006, 0.50, NutrientCategory.VITAMIN_FAT,
            absorption_site='small_intestine', transport_protein='lipoprotein',
            antagonists=[], synergists=['fat', 'vitamin_e'],
            circadian_peak='morning', coherence_frequency=2.62e13
        )
        
        nutrients['lutein'] = NutrientDatabase.create_nutrient(
            'lutein', 'C40H56O2', 0.010, 0.40, NutrientCategory.VITAMIN_FAT,
            absorption_site='small_intestine', transport_protein='lipoprotein',
            antagonists=[], synergists=['fat', 'zeaxanthin'],
            circadian_peak='morning', coherence_frequency=2.64e13
        )
        
        nutrients['zeaxanthin'] = NutrientDatabase.create_nutrient(
            'zeaxanthin', 'C40H56O2', 0.002, 0.40, NutrientCategory.VITAMIN_FAT,
            absorption_site='small_intestine', transport_protein='lipoprotein',
            antagonists=[], synergists=['fat', 'lutein'],
            circadian_peak='morning', coherence_frequency=2.66e13
        )
        
        nutrients['anthocyanins'] = NutrientDatabase.create_nutrient(
            'anthocyanins', 'C15H11O6', 0.200, 0.12, NutrientCategory.VITAMIN_WATER,
            absorption_site='small_intestine', transport_protein='passive',
            antagonists=[], synergists=['vitamin_c'],
            circadian_peak='morning', coherence_frequency=2.68e13
        )
        
        nutrients['ellagic_acid'] = NutrientDatabase.create_nutrient(
            'ellagic_acid', 'C14H6O8', 0.100, 0.20, NutrientCategory.VITAMIN_WATER,
            absorption_site='small_intestine', transport_protein='passive',
            antagonists=[], synergists=[],
            circadian_peak='morning', coherence_frequency=2.7e13
        )
        
        nutrients['genistein'] = NutrientDatabase.create_nutrient(
            'genistein', 'C15H10O5', 0.050, 0.30, NutrientCategory.VITAMIN_WATER,
            absorption_site='small_intestine', transport_protein='passive',
            antagonists=[], synergists=['gut_bacteria'],
            circadian_peak='morning', coherence_frequency=2.72e13
        )
        
        nutrients['indole3carbinol'] = NutrientDatabase.create_nutrient(
            'indole3carbinol', 'C9H9NO', 0.200, 0.50, NutrientCategory.VITAMIN_WATER,
            absorption_site='small_intestine', transport_protein='passive',
            antagonists=[], synergists=[],
            circadian_peak='morning', coherence_frequency=2.74e13
        )
        
        nutrients['capsaicin'] = NutrientDatabase.create_nutrient(
            'capsaicin', 'C18H27NO3', 0.005, 0.90, NutrientCategory.VITAMIN_WATER,
            absorption_site='small_intestine', transport_protein='passive',
            antagonists=[], synergists=[],
            circadian_peak='morning', coherence_frequency=2.76e13
        )
        
        nutrients['allicin'] = NutrientDatabase.create_nutrient(
            'allicin', 'C6H10OS2', 0.010, 0.70, NutrientCategory.VITAMIN_WATER,
            absorption_site='small_intestine', transport_protein='passive',
            antagonists=[], synergists=['alliinase'],
            circadian_peak='morning', coherence_frequency=2.78e13
        )
        
        nutrients['gingerol'] = NutrientDatabase.create_nutrient(
            'gingerol', 'C17H26O4', 0.050, 0.40, NutrientCategory.VITAMIN_WATER,
            absorption_site='small_intestine', transport_protein='passive',
            antagonists=[], synergists=['piperine'],
            circadian_peak='morning', coherence_frequency=2.8e13
        )
        
        nutrients['piperine'] = NutrientDatabase.create_nutrient(
            'piperine', 'C17H19NO3', 0.005, 0.95, NutrientCategory.VITAMIN_WATER,
            absorption_site='small_intestine', transport_protein='passive',
            antagonists=[], synergists=['curcumin', 'many_nutrients'],
            circadian_peak='morning', coherence_frequency=2.82e13
        )
        
        nutrients['chlorophyll'] = NutrientDatabase.create_nutrient(
            'chlorophyll', 'C55H72MgN4O5', 0.100, 0.10, NutrientCategory.VITAMIN_WATER,
            absorption_site='small_intestine', transport_protein='passive',
            antagonists=[], synergists=['magnesium'],
            circadian_peak='morning', coherence_frequency=2.84e13
        )
        
        nutrients['coq10'] = NutrientDatabase.create_nutrient(
            'coq10', 'C59H90O4', 0.100, 0.05, NutrientCategory.VITAMIN_FAT,
            absorption_site='small_intestine', transport_protein='lipoprotein',
            antagonists=[], synergists=['fat', 'vitamin_e'],
            circadian_peak='morning', coherence_frequency=2.86e13
        )
        
        nutrients['alpha_lipoic_acid'] = NutrientDatabase.create_nutrient(
            'alpha_lipoic_acid', 'C8H14O2S2', 0.050, 0.30, NutrientCategory.VITAMIN_WATER,
            absorption_site='small_intestine', transport_protein='MCT',
            antagonists=[], synergists=['vitamin_c', 'vitamin_e'],
            circadian_peak='morning', coherence_frequency=2.88e13
        )
        
        print(f"Expanded database created with {len(nutrients)} nutrients")
        return nutrients


if __name__ == "__main__":
    print("="*80)
    print("EXPANDED NUTRIENT DATABASE")
    print("="*80)
    
    nutrients = ExpandedNutrientDatabase.get_all_nutrients()
    
    # Count by category
    from collections import defaultdict
    categories = defaultdict(list)
    
    for name, nutrient in nutrients.items():
        categories[nutrient.category.value].append(name)
    
    print(f"\nTotal nutrients: {len(nutrients)}")
    print("\nBreakdown by category:")
    for category, names in sorted(categories.items()):
        print(f"  {category:20s}: {len(names):3d} nutrients")
    
    # Frequency range
    frequencies = [n.coherence_frequency for n in nutrients.values()]
    print(f"\nCoherence frequency range:")
    print(f"  Min: {min(frequencies):.2e} Hz")
    print(f"  Max: {max(frequencies):.2e} Hz")
    print(f"  Span: {max(frequencies)/min(frequencies):.1f}x")
    
    print("\n" + "="*80)
