# GPU UBP System Development Whiteboard

**Project Goal:** Build fully functional GPU-accelerated UBP 3.6 system for iMac (Intel Iris Pro)  
**Started:** November 21, 2025  
**Status:** Phase 2 - Implementation with Taichi + Metal

---

## Key Decisions

### Technology Stack (FINAL)
- ✅ **CPU Layer:** Python 3.11 + UBP 3.6 (complete, no mocks)
- ✅ **GPU Layer:** Taichi with Metal backend (proven for Intel Iris Pro)
- ✅ **Architecture:** Master-Worker pattern (CPU authority, GPU visualization)
- ✅ **Precision:** CPU 64-bit, GPU 32-bit (visualization only)

### Why Taichi + Metal?
1. **Proven solution:** Already validated for Intel Iris Pro hardware
2. **Keep Python logic:** 64-bit TGIC stays in Python (high fidelity)
3. **Fastest path:** Focus on study data, not API wrestling
4. **Target:** CHSH Entanglement Test and other real studies

---

## Architecture Overview

```
CPU (64-bit Authority)          GPU (32-bit Worker - Taichi)
==================             ============================
UBP 3.6 Core                   Taichi Fields (Metal backend)
- CoherenceState               - ti.field(dtype=ti.f32) for NRCI
- Operators                    - ti.Vector.field(3, ti.f32) for positions
- TGIC (Dodecahedral)          - ti.field(dtype=ti.i32) for connections
- Error Correction             
- Resonance tracking           Taichi Kernels (@ti.kernel)
                               - Color mapping (NRCI → RGB)
State Bridge                   - Particle rendering
- CoherenceState → f32         - Edge rendering
- TGIC graph → adjacency       
- Batch per CSC                Visualization
- Validate < 1e-6              - 60+ FPS target
                               - Interactive (pause/step/reset)
```

---

## Implementation Plan

### Phase 1: Core Bridge (Current)
- [x] Project structure created
- [x] Taichi installed (v1.7.4)
- [ ] Create `gpu_bridge.py` - State serialization
- [ ] Create TGIC graph baking function
- [ ] Round-trip validation test

### Phase 2: Taichi GPU Layer
- [ ] Initialize Taichi with Metal backend
- [ ] Create ti.fields for NRCI, positions, connections
- [ ] Write @ti.kernel for NRCI → color mapping
- [ ] Data transfer: CPU → Taichi fields

### Phase 3: Visualization
- [ ] Particle renderer (nodes as spheres/points)
- [ ] Edge renderer (connections as lines)
- [ ] Camera controls (orbit, zoom, pan)
- [ ] Real-time metrics overlay (NRCI, CSC count, regime)

### Phase 4: Validation Framework
- [ ] Fidelity tests: GPU NRCI vs CPU NRCI
- [ ] Statistical validation (KS test)
- [ ] Temporal coherence tracking
- [ ] Performance benchmarks (CSC/sec, FPS)

### Phase 5: Real Studies
- [ ] **CHSH Entanglement Test** (priority)
- [ ] Quantum realm: energy levels, wavefunctions
- [ ] TGIC topology: dodecahedral coherence
- [ ] Error correction: regime transitions

---

## Critical Findings

### UBP 3.6 System
- **Complete implementation:** coherence_substrate, kernels, TGIC, error correction, 9 realms
- **Zero external dependencies:** Pure Python (no numpy in UBP core)
- **Log-NRCI tracking:** Accurate error accumulation in log space
- **100% test coverage:** 72+ tests passing
- **TGIC:** Dodecahedral graph (20 nodes, 30 edges, golden ratio geometry)

### Hardware Constraints (Intel Iris Pro)
- **No f64 support:** Metal backend uses f32 only
- **Fidelity requirement:** NRCI ≥ 0.999997 (±1e-6)
- **Solution:** CPU does ALL arithmetic, GPU only reads/visualizes
- **Proven:** This architecture already works per user confirmation

### Precision Strategy
1. **CPU:** All UBP operations in 64-bit (CoherenceState, operators, NRCI)
2. **Bridge:** Convert f64 → f32 with validation (must be < 1e-6 error)
3. **GPU:** Read-only access to f32 NRCI for visualization
4. **Never:** GPU arithmetic that modifies UBP state

---

## TGIC Graph Structure

### Dodecahedral Graph (from tgic.py)
- **20 vertices:** Generated using golden ratio φ
- **30 edges:** Each vertex connects to exactly 3 others
- **12 pentagonal faces**
- **3-6-9 structure:** Natural coherence geometry

### Baking Strategy (for GPU)
```python
# Input: DodecahedralGraph (Python objects)
# Output: Taichi fields (GPU arrays)

positions = ti.Vector.field(3, dtype=ti.f32, shape=20)
connections = ti.field(dtype=ti.i32, shape=(20, 3))  # Max 3 neighbors
nrci_values = ti.field(dtype=ti.f32, shape=20)
```

---

## Open Questions

1. ✅ **Backend choice:** Taichi + Metal (decided)
2. **Initial node count:** Start with 20 (dodecahedron) or 100?
3. **CSC rate:** How many cycles per second for studies?
4. **Study priority:** CHSH test first, then quantum realm?
5. **Export format:** JSON for data, PNG for visualizations?

---

## Next Actions (Immediate)

1. Create symlink to UBP 3.6 for imports
2. Create `gpu_bridge.py` - CoherenceState serialization
3. Create `tgic_baker.py` - Convert DodecahedralGraph → Taichi fields
4. Create `gpu_renderer.py` - Taichi visualization
5. Test round-trip: CPU → GPU → validate fidelity

---

## Notes

- **No mocks/placeholders:** Using complete UBP 3.6 system from /home/ubuntu/UBP_Repo/ubp_3.6
- **Real data only:** All validation uses actual UBP calculations
- **Metal backend:** Will use CPU backend in sandbox, Metal on user's iMac
- **Focus on studies:** Goal is to generate real UBP data for research
- **CHSH Entanglement Test:** Priority study identified by user
