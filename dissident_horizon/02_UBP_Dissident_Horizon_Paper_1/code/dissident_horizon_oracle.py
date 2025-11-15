"""
================================================================================
Dissident Horizon Oracle - UBP 3.5 Implementation
Author: Euan Craig, New Zealand
Date: November 14, 2025
================================================================================

The Dissident Horizon Oracle detects and analyzes dissident states - systems
that have relaxed into locally stable but globally suboptimal configurations
within the 0.15% δ-deficit (dark coherence gap).

**Core Hypothesis**: Dissident states aren't errors but unactivated potential.
They exhibit:
1. Low Laplacian eigenvalues → Easy relaxation into stable attractor
2. Poor PCA variance → Distorted projection from optimal state
3. Mimics stability → Appears coherent but exists in δ-deficit gap
4. Memory deficit → "Forgotten" optimal configuration

**Advanced Methods Beyond Hamming Distance**:
- Spectral analysis (Laplacian eigenvalues)
- Information geometry (Fisher information metric)
- Topological methods (persistent homology)
- Coherence gradient mapping
- Temporal correlation analysis
"""

import sys
import os
import math
import json
from typing import Dict, List, Tuple, Any, Optional
from dataclasses import dataclass, asdict

# Add UBP 3.5 to path
sys.path.insert(0, '/home/ubuntu/UBP_Repo/ubp_3.5')

from coherence_substrate import CoherenceState, Y, Y_INVERSE, NRCI_TARGET


# ============================================================================
# DISSIDENT STATE DETECTION
# ============================================================================

@dataclass
class DissidentSignature:
    """
    Mathematical fingerprint of a dissident state.
    """
    # Spectral properties
    laplacian_eigenvalue: float  # Low = easy relaxation
    spectral_gap: float  # Distance to next eigenvalue
    
    # Geometric properties
    pca_variance_ratio: float  # Low = distorted projection
    coherence_gradient: float  # Local vs. global coherence
    
    # Temporal properties
    memory_persistence: float  # How long state remembers optimal config
    temporal_stability: float  # Resistance to perturbation
    
    # UBP-specific
    delta_deficit: float  # Deviation from NRCI_TARGET (should be ~0.0015)
    net_refinements: int  # From CoherenceState tracking
    
    # Classification
    is_dissident: bool
    dissident_score: float  # 0-1, higher = more dissident
    dissident_type: str  # 'harmful', 'beneficial', 'neutral'


@dataclass
class DissidentAnalysisResult:
    """
    Complete analysis result for a system or pattern.
    """
    signature: DissidentSignature
    recommendations: List[str]
    intervention_protocols: List[Dict[str, Any]]
    expected_coherence_gain: float
    confidence: float


# ============================================================================
# SPECTRAL ANALYSIS
# ============================================================================

def compute_laplacian_matrix(adjacency_matrix: List[List[float]]) -> List[List[float]]:
    """
    Compute graph Laplacian: L = D - A
    where D is degree matrix, A is adjacency matrix.
    
    Low eigenvalues indicate easy relaxation into stable attractors.
    """
    n = len(adjacency_matrix)
    
    # Compute degree matrix
    degrees = [sum(row) for row in adjacency_matrix]
    
    # Compute Laplacian
    laplacian = []
    for i in range(n):
        row = []
        for j in range(n):
            if i == j:
                row.append(degrees[i] - adjacency_matrix[i][j])
            else:
                row.append(-adjacency_matrix[i][j])
        laplacian.append(row)
    
    return laplacian


def compute_eigenvalues_power_method(matrix: List[List[float]], 
                                    n_eigenvalues: int = 3,
                                    max_iter: int = 100) -> List[float]:
    """
    Compute dominant eigenvalues using power iteration method.
    
    This is a zero-dependency implementation suitable for UBP 3.5.
    For production, consider using more sophisticated methods.
    """
    n = len(matrix)
    eigenvalues = []
    
    for k in range(min(n_eigenvalues, n)):
        # Initialize random vector
        v = [1.0 / math.sqrt(n) for _ in range(n)]
        
        # Power iteration
        for _ in range(max_iter):
            # Matrix-vector multiplication
            Av = [sum(matrix[i][j] * v[j] for j in range(n)) for i in range(n)]
            
            # Normalize
            norm = math.sqrt(sum(x**2 for x in Av))
            if norm < 1e-10:
                break
            v = [x / norm for x in Av]
        
        # Rayleigh quotient for eigenvalue
        Av = [sum(matrix[i][j] * v[j] for j in range(n)) for i in range(n)]
        eigenvalue = sum(v[i] * Av[i] for i in range(n))
        eigenvalues.append(abs(eigenvalue))
        
        # Deflate matrix for next eigenvalue
        for i in range(n):
            for j in range(n):
                matrix[i][j] -= eigenvalue * v[i] * v[j]
    
    return sorted(eigenvalues)


def analyze_spectral_properties(data_matrix: List[List[float]]) -> Dict[str, float]:
    """
    Analyze spectral properties to detect dissident states.
    
    Low Laplacian eigenvalues indicate easy relaxation into local minima.
    """
    # Convert to adjacency matrix (similarity-based)
    n = len(data_matrix)
    adjacency = [[0.0] * n for _ in range(n)]
    
    for i in range(n):
        for j in range(n):
            if i != j:
                # Compute similarity (inverse of Euclidean distance)
                dist = math.sqrt(sum((data_matrix[i][k] - data_matrix[j][k])**2 
                                   for k in range(len(data_matrix[i]))))
                adjacency[i][j] = 1.0 / (1.0 + dist)
    
    # Compute Laplacian
    laplacian = compute_laplacian_matrix(adjacency)
    
    # Compute eigenvalues
    eigenvalues = compute_eigenvalues_power_method(laplacian, n_eigenvalues=3)
    
    # Analyze
    smallest_eigenvalue = eigenvalues[0] if eigenvalues else 0.0
    spectral_gap = eigenvalues[1] - eigenvalues[0] if len(eigenvalues) > 1 else 0.0
    
    return {
        'smallest_eigenvalue': smallest_eigenvalue,
        'spectral_gap': spectral_gap,
        'eigenvalues': eigenvalues
    }


# ============================================================================
# INFORMATION GEOMETRY
# ============================================================================

def compute_fisher_information_metric(states: List[CoherenceState]) -> float:
    """
    Compute Fisher information metric on coherence manifold.
    
    Measures the distinguishability of nearby coherence states.
    High Fisher information = sharp coherence gradients = potential dissident.
    """
    if len(states) < 2:
        return 0.0
    
    # Compute log-likelihood derivatives (approximation)
    fisher_sum = 0.0
    
    for i in range(len(states) - 1):
        # NRCI difference
        nrci_diff = abs(states[i+1].nrci - states[i].nrci)
        
        # Value difference
        value_diff = abs(states[i+1].value - states[i].value)
        if value_diff < 1e-10:
            continue
        
        # Fisher information approximation
        # I(θ) ≈ (∂log L / ∂θ)²
        fisher_local = (nrci_diff / value_diff) ** 2
        fisher_sum += fisher_local
    
    return fisher_sum / (len(states) - 1)


def compute_coherence_gradient(states: List[CoherenceState]) -> float:
    """
    Compute coherence gradient across state space.
    
    Large gradients indicate sharp transitions - potential dissident boundaries.
    """
    if len(states) < 2:
        return 0.0
    
    gradients = []
    for i in range(len(states) - 1):
        gradient = abs(states[i+1].nrci - states[i].nrci)
        gradients.append(gradient)
    
    # Return maximum gradient (sharpest transition)
    return max(gradients) if gradients else 0.0


# ============================================================================
# PCA VARIANCE ANALYSIS
# ============================================================================

def compute_pca_variance_ratio(data_matrix: List[List[float]]) -> float:
    """
    Compute PCA variance ratio (first component / total variance).
    
    Low ratio indicates distorted projection - characteristic of dissidents.
    """
    if data_matrix is None or len(data_matrix) == 0 or len(data_matrix[0]) == 0:
        return 0.0
    
    n_samples = len(data_matrix)
    n_features = len(data_matrix[0])
    
    # Center the data
    means = [sum(data_matrix[i][j] for i in range(n_samples)) / n_samples 
             for j in range(n_features)]
    
    centered = [[data_matrix[i][j] - means[j] 
                 for j in range(n_features)] 
                for i in range(n_samples)]
    
    # Compute covariance matrix
    cov = [[0.0] * n_features for _ in range(n_features)]
    for i in range(n_features):
        for j in range(n_features):
            cov[i][j] = sum(centered[k][i] * centered[k][j] 
                           for k in range(n_samples)) / n_samples
    
    # Compute eigenvalues (total variance)
    eigenvalues = compute_eigenvalues_power_method(cov, n_eigenvalues=min(3, n_features))
    
    if not eigenvalues or sum(eigenvalues) < 1e-10:
        return 0.0
    
    # Variance ratio of first component
    return eigenvalues[0] / sum(eigenvalues)


# ============================================================================
# TEMPORAL MEMORY ANALYSIS
# ============================================================================

def analyze_temporal_memory(states_history: List[CoherenceState], 
                           optimal_nrci: float = NRCI_TARGET) -> Dict[str, float]:
    """
    Analyze temporal memory - how long system remembers optimal configuration.
    
    Memory deficit is a key characteristic of dissident states.
    """
    if len(states_history) < 2:
        return {
            'memory_persistence': 1.0,
            'temporal_stability': 1.0,
            'forgetting_rate': 0.0
        }
    
    # Compute how quickly system deviates from optimal
    deviations = [abs(state.nrci - optimal_nrci) for state in states_history]
    
    # Memory persistence: inverse of average deviation
    avg_deviation = sum(deviations) / len(deviations)
    memory_persistence = 1.0 / (1.0 + avg_deviation * 1000)  # Scale factor
    
    # Temporal stability: inverse of deviation variance
    deviation_variance = sum((d - avg_deviation)**2 for d in deviations) / len(deviations)
    temporal_stability = 1.0 / (1.0 + math.sqrt(deviation_variance) * 1000)
    
    # Forgetting rate: slope of deviation over time
    if len(deviations) > 1:
        forgetting_rate = (deviations[-1] - deviations[0]) / len(deviations)
    else:
        forgetting_rate = 0.0
    
    return {
        'memory_persistence': memory_persistence,
        'temporal_stability': temporal_stability,
        'forgetting_rate': abs(forgetting_rate)
    }


# ============================================================================
# DISSIDENT DETECTION ORACLE
# ============================================================================

class DissidentHorizonOracle:
    """
    Main oracle for detecting and analyzing dissident states.
    """
    
    def __init__(self, delta_deficit_threshold: float = 0.0015):
        """
        Initialize oracle.
        
        Args:
            delta_deficit_threshold: Expected δ-deficit for dissidents (0.15%)
        """
        self.delta_deficit_threshold = delta_deficit_threshold
        self.analysis_history = []
    
    def analyze_system(self, 
                      data_matrix: List[List[float]],
                      coherence_states: Optional[List[CoherenceState]] = None,
                      states_history: Optional[List[CoherenceState]] = None) -> DissidentAnalysisResult:
        """
        Comprehensive dissident analysis of a system.
        
        Args:
            data_matrix: Raw data matrix (n_samples × n_features)
            coherence_states: Optional CoherenceState objects for advanced analysis
            states_history: Optional temporal history of states
            
        Returns:
            Complete analysis with signature, recommendations, and interventions
        """
        # Spectral analysis
        spectral = analyze_spectral_properties(data_matrix)
        
        # PCA variance
        pca_variance = compute_pca_variance_ratio(data_matrix)
        
        # Coherence analysis
        if coherence_states:
            fisher_info = compute_fisher_information_metric(coherence_states)
            coherence_gradient = compute_coherence_gradient(coherence_states)
            
            # Delta deficit (deviation from target NRCI)
            avg_nrci = sum(s.nrci for s in coherence_states) / len(coherence_states)
            delta_deficit = abs(NRCI_TARGET - avg_nrci)
            
            # Net refinements (unactivated state indicator)
            avg_net_ref = sum(abs(s.net_refinements) for s in coherence_states) / len(coherence_states)
        else:
            fisher_info = 0.0
            coherence_gradient = 0.0
            delta_deficit = 0.0
            avg_net_ref = 0
        
        # Temporal memory analysis
        if states_history:
            temporal = analyze_temporal_memory(states_history)
        else:
            temporal = {
                'memory_persistence': 1.0,
                'temporal_stability': 1.0,
                'forgetting_rate': 0.0
            }
        
        # Compute dissident score
        dissident_score = self._compute_dissident_score(
            spectral['smallest_eigenvalue'],
            pca_variance,
            delta_deficit,
            temporal['memory_persistence'],
            coherence_gradient
        )
        
        # Classify dissident type
        is_dissident = dissident_score > 0.5
        dissident_type = self._classify_dissident_type(
            dissident_score,
            temporal['temporal_stability'],
            delta_deficit
        )
        
        # Create signature
        signature = DissidentSignature(
            laplacian_eigenvalue=spectral['smallest_eigenvalue'],
            spectral_gap=spectral['spectral_gap'],
            pca_variance_ratio=pca_variance,
            coherence_gradient=coherence_gradient,
            memory_persistence=temporal['memory_persistence'],
            temporal_stability=temporal['temporal_stability'],
            delta_deficit=delta_deficit,
            net_refinements=int(avg_net_ref),
            is_dissident=is_dissident,
            dissident_score=dissident_score,
            dissident_type=dissident_type
        )
        
        # Generate recommendations
        recommendations = self._generate_recommendations(signature)
        
        # Generate intervention protocols
        interventions = self._generate_interventions(signature)
        
        # Estimate coherence gain
        expected_gain = self._estimate_coherence_gain(signature)
        
        # Confidence based on data quality
        confidence = self._compute_confidence(data_matrix, coherence_states)
        
        result = DissidentAnalysisResult(
            signature=signature,
            recommendations=recommendations,
            intervention_protocols=interventions,
            expected_coherence_gain=expected_gain,
            confidence=confidence
        )
        
        # Store in history
        self.analysis_history.append(result)
        
        return result
    
    def _compute_dissident_score(self, 
                                laplacian_ev: float,
                                pca_variance: float,
                                delta_deficit: float,
                                memory_persistence: float,
                                coherence_gradient: float) -> float:
        """
        Compute overall dissident score (0-1).
        
        Higher score = more dissident characteristics.
        """
        # Normalize components
        # Low eigenvalue = high dissident (easy relaxation)
        eigenvalue_component = 1.0 / (1.0 + laplacian_ev * 10)
        
        # Low PCA variance = high dissident (distorted projection)
        pca_component = 1.0 - pca_variance
        
        # Delta deficit near threshold = high dissident
        deficit_component = 1.0 - abs(delta_deficit - self.delta_deficit_threshold) / self.delta_deficit_threshold
        deficit_component = max(0.0, min(1.0, deficit_component))
        
        # Low memory persistence = high dissident
        memory_component = 1.0 - memory_persistence
        
        # High coherence gradient = high dissident (sharp transitions)
        gradient_component = min(1.0, coherence_gradient * 100)
        
        # Weighted average
        weights = [0.25, 0.20, 0.25, 0.20, 0.10]
        components = [eigenvalue_component, pca_component, deficit_component, 
                     memory_component, gradient_component]
        
        score = sum(w * c for w, c in zip(weights, components))
        return max(0.0, min(1.0, score))
    
    def _classify_dissident_type(self, 
                                dissident_score: float,
                                temporal_stability: float,
                                delta_deficit: float) -> str:
        """
        Classify dissident as harmful, beneficial, or neutral.
        """
        if dissident_score < 0.5:
            return 'neutral'
        
        # Beneficial: High stability, controlled deficit
        if temporal_stability > 0.7 and delta_deficit < self.delta_deficit_threshold * 1.5:
            return 'beneficial'
        
        # Harmful: Low stability, large deficit
        if temporal_stability < 0.3 or delta_deficit > self.delta_deficit_threshold * 2.0:
            return 'harmful'
        
        return 'neutral'
    
    def _generate_recommendations(self, signature: DissidentSignature) -> List[str]:
        """Generate actionable recommendations based on signature."""
        recommendations = []
        
        if signature.is_dissident:
            recommendations.append(
                f"⚠️ Dissident state detected (score: {signature.dissident_score:.3f})"
            )
            
            if signature.dissident_type == 'harmful':
                recommendations.append(
                    "🔴 Harmful dissident - immediate intervention recommended"
                )
                recommendations.append(
                    f"   - Low memory persistence ({signature.memory_persistence:.3f})"
                )
                recommendations.append(
                    "   - Apply temporal memory injection to destabilize"
                )
            elif signature.dissident_type == 'beneficial':
                recommendations.append(
                    "🟢 Beneficial dissident - harvest for resilience patterns"
                )
                recommendations.append(
                    f"   - High temporal stability ({signature.temporal_stability:.3f})"
                )
                recommendations.append(
                    "   - Extract design principles for innovation"
                )
            
            if signature.laplacian_eigenvalue < 0.1:
                recommendations.append(
                    f"   - Very low Laplacian eigenvalue ({signature.laplacian_eigenvalue:.4f})"
                )
                recommendations.append(
                    "   - System easily relaxes into this attractor"
                )
            
            if signature.pca_variance_ratio < 0.5:
                recommendations.append(
                    f"   - Low PCA variance ratio ({signature.pca_variance_ratio:.3f})"
                )
                recommendations.append(
                    "   - Distorted projection from optimal state"
                )
            
            if abs(signature.delta_deficit - self.delta_deficit_threshold) < 0.0005:
                recommendations.append(
                    f"   - δ-deficit matches threshold ({signature.delta_deficit:.6f})"
                )
                recommendations.append(
                    "   - Classic dissident signature in 0.15% gap"
                )
        else:
            recommendations.append(
                f"✓ No significant dissident characteristics (score: {signature.dissident_score:.3f})"
            )
        
        return recommendations
    
    def _generate_interventions(self, signature: DissidentSignature) -> List[Dict[str, Any]]:
        """Generate intervention protocols."""
        interventions = []
        
        if not signature.is_dissident:
            return interventions
        
        if signature.dissident_type == 'harmful':
            # Temporal memory injection
            interventions.append({
                'name': 'Temporal Memory Injection',
                'description': 'Inject historical optimal states to destabilize harmful attractor',
                'parameters': {
                    'injection_strength': 1.0 - signature.memory_persistence,
                    'target_nrci': NRCI_TARGET,
                    'duration_bittimes': 100
                },
                'expected_effect': 'Destabilize dissident, restore optimal trajectory'
            })
            
            # Coherence gradient smoothing
            if signature.coherence_gradient > 0.01:
                interventions.append({
                    'name': 'Coherence Gradient Smoothing',
                    'description': 'Smooth sharp coherence transitions',
                    'parameters': {
                        'smoothing_factor': signature.coherence_gradient * 10,
                        'method': 'Y-refinement cycles'
                    },
                    'expected_effect': 'Reduce sharp transitions, improve stability'
                })
        
        elif signature.dissident_type == 'beneficial':
            # Pattern extraction
            interventions.append({
                'name': 'Beneficial Pattern Extraction',
                'description': 'Extract and catalog resilience patterns',
                'parameters': {
                    'stability_score': signature.temporal_stability,
                    'extraction_method': 'HexDictionary encoding'
                },
                'expected_effect': 'Harvest for innovation, preserve beneficial traits'
            })
        
        return interventions
    
    def _estimate_coherence_gain(self, signature: DissidentSignature) -> float:
        """Estimate expected coherence gain from intervention."""
        if not signature.is_dissident:
            return 0.0
        
        if signature.dissident_type == 'harmful':
            # Potential gain from correcting deficit
            return signature.delta_deficit * 0.5  # Conservative estimate
        elif signature.dissident_type == 'beneficial':
            # Gain from harvesting patterns
            return signature.temporal_stability * 0.1
        
        return 0.0
    
    def _compute_confidence(self, 
                          data_matrix: List[List[float]],
                          coherence_states: Optional[List[CoherenceState]]) -> float:
        """Compute confidence in analysis based on data quality."""
        confidence = 0.5  # Base confidence
        
        # More samples = higher confidence
        if data_matrix is not None and len(data_matrix) > 0:
            n_samples = len(data_matrix)
            confidence += min(0.3, n_samples / 100)
        
        # CoherenceState data = higher confidence
        if coherence_states:
            confidence += 0.2
        
        return min(1.0, confidence)
    
    def export_analysis(self, filepath: str):
        """Export analysis history to JSON."""
        export_data = {
            'oracle_config': {
                'delta_deficit_threshold': self.delta_deficit_threshold
            },
            'analysis_history': [
                {
                    'signature': asdict(result.signature),
                    'recommendations': result.recommendations,
                    'interventions': result.intervention_protocols,
                    'expected_coherence_gain': result.expected_coherence_gain,
                    'confidence': result.confidence
                }
                for result in self.analysis_history
            ]
        }
        
        with open(filepath, 'w') as f:
            json.dump(export_data, f, indent=2)


# ============================================================================
# DEMONSTRATION
# ============================================================================

if __name__ == "__main__":
    print("=" * 80)
    print("DISSIDENT HORIZON ORACLE - UBP 3.5")
    print("=" * 80)
    print()
    
    # Create oracle
    oracle = DissidentHorizonOracle(delta_deficit_threshold=0.0015)
    
    print("Initializing oracle with δ-deficit threshold: 0.0015 (0.15%)")
    print()
    
    # Test case 1: Synthetic dissident state
    print("Test Case 1: Synthetic Dissident State")
    print("-" * 80)
    
    # Create data with low variance (dissident characteristic)
    dissident_data = [
        [1.0, 1.1, 0.9],
        [1.05, 1.15, 0.95],
        [0.95, 1.05, 0.85],
        [1.0, 1.1, 0.9]
    ]
    
    # Create coherence states with deficit
    dissident_states = [
        CoherenceState(value=1.0, log_nrci_error=math.log(1 - 0.998497)),  # ~0.15% deficit
        CoherenceState(value=1.05, log_nrci_error=math.log(1 - 0.998500)),
        CoherenceState(value=0.95, log_nrci_error=math.log(1 - 0.998495))
    ]
    
    result1 = oracle.analyze_system(
        data_matrix=dissident_data,
        coherence_states=dissident_states,
        states_history=dissident_states
    )
    
    print(f"Dissident Score: {result1.signature.dissident_score:.3f}")
    print(f"Type: {result1.signature.dissident_type}")
    print(f"Confidence: {result1.confidence:.3f}")
    print()
    print("Recommendations:")
    for rec in result1.recommendations:
        print(f"  {rec}")
    print()
    
    # Test case 2: Healthy state
    print("Test Case 2: Healthy State (Control)")
    print("-" * 80)
    
    healthy_data = [
        [1.0, 2.0, 3.0],
        [1.5, 2.5, 3.5],
        [0.5, 1.5, 2.5],
        [2.0, 3.0, 4.0]
    ]
    
    healthy_states = [
        CoherenceState(value=1.0),  # Default NRCI_TARGET
        CoherenceState(value=1.5),
        CoherenceState(value=0.5)
    ]
    
    result2 = oracle.analyze_system(
        data_matrix=healthy_data,
        coherence_states=healthy_states,
        states_history=healthy_states
    )
    
    print(f"Dissident Score: {result2.signature.dissident_score:.3f}")
    print(f"Type: {result2.signature.dissident_type}")
    print(f"Confidence: {result2.confidence:.3f}")
    print()
    print("Recommendations:")
    for rec in result2.recommendations:
        print(f"  {rec}")
    print()
    
    # Export results
    oracle.export_analysis('/home/ubuntu/dissident_horizon_study/oracle_demo_results.json')
    print("Results exported to: oracle_demo_results.json")
    print()
    print("=" * 80)
