# Verification status — 7 October 2026

**Local verification record, completed before publication.** Public-commit preflight results will be recorded
in the repository's Actions runs once the package is published; nothing below is a Palomar acceptance.

All 87 root modules and all 80 `GravityScreening` modules compile on Lean 4.35.0-rc2 against Mathlib revision
`065356127b1dc0016f66b7283ce0ce2c4055aa55`, with the nine transitive packages pinned in `lake-manifest.json` (the same pin
as the two registered packages this one builds on). Every root library was built as a target (6–7 October 2026, exit 0);
every `GravityScreening` module lies in the import closure of some root module, so that build covers them all. Eight
`GravityScreening` modules outside every closure, and three smoke-test modules outside every proof closure, were dropped
rather than shipped unbuilt (`PROVENANCE.md` names them). `lake build Solution Challenge` exits 0.

The twelve selected declarations in `Solution.lean` each depend on exactly `propext`, `Classical.choice` and
`Quot.sound` (recorded by `#print axioms` on a direct recompile of `Solution.lean`, 7 October 2026, after the
`smoothClassification` statement was strengthened to an equivalence). No module in the package contains `sorry` outside
the twelve `sorry` placeholders of `Challenge.lean`, and no module uses `native_decide` or declares an axiom.
`Challenge.lean` imports Mathlib alone. `comparator.json`, `Solution.lean` and `Challenge.lean` name the same twelve
declarations in the same order.

## Completed local checks

- Full compile of the research closure after the port (6 October 2026). The port changes are listed module by module
  in `PROVENANCE.md`: `try` guards on `dsimp`, `all_goals` guards on post-closure tactics, three removals of tactic
  steps that no longer act, one heartbeat budget, one visibility change, and one module trimmed of the registered
  theorems this package does not resubmit. No compared statement, and no research theorem the bridge invokes, was
  changed.
- The statement bridge proves every Challenge object equal to the corresponding research object — the Lorentz
  generator and field-action tables by the research module's own formula theorems
  (`PDTQuadraticSource.lorentz_formula`, `PDTQuadraticSource.field_action_formula`), all other definitions by `rfl` —
  and derives each compared statement from the research theorem it corresponds to
  (`source_classification`, `source_uniqueness`, `finite_certificate`, `conserved_source_classification`,
  `conservation_forces_hodge_invariance`, `regular_source_polynomial` + `conserved_polynomial_classification` with
  `full_smooth_conserved_family` for the converse, `smooth_zero_field_selection`,
  `differentiable_sourceful_classification`, `differentiable_normalized_selection`, and the three control declarations
  from six research control theorems).
- The original research batches (C2-059, C2-060, C2-061, C2-062, C2-063) carry their own 30 September 2026
  verification receipts on Lean 4.31.0 / Mathlib fabf563a, with 38, 42, 32, 21 and 29 independent exact checks
  respectively; those receipts and sources are preserved unchanged.
- MSC2020 codes are `15A72` (vector and tensor algebra, invariant theory), `35Q61` (Maxwell equations), `70S10`
  (symmetries and conservation laws in field theory), `78A25` (electromagnetic theory, general) and `68V20`
  (formalization of mathematics). These describe the selected mathematics and its form.
- Compiler warnings: the full build log of the three package targets (`lake build Challenge StatementBridge Solution`,
  9 October 2026, exit 0, zero errors) carries 26 warnings, recorded per file in `local-checks.json`: the 12 `sorry`
  placeholders of `Challenge.lean`, and 14 in seven inherited `GravityScreening` modules that are left untouched so
  they stay identical to the registered `pdt-hodge-lie-generation` package apart from the module header (7 Mathlib
  deprecations, 6 `tac1 <;> tac2` style suggestions, 1 unused-tactic report). Every other module compiles without a
  warning. The first build of this package carried 308 warnings in 23 files (250 unused-tactic reports, 29
  never-executed reports, 10 style suggestions, 7 deprecations, 12 `sorry`); the 15 research modules that held the
  unused-tactic and never-executed reports (216 of them in `SourceCoefficientBridge`) and the style suggestions in
  `FinitePfaffian` were cleaned by deleting the no-op tactic steps, without touching a statement or a definition and
  without disabling a linter (see `PROVENANCE.md`). The Palomar verifier (`verify_submission.py`, pipeline commit
  `65f0154e`) does not parse compiler warnings.

## Reviews run on the package (7 October 2026)

**Revision of 13 October 2026.** The five review reports below, with the blind re-derivation scripts, the
literature cross-check scripts and the seven definitions-audit tests (stored as `.lean.txt`, see
`reviews/definitions_audit_tests/README.md`), are committed under `reviews/` at this revision. The 7 October
commits cited them while `.gitignore` excluded the folder; Palomar's automated review of commit `7517011`
(13 October 2026, no blocking problems) noted that the cited records could not be checked in the pinned
repository. Three pointers to the private canon in `reviews/CALIBRATION_prose_2026-10-07.md` were replaced by
neutral wording; no other review text, and no Lean source, changed.

All five are AI reviews, recorded in `reviews/`; none is human peer review or a Palomar determination.

- Statement fidelity (referee): each of the twelve Lean statements restated and compared with the abstract, the claim
  table and the alignment block; independently checked that the 209 constraints have rank 209 with a one-dimensional
  nullspace containing the stress, that nonzero vacuum and sourced jets exist (compiled against the Challenge), that
  the six generators are a basis of so(3,1) acting identically on field and tensor, and that `J` is the Lorentzian
  Hodge star. Verdict: fix then submit; the fixes (prose stated above its content) are applied in this commit.
- Definitions audit: see `reviews/DEFINITIONS_audit_2026-10-07.md`.
- Blind re-derivation: the four classifications recomputed from scratch in exact rational arithmetic with
  independently chosen conventions; dimensions 1 (covariance and trace), 3 (covariance alone), 189 (trace alone),
  1 (conservation), 17 (degree at most two, conserved), and the sourceful coefficient forced to equal k, all agree.
- Calibration (prose above and below tier): twelve items, concentrated in the verification record; applied in this
  commit (the eight unbuilt modules, the port-change record, the fifth batch, the Kerrighan citation, the comparatives).
- Literature, second pass: see `reviews/LITSCOUT_second_pass_2026-10-07.md` and `PRIOR_WORK.md`.

## Not yet done

- The official pinned preflight (`.github/workflows/palomar-preflight.yml`) on the exact public commit, in Palomar's
  Linux sandbox with the independent kernels. Local compilation used the pinned dependency cache and is not a
  substitute. Before submission the published package must pass that workflow with zero errors.
- `local-checks.json` with source hashes, to be generated at publication.

No acceptance or public registry ID is claimed for this package. The two registered packages it builds on are unchanged.
