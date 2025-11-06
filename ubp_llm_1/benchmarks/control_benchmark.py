#!/usr/bin/env python3.11
"""
Control Group Benchmark: Non-UBP LLMs
Tests raw LLM responses without any UBP augmentation
"""

import time
import json
from openai import OpenAI
from dataclasses import dataclass, asdict
from typing import List, Optional

@dataclass
class ControlResult:
    """Result from non-UBP LLM test"""
    query: str
    category: str
    model: str
    
    # Response metrics
    response: str
    response_time: float
    tokens_used: Optional[int]
    
    # Manual quality assessment (to be scored)
    has_errors: bool = False
    error_description: str = ""
    completeness_score: float = 0.0  # 0-1
    accuracy_score: float = 0.0  # 0-1
    coherence_score: float = 0.0  # 0-1

# Standard test queries (same as UBP benchmark)
TEST_QUERIES = [
    {
        'category': 'Mathematical',
        'query': 'Calculate the eigenvalues of matrix [[3,1],[1,3]] and explain the geometric meaning',
        'expected_answer': 'Eigenvalues are 4 and 2'
    },
    {
        'category': 'Physical',
        'query': 'Derive the Schwarzschild radius and explain why nothing can escape a black hole',
        'expected_answer': 'Rs = 2GM/c^2'
    },
    {
        'category': 'Logical',
        'query': 'If all A are B, and some B are C, what can we conclude about A and C?',
        'expected_answer': 'Cannot conclude anything definite about A and C'
    },
    {
        'category': 'Code',
        'query': 'Write a Python function to find the longest palindromic substring using dynamic programming',
        'expected_answer': 'Working DP solution'
    },
    {
        'category': 'Multi-step',
        'query': 'A train travels 120 km in 2 hours, then 180 km in 3 hours. Calculate average speed and explain if it equals the average of the two speeds.',
        'expected_answer': 'Average speed is 60 km/h, not equal to average of speeds'
    },
    {
        'category': 'Edge Case',
        'query': 'What is 0^0? Explain why different contexts give different answers.',
        'expected_answer': 'Context-dependent: 1 in combinatorics, undefined in analysis'
    },
    {
        'category': 'Contradiction',
        'query': 'Explain the twin paradox in special relativity. Why does each twin think the other should age slower?',
        'expected_answer': 'Symmetry breaking through acceleration'
    },
    {
        'category': 'Complex',
        'query': 'Prove that the sum of angles in a triangle is 180 degrees using parallel postulate',
        'expected_answer': 'Proof using alternate interior angles'
    }
]

class ControlBenchmark:
    """Benchmark for non-UBP LLMs"""
    
    def __init__(self):
        self.client = OpenAI()
        print("Control Benchmark initialized (No UBP)")
        print("Testing raw LLM responses without augmentation")
        print()
    
    def call_llm(self, model: str, query: str) -> tuple:
        """
        Call LLM without any UBP augmentation
        
        Returns: (response_text, response_time, tokens_used)
        """
        start_time = time.time()
        
        try:
            response = self.client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": "You are a helpful AI assistant. Provide clear, accurate, and complete answers."},
                    {"role": "user", "content": query}
                ],
                temperature=0.7,
                max_tokens=2000
            )
            
            response_time = time.time() - start_time
            response_text = response.choices[0].message.content
            
            tokens_used = None
            if hasattr(response, 'usage'):
                tokens_used = response.usage.total_tokens
            
            return response_text, response_time, tokens_used
            
        except Exception as e:
            return f"ERROR: {str(e)}", time.time() - start_time, None
    
    def assess_quality(self, response: str, expected: str, category: str) -> dict:
        """
        Automated quality assessment of response
        
        Returns dict with:
        - has_errors: bool
        - error_description: str
        - completeness_score: float (0-1)
        - accuracy_score: float (0-1)
        - coherence_score: float (0-1)
        """
        # Simple heuristic assessment
        response_lower = response.lower()
        
        # Check for errors
        has_errors = False
        error_desc = ""
        
        # Common error patterns
        if "i don't know" in response_lower or "i cannot" in response_lower:
            has_errors = True
            error_desc = "Refused to answer"
        elif "error" in response_lower and ":" in response:
            has_errors = True
            error_desc = "Error in response"
        elif len(response) < 50:
            has_errors = True
            error_desc = "Response too short"
        
        # Completeness (length and structure)
        if len(response) > 500:
            completeness = 1.0
        elif len(response) > 200:
            completeness = 0.8
        elif len(response) > 100:
            completeness = 0.6
        else:
            completeness = 0.4
        
        # Accuracy (check for expected content)
        accuracy = 0.5  # Default neutral
        expected_lower = expected.lower()
        
        # Simple keyword matching
        keywords = expected_lower.split()
        matches = sum(1 for kw in keywords if kw in response_lower)
        if matches > len(keywords) * 0.7:
            accuracy = 0.9
        elif matches > len(keywords) * 0.5:
            accuracy = 0.7
        elif matches > 0:
            accuracy = 0.6
        
        # Coherence (sentence structure)
        sentences = response.split('.')
        if len(sentences) > 3:
            coherence = 0.8
        elif len(sentences) > 1:
            coherence = 0.6
        else:
            coherence = 0.4
        
        return {
            'has_errors': has_errors,
            'error_description': error_desc,
            'completeness_score': completeness,
            'accuracy_score': accuracy,
            'coherence_score': coherence
        }
    
    def run_benchmark(self, model: str, queries: List[dict]) -> List[ControlResult]:
        """Run control benchmark on model"""
        
        print("=" * 80)
        print(f"CONTROL BENCHMARK: {model} (No UBP)")
        print("=" * 80)
        print(f"Testing {len(queries)} queries without UBP augmentation")
        print()
        
        results = []
        
        for i, test in enumerate(queries, 1):
            print(f"[{i}/{len(queries)}] {test['category']}: {test['query'][:60]}...")
            
            # Call LLM
            response, resp_time, tokens = self.call_llm(model, test['query'])
            
            # Assess quality
            quality = self.assess_quality(
                response,
                test['expected_answer'],
                test['category']
            )
            
            result = ControlResult(
                query=test['query'],
                category=test['category'],
                model=model,
                response=response,
                response_time=resp_time,
                tokens_used=tokens,
                **quality
            )
            
            results.append(result)
            
            # Print summary
            print(f"  Time: {resp_time:.2f}s")
            print(f"  Completeness: {quality['completeness_score']:.2f}")
            print(f"  Accuracy: {quality['accuracy_score']:.2f}")
            print(f"  Coherence: {quality['coherence_score']:.2f}")
            if quality['has_errors']:
                print(f"  ⚠️  Error: {quality['error_description']}")
            print()
        
        # Summary
        print("=" * 80)
        print("CONTROL BENCHMARK SUMMARY")
        print("=" * 80)
        
        avg_time = sum(r.response_time for r in results) / len(results)
        avg_completeness = sum(r.completeness_score for r in results) / len(results)
        avg_accuracy = sum(r.accuracy_score for r in results) / len(results)
        avg_coherence = sum(r.coherence_score for r in results) / len(results)
        error_count = sum(1 for r in results if r.has_errors)
        
        print(f"Model: {model}")
        print(f"Tests: {len(results)}")
        print(f"Errors: {error_count} ({100*error_count/len(results):.1f}%)")
        print(f"Avg time: {avg_time:.2f}s")
        print(f"Avg completeness: {avg_completeness:.3f}")
        print(f"Avg accuracy: {avg_accuracy:.3f}")
        print(f"Avg coherence: {avg_coherence:.3f}")
        print(f"Overall score: {(avg_completeness + avg_accuracy + avg_coherence) / 3:.3f}")
        print()
        
        return results

def main():
    """Run control benchmark"""
    benchmark = ControlBenchmark()
    
    # Test on gpt-4.1-nano (best from UBP benchmark)
    results = benchmark.run_benchmark('gpt-4.1-nano', TEST_QUERIES)
    
    # Save results
    output = {
        'model': 'gpt-4.1-nano',
        'system': 'control (no UBP)',
        'test_count': len(results),
        'results': [asdict(r) for r in results]
    }
    
    with open('control_results_gpt-4.1-nano.json', 'w') as f:
        json.dump(output, f, indent=2)
    
    print(f"Results saved to: control_results_gpt-4.1-nano.json")

if __name__ == "__main__":
    main()
