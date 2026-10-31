# Wolfram Cloud verification runs: index

*Snapshot of Edwin Rosero's Wolfram Cloud account, first taken 2026-10-30 and corrected 2026-10-31 (read-only scans). The notebooks themselves live in the cloud; this file records what each one checked and how its verdicts came out. Verdicts are counted in Output cells only.*

Each check emits an association with `"pass" -> True|False` and a `"gate"` field. Every verdict in every notebook carries `"gate" -> "HOLD"` and `"claim_3" -> False`, so none of these runs promoted a claim on its own.

## Summary

| Series | Notebooks | Dates | With verdicts | Pass | Fail |
|---|---|---|---|---|---|
| WC, named notebooks (WC checks folder) | 74 | 2026-09-19 to 2026-10-06 | 34 | 46 | 2 |
| Lite Seals (batched seals) | 149 | 2026-10-09 to 2026-10-29 | 149 | 3108 | 0 |
| WC106 to WC2580, five unnamed working notebooks | 5 | 2026-09-20 to 2026-10-09 | 420 of 432 checks | 442 | 0 |

### What the failures are

- **Correction (2026-10-31): there were no timeouts.** An earlier version of this index reported 88 Lite Seals failures, all `"status" -> "TIMEOUT"`. Those were not results. Each confluence check is wrapped in `TimeConstrained[..., 60, <|"status" -> "TIMEOUT", "pass" -> False, ...|>]`, and that scan counted the fallback written in the input code. Counting verdicts in Output cells only, every Lite Seals check passed (3108 of 3108), and the same holds for 14 apparent failures in the working notebooks. Earlier pass counts were also slightly inflated by the success-branch literal `"pass" -> True` in the code; every table below now counts outputs only. The only genuine false verdicts anywhere are WC73 and WC76, explained next.
- **WC73 and WC76 (resolved 2026-10-30).** Both compute the singular series S for the pattern {0, 2, 4}. The exact value is S = 0, because {0, 2, 4} covers every residue mod 3, so the local factor at p = 3 vanishes. WC73 tested the claim "S is nonzero"; its failure is the mathematically correct outcome. WC76 reported S = 1 only because its notebook is corrupted: the full text of WC77 was pasted inside its product loop's iterator, so the loop never ran and the product kept its initial value 1 (reproduced exactly). Rerun cleanly in Wolfram Language, WC76 passes with S = 0. No genuine contradiction remains.
- **Cleanup note (2026-10-30).** Five empty or superseded items were moved to the cloud Trash (two blank notebooks, a scratchpad link, WC103 "old" and WC37 "Error"); they are no longer listed below. A corrected copy of WC76, "WC76 S Zero Two Four Seal (fixed).nb", sits beside the original in the WC checks folder.
- **40 named WC notebooks have no pass/fail field** (mostly WC1 to WC31, the earliest runs, which print raw values instead).
- **WC5 and WC19 outputs are unreliable** (neither has a pass/fail field, so the totals above are unaffected): WC5 raised `StringLength::string` errors, and WC19 hit the cloud time limit and then `Partition::npart`.

## WC series

| # | Check | Date | KB | Pass | Fail | Outputs |
|---|---|---|---|---|---|---|
| WC1 | Edge Count Stamp | 2026-09-19 | 5 | 0 | 0 | 1 |
| WC2 | Match Trio Bits | 2026-09-19 | 82 | 0 | 0 | 1 |
| WC3 | H4 Lockstep Zero | 2026-09-19 | 4 | 0 | 0 | 1 |
| WC4 | Toggle Cycle Length | 2026-09-19 | 4 | 0 | 0 | 1 |
| WC5 | Fibonacci Length Ladder | 2026-09-19 | 6 | 0 | 0 | 2 |
| WC6 | One-Way Event Asymmetry | 2026-09-19 | 81 | 0 | 0 | 1 |
| WC7 | FS Distance Symmetry | 2026-09-19 | 8 | 0 | 0 | 1 |
| WC8 | Split Length Formula | 2026-09-19 | 8 | 0 | 0 | 1 |
| WC9 | Double Finals FS Triangle | 2026-09-19 | 41 | 0 | 0 | 1 |
| WC10 | Flat2d Edge Monotone | 2026-09-19 | 3 | 0 | 0 | 1 |
| WC11 | One-Way Zero Divergent | 2026-09-19 | 8 | 0 | 0 | 1 |
| WC13 | Hand Conf Not CI | 2026-09-19 | 12 | 0 | 0 | 1 |
| WC14 | Twin Singular Series | 2026-09-19 | 3 | 1 | 0 | 1 |
| WC15 | Sort Annihilate Path Death | 2026-09-19 | 5 | 0 | 0 | 1 |
| WC16 | Pair Singular Series | 2026-09-19 | 4 | 1 | 0 | 1 |
| WC17 | Wolfram1 Divergent Noninc | 2026-09-19 | 8 | 0 | 0 | 1 |
| WC18 | Gorard Fib Cap Flip | 2026-09-19 | 9 | 0 | 0 | 1 |
| WC19 | Chain27 Hatd Flip Count | 2026-09-19 | 11 | 0 | 0 | 4 |
| WC20 | Dim27 Hatd Miss Band | 2026-09-19 | 18 | 0 | 0 | 1 |
| WC21 | Match Bit Flat2d | 2026-09-19 | 6 | 0 | 0 | 1 |
| WC22 | Match Bit Dim27 | 2026-09-19 | 6 | 0 | 0 | 1 |
| WC23 | Match Bit Chain27 | 2026-09-19 | 6 | 0 | 0 | 1 |
| WC24 | Toggle Return Stable | 2026-09-19 | 37 | 0 | 0 | 1 |
| WC25 | Fib Ladder Regression | 2026-09-19 | 3 | 0 | 0 | 1 |
| WC26 | Split Length Regression | 2026-09-19 | 9 | 0 | 0 | 1 |
| WC27 | Oneway Asymmetry Regression | 2026-09-19 | 65 | 0 | 0 | 1 |
| WC28 | H4 Lockstep Spot | 2026-09-19 | 4 | 0 | 0 | 1 |
| WC29 | FS Symmetry Regression | 2026-09-19 | 8 | 0 | 0 | 1 |
| WC30 | FS Triangle Regression | 2026-09-19 | 44 | 0 | 0 | 1 |
| WC31 | Flat2d Monotone Regression | 2026-09-19 | 3 | 0 | 0 | 1 |
| WC32 | S0612 Not Zero | 2026-09-19 | 3 | 1 | 0 | 1 |
| WC33 | H4 G4 Term Zero | 2026-09-19 | 2 | 1 | 0 | 1 |
| WC34 | S01224 Not Zero | 2026-09-19 | 3 | 1 | 0 | 1 |
| WC35 | Twin Series Regression | 2026-09-19 | 3 | 1 | 0 | 1 |
| WC36 | Coarse Grain Regression | 2026-09-19 | 6 | 0 | 0 | 1 |
| WC37 | Sort Annihilate Regression | 2026-09-19 | 5 | 0 | 0 | 1 |
| WC38 | Pair Series Regression | 2026-09-19 | 5 | 1 | 0 | 1 |
| WC39 | H6 Existence Spot | 2026-09-19 | 2 | 0 | 0 | 1 |
| WC40 | Dim27 Miss Band Regression | 2026-09-19 | 22 | 0 | 0 | 1 |
| WC41 | Match Trio Regression | 2026-09-19 | 92 | 0 | 0 | 1 |
| WC43 | Hand CI Not Conf | 2026-09-19 | 62 | 1 | 0 | 2 |
| WC44 | G Le H Spot | 2026-09-19 | 3 | 1 | 0 | 1 |
| WC49 | Pair Series Spot | 2026-09-19 | 58 | 4 | 0 | 5 |
| WC50 | Toggle Return Spot | 2026-09-20 | 35 | 0 | 0 | 1 |
| WC52 | Match Flat2d Spot | 2026-09-20 | 12 | 0 | 0 | 1 |
| WC52 | Match Flat2d Spot | 2026-09-20 | 29 | 0 | 0 | 2 |
| WC53 | Match Dim27 Spot | 2026-09-20 | 6 | 0 | 0 | 1 |
| WC54 | H4 Count Spot | 2026-09-20 | 4 | 1 | 0 | 1 |
| WC57 | Try3d Match Spot | 2026-09-20 | 20 | 0 | 0 | 2 |
| WC59 | Singleslit Match Spot | 2026-09-20 | 8 | 0 | 0 | 1 |
| WC62 | FS Triangle Spot | 2026-09-20 | 46 | 2 | 0 | 3 |
| WC63 | Sort Annihilate Spot | 2026-09-20 | 5 | 1 | 0 | 1 |
| WC64 | Coarse Grain Spot | 2026-09-20 | 20 | 1 | 0 | 1 |
| WC65 | Twin Product Spot | 2026-09-20 | 3 | 1 | 0 | 1 |
| WC67 | One Way Divergent Spot | 2026-09-20 | 20 | 2 | 0 | 2 |
| WC69 | Split K Five Spot | 2026-09-20 | 9 | 1 | 0 | 1 |
| WC71 | H2 Existence Spot | 2026-09-20 | 4 | 1 | 0 | 1 |
| WC72 | H3 Existence Spot | 2026-09-20 | 5 | 1 | 0 | 1 |
| WC73 | S Zero Two Four **(fail; correct, see above)** | 2026-09-20 | 4 | 0 | 1 | 1 |
| WC75 | Twin Bound Spot | 2026-09-20 | 4 | 1 | 0 | 1 |
| WC76 | S Zero Two Four Seal **(fail; corrupted notebook, passes on clean rerun)** | 2026-09-20 | 9 | 0 | 1 | 1 |
| WC77 | Odd H Absent Spot | 2026-09-20 | 3 | 1 | 0 | 1 |
| WC78 | Even H Four Spot | 2026-09-20 | 3 | 1 | 0 | 1 |
| WC81 | Pair H Ten Spot | 2026-09-20 | 10 | 3 | 0 | 3 |
| WC82 | S Zero Four Six | 2026-09-20 | 3 | 1 | 0 | 1 |
| WC87 | Odd H Seven Spot | 2026-09-20 | 31 | 3 | 0 | 4 |
| WC92 | S Zero Six Twelve | 2026-09-20 | 20 | 4 | 0 | 4 |
| WC93 | Toggle Step Eight Spot | 2026-09-20 | 4 | 1 | 0 | 1 |
| WC94 | Match Dim27 Again | 2026-09-20 | 6 | 0 | 0 | 1 |
| WC98 | H6 First Five | 2026-09-20 | 8 | 2 | 0 | 2 |
| WC99 | Fib Step Nine Spot | 2026-09-20 | 3 | 1 | 0 | 1 |
| WC101 | Pair H Fourteen Spot | 2026-09-20 | 12 | 2 | 0 | 2 |
| WC103 | Toggle Step Ten Spot | 2026-09-20 | 3 | 1 | 0 | 1 |
| WC105 | Twin Bound Recheck | 2026-09-20 | 21 | 1 | 0 | 2 |

## Lite Seals series

Numbered by spelled-out name ("Lite Seals Four" = 4). Every check passed. #153 was created on 2026-10-31 and is still empty.

| # | Date | KB | Pass | Fail |
|---|---|---|---|---|
| 4 | 2026-10-09 | 209 | 35 | 0 |
| 5 | 2026-10-09 | 174 | 28 | 0 |
| 6 | 2026-10-09 | 179 | 30 | 0 |
| 7 | 2026-10-09 | 184 | 31 | 0 |
| 8 | 2026-10-09 | 163 | 28 | 0 |
| 9 | 2026-10-09 | 188 | 29 | 0 |
| 10 | 2026-10-10 | 184 | 30 | 0 |
| 11 | 2026-10-10 | 180 | 30 | 0 |
| 12 | 2026-10-10 | 187 | 30 | 0 |
| 13 | 2026-10-10 | 195 | 30 | 0 |
| 14 | 2026-10-10 | 200 | 30 | 0 |
| 15 | 2026-10-10 | 129 | 20 | 0 |
| 16 | 2026-10-10 | 135 | 20 | 0 |
| 17 | 2026-10-10 | 131 | 20 | 0 |
| 18 | 2026-10-10 | 134 | 20 | 0 |
| 19 | 2026-10-10 | 130 | 20 | 0 |
| 20 | 2026-10-10 | 140 | 20 | 0 |
| 21 | 2026-10-10 | 144 | 20 | 0 |
| 22 | 2026-10-10 | 134 | 20 | 0 |
| 23 | 2026-10-10 | 139 | 20 | 0 |
| 24 | 2026-10-10 | 138 | 20 | 0 |
| 25 | 2026-10-10 | 140 | 20 | 0 |
| 26 | 2026-10-10 | 134 | 20 | 0 |
| 27 | 2026-10-10 | 146 | 20 | 0 |
| 28 | 2026-10-10 | 149 | 20 | 0 |
| 29 | 2026-10-10 | 138 | 20 | 0 |
| 30 | 2026-10-10 | 143 | 20 | 0 |
| 31 | 2026-10-10 | 143 | 20 | 0 |
| 32 | 2026-10-10 | 142 | 20 | 0 |
| 33 | 2026-10-10 | 140 | 20 | 0 |
| 34 | 2026-10-10 | 150 | 20 | 0 |
| 35 | 2026-10-10 | 153 | 20 | 0 |
| 36 | 2026-10-10 | 143 | 20 | 0 |
| 37 | 2026-10-10 | 148 | 20 | 0 |
| 38 | 2026-10-10 | 145 | 20 | 0 |
| 39 | 2026-10-10 | 147 | 20 | 0 |
| 40 | 2026-10-10 | 144 | 20 | 0 |
| 41 | 2026-10-10 | 152 | 20 | 0 |
| 42 | 2026-10-10 | 157 | 20 | 0 |
| 43 | 2026-10-10 | 146 | 20 | 0 |
| 44 | 2026-10-10 | 150 | 20 | 0 |
| 45 | 2026-10-10 | 149 | 20 | 0 |
| 46 | 2026-10-10 | 150 | 20 | 0 |
| 47 | 2026-10-10 | 147 | 20 | 0 |
| 48 | 2026-10-10 | 168 | 21 | 0 |
| 49 | 2026-10-10 | 160 | 20 | 0 |
| 50 | 2026-10-10 | 150 | 20 | 0 |
| 51 | 2026-10-10 | 154 | 20 | 0 |
| 52 | 2026-10-10 | 153 | 20 | 0 |
| 53 | 2026-10-10 | 154 | 20 | 0 |
| 54 | 2026-10-10 | 151 | 20 | 0 |
| 55 | 2026-10-11 | 161 | 20 | 0 |
| 56 | 2026-10-11 | 165 | 20 | 0 |
| 57 | 2026-10-11 | 154 | 20 | 0 |
| 58 | 2026-10-11 | 158 | 20 | 0 |
| 59 | 2026-10-11 | 157 | 20 | 0 |
| 60 | 2026-10-11 | 156 | 20 | 0 |
| 61 | 2026-10-11 | 156 | 20 | 0 |
| 62 | 2026-10-11 | 164 | 20 | 0 |
| 63 | 2026-10-11 | 169 | 20 | 0 |
| 64 | 2026-10-11 | 158 | 20 | 0 |
| 65 | 2026-10-11 | 161 | 20 | 0 |
| 66 | 2026-10-11 | 161 | 20 | 0 |
| 67 | 2026-10-11 | 162 | 20 | 0 |
| 68 | 2026-10-11 | 158 | 20 | 0 |
| 69 | 2026-10-11 | 168 | 20 | 0 |
| 70 | 2026-10-11 | 172 | 20 | 0 |
| 71 | 2026-10-11 | 160 | 20 | 0 |
| 72 | 2026-10-11 | 167 | 20 | 0 |
| 73 | 2026-10-11 | 168 | 20 | 0 |
| 74 | 2026-10-11 | 168 | 20 | 0 |
| 75 | 2026-10-11 | 167 | 20 | 0 |
| 76 | 2026-10-11 | 178 | 20 | 0 |
| 77 | 2026-10-11 | 181 | 20 | 0 |
| 78 | 2026-10-11 | 173 | 20 | 0 |
| 79 | 2026-10-11 | 178 | 20 | 0 |
| 80 | 2026-10-11 | 176 | 20 | 0 |
| 81 | 2026-10-11 | 179 | 20 | 0 |
| 82 | 2026-10-11 | 151 | 20 | 0 |
| 83 | 2026-10-11 | 135 | 20 | 0 |
| 84 | 2026-10-11 | 139 | 20 | 0 |
| 85 | 2026-10-11 | 131 | 20 | 0 |
| 86 | 2026-10-11 | 133 | 20 | 0 |
| 87 | 2026-10-11 | 132 | 20 | 0 |
| 88 | 2026-10-11 | 133 | 20 | 0 |
| 89 | 2026-10-11 | 129 | 20 | 0 |
| 90 | 2026-10-11 | 139 | 20 | 0 |
| 91 | 2026-10-11 | 144 | 20 | 0 |
| 92 | 2026-10-11 | 139 | 20 | 0 |
| 93 | 2026-10-11 | 139 | 20 | 0 |
| 94 | 2026-10-11 | 135 | 20 | 0 |
| 95 | 2026-10-11 | 136 | 20 | 0 |
| 96 | 2026-10-11 | 134 | 20 | 0 |
| 97 | 2026-10-11 | 144 | 20 | 0 |
| 98 | 2026-10-11 | 147 | 20 | 0 |
| 99 | 2026-10-11 | 140 | 20 | 0 |
| 100 | 2026-10-11 | 143 | 20 | 0 |
| 101 | 2026-10-11 | 141 | 20 | 0 |
| 102 | 2026-10-11 | 151 | 20 | 0 |
| 103 | 2026-10-12 | 140 | 20 | 0 |
| 104 | 2026-10-12 | 148 | 20 | 0 |
| 105 | 2026-10-12 | 153 | 20 | 0 |
| 106 | 2026-10-12 | 142 | 20 | 0 |
| 107 | 2026-10-12 | 146 | 20 | 0 |
| 108 | 2026-10-12 | 146 | 20 | 0 |
| 109 | 2026-10-12 | 147 | 20 | 0 |
| 110 | 2026-10-12 | 142 | 20 | 0 |
| 111 | 2026-10-12 | 152 | 20 | 0 |
| 112 | 2026-10-12 | 156 | 20 | 0 |
| 113 | 2026-10-12 | 145 | 20 | 0 |
| 114 | 2026-10-12 | 150 | 20 | 0 |
| 115 | 2026-10-12 | 149 | 20 | 0 |
| 116 | 2026-10-12 | 148 | 20 | 0 |
| 117 | 2026-10-12 | 147 | 20 | 0 |
| 118 | 2026-10-12 | 156 | 20 | 0 |
| 119 | 2026-10-12 | 159 | 20 | 0 |
| 120 | 2026-10-12 | 150 | 20 | 0 |
| 121 | 2026-10-12 | 154 | 20 | 0 |
| 122 | 2026-10-12 | 153 | 20 | 0 |
| 123 | 2026-10-12 | 155 | 20 | 0 |
| 124 | 2026-10-12 | 151 | 20 | 0 |
| 125 | 2026-10-12 | 161 | 20 | 0 |
| 126 | 2026-10-12 | 166 | 20 | 0 |
| 127 | 2026-10-12 | 154 | 20 | 0 |
| 128 | 2026-10-13 | 158 | 20 | 0 |
| 129 | 2026-10-16 | 157 | 20 | 0 |
| 130 | 2026-10-16 | 157 | 20 | 0 |
| 131 | 2026-10-16 | 160 | 20 | 0 |
| 132 | 2026-10-16 | 179 | 20 | 0 |
| 133 | 2026-10-16 | 168 | 20 | 0 |
| 134 | 2026-10-16 | 158 | 20 | 0 |
| 135 | 2026-10-16 | 170 | 20 | 0 |
| 136 | 2026-10-17 | 161 | 20 | 0 |
| 137 | 2026-10-17 | 161 | 20 | 0 |
| 138 | 2026-10-17 | 158 | 20 | 0 |
| 139 | 2026-10-17 | 168 | 20 | 0 |
| 140 | 2026-10-17 | 170 | 20 | 0 |
| 141 | 2026-10-17 | 161 | 20 | 0 |
| 142 | 2026-10-17 | 166 | 20 | 0 |
| 143 | 2026-10-17 | 163 | 20 | 0 |
| 144 | 2026-10-17 | 165 | 20 | 0 |
| 145 | 2026-10-17 | 162 | 20 | 0 |
| 146 | 2026-10-18 | 171 | 20 | 0 |
| 147 | 2026-10-20 | 175 | 20 | 0 |
| 148 | 2026-10-21 | 371 | 35 | 0 |
| 149 | 2026-10-23 | 184 | 21 | 0 |
| 150 | 2026-10-25 | 168 | 20 | 0 |
| 151 | 2026-10-27 | 178 | 20 | 0 |
| 152 | 2026-10-29 | 88 | 20 | 0 |
| 153 | 2026-10-31 | 0 | 0 | 0 |

## WC106 to WC2580: checks in five unnamed working notebooks

These notebooks are not in any folder (the cloud file browser lists them under **Unnamed**). Byte-identical copies with descriptive names (A to E, plus hard102, hard104, the Kerr metric and scalar field notebooks and WC1321) are in the cloud folder **Rescued unnamed notebooks** (2026-10-31); the originals are untouched. Together they hold 432 check cells covering 423 distinct check numbers. 420 cells carry verdicts: 442 passes and 0 failures (426 attributed to a numbered check below, 16 in output cells that follow a cell without a WC header). Twelve cells have no verdict, mostly earlier runs of a number that was rerun later.

| Notebook | Cloud id (first 8) | Created | Last modified | Size | Check cells | Check numbers | Passes |
|---|---|---|---|---|---|---|---|
| A | 19e1ce52 | 2026-09-20 | 2026-09-20 | 127 KB | 7 | WC106 to WC111 | 5 |
| B | 960a9c2b | 2026-09-20 | 2026-09-22 | 1228 KB | 60 | WC468 to WC535 | 68 |
| C | e9f193ec | 2026-09-22 | 2026-10-09 | 1186 KB | 237 | WC2161 to WC2395 | 237 |
| D | 9fd9f958 | 2026-10-09 | 2026-10-09 | 424 KB | 69 | WC2448 to WC2521 | 73 |
| E | 64ccd447 | 2026-10-09 | 2026-10-09 | 344 KB | 59 | WC2522 to WC2580 | 59 |

The checks rotate through a fixed set of families, each rerun with an incrementing parameter (Fib Step 45, 46, 47, and so on). Passes can exceed check numbers where one check emits more than one verdict.

| Family | Check numbers | Passes | No verdict | Range |
|---|---|---|---|---|
| Fib Step | 41 | 41 | 0 | WC469 to WC2579 |
| Split K | 41 | 41 | 0 | WC470 to WC2580 |
| Pair H (incl. spot check WC491) | 42 | 41 | 1 | WC471 to WC2571 |
| Toggle Step (incl. spot check WC513) | 42 | 41 | 1 | WC473 to WC2573 |
| Odd H (incl. spot check WC107) | 41 | 41 | 0 | WC107 to WC2577 |
| Match seals (Sierpinski, Chain27, Try3d, Doubleslit, Singleslit, Flat2d, Dim27) | 41 | 42 | 0 | WC476 to WC2576 |
| S singular-series seal | 28 | 30 | 0 | WC106 to WC2572 |
| S singular-series | 15 | 15 | 0 | WC472 to WC2562 |
| H8 First Seal | 22 | 21 | 1 | WC478 to WC2568 |
| H6 First Seal | 20 | 20 | 0 | WC468 to WC2578 |
| Twin Bound Seal | 17 | 17 | 0 | WC494 to WC2574 |
| Sort Annihilate Seal | 17 | 22 | 0 | WC495 to WC2575 |
| One Way L | 14 | 14 | 0 | WC474 to WC2564 |
| Hand Ci L | 13 | 12 | 4 | WC485 to WC2565 |
| Hand Conf L | 13 | 13 | 3 | WC475 to WC2555 |
| Coarse Grain Seal | 12 | 12 | 0 | WC484 to WC2554 |
| One-off rechecks (G Less H Spot, FS Symmetry Recheck, FS Triangle Recheck) | 3 | 3 | 0 | WC108 to WC110 |
| WC111 (untitled) | 1 | 0 | 2 | WC111 |

## Causal geometry experiments

The 13 notebooks in the cloud folder "Causal geometry experiments" use a `"held"` verdict instead of `"pass"`. Results, including first runs of four notebooks, fixed copies of two of them in the cloud, and the bugs that kept them from finishing, are in [CAUSAL_GEOMETRY.md](CAUSAL_GEOMETRY.md).
