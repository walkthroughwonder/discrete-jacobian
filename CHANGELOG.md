# Changelog

All notable release changes are recorded here.

## [1.1.0] - 2026-08-12

### Added

- A human-readable rigidity theorem: semantic D1 plus
  history-unambiguity implies injective one-step evolution on isomorphism
  classes (`PROOF_rigidity.md`). The proof is pending external or generic
  Lean review.
- Machine-readable citation metadata (`CITATION.cff`).
- A pinned Lean/Mathlib project and reproducibility guide.
- A Wolfram Community post draft.

### Corrected

- Reclassified `cert_deep_r2.json` as a certificate of the two displayed
  two-step paths, not a certificate of minimum merge depth. The two seeds
  also have a common one-step successor.
- Limited Lean claims to what `lean/SpliceCollision.lean` actually proves:
  the concrete collision, source non-isomorphism, agreement of successor
  isomorphism classes, and S1-successor terminality. Symmetric terminality
  and mutual unreachability remain hand arguments; semantic D1 remains
  bounded sweep evidence.
- Replaced stale references to the rigidity result as a conjecture.

## [1.0.0] - 2026-07-27

- First public research-software release: splice collision, 13 distinct R1
  certificates plus a byte-identical flagship alias, one R2 path
  certificate, sweep logs, and the concrete Lean formalization.
- Archived at DOI `10.5281/zenodo.21630927`; all-version concept DOI
  `10.5281/zenodo.21630926`.
