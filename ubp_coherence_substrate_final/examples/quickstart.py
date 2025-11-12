#!/usr/bin/env python3
"""
UBP Coherence Substrate - Quick Start Example
==============================================

This script demonstrates the basic usage of the UBP Coherence Substrate.

Author: Euan R A Craig, New Zealand
Date: November 11, 2025
Version: 1.0.0
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from ubp import *
import math

print("="*70)
print("UBP COHERENCE SUBSTRATE v1.0 - QUICK START")
print("="*70)

# Example 1: Integration
print("\n📊 Example 1: Numerical Integration")
print("   Computing ∫ x² dx from 0 to 1")
result, metrics = integrate(lambda x: x**2, 0, 1, exact=1/3)
print(f"   Result: {result:.10f}")
print(f"   Exact:  {1/3:.10f}")
print(f"   Error:  {metrics['error']:.2e}")
print(f"   NRCI:   {metrics['nrci']:.10f}")

# Example 2: Root Finding
print("\n📊 Example 2: Root Finding")
print("   Finding root of x² - 2 = 0")
result = root(lambda x: x**2 - 2, x0=1.0)
print(f"   Root: x = {result['x']:.10f}")
print(f"   √2 =      {math.sqrt(2):.10f}")
print(f"   f(x) =    {result['f(x)']:.2e}")
print(f"   NRCI =    {result['nrci']:.10f}")

# Example 3: Linear System
print("\n📊 Example 3: Solving Linear System")
print("   2x + y = 5")
print("   x + 3y = 7")
A = [[2, 1], [1, 3]]
b = [5, 7]
result = solve(A, b)
print(f"   Solution: x = {result['x']}")
print(f"   NRCI:     {result['nrci']:.10f}")

# Example 4: Coherence State
print("\n📊 Example 4: Coherence State")
state = CoherenceState(1000.0)
print(f"   Initial: value={state.value:.2f}, nrci={state.nrci:.10f}")

forward = state.refine_forward()
print(f"   Forward: value={forward.value:.2f}, nrci={forward.nrci:.10f}")

backward = forward.refine_backward()
print(f"   Backward: value={backward.value:.2f}, nrci={backward.nrci:.10f}")

error, ok = state.test_closure()
print(f"   Closure: error={error:.2e}, ok={ok}")

# Example 5: Self-Healing
print("\n📊 Example 5: Self-Healing Under Perturbation")
state = CoherenceState(1.0)
healed, metrics = self_heal(state, shock_magnitude=0.1, healing_iterations=5)
print(f"   Initial NRCI:  {metrics['initial_nrci']:.10f}")
print(f"   After shock:   {metrics['shocked_nrci']:.10f}")
print(f"   After healing: {metrics['final_nrci']:.10f}")
print(f"   Recovery:      {metrics['recovery_rate']:.2%}")
print(f"   {'✅ Healed!' if metrics['healed'] else '❌ Collapsed'}")

print("\n" + "="*70)
print("✓ Quick Start Complete")
print("="*70)
print("\n💡 This is UBP: information-first, coherence-native computation.")
print("   Every value carries its own quality measure (NRCI).")
print("   Computation maintains coherence, not just accuracy.")
