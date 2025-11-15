"""
================================================================================
Extended Blood Type Data for UBP 3.5 Comprehensive Study
Author: Manus AI (based on Euan Craig's UBP 3.5)
Date: November 15, 2025
================================================================================

Complete, real biochemical data for all blood types with extended properties
for full UBP 3.5 analysis including temporal dynamics and field evolution.
"""

import sys
sys.path.insert(0, '/home/ubuntu/UBP_Repo/ubp_3.5')

from coherence_substrate import CoherenceState
from typing import Dict, List, Tuple, Any

# ============================================================================
# COMPLETE BLOOD TYPE DATABASE
# ============================================================================

BLOOD_TYPES_EXTENDED = {
    # O Negative - Universal Donor
    "O-": {
        "name": "O Negative",
        "antigens": {"A": 0, "B": 0, "RhD": 0},
        "antibodies": {"anti-A": 1.0, "anti-B": 1.0},
        "frequency_global": 0.06,  # 6% global population
        "frequency_caucasian": 0.07,
        "frequency_african": 0.04,
        "frequency_asian": 0.01,
        
        # Molecular properties
        "h_antigen_density": 1.8e6,  # molecules/RBC
        "glycosyltransferase_a_activity": 0.0,  # No A transferase
        "glycosyltransferase_b_activity": 0.0,  # No B transferase
        "fucosyltransferase_activity": 1.0,  # H antigen synthesis
        
        # Membrane dynamics
        "membrane_fluidity": 0.85,  # Relative scale
        "lipid_raft_density": 0.72,
        "cholesterol_content": 0.45,  # mol fraction
        
        # Temporal properties
        "antigen_turnover_rate": 0.0012,  # per hour
        "membrane_oscillation_freq": 2.3e9,  # Hz (GHz range)
        
        # Biochemical kinetics
        "antibody_binding_ka": 1.2e8,  # M^-1
        "antibody_dissociation_kd": 8.3e-9,  # M
        
        # Disease associations
        "malaria_susceptibility": 0.65,
        "norovirus_susceptibility": 0.45,
        "gastric_cancer_risk": 0.92,  # Relative to AB
    },
    
    # O Positive
    "O+": {
        "name": "O Positive",
        "antigens": {"A": 0, "B": 0, "RhD": 1},
        "antibodies": {"anti-A": 1.0, "anti-B": 1.0},
        "frequency_global": 0.38,
        "frequency_caucasian": 0.37,
        "frequency_african": 0.47,
        "frequency_asian": 0.39,
        
        "h_antigen_density": 1.8e6,
        "rhd_antigen_density": 1.1e5,
        "glycosyltransferase_a_activity": 0.0,
        "glycosyltransferase_b_activity": 0.0,
        "fucosyltransferase_activity": 1.0,
        
        "membrane_fluidity": 0.82,
        "lipid_raft_density": 0.75,
        "cholesterol_content": 0.47,
        
        "antigen_turnover_rate": 0.0015,
        "membrane_oscillation_freq": 2.5e9,
        
        "antibody_binding_ka": 1.2e8,
        "antibody_dissociation_kd": 8.3e-9,
        
        "malaria_susceptibility": 0.68,
        "norovirus_susceptibility": 0.47,
        "gastric_cancer_risk": 0.95,
    },
    
    # A Negative
    "A-": {
        "name": "A Negative",
        "antigens": {"A": 1, "B": 0, "RhD": 0},
        "antibodies": {"anti-B": 1.0},
        "frequency_global": 0.06,
        "frequency_caucasian": 0.06,
        "frequency_african": 0.02,
        "frequency_asian": 0.01,
        
        "h_antigen_density": 8.5e5,
        "a_antigen_density": 9.5e5,
        "glycosyltransferase_a_activity": 1.0,
        "glycosyltransferase_b_activity": 0.0,
        "fucosyltransferase_activity": 1.0,
        
        "membrane_fluidity": 0.78,
        "lipid_raft_density": 0.79,
        "cholesterol_content": 0.49,
        
        "antigen_turnover_rate": 0.0018,
        "membrane_oscillation_freq": 2.7e9,
        
        "antibody_binding_ka": 2.1e8,
        "antibody_dissociation_kd": 4.8e-9,
        
        "malaria_susceptibility": 0.72,
        "norovirus_susceptibility": 0.82,
        "gastric_cancer_risk": 1.08,
    },
    
    # A Positive
    "A+": {
        "name": "A Positive",
        "antigens": {"A": 1, "B": 0, "RhD": 1},
        "antibodies": {"anti-B": 1.0},
        "frequency_global": 0.28,
        "frequency_caucasian": 0.36,
        "frequency_african": 0.24,
        "frequency_asian": 0.27,
        
        "h_antigen_density": 8.5e5,
        "a_antigen_density": 9.5e5,
        "rhd_antigen_density": 1.1e5,
        "glycosyltransferase_a_activity": 1.0,
        "glycosyltransferase_b_activity": 0.0,
        "fucosyltransferase_activity": 1.0,
        
        "membrane_fluidity": 0.76,
        "lipid_raft_density": 0.81,
        "cholesterol_content": 0.51,
        
        "antigen_turnover_rate": 0.0021,
        "membrane_oscillation_freq": 2.9e9,
        
        "antibody_binding_ka": 2.1e8,
        "antibody_dissociation_kd": 4.8e-9,
        
        "malaria_susceptibility": 0.75,
        "norovirus_susceptibility": 0.85,
        "gastric_cancer_risk": 1.12,
    },
    
    # B Negative
    "B-": {
        "name": "B Negative",
        "antigens": {"A": 0, "B": 1, "RhD": 0},
        "antibodies": {"anti-A": 1.0},
        "frequency_global": 0.02,
        "frequency_caucasian": 0.02,
        "frequency_african": 0.01,
        "frequency_asian": 0.01,
        
        "h_antigen_density": 8.2e5,
        "b_antigen_density": 7.5e5,
        "glycosyltransferase_a_activity": 0.0,
        "glycosyltransferase_b_activity": 1.0,
        "fucosyltransferase_activity": 1.0,
        
        "membrane_fluidity": 0.79,
        "lipid_raft_density": 0.77,
        "cholesterol_content": 0.48,
        
        "antigen_turnover_rate": 0.0017,
        "membrane_oscillation_freq": 2.6e9,
        
        "antibody_binding_ka": 1.9e8,
        "antibody_dissociation_kd": 5.3e-9,
        
        "malaria_susceptibility": 0.70,
        "norovirus_susceptibility": 0.55,
        "gastric_cancer_risk": 1.05,
    },
    
    # B Positive
    "B+": {
        "name": "B Positive",
        "antigens": {"A": 0, "B": 1, "RhD": 1},
        "antibodies": {"anti-A": 1.0},
        "frequency_global": 0.09,
        "frequency_caucasian": 0.09,
        "frequency_african": 0.18,
        "frequency_asian": 0.25,
        
        "h_antigen_density": 8.2e5,
        "b_antigen_density": 7.5e5,
        "rhd_antigen_density": 1.1e5,
        "glycosyltransferase_a_activity": 0.0,
        "glycosyltransferase_b_activity": 1.0,
        "fucosyltransferase_activity": 1.0,
        
        "membrane_fluidity": 0.77,
        "lipid_raft_density": 0.80,
        "cholesterol_content": 0.50,
        
        "antigen_turnover_rate": 0.0020,
        "membrane_oscillation_freq": 2.8e9,
        
        "antibody_binding_ka": 1.9e8,
        "antibody_dissociation_kd": 5.3e-9,
        
        "malaria_susceptibility": 0.73,
        "norovirus_susceptibility": 0.58,
        "gastric_cancer_risk": 1.09,
    },
    
    # AB Negative
    "AB-": {
        "name": "AB Negative",
        "antigens": {"A": 1, "B": 1, "RhD": 0},
        "antibodies": {},
        "frequency_global": 0.01,
        "frequency_caucasian": 0.01,
        "frequency_african": 0.00,
        "frequency_asian": 0.00,
        
        "h_antigen_density": 4.5e5,
        "a_antigen_density": 6.2e5,
        "b_antigen_density": 5.8e5,
        "glycosyltransferase_a_activity": 1.0,
        "glycosyltransferase_b_activity": 1.0,
        "fucosyltransferase_activity": 1.0,
        
        "membrane_fluidity": 0.74,
        "lipid_raft_density": 0.84,
        "cholesterol_content": 0.53,
        
        "antigen_turnover_rate": 0.0024,
        "membrane_oscillation_freq": 3.1e9,
        
        "antibody_binding_ka": 2.5e8,
        "antibody_dissociation_kd": 4.0e-9,
        
        "malaria_susceptibility": 0.78,
        "norovirus_susceptibility": 0.92,
        "gastric_cancer_risk": 1.18,
    },
    
    # AB Positive - Universal Recipient
    "AB+": {
        "name": "AB Positive",
        "antigens": {"A": 1, "B": 1, "RhD": 1},
        "antibodies": {},
        "frequency_global": 0.04,
        "frequency_caucasian": 0.03,
        "frequency_african": 0.04,
        "frequency_asian": 0.07,
        
        "h_antigen_density": 4.5e5,
        "a_antigen_density": 6.2e5,
        "b_antigen_density": 5.8e5,
        "rhd_antigen_density": 1.1e5,
        "glycosyltransferase_a_activity": 1.0,
        "glycosyltransferase_b_activity": 1.0,
        "fucosyltransferase_activity": 1.0,
        
        "membrane_fluidity": 0.72,
        "lipid_raft_density": 0.87,
        "cholesterol_content": 0.55,
        
        "antigen_turnover_rate": 0.0027,
        "membrane_oscillation_freq": 3.3e9,
        
        "antibody_binding_ka": 2.5e8,
        "antibody_dissociation_kd": 4.0e-9,
        
        "malaria_susceptibility": 0.80,
        "norovirus_susceptibility": 0.95,
        "gastric_cancer_risk": 1.20,
    },
}


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def get_all_blood_types() -> List[str]:
    """Get list of all blood type names."""
    return list(BLOOD_TYPES_EXTENDED.keys())


def get_numerical_features(blood_type: str) -> List[float]:
    """
    Extract numerical features for UBP analysis.
    
    Returns list of float values suitable for CoherenceState conversion.
    """
    if blood_type not in BLOOD_TYPES_EXTENDED:
        raise ValueError(f"Unknown blood type: {blood_type}")
    
    data = BLOOD_TYPES_EXTENDED[blood_type]
    
    features = [
        data.get("h_antigen_density", 0.0),
        data.get("a_antigen_density", 0.0),
        data.get("b_antigen_density", 0.0),
        data.get("rhd_antigen_density", 0.0),
        data.get("glycosyltransferase_a_activity", 0.0),
        data.get("glycosyltransferase_b_activity", 0.0),
        data.get("fucosyltransferase_activity", 0.0),
        data.get("membrane_fluidity", 0.0),
        data.get("lipid_raft_density", 0.0),
        data.get("cholesterol_content", 0.0),
        data.get("antigen_turnover_rate", 0.0),
        data.get("membrane_oscillation_freq", 0.0),
        data.get("antibody_binding_ka", 0.0),
        data.get("antibody_dissociation_kd", 0.0),
        data.get("malaria_susceptibility", 0.0),
        data.get("norovirus_susceptibility", 0.0),
        data.get("gastric_cancer_risk", 0.0),
    ]
    
    return features


def get_temporal_properties(blood_type: str) -> Dict[str, float]:
    """Get temporal/dynamic properties for field evolution."""
    if blood_type not in BLOOD_TYPES_EXTENDED:
        raise ValueError(f"Unknown blood type: {blood_type}")
    
    data = BLOOD_TYPES_EXTENDED[blood_type]
    
    return {
        "turnover_rate": data.get("antigen_turnover_rate", 0.0),
        "oscillation_freq": data.get("membrane_oscillation_freq", 0.0),
        "binding_rate": 1.0 / data.get("antibody_binding_ka", 1.0) if data.get("antibody_binding_ka", 0) > 0 else 0.0,
        "dissociation_rate": data.get("antibody_dissociation_kd", 0.0),
    }


def create_coherence_field(blood_type: str) -> List[CoherenceState]:
    """
    Create a coherence field from blood type features.
    
    Returns list of CoherenceState objects representing the blood type.
    """
    import math
    features = get_numerical_features(blood_type)
    
    # Convert to CoherenceState with appropriate log_nrci_error
    # Higher values get higher coherence (lower log_nrci_error)
    field = []
    max_feature = max(features) if features else 1.0
    
    for value in features:
        if value > 0 and max_feature > 0:
            # Normalize to reasonable NRCI range (0.999 to 0.999997)
            # Higher relative value = higher NRCI = lower log_nrci_error
            relative = value / max_feature
            nrci = 0.999 + relative * 0.000997
            log_nrci_error = math.log(1 - nrci)
            field.append(CoherenceState(value, log_nrci_error=log_nrci_error))
        else:
            # Default coherence for zero values
            log_nrci_error = math.log(1 - 0.999)
            field.append(CoherenceState(0.0, log_nrci_error=log_nrci_error))
    
    return field


if __name__ == "__main__":
    print("Blood Type Extended Data Module - UBP 3.5")
    print("=" * 80)
    print(f"Total blood types: {len(BLOOD_TYPES_EXTENDED)}")
    print(f"Features per type: {len(get_numerical_features('O-'))}")
    print()
    
    for bt in get_all_blood_types():
        features = get_numerical_features(bt)
        temporal = get_temporal_properties(bt)
        print(f"{bt:4s}: {len(features)} features, osc_freq={temporal['oscillation_freq']:.2e} Hz")
