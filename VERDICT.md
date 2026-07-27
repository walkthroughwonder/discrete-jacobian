# VERDICT — Phase 0 go/no-go (2026-07-26)

## Decision: **GO**, with two reading obligations before any novelty claim.

## Basis

The question pair at the heart of the program appears genuinely open:

1. **Q1/Q2 (discrete Jacobian):** no literature found that asks whether
   locally invertible rewriting (any of D1/D2/D3) forces global injectivity —
   let alone exhibits a counterexample. The nearby schools all run the
   opposite direction: Arrighi et al. derive local structure FROM global
   invertibility (CGD 2015–2020) or engineer sufficient conditions FOR
   reversibility (space-time reversible rewriting 2025); SDCA constructs
   reversible variants by memory tricks. The rigidity question is unasked.
2. **Q4 (Garden of Eden for dynamic topology):** GoE theory is being actively
   generalized (non-uniform CA 2023–25, Smale spaces 2025) but always on
   frozen geometry. No GoE/surjunctivity/pre-injectivity statement for graph
   or hypergraph rewriting surfaced under direct search.

## Obligations attached to the GO

1. **Read in full: [arXiv:2510.03296](https://arxiv.org/abs/2510.03296)**
   (*Space-time reversible graph rewriting*, Arrighi–Costes–Maignan). Its
   "nearby cuts mutually determine each other" notion may overlap D1. Two
   outcomes, both fine: if their sufficient conditions are close to D1, our
   Q1 search becomes a **sharpness probe of their theorem** (a found
   collision = their conditions are not necessary; publishable connection);
   if far, our lane is clear. Check their open-questions section explicitly
   for GoE-type statements.
2. **Read in full: the Natural Computing 2020 CGD paper** for the exact
   invertibility/vertex-preservation statements, so T1 (frozen-topology
   reduction) cites them correctly and Q3's "dynamic class" boundary is drawn
   where their theorems actually stop.

## Refined main conjecture (what Phase 2 hunts, what Phase 3 attacks)

> **Discrete Jacobian Question.** Is there a D1-invertible rule set whose
> multiway system has a merge with distinct ancestry (R2), or whose
> canonical-policy evolution collides (R1)? Equivalently: does the
> branched-cover mechanism of the ℂ³ counterexample have a finite,
> certificate-checkable analogue in hypergraph rewriting?

Betting note (honest prior): DPO's per-application undoability makes me
suspect R1 collisions under D1 alone are FINDABLE (the policy forgets the
match — that is real information loss), while D1 ∧ D3 ∧ D2-closed may be
rigid at small scale. That asymmetry, if it holds, is itself the first
result: it locates the discrete Jacobian phenomenon precisely in the gap
between application-reversibility and census-reversibility.

## Phase 0 exit-criteria status

| Criterion | Status |
|---|---|
| Primary definition chosen | ✅ D1 primary, D3 secondary hypothesis, D2 for Q4 (DEFINITIONS.md) |
| Toy example + non-example, hand-verified | ✅ edge-reversal / endpoint-merge / pendant-creation (DEFINITIONS.md) |
| Near-miss triviality guards | ✅ four degenerate collision classes excluded (DEFINITIONS.md) |
| Prior-art sweep | ✅ PRIOR_ART.md; two ⚠ full-reads outstanding |
| Question confirmed open | ✅ modulo the two ⚠ reads |

## Next (Phase 1 gate)

Phase 1 infrastructure may start now; the two ⚠ reads must complete before
any Phase 4 write-up claims novelty. First Phase 1 deliverable: canonical
hypergraph hashing + the round-trip planted-collision test.
