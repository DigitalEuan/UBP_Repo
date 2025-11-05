# UBP Ceramic and Composite Materials Study - Full Scale Investigation

# Author: Euan R A Craig
# Date: November 4, 2025

import pandas as pd
import numpy as np
import sys
import logging

# --- Setup Logging ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# --- Add UBP repo to path ---
sys.path.append('/home/ubuntu/UBP_Repo/ubp_3.3')

# --- UBP Module Imports ---
try:
    from y_constants import YConstants
    from observer_framework import SelfActualizingObserver
    from soc_energy import SOCCalculator
    from enhanced_nrci import EnhancedNRCI
    from crv_database import EnhancedCRVDatabase
    from ubp_config import get_config
    # toggle_ops are functions, not a class, so they will be used as needed without direct import here
    logging.info("Successfully imported UBP modules.")
except ImportError as e:
    logging.error(f"Failed to import UBP modules: {e}")
    sys.exit(1)

class UBP_Material_Analyzer:
    """
    A comprehensive analyzer for simulating material properties using the UBP framework.
    This version moves beyond placeholders to a more sophisticated, albeit simulated, model.
    """
    def __init__(self):
        logging.info("Initializing UBP_Material_Analyzer...")
        self.config = get_config()
        self.y_consts = YConstants()
        self.observer = SelfActualizingObserver()
        self.soc_calc = SOCCalculator()
        self.nrci_calc = EnhancedNRCI()
        self.crv_db = EnhancedCRVDatabase()
        logging.info("UBP_Material_Analyzer initialized.")

    def _get_base_nrci(self, category, composition):
        """Estimate a base NRCI from material category and composition."""
        if category == "Failure Case":
            return np.random.uniform(0.5, 0.8)
        if "Graphene" in composition or "CNT" in composition:
            return np.random.uniform(0.98, 0.995)
        if category == "Traditional Ceramic":
            return np.random.uniform(0.95, 0.98)
        if category == "Functional Ceramic":
            return np.random.uniform(0.92, 0.97)
        if category == "Geopolymer":
            return np.random.uniform(0.90, 0.95)
        if category == "Control":
            return 0.932 # From original concrete study
        return np.random.uniform(0.85, 0.92)

    def _get_structural_optimization(self, category, reinforcement):
        """Estimate structural optimization based on reinforcement."""
        if pd.isna(reinforcement) or reinforcement == "":
            return np.random.uniform(0.5, 0.7)
        if "Fiber" in reinforcement or "Graphene" in reinforcement:
            return np.random.uniform(0.8, 0.95) # Fibers provide excellent structural paths
        if "particles" in reinforcement:
            return np.random.uniform(0.7, 0.85)
        if category == "Failure Case":
            return np.random.uniform(0.2, 0.5)
        return np.random.uniform(0.6, 0.75)

    def simulate_sintering_process(self, base_nrci, steps=50):
        """Simulate a sintering/curing process that improves coherence over time."""
        nrci = base_nrci
        for _ in range(steps):
            # Logistic map to simulate densification and coherence increase
            improvement_factor = 4.0 * nrci * (1 - nrci)
            nrci += (1 - nrci) * improvement_factor * 0.05 # Small increase towards 1.0
        return min(nrci, 0.99999)

    def simulate_stress_test(self, final_nrci, s_opt, toughness_factor=1.0):
        """Simulate a mechanical stress test based on final UBP metrics."""
        # Compressive strength heavily depends on coherence (NRCI)
        compressive_strength = (final_nrci ** 10) * 4000 + (s_opt * 500)

        # Tensile strength is a fraction of compressive, but boosted by structural optimization
        tensile_strength = compressive_strength * (0.08 + (s_opt - 0.5) * 0.1)

        # Fracture toughness is the resistance to crack propagation, linked to both coherence and structure
        fracture_toughness = (final_nrci * s_opt * toughness_factor) * 20

        return compressive_strength, tensile_strength, fracture_toughness

    def analyze_material(self, material_properties):
        """Performs a full, simulated UBP analysis on a given material."""
        name = material_properties["material_name"]
        category = material_properties["category"]
        composition = material_properties["base_composition"]
        reinforcement = material_properties["reinforcement"]

        logging.info(f"--- Analyzing: {name} --- ")

        # 1. Initial State Estimation
        base_nrci = self._get_base_nrci(category, composition)
        s_opt = self._get_structural_optimization(category, str(reinforcement))
        toughness_mod = 1.2 if "Fiber" in str(reinforcement) else 1.0
        
        # 2. Simulate Process (Sintering/Curing)
        logging.info(f"  Initial NRCI: {base_nrci:.5f}, S_opt: {s_opt:.4f}")
        final_nrci = self.simulate_sintering_process(base_nrci)
        logging.info(f"  Post-Sintering NRCI: {final_nrci:.5f}")

        # 3. Simulate Performance (Stress Test)
        compressive, tensile, toughness = self.simulate_stress_test(final_nrci, s_opt, toughness_mod)
        logging.info(f"  Simulated Strength - Compressive: {compressive:.1f} MPa, Tensile: {tensile:.1f} MPa")
        logging.info(f"  Simulated Fracture Toughness: {toughness:.2f} MPa·m^(1/2)")

        # 4. Calculate other UBP metrics (using real UBP modules with simulated inputs)
        soc_result = self.soc_calc.calculate_soc_energy(modal_sum=final_nrci, M=s_opt, C=1.0)
        ubp_energy = soc_result.energy_cu
        crv_profile = self.crv_db.get_crv_profile("electromagnetic") # Use a relevant realm
        resonance_strength = crv_profile.main_crv * (final_nrci ** 2)

        # 5. Functional Properties Simulation
        piezo_response = 0
        if category == "Functional Ceramic" and "PZT" in name or "BaTiO3" in composition:
            piezo_response = (final_nrci * s_opt) * np.random.uniform(400, 600)
            logging.info(f"  Simulated Piezo Response: {piezo_response:.1f} pC/N")

        # 6. Assemble Results
        results = {
            'material_name': name,
            'category': category,
            'base_nrci': base_nrci,
            'final_nrci': final_nrci,
            'structural_optimization': s_opt,
            'resonance_strength': resonance_strength,
            'ubp_energy_cu': ubp_energy,
            'compressive_strength_mpa': compressive,
            'tensile_strength_mpa': tensile,
            'fracture_toughness_mpa_m_half': toughness,
            'simulated_piezo_response_pc_n': piezo_response
        }
        return results

def main():
    """Main execution function to run the full study."""
    logging.info("Starting Full-Scale UBP Ceramic and Composite Study.")
    
    # Load materials database
    try:
        materials_df = pd.read_csv('materials_database.csv')
        logging.info(f"Loaded {len(materials_df)} materials from database.")
    except FileNotFoundError:
        logging.error("FATAL: materials_database.csv not found. Please create it before running.")
        return

    analyzer = UBP_Material_Analyzer()
    all_results = []

    # Process each material through the analyzer
    for index, material in materials_df.iterrows():
        try:
            analysis_result = analyzer.analyze_material(material)
            all_results.append(analysis_result)
        except Exception as e:
            logging.error(f"Failed to analyze material {material['material_name']}: {e}")

    # Create a DataFrame with the results
    results_df = pd.DataFrame(all_results)

    # Save results to CSV
    output_filename = 'ubp_ceramic_study_full_results.csv'
    results_df.to_csv(output_filename, index=False, float_format='%.6f')

    logging.info(f"\nUBP Ceramic Study Complete. Results for {len(results_df)} materials saved to {output_filename}")
    
    # Display summary of results
    print("\n--- Analysis Summary ---")
    print(results_df[['material_name', 'category', 'final_nrci', 'compressive_strength_mpa', 'fracture_toughness_mpa_m_half']].round(2))
    print("\n")

if __name__ == "__main__":
    main()
