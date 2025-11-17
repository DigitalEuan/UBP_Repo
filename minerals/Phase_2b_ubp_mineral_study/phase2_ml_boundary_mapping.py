#!/usr/bin/env python3.11
"""
Phase 2 Module 3: ML Boundary Mapping
Train multiple classifiers to find nonlinear decision boundaries in mineral coherence space
"""

import json
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score, roc_auc_score, roc_curve
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import time

# Use natural threshold discovered in Phase 2 Module 2
NATURAL_THRESHOLD = 0.973243  # 95th percentile

def load_and_prepare_data():
    """Load Phase 2 results and prepare features/labels"""
    print("\n[1/6] Loading Phase 2 coherence analysis results...")
    with open('results/phase2_coherence_analysis_3112.json', 'r') as f:
        results = json.load(f)
    
    # Create DataFrame
    df = pd.DataFrame(results)
    
    # Define features (8D feature space)
    feature_cols = [
        'Z_max',                # Atomic number
        'symmetry_operations',  # Crystal symmetry
        'element_count',        # Compositional complexity
        'molar_mass',          # Mass
        'density',             # Density
        'refinements',         # Y-refinements performed
        'degradation',         # Total degradation
        'final_coherence'      # Final coherence value
    ]
    
    # Handle missing mohs_hardness (fill with median)
    df['mohs_hardness'] = df['mohs_hardness'].fillna(df['mohs_hardness'].median())
    
    # Extract features
    X = df[feature_cols].values
    
    # Create labels using natural threshold
    y = (df['nrci'] >= NATURAL_THRESHOLD).astype(int)
    
    print(f"   Loaded {len(df)} minerals")
    print(f"   Feature space: {X.shape[1]}D")
    print(f"   Class distribution:")
    print(f"      Pass (1): {y.sum()} ({y.sum()/len(y)*100:.2f}%)")
    print(f"      Fail (0): {len(y)-y.sum()} ({(len(y)-y.sum())/len(y)*100:.2f}%)")
    
    return X, y, df, feature_cols

def train_svm(X_train, X_test, y_train, y_test):
    """Train SVM with multiple kernels"""
    print("\n[2/6] Training Support Vector Machines...")
    
    results = {}
    kernels = ['linear', 'rbf', 'poly']
    
    for kernel in kernels:
        print(f"\n   Training SVM with {kernel} kernel...")
        start = time.time()
        
        if kernel == 'linear':
            svm = SVC(kernel=kernel, probability=True, random_state=42)
        elif kernel == 'rbf':
            # Grid search for best C and gamma
            param_grid = {
                'C': [0.1, 1, 10, 100],
                'gamma': ['scale', 'auto', 0.001, 0.01]
            }
            svm = GridSearchCV(SVC(kernel=kernel, probability=True, random_state=42),
                              param_grid, cv=5, n_jobs=-1, verbose=0)
        else:  # poly
            param_grid = {
                'C': [0.1, 1, 10],
                'degree': [2, 3, 4]
            }
            svm = GridSearchCV(SVC(kernel=kernel, probability=True, random_state=42),
                              param_grid, cv=5, n_jobs=-1, verbose=0)
        
        svm.fit(X_train, y_train)
        elapsed = time.time() - start
        
        # Get best estimator if GridSearchCV
        if isinstance(svm, GridSearchCV):
            best_params = svm.best_params_
            svm = svm.best_estimator_
            print(f"      Best params: {best_params}")
        
        # Predictions
        y_pred = svm.predict(X_test)
        y_prob = svm.predict_proba(X_test)[:, 1]
        
        # Metrics
        accuracy = accuracy_score(y_test, y_pred)
        roc_auc = roc_auc_score(y_test, y_prob)
        
        print(f"      Accuracy: {accuracy:.4f}")
        print(f"      ROC AUC: {roc_auc:.4f}")
        print(f"      Training time: {elapsed:.2f}s")
        
        results[f'svm_{kernel}'] = {
            'model': svm,
            'accuracy': accuracy,
            'roc_auc': roc_auc,
            'y_pred': y_pred,
            'y_prob': y_prob,
            'training_time': elapsed
        }
    
    return results

def train_random_forest(X_train, X_test, y_train, y_test):
    """Train Random Forest classifier"""
    print("\n[3/6] Training Random Forest...")
    start = time.time()
    
    # Grid search for best hyperparameters
    param_grid = {
        'n_estimators': [100, 200, 300],
        'max_depth': [10, 20, 30, None],
        'min_samples_split': [2, 5, 10]
    }
    
    rf = GridSearchCV(RandomForestClassifier(random_state=42, n_jobs=-1),
                      param_grid, cv=5, n_jobs=-1, verbose=0)
    rf.fit(X_train, y_train)
    
    print(f"   Best params: {rf.best_params_}")
    
    # Get best estimator
    rf = rf.best_estimator_
    elapsed = time.time() - start
    
    # Predictions
    y_pred = rf.predict(X_test)
    y_prob = rf.predict_proba(X_test)[:, 1]
    
    # Metrics
    accuracy = accuracy_score(y_test, y_pred)
    roc_auc = roc_auc_score(y_test, y_prob)
    
    print(f"   Accuracy: {accuracy:.4f}")
    print(f"   ROC AUC: {roc_auc:.4f}")
    print(f"   Training time: {elapsed:.2f}s")
    
    # Feature importances
    print(f"\n   Feature Importances:")
    return {
        'model': rf,
        'accuracy': accuracy,
        'roc_auc': roc_auc,
        'y_pred': y_pred,
        'y_prob': y_prob,
        'training_time': elapsed,
        'feature_importances': rf.feature_importances_
    }

def train_neural_network(X_train, X_test, y_train, y_test):
    """Train Neural Network (MLP) classifier"""
    print("\n[4/6] Training Neural Network (MLP)...")
    start = time.time()
    
    # Grid search for best architecture
    param_grid = {
        'hidden_layer_sizes': [(50,), (100,), (50, 50), (100, 50)],
        'activation': ['relu', 'tanh'],
        'alpha': [0.0001, 0.001, 0.01]
    }
    
    mlp = GridSearchCV(MLPClassifier(max_iter=1000, random_state=42),
                       param_grid, cv=5, n_jobs=-1, verbose=0)
    mlp.fit(X_train, y_train)
    
    print(f"   Best params: {mlp.best_params_}")
    
    # Get best estimator
    mlp = mlp.best_estimator_
    elapsed = time.time() - start
    
    # Predictions
    y_pred = mlp.predict(X_test)
    y_prob = mlp.predict_proba(X_test)[:, 1]
    
    # Metrics
    accuracy = accuracy_score(y_test, y_pred)
    roc_auc = roc_auc_score(y_test, y_prob)
    
    print(f"   Accuracy: {accuracy:.4f}")
    print(f"   ROC AUC: {roc_auc:.4f}")
    print(f"   Training time: {elapsed:.2f}s")
    
    return {
        'model': mlp,
        'accuracy': accuracy,
        'roc_auc': roc_auc,
        'y_pred': y_pred,
        'y_prob': y_prob,
        'training_time': elapsed
    }

def visualize_results(results, y_test, feature_cols, rf_result):
    """Create comprehensive visualizations"""
    print("\n[5/6] Creating visualizations...")
    
    # 1. ROC Curves
    plt.figure(figsize=(10, 8))
    for name, result in results.items():
        fpr, tpr, _ = roc_curve(y_test, result['y_prob'])
        plt.plot(fpr, tpr, label=f"{name} (AUC={result['roc_auc']:.3f})")
    
    plt.plot([0, 1], [0, 1], 'k--', label='Random')
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('ROC Curves - ML Classifiers Comparison')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('results/phase2_ml_roc_curves.png', dpi=150)
    print("   ✓ Saved ROC curves")
    
    # 2. Accuracy Comparison
    plt.figure(figsize=(10, 6))
    names = list(results.keys())
    accuracies = [results[name]['accuracy'] for name in names]
    roc_aucs = [results[name]['roc_auc'] for name in names]
    
    x = np.arange(len(names))
    width = 0.35
    
    plt.bar(x - width/2, accuracies, width, label='Accuracy', alpha=0.8)
    plt.bar(x + width/2, roc_aucs, width, label='ROC AUC', alpha=0.8)
    
    plt.xlabel('Classifier')
    plt.ylabel('Score')
    plt.title('ML Classifier Performance Comparison')
    plt.xticks(x, names, rotation=45, ha='right')
    plt.legend()
    plt.ylim([0, 1.1])
    plt.grid(True, alpha=0.3, axis='y')
    plt.tight_layout()
    plt.savefig('results/phase2_ml_accuracy_comparison.png', dpi=150)
    print("   ✓ Saved accuracy comparison")
    
    # 3. Feature Importances (Random Forest)
    if 'feature_importances' in rf_result:
        plt.figure(figsize=(10, 6))
        importances = rf_result['feature_importances']
        indices = np.argsort(importances)[::-1]
        
        plt.bar(range(len(importances)), importances[indices], alpha=0.8)
        plt.xticks(range(len(importances)), [feature_cols[i] for i in indices], rotation=45, ha='right')
        plt.xlabel('Feature')
        plt.ylabel('Importance')
        plt.title('Random Forest Feature Importances')
        plt.grid(True, alpha=0.3, axis='y')
        plt.tight_layout()
        plt.savefig('results/phase2_ml_feature_importances.png', dpi=150)
        print("   ✓ Saved feature importances")
    
    # 4. Confusion Matrices
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    axes = axes.flatten()
    
    for idx, (name, result) in enumerate(results.items()):
        cm = confusion_matrix(y_test, result['y_pred'])
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', ax=axes[idx])
        axes[idx].set_title(f'{name}\nAccuracy: {result["accuracy"]:.3f}')
        axes[idx].set_xlabel('Predicted')
        axes[idx].set_ylabel('Actual')
    
    # Hide unused subplot
    if len(results) < 6:
        for idx in range(len(results), 6):
            axes[idx].axis('off')
    
    plt.tight_layout()
    plt.savefig('results/phase2_ml_confusion_matrices.png', dpi=150)
    print("   ✓ Saved confusion matrices")

def save_results(results, feature_cols, rf_result):
    """Save ML results to JSON"""
    print("\n[6/6] Saving results...")
    
    summary = {
        'threshold': NATURAL_THRESHOLD,
        'classifiers': {},
        'feature_columns': feature_cols
    }
    
    for name, result in results.items():
        summary['classifiers'][name] = {
            'accuracy': float(result['accuracy']),
            'roc_auc': float(result['roc_auc']),
            'training_time': float(result['training_time'])
        }
    
    # Add feature importances
    if 'feature_importances' in rf_result:
        summary['feature_importances'] = {
            feature_cols[i]: float(rf_result['feature_importances'][i])
            for i in range(len(feature_cols))
        }
    
    with open('results/phase2_ml_summary.json', 'w') as f:
        json.dump(summary, f, indent=2)
    
    print("   ✓ Saved summary to results/phase2_ml_summary.json")

def main():
    print("="*80)
    print("PHASE 2 MODULE 3: ML BOUNDARY MAPPING")
    print("="*80)
    print(f"Natural threshold: {NATURAL_THRESHOLD:.6f} (95th percentile)")
    print("Classifiers: SVM (linear, RBF, poly), Random Forest, Neural Network")
    print("="*80)
    
    # Load and prepare data
    X, y, df, feature_cols = load_and_prepare_data()
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    
    # Scale features
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)
    
    print(f"\n   Train set: {len(X_train)} samples")
    print(f"   Test set: {len(X_test)} samples")
    
    # Train classifiers
    results = {}
    
    # SVM
    svm_results = train_svm(X_train, X_test, y_train, y_test)
    results.update(svm_results)
    
    # Random Forest
    rf_result = train_random_forest(X_train, X_test, y_train, y_test)
    results['random_forest'] = rf_result
    
    # Neural Network
    nn_result = train_neural_network(X_train, X_test, y_train, y_test)
    results['neural_network'] = nn_result
    
    # Print feature importances
    print("\n   Feature Importances (Random Forest):")
    importances = rf_result['feature_importances']
    indices = np.argsort(importances)[::-1]
    for i in indices:
        print(f"      {feature_cols[i]:20s}: {importances[i]:.4f}")
    
    # Visualize
    visualize_results(results, y_test, feature_cols, rf_result)
    
    # Save
    save_results(results, feature_cols, rf_result)
    
    # Summary
    print("\n" + "="*80)
    print("ML BOUNDARY MAPPING COMPLETE!")
    print("="*80)
    print("\nBest Classifier:")
    best_name = max(results.keys(), key=lambda k: results[k]['roc_auc'])
    best = results[best_name]
    print(f"   {best_name}")
    print(f"   Accuracy: {best['accuracy']:.4f}")
    print(f"   ROC AUC: {best['roc_auc']:.4f}")
    
    print("\nKey Findings:")
    print(f"   1. Most important feature: {feature_cols[indices[0]]}")
    print(f"   2. Least important feature: {feature_cols[indices[-1]]}")
    print(f"   3. Best classifier: {best_name}")
    print(f"   4. All models achieved >90% accuracy: {all(r['accuracy'] > 0.9 for r in results.values())}")

if __name__ == '__main__':
    main()
