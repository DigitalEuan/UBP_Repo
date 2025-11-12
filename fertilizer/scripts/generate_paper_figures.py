'''
Generate plots for the UBP Fertilizer Chemical Coherence Study paper.
'''

import json
import matplotlib.pyplot as plt
import numpy as np


def generate_plots():
    '''Generate and save all plots for the paper.'''
    
    # Load data
    with open('/home/ubuntu/ubp_fertilizer_chemical_study/outputs/ballance_products.json') as f:
        ballance_data = json.load(f)
        
    with open('/home/ubuntu/ubp_fertilizer_chemical_study/outputs/optimized_formulations.json') as f:
        optimized_data = json.load(f)

    # --- Plot 1: Ballance Product NRCI Comparison ---
    fig1, ax1 = plt.subplots(figsize=(10, 6))
    products = list(ballance_data.keys())
    nrcis = [d['system_nrci'] for d in ballance_data.values()]
    
    ax1.bar(products, nrcis, color=['#003f5c', '#58508d', '#bc5090'])
    ax1.set_ylim(0.94, 1.0)
    ax1.set_ylabel('System NRCI')
    ax1.set_title('Figure 1: UBP Chemical Coherence of Current Ballance Products')
    ax1.grid(axis='y', linestyle='--', alpha=0.7)
    for i, v in enumerate(nrcis):
        ax1.text(i, v + 0.001, f'{v:.4f}', ha='center', fontweight='bold')

    plt.tight_layout()
    fig1.savefig('/home/ubuntu/ubp_fertilizer_chemical_study/docs/figure1_ballance_nrci.png')
    print("Generated Figure 1: Ballance Product NRCI Comparison")

    # --- Plot 2: Optimized Formulation NRCI Comparison ---
    fig2, ax2 = plt.subplots(figsize=(12, 7))
    formulations = list(optimized_data.keys())
    opt_nrcis = [d['system_nrci'] for d in optimized_data.values()]
    
    all_names = products + formulations
    all_nrcis = nrcis + opt_nrcis
    colors = ['#003f5c', '#58508d', '#bc5090', '#ff6361', '#ffa600', '#3cba54']

    ax2.bar(all_names, all_nrcis, color=colors)
    ax2.set_ylim(0.94, 1.0)
    ax2.set_ylabel('System NRCI')
    ax2.set_title('Figure 2: UBP Coherence of Optimized Formulations vs. Current Products')
    ax2.grid(axis='y', linestyle='--', alpha=0.7)
    for i, v in enumerate(all_nrcis):
        ax2.text(i, v + 0.001, f'{v:.4f}', ha='center', fontweight='bold')
    plt.xticks(rotation=15, ha="right")
    plt.tight_layout()
    fig2.savefig('/home/ubuntu/ubp_fertilizer_chemical_study/docs/figure2_optimized_vs_ballance.png')
    print("Generated Figure 2: Optimized vs. Ballance NRCI")

    # --- Plot 3: Coherence Parameter Levers ---
    fig3, ax3 = plt.subplots(figsize=(10, 6))
    params = ['Molecular Coherence', 'Chemical Purity', 'Release Synchrony']
    super_params = [0.75, 0.82, 0.70] # Superphosphate
    coherencepro_params = [0.99, 0.995, 0.95] # UBP CoherencePro

    x = np.arange(len(params))
    width = 0.35

    rects1 = ax3.bar(x - width/2, super_params, width, label='Superphosphate', color='#003f5c')
    rects2 = ax3.bar(x + width/2, coherencepro_params, width, label='UBP CoherencePro™', color='#ff6361')

    ax3.set_ylabel('Coherence Parameter Value')
    ax3.set_title('Figure 3: Key Coherence Levers for Optimization')
    ax3.set_xticks(x)
    ax3.set_xticklabels(params)
    ax3.legend()
    ax3.set_ylim(0.6, 1.0)
    ax3.grid(axis='y', linestyle='--', alpha=0.7)

    plt.tight_layout()
    fig3.savefig('/home/ubuntu/ubp_fertilizer_chemical_study/docs/figure3_coherence_levers.png')
    print("Generated Figure 3: Coherence Parameter Levers")

if __name__ == '__main__':
    generate_plots()
