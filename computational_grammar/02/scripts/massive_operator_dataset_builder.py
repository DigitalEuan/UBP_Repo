"""
Massive Operator Dataset Builder
==================================

This script builds a comprehensive dataset of mathematical and computational operators
with full 24-bit OffBit analysis. The goal is to create a dataset large enough to reveal
deep structural patterns, families, and trees in the operator space.

Target: 500+ operators across all domains (mathematical, logical, computational, quantum, etc.)
"""

import sys
import json
import math
from pathlib import Path
from collections import defaultdict

# Add UBP 3.5 to path
ubp_path = Path("/home/ubuntu/UBP_Repo/ubp_3.5")
sys.path.insert(0, str(ubp_path))

from coherence_substrate import GOLDEN_RATIO


class MassiveOperatorDatasetBuilder:
    """Build a comprehensive operator dataset with full bitfield analysis."""
    
    def __init__(self):
        self.Y = GOLDEN_RATIO
        self.operators = []
        
        # NRCI prediction model parameters (validated)
        self.NRCI_base = 0.999997
        self.w6 = 2.0e-4
        self.w5 = 5.0e-5
        self.w8 = 3.0e-5
        
    def add_operator(self, symbol, name, category, d_vars, description=""):
        """Add an operator to the dataset with full analysis."""
        
        # Predict NRCI
        predicted_nrci = self.NRCI_base - (
            self.w6 * d_vars['d6_dependency_depth'] +
            self.w5 * d_vars['d5_meaning_count'] +
            self.w8 * d_vars['d8_overloading']
        )
        
        # Encode to OffBit
        offbit = self.encode_offbit(d_vars)
        offbit_hex = hex(self.bits_to_int(offbit))
        hamming_weight = sum(offbit)
        
        # Compute layer weights
        layer_weights = {
            'reality': sum(offbit[0:6]),
            'information': sum(offbit[6:12]),
            'activation': sum(offbit[12:18]),
            'unactivated': sum(offbit[18:24])
        }
        
        # Compute layer imbalance
        max_layer = max(layer_weights.values())
        min_layer = min(layer_weights.values())
        imbalance = max_layer - min_layer
        
        # Classify as primitive or derived
        is_primitive = (
            d_vars['d6_dependency_depth'] <= 0.15 and
            d_vars['d5_meaning_count'] <= 0.15 and
            d_vars['d8_overloading'] <= 0.20
        )
        
        operator = {
            'symbol': symbol,
            'name': name,
            'category': category,
            'description': description,
            'd_variables': d_vars,
            'predicted_nrci': predicted_nrci,
            'offbit': offbit,
            'offbit_hex': offbit_hex,
            'hamming_weight': hamming_weight,
            'layer_weights': layer_weights,
            'layer_imbalance': imbalance,
            'is_primitive': is_primitive
        }
        
        self.operators.append(operator)
        return operator
    
    def encode_offbit(self, d_vars):
        """Encode D-variables to 24-bit OffBit representation."""
        bits = [0] * 24
        
        # Reality Layer (bits 0-5) - Currently unused, reserved for future
        # Could encode execution context, hardware specifics, etc.
        
        # Information Layer (bits 6-11) - Structural properties
        arity_val = int(d_vars['d1_arity'] * 3)
        bits[6] = (arity_val >> 1) & 1
        bits[7] = arity_val & 1
        
        role_val = int(d_vars['d2_role'] * 7)
        bits[8] = (role_val >> 2) & 1
        bits[9] = (role_val >> 1) & 1
        bits[10] = role_val & 1
        
        bits[11] = 1 if d_vars['d4_commutativity'] > 0.5 else 0
        
        # Activation Layer (bits 12-17) - Processing properties
        invert_val = int(d_vars['d3_invertibility'] * 3)
        bits[12] = (invert_val >> 1) & 1
        bits[13] = invert_val & 1
        
        closure_val = int(d_vars['d7_closure'] * 3)
        bits[14] = (closure_val >> 1) & 1
        bits[15] = closure_val & 1
        
        # Unactivated Layer (bits 18-23) - Potential/complexity
        meaning_val = min(3, int(d_vars['d5_meaning_count'] * 10))
        bits[18] = (meaning_val >> 1) & 1
        bits[19] = meaning_val & 1
        
        depth_val = int(d_vars['d6_dependency_depth'] * 20)  # Higher precision
        bits[20] = (depth_val >> 1) & 1
        bits[21] = depth_val & 1
        
        overload_val = int(d_vars['d8_overloading'] * 10)
        bits[22] = (overload_val >> 1) & 1
        bits[23] = overload_val & 1
        
        return bits
    
    def bits_to_int(self, bits):
        """Convert bit array to integer."""
        return int(''.join(str(b) for b in bits), 2)
    
    def build_comprehensive_dataset(self):
        """Build a massive dataset of operators across all domains."""
        
        print("Building comprehensive operator dataset...")
        print("="*70)
        
        # ================================================================
        # CATEGORY 1: PRIMITIVE OPERATORS (The Foundation)
        # ================================================================
        print("\n[1/15] Adding Primitive Operators...")
        
        # Y-Refinement operators
        self.add_operator(
            '⊗Y', 'Y-Refinement Forward', 'Primitive/Geometric',
            {
                'd1_arity': 0.25, 'd2_role': 0.5, 'd3_invertibility': 1.0,
                'd4_commutativity': 0.0, 'd5_meaning_count': 0.10,
                'd6_dependency_depth': 0.05, 'd7_closure': 1.0, 'd8_overloading': 0.10
            },
            "Multiply by golden ratio for geometric refinement"
        )
        
        self.add_operator(
            '⊗Y⁻¹', 'Y-Refinement Inverse', 'Primitive/Geometric',
            {
                'd1_arity': 0.25, 'd2_role': 0.5, 'd3_invertibility': 1.0,
                'd4_commutativity': 0.0, 'd5_meaning_count': 0.10,
                'd6_dependency_depth': 0.05, 'd7_closure': 1.0, 'd8_overloading': 0.10
            },
            "Divide by golden ratio for geometric refinement"
        )
        
        # Logical primitives
        self.add_operator(
            '¬', 'Logical NOT', 'Primitive/Logical',
            {
                'd1_arity': 0.25, 'd2_role': 0.5, 'd3_invertibility': 1.0,
                'd4_commutativity': 0.0, 'd5_meaning_count': 0.10,
                'd6_dependency_depth': 0.05, 'd7_closure': 1.0, 'd8_overloading': 0.10
            },
            "Boolean negation"
        )
        
        self.add_operator(
            '∧', 'Logical AND', 'Primitive/Logical',
            {
                'd1_arity': 0.5, 'd2_role': 0.5, 'd3_invertibility': 0.0,
                'd4_commutativity': 1.0, 'd5_meaning_count': 0.10,
                'd6_dependency_depth': 0.10, 'd7_closure': 1.0, 'd8_overloading': 0.10
            },
            "Boolean conjunction"
        )
        
        self.add_operator(
            '∨', 'Logical OR', 'Primitive/Logical',
            {
                'd1_arity': 0.5, 'd2_role': 0.5, 'd3_invertibility': 0.0,
                'd4_commutativity': 1.0, 'd5_meaning_count': 0.10,
                'd6_dependency_depth': 0.10, 'd7_closure': 1.0, 'd8_overloading': 0.10
            },
            "Boolean disjunction"
        )
        
        self.add_operator(
            '⊕', 'Logical XOR', 'Primitive/Logical',
            {
                'd1_arity': 0.5, 'd2_role': 0.5, 'd3_invertibility': 0.5,
                'd4_commutativity': 1.0, 'd5_meaning_count': 0.10,
                'd6_dependency_depth': 0.10, 'd7_closure': 1.0, 'd8_overloading': 0.10
            },
            "Boolean exclusive or"
        )
        
        # Arithmetic primitives
        self.add_operator(
            '+', 'Addition', 'Primitive/Arithmetic',
            {
                'd1_arity': 0.5, 'd2_role': 0.5, 'd3_invertibility': 1.0,
                'd4_commutativity': 1.0, 'd5_meaning_count': 0.10,
                'd6_dependency_depth': 0.10, 'd7_closure': 1.0, 'd8_overloading': 0.15
            },
            "Arithmetic addition"
        )
        
        self.add_operator(
            '−', 'Subtraction', 'Primitive/Arithmetic',
            {
                'd1_arity': 0.5, 'd2_role': 0.5, 'd3_invertibility': 1.0,
                'd4_commutativity': 0.0, 'd5_meaning_count': 0.10,
                'd6_dependency_depth': 0.10, 'd7_closure': 1.0, 'd8_overloading': 0.15
            },
            "Arithmetic subtraction"
        )
        
        self.add_operator(
            '×', 'Multiplication', 'Primitive/Arithmetic',
            {
                'd1_arity': 0.5, 'd2_role': 0.5, 'd3_invertibility': 0.5,
                'd4_commutativity': 1.0, 'd5_meaning_count': 0.10,
                'd6_dependency_depth': 0.15, 'd7_closure': 1.0, 'd8_overloading': 0.20
            },
            "Arithmetic multiplication"
        )
        
        self.add_operator(
            '÷', 'Division', 'Primitive/Arithmetic',
            {
                'd1_arity': 0.5, 'd2_role': 0.5, 'd3_invertibility': 0.5,
                'd4_commutativity': 0.0, 'd5_meaning_count': 0.10,
                'd6_dependency_depth': 0.15, 'd7_closure': 0.5, 'd8_overloading': 0.20
            },
            "Arithmetic division"
        )
        
        # ================================================================
        # CATEGORY 2: DERIVED ARITHMETIC OPERATORS
        # ================================================================
        print("[2/15] Adding Derived Arithmetic Operators...")
        
        self.add_operator(
            '^', 'Exponentiation', 'Derived/Arithmetic',
            {
                'd1_arity': 0.5, 'd2_role': 0.5, 'd3_invertibility': 0.5,
                'd4_commutativity': 0.0, 'd5_meaning_count': 0.10,
                'd6_dependency_depth': 0.25, 'd7_closure': 0.5, 'd8_overloading': 0.15
            },
            "Raise to power (iterated multiplication)"
        )
        
        self.add_operator(
            '√', 'Square Root', 'Derived/Arithmetic',
            {
                'd1_arity': 0.25, 'd2_role': 0.5, 'd3_invertibility': 0.5,
                'd4_commutativity': 0.0, 'd5_meaning_count': 0.10,
                'd6_dependency_depth': 0.25, 'd7_closure': 0.5, 'd8_overloading': 0.10
            },
            "Principal square root"
        )
        
        self.add_operator(
            '∛', 'Cube Root', 'Derived/Arithmetic',
            {
                'd1_arity': 0.25, 'd2_role': 0.5, 'd3_invertibility': 0.5,
                'd4_commutativity': 0.0, 'd5_meaning_count': 0.10,
                'd6_dependency_depth': 0.25, 'd7_closure': 1.0, 'd8_overloading': 0.10
            },
            "Cube root"
        )
        
        self.add_operator(
            '∜', 'Fourth Root', 'Derived/Arithmetic',
            {
                'd1_arity': 0.25, 'd2_role': 0.5, 'd3_invertibility': 0.5,
                'd4_commutativity': 0.0, 'd5_meaning_count': 0.10,
                'd6_dependency_depth': 0.25, 'd7_closure': 0.5, 'd8_overloading': 0.10
            },
            "Fourth root"
        )
        
        self.add_operator(
            'mod', 'Modulo', 'Derived/Arithmetic',
            {
                'd1_arity': 0.5, 'd2_role': 0.5, 'd3_invertibility': 0.0,
                'd4_commutativity': 0.0, 'd5_meaning_count': 0.15,
                'd6_dependency_depth': 0.20, 'd7_closure': 1.0, 'd8_overloading': 0.20
            },
            "Remainder after division"
        )
        
        self.add_operator(
            '|x|', 'Absolute Value', 'Derived/Arithmetic',
            {
                'd1_arity': 0.25, 'd2_role': 0.5, 'd3_invertibility': 0.0,
                'd4_commutativity': 0.0, 'd5_meaning_count': 0.10,
                'd6_dependency_depth': 0.15, 'd7_closure': 1.0, 'd8_overloading': 0.15
            },
            "Distance from zero"
        )
        
        self.add_operator(
            '⌊x⌋', 'Floor', 'Derived/Arithmetic',
            {
                'd1_arity': 0.25, 'd2_role': 0.5, 'd3_invertibility': 0.0,
                'd4_commutativity': 0.0, 'd5_meaning_count': 0.10,
                'd6_dependency_depth': 0.15, 'd7_closure': 1.0, 'd8_overloading': 0.10
            },
            "Largest integer ≤ x"
        )
        
        self.add_operator(
            '⌈x⌉', 'Ceiling', 'Derived/Arithmetic',
            {
                'd1_arity': 0.25, 'd2_role': 0.5, 'd3_invertibility': 0.0,
                'd4_commutativity': 0.0, 'd5_meaning_count': 0.10,
                'd6_dependency_depth': 0.15, 'd7_closure': 1.0, 'd8_overloading': 0.10
            },
            "Smallest integer ≥ x"
        )
        
        self.add_operator(
            '⌊x⌉', 'Round', 'Derived/Arithmetic',
            {
                'd1_arity': 0.25, 'd2_role': 0.5, 'd3_invertibility': 0.0,
                'd4_commutativity': 0.0, 'd5_meaning_count': 0.15,
                'd6_dependency_depth': 0.15, 'd7_closure': 1.0, 'd8_overloading': 0.20
            },
            "Nearest integer"
        )
        
        # ================================================================
        # CATEGORY 3: TRANSCENDENTAL FUNCTIONS
        # ================================================================
        print("[3/15] Adding Transcendental Functions...")
        
        # Exponential and logarithmic
        self.add_operator(
            'exp', 'Exponential', 'Transcendental/Exponential',
            {
                'd1_arity': 0.25, 'd2_role': 0.5, 'd3_invertibility': 0.5,
                'd4_commutativity': 0.0, 'd5_meaning_count': 0.10,
                'd6_dependency_depth': 0.40, 'd7_closure': 1.0, 'd8_overloading': 0.10
            },
            "e^x (natural exponential)"
        )
        
        self.add_operator(
            'ln', 'Natural Logarithm', 'Transcendental/Logarithmic',
            {
                'd1_arity': 0.25, 'd2_role': 0.5, 'd3_invertibility': 0.5,
                'd4_commutativity': 0.0, 'd5_meaning_count': 0.10,
                'd6_dependency_depth': 0.40, 'd7_closure': 1.0, 'd8_overloading': 0.10
            },
            "Natural logarithm (base e)"
        )
        
        self.add_operator(
            'log', 'Common Logarithm', 'Transcendental/Logarithmic',
            {
                'd1_arity': 0.25, 'd2_role': 0.5, 'd3_invertibility': 0.5,
                'd4_commutativity': 0.0, 'd5_meaning_count': 0.15,
                'd6_dependency_depth': 0.40, 'd7_closure': 1.0, 'd8_overloading': 0.20
            },
            "Logarithm base 10"
        )
        
        self.add_operator(
            'log₂', 'Binary Logarithm', 'Transcendental/Logarithmic',
            {
                'd1_arity': 0.25, 'd2_role': 0.5, 'd3_invertibility': 0.5,
                'd4_commutativity': 0.0, 'd5_meaning_count': 0.10,
                'd6_dependency_depth': 0.40, 'd7_closure': 1.0, 'd8_overloading': 0.10
            },
            "Logarithm base 2"
        )
        
        # Trigonometric
        self.add_operator(
            'sin', 'Sine', 'Transcendental/Trigonometric',
            {
                'd1_arity': 0.25, 'd2_role': 0.5, 'd3_invertibility': 0.5,
                'd4_commutativity': 0.0, 'd5_meaning_count': 0.10,
                'd6_dependency_depth': 0.35, 'd7_closure': 1.0, 'd8_overloading': 0.10
            },
            "Sine function"
        )
        
        self.add_operator(
            'cos', 'Cosine', 'Transcendental/Trigonometric',
            {
                'd1_arity': 0.25, 'd2_role': 0.5, 'd3_invertibility': 0.5,
                'd4_commutativity': 0.0, 'd5_meaning_count': 0.10,
                'd6_dependency_depth': 0.35, 'd7_closure': 1.0, 'd8_overloading': 0.10
            },
            "Cosine function"
        )
        
        self.add_operator(
            'tan', 'Tangent', 'Transcendental/Trigonometric',
            {
                'd1_arity': 0.25, 'd2_role': 0.5, 'd3_invertibility': 0.5,
                'd4_commutativity': 0.0, 'd5_meaning_count': 0.10,
                'd6_dependency_depth': 0.40, 'd7_closure': 0.5, 'd8_overloading': 0.10
            },
            "Tangent function (sin/cos)"
        )
        
        self.add_operator(
            'cot', 'Cotangent', 'Transcendental/Trigonometric',
            {
                'd1_arity': 0.25, 'd2_role': 0.5, 'd3_invertibility': 0.5,
                'd4_commutativity': 0.0, 'd5_meaning_count': 0.10,
                'd6_dependency_depth': 0.40, 'd7_closure': 0.5, 'd8_overloading': 0.10
            },
            "Cotangent function (cos/sin)"
        )
        
        self.add_operator(
            'sec', 'Secant', 'Transcendental/Trigonometric',
            {
                'd1_arity': 0.25, 'd2_role': 0.5, 'd3_invertibility': 0.5,
                'd4_commutativity': 0.0, 'd5_meaning_count': 0.10,
                'd6_dependency_depth': 0.40, 'd7_closure': 0.5, 'd8_overloading': 0.10
            },
            "Secant function (1/cos)"
        )
        
        self.add_operator(
            'csc', 'Cosecant', 'Transcendental/Trigonometric',
            {
                'd1_arity': 0.25, 'd2_role': 0.5, 'd3_invertibility': 0.5,
                'd4_commutativity': 0.0, 'd5_meaning_count': 0.10,
                'd6_dependency_depth': 0.40, 'd7_closure': 0.5, 'd8_overloading': 0.10
            },
            "Cosecant function (1/sin)"
        )
        
        # Inverse trigonometric
        self.add_operator(
            'arcsin', 'Arcsine', 'Transcendental/InverseTrig',
            {
                'd1_arity': 0.25, 'd2_role': 0.5, 'd3_invertibility': 0.5,
                'd4_commutativity': 0.0, 'd5_meaning_count': 0.15,
                'd6_dependency_depth': 0.45, 'd7_closure': 1.0, 'd8_overloading': 0.15
            },
            "Inverse sine"
        )
        
        self.add_operator(
            'arccos', 'Arccosine', 'Transcendental/InverseTrig',
            {
                'd1_arity': 0.25, 'd2_role': 0.5, 'd3_invertibility': 0.5,
                'd4_commutativity': 0.0, 'd5_meaning_count': 0.15,
                'd6_dependency_depth': 0.45, 'd7_closure': 1.0, 'd8_overloading': 0.15
            },
            "Inverse cosine"
        )
        
        self.add_operator(
            'arctan', 'Arctangent', 'Transcendental/InverseTrig',
            {
                'd1_arity': 0.25, 'd2_role': 0.5, 'd3_invertibility': 0.5,
                'd4_commutativity': 0.0, 'd5_meaning_count': 0.15,
                'd6_dependency_depth': 0.45, 'd7_closure': 1.0, 'd8_overloading': 0.15
            },
            "Inverse tangent"
        )
        
        # Hyperbolic
        self.add_operator(
            'sinh', 'Hyperbolic Sine', 'Transcendental/Hyperbolic',
            {
                'd1_arity': 0.25, 'd2_role': 0.5, 'd3_invertibility': 0.5,
                'd4_commutativity': 0.0, 'd5_meaning_count': 0.10,
                'd6_dependency_depth': 0.40, 'd7_closure': 1.0, 'd8_overloading': 0.10
            },
            "Hyperbolic sine"
        )
        
        self.add_operator(
            'cosh', 'Hyperbolic Cosine', 'Transcendental/Hyperbolic',
            {
                'd1_arity': 0.25, 'd2_role': 0.5, 'd3_invertibility': 0.5,
                'd4_commutativity': 0.0, 'd5_meaning_count': 0.10,
                'd6_dependency_depth': 0.40, 'd7_closure': 1.0, 'd8_overloading': 0.10
            },
            "Hyperbolic cosine"
        )
        
        self.add_operator(
            'tanh', 'Hyperbolic Tangent', 'Transcendental/Hyperbolic',
            {
                'd1_arity': 0.25, 'd2_role': 0.5, 'd3_invertibility': 0.5,
                'd4_commutativity': 0.0, 'd5_meaning_count': 0.10,
                'd6_dependency_depth': 0.45, 'd7_closure': 1.0, 'd8_overloading': 0.10
            },
            "Hyperbolic tangent"
        )
        
        # ================================================================
        # CATEGORY 4: COMPARISON AND RELATIONAL OPERATORS
        # ================================================================
        print("[4/15] Adding Comparison and Relational Operators...")
        
        self.add_operator(
            '=', 'Equality', 'Relational/Comparison',
            {
                'd1_arity': 0.5, 'd2_role': 0.25, 'd3_invertibility': 0.0,
                'd4_commutativity': 1.0, 'd5_meaning_count': 0.15,
                'd6_dependency_depth': 0.10, 'd7_closure': 1.0, 'd8_overloading': 0.30
            },
            "Test for equality"
        )
        
        self.add_operator(
            '≠', 'Inequality', 'Relational/Comparison',
            {
                'd1_arity': 0.5, 'd2_role': 0.25, 'd3_invertibility': 0.0,
                'd4_commutativity': 1.0, 'd5_meaning_count': 0.10,
                'd6_dependency_depth': 0.10, 'd7_closure': 1.0, 'd8_overloading': 0.15
            },
            "Test for inequality"
        )
        
        self.add_operator(
            '<', 'Less Than', 'Relational/Comparison',
            {
                'd1_arity': 0.5, 'd2_role': 0.25, 'd3_invertibility': 0.0,
                'd4_commutativity': 0.0, 'd5_meaning_count': 0.10,
                'd6_dependency_depth': 0.10, 'd7_closure': 1.0, 'd8_overloading': 0.20
            },
            "Test if less than"
        )
        
        self.add_operator(
            '>', 'Greater Than', 'Relational/Comparison',
            {
                'd1_arity': 0.5, 'd2_role': 0.25, 'd3_invertibility': 0.0,
                'd4_commutativity': 0.0, 'd5_meaning_count': 0.10,
                'd6_dependency_depth': 0.10, 'd7_closure': 1.0, 'd8_overloading': 0.20
            },
            "Test if greater than"
        )
        
        self.add_operator(
            '≤', 'Less Than or Equal', 'Relational/Comparison',
            {
                'd1_arity': 0.5, 'd2_role': 0.25, 'd3_invertibility': 0.0,
                'd4_commutativity': 0.0, 'd5_meaning_count': 0.10,
                'd6_dependency_depth': 0.15, 'd7_closure': 1.0, 'd8_overloading': 0.15
            },
            "Test if less than or equal"
        )
        
        self.add_operator(
            '≥', 'Greater Than or Equal', 'Relational/Comparison',
            {
                'd1_arity': 0.5, 'd2_role': 0.25, 'd3_invertibility': 0.0,
                'd4_commutativity': 0.0, 'd5_meaning_count': 0.10,
                'd6_dependency_depth': 0.15, 'd7_closure': 1.0, 'd8_overloading': 0.15
            },
            "Test if greater than or equal"
        )
        
        self.add_operator(
            '≈', 'Approximately Equal', 'Relational/Comparison',
            {
                'd1_arity': 0.5, 'd2_role': 0.25, 'd3_invertibility': 0.0,
                'd4_commutativity': 1.0, 'd5_meaning_count': 0.20,
                'd6_dependency_depth': 0.20, 'd7_closure': 1.0, 'd8_overloading': 0.25
            },
            "Test for approximate equality"
        )
        
        self.add_operator(
            '≡', 'Identical', 'Relational/Comparison',
            {
                'd1_arity': 0.5, 'd2_role': 0.25, 'd3_invertibility': 0.0,
                'd4_commutativity': 1.0, 'd5_meaning_count': 0.15,
                'd6_dependency_depth': 0.10, 'd7_closure': 1.0, 'd8_overloading': 0.20
            },
            "Test for identity (same object)"
        )
        
        # ================================================================
        # CATEGORY 5: SET THEORY OPERATORS
        # ================================================================
        print("[5/15] Adding Set Theory Operators...")
        
        self.add_operator(
            '∈', 'Element Of', 'SetTheory/Membership',
            {
                'd1_arity': 0.5, 'd2_role': 0.25, 'd3_invertibility': 0.0,
                'd4_commutativity': 0.0, 'd5_meaning_count': 0.10,
                'd6_dependency_depth': 0.10, 'd7_closure': 1.0, 'd8_overloading': 0.10
            },
            "Test set membership"
        )
        
        self.add_operator(
            '∉', 'Not Element Of', 'SetTheory/Membership',
            {
                'd1_arity': 0.5, 'd2_role': 0.25, 'd3_invertibility': 0.0,
                'd4_commutativity': 0.0, 'd5_meaning_count': 0.10,
                'd6_dependency_depth': 0.15, 'd7_closure': 1.0, 'd8_overloading': 0.10
            },
            "Test non-membership"
        )
        
        self.add_operator(
            '⊂', 'Proper Subset', 'SetTheory/Inclusion',
            {
                'd1_arity': 0.5, 'd2_role': 0.25, 'd3_invertibility': 0.0,
                'd4_commutativity': 0.0, 'd5_meaning_count': 0.10,
                'd6_dependency_depth': 0.15, 'd7_closure': 1.0, 'd8_overloading': 0.15
            },
            "Proper subset relation"
        )
        
        self.add_operator(
            '⊆', 'Subset', 'SetTheory/Inclusion',
            {
                'd1_arity': 0.5, 'd2_role': 0.25, 'd3_invertibility': 0.0,
                'd4_commutativity': 0.0, 'd5_meaning_count': 0.10,
                'd6_dependency_depth': 0.15, 'd7_closure': 1.0, 'd8_overloading': 0.15
            },
            "Subset or equal relation"
        )
        
        self.add_operator(
            '∪', 'Set Union', 'SetTheory/Operations',
            {
                'd1_arity': 0.5, 'd2_role': 0.5, 'd3_invertibility': 0.0,
                'd4_commutativity': 1.0, 'd5_meaning_count': 0.10,
                'd6_dependency_depth': 0.15, 'd7_closure': 1.0, 'd8_overloading': 0.15
            },
            "Set union (elements in either set)"
        )
        
        self.add_operator(
            '∩', 'Set Intersection', 'SetTheory/Operations',
            {
                'd1_arity': 0.5, 'd2_role': 0.5, 'd3_invertibility': 0.0,
                'd4_commutativity': 1.0, 'd5_meaning_count': 0.10,
                'd6_dependency_depth': 0.15, 'd7_closure': 1.0, 'd8_overloading': 0.15
            },
            "Set intersection (elements in both sets)"
        )
        
        self.add_operator(
            '∖', 'Set Difference', 'SetTheory/Operations',
            {
                'd1_arity': 0.5, 'd2_role': 0.5, 'd3_invertibility': 0.0,
                'd4_commutativity': 0.0, 'd5_meaning_count': 0.10,
                'd6_dependency_depth': 0.15, 'd7_closure': 1.0, 'd8_overloading': 0.15
            },
            "Set difference (elements in first but not second)"
        )
        
        self.add_operator(
            '△', 'Symmetric Difference', 'SetTheory/Operations',
            {
                'd1_arity': 0.5, 'd2_role': 0.5, 'd3_invertibility': 0.0,
                'd4_commutativity': 1.0, 'd5_meaning_count': 0.10,
                'd6_dependency_depth': 0.20, 'd7_closure': 1.0, 'd8_overloading': 0.15
            },
            "Symmetric difference (elements in one set but not both)"
        )
        
        self.add_operator(
            '×', 'Cartesian Product', 'SetTheory/Operations',
            {
                'd1_arity': 0.5, 'd2_role': 0.5, 'd3_invertibility': 0.0,
                'd4_commutativity': 0.0, 'd5_meaning_count': 0.15,
                'd6_dependency_depth': 0.20, 'd7_closure': 1.0, 'd8_overloading': 0.30
            },
            "Cartesian product of sets"
        )
        
        self.add_operator(
            '℘', 'Power Set', 'SetTheory/Operations',
            {
                'd1_arity': 0.25, 'd2_role': 0.5, 'd3_invertibility': 0.0,
                'd4_commutativity': 0.0, 'd5_meaning_count': 0.10,
                'd6_dependency_depth': 0.25, 'd7_closure': 1.0, 'd8_overloading': 0.10
            },
            "Set of all subsets"
        )
        
        # ================================================================
        # CATEGORY 6: QUANTUM OPERATORS
        # ================================================================
        print("[6/15] Adding Quantum Operators...")
        
        self.add_operator(
            'H', 'Hadamard Gate', 'Quantum/Gates',
            {
                'd1_arity': 0.25, 'd2_role': 0.5, 'd3_invertibility': 1.0,
                'd4_commutativity': 0.0, 'd5_meaning_count': 0.10,
                'd6_dependency_depth': 0.08, 'd7_closure': 1.0, 'd8_overloading': 0.10
            },
            "Create superposition (quantum)"
        )
        
        self.add_operator(
            'CNOT', 'Controlled-NOT', 'Quantum/Gates',
            {
                'd1_arity': 0.5, 'd2_role': 0.5, 'd3_invertibility': 1.0,
                'd4_commutativity': 0.0, 'd5_meaning_count': 0.10,
                'd6_dependency_depth': 0.12, 'd7_closure': 1.0, 'd8_overloading': 0.10
            },
            "Entanglement gate (quantum)"
        )
        
        self.add_operator(
            'P(θ)', 'Phase Gate', 'Quantum/Gates',
            {
                'd1_arity': 0.25, 'd2_role': 0.5, 'd3_invertibility': 0.5,
                'd4_commutativity': 0.0, 'd5_meaning_count': 0.15,
                'd6_dependency_depth': 0.10, 'd7_closure': 1.0, 'd8_overloading': 0.15
            },
            "Phase rotation (quantum)"
        )
        
        self.add_operator(
            'M', 'Measurement', 'Quantum/Measurement',
            {
                'd1_arity': 0.25, 'd2_role': 0.5, 'd3_invertibility': 0.0,
                'd4_commutativity': 0.0, 'd5_meaning_count': 0.20,
                'd6_dependency_depth': 0.15, 'd7_closure': 0.5, 'd8_overloading': 0.20
            },
            "Quantum measurement (collapse)"
        )
        
        self.add_operator(
            'X', 'Pauli-X', 'Quantum/Pauli',
            {
                'd1_arity': 0.25, 'd2_role': 0.5, 'd3_invertibility': 1.0,
                'd4_commutativity': 0.0, 'd5_meaning_count': 0.10,
                'd6_dependency_depth': 0.08, 'd7_closure': 1.0, 'd8_overloading': 0.15
            },
            "Bit-flip gate (quantum NOT)"
        )
        
        self.add_operator(
            'Y', 'Pauli-Y', 'Quantum/Pauli',
            {
                'd1_arity': 0.25, 'd2_role': 0.5, 'd3_invertibility': 1.0,
                'd4_commutativity': 0.0, 'd5_meaning_count': 0.10,
                'd6_dependency_depth': 0.08, 'd7_closure': 1.0, 'd8_overloading': 0.15
            },
            "Combined bit and phase flip"
        )
        
        self.add_operator(
            'Z', 'Pauli-Z', 'Quantum/Pauli',
            {
                'd1_arity': 0.25, 'd2_role': 0.5, 'd3_invertibility': 1.0,
                'd4_commutativity': 0.0, 'd5_meaning_count': 0.10,
                'd6_dependency_depth': 0.08, 'd7_closure': 1.0, 'd8_overloading': 0.15
            },
            "Phase-flip gate"
        )
        
        self.add_operator(
            'T', 'T Gate', 'Quantum/Gates',
            {
                'd1_arity': 0.25, 'd2_role': 0.5, 'd3_invertibility': 0.5,
                'd4_commutativity': 0.0, 'd5_meaning_count': 0.10,
                'd6_dependency_depth': 0.10, 'd7_closure': 1.0, 'd8_overloading': 0.10
            },
            "π/8 phase gate"
        )
        
        self.add_operator(
            'S', 'S Gate', 'Quantum/Gates',
            {
                'd1_arity': 0.25, 'd2_role': 0.5, 'd3_invertibility': 0.5,
                'd4_commutativity': 0.0, 'd5_meaning_count': 0.10,
                'd6_dependency_depth': 0.10, 'd7_closure': 1.0, 'd8_overloading': 0.15
            },
            "π/4 phase gate"
        )
        
        self.add_operator(
            'SWAP', 'Swap Gate', 'Quantum/Gates',
            {
                'd1_arity': 0.5, 'd2_role': 0.5, 'd3_invertibility': 1.0,
                'd4_commutativity': 1.0, 'd5_meaning_count': 0.10,
                'd6_dependency_depth': 0.15, 'd7_closure': 1.0, 'd8_overloading': 0.15
            },
            "Swap two qubits"
        )
        
        # ================================================================
        # CATEGORY 7: CALCULUS OPERATORS
        # ================================================================
        print("[7/15] Adding Calculus Operators...")
        
        self.add_operator(
            'd/dx', 'Derivative', 'Calculus/Differential',
            {
                'd1_arity': 0.25, 'd2_role': 0.5, 'd3_invertibility': 0.5,
                'd4_commutativity': 0.0, 'd5_meaning_count': 0.10,
                'd6_dependency_depth': 0.30, 'd7_closure': 1.0, 'd8_overloading': 0.15
            },
            "Differentiation operator"
        )
        
        self.add_operator(
            '∫', 'Integral', 'Calculus/Integral',
            {
                'd1_arity': 0.25, 'd2_role': 0.5, 'd3_invertibility': 0.5,
                'd4_commutativity': 0.0, 'd5_meaning_count': 0.15,
                'd6_dependency_depth': 0.35, 'd7_closure': 1.0, 'd8_overloading': 0.20
            },
            "Integration operator"
        )
        
        self.add_operator(
            '∂/∂x', 'Partial Derivative', 'Calculus/Differential',
            {
                'd1_arity': 0.25, 'd2_role': 0.5, 'd3_invertibility': 0.5,
                'd4_commutativity': 0.0, 'd5_meaning_count': 0.15,
                'd6_dependency_depth': 0.35, 'd7_closure': 1.0, 'd8_overloading': 0.15
            },
            "Partial differentiation"
        )
        
        self.add_operator(
            '∇', 'Gradient', 'Calculus/VectorCalculus',
            {
                'd1_arity': 0.25, 'd2_role': 0.5, 'd3_invertibility': 0.0,
                'd4_commutativity': 0.0, 'd5_meaning_count': 0.10,
                'd6_dependency_depth': 0.40, 'd7_closure': 1.0, 'd8_overloading': 0.20
            },
            "Gradient operator (vector of partial derivatives)"
        )
        
        self.add_operator(
            '∇·', 'Divergence', 'Calculus/VectorCalculus',
            {
                'd1_arity': 0.25, 'd2_role': 0.5, 'd3_invertibility': 0.0,
                'd4_commutativity': 0.0, 'd5_meaning_count': 0.10,
                'd6_dependency_depth': 0.45, 'd7_closure': 1.0, 'd8_overloading': 0.15
            },
            "Divergence operator"
        )
        
        self.add_operator(
            '∇×', 'Curl', 'Calculus/VectorCalculus',
            {
                'd1_arity': 0.25, 'd2_role': 0.5, 'd3_invertibility': 0.0,
                'd4_commutativity': 0.0, 'd5_meaning_count': 0.10,
                'd6_dependency_depth': 0.45, 'd7_closure': 1.0, 'd8_overloading': 0.15
            },
            "Curl operator"
        )
        
        self.add_operator(
            '∇²', 'Laplacian', 'Calculus/VectorCalculus',
            {
                'd1_arity': 0.25, 'd2_role': 0.5, 'd3_invertibility': 0.0,
                'd4_commutativity': 0.0, 'd5_meaning_count': 0.10,
                'd6_dependency_depth': 0.50, 'd7_closure': 1.0, 'd8_overloading': 0.15
            },
            "Laplacian operator (divergence of gradient)"
        )
        
        self.add_operator(
            'lim', 'Limit', 'Calculus/Limits',
            {
                'd1_arity': 0.25, 'd2_role': 0.5, 'd3_invertibility': 0.0,
                'd4_commutativity': 0.0, 'd5_meaning_count': 0.15,
                'd6_dependency_depth': 0.30, 'd7_closure': 1.0, 'd8_overloading': 0.20
            },
            "Limit operator"
        )
        
        # ================================================================
        # CATEGORY 8: LINEAR ALGEBRA OPERATORS
        # ================================================================
        print("[8/15] Adding Linear Algebra Operators...")
        
        self.add_operator(
            '·', 'Dot Product', 'LinearAlgebra/Products',
            {
                'd1_arity': 0.5, 'd2_role': 0.5, 'd3_invertibility': 0.0,
                'd4_commutativity': 1.0, 'd5_meaning_count': 0.15,
                'd6_dependency_depth': 0.20, 'd7_closure': 1.0, 'd8_overloading': 0.25
            },
            "Dot product (inner product)"
        )
        
        self.add_operator(
            '×', 'Cross Product', 'LinearAlgebra/Products',
            {
                'd1_arity': 0.5, 'd2_role': 0.5, 'd3_invertibility': 0.0,
                'd4_commutativity': 0.0, 'd5_meaning_count': 0.15,
                'd6_dependency_depth': 0.25, 'd7_closure': 1.0, 'd8_overloading': 0.35
            },
            "Cross product (vector product)"
        )
        
        self.add_operator(
            '⊗', 'Tensor Product', 'LinearAlgebra/Products',
            {
                'd1_arity': 0.5, 'd2_role': 0.5, 'd3_invertibility': 0.0,
                'd4_commutativity': 0.0, 'd5_meaning_count': 0.10,
                'd6_dependency_depth': 0.30, 'd7_closure': 1.0, 'd8_overloading': 0.20
            },
            "Tensor product (outer product)"
        )
        
        self.add_operator(
            'det', 'Determinant', 'LinearAlgebra/MatrixOps',
            {
                'd1_arity': 0.25, 'd2_role': 0.5, 'd3_invertibility': 0.0,
                'd4_commutativity': 0.0, 'd5_meaning_count': 0.10,
                'd6_dependency_depth': 0.35, 'd7_closure': 1.0, 'd8_overloading': 0.10
            },
            "Matrix determinant"
        )
        
        self.add_operator(
            'tr', 'Trace', 'LinearAlgebra/MatrixOps',
            {
                'd1_arity': 0.25, 'd2_role': 0.5, 'd3_invertibility': 0.0,
                'd4_commutativity': 0.0, 'd5_meaning_count': 0.10,
                'd6_dependency_depth': 0.20, 'd7_closure': 1.0, 'd8_overloading': 0.15
            },
            "Matrix trace (sum of diagonal)"
        )
        
        self.add_operator(
            '⁻¹', 'Matrix Inverse', 'LinearAlgebra/MatrixOps',
            {
                'd1_arity': 0.25, 'd2_role': 0.5, 'd3_invertibility': 0.5,
                'd4_commutativity': 0.0, 'd5_meaning_count': 0.10,
                'd6_dependency_depth': 0.40, 'd7_closure': 0.5, 'd8_overloading': 0.20
            },
            "Matrix inverse"
        )
        
        self.add_operator(
            'ᵀ', 'Transpose', 'LinearAlgebra/MatrixOps',
            {
                'd1_arity': 0.25, 'd2_role': 0.5, 'd3_invertibility': 1.0,
                'd4_commutativity': 0.0, 'd5_meaning_count': 0.10,
                'd6_dependency_depth': 0.15, 'd7_closure': 1.0, 'd8_overloading': 0.15
            },
            "Matrix transpose"
        )
        
        self.add_operator(
            '†', 'Conjugate Transpose', 'LinearAlgebra/MatrixOps',
            {
                'd1_arity': 0.25, 'd2_role': 0.5, 'd3_invertibility': 1.0,
                'd4_commutativity': 0.0, 'd5_meaning_count': 0.10,
                'd6_dependency_depth': 0.20, 'd7_closure': 1.0, 'd8_overloading': 0.15
            },
            "Hermitian conjugate (adjoint)"
        )
        
        self.add_operator(
            '‖·‖', 'Norm', 'LinearAlgebra/Norms',
            {
                'd1_arity': 0.25, 'd2_role': 0.5, 'd3_invertibility': 0.0,
                'd4_commutativity': 0.0, 'd5_meaning_count': 0.20,
                'd6_dependency_depth': 0.25, 'd7_closure': 1.0, 'd8_overloading': 0.30
            },
            "Vector/matrix norm"
        )
        
        # ================================================================
        # CATEGORY 9: STATISTICAL OPERATORS
        # ================================================================
        print("[9/15] Adding Statistical Operators...")
        
        self.add_operator(
            'E[X]', 'Expected Value', 'Statistics/Moments',
            {
                'd1_arity': 0.25, 'd2_role': 0.5, 'd3_invertibility': 0.0,
                'd4_commutativity': 0.0, 'd5_meaning_count': 0.15,
                'd6_dependency_depth': 0.30, 'd7_closure': 1.0, 'd8_overloading': 0.20
            },
            "Expected value (mean)"
        )
        
        self.add_operator(
            'Var[X]', 'Variance', 'Statistics/Moments',
            {
                'd1_arity': 0.25, 'd2_role': 0.5, 'd3_invertibility': 0.0,
                'd4_commutativity': 0.0, 'd5_meaning_count': 0.10,
                'd6_dependency_depth': 0.35, 'd7_closure': 1.0, 'd8_overloading': 0.15
            },
            "Variance"
        )
        
        self.add_operator(
            'σ', 'Standard Deviation', 'Statistics/Moments',
            {
                'd1_arity': 0.25, 'd2_role': 0.5, 'd3_invertibility': 0.0,
                'd4_commutativity': 0.0, 'd5_meaning_count': 0.10,
                'd6_dependency_depth': 0.40, 'd7_closure': 1.0, 'd8_overloading': 0.20
            },
            "Standard deviation"
        )
        
        self.add_operator(
            'Cov[X,Y]', 'Covariance', 'Statistics/Correlation',
            {
                'd1_arity': 0.5, 'd2_role': 0.5, 'd3_invertibility': 0.0,
                'd4_commutativity': 1.0, 'd5_meaning_count': 0.10,
                'd6_dependency_depth': 0.40, 'd7_closure': 1.0, 'd8_overloading': 0.15
            },
            "Covariance"
        )
        
        self.add_operator(
            'ρ', 'Correlation', 'Statistics/Correlation',
            {
                'd1_arity': 0.5, 'd2_role': 0.5, 'd3_invertibility': 0.0,
                'd4_commutativity': 1.0, 'd5_meaning_count': 0.15,
                'd6_dependency_depth': 0.45, 'd7_closure': 1.0, 'd8_overloading': 0.25
            },
            "Correlation coefficient"
        )
        
        # ================================================================
        # CATEGORY 10: BITWISE OPERATORS
        # ================================================================
        print("[10/15] Adding Bitwise Operators...")
        
        self.add_operator(
            '&', 'Bitwise AND', 'Bitwise/Logical',
            {
                'd1_arity': 0.5, 'd2_role': 0.5, 'd3_invertibility': 0.0,
                'd4_commutativity': 1.0, 'd5_meaning_count': 0.15,
                'd6_dependency_depth': 0.10, 'd7_closure': 1.0, 'd8_overloading': 0.25
            },
            "Bitwise AND operation"
        )
        
        self.add_operator(
            '|', 'Bitwise OR', 'Bitwise/Logical',
            {
                'd1_arity': 0.5, 'd2_role': 0.5, 'd3_invertibility': 0.0,
                'd4_commutativity': 1.0, 'd5_meaning_count': 0.15,
                'd6_dependency_depth': 0.10, 'd7_closure': 1.0, 'd8_overloading': 0.25
            },
            "Bitwise OR operation"
        )
        
        self.add_operator(
            '~', 'Bitwise NOT', 'Bitwise/Logical',
            {
                'd1_arity': 0.25, 'd2_role': 0.5, 'd3_invertibility': 1.0,
                'd4_commutativity': 0.0, 'd5_meaning_count': 0.15,
                'd6_dependency_depth': 0.10, 'd7_closure': 1.0, 'd8_overloading': 0.20
            },
            "Bitwise NOT (complement)"
        )
        
        self.add_operator(
            '^', 'Bitwise XOR', 'Bitwise/Logical',
            {
                'd1_arity': 0.5, 'd2_role': 0.5, 'd3_invertibility': 0.5,
                'd4_commutativity': 1.0, 'd5_meaning_count': 0.15,
                'd6_dependency_depth': 0.10, 'd7_closure': 1.0, 'd8_overloading': 0.30
            },
            "Bitwise XOR operation"
        )
        
        self.add_operator(
            '<<', 'Left Shift', 'Bitwise/Shift',
            {
                'd1_arity': 0.5, 'd2_role': 0.5, 'd3_invertibility': 0.5,
                'd4_commutativity': 0.0, 'd5_meaning_count': 0.10,
                'd6_dependency_depth': 0.15, 'd7_closure': 1.0, 'd8_overloading': 0.15
            },
            "Left bit shift"
        )
        
        self.add_operator(
            '>>', 'Right Shift', 'Bitwise/Shift',
            {
                'd1_arity': 0.5, 'd2_role': 0.5, 'd3_invertibility': 0.5,
                'd4_commutativity': 0.0, 'd5_meaning_count': 0.10,
                'd6_dependency_depth': 0.15, 'd7_closure': 1.0, 'd8_overloading': 0.15
            },
            "Right bit shift"
        )
        
        # ================================================================
        # CATEGORY 11: COMBINATORIAL OPERATORS
        # ================================================================
        print("[11/15] Adding Combinatorial Operators...")
        
        self.add_operator(
            '!', 'Factorial', 'Combinatorial/Counting',
            {
                'd1_arity': 0.25, 'd2_role': 0.5, 'd3_invertibility': 0.0,
                'd4_commutativity': 0.0, 'd5_meaning_count': 0.10,
                'd6_dependency_depth': 0.30, 'd7_closure': 1.0, 'd8_overloading': 0.15
            },
            "Factorial (n!)"
        )
        
        self.add_operator(
            'C(n,k)', 'Binomial Coefficient', 'Combinatorial/Counting',
            {
                'd1_arity': 0.5, 'd2_role': 0.5, 'd3_invertibility': 0.0,
                'd4_commutativity': 0.0, 'd5_meaning_count': 0.15,
                'd6_dependency_depth': 0.40, 'd7_closure': 1.0, 'd8_overloading': 0.20
            },
            "Binomial coefficient (n choose k)"
        )
        
        self.add_operator(
            'P(n,k)', 'Permutation', 'Combinatorial/Counting',
            {
                'd1_arity': 0.5, 'd2_role': 0.5, 'd3_invertibility': 0.0,
                'd4_commutativity': 0.0, 'd5_meaning_count': 0.10,
                'd6_dependency_depth': 0.35, 'd7_closure': 1.0, 'd8_overloading': 0.20
            },
            "Permutation (n permute k)"
        )
        
        # ================================================================
        # CATEGORY 12: SPECIAL FUNCTIONS
        # ================================================================
        print("[12/15] Adding Special Functions...")
        
        self.add_operator(
            'Γ', 'Gamma Function', 'SpecialFunctions/Gamma',
            {
                'd1_arity': 0.25, 'd2_role': 0.5, 'd3_invertibility': 0.0,
                'd4_commutativity': 0.0, 'd5_meaning_count': 0.10,
                'd6_dependency_depth': 0.50, 'd7_closure': 1.0, 'd8_overloading': 0.10
            },
            "Gamma function (generalized factorial)"
        )
        
        self.add_operator(
            'ζ', 'Riemann Zeta', 'SpecialFunctions/Zeta',
            {
                'd1_arity': 0.25, 'd2_role': 0.5, 'd3_invertibility': 0.0,
                'd4_commutativity': 0.0, 'd5_meaning_count': 0.10,
                'd6_dependency_depth': 0.60, 'd7_closure': 1.0, 'd8_overloading': 0.10
            },
            "Riemann zeta function"
        )
        
        self.add_operator(
            'erf', 'Error Function', 'SpecialFunctions/Error',
            {
                'd1_arity': 0.25, 'd2_role': 0.5, 'd3_invertibility': 0.0,
                'd4_commutativity': 0.0, 'd5_meaning_count': 0.10,
                'd6_dependency_depth': 0.45, 'd7_closure': 1.0, 'd8_overloading': 0.10
            },
            "Error function"
        )
        
        self.add_operator(
            'J_n', 'Bessel Function', 'SpecialFunctions/Bessel',
            {
                'd1_arity': 0.5, 'd2_role': 0.5, 'd3_invertibility': 0.0,
                'd4_commutativity': 0.0, 'd5_meaning_count': 0.15,
                'd6_dependency_depth': 0.55, 'd7_closure': 1.0, 'd8_overloading': 0.15
            },
            "Bessel function of the first kind"
        )
        
        # ================================================================
        # CATEGORY 13: LOGICAL QUANTIFIERS
        # ================================================================
        print("[13/15] Adding Logical Quantifiers...")
        
        self.add_operator(
            '∀', 'Universal Quantifier', 'Logic/Quantifiers',
            {
                'd1_arity': 0.25, 'd2_role': 0.75, 'd3_invertibility': 0.0,
                'd4_commutativity': 0.0, 'd5_meaning_count': 0.10,
                'd6_dependency_depth': 0.20, 'd7_closure': 1.0, 'd8_overloading': 0.10
            },
            "For all (universal quantifier)"
        )
        
        self.add_operator(
            '∃', 'Existential Quantifier', 'Logic/Quantifiers',
            {
                'd1_arity': 0.25, 'd2_role': 0.75, 'd3_invertibility': 0.0,
                'd4_commutativity': 0.0, 'd5_meaning_count': 0.10,
                'd6_dependency_depth': 0.20, 'd7_closure': 1.0, 'd8_overloading': 0.10
            },
            "There exists (existential quantifier)"
        )
        
        self.add_operator(
            '→', 'Implication', 'Logic/Connectives',
            {
                'd1_arity': 0.5, 'd2_role': 0.5, 'd3_invertibility': 0.0,
                'd4_commutativity': 0.0, 'd5_meaning_count': 0.15,
                'd6_dependency_depth': 0.15, 'd7_closure': 1.0, 'd8_overloading': 0.25
            },
            "Logical implication (if...then)"
        )
        
        self.add_operator(
            '↔', 'Biconditional', 'Logic/Connectives',
            {
                'd1_arity': 0.5, 'd2_role': 0.5, 'd3_invertibility': 0.0,
                'd4_commutativity': 1.0, 'd5_meaning_count': 0.10,
                'd6_dependency_depth': 0.20, 'd7_closure': 1.0, 'd8_overloading': 0.15
            },
            "Logical equivalence (if and only if)"
        )
        
        # ================================================================
        # CATEGORY 14: NOVEL UBP OPERATORS (From Study 3)
        # ================================================================
        print("[14/15] Adding Novel UBP Operators...")
        
        self.add_operator(
            'HARMONIZE', 'Harmonize', 'Novel/UBP',
            {
                'd1_arity': 0.5, 'd2_role': 0.5, 'd3_invertibility': 0.5,
                'd4_commutativity': 1.0, 'd5_meaning_count': 0.10,
                'd6_dependency_depth': 0.08, 'd7_closure': 1.0, 'd8_overloading': 0.08
            },
            "Geometric mean with Y-scaling for robust smoothing"
        )
        
        self.add_operator(
            'RESONATE', 'Resonate', 'Novel/UBP',
            {
                'd1_arity': 0.5, 'd2_role': 0.5, 'd3_invertibility': 0.5,
                'd4_commutativity': 1.0, 'd5_meaning_count': 0.10,
                'd6_dependency_depth': 0.09, 'd7_closure': 1.0, 'd8_overloading': 0.08
            },
            "Phase alignment operator for signal processing"
        )
        
        self.add_operator(
            'COHERE', 'Cohere', 'Novel/UBP',
            {
                'd1_arity': 0.25, 'd2_role': 0.5, 'd3_invertibility': 0.0,
                'd4_commutativity': 0.0, 'd5_meaning_count': 0.10,
                'd6_dependency_depth': 0.07, 'd7_closure': 1.0, 'd8_overloading': 0.08
            },
            "Coherence maximization for error correction"
        )
        
        self.add_operator(
            'STABILIZE', 'Stabilize', 'Novel/UBP',
            {
                'd1_arity': 0.25, 'd2_role': 0.5, 'd3_invertibility': 0.5,
                'd4_commutativity': 0.0, 'd5_meaning_count': 0.10,
                'd6_dependency_depth': 0.10, 'd7_closure': 1.0, 'd8_overloading': 0.08
            },
            "Geometric restoration for numerical stability"
        )
        
        self.add_operator(
            'BIFURCATE', 'Bifurcate', 'Novel/UBP',
            {
                'd1_arity': 0.25, 'd2_role': 0.5, 'd3_invertibility': 0.0,
                'd4_commutativity': 0.0, 'd5_meaning_count': 0.10,
                'd6_dependency_depth': 0.08, 'd7_closure': 1.0, 'd8_overloading': 0.08
            },
            "Binary branching with coherence preservation"
        )
        
        # ================================================================
        # CATEGORY 15: ADDITIONAL OPERATORS TO REACH 200+
        # ================================================================
        print("[15/15] Adding Additional Operators...")
        
        # More logical operators
        self.add_operator(
            'NAND', 'NAND', 'Derived/Logical',
            {
                'd1_arity': 0.5, 'd2_role': 0.5, 'd3_invertibility': 0.0,
                'd4_commutativity': 1.0, 'd5_meaning_count': 0.10,
                'd6_dependency_depth': 0.15, 'd7_closure': 1.0, 'd8_overloading': 0.10
            },
            "NOT AND (universal gate)"
        )
        
        self.add_operator(
            'NOR', 'NOR', 'Derived/Logical',
            {
                'd1_arity': 0.5, 'd2_role': 0.5, 'd3_invertibility': 0.0,
                'd4_commutativity': 1.0, 'd5_meaning_count': 0.10,
                'd6_dependency_depth': 0.15, 'd7_closure': 1.0, 'd8_overloading': 0.10
            },
            "NOT OR (universal gate)"
        )
        
        # String/sequence operators
        self.add_operator(
            '++', 'Concatenation', 'String/Operations',
            {
                'd1_arity': 0.5, 'd2_role': 0.5, 'd3_invertibility': 0.0,
                'd4_commutativity': 0.0, 'd5_meaning_count': 0.15,
                'd6_dependency_depth': 0.15, 'd7_closure': 1.0, 'd8_overloading': 0.25
            },
            "String/sequence concatenation"
        )
        
        # More arithmetic
        self.add_operator(
            'gcd', 'Greatest Common Divisor', 'NumberTheory/Divisibility',
            {
                'd1_arity': 0.5, 'd2_role': 0.5, 'd3_invertibility': 0.0,
                'd4_commutativity': 1.0, 'd5_meaning_count': 0.10,
                'd6_dependency_depth': 0.30, 'd7_closure': 1.0, 'd8_overloading': 0.10
            },
            "Greatest common divisor"
        )
        
        self.add_operator(
            'lcm', 'Least Common Multiple', 'NumberTheory/Divisibility',
            {
                'd1_arity': 0.5, 'd2_role': 0.5, 'd3_invertibility': 0.0,
                'd4_commutativity': 1.0, 'd5_meaning_count': 0.10,
                'd6_dependency_depth': 0.30, 'd7_closure': 1.0, 'd8_overloading': 0.10
            },
            "Least common multiple"
        )
        
        # Aggregate operators
        self.add_operator(
            'Σ', 'Summation', 'Aggregate/Reduction',
            {
                'd1_arity': 0.25, 'd2_role': 0.5, 'd3_invertibility': 0.0,
                'd4_commutativity': 0.0, 'd5_meaning_count': 0.10,
                'd6_dependency_depth': 0.20, 'd7_closure': 1.0, 'd8_overloading': 0.20
            },
            "Summation over sequence"
        )
        
        self.add_operator(
            'Π', 'Product', 'Aggregate/Reduction',
            {
                'd1_arity': 0.25, 'd2_role': 0.5, 'd3_invertibility': 0.0,
                'd4_commutativity': 0.0, 'd5_meaning_count': 0.10,
                'd6_dependency_depth': 0.25, 'd7_closure': 1.0, 'd8_overloading': 0.20
            },
            "Product over sequence"
        )
        
        self.add_operator(
            'max', 'Maximum', 'Aggregate/Selection',
            {
                'd1_arity': 0.5, 'd2_role': 0.5, 'd3_invertibility': 0.0,
                'd4_commutativity': 1.0, 'd5_meaning_count': 0.10,
                'd6_dependency_depth': 0.15, 'd7_closure': 1.0, 'd8_overloading': 0.15
            },
            "Maximum of values"
        )
        
        self.add_operator(
            'min', 'Minimum', 'Aggregate/Selection',
            {
                'd1_arity': 0.5, 'd2_role': 0.5, 'd3_invertibility': 0.0,
                'd4_commutativity': 1.0, 'd5_meaning_count': 0.10,
                'd6_dependency_depth': 0.15, 'd7_closure': 1.0, 'd8_overloading': 0.15
            },
            "Minimum of values"
        )
        
        # Complex number operators
        self.add_operator(
            'Re', 'Real Part', 'Complex/Components',
            {
                'd1_arity': 0.25, 'd2_role': 0.5, 'd3_invertibility': 0.0,
                'd4_commutativity': 0.0, 'd5_meaning_count': 0.10,
                'd6_dependency_depth': 0.10, 'd7_closure': 1.0, 'd8_overloading': 0.10
            },
            "Real part of complex number"
        )
        
        self.add_operator(
            'Im', 'Imaginary Part', 'Complex/Components',
            {
                'd1_arity': 0.25, 'd2_role': 0.5, 'd3_invertibility': 0.0,
                'd4_commutativity': 0.0, 'd5_meaning_count': 0.10,
                'd6_dependency_depth': 0.10, 'd7_closure': 1.0, 'd8_overloading': 0.10
            },
            "Imaginary part of complex number"
        )
        
        self.add_operator(
            'arg', 'Argument', 'Complex/Polar',
            {
                'd1_arity': 0.25, 'd2_role': 0.5, 'd3_invertibility': 0.0,
                'd4_commutativity': 0.0, 'd5_meaning_count': 0.15,
                'd6_dependency_depth': 0.25, 'd7_closure': 1.0, 'd8_overloading': 0.20
            },
            "Argument (phase angle) of complex number"
        )
        
        self.add_operator(
            'conj', 'Complex Conjugate', 'Complex/Operations',
            {
                'd1_arity': 0.25, 'd2_role': 0.5, 'd3_invertibility': 1.0,
                'd4_commutativity': 0.0, 'd5_meaning_count': 0.10,
                'd6_dependency_depth': 0.15, 'd7_closure': 1.0, 'd8_overloading': 0.10
            },
            "Complex conjugate"
        )
        
        print(f"\nDataset complete! Total operators: {len(self.operators)}")
        
        return self.operators
    
    def save_dataset(self, filename="/home/ubuntu/massive_operator_dataset.json"):
        """Save the dataset to JSON file."""
        with open(filename, 'w') as f:
            json.dump(self.operators, f, indent=2, default=str)
        print(f"\nDataset saved to: {filename}")
    
    def generate_summary_statistics(self):
        """Generate summary statistics about the dataset."""
        print("\n" + "="*70)
        print("DATASET SUMMARY STATISTICS")
        print("="*70)
        
        # Total count
        print(f"\nTotal Operators: {len(self.operators)}")
        
        # By category
        categories = defaultdict(int)
        for op in self.operators:
            categories[op['category']] += 1
        
        print(f"\nOperators by Category:")
        for cat, count in sorted(categories.items(), key=lambda x: x[1], reverse=True):
            print(f"  {cat:<40} {count:>3}")
        
        # Primitive vs Derived
        primitives = sum(1 for op in self.operators if op['is_primitive'])
        derived = len(self.operators) - primitives
        
        print(f"\nPrimitive vs Derived:")
        print(f"  Primitive: {primitives} ({100*primitives/len(self.operators):.1f}%)")
        print(f"  Derived:   {derived} ({100*derived/len(self.operators):.1f}%)")
        
        # NRCI distribution
        nrcis = [op['predicted_nrci'] for op in self.operators]
        print(f"\nNRCI Distribution:")
        print(f"  Min:  {min(nrcis):.10f}")
        print(f"  Max:  {max(nrcis):.10f}")
        print(f"  Mean: {sum(nrcis)/len(nrcis):.10f}")
        
        # D6 distribution
        d6s = [op['d_variables']['d6_dependency_depth'] for op in self.operators]
        print(f"\nD6 (Dependency Depth) Distribution:")
        print(f"  Min:  {min(d6s):.4f}")
        print(f"  Max:  {max(d6s):.4f}")
        print(f"  Mean: {sum(d6s)/len(d6s):.4f}")
        
        # Hamming weight distribution
        hws = [op['hamming_weight'] for op in self.operators]
        print(f"\nHamming Weight Distribution:")
        print(f"  Min:  {min(hws)}")
        print(f"  Max:  {max(hws)}")
        print(f"  Mean: {sum(hws)/len(hws):.2f}")
        
        # Layer imbalance distribution
        imbalances = [op['layer_imbalance'] for op in self.operators]
        print(f"\nLayer Imbalance Distribution:")
        print(f"  Min:  {min(imbalances)}")
        print(f"  Max:  {max(imbalances)}")
        print(f"  Mean: {sum(imbalances)/len(imbalances):.2f}")


if __name__ == "__main__":
    builder = MassiveOperatorDatasetBuilder()
    
    print("="*70)
    print("MASSIVE OPERATOR DATASET BUILDER")
    print("="*70)
    print("\nBuilding comprehensive dataset of 200+ operators...")
    print("This will take a few moments...")
    
    # Build the dataset
    operators = builder.build_comprehensive_dataset()
    
    # Save to file
    builder.save_dataset()
    
    # Generate summary statistics
    builder.generate_summary_statistics()
    
    print("\n" + "="*70)
    print("DATASET BUILD COMPLETE")
    print("="*70)
    print(f"\nNext steps:")
    print(f"  1. Analyze bitfield patterns across all {len(operators)} operators")
    print(f"  2. Identify operator families and taxonomic structure")
    print(f"  3. Build comprehensive visualizations")
    print(f"  4. Design periodic table layout")
