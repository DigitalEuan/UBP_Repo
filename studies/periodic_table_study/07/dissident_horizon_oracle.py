            coherence_states: Optional CoherenceState objects for advanced analysis
            states_history: Optional temporal history of states
            
        Returns:
            Complete analysis with signature, recommendations, and interventions
        """
        # Spectral analysis
        spectral = analyze_spectral_properties(data_matrix)
        
        # PCA variance
        pca_variance = compute_pca_variance_ratio(data_matrix)
        
        # Coherence analysis
        if coherence_states:
            fisher_info = compute_fisher_information_metric(coherence_states)
            coherence_gradient = compute_coherence_gradient(coherence_states)
            
            # Delta deficit (deviation from target NRCI)
            avg_nrci = sum(s.nrci for s in coherence_states) / len(coherence_states)
            delta_deficit = abs(NRCI_TARGET - avg_nrci)
            
            # Net refinements (unactivated state indicator)
            avg_net_ref = sum(abs(s.net_refinements) for s in coherence_states) / len(coherence_states)
        else:
            fisher_info = 0.0
            coherence_gradient = 0.0
            delta_deficit = 0.0
            avg_net_ref = 0
        
        # Temporal memory analysis
        if states_history:
            temporal = analyze_temporal_memory(states_history)
        else:
            temporal = {
                'memory_persistence': 1.0,
                'temporal_stability': 1.0,
                'forgetting_rate': 0.0
            }
        
        # Compute dissident score
        dissident_score = self._compute_dissident_score(
            spectral['smallest_eigenvalue'],
            pca_variance,
            delta_deficit,
            temporal['memory_persistence'],
            coherence_gradient
        )
        
        # Classify dissident type
        is_dissident = dissident_score > 0.5
        dissident_type = self._classify_dissident_type(
            dissident_score,
            temporal['temporal_stability'],
            delta_deficit
        )
        
        # Create signature
        signature = DissidentSignature(
            laplacian_eigenvalue=spectral['smallest_eigenvalue'],
            spectral_gap=spectral['spectral_gap'],
            pca_variance_ratio=pca_variance,
            coherence_gradient=coherence_gradient,
            memory_persistence=temporal['memory_persistence'],
            temporal_stability=temporal['temporal_stability'],
            delta_deficit=delta_deficit,
            net_refinements=int(avg_net_ref),
            is_dissident=is_dissident,
            dissident_score=dissident_score,
            dissident_type=dissident_type
        )
        
        # Generate recommendations
        recommendations = self._generate_recommendations(signature)
        
        # Generate intervention protocols
        interventions = self._generate_interventions(signature)
        
        # Estimate coherence gain
        expected_gain = self._estimate_coherence_gain(signature)
        
        # Confidence based on data quality
        confidence = self._compute_confidence(data_matrix, coherence_states)
        
        result = DissidentAnalysisResult(
            signature=signature,
            recommendations=recommendations,
            intervention_protocols=interventions,
            expected_coherence_gain=expected_gain,
            confidence=confidence
        )
        
        # Store in history
        self.analysis_history.append(result)
        
        return result
    
    def _compute_dissident_score(self, 
                                laplacian_ev: float,
                                pca_variance: float,
                                delta_deficit: float,