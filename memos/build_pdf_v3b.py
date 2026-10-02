import json
from math import sqrt, log, exp
from statistics import NormalDist
from reportlab.platypus import Spacer, Table, TableStyle
from reportlab.lib.units import inch
from bxpe import *

M = json.load(open("model_out_v3b.json")); V3 = json.load(open("model_out.json"))
pick, legs, scen, bt, screen = M["pick"], M["legs"], M["scen"], M["bt"], M["screen"]
spot = {"BA":192.35,"MU":1091.89,"NVDA":231.59,"RTX":186.12,"LMT":506.50,"MRVL":269.30,"SKHY":191.40,"GDX":86.13}
N = NormalDist().cdf; R=0.04
def bs(S,K,T,iv):
    if T<=0: return max(S-K,0)
    d1=(log(S/K)+(R+.5*iv*iv)*T)/(iv*sqrt(T)); return S*N(d1)-K*exp(-R*T)*N(d1-iv*sqrt(T))
dep=M["deployed"]; cash=M["cash"]; p=pick["MU"]; TH=42/365; sig=p["iv"]*sqrt(TH)
lo,hi=1100.0,1600.0
for _ in range(80):
    m_=(lo+hi)/2
    if bs(m_,1350,4/365,p['iv'])*100 < p['cost']: lo=m_
    else: hi=m_
BE=(lo+hi)/2

doc = make_doc("Ritts_6_week_Wedding_Model_V3b_MU_SKHY_BA.pdf", "RWS V3b", "MYTHOS-RWS-V3B-20261002", "October 2026 RWS Update", "Ritts Wedding Sleeve V3b")
S = title_block("OCTOBER 2026", "Ritts Wedding Sleeve &#8211; Version 3b Variant (&#8220;RWS V3b&#8221;)",
    f"RWS V3b is the seven-leg variant of the $5,000 Version 3 sleeve {defined('Sleeve')}: the MU anchor moves out to the 1350C, SKHY is restored, and BA takes the LMT slot beside RTX, "
    f"on the same October 5 entry and November 16, 2026 exit<super><font size=7>(1)</font></super>")
S.append(stats([(f"${dep:,.0f}","premium deployed",f"seven legs, ${cash:,.0f} cash"),
                (f"{scen['Gamma']['ret']:+.0%}","Gamma Upside Case return on book",f"vs. {V3['scen']['Gamma']['ret']:+.0%} for RWS V3<super>(3)</super>"),
                (f"{p['cost']/5000:.0%}","MU 1350C share of premium","vs. 61% for the V3 1300C")]))
S.append(h1("Book Construction","2")); S.append(sub("(Nov 20 '26 calls; entry Oct 5 '26; delta floor relaxed to 0.18 for MU and BA only; all other legs keep their V3 strikes at 0.20)"))
rows=[["Leg","Ctr","Spot","Entry $/ctr","Delta","Gamma","Gamma/$","Mid-IV","Call OI","Deployed $","vs. V3"]]
for tk,n in legs:
    q=pick[tk]; d = ("new" if tk in ("BA","SKHY") else ("1300C to 1350C" if tk=="MU" else ("x2 to x1" if tk=="GDX" else "same")))
    rows.append([f"{tk} {q['K']}C", str(n), f"{spot[tk]:,.2f}", f"${q['cost']:,.0f}", f"{q['delta']:.3f}", f"{q['gamma']:.5f}", f"{q['gpp']:.3f}", f"{q['iv']:.1%}", f"{q['oi']:,}", f"${q['cost']*n:,.0f}", d])
rows.append(["Cash / dry powder","–","–","–","–","–","–","–","–",f"${cash:,.0f}","$12"]); rows.append(["Total","","","","","","","","","$5,000",""])
S.append(tbl(rows,[1.0,0.35,0.6,0.7,0.5,0.62,0.6,0.55,0.6,0.75,1.0], bold_last=True, font=7.9))
S.append(Paragraph("Three changes versus RWS V3: (i) the MU anchor moves one strike out to the MU Nov 20 '26 1350C ($2,355, delta 0.182), which breaks the 0.20 delta floor but frees $710; (ii) SKHY 230C "
 "is restored ($610); (iii) BA takes the LMT slot as the second aerospace/defense leg alongside RTX (BA Nov 20 '26 220C, $280). To fit all seven legs in $5,000 the floor is relaxed to 0.18 for MU and BA "
 "only, and GDX drops from two contracts to one.", BODY))
S += note("Please reference the Endnotes for sourcing and methodology. (1) Hold is 42 calendar days. (2) Delta and gamma by Black-Scholes at 46 days to expiry, r = 4%, q = 0%; entry cost is the quoted mid times 100.")

S.append(h1("Premium Breakdown and BA Strike Screen","2")); S.append(sub("(% of deployed premium; five BA strikes screened at 46 days to expiry; BA mid-IV 38.0% vs. 29.4% 30-day realized)"))
labels=[f"{tk} {pick[tk]['K']}C" for tk,n in legs]; vals=[pick[tk]['cost']*n/dep*100 for tk,n in legs]
rows=[["Strike","Mid $","IV","Delta","Gamma/$","Cost/ctr","Call OI","Verdict"]]
for r in screen["BA"]:
    v = "Selected (0.18 floor)" if r["K"]==pick["BA"]["K"] else ("Fails 0.18 floor" if r["delta"]<0.18 else ("Clears 0.20; no fit" if r["K"]==215 else "Lower gamma/$"))
    rows.append([f"{r['K']}C", f"{r['mid']:.2f}", f"{r['iv']:.1%}", f"{r['delta']:.3f}", f"{r['gpp']:.4f}", f"${r['cost']:,.0f}", f"{r['oi']:,}", v])
right=[tbl(rows,[0.5,0.45,0.45,0.45,0.55,0.6,0.55,1.05], font=7.8), Spacer(1,5),
       Paragraph(f"The 220C is the maximum gamma-per-premium strike at the relaxed floor and carries the deepest open interest in the BA chain (7,602). The 215C clears 0.20 but at $378 would push the "
                 f"book $74 over $5,000 unless GDX were released. Versus LMT: BA 220C screens at {pick['BA']['gpp']:.3f} gamma per dollar (4.3 times LMT's best 0.086) for $280 against LMT's $655–$930, "
                 f"with two-year realized volatility 9 points higher and a +18% Base Case hit rate of {bt['BA']['hb']:.0%} versus LMT's {bt['LMT']['hb']:.0%}.", BODY)]
two=Table([[pie(labels, vals), right]], colWidths=[2.9*inch, USABLE-2.9*inch])
two.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),0),('RIGHTPADDING',(0,0),(-1,-1),6)]))
S.append(two)

S.append(h1("Scenario Ladder and Portfolio Payout","3")); S.append(sub("(P&L marked Nov 16 '26 at 4 days to expiry, Black-Scholes at entry IV; Base +18% uniform; Bull +18% + 1 s.d.; Gamma Upside +18% + 2 s.d.)"))
rows=[["Leg","Flat (0%)","Base +18%","Bull (+18% + 1 s.d.)","Gamma Upside (+18% + 2 s.d.)"]]
for tk,n in legs:
    q=pick[tk]
    def cell(s): r=scen[s]['rows'][tk]; return f"{r['pnl']:+,.0f} ({r['ret']:+.0%})"
    def mv(s): return f"{scen[s]['rows'][tk]['move']:+.1%}"
    rows.append([f"{tk} {q['K']}C (x{n})", cell('Flat'), cell('Base'), f"{cell('Bull')} @ {mv('Bull')}", f"{cell('Gamma')} @ {mv('Gamma')}"])
S.append(tbl(rows,[1.2,1.1,1.2,1.7,1.9])); S.append(Spacer(1,6))
rows=[["Scenario","V3b P&L","V3b Ending Value","V3b Return","V3 Return (ref.)","Diff. vs. V3"]]
for s,lab in [("Flat","Flat (0%)"),("Base","Base Case (+18%)"),("Bull","Bull Case (+18% + 1 s.d.)"),("Gamma","Gamma Upside Case (+18% + 2 s.d.)")]:
    v=scen[s]; w=V3['scen'][s]; rows.append([lab, f"{v['pnl']:+,.0f}", f"${v['end']:,.0f}", f"{v['ret']:+.1%}", f"{w['ret']:+.1%}", f"{(v['ret']-w['ret'])*100:+.1f} pts"])
S.append(tbl(rows,[2.2,1.0,1.2,1.0,1.1,1.0]))
S += note(PAST_PERF)
S.append(h2("MU Anchor-Leg Sensitivity (1350C)"))
S.append(Paragraph(f"MU is {p['cost']/5000:.0%} of premium (V3: 61%). The 42-day one-standard-deviation move at {p['iv']:.1%} IV is {sig:.1%} (${spot['MU']*sig:,.0f}). Breakeven at the four-day mark is "
 f"MU of approximately ${BE:,.0f} ({BE/spot['MU']-1:+.1%}; versus ${1350+p['mid']:,.0f} / {(1350+p['mid'])/spot['MU']-1:+.1%} at expiry). The other six legs are held at the Base Case column.", BODY))
rows=[["MU on Nov 16","Move","Call value","MU leg P&L","MU leg return","Book P&L (rest @ Base)","Book return","V3 book return"]]
others = scen['Base']['pnl']-scen['Base']['rows']['MU']['pnl']; others3 = V3['scen']['Base']['pnl']-V3['scen']['Base']['rows']['MU']['pnl']
for mvp in [0.0,0.10,0.18,0.25,0.30,sig+0.18,0.45,0.50,2*sig+0.18,0.75,1.00]:
    S1=spot['MU']*(1+mvp); v=bs(S1,1350,4/365,p['iv'])*100; pnl=v-p['cost']
    v3=bs(S1,1300,4/365,V3['pick']['MU']['iv'])*100-V3['pick']['MU']['cost']
    rows.append([f"${S1:,.0f}", f"{mvp:+.1%}", f"${v:,.0f}", f"{pnl:+,.0f}", f"{pnl/p['cost']:+.0%}", f"{pnl+others:+,.0f}", f"{(pnl+others)/5000:+.0%}", f"{(v3+others3)/5000:+.0%}"])
S.append(tbl(rows,[0.9,0.65,0.8,0.9,0.9,1.5,0.9,0.95], font=7.9))

S.append(h1("Backtest: Six-Week Forward Returns","4")); S.append(sub("(overlapping 42-day windows from two years of weekly closes, n = 99 per name; thresholds use each leg's entry IV)"))
rows=[["Ticker","Real. Vol","Entry IV","Mean 6wk","Max 6wk","Base thr.","Hit Base","Bull thr.","Hit Bull","Gam. thr.","Hit Gam."]]
for tk in ["MU","NVDA","RTX","BA","MRVL","GDX","LMT"]:
    v=bt[tk]; rows.append([tk+("*" if tk=="LMT" else ""), f"{v['rv']:.1%}", f"{v['iv']:.1%}", f"{v['mean']:+.1%}", f"{v['mx']:+.1%}", f"{v['base']:.0%}", f"{v['hb']:.0%}", f"{v['bull']:.1%}", f"{v['hu']:.0%}", f"{v['gam']:.1%}", f"{v['hg']:.0%}"])
S.append(tbl(rows,[0.6,0.7,0.65,0.7,0.7,0.65,0.65,0.65,0.65,0.7,0.7]))
S.append(Paragraph("* LMT is not in the Sleeve; shown as the leg BA replaces. SKHY (13 weekly bars since listing) is excluded.", NOTE))
S.append(h2("Key Findings"))
S += bullets([
 f"<b>BA</b> clears the +18% Base Case in {bt['BA']['hb']:.0%} of windows (LMT {bt['LMT']['hb']:.0%}; RTX {bt['RTX']['hb']:.0%}), the strongest of the three aerospace/defense candidates on historical frequency; its Bull (+{bt['BA']['bull']:.1%}) and Gamma (+{bt['BA']['gam']:.1%}) thresholds each printed once in 99 windows (maximum +{bt['BA']['mx']:.1%}).",
 f"<b>MU 1350C</b> shifts the leg's thresholds by only 0.3 points versus the 1300C, so hit rates are unchanged at {bt['MU']['hb']:.0%} / {bt['MU']['hu']:.0%} / {bt['MU']['hg']:.0%}; what changes is the payoff shape: at a +18% print the 1350C loses {scen['Base']['rows']['MU']['ret']:.0%} versus {V3['scen']['Base']['rows']['MU']['ret']:.0%} for the 1300C, while at +57% it returns {scen['Gamma']['rows']['MU']['ret']:+.0%} versus {V3['scen']['Gamma']['rows']['MU']['ret']:+.0%}.",
 "Two memory legs (MU and SKHY) now sit side by side: 59% of premium is memory/HBM beta. SKHY's window contains SK Hynix's third-quarter report (late October), a dated catalyst MU itself lacks in-window.",
 "In-window dated catalysts (approximate): BA third-quarter report Oct 21–22 and RTX Oct 20–21 (both aerospace/defense legs trade through earnings); FOMC Oct 27–28; SK Hynix late October. NVDA (Nov 18–19) and MU (December) report after the exit.",
])
S.append(h1("Assessment"))
S.append(Paragraph(
 f"RWS V3b is the broader book: seven legs, five sectors of convexity, MU at {p['cost']/5000:.0%} of premium rather than 61%, and MU contributing {scen['Bull']['rows']['MU']['pnl']/scen['Bull']['pnl']:.0%} / "
 f"{scen['Gamma']['rows']['MU']['pnl']/scen['Gamma']['pnl']:.0%} of Bull / Gamma Upside Case P&L (V3: 54% / 58%). The price of the breadth is in the Base Case column: {scen['Base']['ret']:+.0%} versus "
 f"{V3['scen']['Base']['ret']:+.0%}, because the 1350C needs MU above ${BE:,.0f} on November 16 to be worth its premium versus $1,299 for the 1300C. On the MU-only axis (other legs at the Base Case) V3 leads at "
 f"every MU print by a near-constant 80 points: the 1300C carries $5,000 more intrinsic value per contract than the 1350C at any MU level above both strikes while costing $710 more. V3b overtakes V3 only "
 f"when the satellite legs also run (Bull Case +{(scen['Bull']['ret']-V3['scen']['Bull']['ret'])*100:.0f} points, Gamma Upside Case +{(scen['Gamma']['ret']-V3['scen']['Gamma']['ret'])*100:.0f} points): it is the better "
 f"book in a broad semis/defense/gold move and the worse one in a MU-only move. Two legs (MU, BA) sit below the 0.20 delta floor at 0.182 and 0.187; the other five hold it.", BODY))

from addendum_jan2026 import addendum
S += addendum("5")
S.append(h1("Endnotes"))
S += [Paragraph(t, EN) for t in [
 "(1) Entry Monday, October 5, 2026; exit Monday, November 16, 2026; contracts expire Friday, November 20, 2026. Dates in the catalyst list are approximate.",
 "(2) Delta and gamma by Black-Scholes at 46 days to expiry (r = 4%, q = 0%) using each contract's mid implied volatility. Entry cost per contract is the Interactive Brokers SMART mid at the October 2, 2026 close multiplied by 100. Strike selection: minimum entry delta 0.20 (0.18 for MU and BA in this variant), then maximum gamma per dollar of premium.",
 "(3) Scenarios are marked on November 16, 2026 by Black-Scholes at four days to expiry using each leg's entry implied volatility (no change in volatility assumed). The per-name standard deviation is entry IV multiplied by the square root of 42/365.",
 "(4) Backtest: Interactive Brokers weekly closes, two-year lookback through the September 28, 2026 bar, overlapping six-week forward returns, n = 99 per name.",
 "(5) Statement figures are as printed on the January 1–30, 2026 J.P. Morgan Securities statement. Blotter statistics are parsed from its trade-activity section and capture 134 closing transactions totaling $22,224 against the statement's $22,602 net realized.",
 "Model code: memos/ritts_6wk_model_v3.py (run with argument v3b).",
]]
S += disclosure("memo", "Mythos", "Donald B. Ritts III",
 extra=["<b>Statement Example.</b> The January 2026 statement presented in the addendum is a single selected period and may not be representative of all periods or of the Sleeve's own outcome. It should not be "
        "assumed that the Sleeve will make equally successful or comparable trades. The positions in that statement were entered under different market conditions and with a different structure (30–45 "
        "concurrent lines, one- to two-week tenors) from the Sleeve presented herein."])
doc.build(S); print("ok v3b")
