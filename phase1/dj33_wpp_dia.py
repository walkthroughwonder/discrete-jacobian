#!/usr/bin/env python3
"""IDEA-DJ-33-WPP-DIA: DJ D-IA / R1 / f_min on the 7 TLP ST_PRESETS rules.

DJ predicates on WPP hypergraph rules — the reverse of Expt 9. Not a TLP UI
job, not Expt 10, not a rerun of 29/30/31/32/37. dim27 is the same *rule*
as IDEA-WPP-37 (TI canonical 2_2→3_2) under a *different* predicate
(D-IA / R1 / f_min, not SAT joinability); 37 is cited, not redone.

DEFINITIONS (cite, do not redo: DEFINITIONS.md addendum D-IA,
WITNESS_ANALYSIS.md Proposition B, Q5_NOTES.md):

- D-IA: some history-ambiguity witness is both replayable and independent
  (independent_ambiguity.classify_rule's `ia` bit). Replay = [T] is a
  genuine one-step successor of [P]. Independent = mutually unreachable
  under the forward rule within search.reachable bounds (2000 states, 7
  verts). For a strictly edge-growing rule, equal-|E| pairs are independent
  without BFS (q5_deep.py: mutual reachability is impossible because edge
  count strictly increases); unequal-|E| pairs still get a one-way BFS.
- R1 independent collision: two canonically distinct census states with
  the same f_min image, neither reachable from the other (DEFINITIONS.md
  R1 + artifact class 6). Orbit (mutual) artifacts cannot occur for
  growers; downstream one-way pairs are reported separately and do not
  count as R1_independent_collision.
- f_min rigidity: no genuine independent f_min collision at the stamped
  tier (the min-successor policy is injective on that census).
- tier: Q5 vocabulary [maxv, maxe] = canonical states with <= maxv verts
  and 1..maxe edges of the rule's arity. Default pair: (4,4) and (6,4),
  both already used in Q5_NOTES.md (and IDEA-DJ-30). A new arity-3 census
  is opened only if both of those Q5 tiers are match-dry for the rule
  (binary census cannot host a ternary LHS).

EVIDENCE DISCIPLINE: BOUNDED COMPUTATION at the stamped tiers. No
physics reading. Searcher (this file + core.py + search.py) is not the
verifier. Any new R1 cert is written unnamed (*.pending.json), passed to
phase1/verify_independent.py (blob 4bade5643b9e), and named only on
VERDICT CONFIRMED. Cite, do not redo: Q5 12/12, q5_mindec.jsonl, the 14
splice/Q5 certs, IDEA-DJ-30 (dj30_fourcell.py / dj30_results.jsonl).
Does not import TLP, does not call checkCausalInvariance, does not load
the 21 string PRESETS, does not touch 712 / zarankiewicz / SAT / GPU.

Usage:
  python dj33_wpp_dia.py [--out dj33_results.jsonl] [--force]
      [--budget-seconds 600]
"""
import argparse
import json
import os
import subprocess
import sys
import time
from itertools import combinations_with_replacement, product

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from core import (apply_rule, apply_rule_traced, canonical, f_min,
                  matches, normalize, reverse_rule, rule_vars, successors,
                  vertices)
from search import enumerate_states, reachable
from dj33_adapter import (PRESET_ORDER, all_adapted, run_adapter_tests,
                          wolfram_form)

HERE = os.path.dirname(os.path.abspath(__file__))
VERIFY = os.path.join(HERE, "verify_independent.py")
VERIFY_BLOB = "4bade5643b9e"

# Q5_NOTES.md already-used small tiers (also IDEA-DJ-30's pair).
Q5_TIERS = [(4, 4), (6, 4)]
# Opened only when both Q5 binary tiers are match-dry (wrong arity, or
# the LHS needs more vertices than the 4-vert Q5 cell can host).
# sierpinski (3 verts, 1 ternary edge): (4,2)+(4,3) arity 3.
# try3d (5 verts, 2 ternary edges): (5,3) small host + Q5_NOTES (5,4) arity 3.
# (6,4) arity 3 is not small (216^4 combinations).

PAIR_CAP = 400          # independent_ambiguity.py
BFS_STATES = 2000       # search.reachable / Q5 independence_bounds
BFS_VERTS = 7
BOUNDS = {"max_states": BFS_STATES, "max_verts": BFS_VERTS}


def jstate(state):
    return [list(e) for e in state]


def jrule(rule):
    return [[list(e) for e in side] for side in rule]


def net_edge_delta(rule):
    return len(rule[1]) - len(rule[0])


def enumerate_census(maxv, maxe, arity):
    """Canonical states, <= maxv verts, 1..maxe edges of the given arity.

    Binary arity=2 delegates to search.enumerate_states (the Q5 enumerator).
    Ternary uses the dj30 combinations_with_replacement census (cite-not-redo
    of dj30_fourcell.enumerate_census) with product(..., repeat=arity).
    """
    if arity == 2:
        return enumerate_states(maxv, maxe, arity=2)
    all_edges = sorted(product(range(maxv), repeat=arity))
    seen_norm, out = set(), set()
    for k in range(1, maxe + 1):
        for combo in combinations_with_replacement(all_edges, k):
            n = normalize(combo)
            if n in seen_norm:
                continue
            seen_norm.add(n)
            out.add(canonical(n))
    return sorted(out)


def causal_class(s, pred, rule):
    """orbit / oneway / independent, grower-shortcut when legal.

    Equal-|E| pairs under a strictly edge-growing rule cannot reach each
    other (q5_deep.py). Unequal pairs: the larger cannot reach the smaller;
    the smaller→larger direction is a bounded BFS.
    """
    d = net_edge_delta(rule)
    rules = [rule]
    if d > 0 and len(s) == len(pred):
        return "independent", "equal-edge-count-grower"
    if d > 0 and len(s) != len(pred):
        lo, hi = (s, pred) if len(s) < len(pred) else (pred, s)
        if (len(hi) - len(lo)) % d != 0:
            return "independent", "edge-count-not-multiple-of-growth"
        hit = reachable(lo, hi, rules, BFS_STATES, BFS_VERTS)
        if hit:
            return "oneway", "grower-oneway-bfs"
        return "independent", "grower-oneway-bfs-miss"
    # non-grower (should not occur for ST_PRESETS); full both-way BFS
    r_sp = reachable(s, pred, rules, BFS_STATES, BFS_VERTS)
    r_ps = reachable(pred, s, rules, BFS_STATES, BFS_VERTS)
    if r_sp and r_ps:
        return "orbit", "both-way-bfs"
    if r_sp or r_ps:
        return "oneway", "both-way-bfs"
    return "independent", "both-way-bfs"


def witness_pairs(rule, probes):
    """Deduped (S, pred, Tc) as in independent_ambiguity.witness_pairs."""
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


def classify_dia(rule, probes, deadline=None):
    """D-IA classification on a probe census. Returns a json-ready dict."""
    t0 = time.monotonic()
    counts = {}
    n_pairs = 0
    ia_collide = ia_shield = ia_in_census = 0
    example = None
    truncated = False
    rules = [rule]
    maxe_probe = max((len(s) for s in probes), default=0)
    maxv_probe = max((len(vertices(s)) for s in probes), default=0)
    for s, pred, tc in witness_pairs(rule, probes):
        if deadline is not None and time.monotonic() > deadline:
            truncated = True
            break
        n_pairs += 1
        replay = tc in successors(pred, rules)
        cls, how = causal_class(s, pred, rule)
        key = f"{cls}|{'replay' if replay else 'phantom'}"
        counts[key] = counts.get(key, 0) + 1
        if cls == "independent" and replay:
            nv = len(vertices(pred))
            in_census = nv <= maxv_probe and len(pred) <= maxe_probe
            ia_in_census += int(in_census)
            policy_hit = f_min(s, rules) == f_min(pred, rules)
            if policy_hit:
                ia_collide += 1
            else:
                ia_shield += 1
            if example is None:
                example = {
                    "S": jstate(s), "pred": jstate(pred), "T": jstate(tc),
                    "pred_in_census": in_census,
                    "policy_collides": policy_hit,
                    "independence_how": how,
                }
    return {
        "pairs": n_pairs,
        "classes": counts,
        "ia": counts.get("independent|replay", 0) > 0,
        "ia_policy_collide": ia_collide,
        "ia_policy_shielded": ia_shield,
        "ia_pred_in_census": ia_in_census,
        "example_ia": example,
        "truncated": truncated,
        "secs": round(time.monotonic() - t0, 2),
    }


def fmin_collisions(census, rule, deadline=None):
    """Independent / downstream f_min collisions on a census."""
    t0 = time.monotonic()
    table = {}
    n_match = 0
    capped = False
    rules = [rule]
    for s in census:
        if deadline is not None and time.monotonic() > deadline:
            capped = True
            break
        img = f_min(s, rules)
        if img is not None:
            n_match += 1
            table.setdefault(img, []).append(s)
    indep = []
    downstream = []
    artifacts_orbit = 0
    for img, pre in sorted(table.items()):
        if len(pre) < 2:
            continue
        # pick a canonical independent pair if any
        found_indep = None
        found_down = None
        for i in range(len(pre)):
            for j in range(i + 1, len(pre)):
                a, b = pre[i], pre[j]
                cls, how = causal_class(a, b, rule)
                if cls == "orbit":
                    artifacts_orbit += 1
                    continue
                if cls == "independent":
                    found_indep = (a, b, how)
                    break
                if cls == "oneway" and found_down is None:
                    found_down = (a, b, how)
            if found_indep:
                break
        if found_indep:
            a, b, how = found_indep
            indep.append({"image": img, "s1": a, "s2": b, "how": how,
                          "n_preimages": len(pre)})
        elif found_down:
            a, b, how = found_down
            downstream.append({"image": img, "s1": a, "s2": b, "how": how,
                               "n_preimages": len(pre)})
    return {
        "n_match": n_match,
        "n_images_multi": sum(1 for pre in table.values() if len(pre) >= 2),
        "n_independent": len(indep),
        "n_downstream": len(downstream),
        "n_orbit": artifacts_orbit,
        "example_independent": (
            {"image": jstate(indep[0]["image"]),
             "s1": jstate(indep[0]["s1"]),
             "s2": jstate(indep[0]["s2"]),
             "how": indep[0]["how"],
             "n_preimages": indep[0]["n_preimages"]}
            if indep else None),
        "capped": capped,
        "secs": round(time.monotonic() - t0, 2),
        "_indep_raw": indep,  # stripped before jsonl
    }


def write_pending_cert(preset, rule, tier, arity, example, path):
    # Independence BFS at Q5's max_verts=7 does not complete in the
    # independent verifier for 2-edge-LHS growers (branching × 7!). Census
    # maxv is the bound the verifier actually finishes; equal-|E| grower
    # independence is unbounded (edge count strictly increases).
    maxv = int(tier[0])
    cert = {
        "kind": "R1-collision",
        "policy": "min-successor",
        "tier": list(tier),
        "arity": arity,
        "preset": preset,
        "experiment": "IDEA-DJ-33-WPP-DIA",
        "rules": [jrule(rule)],
        "state1": example["s1"],
        "state2": example["s2"],
        "claimed_image": example["image"],
        "independence_bounds": {"max_states": BFS_STATES, "max_verts": maxv},
        "independence_argument": "equal-edge-count-grower",
        "note": (
            f"IDEA-DJ-33-WPP-DIA pending (unnamed): ST_PRESETS {preset} "
            f"f_min independent collision at tier {list(tier)} arity={arity}. "
            "BOUNDED COMPUTATION. independence_bounds.max_verts = census maxv "
            "(Q5's max_verts=7 does not complete on this grower in "
            "verify_independent.py). Equal-|E| grower pairs are mutually "
            "unreachable at any bound. Not named until verify_independent.py "
            f"(blob {VERIFY_BLOB}) CONFIRMED. Searcher != verifier."
        ),
    }
    with open(path, "w") as fh:
        json.dump(cert, fh, indent=1)
        fh.write("\n")
    return cert


def verify_cert(path):
    """Run existing verify_independent.py. Searcher does not reimplement."""
    proc = subprocess.run(
        [sys.executable, VERIFY, path],
        cwd=HERE, capture_output=True, text=True,
    )
    out = (proc.stdout or "") + (proc.stderr or "")
    confirmed = proc.returncode == 0 and "VERDICT: CONFIRMED" in proc.stdout
    return confirmed, proc.returncode, out


def pick_tiers(arity, rule, q5_match_counts):
    """Two Q5 tiers, or arity-hosting fallback if both Q5 binary cells are dry.

    Returns (tiers as (maxv,maxe,arity), used_fallback, reason).
    """
    nv = len(rule_vars(rule[0]))
    ne = len(rule[0])
    q5_dry = all(c == 0 for c in q5_match_counts)
    if arity == 2:
        return [(t[0], t[1], 2) for t in Q5_TIERS], False, (
            "Q5_NOTES.md / IDEA-DJ-30 tiers (4,4)+(6,4) binary")
    if not q5_dry:
        return [(t[0], t[1], 2) for t in Q5_TIERS], False, (
            "Q5 binary tiers hosted matches (unexpected for ternary)")
    if nv <= 4:
        return [(4, 2, 3), (4, 3, 3)], True, (
            "Q5 binary (4,4)+(6,4) match-dry for ternary LHS; arity-3 "
            "fallback (4,2)+(4,3) hosts sierpinski (3v,1e)")
    # try3d: 5 distinct LHS verts. (4,*) cannot host. (6,4) arity 3 is not
    # small. (5,4) is Q5_NOTES; (5,3) is the small host opened because
    # (5,2) arity-3 is collision-dry (1 match).
    return [(5, 3, 3), (5, 4, 3)], True, (
        f"Q5 binary match-dry (LHS needs {nv}v/{ne}e); (5,3) small host "
        "+ Q5_NOTES (5,4) arity 3")


def main():
    ap = argparse.ArgumentParser(description="IDEA-DJ-33-WPP-DIA")
    ap.add_argument("--out", default=os.path.join(HERE, "dj33_results.jsonl"))
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--budget-seconds", type=float, default=600.0,
                    help="wall-clock budget per (preset, tier) cell")
    args = ap.parse_args()
    out = args.out
    if os.path.exists(out) and not args.force:
        out = out + ".rerun"
        print(f"[dj33] {args.out} exists; writing to {out} "
              f"(use --force to overwrite)", flush=True)

    try:
        sys.stdout.reconfigure(line_buffering=True)
    except Exception:
        pass
    adapter_rec = run_adapter_tests()
    print(f"[dj33] adapter tests PASS  dim27={adapter_rec['dim27']}",
          flush=True)
    print(f"[dj33]                     chain27={adapter_rec['chain27']}",
          flush=True)

    blob, adapted = all_adapted()
    by_name = {a["preset"]: a for a in adapted}

    # cache censuses
    census_cache = {}

    def get_census(maxv, maxe, arity):
        key = (maxv, maxe, arity)
        if key not in census_cache:
            t0 = time.monotonic()
            census_cache[key] = enumerate_census(maxv, maxe, arity)
            print(f"[dj33] census {key}: {len(census_cache[key])} states "
                  f"({time.monotonic()-t0:.1f}s)", flush=True)
        return census_cache[key]

    rows = []
    # distinct-rule cache so doubleslit/singleslit reuse flat2d work
    rule_cache = {}

    with open(out, "w") as log:
        header = {
            "type": "header",
            "experiment": "IDEA-DJ-33-WPP-DIA",
            "evidence_label": "BOUNDED COMPUTATION",
            "owner": "Edwin Rosero (walkthroughwonder)",
            "ai_assistance": (
                "Cursor Grok 4.6 cloud agent; disclosed. Searcher is this "
                "file; verifier is unmodified phase1/verify_independent.py "
                f"blob {VERIFY_BLOB}."
            ),
            "st_presets_provenance": blob["provenance"],
            "adapter_convention": (
                "TLP integer ports → DJ string atoms; binary {0,1,2,3} → "
                "x,y,z,w; ternary {0,1,2,3,4,5} → x,y,z,u,v,w. core.matches "
                "injective. Inits not used. String PRESETS not loaded."
            ),
            "adapter_tests": adapter_rec,
            "caps": {"pair_cap": PAIR_CAP, "independence_bounds": BOUNDS,
                     "cell_budget_s": args.budget_seconds},
            "q5_tiers": [list(t) for t in Q5_TIERS],
            "ternary_fallback": {
                "sierpinski": [[4, 2, 3], [4, 3, 3]],
                "try3d": [[5, 3, 3], [5, 4, 3]],
            },
            "cites": [
                "DEFINITIONS.md (D-IA addendum)",
                "WITNESS_ANALYSIS.md",
                "Q5_NOTES.md (tiers (4,4),(6,4); Q5 12/12)",
                "IDEA-DJ-30-FOUR-CELL HEAD 32b526c990d9 "
                "(dj30_fourcell.py, dj30_replay.py, dj30_results.jsonl)",
                "phase1/independent_ambiguity.py",
                "phase1/search.py find_r1_collisions / enumerate_states",
                "q5_mindec.jsonl; cert_0..11.json + cert_flagship.json "
                "(14 splice/Q5 certs counted as in README)",
                "verify_independent.py blob 4bade5643b9e",
                "TLP index.html blob 36070e4f18a7 const ST_PRESETS "
                "@ c60aed3eb08d",
            ],
            "not_done": [
                "no TLP UI / no checkCausalInvariance / no string-(29) verifier",
                "no IDEA-WPP-37 redo (SAT joinability)",
                "no Expt 10 / 29 / 30 / 31 / 32 rerun",
                "no 712 / zarankiewicz / SAT / GPU / Kissat / 19x19",
                "no physics reading",
                "no public release; unmerged evidence PR only",
            ],
            "code_provenance": (
                "imports phase1/core.py, search.py, dj33_adapter.py; "
                "D-IA witness loop follows independent_ambiguity.py; "
                "no code shared with TLP worker.js; string PRESETS never loaded"
            ),
        }
        log.write(json.dumps(header, ensure_ascii=False) + "\n")
        log.flush()

        for name in PRESET_ORDER:
            a = by_name[name]
            rule = a["rule"]
            arity = a["arity"]
            key = a["wolfram"]
            print(f"[dj33] {name} arity={arity} {a['wolfram']}", flush=True)

            if key in rule_cache:
                rec = dict(rule_cache[key])
                rec["preset"] = name
                rec["reused_from"] = rec["computed_for"]
                rec["type"] = "summary"
                log.write(json.dumps(
                    {k: v for k, v in rec.items() if not k.startswith("_")},
                    ensure_ascii=False) + "\n")
                log.flush()
                rows.append(rec)
                print(f"[dj33] {name}: reused {rec['computed_for']} "
                      f"(same DJ rule)", flush=True)
                continue

            # probe Q5 binary tiers for matches (even for ternary: document dry)
            q5_match = []
            q5_fmin = []
            for tv, te in Q5_TIERS:
                cen = get_census(tv, te, 2)
                n_match = sum(1 for s in cen if matches(s, rule))
                q5_match.append(n_match)
                print(f"[dj33] {name} Q5-tier ({tv},{te}) arity=2 "
                      f"matches {n_match}/{len(cen)}", flush=True)

            tiers, used_fallback, tier_reason = pick_tiers(
                arity, rule, q5_match)
            print(f"[dj33] {name} tiers={tiers} ({tier_reason})",
                  flush=True)
            dia_yes = False
            dia_records = []
            fmin_records = []
            first_indep = None
            first_indep_tier = None

            for tv, te, tar in tiers:
                cell_deadline = time.monotonic() + args.budget_seconds
                cen = get_census(tv, te, tar)
                n_match = sum(1 for s in cen if matches(s, rule))
                print(f"[dj33] {name} working tier ({tv},{te}) arity={tar} "
                      f"census={len(cen)} matches={n_match}", flush=True)

                dia = classify_dia(rule, cen, cell_deadline)
                dia_rec = {
                    "type": "dia", "preset": name, "tier": [tv, te],
                    "arity": tar, "census": len(cen), "n_match": n_match,
                    **{k: v for k, v in dia.items()},
                }
                log.write(json.dumps(dia_rec, ensure_ascii=False) + "\n")
                log.flush()
                dia_records.append(dia_rec)
                if dia["ia"]:
                    dia_yes = True
                print(f"[dj33] {name} D-IA ({tv},{te}): ia={dia['ia']} "
                      f"pairs={dia['pairs']} classes={dia['classes']} "
                      f"({dia['secs']}s)", flush=True)

                remaining = cell_deadline - time.monotonic()
                fmin = fmin_collisions(
                    cen, rule, cell_deadline if remaining > 0 else time.monotonic()
                )
                raw = fmin.pop("_indep_raw")
                fmin_rec = {
                    "type": "fmin", "preset": name, "tier": [tv, te],
                    "arity": tar, "census": len(cen), **fmin,
                }
                log.write(json.dumps(fmin_rec, ensure_ascii=False) + "\n")
                log.flush()
                fmin_records.append(fmin_rec)
                print(f"[dj33] {name} f_min ({tv},{te}): match={fmin['n_match']} "
                      f"indep={fmin['n_independent']} down={fmin['n_downstream']} "
                      f"({fmin['secs']}s)", flush=True)
                if raw and first_indep is None:
                    first_indep = {
                        "image": jstate(raw[0]["image"]),
                        "s1": jstate(raw[0]["s1"]),
                        "s2": jstate(raw[0]["s2"]),
                        "how": raw[0]["how"],
                    }
                    first_indep_tier = (tv, te, tar)

            r1_yes = first_indep is not None
            fmin_rigid = not r1_yes
            cert_path = None
            verify_out = None
            if r1_yes:
                pending = os.path.join(
                    HERE, f"dj33cert_{name}.pending.json")
                write_pending_cert(
                    name, rule, first_indep_tier[:2], first_indep_tier[2],
                    first_indep, pending)
                print(f"[dj33] {name}: pending cert {pending} "
                      f"(unnamed until verifier CONFIRMED)", flush=True)
                ok, rc, vout = verify_cert(pending)
                verify_out = {"returncode": rc, "confirmed": ok,
                              "output": vout}
                vrec = {"type": "verify", "preset": name,
                        "pending": os.path.basename(pending), **verify_out}
                log.write(json.dumps(vrec, ensure_ascii=False) + "\n")
                log.flush()
                print(vout, flush=True)
                if ok:
                    named = os.path.join(HERE, f"dj33cert_{name}.json")
                    os.replace(pending, named)
                    cert_path = os.path.relpath(named, HERE)
                    print(f"[dj33] {name}: NAMED {cert_path} "
                          f"after independent CONFIRMED", flush=True)
                else:
                    print(f"[dj33] {name}: verifier REJECTED; "
                          f"leaving {pending} unnamed", flush=True)
                    cert_path = None

            rec = {
                "type": "summary",
                "preset": name,
                "computed_for": name,
                "wolfram": a["wolfram"],
                "arity": arity,
                "rule": a["rule_json"],
                "q5_binary_matches": q5_match,
                "used_ternary_fallback": used_fallback,
                "tier_reason": tier_reason,
                "tiers": [[tv, te, tar] for tv, te, tar in tiers],
                "D-IA": dia_yes,
                "R1_independent_collision": r1_yes and cert_path is not None,
                "R1_found_but_unnamed": r1_yes and cert_path is None,
                "f_min_rigid": fmin_rigid,
                "tier": "+".join(
                    f"({tv},{te},arity={tar})" for tv, te, tar in tiers),
                "cert_path_or_none": cert_path or "none",
                "dia_pairs": [d["pairs"] for d in dia_records],
                "fmin_independent_counts": [
                    f["n_independent"] for f in fmin_records],
            }
            log.write(json.dumps(rec, ensure_ascii=False) + "\n")
            log.flush()
            rows.append(rec)
            rule_cache[key] = rec

    print()
    hdr = (f"{'preset':<12}{'D-IA':<8}{'R1_indep':<10}"
           f"{'f_min_rigid':<14}{'tier':<36}{'cert'}")
    print(hdr)
    print("-" * len(hdr))
    for r in rows:
        print(f"{r['preset']:<12}{str(r['D-IA']):<8}"
              f"{str(r['R1_independent_collision']):<10}"
              f"{str(r['f_min_rigid']):<14}"
              f"{r['tier']:<36}{r['cert_path_or_none']}")
    print(f"\n[dj33] results: {out}")
    print("[dj33] evidence label: BOUNDED COMPUTATION")


if __name__ == "__main__":
    main()
