# The Discrete Jacobian Program
## Local Invertibility Without Global Injectivity in Graph Rewriting

**Edwin Rosero**  
Meeting with Pablo Arrighi, Marin Costes & Luidnel Maignan  
11 August 2026

---

## Slide 1 – Title

**The Discrete Jacobian Program**  
Local invertibility does not imply global injectivity in graph rewriting

Edwin Rosero  
Meeting with Pablo Arrighi, Marin Costes, Luidnel Maignan  
August 11, 2026

*GitHub: github.com/walkthroughwonder/discrete-jacobian*

---

## Slide 2 – Motivation

- Classical Jacobian Conjecture (Keller, 1939):  
  Constant nonzero Jacobian determinant ⇒ global invertibility of polynomial maps

- July 2026 counterexample (Alpöge):  
  Explicit F : ℂ³ → ℂ³ with det JF ≡ −2, yet 3-to-1

- Discrete analog for (hyper)graph rewriting:  
  Does *local* invertibility of a rewrite rule imply *global* injectivity of the evolution on isomorphism classes?

---

## Slide 3 – Setting & Definitions

- **States**: finite multisets of ordered edges over anonymous vertices (up to isomorphism)
- **Rules**: double-pushout (DPO) style

**Semantic D1 (local invertibility)**  
Every application is uniquely undoable when restricted to its comatch region.

**History ambiguity**  
A reverse match exists at a support different from the comatch that produces a non-isomorphic predecessor.

---

## Slide 4 – Flagship Example: Splice Collision

**Rule**  
`{(a,a), (b,c)} → {(a,b), (c,a)}`  
“splice a loop into an edge”

**Two non-isomorphic states**  
- S₁ = loop ⊔ out-star  
- S₂ = loop ⊔ in-star  

both rewrite to the **same directed 4-path**

Properties:  
- Edge- and vertex-count preserving  
- Semantically D1  
- Unique successor up to isomorphism (policy-independent)  
- Terminal → mutually unreachable

→ Evolution on isomorphism classes is **not injective**  
The image forgets which vertex carried the loop (discrete monodromy)

---

## Slide 5 – Formal Verification & Sweep

- Lean 4 + Mathlib formalization of the splice collision (zero sorries)
- Independent verifier confirms all certificates

**Enumeration**  
489 rules → 238 semantically D1 survivors

- 52 collisions at ≤4 vertices, ≤3 edges  
- 182 collisions at ≤4 vertices, ≤4 edges

**Key observation**  
History ambiguity is necessary for collision in every tested tier (zero exceptions)

---

## Slide 6 – Rigidity Theorem

**Theorem**  
A semantically D1 rule that is history-unambiguous has injective one-step evolution on isomorphism classes (under every updating policy).

**Proof idea**  
Transport the unique DPO inverse along the isomorphism of the resulting states.  
If the supports differed, history-unambiguity would be violated.

Empirical confirmation: the only unambiguous rule at the (4,4) tier is rigid.

---

## Slide 7 – Positioning relative to Space-time Reversible Graph Rewriting

Your framework (arXiv:2510.03296) supplies **sufficient local conditions** for full space-time reversibility, including the crucial **context-preservation** requirement.

Discrete Jacobian results are complementary:
- Retain only per-application undoability (semantic D1)
- Drop context-preservation
- Explicit, census-preserving, machine-checked collisions appear

→ The splice collision (and the larger family) serve as **sharpness witnesses** for the necessity of your hypotheses.

---

## Slide 8 – Complementary Perspectives

- You show *how to design* systems that achieve space-time reversibility.
- We map the precise boundary where local invertibility ceases to guarantee global injectivity / reversibility — even for rules that preserve the exact number of vertices and edges.

Per-application invertibility is strictly weaker than space-time reversibility.  
Your conditions are not merely sufficient; they are tight in an important sense.

---

## Slide 9 – Open Questions of Shared Interest

- Dichotomy: is history ambiguity also *sufficient* for (eventual) collision?
- Garden-of-Eden / Moore–Myhill theorem for *dynamic topology*
- Intermediate notions between semantic D1 and full space-time reversibility
- Lifting rigidity results into the space-time deterministic setting
- Quantum regimes, expansive graph subshifts, simulation of reversible systems

---

## Slide 10 – Resources & Discussion

**Repository**  
https://github.com/walkthroughwonder/discrete-jacobian  
(Lean proofs, 14+ certificates, exhaustive logs, NOTE_DRAFT.md, POSITIONING.md)

**Zenodo**  
v1.0.0 release available

Happy to walk through any certificate, formalization detail, or potential joint direction.

Thank you — looking forward to your questions and the discussion.

---

*Speaker notes can be expanded on request. Suggested visuals: simple graph diagrams for S₁ / S₂ → P₄; table of sweep numbers; side-by-side comparison of conditions.*
