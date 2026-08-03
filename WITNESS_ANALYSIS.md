# Witness anatomy, replayability, and independent ambiguity (D-IA)

*2026-08-03 (analysis begun 2026-07-28). Sharpens the dichotomy question
left open in PROOF_rigidity.md by decomposing history ambiguity at the
level of individual witnesses. Code: `phase1/independent_ambiguity.py`;
data: `phase1/ia_holdouts_4_4.jsonl`, `phase1/ia_colliders_4_4.jsonl`.*

## 1. Witness anatomy

A **history-ambiguity witness** for a rule ρ is a tuple (S, m, T, m2, P):
a state S, a match m whose traced application yields T with comatch
region c, and a reverse-match m2 in T supported on an edge set ≠ c whose
application yields a predecessor P with P ≇ S. The rule-level predicate
used throughout the sweeps ("ambiguous") is: some witness exists among
the probe states.

The dichotomy question asked whether ambiguity forces collision. The
witness-level analysis splits that question along two independent axes.

## 2. The replay obstruction (a negative result)

It is tempting to argue: by the DPO undo fact, the forward rule applied
to P at the comatch of the reverse application returns T, so every
witness exhibits one-step non-injectivity of the successor relation
({S, P} → T). **This argument is wrong for vertex-creating rules.** The
undo needs the *retained binding* of the reverse application: replaying
ρ forward from P by fresh matching re-binds vars(R)\vars(L) to fresh
vertices, so the replayed image can differ from T (even up to iso) when
the forward-created vertices were entangled with the rest of the state.
The monodromy that powers the whole program cuts both ways.

Call a witness **replayable** if [T] ∈ successors([P]) genuinely (checked
by forward search, not assumed). Empirically at the (4,4) probe tier:

- the 55 ambiguous-but-rigid holdouts carry 774 phantom
  (non-replayable) witness pairs out of 3320 total — the replay
  obstruction is doing real work, not corner-case work;
- the splice flagship (fully variable-preserving) has every witness
  replayable, as Proposition A predicts.

**Proposition A (replay).** If vars(R) ⊆ vars(L), every witness is
replayable — indeed the fresh forward match at the comatch region of the
reverse application reproduces T exactly.

*Proof.* The comatch region of the reverse application consists of
L-pattern edges created under the retained binding b. Fresh matching of
L against those edges recovers (at least) b restricted to vars(L);
applying ρ there re-creates the R-edges under b — no variable needs a
fresh vertex since vars(R) ⊆ vars(L) — and leaves the context untouched,
reproducing T edge-for-edge. ∎

## 3. The hidden hypothesis in the Rigidity Theorem

The dual subtlety affects the *reverse* direction. PROOF_rigidity.md's
step "DPO says one of them yields S₁" — that some fresh reverse-match
supported on the comatch yields the source exactly — holds when
vars(L) ⊆ vars(R) (syntactic D1): then the reverse rule freshens
nothing, and the argument of Proposition A applies verbatim with the
roles of L and R swapped. For rules with vars(L) ⊄ vars(R) the step can
fail, and the theorem's proof needs the hypothesis stated.

**This does not retract anything**: every rule in the swept class passes
the syntactic-D1 gate (vars(L) ⊆ vars(R)) before semantic D1 is even
tested, so the Rigidity Theorem as applied is sound. But the theorem
statement should carry "syntactic D1" (or equivalently "some fresh
reverse-match at the comatch recovers the source") as an explicit
hypothesis. PROOF_rigidity.md has been amended accordingly.

## 4. Causal classification and the definition of D-IA

For a replayable witness, {[S], [P]} → [T] is a genuine one-step merge.
Whether it can ever count as a *collision* depends on the causal
relation between S and P (bounded BFS, same bounds as the sweep's
artifact quarantine):

- **orbit**: S and P mutually reachable — the ambiguity only rewinds
  within one orbit; quarantined as an artifact by every sweep;
- **oneway**: one direction reachable;
- **independent**: mutually unreachable — the analogue of the sweep's
  INDEPENDENT pairs.

**Definition (D-IA).** A rule has **independent ambiguity** if some
witness is both replayable and independent.

**Proposition B (witness ⟺ pair).** For rules with vars(L) ⊆ vars(R)
(syntactic D1) that are semantically D1: S admits a replayable witness
with alternative predecessor P **iff** ([S], [P]) is a one-step
collision pair of the successor relation on isomorphism classes, and
the correspondence preserves the causal class. Hence:

    D-IA  ⟺  some INDEPENDENT one-step relation-merge exists.

*Proof.* (⟹) Replayability is exactly [T] ∈ succ([P]); [T] ∈ succ([S])
by construction; [P] ≠ [S] by the witness condition. (⟸) Given
applications a : S → T₁, a' : P → T₂ and φ : T₂ ≅ T₁, transport the
comatch c₂ of a' along φ. By syntactic D1 and the swapped Proposition A,
some fresh reverse-match at φ(c₂) in T₁ yields ≅ P. If φ(c₂) ≠ c₁ this
is a witness at S with alternative predecessor P, replayable via a'. If
φ(c₂) = c₁, the comatch support carries fresh reverse-matches yielding
both S and ≅ P ≇ S — contradicting semantic D1. Causal class is
preserved because the pair ([S], [P]) is literally the same. ∎

So at the **relation level** the dichotomy is *closed* for the studied
class: injectivity ⟺ no replayable witness with non-isomorphic
predecessor; independent merges ⟺ D-IA. What remains genuinely open is
the **policy level**:

> **Open (policy dichotomy).** Does D-IA force a min-successor-policy
> collision between mutually unreachable states at some tier?

A D-IA pair can be *policy-shielded*: f_min diverts S or P to a
different successor, so the relation-merge never surfaces as an R1
collision. The empirical question is whether shielding can persist
across all tiers.

## 5. Data (probe tier (4,4); reachability bounds: 2000 states, ≤7 vertices)

Witness pairs are deduplicated on (S, P, T); per-rule cap 400 pairs.

*(Holdout row FINAL, 2026-08-03; collider control still computing —
its row lands in the follow-up commit.)*

| group | rules | pairs | orbit | oneway | independent | of which replayable (D-IA pairs) |
|---|---|---|---|---|---|---|
| ambiguous-rigid holdouts | 55 | 3320 | 2272 | 0 | 1048 | 274 |
| colliders (control) | running | — | — | — | — | — |

Headline classification of the 55 holdouts (final):

- rules with at least one D-IA pair (independent + replayable):
  **12** — each is a certified one-step relation-merge of mutually
  unreachable states that the min-successor policy shields in-range
  (policy-collide/shielded split over the 274 D-IA pairs: **0 / 274**;
  all 274 alternative predecessors lie inside the census, so census
  overflow explains nothing);
- rules whose independent witnesses are all phantom (non-replayable):
  **18**;
- rules with no independent witnesses at all (orbit-rewind only):
  **25**.

Interpretation. Holdout rigidity is not one phenomenon but three, and
the partition is exhaustive (12 + 18 + 25 = 55): (i) for 25 rules the
ambiguity never leaves an orbit — the sweeps' artifact quarantine was
already the right lens; (ii) for 18 rules every causally independent
reading is phantom — the replay obstruction of §2, i.e. rigidity by
monodromy itself; (iii) for 12 rules genuine independent relation-merges
exist and are *uniformly policy-shielded* — zero of 274 D-IA pairs
produce an f_min collision in range, with no census excuse available.
Group (iii) is the entire Q5 frontier: either shielding persists at all
tiers for these rules (a policy-rigidity phenomenon worth a theorem) or
it breaks at some tier (a collision). Notably, no oneway witnesses occur
at all in this population, and the two heaviest D-IA rules are the
edge-growing pair {(a,b)} → {(a,b),(b,c)} and {(a,b)} → {(a,b),(c,a)}
(326 witness pairs each, 296 of them phantom — growth makes most
alternative readings unreplayable, but not all).

## 6. Verification notes

- Every replayability verdict is a positive forward-search check
  ([T] ∈ successors([P]) on canonical forms), not an inference from the
  undo fact — that inference is exactly what Section 2 refutes.
- Causal classes use `search.reachable` verbatim (the sweep's artifact
  quarantine), so "independent" here means what "INDEPENDENT pair"
  means in RESULTS.md, with the same bounded-BFS caveat: bounds can
  only overcount independence, never undercount it.
- All claims are (4,4)-probe-tier claims; the propositions are exact
  and unbounded.
