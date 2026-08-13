# ADVERSARIAL REVIEW — attacking our own definitions and claims
(pre-publication pass, 2026-07-27)

Six attacks a hostile referee would make, with our defenses and the honest
residue each leaves. The note must incorporate all six residues.

## A1. "The splice rule deletes an edge — this is deletion in disguise."

Defense: semantic D1 is about what (result + comatch) determines, not about
edge counts. The delete rule {(x,y)} → {} destroys the identities x, y; the
splice keeps every matched vertex present and identified (vars(L) = vars(R))
and its reverse at the comatch is unique. The distinction is principled:
delete fails syntactic D1, chain-step has bounded semantic-D1 failures, and
splice passes the declared finite semantic-D1 probe. Global semantic D1 for
splice has not been proved.
**Residue:** D1 is *our* definition. The note must present it as a
definition with motivation, not as the platonic notion of local
invertibility — and must state plainly that under Arrighi-style
context-preservation the splice is excluded. That exclusion is the point
(sharpness), but it must be stated, not hidden.

## A2. "On named graphs F is injective; iso-classes are the wrong object."

Defense: on named graphs the flagship's two applications give two *named*
successors (they differ in which concrete vertex ends up where), so named
evolution is not even single-valued; it is precisely at the isomorphism
level that the successor becomes unique — and there, injectivity fails.
Working modulo isomorphism is also the standard semantics (CGD: "pointed
graphs modulo"; Wolfram model states are abstract hypergraphs).
**Residue:** the note must state "unique successor *up to isomorphism*"
with the named-graph nuance spelled out, since it is exactly where a
careless reader would object.

## A3. "The min-successor policy is arbitrary."

Defense: the flagship needs no policy — all successors of each state lie in
one isomorphism class (Lean lemmas succ_S1_iso_P4 / succ_S2_iso_P4), so the
collision is a statement about the successor *relation*, robust under every
policy. Policy-relative certificates (e.g. cert_d3strict) are labeled as
such. **Residue:** keep the two classes rigorously separated in the note.

## A4. "Terminating dynamics collide cheaply; where is the surprise?"

The strongest attack. Defense, in three parts: (i) in partitioned/block CA,
locally-permutation structure DOES force global bijectivity — so there was
a real question of whether match-level invertibility forces state-level
injectivity; the answer (no, with 3-edge certificates) locates the failure
precisely at match-anonymity, which partitioned CA lack by construction;
(ii) census preservation (D3-strict examples) removes the "obviously lossy"
version of the objection; (iii) the value claim is calibrated: elementary
once seen — the contributions are the definitional mapping to the Jacobian
mechanism, machine-checked minimal certificates, the necessity-of-ambiguity
empirics, and the sharpness link to Arrighi's hypotheses. **Residue: the
note must not oversell.** Frame as "a precise elementary boundary,"
not "a deep theorem."

## A5. "Bounded sweeps prove nothing about rigidity."

Defense: empirical rigidity labels are always stated "in range"; the
general theorem is exact under its stated hypotheses but its current hand
proof remains pending external or generic Lean review. The converse's
evidence base is reported with exact tiers ((4,3), (5,3), (4,4), and the
(5,4) holdout check). The concrete collision is Lean-checked; unconditional
mutual unreachability is a hand terminality argument. **Residue:** every rigidity number in
the note carries its tier; no asymptotic language anywhere.

## A6. "Your two 'independent' implementations shared a bug once; why
trust the pipeline?"

Defense: the double-relabeling bug was IN the verifier, was caught precisely
because two implementations disagreed, and led to verifier self-tests. The
searcher's results were unaffected. All 13 certificates re-verified after
the fix. **Residue:** publish the full pipeline (searcher, verifier, logs,
certs) so third parties can re-run; disclose the bug in a methods footnote
— it is evidence the discipline works, and hiding it would be worse.

## Verdict

No attack overturns the results. Every residue is a framing obligation on
the note: define-don't-assume (A1), iso-nuance (A2), class separation (A3),
calibrated claims (A4), tier-stamped numbers (A5), full disclosure (A6).
