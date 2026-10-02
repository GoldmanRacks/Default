"""V5 optimizer: integer allocation of Nov 20 '26 calls maximizing the equal-weighted mean P&L across Flat / Base / Bull / Gamma Upside,
marked Nov 16 '26 (4 DTE) at entry IV, under a $5,000 budget. Group knapsack over names with per-name premium cap and MU required."""
import json, itertools, sys
from math import log, sqrt, exp
from statistics import NormalDist
from candidates import spot, cands
N=NormalDist().cdf; R=0.04; T0=46/365; T1=4/365; TH=42/365; BOOK=5000
def bs(S,K,T,iv):
    if T<=0: return max(S-K,0.0)
    d1=(log(S/K)+(R+.5*iv*iv)*T)/(iv*sqrt(T)); return S*N(d1)-K*exp(-R*T)*N(d1-iv*sqrt(T))
def delta(S,K,T,iv): return N((log(S/K)+(R+.5*iv*iv)*T)/(iv*sqrt(T)))
CASES=[("Flat",0.0),("Base",None),("Bull",1),("Gamma",2)]
def case_moves(iv, scheme="standing"):
    sig=iv*sqrt(TH)
    if scheme=="standing": return {"Flat":0.0,"Base":0.18,"Bull":0.18+sig,"Gamma":0.18+2*sig}
    return {"Flat":0.0,"Base":sig,"Bull":2*sig,"Gamma":3*sig}          # vol-normalized: +1/+2/+3 s.d. per name
def contract_rows(exclude=("DRAM",), floor=0.20, min_oi=500, require=("MU",), scheme="standing"):
    rows=[]
    for tk,lst in cands.items():
        if tk in exclude: continue
        for K,mid,iv,oi in lst:
            d=delta(spot[tk],K,T0,iv)
            if d<floor or oi<min_oi: continue
            cost=mid*100; pnl={}; mvs=case_moves(iv, scheme)
            for name,_ in CASES:
                pnl[name]=bs(spot[tk]*(1+mvs[name]),K,T1,iv)*100-cost
            rows.append(dict(tk=tk,K=K,mid=mid,iv=iv,oi=oi,delta=d,cost=cost,pnl=pnl,obj=sum(pnl.values())/4))
    return rows
def optimize(rows, budget=BOOK, cap=0.35, require=("MU",), weights=None, unit=5, require_max=1):
    """Group knapsack: per name enumerate contract combos within cap, DP across names on budget (in $unit steps)."""
    W=weights or {"Flat":.25,"Base":.25,"Bull":.25,"Gamma":.25}
    val=lambda r: sum(W[c]*r["pnl"][c] for c in W)
    names=sorted(set(r["tk"] for r in rows)); capd=cap*budget
    groups={}
    for tk in names:
        its=[r for r in rows if r["tk"]==tk]; opts={}
        tcap = budget if tk in require else capd            # the required anchor is exempt from the single-name cap, limited to require_max contracts
        maxn=[(require_max if tk in require else int(tcap//r["cost"])) for r in its]
        for combo in itertools.product(*[range(m+1) for m in maxn]):
            c=sum(n*r["cost"] for n,r in zip(combo,its))
            if c>tcap or (tk in require and not (1<=sum(combo)<=require_max)): continue
            v=sum(n*val(r) for n,r in zip(combo,its)); key=-(-int(round(c))//unit)   # ceil: never exceed the budget
            if key not in opts or v>opts[key][0]: opts[key]=(v,combo)
        if tk not in require: opts.setdefault(0,(0.0,tuple(0 for _ in its)))
        groups[tk]=(its,opts)
    B=int(budget//unit); NEG=-1e18
    dp=[NEG]*(B+1); dp[0]=0.0; choice=[dict() for _ in range(B+1)]
    for tk in names:
        its,opts=groups[tk]; nd=[NEG]*(B+1); nc=[None]*(B+1)
        for b in range(B+1):
            if dp[b]==NEG: continue
            for k,(v,combo) in opts.items():
                if b+k<=B and dp[b]+v>nd[b+k]: nd[b+k]=dp[b]+v; nc[b+k]=(b,combo)
        # backtrack bookkeeping
        newchoice=[None]*(B+1)
        for b in range(B+1):
            if nc[b] is not None:
                pb,combo=nc[b]; d=dict(choice[pb]); d[tk]=combo; newchoice[b]=d
        dp=nd; choice=[c if c is not None else {} for c in newchoice]
    best=max(range(B+1), key=lambda b: dp[b]); sel=choice[best]
    legs=[]
    for tk,combo in sel.items():
        its=groups[tk][0]
        for n,r in zip(combo,its):
            if n>0: legs.append(dict(r, n=n))
    return legs, dp[best]
def summarize(legs):
    dep=sum(l["cost"]*l["n"] for l in legs); out={"deployed":dep,"cash":BOOK-dep,"legs":legs,"scen":{}}
    for name,_ in CASES:
        tot=sum(l["pnl"][name]*l["n"] for l in legs); out["scen"][name]=dict(pnl=tot,end=BOOK+tot,ret=tot/BOOK)
    out["obj"]=sum(out["scen"][c]["pnl"] for c,_ in CASES)/4
    return out
if __name__=="__main__":
    res={}
    rows=contract_rows()                                   # standing rules: 0.20 floor, OI>=500, DRAM excluded, MU required
    legs,_=optimize(rows, cap=0.35); res["primary"]=summarize(legs)
    legs,_=optimize(rows, cap=1.0);  res["nocap"]=summarize(legs)        # no single-name cap
    rows2=contract_rows(floor=0.0, min_oi=0)                              # no floor, no liquidity filter
    legs,_=optimize(rows2, cap=1.0); res["unconstrained"]=summarize(legs)
    legs,_=optimize(rows, cap=0.35, weights={"Flat":0,"Base":1/3,"Bull":1/3,"Gamma":1/3}); res["exflat"]=summarize(legs)
    rows3=contract_rows(scheme="normalized")
    legs,_=optimize(rows3, cap=0.35); res["normalized"]=summarize(legs)
    # re-mark the primary book on the normalized ladder and the normalized book on the standing ladder for comparison
    def remark(legs, scheme):
        out={}
        for name,_ in CASES:
            out[name]=sum((bs(spot[l["tk"]]*(1+case_moves(l["iv"],scheme)[name]),l["K"],T1,l["iv"])*100-l["cost"])*l["n"] for l in legs)/BOOK
        return out
    res["primary"]["normalized_ret"]=remark(res["primary"]["legs"],"normalized")
    res["normalized"]["standing_ret"]=remark(res["normalized"]["legs"],"standing")
    # flat-spot vol re-rate for the primary and normalized books
    def rerate(legs):
        out={}
        for lab,dte in [("Oct 23 (28 DTE)",28),("Oct 30 (21 DTE)",21),("Nov 6 (14 DTE)",14),("Nov 16 (4 DTE)",4)]:
            def bv(dv): return sum(bs(spot[l["tk"]],l["K"],dte/365,l["iv"]+dv)*100*l["n"] for l in legs)
            dep=sum(l["cost"]*l["n"] for l in legs); row={"dte":dte,"flat_ret":(bv(0)-dep)/BOOK}
            for tgt in (0.05,0.10):
                lo,hi=0.0,3.0
                if (bv(hi)-dep)/BOOK<tgt: row[f"dvol_{int(tgt*100)}"]=None; continue
                for _ in range(60):
                    mid=(lo+hi)/2
                    if (bv(mid)-dep)/BOOK<tgt: lo=mid
                    else: hi=mid
                row[f"dvol_{int(tgt*100)}"]=(lo+hi)/2
            out[lab]=row
        return out
    res["primary"]["flat_rerate"]=rerate(res["primary"]["legs"]); res["normalized"]["flat_rerate"]=rerate(res["normalized"]["legs"])
    res["universe"]=[dict(r, pnl=r["pnl"]) for r in rows]
    json.dump(res, open("model_out_v5.json","w"), indent=1)
    for k in ["primary","nocap","unconstrained","exflat","normalized"]:
        o=res[k]; print("==",k, "deployed",round(o["deployed"]),"obj",round(o["obj"]))
        for l in o["legs"]: print(f"   {l['tk']:5}{l['K']}C x{l['n']} cost {l['cost']*l['n']:,.0f} d={l['delta']:.3f} oi={l['oi']} pnl F/B/Bu/G {l['pnl']['Flat']*l['n']:+,.0f}/{l['pnl']['Base']*l['n']:+,.0f}/{l['pnl']['Bull']*l['n']:+,.0f}/{l['pnl']['Gamma']*l['n']:+,.0f}")
        print("   ", {c:f"{o['scen'][c]['ret']:+.0%}" for c in o["scen"]})
