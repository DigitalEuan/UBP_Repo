"""
A2 Error Correction Module
-------------------------
Author: Euan Craig, New Zealand
Date: 03 October 2025

This module provides a function to map a 24-bit OffBit (numpy array of 0s and 1s)
to a 2D coordinate based on bit-pair mapping. Designed for error correction
in the context of the A2 lattice.

Usage:
    import numpy as np
    from error_correction.A2_error_correction import map_offbit_to_a2_coordinate

    offbit = np.random.randint(0, 2, 24)
    coord = map_offbit_to_a2_coordinate(offbit)
    print(coord)
"""

import numpy as np

def map_offbit_to_a2_coordinate(offbit: np.ndarray) -> tuple[float, float]:
    """
    Maps a 24-bit OffBit (represented as a numpy array of 0s and 1s)
    to a 2D coordinate (x, y) based on pairs of bits.

    Args:
        offbit (np.ndarray): Array of shape (24,) containing 0s and 1s.

    Returns:
        tuple[float, float]: 2D coordinate (x, y).
    """
    if not isinstance(offbit, np.ndarray):
        raise TypeError("Input must be a numpy ndarray.")
    if offbit.shape != (24,):
        raise ValueError("OffBit must be a 24-element array.")

    # Divide the 24 bits into 12 pairs
    bit_pairs = offbit.reshape(-1, 2)  # Shape (12, 2)
    pair_values = bit_pairs[:, 0] * 2 + bit_pairs[:, 1]  # Shape (12,)

    # First 12 bits (6 pairs) for X, next 12 bits (6 pairs) for Y
    x_pairs = offbit[:12].reshape(-1, 2)
    y_pairs = offbit[12:].reshape(-1, 2)
    x_pair_values = x_pairs[:, 0] * 2 + x_pairs[:, 1]
    y_pair_values = y_pairs[:, 0] * 2 + y_pairs[:, 1]

    # Sum and scale to range [-5, 5]
    x_sum = np.sum(x_pair_values)
    y_sum = np.sum(y_pair_values)
    min_sum, max_sum = 0, 18
    coord_min, coord_max = -5.0, 5.0

    x_coord = coord_min + (coord_max - coord_min) * (x_sum - min_sum) / (max_sum - min_sum)
    y_coord = coord_min + (coord_max - coord_min) * (y_sum - min_sum) / (max_sum - min_sum)

    return (x_coord, y_coord)

if __name__ == "__main__":
    # Example Usage
    dummy_offbit = np.random.randint(0, 2, 24)
    coordinate = map_offbit_to_a2_coordinate(dummy_offbit)
    print(f"Dummy OffBit: {dummy_offbit}")
    print(f"Mapped Coordinate: {coordinate}")

    # Test with an all-zero OffBit
    zero_offbit = np.zeros(24, dtype=int)
    zero_coord = map_offbit_to_a2_coordinate(zero_offbit)
    print(f"\nZero OffBit: {zero_offbit}")
    print(f"Mapped Coordinate: {zero_coord}")  # Expected: (-5.0, -5.0)

    # Test with an all-one OffBit
    one_offbit = np.ones(24, dtype=int)
    one_coord = map_offbit_to_a2_coordinate(one_offbit)
    print(f"\nOne OffBit: {one_offbit}")
    print(f"Mapped Coordinate: {one_coord}")  # Expected: (5.0, 5.0)

    # Test with a mix
    mixed_offbit = np.array([0,1,0,1,0,1,0,1,0,1,0,1, 1,0,1,0,1,0,1,0,1,0,1,0])
    mixed_coord = map_offbit_to_a2_coordinate(mixed_offbit)
    print(f"\nMixed OffBit: {mixed_offbit}")
    print(f"Mapped Coordinate: {mixed_coord}")  # Expected: somewhere in the middle
