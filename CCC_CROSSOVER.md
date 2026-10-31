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
E <= 6). Results: [`ccc_crossover_E6.jsonl`](ccc_crossover_E6.jsonl). Checks
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

(Two numbers in a cell are sink / source; one number means both rules agree.)

**1. Forgetting front-loads, then stops.** The first big bang erases the most
(4.2 to 4.6 bits at E = 6); each later one erases less, and within 9 cycles
every universe has settled. On a settled orbit the cycle map is a bijection,
so a recurring universe can no longer forget anything: what survives is only
*which* attractor it fell into (about 6 to 7 bits out of 13.4 at E = 6).

**2. Most attractors are frozen.** 398 of the roughly 410 attractors at E = 6
are states where nothing ever happens again: either no loops and no edge the
reseed rule can convert (352), or loops stranded because every other edge
touches them (46). The counts are identical for both rules, as the mirror
symmetry predicts.

**3. A few universes recur forever.** The rest are live: the universe
genuinely evolves in every aeon and is reborn into the same sequence of
states. At E = 6 there are 11 (sink) and 16 (source) of them, with periods 1,
2, 3 and, for `source`, one orbit of period 7 that runs through seven
distinct aeons before repeating.

**4. The restart rule decides the fate.** Under `sink`, the frozen share grows
with size (56%, 82%, 94%, 97%): almost every universe eventually suffers a
heat death it cannot restart from. Under `source`, roughly half keep
recurring. The splice rule is not symmetric under edge reversal, so the
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

Tiny universes (E <= 6), one deterministic update policy, two hand-chosen
reseed rules, no continuum limit and nothing resembling a conformal factor.
Open next steps: other reseed rules (including random or multiway ones),
larger E with a faster canonizer, and whether live attractors share a
structural signature.
