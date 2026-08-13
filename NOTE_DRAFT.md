# Application-level undoability need not prevent global state collisions:
# explicit certificates, a machine-checked splice collision, and a human rigidity theorem

*Draft v1.1, revised 2026-08-12. Author: Edwin Rosero
(walkthroughwonder), with AI assistance from Anthropic Claude and OpenAI
Codex disclosed. Status: public working draft — not peer reviewed;
comments and corrections welcome via repository issues.*

## Abstract

A polynomial map with everywhere-invertible differential can fail to be
globally injective: the July 2026 counterexample to the Jacobian conjecture
realizes this with a generically 3-to-1 map ℂ³ → ℂ³. We study the discrete
analogue for hypergraph rewriting. We define semantic D1 as the global
condition that every application is uniquely undoable from its result and
comatch region. The implementation tests it only over a declared finite
probe of states with at most 4 vertices and 3 edges. The splice rule passes
that probe and produces an explicit policy-independent collision on
isomorphism classes. The flagship
"splice" collision (one rule, two 3-edge states) is formalized in Lean 4
and checked against a pinned Mathlib revision with no `sorry`s. This Lean
file proves the concrete collision, source non-isomorphism, successor-class
agreement, and terminality for S1 successors; it does not formalize the
symmetric terminality fact, mutual unreachability, or semantic D1. An
exhaustive
sweep of 489 small rules identifies *history ambiguity* — the existence of
a reverse-match at a support other than the comatch yielding a different
predecessor — as necessary for collision, first empirically (zero
exceptions across all tiers) and then by a human-readable elementary theorem: a
semantically locally-invertible, history-unambiguous rule has one-step
evolution injective on isomorphism classes. The converse (a dichotomy)
remains open. The general theorem is pending external review or generic
Lean formalization. We position
the results as sharpness witnesses for the sufficient reversibility
conditions of Arrighi, Costes and Maignan, and state the Moore–Myhill
question for dynamic topology, which appears to be open.

## 1. Introduction

[Motivation: Jacobian counterexample (Alpöge 2026); the mechanism is a
nonproper, generically three-to-one étale map — local invertibility
everywhere, global sheet collision.
Question: does the analogous local-to-global inference hold for graph
rewriting? For cellular automata on fixed geometry, partitioned/block
constructions show locally-permutation structure forces global bijectivity;
for *dynamic* topology the question appears unexamined.]

Contributions, calibrated (the mathematics is elementary once seen; the
value is in locating the boundary precisely):

- **C1.** A definitional framework separating three grades of local
  invertibility (syntactic D1, semantic D1, context-preservation), with
  witnesses that each gate does real work.
- **C2.** Minimal explicit census-preserving collision examples whose
  rules pass the declared bounded semantic-D1 probe. Lean checks the
  flagship's concrete collision and policy independence; unconditional
  mutual unreachability is supplied by the hand proof.
- **C3.** Exhaustive bounded empirics: 489 rules, of which 238 pass the
  semantic-D1 probe over states with ≤4 vertices and ≤3 edges, with a
  two-implementation verification pipeline.
- **C4.** The Rigidity Theorem (unambiguous ⟹ injective), with an elementary
  hand proof pending external or generic Lean review, and the
  dynamic-topology Garden-of-Eden question.

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

Rule: {(a,a),(b,c)} → {(a,b),(c,a)}, a,b,c distinct. It preserves edge and
matched-vertex counts and passes the declared bounded semantic-D1 probe;
no unbounded semantic-D1 proof is currently claimed.

States S₁ = {(0,0),(1,2),(1,3)}, S₂ = {(0,0),(1,2),(3,2)}.

**Theorem.** S₁ ≇ S₂; each has successors, all four applications yield
directed 4-paths (one isomorphism class); successors are terminal, hence
S₁, S₂ are mutually unreachable unconditionally. Evolution on isomorphism
classes is therefore well-defined at S₁, S₂ and not injective.

[Proof: PROOF_flagship.md, three steps, no computation needed. Lean 4
formalization: SpliceCollision.lean — theorems splice_collision,
S1_not_iso_S2, succ_S1_iso_P4, succ_S2_iso_P4, succ_S1_terminal; compiles
against the pinned Mathlib revision with zero `sorry`s. The symmetric
terminality fact and mutual unreachability have a short hand proof.
Semantic D1 is a separate bounded sweep claim, not a theorem in this Lean
file.]

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
- 489 rules → 238 non-identity survivors of the semantic-D1 probe on all
  enumerated states with ≤4 vertices and ≤3 edges.
- Tier (≤4v, ≤3e): 52 rules collide (77 INDEPENDENT pairs; 32 from
  edge-count-preserving rules; 12 rules fully census-preserving AND
  policy-independent). 13 certificates machine-verified.
- Tier (≤5v, ≤3e): same 52 colliders; zero unambiguous colliders.
- Tier (≤4v, ≤4e): collisions explode to 182/238 with one extra edge of
  probe room; still zero unambiguous colliders. Only one rule remains
  history-unambiguous at this tier — {(a,a),(b,b)} → {(a,b),(b,a)}, "fuse
  two loops into a 2-cycle" — and it is collision-free in that tier,
  consistent with the theorem but not an unbounded verification of its
  hypotheses.
  Its unambiguity has a structural explanation: its RHS symmetry (a ↔ b)
  acts trivially on the predecessor, so distinct reverse-readings agree.
- R2 (multiway): 87/226 systems show bounded merges of seeds classified as
  mutually unreachable within the search bounds. Of 123 logged examples,
  55 were detected by the original one-step policy-image test and 68 were
  not. The historical artifact `cert_deep_r2.json` independently replays
  two legal two-step paths to a common witness, but does not establish
  minimum merge depth: its seeds also share a one-step successor.

## 5. The Rigidity Theorem — human proof, not yet Lean-formalized

Empirics: history ambiguity is necessary for collision in every tier tested
(zero false negatives across 238 rules × 4 tiers); it is not sufficient
(ambiguous-but-rigid rules persist through tier (5,4)).

**Theorem (Rigidity, hand proof pending scrutiny).** A semantically
locally-invertible rule with no
history ambiguity has injective one-step evolution on isomorphism classes —
under every updating policy, including the successor relation itself.

*Proof sketch* (full proof: PROOF_rigidity.md): suppose two applications
have isomorphic results. Transport the DPO undo of the second application
along the isomorphism into the first result, and compare its support with
the first comatch: if equal, semantic D1 forces the predecessors to agree;
if different, history-unambiguity forces the same. Either way the sources
are isomorphic. The empirical record (zero unambiguous colliders) is
thereby explained rather than merely observed.

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
governing a global injectivity property. The proof shows that unambiguity
forces every one-step collision to factor through an isomorphism of
sources. A generic Lean formalization remains future work.]

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
elementary mechanism, calibrated claims (A4); R2 paths certified but
minimum-depth claims not established; general rigidity proof not yet
formalized or externally reviewed.

## Reproducibility

[Repo: code (searcher, independent verifier with self-tests), 13 distinct
R1 certificates plus one R2 path artifact, sweep logs for every tier, Lean proof, and this document's
full provenance. All experiments single-machine, minutes-scale.]
