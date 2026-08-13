"""Bounded consistency stress test for rigidity labels at a larger tier.

Usage: python stress_conjecture.py MAX_V MAX_E WORKERS OUTFILE

For every stage-1 survivor rule, recompute bounded history-ambiguity and R1
collision labels at the (MAX_V, MAX_E) tier. A bounded label conflict flags
the probe or implementation for investigation; it does not by itself refute
the exact theorem, whose hypotheses are unbounded. Incremental JSONL output
keeps partial runs usable. The legacy JSON key is retained for compatibility.
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
                print(f"!! BOUNDED LABEL CONFLICT: {rec['rule']}", flush=True)
            if rec.get("genuine"):
                new_colliders += 1
            if (i + 1) % 40 == 0:
                print(f"[stress {MAX_V},{MAX_E}] {i+1}/{len(rules)} "
                      f"({time.time()-t0:.0f}s)", flush=True)
    print(f"[stress {MAX_V},{MAX_E}] DONE {time.time()-t0:.0f}s: "
          f"colliding={new_colliders}, BOUNDED LABEL CONFLICTS={violations}",
          flush=True)


if __name__ == "__main__":
    main()
