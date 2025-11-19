"""
================================================================================
HexDictionary v2.0 - Complete Production Module for UBP 3.5
Author: Euan Craig, New Zealand
Date: November 19, 2025
================================================================================

Content-addressable storage with 8 advanced analysis methods.

**8 Analysis Methods**:
1. Cosine Similarity - Fast, general-purpose
2. Euclidean Similarity - Normalized distance
3. Hamming Distance - Bit-level comparison (baseline)
4. Spectral Coherence - Global structure analysis
5. Information Geometry - KL divergence
6. Topological Analysis - Shape-based features
7. Wavelet Multi-Scale - Multi-resolution analysis
8. Frequency Domain - FFT-based analysis

**Dependencies**: Python stdlib + coherence_substrate.py only
"""

import json
import hashlib
import os
import math
from collections import defaultdict
from coherence_substrate import CoherenceState

# ============================================================================
# ANALYSIS METHODS
# ============================================================================

def cosine_similarity(vec1, vec2):
    """Cosine similarity between feature vectors."""
    common_keys = set(vec1.keys()) & set(vec2.keys())
    if not common_keys:
        return 0.0
    
    dot_product = sum(vec1[k] * vec2[k] for k in common_keys)
    mag1 = math.sqrt(sum(vec1[k]**2 for k in common_keys))
    mag2 = math.sqrt(sum(vec2[k]**2 for k in common_keys))
    
    if mag1 == 0 or mag2 == 0:
        return 0.0
    
    return dot_product / (mag1 * mag2)


def euclidean_similarity(vec1, vec2):
    """Normalized Euclidean similarity."""
    common_keys = set(vec1.keys()) & set(vec2.keys())
    if not common_keys:
        return 0.0
    
    # Normalize to [0, 1]
    all_values = []
    for k in common_keys:
        all_values.extend([vec1[k], vec2[k]])
    
    min_val = min(all_values)
    max_val = max(all_values)
    range_val = max_val - min_val if max_val != min_val else 1.0
    
    # Normalized Euclidean distance
    dist = math.sqrt(sum(((vec1[k] - min_val) / range_val - (vec2[k] - min_val) / range_val)**2 
                        for k in common_keys))
    
    max_dist = math.sqrt(len(common_keys))
    return 1.0 - (dist / max_dist) if max_dist > 0 else 0.0


def hamming_similarity(vec1, vec2):
    """Hamming distance converted to similarity (baseline method)."""
    common_keys = set(vec1.keys()) & set(vec2.keys())
    if not common_keys:
        return 0.0
    
    # Convert to binary strings and compare
    total_bits = 0
    matching_bits = 0
    
    for k in common_keys:
        # Convert floats to integer representation
        val1 = int(abs(vec1[k]) * 1000)
        val2 = int(abs(vec2[k]) * 1000)
        
        # XOR to find differing bits
        xor = val1 ^ val2
        bits = bin(xor).count('1')
        max_bits = max(val1.bit_length(), val2.bit_length())
        
        total_bits += max_bits
        matching_bits += (max_bits - bits)
    
    return matching_bits / total_bits if total_bits > 0 else 0.0


def spectral_similarity(vec1, vec2):
    """Spectral coherence based on autocorrelation."""
    common_keys = sorted(set(vec1.keys()) & set(vec2.keys()))
    if not common_keys:
        return 0.0
    
    data1 = [vec1[k] for k in common_keys]
    data2 = [vec2[k] for k in common_keys]
    
    # Autocorrelation at lag 1
    def autocorr(data):
        if len(data) < 2:
            return 0.0
        mean = sum(data) / len(data)
        var = sum((x - mean)**2 for x in data)
        if var == 0:
            return 0.0
        cov = sum((data[i] - mean) * (data[i+1] - mean) for i in range(len(data)-1))
        return cov / var
    
    ac1 = autocorr(data1)
    ac2 = autocorr(data2)
    
    # Similarity based on autocorrelation difference
    return 1.0 - abs(ac1 - ac2)


def information_similarity(vec1, vec2):
    """Information geometry using KL divergence."""
    common_keys = set(vec1.keys()) & set(vec2.keys())
    if not common_keys:
        return 0.0
    
    epsilon = 1e-10
    
    # Normalize to probability distributions
    vals1 = [abs(vec1[k]) + epsilon for k in common_keys]
    vals2 = [abs(vec2[k]) + epsilon for k in common_keys]
    
    sum1 = sum(vals1)
    sum2 = sum(vals2)
    
    p = [v / sum1 for v in vals1]
    q = [v / sum2 for v in vals2]
    
    # Symmetric KL divergence
    kl_pq = sum(pi * math.log(pi / qi) for pi, qi in zip(p, q) if pi > epsilon and qi > epsilon)
    kl_qp = sum(qi * math.log(qi / pi) for pi, qi in zip(p, q) if pi > epsilon and qi > epsilon)
    
    # Convert to similarity (0 = identical, higher = more different)
    kl_sym = (kl_pq + kl_qp) / 2.0
    
    # Normalize to [0, 1] similarity
    return 1.0 / (1.0 + kl_sym)


def topological_similarity(vec1, vec2):
    """Topological analysis based on persistence."""
    common_keys = sorted(set(vec1.keys()) & set(vec2.keys()))
    if not common_keys:
        return 0.0
    
    data1 = [vec1[k] for k in common_keys]
    data2 = [vec2[k] for k in common_keys]
    
    # Compute persistence (simplified: local maxima/minima)
    def compute_features(data):
        if len(data) < 3:
            return []
        features = []
        for i in range(1, len(data)-1):
            if data[i] > data[i-1] and data[i] > data[i+1]:  # Local maximum
                features.append(('max', data[i]))
            elif data[i] < data[i-1] and data[i] < data[i+1]:  # Local minimum
                features.append(('min', data[i]))
        return features
    
    feat1 = compute_features(data1)
    feat2 = compute_features(data2)
    
    # Compare number and magnitude of features
    if not feat1 and not feat2:
        return 1.0
    if not feat1 or not feat2:
        return 0.0
    
    # Similarity based on feature count and average magnitude
    count_sim = min(len(feat1), len(feat2)) / max(len(feat1), len(feat2))
    
    avg1 = sum(abs(v) for _, v in feat1) / len(feat1)
    avg2 = sum(abs(v) for _, v in feat2) / len(feat2)
    mag_sim = 1.0 - abs(avg1 - avg2) / (abs(avg1) + abs(avg2) + 1e-10)
    
    return (count_sim + mag_sim) / 2.0


def wavelet_similarity(vec1, vec2):
    """Wavelet multi-scale analysis."""
    common_keys = sorted(set(vec1.keys()) & set(vec2.keys()))
    if not common_keys:
        return 0.0
    
    data1 = [vec1[k] for k in common_keys]
    data2 = [vec2[k] for k in common_keys]
    
    # Simple Haar wavelet transform
    def haar_transform(data):
        if len(data) < 2:
            return data, []
        approx = [(data[i] + data[i+1]) / 2.0 for i in range(0, len(data)-1, 2)]
        detail = [(data[i] - data[i+1]) / 2.0 for i in range(0, len(data)-1, 2)]
        return approx, detail
    
    # Single level decomposition
    approx1, detail1 = haar_transform(data1)
    approx2, detail2 = haar_transform(data2)
    
    # Compare detail coefficients
    if not detail1 or not detail2:
        return 1.0
    
    # Pad to same length
    max_len = max(len(detail1), len(detail2))
    detail1 += [0.0] * (max_len - len(detail1))
    detail2 += [0.0] * (max_len - len(detail2))
    
    # Euclidean distance of detail coefficients
    dist = math.sqrt(sum((d1 - d2)**2 for d1, d2 in zip(detail1, detail2)))
    max_dist = math.sqrt(sum(d**2 for d in detail1) + sum(d**2 for d in detail2))
    
    return 1.0 - (dist / max_dist) if max_dist > 0 else 1.0


def frequency_similarity(vec1, vec2):
    """Frequency domain analysis using FFT."""
    common_keys = sorted(set(vec1.keys()) & set(vec2.keys()))
    if not common_keys:
        return 0.0
    
    data1 = [vec1[k] for k in common_keys]
    data2 = [vec2[k] for k in common_keys]
    
    # Simple DFT (since we can't use numpy)
    def dft_magnitude(data):
        n = len(data)
        if n == 0:
            return []
        magnitudes = []
        for k in range(n // 2):  # Only positive frequencies
            real = sum(data[i] * math.cos(2 * math.pi * k * i / n) for i in range(n))
            imag = sum(data[i] * math.sin(2 * math.pi * k * i / n) for i in range(n))
            magnitudes.append(math.sqrt(real**2 + imag**2))
        return magnitudes
    
    mag1 = dft_magnitude(data1)
    mag2 = dft_magnitude(data2)
    
    if not mag1 or not mag2:
        return 1.0
    
    # Compare frequency spectra
    min_len = min(len(mag1), len(mag2))
    mag1 = mag1[:min_len]
    mag2 = mag2[:min_len]
    
    # Correlation of frequency magnitudes
    mean1 = sum(mag1) / len(mag1)
    mean2 = sum(mag2) / len(mag2)
    
    cov = sum((m1 - mean1) * (m2 - mean2) for m1, m2 in zip(mag1, mag2))
    var1 = sum((m1 - mean1)**2 for m1 in mag1)
    var2 = sum((m2 - mean2)**2 for m2 in mag2)
    
    if var1 == 0 or var2 == 0:
        return 1.0
    
    corr = cov / math.sqrt(var1 * var2)
    return (corr + 1.0) / 2.0  # Normalize to [0, 1]


# ============================================================================
# CORE HEX DICTIONARY
# ============================================================================

class HexDictionary:
    """
    Content-addressable storage with 8 advanced analysis methods.
    """
    
    METHODS = {
        'cosine': cosine_similarity,
        'euclidean': euclidean_similarity,
        'hamming': hamming_similarity,
        'spectral': spectral_similarity,
        'information': information_similarity,
        'topological': topological_similarity,
        'wavelet': wavelet_similarity,
        'frequency': frequency_similarity
    }
    
    def __init__(self, storage_dir="./hex_storage/", metadata_file="./hex_metadata.json"):
        """Initialize HexDictionary with storage directory."""
        self.storage_dir = storage_dir
        self.metadata_file = metadata_file
        self.metadata = {}
        
        os.makedirs(storage_dir, exist_ok=True)
        
        if os.path.exists(metadata_file):
            with open(metadata_file, 'r') as f:
                self.metadata = json.load(f)
    
    def _save_metadata(self):
        """Save metadata to disk."""
        with open(self.metadata_file, 'w') as f:
            json.dump(self.metadata, f, indent=2)
    
    def _compute_hash(self, data_bytes):
        """Compute SHA-256 hash of data."""
        return hashlib.sha256(data_bytes).hexdigest()
    
    def _serialize(self, data, data_type='json'):
        """Serialize data to bytes."""
        if data_type == 'json':
            return json.dumps(data, sort_keys=True).encode('utf-8')
        elif data_type == 'text':
            return data.encode('utf-8')
        elif data_type == 'bytes':
            return data
        else:
            raise ValueError(f"Unknown data_type: {data_type}")
    
    def _deserialize(self, data_bytes, data_type='json'):
        """Deserialize bytes to data."""
        if data_type == 'json':
            return json.loads(data_bytes.decode('utf-8'))
        elif data_type == 'text':
            return data_bytes.decode('utf-8')
        elif data_type == 'bytes':
            return data_bytes
        else:
            raise ValueError(f"Unknown data_type: {data_type}")
    
    def store(self, data, data_type='json', metadata=None):
        """Store data with coherence preservation."""
        data_bytes = self._serialize(data, data_type)
        content_hash = self._compute_hash(data_bytes)
        
        # Create coherence state
        hash_value = int(content_hash[:16], 16)
        state = CoherenceState(float(hash_value))
        
        # Store file
        file_path = os.path.join(self.storage_dir, content_hash + ".dat")
        with open(file_path, 'wb') as f:
            f.write(data_bytes)
        
        # Store metadata
        self.metadata[content_hash] = {
            'data_type': data_type,
            'size': len(data_bytes),
            'nrci': state.nrci,
            'user_metadata': metadata or {},
            'content_hash': content_hash
        }
        
        self._save_metadata()
        
        return content_hash
    
    def retrieve(self, content_hash):
        """Retrieve data by content hash."""
        if content_hash not in self.metadata:
            raise KeyError(f"Hash not found: {content_hash}")
        
        meta = self.metadata[content_hash]
        file_path = os.path.join(self.storage_dir, content_hash + ".dat")
        
        with open(file_path, 'rb') as f:
            data_bytes = f.read()
        
        return self._deserialize(data_bytes, meta['data_type'])
    
    def _extract_numerical_features(self, data):
        """Extract numerical features from data."""
        if isinstance(data, dict):
            features = {}
            for k, v in data.items():
                if isinstance(v, (int, float)):
                    features[k] = float(v)
            return features
        else:
            return {}
    
    def find_similar(self, query_data, method='cosine', top_k=10):
        """Find entries similar to query data using specified method."""
        if method not in self.METHODS:
            raise ValueError(f"Unknown method: {method}. Available: {list(self.METHODS.keys())}")
        
        query_features = self._extract_numerical_features(query_data)
        
        if not query_features:
            return []
        
        similarity_func = self.METHODS[method]
        similarities = []
        
        for content_hash in self.metadata.keys():
            try:
                stored_data = self.retrieve(content_hash)
                stored_features = self._extract_numerical_features(stored_data)
                
                sim = similarity_func(query_features, stored_features)
                similarities.append((content_hash, sim))
            except Exception:
                continue
        
        similarities.sort(key=lambda x: x[1], reverse=True)
        
        return similarities[:top_k]
    
    def predict_missing(self, partial_data, method='cosine', top_k=5):
        """Predict missing properties based on similar entries."""
        similar = self.find_similar(partial_data, method=method, top_k=top_k)
        
        if not similar:
            return {
                'predicted_data': partial_data.copy(),
                'confidence': 0.0,
                'sources': []
            }
        
        all_properties = defaultdict(list)
        
        for content_hash, similarity in similar:
            try:
                stored_data = self.retrieve(content_hash)
                features = self._extract_numerical_features(stored_data)
                
                for key, value in features.items():
                    all_properties[key].append((value, similarity))
            except Exception:
                continue
        
        predicted = partial_data.copy()
        
        for key, values in all_properties.items():
            if key not in predicted:
                total_weight = sum(sim for _, sim in values)
                if total_weight > 0:
                    weighted_sum = sum(val * sim for val, sim in values)
                    predicted[key] = weighted_sum / total_weight
        
        avg_similarity = sum(sim for _, sim in similar) / len(similar) if similar else 0.0
        
        return {
            'predicted_data': predicted,
            'confidence': avg_similarity,
            'sources': [h for h, _ in similar]
        }
    
    def compare(self, hash1, hash2, method='cosine'):
        """Compare two stored entries."""
        data1 = self.retrieve(hash1)
        data2 = self.retrieve(hash2)
        
        features1 = self._extract_numerical_features(data1)
        features2 = self._extract_numerical_features(data2)
        
        if method not in self.METHODS:
            raise ValueError(f"Unknown method: {method}")
        
        similarity_func = self.METHODS[method]
        sim = similarity_func(features1, features2)
        
        return {
            'similarity': sim,
            'method': method
        }
    
    def get_stats(self):
        """Get dictionary statistics."""
        if not self.metadata:
            return {
                'total_entries': 0,
                'avg_nrci': 0.0,
                'min_nrci': 0.0,
                'max_nrci': 0.0
            }
        
        nrcis = [meta['nrci'] for meta in self.metadata.values()]
        
        return {
            'total_entries': len(self.metadata),
            'avg_nrci': sum(nrcis) / len(nrcis),
            'min_nrci': min(nrcis),
            'max_nrci': max(nrcis)
        }
    
    def export_all(self, output_file):
        """Export all stored data to JSON file."""
        export_data = {}
        
        for content_hash in self.metadata.keys():
            try:
                data = self.retrieve(content_hash)
                export_data[content_hash] = {
                    'data': data,
                    'metadata': self.metadata[content_hash]
                }
            except Exception as e:
                export_data[content_hash] = {
                    'error': str(e)
                }
        
        with open(output_file, 'w') as f:
            json.dump(export_data, f, indent=2, default=str)


# ============================================================================
# DEMO
# ============================================================================

if __name__ == "__main__":
    print("=" * 80)
    print("UBP 3.5 HEX DICTIONARY v2.0 - COMPLETE")
    print("=" * 80)
    print("Content-Addressable Storage with 8 Analysis Methods")
    print()
    
    hd = HexDictionary()
    
    # Store test data
    print("Storing test elements...")
    elements = [
        {'Element': 'Hydrogen', 'Z': 1, 'mass': 1.008, 'radius': 53, 'ionization': 1312},
        {'Element': 'Helium', 'Z': 2, 'mass': 4.003, 'radius': 31, 'ionization': 2372},
        {'Element': 'Iron', 'Z': 26, 'mass': 55.845, 'radius': 156, 'ionization': 762},
        {'Element': 'Gold', 'Z': 79, 'mass': 196.967, 'radius': 174, 'ionization': 890},
    ]
    
    hashes = []
    for elem in elements:
        h = hd.store(elem, data_type='json')
        hashes.append(h)
        print(f"  {elem['Element']:10s}: {h[:16]}...")
    
    # Test all 8 methods
    print("\nComparing Fe vs Au with all 8 methods:")
    print(f"{'Method':<15s} {'Similarity':<12s}")
    print("-" * 30)
    
    for method in HexDictionary.METHODS.keys():
        result = hd.compare(hashes[2], hashes[3], method=method)
        print(f"{method:<15s} {result['similarity']:<12.6f}")
    
    print("\n" + "=" * 80)
    print("All 8 analysis methods working!")
    print("=" * 80)
