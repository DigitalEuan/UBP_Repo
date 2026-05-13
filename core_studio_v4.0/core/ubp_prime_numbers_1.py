import os
import csv
from datetime import datetime

# =============================================================================
# 0. UBP KERNEL INTEGRATION
# =============================================================================
# Import the hardened UBP ALU from the v5 kernel
from ubp_unified_v5 import NoiseALU

# Instantiate the ALU once to maintain the manifold state across the test
ubp_alu = NoiseALU(mode="SV")

# =============================================================================
# 1. GROUND TRUTH & TARGET FUNCTIONS
# =============================================================================

def is_prime_ground_truth(n: int) -> bool:
    """Standard deterministic O(sqrt(n)) prime checker for baseline validation."""
    if n < 2: return False
    if n in (2, 3): return True
    if n % 2 == 0 or n % 3 == 0: return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True

def is_prime_target(n: int) -> bool:
    """
    The target function being tested. 
    Now fully hooked into the UBP Unified v5 NoiseALU.
    """
    # The UBP ALU returns a rich dictionary. We extract the boolean result.
    response = ubp_alu.is_prime(n)
    return response["result"]

# =============================================================================
# 2. TEST HARNESS
# =============================================================================

def test_prime_range(low: int, high: int, step: int = 1, name: str = "Range") -> dict:
    """Tests the target prime function over a specific range and step."""
    numbers_tested = list(range(low, high + 1, step))
    
    true_positives = 0
    false_positives = 0
    false_negatives = 0
    
    for num in numbers_tested:
        expected = is_prime_ground_truth(num)
        actual = is_prime_target(num)
        
        if actual and expected:
            true_positives += 1
        elif actual and not expected:
            false_positives += 1
        elif not actual and expected:
            false_negatives += 1
            
    total_tested = len(numbers_tested)
    total_expected_primes = sum(1 for n in numbers_tested if is_prime_ground_truth(n))
    total_found_primes = true_positives + false_positives
    errors = false_positives + false_negatives
    
    # Accuracy = (Total Tested - Errors) / Total Tested
    accuracy = (total_tested - errors) / total_tested if total_tested > 0 else 0.0
    
    return {
        'Range_Name': name,
        'Total_Tested': total_tested,
        'Found_Primes': total_found_primes,
        'Known_Primes': total_expected_primes,
        'True_Positives': true_positives,
        'False_Positives': false_positives,
        'False_Negatives': false_negatives,
        'Total_Errors': errors,
        'Accuracy': accuracy
    }

# =============================================================================
# 3. MAIN EXECUTION
# =============================================================================

def run_prime_diagnostics():
    print("=" * 85)
    print("UBP PRIME DETECTION DIAGNOSTICS (NATIVE NOISE-ALU)")
    print("=" * 85)
    
    ranges = [
        # Test every number from 2 to 1,000
        {"name": "LOW (2-1,000)", "low": 2, "high": 1000, "step": 1},
        
        # Test a continuous block deep in the 10 Million range
        {"name": "MID (10M Block)", "low": 10000000, "high": 10010000, "step": 1},
        
        # Diagonal slice across the 1 Billion range (Stepping by a prime: 997)
        {"name": "HIGH (1B Diagonal)", "low": 100000000, "high": 1000000000, "step": 997}
    ]
    
    results = []
    for r in ranges:
        print(f"Testing {r['name']}... (Step: {r['step']})")
        res = test_prime_range(r['low'], r['high'], r['step'], r['name'])
        results.append(res)
        
    # --- Print Formatted Table ---
    print("\n" + "=" * 85)
    print(f"{'Range':<25} | {'Tested':<8} | {'Found':<8} | {'Known':<8} | {'Errors (FP/FN)':<15} | {'Accuracy'}")
    print("-" * 85)
    
    total_tested = 0
    total_errors = 0
    
    for r in results:
        err_str = f"{r['Total_Errors']} ({r['False_Positives']}/{r['False_Negatives']})"
        acc_str = f"{r['Accuracy']*100:.2f}%"
        print(f"{r['Range_Name']:<25} | {r['Total_Tested']:<8} | {r['Found_Primes']:<8} | {r['Known_Primes']:<8} | {err_str:<15} | {acc_str}")
        
        total_tested += r['Total_Tested']
        total_errors += r['Total_Errors']
        
    total_accuracy = (total_tested - total_errors) / total_tested if total_tested > 0 else 0
    
    print("-" * 85)
    print(f"{'TOTAL':<25} | {total_tested:<8} | {'-':<8} | {'-':<8} | {total_errors:<15} | {total_accuracy*100:.2f}%")
    print("=" * 85)
    
    # --- Save to CSV ---
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"prime_test_results_UBP_{timestamp}.csv"
    
    keys = results[0].keys()
    with open(filename, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(results)
        
    print(f"\n✅ Detailed results saved to: {filename}")

if __name__ == "__main__":
    run_prime_diagnostics()