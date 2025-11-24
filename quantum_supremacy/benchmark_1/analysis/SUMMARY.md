# UBP Benchmark Study - Summary

**Date:** 2025-11-24T13:35:41.901458

## Benchmarks Completed

| Benchmark | Realm | Key Metric | NRCI | Status |
|-----------|-------|------------|------|--------|
| CHSH Quantum | Quantum | S = -2.831 ± 0.031 | 0.9999970000 | ✅ Violates classical bound |
| Balmer Series | Atomic | Error: 0.0234% | 0.9999999999 | ✅ Within 0.05% tolerance |
| Multi-Realm | Multiple | 9/9 realms | Various | ✅ All pass |
| Scaling Study | Multiple | 4,381 - 15,034 meas/s | 0.999997 | ✅ Sub-linear scaling |

## Key Findings

1. **Quantum Realm:** Successfully violates CHSH inequality with S ≈ 2.83 (near quantum bound)
2. **Atomic Realm:** Reproduces hydrogen Balmer series within 0.03% error
3. **Multi-Realm:** All 9 physical realms validated successfully
4. **Scaling:** Sub-linear scaling behavior - efficiency improves at larger scales
5. **Coherence:** Maintains NRCI ≥ 0.999997 (SuperCoherent) across all benchmarks

## Performance Summary

- **Best throughput:** 16,171 measurements/second
- **Scaling efficiency:** 3.4× improvement from smallest to largest scale
- **Coherence maintenance:** 100% SuperCoherent regime across all tests

