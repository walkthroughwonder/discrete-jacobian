"""Certify an R2 convergence witness with explicit paths of at least two
steps from each seed.

This is a path certificate, not a shortest-path certificate: it does not
exclude a shorter common successor. In the checked artifact the two seeds
also share a one-step successor. The historical JSON kind is retained for
backward compatibility with the independent verifier.
"""
import json
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


def main():
    # systems with logged R2 convergence examples from the stage-3 log
    for line in open("maxsweep_log.jsonl"):
        rec = json.loads(line)
        if rec.get("stage") != 3 or not rec.get("r2_merges"):
            continue
        rules = [tuple(tuple(tuple(e) for e in side) for side in r)
                 for r in rec["rules"]]
        seeds = [s for s in enumerate_states(4, 3)]
        fwd = {s: bfs_paths(s, rules) for s in seeds}
        for s, t in combinations(seeds, 2):
            common = set(fwd[s]) & set(fwd[t]) - {s, t}
            for w in sorted(common):
                ps, pt = fwd[s][w], fwd[t][w]
                if len(ps) < 3 or len(pt) < 3:
                    continue  # require an explicit >=2-step path on both sides
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
                    "reachability_bounds": {"max_states": 800, "max_verts": 7},
                }
                json.dump(cert, open("cert_deep_r2.json", "w"), indent=1)
                print("R2 two-step path certificate written:")
                print("  rules:", rules)
                print("  seed1:", s, f"({len(ps)-1} steps)")
                print("  seed2:", t, f"({len(pt)-1} steps)")
                print("  witness:", w)
                return
    print("no qualifying R2 path found under constraints")


if __name__ == "__main__":
    main()
