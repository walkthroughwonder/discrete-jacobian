"""Crossover map: repeated "aeons" of the splice rule, each followed by a
"new big bang" that reseeds loops using only the dead state's own structure.

Rule (flagship splice):  {(a,a),(b,c)} -> {(a,b),(c,a)}, a, b, c distinct.

One cycle C = reseed o aeon:
  aeon(S)   run the splice rule under the min-successor policy until no
            match exists (the clock of loops has run down);
  reseed(T) an isomorphism-invariant "big bang" that turns edges into loops
            using only T's own shape:
              SINK   every non-loop edge (u, v) with out-degree(v) = 0
                     becomes the loop (v, v);
              SOURCE every non-loop edge (u, v) with in-degree(u) = 0
                     becomes the loop (u, u).
Edge count is conserved by both steps, so the set of all states with E edges
is a finite closed universe and C is a deterministic map on it. States are
compared up to isomorphism (canonical forms).

Measured, starting from every state with E edges equally likely:
  * entropy of the state distribution after each cycle (bits forgotten);
  * the attractors of C: fixed points and periodic orbits, i.e. universes
    that end up repeating the same sequence of aeons forever;
  * "dead" attractors, where the reseed creates no loop and nothing ever
    happens again;
  * how many cycles it takes to reach an attractor (longest transient).

Self-contained; no dependency on the repository engine.
"""
import json
import math
import sys
from collections import Counter, defaultdict
from functools import lru_cache
from itertools import permutations, product


def relabel(edges):
    vs = sorted({v for e in edges for v in e})
    mp = {v: i for i, v in enumerate(vs)}
    return tuple(sorted((mp[a], mp[b]) for a, b in edges))


@lru_cache(maxsize=None)
def canon(state):
    if not state:
        return ()
    vs = sorted({v for e in state for v in e})
    sig = {v: [0, 0, 0] for v in vs}
    for x, y in state:
        if x == y:
            sig[x][2] += 1
        else:
            sig[x][0] += 1
            sig[y][1] += 1
    groups = defaultdict(list)
    for v in vs:
        groups[tuple(sig[v])].append(v)
    classes = [groups[k] for k in sorted(groups)]
    offsets, o = [], 0
    for c in classes:
        offsets.append(o)
        o += len(c)
    best = None
    for perms in product(*[permutations(c) for c in classes]):
        mp = {}
        for off, p in zip(offsets, perms):
            for i, v in enumerate(p):
                mp[v] = off + i
        cand = tuple(sorted((mp[x], mp[y]) for x, y in state))
        if best is None or cand < best:
            best = cand
    return best


@lru_cache(maxsize=None)
def successors(state):
    out = set()
    n = len(state)
    for i in range(n):
        a, a2 = state[i]
        if a != a2:
            continue
        for j in range(n):
            if j == i:
                continue
            b, c = state[j]
            if b == c or a in (b, c):
                continue
            rest = [state[k] for k in range(n) if k not in (i, j)]
            out.add(canon(relabel(rest + [(a, b), (c, a)])))
    return frozenset(out)


@lru_cache(maxsize=None)
def aeon(state):
    """Min-successor evolution to a terminal (match-free) state."""
    s = state
    while True:
        nxt = successors(s)
        if not nxt:
            return s
        s = min(nxt)


def reseed_sink(state):
    outdeg = Counter(x for x, y in state if x != y)
    new = [(y, y) if (x != y and outdeg[y] == 0) else (x, y) for x, y in state]
    return canon(relabel(new))


def reseed_source(state):
    indeg = Counter(y for x, y in state if x != y)
    new = [(x, x) if (x != y and indeg[x] == 0) else (x, y) for x, y in state]
    return canon(relabel(new))


RESEEDS = {"sink": reseed_sink, "source": reseed_source}


def all_states(E):
    layer = {()}
    for _ in range(E):
        nxt = set()
        for s in layer:
            n = len({v for e in s for v in e})
            for x in range(n + 2):
                for y in range(n + 2):
                    nxt.add(canon(relabel(s + ((x, y),))))
        layer = nxt
    return sorted(layer)


def entropy(counter):
    tot = sum(counter.values())
    return -sum(c / tot * math.log2(c / tot) for c in counter.values() if c)


def loops(s):
    return sum(1 for x, y in s if x == y)


def analyse(E, rule):
    states = all_states(E)
    C = {s: RESEEDS[rule](aeon(s)) for s in states}
    # every image is again a state with E edges, so C maps the universe to itself
    assert all(len(t) == E for t in C.values())
    for t in set(C.values()):
        if t not in C:
            C[t] = RESEEDS[rule](aeon(t))

    # attractors (periodic orbits) of the functional graph
    on_cycle = {}
    for s in states:
        path, seen = [], {}
        x = s
        while x not in seen and x not in on_cycle:
            seen[x] = len(path)
            path.append(x)
            x = C[x]
        if x in seen and x not in on_cycle:
            cyc = path[seen[x]:]
            cid = min(cyc)
            for y in cyc:
                on_cycle[y] = (cid, len(cyc))
    cycles = {}
    for y, (cid, L) in on_cycle.items():
        cycles.setdefault(cid, L)

    def orbit(cid):
        xs, x = [cid], C[cid]
        while x != cid:
            xs.append(x)
            x = C[x]
        return xs

    def is_dead(cid):
        # frozen universe: no splice ever fires anywhere on the orbit, so
        # nothing happens again (loop-free, or loops that can never match)
        return all(not successors(x) for x in orbit(cid))

    # transient length and basin of each state
    depth, basin = {}, Counter()
    for s in states:
        x, k = s, 0
        while x not in on_cycle:
            x = C[x]
            k += 1
        depth[s] = k
        basin[on_cycle[x][0]] += 1

    # entropy per cycle, starting uniform over all states
    dist = Counter({s: 1 for s in states})
    H = [round(math.log2(len(states)), 3)]
    for _ in range(max(depth.values()) + 1):
        new = Counter()
        for s, c in dist.items():
            new[C[s]] += c
        dist = new
        H.append(round(entropy(dist), 3))

    dead = [cid for cid in cycles if is_dead(cid)]
    live = [cid for cid in cycles if not is_dead(cid)]
    return {
        "E": E,
        "rule": rule,
        "states": len(states),
        "bits_initial": H[0],
        "bits_after_cycle": H[1:],
        "bits_forgotten_total": round(H[0] - H[-1], 3),
        "attractors": len(cycles),
        "attractor_states": sum(cycles.values()),
        "periods": dict(Counter(cycles.values())),
        "dead_attractors": len(dead),
        "share_ending_dead": round(sum(basin[c] for c in dead) / len(states), 3),
        "live_attractors": len(live),
        "largest_basin": max(basin.values()),
        "longest_transient_cycles": max(depth.values()),
        "share_ending_live": round(sum(basin[c] for c in live) / len(states), 3),
        "example_live_orbit": (
            [[list(map(list, x)), list(map(list, aeon(x)))] for x in orbit(max(live, key=lambda c: basin[c]))]
            if live else None),
    }


if __name__ == "__main__":
    max_E = int(sys.argv[1]) if len(sys.argv) > 1 else 6
    rows = []
    for E in range(2, max_E + 1):
        for rule in RESEEDS:
            r = analyse(E, rule)
            rows.append(r)
            print(json.dumps(r), flush=True)
    with open(__file__.rsplit("/", 1)[0] + f"/ccc_crossover_E{max_E}.jsonl", "w") as f:
        for r in rows:
            f.write(json.dumps(r) + "\n")
