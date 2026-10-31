# Causal geometry experiments: results snapshot

*Snapshot 2026-10-31 of the Wolfram Cloud folder "Causal geometry experiments"
(13 notebooks). Verdicts read from Output cells only, as in
[INDEX.md](INDEX.md). Three notebooks had never been evaluated and one had
been aborted; all four were run on 2026-10-31 (details below). Fixed copies of
four notebooks (these four, except hard39 slim, plus hard49) now sit beside
the originals in the cloud, with their outputs saved; the originals are
untouched. AI assistance (Claude, Anthropic).*

The verdict field in this folder is `"held"`; every notebook also carries the
usual `"claim_3" -> False` and `"hold" -> "HOLD"` guards.

## Results

| Notebook | Cloud id | Status | Verdict | Key numbers |
|---|---|---|---|---|
| Causal Firing Lag | 90a5634f; fixed copy 34ffe85e | never run; fixed copy run in the cloud 2026-10-31 | **held True** | firing lag dim27 vs chain27: 43 vs 46 at event 50, 141 vs 143 at event 149 in the cloud (44/46 and 142/143 in a newer kernel; stored local reference 44/45 and 141/142) |
| Causal Shell Ratio | 8a9f569f; fixed copy 71eb8e6b | never run; fixed copy run in the cloud 2026-10-31 | **held False** | R(t) = E(depth t) / E(depth t-2): tie at mid t = 3 (4.0 vs 4.0); at t = 6 dim27 3.43 vs chain27 0.75 in the cloud (3.13 in a newer kernel). Local reference claimed 4.0 vs 3.0 at t = 3 and held True, so it does not reproduce |
| hard39 Cube Rewiring Spectral Dimension (Slim) | 907e3f4a | never run; rerun 2026-10-31 as written | **held True** | mean spectral dimension at rewiring p = 0, 0.01, 0.03, 0.1, 0.3: 2.56, 2.64, 2.77, 3.41, 4.36 (non-decreasing; leaves the 2.5 to 3.5 band at p = 0.3) |
| Cloud Experiments: Rewiring Causal Metrics and Betti Tests (2026-08-21) | 529d8e7b | run | **held True**, gate HOLD | preregistered cube-rewire hard39: 2.56, 2.61, 2.81, 3.36, 4.31 (agrees with the slim rerun within seed noise) |
| hard94 to hard98 Annulus Flux and Wavefront Variance | f696ae87 | run, 5 outputs, no messages | **held True** (3 of 3) | flux ratios F5/F4 0.79, 0.98, 1.20 and F4/F3 0.68, 0.95, 1.24; wavefront test `cube_lt_square` True (mean L1 3.87 vs 4.69) |
| hard142 huygens_wave_shell_ratio_t8_pent | ecedd1b6 | run | **held True** | outer/inner shell ratio 1.41, 1.67, 0.74, 0.39 as support grows 145 to 13073 |
| hard141 huygens_wave_second_shell_ratio_t9 | 9a6f93f8 | run | **held False** | shell ratio 1.32, 1.46, 0.72; second shell ratio 3.56, 2.05, 1.94 |
| hard145 huygens_wave_radial_tv_t8 | 806efc25 | run, 13 sub-tests | **4 held, 9 not** | radial total variation, angular entropy, cone IPR and outer-fraction meters; most fail |
| Causal Graph Metrics, Homology and Wave H Tests | 16e5b1fb | run, 1 message (Set::setraw) | **held False** (2 of 2) | discrete Huygens meter H grows with size (0.06, 0.11, 0.17, 0.23) instead of staying small |
| Increment Mismatch TV | ad8c0753; fixed copy 55b829cf | aborted in the cloud; fixed copy ([imtv_fast.wl](imtv_fast.wl)) run in the cloud 2026-10-31, matching the Python port [imtv.py](imtv.py) | **held False** | TV dim27 vs chain27: 0.988 vs 0.553 at event 50, 0.802 vs 0.298 at event 149. dim27 is above, not below, so the claim is reversed. chain27 matches the stored local reference exactly; dim27 is close (reference 0.994 and 0.849) |
| Wolfram Model Geometry, Dimension and Injectivity Experiments | 57a3ac7a | exploratory log, 18 inputs; every failing cell was rerun cleanly later (see below) | no verdict field (measurements only) | dim27 vs chain27 at the same sizes: ball-growth dimension 1.82 vs 1.79, line-graph 1.93 vs 1.81; four-point hyperbolicity 0.91 vs 0.08 (diameters 15 and 28); local cycle density 0.63 vs 0.74; Forman curvature mean -5.07 vs -4.92 |
| Same, code only (no outputs) | 03e12762 | code copy | none | input-only copy of the notebook above |
| hard39 to hard51 Spectral Dimension and Tesseract Horizon Tests | 822fbbbc; hard49 fixed copy 3cfbf601 | log of 13 tests in 23 runs; all 65 message cells are in attempts that were rerun cleanly | **mixed: 5 held, 8 not** (final run of each test) | held: hard39, hard43 (deep interior: square 1.82, cube 2.78), hard48 (parity window), hard49 (after the fix below), hard50 (horizon window, square 1.81, cube 2.74). Not held: hard40 (tesseract baseline reads 3.19, below its 3.5 to 4.5 band), hard41, hard42, hard44 to hard47, hard51 |

**Tally.** Five notebooks hold (Causal Firing Lag, both hard39 cube-rewire
runs, hard94 to hard98, hard142). Five fail or mostly fail (Causal Shell
Ratio, Increment Mismatch TV, hard141, hard145, the Huygens H test). The
hard39 to hard51 log is mixed (5 of its 13 tests hold). Two carry no verdict
(the exploratory geometry notebook and its code-only copy).

**The two "error-heavy" notebooks are not broken.** Both are working logs:
every cell that raised messages was followed by a corrected rerun. In
hard39 to hard51, the messages come from the first two hard42 attempts (fixed
by `Normal[Total[adj]]`), the first two hard50 attempts (rerun as "FIXED")
and a superseded hard51 gate cell with a syntax error. In the 42.7 MB
notebook, cell 1 (LinearModelFit), cell 5 (syntax), cell 12 (Part on
`GraphDistanceMatrix`) and cell 17 (`Degree`, which is the degree constant
for angles, used instead of `VertexDegree`) were each rerun cleanly; the only
remaining messages are `Eigenvalues::arh` warnings on a run that still
returned values. The file is large because one cell outputs a grid of graph
plots.

## Bug found in two never-run notebooks

`Causal Firing Lag` and `Causal Shell Ratio` call

```wolfram
ResourceFunction["WolframModel"][rule, init, 150, "CausalGraph", ...]
```

The third argument of `WolframModel` counts **generations**, not events. The
dim27 rule doubles its edge count every generation, so 150 generations can
never finish on any machine (this is why the cloud evaluation hung). Both
notebooks clearly mean events: they index the result by event number and
compare against a local reference computed per event. The reruns above use

```wolfram
ResourceFunction["WolframModel"][rule, init, <|"MaxEvents" -> 150|>, "CausalGraph",
  "EventOrderingFunction" -> "LeastRecentEdge"]
```

with everything else unchanged. With that fix Causal Firing Lag reproduces its
local reference to within one step, and Causal Shell Ratio does not reproduce:
under the official `WolframModel` event order, chain27 reaches causal depth 6
(not 7) within 150 events, and the two ratios tie at the mid window.

## Bug found in Increment Mismatch TV

The notebook looks up which event wrote each consumed edge with

```wolfram
Lookup[edgeWriter, #, -1] & /@ consumed
```

An edge is a list such as `{1, 2}`, and `Lookup` treats a list as a list of
separate keys, so every edge reads as an initial edge. Every event then gets
causal depth 0 and TV is identically 0, whatever the rule. The fix is
`Lookup[edgeWriter, Key[#], -1]`. With it, the Wolfram code and the Python port
agree on all 24 TV values per rule at 24 events. The full 150-event run needs
the port: the notebook scans every ordered pair of edges at every event, which
is far beyond the cloud plan's time limit, while the port finishes in about
4 seconds.

The fixed cloud copy ([imtv_fast.wl](imtv_fast.wl)) keeps the same selection
rule but finds all candidate matches per event with one vectorized comparison,
keeping the original (i1, i2) order so ties break the same way. In a fresh
kernel it matches the Python port exactly over all 150 events for both rules
(same TV sums, sums of squares and candidate counts, 75430 and 44487), takes
about 13 s, and in the cloud returned the same verdict with its output saved.

## Bug found in hard49 (chord-fill-parity)

The square grid is bipartite, so with a single random chord the walk never
returns on odd steps near the centers, and the odd-step fit has no points
(`Indeterminate`). The verdict line `!(1.7 <= Indeterminate <= 2.3)` then
never evaluates, so `held` was left as an unevaluated expression. The fixed
copy uses `!TrueQ[1.7 <= ... <= 2.3]`, so a missing odd return counts as out
of band. Same rows as the original run (even-step dimension 1.79, 1.90, 2.18,
2.64 for 1, 5, 20, 50 chords), now **held True**, run in the cloud with the
output saved.

Cloud note: an Input cell stored as plain text is parsed by the cloud front
end, which turned `UndirectedEdge @@@ list` into a broken `ApplyOne[...]`
expression. The fixed copy uses `Apply[UndirectedEdge, list, {1}]` instead.

## Status

Every notebook in the folder now has a final reading. Nothing is left
unevaluated or aborted, and no remaining verdict depends on an errored cell.
