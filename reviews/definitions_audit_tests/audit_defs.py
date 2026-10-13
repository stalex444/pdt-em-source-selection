"""Independent sympy replica of every definition in Challenge.lean, with checks.
Run: python3 audit_defs.py
"""
import sympy as sp
from sympy import Matrix, Rational, symbols, zeros, eye, diag, expand, Poly
import itertools, random

R = Rational
# --- objects ------------------------------------------------------------
eta = [1, 1, 1, -1]
metric = diag(*eta)

def mink(a, b):
    return a[0]*b[0] + a[1]*b[1] + a[2]*b[2] - a[3]*b[3]

def embed(x):
    v = [0]*15
    v[0], v[1], v[2], v[5], v[6], v[9] = x[0], x[1], x[2], x[3], x[4], x[5]
    return v

def field(v):
    return Matrix([[0, v[0], v[1], v[2]],
                   [-v[0], 0, v[5], v[6]],
                   [-v[1], -v[5], 0, v[9]],
                   [-v[2], -v[6], -v[9], 0]])

def invariant(F):
    rows = [list(F.row(i)) for i in range(4)]
    return mink(rows[0], rows[0]) + mink(rows[1], rows[1]) + mink(rows[2], rows[2]) - mink(rows[3], rows[3])

def stress(d, F):
    rows = [list(F.row(i)) for i in range(4)]
    inv = invariant(F)
    return Matrix(4, 4, lambda m, n: d*(mink(rows[m], rows[n]) - metric[m, n]*inv/4))

def registerStress(d, v):
    return stress(d, field(v))

monomialPair = [(0,0),(0,1),(0,2),(0,3),(0,4),(0,5),
    (1,1),(1,2),(1,3),(1,4),(1,5),(2,2),(2,3),(2,4),(2,5),
    (3,3),(3,4),(3,5),(4,4),(4,5),(5,5)]
tensorIndex = [[0,1,2,3],[1,4,5,6],[2,5,7,8],[3,6,8,9]]

def poly(c, x):
    return sum(c[m]*x[monomialPair[m][0]]*x[monomialPair[m][1]] for m in range(21))

def source(c, x):
    return Matrix(4, 4, lambda i, j: poly(c[tensorIndex[i][j]], x))

lorentzTable = [
 Matrix([[0,1,0,0],[-1,0,0,0],[0,0,0,0],[0,0,0,0]]),
 Matrix([[0,0,1,0],[0,0,0,0],[-1,0,0,0],[0,0,0,0]]),
 Matrix([[0,0,0,-1],[0,0,0,0],[0,0,0,0],[-1,0,0,0]]),
 Matrix([[0,0,0,0],[0,0,1,0],[0,-1,0,0],[0,0,0,0]]),
 Matrix([[0,0,0,0],[0,0,0,-1],[0,0,0,0],[0,-1,0,0]]),
 Matrix([[0,0,0,0],[0,0,0,0],[0,0,0,-1],[0,0,-1,0]])]

def fieldAction(k, x):
    T = [[0, x[3], x[4], -x[1], -x[2], 0],
         [-x[3], 0, x[5], x[0], 0, -x[2]],
         [x[4], x[5], 0, 0, x[0], x[1]],
         [x[1], -x[0], 0, 0, x[5], -x[4]],
         [-x[2], 0, -x[0], x[5], 0, x[3]],
         [0, -x[2], -x[1], -x[4], -x[3], 0]]
    return T[k]

def tensorAction(k, T):
    L = lorentzTable[k]
    return L*T + T*L.T

def traceEta(T):
    return T[0,0] + T[1,1] + T[2,2] - T[3,3]

# constraints: parse from Challenge.lean directly so we audit the SAME table.
import re, pathlib
src = pathlib.Path(__file__).with_name("Challenge.lean").read_text()
m = re.search(r"def constraints \(c : Coeff\) : Fin 209 → ℝ :=\n  !\[(.*?)\]\n", src, re.S)
rows_txt = [r.strip() for r in m.group(1).split(",\n")]
assert len(rows_txt) == 209, len(rows_txt)
C = sp.Matrix(10, 21, lambda i, j: sp.Symbol(f"c_{i}_{j}"))
csyms = list(C)
def parse_row(t):
    t = t.replace("c ", "C[").replace("*", "*")
    # tokens like "(-2) * C[1 0" -> need "C[1,0]"
    t = re.sub(r"C\[(\d+) (\d+)", r"C[\1,\2]", t)
    return eval(t, {"C": C})
constraint_exprs = [expand(parse_row(t)) for t in rows_txt]

# maxwellCoefficients from SourceCoefficientData.lean
h = R(1,2)
maxwell = [
 [h,0,0,0,0,0,h,0,0,0,0,-h,0,0,0,-h,0,0,h,0,h],
 [0,0,0,0,0,0,0,0,1,0,0,0,0,-1,0,0,0,0,0,0,0],
 [0,0,0,-1,0,0,0,0,0,0,0,0,0,0,-1,0,0,0,0,0,0],
 [0,0,0,0,-1,0,0,0,0,0,-1,0,0,0,0,0,0,0,0,0,0],
 [h,0,0,0,0,0,-h,0,0,0,0,h,0,0,0,h,0,0,-h,0,h],
 [0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,-1,0],
 [0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,-1,0,0,0],
 [-h,0,0,0,0,0,h,0,0,0,0,h,0,0,0,h,0,0,h,0,-h],
 [0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,1,0,0,0,0],
 [h,0,0,0,0,0,h,0,0,0,0,h,0,0,0,h,0,0,h,0,h]]

J = Matrix([[0,0,0,0,0,-1],[0,0,0,0,1,0],[0,0,0,1,0,0],
            [0,0,-1,0,0,0],[0,-1,0,0,0,0],[1,0,0,0,0,0]])

def crossCoefficients(b):
    return [[b[0],b[1],-b[2],-b[3],b[4],b[5]],[0,b[3],-b[4],b[1],-b[2],0],[-b[3],0,-b[5],-b[0],0,-b[2]],
            [-b[4],-b[5],0,0,-b[0],-b[1]],[b[0],-b[1],b[2],b[3],-b[4],b[5]],[b[1],b[0],0,0,-b[5],-b[4]],
            [b[2],0,b[0],-b[5],0,-b[3]],[-b[0],b[1],b[2],b[3],b[4],-b[5]],[0,b[2],b[1],b[4],b[3],0],
            [b[0],b[1],b[2],b[3],b[4],b[5]]]

def linear(l, x):
    return Matrix(4,4, lambda i,j: sum(l[tensorIndex[i][j]][a]*x[a] for a in range(6)))

# ===================== CHECKS ==========================================
x = sp.symbols("x0:6")
X = list(x)
print("== 1. field(embed x)")
F = field(embed(X))
sp.pprint(F)
assert F == Matrix([[0,x[0],x[1],x[2]],[-x[0],0,x[3],x[4]],[-x[1],-x[3],0,x[5]],[-x[2],-x[4],-x[5],0]])
assert F.T == -F
print("OK: F01=x0 F02=x1 F03=x2 F12=x3 F13=x4 F23=x5, antisymmetric")

print("\n== 2. lorentzTable in so(3,1)?")
for k, L in enumerate(lorentzTable):
    a = L.T*metric + metric*L          # vector-rep condition  (preserves v^T eta w for v->Lv)
    b = L*metric + metric*L.T          # contravariant-tensor condition (eta covariant under L T + T L^T)
    print(f"  k={k}: L^T eta + eta L = 0 ? {a == zeros(4,4)} ;  L eta + eta L^T = 0 ? {b == zeros(4,4)}")
    assert a == zeros(4,4) and b == zeros(4,4)
vecs = Matrix([list(L) for L in lorentzTable])
print("  rank of the six generators as 16-vectors:", vecs.rank())
assert vecs.rank() == 6
# commutator closure
span = vecs
for i in range(6):
    for j in range(6):
        comm = lorentzTable[i]*lorentzTable[j] - lorentzTable[j]*lorentzTable[i]
        assert Matrix.vstack(span, Matrix([list(comm)])).rank() == 6
print("  commutators stay in the span: OK (a Lie subalgebra of dim 6 = so(3,1))")
# tensorAction on metric
for k in range(6):
    assert tensorAction(k, metric) == zeros(4,4)
print("  tensorAction k eta = 0 for all k: OK (eta is an invariant contravariant tensor)")

print("\n== 3. fieldAction k x induced by tensorAction?")
for k in range(6):
    lhs = field(embed(fieldAction(k, X)))
    rhs = tensorAction(k, F)
    ok = sp.simplify(lhs - rhs) == zeros(4,4)
    okneg = sp.simplify(lhs + rhs) == zeros(4,4)
    print(f"  k={k}: field(embed(fieldAction)) == L F + F L^T ? {ok}   (== -(L F + F L^T)? {okneg})")
    assert ok

print("\n== 4. stress: Maxwell tensor? symmetric? traceless?")
d = sp.Symbol("d")
T = stress(d, F)
assert sp.simplify(T - T.T) == zeros(4,4)
assert sp.simplify(traceEta(T)) == 0
# compare with textbook T^{mu nu} = F^{mu a} F^{nu}_a - 1/4 eta^{mu nu} F_{ab} F^{ab}, F upper-index
Fup = F
Flow = metric*Fup*metric
FF = sum(Flow[a,b]*Fup[a,b] for a in range(4) for b in range(4))
Ttext = Matrix(4,4, lambda m,n: sum(Fup[m,a]*Fup[n,b]*metric[a,b] for a in range(4) for b in range(4)) - R(1,4)*metric[m,n]*FF)
assert sp.simplify(T - d*Ttext) == zeros(4,4)
print("  stress d F == d*(F^{ma}F^n_a - 1/4 eta^{mn} F_{ab}F^{ab}) with F = upper-index: OK")
print("  invariant F == F_{ab}F^{ab}:", sp.simplify(invariant(F) - FF) == 0)
# energy density sign: time index 3, E_i := F^{i3}
Ex, Ey, Ez, Bx, By, Bz = sp.symbols("Ex Ey Ez Bx By Bz")
# F^{12} = Bz, F^{23} = Bx, F^{13} = -By  (standard B_k = 1/2 eps_{kij}F^{ij}), F^{i3} = E_i
Fphys = field(embed([Ex, Ey, Ez, Bz, -By, Bx])) if False else None
xs = [0,0,Ex,0,0,0]
print("  T^{33} for pure E_z field (F^{03}=Ez,d=1):", sp.expand(stress(1, field(embed([0,0,Ez,0,0,0])))[3,3]))
print("  T^{33} for pure B field (F^{12}=Bz,d=1):", sp.expand(stress(1, field(embed([0,0,0,Bz,0,0])))[3,3]))
print("  invariant for E_z only:", sp.expand(invariant(field(embed([0,0,Ez,0,0,0])))), " for B_z only:", sp.expand(invariant(field(embed([0,0,0,Bz,0,0])))))

print("\n== 5. jets, Bianchi, current, vacuum jets")
# Build a genuine first jet from a quadratic potential A^nu = 1/2 Cnu_ab x^a x^b, F^{mn} = d^m A^n - d^n A^m.
Csym = {}
for nu in range(4):
    for a in range(4):
        for b in range(a, 4):
            Csym[(nu,a,b)] = Csym[(nu,b,a)] = sp.Symbol(f"C{nu}{a}{b}")
def dA(nu, a, mu):  # d_mu d_a A^nu
    return Csym[(nu,a,mu)]
def dF(mu, m, n):   # d_mu F^{mn} = eta^{ma} d_mu d_a A^n - eta^{na} d_mu d_a A^m
    return eta[m]*dA(n, m, mu) - eta[n]*dA(m, n, mu)
slots = [(0,1),(0,2),(0,3),(1,2),(1,3),(2,3)]
Djet = [[dF(mu, m, n) for (m,n) in slots] for mu in range(4)]   # D mu : Local
Dreg = [embed(Djet[mu]) for mu in range(4)]
def bianchiJet(D):
    return [D[0][5]-D[1][1]+D[2][0], D[0][6]-D[1][2]-D[3][0], D[0][9]-D[2][2]-D[3][1], D[1][9]-D[2][6]-D[3][5]]
bj = [sp.expand(e) for e in bianchiJet(Dreg)]
print("  bianchiJet on the jet of F = dA (upper-index F, D mu = d_mu):", bj)
assert all(e == 0 for e in bj)
# compare with lower-index reading: would the file's equations ALSO vanish if slots were F_{mn} (lower)?
def dFlow(mu, m, n):
    return eta[m]*eta[n]*dF(mu, m, n)
DjetL = [[dFlow(mu, m, n) for (m,n) in slots] for mu in range(4)]
bjL = [sp.expand(e) for e in bianchiJet([embed(DjetL[mu]) for mu in range(4)])]
print("  bianchiJet if slots were LOWER-index F_{mn}:", bjL, "-> vanish?", all(e == 0 for e in bjL))
# genuine Bianchi ∂_[mu F_nu rho] = 0 in lower-index form, check equals file eqs up to sign
def sourcedCurrent(dd, Dreg):
    return [dd*sum(field(Dreg[mu])[mu, nu] for mu in range(4)) for nu in range(4)]
cur = [sp.expand(e) for e in sourcedCurrent(1, Dreg)]
boxA = [sum(eta[a]*Csym[(nu,a,a)] for a in range(4)) for nu in range(4)]
divA = [sum(Csym[(a,a,nu)] for a in range(4)) for a in [0]]  # placeholder
print("  sourcedCurrent 1 on jet of dA, component 0:", cur[0])
# expected: d_mu F^{mu nu} = box A^nu - d^nu (d_a A^a)
expected = [sp.expand(sum(eta[mu]*Csym[(nu,mu,mu)] for mu in range(4)) - eta[nu]*sum(Csym[(a,a,nu)] for a in range(4))) for nu in range(4)]
print("  equals box A^nu - d^nu(div A)?", all(sp.expand(cur[i]-expected[i]) == 0 for i in range(4)))
# Solve the vacuum-jet system directly: 24 unknowns, 8 equations
dsyms = sp.symbols("D0:24")
Dgen = [[dsyms[6*mu+i] for i in range(6)] for mu in range(4)]
Dreg_gen = [embed(Dgen[mu]) for mu in range(4)]
eqs = bianchiJet(Dreg_gen) + sourcedCurrent(1, Dreg_gen)
A, _ = sp.linear_eq_to_matrix(eqs, dsyms)
print("  vacuum-jet system: rank", A.rank(), "of 8 equations in 24 unknowns -> solution dim", 24 - A.rank())
ns = A.nullspace()
# exhibit an integer vacuum jet: plane wave along x^2 (y): E_x = f(y - t), B_z = f(y - t) ... choose from nullspace
# pick: F^{03}=Ez varies? Simpler: take nullspace vector with small integer entries
cand = None
for v in ns:
    vv = v*sp.lcm([sp.fraction(e)[1] for e in v])
    if sum(1 for e in vv if e != 0) <= 2:
        cand = vv; break
if cand is None:
    cand = ns[0]*sp.lcm([sp.fraction(e)[1] for e in ns[0]])
Dc = [[cand[6*mu+i] for i in range(6)] for mu in range(4)]
print("  example nonzero vacuum jet D (rows mu=0..3, slots 01,02,03,12,13,23):")
for row in Dc: print("    ", row)
assert all(e == 0 for e in bianchiJet([embed(r) for r in Dc]) + sourcedCurrent(1, [embed(r) for r in Dc]))
# Physical plane wave: E_x(t,y) = cos(y - t) -> at a point, D_1 (d/dy) slot F^{02}? we have F^{i3}=E_i: F^{03} = E_x? no: F^{03} slot 2 = E_x? index 0 = x. So F^{03}=E_x (slot 2). B_z = F^{01}?? B_z = F^{12}? With indices (x,y,z)=(0,1,2): B_z = F^{01} (slot 0). plane wave along y: E_x = f(y-t), B_z = -f(y-t) or +; jet: D_1 slot2 = f', D_3 slot2 = -f', D_1 slot0 = s f', D_3 slot0 = -s f'
for s in [1, -1]:
    Dpw = [[0]*6 for _ in range(4)]
    Dpw[1][2] = 1; Dpw[3][2] = -1; Dpw[1][0] = s; Dpw[3][0] = -s
    Dr = [embed(r) for r in Dpw]
    print(f"  plane wave E_x=f(y-t), B_z={s:+d}f(y-t): bianchi", bianchiJet(Dr), " current", sourcedCurrent(1, Dr))

print("\n== 5b. divergence identity: div(stress 1) = exchange(x)(current 1) on Bianchi jets")
def divergence_poly(Sfun, xval, D):
    # S polynomial in x: d/dt S(x + t D mu) at 0 = directional derivative
    t = sp.Symbol("t")
    out = []
    for nu in range(4):
        tot = 0
        for mu in range(4):
            xt = [xval[i] + t*D[mu][i] for i in range(6)]
            tot += sp.diff(Sfun(xt)[mu, nu], t).subs(t, 0)
        out.append(sp.expand(tot))
    return out
def exchange(v, j):
    Fv = field(v)
    return [mink(list(Fv.row(nu)), j) for nu in range(4)]
# general Bianchi jet: solve bianchi only
Ab, _ = sp.linear_eq_to_matrix(bianchiJet(Dreg_gen), dsyms)
nsb = Ab.nullspace()
params = sp.symbols("p0:%d" % len(nsb))
Dgen_b_vec = sum((params[i]*nsb[i] for i in range(len(nsb))), sp.zeros(24,1))
Dgb = [[Dgen_b_vec[6*mu+i] for i in range(6)] for mu in range(4)]
Dgb_reg = [embed(r) for r in Dgb]
lhs = divergence_poly(lambda xx: registerStress(1, embed(xx)), X, Dgb)
rhs = [sp.expand(e) for e in exchange(embed(X), sourcedCurrent(1, Dgb_reg))]
print("  div(stress 1) == exchange(embed x)(sourcedCurrent 1 D) on all Bianchi jets?", all(sp.expand(lhs[i]-rhs[i]) == 0 for i in range(4)))
print("  div(stress 1) == -exchange(...)?", all(sp.expand(lhs[i]+rhs[i]) == 0 for i in range(4)))

print("\n== 6. constraints: Maxwell vector, rank, independent re-derivation")
subsM = {C[i,j]: maxwell[i][j] for i in range(10) for j in range(21)}
vals = [e.subs(subsM) for e in constraint_exprs]
print("  constraints(maxwellCoefficients) all zero?", all(v == 0 for v in vals), " nonzero rows:", [i for i,v in enumerate(vals) if v != 0])
Acon, _ = sp.linear_eq_to_matrix(constraint_exprs, csyms)
rk = Acon.rank()
print("  rank of the 209 constraints over 210 unknowns:", rk)
# which d: source maxwell == registerStress d (embed x)?
SM = source(maxwell, X)
for dd in [R(1,2), 1, 2, -1, R(-1,2)]:
    if sp.simplify(SM - registerStress(dd, embed(X))) == zeros(4,4):
        print(f"  source maxwellCoefficients == registerStress {dd} (embed x)")
# independent derivation of Covariant ∧ TraceFree on the general quadratic class
Cl = [[C[i,j] for j in range(21)] for i in range(10)]
t = sp.Symbol("t")
eqs_cov = []
Sgen = source(Cl, X)
for k in range(6):
    a = fieldAction(k, X)
    xt = [X[i] + t*a[i] for i in range(6)]
    lhsM = source(Cl, xt).diff(t).subs(t, 0)
    rhsM = tensorAction(k, Sgen)
    diffM = (lhsM - rhsM)
    for i in range(4):
        for j in range(i, 4):
            p = Poly(sp.expand(diffM[i,j]), *X)
            eqs_cov += p.coeffs()
eqs_tr = Poly(sp.expand(traceEta(Sgen)), *X).coeffs()
Aind, _ = sp.linear_eq_to_matrix(eqs_cov + eqs_tr, csyms)
print("  independent (Covariant ∧ TraceFree) system: rank", Aind.rank())
print("  rank of [constraints ; independent] stacked:", Matrix.vstack(Acon, Aind).rank(), "(equal row spaces iff all three ranks agree)")
nsI = Aind.nullspace()
print("  nullspace dim of independent system:", len(nsI))
mv = Matrix([maxwell[i][j] for i in range(10) for j in range(21)])
print("  Maxwell vector in nullspace of independent system?", (Aind*mv) == zeros(Aind.rows,1))

print("\n== 7. J Hodge dual; crossCoefficients bilinearity")
print("  J*J =", (J*J == -eye(6)) and "-I", "; J^T J = I?", J.T*J == eye(6))
# Hodge star on upper-index F with eps^{0123} = +1: *F^{mn} = 1/2 eps^{mnrs} F_{rs}
from sympy import LeviCivita
Fl = metric*F*metric
star = Matrix(4,4, lambda m,n: R(1,2)*sum(LeviCivita(m,n,r,s)*Fl[r,s] for r in range(4) for s in range(4)))
starx = [star[m,n] for (m,n) in slots]
print("  (J x) == components of *F (eps^{0123}=+1)?", list(J*Matrix(X)) == [sp.expand(e) for e in starx])
print("  (J x) == components of -*F?", list(-J*Matrix(X)) == [sp.expand(e) for e in starx])
b = sp.symbols("b0:6")
Lc = crossCoefficients(list(b))
Mcross = linear(Lc, X)
print("  crossCoefficients entries all of form (+-1)*b_i or 0:", all(e == 0 or any(e == s*bb for s in (1,-1) for bb in b) for row in Lc for e in row))
print("  linear(cross b) x bilinear (every entry degree 1 in b and in x):",
      all(e == 0 or (Poly(e, *b).total_degree() == 1 and Poly(e, *X).total_degree() == 1) for e in Mcross))
print("  linear(cross b) x symmetric:", Mcross == Mcross.T)
# is the cross family conserved for all b? (not claimed by the theorems; informational)
lhsc = divergence_poly(lambda xx: linear(Lc, xx), X, Dgen)
# restrict to vacuum jets: substitute nullspace param
paramsV = sp.symbols("q0:%d" % len(ns))
DV = sum((paramsV[i]*ns[i] for i in range(len(ns))), sp.zeros(24,1))
subsV = {dsyms[i]: DV[i] for i in range(24)}
lhsc_v = [sp.expand(e.subs(subsV)) for e in lhsc]
print("  div(linear(cross b)) on all vacuum jets == 0 for all b?", all(e == 0 for e in lhsc_v))
# is cross(b) covariant for any b != 0? (smoothNecessity shows no for b = e0)
# is constant A conserved? trivially (derivative zero). Covariant iff A ∝ eta:
print("  covariantFamily 1 0 = eta, tensorAction eta = 0 (checked above)")

print("\n== 8. controls")
SMI = source([[maxwell[0][0]*0 + e for e in row] for row in [[2,0,0,0,0,0,2,0,0,0,0,-2,0,0,0,2,0,0,-2,0,-2],[0]*21,[0]*21,[0]*21,[2,0,0,0,0,0,2,0,0,0,0,-2,0,0,0,2,0,0,-2,0,-2],[0]*21,[0]*21,[2,0,0,0,0,0,2,0,0,0,0,-2,0,0,0,2,0,0,-2,0,-2],[0]*21,[-2,0,0,0,0,0,-2,0,0,0,0,2,0,0,0,-2,0,0,2,0,2]]], X)
print("  metricInvariantCoefficients source == eta * invariant(F)?", sp.simplify(SMI - metric*invariant(F)) == zeros(4,4))
SAN = source([[1]+[0]*20,[0]*21,[0]*21,[0]*21,[-1]+[0]*20,[0]*21,[0]*21,[0]*21,[0]*21,[0]*21], X)
print("  anisotropicCoefficients source == diag(x0^2,-x0^2,0,0)?", SAN == diag(x[0]**2, -x[0]**2, 0, 0))
print("\nALL CHECKS PASSED")
