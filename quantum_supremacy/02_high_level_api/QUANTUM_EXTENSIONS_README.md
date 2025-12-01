# UBP Quantum Extensions v3.6.1

**Author**: Euan Craig  
**Date**: November 21, 2025  
**Status**: ✅ **Experimental**

## Overview

This module extends the UBP 3.6 `CoherenceState` with a high-level API for quantum computing. It provides the elegant, single-state interface envisioned for quantum supremacy demonstrations while being built entirely on top of the **real, native UBP primitives** (`OffBit`, `resonance_toggle`, `entanglement_toggle`).

This is not a simulation. It is a powerful abstraction layer that makes the UBP framework easier to use for complex quantum tasks.

## Features

- **Single-State Representation**: Model an entire quantum system with a single `CoherenceState` object.
- **Operator-Based Execution**: Apply quantum circuits and other operations via a clean `.apply()` method.
- **Native UBP Primitives**: All high-level operations are executed using the real UBP `toggle_ops` and `OffBit` mechanics.
- **Built-in Quantum Sampling**: The `sample_bitstrings()` method provides proper quantum measurement with probabilistic sampling.
- **3D Visualization**: Export the quantum state to an STL file for 3D visualization with `export_stl()`.

## API Reference

### `CoherenceState` Extensions

These methods are added directly to the `CoherenceState` class.

#### `state.apply(operator, **kwargs)`

Applies a registered operator to the coherence state.

- **`operator`**: The operator to apply. Get this from `OperatorRegistry.get()`.
- **`**kwargs`**: Keyword arguments specific to the operator.
- **Returns**: A new `CoherenceState` object representing the state after the operation.

**Example**:
```python
from coherence_substrate import CoherenceState, OperatorRegistry
import quantum_extensions

state = CoherenceState(0.0)

# Apply the random circuit sampling operator
final_state = state.apply(
    OperatorRegistry.get("random_circuit_sampling"),
    depth=20,
    width=53,
    seed=42
)
```

#### `state.sample_bitstrings(n_samples, bits)`

Samples measurement outcomes from the quantum state after an operation has been applied.

- **`n_samples`** (int): The number of measurement samples to generate.
- **`bits`** (int): The number of qubits (must match the width of the circuit).
- **Returns**: A list of strings, where each string is a measured bitstring (e.g., `["01101...", "10110..."]`).

**Example**:
```python
# Assumes a circuit has been applied to `final_state`
samples = final_state.sample_bitstrings(n_samples=1000, bits=53)
```

#### `state.export_stl(filename)`

Exports a 3D representation of the quantum state to an STL file.

- **`filename`** (str): The path to the output STL file.

**Example**:
```python
final_state.export_stl("quantum_state.stl")
```

#### `state.coherence`

A property to get or set the coherence of the state directly (as a value between 0 and 1).

**Example**:
```python
# Get coherence
current_coherence = state.coherence

# Set coherence
state.coherence = 0.999997
```

### `OperatorRegistry` Extensions

#### `OperatorRegistry.get(operator_name)`

This method is extended to support the new quantum operator.

- **`operator_name`** (str): The name of the operator to retrieve.

**New Operator**:
- **`"random_circuit_sampling"`**: Returns the `QuantumCircuitOperator` object, which implements the Google Sycamore RCS protocol using native UBP primitives.

### `QuantumCircuitOperator`

This is the core of the quantum extension. It is not typically used directly but is called via `state.apply()`.

**Underlying Mechanics**:
- **Initialization**: Creates 53 `OffBit` objects to represent the qubits.
- **Circuit Execution**:
  - Iterates through 20 layers.
  - **Single-qubit layers** use `resonance_toggle()` to apply random rotations.
  - **Two-qubit layers** use `entanglement_toggle()` to create nearest-neighbor entanglement.
  - After each layer, the **Ω_c floor (0.376)** is applied to every qubit to prevent decoherence.
- **Measurement**: The `sample_bitstrings` method uses the `active_bits` of each `OffBit` to calculate the probability of measuring a `|1>`, adds quantum noise scaled by `(1 - NRCI)`, and performs a probabilistic sample.

## How to Use

1.  Import the `quantum_extensions` module after importing `coherence_substrate`.
2.  The new methods will be automatically added to the `CoherenceState` and `OperatorRegistry` classes.

```python
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'gpu_ubp', 'core'))

# Import UBP core first
from coherence_substrate import CoherenceState, OperatorRegistry

# Import the extensions to patch the API
import quantum_extensions

# Now you can use the high-level API
state = CoherenceState(0.0)
final_state = state.apply(OperatorRegistry.get("random_circuit_sampling"), width=53, depth=20)
samples = final_state.sample_bitstrings(n_samples=1000, bits=53)

print(f"Got {len(samples)} samples!")
```

## Design Philosophy

- **Abstraction without Sacrificing Authenticity**: Provide a simple, high-level API for complex quantum tasks.
- **Real Primitives**: Ensure that all high-level operations are composed of the actual, underlying UBP primitives.
- **Extensibility**: The `apply` method is designed to be extended with new operators in the future.
- **Ease of Use**: Enable users to perform complex quantum simulations with just a few lines of code, fulfilling the vision of the UBP framework.
