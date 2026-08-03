"""Witness-level analysis of history ambiguity (D-IA, 2026-07-28).

Every ambiguity witness is a 5-tuple (S, m, T, m2, pred): a probe state S,
a match m with traced result T, and a reverse-match m2 supported off the
comatch whose application yields pred with pred != S up to iso. By the DPO
undo fact the forward rule applied to pred at the comatch of (rev, m2)
returns T exactly, so EVERY witness exhibits one-step non-injectivity of
the successor RELATION on iso classes: {S, pred} -> T. (Checked per
witness below: `fwd_ok`.) The open questions therefore live in what ELSE
the pair (S, pred) satisfies:

  - causal class: `orbit` (mutually reachable, bounded BFS), `oneway`,
    or `independent` (mutually unreachable — the analogue of the sweep's
    INDEPENDENT pairs);
  - policy: whether the min-successor policy sends S and pred to the SAME
    image (a policy collision) or shields the pair (diverts one of them);
  - census: whether pred fits inside the probe tier at all.

A rule has INDEPENDENT AMBIGUITY (D-IA) iff some witness is independent.
Usage: python independent_ambiguity.py MAX_V MAX_E WORKERS OUTFILE
                                        [--rules holdout|colliders|all]
"""
import argparse
import json
import sys
import time
from concurrent.futures import ProcessPoolExecutor, as_completed

from core import (canonical, matches, apply_rule, apply_rule_traced,
                  reverse_rule, f_min)
from search import enumerate_states, reachable

PAIR_CAP = 400          # distinct (S, pred) pairs examined per rule
BFS_STATES = 2000       # mirror search.reachable defaults exactly
BFS_VERTS = 7

_probes = None
_ARGS = None


def get_probes(maxv, maxe):
    global _probes
    if _probes is None:
        _probes = enumerate_states(maxv, maxe)
    return _probes


def witness_pairs(rule, probes):
    """Yield deduplicated witness pairs (S, pred, Tc) with S, pred, Tc
    canonical and pred != S."""
    rev = reverse_rule(rule)
    seen = set()
    for s in probes:
        cs = canonical(s)
        for m in matches(s, rule):
            result, (co_idx, _) = apply_rule_traced(s, rule, m)
            tc = canonical(result)
            for m2 in matches(result, rev):
                if set(m2[0]) == set(co_idx):
                    continue
                pred = canonical(apply_rule(result, rev, m2))
                if pred == cs:
                    continue
                key = (cs, pred, tc)
                if key in seen:
                    continue
                seen.add(key)
                yield cs, pred, tc
                if len(seen) >= PAIR_CAP:
                    return


def classify_rule(rule, maxv, maxe):
    probes = get_probes(maxv, maxe)
    rules = [rule]
    reach_memo = {}

    def reach(a, b):
        if (a, b) not in reach_memo:
            reach_memo[(a, b)] = reachable(a, b, rules, BFS_STATES, BFS_VERTS)
        return reach_memo[(a, b)]

    counts = {}          # (causal_class, replayable) -> count
    ia_policy_collide = 0    # independent AND replayable, policy-colliding
    ia_policy_shielded = 0   # independent AND replayable, policy-diverted
    ia_pred_in_census = 0
    example = None
    n_pairs = 0
    from core import successors
    for s, pred, tc in witness_pairs(rule, probes):
        n_pairs += 1
        replay = tc in successors(pred, rules)
        r_sp, r_ps = reach(s, pred), reach(pred, s)
        cls = ("orbit" if (r_sp and r_ps) else
               "oneway" if (r_sp or r_ps) else "independent")
        key = f"{cls}|{'replay' if replay else 'phantom'}"
        counts[key] = counts.get(key, 0) + 1
        if cls == "independent" and replay:
            nv = len({v for e in pred for v in e})
            in_census = nv <= maxv and len(pred) <= maxe
            ia_pred_in_census += in_census
            policy_hit = f_min(s, rules) == f_min(pred, rules)
            if policy_hit:
                ia_policy_collide += 1
            else:
                ia_policy_shielded += 1
            if example is None:
                example = {"S": [list(e) for e in s],
                           "pred": [list(e) for e in pred],
                           "T": [list(e) for e in tc],
                           "pred_in_census": in_census,
                           "policy_collides": policy_hit}
    return counts, n_pairs, example, \
        ia_policy_collide, ia_policy_shielded, ia_pred_in_census


def work(rule_l):
    maxv, maxe = _ARGS
    rule = tuple(tuple(tuple(e) for e in side) for side in rule_l)
    rec = {"rule": rule_l, "tier": [maxv, maxe]}
    try:
        t0 = time.time()
        (counts, n_pairs, example,
         ipc, ips, ipin) = classify_rule(rule, maxv, maxe)
        rec.update(status="ok", pairs=n_pairs, classes=counts,
                   ia=counts.get("independent|replay", 0) > 0,
                   ia_policy_collide=ipc, ia_policy_shielded=ips,
                   ia_pred_in_census=ipin,
                   example_ia=example,
                   secs=round(time.time() - t0, 1))
    except Exception as e:
        rec["status"] = f"error:{e!r}"
    return rec


def init_worker(args):
    global _ARGS
    _ARGS = args


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("maxv", type=int)
    ap.add_argument("maxe", type=int)
    ap.add_argument("workers", type=int)
    ap.add_argument("outfile")
    ap.add_argument("--rules", default="holdouts",
                    choices=["holdouts", "colliders", "all", "ia-frontier"])
    a = ap.parse_args()

    sel = []
    if a.rules == "ia-frontier":
        # the D-IA-but-rigid rules from the (4,4) witness classification
        for line in open("ia_holdouts_4_4.jsonl"):
            r = json.loads(line)
            if r.get("status") == "ok" and r.get("ia"):
                sel.append(r["rule"])
    else:
        for line in open("stress_4_4.jsonl"):
            r = json.loads(line)
            if r.get("status") != "ok":
                continue
            if a.rules == "holdouts" and r["ambiguous"] and not r["genuine"]:
                sel.append(r["rule"])
            elif a.rules == "colliders" and r["genuine"]:
                sel.append(r["rule"])
            elif a.rules == "all":
                sel.append(r["rule"])
    print(f"[ia {a.maxv},{a.maxe}] {len(sel)} rules, {a.workers} workers",
          flush=True)
    t0 = time.time()
    n_indep = 0
    with open(a.outfile, "w") as log, \
         ProcessPoolExecutor(a.workers, initializer=init_worker,
                             initargs=((a.maxv, a.maxe),)) as ex:
        futs = [ex.submit(work, r) for r in sel]
        for i, fut in enumerate(as_completed(futs)):
            rec = fut.result()
            log.write(json.dumps(rec) + "\n")
            log.flush()
            n_indep += bool(rec.get("ia"))
            if (i + 1) % 10 == 0:
                print(f"[ia] {i+1}/{len(sel)} ({time.time()-t0:.0f}s)",
                      flush=True)
    print(f"[ia] DONE {time.time()-t0:.0f}s: "
          f"{n_indep}/{len(sel)} rules have INDEPENDENT ambiguity", flush=True)


if __name__ == "__main__":
    init_worker((int(sys.argv[1]), int(sys.argv[2])))
    main()
