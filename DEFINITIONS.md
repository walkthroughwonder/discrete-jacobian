# DEFINITIONS — Discrete Jacobian Program (Phase 0.1)

Setting: a **state** is a finite hypergraph in Wolfram-model style — a multiset
of ordered hyperedges over an abstract vertex set, considered up to
isomorphism. A **rule** ρ : L → R rewrites an instance of the pattern L into R,
with shared pattern variables giving the glueing; fresh variables on the right
create vertices, variables absent on the right destroy them. DPO semantics
(Gorard's adhesive-category formulation) is the reference formalism.

The continuous object we are imitating: a polynomial map F : ℂ³ → ℂ³ with
det DF = const ≠ 0 (locally invertible *everywhere*) that is generically
3-to-1 (globally non-injective). The mechanism there is a nonproper étale
map with several generic sheets:
locally you can always invert, but *which* inverse branch you are on is
global data. The discrete slogan:

> **Local undo data exists at every step; global injectivity fails because the
> successor state does not remember which rule/match produced it.**

That "forgotten match" is our monodromy.

---

## D1 — Application-level invertibility (primary definition)

A rule ρ : L → R is **D1-invertible** if for every boundary context B (the
part of the state untouched by the application, plus the glueing embedding),
the induced map

  {instances of L compatible with B} → {instances of R compatible with B}

is a bijection. Informally: knowing the rule used, the match location, and the
result, the predecessor is uniquely determined; and conversely every
R-instance arises from exactly one L-instance.

- **Example (D1 holds):** {{x,y}} → {{y,x}} (edge reversal). The application
  is its own inverse up to the reverse rule.
- **Example (D1 fails):** {{x,y}} → {{x,x}} (endpoint merge). The identity of
  y is destroyed; distinct predecessors give the same local result.
- **Example (D1 holds, deceptively):** {{x,y}} → {{x,y},{y,z}} with z fresh.
  Given the match data the pendant edge {y,z} is removable and y recoverable.
  Vertex creation is NOT the enemy of D1; anonymous collision is.

**Operationalization (refined 2026-07-26, by Phase 1 experiments):**

- *Syntactic D1 (necessary):* vars(LHS) ⊆ vars(RHS) — no matched vertex is
  forgotten. (The DPO fact that every rule is undoable at its own comatch
  makes undo-based probing vacuous; D1 is about what the RESULT remembers.)
- *Semantic D1 (necessary, strictly stronger):* for every application, the
  reverse-matches supported on exactly the comatch region must all yield the
  same predecessor. Discovered necessary via the chain-step rule
  {{x,y},{y,z}} → {{x,z},{y,z}}: syntactically D1, but its result pair
  {(x,z),(y,z)} decomposes ambiguously (two reverse-matches, two distinct
  predecessors), and it duly "collides" for the wrong reason. Semantic D1 is
  the program's working definition; `core.semantic_d1_violation` implements
  the probe.

**Warning learned from DPO theory:** every DPO rule is undoable *at its own
match* (the reverse span applied at the comatch). So "each application is
reversible" is nearly free in DPO and must not be confused with injectivity of
the global step map. D1 is a statement about applications; the program's
question is about states.

## History ambiguity and unambiguity

Fix an application `a : S → T` of a rule ρ with comatch support `c` in `T`.
It is **history-ambiguous** if the reverse rule has a match in `T` supported
on a region different from `c` whose resulting predecessor is not
isomorphic to `S`. It is **history-unambiguous** if every such alternative
reverse match yields a predecessor isomorphic to `S`. A rule has either
property globally when the condition holds for every application. The
implementation only approximates these global properties on explicitly
declared finite probe spaces.

## D2 — Reversible-rule-set (system-level closure)

A rule set 𝓡 is **D2-closed** if for every ρ ∈ 𝓡 the reverse rule ρ⁻¹
(reverse span R ← K → L) is also in 𝓡, and both directions are D1-invertible.
This is the analogue of "the dynamics has a legal past": every state has
predecessors under the system itself. D2 systems are where surjectivity
questions (Garden-of-Eden states = states with no predecessor) become
non-trivially coupled to injectivity questions.

## D3 — Determinant analogue (the genuinely Jacobian-flavored condition)

Associate to a rule ρ its **signature action**: the linear map on the vector
of local invariants (vertex count, edge count per arity, and any chosen local
census) induced by one application. ρ is **D3-unimodular** if this action is
invertible over ℤ (determinant ±1) — the discrete "det DF = const ≠ 0".

D3 is strictly weaker than D1 (it forgets everything but counts) and
strictly stronger than nothing: it rules out projections that destroy
census information. D1 ∧ D3 was an experimental rigidity hypothesis. The
current collision examples combine own-comatch undoability with bounded
semantic-D1 screening; they do not settle exact global D1 ∧ D3 rigidity.

---

## Collision regimes

Both regimes define collision **on canonical forms** (isomorphism classes via
canonical labeling); two states related by relabeling are the same state.

### R1 — Deterministic collision

Fix an updating policy π (canonical example: apply the rule/match that is
minimal in the canonical ordering of the state). This makes evolution a
function F_π on states. A collision is a pair of states S ≠ S′ with
F_π(S) = F_π(S′).

This is CA-shaped: on a frozen geometry, F_π is (a sequentialized) cellular
map and Moore–Myhill theory applies. The novelty budget is entirely in the
dynamic topology.

### R2 — Multiway (branchial) collision

No policy: all rules at all matches. The multiway evolution is a rewriting
relation; a collision is a **merge with distinct ancestry**: a state T
reachable from two states S ≠ S′ neither of which is reachable from the other
(so the merge is not mere confluence of one state's own branches).

R2 is the closest discrete mirror of the ℂ³ picture: the 3-to-1 collision is
three points (three multiway ancestors) sharing one image (one merged state).
Confluence, causal invariance, and critical-pair theory live here; a
D1-invertible system exhibiting mandatory R2 merges of distinct ancestries is
the discrete Jacobian counterexample in its strongest form.

### Degenerate collisions to exclude (triviality guards)

1. **Relabeling collisions** — excluded by canonical forms.
2. **Garbage-collection collisions** — a rule that deletes a disconnected
   component trivially merges states; excluded because deletion of a
   component with unrecoverable content violates D1.
3. **Symmetric-image collisions** — S and S′ isomorphic; excluded (S = S′ as
   canonical forms).
4. **Policy artifacts (R1 only)** — F_π collisions that vanish under a
   different policy π′ are results about π, not about 𝓡. Report per-policy;
   the strong R1 statement is a collision robust across all canonical
   policies.
5. **Orbit artifacts (found live 2026-07-26)** — if S and S′ are *mutually
   reachable*, the min-successor policy collapses their orbit and the shared
   image is an artifact of orbit structure, not information loss. Genuine
   collisions require mutual unreachability (bounded-BFS check; bounds can
   only let artifacts through, so claimed counterexamples must document
   their reachability analysis explicitly).
6. **Downstream collisions (ruling)** — if S →* S′ one-way and
   F(S) = F(S′), the pair is classified DOWNSTREAM and reported separately.
   The strong, Jacobian-shaped class is INDEPENDENT: neither state reachable
   from the other (mirroring the three mutually-unrelated colliding points
   in ℂ³, and R2's distinct-ancestry condition). Only INDEPENDENT pairs may
   be claimed as discrete Jacobian collisions; DOWNSTREAM pairs are kept as
   secondary data (they measure how non-tree-like the successor relation
   is, not monodromy).

---

## The precise questions

- **Q1 (R1):** Does there exist a D1-invertible (resp. D1 ∧ D3, resp.
  D2-closed) rule set and canonical policy π with a collision F_π(S) = F_π(S′),
  S ≠ S′?
- **Q2 (R2):** Does there exist a D1-invertible rule set whose multiway system
  has a merge with distinct ancestry?
- **Q3 (rigidity):** For frozen-topology systems both answers reduce to
  classical CA theory — write down the exact reduction (T1). For which dynamic
  classes does the reduction's rigidity survive?
- **Q4 (Garden of Eden):** For D2-closed systems, is surjectivity (no
  Garden-of-Eden states) equivalent to pre-injectivity (no collisions between
  states differing in a bounded region)? This is the Moore–Myhill question for
  rewriting with dynamic topology — see VERDICT.md on its apparent openness.
