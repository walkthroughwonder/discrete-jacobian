#!/usr/bin/env python3
"""Independent replay checker for IDEA-DJ-33 (adversarial re-verification).

Reads dj33_results.jsonl ONLY (never dj33_wpp_dia.py internals). Recomputes
from recorded states using core.py:

  1. Adapter round-trip: dim27 and chain27 print the TLP Wolfram form
     (via dj33_adapter, which is encoding, not the searcher).
  2. For each summary row, if a D-IA example is on the jsonl dia line,
     recompute: T is a successor of S; replay T in successors(P); S ≇ P;
     equal-|E| grower independence.
  3. For each fmin line with an independent example, recompute f_min(s1)
     == f_min(s2) == claimed image, canonical distinctness, grower
     independence (equal edge count ⇒ mutually unreachable).
  4. Re-run unmodified verify_independent.py on any *named* cert
     (searcher ≠ verifier; this is a second verifier pass).

Appends nothing to the jsonl.
"""
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import core
from dj33_adapter import PRINTED_WOLFRAM, all_adapted, run_adapter_tests, wolfram_form

JSONL = os.path.join(HERE, "dj33_results.jsonl")
REPORT = os.path.join(HERE, "dj33_replay_report.txt")
VERIFY = os.path.join(HERE, "verify_independent.py")


def load(path):
    header, dia, fmin, summaries, verifies = None, [], [], [], []
    with open(path) as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            d = json.loads(line)
            t = d.get("type")
            if t == "header":
                header = d
            elif t == "dia":
                dia.append(d)
            elif t == "fmin":
                fmin.append(d)
            elif t == "summary":
                summaries.append(d)
            elif t == "verify":
                verifies.append(d)
    return header, dia, fmin, summaries, verifies


def as_state(edges):
    return tuple(tuple(e) for e in edges)


def as_rule(rule_json):
    lhs, rhs = rule_json
    return (tuple(tuple(e) for e in lhs), tuple(tuple(e) for e in rhs))


def net_delta(rule):
    return len(rule[1]) - len(rule[0])


def main():
    jsonl = sys.argv[1] if len(sys.argv) > 1 else JSONL
    report_path = sys.argv[2] if len(sys.argv) > 2 else REPORT
    header, dia, fmin, summaries, verifies = load(jsonl)
    lines = []
    lines.append("IDEA-DJ-33 independent replay (dj33_replay.py)")
    lines.append(f"jsonl: {jsonl}")
    lines.append("searcher was dj33_wpp_dia.py; this file does not import it.")
    lines.append("verifier: unmodified phase1/verify_independent.py "
                 "(blob 4bade5643b9e)")
    lines.append("evidence label: BOUNDED COMPUTATION")
    lines.append("")

    overall_ok = True

    # 1. adapter
    try:
        rec = run_adapter_tests()
        lines.append(f"adapter tests PASS dim27={rec['dim27']}")
        lines.append(f"                 chain27={rec['chain27']}")
    except AssertionError as e:
        overall_ok = False
        lines.append(f"adapter tests FAIL: {e}")
    _, adapted = all_adapted()
    by = {a["preset"]: a for a in adapted}
    for name in ("dim27", "chain27"):
        got = wolfram_form(by[name]["rule"])
        want = PRINTED_WOLFRAM[name]
        if got != want:
            overall_ok = False
            lines.append(f"  round-trip FAIL {name}: {got!r} != {want!r}")
        else:
            lines.append(f"  round-trip OK {name}: {got}")
    lines.append("")

    if header:
        lines.append(f"header experiment={header.get('experiment')} "
                     f"label={header.get('evidence_label')}")
        lines.append(f"summary rows: {len(summaries)}")
    lines.append("")

    # 2. D-IA examples
    for d in dia:
        preset, tier = d["preset"], tuple(d["tier"])
        rule = by[preset]["rule"]
        lines.append(f"=== D-IA {preset} tier{tier} arity={d.get('arity')} "
                     f"ia={d.get('ia')} pairs={d.get('pairs')} ===")
        ex = d.get("example_ia")
        if not d.get("ia"):
            if ex:
                overall_ok = False
                lines.append("  DISPUTED: ia=false but example_ia present")
            else:
                lines.append("  no D-IA example (ia=false); nothing to replay")
            continue
        if not ex:
            overall_ok = False
            lines.append("  DISPUTED: ia=true but no example_ia")
            continue
        s = core.canonical(as_state(ex["S"]))
        p = core.canonical(as_state(ex["pred"]))
        t = core.canonical(as_state(ex["T"]))
        problems = []
        if s == p:
            problems.append("S canonically equals pred")
        succs = core.successors(s, [rule])
        if t not in succs:
            problems.append("T is not a successor of S")
        succp = core.successors(p, [rule])
        if t not in succp:
            problems.append("T is not a successor of pred (not replayable)")
        if net_delta(rule) > 0 and len(s) == len(p):
            # grower equal-|E|: independent
            pass
        else:
            problems.append("example is not an equal-|E| grower pair; "
                            "replay does not re-run the searcher's BFS")
        if problems:
            overall_ok = False
            lines.append("  DISPUTED: " + "; ".join(problems))
        else:
            lines.append("  replayed example (S, pred, T): successor+replay+"
                         "distinct+equal-|E| grower independent: OK")
    lines.append("")

    # 3. f_min examples
    for f in fmin:
        preset, tier = f["preset"], tuple(f["tier"])
        rule = by[preset]["rule"]
        lines.append(f"=== f_min {preset} tier{tier} arity={f.get('arity')} "
                     f"indep={f.get('n_independent')} "
                     f"match={f.get('n_match')} ===")
        ex = f.get("example_independent")
        if f.get("n_independent", 0) == 0:
            if ex:
                overall_ok = False
                lines.append("  DISPUTED: n_independent=0 but example present")
            else:
                lines.append("  rigid at this tier (no independent example)")
            continue
        if not ex:
            overall_ok = False
            lines.append("  DISPUTED: n_independent>0 but no example")
            continue
        s1 = core.canonical(as_state(ex["s1"]))
        s2 = core.canonical(as_state(ex["s2"]))
        img = core.canonical(as_state(ex["image"]))
        problems = []
        if s1 == s2:
            problems.append("s1 canonically equals s2")
        f1, f2 = core.f_min(s1, [rule]), core.f_min(s2, [rule])
        if f1 != f2:
            problems.append(f"f_min images disagree {f1} vs {f2}")
        if f1 != img:
            problems.append(f"claimed image {img} != recomputed {f1}")
        if net_delta(rule) > 0 and len(s1) == len(s2):
            pass
        elif net_delta(rule) > 0:
            # unequal |E|: replay records the searcher's how, does not BFS
            lines.append(f"  note: unequal |E| pair how={ex.get('how')}; "
                         "independence is the searcher's BFS stamp")
        else:
            problems.append("non-grower pair in replay")
        if problems:
            overall_ok = False
            lines.append("  DISPUTED: " + "; ".join(problems))
        else:
            lines.append("  replayed independent pair: f_min images agree, "
                         "states distinct: OK")
    lines.append("")

    # 4. named certs through the independent verifier
    named = []
    for s in summaries:
        p = s.get("cert_path_or_none")
        if p and p != "none":
            named.append((s["preset"], p))
    # unique paths
    seen = set()
    uniq = []
    for preset, p in named:
        if p not in seen:
            seen.add(p)
            uniq.append((preset, p))
    lines.append(f"named certs: {len(uniq)}")
    for preset, rel in uniq:
        path = rel if os.path.isabs(rel) else os.path.join(HERE, rel)
        lines.append(f"=== verifier {preset} {rel} ===")
        proc = subprocess.run(
            [sys.executable, VERIFY, path],
            cwd=HERE, capture_output=True, text=True,
        )
        out = proc.stdout or ""
        lines.append(out.rstrip())
        if proc.returncode != 0 or "VERDICT: CONFIRMED" not in out:
            overall_ok = False
            lines.append("  DISPUTED: verifier did not CONFIRMED")
        else:
            lines.append("  VERDICT: CONFIRMED (second pass)")
    lines.append("")

    # 5. seven-row shape
    if len(summaries) != 7:
        overall_ok = False
        lines.append(f"DISPUTED: expected 7 summary rows, got {len(summaries)}")
    else:
        lines.append("seven summary rows present")
    wanted = ["dim27", "chain27", "flat2d", "try3d", "sierpinski",
              "doubleslit", "singleslit"]
    got = [s["preset"] for s in summaries]
    if got != wanted:
        overall_ok = False
        lines.append(f"DISPUTED: preset order {got} != {wanted}")

    lines.append("")
    lines.append("OVERALL: " + ("all checks CONFIRMED" if overall_ok
                                else "one or more checks DISPUTED"))
    report = "\n".join(lines) + "\n"
    with open(report_path, "w") as fh:
        fh.write(report)
    print(report)
    return 0 if overall_ok else 1


if __name__ == "__main__":
    sys.exit(main())
