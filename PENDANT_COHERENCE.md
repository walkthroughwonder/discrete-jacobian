# Partial results toward pendant coherence (the Q5 hard core)

*2026-08-03, late session. Two lemmas proved and machine-checked; the
conjecture reduces to a sharp combinatorial kernel. Rules concerned:
the out-pendant grower ρ→ : {(a,b)} → {(a,b),(b,c)} and its mirror
ρ← : {(a,b)} → {(a,b),(c,a)}; edge-reversal (x,y) ↦ (y,x) is a
bijection of states commuting with matching and application and maps
ρ→ to ρ←, so every statement below transfers to ρ← verbatim.*

**Definitions.** A *sink-leaf edge* of a state X is an edge (v,w) whose
leaf w has out-degree 0 and in-degree 1 in X. (A loop (w,w) is never a
sink-leaf: its vertex has out-degree ≥ 1.) A state is *pendant-free*
if it has no sink-leaf edge. The *core* of X, core(X), is the result of
deleting sink-leaf edges repeatedly until none remains.

**Lemma 0 (core well-defined).** The stripping process is terminating
and locally confluent, so core(X) is independent of deletion order.
*Proof.* Termination: each step deletes an edge. Local confluence: let
e = (v,w) and e′ = (v′,w′) be distinct sink-leaf edges of X. Their
leaves are distinct (w = w′ would give w in-degree ≥ 2) and neither
leaf is the other's support (w has out-degree 0, so w ≠ v′; likewise
w′ ≠ v). Deleting e therefore leaves e′ a sink-leaf and vice versa,
and both orders reach X − e − e′. Newman's lemma applies. ∎

**Lemma A (pendant-free rigidity).** If S₁ and S₂ are pendant-free and
share a one-step successor up to isomorphism (under ρ→), then S₁ ≅ S₂.
In particular pendant-free states admit no relation-merge at all —
under any policy, and before any policy is chosen.
*Proof.* Let T = S₁ + p₁ realize the shared successor, where
p₁ = (v₁,w₁) is the added pendant — a sink-leaf of T, since w₁ is
fresh. Transporting the second application along the isomorphism,
T = S₂′ + p₂′ with S₂′ ≅ S₂ and p₂′ a sink-leaf of T. If p₂′ = p₁ then
S₂′ = T − p₁ = S₁ and we are done. Otherwise p₂′ ≠ p₁ as edge
instances; then p₁ ∈ S₂′ = T − p₂′, and p₁ is still a sink-leaf there
(deleting p₂′ touches neither w₁, which has out-degree 0 and so is not
p₂′'s support vertex, nor p₁ itself). So S₂′ — hence S₂ — is not
pendant-free, a contradiction. ∎

**Lemma B (core conservation).** For every application S → T of ρ→,
core(T) = core(S). Hence core is a conserved quantity of the entire
successor RELATION: states in the same multiway orbit, and a fortiori
any two states sharing a successor, have isomorphic cores.
*Proof.* T = S + p with p a sink-leaf of T. One admissible stripping
sequence of T deletes p first, reaching S, and then continues to
core(S). By Lemma 0 all stripping sequences of T reach the same
normal form, so core(T) = core(S). ∎

**Machine checks (2026-08-03).** On the full (5,4) census (333 states):
core conservation holds along every successor of every state
(0 violations), and no two of the 160 pendant-free states share any
successor (0 violations).

## What the lemmas say about the phenomenon

Every relation-merge of ρ→ — hence every D-IA pair, hence any would-be
policy collision — lives inside a single core class. The evolution
NEVER forgets the core; what it forgets is exactly the pendant
decoration history. The discrete monodromy of the pendant growers is
therefore localized: information loss is confined to the decoration
layer, and the core rides along as an absolutely conserved skeleton.
(This also gives structural meaning to the hard core's resistance:
policies only ever choose among decorations of one fixed skeleton.)

The same proof scheme should apply to the other growers with their own
stripped feature (loop-at-tail core, doubled-edge core) — but for
those rules the max policy DOES collide at (4,4), so conservation
alone cannot yield coherence; whatever separates the pendant rules
must involve the fresh vertex. Candidate mechanism: pendant addition
grows |V|, and canonical relabeling of the enlarged vertex set places
the new leaf at a position determined by the pair (core, decoration)
alone.

## The open kernel

**Pendant coherence conjecture, reduced form.** Fix a core C. For each
canonical order-statistic policy π, the map
    (decoration class D of C) ↦ π-extension of the state (C, D)
is injective. Equivalently: if T = F_π(S₁) = F_π(S₂) then the two
pendant-deletions of T that invert the applications are equivalent
under Aut(T).

Status: open. Supported by censuses through (5,5) and (6,4) under both
min and max; the (6,5)/(5,6) stress under both policies is running
(`phase1/q5_core_stress.py`). A refuting pair, if one exists, must by
Lemmas A/B consist of two same-core, differently-decorated states —
which is precisely where a targeted search should look next if the
census stress stays dry: enumerate decorations of a fixed small core
directly, escaping the global census size limit.
