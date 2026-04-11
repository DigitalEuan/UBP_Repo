import json
import os
import importlib
import ubp_python_engine

# ==========================================
# CONFIGURATION
# ==========================================
TARGET_FILE = 'ubp_fom_manager_v2_evolved.py'  # Change this to any file in your workspace
OUTPUT_SUFFIX = '_evolved.py'
# ==========================================

def run_evolution():
    # 1. Force reload the engine to ensure we have the latest logic
    importlib.reload(ubp_python_engine)
    engine = ubp_python_engine.UBPPythonEngine()

    if not os.path.exists(TARGET_FILE):
        print(f"❌ Error: Target file '{TARGET_FILE}' not found.")
        return

    print(f"\n{'='*80}")
    print(f"UBP EVOLUTION PROTOCOL: Analyzing '{TARGET_FILE}'")
    print(f"{'='*80}")

    # 2. Load the source code
    with open(TARGET_FILE, 'r', encoding='utf-8') as f:
        source_code = f.read()

    # 3. Perform the Improvement Analysis
    # Note: We removed 'execute' to match the v1.6 UPCE signature
    try:
        reflection = engine.improve(source_code, verbose=True)
    except TypeError:
        # Fallback for older versions if necessary
        reflection = engine.improve(source_code)

    # 4. Report Findings
    print("\n" + "="*80)
    print("EVOLUTION REPORT")
    print("="*80)

    # Handle both object-based and dict-based results
    issues = getattr(reflection, 'issues_found', [])
    nrci_before = getattr(reflection, 'nrci_before', 0.0)
    nrci_after = getattr(reflection, 'nrci_after', 0.0)
    improved_code = getattr(reflection, 'improved_code', source_code)

    print(f"Total Issues Detected: {len(issues)}")
    for i, issue in enumerate(issues[:10]): # Show first 10
        print(f"  [{i+1}] {issue}")
    if len(issues) > 10:
        print(f"  ... and {len(issues)-10} more.")

    print(f"\nInternal Stability (NRCI): {nrci_before:.4f} -> {nrci_after:.4f}")

    # 5. Save the Evolved Output
    output_path = TARGET_FILE.replace('.py', OUTPUT_SUFFIX)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(improved_code)

    print(f"\n✅ Evolution complete. Result saved to: '{output_path}'")
    print(f"{'='*80}\n")

if __name__ == "__main__":
    run_evolution()