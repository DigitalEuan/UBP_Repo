"""
================================================================================
UBP Antibiotic Discovery - Bitfield Explorer
Author: Euan R A Craig, New Zealand - # Powered by UBP 3.7.1
Date: 30 November 2025
================================================================================

Systematic exploration of the 24-bit OffBit Bitfield for antibiotic discovery.

**Core Concept**:
The 24-bit space (2^24 = 16,777,216 states) is treated as a unified Bitfield
where antibiotics emerge naturally when resonance conditions are applied.

**Exploration Strategy**:
1. Random sampling (for broad coverage)
2. Seeded patterns (from known antibiotics)
3. Targeted regions (high-coherence neighborhoods)

**Zero Dependencies**: Only Python stdlib + UBP 3.6 core + antibiotic_realm
"""

import sys
import random
import time
import json
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass, asdict

# Add UBP core to path
sys.path.insert(0, '/home/ubuntu/ubp_antibiotics_study/ubp_core')
sys.path.insert(0, '/home/ubuntu/ubp_antibiotics_study')

from antibiotic_realm import AntibioticRealm, AntibioticState, NRCI_MODERATE


# ============================================================================
# EXPLORATION STATISTICS
# ============================================================================

@dataclass
class ExplorationStats:
    """Statistics from Bitfield exploration."""
    total_patterns_explored: int = 0
    patterns_passed_filters: int = 0
    supercoherent_hits: int = 0
    excellent_hits: int = 0
    good_hits: int = 0
    moderate_hits: int = 0
    novel_scaffolds: int = 0
    zero_toxicity_hits: int = 0
    exploration_time_seconds: float = 0.0
    patterns_per_second: float = 0.0
    
    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return asdict(self)
    
    def update_from_candidate(self, candidate: AntibioticState):
        """Update statistics from a candidate."""
        self.patterns_passed_filters += 1
        
        # Activity class
        if candidate.activity_class == "SuperCoherent":
            self.supercoherent_hits += 1
        elif candidate.activity_class == "Excellent":
            self.excellent_hits += 1
        elif candidate.activity_class == "Good":
            self.good_hits += 1
        elif candidate.activity_class == "Moderate":
            self.moderate_hits += 1
        
        # Novel scaffolds (all are novel by definition)
        if candidate.is_novel:
            self.novel_scaffolds += 1
        
        # Zero toxicity
        if not candidate.toxicity_flag:
            self.zero_toxicity_hits += 1
    
    def finalize(self, elapsed_time: float):
        """Finalize statistics after exploration."""
        self.exploration_time_seconds = elapsed_time
        if elapsed_time > 0:
            self.patterns_per_second = self.total_patterns_explored / elapsed_time
    
    def print_summary(self):
        """Print exploration summary."""
        print("\n" + "=" * 80)
        print("EXPLORATION SUMMARY")
        print("=" * 80)
        print(f"Total patterns explored: {self.total_patterns_explored:,}")
        print(f"Patterns passed filters: {self.patterns_passed_filters:,}")
        print(f"Hit rate: {100.0 * self.patterns_passed_filters / max(1, self.total_patterns_explored):.6f}%")
        print(f"\nActivity Distribution:")
        print(f"  SuperCoherent: {self.supercoherent_hits:,}")
        print(f"  Excellent: {self.excellent_hits:,}")
        print(f"  Good: {self.good_hits:,}")
        print(f"  Moderate: {self.moderate_hits:,}")
        print(f"\nNovel scaffolds: {self.novel_scaffolds:,}")
        print(f"Zero toxicity hits: {self.zero_toxicity_hits:,}")
        print(f"\nPerformance:")
        print(f"  Exploration time: {self.exploration_time_seconds:.2f} seconds")
        print(f"  Patterns/second: {self.patterns_per_second:,.0f}")
        print("=" * 80)


# ============================================================================
# KNOWN ANTIBIOTIC SEEDS
# ============================================================================

# Known antibiotics for training/seeding
# These are hex values derived from known antibiotic structures
KNOWN_ANTIBIOTIC_SEEDS = {
    "linezolid": 0xA77F3C,
    "penicillin_core": 0x19B88E,
    "vancomycin_fragment": 0xE44C11,
    "daptomycin_analog": 0x77B001,
    "tigecycline_base": 0x000F3D,
    "lincomycin_scaffold": 0xC003A9,
    "streptomycin_core": 0xF88887,
}


# ============================================================================
# BITFIELD EXPLORER
# ============================================================================

class BitfieldExplorer:
    """
    Explores the 24-bit OffBit Bitfield for antibiotic candidates.
    
    Implements multiple exploration strategies:
    - Random sampling
    - Seeded patterns
    - Neighborhood search
    """
    
    def __init__(self, realm: Optional[AntibioticRealm] = None):
        """
        Initialize Bitfield explorer.
        
        Args:
            realm: AntibioticRealm instance (creates new if None)
        """
        self.realm = realm if realm is not None else AntibioticRealm()
        self.stats = ExplorationStats()
        self.candidates: List[AntibioticState] = []
        self.explored_patterns: set = set()
    
    def explore_random(
        self,
        num_patterns: int,
        seed: Optional[int] = None,
        progress_interval: int = 10000
    ) -> List[AntibioticState]:
        """
        Explore random patterns in the Bitfield.
        
        Args:
            num_patterns: Number of patterns to explore
            seed: Random seed for reproducibility
            progress_interval: Print progress every N patterns
            
        Returns:
            List of AntibioticState candidates
        """
        if seed is not None:
            random.seed(seed)
        
        print(f"\n🔍 Exploring {num_patterns:,} random patterns...")
        start_time = time.time()
        
        candidates = []
        
        for i in range(num_patterns):
            # Generate random 24-bit pattern
            pattern = random.randint(0, 0xFFFFFF)
            
            # Skip if already explored
            if pattern in self.explored_patterns:
                continue
            
            self.explored_patterns.add(pattern)
            self.stats.total_patterns_explored += 1
            
            # Process candidate
            candidate = self.realm.process_candidate(pattern)
            
            if candidate is not None:
                candidates.append(candidate)
                self.stats.update_from_candidate(candidate)
                
                # Print rabbit emoji for super-rabbits
                if candidate.activity_class == "SuperCoherent":
                    print(f"🐰 Super-rabbit found! {candidate.offbit_hex} (NRCI: {candidate.nrci:.10f})")
            
            # Progress update
            if (i + 1) % progress_interval == 0:
                elapsed = time.time() - start_time
                rate = (i + 1) / elapsed
                print(f"   Progress: {i+1:,}/{num_patterns:,} ({100.0*(i+1)/num_patterns:.1f}%) "
                      f"- {rate:,.0f} patterns/sec - {len(candidates)} hits")
        
        elapsed_time = time.time() - start_time
        self.stats.finalize(elapsed_time)
        
        self.candidates.extend(candidates)
        return candidates
    
    def explore_seeds(
        self,
        seeds: Optional[Dict[str, int]] = None
    ) -> List[AntibioticState]:
        """
        Explore known antibiotic seeds.
        
        Args:
            seeds: Dictionary of seed names to hex values (uses defaults if None)
            
        Returns:
            List of AntibioticState candidates
        """
        if seeds is None:
            seeds = KNOWN_ANTIBIOTIC_SEEDS
        
        print(f"\n🌱 Exploring {len(seeds)} known antibiotic seeds...")
        start_time = time.time()
        
        candidates = []
        
        for name, pattern in seeds.items():
            self.explored_patterns.add(pattern)
            self.stats.total_patterns_explored += 1
            
            # Process candidate
            candidate = self.realm.process_candidate(pattern)
            
            if candidate is not None:
                candidates.append(candidate)
                self.stats.update_from_candidate(candidate)
                print(f"   ✓ {name}: {candidate.offbit_hex} (NRCI: {candidate.nrci:.10f}, "
                      f"MIC: {candidate.predicted_mic:.3f} μg/mL)")
            else:
                print(f"   ✗ {name}: {hex(pattern)} (failed filters)")
        
        elapsed_time = time.time() - start_time
        
        self.candidates.extend(candidates)
        return candidates
    
    def explore_neighborhood(
        self,
        center_pattern: int,
        radius: int = 1000,
        max_patterns: int = 10000
    ) -> List[AntibioticState]:
        """
        Explore neighborhood around a center pattern.
        
        Args:
            center_pattern: Center OffBit pattern
            radius: Hamming distance radius
            max_patterns: Maximum patterns to explore
            
        Returns:
            List of AntibioticState candidates
        """
        print(f"\n🎯 Exploring neighborhood around {hex(center_pattern)} (radius={radius})...")
        start_time = time.time()
        
        candidates = []
        patterns_explored = 0
        
        # Generate patterns within Hamming distance
        for _ in range(max_patterns):
            # Flip random bits
            num_flips = random.randint(1, radius)
            pattern = center_pattern
            
            for _ in range(num_flips):
                bit_pos = random.randint(0, 23)
                pattern ^= (1 << bit_pos)
            
            # Skip if already explored
            if pattern in self.explored_patterns:
                continue
            
            self.explored_patterns.add(pattern)
            self.stats.total_patterns_explored += 1
            patterns_explored += 1
            
            # Process candidate
            candidate = self.realm.process_candidate(pattern)
            
            if candidate is not None:
                candidates.append(candidate)
                self.stats.update_from_candidate(candidate)
                
                if candidate.activity_class == "SuperCoherent":
                    print(f"   🐰 {candidate.offbit_hex} (NRCI: {candidate.nrci:.10f})")
        
        elapsed_time = time.time() - start_time
        print(f"   Explored {patterns_explored:,} patterns, found {len(candidates)} hits")
        
        self.candidates.extend(candidates)
        return candidates
    
    def get_top_candidates(
        self,
        n: int = 10,
        sort_by: str = 'nrci'
    ) -> List[AntibioticState]:
        """
        Get top N candidates.
        
        Args:
            n: Number of candidates to return
            sort_by: Sort criterion ('nrci', 'mic', 'selectivity')
            
        Returns:
            List of top candidates
        """
        if sort_by == 'nrci':
            sorted_candidates = sorted(self.candidates, key=lambda c: c.nrci, reverse=True)
        elif sort_by == 'mic':
            sorted_candidates = sorted(self.candidates, key=lambda c: c.predicted_mic)
        elif sort_by == 'selectivity':
            sorted_candidates = sorted(self.candidates, key=lambda c: c.selectivity_index, reverse=True)
        else:
            sorted_candidates = self.candidates
        
        return sorted_candidates[:n]
    
    def export_results(
        self,
        filename: str,
        include_stats: bool = True
    ):
        """
        Export results to JSON file.
        
        Args:
            filename: Output filename
            include_stats: Include exploration statistics
        """
        results = {
            'candidates': [c.to_dict() for c in self.candidates],
            'num_candidates': len(self.candidates)
        }
        
        if include_stats:
            results['statistics'] = self.stats.to_dict()
        
        with open(filename, 'w') as f:
            json.dump(results, f, indent=2)
        
        print(f"\n💾 Results exported to {filename}")
    
    def print_summary(self):
        """Print exploration summary."""
        self.stats.print_summary()
        
        if self.candidates:
            print(f"\n📊 TOP 10 CANDIDATES (by NRCI):")
            print("-" * 80)
            top_10 = self.get_top_candidates(10, 'nrci')
            for i, candidate in enumerate(top_10, 1):
                print(f"{i:2d}. {candidate.offbit_hex} | NRCI: {candidate.nrci:.10f} | "
                      f"MIC: {candidate.predicted_mic:.3f} μg/mL | "
                      f"Activity: {candidate.activity_class}")
            print("-" * 80)


# ============================================================================
# VALIDATION
# ============================================================================

def validate_bitfield_explorer():
    """Validate the Bitfield explorer."""
    print("=" * 80)
    print("Bitfield Explorer Validation")
    print("=" * 80)
    
    explorer = BitfieldExplorer()
    
    # Test 1: Explore seeds
    print("\n1. Testing seed exploration...")
    seed_candidates = explorer.explore_seeds()
    print(f"   Found {len(seed_candidates)} candidates from seeds")
    
    # Test 2: Small random exploration
    print("\n2. Testing random exploration (1000 patterns)...")
    random_candidates = explorer.explore_random(1000, seed=42, progress_interval=500)
    print(f"   Found {len(random_candidates)} candidates from random exploration")
    
    # Test 3: Neighborhood exploration
    if seed_candidates:
        print("\n3. Testing neighborhood exploration...")
        center = seed_candidates[0].offbit.value
        neighborhood_candidates = explorer.explore_neighborhood(center, radius=5, max_patterns=500)
        print(f"   Found {len(neighborhood_candidates)} candidates from neighborhood")
    
    # Print summary
    explorer.print_summary()
    
    print("\n" + "=" * 80)
    print("✅ Bitfield Explorer Validation Complete")
    print("=" * 80)


if __name__ == "__main__":
    validate_bitfield_explorer()
