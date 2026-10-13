"""
Blind re-derivation: symmetric tensor-valued functions S(F) of the Maxwell field
strength on flat R^4 with eta = diag(1,1,1,-1).

CONVENTIONS (fixed here, stated in the report):
  * Index 3 is time; eta = diag(1,1,1,-1); eta^{-1} = eta.
  * F is CONTRAVARIANT: F^{mu nu}, antisymmetric, components
        f01,f02,f03,f12,f13,f23  (F^{01}=f01, etc.)
  * S is CONTRAVARIANT symmetric S^{mu nu}.
  * so(3,1) generators: L^mu_nu with  L^T eta + eta L = 0, i.e. L = eta^{-1} w, w antisymmetric.
    Action on contravariant tensors:  dF = L F + F L^T,  dS = L S + S L^T.
    Covariance:  DS(F)[L F + F L^T] = L S(F) + S(F) L^T   for all 6 generators.
  * eta-trace:  tr_eta S = eta_{mu nu} S^{mu nu}.
  * Jets: J[mu][a] = d_mu F^a  (24 symbols).  Lowering: F_{mu nu} = eta_mu eta_nu F^{mu nu}.
  * Levi-Civita: eps^{0123} = +1 (contravariant).  *F^{mu nu} = 1/2 eps^{mu nu rho sigma} F_{rho sigma}.
  * Bianchi: d_mu *F^{mu nu} = 0 (equivalent to d_[mu F_nu rho] = 0).  Maxwell: d_mu F^{mu nu} = 0.
  * Divergence: (div S)^nu = sum_mu d_mu S^{mu nu}.
"""
import sympy as sp
from sympy import Matrix, symbols, Rational, eye, zeros, diag
from itertools import permutations, combinations

eta = diag(1, 1, 1, -1)
etad = [1, 1, 1, -1]
pairs = [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]
fs = symbols('f01 f02 f03 f12 f13 f23')
Fup = zeros(4, 4)
for (i, j), f in zip(pairs, fs):
    Fup[i, j] = f
    Fup[j, i] = -f
Fdn = eta * Fup * eta   # F_{mu nu}

def levi(a, b, c, d):
    return sp.LeviCivita(a, b, c, d)

# dual *F^{mu nu} = 1/2 eps^{mu nu rho sigma} F_{rho sigma}
Fdual = zeros(4, 4)
for m in range(4):
    for n in range(4):
        Fdual[m, n] = Rational(1, 2) * sum(levi(m, n, r, s) * Fdn[r, s] for r in range(4) for s in range(4))

# quadratic monomials
monos2 = [fs[i] * fs[j] for i in range(6) for j in range(i, 6)]
monos1 = list(fs)
monos0 = [sp.Integer(1)]
sympairs = [(i, j) for i in range(4) for j in range(i, 4)]  # 10 symmetric slots

def general_S(degrees, prefix='c'):
    """Return (S matrix, list of coefficient symbols)."""
    monos = []
    if 0 in degrees: monos += monos0
    if 1 in degrees: monos += monos1
    if 2 in degrees: monos += monos2
    coeffs = []
    S = zeros(4, 4)
    for k, (i, j) in enumerate(sympairs):
        expr = 0
        for m, mono in enumerate(monos):
            c = sp.Symbol(f'{prefix}_{i}{j}_{m}')
            coeffs.append(c)
            expr += c * mono
        S[i, j] = expr
        S[j, i] = expr
    return S, coeffs

# so(3,1) generators: L = eta^{-1} w, w antisymmetric basis
gens = []
for (a, b) in pairs:
    w = zeros(4, 4); w[a, b] = 1; w[b, a] = -1
    gens.append(eta.inv() * w)
# sanity: L^T eta + eta L = 0
for L in gens:
    assert (L.T * eta + eta * L) == zeros(4, 4)

def components(M):
    return [M[i, j] for (i, j) in pairs]

def directional_derivative(S, dF):
    """D S(F)[dF] where dF is an antisymmetric matrix of variations."""
    dfc = components(dF)
    out = zeros(4, 4)
    for i in range(4):
        for j in range(4):
            out[i, j] = sum(sp.diff(S[i, j], fs[k]) * dfc[k] for k in range(6))
    return out

def linear_system(exprs, unknowns):
    """Collect polynomial coefficients in all non-unknown symbols -> linear equations."""
    eqs = []
    for e in exprs:
        e = sp.expand(e)
        if e == 0:
            continue
        others = sorted(e.free_symbols - set(unknowns) - {sp.Symbol('k')}, key=str)
        if others:
            P = sp.Poly(e, *others)
            eqs += [c for c in P.coeffs()]
        else:
            eqs.append(e)
    return eqs

def solve_space(eqs, unknowns):
    """Return (dimension, basis of solutions as list of dicts unknown->value)."""
    if not eqs:
        A = zeros(0, len(unknowns))
    else:
        A, _ = sp.linear_eq_to_matrix(eqs, unknowns)
    ns = A.nullspace()
    return len(ns), ns

def S_from_vec(vec, S, coeffs):
    sub = {c: v for c, v in zip(coeffs, vec)}
    return S.subs(sub)

def tr_eta(S):
    return sp.expand(sum(eta[m, n] * S[m, n] for m in range(4) for n in range(4)))

# ---------- candidate named tensors ----------
FF = sp.expand(sum(Fup[m, n] * Fdn[m, n] for m in range(4) for n in range(4)))        # F^{mn}F_{mn}
FFd = sp.expand(sum(Fup[m, n] * (eta * Fdual * eta)[m, n] for m in range(4) for n in range(4)))  # F^{mn} *F_{mn}
# F^{mu rho} F^{nu}_rho = (F eta F^T)^{mu nu}
FFT = Fup * eta * Fup.T
T_maxwell = sp.simplify(FFT - Rational(1, 4) * eta.inv() * FF)   # eta^{mu nu} = (eta^{-1})
etaFF = eta.inv() * FF
etaFFd = eta.inv() * FFd
FdFdT = Fdual * eta * Fdual.T
FFdT = Fup * eta * Fdual.T

print("F.F  =", FF)
print("F.*F =", FFd)
print("F *F^T - 1/4 eta (F.*F) == 0 ?", sp.simplify(FFdT - Rational(1,4)*eta.inv()*FFd) == zeros(4,4))
print("*F*F^T  vs F F^T - 1/2 eta F.F == 0 ?", sp.simplify(FdFdT - (FFT - Rational(1,2)*eta.inv()*FF)) == zeros(4,4))
print("tr_eta T_maxwell =", tr_eta(T_maxwell))

def coords_in_basis(target, basis_mats):
    """Express symmetric matrix target as combination of basis_mats (polynomial identity). Return coeffs or None."""
    a = symbols(f'a0:{len(basis_mats)}')
    E = target - sum((ai * B for ai, B in zip(a, basis_mats)), zeros(4, 4))
    eqs = linear_system([E[i, j] for (i, j) in sympairs], a)
    sol = sp.solve(eqs, a, dict=True)
    return sol[0] if sol else None

# ================= (a) covariance and trace =================
print("\n=========== (a) quadratic S: covariance and trace ===========")
S2, c2 = general_S([2], 'q')
print("number of free quadratic coefficients:", len(c2))
cov_eqs = []
for L in gens:
    dF = L * Fup + Fup * L.T
    lhs = directional_derivative(S2, dF)
    rhs = L * S2 + S2 * L.T
    cov_eqs += linear_system([lhs[i, j] - rhs[i, j] for i in range(4) for j in range(4)], c2)
dim_cov, ns_cov = solve_space(cov_eqs, c2)
print("dim covariant quadratic S:", dim_cov)
cov_basis = [S_from_vec(v, S2, c2) for v in ns_cov]
for k, B in enumerate(cov_basis):
    print(f"  cov basis[{k}] in terms of (T_maxwell, eta F.F, eta F.*F):",
          coords_in_basis(B, [T_maxwell, etaFF, etaFFd]))
# conversely, are named tensors in the covariant space?
for name, M in [("T_maxwell", T_maxwell), ("eta F.F", etaFF), ("eta F.*F", etaFFd), ("F F^T", FFT), ("*F *F^T", FdFdT)]:
    print(f"  {name} in covariant space:", coords_in_basis(M, cov_basis) is not None)

tr_eqs = linear_system([tr_eta(S2)], c2)
dim_tr, ns_tr = solve_space(tr_eqs, c2)
print("dim traceless quadratic S:", dim_tr, "(expected 210 - 21 = 189)")

dim_both, ns_both = solve_space(cov_eqs + tr_eqs, c2)
print("dim covariant AND traceless:", dim_both)
both_basis = [S_from_vec(v, S2, c2) for v in ns_both]
for k, B in enumerate(both_basis):
    print(f"  cov+traceless basis[{k}] =", coords_in_basis(B, [T_maxwell, etaFF, etaFFd]))

# ================= jets and constraints =================
J = [[sp.Symbol(f'J{m}_{a}') for a in range(6)] for m in range(4)]   # J[m][a] = d_m F^a
Jsyms = [J[m][a] for m in range(4) for a in range(6)]
def dF_matrix(m):
    M = zeros(4, 4)
    for (i, j), a in zip(pairs, range(6)):
        M[i, j] = J[m][a]; M[j, i] = -J[m][a]
    return M
dFup = [dF_matrix(m) for m in range(4)]
dFdn = [eta * M * eta for M in dFup]
dFdual = []
for m in range(4):
    D = zeros(4, 4)
    for a in range(4):
        for b in range(4):
            D[a, b] = Rational(1, 2) * sum(levi(a, b, r, s) * dFdn[m][r, s] for r in range(4) for s in range(4))
    dFdual.append(D)
maxwell_c = [sum(dFup[m][m, n] for m in range(4)) for n in range(4)]     # d_mu F^{mu nu}
bianchi_c = [sum(dFdual[m][m, n] for m in range(4)) for n in range(4)]   # d_mu *F^{mu nu}
# check Bianchi equivalence with d_[a F_bc] = 0
bianchi_alt = [sp.expand(dFdn[a][b, c] + dFdn[b][c, a] + dFdn[c][a, b]) for (a, b, c) in combinations(range(4), 3)]
A1, _ = sp.linear_eq_to_matrix(bianchi_c, Jsyms); A2, _ = sp.linear_eq_to_matrix(bianchi_alt, Jsyms)
print("\nBianchi (d_mu *F^{mu nu}) and d_[a F_bc] span same constraints:", A1.rank() == A2.rank() == A1.col_join(A2).rank())

def jet_param(constraints, name='t'):
    A, _ = sp.linear_eq_to_matrix(constraints, Jsyms)
    ns = A.nullspace()
    ts = symbols(f'{name}0:{len(ns)}')
    sub = {}
    vec = sum((t * v for t, v in zip(ts, ns)), zeros(len(Jsyms), 1))
    for k, s in enumerate(Jsyms):
        sub[s] = vec[k]
    return sub, ts
sub_MB, t_MB = jet_param(maxwell_c + bianchi_c)   # Maxwell + Bianchi jets
sub_B, t_B = jet_param(bianchi_c)                  # Bianchi-only jets
print("free jet parameters: Maxwell+Bianchi =", len(t_MB), ", Bianchi only =", len(t_B))

def divergence(S, sub):
    out = []
    for n in range(4):
        e = 0
        for m in range(4):
            e += sum(sp.diff(S[m, n], fs[a]) * J[m][a] for a in range(6))
        out.append(sp.expand(e.subs(sub)))
    return out

# ================= (b) conserved quadratic =================
print("\n=========== (b) quadratic S conserved on Maxwell+Bianchi jets ===========")
cons_eqs = linear_system(divergence(S2, sub_MB), c2)
dim_cons, ns_cons = solve_space(cons_eqs, c2)
print("dim conserved quadratic S:", dim_cons)
cons_basis = [S_from_vec(v, S2, c2) for v in ns_cons]
for k, B in enumerate(cons_basis):
    print(f"  conserved basis[{k}] in (T_maxwell, eta F.F, eta F.*F):", coords_in_basis(B, [T_maxwell, etaFF, etaFFd]),
          "| tr_eta =", tr_eta(B))
    print("     matrix:", B)
print("  T_maxwell conserved?", all(sp.expand(e) == 0 for e in divergence(T_maxwell, sub_MB)))
print("  eta F.F conserved?", all(sp.expand(e) == 0 for e in divergence(etaFF, sub_MB)))
print("  eta F.*F conserved?", all(sp.expand(e) == 0 for e in divergence(etaFFd, sub_MB)))
# does conservation imply covariance? check each conserved basis element against covariance eqs
dim_cons_cov, _ = solve_space(cons_eqs + cov_eqs, c2)
dim_cons_tr, _ = solve_space(cons_eqs + tr_eqs, c2)
print("dim conserved AND covariant:", dim_cons_cov, "; conserved AND traceless:", dim_cons_tr)

# ================= (c) degree <= 2 =================
print("\n=========== (c) polynomial S of degree <= 2 conserved on Maxwell+Bianchi jets ===========")
S012, c012 = general_S([0, 1, 2], 'p')
print("free coefficients:", len(c012))
eqs012 = linear_system(divergence(S012, sub_MB), c012)
dim012, ns012 = solve_space(eqs012, c012)
print("dim conserved deg<=2:", dim012)
for deg, pre in [([0], 'z'), ([1], 'l'), ([2], 'q')]:
    Sd, cd = general_S(deg, pre)
    e = linear_system(divergence(Sd, sub_MB), cd)
    d, ns = solve_space(e, cd)
    print(f"  degree {deg}: dim conserved = {d} of {len(cd)}")
    if deg == [1]:
        for v in ns:
            print("    linear conserved:", S_from_vec(v, Sd, cd))
# the elementary currents F^{mu nu} a_nu, *F^{mu nu} b_nu, as symmetric-tensor constructions:
a = symbols('a0:4'); b = symbols('b0:4')
Ja = Fup * Matrix(a); Jb = Fdual * Matrix(b)
print("  d_mu (F^{mu nu} a_nu) on MB jets zero:", all(sp.expand(sum(sum(sp.diff(Ja[m], fs[k]) * J[m][k] for k in range(6)) for m in range(4)).subs(sub_MB)) == 0 for _ in [0]))
print("  d_mu (*F^{mu nu} b_nu) on MB jets zero:", all(sp.expand(sum(sum(sp.diff(Jb[m], fs[k]) * J[m][k] for k in range(6)) for m in range(4)).subs(sub_MB)) == 0 for _ in [0]))
# general linear S of the form S^{mu nu} = X^nu_b F^{mu b} + Z^nu_g *F^{mu g}; require symmetry
X = Matrix(4, 4, symbols('X0:16')); Z = Matrix(4, 4, symbols('Z0:16'))
Slin = Fup * eta * X.T + Fdual * eta * Z.T     # S^{mu nu} = F^{mu b} eta_{bb} X^{nu b}+...
sym_eqs = linear_system([Slin[i, j] - Slin[j, i] for i in range(4) for j in range(i + 1, 4)], list(X) + list(Z))
dsym, nsym = solve_space(sym_eqs, list(X) + list(Z))
print("  symmetric members of {X.F + Z.*F} (divergence-free by Maxwell/Bianchi):", dsym)
for v in nsym:
    print("    ", Slin.subs({s: val for s, val in zip(list(X) + list(Z), v)}))
# Are all linear S whose divergence vanishes on MB jets of the X.F + Z.*F form?  (annihilator argument)
S1, c1 = general_S([1], 'l')
eq1 = linear_system(divergence(S1, sub_MB), c1)
d1, ns1 = solve_space(eq1, c1)
print("  linear conserved (direct):", d1)

# ================= (d) divergence = Lorentz exchange on Bianchi-only jets =================
print("\n=========== (d) div S = F^{nu lam} j_lam, j^lam = k d_mu F^{mu lam}, Bianchi-only jets ===========")
k = sp.Symbol('k')
jup = Matrix([k * maxwell_c[n] for n in range(4)])        # j^lam
jdn = eta * jup                                            # j_lam
rhs = Fup * jdn                                            # F^{nu lam} j_lam
divS = divergence(S012, sub_B)
rhs_sub = [sp.expand(rhs[n].subs(sub_B)) for n in range(4)]
eqs_d = linear_system([divS[n] - rhs_sub[n] for n in range(4)], c012)
A, bb = sp.linear_eq_to_matrix(eqs_d, c012)
# particular + homogeneous solution
sol = sp.linsolve((A, bb), c012)
print("  solvable:", sol != sp.S.EmptySet)
sol = list(sol)[0]
free = sorted(set().union(*[s.free_symbols for s in sol]) - {k}, key=str)
print("  number of free parameters in solution (homogeneous dim):", len(free))
Ssol = S_from_vec(sol, S012, c012)
# split: particular (free -> 0) and homogeneous
Spart = sp.expand(Ssol.subs({f: 0 for f in free}))
print("  particular solution in (T_maxwell, eta F.F, eta F.*F):", coords_in_basis(Spart, [T_maxwell, etaFF, etaFFd]))
print("  particular solution matrix:", Spart)
# homogeneous: conserved for all Bianchi-only jets
eqs_h = linear_system(divergence(S012, sub_B), c012)
dh, nsh = solve_space(eqs_h, c012)
print("  homogeneous (div S = 0 on Bianchi-only jets) dim:", dh)
for v in nsh:
    print("    ", S_from_vec(v, S012, c012))
# Is Maxwell-stress coefficient forced?  Project general solution onto the quadratic part and check coefficient of T_maxwell
Sq = sp.expand(Ssol - Ssol.subs({f: 0 for f in fs}))   # drop constants
Sq = Sq - sp.expand(Sq.subs({f: 0 for f in fs}))
# quadratic part only:
Squad = zeros(4,4)
for i in range(4):
    for j in range(4):
        P = sp.Poly(sp.expand(Ssol[i,j]), *fs)
        Squad[i,j] = sum(coef*sp.prod([f**e for f,e in zip(fs,mon)]) for mon,coef in P.terms() if sum(mon)==2)
print("  quadratic part of general solution in (T_maxwell, eta F.F, eta F.*F):", coords_in_basis(Squad, [T_maxwell, etaFF, etaFFd]))
print("  sign check: div T_maxwell on Bianchi-only jets vs F^{nu lam} (d_mu F^{mu}_lam):")
dT = divergence(T_maxwell, sub_B)
lorentz = [sp.expand((Fup * eta * Matrix(maxwell_c))[n].subs(sub_B)) for n in range(4)]
for sgn in [1, -1]:
    print(f"    div T == {sgn} * F^{{nu lam}} d_mu F^mu_lam :", all(sp.expand(dT[n] - sgn * lorentz[n]) == 0 for n in range(4)))
