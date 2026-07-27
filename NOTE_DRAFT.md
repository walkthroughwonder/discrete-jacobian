# Locally invertible graph rewriting need not be globally injective:
# explicit certificates, a machine-checked splice collision, and a rigidity conjecture

*Draft v1, 2026-07-27. Author: Edwin Rosero (walkthroughwonder), with
AI assistance (Claude, Anthropic) disclosed throughout. Status: internal
draft — NOT for distribution until Edwin approves.*

## Abstract

A polynomial map with everywhere-invertible differential can fail to be
globally injective: the July 2026 counterexample to the Jacobian conjecture
realizes this with a generically 3-to-1 map ℂ³ → ℂ³. We study the discrete
analogue for hypergraph rewriting. We define a semantic notion of local
invertibility for double-pushout-style rewrite rules (every application is
uniquely undoable from its result and comatch region) and exhibit explicit,
minimal certificates that it does not imply injectivity of the induced
evolution on isomorphism classes — even for rules preserving both edge and
vertex counts, and even when every state involved has a unique successor up
to isomorphism, so that no updating-policy choice is involved. The flagship
"splice" collision (one rule, two 3-edge states) is formalized in Lean 4
and checked against Mathlib with no unproven obligations. An exhaustive
sweep of 489 small rules identifies *history ambiguity* — the existence of
a reverse-match at a support other than the comatch yielding a different
predecessor — as empirically necessary for collision (52/52 colliding rules
ambiguous; all 56 unambiguous rules rigid at every tier tested), motivating
a rigidity conjecture in the spirit of Garden-of-Eden theory. We position
the results as sharpness witnesses for the sufficient reversibility
conditions of Arrighi, Costes and Maignan, and state the Moore–Myhill
question for dynamic topology, which appears to be open.

## 1. Introduction

[Motivation: Jacobian counterexample (Alpöge 2026); the mechanism is a
branched cover — local invertibility everywhere, global branch collision.
Question: does the analogous local-to-global inference hold for graph
rewriting? For cellular automata on fixed geometry, partitioned/block
constructions show locally-permutation structure forces global bijectivity;
for *dynamic* topology the question appears unexamined.]

Contributions, calibrated (the mathematics is elementary once seen; the
value is in locating the boundary precisely):

- **C1.** A definitional framework separating three grades of local
  invertibility (syntactic D1, semantic D1, context-preservation), with
  witnesses that each gate does real work.
- **C2.** Minimal explicit counterexamples: semantically locally-invertible,
  census-preserving rules whose evolution on isomorphism classes merges
  non-isomorphic, mutually-unreachable states. The flagship is
  machine-checked in Lean 4 / Mathlib (zero sorries), including
  policy-independence and unconditional unreachability via terminality.
- **C3.** Exhaustive small-scale empirics (489 rules; 238 semantic-D1
  survivors) with a two-implementation verification pipeline, identifying
  history ambiguity as empirically necessary for collision.
- **C4.** The Rigidity Conjecture (unambiguous ⟹ injective) and the
  dynamic-topology Garden-of-Eden question, with positioning against the
  causal-graph-dynamics and space-time-reversible-rewriting literature.

## 2. Definitions

[States: finite multisets of ordered edges over anonymous vertices,
considered up to isomorphism — the standard semantics for Wolfram-model
rewriting and consistent with CGD's "pointed graphs modulo." Named-graph
nuance stated explicitly per review item A2: on named graphs the successor
is not even single-valued; uniqueness and the collision both live at the
isomorphism level.]

**Rules and application** (DPO-style, injective matching). [Standard.]

**Syntactic D1**: vars(L) ⊆ vars(R) — no matched vertex forgotten.
**Semantic D1**: additionally, every reverse-match supported exactly on the
comatch region yields the same predecessor. [Chain-step witness shows the
gap between the two.] We note plainly: this is *our* definition of local
invertibility; Arrighi-style context-preservation is strictly stronger and
excludes the rules below — that exclusion is the subject of §6.

**Collision classes**: policy-independent vs policy-relative;
INDEPENDENT (mutually unreachable) vs DOWNSTREAM; orbit-artifact guard.
[Definitions as in the program's DEFINITIONS.md, tightened.]

**History ambiguity**: a rule is history-ambiguous if some application's
result admits a reverse-match at a support different from the comatch whose
predecessor is not isomorphic to the source.

## 3. The splice collision (main example)

Rule: {(a,a),(b,c)} → {(a,b),(c,a)}, a,b,c distinct. Edge- and
vertex-preserving; semantic D1.

States S₁ = {(0,0),(1,2),(1,3)}, S₂ = {(0,0),(1,2),(3,2)}.

**Theorem.** S₁ ≇ S₂; each has successors, all four applications yield
directed 4-paths (one isomorphism class); successors are terminal, hence
S₁, S₂ are mutually unreachable unconditionally. Evolution on isomorphism
classes is therefore well-defined at S₁, S₂ and not injective.

[Proof: PROOF_flagship.md, three steps, no computation needed. Lean 4
formalization: SpliceCollision.lean — theorems splice_collision,
S1_not_iso_S2, succ_S1_iso_P4, succ_S2_iso_P4, succ_S1_terminal; compiles
against Mathlib with zero sorries.]

Mechanism: the P₄ image does not remember which interior vertex was the
spliced loop. The forgotten comatch is the discrete monodromy — the exact
analogue of the forgotten branch in the ℂ³ counterexample.

## 4. Exhaustive small-scale sweep

[Methodology: rule classes A/B/B+; two D1 gates; orbit-artifact and
downstream classification; independent verifier sharing no code with the
searcher. Methods footnote per review item A6: the verifier initially
rejected all certificates due to a bug in the *verifier's* canonical form;
the disagreement between implementations is what surfaced it; verifier
self-tests added; full pipeline and logs published for third-party re-run.]

Numbers (all tier-stamped, "in range" only):
- 489 rules → 238 semantic-D1 non-identity survivors.
- Tier (≤4v, ≤3e): 52 rules collide (77 INDEPENDENT pairs; 32 from
  edge-count-preserving rules; 12 rules fully census-preserving AND
  policy-independent). 13 certificates machine-verified.
- Tier (≤5v, ≤3e): same 52 colliders; zero unambiguous colliders.
- Tier (≤4v, ≤4e): collisions explode to 182/238 with one extra edge of
  probe room; still zero unambiguous colliders. Only one rule remains
  history-unambiguous at this tier — {(a,a),(b,b)} → {(a,b),(b,a)}, "fuse
  two loops into a 2-cycle" — and it is rigid, as the conjecture requires.
  Its unambiguity has a structural explanation: its RHS symmetry (a ↔ b)
  acts trivially on the predecessor, so distinct reverse-readings agree.
- R2 (multiway): 87/226 systems show merges of mutually-unreachable seeds;
  of 123 examples, 55 reduce to one-step collisions, 68 are genuinely
  multi-step. One deep merge is certified and independently replayed
  (cert_deep_r2.json: the "unsplice" rule {(a,b),(b,c)} → {(a,a),(c,b)},
  two seeds two steps each to a common witness; nine-check verification).

## 5. The Rigidity Conjecture

Empirics: history ambiguity is necessary for collision in every tier tested
(zero false negatives across 238 rules × 3 tiers); it is not sufficient
(130 ambiguous rules rigid in range).

**Conjecture (weak form).** A semantically locally-invertible rule with no
history ambiguity has injective one-step evolution on isomorphism classes.

**Open question (dichotomy).** Is history ambiguity *equivalent* to
eventual collision? The evidence is mixed in an instructive way: one extra
edge of probe room converts most rigid rules to colliders (52 → 182 of 238
from tier (4,3) to (4,4)), yet the 55 rules that remain ambiguous-but-rigid
at (4,4) ALL survive the richer (5,4) tier (333 states; positive control:
the splice shows 23 collision images there). So ambiguity alone is
demonstrably not sufficient in range, and the refined criterion worth
formalizing is *independent ambiguity*: an alternative reverse-reading
whose predecessor is not merely non-isomorphic but unreachable-independent
of the original. We leave the refinement as the immediate next step.

[Discussion: Garden-of-Eden-shaped — a local combinatorial condition
governing a global injectivity property. The weak form's proof should show
unambiguity forces every collision to factor through an isomorphism of
sources (the loops-to-2-cycle rule illustrates the mechanism: RHS symmetry
acting trivially on histories). A refutation needs an explicit
certificate.]

## 6. Positioning and the open question

[Per POSITIONING.md: Arrighi–Costes–Maignan give sufficient local
conditions (context-preservation + operator injectivity) for space-time
reversibility; the splice violates context-preservation; our certificates
show the failure is genuine, not an artifact of proof technique — i.e.
sharpness witnesses. Arrighi–Martiel–Perdrix impose global bijectivity
(their Def. 7) and derive structure; their intro explicitly cites the
pre-injectivity/surjectivity (Garden-of-Eden) literature for fixed Cayley
graphs and pivots to bijectivity-assumed questions.]

**Open question (Garden of Eden for dynamic topology).** For a suitable
class of rewriting systems closed under reversal (D2), is surjectivity of
the evolution equivalent to pre-injectivity? To our knowledge no result of
this type exists for rewriting that modifies its own underlying geometry.

## 7. Limitations

Definition-relative (A1); bounded sweeps with tier-stamped claims only
(A5); isomorphism-level semantics with the named-graph nuance (A2);
elementary mechanism, calibrated claims (A4); multi-step (R2) monodromy
observed but not yet certified end-to-end.

## Reproducibility

[Repo: code (searcher, independent verifier with self-tests), 13 + 1
certificates, sweep logs for every tier, Lean proof, and this document's
full provenance. All experiments single-machine, minutes-scale.]
