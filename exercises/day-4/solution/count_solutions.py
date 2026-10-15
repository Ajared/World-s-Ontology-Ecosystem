"""Brute-force count of Zebra Puzzle arrangements consistent with each clue stage.

Used only to check what an abductive guess could justify at each stage (see ai-log.md).
Run: python3 count_solutions.py  (takes a few minutes)
"""
from itertools import permutations
from collections import Counter
H=range(5)
N=["Englishman","Spaniard","Ukrainian","Norwegian","Japanese"]
def nxt(a,b): return abs(a-b)==1
stages={1:range(2,6),2:range(2,9),3:range(2,12),4:range(2,16)}
def ok(c,n,p,d,s,k):
    E,Sp,U,No,J=n; R,G,I,Y,B=c; Co,T,M,O,W=d; Dg,Sn,Fx,Hr,Z=p; OG,K,Ch,LS,P=s
    t={2:E==R,3:Sp==Dg,4:Co==G,5:U==T,6:G==I+1,7:OG==Sn,8:K==Y,9:M==2,10:No==0,11:nxt(Ch,Fx),12:nxt(K,Hr),13:LS==O,14:J==P,15:nxt(No,B)}
    return all(t[i] for i in k)
for st,k in stages.items():
    cnt=Counter(); tot=0
    P=list(permutations(H))
    for c in P:
      if 6 in k and c[1]!=c[2]+1: continue
      for n in P:
        if 2 in k and n[0]!=c[0]: continue
        if 10 in k and n[3]!=0: continue
        if 15 in k and not nxt(n[3],c[4]): continue
        for d in P:
          if not ok(c,n,(0,)*5,d,(0,)*5,[i for i in k if i in (4,5,9,10)]): continue
          for s in P:
            if not ok(c,n,(0,)*5,d,s,[i for i in k if i in (8,13,14)]): continue
            for p in P:
              if ok(c,n,p,d,s,k):
                tot+=1; z=p[4]; cnt[N[n.index(z)]]+=1
    print(st,tot,{x:round(cnt[x]/tot,3) for x in N})
