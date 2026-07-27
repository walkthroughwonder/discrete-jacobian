"""N4: classify the R2 multiway merges. N5: test the history-ambiguity
predictor against the colliding/rigid split of the 238 survivors.

History ambiguity (rule-level, probed): there exist a probe state S, a match
m with result T, and a reverse-match in T whose SUPPORT differs from the
comatch region, yielding a predecessor not isomorphic to S. Intuition: the
image can be 'read back' along a different history — the splice mechanism.
"""
import json
from core import (canonical, matches, apply_rule, apply_rule_traced,
                  reverse_rule, f_min)
from search import enumerate_states


def history_ambiguity(rule, probes):
    rev = reverse_rule(rule)
    for s in probes:
        cs = canonical(s)
        for m in matches(s, rule):
            result, (co_idx, _) = apply_rule_traced(s, rule, m)
            for m2 in matches(result, rev):
                if set(m2[0]) == set(co_idx):
                    continue  # same support: the honest undo
                pred = canonical(apply_rule(result, rev, m2))
                if pred != cs:
                    return True
    return False


def main():
    probes = enumerate_states(4, 3)

    # ---- N5 ----
    rules = []
    for line in open('maxsweep_log.jsonl'):
        rec = json.loads(line)
        if rec.get('stage') == 1 and rec.get('status') == 'swept':
            rule = tuple(tuple(tuple(e) for e in side) for side in rec['rule'])
            rules.append((rule, rec.get('genuine', 0) > 0))

    tp = fp = fn = tn = 0
    fn_rules, fp_rules = [], []
    for rule, collides in rules:
        pred = history_ambiguity(rule, probes)
        if pred and collides:
            tp += 1
        elif pred and not collides:
            fp += 1
            fp_rules.append(rule)
        elif not pred and collides:
            fn += 1
            fn_rules.append(rule)
        else:
            tn += 1
    print("=== N5: history-ambiguity predictor vs actual collision ===")
    print(f"true positive  (predicted & collides): {tp}")
    print(f"false positive (predicted, rigid in range): {fp}")
    print(f"false negative (not predicted, collides): {fn}")
    print(f"true negative: {tn}")
    for r in fn_rules[:5]:
        print(f"  FN example: {r}")
    for r in fp_rules[:5]:
        print(f"  FP example: {r}")

    # ---- N4 ----
    one_step = deeper = 0
    for line in open('maxsweep_log.jsonl'):
        rec = json.loads(line)
        if rec.get('stage') != 3 or not rec.get('r2_merges'):
            continue
        rules_ = [tuple(tuple(tuple(e) for e in side) for side in r)
                  for r in rec['rules']]
        for ex in rec.get('examples', []):
            s = tuple(tuple(e) for e in ex['s'])
            t = tuple(tuple(e) for e in ex['t'])
            i1, i2 = f_min(s, rules_), f_min(t, rules_)
            if i1 is not None and i1 == i2:
                one_step += 1
            else:
                deeper += 1
    print("\n=== N4: R2 merge examples ===")
    print(f"explained by one-step R1 collision: {one_step}")
    print(f"deeper (multi-step) merges: {deeper}")


if __name__ == "__main__":
    main()
