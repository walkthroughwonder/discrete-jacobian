# An own-comatch-undoable Wolfram model rule that merges branches: the "discrete Jacobian" collision

*[Draft for community.wolfram.com — Edwin Rosero. AI assistance from
Anthropic Claude and OpenAI Codex disclosed. Post under Edwin's account
only after his final read.]*

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
edge count. Each displayed application is undoable when its own comatch is
retained: given the result and the two edges that application produced, the
predecessor is uniquely determined. The rule also passes the declared
semantic-D1 probe over states with ≤4 vertices and ≤3 edges; no unbounded
semantic-D1 claim is made.

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
forgotten match is the discrete analogue of a forgotten sheet of the
nonproper étale map in the ℂ³ counterexample — a discrete monodromy.

## What's proven, what's swept, and what's open

- **Machine-checked:** source non-isomorphism, successor-class agreement,
  the collision, and terminality for successors of S1 are formalized in
  Lean 4 and compile against the pinned Mathlib revision with zero
  `sorry`s. The symmetric terminality fact and unconditional mutual
  unreachability have a short hand proof. Semantic local invertibility is
  bounded sweep evidence, not a theorem in this Lean file.
- **Bounded sweep:** all 489 rules in three small signature classes; 238
  pass the semantic-D1 probe over states with ≤4 vertices and ≤3 edges; 52
  of them collide in that tier, 182 at ≤4 edges. Every certificate is checked by
  an independently implemented verifier. The R2 artifact independently
  replays two legal two-step paths, but it does not prove minimum merge
  depth; its seeds also share a one-step successor.
- **Hand theorem, pending scrutiny:** collision is governed by *history ambiguity* —
  whether some image can be "read backwards" at a different location than
  the one that produced it, yielding a different predecessor. Across every
  rule and tier tested, ambiguity was necessary for collision with zero
  exceptions. An elementary proof now shows that semantic D1 plus
  history-unambiguity implies one-step injectivity. A generic Lean proof and
  the sharper converse/dichotomy question remain open.

## Why I think this matters for multiway systems

Branch merging is usually discussed here as a *feature* (confluence,
causal invariance, quantum interpretations). This example isolates merging
of two non-isomorphic, mutually unreachable source states despite each
application carrying its own comatch undo data. In
Garden-of-Eden terms: for cellular automata on fixed geometry there is a
century of theory linking local injectivity properties to global ones
(Moore–Myhill, Gottschalk, Gromov); for rewriting that changes its own
geometry, that theory appears not to exist yet. The nearest work
(Arrighi et al. on reversible causal graph dynamics and space-time
reversible rewriting) *designs* reversibility in via context-preservation
conditions. The splice rule shows that removing context preservation can
permit reversibility to fail, even census-preservingly; it does not show
failure is necessary for every rule outside that class.

Everything — code, 15 independently replayed certificate files (14 unique
contents), sweep logs, the Lean
proof, and a working-draft note — is public:

- Repository: https://github.com/walkthroughwonder/discrete-jacobian
- Archived + citable: https://doi.org/10.5281/zenodo.21630926

I'd especially welcome an independent review or generic Lean formalization
of the Rigidity Theorem, a corrected minimum-depth R2 certificate,
richer-tier searches, and a branchial visualization of the splice
collision.

*Disclosure: this project was carried out with AI assistance from Anthropic
Claude and OpenAI Codex, including searches, code, the concrete Lean proof,
and this post. The certificates are independently replayed; the concrete
Lean claims listed above are formalized, while the general rigidity theorem remains
a hand proof pending scrutiny.*
