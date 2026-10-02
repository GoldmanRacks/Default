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

spot = {"MU":1091.89,"NVDA":231.59,"RTX":186.12,"LMT":506.50,"MRVL":269.30,"SKHY":191.40,"GDX":86.13}
# (strike, mid, mid-IV, call OI)
cands = {
 "MU":  [(1200,52.68,.549,2688),(1250,40.48,.559,2228),(1300,30.65,.570,3722),(1350,23.55,.577,7386)],
 "NVDA":[(245,6.90,.348,21327),(250,5.38,.344,36129),(255,4.15,.341,11600),(260,3.15,.341,24287)],
 "RTX": [(195,4.28,.288,392),(200,2.91,.286,1928),(210,1.29,.289,1786)],
 "LMT": [(540,9.30,.276,137),(545,8.85,.289,50),(550,7.60,.286,109),(555,6.55,.288,35)],
 "MRVL":[(300,14.63,.650,10309),(310,12.13,.651,8849),(320,10.08,.655,6063),(330,8.33,.661,965)],
 "SKHY":[(215,9.40,.586,973),(220,8.03,.584,1791),(225,6.90,.586,489),(230,6.10,.605,2222),(235,4.95,.588,327)],
 "GDX": [(93,3.05,.410,1095),(95,2.59,.420,1434),(96,2.31,.419,628),(98,1.92,.424,3000)],
}

screen = {}
for tk, rows in cands.items():
    out = []
    for K, mid, iv, oi in rows:
        d, g = greeks(spot[tk], K, T0, iv)
        out.append(dict(K=K, mid=mid, iv=iv, oi=oi, delta=d, gamma=g, gpp=g/mid*100, cost=mid*100))
    screen[tk] = out

# Selection rule: delta >= 0.20 floor, max gamma-per-$premium
pick = {}
for tk, rows in screen.items():
    ok = [r for r in rows if r["delta"] >= 0.20]
    pick[tk] = max(ok, key=lambda r: r["gpp"])

# Book: MU 1 ctr (mandated), then remaining names by gamma/$ until $5,000 is spent; LMT + SKHY dropped (see memo)
BOOK = 5000.0
legs = [("MU",1),("NVDA",1),("RTX",1),("MRVL",1),("GDX",1)]
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

json.dump(dict(screen=screen, pick=pick, legs=legs, cash=cash, deployed=deployed, scen=scen, bt=bt),
          open("/home/user/Default/memos/model_out.json","w"), indent=1, default=float)

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
