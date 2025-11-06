#!/usr/bin/env python3.11
"""
Comprehensive Test Suite for Expanded UBP System
Demonstrates all 7 layers with realistic scenarios
"""

import sys
import os
import json
import time
import numpy as np
from dataclasses import asdict

sys.path.insert(0, '/home/ubuntu/ubp_expanded_system/ubp_ai_expanded')
sys.path.insert(0, '/home/ubuntu/UBP_Repo/ubp_3.4')

from ubp_pipeline import UBPPipeline, PipelineConfig, ValidationResult
from ubp_ai.tct_engine import TCTResult

class ExpandedSystemTests:
    """Comprehensive test suite for expanded UBP system"""
    
    def __init__(self):
        # Create pipeline with test-friendly settings
        self.config = PipelineConfig(
            nrci_accept_threshold=0.85,  # Lower for testing
            nrci_correct_threshold=0.65,
            nrci_regenerate_threshold=0.45,
            apply_glr_correction=True,
            observer_convergence_enabled=True,
            store_validated_responses=True,
            min_nrci_for_storage=0.80
        )
        
        self.pipeline = UBPPipeline(self.config)
        self.results = []
        
    def create_mock_tct_result(self, query: str, quality: str = "high") -> TCTResult:
        """
        Create mock TCT result with specified quality
        
        quality: "high", "medium", "low"
        """
        if quality == "high":
            coherence = np.random.uniform(0.90, 0.98)
            language = f"""
            **Language Column (Narrative):**
            
            This problem asks us to {query}. We can approach this systematically by 
            breaking it down into clear steps. The underlying principle is well-established
            in the field and has been verified through multiple experiments.
            
            The key insight is that we need to consider both the theoretical framework
            and the practical implementation. By combining these perspectives, we can
            arrive at a robust solution that is both mathematically sound and 
            computationally efficient.
            """
            
            mathematics = f"""
            **Mathematics Column (Formal):**
            
            Let x be the primary variable.
            Given: f(x) = x² + 2x + 1
            
            We seek to find: x such that f(x) = 0
            
            Solution:
            x² + 2x + 1 = 0
            (x + 1)² = 0
            x = -1
            
            Verification: f(-1) = (-1)² + 2(-1) + 1 = 1 - 2 + 1 = 0 ✓
            """
            
            script = """
            **Script Column (Executable):**
            
            import numpy as np
            
            def solve_problem(x):
                return x**2 + 2*x + 1
            
            # Find solution
            x_solution = -1
            
            # Verify
            result = solve_problem(x_solution)
            print(f"f({x_solution}) = {result}")
            
            assert abs(result) < 1e-10, "Solution verification failed"
            print("Solution verified!")
            """
            
        elif quality == "medium":
            coherence = np.random.uniform(0.70, 0.85)
            language = f"This problem involves {query}. We can solve it using standard methods."
            mathematics = f"Let x be the variable. Then x = solution."
            script = f"# Code for {query}\nx = 0\nprint(x)"
            
        else:  # low
            coherence = np.random.uniform(0.40, 0.60)
            language = f"Something about {query}"
            mathematics = "x = y"
            script = "pass"
        
        return TCTResult(
            language_column=language,
            mathematics_column=mathematics,
            script_column=script,
            coherence_score=coherence,
            script_output="Success" if quality == "high" else None
        )
    
    def test_category_a_mathematical_reasoning(self):
        """Test A: Mathematical Reasoning with full UBP integration"""
        print("=" * 80)
        print("TEST CATEGORY A: MATHEMATICAL REASONING (Full UBP)")
        print("=" * 80)
        print()
        
        test_cases = [
            ("Solve x² - 5x + 6 = 0", "high"),
            ("Derive the area formula for a circle", "high"),
            ("Prove the Pythagorean theorem", "high"),
            ("Calculate lim(x→0) sin(x)/x", "medium"),
            ("Integrate x·e^x dx", "medium"),
        ]
        
        for query, quality in test_cases:
            print(f"Testing: {query}")
            print("-" * 80)
            
            # Create high-quality mock TCT
            tct_result = self.create_mock_tct_result(query, quality)
            
            # Manually process through pipeline layers
            result = self._process_with_mock_tct(query, tct_result)
            
            self.results.append({
                "category": "Mathematical Reasoning",
                "query": query,
                "quality": quality,
                "result": result
            })
            
            print(f"  NRCI: {result.nrci_score:.6f}")
            print(f"  Regime: {result.coherence_regime}")
            print(f"  Final Action: {result.final_action}")
            print(f"  Overall Score: {result.overall_score:.3f}")
            print()
        
        print()
    
    def test_category_b_physical_reasoning(self):
        """Test B: Physical Reasoning with UBP realms"""
        print("=" * 80)
        print("TEST CATEGORY B: PHYSICAL REASONING (UBP Realms)")
        print("=" * 80)
        print()
        
        test_cases = [
            ("Calculate gravitational force between Earth and Moon", "high"),
            ("Explain quantum tunneling in U-238 alpha decay", "high"),
            ("Derive time dilation formula", "medium"),
            ("Calculate resonant frequency of LC circuit", "high"),
            ("Explain LIGO gravitational wave detection", "medium"),
        ]
        
        for query, quality in test_cases:
            print(f"Testing: {query}")
            print("-" * 80)
            
            tct_result = self.create_mock_tct_result(query, quality)
            result = self._process_with_mock_tct(query, tct_result)
            
            self.results.append({
                "category": "Physical Reasoning",
                "query": query,
                "quality": quality,
                "result": result
            })
            
            print(f"  NRCI: {result.nrci_score:.6f}")
            print(f"  GLR Errors: {len(result.glr_errors)}")
            print(f"  O_observer: {result.o_observer_final:.6f}")
            print(f"  E_SOC: {result.e_soc:.3e} CU")
            print()
        
        print()
    
    def test_category_c_logical_consistency(self):
        """Test C: Logical Consistency with GLR"""
        print("=" * 80)
        print("TEST CATEGORY C: LOGICAL CONSISTENCY (GLR Error Correction)")
        print("=" * 80)
        print()
        
        test_cases = [
            ("Detect contradiction: A implies B, but not B", "medium"),
            ("Check consistency: All X are Y, Z is X, therefore Z is Y", "high"),
            ("Identify circular reasoning in argument", "medium"),
            ("Verify transitivity: A>B, B>C, therefore A>C", "high"),
            ("Detect false dichotomy", "medium"),
        ]
        
        for query, quality in test_cases:
            print(f"Testing: {query}")
            print("-" * 80)
            
            tct_result = self.create_mock_tct_result(query, quality)
            result = self._process_with_mock_tct(query, tct_result)
            
            self.results.append({
                "category": "Logical Consistency",
                "query": query,
                "quality": quality,
                "result": result
            })
            
            print(f"  NRCI: {result.nrci_score:.6f}")
            print(f"  GLR Errors Detected: {len(result.glr_errors)}")
            print(f"  GLR Corrections Applied: {result.glr_corrections_applied}")
            print(f"  NRCI Improvement: {result.nrci_improvement:+.6f}")
            print()
        
        print()
    
    def test_category_d_hexdict_analytics(self):
        """Test D: HexDict Advanced Analytics"""
        print("=" * 80)
        print("TEST CATEGORY D: HEXDICT ADVANCED ANALYTICS")
        print("=" * 80)
        print()
        
        test_cases = [
            ("The Y constant is π/(π²+2)", "high"),  # Known fact
            ("The Z constant is related to dark energy", "medium"),  # Novel claim
            ("O_observer equals 2.5", "low"),  # Contradicts known fact
            ("NRCI measures quantum coherence", "high"),  # Partially correct
            ("UBP explains gravity through coherence gradients", "high"),  # Known
        ]
        
        for query, quality in test_cases:
            print(f"Testing: {query}")
            print("-" * 80)
            
            tct_result = self.create_mock_tct_result(query, quality)
            result = self._process_with_mock_tct(query, tct_result)
            
            self.results.append({
                "category": "HexDict Analytics",
                "query": query,
                "quality": quality,
                "result": result
            })
            
            print(f"  Novelty Score: {result.novelty_score:.3f}")
            print(f"  Verified Claims: {result.verified_claims}")
            print(f"  Novel Claims: {result.novel_claims}")
            print(f"  Contradictions: {result.contradictions}")
            print()
        
        print()
    
    def test_category_e_observer_convergence(self):
        """Test E: Observer Framework Convergence"""
        print("=" * 80)
        print("TEST CATEGORY E: OBSERVER FRAMEWORK CONVERGENCE")
        print("=" * 80)
        print()
        
        test_cases = [
            ("Simple task: add two numbers", "high", 0.2),  # Low complexity
            ("Medium task: solve differential equation", "high", 0.5),
            ("Complex task: prove Riemann hypothesis", "medium", 0.9),
        ]
        
        for query, quality, complexity in test_cases:
            print(f"Testing: {query} (complexity={complexity:.1f})")
            print("-" * 80)
            
            tct_result = self.create_mock_tct_result(query, quality)
            result = self._process_with_mock_tct(query, tct_result)
            
            self.results.append({
                "category": "Observer Convergence",
                "query": query,
                "quality": quality,
                "complexity": complexity,
                "result": result
            })
            
            print(f"  Initial O_observer: {result.o_observer_initial:.6f}")
            print(f"  Final O_observer: {result.o_observer_final:.6f}")
            print(f"  Target (1/Y): 3.778212426")
            print(f"  Distance from target: {abs(result.o_observer_final - 3.778212426):.6f}")
            print(f"  Convergence iterations: {result.convergence_iterations}")
            print()
        
        print()
    
    def _process_with_mock_tct(self, query: str, tct_result: TCTResult) -> ValidationResult:
        """Process query with pre-generated TCT result"""
        start_time = time.time()
        
        # Override pipeline's TCT generation
        original_layer1 = self.pipeline._layer1_tct
        self.pipeline._layer1_tct = lambda q, h, c: tct_result
        
        # Process through pipeline
        result = self.pipeline.process(query)
        
        # Restore original
        self.pipeline._layer1_tct = original_layer1
        
        return result
    
    def generate_summary(self):
        """Generate test summary"""
        print("=" * 80)
        print("EXPANDED SYSTEM TEST SUMMARY")
        print("=" * 80)
        print()
        
        # Overall stats
        total_tests = len(self.results)
        
        # NRCI stats
        nrcis = [r["result"].nrci_score for r in self.results]
        avg_nrci = np.mean(nrcis)
        
        # Score stats
        scores = [r["result"].overall_score for r in self.results]
        avg_score = np.mean(scores)
        
        # Action distribution
        actions = [r["result"].final_action for r in self.results]
        action_counts = {
            "accept": actions.count("accept"),
            "correct": actions.count("correct"),
            "regenerate": actions.count("regenerate"),
            "reject": actions.count("reject")
        }
        
        print(f"Total Tests: {total_tests}")
        print()
        
        print("NRCI Statistics:")
        print(f"  Average: {avg_nrci:.6f}")
        print(f"  Min: {min(nrcis):.6f}")
        print(f"  Max: {max(nrcis):.6f}")
        print()
        
        print("Overall Score Statistics:")
        print(f"  Average: {avg_score:.3f}")
        print(f"  Min: {min(scores):.3f}")
        print(f"  Max: {max(scores):.3f}")
        print()
        
        print("Action Distribution:")
        for action, count in action_counts.items():
            percentage = (count / total_tests) * 100
            print(f"  {action.capitalize()}: {count} ({percentage:.1f}%)")
        print()
        
        # Category breakdown
        categories = {}
        for r in self.results:
            cat = r["category"]
            if cat not in categories:
                categories[cat] = []
            categories[cat].append(r["result"])
        
        print("Category Breakdown:")
        for cat, results in categories.items():
            cat_nrci = np.mean([r.nrci_score for r in results])
            cat_score = np.mean([r.overall_score for r in results])
            print(f"  {cat}:")
            print(f"    Tests: {len(results)}")
            print(f"    Avg NRCI: {cat_nrci:.6f}")
            print(f"    Avg Score: {cat_score:.3f}")
        print()
        
        # GLR statistics
        total_glr_errors = sum(len(r["result"].glr_errors) for r in self.results)
        total_glr_corrections = sum(r["result"].glr_corrections_applied for r in self.results)
        avg_nrci_improvement = np.mean([r["result"].nrci_improvement for r in self.results])
        
        print("GLR Error Correction:")
        print(f"  Total Errors Detected: {total_glr_errors}")
        print(f"  Total Corrections Applied: {total_glr_corrections}")
        print(f"  Avg NRCI Improvement: {avg_nrci_improvement:+.6f}")
        print()
        
        # Observer statistics
        avg_o_initial = np.mean([r["result"].o_observer_initial for r in self.results])
        avg_o_final = np.mean([r["result"].o_observer_final for r in self.results])
        avg_convergence = np.mean([r["result"].convergence_iterations for r in self.results])
        
        print("Observer Framework:")
        print(f"  Avg Initial O_observer: {avg_o_initial:.6f}")
        print(f"  Avg Final O_observer: {avg_o_final:.6f}")
        print(f"  Target (1/Y): 3.778212426")
        print(f"  Avg Distance from Target: {abs(avg_o_final - 3.778212426):.6f}")
        print(f"  Avg Convergence Iterations: {avg_convergence:.1f}")
        print()
        
        # SOC statistics
        avg_e_soc = np.mean([r["result"].e_soc for r in self.results if r["result"].e_soc > 0])
        
        print("SOC Energy:")
        print(f"  Avg E_SOC: {avg_e_soc:.3e} CU")
        print()
        
        # Storage statistics
        stored_count = sum(1 for r in self.results if r["result"].stored_hash is not None)
        storage_rate = (stored_count / total_tests) * 100
        
        print("Knowledge Persistence:")
        print(f"  Responses Stored: {stored_count}/{total_tests} ({storage_rate:.1f}%)")
        print()
        
        print("=" * 80)
        
        # Save results
        self.save_results()
    
    def save_results(self):
        """Save test results to JSON"""
        output = {
            "test_suite": "Expanded UBP System",
            "timestamp": time.time(),
            "config": asdict(self.config),
            "results": []
        }
        
        for r in self.results:
            result_dict = {
                "category": r["category"],
                "query": r["query"],
                "quality": r["quality"],
                "nrci": r["result"].nrci_score,
                "regime": r["result"].coherence_regime,
                "final_action": r["result"].final_action,
                "overall_score": r["result"].overall_score,
                "glr_errors": len(r["result"].glr_errors),
                "glr_corrections": r["result"].glr_corrections_applied,
                "nrci_improvement": r["result"].nrci_improvement,
                "o_observer_final": r["result"].o_observer_final,
                "e_soc": r["result"].e_soc,
                "stored": r["result"].stored_hash is not None
            }
            output["results"].append(result_dict)
        
        filepath = "/home/ubuntu/ubp_expanded_system/tests/expanded_system_results.json"
        with open(filepath, 'w') as f:
            json.dump(output, f, indent=2)
        
        print(f"Results saved to: {filepath}")
        print()
    
    def run_all_tests(self):
        """Run all test categories"""
        print()
        print("╔" + "=" * 78 + "╗")
        print("║" + " " * 15 + "EXPANDED UBP SYSTEM - COMPREHENSIVE TESTS" + " " * 22 + "║")
        print("╚" + "=" * 78 + "╝")
        print()
        
        self.test_category_a_mathematical_reasoning()
        self.test_category_b_physical_reasoning()
        self.test_category_c_logical_consistency()
        self.test_category_d_hexdict_analytics()
        self.test_category_e_observer_convergence()
        
        self.generate_summary()


def main():
    """Run comprehensive tests"""
    tests = ExpandedSystemTests()
    tests.run_all_tests()

if __name__ == "__main__":
    main()
