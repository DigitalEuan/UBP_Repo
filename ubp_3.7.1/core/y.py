#!/usr/bin/env python3
"""
UBP 3.7.1 - Y-Constants (Core)
===============================

Core Y-constants with perfect mathematical closure.

Author: Euan R A Craig, New Zealand
Date: November 28, 2025
Version: 3.7.1
"""

import math

# Core Y-constants
PI = math.pi
Y = PI / (PI**2 + 2)
Y_INVERSE = PI + 2/PI

# Verification
assert abs(Y * Y_INVERSE - 1.0) < 1e-10, "Y × Y_INVERSE must equal 1.0"

# Export
__all__ = ['PI', 'Y', 'Y_INVERSE']

if __name__ == "__main__":
    print("="*70)
    print("Y-CONSTANTS (CORE)")
    print("="*70)
    print(f"\nπ = {PI:.15f}")
    print(f"Y = π/(π²+2) = {Y:.15f}")
    print(f"Y_INVERSE = π + 2/π = {Y_INVERSE:.15f}")
    print(f"\nY × Y_INVERSE = {Y * Y_INVERSE:.15f}")
    print(f"Error from 1.0: {abs(Y * Y_INVERSE - 1.0):.2e}")
    print(f"\n✓ Y-constants are mathematically correct")
    print("="*70)
