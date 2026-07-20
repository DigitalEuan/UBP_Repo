"""
Rainbow UBP Constants
Study 58: Rainbows as Geometric Resonance
"""

import numpy as np
from math import pi, sqrt

# UBP 3.4 Constants
Y_CONSTANT = pi / (pi**2 + 2)  # 0.264675430404527
Y_INVERSE = pi + 2/pi  # 3.778212425957375
O_OBSERVER = Y_INVERSE
PGCI_TARGET = 0.999997
DARK_DEFICIT_2D = 1 - PGCI_TARGET  # 0.0003%
DARK_DEFICIT_6D = 0.0015  # 0.15%

# Physical Constants
C_LIGHT = 299792458  # m/s
H_PLANCK = 6.62607015e-34  # J·s
N_WATER = 1.333  # refractive index of water (average)

# Sellmeier coefficients for water (visible spectrum)
# n²(λ) = 1 + Σ(Bᵢλ²/(λ² - Cᵢ))
SELLMEIER_B1 = 0.5684
SELLMEIER_C1 = 0.005101  # μm²

# Rainbow Parameters
THETA_CRITICAL_RED = 42.5  # degrees (red light)
THETA_CRITICAL_GREEN = 42.0  # degrees (green light, average)
THETA_CRITICAL_VIOLET = 40.6  # degrees (violet light)

# Wavelengths (m)
WAVELENGTH_RED = 700e-9
WAVELENGTH_ORANGE = 620e-9
WAVELENGTH_YELLOW = 580e-9
WAVELENGTH_GREEN = 550e-9
WAVELENGTH_CYAN = 500e-9
WAVELENGTH_BLUE = 470e-9
WAVELENGTH_VIOLET = 400e-9

# Compute frequencies (Hz)
FREQ_RED = C_LIGHT / WAVELENGTH_RED  # 4.28×10¹⁴ Hz
FREQ_ORANGE = C_LIGHT / WAVELENGTH_ORANGE  # 4.84×10¹⁴ Hz
FREQ_YELLOW = C_LIGHT / WAVELENGTH_YELLOW  # 5.17×10¹⁴ Hz
FREQ_GREEN = C_LIGHT / WAVELENGTH_GREEN  # 5.45×10¹⁴ Hz
FREQ_CYAN = C_LIGHT / WAVELENGTH_CYAN  # 6.00×10¹⁴ Hz
FREQ_BLUE = C_LIGHT / WAVELENGTH_BLUE  # 6.38×10¹⁴ Hz
FREQ_VIOLET = C_LIGHT / WAVELENGTH_VIOLET  # 7.50×10¹⁴ Hz

# Wall of Reality
F_MAX_COHERENT = 1e12  # 1 THz
BIT_TIME = 1e-12  # 1 ps

# Toggle cycles per photon
TOGGLE_CYCLES_RED = FREQ_RED / F_MAX_COHERENT  # ~428 cycles
TOGGLE_CYCLES_GREEN = FREQ_GREEN / F_MAX_COHERENT  # ~545 cycles
TOGGLE_CYCLES_VIOLET = FREQ_VIOLET / F_MAX_COHERENT  # ~750 cycles

# Golden Ratio
PHI = (1 + sqrt(5)) / 2  # 1.618033988749895

# Geometric relationships
Y_PHI_PRODUCT = Y_CONSTANT * PHI  # ≈ 0.428
Y_PI_PRODUCT = Y_CONSTANT * pi  # ≈ 0.832
Y_INV_PI_PRODUCT = Y_INVERSE * pi  # ≈ 11.865

print("=" * 60)
print("RAINBOW UBP CONSTANTS LOADED")
print("=" * 60)
print(f"Y constant: {Y_CONSTANT:.15f}")
print(f"1/Y (O_observer): {Y_INVERSE:.15f}")
print(f"PGCI target: {PGCI_TARGET}")
print(f"Dark deficit (2D): {DARK_DEFICIT_2D:.6%}")
print(f"Dark deficit (6D): {DARK_DEFICIT_6D:.2%}")
print()
print("Visible Spectrum:")
print(f"  Red: {WAVELENGTH_RED*1e9:.0f} nm, {FREQ_RED:.2e} Hz")
print(f"  Green: {WAVELENGTH_GREEN*1e9:.0f} nm, {FREQ_GREEN:.2e} Hz")
print(f"  Violet: {WAVELENGTH_VIOLET*1e9:.0f} nm, {FREQ_VIOLET:.2e} Hz")
print()
print("Toggle Cycles per Coherent State:")
print(f"  Red: {TOGGLE_CYCLES_RED:.1f} cycles")
print(f"  Green: {TOGGLE_CYCLES_GREEN:.1f} cycles")
print(f"  Violet: {TOGGLE_CYCLES_VIOLET:.1f} cycles")
print()
print("Geometric Products:")
print(f"  Y × φ = {Y_PHI_PRODUCT:.6f}")
print(f"  Y × π = {Y_PI_PRODUCT:.6f}")
print(f"  (1/Y) × π = {Y_INV_PI_PRODUCT:.6f}")
print("=" * 60)
