"""Sanity suite: the machinery must not manufacture collisions where rigidity
is obvious, and the D1 probe must classify the planted rules correctly."""
from core import canonical, is_d1, undo_at_comatch_ok
from search import enumerate_states, find_r1_collisions

REVERSAL = ((("x", "y"),), (("y", "x"),))   # D1: involutive relabel-free swap
DELETE = ((("x", "y"),), ())                # non-D1: erases edge content

states = enumerate_states(4, 3)
print(f"{len(states)} states enumerated (<=4 vertices, <=3 binary edges)")

# 1. Edge reversal: expect ZERO genuine collisions; orbit artifacts allowed
#    (reversal makes S <-> T orbits and the policy collapses them — this is
#    exactly degenerate-collision class 4 in DEFINITIONS.md, discovered live
#    by this suite's first run on 2026-07-26).
_, collisions, artifacts = find_r1_collisions([REVERSAL])
print(f"reversal rule: genuine={len(collisions)} (expect 0), "
      f"orbit artifacts={len(artifacts)} (expected >0)")
assert not collisions, "false positive: invertible rule produced a genuine collision"
assert artifacts, "expected orbit artifacts under reversal; guard untested"

# 2. D1 classification is syntactic: reversal D1, delete non-D1.
assert is_d1(REVERSAL) and not is_d1(DELETE)
print("D1 syntactic classification: PASS (reversal D1, delete non-D1)")

# 3. DPO undoability fact: EVERY rule (even non-D1 delete) is undoable at its
#    own comatch when full match data is retained. This is the machinery
#    self-test AND the theory point: reversibility is free at the match;
#    the program's content lives in what the RESULT forgets.
for rule, name in [(REVERSAL, "reversal"), (DELETE, "delete")]:
    bad = [s for s in states if not undo_at_comatch_ok(s, rule)]
    print(f"undo-at-comatch ({name}): {len(bad)} failures (expect 0)")
    assert not bad

# 3. Canonical-form soundness spot check: relabeled states collapse.
a = ((0, 1), (1, 2))
b = ((5, 3), (3, 9))
assert canonical(a) == canonical(b)
print("canonical-form spot check: PASS")

print("ALL SANITY CHECKS PASSED")
