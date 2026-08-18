"""Independent replay checker for IDEA-DJ-30 (adversarial re-verification).

Reads dj30_results.jsonl ONLY (never dj30_fourcell.py's internals). For each
decided (grower, tier) summary cell, samples up to 20 recorded pairs and
recomputes, from the recorded pair state and matched-edge values, using
core.py for rule application:

  1. that m1/m2 correspond to real, distinct, occurrence-disjoint,
     vertex-sharing matches of the cell's rule whose one-step results
     canonically equal the recorded t1/t2;
  2. joinability of canonical(t1)/canonical(t2) by an independently written
     level-synchronized BFS under the header's stated caps
     (depth 6 / max_states 2000 / max_verts 7 per side);
  3. causal-DAG iso for the two orders: for each order, apply the first
     event traced (core.apply_rule_traced), port the second match's
     untouched occurrence into the intermediate state, and record whether
     the second event consumes any edge PRODUCED by the first (the comatch);
     per the header, two 2-node same-label DAGs are iso iff the dependency
     edge counts are equal.

Also cross-checks each summary's aggregate counts against a full scan of the
cell's recorded pair lines. Appends nothing to the jsonl.
"""
import json
import random
import sys
from collections import deque

sys.path.insert(0, "/Users/edwin/Projects/discrete-jacobian/phase1")
import core

JSONL = "/Users/edwin/Projects/discrete-jacobian/phase1/dj30_results.jsonl"
REPORT = "/Users/edwin/Projects/discrete-jacobian/phase1/dj30_replay_report.txt"
SAMPLE = 20
SEED = 712

DEPTH_CAP = 6
MAX_STATES = 2000
MAX_VERTS = 7


def load():
    header, summaries, pairs = None, [], []
    with open(JSONL) as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            d = json.loads(line)
            if d["type"] == "header":
                header = d
            elif d["type"] == "summary":
                summaries.append(d)
            elif d["type"] == "pair":
                pairs.append(d)
    return header, summaries, pairs


def as_state(edges):
    return tuple(tuple(e) for e in edges)


def as_rule(rule_json):
    lhs, rhs = rule_json
    return (tuple(tuple(e) for e in lhs), tuple(tuple(e) for e in rhs))


def closure(start, rule):
    """Forward closure of canonical state `start` under `rule`, level by level.

    Yields (depth, frontier_set); respects MAX_STATES / MAX_VERTS caps.
    Returns via StopIteration-free generator; caller enforces DEPTH_CAP.
    """
    seen = {start}
    frontier = {start}
    yield 0, frontier
    depth = 0
    while frontier and depth < DEPTH_CAP:
        depth += 1
        nxt = set()
        for s in frontier:
            if len(core.vertices(s)) > MAX_VERTS:
                continue  # retained as member, not expanded
            for m in core.matches(s, rule):
                c = core.canonical(core.apply_rule(s, rule, m))
                if c not in seen:
                    seen.add(c)
                    nxt.add(c)
            if len(seen) > MAX_STATES:
                return
        frontier = nxt
        yield depth, frontier


def joinable(t1, t2, rule):
    """Level-synchronized BFS join search. Returns True/False/None(cap)."""
    g1, g2 = closure(t1, rule), closure(t2, rule)
    seen1, seen2 = set(), set()
    done1 = done2 = False
    cap = False
    for _ in range(DEPTH_CAP + 1):
        if not done1:
            try:
                _, f1 = next(g1)
                seen1 |= f1
            except StopIteration:
                done1 = True
                if len(seen1) >= MAX_STATES:
                    cap = True
        if not done2:
            try:
                _, f2 = next(g2)
                seen2 |= f2
            except StopIteration:
                done2 = True
                if len(seen2) >= MAX_STATES:
                    cap = True
        if seen1 & seen2:
            return True
        if done1 and done2:
            break
    if seen1 & seen2:
        return True
    return None if cap else False


def find_match_pairs(state, rule, m1_edges, m2_edges, t1c, t2c):
    """All ordered (ma, mb) distinct matches with occurrence-disjoint index
    sets, matched edge values equal to m1_edges/m2_edges (as multisets over
    occurrences), sharing >=1 vertex, and results canonically t1c/t2c."""
    ms = core.matches(state, rule)
    want1 = sorted(tuple(e) for e in m1_edges)
    want2 = sorted(tuple(e) for e in m2_edges)
    out = []
    for ma in ms:
        va = sorted(state[j] for j in ma[0])
        if va != want1:
            continue
        if core.canonical(core.apply_rule(state, rule, ma)) != t1c:
            continue
        for mb in ms:
            if mb is ma:
                continue
            vb = sorted(state[j] for j in mb[0])
            if vb != want2:
                continue
            if set(ma[0]) & set(mb[0]):
                continue  # occurrence overlap: not this class
            sa = {v for j in ma[0] for v in state[j]}
            sb = {v for j in mb[0] for v in state[j]}
            if not (sa & sb):
                continue  # parallel independent, excluded class
            if core.canonical(core.apply_rule(state, rule, mb)) != t2c:
                continue
            out.append((ma, mb))
    return out


def dep_edge(state, rule, first, second):
    """Apply `first` traced; port `second` (occurrence-disjoint) into the
    intermediate; return whether second consumes any produced edge of first.

    Since occurrences are disjoint, second's edges survive: their new indices
    are old index minus the number of consumed indices below them. Produced
    edges occupy the tail (the comatch). So the dependency is second's ported
    indices intersecting the comatch indices."""
    result, (co_idx, _) = core.apply_rule_traced(state, rule, first)
    consumed = sorted(first[0])
    ported = []
    for j in second[0]:
        nj = j - sum(1 for c in consumed if c < j)
        # verify the ported occurrence is intact
        if result[nj] != state[j]:
            raise AssertionError("port failed: edge moved unexpectedly")
        ported.append(nj)
    # sanity: ported occurrence is a live match of the rule in result
    live = any(set(m[0]) == set(ported) and m[1] == second[1]
               for m in core.matches(result, rule))
    if not live:
        raise AssertionError("ported second event is not a live match")
    return bool(set(ported) & set(co_idx)), result, ported


def final_state(state, rule, first, second):
    result, _ = core.apply_rule_traced(state, rule, first)
    consumed = sorted(first[0])
    ported = tuple(j - sum(1 for c in consumed if c < j) for j in second[0])
    return core.canonical(core.apply_rule(result, rule, (ported, second[1])))


def recheck_pair(p, rule):
    """Returns (ok, detail_string_or_None)."""
    state = as_state(p["state"])
    t1c = core.canonical(as_state(p["t1"]))
    t2c = core.canonical(as_state(p["t2"]))

    cands = find_match_pairs(state, rule, p["m1_edges"], p["m2_edges"],
                             t1c, t2c)
    if not cands:
        return False, ("no (m1,m2) match pair in the recorded state "
                       "reproduces the recorded t1/t2")

    # joinability, recomputed from scratch
    j = joinable(t1c, t2c, rule)
    if j is not p["state_join"]:
        return False, (f"join mismatch: recorded state_join={p['state_join']}"
                       f", replay found {j} "
                       f"(t1c={t1c}, t2c={t2c})")

    # DAG iso, recomputed for every candidate realization
    iso_vals = set()
    dep_pairs = set()
    for ma, mb in cands:
        dA, _, _ = dep_edge(state, rule, ma, mb)   # order A: m1 then m2
        dB, _, _ = dep_edge(state, rule, mb, ma)   # order B: m2 then m1
        dep_pairs.add((dA, dB))
        iso_vals.add(dA == dB)  # 2-node same-label DAGs: iso iff edge counts equal
    if len(iso_vals) != 1:
        return False, (f"ambiguous realization: candidate match pairs "
                       f"disagree on dag-iso: dep pairs {sorted(dep_pairs)}")
    iso = iso_vals.pop()
    if iso is not (p["dag_iso"] is True):
        return False, (f"dag_iso mismatch: recorded {p['dag_iso']}, replay "
                       f"computed {iso} (dep edges {sorted(dep_pairs)})")

    # bonus consistency: completions equal iff recorded (do not fail the cell
    # verdict on this alone, but report it -- it is part of CI evidence)
    ma, mb = cands[0]
    fA = final_state(state, rule, ma, mb)
    fB = final_state(state, rule, mb, ma)
    if "completions_equal" in p and (fA == fB) != p["completions_equal"]:
        return False, (f"completions_equal mismatch: recorded "
                       f"{p['completions_equal']}, replay {fA == fB}")
    return True, None


def main():
    header, summaries, pairs = load()
    rng = random.Random(SEED)
    lines = []
    lines.append("IDEA-DJ-30 independent replay (dj30_replay.py)")
    lines.append(f"jsonl: {JSONL}")
    lines.append(f"seed={SEED}, sample cap={SAMPLE} pairs/cell; caps: "
                 f"depth={DEPTH_CAP}, max_states={MAX_STATES}, "
                 f"max_verts={MAX_VERTS}")
    lines.append("")

    decided = [s for s in summaries
               if not s["piskunov_cell"].startswith("Inconclusive")]
    lines.append(f"summary cells found: {len(summaries)}; "
                 f"decided (non-Inconclusive): {len(decided)}")
    for s in summaries:
        lines.append(f"  {s['grower']} tier{tuple(s['tier'])}: "
                     f"{s['piskunov_cell']}")
    lines.append("")

    overall_ok = True
    for s in decided:
        g, tier = s["grower"], tuple(s["tier"])
        rule = as_rule(s["rule"])
        cell_pairs = [p for p in pairs
                      if p["grower"] == g and tuple(p["tier"]) == tier]
        lines.append(f"=== cell {g} tier{tier} -- recorded verdict: "
                     f"{s['piskunov_cell']} ===")

        # aggregate cross-check against full scan of recorded lines
        agg_probs = []
        if len(cell_pairs) != s["n_tested"]:
            agg_probs.append(f"jsonl has {len(cell_pairs)} pair lines, "
                             f"summary n_tested={s['n_tested']}")
        n_join = sum(1 for p in cell_pairs if p["state_join"] is True)
        n_iso = sum(1 for p in cell_pairs if p["dag_iso"] is True)
        n_none = sum(1 for p in cell_pairs if p["dag_iso"] is None)
        n_cap = sum(1 for p in cell_pairs if p.get("cap_hit"))
        for name, got, want in [("n_state_join", n_join, s["n_state_join"]),
                                ("n_dag_iso", n_iso, s["n_dag_iso"]),
                                ("n_dag_none", n_none, s["n_dag_none"])]:
            if got != want:
                agg_probs.append(f"{name}: recorded lines give {got}, "
                                 f"summary says {want}")
        if n_cap and not s["cap_hit"]:
            agg_probs.append(f"{n_cap} pair lines have cap_hit but summary "
                             f"cap_hit=false")
        lines.append(f"aggregate scan of {len(cell_pairs)} recorded pairs: "
                     + ("consistent with summary" if not agg_probs
                        else "; ".join(agg_probs)))

        # verdict-shape check (from header definition, independently applied)
        if s["piskunov_cell"] == "CI∧confluent":
            shape_ok = (n_join == len(cell_pairs) == s["n_pairs"]
                        and n_iso == len(cell_pairs) and n_none == 0
                        and s["n_untested"] == 0 and n_cap == 0)
            if not shape_ok:
                agg_probs.append("recorded per-pair lines do not support "
                                 "CI∧confluent for the whole cell")

        sample = (cell_pairs if len(cell_pairs) <= SAMPLE
                  else rng.sample(cell_pairs, SAMPLE))
        sample.sort(key=lambda p: p["pair_index"])
        first_bad = None
        for p in sample:
            ok, why = recheck_pair(p, rule)
            if not ok:
                first_bad = (p, why)
                break
        if first_bad is None and not agg_probs:
            lines.append(f"replayed {len(sample)} sampled pairs "
                         f"(pair_index {[p['pair_index'] for p in sample]}): "
                         f"all agree")
            lines.append(f"VERDICT: CONFIRMED -- {g} tier{tier} "
                         f"{s['piskunov_cell']}")
        else:
            overall_ok = False
            lines.append(f"VERDICT: DISPUTED -- {g} tier{tier}")
            if agg_probs:
                for a in agg_probs:
                    lines.append(f"  aggregate problem: {a}")
            if first_bad:
                p, why = first_bad
                lines.append("  first disagreeing pair, in full:")
                lines.append(f"    pair_index={p['pair_index']}")
                lines.append(f"    state={p['state']}")
                lines.append(f"    m1_edges={p['m1_edges']} "
                             f"m2_edges={p['m2_edges']}")
                lines.append(f"    recorded: t1={p['t1']} t2={p['t2']} "
                             f"state_join={p['state_join']} "
                             f"dag_iso={p['dag_iso']} "
                             f"completions_equal={p.get('completions_equal')}")
                lines.append(f"    disagreement: {why}")
        lines.append("")

    lines.append("OVERALL: " + ("all decided cells CONFIRMED" if overall_ok
                                else "one or more cells DISPUTED"))
    report = "\n".join(lines) + "\n"
    with open(REPORT, "w") as fh:
        fh.write(report)
    print(report)


if __name__ == "__main__":
    main()
