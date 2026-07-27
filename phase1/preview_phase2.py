"""Phase 2 preview: R1 collision search over a few hand-picked D1 rule sets.
Bounded sweep — results are 'rigid up to (4 vertices, 3 edges)' claims only."""
from core import is_d1
from search import find_r1_collisions

SYSTEMS = {
    "reversal": [((("x", "y"),), (("y", "x"),))],
    "duplication": [((("x", "y"),), (("x", "y"), ("x", "y")))],
    "pendant-creation": [((("x", "y"),), (("x", "y"), ("y", "z")))],
    "chain-step": [((("x", "y"), ("y", "z")), (("x", "z"), ("y", "z")))],
    "rev+dup": [((("x", "y"),), (("y", "x"),)),
                ((("x", "y"),), (("x", "y"), ("x", "y")))],
}

for name, rules in SYSTEMS.items():
    assert all(is_d1(r) for r in rules), f"{name}: not a D1 system"
    states, genuine, artifacts = find_r1_collisions(rules, max_vertices=4, max_edges=3)
    tag = "COLLISION CANDIDATE" if genuine else "rigid in range"
    print(f"{name:18s} genuine={len(genuine):2d} artifacts={len(artifacts):2d}  -> {tag}")
    for img, pre in sorted(genuine.items())[:3]:
        print(f"    image {img}")
        for s in pre[:3]:
            print(f"      <- {s}")
