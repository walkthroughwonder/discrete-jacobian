/-
The splice collision, machine-checked.

Rule R (injective matching, a b c distinct):
    {(a,a), (b,c)}  →  {(a,b), (c,a)}
"Splice the loop at a into the edge b→c."

We prove: the states
    S1 = {(0,0), (1,2), (1,3)}   (loop ⊔ out-star)
    S2 = {(0,0), (1,2), (3,2)}   (loop ⊔ in-star)
are non-isomorphic, every R-successor of S1 is isomorphic to every
R-successor of S2 (all four are the directed path P₄), and successors are
terminal. Hence one-step R-evolution on isomorphism classes is well-defined
and NOT injective: a census-preserving, locally invertible rewrite rule
with a policy-independent global collision.

Companion to PROOF_flagship.md and cert_flagship.json in the
discrete-jacobian program.
-/
import Mathlib

open Finset

abbrev St := Finset (ℕ × ℕ)

/-- One application of the splice rule at match (a, b, c). -/
def RStep (s t : St) : Prop :=
  ∃ a b c : ℕ, a ≠ b ∧ a ≠ c ∧ b ≠ c ∧
    (a, a) ∈ s ∧ (b, c) ∈ s ∧
    t = insert (a, b) (insert (c, a) ((s.erase (a, a)).erase (b, c)))

def S1 : St := {(0, 0), (1, 2), (1, 3)}
def S2 : St := {(0, 0), (1, 2), (3, 2)}

/-- The canonical directed path on four vertices. -/
def P4 : St := {(0, 1), (1, 2), (2, 3)}

def emap (σ : ℕ ≃ ℕ) (e : ℕ × ℕ) : ℕ × ℕ := (σ e.1, σ e.2)

/-- Graph isomorphism (as vertex relabeling by a permutation of ℕ). -/
def IsoTo (s t : St) : Prop := ∃ σ : ℕ ≃ ℕ, s.image (emap σ) = t

lemma isoTo_symm {s t : St} (h : IsoTo s t) : IsoTo t s := by
  obtain ⟨σ, rfl⟩ := h
  refine ⟨σ.symm, ?_⟩
  have hcomp : emap σ.symm ∘ emap σ = id := by
    funext e; simp [emap]
  rw [Finset.image_image, hcomp, Finset.image_id]

lemma isoTo_trans {s t u : St} (h₁ : IsoTo s t) (h₂ : IsoTo t u) : IsoTo s u := by
  obtain ⟨σ₁, rfl⟩ := h₁
  obtain ⟨σ₂, rfl⟩ := h₂
  refine ⟨σ₁.trans σ₂, ?_⟩
  rw [Finset.image_image]
  rfl

/-- Out-degree of a vertex. -/
def outdeg (s : St) (v : ℕ) : ℕ := (s.filter (fun e => e.1 = v)).card

lemma outdeg_image (σ : ℕ ≃ ℕ) (s : St) (v : ℕ) :
    outdeg (s.image (emap σ)) (σ v) = outdeg s v := by
  unfold outdeg
  have hfilter :
      (s.image (emap σ)).filter (fun e => e.1 = σ v) =
        (s.filter (fun e => e.1 = v)).image (emap σ) := by
    ext e
    simp only [Finset.mem_filter, Finset.mem_image]
    constructor
    · rintro ⟨⟨x, hx, rfl⟩, hfst⟩
      exact ⟨x, ⟨hx, σ.injective hfst⟩, rfl⟩
    · rintro ⟨x, ⟨hx, hfst⟩, rfl⟩
      exact ⟨⟨x, hx, rfl⟩, by simp [emap, hfst]⟩
  rw [hfilter, Finset.card_image_of_injective]
  intro e₁ e₂ h
  have h1 : σ e₁.1 = σ e₂.1 := congrArg Prod.fst h
  have h2 : σ e₁.2 = σ e₂.2 := congrArg Prod.snd h
  exact Prod.ext (σ.injective h1) (σ.injective h2)

/-- Vertex 1 has out-degree 2 in S1. -/
lemma outdeg_S1 : outdeg S1 1 = 2 := by decide

/-- Every vertex of S2 has out-degree at most 1. -/
lemma outdeg_S2_le (v : ℕ) : outdeg S2 v ≤ 1 := by
  unfold outdeg
  refine Finset.card_le_one.mpr ?_
  intro e₁ h₁ e₂ h₂
  simp only [Finset.mem_filter, S2, Finset.mem_insert, Finset.mem_singleton] at h₁ h₂
  obtain ⟨he₁, hv₁⟩ := h₁
  obtain ⟨he₂, hv₂⟩ := h₂
  rcases he₁ with rfl | rfl | rfl <;> rcases he₂ with rfl | rfl | rfl <;>
    first
      | rfl
      | exact absurd (hv₁.trans hv₂.symm) (by decide)

/-- The two starting states are not isomorphic. -/
theorem S1_not_iso_S2 : ¬ IsoTo S1 S2 := by
  rintro ⟨σ, h⟩
  have h2 : outdeg S2 (σ 1) = 2 := by
    rw [← h, outdeg_image, outdeg_S1]
  have hle := outdeg_S2_le (σ 1)
  omega

-- Explicit permutations sending each successor to P4.
def σ1A : ℕ ≃ ℕ := (Equiv.swap 0 1).trans (Equiv.swap 0 2)
def σ1B : ℕ ≃ ℕ := (Equiv.swap 0 1).trans ((Equiv.swap 0 2).trans (Equiv.swap 0 3))
def σ2A : ℕ ≃ ℕ := (Equiv.swap 0 2).trans ((Equiv.swap 0 1).trans (Equiv.swap 0 3))
def σ2B : ℕ ≃ ℕ := (Equiv.swap 0 2).trans (Equiv.swap 0 1)

/-- Every R-successor of S1 is isomorphic to P4. -/
theorem succ_S1_iso_P4 (t : St) (h : RStep S1 t) : IsoTo t P4 := by
  obtain ⟨a, b, c, hab, hac, hbc, hloop, hedge, ht⟩ := h
  simp only [S1, Finset.mem_insert, Finset.mem_singleton, Prod.mk.injEq] at hloop hedge
  rcases hloop with ⟨rfl, -⟩ | ⟨h1, h2⟩ | ⟨h1, h2⟩
  · rcases hedge with ⟨rfl, rfl⟩ | ⟨rfl, rfl⟩ | ⟨rfl, rfl⟩
    · exact absurd rfl hab
    · exact ⟨σ1A, by subst ht; decide⟩
    · exact ⟨σ1B, by subst ht; decide⟩
  · omega
  · omega

/-- Every R-successor of S2 is isomorphic to P4. -/
theorem succ_S2_iso_P4 (t : St) (h : RStep S2 t) : IsoTo t P4 := by
  obtain ⟨a, b, c, hab, hac, hbc, hloop, hedge, ht⟩ := h
  simp only [S2, Finset.mem_insert, Finset.mem_singleton, Prod.mk.injEq] at hloop hedge
  rcases hloop with ⟨rfl, -⟩ | ⟨h1, h2⟩ | ⟨h1, h2⟩
  · rcases hedge with ⟨rfl, rfl⟩ | ⟨rfl, rfl⟩ | ⟨rfl, rfl⟩
    · exact absurd rfl hab
    · exact ⟨σ2A, by subst ht; decide⟩
    · exact ⟨σ2B, by subst ht; decide⟩
  · omega
  · omega

/-- Both states do step somewhere. -/
theorem S1_steps : ∃ t, RStep S1 t :=
  ⟨_, 0, 1, 2, by omega, by omega, by omega, by decide, by decide, rfl⟩

theorem S2_steps : ∃ t, RStep S2 t :=
  ⟨_, 0, 1, 2, by omega, by omega, by omega, by decide, by decide, rfl⟩

/-- THE COLLISION: distinct states, same (unique) successor class. -/
theorem splice_collision :
    (∃ t, RStep S1 t) ∧ (∃ t, RStep S2 t) ∧
    (∀ t₁ t₂, RStep S1 t₁ → RStep S2 t₂ → IsoTo t₁ t₂) ∧
    ¬ IsoTo S1 S2 :=
  ⟨S1_steps, S2_steps,
   fun _ _ h₁ h₂ =>
     isoTo_trans (succ_S1_iso_P4 _ h₁) (isoTo_symm (succ_S2_iso_P4 _ h₂)),
   S1_not_iso_S2⟩

/-- Successors are terminal: the rule needs a loop, successors have none.
With `splice_collision`, this gives unconditional mutual unreachability. -/
theorem succ_S1_terminal (t u : St) (h : RStep S1 t) : ¬ RStep t u := by
  obtain ⟨a, b, c, hab, hac, hbc, hloop, hedge, ht⟩ := h
  simp only [S1, Finset.mem_insert, Finset.mem_singleton, Prod.mk.injEq] at hloop hedge
  rintro ⟨a', b', c', hab', hac', hbc', hloop', hedge', -⟩
  rcases hloop with ⟨rfl, -⟩ | ⟨h1, h2⟩ | ⟨h1, h2⟩
  · rcases hedge with ⟨rfl, rfl⟩ | ⟨rfl, rfl⟩ | ⟨rfl, rfl⟩
    · exact absurd rfl hab
    · subst ht
      simp only [S1, Finset.mem_insert, Finset.mem_erase, Finset.mem_singleton,
        Prod.mk.injEq, ne_eq] at hloop'
      omega
    · subst ht
      simp only [S1, Finset.mem_insert, Finset.mem_erase, Finset.mem_singleton,
        Prod.mk.injEq, ne_eq] at hloop'
      omega
  · omega
  · omega
