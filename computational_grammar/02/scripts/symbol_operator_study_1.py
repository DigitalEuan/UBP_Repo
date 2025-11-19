#!/usr/bin/env python3
"""
UBP Symbol Operator Study - Focus_1: Comprehensive Investigation
Phase 1: Operator Taxonomy and Coherence Analysis

This script investigates whether Symbol Operators represent the 
"instruction set" of the UBP Bitfield - geometrically necessary 
operations that emerge from the substrate itself.

Author: Euan Craig / Genspark Super Agent: UBP Creator 3.5
Date: November 18, 2025
"""

import math
import json
from typing import Dict, List, Tuple, Set, Callable
from collections import defaultdict

# Since we're working with zero-dependency UBP, implement minimal required functionality
class MinimalCoherenceState:
    """Minimal CoherenceState for operator analysis."""
    
    def __init__(self, value: float, nrci: float = 0.999997):
        self.value = value
        self.nrci = nrci
        self.log_nrci_error = math.log(1.0 - nrci)
    
    def __repr__(self):
        return f"CS({self.value:.6e}, NRCI={self.nrci:.10f})"


# UBP Constants
PI = math.pi
Y = PI / (PI**2 + 2)  # 0.264675430404527
Y_INVERSE = PI + 2/PI  # 3.778212425957375
GOLDEN_RATIO = (1 + math.sqrt(5)) / 2


class SymbolOperator:
    """
    Represents a mathematical/computational operator with UBP properties.
    
    An operator in UBP is not just a function - it's a geometrically 
    positioned entity in the information substrate.
    """
    
    def __init__(self, name: str, symbol: str, 
                 implementation: Callable,
                 d1_arity: float,
                 d2_role: float,
                 d3_invertibility: float,
                 d4_commutativity: float,
                 d5_meaning_count: float,
                 d6_dependency_depth: float,
                 d7_closure: float,
                 d8_overloading: float,
                 description: str = ""):
        
        self.name = name
        self.symbol = symbol
        self.implementation = implementation
        self.description = description
        
        # 8D Property Vector (D-variables from Symbol Study)
        self.d1_arity = d1_arity
        self.d2_role = d2_role
        self.d3_invertibility = d3_invertibility
        self.d4_commutativity = d4_commutativity
        self.d5_meaning_count = d5_meaning_count
        self.d6_dependency_depth = d6_dependency_depth
        self.d7_closure = d7_closure
        self.d8_overloading = d8_overloading
        
        # Compute intrinsic NRCI from D-variables
        self.predicted_nrci = self._compute_nrci()
        
        # Toggle set representation for Jaccard distance
        self.toggle_set = self._compute_toggle_set()
    
    def _compute_nrci(self) -> float:
        """
        Compute predicted NRCI from D-variables using discovered model.
        
        From Symbol Study: D6 (Depth) and D5 (Meaning) are dominant.
        Simple model: NRCI ≈ 1 - (w6*D6 + w5*D5 + w8*D8)
        """
        # Empirical weights from Symbol Study
        w6 = 0.000200  # Dependency depth (most important)
        w5 = 0.000050  # Meaning count
        w8 = 0.000030  # Overloading
        
        error_contribution = (
            w6 * self.d6_dependency_depth +
            w5 * self.d5_meaning_count +
            w8 * self.d8_overloading
        )
        
        # NRCI baseline for optimal operators
        base_nrci = 0.999997
        
        # Clamp to valid range
        nrci = max(0.0, min(1.0, base_nrci - error_contribution))
        return nrci
    
    def _compute_toggle_set(self) -> Set[str]:
        """
        Convert D-variables to toggle set for Jaccard distance.
        This enables geometric clustering of operators.
        """
        toggles = set()
        
        # Arity toggles
        if self.d1_arity <= 0.25:
            toggles.add("arity_nullary")
        elif self.d1_arity <= 0.5:
            toggles.add("arity_unary")
        elif self.d1_arity <= 0.75:
            toggles.add("arity_binary")
        else:
            toggles.add("arity_ternary")
        
        # Role toggles
        if self.d2_role < 0.2:
            toggles.add("role_operand")
        elif self.d2_role < 0.4:
            toggles.add("role_relation")
        elif self.d2_role < 0.6:
            toggles.add("role_operator")
        elif self.d2_role < 0.8:
            toggles.add("role_quantifier")
        else:
            toggles.add("role_meta")
        
        # Invertibility
        if self.d3_invertibility > 0.8:
            toggles.add("invertible_full")
        elif self.d3_invertibility > 0.3:
            toggles.add("invertible_partial")
        else:
            toggles.add("invertible_none")
        
        # Commutativity
        if self.d4_commutativity > 0.5:
            toggles.add("commutative")
        
        # Meaning count (ambiguity)
        if self.d5_meaning_count < 0.2:
            toggles.add("meaning_single")
        elif self.d5_meaning_count < 0.5:
            toggles.add("meaning_few")
        else:
            toggles.add("meaning_many")
        
        # Dependency depth (complexity)
        if self.d6_dependency_depth < 0.2:
            toggles.add("depth_primitive")
        elif self.d6_dependency_depth < 0.5:
            toggles.add("depth_moderate")
        else:
            toggles.add("depth_complex")
        
        # Closure
        if self.d7_closure > 0.8:
            toggles.add("closure_full")
        elif self.d7_closure > 0.3:
            toggles.add("closure_partial")
        else:
            toggles.add("closure_none")
        
        # Overloading
        if self.d8_overloading < 0.2:
            toggles.add("overload_minimal")
        elif self.d8_overloading < 0.5:
            toggles.add("overload_moderate")
        else:
            toggles.add("overload_high")
        
        return toggles
    
    def execute(self, *args):
        """Execute the operator on given arguments."""
        return self.implementation(*args)
    
    def __repr__(self):
        return f"Operator({self.symbol}, NRCI={self.predicted_nrci:.10f})"


def jaccard_distance(set_a: Set[str], set_b: Set[str]) -> float:
    """Compute Jaccard distance between two toggle sets."""
    if len(set_a) == 0 and len(set_b) == 0:
        return 0.0
    union = set_a | set_b
    if len(union) == 0:
        return 0.0
    intersection = set_a & set_b
    similarity = len(intersection) / len(union)
    return 1.0 - similarity


def define_core_operators() -> List[SymbolOperator]:
    """
    Define core mathematical and computational operators.
    
    This includes:
    1. Arithmetic operators (+, -, *, /, ^)
    2. Logical operators (AND, OR, XOR, NOT)
    3. Comparison operators (=, <, >)
    4. Transcendental functions (sin, cos, exp, log)
    5. Novel operators from Symbol Study
    """
    
    operators = []
    
    # === ARITHMETIC OPERATORS ===
    
    # Addition (+)
    operators.append(SymbolOperator(
        name="Addition",
        symbol="+",
        implementation=lambda x, y: x + y,
        d1_arity=0.5,  # Binary (2/2 = 1.0 → min with 1.0)
        d2_role=0.5,   # Operator
        d3_invertibility=1.0,  # Fully invertible (subtraction)
        d4_commutativity=1.0,  # Commutative
        d5_meaning_count=0.1,  # Single meaning
        d6_dependency_depth=0.1,  # Primitive operation
        d7_closure=1.0,  # Closed over numbers
        d8_overloading=0.2,  # Minimal overloading
        description="Binary addition operator"
    ))
    
    # Subtraction (-)
    operators.append(SymbolOperator(
        name="Subtraction",
        symbol="-",
        implementation=lambda x, y: x - y,
        d1_arity=0.5,
        d2_role=0.5,
        d3_invertibility=1.0,
        d4_commutativity=0.0,  # NOT commutative
        d5_meaning_count=0.1,
        d6_dependency_depth=0.1,
        d7_closure=1.0,
        d8_overloading=0.2,
        description="Binary subtraction operator"
    ))
    
    # Multiplication (*)
    operators.append(SymbolOperator(
        name="Multiplication",
        symbol="*",
        implementation=lambda x, y: x * y,
        d1_arity=0.5,
        d2_role=0.5,
        d3_invertibility=1.0,  # Division
        d4_commutativity=1.0,
        d5_meaning_count=0.15,  # Slight ambiguity (scalar vs cross product)
        d6_dependency_depth=0.15,
        d7_closure=1.0,
        d8_overloading=0.3,
        description="Binary multiplication operator"
    ))
    
    # Division (/)
    operators.append(SymbolOperator(
        name="Division",
        symbol="/",
        implementation=lambda x, y: x / y if y != 0 else float('inf'),
        d1_arity=0.5,
        d2_role=0.5,
        d3_invertibility=1.0,
        d4_commutativity=0.0,
        d5_meaning_count=0.1,
        d6_dependency_depth=0.15,
        d7_closure=0.5,  # Partial closure (division by zero)
        d8_overloading=0.2,
        description="Binary division operator"
    ))
    
    # Exponentiation (^)
    operators.append(SymbolOperator(
        name="Exponentiation",
        symbol="^",
        implementation=lambda x, y: x ** y,
        d1_arity=0.5,
        d2_role=0.5,
        d3_invertibility=0.5,  # Partially invertible (logarithm)
        d4_commutativity=0.0,
        d5_meaning_count=0.1,
        d6_dependency_depth=0.25,  # More complex
        d7_closure=0.5,  # Complex results possible
        d8_overloading=0.2,
        description="Binary exponentiation operator"
    ))
    
    # === LOGICAL OPERATORS ===
    
    # AND
    operators.append(SymbolOperator(
        name="LogicalAND",
        symbol="∧",
        implementation=lambda x, y: x and y,
        d1_arity=0.5,
        d2_role=0.5,
        d3_invertibility=0.0,  # Not invertible
        d4_commutativity=1.0,
        d5_meaning_count=0.1,
        d6_dependency_depth=0.1,
        d7_closure=1.0,  # Boolean closure
        d8_overloading=0.1,
        description="Logical AND operator"
    ))
    
    # OR
    operators.append(SymbolOperator(
        name="LogicalOR",
        symbol="∨",
        implementation=lambda x, y: x or y,
        d1_arity=0.5,
        d2_role=0.5,
        d3_invertibility=0.0,
        d4_commutativity=1.0,
        d5_meaning_count=0.1,
        d6_dependency_depth=0.1,
        d7_closure=1.0,
        d8_overloading=0.1,
        description="Logical OR operator"
    ))
    
    # XOR
    operators.append(SymbolOperator(
        name="LogicalXOR",
        symbol="⊕",
        implementation=lambda x, y: (x or y) and not (x and y),
        d1_arity=0.5,
        d2_role=0.5,
        d3_invertibility=1.0,  # Self-inverse
        d4_commutativity=1.0,
        d5_meaning_count=0.1,
        d6_dependency_depth=0.1,
        d7_closure=1.0,
        d8_overloading=0.15,  # Sometimes used for addition mod 2
        description="Logical XOR operator (self-inverse)"
    ))
    
    # NOT
    operators.append(SymbolOperator(
        name="LogicalNOT",
        symbol="¬",
        implementation=lambda x: not x,
        d1_arity=0.25,  # Unary (1/2 = 0.5, min with 1.0)
        d2_role=0.5,
        d3_invertibility=1.0,  # Self-inverse
        d4_commutativity=0.0,  # Unary, N/A
        d5_meaning_count=0.1,
        d6_dependency_depth=0.05,  # Most primitive
        d7_closure=1.0,
        d8_overloading=0.1,
        description="Logical NOT operator (involution)"
    ))
    
    # === COMPARISON OPERATORS ===
    
    # Equality (=)
    operators.append(SymbolOperator(
        name="Equality",
        symbol="=",
        implementation=lambda x, y: x == y,
        d1_arity=0.5,
        d2_role=0.25,  # Relation, not operator
        d3_invertibility=0.0,
        d4_commutativity=1.0,
        d5_meaning_count=0.2,  # Assignment vs comparison ambiguity
        d6_dependency_depth=0.1,
        d7_closure=1.0,  # Returns boolean
        d8_overloading=0.5,  # High overloading (assignment, comparison, definition)
        description="Equality relation/operator"
    ))
    
    # Less Than (<)
    operators.append(SymbolOperator(
        name="LessThan",
        symbol="<",
        implementation=lambda x, y: x < y,
        d1_arity=0.5,
        d2_role=0.25,
        d3_invertibility=0.0,
        d4_commutativity=0.0,
        d5_meaning_count=0.1,
        d6_dependency_depth=0.1,
        d7_closure=1.0,
        d8_overloading=0.1,
        description="Less than relation"
    ))
    
    # === TRANSCENDENTAL FUNCTIONS ===
    
    # Sine
    operators.append(SymbolOperator(
        name="Sine",
        symbol="sin",
        implementation=lambda x: math.sin(x),
        d1_arity=0.25,
        d2_role=0.5,
        d3_invertibility=0.5,  # Arcsin, but not full
        d4_commutativity=0.0,
        d5_meaning_count=0.1,
        d6_dependency_depth=0.35,  # Requires series/lookup
        d7_closure=1.0,  # Returns [-1, 1]
        d8_overloading=0.1,
        description="Trigonometric sine function"
    ))
    
    # Cosine
    operators.append(SymbolOperator(
        name="Cosine",
        symbol="cos",
        implementation=lambda x: math.cos(x),
        d1_arity=0.25,
        d2_role=0.5,
        d3_invertibility=0.5,
        d4_commutativity=0.0,
        d5_meaning_count=0.1,
        d6_dependency_depth=0.35,
        d7_closure=1.0,
        d8_overloading=0.1,
        description="Trigonometric cosine function"
    ))
    
    # Exponential
    operators.append(SymbolOperator(
        name="Exponential",
        symbol="exp",
        implementation=lambda x: math.exp(x),
        d1_arity=0.25,
        d2_role=0.5,
        d3_invertibility=1.0,  # Natural log
        d4_commutativity=0.0,
        d5_meaning_count=0.1,
        d6_dependency_depth=0.30,
        d7_closure=0.5,  # Can overflow
        d8_overloading=0.1,
        description="Natural exponential function"
    ))
    
    # Natural Logarithm
    operators.append(SymbolOperator(
        name="NaturalLog",
        symbol="ln",
        implementation=lambda x: math.log(x) if x > 0 else float('-inf'),
        d1_arity=0.25,
        d2_role=0.5,
        d3_invertibility=1.0,  # Exponential
        d4_commutativity=0.0,
        d5_meaning_count=0.15,  # ln vs log confusion
        d6_dependency_depth=0.30,
        d7_closure=0.5,  # Undefined for x<=0
        d8_overloading=0.2,
        description="Natural logarithm function"
    ))
    
    # === NOVEL OPERATORS FROM SYMBOL STUDY ===
    
    # Geometric-Harmonic Mean (⊛)
    operators.append(SymbolOperator(
        name="GeometricHarmonicMean",
        symbol="⊛",
        implementation=lambda a, b: math.sqrt(a * b) * 2 / (1/a + 1/b) if a > 0 and b > 0 else 0,
        d1_arity=0.5,
        d2_role=0.5,
        d3_invertibility=0.0,
        d4_commutativity=1.0,
        d5_meaning_count=0.1,  # PMA: Single meaning
        d6_dependency_depth=0.1,  # PMC: Simple composition
        d7_closure=1.0,
        d8_overloading=0.1,  # PMU: Unique role
        description="Novel: Geometric-Harmonic Mean (NRCI=0.999993)"
    ))
    
    # Soft Constraint (≲)
    operators.append(SymbolOperator(
        name="SoftConstraint",
        symbol="≲",
        implementation=lambda x, bound, k=1.0: 1.0 / (1.0 + math.exp(k * (x - bound))),
        d1_arity=0.67,  # Ternary (3/2, min with 1.0)
        d2_role=0.5,
        d3_invertibility=0.5,
        d4_commutativity=0.0,
        d5_meaning_count=0.1,
        d6_dependency_depth=0.1,
        d7_closure=1.0,  # Returns [0, 1]
        d8_overloading=0.1,
        description="Novel: Soft Constraint (NRCI=0.999992)"
    ))
    
    # Momentum Tracker (↑)
    operators.append(SymbolOperator(
        name="MomentumTracker",
        symbol="↑",
        implementation=lambda current, previous, alpha=0.9: alpha * previous + (1 - alpha) * current,