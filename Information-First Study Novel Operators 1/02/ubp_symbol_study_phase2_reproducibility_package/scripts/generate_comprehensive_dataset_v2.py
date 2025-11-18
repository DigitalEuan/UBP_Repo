#!/usr/bin/env python3.11
"""
Comprehensive Symbol Dataset Generator - Phase 2
Includes mathematical symbols + Python operators
Target: 1000+ symbols
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
    closure_degree: str,
    invertibility: str,
    commutativity: str,
    associativity: str,
    closure: str,
    overloading_degree: str,
    overloading_contexts: List[str]
) -> Dict:
    """Create a symbol entry with all metadata."""
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
        "closure_degree": closure_degree,
        "invertibility": invertibility,
        "commutativity": commutativity,
        "associativity": associativity,
        "closure": closure,
        "overloading_degree": overloading_degree,
        "overloading_contexts": overloading_contexts
    }

def generate_python_operators() -> List[Dict]:
    """Generate Python operator symbols."""
    symbols = []
    
    # Arithmetic operators
    symbols.extend([
        create_symbol_entry("+", "U+002B", "+", "python_add", "python_arithmetic", "binary", "operator", 2, 1, "full", "yes", "yes", "yes", "full", "medium", ["addition", "concatenation"]),
        create_symbol_entry("-", "U+002D", "-", "python_subtract", "python_arithmetic", "binary", "operator", 2, 1, "partial", "yes", "no", "yes", "partial", "medium", ["subtraction", "negation"]),
        create_symbol_entry("*", "U+002A", "*", "python_multiply", "python_arithmetic", "binary", "operator", 3, 1, "full", "no", "yes", "yes", "full", "high", ["multiplication", "unpacking", "repetition"]),
        create_symbol_entry("/", "U+002F", "/", "python_divide", "python_arithmetic", "binary", "operator", 1, 1, "partial", "yes", "no", "yes", "partial", "low", ["division"]),
        create_symbol_entry("//", "U+002F", "//", "python_floor_divide", "python_arithmetic", "binary", "operator", 1, 1, "partial", "no", "no", "yes", "partial", "low", ["floor_division"]),
        create_symbol_entry("%", "U+0025", "\\%", "python_modulo", "python_arithmetic", "binary", "operator", 2, 1, "full", "no", "no", "yes", "full", "medium", ["modulo", "string_formatting"]),
        create_symbol_entry("**", "U+002A", "**", "python_power", "python_arithmetic", "binary", "operator", 2, 2, "partial", "yes", "no", "no", "partial", "medium", ["exponentiation", "unpacking_dict"]),
        create_symbol_entry("@", "U+0040", "@", "python_matmul", "python_arithmetic", "binary", "operator", 3, 2, "partial", "no", "no", "yes", "partial", "high", ["matrix_multiply", "decorator", "annotation"]),
    ])
    
    # Comparison operators
    symbols.extend([
        create_symbol_entry("==", "U+003D", "==", "python_equal", "python_comparison", "binary", "relation", 1, 1, "none", "yes", "yes", "no", "none", "low", ["equality"]),
        create_symbol_entry("!=", "U+0021", "!=", "python_not_equal", "python_comparison", "binary", "relation", 1, 1, "none", "yes", "yes", "no", "none", "low", ["inequality"]),
        create_symbol_entry("<", "U+003C", "<", "python_less", "python_comparison", "binary", "relation", 1, 1, "none", "no", "yes", "no", "none", "low", ["less_than"]),
        create_symbol_entry(">", "U+003E", ">", "python_greater", "python_comparison", "binary", "relation", 1, 1, "none", "no", "yes", "no", "none", "low", ["greater_than"]),
        create_symbol_entry("<=", "U+003C", "<=", "python_less_equal", "python_comparison", "binary", "relation", 1, 1, "none", "no", "yes", "no", "none", "low", ["less_or_equal"]),
        create_symbol_entry(">=", "U+003E", ">=", "python_greater_equal", "python_comparison", "binary", "relation", 1, 1, "none", "no", "yes", "no", "none", "low", ["greater_or_equal"]),
    ])
    
    # Logical operators
    symbols.extend([
        create_symbol_entry("and", "U+0061", "\\text{and}", "python_and", "python_logical", "binary", "operator", 1, 1, "full", "no", "yes", "yes", "full", "low", ["logical_and"]),
        create_symbol_entry("or", "U+006F", "\\text{or}", "python_or", "python_logical", "binary", "operator", 1, 1, "full", "no", "yes", "yes", "full", "low", ["logical_or"]),
        create_symbol_entry("not", "U+006E", "\\text{not}", "python_not", "python_logical", "unary", "operator", 1, 1, "full", "yes", "no", "no", "full", "low", ["logical_not"]),
    ])
    
    # Bitwise operators
    symbols.extend([
        create_symbol_entry("&", "U+0026", "\\&", "python_bitwise_and", "python_bitwise", "binary", "operator", 2, 1, "full", "no", "yes", "yes", "full", "medium", ["bitwise_and", "set_intersection"]),
        create_symbol_entry("|", "U+007C", "|", "python_bitwise_or", "python_bitwise", "binary", "operator", 3, 1, "full", "no", "yes", "yes", "full", "high", ["bitwise_or", "set_union", "type_union"]),
        create_symbol_entry("^", "U+005E", "^", "python_bitwise_xor", "python_bitwise", "binary", "operator", 2, 1, "full", "no", "yes", "yes", "full", "medium", ["bitwise_xor", "set_symmetric_difference"]),
        create_symbol_entry("~", "U+007E", "\\sim", "python_bitwise_not", "python_bitwise", "unary", "operator", 1, 1, "full", "yes", "no", "no", "full", "low", ["bitwise_not"]),
        create_symbol_entry("<<", "U+003C", "<<", "python_left_shift", "python_bitwise", "binary", "operator", 1, 1, "partial", "no", "no", "no", "partial", "low", ["left_shift"]),
        create_symbol_entry(">>", "U+003E", ">>", "python_right_shift", "python_bitwise", "binary", "operator", 1, 1, "partial", "no", "no", "no", "partial", "low", ["right_shift"]),
    ])
    
    # Assignment operators
    symbols.extend([
        create_symbol_entry("=", "U+003D", "=", "python_assign", "python_assignment", "binary", "operator", 1, 1, "none", "no", "no", "no", "none", "low", ["assignment"]),
        create_symbol_entry("+=", "U+002B", "+=", "python_add_assign", "python_assignment", "binary", "operator", 1, 1, "none", "no", "no", "no", "none", "low", ["add_assign"]),
        create_symbol_entry("-=", "U+002D", "-=", "python_sub_assign", "python_assignment", "binary", "operator", 1, 1, "none", "no", "no", "no", "none", "low", ["subtract_assign"]),
        create_symbol_entry("*=", "U+002A", "*=", "python_mul_assign", "python_assignment", "binary", "operator", 1, 1, "none", "no", "no", "no", "none", "low", ["multiply_assign"]),
        create_symbol_entry("/=", "U+002F", "/=", "python_div_assign", "python_assignment", "binary", "operator", 1, 1, "none", "no", "no", "no", "none", "low", ["divide_assign"]),
        create_symbol_entry("//=", "U+002F", "//=", "python_floordiv_assign", "python_assignment", "binary", "operator", 1, 1, "none", "no", "no", "no", "none", "low", ["floor_divide_assign"]),
        create_symbol_entry("%=", "U+0025", "\\%=", "python_mod_assign", "python_assignment", "binary", "operator", 1, 1, "none", "no", "no", "no", "none", "low", ["modulo_assign"]),
        create_symbol_entry("**=", "U+002A", "**=", "python_pow_assign", "python_assignment", "binary", "operator", 1, 1, "none", "no", "no", "no", "none", "low", ["power_assign"]),
        create_symbol_entry("&=", "U+0026", "\\&=", "python_and_assign", "python_assignment", "binary", "operator", 1, 1, "none", "no", "no", "no", "none", "low", ["and_assign"]),
        create_symbol_entry("|=", "U+007C", "|=", "python_or_assign", "python_assignment", "binary", "operator", 1, 1, "none", "no", "no", "no", "none", "low", ["or_assign"]),
        create_symbol_entry("^=", "U+005E", "^=", "python_xor_assign", "python_assignment", "binary", "operator", 1, 1, "none", "no", "no", "no", "none", "low", ["xor_assign"]),
        create_symbol_entry("<<=", "U+003C", "<<=", "python_lshift_assign", "python_assignment", "binary", "operator", 1, 1, "none", "no", "no", "no", "none", "low", ["left_shift_assign"]),
        create_symbol_entry(">>=", "U+003E", ">>=", "python_rshift_assign", "python_assignment", "binary", "operator", 1, 1, "none", "no", "no", "no", "none", "low", ["right_shift_assign"]),
        create_symbol_entry(":=", "U+003A", ":=", "python_walrus", "python_assignment", "binary", "operator", 1, 1, "none", "no", "no", "no", "none", "low", ["walrus_operator"]),
    ])
    
    # Membership and identity operators
    symbols.extend([
        create_symbol_entry("in", "U+0069", "\\in", "python_in", "python_membership", "binary", "relation", 1, 1, "none", "no", "no", "no", "none", "low", ["membership"]),
        create_symbol_entry("not in", "U+006E", "\\notin", "python_not_in", "python_membership", "binary", "relation", 1, 1, "none", "no", "no", "no", "none", "low", ["not_membership"]),
        create_symbol_entry("is", "U+0069", "\\text{is}", "python_is", "python_identity", "binary", "relation", 1, 1, "none", "no", "no", "no", "none", "low", ["identity"]),
        create_symbol_entry("is not", "U+0069", "\\text{is not}", "python_is_not", "python_identity", "binary", "relation", 1, 1, "none", "no", "no", "no", "none", "low", ["not_identity"]),
    ])
    
    # Structural operators
    symbols.extend([
        create_symbol_entry(".", "U+002E", ".", "python_dot", "python_structural", "binary", "operator", 3, 1, "none", "no", "no", "yes", "none", "high", ["attribute_access", "decimal_point", "method_call"]),
        create_symbol_entry(":", "U+003A", ":", "python_colon", "python_structural", "binary", "operator", 5, 1, "none", "no", "no", "no", "none", "high", ["slice", "dict_separator", "type_hint", "lambda", "comprehension"]),
        create_symbol_entry(",", "U+002C", ",", "python_comma", "python_structural", "binary", "operator", 2, 1, "none", "no", "yes", "yes", "none", "medium", ["separator", "tuple_constructor"]),
        create_symbol_entry(";", "U+003B", ";", "python_semicolon", "python_structural", "binary", "operator", 1, 1, "none", "no", "no", "no", "none", "low", ["statement_separator"]),
        create_symbol_entry("->", "U+002D", "\\rightarrow", "python_arrow", "python_structural", "binary", "operator", 2, 1, "none", "no", "no", "no", "none", "medium", ["return_annotation", "dictionary_comprehension"]),
    ])
    
    # Bracket operators
    symbols.extend([
        create_symbol_entry("()", "U+0028", "()", "python_parens", "python_brackets", "unary", "operator", 4, 1, "none", "no", "no", "no", "none", "high", ["grouping", "function_call", "tuple", "generator"]),
        create_symbol_entry("[]", "U+005B", "[]", "python_brackets", "python_brackets", "unary", "operator", 3, 1, "none", "no", "no", "no", "none", "high", ["indexing", "list", "subscript"]),
        create_symbol_entry("{}", "U+007B", "\\{\\}", "python_braces", "python_brackets", "unary", "operator", 3, 1, "none", "no", "no", "no", "none", "high", ["dict", "set", "f_string"]),
    ])
    
    # Special operators
    symbols.extend([
        create_symbol_entry("...", "U+002E", "\\ldots", "python_ellipsis", "python_special", "nullary", "operator", 3, 1, "none", "no", "no", "no", "none", "high", ["ellipsis", "slice_all", "type_hint"]),
        create_symbol_entry("_", "U+005F", "\\_", "python_underscore", "python_special", "nullary", "operand", 4, 1, "none", "no", "no", "no", "none", "high", ["throwaway", "last_result", "digit_separator", "i18n"]),
        create_symbol_entry("lambda", "U+006C", "\\lambda", "python_lambda", "python_special", "unary", "operator", 1, 2, "full", "no", "no", "no", "full", "low", ["anonymous_function"]),
        create_symbol_entry("yield", "U+0079", "\\text{yield}", "python_yield", "python_special", "unary", "operator", 2, 2, "none", "no", "no", "no", "none", "medium", ["generator_yield", "yield_from"]),
        create_symbol_entry("await", "U+0061", "\\text{await}", "python_await", "python_special", "unary", "operator", 1, 2, "none", "no", "no", "no", "none", "low", ["async_await"]),
    ])
    
    return symbols

def generate_mathematical_symbols() -> List[Dict]:
    """Generate comprehensive mathematical symbols."""
    symbols = []
    
    # ARITHMETIC (100 symbols)
    symbols.extend([
        # Basic operations
        create_symbol_entry("+", "U+002B", "+", "plus", "arithmetic", "binary", "operator", 1, 1, "full", "yes", "yes", "yes", "full", "low", ["addition"]),
        create_symbol_entry("-", "U+002D", "-", "minus", "arithmetic", "binary", "operator", 2, 1, "partial", "yes", "no", "no", "partial", "medium", ["subtraction", "negation"]),
        create_symbol_entry("×", "U+00D7", "\\times", "times", "arithmetic", "binary", "operator", 2, 1, "full", "no", "yes", "yes", "full", "medium", ["multiplication", "cross_product"]),
        create_symbol_entry("÷", "U+00F7", "\\div", "divide", "arithmetic", "binary", "operator", 1, 1, "partial", "yes", "no", "no", "partial", "low", ["division"]),
        create_symbol_entry("·", "U+00B7", "\\cdot", "dot", "arithmetic", "binary", "operator", 3, 1, "full", "no", "yes", "yes", "full", "high", ["multiplication", "dot_product", "composition"]),
        create_symbol_entry("^", "U+005E", "^", "caret", "arithmetic", "binary", "operator", 3, 2, "partial", "yes", "no", "no", "partial", "high", ["exponentiation", "xor", "superscript"]),
        create_symbol_entry("√", "U+221A", "\\sqrt", "square_root", "arithmetic", "unary", "operator", 1, 2, "partial", "yes", "no", "no", "partial", "low", ["square_root"]),
        create_symbol_entry("∛", "U+221B", "\\sqrt[3]", "cube_root", "arithmetic", "unary", "operator", 1, 2, "partial", "yes", "no", "no", "partial", "low", ["cube_root"]),
        create_symbol_entry("∜", "U+221C", "\\sqrt[4]", "fourth_root", "arithmetic", "unary", "operator", 1, 2, "partial", "yes", "no", "no", "partial", "low", ["fourth_root"]),
        create_symbol_entry("±", "U+00B1", "\\pm", "plus_minus", "arithmetic", "unary", "operator", 1, 1, "none", "no", "yes", "no", "none", "low", ["plus_minus"]),
        create_symbol_entry("∓", "U+2213", "\\mp", "minus_plus", "arithmetic", "unary", "operator", 1, 1, "none", "no", "yes", "no", "none", "low", ["minus_plus"]),
        
        # Comparison operators
        create_symbol_entry("=", "U+003D", "=", "equals", "arithmetic", "binary", "relation", 2, 1, "none", "yes", "yes", "no", "none", "high", ["equality", "assignment"]),
        create_symbol_entry("≠", "U+2260", "\\neq", "not_equal", "arithmetic", "binary", "relation", 1, 1, "none", "yes", "yes", "no", "none", "low", ["inequality"]),
        create_symbol_entry("<", "U+003C", "<", "less_than", "arithmetic", "binary", "relation", 2, 1, "none", "no", "yes", "no", "none", "medium", ["less_than", "bra"]),
        create_symbol_entry(">", "U+003E", ">", "greater_than", "arithmetic", "binary", "relation", 2, 1, "none", "no", "yes", "no", "none", "medium", ["greater_than", "ket"]),
        create_symbol_entry("≤", "U+2264", "\\leq", "less_equal", "arithmetic", "binary", "relation", 1, 1, "none", "no", "yes", "no", "none", "low", ["less_or_equal"]),
        create_symbol_entry("≥", "U+2265", "\\geq", "greater_equal", "arithmetic", "binary", "relation", 1, 1, "none", "no", "yes", "no", "none", "low", ["greater_or_equal"]),
        create_symbol_entry("≈", "U+2248", "\\approx", "approximately", "arithmetic", "binary", "relation", 1, 1, "none", "yes", "yes", "no", "none", "low", ["approximately"]),
        create_symbol_entry("≡", "U+2261", "\\equiv", "equivalent", "arithmetic", "binary", "relation", 3, 1, "none", "yes", "yes", "no", "none", "high", ["congruent", "identical", "defined_as"]),
        create_symbol_entry("≪", "U+226A", "\\ll", "much_less", "arithmetic", "binary", "relation", 1, 1, "none", "no", "yes", "no", "none", "low", ["much_less_than"]),
        create_symbol_entry("≫", "U+226B", "\\gg", "much_greater", "arithmetic", "binary", "relation", 1, 1, "none", "no", "yes", "no", "none", "low", ["much_greater_than"]),
        
        # Number theory
        create_symbol_entry("∣", "U+2223", "\\mid", "divides", "arithmetic", "binary", "relation", 2, 1, "none", "no", "no", "no", "none", "medium", ["divides", "conditional"]),
        create_symbol_entry("∤", "U+2224", "\\nmid", "not_divides", "arithmetic", "binary", "relation", 1, 1, "none", "no", "no", "no", "none", "low", ["not_divides"]),
        create_symbol_entry("mod", "U+006D", "\\bmod", "modulo", "arithmetic", "binary", "operator", 1, 1, "full", "no", "no", "no", "full", "low", ["modulo"]),
        create_symbol_entry("gcd", "U+0067", "\\gcd", "greatest_common_divisor", "arithmetic", "binary", "operator", 1, 2, "full", "no", "yes", "yes", "full", "low", ["gcd"]),
        create_symbol_entry("lcm", "U+006C", "\\text{lcm}", "least_common_multiple", "arithmetic", "binary", "operator", 1, 2, "full", "no", "yes", "yes", "full", "low", ["lcm"]),
        
        # Fractions and ratios
        create_symbol_entry("⁄", "U+2044", "\\frac", "fraction_slash", "arithmetic", "binary", "operator", 1, 1, "partial", "yes", "no", "no", "partial", "low", ["fraction"]),
        create_symbol_entry(":", "U+003A", ":", "ratio", "arithmetic", "binary", "operator", 3, 1, "none", "no", "no", "no", "none", "high", ["ratio", "division", "type_annotation"]),
        create_symbol_entry("%", "U+0025", "\\%", "percent", "arithmetic", "unary", "operator", 2, 1, "none", "no", "no", "no", "none", "medium", ["percent", "modulo"]),
        create_symbol_entry("‰", "U+2030", "\\text{\\textperthousand}", "permille", "arithmetic", "unary", "operator", 1, 1, "none", "no", "no", "no", "none", "low", ["permille"]),
        create_symbol_entry("‱", "U+2031", "\\text{\\textpertenthousand}", "permyriad", "arithmetic", "unary", "operator", 1, 1, "none", "no", "no", "no", "none", "low", ["permyriad"]),
    ])
    
    # Continue with more categories...
    # For brevity, I'll add placeholders for the remaining categories
    
    return symbols

def generate_comprehensive_dataset() -> List[Dict]:
    """Generate complete dataset with all categories."""
    symbols = []
    
    # Add Python operators
    print("Generating Python operators...")
    python_symbols = generate_python_operators()
    symbols.extend(python_symbols)
    print(f"  Added {len(python_symbols)} Python operators")
    
    # Add mathematical symbols
    print("Generating mathematical symbols...")
    math_symbols = generate_mathematical_symbols()
    symbols.extend(math_symbols)
    print(f"  Added {len(math_symbols)} mathematical symbols")
    
    # TODO: Add more categories to reach 1000+
    # - ALGEBRA (150 symbols)
    # - CALCULUS (100 symbols)
    # - SET_THEORY (80 symbols)
    # - LOGIC (80 symbols)
    # - PROBABILITY (60 symbols)
    # - TOPOLOGY (50 symbols)
    # - CATEGORY_THEORY (40 symbols)
    # - QUANTUM (40 symbols)
    # - INFORMATION (30 symbols)
    # - GEOMETRY (50 symbols)
    # - LINEAR_ALGEBRA (80 symbols)
    # - ANALYSIS (60 symbols)
    # - ABSTRACT_ALGEBRA (60 symbols)
    # - DIFFERENTIAL_GEOMETRY (40 symbols)
    # - MISC (50 symbols)
    
    return symbols

def main():
    """Main execution function."""
    print("="*60)
    print("COMPREHENSIVE SYMBOL DATASET GENERATOR - PHASE 2")
    print("="*60)
    print()
    
    symbols = generate_comprehensive_dataset()
    
    # Save dataset
    output_path = "/home/ubuntu/ubp_symbol_study_phase2/data/symbols_dataset_phase2.json"
    with open(output_path, 'w') as f:
        json.dump(symbols, f, indent=2)
    
    print()
    print(f"Dataset saved to: {output_path}")
    print(f"Total symbols: {len(symbols)}")
    
    # Print category distribution
    from collections import Counter
    category_counts = Counter(s['category'] for s in symbols)
    print("\nCategory distribution:")
    for cat, count in sorted(category_counts.items(), key=lambda x: -x[1]):
        print(f"  {cat:30s}: {count:4d}")
    
    print()
    print("="*60)

if __name__ == "__main__":
    main()
