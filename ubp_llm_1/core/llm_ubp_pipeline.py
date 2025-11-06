#!/usr/bin/env python3.11
"""
LLM-Integrated UBP Pipeline for Benchmarking
Connects real LLMs to the 7-layer UBP validation system
"""

import sys
import os
import time
import json
import re
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict

# Add paths
sys.path.insert(0, '/home/ubuntu/UBP_Repo/ubp_3.4')
sys.path.insert(0, '/home/ubuntu/ubp_expanded_system/ubp_ai_expanded')
sys.path.insert(0, '/home/ubuntu/ubp_augmented_ai/ubp_ai')

# OpenAI client
from openai import OpenAI

# UBP imports
from ubp_pipeline import UBPPipeline, PipelineConfig, ValidationResult
from tct_engine import TCTResult

@dataclass
class LLMBenchmarkResult:
    """Complete benchmark result for an LLM"""
    model_name: str
    test_query: str
    test_category: str
    
    # LLM metrics
    llm_response_time: float
    llm_tokens_used: Optional[int]
    llm_raw_response: str
    
    # UBP validation
    ubp_validation: ValidationResult
    
    # Overall
    total_time: float
    success: bool

class LLMUBPPipeline:
    """
    LLM-integrated UBP Pipeline
    
    Connects real LLMs (OpenAI, Gemini) to the 7-layer UBP validation system
    """
    
    # TCT System Prompt
    TCT_SYSTEM_PROMPT = """You are a UBP-augmented AI assistant that employs Three Column Thinking (TCT) methodology.

For every problem, structure your analysis into three columns:

**COLUMN 1: LANGUAGE (Narrative)**
- Explain the concept intuitively
- Provide context and physical meaning
- Use analogies where helpful
- Focus on WHY things work

**COLUMN 2: MATHEMATICS (Formal)**
- Express precisely using mathematical notation
- Define all variables and constants
- Show derivations step-by-step
- Include units and dimensions

**COLUMN 3: SCRIPT (Executable)**
- Provide working Python code
- Include comments explaining logic
- Show example output
- Verify results programmatically

Ensure all three columns are aligned and consistent. The script should verify the mathematics, and the language should explain both.

Format your response EXACTLY as:

=== LANGUAGE ===
[Your narrative explanation here]

=== MATHEMATICS ===
[Your mathematical formulation here]

=== SCRIPT ===
```python
[Your Python code here]
```

Do not include any other text outside these sections."""
    
    def __init__(self, config: Optional[PipelineConfig] = None):
        self.config = config or PipelineConfig(
            nrci_accept_threshold=0.85,
            nrci_correct_threshold=0.70,
            apply_glr_correction=True,
            observer_convergence_enabled=True,
            store_validated_responses=True
        )
        
        # Initialize UBP pipeline
        self.ubp_pipeline = UBPPipeline(self.config)
        
        # Initialize OpenAI client (API key from environment)
        self.client = OpenAI()
        
        print("LLM-UBP Pipeline initialized")
        print(f"  Available models: gpt-4.1-mini, gpt-4.1-nano, gemini-2.5-flash")
        print()
    
    def call_llm(self, model: str, query: str, temperature: float = 0.7) -> tuple:
        """
        Call LLM with query
        
        Returns: (response_text, response_time, tokens_used)
        """
        start_time = time.time()
        
        try:
            response = self.client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": self.TCT_SYSTEM_PROMPT},
                    {"role": "user", "content": query}
                ],
                temperature=temperature,
                max_tokens=2000
            )
            
            response_time = time.time() - start_time
            response_text = response.choices[0].message.content
            
            # Get token usage if available
            tokens_used = None
            if hasattr(response, 'usage'):
                tokens_used = response.usage.total_tokens
            
            return response_text, response_time, tokens_used
            
        except Exception as e:
            print(f"  ⚠️  LLM call failed: {e}")
            return None, time.time() - start_time, None
    
    def parse_tct_response(self, response_text: str) -> Optional[TCTResult]:
        """
        Parse LLM response into TCT columns
        
        Expected format:
        === LANGUAGE ===
        ...
        === MATHEMATICS ===
        ...
        === SCRIPT ===
        ```python
        ...
        ```
        """
        if not response_text:
            return None
        
        try:
            # Extract sections
            language_match = re.search(r'=== LANGUAGE ===\s*(.*?)\s*=== MATHEMATICS ===', 
                                      response_text, re.DOTALL)
            math_match = re.search(r'=== MATHEMATICS ===\s*(.*?)\s*=== SCRIPT ===', 
                                  response_text, re.DOTALL)
            script_match = re.search(r'=== SCRIPT ===\s*```python\s*(.*?)\s*```', 
                                    response_text, re.DOTALL)
            
            if not (language_match and math_match and script_match):
                # Try alternative parsing
                print("  ⚠️  Standard TCT format not found, attempting flexible parsing...")
                return self._flexible_parse(response_text)
            
            language = language_match.group(1).strip()
            mathematics = math_match.group(1).strip()
            script = script_match.group(1).strip()
            
            # Calculate heuristic coherence
            coherence = self._calculate_coherence(language, mathematics, script)
            
            return TCTResult(
                language_column=language,
                mathematics_column=mathematics,
                script_column=script,
                coherence_score=coherence,
                script_output=None
            )
            
        except Exception as e:
            print(f"  ⚠️  TCT parsing failed: {e}")
            return None
    
    def _flexible_parse(self, response_text: str) -> Optional[TCTResult]:
        """Flexible parsing when standard format fails"""
        # Split by common section markers
        lines = response_text.split('\n')
        
        language = []
        mathematics = []
        script = []
        current_section = None
        in_code_block = False
        
        for line in lines:
            line_lower = line.lower().strip()
            
            # Detect section transitions
            if 'language' in line_lower or 'narrative' in line_lower:
                current_section = 'language'
                continue
            elif 'mathematics' in line_lower or 'formal' in line_lower or 'equation' in line_lower:
                current_section = 'mathematics'
                continue
            elif 'script' in line_lower or 'code' in line_lower or 'python' in line_lower:
                current_section = 'script'
                continue
            
            # Detect code blocks
            if '```' in line:
                in_code_block = not in_code_block
                if 'python' in line_lower:
                    current_section = 'script'
                continue
            
            # Add content to current section
            if current_section == 'language' and not in_code_block:
                language.append(line)
            elif current_section == 'mathematics' and not in_code_block:
                mathematics.append(line)
            elif current_section == 'script' or in_code_block:
                script.append(line)
        
        # Join sections
        language_text = '\n'.join(language).strip()
        math_text = '\n'.join(mathematics).strip()
        script_text = '\n'.join(script).strip()
        
        if not (language_text and math_text and script_text):
            # Last resort: split into thirds
            third = len(lines) // 3
            language_text = '\n'.join(lines[:third])
            math_text = '\n'.join(lines[third:2*third])
            script_text = '\n'.join(lines[2*third:])
        
        coherence = self._calculate_coherence(language_text, math_text, script_text)
        
        return TCTResult(
            language_column=language_text,
            mathematics_column=math_text,
            script_column=script_text,
            coherence_score=coherence,
            script_output=None
        )
    
    def _calculate_coherence(self, language: str, mathematics: str, script: str) -> float:
        """Calculate heuristic coherence score"""
        score = 0.5  # Base score
        
        # Check language quality
        if len(language) > 100:
            score += 0.1
        if any(word in language.lower() for word in ['because', 'therefore', 'thus', 'since']):
            score += 0.05
        
        # Check mathematics quality
        if any(symbol in mathematics for symbol in ['=', '+', '-', '*', '/', '^']):
            score += 0.1
        if any(word in mathematics for word in ['where', 'given', 'let']):
            score += 0.05
        
        # Check script quality
        if 'def ' in script or 'import ' in script:
            score += 0.1
        if 'print(' in script or 'return' in script:
            score += 0.05
        
        # Check alignment (keyword overlap)
        language_words = set(language.lower().split())
        math_words = set(mathematics.lower().split())
        script_words = set(script.lower().split())
        
        overlap = len(language_words & math_words & script_words)
        if overlap > 5:
            score += 0.1
        
        return min(1.0, score)
    
    def benchmark(self, model: str, query: str, category: str = "General") -> LLMBenchmarkResult:
        """
        Benchmark an LLM on a single query through full UBP pipeline
        
        Args:
            model: Model name (gpt-4.1-mini, gpt-4.1-nano, gemini-2.5-flash)
            query: Test query
            category: Test category
            
        Returns:
            LLMBenchmarkResult with complete metrics
        """
        total_start = time.time()
        
        print(f"Benchmarking {model} on: {query[:60]}...")
        print("-" * 80)
        
        # Step 1: Call LLM
        print("  [1/3] Calling LLM...")
        response_text, llm_time, tokens = self.call_llm(model, query)
        
        if not response_text:
            print("  ✗ LLM call failed")
            return None
        
        print(f"  ✓ LLM responded in {llm_time:.2f}s ({tokens} tokens)")
        
        # Step 2: Parse TCT
        print("  [2/3] Parsing TCT columns...")
        tct_result = self.parse_tct_response(response_text)
        
        if not tct_result:
            print("  ✗ TCT parsing failed")
            return None
        
        print(f"  ✓ TCT parsed (coherence: {tct_result.coherence_score:.3f})")
        
        # Step 3: UBP validation
        print("  [3/3] Running UBP validation (7 layers)...")
        
        # Override pipeline's TCT generation
        original_layer1 = self.ubp_pipeline._layer1_tct
        self.ubp_pipeline._layer1_tct = lambda q, h, c: tct_result
        
        # Run through UBP pipeline
        ubp_result = self.ubp_pipeline.process(query)
        
        # Restore original
        self.ubp_pipeline._layer1_tct = original_layer1
        
        total_time = time.time() - total_start
        success = ubp_result.final_action in ["accept", "correct"]
        
        print(f"  ✓ UBP validation complete")
        print(f"  → NRCI: {ubp_result.nrci_score:.6f}")
        print(f"  → Action: {ubp_result.final_action}")
        print(f"  → Total time: {total_time:.2f}s")
        print()
        
        return LLMBenchmarkResult(
            model_name=model,
            test_query=query,
            test_category=category,
            llm_response_time=llm_time,
            llm_tokens_used=tokens,
            llm_raw_response=response_text,
            ubp_validation=ubp_result,
            total_time=total_time,
            success=success
        )


def demo_benchmark():
    """Demo: Benchmark a single LLM"""
    print("=" * 80)
    print("LLM-UBP BENCHMARK DEMO")
    print("=" * 80)
    print()
    
    pipeline = LLMUBPPipeline()
    
    # Test query
    query = "Solve the quadratic equation x² - 5x + 6 = 0 using the quadratic formula"
    
    # Benchmark gpt-4.1-mini
    result = pipeline.benchmark("gpt-4.1-mini", query, "Mathematical Reasoning")
    
    if result:
        print("=" * 80)
        print("BENCHMARK RESULT")
        print("=" * 80)
        print(f"Model: {result.model_name}")
        print(f"Query: {result.test_query}")
        print(f"LLM Time: {result.llm_response_time:.2f}s")
        print(f"Tokens: {result.llm_tokens_used}")
        print(f"NRCI: {result.ubp_validation.nrci_score:.6f}")
        print(f"Final Action: {result.ubp_validation.final_action}")
        print(f"Overall Score: {result.ubp_validation.overall_score:.3f}")
        print(f"Total Time: {result.total_time:.2f}s")
        print(f"Success: {result.success}")
        print()

if __name__ == "__main__":
    demo_benchmark()
