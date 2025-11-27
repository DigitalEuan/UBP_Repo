#!/usr/bin/env python3.11
"""Comprehensive test of all migrated modules in realms, utils, and analysis"""
import sys
sys.path.insert(0, '.')

print("="*80)
print("COMPREHENSIVE TEST OF MIGRATED FOLDERS")
print("="*80)

# Test all 9 realms
realms = [
    'quantum_realm',
    'atomic_realm', 
    'electromagnetic_realm',
    'optical_realm',
    'nuclear_realm',
    'gravitational_realm',
    'biological_realm',
    'plasma_realm',
    'cosmological_realm'
]

# Test all utils
utils = [
    'geometric_codex',
    'geometric_operations',
    'hex_dictionary',
    'metrics',
    'tgic',
    'toggle_ops',
    'crv_database',
    'runtime',
    'kernels',
    'ubp_config',
    'ubp_pattern_library',
    'global_coherence'
]

# Test analysis
analysis = [
    'spectral_extraction',
    'enhanced_nrci'
]

passed = 0
failed = 0
errors = []

print("\n--- TESTING REALMS (9 modules) ---")
for realm in realms:
    try:
        mod = __import__(f'realms.{realm}', fromlist=['*'])
        print(f"✓ {realm}")
        passed += 1
    except Exception as e:
        print(f"✗ {realm}: {e}")
        errors.append((realm, str(e)))
        failed += 1

print("\n--- TESTING UTILS (12 modules) ---")
for util in utils:
    try:
        mod = __import__(f'utils.{util}', fromlist=['*'])
        print(f"✓ {util}")
        passed += 1
    except Exception as e:
        print(f"✗ {util}: {e}")
        errors.append((util, str(e)))
        failed += 1

print("\n--- TESTING ANALYSIS (2 modules) ---")
for analysis_mod in analysis:
    try:
        mod = __import__(f'analysis.{analysis_mod}', fromlist=['*'])
        print(f"✓ {analysis_mod}")
        passed += 1
    except Exception as e:
        print(f"✗ {analysis_mod}: {e}")
        errors.append((analysis_mod, str(e)))
        failed += 1

print("\n" + "="*80)
print(f"RESULTS: {passed} passed, {failed} failed out of 23 modules")
print("="*80)

if errors:
    print("\nERRORS FOUND:")
    for name, error in errors:
        print(f"  {name}: {error}")

sys.exit(0 if failed == 0 else 1)
