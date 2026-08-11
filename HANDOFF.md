# HANDOFF — Discrete Jacobian Program

*Written 2026-07-28 by the remote (Claude Code on the web) session, for the
local agent picking the program up. Read this first; it supersedes the
"Next steps" scatter across the other files.*

## State in one paragraph

The program answered its founding question: **yes, locally invertible
hypergraph rewriting can fail global injectivity** — flagship = the splice
rule, Lean-verified with zero sorries. The sweep, certificates, adversarial
review, Zenodo archive (DOI 10.5281/zenodo.21630926), and a Wolfram
Community post draft are all done. The final act of the last session
(2026-07-27) upgraded the weak-form rigidity conjecture to a **theorem**
with a short elementary proof (`PROOF_rigidity.md`). Everything is
committed and pushed; the working tree is clean; `main` and
`claude/session-context-6gp9t9` both point at `37302ea`.

## What is proven / verified (trust levels)

| Claim | Trust level |
|---|---|
| Splice collision (non-iso states, unique successor up to iso, terminality) | **Lean 4, zero sorries** (`lean/SpliceCollision.lean`, compiles against Mathlib) |
| 14 certificates (13 R1 + 1 deep two-step R2 — regenerated 2026-08-11 after the original "unsplice" cert was refuted as reducible to one step) | Independently-implemented verifier, CONFIRMED |
| Sweep statistics (489 → 238 semantic-D1; 52 colliders at ≤4v/≤3e; 182 at (4,4)) | Machine-swept, tier-stamped, "in range" claims only |
| Ambiguity necessary for collision (52/52; all 56 unambiguous rules rigid) | Empirical at swept tiers — now *explained* by the theorem |
| **Rigidity Theorem** (semantic D1 + history-unambiguous ⟹ one-step evolution injective up to iso, policy-free) | Hand proof, `PROOF_rigidity.md` — **pending scrutiny**: no second reader yet, no Lean. Say "theorem with proof, pending scrutiny" externally. |

## Known inconsistency — RESOLVED 2026-07-28

`WOLFRAM_POST.md` was drafted before the rigidity proof and still called
rigidity a conjecture. Fixed 2026-07-28 (remote session): the post now
states the theorem (with the pending-scrutiny qualifier) and reframes the
help-ask toward the open converse. It is ready for Edwin's final read.

## Work queue (priority order)

1. ~~Revise `WOLFRAM_POST.md`~~ DONE 2026-07-28. Next step is Edwin's
   final read. Posting happens **only under Edwin's account, only after
   his sign-off** — the agent never posts it.
2. **Residual reading obligation** (from VERDICT.md N3 residue in
   RESULTS.md): skim the Natural Computing 2020 CGD paper's exact
   definitions before any submission, so the frozen-topology citations are
   drawn where their theorems actually stop. (The other obligation —
   arXiv:2510.03296 — is discharged: see POSITIONING.md; our certificates
   are sharpness witnesses for their context-preservation hypotheses.)
3. **The live research front — the converse / dichotomy question.** Does
   *genuine* history ambiguity force eventual collision? Naive converse is
   dead: 130 ambiguous-but-rigid rules in range at (≤4v,≤3e), and the 55
   ambiguous-rigid holdouts at (4,4) all survive tier (5,4)
   (`phase1/holdouts_5_4.jsonl`, produced by `holdouts_5_4.py`; the splice
   positive-control shows 23 collision images there, so the tier has
   power). Refined target: define **independent ambiguity** (ambiguity not
   explained by a benign automorphism, e.g. doubled-edge multiset
   symmetry — the one rule still unambiguous at (4,4),
   `{(a,a),(b,b)} → {(a,b),(b,a)}`, is rigid because its RHS symmetry acts
   trivially on histories) and re-run the necessity/sufficiency analysis
   against the holdouts. Either outcome is a result.
4. **Lean formalization of the general Rigidity Theorem.** Needs generic
   matching/application infrastructure — a much bigger lift than the
   concrete splice proof, but the proof is two case-splits, so it's
   well-defined. Doubles as the "second reader" for item 5.
5. **Second reader for `PROOF_rigidity.md`.** Until a human or Lean
   confirms it, every external artifact keeps the "pending scrutiny"
   qualifier.
6. Unstarted Phase 4 items: arXiv-shaped version of the note; the
   interactive visualizer companion (explorer preset showing the branchial
   merge; the Sym³(ℙ¹) branched-cover picture).

## Standing protocols (do not relax)

- **Nothing leaves the repo without Edwin's explicit sign-off.** Drafts
  only. Wolfram post under Edwin's account.
- **Verifier independence:** every new claim gets checked by
  `verify_independent.py` (shares no code with the search stack). History
  lesson twice over: the v3 retraction, and the verifier's own
  double-relabeling bug (first run rejected all 12 certs; verifier now has
  self-tests). A passing round-trip can pass by coincidence.
- **Tier-stamped claims only.** Never state a sweep result without its
  (vertices, edges) bounds. The splice and cert_0 lift their bounds by
  hand (terminal successors); other certificates are bounds-relative.
- **AI assistance disclosed** in every public artifact.
- **712/zarankiewicz hold is absolute** until Edwin lifts it. Kourovka PRs
  #4638/#4639: feedback, when it arrives, takes priority over this
  program.

## Addendum 2026-08-03 — dichotomy campaign complete; Arrighi call pending

- **The converse is resolved at the relation level and open exactly at
  the policy level.** See WITNESS_ANALYSIS.md (Props A/B, the phantom
  witness obstruction, D-IA), DEFINITIONS.md addendum (Q5), RESULTS.md
  dated section. Machine-check: 182/182 colliders have D-IA; the 55
  holdouts partition 25 orbit / 18 phantom / 12 policy-shielded D-IA.
  **Q5** (does policy shielding persist for the 12 frontier rules?) is
  the program's new central question.
- **PROOF_rigidity remark 6**: the syntactic-D1 hypothesis is now
  explicit. Nothing retracts; state it proactively on the call.
- **Arrighi/Costes/Maignan Zoom, this week** (reply of 08-02). Prep:
  (1) remark 6 up front; (2) phantom-witness result; (3) the 12-rule Q5
  frontier as new content; (4) cite cert_deep_r2.json if R2 end-to-end
  certification is questioned; (5) DO the Natural Computing 2020 CGD
  definitions skim (VERDICT.md obligation, still outstanding, now
  time-critical); (6) consider merging this branch to main pre-call.
- **Fleet coordination**: FLEET_ANSWER_M9.md here + ANSWER C1 in
  zarankiewicz fleet/inbox_mac.txt (pushed to their main, 2cffda0)
  answer the Mac's REQ M9/X2. Follow-ups arrive in either channel.

## Addendum 2026-07-28 — adjacent-project status (public facts only)

- **Kourovka PRs #4638 (1.74) / #4639 (1.40) on formal-conjectures:** the
  July 26 CI failures were addressed by the July 27 rebase onto
  post-#4645 upstream main (`FormalConjecturesUtil` import). Verified
  2026-07-28 in a clean environment: both files elaborate on Lean
  v4.27.0 + Mathlib cache and pass the repo's style linters
  (`autoImplicit=false`, ams/category/moduleDocstring/latex_docstring,
  copyright, namespace) with only the intentional `sorry`s. Both proposal
  issues (#1915, #1931) have maintainer go-aheads; #1931 is assigned.
  Nothing left to push — just watch CI/review.
- **Erdős #872:** PR #4226 (872.lean) merged upstream 2026-07-02.
  Buddhdev's 2026-07-12 comment on erdosproblems.com/872 credits Edwin's
  K₅ computation and claims an **unconditional**
  L(n) ≥ c_δ·n(log log n)²/log n bound (revised manuscript public in
  xa8zz/erdos-harness), with two selector arguments not yet in Lean.
  Per Edwin's own 2026-07-08 forum comment, the promised **second
  formal-conjectures PR** stating the improved bound is now unblocked —
  a concrete next work item.

## Orientation map

| File | What it is |
|---|---|
| `ULTRAPLAN.md` | The original program plan (phases, risk register) |
| `VERDICT.md` | Phase 0 go/no-go (GO + the two reading obligations) |
| `DEFINITIONS.md` | D1/D2/D3, R1/R2, collision classes, history ambiguity |
| `RESULTS.md` | Full findings; its "Next steps" section is the detailed log |
| `PROOF_flagship.md` / `lean/SpliceCollision.lean` | Splice collision, hand + Lean |
| `PROOF_rigidity.md` | The Rigidity Theorem and proof |
| `ADVERSARIAL_REVIEW.md` | Six self-attacks and what survived |
| `POSITIONING.md` | Novelty gate vs. Arrighi et al. — passed |
| `NOTE_DRAFT.md` | The public working-draft write-up |
| `WOLFRAM_POST.md` | Community post draft — theorem-consistent as of 2026-07-28, awaiting Edwin's read |
| `phase1/` | Searcher (`search.py`, `maxsweep.py`), engine (`core.py`), independent verifier, 14 certs, sweep/stress logs |

## Reproduce

```
cd phase1
python test_sanity.py                          # engine sanity + planted round trip
python verify_independent.py cert_flagship.json
python maxsweep.py                             # full sweep, ~5 min on 14 cores
```

Lean: `lake env lean lean/SpliceCollision.lean` with any
Mathlib-provisioned toolchain.
