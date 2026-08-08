"""Phase 2 sweep: enumerate small D1 rules, filter by semantic D1, search for
R1 collisions, classify each collision pair as INDEPENDENT (neither state
reachable from the other — the strong, Jacobian-shaped class) or DOWNSTREAM
(one-way reachable). Logs every rule's outcome to sweep_log.jsonl.

Scope of this sweep (documented, per no-silent-caps):
  - single-rule systems only
  - LHS: 1 binary edge over {x,y}, or 2 binary edges over <=3 vars
  - RHS: 1..2 binary edges; vars(LHS) subset of vars(RHS); at most one fresh
    var (single-edge LHS only)
  - probe/search space: states with <=4 vertices, <=3 edges
Claims are 'in range' only.
"""
import sys
import os
import json
from itertools import product

from core import canonical, is_d1, semantic_d1_violation
from search import enumerate_states, find_r1_collisions, reachable


def canon_rule(rule):
    """Cheap rule dedup: canonical renaming of variables by first appearance."""
    lhs, rhs = rule
    order = []
    for e in lhs + rhs:
        for v in e:
            if v not in order:
                order.append(v)
    ren = {v: f"v{i}" for i, v in enumerate(order)}
    return (tuple(sorted(tuple(ren[v] for v in e) for e in lhs)),
            tuple(sorted(tuple(ren[v] for v in e) for e in rhs)))


def enumerate_rules():
    rules = set()
    # class A: LHS = one edge over {x,y}
    lhs_a = [(("x", "y"),)]
    vars_a = ["x", "y", "z"]  # z fresh allowed
    edges_a = list(product(vars_a, repeat=2))
    for lhs in lhs_a:
        for n in (1, 2):
            for combo in product(edges_a, repeat=n):
                rhs = tuple(sorted(combo))
                rules.add(canon_rule((lhs, rhs)))
    # class B: LHS = two edges over <=3 vars, RHS over exactly LHS vars
    vars_b = ["x", "y", "z"]
    edges_b = list(product(vars_b, repeat=2))
    lhs_bs = set()
    for e1 in edges_b:
        for e2 in edges_b:
            lhs_bs.add(tuple(sorted((e1, e2))))
    for lhs in lhs_bs:
        lv = {v for e in lhs for v in e}
        redges = [e for e in edges_b if set(e) <= lv]
        for n in (1, 2):
            for combo in product(redges, repeat=n):
                rhs = tuple(sorted(combo))
                if lv <= {v for e in rhs for v in e}:
                    rules.add(canon_rule((lhs, rhs)))
    return sorted(rules)


def is_identity_like(rule, probes):
    """Every application maps S to canonical(S)."""
    from core import matches, apply_rule
    for s in probes:
        for m in matches(s, rule):
            if canonical(apply_rule(s, rule, m)) != canonical(s):
                return False
    return True


def classify_pairs(genuine, rules):
    out = []
    for img, pre in genuine.items():
        for i in range(len(pre)):
            for j in range(i + 1, len(pre)):
                s, t = pre[i], pre[j]
                st = reachable(s, t, rules)
                ts = reachable(t, s, rules)
                kind = "INDEPENDENT" if not (st or ts) else "DOWNSTREAM"
                out.append({"image": img, "s": s, "t": t, "kind": kind})
    return out


def open_evidence_log(default_path):
    """Open a log for writing without ever silently destroying evidence.

    This path is committed evidence and the README tells the reader to run
    this script, which used to open it with "w". --out PATH writes where you
    say; otherwise an existing default sends this run to a .rerun sibling.
    --force is the only way to overwrite.
    """
    argv = sys.argv
    path = argv[argv.index("--out") + 1] if "--out" in argv else default_path
    if os.path.exists(path) and "--force" not in argv:
        if "--out" in argv:
            sys.exit(f"refusing to overwrite {path} (pass --force if you mean it)")
        stem, ext = os.path.splitext(default_path)
        path = f"{stem}.rerun{ext}"
        print(f"[log] {default_path} exists and is committed evidence; "
              f"writing this run to {path} instead.", flush=True)
    return open(path, "w")


def main():
    probes = enumerate_states(4, 3)
    all_rules = enumerate_rules()
    print(f"enumerated {len(all_rules)} candidate rules; probing D1...")

    log = open_evidence_log("sweep_log.jsonl")
    stats = {"rules": len(all_rules), "syntactic_d1": 0, "semantic_d1": 0,
             "identity_skipped": 0, "colliding": 0, "independent_pairs": 0}
    finds = []
    for k, rule in enumerate(all_rules):
        rec = {"rule": rule}
        if not is_d1(rule):
            rec["status"] = "not-syntactic-d1"
            log.write(json.dumps(rec) + "\n")
            continue
        stats["syntactic_d1"] += 1
        if any(semantic_d1_violation(s, rule) for s in probes):
            rec["status"] = "not-semantic-d1"
            log.write(json.dumps(rec) + "\n")
            continue
        stats["semantic_d1"] += 1
        if is_identity_like(rule, probes):
            stats["identity_skipped"] += 1
            rec["status"] = "identity-like"
            log.write(json.dumps(rec) + "\n")
            continue
        _, genuine, artifacts = find_r1_collisions([rule], 4, 3)
        pairs = classify_pairs(genuine, [rule]) if genuine else []
        indep = [p for p in pairs if p["kind"] == "INDEPENDENT"]
        rec["status"] = "swept"
        rec["genuine_images"] = len(genuine)
        rec["independent_pairs"] = len(indep)
        rec["downstream_pairs"] = len(pairs) - len(indep)
        log.write(json.dumps(rec) + "\n")
        if genuine:
            stats["colliding"] += 1
            stats["independent_pairs"] += len(indep)
            finds.append((rule, pairs))
        if (k + 1) % 50 == 0:
            print(f"  ...{k + 1}/{len(all_rules)} rules")
    log.close()

    print("\n=== SWEEP SUMMARY ===")
    for k2, v in stats.items():
        print(f"  {k2}: {v}")
    print("\n=== SEMANTIC-D1 SYSTEMS WITH GENUINE COLLISIONS ===")
    for rule, pairs in finds:
        indep = [p for p in pairs if p["kind"] == "INDEPENDENT"]
        print(f"rule {rule}: {len(indep)} independent, "
              f"{len(pairs) - len(indep)} downstream")
        for p in indep[:2]:
            print(f"   INDEPENDENT: {p['s']}  vs  {p['t']}  ->  {p['image']}")


if __name__ == "__main__":
    main()
