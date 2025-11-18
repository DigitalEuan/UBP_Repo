        
        # Set class-level HexDictionary
        CoherenceState.set_hex_dictionary(self.hex_dict, auto_persist=False)
        
        self.results: List[MineralCoherenceResult] = []
    
    def create_base_state(self, crystal_system: str, Z: int) -> CoherenceState:
        """Create base coherence state for a crystal system."""
        pattern = OFFBIT_PATTERNS.get(crystal_system.lower(), OFFBIT_PATTERNS['triclinic'])
        
        # Initialize with base NRCI
        base_log_error = math.log(1 - pattern['base_nrci'])
        
        state = CoherenceState(
            value=pattern['geometric_score'],
            log_nrci_error=base_log_error,
            net_refinements=0,
            history=ComputationHistory(),
            precision_mode=self.precision_mode,
            metadata={
                'crystal_system': crystal_system,
                'Z': Z,
                'symmetry_order': pattern['symmetry_order'],
                'phase': 'initialization'
            }
        )
        
        return state
    
    def apply_geometric_refinements(self, state: CoherenceState, target_refinements: int) -> CoherenceState:
        """Apply Y-refinements based on crystal symmetry."""
        current_state = state
        
        for i in range(target_refinements):
            current_state = current_state.refine_forward()
            current_state.metadata['phase'] = f'refinement_{i+1}'
        
        return current_state
    
    def calculate_degradation(self, Z: int) -> Tuple[float, float, float]:
        """
        Calculate total degradation with enhanced penalties.
        
        Returns:
            (total_degradation, z_penalty, bottleneck_penalty)
        """
        # Base degradation scales linearly with Z
        base_deg = BASE_DEGRADATION * Z
        
        # TGIC constraint (geometric interaction limit)
        tgic_penalty = (1.0 - TGIC_FACTOR) * math.log(max(Z, 2)) * Z_PENALTY_SCALE
        
        # Bottleneck amplification for Z=80-92 (Study 1 discovery)
        bottleneck_penalty = 0.0
        if 80 <= Z <= 92:
            # Extra penalty in bottleneck region
            bottleneck_factor = BOTTLENECK_AMPLIFICATION * (1.0 - abs(Z - 86) / 6.0)
            bottleneck_penalty = bottleneck_factor * BASE_DEGRADATION * Z
        
        # Total degradation in log-error space
        total_deg = base_deg + tgic_penalty + bottleneck_penalty
        
        return total_deg, tgic_penalty, bottleneck_penalty
    
    def apply_complexity_degradation(self, state: CoherenceState, Z: int) -> Tuple[CoherenceState, float, float, float]:
        """
        Apply recalibrated coherence degradation.
        
        Returns:
            (degraded_state, total_degradation, z_penalty, bottleneck_penalty)
        """
        total_deg, z_penalty, bottleneck_penalty = self.calculate_degradation(Z)
        
        degraded_state = state.degrade_by(total_deg)
        degraded_state.metadata['phase'] = 'complexity_degradation'
        degraded_state.metadata['total_degradation'] = total_deg
        degraded_state.metadata['z_penalty'] = z_penalty
        degraded_state.metadata['bottleneck_penalty'] = bottleneck_penalty
        
        return degraded_state, total_deg, z_penalty, bottleneck_penalty
    
    def apply_observer_cost(self, state: CoherenceState) -> CoherenceState:
        """Apply observer measurement cost (1/Y refinement)."""
        observer_state = state.refine_backward()
        observer_state.metadata['phase'] = 'observer_cost'
        observer_state.metadata['O_observer'] = 1.0 / Y
        
        return observer_state
    
    def calculate_mineral_coherence(self, 
                                    name: str,
                                    formula: str,
                                    space_group: int,
                                    crystal_system: str,
                                    Z: int) -> MineralCoherenceResult:
        """
        Calculate full coherence for a mineral structure.
        
        Workflow:
        1. Create base state (crystal system dependent)
        2. Apply geometric refinements (symmetry dependent)
        3. Apply recalibrated complexity degradation (Z dependent)
        4. Apply observer cost
        5. Evaluate against thresholds
        6. Persist to HexDictionary
        """
        # Step 1: Base state
        state = self.create_base_state(crystal_system, Z)
        base_nrci = state.nrci
        
        # Step 2: Geometric refinements
        pattern = OFFBIT_PATTERNS.get(crystal_system.lower(), OFFBIT_PATTERNS['triclinic'])
        state = self.apply_geometric_refinements(state, pattern['Y_refinements'])
        
        # Step 3: Recalibrated complexity degradation
        state, total_deg, z_penalty, bottleneck_penalty = self.apply_complexity_degradation(state, Z)
        
        # Step 4: Observer cost
        state = self.apply_observer_cost(state)
        
        # Step 5: Persist and evaluate
        state.persist()
        final_nrci = state.nrci
        
        result = MineralCoherenceResult(
            name=name,
            formula=formula,
            space_group=space_group,
            crystal_system=crystal_system,
            Z=Z,
            base_nrci=base_nrci,
            final_nrci=final_nrci,
            passes_natural=(final_nrci >= NRCI_NATURAL_MINERAL),
            passes_perfect=(final_nrci >= NRCI_PERFECT_CRYSTAL),
            total_degradation=total_deg,
            z_penalty=z_penalty,
            bottleneck_penalty=bottleneck_penalty,
            net_refinements=state.net_refinements,
            computation_depth=len(state.history.operations),
            hex_address=state.hex_address or "not_persisted",
            history_summary=state.history.get_summary(),
            metadata=state.metadata.copy()
        )
        
        self.results.append(result)
        return result
    
    def batch_calculate(self, minerals: List[Dict[str, Any]]) -> List[MineralCoherenceResult]:
        """Calculate coherence for multiple minerals."""
        results = []