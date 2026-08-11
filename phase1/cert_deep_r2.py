"""Certify one genuinely multi-step R2 merge: two mutually-unreachable seeds
whose multiway futures intersect only after >=2 steps. Emits a path
certificate (explicit step sequences) for independent replay.

CR11 fix (2026-08-11): the original predicate only required the CHOSEN
witness to sit >=2 steps from each seed, never that no SHALLOWER meeting
point exists — so a pair whose futures already intersect after one step
could be certified as "deep" (the retracted first cert_deep_r2.json was
exactly that: both emitted paths passed through the same depth-1 state).
A pair now qualifies only if the seeds share no common state at any depth
shorter than the witness paths: their exact one-step canonical successor
sets must be disjoint, no one-step successor of either seed may appear
anywhere in the other's explored future, and the witness is chosen at the
earliest intersection depth."""
import json
import sys
import time
from itertools import combinations

from core import canonical, successors
from search import enumerate_states, reachable


def bfs_paths(seed, rules, depth=3, cap=400, max_verts=6):
    """state -> shortest path (list of states) from seed."""
    paths = {seed: [seed]}
    frontier = [seed]
    for _ in range(depth):
        nxt = []
        for s in frontier:
            if len({v for e in s for v in e}) > max_verts:
                continue
            for t in successors(s, rules):
                if t not in paths and len(paths) < cap:
                    paths[t] = paths[s] + [t]
                    nxt.append(t)
        frontier = nxt
    return paths


def main(budget=600.0):
    start = time.time()
    # systems with known multi-step merges, from the maxsweep stage-3 log
    for line in open("maxsweep_log.jsonl"):
        if time.time() - start > budget:
            print(f"time budget exhausted ({budget:.0f}s); "
                  "no deep merge certified")
            return
        rec = json.loads(line)
        if rec.get("stage") != 3 or not rec.get("r2_merges"):
            continue
        rules = [tuple(tuple(tuple(e) for e in side) for side in r)
                 for r in rec["rules"]]
        seeds = [s for s in enumerate_states(4, 3)]
        fwd = {s: bfs_paths(s, rules) for s in seeds}
        succ = {s: successors(s, rules) for s in seeds}  # exact, unbounded
        for s, t in combinations(seeds, 2):
            if succ[s] & succ[t]:
                continue  # futures meet after ONE step: reducible, not deep
            if succ[s] & set(fwd[t]) or succ[t] & set(fwd[s]):
                continue  # a depth-1 state of one seed sits in the other's
                          # future: some meeting point is <2 steps away
            common = set(fwd[s]) & set(fwd[t]) - {s, t}
            if not common:
                continue
            # every remaining common state is >=2 steps from BOTH seeds;
            # the witness is the SHALLOWEST one (earliest intersection),
            # so no shorter meeting point exists to undercut the claim
            w = min(common,
                    key=lambda c: (max(len(fwd[s][c]), len(fwd[t][c])), c))
            ps, pt = fwd[s][w], fwd[t][w]
            if reachable(s, t, rules, max_states=800, max_verts=7) or \
               reachable(t, s, rules, max_states=800, max_verts=7):
                continue
            cert = {
                "kind": "R2-deep-merge",
                "rules": [[[list(e) for e in side] for side in r]
                          for r in rules],
                "seed1": [list(e) for e in s],
                "seed2": [list(e) for e in t],
                "path1": [[list(e) for e in st] for st in ps],
                "path2": [[list(e) for e in st] for st in pt],
                "witness": [list(e) for e in w],
                "earliest_intersection_steps": max(len(ps), len(pt)) - 1,
                "one_step_successor_sets_disjoint": True,
                "reachability_bounds": {"max_states": 800, "max_verts": 7},
            }
            json.dump(cert, open("cert_deep_r2.json", "w"), indent=1)
            print("deep R2 merge certified:")
            print("  rules:", rules)
            print("  seed1:", s, f"({len(ps)-1} steps)")
            print("  seed2:", t, f"({len(pt)-1} steps)")
            print("  witness:", w,
                  f"(earliest intersection: {max(len(ps), len(pt)) - 1} steps)")
            return
    print("no deep merge found under constraints")


if __name__ == "__main__":
    main(float(sys.argv[1]) if len(sys.argv) > 1 else 600.0)
