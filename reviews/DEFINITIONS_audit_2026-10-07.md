# Definitions audit — Challenge.lean (em_source_selection), 2026-10-07

Hostile audit of the gap the kernel does not close: whether the DEFINITIONS in
`Challenge.lean` mean what the English (README.md, MATHEMATICS.md, the module docstring)
says. Every item below was settled by computation — a Lean 4.35.0-rc2 check against the
compiled package (files `AuditTest1..7.lean` in the compiled copy, run with
`lake env lean`, all 0 errors on a clean re-run) or an independent sympy replica of the
definitions (`audit_defs.py`, same directory, which re-parses the 209-row `constraints`
table out of `Challenge.lean` rather than retyping it). No package file was edited; the
audited `Challenge.lean` is byte-identical to the compiled copy (`diff` empty).

## Verdict

No FATAL, no SERIOUS finding. Every definition audited means what the English says, with
one consistent convention the English never states explicitly (the six slots are the
UPPER-index components F^{μν}; D μ = ∂_μ). Two MINOR wording points and several NOTEs.

| # | severity | item |
|---|---|---|
| 1 | — (pass) | `field (embed x)` is the antisymmetric matrix F01=x0 … F23=x5 (kernel) |
| 2 | — (pass) | all six `lorentzTable` matrices satisfy Lᵀη+ηL = 0 AND Lη+ηLᵀ = 0 (kernel, `decide`); independent (kernel); bracket-closed (sympy) ⇒ a basis of so(3,1) |
| 3 | — (pass) | `fieldAction k` is exactly the action induced by `tensorAction k` on the embedded field, all six k (kernel); the opposite sign is refuted (kernel) |
| 4 | — (pass) | `stress d F` = d·(F^{μα}F^ν{}_α − ¼η^{μν}F_{αβ}F^{αβ}) with F upper-index (sympy); symmetric and η-trace-free for EVERY F (kernel); T^{33} = ½(E²+B²) ≥ 0 at d=1 |
| 5 | — (pass) | `bianchiJet` = the four Bianchi equations for upper-index F with D μ = ∂_μ (sympy, via the jet of F = dA); `sourcedCurrent 1` = ∂_μF^{μν} = □A^ν − ∂^ν(∂·A); vacuum-jet space has dimension 16; two explicit nonzero vacuum jets proved in the kernel; a non-vacuum jet also exhibited |
| 6 | — (pass) | `constraints maxwellCoefficients = 0` (kernel, all 209 rows); rank 209 over 210 unknowns (sympy); an INDEPENDENT derivation of Covariant ∧ TraceFree on the quadratic class has the same row space and the same 1-dim kernel; `source maxwellCoefficients = registerStress 1 (embed x)` (kernel) |
| 7 | — (pass) | J is the Hodge star on upper-index components with ε^{0123}=+1; J² = −1, JᵀJ = 1 (kernel); `crossCoefficients` is injective in b, `linear (crossCoefficients b) x` is bilinear and symmetric (kernel + sympy) |
| 8 | — (pass) | `RegularSource` = symmetric ∧ each entry C³; `DifferentiableSource` = symmetric ∧ each entry Fréchet-differentiable, as stated |
| M1 | MINOR | "Lorentz covariance" in the English is so(3,1)-equivariance (infinitesimal, connected component); parity and time reversal are not imposed. Harmless here (the selected line is P,T-even and the theorem already pins a 1-dim space), but the docs should say "proper (infinitesimal) Lorentz covariance" |
| M2 | MINOR | The index placement of the slots (upper, F^{μν}) and of the jet (D μ = ∂_μ, lower) is nowhere stated in README/MATHEMATICS. It is the only convention under which `bianchiJet`, `sourcedCurrent`, `stress` and `tensorAction` are simultaneously correct; it should be one sentence in MATHEMATICS.md |
| N1 | NOTE | `divergence` uses `deriv`, whose junk value is 0 off differentiability; `Conserved` is therefore only meaningful under a regularity hypothesis. Every theorem that consumes it supplies one (quadratic, RegularSource, DifferentiableSource, or a polynomial family) — no exposure |
| N2 | NOTE | `smoothClassification` is one direction only (conserved ⇒ in family). sympy shows the converse also holds (every member of `conservedFamily` is conserved: the cross term's divergence vanishes on all 16 vacuum-jet directions for all b). README's "lies in" is accurate and does not overclaim |
| N3 | NOTE | MATHEMATICS.md "identified with the displayed stress including its signs and the factor 1/2": the Maxwell coefficient vector equals `registerStress 1`, i.e. scale d = 1; the "1/2" refers to the ½ entries of the vector, not to a scale. Not wrong, but the sentence could be read as d = ½ |
| N4 | NOTE | The sign convention of `sourcedCurrent` relative to a physical current, and hence whether k > 0 is attractive or repulsive, is not fixed by the package. README says so ("Nothing here selects a physical coupling") — consistent |
| N5 | NOTE | `ExchangeLaw k`: sympy confirms the identity div(stress 1) = exchange(embed x)(sourcedCurrent 1 D) on EVERY Bianchi jet (with +, not −), so "stiffness k" ⇔ "stress of scale exactly k" is the right reading of the theorem |

## The checks, item by item

### 1. `embed`, `field`

`AuditTest1.lean` (pass, ~2.5 s):

```lean
theorem audit_field_embed (a b c d e f : ℝ) :
    field (embed ![a,b,c,d,e,f]) =
      !![0, a, b, c; -a, 0, d, e; -b, -d, 0, f; -c, -e, -f, 0] := by
  ext i j; fin_cases i <;> fin_cases j <;> simp [field, embed]
theorem audit_field_antisymm (v : Register) : (field v).transpose = -field v
```

So slots (0,1,2,5,6,9) ↦ (F01,F02,F03,F12,F13,F23) exactly as the docstring says. `field`
ignores register slots 3,4,7,8,10–14; the Challenge only ever applies it to `embed x` or to
`registerJet D = embed ∘ D`, so nothing leaks through the unused slots.

### 2. `lorentzTable`, `tensorAction`

`AuditTest2.lean` (pass, ~5 s). With `etaZ := diagonal ![1,1,1,-1]` over ℤ:

```lean
theorem audit_generators_vector_form : ∀ k, (lorentzTable k)ᵀ * etaZ + etaZ * lorentzTable k = 0 := by decide
theorem audit_generators_tensor_form : ∀ k, lorentzTable k * etaZ + etaZ * (lorentzTable k)ᵀ = 0 := by decide
theorem audit_tensorAction_metric (k : Fin 6) : tensorAction k metric = 0
theorem audit_generators_independent (a : Fin 6 → ℤ) (h : ∑ k, a k • lorentzTable k = 0) : a = 0
```

Both conventions hold at once (for η diagonal with ±1 entries they are equivalent), so the
file is convention-robust on this point. k = 0,1,3 are the rotations (antisymmetric blocks
in 01, 02, 12), k = 2,4,5 the boosts (symmetric blocks in 03, 13, 23). sympy: rank of the
six 16-vectors is 6; all 15 commutators lie in the span. Six independent elements of the
6-dimensional so(3,1) are a basis.

`tensorAction k T = L T + T Lᵀ` is the infinitesimal action on a CONTRAVARIANT rank-2
tensor when δv = Lv on vectors. `audit_tensorAction_metric` confirms η is invariant under it
(as η^{μν} must be), and item 3 confirms `stress` and `field` are both read as upper-index,
so the action is the correct one for the objects it is applied to.

### 3. `fieldAction` — the decisive check

`AuditTest3.lean` (pass, ~10 s; `simp` closes all 96 entry goals, `ring` never needed):

```lean
theorem audit_fieldAction_induced (k : Fin 6) (x : Local) :
    field (embed (fieldAction k x)) = tensorAction k (field (embed x)) := by
  fin_cases k <;> ext i j <;> fin_cases i <;> fin_cases j <;>
    simp [field, embed, fieldAction, tensorAction, lorentzGenerator, lorentzTable,
      Matrix.mul_apply, Matrix.vecMul, dotProduct, Matrix.transpose_apply, Fin.sum_univ_four]

theorem audit_fieldAction_sign_matters :
    ¬ (∀ k x, field (embed (fieldAction k x)) = - tensorAction k (field (embed x)))
```

Since `field ∘ embed` is a linear bijection onto antisymmetric matrices and `tensorAction k`
preserves antisymmetry, this identity pins `fieldAction k` uniquely: it IS the so(3,1)
action on the bivector, with the same sign as `tensorAction`. Hence `Covariant S` —
d/dt S(x + t·a_k(x))|₀ = ρ(L_k)(S x) — is exactly infinitesimal equivariance of S under
so(3,1) for the representation Λ² → Sym², i.e. Lorentz covariance of a contravariant
symmetric 2-tensor built from F. The headline theorem is about the right group action.
sympy independently reproduces the same identity for all six k and refutes the negated
version.

### 4. `stress`

`AuditTest4.lean` (pass, ~5 s):

```lean
theorem audit_stress_symm (d : ℝ) (F : Tensor) : (stress d F).transpose = stress d F
theorem audit_stress_traceFree (d : ℝ) (F : Tensor) :
    stress d F 0 0 + stress d F 1 1 + stress d F 2 2 - stress d F 3 3 = 0
theorem audit_maxwell_is_stress_one (x : Local) :
    source maxwellCoefficients' x = registerStress 1 (embed x)
```

(`maxwellCoefficients'` is a verbatim copy of `maxwellCoefficients` from
SourceCoefficientData.lean, which is not in the Challenge.) Symmetry and η-tracelessness
hold for every 4×4 F, not only antisymmetric ones.

sympy, with F = field(embed x) read as F^{μν}, F_{μν} := ηFη, FF := F_{αβ}F^{αβ}:
`stress d F == d*(F^{μα}F^{νβ}η_{αβ} − ¼ η^{μν} FF)` identically, and
`invariant F == FF`. Energy-density sign at d = 1: pure F^{03} = E gives T^{33} = E²/2,
pure F^{12} = B gives T^{33} = B²/2; invariant = −2E² and +2B² respectively, i.e.
F·F = 2(B² − E²), the standard value. Operator precedence in
`metric μ ν*invariant F/4` is `(metric μ ν * invariant F)/4`, as intended.

### 5. `divergence`, `bianchiJet`, `sourcedCurrent`, `VacuumJet`, `exchange`, `ExchangeLaw`

`divergence S x D ν = Σ_μ deriv (t ↦ S(x + t·D μ) μ ν) 0`: with D μ = ∂_μ x this is the
chain rule for ∂_μ (S^{μν} ∘ F) = Σ_μ (∂_μ x)·∇S^{μν} — the divergence on the first index.
(N1: `deriv` is a junk 0 where the entry is not differentiable; every consumer of
`Conserved`/`ExchangeLaw` carries a regularity hypothesis, so this is not exploitable.)

`bianchiJet`. sympy builds the genuine first jet of F^{μν} = ∂^μA^ν − ∂^νA^μ from a
quadratic potential A^ν = ½C^ν_{ab}x^ax^b (C symbolic, symmetric in ab), sets
D μ = ∂_μ F (slots upper-index), and finds all four `bianchiJet` expressions ≡ 0. If the
slots were read as LOWER-index F_{μν}, three of the four fail
(`[0, 2C013−2C103, 2C023−2C203, 2C123−2C213]`). So the four equations are
∂_[0F_12] = 0, ∂_[0F_13] = 0, ∂_[0F_23] = 0, ∂_[1F_23] = 0 written in upper-index slots —
the complete Bianchi set — and the slot convention is forced to be contravariant, matching
items 3 and 4.

`sourcedCurrent 1 D ν = Σ_μ field(D μ) μ ν = Σ_μ ∂_μ F^{μν}`; on the jet of dA this equals
□A^ν − ∂^ν(∂·A) (sympy), the Maxwell operator. So `sourcedCurrent 1` is the current in the
convention ∂_μF^{μν} = J^ν (N4: the physical sign is a convention, which the README
disclaims).

`VacuumJet` is NOT vacuous. The 8 equations (4 Bianchi + 4 current) in the 24 jet
unknowns have rank 8, leaving a 16-dimensional space (MATHEMATICS.md's "sixteen admissible
vacuum jets"). Since the equations are first order and linear, F(y) = F₀ + y^μ D_μ is an
exact vacuum solution for every such D, so `Conserved S` is literally "∂_μ S^{μν}(F) = 0
along every vacuum Maxwell solution, at every point". `AuditTest5.lean` (pass, ~2.3 s):

```lean
/-- ∂_1 F^{03} = 1, ∂_3 F^{03} = −1, ∂_1 F^{01} = 1, ∂_3 F^{01} = −1 : a plane wave along y -/
def planeWaveJet : Jet := ![![0,0,0,0,0,0], ![1,0,1,0,0,0], ![0,0,0,0,0,0], ![-1,0,-1,0,0,0]]
theorem audit_planeWave_vacuum : VacuumJet planeWaveJet
theorem audit_planeWave_nonzero : planeWaveJet ≠ 0
def nullspaceJet : Jet := ![![0,0,0,1,0,0], ![0,1,0,0,0,0], ![0,0,0,0,0,0], ![0,0,0,0,0,0]]
theorem audit_nullspace_vacuum : VacuumJet nullspaceJet
theorem audit_nonvacuum_exists : ¬ VacuumJet ![![0,0,0,0,0,0], ![0,0,1,0,0,0], 0, 0]
```

The plane wave with the opposite relative sign of F^{01} fails both Bianchi (013) and the
current (sympy: `bianchi [0,-2,0,0] current [2,0,0,0]`), so the vacuum condition is
genuinely selective.

`exchange v j ν = mink (field v ν) j = F^{νβ} j_β` — the Lorentz-force density. sympy, on
the general Bianchi jet (16-parameter family): `div(stress 1) == exchange (embed x)
(sourcedCurrent 1 D)` identically, with + sign (the − version fails). This is the standard
identity ∂_μT^{μν} = F^{νβ}∂_μF^{μ}{}_β on Bianchi-compatible jets, and it is why
`ExchangeLaw k` selects scale exactly k (N5).

### 6. `constraints`

`AuditTest6.lean` (pass, 79 s, needs `maxHeartbeats 20000000` for the 209 `fin_cases`):

```lean
theorem audit_constraints_maxwell : constraints maxwellCoefficients' = 0
theorem audit_maxwell_nonzero : maxwellCoefficients' ≠ 0
```

So the left side of `finiteCertificate` is satisfied by a nonzero vector and the theorem is
not vacuous. sympy (table parsed from Challenge.lean, 209 rows over the 210 symbols c_i_j):
rank 209; `constraints(maxwell) = 0` row by row. An INDEPENDENT system — collect the
polynomial coefficients of d/dt source(c)(x + t·fieldAction k x)|₀ − tensorAction k
(source c x) for all k and (i ≤ j), plus the 21 coefficients of the η-trace — also has rank
209, the stacked matrix [constraints; independent] has rank 209 (identical row spaces), the
independent nullspace is 1-dimensional and contains the Maxwell vector. The 209 displayed
equations therefore ARE Covariant ∧ TraceFree on the quadratic class, by a route that does
not pass through the package's own proof.

### 7. `J`, `crossCoefficients`, `conservedFamily`, `covariantFamily`

`AuditTest7.lean` (pass, ~6.5 s):

```lean
theorem audit_J_explicit (x : Local) : J *ᵥ x = ![-x 5, x 4, x 3, -x 2, -x 1, x 0]
theorem audit_J_sq : J * J = -1
theorem audit_J_orth : J.transpose * J = 1
theorem audit_cross_symm (b x) : (linear (crossCoefficients b) x)ᵀ = linear (crossCoefficients b) x
theorem audit_cross_linear_in_b (b b' x) : linear (crossCoefficients (b+b')) x = … b … + … b' …
```

sympy: with F_{ρσ} = (ηFη) and ε^{0123} = +1, the six components of
*F^{μν} = ½ε^{μνρσ}F_{ρσ} are exactly `J x` (and not `−J x`). So J is the Hodge star on the
upper-index bivector; J² = −1 is the Lorentzian signature check. Every entry of
`crossCoefficients b` is 0 or ±b_i; the map b ↦ crossCoefficients b has rank 6 (injective;
its row 9 is the identity), and `linear (crossCoefficients b) x` has every entry of degree
exactly 1 in b and in x. Hence `conservedFamily A b d` is an honest 17-parameter family
(10 + 6 + 1), symmetric by construction (`tensorIndex` is symmetric with values 0..9).
`covariantFamily c d = c•η + stress d`: η is covariant (`audit_tensorAction_metric`) with
η-trace 4, so `covariantFamily 1 0` is the right witness for "covariant, conserved, not
trace-free". sympy also confirms: covariant constant symmetric tensors = span(η) (dim 1),
no nonzero b gives a covariant cross term (dim 0) — consistent with `smoothNecessity` and
`smoothZeroFieldSelection`.

### 8. `RegularSource`, `DifferentiableSource`

As stated: symmetry `(S x)ᵀ = S x` for all x, plus `ContDiff ℝ 3` resp.
`Differentiable ℝ` of each scalar entry x ↦ S x i j on Local = Fin 6 → ℝ. "Globally C³"
and "everywhere-differentiable" in the README are the literal meanings.

### Controls

sympy: `source metricInvariantCoefficients == η · invariant(F)` and
`source anisotropicCoefficients == diag(x0², −x0², 0, 0)`, matching the MATHEMATICS.md rows
for `traceNecessity` and `covarianceNecessity`.

## English vs definitions

README.md and MATHEMATICS.md match the definitions. Specifically: "six infinitesimal
Lorentz covariance equations" = `Covariant` over the six so(3,1) basis elements (M1: proper,
infinitesimal); "zero trace" = η-trace; "210 free coefficients" = 10 symmetric entries × 21
monomials, homogeneous quadratic (constants and linear terms are excluded by the CLASS, not
by the laws — which is exactly why statement 3 needs `S 0 = 0`, and the docs say so);
"source-free Maxwell/Bianchi first jet" = `VacuumJet`, a 16-dimensional, non-vacuous,
genuinely selective condition equal to the jets of actual vacuum solutions; "seventeen-
parameter family" = 17 independent parameters; "Hodge map J" = the Hodge star;
"sourceful exchange law at current stiffness k" = ∂_μS^{μν} = F^{νβ}(k ∂_μF^{μ}{}_β), which
`stress k` satisfies identically. The one thing the English omits (M2) is the index
convention that makes all of this consistent: slots are F^{μν}, D μ = ∂_μ, η = diag(1,1,1,−1)
with index 3 the time direction.

## Artifacts

- Lean tests (compiled copy, not in the lakefile): `AuditTest1.lean` … `AuditTest7.lean`
  under `/private/tmp/claude-501/-Users-stephaniealexander-Library-Mobile-Documents-com-apple-CloudDocs-pdt-automath/9014696c-f478-4ad2-8e82-4483eb404c05/scratchpad/em-source-selection/pdt-em-source-selection/`.
  Run: `cd <that dir> && lake env lean AuditTestN.lean`. Clean re-run of all seven: 0 errors.
- sympy replica: `audit_defs.py` in the same directory (`python3 audit_defs.py`,
  sympy 1.14.0, ~13 s, ends `ALL CHECKS PASSED`).
- Audited file: `palomar/em_source_selection/Challenge.lean`, identical to the compiled
  copy's `Challenge.lean`.
