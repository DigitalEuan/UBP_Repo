# Cell 102 from UBP_UNIFIED_SYSTEM_1.ipynb

# @title FastExactNumber re-declared
from fractions import Fraction
import math
from typing import Union

# Assuming FastExactNumber is defined in a previous cell or context.
# If not, it would need to be re-declared here for standalone execution.
# For this step, we'll assume FastExactNumber is available.

class FastExactNumber:
    def __init__(self, value: Union[int, Fraction, 'FastExactNumber']):
        if isinstance(value, FastExactNumber):
            self.f = value.f
        elif isinstance(value, Fraction):
            self.f = value
        elif isinstance(value, int):
            self.f = Fraction(value)
        else:
            raise TypeError(f"Unsupported type for FastExactNumber: {type(value)}")

    def to_fraction(self) -> Fraction:
        return self.f

    def __add__(self, other: Union[int, Fraction, 'FastExactNumber']) -> 'FastExactNumber':
        o = FastExactNumber(other)
        return FastExactNumber(self.f + o.f)

    def __radd__(self, other): return self.__add__(other)
    def __sub__(self, other): return FastExactNumber(self.f - FastExactNumber(other).f)
    def __rsub__(self, other): return FastExactNumber(FastExactNumber(other).f - self.f)
    def __mul__(self, other): return FastExactNumber(self.f * FastExactNumber(other).f)
    def __rmul__(self, other): return self.__mul__(other)
    def __truediv__(self, other): return FastExactNumber(self.f / FastExactNumber(other).f)
    def __rtruediv__(self, other): return FastExactNumber(FastExactNumber(other).f / self.f)
    def __neg__(self): return FastExactNumber(-self.f)
    def __abs__(self): return FastExactNumber(abs(self.f))
    def __pow__(self, exp: int):
        if exp >= 0:
            return FastExactNumber(self.f ** exp)
        else:
            return FastExactNumber(1) / (self ** (-exp))

    def __eq__(self, other): return self.f == FastExactNumber(other).f
    def __lt__(self, other): return self.f < FastExactNumber(other).f
    def __le__(self, other): return self.f <= FastExactNumber(other).f
    def __gt__(self, other): return self.f > FastExactNumber(other).f
    def __ge__(self, other): return self.f >= FastExactNumber(other).f
    def __hash__(self): return hash(self.f)
    def __repr__(self): return str(self.f)

    def __int__(self) -> int:
        if self.f.denominator != 1:
            raise ValueError(f"{self.f} is not an integer")
        return int(self.f)

    def round_to_nearest_integer(self) -> 'FastExactNumber':
        return FastExactNumber(round(self.f))

    def sqrt_fast(self, iterations: int = 15) -> 'FastExactNumber':
        if self.f < 0: raise ValueError("Cannot calculate square root of a negative FastExactNumber.")
        if self.f == 0: return FastExactNumber(0)

        guess = FastExactNumber(Fraction(1)) # Initial guess
        for _ in range(iterations):
            new_guess = (guess + self / guess) / FastExactNumber(2)
            if abs(new_guess - guess) < abs(new_guess) / FastExactNumber(10**20) or new_guess.f == guess.f:
                return new_guess
            guess = new_guess
        return guess

def archimedes_pi_exact_fast(sides: int) -> FastExactNumber:
    """
    Derive Pi from first principles using the half-angle method with FastExactNumber.
    """
    if sides < 4 or (sides & (sides - 1)) != 0: # Ensure sides is a power of 2 >= 4
        raise ValueError("Number of sides must be a power of 2 >= 4.")

    # Initialize for a square (n=4) inscribed in a circle of radius 1
    # The half-angle for a square is pi/4, so sin(pi/4) = sqrt(1/2)
    # n_start = FastExactNumber(4)
    # r = FastExactNumber(1)

    # Current sin(half_angle) for a polygon with 'current_n_sides'
    # For a square (n=4), the central angle is pi/2, half_angle = pi/4
    # sin(pi/4) = sqrt(1/2)
    current_sin_half_angle = (FastExactNumber(1) / FastExactNumber(2)).sqrt_fast()

    # Determine the number of doublings needed to reach 'sides' from 4
    # sides = 4 * (2^doublings)
    doublings = int(math.log2(sides / 4))

    # Iterate, applying the half-angle formulas
    for _ in range(doublings):
        # cos(x) = sqrt(1 - sin^2(x))
        cos_half_angle = (FastExactNumber(1) - current_sin_half_angle * current_sin_half_angle).sqrt_fast()

        # sin(x/2) = sqrt((1 - cos(x))/2)
        # This is equivalent to sin(x/2) = sin(x) / sqrt(2 * (1 + cos(x)))
        # We use current_sin_half_angle as sin(x), so new_sin_half_angle is sin(x/2)
        # new_sin_half_angle = ( (FastExactNumber(1) - cos_half_angle) / FastExactNumber(2) ).sqrt_fast()

        # Using the other stable form: new_sin = sin / sqrt(2*(1+cos))
        denominator = (FastExactNumber(2) * (FastExactNumber(1) + cos_half_angle)).sqrt_fast()
        current_sin_half_angle = current_sin_half_angle / denominator

    # After all doublings, the current_sin_half_angle is sin(pi / sides)
    # Pi approximation = sides * sin(pi / sides)
    pi_approx = FastExactNumber(sides) * current_sin_half_angle

    return pi_approx

print("archimedes_pi_exact_fast function defined.")