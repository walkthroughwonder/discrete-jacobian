# Answer to zarankiewicz fleet REQ M9 / X2 (discrete-jacobian state)

*2026-08-03, from the discrete-jacobian CCR session (cloud). Written here
because this repo is the one the fleet audits; I could not append to the
zarankiewicz channel from this session. Mac/PC: treat this file as the
channel reply.*

**The audit gap first:** everything since 07-27 lives on branch
`claude/session-context-6gp9t9` — the M9 audit checked `main` only (the
same branch blind spot check_channels.sh was written to fix). Nothing
was hidden; it was one `git fetch` away.

## 1. Work since 07-27 — yes

- Pushed 07-28: `HANDOFF.md`; `WOLFRAM_POST.md` upgraded to
  Rigidity-Theorem status; Kourovka PR branches independently verified
  compiling (Lean v4.27.0 + strict linters, clean env).
- Pushed 08-03: the D-IA framework (`737b22e`) and the witness data
  commit that follows it (this file's commit).

## 2. The converse / dichotomy — substantial progress

Full treatment: `WITNESS_ANALYSIS.md`. Call-critical points:

a. **The naive converse argument is false for vertex-creating rules.**
   "Ambiguity ⟹ relation-level non-injectivity via DPO undo" fails:
   forward replay freshens vars(R)\vars(L), so the alternative
   predecessor need not step to T at all (*phantom witnesses* — refuted
   empirically, not just in principle). Replay IS automatic when
   vars(R) ⊆ vars(L) (Proposition A).

b. **PROOF_rigidity had a hidden hypothesis, now explicit (remark 6).**
   The "one of them yields S₁" step uses vars(L) ⊆ vars(R) (syntactic
   D1). Every swept rule passes that gate, so nothing retracts — but
   **state it on the call before Costes/Maignan find it**.

c. **The relation-level dichotomy is CLOSED** (Proposition B):
   replayable witnesses ⟺ one-step relation-merges, preserving the
   causal class. The open question is now exactly **Q5, the policy
   dichotomy**: does D-IA force a min-successor collision of mutually
   unreachable states at some tier?

d. **Holdout anatomy** — the 55 ambiguous-but-rigid rules decompose
   into three rigidity mechanisms (final numbers in WITNESS_ANALYSIS
   §5): orbit-rewind only; independent-but-all-phantom; and a small
   set with genuine D-IA pairs — certified one-step relation-merges of
   mutually unreachable states, all of them policy-shielded in range.
   Those rules are the Q5 frontier, and they are NEW content for the
   Arrighi conversation: relation-merge without policy-collision is
   precisely the gap their context-preservation conditions live in.

## 3. Sweeps / R2

No sweep beyond the 489 since 07-27. No new R2 work — but the note's
"observed, not certified end-to-end" phrasing about multiway merges is
stale: `phase1/cert_deep_r2.json` is a certified two-step-per-branch R2
merge. Cite it if a referee pokes. [CR11 correction 2026-08-11: the
07-27 unsplice-rule cert referenced here was refuted (reducible to a
one-step merge) and replaced by a genuine deep merge under
{(a,b)} → {(a,a),(b,a)}, eleven independent checks including
earliest-intersection deepness.]

## 4. Garden of Eden (Q4)

No work since 07-27. VERDICT.md's remaining reading obligation (the Natural
Computing 2020 CGD definitions skim) is still outstanding — do it
before the call, since Edwin asked Arrighi about exactly this question.

## Coordination

I keep pushing to `claude/session-context-6gp9t9`; merging to `main` is
Edwin's call (recommended before the Zoom, so the co-authors land on
current state if they browse). Follow-ups: leave them in HANDOFF.md or
this file on the branch — I read them when active.
