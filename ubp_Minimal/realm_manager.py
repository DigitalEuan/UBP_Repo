"""
Universal Binary Principle (UBP) - Realms Management System
Author: Euan Craig, New Zealand
Date: September 17, 2025

This module implements the Realms management system for handling different
UBP realms with their specific physics, GLR frameworks, and configurations.
"""

import math
import time
import json
from typing import Dict, List, Tuple, Optional, Any, Union
from dataclasses import dataclass, field, asdict
from enum import Enum
from pathlib import Path
import numpy as np

from ..core.offbit import OffBit, create_quantum_offbit, create_electromagnetic_offbit, create_cosmological_offbit
from ..core.bitfield import SparseBitfield, BitfieldConfig
from ..glr.glr_framework import GLRFramework, RealmType, GLRLevel
from ..tgic.tgic_system import TGICSystem, TGICGeometry


class RealmPhysics(Enum):
    """Types of realm physics."""
    QUANTUM = "quantum"
    ELECTROMAGNETIC = "electromagnetic"
    GRAVITATIONAL = "gravitational"
    BIOLOGICAL = "biological"
    COSMOLOGICAL = "cosmological"
    NUCLEAR = "nuclear"
    OPTICAL = "optical"


@dataclass
class RealmConfiguration:
    """Configuration for a UBP realm."""
    realm_id: str
    name: str
    physics_type: RealmPhysics
    
    # Core Resonance Values (CRV)
    crv: float
    frequency_hz: float
    wavelength_nm: float
    
    # Geometric properties
    geometry: TGICGeometry
    lattice_dimension: int
    coordination_number: int
    
    # GLR configuration
    primary_glr_level: GLRLevel
    secondary_glr_levels: List[GLRLevel] = field(default_factory=list)
    
    # Physical constants
    toggle_bias: float = 0.5  # Default toggle probability
    coherence_threshold: float = 0.95
    energy_scale: float = 1.0
    
    # Bitfield configuration
    bitfield_config: Optional[BitfieldConfig] = None
    
    # Temporal properties
    csc_period: float = 1.0 / math.pi  # Coherent Synchronization Cycle
    temporal_scaling: float = 1.0
    
    # Metadata
    description: str = ""
    references: List[str] = field(default_factory=list)
    active: bool = True
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        data = asdict(self)
        # Convert enums to strings
        data['physics_type'] = self.physics_type.value
        data['geometry'] = self.geometry.value
        data['primary_glr_level'] = self.primary_glr_level.value
        data['secondary_glr_levels'] = [level.value for level in self.secondary_glr_levels]
        return data
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'RealmConfiguration':
        """Create from dictionary."""
        # Convert string enums back to enum objects
        data['physics_type'] = RealmPhysics(data['physics_type'])
        data['geometry'] = TGICGeometry(data['geometry'])
        data['primary_glr_level'] = GLRLevel(data['primary_glr_level'])
        data['secondary_glr_levels'] = [GLRLevel(level) for level in data['secondary_glr_levels']]
        return cls(**data)


@dataclass
class RealmState:
    """Current state of a realm."""
    realm_id: str
    active_offbits: int = 0
    coherence_level: float = 0.0
    energy_level: float = 0.0
    last_update: float = field(default_factory=time.time)
    processing_cycles: int = 0
    error_count: int = 0
    correction_count: int = 0
    
    # Performance metrics
    nrci: float = 0.0  # Non-Random Coherence Index
    spatial_efficiency: float = 0.0
    temporal_efficiency: float = 0.0
    
    # Resonance information
    dominant_frequency: float = 0.0
    resonance_patterns: int = 0
    
    metadata: Dict[str, Any] = field(default_factory=dict)


class Realm:
    """
    Represents a single UBP realm with its configuration and state.
    """
    
    def __init__(self, config: RealmConfiguration):
        """
        Initialize realm with configuration.
        
        Args:
            config: Realm configuration
        """
        self.config = config
        self.state = RealmState(realm_id=config.realm_id)
        
        # Initialize realm-specific components
        self.bitfield = self._create_bitfield()
        self.glr_framework = self._create_glr_framework()
        self.tgic_system = self._create_tgic_system()
        
        # Processing history
        self.processing_history = []
        
        # Statistics
        self.stats = {
            'total_processing_time': 0.0,
            'total_operations': 0,
            'average_coherence': 0.0,
            'peak_energy': 0.0
        }
    
    def _create_bitfield(self) -> SparseBitfield:
        """Create bitfield with realm-specific configuration."""
        if self.config.bitfield_config:
            bitfield_config = self.config.bitfield_config
        else:
            # Create default configuration based on realm type
            if self.config.physics_type == RealmPhysics.QUANTUM:
                bitfield_config = BitfieldConfig(
                    dimensions=(100, 100, 100, 3, 2, 2),
                    max_offbits=100000,
                    sparsity_target=0.005
                )
            elif self.config.physics_type == RealmPhysics.ELECTROMAGNETIC:
                bitfield_config = BitfieldConfig(
                    dimensions=(170, 170, 170, 5, 2, 2),
                    max_offbits=1000000,
                    sparsity_target=0.01
                )
            else:
                # Default configuration
                bitfield_config = BitfieldConfig()
        
        from ..core.bitfield import SparseBitfield
        return SparseBitfield(bitfield_config)
    
    def _create_glr_framework(self) -> GLRFramework:
        """Create GLR framework for this realm."""
        from ..glr.glr_framework import GLRFramework
        return GLRFramework()
    
    def _create_tgic_system(self) -> TGICSystem:
        """Create TGIC system for this realm."""
        from ..tgic.tgic_system import TGICSystem
        return TGICSystem(self.config.geometry)
    
    def initialize_with_pattern(self, pattern_type: str = "random", 
                              density: float = 0.01) -> None:
        """
        Initialize realm with a specific pattern.
        
        Args:
            pattern_type: Type of pattern ("random", "harmonic", "spiral", "crystalline")
            density: Density of OffBits to create
        """
        num_offbits = int(self.bitfield.config.linear_size * density)
        
        if pattern_type == "random":
            self._initialize_random_pattern(num_offbits)
        elif pattern_type == "harmonic":
            self._initialize_harmonic_pattern(num_offbits)
        elif pattern_type == "spiral":
            self._initialize_spiral_pattern(num_offbits)
        elif pattern_type == "crystalline":
            self._initialize_crystalline_pattern(num_offbits)
        else:
            self._initialize_random_pattern(num_offbits)
        
        self._update_state()
    
    def _initialize_random_pattern(self, num_offbits: int):
        """Initialize with random OffBit placement."""
        dims = self.bitfield.config.dimensions
        
        for _ in range(num_offbits):
            coord = tuple(np.random.randint(0, dim) for dim in dims)
            offbit = self._create_realm_offbit()
            self.bitfield.set_offbit(coord, offbit)
    
    def _initialize_harmonic_pattern(self, num_offbits: int):
        """Initialize with harmonic wave pattern."""
        dims = self.bitfield.config.dimensions
        
        for i in range(num_offbits):
            # Create harmonic spatial distribution
            t = i / num_offbits * 4 * math.pi
            
            x = int(dims[0] * (0.5 + 0.3 * math.sin(t)))
            y = int(dims[1] * (0.5 + 0.3 * math.cos(t)))
            z = int(dims[2] * (0.5 + 0.2 * math.sin(2 * t)))
            w = min(dims[3] - 1, int(dims[3] * abs(math.sin(t))))
            v = min(dims[4] - 1, int(dims[4] * abs(math.cos(t))))
            u = min(dims[5] - 1, int(dims[5] * abs(math.sin(3 * t))))
            
            coord = (x, y, z, w, v, u)
            
            # Create OffBit with harmonic properties
            phase = t + self.config.crv
            reality = int(128 + 64 * math.sin(phase))
            info = int(128 + 64 * math.cos(phase))
            activation = int(128 + 32 * math.sin(2 * phase))
            
            offbit = self._create_realm_offbit(reality, info, activation)
            self.bitfield.set_offbit(coord, offbit)
    
    def _initialize_spiral_pattern(self, num_offbits: int):
        """Initialize with spiral pattern."""
        dims = self.bitfield.config.dimensions
        center = [d // 2 for d in dims[:3]]
        
        for i in range(num_offbits):
            t = i / num_offbits * 6 * math.pi
            r = (i / num_offbits) * min(dims[:3]) * 0.4
            
            x = int(center[0] + r * math.cos(t))
            y = int(center[1] + r * math.sin(t))
            z = int(center[2] + (i / num_offbits) * dims[2] * 0.8)
            
            # Ensure coordinates are within bounds
            x = max(0, min(dims[0] - 1, x))
            y = max(0, min(dims[1] - 1, y))
            z = max(0, min(dims[2] - 1, z))
            
            coord = (x, y, z, 1, 0, 1)
            offbit = self._create_realm_offbit()
            self.bitfield.set_offbit(coord, offbit)
    
    def _initialize_crystalline_pattern(self, num_offbits: int):
        """Initialize with crystalline lattice pattern."""
        dims = self.bitfield.config.dimensions
        
        # Create cubic lattice points
        lattice_spacing = max(1, int((dims[0] * dims[1] * dims[2] / num_offbits) ** (1/3)))
        
        count = 0
        for x in range(0, dims[0], lattice_spacing):
            for y in range(0, dims[1], lattice_spacing):
                for z in range(0, dims[2], lattice_spacing):
                    if count >= num_offbits:
                        break
                    
                    coord = (x, y, z, 1, 0, 1)
                    offbit = self._create_realm_offbit()
                    self.bitfield.set_offbit(coord, offbit)
                    count += 1
                
                if count >= num_offbits:
                    break
            if count >= num_offbits:
                break
    
    def _create_realm_offbit(self, reality: Optional[int] = None,
                           info: Optional[int] = None,
                           activation: Optional[int] = None) -> OffBit:
        """Create an OffBit appropriate for this realm."""
        if self.config.physics_type == RealmPhysics.QUANTUM:
            return create_quantum_offbit(reality, info, activation)
        elif self.config.physics_type == RealmPhysics.ELECTROMAGNETIC:
            return create_electromagnetic_offbit(reality, info, activation)
        elif self.config.physics_type == RealmPhysics.COSMOLOGICAL:
            return create_cosmological_offbit(reality, info, activation)
        else:
            # Default quantum OffBit
            return create_quantum_offbit(reality, info, activation)
    
    def process_cycle(self) -> RealmState:
        """
        Execute one processing cycle for this realm.
        
        Returns:
            Updated realm state
        """
        start_time = time.time()
        
        # Apply TGIC constraints
        tgic_results = self.tgic_system.apply_constraints(self.bitfield)
        
        # Apply GLR error correction
        glr_results = self.glr_framework.process_bitfield(
            self.bitfield, 
            RealmType(self.config.physics_type.value)
        )
        
        # Update state based on processing results
        self._update_state()
        
        # Record processing cycle
        cycle_time = time.time() - start_time
        self.state.processing_cycles += 1
        self.state.last_update = time.time()
        
        # Update statistics
        self.stats['total_processing_time'] += cycle_time
        self.stats['total_operations'] += 1
        
        # Record history
        self.processing_history.append({
            'cycle': self.state.processing_cycles,
            'timestamp': self.state.last_update,
            'processing_time': cycle_time,
            'tgic_results': tgic_results,
            'glr_results': {str(k): v.__dict__ for k, v in glr_results.items()},
            'state_snapshot': asdict(self.state)
        })
        
        # Keep only recent history
        if len(self.processing_history) > 100:
            self.processing_history = self.processing_history[-100:]
        
        return self.state
    
    def _update_state(self):
        """Update realm state based on current bitfield."""
        self.state.active_offbits = self.bitfield.active_count
        self.state.coherence_level = self.bitfield.get_coherence()
        
        # Calculate energy level
        active_offbits = self.bitfield.get_active_offbits()
        total_energy = sum(offbit.active_bits for _, offbit in active_offbits)
        self.state.energy_level = total_energy * self.config.energy_scale
        
        # Update peak energy
        if self.state.energy_level > self.stats['peak_energy']:
            self.stats['peak_energy'] = self.state.energy_level
        
        # Calculate NRCI (simplified - would need target bitfield for full calculation)
        self.state.nrci = self.state.coherence_level
        
        # Update average coherence
        if self.stats['total_operations'] > 0:
            self.stats['average_coherence'] = (
                (self.stats['average_coherence'] * (self.stats['total_operations'] - 1) + 
                 self.state.coherence_level) / self.stats['total_operations']
            )
        else:
            self.stats['average_coherence'] = self.state.coherence_level
    
    def get_realm_info(self) -> Dict[str, Any]:
        """Get comprehensive realm information."""
        return {
            'config': self.config.to_dict(),
            'state': asdict(self.state),
            'statistics': self.stats.copy(),
            'bitfield_info': {
                'dimensions': self.bitfield.config.dimensions,
                'active_count': self.bitfield.active_count,
                'sparsity': self.bitfield.current_sparsity,
                'memory_usage': self.bitfield.memory_usage
            },
            'recent_history': self.processing_history[-5:] if self.processing_history else []
        }


class RealmManager:
    """
    Manager for multiple UBP realms with switching and coordination.
    """
    
    def __init__(self):
        """Initialize the realm manager."""
        self.realms = {}
        self.active_realm_id = None
        self.realm_configs = {}
        
        # Cross-realm coordination
        self.coordination_enabled = True
        self.synchronization_period = 1.0 / math.pi  # CSC period
        
        # Initialize default realm configurations
        self._initialize_default_realms()
        
        # Statistics
        self.global_stats = {
            'total_realms': 0,
            'active_realms': 0,
            'total_processing_cycles': 0,
            'cross_realm_coherence': 0.0
        }
    
    def _initialize_default_realms(self):
        """Initialize default realm configurations."""
        
        # Quantum Realm
        quantum_config = RealmConfiguration(
            realm_id="quantum",
            name="Quantum Realm",
            physics_type=RealmPhysics.QUANTUM,
            crv=math.e / 12,  # ≈ 0.2265234857
            frequency_hz=4.58e14,
            wavelength_nm=655.0,
            geometry=TGICGeometry.TETRAHEDRAL,
            lattice_dimension=4,
            coordination_number=4,
            primary_glr_level=GLRLevel.LEVEL_5_TETRAHEDRAL,
            secondary_glr_levels=[GLRLevel.LEVEL_1_HAMMING, GLRLevel.LEVEL_3_GOLAY],
            toggle_bias=math.e / 12,
            coherence_threshold=0.875,
            description="Quantum realm with tetrahedral GLR and e/12 resonance"
        )
        
        # Electromagnetic Realm
        em_config = RealmConfiguration(
            realm_id="electromagnetic",
            name="Electromagnetic Realm",
            physics_type=RealmPhysics.ELECTROMAGNETIC,
            crv=math.pi,
            frequency_hz=3.141593,
            wavelength_nm=635.0,
            geometry=TGICGeometry.CUBIC,
            lattice_dimension=3,
            coordination_number=6,
            primary_glr_level=GLRLevel.LEVEL_4_CUBIC,
            secondary_glr_levels=[GLRLevel.LEVEL_1_HAMMING, GLRLevel.LEVEL_3_GOLAY],
            toggle_bias=0.5,
            coherence_threshold=1.0,
            description="Electromagnetic realm with cubic GLR and π-resonance"
        )
        
        # Gravitational Realm
        grav_config = RealmConfiguration(
            realm_id="gravitational",
            name="Gravitational Realm",
            physics_type=RealmPhysics.GRAVITATIONAL,
            crv=1.0,
            frequency_hz=100.0,
            wavelength_nm=1000.0,
            geometry=TGICGeometry.OCTAHEDRAL,
            lattice_dimension=3,
            coordination_number=12,
            primary_glr_level=GLRLevel.LEVEL_6_FCC,
            secondary_glr_levels=[GLRLevel.LEVEL_1_HAMMING, GLRLevel.LEVEL_3_GOLAY],
            toggle_bias=0.3,
            coherence_threshold=0.915,
            description="Gravitational realm with FCC GLR and 100 Hz resonance"
        )
        
        # Cosmological Realm
        cosmic_config = RealmConfiguration(
            realm_id="cosmological",
            name="Cosmological Realm",
            physics_type=RealmPhysics.COSMOLOGICAL,
            crv=math.pi ** (1 / ((1 + math.sqrt(5)) / 2)),  # π^φ ≈ 0.83203682
            frequency_hz=1e-11,
            wavelength_nm=800.0,
            geometry=TGICGeometry.ICOSAHEDRAL,
            lattice_dimension=3,
            coordination_number=12,
            primary_glr_level=GLRLevel.LEVEL_8_ICOSAHEDRAL,
            secondary_glr_levels=[GLRLevel.LEVEL_1_HAMMING, GLRLevel.LEVEL_3_GOLAY],
            toggle_bias=math.pi ** (1 / ((1 + math.sqrt(5)) / 2)),
            coherence_threshold=0.797,
            description="Cosmological realm with icosahedral GLR and π^φ resonance"
        )
        
        # Store configurations
        self.realm_configs = {
            "quantum": quantum_config,
            "electromagnetic": em_config,
            "gravitational": grav_config,
            "cosmological": cosmic_config
        }
    
    def create_realm(self, config: RealmConfiguration) -> Realm:
        """
        Create a new realm with the given configuration.
        
        Args:
            config: Realm configuration
        
        Returns:
            Created realm
        """
        realm = Realm(config)
        self.realms[config.realm_id] = realm
        self.realm_configs[config.realm_id] = config
        
        # Set as active if it's the first realm
        if self.active_realm_id is None:
            self.active_realm_id = config.realm_id
        
        self.global_stats['total_realms'] += 1
        if config.active:
            self.global_stats['active_realms'] += 1
        
        return realm
    
    def get_realm(self, realm_id: str) -> Optional[Realm]:
        """Get realm by ID."""
        return self.realms.get(realm_id)
    
    def switch_realm(self, realm_id: str) -> bool:
        """
        Switch to a different active realm.
        
        Args:
            realm_id: ID of realm to switch to
        
        Returns:
            True if switch successful, False otherwise
        """
        if realm_id in self.realms and self.realm_configs[realm_id].active:
            self.active_realm_id = realm_id
            return True
        return False
    
    def get_active_realm(self) -> Optional[Realm]:
        """Get the currently active realm."""
        if self.active_realm_id:
            return self.realms.get(self.active_realm_id)
        return None
    
    def initialize_all_realms(self, pattern_type: str = "harmonic", 
                            density: float = 0.01):
        """Initialize all realms with patterns."""
        for realm in self.realms.values():
            if realm.config.active:
                realm.initialize_with_pattern(pattern_type, density)
    
    def process_all_realms(self) -> Dict[str, RealmState]:
        """
        Process all active realms for one cycle.
        
        Returns:
            Dictionary of realm states
        """
        results = {}
        
        for realm_id, realm in self.realms.items():
            if realm.config.active:
                state = realm.process_cycle()
                results[realm_id] = state
                self.global_stats['total_processing_cycles'] += 1
        
        # Calculate cross-realm coherence if coordination is enabled
        if self.coordination_enabled and len(results) > 1:
            self._calculate_cross_realm_coherence()
        
        return results
    
    def _calculate_cross_realm_coherence(self):
        """Calculate coherence across all active realms."""
        active_realms = [r for r in self.realms.values() if r.config.active]
        
        if len(active_realms) < 2:
            self.global_stats['cross_realm_coherence'] = 1.0
            return
        
        coherence_sum = 0.0
        pair_count = 0
        
        for i, realm1 in enumerate(active_realms):
            for realm2 in active_realms[i+1:]:
                # Calculate coherence between realm bitfields
                coherence = realm1.bitfield.compute_nrci(realm2.bitfield)
                coherence_sum += coherence
                pair_count += 1
        
        self.global_stats['cross_realm_coherence'] = coherence_sum / max(1, pair_count)
    
    def get_realm_list(self) -> List[Dict[str, Any]]:
        """Get list of all realms with basic info."""
        realm_list = []
        
        for realm_id, config in self.realm_configs.items():
            realm = self.realms.get(realm_id)
            
            info = {
                'realm_id': realm_id,
                'name': config.name,
                'physics_type': config.physics_type.value,
                'active': config.active,
                'is_current_active': realm_id == self.active_realm_id
            }
            
            if realm:
                info.update({
                    'state': asdict(realm.state),
                    'processing_cycles': realm.state.processing_cycles,
                    'coherence': realm.state.coherence_level
                })
            
            realm_list.append(info)
        
        return realm_list
    
    def get_manager_statistics(self) -> Dict[str, Any]:
        """Get comprehensive manager statistics."""
        return {
            'global_stats': self.global_stats.copy(),
            'active_realm': self.active_realm_id,
            'realm_count': len(self.realms),
            'coordination_enabled': self.coordination_enabled,
            'realm_summary': {
                realm_id: {
                    'active_offbits': realm.state.active_offbits,
                    'coherence': realm.state.coherence_level,
                    'energy': realm.state.energy_level,
                    'cycles': realm.state.processing_cycles
                }
                for realm_id, realm in self.realms.items()
            }
        }
    
    def save_configuration(self, filepath: str):
        """Save realm configurations to file."""
        config_data = {
            'realm_configs': {
                realm_id: config.to_dict() 
                for realm_id, config in self.realm_configs.items()
            },
            'active_realm': self.active_realm_id,
            'coordination_enabled': self.coordination_enabled,
            'global_stats': self.global_stats
        }
        
        with open(filepath, 'w') as f:
            json.dump(config_data, f, indent=2, default=str)
    
    def load_configuration(self, filepath: str):
        """Load realm configurations from file."""
        with open(filepath, 'r') as f:
            config_data = json.load(f)
        
        # Load realm configurations
        for realm_id, config_dict in config_data['realm_configs'].items():
            config = RealmConfiguration.from_dict(config_dict)
            self.realm_configs[realm_id] = config
            
            # Create realm if it doesn't exist
            if realm_id not in self.realms:
                self.create_realm(config)
        
        # Restore other settings
        self.active_realm_id = config_data.get('active_realm')
        self.coordination_enabled = config_data.get('coordination_enabled', True)
        self.global_stats.update(config_data.get('global_stats', {}))


# Factory function
def create_realm_manager() -> RealmManager:
    """Create a realm manager with default realms."""
    manager = RealmManager()
    
    # Create default realms
    for realm_id, config in manager.realm_configs.items():
        manager.create_realm(config)
    
    return manager


if __name__ == "__main__":
    # Test the realm management system
    print("Testing Realm Management System...")
    
    # Create realm manager
    manager = create_realm_manager()
    print(f"Created realm manager with {len(manager.realms)} realms")
    
    # Show realm list
    realm_list = manager.get_realm_list()
    print(f"\nAvailable realms:")
    for realm_info in realm_list:
        print(f"  {realm_info['realm_id']}: {realm_info['name']} ({realm_info['physics_type']})")
        print(f"    Active: {realm_info['active']}, Current: {realm_info['is_current_active']}")
    
    # Initialize realms with patterns
    print(f"\nInitializing realms with harmonic patterns...")
    manager.initialize_all_realms("harmonic", density=0.005)
    
    # Process several cycles
    print(f"\nProcessing 3 cycles across all realms...")
    for cycle in range(3):
        results = manager.process_all_realms()
        print(f"  Cycle {cycle + 1}: Processed {len(results)} realms")
        
        for realm_id, state in results.items():
            print(f"    {realm_id}: {state.active_offbits} OffBits, coherence {state.coherence_level:.3f}")
    
    # Switch active realm
    print(f"\nSwitching to quantum realm...")
    success = manager.switch_realm("quantum")
    print(f"Switch successful: {success}")
    
    active_realm = manager.get_active_realm()
    if active_realm:
        print(f"Active realm: {active_realm.config.name}")
        print(f"  CRV: {active_realm.config.crv:.6f}")
        print(f"  Frequency: {active_realm.config.frequency_hz:.2e} Hz")
        print(f"  Coherence: {active_realm.state.coherence_level:.3f}")
    
    # Show manager statistics
    stats = manager.get_manager_statistics()
    print(f"\nRealm Manager Statistics:")
    print(f"  Total realms: {stats['global_stats']['total_realms']}")
    print(f"  Active realms: {stats['global_stats']['active_realms']}")
    print(f"  Total processing cycles: {stats['global_stats']['total_processing_cycles']}")
    print(f"  Cross-realm coherence: {stats['global_stats']['cross_realm_coherence']:.3f}")
    
    print("\nRealm Management System test completed successfully!")

