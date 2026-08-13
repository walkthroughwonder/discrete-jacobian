# POSITIONING vs. the two ⚠ papers (N3, completed 2026-07-26)

## vs. Arrighi–Costes–Maignan, *Space-time reversible graph rewriting*
(arXiv:2510.03296)

Read in full (HTML v1). Their framework and ours are **complementary, not
overlapping**, in three precise ways:

1. **Their conditions exclude our rules by design.** Their sufficient local
   conditions for space-time reversibility (Prop. 2: injectivity of the
   local operator + surjectivity + back-reachability) sit on top of a
   *context-preservation* requirement — rules may not rewire how the
   rewritten region connects to its exterior — and a DAG/port-graph setting
   that is incompatible with self-loops. The splice rule
   {(a,a),(b,c)} → {(a,b),(c,a)} violates context-preservation (it re-threads
   external connectivity through a) and uses a loop. **Our collision
   example therefore probes the boundary of their assumptions:** drop
   context-preservation while retaining own-comatch undoability, and global
   reversibility can fail. The splice rule passes the declared bounded
   semantic-D1 probe; no global semantic-D1 theorem is claimed.
2. **No Garden-of-Eden theorem.** Their reversibility implies bijectivity
   within their class by construction; they prove no surjective ⟺
   pre-injective statement, and their open-questions list (simulation
   universality, relaxing past-to-future position mapping, expansive graph
   subshifts, quantum regimes) does not contain our rigidity question Q4.
   The dynamic-topology Garden-of-Eden problem remains open and unclaimed.
3. **Different nondeterminism treatment.** They achieve space-time
   determinism (schedule-independence of the unfolding); our R1/R2
   collisions live exactly in the regime their conditions rule out, where
   schedule-forgetting (the comatch monodromy) has global consequences.

## vs. Arrighi–Martiel–Perdrix, *Reversible Causal Graph Dynamics*
(arXiv:1502.04368 / Natural Computing 2020)

Full-text read (journal version, 33 pp, 2026-07-27). Confirmed at the
definition level: **Definition 7 imposes invertibility globally** ("a
dynamics (F, R•) is invertible if F is a bijection over X_{Σ,Δ,π}");
Theorem 1 then derives almost-vertex-preservation, and later sections
reversibility ⟹ block representation. Setting: pointed graphs modulo
isomorphism, bounded degree, synchronous. Crucially, their own introduction
cites the pre-injectivity ⟹ surjectivity (Garden-of-Eden) literature for
Cayley graphs as adjacent context and states "this paper on the other hand
provides a context in which to study bijectivity upon time-varying graphs"
— i.e., they explicitly took the bijectivity-assumed fork and left the
GoE fork for dynamic topology untraveled. Their guiding question ("does
bijectivity rigidify space?") is a cousin of our rigidity question, asked
in the opposite direction. No conflict; direct citation trail for our
open-problem statement. Residual obligation CLOSED.

## Consequence for the write-up

The result can be framed as: *the declared bounded semantic-D1 probe is
compatible with a concrete, Lean-checked census-preserving collision, while
space-time reversibility requires stronger context conditions; and the
Moore–Myhill question for dynamic topology is open.* Positioning sentence
for the intro: "Arrighi et al. show how to design reversible graph
rewriting; the splice example shows that when context preservation is
removed, reversibility can fail even for a census-preserving rule."

Residual obligations: skim the CGD journal PDF §definitions before any
submission; cite both lines generously.
