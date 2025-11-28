# UBP 3.7.1 - GLR Binary Toggle Architecture

## 1. Core Principle: Pure Binary Logic

The fundamental change is to move all GLR (Geometric Lattice Realm) frameworks from continuous/vector/phase mathematics to pure binary toggle logic. This aligns with the core UBP principle that all information can be represented by binary states.

**Key Changes:**

- **No more `float` positions:** All lattice sites will be represented by integer coordinates.
- **No more `resonance_phase`:** The state of a site will be a 24-bit `OffBit` object, not a continuous phase angle.
- **No more Platonic solids:** The geometry will be defined by the connectivity of the lattice, not by embedding Platonic solids.
- **No more continuous evolution:** All state changes will be discrete toggle operations on `OffBit` objects.

## 2. Data Structures

### 2.1. `LatticeSite`

A dataclass representing a single point in the lattice.

```python
from dataclasses import dataclass
from typing import Tuple
from core.state import OffBit

@dataclass
class LatticeSite:
    coordinates: Tuple[int, int, int]  # Integer coordinates
    state: OffBit                      # 24-bit binary state
    neighbors: list["LatticeSite"]   # List of connected sites
```

### 2.2. `GLRFramework` (Base Class)

An abstract base class that defines the common interface for all GLR frameworks.

```python
from abc import ABC, abstractmethod

class GLRFramework(ABC):
    def __init__(self, dimensions: Tuple[int, int, int]):
        self.sites = self._create_lattice(dimensions)
        self._connect_neighbors()

    @abstractmethod
    def _create_lattice(self, dimensions):
        pass

    @abstractmethod
    def _connect_neighbors(self):
        pass

    def get_site(self, coordinates: Tuple[int, int, int]) -> LatticeSite:
        # ... implementation ...
        pass

    def toggle_site(self, coordinates: Tuple[int, int, int], toggle_pattern: OffBit):
        site = self.get_site(coordinates)
        site.state.toggle(toggle_pattern)

    def evolve(self):
        # Apply toggle rules to all sites based on neighbor states
        pass
```

## 3. GLR Framework Implementations

Each of the 5 GLR frameworks will be a concrete implementation of the `GLRFramework` base class, differing only in their `_create_lattice` and `_connect_neighbors` methods.

### 3.1. `SimpleCubicGLR`

- **Lattice:** Simple cubic grid.
- **Neighbors:** 6 nearest neighbors (up, down, left, right, front, back).

### 3.2. `DiamondGLR`

- **Lattice:** Diamond cubic structure.
- **Neighbors:** 4 nearest neighbors in a tetrahedral arrangement.

### 3.3. `FCCGLR` (Face-Centered Cubic)

- **Lattice:** Face-centered cubic structure.
- **Neighbors:** 12 nearest neighbors.

### 3.4. `H3IcosahedralGLR`

- **Lattice:** Projection of the H3 Coxeter group (icosahedral symmetry).
- **Neighbors:** Defined by the H3 group structure.

### 3.5. `H4120CellGLR`

- **Lattice:** Projection of the H4 Coxeter group (120-cell symmetry).
- **Neighbors:** Defined by the H4 group structure.

## 4. Toggle Logic

The `evolve()` method in the base class will implement the core toggle logic. This will be a simple rule applied to all sites, such as:

```python
# Example toggle rule in evolve()
def evolve(self):
    for site in self.sites.values():
        # XOR the state with the XOR of all neighbor states
        neighbor_xor = OffBit(0)
        for neighbor in site.neighbors:
            neighbor_xor.toggle(neighbor.state)
        site.state.toggle(neighbor_xor)
```

This architecture ensures that all GLR frameworks are built on a common, pure binary foundation, and that the complexity is isolated to the lattice generation and connectivity, not the state representation or evolution logic.
