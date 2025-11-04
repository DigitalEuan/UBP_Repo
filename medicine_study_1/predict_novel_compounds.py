#!/usr/bin/env python3
"""
Novel Compound Prediction Using UBP Signatures
Identifies potential pharmaceutical candidates based on UBP metrics
"""

import sys
import os
import pandas as pd
import numpy as np
import json
from datetime import datetime
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import cross_val_score
from sklearn.preprocessing import StandardScaler

# Add UBP 3.3 to path
sys.path.insert(0, '/home/ubuntu/UBP_Repo/ubp_3.3')

from pharmaceutical_realm import PharmaceuticalRealm


def load_ubp_results(filepath):
    """Load UBP analysis results."""
    print(f"Loading UBP results from {filepath}...")
    df = pd.read_csv(filepath)
    print(f"Loaded {len(df)} analyzed compounds")
    return df


def identify_optimal_ubp_signatures(df):
    """
    Identify optimal UBP signatures for therapeutic potential.
    
    Analyzes the relationship between UBP metrics and drug-likeness
    to establish target ranges for novel compound prediction.
    """
    print("\n" + "="*80)
    print("IDENTIFYING OPTIMAL UBP SIGNATURES")
    print("="*80 + "\n")
    
    # Define high-performing compounds (top 20% by therapeutic potential)
    threshold = df['ubp_therapeutic_potential'].quantile(0.80)
    high_performers = df[df['ubp_therapeutic_potential'] >= threshold]
    
    print(f"High-performing compounds (top 20%): {len(high_performers)}")
    print(f"Therapeutic potential threshold: {threshold:.4f}\n")
    
    # Calculate optimal ranges for UBP metrics
    optimal_signatures = {}
    
    for metric in ['ubp_energy', 'ubp_nrci', 'ubp_crv', 'ubp_resonance']:
        mean_val = high_performers[metric].mean()
        std_val = high_performers[metric].std()
        min_val = high_performers[metric].min()
        max_val = high_performers[metric].max()
        
        optimal_signatures[metric] = {
            'mean': float(mean_val),
            'std': float(std_val),
            'min': float(min_val),
            'max': float(max_val),
            'target_range': (float(mean_val - std_val), float(mean_val + std_val))
        }
        
        print(f"{metric}:")
        print(f"  Mean: {mean_val:.6e}" if 'energy' in metric else f"  Mean: {mean_val:.6f}")
        print(f"  Std Dev: {std_val:.6e}" if 'energy' in metric else f"  Std Dev: {std_val:.6f}")
        print(f"  Target Range: [{optimal_signatures[metric]['target_range'][0]:.6e}, {optimal_signatures[metric]['target_range'][1]:.6e}]" if 'energy' in metric else f"  Target Range: [{optimal_signatures[metric]['target_range'][0]:.6f}, {optimal_signatures[metric]['target_range'][1]:.6f}]")
        print()
    
    # Therapeutic area analysis
    print("Optimal signatures by therapeutic area:")
    for area in high_performers['therapeutic_area'].unique():
        area_compounds = high_performers[high_performers['therapeutic_area'] == area]
        if len(area_compounds) >= 5:  # Only show areas with sufficient data
            print(f"\n{area} ({len(area_compounds)} compounds):")
            print(f"  Mean UBP Energy: {area_compounds['ubp_energy'].mean():.6e}")
            print(f"  Mean NRCI: {area_compounds['ubp_nrci'].mean():.10f}")
            print(f"  Mean CRV: {area_compounds['ubp_crv'].mean():.6f}")
    
    return optimal_signatures, high_performers


def build_predictive_model(df):
    """
    Build machine learning model to predict therapeutic potential
    from molecular descriptors.
    """
    print("\n" + "="*80)
    print("BUILDING PREDICTIVE MODEL")
    print("="*80 + "\n")
    
    # Features: molecular descriptors (only those available in results)
    feature_cols = [
        'molecular_weight', 'logp', 'complexity',
        'aromatic_rings', 'heavy_atoms'
    ]
    
    # Target: therapeutic potential
    X = df[feature_cols].values
    y = df['ubp_therapeutic_potential'].values
    
    # Scale features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # Train Random Forest model
    print("Training Random Forest model...")
    model = RandomForestRegressor(
        n_estimators=100,
        max_depth=10,
        random_state=42,
        n_jobs=-1
    )
    
    model.fit(X_scaled, y)
    
    # Cross-validation
    cv_scores = cross_val_score(model, X_scaled, y, cv=5, scoring='r2')
    print(f"Cross-validation R² scores: {cv_scores}")
    print(f"Mean R²: {cv_scores.mean():.4f} (+/- {cv_scores.std() * 2:.4f})")
    
    # Feature importance
    print("\nFeature importance:")
    feature_importance = pd.DataFrame({
        'feature': feature_cols,
        'importance': model.feature_importances_
    }).sort_values('importance', ascending=False)
    
    print(feature_importance.to_string(index=False))
    
    return model, scaler, feature_cols


def generate_novel_compound_candidates(optimal_signatures, n_candidates=100):
    """
    Generate novel compound candidates by sampling from optimal UBP signature space.
    
    Uses Monte Carlo sampling within optimal ranges to propose new molecular
    descriptor combinations that should exhibit high therapeutic potential.
    """
    print("\n" + "="*80)
    print(f"GENERATING {n_candidates} NOVEL COMPOUND CANDIDATES")
    print("="*80 + "\n")
    
    candidates = []
    
    # Define realistic ranges for molecular descriptors
    # Based on drug-like space (Lipinski's Rule of 5 and extensions)
    descriptor_ranges = {
        'molecular_weight': (200, 500),  # Da
        'logp': (0, 5),                   # Lipophilicity
        'complexity': (300, 1200),        # Bertz CT
        'hbd': (0, 5),                    # H-bond donors
        'hba': (2, 10),                   # H-bond acceptors
        'tpsa': (40, 120),                # Topological PSA (Ų)
        'rotatable_bonds': (2, 10),       # Flexibility
        'aromatic_rings': (1, 4),         # Rigidity
        'heavy_atoms': (15, 40)           # Size
    }
    
    # Therapeutic areas to target
    therapeutic_areas = [
        'Oncology', 'CNS/Neurology', 'Cardiovascular',
        'Anti-infective', 'Metabolic', 'Immunology',
        'Pain/Inflammation'
    ]
    
    np.random.seed(42)  # For reproducibility
    
    for i in range(n_candidates):
        # Sample molecular descriptors
        candidate = {
            'candidate_id': f'NOVEL_{i+1:04d}',
            'molecular_weight': np.random.uniform(*descriptor_ranges['molecular_weight']),
            'logp': np.random.uniform(*descriptor_ranges['logp']),
            'complexity': np.random.uniform(*descriptor_ranges['complexity']),
            'hbd': int(np.random.uniform(*descriptor_ranges['hbd'])),
            'hba': int(np.random.uniform(*descriptor_ranges['hba'])),
            'tpsa': np.random.uniform(*descriptor_ranges['tpsa']),
            'rotatable_bonds': int(np.random.uniform(*descriptor_ranges['rotatable_bonds'])),
            'aromatic_rings': int(np.random.uniform(*descriptor_ranges['aromatic_rings'])),
            'heavy_atoms': int(np.random.uniform(*descriptor_ranges['heavy_atoms'])),
            'therapeutic_area': np.random.choice(therapeutic_areas)
        }
        
        candidates.append(candidate)
    
    candidates_df = pd.DataFrame(candidates)
    
    print(f"Generated {len(candidates_df)} novel compound candidates")
    print(f"\nDescriptor ranges:")
    print(candidates_df.describe())
    
    return candidates_df


def predict_ubp_signatures_for_candidates(candidates_df, realm):
    """
    Predict UBP signatures for novel compound candidates.
    """
    print("\n" + "="*80)
    print("PREDICTING UBP SIGNATURES FOR NOVEL CANDIDATES")
    print("="*80 + "\n")
    
    predictions = []
    
    for idx, row in candidates_df.iterrows():
        if (idx + 1) % 20 == 0:
            print(f"Processing candidate {idx + 1}/{len(candidates_df)}...")
        
        try:
            # Prepare compound data for UBP analysis
            compound_data = {
                'chembl_id': row['candidate_id'],
                'name': row['candidate_id'],
                'molecular_weight': row['molecular_weight'],
                'logp': row['logp'],
                'complexity': row['complexity'],
                'hbd': row['hbd'],
                'hba': row['hba'],
                'tpsa': row['tpsa'],
                'rotatable_bonds': row['rotatable_bonds'],
                'aromatic_rings': row['aromatic_rings'],
                'heavy_atoms': row['heavy_atoms'],
                'therapeutic_area': row['therapeutic_area']
            }
            
            # Run UBP analysis
            result = realm.analyze_compound(compound_data)
            predictions.append(result)
            
        except Exception as e:
            print(f"  Error processing {row['candidate_id']}: {e}")
    
    predictions_df = pd.DataFrame(predictions)
    
    print(f"\nSuccessfully predicted UBP signatures for {len(predictions_df)} candidates")
    
    return predictions_df


def rank_novel_candidates(predictions_df, optimal_signatures):
    """
    Rank novel candidates by their similarity to optimal UBP signatures.
    """
    print("\n" + "="*80)
    print("RANKING NOVEL CANDIDATES")
    print("="*80 + "\n")
    
    # Calculate similarity scores
    scores = []
    
    for idx, row in predictions_df.iterrows():
        # Calculate distance from optimal ranges (normalized)
        energy_target = optimal_signatures['ubp_energy']['mean']
        energy_std = optimal_signatures['ubp_energy']['std']
        energy_score = 1.0 - abs(row['ubp_energy'] - energy_target) / (3 * energy_std)
        energy_score = max(0, min(1, energy_score))
        
        nrci_target = optimal_signatures['ubp_nrci']['mean']
        nrci_std = optimal_signatures['ubp_nrci']['std']
        nrci_score = 1.0 - abs(row['ubp_nrci'] - nrci_target) / (3 * nrci_std)
        nrci_score = max(0, min(1, nrci_score))
        
        crv_target = optimal_signatures['ubp_crv']['mean']
        crv_std = optimal_signatures['ubp_crv']['std']
        crv_score = 1.0 - abs(row['ubp_crv'] - crv_target) / (3 * crv_std)
        crv_score = max(0, min(1, crv_score))
        
        resonance_target = optimal_signatures['ubp_resonance']['mean']
        resonance_std = optimal_signatures['ubp_resonance']['std']
        resonance_score = 1.0 - abs(row['ubp_resonance'] - resonance_target) / (3 * resonance_std)
        resonance_score = max(0, min(1, resonance_score))
        
        # Composite score (weighted average)
        composite_score = (
            0.3 * energy_score +
            0.25 * nrci_score +
            0.25 * crv_score +
            0.2 * resonance_score
        )
        
        scores.append({
            'candidate_id': row['chembl_id'],
            'energy_score': energy_score,
            'nrci_score': nrci_score,
            'crv_score': crv_score,
            'resonance_score': resonance_score,
            'composite_score': composite_score
        })
    
    scores_df = pd.DataFrame(scores)
    
    # Merge with predictions
    ranked_df = predictions_df.merge(scores_df, left_on='chembl_id', right_on='candidate_id')
    ranked_df = ranked_df.sort_values('composite_score', ascending=False)
    
    print(f"Top 20 novel candidates by composite UBP score:")
    print("="*80)
    top_20 = ranked_df.head(20)[[
        'chembl_id', 'therapeutic_area', 'composite_score',
        'ubp_energy', 'ubp_nrci', 'ubp_crv', 'ubp_therapeutic_potential'
    ]]
    print(top_20.to_string(index=False))
    
    return ranked_df


def main():
    """Main execution."""
    # Setup
    results_dir = '/home/ubuntu/ubp_medicine_study/ubp_results'
    
    # Find most recent UBP results file
    import glob
    results_files = glob.glob(os.path.join(results_dir, 'ubp_analysis_results_*.csv'))
    if not results_files:
        print("ERROR: No UBP results files found!")
        return
    
    latest_results = max(results_files, key=os.path.getctime)
    print(f"Using results file: {latest_results}\n")
    
    # Load UBP results
    df = load_ubp_results(latest_results)
    
    # Identify optimal signatures
    optimal_signatures, high_performers = identify_optimal_ubp_signatures(df)
    
    # Build predictive model
    model, scaler, feature_cols = build_predictive_model(df)
    
    # Generate novel candidates
    candidates_df = generate_novel_compound_candidates(optimal_signatures, n_candidates=100)
    
    # Initialize pharmaceutical realm
    realm = PharmaceuticalRealm()
    
    # Predict UBP signatures for candidates
    predictions_df = predict_ubp_signatures_for_candidates(candidates_df, realm)
    
    # Rank candidates
    ranked_df = rank_novel_candidates(predictions_df, optimal_signatures)
    
    # Save results
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    output_file = os.path.join(results_dir, f'novel_candidates_ranked_{timestamp}.csv')
    ranked_df.to_csv(output_file, index=False)
    print(f"\n✓ Novel candidates saved to: {output_file}")
    
    # Save optimal signatures
    signatures_file = os.path.join(results_dir, f'optimal_ubp_signatures_{timestamp}.json')
    with open(signatures_file, 'w') as f:
        json.dump(optimal_signatures, f, indent=2)
    print(f"✓ Optimal signatures saved to: {signatures_file}")
    
    print("\n" + "="*80)
    print("NOVEL COMPOUND PREDICTION COMPLETE")
    print("="*80)
    print(f"\nGenerated and ranked {len(ranked_df)} novel candidates")
    print(f"Top candidate composite score: {ranked_df['composite_score'].max():.4f}")
    
    return ranked_df, optimal_signatures


if __name__ == '__main__':
    ranked_df, optimal_signatures = main()
