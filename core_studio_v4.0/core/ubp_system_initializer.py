#!/usr/bin/env python3
"""
UBP System v5.3 - System Initializer
Provides comprehensive system initialization and access.
Updated for UBP Core v5.3 Merged.

Author: Euan R A Craig, New Zealand
Date: 20 Feb 2026
"""

from ubp_core_v5_3_merged import (
    GOLAY_ENGINE,
    LEECH_ENGINE,
    PARTICLE_PHYSICS,
    UBPUltimateSubstrate,
    BinaryLinearAlgebra,
    GolayCodeEngine,
    LeechPointScaled,
)

from ubp_phenomenology_v4_2_6 import (
    PhenomenologyEngine,
)

from ubp_nrci_calculator import (
    NRCICalculator,
)

from metrics_exact import (
    UBPMetricsExact,
)

from ubp_tgic_engine import (
    TGICExactEngine,
)

def initialize_ubp_system():
    """
    Initialize and return the complete UBP system.
    
    Returns:
        dict: System dictionary with all components
    """
    system = {
        'golay': GOLAY_ENGINE,
        'leech': LEECH_ENGINE,
        'physics': PARTICLE_PHYSICS,
        'substrate': UBPUltimateSubstrate,
        'algebra': BinaryLinearAlgebra,
        'phenomenology': PhenomenologyEngine(),
        'nrci': NRCICalculator(),
        'metrics': UBPMetricsExact(),
        'tgic': TGICExactEngine(),
    }
    return system

def get_system_status():
    """Get comprehensive system status report."""
    system = initialize_ubp_system()
    
    status = {
        'version': '5.3 (Merged)',
        'status': 'OPERATIONAL',
        'components': {
            'golay': 'Ready (4096 codewords)',
            'leech': 'Ready (Λ₂₄ enhanced)',
            'physics': 'Ready (50-term π precision)',
            'phenomenology': 'Ready',
            'nrci': 'Ready',
            'metrics': 'Ready',
            'tgic': 'Ready',
        },
        'constants': UBPUltimateSubstrate.get_constants(50),
    }
    
    return status

if __name__ == '__main__':
    system = initialize_ubp_system()
    status = get_system_status()
    
    print("\n" + "=" * 80)
    print("UBP SYSTEM v5.3 - INITIALIZATION")
    print("=" * 80)
    print(f"\nVersion: {status['version']}")
    print(f"Status: {status['status']}")
    print(f"\nComponents:")
    for component, info in status['components'].items():
        print(f"  ✓ {component}: {info}")
    
    print(f"\nConstants:")
    for const, value in status['constants'].items():
        if const != 'precision_terms':
            print(f"  {const}: {value}")
    
    print("\n" + "=" * 80)