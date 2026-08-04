"""Stress the two-rule hard core (fresh-vertex pendant growers) at richer
censuses under BOTH canonical policies. Any genuine INDEPENDENT collision
refutes the pendant coherence conjecture (Q5_NOTES.md §5).

Usage: python q5_core_stress.py MAX_V MAX_E OUTFILE
"""
import json
import sys
import time
from concurrent.futures import ProcessPoolExecutor, as_completed

CORE = [
    [[["v0", "v1"]], [["v0", "v1"], ["v1", "v2"]]],
    [[["v0", "v1"]], [["v0", "v1"], ["v2", "v0"]]],
]


def work(args):
    rule_l, maxv, maxe, polname = args
    from core import successors
    from search import enumerate_states, reachable
    pick = min if polname == "min" else max
    rule = tuple(tuple(tuple(e) for e in side) for side in rule_l)
    rec = {"rule": rule_l, "tier": [maxv, maxe], "policy": polname}
    try:
        t0 = time.time()
        states = enumerate_states(maxv, maxe)
        table = {}
        for s in states:
            succ = successors(s, [rule])
            if succ:
                table.setdefault(pick(succ), []).append(s)
        indep = 0
        example = None
        for img, pre in table.items():
            if len(pre) < 2:
                continue
            for i in range(len(pre)):
                for j in range(i + 1, len(pre)):
                    a, b = pre[i], pre[j]
                    if not reachable(a, b, [rule]) and \
                       not reachable(b, a, [rule]):
                        indep += 1
                        if example is None:
                            example = {"image": [list(e) for e in img],
                                       "s1": [list(e) for e in a],
                                       "s2": [list(e) for e in b]}
        rec.update(status="ok", census=len(states), independent_collisions=indep,
                   example=example, secs=round(time.time() - t0, 1))
    except Exception as e:
        rec["status"] = f"error:{e!r}"
    return rec


def main():
    maxv, maxe, outfile = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3]
    jobs = [(r, maxv, maxe, p) for r in CORE for p in ("min", "max")]
    print(f"[corestress {maxv},{maxe}] {len(jobs)} jobs", flush=True)
    with open(outfile, "w") as log, ProcessPoolExecutor(4) as ex:
        futs = [ex.submit(work, j) for j in jobs]
        for fut in as_completed(futs):
            rec = fut.result()
            log.write(json.dumps(rec) + "\n")
            log.flush()
            tag = ("!! REFUTED" if rec.get("independent_collisions")
                   else "coherent")
            print(f"[corestress] {rec['rule']} {rec['policy']}: {tag} "
                  f"({rec.get('secs','?')}s)", flush=True)


if __name__ == "__main__":
    main()
