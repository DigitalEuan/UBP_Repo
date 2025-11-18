#!/usr/bin/env python3.11
"""
Generate comprehensive mathematical symbol dataset for UBP study.
This script creates a dataset of 200+ symbols with complete metadata.
"""

import json
from typing import List, Dict

def create_symbol_entry(
    symbol: str,
    unicode: str,
    latex: str,
    name: str,
    category: str,
    arity: str,
    formal_role: str,
    meaning_count: int,
    dependency_depth: int,
    invertibility: str,
    commutativity: str,
    associativity: str,
    identity_exists: str,
    inverse_exists: str,
    closure_degree: str,
    overloading_contexts: List[str]
) -> Dict:
    """Create a symbol entry with all required metadata."""
    return {
        "symbol": symbol,
        "unicode": unicode,
        "latex": latex,
        "name": name,
        "category": category,
        "arity": arity,
        "formal_role": formal_role,
        "meaning_count": meaning_count,
        "dependency_depth": dependency_depth,
        "invertibility": invertibility,
        "commutativity": commutativity,
        "associativity": associativity,
        "identity_exists": identity_exists,
        "inverse_exists": inverse_exists,
        "closure_degree": closure_degree,
        "overloading_contexts": overloading_contexts
    }

def generate_dataset() -> List[Dict]:
    """Generate the complete symbol dataset."""
    symbols = []
    
    # ARITHMETIC OPERATORS
    symbols.extend([
        create_symbol_entry("+", "U+002B", "+", "plus", "arithmetic", "binary", "operator", 2, 2, "full", "yes", "yes", "yes", "full", "high", ["arithmetic", "vector", "matrix", "set_union", "complex", "modular"]),
        create_symbol_entry("−", "U+2212", "-", "minus", "arithmetic", "binary", "operator", 2, 2, "full", "no", "no", "yes", "full", "high", ["arithmetic", "vector", "matrix", "set_difference", "complex"]),
        create_symbol_entry("×", "U+00D7", "\\times", "times", "arithmetic", "binary", "operator", 2, 2, "partial", "yes", "yes", "yes", "partial", "high", ["arithmetic", "vector_cross", "matrix", "cartesian_product", "complex"]),
        create_symbol_entry("÷", "U+00F7", "\\div", "divide", "arithmetic", "binary", "operator", 1, 2, "partial", "no", "no", "yes", "partial", "medium", ["arithmetic", "field_division"]),
        create_symbol_entry("√", "U+221A", "\\sqrt", "square_root", "arithmetic", "unary", "operator", 2, 3, "partial", "no", "no", "no", "partial", "medium", ["real", "complex", "matrix"]),
        create_symbol_entry("∑", "U+2211", "\\sum", "summation", "arithmetic", "unary", "operator", 1, 1, "none", "yes", "yes", "yes", "none", "high", ["series", "finite_sum"]),
        create_symbol_entry("∏", "U+220F", "\\prod", "product", "arithmetic", "unary", "operator", 1, 1, "none", "yes", "yes", "yes", "none", "high", ["series", "finite_product"]),
        create_symbol_entry("⌈", "U+2308", "\\lceil", "ceiling", "arithmetic", "unary", "operator", 1, 2, "none", "no", "no", "no", "none", "medium", ["ceiling_function"]),
        create_symbol_entry("⌊", "U+230A", "\\lfloor", "floor", "arithmetic", "unary", "operator", 1, 2, "none", "no", "no", "no", "none", "medium", ["floor_function"]),
        create_symbol_entry("!", "U+0021", "!", "factorial", "arithmetic", "unary", "operator", 2, 3, "none", "no", "no", "no", "none", "high", ["factorial", "logical_not"]),
        create_symbol_entry("mod", "U+006D", "\\bmod", "modulo", "arithmetic", "binary", "operator", 1, 2, "none", "no", "no", "no", "none", "high", ["modulo"]),
        create_symbol_entry("gcd", "U+0067", "\\gcd", "greatest_common_divisor", "arithmetic", "binary", "operator", 1, 2, "none", "yes", "yes", "no", "none", "high", ["gcd"]),
        create_symbol_entry("lcm", "U+006C", "\\text{lcm}", "least_common_multiple", "arithmetic", "binary", "operator", 1, 2, "none", "yes", "yes", "no", "none", "high", ["lcm"]),
        create_symbol_entry("max", "U+006D", "\\max", "maximum", "arithmetic", "binary", "operator", 1, 2, "none", "yes", "yes", "no", "none", "high", ["maximum"]),
        create_symbol_entry("min", "U+006D", "\\min", "minimum", "arithmetic", "binary", "operator", 1, 2, "none", "yes", "yes", "no", "none", "high", ["minimum"]),
        create_symbol_entry("abs", "U+0061", "\\text{abs}", "absolute_value", "arithmetic", "unary", "operator", 2, 2, "partial", "no", "no", "no", "partial", "high", ["absolute_value", "cardinality"]),
        create_symbol_entry("sgn", "U+0073", "\\text{sgn}", "sign", "arithmetic", "unary", "operator", 1, 2, "none", "no", "no", "no", "none", "high", ["sign_function"]),
        create_symbol_entry("^", "U+005E", "^", "power", "arithmetic", "binary", "operator", 2, 3, "partial", "no", "no", "yes", "partial", "high", ["exponentiation", "bitwise_xor"]),
        create_symbol_entry("²", "U+00B2", "^2", "squared", "arithmetic", "unary", "operator", 1, 3, "partial", "no", "no", "no", "partial", "high", ["square"]),
        create_symbol_entry("³", "U+00B3", "^3", "cubed", "arithmetic", "unary", "operator", 1, 3, "full", "no", "no", "no", "full", "high", ["cube"]),
        create_symbol_entry("∛", "U+221B", "\\sqrt[3]", "cube_root", "arithmetic", "unary", "operator", 1, 3, "full", "no", "no", "no", "full", "high", ["cube_root"]),
        create_symbol_entry("∜", "U+221C", "\\sqrt[4]", "fourth_root", "arithmetic", "unary", "operator", 1, 3, "partial", "no", "no", "no", "partial", "medium", ["fourth_root"]),
        create_symbol_entry("±", "U+00B1", "\\pm", "plus_minus", "arithmetic", "unary", "operator", 2, 2, "none", "no", "no", "no", "none", "medium", ["plus_minus", "error_margin"]),
        create_symbol_entry("∓", "U+2213", "\\mp", "minus_plus", "arithmetic", "unary", "operator", 1, 2, "none", "no", "no", "no", "none", "medium", ["minus_plus"]),
        create_symbol_entry("⋅", "U+22C5", "\\cdot", "dot", "arithmetic", "binary", "operator", 3, 2, "partial", "partial", "yes", "yes", "partial", "high", ["multiplication", "dot_product", "composition"]),
    ])
    
    # ALGEBRA RELATIONS & OPERATORS
    symbols.extend([
        create_symbol_entry("=", "U+003D", "=", "equals", "algebra", "binary", "relation", 2, 1, "full", "yes", "no", "no", "full", "high", ["equality", "assignment", "definition"]),
        create_symbol_entry("≠", "U+2260", "\\neq", "not_equal", "algebra", "binary", "relation", 1, 1, "full", "yes", "no", "no", "full", "high", ["inequality"]),
        create_symbol_entry("≡", "U+2261", "\\equiv", "equivalent", "algebra", "binary", "relation", 3, 1, "full", "yes", "yes", "no", "full", "high", ["congruence", "identical", "logical_equivalence"]),
        create_symbol_entry("≈", "U+2248", "\\approx", "approximately", "algebra", "binary", "relation", 2, 1, "partial", "yes", "no", "no", "partial", "medium", ["approximation", "asymptotic"]),
        create_symbol_entry("∝", "U+221D", "\\propto", "proportional", "algebra", "binary", "relation", 1, 1, "partial", "no", "no", "no", "partial", "medium", ["proportionality"]),
        create_symbol_entry("<", "U+003C", "<", "less_than", "algebra", "binary", "relation", 1, 1, "full", "no", "no", "no", "full", "high", ["ordering"]),
        create_symbol_entry(">", "U+003E", ">", "greater_than", "algebra", "binary", "relation", 1, 1, "full", "no", "no", "no", "full", "high", ["ordering"]),
        create_symbol_entry("≤", "U+2264", "\\leq", "less_equal", "algebra", "binary", "relation", 1, 1, "full", "no", "no", "no", "full", "high", ["ordering"]),
        create_symbol_entry("≥", "U+2265", "\\geq", "greater_equal", "algebra", "binary", "relation", 1, 1, "full", "no", "no", "no", "full", "high", ["ordering"]),
        create_symbol_entry("≪", "U+226A", "\\ll", "much_less", "algebra", "binary", "relation", 1, 1, "full", "no", "no", "no", "full", "medium", ["much_less"]),
        create_symbol_entry("≫", "U+226B", "\\gg", "much_greater", "algebra", "binary", "relation", 1, 1, "full", "no", "no", "no", "full", "medium", ["much_greater"]),
        create_symbol_entry("∼", "U+223C", "\\sim", "similar", "algebra", "binary", "relation", 3, 1, "full", "yes", "yes", "no", "full", "high", ["similarity", "equivalence", "distribution"]),
        create_symbol_entry("≃", "U+2243", "\\simeq", "asymptotically_equal", "algebra", "binary", "relation", 2, 1, "full", "yes", "no", "no", "full", "medium", ["asymptotic_equality", "isomorphism"]),
        create_symbol_entry("≅", "U+2245", "\\cong", "congruent", "algebra", "binary", "relation", 2, 1, "full", "yes", "yes", "no", "full", "high", ["congruence", "isomorphism"]),
        create_symbol_entry("∥", "U+2225", "\\parallel", "parallel", "algebra", "binary", "relation", 2, 1, "full", "yes", "no", "no", "full", "high", ["parallel", "norm"]),
        create_symbol_entry("⊥", "U+22A5", "\\perp", "perpendicular", "algebra", "binary", "relation", 3, 1, "full", "yes", "no", "no", "full", "high", ["perpendicular", "orthogonal", "bottom"]),
        create_symbol_entry("⊙", "U+2299", "\\odot", "hadamard_product", "algebra", "binary", "operator", 2, 2, "partial", "yes", "yes", "yes", "partial", "high", ["hadamard_product", "circled_dot"]),
        create_symbol_entry("⊛", "U+229B", "\\circledast", "circled_asterisk", "algebra", "binary", "operator", 2, 2, "partial", "yes", "yes", "yes", "partial", "high", ["convolution", "circled_operator"]),
        create_symbol_entry("⋆", "U+22C6", "\\star", "star", "algebra", "binary", "operator", 3, 2, "partial", "partial", "yes", "yes", "partial", "high", ["hodge_star", "convolution", "binary_operation"]),
        create_symbol_entry("det", "U+0064", "\\det", "determinant", "algebra", "unary", "operator", 1, 2, "none", "no", "no", "no", "none", "high", ["matrix_determinant"]),
        create_symbol_entry("tr", "U+0074", "\\text{tr}", "trace", "algebra", "unary", "operator", 1, 2, "none", "no", "no", "no", "none", "high", ["matrix_trace"]),
        create_symbol_entry("rank", "U+0072", "\\text{rank}", "rank", "algebra", "unary", "operator", 1, 2, "none", "no", "no", "no", "none", "high", ["matrix_rank"]),
        create_symbol_entry("dim", "U+0064", "\\dim", "dimension", "algebra", "unary", "operator", 1, 2, "none", "no", "no", "no", "none", "high", ["vector_space_dimension"]),
        create_symbol_entry("ker", "U+006B", "\\ker", "kernel", "algebra", "unary", "operator", 1, 2, "none", "no", "no", "no", "none", "high", ["linear_map_kernel"]),
        create_symbol_entry("im", "U+0069", "\\text{im}", "image", "algebra", "unary", "operator", 2, 2, "none", "no", "no", "no", "none", "high", ["linear_map_image", "imaginary_part"]),
        create_symbol_entry("Re", "U+0052", "\\Re", "real_part", "algebra", "unary", "operator", 1, 2, "none", "no", "no", "no", "none", "high", ["real_part"]),
        create_symbol_entry("Im", "U+0049", "\\Im", "imaginary_part", "algebra", "unary", "operator", 1, 2, "none", "no", "no", "no", "none", "high", ["imaginary_part"]),
        create_symbol_entry("arg", "U+0061", "\\arg", "argument", "algebra", "unary", "operator", 2, 2, "partial", "no", "no", "no", "partial", "medium", ["complex_argument", "function_argument"]),
        create_symbol_entry("⋉", "U+22C9", "\\ltimes", "left_semidirect_product", "algebra", "binary", "operator", 1, 2, "none", "no", "yes", "yes", "none", "high", ["semidirect_product"]),
        create_symbol_entry("⋊", "U+22CA", "\\rtimes", "right_semidirect_product", "algebra", "binary", "operator", 1, 2, "none", "no", "yes", "yes", "none", "high", ["semidirect_product"]),
        create_symbol_entry("⊲", "U+22B2", "\\triangleleft", "normal_subgroup", "algebra", "binary", "relation", 1, 1, "none", "no", "yes", "no", "none", "high", ["normal_subgroup"]),
        create_symbol_entry("⊳", "U+22B3", "\\triangleright", "contains_as_normal", "algebra", "binary", "relation", 1, 1, "none", "no", "yes", "no", "none", "high", ["normal_subgroup"]),
    ])
    
    # LOGIC OPERATORS
    symbols.extend([
        create_symbol_entry("∧", "U+2227", "\\land", "and", "logic", "binary", "operator", 1, 2, "partial", "yes", "yes", "yes", "partial", "high", ["logical_and", "meet"]),
        create_symbol_entry("∨", "U+2228", "\\lor", "or", "logic", "binary", "operator", 1, 2, "partial", "yes", "yes", "yes", "partial", "high", ["logical_or", "join"]),
        create_symbol_entry("¬", "U+00AC", "\\neg", "not", "logic", "unary", "operator", 1, 2, "full", "no", "no", "no", "full", "high", ["logical_not", "complement"]),
        create_symbol_entry("→", "U+2192", "\\to", "implies", "logic", "binary", "operator", 3, 2, "none", "no", "no", "no", "none", "high", ["implication", "function_arrow", "limit"]),
        create_symbol_entry("↔", "U+2194", "\\leftrightarrow", "iff", "logic", "binary", "operator", 2, 2, "full", "yes", "no", "no", "full", "high", ["biconditional", "equivalence"]),
        create_symbol_entry("⊕", "U+2295", "\\oplus", "xor", "logic", "binary", "operator", 3, 2, "full", "yes", "yes", "yes", "full", "high", ["exclusive_or", "direct_sum", "tensor_sum"]),
        create_symbol_entry("⊤", "U+22A4", "\\top", "true", "logic", "nullary", "operand", 1, 3, "none", "no", "no", "no", "none", "high", ["truth_value"]),
        create_symbol_entry("⊥", "U+22A5", "\\bot", "false", "logic", "nullary", "operand", 2, 3, "none", "no", "no", "no", "none", "high", ["truth_value", "orthogonal"]),
        create_symbol_entry("∀", "U+2200", "\\forall", "for_all", "logic", "unary", "quantifier", 1, 1, "none", "no", "no", "no", "none", "high", ["universal_quantifier"]),
        create_symbol_entry("∃", "U+2203", "\\exists", "exists", "logic", "unary", "quantifier", 1, 1, "none", "no", "no", "no", "none", "high", ["existential_quantifier"]),
        create_symbol_entry("⇒", "U+21D2", "\\Rightarrow", "double_implies", "logic", "binary", "operator", 1, 2, "none", "no", "no", "no", "none", "high", ["strong_implication"]),
        create_symbol_entry("⇔", "U+21D4", "\\Leftrightarrow", "double_iff", "logic", "binary", "operator", 1, 2, "full", "yes", "no", "no", "full", "high", ["strong_equivalence"]),
        create_symbol_entry("⊢", "U+22A2", "\\vdash", "proves", "logic", "binary", "relation", 1, 1, "none", "no", "no", "no", "none", "high", ["syntactic_consequence"]),
        create_symbol_entry("⊨", "U+22A8", "\\models", "models", "logic", "binary", "relation", 1, 1, "none", "no", "no", "no", "none", "high", ["semantic_consequence"]),
        create_symbol_entry("⊻", "U+22BB", "\\veebar", "exclusive_or", "logic", "binary", "operator", 1, 2, "full", "yes", "yes", "yes", "full", "high", ["xor"]),
        create_symbol_entry("⊼", "U+22BC", "\\barwedge", "nand", "logic", "binary", "operator", 1, 2, "none", "yes", "no", "no", "none", "high", ["nand"]),
        create_symbol_entry("⊽", "U+22BD", "\\veebar", "nor", "logic", "binary", "operator", 1, 2, "none", "yes", "no", "no", "none", "high", ["nor"]),
        create_symbol_entry("⋀", "U+22C0", "\\bigwedge", "big_and", "logic", "unary", "operator", 1, 1, "none", "yes", "yes", "yes", "none", "high", ["conjunction"]),
        create_symbol_entry("⋁", "U+22C1", "\\bigvee", "big_or", "logic", "unary", "operator", 1, 1, "none", "yes", "yes", "yes", "none", "high", ["disjunction"]),
        create_symbol_entry("⋎", "U+22CE", "\\curlyvee", "curly_vee", "logic", "binary", "operator", 1, 2, "partial", "yes", "yes", "yes", "partial", "high", ["logical_or_variant"]),
        create_symbol_entry("⋏", "U+22CF", "\\curlywedge", "curly_wedge", "logic", "binary", "operator", 1, 2, "partial", "yes", "yes", "yes", "partial", "high", ["logical_and_variant"]),
    ])
    
    # SET THEORY
    symbols.extend([
        create_symbol_entry("∈", "U+2208", "\\in", "element_of", "set_theory", "binary", "relation", 1, 1, "none", "no", "no", "no", "none", "high", ["membership"]),
        create_symbol_entry("∉", "U+2209", "\\notin", "not_element_of", "set_theory", "binary", "relation", 1, 1, "none", "no", "no", "no", "none", "high", ["membership"]),
        create_symbol_entry("⊆", "U+2286", "\\subseteq", "subset_equal", "set_theory", "binary", "relation", 1, 1, "partial", "no", "yes", "no", "partial", "high", ["subset"]),
        create_symbol_entry("⊂", "U+2282", "\\subset", "proper_subset", "set_theory", "binary", "relation", 1, 1, "partial", "no", "yes", "no", "partial", "high", ["proper_subset"]),
        create_symbol_entry("∪", "U+222A", "\\cup", "union", "set_theory", "binary", "operator", 1, 2, "none", "yes", "yes", "yes", "none", "high", ["set_union"]),
        create_symbol_entry("∩", "U+2229", "\\cap", "intersection", "set_theory", "binary", "operator", 1, 2, "none", "yes", "yes", "yes", "none", "high", ["set_intersection"]),
        create_symbol_entry("∅", "U+2205", "\\emptyset", "empty_set", "set_theory", "nullary", "operand", 1, 3, "none", "no", "no", "no", "none", "high", ["empty_set"]),
        create_symbol_entry("∁", "U+2201", "\\complement", "complement", "set_theory", "unary", "operator", 1, 2, "full", "no", "no", "no", "full", "high", ["set_complement"]),
        create_symbol_entry("℘", "U+2118", "\\wp", "power_set", "set_theory", "unary", "operator", 2, 2, "none", "no", "no", "no", "none", "high", ["power_set", "weierstrass_p"]),
        create_symbol_entry("⊇", "U+2287", "\\supseteq", "superset_equal", "set_theory", "binary", "relation", 1, 1, "partial", "no", "yes", "no", "partial", "high", ["superset"]),
        create_symbol_entry("⊃", "U+2283", "\\supset", "proper_superset", "set_theory", "binary", "relation", 1, 1, "partial", "no", "yes", "no", "partial", "high", ["proper_superset"]),
        create_symbol_entry("∖", "U+2216", "\\setminus", "set_difference", "set_theory", "binary", "operator", 1, 2, "none", "no", "no", "no", "none", "high", ["set_difference"]),
        create_symbol_entry("△", "U+25B3", "\\triangle", "symmetric_difference", "set_theory", "binary", "operator", 2, 2, "full", "yes", "yes", "yes", "full", "high", ["symmetric_difference", "triangle"]),
        create_symbol_entry("⋃", "U+22C3", "\\bigcup", "big_union", "set_theory", "unary", "operator", 1, 1, "none", "yes", "yes", "yes", "none", "high", ["indexed_union"]),
        create_symbol_entry("⋂", "U+22C2", "\\bigcap", "big_intersection", "set_theory", "unary", "operator", 1, 1, "none", "yes", "yes", "yes", "none", "high", ["indexed_intersection"]),
        create_symbol_entry("ℕ", "U+2115", "\\mathbb{N}", "naturals", "set_theory", "nullary", "operand", 1, 3, "none", "no", "no", "no", "none", "high", ["natural_numbers"]),
        create_symbol_entry("ℤ", "U+2124", "\\mathbb{Z}", "integers", "set_theory", "nullary", "operand", 1, 3, "none", "no", "no", "no", "none", "high", ["integers"]),
        create_symbol_entry("ℚ", "U+211A", "\\mathbb{Q}", "rationals", "set_theory", "nullary", "operand", 1, 3, "none", "no", "no", "no", "none", "high", ["rational_numbers"]),
        create_symbol_entry("ℝ", "U+211D", "\\mathbb{R}", "reals", "set_theory", "nullary", "operand", 1, 3, "none", "no", "no", "no", "none", "high", ["real_numbers"]),
        create_symbol_entry("ℂ", "U+2102", "\\mathbb{C}", "complex", "set_theory", "nullary", "operand", 1, 3, "none", "no", "no", "no", "none", "high", ["complex_numbers"]),
        create_symbol_entry("ℵ", "U+2135", "\\aleph", "aleph", "set_theory", "nullary", "operand", 1, 3, "none", "no", "no", "no", "none", "high", ["cardinality"]),
        create_symbol_entry("⊏", "U+228F", "\\sqsubset", "square_image_of", "set_theory", "binary", "relation", 1, 1, "partial", "no", "yes", "no", "partial", "high", ["square_subset"]),
        create_symbol_entry("⊐", "U+2290", "\\sqsupset", "square_original_of", "set_theory", "binary", "relation", 1, 1, "partial", "no", "yes", "no", "partial", "high", ["square_superset"]),
        create_symbol_entry("⊓", "U+2293", "\\sqcap", "square_cap", "set_theory", "binary", "operator", 1, 2, "none", "yes", "yes", "yes", "none", "high", ["meet"]),
        create_symbol_entry("⊔", "U+2294", "\\sqcup", "square_cup", "set_theory", "binary", "operator", 1, 2, "none", "yes", "yes", "yes", "none", "high", ["join"]),
        create_symbol_entry("⊎", "U+228E", "\\uplus", "multiset_union", "set_theory", "binary", "operator", 1, 2, "none", "yes", "yes", "yes", "none", "high", ["disjoint_union"]),
        create_symbol_entry("⨄", "U+2A04", "\\biguplus", "big_union_plus", "set_theory", "unary", "operator", 1, 1, "none", "yes", "yes", "yes", "none", "high", ["big_union"]),
        create_symbol_entry("⨅", "U+2A05", "\\bigsqcap", "big_square_cap", "set_theory", "unary", "operator", 1, 1, "none", "yes", "yes", "yes", "none", "high", ["big_meet"]),
        create_symbol_entry("⨆", "U+2A06", "\\bigsqcup", "big_square_cup", "set_theory", "unary", "operator", 1, 1, "none", "yes", "yes", "yes", "none", "high", ["big_join"]),
    ])
    
    # CALCULUS
    symbols.extend([
        create_symbol_entry("∂", "U+2202", "\\partial", "partial_derivative", "calculus", "unary", "operator", 2, 1, "none", "no", "no", "no", "none", "low", ["partial_derivative", "boundary"]),
        create_symbol_entry("∇", "U+2207", "\\nabla", "nabla", "calculus", "unary", "operator", 4, 1, "none", "no", "no", "no", "none", "low", ["gradient", "divergence", "curl", "del_operator"]),
        create_symbol_entry("∫", "U+222B", "\\int", "integral", "calculus", "unary", "operator", 3, 1, "none", "no", "no", "no", "none", "low", ["definite_integral", "indefinite_integral", "line_integral"]),
        create_symbol_entry("∮", "U+222E", "\\oint", "contour_integral", "calculus", "unary", "operator", 1, 1, "none", "no", "no", "no", "none", "low", ["contour_integral"]),
        create_symbol_entry("d", "U+0064", "d", "differential", "calculus", "unary", "operator", 2, 2, "none", "no", "no", "no", "none", "low", ["differential", "exterior_derivative"]),
        create_symbol_entry("Δ", "U+0394", "\\Delta", "delta", "calculus", "unary", "operator", 4, 2, "none", "no", "no", "no", "none", "medium", ["difference", "laplacian", "discriminant", "change"]),
        create_symbol_entry("∞", "U+221E", "\\infty", "infinity", "calculus", "nullary", "operand", 2, 3, "none", "no", "no", "no", "none", "low", ["infinity", "cardinality"]),
        create_symbol_entry("sin", "U+0073", "\\sin", "sine", "calculus", "unary", "operator", 1, 2, "partial", "no", "no", "no", "partial", "high", ["trigonometric"]),
        create_symbol_entry("cos", "U+0063", "\\cos", "cosine", "calculus", "unary", "operator", 1, 2, "partial", "no", "no", "no", "partial", "high", ["trigonometric"]),
        create_symbol_entry("tan", "U+0074", "\\tan", "tangent", "calculus", "unary", "operator", 1, 2, "partial", "no", "no", "no", "partial", "medium", ["trigonometric"]),
        create_symbol_entry("exp", "U+0065", "\\exp", "exponential", "calculus", "unary", "operator", 1, 2, "full", "no", "no", "no", "full", "high", ["exponential"]),
        create_symbol_entry("log", "U+006C", "\\log", "logarithm", "calculus", "unary", "operator", 2, 2, "full", "no", "no", "no", "full", "medium", ["natural_log", "common_log"]),
        create_symbol_entry("ln", "U+006C", "\\ln", "natural_logarithm", "calculus", "unary", "operator", 1, 2, "full", "no", "no", "no", "full", "high", ["natural_logarithm"]),
        create_symbol_entry("lim", "U+006C", "\\lim", "limit", "calculus", "unary", "operator", 2, 1, "none", "no", "no", "no", "none", "low", ["limit", "limit_inferior"]),
        create_symbol_entry("sup", "U+0073", "\\sup", "supremum", "calculus", "unary", "operator", 1, 1, "none", "no", "no", "no", "none", "medium", ["supremum"]),
        create_symbol_entry("inf", "U+0069", "\\inf", "infimum", "calculus", "unary", "operator", 1, 1, "none", "no", "no", "no", "none", "medium", ["infimum"]),
        create_symbol_entry("Γ", "U+0393", "\\Gamma", "gamma_function", "calculus", "unary", "operator", 2, 2, "none", "no", "no", "no", "none", "medium", ["gamma_function", "christoffel_symbol"]),
        create_symbol_entry("ζ", "U+03B6", "\\zeta", "riemann_zeta", "calculus", "unary", "operator", 1, 2, "none", "no", "no", "no", "none", "medium", ["riemann_zeta"]),
    ])
    
    # PROBABILITY & STATISTICS
    symbols.extend([
        create_symbol_entry("ℙ", "U+2119", "\\mathbb{P}", "probability", "probability", "unary", "operator", 2, 1, "none", "no", "no", "no", "none", "medium", ["probability_measure", "projective_space"]),
        create_symbol_entry("𝔼", "U+1D53C", "\\mathbb{E}", "expectation", "probability", "unary", "operator", 1, 1, "none", "no", "no", "no", "none", "medium", ["expected_value"]),
        create_symbol_entry("~", "U+007E", "\\sim", "distributed_as", "probability", "binary", "relation", 3, 1, "none", "no", "no", "no", "none", "medium", ["distribution", "equivalence", "asymptotic"]),
        create_symbol_entry("|", "U+007C", "|", "bar", "probability", "binary", "operator", 5, 2, "none", "no", "no", "no", "none", "medium", ["conditional", "absolute_value", "divides", "cardinality", "restriction"]),
        create_symbol_entry("σ", "U+03C3", "\\sigma", "sigma", "probability", "unary", "operator", 4, 2, "none", "no", "no", "no", "none", "medium", ["standard_deviation", "pauli_matrix", "stress_tensor", "sigma_algebra"]),
        create_symbol_entry("μ", "U+03BC", "\\mu", "mu", "probability", "unary", "operator", 3, 2, "none", "no", "no", "no", "none", "medium", ["mean", "measure", "mobius_function"]),
        create_symbol_entry("Var", "U+0056", "\\text{Var}", "variance", "probability", "unary", "operator", 1, 1, "none", "no", "no", "no", "none", "medium", ["variance"]),
        create_symbol_entry("Cov", "U+0043", "\\text{Cov}", "covariance", "probability", "binary", "operator", 1, 1, "none", "yes", "no", "no", "none", "medium", ["covariance"]),
        create_symbol_entry("Corr", "U+0043", "\\text{Corr}", "correlation", "probability", "binary", "operator", 1, 1, "none", "yes", "no", "no", "none", "medium", ["correlation"]),
    ])
    
    # QUANTUM MECHANICS
    symbols.extend([
        create_symbol_entry("⊗", "U+2297", "\\otimes", "tensor_product", "quantum", "binary", "operator", 2, 2, "none", "no", "yes", "yes", "none", "high", ["tensor_product", "kronecker_product"]),
        create_symbol_entry("⟨", "U+27E8", "\\langle", "bra", "quantum", "unary", "operator", 2, 2, "full", "no", "no", "no", "full", "high", ["bra_vector", "inner_product"]),
        create_symbol_entry("⟩", "U+27E9", "\\rangle", "ket", "quantum", "unary", "operator", 2, 2, "full", "no", "no", "no", "full", "high", ["ket_vector", "inner_product"]),
        create_symbol_entry("ρ", "U+03C1", "\\rho", "density_matrix", "quantum", "nullary", "operand", 3, 3, "none", "no", "no", "no", "none", "high", ["density_matrix", "correlation", "resistivity"]),
        create_symbol_entry("†", "U+2020", "\\dagger", "hermitian_conjugate", "quantum", "unary", "operator", 1, 2, "full", "no", "no", "no", "full", "high", ["hermitian_conjugate"]),
        create_symbol_entry("⊠", "U+22A0", "\\boxtimes", "box_times", "quantum", "binary", "operator", 1, 2, "none", "no", "yes", "yes", "none", "high", ["tensor_product"]),
        create_symbol_entry("⊞", "U+229E", "\\boxplus", "box_plus", "quantum", "binary", "operator", 1, 2, "partial", "yes", "yes", "yes", "partial", "high", ["direct_sum"]),
        create_symbol_entry("⊟", "U+229F", "\\boxminus", "box_minus", "quantum", "binary", "operator", 1, 2, "partial", "no", "no", "yes", "partial", "high", ["quantum_operator"]),
    ])
    
    # INFORMATION THEORY
    symbols.extend([
        create_symbol_entry("H", "U+0048", "H", "entropy", "information", "unary", "operator", 3, 1, "none", "no", "no", "no", "none", "medium", ["shannon_entropy", "hamiltonian", "hilbert_space"]),
        create_symbol_entry("I", "U+0049", "I", "mutual_information", "information", "binary", "operator", 3, 1, "none", "yes", "no", "no", "none", "medium", ["mutual_information", "identity_matrix", "indicator"]),
        create_symbol_entry("S", "U+0053", "S", "von_neumann_entropy", "information", "unary", "operator", 2, 1, "none", "no", "no", "no", "none", "medium", ["von_neumann_entropy", "action"]),
    ])
    
    # MISCELLANEOUS
    symbols.extend([
        create_symbol_entry("∘", "U+2218", "\\circ", "composition", "miscellaneous", "binary", "operator", 3, 2, "partial", "no", "yes", "yes", "partial", "high", ["function_composition", "hadamard_product", "ring_operator"]),
        create_symbol_entry("∠", "U+2220", "\\angle", "angle", "miscellaneous", "unary", "operator", 1, 2, "none", "no", "no", "no", "none", "high", ["angle"]),
        create_symbol_entry("π", "U+03C0", "\\pi", "pi", "miscellaneous", "nullary", "operand", 2, 3, "none", "no", "no", "no", "none", "high", ["pi_constant", "prime_counting"]),
        create_symbol_entry("e", "U+0065", "e", "eulers_number", "miscellaneous", "nullary", "operand", 1, 3, "none", "no", "no", "no", "none", "high", ["eulers_number"]),
        create_symbol_entry("i", "U+0069", "i", "imaginary_unit", "miscellaneous", "nullary", "operand", 2, 3, "none", "no", "no", "no", "none", "high", ["imaginary_unit", "index"]),
        create_symbol_entry("φ", "U+03C6", "\\phi", "golden_ratio", "miscellaneous", "nullary", "operand", 3, 3, "none", "no", "no", "no", "none", "high", ["golden_ratio", "euler_totient", "angle"]),
        create_symbol_entry("γ", "U+03B3", "\\gamma", "euler_mascheroni", "miscellaneous", "nullary", "operand", 3, 3, "none", "no", "no", "no", "none", "high", ["euler_mascheroni", "gamma_function", "lorentz_factor"]),
        create_symbol_entry("⨀", "U+2A00", "\\bigodot", "big_circled_dot", "miscellaneous", "unary", "operator", 1, 1, "none", "yes", "yes", "yes", "none", "high", ["big_operator"]),
        create_symbol_entry("⨁", "U+2A01", "\\bigoplus", "big_circled_plus", "miscellaneous", "unary", "operator", 1, 1, "none", "yes", "yes", "yes", "none", "high", ["big_operator"]),
        create_symbol_entry("⨂", "U+2A02", "\\bigotimes", "big_circled_times", "miscellaneous", "unary", "operator", 1, 1, "none", "yes", "yes", "yes", "none", "high", ["big_operator"]),
    ])
    
    # ADDITIONAL CALCULUS SYMBOLS
    symbols.extend([
        create_symbol_entry("sinh", "U+0073", "\\sinh", "hyperbolic_sine", "calculus", "unary", "operator", 1, 2, "full", "no", "no", "no", "full", "high", ["hyperbolic"]),
        create_symbol_entry("cosh", "U+0063", "\\cosh", "hyperbolic_cosine", "calculus", "unary", "operator", 1, 2, "full", "no", "no", "no", "full", "high", ["hyperbolic"]),
        create_symbol_entry("tanh", "U+0074", "\\tanh", "hyperbolic_tangent", "calculus", "unary", "operator", 1, 2, "full", "no", "no", "no", "full", "high", ["hyperbolic"]),
        create_symbol_entry("arcsin", "U+0061", "\\arcsin", "arcsine", "calculus", "unary", "operator", 1, 2, "partial", "no", "no", "no", "partial", "medium", ["inverse_trig"]),
        create_symbol_entry("arccos", "U+0061", "\\arccos", "arccosine", "calculus", "unary", "operator", 1, 2, "partial", "no", "no", "no", "partial", "medium", ["inverse_trig"]),
        create_symbol_entry("arctan", "U+0061", "\\arctan", "arctangent", "calculus", "unary", "operator", 1, 2, "partial", "no", "no", "no", "partial", "medium", ["inverse_trig"]),
        create_symbol_entry("sec", "U+0073", "\\sec", "secant", "calculus", "unary", "operator", 1, 2, "partial", "no", "no", "no", "partial", "medium", ["trigonometric"]),
        create_symbol_entry("csc", "U+0063", "\\csc", "cosecant", "calculus", "unary", "operator", 1, 2, "partial", "no", "no", "no", "partial", "medium", ["trigonometric"]),
        create_symbol_entry("cot", "U+0063", "\\cot", "cotangent", "calculus", "unary", "operator", 1, 2, "partial", "no", "no", "no", "partial", "medium", ["trigonometric"]),
    ])
    
    # ADDITIONAL ALGEBRA SYMBOLS
    symbols.extend([
        create_symbol_entry("⊕", "U+2295", "\\oplus", "direct_sum", "algebra", "binary", "operator", 3, 2, "partial", "yes", "yes", "yes", "partial", "high", ["direct_sum", "xor", "tensor_sum"]),
        create_symbol_entry("⊖", "U+2296", "\\ominus", "circled_minus", "algebra", "binary", "operator", 1, 2, "partial", "no", "no", "yes", "partial", "high", ["circled_minus"]),
        create_symbol_entry("⊘", "U+2298", "\\oslash", "circled_slash", "algebra", "binary", "operator", 1, 2, "partial", "no", "no", "yes", "partial", "high", ["circled_division"]),
        create_symbol_entry("⋀", "U+22C0", "\\bigwedge", "exterior_product", "algebra", "unary", "operator", 2, 1, "none", "yes", "yes", "yes", "none", "high", ["exterior_product", "conjunction"]),
        create_symbol_entry("⋁", "U+22C1", "\\bigvee", "join_operator", "algebra", "unary", "operator", 2, 1, "none", "yes", "yes", "yes", "none", "high", ["join", "disjunction"]),
        create_symbol_entry("∔", "U+2214", "\\dotplus", "dot_plus", "algebra", "binary", "operator", 1, 2, "partial", "yes", "yes", "yes", "partial", "high", ["dot_plus"]),
        create_symbol_entry("∸", "U+2238", "\\dotminus", "dot_minus", "algebra", "binary", "operator", 1, 2, "partial", "no", "no", "yes", "partial", "high", ["dot_minus"]),
        create_symbol_entry("≺", "U+227A", "\\prec", "precedes", "algebra", "binary", "relation", 1, 1, "partial", "no", "yes", "no", "partial", "high", ["order_relation"]),
        create_symbol_entry("≻", "U+227B", "\\succ", "succeeds", "algebra", "binary", "relation", 1, 1, "partial", "no", "yes", "no", "partial", "high", ["order_relation"]),
        create_symbol_entry("⪯", "U+2AAF", "\\preceq", "precedes_equal", "algebra", "binary", "relation", 1, 1, "partial", "no", "yes", "no", "partial", "high", ["order_relation"]),
        create_symbol_entry("⪰", "U+2AB0", "\\succeq", "succeeds_equal", "algebra", "binary", "relation", 1, 1, "partial", "no", "yes", "no", "partial", "high", ["order_relation"]),
        create_symbol_entry("≼", "U+227C", "\\curlyeqprec", "curly_precedes", "algebra", "binary", "relation", 1, 1, "partial", "no", "yes", "no", "partial", "high", ["order_relation"]),
        create_symbol_entry("≽", "U+227D", "\\curlyeqsucc", "curly_succeeds", "algebra", "binary", "relation", 1, 1, "partial", "no", "yes", "no", "partial", "high", ["order_relation"]),
    ])
    
    # ADDITIONAL INFORMATION THEORY SYMBOLS
    symbols.extend([
        create_symbol_entry("D", "U+0044", "D", "kl_divergence", "information", "binary", "operator", 2, 1, "none", "no", "no", "no", "none", "medium", ["kl_divergence", "derivative"]),
        create_symbol_entry("KL", "U+004B", "\\text{KL}", "kullback_leibler", "information", "binary", "operator", 1, 1, "none", "no", "no", "no", "none", "medium", ["kl_divergence"]),
        create_symbol_entry("JS", "U+004A", "\\text{JS}", "jensen_shannon", "information", "binary", "operator", 1, 1, "none", "yes", "no", "no", "none", "medium", ["js_divergence"]),
    ])
    
    # ADDITIONAL PROBABILITY SYMBOLS
    symbols.extend([
        create_symbol_entry("Pr", "U+0050", "\\Pr", "probability_function", "probability", "unary", "operator", 1, 1, "none", "no", "no", "no", "none", "medium", ["probability"]),
        create_symbol_entry("Med", "U+004D", "\\text{Med}", "median", "probability", "unary", "operator", 1, 1, "none", "no", "no", "no", "none", "medium", ["median"]),
        create_symbol_entry("Mode", "U+004D", "\\text{Mode}", "mode", "probability", "unary", "operator", 1, 1, "none", "no", "no", "no", "none", "medium", ["mode"]),
        create_symbol_entry("SE", "U+0053", "\\text{SE}", "standard_error", "probability", "unary", "operator", 1, 1, "none", "no", "no", "no", "none", "medium", ["standard_error"]),
        create_symbol_entry("χ²", "U+03C7", "\\chi^2", "chi_squared", "probability", "unary", "operator", 1, 2, "none", "no", "no", "no", "none", "medium", ["chi_squared"]),
        create_symbol_entry("F", "U+0046", "F", "f_statistic", "probability", "binary", "operator", 2, 1, "none", "no", "no", "no", "none", "medium", ["f_test", "force"]),
        create_symbol_entry("t", "U+0074", "t", "t_statistic", "probability", "unary", "operator", 2, 1, "none", "no", "no", "no", "none", "medium", ["t_test", "time"]),
        create_symbol_entry("z", "U+007A", "z", "z_score", "probability", "unary", "operator", 2, 1, "none", "no", "no", "no", "none", "medium", ["z_score", "complex_variable"]),
    ])
    
    # ADDITIONAL QUANTUM SYMBOLS
    symbols.extend([
        create_symbol_entry("⊕", "U+2295", "\\oplus", "quantum_xor", "quantum", "binary", "operator", 3, 2, "full", "yes", "yes", "yes", "full", "high", ["quantum_xor", "direct_sum", "xor"]),
        create_symbol_entry("ψ", "U+03C8", "\\psi", "wave_function", "quantum", "nullary", "operand", 1, 3, "none", "no", "no", "no", "none", "high", ["wave_function"]),
        create_symbol_entry("Ψ", "U+03A8", "\\Psi", "state_vector", "quantum", "nullary", "operand", 1, 3, "none", "no", "no", "no", "none", "high", ["state_vector"]),
        create_symbol_entry("ℏ", "U+210F", "\\hbar", "reduced_planck", "quantum", "nullary", "operand", 1, 3, "none", "no", "no", "no", "none", "high", ["reduced_planck"]),
    ])
    
    # ADDITIONAL MISCELLANEOUS SYMBOLS
    symbols.extend([
        create_symbol_entry("∴", "U+2234", "\\therefore", "therefore", "miscellaneous", "nullary", "operator", 1, 1, "none", "no", "no", "no", "none", "high", ["therefore"]),
        create_symbol_entry("∵", "U+2235", "\\because", "because", "miscellaneous", "nullary", "operator", 1, 1, "none", "no", "no", "no", "none", "high", ["because"]),
        create_symbol_entry("∎", "U+220E", "\\qed", "qed", "miscellaneous", "nullary", "operator", 1, 1, "none", "no", "no", "no", "none", "high", ["qed"]),
        create_symbol_entry("□", "U+25A1", "\\square", "box", "miscellaneous", "unary", "operator", 2, 2, "none", "no", "no", "no", "none", "high", ["modal_necessity", "end_proof"]),
        create_symbol_entry("◇", "U+25C7", "\\diamond", "diamond", "miscellaneous", "unary", "operator", 2, 2, "none", "no", "no", "no", "none", "high", ["modal_possibility", "operator"]),
        create_symbol_entry("★", "U+2605", "\\bigstar", "star_operator", "miscellaneous", "binary", "operator", 1, 2, "partial", "yes", "yes", "yes", "partial", "high", ["convolution"]),
        create_symbol_entry("†", "U+2020", "\\dagger", "dagger", "miscellaneous", "unary", "operator", 2, 2, "full", "no", "no", "no", "full", "high", ["adjoint", "footnote"]),
        create_symbol_entry("‡", "U+2021", "\\ddagger", "double_dagger", "miscellaneous", "unary", "operator", 1, 2, "none", "no", "no", "no", "none", "high", ["footnote"]),
    ])
    
    return symbols

def main():
    """Generate and save the dataset."""
    symbols = generate_dataset()
    
    # Save to JSON
    output_path = "/home/ubuntu/ubp_symbol_study_phase1/data/symbols_dataset.json"
    with open(output_path, 'w') as f:
        json.dump(symbols, f, indent=2, ensure_ascii=False)
    
    # Print statistics
    from collections import Counter
    print(f"Generated {len(symbols)} symbols")
    print(f"\nCategory distribution:")
    cats = Counter(s['category'] for s in symbols)
    for cat, count in sorted(cats.items(), key=lambda x: -x[1]):
        print(f"  {cat:20s}: {count:3d}")
    
    print(f"\nDataset saved to: {output_path}")

if __name__ == "__main__":
    main()
