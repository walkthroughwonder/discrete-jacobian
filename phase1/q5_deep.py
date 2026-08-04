"""Q5 falsification hunt: deep-census F-injectivity check for the 12
D-IA frontier rules. For edge-growing rules mutual reachability is
impossible (edge count strictly increases), so ANY genuine f_min
collision here answers Q5 negatively; sustained dryness supports the
policy-coherence conjecture (Q5_NOTES.md).

Usage: python q5_deep.py MAX_V MAX_E WORKERS OUTFILE [--growers-only]
"""
import json
import sys
import time
from concurrent.futures import ProcessPoolExecutor, as_completed


def work(args):
    rule_l, maxv, maxe = args
    from search import find_r1_collisions
    rule = tuple(tuple(tuple(e) for e in side) for side in rule_l)
    rec = {"rule": rule_l, "tier": [maxv, maxe]}
    try:
        t0 = time.time()
        states, genuine, artifacts = find_r1_collisions([rule], maxv, maxe)
        rec.update(status="ok", census=len(states), genuine=len(genuine),
                   artifacts=len(artifacts), secs=round(time.time() - t0, 1))
        if genuine:
            img, pre = sorted(genuine.items())[0]
            rec["example"] = {"image": [list(e) for e in img],
                              "preimages": [[list(e) for e in s] for s in pre[:3]]}
    except Exception as e:
        rec["status"] = f"error:{e!r}"
    return rec


def main():
    maxv, maxe, workers, outfile = (int(sys.argv[1]), int(sys.argv[2]),
                                    int(sys.argv[3]), sys.argv[4])
    growers_only = "--growers-only" in sys.argv
    rules = []
    for line in open("ia_frontier_5_4.jsonl"):
        r = json.loads(line)
        if r.get("status") != "ok":
            continue
        if growers_only and len(r["rule"][0]) != 1:
            continue
        rules.append(r["rule"])
    print(f"[q5deep {maxv},{maxe}] {len(rules)} rules, {workers} workers",
          flush=True)
    t0 = time.time()
    hits = 0
    with open(outfile, "w") as log, ProcessPoolExecutor(workers) as ex:
        futs = [ex.submit(work, (r, maxv, maxe)) for r in rules]
        for i, fut in enumerate(as_completed(futs)):
            rec = fut.result()
            log.write(json.dumps(rec) + "\n")
            log.flush()
            if rec.get("genuine"):
                hits += 1
                print(f"!! Q5 BREAK: {rec['rule']}", flush=True)
            print(f"[q5deep] {i+1}/{len(rules)} ({time.time()-t0:.0f}s)",
                  flush=True)
    print(f"[q5deep {maxv},{maxe}] DONE {time.time()-t0:.0f}s: "
          f"{hits}/{len(rules)} rules collide", flush=True)


if __name__ == "__main__":
    main()
