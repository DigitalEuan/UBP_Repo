#!/usr/bin/env python3.11
"""
UBP-Augmented Benchmark
Run same queries through original UBP system (NRCI threshold 0.85)
"""

import sys
sys.path.insert(0, '/home/ubuntu/ubp_benchmark')

from llm_ubp_pipeline import LLMUBPPipeline
from ubp_pipeline import PipelineConfig
import json
import time

# Same test queries as control
TEST_QUERIES = [
    {'category': 'Mathematical', 'query': 'Calculate the eigenvalues of matrix [[3,1],[1,3]] and explain the geometric meaning'},
    {'category': 'Physical', 'query': 'Derive the Schwarzschild radius and explain why nothing can escape a black hole'},
    {'category': 'Logical', 'query': 'If all A are B, and some B are C, what can we conclude about A and C?'},
    {'category': 'Code', 'query': 'Write a Python function to find the longest palindromic substring using dynamic programming'},
    {'category': 'Multi-step', 'query': 'A train travels 120 km in 2 hours, then 180 km in 3 hours. Calculate average speed and explain if it equals the average of the two speeds.'},
    {'category': 'Edge Case', 'query': 'What is 0^0? Explain why different contexts give different answers.'},
    {'category': 'Contradiction', 'query': 'Explain the twin paradox in special relativity. Why does each twin think the other should age slower?'},
    {'category': 'Complex', 'query': 'Prove that the sum of angles in a triangle is 180 degrees using parallel postulate'}
]

def main():
    print("=" * 80)
    print("UBP-AUGMENTED BENCHMARK (Original System)")
    print("=" * 80)
    print("NRCI threshold: 0.85 (original)")
    print("Testing 8 queries with full 7-layer UBP validation")
    print()
    
    # Create UBP pipeline with original config
    config = PipelineConfig(
        nrci_accept_threshold=0.85,  # Original threshold
        nrci_correct_threshold=0.70,
        apply_glr_correction=True,
        observer_convergence_enabled=True,
        store_validated_responses=True
    )
    
    pipeline = LLMUBPPipeline(config=config)
    
    results = []
    
    for i, test in enumerate(TEST_QUERIES, 1):
        print(f"[{i}/{len(TEST_QUERIES)}] {test['category']}: {test['query'][:60]}...")
        
        start_time = time.time()
        
        try:
            result = pipeline.benchmark('gpt-4.1-nano', test['query'], test['category'])
            elapsed = time.time() - start_time
            
            print(f"  Time: {elapsed:.2f}s")
            print(f"  NRCI: {result.ubp_validation.nrci_score:.6f}")
            print(f"  Action: {result.ubp_validation.final_action}")
            print(f"  Score: {result.ubp_validation.overall_score:.3f}")
            print()
            
            results.append({
                'category': test['category'],
                'query': test['query'],
                'nrci': result.ubp_validation.nrci_score,
                'action': result.ubp_validation.final_action,
                'score': result.ubp_validation.overall_score,
                'time': elapsed,
                'llm_time': result.llm_response_time,
                'ubp_overhead': elapsed - result.llm_response_time,
                'success': True
            })
            
        except Exception as e:
            elapsed = time.time() - start_time
            print(f"  ✗ Error: {str(e)}")
            print()
            
            results.append({
                'category': test['category'],
                'query': test['query'],
                'error': str(e),
                'time': elapsed,
                'success': False
            })
    
    # Summary
    print("=" * 80)
    print("UBP-AUGMENTED SUMMARY")
    print("=" * 80)
    
    successful = [r for r in results if r['success']]
    
    if successful:
        avg_nrci = sum(r['nrci'] for r in successful) / len(successful)
        avg_score = sum(r['score'] for r in successful) / len(successful)
        avg_time = sum(r['time'] for r in successful) / len(successful)
        avg_llm_time = sum(r['llm_time'] for r in successful) / len(successful)
        avg_ubp_overhead = sum(r['ubp_overhead'] for r in successful) / len(successful)
        
        actions = {}
        for r in successful:
            actions[r['action']] = actions.get(r['action'], 0) + 1
        
        print(f"Success rate: {len(successful)}/{len(results)} ({100*len(successful)/len(results):.1f}%)")
        print(f"Avg NRCI: {avg_nrci:.6f}")
        print(f"Avg score: {avg_score:.3f}")
        print(f"Avg total time: {avg_time:.2f}s")
        print(f"Avg LLM time: {avg_llm_time:.2f}s")
        print(f"Avg UBP overhead: {avg_ubp_overhead:.2f}s")
        print()
        print("Action distribution:")
        for action, count in sorted(actions.items()):
            print(f"  {action}: {count} ({100*count/len(successful):.1f}%)")
        print()
    
    # Save results
    output = {
        'model': 'gpt-4.1-nano',
        'system': 'UBP-augmented (original, NRCI=0.85)',
        'test_count': len(results),
        'results': results
    }
    
    with open('ubp_augmented_results.json', 'w') as f:
        json.dump(output, f, indent=2)
    
    print(f"Results saved to: ubp_augmented_results.json")

if __name__ == "__main__":
    main()
