# Q5 resolved in strata: census artifacts, policy relativity, and a two-rule hard core

*2026-08-03, evening session. Machine-checked by direct recomputation at
the stated tiers; example pairs independence-verified (bounded BFS, both
directions); NOT yet independently re-verified — the verifier speaks
only min-successor certificates, and extending it is the required next
infrastructure step before external claims. Data:
`phase1/q5_deep_5_5.jsonl`, `phase1/q5_deep_6_4.jsonl`, plus the inline
f_max experiment (§2).*

## 0. Outcome in one paragraph

Q5 asked whether min-successor shielding of the 12 D-IA frontier rules
persists at all tiers. Answer: **for the seven 2→2 rules, no — they
collide under f_min at the (5,5) census** (11–31 genuine images each;
example pairs verified INDEPENDENT). Their "ambiguous-but-rigid" status
was a census-bound artifact, and the forcing direction of the dichotomy
("independent ambiguity ⟹ eventual collision") is CONFIRMED for them.
The five edge-growers stay min-rigid through (5,5) and (6,4) — but
**three of the five collide under the equally-canonical max-successor
policy at (4,4)**, so their rigidity is policy-relative. The
irreducible core is **two rules**: the fresh-vertex pendant growers
{(a,b)} → {(a,b),(b,c)} and {(a,b)} → {(a,b),(c,a)}, rigid under BOTH
policies at every tier tested.

## 1. The three strata

| stratum | rules | f_min | f_max (4,4) | verdict |
|---|---|---|---|---|
| eventual colliders | all seven 2→2 rules | **collide at (5,5)** | 3 of 7 collide | dichotomy's forcing direction holds; holdout status was census-bound |
| policy-relative | {(a,b)}→{(a,a),(a,b)}, {(a,b)}→{(a,b),(b,b)}, {(a,b)}→{(a,b),(a,b)} | rigid ≤(5,5),(6,4) | **collide** (22/22/16 images) | merges are policy-realizable; min-coherence open |
| hard core *(dissolved same night — see below)* | {(a,b)}→{(a,b),(b,c)}, {(a,b)}→{(a,b),(c,a)} | rigid ≤(6,5),(5,6) | rigid at (4,4)–(6,4); **collides at (6,5),(5,6)** | max breaks at richer censuses (certified); min-coherence survives |

**Postscript (same night).** The hard-core stress broke the last two
rules under f_max at (6,5)/(5,6) — four representative pairs certified
and independently verified (`q5cert_pendmax_*.json`). Final tally:
**12/12 frontier rules have genuine, independently verified policy
collisions under {min, max}**; the policy-existential dichotomy (Q5b)
is answered YES across the board, and "ambiguous-but-rigid" has fully
dissolved into census bounds + policy choice. The sole surviving
rigidity is f_min on the five growers (six censuses, zero collisions) —
now the **min-coherence of growth** conjecture, with two proven
structural lemmas behind it (PENDANT_COHERENCE.md: pendant-free
rigidity; core conservation).

(5,5) census = 1603 states; (6,4) = 356; genuineness = the sweep's
orbit quarantine, and each rule's example pair was additionally checked
mutually unreachable in both directions.

## 2. The max-policy experiment

f_max = lexicographically maximal canonical successor: isomorphism-
invariant, on exactly the same footing as f_min. At (4,4) it realizes
genuine collisions for 6 of the 12 rules — three 2→2 rules and the
three loop/doubling growers (the latter spectacularly: 22, 22, 16
images) — including the exact D-IA pairs that f_min shields — e.g. the add-loop-at-tail grower realizes
S = {(0,0),(0,0),(0,1),(1,0)}, P = {(0,0),(0,1),(1,0),(1,1)} onto their
shared image, the pair recorded in WITNESS_ANALYSIS's own example
field.

Union over the two policies tested: **10 of 12 frontier rules have a
genuine policy collision**; only the two pendant growers resist both.

## 3. The observed shielding mechanism (why min held as long as it did)

In every inspected shielded pair, F(P) = T is forced (succ(P) tiny)
while S owns a second successor sorting canonically BELOW T — min
always finds S a smaller exit. Dually, f_max finds S a LARGER exit —
which is why max realizes merges that min shields, and vice versa is
not observed (T tends to sit at the top of P's successor set in these
examples). Shielding is an order-statistic accident, not a rewriting
property — except possibly for the hard core (§5).

## 4. A guardrail on Q5b (policy-existential formulations)

"Does D-IA force collision under SOME iso-invariant policy?" is TRIVIAL
if arbitrary per-class choice functions count as policies: pick
π(S) = π(P) = T by fiat. The meaningful question quantifies over
CANONICAL policies (uniform order statistics of the canonical successor
set: min, max, k-th, and definable refinements). Under {min, max} the
answer is yes for 10 of 12; the hard core resists both extremes.

## 5. The hard core conjecture

Both hard-core rules add an edge to a FRESH vertex — the only two
frontier rules whose added feature touches an anonymous vertex. The
added pendant is structurally identical at every application site, so
the image determines the multiset of pendant-deletions symmetrically —
plausibly making EVERY canonical order-statistic policy coherent
(injective). **Conjecture (pendant coherence):** for the two pendant
growers, every canonical policy is injective on isomorphism classes;
the successor relation merges (274+ certified D-IA pairs) but no
canonical policy ever realizes one. If true, these two rules witness
the relation/policy gap in its purest form — global information loss
visible in the multiway structure yet invisible to every deterministic
canonical evolution. Attack: characterize min/max-successors of
pendant-growth explicitly (the added pendant's location in the
canonical form) and prove the inversion map well-defined.

## 6. Verification status

1. ~~Extend `verify_independent.py` with a policy parameter~~ **DONE
   2026-08-03**: policy dispatch (min/max) plus a NEW verifier-side
   bounded independence check (its own BFS via `one_step_images` +
   `decode`), activated by an `independence_bounds` certificate field.
2. ~~Certify the collisions~~ **DONE**: 13 certificates
   (`q5cert_min55_*.json` × 7, `q5cert_max44_*.json` × 6 — complete
   coverage of every colliding rule under each policy), each carrying
   policy, tier, and independence bounds. **All 13 CONFIRMED by the
   independent verifier**, including its own both-direction
   unreachability check. Legacy regressions (cert_flagship,
   cert_deep_r2, test_sanity) still pass. [CR11 note 2026-08-11:
   cert_deep_r2.json was re-issued after an audit refuted the 07-27
   original; the regression passes against the regenerated certificate.]
3. OPEN: stress the two-rule hard core at (6,5)/(5,6) under both
   policies; attempt the pendant coherence proof.
4. All claims tier-stamped; nothing here exceeds its stated census.
