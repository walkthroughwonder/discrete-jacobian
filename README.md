# The Discrete Jacobian Program

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.21630926.svg)](https://doi.org/10.5281/zenodo.21630926)

Can application-level undoability coexist with a global state collision?
**Yes.** This repository contains explicit certificates, an exhaustive
bounded sweep, a Lean 4 proof of the concrete splice collision, and a
human proof of a general rigidity theorem. The latter is pending external
review and is not yet formalized in Lean.

Inspired by the July 2026 counterexample to the Jacobian conjecture
(local invertibility everywhere, global 3-to-1 collision), this project
asks the analogous question for Wolfram-model-style hypergraph rewriting
and answers it with the **splice collision**:

    rule   {(a,a), (b,c)}  →  {(a,b), (c,a)}     "splice a loop into an edge"

    S₁ = {(0,0),(1,2),(1,3)}  (loop ⊔ out-star)  ─┐
                                                  ├─→  the directed 4-path
    S₂ = {(0,0),(1,2),(3,2)}  (loop ⊔ in-star)   ─┘

The rule preserves edge and matched-vertex counts and passes the declared
semantic-D1 probe on states with at most 4 vertices and 3 edges. All four
displayed applications have isomorphic successors (no policy involved),
yet the two non-isomorphic sources collide. Their unconditional mutual
unreachability has a hand proof. No unbounded semantic-D1 proof is claimed.
The image forgets which vertex carried the loop: **the forgotten match is
the discrete monodromy.**

## Status

⚠️ **Public research-software working draft.** The concrete splice
collision is machine-checked and the certificates are independently
replayed, but the project has not undergone external peer review. Semantic
D1 and sweep statistics are bounded empirical results. The general
rigidity theorem currently has a human-readable proof pending external or
generic Lean review. AI assistance is disclosed in the working draft.

## Key artifacts

| File | What it is |
|---|---|
| [NOTE_DRAFT.md](NOTE_DRAFT.md) | The write-up (draft) |
| [PROOF_flagship.md](PROOF_flagship.md) | Hand proof of the splice collision |
| [lean/SpliceCollision.lean](lean/SpliceCollision.lean) | Lean 4 proof of concrete non-isomorphism, collision, successor-class agreement, and S1-successor terminality; zero `sorry`s |
| [PROOF_rigidity.md](PROOF_rigidity.md) | General rigidity theorem and hand proof, pending external review |
| [RESULTS.md](RESULTS.md) | Full findings incl. sweep statistics and stress tiers |
| [DEFINITIONS.md](DEFINITIONS.md) | The definitional framework (D1 grades, collision classes, history ambiguity) |
| [ADVERSARIAL_REVIEW.md](ADVERSARIAL_REVIEW.md) | Six attacks on our own claims, and what survived |
| [POSITIONING.md](POSITIONING.md) | Relation to Arrighi et al. (CGD, space-time reversible rewriting) |
| [phase1/](phase1) | Searcher, independent verifier (self-tested), sweep logs, 15 certificate filenames / 14 unique contents |

## Headline numbers (tier-stamped; "in range" claims only)

- 489 rules enumerated → 238 non-identity survivors of the semantic-D1
  probe over every enumerated state with ≤4 vertices and ≤3 edges.
- 52 of those probe survivors collide at (≤4 vertices, ≤3 edges); **182**
  at (≤4, ≤4).
- History ambiguity is necessary for collision in every tier tested
  (zero exceptions); exactly one rule is unambiguous at (4,4) — and rigid.
- 13 distinct R1 certificates plus the byte-identical `cert_flagship.json`
  alias, and 1 R2 two-step-path certificate, all confirmed by an
  independently implemented verifier. The R2 artifact certifies its
  displayed paths, not minimum merge depth; its seeds also share a one-step
  successor.

## Reproduce

```bash
python3 phase1/test_sanity.py
python3 phase1/verify_independent.py phase1/cert_flagship.json
python3 phase1/verify_independent.py phase1/cert_deep_r2.json
```

For the pinned single-core Lean and full-certificate commands, see
[REPRODUCIBILITY.md](REPRODUCIBILITY.md). The full sweep is optional and
substantially more expensive than the release verification gate.

## License

MIT (see LICENSE). To cite this work, use the Zenodo DOI:
[10.5281/zenodo.21630926](https://doi.org/10.5281/zenodo.21630926)
(all versions; v1.0.0 specifically is 10.5281/zenodo.21630927).
