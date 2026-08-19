#!/usr/bin/env python3
"""TLP ST_PRESETS integer patterns → Discrete Jacobian rule encoding.

IDEA-DJ-33-WPP-DIA adapter. Hypergraph spacetime presets only (the seven
ST_PRESETS entries). The 21 string PRESETS in the same TLP index.html are
not loaded and have no encoding here.

ATOM / PORT CONVENTION
----------------------
TLP encodes a Wolfram-model rule as two lists of integer tuples:

  lhs / rhs : list of edges; each edge is a list of integer *ports*.
  The same integer in lhs and rhs is the same pattern variable (glueing).
  Integers that occur only on the rhs are fresh vertices under DJ
  application (core.py: vars(RHS) \\ vars(LHS) get new vertex ids).

Letter names (the printed Wolfram form used in TLP comments, and the
string variables core.py binds injectively):

  If every port is in {0,1,2,3}  (binary 2_2→3_2 / 2_2→4_2 family):
      0→x, 1→y, 2→z, 3→w
  If every port is in {0,1,2,3,4,5} (ternary family, try3d / sierpinski):
      0→x, 1→y, 2→z, 3→u, 4→v, 5→w

These two tables are exactly the names TLP prints next to the integer
patterns in index.html (blob 36070e4f18a7). They are *not* the same map
at port 3: binary comments write 3 as w; ternary comments write 3 as u.

DJ matching is core.matches: injective port→vertex binding, edge-multiset
inclusion of the LHS. TLP inits are recorded for provenance and are NOT
fed to the D-IA / f_min census (the census is all canonical states at a
tier, as in search.enumerate_states / Q5). In particular sierpinski's
TLP seed {{0,0,0}} is a non-injective loop and would not match {{x,y,z}}
under core.matches; that is a seed fact, not a rule-encoding fact.

Provenance of the seven patterns: walkthroughwonder/topological-light-
propagation@c60aed3eb08d index.html blob 36070e4f18a7, object
`const ST_PRESETS`. Slice committed as dj33_st_presets.json. Fetched via
GitHub API; TLP was not cloned.

Round-trip tests (dim27, chain27) check wolfram_form(adapt(lhs,rhs))
equals the comment printed in TLP.
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
SLICE_PATH = os.path.join(HERE, "dj33_st_presets.json")

# Binary four-port family (dim27, chain27, flat2d, doubleslit, singleslit).
ATOMS_BINARY_4 = {0: "x", 1: "y", 2: "z", 3: "w"}
# Ternary six-port family (try3d, sierpinski).
ATOMS_TERNARY_6 = {0: "x", 1: "y", 2: "z", 3: "u", 4: "v", 5: "w"}

PRESET_ORDER = (
    "dim27", "chain27", "flat2d", "try3d",
    "sierpinski", "doubleslit", "singleslit",
)

PRINTED_WOLFRAM = {
    "dim27": "{{x,y},{x,z}}→{{x,z},{x,w},{y,w},{z,w}}",
    "chain27": "{{x,y},{y,z}}→{{w,y},{y,x},{x,w},{w,z}}",
    "flat2d": "{{x,y},{y,z}}→{{x,z},{z,w},{w,x},{w,y}}",
    "try3d": "{{x,y,z},{u,y,v}}→{{w,z,x},{z,w,u},{x,y,w}}",
    "sierpinski": "{{x,y,z}}→{{x,u,w},{y,v,u},{z,w,v}}",
    "doubleslit": "{{x,y},{y,z}}→{{x,z},{z,w},{w,x},{w,y}}",
    "singleslit": "{{x,y},{y,z}}→{{x,z},{z,w},{w,x},{w,y}}",
}


def load_st_presets(path=None):
    """Load the pinned ST_PRESETS hypergraph slice. Never reads string PRESETS."""
    path = path or SLICE_PATH
    with open(path) as fh:
        blob = json.load(fh)
    presets = blob["presets"]
    missing = [k for k in PRESET_ORDER if k not in presets]
    if missing:
        raise ValueError(f"ST_PRESETS slice missing {missing}")
    extra = set(presets) - set(PRESET_ORDER)
    if extra:
        raise ValueError(f"unexpected keys in ST_PRESETS slice: {extra}")
    return blob


def atom_table(lhs, rhs):
    """Return the port→letter table for a TLP integer pattern pair."""
    ports = {p for edge in list(lhs) + list(rhs) for p in edge}
    if not ports:
        raise ValueError("empty pattern")
    mx = max(ports)
    if ports <= set(ATOMS_BINARY_4) and mx <= 3:
        return ATOMS_BINARY_4
    if ports <= set(ATOMS_TERNARY_6) and mx <= 5:
        return ATOMS_TERNARY_6
    raise ValueError(f"no atom table for ports {sorted(ports)}")


def arity_of(lhs, rhs):
    arities = {len(e) for e in list(lhs) + list(rhs)}
    if len(arities) != 1:
        raise ValueError(f"mixed arities {arities}")
    return arities.pop()


def pattern_to_rule(lhs, rhs):
    """Integer TLP pattern → DJ rule ((lhs edges of str vars), (rhs ...)).

    Returns a core.py rule: tuple-of-tuple-of-str on each side.
    """
    table = atom_table(lhs, rhs)
    def conv(side):
        return tuple(tuple(table[p] for p in edge) for edge in side)
    return (conv(lhs), conv(rhs))


def rule_to_json(rule):
    return [[list(e) for e in side] for side in rule]


def wolfram_form(rule):
    """Print a DJ rule in the TLP comment Wolfram form, no spaces."""
    def side(edges):
        inner = ",".join("{" + ",".join(e) + "}" for e in edges)
        return "{" + inner + "}"
    lhs, rhs = rule
    return f"{side(lhs)}→{side(rhs)}"


def adapt_preset(name, presets=None):
    """Return dict with DJ rule, arity, wolfram string, json encoding."""
    if presets is None:
        presets = load_st_presets()["presets"]
    p = presets[name]
    rule = pattern_to_rule(p["lhs"], p["rhs"])
    return {
        "preset": name,
        "label": p.get("label"),
        "rule": rule,
        "rule_json": rule_to_json(rule),
        "arity": arity_of(p["lhs"], p["rhs"]),
        "wolfram": wolfram_form(rule),
        "lhs_int": p["lhs"],
        "rhs_int": p["rhs"],
        "same_rule_as": p.get("same_rule_as"),
    }


def all_adapted():
    blob = load_st_presets()
    return blob, [adapt_preset(n, blob["presets"]) for n in PRESET_ORDER]


def run_adapter_tests():
    """dim27 and chain27 round-trip to the printed Wolfram form; extras check."""
    blob, adapted = all_adapted()
    by_name = {a["preset"]: a for a in adapted}
    failures = []
    for name in ("dim27", "chain27"):
        got = by_name[name]["wolfram"]
        want = PRINTED_WOLFRAM[name]
        if got != want:
            failures.append(f"{name}: got {got!r} want {want!r}")
        # also equals the slice's recorded printed form when present
        slice_print = blob["presets"][name].get("printed_wolfram")
        if slice_print and got != slice_print:
            failures.append(f"{name}: adapter {got!r} != slice {slice_print!r}")
    # sanity: all seven print, arities, doubleslit/singleslit share flat2d
    for a in adapted:
        if a["wolfram"] != PRINTED_WOLFRAM[a["preset"]]:
            failures.append(f"{a['preset']}: wolfram {a['wolfram']!r} "
                            f"!= {PRINTED_WOLFRAM[a['preset']]!r}")
    if by_name["doubleslit"]["rule"] != by_name["flat2d"]["rule"]:
        failures.append("doubleslit rule != flat2d rule")
    if by_name["singleslit"]["rule"] != by_name["flat2d"]["rule"]:
        failures.append("singleslit rule != flat2d rule")
    if by_name["dim27"]["arity"] != 2 or by_name["try3d"]["arity"] != 3:
        failures.append("arity misread")
    # hypergraph-only guard: every edge is a list of ints, never a char string
    for name, p in blob["presets"].items():
        for edge in p["lhs"] + p["rhs"]:
            if not edge or not all(isinstance(x, int) for x in edge):
                failures.append(f"{name}: non-integer port in {edge!r}")
    if failures:
        raise AssertionError("adapter tests FAILED:\n  " + "\n  ".join(failures))
    return {
        "ok": True,
        "dim27": by_name["dim27"]["wolfram"],
        "chain27": by_name["chain27"]["wolfram"],
        "n_presets": len(adapted),
    }


if __name__ == "__main__":
    rec = run_adapter_tests()
    print("adapter tests PASS")
    print(f"  dim27    {rec['dim27']}")
    print(f"  chain27  {rec['chain27']}")
    _, adapted = all_adapted()
    for a in adapted:
        print(f"  {a['preset']:<12} arity={a['arity']}  {a['wolfram']}")
