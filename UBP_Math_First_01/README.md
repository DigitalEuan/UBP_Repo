# UBP-Core: Universal Binary Principle Implementation
Euan Craig, New Zealand

A complete, runnable Python implementation of the Universal Binary Principle (UBP) computational framework. This project provides a clean, modular foundation for UBP research and development, implementing the mathematical axioms and specifications from the authoritative UBP documentation.

## Overview

The Universal Binary Principle (UBP) is a deterministic, toggle-based computational framework that unifies physical, biological, quantum, nuclear, gravitational, optical, and cosmological phenomena using a 6D Bitfield structure. This implementation targets high coherence (NRCI ≥ 0.999999) through mathematically rigorous operations and realm-specific dynamics.

### Key Features

- **Spec-Driven Architecture**: All mathematical operations implement formulas directly from UBP specifications
- **6D Bitfield**: Sparse computational substrate with 24-bit OffBits and 4 ontological layers
- **Multi-Realm Support**: Quantum, electromagnetic, gravitational, biological, cosmological, nuclear, and optical realms
- **Toggle Algebra**: Complete implementation of UBP toggle operations (AND, XOR, OR, resonance, entanglement, etc.)
- **Energy Equation**: Full UBP energy calculation with all parameters
- **NRCI Validation**: Non-Random Coherence Index targeting six nines fidelity (0.999999)
- **DSL Support**: Simple scripting language for UBP operations
- **Hardware Scaling**: Configurable for desktop (8GB), mobile (4GB), and Raspberry Pi platforms

## Quick Start

### Installation

```bash
# Clone or extract the ubp-core project
cd ubp-core

# Install dependencies (optional, uses only Python standard library + numpy/yaml)
pip install numpy pyyaml matplotlib  # matplotlib optional for plotting examples
```

### Basic Usage

#### Python API

```python
from ubp_vm import Runtime
from ubp_semantics import OffBit, energy, nrci

# Initialize UBP runtime
runtime = Runtime("desktop_8gb")
runtime.set_realm("quantum")
runtime.initialize_bitfield("quantum_bias", density=0.01, seed=42)

# Run simulation
result = runtime.run_simulation(steps=100, operations_per_step=10)

print(f"Final NRCI: {result.final_state.nrci_value:.6f}")
print(f"Energy: {result.final_state.energy_value:.2e}")
```

#### UBP Script Language

```bash
# Run a UBP script
python -c "
from ubp_vm import eval_program
result = eval_program('''
    use-realm quantum
    init-bitfield pattern=quantum_bias density=0.01 seed=42
    run-simulation steps=50 ops_per_step=10
    get-metrics
''')
print('NRCI:', result['final_state']['runtime_state']['nrci_value'])
"
```

### Examples

Run the included examples:

```bash
# Basic tutorial
python -c "from ubp_vm import eval_program; eval_program(open('examples/tutorial_basic.ubp').read())"

# Python API demonstration
python examples/python_api_example.py

# Quantum simulation
python -c "from ubp_vm import eval_program; eval_program(open('examples/quantum_simulation.ubp').read())"
```

## Architecture

### Project Structure

```
ubp-core/
├── spec/                    # Authoritative specifications
│   ├── core.yaml           # Constants and parameters
│   └── axioms.md           # Mathematical axioms
├── ubp_semantics/          # Pure mathematical functions
│   ├── constants.py        # Constants loader
│   ├── state.py           # OffBit and Bitfield classes
│   ├── kernels.py         # Core mathematical kernels
│   ├── energy.py          # Energy equation implementation
│   ├── toggle_ops.py      # Toggle algebra operations
│   └── metrics.py         # Validation metrics (NRCI, etc.)
├── ubp_vm/                 # Virtual machine and runtime
│   ├── runtime.py         # Runtime orchestration
│   └── dsl.py             # Domain-specific language
├── tests/                  # Comprehensive test suite
│   ├── test_axioms.py     # Mathematical axiom validation
│   └── test_integration.py # Integration tests
└── examples/               # Example scripts and tutorials
    ├── tutorial_basic.ubp
    ├── quantum_simulation.ubp
    ├── multi_realm_simulation.ubp
    └── python_api_example.py
```

### Core Components

#### 1. OffBit (24-bit Fundamental Unit)

```python
from ubp_semantics import OffBit

# Create OffBit with 4 ontological layers
offbit = OffBit(0x123456)
offbit.reality_layer = 42      # Observable properties (bits 0-5)
offbit.information_layer = 21  # Data processing (bits 6-11)
offbit.activation_layer = 15   # Dynamic states (bits 12-17)
offbit.unactivated_layer = 8   # Potential states (bits 18-23)
```

#### 2. Bitfield (6D Sparse Array)

```python
from ubp_semantics import Bitfield

# Initialize 6D Bitfield (170×170×170×5×2×2 = ~2.3M cells)
bitfield = Bitfield("desktop_8gb")
coord = (10, 20, 30, 1, 0, 1)
bitfield.set_offbit(coord, OffBit(12345))
```

#### 3. Toggle Operations

```python
from ubp_semantics import toggle_xor, resonance_toggle, entanglement_toggle

# Basic operations: AND, XOR, OR
result = toggle_xor(OffBit(100), OffBit(200))  # |100 - 200| = 100

# Advanced operations
resonance_result = resonance_toggle(OffBit(1000), frequency=100.0, time=0.1)
entanglement_result = entanglement_toggle(OffBit(100), OffBit(200), coherence=0.96)
```

#### 4. Energy Equation

```python
from ubp_semantics import energy

# Complete UBP energy equation
E = energy(
    M=1000,              # Active OffBits
    R=0.965885,          # Resonance strength
    S_opt=0.98,          # Structural optimality
    P_GCI=0.827046,      # Global Coherence Invariant
    O_observer=1.0       # Observer effect
)
```

#### 5. NRCI Validation

```python
from ubp_semantics import nrci

# Calculate Non-Random Coherence Index
simulated = [1.0, 2.0, 3.0, 4.0, 5.0]
target = [1.01, 1.98, 3.02, 3.97, 5.01]
nrci_value = nrci(simulated, target)  # Target: ≥ 0.999999
```

## Realms

UBP supports seven distinct realms, each with specific mathematical properties:

| Realm | CRV | Frequency | Wavelength | NRCI Baseline | Geometry |
|-------|-----|-----------|------------|---------------|----------|
| Quantum | e/12 ≈ 0.2265 | 4.58×10¹⁴ Hz | 655 nm | 0.875 | Tetrahedral |
| Electromagnetic | π ≈ 3.1416 | 3.141593 Hz | 635 nm | 1.0 | Cubic |
| Gravitational | 100 | 100 Hz | 1000 nm | 0.915 | FCC |
| Biological | 10 | 10 Hz | 700 nm | 0.911 | H4 120-Cell |
| Cosmological | π^φ ≈ 0.8320 | 10⁻¹¹ Hz | 800 nm | 0.797 | H3 Icosahedral |
| Nuclear | 1.2356×10²⁰ | 10¹⁶-10²⁰ Hz | - | TBD | E8-to-G2 |
| Optical | 5×10¹⁴ | 5×10¹⁴ Hz | 600 nm | >0.999999 | Photonic |

## UBP Script Language

The UBP DSL provides a simple scripting interface:

```ubp
# Initialize system
init-runtime hardware=desktop_8gb
use-realm quantum

# Setup Bitfield
init-bitfield pattern=quantum_bias density=0.01 seed=42

# Execute operations
toggle xor [0,0,0,0,0,0] [0,0,0,0,0,1]
toggle resonance [1,1,1,0,0,0] frequency=1000.0 time=0.001
toggle entanglement [2,2,2,0,0,0] [2,2,2,0,0,1] coherence=0.95

# Run simulation
run-simulation steps=100 ops_per_step=10 timeline=true

# Export results
export-results simulation_results.json
get-metrics
```

### Available Commands

- `init-runtime hardware=<profile>` - Initialize runtime
- `use-realm <realm_name>` - Set active realm
- `init-bitfield pattern=<pattern> density=<float> seed=<int>` - Initialize Bitfield
- `toggle <operation> <coord1> [coord2] [params...]` - Execute toggle operation
- `run-simulation steps=<int> ops_per_step=<int>` - Run simulation
- `get-metrics` - Get current system metrics
- `export-results <filename>` - Export simulation results
- `export-state <filename>` - Export runtime state

## Testing

Run the comprehensive test suite:

```bash
# Run all tests
python -m pytest tests/ -v

# Run specific test categories
python tests/test_axioms.py          # Mathematical axiom validation
python tests/test_integration.py    # Integration tests

# Run with coverage (if pytest-cov installed)
python -m pytest tests/ --cov=ubp_semantics --cov=ubp_vm
```

### Test Categories

1. **Axiom Tests** (`test_axioms.py`): Validate mathematical formulas against specifications
2. **Integration Tests** (`test_integration.py`): Test complete workflows and system interactions
3. **Performance Tests**: Validate hardware scaling and performance targets

## Hardware Profiles

UBP-Core supports multiple hardware configurations:

### Desktop (8GB)
- Max OffBits: 1,000,000
- Matrix format: `dok_matrix`
- Target: Full-scale simulations

### Mobile (4GB)
- Max OffBits: 10,000
- Matrix format: Compressed sparse
- Compression: Reed-Solomon (30%)

### Raspberry Pi
- Max OffBits: 100,000
- Matrix format: Compressed sparse
- Target: <2 seconds per operation

## Mathematical Foundation

All implementations are based on the authoritative UBP specifications:

### Core Axioms

1. **Energy Equation**: `E = M × C × (R × S_opt) × P_GCI × O_observer × c_∞ × I_spin × Σ(w_ij M_ij)`
2. **NRCI**: `NRCI = 1 - (RMSE(S, T) / σ(T))`
3. **Resonance Kernel**: `f(d) = exp(-k × d²)`
4. **Toggle Operations**: `AND = min(b_i, b_j)`, `XOR = |b_i - b_j|`, `OR = max(b_i, b_j)`
5. **Coherence**: `C_ij = (1/N) × Σ(s_i(t_k) × s_j(t_k))`

### Constants

All mathematical constants are loaded from `spec/core.yaml`:
- π = 3.141592653589793
- φ = 1.618033988749895 (Golden Ratio)
- e = 2.718281828459045
- c = 299,792,458 m/s (Speed of light)

## Development

### Adding New Realms

1. Add realm configuration to `spec/core.yaml`
2. Implement realm-specific operations in `ubp_semantics/`
3. Add tests in `tests/test_axioms.py`
4. Update documentation

### Extending Toggle Operations

1. Define mathematical axiom in `spec/axioms.md`
2. Implement function in `ubp_semantics/toggle_ops.py`
3. Add to DSL parser in `ubp_vm/dsl.py`
4. Create validation tests

### Performance Optimization

- Use sparse matrix operations for large Bitfields
- Implement hardware-specific optimizations
- Profile with `cProfile` and optimize bottlenecks

## Validation Targets

UBP-Core aims to achieve:

- **NRCI ≥ 0.999999** (six nines fidelity)
- **Coherence ≥ 0.95** for observable interactions
- **Energy conservation** within numerical precision
- **Cross-realm synchronization** with temporal coherence
- **Hardware scalability** across all supported platforms

## Contributing

1. Ensure all mathematical implementations follow `spec/axioms.md`
2. Add comprehensive tests for new functionality
3. Maintain compatibility with all hardware profiles
4. Update documentation for API changes

## License

Universal Binary Principle is free of copyright. Specific inventions remain copyright to Euan Craig, New Zealand 2025.

## References

- Craig, E. (2025). *The Universal Binary Principle: A Meta-Temporal Framework for a Computational Reality*
- Del Bel, J. (2025). *The Cykloid Adelic Recursive Expansive Field Equation (CARFE)*
- Vossen, S. *Dot Theory*. https://www.dottheory.co.uk/
- Craig, E., & Grok (xAI). (2025). *Universal Binary Principle Research Prompt v15.0*

---

**Version**: 1.0.0  
**Created**: August 28, 2025  
**Source Documents**: ubp_20Aug2025.txt, UBP29June25.pdf

