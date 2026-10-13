# Referee review — statement fidelity and overstatement
Package: `palomar/em_source_selection` (canon copy, files dated 6–7 Oct 2026). Reviewer: referee agent, 2026-10-07.
Scope: Lean statements vs prose (abstract, README, MATHEMATICS, PRIOR_WORK, alignment); vacuity; necessity controls; prior-art framing; tier audit. No package file was edited.

## 0. What was checked independently (oracle-level, not model confidence)

- **Rank of the 209 constraints** (sympy, parsed from `Challenge.lean` l.102–311): rank = 209, 209 distinct rows, nullspace dimension 1, and the coefficient vector of `stress 1 (field x)` lies in the nullspace. So "209" is not padded and the quadratic solution set is exactly the stress line.
- **Vacuum jets exist and are nonzero** (the hypothesis of `Conserved` is not vacuous). Hand-built from the definitions: `D 1 = e₁` (∂¹F₀₂ = 1), `D 2 = e₀` (∂²F₀₁ = 1), `D 0 = D 3 = 0` — the static field E = (y, x, 0), curl- and divergence-free. Kernel-checked against the Challenge definitions in the buildable copy (`lake env lean`, exit 0): `VacuumJet refereeJet`, `refereeJet ≠ 0`; plus a sourced Bianchi jet `D 0 = e₀` with `sourcedCurrent 1 _ 1 = 1`, so `ExchangeLaw` quantifies over a class containing genuinely sourced jets. The research module `ConservationJets.lean` carries sixteen such jets (`testJet_vacuum`), a basis of the 16-dimensional vacuum-jet space (24 unknowns − 8 independent linear conditions).
- **Generators**: all six `lorentzTable` matrices satisfy Lᵀη + ηL = 0 and are linearly independent (a basis of so(3,1) for η = diag(1,1,1,−1)); `fieldAction k x` equals L F + F Lᵀ read back into the six slots, for every k — the field and tensor actions are the same representation, so `Covariant` is the correct infinitesimal-covariance equation.
- **Hodge map**: `J` is exactly ⋆ with ε₀₁₂₃ = +1 (J x reproduces the components of ½ε_{μναβ}F^{αβ}); J² = −1; `stress 1 (field (J x)) = stress 1 (field x)` identically.
- **Controls**: `source metricInvariantCoefficients` = η·(F·F) with F·F = 2(x₀²+x₁²+x₃²) − 2(x₂²+x₄²+x₅²); covariant under all six generators, η-trace = 4·F·F ≠ 0. `source anisotropicCoefficients` = diag(x₀², −x₀², 0, 0): trace-free, covariance residual under generator 0 is 2x₀² in the (0,1) entry. Both lie in the homogeneous quadratic class and violate exactly the stated law.
- **Cross family**: `linear (crossCoefficients b) x = stress 1 (x + b) − stress 1 x − stress 1 b` exactly (factor 1), i.e. the cross term is the polarization of the stress at a constant bivector b; its η-trace is 0. The research already proves this in the kernel (`CrossSource.lean` l.24, `cross_stress_increment`).
- **Exchange law sanity**: for a random sourced Bianchi jet, `divergence (stress k) x D = exchange (embed x) (sourcedCurrent k D)` holds identically in x (k = 3).
- **Jet convention**: the formulas are self-consistent only if `D μ` is read as ∂^μF (contravariant index): with D' μ = η^{μμ} D μ the four Bianchi rows, the current and the divergence all become the textbook expressions. Undocumented (see M6).

No FATAL finding. The twelve Lean statements say what the claim table says; the problems are in the surrounding prose.

## 1. Statement-by-statement fidelity (what the Lean actually says)

| # | declaration | Lean statement, in one sentence | prose match |
|---|---|---|---|
| 1 | `quadraticSelection` | For S with some c : Fin 10 → Fin 21 → ℝ, S = source c (symmetric by `tensorIndex`, **homogeneous** degree 2, no constant/linear part): (∀ k x i j, HasDerivAt (t ↦ S(x + t·fieldAction k x) i j) (tensorAction k (S x) i j) 0) ∧ (∀ x, S x 00 + S x 11 + S x 22 − S x 33 = 0) ⟺ ∃ d, S = registerStress d ∘ embed. | yaml l.206, MATH l.33 ✓; "homogeneous" absent everywhere (S2) |
| 2 | `quadraticUniqueness` | Same hypotheses plus both laws: ∃! d. | ✓ |
| 3 | `finiteCertificate` | For every c: constraints c = 0 (209 explicit linear forms) ⟺ Covariant (source c) ∧ TraceFree (source c). | ✓ |
| 4 | `conservationSelection` | For S homogeneous-quadratic symmetric: (∀ x D, bianchiJet (registerJet D) ∧ sourcedCurrent 1 (registerJet D) = 0 → ∀ ν, Σ_μ deriv (t ↦ S(x + t·D μ) μ ν) 0 = 0) ⟺ ∃ d, S = registerStress d ∘ embed. | ✓ but "Conservation alone" sentences omit the class (S2) |
| 5 | `conservationHodgeInvariance` | S homogeneous-quadratic symmetric and Conserved ⟹ ∀ x, S (J *ᵥ x) = S x, J the displayed 6×6 matrix on `Local`. | ✓ (N1) |
| 6 | `smoothClassification` | (∀ x, (S x)ᵀ = S x) ∧ (∀ i j, ContDiff ℝ 3 (x ↦ S x i j)) ∧ Conserved S ⟹ ∃ A b d, S = constant A + linear (crossCoefficients b) + registerStress d ∘ embed. One direction only. | ✓ "lies in"; "classification" overreaches (M1) |
| 7 | `smoothZeroFieldSelection` | Regular ∧ Conserved ∧ Covariant ⟹ (S 0 = 0 ↔ TraceFree S) ∧ (S 0 = 0 ↔ ∃ d, S = stress d). | ✓ |
| 8 | `differentiableSourcefulClassification` | (∀ x, (S x)ᵀ = S x) ∧ (∀ i j, Differentiable ℝ (x ↦ S x i j)) ⟹ [ (∀ x D, bianchiJet (registerJet D) → divergence S x D = exchange (embed x) (sourcedCurrent k (registerJet D))) ⟺ ∃ A, S = conservedFamily A 0 k ]. The k is one universally quantified real on both sides; `crossCoefficients 0` is the zero table, so the cross term is literally 0 and the conclusion is "constant + stress of scale exactly k". | ✓ |
| 9 | `differentiableNormalizedSelection` | Differentiable symmetric, ExchangeLaw k, S 0 = 0 ⟹ S = registerStress k ∘ embed. | ✓ |
| 10 | `traceNecessity` | Covariant (η·F·F) ∧ ¬TraceFree (η·F·F). | ✓ |
| 11 | `covarianceNecessity` | TraceFree (diag(x₀², −x₀², 0, 0)) ∧ ¬Covariant (same). | ✓ |
| 12 | `smoothNecessity` | Regular ∧ Conserved ∧ ¬Covariant for the cross term at b = e₀, d = 0, A = 0; Regular ∧ Conserved ∧ Covariant ∧ ¬TraceFree for the constant η. | ✓ but see M7 |

Seventeen parameters: A ∈ ℝ¹⁰, b ∈ ℝ⁶, d ∈ ℝ. The parameterization is in fact injective (constant A is injective; `crossCoefficients b` row 0 is (b₀, b₁, −b₂, −b₃, b₄, b₅) so b is recoverable; the three pieces have degrees 0, 1, 2), so "seventeen-parameter" is not an overcount; the package nowhere claims injectivity and need not.

## 2. Findings

### SERIOUS

**S1. "each hypothesis is necessary" — overstated.**
`formalization.yaml` l.15: "Explicit counterexamples show each hypothesis is necessary." `README.md` l.18: "Explicit counterexamples show that each hypothesis is necessary."
The Challenge exhibits exactly four controls (its own docstring l.24–26 lists them honestly): trace-zero and covariance in the quadratic selection; covariance and the zero-field normalization in the C³ selection. Not exhibited in the Challenge: necessity of homogeneity (a constant metric is conserved — research `ConservationControls.constant_metric_conserved`), of symmetry (research `columnSource`: conserved, not symmetric), of conservation in the C³ route (research `exponentialSource`), of C³ regularity itself, and of differentiability or symmetry in the sourceful route.
Fix: "Explicit counterexamples show that covariance and zero trace are each necessary in the quadratic selection, and that covariance and the zero-field normalization are each necessary in the C³ selection." (Or port the three further research controls into the Challenge and keep the sentence.)

**S2. "quadratic" never says "homogeneous"; the "conservation alone" sentences do not restate the class.**
`source c` (Challenge l.71–74) contains only degree-2 monomials (`monomialPair`); constants and linear terms are excluded by construction. A reader who takes "quadratic" as "degree ≤ 2" reads `conservationSelection` as false — the conserved symmetric sources of degree ≤ 2 form the seventeen-parameter family, which the package itself proves. Offending text: yaml l.6–7 "Among all symmetric quadratic sources (210 free coefficients)"; l.9 "Conservation alone … selects the same line"; README l.9, l.11; Challenge docstring l.13, l.16; MATHEMATICS l.18 "The quadratic class is parameterized by all 210 coefficients"; alignment l.206, l.221. The "210" and "twenty-one monomials" disambiguate only for a reader who counts.
Fix: write "homogeneous quadratic" at first use in each document, and make the conservation sentence self-contained: "Among symmetric homogeneous quadratic sources, conservation alone — … — selects the same line."

**S3. README l.5–7: "answers that question four times over, with increasingly weak hypotheses, and each time the answer is the Maxwell stress tensor."**
(a) The four hypothesis sets are not totally ordered: route 4 weakens regularity (differentiable vs C³) but strengthens the law (the exchange law binds on every Bianchi jet, sourced ones included, and fixes the scale); routes 2 and 3 differ in class (homogeneous quadratic vs C³), not in strength. (b) Route 3's answer is the seventeen-parameter family; the stress line appears only after adding covariance and S 0 = 0 (`smoothZeroFieldSelection`).
Fix: "answers that question under four different hypothesis sets; in each case what survives, after the stated normalization, is the Maxwell stress."

**S4. Navarro–Sancho comparison misstates their hypotheses and claims "weaker".**
yaml l.87–89: "Theorem 3.5 obtains the Maxwell stress with its coefficient fixed by the current from naturality, scale independence and a sourceful divergence identity. The sourceful statement here reaches the same conclusion on a fixed flat frame under weaker hypotheses (everywhere differentiable, no naturality or scale axiom)." PRIOR_WORK l.26–28 similar ("different and weaker").
Checked against arXiv:1201.3504, Theorem 3.5: the hypotheses are (1) scale independence T(λ²g, λ^{k−1}ω) = T(g, ω); (2) **ω_x = 0 ⇒ T(g,ω)_x = 0** (a zero-field-value hypothesis); (3) div_g T = −i_{∂ω}ω whenever ω is closed. The package omits (2) from its description of their theorem while using the same hypothesis itself (`h0 : S 0 = 0` in `differentiableNormalizedSelection`). And "weaker" is not well-defined here: the package assumes dependence on the six field components only, on one fixed flat frame (N–S natural operators may depend on jets of ω and g on any Lorentzian manifold), while dropping naturality and scale-independence. The sets are incomparable.
Fix: list all three N–S hypotheses including the zero-field one; replace "weaker" with "different and incomparable: fixed flat frame and field-only dependence, but no naturality, no scale axiom, and differentiability only."

### MINOR

**M1. "classification" vs a one-directional statement.** `smoothClassification` states only containment; the research proves the converse (`PolynomialSelection.conserved_family_converse`, `SmoothConsequences.full_smooth_conserved_family`: every member is C³, symmetric and conserved). PRIOR_WORK l.45 "the C^3 classification into an explicit seventeen-parameter family" and the Lean name promise an iff. Fix: add the converse conjunct to the Challenge (one bridge line) or write "containment in".

**M2. The cross-family hedge can be replaced by an exact, kernel-proved statement.** PRIOR_WORK l.21–23 and yaml l.194–196 hedge on whether the cross family matches Anco–Pohjanpelto's elementary linear currents. The package already contains the exact description: `cross_stress_increment` — `registerStress 1 (b + x) = registerStress 1 b + linear (crossCoefficients b) x + registerStress 1 x`. So the cross term is the polarization of the stress at a constant background bivector, and `conservedFamily A b d = (A − d·T(β)) + d·T(x + β)` with β = b/d for d ≠ 0: the family is the closure of {constant + d·stress} under field translation x ↦ x + β, which `Conserved` manifestly respects (jets of constant fields vanish). Recommend stating this (it is stronger and self-contained) and keeping the A–P remark as a remark.

**M3. PRIOR_WORK l.35–37 absence claim slightly too broad.** physlib `master` (GitHub tree, 2026-10-07) has `PhyslibAlpha/Electromagnetism/BoxChargeConservation.lean` (charge conservation) and `Physlib/Electromagnetism/Dynamics/Lagrangian.lean`, `Hamiltonian.lean`; no energy–momentum/stress tensor module. Narrow "no formalized stress tensor, conservation statement or uniqueness statement" to "no energy–momentum tensor, and no conservation or uniqueness statement for one". Keep it dated.

**M4. Lovelock 1974 is resolvable.** D. Lovelock, "The uniqueness of the Einstein–Maxwell field equations", Gen. Relativ. Gravit. 5 (1974), DOI 10.1007/BF00763035 (zbMATH 0335.53034). Kerrighan's 1978 Waterloo thesis under Lovelock bears the same title; Kerrighan 1982 is its concomitant-uniqueness descendant. Give the citation; keeping "no hypothesis set attributed" is fine.

**M5. "Maxwell stress" names the 4×4 object.** In the physics literature "Maxwell stress tensor" is usually the 3×3 spatial block; the 4×4 object is the electromagnetic energy–momentum (stress–energy) tensor, which is the term PRIOR_WORK uses for the citations. Add one gloss in MATHEMATICS §Objects: "the Maxwell stress (the electromagnetic energy–momentum tensor F_{μα}F_ν{}^α − ¼η_{μν}F·F, lower indices, signature (+,+,+,−); sign and scale are carried by d)."

**M6. Jet convention undocumented.** `D μ` is ∂^μF (contravariant): the Bianchi rows carry −D 3 where the textbook ∂_{[μ}F_{νρ]} = 0 has +∂₃, and the current and divergence sums carry no η. A reader checking `bianchiJet` by hand sees a sign flip on the time index. Add one sentence to MATHEMATICS §Objects.

**M7. smoothNecessity wording.** Challenge l.428–429 / alignment l.261: "both laws remain necessary … a conserved covariant source can carry nonzero trace." In `smoothZeroFieldSelection` trace-free is not a hypothesis; the η example shows the zero-field normalization S 0 = 0 cannot be dropped. Say "the zero-field normalization is necessary" rather than implying a trace law.

**M8. Alignment `note` fields duplicate `source` verbatim** (yaml l.210, 215, 220, …, 265). The schema's note is for divergences; either delete or record the real divergence (e.g. for `quadraticSelection`: "class is symmetric homogeneous degree-2; symmetry is built into `tensorIndex`").

**M9. yaml `classification.arxiv: math.RT`** is a stretch for a six-generator action on polynomials; `math-ph` alone (or with `math.DG`) is defensible.

### NOTE

**N1.** `conservationHodgeInvariance` is a one-line corollary of `conservationSelection` and the identity stress(⋆F) = stress(F); not an independent result. Prose is accurate; do not weight it as a twelfth theorem of equal standing in any summary.
**N2.** "covariance and trace zero derived" (yaml l.10) holds by composing `conservationSelection` with `quadraticSelection` (←); no Challenge theorem states Conserved → Covariant directly (research has `conservation_forces_covariance_and_trace`). Acceptable; could be added.
**N3.** Nine of the fifteen register slots are inert in every compared statement; say so (a reviewer will ask why 15).
**N4.** "stiffness" and "sourceful" are idiosyncratic. Gloss "current stiffness k" at first use as "the real factor k multiplying the jet current".
**N5.** `divergence` uses `deriv` (0 on non-differentiable functions). In every compared theorem the source is polynomial, C³ or differentiable, so nothing is vacuous — but a hostile reader will spot `deriv`; one sentence in `fidelity.divergences` closes it.
**N6.** Fock: Appendix B title confirmed ("Proof of the Uniqueness of the Energy-Momentum Tensor of the Electromagnetic Field"), §31* confirmed. Fock's exact regularity assumption was not verified here; PRIOR_WORK's containment claim ("contains the covariance corollary of smoothClassification") should be checked against the text by the PI before submission.
**N7.** Tier audit (TIERS.md): all twelve statements T0; the prior-art sentences T1; the physical reading ("source of the electromagnetic field", "Pisot Dimensional Theory motivates the frame") is T4 motivation and is marked as such (README l.34, yaml l.19, MATHEMATICS l.57–61). The only sentence that presupposes the identification is README l.5 "Which symmetric tensor-valued functions of an electromagnetic field can serve as its source?" — acceptable as the motivating question; it does not become a claim.
**N8.** yaml l.200–202 "No adversarial proof review has yet been run": after fixes, record this review as a statement-fidelity review (not a proof review), dated.
**N9.** The abstract states the sourceful classification as ⇒ while the Lean is ⟺ (alignment l.241 says "and conversely"). Under-claim; harmless.
**N10.** Priority framing elsewhere is clean: "This package does not claim that result as new" (README l.28), "does not assert novelty" (yaml l.45–46), "a dated search result, not a priority claim" (PRIOR_WORK l.37). No offending priority sentence found beyond S4's "weaker".

## 3. Verdict

**FIX-THEN-SUBMIT.** The twelve kernel statements are sound, non-vacuous (nonzero vacuum and sourced jets exhibited and compiled; 209 independent constraints with a one-dimensional nullspace containing the stress; six genuine so(3,1) generators acting identically on field and tensor; J exactly the Lorentzian Hodge star), and the claim table in MATHEMATICS.md matches them line for line. The failures are prose stated above its content: the blanket "each hypothesis is necessary" (S1), "quadratic" without "homogeneous" and "conservation alone" without its class (S2), the README's "increasingly weak hypotheses … each time the answer is the Maxwell stress" (S3), and a Navarro–Sancho comparison that omits their zero-field hypothesis and calls incomparable hypotheses "weaker" (S4). Each has a one-sentence fix. The minor items (M1–M9) improve defensibility; M2 in particular replaces a hedge with a statement the package has already proved.
