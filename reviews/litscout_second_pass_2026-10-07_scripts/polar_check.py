import sympy as sp
exec(open('cross_check.py').read().split("# ---- conservation check")[0].replace('print(','(lambda *a,**k: None)('))
exec(open('cross_check.py').read().split("# ---- conservation check in the Lean convention ----")[1].split("print(\"stress conserved")[0].replace('print(','(lambda *a,**k: None)('))
# stress as a function of the six components
def stress_of(xv):
    Fv = sp.Matrix([[0, xv[0], xv[1], xv[2]],[-xv[0], 0, xv[3], xv[4]],[-xv[1], -xv[3], 0, xv[5]],[-xv[2], -xv[4], -xv[5], 0]])
    return sp.Matrix(4,4, lambda m,n: (Fv.row(m)*eta*Fv.row(n).T)[0,0] - eta[m,n]*sum(eta[k,k]*(Fv.row(k)*eta*Fv.row(k).T)[0,0] for k in range(4))/4)
xb = [x[i]+b[i] for i in range(6)]
polar = (stress_of(xb) - stress_of(x) - stress_of(b)).applyfunc(sp.expand)
for lam in (1, -1, sp.Rational(1,2), -sp.Rational(1,2), 2, -2):
    if (polar - lam*cross(b)).applyfunc(sp.expand) == sp.zeros(4,4):
        print(f"VERIFIED: stress(x+b) - stress(x) - stress(b) == {lam} * cross(b)(x)  (cross is the polarization of the Maxwell stress)")
        break
else:
    print("polarization does not match cross(b) with a scalar factor; polar[0,0] =", polar[0,0], " cross[0,0] =", cross(b)[0,0])
