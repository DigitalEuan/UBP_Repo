"""
# =============================================================================
# UBP Universal Continuous ALU v9.1 (Grand Unified Sovereign Edition - Restored)
# =============================================================================
* ZERO DEPENDENCIES: No math, no cmath, no numpy.
* All transcendental functions implemented via Taylor/Newton/Lanczos series.
* Supports complex numbers and automatic differentiation via Dual.
* Core projection: eml(x, y) = exp(x) - ln(y)
* Inspired by: All elementary functions from a single operator
Andrzej Odrzywolek
Institute of Theoretical Physics, Jagiellonian University, 30-348 Krakow, Poland
E-mail: andrzej.odrzywolek@uj.edu.pl
April 7, 2026
"""
_PI = 3.14159265358979323846264338327950288419716939937510 + 0j
_E_CONST = 2.71828182845904523536028747135266249775724709369995 + 0j
_SQRT2PI = 2.5066282746310005024157652848110452530069867406099 + 0j

class Dual:
    __slots__ = ('r', 'd')
    def __init__(self, real, deriv=0.0):
        self.r = complex(real) if not isinstance(real, complex) else real
        self.d = complex(deriv) if not isinstance(deriv, complex) else deriv
    def __repr__(self): return f"Dual({self.r}, {self.d})"
    def _promote(self, o):
        if isinstance(o, Dual): return o
        if isinstance(o, complex): return Dual(o, 0j)
        return Dual(complex(o), 0j)
    def __add__(self, o): o = self._promote(o); return Dual(self.r + o.r, self.d + o.d)
    def __radd__(self, o): return self.__add__(o)
    def __sub__(self, o): o = self._promote(o); return Dual(self.r - o.r, self.d - o.d)
    def __rsub__(self, o): o = self._promote(o); return Dual(o.r - self.r, o.d - self.d)
    def __mul__(self, o): o = self._promote(o); return Dual(self.r * o.r, self.r * o.d + self.d * o.r)
    def __rmul__(self, o): return self.__mul__(o)
    def __truediv__(self, o):
        o = self._promote(o)
        if o.r == 0: return Dual(complex('nan'), complex('nan'))
        return Dual(self.r / o.r, (self.d * o.r - self.r * o.d) / (o.r * o.r))
    def __rtruediv__(self, o): o = self._promote(o); return o.__truediv__(self)
    def __pow__(self, n):
        n_c = complex(n) if not isinstance(n, (complex, Dual)) else (n.r if isinstance(n, Dual) else n)
        if self.r == 0 and n_c.real <= 0: return Dual(complex('nan'), complex('nan'))
        val = self.r ** n_c
        deriv = n_c * (self.r ** (n_c - 1)) * self.d
        return Dual(val, deriv)
    def __neg__(self): return Dual(-self.r, -self.d)
    def __abs__(self): return abs(self.r)

def _pure_exp(z, terms=100):
    z = complex(z) if not isinstance(z, complex) else z
    result, term = 1.0 + 0j, 1.0 + 0j  # MUST BE 1.0 for exp!
    for n in range(1, terms):
        term *= z / n
        result += term
        if abs(term) < 1e-18: break
    return result

def _pure_ln(z, iterations=50):
    z = complex(z) if not isinstance(z, complex) else z
    if z == 0: return complex('-inf')
    w = complex(0.5 * (abs(z) - 1) / (abs(z) + 1), 0) if abs(z) > 0.1 else complex(-1, 0)
    for _ in range(iterations):
        ew = _pure_exp(w)
        denom = z + ew
        if denom == 0: break
        w += 2 * (z - ew) / denom
        if abs(z - ew) < 1e-16: break
    return w

def _pure_sqrt(z, iterations=50):
    z = complex(z) if not isinstance(z, complex) else z
    if z == 0: return 0j
    w = complex(abs(z)**0.5, 0) if z.imag == 0 else complex(1, 1)
    for _ in range(iterations):
        w_new = 0.5 * (w + z / w)
        if abs(w_new - w) < 1e-16: break
        w = w_new
    return w

def _pure_sin(z, terms=50):
    z = complex(z) if not isinstance(z, complex) else z
    result, term = 0.0 + 0j, z
    z2 = z * z
    for n in range(terms):
        result += term
        term *= -z2 / ((2*n + 2) * (2*n + 3))
        if abs(term) < 1e-18: break
    return result

def _pure_cos(z, terms=50):
    z = complex(z) if not isinstance(z, complex) else z
    result, term = 0.0 + 0j, 1.0 + 0j # MUST BE 0.0 for cos!
    z2 = z * z
    for n in range(terms):
        result += term
        term *= -z2 / ((2*n + 1) * (2*n + 2))
        if abs(term) < 1e-18: break
    return result

class GrandUnifiedEmlALU:
    def __init__(self):
        self.C1 = 1.0 + 0j
        self.C2 = 2.0 + 0j
        self.C4 = 4.0 + 0j
        self.C6 = 6.0 + 0j
        self.C15 = 15.0 + 0j
        self.PI = _PI
        self.E_CONST = _E_CONST
        self.SQRT2PI = _SQRT2PI
        self.I = 1j
        self.MINUS_I = -1j
        self.TWO_I = self.C2 * self.I

        self.E = self.eml(self.C1, self.C1)
        self.EXP_E = self.eml(self.E, self.C1)
        self.ZERO = self.eml(self.C1, self.EXP_E)
        self.E_MINUS_1 = self.eml(self.C1, self.E)
        self.PHI = self.divide(self.add(self.C1, self.sqrt(5.0 + 0j)), self.C2)
        self.TRIADIC_MONAD = self.multiply(self.multiply(self.PI, self.PHI), self.E)

        self._lanczos_g = 7
        self._lanczos_coef = [
            0.99999999999980993, 676.5203681218851, -1259.1392167224028,
            771.32342877765313, -176.61502916214059, 12.507343278686905,
            -0.13857109526572012, 9.9843695780195716e-6, 1.5056327351493116e-7
        ]

    @staticmethod
    def eml(x, y): return _pure_exp(x) - _pure_ln(y)

    @staticmethod
    def _val(x): return x.r if isinstance(x, Dual) else (complex(x) if not isinstance(x, complex) else x)

    @staticmethod
    def _deriv(x): return x.d if isinstance(x, Dual) else 0j

    def exp(self, x):
        v = self._val(x); dv = self._deriv(x)
        ev = _pure_exp(v)
        return Dual(ev, ev * dv) if isinstance(x, Dual) else ev

    def ln(self, x):
        v = self._val(x); dv = self._deriv(x)
        if v == 0: return Dual(complex('-inf'), complex('nan')) if isinstance(x, Dual) else complex('-inf')
        lv = _pure_ln(v)
        return Dual(lv, dv / v) if isinstance(x, Dual) else lv

    def add(self, x, y): return x + y
    def subtract(self, x, y): return x - y
    def multiply(self, x, y): return x * y
    def divide(self, x, y):
        yv = self._val(y) if isinstance(y, Dual) else complex(y)
        if yv == 0: return Dual(complex('nan'), complex('nan')) if isinstance(x, Dual) or isinstance(y, Dual) else complex('nan')
        return x / y
    def power(self, x, y): return x ** y
    def sqrt(self, x):
        v = self._val(x); dv = self._deriv(x)
        sv = _pure_sqrt(v)
        return Dual(sv, dv / (2 * sv)) if isinstance(x, Dual) else sv

    def dot_product(self, vec_a, vec_b):
        res = self.ZERO
        for a, b in zip(vec_a, vec_b): res = self.add(res, self.multiply(a, b))
        return res

    def cross_product(self, a, b):
        return [
            self.subtract(self.multiply(a[1], b[2]), self.multiply(a[2], b[1])),
            self.subtract(self.multiply(a[2], b[0]), self.multiply(a[0], b[2])),
            self.subtract(self.multiply(a[0], b[1]), self.multiply(a[1], b[0]))
        ]

    def magnitude(self, v): return self.sqrt(self.dot_product(v, v))

    def sinh(self, x):
        ex = self.exp(x); emx = self.exp(self.subtract(self.ZERO, x))
        return self.divide(self.subtract(ex, emx), self.C2)
    def cosh(self, x):
        ex = self.exp(x); emx = self.exp(self.subtract(self.ZERO, x))
        return self.divide(self.add(ex, emx), self.C2)
    def tanh(self, x): return self.divide(self.sinh(x), self.cosh(x))

    def sin(self, x):
        if isinstance(x, Dual):
            v, dv = x.r, x.d
            sv = _pure_sin(v); cv = _pure_cos(v)
            return Dual(sv, cv * dv)
        return _pure_sin(x)

    def cos(self, x):
        if isinstance(x, Dual):
            v, dv = x.r, x.d
            sv = _pure_sin(v); cv = _pure_cos(v)
            return Dual(cv, -sv * dv)
        return _pure_cos(x)

    def tan(self, x): return self.divide(self.sin(x), self.cos(x))

    def arcsin(self, x):
        ix = self.multiply(self.I, x)
        x2 = self.power(x, self.C2)
        sqrt_term = self.sqrt(self.subtract(self.C1, x2))
        return self.multiply(self.MINUS_I, self.ln(self.add(ix, sqrt_term)))

    def arccos(self, x):
        x2 = self.power(x, self.C2)
        i_sqrt = self.multiply(self.I, self.sqrt(self.subtract(self.C1, x2)))
        return self.multiply(self.MINUS_I, self.ln(self.add(x, i_sqrt)))

    def arctan(self, x):
        ix = self.multiply(self.I, x)
        num = self.subtract(self.C1, ix)
        den = self.add(self.C1, ix)
        i_half = self.divide(self.I, self.C2)
        return self.multiply(i_half, self.ln(self.divide(num, den)))

    def fft(self, x, invert=False):
        n = len(x)
        if n <= 1: return x[:]
        even = self.fft(x[0::2], invert)
        odd = self.fft(x[1::2], invert)
        direction = self.I if invert else self.MINUS_I
        T = []
        for k in range(n // 2):
            angle = self.multiply(self.multiply(self.C2, self.PI), self.divide(complex(k), complex(n)))
            twiddle = self.exp(self.multiply(-direction if not invert else direction, angle))
            T.append(self.multiply(twiddle, odd[k]))
        return [self.add(even[k], T[k]) for k in range(n // 2)] + \
               [self.subtract(even[k], T[k]) for k in range(n // 2)]

    def ifft(self, x):
        n = len(x)
        transformed = self.fft(x, invert=True)
        return [self.divide(val, complex(n)) for val in transformed]

    def derivative(self, func, x):
        return func(Dual(x, 1.0)).d

    def integrate(self, func, a, b, tol=1e-10, max_depth=50):
        def simp(f, a, b):
            c = self.divide(self.add(a, b), self.C2)
            return self.multiply(self.subtract(b, a), 
                               self.divide(self.add(self.add(f(a), self.multiply(self.C4, f(c))), f(b)), self.C6))
        def recur(f, a, b, tol, whole, depth):
            if depth >= max_depth: return whole
            c = self.divide(self.add(a, b), self.C2)
            left = simp(f, a, c); right = simp(f, c, b)
            combined = self.add(left, right)
            if abs(self._val(self.subtract(combined, whole))) <= 15 * tol:
                return self.add(combined, self.divide(self.subtract(combined, whole), self.C15))
            return self.add(recur(f, a, c, tol/2, left, depth+1),
                          recur(f, c, b, tol/2, right, depth+1))
        a_c, b_c = complex(a), complex(b)
        initial = simp(func, a_c, b_c)
        return recur(func, a_c, b_c, tol, initial, 0)

    def gamma(self, z):
        zv = self._val(z); dz = self._deriv(z)
        is_dual = isinstance(z, Dual)

        if zv.real < 0.5:
            sin_term = self.sin(self.multiply(self.PI, z))
            gamma_ref = self.gamma(self.subtract(self.C1, z))
            result = self.divide(self.PI, self.multiply(sin_term, gamma_ref))
            return result if not is_dual else Dual(self._val(result), self._deriv(result))

        z_shifted = self.subtract(z, self.C1)
        x = self._lanczos_coef[0] + 0j
        for k in range(1, len(self._lanczos_coef)):
            x = self.add(x, self.divide(self._lanczos_coef[k] + 0j, self.add(z_shifted, complex(k))))

        t = self.add(z_shifted, self._lanczos_g + 0.5)
        exp_term = self.exp(self.subtract(self.ZERO, t))
        power_term = self.power(t, self.add(z_shifted, 0.5 + 0j))

        result = self.multiply(self.SQRT2PI, self.multiply(exp_term, self.multiply(power_term, x)))

        if is_dual:
            h = 1e-7
            gamma_plus = self._val(self.gamma(self.add(z, complex(h))))
            gamma_minus = self._val(self.gamma(self.subtract(z, complex(h))))
            deriv_approx = self.divide(self.subtract(gamma_plus, gamma_minus), self.multiply(self.C2, complex(h)))
            return Dual(self._val(result), dz * deriv_approx)
        return result

    def factorial(self, n):
        return self.gamma(self.add(n, self.C1))

def run_grand_audit():
    alu = GrandUnifiedEmlALU()
    print("="*85)
    print("UBP GRAND UNIFIED EML-ALU v9.1: SOVEREIGN EDITION AUDIT (RESTORED)")
    print("="*85)

    print(f"[Constants]  Φ (Golden Ratio):   {alu.PHI.real:.12f}")
    print(f"[Constants]  Triadic Monad:      {alu.TRIADIC_MONAD.real:.12f}")

    v1, v2 = [1.0, 0.0, 0.0], [0.0, 1.0, 0.0]
    cross = alu.cross_product(v1, v2)
    print(f"\n[Vectors]    Cross {v1} × {v2} = {[c.real for c in cross]}")
    print(f"[Vectors]    ‖[3,4]‖ = {alu.magnitude([3.0, 4.0]).real:.1f}")

    print(f"\n[Analytic]   acos(0.5) = {alu.arccos(0.5).real:.12f} | π/3")
    print(f"[Analytic]   atan(1.0) = {alu.arctan(1.0).real:.12f} | π/4")
    print(f"[Analytic]   asin(0.5) = {alu.arcsin(0.5).real:.12f} | π/6")

    def f_x2(x): return alu.power(x, 2)
    print(f"\n[Calculus]   d/dx(x²)@3 = {alu.derivative(f_x2, 3.0).real:.12f} | 6.0")

    def f_x(x): return x
    print(f"[Calculus]   ∫₀² x dx = {alu.integrate(f_x, 0, 2).real:.12f} | 2.0")

    print(f"\n[Discrete]   5! = {alu.factorial(5).real:.12f} | 120.0")
    print(f"[Discrete]   Γ(½) = {alu.gamma(0.5).real:.12f} | √π ≈ 1.772453850906")

    signal = [1.0, 0.0, -1.0, 0.0]
    spectrum = alu.fft(signal)
    recovered = alu.ifft(spectrum)
    print(f"\n[Signal]     FFT/IFFT round-trip error: {max(abs(a-b) for a,b in zip(signal, recovered)):.2e}")

    x_val = _PI.real / 4
    def f_sin(x): return alu.sin(x)
    dual_result = f_sin(Dual(x_val, 1.0))
    print(f"[Dual AD]    d/dx sin(x)@π/4 = {dual_result.d.real:.12f} | cos(π/4) ≈ 0.707106781187")

    print("\n" + "-" * 85)
    print("PARTICLE PHYSICS PROJECTIONS (SOVEREIGN MONAD DERIVED)")
    print("-" * 85)

    monad = alu.TRIADIC_MONAD.real
    wobble = monad % 1.0
    L = wobble / 13.0
    sigma = 29.0 / 24.0
    L_s = L * sigma

    alpha_inv = 137.0 + L
    target_alpha = 137.035999
    err_alpha = abs(alpha_inv - target_alpha) / target_alpha * 100
    print(f"Alpha Inverse (1/a): {alpha_inv:.6f} | Target: {target_alpha:.6f} | Err: {err_alpha:.5f}%")

    proton_ratio = 1836.0 + (2.0 * L_s)
    target_proton = 1836.15267
    err_proton = abs(proton_ratio - target_proton) / target_proton * 100
    print(f"Proton/e- Ratio:     {proton_ratio:.6f} | Target: {target_proton:.6f} | Err: {err_proton:.5f}%")

    muon_ratio = 206.0 + (12.0 * L)
    target_muon = 206.76828
    err_muon = abs(muon_ratio - target_muon) / target_muon * 100
    print(f"Muon/e- Ratio:       {muon_ratio:.6f} | Target: {target_muon:.6f} | Err: {err_muon:.5f}%")

    print("="*85)

if __name__ == '__main__':
    run_grand_audit()
