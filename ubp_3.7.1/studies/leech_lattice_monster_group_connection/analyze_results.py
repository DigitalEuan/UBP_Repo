import pandas as pd
import numpy as np
import os
from scipy.stats import pearsonr

# --- Configuration ---
DATA_FILE = 'data/monster_study_results.csv'
DATA_PATH = os.path.join(os.path.dirname(__file__), DATA_FILE)
OUTPUT_FILE = 'analysis_summary.md'
OUTPUT_PATH = os.path.join(os.path.dirname(__file__), OUTPUT_FILE)

# --- Analysis ---
def analyze_data():
    """
    Loads the study data, calculates key statistics, and determines the
    correlation between TGIC Coherence and the Monster Group Proxy Metric.
    """
    try:
        df = pd.read_csv(DATA_PATH)
    except FileNotFoundError:
        return "Error: Data file not found at " + DATA_PATH

    # Convert relevant columns to numeric types
    df['tgic_coherence'] = pd.to_numeric(df['tgic_coherence'])
    df['distance_to_codeword_weight'] = pd.to_numeric(df['distance_to_codeword_weight'])
    df['is_golay_codeword'] = df['is_golay_codeword'].astype(int)
    
    # --- Key Metrics ---
    
    # 1. Correlation between TGIC Coherence and DCW (Distance to Codeword Weight)
    # Hypothesis: Higher coherence (closer to 1.0) should correlate with lower DCW (closer to 0).
    # Therefore, we expect a negative correlation.
    corr_coherence_dcw, p_value_coherence_dcw = pearsonr(
        df['tgic_coherence'], df['distance_to_codeword_weight']
    )
    
    # 2. Mean Coherence for Golay Codewords vs. Non-Codewords
    mean_coherence_golay = df[df['is_golay_codeword'] == 1]['tgic_coherence'].mean()
    mean_coherence_non_golay = df[df['is_golay_codeword'] == 0]['tgic_coherence'].mean()
    
    # 3. Distribution of DCW
    dcw_counts = df['distance_to_codeword_weight'].value_counts().sort_index()
    
    # 4. Distribution of Coherence
    coherence_stats = df['tgic_coherence'].describe()
    
    # --- Generate Summary Report ---
    report = f"""# UBP 3.7.1 Monster Group Connection Study: Analysis Summary

## 1. Study Overview
- **Total Samples:** {len(df)}
- **TGIC Geometry Used:** CubicGraph (Proxy mapping: OffBit weight to Node weights)
- **Monster Group Proxy Metric (MGPM):** Distance to Golay Codeword Weight (DCW)

## 2. Key Correlation Result
The central hypothesis is that states with higher TGIC Coherence (Information-First principle) should naturally align with the underlying mathematical structure (Golay/Leech) that gives rise to the Monster Group. This is tested by correlating TGIC Coherence with the Distance to Codeword Weight (DCW).

| Metric | Value | P-Value | Interpretation |
| :--- | :--- | :--- | :--- |
| **Pearson Correlation (Coherence vs. DCW)** | **{corr_coherence_dcw:.6f}** | {p_value_coherence_dcw:.6f} | Negative correlation supports the hypothesis. |

## 3. Coherence Comparison: Golay vs. Non-Golay States
This compares the average TGIC Coherence for OffBits that are valid Golay codewords (DCW=0) versus those that are not.

| State Type | Average TGIC Coherence |
| :--- | :--- |
| **Valid Golay Codewords (MGPM=0)** | **{mean_coherence_golay:.6f}** |
| **Non-Golay Codewords (MGPM>0)** | **{mean_coherence_non_golay:.6f}** |

## 4. TGIC Coherence Distribution
{coherence_stats.to_markdown()}

## 5. Distance to Codeword Weight (DCW) Distribution
This shows how frequently OffBits are close to the Golay structure.

| DCW | Count | Percentage |
| :--- | :--- | :--- |
{dcw_counts.to_frame(name='Count').reset_index().assign(Percentage=lambda x: (x['Count'] / len(df) * 100).round(2)).to_markdown(index=False)}

## 6. Scientific Conclusion and Next Steps
The correlation result and the coherence comparison will provide the first computational evidence for or against the UBP's ability to naturally generate the underlying structure of the Monster Group.

- **If the correlation is significantly negative** and **mean_coherence_golay > mean_coherence_non_golay**, it suggests that the TGIC constraints inherently favor states that are mathematically significant to the Leech Lattice/Monster Group connection.
- **If the correlation is near zero**, it suggests the current proxy mapping (OffBit weight to Node weights) is insufficient to capture the deep connection, and a more direct mapping (e.g., OffBit bits to Node activation states) or a different TGIC geometry (e.g., LeechLatticeProjection) is required.

**Next Steps:**
1. Interpret the results.
2. Based on the interpretation, suggest adjustments to the UBP framework or the study methodology for further investigation.
"""
    
    with open(OUTPUT_PATH, 'w') as f:
        f.write(report)
        
    return report

if __name__ == '__main__':
    analysis_report = analyze_data()
    print("Analysis complete. Report saved to " + OUTPUT_PATH)
    # Print key results for immediate review
    print("\n--- Key Results ---")
    print(analysis_report.split('## 2. Key Correlation Result')[1].split('## 3. Coherence Comparison')[0])
    print("\n--- Coherence Comparison ---")
    print(analysis_report.split('## 3. Coherence Comparison')[1].split('## 4. TGIC Coherence Distribution')[0])
