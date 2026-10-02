import json
from math import sqrt, log, exp
from statistics import NormalDist
from reportlab.platypus import Spacer, Table, TableStyle, KeepTogether
from reportlab.lib.units import inch
from bxpe import *

M = json.load(open("model_out.json"))
pick, legs, scen, bt, screen = M["pick"], M["legs"], M["scen"], M["bt"], M["screen"]
spot = {"MU":1091.89,"NVDA":231.59,"RTX":186.12,"LMT":506.50,"MRVL":269.30,"SKHY":191.40,"GDX":86.13}
N = NormalDist().cdf; R=0.04
def bs(S,K,T,iv):
    if T<=0: return max(S-K,0)
    d1=(log(S/K)+(R+.5*iv*iv)*T)/(iv*sqrt(T)); return S*N(d1)-K*exp(-R*T)*N(d1-iv*sqrt(T))
dep=M["deployed"]; cash=M["cash"]; p=pick['MU']; TH=42/365; sig=p['iv']*sqrt(TH)
lo,hi=1100.0,1500.0
for _ in range(80):
    m_=(lo+hi)/2
    if bs(m_,1300,4/365,p['iv'])*100 < p['cost']: lo=m_
    else: hi=m_
BE=(lo+hi)/2

doc = make_doc("Ritts_6_week_Wedding_Model_V3_MU.pdf", "RWS V3", "MYTHOS-RWS-V3-20261002", "October 2026 RWS Update", "Ritts Wedding Sleeve V3")
S = title_block("OCTOBER 2026", "Ritts Wedding Sleeve &#8211; Version 3 (&#8220;RWS V3&#8221;)",
    f"RWS V3 is a $5,000 short-dated long-call options sleeve {defined('Sleeve')} anchored on a single MU November 2026 call with four satellite gamma legs across "
    f"semiconductors, defense and gold miners, entered Monday, October 5, 2026 and exited Monday, November 16, 2026<super><font size=7>(1)</font></super>")
S.append(stats([("$5,000","book size","fully deployed: $4,988 premium, $12 cash"),
                (f"{scen['Bull']['ret']:+.0%}","Bull Case return on book","(Nov 16 '26 mark, +18% + 1 s.d. per name)<super>(3)</super>"),
                (f"{p['cost']/5000:.0%}","MU 1300C share of premium","single contract, $3,065, delta 0.231")]))
S.append(h1("Book Construction","2")); S.append(sub("(Nov 20 '26 calls; entry Oct 5 '26; Interactive Brokers SMART mids and mid-IVs as of the Oct 2 close)"))
rows=[["Leg","Ctr","Spot","Entry $/ctr","Delta","Gamma","Gamma/$","Mid-IV","Call OI","Deployed $"]]
for tk,n in legs:
    q=pick[tk]; rows.append([f"{tk} {q['K']}C", str(n), f"{spot[tk]:,.2f}", f"${q['cost']:,.0f}", f"{q['delta']:.3f}", f"{q['gamma']:.5f}", f"{q['gpp']:.3f}", f"{q['iv']:.1%}", f"{q['oi']:,}", f"${q['cost']*n:,.0f}"])
rows.append(["Cash / dry powder","–","–","–","–","–","–","–","–",f"${cash:,.0f}"]); rows.append(["Total","","","","","","","","","$5,000"])
S.append(tbl(rows,[1.1,0.4,0.65,0.75,0.55,0.65,0.65,0.6,0.65,0.8], bold_last=True))
S.append(Paragraph("Three changes versus the Version 2 memo of September 23: MU added as the anchor leg; the entry date moved to October 5 with every leg re-priced off live quotes; and the horizon "
 "extended from 37 to 42 days with the whole book rolled from the October 30 weekly to the November 20 monthly, the first regular expiry that covers the November 16 exit (46 days to expiry at entry, "
 "4 at exit). The selection rule is unchanged: a minimum entry delta of 0.20 and maximum gamma per dollar of premium. Funding the MU contract required dropping LMT (lowest gamma-per-premium of all "
 "28 candidates, with 35–137 open interest) and SKHY (the memory proxy carried in Version 2 because the MU contract was unaffordable; redundant once MU is held outright). "
 "The $204 residual bought a second GDX 98C.", BODY))
S.append(h2("Roll and Re-Strike of Carried Legs"))
S.append(Paragraph("Every Version 2 leg was re-screened at the November 20 expiry (Version 2 strikes in parentheses): NVDA 255C (245C); RTX 200C (205C; the November chain has no 205 strike and the 210C "
 "fails the delta floor at 0.141); MRVL 330C (305C); GDX 98C (108C; the November chain tops out at 102 and GDX has retraced to 86.13, so the 98C is the maximum-gamma strike that clears the floor).", BODY))
S += note("Please reference the Endnotes for sourcing and methodology. (1) Hold is 42 calendar days / 30 trading days. (2) Delta and gamma by Black-Scholes at 46 days to expiry, r = 4%, q = 0%; "
          "entry cost is the quoted mid times 100. Open interest as of Oct 2.")

# ---- page 2: premium breakdown + MU strike screen
S.append(h1("Premium Breakdown and MU Strike Screen","2")); S.append(sub("(% of deployed premium; four MU strikes screened at 46 days to expiry)"))
labels=[f"{tk} {pick[tk]['K']}C" for tk,n in legs]; vals=[pick[tk]['cost']*n/dep*100 for tk,n in legs]
rows=[["Strike","Mid $","IV","Delta","Gamma/$","Cost/ctr","Call OI","Verdict"]]
for r in screen["MU"]:
    v = "Selected" if r["K"]==pick["MU"]["K"] else ("Fails delta floor" if r["delta"]<0.20 else "Lower gamma/$")
    rows.append([f"{r['K']}C", f"{r['mid']:.2f}", f"{r['iv']:.1%}", f"{r['delta']:.3f}", f"{r['gpp']:.4f}", f"${r['cost']:,.0f}", f"{r['oi']:,}", v])
right=[tbl(rows,[0.5,0.45,0.45,0.45,0.55,0.6,0.55,0.95], font=7.8), Spacer(1,5),
       Paragraph("The 1350C has the best gamma-per-premium but fails the 0.20 delta floor at 0.182; the 1300C is the cheapest strike that clears it, at 42% less premium than the 1250C screened out in "
                 "Version 2. Open interest of 3,722 is the deepest among the four strikes after the 1350C.", BODY)]
two=Table([[pie(labels, vals), right]], colWidths=[2.9*inch, USABLE-2.9*inch])
two.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),0),('RIGHTPADDING',(0,0),(-1,-1),6)]))
S.append(two)

S.append(h1("Scenario Ladder and Portfolio Payout","3")); S.append(sub("(P&L marked Nov 16 '26 at 4 days to expiry, Black-Scholes at entry IV; Base +18% uniform; Bull +18% + 1 s.d.; Gamma Upside +18% + 2 s.d., 42-day s.d. per name)"))
rows=[["Leg","Flat (0%)","Base +18%","Bull (+18% + 1 s.d.)","Gamma Upside (+18% + 2 s.d.)"]]
for tk,n in legs:
    q=pick[tk]
    def cell(s): r=scen[s]['rows'][tk]; return f"{r['pnl']:+,.0f} ({r['ret']:+.0%})"
    def mv(s): return f"{scen[s]['rows'][tk]['move']:+.1%}"
    rows.append([f"{tk} {q['K']}C (x{n})", cell('Flat'), cell('Base'), f"{cell('Bull')} @ {mv('Bull')}", f"{cell('Gamma')} @ {mv('Gamma')}"])
S.append(tbl(rows,[1.2,1.1,1.2,1.7,1.9])); S.append(Spacer(1,6))
rows=[["Scenario","Portfolio P&L","Ending Value","Return on $5,000"]]
for s,lab in [("Flat","Flat (0%)"),("Base","Base Case (+18%)"),("Bull","Bull Case (+18% + 1 s.d.)"),("Gamma","Gamma Upside Case (+18% + 2 s.d.)")]:
    v=scen[s]; rows.append([lab, f"{v['pnl']:+,.0f}", f"${v['end']:,.0f}", f"{v['ret']:+.1%}"])
S.append(tbl(rows,[2.6,1.5,1.5,1.6]))
S += note(PAST_PERF)
S.append(h2("MU Anchor-Leg Sensitivity"))
S.append(Paragraph(f"MU is {p['cost']/5000:.0%} of premium, so the Sleeve's return is dominated by where MU prints on November 16. The 42-day one-standard-deviation move at 57.0% IV is {sig:.1%} "
 f"(${spot['MU']*sig:,.0f}). Breakeven at the four-day mark is MU of approximately ${BE:,.0f} ({BE/spot['MU']-1:+.1%}; versus ${1300+p['mid']:,.0f} / {(1300+p['mid'])/spot['MU']-1:+.1%} at expiry). "
 "Other legs are held at the Base Case column for the book-level row.", BODY))
rows=[["MU on Nov 16","Move","Call value","MU leg P&L","MU leg return","Book P&L (rest @ Base)","Book return"]]
others = scen['Base']['pnl'] - scen['Base']['rows']['MU']['pnl']
for mvp in [0.0,0.10,0.18,0.25,0.30,sig+0.18,0.45,0.50,2*sig+0.18,0.75,1.00]:
    S1=spot['MU']*(1+mvp); v=bs(S1,1300,4/365,p['iv'])*100; pnl=v-p['cost']
    rows.append([f"${S1:,.0f}", f"{mvp:+.1%}", f"${v:,.0f}", f"{pnl:+,.0f}", f"{pnl/p['cost']:+.0%}", f"{pnl+others:+,.0f}", f"{(pnl+others)/5000:+.0%}"])
S.append(tbl(rows,[1.0,0.7,0.9,1.0,1.0,1.6,1.0]))

S.append(h1("Backtest: Six-Week Forward Returns","4")); S.append(sub("(overlapping 42-day windows from two years of weekly closes, n = 99 per name; thresholds use each leg's entry IV)"))
rows=[["Ticker","Real. Vol","Entry IV","Mean 6wk","Max 6wk","Base thr.","Hit Base","Bull thr.","Hit Bull","Gam. thr.","Hit Gam."]]
for tk in ["MU","NVDA","RTX","MRVL","GDX","LMT"]:
    v=bt[tk]; rows.append([tk+("*" if tk=="LMT" else ""), f"{v['rv']:.1%}", f"{v['iv']:.1%}", f"{v['mean']:+.1%}", f"{v['mx']:+.1%}", f"{v['base']:.0%}", f"{v['hb']:.0%}", f"{v['bull']:.1%}", f"{v['hu']:.0%}", f"{v['gam']:.1%}", f"{v['hg']:.0%}"])
S.append(tbl(rows,[0.6,0.7,0.65,0.7,0.7,0.65,0.65,0.65,0.65,0.7,0.7]))
S.append(Paragraph("* LMT is not in the Version 3 Sleeve; shown for continuity with Version 2. SKHY (13 weekly bars since listing) is excluded.", NOTE))
S.append(h2("Key Findings"))
S += bullets([
 f"<b>MU is the only leg whose Bull threshold (+{bt['MU']['bull']:.1%}) has a double-digit historical hit rate ({bt['MU']['hu']:.0%} of windows);</b> its Gamma Upside threshold (+{bt['MU']['gam']:.1%}) has printed in {bt['MU']['hg']:.0%} of windows (maximum observed six-week move +{bt['MU']['mx']:.1%}). The in-sample mean six-week return is +{bt['MU']['mean']:.1%}; the uniform +18% Base Case is MU's historical average, not a tail.",
 f"Extending the window from five to six weeks raises Base Case hit rates versus Version 2 for every carried name (MU 39% to {bt['MU']['hb']:.0%}, MRVL 32% to {bt['MRVL']['hb']:.0%}, GDX 14% to {bt['GDX']['hb']:.0%}, RTX 0% to {bt['RTX']['hb']:.0%}); NVDA is unchanged at {bt['NVDA']['hb']:.0%}.",
 f"Entry IVs sit within 2–10 points of two-year realized volatility on every leg; MU at 57.0% versus {bt['MU']['rv']:.1%} realized is the largest discount.",
 f"RTX and GDX function as cheap-gamma ballast (0.60 and 1.21 gamma per dollar); RTX's +18% Base Case has occurred in {bt['RTX']['hb']:.0%} of windows (maximum +{bt['RTX']['mx']:.1%}), GDX's in {bt['GDX']['hb']:.0%}.",
 "In-window dated catalysts (approximate): RTX third-quarter report Oct 20–21; FOMC Oct 27–28; SK Hynix third-quarter results late October (HBM/DRAM pricing read-through to MU). NVDA's report (Nov 18–19) and MU's fiscal first-quarter report (December) fall after the exit.",
])

S.append(h1("Assessment and Recommendation"))
S.append(Paragraph(
 f"All five legs clear the delta floor with positive gamma-per-premium, and the Sleeve is fully deployed (${dep:,.0f} of $5,000). It is a concentrated MU convexity position with four satellite gamma legs: "
 f"MU contributes {scen['Bull']['rows']['MU']['pnl']/scen['Bull']['pnl']:.0%} of Bull Case P&L and {scen['Gamma']['rows']['MU']['pnl']/scen['Gamma']['pnl']:.0%} of Gamma Upside Case P&L. The Base Case column is "
 f"carried by NVDA, RTX and GDX, while MU and MRVL sit just below strike at the four-day mark (the 1300 strike is +19.1% from spot); MU needs a {BE/spot['MU']-1:+.1%} move to break even at the exit mark "
 f"and a +{sig+0.18:.1%} move (Bull Case) to return {scen['Bull']['rows']['MU']['ret']:+.0%} on the leg. The six-week extension helps on both axes: historical Base and Bull hit rates rise across the board, "
 f"and the November 20 monthly carries materially deeper open interest than the October 30 weeklies used in Version 2 (MU 3,722; NVDA 11,600; GDX 3,000).", BODY))
S.append(h2("Concentration Note"))
S.append(Paragraph(f"MU plus MRVL is 78% of premium. Where the MU weight is to be reduced without leaving the name, the alternative is the MU 1350C (delta 0.182, $2,355), which breaks the delta floor but frees $710, "
 f"enough to restore SKHY 230C. That variant is modeled in the companion RWS V3b memo; the mandate here was to maximize upside, which the 1300C delivers (Gamma Upside Case leg P&L "
 f"{scen['Gamma']['rows']['MU']['pnl']:+,.0f} versus an estimated +{(bs(spot['MU']*(1.18+2*sig),1350,4/365,.577)*100-2355):,.0f} for the 1350C).", BODY))

from addendum_jan2026 import addendum
S += addendum("5")

S.append(h1("Endnotes"))
S += [Paragraph(t, EN) for t in [
 "(1) Entry Monday, October 5, 2026; exit Monday, November 16, 2026; contracts expire Friday, November 20, 2026. Dates in the catalyst list are approximate.",
 "(2) Delta and gamma by Black-Scholes at 46 days to expiry (r = 4%, q = 0%) using each contract's mid implied volatility. Entry cost per contract is the Interactive Brokers SMART mid at the October 2, 2026 close multiplied by 100. Strike selection: minimum entry delta 0.20, then maximum gamma per dollar of premium. Open interest is call open interest as of October 2.",
 "(3) Scenarios are marked on November 16, 2026 by Black-Scholes at four days to expiry using each leg's entry implied volatility (no change in volatility assumed). The per-name standard deviation is entry IV multiplied by the square root of 42/365. Flat (0%) is a time-decay reference.",
 "(4) Backtest: Interactive Brokers weekly closes, two-year lookback through the September 28, 2026 bar, overlapping six-week forward returns, n = 99 per name. Realized volatility is annualized from weekly log returns.",
 "(5) Statement figures are as printed on the January 1–30, 2026 J.P. Morgan Securities statement. Blotter statistics are parsed from its trade-activity section and capture 134 closing transactions totaling $22,224 against the statement's $22,602 net realized.",
 "Model code: memos/ritts_6wk_model_v3.py.",
]]
S += disclosure("memo", "Mythos", "Donald B. Ritts III",
 extra=["<b>Statement Example.</b> The January 2026 statement presented in the addendum is a single selected period and may not be representative of all periods or of the Sleeve's own outcome. It should not be "
        "assumed that the Sleeve will make equally successful or comparable trades. The positions in that statement were entered under different market conditions and with a different structure (30–45 "
        "concurrent lines, one- to two-week tenors) from the Sleeve presented herein."])
doc.build(S); print("ok v3")
