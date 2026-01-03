#!/usr/bin/env python3
"""
OffBits UBP Analysis - Setup and Environment
================================================
Initialize environment and download large chemical dataset
"""

import sys
import json
from pathlib import Path
import importlib.util

# Setup paths
BASE_DIR = Path("/app/sandbox/session_20260102_222825_9c4bac117ac1")
UBP_DIR = BASE_DIR / "user_data" / "UBP_v4.2.6_Polished" / "ubp_clean"
sys.path.insert(0, str(UBP_DIR))

print("=" * 70)
print("OFFBITS UBP ANALYSIS - ENVIRONMENT SETUP")
print("=" * 70)

# Check Python version
print(f"\n[1/5] Python version: {sys.version}")
assert sys.version_info >= (3, 12), "Python 3.12+ required"
print("✓ Python version OK")

# Check required packages
print("\n[2/5] Checking required packages...")
required_packages = {
    'numpy': 'numpy',
    'pandas': 'pandas',
    'matplotlib': 'matplotlib.pyplot',
    'scipy': 'scipy.stats',
    'sklearn': 'sklearn',
}

available_packages = {}
for name, import_name in required_packages.items():
    try:
        spec = importlib.util.find_spec(import_name.split('.')[0])
        if spec is not None:
            available_packages[name] = True
            print(f"  ✓ {name}")
        else:
            available_packages[name] = False
            print(f"  ✗ {name} - NOT FOUND")
    except Exception as e:
        available_packages[name] = False
        print(f"  ✗ {name} - ERROR: {e}")

# Check UBP system
print("\n[3/5] Checking UBP system files...")
ubp_files = [
    "ubp_core_v4_2_6_COMBINED.py",
    "metrics_exact.py",
    "hex_dictionary_v4_exact.py",
    "tgic_engine_exact.py",
    "ubp_handshake_v4_2_6.py"
]

for fname in ubp_files:
    fpath = UBP_DIR / fname
    if fpath.exists():
        print(f"  ✓ {fname}")
    else:
        print(f"  ✗ {fname} - MISSING")

# Create directory structure
print("\n[4/5] Creating directory structure...")
dirs = [
    "workflow",
    "data/fingerprints",
    "data/raw",
    "figures/offbits",
    "results/iterations",
    "logs"
]

for dirname in dirs:
    dirpath = BASE_DIR / dirname
    dirpath.mkdir(parents=True, exist_ok=True)
    print(f"  ✓ {dirname}/")

# Test UBP imports
print("\n[5/5] Testing UBP imports...")
try:
    from ubp_core_v4_2_6_COMBINED import UBPUltimateSubstrate
    print("  ✓ UBP Core imported successfully")

    # Test basic functionality
    constants = UBPUltimateSubstrate.get_constants(precision=50)
    print(f"  ✓ Y-constant: {float(constants['Y']):.6f}")
    print(f"  ✓ Alpha anchor: {constants['alpha_anchor']}")
    print(f"  ✓ Omega anchor: {constants['omega_anchor']}")

except Exception as e:
    print(f"  ✗ UBP import failed: {e}")
    sys.exit(1)

# Save environment info
env_info = {
    "python_version": sys.version,
    "base_dir": str(BASE_DIR),
    "ubp_dir": str(UBP_DIR),
    "packages": available_packages,
    "status": "ready"
}

env_file = BASE_DIR / "logs" / "environment_info.json"
with open(env_file, 'w') as f:
    json.dump(env_info, f, indent=2)

print("\n" + "=" * 70)
print("✓ ENVIRONMENT SETUP COMPLETE")
print("=" * 70)
print(f"\nEnvironment info saved to: {env_file}")
print("\nNext step: Run 02_data_acquisition_large.py to download dataset")
