# PRIOR ART — Discrete Jacobian Program (Phase 0.3)

Swept 2026-07-26. Organized by distance from our question. The two "must-read
in full before any novelty claim" items are marked ⚠.

## 1. Classical rigidity theory (the theory we want to transport)

- **Moore (1962) / Myhill (1963), Garden of Eden theorem:** a CA over ℤⁿ is
  surjective ⟺ pre-injective. Extended to amenable groups
  (Ceccherini-Silberstein–Machì–Scarabotti 1999); *characterizes* amenability
  (Bartholdi). Canonical source: Ceccherini-Silberstein & Coornaert,
  *Cellular Automata and Groups*; see also their [GoE survey chapter](https://link.springer.com/chapter/10.1007/978-3-031-43328-3_5).
- **Gottschalk surjunctivity (1973); Gromov–Weiss:** injective CA over sofic
  groups are surjective. The local→global rigidity prototype.
- **Ax–Grothendieck:** injective polynomial self-maps of ℂⁿ are surjective;
  proved by transfer from finite fields — the same finite-approximation
  spirit as soficity. Note the asymmetry after July 2026: Ax–Grothendieck
  (assumes injectivity) stands; the Jacobian conjecture (tried to derive
  injectivity from local data) is false. Our Q1/Q2 ask the Jacobian-shaped
  question in the discrete setting; Q4 asks the Moore–Myhill-shaped one.
- **Recent boundary-probing:** GoE for [non-uniform CA](https://arxiv.org/abs/2507.06987)
  (2025 — different local rules per cell, still frozen grid); GoE for
  [Smale spaces](https://arxiv.org/pdf/2505.14409) (2025); linear-CA GoE
  failing over free groups. Direction of travel is "weaken uniformity, keep
  the geometry frozen." Nobody in this literature moves the geometry.

## 2. Causal graph dynamics (closest formal framework) ⚠

Arrighi, Martiel, Perdrix, Dowek school — CA generalized to bounded-degree
time-varying graphs, synchronous global dynamics with shift-invariance +
bounded information speed.

- [*Reversible Causal Graph Dynamics*](https://arxiv.org/abs/1502.04368) and
  the journal version [*invertibility, block representation,
  vertex-preservation*](https://link.springer.com/article/10.1007/s11047-019-09768-0)
  (Natural Computing 2020): if the **global** dynamics is invertible, then it
  is a CGD, admits finite-depth reversible block circuits, and is (in the
  relevant setting) vertex-preserving.
  **Direction: global → local structure.** Our Q1–Q3 are the converse
  (local conditions → global injectivity?); Q4 (GoE) is absent from this
  line entirely as far as the sweep shows.
- [*Space-time deterministic graph rewriting*](https://arxiv.org/abs/2404.05838)
  (2024): sufficient conditions for asynchronous rule applications to yield
  well-defined space-time events (determinism, not injectivity).
- ⚠ [*Space-time reversible graph rewriting*](https://arxiv.org/abs/2510.03296)
  (Arrighi–Costes–Maignan, late 2025): physics-inspired reversibility =
  "nearby space-like cuts mutually determine each other"; gives **sufficient
  local conditions** for this. Again the *engineering* direction (design
  rules guaranteed reversible), not the *rigidity* direction (when is
  reversibility forced / when does it fail globally despite holding
  locally), and no Moore–Myhill statement in the abstract. **Must read in
  full (esp. conclusions/open questions) before any write-up claims
  novelty.** If their "mutual determination" condition is close to our D1,
  our Q1 counterexample search doubles as a sharpness probe for their
  sufficient conditions — a publishable connection either way.

## 3. Reversible graph rewriting / DPO theory (the definitional substrate)

- DPO rules are always undoable *at their own match* (reverse span at the
  comatch) — standard since Ehrig et al. This is why D1 (application-level)
  must be distinguished from global-step injectivity; the gap between them
  IS the program.
- Reversible-DPO / reversible graph transformation literature exists
  (reversible computing community, Danos–Krivine-style ideas); relevant for
  D2's phrasing but does not touch GoE-type questions per the sweep.
- Gorard, [Wolfram-model DPO semantics over selective adhesive categories](https://arxiv.org/pdf/2010.02752) —
  the formalism our definitions should be phrased in for the Wolfram-facing
  write-up; [GReTA talk](https://www.irif.fr/~greta/event/apr9th2021-gorard/).

## 4. Structurally dynamic CA (the spiritual ancestor)

- [Ilachinski & Halpern 1987](https://content.wolfram.com/sites/13/2018/02/01-3-7.pdf),
  *Structurally Dynamic Cellular Automata*: states AND links evolve. Rich
  simulations, universality results; **no rigidity theory** (no GoE, no
  surjunctivity). Later "reversible SDCA" works (Alonso-Sanz et al.) obtain
  reversibility by *construction* (memory mechanisms) — again engineering,
  not rigidity.

## 5. Wolfram-model literature proper

- Multiway systems, branchial space, causal invariance (Gorard,
  wolframphysics.org working papers): confluence/critical-pair language for
  R2 merges exists, but merges are studied as a *feature* (quantum
  superposition analogies), never as a *pathology against local
  invertibility*. Two-way rules appear informally in ruliad discussions
  ([Wolfram, Metamathematics ch. 10](https://www.wolframscience.com/metamathematics/the-case-of-hypergraphs/)).
  No injectivity/GoE theory found.

## Gap statement (feeds VERDICT.md)

Both nearby literatures approach reversibility as a design goal:
CGD proves structure *given* global invertibility; space-time reversible
rewriting *engineers* reversibility from sufficient local conditions; SDCA
*constructs* reversible variants. **Nobody asks the rigidity questions:**
does local invertibility force global injectivity (Q1/Q2), and does
surjective ⟺ pre-injective survive dynamic topology (Q4)? The non-uniform-CA
GoE line (2023–25) shows the classical community actively generalizing GoE —
but always on frozen geometry. The intersection — GoE/surjunctivity for
dynamic topology — appears untouched.
