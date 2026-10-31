# Wolfram Cloud verification runs: index

*Snapshot taken 2026-10-30 from Edwin Rosero's Wolfram Cloud account (read-only scan). The notebooks themselves live in the cloud; this file records what each one checked and how its verdicts came out.*

Each check emits an association with `"pass" -> True|False` and a `"gate"` field. Every verdict in every notebook carries `"gate" -> "HOLD"` and `"claim_3" -> False`, so none of these runs promoted a claim on its own.

## Summary

| Series | Notebooks | Dates | With verdicts | Pass | Fail |
|---|---|---|---|---|---|
| WC (single cloud checks) | 76 | 2026-09-19 to 2026-10-06 | 35 | 49 | 2 |
| Lite Seals (batched seals) | 149 | 2026-10-09 to 2026-10-29 | 149 | 3191 | 88 |

### What the failures are

- **Lite Seals: 88 failures, all the same check timing out.** In each of the 88 affected notebooks the single failing verdict carries `"status" -> "TIMEOUT"`: the confluence / critical-pair analysis exceeded the cloud time limit. It is not a wrong mathematical result, and the companion run of the same analysis (L = 3 or 4, 85 states, 147 events, 0 overlapping pairs) passes in the same notebook. The timing-out and non-timing-out notebooks alternate almost perfectly by number, which suggests two batch variants rather than flakiness.
- **WC73 and WC76 (resolved 2026-10-30).** Both compute the singular series S for the pattern {0, 2, 4}. The exact value is S = 0, because {0, 2, 4} covers every residue mod 3, so the local factor at p = 3 vanishes. WC73 tested the claim "S is nonzero"; its failure is the mathematically correct outcome. WC76 reported S = 1 only because its notebook is corrupted: the full text of WC77 was pasted inside its product loop's iterator, so the loop never ran and the product kept its initial value 1 (reproduced exactly). Rerun cleanly in Wolfram Language, WC76 passes with S = 0. No genuine contradiction remains.
- **Cleanup note (2026-10-30).** Five empty or superseded items were moved to the cloud Trash (two blank notebooks, a scratchpad link, WC103 "old" and WC37 "Error"); the scans above were taken before that, so WC37 Error and WC103 old still appear in the tables.
- **41 WC notebooks have no pass/fail field** (mostly WC1 to WC31, the earliest runs, which print raw values instead). WC37 "Sort Annihilate Regression Error" was never evaluated (0 outputs).

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
| WC37 | Sort Annihilate Regression Error | 2026-09-19 | 6 | 0 | 0 | 0 |
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
| WC72 | H3 Existence Spot | 2026-09-20 | 5 | 2 | 0 | 1 |
| WC73 | S Zero Two Four **(fail; correct, see above)** | 2026-09-20 | 4 | 0 | 1 | 1 |
| WC75 | Twin Bound Spot | 2026-09-20 | 4 | 1 | 0 | 1 |
| WC76 | S Zero Two Four Seal **(fail; corrupted notebook, passes on clean rerun)** | 2026-09-20 | 9 | 0 | 1 | 1 |
| WC77 | Odd H Absent Spot | 2026-09-20 | 3 | 1 | 0 | 1 |
| WC78 | Even H Four Spot | 2026-09-20 | 3 | 1 | 0 | 1 |
| WC81 | Pair H Ten Spot | 2026-09-20 | 10 | 3 | 0 | 3 |
| WC82 | S Zero Four Six | 2026-09-20 | 3 | 2 | 0 | 1 |
| WC87 | Odd H Seven Spot | 2026-09-20 | 31 | 3 | 0 | 4 |
| WC92 | S Zero Six Twelve | 2026-09-20 | 20 | 4 | 0 | 4 |
| WC93 | Toggle Step Eight Spot | 2026-09-20 | 4 | 1 | 0 | 1 |
| WC94 | Match Dim27 Again | 2026-09-20 | 6 | 0 | 0 | 1 |
| WC98 | H6 First Five | 2026-09-20 | 8 | 2 | 0 | 2 |
| WC99 | Fib Step Nine Spot | 2026-09-20 | 3 | 1 | 0 | 1 |
| WC101 | Pair H Fourteen Spot | 2026-09-20 | 12 | 2 | 0 | 2 |
| WC103 | Toggle Step Ten Spot | 2026-09-20 | 3 | 1 | 0 | 1 |
| WC103 | Toggle Step Ten Spot old | 2026-09-20 | 7 | 1 | 0 | 1 |
| WC105 | Twin Bound Recheck | 2026-09-20 | 21 | 1 | 0 | 2 |

## Lite Seals series

Numbered by spelled-out name ("Lite Seals Four" = 4). Fail = 1 means the one confluence check timed out (see above).

| # | Date | KB | Pass | Fail |
|---|---|---|---|---|
| 4 | 2026-10-09 | 209 | 36 | 1 |
| 5 | 2026-10-09 | 174 | 31 | 1 |
| 6 | 2026-10-09 | 179 | 31 | 1 |
| 7 | 2026-10-09 | 184 | 32 | 1 |
| 8 | 2026-10-09 | 163 | 30 | 0 |
| 9 | 2026-10-09 | 188 | 31 | 1 |
| 10 | 2026-10-10 | 184 | 31 | 1 |
| 11 | 2026-10-10 | 180 | 31 | 1 |
| 12 | 2026-10-10 | 187 | 31 | 1 |
| 13 | 2026-10-10 | 195 | 31 | 1 |
| 14 | 2026-10-10 | 200 | 31 | 1 |
| 15 | 2026-10-10 | 129 | 20 | 0 |
| 16 | 2026-10-10 | 135 | 21 | 1 |
| 17 | 2026-10-10 | 131 | 20 | 0 |
| 18 | 2026-10-10 | 134 | 21 | 1 |
| 19 | 2026-10-10 | 130 | 20 | 0 |
| 20 | 2026-10-10 | 140 | 21 | 1 |
| 21 | 2026-10-10 | 144 | 21 | 1 |
| 22 | 2026-10-10 | 134 | 20 | 0 |
| 23 | 2026-10-10 | 139 | 21 | 1 |
| 24 | 2026-10-10 | 138 | 20 | 0 |
| 25 | 2026-10-10 | 140 | 21 | 1 |
| 26 | 2026-10-10 | 134 | 20 | 0 |
| 27 | 2026-10-10 | 146 | 21 | 1 |
| 28 | 2026-10-10 | 149 | 21 | 1 |
| 29 | 2026-10-10 | 138 | 20 | 0 |
| 30 | 2026-10-10 | 143 | 21 | 1 |
| 31 | 2026-10-10 | 143 | 20 | 0 |
| 32 | 2026-10-10 | 142 | 21 | 1 |
| 33 | 2026-10-10 | 140 | 20 | 0 |
| 34 | 2026-10-10 | 150 | 21 | 1 |
| 35 | 2026-10-10 | 153 | 21 | 1 |
| 36 | 2026-10-10 | 143 | 20 | 0 |
| 37 | 2026-10-10 | 148 | 21 | 1 |
| 38 | 2026-10-10 | 145 | 20 | 0 |
| 39 | 2026-10-10 | 147 | 21 | 1 |
| 40 | 2026-10-10 | 144 | 20 | 0 |
| 41 | 2026-10-10 | 152 | 21 | 1 |
| 42 | 2026-10-10 | 157 | 21 | 1 |
| 43 | 2026-10-10 | 146 | 20 | 0 |
| 44 | 2026-10-10 | 150 | 21 | 1 |
| 45 | 2026-10-10 | 149 | 20 | 0 |
| 46 | 2026-10-10 | 150 | 21 | 1 |
| 47 | 2026-10-10 | 147 | 20 | 0 |
| 48 | 2026-10-10 | 168 | 22 | 1 |
| 49 | 2026-10-10 | 160 | 21 | 1 |
| 50 | 2026-10-10 | 150 | 20 | 0 |
| 51 | 2026-10-10 | 154 | 21 | 1 |
| 52 | 2026-10-10 | 153 | 20 | 0 |
| 53 | 2026-10-10 | 154 | 21 | 1 |
| 54 | 2026-10-10 | 151 | 20 | 0 |
| 55 | 2026-10-11 | 161 | 21 | 1 |
| 56 | 2026-10-11 | 165 | 21 | 1 |
| 57 | 2026-10-11 | 154 | 20 | 0 |
| 58 | 2026-10-11 | 158 | 21 | 1 |
| 59 | 2026-10-11 | 157 | 20 | 0 |
| 60 | 2026-10-11 | 156 | 21 | 1 |
| 61 | 2026-10-11 | 156 | 20 | 0 |
| 62 | 2026-10-11 | 164 | 21 | 1 |
| 63 | 2026-10-11 | 169 | 21 | 1 |
| 64 | 2026-10-11 | 158 | 20 | 0 |
| 65 | 2026-10-11 | 161 | 21 | 1 |
| 66 | 2026-10-11 | 161 | 20 | 0 |
| 67 | 2026-10-11 | 162 | 21 | 1 |
| 68 | 2026-10-11 | 158 | 20 | 0 |
| 69 | 2026-10-11 | 168 | 21 | 1 |
| 70 | 2026-10-11 | 172 | 21 | 1 |
| 71 | 2026-10-11 | 160 | 20 | 0 |
| 72 | 2026-10-11 | 167 | 21 | 1 |
| 73 | 2026-10-11 | 168 | 20 | 0 |
| 74 | 2026-10-11 | 168 | 21 | 1 |
| 75 | 2026-10-11 | 167 | 20 | 0 |
| 76 | 2026-10-11 | 178 | 21 | 1 |
| 77 | 2026-10-11 | 181 | 21 | 1 |
| 78 | 2026-10-11 | 173 | 20 | 0 |
| 79 | 2026-10-11 | 178 | 21 | 1 |
| 80 | 2026-10-11 | 176 | 20 | 0 |
| 81 | 2026-10-11 | 179 | 21 | 1 |
| 82 | 2026-10-11 | 151 | 20 | 0 |
| 83 | 2026-10-11 | 135 | 21 | 1 |
| 84 | 2026-10-11 | 139 | 21 | 1 |
| 85 | 2026-10-11 | 131 | 20 | 0 |
| 86 | 2026-10-11 | 133 | 21 | 1 |
| 87 | 2026-10-11 | 132 | 20 | 0 |
| 88 | 2026-10-11 | 133 | 21 | 1 |
| 89 | 2026-10-11 | 129 | 20 | 0 |
| 90 | 2026-10-11 | 139 | 21 | 1 |
| 91 | 2026-10-11 | 144 | 21 | 1 |
| 92 | 2026-10-11 | 139 | 20 | 0 |
| 93 | 2026-10-11 | 139 | 21 | 1 |
| 94 | 2026-10-11 | 135 | 20 | 0 |
| 95 | 2026-10-11 | 136 | 21 | 1 |
| 96 | 2026-10-11 | 134 | 20 | 0 |
| 97 | 2026-10-11 | 144 | 21 | 1 |
| 98 | 2026-10-11 | 147 | 21 | 1 |
| 99 | 2026-10-11 | 140 | 20 | 0 |
| 100 | 2026-10-11 | 143 | 21 | 1 |
| 101 | 2026-10-11 | 141 | 20 | 0 |
| 102 | 2026-10-11 | 151 | 21 | 1 |
| 103 | 2026-10-12 | 140 | 20 | 0 |
| 104 | 2026-10-12 | 148 | 21 | 1 |
| 105 | 2026-10-12 | 153 | 21 | 1 |
| 106 | 2026-10-12 | 142 | 20 | 0 |
| 107 | 2026-10-12 | 146 | 21 | 1 |
| 108 | 2026-10-12 | 146 | 20 | 0 |
| 109 | 2026-10-12 | 147 | 21 | 1 |
| 110 | 2026-10-12 | 142 | 20 | 0 |
| 111 | 2026-10-12 | 152 | 21 | 1 |
| 112 | 2026-10-12 | 156 | 21 | 1 |
| 113 | 2026-10-12 | 145 | 20 | 0 |
| 114 | 2026-10-12 | 150 | 21 | 1 |
| 115 | 2026-10-12 | 149 | 20 | 0 |
| 116 | 2026-10-12 | 148 | 21 | 1 |
| 117 | 2026-10-12 | 147 | 20 | 0 |
| 118 | 2026-10-12 | 156 | 21 | 1 |
| 119 | 2026-10-12 | 159 | 21 | 1 |
| 120 | 2026-10-12 | 150 | 20 | 0 |
| 121 | 2026-10-12 | 154 | 21 | 1 |
| 122 | 2026-10-12 | 153 | 20 | 0 |
| 123 | 2026-10-12 | 155 | 21 | 1 |
| 124 | 2026-10-12 | 151 | 20 | 0 |
| 125 | 2026-10-12 | 161 | 21 | 1 |
| 126 | 2026-10-12 | 166 | 21 | 1 |
| 127 | 2026-10-12 | 154 | 20 | 0 |
| 128 | 2026-10-13 | 158 | 21 | 1 |
| 129 | 2026-10-16 | 157 | 20 | 0 |
| 130 | 2026-10-16 | 157 | 21 | 1 |
| 131 | 2026-10-16 | 160 | 20 | 0 |
| 132 | 2026-10-16 | 179 | 21 | 1 |
| 133 | 2026-10-16 | 168 | 21 | 1 |
| 134 | 2026-10-16 | 158 | 20 | 0 |
| 135 | 2026-10-16 | 170 | 21 | 1 |
| 136 | 2026-10-17 | 161 | 20 | 0 |
| 137 | 2026-10-17 | 161 | 21 | 1 |
| 138 | 2026-10-17 | 158 | 20 | 0 |
| 139 | 2026-10-17 | 168 | 21 | 1 |
| 140 | 2026-10-17 | 170 | 21 | 1 |
| 141 | 2026-10-17 | 161 | 20 | 0 |
| 142 | 2026-10-17 | 166 | 21 | 1 |
| 143 | 2026-10-17 | 163 | 20 | 0 |
| 144 | 2026-10-17 | 165 | 21 | 1 |
| 145 | 2026-10-17 | 162 | 20 | 0 |
| 146 | 2026-10-18 | 171 | 21 | 1 |
| 147 | 2026-10-20 | 175 | 21 | 1 |
| 148 | 2026-10-21 | 371 | 35 | 0 |
| 149 | 2026-10-23 | 184 | 22 | 1 |
| 150 | 2026-10-25 | 168 | 20 | 0 |
| 151 | 2026-10-27 | 178 | 21 | 1 |
| 152 | 2026-10-29 | 88 | 10 | 0 |
