import random
from ubp_unified_v5 import GOLAY_ENGINE

def evaluate_permutation(perm, codewords):
    """
    Applies the 24-bit permutation to all codewords and counts the total noisy columns.
    A noisy column is one that breaks the MOG parity rule.
    """
    noisy_columns = 0
    for cw in codewords:
        # Apply permutation
        p_cw = [cw[perm[i]] for i in range(24)]
        
        # Map to 4x6 MOG grid
        columns = [[p_cw[i], p_cw[i+6], p_cw[i+12], p_cw[i+18]] for i in range(6)]
        parities = [sum(col) % 2 for col in columns]
        
        total_parity = sum(parities)
        if total_parity != 0 and total_parity != 6:
            ones = total_parity
            zeros = 6 - ones
            noisy_columns += min(ones, zeros)
            
    return noisy_columns

def run_mog_hunter():
    print("=== UBP MOG Hunter: Searching for the 24x24 Alignment Key ===")
    
    codewords = GOLAY_ENGINE.get_all_codewords()
    
    # Start with the identity permutation (our current linear slice)
    current_perm = list(range(24))
    current_cost = evaluate_permutation(current_perm, codewords)
    
    print(f"Initial Leakage (Cost): {current_cost} noisy columns")
    print("Initiating Topological Hill-Climb...\n")
    
    iterations = 0
    max_iterations = 5000
    
    while current_cost > 0 and iterations < max_iterations:
        # Propose a new permutation by swapping two random axes
        idx1, idx2 = random.sample(range(24), 2)
        proposed_perm = list(current_perm)
        proposed_perm[idx1], proposed_perm[idx2] = proposed_perm[idx2], proposed_perm[idx1]
        
        proposed_cost = evaluate_permutation(proposed_perm, codewords)
        
        # If the swap reduces or maintains the leakage, accept it (allows lateral movement)
        if proposed_cost <= current_cost:
            if proposed_cost < current_cost:
                print(f"  [Tick {iterations}] Leakage reduced: {current_cost} -> {proposed_cost}")
            current_perm = proposed_perm
            current_cost = proposed_cost
            
        iterations += 1

    print("\n=== SEARCH CONCLUDED ===")
    print(f"Final Leakage: {current_cost} noisy columns")
    if current_cost == 0:
        print("SUCCESS: 24x24 Permutation Key Found!")
        print(f"Key: {current_perm}")
    else:
        print("Local minimum reached. The search space may require simulated annealing or algebraic derivation.")

if __name__ == "__main__":
    run_mog_hunter()