"""
Deep Data Analysis of Computational Grammar Dataset
====================================================

Comprehensive analysis to extract every possible insight from 611 operators.

Analysis Goals:
1. Find hidden patterns in OffBit structure
2. Discover correlations between D-variables
3. Identify operator evolution pathways
4. Analyze category relationships
5. Find predictive rules for operator design
6. Uncover anomalies and outliers
7. Build operator genealogy trees
8. Extract composition algebra
"""

import json
import math
from collections import defaultdict, Counter
from pathlib import Path


def load_data():
    """Load all datasets."""
    with open('/home/ubuntu/comprehensive_operator_dataset.json') as f:
        operators = json.load(f)
    
    with open('/home/ubuntu/offbit_family_analysis.json') as f:
        families = json.load(f)
    
    with open('/home/ubuntu/noble_operators.json') as f:
        nobles = json.load(f)
    
    with open('/home/ubuntu/operator_taxonomy.json') as f:
        taxonomy = json.load(f)
    
    return operators, families, nobles, taxonomy


def analyze_offbit_bit_patterns(operators):
    """Deep analysis of individual bit positions in OffBit structure."""
    print("\n" + "="*80)
    print("ANALYSIS 1: OffBit Bit-Level Patterns")
    print("="*80)
    
    # Filter operators with OffBit data
    valid_ops = [op for op in operators if 'offbit_binary' in op]
    
    print(f"\nAnalyzing {len(valid_ops)} operators with OffBit data")
    
    # Analyze each bit position
    bit_stats = []
    
    for bit_pos in range(24):
        ones = sum(1 for op in valid_ops if op['offbit_binary'][bit_pos] == '1')
        zeros = len(valid_ops) - ones
        entropy = 0
        if ones > 0 and zeros > 0:
            p1 = ones / len(valid_ops)
            p0 = zeros / len(valid_ops)
            entropy = -(p1 * math.log2(p1) + p0 * math.log2(p0))
        
        bit_stats.append({
            'position': bit_pos,
            'ones': ones,
            'zeros': zeros,
            'ones_pct': 100 * ones / len(valid_ops),
            'entropy': entropy
        })
    
    # Print by layer
    print("\n" + "-"*80)
    print("Reality Layer (Bits 0-5):")
    print(f"{'Bit':<5} {'Ones':<8} {'Zeros':<8} {'Ones %':<10} {'Entropy':<10} {'Interpretation'}")
    print("-"*80)
    
    for i in range(6):
        bs = bit_stats[i]
        interp = "Hardware/IO (currently unused)" if i < 6 else ""
        print(f"{bs['position']:<5} {bs['ones']:<8} {bs['zeros']:<8} {bs['ones_pct']:<10.1f} {bs['entropy']:<10.3f} {interp}")
    
    print("\n" + "-"*80)
    print("Information Layer (Bits 6-11): Structure (D1, D2, D4)")
    print(f"{'Bit':<5} {'Ones':<8} {'Zeros':<8} {'Ones %':<10} {'Entropy':<10} {'Interpretation'}")
    print("-"*80)
    
    interpretations = {
        6: "Arity bit 1",
        7: "Arity bit 0",
        8: "Role bit 2",
        9: "Role bit 1",
        10: "Role bit 0",
        11: "Commutativity"
    }
    
    for i in range(6, 12):
        bs = bit_stats[i]
        interp = interpretations.get(i, "")
        print(f"{bs['position']:<5} {bs['ones']:<8} {bs['zeros']:<8} {bs['ones_pct']:<10.1f} {bs['entropy']:<10.3f} {interp}")
    
    print("\n" + "-"*80)
    print("Activation Layer (Bits 12-17): Processing (D3, D7)")
    print(f"{'Bit':<5} {'Ones':<8} {'Zeros':<8} {'Ones %':<10} {'Entropy':<10} {'Interpretation'}")
    print("-"*80)
    
    interpretations = {
        12: "Invertibility bit 1",
        13: "Invertibility bit 0",
        14: "Closure bit 1",
        15: "Closure bit 0",
        16: "Reserved",
        17: "Reserved"
    }
    
    for i in range(12, 18):
        bs = bit_stats[i]
        interp = interpretations.get(i, "")
        print(f"{bs['position']:<5} {bs['ones']:<8} {bs['zeros']:<8} {bs['ones_pct']:<10.1f} {bs['entropy']:<10.3f} {interp}")
    
    print("\n" + "-"*80)
    print("Unactivated Layer (Bits 18-23): Potential (D5, D6, D8)")
    print(f"{'Bit':<5} {'Ones':<8} {'Zeros':<8} {'Ones %':<10} {'Entropy':<10} {'Interpretation'}")
    print("-"*80)
    
    interpretations = {
        18: "Meaning count bit 1",
        19: "Meaning count bit 0",
        20: "Dependency depth bit 1",
        21: "Dependency depth bit 0",
        22: "Overloading bit 1",
        23: "Overloading bit 0"
    }
    
    for i in range(18, 24):
        bs = bit_stats[i]
        interp = interpretations.get(i, "")
        print(f"{bs['position']:<5} {bs['ones']:<8} {bs['zeros']:<8} {bs['ones_pct']:<10.1f} {bs['entropy']:<10.3f} {interp}")
    
    # Find highest entropy bits (most informative)
    sorted_bits = sorted(bit_stats, key=lambda x: x['entropy'], reverse=True)
    
    print("\n" + "-"*80)
    print("Most Informative Bits (Highest Entropy):")
    print(f"{'Rank':<6} {'Bit':<6} {'Entropy':<10} {'Layer':<20} {'Interpretation'}")
    print("-"*80)
    
    layer_names = {
        range(0, 6): "Reality",
        range(6, 12): "Information",
        range(12, 18): "Activation",
        range(18, 24): "Unactivated"
    }
    
    for rank, bs in enumerate(sorted_bits[:10], 1):
        bit_pos = bs['position']
        layer = next((name for r, name in layer_names.items() if bit_pos in r), "Unknown")
        
        # Get interpretation
        all_interps = {
            6: "Arity bit 1", 7: "Arity bit 0",
            8: "Role bit 2", 9: "Role bit 1", 10: "Role bit 0",
            11: "Commutativity",
            12: "Invertibility bit 1", 13: "Invertibility bit 0",
            14: "Closure bit 1", 15: "Closure bit 0",
            18: "Meaning count bit 1", 19: "Meaning count bit 0",
            20: "Dependency depth bit 1", 21: "Dependency depth bit 0",
            22: "Overloading bit 1", 23: "Overloading bit 0"
        }
        
        interp = all_interps.get(bit_pos, "Unused/Reserved")
        
        print(f"{rank:<6} {bit_pos:<6} {bs['entropy']:<10.3f} {layer:<20} {interp}")
    
    return bit_stats


def analyze_d_variable_correlations_matrix(operators):
    """Compute full correlation matrix between all D-variables."""
    print("\n" + "="*80)
    print("ANALYSIS 2: D-Variable Correlation Matrix")
    print("="*80)
    
    valid_ops = [op for op in operators if 'd_variables' in op]
    
    d_vars = ['d1_arity', 'd2_role', 'd3_invertibility', 'd4_commutativity',
              'd5_meaning_count', 'd6_dependency_depth', 'd7_closure', 'd8_overloading']
    
    # Compute correlation matrix
    n = len(d_vars)
    corr_matrix = [[0.0 for _ in range(n)] for _ in range(n)]
    
    for i, var1 in enumerate(d_vars):
        for j, var2 in enumerate(d_vars):
            if i == j:
                corr_matrix[i][j] = 1.0
            else:
                # Compute Pearson correlation
                vals1 = [op['d_variables'][var1] for op in valid_ops]
                vals2 = [op['d_variables'][var2] for op in valid_ops]
                
                mean1 = sum(vals1) / len(vals1)
                mean2 = sum(vals2) / len(vals2)
                
                numerator = sum((vals1[k] - mean1) * (vals2[k] - mean2) for k in range(len(vals1)))
                denom1 = math.sqrt(sum((v - mean1)**2 for v in vals1))
                denom2 = math.sqrt(sum((v - mean2)**2 for v in vals2))
                
                if denom1 > 0 and denom2 > 0:
                    corr_matrix[i][j] = numerator / (denom1 * denom2)
                else:
                    corr_matrix[i][j] = 0.0
    
    # Print correlation matrix
    print(f"\nCorrelation Matrix ({len(valid_ops)} operators):")
    print("\n" + " "*20, end="")
    for var in d_vars:
        print(f"{var[:4]:>8}", end="")
    print()
    print("-" * (20 + 8 * len(d_vars)))
    
    for i, var1 in enumerate(d_vars):
        print(f"{var1:<20}", end="")
        for j in range(len(d_vars)):
            corr = corr_matrix[i][j]
            if abs(corr) > 0.5:
                print(f"\033[1m{corr:>8.3f}\033[0m", end="")  # Bold for strong correlations
            else:
                print(f"{corr:>8.3f}", end="")
        print()
    
    # Find strongest correlations (excluding diagonal)
    strong_corrs = []
    for i in range(n):
        for j in range(i+1, n):
            corr = abs(corr_matrix[i][j])
            if corr > 0.3:  # Threshold for "interesting"
                strong_corrs.append((d_vars[i], d_vars[j], corr_matrix[i][j]))
    
    strong_corrs.sort(key=lambda x: abs(x[2]), reverse=True)
    
    print("\n" + "-"*80)
    print("Strongest Correlations (|r| > 0.3):")
    print(f"{'Variable 1':<25} {'Variable 2':<25} {'Correlation':<15} {'Interpretation'}")
    print("-"*80)
    
    for var1, var2, corr in strong_corrs[:15]:
        interp = ""
        if 'arity' in var1 and 'dependency' in var2:
            interp = "More args → more complex"
        elif 'invertibility' in var1 and 'dependency' in var2:
            interp = "Invertible ops are simpler"
        elif 'commutativity' in var1 and 'dependency' in var2:
            interp = "Commutative ops are simpler"
        elif 'meaning' in var1 and 'dependency' in var2:
            interp = "Ambiguity correlates with complexity"
        
        print(f"{var1:<25} {var2:<25} {corr:<15.3f} {interp}")
    
    return corr_matrix


def analyze_operator_evolution_pathways(operators):
    """Identify evolutionary pathways from primitives to derived operators."""
    print("\n" + "="*80)
    print("ANALYSIS 3: Operator Evolution Pathways")
    print("="*80)
    
    # Separate primitives and derived
    primitives = [op for op in operators if op.get('is_primitive', False)]
    derived = [op for op in operators if not op.get('is_primitive', False)]
    
    print(f"\nPrimitives: {len(primitives)}")
    print(f"Derived: {len(derived)}")
    
    # Cluster derived operators by D6 (complexity)
    d6_bins = defaultdict(list)
    
    for op in derived:
        if 'd_variables' in op:
            d6 = op['d_variables']['d6_dependency_depth']
            bin_idx = int(d6 * 10)  # 10 bins
            d6_bins[bin_idx].append(op)
    
    # Analyze evolution from primitives
    print("\n" + "-"*80)
    print("Evolution Stages (by D6 complexity):")
    print(f"{'Stage':<8} {'D6 Range':<15} {'Count':<8} {'% Total':<10} {'Avg NRCI':<15} {'Representative Ops'}")
    print("-"*80)
    
    stages = []
    
    for bin_idx in sorted(d6_bins.keys()):
        ops_in_bin = d6_bins[bin_idx]
        d6_min = bin_idx / 10.0
        d6_max = (bin_idx + 1) / 10.0
        count = len(ops_in_bin)
        pct = 100 * count / len(derived)
        avg_nrci = sum(op.get('predicted_nrci', 0) for op in ops_in_bin) / count
        
        # Get representatives
        reps = [op['symbol'] for op in ops_in_bin[:3]]
        rep_str = ', '.join(reps)
        
        stage_name = ""
        if d6_min < 0.15:
            stage_name = "Stage 1"
        elif d6_min < 0.25:
            stage_name = "Stage 2"
        elif d6_min < 0.35:
            stage_name = "Stage 3"
        elif d6_min < 0.45:
            stage_name = "Stage 4"
        else:
            stage_name = "Stage 5+"
        
        stages.append({
            'stage': stage_name,
            'd6_range': f"{d6_min:.1f}-{d6_max:.1f}",
            'count': count,
            'pct': pct,
            'avg_nrci': avg_nrci,
            'operators': ops_in_bin
        })
        
        print(f"{stage_name:<8} {d6_min:.1f}-{d6_max:.1f}      {count:<8} {pct:<10.1f} {avg_nrci:<15.10f} {rep_str}")
    
    # Analyze transitions between stages
    print("\n" + "-"*80)
    print("Evolutionary Interpretation:")
    print("-"*80)
    print("Stage 1 (D6 < 0.15): Near-primitives (basic arithmetic, simple logic)")
    print("Stage 2 (D6 0.15-0.25): First-order derived (set theory, basic algebra)")
    print("Stage 3 (D6 0.25-0.35): Second-order derived (transcendental functions)")
    print("Stage 4 (D6 0.35-0.45): Third-order derived (special functions, advanced calculus)")
    print("Stage 5+ (D6 > 0.45): Higher-order derived (exotic special functions, field theory)")
    
    return stages


def analyze_category_relationships(operators, taxonomy):
    """Analyze relationships between operator categories."""
    print("\n" + "="*80)
    print("ANALYSIS 4: Category Relationships & Clustering")
    print("="*80)
    
    # Build category co-occurrence matrix
    categories = list(set(op.get('category', 'Unknown') for op in operators))
    categories.sort()
    
    print(f"\nTotal categories: {len(categories)}")
    
    # Group by domain (first part of category before '/')
    domains = defaultdict(list)
    for cat in categories:
        domain = cat.split('/')[0]
        domains[domain].append(cat)
    
    print(f"Total domains: {len(domains)}")
    
    # Analyze domain sizes
    print("\n" + "-"*80)
    print("Domain Sizes:")
    print(f"{'Domain':<40} {'Subcategories':<15} {'Total Operators'}")
    print("-"*80)
    
    domain_stats = []
    
    for domain, cats in sorted(domains.items(), key=lambda x: len(x[1]), reverse=True)[:30]:
        total_ops = sum(1 for op in operators if op.get('category', '').startswith(domain))
        domain_stats.append({
            'domain': domain,
            'subcategories': len(cats),
            'total_operators': total_ops
        })
        print(f"{domain:<40} {len(cats):<15} {total_ops}")
    
    # Analyze primitive density by domain
    print("\n" + "-"*80)
    print("Primitive Density by Domain (Top 20):")
    print(f"{'Domain':<40} {'Primitives':<12} {'Total':<10} {'Density %'}")
    print("-"*80)
    
    for domain in sorted(domains.keys()):
        ops_in_domain = [op for op in operators if op.get('category', '').startswith(domain)]
        if len(ops_in_domain) == 0:
            continue
        
        primitives = sum(1 for op in ops_in_domain if op.get('is_primitive', False))
        density = 100 * primitives / len(ops_in_domain)
        
        if len(ops_in_domain) >= 5:  # Only show domains with at least 5 operators
            domain_stats_item = next((d for d in domain_stats if d['domain'] == domain), None)
            if domain_stats_item:
                domain_stats_item['primitives'] = primitives
                domain_stats_item['density'] = density
    
    # Sort by density
    domain_stats_with_density = [d for d in domain_stats if 'density' in d]
    domain_stats_with_density.sort(key=lambda x: x['density'], reverse=True)
    
    for ds in domain_stats_with_density[:20]:
        print(f"{ds['domain']:<40} {ds['primitives']:<12} {ds['total_operators']:<10} {ds['density']:<.1f}")
    
    return domain_stats


def analyze_predictive_rules(operators):
    """Extract predictive rules for operator design."""
    print("\n" + "="*80)
    print("ANALYSIS 5: Predictive Rules for Operator Design")
    print("="*80)
    
    valid_ops = [op for op in operators if 'd_variables' in op and 'predicted_nrci' in op]
    
    # Rule 1: If D6 < threshold, then primitive
    d6_threshold_primitive = 0.15
    correct_primitive = sum(1 for op in valid_ops 
                           if (op['d_variables']['d6_dependency_depth'] < d6_threshold_primitive) == op.get('is_primitive', False))
    accuracy_primitive = 100 * correct_primitive / len(valid_ops)
    
    print(f"\nRule 1: D6 < {d6_threshold_primitive} → Primitive")
    print(f"  Accuracy: {accuracy_primitive:.1f}%")
    
    # Rule 2: If D6 > threshold, then NRCI < value
    d6_high = 0.4
    nrci_low = 0.999920
    correct_nrci = sum(1 for op in valid_ops 
                      if not (op['d_variables']['d6_dependency_depth'] > d6_high and op['predicted_nrci'] > nrci_low))
    accuracy_nrci = 100 * correct_nrci / len(valid_ops)
    
    print(f"\nRule 2: D6 > {d6_high} → NRCI < {nrci_low}")
    print(f"  Accuracy: {accuracy_nrci:.1f}%")
    
    # Rule 3: Commutativity → Lower D6
    commutative_ops = [op for op in valid_ops if op['d_variables']['d4_commutativity'] > 0.5]
    non_commutative_ops = [op for op in valid_ops if op['d_variables']['d4_commutativity'] <= 0.5]
    
    if commutative_ops and non_commutative_ops:
        avg_d6_comm = sum(op['d_variables']['d6_dependency_depth'] for op in commutative_ops) / len(commutative_ops)
        avg_d6_non_comm = sum(op['d_variables']['d6_dependency_depth'] for op in non_commutative_ops) / len(non_commutative_ops)
        
        print(f"\nRule 3: Commutative operators have lower D6")
        print(f"  Avg D6 (commutative): {avg_d6_comm:.4f}")
        print(f"  Avg D6 (non-commutative): {avg_d6_non_comm:.4f}")
        print(f"  Difference: {avg_d6_non_comm - avg_d6_comm:.4f}")
    
    # Rule 4: Arity → Complexity
    arity_bins = defaultdict(list)
    for op in valid_ops:
        arity = op['d_variables']['d1_arity']
        arity_bin = int(arity * 4)  # 0, 0.25, 0.5, 0.75
        arity_bins[arity_bin].append(op)
    
    print(f"\nRule 4: Higher arity → Higher complexity")
    print(f"{'Arity Range':<15} {'Count':<10} {'Avg D6':<15} {'Avg NRCI'}")
    print("-"*60)
    
    for arity_bin in sorted(arity_bins.keys()):
        ops_in_bin = arity_bins[arity_bin]
        arity_min = arity_bin / 4.0
        arity_max = (arity_bin + 1) / 4.0
        avg_d6 = sum(op['d_variables']['d6_dependency_depth'] for op in ops_in_bin) / len(ops_in_bin)
        avg_nrci = sum(op['predicted_nrci'] for op in ops_in_bin) / len(ops_in_bin)
        
        print(f"{arity_min:.2f}-{arity_max:.2f}      {len(ops_in_bin):<10} {avg_d6:<15.4f} {avg_nrci:.10f}")
    
    # Rule 5: Design formula
    print(f"\n" + "-"*80)
    print("Operator Design Formula:")
    print("-"*80)
    print("To design a high-coherence operator:")
    print("  1. Minimize D6 (dependency depth) - most important")
    print("  2. Minimize D5 (meaning count) - avoid ambiguity")
    print("  3. Minimize D8 (overloading) - single clear purpose")
    print("  4. Prefer commutativity when possible")
    print("  5. Keep arity low (unary or binary)")
    print("  6. Ensure invertibility if possible")
    print("\nPredicted NRCI = 0.999997 - (2.0e-4 × D6 + 5.0e-5 × D5 + 3.0e-5 × D8)")


def find_anomalies_and_outliers(operators):
    """Find unusual operators that don't fit expected patterns."""
    print("\n" + "="*80)
    print("ANALYSIS 6: Anomalies & Outliers")
    print("="*80)
    
    valid_ops = [op for op in operators if 'd_variables' in op and 'predicted_nrci' in op]
    
    # Anomaly 1: High D6 but high NRCI (unexpectedly coherent complex operators)
    high_d6_high_nrci = [op for op in valid_ops 
                         if op['d_variables']['d6_dependency_depth'] > 0.4 and op['predicted_nrci'] > 0.999950]
    
    print(f"\nAnomaly 1: High Complexity but High Coherence (D6 > 0.4, NRCI > 0.999950)")
    print(f"Found {len(high_d6_high_nrci)} operators:")
    
    if high_d6_high_nrci:
        print(f"{'Symbol':<15} {'Name':<30} {'D6':<10} {'NRCI':<15} {'Category'}")
        print("-"*100)
        for op in high_d6_high_nrci[:10]:
            print(f"{op['symbol']:<15} {op['name']:<30} {op['d_variables']['d6_dependency_depth']:<10.4f} {op['predicted_nrci']:<15.10f} {op['category']}")
    
    # Anomaly 2: Low D6 but low NRCI (unexpectedly incoherent simple operators)
    low_d6_low_nrci = [op for op in valid_ops 
                       if op['d_variables']['d6_dependency_depth'] < 0.2 and op['predicted_nrci'] < 0.999960]
    
    print(f"\nAnomaly 2: Low Complexity but Low Coherence (D6 < 0.2, NRCI < 0.999960)")
    print(f"Found {len(low_d6_low_nrci)} operators:")
    
    if low_d6_low_nrci:
        print(f"{'Symbol':<15} {'Name':<30} {'D6':<10} {'NRCI':<15} {'Category'}")
        print("-"*100)
        for op in low_d6_low_nrci[:10]:
            print(f"{op['symbol']:<15} {op['name']:<30} {op['d_variables']['d6_dependency_depth']:<10.4f} {op['predicted_nrci']:<15.10f} {op['category']}")
    
    # Anomaly 3: Primitives with high D6 (should not exist)
    primitive_high_d6 = [op for op in valid_ops 
                         if op.get('is_primitive', False) and op['d_variables']['d6_dependency_depth'] > 0.15]
    
    print(f"\nAnomaly 3: Primitives with High D6 (should not exist)")
    print(f"Found {len(primitive_high_d6)} operators:")
    
    if primitive_high_d6:
        print(f"{'Symbol':<15} {'Name':<30} {'D6':<10} {'NRCI':<15} {'Category'}")
        print("-"*100)
        for op in primitive_high_d6[:10]:
            print(f"{op['symbol']:<15} {op['name']:<30} {op['d_variables']['d6_dependency_depth']:<10.4f} {op['predicted_nrci']:<15.10f} {op['category']}")
    
    # Anomaly 4: Extreme outliers in NRCI
    nrcis = [op['predicted_nrci'] for op in valid_ops]
    mean_nrci = sum(nrcis) / len(nrcis)
    std_nrci = math.sqrt(sum((n - mean_nrci)**2 for n in nrcis) / len(nrcis))
    
    outliers = [op for op in valid_ops 
                if abs(op['predicted_nrci'] - mean_nrci) > 3 * std_nrci]
    
    print(f"\nAnomaly 4: Extreme NRCI Outliers (> 3σ from mean)")
    print(f"Mean NRCI: {mean_nrci:.10f}, StdDev: {std_nrci:.10f}")
    print(f"Found {len(outliers)} operators:")
    
    if outliers:
        print(f"{'Symbol':<15} {'Name':<30} {'NRCI':<15} {'Deviation (σ)':<15} {'Category'}")
        print("-"*100)
        for op in outliers[:10]:
            deviation = (op['predicted_nrci'] - mean_nrci) / std_nrci
            print(f"{op['symbol']:<15} {op['name']:<30} {op['predicted_nrci']:<15.10f} {deviation:<15.2f} {op['category']}")


def main():
    print("="*80)
    print("DEEP DATA ANALYSIS: Computational Grammar Dataset")
    print("="*80)
    print("\nExtracting every possible insight from 611 operators...")
    
    # Load data
    operators, families, nobles, taxonomy = load_data()
    
    print(f"\nDataset loaded:")
    print(f"  Operators: {len(operators)}")
    print(f"  Families: {len(families)}")
    print(f"  Noble operators: {len(nobles)}")
    print(f"  Taxonomic domains: {len(taxonomy)}")
    
    # Run analyses
    bit_stats = analyze_offbit_bit_patterns(operators)
    corr_matrix = analyze_d_variable_correlations_matrix(operators)
    evolution = analyze_operator_evolution_pathways(operators)
    category_stats = analyze_category_relationships(operators, taxonomy)
    analyze_predictive_rules(operators)
    find_anomalies_and_outliers(operators)
    
    # Save analysis results
    analysis_results = {
        'bit_statistics': bit_stats,
        'correlation_matrix': corr_matrix,
        'evolution_stages': evolution,
        'category_statistics': category_stats
    }
    
    with open('/home/ubuntu/deep_analysis_results.json', 'w') as f:
        json.dump(analysis_results, f, indent=2, default=str)
    
    print("\n" + "="*80)
    print("DEEP ANALYSIS COMPLETE")
    print("="*80)
    print("\nResults saved to: deep_analysis_results.json")
    print("\nKey insights extracted - ready for interpretation and periodic table design!")


if __name__ == "__main__":
    main()
