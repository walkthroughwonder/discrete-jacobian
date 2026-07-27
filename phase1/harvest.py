"""Harvest INDEPENDENT collision candidates from maxsweep_log.jsonl:
re-verify mutual unreachability at much larger bounds, emit certificates,
and report the strongest candidates (count-preserving first)."""
import json

from search import reachable, certificate
from core import canonical


def load_stage1_hits():
    hits = []
    for line in open("maxsweep_log.jsonl"):
        rec = json.loads(line)
        if rec.get("stage") == 1 and rec.get("independent", 0) > 0:
            hits.append(rec)
    return hits


def as_rule(r):
    return tuple(tuple(tuple(e) for e in side) for side in r)


def main():
    hits = load_stage1_hits()
    print(f"{len(hits)} stage-1 rules with INDEPENDENT pairs")

    scored = []
    for rec in hits:
        rule = as_rule(rec["rule"])
        lhs, rhs = rule
        count_preserving = len(lhs) == len(rhs)
        indep_pairs = [p for p in rec["pairs"] if p["kind"] == "INDEPENDENT"]
        for p in indep_pairs:
            scored.append((not count_preserving, rule, p))  # count-preserving first
    scored.sort(key=lambda x: x[0])
    print(f"{len(scored)} INDEPENDENT pairs total; "
          f"{sum(1 for cp, _, _ in scored if not cp)} from count-preserving rules")

    confirmed = []
    for i, (noncp, rule, p) in enumerate(scored[:12]):
        s = tuple(tuple(e) for e in p["s"])
        t = tuple(tuple(e) for e in p["t"])
        img = tuple(tuple(e) for e in p["image"])
        # hard reachability recheck: 10x states, higher vertex cap
        st = reachable(s, t, [rule], max_states=5000, max_verts=8)
        ts = reachable(t, s, [rule], max_states=5000, max_verts=8)
        tag = "count-preserving" if not noncp else "count-changing"
        if st or ts:
            print(f"[{i}] DEMOTED to downstream at larger bounds ({tag}) {rule}")
            continue
        cert = certificate([rule], s, t, img)
        cert["reachability"] = {"s_to_t": False, "t_to_s": False,
                               "bounds": {"max_states": 5000, "max_verts": 8}}
        path = f"cert_{i}.json"
        json.dump(cert, open(path, "w"), indent=1)
        confirmed.append((path, tag, rule, s, t, img))
        print(f"[{i}] CANDIDATE ({tag}) cert={path}")
        print(f"     rule {rule}")
        print(f"     {s}  vs  {t}  ->  {img}")
    print(f"\n{len(confirmed)} candidates confirmed at large bounds; "
          f"certificates written")


if __name__ == "__main__":
    main()
