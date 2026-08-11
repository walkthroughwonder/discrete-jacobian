# The Discrete Jacobian Program

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.21630926.svg)](https://doi.org/10.5281/zenodo.21630926)

Can a locally invertible rewrite rule fail to be globally injective?
**Yes** — and this repository contains the explicit certificates, an
exhaustive small-scale sweep, a machine-checked Lean 4 proof, and the
rigidity conjecture the data points to.

Inspired by the July 2026 counterexample to the Jacobian conjecture
(local invertibility everywhere, global 3-to-1 collision), this project
asks the analogous question for Wolfram-model-style hypergraph rewriting
and answers it with the **splice collision**:

    rule   {(a,a), (b,c)}  →  {(a,b), (c,a)}     "splice a loop into an edge"

    S₁ = {(0,0),(1,2),(1,3)}  (loop ⊔ out-star)  ─┐
                                                  ├─→  the directed 4-path
    S₂ = {(0,0),(1,2),(3,2)}  (loop ⊔ in-star)   ─┘

Edge- and vertex-count preserving, every application uniquely undoable at
its comatch, unique successor up to isomorphism (no policy involved) — and
the two non-isomorphic, mutually-unreachable states evolve to the same
state. The image forgets which vertex carried the loop: **the forgotten
match is the discrete monodromy.**

## Status

⚠️ **Internal research draft.** Results are machine-verified but have not
undergone external peer review. The note (NOTE_DRAFT.md) is a working
draft. AI assistance (Claude, Anthropic) throughout, disclosed.

## Key artifacts

| File | What it is |
|---|---|
| [NOTE_DRAFT.md](NOTE_DRAFT.md) | The write-up (draft) |
| [PROOF_flagship.md](PROOF_flagship.md) | Hand proof of the splice collision |
| [lean/SpliceCollision.lean](lean/SpliceCollision.lean) | Lean 4 proof, compiles against Mathlib with zero sorries |
| [RESULTS.md](RESULTS.md) | Full findings incl. sweep statistics and stress tiers |
| [DEFINITIONS.md](DEFINITIONS.md) | The definitional framework (D1 grades, collision classes, history ambiguity) |
| [ADVERSARIAL_REVIEW.md](ADVERSARIAL_REVIEW.md) | Six attacks on our own claims, and what survived |
| [POSITIONING.md](POSITIONING.md) | Relation to Arrighi et al. (CGD, space-time reversible rewriting) |
| [phase1/](phase1) | Searcher, independent verifier (self-tested), sweep logs, 14 certificates |

## Headline numbers (tier-stamped; "in range" claims only)

- 489 rules enumerated → 238 semantically locally-invertible survivors.
- 52 collide at (≤4 vertices, ≤3 edges); **182** at (≤4, ≤4).
- History ambiguity is necessary for collision in every tier tested
  (zero exceptions); exactly one rule is unambiguous at (4,4) — and rigid.
- 13 R1 certificates + 1 deep R2 (multiway) certificate, all confirmed by
  an independently-implemented verifier. (The deep R2 certificate was
  re-issued 2026-08-11: a CR11 audit found the original reducible to a
  one-step merge; the replacement is verified with explicit
  earliest-intersection deepness checks.)

## Reproduce

```
cd phase1
python test_sanity.py          # engine sanity + planted-collision round trip
python verify_independent.py cert_flagship.json
python maxsweep.py             # full 3-stage sweep (~5 min on 14 cores)
```

These commands do not overwrite the committed evidence. `maxsweep.py`,
`sweep_phase2.py`, and `search.py` write to a `.rerun` sibling when their
default output already exists, so a rerun produces
`maxsweep_log.rerun.jsonl` alongside the original for comparison. Pass
`--out PATH` to choose a destination, or `--force` to overwrite
deliberately. `phase1/maxsweep_log.jsonl` in particular is pinned by
SHA-256 from `discrete-jacobian-research`
(`scripts/audit_finite_prefix_obstruction.py`), so overwriting it breaks an
audit in the other repository.

The Lean proof builds against the pinned environment in lean/ (Lean 4 v4.33.0-rc2, Mathlib 3dd956ad — committed lake-manifest.json):
`cd lean && lake exe cache get && lake build`.

## License

MIT (see LICENSE). To cite this work, use the Zenodo DOI:
[10.5281/zenodo.21630926](https://doi.org/10.5281/zenodo.21630926)
(all versions; v1.0.0 specifically is 10.5281/zenodo.21630927).
