# Zoom brief — presenting to Arrighi, Costes, Maignan (week of 2026-08-03)

*One page to reread before the call. Everything cited is pushed on
`main`. Cite their results by NAME, not number (the conference/journal
versions number differently).*

## The 90-second story

The Jacobian conjecture fell in July 2026: local invertibility
everywhere, global 3-to-1. Question: does the same phenomenon exist for
hypergraph rewriting? **Yes** — the splice rule
`{(a,a),(b,c)} → {(a,b),(c,a)}` is census-preserving and per-application
undoable, yet two non-isomorphic states evolve to the same 4-path;
machine-checked in Lean 4, zero sorries. The image forgets which vertex
carried the loop: the forgotten match is a discrete monodromy. An
exhaustive sweep (489 rules, independently verified certificates) then
located the mechanism exactly: **history ambiguity**, and the Rigidity
Theorem proves unambiguity ⟹ one-step injectivity. This week the
converse was resolved at the relation level, leaving one sharp open
question (Q5).

## The five cards

1. **Splice + Lean.** Collision, non-isomorphism, successor-uniqueness,
   terminality all formal (`lean/SpliceCollision.lean`). Policy-free.
2. **Rigidity Theorem** (PROOF_rigidity.md): semantically D1 +
   history-unambiguous ⟹ one-step evolution injective on iso classes.
   **State remark 6 proactively**: the proof uses syntactic D1
   (vars(L) ⊆ vars(R)) — every swept rule passes that gate, nothing
   retracts, but the hypothesis belongs in the statement. Saying this
   unprompted, to the authors of the paper ours comments on, is the
   right posture.
3. **The converse, resolved at relation level** (WITNESS_ANALYSIS.md).
   The naive converse is *false* for vertex-creating rules — replaying
   the alternative predecessor freshens vars(R)\vars(L), so it need not
   reach the shared image ("phantom witnesses"; the monodromy cuts both
   ways). With replayability as the missing condition, Propositions A/B
   close the relation-level dichotomy; machine-check: **182/182
   colliders have D-IA, zero exceptions**.
4. **Q5, resolved in strata the night before** (Q5_NOTES.md). The 55
   ambiguous-but-rigid rules partition 25 orbit-rewind / 18 all-phantom
   / 12 D-IA rules — and the 12 then split three ways: the seven 2→2
   rules **collide under min at the (5,5) census** (holdout status was
   a census artifact; the forcing direction of the dichotomy holds);
   and all five growers are **policy-relative**: max realizes their
   merges (the pendant pair only at richer censuses, (6,5)/(5,6)),
   while **min stays collision-free for every grower through six
   censuses**. Final tally: 12/12 frontier rules have genuine,
   independently verified policy collisions under {min, max} — the
   dichotomy's forcing direction holds policy-existentially across the
   board — and the surviving conjecture is **min-coherence of growth**
   (f_min injective for edge-growing rules), backed by two proven
   structural lemmas: pendant-free states share no successor at all,
   and the sink-leaf core is absolutely conserved by the successor
   relation (PENDANT_COHERENCE.md). The conserved-core picture — the
   skeleton rides along, information loss confined to the decoration
   layer — is the genuinely new object for this audience. (All 17
   collision certificates independently verified, tier-stamped.)
5. **Positioning against their work** (CGD_BOUNDARY_NOTE.md). Their
   theory: global bijectivity in, local structure out, on a compact
   bounded-degree pointed space ("invertible implies reversible",
   "invertible implies almost-vertex-preserving" — compactness
   load-bearing, their own emphasis). Ours: local invertibility in,
   global injectivity fails, off that space. **No hypothesis overlap —
   the directions compose rather than compete.** Mirror image worth
   saying aloud: they prove global invertibility forces (almost)
   vertex-preservation; we prove census-preservation does not force
   global invertibility.

## Likely questions, ready answers

- *"Multi-step / multiway merging — certified or anecdotal?"* →
  `phase1/cert_deep_r2.json`: two-step-per-branch R2 merge (unsplice
  rule), nine independent checks. Certified end-to-end.
- *"Is your D1 too weak? A rule that 'moves' content isn't locally
  invertible."* → That boundary is the result: semantic D1 is
  result-side uniqueness at the comatch; the D3-strict sweep shows the
  phenomenon survives full census preservation and loop-free pure
  rewiring (18/105). Wherever the line is drawn short of their global
  axioms, collisions exist on the far side.
- *"Does this contradict your paper?"* → No — see card 5. It shows the
  phenomenon their axioms exclude by fiat is real one step outside them.
- *"Garden of Eden for dynamic topology?"* → Verified against their
  text: no Moore–Myhill/surjunctivity statement exists there (one
  Gromov citation, explicitly pivoted from). Q4 appears genuinely open;
  ask them directly — Edwin already posed it in the 07-27 email.
- *"AI involvement?"* → Disclosed throughout; independent verifier
  shares no code with the search; flagship fully formal. Trust the
  proofs, not the process.

## The asks

1. Their read on Q4's openness (and interest in the D2-closed class).
2. Critical feedback on NOTE_DRAFT.md — and if they consider it
   reasonable arXiv material, the endorsement for cs.DM (cross
   math.DS) requested in the 07-27 email.
3. Whether the Q5 frontier (12 rules, two edge-grower families) fits
   any framework they know for policy/scheduler-independence.

## Repo pointers (all on main)

README → NOTE_DRAFT → PROOF_rigidity (remark 6) → WITNESS_ANALYSIS →
CGD_BOUNDARY_NOTE → phase1/ certificates + `verify_independent.py`.
DOI: 10.5281/zenodo.21630926.
