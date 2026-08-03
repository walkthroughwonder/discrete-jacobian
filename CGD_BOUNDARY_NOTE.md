# CGD boundary note — where Arrighi–Martiel–Perdrix stops and this program starts

*2026-08-03. Discharges VERDICT.md reading obligation #2 (the Natural
Computing 2020 CGD paper). Source: arXiv:1502.04368v3, "Reversible
Causal Graph Dynamics: Invertibility, Vertex-preservation, Block
representation" (= Natural Computing 19 (2020); merges RC 2016 + FCT
2015 — theorem NUMBERS differ across versions, so cite results by NAME
on the call). All quotes verbatim from the ar5iv full text.*

## 1. Their framework (every theorem quantifies over this)

Configurations are **pointed, connected, bounded-degree, port-wired
graphs modulo isomorphism**: finite port set π (degree ≤ |π|, each port
used at most once), finite vertex/edge label sets Σ, Δ, a privileged
origin, at most countably many vertices. This makes the configuration
space a **compact metric space** — and they say compactness is the
point: the topological characterization "is one of the crucial
ingredients to prove that the inverse of a CGD is a CGD."

A *dynamics* is a pair (F, R_•): the global map **plus** a
vertex-correspondence R_X : V(X) → V(F(X)) tracking which vertex became
which. A **CGD** is a shift-invariant, continuous (= causal), bounded
dynamics — global/topological axioms taken as primary, deliberately.

## 2. Their two notions, and the exact distinction

- **Invertible** (Def. 7): "F is a bijection over X_{Σ,Δ,π}" — global
  bijectivity of the one-step map over the entire space, imposed as an
  axiom. Nothing is asked of F⁻¹ or of R_X.
- **Reversible** (Def. 10): invertible AND the inverse, with some
  vertex-correspondence S_•, is itself a CGD.

Their theorem chain (all directions **global ⟹ local**):

- **Lemma 5**: shift-invariance + bijectivity alone ⟹ R_X preserves
  shift-equivalence of vertices. **Lemma 6**: the number of
  shift-equivalence classes is conserved (its proof imports the
  local-rule equivalence from the companion CGD paper).
- **"Invertible implies almost-vertex-preserving"** (Thm 4.1): if F is
  a bijective CGD, there is a bound p such that R_X is bijective for
  every X with |V(X)| > p. The "almost" is sharp — their "turtle"
  example is an invertible CGD oscillating between a 1-vertex and a
  2-vertex graph. The bound p comes from compactness, non-effectively.
- **"Invertible implies reversible"** (Thm 5.1): unconditionally, for
  CGD. Their own emphasis: "this result crucially relies on the
  compactness of X_{Σ,Δ,π} which in turn relies on the boundedness of
  the degree |π| and the finiteness of the internal states." Also: the
  inverse's radius is not computable from the forward radius (via
  Kari).
- **Block representation** (Thm 6.1): reversible CGD = finite-depth
  circuits of local reversible gates.

## 3. The frozen line (why our lane is genuinely open)

**Per-application/local invertibility is never defined, hypothesized,
or concluded anywhere in the paper.** Their only sentence about local
rule injectivity says the opposite is normal: the RCA local rule "by
definition is not injective" — global reversibility with non-injective
local rules is their default picture, and the block representation
exists to *recover* local reversibility from global bijectivity. The
converse question — whether local invertibility of a rule forces
global injectivity — is unasked in the text. That is exactly the
discrete Jacobian question, and the splice answers it negatively the
moment one leaves their axiom set.

**Honest sharpness framing** (use this wording): our examples do not
contradict any theorem of theirs — the hypotheses never overlap. They
show the phenomenon their axioms exclude *by fiat* (global bijectivity
is an input, never derived) actually occurs in unpointed, unbounded-
degree, DPO-style rewriting with per-application undoability. And the
two programs are mirror images on matter conservation: **they prove
global invertibility forces (almost) vertex-preservation; we prove
census-preservation does not force global invertibility** (18 of 105
fully census-preserving semantic-D1 rules collide; splice is
vertex- and edge-preserving).

## 4. Garden of Eden: Q4's openness survives contact with the text

Verified by grep over the full text: **"Moore", "Myhill",
"surjunctiv-", "Garden", "Eden" appear nowhere in the paper.** Their
entire contact with that circle is one introduction sentence citing
Gromov [14] (pre-injectivity ⟹ surjectivity for certain Cayley
graphs), from which they explicitly pivot: "This paper on the other
hand provides a context in which to study 'bijectivity upon
time-varying graphs'." So: the fixed-geometry GoE literature is cited
in one sentence and the bijectivity-assumed fork is taken — Edwin's
formulation in the 07-27 email to Arrighi is accurate, with the
precision that it is one Gromov citation, not a survey. **No
Moore–Myhill-type statement for dynamic topology exists in this
paper.** Q4 remains open as far as this source is concerned.

## 5. Their open edges (conversation hooks for the call)

1. "Future work" (verbatim): the result "could perhaps be understood
   as a 'Matter conservation theorem', à la Lavoisier. Still, this
   cannot forbid that some 'dark matter' which was there at all times,
   could now be made 'visible'. We plan to follow this idea in a
   subsequent work." Plus the quantum regime (their QCGD line).
2. Restricted state spaces (forbidden-disk subspaces stay compact):
   "theorems of this paper will carry through, **except perhaps that of
   the block representation**" — an explicitly unresolved edge.
3. Their conjecture that CA embed into CGD preserving invertibility if
   Σ may be extended — stated as unresolved.

## 6. One-line summary for the Zoom

Their theory: global bijectivity in, local structure out — on a
compact, bounded-degree, pointed space. Our theory: local
invertibility in, global injectivity *fails* — off that space; the
Rigidity Theorem + D-IA dichotomy then locate exactly which local
condition (history-unambiguity) restores injectivity, and Q5 is what
remains. The two directions compose rather than compete.
