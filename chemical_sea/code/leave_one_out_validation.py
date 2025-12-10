#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Leave-One-Out Cross-Validation (LOOCV) for The Chemical Sea Study.

This script performs a rigorous, out-of-sample validation of the alpha prediction
framework. For each element, it trains a regression model on all other elements
and then predicts the properties of the held-out element.

This addresses the critical feedback from Deepseek AI to demonstrate true
predictive power, not just self-consistent fitting.
"""

import json
from decimal import Decimal, getcontext

from data_loader_final_json import load_periodic_table_from_json
from exact_arithmetic import ExactArithmetic, ExactConstants

# Set precision for Decimal
getcontext().prec = 100

class LeaveOneOutValidator:
    """Performs LOOCV on the chemical sea dataset."""

    def __init__(self):
        self.elements_raw = load_periodic_table_from_json('../data/PeriodicTableJSON.json')
        self.elements = self._create_element_objects(self.elements_raw)
        self.ea = ExactArithmetic()
        self.properties_to_test = [
            'atomic_mass',
            'atomic_radius',
            'first_ionization_energy',
            'electron_affinity',
            'electronegativity_pauling',
            'melting_point',
            'boiling_point',
            'density'
        ]
        self.reference_element = next(e for e in self.elements if e.symbol == 'H')

    def _create_element_objects(self, raw_data):
        """Converts raw dicts to objects for easier attribute access."""
        class Element:
            def __init__(self, data):
                for key, value in data.items():
                    # Convert camelCase to snake_case for attribute names
                    import re
                    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', key)
                    snake_case_key = re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()
                    setattr(self, snake_case_key, value)
        return [Element(e) for e in raw_data]

    def get_alpha(self, element, prop_name):
        """Calculates alpha for a given element and property."""
        p_ref_val = getattr(self.reference_element, prop_name, None)
        p_val = getattr(element, prop_name, None)

        if p_val is None or p_ref_val is None or p_val <= 0 or p_ref_val <= 0:
            return None

        p_ratio = Decimal(p_val) / Decimal(p_ref_val)
        if p_ratio == 1:
            return Decimal(0)

        

        alpha = -self.ea.log(p_ratio, ExactConstants.Y)
        return alpha

    def build_regression_model(self, training_set, prop_name):
        """Builds a simple linear regression model to predict alpha."""
        features = []
        targets = []

        for element in training_set:
            alpha = self.get_alpha(element, prop_name)
            if alpha is not None:
                targets.append(alpha)
                features.append([
                    Decimal(1),  # Intercept
                    Decimal(element.period),
                    Decimal(element.period) ** 2,
                    Decimal(element.number),
                    Decimal(element.number) / 2, # Reality Layer
                    Decimal(element.atomic_mass) / 5, # Information Layer
                ])

        if len(features) < 2:
            return None # Not enough data to build a model

        # Simple linear regression using normal equation (for demonstration)
        # A more robust implementation would use a library like statsmodels
        # For now, we'll use a simplified model focusing on the main feature: Period
        
        # Simplified model: alpha ~ c0 + c1*Period
        sum_x = sum(f[1] for f in features)
        sum_y = sum(targets)
        sum_x2 = sum(f[1]**2 for f in features)
        sum_xy = sum(f[1] * y for f, y in zip(features, targets))
        n = Decimal(len(features))

        try:
            c1 = (n * sum_xy - sum_x * sum_y) / (n * sum_x2 - sum_x**2)
            c0 = (sum_y - c1 * sum_x) / n
            return {'c0': c0, 'c1': c1}
        except Exception:
            return None

    def predict_alpha(self, model, element):
        """Predicts alpha for an element using the trained model."""
        if model is None:
            return None
        # Simplified prediction
        return model['c0'] + model['c1'] * Decimal(element.period)

    def run_validation(self):
        """Runs the full LOOCV process."""
        results = {prop: [] for prop in self.properties_to_test}

        for prop_name in self.properties_to_test:
            print(f"Validating property: {prop_name}...")
            elements_with_prop = [e for e in self.elements if getattr(e, prop_name, None) is not None]

            for i, held_out_element in enumerate(elements_with_prop):
                training_set = elements_with_prop[:i] + elements_with_prop[i+1:]

                # 1. Build model on training set
                model = self.build_regression_model(training_set, prop_name)
                if model is None:
                    continue

                # 2. Predict alpha for the held-out element
                predicted_alpha = self.predict_alpha(model, held_out_element)
                if predicted_alpha is None:
                    continue

                # 3. Calculate predicted property value
                p_ref_val = getattr(self.reference_element, prop_name)
                predicted_p = Decimal(p_ref_val) * (ExactConstants.Y ** -predicted_alpha)

                # 4. Compare with actual value
                actual_p = Decimal(getattr(held_out_element, prop_name))
                error = abs(predicted_p - actual_p) / actual_p

                results[prop_name].append({
                    'element': held_out_element.symbol,
                    'atomic_number': held_out_element.number,
                    'actual_p': float(actual_p),
                    'predicted_p': float(predicted_p),
                    'mape': float(error)
                })

        # Calculate and save summary
        summary = {}
        for prop_name, prop_results in results.items():
            if not prop_results:
                continue
            avg_mape = sum(r['mape'] for r in prop_results) / len(prop_results)
            summary[prop_name] = {'average_mape': avg_mape, 'count': len(prop_results)}
            print(f"  - {prop_name}: Average MAPE = {avg_mape:.4f} across {len(prop_results)} elements")

        with open('../results/loocv_summary.json', 'w') as f:
            json.dump(summary, f, indent=4)
        
        with open('../results/loocv_full_results.json', 'w') as f:
            json.dump(results, f, indent=4)

        print("\nLOOCV validation complete. Results saved to results/loocv_summary.json")

if __name__ == "__main__":
    validator = LeaveOneOutValidator()
    validator.run_validation()
