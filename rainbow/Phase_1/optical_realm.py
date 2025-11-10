        """
        Calculate chromatic dispersion effects.
        
        Args:
            wavelength_range: Array of wavelengths (meters)
            
        Returns:
            Dictionary containing dispersion results
        """
        # Material dispersion (Sellmeier equation for silicon)
        def sellmeier_silicon(lam):
            # Wavelength in micrometers
            lam_um = lam * 1e6
            n_sq = 1 + (10.6684293 * lam_um**2) / (lam_um**2 - 0.301516485**2) + \
                   (0.0030434748 * lam_um**2) / (lam_um**2 - 1.13475115**2) + \
                   (1.54133408 * lam_um**2) / (lam_um**2 - 1104**2)
            return np.sqrt(n_sq)
        
        # Calculate refractive index for wavelength range
        n_values = np.array([sellmeier_silicon(lam) for lam in wavelength_range])
        
        # Group velocity dispersion (GVD)
        c_light = self.photonic_constants['speed_of_light']
        
        # Numerical derivatives for dispersion calculation
        if len(wavelength_range) > 2:
            dn_dlam = np.gradient(n_values, wavelength_range)
            d2n_dlam2 = np.gradient(dn_dlam, wavelength_range)
            
            # Group velocity
            v_g = c_light / (n_values - wavelength_range * dn_dlam)
            
            # GVD parameter
            D = -(wavelength_range / c_light) * d2n_dlam2  # s/m²
            
            # Dispersion length
            pulse_width = 1e-12  # 1 ps pulse
            L_D = pulse_width**2 / np.abs(D)
        else:
            v_g = np.array([c_light / n_values[0]])
            D = np.array([0.0])
            L_D = np.array([np.inf])
        
        return {
            'wavelength_range': wavelength_range,
            'refractive_index': n_values,
            'group_velocity': v_g,
            'dispersion_parameter': D,
            'dispersion_length': L_D,
            'dn_dlambda': dn_dlam if len(wavelength_range) > 2 else np.array([0.0]),
            'd2n_dlambda2': d2n_dlam2 if len(wavelength_range) > 2 else np.array([0.0])
        }
    
    def calculate_coupling_efficiency(self, mode1: PhotonicModeProfile, 
                                    mode2: PhotonicModeProfile) -> float:
        """