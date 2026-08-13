# v1.1.0 — Rigidity theorem and corrected evidence boundary

This research-software release preserves the concrete splice result while
making the scope of every evidence layer explicit.

## Added

- `PROOF_rigidity.md`: an elementary hand proof that semantic local
  invertibility plus history-unambiguity implies injective one-step
  evolution on graph-isomorphism classes.
- `CITATION.cff`, a changelog, a pinned Lean/Mathlib project, and a compact
  release verification guide.
- `WOLFRAM_POST.md`, a draft public exposition.

## Corrected

- `cert_deep_r2.json` is now described as a two-step-path certificate. Its
  displayed steps replay independently, but its seeds share a one-step
  successor, so it does not establish minimum merge depth.
- Lean claims are limited to the properties formalized in
  `lean/SpliceCollision.lean`: source non-isomorphism, successor-class
  agreement, the collision, and S1-successor terminality. The symmetric
  terminality and mutual-unreachability arguments are hand proofs.
- Semantic D1, ambiguity classifications, reachability separation, and
  census statistics remain explicitly bounded by their probe parameters.

## Review status

The concrete Lean file compiles with zero `sorry`s against the pinned
toolchain. The general rigidity theorem has a human-readable proof but is
not yet externally peer reviewed or formalized in generic Lean
infrastructure. Its converse remains open. “Discrete Jacobian” is an
analogy; this release makes no claim about the classical polynomial
Jacobian conjecture.

AI assistance from Anthropic Claude and OpenAI Codex is disclosed. Edwin
Rosero is the release creator. No private research repository is included.
