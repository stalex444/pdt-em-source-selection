# Calibration audit — palomar/em_source_selection prose surfaces (2026-10-07)

Gate: calibration-gate (both directions). Scope: formalization.yaml (description, sources[].note,
status.scope, fidelity.divergences, review.notes, alignment), README.md, MATHEMATICS.md, PRIOR_WORK.md,
PROVENANCE.md, VERIFICATION.md. Ground truth used: Challenge.lean / Solution.lean / StatementBridge.lean;
the canon's finding entry for this package and its prior-art report; the original research
batches in the Canon 2 workspace (sources, RESULT.md files, verification-receipt.json);
the registered package pdt-hodge-lie-generation at e2d8dde; Crossref records for the cited DOIs;
the two registered packages' lake-manifest.json pins. Report only; no package file edited.

What this gate did NOT do: re-run `lake build`. No `.lake` directory or build artifact for this package
existed on the audit machine, so the exit-0 / `#print axioms` claims are taken
from the session record and will be settled by the Palomar preflight, not by this audit.

## Numbers that trace (no flag)

- 210 = 10 tensor entries x 21 monomials (`Coeff := Fin 10 -> Fin 21 -> R`); 209 = `Fin 209` in
  `constraints`; 17 = 10 + 6 + 1 (`conservedFamily A b d`); 16 vacuum jets = `testJet : Fin 16 -> Jet`
  (ConservationJets.lean:15); "four current probes" = DifferentiableSourceful.lean:69; "factor 1/2" =
  SourceMaxwell.lean:20 docstring; "background Jacobian scalar" = BackgroundRigidity / SmoothIntegrability.
- 38 / 42 / 21 / 29 exact checks = SOURCE_SELECTION_RESULT.md (C2-059), CONSERVED_SOURCE_RESULT.md (C2-060),
  SMOOTH_SOURCE_RESULT.md (C2-062), SOURCEFUL_SELECTION_RESULT.md (C2-063); all five receipts record
  Lean 4.31.0; the research sources carry Mathlib fabf563a. (But see item 3: a fifth batch is missing.)
- 87 root `.lean` files on disk; 88 files in GravityScreening/; lakefile has 88 `[[lean_lib]]` entries
  (GravityScreening + 87 root); 9 packages in lake-manifest.json; Mathlib 0653561 is also the pin of both
  registered packages (hodge-lie checkout; pfaffian manifest fetched at 0e436b9e). `sorry` occurs only in
  Challenge.lean (12); `native_decide` occurs only inside a doc comment (ResponseClosureCertificate.lean:18);
  no `axiom` declaration. All eleven research theorem names in VERIFICATION.md resolve in StatementBridge.lean.
- GravityScreening/* and ResponseClosure{Certificate,Geometry,OrthogonalBasis}.lean are byte-identical
  (modulo module-system lines) to the hodge-lie package at e2d8dde.
- Twelve declarations: Challenge, Solution, comparator.json and formalization.yaml agree, same order.
- MSC 15A72 (vector/tensor algebra, invariant theory), 35Q61 (Maxwell equations), 70S10 (symmetries and
  conservation laws in field theory): apt for the content. No flag.

## Flags

### 1. VERIFICATION.md — compile claim covers 8 modules that no target builds   [ABOVE]
Quoted: "All 87 root modules and the 88 `GravityScreening` modules compile (every root library built as a
target, 6-7 October 2026, exit 0 ...)".
Evidence: the import closure of all 87 root modules reaches 80 of the 88 GravityScreening modules. The eight
outside every closure are AdjointResponseUniqueness, HodgeBulkScreen, HorizonEinsteinClosureCapstone,
PdtOpticalRepair, PdtStabilizer, QuantumGalileoPhase, StructuralGravityExponent, TwoSidedTraceFree. The
`[[lean_lib]] name = "GravityScreening"` entry has no root module file (`GravityScreening.lean` does not exist,
here or in the hodge-lie package), so building "every root library as a target" never compiles them. Nothing
in the record shows they were built on Lean 4.35.0-rc2 / Mathlib 0653561.
Consistency note: the three smoke modules were dropped on exactly the rationale "outside every proof closure";
these eight (several carrying physics-identification names) are retained on the same footing.
Fix: "All 87 root modules and the 80 GravityScreening modules in their import closure compile ... Eight
GravityScreening modules (list) are carried unchanged from the registered package, lie outside every closure
of this package, and were not built here" — or drop them, as the smoke modules were.

### 2. PROVENANCE.md / VERIFICATION.md / formalization.yaml — port-change record understates what changed   [ABOVE]
Quoted (PROVENANCE): "Port changes: module-system declarations ...; `simp`/`dsimp` steps that no longer act
after `norm_num` wrapped in `try` or removed; tactics that now run after their goal is already closed guarded
with `all_goals`; and one declaration ... given an unbounded heartbeat budget. No statement, definition or proof
logic was changed."
Quoted (VERIFICATION): "Port repairs, all recorded in `PROVENANCE.md`: ... (`FinitePfaffian`, `SourceMaxwell`,
`CrossSource`); ... (`SourceControls`, `ConservationControls`, `SmoothConsequences`); ...
(`UnrestrictedSourceKernel.probe_formulas`). No statement or proof logic changed."
Quoted (yaml prompting_notes): "Port changes were limited to module-system declarations, guarding
simplification steps that no longer act, and one heartbeat budget; no statement or proof logic was changed."
Evidence (line diff of every root module against its original in ~/Documents/Codex/.../outputs, ignoring
`module`, `public import`, `@[expose] public section`, and the added set_option): 16 modules differ, not 7.
  - Undocumented `dsimp -> try dsimp`: BoundaryConnection, ConservationJets, MaxwellResponse, MaxwellSymbol,
    PolynomialConsequences, PolynomialUniqueness.
  - Undocumented `all_goals` guards in the two load-bearing sourceful modules: DifferentiableSourceful (24
    changed lines), SourcefulSelection (24 changed lines).
  - Tactics deleted rather than guarded: CubicInvariance (trailing `<;> rfl` removed on every action lemma),
    StabilizerRecovery (twelve `rfl` lines removed), FinitePfaffian (`simp +decide only [ite_false]` removed).
  - A definition's visibility changed: StabilizerControls `private def metricIntegral` -> `def metricIntegral`.
  - A module restructured: PfaffianBridge — import `CompanionCompatibility` replaced by ResponseBridge,
    HodgeConnection, StressTensor, GravityScreening.HodgeLieGeneration; the definition `pfaffianGenerated` and
    the theorems `generated_same`, `generated_sl`, `generated_dimension`, `hessian_reads_as_phase`,
    `companion_from_pfaffian` (with their `#print axioms`) were REMOVED. CubicInvariance's import
    `PfaffianEM` -> `PfaffianBridge` likewise.
  - Every module gained `set_option backward.isDefEq.respectTransparency false` — this is the unnamed
    "transparency compatibility option"; it is an elaboration option, not a module-system declaration, and
    should be named.
What survives: the twelve compared statements and every research theorem the bridge invokes are unchanged;
the PfaffianBridge removals are consistent with "selected theorems are not imported or resubmitted". But
"limited to", "all recorded in PROVENANCE.md" (PROVENANCE names only one module) and "No statement,
definition or proof logic was changed" are not true as written: a definition and five theorems were deleted
and tactics were removed, not only guarded.
Fix: list all 16 modules by category; name the option; replace the blanket sentence with "No compared
statement, and no research theorem used by StatementBridge, was changed. PfaffianBridge was trimmed to the
declarations the closure needs (the registered package's selected theorems `generated_sl`,
`generated_dimension` and the companion lemmas were removed with their import); `metricIntegral` was made
public."

### 3. Batch list omits C2-061, which is load-bearing   [INCONSISTENT]
Quoted (VERIFICATION): "The original research batches (C2-059, C2-060, C2-062, C2-063) carry their own
30 September 2026 verification receipts ... with 38, 42, 21 and 29 independent exact checks respectively".
Quoted (yaml sources[0].note): "(Canon 2, C2-059, C2-060, C2-062, C2-063, verified 30 September 2026)".
Quoted (PROVENANCE): "the transitive closure of the four research batches" — while the same paragraph lists
five (C2-061 `pdt-polynomial-source` among them).
Evidence: StatementBridge.lean:429 proves `smoothClassification` via
`PDTPolynomialSource.conserved_polynomial_classification` — C2-061's theorem. C2-061
(pdt-polynomial-source-2026-09-30) has its own receipt: 52 public theorems, **32 independent exact checks**,
Lean 4.31.0. The canon's finding entry carries the same four-batch list (correcting it is the canon's
business, not this package's).
Fix: five batches, "38, 42, 32, 21 and 29 exact checks (C2-059, C2-060, C2-061, C2-062, C2-063)"; PROVENANCE
"five research batches".

### 4. PROVENANCE.md — "fourteen folders, 83 root modules" is not reproducible   [INCONSISTENT]
Quoted: "Extraction kept the transitive closure of the four research batches (fourteen folders, 83 root
modules)".
Evidence: the 87 root modules decompose as 3 package-authored (Challenge, Solution, StatementBridge) + 3
copied from the hodge-lie package (ResponseClosure*) + 81 research modules whose originals sit in 21 distinct
Codex output folders (listed in the audit log). Neither 14 nor 83 is recoverable from the shipped package.
Fix: use the reproducible decomposition, or drop the parenthetical.

### 5. Kerrighan citation contradicts the publisher record and the lit-scout report   [INCONSISTENT]
Quoted (yaml, PRIOR_WORK): "**B. Kerrighan**, 'An electromagnetic energy-momentum tensor uniqueness theorem',
J. Math. Phys. 23 (1982), 1979-1980."
Evidence: Crossref deposit for DOI 10.1063/1.525217: title "On the uniqueness of the energy-momentum tensor
for electromagnetism", author D. B. Kerrighan, JMP 23, 1979-1980, 1 Oct 1982. The prior-art report (section
0.2) resolved the same record. review.notes says the literature pass "fixed the framing used here"; this
entry departs from it (the variant title appears to be a secondary-source transcription).
Fix: "D. B. Kerrighan, 'On the uniqueness of the energy-momentum tensor for electromagnetism', J. Math. Phys.
23 (1982) 1979-1980, DOI 10.1063/1.525217."

### 6. formalization.yaml Navarro-Sancho note — "weaker hypotheses"   [ABOVE]
Quoted: "The sourceful statement here reaches the same conclusion on a fixed flat frame under weaker
hypotheses (everywhere differentiable, no naturality or scale axiom)."
Evidence: prior-art table row: "OVERLAPS (D) ... under DIFFERENT hypotheses". Navarro-Sancho do not assume
symmetry, admit derivatives of g and F to arbitrary finite order, and work on a manifold; (D) assumes a
symmetric, field-only source on one flat frame. Weaker in regularity and in dropping naturality/scale;
stronger in the admitted class. PRIOR_WORK.md's "different and weaker" is nearer the record.
Fix: "under different hypotheses: everywhere differentiable with no naturality or scale axiom, but symmetric,
field-only and on a fixed flat frame."

### 7. README — "increasingly weak hypotheses"   [ABOVE]
Quoted: "this formalization answers that question four times over, with increasingly weak hypotheses".
Evidence: `ExchangeLaw k S` implies `Conserved S` (on a vacuum jet `sourcedCurrent 1 D = 0`, hence the
exchange term vanishes), so route 4's law is strictly stronger than route 3's; route 2's conservation and
route 1's covariance+trace are incomparable. Only the regularity hypothesis weakens monotonically
(quadratic -> C^3 -> differentiable).
Fix: "with increasingly weak regularity hypotheses" or "under four different hypothesis sets".

### 8. "each hypothesis is necessary"   [ABOVE, minor]
Quoted (yaml description; README line 18): "Explicit counterexamples show each hypothesis is necessary."
Evidence: the three control declarations show the two laws cannot be dropped (trace-zero, covariance; in the
smooth class, covariance and zero-field/trace). No control addresses the quadratic, C^3, differentiability or
symmetry hypotheses.
Fix: "Explicit counterexamples show that neither law can be dropped."

### 9. PRIOR_WORK.md — formalization-search coverage   [ABOVE, minor]
Quoted: "A search on 6 October 2026 of Mathlib, physlib ..., the Archive of Formal Proofs, Lean4PHYS, Lean
Zulip and the Palomar registry found ..."
Evidence: the report records that the Mathlib docs search "could not be run headlessly — assessed from the
library's directory structure", and that Palomar entries before 2026-09-02 were "not enumerable ... coverage
partial". "Dated search result" is the right frame; the coverage limits are not stated.
Fix: append "(Palomar: public feed from 2 September 2026 only; Mathlib: by library structure)".

### 10. "a remark" for an unverified correspondence   [INCONSISTENT, minor]
Quoted (MATHEMATICS, fidelity.divergences): "The correspondence between the six-parameter cross family and
the elementary linear conservation laws of Maxwell's equations is a remark [in PRIOR_WORK.md], not a
formalized claim."
Evidence: PRIOR_WORK.md says it "has not been checked against the Lean statement and is not asserted"; the
report (section 8) lists it as OPEN, "inferred from dimension count and structure".
Fix: "is noted in PRIOR_WORK.md as an unverified expectation, not a formalized claim."

### 11. Untraceable counts   [INCONSISTENT, minor]
- VERIFICATION: "eleven build rounds" — no log in the record.
- VERIFICATION: "and the four control theorems" — the bridge derives three compared control declarations
  from six research theorems (`metric_invariant_covariant`, `metric_invariant_not_trace_free`,
  `anisotropic_trace_free`, `anisotropic_not_covariant`, `smooth_covariance_control`,
  `smooth_trace_control`). Fix: "the three control declarations, from six research control theorems".
- VERIFICATION: "Port repairs, all recorded in `PROVENANCE.md`" — PROVENANCE names one module. (Folded
  into item 2.)

### 12. One understatement   [BELOW, minor]
PRIOR_WORK.md "The contribution" lists the C^3 classification "without polynomiality, naturality or
symmetry-of-origin assumptions" but omits the regularity contrast the report records: Anco-Pohjanpelto work
with smooth jet functions and Fock takes second partials freely, whereas `smoothClassification` is proved for
globally C^3 sources and the sourceful route for merely differentiable ones. That is a strength of the
kernel-checked statements the prose leaves on the table.
Fix: add "at finite regularity (C^3, and everywhere-differentiable for the sourceful route), where the
classical arguments use smooth jet functions".

## arXiv classification (advisory, not a flag)
math-ph is right. math.RT is defensible only through 15A72 (invariant theory of a fixed six-generator
action); the content is linear algebra plus real analysis on R^6, with no representation theory beyond that
action. math.AP matches 35Q61/70S10 as well or better; math.DG is not apt (one flat frame, no manifold).
Either keep math-ph alone or pair it with math.AP; math.RT is not wrong, but the MSC triple and the arXiv
pair currently point in different directions.

## Checks with no finding
- Retrieval rule / source inversion: every status sentence about the mathematics traces to Challenge.lean or
  the prior-art report; no inverted framing found.
- Tier floor: the sourceful theorem is stated at full strength (no polynomial, degree, C^3, covariance or
  trace hypothesis) in the description, README, MATHEMATICS, and alignment; the conservation route's derived
  covariance / trace / Hodge invariance is stated in all four surfaces.
- Banned frames / class placement / novelty tax: none. No "first" claim beyond the dated bounded form; the
  report's own "first machine-checked statement in any prover" was correctly NOT carried into the package.
- Drafting-layer riders: "no physical coupling is selected", "no curved-space or global solution", "this
  designation does not assert novelty" are constraints the sources require (report section 6), not
  concessions.
- Weight: README leads with content and keeps scope to one paragraph; PRIOR_WORK is proportionally prior
  literature then contribution; MATHEMATICS is statements then proofs then limits. Emphasis tracks the record.

## Direction audit
ABOVE: items 1, 2, 6, 7, 8, 9 (six). INCONSISTENT / neutral: 3, 4, 5, 10, 11 (five). BELOW: 12 (one).
The ABOVE cluster is concentrated in the verification record (items 1-2) and in hypothesis-strength wording
(6-8); it is overstatement of process and comparatives, not of theorems. No minimizing cluster.

## Verdict
MINOR DRIFT — deliverable with the listed corrections. Items 1, 2, 3 and 5 should be fixed before the
public commit: they are statements in VERIFICATION.md / PROVENANCE.md / the citation list that a referee can
falsify mechanically. None of the twelve compared statements, their axioms, or the prior-art framing of the
mathematics is affected.
