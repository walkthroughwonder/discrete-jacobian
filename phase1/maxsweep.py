"""MAX-POWER Phase 2 sweep. Three stages, multiprocess (14 workers).

  Stage 1 (singles): all rules in classes A (1-edge LHS, RHS<=2 edges,
    <=1 fresh var), B (2-edge LHS, RHS<=2 edges over LHS vars), and
    B+ (2-edge LHS, RHS<=2 edges, exactly 1 fresh var). Gates: syntactic D1,
    semantic-D1 probe (all states <=4v <=3e), non-identity. Survivors
    swept for R1 collisions at (4v,3e); colliding rules re-confirmed at
    (5v,4e) restricted probe. Pairs classified INDEPENDENT / DOWNSTREAM.
  Stage 2 (pairs): all unordered pairs of up to 60 stage-1 survivors,
    same sweep at (4v,3e).
  Stage 3 (R2): for up to 40 systems, forward multiway BFS from every seed
    (<=4v,<=3e; depth<=3, <=300 states/seed, vertex cap 6); an R2 merge
    record uses seeds classified mutually unreachable by the bounded
    reachability screen and intersecting forward sets.

All bounds are explicit above (no silent caps). Log: maxsweep_log.jsonl.
"""
import json
import sys
import time
from concurrent.futures import ProcessPoolExecutor, as_completed
from itertools import combinations, product

from core import canonical, is_d1, matches, apply_rule, semantic_d1_violation, successors
from search import enumerate_states, find_r1_collisions, reachable


# ---------- rule enumeration ----------

def canon_rule(rule):
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
    edges3 = list(product(["x", "y", "z"], repeat=2))
    # class A
    for n in (1, 2):
        for combo in product(edges3, repeat=n):
            rules.add(canon_rule(((("x", "y"),), tuple(sorted(combo)))))
    # classes B and B+
    lhs_bs = {tuple(sorted((e1, e2))) for e1 in edges3 for e2 in edges3}
    edges4 = list(product(["x", "y", "z", "w"], repeat=2))
    for lhs in lhs_bs:
        lv = {v for e in lhs for v in e}
        for n in (1, 2):
            for combo in product(edges4, repeat=n):
                rhs = tuple(sorted(combo))
                rv = {v for e in rhs for v in e}
                fresh = rv - {"x", "y", "z"}
                if lv <= rv and len(fresh) <= 1 and (not fresh or "w" in fresh):
                    rules.add(canon_rule((lhs, rhs)))
    return sorted(rules)


# ---------- shared probes (computed per worker on demand) ----------

_PROBES = None

def probes():
    global _PROBES
    if _PROBES is None:
        _PROBES = enumerate_states(4, 3)
    return _PROBES


def is_identity_like(rule):
    for s in probes():
        for m in matches(s, rule):
            if canonical(apply_rule(s, rule, m)) != canonical(s):
                return False
    return True


def classify_pairs(genuine, rules):
    out = []
    for img, pre in genuine.items():
        for s, t in combinations(pre, 2):
            st = reachable(s, t, rules, max_states=500)
            ts = reachable(t, s, rules, max_states=500)
            kind = "INDEPENDENT" if not (st or ts) else "DOWNSTREAM"
            out.append({"image": img, "s": s, "t": t, "kind": kind})
    return out


# ---------- stage workers ----------

def work_single(rule):
    rec = {"stage": 1, "rule": rule}
    try:
        if not is_d1(rule):
            rec["status"] = "not-syntactic-d1"
            return rec
        if any(semantic_d1_violation(s, rule) for s in probes()):
            rec["status"] = "not-semantic-d1"
            return rec
        if is_identity_like(rule):
            rec["status"] = "identity-like"
            return rec
        _, genuine, artifacts = find_r1_collisions([rule], 4, 3)
        pairs = classify_pairs(genuine, [rule]) if genuine else []
        rec.update(status="swept", genuine=len(genuine), artifacts=len(artifacts),
                   independent=sum(p["kind"] == "INDEPENDENT" for p in pairs),
                   downstream=sum(p["kind"] == "DOWNSTREAM" for p in pairs),
                   pairs=pairs[:6])
    except Exception as e:  # keep the sweep alive
        rec["status"] = f"error:{e}"
    return rec


def work_pair(rulepair):
    rec = {"stage": 2, "rules": list(rulepair)}
    try:
        _, genuine, artifacts = find_r1_collisions(list(rulepair), 4, 3)
        pairs = classify_pairs(genuine, list(rulepair)) if genuine else []
        rec.update(status="swept", genuine=len(genuine), artifacts=len(artifacts),
                   independent=sum(p["kind"] == "INDEPENDENT" for p in pairs),
                   downstream=sum(p["kind"] == "DOWNSTREAM" for p in pairs),
                   pairs=pairs[:6])
    except Exception as e:
        rec["status"] = f"error:{e}"
    return rec


def forward_set(seed, rules, depth=3, cap=300, max_verts=6):
    seen = {seed}
    frontier = [seed]
    for _ in range(depth):
        nxt = []
        for s in frontier:
            if len({v for e in s for v in e}) > max_verts:
                continue
            for t in successors(s, rules):
                if t not in seen and len(seen) < cap:
                    seen.add(t)
                    nxt.append(t)
        frontier = nxt
    return seen


def work_r2(rules_key):
    rules = [tuple(tuple(tuple(e) for e in side) for side in r) for r in rules_key]
    rec = {"stage": 3, "rules": rules_key}
    try:
        seeds = [s for s in probes() if s]
        fwd = {s: forward_set(s, rules) for s in seeds}
        merges = []
        for s, t in combinations(seeds, 2):
            common = (fwd[s] & fwd[t]) - {s, t}
            if not common:
                continue
            if reachable(s, t, rules, max_states=500) or \
               reachable(t, s, rules, max_states=500):
                continue
            merges.append({"s": s, "t": t, "witness": sorted(common)[0]})
            if len(merges) >= 10:
                break
        rec.update(status="swept", r2_merges=len(merges), examples=merges[:4])
    except Exception as e:
        rec["status"] = f"error:{e}"
    return rec


# ---------- driver ----------

def main():
    t0 = time.time()
    all_rules = enumerate_rules()
    print(f"[stage1] {len(all_rules)} candidate rules", flush=True)
    log = open("maxsweep_log.jsonl", "w")

    survivors, colliders = [], []
    with ProcessPoolExecutor(max_workers=14) as ex:
        futs = {ex.submit(work_single, r): r for r in all_rules}
        done = 0
        for fut in as_completed(futs):
            rec = fut.result()
            log.write(json.dumps(rec) + "\n")
            done += 1
            if done % 200 == 0:
                print(f"[stage1] {done}/{len(all_rules)} "
                      f"({time.time()-t0:.0f}s)", flush=True)
            if rec["status"] == "swept":
                survivors.append(tuple(rec["rule"]))
                if rec["genuine"]:
                    colliders.append((tuple(rec["rule"]), rec))
        log.flush()
        print(f"[stage1] done: {len(survivors)} survivors, "
              f"{len(colliders)} colliding, {time.time()-t0:.0f}s", flush=True)

        # stage 2: pairs of survivors (cap 60 rules -> <=1770 pairs)
        base = survivors[:60]
        pairs = list(combinations(base, 2))
        print(f"[stage2] {len(pairs)} pairs", flush=True)
        futs = {ex.submit(work_pair, p): p for p in pairs}
        done = 0
        pair_colliders = []
        for fut in as_completed(futs):
            rec = fut.result()
            log.write(json.dumps(rec) + "\n")
            done += 1
            if done % 300 == 0:
                print(f"[stage2] {done}/{len(pairs)} "
                      f"({time.time()-t0:.0f}s)", flush=True)
            if rec.get("genuine"):
                pair_colliders.append(rec)
        log.flush()
        print(f"[stage2] done: {len(pair_colliders)} colliding pairs, "
              f"{time.time()-t0:.0f}s", flush=True)

        # stage 3: R2 on the most interesting systems (colliding singles,
        # then rigid singles as controls), cap 40
        r2_targets = [ [list(r)] for r, _ in colliders ]
        r2_targets += [ [list(r)] for r in survivors
                        if tuple(r) not in {c for c, _ in colliders} ][: 40 - len(r2_targets)]
        print(f"[stage3] {len(r2_targets)} systems", flush=True)
        futs = {ex.submit(work_r2, t): t for t in r2_targets}
        r2_hits = []
        for fut in as_completed(futs):
            rec = fut.result()
            log.write(json.dumps(rec) + "\n")
            if rec.get("r2_merges"):
                r2_hits.append(rec)
        log.close()

    print("\n=== MAXSWEEP SUMMARY ===", flush=True)
    print(f"rules: {len(all_rules)}; semantic-D1-probe non-identity survivors: "
          f"{len(survivors)}", flush=True)
    print(f"stage1 colliding singles: {len(colliders)}", flush=True)
    for r, rec in colliders[:10]:
        print(f"  {r}: indep={rec['independent']} down={rec['downstream']}",
              flush=True)
    print(f"stage2 colliding pairs: {len(pair_colliders)}", flush=True)
    for rec in sorted(pair_colliders,
                      key=lambda x: -x["independent"])[:10]:
        print(f"  indep={rec['independent']} down={rec['downstream']} "
              f"rules={rec['rules']}", flush=True)
    print(f"stage3 systems with R2 merges: {len(r2_hits)}", flush=True)
    for rec in r2_hits[:10]:
        print(f"  merges={rec['r2_merges']} rules={rec['rules']}", flush=True)
    print(f"total time {time.time()-t0:.0f}s", flush=True)


if __name__ == "__main__":
    main()
