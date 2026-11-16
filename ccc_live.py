"""Which universes keep recurring under the crossover map (see CCC_CROSSOVER.md).

For each E and reseed rule: find every attractor of the cycle map
(aeon then reseed), mark it live if a splice fires anywhere on its orbit,
and report the share of starting states that end live, by the vertex count V
of the starting state. Also writes every live attractor (orbit states,
terminal states, splices per aeon) to ccc_live_E{max_E}.json.

Usage: python3 ccc_live.py [max_E]   (default 6; about 10 s)
Needs ccc_crossover.py in the same folder.
"""
import json
import os
import sys
from collections import Counter, defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ccc_crossover as cc  # noqa: E402


def cycle_map(E, rule):
    states = cc.all_states(E)
    C = {}

    def step(s):
        if s not in C:
            C[s] = cc.RESEEDS[rule](cc.aeon(s))
        return C[s]

    on, end = {}, {}
    for s in states:
        path, seen, x = [], {}, s
        while x not in seen and x not in on:
            seen[x] = len(path)
            path.append(x)
            x = step(x)
        if x in seen and x not in on:
            cyc = path[seen[x]:]
            cid = min(cyc)
            for y in cyc:
                on[y] = cid
        end[s] = on[x]
    orbits = defaultdict(list)
    for y, cid in on.items():
        orbits[cid].append(y)
    return states, C, end, orbits


def nverts(s):
    return len({v for e in s for v in e})


def analyse_live(E, rule):
    states, C, end, orbits = cycle_map(E, rule)
    live = {cid: any(cc.successors(x) for x in orb) for cid, orb in orbits.items()}
    byV = defaultdict(lambda: [0, 0])
    for s in states:
        byV[nverts(s)][0] += live[end[s]]
        byV[nverts(s)][1] += 1
    basin = Counter(end.values())
    out = []
    for cid, is_live in live.items():
        if not is_live:
            continue
        orb, x = [cid], C[cid]
        while x != cid:
            orb.append(x)
            x = C[x]
        out.append({
            "E": E, "rule": rule, "period": len(orb), "basin": basin[cid],
            "V": nverts(cid),
            "splices_per_aeon": [cc.loops(x) - cc.loops(cc.aeon(x)) for x in orb],
            "states": [list(map(list, x)) for x in orb],
            "terminal": [list(map(list, cc.aeon(x))) for x in orb],
        })
    share = {V: round(a / b, 3) for V, (a, b) in sorted(byV.items())}
    counts = {V: b for V, (a, b) in sorted(byV.items())}
    return {"E": E, "rule": rule, "live_share_by_V": share, "states_by_V": counts}, out


if __name__ == "__main__":
    max_E = int(sys.argv[1]) if len(sys.argv) > 1 else 6
    attractors = []
    for E in range(2, max_E + 1):
        for rule in cc.RESEEDS:
            summary, live = analyse_live(E, rule)
            attractors += live
            print(json.dumps(summary), flush=True)
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), f"ccc_live_E{max_E}.json"), "w") as f:
        json.dump(attractors, f)
    print(len(attractors), "live attractors written", flush=True)
