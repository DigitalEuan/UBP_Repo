            
            # Convert to log_nrci_error
            nrci = NRCI_TARGET * (1.0 - degradation)
            log_error = math.log(1.0 - nrci) if nrci < 1.0 else -1e10
            
            state = CoherenceState(value, log_nrci_error=log_error)
            states.append(state)
        
        return states
    
    def analyze_with_coherence_field(self) -> Optional[Dict[str, Any]]:
        """
        Analyze resonance history using Coherence Field ELITE.
        
        This is a convenience method that automatically converts history
        to CoherenceState sequence and runs resonance detection.
        
        Returns:
            Dictionary with analysis results, or None if Coherence Field unavailable
            
        Example:
            >>> b = OffBit(0x123456)
            >>> # ... apply resonance toggles ...
            >>> analysis = b.analyze_with_coherence_field()
            >>> if analysis and analysis.get('resonance'):
            ...     res = analysis['resonance']
            ...     print(f"Detected {res.p}/{res.q} resonance")
        """
        if not self.resonance_history:
            return {'error': 'No resonance history'}
        
        try:
            import coherence_field as cf
            
            # Convert to states
            states = self.to_coherence_states()
            
            # Detect resonance
            detector = cf.ResonanceDetector()
            resonance = detector.detect_resonance(states)
            
            # Get statistics
            stats = self.get_resonance_statistics()
            
            # Build result
            result = {
                'resonance': resonance,
                'history_length': stats['history_length'],
                'time_range': stats['time_range'],
                'frequency_range': stats['frequency_range'],
                'avg_resonance_factor': stats['avg_resonance_factor'],
                'min_resonance_factor': stats['min_resonance_factor'],
                'max_resonance_factor': stats['max_resonance_factor'],
                'coherence_states': states
            }
            
            # Add resonance details if detected
            if resonance:
                result['resonance_detected'] = True
                result['resonance_p'] = resonance.p
                result['resonance_q'] = resonance.q
                result['resonance_confidence'] = resonance.confidence
            else:
                result['resonance_detected'] = False
            
            return result
            
        except ImportError:
            return None
    
    def toggle(self) -> 'OffBit':
        """
        Create a new OffBit with toggled state.
        
        Toggling is a coherence transformation - it applies Y-refinement.
        Preserves resonance history.
        
        Returns:
            New OffBit with inverted bits and refined coherence
        """
        new_value = self.value ^ 0xFFFFFF
        new_coherence = self.coherence.refine_forward()
        return OffBit(new_value, new_coherence, self.resonance_history)
    
    def toggle_bit(self, position: int) -> 'OffBit':
        """
        Create a new OffBit with a specific bit toggled.
        
        Args:
            position: Bit position to toggle (0-23)
        
        Returns:
            New OffBit with specified bit toggled
        """
        if not (0 <= position < 24):
            raise ValueError(f"Bit position {position} out of range [0, 23]")
        
        new_value = self.value ^ (1 << position)
        # Small toggle = small coherence change
        new_coherence = self.coherence.degrade_by(1e-8)
        return OffBit(new_value, new_coherence, self.resonance_history)
    
    def get_bit(self, position: int) -> int:
        """
        Get the value of a specific bit.
        
        Args:
            position: Bit position (0-23)
        
        Returns:
            Bit value (0 or 1)
        """
        if not (0 <= position < 24):
            raise ValueError(f"Bit position {position} out of range [0, 23]")
        
        return (self.value >> position) & 1
    
    def set_bit(self, position: int, bit_value: int) -> 'OffBit':
        """
        Create a new OffBit with a specific bit set.
        
        Args:
            position: Bit position (0-23)
            bit_value: Bit value (0 or 1)
        
        Returns:
            New OffBit with specified bit set
        """
        if not (0 <= position < 24):
            raise ValueError(f"Bit position {position} out of range [0, 23]")