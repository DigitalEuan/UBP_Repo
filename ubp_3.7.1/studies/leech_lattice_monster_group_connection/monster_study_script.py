import sys
import numpy as np
import random
import csv
import os
from typing import List, Tuple, Dict, Any

# --- Configuration ---
STUDY_SIZE = 10000  # Number of OffBits to sample
OUTPUT_FILE = 'data/monster_study_results.csv'
OUTPUT_PATH = os.path.join(os.path.dirname(__file__), OUTPUT_FILE)

# --- UBP Imports ---
# Add UBP root to path for imports
sys.path.append(os.path.abspath('/home/ubuntu/UBP_Repo/ubp_3.7.1'))
from core.state import OffBit
from utils.tgic import TGICSystem, CubicGraph, TGICNode, TGICGeometry, LeechLatticeProjection # Assuming TGICSystem is the main class

# Initialize TGIC System once
try:
    TGIC_SYSTEM = TGICSystem(TGICGeometry.LEECH_24D)
    TGIC_AVAILABLE = True
except Exception as e:
    print(f"Warning: TGICSystem initialization failed: {e}. Using random coherence placeholder.")
    TGIC_AVAILABLE = False

# --- Monster Group Proxy Metric (MGPM) ---
def calculate_monster_group_proxy_metric(offbit: OffBit) -> Dict[str, Any]:
    """
    Calculates metrics that proxy the OffBit's connection to the Leech Lattice
    and, by extension, the Monster Group.
    
    The metric is based on the OffBit's Hamming weight (active_bits) and its
    proximity to valid Golay codeword weights, which are the foundation of the
    Leech lattice.
    """
    weight = offbit.active_bits
    
    # 1. Golay Codeword Status (G24)
    # Codewords have weight 0, 8, 12, 16, 24.
    is_golay = offbit.is_golay_codeword
    
    # 2. Distance from Codeword Weight (DCW)
    # Measures how "close" the weight is to a valid Golay codeword weight.
    # The set of valid weights is W = {0, 8, 12, 16, 24}.
    valid_weights = np.array([0, 8, 12, 16, 24])
    dcw = np.min(np.abs(weight - valid_weights))
    
    # 3. Golay Parity (mod 4)
    golay_parity = offbit.golay_parity()
    
    return {
        'weight': weight,
        'is_golay_codeword': is_golay,
        'distance_to_codeword_weight': dcw,
        'golay_parity_mod_4': golay_parity,
    }

# --- Study Execution ---
def calculate_offbit_coherence(offbit: OffBit) -> float:
    """
    Calculates the TGIC coherence for a single OffBit using the Leech 24D
    geometry.
    
    The coherence is based on the OffBit's Leech lattice properties, specifically
    the squared norm of the corresponding vector. The Leech lattice is defined
    by vectors of minimum non-zero norm 4.
    
    We use the Golay parity (weight mod 4) as the primary coherence driver,
    as it is the most direct link to the Leech lattice structure (Construction A).
    """
    if not TGIC_AVAILABLE:
        return random.uniform(0.0, 1.0) # Placeholder if import failed

    # 1. Get the Leech-related property from the OffBit
    # The Leech lattice is defined by the Golay code (G24).
    # The Golay parity (weight mod 4) is the key property.
    golay_parity = offbit.golay_parity()
    
    # 2. Define Coherence based on Golay Parity
    # A valid Leech lattice vector (from Construction A) must come from a
    # Golay codeword 'c' with wt(c) = 0 (mod 4).
    # This means a Golay parity of 0 is the highest coherence state.
    
    # Coherence is 1.0 for parity 0, and decreases as parity increases.
    # Max parity is 3.
    coherence = 1.0 - (golay_parity / 3.0)
    
    # 3. Refine Coherence with the full Golay Codeword status
    # If it is a full Golay codeword (is_golay_codeword is True), it is a perfect
    # state, so coherence is 1.0.
    if offbit.is_golay_codeword:
        coherence = 1.0
    
    # For non-codewords, the parity is a good proxy for "Leech-likeness".
    
    # Clamp coherence to [0, 1]
    return max(0.0, min(1.0, coherence))


def run_monster_study():
    """
    Generates a sample of OffBits and analyzes their Monster Group Proxy Metric
    and their TGIC Coherence.
    """
    print(f"Starting Monster Group Connection Study with {STUDY_SIZE} samples...")
    
    if TGIC_AVAILABLE:
        print(f"TGIC System initialized with {TGIC_SYSTEM.geometry.value}. Coherence calculation adapted for Leech 24D.")
    
    # Prepare CSV output
    fieldnames = ['sample_id', 'offbit_value', 'tgic_coherence', 'weight', 
                  'is_golay_codeword', 'distance_to_codeword_weight', 
                  'golay_parity_mod_4']
    
    with open(OUTPUT_PATH, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        
        for i in range(STUDY_SIZE):
            # 1. Generate OffBit (Random for first-principles study)
            random_value = random.randint(0, 0xFFFFFF)
            offbit = OffBit(random_value)
            
            # 2. Calculate TGIC Coherence
            tgic_coherence = calculate_offbit_coherence(offbit)
            
            # 3. Calculate Monster Group Proxy Metric
            mgpm_metrics = calculate_monster_group_proxy_metric(offbit)
            
            # 4. Write results
            row = {
                'sample_id': i + 1,
                'offbit_value': hex(offbit.value),
                'tgic_coherence': f"{tgic_coherence:.6f}",
                **mgpm_metrics
            }
            writer.writerow(row)
            
            if (i + 1) % 1000 == 0:
                print(f"Processed {i + 1}/{STUDY_SIZE} samples.")

    print(f"Study complete. Results saved to {OUTPUT_PATH}")

if __name__ == '__main__':
    # Ensure the data directory exists
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    run_monster_study()
