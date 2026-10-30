"""CCC experiment: how much does the splice rule compress its own phase space?

Rule (flagship):  {(a,a),(b,c)} -> {(a,b),(c,a)}

Facts used:
  * vertex count and edge count are conserved, so each (V,E) sector is a
    finite closed "universe";
  * every application destroys exactly one loop (a,a) and creates none
    (b != c by injective matching), so every evolution halts within at most
    L steps, L = number of loops; it ends early only when the remaining
    loops are stranded (every non-loop edge touches every loop vertex).

Penrose's conformal cyclic cosmology needs the late universe to have
"forgotten" enough that its phase space is effectively smaller than the
early one's. The discrete analogue measured here:

  * terminal set   T(S) = terminal (match-free) states reachable from S
                   (multiway, all matches, no policy);
  * confluence     |T(S)| == 1 for every S means the end state is
                   policy-free ("heat death is unique");
  * compression    bits lost = H(S) - H(T(S)) for S uniform on a sector,
                   i.e. how much of the initial condition the final state
                   cannot recover.

Canonical forms use invariant-refined brute force (permute only within
vertex classes of equal (out, in, loop) degree), which is a valid canonical
form; because the measurement is policy-free, no comparison with
core.canonical's ordering is needed.
"""
import sys
import json
import math
from collections import Counter, defaultdict
from functools import lru_cache
from itertools import permutations, product

sys.path.insert(0, __file__.rsplit("/", 1)[0])
from core import matches, apply_rule  # noqa: E402

SPLICE = ((("a", "a"), ("b", "c")), (("a", "b"), ("c", "a")))


def _classes(state):
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
    return [groups[k] for k in sorted(groups)]


@lru_cache(maxsize=1 << 22)
def canon(state):
    if not state:
        return ()
    classes = _classes(state)
    best = None
    offsets, o = [], 0
    for c in classes:
        offsets.append(o)
        o += len(c)
    for perms in product(*[permutations(c) for c in classes]):
        mapping = {}
        for off, p in zip(offsets, perms):
            for i, v in enumerate(p):
                mapping[v] = off + i
        cand = tuple(sorted((mapping[x], mapping[y]) for x, y in state))
        if best is None or cand < best:
            best = cand
    return best


def succ(state):
    return {canon(apply_rule(state, SPLICE, m)) for m in matches(state, SPLICE)}


def all_states(max_e):
    """All canonical states (binary edges, loops and multi-edges allowed),
    grouped by edge count, by single-edge augmentation."""
    layers = {0: {()}}
    for e in range(1, max_e + 1):
        nxt = set()
        for s in layers[e - 1]:
            n = len({v for ed in s for v in ed})
            pool = range(n + 2)
            for x in pool:
                for y in pool:
                    t = tuple(sorted(s + ((x, y),)))
                    # relabel to contiguous vertices
                    vs = sorted({v for ed in t for v in ed})
                    mp = {v: i for i, v in enumerate(vs)}
                    t = tuple(sorted((mp[a], mp[b]) for a, b in t))
                    nxt.add(canon(t))
        layers[e] = nxt
    return layers


@lru_cache(maxsize=None)
def terminals(state):
    nxt = succ(state)
    if not nxt:
        return frozenset([state])
    out = set()
    for t in nxt:
        out |= terminals(t)
    return frozenset(out)


def loops(s):
    return sum(1 for x, y in s if x == y)


def nverts(s):
    return len({v for e in s for v in e})


def entropy_bits(counts):
    tot = sum(counts)
    return -sum(c / tot * math.log2(c / tot) for c in counts if c)


def main(max_e):
    layers = all_states(max_e)
    rows = []
    for e in range(1, max_e + 1):
        sectors = defaultdict(list)
        for s in layers[e]:
            sectors[nverts(s)].append(s)
        for v in sorted(sectors):
            states = sectors[v]
            n = len(states)
            nonconf = 0
            fiber = Counter()
            for s in states:
                ts = terminals(s)
                if len(ts) != 1:
                    nonconf += 1
                    continue
                fiber[next(iter(ts))] += 1
            # states that halt immediately (loop-free) are their own terminal
            n_conf = n - nonconf
            h_init = math.log2(n_conf) if n_conf else 0.0
            h_term = entropy_bits(list(fiber.values())) if fiber else 0.0
            maxfiber = max(fiber.values()) if fiber else 0
            # restrict to states that actually evolve (>=1 loop)
            active = [s for s in states if loops(s) > 0 and len(terminals(s)) == 1]
            fa = Counter(next(iter(terminals(s))) for s in active)
            row = dict(
                E=e, V=v, states=n, nonconfluent=nonconf,
                terminals=len(fiber), max_fiber=maxfiber,
                bits_initial=round(h_init, 3), bits_terminal=round(h_term, 3),
                bits_lost=round(h_init - h_term, 3),
                active=len(active), active_terminals=len(fa),
                active_bits_lost=round(
                    (math.log2(len(active)) - entropy_bits(list(fa.values())))
                    if active else 0.0, 3),
            )
            rows.append(row)
            print(json.dumps(row), flush=True)
    return rows


if __name__ == "__main__":
    max_e = int(sys.argv[1]) if len(sys.argv) > 1 else 4
    rows = main(max_e)
    out = __file__.rsplit("/", 1)[0] + f"/ccc_compression_E{max_e}.jsonl"
    with open(out, "w") as f:
        for r in rows:
            f.write(json.dumps(r) + "\n")
