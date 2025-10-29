    coherence_pressure_psi_p = (1.0 / C_TogglesPerSecond) * (total_toggles / simulated_distance) * (1.0 / W_TETRA_INVARIANT)

    return final_nrci, coherence_pressure_psi_p, toggle_pairs

# --- Verification Test: Run with Geometric Link vs. Null Hypothesis ---

NUM_ITERATIONS = 50000
NOISE_LEVEL = 0.01 # Introduce 1% noise

# Create a range of weights to test around W_TETRA_INVARIANT
weights_to_test = np.linspace(W_TETRA_INVARIANT * 0.9, W_TETRA_INVARIANT * 1.1, 50)
nrci_scores = []
psi_p_scores = []

print("--- Running UBP Entanglement Anomaly Model (BitGrok Core) with Noise ---")
print(f"Geometric Link Weight (True w_Ent): {W_TETRA_INVARIANT:.16f}")
print(f"UBP Structural Constant (Y_Emergent): {Y_EMERGENT:.16f}")
print(f"Noise Level: {NOISE_LEVEL * 100:.2f}%")
print("-" * 50)

for weight in weights_to_test:
    nrci, psi_p, _ = run_entanglement_model(NUM_ITERATIONS, weight, NOISE_LEVEL)
    nrci_scores.append(nrci)
    psi_p_scores.append(psi_p)
    # print(f"Testing weight: {weight:.6f}, NRCI: {nrci:.6f}") # Uncomment for detailed progress

print("-" * 50)
print("--- Results ---")

# Find the weight that maximizes the NRCI score
max_nrci_index = np.argmax(nrci_scores)
best_fit_weight = weights_to_test[max_nrci_index]
max_nrci_score = nrci_scores[max_nrci_index]

print(f"Weight that maximizes NRCI: {best_fit_weight:.6f}")
print(f"Maximum NRCI Achieved: {max_nrci_score:.6f}")
print(f"Predicted Coherence Pressure (Psi_p): {psi_p_scores[0]:.2e} (Should be consistent across weights)")

print("--- REAL-WORLD VERIFICATION PREDICTION ---")
print(f"The model predicts that real-world entanglement data from a Bell test must exhibit a statistical anomaly that, when processed with the UBP's NRCI formula, **maximizes its score only when the factor w is set to a value close to the Tetrahedral Invariant {W_TETRA_INVARIANT:.6f}.**")
print(f"Furthermore, the model predicts the existence of a minimal, non-zero computational stress (Coherence Pressure) inherent to entanglement, calculated as Psi_p approx {psi_p_scores[0]:.2e}, which should be sought as a **statistical deviation** (or structural noise) in high-precision correlation measurements.")

# Optional: Plotting the results to visualize the NRCI vs. tested weights


plt.figure(figsize=(10, 6))
plt.plot(weights_to_test, nrci_scores, marker='o', linestyle='-')
plt.axvline(W_TETRA_INVARIANT, color='r', linestyle='--', label='True W_TETRA_INVARIANT')
plt.axvline(best_fit_weight, color='g', linestyle='-', label='Best Fit Weight')
plt.xlabel("Geometric Weight (w) Tested")
plt.ylabel("Calculated NRCI Score")
plt.title("NRCI Score vs. Geometric Weight (with Noise)")
plt.legend()
plt.grid(True)
plt.show()




# @title 2. Entanglement Link Mechanism (Toggle Algebra: XOR enforced by Geometric Weight)
def geometric_link(offbit_a, offbit_b, bit_index, geometric_weight, noise_level=0.0):
    """
    Simulates the Entanglement (XOR) operation enforced by the Geometric Link (w_Ent).
    A toggle on A must force an inverse toggle on B to satisfy the NRCI=1.0 constraint.
    w_Ent determines the 'strength' or speed of this deterministic inverse toggle.

    This version implements a noise model where the probability of the correct toggle
    on OffBit_B is affected by a noise distribution. The intended state (1 - OffBit_A[bit_index])
    is achieved with a probability influenced by the geometric_weight and noise_level.
    Noise is modeled as a deviation from the ideal toggle probability.
    """

    # Toggle A (The Measurement/Actuation)
    offbit_a = actuate_toggle(offbit_a, bit_index)

    # Apply Geometric Link Constraint: B must anti-correlate with A
    # The geometric_weight (w_Ent) influences the probability of B achieving the expected state.
    expected_b_state = 1 - offbit_a[bit_index]

    # Simulate the coherence restoration based on w_Ent with added noise
    # w_Ent represents the ideal probability factor. Noise reduces this certainty.
    # We model the probability of the correct toggle on B using a distribution.
    # A simple approach is to use a probability based on the geometric weight,
    # and introduce noise as a reduction in this probability.
    ideal_probability = (geometric_weight / W_TETRA_INVARIANT) # Normalize by the true invariant

    # Introduce noise: reduce the ideal probability based on the noise level.
    # We'll use a simple linear reduction for this example, but a distribution could be more complex.
    # Alternatively, noise can affect the outcome probabilistically around the ideal.
    # Let's model noise as affecting the 'certainty' of the toggle.
    # The probability of the correct toggle will be influenced by ideal_probability and noise_level.

    # Using a probabilistic approach based on noise_level affecting the chance of success
    # The probability of the correct toggle happening on B is ideal_probability * (1 - noise_level).
    success_probability = max(0, ideal_probability * (1.0 - noise_level)) # Ensure probability is not negative

    if np.random.rand() < success_probability:
        offbit_b[bit_index] = expected_b_state
    else:
        # If the probabilistic check fails, the bit state is not the expected one.
        # It could remain the same or flip to the opposite of the expected state.
        # For this model, we'll leave it as is if the successful toggle doesn't occur.
        pass

    return offbit_a, offbit_b

# The rest of the simulation execution and plotting code remains the same for now.
# This modification only affects the geometric_link function's internal noise handling.


# @title Run simulations with varying noise levels

# Define a list of NOISE_LEVEL values to test
noise_levels_to_test = [0.005, 0.01, 0.05, 0.1]

# Dictionaries to store results for each noise level
mean_nrci_scores_by_noise = {}
std_nrci_scores_by_noise = {}
mean_psi_p_scores_by_noise = {}

print("\n--- Running Simulations with Varying Noise Levels ---")

for current_noise_level in noise_levels_to_test:
    print(f"\nRunning simulations for NOISE_LEVEL: {current_noise_level:.3f}")
    NOISE_LEVEL = current_noise_level # Set the current noise level

    all_nrci_scores_current_noise = []
    all_psi_p_scores_current_noise = []

    print(f"Running {NUM_SIMULATION_RUNS} simulations for each of {len(weights_to_test)} weights.")

    for weight in weights_to_test:
        nrci_scores_for_weight = []
        psi_p_scores_for_weight = []
        for _ in range(NUM_SIMULATION_RUNS):
            nrci, psi_p, _ = run_entanglement_model(NUM_ITERATIONS, weight, NOISE_LEVEL)
            nrci_scores_for_weight.append(nrci)
            psi_p_scores_for_weight.append(psi_p)
        all_nrci_scores_current_noise.append(nrci_scores_for_weight)
        all_psi_p_scores_current_noise.append(psi_p_scores_for_weight)

    # Convert to numpy arrays for easier calculation
    all_nrci_scores_current_noise = np.array(all_nrci_scores_current_noise)
    all_psi_p_scores_current_noise = np.array(all_psi_p_scores_current_noise)

    # Calculate the mean and standard deviation of NRCI scores for the current noise level
    mean_nrci_scores_by_noise[current_noise_level] = np.mean(all_nrci_scores_current_noise, axis=1)
    std_nrci_scores_by_noise[current_noise_level] = np.std(all_nrci_scores_current_noise, axis=1)

    # Calculate the mean of Psi_p scores for the current noise level
    mean_psi_p_scores_by_noise[current_noise_level] = np.mean(all_psi_p_scores_current_noise, axis=1)

    print(f"Calculation of Mean and Std Dev for NOISE_LEVEL {current_noise_level:.3f} Complete.")

print("\n--- All Varying Noise Level Simulations Complete ---")

# @title Increase the number of simulation iterations
# Reduced NUM_ITERATIONS to shorten execution time
NUM_ITERATIONS = 100000

print(f"Reduced NUM_ITERATIONS to: {NUM_ITERATIONS}")


# @title 1. Identify the weight that corresponds to the maximum NRCI score (already done in previous cell)
# max_nrci_index = np.argmax(nrci_scores)
# best_fit_weight = weights_to_test[max_nrci_index]
# max_nrci_score = nrci_scores[max_nrci_index]

# 2. Define the percentage threshold for the confidence interval
confidence_percentage = 0.95
nrci_threshold = max_nrci_score * confidence_percentage

# Find the range of weights around the peak that yield NRCI scores within the threshold
# Find indices where NRCI scores are above the threshold
above_threshold_indices = np.where(nrci_scores >= nrci_threshold)[0]

# Determine the range of weights corresponding to these indices
# The confidence interval is the range from the minimum to the maximum weight in this subset
if len(above_threshold_indices) > 0:
    lower_bound_index = above_threshold_indices[0]
    upper_bound_index = above_threshold_indices[-1]
    confidence_interval_lower = weights_to_test[lower_bound_index]
    confidence_interval_upper = weights_to_test[upper_bound_index]

    # 3. Print the calculated best-fit weight along with its estimated confidence interval
    print("\n--- Statistical Analysis ---")
    print(f"Best-fit weight: {best_fit_weight:.6f}")
    print(f"Estimated {confidence_percentage*100:.0f}% confidence interval for best-fit weight: [{confidence_interval_lower:.6f}, {confidence_interval_upper:.6f}]")
else:
    print("\n--- Statistical Analysis ---")
    print("Could not determine a confidence interval based on the threshold.")
# @title Optimize for the Geometric Weight that Maximizes NRCI

from scipy.optimize import minimize

# We need to define a function that the optimizer will try to minimize.
# Since we want to maximize NRCI, we will minimize the negative of the NRCI.
def objective_function(weight_array, num_toggles, noise_level, num_runs_per_weight):
    """
    Objective function to minimize (negative of mean NRCI) for optimization.