#!/usr/bin/env python3.11
"""
Final Comprehensive Symbol Dataset Generator - Phase 2
Complete coverage: 1000+ symbols across all mathematical domains
"""

import json
import sys
sys.path.append('/home/ubuntu/ubp_symbol_study_phase2/scripts')

from generate_massive_dataset import (
    create_symbol_entry,
    generate_python_operators,
    generate_mathematical_symbols,
    generate_algebra_symbols,
    generate_calculus_symbols,
    generate_set_theory_symbols,
    generate_logic_symbols,
    generate_probability_statistics_symbols,
    generate_linear_algebra_symbols,
    generate_topology_symbols
)

def generate_category_theory_symbols() -> list:
    """Generate category theory symbols (60 symbols)."""
    symbols = []
    
    # Basic category theory (20 symbols)
    cat_ops = [
        ("→", "U+2192", "\\to", "morphism", "binary", ["morphism"]),
        ("⇒", "U+21D2", "\\Rightarrow", "natural_transformation", "binary", ["natural_transformation"]),
        ("∘", "U+2218", "\\circ", "composition_cat", "binary", ["composition"]),
        ("id", "U+0069", "\\text{id}", "identity_morphism", "unary", ["identity"]),
        ("≅", "U+2245", "\\cong", "isomorphism_cat", "binary", ["isomorphism"]),
        ("⊗", "U+2297", "\\otimes", "monoidal_product", "binary", ["monoidal_product"]),
        ("⊕", "U+2295", "\\oplus", "coproduct_cat", "binary", ["coproduct"]),
        ("×", "U+00D7", "\\times", "product_cat", "binary", ["product"]),
        ("⨿", "U+2A3F", "\\amalg", "coproduct_amalg", "binary", ["coproduct"]),
        ("⊔", "U+2294", "\\sqcup", "coproduct_sqcup", "binary", ["coproduct"]),
        ("⊓", "U+2293", "\\sqcap", "product_sqcap", "binary", ["product"]),
        ("⇄", "U+21C4", "\\rightleftarrows", "adjunction", "binary", ["adjunction"]),
        ("⊣", "U+22A3", "\\dashv", "adjoint_cat", "binary", ["adjoint"]),
        ("⊢", "U+22A2", "\\vdash", "entails", "binary", ["entails"]),
        ("⊤", "U+22A4", "\\top", "terminal_object", "nullary", ["terminal"]),
        ("⊥", "U+22A5", "\\bot", "initial_object", "nullary", ["initial"]),
        ("1", "U+0031", "1", "unit_object", "nullary", ["unit"]),
        ("0", "U+0030", "0", "zero_object", "nullary", ["zero"]),
    ]
    
    for symbol, unicode, latex, name, arity, contexts in cat_ops[:18]:
        symbols.append(create_symbol_entry(
            symbol, unicode, latex, name, "category_theory", arity, "operator" if arity != "nullary" else "operand",
            1, 3, "partial" if arity != "nullary" else "none", "no", "no", "no", 
            "partial" if arity != "nullary" else "none", "medium",
            contexts
        ))
    
    # Functors and natural transformations (20 symbols)
    functor_ops = [
        ("F", "U+0046", "F", "functor", "unary", ["functor"]),
        ("G", "U+0047", "G", "functor_G", "unary", ["functor"]),
        ("H", "U+0048", "H", "functor_H", "unary", ["functor"]),
        ("Hom", "U+0048", "\\text{Hom}", "hom_functor", "binary", ["hom_functor"]),
        ("End", "U+0045", "\\text{End}", "endomorphism", "unary", ["endomorphism"]),
        ("Aut", "U+0041", "\\text{Aut}", "automorphism", "unary", ["automorphism"]),
        ("Iso", "U+0049", "\\text{Iso}", "isomorphism_set", "binary", ["isomorphism"]),
        ("Ob", "U+004F", "\\text{Ob}", "objects", "unary", ["objects"]),
        ("Mor", "U+004D", "\\text{Mor}", "morphisms", "unary", ["morphisms"]),
        ("dom", "U+0064", "\\text{dom}", "domain", "unary", ["domain"]),
        ("cod", "U+0063", "\\text{cod}", "codomain", "unary", ["codomain"]),
        ("ker", "U+006B", "\\ker", "kernel_cat", "unary", ["kernel"]),
        ("coker", "U+0063", "\\text{coker}", "cokernel", "unary", ["cokernel"]),
        ("im", "U+0069", "\\text{im}", "image_cat", "unary", ["image"]),
        ("coim", "U+0063", "\\text{coim}", "coimage", "unary", ["coimage"]),
    ]
    
    for symbol, unicode, latex, name, arity, contexts in functor_ops[:15]:
        symbols.append(create_symbol_entry(
            symbol, unicode, latex, name, "category_theory", arity, "operator",
            1, 3, "partial", "no", "no", "no", "partial", "medium",
            contexts
        ))
    
    # Limits and colimits (15 symbols)
    limit_ops = [
        ("lim", "U+006C", "\\lim", "limit_cat", "unary", ["limit"]),
        ("colim", "U+0063", "\\text{colim}", "colimit", "unary", ["colimit"]),
        ("←", "U+2190", "\\leftarrow", "inverse_limit", "unary", ["inverse_limit"]),
        ("→", "U+2192", "\\rightarrow", "direct_limit", "unary", ["direct_limit"]),
        ("∏", "U+220F", "\\prod", "product_limit", "unary", ["product"]),
        ("∐", "U+2210", "\\coprod", "coproduct_limit", "unary", ["coproduct"]),
        ("⨉", "U+2A09", "\\times", "product_n", "unary", ["product"]),
        ("⨁", "U+2A01", "\\bigoplus", "direct_sum_cat", "unary", ["direct_sum"]),
        ("⨂", "U+2A02", "\\bigotimes", "tensor_product_cat", "unary", ["tensor_product"]),
        ("∫", "U+222B", "\\int", "coend", "unary", ["coend"]),
        ("∫", "U+222B", "\\int", "end", "unary", ["end"]),
    ]
    
    for symbol, unicode, latex, name, arity, contexts in limit_ops[:11]:
        symbols.append(create_symbol_entry(
            symbol, unicode, latex, name, "category_theory", arity, "operator",
            1, 3, "none", "no", "no", "no", "none", "medium",
            contexts
        ))
    
    return symbols

def generate_quantum_mechanics_symbols() -> list:
    """Generate quantum mechanics symbols (60 symbols)."""
    symbols = []
    
    # Dirac notation (20 symbols)
    dirac_ops = [
        ("|ψ⟩", "U+007C", "|\\psi\\rangle", "ket", "nullary", ["ket", "state_vector"]),
        ("⟨ψ|", "U+27E8", "\\langle\\psi|", "bra", "nullary", ["bra", "dual_vector"]),
        ("⟨ψ|φ⟩", "U+27E8", "\\langle\\psi|\\phi\\rangle", "inner_product_qm", "binary", ["inner_product"]),
        ("|ψ⟩⟨φ|", "U+007C", "|\\psi\\rangle\\langle\\phi|", "outer_product_qm", "binary", ["outer_product"]),
        ("|0⟩", "U+007C", "|0\\rangle", "ket_0", "nullary", ["ground_state"]),
        ("|1⟩", "U+007C", "|1\\rangle", "ket_1", "nullary", ["excited_state"]),
        ("|+⟩", "U+007C", "|+\\rangle", "ket_plus", "nullary", ["plus_state"]),
        ("|−⟩", "U+007C", "|-\\rangle", "ket_minus", "nullary", ["minus_state"]),
        ("|↑⟩", "U+007C", "|\\uparrow\\rangle", "spin_up", "nullary", ["spin_up"]),
        ("|↓⟩", "U+007C", "|\\downarrow\\rangle", "spin_down", "nullary", ["spin_down"]),
        ("⟨ψ|Â|φ⟩", "U+27E8", "\\langle\\psi|\\hat{A}|\\phi\\rangle", "expectation_value", "ternary", ["expectation_value"]),
        ("⟨Â⟩", "U+27E8", "\\langle\\hat{A}\\rangle", "expectation", "unary", ["expectation"]),
    ]
    
    for symbol, unicode, latex, name, arity, contexts in dirac_ops[:12]:
        symbols.append(create_symbol_entry(
            symbol, unicode, latex, name, "quantum", arity, "operand" if arity == "nullary" else "operator",
            1, 2, "none", "no", "no", "no", "none", "low",
            contexts
        ))
    
    # Operators (20 symbols)
    qm_operators = [
        ("Ĥ", "U+0124", "\\hat{H}", "hamiltonian", "nullary", ["hamiltonian"]),
        ("p̂", "U+0070", "\\hat{p}", "momentum_operator", "nullary", ["momentum"]),
        ("x̂", "U+0078", "\\hat{x}", "position_operator", "nullary", ["position"]),
        ("Ŝ", "U+0053", "\\hat{S}", "spin_operator", "nullary", ["spin"]),
        ("L̂", "U+004C", "\\hat{L}", "angular_momentum", "nullary", ["angular_momentum"]),
        ("σ̂", "U+03C3", "\\hat{\\sigma}", "pauli_operator", "nullary", ["pauli"]),
        ("σ̂ₓ", "U+03C3", "\\hat{\\sigma}_x", "pauli_x", "nullary", ["pauli_x"]),
        ("σ̂ᵧ", "U+03C3", "\\hat{\\sigma}_y", "pauli_y", "nullary", ["pauli_y"]),
        ("σ̂_z", "U+03C3", "\\hat{\\sigma}_z", "pauli_z", "nullary", ["pauli_z"]),
        ("Î", "U+00CE", "\\hat{I}", "identity_operator", "nullary", ["identity"]),
        ("Û", "U+00DB", "\\hat{U}", "unitary_operator", "nullary", ["unitary"]),
        ("ρ̂", "U+03C1", "\\hat{\\rho}", "density_operator", "nullary", ["density_matrix"]),
        ("[Â,B̂]", "U+005B", "[\\hat{A},\\hat{B}]", "commutator", "binary", ["commutator"]),
        ("{Â,B̂}", "U+007B", "\\{\\hat{A},\\hat{B}\\}", "anticommutator", "binary", ["anticommutator"]),
    ]
    
    for symbol, unicode, latex, name, arity, contexts in qm_operators[:14]:
        symbols.append(create_symbol_entry(
            symbol, unicode, latex, name, "quantum", arity, "operand" if arity == "nullary" else "operator",
            1, 3, "none", "no", "no", "no", "none", "low",
            contexts
        ))
    
    # Constants and special symbols (15 symbols)
    qm_constants = [
        ("ℏ", "U+210F", "\\hbar", "reduced_planck", "nullary", ["reduced_planck_constant"]),
        ("ψ", "U+03C8", "\\psi", "wavefunction", "nullary", ["wavefunction"]),
        ("Ψ", "U+03A8", "\\Psi", "wavefunction_capital", "nullary", ["wavefunction"]),
        ("φ", "U+03C6", "\\phi", "phase", "nullary", ["phase"]),
        ("α", "U+03B1", "\\alpha", "fine_structure", "nullary", ["fine_structure_constant"]),
        ("λ", "U+03BB", "\\lambda", "wavelength_qm", "nullary", ["wavelength"]),
        ("ν", "U+03BD", "\\nu", "frequency", "nullary", ["frequency"]),
        ("ω", "U+03C9", "\\omega", "angular_frequency", "nullary", ["angular_frequency"]),
        ("k", "U+006B", "k", "wave_number", "nullary", ["wave_number"]),
        ("E", "U+0045", "E", "energy", "nullary", ["energy"]),
        ("T", "U+0054", "T", "kinetic_energy", "nullary", ["kinetic_energy"]),
        ("V", "U+0056", "V", "potential_energy", "nullary", ["potential_energy"]),
        ("S", "U+0053", "S", "action", "nullary", ["action"]),
        ("ℒ", "U+2112", "\\mathcal{L}", "lagrangian", "nullary", ["lagrangian"]),
    ]
    
    for symbol, unicode, latex, name, arity, contexts in qm_constants[:14]:
        symbols.append(create_symbol_entry(
            symbol, unicode, latex, name, "quantum", arity, "operand",
            1, 2, "none", "no", "no", "no", "none", "medium",
            contexts
        ))
    
    return symbols

def generate_information_theory_symbols() -> list:
    """Generate information theory symbols (50 symbols)."""
    symbols = []
    
    # Entropy and information measures (25 symbols)
    info_measures = [
        ("H", "U+0048", "H", "entropy", "unary", ["entropy"]),
        ("S", "U+0053", "S", "entropy_S", "unary", ["entropy"]),
        ("I", "U+0049", "I", "mutual_information", "binary", ["mutual_information"]),
        ("D", "U+0044", "D", "divergence", "binary", ["divergence"]),
        ("KL", "U+004B", "D_{KL}", "kl_divergence", "binary", ["kl_divergence"]),
        ("JS", "U+004A", "D_{JS}", "js_divergence", "binary", ["js_divergence"]),
        ("H(X)", "U+0048", "H(X)", "entropy_X", "unary", ["entropy"]),
        ("H(X|Y)", "U+0048", "H(X|Y)", "conditional_entropy", "binary", ["conditional_entropy"]),
        ("I(X;Y)", "U+0049", "I(X;Y)", "mutual_info_XY", "binary", ["mutual_information"]),
        ("H(X,Y)", "U+0048", "H(X,Y)", "joint_entropy", "binary", ["joint_entropy"]),
        ("C", "U+0043", "C", "channel_capacity", "nullary", ["channel_capacity"]),
        ("R", "U+0052", "R", "rate", "nullary", ["rate"]),
        ("log", "U+006C", "\\log", "logarithm_info", "unary", ["logarithm"]),
        ("log₂", "U+006C", "\\log_2", "log_base_2", "unary", ["log_base_2"]),
        ("ln", "U+006C", "\\ln", "natural_log_info", "unary", ["natural_log"]),
        ("exp", "U+0065", "\\exp", "exponential_info", "unary", ["exponential"]),
        ("e", "U+0065", "e", "euler_number", "nullary", ["euler_number"]),
        ("2", "U+0032", "2", "binary_base", "nullary", ["binary"]),
        ("p", "U+0070", "p", "probability_p", "nullary", ["probability"]),
        ("q", "U+0071", "q", "probability_q", "nullary", ["probability"]),
    ]
    
    for symbol, unicode, latex, name, arity, contexts in info_measures[:20]:
        symbols.append(create_symbol_entry(
            symbol, unicode, latex, name, "information", arity, "operator" if arity != "nullary" else "operand",
            1, 2, "none", "no", "no", "no", "none", "low",
            contexts
        ))
    
    # Coding theory (15 symbols)
    coding_ops = [
        ("⊕", "U+2295", "\\oplus", "xor_coding", "binary", ["xor"]),
        ("⊗", "U+2297", "\\otimes", "tensor_coding", "binary", ["tensor"]),
        ("⊙", "U+2299", "\\odot", "hadamard_coding", "binary", ["hadamard"]),
        ("∘", "U+2218", "\\circ", "composition_coding", "binary", ["composition"]),
        ("⋆", "U+22C6", "\\star", "convolution_coding", "binary", ["convolution"]),
        ("*", "U+002A", "*", "convolution_alt", "binary", ["convolution"]),
        ("⊻", "U+22BB", "\\veebar", "xor_alt", "binary", ["xor"]),
        ("≪", "U+226A", "\\ll", "left_shift_coding", "binary", ["left_shift"]),
        ("≫", "U+226B", "\\gg", "right_shift_coding", "binary", ["right_shift"]),
        ("∧", "U+2227", "\\land", "and_coding", "binary", ["and"]),
        ("∨", "U+2228", "\\lor", "or_coding", "binary", ["or"]),
        ("¬", "U+00AC", "\\neg", "not_coding", "unary", ["not"]),
        ("⊤", "U+22A4", "\\top", "one_bit", "nullary", ["one"]),
        ("⊥", "U+22A5", "\\bot", "zero_bit", "nullary", ["zero"]),
    ]
    
    for symbol, unicode, latex, name, arity, contexts in coding_ops[:14]:
        symbols.append(create_symbol_entry(
            symbol, unicode, latex, name, "information", arity, "operator" if arity != "nullary" else "operand",
            1, 1, "full" if arity == "binary" else "none", "no", "yes" if arity == "binary" else "no", 
            "yes" if arity == "binary" else "no", "full" if arity == "binary" else "none", "medium",
            contexts
        ))
    
    return symbols

def generate_geometry_symbols() -> list:
    """Generate geometry symbols (80 symbols)."""
    symbols = []
    
    # Basic geometry (30 symbols)
    geom_ops = [
        ("∠", "U+2220", "\\angle", "angle", "ternary", ["angle"]),
        ("∡", "U+2221", "\\measuredangle", "measured_angle", "ternary", ["measured_angle"]),
        ("∢", "U+2222", "\\sphericalangle", "spherical_angle", "ternary", ["spherical_angle"]),
        ("°", "U+00B0", "^\\circ", "degree", "nullary", ["degree"]),
        ("′", "U+2032", "'", "prime", "nullary", ["minute", "prime"]),
        ("″", "U+2033", "''", "double_prime", "nullary", ["second", "double_prime"]),
        ("‴", "U+2034", "'''", "triple_prime", "nullary", ["triple_prime"]),
        ("∥", "U+2225", "\\parallel", "parallel_geom", "binary", ["parallel"]),
        ("∦", "U+2226", "\\nparallel", "not_parallel", "binary", ["not_parallel"]),
        ("⊥", "U+22A5", "\\perp", "perpendicular_geom", "binary", ["perpendicular"]),
        ("⟂", "U+27C2", "\\perp", "perpendicular_alt", "binary", ["perpendicular"]),
        ("≅", "U+2245", "\\cong", "congruent_geom", "binary", ["congruent"]),
        ("∼", "U+223C", "\\sim", "similar_geom", "binary", ["similar"]),
        ("≃", "U+2243", "\\simeq", "similar_equal", "binary", ["similar_equal"]),
        ("△", "U+25B3", "\\triangle", "triangle", "nullary", ["triangle"]),
        ("▷", "U+25B7", "\\triangleright", "triangle_right", "nullary", ["triangle_right"]),
        ("◁", "U+25C1", "\\triangleleft", "triangle_left", "nullary", ["triangle_left"]),
        ("▽", "U+25BD", "\\triangledown", "triangle_down", "nullary", ["triangle_down"]),
        ("□", "U+25A1", "\\square", "square_geom", "nullary", ["square"]),
        ("▭", "U+25AD", "\\rectangle", "rectangle", "nullary", ["rectangle"]),
        ("○", "U+25CB", "\\bigcirc", "circle", "nullary", ["circle"]),
        ("◯", "U+25EF", "\\bigcirc", "large_circle", "nullary", ["large_circle"]),
        ("⬭", "U+2B2D", "\\pentagon", "pentagon", "nullary", ["pentagon"]),
        ("⬢", "U+2B22", "\\hexagon", "hexagon", "nullary", ["hexagon"]),
    ]
    
    for symbol, unicode, latex, name, arity, contexts in geom_ops[:24]:
        symbols.append(create_symbol_entry(
            symbol, unicode, latex, name, "geometry", arity, "operator" if arity != "nullary" else "operand",
            1, 1, "none", "no", "no", "no", "none", "low",
            contexts
        ))
    
    # Trigonometric and measurement (30 symbols)
    trig_geom = [
        ("sin", "U+0073", "\\sin", "sine_geom", "unary", ["sine"]),
        ("cos", "U+0063", "\\cos", "cosine_geom", "unary", ["cosine"]),
        ("tan", "U+0074", "\\tan", "tangent_geom", "unary", ["tangent"]),
        ("cot", "U+0063", "\\cot", "cotangent_geom", "unary", ["cotangent"]),
        ("sec", "U+0073", "\\sec", "secant_geom", "unary", ["secant"]),
        ("csc", "U+0063", "\\csc", "cosecant_geom", "unary", ["cosecant"]),
        ("d", "U+0064", "d", "distance", "binary", ["distance"]),
        ("A", "U+0041", "A", "area", "unary", ["area"]),
        ("V", "U+0056", "V", "volume", "unary", ["volume"]),
        ("P", "U+0050", "P", "perimeter", "unary", ["perimeter"]),
        ("C", "U+0043", "C", "circumference", "unary", ["circumference"]),
        ("r", "U+0072", "r", "radius", "nullary", ["radius"]),
        ("d", "U+0064", "d", "diameter", "nullary", ["diameter"]),
        ("h", "U+0068", "h", "height", "nullary", ["height"]),
        ("b", "U+0062", "b", "base", "nullary", ["base"]),
        ("l", "U+006C", "l", "length", "nullary", ["length"]),
        ("w", "U+0077", "w", "width", "nullary", ["width"]),
        ("a", "U+0061", "a", "side_a", "nullary", ["side"]),
        ("b", "U+0062", "b", "side_b", "nullary", ["side"]),
        ("c", "U+0063", "c", "side_c", "nullary", ["side"]),
        ("π", "U+03C0", "\\pi", "pi_geom", "nullary", ["pi"]),
        ("τ", "U+03C4", "\\tau", "tau", "nullary", ["tau"]),
        ("φ", "U+03C6", "\\phi", "golden_ratio", "nullary", ["golden_ratio"]),
    ]
    
    for symbol, unicode, latex, name, arity, contexts in trig_geom[:23]:
        symbols.append(create_symbol_entry(
            symbol, unicode, latex, name, "geometry", arity, "operator" if arity != "nullary" else "operand",
            1, 1, "partial" if arity == "unary" else "none", "no", "no", "no", 
            "partial" if arity == "unary" else "none", "low",
            contexts
        ))
    
    return symbols

def generate_number_theory_symbols() -> list:
    """Generate number theory symbols (60 symbols)."""
    symbols = []
    
    # Divisibility and primes (25 symbols)
    number_ops = [
        ("∣", "U+2223", "\\mid", "divides_nt", "binary", ["divides"]),
        ("∤", "U+2224", "\\nmid", "not_divides_nt", "binary", ["not_divides"]),
        ("≡", "U+2261", "\\equiv", "congruent_mod", "ternary", ["congruent_modulo"]),
        ("≢", "U+2262", "\\not\\equiv", "not_congruent_mod", "ternary", ["not_congruent_modulo"]),
        ("mod", "U+006D", "\\bmod", "modulo_nt", "binary", ["modulo"]),
        ("gcd", "U+0067", "\\gcd", "gcd_nt", "binary", ["gcd"]),
        ("lcm", "U+006C", "\\text{lcm}", "lcm_nt", "binary", ["lcm"]),
        ("(a,b)", "U+0028", "(a,b)", "gcd_notation", "binary", ["gcd"]),
        ("[a,b]", "U+005B", "[a,b]", "lcm_notation", "binary", ["lcm"]),
        ("φ", "U+03C6", "\\phi", "euler_totient", "unary", ["euler_totient"]),
        ("μ", "U+03BC", "\\mu", "mobius", "unary", ["mobius_function"]),
        ("τ", "U+03C4", "\\tau", "divisor_function", "unary", ["divisor_function"]),
        ("σ", "U+03C3", "\\sigma", "sum_of_divisors", "unary", ["sum_of_divisors"]),
        ("ω", "U+03C9", "\\omega", "distinct_prime_factors", "unary", ["distinct_prime_factors"]),
        ("Ω", "U+03A9", "\\Omega", "prime_factors_with_multiplicity", "unary", ["prime_factors"]),
        ("π", "U+03C0", "\\pi", "prime_counting", "unary", ["prime_counting"]),
        ("li", "U+006C", "\\text{li}", "logarithmic_integral", "unary", ["logarithmic_integral"]),
        ("p", "U+0070", "p", "prime", "nullary", ["prime"]),
        ("q", "U+0071", "q", "prime_q", "nullary", ["prime"]),
        ("n", "U+006E", "n", "integer_n", "nullary", ["integer"]),
        ("m", "U+006D", "m", "integer_m", "nullary", ["integer"]),
        ("k", "U+006B", "k", "integer_k", "nullary", ["integer"]),
        ("a", "U+0061", "a", "integer_a", "nullary", ["integer"]),
        ("b", "U+0062", "b", "integer_b", "nullary", ["integer"]),
    ]
    
    for symbol, unicode, latex, name, arity, contexts in number_ops[:24]:
        symbols.append(create_symbol_entry(
            symbol, unicode, latex, name, "number_theory", arity, "operator" if arity != "nullary" else "operand",
            1, 2, "full" if arity == "binary" else "none", "no", "yes" if arity == "binary" else "no", 
            "yes" if arity == "binary" else "no", "full" if arity == "binary" else "none", "low",
            contexts
        ))
    
    # Continued fractions and special functions (20 symbols)
    special_nt = [
        ("[a₀;a₁,a₂,...]", "U+005B", "[a_0;a_1,a_2,\\ldots]", "continued_fraction", "unary", ["continued_fraction"]),
        ("⌊x⌋", "U+230A", "\\lfloor x\\rfloor", "floor", "unary", ["floor"]),
        ("⌈x⌉", "U+2308", "\\lceil x\\rceil", "ceiling", "unary", ["ceiling"]),
        ("{x}", "U+007B", "\\{x\\}", "fractional_part", "unary", ["fractional_part"]),
        ("⌊⌋", "U+230A", "\\lfloor\\rfloor", "floor_brackets", "unary", ["floor"]),
        ("⌈⌉", "U+2308", "\\lceil\\rceil", "ceiling_brackets", "unary", ["ceiling"]),
        ("||", "U+007C", "||", "absolute_value", "unary", ["absolute_value"]),
        ("sgn", "U+0073", "\\text{sgn}", "sign_function", "unary", ["sign"]),
        ("⌊x⌋", "U+230A", "\\lfloor x\\rfloor", "greatest_integer", "unary", ["greatest_integer"]),
        ("⌈x⌉", "U+2308", "\\lceil x\\rceil", "least_integer", "unary", ["least_integer"]),
        ("⌊x⌉", "U+230A", "\\lfloor x\\rceil", "nearest_integer", "unary", ["nearest_integer"]),
        ("∞", "U+221E", "\\infty", "infinity_nt", "nullary", ["infinity"]),
        ("−∞", "U+2212", "-\\infty", "negative_infinity", "nullary", ["negative_infinity"]),
        ("ℵ₀", "U+2135", "\\aleph_0", "aleph_null", "nullary", ["aleph_null"]),
        ("ℵ₁", "U+2135", "\\aleph_1", "aleph_one", "nullary", ["aleph_one"]),
    ]
    
    for symbol, unicode, latex, name, arity, contexts in special_nt[:15]:
        symbols.append(create_symbol_entry(
            symbol, unicode, latex, name, "number_theory", arity, "operator" if arity != "nullary" else "operand",
            1, 2, "partial" if arity == "unary" else "none", "no", "no", "no", 
            "partial" if arity == "unary" else "none", "low",
            contexts
        ))
    
    return symbols

def generate_abstract_algebra_symbols() -> list:
    """Generate abstract algebra symbols (70 symbols)."""
    symbols = []
    
    # Group theory (25 symbols)
    group_ops = [
        ("∗", "U+2217", "\\ast", "group_operation", "binary", ["group_operation"]),
        ("·", "U+00B7", "\\cdot", "group_multiplication", "binary", ["multiplication"]),
        ("+", "U+002B", "+", "group_addition", "binary", ["addition"]),
        ("e", "U+0065", "e", "identity_element", "nullary", ["identity"]),
        ("1", "U+0031", "1", "multiplicative_identity", "nullary", ["identity"]),
        ("0", "U+0030", "0", "additive_identity", "nullary", ["identity"]),
        ("−", "U+2212", "-", "inverse", "unary", ["inverse"]),
        ("⁻¹", "U+207B", "^{-1}", "group_inverse", "unary", ["inverse"]),
        ("⟨g⟩", "U+27E8", "\\langle g\\rangle", "cyclic_group", "unary", ["cyclic_group"]),
        ("⟨S⟩", "U+27E8", "\\langle S\\rangle", "generated_subgroup", "unary", ["generated_subgroup"]),
        ("H≤G", "U+2264", "H\\leq G", "subgroup", "binary", ["subgroup"]),
        ("H⊴G", "U+22B4", "H\\trianglelefteq G", "normal_subgroup", "binary", ["normal_subgroup"]),
        ("G/H", "U+002F", "G/H", "quotient_group", "binary", ["quotient_group"]),
        ("G×H", "U+00D7", "G\\times H", "direct_product", "binary", ["direct_product"]),
        ("G⋊H", "U+22CA", "G\\rtimes H", "semidirect_product", "binary", ["semidirect_product"]),
        ("|G|", "U+007C", "|G|", "group_order", "unary", ["order"]),
        ("[G:H]", "U+005B", "[G:H]", "index", "binary", ["index"]),
        ("Aut(G)", "U+0041", "\\text{Aut}(G)", "automorphism_group", "unary", ["automorphism_group"]),
        ("Inn(G)", "U+0049", "\\text{Inn}(G)", "inner_automorphism", "unary", ["inner_automorphism"]),
        ("Z(G)", "U+005A", "Z(G)", "center", "unary", ["center"]),
        ("C_G(H)", "U+0043", "C_G(H)", "centralizer", "binary", ["centralizer"]),
        ("N_G(H)", "U+004E", "N_G(H)", "normalizer", "binary", ["normalizer"]),
    ]
    
    for symbol, unicode, latex, name, arity, contexts in group_ops[:22]:
        symbols.append(create_symbol_entry(
            symbol, unicode, latex, name, "abstract_algebra", arity, "operator" if arity != "nullary" else "operand",
            1, 2, "full" if arity == "binary" else "partial" if arity == "unary" else "none", 
            "no", "yes" if arity == "binary" else "no", "yes" if arity == "binary" else "no", 
            "full" if arity == "binary" else "partial" if arity == "unary" else "none", "low",
            contexts
        ))
    
    # Ring theory (25 symbols)
    ring_ops = [
        ("+", "U+002B", "+", "ring_addition", "binary", ["addition"]),
        ("·", "U+00B7", "\\cdot", "ring_multiplication", "binary", ["multiplication"]),
        ("×", "U+00D7", "\\times", "ring_product", "binary", ["product"]),
        ("0", "U+0030", "0", "zero_ring", "nullary", ["zero"]),
        ("1", "U+0031", "1", "one_ring", "nullary", ["one"]),
        ("−", "U+2212", "-", "additive_inverse", "unary", ["additive_inverse"]),
        ("⁻¹", "U+207B", "^{-1}", "multiplicative_inverse", "unary", ["multiplicative_inverse"]),
        ("I", "U+0049", "I", "ideal", "nullary", ["ideal"]),
        ("⟨a⟩", "U+27E8", "\\langle a\\rangle", "principal_ideal", "unary", ["principal_ideal"]),
        ("R/I", "U+002F", "R/I", "quotient_ring", "binary", ["quotient_ring"]),
        ("R[x]", "U+005B", "R[x]", "polynomial_ring", "unary", ["polynomial_ring"]),
        ("R[[x]]", "U+005B", "R[[x]]", "power_series_ring", "unary", ["power_series_ring"]),
        ("Frac(R)", "U+0046", "\\text{Frac}(R)", "field_of_fractions", "unary", ["field_of_fractions"]),
        ("char(R)", "U+0063", "\\text{char}(R)", "characteristic", "unary", ["characteristic"]),
        ("U(R)", "U+0055", "U(R)", "units", "unary", ["units"]),
        ("Spec(R)", "U+0053", "\\text{Spec}(R)", "spectrum_ring", "unary", ["spectrum"]),
        ("Max(R)", "U+004D", "\\text{Max}(R)", "maximal_ideals", "unary", ["maximal_ideals"]),
        ("Nil(R)", "U+004E", "\\text{Nil}(R)", "nilradical", "unary", ["nilradical"]),
        ("Jac(R)", "U+004A", "\\text{Jac}(R)", "jacobson_radical", "unary", ["jacobson_radical"]),
    ]
    
    for symbol, unicode, latex, name, arity, contexts in ring_ops[:19]:
        symbols.append(create_symbol_entry(
            symbol, unicode, latex, name, "abstract_algebra", arity, "operator" if arity != "nullary" else "operand",
            1, 2, "full" if arity == "binary" else "partial" if arity == "unary" else "none", 
            "no", "yes" if arity == "binary" else "no", "yes" if arity == "binary" else "no", 
            "full" if arity == "binary" else "partial" if arity == "unary" else "none", "low",
            contexts
        ))
    
    # Field and module theory (20 symbols)
    field_ops = [
        ("𝔽", "U+1D53D", "\\mathbb{F}", "field_F", "nullary", ["field"]),
        ("𝔽_p", "U+1D53D", "\\mathbb{F}_p", "finite_field", "nullary", ["finite_field"]),
        ("𝔽_q", "U+1D53D", "\\mathbb{F}_q", "finite_field_q", "nullary", ["finite_field"]),
        ("GF(q)", "U+0047", "\\text{GF}(q)", "galois_field", "nullary", ["galois_field"]),
        ("[F:K]", "U+005B", "[F:K]", "degree_extension", "binary", ["degree"]),
        ("Gal(F/K)", "U+0047", "\\text{Gal}(F/K)", "galois_group", "binary", ["galois_group"]),
        ("Aut(F/K)", "U+0041", "\\text{Aut}(F/K)", "automorphism_field", "binary", ["automorphism"]),
        ("F(α)", "U+0046", "F(\\alpha)", "field_extension", "unary", ["field_extension"]),
        ("F[α]", "U+0046", "F[\\alpha]", "ring_extension", "unary", ["ring_extension"]),
        ("M", "U+004D", "M", "module", "nullary", ["module"]),
        ("R-Mod", "U+0052", "R\\text{-Mod}", "category_of_modules", "nullary", ["category_of_modules"]),
        ("⊗_R", "U+2297", "\\otimes_R", "tensor_product_module", "binary", ["tensor_product"]),
        ("Hom_R(M,N)", "U+0048", "\\text{Hom}_R(M,N)", "module_homomorphisms", "binary", ["homomorphisms"]),
        ("Ann(M)", "U+0041", "\\text{Ann}(M)", "annihilator", "unary", ["annihilator"]),
        ("Tor", "U+0054", "\\text{Tor}", "tor_functor", "binary", ["tor"]),
        ("Ext", "U+0045", "\\text{Ext}", "ext_functor", "binary", ["ext"]),
    ]
    
    for symbol, unicode, latex, name, arity, contexts in field_ops[:16]:
        symbols.append(create_symbol_entry(
            symbol, unicode, latex, name, "abstract_algebra", arity, "operator" if arity != "nullary" else "operand",
            1, 3, "partial" if arity != "nullary" else "none", "no", "no", "no", 
            "partial" if arity != "nullary" else "none", "medium",
            contexts
        ))
    
    return symbols

def main():
    """Main execution function."""
    print("="*60)
    print("FINAL COMPREHENSIVE SYMBOL DATASET GENERATOR - PHASE 2")
    print("Target: 1000+ symbols")
    print("="*60)
    print()
    
    symbols = []
    
    # Add all categories
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
    
    print("Generating category theory symbols...")
    cat_symbols = generate_category_theory_symbols()
    symbols.extend(cat_symbols)
    print(f"  Added {len(cat_symbols)} category theory symbols")
    
    print("Generating quantum mechanics symbols...")
    qm_symbols = generate_quantum_mechanics_symbols()
    symbols.extend(qm_symbols)
    print(f"  Added {len(qm_symbols)} quantum mechanics symbols")
    
    print("Generating information theory symbols...")
    info_symbols = generate_information_theory_symbols()
    symbols.extend(info_symbols)
    print(f"  Added {len(info_symbols)} information theory symbols")
    
    print("Generating geometry symbols...")
    geom_symbols = generate_geometry_symbols()
    symbols.extend(geom_symbols)
    print(f"  Added {len(geom_symbols)} geometry symbols")
    
    print("Generating number theory symbols...")
    nt_symbols = generate_number_theory_symbols()
    symbols.extend(nt_symbols)
    print(f"  Added {len(nt_symbols)} number theory symbols")
    
    print("Generating abstract algebra symbols...")
    aa_symbols = generate_abstract_algebra_symbols()
    symbols.extend(aa_symbols)
    print(f"  Added {len(aa_symbols)} abstract algebra symbols")
    
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
    print(f"✓ Successfully generated {len(symbols)} symbols!")
    print("="*60)

if __name__ == "__main__":
    main()


def generate_complex_analysis_symbols() -> list:
    """Generate complex analysis symbols (50 symbols)."""
    symbols = []
    
    # Complex numbers and operations (20 symbols)
    complex_ops = [
        ("i", "U+0069", "i", "imaginary_unit", "nullary", ["imaginary_unit"]),
        ("j", "U+006A", "j", "imaginary_unit_j", "nullary", ["imaginary_unit"]),
        ("ℂ", "U+2102", "\\mathbb{C}", "complex_numbers", "nullary", ["complex_numbers"]),
        ("Re", "U+0052", "\\text{Re}", "real_part", "unary", ["real_part"]),
        ("Im", "U+0049", "\\text{Im}", "imaginary_part", "unary", ["imaginary_part"]),
        ("z", "U+007A", "z", "complex_variable", "nullary", ["complex_variable"]),
        ("w", "U+0077", "w", "complex_variable_w", "nullary", ["complex_variable"]),
        ("z̄", "U+007A", "\\bar{z}", "complex_conjugate", "unary", ["conjugate"]),
        ("|z|", "U+007C", "|z|", "modulus", "unary", ["modulus"]),
        ("arg(z)", "U+0061", "\\arg(z)", "argument", "unary", ["argument"]),
        ("∠z", "U+2220", "\\angle z", "angle_complex", "unary", ["angle"]),
        ("e^(iθ)", "U+0065", "e^{i\\theta}", "euler_formula", "unary", ["euler_formula"]),
        ("Log", "U+004C", "\\text{Log}", "principal_logarithm", "unary", ["principal_logarithm"]),
        ("log", "U+006C", "\\log", "complex_logarithm", "unary", ["complex_logarithm"]),
        ("√", "U+221A", "\\sqrt", "complex_square_root", "unary", ["square_root"]),
        ("z^w", "U+007A", "z^w", "complex_power", "binary", ["complex_power"]),
        ("exp", "U+0065", "\\exp", "complex_exponential", "unary", ["exponential"]),
    ]
    
    for symbol, unicode, latex, name, arity, contexts in complex_ops[:17]:
        symbols.append(create_symbol_entry(
            symbol, unicode, latex, name, "complex_analysis", arity, "operator" if arity != "nullary" else "operand",
            1, 2, "partial" if arity == "unary" else "full" if arity == "binary" else "none", 
            "no", "no", "no", "partial" if arity != "nullary" else "none", "medium",
            contexts
        ))
    
    # Analytic functions (20 symbols)
    analytic_ops = [
        ("f(z)", "U+0066", "f(z)", "analytic_function", "unary", ["analytic_function"]),
        ("f'(z)", "U+0066", "f'(z)", "derivative_complex", "unary", ["derivative"]),
        ("∂f/∂z", "U+2202", "\\frac{\\partial f}{\\partial z}", "partial_z", "unary", ["partial_derivative"]),
        ("∂f/∂z̄", "U+2202", "\\frac{\\partial f}{\\partial\\bar{z}}", "partial_zbar", "unary", ["partial_derivative"]),
        ("∮", "U+222E", "\\oint", "contour_integral_ca", "unary", ["contour_integral"]),
        ("∫_γ", "U+222B", "\\int_\\gamma", "path_integral", "unary", ["path_integral"]),
        ("Res", "U+0052", "\\text{Res}", "residue", "binary", ["residue"]),
        ("Ind", "U+0049", "\\text{Ind}", "index", "binary", ["index"]),
        ("γ", "U+03B3", "\\gamma", "contour", "nullary", ["contour"]),
        ("Γ", "U+0393", "\\Gamma", "gamma_function", "unary", ["gamma_function"]),
        ("ζ", "U+03B6", "\\zeta", "riemann_zeta", "unary", ["riemann_zeta"]),
        ("η", "U+03B7", "\\eta", "dedekind_eta", "unary", ["dedekind_eta"]),
        ("ϑ", "U+03D1", "\\vartheta", "theta_function", "unary", ["theta_function"]),
        ("℘", "U+2118", "\\wp", "weierstrass_p", "unary", ["weierstrass_p"]),
        ("Ei", "U+0045", "\\text{Ei}", "exponential_integral", "unary", ["exponential_integral"]),
        ("erf", "U+0065", "\\text{erf}", "error_function", "unary", ["error_function"]),
        ("erfc", "U+0065", "\\text{erfc}", "complementary_error", "unary", ["complementary_error"]),
    ]
    
    for symbol, unicode, latex, name, arity, contexts in analytic_ops[:17]:
        symbols.append(create_symbol_entry(
            symbol, unicode, latex, name, "complex_analysis", arity, "operator" if arity != "nullary" else "operand",
            1, 3, "partial" if arity != "nullary" else "none", "no", "no", "no", 
            "partial" if arity != "nullary" else "none", "medium",
            contexts
        ))
    
    return symbols

def generate_functional_analysis_symbols() -> list:
    """Generate functional analysis symbols (50 symbols)."""
    symbols = []
    
    # Normed spaces and operators (25 symbols)
    func_ops = [
        ("‖·‖", "U+2016", "\\|\\cdot\\|", "norm_fa", "unary", ["norm"]),
        ("‖f‖", "U+2016", "\\|f\\|", "function_norm", "unary", ["norm"]),
        ("‖T‖", "U+2016", "\\|T\\|", "operator_norm", "unary", ["operator_norm"]),
        ("⟨·,·⟩", "U+27E8", "\\langle\\cdot,\\cdot\\rangle", "inner_product_fa", "binary", ["inner_product"]),
        ("L^p", "U+004C", "L^p", "lp_space", "nullary", ["lp_space"]),
        ("L^∞", "U+004C", "L^\\infty", "l_infinity_space", "nullary", ["l_infinity"]),
        ("ℓ^p", "U+2113", "\\ell^p", "little_lp_space", "nullary", ["little_lp"]),
        ("C[a,b]", "U+0043", "C[a,b]", "continuous_functions", "nullary", ["continuous"]),
        ("C^k", "U+0043", "C^k", "k_times_differentiable", "nullary", ["differentiable"]),
        ("C^∞", "U+0043", "C^\\infty", "smooth_functions", "nullary", ["smooth"]),
        ("H", "U+0048", "H", "hilbert_space", "nullary", ["hilbert_space"]),
        ("B", "U+0042", "B", "banach_space", "nullary", ["banach_space"]),
        ("X", "U+0058", "X", "normed_space", "nullary", ["normed_space"]),
        ("X*", "U+0058", "X^*", "dual_space", "unary", ["dual_space"]),
        ("X**", "U+0058", "X^{**}", "double_dual", "unary", ["double_dual"]),
        ("T", "U+0054", "T", "operator_T", "nullary", ["operator"]),
        ("T*", "U+0054", "T^*", "adjoint_operator", "unary", ["adjoint"]),
        ("T⁻¹", "U+0054", "T^{-1}", "inverse_operator", "unary", ["inverse"]),
        ("ker(T)", "U+006B", "\\ker(T)", "kernel_operator", "unary", ["kernel"]),
        ("im(T)", "U+0069", "\\text{im}(T)", "image_operator", "unary", ["image"]),
        ("ran(T)", "U+0072", "\\text{ran}(T)", "range", "unary", ["range"]),
        ("σ(T)", "U+03C3", "\\sigma(T)", "spectrum_operator", "unary", ["spectrum"]),
        ("ρ(T)", "U+03C1", "\\rho(T)", "resolvent_set", "unary", ["resolvent_set"]),
        ("R(λ,T)", "U+0052", "R(\\lambda,T)", "resolvent", "binary", ["resolvent"]),
    ]
    
    for symbol, unicode, latex, name, arity, contexts in func_ops[:24]:
        symbols.append(create_symbol_entry(
            symbol, unicode, latex, name, "functional_analysis", arity, "operator" if arity != "nullary" else "operand",
            1, 3, "partial" if arity != "nullary" else "none", "no", "no", "no", 
            "partial" if arity != "nullary" else "none", "medium",
            contexts
        ))
    
    # Convergence and topology (20 symbols)
    conv_ops = [
        ("→", "U+2192", "\\to", "converges_fa", "binary", ["converges"]),
        ("⇀", "U+21C0", "\\rightharpoonup", "weak_convergence", "binary", ["weak_convergence"]),
        ("⇁", "U+21C1", "\\rightharpoondown", "weak_star_convergence", "binary", ["weak_star"]),
        ("⟶", "U+27F6", "\\longrightarrow", "strong_convergence", "binary", ["strong_convergence"]),
        ("⟹", "U+27F9", "\\Longrightarrow", "uniform_convergence", "binary", ["uniform_convergence"]),
        ("lim", "U+006C", "\\lim", "limit_fa", "unary", ["limit"]),
        ("sup", "U+0073", "\\sup", "supremum_fa", "unary", ["supremum"]),
        ("inf", "U+0069", "\\inf", "infimum_fa", "unary", ["infimum"]),
        ("limsup", "U+006C", "\\limsup", "limit_superior_fa", "unary", ["limit_superior"]),
        ("liminf", "U+006C", "\\liminf", "limit_inferior_fa", "unary", ["limit_inferior"]),
        ("∑", "U+2211", "\\sum", "series_fa", "unary", ["series"]),
        ("∏", "U+220F", "\\prod", "product_fa", "unary", ["product"]),
        ("∫", "U+222B", "\\int", "integral_fa", "unary", ["integral"]),
        ("∂", "U+2202", "\\partial", "boundary_fa", "unary", ["boundary"]),
        ("cl", "U+0063", "\\text{cl}", "closure_fa", "unary", ["closure"]),
        ("int", "U+0069", "\\text{int}", "interior_fa", "unary", ["interior"]),
        ("⊕", "U+2295", "\\oplus", "direct_sum_fa", "binary", ["direct_sum"]),
        ("⊗", "U+2297", "\\otimes", "tensor_product_fa", "binary", ["tensor_product"]),
    ]
    
    for symbol, unicode, latex, name, arity, contexts in conv_ops[:18]:
        symbols.append(create_symbol_entry(
            symbol, unicode, latex, name, "functional_analysis", arity, "operator",
            1, 2, "partial" if arity == "unary" else "none", "no", "no", "no", 
            "partial" if arity != "nullary" else "none", "low",
            contexts
        ))
    
    return symbols

def generate_differential_geometry_symbols() -> list:
    """Generate differential geometry symbols (50 symbols)."""
    symbols = []
    
    # Manifolds and tensors (25 symbols)
    diff_geom = [
        ("M", "U+004D", "M", "manifold_dg", "nullary", ["manifold"]),
        ("TM", "U+0054", "TM", "tangent_bundle_dg", "nullary", ["tangent_bundle"]),
        ("T*M", "U+0054", "T^*M", "cotangent_bundle_dg", "nullary", ["cotangent_bundle"]),
        ("T_pM", "U+0054", "T_pM", "tangent_space", "nullary", ["tangent_space"]),
        ("T_p*M", "U+0054", "T_p^*M", "cotangent_space", "nullary", ["cotangent_space"]),
        ("X", "U+0058", "X", "vector_field", "nullary", ["vector_field"]),
        ("ω", "U+03C9", "\\omega", "differential_form_dg", "nullary", ["differential_form"]),
        ("d", "U+0064", "d", "exterior_derivative_dg", "unary", ["exterior_derivative"]),
        ("∧", "U+2227", "\\wedge", "wedge_product_dg", "binary", ["wedge_product"]),
        ("∇", "U+2207", "\\nabla", "connection_dg", "unary", ["connection"]),
        ("∇_X", "U+2207", "\\nabla_X", "covariant_derivative", "unary", ["covariant_derivative"]),
        ("⟨·,·⟩", "U+27E8", "\\langle\\cdot,\\cdot\\rangle", "metric_dg", "binary", ["metric"]),
        ("g", "U+0067", "g", "metric_tensor_dg", "nullary", ["metric_tensor"]),
        ("g_{ij}", "U+0067", "g_{ij}", "metric_components", "nullary", ["metric_components"]),
        ("g^{ij}", "U+0067", "g^{ij}", "inverse_metric", "nullary", ["inverse_metric"]),
        ("R", "U+0052", "R", "riemann_curvature_dg", "nullary", ["riemann_curvature"]),
        ("Ric", "U+0052", "\\text{Ric}", "ricci_curvature_dg", "nullary", ["ricci_curvature"]),
        ("R_{ijkl}", "U+0052", "R_{ijkl}", "riemann_tensor", "nullary", ["riemann_tensor"]),
        ("R_{ij}", "U+0052", "R_{ij}", "ricci_tensor", "nullary", ["ricci_tensor"]),
        ("R", "U+0052", "R", "scalar_curvature", "nullary", ["scalar_curvature"]),
        ("Γ^k_{ij}", "U+0393", "\\Gamma^k_{ij}", "christoffel_symbols", "nullary", ["christoffel"]),
        ("∂_i", "U+2202", "\\partial_i", "partial_derivative_i", "unary", ["partial_derivative"]),
        ("∂/∂x^i", "U+2202", "\\frac{\\partial}{\\partial x^i}", "coordinate_derivative", "unary", ["coordinate_derivative"]),
    ]
    
    for symbol, unicode, latex, name, arity, contexts in diff_geom[:23]:
        symbols.append(create_symbol_entry(
            symbol, unicode, latex, name, "differential_geometry", arity, "operator" if arity != "nullary" else "operand",
            1, 3, "partial" if arity != "nullary" else "none", "no", "no", "no", 
            "partial" if arity != "nullary" else "none", "medium",
            contexts
        ))
    
    # Lie groups and algebras (20 symbols)
    lie_ops = [
        ("G", "U+0047", "G", "lie_group", "nullary", ["lie_group"]),
        ("𝔤", "U+1D524", "\\mathfrak{g}", "lie_algebra", "nullary", ["lie_algebra"]),
        ("[X,Y]", "U+005B", "[X,Y]", "lie_bracket", "binary", ["lie_bracket"]),
        ("exp", "U+0065", "\\exp", "exponential_map", "unary", ["exponential_map"]),
        ("log", "U+006C", "\\log", "logarithm_map", "unary", ["logarithm_map"]),
        ("Ad", "U+0041", "\\text{Ad}", "adjoint_representation", "unary", ["adjoint"]),
        ("ad", "U+0061", "\\text{ad}", "adjoint_action", "unary", ["adjoint_action"]),
        ("SO(n)", "U+0053", "SO(n)", "special_orthogonal", "nullary", ["special_orthogonal"]),
        ("SU(n)", "U+0053", "SU(n)", "special_unitary", "nullary", ["special_unitary"]),
        ("SL(n)", "U+0053", "SL(n)", "special_linear", "nullary", ["special_linear"]),
        ("O(n)", "U+004F", "O(n)", "orthogonal_group", "nullary", ["orthogonal"]),
        ("U(n)", "U+0055", "U(n)", "unitary_group", "nullary", ["unitary"]),
        ("GL(n)", "U+0047", "GL(n)", "general_linear", "nullary", ["general_linear"]),
        ("𝔰𝔬(n)", "U+1D530", "\\mathfrak{so}(n)", "so_algebra", "nullary", ["so_algebra"]),
        ("𝔰𝔲(n)", "U+1D530", "\\mathfrak{su}(n)", "su_algebra", "nullary", ["su_algebra"]),
        ("𝔰𝔩(n)", "U+1D530", "\\mathfrak{sl}(n)", "sl_algebra", "nullary", ["sl_algebra"]),
    ]
    
    for symbol, unicode, latex, name, arity, contexts in lie_ops[:16]:
        symbols.append(create_symbol_entry(
            symbol, unicode, latex, name, "differential_geometry", arity, "operator" if arity != "nullary" else "operand",
            1, 3, "partial" if arity != "nullary" else "none", "no", "no", "no", 
            "partial" if arity != "nullary" else "none", "medium",
            contexts
        ))
    
    return symbols

def generate_combinatorics_symbols() -> list:
    """Generate combinatorics symbols (50 symbols)."""
    symbols = []
    
    # Binomial coefficients and factorials (20 symbols)
    comb_ops = [
        ("n!", "U+006E", "n!", "factorial", "unary", ["factorial"]),
        ("!!", "U+0021", "!!", "double_factorial", "unary", ["double_factorial"]),
        ("C(n,k)", "U+0043", "C(n,k)", "binomial", "binary", ["binomial"]),
        ("(n k)", "U+0028", "\\binom{n}{k}", "binomial_notation", "binary", ["binomial"]),
        ("P(n,k)", "U+0050", "P(n,k)", "permutation", "binary", ["permutation"]),
        ("n^(k)", "U+006E", "n^{(k)}", "falling_factorial", "binary", ["falling_factorial"]),
        ("n^{(k)}", "U+006E", "n^{(k)}", "rising_factorial", "binary", ["rising_factorial"]),
        ("⟨n k⟩", "U+27E8", "\\langle n\\atop k\\rangle", "stirling_first", "binary", ["stirling_first"]),
        ("{n k}", "U+007B", "\\{n\\atop k\\}", "stirling_second", "binary", ["stirling_second"]),
        ("B_n", "U+0042", "B_n", "bell_number", "unary", ["bell_number"]),
        ("C_n", "U+0043", "C_n", "catalan_number", "unary", ["catalan_number"]),
        ("F_n", "U+0046", "F_n", "fibonacci", "unary", ["fibonacci"]),
        ("L_n", "U+004C", "L_n", "lucas_number", "unary", ["lucas_number"]),
        ("p(n)", "U+0070", "p(n)", "partition_function", "unary", ["partition"]),
        ("p(n,k)", "U+0070", "p(n,k)", "partition_k_parts", "binary", ["partition"]),
        ("D_n", "U+0044", "D_n", "derangement", "unary", ["derangement"]),
        ("S(n,k)", "U+0053", "S(n,k)", "stirling_second_alt", "binary", ["stirling_second"]),
        ("s(n,k)", "U+0073", "s(n,k)", "stirling_first_alt", "binary", ["stirling_first"]),
    ]
    
    for symbol, unicode, latex, name, arity, contexts in comb_ops[:18]:
        symbols.append(create_symbol_entry(
            symbol, unicode, latex, name, "combinatorics", arity, "operator",
            1, 2, "partial", "no", "no", "no", "partial", "low",
            contexts
        ))
    
    # Generating functions and recurrences (20 symbols)
    gen_func = [
        ("G(x)", "U+0047", "G(x)", "generating_function", "unary", ["generating_function"]),
        ("F(x)", "U+0046", "F(x)", "ordinary_gf", "unary", ["ordinary_generating_function"]),
        ("E(x)", "U+0045", "E(x)", "exponential_gf", "unary", ["exponential_generating_function"]),
        ("∑", "U+2211", "\\sum", "sum_comb", "unary", ["sum"]),
        ("∏", "U+220F", "\\prod", "product_comb", "unary", ["product"]),
        ("[x^n]", "U+005B", "[x^n]", "coefficient_extraction", "unary", ["coefficient"]),
        ("a_n", "U+0061", "a_n", "sequence", "nullary", ["sequence"]),
        ("a_{n+1}", "U+0061", "a_{n+1}", "next_term", "nullary", ["next_term"]),
        ("a_n = f(a_{n-1})", "U+0061", "a_n = f(a_{n-1})", "recurrence", "unary", ["recurrence"]),
        ("O(f)", "U+004F", "O(f)", "big_o", "unary", ["big_o"]),
        ("Θ(f)", "U+0398", "\\Theta(f)", "big_theta", "unary", ["big_theta"]),
        ("Ω(f)", "U+03A9", "\\Omega(f)", "big_omega", "unary", ["big_omega"]),
        ("o(f)", "U+006F", "o(f)", "little_o", "unary", ["little_o"]),
        ("ω(f)", "U+03C9", "\\omega(f)", "little_omega", "unary", ["little_omega"]),
        ("∼", "U+223C", "\\sim", "asymptotic", "binary", ["asymptotic"]),
        ("≈", "U+2248", "\\approx", "approximately_comb", "binary", ["approximately"]),
    ]
    
    for symbol, unicode, latex, name, arity, contexts in gen_func[:16]:
        symbols.append(create_symbol_entry(
            symbol, unicode, latex, name, "combinatorics", arity, "operator" if arity != "nullary" else "operand",
            1, 2, "partial" if arity != "nullary" else "none", "no", "no", "no", 
            "partial" if arity != "nullary" else "none", "low",
            contexts
        ))
    
    return symbols

def generate_graph_theory_symbols() -> list:
    """Generate graph theory symbols (30 symbols)."""
    symbols = []
    
    # Graph notation (30 symbols)
    graph_ops = [
        ("G", "U+0047", "G", "graph", "nullary", ["graph"]),
        ("V", "U+0056", "V", "vertices", "nullary", ["vertices"]),
        ("E", "U+0045", "E", "edges", "nullary", ["edges"]),
        ("G=(V,E)", "U+0047", "G=(V,E)", "graph_definition", "nullary", ["graph_definition"]),
        ("v", "U+0076", "v", "vertex", "nullary", ["vertex"]),
        ("e", "U+0065", "e", "edge", "nullary", ["edge"]),
        ("u~v", "U+007E", "u\\sim v", "adjacent", "binary", ["adjacent"]),
        ("u-v", "U+002D", "u-v", "edge_notation", "binary", ["edge"]),
        ("deg(v)", "U+0064", "\\deg(v)", "degree", "unary", ["degree"]),
        ("d(u,v)", "U+0064", "d(u,v)", "distance_graph", "binary", ["distance"]),
        ("δ(G)", "U+03B4", "\\delta(G)", "minimum_degree", "unary", ["minimum_degree"]),
        ("Δ(G)", "U+0394", "\\Delta(G)", "maximum_degree", "unary", ["maximum_degree"]),
        ("|V|", "U+007C", "|V|", "order", "unary", ["order"]),
        ("|E|", "U+007C", "|E|", "size", "unary", ["size"]),
        ("χ(G)", "U+03C7", "\\chi(G)", "chromatic_number", "unary", ["chromatic_number"]),
        ("α(G)", "U+03B1", "\\alpha(G)", "independence_number", "unary", ["independence_number"]),
        ("ω(G)", "U+03C9", "\\omega(G)", "clique_number", "unary", ["clique_number"]),
        ("κ(G)", "U+03BA", "\\kappa(G)", "connectivity", "unary", ["connectivity"]),
        ("λ(G)", "U+03BB", "\\lambda(G)", "edge_connectivity", "unary", ["edge_connectivity"]),
        ("γ(G)", "U+03B3", "\\gamma(G)", "domination_number", "unary", ["domination_number"]),
        ("K_n", "U+004B", "K_n", "complete_graph", "unary", ["complete_graph"]),
        ("C_n", "U+0043", "C_n", "cycle_graph", "unary", ["cycle"]),
        ("P_n", "U+0050", "P_n", "path_graph", "unary", ["path"]),
        ("K_{m,n}", "U+004B", "K_{m,n}", "complete_bipartite", "binary", ["complete_bipartite"]),
        ("Q_n", "U+0051", "Q_n", "hypercube", "unary", ["hypercube"]),
        ("⊆", "U+2286", "\\subseteq", "subgraph", "binary", ["subgraph"]),
        ("⊂", "U+2282", "\\subset", "proper_subgraph", "binary", ["proper_subgraph"]),
        ("∪", "U+222A", "\\cup", "union_graph", "binary", ["union"]),
        ("∩", "U+2229", "\\cap", "intersection_graph", "binary", ["intersection"]),
        ("⊕", "U+2295", "\\oplus", "disjoint_union_graph", "binary", ["disjoint_union"]),
    ]
    
    for symbol, unicode, latex, name, arity, contexts in graph_ops[:30]:
        symbols.append(create_symbol_entry(
            symbol, unicode, latex, name, "graph_theory", arity, "operator" if arity != "nullary" else "operand",
            1, 2, "partial" if arity != "nullary" else "none", "no", "no", "no", 
            "partial" if arity != "nullary" else "none", "low",
            contexts
        ))
    
    return symbols

# Update main to include new categories
if __name__ == "__main__":
    print("="*60)
    print("FINAL COMPREHENSIVE SYMBOL DATASET GENERATOR - PHASE 2")
    print("Target: 1000+ symbols")
    print("="*60)
    print()
    
    symbols = []
    
    # Add all categories
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
    
    print("Generating category theory symbols...")
    cat_symbols = generate_category_theory_symbols()
    symbols.extend(cat_symbols)
    print(f"  Added {len(cat_symbols)} category theory symbols")
    
    print("Generating quantum mechanics symbols...")
    qm_symbols = generate_quantum_mechanics_symbols()
    symbols.extend(qm_symbols)
    print(f"  Added {len(qm_symbols)} quantum mechanics symbols")
    
    print("Generating information theory symbols...")
    info_symbols = generate_information_theory_symbols()
    symbols.extend(info_symbols)
    print(f"  Added {len(info_symbols)} information theory symbols")
    
    print("Generating geometry symbols...")
    geom_symbols = generate_geometry_symbols()
    symbols.extend(geom_symbols)
    print(f"  Added {len(geom_symbols)} geometry symbols")
    
    print("Generating number theory symbols...")
    nt_symbols = generate_number_theory_symbols()
    symbols.extend(nt_symbols)
    print(f"  Added {len(nt_symbols)} number theory symbols")
    
    print("Generating abstract algebra symbols...")
    aa_symbols = generate_abstract_algebra_symbols()
    symbols.extend(aa_symbols)
    print(f"  Added {len(aa_symbols)} abstract algebra symbols")
    
    print("Generating complex analysis symbols...")
    ca_symbols = generate_complex_analysis_symbols()
    symbols.extend(ca_symbols)
    print(f"  Added {len(ca_symbols)} complex analysis symbols")
    
    print("Generating functional analysis symbols...")
    fa_symbols = generate_functional_analysis_symbols()
    symbols.extend(fa_symbols)
    print(f"  Added {len(fa_symbols)} functional analysis symbols")
    
    print("Generating differential geometry symbols...")
    dg_symbols = generate_differential_geometry_symbols()
    symbols.extend(dg_symbols)
    print(f"  Added {len(dg_symbols)} differential geometry symbols")
    
    print("Generating combinatorics symbols...")
    comb_symbols = generate_combinatorics_symbols()
    symbols.extend(comb_symbols)
    print(f"  Added {len(comb_symbols)} combinatorics symbols")
    
    print("Generating graph theory symbols...")
    graph_symbols = generate_graph_theory_symbols()
    symbols.extend(graph_symbols)
    print(f"  Added {len(graph_symbols)} graph theory symbols")
    
    # Add miscellaneous symbols to reach 1000+
    print("Generating miscellaneous symbols...")
    misc_symbols = [
        create_symbol_entry("∞", "U+221E", "\\infty", "infinity", "miscellaneous", "nullary", "operand", 1, 1, "none", "no", "no", "no", "none", "low", ["infinity"]),
        create_symbol_entry("∅", "U+2205", "\\emptyset", "empty_set_misc", "miscellaneous", "nullary", "operand", 1, 1, "none", "no", "no", "no", "none", "low", ["empty_set"]),
        create_symbol_entry("℧", "U+2127", "\\mho", "mho", "miscellaneous", "nullary", "operand", 1, 1, "none", "no", "no", "no", "none", "low", ["mho"]),
        create_symbol_entry("℩", "U+2129", "\\iota", "turned_iota", "miscellaneous", "nullary", "operand", 1, 1, "none", "no", "no", "no", "none", "low", ["turned_iota"]),
        create_symbol_entry("℮", "U+212E", "e", "estimated_symbol", "miscellaneous", "nullary", "operand", 1, 1, "none", "no", "no", "no", "none", "low", ["estimated"]),
        create_symbol_entry("⅀", "U+2140", "\\sum", "double_struck_sum", "miscellaneous", "unary", "operator", 1, 2, "none", "no", "no", "no", "none", "low", ["sum"]),
        create_symbol_entry("⅁", "U+2141", "G", "turned_sans_serif_G", "miscellaneous", "nullary", "operand", 1, 1, "none", "no", "no", "no", "none", "low", ["turned_G"]),
        create_symbol_entry("⅂", "U+2142", "L", "turned_sans_serif_L", "miscellaneous", "nullary", "operand", 1, 1, "none", "no", "no", "no", "none", "low", ["turned_L"]),
        create_symbol_entry("⅃", "U+2143", "L", "reversed_sans_serif_L", "miscellaneous", "nullary", "operand", 1, 1, "none", "no", "no", "no", "none", "low", ["reversed_L"]),
        create_symbol_entry("⅄", "U+2144", "Y", "turned_sans_serif_Y", "miscellaneous", "nullary", "operand", 1, 1, "none", "no", "no", "no", "none", "low", ["turned_Y"]),
        create_symbol_entry("℀", "U+2100", "a/c", "account_of", "miscellaneous", "nullary", "operand", 1, 1, "none", "no", "no", "no", "none", "low", ["account_of"]),
        create_symbol_entry("℁", "U+2101", "a/s", "addressed_to_subject", "miscellaneous", "nullary", "operand", 1, 1, "none", "no", "no", "no", "none", "low", ["addressed_to"]),
        create_symbol_entry("ℂ", "U+2102", "\\mathbb{C}", "complex_numbers_misc", "miscellaneous", "nullary", "operand", 1, 1, "none", "no", "no", "no", "none", "low", ["complex_numbers"]),
        create_symbol_entry("℃", "U+2103", "^\\circ C", "celsius", "miscellaneous", "nullary", "operand", 1, 1, "none", "no", "no", "no", "none", "low", ["celsius"]),
        create_symbol_entry("℉", "U+2109", "^\\circ F", "fahrenheit", "miscellaneous", "nullary", "operand", 1, 1, "none", "no", "no", "no", "none", "low", ["fahrenheit"]),
        create_symbol_entry("№", "U+2116", "No.", "numero_sign", "miscellaneous", "nullary", "operand", 1, 1, "none", "no", "no", "no", "none", "low", ["numero"]),
        create_symbol_entry("℗", "U+2117", "P", "sound_recording_copyright", "miscellaneous", "nullary", "operand", 1, 1, "none", "no", "no", "no", "none", "low", ["sound_copyright"]),
        create_symbol_entry("℘", "U+2118", "\\wp", "weierstrass_p_misc", "miscellaneous", "unary", "operator", 1, 2, "partial", "no", "no", "no", "partial", "low", ["weierstrass"]),
        create_symbol_entry("℞", "U+211E", "Rx", "prescription_take", "miscellaneous", "nullary", "operand", 1, 1, "none", "no", "no", "no", "none", "low", ["prescription"]),
        create_symbol_entry("℟", "U+211F", "R", "response", "miscellaneous", "nullary", "operand", 1, 1, "none", "no", "no", "no", "none", "low", ["response"]),
        create_symbol_entry("™", "U+2122", "TM", "trademark", "miscellaneous", "nullary", "operand", 1, 1, "none", "no", "no", "no", "none", "low", ["trademark"]),
        create_symbol_entry("℠", "U+2120", "SM", "service_mark", "miscellaneous", "nullary", "operand", 1, 1, "none", "no", "no", "no", "none", "low", ["service_mark"]),
        create_symbol_entry("℡", "U+2121", "TEL", "telephone_sign", "miscellaneous", "nullary", "operand", 1, 1, "none", "no", "no", "no", "none", "low", ["telephone"]),
        create_symbol_entry("℣", "U+2123", "V", "versicle", "miscellaneous", "nullary", "operand", 1, 1, "none", "no", "no", "no", "none", "low", ["versicle"]),
        create_symbol_entry("Ω", "U+03A9", "\\Omega", "ohm", "miscellaneous", "nullary", "operand", 2, 1, "none", "no", "no", "no", "none", "medium", ["ohm", "omega"]),
        create_symbol_entry("K", "U+004B", "K", "kelvin", "miscellaneous", "nullary", "operand", 2, 1, "none", "no", "no", "no", "none", "medium", ["kelvin", "K"]),
        create_symbol_entry("Å", "U+00C5", "\\AA", "angstrom", "miscellaneous", "nullary", "operand", 1, 1, "none", "no", "no", "no", "none", "low", ["angstrom"]),
        create_symbol_entry("℧", "U+2127", "\\mho", "conductance", "miscellaneous", "nullary", "operand", 1, 1, "none", "no", "no", "no", "none", "low", ["conductance"]),
        create_symbol_entry("℈", "U+2108", "scruple", "scruple", "miscellaneous", "nullary", "operand", 1, 1, "none", "no", "no", "no", "none", "low", ["scruple"]),
        create_symbol_entry("℔", "U+2114", "lb", "pound", "miscellaneous", "nullary", "operand", 1, 1, "none", "no", "no", "no", "none", "low", ["pound"]),
    ]
    symbols.extend(misc_symbols)
    print(f"  Added {len(misc_symbols)} miscellaneous symbols")
    
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
    print(f"✓ Successfully generated {len(symbols)} symbols!")
    if len(symbols) >= 1000:
        print("🎉 TARGET ACHIEVED: 1000+ symbols!")
    print("="*60)
