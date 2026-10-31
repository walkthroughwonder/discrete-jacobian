# The splice rule as a toy "aeon": a note on Penrose's CCC

*Exploratory note, 2026-10-30. Analogy plus small exact computations; not a
physics claim. AI assistance (Claude, Anthropic), disclosed as elsewhere in
this repo.*

Discussion: [Wolfram Community thread](https://community.wolfram.com/t/a-locally-invertible-hypergraph-rule-as-a-toy-model-of-information-loss-in-conformal-cyclic-cosmology/28448).

## Why CCC is relevant at all

Penrose's Conformal Cyclic Cosmology (CCC) glues the conformal infinity of one
aeon to the Big Bang of the next. For the second law to survive the cycle,
the late universe must have effectively *less* phase space than the early
one, so the entropy count can restart. Penrose places that loss in black hole
evaporation, and the crossover itself works because a universe containing only
massless fields has no clocks and therefore forgets its scale.

The splice collision has the same logical shape:

| CCC | Splice rule |
|---|---|
| Physics locally reversible | Every application uniquely undoable at its comatch (D1) |
| Global information loss over an aeon | Distinct states merge (flagship: loop + out-star, loop + in-star) |
| Loss appears once scale is forgotten (conformal identification) | Loss appears only on isomorphism classes, once labels are forgotten |
| Massive particles act as clocks; they decay away | Loops are consumed one per step and never created |
| Late epoch: massless, clockless, nothing left to happen | Terminal states: no match, evolution halts (typically loop-free) |

The last two rows are not decoration. Because matching is injective,
`b != c`, so the rule destroys exactly one loop per application and creates
none. Every evolution therefore halts within at most L steps (L = number of
loops). It halts early only if loops are *stranded*: every remaining non-loop
edge touches the vertex of every remaining loop, so no match exists. Vertex
and edge counts are conserved, so each (V, E) sector is a finite closed
universe with a guaranteed terminal epoch.

Stranded endings become rare as systems grow. Fraction of evolving states
whose evolution runs all L steps to a loop-free state (min-successor policy):
1 of 5 at E = 2, 15 of 28 (54%) at E = 3, 126 of 166 (76%) at E = 4,
914 of 1036 (88%) at E = 5, 6473 of 6849 (94.5%) at E = 6. (An earlier version
of this note wrongly stated that every evolution ends loop-free; the
information-loss measurements below never relied on that claim.)

## The measurement

For each sector, take every state that can evolve (at least one loop),
uniformly, and ask how much of it the terminal state still remembers:

    bits lost = log2(#initial states) - H(final state)

Two versions:

1. **Policy-free (multiway).** `T(S)` = all terminal states reachable from S
   under every match order. Measure loss on states where `|T(S)| = 1`.
2. **Deterministic.** Min-successor policy (lexicographically minimal
   canonical successor) applied to every evolving state.

Script: [`phase1/ccc_compression.py`](phase1/ccc_compression.py) (policy-free,
plus confluence counts) and
[`phase1/ccc_policy_fmin.py`](phase1/ccc_policy_fmin.py) (deterministic).
Exhaustive over all binary-edge states (loops and multi-edges allowed) with
E <= 6 edges, every vertex count. Runtime about 7 s.

Canonical forms in these scripts permute vertices only within classes of equal
(out, in, loop) degree, a valid canonical form but a different total order
from `core.canonical`. The policy-free numbers do not depend on that order;
the deterministic numbers describe *a* min-successor policy, not necessarily
the identical one used in RESULTS.md.

A Wolfram Language implementation written from scratch
([`wolfram/SpliceAeon.nb`](wolfram/SpliceAeon.nb), [`wolfram/SpliceAeon.wl`](wolfram/SpliceAeon.wl))
reproduces every sector exactly for E <= 5, including the termination
property and the loop-free fractions.

Independent check: the flagship collision (S1 not isomorphic to S2, both with
a unique successor class, that class being the directed 4-path) was re-derived
from scratch in Wolfram Language with `CanonicalGraph`.

## Results

**Deterministic policy, all evolving states, peak sector per edge count:**

| E | densest-loss sector (V) | states with a loop | distinct endpoints | max fiber | bits lost |
|---|---|---|---|---|---|
| 3 | 4 | 6 | 4 | 2 | 0.67 |
| 4 | 4 | 63 | 30 | 6 | 1.28 |
| 5 | 4 | 337 | 100 | 10 | 2.04 |
| 6 | 4 | 1432 | 304 | 17 | 2.67 |

Loss grows steadily with universe size (roughly 0.65 bits per added edge in
range), and the largest fiber in the peak sector grows from 2 to 17. By E = 6, the end state of a
typical evolution is compatible with about 2^2.67, so roughly 6, different
beginnings.

**Policy-free version** shows the same growth on the confluent subset (for
V = 3: 0.46, 1.20, 1.59, 1.90 bits for E = 3..6).

**Two sharp side findings:**

- **Rigid sectors.** Every V = 2 sector loses exactly zero bits, at every E
  tested. Too little room for a forgotten match. (Natural test case for the
  rigidity conjecture: a full proof here should be easy.)
- **The heat death is not unique.** Large fractions of states have more than
  one possible terminal state depending on match order, e.g. 1929 of 3353
  states in sector (E = 6, V = 5). The rule is not causally invariant on these
  sectors, so the "final aeon state" is fixed only once an ordering is chosen.
  In CCC terms, the crossover surface would depend on foliation.

## What this does and does not show

It shows that the splice rule realizes, exactly and checkably, the abstract
structure CCC relies on: local reversibility, a monotone "clock" that runs
down, a terminal epoch where nothing can happen, and global information loss
that grows with system size.

It does not show anything about actual cosmology. Wolfram models lack a proven
continuum limit; there is no hypergraph analogue of a conformal factor yet;
and the loss mechanism here (relabeling symmetry) is not black hole
evaporation.

## Open questions this suggests

1. **Scaling.** Does bits-lost per sector grow linearly in E, and does the
   peak stay at small V? Pushing to E = 7, 8 needs a faster canonizer (nauty).
2. **A crossover map.** Define a "next aeon" map that reseeds loops onto a
   loop-free terminal state using only that state's own data. Does the
   resulting cyclic dynamics have a well-defined entropy per cycle?
   *Done: see [CCC_CROSSOVER.md](CCC_CROSSOVER.md). Forgetting is front-loaded
   and stops within 9 cycles at E <= 6; most universes freeze, and the reseed
   rule decides how many keep recurring.*
3. **Scale-forgetting quotient.** Identify hypergraphs up to edge subdivision
   (a crude conformal rescaling). Do D1 rules that are rigid on isomorphism
   classes start colliding under this coarser quotient?
4. **Ambiguity link.** Does history ambiguity (DEFINITIONS.md, D-IA) predict
   which sectors lose information, as it predicts collision in RESULTS.md?
