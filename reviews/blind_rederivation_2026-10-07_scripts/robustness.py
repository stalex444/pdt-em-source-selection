"""Robustness checks for em_sources.py (same conventions)."""
import sympy as sp
from sympy import Matrix, symbols, Rational, zeros, diag
import importlib.util, sys, io, contextlib
spec = importlib.util.spec_from_file_location("em", "em_sources.py")
em = importlib.util.module_from_spec(spec)
with contextlib.redirect_stdout(io.StringIO()):
    spec.loader.exec_module(em)

eta, Fup, Fdual, fs, pairs = em.eta, em.Fup, em.Fdual, em.fs, em.pairs

# ---- 1. structure of the 6 linear conserved symmetric tensors ----
S1, c1 = em.general_S([1], 'l')
eq1 = em.linear_system(em.divergence(S1, em.sub_MB), c1)
d1, ns1 = em.solve_space(eq1, c1)
lin_basis = [em.S_from_vec(v, S1, c1) for v in ns1]
print("linear conserved dim:", d1)
# candidate: S^{mu nu}(w) = F^{mu r} w_r^nu + F^{nu r} w_r^mu + c * eta^{mu nu} (w_{rs} F^{rs})  with w antisymmetric
# and the dual analogue with *F.
wsyms = symbols('w0:6'); c = sp.Symbol('c')
W = zeros(4, 4)
for (i, j), w in zip(pairs, wsyms):
    W[i, j] = w; W[j, i] = -w                       # w^{rs}
Wdn = eta * W * eta                                  # w_{rs}
def cand(Fm, cc):
    A = Fm * eta * W                                 # F^{mu r} eta_rr w^{r nu}  = F^{mu r} w_r^nu
    tr = sum(Wdn[r, s] * Fm[r, s] for r in range(4) for s in range(4))
    return A + A.T + cc * eta.inv() * tr
for name, Fm in [("F", Fup), ("*F", Fdual)]:
    for cc in [0, Rational(1, 2), -Rational(1, 2), 1, -1]:
        Sc = cand(Fm, cc)
        ok = all(sp.expand(e) == 0 for e in em.divergence(Sc, em.sub_MB))
        print(f"  {name}: F w + (F w)^T + {cc} eta (w.F) conserved on MB jets: {ok}")
# express cand in lin_basis
for name, Fm in [("F", Fup), ("*F", Fdual)]:
    for cc in [Rational(1,2), -Rational(1,2)]:
        Sc = cand(Fm, cc)
        a = symbols(f'a0:{len(lin_basis)}')
        E = Sc - sum((ai*B for ai,B in zip(a, lin_basis)), zeros(4,4))
        eqs = em.linear_system([E[i,j] for (i,j) in em.sympairs], list(a))
        sol = sp.solve(eqs, a, dict=True)
        print(f"  {name}, c={cc}: lies in the 6-dim conserved linear space:", bool(sol))
# are the F-family and *F-family the same 6-dim space?  (dimension of their union)
Sa = cand(Fup, Rational(1,2)); Sb = cand(Fdual, Rational(1,2))
# build spanning vectors over the 60 linear coefficient slots
def vec_of(S):
    v = []
    for (i,j) in em.sympairs:
        P = sp.Poly(sp.expand(S[i,j]), *fs)
        v += [P.coeff_monomial(f) for f in fs]
    return v
rows = []
for w in wsyms:
    rows.append(vec_of(Sa.subs({ww: (1 if ww == w else 0) for ww in wsyms})))
rankF = Matrix(rows).rank()
for w in wsyms:
    rows.append(vec_of(Sb.subs({ww: (1 if ww == w else 0) for ww in wsyms})))
print("  rank of F-family:", rankF, "; rank of F-family + *F-family:", Matrix(rows).rank())
# trace and covariance of the linear conserved space
print("  eta-traces of linear conserved basis:", [em.tr_eta(B) for B in lin_basis])
cov_eqs1 = []
for L in em.gens:
    dF = L * Fup + Fup * L.T
    lhs = em.directional_derivative(S1, dF); rhs = L * S1 + S1 * L.T
    cov_eqs1 += em.linear_system([lhs[i,j]-rhs[i,j] for i in range(4) for j in range(4)], c1)
print("  dim linear S that are Lorentz-covariant:", em.solve_space(cov_eqs1, c1)[0],
      "; covariant AND conserved:", em.solve_space(cov_eqs1 + eq1, c1)[0])

# ---- 2. covariance in the covariant-F convention: dF_lower = -(L^T F_lower + F_lower L) ----
S2, c2 = em.general_S([2], 'q')
Fdn = eta * Fup * eta
cov_eqs_alt = []
for L in em.gens:
    dFdn = -(L.T * Fdn + Fdn * L)
    dFup = eta * dFdn * eta
    lhs = em.directional_derivative(S2, dFup)
    rhs = L * S2 + S2 * L.T
    cov_eqs_alt += em.linear_system([lhs[i,j]-rhs[i,j] for i in range(4) for j in range(4)], c2)
print("covariant-F convention: dim covariant quadratic S =", em.solve_space(cov_eqs_alt, c2)[0])
tr_eqs = em.linear_system([em.tr_eta(S2)], c2)
print("covariant-F convention: dim covariant+traceless =", em.solve_space(cov_eqs_alt + tr_eqs, c2)[0])

# ---- 3. (d) at numeric k, and k-coefficient of Maxwell stress ----
S012, c012 = em.general_S([0,1,2], 'p')
for kval in [1, 3, Rational(-2, 7)]:
    jup = Matrix([kval * em.maxwell_c[n] for n in range(4)])
    rhs = Fup * eta * jup
    divS = em.divergence(S012, em.sub_B)
    eqs = em.linear_system([divS[n] - sp.expand(rhs[n].subs(em.sub_B)) for n in range(4)], c012)
    A, bb = sp.linear_eq_to_matrix(eqs, c012)
    sol = list(sp.linsolve((A, bb), c012))[0]
    free = sorted(set().union(*[s.free_symbols for s in sol]), key=str)
    Ssol = em.S_from_vec(sol, S012, c012).subs({f: 0 for f in free})
    coords = em.coords_in_basis(Ssol, [em.T_maxwell, em.etaFF, em.etaFFd])
    print(f"  k={kval}: homogeneous dim={len(free)}, particular = {coords} (T_maxwell, eta F.F, eta F.*F)")

# ---- 4. (d) without Bianchi (all 24 jets free): still solvable? ----
sub_none = {s: s for s in em.Jsyms}
jup = Matrix([em.maxwell_c[n] for n in range(4)])
rhs = Fup * eta * jup
divS = em.divergence(S012, sub_none)
eqs = em.linear_system([divS[n] - sp.expand(rhs[n]) for n in range(4)], c012)
A, bb = sp.linear_eq_to_matrix(eqs, c012)
print("(d) with NO Bianchi constraint (all 24 jets free): solvable =", sp.linsolve((A, bb), c012) != sp.S.EmptySet)

# ---- 5. (b) without Bianchi: conserved quadratic using Maxwell-only jets ----
sub_M, t_M = em.jet_param(em.maxwell_c)
eqsM = em.linear_system(em.divergence(S2, sub_M), c2)
print("(b) Maxwell-only jets (no Bianchi): dim conserved quadratic =", em.solve_space(eqsM, c2)[0])
eqsB = em.linear_system(em.divergence(S2, em.sub_B), c2)
print("(b) Bianchi-only jets (no Maxwell): dim conserved quadratic =", em.solve_space(eqsB, c2)[0])
