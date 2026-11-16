# Repeated aeons: what a splice universe remembers across many big bangs

*Exploratory note, 2026-10-31. Follow-up to [CCC_NOTE.md](CCC_NOTE.md) (open
question 2, "a crossover map"). Exact computation on small universes; an
analogy with cyclic cosmology, not a physics claim. AI assistance (Claude,
Anthropic), disclosed as elsewhere in this repo.*

## Setup

One **cycle** is an aeon followed by a new big bang:

1. **Aeon.** Run the splice rule `{(a,a),(b,c)} -> {(a,b),(c,a)}` under the
   min-successor policy until no match exists (the loop clock has run down).
2. **Big bang (reseed).** Turn edges back into loops using only the dead
   state's own shape, so nothing outside the network chooses the restart.
   Two rules, mirror images of each other under edge reversal:
   * `sink`: every non-loop edge `(u, v)` into a vertex with no outgoing
     edge becomes the loop `(v, v)`;
   * `source`: every non-loop edge `(u, v)` out of a vertex with no
     incoming edge becomes the loop `(u, u)`.

Both steps conserve the number of edges E, so the set of all states with E
edges (any vertex count, loops and multi-edges allowed, up to isomorphism) is
a finite closed universe and the cycle is a deterministic map on it. Every
starting state is followed, all equally likely.

Script: [`ccc_crossover.py`](ccc_crossover.py) (self-contained, about 7 s for
E <= 6 and about 3 minutes for E = 7). Results:
[`ccc_crossover_E6.jsonl`](ccc_crossover_E6.jsonl) and
[`ccc_crossover_E7.jsonl`](ccc_crossover_E7.jsonl) (E = 7 only). Checks
run: canonical forms invariant under random relabelings, entropy
non-increasing on every run, the two reseed rules exact mirror images under
edge reversal.

## Results

| E | states | bits at start | forgotten by 1st big bang | forgotten in total | cycles until settled | attractors | frozen share (sink / source) |
|---|---|---|---|---|---|---|---|
| 3 | 52 | 5.70 | 2.18 / 2.17 | 2.89 / 2.67 | 3 | 8 / 9 | 56% / 56% |
| 4 | 296 | 8.21 | 2.78 / 2.85 | 4.42 / 3.78 | 8 / 5 | 29 / 31 | 82% / 48% |
| 5 | 1724 | 10.75 | 3.52 / 3.70 | 5.75 / 5.51 | 7 / 6 | 86 / 93 | 94% / 34% |
| 6 | 11060 | 13.43 | 4.19 / 4.59 | 6.60 / 7.68 | 9 / 8 | 409 / 414 | 97% / 52% |
| 7 | 74527 | 16.19 | 4.80 / 5.49 | 7.19 / 10.19 | 12 / 17 | 2053 / 2056 | 99.6% / 69% |

(Two numbers in a cell are sink / source; one number means both rules agree.)

**1. Forgetting front-loads, then stops.** The first big bang erases the most
(4.2 to 4.6 bits at E = 6, 4.8 to 5.5 at E = 7); each later one erases less,
and every universe settles within 9 cycles at E = 6 (17 at E = 7). On a settled orbit the cycle map is a bijection,
so a recurring universe can no longer forget anything: what survives is only
*which* attractor it fell into (about 6 to 7 bits out of 13.4 at E = 6).

**2. Most attractors are frozen.** 398 of the roughly 410 attractors at E = 6
are states where nothing ever happens again: either no loops and no edge the
reseed rule can convert (352), or loops stranded because every other edge
touches them (46). At E = 7 it is 2036 of about 2055. The counts are
identical for both rules, as the mirror symmetry predicts.

**3. A few universes recur forever.** The rest are live: the universe
genuinely evolves in every aeon and is reborn into the same sequence of
states. At E = 6 there are 11 (sink) and 16 (source) of them, with periods 1,
2, 3 and, for `source`, one orbit of period 7 that runs through seven
distinct aeons before repeating.

**4. The restart rule decides the fate.** Under `sink`, the frozen share grows
with size (56%, 82%, 94%, 97%, 99.6% for E = 3 to 7): almost every universe
eventually suffers a heat death it cannot restart from. Under `source`, far
more keep recurring (44%, 52%, 66%, 48%, 31%), but the share has fallen for
two sizes in a row, so this rule may only delay the freeze rather than
prevent it. The splice rule is not symmetric under edge reversal, so the
same law of motion paired with mirror-image big bangs gives very different
long-run cosmologies.

## Reading it (interpretation, not result)

* A cyclic universe of this kind loses its past quickly and then stops
  losing it. "Where did our big bang come from?" has a finite, mostly
  forgotten answer: an observer inside can at best learn which recurring
  pattern they are in, not which of the many earlier histories fed it.
* The forgetting is relative to an observer who sees only structure. A
  simulator that keeps vertex labels can still rewind every splice step.
* Whether the cosmos keeps restarting depends less on the dynamics inside an
  aeon than on how the crossover reads the dead state.

## Limits

Tiny universes (E <= 7), one deterministic update policy, two hand-chosen
reseed rules, no continuum limit and nothing resembling a conformal factor.
Open next steps: other reseed rules (including random or multiway ones),
E >= 8 with a faster canonizer, and whether the falling live share under
`source` continues. For which universes recur, see the follow-up below.

## Follow-up (2026-11-15): which universes keep recurring

Script: [`ccc_live.py`](ccc_live.py) (finds every live attractor and the share
of starting states that end live, by vertex count; about 10 s for E <= 6 and
7 minutes for E = 7; `python3 ccc_live.py 7` also writes every live attractor
with its orbit to `ccc_live_E7.json`).

**What a splice does.** `{(a,a),(b,c)} -> {(a,b),(c,a)}` replaces the edge
`b -> c` by the path `c -> a -> b`: it reverses one edge and threads the loop
vertex into it. Every aeon is therefore a sequence of edge reversals, one per
loop consumed, which is one way to see why mirror-image reseeds (sinks versus
sources) do not behave alike.

**Sparse universes keep recurring; dense ones freeze.** Share of all states
with E edges that end on a live attractor, by the vertex count V of the
starting state (`source` rule unless marked):

| E | V = 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|---|---|---|---|---|---|---|---|
| 4 | 67% | 79% | 64% | 50% | 0% | | |
| 5 | 55% | 84% | 90% | 83% | 68% | 50% | 0% |
| 6 | 0.5% | 37% | 74% | 83% | 82% | 77% | 68% |
| 7 | 0% | 17% | 7% | 59% | 77% | 80% | 80% |
| 7 (`sink`) | 0% | 0% | 0% | 0.2% | 3% | 0.4% | 0% |

Under `source`, sparse starting states (average degree near 2 or below, so
trees, chains and single cycles) keep recurring at roughly 70 to 90%, while dense ones
almost all freeze, and the dense side grows as E grows. That explains the
falling overall live share in the results table (66%, 48%, 31% for E = 5, 6,
7): most states with 7 edges have V <= 7 (63,419 of 74,527), where recurrence
is rarer, while sparse universes recur as often as before. Under `sink`, no
vertex count reaches 26% for E = 4 to 7, and at E = 7 none exceeds 3%. At
E = 6, starting with more loops also lowers the live share under `source` (47%
with no loops, 24% with four, 0% with six), and so does starting with a
directed cycle (35% versus 54%).

**Live attractors.** 92 for E <= 7 across both rules (37 at E = 7). On every
one of them the vertex count stays constant around the orbit, and each aeon
fires between one and four splices before the universe dies and is reseeded.
At E = 7 the largest (`source`, period 3, 7 vertices) collects 12,518 of the
74,527 starting states and fires 2, 2 and 1 splices per aeon. The longest
period seen is 7 (E = 6, `source`).
