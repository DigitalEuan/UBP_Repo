#!/usr/bin/env python3
"""
UBP Cheese Mould Study - Main Analysis Script
==============================================

This script reproduces the complete analysis from the academic paper:
"A Geometric Model of Mycological Metabolism in Dairy Fermentation"

Author: E. R. A. Craig, New Zealand
Date: January 2026

Usage:
    python run_analysis.py
"""

import sys
import os
import math
import json
from fractions import Fraction

# Add ubp_core to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'ubp_core'))

from ubp_core_v4_2_6_COMBINED import (
    UBPUltimateSubstrate, 
    GolayCodeEngine, 
    LeechPointScaled, 
    BinaryLinearAlgebra,
    GOLAY_DECODER,
    LEECH_ENHANCED
)

# =============================================================================
# CONSTANTS
# =============================================================================

PI = UBPUltimateSubstrate.get_pi(50)
Y = PI / (PI**2 + 2)
Y_INV = Fraction(1, 1) / Y
SCALE_BASE = float(Y_INV)  # approx 3.778
H_MASS = 1.00784  # Hydrogen mass in Daltons

# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def molecule_to_bits(data):
    """
    Convert molecular formula to 24-bit vector.
    
    Partition: C(6) | H(6) | N(6) | O(6)
    """
    c = data.get('C', 0)
    h = data.get('H', 0)
    n = data.get('N', 0)
    o = data.get('O', 0)
    
    vec = []
    for count in [c, h, n, o]:
        val = (count * 13) % 64
        vec.extend([(val >> i) & 1 for i in range(5, -1, -1)])
    return vec


def get_nrci(vec):
    """Calculate Non-Random Coherence Index from 24-bit vector."""
    pt = LeechPointScaled(tuple(vec))
    health = pt.get_ontological_health()
    total = sum(v for v in health.values() if isinstance(v, Fraction))
    return float(total / 2.0)


def get_mass_shell(mass_daltons):
    """Calculate Mass Shell N from molecular mass."""
    ratio = mass_daltons / H_MASS
    N = math.log(ratio, SCALE_BASE)
    return N


def get_layer_analysis(vec):
    """Get detailed MOG layer breakdown."""
    pt = LeechPointScaled(tuple(vec))
    health = pt.get_ontological_health()
    return {
        'Reality': float(health['Reality']),
        'Info': float(health['Info']),
        'Activation': float(health['Activation']),
        'Potential': float(health['Potential']),
    }


# =============================================================================
# DATASET
# =============================================================================

COMPOUNDS = [
    # Flavor compounds
    {"name": "2-Heptanone", "mass": 114.18, "atoms": {"C": 7, "H": 14, "N": 0, "O": 1}, "type": "FLAVOR", "source": "Blue cheese"},
    {"name": "2-Nonanone", "mass": 142.24, "atoms": {"C": 9, "H": 18, "N": 0, "O": 1}, "type": "FLAVOR", "source": "Blue cheese"},
    {"name": "2-Pentanone", "mass": 86.13, "atoms": {"C": 5, "H": 10, "N": 0, "O": 1}, "type": "FLAVOR", "source": "Blue cheese"},
    {"name": "1-Octen-3-ol", "mass": 128.21, "atoms": {"C": 8, "H": 16, "N": 0, "O": 1}, "type": "FLAVOR", "source": "Mushroom note"},
    {"name": "Butyric Acid", "mass": 88.11, "atoms": {"C": 4, "H": 8, "N": 0, "O": 2}, "type": "FLAVOR", "source": "Rancid/cheesy"},
    {"name": "Methyl Cinnamate", "mass": 162.19, "atoms": {"C": 10, "H": 10, "N": 0, "O": 2}, "type": "FLAVOR", "source": "Balsamic"},
    {"name": "Ethyl Butyrate", "mass": 116.16, "atoms": {"C": 6, "H": 12, "N": 0, "O": 2}, "type": "FLAVOR", "source": "Fruity"},
    {"name": "Diacetyl", "mass": 86.09, "atoms": {"C": 4, "H": 6, "N": 0, "O": 2}, "type": "FLAVOR", "source": "Buttery"},
    {"name": "Acetoin", "mass": 88.11, "atoms": {"C": 4, "H": 8, "N": 0, "O": 2}, "type": "FLAVOR", "source": "Creamy"},
    {"name": "Hexanoic Acid", "mass": 116.16, "atoms": {"C": 6, "H": 12, "N": 0, "O": 2}, "type": "FLAVOR", "source": "Goaty"},
    # Mycotoxins
    {"name": "Ochratoxin A", "mass": 403.81, "atoms": {"C": 20, "H": 18, "N": 1, "O": 6}, "type": "TOXIN", "source": "P. nordicum"},
    {"name": "Roquefortine C", "mass": 389.41, "atoms": {"C": 22, "H": 23, "N": 5, "O": 2}, "type": "TOXIN", "source": "P. roqueforti"},
    {"name": "Cyclopiazonic Acid", "mass": 336.39, "atoms": {"C": 20, "H": 20, "N": 2, "O": 3}, "type": "TOXIN", "source": "P. camemberti"},
    {"name": "Sterigmatocystin", "mass": 324.29, "atoms": {"C": 18, "H": 12, "N": 0, "O": 6}, "type": "TOXIN", "source": "A. versicolor"},
    {"name": "Mycophenolic Acid", "mass": 320.34, "atoms": {"C": 17, "H": 20, "N": 0, "O": 6}, "type": "TOXIN", "source": "P. roqueforti"},
    {"name": "Patulin", "mass": 154.12, "atoms": {"C": 7, "H": 6, "N": 0, "O": 4}, "type": "TOXIN", "source": "P. expansum"},
    {"name": "Citrinin", "mass": 250.25, "atoms": {"C": 13, "H": 14, "N": 0, "O": 5}, "type": "TOXIN", "source": "P. citrinum"},
    {"name": "Penicillic Acid", "mass": 170.16, "atoms": {"C": 8, "H": 10, "N": 0, "O": 4}, "type": "TOXIN", "source": "P. cyclopium"},
]


# =============================================================================
# ANALYSIS FUNCTIONS
# =============================================================================

def calculate_statistics(data, key):
    """Calculate mean, std, min, max for a given key."""
    values = [d[key] for d in data]
    n = len(values)
    mean = sum(values) / n
    variance = sum((x - mean)**2 for x in values) / n
    std = variance ** 0.5
    return mean, std, min(values), max(values)


def cohens_d(group1, group2, key):
    """Calculate Cohen's d effect size."""
    m1 = sum(d[key] for d in group1) / len(group1)
    m2 = sum(d[key] for d in group2) / len(group2)
    v1 = sum((d[key] - m1)**2 for d in group1) / len(group1)
    v2 = sum((d[key] - m2)**2 for d in group2) / len(group2)
    pooled_std = ((v1 + v2) / 2) ** 0.5
    if pooled_std == 0:
        return 0
    return (m2 - m1) / pooled_std


def run_analysis():
    """Run the complete analysis."""
    print("=" * 70)
    print("UBP CHEESE MOULD STUDY - COMPLETE ANALYSIS")
    print("=" * 70)
    print()
    
    # --- STEP 1: System Verification ---
    print("--- STEP 1: UBP CORE VERIFICATION ---")
    print(f"  Pi (50-term CF):     {float(PI):.15f}")
    print(f"  Y constant:          {float(Y):.15f}")
    print(f"  1/Y (scale base):    {float(Y_INV):.15f}")
    
    # Verify particle predictions
    muon_pred = (Y_INV ** 4) + 3
    muon_exp = 206.768283
    print(f"  Muon/Electron pred:  {float(muon_pred):.6f} (actual: {muon_exp}, error: {abs(float(muon_pred) - muon_exp)/muon_exp*100:.4f}%)")
    print()
    
    # --- STEP 2: Analyze Compounds ---
    print("--- STEP 2: COMPOUND ANALYSIS ---")
    print()
    
    results = []
    for comp in COMPOUNDS:
        vec = molecule_to_bits(comp['atoms'])
        nrci = get_nrci(vec)
        shell = get_mass_shell(comp['mass'])
        layers = get_layer_analysis(vec)
        
        results.append({
            'name': comp['name'],
            'mass': comp['mass'],
            'shell': shell,
            'nrci': nrci,
            'type': comp['type'],
            'source': comp['source'],
            'layers': layers,
        })
    
    # Sort by type and shell
    results.sort(key=lambda x: (x['type'], x['shell']))
    
    print(f"{'Compound':<22} | {'Mass':>7} | {'Shell':>6} | {'NRCI':>5} | {'Type':>7}")
    print("-" * 60)
    for r in results:
        print(f"{r['name']:<22} | {r['mass']:>7.2f} | {r['shell']:>6.3f} | {r['nrci']:>5.3f} | {r['type']:>7}")
    print()
    
    # --- STEP 3: Statistical Analysis ---
    print("--- STEP 3: STATISTICAL ANALYSIS ---")
    print()
    
    flavors = [r for r in results if r['type'] == 'FLAVOR']
    toxins = [r for r in results if r['type'] == 'TOXIN']
    
    print(f"{'Metric':<15} | {'Flavor (n={})'.format(len(flavors)):>25} | {'Toxin (n={})'.format(len(toxins)):>25} | {'Cohen d':>8}")
    print("-" * 85)
    
    for metric in ['nrci', 'shell', 'mass']:
        f_mean, f_std, f_min, f_max = calculate_statistics(flavors, metric)
        t_mean, t_std, t_min, t_max = calculate_statistics(toxins, metric)
        d = cohens_d(flavors, toxins, metric)
        print(f"{metric.upper():<15} | {f_mean:>7.3f} ± {f_std:>5.3f} [{f_min:.2f}-{f_max:.2f}] | {t_mean:>7.3f} ± {t_std:>5.3f} [{t_min:.2f}-{t_max:.2f}] | {d:>8.3f}")
    print()
    
    # --- STEP 4: Classification Test ---
    print("--- STEP 4: CLASSIFICATION TEST ---")
    print()
    
    # Test multiple rules
    rules = [
        ("Shell >= 4.0", lambda r: r['shell'] >= 4.0),
        ("Shell >= 3.8", lambda r: r['shell'] >= 3.8),
        ("NRCI >= 0.75", lambda r: r['nrci'] >= 0.75),
        ("Shell >= 4.0 AND NRCI >= 0.75", lambda r: r['shell'] >= 4.0 and r['nrci'] >= 0.75),
    ]
    
    print(f"{'Rule':<40} | {'Acc':>5} | {'Prec':>5} | {'Rec':>5} | {'F1':>5}")
    print("-" * 70)
    
    for rule_name, rule_fn in rules:
        tp = fp = tn = fn = 0
        for r in results:
            predicted = "TOXIN" if rule_fn(r) else "FLAVOR"
            actual = r['type']
            if predicted == "TOXIN" and actual == "TOXIN":
                tp += 1
            elif predicted == "TOXIN" and actual == "FLAVOR":
                fp += 1
            elif predicted == "FLAVOR" and actual == "FLAVOR":
                tn += 1
            else:
                fn += 1
        
        accuracy = (tp + tn) / (tp + tn + fp + fn)
        precision = tp / (tp + fp) if (tp + fp) > 0 else 0
        recall = tp / (tp + fn) if (tp + fn) > 0 else 0
        f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0
        
        print(f"{rule_name:<40} | {accuracy:>5.1%} | {precision:>5.1%} | {recall:>5.1%} | {f1:>5.2f}")
    
    print()
    print("=" * 70)
    print("ANALYSIS COMPLETE")
    print("=" * 70)
    
    # Save results
    output_dir = os.path.join(os.path.dirname(__file__), 'data')
    os.makedirs(output_dir, exist_ok=True)
    
    with open(os.path.join(output_dir, 'analysis_results.json'), 'w') as f:
        json.dump(results, f, indent=2)
    print(f"\nResults saved to: data/analysis_results.json")
    
    return results


# =============================================================================
# MAIN
# =============================================================================

if __name__ == "__main__":
    run_analysis()
