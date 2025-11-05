"""
UBP 3.3 Petroleum Analysis with Multiple OffBit Encoding Strategies
Compares different 24-bit layer assignments to find optimal molecular representation
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

from y_constants import calculate_y_emergent, YConstants
from observer_framework import SelfActualizingObserver
from soc_energy import SOCCalculator
from wall_of_reality import WallOfReality
from enhanced_nrci import EnhancedNRCI
from level_7_global_golay import GlobalGolayCorrection

class OffBitEncodingStrategy:
    """Different strategies for encoding molecular properties into 24-bit OffBit"""
    
    @staticmethod
    def standard_encoding(mol_weight, carbon_count, freq_hz, complexity):
        """
        Standard: MW→Reality, Carbon→Information, Frequency→Activation
        Reality layer represents physical mass
        """
        state = np.zeros(24, dtype=int)
        
        # Reality (0-5): Molecular weight
        mw_encoded = int((mol_weight / 600.0) * 63) % 64
        for i in range(6):
            state[i] = (mw_encoded >> i) & 1
        
        # Information (6-11): Carbon count
        c_encoded = min(carbon_count, 63)
        for i in range(6):
            state[6 + i] = (c_encoded >> i) & 1
        
        # Activation (12-17): Frequency
        freq_encoded = int((np.log10(freq_hz) - 11) * 10) % 64
        for i in range(6):
            state[12 + i] = (freq_encoded >> i) & 1
        
        # Unactivated (18-23): Complexity
        comp_encoded = min(complexity, 63)
        for i in range(6):
            state[18 + i] = (comp_encoded >> i) & 1
        
        return state
    
    @staticmethod
    def inverted_encoding(mol_weight, carbon_count, freq_hz, complexity):
        """
        Inverted: Frequency→Reality, Carbon→Information, MW→Activation
        Reality layer represents vibrational frequency (more fundamental)
        """
        state = np.zeros(24, dtype=int)
        
        # Reality (0-5): Frequency
        freq_encoded = int((np.log10(freq_hz) - 11) * 10) % 64
        for i in range(6):
            state[i] = (freq_encoded >> i) & 1
        
        # Information (6-11): Carbon count
        c_encoded = min(carbon_count, 63)
        for i in range(6):
            state[6 + i] = (c_encoded >> i) & 1
        
        # Activation (12-17): Molecular weight
        mw_encoded = int((mol_weight / 600.0) * 63) % 64
        for i in range(6):
            state[12 + i] = (mw_encoded >> i) & 1
        
        # Unactivated (18-23): Complexity
        comp_encoded = min(complexity, 63)
        for i in range(6):
            state[18 + i] = (comp_encoded >> i) & 1
        
        return state
    
    @staticmethod
    def complexity_focused_encoding(mol_weight, carbon_count, freq_hz, complexity):
        """
        Complexity-focused: Carbon→Reality, Complexity→Information, Frequency→Activation
        Emphasizes structural complexity as fundamental
        """
        state = np.zeros(24, dtype=int)
        
        # Reality (0-5): Carbon count (structural reality)
        c_encoded = min(carbon_count, 63)
        for i in range(6):
            state[i] = (c_encoded >> i) & 1
        
        # Information (6-11): Complexity
        comp_encoded = min(complexity, 63)
        for i in range(6):
            state[6 + i] = (comp_encoded >> i) & 1
        
        # Activation (12-17): Frequency
        freq_encoded = int((np.log10(freq_hz) - 11) * 10) % 64
        for i in range(6):
            state[12 + i] = (freq_encoded >> i) & 1
        
        # Unactivated (18-23): Molecular weight
        mw_encoded = int((mol_weight / 600.0) * 63) % 64
        for i in range(6):
            state[18 + i] = (mw_encoded >> i) & 1
        
        return state
    
    @staticmethod
    def balanced_encoding(mol_weight, carbon_count, freq_hz, complexity):
        """
        Balanced: Hybrid of MW+Carbon→Reality, Freq+Complexity→Information
        Distributes information across layers more evenly
        """
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

class MultiEncodingPetroleumAnalyzer:
    """Analyze petroleum molecules with multiple OffBit encoding strategies"""
    
    def __init__(self):
        print("Initializing Multi-Encoding UBP Analyzer...")
        
        # Initialize UBP components
        self.y_constants = YConstants()
        self.observer = SelfActualizingObserver()
        self.soc_calc = SOCCalculator()
        self.wall = WallOfReality(enforce_limit=False)
        self.nrci_calc = EnhancedNRCI()
        self.glr = GlobalGolayCorrection()
        
        # Converge observer
        print("Converging observer...")
        obs_result = self.observer.simulate_observer_convergence()
        self.o_observer = obs_result.final_o_observer
        
        # Get constants
        self.Y = self.y_constants.Y_BASE
        self.Y_m = self.y_constants.Y_M
        self.Y_emergent = calculate_y_emergent(0.999997, self.o_observer)
        
        print(f"  O_observer: {self.o_observer:.10f}")
        print(f"  Y_BASE: {self.Y:.15f}")
        print(f"  Y_M: {self.Y_m:.15e}")
        
        # Encoding strategies
        self.strategies = {
            'standard': OffBitEncodingStrategy.standard_encoding,
            'inverted': OffBitEncodingStrategy.inverted_encoding,
            'complexity_focused': OffBitEncodingStrategy.complexity_focused_encoding,
            'balanced': OffBitEncodingStrategy.balanced_encoding
        }
        
        self.results = {strategy: [] for strategy in self.strategies.keys()}
    
    def analyze_molecule_with_strategy(self, molecule_data, strategy_name):
        """Analyze molecule with specific encoding strategy"""
        
        mol_id = molecule_data['id']
        name = molecule_data['name']
        mol_weight = molecule_data['molecular_weight']
        carbon_count = molecule_data['carbon_count']
        mol_type = molecule_data['type']
        freq_hz = molecule_data['estimated_frequency_hz']
        complexity = molecule_data.get('complexity', len(str(molecule_data.get('smiles', ''))))
        
        result = {
            'id': mol_id,
            'name': name,
            'type': mol_type,
            'strategy': strategy_name
        }
        
        try:
            # Generate bit state with this strategy
            encoding_func = self.strategies[strategy_name]
            bit_state = encoding_func(mol_weight, carbon_count, freq_hz, complexity)
            
            # GLR Correction
            glr_result = self.glr.process_correction(bit_state)
            result['glr_errors'] = glr_result.error_count
            result['glr_nrci_before'] = glr_result.nrci_before
            result['glr_nrci_after'] = glr_result.nrci_after
            result['glr_efficiency'] = glr_result.correction_efficiency
            
            # Calculate NRCI
            pattern_sim = self.generate_pattern(mol_weight, carbon_count, complexity)
            pattern_theo = np.random.normal(0, 1.0, len(pattern_sim))
            nrci_result = self.nrci_calc.compute_basic_nrci(pattern_sim, pattern_theo)
            result['nrci'] = nrci_result.value
            
            # SOC Energy
            modal_sum = carbon_count * 0.1 + mol_weight * 0.001
            soc_result = self.soc_calc.calculate_soc_energy(modal_sum=modal_sum, M=mol_weight, C=1.0)
            result['soc_energy_cu'] = soc_result.energy_cu
            
            # Wall check
            wall_status = self.wall.detect_wall_approach(freq_hz)
            result['wall_safe'] = self.wall.check_frequency_limit(freq_hz)
            
            # Coherence factor
            result['coherence_factor'] = result['nrci'] * (1.0 + np.log10(max(result['soc_energy_cu'], 1.0)) / 10.0)
            
            result['success'] = True
            
        except Exception as e:
            result['success'] = False
            result['error'] = str(e)
            for key in ['glr_errors', 'glr_nrci_after', 'glr_efficiency', 'nrci', 'soc_energy_cu', 'coherence_factor']:
                result[key] = None
        
        return result
    
    def generate_pattern(self, mol_weight, carbon_count, complexity):
        """Generate molecular pattern"""
        np.random.seed(int(mol_weight * carbon_count) % 10000)
        pattern = np.random.normal(0, 0.05, 1000)
        pattern += np.sin(np.linspace(0, carbon_count * np.pi, 1000)) * 0.01
        return pattern
    
    def analyze_dataset(self, molecules_df, sample_size=100):
        """Analyze dataset with all encoding strategies"""
        
        # Sample for faster analysis
        if len(molecules_df) > sample_size:
            molecules_df = molecules_df.sample(n=sample_size, random_state=42)
        
        print(f"\nAnalyzing {len(molecules_df)} molecules with {len(self.strategies)} encoding strategies...")
        print("=" * 80)
        
        for strategy_name in self.strategies.keys():
            print(f"\nStrategy: {strategy_name}")
            for idx, row in molecules_df.iterrows():
                if (idx + 1) % 25 == 0:
                    print(f"  Progress: {idx + 1}/{len(molecules_df)}")
                
                result = self.analyze_molecule_with_strategy(row.to_dict(), strategy_name)
                self.results[strategy_name].append(result)
        
        print(f"\n✓ Analysis complete")
        
        return {strategy: pd.DataFrame(results) for strategy, results in self.results.items()}
    
    def compare_strategies(self, results_dfs):
        """Compare encoding strategies"""
        
        print("\n" + "=" * 80)
        print("ENCODING STRATEGY COMPARISON")
        print("=" * 80)
        
        comparison = {}
        
        for strategy_name, df in results_dfs.items():
            success_df = df[df['success'] == True]
            
            comparison[strategy_name] = {
                'mean_nrci': float(success_df['nrci'].mean()),
                'std_nrci': float(success_df['nrci'].std()),
                'mean_glr_efficiency': float(success_df['glr_efficiency'].mean()),
                'mean_glr_errors': float(success_df['glr_errors'].mean()),
                'mean_coherence': float(success_df['coherence_factor'].mean()),
                'nrci_improvement': float((success_df['glr_nrci_after'] - success_df['glr_nrci_before']).mean())
            }
            
            print(f"\n{strategy_name.upper()}:")
            print(f"  Mean NRCI: {comparison[strategy_name]['mean_nrci']:.6f}")
            print(f"  NRCI Std Dev: {comparison[strategy_name]['std_nrci']:.6f}")
            print(f"  Mean GLR Efficiency: {comparison[strategy_name]['mean_glr_efficiency']:.4f}")
            print(f"  Mean GLR Errors Corrected: {comparison[strategy_name]['mean_glr_errors']:.2f}")
            print(f"  Mean Coherence Factor: {comparison[strategy_name]['mean_coherence']:.6f}")
            print(f"  NRCI Improvement: {comparison[strategy_name]['nrci_improvement']:.6f}")
        
        return comparison
    
    def visualize_comparison(self, results_dfs):
        """Create comparison visualizations"""
        
        print("\nGenerating comparison visualizations...")
        
        fig = plt.figure(figsize=(20, 12))
        
        # 1. NRCI by Strategy
        plt.subplot(2, 3, 1)
        data = [results_dfs[s][results_dfs[s]['success']]['nrci'].dropna() for s in self.strategies.keys()]
        plt.boxplot(data, labels=list(self.strategies.keys()))
        plt.ylabel('NRCI')
        plt.title('NRCI Distribution by Encoding Strategy')
        plt.xticks(rotation=45)
        
        # 2. GLR Efficiency by Strategy
        plt.subplot(2, 3, 2)
        data = [results_dfs[s][results_dfs[s]['success']]['glr_efficiency'].dropna() for s in self.strategies.keys()]
        plt.boxplot(data, labels=list(self.strategies.keys()))
        plt.ylabel('GLR Efficiency')
        plt.title('GLR Correction Efficiency by Strategy')
        plt.xticks(rotation=45)
        
        # 3. Coherence Factor by Strategy
        plt.subplot(2, 3, 3)
        data = [results_dfs[s][results_dfs[s]['success']]['coherence_factor'].dropna() for s in self.strategies.keys()]
        plt.boxplot(data, labels=list(self.strategies.keys()))
        plt.ylabel('Coherence Factor')
        plt.title('Coherence Factor by Strategy')
        plt.xticks(rotation=45)
        
        # 4. GLR Errors Corrected
        plt.subplot(2, 3, 4)
        means = [results_dfs[s][results_dfs[s]['success']]['glr_errors'].mean() for s in self.strategies.keys()]
        plt.bar(list(self.strategies.keys()), means)
        plt.ylabel('Mean Errors Corrected')
        plt.title('Mean GLR Errors Corrected by Strategy')
        plt.xticks(rotation=45)
        
        # 5. NRCI Improvement
        plt.subplot(2, 3, 5)
        improvements = [(results_dfs[s][results_dfs[s]['success']]['glr_nrci_after'] - 
                        results_dfs[s][results_dfs[s]['success']]['glr_nrci_before']).mean() 
                       for s in self.strategies.keys()]
        plt.bar(list(self.strategies.keys()), improvements)
        plt.ylabel('Mean NRCI Improvement')
        plt.title('NRCI Improvement After GLR by Strategy')
        plt.xticks(rotation=45)
        
        # 6. Strategy Rankings
        plt.subplot(2, 3, 6)
        rankings = {}
        for s in self.strategies.keys():
            df = results_dfs[s][results_dfs[s]['success']]
            rankings[s] = df['coherence_factor'].mean()
        
        sorted_strategies = sorted(rankings.items(), key=lambda x: x[1], reverse=True)
        names = [s[0] for s in sorted_strategies]
        values = [s[1] for s in sorted_strategies]
        
        plt.barh(names, values)
        plt.xlabel('Mean Coherence Factor')
        plt.title('Strategy Ranking by Coherence')
        
        plt.tight_layout()
        plt.savefig('ubp_encoding_strategy_comparison.png', dpi=300, bbox_inches='tight')
        print("  ✓ Saved: ubp_encoding_strategy_comparison.png")
        plt.close()

def main():
    print("=" * 80)
    print("UBP 3.3 PETROLEUM ANALYSIS - MULTI-ENCODING COMPARISON")
    print("Author: Euan R A Craig")
    print("=" * 80)
    
    # Load data
    print("\nLoading petroleum molecules...")
    molecules_df = pd.read_csv('petroleum_molecules_1000.csv')
    print(f"Loaded {len(molecules_df)} molecules")
    
    # Initialize analyzer
    analyzer = MultiEncodingPetroleumAnalyzer()
    
    # Analyze with all strategies
    results_dfs = analyzer.analyze_dataset(molecules_df, sample_size=200)
    
    # Save results
    print("\nSaving results...")
    for strategy_name, df in results_dfs.items():
        df.to_csv(f'ubp_results_{strategy_name}.csv', index=False)
        print(f"  ✓ Saved: ubp_results_{strategy_name}.csv")
    
    # Compare strategies
    comparison = analyzer.compare_strategies(results_dfs)
    
    with open('encoding_strategy_comparison.json', 'w') as f:
        json.dump(comparison, f, indent=2)
    print("\n  ✓ Saved: encoding_strategy_comparison.json")
    
    # Visualize
    analyzer.visualize_comparison(results_dfs)
    
    # Determine best strategy
    best_strategy = max(comparison.items(), key=lambda x: x[1]['mean_coherence'])
    
    print("\n" + "=" * 80)
    print("CONCLUSION")
    print("=" * 80)
    print(f"\nBest Encoding Strategy: {best_strategy[0].upper()}")
    print(f"  Mean Coherence: {best_strategy[1]['mean_coherence']:.6f}")
    print(f"  Mean NRCI: {best_strategy[1]['mean_nrci']:.6f}")
    print(f"  GLR Efficiency: {best_strategy[1]['mean_glr_efficiency']:.4f}")
    
    print("\n✓ MULTI-ENCODING ANALYSIS COMPLETE")

if __name__ == '__main__':
    main()
