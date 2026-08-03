# The Rigidity Theorem (formerly the weak-form conjecture)

*2026-07-27. The "conjecture" turns out to be a theorem with an elementary
proof — the definitions, once forced into their final shape by the Phase 1–2
experiments, contain it.*

**Theorem.** Let ρ be a rewrite rule that is semantically D1 and
history-unambiguous at a state S₁ (for a given application). If a state S₂
admits an application of ρ whose result is isomorphic to the result of that
application of S₁, then S₂ ≅ S₁.

Consequently, for rules satisfying the hypotheses at every state: the
one-step successor relation is injective up to isomorphism — no policy
collisions (under any updating policy), no INDEPENDENT pairs, no DOWNSTREAM
pairs, and no one-step R2 merges of distinct states.

**Proof.** Let a₁ : S₁ → T₁ be the given application with comatch region c₁,
and a₂ : S₂ → T₂ an application with comatch c₂, with an isomorphism
φ : T₂ → T₁.

By the DPO undo fact (verified in `core.undo_at_comatch_ok` for every rule),
the reverse rule ρ⁻¹ has a match in T₂ supported on c₂ whose application
yields S₂ exactly. Matching and application commute with isomorphisms, so
ρ⁻¹ has a match in T₁ supported on φ(c₂) whose result is isomorphic to S₂.

Compare supports inside T₁:

- **If φ(c₂) = c₁** (same edge-instance set): semantic D1 at a₁ says all
  reverse-matches supported exactly on c₁ yield one predecessor, and DPO
  says one of them yields S₁. Hence S₂ ≅ S₁.
- **If φ(c₂) ≠ c₁**: history-unambiguity at a₁ says every reverse-match
  supported on a region other than c₁ yields a predecessor isomorphic to
  S₁. Hence S₂ ≅ S₁. ∎

**Remarks.**

1. The hypothesis is *local*: unambiguity is only needed at the specific
   application whose result is shared. The global statement follows by
   quantifying.
2. This explains the perfect empirical record (zero unambiguous colliders
   across 238 rules × four tiers): it could not have been otherwise. The
   experiments were rediscovering a theorem.
3. The empirical labels "unambiguous" are probe-bounded approximations of
   the theorem's hypothesis; a rule labeled unambiguous in range might be
   ambiguous at larger states. The theorem itself is exact and unbounded.
4. *(Superseded 2026-08-03 — see WITNESS_ANALYSIS.md.)* The converse is
   now CLOSED at the successor-relation level: for the studied class,
   a replayable witness with non-isomorphic predecessor is literally a
   one-step relation-merge, and conversely (Proposition B). The naive
   converse fails for a different reason than first suspected — witness
   replay can be blocked by fresh-vertex re-binding (the "phantom
   witness" obstruction, Proposition A's complement). What remains open
   is the POLICY dichotomy: does independent ambiguity (D-IA) force a
   min-successor collision of mutually unreachable states at some tier?
5. The proof is two case-splits over an exhaustive support comparison; a
   Lean formalization is plausible once matching/application are formalized
   generically (a bigger infrastructure lift than the concrete splice
   proof, but well-defined).
6. **Hypothesis made explicit (2026-08-03).** The step "DPO says one of
   them yields S₁" uses that some *fresh* reverse-match supported on the
   comatch recovers the source — true when vars(L) ⊆ vars(R) (syntactic
   D1), because then the reverse rule freshens no variable and the
   retained-binding undo is realized by a fresh match. For rules outside
   syntactic D1 the step can fail (the reverse of the replay obstruction
   in WITNESS_ANALYSIS.md §2). Every rule in the swept class passes the
   syntactic-D1 gate before semantic D1 is tested, so nothing claimed is
   affected; the theorem statement should be read with "semantically D1"
   meaning the gated combination (syntactic + semantic), as implemented.

**Status.** Elementary and short enough to be checked by eye; not yet
externally reviewed. Treat as "theorem with proof, pending scrutiny" in all
external claims until a second reader (or a Lean formalization of the
general framework) confirms.
