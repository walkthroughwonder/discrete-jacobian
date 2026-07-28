# A locally invertible Wolfram model rule that merges branches: the "discrete Jacobian" collision

*[Draft for community.wolfram.com — Edwin Rosero. AI assistance (Claude,
Anthropic) disclosed. Post under Edwin's account only after his final read.]*

---

This July, the 87-year-old Jacobian conjecture fell: there is an explicit
polynomial map ℂ³ → ℂ³ whose differential is invertible at *every point*,
yet which globally maps three distinct points to one. Local invertibility
everywhere; global information loss. I wanted to know: **does the same
phenomenon exist for hypergraph rewriting?**

It does — and the minimal example is small enough to run in two lines.

## The splice rule

    {{a, a}, {b, c}}  ->  {{a, b}, {c, a}}

"Splice the loop at `a` into the edge `b -> c`." Note what this rule does
*not* do: it creates no vertices, deletes no vertices, and preserves the
edge count. Every application is undoable: given the result and the two
edges the application produced, the predecessor is uniquely determined.
In that per-application sense the rule is locally invertible.

## The collision

Take these two states — non-isomorphic (check the out-degrees), and
neither reachable from the other:

    S1 = {{0,0}, {1,2}, {1,3}}    (* loop + out-star  *)
    S2 = {{0,0}, {1,2}, {3,2}}    (* loop + in-star   *)

Try it:

    r = {{a, a}, {b, c}} -> {{a, b}, {c, a}};
    s1 = ResourceFunction["WolframModel"][r, {{0,0},{1,2},{1,3}}, 1, "FinalState"]
    s2 = ResourceFunction["WolframModel"][r, {{0,0},{1,2},{3,2}}, 1, "FinalState"]
    IsomorphicGraphQ[Graph[DirectedEdge @@@ s1], Graph[DirectedEdge @@@ s2]]

*(→ `True` — verified in Wolfram Cloud against a live kernel, 27 July
2026. The default updating order picks one of the two possible events per
state; the collision doesn't care, since all successors are isomorphic —
that is part of what's proven.)*

Each state has two possible updates — and all four results are the same
hypergraph up to renaming: the directed path on four vertices. So the
one-step evolution on isomorphism classes is well-defined at S1 and S2
(unique successor, no updating-order choice involved), and it is **not
injective**: two genuinely different states evolve to one.

Where did the information go? The path does not remember *which interior
vertex used to carry the loop*. Locally, every application knows its own
undo; globally, the state forgets which application happened. The
forgotten match is the discrete analogue of the forgotten branch of the
covering map in the ℂ³ counterexample — a discrete monodromy.

## What's proven, what's swept, what's open

- **Machine-checked:** the collision above — non-isomorphism, successor
  uniqueness up to isomorphism, and terminality (successors admit no
  further application, so the two states are unconditionally mutually
  unreachable) — is formalized in Lean 4 and compiles against Mathlib with
  zero `sorry`s.
- **Swept:** all 489 rules in three small signature classes; 238 pass a
  semantic local-invertibility gate; 52 of them collide at states with ≤4
  vertices and ≤3 edges, 182 at ≤4 edges. Every certificate is checked by
  an independently implemented verifier. Multiway (branchial) merges with
  distinct ancestry also occur, including certified merges that need two
  steps on each branch — merging is not just one-step collision in
  disguise.
- **Proven (elementary proof, pending external scrutiny):** collision is
  governed by *history ambiguity* — whether some image can be "read
  backwards" at a different location than the one that produced it,
  yielding a different predecessor. Across every rule and tier tested,
  ambiguity was necessary for collision with zero exceptions — and that
  perfect record turns out to be a theorem rather than a coincidence: a
  locally invertible rule with no history ambiguity has one-step evolution
  injective on isomorphism classes, under every updating policy. The proof
  is a short support-comparison argument (PROOF_rigidity.md in the
  repository); the sweeps were rediscovering it empirically.
- **Open:** the converse (a dichotomy question) — does genuine history
  ambiguity force eventual collision? Ambiguous-but-rigid rules persist
  through every tier swept so far, so the naive converse needs at least a
  refinement; the working notion is *independent* ambiguity, ambiguity not
  explained by a symmetry of the rule itself.

## Why I think this matters for multiway systems

Branch merging is usually discussed here as a *feature* (confluence,
causal invariance, quantum interpretations). This example isolates a
different mechanism: merging of branches with **disjoint ancestries**,
forced by rules that are individually information-preserving. In
Garden-of-Eden terms: for cellular automata on fixed geometry there is a
century of theory linking local injectivity properties to global ones
(Moore–Myhill, Gottschalk, Gromov); for rewriting that changes its own
geometry, that theory appears not to exist yet. The nearest work
(Arrighi et al. on reversible causal graph dynamics and space-time
reversible rewriting) *designs* reversibility in via context-preservation
conditions — the splice rule shows those conditions are exactly the load-
bearing ones: drop them and reversibility must fail, even census-
preservingly.

Everything — code, 14 machine-verified certificates, sweep logs, the Lean
proof, and a working-draft note — is public:

- Repository: https://github.com/walkthroughwonder/discrete-jacobian
- Archived + citable: https://doi.org/10.5281/zenodo.21630926

I'd love help with: (1) scrutiny of the rigidity theorem's proof
(PROOF_rigidity.md — it is a page, and either right or instructively
wrong), and the open converse: does independent history ambiguity force
eventual collision?; (2) richer-tier searches (the pipeline is a few
hundred lines of Python); (3) visualizations of the branchial picture of
the splice — the merge is begging for a good multiway graph rendering.

*Disclosure: this project was carried out in close collaboration with an
AI assistant (Claude, Anthropic), including the searches, the Lean proof,
and this post. All certificates are independently machine-verified, and
the flagship is fully formalized — trust the proofs, not the process.*
