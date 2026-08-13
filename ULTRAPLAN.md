# ULTRAPLAN — The Discrete Jacobian Program

**Goal.** Turn the July 2026 Jacobian counterexample into a research program on
discrete rewriting systems, with two coupled tracks:

- **Track A (search):** find — or rule out at small scale — a *discrete Jacobian
  counterexample*: a locally invertible hypergraph rewrite system whose global
  evolution is not injective (distinct states collide).
- **Track B (theory):** pose and attack the rigidity question that explains
  Track A's outcome: *which local invertibility conditions force global
  injectivity/surjectivity of evolution?* — the surjunctivity bridge
  (Ax–Grothendieck ↔ Moore–Myhill ↔ Gottschalk/Gromov).

The tracks feed each other: A generates certificates and data, B supplies the
conjectures worth testing. Either outcome of A is a result:

| A finds a collision | A comes up dry at small scale |
|---|---|
| Explicit discrete analogue of the Jacobian phenomenon; minimize + visualize + write up | Empirical rigidity; conjecture a discrete Garden-of-Eden theorem for dynamic topology; attack in B |

**Non-goals.** No claims about physics. No touching unrelated research
repositories. Other projects continue independently.

---

## Phase 0 — Definitions and prior art (the load-bearing phase)

Everything downstream dies if the definition of "locally invertible" is wrong
(too strong → global injectivity is trivially forced; too weak → collisions are
trivial and boring). Deliverable: `DEFINITIONS.md` with worked toy examples.

**0.1 Candidate definitions of a locally invertible rule** (draft all three,
pick a primary and an alternate):
- **D1 — application-level bijectivity:** each rule application, with its
  boundary (glueing context) fixed, is a bijection between local
  configurations; the rewrite is undoable knowing only the rule and the
  boundary. (Analogue of "Jacobian nonvanishing at each point".)
- **D2 — reversible-DPO:** the rule is a double-pushout span L ← K → R whose
  reverse R ← K → L is also a valid rule of the system. Prior art exists
  (reversible graph grammars) — must be surveyed, not rediscovered.
- **D3 — determinant analogue:** the rule's action on local invariant counts
  (edge signature / incidence matrix) has determinant ±1 — a genuinely
  "Jacobian-flavored" condition, probably the novel one.

**0.2 Two collision regimes**, kept separate from day one:
- **R1 — deterministic:** a fixed updating scheme; collision = two distinct
  global states with the same successor. (CA-style; Moore–Myhill territory.)
- **R2 — multiway:** collision = distinct multiway branches merging (same
  state reached along causally distinct histories from distinct ancestors).
  This is the branchial-space version and the one closest to the 3-to-1
  collision in the ℂ³ counterexample.

**0.3 Prior-art sweep** (a half-day each, notes into `PRIOR_ART.md`):
- Reversible cellular automata; Garden-of-Eden / Moore–Myhill over amenable
  groups; Gromov–Weiss surjunctivity for sofic groups
  (Ceccherini-Silberstein–Coornaert book is the canonical source).
- Reversible graph rewriting / reversible DPO literature.
- Wolfram-model literature on rule invertibility and confluence (so the
  framing lands with that community rather than duplicating it).
- Check: has anyone already posed the dynamic-topology Garden-of-Eden
  question? If yes, the program pivots to their open questions.

**Exit criteria:** primary definition chosen; at least one toy example of a
locally invertible system and one non-example, hand-verified; confirmation the
main question is genuinely open.

---

## Phase 1 — Infrastructure (`E:\math\discrete-jacobian\`, then a git repo)

Built to the 712/872 standard: **the verifier is independent of the searcher**
(the v3-retraction lesson: test the found object's property directly, never the
search predicate).

- **1.1 Rule enumerator** — small hypergraph rewrite rules by signature
  (e.g. 2₂→2₂, 2₂→3₂, 3₂→3₂ in Wolfram-model notation), filtered to the
  locally invertible subset per the Phase 0 definition. Python.
- **1.2 Canonical state hashing** — hypergraph canonical form via bipartite
  incidence-graph canonicalization (igraph/nauty backend). Without this,
  collision detection is meaningless (isomorphic ≠ colliding).
- **1.3 Evolution engine** — deterministic scheme for R1; multiway BFS with
  canonical dedup for R2. Bounded: states up to N edges, depth up to D.
- **1.4 Collision detector** — R1: successor-map inversion table.
  R2: merge events between branches with distinct ancestries.
- **1.5 Independent verifier** — standalone script that takes a claimed
  collision certificate (rule set + two states + evolution traces) and checks
  it from scratch, sharing no code with the search stack.
- **1.6 Visualizer hook** — export certificates in a JSON format the
  `topological-light-propagation` explorer can load as a preset
  ("locally invertible rules with merging branches").

**Exit criteria:** round-trip test — plant a known collision in a known-trivial
system, searcher finds it, verifier confirms it.

---

## Phase 2 — Search campaign (Track A)

- **2.1 Exhaustive small sweep:** all locally invertible rules at the smallest
  signatures, all initial states ≤ N₀ edges. Log everything
  (`sweep_results.jsonl`); no silent caps — record what was truncated.
- **2.2 Escalation ladder:** raise signature size / N / D stepwise;
  loop-until-dry (stop a tier after two full passes with nothing new).
- **2.3 On any hit:** verify independently → minimize (shrink rule set and
  states while preserving the collision) → classify (R1 vs R2; which
  definition D1/D2/D3 it lives under) → visualize.
- **2.4 On sustained dryness:** the data *is* the deliverable — tabulate
  "rigidity up to (signature, N, D)" and hand Track B an empirical conjecture.

**Milestone M2:** either a verified minimal collision certificate, or a
rigidity table + precisely stated conjecture.

---

## Phase 3 — Theory (Track B)

- **3.1 Fixed-topology reduction (warm-up theorem):** hypergraph rewriting on a
  frozen underlying geometry is a CA over a group/graph; state exactly which
  known results (Moore–Myhill on amenable groups, Gromov on sofic) transfer.
  This is the "T1" result and is mostly bookkeeping — but nobody has written
  it down in Wolfram-model language.
- **3.2 The real question:** does any Garden-of-Eden-type theorem survive
  *dynamic topology* (the rewrite changes the geometry it acts on)?
  Three candidate outcomes, all publishable:
  - **T2a:** a rigidity theorem for a restricted dynamic class
    (e.g. degree-bounded, causal-invariant rules);
  - **T2b:** Phase 2's counterexample shows rigidity fails → characterize the
    failure mechanism (the discrete analogue of the branched-cover mechanism
    Sawin/Tao identified in ℂ³);
  - **T2c:** an equivalence — local invertibility class ↔ injectivity class —
    even partial, is a strong result.
- **3.3 Lean angle (our comparative advantage):** state the main conjecture in
  Lean 4. If Phase 2 produced a finite certificate, formalize the
  counterexample end-to-end (finite object — fully checkable, no `sorry`).
  Candidate venue: formal-conjectures (new conjecture file) and/or a
  standalone repo like erdos-872.
- **3.4 Expert outreach** (drafts only — nothing sent without explicit
  sign-off, and only after results are self-verified; the 872 protocol):
  CA-and-groups community (Ceccherini-Silberstein school) for Track B;
  Wolfram Physics community for the framing and the visualizer.

---

## Phase 4 — Write-up and dissemination

- **4.1** Short note (arXiv math.DS/math.GR crosslist or Wolfram Community
  post, depending on what Phase 2/3 produced): definitions, search
  methodology, certificate or rigidity table, the T1 reduction, open
  questions.
- **4.2** Interactive companion: explorer preset that *shows* the collision
  (or shows exhaustive rigidity), plus a "why the ℂ³ counterexample works"
  visual (branched cover of Sym³(ℙ¹) — branch merging is the same picture).
- **4.3** Feed surviving open questions back into the loop.

---

## Risk register

| Risk | Mitigation |
|---|---|
| Definition makes the question trivial (either direction) | Phase 0 toy examples must include a near-miss in each direction before any code is written |
| Rediscovering reversible-rewriting literature | Prior-art sweep is a Phase 0 exit criterion, not an afterthought |
| State-space explosion | Canonical hashing + hard N/D bounds + escalation ladder; never claim more than the swept range |
| Search-predicate bug (the v3 failure mode) | Independent verifier, written separately, run on every claim |
| Isomorphism false-positives ("collision" that's just relabeling) | Collisions defined on canonical forms only; verifier re-canonicalizes from scratch |
| Overclaiming physics relevance | Non-goal by charter; the note claims mathematics only |

## Cadence and sequencing

- This program runs in the gaps while Kourovka PRs (#4638/#4639) await review;
  Kourovka feedback, when it arrives, takes priority (small, fast wins).
- Phase 0 is pure reading/writing — no compute. Phases 1–2 are exactly the
  SAT-witness workflow already proven on 712, applied to a new domain.
- Unrelated research remains out of scope.

## Immediate next actions (Phase 0 kickoff)

1. Draft `DEFINITIONS.md` with D1/D2/D3 + one worked toy example each.
2. Prior-art sweep: reversible DPO rewriting; Moore–Myhill/Gottschalk survey;
   Wolfram-model invertibility posts.
3. Verdict memo: is the dynamic-topology Garden-of-Eden question open?
   (Go/no-go gate for the whole program.)
