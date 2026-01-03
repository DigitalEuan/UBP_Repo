#!/usr/bin/env python3
"""
Step 1: Environment Setup and Validation
Tests UBP system imports and basic functionality.
"""

import sys
import os
from pathlib import Path

print("="*80)
print("STEP 1: ENVIRONMENT SETUP AND VALIDATION")
print("="*80)

# Add UBP system to path
ubp_path = Path("/app/sandbox/session_20260102_222825_9c4bac117ac1/user_data/UBP_v4.2.6_Polished/ubp_clean")
sys.path.insert(0, str(ubp_path))

print(f"\n[1/4] Testing Python version...")
print(f"  Python version: {sys.version}")
assert sys.version_info >= (3, 11), "Python 3.11+ required"
print("  ✓ Python version OK")

print(f"\n[2/4] Testing UBP system imports...")
try:
    # Import core UBP modules
    from ubp_core_v4_2_6_COMBINED import (
        UBPUltimateSubstrate,
        GolayCodeEngine,
        LeechPointScaled,
        BinaryLinearAlgebra
    )
    print("  ✓ UBP Core imported successfully")

    from ubp_phenomenology_v4_2_6 import (
        PhenomenologyEngine,
        PhenomenonDefinition,
        DEF_SEMANTIC_HASH
    )
    print("  ✓ Phenomenology Engine imported successfully")

    from ubp_integration_adapter import UBP_INTEGRATION
    print("  ✓ Integration Adapter imported successfully")

except ImportError as e:
    print(f"  ✗ Import failed: {e}")
    sys.exit(1)

print(f"\n[3/4] Testing basic UBP functionality...")
try:
    # Test 1: Create Golay engine
    golay = GolayCodeEngine()
    print(f"  ✓ Golay engine initialized ({len(golay.get_all_codewords())} codewords)")

    # Test 2: Test phenomenology engine
    engine = PhenomenologyEngine()
    test_result = engine.process_phenomenon(
        DEF_SEMANTIC_HASH,
        {"value": "TestChemical"}
    )
    print(f"  ✓ Phenomenology engine test passed")
    print(f"    - NRCI: {test_result['metrics']['nrci']:.4f}")
    print(f"    - Symmetry Tax: {test_result['metrics']['symmetry_tax']:.4f}")
    print(f"    - Stability Score: {test_result['metrics']['stability_score']:.4f}")

except Exception as e:
    print(f"  ✗ UBP test failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print(f"\n[4/4] Verifying directory structure...")
session_dir = Path("/app/sandbox/session_20260102_222825_9c4bac117ac1")
dirs = ["workflow", "data", "figures", "results", "reports", "logs"]
for d in dirs:
    dir_path = session_dir / d
    if dir_path.exists():
        print(f"  ✓ {d}/ exists")
    else:
        print(f"  ! {d}/ does not exist (this is OK, will be created as needed)")

print("\n" + "="*80)
print("ENVIRONMENT SETUP COMPLETE - ALL TESTS PASSED")
print("="*80)
print("\nKey information:")
print(f"  - Python: {sys.version.split()[0]}")
print(f"  - UBP Core: v4.2.6")
print(f"  - Golay Codewords: 4096")
print(f"  - Session: /app/sandbox/session_20260102_222825_9c4bac117ac1")
print("\nReady to proceed with chemical analysis.")
