#!/usr/bin/env python3
"""IDEA-DJ-30-FOUR-CELL: four-cell Piskunov table on the five edge-growers.

Per (grower, tier) cell: enumerate overlapping critical pairs over the tier
census, test each pair for (a) final-state joinability and (b) causal-DAG iso
of the two completion orders, and stamp the cell into one of
CI∧confluent / CI∧¬confluent / ¬CI∧confluent / neither / Inconclusive.

DEFINITIONS (stamped here per ADVERSARIAL_REVIEW A1 define-don't-assume; none
of these terms is defined elsewhere in the repo):

- tier [maxv, maxe]: the census of all canonical states with <= maxv vertices
  and 1..maxe edges (Q5 vocabulary; q5_deep.py usage line). Tiers here are
  (4,4) and (6,4), both Q5-already-used (q5cert_max44_*, q5_deep_6_4.jsonl).
- event: a single rule application, the triple (state S, rule r, match m)
  with m = (edge_indices, binding) exactly as produced by core.matches; its
  effect is core.apply_rule_traced(S, r, m).
- overlapping critical pair: an unordered pair {m1, m2} of DISTINCT matches of
  the grower at one census state S such that the matched edge occurrences
  overlap. Two overlap notions are recorded:
    overlap="edge":   the matched edge-index sets intersect (the REQ's strict
                      notion: they share at least one edge OCCURRENCE);
    overlap="vertex": occurrence sets disjoint but the matched edges share at
                      least one vertex.
  NOTE (proved by exhaustion in every cell, see n_pairs_edge_overlap): for a
  single-edge-LHS rule, core.matches binds injectively, so every non-loop
  edge occurrence admits EXACTLY ONE match; hence two distinct applications
  can never share an occurrence and the strict "edge" class is empty. The
  script still enumerates it (the check is the proof-by-exhaustion) and the
  substantive table is carried by the "vertex" class. Pairs with disjoint
  vertex support are parallel-independent boilerplate and are excluded.
- pair dedup: pairs are deduplicated by canonical form = minimum over all
  vertex relabelings of (sorted relabeled S, sorted relabeled matched-edge
  multisets, unordered in m1/m2).
- joinability: T1 = canonical(apply(S,r,m1)), T2 = canonical(apply(S,r,m2))
  are joinable iff a common canonical state exists in the forward closures,
  searched by level-synchronized BFS with depth cap 6 per side, guarded by
  max_states=2000 and max_verts=7 per side -- deliberately the exact
  independence_bounds vocabulary of the Q5 certificates. A state with more
  than max_verts vertices is retained as a member but not expanded (same
  convention as search.reachable). A "no" with none of the guards tripped is
  "not joinable within depth 6"; a "no" with a guard tripped is cap_hit and
  counts as unknown.
- completion strategy: order A applies m1 first (traced, unnormalized), then
  m2 ported through it: if m2's occurrences are untouched, its indices are
  re-based over the kept edges and verified to be a live match; otherwise (or
  if verification fails) the residual is the lexicographically least match in
  the intermediate state on the same matched-edge VALUES with the identical
  binding. If no such match exists the pair records dag_iso=None with the
  reason (never faked). Order B is symmetric.
- causal DAG of an order: nodes = the 2 events labeled by the rule; edge
  first->second iff the second event's matched occurrences intersect the
  first event's comatch (produced occurrences), i.e. produced->consumed
  dependency. causal-DAG iso: label-respecting digraph isomorphism. For two
  2-node DAGs whose nodes all carry the same rule label and whose only
  possible edge is earlier->later, an iso exists iff the edge counts are
  equal; the code uses that complete invariant.
- piskunov_cell: over all enumerated pairs of the cell,
  all join & all iso -> "CI∧confluent"; all iso & some definite non-join ->
  "CI∧¬confluent"; all join & some definite non-iso -> "¬CI∧confluent";
  definite non-join & definite non-iso -> "neither". Any unknown (cap_hit
  non-join, dag_iso=None, budget-untested pair) that leaves the cell
  ambiguous -> "Inconclusive-at-depth/tier". Zero enumerated pairs ->
  "Inconclusive-at-tier(no-overlapping-pairs)" (vacuous truth is not
  stamped as a substantive cell).

EVIDENCE DISCIPLINE: everything below is bounded computation at the stamped
tier and caps; no asymptotic or physical claim. Cite, do not redo: Q5 12/12
(Q5_NOTES.md §6, q5cert_min55_* x7, q5cert_max44_* x6), q5_mindec.jsonl,
splice certs (cert_0..11.json, cert_flagship.json), IDEA-DJ-1-MINCOH,
IDEA-DJ-2-ORDERSTAT. This file shares no code with any worker.js
(topological-light-propagation or portfolio copies) or the string-(29)
verifier, and never calls checkCausalInvariance; the only import is the
shared DJ engine phase1/core.py, as sanctioned by the REQ.

Usage:
  python dj30_fourcell.py [--budget-seconds 600] [--pair-timeout 5]
      [--out dj30_results.jsonl] [--growers G1,G3] [--tiers "4,4;6,4"]
      [--force]

Deterministic given the caps: all iteration is over sorted structures; wall
clock is consulted only to record budget/timeout cap_hit, never to order or
select results.
"""
import argparse
import json
import os
import sys
import time
from itertools import combinations_with_replacement, permutations, product

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from core import (apply_rule, apply_rule_traced, canonical, matches,
                  normalize, vertices)

GROWERS = [
    ("G1", [[["v0", "v1"]], [["v0", "v0"], ["v0", "v1"]]]),
    ("G2", [[["v0", "v1"]], [["v0", "v1"], ["v1", "v1"]]]),
    ("G3", [[["v0", "v1"]], [["v0", "v1"], ["v0", "v1"]]]),
    ("G4", [[["v0", "v1"]], [["v0", "v1"], ["v1", "v2"]]]),
    ("G5", [[["v0", "v1"]], [["v0", "v1"], ["v2", "v0"]]]),
]
DEFAULT_TIERS = [(4, 4), (6, 4)]
JOIN_DEPTH = 6
JOIN_MAX_STATES = 2000
JOIN_MAX_VERTS = 7


def to_rule(enc):
    return tuple(tuple(tuple(e) for e in side) for side in enc)


def enumerate_census(maxv, maxe):
    """All canonical states with <= maxv vertices, 1..maxe edges (arity 2).

    Own enumerator (cite-not-redo: search.enumerate_states is the existing
    analogue and is deliberately not copied). Edges over range(maxv) bound the
    vertex count by construction; normalize-level dedup keeps the |V|!
    canonicalizations to distinct normal forms only.
    """
    all_edges = sorted(product(range(maxv), repeat=2))
    seen_norm, out = set(), set()
    for k in range(1, maxe + 1):
        for combo in combinations_with_replacement(all_edges, k):
            n = normalize(combo)
            if n in seen_norm:
                continue
            seen_norm.add(n)
            out.add(canonical(n))
    return sorted(out)


def pair_fingerprint(state, edges1, edges2):
    """Canonical form of (state, {matched-edge multiset 1, ... 2})."""
    vs = vertices(state)
    best = None
    for perm in permutations(range(len(vs))):
        mp = dict(zip(vs, perm))
        st = tuple(sorted(tuple(mp[v] for v in e) for e in state))
        a = tuple(sorted(tuple(mp[v] for v in e) for e in edges1))
        b = tuple(sorted(tuple(mp[v] for v in e) for e in edges2))
        cand = (st, min((a, b), (b, a)))
        if best is None or cand < best:
            best = cand
    return best


def enumerate_pairs(census, rule, cell_deadline):
    """Deduped overlapping critical pairs over the census. Deterministic.

    Returns (pairs, truncated): truncated=True iff the cell budget expired
    mid-enumeration (pair list then incomplete -> cell Inconclusive).
    """
    pairs, seen_fp = [], set()
    for S in census:
        if time.monotonic() > cell_deadline:
            return pairs, True
        ms = matches(S, rule)
        for i in range(len(ms)):
            for j in range(i + 1, len(ms)):
                m1, m2 = ms[i], ms[j]
                e1 = tuple(S[k] for k in m1[0])
                e2 = tuple(S[k] for k in m2[0])
                if set(m1[0]) & set(m2[0]):
                    kind = "edge"
                elif {v for e in e1 for v in e} & {v for e in e2 for v in e}:
                    kind = "vertex"
                else:
                    continue  # disjoint support: parallel independent, not a critical pair
                fp = pair_fingerprint(S, e1, e2)
                if fp in seen_fp:
                    continue
                seen_fp.add(fp)
                pairs.append({"state": S, "m1": m1, "m2": m2,
                              "e1": e1, "e2": e2, "overlap": kind, "fp": fp})
    return pairs, False


def bfs_join(t1, t2, rule, deadline):
    """Joinability within JOIN_DEPTH/JOIN_MAX_STATES/JOIN_MAX_VERTS per side.

    Returns (joined, [depth_from_t1, depth_from_t2] or None, capped).
    capped=True means some guard (timeout, max_states, max_verts) truncated
    the search; a negative answer with capped=True is unknown, not a no.
    """
    if t1 == t2:
        return True, [0, 0], False
    depth = [{t1: 0}, {t2: 0}]
    frontier = [[t1], [t2]]
    capped = False
    for d in range(1, JOIN_DEPTH + 1):
        for side in (0, 1):
            other = 1 - side
            nxt = []
            for s in frontier[side]:
                if time.monotonic() > deadline:
                    return False, None, True
                if len(vertices(s)) > JOIN_MAX_VERTS:
                    capped = True  # retained as member, not expanded
                    continue
                succ = sorted({canonical(apply_rule(s, rule, m))
                               for m in matches(s, rule)})
                for t in succ:
                    if t in depth[side]:
                        continue
                    if len(depth[side]) >= JOIN_MAX_STATES:
                        capped = True
                        break
                    depth[side][t] = d
                    if t in depth[other]:
                        out = [0, 0]
                        out[side] = d
                        out[other] = depth[other][t]
                        return True, out, capped
                    nxt.append(t)
            frontier[side] = nxt
        if not frontier[0] and not frontier[1]:
            break
    return False, None, capped


def complete_order(state, rule, m_first, m_second):
    """Apply m_first (traced), then m_second ported/residual. See docstring.

    Returns {"dep": bool, "final": canonical, "via": "ported"|"residual"}
    or None if the residual is undefined (caller records dag_iso=None).
    """
    traw, (prod_idxs, _) = apply_rule_traced(state, rule, m_first)
    first = set(m_first[0])
    sec_edges = tuple(sorted(state[j] for j in m_second[0]))
    ported, via = None, None
    if not (set(m_second[0]) & first):
        idxs = tuple(j - sum(1 for k in m_first[0] if k < j)
                     for j in m_second[0])
        cand = (idxs, dict(m_second[1]))
        if any(mi[0] == cand[0] and mi[1] == cand[1]
               for mi in matches(traw, rule)):
            ported, via = cand, "ported"
    if ported is None:
        cands = [mi for mi in matches(traw, rule)
                 if tuple(sorted(traw[j] for j in mi[0])) == sec_edges
                 and mi[1] == m_second[1]]
        if not cands:
            return None
        ported, via = min(cands, key=lambda mi: mi[0]), "residual"
    dep = bool(set(ported[0]) & set(prod_idxs))
    final_raw, _ = apply_rule_traced(traw, rule, ported)
    return {"dep": dep, "final": canonical(final_raw), "via": via}


def jstate(state):
    return [list(e) for e in state]


def cell_verdict(records, n_untested, enum_truncated):
    n = len(records) + n_untested
    if n == 0:
        if enum_truncated:
            return "Inconclusive-at-depth/tier"
        return "Inconclusive-at-tier(no-overlapping-pairs)"
    join_false = any(r["state_join"] is False and not r["cap_hit"]
                     for r in records)
    join_unknown = (n_untested > 0 or enum_truncated or
                    any(r["state_join"] is False and r["cap_hit"]
                        for r in records))
    iso_false = any(r["dag_iso"] is False for r in records)
    iso_unknown = (n_untested > 0 or enum_truncated or
                   any(r["dag_iso"] is None for r in records))
    join_st = ("not-all" if join_false
               else ("unknown" if join_unknown else "all"))
    iso_st = ("not-all" if iso_false
              else ("unknown" if iso_unknown else "all"))
    if join_st == "not-all" and iso_st == "not-all":
        return "neither"
    if "unknown" in (join_st, iso_st):
        return "Inconclusive-at-depth/tier"
    return {("all", "all"): "CI∧confluent",
            ("all", "not-all"): "¬CI∧confluent",
            ("not-all", "all"): "CI∧¬confluent",
            }[(join_st, iso_st)]


def run_cell(gid, rule_enc, tier, census, budget, pair_timeout, log):
    rule = to_rule(rule_enc)
    t0 = time.monotonic()
    cell_deadline = t0 + budget
    pairs, enum_truncated = enumerate_pairs(census, rule, cell_deadline)
    records = []
    n_untested = 0
    for k, p in enumerate(pairs):
        if time.monotonic() > cell_deadline:
            n_untested = len(pairs) - k
            break
        tp0 = time.monotonic()
        deadline = min(tp0 + pair_timeout, cell_deadline)
        S, m1, m2 = p["state"], p["m1"], p["m2"]
        t1 = canonical(apply_rule(S, rule, m1))
        t2 = canonical(apply_rule(S, rule, m2))
        joined, jdepth, jcapped = bfs_join(t1, t2, rule, deadline)
        ca = complete_order(S, rule, m1, m2)
        cb = complete_order(S, rule, m2, m1)
        if ca is None or cb is None:
            dag_iso, dag_reason, deps, compl_eq = None, (
                "residual-undefined: after the first application the second "
                "has no match on its original matched-edge values with the "
                "identical binding (order %s)" %
                ("A" if ca is None else "B")), None, None
        else:
            # both DAGs: 2 events, same rule label, only possible edge is
            # earlier->later => label-respecting iso <=> equal edge count.
            dag_iso = (ca["dep"] == cb["dep"])
            dag_reason = None
            deps = [ca["dep"], cb["dep"]]
            compl_eq = (ca["final"] == cb["final"])
        cap_hit = bool(jcapped and not joined)
        rec = {
            "type": "pair", "grower": gid, "rule": rule_enc,
            "tier": list(tier), "pair_index": k,
            "fingerprint": {"state": jstate(p["fp"][0]),
                            "m1_edges": jstate(p["fp"][1][0]),
                            "m2_edges": jstate(p["fp"][1][1])},
            "state": jstate(S), "overlap": p["overlap"],
            "m1_edges": jstate(p["e1"]), "m2_edges": jstate(p["e2"]),
            "t1": jstate(t1), "t2": jstate(t2),
            "state_join": joined, "join_depth": jdepth,
            "join_caps": {"depth": JOIN_DEPTH,
                          "max_states": JOIN_MAX_STATES,
                          "max_verts": JOIN_MAX_VERTS},
            "dag_iso": dag_iso, "dag_reason": dag_reason,
            "dag_dep_edges": deps,
            "completions_equal": compl_eq,
            "completion_via": ([ca["via"], cb["via"]]
                               if ca is not None and cb is not None else None),
            "cap_hit": cap_hit,
            "wall_ms": round((time.monotonic() - tp0) * 1000, 1),
        }
        log.write(json.dumps(rec, ensure_ascii=False) + "\n")
        log.flush()
        records.append(rec)
    n_pairs = len(pairs)
    budget_capped = enum_truncated or n_untested > 0
    summary = {
        "type": "summary", "grower": gid, "rule": rule_enc,
        "tier": list(tier), "census": len(census),
        "n_pairs": n_pairs,
        "n_tested": len(records), "n_untested": n_untested,
        "enum_truncated": enum_truncated,
        "n_pairs_edge_overlap": sum(1 for p in pairs
                                    if p["overlap"] == "edge"),
        "n_pairs_vertex_overlap": sum(1 for p in pairs
                                      if p["overlap"] == "vertex"),
        "n_state_join": sum(1 for r in records if r["state_join"]),
        "n_dag_iso": sum(1 for r in records if r["dag_iso"] is True),
        "n_dag_none": sum(1 for r in records if r["dag_iso"] is None),
        "piskunov_cell": cell_verdict(records, n_untested, enum_truncated),
        "cap_hit": bool(budget_capped or
                        any(r["cap_hit"] for r in records)),
        "budget_seconds": budget,
        "secs": round(time.monotonic() - t0, 1),
    }
    log.write(json.dumps(summary, ensure_ascii=False) + "\n")
    log.flush()
    return summary


def main():
    ap = argparse.ArgumentParser(description="IDEA-DJ-30 four-cell table")
    ap.add_argument("--budget-seconds", type=float, default=600.0,
                    help="wall-clock budget per (grower,tier) cell")
    ap.add_argument("--pair-timeout", type=float, default=5.0,
                    help="wall-clock cap per pair (joinability BFS)")
    ap.add_argument("--out", default=os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "dj30_results.jsonl"))
    ap.add_argument("--growers", default=None,
                    help="comma list, e.g. G1,G3 (default: all five)")
    ap.add_argument("--tiers", default=None,
                    help='semicolon list, e.g. "4,4;6,4" (default both)')
    ap.add_argument("--force", action="store_true",
                    help="allow clobbering an existing --out file")
    args = ap.parse_args()

    out = args.out
    if os.path.exists(out) and not args.force:
        # repo convention (maxsweep.open_evidence_log): committed evidence is
        # never clobbered silently.
        out = out + ".rerun"
        print(f"[dj30] {args.out} exists; writing to {out} "
              f"(use --force to overwrite)", flush=True)

    growers = GROWERS
    if args.growers:
        want = set(args.growers.split(","))
        growers = [g for g in GROWERS if g[0] in want]
    tiers = DEFAULT_TIERS
    if args.tiers:
        tiers = [tuple(int(x) for x in t.split(","))
                 for t in args.tiers.split(";")]

    rows = []
    with open(out, "w") as log:
        header = {
            "type": "header", "experiment": "IDEA-DJ-30-FOUR-CELL",
            "definitions": __doc__.split("DEFINITIONS")[1]
                                  .split("EVIDENCE DISCIPLINE")[0].strip(),
            "caps": {"join_depth": JOIN_DEPTH,
                     "join_max_states": JOIN_MAX_STATES,
                     "join_max_verts": JOIN_MAX_VERTS,
                     "pair_timeout_s": args.pair_timeout,
                     "cell_budget_s": args.budget_seconds},
            "tiers": [list(t) for t in tiers],
            "growers": {gid: enc for gid, enc in growers},
            "cites": ["Q5_NOTES.md §6 (Q5 12/12)", "q5cert_min55_00..06",
                      "q5cert_max44_07..12", "q5_mindec.jsonl",
                      "cert_0..11.json + cert_flagship.json (splice)",
                      "IDEA-DJ-1-MINCOH", "IDEA-DJ-2-ORDERSTAT"],
            "code_provenance": "imports phase1/core.py only; no code shared "
                               "with any worker.js copy or the string-(29) "
                               "verifier; checkCausalInvariance never called",
        }
        log.write(json.dumps(header, ensure_ascii=False) + "\n")
        log.flush()
        for tier in tiers:
            tcen = time.monotonic()
            census = enumerate_census(*tier)
            print(f"[dj30] tier {tier}: census {len(census)} states "
                  f"({time.monotonic()-tcen:.1f}s)", flush=True)
            for gid, enc in growers:
                s = run_cell(gid, enc, tier, census, args.budget_seconds,
                             args.pair_timeout, log)
                rows.append(s)
                print(f"[dj30] {gid} {tier}: n_pairs={s['n_pairs']} "
                      f"join={s['n_state_join']}/{s['n_tested']} "
                      f"iso={s['n_dag_iso']}/{s['n_tested']} "
                      f"-> {s['piskunov_cell']} "
                      f"(cap_hit={s['cap_hit']}, {s['secs']}s)", flush=True)

    rows.sort(key=lambda r: (r["grower"], r["tier"]))
    print()
    hdr = (f"{'grower':<7}{'tier':<8}{'n_pairs':>8}{'n_join':>8}"
           f"{'n_iso':>7}  {'piskunov_cell':<42}{'cap_hit'}")
    print(hdr)
    print("-" * len(hdr))
    for r in rows:
        print(f"{r['grower']:<7}{str(tuple(r['tier'])):<8}"
              f"{r['n_pairs']:>8}{r['n_state_join']:>8}"
              f"{r['n_dag_iso']:>7}  {r['piskunov_cell']:<42}"
              f"{r['cap_hit']}")
    print(f"\n[dj30] results: {out}")


if __name__ == "__main__":
    main()
