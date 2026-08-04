"""Targeted falsification of MIN-coherence for the pendant growers via
decoration enumeration (complete per core class by Lemma B).

By core conservation, any f_min collision pair shares a core; by strict
edge growth, same-edge-count pairs are automatically mutually
unreachable (INDEPENDENT). So enumerating all pendant decorations of
each small core and comparing f_min within (core, |E|) buckets is a
COMPLETE search of that stratum — no global census needed, reaching
state sizes (6V, 7E) beyond every census swept so far.

Usage: python q5_min_decoration.py OUTFILE
"""
import json
import sys
import time
from concurrent.futures import ProcessPoolExecutor, as_completed

from core import canonical, successors
from search import enumerate_states

PEND_OUT = ((("v0", "v1"),), (("v0", "v1"), ("v1", "v2")))
PEND_IN = ((("v0", "v1"),), (("v0", "v1"), ("v2", "v0")))

# decoration edge budget by core vertex count; the vertex guard in
# decoration_layers independently caps |V| <= 6 so successor canonical
# forms live on <= 7 vertices
BUDGET = {0: 6, 1: 5, 2: 4, 3: 4, 4: 3}


def strip_core(state):
    edges = list(state)
    changed = True
    while changed:
        changed = False
        for i, (v, w) in enumerate(edges):
            indeg = sum(1 for e in edges if e[1] == w)
            outdeg = sum(1 for e in edges if e[0] == w)
            if outdeg == 0 and indeg == 1 and v != w:
                edges.pop(i)
                changed = True
                break
    return canonical(tuple(edges))


MAX_VERTS = 6  # successor canonical forms then live on <= 7 vertices


def decoration_layers(core_state, kmax):
    """Canonical states obtainable by adding k <= kmax pendant leaf edges:
    either (v, fresh) attached at any existing vertex (chaining allowed),
    or (fresh_root, fresh_leaf) starting a new DISCONNECTED tree — both
    strip back to the same core, so this is complete for the core class
    within the vertex guard. Yields (k, layer_of_canonical_states)."""
    layer = {canonical(core_state)}
    yield 0, layer
    for k in range(1, kmax + 1):
        nxt = set()
        for s in layer:
            vs = sorted({v for e in s for v in e})
            fresh = (max(vs) + 1) if vs else 0
            nv = len(vs)
            if nv + 1 <= MAX_VERTS:
                for v in vs:
                    nxt.add(canonical(tuple(s) + ((v, fresh),)))
            if nv + 2 <= MAX_VERTS:
                nxt.add(canonical(tuple(s) + ((fresh, fresh + 1),)))
        layer = nxt
        yield k, layer


def work(args):
    core_l, rule_name = args
    rule = PEND_OUT if rule_name == "out" else PEND_IN
    core_state = tuple(tuple(e) for e in core_l)
    nverts = len({v for e in core_state for v in e})
    kmax = BUDGET.get(nverts, 0)
    rec = {"core": core_l, "rule": rule_name, "kmax": kmax}
    try:
        t0 = time.time()
        checked = 0
        collisions = []
        for k, layer in decoration_layers(core_state, kmax):
            table = {}
            for s in layer:
                # mirror rule: decorations for PEND_IN attach source-leafs;
                # reuse the same layer only for PEND_OUT. For PEND_IN,
                # reverse every state (edge-reversal duality maps the rule
                # to PEND_OUT and commutes with matching/application, but
                # NOT with canonical order - so recompute f_min directly
                # on the reversed state under PEND_IN).
                st = s if rule_name == "out" else canonical(
                    tuple((b, a) for (a, b) in s))
                succ = successors(st, [rule])
                if succ:
                    table.setdefault(min(succ), []).append(st)
                checked += 1
            for img, pre in table.items():
                pre = sorted(set(pre))
                if len(pre) >= 2:
                    collisions.append({"image": [list(e) for e in img],
                                       "preimages": [[list(e) for e in s]
                                                     for s in pre[:3]],
                                       "k": k})
        rec.update(status="ok", checked=checked,
                   collisions=len(collisions),
                   examples=collisions[:2],
                   secs=round(time.time() - t0, 1))
    except Exception as e:
        rec["status"] = f"error:{e!r}"
    return rec


def main():
    outfile = sys.argv[1]
    cores = [()]  # the empty core (pure forests)
    for s in enumerate_states(4, 4):
        if strip_core(s) == canonical(s):
            cores.append(s)
    jobs = [(list(list(e) for e in c), rn)
            for c in cores for rn in ("out", "in")]
    print(f"[mindec] {len(cores)} cores x 2 rules = {len(jobs)} jobs",
          flush=True)
    t0 = time.time()
    total_coll = 0
    with open(outfile, "w") as log, ProcessPoolExecutor(14) as ex:
        futs = [ex.submit(work, j) for j in jobs]
        for i, fut in enumerate(as_completed(futs)):
            rec = fut.result()
            log.write(json.dumps(rec) + "\n")
            log.flush()
            if rec.get("collisions"):
                total_coll += rec["collisions"]
                print(f"!! MIN-COHERENCE REFUTED at core {rec['core']} "
                      f"({rec['rule']}): {rec['collisions']} collisions",
                      flush=True)
            if (i + 1) % 40 == 0:
                print(f"[mindec] {i+1}/{len(jobs)} ({time.time()-t0:.0f}s)",
                      flush=True)
    print(f"[mindec] DONE {time.time()-t0:.0f}s: "
          f"total collisions={total_coll}", flush=True)


if __name__ == "__main__":
    main()
