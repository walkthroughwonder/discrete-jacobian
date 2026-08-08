"""R1 collision search: enumerate small states, apply the min-successor
policy, and report collisions F(S) = F(S') with S != S' (canonical forms).

Emits certificates as JSON for the independent verifier.
"""
import os
import json
import sys
from itertools import product

from core import canonical, f_min, successors


def enumerate_states(max_vertices, max_edges, arity=2):
    """All states up to iso with <= max_vertices vertices, 1..max_edges edges."""
    seen = set()
    verts = range(max_vertices)
    all_edges = list(product(verts, repeat=arity))
    def rec(edges, start):
        if edges:
            c = canonical(tuple(edges))
            if c not in seen and len({v for e in c for v in e}) <= max_vertices:
                seen.add(c)
        if len(edges) == max_edges:
            return
        for i in range(start, len(all_edges)):
            rec(edges + [all_edges[i]], i)  # i (not i+1): allow multi-edges
    rec([], 0)
    return sorted(seen)


def reachable(src, dst, rules, max_states=2000, max_verts=7):
    """Is dst reachable from src under any rule applications (bounded BFS)?

    Bounded in explored-state count AND vertex count (canonicalization is
    |V|! — states past max_verts are not expanded). A negative answer is
    therefore "not reachable within bounds": safe for quarantining orbit
    artifacts (may over-quarantine, never under-quarantines... note the
    asymmetry: bounds can only cause a FALSE NEGATIVE here, i.e. a genuine
    orbit relation missed, letting an artifact through as 'genuine'. The
    independent verifier does not check reachability, so any claimed
    counterexample must additionally document its reachability analysis)."""
    seen = {src}
    frontier = [src]
    while frontier and len(seen) < max_states:
        nxt = []
        for s in frontier:
            if len({v for e in s for v in e}) > max_verts:
                continue
            for t in successors(s, rules):
                if t == dst:
                    return True
                if t not in seen:
                    seen.add(t)
                    nxt.append(t)
        frontier = nxt
    return dst in seen


def find_r1_collisions(rules, max_vertices=4, max_edges=3):
    """Returns (states, genuine, artifacts).

    genuine: image -> list of pairwise mutually-unreachable preimages (>=2).
    artifacts: image -> preimage lists whose collisions are orbit artifacts
    (some pair mutually reachable) — reported, never claimed as collisions.
    """
    states = enumerate_states(max_vertices, max_edges)
    table = {}
    for s in states:
        img = f_min(s, rules)
        if img is not None:
            table.setdefault(img, []).append(s)
    genuine, artifacts = {}, {}
    for img, pre in table.items():
        if len(pre) < 2:
            continue
        core_pre = []
        for s in pre:
            if any(reachable(s, t, rules) and reachable(t, s, rules)
                   for t in core_pre):
                continue  # same orbit as an already-kept representative
            core_pre.append(s)
        if len(core_pre) >= 2:
            genuine[img] = core_pre
        else:
            artifacts[img] = pre
    return states, genuine, artifacts


def certificate(rules, s1, s2, image):
    return {
        "kind": "R1-collision",
        "policy": "min-successor",
        "rules": [[list(map(list, side)) for side in rule] for rule in rules],
        "state1": [list(e) for e in s1],
        "state2": [list(e) for e in s2],
        "claimed_image": [list(e) for e in image],
    }


if __name__ == "__main__":
    # Planted test system: edge deletion {{x,y}} -> {} . Non-D1 (the reverse
    # would have to create an edge with no way to know where): collisions
    # expected. This is the Phase 1 round-trip target, not a research claim.
    delete_rule = ((("x", "y"),), ())
    states, collisions, artifacts = find_r1_collisions([delete_rule])
    print(f"enumerated {len(states)} states")
    print(f"genuine collision images: {len(collisions)} "
          f"(orbit artifacts: {len(artifacts)})")
    for img, pre in sorted(collisions.items())[:5]:
        print(f"  image {img}  <-  {pre[:4]}")
    if collisions:
        img, pre = sorted(collisions.items())[0]
        cert = certificate([delete_rule], pre[0], pre[1], img)
        out = sys.argv[1] if len(sys.argv) > 1 else "planted_cert.json"
        # planted_cert.json is committed evidence; do not clobber it on a
        # bare `python search.py`. An explicit argv[1] is a deliberate choice
        # and is honoured.
        if len(sys.argv) <= 1 and os.path.exists(out):
            out = "planted_cert.rerun.json"
            print(f"[cert] planted_cert.json exists and is committed "
                  f"evidence; writing this run to {out} instead.")
        with open(out, "w") as f:
            json.dump(cert, f, indent=1)
        print(f"certificate written: {out}")
