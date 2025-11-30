# TGIC Geometry Selection Guide

**Version:** 1.0  
**Date:** November 30, 2025  
**Status:** Production Ready

---

## Overview

TGIC (Triad Graph Interaction Constraint) now supports **6 geometric structures**, each optimized for different computational tasks. This guide helps you select the appropriate geometry for your UBP 3.7.1 application.

---

## Quick Reference

| Geometry | NRCI | Best For | Triad | Nodes | Edges |
|----------|------|----------|-------|-------|-------|
| **Dodecahedral** | 0.860 | General purpose, 3-6-9 resonance | (3,6,9) | 20 | 30 |
| **Tetrahedral** | 0.840 | Minimal proofs, base cases | (3,4,6) | 4 | 6 |
| **Cubic** | 0.800 | Orthogonal logic, base layer | (3,6,8) | 8 | 12 |
| **Leech 24D** | 0.600 | Deep coherence, cosmological | (3,8,24) | - | - |
| **Octahedral** | 0.520* | Spin-1 analogues, dual operations | (4,6,8) | 6 | 12 |
| **Icosahedral** | 0.480* | High coherence, consciousness | (5,12,30) | 12 | 30 |

*With default TGIC constraints. Use geometry-specific constraints for better performance.

---

## Detailed Geometry Profiles

### 1. Dodecahedral (Default) 🌟

**NRCI:** 0.860  
**Triad:** (3, 6, 9)  
**Structure:** 20 nodes, 30 edges, 3-regular

**Strengths:**
- ✅ Highest NRCI score (0.860)
- ✅ Perfect constraint satisfaction (100%)
- ✅ Balanced 3-6-9 resonance pattern
- ✅ Good coherence (0.65)
- ✅ Well-tested and validated

**Best For:**
- General-purpose TGIC operations
- UBP realm interactions
- 3-6-9 pattern enforcement
- Balanced performance across all metrics

**When to Use:**
- Default choice for most applications
- When you need proven, reliable performance
- When 3-6-9 resonance is important
- When you don't have specific geometric requirements

**Example:**
```python
from utils.tgic import TGICSystem, TGICGeometry

# Default geometry (dodecahedral)
system = TGICSystem()

# Or explicitly:
system = TGICSystem(geometry=TGICGeometry.DODECAHEDRAL)
```

---

### 2. Tetrahedral 🔺

**NRCI:** 0.840  
**Triad:** (3, 4, 6)  
**Structure:** 4 nodes, 6 edges, complete graph (K4)

**Strengths:**
- ✅ Second-highest NRCI (0.840)
- ✅ Simplest Platonic solid
- ✅ Complete connectivity (all nodes connected)
- ✅ Perfect for minimal proofs
- ✅ Fast computation (only 4 nodes)

**Best For:**
- Minimal proof systems
- Base case validation
- Simplex symmetry operations
- Fast prototyping
- Unit testing

**When to Use:**
- When you need the simplest non-trivial structure
- For proving fundamental theorems
- When computational speed is critical
- For base cases in recursive algorithms

**Example:**
```python
system = TGICSystem(geometry=TGICGeometry.TETRAHEDRAL)

# Perfect for minimal proofs
result = system.validate_tgic_system()
assert result['geometric_structure']  # Minimal but complete
```

---

### 3. Cubic 📦

**NRCI:** 0.800  
**Triad:** (3, 6, 8)  
**Structure:** 8 nodes, 12 edges, 3-regular

**Strengths:**
- ✅ Orthogonal structure (axis-aligned)
- ✅ Minimal nonlinearity
- ✅ Perfect for logical operations
- ✅ Dual to octahedral
- ✅ Familiar Cartesian geometry

**Best For:**
- Base logic layer operations
- Orthogonal transformations
- Boolean logic implementations
- Grid-based computations
- Classical computing analogues

**When to Use:**
- When you need axis-aligned operations
- For logical/boolean operations
- When orthogonality is important
- For interfacing with classical computing

**Example:**
```python
system = TGICSystem(geometry=TGICGeometry.CUBIC)

# Ideal for orthogonal operations
# Each edge aligns with x, y, or z axis
```

---

### 4. Leech 24D 🌌

**NRCI:** 0.600  
**Triad:** (3, 8, 24)  
**Structure:** 24D lattice (no 3D graph)

**Strengths:**
- ✅ Optimal sphere packing in 24D
- ✅ Deep mathematical structure
- ✅ Cosmological applications
- ✅ Pre-optimized (no position tuning needed)
- ✅ Unique high-dimensional properties

**Best For:**
- Deep coherence layer
- Cosmological simulations
- High-dimensional optimization
- Advanced mathematical operations
- Research applications

**When to Use:**
- When you need 24D operations
- For cosmological-scale computations
- When optimal packing is required
- For advanced research (not typical applications)

**Limitations:**
- ⚠️ No 3D graph structure
- ⚠️ Zero coherence (no nodes)
- ⚠️ Limited to lattice operations
- ⚠️ Harder to visualize

**Example:**
```python
system = TGICSystem(geometry=TGICGeometry.LEECH_24D)

# Access 24D lattice points
lattice_points = system.leech_projection.lattice_points
```

---

### 5. Octahedral ⬢

**NRCI:** 0.520 (with default constraints)  
**Triad:** (4, 6, 8)  
**Structure:** 6 nodes, 12 edges, 4-regular

**Strengths:**
- ✅ Dual to cubic
- ✅ 4-regular (high connectivity)
- ✅ Spin-1 analogues
- ✅ Excellent with geometry-specific constraints (0.820 NRCI)

**Best For:**
- Spin-1 quantum analogues
- Dual operations (complement to cubic)
- High-connectivity tasks
- Rotational symmetry operations

**When to Use:**
- When you need higher node connectivity (4 vs 3)
- For spin-1 particle analogues
- When using geometry-specific constraints
- For operations dual to cubic

**Note:** Performs better (0.820 NRCI) with geometry-specific constraints from `studies.TGIC.geometry_constraints_ext`.

**Example:**
```python
system = TGICSystem(geometry=TGICGeometry.OCTAHEDRAL)

# For best performance, use geometry-specific constraints
from studies.TGIC.geometry_constraints_ext import inject_geometry_methods
inject_geometry_methods(system)
```

---

### 6. Icosahedral 🌟

**NRCI:** 0.480 (with default constraints)  
**Triad:** (5, 12, 30)  
**Structure:** 12 nodes, 30 edges, 5-regular

**Strengths:**
- ✅ Highest coherence (0.70)
- ✅ Pentavalent symmetry (5-fold)
- ✅ Most edges (30)
- ✅ Excellent for consciousness layer (0.680 NRCI with specific constraints)

**Best For:**
- Consciousness layer operations
- High-coherence applications
- Pentavalent symmetry
- Complex interaction patterns

**When to Use:**
- When coherence is more important than constraint satisfaction
- For consciousness-related computations
- When you need 5-fold symmetry
- When using geometry-specific constraints

**Note:** Performs much better (0.680 NRCI) with geometry-specific constraints. Highest coherence of all geometries.

**Example:**
```python
system = TGICSystem(geometry=TGICGeometry.ICOSAHEDRAL)

# Best for high-coherence applications
analysis = system.analyze_interaction_patterns()
print(f"Coherence: {analysis['average_coherence']}")  # 0.70
```

---

## Selection Decision Tree

```
START: What is your primary goal?

├─ General UBP operations?
│  └─> DODECAHEDRAL (default, proven, balanced)
│
├─ Minimal/fastest computation?
│  └─> TETRAHEDRAL (4 nodes, complete graph)
│
├─ Orthogonal/logical operations?
│  └─> CUBIC (axis-aligned, minimal nonlinearity)
│
├─ High coherence needed?
│  └─> ICOSAHEDRAL (0.70 coherence, use specific constraints)
│
├─ High connectivity needed?
│  └─> OCTAHEDRAL (4-regular, use specific constraints)
│
├─ 24D/cosmological operations?
│  └─> LEECH_24D (optimal packing, research)
│
└─ Not sure?
   └─> DODECAHEDRAL (safe default choice)
```

---

## Performance Comparison

### By NRCI Score (Higher is Better)

1. **Dodecahedral:** 0.860 ⭐⭐⭐⭐⭐
2. **Tetrahedral:** 0.840 ⭐⭐⭐⭐⭐
3. **Cubic:** 0.800 ⭐⭐⭐⭐
4. **Leech 24D:** 0.600 ⭐⭐⭐
5. **Octahedral:** 0.520 ⭐⭐⭐ (0.820 with specific constraints)
6. **Icosahedral:** 0.480 ⭐⭐ (0.680 with specific constraints)

### By Coherence (Higher is Better)

1. **Icosahedral:** 0.700 ⭐⭐⭐⭐⭐
2. **Dodecahedral:** 0.650 ⭐⭐⭐⭐
3. **Tetrahedral:** 0.600 ⭐⭐⭐⭐
4. **Octahedral:** 0.550 ⭐⭐⭐
5. **Cubic:** 0.500 ⭐⭐⭐
6. **Leech 24D:** 0.000 (no nodes)

### By Constraint Satisfaction (Higher is Better)

1. **Dodecahedral:** 100% ✅✅✅
2. **Tetrahedral:** 100% ✅✅✅
3. **Cubic:** 100% ✅✅✅
4. **Leech 24D:** 100% ✅✅✅
5. **Octahedral:** 50% ⚠️
6. **Icosahedral:** 33% ⚠️

### By Computational Speed (Faster is Better)

1. **Tetrahedral:** 4 nodes ⚡⚡⚡⚡⚡
2. **Octahedral:** 6 nodes ⚡⚡⚡⚡
3. **Cubic:** 8 nodes ⚡⚡⚡⚡
4. **Icosahedral:** 12 nodes ⚡⚡⚡
5. **Dodecahedral:** 20 nodes ⚡⚡
6. **Leech 24D:** 24D lattice ⚡

---

## Usage Examples

### Example 1: Default Usage

```python
from utils.tgic import TGICSystem

# Use default (dodecahedral)
system = TGICSystem()

# Analyze
analysis = system.analyze_interaction_patterns()
print(f"NRCI: {0.6 * analysis['constraint_satisfaction']['satisfaction_rate'] + 0.4 * analysis['average_coherence']:.3f}")
```

### Example 2: Geometry Selection

```python
from utils.tgic import TGICSystem, TGICGeometry

# Choose geometry based on task
if task_type == "minimal_proof":
    system = TGICSystem(geometry=TGICGeometry.TETRAHEDRAL)
elif task_type == "logical_operation":
    system = TGICSystem(geometry=TGICGeometry.CUBIC)
elif task_type == "high_coherence":
    system = TGICSystem(geometry=TGICGeometry.ICOSAHEDRAL)
else:
    system = TGICSystem(geometry=TGICGeometry.DODECAHEDRAL)
```

### Example 3: Using Geometry-Specific Constraints

```python
from utils.tgic import TGICSystem, TGICGeometry
from studies.TGIC.geometry_constraints_ext import inject_geometry_methods

# Create system with specific geometry
system = TGICSystem(geometry=TGICGeometry.OCTAHEDRAL)

# Inject geometry-specific constraints for better performance
inject_geometry_methods(system)

# Now octahedral achieves 0.820 NRCI instead of 0.520
```

### Example 4: Comparing Geometries

```python
from utils.tgic import TGICSystem, TGICGeometry

geometries = [
    TGICGeometry.DODECAHEDRAL,
    TGICGeometry.TETRAHEDRAL,
    TGICGeometry.CUBIC
]

results = {}
for geo in geometries:
    system = TGICSystem(geometry=geo)
    analysis = system.analyze_interaction_patterns()
    nrci = 0.6 * analysis['constraint_satisfaction']['satisfaction_rate'] + 0.4 * analysis['average_coherence']
    results[geo.value] = nrci

best_geometry = max(results, key=results.get)
print(f"Best geometry for this task: {best_geometry}")
```

---

## Advanced Topics

### Geometry-Specific Constraints

For **octahedral** and **icosahedral** geometries, use geometry-specific constraints for optimal performance:

```python
from utils.tgic import TGICSystem, TGICGeometry
from studies.TGIC.geometry_constraints_ext import inject_geometry_methods

system = TGICSystem(geometry=TGICGeometry.OCTAHEDRAL)
inject_geometry_methods(system)  # Injects octahedral-specific constraints

# Performance improves from 0.520 → 0.820 NRCI
```

### Custom Geometry Selection Function

```python
def select_geometry(task_requirements):
    """
    Automatically select best geometry based on task requirements.
    
    Args:
        task_requirements: Dict with keys like 'coherence_priority', 'speed_priority', etc.
    
    Returns:
        TGICGeometry enum value
    """
    if task_requirements.get('speed_priority') == 'highest':
        return TGICGeometry.TETRAHEDRAL
    elif task_requirements.get('coherence_priority') == 'highest':
        return TGICGeometry.ICOSAHEDRAL
    elif task_requirements.get('orthogonal_required'):
        return TGICGeometry.CUBIC
    elif task_requirements.get('high_dimensional'):
        return TGICGeometry.LEECH_24D
    else:
        return TGICGeometry.DODECAHEDRAL  # Safe default

# Usage
geometry = select_geometry({'coherence_priority': 'highest'})
system = TGICSystem(geometry=geometry)
```

---

## Frequently Asked Questions

### Q: Which geometry should I use by default?

**A:** **Dodecahedral** (default). It has the highest NRCI (0.860), perfect constraint satisfaction, and is well-tested.

### Q: When should I use tetrahedral instead of dodecahedral?

**A:** When you need:
- Minimal computational overhead (only 4 nodes)
- Simplest non-trivial structure
- Fast prototyping or unit tests
- Minimal proofs or base cases

### Q: Why do octahedral and icosahedral have lower NRCI scores?

**A:** They perform poorly with the default TGIC constraints (designed for dodecahedral). Use geometry-specific constraints from `studies.TGIC.geometry_constraints_ext` for better performance (0.820 and 0.680 respectively).

### Q: Can I switch geometries during runtime?

**A:** No. Geometry is set during `TGICSystem` initialization. Create a new system instance to change geometry:

```python
system1 = TGICSystem(geometry=TGICGeometry.CUBIC)
# ... do work ...
system2 = TGICSystem(geometry=TGICGeometry.TETRAHEDRAL)
# ... do different work ...
```

### Q: What's the computational cost of each geometry?

**A:** Roughly proportional to node count:
- Tetrahedral: 4 nodes (fastest)
- Octahedral: 6 nodes
- Cubic: 8 nodes
- Icosahedral: 12 nodes
- Dodecahedral: 20 nodes
- Leech 24D: 24D lattice (variable)

### Q: Can I create custom geometries?

**A:** Yes, but requires implementing:
1. Graph generator (see `studies/TGIC/geometry_graphs.py`)
2. Geometry-specific constraints (see `studies/TGIC/geometry_constraints_ext.py`)
3. Registry entry (see `studies/TGIC/geometry_registry.py`)

---

## References

- **TGIC Implementation:** `ubp_3.7.1/utils/tgic.py`
- **Geometry Graphs:** `ubp_3.7.1/studies/TGIC/geometry_graphs.py`
- **Cross-Geometry Validation:** `ubp_3.7.1/studies/TGIC/CROSS_GEOMETRY_FINDINGS.md`
- **Geometry-Specific Constraints:** `ubp_3.7.1/studies/TGIC/geometry_constraints_ext.py`

---

## Changelog

**v1.0 (Nov 30, 2025)**
- Initial release
- 6 geometries supported
- Dodecahedral constraints tuned (0.460 → 0.860 NRCI)
- Leech 24D optimization fixed
- Full integration with main TGIC system

---

**Author:** UBP Development Team  
**Concept:** Qwen AI (cross-geometry validation)  
**Date:** November 30, 2025  
**Status:** ✅ Production Ready
