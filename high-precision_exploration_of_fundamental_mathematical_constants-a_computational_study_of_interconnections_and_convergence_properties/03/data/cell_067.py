# Cell 67 from UBP_UNIFIED_SYSTEM_1.ipynb

# @title Correct and Numerically Stable Archimedes Method from First Principles

# Correct and Numerically Stable Archimedes Method from First Principles
# =======================================================================

# The key insight: We need to track BOTH the inscribed and circumscribed polygons
# to get a numerically stable algorithm, OR use a different geometric relationship.

# Actually, the REAL solution is simpler: use the apothem-based formula correctly!

# For a regular n-gon inscribed in a circle of radius r:
# - Side length: s_n
# - Apothem (perpendicular distance from center to side): a_n = sqrt(r**2 - (s_n/2)**2)

# For the 2n-gon:
# - The new side connects two adjacent vertices of the n-gon
# - By the Pythagorean theorem on the triangle formed:
#   s_{2n}**2 = (s_n/2)**2 + (r - a_n)**2

# This is what we were using, but let's implement it MORE CAREFULLY to avoid
# the numerical issues.

# The problem was in how we calculated things. Let's use a BETTER approach:

# Instead of tracking side length directly, track the HALF-ANGLE θ/2 where:
#   sin(θ/2) = s/(2r)

# For the doubled polygon:
#   sin(θ/4) = sin(θ/2) / sqrt(2 * (1 + cos(θ/2)))

# Where: cos(θ/2) = sqrt(1 - sin**2(θ/2))

# This avoids the catastrophic cancellation!

# Author: Manus AI
# Date: December 06, 2025

# from first_principles_math import sqrt_newton, sin_taylor, abs_value


def archimedes_via_half_angle(max_iterations: int = 40, verbose: bool = True) -> tuple:
    """
    Archimedes method using half-angle tracking for numerical stability.

    Instead of tracking side length directly (which becomes tiny), we track
    sin(θ/2) where θ is the angle subtended by one side at the center.

    For a hexagon: θ = 2π/6 = π/3, so θ/2 = π/6, and sin(π/6) = 0.5

    For doubling: sin(θ_new/2) = sin(θ_old/2) / sqrt(2 * (1 + cos(θ_old/2)))

    Where: cos(θ/2) = sqrt(1 - sin**2(θ/2))

    This is numerically stable because we're always working with values in [0, 1].

    Args:
        max_iterations: Number of doublings
        verbose: Print progress

    Returns:
        (final_pi, history_list)
    """
    if verbose:
        print("=" * 80)
        print("NUMERICALLY STABLE ARCHIMEDES METHOD")
        print("Half-Angle Tracking Approach (First Principles)")
        print("=" * 80)
        print()

    # Initial: hexagon inscribed in unit-diameter circle (radius = 0.5)
    n_sides = 6
    radius = 0.5

    # For hexagon: angle per side = 2π/6 = π/3
    # Half-angle: π/6
    # sin(π/6) = 0.5 (this is a known exact value from geometry)
    sin_half_angle = 0.5

    # Calculate initial π estimate
    # Side length: s = 2 * r * sin(θ/2) = 2 * 0.5 * 0.5 = 0.5
    side_length = 2 * radius * sin_half_angle
    perimeter = n_sides * side_length
    diameter = 2 * radius
    pi_estimate = perimeter / diameter

    history = [pi_estimate]

    if verbose:
        print(f"Iteration  0: n={n_sides:>12}, sin(θ/2)={sin_half_angle:.15f}, π ≈ {pi_estimate:.15f}")

    # Iteratively double the number of sides
    for iteration in range(1, max_iterations + 1):
        # Calculate cos(θ/2) = sqrt(1 - sin²(θ/2))
        sin_squared = sin_half_angle * sin_half_angle
        cos_half_angle = sqrt_newton(1 - sin_squared)

        # Calculate new sin(θ/4) using half-angle formula:
        # sin(θ/4) = sin(θ/2) / sqrt(2 * (1 + cos(θ/2)))
        denominator = sqrt_newton(2 * (1 + cos_half_angle))
        sin_half_angle = sin_half_angle / denominator

        # Double the number of sides
        n_sides = n_sides * 2

        # Calculate new side length and π estimate
        side_length = 2 * radius * sin_half_angle
        perimeter = n_sides * side_length
        pi_estimate = perimeter / diameter

        history.append(pi_estimate)

        if verbose:
            print(f"Iteration {iteration:>2}: n={n_sides:>12}, sin(θ/2)={sin_half_angle:.15f}, π ≈ {pi_estimate:.15f}")

    if verbose:
        print()
        print("=" * 80)
        print(f"FINAL RESULT: π ≈ {pi_estimate:.15f}")
        print("=" * 80)
        print()

    return pi_estimate, history


def test_numerical_stability():
    """
    Test numerical stability across many iterations.
    """
    print("\n")
    print("╔" + "═" * 78 + "╗")
    print("║" + " " * 78 + "║")
    print("║" + "  NUMERICAL STABILITY TEST".center(78) + "║")
    print("║" + "  Half-Angle Tracking Method".center(78) + "║")
    print("║" + " " * 78 + "║")
    print("╚" + "═" * 78 + "╝")
    print("\n")

    reference_pi = 3.141592653589793
    test_iterations = [10, 20, 30, 40, 50]

    print(f"{'Iterations':<12} {'π Estimate':<20} {'Error':<15} {'Status':<10}")
    print("-" * 80)

    for max_iter in test_iterations:
        pi_est, _ = archimedes_via_half_angle(max_iterations=max_iter, verbose=False)
        error = abs_value(pi_est - reference_pi)

        if error < 1e-13:
            status = "✅ Excellent"
        elif error < 1e-10:
            status = "✅ Good"
        elif error < 1e-5:
            status = "⚠️  Degraded"
        else:
            status = "❌ Failed"

        print(f"{max_iter:<12} {pi_est:.15f} {error:.6e}    {status}")

    print()
    print("=" * 80)
    print()


def convergence_rate_analysis():
    """
    Analyze convergence rate to verify quadratic behavior.
    """
    print("\n")
    print("╔" + "═" * 78 + "╗")
    print("║" + " " * 78 + "║")
    print("║" + "  CONVERGENCE RATE ANALYSIS".center(78) + "║")
    print("║" + " " * 78 + "║")
    print("╚" + "═" * 78 + "╝")
    print("\n")

    pi_final, history = archimedes_via_half_angle(max_iterations=30, verbose=False)
    reference_pi = 3.141592653589793

    print(f"{'Iter':<6} {'n_sides':<15} {'π Estimate':<20} {'Error':<15} {'Ratio':<10}")
    print("-" * 80)

    n_sides = 6
    errors = []
    ratios = []

    for i, pi_est in enumerate(history):
        error = abs_value(pi_est - reference_pi)
        errors.append(error)

        if i > 0 and errors[i-1] > 1e-15:  # Avoid division by tiny numbers
            ratio = error / errors[i-1]
            ratios.append(ratio)
        else:
            ratio = 0.0

        if i < 25:  # Print first 25 iterations
            print(f"{i:<6} {n_sides:<15} {pi_est:.15f} {error:.6e}    {ratio:.6f}")

        n_sides *= 2

    # Calculate average ratio from middle iterations (where convergence is stable)
    if len(ratios) > 10:
        middle_ratios = ratios[5:20]  # Use iterations 5-20
        avg_ratio = sum(middle_ratios) / len(middle_ratios)
    else:
        avg_ratio = sum(ratios) / len(ratios) if ratios else 0.0

    print()
    print(f"Average Convergence Ratio (iterations 5-20): {avg_ratio:.6f}")
    print(f"Theoretical Prediction (quadratic):           ~0.25")
    print()

    if 0.24 < avg_ratio < 0.26:
        print("✅ SUCCESS: Convergence matches theoretical prediction!")
        print("   The method exhibits quadratic convergence as expected.")
    else:
        print(f"⚠️  WARNING: Convergence ratio {avg_ratio:.6f} deviates from theory")

    print()
    print("=" * 80)
    print()


if __name__ == "__main__":
    # Run stability test
    test_numerical_stability()

    # Run convergence analysis
    convergence_rate_analysis()

    # Run full demonstration
    print("\nFull Demonstration (40 iterations):")
    print()
    pi_final, history = archimedes_via_half_angle(max_iterations=40, verbose=True)