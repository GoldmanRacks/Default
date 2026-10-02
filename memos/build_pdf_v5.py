import json
from math import sqrt, log, exp
from statistics import NormalDist
from reportlab.platypus import Spacer, Table, TableStyle
from reportlab.lib.units import inch
from bxpe import *
from reportlab.lib.styles import ParagraphStyle
from candidates import spot

O = json.load(open("model_out_v5.json")); V3 = json.load(open("model_out.json")); V4 = json.load(open("model_out_v4.json")); bt = V4["bt"]
P = O["primary"]; NR = O["normalized"]; UC = O["unconstrained"]; FR = P["flat_rerate"]
legs = P["legs"]; dep = P["deployed"]; cash = P["cash"]; S4 = V4["scen"]; S3 = V3["scen"]
N = NormalDist().cdf; R=0.04
def bs(S,K,T,iv):
    if T<=0: return max(S-K,0)
    d1=(log(S/K)+(R+.5*iv*iv)*T)/(iv*sqrt(T)); return S*N(d1)-K*exp(-R*T)*N(d1-iv*sqrt(T))
def legname(l): return f"{l['tk']} {l['K']}C"
mu=[l for l in legs if l["tk"]=="MU"][0]; TH=42/365; sig=mu["iv"]*sqrt(TH)
def ret(o,c): return o["scen"][c]["ret"]

doc = make_doc("Ritts_6_week_Wedding_Model_V5_Optimized.pdf", "RWS V5", "MYTHOS-RWS-V5-20261002", "October 2026 RWS Update", "Ritts Wedding Sleeve V5")
S = title_block("OCTOBER 2026", "Ritts Wedding Sleeve &#8211; Version 5 (&#8220;RWS V5&#8221;)",
    f"RWS V5 restores MU as the anchor in place of the DRAM ETF and lets an integer optimizer allocate the rest of the $5,000 across every November 20 '26 call quoted this session, "
    f"maximizing the equal-weighted mean P&L across the four ladder cases, on the same October 5 entry and November 16, 2026 exit<super><font size=7>(1)</font></super>")
OBJ3=(S3['Flat']['pnl']+S3['Base']['pnl']+S3['Bull']['pnl']+S3['Gamma']['pnl'])/4; OBJ4=(S4['Flat']['pnl']+S4['Base']['pnl']+S4['Bull']['pnl']+S4['Gamma']['pnl'])/4
S.append(stats([(f"${P['obj']:,.0f}","mean P&L across Flat / Base / Bull / Gamma",f"the maximized objective; V3 scores ${OBJ3:,.0f}, V4 ${OBJ4:,.0f}"),
                (f"{ret(P,'Base'):+.0%}","Base Case return on book",f"vs. {S3['Base']['ret']:+.0%} for V3 and {S4['Base']['ret']:+.0%} for V4<super>(3)</super>"),
                (f"{ret(P,'Gamma'):+.0%}","Gamma Upside Case return on book",f"vs. {S3['Gamma']['ret']:+.0%} for V3 and {S4['Gamma']['ret']:+.0%} for V4")]))
S.append(h1("Optimized Book","2")); S.append(sub("(Nov 20 '26 calls; entry Oct 5 '26; objective: mean of the four case P&Ls marked Nov 16 at 4 DTE; constraints: $5,000 budget, 0.20 delta floor, call OI &ge; 500, MU required as a single anchor contract, 35% single-name premium cap on satellites)"))
rows=[["Leg","Ctr","Spot","Entry $/ctr","Delta","Mid-IV","Call OI","Deployed $","P&L Flat","P&L Base","P&L Bull","P&L Gamma"]]
for l in legs:
    n=l["n"]; rows.append([legname(l), str(n), f"{spot[l['tk']]:,.2f}", f"${l['cost']:,.0f}", f"{l['delta']:.3f}", f"{l['iv']:.1%}", f"{l['oi']:,}", f"${l['cost']*n:,.0f}",
                           f"{l['pnl']['Flat']*n:+,.0f}", f"{l['pnl']['Base']*n:+,.0f}", f"{l['pnl']['Bull']*n:+,.0f}", f"{l['pnl']['Gamma']*n:+,.0f}"])
rows.append(["Cash","–","–","–","–","–","–",f"${cash:,.0f}","","","",""])
rows.append(["Total","","","","","","","$5,000",f"{P['scen']['Flat']['pnl']:+,.0f}",f"{P['scen']['Base']['pnl']:+,.0f}",f"{P['scen']['Bull']['pnl']:+,.0f}",f"{P['scen']['Gamma']['pnl']:+,.0f}"])
S.append(tbl(rows,[0.95,0.33,0.55,0.65,0.48,0.55,0.6,0.7,0.65,0.65,0.7,0.75], bold_last=True, font=7.8))
S.append(Paragraph(
 f"The optimizer keeps the MU 1300C ({mu['cost']/5000:.0%} of premium, the V3 anchor) and spends the remaining ${5000-mu['cost']:,.0f} on five RTX 200C and one NVDA 255C, leaving ${cash:,.0f}. RTX sits at its 35% "
 f"single-name cap; without the cap the solution adds a sixth RTX contract in place of NVDA. Every other screened name (AMD, INTC, BA, MRVL, SKHY, GDX) is allocated zero because, per dollar of premium, "
 f"RTX 200C and NVDA 255C produce the highest mean P&L across the four cases in this quote set.", BODY))
S += note("Please reference the Endnotes for sourcing and methodology. (1) Hold is 42 calendar days. (2) Candidate universe: the 14 names and 60 Nov 20 '26 strikes quoted on Oct 2 for Versions 3 through 4; "
          "DRAM excluded by instruction, 33 contracts removed by the 0.20 delta floor or the 500-contract open-interest filter, 27 remaining across nine names. Mids as of the Oct 2 close.")

S.append(h1("Optimization Method and Results","2")); S.append(sub("(group knapsack over names, exact integer contracts; four constraint sets; two ladder definitions)"))
S.append(Paragraph("Each candidate contract is priced in the four ladder cases at the November 16 mark, giving a per-contract P&L vector. The objective is the equal-weighted mean of the four, summed across the book. "
 "The allocation is solved exactly by dynamic programming over the budget in $5 steps, enumerating every contract combination within each name's cap and choosing one combination per name. Results under "
 "progressively looser constraints, and under a vol-normalized ladder in which the Base, Bull and Gamma cases are +1, +2 and +3 standard deviations of each name rather than a uniform +18% plus 1 or 2:", BODY))
CELL=ParagraphStyle("cell", fontName="SourceSans3-Regular", fontSize=7.4, leading=8.8, textColor=BLACK)
def book_str(o): return Paragraph(", ".join(f"{legname(l)} x{l['n']}" for l in o["legs"]), CELL)
def cell(t): return Paragraph(t, CELL)
rows=[["Constraint set","Book","Deployed","Flat","Base","Bull","Gamma","Mean P&L"]]
rows.append(["Primary: floor 0.20, OI ≥ 500, MU x1, 35% cap", book_str(P), f"${dep:,.0f}", f"{ret(P,'Flat'):+.0%}", f"{ret(P,'Base'):+.0%}", f"{ret(P,'Bull'):+.0%}", f"{ret(P,'Gamma'):+.0%}", f"${P['obj']:,.0f}"])
rows.append([cell("No single-name cap"), book_str(O['nocap']), f"${O['nocap']['deployed']:,.0f}", f"{ret(O['nocap'],'Flat'):+.0%}", f"{ret(O['nocap'],'Base'):+.0%}", f"{ret(O['nocap'],'Bull'):+.0%}", f"{ret(O['nocap'],'Gamma'):+.0%}", f"${O['nocap']['obj']:,.0f}"])
rows.append([cell("Unconstrained: no floor, no OI filter, no cap"), book_str(UC), f"${UC['deployed']:,.0f}", f"{ret(UC,'Flat'):+.0%}", f"{ret(UC,'Base'):+.0%}", f"{ret(UC,'Bull'):+.0%}", f"{ret(UC,'Gamma'):+.0%}", f"${UC['obj']:,.0f}"])
rows.append([cell("Primary constraints, vol-normalized ladder"), book_str(NR), f"${NR['deployed']:,.0f}", f"{ret(NR,'Flat'):+.0%}", f"{ret(NR,'Base'):+.0%}", f"{ret(NR,'Bull'):+.0%}", f"{ret(NR,'Gamma'):+.0%}", f"${NR['obj']:,.0f}*"])
rows.append([cell("V4 (INTC book, for reference)"), cell("DRAM 55C x1, NVDA 255C, AMD 760C, INTC 155C x2, BA 215C, MRVL 330C, GDX 98C x2"), f"${V4['deployed']:,.0f}", f"{S4['Flat']['ret']:+.0%}", f"{S4['Base']['ret']:+.0%}", f"{S4['Bull']['ret']:+.0%}", f"{S4['Gamma']['ret']:+.0%}", f"${(S4['Flat']['pnl']+S4['Base']['pnl']+S4['Bull']['pnl']+S4['Gamma']['pnl'])/4:,.0f}"])
rows.append([cell("V3 (MU anchor book, for reference)"), cell("MU 1300C, NVDA 255C, RTX 200C, MRVL 330C, GDX 98C x2"), f"${V3['deployed']:,.0f}", f"{S3['Flat']['ret']:+.0%}", f"{S3['Base']['ret']:+.0%}", f"{S3['Bull']['ret']:+.0%}", f"{S3['Gamma']['ret']:+.0%}", f"${(S3['Flat']['pnl']+S3['Base']['pnl']+S3['Bull']['pnl']+S3['Gamma']['pnl'])/4:,.0f}"])
S.append(tbl(rows,[1.6,2.2,0.65,0.5,0.5,0.55,0.6,0.75], font=7.4))
S.append(Paragraph("* Mean P&L on the normalized ladder, not comparable with the standing-ladder column above it. Marked on the standing ladder, the normalized book returns "
 f"{NR['standing_ret']['Flat']:+.0%} / {NR['standing_ret']['Base']:+.0%} / {NR['standing_ret']['Bull']:+.0%} / {NR['standing_ret']['Gamma']:+.0%}; marked on the normalized ladder, the primary book returns "
 f"{P['normalized_ret']['Flat']:+.0%} / {P['normalized_ret']['Base']:+.0%} / {P['normalized_ret']['Bull']:+.0%} / {P['normalized_ret']['Gamma']:+.0%}.", NOTE))
S.append(h2("What Drives the Allocation"))
S += bullets([
 "The standing ladder applies a uniform +18% Base Case to every name. For RTX (28.6% IV) that is a 1.6 standard-deviation move in 42 days; for MU (57.0%) it is 0.9. The optimizer therefore prices RTX 200C as the cheapest way to buy Base and Bull Case P&L, and the unconstrained run takes the logic to its end: twenty RTX 210C at delta 0.141 beside one MU 1350C.",
 "The single-name cap and the delta floor are what keep the primary book recognizable: the cap limits RTX to $1,455 of premium, and the floor removes the 210C (0.141) in favor of the 200C (0.272).",
 f"Under the vol-normalized ladder the same optimizer shifts the satellite budget to INTC 155C x4 (74% IV, so its +1/+2/+3 s.d. moves are large) with one RTX and one GDX, and keeps the MU 1300C in both versions: the anchor choice is robust to the ladder definition, the satellite choice is not.",
 "The objective treats the four cases as equally likely. The backtest does not: across 99 six-week windows the +18% Base Case has printed 2% of the time for RTX, 13% for NVDA and 40% for MU. Weighting the cases by those frequencies would shift premium back toward MU and away from RTX.",
])

S.append(h1("Scenario Ladder and Portfolio Payout","3")); S.append(sub("(P&L marked Nov 16 '26 at 4 days to expiry, Black-Scholes at entry IV; Base +18% uniform; Bull +18% + 1 s.d.; Gamma Upside +18% + 2 s.d., 42-day s.d. per name)"))
rows=[["Leg","Flat (0%)","Base +18%","Bull (+18% + 1 s.d.)","Gamma Upside (+18% + 2 s.d.)"]]
for l in legs:
    n=l["n"]; c=l["cost"]*n; sg=l["iv"]*sqrt(TH)
    rows.append([f"{legname(l)} (x{n})", f"{l['pnl']['Flat']*n:+,.0f} ({l['pnl']['Flat']/l['cost']:+.0%})", f"{l['pnl']['Base']*n:+,.0f} ({l['pnl']['Base']/l['cost']:+.0%})",
                 f"{l['pnl']['Bull']*n:+,.0f} ({l['pnl']['Bull']/l['cost']:+.0%}) @ {0.18+sg:+.1%}", f"{l['pnl']['Gamma']*n:+,.0f} ({l['pnl']['Gamma']/l['cost']:+.0%}) @ {0.18+2*sg:+.1%}"])
S.append(tbl(rows,[1.2,1.1,1.2,1.7,1.9])); S.append(Spacer(1,6))
f5=FR["Oct 30 (21 DTE)"]["dvol_5"]; f10=FR["Oct 30 (21 DTE)"]["dvol_10"]
rows=[["Scenario","Mark","V5 P&L","V5 Ending Value","V5 Return","V4 (ref.)","V3 (ref.)"]]
rows.append(["Flat (0% spot, entry IV)","Nov 16, 4 DTE", f"{P['scen']['Flat']['pnl']:+,.0f}", f"${P['scen']['Flat']['end']:,.0f}", f"{ret(P,'Flat'):+.1%}", f"{S4['Flat']['ret']:+.1%}", f"{S3['Flat']['ret']:+.1%}"])
rows.append([f"Flat + vol re-rate (IV +{f5*100:.0f} pts)","Oct 30, 21 DTE", "+250", "$5,250", "+5.0%", f"+{V4['flat_rerate']['Oct 30 (21 DTE)']['dvol_5']*100:.0f} pts", "n/a"])
rows.append([f"Flat + vol re-rate (IV +{f10*100:.0f} pts)","Oct 30, 21 DTE", "+500", "$5,500", "+10.0%", f"+{V4['flat_rerate']['Oct 30 (21 DTE)']['dvol_10']*100:.0f} pts", "n/a"])
for s,lab in [("Base","Base Case (+18%)"),("Bull","Bull Case (+18% + 1 s.d.)"),("Gamma","Gamma Upside Case (+18% + 2 s.d.)")]:
    rows.append([lab,"Nov 16, 4 DTE", f"{P['scen'][s]['pnl']:+,.0f}", f"${P['scen'][s]['end']:,.0f}", f"{ret(P,s):+.1%}", f"{S4[s]['ret']:+.1%}", f"{S3[s]['ret']:+.1%}"])
S.append(tbl(rows,[2.1,1.0,0.9,1.1,0.9,0.9,0.9]))
S += note(PAST_PERF)
S.append(h2("Flat Case: Conditions for a +5% to +10% Book Return"))
rows=[["Exit mark","Days to expiry","Flat return at entry IV","IV rise for +5%","IV rise for +10%"]]
for lab,r in FR.items():
    rows.append([lab, str(r["dte"]), f"{r['flat_ret']:+.1%}", f"+{r['dvol_5']*100:.0f} pts" if r["dvol_5"] else "not reachable", f"+{r['dvol_10']*100:.0f} pts" if r["dvol_10"] else "not reachable"])
S.append(tbl(rows,[1.6,1.1,1.5,1.4,1.4]))
S.append(Paragraph(f"The optimized book needs the smallest re-rate of any version to reach +5% at a flat print: +{FR['Oct 23 (28 DTE)']['dvol_5']*100:.0f} points on October 23 or +{f5*100:.0f} on October 30 "
 f"(V4: +{V4['flat_rerate']['Oct 23 (28 DTE)']['dvol_5']*100:.0f} and +{V4['flat_rerate']['Oct 30 (21 DTE)']['dvol_5']*100:.0f}), because 29% of premium sits in RTX at 28.6% IV where a point of volatility is a large proportional change. "
 f"The November 16 mark remains out of reach (+{FR['Nov 16 (4 DTE)']['dvol_5']*100:.0f} points).", BODY))
S.append(h2("MU Anchor-Leg Sensitivity"))
S.append(Paragraph(f"MU is {mu['cost']/5000:.0%} of premium. The 42-day one-standard-deviation move at 57.0% IV is {sig:.1%} (${spot['MU']*sig:,.0f}); breakeven at the four-day mark is approximately $1,299 (+19.0%). "
 "Other legs are held at the Base Case column for the book-level row.", BODY))
rows=[["MU on Nov 16","Move","Call value","MU leg P&L","MU leg return","Book P&L (rest @ Base)","Book return","V3 book return"]]
others=P['scen']['Base']['pnl']-mu['pnl']['Base']; others3=S3['Base']['pnl']-S3['Base']['rows']['MU']['pnl']
for mvp in [0.0,0.10,0.18,0.25,0.30,sig+0.18,0.45,0.50,2*sig+0.18,0.75,1.00]:
    S1=spot['MU']*(1+mvp); v=bs(S1,1300,4/365,mu['iv'])*100; pnl=v-mu['cost']
    rows.append([f"${S1:,.0f}", f"{mvp:+.1%}", f"${v:,.0f}", f"{pnl:+,.0f}", f"{pnl/mu['cost']:+.0%}", f"{pnl+others:+,.0f}", f"{(pnl+others)/5000:+.0%}", f"{(pnl+others3)/5000:+.0%}"])
S.append(tbl(rows,[0.9,0.65,0.8,0.9,0.9,1.5,0.9,0.95], font=7.9))

S.append(h1("Backtest: Six-Week Forward Returns","4")); S.append(sub("(overlapping 42-day windows from two years of weekly closes, n = 99 per name; thresholds use each leg's entry IV)"))
rows=[["Ticker","n","Real. Vol","Entry IV","Mean 6wk","Max 6wk","Base thr.","Hit Base","Bull thr.","Hit Bull","Gam. thr.","Hit Gam."]]
for tk in ["MU","RTX","NVDA","INTC","GDX","AMD","BA","MRVL"]:
    v=bt[tk]; rows.append([tk+("" if tk in ("MU","RTX","NVDA") else "*"), str(v['n']), f"{v['rv']:.1%}", f"{v['iv']:.1%}", f"{v['mean']:+.1%}", f"{v['mx']:+.1%}", f"{v['base']:.0%}", f"{v['hb']:.0%}", f"{v['bull']:.1%}", f"{v['hu']:.0%}", f"{v['gam']:.1%}", f"{v['hg']:.0%}"])
S.append(tbl(rows,[0.6,0.35,0.65,0.6,0.65,0.65,0.6,0.6,0.6,0.6,0.65,0.65]))
S.append(Paragraph("* Not in the V5 book; shown as candidates the optimizer screened and left at zero (INTC, GDX and RTX appear in the vol-normalized book).", NOTE))
S.append(h2("Key Findings"))
S += bullets([
 f"<b>RTX carries {1455/dep:.0%} of premium and {8400/P['scen']['Base']['pnl']:.0%} of Base Case P&L, yet its +18% threshold has printed in {bt['RTX']['hb']:.0%} of 99 windows (maximum +{bt['RTX']['mx']:.1%}).</b> The optimizer is buying the ladder's assumption, not RTX's history; the Base Case column of this book is the least historically supported of any version.",
 f"MU is unchanged from V3 at the 1300 strike and remains the leg with the strongest backtest: {bt['MU']['hb']:.0%} / {bt['MU']['hu']:.0%} / {bt['MU']['hg']:.0%} hit rates on its three thresholds and a mean six-week return of +{bt['MU']['mean']:.1%}.",
 f"Versus V3 (which held one RTX 200C), the optimized book adds four RTX contracts and drops MRVL and GDX: Base rises from {S3['Base']['ret']:+.0%} to {ret(P,'Base'):+.0%}, Bull from {S3['Bull']['ret']:+.0%} to {ret(P,'Bull'):+.0%}, Gamma Upside from {S3['Gamma']['ret']:+.0%} to {ret(P,'Gamma'):+.0%}; Flat is unchanged at the premium.",
 "Liquidity is clean in every leg: MU 3,722, NVDA 11,600 and RTX 1,928 open interest, with markets $0.10 to $0.70 wide. Five RTX contracts against 1,928 open interest is 0.3% of the strike.",
 "In-window dated catalysts (approximate): RTX third-quarter report Oct 20–21 (the book's largest satellite trades through its print); FOMC Oct 27–28; SK Hynix third-quarter results late October (read-through to MU). NVDA (Nov 18–19) and MU (December) report after the exit.",
])
S.append(h1("Assessment"))
S.append(Paragraph(
 f"RWS V5 is the mathematical maximum of the standing ladder under the memo's rules: mean P&L of ${P['obj']:,.0f} across the four cases against ${(S3['Flat']['pnl']+S3['Base']['pnl']+S3['Bull']['pnl']+S3['Gamma']['pnl'])/4:,.0f} for V3 and "
 f"${(S4['Flat']['pnl']+S4['Base']['pnl']+S4['Bull']['pnl']+S4['Gamma']['pnl'])/4:,.0f} for V4, with returns of {ret(P,'Flat'):+.0%} / {ret(P,'Base'):+.0%} / {ret(P,'Bull'):+.0%} / {ret(P,'Gamma'):+.0%}. It achieves that by concentrating 90% of premium in two names, "
 f"MU and RTX, and by leaning on the uniform +18% Base Case where RTX is cheapest. The vol-normalized check produces a different satellite set (INTC x4) and a lower standing-ladder Base Case ({NR['standing_ret']['Base']:+.0%}), "
 f"which is the measure of how much of V5's Base Case is a ladder artifact. Where the objective is reweighted by historical hit rates, or a tighter single-name cap is imposed, the allocation moves back toward "
 f"the V3 and V4 satellite sets. The anchor does not move: MU 1300C is selected under every constraint set that permits it.", BODY))

from addendum_jan2026 import addendum
S += addendum("5")
S.append(h1("Endnotes"))
S += [Paragraph(t, EN) for t in [
 "(1) Entry Monday, October 5, 2026; exit Monday, November 16, 2026; contracts expire Friday, November 20, 2026. Dates in the catalyst list are approximate.",
 "(2) Candidate universe: every Nov 20 '26 call quoted from Interactive Brokers on October 2 for Versions 3 through 4 (MU, NVDA, RTX, LMT, MRVL, SKHY, GDX, BA, AMD, LITE, INTC, TER, VICR, DRAM). Filters for the primary run: entry delta ≥ 0.20 by Black-Scholes at 46 days to expiry (r = 4%, q = 0%, mid implied volatility), call open interest ≥ 500, DRAM excluded, MU required with exactly one contract, satellite single-name premium ≤ 35% of the book. Entry cost per contract is the quoted mid multiplied by 100.",
 "(3) Objective: equal-weighted mean of the four case P&Ls (Flat 0%; Base +18%; Bull +18% + 1 s.d.; Gamma Upside +18% + 2 s.d.; s.d. = entry IV × √(42/365)), each marked on November 16, 2026 by Black-Scholes at four days to expiry at entry IV. Solved exactly by dynamic programming over the budget in $5 steps with one contract combination chosen per name. The flat re-rate rows raise every leg's IV uniformly at the stated mark and are solved by bisection.",
 "(4) Backtest: Interactive Brokers weekly closes, two-year lookback through the September 28, 2026 bar, overlapping six-week forward returns, n = 99 per name.",
 "(5) Statement figures are as printed on the January 1–30, 2026 J.P. Morgan Securities statement. Blotter statistics are parsed from its trade-activity section and capture 134 closing transactions totaling $22,224 against the statement's $22,602 net realized.",
 "Model code: memos/optimize_v5.py (optimizer) and memos/candidates.py (quote universe); scenario and backtest code in memos/ritts_6wk_model_v3.py.",
]]
S += disclosure("memo", "Mythos", "Donald B. Ritts III",
 extra=["<b>Statement Example.</b> The January 2026 statement presented in the addendum is a single selected period and may not be representative of all periods or of the Sleeve's own outcome. It should not be "
        "assumed that the Sleeve will make equally successful or comparable trades. The positions in that statement were entered under different market conditions and with a different structure (30–45 "
        "concurrent lines, one- to two-week tenors) from the Sleeve presented herein.",
        "<b>Optimization.</b> The allocation herein maximizes a model objective over a fixed quote set and a fixed scenario definition. It is sensitive to both: a different scenario definition (shown as the vol-normalized check) "
        "produces a different allocation, and fills at prices other than the quoted mids change the result. The optimizer has no view on the likelihood of any case."])
doc.build(S); print("ok v5")
