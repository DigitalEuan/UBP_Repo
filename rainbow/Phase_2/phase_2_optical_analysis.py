    """
    Calculate primary rainbow angle for given wavelength.
    
    Primary rainbow: 1 internal reflection
    
    Args:
        wavelength_nm: Wavelength in nanometers
    
    Returns:
        Rainbow angle in degrees (from antisolar point)
    """
    n = refractive_index_water(wavelength_nm)
    
    # For primary rainbow with 1 internal reflection:
    # The deviation angle D from the incident ray is:
    # D = (i - r) + (π - 2r) + (i - r) = 2i + π - 4r
    # where i is incident angle, r is refracted angle
    # Snell's law: sin(i) = n*sin(r)
    
    # For minimum deviation (brightest rainbow):
    # dD/di = 0 gives: cos(i) = n²*cos(r)
    # Combined with Snell's law: sin²(i) = n²*sin²(r)
    # This gives: i = arcsin(sqrt((4-n²)/3))
    
    # Calculate optimal incident angle
    sin_i_opt = math.sqrt((4 - n**2) / 3)
    i_opt = math.asin(sin_i_opt)
    
    # Calculate refracted angle using Snell's law
    sin_r = sin_i_opt / n
    r_opt = math.asin(sin_r)
    
    # Calculate minimum deviation angle
    D_min = 2*i_opt + math.pi - 4*r_opt
    
    # Rainbow angle from antisolar point (180° - D)
    # Or equivalently, the supplement of the scattering angle
    theta_rainbow = math.pi - D_min
    
    return math.degrees(theta_rainbow)

def rainbow_angle_secondary(wavelength_nm):
    """
    Calculate secondary rainbow angle for given wavelength.
    
    Secondary rainbow: 2 internal reflections
    
    Args:
        wavelength_nm: Wavelength in nanometers
    
    Returns:
        Rainbow angle in degrees (from antisolar point)
    """
    n = refractive_index_water(wavelength_nm)
    
    # For secondary rainbow with 2 internal reflections:
    # Deviation angle: D = 2i - 6r + 2π
    # For minimum deviation: i = arcsin(sqrt((9-n²)/8))
    
    # Calculate optimal incident angle
    sin_i_opt = math.sqrt((9 - n**2) / 8)
    i_opt = math.asin(sin_i_opt)
    
    # Calculate refracted angle
    sin_r = sin_i_opt / n
    r_opt = math.asin(sin_r)
    
    # Calculate minimum deviation
    D_min = 2*i_opt - 6*r_opt + 2*math.pi
    
    # Rainbow angle from antisolar point
    theta_rainbow = D_min - math.pi
    
    return math.degrees(theta_rainbow)

# Test rainbow angle calculation
print("Rainbow angles for test wavelengths:")
print(f"{'Wavelength':>12s} {'n':>10s} {'Primary':>10s} {'Secondary':>12s}")
print("-" * 50)
for wl in wavelengths_test:
    n = refractive_index_water(wl)