"""Line-for-line port of the cloud notebook "Increment Mismatch TV" (Phase 1).

Every event: enumerate ordered pairs (i1, i2) of distinct edge positions that
match the two-edge LHS injectively, score each by
  key = (max writer, min writer, sorted consumed edges)
(writer = id of the event that created the edge, -1 for initial edges), take
the lexicographically first key (stable, so ties keep enumeration order), and
record TV between the depth of the chosen event and the depth histogram of all
candidate matches ("mismatch" depths).

The writer lookup uses the whole edge as one key, which is the notebook with
its Lookup bug fixed (Lookup[edgeWriter, Key[#], -1]). Checked against the
fixed Wolfram code: identical TV at every event for n = 24.
Usage: python3 imtv.py [n]   (default 150; about 4 s)
"""
import sys
from collections import Counter


def tv_depth(rewrote, mismatch):
    if not rewrote or not mismatch:
        return None
    cr, cm = Counter(rewrote), Counter(mismatch)
    nr, nm = len(rewrote), len(mismatch)
    return 0.5 * sum(abs(cr[k] / nr - cm[k] / nm) for k in set(cr) | set(cm))


def match_pick2(edges, lhs, writer, event_depths):
    scored, mdepths = [], []
    nE = len(edges)
    for i1 in range(nE):
        for i2 in range(nE):
            if i1 == i2:
                continue
            m, ok = {}, True
            for pe, ce in ((lhs[0], edges[i1]), (lhs[1], edges[i2])):
                for j in range(len(pe)):
                    if pe[j] in m and m[pe[j]] != ce[j]:
                        ok = False
                    m[pe[j]] = ce[j]
            if ok and len(m.values()) != len(set(m.values())):
                ok = False
            if not ok:
                continue
            consumed = [tuple(m[v] for v in lhs[0]), tuple(m[v] for v in lhs[1])]
            writers = [writer.get(e, -1) for e in consumed]
            parents = sorted(set(w for w in writers if w >= 0))
            depth = 0 if not parents else 1 + max(event_depths[p] for p in parents)
            mdepths.append(depth)
            key = (max(writers), min(writers), tuple(sorted(consumed)))
            scored.append((key, m, consumed, depth, parents))
    if not scored:
        return None
    scored.sort(key=lambda s: s[0])  # stable, like SortBy
    return mdepths, scored[0]


def run_seq_tv(lhs, rhs, init, n):
    edges = [tuple(e) for e in init]
    writer = {e: -1 for e in edges}
    events, tv, mmn = [], {}, {}
    plhs = set(v for e in lhs for v in e)
    prhs = set(v for e in rhs for v in e)
    newp = sorted(prhs - plhs)
    for t in range(n):
        pack = match_pick2(edges, lhs, writer, events)
        if pack is None:
            break
        mdepths, (key, m, consumed, depth, parents) = pack
        eid = len(events)
        events.append(depth)
        tv[t] = tv_depth([depth], mdepths)
        mmn[t] = len(mdepths)
        remaining = list(edges)
        for c in consumed:
            remaining.remove(c)  # first occurrence, like DeleteCases[..., 1]
        maxv = max(v for e in edges for v in e)
        nm = dict(m)
        for p in newp:
            maxv += 1
            nm[p] = maxv
        added = [tuple(nm[v] for v in e) for e in rhs]
        for c in consumed:
            writer.pop(c, None)
        for a in added:
            writer[a] = eid
        edges = remaining + added
    return {"n": len(events), "tv": tv, "mmN": mmn}


X, Y, Z, W = "x", "y", "z", "w"
DIM = ([(X, Y), (X, Z)], [(X, Z), (X, W), (Y, W), (Z, W)], [(1, 2), (1, 3)])
CHAIN = ([(X, Y), (Y, Z)], [(W, Y), (Y, X), (X, W), (W, Z)], [(0, 1), (1, 2), (2, 3), (3, 0)])

if __name__ == "__main__":
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 150
    midT, largeT = (50, 149) if n == 150 else (n // 3, n - 1)
    d = run_seq_tv(*DIM, n)
    c = run_seq_tv(*CHAIN, n)
    if n != 150:
        print("dim_tv", [round(d["tv"][t], 6) for t in sorted(d["tv"])])
        print("chain_tv", [round(c["tv"][t], 6) for t in sorted(c["tv"])])
    shared = d["n"] > largeT and c["n"] > largeT
    tdM, tcM, tdL, tcL = d["tv"][midT], c["tv"][midT], d["tv"][largeT], c["tv"][largeT]
    held = shared and tdM < tcM and tdL < tcL
    print({"n": (d["n"], c["n"]), "mid": (midT, tdM, tcM), "large": (largeT, tdL, tcL), "held": held})
