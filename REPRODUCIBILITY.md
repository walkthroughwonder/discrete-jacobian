# Reproducibility

This release has two evidence layers. The Python layer replays the search
engine and finite certificates. The Lean layer checks the concrete splice
theorems in `lean/SpliceCollision.lean`: source non-isomorphism,
successor-class agreement, collision, and S1-successor terminality. It does
not formalize symmetric terminality, mutual unreachability, the semantic D1
definition, or the general rigidity theorem.

## Pinned environment

- Python: tested with CPython 3.9.6; the release scripts use only the
  standard library.
- Lean: `leanprover/lean4:v4.33.0-rc2`.
- Mathlib commit: `3dd956ad3d5bc5dbf49ed1875f430add38a742ca`.

## Release gate

Run from the repository root:

```bash
python3 phase1/test_sanity.py

for cert in phase1/cert_*.json; do
  python3 phase1/verify_independent.py "$cert"
done

lake env lean --version
lake exe cache get
lake env lean -j1 -M4096 lean/SpliceCollision.lean
lake build DiscreteJacobian
```

The single-core Lean elaboration avoids consuming all available cores. The
15 `cert_*.json` filenames contain 13 distinct R1 certificates because
`cert_flagship.json` is a byte-identical alias of `cert_9.json`, plus one
R2 path certificate.

## Claim boundary

- The R1 certificates and their policy calculations are finite artifacts.
- Semantic D1, ambiguity, reachability separation, and sweep counts are
  explicitly bounded by the probe parameters in their scripts/logs.
- `cert_deep_r2.json` independently certifies the legality and convergence
  of its displayed two-step paths. It does not prove those paths are
  shortest, and its seeds also share a one-step successor.
- `PROOF_rigidity.md` is a hand theorem conditional on exact semantic D1,
  exact history-unambiguity, correct own-comatch reversal, and
  isomorphism-equivariant matching/application. It is pending external
  review and generic Lean formalization.

## Optional exhaustive sweep

`python3 phase1/maxsweep.py` reproduces the three-stage bounded experiment.
It is not required for the compact release gate and may use substantial CPU;
inspect its worker settings before running on a shared machine.
