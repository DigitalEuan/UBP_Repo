# UBP-Core API Documentation

Complete API reference for the Universal Binary Principle implementation.

## Table of Contents

1. [Core Classes](#core-classes)
2. [Semantic Functions](#semantic-functions)
3. [Runtime System](#runtime-system)
4. [DSL Interface](#dsl-interface)
5. [Constants and Configuration](#constants-and-configuration)
6. [Examples](#examples)

## Core Classes

### OffBit

24-bit fundamental unit with 4 ontological layers.

```python
from ubp_semantics import OffBit

# Constructor
OffBit(value: int = 0)
```

#### Properties

- `value: int` - Complete 24-bit value
- `reality_layer: int` - Observable properties (bits 0-5)
- `information_layer: int` - Data processing (bits 6-11)
- `activation_layer: int` - Dynamic states (bits 12-17)
- `unactivated_layer: int` - Potential states (bits 18-23)
- `toggle_state: bool` - Toggle state (bit 12 of activation layer)

#### Methods

```python
# Layer manipulation
set_layer_bits(layer_name: str, bits: List[int])
get_layer_bits(layer_name: str) -> List[int]

# String representation
__str__() -> str
__repr__() -> str
```

#### Example

```python
offbit = OffBit(0x123456)
offbit.reality_layer = 42
offbit.toggle_state = True
print(f"OffBit value: {offbit.value:06x}")
```

### Bitfield

6D sparse array for OffBit storage.

```python
from ubp_semantics import Bitfield

# Constructor
Bitfield(hardware_profile: str = "desktop_8gb")
```

#### Properties

- `dimensions: Tuple[int, ...]` - 6D dimensions (170,170,170,5,2,2)
- `total_cells: int` - Total possible cells (~2.3M)
- `active_count: int` - Number of active OffBits
- `total_offbits: int` - Total stored OffBits
- `current_sparsity: float` - Current sparsity ratio
- `max_offbits: int` - Maximum OffBits for hardware profile

#### Methods

```python
# OffBit operations
set_offbit(coord: Tuple[int, ...], offbit: OffBit)
get_offbit(coord: Tuple[int, ...]) -> OffBit
remove_offbit(coord: Tuple[int, ...])

# Validation
is_valid_coordinate(coord: Tuple[int, ...]) -> bool

# Neighbors
get_neighbors(coord: Tuple[int, ...], radius: int = 1) -> List[Tuple[Tuple[int, ...], OffBit]]

# State management
get_active_offbits() -> Dict[Tuple[int, ...], OffBit]
clear()
reset_statistics()
```

#### Example

```python
bitfield = Bitfield("desktop_8gb")
coord = (10, 20, 30, 1, 0, 1)
bitfield.set_offbit(coord, OffBit(12345))
retrieved = bitfield.get_offbit(coord)
```

## Semantic Functions

### Energy Calculation

```python
from ubp_semantics import energy

energy(M: int = 1000, 
       C: float = 299792458, 
       R: float = None, 
       S_opt: float = None, 
       P_GCI: float = None, 
       O_observer: float = 1.0, 
       c_infinity: float = None, 
       I_spin: float = 1.0, 
       w_sum: float = 0.1) -> float
```

Complete UBP energy equation implementation.

#### Parameters

- `M`: Active OffBits count
- `C`: Speed of light (299,792,458 m/s)
- `R`: Resonance strength (default: 0.965885)
- `S_opt`: Structural optimality (default: 0.98)
- `P_GCI`: Global Coherence Invariant (default: 0.827046)
- `O_observer`: Observer effect (default: 1.0)
- `c_infinity`: Infinity constant (default: 38.8328157)
- `I_spin`: Spin entropy (default: 1.0)
- `w_sum`: Weight sum (default: 0.1)

### NRCI Calculation

```python
from ubp_semantics import nrci

nrci(simulated: List[float], target: List[float]) -> float
```

Calculate Non-Random Coherence Index.

#### Formula

```
NRCI = 1 - (RMSE(simulated, target) / σ(target))
```

Target: ≥ 0.999999 (six nines fidelity)

### Toggle Operations

#### Basic Operations

```python
from ubp_semantics import toggle_and, toggle_xor, toggle_or

# AND: min(b_i, b_j)
toggle_and(b_i: Union[OffBit, int], b_j: Union[OffBit, int]) -> Union[OffBit, int]

# XOR: |b_i - b_j|
toggle_xor(b_i: Union[OffBit, int], b_j: Union[OffBit, int]) -> Union[OffBit, int]

# OR: max(b_i, b_j)
toggle_or(b_i: Union[OffBit, int], b_j: Union[OffBit, int]) -> Union[OffBit, int]
```

#### Advanced Operations

```python
from ubp_semantics import (
    resonance_toggle, entanglement_toggle, superposition_toggle,
    hybrid_xor_resonance, spin_transition
)

# Resonance: b_i × exp(-k × (t × f)²)
resonance_toggle(offbit: OffBit, frequency: float, time: float, k: float = 0.0002) -> OffBit

# Entanglement: b_i × b_j × C_ij (C_ij ≥ 0.95)
entanglement_toggle(b_i: OffBit, b_j: OffBit, coherence: float) -> OffBit

# Superposition: Σ(states × weights)
superposition_toggle(states: List[OffBit], weights: List[float]) -> OffBit

# Hybrid XOR Resonance: |b_i - b_j| × exp(-k × d²)
hybrid_xor_resonance(b_i: OffBit, b_j: OffBit, distance: float, k: float = 0.0002) -> OffBit

# Spin Transition: b_i × ln(1/p_s)
spin_transition(offbit: OffBit, p_s: float) -> OffBit
```

### Coherence Functions

```python
from ubp_semantics import coherence, global_coherence_invariant

# Signal coherence: C_ij = (1/N) × Σ(s_i(t_k) × s_j(t_k))
coherence(signal_i: List[float], signal_j: List[float]) -> float

# Global Coherence Invariant: cos(2π × f_avg × Δt)
global_coherence_invariant(f_avg: float, delta_t: float = 0.318309886) -> float
```

### Validation Metrics

```python
from ubp_semantics import (
    coherence_pressure_spatial, coherence_pressure_temporal,
    fractal_dimension, calculate_system_coherence_score
)

# Spatial coherence pressure
coherence_pressure_spatial(distances: List[float], 
                          max_distances: List[float], 
                          active_bits: List[int]) -> float

# Temporal coherence pressure
coherence_pressure_temporal(time_diffs: List[float], 
                           max_time_diff: float, 
                           frequencies: List[float]) -> float

# Fractal dimension: D = log(m) / log(s)
fractal_dimension(sub_clusters: int, scale_factor: float = 2.0) -> float

# System coherence score
calculate_system_coherence_score(nrci: float, 
                                coherence_pressure: float, 
                                fractal_dim: float, 
                                sri: float, 
                                cri: float) -> float
```

## Runtime System

### Runtime Class

```python
from ubp_vm import Runtime

# Constructor
Runtime(hardware_profile: str = "desktop_8gb")
```

#### Methods

```python
# Realm management
set_realm(realm_name: str)
get_realm_config(realm_name: str = None) -> Dict[str, Any]

# Bitfield initialization
initialize_bitfield(pattern: str = "sparse_random", 
                   density: float = 0.01, 
                   seed: int = None)

# Toggle operations
execute_toggle_operation(operation: str, 
                        coord1: Tuple[int, ...], 
                        coord2: Tuple[int, ...] = None, 
                        **kwargs) -> OffBit

# Simulation
run_simulation(steps: int, 
              operations_per_step: int = 10,
              target_coords: List[Tuple[int, ...]] = None,
              record_timeline: bool = True) -> SimulationResult

# State management
export_state(filepath: str, format: str = "json")
reset()
get_performance_stats() -> Dict[str, float]
```

#### Properties

- `state: SimulationState` - Current simulation state
- `bitfield: Bitfield` - Active Bitfield
- `hardware_profile: str` - Hardware configuration
- `realm_configs: Dict` - Available realm configurations

### SimulationResult

```python
@dataclass
class SimulationResult:
    initial_state: SimulationState
    final_state: SimulationState
    metrics: Dict[str, float]
    timeline: List[SimulationState]
    execution_time: float
    
    def to_dict() -> Dict[str, Any]
```

### SimulationState

```python
@dataclass
class SimulationState:
    time_step: int = 0
    global_time: float = 0.0
    active_realm: str = "quantum"
    energy_value: float = 0.0
    nrci_value: float = 0.0
    coherence_pressure: float = 0.0
    total_toggles: int = 0
    
    def to_dict() -> Dict[str, Any]
```

## DSL Interface

### Script Execution

```python
from ubp_vm import eval_program, parse_ubp_script
from ubp_vm.dsl import DSLParser

# Execute complete program
eval_program(script_content: str, hardware_profile: str = "desktop_8gb") -> Dict[str, Any]

# Parse script into commands
parse_ubp_script(script_content: str) -> List[UBPCommand]

# Manual parser usage
parser = DSLParser()
results = parser.execute_script(script_content)
```

### DSL Commands

#### Runtime Commands

```ubp
init-runtime hardware=<profile>
use-realm <realm_name>
set-var <name> <value>
reset
```

#### Bitfield Commands

```ubp
init-bitfield pattern=<pattern> density=<float> seed=<int>
```

Patterns: `sparse_random`, `quantum_bias`, `realm_specific`

#### Toggle Commands

```ubp
toggle <operation> <coord1> [coord2] [parameters...]
```

Operations: `and`, `xor`, `or`, `resonance`, `entanglement`, `superposition`, `hybrid_xor_resonance`, `spin_transition`, `tgic`

#### Simulation Commands

```ubp
run-simulation steps=<int> ops_per_step=<int> timeline=<bool>
get-metrics
```

#### Export Commands

```ubp
export-state <filepath> format=<format>
export-results <filepath>
```

### Command Line Interface

```bash
# Run script
ubp-run script.ubp

# Interactive mode
ubp-run -i

# With output file
ubp-run script.ubp -o results.json

# List examples
ubp-run --list-examples
```

## Constants and Configuration

### Loading Constants

```python
from ubp_semantics import load_constants, get_realm_constants

# Load all constants
constants = load_constants()

# Get realm-specific constants
quantum_config = get_realm_constants("quantum")
```

### Mathematical Constants

```python
from ubp_semantics import PI, PHI, EULER_E, C

print(f"π = {PI}")           # 3.141592653589793
print(f"φ = {PHI}")          # 1.618033988749895
print(f"e = {EULER_E}")      # 2.718281828459045
print(f"c = {C}")            # 299792458
```

### Hardware Profiles

```python
# Available profiles
profiles = ["desktop_8gb", "mobile_4gb", "raspberry_pi"]

# Profile specifications
desktop_8gb = {
    "max_offbits": 1000000,
    "matrix_format": "dok_matrix",
    "compression": None
}

mobile_4gb = {
    "max_offbits": 10000,
    "matrix_format": "compressed_sparse",
    "compression": "reed_solomon"
}

raspberry_pi = {
    "max_offbits": 100000,
    "matrix_format": "compressed_sparse", 
    "compression": "reed_solomon"
}
```

### Realm Configurations

```python
# Available realms
realms = [
    "quantum", "electromagnetic", "gravitational", 
    "biological", "cosmological", "nuclear", "optical"
]

# Realm properties
quantum = {
    "name": "Quantum",
    "main_crv": 0.2265234857,  # e/12
    "frequency": 4.58e14,      # Hz
    "wavelength": 655,         # nm
    "nrci_baseline": 0.875,
    "geometry": "tetrahedral"
}
```

## Examples

### Basic Usage

```python
from ubp_vm import Runtime
from ubp_semantics import OffBit, energy, nrci

# Initialize system
runtime = Runtime("desktop_8gb")
runtime.set_realm("quantum")
runtime.initialize_bitfield("quantum_bias", density=0.01, seed=42)

# Execute operations
coord1 = (10, 10, 10, 1, 0, 0)
coord2 = (10, 10, 10, 1, 0, 1)

result = runtime.execute_toggle_operation("xor", coord1, coord2)
print(f"XOR result: {result}")

# Run simulation
sim_result = runtime.run_simulation(steps=100, operations_per_step=10)
print(f"Final NRCI: {sim_result.final_state.nrci_value:.6f}")
```

### Script Usage

```python
from ubp_vm import eval_program

script = '''
use-realm quantum
init-bitfield pattern=quantum_bias density=0.01 seed=42
toggle xor [0,0,0,0,0,0] [0,0,0,0,0,1]
run-simulation steps=50 ops_per_step=10
get-metrics
'''

results = eval_program(script)
print(f"NRCI: {results['final_state']['runtime_state']['nrci_value']}")
```

### Energy Calculation

```python
from ubp_semantics import energy, resonance_strength, structural_optimality

# Calculate energy with custom parameters
M = 1000  # Active OffBits
R = resonance_strength(R_0=0.95, H_t=0.05)
S_opt = structural_optimality([1.0, 2.0, 3.0], 5.0, [6, 8, 10])

E = energy(M=M, R=R, S_opt=S_opt)
print(f"System energy: {E:.2e}")
```

### NRCI Validation

```python
from ubp_semantics import nrci
import numpy as np

# Generate test data
target = [1.0, 2.0, 3.0, 4.0, 5.0]
simulated = [1.01, 1.98, 3.02, 3.97, 5.01]

nrci_value = nrci(simulated, target)
print(f"NRCI: {nrci_value:.6f}")
print(f"Meets target (≥0.999999): {nrci_value >= 0.999999}")
```

### Multi-Realm Simulation

```python
from ubp_vm import Runtime

runtime = Runtime("desktop_8gb")

realms = ["quantum", "electromagnetic", "gravitational"]
results = {}

for realm in realms:
    runtime.reset()
    runtime.set_realm(realm)
    runtime.initialize_bitfield("realm_specific", density=0.005, seed=42)
    
    result = runtime.run_simulation(steps=20, operations_per_step=5)
    results[realm] = result.final_state.nrci_value

for realm, nrci_val in results.items():
    print(f"{realm}: NRCI = {nrci_val:.6f}")
```

## Error Handling

### Exception Types

```python
from ubp_vm.dsl import UBPParseError, UBPRuntimeError

try:
    eval_program("invalid-command")
except UBPParseError as e:
    print(f"Parse error: {e}")
except UBPRuntimeError as e:
    print(f"Runtime error: {e}")
```

### Validation

```python
from ubp_semantics import Bitfield

bitfield = Bitfield("desktop_8gb")

# Coordinate validation
coord = (200, 0, 0, 0, 0, 0)  # Out of bounds
if not bitfield.is_valid_coordinate(coord):
    print("Invalid coordinate")

# Hardware limits
if bitfield.total_offbits >= bitfield.max_offbits:
    print("Hardware limit reached")
```

## Performance Considerations

### Memory Usage

- Use appropriate hardware profiles for your system
- Monitor `bitfield.current_sparsity` for memory efficiency
- Consider compression for large simulations

### Optimization Tips

- Use sparse patterns for large Bitfields
- Batch toggle operations when possible
- Profile with `runtime.get_performance_stats()`

### Hardware Scaling

```python
# Choose appropriate profile
if available_memory >= 8_000_000_000:  # 8GB
    profile = "desktop_8gb"
elif available_memory >= 4_000_000_000:  # 4GB
    profile = "mobile_4gb"
else:
    profile = "raspberry_pi"

runtime = Runtime(profile)
```

---

**API Version**: 1.0.0  
**Last Updated**: August 28, 2025

