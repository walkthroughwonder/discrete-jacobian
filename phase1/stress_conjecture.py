"""Rigidity Conjecture stress test at a larger probe tier.

Usage: python stress_conjecture.py MAX_V MAX_E WORKERS OUTFILE

For every stage-1 survivor rule: recompute history ambiguity and R1
collisions at the (MAX_V, MAX_E) tier. The conjecture dies if any rule is
UNAMBIGUOUS (at this tier) yet COLLIDES (at this tier). Incremental JSONL
output so partial runs are usable.
"""
import json
import sys
import time
from concurrent.futures import ProcessPoolExecutor, as_completed

MAX_V, MAX_E, WORKERS, OUTFILE = (int(sys.argv[1]), int(sys.argv[2]),
                                  int(sys.argv[3]), sys.argv[4])

_probes = None

def get_probes():
    global _probes
    if _probes is None:
        from search import enumerate_states
        _probes = enumerate_states(MAX_V, MAX_E)
    return _probes


def work(rule_l):
    from analysis_n4n5 import history_ambiguity
    from search import find_r1_collisions
    rule = tuple(tuple(tuple(e) for e in side) for side in rule_l)
    rec = {"rule": rule_l, "tier": [MAX_V, MAX_E]}
    try:
        t0 = time.time()
        amb = history_ambiguity(rule, get_probes())
        _, genuine, artifacts = find_r1_collisions([rule], MAX_V, MAX_E)
        rec.update(status="ok", ambiguous=amb, genuine=len(genuine),
                   artifacts=len(artifacts), secs=round(time.time() - t0, 1))
        if genuine and not amb:
            rec["CONJECTURE_VIOLATION"] = True
    except Exception as e:
        rec["status"] = f"error:{e}"
    return rec


def main():
    rules = []
    for line in open("maxsweep_log.jsonl"):
        r = json.loads(line)
        if r.get("stage") == 1 and r.get("status") == "swept":
            rules.append(r["rule"])
    print(f"[stress {MAX_V},{MAX_E}] {len(rules)} rules, {WORKERS} workers",
          flush=True)
    t0 = time.time()
    violations = new_colliders = 0
    with open(OUTFILE, "w") as log, ProcessPoolExecutor(WORKERS) as ex:
        futs = [ex.submit(work, r) for r in rules]
        for i, fut in enumerate(as_completed(futs)):
            rec = fut.result()
            log.write(json.dumps(rec) + "\n")
            log.flush()
            if rec.get("CONJECTURE_VIOLATION"):
                violations += 1
                print(f"!! VIOLATION: {rec['rule']}", flush=True)
            if rec.get("genuine"):
                new_colliders += 1
            if (i + 1) % 40 == 0:
                print(f"[stress {MAX_V},{MAX_E}] {i+1}/{len(rules)} "
                      f"({time.time()-t0:.0f}s)", flush=True)
    print(f"[stress {MAX_V},{MAX_E}] DONE {time.time()-t0:.0f}s: "
          f"colliding={new_colliders}, CONJECTURE VIOLATIONS={violations}",
          flush=True)


if __name__ == "__main__":
    main()
