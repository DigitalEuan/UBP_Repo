# Cell 82 from UBP_UNIFIED_SYSTEM_1.ipynb

# @title symbolic engine V1
from sympy import symbols, sqrt, Rational, simplify, pprint, expand

# --- 1. Build symbolic π from nested radical (polygon series) ---
# Example: π approximation via 2^n-gon nested radicals
def build_pi_nested(n_sides):
    """
    Construct π as the nested radical of a 2^n-gon.
    Returns symbolic expression.
    """
    # Base case: sqrt(2)
    expr = sqrt(2)

    # Recurse for n iterations
    for _ in range(n_sides):
        expr = sqrt(2 + expr)

    # π ≈ 2^n * sin(π / 2^n) series simplified via nested radicals
    return expr

# --- 2. Construct Y symbolically ---
def compute_Y(pi_expr):
    """
    Compute Y = π / (π^2 + 2) symbolically
    """
    Y = pi_expr / (pi_expr**2 + 2)
    return simplify(Y)

# --- 3. Compute (1/Y)^n symbolically ---
def power_of_inverse(Y_expr, n):
    """
    Compute (1/Y)^n symbolically
    """
    inv_expr = 1 / Y_expr
    power_expr = inv_expr**n
    return simplify(power_expr)

# --- Example Usage ---
# Choose depth (number of nested radicals, e.g., 4–6 for testing, can go deeper)
depth = 6

# Build symbolic π
pi_sym = build_pi_nested(depth)
print("\nSymbolic π (nested radicals):")
pprint(pi_sym)

# Compute Y
Y_sym = compute_Y(pi_sym)
print("\nSymbolic Y = π / (π^2 + 2):")
pprint(Y_sym)

# Compute (1/Y)^4
inv4_sym = power_of_inverse(Y_sym, 4)
print("\nSymbolic (1/Y)^4:")
pprint(inv4_sym)

# Compute (1/Y)^6
inv6_sym = power_of_inverse(Y_sym, 6)
print("\nSymbolic (1/Y)^6:")
pprint(inv6_sym)

# Optionally, expand or simplify further
print("\nExpanded (1/Y)^4:")
pprint(expand(inv4_sym))

print("\nExpanded (1/Y)^6:")
pprint(expand(inv6_sym))