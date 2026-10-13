# Blind re-derivation: symmetric polynomial sources S(F) on flat (R⁴, η = diag(1,1,1,−1))

Date: 2026-10-07. Agent: blind-adversary (independent path; no PDT material consulted; the prompt
contained the problem statement and candidate names only, no solution material).
Tooling: sympy 1.14.0 (exact rational linear algebra). Scripts and raw logs are in
`reviews/blind_rederivation_2026-10-07_scripts/` (`em_sources.py`, `robustness.py`, `run2.log`,
`robustness.log`, `linear_structure.log`); the originals live in the session scratchpad
`/private/tmp/claude-501/.../scratchpad/blind_adversary/`. Scripts are reproduced verbatim in Appendix A.

## 0. Choice of mathematical object

Candidates considered for "symmetric tensor-valued functions S(F) of the six components":
1. S as a polynomial map Λ²(R⁴) → Sym²(R⁴) with contravariant indices S^{μν}, F^{μν} — chosen.
2. S with covariant indices S_{μν}, F_{μν} — equivalent to (1) by raising with η (a sign flip per time
   index); I re-ran covariance in this convention as a robustness check (same dimensions).
3. S as a map on Λ² without any Lorentz structure (just GL(4)) — rejected: the question fixes η and
   so(3,1), and the Bianchi/Maxwell constraints and η-trace need the metric.
4. Conservation as a condition on fields (solutions of Maxwell on an open set) rather than on
   first jets at a point — rejected because the divergence of a polynomial S depends only on the
   first jet; by the Cauchy–Kovalevskaya-free argument "every first jet consistent with the
   constraints is attained by some solution" (the constraints are linear algebraic on the jet and
   the system is linear), the jet formulation is exactly the pointwise statement.

Linear algebra set-up: every condition in (a)–(d) is linear in the coefficients of S and polynomial
in (F, jets); I expand in the monomials of (F, jet parameters) and solve the resulting exact
rational linear system (nullspace / linsolve). Dimensions are therefore exact.

## 1. Conventions (fixed, stated)

* Index 3 is time; η = diag(1,1,1,−1), η⁻¹ = η. Components: F^{01}=f01, F^{02}=f02, F^{03}=f03,
  F^{12}=f12, F^{13}=f13, F^{23}=f23 (contravariant, antisymmetric). F_{μν} = η_{μμ}η_{νν}F^{μν}.
* S^{μν} contravariant symmetric (10 slots). Quadratic S: 10 × 21 = 210 coefficients;
  linear: 10 × 6 = 60; constant: 10; degree ≤ 2 total: 280.
* so(3,1): L = η⁻¹ω with ω antisymmetric (6 generators, ω = E_{ab} − E_{ba}); check Lᵀη + ηL = 0.
  Action on contravariant 2-tensors: δF = L F + F Lᵀ, δS = L S + S Lᵀ.
  Covariance: D S(F)[L F + F Lᵀ] = L S(F) + S(F) Lᵀ for all six L.
* η-trace: η_{μν}S^{μν}.
* Levi-Civita ε^{0123} = +1; dual *F^{μν} = ½ ε^{μνρσ}F_{ρσ}.
  Then F_{μν}F^{μν} = 2(f01²+f02²−f03²+f12²−f13²−f23²),
  F_{μν}*F^{μν} = −4 f01 f23 + 4 f02 f13 − 4 f03 f12.
* Named tensors: (F Fᵀ)^{μν} := F^{μρ}η_{ρρ}F^{νρ} = F^{μρ}F^ν{}_ρ;
  T_Max := F^{μρ}F^ν{}_ρ − ¼ η^{μν} F·F (Maxwell stress; η-trace 0 verified);
  ηFF := η^{μν} F_{ρσ}F^{ρσ}; ηF*F := η^{μν} F_{ρσ}*F^{ρσ}.
  Verified identities: F^{μρ}*F^ν{}_ρ = ¼ η^{μν}(F·*F); *F^{μρ}*F^ν{}_ρ = F^{μρ}F^ν{}_ρ − ½η^{μν}(F·F).
* Jets: J[μ][a] = ∂_μ F^a, 24 symbols. Bianchi: ∂_μ *F^{μν} = 0 (verified to span the same 4
  constraints as ∂_{[α}F_{βγ]} = 0). Maxwell: ∂_μ F^{μν} = 0. Maxwell+Bianchi leaves 16 free jet
  parameters; Bianchi alone leaves 20.
* Divergence: (div S)^ν = Σ_μ ∂_μ S^{μν} = Σ_μ Σ_a (∂S^{μν}/∂F^a) J[μ][a].

## 2. Results

### (a) Quadratic S: covariance and η-trace

| condition | dimension (of 210) | basis |
|---|---|---|
| covariance alone | **3** | T_Max, η^{μν}(F·F), η^{μν}(F·*F) |
| η-trace zero alone | **189** | (210 − 21: one linear condition per quadratic monomial) |
| covariance AND trace zero | **1** | T_Max = F^{μρ}F^ν{}_ρ − ¼η^{μν}F·F |

All three expected candidates occur. The sympy nullspace basis came out as {¼ ηF*F, T_Max − ¼ηFF,
T_Max + ¼ηFF}, i.e. {F^{μρ}F^ν{}_ρ − ½ηF·F = *F*Fᵀ, F^{μρ}F^ν{}_ρ = FFᵀ, ηF*F}, which spans the same
space. F Fᵀ and *F *Fᵀ are both in the covariant space (consistent with the identities above).
The pseudoscalar term ηF*F is covariant under the connected group so(3,1) (it would be excluded
only by parity, which is not part of the stated condition). Trace-zero kills both η-proportional
pieces, leaving T_Max alone (explicit matrix: `run2.log`, "conserved basis[0]", which equals 2·T_Max).

### (b) Quadratic S conserved on all Maxwell+Bianchi first jets

* dimension = **1**, basis = T_Max (nullspace vector = 2·T_Max, η-trace 0).
* η(F·F) and η(F·*F) are NOT conserved (checked directly).
* Conserved ∧ covariant = 1, conserved ∧ traceless = 1: **conservation alone implies both
  covariance and trace-zero** among homogeneous quadratics (the unique conserved line is T_Max,
  which is covariant and traceless). This is a consequence, not an extra assumption.
* Controls: with Maxwell-only jets (no Bianchi) the conserved space is 0-dimensional; with
  Bianchi-only jets (no Maxwell) it is also 0-dimensional. Both constraint sets are needed.

### (c) Polynomial S of degree ≤ 2 conserved on Maxwell+Bianchi jets

The divergence operator preserves polynomial degree in F, so the solution space is graded:

* degree 0: **10** of 10 (every constant symmetric tensor is trivially conserved);
* degree 1: **6** of 60;
* degree 2: **1** of 210 (T_Max);
* total: **17** of 280.

Linear conserved sources, explicit basis (`run2.log`, "linear conserved:"), equivalently the family

    S_ω^{μν} = F^{μρ}ω_ρ{}^ν + F^{νρ}ω_ρ{}^μ + ½ η^{μν} ω_{ρσ}F^{ρσ},   ω ∈ Λ²(R⁴) constant (6 parameters).

Verified: each S_ω is conserved on Maxwell+Bianchi jets; the six S_ω for ω = basis 2-forms are
linearly independent and lie in the 6-dim conserved space, so they are a basis of it. The trace
coefficient ½ is forced (c ∈ {0, −½, ±1} all fail); every S_ω is η-traceless; none is Lorentz-
covariant (the linear covariant space is 0-dimensional — no constant 2-form is invariant).

Relation to the elementary laws ∂_μ(F^{μν}a_ν) = 0 (Maxwell) and ∂_μ(*F^{μν}b_ν) = 0 (Bianchi):
for ω = a∧b the tensor is

    S_{a∧b}^{μν} = (F·a)^μ b^ν + b^μ (F·a)^ν − (F·b)^μ a^ν − a^μ (F·b)^ν + ½ η^{μν} (a∧b)·F,

the symmetrised products of the elementary currents F·a with constant vectors; its divergence
is ∂_μ(F^{μρ}a_ρ) b^ν − (a↔b) [= 0 by Maxwell] plus b·∂ (F·a)^ν − a·∂(F·b)^ν + ½∂^ν((a∧b)·F)
[= 0 by Bianchi]. The dual family built from *F gives NOTHING new: S_ω[*F] = S_{−*ω}[F]
exactly (verified; the F-family and the *F-family together still have rank 6). So the linear
conserved sources are exactly the symmetric "ω-twists" of the F·a currents; the *F·b currents
are the same space re-parametrised by Hodge duality of ω.

### (d) Divergence = Lorentz-force exchange on Bianchi-only jets

Condition: Σ_μ ∂_μ S^{μν} = F^{νλ} j_λ with j^λ = k ∂_μ F^{μλ}, for all jets with ∂_μ *F^{μν} = 0
(20 free parameters), S of degree ≤ 2.

* The system is solvable; the affine solution space is **(particular) + 10-dimensional homogeneous**.
* Homogeneous part (div S = 0 on all Bianchi-only jets): exactly the **10 constant** symmetric
  tensors; no linear and no quadratic homogeneous solution survives when Maxwell is dropped.
* Particular solution: **S = k · T_Max** exactly (coordinates (k, 0, 0) on (T_Max, ηFF, ηF*F);
  no linear or constant part needed). Checked symbolically in k and at k = 1, 3, −2/7.
* Therefore the quadratic part of EVERY solution is k·T_Max: **the coefficient of the Maxwell
  stress is forced to equal k** (with the sign fixed by the stated convention:
  div T_Max = +F^{νλ}∂_μF^μ{}_λ on Bianchi jets in these conventions; the opposite sign check fails).
  A convention that flips the sign of F·j would flip the forced coefficient to −k; the
  magnitude |coefficient| = |k| is convention-free.
* Control: with no Bianchi constraint at all (all 24 jets free) the system is inconsistent — the
  exchange identity needs the Bianchi identity.

## 3. Strongest rival object rejected

The strongest rival was to treat conservation on SOLUTIONS (fields on an open set) and to allow
S to depend on ∂F as well — i.e. to admit improvement terms ∂_ρ(B^{ρμν}) with B antisymmetric in
ρμ, which are conserved identically and would enlarge every solution space. Rejected because the
question restricts S to functions of the six components of F only (no jets in S), which removes
all improvement terms; within that class the jet formulation is exactly equivalent to the
pointwise field formulation (every constrained first jet is realised by a solution of the linear
system). A second rival — imposing parity (O(3,1)) rather than so(3,1) — would drop η(F·*F) from
the covariant space in (a) (3 → 2); I kept the infinitesimal condition as stated, and note that
(b)–(d) do not depend on this choice since η(F·*F) is not conserved anyway.

## 4. Robustness

* Covariant-F convention (δF_{low} = −(LᵀF_{low} + F_{low}L)): covariant dim 3, covariant+traceless 1 — unchanged.
* Bianchi written as ∂_μ*F^{μν} = 0 and as ∂_{[α}F_{βγ]} = 0 give the same constraint span.
* Levi-Civita sign convention only changes the sign of basis elements involving *F; dimensions unchanged.
* (d) checked for symbolic k and three numeric values; particular solution always (k,0,0).
* Negative controls: (b) with only one of the two constraint sets → 0-dim; (d) without Bianchi → inconsistent.
* All linear algebra is exact rational (no floating point); runtime ≈ 40 s + 55 s.

## 5. Summary of forced results

(a) covariant: 3 = span{T_Max, ηF·F, ηF·*F}; traceless: 189; both: 1 = T_Max.
(b) conserved quadratic: 1 = T_Max; conservation ⇒ covariance and trace-zero.
(c) conserved deg ≤ 2: 17 = 10 constants ⊕ 6 linear S_ω (ω ∈ Λ²; the ω-twisted F·a currents,
    *F·b family identical) ⊕ 1 (T_Max).
(d) Lorentz-exchange with current stiffness k on Bianchi jets: S = k·T_Max + (any constant
    symmetric tensor), 10-dim affine; Maxwell-stress coefficient forced = k.

---

## Appendix A — scripts (verbatim)

### em_sources.py
```python
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
```

### robustness.py
```python
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
# express cand in lin_basis  [NOTE: this block is flawed — the candidate still carries the free w
# symbols, which coords_in_basis treats as polynomial variables; the rank test below and
# linear_structure.log are the valid membership checks]
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
```

### linear_structure (inline check, see linear_structure.log)
```python
# per-basis-element membership of the F- and *F-families in the 6-dim conserved linear space,
# the a^b description, and the duality identity S_w[*F] = S_{-*w}[F]
import sympy as sp, io, contextlib, importlib.util
from sympy import Matrix, symbols, Rational, zeros
spec = importlib.util.spec_from_file_location("em", "em_sources.py"); em = importlib.util.module_from_spec(spec)
with contextlib.redirect_stdout(io.StringIO()): spec.loader.exec_module(em)
eta, Fup, Fdual, fs, pairs = em.eta, em.Fup, em.Fdual, em.fs, em.pairs
S1, c1 = em.general_S([1], 'l')
d1, ns1 = em.solve_space(em.linear_system(em.divergence(S1, em.sub_MB), c1), c1)
lin_basis = [em.S_from_vec(v, S1, c1) for v in ns1]
def Sw(Fm, W):
    Wdn = eta*W*eta; A = Fm*eta*W
    return A + A.T + Rational(1,2)*eta.inv()*sum(Wdn[r,s]*Fm[r,s] for r in range(4) for s in range(4))
ok = True
for (i,j) in pairs:
    W = zeros(4,4); W[i,j]=1; W[j,i]=-1
    for Fm in (Fup, Fdual):
        ok &= em.coords_in_basis(Sw(Fm, W), lin_basis) is not None
print("each F- and *F-family element lies in the 6-dim conserved linear space:", ok)
a = Matrix(symbols('a0:4')); b = Matrix(symbols('b0:4'))
W = a*b.T - b*a.T
Fa = Fup*eta*a; Fb = Fup*eta*b   # F^{mu r} a_r
Sab = Fa*b.T + b*Fa.T - Fb*a.T - a*Fb.T + Rational(1,2)*eta.inv()*sum((eta*W*eta)[r,s]*Fup[r,s] for r in range(4) for s in range(4))
print("S(a^b) == Sw(F, a^b):", sp.expand(Sab - Sw(Fup, W)) == zeros(4,4))
print("S(a^b) conserved on MB jets:", all(sp.expand(e)==0 for e in em.divergence(Sab, em.sub_MB)))
def dual2(W):
    Wdn = eta*W*eta; D = zeros(4,4)
    for m in range(4):
        for n in range(4):
            D[m,n] = Rational(1,2)*sum(sp.LeviCivita(m,n,r,s)*Wdn[r,s] for r in range(4) for s in range(4))
    return D
W = zeros(4,4)
for (i,j), w in zip(pairs, symbols('w0:6')): W[i,j]=w; W[j,i]=-w
for sgn in (1,-1):
    print(f"Sw(*F, w) == Sw(F, {sgn}*w):", sp.expand(Sw(Fdual, W) - Sw(Fup, sgn*dual2(W))) == zeros(4,4))
```

## Appendix B — raw output (run2.log, abbreviated to the decisive lines)

```
F.F  = 2*f01**2 + 2*f02**2 - 2*f03**2 + 2*f12**2 - 2*f13**2 - 2*f23**2
F.*F = -4*f01*f23 + 4*f02*f13 - 4*f03*f12
F *F^T - 1/4 eta (F.*F) == 0 ? True
*F*F^T  vs F F^T - 1/2 eta F.F == 0 ? True
tr_eta T_maxwell = 0
(a) number of free quadratic coefficients: 210
    dim covariant quadratic S: 3   [basis coords: (0,0,1/4), (1,-1/4,0), (1,1/4,0)]
    dim traceless quadratic S: 189
    dim covariant AND traceless: 1  = 2*T_maxwell
Bianchi (d_mu *F^{mu nu}) and d_[a F_bc] span same constraints: True
free jet parameters: Maxwell+Bianchi = 16 , Bianchi only = 20
(b) dim conserved quadratic S: 1  = 2*T_maxwell, tr_eta = 0
    eta F.F conserved? False ; eta F.*F conserved? False
    dim conserved AND covariant: 1 ; conserved AND traceless: 1
(c) free coefficients: 280 ; dim conserved deg<=2: 17
    degree [0]: 10 of 10 ; degree [1]: 6 of 60 ; degree [2]: 1 of 210
    linear conserved basis (6 matrices):
      [[f01,0,-f12,-f13],[0,f01,f02,f03],[-f12,f02,-f01,0],[-f13,f03,0,f01]]
      [[f02,f12,0,-f23],[f12,-f02,f01,0],[0,f01,f02,f03],[-f23,0,f03,f02]]
      [[-f03,-f13,-f23,0],[-f13,f03,0,f01],[-f23,0,f03,f02],[0,f01,f02,f03]]
      [[-f12,f02,-f01,0],[f02,f12,0,-f23],[-f01,0,f12,f13],[0,-f23,f13,f12]]
      [[f13,-f03,0,-f01],[-f03,-f13,-f23,0],[0,-f23,f13,f12],[-f01,0,f12,f13]]
      [[f23,0,-f03,-f02],[0,f23,-f13,-f12],[-f03,-f13,-f23,0],[-f02,-f12,0,f23]]
    d_mu (F^{mu nu} a_nu) = 0 on MB jets: True ; d_mu (*F^{mu nu} b_nu) = 0: True
    symmetric members of {X.F + Z.*F}: 6 ; linear conserved (direct): 6
(d) solvable: True ; homogeneous dim: 10 (the ten constant symmetric tensors)
    particular solution = (k, 0, 0) on (T_maxwell, eta F.F, eta F.*F)
    quadratic part of general solution = (k, 0, 0)
    div T == +1 * F^{nu lam} d_mu F^mu_lam : True ;  -1: False
robustness.log:
    F w + (F w)^T + 1/2 eta (w.F) conserved: True (c = 0, -1/2, 1, -1: False); same for *F
    rank of F-family: 6 ; rank of F-family + *F-family: 6
    eta-traces of linear conserved basis: all 0 ; linear covariant: 0 ; covariant AND conserved: 0
    covariant-F convention: dim covariant = 3, covariant+traceless = 1
    k=1,3,-2/7: homogeneous dim=10, particular = (k,0,0)
    (d) with NO Bianchi: solvable = False
    (b) Maxwell-only jets: 0 ; Bianchi-only jets: 0
linear_structure.log:
    each F- and *F-family element lies in the 6-dim conserved linear space: True
    S(a^b) == Sw(F, a^b): True ; S(a^b) conserved on MB jets: True
    Sw(*F, w) == Sw(F, -*w): True
```
