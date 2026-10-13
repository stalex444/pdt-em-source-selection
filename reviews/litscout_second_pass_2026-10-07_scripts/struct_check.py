import sympy as sp
from sympy.combinatorics import Permutation
exec(open('cross_check.py').read().split("# ---- conservation check")[0].replace('print(','(lambda *a,**k: None)('))
# general symmetric solution in terms of free params; lower the first index: a_{alpha nu} = eta_{alpha alpha} A_{alpha nu}
Agen = sp.Matrix(4,4, sol[:16]); Bgen = sp.Matrix(4,4, sol[16:])
a_low = eta*Agen; b_low = eta*Bgen
print("a_low antisymmetric for all solutions:", sp.simplify(a_low + a_low.T) == sp.zeros(4,4))
print("b_low antisymmetric for all solutions:", sp.simplify(b_low + b_low.T) == sp.zeros(4,4))
# dual of a_low as a 2-form: (*a)_{mu nu} = 1/2 eps_{mu nu rs} a^{rs}, a^{rs} = eta a_low eta
a_up = eta*a_low*eta
dual_a = sp.Matrix(4,4, lambda m,n: sp.Rational(1,2)*sum(eps(m,n,r,s)*a_up[r,s] for r in range(4) for s in range(4)))
for sgn in (1,-1):
    print(f"b_low == {sgn:+d} * (*a_low):", sp.simplify(b_low - sgn*dual_a) == sp.zeros(4,4))
print("free parameters:", free)
print("a_low =", a_low)
print("b_low =", b_low)
# Lean b <-> bivector a: solve cross(b) == F*A + Fdual*B for b in terms of free params
bb = sp.symbols('q0:6')
E = (cross(bb) - Lsym).applyfunc(sp.expand)
eqs=[E[i,j].coeff(x[a]) for i in range(4) for j in range(4) for a in range(6)]
print("Lean b in terms of A-P free params:", sp.linsolve(eqs, list(bb)))
