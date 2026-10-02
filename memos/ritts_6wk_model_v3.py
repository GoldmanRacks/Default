"""
Ritts 6-week Wedding Model V3 -- MU added, Oct 5 '26 entry, Nov 16 '26 exit, Nov 20 '26 expiry.
Black-Scholes (r=4%, q=0%). Quotes = IBKR SMART mids pulled 2026-10-02.
"""
import math, json
from math import log, sqrt, exp
from statistics import NormalDist

N = NormalDist().cdf
pdf = NormalDist().pdf
R = 0.04

def bs_call(S, K, T, iv):
    if T <= 0: return max(S-K, 0.0)
    d1 = (log(S/K) + (R + 0.5*iv*iv)*T) / (iv*sqrt(T))
    d2 = d1 - iv*sqrt(T)
    return S*N(d1) - K*exp(-R*T)*N(d2)

def greeks(S, K, T, iv):
    d1 = (log(S/K) + (R + 0.5*iv*iv)*T) / (iv*sqrt(T))
    return N(d1), pdf(d1)/(S*iv*sqrt(T))

ENTRY_DTE = 46      # Oct 5 -> Nov 20
EXIT_DTE  = 4       # Nov 16 -> Nov 20
HOLD_DAYS = 42      # Oct 5 -> Nov 16
T0 = ENTRY_DTE/365; T1 = EXIT_DTE/365; TH = HOLD_DAYS/365

from candidates import spot, cands
# (strike, mid, mid-IV, call OI)

screen = {}
for tk, rows in cands.items():
    out = []
    for K, mid, iv, oi in rows:
        d, g = greeks(spot[tk], K, T0, iv)
        out.append(dict(K=K, mid=mid, iv=iv, oi=oi, delta=d, gamma=g, gpp=g/mid*100, cost=mid*100))
    screen[tk] = out

# Selection rule: delta >= 0.20 floor, max gamma-per-$premium
import sys
VARIANT = sys.argv[1] if len(sys.argv) > 1 else "v3"
FLOOR = 0.20
FLOOR_OVERRIDE = {"MU":0.18, "BA":0.18} if VARIANT == "v3b" else ({"AMD":0.18, "LITE":0.14} if VARIANT in ("v4","v4a","v4b") else {})
pick = {}
for tk, rows in screen.items():
    ok = [r for r in rows if r["delta"] >= FLOOR_OVERRIDE.get(tk, FLOOR)]
    pick[tk] = max(ok, key=lambda r: r["gpp"])
if VARIANT in ("v4","v4a","v4b"):
    # ITM rule for the DRAM anchor: delta >= 0.70 (in the money), then deepest open interest
    itm = [r for r in screen["DRAM"] if r["delta"] >= 0.70]
    pick["DRAM"] = max(itm, key=lambda r: r["oi"])

# Book: MU 1 ctr (mandated), then remaining names by gamma/$ until $5,000 is spent; LMT + SKHY dropped (see memo)
BOOK = 5000.0
legs = [("MU",1),("NVDA",1),("RTX",1),("MRVL",1),("GDX",1)]
if VARIANT == "v3b":
    legs = [("MU",1),("NVDA",1),("RTX",1),("BA",1),("MRVL",1),("SKHY",1),("GDX",1)]
if VARIANT == "v4":
    # INTC replaces LITE in the AMD book; INTC's low contract cost lets BA and MRVL return and GDX go back to two contracts
    legs = [("DRAM",1),("NVDA",1),("AMD",1),("INTC",2),("BA",1),("MRVL",1),("GDX",2)]
if VARIANT == "v4b":
    # TER alternative in the same slot: one TER contract at the floor, BA restored, MRVL does not fit
    legs = [("DRAM",1),("NVDA",1),("AMD",1),("TER",1),("BA",1),("GDX",2)]
if VARIANT == "v4a":
    # AMD-only alternative: AMD in the former VICR slot, all other V4 legs unchanged
    legs = [("DRAM",2),("NVDA",1),("AMD",1),("BA",1),("MRVL",1),("GDX",1)]
deployed = sum(pick[t]["cost"]*n for t,n in legs)
cash = BOOK - deployed
# use residual cash on cheapest-gamma legs in whole contracts
for tk in ["GDX","RTX","NVDA"]:
    c = pick[tk]["cost"]
    while cash >= c:
        legs = [(t, n+1 if t==tk else n) for t,n in legs]
        cash -= c
deployed = BOOK - cash

def leg_pnl(tk, n, move_pct):
    p = pick[tk]; S1 = spot[tk]*(1+move_pct)
    v1 = bs_call(S1, p["K"], T1, p["iv"])*100
    return (v1 - p["cost"])*n, v1*n

scen = {}
for name, mult in [("Flat",0),("Base",None),("Bull",1),("Gamma",2)]:
    rows = {}; tot = 0
    for tk, n in legs:
        p = pick[tk]; sig = p["iv"]*sqrt(TH)
        mv = 0.0 if mult==0 else 0.18 + (0 if mult is None else mult*sig)
        pnl, val = leg_pnl(tk, n, mv)
        rows[tk] = dict(move=mv, pnl=pnl, ret=pnl/(p["cost"]*n))
        tot += pnl
    scen[name] = dict(rows=rows, pnl=tot, end=BOOK+tot, ret=tot/BOOK)

# ---- flat-spot vol re-rate: IV shift (points, uniform) needed for +5% / +10% book return at each exit mark
def book_value(move, dte, dvol):
    tot=0
    for tk,n in legs:
        q=pick[tk]; S1=spot[tk]*(1+move); iv=max(q["iv"]+dvol, 0.05)
        tot += bs_call(S1, q["K"], dte/365, iv)*100*n
    return tot
flat_rerate = {}
for lab,dte in [("Oct 23 (28 DTE)",28),("Oct 30 (21 DTE)",21),("Nov 6 (14 DTE)",14),("Nov 16 (4 DTE)",4)]:
    row={"dte":dte,"flat_ret": (book_value(0,dte,0)-deployed)/BOOK}
    for tgt in (0.05,0.10):
        lo,hi=0.0,3.0; feasible = (book_value(0,dte,hi)-deployed)/BOOK >= tgt
        if feasible:
            for _ in range(60):
                mid=(lo+hi)/2
                if (book_value(0,dte,mid)-deployed)/BOOK < tgt: lo=mid
                else: hi=mid
            row[f"dvol_{int(tgt*100)}"]=(lo+hi)/2
        else: row[f"dvol_{int(tgt*100)}"]=None
    flat_rerate[lab]=row
# per-leg values for the flat re-rate rows shown in the ladder (Oct 30 mark)
def leg_rows(move, dte, dvol):
    out={}
    for tk,n in legs:
        q=pick[tk]; S1=spot[tk]*(1+move); iv=max(q["iv"]+dvol,0.05); v=bs_call(S1,q["K"],dte/365,iv)*100*n
        out[tk]=dict(move=move, pnl=v-q["cost"]*n, ret=(v-q["cost"]*n)/(q["cost"]*n))
    return out
r30=flat_rerate["Oct 30 (21 DTE)"]
for tgt in (5,10):
    dv=r30.get(f"dvol_{tgt}")
    if dv is not None:
        rows=leg_rows(0,21,dv); tot=sum(r["pnl"] for r in rows.values())
        scen[f"Flat+{tgt}"]=dict(rows=rows, pnl=tot, end=BOOK+tot, ret=tot/BOOK, dvol=dv, dte=21)

# ---- backtest: 6-week forward returns from 2y weekly closes (IBKR, through 9/28/26 bar)
closes = json.load(open("/home/user/Default/memos/weekly_closes.json"))
bt = {}
for tk, cl in closes.items():
    if len(cl) < 20: continue
    rets = [cl[i+6]/cl[i]-1 for i in range(len(cl)-6)]
    lr = [log(cl[i+1]/cl[i]) for i in range(len(cl)-1)]
    mu_ = sum(lr)/len(lr); rv = sqrt(sum((x-mu_)**2 for x in lr)/(len(lr)-1))*sqrt(52)
    sig = pick[tk]["iv"]*sqrt(TH)
    base, bull, gam = 0.18, 0.18+sig, 0.18+2*sig
    bt[tk] = dict(n=len(rets), rv=rv, iv=pick[tk]["iv"], mean=sum(rets)/len(rets), mx=max(rets),
                  hb=sum(r>=base for r in rets)/len(rets), hu=sum(r>=bull for r in rets)/len(rets),
                  hg=sum(r>=gam for r in rets)/len(rets), base=base, bull=bull, gam=gam)

json.dump(dict(variant=VARIANT, floor=FLOOR, floor_override=FLOOR_OVERRIDE, flat_rerate=flat_rerate, screen=screen, pick=pick, legs=legs, cash=cash, deployed=deployed, scen=scen, bt=bt),
          open(f"/home/user/Default/memos/model_out{'' if VARIANT=='v3' else '_'+VARIANT}.json","w"), indent=1, default=float)

print("PICKS"); 
for tk,n in legs: p=pick[tk]; print(f"{tk:5} {p['K']}C x{n} mid={p['mid']:.2f} iv={p['iv']:.1%} d={p['delta']:.3f} g={p['gamma']:.5f} g/$={p['gpp']:.3f} cost={p['cost']*n:,.0f} OI={p['oi']}")
print(f"deployed {deployed:,.0f} cash {cash:,.0f}")
for s,v in scen.items():
    print(f"{s:6} P&L {v['pnl']:+,.0f} end {v['end']:,.0f} ret {v['ret']:+.1%}")
    for tk,r in v['rows'].items(): print(f"   {tk:5} move {r['move']:+.1%} pnl {r['pnl']:+,.0f} ({r['ret']:+.1%})")
print("BACKTEST")
for tk,v in bt.items(): print(f"{tk:5} n={v['n']} rv={v['rv']:.1%} iv={v['iv']:.1%} mean={v['mean']:+.1%} max={v['mx']:+.1%} base>={v['base']:.1%}:{v['hb']:.0%} bull>={v['bull']:.1%}:{v['hu']:.0%} gamma>={v['gam']:.1%}:{v['hg']:.0%}")
print("SCREEN (LMT incl.)")
for tk,rows in screen.items():
    for r in rows: print(f"  {tk:5} {r['K']}C mid={r['mid']:.2f} d={r['delta']:.3f} g/$={r['gpp']:.3f} cost={r['cost']:,.0f}")
