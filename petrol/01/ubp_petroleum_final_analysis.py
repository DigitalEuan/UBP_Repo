"""
UBP 3.3 Comprehensive Petroleum Analysis
Using optimal balanced OffBit encoding strategy
Full 1000-molecule analysis with all UBP modules
Author: Euan R A Craig
Date: November 2025
"""

import sys
sys.path.insert(0, '/home/ubuntu/UBP_Repo/ubp_3.3')

import pandas as pd
import numpy as np
import json
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns

from y_constants import calculate_y_emergent, YConstants
from observer_framework import SelfActualizingObserver
from soc_energy import SOCCalculator
from wall_of_reality import WallOfReality
from enhanced_nrci import EnhancedNRCI
from level_7_global_golay import GlobalGolayCorrection

def balanced_offbit_encoding(mol_weight, carbon_count, freq_hz, complexity):
    """Optimal balanced OffBit encoding for petroleum molecules"""
    state = np.zeros(24, dtype=int)
    
    # Reality (0-5): Combined MW and Carbon (3 bits each)
    mw_encoded = int((mol_weight / 600.0) * 7) % 8
    c_encoded = min(carbon_count // 8, 7)
    combined_reality = (mw_encoded << 3) | c_encoded
    for i in range(6):
        state[i] = (combined_reality >> i) & 1
    
    # Information (6-11): Combined Frequency and Complexity
    freq_encoded = int((np.log10(freq_hz) - 11) * 1.5) % 8
    comp_encoded = min(complexity // 4, 7)
    combined_info = (freq_encoded << 3) | comp_encoded
    for i in range(6):
        state[6 + i] = (combined_info >> i) & 1
    
    # Activation (12-17): Full frequency encoding
    freq_full = int((np.log10(freq_hz) - 11) * 10) % 64
    for i in range(6):
        state[12 + i] = (freq_full >> i) & 1
    
    # Unactivated (18-23): Full carbon encoding
    c_full = min(carbon_count, 63)
    for i in range(6):
        state[18 + i] = (c_full >> i) & 1
    
    return state

class ComprehensivePetroleumAnalyzer:
    """Full UBP analysis with balanced encoding"""
    
    def __init__(self):
        print("Initializing Comprehensive UBP Petroleum Analyzer...")
        print("Using BALANCED OffBit encoding strategy")
        
        # Initialize UBP components
        self.y_constants = YConstants()
        self.observer = SelfActualizingObserver()
        self.soc_calc = SOCCalculator()
        self.wall = WallOfReality(enforce_limit=False)
        self.nrci_calc = EnhancedNRCI()
        self.glr = GlobalGolayCorrection()
        
        # Converge observer
        print("\nConverging self-actualizing observer...")
        obs_result = self.observer.simulate_observer_convergence()
        self.o_observer = obs_result.final_o_observer
        
        # Get constants
        self.Y = self.y_constants.Y_BASE
        self.Y_m = self.y_constants.Y_M
        self.Y_emergent = calculate_y_emergent(0.999997, self.o_observer)
        
        print(f"  O_observer: {self.o_observer:.10f}")
        print(f"  Y_BASE: {self.Y:.15f}")
        print(f"  Y_M: {self.Y_m:.15e}")
        print(f"  Y_emergent: {self.Y_emergent:.15f}")
        
        self.results = []
    
    def analyze_molecule(self, molecule_data):
        """Full UBP analysis on single molecule"""
        
        mol_id = molecule_data['id']
        name = molecule_data['name']
        mol_weight = molecule_data['molecular_weight']
        carbon_count = molecule_data['carbon_count']
        mol_type = molecule_data['type']
        freq_hz = molecule_data['estimated_frequency_hz']
        complexity = molecule_data.get('complexity', len(str(molecule_data.get('smiles', ''))))
        fraction = molecule_data.get('petroleum_fraction', 'Unknown')
        category = molecule_data.get('category', 'Unknown')
        
        result = {
            'id': mol_id,
            'name': name,
            'type': mol_type,
            'category': category,
            'fraction': fraction,
            'carbon_count': carbon_count,
            'molecular_weight': mol_weight,
            'frequency_hz': freq_hz,
            'complexity': complexity
        }
        
        try:
            # 1. Balanced OffBit encoding
            bit_state = balanced_offbit_encoding(mol_weight, carbon_count, freq_hz, complexity)
            result['bit_state_decimal'] = int(''.join(map(str, bit_state[::-1])), 2)
            
            # 2. GLR Correction
            glr_result = self.glr.process_correction(bit_state)
            result['glr_errors'] = glr_result.error_count
            result['glr_nrci_before'] = glr_result.nrci_before
            result['glr_nrci_after'] = glr_result.nrci_after
            result['glr_efficiency'] = glr_result.correction_efficiency
            result['glr_improvement'] = glr_result.nrci_after - glr_result.nrci_before
            
            # 3. NRCI Calculation
            pattern_sim = self.generate_pattern(mol_weight, carbon_count, complexity)
            pattern_theo = np.random.normal(0, 1.0, len(pattern_sim))
            nrci_result = self.nrci_calc.compute_basic_nrci(pattern_sim, pattern_theo)
            result['nrci'] = nrci_result.value
            result['nrci_regime'] = str(nrci_result.regime)
            
            # 4. SOC Energy
            modal_sum = carbon_count * 0.1 + mol_weight * 0.001
            soc_result = self.soc_calc.calculate_soc_energy(modal_sum=modal_sum, M=mol_weight, C=1.0)
            result['soc_energy_cu'] = soc_result.energy_cu
            result['modal_sum'] = modal_sum
            
            # 5. Wall of Reality
            wall_status = self.wall.detect_wall_approach(freq_hz)
            result['wall_proximity'] = wall_status.proximity
            result['wall_safe'] = self.wall.check_frequency_limit(freq_hz)
            result['nrci_risk'] = wall_status.nrci_risk
            
            # 6. Coherence metrics
            result['coherence_factor'] = result['nrci'] * (1.0 + np.log10(max(result['soc_energy_cu'], 1.0)) / 10.0)
            result['resonance_strength'] = self.calc_resonance(freq_hz, mol_weight, carbon_count)
            result['emergence_intensity'] = np.log10(max(result['soc_energy_cu'], 1.0)) / 10.0
            
            result['success'] = True
            result['error'] = None
            
        except Exception as e:
            result['success'] = False
            result['error'] = str(e)
            for key in ['glr_errors', 'nrci', 'soc_energy_cu', 'coherence_factor']:
                if key not in result:
                    result[key] = None
        
        return result
    
    def generate_pattern(self, mol_weight, carbon_count, complexity):
        """Generate molecular pattern for NRCI"""
        np.random.seed(int(mol_weight * carbon_count) % 10000)
        pattern = np.random.normal(0, 0.05, 1000)
        pattern += np.sin(np.linspace(0, carbon_count * np.pi, 1000)) * 0.01
        return pattern
    
    def calc_resonance(self, freq_hz, mol_weight, carbon_count):
        """Calculate resonance strength"""
        optimal_weight = 100.0
        weight_factor = np.exp(-((mol_weight - optimal_weight) / 200.0) ** 2)
        return weight_factor * (carbon_count / 10.0) * (freq_hz / 1e12)
    
    def analyze_dataset(self, molecules_df):
        """Analyze full dataset"""
        
        print(f"\nAnalyzing {len(molecules_df)} petroleum molecules...")
        print("=" * 80)
        
        for idx, row in molecules_df.iterrows():
            if (idx + 1) % 100 == 0:
                print(f"Progress: {idx + 1}/{len(molecules_df)} molecules")
            
            result = self.analyze_molecule(row.to_dict())
            self.results.append(result)
        
        print(f"\n✓ Analysis complete: {len(self.results)} molecules")
        
        return pd.DataFrame(self.results)
    
    def generate_insights(self, results_df):
        """Generate novel insights from results"""
        
        success_df = results_df[results_df['success'] == True].copy()
        
        insights = {
            'timestamp': datetime.now().isoformat(),
            'total_molecules': len(results_df),
            'successful': int(success_df['success'].sum()),
            
            'ubp_constants': {
                'Y_BASE': float(self.Y),
                'Y_M': float(self.Y_m),
                'Y_emergent': float(self.Y_emergent),
                'O_observer': float(self.o_observer)
            },
            
            'global_statistics': {
                'mean_nrci': float(success_df['nrci'].mean()),
                'std_nrci': float(success_df['nrci'].std()),
                'mean_soc_energy': float(success_df['soc_energy_cu'].mean()),
                'mean_glr_efficiency': float(success_df['glr_efficiency'].mean()),
                'mean_glr_improvement': float(success_df['glr_improvement'].mean()),
                'mean_coherence': float(success_df['coherence_factor'].mean())
            },
            
            'by_petroleum_fraction': {},
            'by_molecule_category': {},
            'by_carbon_class': {},
            
            'novel_findings': []
        }
        
        # Analysis by petroleum fraction
        for fraction in success_df['fraction'].unique():
            frac_df = success_df[success_df['fraction'] == fraction]
            insights['by_petroleum_fraction'][fraction] = {
                'count': len(frac_df),
                'mean_nrci': float(frac_df['nrci'].mean()),
                'mean_coherence': float(frac_df['coherence_factor'].mean()),
                'mean_glr_efficiency': float(frac_df['glr_efficiency'].mean())
            }
        
        # Analysis by category
        for category in success_df['category'].unique():
            cat_df = success_df[success_df['category'] == category]
            insights['by_molecule_category'][category] = {
                'count': len(cat_df),
                'mean_nrci': float(cat_df['nrci'].mean()),
                'mean_resonance': float(cat_df['resonance_strength'].mean())
            }
        
        # Novel findings
        # 1. Optimal coherence molecules
        top_coherence = success_df.nlargest(10, 'coherence_factor')[['name', 'type', 'coherence_factor', 'carbon_count']]
        insights['novel_findings'].append({
            'finding': 'Top 10 highest coherence petroleum molecules',
            'molecules': top_coherence.to_dict('records')
        })
        
        # 2. GLR efficiency leaders
        top_glr = success_df.nlargest(10, 'glr_efficiency')[['name', 'type', 'glr_efficiency', 'glr_improvement']]
        insights['novel_findings'].append({
            'finding': 'Molecules with highest GLR error correction efficiency',
            'molecules': top_glr.to_dict('records')
        })
        
        # 3. Resonance patterns
        gasoline_resonance = success_df[success_df['fraction'] == 'Gasoline']['resonance_strength'].mean()
        diesel_resonance = success_df[success_df['fraction'] == 'Diesel']['resonance_strength'].mean()
        insights['novel_findings'].append({
            'finding': 'Resonance strength comparison',
            'gasoline_mean_resonance': float(gasoline_resonance),
            'diesel_mean_resonance': float(diesel_resonance),
            'ratio': float(gasoline_resonance / diesel_resonance) if diesel_resonance > 0 else None
        })
        
        return insights
    
    def create_comprehensive_visualizations(self, results_df):
        """Create detailed visualizations"""
        
        print("\nGenerating comprehensive visualizations...")
        
        success_df = results_df[results_df['success'] == True].copy()
        
        fig = plt.figure(figsize=(24, 16))
        
        # 1. NRCI by Petroleum Fraction
        plt.subplot(3, 4, 1)
        success_df.boxplot(column='nrci', by='fraction', ax=plt.gca())
        plt.title('NRCI by Petroleum Fraction')
        plt.suptitle('')
        plt.ylabel('NRCI')
        
        # 2. SOC Energy Distribution
        plt.subplot(3, 4, 2)
        plt.hist(np.log10(success_df['soc_energy_cu']), bins=50, edgecolor='black', alpha=0.7)
        plt.xlabel('log10(SOC Energy [CU])')
        plt.ylabel('Frequency')
        plt.title('SOC Energy Distribution')
        
        # 3. GLR Efficiency by Category
        plt.subplot(3, 4, 3)
        category_glr = success_df.groupby('category')['glr_efficiency'].mean().sort_values()
        category_glr.plot(kind='barh')
        plt.xlabel('Mean GLR Efficiency')
        plt.title('GLR Efficiency by Molecule Category')
        
        # 4. Coherence vs Carbon Count
        plt.subplot(3, 4, 4)
        plt.scatter(success_df['carbon_count'], success_df['coherence_factor'], 
                   c=success_df['molecular_weight'], cmap='viridis', alpha=0.6, s=20)
        plt.xlabel('Carbon Count')
        plt.ylabel('Coherence Factor')
        plt.title('Coherence vs Carbon Count')
        plt.colorbar(label='Molecular Weight')
        
        # 5. Resonance Strength Distribution
        plt.subplot(3, 4, 5)
        for fraction in success_df['fraction'].unique():
            frac_data = success_df[success_df['fraction'] == fraction]['resonance_strength']
            plt.hist(frac_data, bins=30, alpha=0.5, label=fraction)
        plt.xlabel('Resonance Strength')
        plt.ylabel('Frequency')
        plt.title('Resonance Strength by Fraction')
        plt.legend()
        
        # 6. GLR Improvement
        plt.subplot(3, 4, 6)
        plt.scatter(success_df['glr_nrci_before'], success_df['glr_nrci_after'], alpha=0.5, s=10)
        plt.plot([0, 1], [0, 1], 'r--', label='No improvement')
        plt.xlabel('NRCI Before GLR')
        plt.ylabel('NRCI After GLR')
        plt.title('GLR Correction Effect')
        plt.legend()
        
        # 7. Wall Proximity
        plt.subplot(3, 4, 7)
        wall_counts = success_df['wall_proximity'].value_counts()
        wall_counts.plot(kind='bar')
        plt.xlabel('Wall Proximity')
        plt.ylabel('Count')
        plt.title('Wall of Reality Proximity')
        plt.xticks(rotation=45)
        
        # 8. Emergence Intensity
        plt.subplot(3, 4, 8)
        plt.scatter(success_df['nrci'], success_df['emergence_intensity'], alpha=0.5, s=10)
        plt.xlabel('NRCI')
        plt.ylabel('Emergence Intensity')
        plt.title('Emergence vs Coherence')
        
        # 9. Coherence by Type (top 10)
        plt.subplot(3, 4, 9)
        type_coherence = success_df.groupby('type')['coherence_factor'].mean().nlargest(10)
        type_coherence.plot(kind='barh')
        plt.xlabel('Mean Coherence Factor')
        plt.title('Top 10 Molecule Types by Coherence')
        
        # 10. Frequency vs MW
        plt.subplot(3, 4, 10)
        plt.scatter(success_df['molecular_weight'], np.log10(success_df['frequency_hz']), 
                   c=success_df['carbon_count'], cmap='plasma', alpha=0.6, s=20)
        plt.xlabel('Molecular Weight (g/mol)')
        plt.ylabel('log10(Frequency [Hz])')
        plt.title('Frequency vs Molecular Weight')
        plt.colorbar(label='Carbon Count')
        
        # 11. GLR Errors by Complexity
        plt.subplot(3, 4, 11)
        plt.scatter(success_df['complexity'], success_df['glr_errors'], alpha=0.5, s=10)
        plt.xlabel('Molecular Complexity')
        plt.ylabel('GLR Errors Corrected')
        plt.title('GLR Errors vs Complexity')
        
        # 12. Heatmap: Category vs Fraction
        plt.subplot(3, 4, 12)
        pivot = success_df.pivot_table(values='coherence_factor', 
                                      index='category', 
                                      columns='fraction', 
                                      aggfunc='mean')
        sns.heatmap(pivot, annot=True, fmt='.2e', cmap='YlOrRd')
        plt.title('Mean Coherence: Category vs Fraction')
        
        plt.tight_layout()
        plt.savefig('ubp_petroleum_comprehensive_analysis.png', dpi=300, bbox_inches='tight')
        print("  ✓ Saved: ubp_petroleum_comprehensive_analysis.png")
        plt.close()

def main():
    print("=" * 80)
    print("UBP 3.3 COMPREHENSIVE PETROLEUM ANALYSIS")
    print("1000 Real Molecules | Balanced OffBit Encoding | Full Implementation")
    print("Author: Euan R A Craig")
    print("=" * 80)
    
    # Load data
    print("\nLoading petroleum molecules...")
    molecules_df = pd.read_csv('petroleum_molecules_1000.csv')
    print(f"Loaded {len(molecules_df)} molecules")
    
    # Initialize
    analyzer = ComprehensivePetroleumAnalyzer()
    
    # Analyze
    results_df = analyzer.analyze_dataset(molecules_df)
    
    # Save
    print("\nSaving results...")
    results_df.to_csv('ubp_petroleum_final_results.csv', index=False)
    results_df.to_json('ubp_petroleum_final_results.json', orient='records', indent=2)
    print("  ✓ Saved results files")
    
    # Generate insights
    print("\nGenerating insights...")
    insights = analyzer.generate_insights(results_df)
    
    with open('ubp_petroleum_insights.json', 'w') as f:
        json.dump(insights, f, indent=2, default=str)
    print("  ✓ Saved: ubp_petroleum_insights.json")
    
    # Visualize
    analyzer.create_comprehensive_visualizations(results_df)
    
    # Print summary
    print("\n" + "=" * 80)
    print("ANALYSIS COMPLETE - KEY RESULTS")
    print("=" * 80)
    print(f"\nTotal molecules: {insights['total_molecules']}")
    print(f"Successful analyses: {insights['successful']}")
    print(f"\nMean NRCI: {insights['global_statistics']['mean_nrci']:.6f}")
    print(f"Mean GLR Efficiency: {insights['global_statistics']['mean_glr_efficiency']:.4f}")
    print(f"Mean Coherence Factor: {insights['global_statistics']['mean_coherence']:.6e}")
    print(f"\nTop coherence molecule: {insights['novel_findings'][0]['molecules'][0]['name']}")
    
    print("\n✓ COMPREHENSIVE PETROLEUM UBP ANALYSIS COMPLETE")

if __name__ == '__main__':
    main()
