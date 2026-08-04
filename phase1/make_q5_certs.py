"""Generate R1-collision certificates for the Q5 strata (searcher-side).

- 7 min-successor collisions at the (5,5) census (from q5_deep_5_5.jsonl)
- 7 max-successor collisions at the (4,4) census (recomputed here)

Every certificate carries the policy, the tier, and the independence
bounds under which the pair was quarantined; verify_independent.py
rechecks all of it from scratch with its own engine.
"""
import json

from core import canonical, successors
from search import enumerate_states, reachable

BOUNDS = {"max_states": 2000, "max_verts": 7}


def cert(rule, s1, s2, image, policy, tier, note):
    return {
        "kind": "R1-collision",
        "policy": policy,
        "tier": tier,
        "rules": [[[list(e) for e in side] for side in rule]],
        "state1": [list(e) for e in s1],
        "state2": [list(e) for e in s2],
        "claimed_image": [list(e) for e in image],
        "independence_bounds": dict(BOUNDS),
        "note": note,
    }


def main():
    made = []

    # --- stratum 1: min-policy collisions at (5,5), from the deep hunt ---
    for line in open("q5_deep_5_5.jsonl"):
        r = json.loads(line)
        if r.get("status") != "ok" or not r.get("genuine"):
            continue
        rule = tuple(tuple(tuple(e) for e in side) for side in r["rule"])
        ex = r["example"]
        s1, s2 = (tuple(tuple(e) for e in st) for st in ex["preimages"][:2])
        img = tuple(tuple(e) for e in ex["image"])
        assert not reachable(s1, s2, [rule], **{
            "max_states": BOUNDS["max_states"], "max_verts": BOUNDS["max_verts"]})
        assert not reachable(s2, s1, [rule], **{
            "max_states": BOUNDS["max_states"], "max_verts": BOUNDS["max_verts"]})
        made.append(cert(rule, s1, s2, img, "min-successor", [5, 5],
                         "Q5 stratum 1: 2->2 frontier rule, census-bound "
                         "artifact resolved at (5,5); pair INDEPENDENT "
                         "within stated bounds"))

    # --- strata 1-2: max-policy collisions at (4,4), recomputed ---
    states = enumerate_states(4, 4)
    for line in open("ia_frontier_5_4.jsonl"):
        r = json.loads(line)
        if r.get("status") != "ok":
            continue
        rule = tuple(tuple(tuple(e) for e in side) for side in r["rule"])
        table = {}
        for s in states:
            succ = successors(s, [rule])
            if succ:
                table.setdefault(max(succ), []).append(s)
        found = None
        for img, pre in sorted(table.items()):
            if len(pre) < 2:
                continue
            core_pre = []
            for s in pre:
                if any(reachable(s, t, [rule]) and reachable(t, s, [rule])
                       for t in core_pre):
                    continue
                core_pre.append(s)
            # keep only a mutually-unreachable pair (INDEPENDENT, not
            # DOWNSTREAM): recheck one-way too
            for i in range(len(core_pre)):
                for j in range(i + 1, len(core_pre)):
                    a, b = core_pre[i], core_pre[j]
                    if not reachable(a, b, [rule]) and \
                       not reachable(b, a, [rule]):
                        found = (a, b, img)
                        break
                if found:
                    break
            if found:
                break
        if found:
            s1, s2, img = found
            made.append(cert(rule, s1, s2, tuple(tuple(e) for e in img),
                             "max-successor", [4, 4],
                             "Q5 policy-relativity: genuine collision under "
                             "the max-successor canonical policy; pair "
                             "INDEPENDENT within stated bounds"))

    for i, c in enumerate(made):
        pol = "min55" if c["policy"] == "min-successor" else "max44"
        path = f"q5cert_{pol}_{i:02d}.json"
        with open(path, "w") as f:
            json.dump(c, f, indent=1)
        print("wrote", path)
    print(f"total: {len(made)} certificates")


if __name__ == "__main__":
    main()
