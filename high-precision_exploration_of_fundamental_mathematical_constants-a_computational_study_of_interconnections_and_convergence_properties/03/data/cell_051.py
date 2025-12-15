# Cell 51 from UBP_UNIFIED_SYSTEM_1.ipynb

# @title
e1 = ExactNumber(1)
e_half = ExactNumber(0.5)
e_neg2 = ExactNumber(-2)
e_3_2 = ExactNumber(Fraction(3, 2))

v1 = [ExactNumber(1), ExactNumber(2), ExactNumber(3)]
v2 = [ExactNumber(4), ExactNumber(5), ExactNumber(6)]
v3 = [ExactNumber(1), ExactNumber(0.5), ExactNumber(-1)] # Used for dot product, which produces an integer ExactNumber

# New vector for euclidean_norm_squared that produces a valid integer ExactNumber result
v_norm_test = [ExactNumber(1), ExactNumber(1), ExactNumber(0)] # Norm squared = 1*1 + 1*1 + 0*0 = 2

print("\n--- Testing Vector and Matrix Operations with ExactNumber ---")

# 1. Test vector_add
result_add = vector_add(v1, v2)
print(f"Vector Addition ({[str(x) for x in v1]} + {[str(x) for x in v2]}): {[str(x) for x in result_add]}")

# 2. Test vector_subtract
result_sub = vector_subtract(v2, v1)
print(f"Vector Subtraction ({[str(x) for x in v2]} - {[str(x) for x in v1]}): {[str(x) for x in result_sub]}")

# 3. Test scalar_vector_multiply
scalar_int = 2
result_scalar_int = scalar_vector_multiply(scalar_int, v1)
print(f"Scalar-Vector Multiply (int) ({scalar_int} * {[str(x) for x in v1]}): {[str(x) for x in result_scalar_int]}")

scalar_exact = ExactNumber(0.5)
result_scalar_exact = scalar_vector_multiply(scalar_exact, v1)
print(f"Scalar-Vector Multiply (ExactNumber) ({str(scalar_exact)} * {[str(x) for x in v1]}): {[str(x) for x in result_scalar_exact]}")

# 4. Test dot_product
result_dot = dot_product(v1, v3)
print(f"Dot Product ({[str(x) for x in v1]} . {[str(x) for x in v3]}): {str(result_dot)}")

# 5. Test euclidean_norm_squared with the new valid vector
result_norm_sq = euclidean_norm_squared(v_norm_test)
print(f"Euclidean Norm Squared ({[str(x) for x in v_norm_test]}): {str(result_norm_sq)}")

# 6. Test matrix_vector_multiply
M = [
    [ExactNumber(1), ExactNumber(0), ExactNumber(1)],
    [ExactNumber(0), ExactNumber(1), ExactNumber(0)],
    [ExactNumber(1), ExactNumber(1), ExactNumber(1)]
]
v_test = [ExactNumber(2), ExactNumber(1), ExactNumber(0.5)]

result_mat_vec_mul = matrix_vector_multiply(M, v_test)
print(f"Matrix-Vector Multiply ({[[str(x) for x in row] for row in M]} @ {[str(x) for x in v_test]}): {[str(x) for x in result_mat_vec_mul]}")

# 7. Test are_vectors_equal
v_equal_1 = [ExactNumber(1), ExactNumber(2), ExactNumber(3)]
v_equal_2 = [ExactNumber(1), ExactNumber(2), ExactNumber(3)]
v_diff = [ExactNumber(1), ExactNumber(2), ExactNumber(4)]

print(f"Vectors Equal ({[str(x) for x in v_equal_1]} == {[str(x) for x in v_equal_2]}): {are_vectors_equal(v_equal_1, v_equal_2)}")
print(f"Vectors Equal ({[str(x) for x in v_equal_1]} == {[str(x) for x in v_diff]}): {are_vectors_equal(v_equal_1, v_diff)}")

print("\n--- End of ExactNumber Vector/Matrix Test ---")
