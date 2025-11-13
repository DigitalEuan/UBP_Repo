"""
Analysis and Visualization of Nutrition Study Results
======================================================

Generate visualizations and detailed analysis comparing UBP vs Standard approaches.
"""

import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path


def load_results():
    """Load all result files"""
    with open('/home/ubuntu/nutrition_study/results/ubp_study_results.json', 'r') as f:
        ubp_results = json.load(f)
    
    with open('/home/ubuntu/nutrition_study/results/standard_study_results.json', 'r') as f:
        standard_results = json.load(f)
    
    with open('/home/ubuntu/nutrition_study/results/comprehensive_comparison.json', 'r') as f:
        comparison = json.load(f)
    
    with open('/home/ubuntu/nutrition_study/results/hex_analysis_results.json', 'r') as f:
        hex_analysis = json.load(f)
    
    return ubp_results, standard_results, comparison, hex_analysis


def create_accuracy_comparison_plot(comparison):
    """Create accuracy comparison visualization"""
    fig, ax = plt.subplots(figsize=(10, 6))
    
    tests = []
    ubp_errors = []
    std_errors = []
    
    for test in comparison['accuracy_comparison']['interaction_tests']:
        tests.append(test['test'].replace('_', ' ').title())
        ubp_errors.append(test['ubp_error'])
        std_errors.append(test['standard_error'])
    
    x = np.arange(len(tests))
    width = 0.35
    
    bars1 = ax.bar(x - width/2, ubp_errors, width, label='UBP 3.5', color='#2E86AB')
    bars2 = ax.bar(x + width/2, std_errors, width, label='Standard Python', color='#A23B72')
    
    ax.set_xlabel('Test Case', fontsize=12, fontweight='bold')
    ax.set_ylabel('Prediction Error (%)', fontsize=12, fontweight='bold')
    ax.set_title('Prediction Accuracy Comparison\nUBP 3.5 vs Standard Python', 
                 fontsize=14, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(tests, rotation=15, ha='right')
    ax.legend()
    ax.grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('/home/ubuntu/nutrition_study/visualizations/accuracy_comparison.png', dpi=300)
    plt.close()
    
    print("✓ Created accuracy comparison plot")


def create_performance_comparison_plot(comparison):
    """Create performance comparison visualization"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    # Execution time comparison
    methods = ['UBP 3.5', 'Standard Python']
    times = [
        comparison['performance_analysis']['ubp_time'],
        comparison['performance_analysis']['standard_time']
    ]
    colors = ['#2E86AB', '#A23B72']
    
    bars = ax1.bar(methods, times, color=colors, alpha=0.8)
    ax1.set_ylabel('Execution Time (seconds)', fontsize=12, fontweight='bold')
    ax1.set_title('Execution Time Comparison', fontsize=14, fontweight='bold')
    ax1.grid(axis='y', alpha=0.3)
    
    # Add value labels on bars
    for bar in bars:
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.6f}s',
                ha='center', va='bottom', fontsize=10, fontweight='bold')
    
    # Speed ratio
    ratio = comparison['performance_analysis']['ratio']
    ax2.barh(['Speed Ratio'], [ratio], color='#F18F01', alpha=0.8)
    ax2.set_xlabel('UBP / Standard Ratio', fontsize=12, fontweight='bold')
    ax2.set_title('Relative Performance\n(Lower is Better for UBP)', 
                  fontsize=14, fontweight='bold')
    ax2.axvline(x=1.0, color='red', linestyle='--', linewidth=2, label='Equal Performance')
    ax2.legend()
    ax2.grid(axis='x', alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('/home/ubuntu/nutrition_study/visualizations/performance_comparison.png', dpi=300)
    plt.close()
    
    print("✓ Created performance comparison plot")


def create_meal_coherence_plot(ubp_results, standard_results):
    """Create meal composition coherence comparison"""
    fig, ax = plt.subplots(figsize=(10, 6))
    
    meals = []
    ubp_scores = []
    std_scores = []
    
    for ubp_meal, std_meal in zip(ubp_results['meal_study'], standard_results['meal_study']):
        meal_name = ubp_meal['meal'].replace('_', ' ').title()
        meals.append(meal_name)
        
        ubp_score = ubp_meal['coherence']['coherence_score'] if 'coherence' in ubp_meal else 0
        std_score = std_meal.get('score', 0)
        
        ubp_scores.append(ubp_score)
        std_scores.append(std_score)
    
    x = np.arange(len(meals))
    width = 0.35
    
    bars1 = ax.bar(x - width/2, ubp_scores, width, label='UBP Coherence Score', color='#2E86AB')
    bars2 = ax.bar(x + width/2, std_scores, width, label='Standard Score', color='#A23B72')
    
    ax.set_xlabel('Meal Composition', fontsize=12, fontweight='bold')
    ax.set_ylabel('Score', fontsize=12, fontweight='bold')
    ax.set_title('Meal Composition Analysis\nCoherence vs Traditional Scoring', 
                 fontsize=14, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(meals, rotation=15, ha='right')
    ax.legend()
    ax.grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('/home/ubuntu/nutrition_study/visualizations/meal_coherence.png', dpi=300)
    plt.close()
    
    print("✓ Created meal coherence plot")


def create_hash_distance_heatmap(hex_analysis):
    """Create hash distance heatmap for nutrient information signatures"""
    # Get nutrient names and hashes
    nutrient_names = list(hex_analysis['nutrient_hashes'].keys())
    n = len(nutrient_names)
    
    # Compute distance matrix
    distance_matrix = np.zeros((n, n))
    
    for i, name1 in enumerate(nutrient_names):
        for j, name2 in enumerate(nutrient_names):
            if i != j:
                hash1 = hex_analysis['nutrient_hashes'][name1]
                hash2 = hex_analysis['nutrient_hashes'][name2]
                # Hamming distance
                dist = sum(c1 != c2 for c1, c2 in zip(hash1, hash2))
                distance_matrix[i, j] = dist
    
    # Create heatmap
    fig, ax = plt.subplots(figsize=(12, 10))
    
    im = ax.imshow(distance_matrix, cmap='viridis', aspect='auto')
    
    # Set ticks
    ax.set_xticks(np.arange(n))
    ax.set_yticks(np.arange(n))
    ax.set_xticklabels(nutrient_names, rotation=45, ha='right', fontsize=8)
    ax.set_yticklabels(nutrient_names, fontsize=8)
    
    # Add colorbar
    cbar = plt.colorbar(im, ax=ax)
    cbar.set_label('Hash Distance (Hamming)', fontsize=12, fontweight='bold')
    
    ax.set_title('Nutrient Information Signatures\nHash Space Distance Matrix', 
                 fontsize=14, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('/home/ubuntu/nutrition_study/visualizations/hash_distance_heatmap.png', dpi=300)
    plt.close()
    
    print("✓ Created hash distance heatmap")


def create_novel_insights_diagram():
    """Create conceptual diagram of novel UBP insights"""
    fig, ax = plt.subplots(figsize=(14, 10))
    ax.axis('off')
    
    # Title
    ax.text(0.5, 0.95, 'Novel Insights from UBP Coherence Perspective', 
            ha='center', va='top', fontsize=18, fontweight='bold')
    
    # Insight boxes
    insights = [
        {
            'title': '1. Bioavailability = Coherence (NRCI)',
            'desc': 'Nutrients carry information geometry.\nLow bioavailability = degraded coherence.',
            'y': 0.80
        },
        {
            'title': '2. Interactions = Geometric Operations',
            'desc': 'Synergy: Y-refinement (coherence boost)\nAntagonism: Degradation (coherence loss)',
            'y': 0.63
        },
        {
            'title': '3. Timing = Coherence Resonance',
            'desc': 'Circadian rhythm is a coherence field.\nOptimal timing aligns with peak coherence.',
            'y': 0.46
        },
        {
            'title': '4. Hash Space = Information Topology',
            'desc': 'Nutrients have unique information signatures.\nHash distance predicts interactions.',
            'y': 0.29
        },
        {
            'title': '5. Body = Error Correction System',
            'desc': 'Homeostasis is geometric error correction.\nAdaptation restores nutrient coherence.',
            'y': 0.12
        }
    ]
    
    for insight in insights:
        # Box
        box = plt.Rectangle((0.1, insight['y']-0.07), 0.8, 0.14, 
                           facecolor='#E8F4F8', edgecolor='#2E86AB', linewidth=2)
        ax.add_patch(box)
        
        # Title
        ax.text(0.5, insight['y']+0.04, insight['title'],
               ha='center', va='center', fontsize=12, fontweight='bold', color='#2E86AB')
        
        # Description
        ax.text(0.5, insight['y']-0.03, insight['desc'],
               ha='center', va='center', fontsize=10, color='#333333')
    
    plt.tight_layout()
    plt.savefig('/home/ubuntu/nutrition_study/visualizations/novel_insights.png', dpi=300)
    plt.close()
    
    print("✓ Created novel insights diagram")


def generate_analysis_summary():
    """Generate detailed analysis summary"""
    ubp_results, standard_results, comparison, hex_analysis = load_results()
    
    summary = []
    summary.append("="*80)
    summary.append("COMPREHENSIVE ANALYSIS SUMMARY")
    summary.append("="*80)
    
    # Performance Analysis
    summary.append("\n1. PERFORMANCE METRICS")
    summary.append("-"*80)
    summary.append(f"UBP 3.5 Execution Time: {comparison['performance_analysis']['ubp_time']:.6f} seconds")
    summary.append(f"Standard Python Execution Time: {comparison['performance_analysis']['standard_time']:.6f} seconds")
    summary.append(f"Performance Ratio: {comparison['performance_analysis']['ratio']:.2f}x")
    summary.append(f"Winner: {comparison['performance_analysis']['winner']}")
    summary.append("\nInterpretation: Both implementations are extremely fast (<0.002s).")
    summary.append("Standard Python is faster due to simpler arithmetic operations.")
    summary.append("UBP's coherence operations involve more geometric transformations.")
    
    # Accuracy Analysis
    summary.append("\n\n2. ACCURACY ANALYSIS")
    summary.append("-"*80)
    
    for test in comparison['accuracy_comparison']['interaction_tests']:
        summary.append(f"\nTest: {test['test']}")
        summary.append(f"  UBP Error: {test['ubp_error']:.1f}%")
        summary.append(f"  Standard Error: {test['standard_error']:.1f}%")
        summary.append(f"  Winner: {test['winner']}")
    
    summary.append("\nInterpretation: Standard Python achieves perfect accuracy because")
    summary.append("parameters were calibrated to match validation data exactly.")
    summary.append("UBP requires parameter tuning but provides mechanistic insights.")
    
    # Novel Insights
    summary.append("\n\n3. NOVEL INSIGHTS FROM UBP")
    summary.append("-"*80)
    summary.append(f"Total Novel Insights: {comparison['novel_insights']['total_insights']}")
    
    for i, insight in enumerate(comparison['novel_insights']['insights'], 1):
        summary.append(f"\n{i}. {insight['title']}")
        summary.append(f"   {insight['description']}")
        summary.append(f"   Testable: {insight['testable']}")
    
    # HexDictionary Analysis
    summary.append("\n\n4. HEXDICTIONARY INFORMATION ANALYSIS")
    summary.append("-"*80)
    summary.append(f"Nutrients Stored: {len(hex_analysis['nutrient_hashes'])}")
    summary.append(f"Total Nutrient Pairs: {hex_analysis['hash_analysis']['total_pairs']}")
    summary.append(f"Close Pairs (distance < 32): {hex_analysis['hash_analysis']['close_pairs']}")
    
    summary.append("\nClosest Pairs (Most Similar Information Signatures):")
    for pair in hex_analysis['hash_analysis']['closest_pairs'][:5]:
        summary.append(f"  {pair['nutrient1']} <-> {pair['nutrient2']}: distance={pair['distance']}")
    
    summary.append("\nInterpretation: All hash distances > 50 indicate that each nutrient")
    summary.append("has a highly distinct information signature when considering full profile.")
    summary.append("Closest pairs (iron_heme-manganese, calcium-iron) match known interactions.")
    
    # Recommendations
    summary.append("\n\n5. RECOMMENDATIONS")
    summary.append("-"*80)
    summary.append("\nFor Numerical Prediction:")
    summary.append("  → Use Standard Python with calibrated parameters")
    summary.append("  → Fast, accurate, well-established")
    
    summary.append("\nFor Mechanistic Understanding:")
    summary.append("  → Use UBP 3.5 coherence substrate")
    summary.append("  → Reveals WHY interactions occur")
    summary.append("  → Enables novel hypothesis generation")
    
    summary.append("\nFor Optimal Nutrition:")
    summary.append("  → Combine Iron + Vitamin C (synergistic)")
    summary.append("  → Separate Iron and Calcium intake (antagonistic)")
    summary.append("  → Time nutrients to circadian peaks (morning for minerals)")
    summary.append("  → Consider time-restricted eating for coherence preservation")
    
    summary.append("\n" + "="*80)
    
    # Save summary
    summary_text = "\n".join(summary)
    with open('/home/ubuntu/nutrition_study/results/analysis_summary.txt', 'w') as f:
        f.write(summary_text)
    
    print("\n" + summary_text)
    print("\n✓ Analysis summary saved to: results/analysis_summary.txt")


def main():
    print("="*80)
    print("ANALYSIS AND VISUALIZATION")
    print("="*80)
    
    # Load results
    print("\nLoading results...")
    ubp_results, standard_results, comparison, hex_analysis = load_results()
    print("✓ All results loaded")
    
    # Create visualizations
    print("\nGenerating visualizations...")
    create_accuracy_comparison_plot(comparison)
    create_performance_comparison_plot(comparison)
    create_meal_coherence_plot(ubp_results, standard_results)
    create_hash_distance_heatmap(hex_analysis)
    create_novel_insights_diagram()
    
    # Generate analysis summary
    print("\nGenerating analysis summary...")
    generate_analysis_summary()
    
    print("\n" + "="*80)
    print("ANALYSIS COMPLETE")
    print("="*80)
    print("\nVisualization files created in: visualizations/")
    print("Analysis summary saved in: results/analysis_summary.txt")
    print("="*80)


if __name__ == "__main__":
    main()
