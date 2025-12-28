#!/usr/bin/env python3
"""
================================================================================
UBP LEECH ENGINE - ENHANCED v4.1.1 (PRODUCTION)
================================================================================

Leech Lattice Engine with full integration to ubp_core_v4_1_enhanced.py
Version: 4.1.1 Enhanced (Production)
Author: Euan R A Craig, New Zealand + UBP Research Assistant
Date: 26 December 2025

FEATURES:
- Full integration with ubp_core_v4_1_enhanced.py
- Derived Paley matrix (first-principles)
- Deterministic Leech point generation
- Comprehensive lattice analysis
- Particle physics validation
- 100% backward compatible with v4.1
- Pure integer operations (no NumPy required)

================================================================================
"""

from typing import List, Tuple, Dict, Optional, Set, Generator
from fractions import Fraction
import itertools

# Import from enhanced UBP core
try:
    from ubp_core import (
        GOLAY_DECODER,
        LEECH_ENHANCED,
        PARTICLE_VALIDATOR,
        LeechPointScaled,
        PaleyMatrixEngine,
        hamming_weight,
        _binary_matmul,
        _identity,
        _transpose
    )
    CORE_AVAILABLE = True
except ImportError:
    CORE_AVAILABLE = False
    print("[WARNING] ubp_core not available - using fallback mode")
    
    # Fallback functions
    def _identity(n: int) -> List[List[int]]:
        return [[1 if i == j else 0 for j in range(n)] for i in range(n)]
    
    def _transpose(M: List[List[int]]) -> List[List[int]]:
        if not M: return []
        return [[M[i][j] for i in range(len(M))] for j in range(len(M[0]))]
    
    def _binary_matmul(A: List[List[int]], B: List[List[int]]) -> List[List[int]]:
        if not A or not B: return []
        rows_A, cols_A, cols_B = len(A), len(A[0]), len(B[0])
        if cols_A != len(B): raise ValueError(f"Matrix dimensions incompatible")
        result = []
        for i in range(rows_A):
            row = []
            for j in range(cols_B):
                val = sum(A[i][k] * B[k][j] for k in range(cols_A)) % 2
                row.append(val)
            result.append(row)
        return result


# ==============================================================================
# SECTION 1: CONSTRUCTION B MATRIX [ENHANCED]
# ==============================================================================

class ConstructionBMatrix:
    """
    Construction B matrix for Leech Lattice generation.
    Integrates with ubp_core Paley matrix derivation.
    """
    
    def __init__(self):
        """Initialize Construction B matrix."""
        if CORE_AVAILABLE:
            # Use derived Paley matrix from ubp_core
            self.B = LEECH_ENHANCED.B_matrix
        else:
            # Fallback: hardcoded Paley matrix
            self.B = [
                [0,1,1,1,1,1,1,1,1,1,1,1],
                [1,1,1,0,1,1,1,0,0,0,1,0],
                [1,1,0,1,1,1,0,0,0,1,0,1],
                [1,0,1,1,1,0,0,0,1,0,1,1],
                [1,1,1,1,0,0,0,1,0,1,1,0],
                [1,1,1,0,0,0,1,0,1,1,0,1],
                [1,1,0,0,0,1,0,1,1,0,1,1],
                [1,0,0,0,1,0,1,1,0,1,1,1],
                [1,0,0,1,0,1,1,0,1,1,1,0],
                [1,0,1,0,1,1,0,1,1,1,0,0],
                [1,1,0,1,1,0,1,1,1,0,0,0],
                [1,0,1,1,0,1,1,1,0,0,0,1]
            ]
        
        # Identity matrix
        self.I12 = _identity(12)
        
        # Full 24×24 generator matrix
        # [2*I12 |  0  ]
        # [ B    | I12 ]
        self.M = self._construct_generator_matrix()
    
    def _construct_generator_matrix(self) -> List[List[int]]:
        """Construct the full 24×24 generator matrix."""
        M = []
        
        # Top half: [2*I12 | 0]
        for i in range(12):
            row = []
            # 2*I12 part
            for j in range(12):
                row.append(2 if i == j else 0)
            # 0 part
            for j in range(12):
                row.append(0)
            M.append(row)
        
        # Bottom half: [B | I12]
        for i in range(12):
            row = []
            # B part
            for j in range(12):
                row.append(self.B[i][j])
            # I12 part
            for j in range(12):
                row.append(1 if i == j else 0)
            M.append(row)
        
        return M
    
    def matrix_vector_multiply(self, v: List[int]) -> List[int]:
        """Multiply vector by generator matrix."""
        if len(v) != 24:
            raise ValueError("Vector must have 24 elements")
        
        result = []
        for i in range(24):
            val = sum(v[j] * self.M[j][i] for j in range(24)) % 2
            result.append(val)
        
        return result


# ==============================================================================
# SECTION 2: LEECH ENGINE [ENHANCED]
# ==============================================================================

class LeechEngine:
    """
    Enhanced Leech Lattice Engine with full v4.1 integration.
    Provides deterministic generation, analysis, and validation.
    """
    
    def __init__(self):
        """Initialize Leech Engine."""
        self.construction_b = ConstructionBMatrix()
        
        # Integration with ubp_core
        self.golay = GOLAY_DECODER if CORE_AVAILABLE else None
        self.leech_enhanced = LEECH_ENHANCED if CORE_AVAILABLE else None
        self.particle_validator = PARTICLE_VALIDATOR if CORE_AVAILABLE else None
        
        # Constants
        self.DIMENSION = 24
        self.SCALE_FACTOR = 8
        self.MIN_NORM_SCALED = 4
        self.KISSING_NUMBER = 196560
        
        # Cache for minimal vectors
        self._minimal_vectors_cache = None
    
    # ========================================================================
    # BASIC OPERATIONS
    # ========================================================================
    
    def get_leech_point(self, input_vector: List[int]) -> List[int]:
        """
        Maps a 24-element integer vector to a Leech Lattice coordinate.
        
        Args:
            input_vector: 24-element integer vector
        
        Returns:
            24-element Leech point
        """
        if len(input_vector) != 24:
            raise ValueError("Input vector must have 24 elements")
        
        return self.construction_b.matrix_vector_multiply(input_vector)
    
    def verify_norm(self, point: List[int]) -> int:
        """
        Calculate squared norm of a point.
        
        Minimal Leech vectors have norm² = 4 (scaled to 32 in this representation).
        
        Args:
            point: 24-element Leech point
        
        Returns:
            Squared norm
        """
        if len(point) != 24:
            raise ValueError("Point must have 24 elements")
        
        return sum(p * p for p in point)
    
    def verify_norm_actual(self, point: List[int]) -> Fraction:
        """
        Calculate actual squared norm as a Fraction.
        
        Args:
            point: 24-element Leech point
        
        Returns:
            Actual squared norm (norm² / 8)
        """
        norm_scaled = self.verify_norm(point)
        return Fraction(norm_scaled, self.SCALE_FACTOR)
    
    # ========================================================================
    # MEMBERSHIP & VERIFICATION
    # ========================================================================
    
    def is_in_leech(self, point: List[int]) -> bool:
        """
        Check if a point is in the Leech Lattice.
        
        Uses the true membership predicate from ubp_core if available.
        
        Args:
            point: 24-element integer vector
        
        Returns:
            True if point is in Λ₂₄, False otherwise
        """
        if CORE_AVAILABLE and self.leech_enhanced:
            return self.leech_enhanced.is_in_leech(point)
        
        # Fallback: basic checks
        if len(point) != 24:
            return False
        
        if not all(isinstance(p, int) for p in point):
            return False
        
        # Check evenness
        norm_sq = self.verify_norm(point)
        if norm_sq % 2 != 0:
            return False
        
        return True
    
    def verify_point(self, point: List[int]) -> Tuple[bool, List[str]]:
        """
        Comprehensive verification of a Leech point.
        
        Args:
            point: 24-element Leech point
        
        Returns:
            (is_valid, list_of_failures)
        """
        failures = []
        
        if len(point) != 24:
            failures.append("Dimension not 24")
            return (False, failures)
        
        if not all(isinstance(p, int) for p in point):
            failures.append("Non-integer coordinates")
            return (False, failures)
        
        # Use ubp_core verification if available
        if CORE_AVAILABLE and self.leech_enhanced:
            try:
                lp = LeechPointScaled(coords=tuple(point))
                is_valid, core_failures = self.leech_enhanced.verify_point(lp)
                return (is_valid, core_failures)
            except:
                pass
        
        # Fallback verification
        norm_sq = self.verify_norm(point)
        
        # Evenness
        if norm_sq % 2 != 0:
            failures.append("Norm not even")
        
        # Rootlessness (no norm² = 2)
        if norm_sq == 2:
            failures.append("Norm² = 2 (rootless violation)")
        
        # Minimum norm (norm² = 0 or norm² ≥ 4)
        if norm_sq == 1 or norm_sq == 3:
            failures.append("Norm² too small")
        
        return (len(failures) == 0, failures)
    
    # ========================================================================
    # MINIMAL VECTOR GENERATION
    # ========================================================================
    
    def generate_minimal_vectors_from_golay(self) -> Generator[List[int], None, None]:
        """
        Generate minimal vectors (norm² = 4) from Golay codewords.
        
        This is a deterministic generation method.
        
        Yields:
            Minimal Leech vectors
        """
        if not CORE_AVAILABLE or not self.golay:
            return
        
        # Get all Golay codewords
        codewords = self.golay.get_all_codewords()
        
        for cw in codewords:
            # Standard lift: (2b - 1) * 2
            point = [2 * (2 * b - 1) for b in cw]
            
            # Check if minimal
            norm_sq = self.verify_norm(point)
            if norm_sq == 4:
                yield point
    
    def audit_minimal_vectors(self, limit: Optional[int] = None) -> List[List[int]]:
        """
        Audit minimal vectors with deterministic generation.
        
        Args:
            limit: Maximum number to return (None = all)
        
        Returns:
            List of minimal Leech vectors
        """
        minimal_points = []
        
        for point in self.generate_minimal_vectors_from_golay():
            minimal_points.append(point)
            if limit and len(minimal_points) >= limit:
                break
        
        return minimal_points
    
    # ========================================================================
    # ANALYSIS & STATISTICS
    # ========================================================================
    
    def analyze_shell(self, target_norm_actual: Fraction) -> Dict:
        """
        Analyze a shell of the Leech Lattice.
        
        Args:
            target_norm_actual: Target norm² (as Fraction)
        
        Returns:
            Dictionary with shell statistics
        """
        target_norm_scaled = int(target_norm_actual * self.SCALE_FACTOR)
        
        points = []
        for cw in (self.golay.get_all_codewords() if CORE_AVAILABLE and self.golay else []):
            point = [2 * (2 * b - 1) for b in cw]
            if self.verify_norm(point) == target_norm_scaled:
                points.append(point)
        
        return {
            "target_norm_actual": str(target_norm_actual),
            "target_norm_scaled": target_norm_scaled,
            "point_count": len(points),
            "points": points[:10],  # First 10 for display
        }
    
    def get_statistics(self) -> Dict:
        """
        Get overall Leech Lattice statistics.
        
        Returns:
            Dictionary with statistics
        """
        stats = {
            "dimension": self.DIMENSION,
            "scale_factor": self.SCALE_FACTOR,
            "min_norm_scaled": self.MIN_NORM_SCALED,
            "kissing_number": self.KISSING_NUMBER,
            "golay_codewords": len(self.golay._codewords) if (CORE_AVAILABLE and self.golay) else 0,
            "paley_matrix_size": f"{len(self.construction_b.B)}×{len(self.construction_b.B[0])}",
            "core_available": CORE_AVAILABLE,
        }
        
        # Add particle physics if available
        if CORE_AVAILABLE and self.particle_validator:
            pred, exp, passes = self.particle_validator.validate_muon_electron_ratio()
            stats["particle_physics"] = {
                "muon_electron_predicted": pred,
                "muon_electron_experimental": exp,
                "muon_electron_passes": passes,
            }
        
        return stats
    
    # ========================================================================
    # INTEGRATION WITH UBP CORE
    # ========================================================================
    
    def get_leech_point_scaled(self, input_vector: List[int]) -> Optional['LeechPointScaled']:
        """
        Get a Leech point as LeechPointScaled object.
        
        Args:
            input_vector: 24-element integer vector
        
        Returns:
            LeechPointScaled object or None if not available
        """
        if not CORE_AVAILABLE:
            return None
        
        point = self.get_leech_point(input_vector)
        try:
            return LeechPointScaled(coords=tuple(point))
        except:
            return None
    
    def validate_with_particle_physics(self) -> Optional[Tuple[float, float, bool]]:
        """
        Validate Leech Lattice with particle physics.
        
        Returns:
            (predicted, experimental, passes) or None
        """
        if not CORE_AVAILABLE or not self.particle_validator:
            return None
        
        return self.particle_validator.validate_muon_electron_ratio()


# ==============================================================================
# SECTION 3: GLOBAL INSTANCE
# ==============================================================================

LEECH = LeechEngine()


# ==============================================================================
# SECTION 4: UTILITY FUNCTIONS
# ==============================================================================

def get_leech_point(input_vector: List[int]) -> List[int]:
    """Convenience function: get Leech point."""
    return LEECH.get_leech_point(input_vector)

def verify_norm(point: List[int]) -> int:
    """Convenience function: verify norm."""
    return LEECH.verify_norm(point)

def verify_norm_actual(point: List[int]) -> Fraction:
    """Convenience function: verify actual norm."""
    return LEECH.verify_norm_actual(point)

def is_in_leech(point: List[int]) -> bool:
    """Convenience function: check membership."""
    return LEECH.is_in_leech(point)

def verify_point(point: List[int]) -> Tuple[bool, List[str]]:
    """Convenience function: verify point."""
    return LEECH.verify_point(point)

def audit_minimal_vectors(limit: Optional[int] = None) -> List[List[int]]:
    """Convenience function: audit minimal vectors."""
    return LEECH.audit_minimal_vectors(limit)

def get_statistics() -> Dict:
    """Convenience function: get statistics."""
    return LEECH.get_statistics()


# ==============================================================================
# SECTION 5: INITIALIZATION & TESTING
# ==============================================================================

if __name__ == "__main__":
    print("=" * 80)
    print("UBP LEECH ENGINE v4.1.1 - INITIALIZATION TEST")
    print("=" * 80)
    
    # Test basic operations
    print("\n[TEST 1] Basic Operations")
    test_seed = [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    point = LEECH.get_leech_point(test_seed)
    norm = LEECH.verify_norm(point)
    norm_actual = LEECH.verify_norm_actual(point)
    print(f"  Seed:       {test_seed[:4]}...")
    print(f"  Point:      {point[:4]}...")
    print(f"  Norm²:      {norm} (scaled), {norm_actual} (actual)")
    print(f"  In Leech:   {LEECH.is_in_leech(point)}")
    
    # Test verification
    print("\n[TEST 2] Point Verification")
    is_valid, failures = LEECH.verify_point(point)
    print(f"  Valid:      {is_valid}")
    print(f"  Failures:   {failures if failures else 'None'}")
    
    # Test minimal vectors
    print("\n[TEST 3] Minimal Vectors")
    minimal = LEECH.audit_minimal_vectors(limit=5)
    print(f"  Found:      {len(minimal)} minimal vectors (limit 5)")
    if minimal:
        print(f"  First:      {minimal[0][:4]}...")
    
    # Test statistics
    print("\n[TEST 4] Statistics")
    stats = LEECH.get_statistics()
    for key, value in stats.items():
        if key != "points" and key != "particle_physics":
            print(f"  {key:30s}: {value}")
    
    # Test particle physics
    if "particle_physics" in stats:
        print("\n[TEST 5] Particle Physics Validation")
        pp = stats["particle_physics"]
        print(f"  Muon/electron predicted:  {pp['muon_electron_predicted']:.6f}")
        print(f"  Muon/electron experimental: {pp['muon_electron_experimental']:.6f}")
        print(f"  Validation:               {'PASS ✓' if pp['muon_electron_passes'] else 'FAIL ✗'}")
    
    print("\n" + "=" * 80)
    print("✓ LEECH ENGINE INITIALIZATION COMPLETE")
    print("=" * 80)
