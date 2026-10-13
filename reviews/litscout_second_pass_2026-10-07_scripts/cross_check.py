import sympy as sp
from itertools import permutations
x = sp.symbols('x0:6')
eta = sp.diag(1,1,1,-1)
# lower-index field tensor in the Challenge.lean convention
F = sp.Matrix([[0, x[0], x[1], x[2]],
               [-x[0], 0, x[3], x[4]],
               [-x[1], -x[3], 0, x[5]],
               [-x[2], -x[4], -x[5], 0]])
# Levi-Civita
def eps(i,j,k,l):
    p=[i,j,k,l]
    if len(set(p))<4: return 0
    from sympy.combinatorics import Permutation; return Permutation(p).signature()
Fup = eta*F*eta   # F^{mu nu}
Fdual = sp.zeros(4,4)  # *F_{mu nu} = 1/2 eps_{mu nu a b} F^{ab}
for m in range(4):
    for n in range(4):
        Fdual[m,n] = sp.Rational(1,2)*sum(eps(m,n,a,b)*Fup[a,b] for a in range(4) for b in range(4))
# ---- Lean cross family ----
b = sp.symbols('b0:6')
cc = [[b[0], b[1], -b[2], -b[3], b[4], b[5]],
      [0, b[3], -b[4], b[1], -b[2], 0],
      [-b[3], 0, -b[5], -b[0], 0, -b[2]],
      [-b[4], -b[5], 0, 0, -b[0], -b[1]],
      [b[0], -b[1], b[2], b[3], -b[4], b[5]],
      [b[1], b[0], 0, 0, -b[5], -b[4]],
      [b[2], 0, b[0], -b[5], 0, -b[3]],
      [-b[0], b[1], b[2], b[3], b[4], -b[5]],
      [0, b[2], b[1], b[4], b[3], 0],
      [b[0], b[1], b[2], b[3], b[4], b[5]]]
tensorIndex = [[0,1,2,3],[1,4,5,6],[2,5,7,8],[3,6,8,9]]
def cross(bv):
    sub = dict(zip(b,bv))
    return sp.Matrix(4,4,lambda i,j: sum(sp.sympify(cc[tensorIndex[i][j]][a]).subs(sub)*x[a] for a in range(6)))
basis_lean = [cross([1 if k==i else 0 for k in range(6)]) for i in range(6)]
# symmetric? (by construction via tensorIndex)
# coordinate vector of a matrix-valued linear form in x: 16*6 coefficients
def vec(M):
    return sp.Matrix([sp.Poly(sp.expand(M[i,j]), *x).coeff_monomial(x[a]) for i in range(4) for j in range(4) for a in range(6)])
VL = sp.Matrix.hstack(*[vec(M) for M in basis_lean])
print("Lean cross family: rank of 6 generators =", VL.rank())
# ---- Anco-Pohjanpelto symmetric assembly ----
A = sp.Matrix(4,4, sp.symbols('a0:16'))
B = sp.Matrix(4,4, sp.symbols('c0:16'))
L = F*A + Fdual*B           # column nu of L is the elementary current F_{mu alpha} a^alpha_nu + *F_{mu alpha} b^alpha_nu (eta absorbed into A,B)
sym_eqs = []
for i in range(4):
    for j in range(i+1,4):
        e = sp.expand(L[i,j]-L[j,i])
        sym_eqs += [e.coeff(x[a]) for a in range(6)]
sol = sp.linsolve(sym_eqs, list(A)+list(B))
sol = list(sol)[0]
free = sorted({s for e in sol for s in e.free_symbols}, key=str)
print("A-P symmetric assembly: free parameters in (A,B) after symmetry =", len(free))
Lsym = L.subs(dict(zip(list(A)+list(B), sol)))
basis_ap = []
for f in free:
    basis_ap.append(Lsym.subs({g:(1 if g==f else 0) for g in free}))
VA = sp.Matrix.hstack(*[vec(M) for M in basis_ap])
print("A-P family: rank =", VA.rank())
print("joint rank (span equality iff joint rank == both ranks):", sp.Matrix.hstack(VL,VA).rank())
# which (A,B) give the Lean generators? solve L == cross(e_k)
for k in range(6):
    eqs=[]
    D = sp.expand(L - basis_lean[k])
    for i in range(4):
        for j in range(4):
            eqs += [D[i,j].coeff(x[a]) for a in range(6)]
    s = sp.linsolve(eqs, list(A)+list(B))
    s = list(s)
    print(f"cross(e_{k}):", "no (A,B) solution" if not s else "solvable; one solution A,B =", (sp.Matrix(4,4,s[0][:16]).subs({v:0 for v in free+list(A)+list(B)}), sp.Matrix(4,4,s[0][16:]).subs({v:0 for v in free+list(A)+list(B)})) if s else "")
# ---- conservation check in the Lean convention ----
D = sp.Matrix(4,6, sp.symbols('d0:24'))   # D[mu][a] = ∂^mu x_a
# register slots: embed x -> slots 0,1,2,5,6,9 = x0..x5
def reg(row): return {0:row[0],1:row[1],2:row[2],5:row[3],6:row[4],9:row[5]}
R = [reg(D.row(m)) for m in range(4)]
bianchi = [R[0][5]-R[1][1]+R[2][0], R[0][6]-R[1][2]-R[3][0], R[0][9]-R[2][2]-R[3][1], R[1][9]-R[2][6]-R[3][5]]
def fieldReg(r):
    return sp.Matrix([[0,r[0],r[1],r[2]],[-r[0],0,r[5],r[6]],[-r[1],-r[5],0,r[9]],[-r[2],-r[6],-r[9],0]])
maxwell = [sum(fieldReg(R[m])[m,n] for m in range(4)) for n in range(4)]
constraints = bianchi+maxwell
# solve constraints for 8 of the 24 jet variables
csol = list(sp.linsolve(constraints, list(D)))[0]
csub = dict(zip(list(D), csol))
def divergence(S):  # S matrix-valued function of x
    out=[]
    for n in range(4):
        tot=0
        for m in range(4):
            tot += sum(sp.diff(S[m,n], x[a])*D[m,a] for a in range(6))
        out.append(sp.expand(tot.subs(csub)))
    return out
stress = sp.Matrix(4,4, lambda m,n: (F.row(m)*eta*F.row(n).T)[0,0] - eta[m,n]*sum(eta[k,k]*(F.row(k)*eta*F.row(k).T)[0,0] for k in range(4))/4)
print("stress conserved on vacuum jets:", all(e==0 for e in divergence(stress)))
print("cross(b) conserved on vacuum jets for symbolic b:", all(e==0 for e in divergence(cross(b))))
# all symmetric linear sources (60-dim): which are conserved?
lin = sp.Matrix(4,4, lambda i,j: sum(sp.Symbol(f'l{tensorIndex[i][j]}_{a}')*x[a] for a in range(6)))
divs = divergence(lin)
eqs=[]
for e in divs:
    P = sp.Poly(e, *list(D)+list(x))
    eqs += P.coeffs()
ls = sp.linsolve(eqs, sorted(lin.free_symbols - set(x), key=str))
ls = list(ls)[0]
frees = {s for e in ls for s in e.free_symbols}
print("dimension of all conserved symmetric linear sources (Lean convention) =", len(frees))
# trace of the cross family
print("eta-trace of cross(b):", sp.expand(sum(eta[k,k]*cross(b)[k,k] for k in range(4))))
# Hodge map J from Challenge.lean
J = sp.Matrix([[0,0,0,0,0,-1],[0,0,0,0,1,0],[0,0,0,1,0,0],[0,0,-1,0,0,0],[0,-1,0,0,0,0],[1,0,0,0,0,0]])
Jx = J*sp.Matrix(x)
print("stress Hodge-invariant S(Jx)=S(x):", sp.simplify(stress.xreplace(dict(zip(x,Jx))) - stress) == sp.zeros(4,4))
print("cross(b)(Jx) - cross(b)(x) == 0 ?", sp.expand(cross(b).xreplace(dict(zip(x,Jx))) - cross(b)) == sp.zeros(4,4))
print("---- Hodge debug ----")
diff = (stress.xreplace(dict(zip(x,Jx))) - stress).applyfunc(sp.expand)
print("stress(Jx)-stress(x) entries all zero:", diff == sp.zeros(4,4)); print(diff)
# A-P duality action on the linear family: F a + *F b -> *F a - F b ; check the Lean cross family is closed under J (as a space)
VJ = sp.Matrix.hstack(*[vec(M.xreplace(dict(zip(x,Jx))).applyfunc(sp.expand)) for M in basis_lean])
print("rank of [cross basis | J-pulled-back cross basis] =", sp.Matrix.hstack(VL,VJ).rank(), "(6 means the family is J-stable as a space)")
# explicit linear map: which b' gives cross(b)(Jx) = cross(b')(x)?
bp = sp.symbols('p0:6')
E = (cross(b).xreplace(dict(zip(x,Jx))) - cross(bp)).applyfunc(sp.expand)
eqs=[E[i,j].coeff(x[a]) for i in range(4) for j in range(4) for a in range(6)]
print("b' in terms of b:", sp.linsolve(eqs, list(bp)))
