import sys, math, json
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from collections import Counter, defaultdict
from ccc_compression import all_states, succ, loops, nverts, entropy_bits
def fmin_end(s):
    while True:
        n = succ(s)
        if not n: return s
        s = min(n)
if __name__ == '__main__':
  L = all_states(6)
  for e in range(3,7):
      sec = defaultdict(list)
      for s in L[e]:
          if loops(s)>0: sec[nverts(s)].append(s)
      for v in sorted(sec):
          st = sec[v]; f = Counter(fmin_end(s) for s in st)
          print(json.dumps(dict(E=e,V=v,active=len(st),endpoints=len(f),max_fiber=max(f.values()),bits_lost=round(math.log2(len(st))-entropy_bits(list(f.values())),3))))
