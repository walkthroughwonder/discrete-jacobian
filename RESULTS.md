# RESULTS — Discrete Jacobian Program (first findings, 2026-07-26)

## Headline (internal claim, pre-external-review)

**Fully census-preserving (edge- AND vertex-preserving), semantically
locally-invertible rewrite rules exist whose one-step evolution is
non-injective on isomorphism classes — with policy-independent collisions
between unconditionally mutually-unreachable states.** The D3-strict
rigidity hypothesis is FALSE: 18 of 105 fully census-preserving semantic-D1
rules collide, 12 of those collisions are also policy-independent, and the
phenomenon does not even require loops-to-fresh-vertices (loop-free pure
rewiring examples exist, e.g. cert_d3strict.json).

## THE flagship (cert_flagship.json) — maximal strength on every axis

Rule (**splice**): `{(a,a), (b,c)} → {(a,b), (c,a)}` — "splice the loop at
a into the edge b→c, giving c→a→b." Census-preserving on both counts, no
fresh vertices, semantic-D1.

    S1 = {(0,0), (1,2), (1,3)}   loop ⊔ out-star     ─┐
                                                      ├─→  P₄ (directed path)
    S2 = {(0,0), (1,2), (3,2)}   loop ⊔ in-star      ─┘

All four concrete applications (two per state) yield directed 4-paths —
unique successor up to iso, so the collision is POLICY-INDEPENDENT. S1 ≇ S2
(out-degree invariant). Successors contain no loop, so they are terminal:
mutual unreachability is UNCONDITIONAL (hand argument, no BFS bounds).
Full proof: PROOF_flagship.md. Lean formalization: lean/SpliceCollision.lean
(theorem `splice_collision` + `succ_S1_terminal`) — **compiles with zero
sorries against Mathlib (verified 2026-07-26)**: the collision, the
non-isomorphism, the successor-uniqueness-up-to-iso, and terminality are
all machine-checked.

The mechanism, sharpened: the P₄ image does not remember WHICH interior
vertex was the spliced loop. Two distinct (state, match) histories produce
isomorphic results; the forgotten match is the discrete monodromy.

## Secondary example (cert_0)

Rule (count-preserving, semantic-D1):

    {(a,a), (a,b)}  →  {(a,b), (c,c)}      (c fresh)

"A loop anchored at a vertex with an outgoing edge detaches and re-anchors
at a fresh vertex."

Colliding states (canonical, mutually unreachable, non-isomorphic):

    S  =  {(0,0), (0,1), (1,2)}     loop at the START of a 2-path
    S' =  {(0,0), (0,1), (2,0)}     loop at the MIDDLE of a 2-path

Both have exactly one applicable match, and both evolve to the same state:

    F(S) = F(S') = {(0,0), (1,2), (2,3)}    (2-path + isolated loop)

## The mechanism: anchor-forgetting

Locally the application is fully invertible: the reverse rule applied at the
comatch uniquely restores the loop to its anchor. Globally the information
"which vertex of the path carried the loop" is destroyed, because the loop —
the only marker distinguishing the anchor — moves to an *anonymous fresh
vertex*. The comatch knows the anchor; the state does not. This is exactly
the discrete form of the program's slogan (the successor forgets the match =
monodromy), realized by fresh-vertex anonymity rather than branched covering.

Structural notes:

- In the images, the rule can never fire again (the loop sits on an isolated
  vertex, which has no outgoing edge), so each colliding state's forward set
  is exactly {image}: mutual unreachability holds *unconditionally* here, not
  just within BFS bounds. (Hand argument; should be written out formally.)
- The rule is edge-count-preserving (2 → 2) — the nearest discrete analogue
  of constant Jacobian available in our census sense. It is not
  vertex-count-preserving (+1 fresh, −0; the old anchor keeps its edge).

## Sweep statistics (all bounds explicit; "in range" claims only)

- 489 enumerated rules (classes A, B, B+) → 238 semantic-D1 non-identity
  survivors → **52 rules with genuine R1 collisions** at (≤4 vertices,
  ≤3 edges); 77 INDEPENDENT pairs, 32 from count-preserving rules.
- 1,041 of 1,770 two-rule systems collide (largest: 12 independent pairs).
- 87 of 226 systems show R2 multiway merges of mutually-unreachable seeds.
- Rules failing semantic D1 while passing syntactic D1 exist (chain-step:
  12 violating probe states) — the semantic gate is doing real work.

## Verification trail

- Searcher and verifier are separate implementations; the verifier REJECTED
  all 12 certificates on first run — caused by a double-relabeling bug in
  the *verifier's* canonical form, found and fixed (with new unit tests)
  on 2026-07-26. After the fix: 12/12 CONFIRMED, planted regression intact.
  Lesson recorded: a passing round-trip test can pass by coincidence; the
  verifier needs self-tests too.

## Caveats before any external claim

1. **Definition-relative.** "Locally invertible" = semantic D1 (result-side
   uniqueness at the comatch). A skeptic may argue the rule "moves" content
   and D1 should forbid fresh-vertex re-anchoring; the write-up must defend
   the definition (or present the result as: HERE is the exact definitional
   boundary where discrete local-global rigidity fails).
2. ~~Reading obligations outstanding~~ BOTH DISCHARGED: arXiv:2510.03296
   via POSITIONING.md (novelty gate passed, N3), and the Natural
   Computing 2020 CGD paper via CGD_BOUNDARY_NOTE.md (2026-08-03; the
   frozen line confirmed — local invertibility unasked in their
   framework, no GoE statement for dynamic topology exists there).
3. ~~Vertex count is not preserved~~ RESOLVED: D3-strict collisions exist
   (18 rules), including loop-free pure rewiring and policy-independent
   instances. The "anonymity needs fresh room" hypothesis is refuted; the
   splice flagship shows anonymity can hide in graph symmetry itself.
4. All sweeps bounded; the splice and cert_0 flagships lift their bounds by
   hand (terminal successors); other certificates remain bounds-relative.

## Next steps

- ~~N1: hand proof~~ DONE: PROOF_flagship.md (splice), plus Lean
  formalization lean/SpliceCollision.lean (compiling as of this writing).
- ~~N2: D3-strict sweep~~ DONE via log query: phenomenon survives, 18/105.
- ~~N3~~ DONE (POSITIONING.md): novelty gate PASSED. Arrighi–Costes–Maignan's
  sufficient conditions rest on context-preservation + DAG assumptions that
  exclude splice-type rules — our certificates are sharpness witnesses for
  their hypotheses ("drop context-preservation and reversibility MUST fail,
  even census-preservingly"). CGD line assumes global reversibility and
  derives local structure — our converse. Garden-of-Eden for dynamic
  topology confirmed unclaimed in both. Residual: skim CGD journal PDF
  definitions before submission.
- ~~N4~~ DONE — **CORRECTED 2026-08-11 (CR11 audit)**: of 123 R2 merge
  examples, **100 share a one-step successor** (multiway merge at depth 1)
  and only **23 have no one-step meeting point** (deep-merge candidates).
  The originally published 55/68 split compared min-policy images only
  (f_min equality), which inflates "genuinely deeper": differing min-images
  do not rule out a shared one-step successor. The sound test is
  successor-set intersection (analysis_n4n5.py, fixed and rerun).
  The first deep-merge exemplar (2026-07-27, the "unsplice" rule) was
  itself refuted by the audit — its two certificate paths passed through
  the SAME depth-1 state, a one-step R1 collision certified as deep, and
  the old nine-check replay never tested earliest intersection. It is
  withdrawn and replaced: cert_deep_r2.json now certifies the rule
  {(a,b)} → {(a,a),(b,a)}, two mutually-unreachable seeds reaching a
  common witness in 2 steps each with exact one-step successor sets
  disjoint; independently replayed, eleven checks (two new deepness
  checks included), CONFIRMED.
- Conjecture stress (2026-07-27): tiers (5,3) and (4,4) — ZERO violations
  of the weak form. At (4,4) collisions explode 52 → 182/238 and exactly
  one rule stays unambiguous ({(a,a),(b,b)} → {(a,b),(b,a)}, rigid; its RHS
  symmetry acts trivially on histories). BUT the 55 (4,4)-ambiguous-rigid
  holdouts ALL survive (5,4) (333 states; splice positive-control shows 23
  collision images there) — so the strong dichotomy is demoted to an open
  question and the refined target is *independent ambiguity*.
- ~~N5~~ DONE, and it produced the program's main conjecture. Define a rule
  to have **history ambiguity** if some image admits a reverse-match at a
  support other than the comatch yielding a predecessor not isomorphic to
  the original. Empirically, across all 238 semantic-D1 survivors at
  (≤4v, ≤3e):

      history ambiguity is NECESSARY for collision:
      52/52 colliding rules are ambiguous; 0 false negatives;
      all 56 unambiguous rules are rigid.

  (It is not sufficient: 130 ambiguous rules are rigid in range — e.g.
  doubled-edge LHS rules whose ambiguity is a benign multiset automorphism.)

  **RIGIDITY THEOREM (2026-07-27, formerly the Main Conjecture).** A
  semantically locally-invertible rule with no history ambiguity has
  injective one-step evolution on isomorphism classes — under every policy,
  and for the successor relation itself. Elementary five-line proof
  (PROOF_rigidity.md): transport the DPO undo of one application along the
  isomorphism of results and case-split on whether its support hits the
  other comatch — semantic D1 closes one case, unambiguity the other. The
  perfect empirical necessity record was a theorem in disguise. Track B's
  remaining central problem is the CONVERSE (dichotomy): does independent
  ambiguity force eventual collision?

## 2026-08-03 — Witness-level dichotomy analysis (D-IA); the converse resolved at relation level, open at policy level

Full treatment: WITNESS_ANALYSIS.md; definitions: DEFINITIONS.md
addendum; code/data: phase1/independent_ambiguity.py, ia_*.jsonl.

- **Negative result (the replay obstruction).** The tempting converse
  argument "ambiguity ⟹ relation-level non-injectivity via DPO undo" is
  FALSE for vertex-creating rules: replaying the alternative predecessor
  forward freshens vars(R)\vars(L), so it need not reach the shared
  image at all (*phantom witnesses*: 774 of the holdouts' 3320 pairs,
  4591 of the colliders' 13817). Replay is automatic iff no fresh
  variables are needed (Proposition A).
- **Hypothesis surfaced.** PROOF_rigidity's "one of them yields S₁" step
  needs syntactic D1 (vars(L) ⊆ vars(R)) — satisfied by the entire gated
  class, so nothing retracts; now explicit as remark 6.
- **The relation-level dichotomy is CLOSED** (Proposition B): for the
  gated class, replayable witnesses correspond exactly to one-step
  relation-merges, preserving causal class; D-IA (a replayable AND
  causally independent witness) ⟺ an INDEPENDENT one-step merge.
- **Machine-check of Prop B: 182/182 colliders have D-IA** (forced by
  the proposition; zero exceptions, zero errors).
- **The 55 ambiguous-but-rigid holdouts partition exhaustively** into
  three rigidity mechanisms: 25 orbit-rewind only, 18 all-phantom, and
  **12 policy-shielded D-IA rules** — 274 certified independent
  relation-merges, 0 realized by min-successor in range, none excusable
  by census bounds. Colliders shield 4191 of their 8590 D-IA pairs too,
  but always leak at least one.
- **Q5 (the remaining open question).** Does policy shielding persist
  at all tiers for the 12 frontier rules (a policy-rigidity theorem), or
  break eventually (a collision)? The two heaviest frontier rules are
  the edge-growers {(a,b)} → {(a,b),(b,c)} and {(a,b)} → {(a,b),(c,a)}.

All claims (4,4)-probe-tier, reachability bounds as in the sweep;
propositions exact and unbounded.
