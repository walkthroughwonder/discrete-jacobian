# The splice collision: a hand proof (flagship, cert_flagship.json)

**Rule R** (DPO, injective matching; all of a, b, c distinct):

    L = {(a,a), (b,c)}   →   R = {(a,b), (c,a)}

"Splice the loop at a into the edge b→c, threading a between them: c→a→b."
R is edge-count-preserving (2→2), vertex-set-preserving (vars {a,b,c} on both
sides — no creation, no deletion), and semantically D1 on the probe range
(sweep-checked; the reverse rule's comatch decomposition is unique).

**States** (directed multigraphs; all edges distinct so sets suffice):

    S = {(0,0), (1,2), (1,3)}      loop ⊔ out-star at 1
    T = {(0,0), (1,2), (3,2)}      loop ⊔ in-star at 2

**Claim.** S ≇ T; each has a unique successor up to isomorphism; the
successors are isomorphic; and neither state is reachable from the other.
Hence one-step evolution is a well-defined map on isomorphism classes near
S and T, and it is not injective.

## 1. The matches, exhaustively

A match needs (a,a) ∈ state. The only loop in S (and in T) is (0,0), so
a = 0. The edge (b,c) must be a non-loop edge avoiding 0, with b ≠ c:

- In S: (b,c) ∈ {(1,2), (1,3)} — two matches.
- In T: (b,c) ∈ {(1,2), (3,2)} — two matches.

## 2. The successors

Applying R removes (0,0) and (b,c), adds (0,b) and (c,0):

- S, splice (1,2): {(0,1), (2,0), (1,3)} — the directed path 2→0→1→3.
- S, splice (1,3): {(0,1), (3,0), (1,2)} — the directed path 3→0→1→2.
- T, splice (1,2): {(0,1), (2,0), (3,2)} — the directed path 3→2→0→1.
- T, splice (3,2): {(0,3), (2,0), (1,2)} — the directed path 1→2→0→3.

All four are directed paths on 4 vertices (P₄): pairwise isomorphic, with
canonical form {(0,1), (1,2), (2,3)}. So each of S and T has exactly one
successor up to isomorphism — the collision is policy-independent — and the
successors coincide.

## 3. Non-isomorphism of S and T

Out-degrees are isomorphism invariants. In S, vertex 1 has out-degree 2.
In T, every vertex has out-degree ≤ 1 (edges (0,0), (1,2), (3,2) have three
distinct sources 0, 1, 3). Hence S ≇ T. ∎

## 4. Mutual unreachability, unconditionally

Every successor of S or T is a P₄, which contains no loop. R requires a loop
(a,a) to fire, so every P₄ is terminal: the full forward orbit of S is
{S, P₄} and of T is {T, P₄}. Since T ≇ S and T ≇ P₄ (T has a loop), T is not
reachable from S; symmetrically S is not reachable from T. No bounded-search
caveat is needed. ∎

## 5. Where the information goes

Locally, each application is invertible: the reverse rule
{(a,b), (c,a)} → {(a,a), (b,c)} applied at the comatch (the two edges the
splice produced, which meet at a) uniquely restores the loop and the edge.
Globally, the resulting P₄ does not remember *which interior vertex was the
spliced loop*: S's history threads 0 between the star edges one way, T's
another, and the two distinct (state, match) histories produce literally
isomorphic results. The forgotten match datum is the discrete monodromy —
the precise analogue of the branch-of-the-cover datum in the ℂ³ Jacobian
counterexample.

## Status

The finite min-policy certificate is independently replayed. The Lean file
proves source non-isomorphism, step existence, the common successor class,
and S1-successor terminality. Semantic D1, S2-successor terminality, and
mutual unreachability are not machine-checked there; the latter two are
established by the hand argument above.
