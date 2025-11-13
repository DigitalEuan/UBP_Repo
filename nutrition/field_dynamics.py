        """
        Solve complete field equation over specified time.
        
        This is the coherence-native equivalent of CARFE's solve_carfe_equation.
        """
        num_steps = int(evolution_time / self.time_step)
        evolution_states = [initial_state]
        
        current_state = initial_state
        
        for step in range(num_steps):
            if mode == EvolutionMode.RECURSIVE:
                # Pure recursive evolution
                evolved_field = self.recursive_evolution(current_state.field_values, depth=1)
                new_timestamp = CoherenceState(current_state.timestamp.value + self.time_step)
                new_state = FieldState(
                    timestamp=new_timestamp,
                    field_values=evolved_field,
                    topology=current_state.topology,
                    recursion_level=current_state.recursion_level + 1
                )
            
            elif mode == EvolutionMode.EXPANSIVE:
                # Expansive dynamics
                new_state = self.expansive_dynamics(current_state)
            
            elif mode == EvolutionMode.HYBRID:
                # Combined evolution
                # 1. Recursive step
                recursive_field = self.recursive_evolution(current_state.field_values, depth=1)
                
                # 2. Expansive dynamics
                temp_state = FieldState(
                    timestamp=current_state.timestamp,
                    field_values=recursive_field,
                    topology=current_state.topology,
                    recursion_level=current_state.recursion_level
                )
                expanded_state = self.expansive_dynamics(temp_state)
                
                # 3. Geometric error correction on entire field
                corrected_field = [restore_coherence(fv)[0]  # Extract CoherenceState from tuple
                                 for fv in expanded_state.field_values]
                
                new_state = FieldState(
                    timestamp=expanded_state.timestamp,
                    field_values=corrected_field,
                    topology=expanded_state.topology,
                    recursion_level=current_state.recursion_level + 1,
                    metadata={'evolution_mode': 'hybrid'}
                )
            
            else:
                raise ValueError(f"Unknown evolution mode: {mode}")
            
            evolution_states.append(new_state)
            current_state = new_state
        
        return evolution_states
    
    def analyze_stability(self, evolution_states: List[FieldState]) -> Dict[str, Any]:
        """
        Analyze stability of field evolution through coherence metrics.
        """
        if len(evolution_states) < 2:
            return {'stability': 'insufficient_data'}
        
        # Extract time series
        times = [state.timestamp.value for state in evolution_states]
        energies = [state.energy.value for state in evolution_states]
        nrcis = [state.mean_nrci for state in evolution_states]
        
        # Compute variance
        mean_energy = sum(energies) / len(energies)
        energy_variance = sum((e - mean_energy)**2 for e in energies) / len(energies)
        
        mean_nrci = sum(nrcis) / len(nrcis)
        nrci_variance = sum((n - mean_nrci)**2 for n in nrcis) / len(nrcis)
        
        # Stability classification based on coherence
        if nrci_variance < 0.001 and energy_variance < 0.01:
            stability_class = "stable"
        elif nrci_variance > 0.1:
            stability_class = "decoherent"
        else:
            stability_class = "transitional"
        
        return {
            'stability_class': stability_class,
            'energy_variance': energy_variance,
            'nrci_variance': nrci_variance,
            'mean_energy': mean_energy,
            'mean_nrci': mean_nrci,
            'evolution_duration': times[-1] - times[0],
            'num_states': len(evolution_states)
        }


# ============================================================================
# FACTORY FUNCTIONS
# ============================================================================

def create_field_state(field_size: int = 10,
                      topology: FieldTopology = FieldTopology.CYCLOID,
                      initial_amplitude: float = 1.0) -> FieldState:
    """
    Create initial field state with cycloid geometry.
    
    Args:
        field_size: Number of field points
        topology: Field topology type
        initial_amplitude: Initial field amplitude
    
    Returns:
        Initialized FieldState
    """
    if topology == FieldTopology.CYCLOID:
        cycloid = CycloidGeometry()
        field_values = cycloid.generate_field(0.0, 2*math.pi, field_size)
    else:
        # Default: uniform field
        field_values = [CoherenceState(initial_amplitude) for _ in range(field_size)]
    
    return FieldState(
        timestamp=CoherenceState(0.0),
        field_values=field_values,
        topology=topology,
        recursion_level=0
    )


def create_field_dynamics(recursion_depth: int = 10,
                         zitterbewegung_freq: float = 1.2356e20) -> FieldDynamics:
    """
    Create field dynamics system.
    
    Args:
        recursion_depth: Depth of recursive evolution
        zitterbewegung_freq: Zitterbewegung frequency in Hz
    
    Returns:
        Configured FieldDynamics instance
    """
    return FieldDynamics(
        recursion_depth=recursion_depth,
        zitterbewegung_freq=zitterbewegung_freq
    )


# ============================================================================