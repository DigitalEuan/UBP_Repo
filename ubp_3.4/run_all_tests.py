#!/usr/bin/env python3.11
"""
UBP 3.4 Comprehensive Test Runner
==================================

Runs all 18 examples and generates a validation report.

Author: Euan R A Craig, New Zealand
Date: 31 October 2025
"""

import os
import sys
import subprocess
import json
import time
from datetime import datetime

def run_example(example_path):
    """Run a single example and return results."""
    start_time = time.time()
    try:
        result = subprocess.run(
            [sys.executable, example_path],
            capture_output=True,
            text=True,
            timeout=30
        )
        elapsed = time.time() - start_time
        
        return {
            'path': example_path,
            'success': result.returncode == 0,
            'stdout': result.stdout,
            'stderr': result.stderr,
            'elapsed_seconds': elapsed
        }
    except subprocess.TimeoutExpired:
        return {
            'path': example_path,
            'success': False,
            'stdout': '',
            'stderr': 'TIMEOUT',
            'elapsed_seconds': 30.0
        }
    except Exception as e:
        return {
            'path': example_path,
            'success': False,
            'stdout': '',
            'stderr': str(e),
            'elapsed_seconds': 0.0
        }

def main():
    print("=" * 80)
    print("UBP 3.4 COMPREHENSIVE TEST SUITE")
    print("=" * 80)
    print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Find all example files
    examples_dir = '/home/ubuntu/ubp_3.3/examples'
    example_files = []
    
    for root, dirs, files in os.walk(examples_dir):
        for file in files:
            if file.startswith('example_') and file.endswith('.py'):
                example_files.append(os.path.join(root, file))
    
    example_files.sort()
    
    print(f"Found {len(example_files)} examples to test\n")
    
    results = []
    passed = 0
    failed = 0
    
    for i, example_path in enumerate(example_files, 1):
        realm = os.path.basename(os.path.dirname(example_path))
        example_name = os.path.basename(example_path)
        
        print(f"[{i}/{len(example_files)}] Testing {realm}/{example_name}...", end=' ', flush=True)
        
        result = run_example(example_path)
        results.append(result)
        
        if result['success']:
            print(f"✓ PASSED ({result['elapsed_seconds']:.2f}s)")
            passed += 1
        else:
            print(f"✗ FAILED")
            failed += 1
            if result['stderr']:
                print(f"    Error: {result['stderr'][:100]}")
    
    print("\n" + "=" * 80)
    print("TEST SUMMARY")
    print("=" * 80)
    print(f"Total Tests: {len(example_files)}")
    print(f"Passed: {passed} ({100*passed/len(example_files):.1f}%)")
    print(f"Failed: {failed}")
    print()
    
    # Save detailed results
    report_file = '/home/ubuntu/ubp_3.3/examples/TEST_REPORT.json'
    with open(report_file, 'w') as f:
        json.dump({
            'timestamp': datetime.now().isoformat(),
            'total_tests': len(example_files),
            'passed': passed,
            'failed': failed,
            'results': results
        }, f, indent=2)
    
    print(f"Detailed report saved to: {report_file}")
    
    # Check results directory
    results_dir = '/home/ubuntu/ubp_3.3/examples/results'
    result_files = [f for f in os.listdir(results_dir) if f.endswith('.json')]
    
    print(f"\nGenerated {len(result_files)} result files:")
    for rf in sorted(result_files):
        print(f"  - {rf}")
    
    print("\n" + "=" * 80)
    if failed == 0:
        print("✓ ALL TESTS PASSED")
    else:
        print(f"⚠ {failed} TEST(S) FAILED")
    print("=" * 80)
    
    return passed == len(example_files)

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
