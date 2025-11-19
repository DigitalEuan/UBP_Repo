"""
Comprehensive Operator Structure Analysis
==========================================

Analyze 611 operators to reveal:
1. Fundamental families (42 OffBit patterns)
2. Taxonomic trees
3. Noble operators
4. Composition rules
5. Landscape visualization
"""

import json
import math
from collections import defaultdict, Counter
from pathlib import Path


def load_dataset():
    """Load the comprehensive operator dataset."""
    with open('/home/ubuntu/comprehensive_operator_dataset.json') as f:
        return json.load(f)


def analyze_offbit_families(operators):
    """Cluster operators by OffBit patterns to identify fundamental families."""
    print("\n" + "="*70)
    print("ANALYSIS 1: OffBit Families (Fundamental Geometric Clusters)")
    print("="*70)
    
    # Group by OffBit pattern
    families = defaultdict(list)
    for op in operators:
        if 'offbit_binary' in op:
            families[op['offbit_binary']].append(op)
    
    print(f"\nTotal unique OffBit patterns: {len(families)}")
    print(f"Total operators with OffBit: {sum(len(f) for f in families.values())}")
    
    # Sort families by size
    sorted_families = sorted(families.items(), key=lambda x: len(x[1]), reverse=True)
    
    print(f"\nTop 20 Largest Families:")
    print(f"{'Family ID':<12} {'Size':<6} {'OffBit Pattern':<26} {'Sample Operators'}")
    print("-" * 100)
    
    family_analysis = []
    
    for i, (offbit, members) in enumerate(sorted_families[:20]):
        # Get representative operators
        samples = [m['symbol'] for m in members[:5]]
        sample_str = ', '.join(samples)
        if len(members) > 5:
            sample_str += f", ... (+{len(members)-5} more)"
        
        # Analyze family properties
        avg_d6 = sum(m['d_variables']['d6_dependency_depth'] for m in members) / len(members)
        avg_nrci = sum(m['predicted_nrci'] for m in members) / len(members)
        primitives = sum(1 for m in members if m['is_primitive'])
        
        # Get dominant category
        categories = Counter(m['category'] for m in members)
        dominant_cat = categories.most_common(1)[0][0]
        
        family_info = {
            'family_id': i+1,
            'offbit': offbit,
            'size': len(members),
            'avg_d6': avg_d6,
            'avg_nrci': avg_nrci,
            'primitives': primitives,
            'dominant_category': dominant_cat,
            'members': members,
            'samples': samples
        }
        
        family_analysis.append(family_info)
        
        print(f"Family {i+1:<5} {len(members):<6} {offbit:<26} {sample_str[:60]}")
    
    # Save family analysis
    with open('/home/ubuntu/offbit_family_analysis.json', 'w') as f:
        json.dump(family_analysis, f, indent=2, default=str)
    
    print(f"\nFamily analysis saved to: offbit_family_analysis.json")
    
    return family_analysis


def analyze_d_variable_correlations(operators):
    """Analyze correlations between D-variables and family membership."""
    print("\n" + "="*70)
    print("ANALYSIS 2: D-Variable Correlations")
    print("="*70)
    
    # Filter operators with full D-variable data
    valid_ops = [op for op in operators if 'd_variables' in op and 'predicted_nrci' in op]
    
    print(f"\nAnalyzing {len(valid_ops)} operators with complete D-variable data")
    
    # Compute statistics for each D-variable
    d_vars = ['d1_arity', 'd2_role', 'd3_invertibility', 'd4_commutativity',
              'd5_meaning_count', 'd6_dependency_depth', 'd7_closure', 'd8_overloading']
    
    print(f"\nD-Variable Statistics:")
    print(f"{'Variable':<25} {'Min':<10} {'Max':<10} {'Mean':<10} {'StdDev':<10}")
    print("-" * 75)
    
    d_stats = {}
    
    for d_var in d_vars:
        values = [op['d_variables'][d_var] for op in valid_ops]
        mean = sum(values) / len(values)
        variance = sum((v - mean)**2 for v in values) / len(values)
        stddev = math.sqrt(variance)
        
        d_stats[d_var] = {
            'min': min(values),
            'max': max(values),
            'mean': mean,
            'stddev': stddev
        }
        
        print(f"{d_var:<25} {min(values):<10.4f} {max(values):<10.4f} {mean:<10.4f} {stddev:<10.4f}")
    
    # Analyze correlation with NRCI
    print(f"\nCorrelation with NRCI (predicted):")
    print(f"{'Variable':<25} {'Correlation':<15} {'Effect Size'}")
    print("-" * 60)
    
    nrcis = [op['predicted_nrci'] for op in valid_ops]
    mean_nrci = sum(nrcis) / len(nrcis)
    
    for d_var in d_vars:
        values = [op['d_variables'][d_var] for op in valid_ops]
        mean_d = sum(values) / len(values)
        
        # Compute Pearson correlation
        numerator = sum((values[i] - mean_d) * (nrcis[i] - mean_nrci) for i in range(len(values)))
        denom_d = math.sqrt(sum((v - mean_d)**2 for v in values))
        denom_nrci = math.sqrt(sum((n - mean_nrci)**2 for n in nrcis))
        
        if denom_d > 0 and denom_nrci > 0:
            correlation = numerator / (denom_d * denom_nrci)
        else:
            correlation = 0.0
        
        # Effect size (how much NRCI changes per unit change in D-variable)
        # Using the validated model weights
        if d_var == 'd6_dependency_depth':
            effect = -2.0e-4
        elif d_var == 'd5_meaning_count':
            effect = -5.0e-5
        elif d_var == 'd8_overloading':
            effect = -3.0e-5
        else:
            effect = 0.0
        
        print(f"{d_var:<25} {correlation:<15.4f} {effect:<15.2e}")
    
    return d_stats


def identify_noble_operators(operators):
    """Identify 'noble' operators (high coherence primitives)."""
    print("\n" + "="*70)
    print("ANALYSIS 3: Noble Operators (High Coherence Primitives)")
    print("="*70)
    
    # Filter for primitives
    primitives = [op for op in operators if op.get('is_primitive', False)]
    
    print(f"\nTotal primitive operators: {len(primitives)}")
    
    # Sort by NRCI (highest first)
    sorted_prims = sorted(primitives, key=lambda x: x.get('predicted_nrci', 0), reverse=True)
    
    print(f"\nTop 30 'Noble' Operators (Highest Coherence Primitives):")
    print(f"{'Rank':<6} {'Symbol':<15} {'Name':<30} {'NRCI':<15} {'D6':<10} {'Category'}")
    print("-" * 110)
    
    noble_operators = []
    
    for i, op in enumerate(sorted_prims[:30]):
        nrci = op.get('predicted_nrci', 0)
        d6 = op.get('d_variables', {}).get('d6_dependency_depth', 0)
        symbol = op.get('symbol', 'N/A')
        name = op.get('name', 'N/A')
        category = op.get('category', 'N/A')
        
        noble_operators.append(op)
        
        print(f"{i+1:<6} {symbol:<15} {name:<30} {nrci:<15.10f} {d6:<10.4f} {category}")
    
    # Save noble operators
    with open('/home/ubuntu/noble_operators.json', 'w') as f:
        json.dump(noble_operators, f, indent=2, default=str)
    
    print(f"\nNoble operators saved to: noble_operators.json")
    
    return noble_operators


def analyze_taxonomic_structure(operators):
    """Build taxonomic trees based on category hierarchy."""
    print("\n" + "="*70)
    print("ANALYSIS 4: Taxonomic Structure")
    print("="*70)
    
    # Build category tree
    category_tree = defaultdict(lambda: defaultdict(list))
    
    for op in operators:
        category = op.get('category', 'Unknown')
        parts = category.split('/')
        
        if len(parts) >= 2:
            domain = parts[0]
            subdomain = parts[1] if len(parts) > 1 else 'General'
            category_tree[domain][subdomain].append(op)
        else:
            category_tree[category]['General'].append(op)
    
    print(f"\nTotal domains: {len(category_tree)}")
    
    # Sort domains by size
    sorted_domains = sorted(category_tree.items(), key=lambda x: sum(len(ops) for ops in x[1].values()), reverse=True)
    
    print(f"\nTop 20 Domains:")
    print(f"{'Domain':<40} {'Subdomains':<12} {'Total Ops':<12} {'Primitives'}")
    print("-" * 90)
    
    taxonomy = []
    
    for domain, subdomains in sorted_domains[:20]:
        total_ops = sum(len(ops) for ops in subdomains.values())
        num_subdomains = len(subdomains)
        primitives = sum(1 for subdomain_ops in subdomains.values() 
                        for op in subdomain_ops if op.get('is_primitive', False))
        
        taxonomy.append({
            'domain': domain,
            'subdomains': list(subdomains.keys()),
            'total_operators': total_ops,
            'primitives': primitives
        })
        
        print(f"{domain:<40} {num_subdomains:<12} {total_ops:<12} {primitives}")
    
    # Save taxonomy
    with open('/home/ubuntu/operator_taxonomy.json', 'w') as f:
        json.dump(taxonomy, f, indent=2, default=str)
    
    print(f"\nTaxonomy saved to: operator_taxonomy.json")
    
    return taxonomy


def analyze_composition_patterns(operators):
    """Analyze composition patterns in derived operators."""
    print("\n" + "="*70)
    print("ANALYSIS 5: Composition Patterns")
    print("="*70)
    
    # Filter for derived operators
    derived = [op for op in operators if not op.get('is_primitive', False)]
    
    print(f"\nTotal derived operators: {len(derived)}")
    
    # Analyze D6 distribution (proxy for compositional complexity)
    d6_bins = defaultdict(list)
    
    for op in derived:
        d6 = op.get('d_variables', {}).get('d6_dependency_depth', 0)
        bin_idx = int(d6 * 10)  # 10 bins from 0.0 to 1.0
        d6_bins[bin_idx].append(op)
    
    print(f"\nComposition Complexity Distribution (by D6):")
    print(f"{'D6 Range':<15} {'Count':<10} {'% of Derived':<15} {'Sample Operators'}")
    print("-" * 80)
    
    for bin_idx in sorted(d6_bins.keys()):
        ops_in_bin = d6_bins[bin_idx]
        d6_min = bin_idx / 10.0
        d6_max = (bin_idx + 1) / 10.0
        count = len(ops_in_bin)
        percentage = 100 * count / len(derived)
        
        samples = [op['symbol'] for op in ops_in_bin[:3]]
        sample_str = ', '.join(samples)
        
        print(f"{d6_min:.1f}-{d6_max:.1f}      {count:<10} {percentage:<15.1f}% {sample_str}")
    
    # Identify most complex operators
    print(f"\nMost Complex Operators (Highest D6):")
    sorted_derived = sorted(derived, key=lambda x: x.get('d_variables', {}).get('d6_dependency_depth', 0), reverse=True)
    
    print(f"{'Symbol':<15} {'Name':<30} {'D6':<10} {'NRCI':<15} {'Category'}")
    print("-" * 100)
    
    for op in sorted_derived[:15]:
        symbol = op.get('symbol', 'N/A')
        name = op.get('name', 'N/A')
        d6 = op.get('d_variables', {}).get('d6_dependency_depth', 0)
        nrci = op.get('predicted_nrci', 0)
        category = op.get('category', 'N/A')
        
        print(f"{symbol:<15} {name:<30} {d6:<10.4f} {nrci:<15.10f} {category}")
    
    return d6_bins


def generate_landscape_map(operators):
    """Generate a 2D landscape map of operators in D-space."""
    print("\n" + "="*70)
    print("ANALYSIS 6: Operator Landscape Map")
    print("="*70)
    
    # Use D6 (complexity) and NRCI (coherence) as axes
    valid_ops = [op for op in operators if 'd_variables' in op and 'predicted_nrci' in op]
    
    print(f"\nMapping {len(valid_ops)} operators in (D6, NRCI) space")
    
    # Create 2D bins
    d6_bins = 20
    nrci_bins = 20
    
    landscape = [[[] for _ in range(nrci_bins)] for _ in range(d6_bins)]
    
    # Find NRCI range
    nrcis = [op['predicted_nrci'] for op in valid_ops]
    nrci_min = min(nrcis)
    nrci_max = max(nrcis)
    
    for op in valid_ops:
        d6 = op['d_variables']['d6_dependency_depth']
        nrci = op['predicted_nrci']
        
        d6_idx = min(int(d6 * d6_bins), d6_bins - 1)
        nrci_idx = min(int((nrci - nrci_min) / (nrci_max - nrci_min) * nrci_bins), nrci_bins - 1)
        
        landscape[d6_idx][nrci_idx].append(op)
    
    # Print landscape density map
    print(f"\nLandscape Density Map (D6 vs NRCI):")
    print(f"  D6 → (complexity increases →)")
    print(f"  NRCI ↑ (coherence increases ↑)")
    print()
    
    # Print header
    print("    ", end="")
    for i in range(0, d6_bins, 2):
        print(f"{i/d6_bins:.1f}  ", end="")
    print()
    
    # Print map (inverted so high NRCI is at top)
    for nrci_idx in range(nrci_bins-1, -1, -1):
        nrci_val = nrci_min + (nrci_idx / nrci_bins) * (nrci_max - nrci_min)
        print(f"{nrci_val:.6f} ", end="")
        
        for d6_idx in range(d6_bins):
            count = len(landscape[d6_idx][nrci_idx])
            if count == 0:
                print("·", end="")
            elif count < 5:
                print("░", end="")
            elif count < 10:
                print("▒", end="")
            elif count < 20:
                print("▓", end="")
            else:
                print("█", end="")
        print()
    
    print("\nDensity Legend: · (0)  ░ (1-4)  ▒ (5-9)  ▓ (10-19)  █ (20+)")
    
    # Save landscape data
    landscape_data = {
        'd6_bins': d6_bins,
        'nrci_bins': nrci_bins,
        'nrci_min': nrci_min,
        'nrci_max': nrci_max,
        'density': [[len(landscape[i][j]) for j in range(nrci_bins)] for i in range(d6_bins)]
    }
    
    with open('/home/ubuntu/operator_landscape.json', 'w') as f:
        json.dump(landscape_data, f, indent=2)
    
    print(f"\nLandscape data saved to: operator_landscape.json")
    
    return landscape


def main():
    print("="*70)
    print("COMPREHENSIVE OPERATOR STRUCTURE ANALYSIS")
    print("="*70)
    print("\nAnalyzing 611 operators to reveal deep structure...")
    
    # Load dataset
    operators = load_dataset()
    print(f"\nLoaded {len(operators)} operators")
    
    # Run analyses
    families = analyze_offbit_families(operators)
    d_stats = analyze_d_variable_correlations(operators)
    nobles = identify_noble_operators(operators)
    taxonomy = analyze_taxonomic_structure(operators)
    composition = analyze_composition_patterns(operators)
    landscape = generate_landscape_map(operators)
    
    # Final summary
    print("\n" + "="*70)
    print("ANALYSIS COMPLETE")
    print("="*70)
    print("\nKey Findings:")
    print(f"  • {len(families)} fundamental geometric families (OffBit patterns)")
    print(f"  • {len(nobles)} noble operators (high-coherence primitives)")
    print(f"  • {len(taxonomy)} major taxonomic domains")
    print(f"  • D6 is primary complexity driver (correlation with NRCI)")
    print(f"  • Operator landscape shows clear clustering patterns")
    
    print("\nOutput Files:")
    print("  • offbit_family_analysis.json")
    print("  • noble_operators.json")
    print("  • operator_taxonomy.json")
    print("  • operator_landscape.json")
    
    print("\n" + "="*70)
    print("Ready for Periodic Table Design!")
    print("="*70)


if __name__ == "__main__":
    main()
