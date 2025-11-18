#!/usr/bin/env python3.11
"""
Predictive Modeling Module - Phase 2C
Build and validate models to predict NRCI from bitfield features

This module performs:
1. Feature importance analysis
2. Multiple regression models (Linear, Ridge, Random Forest)
3. Cross-validation and performance metrics
4. Residual analysis
5. Model interpretation and insights
"""

import json
import numpy as np
import matplotlib.pyplot as plt
from typing import Dict, List, Tuple
import os

class PredictiveModeler:
    """
    Build predictive models for NRCI from bitfield features.
    """
    
    def __init__(self, processed_data_path: str):
        """
        Initialize modeler with processed symbol data.
        
        Args:
            processed_data_path: Path to symbols_processed.json
        """
        with open(processed_data_path, 'r') as f:
            self.symbols = json.load(f)
        
        print(f"Loaded {len(self.symbols)} processed symbols")
        
        # Extract features (bitfield) and target (NRCI)
        self.X = np.array([
            [s[f"bitfield_d{i}"] for i in range(1, 9)]
            for s in self.symbols
        ])
        
        self.y = np.array([s["nrci"] for s in self.symbols])
        
        # Filter out constant dimensions
        self.stds = self.X.std(axis=0)
        self.varying_dims = self.stds > 0
        self.X_varying = self.X[:, self.varying_dims]
        self.varying_dim_indices = np.where(self.varying_dims)[0]
        
        self.dimension_names = [
            "D1: Arity",
            "D2: Formal Role",
            "D3: Invertibility",
            "D4: Commutativity",
            "D5: Meaning Count (log)",
            "D6: Dependency Depth",
            "D7: Closure Degree",
            "D8: Overloading Index (log)"
        ]
        
        self.varying_dim_names = [self.dimension_names[i] for i in self.varying_dim_indices]
        
        print(f"Feature matrix shape: {self.X_varying.shape}")
        print(f"Target range: [{self.y.min():.6f}, {self.y.max():.6f}]")
        print(f"Using {len(self.varying_dim_names)} varying dimensions: {self.varying_dim_indices.tolist()}")
    
    def train_linear_regression(self) -> Dict:
        """
        Train simple linear regression model.
        
        Returns:
            Dictionary with model results
        """
        from sklearn.linear_model import LinearRegression
        from sklearn.model_selection import cross_val_score, cross_val_predict
        from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error
        
        print("\n" + "="*60)
        print("LINEAR REGRESSION MODEL")
        print("="*60)
        
        # Train model
        model = LinearRegression()
        model.fit(self.X_varying, self.y)
        
        # Predictions
        y_pred = model.predict(self.X_varying)
        
        # Cross-validation (5-fold)
        cv_scores = cross_val_score(model, self.X_varying, self.y, cv=5, scoring='r2')
        y_pred_cv = cross_val_predict(model, self.X_varying, self.y, cv=5)
        
        # Metrics
        r2_train = r2_score(self.y, y_pred)
        r2_cv = cv_scores.mean()
        rmse_train = np.sqrt(mean_squared_error(self.y, y_pred))
        rmse_cv = np.sqrt(mean_squared_error(self.y, y_pred_cv))
        mae_train = mean_absolute_error(self.y, y_pred)
        mae_cv = mean_absolute_error(self.y, y_pred_cv)
        
        print(f"\nModel Performance:")
        print(f"  Training R²: {r2_train:.6f}")
        print(f"  CV R² (5-fold): {r2_cv:.6f} ± {cv_scores.std():.6f}")
        print(f"  Training RMSE: {rmse_train:.8f}")
        print(f"  CV RMSE: {rmse_cv:.8f}")
        print(f"  Training MAE: {mae_train:.8f}")
        print(f"  CV MAE: {mae_cv:.8f}")
        
        print(f"\nModel Coefficients:")
        print(f"  Intercept: {model.intercept_:.6f}")
        for i, coef in enumerate(model.coef_):
            dim_name = self.varying_dim_names[i]
            print(f"  {dim_name:30s}: {coef:+.8f}")
        
        # Feature importance (absolute coefficient values, normalized)
        importance = np.abs(model.coef_)
        importance_norm = importance / importance.sum()
        
        print(f"\nFeature Importance (normalized |coefficient|):")
        sorted_indices = np.argsort(importance_norm)[::-1]
        for idx in sorted_indices:
            dim_name = self.varying_dim_names[idx]
            print(f"  {dim_name:30s}: {importance_norm[idx]*100:5.2f}%")
        
        return {
            "model_type": "LinearRegression",
            "r2_train": float(r2_train),
            "r2_cv": float(r2_cv),
            "r2_cv_std": float(cv_scores.std()),
            "rmse_train": float(rmse_train),
            "rmse_cv": float(rmse_cv),
            "mae_train": float(mae_train),
            "mae_cv": float(mae_cv),
            "intercept": float(model.intercept_),
            "coefficients": {self.varying_dim_names[i]: float(model.coef_[i]) for i in range(len(model.coef_))},
            "feature_importance": {self.varying_dim_names[i]: float(importance_norm[i]) for i in range(len(importance_norm))},
            "predictions": y_pred.tolist(),
            "predictions_cv": y_pred_cv.tolist()
        }
    
    def train_ridge_regression(self, alpha: float = 1.0) -> Dict:
        """
        Train Ridge regression model (L2 regularization).
        
        Args:
            alpha: Regularization strength
            
        Returns:
            Dictionary with model results
        """
        from sklearn.linear_model import Ridge
        from sklearn.model_selection import cross_val_score, cross_val_predict
        from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error
        
        print("\n" + "="*60)
        print(f"RIDGE REGRESSION MODEL (alpha={alpha})")
        print("="*60)
        
        # Train model
        model = Ridge(alpha=alpha)
        model.fit(self.X_varying, self.y)
        
        # Predictions
        y_pred = model.predict(self.X_varying)
        
        # Cross-validation (5-fold)
        cv_scores = cross_val_score(model, self.X_varying, self.y, cv=5, scoring='r2')
        y_pred_cv = cross_val_predict(model, self.X_varying, self.y, cv=5)
        
        # Metrics
        r2_train = r2_score(self.y, y_pred)
        r2_cv = cv_scores.mean()
        rmse_train = np.sqrt(mean_squared_error(self.y, y_pred))
        rmse_cv = np.sqrt(mean_squared_error(self.y, y_pred_cv))
        mae_train = mean_absolute_error(self.y, y_pred)
        mae_cv = mean_absolute_error(self.y, y_pred_cv)
        
        print(f"\nModel Performance:")
        print(f"  Training R²: {r2_train:.6f}")
        print(f"  CV R² (5-fold): {r2_cv:.6f} ± {cv_scores.std():.6f}")
        print(f"  Training RMSE: {rmse_train:.8f}")
        print(f"  CV RMSE: {rmse_cv:.8f}")
        print(f"  Training MAE: {mae_train:.8f}")
        print(f"  CV MAE: {mae_cv:.8f}")
        
        print(f"\nModel Coefficients:")
        print(f"  Intercept: {model.intercept_:.6f}")
        for i, coef in enumerate(model.coef_):
            dim_name = self.varying_dim_names[i]
            print(f"  {dim_name:30s}: {coef:+.8f}")
        
        return {
            "model_type": "Ridge",
            "alpha": alpha,
            "r2_train": float(r2_train),
            "r2_cv": float(r2_cv),
            "r2_cv_std": float(cv_scores.std()),
            "rmse_train": float(rmse_train),
            "rmse_cv": float(rmse_cv),
            "mae_train": float(mae_train),
            "mae_cv": float(mae_cv),
            "intercept": float(model.intercept_),
            "coefficients": {self.varying_dim_names[i]: float(model.coef_[i]) for i in range(len(model.coef_))},
            "predictions": y_pred.tolist(),
            "predictions_cv": y_pred_cv.tolist()
        }
    
    def train_random_forest(self, n_estimators: int = 100) -> Dict:
        """
        Train Random Forest regression model.
        
        Args:
            n_estimators: Number of trees
            
        Returns:
            Dictionary with model results
        """
        from sklearn.ensemble import RandomForestRegressor
        from sklearn.model_selection import cross_val_score, cross_val_predict
        from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error
        
        print("\n" + "="*60)
        print(f"RANDOM FOREST MODEL (n_estimators={n_estimators})")
        print("="*60)
        
        # Train model
        model = RandomForestRegressor(n_estimators=n_estimators, random_state=42, n_jobs=-1)
        model.fit(self.X_varying, self.y)
        
        # Predictions
        y_pred = model.predict(self.X_varying)
        
        # Cross-validation (5-fold)
        cv_scores = cross_val_score(model, self.X_varying, self.y, cv=5, scoring='r2', n_jobs=-1)
        y_pred_cv = cross_val_predict(model, self.X_varying, self.y, cv=5, n_jobs=-1)
        
        # Metrics
        r2_train = r2_score(self.y, y_pred)
        r2_cv = cv_scores.mean()
        rmse_train = np.sqrt(mean_squared_error(self.y, y_pred))
        rmse_cv = np.sqrt(mean_squared_error(self.y, y_pred_cv))
        mae_train = mean_absolute_error(self.y, y_pred)
        mae_cv = mean_absolute_error(self.y, y_pred_cv)
        
        print(f"\nModel Performance:")
        print(f"  Training R²: {r2_train:.6f}")
        print(f"  CV R² (5-fold): {r2_cv:.6f} ± {cv_scores.std():.6f}")
        print(f"  Training RMSE: {rmse_train:.8f}")
        print(f"  CV RMSE: {rmse_cv:.8f}")
        print(f"  Training MAE: {mae_train:.8f}")
        print(f"  CV MAE: {mae_cv:.8f}")
        
        # Feature importance
        importance = model.feature_importances_
        
        print(f"\nFeature Importance:")
        sorted_indices = np.argsort(importance)[::-1]
        for idx in sorted_indices:
            dim_name = self.varying_dim_names[idx]
            print(f"  {dim_name:30s}: {importance[idx]*100:5.2f}%")
        
        return {
            "model_type": "RandomForest",
            "n_estimators": n_estimators,
            "r2_train": float(r2_train),
            "r2_cv": float(r2_cv),
            "r2_cv_std": float(cv_scores.std()),
            "rmse_train": float(rmse_train),
            "rmse_cv": float(rmse_cv),
            "mae_train": float(mae_train),
            "mae_cv": float(mae_cv),
            "feature_importance": {self.varying_dim_names[i]: float(importance[i]) for i in range(len(importance))},
            "predictions": y_pred.tolist(),
            "predictions_cv": y_pred_cv.tolist()
        }
    
    def analyze_residuals(self, model_results: Dict, output_dir: str):
        """
        Analyze residuals for model diagnostics.
        
        Args:
            model_results: Results from a trained model
            output_dir: Directory to save plots
        """
        y_pred = np.array(model_results["predictions"])
        residuals = self.y - y_pred
        
        print("\n" + "="*60)
        print(f"RESIDUAL ANALYSIS - {model_results['model_type']}")
        print("="*60)
        
        print(f"\nResidual Statistics:")
        print(f"  Mean: {residuals.mean():.8f}")
        print(f"  Std: {residuals.std():.8f}")
        print(f"  Min: {residuals.min():.8f}")
        print(f"  Max: {residuals.max():.8f}")
        
        # Normality test
        from scipy.stats import shapiro, normaltest
        shapiro_stat, shapiro_p = shapiro(residuals)
        print(f"\nNormality Tests:")
        print(f"  Shapiro-Wilk: W={shapiro_stat:.6f}, p={shapiro_p:.6e}")
        if shapiro_p > 0.05:
            print(f"    → Residuals appear normally distributed (p > 0.05)")
        else:
            print(f"    → Residuals may not be normally distributed (p < 0.05)")
        
        # Heteroscedasticity test (visual)
        print(f"\nHeteroscedasticity:")
        print(f"  Check residual plot for patterns")
        
        # Create residual plots
        fig, axes = plt.subplots(2, 2, figsize=(12, 10))
        
        # 1. Residuals vs Predicted
        axes[0, 0].scatter(y_pred, residuals, alpha=0.5, s=10)
        axes[0, 0].axhline(y=0, color='r', linestyle='--', linewidth=1)
        axes[0, 0].set_xlabel("Predicted NRCI")
        axes[0, 0].set_ylabel("Residuals")
        axes[0, 0].set_title("Residuals vs Predicted")
        axes[0, 0].grid(True, alpha=0.3)
        
        # 2. Histogram of residuals
        axes[0, 1].hist(residuals, bins=30, edgecolor='black', alpha=0.7)
        axes[0, 1].set_xlabel("Residuals")
        axes[0, 1].set_ylabel("Frequency")
        axes[0, 1].set_title("Residual Distribution")
        axes[0, 1].grid(True, alpha=0.3)
        
        # 3. Q-Q plot
        from scipy.stats import probplot
        probplot(residuals, dist="norm", plot=axes[1, 0])
        axes[1, 0].set_title("Q-Q Plot")
        axes[1, 0].grid(True, alpha=0.3)
        
        # 4. Predicted vs Actual
        axes[1, 1].scatter(self.y, y_pred, alpha=0.5, s=10)
        axes[1, 1].plot([self.y.min(), self.y.max()], [self.y.min(), self.y.max()], 
                       'r--', linewidth=1, label='Perfect prediction')
        axes[1, 1].set_xlabel("Actual NRCI")
        axes[1, 1].set_ylabel("Predicted NRCI")
        axes[1, 1].set_title("Predicted vs Actual")
        axes[1, 1].legend()
        axes[1, 1].grid(True, alpha=0.3)
        
        plt.tight_layout()
        model_name = model_results['model_type'].lower().replace(" ", "_")
        plt.savefig(f"{output_dir}/residuals_{model_name}.png", dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"\nResidual plots saved to: {output_dir}/residuals_{model_name}.png")
    
    def compare_models(self, model_results_list: List[Dict]) -> Dict:
        """
        Compare performance of multiple models.
        
        Args:
            model_results_list: List of model results dictionaries
            
        Returns:
            Comparison summary
        """
        print("\n" + "="*60)
        print("MODEL COMPARISON")
        print("="*60)
        
        print(f"\n{'Model':<20} {'R² (CV)':<12} {'RMSE (CV)':<14} {'MAE (CV)':<14}")
        print("-" * 60)
        
        for results in model_results_list:
            model_name = results['model_type']
            r2_cv = results['r2_cv']
            rmse_cv = results['rmse_cv']
            mae_cv = results['mae_cv']
            print(f"{model_name:<20} {r2_cv:<12.6f} {rmse_cv:<14.8f} {mae_cv:<14.8f}")
        
        # Find best model
        best_model = max(model_results_list, key=lambda x: x['r2_cv'])
        print(f"\nBest model (by CV R²): {best_model['model_type']}")
        print(f"  CV R²: {best_model['r2_cv']:.6f}")
        print(f"  CV RMSE: {best_model['rmse_cv']:.8f}")
        
        return {
            "best_model": best_model['model_type'],
            "best_r2_cv": float(best_model['r2_cv']),
            "best_rmse_cv": float(best_model['rmse_cv'])
        }
    
    def save_results(self, model_results_list: List[Dict], output_path: str):
        """
        Save all model results to JSON.
        
        Args:
            model_results_list: List of model results
            output_path: Path to save results
        """
        results = {
            "dataset_size": len(self.symbols),
            "feature_dimensions": len(self.varying_dim_names),
            "varying_dimensions": self.varying_dim_indices.tolist(),
            "models": model_results_list,
            "comparison": self.compare_models(model_results_list)
        }
        
        with open(output_path, 'w') as f:
            json.dump(results, f, indent=2)
        
        print(f"\nModel results saved to: {output_path}")

def main():
    """Main execution function."""
    print("="*60)
    print("PREDICTIVE MODELING - PHASE 2C")
    print("="*60)
    
    # Initialize modeler
    modeler = PredictiveModeler(
        "/home/ubuntu/ubp_symbol_study_phase2/data/symbols_processed.json"
    )
    
    # Create output directory
    output_dir = "/home/ubuntu/ubp_symbol_study_phase2/results"
    os.makedirs(output_dir, exist_ok=True)
    
    # Train models
    model_results = []
    
    # 1. Linear Regression
    lr_results = modeler.train_linear_regression()
    model_results.append(lr_results)
    modeler.analyze_residuals(lr_results, output_dir)
    
    # 2. Ridge Regression
    ridge_results = modeler.train_ridge_regression(alpha=1.0)
    model_results.append(ridge_results)
    modeler.analyze_residuals(ridge_results, output_dir)
    
    # 3. Random Forest
    rf_results = modeler.train_random_forest(n_estimators=100)
    model_results.append(rf_results)
    modeler.analyze_residuals(rf_results, output_dir)
    
    # Compare models
    modeler.compare_models(model_results)
    
    # Save results
    modeler.save_results(
        model_results,
        f"{output_dir}/predictive_models.json"
    )
    
    print("\n" + "="*60)
    print("PREDICTIVE MODELING COMPLETE")
    print("="*60)

if __name__ == "__main__":
    main()
