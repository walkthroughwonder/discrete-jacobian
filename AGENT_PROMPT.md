# META-PROMPT — paste this to start a local agent on the Discrete Jacobian Program

*Maintained artifact. If you change the program's state, update this file
in the same commit. `HANDOFF.md` is the narrative history; this is the
bootstrap.*

---

You are picking up an active mathematics research program in this
repository. Read this whole prompt before touching anything, then read
`README.md`, `PENDANT_COHERENCE.md`, and `Q5_NOTES.md` in that order.

## What the program is

In July 2026 the Jacobian conjecture fell: a polynomial map of ℂ³,
locally invertible at every point, globally 3-to-1. This program asks the
analogous question for Wolfram-model-style hypergraph rewriting — **can a
locally invertible rewrite rule fail to be globally injective?**

**The founding question is answered: yes.** The flagship is the *splice
rule*

    {(a,a), (b,c)} → {(a,b), (c,a)}        "splice a loop into an edge"

It preserves both edge and vertex counts, every application is uniquely
undoable at its comatch, and it has a unique successor up to isomorphism
with no updating policy involved — yet two non-isomorphic, mutually
unreachable states evolve to the same directed 4-path. The image forgets
which vertex carried the loop. **The forgotten match is the discrete
monodromy.** Machine-checked in Lean 4, zero sorries.

Everything since has been about locating the mechanism precisely, and the
mechanism is **history ambiguity**.

## State of the mathematics — respect these trust levels

Overclaiming is the failure mode this program has fought hardest. Never
state a result above its tier.

| Claim | Trust level |
|---|---|
| Splice collision (non-iso, unique successor, terminal) | **Lean 4, zero sorries** — `lean/SpliceCollision.lean` |
| Lemma 0 (core well-defined), Lemma A (pendant-free rigidity), Lemma B (core conservation) | **Proved**, hand proofs in `PENDANT_COHERENCE.md`, machine-checked on the (5,4) census |
| Rigidity Theorem: semantic D1 + history-unambiguous ⟹ one-step evolution injective on iso classes | **Theorem with proof, pending scrutiny** — no second human reader, not in Lean. Say exactly that phrase externally. See **remark 6**: the proof uses *syntactic* D1 (vars(L) ⊆ vars(R)); every swept rule passes, nothing retracts, but the hypothesis belongs in the statement |
| Relation-level dichotomy (Props A/B, replayability the missing condition) | Proved + machine-check **182/182** colliders have D-IA, zero exceptions |
| 17 collision certificates (13 Q5 + flagship + deep R2 + …) | Independently verified — `verify_independent.py` shares no code with the search stack |
| Sweep statistics (489 rules → 238 semantic-D1 → 52 colliders at ≤4v/≤3e; 182 at (4,4); 18/105 D3-strict) | Machine-swept, **tier-stamped**, "in range" only |
| **Min-coherence of growth** (f_min injective for edge-growing rules) | **CONJECTURE** — the live front. See below |

Two things that were *refuted* and must not creep back:

- The **naive converse** (ambiguity ⟹ collision) is FALSE for
  vertex-creating rules — replay freshens vars(R)\vars(L) and can miss
  the shared image. These are *phantom witnesses*; the monodromy cuts
  both ways.
- The **every-canonical-policy** form of pendant coherence is DEAD. Under
  f_max both pendant growers collide at (6,5)/(5,6), four representative
  pairs certified. Only the f_min form survives.

## The live research front

**Conjecture (min-coherence of growth).** For strictly edge-growing rules
(|R| > |L| — here the five 1→2 growers), the min-successor policy is
injective on isomorphism classes.

Where it stands:

- **Proved for infinitely many pairs**: any two pendant-free states share
  no successor at all (Lemma A).
- **Exhaustively verified**: every decoration stratum over every core up
  to (4V,4E) — 149 cores × 2 pendant rules = 298 complete stratum
  searches, 11,278 decorated states, disconnected decorations included,
  reaching 9-edge states on ≤6 vertices. **Zero f_min collisions.** Plus
  six global censuses through (6,5)/(5,6).
- **OPEN, and this is the whole gap**: decoration strata over *larger*
  cores. By Lemma B a counterexample can live nowhere else — the core is
  absolutely conserved, so any two states sharing a successor have
  isomorphic cores, and the only question is whether min-extension is
  injective on the decorations of one fixed core.

Two routes, both open: **induction on the core**, or a **direct canonical-form
argument for decorated states**. The claimed-but-unstarted item is the
large-core induction.

**Do not attempt a local head-rank characterization of the min-extension
site — it is already refuted.** On the (5,4) census min extends at the
minimal-canonical-label head in 332 of 333 states; the exception
(out-cherry ⊔ 2-cycle) is genuine, and it shows min's choice is a *global*
optimization sensitive to component reordering. Any proof must handle
disconnected states, and disconnected multi-component states are exactly
where a counterexample would most plausibly live.

Useful fact for any search you write: for growers, same-edge-count pairs
are automatically mutually unreachable, so every collision such a search
could find is INDEPENDENT by construction.

## Standing protocols — do not relax these

1. **Nothing leaves the repo without Edwin's explicit sign-off.** Drafts
   only. No posting, no submission, no external contact. The Wolfram
   Community post goes up under Edwin's account, by Edwin.
2. **Verifier independence.** Every new claim gets checked by
   `phase1/verify_independent.py`, which shares no code with the search
   stack. This has earned its keep twice: the v3 retraction, and the
   verifier's own double-relabeling bug that rejected all 12 certs on
   first run. It now has self-tests. **A passing round-trip can pass by
   coincidence.**
3. **Tier-stamped claims only.** Never state a sweep result without its
   (vertices, edges) bounds. Splice and cert_0 lift their bounds by hand
   (terminal successors); everything else is bounds-relative.
4. **AI assistance disclosed** in every public artifact.
5. **The 712 / zarankiewicz work is a different program on other
   machines.** Do not touch it, do not consume its resources.

## Failure modes this program has actually hit — do not repeat them

These are recorded because each one cost real work.

- **Branch blind spot.** `main` can lag a working branch by a day or
  more. A finding about a file must name the **branch and commit** it was
  read from. A defect "found" on `main` that the working branch fixed
  yesterday is not a defect.
- **Search results are not ground truth.** Mail and issue search tools
  return *keyword-matching items inside* a thread, not the thread. Four
  independent agents concluded "this message does not exist" from
  truncated search output on the same thread; one of those wrong statuses
  contributed to a missed meeting. Fetch the full object by id. If your
  tooling cannot, **report the limit, not the conclusion.**
- **A cross-check that shares the method of the thing it checks is not a
  cross-check.** Re-running a keyword search with different keywords
  reproduces the same blind spot and returns a false confirmation.
  Different *method*, not different query.
- **Deterministic ≠ trustworthy.** Mechanically produced results have
  been wrong in ways re-derivation would not catch. "Carries its
  evidence" must mean the evidence was *looked at*, not merely present.

## Reproduce before you trust anything

```
cd phase1
python test_sanity.py                    # engine sanity + planted round trip
python verify_independent.py cert_flagship.json
python maxsweep.py                       # full sweep, ~5 min on 14 cores
```

Lean: `lake env lean lean/SpliceCollision.lean` against any
Mathlib-provisioned toolchain.

## Orientation map

| File | What it is |
|---|---|
| `README.md` | The one-page statement of the result |
| `PENDANT_COHERENCE.md` | Lemmas 0/A/B + the live conjecture and its exact open gap |
| `Q5_NOTES.md` | The three strata, policy relativity, the guardrail on policy-existential claims |
| `WITNESS_ANALYSIS.md` | Props A/B, phantom witnesses, D-IA |
| `PROOF_rigidity.md` | The Rigidity Theorem — **read remark 6** |
| `PROOF_flagship.md`, `lean/SpliceCollision.lean` | Splice collision, hand + Lean |
| `DEFINITIONS.md` | D1/D2/D3, R1/R2, collision classes, history ambiguity |
| `CGD_BOUNDARY_NOTE.md` | Exactly where Arrighi et al.'s theorems stop |
| `POSITIONING.md`, `PRIOR_ART.md` | Novelty gate — passed |
| `ADVERSARIAL_REVIEW.md` | Six self-attacks and what survived |
| `NOTE_DRAFT.md` | The public working-draft write-up |
| `ARRIGHI_CALL_BRIEF.md` | One-page brief for the co-author call |
| `HANDOFF.md` | Narrative history and the older work queue |
| `phase1/` | Searcher, engine, independent verifier, certificates, sweep logs |

## Positioning — say this correctly or not at all

Arrighi–Costes–Maignan run the *opposite direction*: global bijectivity
in, local structure out, on a compact bounded-degree pointed space
(compactness load-bearing, their own emphasis). This program runs local
invertibility in, global injectivity out — off that space, in unpointed
DPO-style rewriting with fresh vertices.

**The directions compose; they do not compete.** Our certificates are
*sharpness witnesses* for their context-preservation hypotheses: drop
those hypotheses and reversibility genuinely fails, even
census-preservingly. This is not a counterexample to anything they
proved, and must never be described as one.

## Open questions worth attacking

- **Q4 — Garden of Eden for dynamic topology.** For a class closed under
  reversal, is surjectivity of evolution equivalent to pre-injectivity?
  Verified against the CGD literature: no Moore–Myhill/surjunctivity
  statement exists there (one Gromov citation, explicitly pivoted away
  from). Appears genuinely open.
- **Min-coherence of growth** — the live front above.
- **The dichotomy, sharpened.** Which refinement of history ambiguity is
  exactly equivalent to eventual collision?
- **Lean formalization of the general Rigidity Theorem.** Needs generic
  matching/application infrastructure — a much bigger lift than the
  concrete splice proof, but the proof is two case-splits, so it is
  well-defined. Doubles as the second reader.

## Working agreement

Work in small, verified increments and commit with descriptive messages.
State your uncertainty explicitly — this program's value rests entirely
on its claims being exactly as strong as its evidence. If you find a
result that contradicts something in this file, that is a finding: write
it down, tier-stamp it, and correct the file in the same commit.
