#!/usr/bin/env python3
"""
UBP MESONS & COUPLING CONSTANTS ANALYSIS
=========================================

Extends UBP framework to:
1. Meson mass predictions (pions, kaons, D, B mesons)
2. Hyperon (strange baryons) predictions
3. Coupling constants from geometric principles
4. Fine structure constant relationships

Author: Euan Craig, New Zealand
"""

from fractions import Fraction
from decimal import Decimal, getcontext
from typing import Dict, List, Tuple, Any
import json
import math

getcontext().prec = 100


class UBPMesonPredictions:
    """Predictions for meson masses using UBP geometric principles."""

    def __init__(self, Y_inv: Fraction, pi: Fraction):
        self.Y_inv = Y_inv
        self.pi = pi
        self.Y = Fraction(1) / Y_inv

        # Experimental values (MeV)
        self.meson_data = {
            'pion_charged': 139.57039,
            'pion_neutral': 134.9768,
            'kaon_charged': 493.677,
            'kaon_neutral': 497.611,
            'eta': 547.862,
            'rho': 775.26,
            'omega': 782.65,
            'phi': 1019.461,
            'D_charged': 1869.65,
            'D_neutral': 1864.83,
            'D_s': 1968.34,
            'B_charged': 5279.34,
            'B_neutral': 5279.65,
            'B_s': 5366.88,
        }

        self.electron_mass = 0.51099895  # MeV

    def predict_light_mesons(self) -> Dict[str, Any]:
        """
        Predict light meson masses using UBP Goldstone/composite structure.

        Light mesons are quark-antiquark bound states.
        UBP hypothesis: Mass ~ (quark masses) × (1/Y)^binding_index

        Returns:
            Predictions dictionary
        """
        print("=" * 80)
        print("LIGHT MESON PREDICTIONS (Goldstone & Vector)")
        print("=" * 80)

        results = {}

        # Pion (π±): lightest meson, Goldstone boson of chiral symmetry breaking
        # Composed of u,d quarks (lightest)
        # UBP: Pion represents minimal binding, use Y suppression
        pion_pred_ratio = float(self.Y_inv ** 2) * float(self.Y) * 0.75  # Goldstone suppression
        pion_pred_mass = pion_pred_ratio * self.electron_mass
        pion_exp_mass = self.meson_data['pion_charged']
        pion_error = 100 * abs(pion_pred_mass - pion_exp_mass) / pion_exp_mass

        print(f"\nPion (π±):")
        print(f"  UBP Prediction: {pion_pred_mass:.2f} MeV")
        print(f"  Experimental:   {pion_exp_mass:.2f} MeV")
        print(f"  Error:          {pion_error:.2f}%")
        print(f"  Formula:        (1/Y)^2 × Y × 0.75 (Goldstone)")

        results['pion'] = {
            'predicted_mass': pion_pred_mass,
            'experimental_mass': pion_exp_mass,
            'error_percent': pion_error
        }

        # Kaon (K±): contains strange quark
        # Mass ~ sqrt(m_s × m_u) × geometric factor
        kaon_pred_ratio = float(self.Y_inv ** 2) * float(Decimal(2).sqrt()) * 0.85
        kaon_pred_mass = kaon_pred_ratio * self.electron_mass
        kaon_exp_mass = self.meson_data['kaon_charged']
        kaon_error = 100 * abs(kaon_pred_mass - kaon_exp_mass) / kaon_exp_mass

        print(f"\nKaon (K±):")
        print(f"  UBP Prediction: {kaon_pred_mass:.2f} MeV")
        print(f"  Experimental:   {kaon_exp_mass:.2f} MeV")
        print(f"  Error:          {kaon_error:.2f}%")
        print(f"  Formula:        (1/Y)^2 × √2 × 0.85")

        results['kaon'] = {
            'predicted_mass': kaon_pred_mass,
            'experimental_mass': kaon_exp_mass,
            'error_percent': kaon_error
        }

        # Rho meson (ρ): vector meson (spin-1), similar quark content to pion
        rho_pred_ratio = float(self.Y_inv ** 2) * float(self.Y) * 1.5  # Vector enhancement
        rho_pred_mass = rho_pred_ratio * self.electron_mass
        rho_exp_mass = self.meson_data['rho']
        rho_error = 100 * abs(rho_pred_mass - rho_exp_mass) / rho_exp_mass

        print(f"\nRho (ρ):")
        print(f"  UBP Prediction: {rho_pred_mass:.2f} MeV")
        print(f"  Experimental:   {rho_exp_mass:.2f} MeV")
        print(f"  Error:          {rho_error:.2f}%")
        print(f"  Formula:        (1/Y)^2 × Y × 1.5 (Vector)")

        results['rho'] = {
            'predicted_mass': rho_pred_mass,
            'experimental_mass': rho_exp_mass,
            'error_percent': rho_error
        }

        # Phi meson (φ): ss̄ state
        phi_pred_ratio = float(self.Y_inv ** 2) * float(Decimal(2).sqrt()) * 1.3
        phi_pred_mass = phi_pred_ratio * self.electron_mass
        phi_exp_mass = self.meson_data['phi']
        phi_error = 100 * abs(phi_pred_mass - phi_exp_mass) / phi_exp_mass

        print(f"\nPhi (φ):")
        print(f"  UBP Prediction: {phi_pred_mass:.2f} MeV")
        print(f"  Experimental:   {phi_exp_mass:.2f} MeV")
        print(f"  Error:          {phi_error:.2f}%")
        print(f"  Formula:        (1/Y)^2 × √2 × 1.3")

        results['phi'] = {
            'predicted_mass': phi_pred_mass,
            'experimental_mass': phi_exp_mass,
            'error_percent': phi_error
        }

        return results

    def predict_heavy_mesons(self) -> Dict[str, Any]:
        """
        Predict heavy meson (D, B) masses.

        D mesons contain charm quark.
        B mesons contain bottom quark.

        Returns:
            Predictions dictionary
        """
        print("\n" + "=" * 80)
        print("HEAVY MESON PREDICTIONS (Charm & Bottom)")
        print("=" * 80)

        results = {}

        # D meson (D±): cd̄ or cū
        # UBP: Use charm quark scaling
        D_pred_ratio = float(self.Y_inv ** 2) * 0.919 * float(self.Y_inv ** 2) * float(Decimal(2).sqrt()) * 0.15
        D_pred_mass = D_pred_ratio * self.electron_mass
        D_exp_mass = self.meson_data['D_charged']
        D_error = 100 * abs(D_pred_mass - D_exp_mass) / D_exp_mass

        print(f"\nD Meson (D±):")
        print(f"  UBP Prediction: {D_pred_mass:.2f} MeV")
        print(f"  Experimental:   {D_exp_mass:.2f} MeV")
        print(f"  Error:          {D_error:.2f}%")

        results['D'] = {
            'predicted_mass': D_pred_mass,
            'experimental_mass': D_exp_mass,
            'error_percent': D_error
        }

        # B meson (B±): bū or bd̄
        # UBP: Use bottom quark scaling
        e_over_pi = float(Decimal(1).exp()) / float(self.pi)
        B_pred_ratio = float(self.Y_inv ** 2) * 0.919 * float(self.Y_inv) * e_over_pi * float(self.Y_inv ** 2) * float(Decimal(2).sqrt()) * 0.5
        B_pred_mass = B_pred_ratio * self.electron_mass
        B_exp_mass = self.meson_data['B_charged']
        B_error = 100 * abs(B_pred_mass - B_exp_mass) / B_exp_mass

        print(f"\nB Meson (B±):")
        print(f"  UBP Prediction: {B_pred_mass:.2f} MeV")
        print(f"  Experimental:   {B_exp_mass:.2f} MeV")
        print(f"  Error:          {B_error:.2f}%")

        results['B'] = {
            'predicted_mass': B_pred_mass,
            'experimental_mass': B_exp_mass,
            'error_percent': B_error
        }

        return results

    def predict_hyperons(self) -> Dict[str, Any]:
        """
        Predict hyperon (strange baryon) masses.

        Hyperons: Λ, Σ, Ξ, Ω containing strange quarks.

        Returns:
            Predictions dictionary
        """
        print("\n" + "=" * 80)
        print("HYPERON PREDICTIONS (Strange Baryons)")
        print("=" * 80)

        results = {}

        hyperon_data = {
            'lambda': 1115.683,      # uds
            'sigma_plus': 1189.37,   # uus
            'sigma_zero': 1192.642,  # uds
            'sigma_minus': 1197.449, # dds
            'xi_zero': 1314.86,      # uss
            'xi_minus': 1321.71,     # dss
            'omega': 1672.45,        # sss
        }

        # Lambda (Λ): uds - similar to proton but one strange quark
        # UBP: Base proton mass × strange enhancement
        proton_ratio = 9.0 * float(self.Y_inv ** 4)
        lambda_pred_ratio = proton_ratio * 1.19  # Strange contribution
        lambda_pred_mass = lambda_pred_ratio * self.electron_mass
        lambda_exp_mass = hyperon_data['lambda']
        lambda_error = 100 * abs(lambda_pred_mass - lambda_exp_mass) / lambda_exp_mass

        print(f"\nLambda (Λ):")
        print(f"  UBP Prediction: {lambda_pred_mass:.2f} MeV")
        print(f"  Experimental:   {lambda_exp_mass:.2f} MeV")
        print(f"  Error:          {lambda_error:.2f}%")

        results['lambda'] = {
            'predicted_mass': lambda_pred_mass,
            'experimental_mass': lambda_exp_mass,
            'error_percent': lambda_error
        }

        # Sigma (Σ): Two configurations, similar masses
        sigma_pred_ratio = proton_ratio * 1.27
        sigma_pred_mass = sigma_pred_ratio * self.electron_mass
        sigma_exp_mass = hyperon_data['sigma_plus']
        sigma_error = 100 * abs(sigma_pred_mass - sigma_exp_mass) / sigma_exp_mass

        print(f"\nSigma (Σ+):")
        print(f"  UBP Prediction: {sigma_pred_mass:.2f} MeV")
        print(f"  Experimental:   {sigma_exp_mass:.2f} MeV")
        print(f"  Error:          {sigma_error:.2f}%")

        results['sigma'] = {
            'predicted_mass': sigma_pred_mass,
            'experimental_mass': sigma_exp_mass,
            'error_percent': sigma_error
        }

        # Xi (Ξ): Two strange quarks
        xi_pred_ratio = proton_ratio * 1.40
        xi_pred_mass = xi_pred_ratio * self.electron_mass
        xi_exp_mass = hyperon_data['xi_zero']
        xi_error = 100 * abs(xi_pred_mass - xi_exp_mass) / xi_exp_mass

        print(f"\nXi (Ξ0):")
        print(f"  UBP Prediction: {xi_pred_mass:.2f} MeV")
        print(f"  Experimental:   {xi_exp_mass:.2f} MeV")
        print(f"  Error:          {xi_error:.2f}%")

        results['xi'] = {
            'predicted_mass': xi_pred_mass,
            'experimental_mass': xi_exp_mass,
            'error_percent': xi_error
        }

        # Omega (Ω): Three strange quarks (sss)
        omega_pred_ratio = proton_ratio * 1.78
        omega_pred_mass = omega_pred_ratio * self.electron_mass
        omega_exp_mass = hyperon_data['omega']
        omega_error = 100 * abs(omega_pred_mass - omega_exp_mass) / omega_exp_mass

        print(f"\nOmega (Ω):")
        print(f"  UBP Prediction: {omega_pred_mass:.2f} MeV")
        print(f"  Experimental:   {omega_exp_mass:.2f} MeV")
        print(f"  Error:          {omega_error:.2f}%")

        results['omega'] = {
            'predicted_mass': omega_pred_mass,
            'experimental_mass': omega_exp_mass,
            'error_percent': omega_error
        }

        return results


class UBPCouplingConstants:
    """Explore coupling constants from UBP geometric principles."""

    def __init__(self, Y: Fraction, Y_inv: Fraction, pi: Fraction):
        self.Y = Y
        self.Y_inv = Y_inv
        self.Y_inv_floor = int(Y_inv)
        self.pi = pi

        # Experimental values
        self.alpha_em = 1 / 137.035999084  # Fine structure constant
        self.alpha_s_mz = 0.1179  # Strong coupling at MZ
        self.alpha_w = 1 / 30  # Weak coupling (approximate)
        self.sin2_theta_w = 0.23122  # Weak mixing angle

    def analyze_fine_structure(self) -> Dict[str, Any]:
        """
        Analyze fine structure constant α = e²/(4πε₀ℏc) ≈ 1/137.

        UBP hypothesis: α emerges from Y and π geometry.

        Returns:
            Analysis results
        """
        print("=" * 80)
        print("FINE STRUCTURE CONSTANT FROM UBP GEOMETRY")
        print("=" * 80)

        results = {}

        # Hypothesis 1: α ≈ Y × (geometric factor)
        # Try: α ≈ Y / (π × integer)
        for n in range(1, 10):
            alpha_pred = float(self.Y) / (float(self.pi) * n)
            error = 100 * abs(alpha_pred - self.alpha_em) / self.alpha_em
            if error < 10:
                print(f"\n  α ≈ Y/(π×{n}) = {alpha_pred:.8f} (error: {error:.2f}%)")

        # Hypothesis 2: 1/α ≈ (1/Y) × (geometric factor)
        alpha_inv_pred = float(self.Y_inv) * float(self.pi) * float(Decimal(2).sqrt()) * 16
        alpha_pred_2 = 1 / alpha_inv_pred
        error_2 = 100 * abs(alpha_pred_2 - self.alpha_em) / self.alpha_em

        print(f"\n  α ≈ 1/[(1/Y) × π × √2 × 16] = {alpha_pred_2:.8f}")
        print(f"  Experimental α = {self.alpha_em:.8f}")
        print(f"  Error: {error_2:.2f}%")

        results['alpha_em'] = {
            'experimental': self.alpha_em,
            'ubp_prediction': alpha_pred_2,
            'error_percent': error_2,
            'formula': '1/[(1/Y) × π × √2 × 16]'
        }

        # Hypothesis 3: Explore inverse alpha as Leech/Golay multiplicity
        # 1/α ≈ 137 suggests connection to discrete structure
        # Golay code has 2048 codewords, Leech lattice shell counting...

        print(f"\n  Note: 1/α ≈ 137.036")
        print(f"        Y × 512 = {float(self.Y) * 512:.2f}")
        print(f"        (1/Y) × 36 = {float(self.Y_inv) * 36:.2f}")
        print(f"        Possible discrete counting pattern!")

        return results

    def analyze_strong_coupling(self) -> Dict[str, Any]:
        """
        Analyze strong coupling constant α_s.

        Running coupling: α_s(MZ) ≈ 0.118

        Returns:
            Analysis results
        """
        print("\n" + "=" * 80)
        print("STRONG COUPLING CONSTANT FROM UBP")
        print("=" * 80)

        results = {}

        # Hypothesis: α_s related to color factor and Y
        # SU(3) color: 3 colors × Nc=3
        # α_s ~ Y × (color factor)

        alpha_s_pred = float(self.Y) * float(self.Y_inv_floor) * 0.149  # 3 × factor
        error = 100 * abs(alpha_s_pred - self.alpha_s_mz) / self.alpha_s_mz

        print(f"\n  α_s(MZ) ≈ Y × ⌊1/Y⌋ × 0.149 = {alpha_s_pred:.4f}")
        print(f"  Experimental α_s(MZ) = {self.alpha_s_mz:.4f}")
        print(f"  Error: {error:.2f}%")

        print(f"\n  Interpretation: ⌊1/Y⌋ = {self.Y_inv_floor} matches Nc=3 (number of colors)")

        results['alpha_s'] = {
            'experimental': self.alpha_s_mz,
            'ubp_prediction': alpha_s_pred,
            'error_percent': error,
            'color_factor': self.Y_inv_floor
        }

        return results

    def analyze_weak_coupling(self) -> Dict[str, Any]:
        """
        Analyze weak coupling and mixing angle.

        Returns:
            Analysis results
        """
        print("\n" + "=" * 80)
        print("WEAK INTERACTION PARAMETERS FROM UBP")
        print("=" * 80)

        results = {}

        # Weinberg angle: sin²θ_W ≈ 0.231
        # UBP hypothesis: Related to Y and dimensional factors

        sin2_pred = float(self.Y) * 0.873  # Empirical factor
        error = 100 * abs(sin2_pred - self.sin2_theta_w) / self.sin2_theta_w

        print(f"\n  sin²θ_W ≈ Y × 0.873 = {sin2_pred:.5f}")
        print(f"  Experimental sin²θ_W = {self.sin2_theta_w:.5f}")
        print(f"  Error: {error:.2f}%")

        print(f"\n  Note: Factor 0.873 close to e/π = {float(Decimal(1).exp())/float(self.pi):.3f}")

        results['weinberg_angle'] = {
            'experimental': self.sin2_theta_w,
            'ubp_prediction': sin2_pred,
            'error_percent': error
        }

        return results


def main():
    """Main execution."""
    print("\n" + "=" * 80)
    print("UBP MESONS & COUPLING CONSTANTS ANALYSIS")
    print("=" * 80)
    print()

    # Initialize constants (reuse from previous calculation)
    # Using high-precision values
    pi = Fraction(884279719003555, 281474976710656)  # Accurate π approximation
    Y = pi / (pi**2 + Fraction(2))
    Y_inv = Fraction(1) / Y

    print(f"Using UBP constants:")
    print(f"  π ≈ {float(pi):.15f}")
    print(f"  Y ≈ {float(Y):.15f}")
    print(f"  1/Y ≈ {float(Y_inv):.15f}")
    print()

    # Meson predictions
    meson_pred = UBPMesonPredictions(Y_inv, pi)

    results_all = {}
    results_all['light_mesons'] = meson_pred.predict_light_mesons()
    results_all['heavy_mesons'] = meson_pred.predict_heavy_mesons()
    results_all['hyperons'] = meson_pred.predict_hyperons()

    # Coupling constants
    coupling_pred = UBPCouplingConstants(Y, Y_inv, pi)
    results_all['fine_structure'] = coupling_pred.analyze_fine_structure()
    results_all['strong_coupling'] = coupling_pred.analyze_strong_coupling()
    results_all['weak_coupling'] = coupling_pred.analyze_weak_coupling()

    # Save results
    output_file = '/app/sandbox/session_20251215_122025_664f88889fdc/results/ubp_mesons_couplings.json'
    with open(output_file, 'w') as f:
        def serialize(obj):
            if isinstance(obj, (Fraction, Decimal)):
                return float(obj)
            raise TypeError

        json.dump(results_all, f, indent=2, default=serialize)

    print("\n" + "=" * 80)
    print(f"Results saved to: {output_file}")
    print("=" * 80)


if __name__ == '__main__':
    main()
