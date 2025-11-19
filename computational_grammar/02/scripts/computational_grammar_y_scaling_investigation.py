"""
Y-Scaling Investigation
=======================

The stress tests revealed that the Y-scaling formula has issues.
This script investigates the TRUE relationship between Y, Hamming weight,
and NRCI to find the correct formula.
"""

import sys
import math
import numpy as np
from pathlib import Path

# Add UBP 3.5 to path
ubp_path = Path("/home/ubuntu/UBP_Repo/ubp_3.5")
sys.path.insert(0, str(ubp_path))

from coherence_substrate import GOLDEN_RATIO


def investigate_y_scaling():
    """Find the correct Y-scaling relationship."""
    
    print("\n" + "="*70)
    print("Y-SCALING INVESTIGATION: FINDING THE TRUE FORMULA")
    print("="*70)
    
    Y = GOLDEN_RATIO
    
    # Data from Study 3 (actual OffBit encodings and NRCI values)
    operators_data = {
        'AND': {'hw': 7, 'nrci': 0.9999690},
        'OR': {'hw': 7, 'nrci': 0.9999690},
        'DIV': {'hw': 7, 'nrci': 0.9999560},
        'Y_REFINE': {'hw': 7, 'nrci': 0.9999805},
        'Y_INVERSE': {'hw': 7, 'nrci': 0.9999805},
        'NOT': {'hw': 7, 'nrci': 0.9999790},
        'SUB': {'hw': 8, 'nrci': 0.9999660},
        'XOR': {'hw': 9, 'nrci': 0.9999675},
        'ADD': {'hw': 9, 'nrci': 0.9999660},
        'MUL': {'hw': 9, 'nrci': 0.9999505},
    }
    
    print(f"\nGolden Ratio (Y): {Y:.10f}")
    print(f"1 - Y: {1 - Y:.10f} (NEGATIVE!)")
    print(f"Y - 1: {Y - 1:.10f}")
    print(f"1/Y: {1/Y:.10f}")
    print(f"1 - 1/Y: {1 - 1/Y:.10f}")
    
    # Extract data
    hw_values = np.array([data['hw'] for data in operators_data.values()])
    nrci_values = np.array([data['nrci'] for data in operators_data.values()])
    
    print("\n" + "-"*70)
    print("HYPOTHESIS 1: Linear relationship NRCI = a - b*HW")
    
    # Fit linear model: NRCI = a - b*HW
    # Using least squares
    A = np.vstack([np.ones(len(hw_values)), hw_values]).T
    params, residuals, rank, s = np.linalg.lstsq(A, nrci_values, rcond=None)
    
    a, b = params[0], -params[1]  # Note: we want NRCI = a - b*HW
    
    print(f"\n  Best fit: NRCI = {a:.10f} - {b:.2e} × HW")
    
    # Calculate R²
    ss_res = np.sum((nrci_values - (a - b * hw_values))**2)
    ss_tot = np.sum((nrci_values - np.mean(nrci_values))**2)
    r_squared = 1 - (ss_res / ss_tot)
    
    print(f"  R² = {r_squared:.6f}")
    
    # Compare b to Y-related constants
    print(f"\n  Comparing slope b = {b:.2e} to Y-related values:")
    print(f"    (Y - 1) × 10^-5 = {(Y - 1) * 1e-5:.2e}")
    print(f"    (1 - 1/Y) × 10^-5 = {(1 - 1/Y) * 1e-5:.2e}")
    print(f"    1/Y × 10^-5 = {(1/Y) * 1e-5:.2e}")
    print(f"    Y × 10^-5 = {Y * 1e-5:.2e}")
    
    # Check which is closest
    y_candidates = {
        '(Y - 1) × 10^-5': (Y - 1) * 1e-5,
        '(1 - 1/Y) × 10^-5': (1 - 1/Y) * 1e-5,
        '1/Y × 10^-5': (1/Y) * 1e-5,
        'Y × 10^-5': Y * 1e-5,
        '(Y - 1)² × 10^-5': (Y - 1)**2 * 1e-5,
        '1/(2Y) × 10^-5': (1/(2*Y)) * 1e-5,
    }
    
    closest_name = None
    closest_error = float('inf')
    
    for name, value in y_candidates.items():
        error = abs(b - value)
        if error < closest_error:
            closest_error = error
            closest_name = name
    
    print(f"\n  ✓ Closest match: {closest_name}")
    print(f"    Error: {closest_error:.2e}")
    
    print("\n" + "-"*70)
    print("HYPOTHESIS 2: NRCI varies with Y^HW (exponential)")
    
    # Try: NRCI = a * Y^(-b*HW)
    # Taking log: log(NRCI) = log(a) - b*HW*log(Y)
    
    log_nrci = np.log(nrci_values)
    A_log = np.vstack([np.ones(len(hw_values)), hw_values]).T
    params_log, _, _, _ = np.linalg.lstsq(A_log, log_nrci, rcond=None)
    
    log_a, slope = params_log
    a_exp = np.exp(log_a)
    b_exp = -slope / np.log(Y)
    
    print(f"\n  Best fit: NRCI = {a_exp:.10f} × Y^(-{b_exp:.6f} × HW)")
    
    # Calculate R² for exponential model
    predicted_exp = a_exp * Y**(-b_exp * hw_values)
    ss_res_exp = np.sum((nrci_values - predicted_exp)**2)
    r_squared_exp = 1 - (ss_res_exp / ss_tot)
    
    print(f"  R² = {r_squared_exp:.6f}")
    
    print("\n" + "-"*70)
    print("HYPOTHESIS 3: Corrected linear with absolute value")
    
    # Try: NRCI = a - b*HW where b = |1 - Y| × 10^-5
    b_corrected = abs(1 - Y) * 1e-5
    
    # Find optimal a using grid search
    best_a = None
    best_error = float('inf')
    
    for a_test in np.linspace(0.999, 1.001, 1000):
        predicted = a_test - b_corrected * hw_values
        error = np.sum((nrci_values - predicted)**2)
        if error < best_error:
            best_error = error
            best_a = a_test
    
    a_corrected = best_a
    
    print(f"\n  Formula: NRCI = {a_corrected:.10f} - {b_corrected:.2e} × HW")
    print(f"  Where b = |1 - Y| × 10^-5 = {b_corrected:.2e}")
    
    predicted_corrected = a_corrected - b_corrected * hw_values
    ss_res_corrected = np.sum((nrci_values - predicted_corrected)**2)
    r_squared_corrected = 1 - (ss_res_corrected / ss_tot)
    
    print(f"  R² = {r_squared_corrected:.6f}")
    
    print("\n" + "-"*70)
    print("MODEL COMPARISON:")
    
    models = [
        ("Linear (fitted)", r_squared, a, b),
        ("Exponential", r_squared_exp, a_exp, b_exp),
        ("Corrected linear", r_squared_corrected, a_corrected, b_corrected),
    ]
    
    best_model = max(models, key=lambda x: x[1])
    
    print(f"\n{'Model':<20} {'R²':<12} {'Parameters'}")
    print("-"*70)
    for name, r2, param1, param2 in models:
        marker = "✓" if (name, r2, param1, param2) == best_model else " "
        print(f"{marker} {name:<20} {r2:.8f}  a={param1:.10f}, b={param2:.2e}")
    
    print(f"\n  Best model: {best_model[0]} (R² = {best_model[1]:.8f})")
    
    print("\n" + "-"*70)
    print("DETAILED PREDICTIONS WITH BEST MODEL:")
    
    a_best, b_best = best_model[2], best_model[3]
    
    print(f"\n{'Operator':<12} {'HW':<4} {'Actual':<14} {'Predicted':<14} {'Error':<12}")
    print("-"*70)
    
    for op_name, data in operators_data.items():
        hw = data['hw']
        actual = data['nrci']
        predicted = a_best - b_best * hw
        error = abs(actual - predicted)
        
        print(f"{op_name:<12} {hw:<4} {actual:.10f}  {predicted:.10f}  {error:.2e}")
    
    max_error = max(abs(data['nrci'] - (a_best - b_best * data['hw'])) 
                    for data in operators_data.values())
    
    print(f"\nMax error: {max_error:.2e}")
    
    if max_error < 1e-5:
        print("✓ Achieves claimed precision (< 10^-5)")
    elif max_error < 1e-4:
        print("⚠ Close to claimed precision (< 10^-4)")
    else:
        print("✗ Does not achieve claimed precision")
    
    print("\n" + "="*70)
    print("CONCLUSION")
    print("="*70)
    
    print(f"\nThe correct Y-scaling formula is:")
    print(f"  NRCI = {a_best:.10f} - {b_best:.2e} × HW")
    
    # Identify the Y-relationship
    if abs(b_best - abs(1 - Y) * 1e-5) < 1e-8:
        print(f"\nWhere the slope is: |1 - Y| × 10^-5")
        print(f"  This makes sense because Y > 1, so we need the absolute value")
    elif abs(b_best - (Y - 1) * 1e-5) < 1e-8:
        print(f"\nWhere the slope is: (Y - 1) × 10^-5")
    elif abs(b_best - (1 - 1/Y) * 1e-5) < 1e-8:
        print(f"\nWhere the slope is: (1 - 1/Y) × 10^-5")
    else:
        print(f"\nThe slope {b_best:.2e} doesn't match simple Y-expressions")
        print(f"  This suggests the relationship may be more complex")
    
    # Save corrected formula
    with open("/home/ubuntu/y_scaling_corrected_formula.txt", 'w') as f:
        f.write("CORRECTED Y-SCALING FORMULA\n")
        f.write("="*50 + "\n\n")
        f.write(f"NRCI(ω) = {a_best:.10f} - {b_best:.10f} × HW(ω)\n\n")
        f.write(f"Where:\n")
        f.write(f"  HW(ω) = Hamming weight of operator ω\n")
        f.write(f"  Y = Golden Ratio = {Y:.10f}\n")
        f.write(f"  Slope = {b_best:.10f}\n\n")
        f.write(f"Model fit: R² = {best_model[1]:.8f}\n")
        f.write(f"Max error: {max_error:.2e}\n")
    
    print("\nCorrected formula saved to: y_scaling_corrected_formula.txt")


if __name__ == "__main__":
    investigate_y_scaling()
