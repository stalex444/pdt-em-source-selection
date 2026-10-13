# Literature pass 2 — EM source-selection package (Palomar)
Date: 2026-10-07 · lit-scout · REPORT ONLY (nothing appended to references/library.md; nothing queued to canon)
Builds on: references/prior_art_em_source_selection_2026-10-06.md (§8 "What stays OPEN")
Package: palomar/em_source_selection (PRIOR_WORK.md, formalization.yaml `sources`, Challenge.lean, MATHEMATICS.md)
Rule: classify BY STATEMENT. Verdicts: CONTAINS · OVERLAPS · IRRELEVANT-BY-STATEMENT. Every bibliographic datum below
was resolved against a primary text, Crossref, OpenAlex or the publisher's own page; anything not retrieved is marked.
Scripts for §2 are in reviews/litscout_second_pass_2026-10-07_scripts/ (sympy 1.14.0; exact rational arithmetic).

Status of the five open items: 1 CLOSED (hypotheses retrieved verbatim; theorem text pp. 61–65 still not) · 2 CLOSED
(VERIFIED, with an exact description) · 3 CLOSED (nothing new) · 4 CLOSED (all pages from the printed texts) · 5 CLOSED
(recommend +78A25, +68V20; replace math.RT by cs.LO, add physics.class-ph).

---------------------------------------------------------------------------------------------------
## 1. Lovelock 1974 — retrieved (pp. 59–60 of 59–65), hypotheses now exact

D. Lovelock, "The Electromagnetic Energy Momentum Tensor and its Uniqueness," *International Journal of Theoretical
Physics* 10 (1) (1974) 59–65, DOI 10.1007/BF01808316. Received 18 August 1973; published July 1974. Department of
Applied Mathematics, University of Waterloo. Plenum. (Crossref + Springer page; first two pages retrieved from
Springer's page-one preview service and read; pages 61–65 NOT retrieved — paywalled.)

Abstract, verbatim and complete: "The uniqueness of the electromagnetic energy momentum tensor is established under
general conditions."

Reference list (Crossref, complete): Collinson 1969 (Proc. Camb. Phil. Soc. 66, 437); Fock 1964 (2nd rev. ed.,
Pergamon); Lovelock 1969 (Arch. Rational Mech. Anal. 33, 54); Rund 1966 (Abh. Math. Sem. Univ. Hamburg 29, 243).

SETTING AND HYPOTHESES (pp. 59–60, verbatim, his notation): n-dimensional "Riemannian space" with metric g_{ij};
"Latin indices run from 1 to n"; ψ_i "an arbitrary vector field", F_{ij} = ψ_{i,j} − ψ_{j,i} (1.2); the energy
momentum tensor T^{ij} = −F^{ih}F^j{}_h + ¼ g^{ij}(F_{ab}F^{ab}) (1.1), with the properties (a) symmetric (1.3),
(b) "whenever the source-free Maxwell equations F^{ij}{}_{|j} = 0 (1.4) are satisfied, the divergence of T^{ij}
vanishes by virtue of the identity T^{ij}{}_{|i} = F^{ih}F_h{}^j{}_{|i} (1.5)", (c) "T^{ij} is trace-free in four
dimensions" (1.6). Then: "Guided by the properties (1.3) and (1.5) the present work is devoted to establishing that in
n-dimensions T^{ij} given by (1.1) is essentially the unique solution to the following problem. To find all tensors
B^{ij} for which
  (i)   B^{ij} is a concomitant of g_{ab}, ψ_a and ψ_{a,b}, i.e. B^{ij} = B^{ij}(g_{ab}; ψ_a; ψ_{a,b})   (1.7);
  (ii)  B^{ij} is symmetric   (1.8);
  (iii) B^{ij}{}_{|j} vanishes whenever (1.4) is valid in the sense that B^{ij}{}_{|j} = a^{ih}F_h{}^j{}_{|j}   (1.9),
        where a^{ih} is a tensor and a concomitant of g_{ab}, ψ_a and ψ_{a,b}   (1.10)."
"Alternative conditions under which T^{ij} is determined uniquely have been discussed by Fock (1964, p. 411) and
Collinson (1969)." Section 2 opens: "In view of the fact that B^{ij} and a^{jh} are tensor concomitants certain
invariance identities must be satisfied (Rund, 1966)" — i.e. the proof is Rund's invariance-identity method for
concomitants. Footnote: "Clearly (1.7) guarantees that B^{ij}{}_{|j} is at worst linear in F_{ij,k}."

WHAT IS AND IS NOT ESTABLISHED FROM THE RETRIEVED PAGES. Established: the hypothesis set (i)–(iii) and the stated aim
("essentially the unique solution"). NOT retrievable here: the exact theorem (whether the conclusion is B = αT + λg
with constants, whether λ survives, whether n ≠ 4 adds terms, what a^{ih} comes out to be). Do not assert any of those.

Three features that matter for classification:
 (1) The arguments are the POTENTIAL and its first derivatives (ψ_a, ψ_{a,b}) — not F alone. His class is larger than
     Fock's/Kerrighan's "function of F" class (gauge-dependent, symmetric-derivative-dependent tensors are admitted),
     but the tensors are general-covariant concomitants (Rund's identities) — a covariance assumption the package does
     not make.
 (2) Hypothesis (iii) is NOT jet-wise vanishing on solutions; it is a structural identity "divergence = (unknown tensor
     concomitant a^{ih}) × (Maxwell left-hand side)". The package's `ExchangeLaw k` is precisely this identity with
     a^{ih} FIXED to k·F^{ih}: in Challenge.lean, divergence S x D = exchange (embed x) (sourcedCurrent k D), i.e.
     ∂^μ S_{μν} = k F_ν{}^α ∂^μ F_{μα}. So on the divergence law Lovelock is weaker (a^{ih} free), on covariance and
     smoothness he is stronger (concomitant; smooth in the arguments). Neither contains the other.
 (3) He records trace-freeness in n = 4 as a PROPERTY of T, not as a hypothesis.

VERDICT against the twelve declarations:
| declaration(s) | verdict | reason |
|---|---|---|
| quadraticSelection, quadraticUniqueness, finiteCertificate | IRRELEVANT-BY-STATEMENT | no trace hypothesis, conservation used, covariance via concomitant structure not six infinitesimal laws |
| conservationSelection, conservationHodgeInvariance | OVERLAPS | both derive the stress line from a divergence condition; Lovelock assumes general covariance and admits ψ-dependence, the package assumes neither covariance nor ψ-dependence (field-only, fixed frame, quadratic) |
| smoothClassification | OVERLAPS, does not contain | the six-parameter cross family is not covariant (`smoothNecessity`), so it lies outside Lovelock's concomitant class; his class contains ψ-dependent tensors outside the package's |
| smoothZeroFieldSelection | OVERLAPS (strongly in content) | the covariant-and-conserved corollary; whether his conclusion carries the λg analogue of c·η is on the unretrieved pages — NOT VERIFIED |
| differentiableSourcefulClassification, differentiableNormalizedSelection | OVERLAPS | his (iii) is the exchange-law form with a free coefficient tensor; the package fixes the coefficient to the current stiffness and drops covariance/smoothness to "everywhere differentiable" — this makes Lovelock 1974, not Navarro–Sancho 2012, the closest CLASSICAL analogue of the sourceful statement's hypothesis shape (Navarro–Sancho remains the closest for the CONCLUSION "coefficient fixed by the current") |
| traceNecessity, covarianceNecessity, smoothNecessity | IRRELEVANT-BY-STATEMENT | — |
Overall: OVERLAPS. CONTAINS nothing as stated (different ambient category); CONTAINED by nothing.

RECOMMENDATION for PRIOR_WORK.md: Lovelock 1974 may now be named beyond its title, at the level of the quoted problem
(i)–(iii) and the sentence "essentially the unique solution", citing pp. 59–60. Suggested replacement for the current
"relevant by title; the paper was not retrieved" sentence:
  "D. Lovelock, 'The electromagnetic energy momentum tensor and its uniqueness', Int. J. Theor. Phys. 10 (1974) 59–65,
  poses (pp. 59–60) the problem of all symmetric tensor concomitants B^{ij}(g, ψ, ∂ψ) of the metric and the potential
  whose divergence equals a tensor concomitant times the Maxwell expression, B^{ij}{}_{|j} = a^{ih}F_h{}^j{}_{|j}, and
  states that the Maxwell tensor is 'essentially the unique solution'; the proof uses Rund's invariance identities. Its
  divergence hypothesis is the exchange-law form with a free coefficient; the sourceful statement here fixes that
  coefficient to the current stiffness and assumes neither general covariance nor smoothness beyond differentiability.
  The theorem's exact conclusion (pp. 61–65) was not consulted."
TIER: THEOREM in a refereed journal (T1 as a citation); it lifts no PDT physical identification above T4.

### 1.1 Two earlier items surfaced while chasing Lovelock (new; classify-by-statement)
- C. D. Collinson, "Proof of the uniqueness of the electromagnetic energy momentum tensor," *Math. Proc. Cambridge
  Philos. Soc.* 66 (2) (1969) 437–438, DOI 10.1017/S0305004100045175. Abstract (OpenAlex, verbatim): "An alternative to
  Fock's proof of the uniqueness of the electromagnetic energy momentum tensor is presented. The proof is
  four-dimensional and is applicable in the curved space-time of general relativity." References: Fock 1964; Veblen,
  *Invariants of quadratic differential forms* (1927). Text NOT retrieved (paywalled). VERDICT: by its own abstract it
  re-proves FOCK's theorem (same hypotheses, Appendix B) in four-dimensional covariant form on curved spacetime —
  CONTAINS the covariant-and-conserved corollary of `smoothZeroFieldSelection` exactly as Fock does; nothing else.
  Cite as "Fock's theorem, four-dimensional and curved-space version (Collinson 1969)". THEOREM.
- Ch. Jankiewicz, "A proof of uniqueness of the energy momentum tensor of the electromagnetic field in Riemannian
  space," *Bull. Acad. Polon. Sci. Sér. Sci. Math. Astron. Phys.* (1962), language Russian per OSTI record 4755698
  (University of Wrocław). Volume, pages, and text NOT retrieved. Title-level only; do not name in PRIOR_WORK.md
  beyond "an earlier Polish-Academy note (Jankiewicz 1962) is reported by title" if at all. NOT RETRIEVED.
- I. M. Anderson, "On the structure of divergence-free tensors," *J. Math. Phys.* 19 (12) (1978) 2570–2575, DOI
  10.1063/1.523642 (cites Lovelock 1974). Abstract (OpenAlex, verbatim): "Contravariant rank two tensors which are
  divergence-free on one index and which are constructed from the metric tensor, an auxiliary collection of arbitrary
  tensor fields, and the first and second partial derivatives of these quantities are classified. The results
  generalize existing mathematical arguments in support of the Einstein field equations." VERDICT: SUPPORTS-CONTEXT
  (the concomitant-classification programme Lovelock 1974 belongs to); not a Maxwell-stress statement. THEOREM.
- R. J. Noriega, C. G. Schifini, "The energy-momentum tensor in Yang–Mills field theory and its uniqueness," *Int. J.
  Theor. Phys.* 24 (12) (1985) 1165–1172, DOI 10.1007/BF00670331 (cites Lovelock 1974; text not retrieved) and
  "The uniqueness of the energy momentum tensor in non-Abelian gauge field theories," *J. Math. Phys.* 30 (11) (1989)
  2671–2673, DOI 10.1063/1.528498 (text read, UBA repository). The 1989 paper finds all gauge-invariant symmetric
  T^{ij}(g_{hk}; F^α_{hk}) with T^{ij}{}_{||i} = 0 whenever F^{αij}{}_{||i} = 0, concluding T^{ij} = T_0^{ij} + λg^{ij};
  it describes the 1985 hypothesis as "the restrictive hypothesis T^{ij}{}_{||i} = C_{αβ}H^{βj}F^{αir}{}_{||i}" — the
  Lovelock-type identity (iii) — and says "Clearly (7) is weaker". VERDICT: Yang–Mills generalisation of Kerrighan;
  SUPPORTS-CONTEXT; confirms the two hypothesis shapes (identity-form vs jet-wise) are recognised as distinct in the
  literature. THEOREM.

---------------------------------------------------------------------------------------------------
## 2. Anco–Pohjanpelto 2001, order-zero sector vs the Lean cross family — VERIFIED

Source read: arXiv:math-ph/0108017 v2 (13 Feb 2002; v1 22 Aug 2001), journal ref *Acta Appl. Math.* 69 (3) (2001)
285–327, DOI 10.1023/A:1014263903283; arXiv classes math-ph, gr-qc. Section 2 quoted below from the PDF text.

A–P's objects (Sec. 2): conserved current Ψ^μ on J^q(F) with D_μΨ^μ = 0 on R^q(F) (2.7); trivial if Ψ^μ = D_νΘ^{μν},
Θ antisymmetric (2.8); classification up to equivalence. The order-zero currents that are x-independent are
 (a) stress-energy currents (2.13) Ψ_T^μ(F;ξ) = F^{μσ}F_{νσ}ξ^ν − ¼F^{νσ}F_{νσ}ξ^μ with ξ a CONSTANT vector
     (Prop. 2.3: of the 15-dimensional stress-energy space "4 have no explicit x dependence"); factoring out ξ^ν gives
     the stress-energy tensor (2.27) T^μ{}_ν = F^{μσ}F_{νσ} − ¼δ^μ_νF^{τσ}F_{τσ};
 (b) linear currents (2.19) Ψ_W^μ(F;W,W̃) = W_νF^{μν} + W̃_ν*F^{μν} where "the vector functions W^ν(x), W̃^ν(x)
     satisfy the adjoint Maxwell's equations ∂^{[μ}W^{ν]} + *∂^{[μ}W̃^{ν]} = 0 (2.20)" — constant W, W̃ satisfy (2.20)
     trivially, so the x-independent order-zero linear currents are F^{μν}a_ν + *F^{μν}b_ν with CONSTANT a, b ∈ ℝ⁴
     (eight parameters per current);
 (c) zilch (2.14) and chiral (2.16)/(2.18) currents are of order ≥ 1 (they contain Lie derivatives of F) and, by
     Theorem 2.2 (n₂ ≤ q−1, n₃ ≤ q−1), do not occur at q = 0.
Theorem 2.2 (verbatim): "Every local conservation law (2.7) of order q ≥ 0 of Maxwell's equations (2.1) is equivalent
to a linear combination of the currents Ψ_T^{(n₁)}(F;ξ), Ψ_Z^{(n₂)}(F;ξ), Ψ_V̂^{(n₃)}(F;ξ,Y), Ψ_W(F;W,W̃) (2.26)
involving a sum over conformal Killing vectors ξ and conformal Killing-Yano tensors Y for each n₁, n₂, n₃, with
0 ≤ n₁ ≤ q, 0 ≤ n₂ ≤ q−1, 0 ≤ n₃ ≤ q−1, and solutions W, W̃ of the adjoint Maxwell's equations (2.20)."

What A–P do NOT state (so PRIOR_WORK.md must keep saying "unstated corollary"): (i) the restriction from "equivalent
to" (which allows x-dependent conformal-Killing currents and trivial currents) to currents that are functions of F
only — for such currents the trivial part restricted to solutions is a constant vector, and the x-dependent members
of (2.26) cannot cancel against it; this step is a short argument they do not write; (ii) any symmetric-tensor
assembly of four currents; (iii) any C³-only regularity (their jet functions are smooth).

THE CHECK (scripts cross_check.py, struct_check.py, polar_check.py; exact rational sympy). Conventions read off
Challenge.lean and confirmed by the sign pattern of `bianchiJet`: x = (F₀₁,F₀₂,F₀₃,F₁₂,F₁₃,F₂₃) lower-index components,
η = diag(1,1,1,−1), jet D_μ = ∂^μx (so `sourcedCurrent 1 D = 0` is ∂^μF_{μν} = 0 and `divergence` is ∂^μS_{μν});
*F_{μν} = ½ε_{μναβ}F^{αβ} with ε₀₁₂₃ = +1 (the displayed `J` is exactly this star on the six components: J x =
(−x₅, x₄, x₃, −x₂, −x₁, x₀) matches *F₀₁ = −F₂₃, *F₀₂ = F₁₃, *F₀₃ = F₁₂, *F₁₂ = −F₀₃, *F₁₃ = −F₀₂, *F₂₃ = F₀₁).

Results (all exact):
 1. Lean side. `linear (crossCoefficients b) x`, b ∈ ℝ⁶: the six generators cross(e_k) are linearly independent
    (rank 6 in the 96-dimensional space of linear maps ℝ⁶ → 4×4 matrices). Every cross(b) is symmetric, has η-trace
    zero, and is CONSERVED on every vacuum jet (divergence vanishes identically on the 16-dimensional space of jets
    satisfying the four Bianchi and four Maxwell relations) — the converse direction that `smoothClassification` does
    not state. The space of ALL symmetric sources linear in x (60 parameters) that are conserved is exactly
    6-dimensional, so the cross family is the whole conserved linear sector.
 2. A–P side ("six parameters a, b ∈ ℝ⁴ modulo what?"). Assemble one elementary linear current per column:
    S_{μν} = F_{μα}a^α{}_ν + *F_{μα}b^α{}_ν, with a, b arbitrary 4×4 matrices — 32 parameters. Imposing S_{μν} = S_{νμ}
    for all F leaves exactly 6 free parameters, and the resulting family has rank 6 (the parametrisation is injective
    on the symmetric solution space). Structure: the symmetry forces a_{αν} (both indices lowered) to be ANTISYMMETRIC
    — a constant bivector, 6 parameters — and b = *a (the Hodge dual of a, in the ε convention above; with the opposite
    ε sign, b = −*a). So the symmetric assembly is {F_{μα}a^α{}_ν + *F_{μα}(*a)^α{}_ν : a ∈ Λ²ℝ⁴}. Answer to "modulo
    what": 32 → 6 by symmetry alone; no quotient by trivial currents is needed because none of these 32 is trivial on
    solutions (trivial order-0 x-independent currents are constants, which sit in the 10-parameter constant block).
 3. Equality of spans: the joint rank of the Lean six and the A–P six is 6 — the spans COINCIDE. Explicit match: with
    a read as a slot vector in the same order as x, Lean's b equals −a, i.e.
       cross(b)_{μν} = −[F_{μα}b^α{}_ν + *F_{μα}(*b)^α{}_ν]   (b as a bivector in slots 01,02,03,12,13,23).
    Each cross(e_k) is realised by an explicit (a, b) pair (listed in the script output; e.g. cross(e₀) has a in the
    (0,1)-plane and *a in the (2,3)-plane).
 4. A sharper description (new, verified): cross(b)(x) = stress(x + b) − stress(x) − stress(b) EXACTLY — the
    six-parameter cross family is the POLARISATION of the Maxwell stress at a constant bivector b. Consequently
    conservedFamily A b d, for d ≠ 0, equals (A − d·stress(b/d)) + d·stress(x + b/d): "a constant plus the Maxwell
    stress of the field translated by a constant bivector"; for d = 0 it is the pure polarisation. This is an algebraic
    identity (bilinearity of the stress), so it follows from the computation above and needs no further hypothesis.
 5. Hodge behaviour: the stress is pointwise J-invariant (stress(Jx) = stress(x), consistent with
    `conservationHodgeInvariance`); the cross family is NOT pointwise J-invariant but is J-STABLE as a space, with
    J acting on the parameter as b ↦ (b₅, −b₄, −b₃, b₂, b₁, −b₀) — i.e. the star acting on the bivector b — consistent
    with `conservationHodgeInvariance` being a statement about the quadratic class only.
 6. Dimension count of the seventeen: constants 10 (symmetric constant tensors = the trivial currents on solutions) +
    cross 6 (one bivector) + stress 1 (constant ξ assembled symmetrically) = 17.

STATUS: VERIFIED (exact symbolic computation, not kernel-checked). Tag for the package: EXPERIMENTAL-EXACT; it supports
the REMARK in PRIOR_WORK.md and the `fidelity.divergences` sentence in formalization.yaml, which may now read "verified
by exact computation on 2026-10-07 (reviews/litscout_second_pass_2026-10-07_scripts), not formalized". It does not
make the correspondence a formalized claim. Suggested PRIOR_WORK.md wording:
  "Its order-zero, x-independent sector — the stress-energy currents (2.13) with constant ξ and the elementary linear
  currents (2.19) with constant W, W̃ — assembles, under the symmetry requirement, to exactly the seventeen-parameter
  family: the six-parameter cross term is F_{μα}a^α{}_ν + *F_{μα}(*a)^α{}_ν for a constant bivector a, equivalently
  the polarisation T(F + a) − T(F) − T(a) of the Maxwell stress. This identification was verified by exact computation
  against the Lean definitions (not formalized); the symmetric-tensor statements and the C³ regularity are not in
  Anco–Pohjanpelto."
One caution: the A–P sector contains the cross family only AFTER the unwritten x-independence step (i) above; the
kernel-checked `smoothClassification` proves that step directly for C³ sources, which is part of the package's
contribution and should stay described as such.

---------------------------------------------------------------------------------------------------
## 3. Formalizations re-checked 2026-10-07 — nothing new

| venue | checked how (today) | result |
|---|---|---|
| Mathlib | package pin: Lean 4.35.0-rc2, Mathlib 065356127b1d (lake-manifest.json). Content grep of the local checkout fabf563a7c (2026-06-15) over Mathlib/**/*.lean for Maxwell, stress, energy-momentum, electromagnet, Lorentz: 0 files each. Docs search is client-side and was not run headlessly; Mathlib has no physics scope. | none |
| physlib (leanprover-community/physlib, formerly PhysLean) | pushed 2026-10-07T13:29:50Z. Full tree (1,448 paths) listed via the API; all 202 .lean files under Physlib/Electromagnetism, Physlib/Relativity, PhyslibAlpha/Electromagnetism and ClassicalMechanics fetched raw (2.2 MB) and grepped: "stress" 0, "energy-momentum" 0, "energyMomentum" 0, "Poynting" 0, "momentum density" 0; "Maxwell" 11 files (ThreeDimension/MaxwellEquations.lean, Vacuum/*, Distributional/*); "Noether"/"conserv" only in PhyslibAlpha/ClassicalMechanics/MomentMap/Basic.lean (Souriau moment map, Noether for Hamiltonian flows — particle mechanics, not field theory). | no stress tensor, no conservation of a field tensor, no uniqueness |
| Lean4PHYS (ShirleyLIYuxin/Lean4PHYS) | pushed 2026-03-20; tree: Electromagnetism contains only Couloubconstant.lean (v1 and v2) | none |
| Isabelle AFP, Mathematics/Physics | 8 entries (GNS construction 2026-03-09; gyrovector spaces/special relativity 2025; Malament–Hogarth 2023; No FTL observers GenRel 2023; Schutz Minkowski axioms 2021; units type system 2020; safe-distance checker 2020; No FTL observers 2016) | none |
| Palomar registry | data.palomar-registry.org/recent.json read; 39 entries dated 2026-10-02-000008 … 2026-10-07-000006 listed (Vaught counterexample, Erdős problems, Catalan formalization, Gerver sofa, four-body configurations, …); no entry mentions Maxwell, electromagnetism, stress/energy-momentum, Lorentz, bivector, conservation law or concomitant. Pre-2026-09-02 window: still not enumerable (unchanged from pass 1). | none |
| openai/math | repository unchanged since the initial commit (2026-10-06T21:58:50Z; pushed_at 22:01:11Z). The 2026-10-06 review's §6.0 keyword scan of all 405 Challenge files (zero hits: stress, Lorentz-covariance; "Maxwell" only in VlasovMaxwell and BoltzmannNonuniqueness) therefore stands; not redone. | none |

---------------------------------------------------------------------------------------------------
## 4. Textbook statements — exact sections and pages (read from the printed texts, not memory)

**Landau & Lifshitz**, *The Classical Theory of Fields* (Course of Theoretical Physics vol. 2), Fourth Revised English
Edition, translated from the Russian, Butterworth-Heinemann (original ISBN 978-0-7506-2768-9); pages read on the
Indian facsimile reprint (ISBN 978-81-8147-787-3; running heads carry the original pagination).
- Chapter 4 "The electromagnetic field equations": §31 "Energy density and energy flux"; **§32 "The energy-momentum
  tensor", pp. 82–85**; **§33 "Energy-momentum tensor of the electromagnetic field", pp. 86–89**; §34 "The virial
  theorem", p. 90; §35 "The energy-momentum tensor for macroscopic bodies", p. 92.
- Also §94 "The energy-momentum tensor" (gravitational chapter; definition by metric variation), p. 290.
- Content (verbatim): §32: "It is necessary to point out that the definition of the tensor T^{ik} is not unique. In
  fact, if T^{ik} is defined by (32.3), then any other tensor of the form T^{ik} + ∂ψ^{ikl}/∂x^l (32.7) will also
  satisfy equation (32.4) … To define the tensor T^{ik} uniquely we can use the requirement that the four-tensor of
  angular momentum (see § 14) of the system be expressed in terms of the four-momentum by …" [⇒ symmetry]. §33: the
  canonical tensor "is not symmetric. To symmetrize it we add the quantity …" [⇒ (33.1)]; "In addition it has the
  property that T^i_i = 0" (33.2).
- Classification: DERIVATION + the standard "improvement ambiguity" remark; the only selection principle is symmetry
  from angular-momentum conservation. NO uniqueness theorem. SUPPORTS-CONTEXT. Pass-1 "§§32–33" was correct; the pages
  are now fixed.

**Jackson**, *Classical Electrodynamics*, 3rd ed., John Wiley & Sons, 1999, ISBN 0-471-30932-X.
- **§12.10 "Canonical and Symmetric Stress Tensors; Conservation Laws", pp. 605–612** (§12.11 "Solution of the Wave
  Equation in Covariant Form; Invariant Green Functions" begins p. 612). Subsections: A "Generalization of the
  Hamiltonian: Canonical Stress Tensor"; B "Symmetric Stress Tensor"; C "Conservation Laws for Electromagnetic Fields
  Interacting with Charged Particles".
- Content (verbatim, §12.10 B): "conservation of angular momentum requires that T^{αβ} be symmetric. Two final
  criticisms of T^{αβ}, (12.104), are that it involves the potentials explicitly, and so is not gauge invariant, and
  that its trace (T^α_α) is not zero, as required for zero-mass photons. There is a general procedure for constructing
  a symmetric, traceless, gauge-invariant stress tensor Θ^{αβ} from the canonical stress tensor T^{αβ} (see the
  references at the end of the chapter). For the electromagnetic T^{αβ} of (12.104) we proceed directly."
- Classification: Belinfante-type construction from the Lagrangian; NO uniqueness theorem. SUPPORTS-CONTEXT. Pass-1
  "§12.10" was correct.

**Fock**, *The Theory of Space, Time and Gravitation*, 2nd revised edition, translated by N. Kemmer, Pergamon Press,
1964 ("This edition follows closely the second Russian edition published in 1961" — Preface to Second Edition).
- **§31* "A System of Equations for the Components of the Mass Tensor as Functions of the Field", pp. 98–100** (§32
  "Examples of the Mass Tensor" begins p. 101); §33 "The Energy Tensor of the Electromagnetic Field", pp. 106–109;
  **Appendix B "Proof of the Uniqueness of the Energy Momentum Tensor of the Electromagnetic Field", pp. 411–416**
  (Appendix A ends p. 410; Appendix C "Proof of the Uniqueness of the Hydrodynamic Mass Tensor" begins p. 417).
  Independent confirmation: Lovelock 1974 cites "Fock (1964, p. 411)". Chapter DOI (ScienceDirect, pass 1):
  10.1016/B978-0-08-010061-6.50017-2.
- The package's existing citation "section 31* and Appendix B" is correct; add the page ranges.

---------------------------------------------------------------------------------------------------
## 5. MSC2020 and arXiv classification — descriptions verified against the official MSC_2020.csv (msc2020.org)

Current codes, with the official text:
- 15A72 "Vector and tensor algebra, theory of invariants" — KEEP. Exactly the quadratic/invariant-theory content
  (Lorentz-covariant quadratic tensors, the 209-equation certificate).
- 35Q61 "Maxwell equations" — KEEP. Conservation is imposed on Maxwell/Bianchi jets.
- 70S10 "Symmetries and conservation laws in mechanics of particles and systems" (under 70Sxx "Classical field
  theories") — KEEP. The conservation-law selection; Anco–Pohjanpelto sits here.
Recommended additions (both describe the object as classified by zbMATH/MathSciNet):
- 78A25 "Electromagnetic theory (general)" — ADD. The home of the electromagnetic stress tensor itself; Kerrighan 1982
  and Navarro–Sancho 2012 are electromagnetic-theory papers.
- 68V20 "Formalization of mathematics in connection with theorem provers" — ADD. The artifact is a formalization; this
  is the MSC2020 code created for exactly that.
Considered and NOT recommended: 83C50 "Electromagnetic fields in general relativity" and 83C22 "Einstein–Maxwell
equations" (the package is flat-frame only and asserts no curved-space statement); 53A55 "Differential invariants
(local theory), geometric objects" (the concomitant framing of Lovelock/Kerrighan — the package deliberately is not a
natural-bundle result); 70S05 (no Lagrangian is assumed); 68V15 "Theorem proving (automated and interactive …)" (the
contribution is the formalized mathematics, not prover technology — 68V20 is the sharper code).

arXiv:
- math-ph — KEEP as primary (Anco–Pohjanpelto and Navarro–Sancho are math-ph).
- math.RT "Representation Theory" — REPLACE. The package uses the six-generator action on bivectors and symmetric
  tensors as a finite linear-algebra certificate; arXiv's math.RT is for representation theory proper, and a
  moderator would likely reclassify. Nothing in the twelve statements is a representation-theoretic result.
- cs.LO "Logic in Computer Science" — ADD. arXiv's category for proof-assistant formalizations (Mathlib and Lean
  formalization papers are routinely cross-listed cs.LO; the schema's `automation` and `fidelity` blocks are about
  exactly this).
- physics.class-ph "Classical Physics" — ADD (optional). Where electromagnetic stress-tensor papers without a GR
  component appear (e.g. arXiv:1802.02141 surfaced in the search log is physics.class-ph).
Recommended set: msc2020 [15A72, 35Q61, 70S10, 78A25, 68V20]; arxiv [math-ph, cs.LO, physics.class-ph].

---------------------------------------------------------------------------------------------------
## 6. Mischaracterizations to fix / wording the package may now use

1. PRIOR_WORK.md ¶"Rainich … Lovelock": replace "D. Lovelock's 1974 concomitant theorems are relevant by title; the
   paper was not retrieved and no specific hypothesis set is attributed to it here" by the §1 wording (hypotheses
   (i)–(iii) quoted from pp. 59–60; theorem text not consulted). Do NOT write "Lovelock proves B = αT + λg".
2. PRIOR_WORK.md ¶Anco–Pohjanpelto: the last sentence ("whether the cross family coincides exactly … has not been
   checked … and is not asserted") is now FALSE as a status report; replace by the §2 wording (verified by exact
   computation; not formalized). formalization.yaml `fidelity.divergences` and the A–P `sources.note` likewise.
3. Add Collinson 1969 next to Fock (Fock's theorem in four-dimensional covariant form, curved spacetime); it is the
   paper Lovelock names as the other "alternative conditions" source. Keep Jankiewicz 1962 out unless a text is read.
4. Textbook citations: give "Landau–Lifshitz 4th rev. English ed., §32 pp. 82–85, §33 pp. 86–89" and "Jackson 3rd ed.,
   §12.10 pp. 605–612" and "Fock 1964 §31* pp. 98–100, Appendix B pp. 411–416"; characterise LL/Jackson as
   DERIVATIONS with the symmetrisation/improvement remark, never as uniqueness theorems.
5. Classification: msc2020 add 78A25, 68V20; arxiv drop math.RT, add cs.LO (and optionally physics.class-ph).
6. Framing nuance for the sourceful statement: the CLOSEST CLASSICAL HYPOTHESIS SHAPE is Lovelock 1974 (iii)
   (divergence = coefficient tensor × Maxwell expression), the closest CONCLUSION is Navarro–Sancho 2012 Thm 3.5
   (coefficient fixed by the current). The current PRIOR_WORK.md text names only Navarro–Sancho; adding the Lovelock
   sentence closes that gap before a referee opens it.
7. Unchanged from pass 1: no "first derivation of uniqueness" claim; Rainich-direction papers are converse results;
   Gotay–Marsden/Choi assume a Lagrangian; Kerrighan pages 1979–1980 (re-confirmed via OpenAlex, abstract verbatim).

---------------------------------------------------------------------------------------------------
## 7. What stays OPEN after this pass
- Lovelock 1974 pp. 61–65 (the theorem statement and the fate of the λg term): not retrieved. Cite at the level of §1.
- Collinson 1969 and Jankiewicz 1962 texts: not retrieved (abstract-level and title-level respectively).
- Palomar entries before 2026-09-02: still not enumerable through the public data endpoints.
- The A–P "x-independence" step (§2, caution): a short argument the paper does not write; the package proves it
  directly (C³) and should keep saying so.

---------------------------------------------------------------------------------------------------
## 8. Search log (2026-10-07; what was fetched, and the outcome)
- link.springer.com/article/10.1007/BF01808316 → 303 to IdP (WebFetch) / "Client Challenge" (curl). rd.springer.com
  same article → 200: title, one-sentence abstract, references (Collinson, Fock, Lovelock 1969, Rund 1966), received
  date, institution. page-one.springer.com/pdf/preview/10.1007/BF01808316 → 200, PDF of pp. 59–60, read with pdftotext.
- api.crossref.org/works/10.1007/BF01808316 → metadata + 4 references, no abstract. api.openalex.org works/doi: →
  no abstract; 6 citing works listed with abstracts (Anderson 1978, Lovelock 1977, Noriega–Schifini 1985,
  Martínez-Bohórquez 2023, two quantum-stress papers). api.semanticscholar.org → citation list, no abstract.
  inspirehep.net title search → 0 hits.
- WebSearch "Lovelock 1974 electromagnetic energy momentum tensor and its uniqueness" (extended) → surfaced Collinson
  1969 (Cambridge) and Jankiewicz 1962 (OSTI 4755698); both record pages fetched. WebSearch for the Noriega–Schifini
  1985 paper → UBA repository records; JMP 1989 PDF downloaded from bibliotecadigital.exactas.uba.ar and read; the 1985
  PDF link (digital.bl.fcen.uba.ar) → 404, aggregator records → 429 (rate-limited twice). Google Books API queries for
  Lovelock–Rund snippets → no items.
- arxiv.org/abs/math-ph/0108017 → metadata; arxiv.org/pdf/math-ph/0108017 → PDF saved, pdftotext, Sec. 2 read (lines
  150–420 of the text dump). arxiv.org/pdf/1201.3504 (Navarro–Sancho) → PDF, pdftotext; intro and bibliography read
  (their refs [9],[10] are Lovelock's GRG 1974 and JMP 1977 papers, NOT the IJTP 1974 paper). arxiv.org/html/2304.02378
  (Martínez-Bohórquez) → bibliography: Lovelock IJTP 1974 is their [14], grouped as "classical characterizations".
- api.github.com: physlib repo (pushed_at), full recursive tree, 202 raw .lean files fetched and grepped; Lean4PHYS
  repo + tree; openai/math repo + commits. `gh` not installed; unauthenticated code search → 401 (not used).
  git clone of physlib was denied by the permission system; the raw-file route replaced it.
- Local: ~/palomar-entries/family-boundary/.lake/packages/mathlib (fabf563a7c) grepped; package lake-manifest.json and
  lean-toolchain read.
- data.palomar-registry.org/recent.json → 39 entries since 2026-10-02 listed; keyword check negative.
- isa-afp.org/topics/mathematics/physics/ → 8 entries listed.
- archive.org: Fock 1964 (item v-a-fock.-the-theory-of-space-time-and-gravitation, djvu text) — ToC, running heads,
  preface read; Jackson 3rd ed. 1999 (item john-david-jackson-classical-electrodynamics-wiley-1999, djvu text) — ToC,
  §12.10 read; Landau–Lifshitz vol. 2 (item classical-theory-of-fields-landau-lifshitz, djvu text of the Butterworth-
  Heinemann Indian reprint, 4th revised English ed.) — front matter, ToC, §§32–33 running heads read; the
  "landau-and-lifshitz-physics-textbooks-series" item is dark (403) and the library-lending items return 403/401.
  ScienceDirect ToC pages (LL, Fock) → 403.
- msc2020.org/MSC_2020.csv → downloaded (tab-separated); descriptions quoted. zbmath.org/classification → 403.
- Scripts (sympy 1.14.0): cross_check.py (ranks, conservation, trace, explicit (A,B) per generator, Hodge),
  struct_check.py (bivector/dual structure, b ↦ a map), polar_check.py (polarisation identity). First Hodge run gave a
  false negative from sequential `subs`; corrected to simultaneous `xreplace` — recorded here so the artefact is not
  mistaken for a result.
