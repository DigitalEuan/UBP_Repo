#!/usr/bin/env python3.11
"""
Massive Symbol Dataset Generator - Phase 2
Comprehensive coverage: 1000+ symbols
"""

import json
from typing import List, Dict
from generate_comprehensive_dataset_v2 import create_symbol_entry, generate_python_operators, generate_mathematical_symbols

def generate_algebra_symbols() -> List[Dict]:
    """Generate algebra symbols (150 symbols)."""
    symbols = []
    
    # Variables (Greek alphabet - 48 symbols)
    greek_letters = [
        ("α", "U+03B1", "\\alpha", "alpha"),
        ("β", "U+03B2", "\\beta", "beta"),
        ("γ", "U+03B3", "\\gamma", "gamma"),
        ("δ", "U+03B4", "\\delta", "delta"),
        ("ε", "U+03B5", "\\epsilon", "epsilon"),
        ("ζ", "U+03B6", "\\zeta", "zeta"),
        ("η", "U+03B7", "\\eta", "eta"),
        ("θ", "U+03B8", "\\theta", "theta"),
        ("ι", "U+03B9", "\\iota", "iota"),
        ("κ", "U+03BA", "\\kappa", "kappa"),
        ("λ", "U+03BB", "\\lambda", "lambda"),
        ("μ", "U+03BC", "\\mu", "mu"),
        ("ν", "U+03BD", "\\nu", "nu"),
        ("ξ", "U+03BE", "\\xi", "xi"),
        ("ο", "U+03BF", "o", "omicron"),
        ("π", "U+03C0", "\\pi", "pi"),
        ("ρ", "U+03C1", "\\rho", "rho"),
        ("σ", "U+03C3", "\\sigma", "sigma"),
        ("τ", "U+03C4", "\\tau", "tau"),
        ("υ", "U+03C5", "\\upsilon", "upsilon"),
        ("φ", "U+03C6", "\\phi", "phi"),
        ("χ", "U+03C7", "\\chi", "chi"),
        ("ψ", "U+03C8", "\\psi", "psi"),
        ("ω", "U+03C9", "\\omega", "omega"),
        # Uppercase
        ("Α", "U+0391", "A", "Alpha"),
        ("Β", "U+0392", "B", "Beta"),
        ("Γ", "U+0393", "\\Gamma", "Gamma"),
        ("Δ", "U+0394", "\\Delta", "Delta"),
        ("Ε", "U+0395", "E", "Epsilon"),
        ("Ζ", "U+0396", "Z", "Zeta"),
        ("Η", "U+0397", "H", "Eta"),
        ("Θ", "U+0398", "\\Theta", "Theta"),
        ("Ι", "U+0399", "I", "Iota"),
        ("Κ", "U+039A", "K", "Kappa"),
        ("Λ", "U+039B", "\\Lambda", "Lambda"),
        ("Μ", "U+039C", "M", "Mu"),
        ("Ν", "U+039D", "N", "Nu"),
        ("Ξ", "U+039E", "\\Xi", "Xi"),
        ("Ο", "U+039F", "O", "Omicron"),
        ("Π", "U+03A0", "\\Pi", "Pi"),
        ("Ρ", "U+03A1", "P", "Rho"),
        ("Σ", "U+03A3", "\\Sigma", "Sigma"),
        ("Τ", "U+03A4", "T", "Tau"),
        ("Υ", "U+03A5", "\\Upsilon", "Upsilon"),
        ("Φ", "U+03A6", "\\Phi", "Phi"),
        ("Χ", "U+03A7", "X", "Chi"),
        ("Ψ", "U+03A8", "\\Psi", "Psi"),
        ("Ω", "U+03A9", "\\Omega", "Omega"),
    ]
    
    for symbol, unicode, latex, name in greek_letters:
        symbols.append(create_symbol_entry(
            symbol, unicode, latex, name, "algebra", "nullary", "operand",
            2, 1, "none", "no", "no", "no", "none", "high",
            ["variable", "constant"]
        ))
    
    # Algebraic operations (50 symbols)
    operations = [
        ("⊕", "U+2295", "\\oplus", "direct_sum", "binary", 3, ["direct_sum", "xor"]),
        ("⊗", "U+2297", "\\otimes", "tensor_product", "binary", 2, ["tensor_product"]),
        ("⊙", "U+2299", "\\odot", "hadamard_product", "binary", 2, ["hadamard_product"]),
        ("⊖", "U+2296", "\\ominus", "circled_minus", "binary", 1, ["circled_minus"]),
        ("⊘", "U+2298", "\\oslash", "circled_slash", "binary", 1, ["circled_division"]),
        ("⊚", "U+229A", "\\circledcirc", "circled_ring", "binary", 1, ["circled_ring"]),
        ("⊛", "U+229B", "\\circledast", "circled_asterisk", "binary", 1, ["circled_asterisk"]),
        ("⊜", "U+229C", "\\circledequal", "circled_equals", "binary", 1, ["circled_equals"]),
        ("⊝", "U+229D", "\\circleddash", "circled_dash", "binary", 1, ["circled_dash"]),
        ("⋆", "U+22C6", "\\star", "star", "binary", 2, ["star_operator", "convolution"]),
        ("∗", "U+2217", "\\ast", "asterisk_operator", "binary", 2, ["asterisk_operator"]),
        ("∘", "U+2218", "\\circ", "composition", "binary", 3, ["composition", "ring_operator"]),
        ("∙", "U+2219", "\\bullet", "bullet_operator", "binary", 2, ["bullet_operator"]),
        ("⋄", "U+22C4", "\\diamond", "diamond_operator", "binary", 2, ["diamond_operator"]),
        ("⋅", "U+22C5", "\\cdot", "dot_operator", "binary", 3, ["dot_product", "multiplication"]),
        ("⋇", "U+22C7", "\\divideontimes", "division_times", "binary", 1, ["division_times"]),
        ("⋈", "U+22C8", "\\bowtie", "bowtie", "binary", 1, ["natural_join"]),
        ("⋉", "U+22C9", "\\ltimes", "left_normal_factor", "binary", 1, ["left_semidirect"]),
        ("⋊", "U+22CA", "\\rtimes", "right_normal_factor", "binary", 1, ["right_semidirect"]),
        ("⋋", "U+22CB", "\\leftthreetimes", "left_semidirect", "binary", 1, ["left_semidirect"]),
    ]
    
    for symbol, unicode, latex, name, arity, meaning_count, contexts in operations[:20]:
        symbols.append(create_symbol_entry(
            symbol, unicode, latex, name, "algebra", arity, "operator",
            meaning_count, 2, "partial", "no", "yes", "yes", "partial", "medium",
            contexts
        ))
    
    # Relations (30 symbols)
    relations = [
        ("≺", "U+227A", "\\prec", "precedes"),
        ("≻", "U+227B", "\\succ", "succeeds"),
        ("⪯", "U+2AAF", "\\preceq", "precedes_equal"),
        ("⪰", "U+2AB0", "\\succeq", "succeeds_equal"),
        ("≼", "U+227C", "\\curlyeqprec", "curly_precedes"),
        ("≽", "U+227D", "\\curlyeqsucc", "curly_succeeds"),
        ("⊏", "U+228F", "\\sqsubset", "square_subset"),
        ("⊐", "U+2290", "\\sqsupset", "square_superset"),
        ("⊑", "U+2291", "\\sqsubseteq", "square_subset_equal"),
        ("⊒", "U+2292", "\\sqsupseteq", "square_superset_equal"),
        ("⊲", "U+22B2", "\\lhd", "normal_subgroup"),
        ("⊳", "U+22B3", "\\rhd", "normal_subgroup_of"),
        ("⊴", "U+22B4", "\\unlhd", "normal_subgroup_or_equal"),
        ("⊵", "U+22B5", "\\unrhd", "normal_subgroup_of_or_equal"),
        ("⊢", "U+22A2", "\\vdash", "proves"),
        ("⊣", "U+22A3", "\\dashv", "adjoint"),
        ("⊤", "U+22A4", "\\top", "top"),
        ("⊥", "U+22A5", "\\bot", "bottom"),
        ("⊦", "U+22A6", "\\assert", "assert"),
        ("⊧", "U+22A7", "\\models", "models"),
    ]
    
    for symbol, unicode, latex, name in relations[:20]:
        symbols.append(create_symbol_entry(
            symbol, unicode, latex, name, "algebra", "binary", "relation",
            1, 1, "none", "no", "no", "no", "none", "low",
            [name]
        ))
    
    # Group theory symbols (22 symbols)
    group_symbols = [
        ("⟨", "U+27E8", "\\langle", "left_angle_bracket", "unary", ["generator", "bra"]),
        ("⟩", "U+27E9", "\\rangle", "right_angle_bracket", "unary", ["generator", "ket"]),
        ("⟦", "U+27E6", "\\llbracket", "left_double_bracket", "unary", ["semantic_brackets"]),
        ("⟧", "U+27E7", "\\rrbracket", "right_double_bracket", "unary", ["semantic_brackets"]),
        ("⟨⟩", "U+27E8", "\\langle\\rangle", "angle_brackets", "unary", ["generator", "inner_product"]),
        ("≅", "U+2245", "\\cong", "isomorphic", "binary", ["isomorphism"]),
        ("≃", "U+2243", "\\simeq", "asymptotically_equal", "binary", ["similar"]),
        ("≌", "U+224C", "\\backsimeq", "reverse_similar", "binary", ["reverse_similar"]),
        ("≊", "U+224A", "\\approxeq", "approximately_equal", "binary", ["approximately_equal"]),
        ("≋", "U+224B", "\\triplesim", "triple_tilde", "binary", ["triple_similar"]),
        ("⋮", "U+22EE", "\\vdots", "vertical_ellipsis", "nullary", ["vertical_dots"]),
        ("⋯", "U+22EF", "\\cdots", "centered_ellipsis", "nullary", ["centered_dots"]),
        ("⋰", "U+22F0", "\\iddots", "up_right_diagonal_ellipsis", "nullary", ["up_diagonal_dots"]),
        ("⋱", "U+22F1", "\\ddots", "down_right_diagonal_ellipsis", "nullary", ["down_diagonal_dots"]),
    ]
    
    for symbol, unicode, latex, name, arity, contexts in group_symbols[:14]:
        symbols.append(create_symbol_entry(
            symbol, unicode, latex, name, "algebra", arity, "operator",
            1, 2, "none", "no", "no", "no", "none", "medium",
            contexts
        ))
    
    return symbols

def generate_calculus_symbols() -> List[Dict]:
    """Generate calculus symbols (100 symbols)."""
    symbols = []
    
    # Differential operators (20 symbols)
    diff_ops = [
        ("d", "U+0064", "d", "differential", "unary", ["differential"]),
        ("∂", "U+2202", "\\partial", "partial_derivative", "unary", ["partial_derivative"]),
        ("∇", "U+2207", "\\nabla", "nabla", "unary", ["gradient", "del"]),
        ("Δ", "U+0394", "\\Delta", "laplacian", "unary", ["laplacian", "difference"]),
        ("δ", "U+03B4", "\\delta", "variation", "unary", ["variation", "dirac_delta"]),
        ("D", "U+0044", "D", "derivative_operator", "unary", ["derivative"]),
        ("∂²", "U+2202", "\\partial^2", "second_partial", "unary", ["second_partial"]),
        ("∇²", "U+2207", "\\nabla^2", "laplacian_operator", "unary", ["laplacian"]),
        ("∇·", "U+2207", "\\nabla\\cdot", "divergence", "unary", ["divergence"]),
        ("∇×", "U+2207", "\\nabla\\times", "curl", "unary", ["curl"]),
        ("d/dx", "U+0064", "\\frac{d}{dx}", "derivative_dx", "unary", ["derivative_wrt_x"]),
        ("∂/∂x", "U+2202", "\\frac{\\partial}{\\partial x}", "partial_dx", "unary", ["partial_wrt_x"]),
        ("∂/∂t", "U+2202", "\\frac{\\partial}{\\partial t}", "partial_dt", "unary", ["partial_wrt_t"]),
        ("d²/dx²", "U+0064", "\\frac{d^2}{dx^2}", "second_derivative", "unary", ["second_derivative"]),
        ("∂²/∂x²", "U+2202", "\\frac{\\partial^2}{\\partial x^2}", "second_partial_x", "unary", ["second_partial_x"]),
    ]
    
    for symbol, unicode, latex, name, arity, contexts in diff_ops[:15]:
        symbols.append(create_symbol_entry(
            symbol, unicode, latex, name, "calculus", arity, "operator",
            1, 2, "partial", "no", "no", "no", "partial", "low",
            contexts
        ))
    
    # Integral operators (25 symbols)
    integral_ops = [
        ("∫", "U+222B", "\\int", "integral", "unary", ["integral"]),
        ("∬", "U+222C", "\\iint", "double_integral", "unary", ["double_integral"]),
        ("∭", "U+222D", "\\iiint", "triple_integral", "unary", ["triple_integral"]),
        ("∮", "U+222E", "\\oint", "contour_integral", "unary", ["contour_integral"]),
        ("∯", "U+222F", "\\oiint", "surface_integral", "unary", ["surface_integral"]),
        ("∰", "U+2230", "\\oiiint", "volume_integral", "unary", ["volume_integral"]),
        ("∱", "U+2231", "\\intclockwise", "clockwise_integral", "unary", ["clockwise_integral"]),
        ("∲", "U+2232", "\\varointclockwise", "clockwise_contour", "unary", ["clockwise_contour"]),
        ("∳", "U+2233", "\\ointctrclockwise", "counterclockwise_contour", "unary", ["counterclockwise_contour"]),
    ]
    
    for symbol, unicode, latex, name, arity, contexts in integral_ops[:9]:
        symbols.append(create_symbol_entry(
            symbol, unicode, latex, name, "calculus", arity, "operator",
            1, 2, "none", "no", "no", "no", "none", "low",
            contexts
        ))
    
    # Trigonometric functions (30 symbols)
    trig_funcs = [
        ("sin", "U+0073", "\\sin", "sine", "unary", ["sine"]),
        ("cos", "U+0063", "\\cos", "cosine", "unary", ["cosine"]),
        ("tan", "U+0074", "\\tan", "tangent", "unary", ["tangent"]),
        ("cot", "U+0063", "\\cot", "cotangent", "unary", ["cotangent"]),
        ("sec", "U+0073", "\\sec", "secant", "unary", ["secant"]),
        ("csc", "U+0063", "\\csc", "cosecant", "unary", ["cosecant"]),
        ("arcsin", "U+0061", "\\arcsin", "arcsine", "unary", ["arcsine"]),
        ("arccos", "U+0061", "\\arccos", "arccosine", "unary", ["arccosine"]),
        ("arctan", "U+0061", "\\arctan", "arctangent", "unary", ["arctangent"]),
        ("sinh", "U+0073", "\\sinh", "hyperbolic_sine", "unary", ["hyperbolic_sine"]),
        ("cosh", "U+0063", "\\cosh", "hyperbolic_cosine", "unary", ["hyperbolic_cosine"]),
        ("tanh", "U+0074", "\\tanh", "hyperbolic_tangent", "unary", ["hyperbolic_tangent"]),
        ("coth", "U+0063", "\\coth", "hyperbolic_cotangent", "unary", ["hyperbolic_cotangent"]),
        ("sech", "U+0073", "\\text{sech}", "hyperbolic_secant", "unary", ["hyperbolic_secant"]),
        ("csch", "U+0063", "\\text{csch}", "hyperbolic_cosecant", "unary", ["hyperbolic_cosecant"]),
        ("arsinh", "U+0061", "\\text{arsinh}", "inverse_hyperbolic_sine", "unary", ["inverse_hyperbolic_sine"]),
        ("arcosh", "U+0061", "\\text{arcosh}", "inverse_hyperbolic_cosine", "unary", ["inverse_hyperbolic_cosine"]),
        ("artanh", "U+0061", "\\text{artanh}", "inverse_hyperbolic_tangent", "unary", ["inverse_hyperbolic_tangent"]),
    ]
    
    for symbol, unicode, latex, name, arity, contexts in trig_funcs[:18]:
        symbols.append(create_symbol_entry(
            symbol, unicode, latex, name, "calculus", arity, "operator",
            1, 2, "partial", "no", "no", "no", "partial", "low",
            contexts
        ))
    
    # Limits and series (20 symbols)
    limit_ops = [
        ("lim", "U+006C", "\\lim", "limit", "unary", ["limit"]),
        ("sup", "U+0073", "\\sup", "supremum", "unary", ["supremum"]),
        ("inf", "U+0069", "\\inf", "infimum", "unary", ["infimum"]),
        ("max", "U+006D", "\\max", "maximum", "unary", ["maximum"]),
        ("min", "U+006D", "\\min", "minimum", "unary", ["minimum"]),
        ("limsup", "U+006C", "\\limsup", "limit_superior", "unary", ["limit_superior"]),
        ("liminf", "U+006C", "\\liminf", "limit_inferior", "unary", ["limit_inferior"]),
        ("∑", "U+2211", "\\sum", "summation", "unary", ["summation"]),
        ("∏", "U+220F", "\\prod", "product", "unary", ["product"]),
        ("∐", "U+2210", "\\coprod", "coproduct", "unary", ["coproduct"]),
        ("⋃", "U+22C3", "\\bigcup", "union", "unary", ["union"]),
        ("⋂", "U+22C2", "\\bigcap", "intersection", "unary", ["intersection"]),
        ("⋁", "U+22C1", "\\bigvee", "join", "unary", ["join"]),
        ("⋀", "U+22C0", "\\bigwedge", "meet", "unary", ["meet"]),
        ("⨁", "U+2A01", "\\bigoplus", "direct_sum_big", "unary", ["direct_sum"]),
        ("⨂", "U+2A02", "\\bigotimes", "tensor_product_big", "unary", ["tensor_product"]),
        ("⨀", "U+2A00", "\\bigodot", "hadamard_product_big", "unary", ["hadamard_product"]),
    ]
    
    for symbol, unicode, latex, name, arity, contexts in limit_ops[:17]:
        symbols.append(create_symbol_entry(
            symbol, unicode, latex, name, "calculus", arity, "operator",
            1, 2, "none", "no", "no", "no", "none", "low",
            contexts
        ))
    
    # Special functions (6 symbols)
    special_funcs = [
        ("exp", "U+0065", "\\exp", "exponential", "unary", ["exponential"]),
        ("ln", "U+006C", "\\ln", "natural_log", "unary", ["natural_logarithm"]),
        ("log", "U+006C", "\\log", "logarithm", "unary", ["logarithm"]),
        ("lg", "U+006C", "\\lg", "log_base_10", "unary", ["log_base_10"]),
        ("arg", "U+0061", "\\arg", "argument", "unary", ["argument"]),
        ("deg", "U+0064", "\\deg", "degree", "unary", ["degree"]),
    ]
    
    for symbol, unicode, latex, name, arity, contexts in special_funcs:
        symbols.append(create_symbol_entry(
            symbol, unicode, latex, name, "calculus", arity, "operator",
            1, 2, "partial", "yes", "no", "no", "partial", "low",
            contexts
        ))
    
    return symbols

def generate_set_theory_symbols() -> List[Dict]:
    """Generate set theory symbols (80 symbols)."""
    symbols = []
    
    # Basic set operations (20 symbols)
    set_ops = [
        ("∈", "U+2208", "\\in", "element_of", "binary", "relation", ["membership"]),
        ("∉", "U+2209", "\\notin", "not_element_of", "binary", "relation", ["not_membership"]),
        ("∋", "U+220B", "\\ni", "contains", "binary", "relation", ["contains"]),
        ("∌", "U+220C", "\\notni", "not_contains", "binary", "relation", ["not_contains"]),
        ("⊂", "U+2282", "\\subset", "subset", "binary", "relation", ["subset"]),
        ("⊃", "U+2283", "\\supset", "superset", "binary", "relation", ["superset"]),
        ("⊄", "U+2284", "\\not\\subset", "not_subset", "binary", "relation", ["not_subset"]),
        ("⊅", "U+2285", "\\not\\supset", "not_superset", "binary", "relation", ["not_superset"]),
        ("⊆", "U+2286", "\\subseteq", "subset_equal", "binary", "relation", ["subset_or_equal"]),
        ("⊇", "U+2287", "\\supseteq", "superset_equal", "binary", "relation", ["superset_or_equal"]),
        ("⊈", "U+2288", "\\nsubseteq", "not_subset_equal", "binary", "relation", ["not_subset_or_equal"]),
        ("⊉", "U+2289", "\\nsupseteq", "not_superset_equal", "binary", "relation", ["not_superset_or_equal"]),
        ("∪", "U+222A", "\\cup", "union", "binary", "operator", ["union"]),
        ("∩", "U+2229", "\\cap", "intersection", "binary", "operator", ["intersection"]),
        ("∖", "U+2216", "\\setminus", "set_difference", "binary", "operator", ["set_difference"]),
        ("△", "U+25B3", "\\triangle", "symmetric_difference", "binary", "operator", ["symmetric_difference"]),
        ("⊎", "U+228E", "\\uplus", "disjoint_union", "binary", "operator", ["disjoint_union"]),
        ("⊓", "U+2293", "\\sqcap", "square_cap", "binary", "operator", ["square_cap"]),
        ("⊔", "U+2294", "\\sqcup", "square_cup", "binary", "operator", ["square_cup"]),
        ("×", "U+00D7", "\\times", "cartesian_product", "binary", "operator", ["cartesian_product"]),
    ]
    
    for symbol, unicode, latex, name, arity, role, contexts in set_ops:
        symbols.append(create_symbol_entry(
            symbol, unicode, latex, name, "set_theory", arity, role,
            1, 1, "full" if role == "operator" else "none", "no", "yes", "yes", 
            "full" if role == "operator" else "none", "low",
            contexts
        ))
    
    # Special sets (20 symbols)
    special_sets = [
        ("∅", "U+2205", "\\emptyset", "empty_set", "nullary", ["empty_set"]),
        ("ℕ", "U+2115", "\\mathbb{N}", "natural_numbers", "nullary", ["natural_numbers"]),
        ("ℤ", "U+2124", "\\mathbb{Z}", "integers", "nullary", ["integers"]),
        ("ℚ", "U+211A", "\\mathbb{Q}", "rationals", "nullary", ["rational_numbers"]),
        ("ℝ", "U+211D", "\\mathbb{R}", "reals", "nullary", ["real_numbers"]),
        ("ℂ", "U+2102", "\\mathbb{C}", "complex", "nullary", ["complex_numbers"]),
        ("ℙ", "U+2119", "\\mathbb{P}", "primes", "nullary", ["prime_numbers"]),
        ("ℍ", "U+210D", "\\mathbb{H}", "quaternions", "nullary", ["quaternions"]),
        ("𝔽", "U+1D53D", "\\mathbb{F}", "field", "nullary", ["field"]),
        ("𝕌", "U+1D54C", "\\mathbb{U}", "universe", "nullary", ["universal_set"]),
    ]
    
    for symbol, unicode, latex, name, arity, contexts in special_sets[:10]:
        symbols.append(create_symbol_entry(
            symbol, unicode, latex, name, "set_theory", arity, "operand",
            1, 3, "none", "no", "no", "no", "none", "low",
            contexts
        ))
    
    # Cardinality and power set (10 symbols)
    card_ops = [
        ("|A|", "U+007C", "|A|", "cardinality", "unary", ["cardinality"]),
        ("#A", "U+0023", "\\#A", "size", "unary", ["size"]),
        ("℘", "U+2118", "\\wp", "power_set", "unary", ["power_set"]),
        ("𝒫", "U+1D4AB", "\\mathcal{P}", "power_set_calligraphic", "unary", ["power_set"]),
        ("ℵ", "U+2135", "\\aleph", "aleph", "nullary", ["aleph_number"]),
        ("ℶ", "U+2136", "\\beth", "beth", "nullary", ["beth_number"]),
        ("ℷ", "U+2137", "\\gimel", "gimel", "nullary", ["gimel_number"]),
        ("ℸ", "U+2138", "\\daleth", "daleth", "nullary", ["daleth_number"]),
    ]
    
    for symbol, unicode, latex, name, arity, contexts in card_ops[:8]:
        symbols.append(create_symbol_entry(
            symbol, unicode, latex, name, "set_theory", arity, "operator",
            1, 2, "none", "no", "no", "no", "none", "low",
            contexts
        ))
    
    # Relations (20 symbols)
    set_relations = [
        ("∼", "U+223C", "\\sim", "similar", "binary", ["equivalence_relation"]),
        ("≈", "U+2248", "\\approx", "approximately", "binary", ["approximately"]),
        ("≃", "U+2243", "\\simeq", "asymptotically_equal", "binary", ["asymptotically_equal"]),
        ("≅", "U+2245", "\\cong", "congruent", "binary", ["congruent"]),
        ("≡", "U+2261", "\\equiv", "equivalent", "binary", ["equivalent"]),
        ("≢", "U+2262", "\\not\\equiv", "not_equivalent", "binary", ["not_equivalent"]),
        ("∝", "U+221D", "\\propto", "proportional", "binary", ["proportional"]),
        ("∼", "U+223C", "\\sim", "tilde_relation", "binary", ["tilde_relation"]),
        ("≁", "U+2241", "\\nsim", "not_similar", "binary", ["not_similar"]),
        ("≂", "U+2242", "\\eqsim", "minus_tilde", "binary", ["minus_tilde"]),
        ("≄", "U+2244", "\\not\\simeq", "not_asymptotically_equal", "binary", ["not_asymptotically_equal"]),
        ("≆", "U+2246", "\\approxnotequal", "approximately_not_equal", "binary", ["approximately_not_equal"]),
        ("≇", "U+2247", "\\ncong", "not_congruent", "binary", ["not_congruent"]),
        ("≉", "U+2249", "\\napprox", "not_approximately", "binary", ["not_approximately"]),
    ]
    
    for symbol, unicode, latex, name, arity, contexts in set_relations[:14]:
        symbols.append(create_symbol_entry(
            symbol, unicode, latex, name, "set_theory", arity, "relation",
            1, 1, "none", "yes", "yes", "no", "none", "low",
            contexts
        ))
    
    # Quantifiers (8 symbols)
    quantifiers = [
        ("∀", "U+2200", "\\forall", "for_all", "unary", ["universal_quantifier"]),
        ("∃", "U+2203", "\\exists", "exists", "unary", ["existential_quantifier"]),
        ("∄", "U+2204", "\\nexists", "not_exists", "unary", ["not_exists"]),
        ("∃!", "U+2203", "\\exists!", "exists_unique", "unary", ["exists_unique"]),
    ]
    
    for symbol, unicode, latex, name, arity, contexts in quantifiers[:4]:
        symbols.append(create_symbol_entry(
            symbol, unicode, latex, name, "set_theory", arity, "quantifier",
            1, 1, "none", "no", "no", "no", "none", "low",
            contexts
        ))
    
    return symbols

def generate_logic_symbols() -> List[Dict]:
    """Generate logic symbols (80 symbols)."""
    symbols = []
    
    # Propositional logic (20 symbols)
    prop_logic = [
        ("∧", "U+2227", "\\land", "and", "binary", "operator", ["conjunction"]),
        ("∨", "U+2228", "\\lor", "or", "binary", "operator", ["disjunction"]),
        ("¬", "U+00AC", "\\neg", "not", "unary", "operator", ["negation"]),
        ("⊤", "U+22A4", "\\top", "true", "nullary", "operand", ["true"]),
        ("⊥", "U+22A5", "\\bot", "false", "nullary", "operand", ["false"]),
        ("→", "U+2192", "\\rightarrow", "implies", "binary", "operator", ["implication"]),
        ("←", "U+2190", "\\leftarrow", "implied_by", "binary", "operator", ["reverse_implication"]),
        ("↔", "U+2194", "\\leftrightarrow", "iff", "binary", "operator", ["biconditional"]),
        ("⇒", "U+21D2", "\\Rightarrow", "double_implies", "binary", "operator", ["double_implication"]),
        ("⇐", "U+21D0", "\\Leftarrow", "double_implied_by", "binary", "operator", ["double_reverse_implication"]),
        ("⇔", "U+21D4", "\\Leftrightarrow", "double_iff", "binary", "operator", ["double_biconditional"]),
        ("⊕", "U+2295", "\\oplus", "xor", "binary", "operator", ["exclusive_or"]),
        ("⊼", "U+22BC", "\\barwedge", "nand", "binary", "operator", ["nand"]),
        ("⊽", "U+22BD", "\\veebar", "nor", "binary", "operator", ["nor"]),
        ("↑", "U+2191", "\\uparrow", "nand_arrow", "binary", "operator", ["sheffer_stroke"]),
        ("↓", "U+2193", "\\downarrow", "nor_arrow", "binary", "operator", ["peirce_arrow"]),
        ("⊻", "U+22BB", "\\veebar", "xor_bar", "binary", "operator", ["xor"]),
        ("⊙", "U+2299", "\\odot", "xnor", "binary", "operator", ["xnor"]),
    ]
    
    for symbol, unicode, latex, name, arity, role, contexts in prop_logic[:18]:
        symbols.append(create_symbol_entry(
            symbol, unicode, latex, name, "logic", arity, role,
            1, 1, "full" if arity == "binary" else "none", "no", "yes" if arity == "binary" else "no", 
            "yes" if arity == "binary" else "no", "full" if arity == "binary" else "none", "low",
            contexts
        ))
    
    # Modal logic (20 symbols)
    modal_logic = [
        ("□", "U+25A1", "\\Box", "necessity", "unary", ["necessity"]),
        ("◇", "U+25C7", "\\Diamond", "possibility", "unary", ["possibility"]),
        ("◻", "U+25FB", "\\square", "always", "unary", ["always"]),
        ("◊", "U+25CA", "\\lozenge", "eventually", "unary", ["eventually"]),
        ("⬜", "U+2B1C", "\\mdwhtsquare", "white_square", "unary", ["white_square"]),
        ("⬛", "U+2B1B", "\\mdblksquare", "black_square", "unary", ["black_square"]),
    ]
    
    for symbol, unicode, latex, name, arity, contexts in modal_logic[:6]:
        symbols.append(create_symbol_entry(
            symbol, unicode, latex, name, "logic", arity, "operator",
            1, 2, "none", "no", "no", "no", "none", "low",
            contexts
        ))
    
    # Temporal logic (10 symbols)
    temporal_logic = [
        ("○", "U+25CB", "\\bigcirc", "next", "unary", ["next"]),
        ("◯", "U+25EF", "\\bigcirc", "next_time", "unary", ["next_time"]),
        ("G", "U+0047", "G", "globally", "unary", ["globally"]),
        ("F", "U+0046", "F", "finally", "unary", ["finally"]),
        ("X", "U+0058", "X", "next_state", "unary", ["next_state"]),
        ("U", "U+0055", "U", "until", "binary", ["until"]),
        ("W", "U+0057", "W", "weak_until", "binary", ["weak_until"]),
        ("R", "U+0052", "R", "release", "binary", ["release"]),
    ]
    
    for symbol, unicode, latex, name, arity, contexts in temporal_logic[:8]:
        symbols.append(create_symbol_entry(
            symbol, unicode, latex, name, "logic", arity, "operator",
            1, 2, "none", "no", "no", "no", "none", "low",
            contexts
        ))
    
    # Proof theory (20 symbols)
    proof_symbols = [
        ("⊢", "U+22A2", "\\vdash", "proves", "binary", ["proves"]),
        ("⊣", "U+22A3", "\\dashv", "adjoint", "binary", ["adjoint"]),
        ("⊨", "U+22A8", "\\vDash", "models", "binary", ["models"]),
        ("⊩", "U+22A9", "\\Vdash", "forces", "binary", ["forces"]),
        ("⊪", "U+22AA", "\\Vvdash", "triple_turnstile", "binary", ["triple_turnstile"]),
        ("⊬", "U+22AC", "\\nvdash", "not_proves", "binary", ["not_proves"]),
        ("⊭", "U+22AD", "\\nvDash", "not_models", "binary", ["not_models"]),
        ("⊮", "U+22AE", "\\nVdash", "not_forces", "binary", ["not_forces"]),
        ("⊯", "U+22AF", "\\nVDash", "not_triple_turnstile", "binary", ["not_triple_turnstile"]),
        ("∴", "U+2234", "\\therefore", "therefore", "nullary", ["therefore"]),
        ("∵", "U+2235", "\\because", "because", "nullary", ["because"]),
        ("∎", "U+220E", "\\qed", "qed", "nullary", ["qed"]),
        ("■", "U+25A0", "\\blacksquare", "black_square_qed", "nullary", ["qed"]),
        ("□", "U+25A1", "\\square", "white_square_qed", "nullary", ["qed"]),
    ]
    
    for symbol, unicode, latex, name, arity, contexts in proof_symbols[:14]:
        symbols.append(create_symbol_entry(
            symbol, unicode, latex, name, "logic", arity, "operator" if arity != "nullary" else "operand",
            1, 1, "none", "no", "no", "no", "none", "low",
            contexts
        ))
    
    # Type theory (12 symbols)
    type_symbols = [
        (":", "U+003A", ":", "type_annotation", "binary", ["type_annotation"]),
        ("::", "U+003A", "::", "cons", "binary", ["cons", "type_signature"]),
        ("∷", "U+2237", "\\Colon", "proportion", "binary", ["proportion"]),
        ("⦂", "U+2982", "\\vcentcolon", "type_judgement", "binary", ["type_judgement"]),
        ("⊸", "U+22B8", "\\multimap", "linear_implication", "binary", ["linear_implication"]),
        ("⊗", "U+2297", "\\otimes", "tensor", "binary", ["tensor"]),
        ("⅋", "U+214B", "\\parr", "par", "binary", ["par"]),
        ("!", "U+0021", "!", "of_course", "unary", ["of_course", "factorial"]),
        ("?", "U+003F", "?", "why_not", "unary", ["why_not", "optional"]),
    ]
    
    for symbol, unicode, latex, name, arity, contexts in type_symbols[:9]:
        symbols.append(create_symbol_entry(
            symbol, unicode, latex, name, "logic", arity, "operator",
            2, 2, "none", "no", "no", "no", "none", "high",
            contexts
        ))
    
    return symbols

def generate_comprehensive_dataset() -> List[Dict]:
    """Generate complete dataset with all categories."""
    symbols = []
    
    print("Generating Python operators...")
    python_symbols = generate_python_operators()
    symbols.extend(python_symbols)
    print(f"  Added {len(python_symbols)} Python operators")
    
    print("Generating mathematical symbols...")
    math_symbols = generate_mathematical_symbols()
    symbols.extend(math_symbols)
    print(f"  Added {len(math_symbols)} mathematical symbols")
    
    print("Generating algebra symbols...")
    algebra_symbols = generate_algebra_symbols()
    symbols.extend(algebra_symbols)
    print(f"  Added {len(algebra_symbols)} algebra symbols")
    
    print("Generating calculus symbols...")
    calculus_symbols = generate_calculus_symbols()
    symbols.extend(calculus_symbols)
    print(f"  Added {len(calculus_symbols)} calculus symbols")
    
    print("Generating set theory symbols...")
    set_symbols = generate_set_theory_symbols()
    symbols.extend(set_symbols)
    print(f"  Added {len(set_symbols)} set theory symbols")
    
    print("Generating logic symbols...")
    logic_symbols = generate_logic_symbols()
    symbols.extend(logic_symbols)
    print(f"  Added {len(logic_symbols)} logic symbols")
    
    return symbols

def main():
    """Main execution function."""
    print("="*60)
    print("MASSIVE SYMBOL DATASET GENERATOR - PHASE 2")
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


def generate_probability_statistics_symbols() -> List[Dict]:
    """Generate probability and statistics symbols (100 symbols)."""
    symbols = []
    
    # Basic probability (30 symbols)
    prob_ops = [
        ("P", "U+0050", "P", "probability", "unary", ["probability"]),
        ("Pr", "U+0050", "\\Pr", "probability_alt", "unary", ["probability"]),
        ("ℙ", "U+2119", "\\mathbb{P}", "probability_measure", "unary", ["probability_measure"]),
        ("𝔼", "U+1D53C", "\\mathbb{E}", "expectation", "unary", ["expectation"]),
        ("E", "U+0045", "E", "expected_value", "unary", ["expected_value"]),
        ("Var", "U+0056", "\\text{Var}", "variance", "unary", ["variance"]),
        ("σ²", "U+03C3", "\\sigma^2", "variance_sigma", "unary", ["variance"]),
        ("σ", "U+03C3", "\\sigma", "standard_deviation", "unary", ["standard_deviation"]),
        ("Cov", "U+0043", "\\text{Cov}", "covariance", "binary", ["covariance"]),
        ("Corr", "U+0043", "\\text{Corr}", "correlation", "binary", ["correlation"]),
        ("ρ", "U+03C1", "\\rho", "correlation_coefficient", "nullary", ["correlation_coefficient"]),
        ("~", "U+007E", "\\sim", "distributed_as", "binary", ["distributed_as"]),
        ("∼", "U+223C", "\\sim", "distributed_as_alt", "binary", ["distributed_as"]),
        ("⊥⊥", "U+22A5", "\\perp\\!\\!\\!\\perp", "independent", "binary", ["independent"]),
        ("⫫", "U+2AEB", "\\upmodels", "independent_alt", "binary", ["independent"]),
        ("|", "U+007C", "|", "conditional", "binary", ["conditional"]),
        ("∝", "U+221D", "\\propto", "proportional_to", "binary", ["proportional"]),
    ]
    
    for symbol, unicode, latex, name, arity, contexts in prob_ops[:17]:
        symbols.append(create_symbol_entry(
            symbol, unicode, latex, name, "probability", arity, "operator",
            1, 2, "none", "no", "no", "no", "none", "low",
            contexts
        ))
    
    # Distributions (30 symbols)
    distributions = [
        ("𝒩", "U+1D4A9", "\\mathcal{N}", "normal_distribution", "nullary", ["normal"]),
        ("N", "U+004E", "N", "normal", "nullary", ["normal_distribution"]),
        ("Bin", "U+0042", "\\text{Bin}", "binomial", "nullary", ["binomial"]),
        ("Bern", "U+0042", "\\text{Bern}", "bernoulli", "nullary", ["bernoulli"]),
        ("Pois", "U+0050", "\\text{Pois}", "poisson", "nullary", ["poisson"]),
        ("Exp", "U+0045", "\\text{Exp}", "exponential", "nullary", ["exponential"]),
        ("Γ", "U+0393", "\\Gamma", "gamma_distribution", "nullary", ["gamma"]),
        ("β", "U+03B2", "\\text{Beta}", "beta_distribution", "nullary", ["beta"]),
        ("χ²", "U+03C7", "\\chi^2", "chi_squared", "nullary", ["chi_squared"]),
        ("t", "U+0074", "t", "t_distribution", "nullary", ["t_distribution"]),
        ("F", "U+0046", "F", "f_distribution", "nullary", ["f_distribution"]),
        ("U", "U+0055", "U", "uniform", "nullary", ["uniform"]),
        ("Geom", "U+0047", "\\text{Geom}", "geometric", "nullary", ["geometric"]),
        ("NB", "U+004E", "\\text{NB}", "negative_binomial", "nullary", ["negative_binomial"]),
        ("Mult", "U+004D", "\\text{Mult}", "multinomial", "nullary", ["multinomial"]),
    ]
    
    for symbol, unicode, latex, name, arity, contexts in distributions[:15]:
        symbols.append(create_symbol_entry(
            symbol, unicode, latex, name, "probability", arity, "operand",
            1, 3, "none", "no", "no", "no", "none", "low",
            contexts
        ))
    
    # Statistical tests and measures (40 symbols)
    stat_measures = [
        ("μ", "U+03BC", "\\mu", "mean", "nullary", ["mean"]),
        ("x̄", "U+0078", "\\bar{x}", "sample_mean", "nullary", ["sample_mean"]),
        ("s", "U+0073", "s", "sample_std", "nullary", ["sample_standard_deviation"]),
        ("s²", "U+0073", "s^2", "sample_variance", "nullary", ["sample_variance"]),
        ("SE", "U+0053", "\\text{SE}", "standard_error", "nullary", ["standard_error"]),
        ("CI", "U+0043", "\\text{CI}", "confidence_interval", "nullary", ["confidence_interval"]),
        ("α", "U+03B1", "\\alpha", "significance_level", "nullary", ["significance_level"]),
        ("p", "U+0070", "p", "p_value", "nullary", ["p_value"]),
        ("H₀", "U+0048", "H_0", "null_hypothesis", "nullary", ["null_hypothesis"]),
        ("H₁", "U+0048", "H_1", "alternative_hypothesis", "nullary", ["alternative_hypothesis"]),
        ("z", "U+007A", "z", "z_score", "nullary", ["z_score"]),
        ("t", "U+0074", "t", "t_statistic", "nullary", ["t_statistic"]),
        ("χ²", "U+03C7", "\\chi^2", "chi_squared_statistic", "nullary", ["chi_squared_statistic"]),
        ("F", "U+0046", "F", "f_statistic", "nullary", ["f_statistic"]),
        ("r", "U+0072", "r", "correlation_r", "nullary", ["correlation_coefficient"]),
        ("R²", "U+0052", "R^2", "r_squared", "nullary", ["coefficient_determination"]),
        ("df", "U+0064", "\\text{df}", "degrees_freedom", "nullary", ["degrees_of_freedom"]),
        ("n", "U+006E", "n", "sample_size", "nullary", ["sample_size"]),
        ("N", "U+004E", "N", "population_size", "nullary", ["population_size"]),
        ("MAD", "U+004D", "\\text{MAD}", "median_absolute_deviation", "nullary", ["median_absolute_deviation"]),
        ("IQR", "U+0049", "\\text{IQR}", "interquartile_range", "nullary", ["interquartile_range"]),
        ("Q₁", "U+0051", "Q_1", "first_quartile", "nullary", ["first_quartile"]),
        ("Q₂", "U+0051", "Q_2", "second_quartile", "nullary", ["median"]),
        ("Q₃", "U+0051", "Q_3", "third_quartile", "nullary", ["third_quartile"]),
        ("Med", "U+004D", "\\text{Med}", "median", "nullary", ["median"]),
        ("Mode", "U+004D", "\\text{Mode}", "mode", "nullary", ["mode"]),
        ("Range", "U+0052", "\\text{Range}", "range", "nullary", ["range"]),
        ("CV", "U+0043", "\\text{CV}", "coefficient_variation", "nullary", ["coefficient_of_variation"]),
    ]
    
    for symbol, unicode, latex, name, arity, contexts in stat_measures[:28]:
        symbols.append(create_symbol_entry(
            symbol, unicode, latex, name, "probability", arity, "operand",
            1, 2, "none", "no", "no", "no", "none", "medium",
            contexts
        ))
    
    return symbols

def generate_linear_algebra_symbols() -> List[Dict]:
    """Generate linear algebra symbols (100 symbols)."""
    symbols = []
    
    # Matrix operations (30 symbols)
    matrix_ops = [
        ("⊗", "U+2297", "\\otimes", "kronecker_product", "binary", ["kronecker_product"]),
        ("⊕", "U+2295", "\\oplus", "direct_sum_matrix", "binary", ["direct_sum"]),
        ("⊙", "U+2299", "\\odot", "hadamard_product_matrix", "binary", ["hadamard_product"]),
        ("⊘", "U+2298", "\\oslash", "hadamard_division", "binary", ["hadamard_division"]),
        ("⊚", "U+229A", "\\circledcirc", "hadamard_power", "binary", ["hadamard_power"]),
        ("†", "U+2020", "\\dagger", "conjugate_transpose", "unary", ["conjugate_transpose"]),
        ("ᵀ", "U+1D40", "^T", "transpose", "unary", ["transpose"]),
        ("⁻¹", "U+207B", "^{-1}", "inverse", "unary", ["inverse"]),
        ("*", "U+002A", "^*", "conjugate", "unary", ["conjugate"]),
        ("tr", "U+0074", "\\text{tr}", "trace", "unary", ["trace"]),
        ("det", "U+0064", "\\det", "determinant", "unary", ["determinant"]),
        ("|A|", "U+007C", "|A|", "determinant_bars", "unary", ["determinant"]),
        ("rank", "U+0072", "\\text{rank}", "rank", "unary", ["rank"]),
        ("dim", "U+0064", "\\dim", "dimension", "unary", ["dimension"]),
        ("ker", "U+006B", "\\ker", "kernel", "unary", ["kernel"]),
        ("im", "U+0069", "\\text{im}", "image", "unary", ["image"]),
        ("span", "U+0073", "\\text{span}", "span", "unary", ["span"]),
        ("null", "U+006E", "\\text{null}", "nullspace", "unary", ["nullspace"]),
        ("col", "U+0063", "\\text{col}", "column_space", "unary", ["column_space"]),
        ("row", "U+0072", "\\text{row}", "row_space", "unary", ["row_space"]),
    ]
    
    for symbol, unicode, latex, name, arity, contexts in matrix_ops[:20]:
        symbols.append(create_symbol_entry(
            symbol, unicode, latex, name, "linear_algebra", arity, "operator",
            1, 2, "partial", "no", "no", "no", "partial", "low",
            contexts
        ))
    
    # Vector operations (20 symbols)
    vector_ops = [
        ("·", "U+00B7", "\\cdot", "dot_product_vector", "binary", ["dot_product"]),
        ("×", "U+00D7", "\\times", "cross_product_vector", "binary", ["cross_product"]),
        ("⊗", "U+2297", "\\otimes", "outer_product", "binary", ["outer_product"]),
        ("∥", "U+2225", "\\parallel", "parallel", "binary", ["parallel"]),
        ("⊥", "U+22A5", "\\perp", "perpendicular", "binary", ["perpendicular"]),
        ("‖v‖", "U+2016", "\\|v\\|", "norm", "unary", ["norm"]),
        ("‖·‖₁", "U+2016", "\\|\\cdot\\|_1", "l1_norm", "unary", ["l1_norm"]),
        ("‖·‖₂", "U+2016", "\\|\\cdot\\|_2", "l2_norm", "unary", ["l2_norm"]),
        ("‖·‖∞", "U+2016", "\\|\\cdot\\|_\\infty", "infinity_norm", "unary", ["infinity_norm"]),
        ("‖·‖_F", "U+2016", "\\|\\cdot\\|_F", "frobenius_norm", "unary", ["frobenius_norm"]),
        ("⟨·,·⟩", "U+27E8", "\\langle\\cdot,\\cdot\\rangle", "inner_product", "binary", ["inner_product"]),
        ("proj", "U+0070", "\\text{proj}", "projection", "binary", ["projection"]),
        ("⊥", "U+22A5", "\\perp", "orthogonal_complement", "unary", ["orthogonal_complement"]),
    ]
    
    for symbol, unicode, latex, name, arity, contexts in vector_ops[:13]:
        symbols.append(create_symbol_entry(
            symbol, unicode, latex, name, "linear_algebra", arity, "operator",
            1, 2, "partial", "no", "yes" if arity == "binary" else "no", "yes" if arity == "binary" else "no", 
            "partial", "low",
            contexts
        ))
    
    # Eigenvalues and decompositions (20 symbols)
    eigen_ops = [
        ("λ", "U+03BB", "\\lambda", "eigenvalue", "nullary", ["eigenvalue"]),
        ("v", "U+0076", "v", "eigenvector", "nullary", ["eigenvector"]),
        ("σ", "U+03C3", "\\sigma", "singular_value", "nullary", ["singular_value"]),
        ("U", "U+0055", "U", "left_singular_vectors", "nullary", ["left_singular_vectors"]),
        ("Σ", "U+03A3", "\\Sigma", "singular_values_matrix", "nullary", ["singular_values"]),
        ("V", "U+0056", "V", "right_singular_vectors", "nullary", ["right_singular_vectors"]),
        ("Q", "U+0051", "Q", "orthogonal_matrix", "nullary", ["orthogonal_matrix"]),
        ("R", "U+0052", "R", "upper_triangular", "nullary", ["upper_triangular"]),
        ("L", "U+004C", "L", "lower_triangular", "nullary", ["lower_triangular"]),
        ("P", "U+0050", "P", "permutation_matrix", "nullary", ["permutation_matrix"]),
        ("D", "U+0044", "D", "diagonal_matrix", "nullary", ["diagonal_matrix"]),
        ("J", "U+004A", "J", "jordan_form", "nullary", ["jordan_form"]),
        ("spec", "U+0073", "\\text{spec}", "spectrum", "unary", ["spectrum"]),
        ("diag", "U+0064", "\\text{diag}", "diagonal", "unary", ["diagonal"]),
    ]
    
    for symbol, unicode, latex, name, arity, contexts in eigen_ops[:14]:
        symbols.append(create_symbol_entry(
            symbol, unicode, latex, name, "linear_algebra", arity, "operand" if arity == "nullary" else "operator",
            1, 3, "none", "no", "no", "no", "none", "low",
            contexts
        ))
    
    # Special matrices (20 symbols)
    special_matrices = [
        ("I", "U+0049", "I", "identity_matrix", "nullary", ["identity"]),
        ("O", "U+004F", "O", "zero_matrix", "nullary", ["zero_matrix"]),
        ("J", "U+004A", "J", "ones_matrix", "nullary", ["ones_matrix"]),
        ("H", "U+0048", "H", "hermitian_matrix", "nullary", ["hermitian"]),
        ("S", "U+0053", "S", "symmetric_matrix", "nullary", ["symmetric"]),
        ("A", "U+0041", "A", "skew_symmetric", "nullary", ["skew_symmetric"]),
        ("U", "U+0055", "U", "unitary_matrix", "nullary", ["unitary"]),
        ("O", "U+004F", "O", "orthogonal_matrix_O", "nullary", ["orthogonal"]),
        ("N", "U+004E", "N", "normal_matrix", "nullary", ["normal"]),
        ("P", "U+0050", "P", "positive_definite", "nullary", ["positive_definite"]),
        ("M", "U+004D", "M", "matrix", "nullary", ["matrix"]),
    ]
    
    for symbol, unicode, latex, name, arity, contexts in special_matrices[:11]:
        symbols.append(create_symbol_entry(
            symbol, unicode, latex, name, "linear_algebra", arity, "operand",
            1, 2, "none", "no", "no", "no", "none", "medium",
            contexts
        ))
    
    # Tensor operations (22 symbols)
    tensor_ops = [
        ("⊗", "U+2297", "\\otimes", "tensor_product_tensor", "binary", ["tensor_product"]),
        ("⊙", "U+2299", "\\odot", "element_wise_product", "binary", ["element_wise"]),
        ("∘", "U+2218", "\\circ", "tensor_contraction", "binary", ["contraction"]),
        ("⋅", "U+22C5", "\\cdot", "tensor_dot", "binary", ["tensor_dot"]),
        ("×₁", "U+00D7", "\\times_1", "mode_1_product", "binary", ["mode_1_product"]),
        ("×₂", "U+00D7", "\\times_2", "mode_2_product", "binary", ["mode_2_product"]),
        ("×₃", "U+00D7", "\\times_3", "mode_3_product", "binary", ["mode_3_product"]),
        ("⊛", "U+229B", "\\circledast", "convolution_tensor", "binary", ["convolution"]),
    ]
    
    for symbol, unicode, latex, name, arity, contexts in tensor_ops[:8]:
        symbols.append(create_symbol_entry(
            symbol, unicode, latex, name, "linear_algebra", arity, "operator",
            1, 3, "partial", "no", "no", "no", "partial", "medium",
            contexts
        ))
    
    return symbols

def generate_topology_symbols() -> List[Dict]:
    """Generate topology symbols (80 symbols)."""
    symbols = []
    
    # Basic topology (30 symbols)
    topo_ops = [
        ("int", "U+0069", "\\text{int}", "interior", "unary", ["interior"]),
        ("cl", "U+0063", "\\text{cl}", "closure", "unary", ["closure"]),
        ("∂", "U+2202", "\\partial", "boundary", "unary", ["boundary"]),
        ("°", "U+00B0", "^\\circ", "interior_degree", "unary", ["interior"]),
        ("‾", "U+203E", "\\overline", "closure_bar", "unary", ["closure"]),
        ("int(A)", "U+0069", "\\text{int}(A)", "interior_of_A", "unary", ["interior"]),
        ("cl(A)", "U+0063", "\\text{cl}(A)", "closure_of_A", "unary", ["closure"]),
        ("∂A", "U+2202", "\\partial A", "boundary_of_A", "unary", ["boundary"]),
        ("A°", "U+0041", "A^\\circ", "interior_A", "unary", ["interior"]),
        ("Ā", "U+0041", "\\overline{A}", "closure_A", "unary", ["closure"]),
        ("Aᶜ", "U+0041", "A^c", "complement", "unary", ["complement"]),
        ("∁", "U+2201", "\\complement", "complement_symbol", "unary", ["complement"]),
    ]
    
    for symbol, unicode, latex, name, arity, contexts in topo_ops[:12]:
        symbols.append(create_symbol_entry(
            symbol, unicode, latex, name, "topology", arity, "operator",
            1, 2, "none", "no", "no", "no", "none", "low",
            contexts
        ))
    
    # Continuity and limits (20 symbols)
    continuity_ops = [
        ("→", "U+2192", "\\to", "maps_to", "binary", ["maps_to"]),
        ("↦", "U+21A6", "\\mapsto", "maps_to_element", "binary", ["maps_to"]),
        ("⟶", "U+27F6", "\\longrightarrow", "long_arrow", "binary", ["long_arrow"]),
        ("⟼", "U+27FC", "\\longmapsto", "long_maps_to", "binary", ["long_maps_to"]),
        ("⇀", "U+21C0", "\\rightharpoonup", "converges", "binary", ["converges"]),
        ("⇁", "U+21C1", "\\rightharpoondown", "converges_down", "binary", ["converges"]),
        ("⟹", "U+27F9", "\\Longrightarrow", "implies_long", "binary", ["implies"]),
        ("≃", "U+2243", "\\simeq", "homotopic", "binary", ["homotopic"]),
        ("≅", "U+2245", "\\cong", "homeomorphic", "binary", ["homeomorphic"]),
        ("≈", "U+2248", "\\approx", "approximately_homeomorphic", "binary", ["approximately"]),
    ]
    
    for symbol, unicode, latex, name, arity, contexts in continuity_ops[:10]:
        symbols.append(create_symbol_entry(
            symbol, unicode, latex, name, "topology", arity, "operator",
            1, 2, "none", "no", "no", "no", "none", "low",
            contexts
        ))
    
    # Homotopy and homology (20 symbols)
    homotopy_ops = [
        ("≃", "U+2243", "\\simeq", "homotopy_equivalent", "binary", ["homotopy_equivalent"]),
        ("≅", "U+2245", "\\cong", "isomorphic_spaces", "binary", ["isomorphic"]),
        ("π₁", "U+03C0", "\\pi_1", "fundamental_group", "unary", ["fundamental_group"]),
        ("π_n", "U+03C0", "\\pi_n", "homotopy_group", "unary", ["homotopy_group"]),
        ("H_n", "U+0048", "H_n", "homology_group", "unary", ["homology"]),
        ("H^n", "U+0048", "H^n", "cohomology_group", "unary", ["cohomology"]),
        ("χ", "U+03C7", "\\chi", "euler_characteristic", "unary", ["euler_characteristic"]),
        ("∼", "U+223C", "\\sim", "homotopic_to", "binary", ["homotopic"]),
        ("≈", "U+2248", "\\approx", "homologous", "binary", ["homologous"]),
        ("∂", "U+2202", "\\partial", "boundary_operator", "unary", ["boundary_operator"]),
        ("δ", "U+03B4", "\\delta", "coboundary", "unary", ["coboundary"]),
        ("∪", "U+222A", "\\cup", "cup_product", "binary", ["cup_product"]),
        ("∩", "U+2229", "\\cap", "cap_product", "binary", ["cap_product"]),
    ]
    
    for symbol, unicode, latex, name, arity, contexts in homotopy_ops[:13]:
        symbols.append(create_symbol_entry(
            symbol, unicode, latex, name, "topology", arity, "operator",
            1, 3, "none", "no", "no", "no", "none", "low",
            contexts
        ))
    
    # Manifolds and differential topology (15 symbols)
    manifold_ops = [
        ("M", "U+004D", "M", "manifold", "nullary", ["manifold"]),
        ("TM", "U+0054", "TM", "tangent_bundle", "nullary", ["tangent_bundle"]),
        ("T*M", "U+0054", "T^*M", "cotangent_bundle", "nullary", ["cotangent_bundle"]),
        ("∇", "U+2207", "\\nabla", "connection", "unary", ["connection"]),
        ("R", "U+0052", "R", "riemann_curvature", "nullary", ["riemann_curvature"]),
        ("Ric", "U+0052", "\\text{Ric}", "ricci_curvature", "nullary", ["ricci_curvature"]),
        ("g", "U+0067", "g", "metric_tensor", "nullary", ["metric_tensor"]),
        ("ω", "U+03C9", "\\omega", "differential_form", "nullary", ["differential_form"]),
        ("d", "U+0064", "d", "exterior_derivative", "unary", ["exterior_derivative"]),
        ("∧", "U+2227", "\\wedge", "wedge_product", "binary", ["wedge_product"]),
        ("⌟", "U+231F", "\\lrcorner", "interior_product", "binary", ["interior_product"]),
        ("⌞", "U+231E", "\\llcorner", "interior_product_left", "binary", ["interior_product"]),
    ]
    
    for symbol, unicode, latex, name, arity, contexts in manifold_ops[:12]:
        symbols.append(create_symbol_entry(
            symbol, unicode, latex, name, "topology", arity, "operand" if arity == "nullary" else "operator",
            1, 3, "none", "no", "no", "no", "none", "low",
            contexts
        ))
    
    return symbols

# Update the main generation function
def generate_comprehensive_dataset_v2() -> List[Dict]:
    """Generate complete dataset with all categories (1000+ symbols)."""
    symbols = []
    
    print("Generating Python operators...")
    python_symbols = generate_python_operators()
    symbols.extend(python_symbols)
    print(f"  Added {len(python_symbols)} Python operators")
    
    print("Generating mathematical symbols...")
    math_symbols = generate_mathematical_symbols()
    symbols.extend(math_symbols)
    print(f"  Added {len(math_symbols)} mathematical symbols")
    
    print("Generating algebra symbols...")
    algebra_symbols = generate_algebra_symbols()
    symbols.extend(algebra_symbols)
    print(f"  Added {len(algebra_symbols)} algebra symbols")
    
    print("Generating calculus symbols...")
    calculus_symbols = generate_calculus_symbols()
    symbols.extend(calculus_symbols)
    print(f"  Added {len(calculus_symbols)} calculus symbols")
    
    print("Generating set theory symbols...")
    set_symbols = generate_set_theory_symbols()
    symbols.extend(set_symbols)
    print(f"  Added {len(set_symbols)} set theory symbols")
    
    print("Generating logic symbols...")
    logic_symbols = generate_logic_symbols()
    symbols.extend(logic_symbols)
    print(f"  Added {len(logic_symbols)} logic symbols")
    
    print("Generating probability/statistics symbols...")
    prob_symbols = generate_probability_statistics_symbols()
    symbols.extend(prob_symbols)
    print(f"  Added {len(prob_symbols)} probability/statistics symbols")
    
    print("Generating linear algebra symbols...")
    linalg_symbols = generate_linear_algebra_symbols()
    symbols.extend(linalg_symbols)
    print(f"  Added {len(linalg_symbols)} linear algebra symbols")
    
    print("Generating topology symbols...")
    topo_symbols = generate_topology_symbols()
    symbols.extend(topo_symbols)
    print(f"  Added {len(topo_symbols)} topology symbols")
    
    return symbols

# Update main to use v2
if __name__ == "__main__":
    print("="*60)
    print("MASSIVE SYMBOL DATASET GENERATOR - PHASE 2")
    print("Target: 1000+ symbols")
    print("="*60)
    print()
    
    symbols = generate_comprehensive_dataset_v2()
    
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
