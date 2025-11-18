#!/usr/bin/env python3.11
"""
Novel Symbol Generator - Phase 2E
Generate and test novel mathematical operators based on theoretical framework

This module:
1. Designs novel symbols optimized for high coherence
2. Designs control symbols with predicted low coherence
3. Computes actual coherence using UBP 3.5
4. Validates theoretical predictions against empirical measurements
"""

import sys
sys.path.append('/home/ubuntu/ubp_symbol_study_phase2/ubp_3.5')

import json
import numpy as np
from typing import Dict, List, Tuple
from coherence_substrate_v2 import CoherenceState
from symbol_encoding import SymbolEncoder
from symbol_coherence_model import SymbolCoherenceModel

class NovelSymbolGenerator:
    """
    Generate and test novel mathematical symbol operators.
    """
    
    def __init__(self):
        """Initialize the generator."""
        self.encoder = SymbolEncoder()
        self.coherence_model = SymbolCoherenceModel(
            refinement_scale=1.0,
            degradation_scale=500.0
        )
        
        print("Initialized NovelSymbolGenerator")
        print("  Using UBP 3.5 coherence substrate")
        print("  Calibrated scales: refinement=1.0, degradation=500.0")
    
    def design_high_coherence_symbols(self) -> List[Dict]:
        """
        Design novel symbols optimized for high coherence.
        
        Based on theoretical framework:
        - Minimum ambiguity (single meaning, no overloading)
        - Minimum compositionality (atomic or simple)
        - High structural regularity (fixed arity, clear role)
        
        Returns:
            List of symbol definitions
        """
        print("\n" + "="*60)
        print("DESIGNING HIGH-COHERENCE SYMBOLS")
        print("="*60)
        
        symbols = [
            {
                "symbol": "⊕",
                "name": "circle_plus",
                "unicode": "U+2295",
                "category": "novel_high_coherence",
                "description": "Novel commutative binary operator (atomic, unambiguous)",
                "arity": "binary",
                "formal_role": "operator",
                "invertibility": "none",
                "commutativity": "yes",
                "meaning_count": 1,
                "dependency_depth": 1,
                "closure_degree": "medium",
                "overloading_count": 0
            },
            {
                "symbol": "⊙",
                "name": "circle_dot",
                "unicode": "U+2299",
                "category": "novel_high_coherence",
                "description": "Novel unary operator (atomic, unambiguous)",
                "arity": "unary",
                "formal_role": "operator",
                "invertibility": "none",
                "commutativity": "no",
                "meaning_count": 1,
                "dependency_depth": 1,
                "closure_degree": "medium",
                "overloading_count": 0
            },
            {
                "symbol": "⋈",
                "name": "double_triangle",
                "unicode": "U+22C8",
                "category": "novel_high_coherence",
                "description": "Novel binary relation (atomic, unambiguous)",
                "arity": "binary",
                "formal_role": "relation",
                "invertibility": "none",
                "commutativity": "yes",
                "meaning_count": 1,
                "dependency_depth": 1,
                "closure_degree": "medium",
                "overloading_count": 0
            },
            {
                "symbol": "⋄",
                "name": "diamond",
                "unicode": "U+22C4",
                "category": "novel_high_coherence",
                "description": "Novel nullary constant (atomic, unambiguous)",
                "arity": "nullary",
                "formal_role": "operand",
                "invertibility": "none",
                "commutativity": "no",
                "meaning_count": 1,
                "dependency_depth": 1,
                "closure_degree": "medium",
                "overloading_count": 0
            },
            {
                "symbol": "⋆",
                "name": "star",
                "unicode": "U+22C6",
                "category": "novel_high_coherence",
                "description": "Novel commutative binary operator (simple, unambiguous)",
                "arity": "binary",
                "formal_role": "operator",
                "invertibility": "none",
                "commutativity": "yes",
                "meaning_count": 1,
                "dependency_depth": 2,
                "closure_degree": "medium",
                "overloading_count": 0
            }
        ]
        
        print(f"\nDesigned {len(symbols)} high-coherence symbols:")
        for s in symbols:
            print(f"  {s['symbol']} ({s['name']}): {s['description']}")
        
        return symbols
    def design_low_coherence_symbols(self) -> List[Dict]:
        """
        Design control symbols predicted to have low coherence.
        
        Based on theoretical framework:
        - High ambiguity (multiple meanings, overloading)
        - High compositionality (complex dependencies)
        - Low structural regularity
        
        Returns:
            List of symbol definitions
        """
        print("\n" + "="*60)
        print("DESIGNING LOW-COHERENCE SYMBOLS (CONTROLS)")
        print("="*60)
        
        symbols = [
            {
                "symbol": "⋆⋆",
                "name": "double_star",
                "unicode": "U+22C6_U+22C6",
                "category": "novel_low_coherence",
                "description": "Overloaded operator with multiple meanings",
                "arity": "binary",
                "formal_role": "operator",
                "invertibility": "none",
                "commutativity": "no",
                "meaning_count": 5,
                "dependency_depth": 3,
                "closure_degree": "medium",
                "overloading_count": 4
            },
            {
                "symbol": "⟪⟫",
                "name": "triple_bracket",
                "unicode": "U+27EA_U+27EB",
                "category": "novel_low_coherence",
                "description": "Complex composite operator with deep dependencies",
                "arity": "binary",
                "formal_role": "operator",
                "invertibility": "none",
                "commutativity": "no",
                "meaning_count": 3,
                "dependency_depth": 3,
                "closure_degree": "medium",
                "overloading_count": 2
            },
            {
                "symbol": "≋",
                "name": "triple_tilde",
                "unicode": "U+224B",
                "category": "novel_low_coherence",
                "description": "Ambiguous relation with multiple interpretations",
                "arity": "binary",
                "formal_role": "relation",
                "invertibility": "none",
                "commutativity": "yes",
                "meaning_count": 4,
                "dependency_depth": 2,
                "closure_degree": "medium",
                "overloading_count": 3
            },
            {
                "symbol": "⋘⋙",
                "name": "triple_angle",
                "unicode": "U+22D8_U+22D9",
                "category": "novel_low_coherence",
                "description": "Complex ternary operator with deep dependencies",
                "arity": "ternary",
                "formal_role": "operator",
                "invertibility": "none",
                "commutativity": "no",
                "meaning_count": 3,
                "dependency_depth": 3,
                "closure_degree": "medium",
                "overloading_count": 2
            },
            {
                "symbol": "∃∃",
                "name": "double_exists",
                "unicode": "U+2203_U+2203",
                "category": "novel_low_coherence",
                "description": "Overloaded quantifier with multiple interpretations",
                "arity": "unary",
                "formal_role": "quantifier",
                "invertibility": "none",
                "commutativity": "no",
                "meaning_count": 4,
                "dependency_depth": 3,
                "closure_degree": "medium",
                "overloading_count": 3
            }
        ]
        
        print(f"\nDesigned {len(symbols)} low-coherence symbols:")
        for s in symbols:
            print(f"  {s['symbol']} ({s['name']}): {s['description']}")
        
        return symbols
    def compute_coherence_for_novel_symbols(self, symbols: List[Dict]) -> List[Dict]:
        """
        Encode and compute coherence for novel symbols.
        
        Args:
            symbols: List of symbol definitions
            
        Returns:
            List of symbols with computed coherence features
        """
        print("\n" + "="*60)
        print("COMPUTING COHERENCE FOR NOVEL SYMBOLS")
        print("="*60)
        
        # Encode symbols
        processed_symbols = []
        for symbol in symbols:
            # Encode symbol (returns tuple)
            unicode_seed, bitfield, bitfield_magnitude, coherence_state = self.encoder.encode_symbol(symbol)
            
            # Format as dictionary for coherence model
            encoded_dict = {
                "symbol": symbol["symbol"],
                "name": symbol["name"],
                "unicode": symbol["unicode"],
                "category": symbol["category"],
                "initial_value": unicode_seed,
                "bitfield": bitfield.tolist(),
                "bitfield_magnitude": bitfield_magnitude,
                "initial_nrci": coherence_state.nrci,
                "properties": {
                    "arity": symbol["arity"],
                    "formal_role": symbol["formal_role"],
                    "invertibility": symbol["invertibility"],
                    "commutativity": symbol["commutativity"],
                    "meaning_count": symbol["meaning_count"],
                    "dependency_depth": symbol["dependency_depth"],
                    "closure_degree": symbol["closure_degree"],
                    "overloading_count": symbol["overloading_count"]
                }
            }
            
            # Compute coherence features
            features = self.coherence_model.compute_coherence_features(encoded_dict)
            processed_symbols.append(features)
        
        print(f"\nProcessed {len(processed_symbols)} novel symbols")
        
        return processed_symbols
    
    def predict_coherence_from_bitfield(self, symbol_data: Dict, model_coefs: Dict) -> float:
        """
        Predict NRCI using the trained linear regression model.
        
        Args:
            symbol_data: Processed symbol data with bitfield_d1-d8 keys
            model_coefs: Model coefficients from predictive_models.json
            
        Returns:
            Predicted NRCI
        """
        # Extract bitfield from separate keys
        bitfield_varying = np.array([
            symbol_data["bitfield_d1"],
            symbol_data["bitfield_d2"],
            symbol_data["bitfield_d4"],
            symbol_data["bitfield_d5"],
            symbol_data["bitfield_d6"],
            symbol_data["bitfield_d8"]
        ])
        
        # Apply linear model
        intercept = model_coefs["intercept"]
        coefs = [
            model_coefs["D1: Arity"],
            model_coefs["D2: Formal Role"],
            model_coefs["D4: Commutativity"],
            model_coefs["D5: Meaning Count (log)"],
            model_coefs["D6: Dependency Depth"],
            model_coefs["D8: Overloading Index (log)"]
        ]
        
        predicted_nrci = intercept + np.dot(bitfield_varying, coefs)
        
        return predicted_nrci
    
    def validate_predictions(self, processed_symbols: List[Dict], model_path: str) -> Dict:
        """
        Validate theoretical predictions against empirical measurements.
        
        Args:
            processed_symbols: Symbols with computed coherence
            model_path: Path to predictive_models.json
            
        Returns:
            Validation results
        """
        print("\n" + "="*60)
        print("VALIDATING THEORETICAL PREDICTIONS")
        print("="*60)
        
        # Load model coefficients
        with open(model_path, 'r') as f:
            model_data = json.load(f)
        
        # Get linear regression coefficients
        lr_model = [m for m in model_data["models"] if m["model_type"] == "LinearRegression"][0]
        coefs = lr_model["coefficients"]
        intercept = lr_model["intercept"]
        
        model_coefs = {
            "intercept": intercept,
            **coefs
        }
        
        # Predict and compare
        results = []
        for symbol in processed_symbols:
            predicted_nrci = self.predict_coherence_from_bitfield(symbol, model_coefs)
            actual_nrci = symbol["nrci"]
            error = actual_nrci - predicted_nrci
            relative_error = abs(error / actual_nrci) * 100
            
            results.append({
                "symbol": symbol["symbol"],
                "name": symbol["name"],
                "category": symbol["category"],
                "predicted_nrci": float(predicted_nrci),
                "actual_nrci": float(actual_nrci),
                "error": float(error),
                "relative_error_pct": float(relative_error)
            })
            
            print(f"\n{symbol['symbol']} ({symbol['name']}):")
            print(f"  Category: {symbol['category']}")
            print(f"  Predicted NRCI: {predicted_nrci:.6f}")
            print(f"  Actual NRCI: {actual_nrci:.6f}")
            print(f"  Error: {error:+.6f} ({relative_error:.2f}%)")
        
        # Compute aggregate statistics
        errors = [r["error"] for r in results]
        relative_errors = [r["relative_error_pct"] for r in results]
        
        print("\n" + "-"*60)
        print("AGGREGATE VALIDATION STATISTICS")
        print("-"*60)
        print(f"Mean absolute error: {np.mean(np.abs(errors)):.6f}")
        print(f"Mean relative error: {np.mean(relative_errors):.2f}%")
        print(f"Max absolute error: {np.max(np.abs(errors)):.6f}")
        print(f"Max relative error: {np.max(relative_errors):.2f}%")
        
        # Separate by category
        high_coherence = [r for r in results if r["category"] == "novel_high_coherence"]
        low_coherence = [r for r in results if r["category"] == "novel_low_coherence"]
        
        print(f"\nHigh-coherence symbols:")
        print(f"  Mean actual NRCI: {np.mean([r['actual_nrci'] for r in high_coherence]):.6f}")
        print(f"  Mean predicted NRCI: {np.mean([r['predicted_nrci'] for r in high_coherence]):.6f}")
        
        print(f"\nLow-coherence symbols:")
        print(f"  Mean actual NRCI: {np.mean([r['actual_nrci'] for r in low_coherence]):.6f}")
        print(f"  Mean predicted NRCI: {np.mean([r['predicted_nrci'] for r in low_coherence]):.6f}")
        
        # Test hypothesis: high-coherence > low-coherence
        from scipy.stats import ttest_ind
        high_nrcis = [r['actual_nrci'] for r in high_coherence]
        low_nrcis = [r['actual_nrci'] for r in low_coherence]
        t_stat, p_value = ttest_ind(high_nrcis, low_nrcis)
        
        print(f"\nHypothesis test (high > low):")
        print(f"  t-statistic: {t_stat:.4f}")
        print(f"  p-value: {p_value:.6f}")
        if p_value < 0.05:
            print(f"  → Significant difference (p < 0.05)")
        else:
            print(f"  → No significant difference (p >= 0.05)")
        
        return {
            "results": results,
            "mean_absolute_error": float(np.mean(np.abs(errors))),
            "mean_relative_error_pct": float(np.mean(relative_errors)),
            "high_coherence_mean_nrci": float(np.mean(high_nrcis)),
            "low_coherence_mean_nrci": float(np.mean(low_nrcis)),
            "t_statistic": float(t_stat),
            "p_value": float(p_value)
        }
    
    def save_results(self, processed_symbols: List[Dict], validation: Dict, output_path: str):
        """
        Save novel symbol results to JSON.
        
        Args:
            processed_symbols: Symbols with computed coherence
            validation: Validation results
            output_path: Path to save results
        """
        results = {
            "novel_symbols": processed_symbols,
            "validation": validation
        }
        
        with open(output_path, 'w') as f:
            json.dump(results, f, indent=2)
        
        print(f"\nNovel symbol results saved to: {output_path}")

def main():
    """Main execution function."""
    print("="*60)
    print("NOVEL SYMBOL GENERATION & TESTING - PHASE 2E")
    print("="*60)
    
    # Initialize generator
    generator = NovelSymbolGenerator()
    
    # Design symbols
    high_coherence_symbols = generator.design_high_coherence_symbols()
    low_coherence_symbols = generator.design_low_coherence_symbols()
    
    all_novel_symbols = high_coherence_symbols + low_coherence_symbols
    
    # Compute coherence
    processed_symbols = generator.compute_coherence_for_novel_symbols(all_novel_symbols)
    
    # Validate predictions
    validation = generator.validate_predictions(
        processed_symbols,
        "/home/ubuntu/ubp_symbol_study_phase2/results/predictive_models.json"
    )
    
    # Save results
    generator.save_results(
        processed_symbols,
        validation,
        "/home/ubuntu/ubp_symbol_study_phase2/results/novel_symbols.json"
    )
    
    print("\n" + "="*60)
    print("NOVEL SYMBOL GENERATION COMPLETE")
    print("="*60)

if __name__ == "__main__":
    main()
