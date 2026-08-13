# RESULTS — Discrete Jacobian Program (first findings, 2026-07-26)

## Headline (internal claim, pre-external-review)

**Within the declared semantic-D1 probe over states with ≤4 vertices and
≤3 edges, fully census-preserving non-identity rules exist whose one-step
evolution is non-injective on isomorphism classes.** Eighteen of 105 fully
census-preserving probe survivors collide, with 12 policy-independent
examples. The concrete splice collision is unbounded by its hand proof,
but global semantic D1 for the splice rule has not been proved.

## THE flagship (cert_flagship.json) — maximal strength on every axis

Rule (**splice**): `{(a,a), (b,c)} → {(a,b), (c,a)}` — "splice the loop at
a into the edge b→c, giving c→a→b." Census-preserving on both counts, no
fresh vertices; it passes the declared bounded semantic-D1 probe.

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
non-isomorphism, successor-class agreement, and S1-successor terminality
are machine-checked. Symmetric terminality and mutual unreachability are
hand arguments in PROOF_flagship.md.

The mechanism, sharpened: the P₄ image does not remember WHICH interior
vertex was the spliced loop. Two distinct (state, match) histories produce
isomorphic results; the forgotten match is the discrete monodromy.

## Secondary example (cert_0)

Rule (count-preserving; passes the bounded semantic-D1 probe):

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

- 489 enumerated rules (classes A, B, B+) → 238 non-identity survivors of
  the semantic-D1 probe over states with ≤4 vertices and ≤3 edges → **52
  rules with genuine R1 collisions** at (≤4 vertices,
  ≤3 edges); 77 INDEPENDENT pairs, 32 from count-preserving rules.
- 1,041 of 1,770 two-rule systems collide (largest: 12 independent pairs).
- 87 of 226 systems show R2 multiway merges of seeds classified as mutually
  unreachable within the recorded search bounds.
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
2. **Reading obligations outstanding** (VERDICT.md): Arrighi–Costes–Maignan
   arXiv:2510.03296 (possible D1 overlap — if their sufficient conditions
   exclude fresh-vertex re-anchoring, our examples probe exactly their
   boundary) and the Natural Computing 2020 CGD paper.
3. ~~Vertex count is not preserved~~ RESOLVED: D3-strict collisions exist
   (18 rules), including loop-free pure rewiring and policy-independent
   instances. The "anonymity needs fresh room" hypothesis is refuted; the
   splice flagship shows anonymity can hide in graph symmetry itself.
4. All sweeps bounded; the splice and cert_0 flagships lift their bounds by
   hand (terminal successors); other certificates remain bounds-relative.

## Next steps

- ~~N1: hand proof~~ DONE: PROOF_flagship.md (splice), plus Lean
  formalization lean/SpliceCollision.lean (compiling as of this writing).
  The Lean file proves the concrete collision properties; semantic D1 is
  bounded sweep evidence and is not formalized there.
- ~~N2: D3-strict sweep~~ DONE via log query: phenomenon survives, 18/105.
- ~~N3~~ DONE (POSITIONING.md): novelty gate PASSED. Arrighi–Costes–Maignan's
  sufficient conditions rest on context-preservation + DAG assumptions that
  exclude splice-type rules. Our concrete example shows that dropping
  context preservation can permit reversibility to fail, even
  census-preservingly. CGD line assumes global reversibility and
  derives local structure — our converse. Garden-of-Eden for dynamic
  topology confirmed unclaimed in both. Residual: skim CGD journal PDF
  definitions before submission.
- ~~N4~~ CORRECTED: of 123 R2 merge examples, 55 were detected by the
  original one-step policy-image comparison and 68 were not. That test did
  not establish minimum merge depth. The historical `cert_deep_r2.json`
  independently replays two legal two-step paths to a common witness, but
  its seeds also share a one-step successor. It is therefore a path
  certificate, not a shortest-path or genuinely-deep-merge certificate.
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
  the original. Empirically, across all 238 bounded semantic-D1 probe
  survivors at
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
  perfect empirical necessity record was a theorem in disguise. This is a
  human-readable theorem pending external or generic Lean review. Track B's
  remaining central problem is the CONVERSE (dichotomy): does independent
  ambiguity force eventual collision?
