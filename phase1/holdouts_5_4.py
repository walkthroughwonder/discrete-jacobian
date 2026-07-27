"""Press the dichotomy: run the (4,4)-ambiguous-but-rigid holdout rules at
the richer (5v,4e) tier. Strong-form conjecture predicts they collide."""
import json
import time
from concurrent.futures import ProcessPoolExecutor, as_completed


def work(rule_l):
    from search import find_r1_collisions
    rule = tuple(tuple(tuple(e) for e in side) for side in rule_l)
    rec = {"rule": rule_l, "tier": [5, 4]}
    try:
        t0 = time.time()
        _, genuine, artifacts = find_r1_collisions([rule], 5, 4)
        rec.update(status="ok", genuine=len(genuine), artifacts=len(artifacts),
                   secs=round(time.time() - t0, 1))
    except Exception as e:
        rec["status"] = f"error:{e}"
    return rec


def main():
    holdouts = []
    for line in open("stress_4_4.jsonl"):
        r = json.loads(line)
        if r.get("status") == "ok" and r["ambiguous"] and not r["genuine"]:
            holdouts.append(r["rule"])
    print(f"[holdouts] {len(holdouts)} ambiguous-but-rigid rules at (5,4)",
          flush=True)
    t0 = time.time()
    newly = 0
    with open("holdouts_5_4.jsonl", "w") as log, \
         ProcessPoolExecutor(14) as ex:
        futs = [ex.submit(work, r) for r in holdouts]
        for i, fut in enumerate(as_completed(futs)):
            rec = fut.result()
            log.write(json.dumps(rec) + "\n")
            log.flush()
            if rec.get("genuine"):
                newly += 1
            if (i + 1) % 10 == 0:
                print(f"[holdouts] {i+1}/{len(holdouts)} "
                      f"({time.time()-t0:.0f}s)", flush=True)
    print(f"[holdouts] DONE {time.time()-t0:.0f}s: "
          f"{newly}/{len(holdouts)} newly collide at (5,4)", flush=True)


if __name__ == "__main__":
    main()
