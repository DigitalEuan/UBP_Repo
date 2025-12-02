"""
UBP 3.7.1 - Study: Toggle Operations and Golay Structure (toggle_ops_golay_1)
=============================================================================

This script investigates the "Golay Blindspot" of the current toggle operations
by quantifying how much each operation perturbs an OffBit's distance from the
nearest valid Golay(24,12) codeword.

The goal is to identify operations that are "Golay-preserving" or to find patterns
that minimize the distance change.

Author: Manus AI
Date: December 2, 2025
"""

import numpy as np
import pandas as pd
from typing import Callable, Union, Tuple, List
import random
import os
import sys

# Setup path for UBP imports
sys.path.append(os.path.abspath('/home/ubuntu/UBP_Repo/ubp_3.7.1'))

from core.state import OffBit
from error_correction.golay_code import GolayG24
from utils.toggle_ops import toggle_xor, toggle_and, toggle_or, toggle_difference

# Initialize Golay Encoder (Singleton for the study)
GOLAY_ENCODER = GolayG24()

def get_golay_distance(offbit: OffBit) -> int:
    """
    Calculates the Hamming distance from the OffBit to the nearest Golay codeword.
    
    This is the Hamming weight of the error vector returned by the Golay decoder.
    
    Args:
        offbit: The OffBit state to check.
        
    Returns:
        The Hamming distance to the nearest codeword (0-3 for correctable errors).
    """
    bits = np.array(offbit.bits, dtype=int)
    corrected_bits = GOLAY_ENCODER.correct_errors(bits)
    
    # The error vector is the XOR of the original and the corrected codeword
    error_vector = (bits + corrected_bits) % 2
    
    # The distance is the Hamming weight of the error vector
    distance = np.sum(error_vector)
    return int(distance)

def get_golay_distance_after_toggle(
    initial_offbit: OffBit, 
    toggle_op: Callable[[OffBit, OffBit], OffBit], 
    operand_offbit: OffBit
) -> Tuple[int, int, int]:
    """
    Applies a toggle operation and calculates the change in Golay distance.
    
    Args:
        initial_offbit: The first OffBit operand.
        toggle_op: The binary toggle operation to apply (e.g., toggle_xor).
        operand_offbit: The second OffBit operand.
        
    Returns:
        Tuple of (initial_distance, final_distance, distance_change)
    """
    # 1. Calculate initial distance
    initial_distance = get_golay_distance(initial_offbit)
    
    # 2. Apply toggle operation
    result_offbit = toggle_op(initial_offbit, operand_offbit)
    
    # 3. Calculate final distance
    final_distance = get_golay_distance(result_offbit)
    
    # 4. Calculate change
    distance_change = final_distance - initial_distance
    
    return initial_distance, final_distance, distance_change

def run_study(num_trials: int = 10000):
    """
    Runs the full study across various toggle operations and random OffBit pairs.
    """
    print(f"--- Running Toggle Ops Golay Study (N={num_trials}) ---")
    
    toggle_operations = {
        "XOR": toggle_xor,
        "AND": toggle_and,
        "OR": toggle_or,
        "DIFFERENCE": toggle_difference,
    }
    
    results = []
    
    for i in range(num_trials):
        # Generate two random 24-bit OffBits
        val_i = random.randint(0, 0xFFFFFF)
        val_j = random.randint(0, 0xFFFFFF)
        offbit_i = OffBit(val_i)
        offbit_j = OffBit(val_j)
        
        for op_name, op_func in toggle_operations.items():
            # Test op_func(offbit_i, offbit_j)
            initial_dist, final_dist, dist_change = get_golay_distance_after_toggle(
                offbit_i, op_func, offbit_j
            )
            
            results.append({
                "trial": i,
                "op_name": op_name,
                "offbit_i_val": val_i,
                "offbit_j_val": val_j,
                "initial_dist": initial_dist,
                "final_dist": final_dist,
                "dist_change": dist_change,
            })
            
            # Test op_func(offbit_j, offbit_i) for non-commutative ops (e.g., DIFFERENCE)
            if op_name == "DIFFERENCE":
                initial_dist, final_dist, dist_change = get_golay_distance_after_toggle(
                    offbit_j, op_func, offbit_i
                )
                results.append({
                    "trial": i,
                    "op_name": op_name + "_REVERSED",
                    "offbit_i_val": val_j,
                    "offbit_j_val": val_i,
                    "initial_dist": initial_dist,
                    "final_dist": final_dist,
                    "dist_change": dist_change,
                })

    # Convert to DataFrame for analysis
    df = pd.DataFrame(results)
    
    # Save raw data
    output_dir = "/home/ubuntu/UBP_Repo/ubp_3.7.1/studies/toggle_ops_golay_1/data"
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "toggle_ops_golay_raw_data.csv")
    df.to_csv(output_path, index=False)
    print(f"Raw data saved to: {output_path}")
    
    # --- Analysis ---
    print("\n--- Summary Analysis ---")
    
    summary = df.groupby("op_name")["dist_change"].agg(["mean", "std", "min", "max", lambda x: (x == 0).mean() * 100]).reset_index()
    summary.columns = ["Operation", "Mean_Change", "Std_Change", "Min_Change", "Max_Change", "Percent_Zero_Change"]
    
    print(summary.to_markdown(index=False))
    
    # Save summary
    summary_path = os.path.join(output_dir, "toggle_ops_golay_summary.md")
    with open(summary_path, "w") as f:
        f.write("# Toggle Operations Golay Distance Change Summary\n\n")
        f.write(f"Study run with N={num_trials} random OffBit pairs.\n\n")
        f.write(summary.to_markdown(index=False))
    print(f"Summary saved to: {summary_path}")
    
    print("\nStudy Complete.")

if __name__ == '__main__':
    # Increase recursion limit for deep UBP calls
    sys.setrecursionlimit(2000)
    
    # Check for required imports before running
    try:
        # Test imports
        _ = OffBit(0)
        _ = GOLAY_ENCODER
        
        # Run the study
        run_study(num_trials=50000) # Use a large number for statistical significance
        
    except ImportError as e:
        print(f"Error: Required UBP module not found. Please ensure all dependencies are installed and the path is correct. Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred during the study: {e}")
        
