"""
VOYAGE 5: COMPREHENSIVE CHEMICAL SEA EXPLORATION
=================================================

Full periodic table analysis with:
- All 118 elements
- 8 measurable properties
- UBP integration
- Predictive α modeling
- Statistical validation

Author: Euan Craig (via Manus AI)
Date: December 9, 2025
"""

import sys
import json
from decimal import Decimal, getcontext
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass, asdict
from collections import defaultdict
import datetime

# Set precision
getcontext().prec = 100

# Import our modules
sys.path.insert(0, '/home/ubuntu/chemical_sea_study')
from code.exact_arithmetic import ExactConstants, ExactArithmetic
from code.data_loader_full import load_periodic_table_full, assign_ubp_clusters, get_property_list, ElementFull

@dataclass
class AlphaPattern:
    """Pattern discovered for a property"""
    element: str
    atomic_number: int
    property_name: str
    measured_value: str  # Decimal as string
    reference_value: str
    optimal_alpha: str  # Fractional exponent
    predicted_value: str
    error_percent: str
    ubp_cluster: int
    ubp_reality: str
    ubp_information: str
    period: int
    group: int

class ComprehensiveVoyage:
    """Comprehensive chemical sea exploration"""
    
    def __init__(self):
        self.Y = ExactConstants.Y
        self.Y_inv = ExactConstants.Y_INVERSE
        self.elements = {}
        self.patterns = []
        self.log_messages = []
        
    def _log(self, message: str):
        """Log message with timestamp"""
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {message}"
        print(log_entry)
        self.log_messages.append(log_entry)
    
    def load_data(self, csv_path: str):
        """Load full periodic table"""
        self._log("=" * 80)
        self._log("VOYAGE 5: COMPREHENSIVE CHEMICAL SEA EXPLORATION")
        self._log("=" * 80)
        self._log(f"Y = {self.Y}")
        self._log(f"Y^(-1) = {self.Y_inv}")
        self._log("=" * 80)
        
        self.elements = load_periodic_table_full(csv_path)
        self.elements = assign_ubp_clusters(self.elements)
        
        self._log(f"Loaded {len(self.elements)} elements")
        
        # Count total measurements
        total_measurements = 0
        for elem in self.elements.values():
            total_measurements += len(get_property_list(elem))
        
        self._log(f"Total property measurements: {total_measurements}")
        self._log("=" * 80)
    
    def solve_alpha(self, measured: Decimal, reference: Decimal) -> Decimal:
        """
        Solve for α in: measured / reference = Y^(-α)
        
        Taking logarithms:
        ln(measured / reference) = -α × ln(Y)
        α = -ln(measured / reference) / ln(Y)
        """
        if measured <= 0 or reference <= 0:
            return Decimal(0)
        
        ratio = measured / reference
        if ratio == 1:
            return Decimal(0)
        
        ln_ratio = ExactArithmetic.ln(ratio)
        ln_Y = ExactArithmetic.ln(self.Y)
        
        alpha = -ln_ratio / ln_Y
        return alpha
    
    def predict_from_alpha(self, alpha: Decimal, reference: Decimal) -> Decimal:
        """Predict value from α: value = reference × Y^(-α)"""
        # Use logarithmic computation to avoid overflow
        # Y^(-α) = exp(-α × ln(Y))
        
        ln_Y = ExactArithmetic.ln(self.Y)
        exponent = -alpha * ln_Y
        scaling = ExactArithmetic.exp(exponent)
        
        return reference * scaling
    
    def compute_error(self, measured: Decimal, predicted: Decimal) -> Decimal:
        """Compute relative error percentage"""
        if measured == 0:
            return Decimal(0)
        return abs(measured - predicted) / measured * Decimal(100)
    
    def cast_net(self):
        """Cast the net across all elements and properties"""
        self._log("\n" + "=" * 80)
        self._log("CASTING NET ACROSS FULL PERIODIC TABLE")
        self._log("=" * 80)
        
        # Group properties by type to determine references
        property_values = defaultdict(list)
        for elem in self.elements.values():
            for prop_name, prop_value in get_property_list(elem):
                property_values[prop_name].append((elem.symbol, prop_value))
        
        # Choose reference values (use hydrogen or lightest element with data)
        references = {}
        for prop_name, values in property_values.items():
            # Try to use H, otherwise use first available
            h_value = next((v for s, v in values if s == 'H'), None)
            if h_value:
                references[prop_name] = ('H', h_value)
            else:
                # Use smallest value as reference
                values_sorted = sorted(values, key=lambda x: x[1])
                references[prop_name] = values_sorted[0]
        
        self._log("\nReference values:")
        for prop_name, (ref_symbol, ref_value) in references.items():
            self._log(f"  {prop_name:20s}: {ref_symbol} = {ref_value}")
        
        # Compute α for all measurements
        self._log("\n" + "=" * 80)
        self._log("COMPUTING ALPHA VALUES")
        self._log("=" * 80)
        
        for elem in sorted(self.elements.values(), key=lambda e: e.atomic_number):
            properties = get_property_list(elem)
            if not properties:
                continue
            
            for prop_name, measured_value in properties:
                if prop_name not in references:
                    continue
                
                ref_symbol, ref_value = references[prop_name]
                
                # Solve for α
                alpha = self.solve_alpha(measured_value, ref_value)
                
                # Predict value (should match measured exactly)
                predicted_value = self.predict_from_alpha(alpha, ref_value)
                
                # Compute error (should be ~0)
                error_pct = self.compute_error(measured_value, predicted_value)
                
                # Store pattern
                pattern = AlphaPattern(
                    element=elem.symbol,
                    atomic_number=elem.atomic_number,
                    property_name=prop_name,
                    measured_value=str(measured_value),
                    reference_value=str(ref_value),
                    optimal_alpha=str(alpha),
                    predicted_value=str(predicted_value),
                    error_percent=str(error_pct),
                    ubp_cluster=elem.ubp_cluster,
                    ubp_reality=str(elem.ubp_reality_layer),
                    ubp_information=str(elem.ubp_information_layer),
                    period=elem.period,
                    group=elem.group,
                )
                
                self.patterns.append(pattern)
        
        self._log(f"\nTotal patterns computed: {len(self.patterns)}")
        
        # Summary statistics
        self._log("\n" + "=" * 80)
        self._log("ALPHA DISTRIBUTION SUMMARY")
        self._log("=" * 80)
        
        alphas_by_property = defaultdict(list)
        for p in self.patterns:
            alphas_by_property[p.property_name].append(float(p.optimal_alpha))
        
        for prop_name in sorted(alphas_by_property.keys()):
            alphas = alphas_by_property[prop_name]
            self._log(f"\n{prop_name}:")
            self._log(f"  Count: {len(alphas)}")
            self._log(f"  Range: [{min(alphas):+.6f}, {max(alphas):+.6f}]")
            self._log(f"  Mean: {sum(alphas)/len(alphas):+.6f}")
            std = (sum((a - sum(alphas)/len(alphas))**2 for a in alphas) / len(alphas))**0.5
            self._log(f"  Std Dev: {std:.6f}")
    
    def analyze_patterns(self):
        """Analyze discovered patterns"""
        self._log("\n" + "=" * 80)
        self._log("PATTERN ANALYSIS")
        self._log("=" * 80)
        
        # 1. Alpha by period
        self._log("\n1. ALPHA BY PERIOD")
        self._log("-" * 80)
        
        for prop_name in ['first_ionization', 'atomic_radius', 'electronegativity']:
            period_alphas = defaultdict(list)
            for p in self.patterns:
                if p.property_name == prop_name:
                    period_alphas[p.period].append(float(p.optimal_alpha))
            
            if period_alphas:
                self._log(f"\n{prop_name}:")
                for period in sorted(period_alphas.keys()):
                    alphas = period_alphas[period]
                    avg = sum(alphas) / len(alphas)
                    self._log(f"  Period {period}: n={len(alphas):3d}, avg α = {avg:+.6f}")
        
        # 2. Alpha by UBP cluster
        self._log("\n2. ALPHA BY UBP CLUSTER")
        self._log("-" * 80)
        
        cluster_alphas = defaultdict(lambda: defaultdict(list))
        for p in self.patterns:
            if p.ubp_cluster >= 0:  # Only assigned clusters
                cluster_alphas[p.ubp_cluster][p.property_name].append(float(p.optimal_alpha))
        
        for cluster_id in sorted(cluster_alphas.keys()):
            self._log(f"\nCluster {cluster_id}:")
            for prop_name in sorted(cluster_alphas[cluster_id].keys()):
                alphas = cluster_alphas[cluster_id][prop_name]
                avg = sum(alphas) / len(alphas)
                self._log(f"  {prop_name:20s}: n={len(alphas):2d}, avg α = {avg:+.6f}")
        
        # 3. Correlations between properties
        self._log("\n3. CROSS-PROPERTY CORRELATIONS")
        self._log("-" * 80)
        
        # Build element-property matrix
        elem_alphas = defaultdict(dict)
        for p in self.patterns:
            elem_alphas[p.element][p.property_name] = float(p.optimal_alpha)
        
        # Compute correlations
        prop_pairs = [
            ('first_ionization', 'atomic_radius'),
            ('first_ionization', 'electronegativity'),
            ('atomic_radius', 'electronegativity'),
            ('density', 'atomic_mass'),
            ('melting_point', 'boiling_point'),
        ]
        
        for prop1, prop2 in prop_pairs:
            pairs = []
            for elem, props in elem_alphas.items():
                if prop1 in props and prop2 in props:
                    pairs.append((props[prop1], props[prop2]))
            
            if len(pairs) >= 3:
                alphas1 = [p[0] for p in pairs]
                alphas2 = [p[1] for p in pairs]
                
                mean1 = sum(alphas1) / len(alphas1)
                mean2 = sum(alphas2) / len(alphas2)
                
                cov = sum((a1 - mean1) * (a2 - mean2) for a1, a2 in pairs) / len(pairs)
                std1 = (sum((a1 - mean1)**2 for a1 in alphas1) / len(alphas1))**0.5
                std2 = (sum((a2 - mean2)**2 for a2 in alphas2) / len(alphas2))**0.5
                
                corr = cov / (std1 * std2) if std1 > 0 and std2 > 0 else 0
                
                self._log(f"\n{prop1} vs {prop2}:")
                self._log(f"  Samples: {len(pairs)}")
                self._log(f"  Correlation: {corr:+.4f}")
                if abs(corr) > 0.7:
                    self._log(f"  *** STRONG CORRELATION ***")
    
    def save_results(self, output_path: str):
        """Save results to JSON"""
        results = {
            'voyage': 5,
            'timestamp': datetime.datetime.now().isoformat(),
            'total_elements': len(self.elements),
            'total_patterns': len(self.patterns),
            'patterns': [asdict(p) for p in self.patterns],
            'log': self.log_messages,
        }
        
        with open(output_path, 'w') as f:
            json.dump(results, f, indent=2)
        
        self._log(f"\nResults saved to {output_path}")

# ============================================================================
# MAIN EXECUTION
# ============================================================================

if __name__ == "__main__":
    voyage = ComprehensiveVoyage()
    
    # Load data
    voyage.load_data("/home/ubuntu/chemical_sea_study/data/periodic_table_full_118.csv")
    
    # Cast net
    voyage.cast_net()
    
    # Analyze patterns
    voyage.analyze_patterns()
    
    # Save results
    voyage.save_results("/home/ubuntu/chemical_sea_study/results/voyage_5_comprehensive.json")
    
    print("\n" + "=" * 80)
    print("VOYAGE 5 COMPLETE")
    print("=" * 80)
