(* Increment Mismatch TV -- FIXED 2026-10-31, fast version of the Phase 1 port.
   Same selection rule, verdict and output as the original notebook, with two changes:
   1. writer lookup uses Key[...] (Lookup on a list key threads, which made every depth 0);
   2. all candidate matches are found per event with one vectorized comparison
      instead of a scalar loop over all ordered pairs (the original exceeded the
      cloud time limit). Candidates are kept in the original (i1, i2) order, and
      ties on the sort key go to the first candidate, as SortBy did.
   Two-t mid=50 large=149. Not unique-3, not HOLD lift, never CLAIM_3. MATCH no. *)
tvDepth[rewrote_List, mismatch_List] := Module[{cr, cm, keys, nr, nm},
  If[rewrote === {} || mismatch === {}, Return[Missing[]]];
  cr = Counts[rewrote]; cm = Counts[mismatch];
  keys = Union[Keys[cr], Keys[cm]];
  nr = N@Length[rewrote]; nm = N@Length[mismatch];
  0.5*Total[Abs[Lookup[cr, #, 0]/nr - Lookup[cm, #, 0]/nm] & /@ keys]];

(* candidate ordered pairs {i1, i2} of edge positions matching the two-edge LHS
   injectively, in the original enumeration order *)
matchPairs[edges_List, lhs_List] := Module[{v, cols, nE, ok, s, t, a, b, d, c},
  v = Flatten[lhs]; nE = Length[edges];
  cols = {edges[[All, 1]], edges[[All, 2]]};
  ok = 1 - IdentityMatrix[nE]; (* i1 != i2 *)
  Do[
    a = cols[[If[s <= 2, s, s - 2]]]; b = cols[[If[t <= 2, t, t - 2]]];
    (* slots with the same variable must agree, different variables must differ *)
    d = Which[
      s <= 2 && t <= 2, Transpose[ConstantArray[a - b, nE]],  (* both slots in edge i1: depends on row *)
      s >= 3, ConstantArray[a - b, nE],                         (* both slots in edge i2: depends on column *)
      True, Outer[Subtract, a, b]];                            (* slot s in edge i1, slot t in edge i2 *)
    c = Unitize[d];
    ok = ok * If[v[[s]] === v[[t]], 1 - c, c],
    {s, 1, 4}, {t, s + 1, 4}];
  Position[ok, 1]];

matchPick2[edges_List, lhs_List, edgeWriter_Association, eventDepths_List] := Module[
  {pairs, wr, w1, w2, mx, mn, deps, cons, keys, best, k, i1, i2, m},
  pairs = matchPairs[edges, lhs];
  If[pairs === {}, Return[<|"ok" -> False|>]];
  wr = Lookup[edgeWriter, Key /@ edges, -1];
  w1 = wr[[pairs[[All, 1]]]]; w2 = wr[[pairs[[All, 2]]]];
  mx = MapThread[Max, {w1, w2}]; mn = MapThread[Min, {w1, w2}];
  deps = MapThread[If[#1 < 0 && #2 < 0, 0, 1 + Max[eventDepths[[Select[{#1, #2}, NonNegative] + 1]]]] &, {w1, w2}];
  cons = Map[Sort[{edges[[#[[1]]]], edges[[#[[2]]]]}] &, pairs];
  keys = MapThread[Join[{#1, #2}, Flatten[#3]] &, {mx, mn, cons}];
  best = First[MinimalBy[Range[Length[keys]], keys[[#]] &]]; (* first of the minimal keys *)
  {i1, i2} = pairs[[best]];
  m = AssociationThread[Flatten[lhs] -> Join[edges[[i1]], edges[[i2]]]];
  <|"ok" -> True, "mismatchDepths" -> deps,
    "pick" -> {keys[[best]], m, {edges[[i1]], edges[[i2]]}, deps[[best]], {}}|>];

runSeqTV[lhs_List, rhs_List, init_List, n_Integer] := Module[
  {edges = init, edgeWriter, events = {}, tvByT = <||>, mmN = <||>, pack, m, consumed, depth, eid,
   remaining, maxv, nm, newP, pLhs, pRhs, added},
  edgeWriter = Association@Thread[edges -> -1];
  pLhs = Union @@ lhs; pRhs = Union @@ rhs; newP = Sort[Complement[pRhs, pLhs]];
  Do[
    pack = matchPick2[edges, lhs, edgeWriter, events];
    If[! TrueQ[pack["ok"]], Break[]];
    m = pack["pick"][[2]]; consumed = pack["pick"][[3]]; depth = pack["pick"][[4]];
    eid = Length[events]; AppendTo[events, depth];
    tvByT[t] = tvDepth[{depth}, pack["mismatchDepths"]];
    mmN[t] = Length[pack["mismatchDepths"]];
    remaining = edges;
    Scan[(remaining = DeleteCases[remaining, #, {1}, 1]) &, consumed];
    maxv = Max[Flatten[edges]]; nm = m;
    Scan[(maxv++; nm[#] = maxv) &, newP];
    added = (nm /@ #) & /@ rhs;
    Scan[KeyDropFrom[edgeWriter, Key[#]] &, consumed];
    Scan[(edgeWriter[#] = eid) &, added];
    edges = Join[remaining, added];
    , {t, 0, n - 1}];
  <|"n" -> Length[events], "tvByT" -> tvByT, "mmN" -> mmN|>];

dimLHS = {{x, y}, {x, z}}; dimRHS = {{x, z}, {x, w}, {y, w}, {z, w}}; dimInit = {{1, 2}, {1, 3}};
chainLHS = {{x, y}, {y, z}}; chainRHS = {{w, y}, {y, x}, {x, w}, {w, z}}; chainInit = {{0, 1}, {1, 2}, {2, 3}, {3, 0}};
n = 150; midT = 50; largeT = 149;
dimS = runSeqTV[dimLHS, dimRHS, dimInit, n];
chainS = runSeqTV[chainLHS, chainRHS, chainInit, n];
sharedOK = dimS["n"] > largeT && chainS["n"] > largeT &&
  KeyExistsQ[dimS["tvByT"], midT] && KeyExistsQ[chainS["tvByT"], midT] &&
  KeyExistsQ[dimS["tvByT"], largeT] && KeyExistsQ[chainS["tvByT"], largeT];
tdM = If[sharedOK, dimS["tvByT"][midT], Missing[]];
tcM = If[sharedOK, chainS["tvByT"][midT], Missing[]];
tdL = If[sharedOK, dimS["tvByT"][largeT], Missing[]];
tcL = If[sharedOK, chainS["tvByT"][largeT], Missing[]];
held = sharedOK && tdM < tcM && tdL < tcL;
failReason = Which[
  ! sharedOK, "no shared t",
  tdM < tcM && ! (tdL < tcL), "dim27 only wins mid window (two-t fail)",
  ! held, "dim27 TV not strictly below chain27 at required t",
  True, None];
<|
  "idea" -> "Increment Mismatch TV", "phase" -> 1, "fixed" -> "2026-10-31: Key[] lookup, vectorized matching",
  "mid_t" -> midT, "large_t" -> largeT,
  "TV_at" -> <|"mid" -> <|"dim27" -> tdM, "chain27" -> tcM|>,
             "large" -> <|"dim27" -> tdL, "chain27" -> tcL|>|>,
  "held" -> held, "fail_reason" -> failReason,
  "claim_3" -> False, "hold" -> "HOLD", "match" -> "no",
  "local_ref" -> <|"mid" -> {50, 0.9935483870967742, 0.5527638190954773},
                  "large" -> {149, 0.8490196078431372, 0.297979797979798},
                  "held" -> False|>
|>
