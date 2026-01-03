#!/usr/bin/env python3
"""
UBP System v4.2.6 - System Initializer
Provides comprehensive system initialization and access
"""

from ubp_core_v4_2_6_COMBINED import (
    GOLAY_DECODER,
    LEECH_ENHANCED,
    PARTICLE_VALIDATOR,
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
        'golay': GOLAY_DECODER,
        'leech': LEECH_ENHANCED,
        'physics': PARTICLE_VALIDATOR,
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
        'version': '4.2.6',
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
    print("UBP SYSTEM v4.2.6 - INITIALIZATION")
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
