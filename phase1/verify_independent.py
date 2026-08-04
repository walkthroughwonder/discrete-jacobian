"""INDEPENDENT verifier for R1 collision certificates.

Deliberately shares no code with core.py/search.py. Reimplements from scratch:
string-encoded states, permutation-minimal canonical form, its own matcher and
rule application, and full (not min-only) successor enumeration to recompute
the policy. If this script and the searcher agree, the claim survives two
implementations; if they disagree, the certificate is rejected.

Usage: python verify_independent.py cert.json
"""
import json
import sys
from itertools import permutations


def canon(edges):
    """Canonical string of a state: try every relabeling, keep the smallest."""
    edges = [tuple(e) for e in edges]
    vs = sorted({v for e in edges for v in e})
    if not vs:
        return "empty"
    best = None
    for p in permutations(range(len(vs))):
        m = {v: p[i] for i, v in enumerate(vs)}
        relabeled = sorted(tuple(m[v] for v in e) for e in edges)
        s = ";".join(",".join(map(str, e)) for e in relabeled)
        if best is None or s < best:
            best = s
    return best


def _self_test():
    """Unit tests for canon itself — added after the double-relabeling bug
    (2026-07-26) slipped past a round-trip test that passed by coincidence."""
    assert canon([(0, 1), (1, 2)]) == canon([(5, 3), (3, 9)])
    assert canon([(0, 0), (0, 1)]) != canon([(0, 0), (1, 0)])
    assert canon([(2, 2)]) == "0,0"
    assert canon([(7, 4)]) == "0,1"


_self_test()


def all_matches(edges, lhs):
    """Injective variable bindings mapping the LHS edge multiset into edges."""
    results = []

    def go(k, used, bind):
        if k == len(lhs):
            results.append((tuple(used), dict(bind)))
            return
        for j, e in enumerate(edges):
            if j in used or len(e) != len(lhs[k]):
                continue
            b = dict(bind)
            good = True
            for var, vert in zip(lhs[k], e):
                if var in b and b[var] != vert:
                    good = False
                    break
                if var not in b and vert in b.values():
                    good = False
                    break
                b[var] = vert
            if good:
                go(k + 1, used + (j,), b)

    go(0, (), {})
    return results


def one_step_images(edges, rules):
    """Canonical strings of every one-step successor under every rule/match."""
    images = set()
    for lhs, rhs in rules:
        for used, bind in all_matches(edges, lhs):
            rest = [e for j, e in enumerate(edges) if j not in used]
            b = dict(bind)
            nxt = max((v for e in edges for v in e), default=-1) + 1
            for var in sorted({v for e in rhs for v in e} - set(b)):
                b[var] = nxt
                nxt += 1
            new = [tuple(b[v] for v in e) for e in rhs]
            images.add(canon(rest + new))
    return images


def decode(canon_str):
    """Inverse of canon's string encoding: 'a,b;c,d' -> [(a,b),(c,d)]."""
    if canon_str == "empty":
        return []
    return [tuple(int(x) for x in part.split(","))
            for part in canon_str.split(";")]


def bounded_unreachable(src, dst_canon, rules, max_states, max_verts):
    """True iff dst is NOT reached from src by BFS within the stated bounds.
    Independent reimplementation (expands via one_step_images + decode);
    a True answer is bounds-relative, exactly as documented in the cert."""
    src_c = canon(src)
    if src_c == dst_canon:
        return False
    seen = {src_c}
    frontier = [src]
    while frontier and len(seen) < max_states:
        nxt = []
        for st in frontier:
            if len({v for e in st for v in e}) > max_verts:
                continue
            for img in one_step_images(st, rules):
                if img == dst_canon:
                    return False
                if img not in seen:
                    seen.add(img)
                    nxt.append(decode(img))
        frontier = nxt
    return True


def verify_r2(cert):
    """Independently replay an R2-deep-merge path certificate: every step of
    both paths must be a legal one-step image, endpoints must meet at the
    witness, and the seeds must be canonically distinct. (Reachability
    separation of the seeds is NOT checked here — it is bounds-relative and
    documented inside the certificate.)"""
    rules = [(tuple(tuple(e) for e in lhs), tuple(tuple(e) for e in rhs))
             for lhs, rhs in cert["rules"]]
    p1 = [[tuple(e) for e in st] for st in cert["path1"]]
    p2 = [[tuple(e) for e in st] for st in cert["path2"]]
    checks = []
    checks.append(("seeds distinct", canon(p1[0]) != canon(p2[0])))
    checks.append(("path1 starts at seed1",
                   canon(p1[0]) == canon([tuple(e) for e in cert["seed1"]])))
    checks.append(("path2 starts at seed2",
                   canon(p2[0]) == canon([tuple(e) for e in cert["seed2"]])))
    for name, p in (("path1", p1), ("path2", p2)):
        ok = all(canon(p[i + 1]) in one_step_images(p[i], rules)
                 for i in range(len(p) - 1))
        checks.append((f"{name} steps all legal ({len(p)-1} steps)", ok))
        checks.append((f"{name} has >=2 steps", len(p) >= 3))
    w = canon([tuple(e) for e in cert["witness"]])
    checks.append(("path1 ends at witness", canon(p1[-1]) == w))
    checks.append(("path2 ends at witness", canon(p2[-1]) == w))
    ok = all(passed for _, passed in checks)
    for name, passed in checks:
        print(f"  [{'PASS' if passed else 'FAIL'}] {name}")
    print("VERDICT:", "CONFIRMED" if ok else "REJECTED")
    return 0 if ok else 1


def main(path):
    cert = json.load(open(path))
    if cert["kind"] == "R2-deep-merge":
        return verify_r2(cert)
    assert cert["kind"] == "R1-collision", "unknown certificate kind"
    policy = cert["policy"]
    assert policy in ("min-successor", "max-successor"), "unknown policy"
    pick = min if policy == "min-successor" else max
    rules = [(tuple(tuple(e) for e in lhs), tuple(tuple(e) for e in rhs))
             for lhs, rhs in cert["rules"]]
    s1 = [tuple(e) for e in cert["state1"]]
    s2 = [tuple(e) for e in cert["state2"]]

    checks = []

    c1, c2 = canon(s1), canon(s2)
    checks.append(("states are distinct (canonically)", c1 != c2))

    im1, im2 = one_step_images(s1, rules), one_step_images(s2, rules)
    checks.append(("state1 has successors", bool(im1)))
    checks.append(("state2 has successors", bool(im2)))
    f1 = pick(im1) if im1 else None
    f2 = pick(im2) if im2 else None
    checks.append((f"policy images agree ({policy})",
                   f1 == f2 and f1 is not None))

    claimed = canon([tuple(e) for e in cert["claimed_image"]])
    checks.append(("claimed image matches recomputation", f1 == claimed))

    if "independence_bounds" in cert:
        b = cert["independence_bounds"]
        ms, mv = int(b["max_states"]), int(b["max_verts"])
        checks.append((f"state2 unreachable from state1 (bounds {ms},{mv})",
                       bounded_unreachable(s1, c2, rules, ms, mv)))
        checks.append((f"state1 unreachable from state2 (bounds {ms},{mv})",
                       bounded_unreachable(s2, c1, rules, ms, mv)))

    ok = all(passed for _, passed in checks)
    for name, passed in checks:
        print(f"  [{'PASS' if passed else 'FAIL'}] {name}")
    print("VERDICT:", "CONFIRMED" if ok else "REJECTED")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))
