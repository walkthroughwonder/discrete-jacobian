(* SpliceAeon.wl
   Exhaustive information-loss measurement for the splice rule
   {{a,a},{b,c}} -> {{a,b},{c,a}}  (discrete Jacobian program, CCC follow-up)
   Repo: https://github.com/walkthroughwonder/discrete-jacobian
   Discussion: https://community.wolfram.com/t/28448
*)

(* Canonical form: brute force over permutations within vertex classes of
   equal (out-degree, in-degree, loop count). Valid canonical form. *)
spliceCanon[st_List] := Module[{vs, sig, cls, perms, cands},
  If[st === {}, Return[{}]];
  vs = Union @@ st;
  sig = Association[# -> {Count[st, {#, x_} /; x =!= #],
        Count[st, {x_, #} /; x =!= #], Count[st, {#, #}]} & /@ vs];
  cls = GatherBy[SortBy[vs, sig], sig];
  perms = Tuples[Permutations /@ cls];
  cands = Table[With[{m = AssociationThread[Flatten[p], Range[0, Length[vs] - 1]]},
      Sort[st /. m]], {p, perms}];
  First[Sort[cands]]];

spliceRelabel[st_] := With[{m = AssociationThread[Union @@ st,
      Range[0, Length[Union @@ st] - 1]]}, Sort[st /. m]];

(* All one-step successors, as canonical forms (all matches, no policy) *)
spliceSuccessors[st_] := Union@Flatten[Table[
     If[st[[i, 1]] == st[[i, 2]] && j != i && Length[Union[{st[[i, 1]]}, st[[j]]]] == 3,
      {spliceCanon@spliceRelabel@Join[Delete[st, {{i}, {j}}],
          {{st[[i, 1]], st[[j, 1]]}, {st[[j, 2]], st[[i, 1]]}}]}, {}],
     {i, Length[st]}, {j, Length[st]}], 2];

(* Every state (binary edges, loops and multi-edges allowed) with 0..maxE edges *)
spliceStateLayers[maxE_] := NestList[Function[prev, Union@Flatten[Table[
       With[{n = Length[Union @@ Append[s, {}]]},
        Table[spliceCanon@spliceRelabel@Append[s, {x, y}], {x, 0, n + 1}, {y, 0, n + 1}]],
       {s, prev}], 2]], {{}}, maxE];

(* Deterministic evolution: min-successor policy, run until no match remains *)
spliceEndpoint[s_] := NestWhile[First@Sort@spliceSuccessors[#] &, s,
   spliceSuccessors[#] =!= {} &];

entropyBits[c_] := With[{p = N[c/Total[c]]}, -Total[p Log2[p]]];

(* Bits of the initial state not recoverable from the terminal state,
   per (E, V) sector, over all states with at least one loop *)
spliceInformationLoss[maxE_] := Module[{layers = spliceStateLayers[maxE]},
  Flatten[Table[
    With[{act = Select[layers[[e + 1]],
         Count[#, {a_, a_}] > 0 && Length[Union @@ #] == v &]},
     If[act === {}, Nothing,
      With[{f = Values@Counts[spliceEndpoint /@ act]},
       <|"E" -> e, "V" -> v, "StatesWithLoop" -> Length[act],
        "Endpoints" -> Length[f], "MaxFiber" -> Max[f],
        "BitsLost" -> Round[Log2[N@Length[act]] - entropyBits[f], 0.001]|>]]],
    {e, 1, maxE}, {v, 1, 2 e}], 1]];

loopCount[s_] := Count[s, {a_, a_}];
