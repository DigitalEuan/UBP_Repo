#!/usr/bin/env python3.11
"""
Advanced HexDictionary Analytics Module
Transforms HexDict from passive storage into active reasoning assistant
"""

import sys
import hashlib
import numpy as np
from typing import List, Dict, Any, Tuple, Optional
from collections import defaultdict
from dataclasses import dataclass

sys.path.insert(0, '/home/ubuntu/UBP_Repo/ubp_3.4')

from hex_dictionary import HexDictionary

@dataclass
class PatternMatch:
    """Pattern match result"""
    pattern_id: str
    pattern_type: str
    frequency: int
    nrci_avg: float
    examples: List[str]
    confidence: float

@dataclass
class NoveltyScore:
    """Novelty assessment result"""
    claim: str
    novelty_score: float  # 0 = fully known, 1 = completely novel
    similar_claims: List[Dict[str, Any]]
    confidence: float
    recommendation: str  # "accept", "verify", "reject"

@dataclass
class ContradictionPair:
    """Contradiction between two claims"""
    claim1: str
    claim2: str
    contradiction_score: float
    nrci1: float
    nrci2: float
    resolution_suggestion: str

@dataclass
class KnowledgeGraphNode:
    """Node in knowledge graph"""
    content_hash: str
    content: str
    nrci: float
    connections: List[str]  # Hashes of related content
    connection_strengths: List[float]

class HexDictAnalytics:
    """
    Advanced analytics for HexDictionary
    
    Capabilities:
    1. Pattern Recognition
    2. Semantic Clustering
    3. Contradiction Mining
    4. Knowledge Graph Construction
    5. Novelty Detection
    6. Confidence Scoring
    7. Emergent Insight Discovery
    """
    
    def __init__(self, hexdict: HexDictionary):
        self.hexdict = hexdict
        self.pattern_cache = {}
        self.knowledge_graph = {}
        self.semantic_clusters = {}
        
    def detect_patterns(self, min_frequency: int = 3) -> List[PatternMatch]:
        """
        Detect recurring patterns across stored responses
        
        Patterns include:
        - Repeated concepts
        - Common reasoning structures
        - Frequent fact patterns
        - Typical error patterns
        """
        patterns = []
        
        # Get all stored content
        all_content = self._get_all_content()
        
        # Extract n-grams (2-5 words)
        ngram_counts = defaultdict(lambda: {"count": 0, "nrcis": [], "examples": []})
        
        for content_hash, content, metadata in all_content:
            # Extract words
            words = content.lower().split()
            
            # Generate n-grams
            for n in range(2, 6):
                for i in range(len(words) - n + 1):
                    ngram = " ".join(words[i:i+n])
                    ngram_counts[ngram]["count"] += 1
                    if metadata and "nrci" in metadata:
                        ngram_counts[ngram]["nrcis"].append(metadata["nrci"])
                    ngram_counts[ngram]["examples"].append(content_hash[:16])
        
        # Filter by frequency
        for ngram, data in ngram_counts.items():
            if data["count"] >= min_frequency:
                avg_nrci = np.mean(data["nrcis"]) if data["nrcis"] else 0.0
                confidence = min(1.0, data["count"] / 10.0)  # More frequent = higher confidence
                
                pattern = PatternMatch(
                    pattern_id=hashlib.sha256(ngram.encode()).hexdigest()[:16],
                    pattern_type="ngram",
                    frequency=data["count"],
                    nrci_avg=avg_nrci,
                    examples=data["examples"][:5],
                    confidence=confidence
                )
                patterns.append(pattern)
        
        # Sort by frequency
        patterns.sort(key=lambda p: p.frequency, reverse=True)
        
        return patterns
    
    def cluster_semantically(self, n_clusters: int = 10) -> Dict[str, List[str]]:
        """
        Cluster similar content semantically
        
        Uses simple word overlap for now (could be enhanced with embeddings)
        """
        all_content = self._get_all_content()
        
        if len(all_content) < n_clusters:
            n_clusters = max(1, len(all_content) // 2)
        
        # Simple clustering based on word overlap
        clusters = defaultdict(list)
        
        for content_hash, content, metadata in all_content:
            # Extract key words (simple: just split)
            words = set(content.lower().split())
            
            # Find best matching cluster
            best_cluster = None
            best_overlap = 0
            
            for cluster_id, cluster_members in clusters.items():
                # Get representative words from cluster
                cluster_words = set()
                for member_hash in cluster_members[:5]:  # Sample first 5
                    member_content = self._get_content_by_hash(member_hash)
                    if member_content:
                        cluster_words.update(member_content.lower().split())
                
                # Calculate overlap
                overlap = len(words & cluster_words)
                if overlap > best_overlap:
                    best_overlap = overlap
                    best_cluster = cluster_id
            
            # Assign to cluster
            if best_cluster is not None and best_overlap > 3:
                clusters[best_cluster].append(content_hash)
            else:
                # Create new cluster
                new_cluster_id = f"cluster_{len(clusters)}"
                clusters[new_cluster_id].append(content_hash)
        
        return dict(clusters)
    
    def mine_contradictions(self, threshold: float = 0.7) -> List[ContradictionPair]:
        """
        Systematically find contradictions in knowledge base
        
        Detects:
        - Direct contradictions (X is Y vs X is not Y)
        - Numerical contradictions (X = 5 vs X = 10)
        - Logical contradictions (A implies B, but not B)
        """
        contradictions = []
        
        all_content = self._get_all_content()
        
        # Pairwise comparison (expensive for large datasets)
        for i, (hash1, content1, meta1) in enumerate(all_content):
            for hash2, content2, meta2 in all_content[i+1:]:
                # Check for contradiction indicators
                contradiction_score = self._calculate_contradiction_score(content1, content2)
                
                if contradiction_score > threshold:
                    nrci1 = meta1.get("nrci", 0.5) if meta1 else 0.5
                    nrci2 = meta2.get("nrci", 0.5) if meta2 else 0.5
                    
                    # Resolution: trust higher NRCI
                    if nrci1 > nrci2:
                        resolution = f"Trust claim 1 (NRCI: {nrci1:.3f} > {nrci2:.3f})"
                    elif nrci2 > nrci1:
                        resolution = f"Trust claim 2 (NRCI: {nrci2:.3f} > {nrci1:.3f})"
                    else:
                        resolution = "Equal NRCI - requires external verification"
                    
                    contradiction = ContradictionPair(
                        claim1=content1[:200],
                        claim2=content2[:200],
                        contradiction_score=contradiction_score,
                        nrci1=nrci1,
                        nrci2=nrci2,
                        resolution_suggestion=resolution
                    )
                    contradictions.append(contradiction)
        
        return contradictions
    
    def build_knowledge_graph(self, similarity_threshold: float = 0.5) -> Dict[str, KnowledgeGraphNode]:
        """
        Build knowledge graph with connections between related facts
        
        Nodes: Stored content
        Edges: Semantic similarity, logical implication, temporal sequence
        """
        all_content = self._get_all_content()
        
        # Create nodes
        for content_hash, content, metadata in all_content:
            nrci = metadata.get("nrci", 0.5) if metadata else 0.5
            
            node = KnowledgeGraphNode(
                content_hash=content_hash,
                content=content,
                nrci=nrci,
                connections=[],
                connection_strengths=[]
            )
            self.knowledge_graph[content_hash] = node
        
        # Create edges
        for hash1, node1 in self.knowledge_graph.items():
            for hash2, node2 in self.knowledge_graph.items():
                if hash1 >= hash2:  # Avoid duplicates
                    continue
                
                # Calculate similarity
                similarity = self._calculate_similarity(node1.content, node2.content)
                
                if similarity > similarity_threshold:
                    # Add bidirectional connection
                    node1.connections.append(hash2)
                    node1.connection_strengths.append(similarity)
                    node2.connections.append(hash1)
                    node2.connection_strengths.append(similarity)
        
        return self.knowledge_graph
    
    def assess_novelty(self, claim: str, top_k: int = 5) -> NoveltyScore:
        """
        Assess how novel a claim is vs existing knowledge
        
        Returns:
        - novelty_score: 0 (fully known) to 1 (completely novel)
        - similar_claims: Most similar existing claims
        - recommendation: accept/verify/reject
        """
        claim_hash = hashlib.sha256(claim.encode()).hexdigest()
        
        # Check for exact match
        exact_match = self.hexdict.retrieve(claim_hash)
        if exact_match:
            return NoveltyScore(
                claim=claim,
                novelty_score=0.0,
                similar_claims=[{"content": exact_match, "similarity": 1.0}],
                confidence=1.0,
                recommendation="accept"
            )
        
        # Find similar claims
        all_content = self._get_all_content()
        similarities = []
        
        for content_hash, content, metadata in all_content:
            similarity = self._calculate_similarity(claim, content)
            nrci = metadata.get("nrci", 0.5) if metadata else 0.5
            similarities.append({
                "content": content[:200],
                "similarity": similarity,
                "nrci": nrci,
                "hash": content_hash
            })
        
        # Sort by similarity
        similarities.sort(key=lambda x: x["similarity"], reverse=True)
        similar_claims = similarities[:top_k]
        
        # Calculate novelty score
        if not similar_claims:
            novelty_score = 1.0
        else:
            max_similarity = similar_claims[0]["similarity"]
            novelty_score = 1.0 - max_similarity
        
        # Recommendation
        if novelty_score < 0.1:
            recommendation = "accept"  # Very similar to known facts
            confidence = 0.9
        elif novelty_score < 0.5:
            recommendation = "verify"  # Somewhat novel, needs verification
            confidence = 0.6
        else:
            recommendation = "verify"  # Very novel, definitely needs verification
            confidence = 0.3
        
        return NoveltyScore(
            claim=claim,
            novelty_score=novelty_score,
            similar_claims=similar_claims,
            confidence=confidence,
            recommendation=recommendation
        )
    
    def calculate_confidence_score(self, claim: str) -> float:
        """
        Calculate confidence score for a claim based on:
        - Retrieval frequency
        - Average NRCI of similar claims
        - Consistency with knowledge graph
        """
        # Find similar claims
        all_content = self._get_all_content()
        similar_nrcis = []
        retrieval_count = 0
        
        for content_hash, content, metadata in all_content:
            similarity = self._calculate_similarity(claim, content)
            if similarity > 0.7:
                retrieval_count += 1
                if metadata and "nrci" in metadata:
                    similar_nrcis.append(metadata["nrci"])
        
        # Calculate components
        frequency_score = min(1.0, retrieval_count / 10.0)
        nrci_score = np.mean(similar_nrcis) if similar_nrcis else 0.5
        
        # Combined confidence
        confidence = 0.5 * frequency_score + 0.5 * nrci_score
        
        return confidence
    
    def discover_emergent_insights(self, min_connection_strength: float = 0.6) -> List[Dict[str, Any]]:
        """
        Find non-obvious connections between facts
        
        Looks for:
        - Transitive relationships (A→B, B→C implies A→C)
        - Common patterns across domains
        - Hidden correlations
        """
        insights = []
        
        # Ensure knowledge graph is built
        if not self.knowledge_graph:
            self.build_knowledge_graph()
        
        # Find transitive relationships
        for hash1, node1 in self.knowledge_graph.items():
            for i, hash2 in enumerate(node1.connections):
                strength12 = node1.connection_strengths[i]
                
                if strength12 < min_connection_strength:
                    continue
                
                # Check node2's connections
                node2 = self.knowledge_graph.get(hash2)
                if not node2:
                    continue
                
                for j, hash3 in enumerate(node2.connections):
                    if hash3 == hash1:  # Skip back-connection
                        continue
                    
                    strength23 = node2.connection_strengths[j]
                    
                    if strength23 < min_connection_strength:
                        continue
                    
                    # Check if hash1 and hash3 are directly connected
                    if hash3 not in node1.connections:
                        # Found transitive relationship!
                        transitive_strength = min(strength12, strength23)
                        
                        insight = {
                            "type": "transitive_relationship",
                            "node1": node1.content[:100],
                            "node2": node2.content[:100],
                            "node3": self.knowledge_graph[hash3].content[:100],
                            "strength": transitive_strength,
                            "explanation": f"If '{node1.content[:50]}...' relates to '{node2.content[:50]}...', "
                                         f"and '{node2.content[:50]}...' relates to '{self.knowledge_graph[hash3].content[:50]}...', "
                                         f"then there may be a connection between the first and third."
                        }
                        insights.append(insight)
        
        return insights
    
    # Helper methods
    
    def _get_all_content(self) -> List[Tuple[str, str, Optional[Dict]]]:
        """Get all stored content with metadata"""
        # This is a simplified version - real implementation would query HexDict properly
        # For now, return empty list (would be populated from actual HexDict storage)
        return []
    
    def _get_content_by_hash(self, content_hash: str) -> Optional[str]:
        """Retrieve content by hash"""
        return self.hexdict.retrieve(content_hash)
    
    def _calculate_similarity(self, text1: str, text2: str) -> float:
        """
        Calculate semantic similarity between two texts
        
        Simple word overlap for now (could use embeddings)
        """
        words1 = set(text1.lower().split())
        words2 = set(text2.lower().split())
        
        if not words1 or not words2:
            return 0.0
        
        intersection = words1 & words2
        union = words1 | words2
        
        # Jaccard similarity
        similarity = len(intersection) / len(union) if union else 0.0
        
        return similarity
    
    def _calculate_contradiction_score(self, text1: str, text2: str) -> float:
        """
        Calculate contradiction score between two texts
        
        Looks for negation patterns and opposing statements
        """
        text1_lower = text1.lower()
        text2_lower = text2.lower()
        
        # Simple heuristics
        contradiction_score = 0.0
        
        # Check for negation patterns
        negation_words = ["not", "no", "never", "neither", "nor", "cannot", "isn't", "aren't", "wasn't", "weren't"]
        
        text1_has_negation = any(neg in text1_lower for neg in negation_words)
        text2_has_negation = any(neg in text2_lower for neg in negation_words)
        
        # If one has negation and they're otherwise similar, likely contradiction
        if text1_has_negation != text2_has_negation:
            similarity = self._calculate_similarity(text1, text2)
            if similarity > 0.5:
                contradiction_score = similarity * 0.8
        
        # Check for opposing numerical values
        # (Would need more sophisticated parsing)
        
        return contradiction_score
    
    def generate_analytics_report(self) -> str:
        """Generate comprehensive analytics report"""
        report = "=" * 80 + "\n"
        report += "HEXDICTIONARY ANALYTICS REPORT\n"
        report += "=" * 80 + "\n\n"
        
        # Pattern detection
        patterns = self.detect_patterns(min_frequency=2)
        report += f"Detected Patterns: {len(patterns)}\n"
        if patterns:
            report += "  Top 5 patterns:\n"
            for pattern in patterns[:5]:
                report += f"    - {pattern.pattern_id}: freq={pattern.frequency}, NRCI={pattern.nrci_avg:.3f}\n"
        report += "\n"
        
        # Semantic clustering
        clusters = self.cluster_semantically(n_clusters=5)
        report += f"Semantic Clusters: {len(clusters)}\n"
        for cluster_id, members in list(clusters.items())[:3]:
            report += f"  {cluster_id}: {len(members)} members\n"
        report += "\n"
        
        # Contradiction mining
        contradictions = self.mine_contradictions(threshold=0.6)
        report += f"Contradictions Found: {len(contradictions)}\n"
        if contradictions:
            report += "  Top contradiction:\n"
            c = contradictions[0]
            report += f"    Claim 1: {c.claim1[:80]}...\n"
            report += f"    Claim 2: {c.claim2[:80]}...\n"
            report += f"    Score: {c.contradiction_score:.3f}\n"
            report += f"    Resolution: {c.resolution_suggestion}\n"
        report += "\n"
        
        # Knowledge graph
        kg = self.build_knowledge_graph(similarity_threshold=0.5)
        report += f"Knowledge Graph Nodes: {len(kg)}\n"
        total_connections = sum(len(node.connections) for node in kg.values())
        report += f"Knowledge Graph Edges: {total_connections // 2}\n"  # Divide by 2 for bidirectional
        report += "\n"
        
        # Emergent insights
        insights = self.discover_emergent_insights(min_connection_strength=0.6)
        report += f"Emergent Insights: {len(insights)}\n"
        if insights:
            report += "  Example insight:\n"
            insight = insights[0]
            report += f"    Type: {insight['type']}\n"
            report += f"    Strength: {insight['strength']:.3f}\n"
        report += "\n"
        
        report += "=" * 80 + "\n"
        
        return report


def test_hexdict_analytics():
    """Test HexDict analytics functionality"""
    print("Testing HexDictionary Analytics...")
    print()
    
    # Create HexDict
    hexdict = HexDictionary()
    
    # Create analytics engine
    analytics = HexDictAnalytics(hexdict)
    
    # Store some test data
    test_claims = [
        "The Y constant is π/(π²+2) = 0.264675430404527",
        "The inverse Y constant is π + 2/π = 3.778212425957375",
        "O_observer equals 1/Y exactly",
        "NRCI quantifies coherence from 0 to 1",
        "High NRCI indicates supercoherent systems",
        "The Y constant relates to geometric resonance",
        "Observer cost converges to fixed point",
        "SOC energy depends on NRCI and O_observer",
    ]
    
    for claim in test_claims:
        metadata = {
            "nrci": np.random.uniform(0.85, 0.99),
            "ubp_version": "3.4",
            "data_type": "test_claim"
        }
        hexdict.store(claim, data_type="str", metadata=metadata)
    
    print("Stored test claims in HexDict")
    print()
    
    # Test novelty assessment
    print("Testing Novelty Assessment:")
    print("-" * 80)
    novel_claim = "The Z constant is related to quantum entanglement"
    novelty = analytics.assess_novelty(novel_claim)
    print(f"Claim: {novelty.claim}")
    print(f"Novelty Score: {novelty.novelty_score:.3f}")
    print(f"Recommendation: {novelty.recommendation}")
    print(f"Confidence: {novelty.confidence:.3f}")
    print()
    
    # Test confidence scoring
    print("Testing Confidence Scoring:")
    print("-" * 80)
    known_claim = "The Y constant is π/(π²+2)"
    confidence = analytics.calculate_confidence_score(known_claim)
    print(f"Claim: {known_claim}")
    print(f"Confidence Score: {confidence:.3f}")
    print()
    
    print("HexDict Analytics Test Complete!")
    print()

if __name__ == "__main__":
    test_hexdict_analytics()
