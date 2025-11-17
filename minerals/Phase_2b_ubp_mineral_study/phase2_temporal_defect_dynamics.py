#!/usr/bin/env python3.11
"""
Phase 2 Module 5: Temporal Evolution and Defect Incorporation Dynamics
Simulate how minerals evolve through Bitfield over time and how defects affect position
"""

import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from coherence_substrate_v2 import CoherenceState
import time

NATURAL_THRESHOLD = 0.973243

def load_data():
    """Load Phase 2 results"""
    print("\n[1/5] Loading Phase 2 coherence analysis results...")
    with open('results/phase2_coherence_analysis_3112.json', 'r') as f:
        results = json.load(f)
    
    df = pd.DataFrame(results)
    print(f"   Loaded {len(df)} minerals")
    
    return df

def simulate_temporal_evolution(mineral, num_steps=10):
    """
    Simulate temporal evolution of a mineral through information space
    Models gradual refinement/degradation over time
    """
    # Initial state
    state = CoherenceState(1.0)
    
    # Parameters
    Z = mineral['Z_max']
    symmetry = mineral['symmetry_operations']
    element_count = mineral['element_count']
    
    # Degradation rate (per step)
    base_deg = 0.0001 * Z
    tgic = np.log(element_count) if element_count > 1 else 0
    tgic_pen = (1 - symmetry/48) * tgic * 0.001
    deg_per_step = (base_deg + tgic_pen) / num_steps
    
    # Refinement opportunities (based on symmetry)
    refine_prob = symmetry / 48  # Probability of refinement per step
    
    # Trajectory
    trajectory = []
    for step in range(num_steps + 1):
        # Current NRCI
        degradation = deg_per_step * step * num_steps
        nrci = float(state.value) - degradation
        
        trajectory.append({
            'step': step,
            'coherence': float(state.value),
            'degradation': degradation,
            'nrci': nrci,
            'passes': nrci >= NATURAL_THRESHOLD
        })
        
        # Refinement step (probabilistic)
        if step < num_steps and np.random.random() < refine_prob:
            state = state.refine_forward()
    
    return trajectory

def simulate_defect_incorporation(mineral, defect_levels=[0.0, 0.01, 0.05, 0.1, 0.2]):
    """
    Simulate effect of defects/impurities on mineral coherence
    Defect level: fraction of atoms replaced by impurities
    """
    results = []
    
    for defect_level in defect_levels:
        # Base parameters
        Z = mineral['Z_max']
        symmetry = mineral['symmetry_operations']
        element_count = mineral['element_count']
        
        # Defects increase effective Z (assume impurities are heavier)
        # and increase compositional complexity
        Z_eff = Z * (1 + defect_level * 0.5)  # Impurities add ~50% to Z
        elem_eff = element_count + defect_level * 10  # Defects add complexity
        
        # Recalculate degradation
        base_deg = 0.001 * Z_eff
        tgic = np.log(elem_eff) if elem_eff > 1 else 0
        tgic_pen = (1 - symmetry/48) * tgic * 0.01
        total_deg = base_deg + tgic_pen
        
        # Refinements (defects reduce symmetry effectiveness)
        refine_factor = (symmetry / 48) * (1 - defect_level)
        num_refine = int(refine_factor * 10)
        
        # Calculate NRCI
        state = CoherenceState(1.0)
        for _ in range(num_refine):
            state = state.refine_forward()
        
        nrci = float(state.value) - total_deg
        
        results.append({
            'defect_level': defect_level,
            'Z_effective': Z_eff,
            'element_effective': elem_eff,
            'degradation': total_deg,
            'refinements': num_refine,
            'nrci': nrci,
            'passes': nrci >= NATURAL_THRESHOLD
        })
    
    return results

def analyze_temporal_patterns(df):
    """Analyze temporal evolution patterns across mineral classes"""
    print("\n[2/5] Analyzing temporal evolution patterns...")
    
    # Sample minerals from different classes
    passed = df[df['nrci'] >= NATURAL_THRESHOLD].sample(min(10, len(df[df['nrci'] >= NATURAL_THRESHOLD])), random_state=42)
    failed = df[df['nrci'] < NATURAL_THRESHOLD].sample(10, random_state=42)
    
    temporal_data = {
        'passed': [],
        'failed': []
    }
    
    print("   Simulating temporal evolution for PASSED minerals...")
    for idx, mineral in passed.iterrows():
        traj = simulate_temporal_evolution(mineral, num_steps=10)
        temporal_data['passed'].append({
            'name': mineral['name'],
            'trajectory': traj
        })
    
    print("   Simulating temporal evolution for FAILED minerals...")
    for idx, mineral in failed.iterrows():
        traj = simulate_temporal_evolution(mineral, num_steps=10)
        temporal_data['failed'].append({
            'name': mineral['name'],
            'trajectory': traj
        })
    
    return temporal_data

def analyze_defect_effects(df):
    """Analyze how defects affect mineral coherence"""
    print("\n[3/5] Analyzing defect incorporation effects...")
    
    # Sample minerals
    passed = df[df['nrci'] >= NATURAL_THRESHOLD].sample(min(10, len(df[df['nrci'] >= NATURAL_THRESHOLD])), random_state=42)
    failed = df[df['nrci'] < NATURAL_THRESHOLD].sample(10, random_state=42)
    
    defect_data = {
        'passed': [],
        'failed': []
    }
    
    print("   Simulating defect incorporation for PASSED minerals...")
    for idx, mineral in passed.iterrows():
        defects = simulate_defect_incorporation(mineral)
        defect_data['passed'].append({
            'name': mineral['name'],
            'defects': defects
        })
    
    print("   Simulating defect incorporation for FAILED minerals...")
    for idx, mineral in failed.iterrows():
        defects = simulate_defect_incorporation(mineral)
        defect_data['failed'].append({
            'name': mineral['name'],
            'defects': defects
        })
    
    return defect_data

def visualize_temporal(temporal_data):
    """Visualize temporal evolution trajectories"""
    print("\n[4/5] Creating temporal evolution visualizations...")
    
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    
    # PASSED minerals
    for mineral in temporal_data['passed']:
        traj = mineral['trajectory']
        steps = [t['step'] for t in traj]
        nrcis = [t['nrci'] for t in traj]
        axes[0].plot(steps, nrcis, alpha=0.6, linewidth=2)
    
    axes[0].axhline(NATURAL_THRESHOLD, color='red', linestyle='--', linewidth=2, label='Threshold')
    axes[0].set_xlabel('Time Step')
    axes[0].set_ylabel('NRCI')
    axes[0].set_title('Temporal Evolution: PASSED Minerals')
    axes[0].legend()
    axes[0].grid(True, alpha=0.3)
    
    # FAILED minerals
    for mineral in temporal_data['failed']:
        traj = mineral['trajectory']
        steps = [t['step'] for t in traj]
        nrcis = [t['nrci'] for t in traj]
        axes[1].plot(steps, nrcis, alpha=0.6, linewidth=2)
    
    axes[1].axhline(NATURAL_THRESHOLD, color='red', linestyle='--', linewidth=2, label='Threshold')
    axes[1].set_xlabel('Time Step')
    axes[1].set_ylabel('NRCI')
    axes[1].set_title('Temporal Evolution: FAILED Minerals')
    axes[1].legend()
    axes[1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('results/phase2_temporal_evolution.png', dpi=150)
    print("   ✓ Saved temporal evolution plot")

def visualize_defects(defect_data):
    """Visualize defect incorporation effects"""
    print("   Creating defect incorporation visualizations...")
    
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    
    # PASSED minerals
    for mineral in defect_data['passed']:
        defects = mineral['defects']
        levels = [d['defect_level'] for d in defects]
        nrcis = [d['nrci'] for d in defects]
        axes[0].plot(levels, nrcis, alpha=0.6, linewidth=2, marker='o')
    
    axes[0].axhline(NATURAL_THRESHOLD, color='red', linestyle='--', linewidth=2, label='Threshold')
    axes[0].set_xlabel('Defect Level (fraction)')
    axes[0].set_ylabel('NRCI')
    axes[0].set_title('Defect Effects: PASSED Minerals')
    axes[0].legend()
    axes[0].grid(True, alpha=0.3)
    
    # FAILED minerals
    for mineral in defect_data['failed']:
        defects = mineral['defects']
        levels = [d['defect_level'] for d in defects]
        nrcis = [d['nrci'] for d in defects]
        axes[1].plot(levels, nrcis, alpha=0.6, linewidth=2, marker='o')
    
    axes[1].axhline(NATURAL_THRESHOLD, color='red', linestyle='--', linewidth=2, label='Threshold')
    axes[1].set_xlabel('Defect Level (fraction)')
    axes[1].set_ylabel('NRCI')
    axes[1].set_title('Defect Effects: FAILED Minerals')
    axes[1].legend()
    axes[1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('results/phase2_defect_effects.png', dpi=150)
    print("   ✓ Saved defect effects plot")

def save_results(temporal_data, defect_data, temporal_stability, defect_tolerance):
    """Save simulation results"""
    print("\n[5/5] Saving results...")
    
    summary = {
        'temporal_stability': temporal_stability,
        'defect_tolerance': defect_tolerance
    }
    
    with open('results/phase2_temporal_defect_summary.json', 'w') as f:
        json.dump(summary, f, indent=2)
    
    print("   ✓ Saved summary to results/phase2_temporal_defect_summary.json")

def main():
    print("="*80)
    print("PHASE 2 MODULE 5: TEMPORAL & DEFECT DYNAMICS")
    print("="*80)
    print("Simulations:")
    print("  1. Temporal evolution (10 time steps)")
    print("  2. Defect incorporation (0-20% defect levels)")
    print("="*80)
    
    # Load data
    df = load_data()
    
    # Analyze
    temporal_data = analyze_temporal_patterns(df)
    defect_data = analyze_defect_effects(df)
    
    # Visualize
    visualize_temporal(temporal_data)
    visualize_defects(defect_data)
    
    # Save
    # Temporal stability analysis
    passed_stable = sum(1 for m in temporal_data['passed'] 
                       if all(t['passes'] for t in m['trajectory']))
    failed_stable = sum(1 for m in temporal_data['failed'] 
                       if all(not t['passes'] for t in m['trajectory']))
    temporal_stability = {
        'passed_stable': passed_stable,
        'passed_total': len(temporal_data['passed']),
        'failed_stable': failed_stable,
        'failed_total': len(temporal_data['failed'])
    }

    # Defect tolerance analysis
    passed_tolerant = sum(1 for m in defect_data['passed']
                         if m['defects'][-1]['passes'])  # Still passes at 20% defects
    failed_never_pass = sum(1 for m in defect_data['failed']
                           if not any(d['passes'] for d in m['defects']))
    defect_tolerance = {
        'passed_tolerant_20_percent': passed_tolerant,
        'passed_total': len(defect_data['passed']),
        'failed_never_pass': failed_never_pass,
        'failed_total': len(defect_data['failed'])
    }

    save_results(temporal_data, defect_data, temporal_stability, defect_tolerance)
    
    # Analysis
    print("\n" + "="*80)
    print("TEMPORAL & DEFECT DYNAMICS COMPLETE!")
    print("="*80)
    
    # Print summary from saved data
    print("\nTemporal Stability:")
    print(f"   PASSED minerals remaining stable: {temporal_stability['passed_stable']}/{temporal_stability['passed_total']}")
    print(f"   FAILED minerals remaining unstable: {temporal_stability['failed_stable']}/{temporal_stability['failed_total']}")

    print("\nDefect Tolerance:")
    print(f"   PASSED minerals tolerant to 20% defects: {defect_tolerance['passed_tolerant_20_percent']}/{defect_tolerance['passed_total']}")
    print(f"   FAILED minerals never passing: {defect_tolerance['failed_never_pass']}/{defect_tolerance['failed_total']}")

if __name__ == '__main__':
    main()
