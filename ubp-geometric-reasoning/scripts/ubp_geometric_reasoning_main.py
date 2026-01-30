"""
================================================================================
UBP GEOMETRIC REASONING - MAIN INTERFACE v1.0
================================================================================

This module provides the primary interface for the UBP Geometric Rational
Reasoning skill. It exposes eight key capabilities that encapsulate the complete
UBP reasoning workflow.

Author: E. R. A. Craig / Manus AI
Date: January 30, 2026
Version: 1.0
================================================================================
"""

import hashlib
import json
from typing import Dict, List, Any, Optional, Tuple
from fractions import Fraction
from pathlib import Path

# Import UBP core modules
try:
    from ubp_core_v4_2_6_COMBINED import (
        GOLAY_DECODER,
        BinaryLinearAlgebra,
        UBPUltimateSubstrate,
        LeechPointScaled
    )
    from hex_dictionary_v4_exact import HEX_DB_EXACT
    from ubp_integrated_engine_v1 import SemanticCortexV3, UBPObserver
    from ubp_nrci_calculator import NRCI_CALCULATOR
    from ubp_rational_engine import RationalCortex
    CORE_AVAILABLE = True
except ImportError as e:
    print(f"[ERROR] Failed to import UBP core modules: {e}")
    CORE_AVAILABLE = False


class UBPGeometricReasoning:
    """
    Main interface for UBP Geometric Rational Reasoning.
    
    This class provides eight key capabilities:
    1. vectorize_concept - Convert concepts to 24-bit vectors
    2. reason_about - Execute full reasoning pipeline
    3. find_counterpart - Find geometric equivalents across domains
    4. calculate_coherence - Deep coherence analysis
    5. snap_to_lattice - Apply reflexive error correction
    6. query_memory - Retrieve relevant memories
    7. validate_concept - Run 5-phase research protocol
    8. archive_to_kb - Format and prepare for KB archival
    """
    
    def __init__(self, kb_path: Optional[str] = None):
        """
        Initialize the UBP Geometric Reasoning system.
        
        Args:
            kb_path: Optional path to external knowledge base
        """
        if not CORE_AVAILABLE:
            raise RuntimeError("UBP core modules not available")
        
        self.golay = GOLAY_DECODER
        self.leech = UBPUltimateSubstrate()
        self.db = HEX_DB_EXACT
        self.nrci_calc = NRCI_CALCULATOR
        
        # Load knowledge base
        if kb_path:
            self._load_external_kb(kb_path)
        elif not self.db.registry:
            print("[UBP] Loading default knowledge base...")
            try:
                self.db.load_memory()
            except Exception as e:
                print(f"[WARNING] Could not load KB: {e}")
        
        # Initialize cortex
        try:
            self.cortex = SemanticCortexV3()
            self.observer = self.cortex.observer
        except Exception as e:
            print(f"[WARNING] Cortex initialization failed: {e}")
            self.cortex = None
            self.observer = None
        
        print("[UBP] Geometric Reasoning System initialized")
    
    def _load_external_kb(self, kb_path: str):
        """Load an external knowledge base."""
        try:
            with open(kb_path, 'r') as f:
                kb_data = json.load(f)
            self.db.registry = kb_data
            print(f"[UBP] Loaded {len(kb_data)} entries from {kb_path}")
        except Exception as e:
            print(f"[ERROR] Failed to load KB from {kb_path}: {e}")
    
    # =========================================================================
    # CAPABILITY 1: VECTORIZE CONCEPT
    # =========================================================================
    
    def vectorize_concept(self, concept: str) -> Dict[str, Any]:
        """
        Perform complete vectorization protocol on a concept.
        
        Args:
            concept: The concept to vectorize (string)
        
        Returns:
            Dictionary containing:
            - vector: 24-bit vector representation
            - fingerprint: SHA-256 hash
            - domain: Octad domain classification
            - nrci: Non-Random Coherence Index
            - hamming_weight: Number of 1-bits
        """
        # Step 1: Generate SHA-256 hash
        hash_bytes = hashlib.sha256(concept.lower().encode('utf-8')).digest()
        
        # Step 2: Extract first 24 bits
        val = int.from_bytes(hash_bytes[:3], 'big') % 4096
        raw_vector = [(val >> i) & 1 for i in range(23, -1, -1)]
        
        # Step 3: Golay decode and encode
        corrected, syndrome, errors = self.golay.decode(raw_vector)
        vector = self.golay.encode(corrected)
        
        # Step 4: Generate fingerprint
        fingerprint = hashlib.sha256(concept.encode('utf-8')).hexdigest()
        
        # Step 5: Determine domain (Octad classification)
        bit_12 = vector[11]
        domain = "SUBSTANCE" if bit_12 == 1 else "QUANTITY"
        
        # Step 6: Calculate NRCI
        try:
            nrci_result = self.nrci_calc.calculate_nrci(vector)
            nrci = nrci_result.global_nrci
        except:
            nrci = 0.0
        
        # Step 7: Calculate Hamming weight
        hamming_weight = sum(vector)
        
        return {
            "concept": concept,
            "vector": vector,
            "fingerprint": fingerprint,
            "domain": domain,
            "nrci": float(nrci),
            "hamming_weight": hamming_weight,
            "errors_corrected": errors
        }
    
    # =========================================================================
    # CAPABILITY 2: REASON ABOUT
    # =========================================================================
    
    def reason_about(self, query: str) -> Dict[str, Any]:
        """
        Execute the full reasoning pipeline on a query.
        
        Args:
            query: Natural language query
        
        Returns:
            Dictionary containing:
            - status: ACCEPTED or REJECTED
            - vector: 24-bit representation
            - resonance: Nearest anchor and distance
            - coherence: NRCI and health metrics
            - energy_cost: Metabolic cost of operation
        """
        if not self.cortex:
            return {"status": "ERROR", "message": "Cortex not initialized"}
        
        # Execute the cortex processing
        result = self.cortex.process_query(query)
        
        return result
    
    # =========================================================================
    # CAPABILITY 3: FIND COUNTERPART
    # =========================================================================
    
    def find_counterpart(self, concept: str, target_domain: str) -> Dict[str, Any]:
        """
        Find the geometric equivalent of a concept in a different domain.
        
        Args:
            concept: The source concept
            target_domain: Target domain from the Octad
        
        Returns:
            Dictionary containing the counterpart concept information
        """
        # Vectorize the source concept
        source_vec_data = self.vectorize_concept(concept)
        source_vector = source_vec_data["vector"]
        
        # Search for nearest concept in target domain
        min_distance = 25
        counterpart = None
        
        for fp, entry in self.db.registry.items():
            # Check if entry is in target domain
            entry_tags = entry.get('tags', [])
            entry_name = str(entry.get('name', '')).lower()
            
            # Simple domain matching (can be refined)
            if target_domain.lower() in ' '.join(entry_tags).lower() or \
               target_domain.lower() in entry_name:
                
                entry_vector = entry.get('vector')
                if entry_vector and len(entry_vector) == 24:
                    distance = BinaryLinearAlgebra.hamming_distance(
                        source_vector, entry_vector
                    )
                    
                    if distance < min_distance:
                        min_distance = distance
                        counterpart = entry
        
        if counterpart:
            return {
                "source_concept": concept,
                "target_domain": target_domain,
                "counterpart": counterpart.get('name'),
                "counterpart_id": counterpart.get('ubp_id'),
                "hamming_distance": min_distance,
                "counterpart_vector": counterpart.get('vector'),
                "status": "FOUND"
            }
        else:
            return {
                "source_concept": concept,
                "target_domain": target_domain,
                "status": "NOT_FOUND",
                "message": f"No counterpart found in {target_domain}"
            }
    
    # =========================================================================
    # CAPABILITY 4: CALCULATE COHERENCE
    # =========================================================================
    
    def calculate_coherence(self, vector: List[int]) -> Dict[str, Any]:
        """
        Perform deep coherence analysis on a vector.
        
        Args:
            vector: 24-bit vector
        
        Returns:
            Dictionary containing:
            - nrci: Non-Random Coherence Index
            - health: Tetradic health metrics
            - regime: Coherence regime (high/medium/low)
            - stability: Stability score
            - symmetry_tax: Energetic cost
        """
        if len(vector) != 24:
            return {"status": "ERROR", "message": "Vector must be 24 bits"}
        
        # Calculate NRCI
        nrci_result = self.nrci_calc.calculate_nrci(vector)
        
        return {
            "nrci": float(nrci_result.global_nrci),
            "health": {
                "reality": float(nrci_result.reality_health),
                "info": float(nrci_result.info_health),
                "activation": float(nrci_result.activation_health),
                "potential": float(nrci_result.potential_health)
            },
            "regime": nrci_result.coherence_regime,
            "stability": float(nrci_result.stability_score),
            "symmetry_tax": float(nrci_result.symmetry_tax)
        }
    
    # =========================================================================
    # CAPABILITY 5: SNAP TO LATTICE
    # =========================================================================
    
    def snap_to_lattice(self, noisy_vector: List[int]) -> Dict[str, Any]:
        """
        Apply reflexive error correction to a noisy vector.
        
        Args:
            noisy_vector: 24-bit vector (potentially noisy)
        
        Returns:
            Dictionary containing:
            - corrected_vector: Snapped vector
            - errors_fixed: Number of bit-flips corrected
            - anchor_distance: Distance to nearest anchor
            - status: CORRECTED or DEEP_HOLE
        """
        if len(noisy_vector) != 24:
            return {"status": "ERROR", "message": "Vector must be 24 bits"}
        
        # Apply Golay decode/encode (Reflexive Logic)
        corrected, syndrome, errors = self.golay.decode(noisy_vector)
        corrected_vector = self.golay.encode(corrected)
        
        # Determine status
        if errors > 3:
            status = "DEEP_HOLE"
        elif errors > 0:
            status = "CORRECTED"
        else:
            status = "PERFECT"
        
        # Find nearest anchor
        min_distance = 25
        nearest_anchor = "UNKNOWN"
        
        for fp, entry in self.db.registry.items():
            entry_vector = entry.get('vector')
            if entry_vector and len(entry_vector) == 24:
                distance = BinaryLinearAlgebra.hamming_distance(
                    corrected_vector, entry_vector
                )
                if distance < min_distance:
                    min_distance = distance
                    nearest_anchor = entry.get('name', entry.get('ubp_id', 'UNKNOWN'))
        
        return {
            "original_vector": noisy_vector,
            "corrected_vector": corrected_vector,
            "errors_fixed": errors,
            "anchor_distance": min_distance,
            "nearest_anchor": nearest_anchor,
            "status": status
        }
    
    # =========================================================================
    # CAPABILITY 6: QUERY MEMORY
    # =========================================================================
    
    def query_memory(self, search_term: str, max_results: int = 12) -> List[Dict[str, Any]]:
        """
        Retrieve a cluster of relevant memories from the knowledge base.
        
        Args:
            search_term: Keyword or concept to search for
            max_results: Maximum number of results to return
        
        Returns:
            List of memory dictionaries with Hamming distances
        """
        # Vectorize search term
        search_vec_data = self.vectorize_concept(search_term)
        search_vector = search_vec_data["vector"]
        search_fp = search_vec_data["fingerprint"]
        
        # Find seed (exact match or closest)
        seed_entry = None
        if search_fp in self.db.registry:
            seed_entry = self.db.registry[search_fp]
        
        # Collect candidates with Hamming distances
        candidates = []
        for fp, entry in self.db.registry.items():
            entry_vector = entry.get('vector')
            if entry_vector and len(entry_vector) == 24:
                distance = BinaryLinearAlgebra.hamming_distance(
                    search_vector, entry_vector
                )
                
                # Also check keyword match
                entry_str = (
                    str(entry.get('name', '')) + " " + 
                    " ".join(entry.get('tags', []))
                ).lower()
                keyword_match = search_term.lower() in entry_str
                
                candidates.append({
                    "entry": entry,
                    "distance": distance,
                    "keyword_match": keyword_match
                })
        
        # Sort by distance, prioritize keyword matches
        candidates.sort(key=lambda x: (not x["keyword_match"], x["distance"]))
        
        # Return top results
        results = []
        for candidate in candidates[:max_results]:
            entry = candidate["entry"]
            results.append({
                "ubp_id": entry.get('ubp_id'),
                "name": entry.get('name'),
                "math": entry.get('math'),
                "language": entry.get('language'),
                "tags": entry.get('tags'),
                "nrci": entry.get('nrci'),
                "hamming_distance": candidate["distance"],
                "keyword_match": candidate["keyword_match"]
            })
        
        return results
    
    # =========================================================================
    # CAPABILITY 7: VALIDATE CONCEPT
    # =========================================================================
    
    def validate_concept(self, concept_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Run a concept through the 5-phase research protocol.
        
        Args:
            concept_data: Dictionary with 'name', 'math', 'language', 'script', 'tags'
        
        Returns:
            Dictionary containing:
            - validation_result: Pass/Fail for each phase
            - nrci: Final NRCI score
            - promotion_eligible: Boolean
        """
        results = {
            "phase_1_initiation": "PENDING",
            "phase_2_development": "PENDING",
            "phase_3_distillation": "PENDING",
            "phase_4_promotion": "PENDING",
            "phase_5_archival": "PENDING",
            "promotion_eligible": False
        }
        
        # PHASE 1: INITIATION
        if 'name' in concept_data and 'math' in concept_data:
            results["phase_1_initiation"] = "PASS"
        else:
            results["phase_1_initiation"] = "FAIL"
            return results
        
        # PHASE 2: DEVELOPMENT (Check for script)
        if 'script' in concept_data:
            results["phase_2_development"] = "PASS"
        else:
            results["phase_2_development"] = "FAIL"
            return results
        
        # PHASE 3: DISTILLATION (Calculate NRCI)
        concept_name = concept_data.get('name', '')
        vec_data = self.vectorize_concept(concept_name)
        vector = vec_data["vector"]
        
        coherence = self.calculate_coherence(vector)
        nrci = coherence["nrci"]
        
        results["nrci"] = nrci
        results["coherence_regime"] = coherence["regime"]
        
        if nrci >= 0.50:
            results["phase_3_distillation"] = "PASS (Coherent)"
        elif nrci >= 0.10:
            results["phase_3_distillation"] = "PASS (Subcoherent)"
        else:
            results["phase_3_distillation"] = "FAIL (Too Noisy)"
            return results
        
        # PHASE 4: PROMOTION (Check stability)
        stability = coherence["stability"]
        if stability >= 0.5:
            results["phase_4_promotion"] = "PASS"
            results["promotion_eligible"] = True
        else:
            results["phase_4_promotion"] = "FAIL (Unstable)"
            return results
        
        # PHASE 5: ARCHIVAL (Ready for KB)
        results["phase_5_archival"] = "READY"
        
        return results
    
    # =========================================================================
    # CAPABILITY 8: ARCHIVE TO KB
    # =========================================================================
    
    def archive_to_kb(self, concept_data: Dict[str, Any]) -> str:
        """
        Format a validated concept for knowledge base archival.
        
        Args:
            concept_data: Dictionary with 'name', 'math', 'language', 'script', 'tags'
        
        Returns:
            Formatted JSON string ready for KB insertion
        """
        # Generate triadic hash (fingerprint)
        math = concept_data.get('math', '0')
        language = concept_data.get('language', 'None')
        script = concept_data.get('script', 'None')
        
        raw = f"{math}|{language}|{script}"
        fingerprint = hashlib.sha256(raw.encode('utf-8')).hexdigest()
        
        # Vectorize
        vec_data = self.vectorize_concept(concept_data.get('name', ''))
        vector = vec_data["vector"]
        
        # Calculate NRCI
        coherence = self.calculate_coherence(vector)
        nrci = coherence["nrci"]
        
        # Format as fraction string
        nrci_fraction = f"{int(nrci * 100)}/100"
        
        # Generate UBP_ID (user should customize)
        ubp_id = concept_data.get('ubp_id', 'CUSTOM_001')
        
        # Build KB entry
        kb_entry = {
            fingerprint: {
                "ubp_id": ubp_id,
                "name": concept_data.get('name'),
                "math": math,
                "language": language,
                "script": script,
                "tags": concept_data.get('tags', []),
                "nrci": nrci_fraction,
                "fingerprint": fingerprint,
                "vector": vector
            }
        }
        
        return json.dumps(kb_entry, indent=2)


# =============================================================================
# MODULE-LEVEL INTERFACE
# =============================================================================

# Global instance (lazy initialization)
_ubp_reasoning = None

def get_reasoning_engine(kb_path: Optional[str] = None) -> UBPGeometricReasoning:
    """Get or create the global UBP reasoning engine."""
    global _ubp_reasoning
    if _ubp_reasoning is None:
        _ubp_reasoning = UBPGeometricReasoning(kb_path=kb_path)
    return _ubp_reasoning


# Convenience functions for direct access
def vectorize_concept(concept: str) -> Dict[str, Any]:
    """Vectorize a concept."""
    return get_reasoning_engine().vectorize_concept(concept)

def reason_about(query: str) -> Dict[str, Any]:
    """Reason about a query."""
    return get_reasoning_engine().reason_about(query)

def find_counterpart(concept: str, target_domain: str) -> Dict[str, Any]:
    """Find counterpart in different domain."""
    return get_reasoning_engine().find_counterpart(concept, target_domain)

def calculate_coherence(vector: List[int]) -> Dict[str, Any]:
    """Calculate coherence of a vector."""
    return get_reasoning_engine().calculate_coherence(vector)

def snap_to_lattice(noisy_vector: List[int]) -> Dict[str, Any]:
    """Snap noisy vector to lattice."""
    return get_reasoning_engine().snap_to_lattice(noisy_vector)

def query_memory(search_term: str, max_results: int = 12) -> List[Dict[str, Any]]:
    """Query the knowledge base."""
    return get_reasoning_engine().query_memory(search_term, max_results)

def validate_concept(concept_data: Dict[str, Any]) -> Dict[str, Any]:
    """Validate a concept."""
    return get_reasoning_engine().validate_concept(concept_data)

def archive_to_kb(concept_data: Dict[str, Any]) -> str:
    """Archive concept to KB."""
    return get_reasoning_engine().archive_to_kb(concept_data)


# =============================================================================
# MAIN EXECUTION (FOR TESTING)
# =============================================================================

if __name__ == "__main__":
    print("\n" + "=" * 80)
    print("UBP GEOMETRIC REASONING - MAIN INTERFACE TEST")
    print("=" * 80)
    
    # Initialize
    ubp = UBPGeometricReasoning()
    
    # Test 1: Vectorize Concept
    print("\n[TEST 1] Vectorize Concept: 'Energy'")
    result = ubp.vectorize_concept("Energy")
    print(f"  Vector: {result['vector'][:8]}... (truncated)")
    print(f"  Domain: {result['domain']}")
    print(f"  NRCI: {result['nrci']:.4f}")
    
    # Test 2: Calculate Coherence
    print("\n[TEST 2] Calculate Coherence")
    coherence = ubp.calculate_coherence(result['vector'])
    print(f"  Regime: {coherence['regime']}")
    print(f"  Stability: {coherence['stability']:.4f}")
    
    # Test 3: Snap to Lattice
    print("\n[TEST 3] Snap Noisy Vector to Lattice")
    noisy = result['vector'].copy()
    noisy[0] = 1 - noisy[0]  # Flip one bit
    snap_result = ubp.snap_to_lattice(noisy)
    print(f"  Errors Fixed: {snap_result['errors_fixed']}")
    print(f"  Status: {snap_result['status']}")
    
    print("\n" + "=" * 80)
    print("✓ UBP GEOMETRIC REASONING INTERFACE READY")
    print("=" * 80)
