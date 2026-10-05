"""RWS V6 at $1,500: same process as V6 (three tranches, event rule, vol-value / liquidity / delta screens, sleeve cap), with the ticket cap scaled to 25% of $1,500.
Exhaustive search: one line per name (1-2 contracts of one strike in one allowed tranche), maximizing the mean of the Base / Bull / Gamma Upside P&L
on the vol-normalized ladder. Writes model_out_v6_1500.json."""
import json, itertools
from datetime import date
import model_v6 as mv
from model_v6 import make_leg, build, TR, days, hv1y
BOOK=1500; TICKET=0.25*BOOK; LINE=0.30*BOOK; SLEEVE=0.40*BOOK; CASHMIN=0.08*BOOK
CAP_T1=0.30*BOOK; CAP_T12=0.62*BOOK; CAP_ALL=BOOK-CASHMIN
# Oct 5 live SPY quotes (spot 770.53) replace the Oct 2 put strikes
mv.spot["SPY"]=770.53
mv.DEC_PUT["SPY"]=[(690,4.08,4.10,11333),(695,4.40,4.42,13248)]
SPYQ=date(2026,10,5)
SLEEVES={"GLD":"Gold / real-asset","GDX":"Gold / real-asset","NVDA":"Memory / AI compute","DRAM":"Memory / AI compute","SKHY":"Memory / AI compute","INTC":"Memory / AI compute",
         "RTX":"Defense / geopolitics","BA":"Defense / geopolitics","SPY":"Crash convexity"}
EVENTS={"RTX":date(2026,10,20),"BA":date(2026,10,27),"NVDA":date(2026,11,18),"INTC":date(2026,10,22),"DRAM":date(2026,10,28),"SKHY":date(2026,10,28),
        "VRT":date(2026,10,21),"CEG":date(2026,11,6),"AMD":date(2026,11,3),"LMT":date(2026,10,22),"NOC":date(2026,10,20),"LHX":date(2026,10,29),"GEV":date(2026,10,21)}
WHY={"GDX":"Miners as gold beta; IV 0.85x realized; cheapest ticket in the screen; no dated event",
     "NVDA":"Deepest market; reports Nov 18, after the Nov 16 exit; 13-week momentum +19%",
     "GLD":"Gold IV 0.94x realized; no dated event; Iran / Hormuz and rates-stress hedge",
     "RTX":"Bought after the Oct 20 print; record backlog; post-midterm Iran optionality",
     "BA":"Bought after the Oct 27 print; 15% 13-week drawdown; IV ~1.1x realized",
     "DRAM":"Memory basket (MU largest holding); IV 0.76x realized; bought after SK hynix",
     "SPY":"Dec put at ~22% IV covers FOMC, midterms and resumed Iran strikes"}
def allowed(tk,tr):
    t=TR[tr]; ev=EVENTS.get(tk)
    return not (ev and t["entry"]<ev<=t["exit"])
def screen_ok(l):
    f=[]
    if l["oi"]<500: f.append("OI")
    if l["spread"] is not None and l["spread"]>0.25: f.append("spread")
    d=abs(l["delta"])
    if l["cp"]=="C" and not 0.18<=d<=0.40: f.append("delta")
    if l["cp"]=="P" and not 0.08<=d<=0.22: f.append("delta")
    if l["cost"]>TICKET: f.append("ticket")
    if l["cp"]=="C" and l["ivhv"] and l["ivhv"]>1.25: f.append("ivhv")
    return f
def universe():
    out=[]; rej=[]
    for tk in SLEEVES:
        for tr,exp,book,cp in [("T1",mv.NOVX,mv.NOV,1),("T2",mv.DECX,mv.DEC,1),("T3",mv.DECX,mv.DEC,1),("T2",mv.DECX,mv.DEC_PUT,-1)]:
            if tk not in book: continue
            if not allowed(tk,tr): rej.append((tk,tr,"event")); continue
            if cp==-1 and tk!="SPY": continue
            for K,b,a,oi in book[tk]:
                l=make_leg(tk,K,tr,1,cp,SLEEVES[tk],WHY.get(tk,""),qdate=(SPYQ if tk=="SPY" else None))
                f=screen_ok(l)
                if f: rej.append((tk,tr,f"{K}{l['cp']}:{','.join(f)}")); continue
                out.append(l)
    return out,rej
def val(l,n): return n*sum(l["pnl"][c] for c in ("Base","Bull","Gamma"))/3
def search(U,force=(),exclude=()):
    names=sorted(set(l["tk"] for l in U if l["tk"] not in exclude)); by={tk:[l for l in U if l["tk"]==tk] for tk in names}
    opts={}
    for tk in names:
        o=[None]
        for l in by[tk]:
            for n in (1,2):
                if l["cost"]*n<=LINE: o.append((l,n))
        opts[tk]=o
    best=None; cnt=0
    for combo in itertools.product(*[opts[tk] for tk in names]):
        lines=[c for c in combo if c]
        if len(lines)<4: continue
        if any(f not in [l["tk"] for l,_ in lines] for f in force): continue
        tr={"T1":0,"T2":0,"T3":0}
        for l,n in lines: tr[l["tranche"]]+=l["cost"]*n
        tot=sum(tr.values())
        if tr["T1"]>CAP_T1 or tr["T1"]+tr["T2"]>CAP_T12 or tot>CAP_ALL: continue
        sl={}
        for l,n in lines: sl[l["sleeve"]]=sl.get(l["sleeve"],0)+l["cost"]*n
        if max(sl.values())>SLEEVE: continue
        if len(sl)<3: continue
        cnt+=1; v=sum(val(l,n) for l,n in lines)
        if best is None or v>best[0]: best=(v,lines)
    return best,cnt
def to_spec(lines):
    return [(l["tk"],l["K"],l["tranche"],n,1 if l["cp"]=="C" else -1,l["sleeve"],l["why"],(SPYQ if l["tk"]=="SPY" else None)) for l,n in sorted(lines,key=lambda x:(x[0]["tranche"],x[0]["tk"]))]
if __name__=="__main__":
    U,rej=universe(); print(len(U),"candidates:",sorted(set((l["tk"],l["tranche"]) for l in U)))
    res={"universe":[dict(tk=l["tk"],K=l["K"],cp=l["cp"],tranche=l["tranche"],cost=l["cost"],delta=l["delta"],iv=l["iv"]) for l in U],"rejected":[list(r) for r in rej]}
    runs={"unhedged":dict(exclude=("SPY",)),"hedged":dict(force=("SPY",)),"free":dict()}
    for name,kw in runs.items():
        best,cnt=search(U,**kw)
        print(f"\n== {name}: {cnt} feasible books")
        if not best: continue
        spec=to_spec(best[1]); o=build(spec,book=BOOK); res[name]=dict(spec=[list(s[:7])+[str(s[7])] for s in spec],model=o,objective=best[0],feasible=cnt)
        for l in o["legs"]: print(f"  {l['tranche']} {l['tk']:5}{l['K']}{l['cp']} x{l['n']} ${l['cost']*l['n']:,.0f} d {l['delta']:+.2f} iv {l['iv']:.0%} g/$100 {l['gamma_per_100']:.2f} | B {l['pnl']['Base']*l['n']:+.0f} Bu {l['pnl']['Bull']*l['n']:+.0f} G {l['pnl']['Gamma']*l['n']:+.0f} S {l['pnl']['Shock']*l['n']:+.0f}")
        print("  deployed",round(o["deployed"]),"cash",round(o["cash"]),{c:f"{o['scen'][c]['ret']:+.0%}" for c in o["scen"]},"stand",{c:f"{o['stand'][c]['ret']:+.0%}" for c in o["stand"]})
        print("  sleeves",{k:round(v) for k,v in o["sleeves"].items()})
        print("  sched",[(s["label"][:12],round(s["pct"],2)) for s in o["schedule"]])
    json.dump(res,open("model_out_v6_1500.json","w"),indent=1,default=str)
