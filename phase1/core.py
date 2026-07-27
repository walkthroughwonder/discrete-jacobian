"""Core engine: states, canonical forms, rules, matching, application, policies.

State = tuple of edges; edge = tuple of vertex ints (ordered, Wolfram-style).
Multisets are represented by repetition. Vertices exist iff they appear in
some edge. All collision claims are made on canonical forms only.
"""
from functools import lru_cache
from itertools import permutations


# ---------- states ----------

def vertices(state):
    return sorted({v for e in state for v in e})


def normalize(state):
    """Relabel vertices by first appearance in the sorted edge list; sort edges."""
    state = tuple(sorted(tuple(e) for e in state))
    mapping = {}
    for e in state:
        for v in e:
            if v not in mapping:
                mapping[v] = len(mapping)
    return tuple(sorted(tuple(mapping[v] for v in e) for e in state))


@lru_cache(maxsize=1 << 20)
def canonical(state):
    """Minimum over all vertex relabelings of the sorted edge tuple.

    Brute force (|V|! permutations) — correct by construction; fine for |V|<=7.
    """
    vs = vertices(state)
    if not vs:
        return ()
    best = None
    for perm in permutations(range(len(vs))):
        mapping = dict(zip(vs, perm))
        cand = tuple(sorted(tuple(mapping[v] for v in e) for e in state))
        if best is None or cand < best:
            best = cand
    return best


# ---------- rules ----------
# A rule is (lhs, rhs): tuples of edges over string variables.
# Matching binds variables injectively to state vertices; LHS edges must be
# present as a sub-multiset. RHS variables absent from LHS become fresh
# vertices. LHS variables absent from RHS are deleted (their other incident
# edges, if any, simply remain — vertices exist only through edges).


def rule_vars(side):
    return {v for e in side for v in e}


def matches(state, rule):
    """All (edge_indices, binding) for rule's LHS in state.

    edge_indices: tuple of distinct indices into state, one per LHS edge.
    binding: dict var -> vertex, injective.
    """
    lhs, _ = rule
    out = []

    def rec(i, used, binding):
        if i == len(lhs):
            out.append((tuple(used), dict(binding)))
            return
        patt = lhs[i]
        for j, e in enumerate(state):
            if j in used or len(e) != len(patt):
                continue
            b = dict(binding)
            ok = True
            for pv, sv in zip(patt, e):
                if pv in b:
                    if b[pv] != sv:
                        ok = False
                        break
                else:
                    if sv in b.values():  # injectivity
                        ok = False
                        break
                    b[pv] = sv
            if ok:
                rec(i + 1, used + [j], b)

    rec(0, [], {})
    return out


def apply_rule(state, rule, match):
    """Apply rule at match; returns normalized successor state."""
    lhs, rhs = rule
    idxs, binding = match
    keep = [e for j, e in enumerate(state) if j not in idxs]
    binding = dict(binding)
    fresh = max([v for e in state for v in e], default=-1) + 1
    for var in sorted(rule_vars(rhs) - set(binding)):
        binding[var] = fresh
        fresh += 1
    new = [tuple(binding[v] for v in e) for e in rhs]
    return normalize(tuple(keep) + tuple(new))


def successors(state, rules):
    """Canonical forms of all one-step successors, deduplicated."""
    out = set()
    for rule in rules:
        for m in matches(state, rule):
            out.add(canonical(apply_rule(state, rule, m)))
    return out


def f_min(state, rules):
    """Min-successor policy: isomorphism-invariant by construction.

    Returns the lexicographically minimal canonical successor, or None.
    """
    succ = successors(state, rules)
    return min(succ) if succ else None


# ---------- rule-level reversibility (D1, empirical operationalization) ----------

def reverse_rule(rule):
    lhs, rhs = rule
    return (rhs, lhs)


def is_d1(rule):
    """Syntactic D1 criterion: no matched variable is forgotten.

    vars(LHS) ⊆ vars(RHS): every vertex the rule touches remains addressable
    in the result, so the application is undoable from (result, comatch)
    without smuggling in deleted content. Delete ({x,y} -> {}) and endpoint
    merge ({x,y} -> {x,x}) fail; reversal and creation pass.

    NOTE (DPO fact, verified by undo_at_comatch_ok below): EVERY rule is
    undoable at its own comatch if you retain the full match data. D1 is not
    about that — it is about what the *result* remembers. This is the
    discrete monodromy at the heart of the program.
    """
    lhs, rhs = rule
    return rule_vars(lhs) <= rule_vars(rhs)


def apply_rule_traced(state, rule, match):
    """Like apply_rule but unnormalized, returning (result, comatch) where
    comatch = (indices of the RHS-created edges in result, extended binding)."""
    lhs, rhs = rule
    idxs, binding = match
    keep = [e for j, e in enumerate(state) if j not in idxs]
    binding = dict(binding)
    fresh = max([v for e in state for v in e], default=-1) + 1
    for var in sorted(rule_vars(rhs) - set(binding)):
        binding[var] = fresh
        fresh += 1
    new = [tuple(binding[v] for v in e) for e in rhs]
    result = tuple(keep) + tuple(new)
    comatch = (tuple(range(len(keep), len(result))), binding)
    return result, comatch


def semantic_d1_violation(state, rule):
    """Semantic D1 (result-side uniqueness), probed at one state.

    For each application, look at the result and the comatch REGION (the edge
    set the application produced) and ask: how many distinct predecessors
    arise from reverse-matches supported on exactly that region? If more than
    one, the result+boundary does not determine the history: the application
    is locally ambiguous even though the syntactic D1 check passes.
    (Discovered necessary by the chain-step candidate, 2026-07-26.)

    Returns an offending match or None.
    """
    rev = reverse_rule(rule)
    for m in matches(state, rule):
        result, (co_idx, _) = apply_rule_traced(state, rule, m)
        preds = set()
        for m2 in matches(result, rev):
            if set(m2[0]) == set(co_idx):
                preds.add(canonical(apply_rule(result, rev, m2)))
        if len(preds) > 1:
            return m
    return None


def undo_at_comatch_ok(state, rule):
    """Machinery self-test of the DPO undoability fact: for every match, the
    reverse rule applied at the exact comatch (with full retained binding)
    recovers the original state. Should hold for ALL rules."""
    c0 = canonical(state)
    rev = reverse_rule(rule)
    for m in matches(state, rule):
        result, comatch = apply_rule_traced(state, rule, m)
        if canonical(apply_rule(result, rev, comatch)) != c0:
            return False
    return True
