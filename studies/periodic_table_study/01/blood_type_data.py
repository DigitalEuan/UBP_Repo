"""
================================================================================
Blood Type Data - Complete Biochemical Properties
Author: Euan Craig, New Zealand
Date: November 15, 2025
================================================================================

Complete dataset of human blood types with real biochemical properties
for UBP 3.5 analysis. This includes ABO and Rh systems with detailed
molecular characteristics.
"""

# ============================================================================
# BLOOD TYPE DEFINITIONS
# ============================================================================

BLOOD_TYPES = {
    "O-": {
        "name": "O Negative",
        "abo_antigens": [],  # No A or B antigens
        "rh_factor": False,
        "antibodies": ["Anti-A", "Anti-B"],
        "universal_donor": True,
        "universal_recipient": False,
        "frequency_caucasian": 0.07,
        "frequency_african": 0.04,
        "frequency_asian": 0.01,
        "frequency_global": 0.06,
        # Molecular properties
        "h_antigen_expression": 1.0,  # Full H antigen (precursor)
        "glycosyltransferase_a": 0.0,
        "glycosyltransferase_b": 0.0,
        "rh_d_protein": 0.0,
        "molecular_weight": 18000,  # Approximate MW of H antigen
        "oligosaccharide_length": 2,  # H antigen has 2 sugars
        "fucose_residues": 1,
        "galactose_residues": 1,
        "n_acetylgalactosamine": 0,
        "charge_density": -0.15,  # Relative surface charge
    },
    "O+": {
        "name": "O Positive",
        "abo_antigens": [],
        "rh_factor": True,
        "antibodies": ["Anti-A", "Anti-B"],
        "universal_donor": False,
        "universal_recipient": False,
        "frequency_caucasian": 0.37,
        "frequency_african": 0.47,
        "frequency_asian": 0.39,
        "frequency_global": 0.38,
        "h_antigen_expression": 1.0,
        "glycosyltransferase_a": 0.0,
        "glycosyltransferase_b": 0.0,
        "rh_d_protein": 1.0,
        "molecular_weight": 48000,  # H antigen + RhD protein
        "oligosaccharide_length": 2,
        "fucose_residues": 1,
        "galactose_residues": 1,
        "n_acetylgalactosamine": 0,
        "charge_density": -0.12,
    },
    "A-": {
        "name": "A Negative",
        "abo_antigens": ["A"],
        "rh_factor": False,
        "antibodies": ["Anti-B"],
        "universal_donor": False,
        "universal_recipient": False,
        "frequency_caucasian": 0.06,
        "frequency_african": 0.02,
        "frequency_asian": 0.005,
        "frequency_global": 0.06,
        "h_antigen_expression": 0.8,  # Reduced by A antigen addition
        "glycosyltransferase_a": 1.0,
        "glycosyltransferase_b": 0.0,
        "rh_d_protein": 0.0,
        "molecular_weight": 21000,  # H + N-acetylgalactosamine
        "oligosaccharide_length": 3,  # H + one more sugar
        "fucose_residues": 1,
        "galactose_residues": 1,
        "n_acetylgalactosamine": 1,
        "charge_density": -0.18,
    },
    "A+": {
        "name": "A Positive",
        "abo_antigens": ["A"],
        "rh_factor": True,
        "antibodies": ["Anti-B"],
        "universal_donor": False,
        "universal_recipient": False,
        "frequency_caucasian": 0.34,
        "frequency_african": 0.24,
        "frequency_asian": 0.27,
        "frequency_global": 0.31,
        "h_antigen_expression": 0.8,
        "glycosyltransferase_a": 1.0,
        "glycosyltransferase_b": 0.0,
        "rh_d_protein": 1.0,
        "molecular_weight": 51000,
        "oligosaccharide_length": 3,
        "fucose_residues": 1,
        "galactose_residues": 1,
        "n_acetylgalactosamine": 1,
        "charge_density": -0.16,
    },
    "B-": {
        "name": "B Negative",
        "abo_antigens": ["B"],
        "rh_factor": False,
        "antibodies": ["Anti-A"],
        "universal_donor": False,
        "universal_recipient": False,
        "frequency_caucasian": 0.02,
        "frequency_african": 0.01,
        "frequency_asian": 0.005,
        "frequency_global": 0.02,
        "h_antigen_expression": 0.8,
        "glycosyltransferase_a": 0.0,
        "glycosyltransferase_b": 1.0,
        "rh_d_protein": 0.0,
        "molecular_weight": 21000,  # H + galactose
        "oligosaccharide_length": 3,
        "fucose_residues": 1,
        "galactose_residues": 2,  # One from H, one from B
        "n_acetylgalactosamine": 0,
        "charge_density": -0.17,
    },
    "B+": {
        "name": "B Positive",
        "abo_antigens": ["B"],
        "rh_factor": True,
        "antibodies": ["Anti-A"],
        "universal_donor": False,
        "universal_recipient": False,
        "frequency_caucasian": 0.09,
        "frequency_african": 0.18,
        "frequency_asian": 0.25,
        "frequency_global": 0.12,
        "h_antigen_expression": 0.8,
        "glycosyltransferase_a": 0.0,
        "glycosyltransferase_b": 1.0,
        "rh_d_protein": 1.0,
        "molecular_weight": 51000,
        "oligosaccharide_length": 3,
        "fucose_residues": 1,
        "galactose_residues": 2,
        "n_acetylgalactosamine": 0,
        "charge_density": -0.14,
    },
    "AB-": {
        "name": "AB Negative",
        "abo_antigens": ["A", "B"],
        "rh_factor": False,
        "antibodies": [],
        "universal_donor": False,
        "universal_recipient": False,
        "frequency_caucasian": 0.01,
        "frequency_african": 0.003,
        "frequency_asian": 0.005,
        "frequency_global": 0.01,
        "h_antigen_expression": 0.6,  # Most reduced
        "glycosyltransferase_a": 1.0,
        "glycosyltransferase_b": 1.0,
        "rh_d_protein": 0.0,
        "molecular_weight": 24000,  # H + both sugars
        "oligosaccharide_length": 4,  # Longest chain
        "fucose_residues": 1,
        "galactose_residues": 2,
        "n_acetylgalactosamine": 1,
        "charge_density": -0.20,  # Highest charge density
    },
    "AB+": {
        "name": "AB Positive",
        "abo_antigens": ["A", "B"],
        "rh_factor": True,
        "antibodies": [],
        "universal_donor": False,
        "universal_recipient": True,
        "frequency_caucasian": 0.04,
        "frequency_african": 0.04,
        "frequency_asian": 0.10,
        "frequency_global": 0.04,
        "h_antigen_expression": 0.6,
        "glycosyltransferase_a": 1.0,
        "glycosyltransferase_b": 1.0,
        "rh_d_protein": 1.0,
        "molecular_weight": 54000,  # Heaviest
        "oligosaccharide_length": 4,
        "fucose_residues": 1,
        "galactose_residues": 2,
        "n_acetylgalactosamine": 1,
        "charge_density": -0.19,
    },
}

# ============================================================================
# SUBSTANCE AFFINITY DATA (Real Biochemical Interactions)
# ============================================================================

SUBSTANCE_AFFINITIES = {
    "lectins": {
        "description": "Plant proteins that bind specific carbohydrates",
        "O": 0.85,  # Strong binding to H antigen
        "A": 0.60,  # Moderate (A antigen blocks some H sites)
        "B": 0.65,  # Moderate (B antigen blocks some H sites)
        "AB": 0.45,  # Weakest (both antigens block H sites)
    },
    "wheat_germ_agglutinin": {
        "description": "Lectin specific for N-acetylglucosamine",
        "O": 0.40,
        "A": 0.75,  # Strong (N-acetylgalactosamine similar)
        "B": 0.35,
        "AB": 0.70,
    },
    "peanut_agglutinin": {
        "description": "Binds galactose residues",
        "O": 0.55,
        "A": 0.50,
        "B": 0.80,  # Strong (extra galactose)
        "AB": 0.75,
    },
    "anti_a_antibody": {
        "description": "Immune response to A antigen",
        "O": 0.95,  # Produces naturally
        "A": 0.0,   # Cannot produce (self-antigen)
        "B": 0.90,
        "AB": 0.0,
    },
    "anti_b_antibody": {
        "description": "Immune response to B antigen",
        "O": 0.95,
        "A": 0.90,
        "B": 0.0,
        "AB": 0.0,
    },
    "malaria_resistance": {
        "description": "Resistance to Plasmodium falciparum",
        "O": 0.70,  # Higher resistance
        "A": 0.45,  # Lower resistance
        "B": 0.50,
        "AB": 0.40,  # Lowest resistance
    },
    "cholera_susceptibility": {
        "description": "Susceptibility to Vibrio cholerae",
        "O": 0.80,  # Higher susceptibility
        "A": 0.50,
        "B": 0.55,
        "AB": 0.45,  # Lower susceptibility
    },
    "von_willebrand_factor": {
        "description": "Blood clotting protein levels",
        "O": 0.75,  # Lower levels (reduced clotting)
        "A": 1.00,  # Higher levels
        "B": 0.95,
        "AB": 1.05,  # Highest levels
    },
    "norovirus_binding": {
        "description": "Norovirus receptor binding",
        "O": 0.85,  # Strong binding (H antigen)
        "A": 0.60,
        "B": 0.55,
        "AB": 0.40,
    },
    "helicobacter_pylori": {
        "description": "H. pylori adhesion",
        "O": 0.75,  # Higher adhesion
        "A": 0.50,
        "B": 0.45,
        "AB": 0.40,
    },
}

# ============================================================================
# BITFIELD REPRESENTATIONS
# ============================================================================

def blood_type_to_bitfield(blood_type: str) -> int:
    """
    Convert blood type to bitfield representation.
    
    Bit layout (8 bits):
    - Bit 0: Has A antigen
    - Bit 1: Has B antigen
    - Bit 2: Rh positive
    - Bit 3: Universal donor
    - Bit 4: Universal recipient
    - Bit 5-7: Reserved for future use
    """
    data = BLOOD_TYPES[blood_type]
    bitfield = 0
    
    if "A" in data["abo_antigens"]:
        bitfield |= (1 << 0)
    if "B" in data["abo_antigens"]:
        bitfield |= (1 << 1)
    if data["rh_factor"]:
        bitfield |= (1 << 2)
    if data["universal_donor"]:
        bitfield |= (1 << 3)
    if data["universal_recipient"]:
        bitfield |= (1 << 4)
    
    return bitfield

def bitfield_to_binary_string(bitfield: int, width: int = 8) -> str:
    """Convert bitfield to binary string representation."""
    return format(bitfield, f'0{width}b')

# Generate bitfields for all blood types
BLOOD_TYPE_BITFIELDS = {
    blood_type: blood_type_to_bitfield(blood_type)
    for blood_type in BLOOD_TYPES.keys()
}

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def get_numerical_features(blood_type: str) -> list:
    """Extract numerical features for UBP analysis."""
    data = BLOOD_TYPES[blood_type]
    return [
        data["h_antigen_expression"],
        data["glycosyltransferase_a"],
        data["glycosyltransferase_b"],
        data["rh_d_protein"],
        data["molecular_weight"] / 1000.0,  # Normalize to kDa
        data["oligosaccharide_length"],
        data["fucose_residues"],
        data["galactose_residues"],
        data["n_acetylgalactosamine"],
        data["charge_density"],
        data["frequency_global"],
    ]

def get_substance_affinity_vector(blood_type: str) -> list:
    """Get substance affinity vector for a blood type."""
    # Extract ABO group (remove Rh)
    abo_group = blood_type.rstrip('+-')
    
    affinities = []
    for substance, data in SUBSTANCE_AFFINITIES.items():
        if isinstance(data, dict) and abo_group in data:
            affinities.append(data[abo_group])
    
    return affinities

if __name__ == "__main__":
    # Print summary
    print("Blood Type Data Summary")
    print("=" * 80)
    for bt, data in BLOOD_TYPES.items():
        bitfield = BLOOD_TYPE_BITFIELDS[bt]
        binary = bitfield_to_binary_string(bitfield)
        print(f"{bt:4s} | {data['name']:15s} | Bitfield: {binary} (0x{bitfield:02X}) | Freq: {data['frequency_global']:.2%}")
    
    print("\n" + "=" * 80)
    print("Substance Affinity Matrix")
    print("=" * 80)
    for substance, data in SUBSTANCE_AFFINITIES.items():
        if isinstance(data, dict):
            print(f"{substance:25s} | O: {data.get('O', 0):.2f} | A: {data.get('A', 0):.2f} | B: {data.get('B', 0):.2f} | AB: {data.get('AB', 0):.2f}")
