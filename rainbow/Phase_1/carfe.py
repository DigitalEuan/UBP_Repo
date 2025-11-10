    def parametric_cycloid(self, t: float) -> Tuple[float, float]:
        """
        Compute parametric cycloid coordinates.
        
        Args:
            t: Parameter value
        
        Returns:
            Tuple of (x, y) coordinates
        """
        x = self.radius * (t - math.sin(t))
        y = self.radius * (1 - math.cos(t))
        return x, y
    
    def cycloid_curvature(self, t: float) -> float:
        """
        Compute curvature of cycloid at parameter t.
        
        Args:
            t: Parameter value
        
        Returns:
            Curvature value
        """
        # Curvature κ = 1/(2R*sin(t/2)) for cycloid
        if abs(math.sin(t/2)) < 1e-10:
            return 0.0
        
        curvature = 1.0 / (2 * self.radius * abs(math.sin(t/2)))
        return curvature
    
    def cycloid_arc_length(self, t1: float, t2: float, num_points: int = 100) -> float:
        """
        Compute arc length of cycloid between parameters t1 and t2.
        
        Args:
            t1, t2: Parameter bounds
            num_points: Number of integration points
        
        Returns:
            Arc length
        """
        t_values = np.linspace(t1, t2, num_points)
        dt = (t2 - t1) / (num_points - 1)
        
        arc_length = 0.0
        for t in t_values[:-1]:
            # ds/dt = R * sqrt(2(1 - cos(t))) for cycloid
            ds_dt = self.radius * math.sqrt(2 * (1 - math.cos(t)))
            arc_length += ds_dt * dt
        
        return arc_length
    
    def generate_cycloid_field(self, t_range: Tuple[float, float], 
                             resolution: int = 100) -> np.ndarray:
        """
        Generate cycloid field values over parameter range.
        
        Args:
            t_range: Parameter range (t_min, t_max)
            resolution: Number of field points
        
        Returns:
            Array of field values
        """
        t_values = np.linspace(t_range[0], t_range[1], resolution)
        field_values = np.zeros(resolution, dtype=complex)
        
        for i, t in enumerate(t_values):
            x, y = self.parametric_cycloid(t)
            curvature = self.cycloid_curvature(t)
            
            # Complex field value incorporating geometry
            field_values[i] = complex(x, y) * curvature
        
        return field_values


class CARFEFieldEquation:
    """
    Main CARFE field equation solver.
    
    Implements the complete Cykloid Adelic Recursive Expansive Field Equation
    for UBP system evolution and temporal alignment.
    """
    
    def __init__(self, parameters: Optional[CARFEParameters] = None):
        self.parameters = parameters or CARFEParameters()
        self.p_adic_calc = PAdicCalculator(
            prime=self.parameters.prime_base,
            precision=self.parameters.adelic_precision
        )
        self.cycloid_geom = CykloidGeometry()
        
        self._field_history = deque(maxlen=1000)
        self._evolution_cache = {}
        
    def compute_recursive_field(self, initial_field: np.ndarray, 
                              recursion_depth: Optional[int] = None) -> np.ndarray:
        """
        Compute recursive field evolution.
        
        Args:
            initial_field: Initial field configuration
            recursion_depth: Depth of recursion (uses parameter default if None)
        
        Returns:
            Evolved field after recursion
        """
        depth = recursion_depth or self.parameters.recursion_depth
        current_field = initial_field.copy()
        
        for level in range(depth):
            # Recursive transformation: F_{n+1} = φ * F_n + nonlinear_term
            linear_term = self.parameters.expansion_factor * current_field
            
            # Nonlinear term with p-adic modulation
            nonlinear_term = self.parameters.nonlinearity_strength * np.sin(current_field)
            
            # p-adic correction
            p_adic_correction = np.zeros_like(current_field)
            for i, val in enumerate(current_field):
                if val != 0:
                    p_adic_norm = self.p_adic_calc.p_adic_norm(int(abs(val) * 1000))
                    p_adic_correction[i] = p_adic_norm * 0.01
            
            # Combine terms
            current_field = linear_term + nonlinear_term + p_adic_correction
            
            # Apply damping for stability
            current_field *= self.parameters.damping_factor
        
        return current_field
    
    def compute_expansive_dynamics(self, field_state: FieldState, 
                                 time_step: Optional[float] = None) -> FieldState:
        """
        Compute expansive field dynamics evolution.
        
        Args:
            field_state: Current field state
            time_step: Time step for evolution
        
        Returns:
            Evolved field state
        """
        dt = time_step or self.parameters.time_step
        
        # Compute field derivatives
        field_gradient = np.gradient(field_state.field_values)