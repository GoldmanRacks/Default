"""RWS V6: staged, multi-sleeve long-convexity book for Oct 5 - Nov 25, 2026.
Prices every leg by Black-Scholes (r = 4%, q = 0) at the implied vol backed out of the Oct 2 mid; later tranches are priced at their entry date
with spot unchanged (indicative). Cases are vol-normalized per leg over its own hold. Writes model_out_v6.json."""
import json, math
from datetime import date
from math import log, sqrt, exp
from statistics import NormalDist, stdev, mean
from quotes_v6 import spot, hv30, NOV, DEC, DEC_PUT
ND=NormalDist(); N=ND.cdf; n=ND.pdf; R=0.04; BOOK=5000
TODAY=date(2026,10,2); NOVX=date(2026,11,20); DECX=date(2026,12,18)
wc=json.load(open("weekly_closes.json"))
def days(a,b): return (b-a).days
def bs(S,K,T,iv,cp=1):
    if T<=0: return max(cp*(S-K),0.0)
    d1=(log(S/K)+(R+.5*iv*iv)*T)/(iv*sqrt(T)); d2=d1-iv*sqrt(T)
    return cp*(S*N(cp*d1)-K*exp(-R*T)*N(cp*d2))
def greeks(S,K,T,iv,cp=1):
    d1=(log(S/K)+(R+.5*iv*iv)*T)/(iv*sqrt(T)); d2=d1-iv*sqrt(T)
    delta=N(d1) if cp==1 else N(d1)-1
    gamma=n(d1)/(S*iv*sqrt(T)); vega=S*n(d1)*sqrt(T)/100
    theta=(-S*n(d1)*iv/(2*sqrt(T)) - cp*R*K*exp(-R*T)*N(cp*d2))/365
    return delta,gamma,vega,theta
def implied(S,K,T,px,cp=1):
    lo,hi=0.01,4.0
    for _ in range(80):
        m=(lo+hi)/2
        if bs(S,K,T,m,cp)<px: lo=m
        else: hi=m
    return (lo+hi)/2
def hv1y(tk):
    c=wc.get(tk)
    if not c or len(c)<10: return None
    lr=[log(c[i+1]/c[i]) for i in range(len(c)-1)][-52:]
    return stdev(lr)*sqrt(52)
def mom13(tk):
    c=wc.get(tk); return (c[-1]/c[-14]-1) if c and len(c)>14 else None
def backtest(tk, w, sig):
    c=wc.get(tk)
    if not c or len(c)<=w+2: return None
    f=[c[i+w]/c[i]-1 for i in range(len(c)-w)]
    return dict(n=len(f), w=w, mean=mean(f), med=sorted(f)[len(f)//2], mx=max(f), mn=min(f),
                h1=sum(x>=sig for x in f)/len(f), h2=sum(x>=2*sig for x in f)/len(f), h3=sum(x>=3*sig for x in f)/len(f), hneg=sum(x<=-2*sig for x in f)/len(f))

TR={"T1":dict(entry=date(2026,10,5), exit=date(2026,11,16), exp=NOVX, label="Tranche 1: Oct 5-9, Nov 20 expiry"),
    "T2":dict(entry=date(2026,10,22), exit=date(2026,11,25), exp=DECX, label="Tranche 2: Oct 22-23, Dec 18 expiry"),
    "T3":dict(entry=date(2026,11,5), exit=date(2026,11,25), exp=DECX, label="Tranche 3: Nov 5-6, Dec 18 expiry")}
CASES=["Flat","Base","Bull","Gamma","Shock"]

def quote(tk,K,exp,cp=1):
    book = (NOV if exp==NOVX else DEC) if cp==1 else DEC_PUT
    for k,b,a,oi in book[tk]:
        if k==K: return b,a,oi
    raise KeyError((tk,K,exp,cp))

def make_leg(tk,K,tranche,n_=1,cp=1,sleeve="",why="",entry_override=None):
    t=TR[tranche]; b,a,oi=quote(tk,K,t["exp"],cp); mid=(a+b)/2; S=spot[tk]
    T_today=days(TODAY,t["exp"])/365; iv=implied(S,K,T_today,mid,cp)
    entry=entry_override or t["entry"]; Te=days(entry,t["exp"])/365; Tx=days(t["exit"],t["exp"])/365; hold=days(entry,t["exit"])
    px=bs(S,K,Te,iv,cp); d,g,v,th=greeks(S,K,Te,iv,cp); sig=iv*sqrt(hold/365)
    moves={"Flat":(0.0,0.0),"Base":(sig,0.0),"Bull":(2*sig,0.0),"Gamma":(3*sig,0.0),"Shock":(-2*sig,0.10)}
    pnl={c:(bs(S*(1+m),K,Tx,iv+dv,cp)-px)*100 for c,(m,dv) in moves.items()}
    stand={"Flat":0.0,"Base":0.18,"Bull":0.18+sig,"Gamma":0.18+2*sig}
    spnl={c:(bs(S*(1+m),K,Tx,iv,cp)-px)*100 for c,m in stand.items()}
    hv=hv1y(tk) or hv30.get(tk); w=max(1,round(hold/7))
    return dict(tk=tk,K=K,cp="C" if cp==1 else "P",tranche=tranche,n=n_,sleeve=sleeve,why=why,exp=t["exp"].isoformat(),entry=entry.isoformat(),exit=t["exit"].isoformat(),
                hold=hold,dte_entry=round(Te*365),dte_exit=round(Tx*365),spot=S,bid=b,ask=a,mid=mid,oi=oi,spread=(a-b)/mid if a>b else None,iv=iv,hv=hv,ivhv=(iv/hv if hv else None),
                px=px,cost=px*100,delta=d,gamma=g,gamma_per_100=g*S*S/100/(px*100)*100,  # gamma in $ P&L per 1% move squared, per $100 premium
                vega=v,theta=th,sig=sig,moves={c:m for c,(m,_) in moves.items()},pnl=pnl,spnl=spnl,mom13=mom13(tk),bt=backtest(tk,w,sig))

PRIMARY=[
 ("GLD",405,"T1",1,1,"Gold / real-asset","Gold IV 21% below 24% realized; defies 5%+ yields; Iran, Hormuz; no dated event in window"),
 ("GDX",98,"T1",2,1,"Gold / real-asset","Miners as gold beta with 42% IV; cheapest ticket in the book; 13-week momentum +11%"),
 ("NVDA",255,"T1",1,1,"Memory / AI compute","Deepest market in the book; reports Nov 18, after the exit; 13-week momentum +19%"),
 ("RTX",200,"T2",2,1,"Defense / geopolitics","Bought after the Oct 20 print; record backlog, munitions ramp; post-midterm Iran escalation optionality"),
 ("VRT",300,"T2",1,1,"AI power / grid","Bought after the Oct 21 print and a 25% drawdown; pipeline 'stronger and stronger'; 65% IV ~ realized"),
 ("SPY",700,"T2",1,-1,"Crash convexity","Dec put at 13% IV covers FOMC Oct 28, midterms Nov 3 and resumed Iran strikes; funded by the cash the staging saves"),
 ("SKHY",230,"T3",2,1,"Memory / AI compute","Bought after FOMC and midterms and after SK hynix's late-October print; HBM 2027 sold out at higher prices"),
 ("DRAM",70,"T3",2,1,"Memory / AI compute","Diversified memory basket (MU is its largest holding) in place of a single MU contract, which would be 43-57% of the book"),
 ("BA",215,"T3",1,1,"Defense / geopolitics","Bought after the Oct 27 print, after the midterms; 15% 13-week drawdown; 38% IV near realized"),
]
MU_VARIANT=[PRIMARY[0],PRIMARY[1],PRIMARY[2],PRIMARY[3],PRIMARY[5],("MU",1350,"T3",1,1,"Memory / AI compute","Single MU anchor, single-name cap waived; bought after FOMC and the midterms, three weeks before the December print")]

def build(spec, front=False):
    legs=[]
    for tk,K,tr,nn,cp,sl,why in spec:
        legs.append(make_leg(tk,K,tr,nn,cp,sl,why, entry_override=(TR["T1"]["entry"] if front else None)))
    dep=sum(l["cost"]*l["n"] for l in legs)
    out=dict(legs=legs,deployed=dep,cash=BOOK-dep,scen={},stand={})
    for c in CASES:
        p=sum(l["pnl"][c]*l["n"] for l in legs); out["scen"][c]=dict(pnl=p,end=BOOK+p,ret=p/BOOK)
    for c in ["Flat","Base","Bull","Gamma"]:
        p=sum(l["spnl"][c]*l["n"] for l in legs); out["stand"][c]=dict(pnl=p,ret=p/BOOK)
    # sleeves
    sl={}
    for l in legs: sl[l["sleeve"]]=sl.get(l["sleeve"],0)+l["cost"]*l["n"]
    out["sleeves"]=sl
    # risk-by-date schedule: premium at risk and book theta/day on each calendar date
    sched=[]
    for lab,d in [("Oct 5 entry T1",date(2026,10,5)),("Oct 14 CPI",date(2026,10,14)),("Oct 20-22 RTX/VRT/LMT prints",date(2026,10,21)),("Oct 22 entry T2",date(2026,10,22)),
                  ("Oct 28 FOMC",date(2026,10,28)),("Nov 3 midterms",date(2026,11,3)),("Nov 5 entry T3",date(2026,11,5)),("Nov 16 exit T1",date(2026,11,16)),("Nov 25 exit T2/T3",date(2026,11,25))]:
        held=[l for l in legs if date.fromisoformat(l["entry"])<=d<=date.fromisoformat(l["exit"])]
        prem=sum(l["cost"]*l["n"] for l in held)
        th=sum(greeks(l["spot"],l["K"],max(days(d,date.fromisoformat(l["exp"])),1)/365,l["iv"],1 if l["cp"]=="C" else -1)[3]*100*l["n"] for l in held)
        sched.append(dict(label=lab,date=d.isoformat(),premium=prem,pct=prem/BOOK,theta=th,n=len(held)))
    out["schedule"]=sched
    # flat re-rate at the two exit marks
    rr={}
    for lab,d in [("Nov 16",date(2026,11,16)),("Nov 25",date(2026,11,25))]:
        held=[l for l in legs if date.fromisoformat(l["exit"])>=d]
        def bv(dv): return sum(bs(l["spot"],l["K"],max(days(d,date.fromisoformat(l["exp"])),0)/365,l["iv"]+dv,1 if l["cp"]=="C" else -1)*100*l["n"] for l in held)
        depd=sum(l["cost"]*l["n"] for l in held); row=dict(flat_ret=(bv(0)-depd)/BOOK, held=len(held), deployed=depd)
        for tgt in (0.05,0.10):
            lo,hi=0.0,3.0
            if (bv(hi)-depd)/BOOK<tgt: row[f"dvol_{int(tgt*100)}"]=None; continue
            for _ in range(60):
                m=(lo+hi)/2
                if (bv(m)-depd)/BOOK<tgt: lo=m
                else: hi=m
            row[f"dvol_{int(tgt*100)}"]=(lo+hi)/2
        rr[lab]=row
    out["rerate"]=rr
    return out

def screen():
    """Every quoted contract scored on the V6 rules at its tranche's entry date."""
    rows=[]
    for exp,book,cp in [(NOVX,NOV,1),(DECX,DEC,1),(DECX,DEC_PUT,-1)]:
        for tk,lst in book.items():
            for K,b,a,oi in lst:
                mid=(a+b)/2; S=spot[tk]; T_today=days(TODAY,exp)/365; iv=implied(S,K,T_today,mid,cp)
                tr="T1" if exp==NOVX else "T2"; t=TR[tr]; Te=days(t["entry"],exp)/365; px=bs(S,K,Te,iv,cp); d,g,v,th=greeks(S,K,Te,iv,cp)
                hv=hv1y(tk) or hv30.get(tk); sp=(a-b)/mid if a>b else None
                fails=[]
                if oi<500: fails.append("OI<500")
                if sp is not None and sp>0.25: fails.append("spread>25%")
                if cp==1 and not (0.18<=d<=0.40): fails.append("delta")
                if cp==-1 and not (0.08<=-d<=0.22): fails.append("delta")
                if px*100>0.25*BOOK: fails.append("ticket>25%")
                if cp==1 and hv and iv/hv>1.25: fails.append("IV/HV>1.25")
                rows.append(dict(tk=tk,K=K,cp="C" if cp==1 else "P",exp=exp.isoformat(),mid=mid,oi=oi,spread=sp,iv=iv,hv=hv,ivhv=(iv/hv if hv else None),delta=d,px=px,cost=px*100,
                                 gamma_per_100=g*S*S/100/(px*100)*100,fails=fails,mom13=mom13(tk)))
    return rows

if __name__=="__main__":
    res={"primary":build(PRIMARY),"mu_variant":build(MU_VARIANT),"front_loaded":build(PRIMARY,front=True),"screen":screen(),
         "tranches":{k:dict(label=v["label"],entry=v["entry"].isoformat(),exit=v["exit"].isoformat(),exp=v["exp"].isoformat()) for k,v in TR.items()}}
    json.dump(res,open("model_out_v6.json","w"),indent=1,default=str)
    for name in ["primary","mu_variant","front_loaded"]:
        o=res[name]; print("==",name,"deployed",round(o["deployed"]),"cash",round(o["cash"]))
        for l in o["legs"]:
            print(f"  {l['tranche']} {l['tk']:5}{l['K']}{l['cp']} mid {l['mid']:.2f} iv {l['iv']:.1%} hv {l['hv'] or 0:.1%} entry {l['px']:.2f} (${l['cost']:.0f}) d {l['delta']:+.3f} g/$100 {l['gamma_per_100']:.3f} sig {l['sig']:.1%} oi {l['oi']} sp {l['spread'] if l['spread'] is None else round(l['spread'],3)} "
                  f"| F {l['pnl']['Flat']:+.0f} B {l['pnl']['Base']:+.0f} Bu {l['pnl']['Bull']:+.0f} G {l['pnl']['Gamma']:+.0f} S {l['pnl']['Shock']:+.0f} | bt {l['bt'] and (l['bt']['n'], round(l['bt']['h1'],2), round(l['bt']['h2'],2), round(l['bt']['h3'],2))}")
        print("  scen",{c:f"{o['scen'][c]['ret']:+.1%}" for c in CASES},"stand",{c:f"{o['stand'][c]['ret']:+.1%}" for c in o["stand"]})
        print("  sleeves",{k:round(v) for k,v in o["sleeves"].items()})
        for s in o["schedule"]: print(f"   {s['label']:32} ${s['premium']:>6,.0f} {s['pct']:5.0%} theta/day {s['theta']:+.0f} legs {s['n']}")
        print("  rerate",{k:{kk:(round(vv,3) if isinstance(vv,float) else vv) for kk,vv in v.items()} for k,v in o["rerate"].items()})
    print("\n== screen (passing)")
    for r in sorted(res["screen"], key=lambda r:(-r["gamma_per_100"])):
        if not r["fails"]: print(f"  {r['tk']:5}{r['K']}{r['cp']} {r['exp'][5:]} cost ${r['cost']:.0f} d {r['delta']:+.2f} iv {r['iv']:.0%} ivhv {r['ivhv'] and round(r['ivhv'],2)} g/$100 {r['gamma_per_100']:.3f} oi {r['oi']} mom {r['mom13'] and round(r['mom13'],2)}")
    print("== screen (failing, by name)")
    for r in res["screen"]:
        if r["fails"]: print(f"  {r['tk']:5}{r['K']}{r['cp']} {r['exp'][5:]} ${r['cost']:.0f} d {r['delta']:+.2f} {r['fails']}")
