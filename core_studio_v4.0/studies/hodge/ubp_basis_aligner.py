from ubp_unified_v5 import GOLAY_ENGINE

def check_column_parity(vec):
    """
    Checks the 6 columns of a 24-bit vector (mapped 4x6).
    Returns True if ALL columns have the same parity (all even or all odd).
    """
    columns = [[vec[i], vec[i+6], vec[i+12], vec[i+18]] for i in range(6)]
    parities = [sum(col) % 2 for col in columns]
    
    # If all parities are the same, the sum will be 0 (all even) or 6 (all odd)
    total_parity = sum(parities)
    return total_parity == 0 or total_parity == 6, parities

def run_parity_audit():
    print("=== UBP Basis Aligner: Parity Leakage Audit ===")
    
    codewords = GOLAY_ENGINE.get_all_codewords()
    total_codewords = len(codewords)
    aligned_count = 0
    total_columns = total_codewords * 6
    noisy_columns = 0
    
    for cw in codewords:
        is_aligned, parities = check_column_parity(cw)
        if is_aligned:
            aligned_count += 1
        else:
            # Count how many columns deviate from the majority parity
            ones = sum(parities)
            zeros = 6 - ones
            noisy_columns += min(ones, zeros)
            
    print(f"Total Codewords Analyzed: {total_codewords}")
    print(f"Perfectly Aligned Codewords (Zero Noise): {aligned_count}")
    print(f"Misaligned Codewords: {total_codewords - aligned_count}")
    print("-" * 50)
    print(f"Total 4-bit Columns: {total_columns}")
    print(f"Noisy Columns (Parity Leaks): {noisy_columns}")
    
    leakage_rate = (noisy_columns / total_columns) * 100
    print(f"Parity Leakage Rate: {leakage_rate:.2f}%")
    
    print("\n=== CONCLUSION ===")
    if aligned_count < total_codewords:
        print("The Systematic Basis is confirmed to be misaligned with the Semantic MOG.")
        print("We must compute a 24x24 permutation matrix to restore universal parity.")

if __name__ == "__main__":
    run_parity_audit()