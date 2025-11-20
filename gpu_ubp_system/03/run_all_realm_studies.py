"""
Multi-Realm Scientific Studies - Complete Validation
====================================================

Run all 9 real-world scientific studies to validate the GPU UBP system.

Each study tests a well-known physical phenomenon and compares UBP predictions
to experimental/observational data.

Author: Euan Craig, New Zealand
Date: November 21, 2025
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'ubp_core'))

import subprocess
import json
import time
from typing import Dict, List


class MultiRealmStudyRunner:
    """Runner for all realm studies."""

    STUDIES = [
        {
            'realm': 'quantum',
            'name': 'CHSH Entanglement Test',
            'script': 'study_chsh_quantum.py',
            'args': ['--backend', 'cpu', '--trials', '10', '--measurements', '2000',
                     '--propagation', '10', '--export', 'chsh_results.json'],
            'status': 'implemented'
        },
        {
            'realm': 'atomic',
            'name': 'Hydrogen Balmer Series',
            'script': 'study_atomic_balmer.py',
            'args': [],
            'status': 'implemented'
        },
        {
            'realm': 'electromagnetic',
            'name': 'Microwave Cavity Resonance',
            'script': 'study_em_cavity.py',
            'args': [],
            'status': 'pending'
        },
        {
            'realm': 'optical',
            'name': 'Double-Slit Interference',
            'script': 'study_optical_doubleslit.py',
            'args': [],
            'status': 'pending'
        },
        {
            'realm': 'nuclear',
            'name': 'U-238 Alpha Decay',
            'script': 'study_nuclear_decay.py',
            'args': [],
            'status': 'pending'
        },
        {
            'realm': 'gravitational',
            'name': 'Binary Pulsar Decay',
            'script': 'study_grav_pulsar.py',
            'args': [],
            'status': 'pending'
        },
        {
            'realm': 'biological',
            'name': 'Enzyme Proton Tunneling',
            'script': 'study_bio_enzyme.py',
            'args': [],
            'status': 'pending'
        },
        {
            'realm': 'plasma',
            'name': 'Tokamak Plasma Frequency',
            'script': 'study_plasma_tokamak.py',
            'args': [],
            'status': 'pending'
        },
        {
            'realm': 'cosmological',
            'name': 'CMB Power Spectrum',
            'script': 'study_cosmo_cmb.py',
            'args': [],
            'status': 'pending'
        }
    ]

    def __init__(self):
        """Initialize runner."""
        self.results = []

        print("=" * 70)
        print("MULTI-REALM SCIENTIFIC STUDIES")
        print("=" * 70)
        print("Running all 9 real-world validation studies...")
        print()

    def run_study(self, study: Dict) -> Dict:
        """Run a single study."""
        print(f"{'=' * 70}")
        print(f"REALM: {study['realm'].upper()}")
        print(f"STUDY: {study['name']}")
        print(f"{'=' * 70}")

        if study['status'] == 'pending':
            print(f"⏭️  SKIPPED - Study not yet implemented")
            print()
            return {
                'realm': study['realm'],
                'name': study['name'],
                'status': 'skipped',
                'reason': 'not_implemented'
            }

        # Run the study script
        start_time = time.time()

        try:
            cmd = ['python', study['script']] + study['args']
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=300  # 5 minute timeout
            )

            elapsed = time.time() - start_time

            # Check exit code
            success = (result.returncode == 0)

            # Print output
            print(result.stdout)
            if result.stderr:
                print("STDERR:", result.stderr)

            status = "✅ PASS" if success else "❌ FAIL"
            print(f"{status} - Elapsed: {elapsed:.2f}s")
            print()

            return {
                'realm': study['realm'],
                'name': study['name'],
                'status': 'pass' if success else 'fail',
                'elapsed_time': elapsed,
                'exit_code': result.returncode
            }

        except subprocess.TimeoutExpired:
            print(f"❌ TIMEOUT - Study exceeded 5 minute limit")
            print()
            return {
                'realm': study['realm'],
                'name': study['name'],
                'status': 'timeout',
                'elapsed_time': 300
            }

        except Exception as e:
            print(f"❌ ERROR - {str(e)}")
            print()
            return {
                'realm': study['realm'],
                'name': study['name'],
                'status': 'error',
                'error': str(e)
            }

    def run_all_studies(self) -> Dict:
        """Run all studies."""
        start_time = time.time()

        for study in self.STUDIES:
            result = self.run_study(study)
            self.results.append(result)

        elapsed = time.time() - start_time

        # Calculate summary
        total = len(self.results)
        passed = sum(1 for r in self.results if r['status'] == 'pass')
        failed = sum(1 for r in self.results if r['status'] == 'fail')
        skipped = sum(1 for r in self.results if r['status'] == 'skipped')

        print("=" * 70)
        print("MULTI-REALM STUDY SUMMARY")
        print("=" * 70)
        print(f"Total studies: {total}")
        print(f"✅ Passed: {passed}")
        print(f"❌ Failed: {failed}")
        print(f"⏭️  Skipped: {skipped}")
        print(f"⏱️  Total time: {elapsed:.2f} seconds")
        print("=" * 70)

        if passed == total:
            print()
            print("🎉 ALL STUDIES PASS! GPU UBP system fully validated across all realms!")
            print()
        elif passed > 0:
            print()
            print(f"✅ {passed}/{total} studies pass. System partially validated.")
            print()

        return {
            'summary': {
                'total': total,
                'passed': passed,
                'failed': failed,
                'skipped': skipped,
                'elapsed_time': elapsed
            },
            'results': self.results
        }


def main():
    """Main entry point."""
    runner = MultiRealmStudyRunner()
    results = runner.run_all_studies()

    # Export results
    with open('multi_realm_study_results.json', 'w') as f:
        json.dump(results, f, indent=2)

    print(f"✅ Results exported to multi_realm_study_results.json")

    # Exit with error if any failed
    if results['summary']['failed'] > 0:
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == '__main__':
    main()
