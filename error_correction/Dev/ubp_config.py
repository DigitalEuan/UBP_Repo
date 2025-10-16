"""
# ubp_config.py

# Global System Configurations
SYSTEM_NAME = "UBP Error Correction System"
SYSTEM_VERSION = "1.0.0"
AUTHOR = "Euan Craig, New Zealand"
DEBUG_MODE = True
"""

# NRCI Configurations
NRCI_THRESHOLD_BASIC = 0.5
NRCI_THRESHOLD_GLR_ENHANCED = 0.7
NRCI_TEMPORAL_DECAY_RATE = 0.1
NRCI_FEEDBACK_GAIN = 0.2

# GLR Framework Configurations
GLR_CONFIG = {
    "level_thresholds": {
        "BASIC_CHECKS": 0.1,
        "CLASSICAL_ECC": 0.2,
        "GEOMETRIC_2D": 0.3,
        "GEOMETRIC_3D": 0.4,
        "NRCI_FEEDBACK": 0.5,
        "P_ADIC_CORRECTION": 0.6,
        "GLOBAL_GOLAY_24": 0.7,
        "TGIC_STRUCTURAL": 0.8,
        "ADAPTIVE_FIBONACCI": 0.9,
    },
    "max_retries_per_level": 3,
    "escalation_strategy": "sequential", # or "adaptive"
}

# Geometric Correction Configurations
GEOMETRIC_2D_TOLERANCE = 0.05
GEOMETRIC_3D_TOLERANCE = 0.08
SUPERFORMULA_DEFAULT_M = 4
SUPERFORMULA_DEFAULT_N1 = 1
SUPERFORMULA_DEFAULT_N2 = 1
SUPERFORMULA_DEFAULT_N3 = 1
SUPERFORMULA_SPRING_FACTOR = 0.1 # Factor for dynamic expansion

# Classical ECC Configurations
HAMMING_CODE_K = 4
HAMMING_CODE_N = 7
BCH_CODE_N = 31
BCH_CODE_K = 21

# P-Adic and Adelic Configurations
P_ADIC_DEFAULT_P = 7
P_ADIC_PRECISION = 5
ADELIC_ARCHIMEDEAN_WEIGHT = 0.5
ADELIC_NON_ARCHIMEDEAN_WEIGHT = 0.5

# TGIC System Configurations
TGIC_CONSTRAINT_STRENGTH = 0.1
TGIC_OPTIMIZATION_ITERATIONS = 100

# Error Correction Result Codes
ERROR_CODES = {
    "NO_ERROR": 0,
    "DETECTED_BUT_UNCORRECTED": 1,
    "CORRECTED_BASIC_ECC": 2,
    "CORRECTED_GEOMETRIC_2D": 3,
    "CORRECTED_GEOMETRIC_3D": 4,
    "CORRECTED_P_ADIC": 5,
    "CORRECTED_GLOBAL_GOLAY": 6,
    "CORRECTED_TGIC": 7,
    "CORRECTED_FIBONACCI": 8,
    "ESCALATED_TO_HIGHER_LEVEL": 9,
}
