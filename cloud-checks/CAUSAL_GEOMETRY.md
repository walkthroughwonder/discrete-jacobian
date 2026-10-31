# Causal geometry experiments: results snapshot

*Snapshot 2026-10-31 of the Wolfram Cloud folder "Causal geometry experiments"
(13 notebooks). Verdicts read from Output cells only, as in
[INDEX.md](INDEX.md). Three notebooks had never been evaluated; they were run
on 2026-10-31 in a separate Wolfram kernel (results below, not yet saved back
into the cloud notebooks). AI assistance (Claude, Anthropic).*

The verdict field in this folder is `"held"`; every notebook also carries the
usual `"claim_3" -> False` and `"hold" -> "HOLD"` guards.

## Results

| Notebook | Cloud id | Status | Verdict | Key numbers |
|---|---|---|---|---|
| Causal Firing Lag | 90a5634f | never run; rerun 2026-10-31 with the fix below | **held True** | firing lag dim27 vs chain27: 44 vs 46 at event 50, 142 vs 143 at event 149 (stored local reference: 44/45 and 141/142) |
| Causal Shell Ratio | 8a9f569f | never run; rerun 2026-10-31 with the fix below | **held False** | R(t) = E(depth t) / E(depth t-2): tie at mid t = 3 (4.0 vs 4.0); at t = 6 dim27 3.13 vs chain27 0.75. Local reference claimed 4.0 vs 3.0 at t = 3 and held True, so it does not reproduce |
| hard39 Cube Rewiring Spectral Dimension (Slim) | 907e3f4a | never run; rerun 2026-10-31 as written | **held True** | mean spectral dimension at rewiring p = 0, 0.01, 0.03, 0.1, 0.3: 2.56, 2.64, 2.77, 3.41, 4.36 (non-decreasing; leaves the 2.5 to 3.5 band at p = 0.3) |
| Cloud Experiments: Rewiring Causal Metrics and Betti Tests (2026-08-21) | 529d8e7b | run | **held True**, gate HOLD | preregistered cube-rewire hard39: 2.56, 2.61, 2.81, 3.36, 4.31 (agrees with the slim rerun within seed noise) |
| hard94 to hard98 Annulus Flux and Wavefront Variance | f696ae87 | run, 5 outputs, no messages | **held True** (3 of 3) | flux ratios F5/F4 0.79, 0.98, 1.20 and F4/F3 0.68, 0.95, 1.24; wavefront test `cube_lt_square` True (mean L1 3.87 vs 4.69) |
| hard142 huygens_wave_shell_ratio_t8_pent | ecedd1b6 | run | **held True** | outer/inner shell ratio 1.41, 1.67, 0.74, 0.39 as support grows 145 to 13073 |
| hard141 huygens_wave_second_shell_ratio_t9 | 9a6f93f8 | run | **held False** | shell ratio 1.32, 1.46, 0.72; second shell ratio 3.56, 2.05, 1.94 |
| hard145 huygens_wave_radial_tv_t8 | 806efc25 | run, 13 sub-tests | **4 held, 9 not** | radial total variation, angular entropy, cone IPR and outer-fraction meters; most fail |
| Causal Graph Metrics, Homology and Wave H Tests | 16e5b1fb | run, 1 message (Set::setraw) | **held False** (2 of 2) | discrete Huygens meter H grows with size (0.06, 0.11, 0.17, 0.23) instead of staying small |
| Increment Mismatch TV | ad8c0753 | aborted | none | stopped by the cloud plan's time limit, output `$Aborted` |
| Wolfram Model Geometry, Dimension and Injectivity Experiments | 57a3ac7a | run, 42.7 MB, 38 message cells | no verdict field | growth and dimension tables only; messages are Part::partw, Part::partd, LinearModelFit::desmat, Eigenvalues::arh, General::stop |
| Same, code only (no outputs) | 03e12762 | code copy | none | input-only copy of the notebook above |
| hard39 to hard51 Spectral Dimension and Tesseract Horizon Tests | 822fbbbc | run, 130 message cells | no readable verdict | error-heavy: Power::infy, Part::partw, Do::iterb, General::stop. Needs a cleanup before any result can be trusted |

**Tally.** Five notebooks hold (Causal Firing Lag, both hard39 cube-rewire
runs, hard94 to hard98, hard142). Four fail or mostly fail (Causal Shell
Ratio, hard141, hard145, the Huygens H test). Four give no verdict (one
aborted, one code-only copy, two error-heavy notebooks).

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

## Next steps

* Patch the third argument in the two notebooks (or save fixed copies beside
  them) so the cloud versions match these reruns.
* Rerun Increment Mismatch TV with a smaller size or locally, since the cloud
  plan's per-evaluation limit stops it.
* Clean up the two error-heavy notebooks before citing anything from them.
