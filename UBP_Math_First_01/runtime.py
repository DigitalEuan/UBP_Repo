"""
UBP Virtual Machine Runtime

The runtime orchestrates UBP semantic functions and manages system state.
It provides a high-level interface for executing UBP operations and simulations.
"""

import time
import json
from typing import Dict, List, Tuple, Optional, Any, Union
from dataclasses import dataclass, asdict

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ubp_semantics import (
    OffBit, Bitfield, load_constants, get_realm_constants,
    energy, nrci, coherence, global_coherence_invariant,
    toggle_and, toggle_xor, toggle_or, resonance_toggle,
    entanglement_toggle, superposition_toggle, hybrid_xor_resonance,
    spin_transition, apply_tgic_constraint,
    coherence_pressure_spatial, coherence_pressure_temporal,
    fractal_dimension, calculate_system_coherence_score
)


@dataclass
class SimulationState:
    """Represents the current state of a UBP simulation."""
    time_step: int = 0
    global_time: float = 0.0
    active_realm: str = "quantum"
    energy_value: float = 0.0
    nrci_value: float = 0.0
    coherence_pressure: float = 0.0
    total_toggles: int = 0
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return asdict(self)


@dataclass
class SimulationResult:
    """Results from a UBP simulation run."""
    initial_state: SimulationState
    final_state: SimulationState
    metrics: Dict[str, float]
    timeline: List[SimulationState]
    execution_time: float
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            'initial_state': self.initial_state.to_dict(),
            'final_state': self.final_state.to_dict(),
            'metrics': self.metrics,
            'timeline': [state.to_dict() for state in self.timeline],
            'execution_time': self.execution_time
        }


class Runtime:
    """
    UBP Virtual Machine Runtime
    
    Manages the execution environment for UBP simulations and operations.
    """
    
    def __init__(self, hardware_profile: str = "desktop_8gb"):
        """
        Initialize the UBP runtime.
        
        Args:
            hardware_profile: Hardware configuration to use
        """
        self.hardware_profile = hardware_profile
        self.constants = load_constants()
        
        # Initialize Bitfield
        self.bitfield = Bitfield(hardware_profile)
        
        # Runtime state
        self.state = SimulationState()
        self.timeline: List[SimulationState] = []
        
        # Performance tracking
        self.operation_count = 0
        self.start_time = 0.0
        
        # Realm configurations
        self.realm_configs = {}
        self._load_realm_configs()
    
    def _load_realm_configs(self):
        """Load realm-specific configurations."""
        realm_names = ["quantum", "electromagnetic", "gravitational", 
                      "biological", "cosmological", "nuclear", "optical"]
        
        for realm_name in realm_names:
            try:
                self.realm_configs[realm_name] = get_realm_constants(realm_name)
            except KeyError:
                # Realm not found in constants, skip
                continue
    
    def set_realm(self, realm_name: str):
        """
        Set the active realm for operations.
        
        Args:
            realm_name: Name of the realm to activate
        """
        if realm_name not in self.realm_configs:
            available = list(self.realm_configs.keys())
            raise ValueError(f"Unknown realm '{realm_name}'. Available: {available}")
        
        self.state.active_realm = realm_name
    
    def get_realm_config(self, realm_name: str = None) -> Dict[str, Any]:
        """
        Get configuration for a realm.
        
        Args:
            realm_name: Realm name (uses active realm if None)
            
        Returns:
            Realm configuration dictionary
        """
        if realm_name is None:
            realm_name = self.state.active_realm
        
        return self.realm_configs.get(realm_name, {})
    
    def initialize_bitfield(self, pattern: str = "sparse_random", 
                           density: float = 0.01, seed: int = None):
        """
        Initialize the Bitfield with a specific pattern.
        
        Args:
            pattern: Initialization pattern ("sparse_random", "quantum_bias", etc.)
            density: Density of active OffBits
            seed: Random seed for reproducibility
        """
        import random
        if seed is not None:
            random.seed(seed)
        
        self.bitfield.clear()
        
        if pattern == "sparse_random":
            self._init_sparse_random(density)
        elif pattern == "quantum_bias":
            self._init_quantum_bias(density)
        elif pattern == "realm_specific":
            self._init_realm_specific(density)
        else:
            raise ValueError(f"Unknown initialization pattern: {pattern}")
        
        self.bitfield.reset_statistics()
    
    def _init_sparse_random(self, density: float):
        """Initialize with sparse random pattern."""
        import random
        
        target_count = int(self.bitfield.total_cells * density)
        target_count = min(target_count, self.bitfield.max_offbits)
        
        for _ in range(target_count):
            coord = tuple(random.randint(0, dim-1) for dim in self.bitfield.dimensions)
            value = random.randint(1, 0xFFFFFF)  # Non-zero 24-bit value
            offbit = OffBit(value)
            self.bitfield.set_offbit(coord, offbit)
    
    def _init_quantum_bias(self, density: float):
        """Initialize with quantum realm bias."""
        import random
        from ..ubp_semantics.constants import EULER_E
        
        target_count = int(self.bitfield.total_cells * density)
        target_count = min(target_count, self.bitfield.max_offbits)
        
        quantum_bias = EULER_E / 12  # e/12 ≈ 0.2265234857
        
        for _ in range(target_count):
            coord = tuple(random.randint(0, dim-1) for dim in self.bitfield.dimensions)
            
            # Bias toward quantum-like values
            if random.random() < quantum_bias:
                value = random.randint(0x100000, 0xFFFFFF)  # Higher values
            else:
                value = random.randint(1, 0x0FFFFF)  # Lower values
            
            offbit = OffBit(value)
            self.bitfield.set_offbit(coord, offbit)
    
    def _init_realm_specific(self, density: float):
        """Initialize with active realm-specific pattern."""
        realm_config = self.get_realm_config()
        
        if "toggle_bias" in realm_config:
            bias = realm_config["toggle_bias"]
            self._init_with_bias(density, bias)
        else:
            self._init_sparse_random(density)
    
    def _init_with_bias(self, density: float, bias: float):
        """Initialize with specific toggle bias."""
        import random
        
        target_count = int(self.bitfield.total_cells * density)
        target_count = min(target_count, self.bitfield.max_offbits)
        
        for _ in range(target_count):
            coord = tuple(random.randint(0, dim-1) for dim in self.bitfield.dimensions)
            
            # Apply bias to value generation
            if random.random() < bias:
                value = random.randint(0x800000, 0xFFFFFF)  # Upper half
            else:
                value = random.randint(1, 0x7FFFFF)  # Lower half
            
            offbit = OffBit(value)
            self.bitfield.set_offbit(coord, offbit)
    
    def execute_toggle_operation(self, operation: str, coord1: Tuple[int, ...], 
                                coord2: Tuple[int, ...] = None, **kwargs) -> OffBit:
        """
        Execute a toggle operation between OffBits.
        
        Args:
            operation: Operation name ("and", "xor", "or", "resonance", etc.)
            coord1: First OffBit coordinate
            coord2: Second OffBit coordinate (if needed)
            **kwargs: Additional operation parameters
            
        Returns:
            Result OffBit
        """
        offbit1 = self.bitfield.get_offbit(coord1)
        
        if coord2 is not None:
            offbit2 = self.bitfield.get_offbit(coord2)
        else:
            offbit2 = OffBit(0)
        
        # Execute operation based on type
        if operation == "and":
            result = toggle_and(offbit1, offbit2)
        elif operation == "xor":
            result = toggle_xor(offbit1, offbit2)
        elif operation == "or":
            result = toggle_or(offbit1, offbit2)
        elif operation == "resonance":
            frequency = kwargs.get('frequency', 1.0)
            time_param = kwargs.get('time', self.state.global_time)
            result = resonance_toggle(offbit1, frequency, time_param)
        elif operation == "entanglement":
            coherence_val = kwargs.get('coherence', 0.95)
            result = entanglement_toggle(offbit1, offbit2, coherence_val)
        elif operation == "superposition":
            weights = kwargs.get('weights', [0.5, 0.5])
            result = superposition_toggle([offbit1, offbit2], weights)
        elif operation == "hybrid_xor_resonance":
            distance = kwargs.get('distance', 1.0)
            result = hybrid_xor_resonance(offbit1, offbit2, distance)
        elif operation == "spin_transition":
            p_s = kwargs.get('p_s', 0.2265234857)  # Default quantum
            result = spin_transition(offbit1, p_s)
        elif operation == "tgic":
            x_state = kwargs.get('x_state', True)
            y_state = kwargs.get('y_state', True)
            z_state = kwargs.get('z_state', False)
            result = apply_tgic_constraint(x_state, y_state, z_state, 
                                         offbit1, offbit2, **kwargs)
        else:
            raise ValueError(f"Unknown operation: {operation}")
        
        # Update statistics
        self.operation_count += 1
        self.state.total_toggles += 1
        
        return result
    
    def run_simulation(self, steps: int, operations_per_step: int = 10,
                      target_coords: List[Tuple[int, ...]] = None,
                      record_timeline: bool = True) -> SimulationResult:
        """
        Run a UBP simulation for specified steps.
        
        Args:
            steps: Number of simulation steps
            operations_per_step: Toggle operations per step
            target_coords: Specific coordinates to operate on (random if None)
            record_timeline: Whether to record state timeline
            
        Returns:
            SimulationResult with metrics and timeline
        """
        start_time = time.time()
        self.start_time = start_time
        
        # Record initial state
        initial_state = SimulationState(
            time_step=0,
            global_time=0.0,
            active_realm=self.state.active_realm,
            energy_value=self._calculate_current_energy(),
            nrci_value=0.0,  # Will be calculated during simulation
            coherence_pressure=0.0,
            total_toggles=0
        )
        
        timeline = [initial_state] if record_timeline else []
        
        # Run simulation steps
        for step in range(steps):
            self._execute_simulation_step(operations_per_step, target_coords)
            
            # Update state
            self.state.time_step = step + 1
            self.state.global_time = (step + 1) * self.constants["system_constants"]["bit_time"]
            self.state.energy_value = self._calculate_current_energy()
            
            # Record timeline if requested
            if record_timeline:
                current_state = SimulationState(
                    time_step=self.state.time_step,
                    global_time=self.state.global_time,
                    active_realm=self.state.active_realm,
                    energy_value=self.state.energy_value,
                    nrci_value=self.state.nrci_value,
                    coherence_pressure=self.state.coherence_pressure,
                    total_toggles=self.state.total_toggles
                )
                timeline.append(current_state)
        
        # Calculate final metrics
        final_metrics = self._calculate_final_metrics()
        execution_time = time.time() - start_time
        
        # Create result
        result = SimulationResult(
            initial_state=initial_state,
            final_state=self.state,
            metrics=final_metrics,
            timeline=timeline,
            execution_time=execution_time
        )
        
        return result
    
    def _execute_simulation_step(self, operations_per_step: int, 
                                target_coords: List[Tuple[int, ...]] = None):
        """Execute a single simulation step."""
        import random
        
        active_offbits = self.bitfield.get_active_offbits()
        if not active_offbits:
            return  # No active OffBits to operate on
        
        coords_list = list(active_offbits.keys())
        
        for _ in range(operations_per_step):
            if target_coords:
                coord1 = random.choice(target_coords)
                coord2 = random.choice(target_coords) if len(target_coords) > 1 else None
            else:
                coord1 = random.choice(coords_list)
                coord2 = random.choice(coords_list) if len(coords_list) > 1 else None
            
            # Choose operation based on realm
            operation = self._choose_realm_operation()
            
            try:
                result = self.execute_toggle_operation(operation, coord1, coord2)
                # Store result back to first coordinate
                self.bitfield.set_offbit(coord1, result)
            except Exception as e:
                # Skip failed operations
                continue
    
    def _choose_realm_operation(self) -> str:
        """Choose an operation based on the active realm."""
        import random
        
        realm_operations = {
            "quantum": ["resonance", "spin_transition", "tgic"],
            "electromagnetic": ["and", "or", "resonance"],
            "gravitational": ["entanglement", "superposition"],
            "biological": ["hybrid_xor_resonance", "superposition"],
            "cosmological": ["spin_transition", "entanglement"],
            "nuclear": ["resonance", "tgic"],
            "optical": ["and", "xor", "resonance"]
        }
        
        operations = realm_operations.get(self.state.active_realm, ["xor", "and", "or"])
        return random.choice(operations)
    
    def _calculate_current_energy(self) -> float:
        """Calculate current system energy."""
        active_count = self.bitfield.active_count
        if active_count == 0:
            return 0.0
        
        return energy(M=active_count)
    
    def _calculate_final_metrics(self) -> Dict[str, float]:
        """Calculate final simulation metrics."""
        # Generate synthetic target data for NRCI calculation
        active_offbits = self.bitfield.get_active_offbits()
        if not active_offbits:
            return {"nrci": 0.0, "coherence_score": 0.0}
        
        # Extract values for NRCI calculation
        simulated_values = [float(offbit.value) for offbit in active_offbits.values()]
        
        # Create synthetic target (for demonstration)
        import random
        target_values = [val + random.gauss(0, val * 0.01) for val in simulated_values]
        
        # Calculate NRCI
        nrci_value = nrci(simulated_values, target_values)
        self.state.nrci_value = nrci_value
        
        # Calculate coherence pressure
        distances = [1.0] * len(active_offbits)  # Simplified
        max_distances = [10.0] * len(active_offbits)  # Simplified
        active_bits = [offbit.information_layer for offbit in active_offbits.values()]
        
        coherence_pressure = coherence_pressure_spatial(distances, max_distances, active_bits)
        self.state.coherence_pressure = coherence_pressure
        
        # Calculate fractal dimension
        fractal_dim = fractal_dimension(len(active_offbits))
        
        # Calculate overall coherence score
        coherence_score = calculate_system_coherence_score(
            nrci=nrci_value,
            coherence_pressure=coherence_pressure,
            fractal_dim=fractal_dim,
            sri=0.8,  # Simplified
            cri=0.9   # Simplified
        )
        
        return {
            "nrci": nrci_value,
            "coherence_pressure": coherence_pressure,
            "fractal_dimension": fractal_dim,
            "coherence_score": coherence_score,
            "active_offbits": len(active_offbits),
            "total_offbits": self.bitfield.total_offbits,
            "sparsity": self.bitfield.current_sparsity,
            "energy": self.state.energy_value
        }
    
    def export_state(self, filepath: str, format: str = "json"):
        """
        Export current runtime state to file.
        
        Args:
            filepath: Output file path
            format: Export format ("json", "yaml")
        """
        state_data = {
            "runtime_state": self.state.to_dict(),
            "bitfield_stats": {
                "dimensions": self.bitfield.dimensions,
                "active_count": self.bitfield.active_count,
                "total_offbits": self.bitfield.total_offbits,
                "sparsity": self.bitfield.current_sparsity,
                "toggle_count": self.bitfield.toggle_count
            },
            "realm_configs": self.realm_configs,
            "operation_count": self.operation_count
        }
        
        if format == "json":
            with open(filepath, 'w') as f:
                json.dump(state_data, f, indent=2)
        elif format == "yaml":
            import yaml
            with open(filepath, 'w') as f:
                yaml.dump(state_data, f, default_flow_style=False)
        else:
            raise ValueError(f"Unsupported format: {format}")
    
    def reset(self):
        """Reset the runtime to initial state."""
        self.bitfield.clear()
        self.state = SimulationState()
        self.timeline.clear()
        self.operation_count = 0
        self.start_time = 0.0
    
    def get_performance_stats(self) -> Dict[str, float]:
        """Get runtime performance statistics."""
        elapsed_time = time.time() - self.start_time if self.start_time > 0 else 0.0
        
        return {
            "elapsed_time": elapsed_time,
            "operations_per_second": self.operation_count / elapsed_time if elapsed_time > 0 else 0.0,
            "total_operations": self.operation_count,
            "memory_efficiency": self.bitfield.current_sparsity,
            "active_offbits": self.bitfield.active_count
        }

