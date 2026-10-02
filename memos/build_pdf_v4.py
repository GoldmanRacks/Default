import json
from math import sqrt, log, exp
from statistics import NormalDist
from reportlab.platypus import Spacer, Table, TableStyle
from reportlab.lib.units import inch
from bxpe import *

M = json.load(open("model_out_v4.json")); V3 = json.load(open("model_out.json")); V4A = json.load(open("model_out_v4a.json")); V4B = json.load(open("model_out_v4b.json"))
pick, legs, scen, bt, screen, FR = M["pick"], M["legs"], M["scen"], M["bt"], M["screen"], M["flat_rerate"]
spot = {"INTC":120.72,"TER":418.93,"AMD":620.00,"LITE":1050.49,"VICR":308.78,"DRAM":62.01,"BA":192.35,"MU":1091.89,"NVDA":231.59,"RTX":186.12,"LMT":506.50,"MRVL":269.30,"SKHY":191.40,"GDX":86.13}
N = NormalDist().cdf; R=0.04
def bs(S,K,T,iv):
    if T<=0: return max(S-K,0)
    d1=(log(S/K)+(R+.5*iv*iv)*T)/(iv*sqrt(T)); return S*N(d1)-K*exp(-R*T)*N(d1-iv*sqrt(T))
dep=M["deployed"]; cash=M["cash"]; p=pick["DRAM"]; nD=dict(legs)["DRAM"]; TH=42/365; sig=p["iv"]*sqrt(TH)
lo,hi=40.0,80.0
for _ in range(80):
    m_=(lo+hi)/2
    if bs(m_,p["K"],4/365,p["iv"])*100 < p["cost"]: lo=m_
    else: hi=m_
BE=(lo+hi)/2
f5=scen.get("Flat+5"); f10=scen.get("Flat+10")

doc = make_doc("Ritts_6_week_Wedding_Model_V4_DRAM_ITM.pdf", "RWS V4", "MYTHOS-RWS-V4-20261002", "October 2026 RWS Update", "Ritts Wedding Sleeve V4")
S = title_block("OCTOBER 2026", "Ritts Wedding Sleeve &#8211; Version 4 (&#8220;RWS V4&#8221;)",
    f"RWS V4 swaps the single out-of-the-money MU 1300C anchor of Version 3 for in-the-money calls on the Roundhill Memory ETF {defined('DRAM', 'ticker')}, adds AMD and INTC as the semiconductor satellite legs in place of RTX, with INTC chosen over TER on liquidity, keeping NVDA, BA, MRVL and GDX, "
    f"on the same October 5 entry and November 16, 2026 exit<super><font size=7>(1)</font></super>")
S.append(stats([(f"{nD}&times; DRAM 55C","in-the-money anchor, delta 0.762",f"${p['cost']*nD:,.0f} premium, {p['cost']*nD/5000:.0%} of book; two contracts released to fund AMD"),
                (f"{scen['Base']['ret']:+.0%}","Base Case return on book",f"vs. {V3['scen']['Base']['ret']:+.0%} for RWS V3 (Nov 16 '26 mark)<super>(3)</super>"),
                (f"{scen['Gamma']['ret']:+.0%}","Gamma Upside Case return on book",f"vs. {V3['scen']['Gamma']['ret']:+.0%} for RWS V3; AMD and INTC carry {(scen['Gamma']['rows']['AMD']['pnl']+scen['Gamma']['rows']['INTC']['pnl'])/scen['Gamma']['pnl']:.0%} of it")]))
S.append(h1("Book Construction","2")); S.append(sub("(Nov 20 '26 calls; entry Oct 5 '26; DRAM by the in-the-money rule, delta &ge; 0.70 then deepest open interest; NVDA, INTC, BA, MRVL and GDX at the 0.20 delta floor; AMD at a relaxed 0.18 floor)"))
rows=[["Leg","Ctr","Spot","Entry $/ctr","Delta","Gamma","Gamma/$","Mid-IV","Call OI","Deployed $","vs. V3"]]
for tk,n in legs:
    q=pick[tk]; d=("replaces MU 1300C, x1" if tk=="DRAM" else ("new (RTX slot)" if tk in ("AMD","INTC") else ("new" if tk=="BA" else "same")))
    rows.append([f"{tk} {q['K']}C", str(n), f"{spot[tk]:,.2f}", f"${q['cost']:,.0f}", f"{q['delta']:.3f}", f"{q['gamma']:.5f}", f"{q['gpp']:.3f}", f"{q['iv']:.1%}", f"{q['oi']:,}", f"${q['cost']*n:,.0f}", d])
rows.append(["Cash / dry powder","–","–","–","–","–","–","–","–",f"${cash:,.0f}","$12"]); rows.append(["Total","","","","","","","","","$5,000",""])
S.append(tbl(rows,[1.0,0.35,0.6,0.7,0.5,0.62,0.6,0.55,0.6,0.75,1.1], bold_last=True, font=7.9))
S.append(Paragraph(f"DRAM holds a basket of memory names (MU, SK Hynix, SanDisk, Western Digital and peers), so the anchor is no longer a single-name bet: V3's 61% MU weight becomes a {p['cost']*nD/5000:.0%} "
 f"basket weight spread across three contracts. The in-the-money structure changes the payoff shape rather than the size of the bet. At $9.40 the 55C carries $7.01 of intrinsic value and $2.39 of time value, "
 f"so a flat print costs {abs(scen['Flat']['rows']['DRAM']['ret']):.0%} of the leg rather than 100%, and every dollar of DRAM upside above 55 is captured at 0.76 delta from the first dollar. "
 f"AMD and INTC take the RTX slot. INTC replaces LITE from the prior draft: the two candidates for that slot, INTC and TER, were screened head-to-head below and INTC was selected on execution and fit. "
 f"At $360 per contract (155C, delta 0.211) two INTC contracts cost a third of one LITE 1500C, which lets BA and MRVL return and GDX go back to two contracts; the book carries seven legs with ${cash:,.0f} cash. "
 f"AMD stays at the relaxed 0.18 floor (760C, $1,230) because the 740C at 0.224 would push the book over $5,000.", BODY))
S += note("Please reference the Endnotes for sourcing and methodology. (1) Hold is 42 calendar days. (2) Delta and gamma by Black-Scholes at 46 days to expiry, r = 4%, q = 0%; entry cost is the quoted mid times 100. BA 215C: mid 3.78, IV 37.8%, 1,096 open interest. "
          "DRAM listed April 2026; its two-year backtest therefore holds 27 weekly bars (21 six-week windows).")

S.append(h1("Premium Breakdown and DRAM Strike Screen","2")); S.append(sub("(% of deployed premium; ten DRAM strikes screened at 46 days to expiry; mid-IV 55–63%, 30-day realized 51.6%)"))
labels=[f"{tk} {pick[tk]['K']}C" for tk,n in legs]; vals=[pick[tk]['cost']*n/dep*100 for tk,n in legs]
rows=[["Strike","Mid $","IV","Delta","Intrinsic","Time value","Cost/ctr","Call OI","Verdict"]]
for r in screen["DRAM"]:
    intr=max(spot["DRAM"]-r["K"],0); v = "Selected" if r["K"]==pick["DRAM"]["K"] else ("Below 0.70 delta" if r["delta"]<0.70 else ("Thin OI" if r["oi"]<500 else "Deeper ITM, less OI"))
    rows.append([f"{r['K']}C", f"{r['mid']:.2f}", f"{r['iv']:.1%}", f"{r['delta']:.3f}", f"{intr:.2f}", f"{r['mid']-intr:.2f}", f"${r['cost']:,.0f}", f"{r['oi']:,}", v])
right=[tbl(rows,[0.45,0.45,0.45,0.45,0.5,0.55,0.55,0.55,0.9], font=7.4), Spacer(1,4),
       Paragraph("The 55C is the deepest-open-interest strike above the 0.70 delta floor (11,656 contracts against single digits at 52, 54 and 56). The 50C is deeper in the money (0.868) at $1,335 per contract "
                 "but only two fit the budget; the 60C has the most open interest on the chain (19,017) but sits at 0.614 delta, below the in-the-money floor.", BODY)]
two=Table([[pie(labels, vals), right]], colWidths=[2.9*inch, USABLE-2.9*inch])
two.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),0),('RIGHTPADDING',(0,0),(-1,-1),6)]))
S.append(two)
S.append(h2("INTC Versus TER for the Satellite Slot (Nov 20 '26)"))
def screen_tbl(tk, floor, bidask):
    rows=[["Strike","Bid / Ask","Mid $","IV","Delta","Gamma/$","Cost/ctr","Call OI","Verdict"]]
    for r in screen[tk]:
        v = "Selected" if r["K"]==pick[tk]["K"] else (f"Below {floor:.2f} floor" if r["delta"]<floor else "More premium")
        rows.append([f"{r['K']}C", bidask[r['K']], f"{r['mid']:.2f}", f"{r['iv']:.1%}", f"{r['delta']:.3f}", f"{r['gpp']:.3f}", f"${r['cost']:,.0f}", f"{r['oi']:,}", v])
    return tbl(rows,[0.6,1.0,0.6,0.6,0.6,0.65,0.75,0.65,1.2])
S.append(screen_tbl("INTC",0.20,{140:"6.05 / 6.20",145:"5.05 / 5.20",150:"4.25 / 4.35",155:"3.55 / 3.65",160:"2.97 / 3.10"})); S.append(Spacer(1,4))
TP=V4B['pick']['TER']; TS=V4B['screen']['TER']
rows=[["Strike","Bid / Ask","Mid $","IV","Delta","Gamma/$","Cost/ctr","Call OI","Verdict"]]
for r in TS:
    v = "TER pick (alt. book)" if r["K"]==TP["K"] else ("Below 0.20 floor" if r["delta"]<0.20 else "More premium")
    rows.append([f"{r['K']}C", {490:"18.00 / 24.70",500:"18.40 / 20.60",510:"13.90 / 18.40",520:"12.00 / 17.80",530:"12.30 / 17.00",540:"9.00 / 13.50"}[r['K']], f"{r['mid']:.2f}", f"{r['iv']:.1%}", f"{r['delta']:.3f}", f"{r['gpp']:.3f}", f"${r['cost']:,.0f}", f"{r['oi']:,}", v])
S.append(tbl(rows,[0.6,1.0,0.6,0.6,0.6,0.65,0.75,0.65,1.2])); S.append(Spacer(1,4))
bi=bt['INTC']; bte=bt['TER']
rows=[["Criterion","INTC 155C","TER 520C","Edge"],
      ["Entry IV / 2-yr realized", f"{bi['iv']:.1%} / {bi['rv']:.1%}", f"{bte['iv']:.1%} / {bte['rv']:.1%}", "INTC (IV 9 pts over realized vs. 17 for TER)"],
      ["Gamma per $ premium", f"{pick['INTC']['gpp']:.3f}", f"{TP['gpp']:.3f}", "INTC, 13x"],
      ["Cost per contract / delta", f"${pick['INTC']['cost']:,.0f} / {pick['INTC']['delta']:.3f}", f"${TP['cost']:,.0f} / {TP['delta']:.3f}", "INTC: two contracts for a quarter of TER's premium"],
      ["Call open interest at strike", f"{pick['INTC']['oi']:,}", f"{TP['oi']:,}", "INTC, 20x"],
      ["Bid / ask width (% of mid)", "$0.10 (3%)", "$5.80 (39%)", "INTC"],
      ["Hit +18% in 6 wks (n = 99)", f"{bi['hb']:.0%}", f"{bte['hb']:.0%}", "TER"],
      ["Hit Bull / Gamma thresholds", f"{bi['hu']:.0%} / {bi['hg']:.0%}", f"{bte['hu']:.0%} / {bte['hg']:.0%}", "INTC"],
      ["Max 6-wk move / mean", f"+{bi['mx']:.0%} / +{bi['mean']:.1%}", f"+{bte['mx']:.0%} / +{bte['mean']:.1%}", "INTC"],
      ["Legs the slot can fund", "INTC x2 + BA + MRVL + GDX x2", "TER x1 + BA + GDX x2 (MRVL out)", "INTC"]]
S.append(tbl(rows,[1.9,1.5,1.5,2.4], first_col_medium=True))
S.append(Paragraph(f"INTC wins the slot on seven of nine criteria. TER's one edge, a higher historical Base Case hit rate ({bte['hb']:.0%} against {bi['hb']:.0%}), comes with no Gamma-threshold hit in 99 windows and a maximum "
 f"six-week move of +{bte['mx']:.0%} against INTC's +{bi['mx']:.0%}; TER's November chain also carries the thin open interest and wide markets that removed VICR and LITE (2\u2013339 contracts per strike, $2\u2013$6 wide). "
 f"The TER book is modeled alongside for reference.", BODY))

S.append(h1("Scenario Ladder and Portfolio Payout","3")); S.append(sub("(P&L marked Nov 16 '26 at 4 days to expiry, Black-Scholes at entry IV; Base +18% uniform; Bull +18% + 1 s.d.; Gamma Upside +18% + 2 s.d., 42-day s.d. per name)"))
rows=[["Leg","Flat (0%)","Base +18%","Bull (+18% + 1 s.d.)","Gamma Upside (+18% + 2 s.d.)"]]
for tk,n in legs:
    q=pick[tk]
    def cell(s): r=scen[s]['rows'][tk]; return f"{r['pnl']:+,.0f} ({r['ret']:+.0%})"
    def mv(s): return f"{scen[s]['rows'][tk]['move']:+.1%}"
    rows.append([f"{tk} {q['K']}C (x{n})", cell('Flat'), cell('Base'), f"{cell('Bull')} @ {mv('Bull')}", f"{cell('Gamma')} @ {mv('Gamma')}"])
S.append(tbl(rows,[1.2,1.1,1.2,1.7,1.9])); S.append(Spacer(1,6))
rows=[["Scenario","Mark","V4 P&L","V4 Ending Value","V4 Return","TER alt.","AMD-only alt.","V3 (ref.)"]]
A=V4A['scen']; T=V4B['scen']
rows.append(["Flat (0% spot, entry IV)","Nov 16, 4 DTE", f"{scen['Flat']['pnl']:+,.0f}", f"${scen['Flat']['end']:,.0f}", f"{scen['Flat']['ret']:+.1%}", f"{T['Flat']['ret']:+.1%}", f"{A['Flat']['ret']:+.1%}", f"{V3['scen']['Flat']['ret']:+.1%}"])
if f5: rows.append([f"Flat + vol re-rate (IV +{f5['dvol']*100:.0f} pts)","Oct 30, 21 DTE", f"{f5['pnl']:+,.0f}", f"${f5['end']:,.0f}", f"{f5['ret']:+.1%}", f"+{T['Flat+5']['dvol']*100:.0f} pts", f"+{A['Flat+5']['dvol']*100:.0f} pts", "n/a"])
if f10: rows.append([f"Flat + vol re-rate (IV +{f10['dvol']*100:.0f} pts)","Oct 30, 21 DTE", f"{f10['pnl']:+,.0f}", f"${f10['end']:,.0f}", f"{f10['ret']:+.1%}", f"+{T['Flat+10']['dvol']*100:.0f} pts", f"+{A['Flat+10']['dvol']*100:.0f} pts", "n/a"])
for s,lab in [("Base","Base Case (+18%)"),("Bull","Bull Case (+18% + 1 s.d.)"),("Gamma","Gamma Upside Case (+18% + 2 s.d.)")]:
    v=scen[s]; w=V3['scen'][s]; rows.append([lab,"Nov 16, 4 DTE", f"{v['pnl']:+,.0f}", f"${v['end']:,.0f}", f"{v['ret']:+.1%}", f"{T[s]['ret']:+.1%}", f"{A[s]['ret']:+.1%}", f"{w['ret']:+.1%}"])
S.append(tbl(rows,[1.9,0.9,0.8,0.95,0.8,0.8,0.9,0.75], font=7.8))
S.append(Paragraph(f"TER alternative: DRAM 55C x1, NVDA 255C, AMD 760C, TER 520C, BA 215C, GDX 98C x2; ${V4B['deployed']:,.0f} deployed, ${V4B['cash']:,.0f} cash (MRVL does not fit). AMD-only alternative: DRAM 55C x2, NVDA 255C, AMD 760C, BA 215C, MRVL 330C, GDX 98C; $4,928 deployed, $72 cash.", NOTE))
S += note(PAST_PERF)

S.append(h2("Flat Case: Conditions for a +5% to +10% Book Return"))
S.append(Paragraph("A long-call book marked at four days to expiry is worth only intrinsic value at a flat print, so a flat-spot gain can come only from implied volatility re-rating while time value remains. "
 "The table solves, for each exit mark, the uniform rise in implied volatility across all five legs that lifts the book to +5% and to +10% with spot unchanged. The two rows carried into the ladder above "
 "use the October 30 mark (21 days to expiry).", BODY))
rows=[["Exit mark","Days to expiry","Flat return at entry IV","IV rise for +5%","IV rise for +10%"]]
for lab,r in FR.items():
    rows.append([lab, str(r["dte"]), f"{r['flat_ret']:+.1%}", f"+{r['dvol_5']*100:.0f} pts" if r["dvol_5"] is not None else "not reachable", f"+{r['dvol_10']*100:.0f} pts" if r["dvol_10"] is not None else "not reachable"])
S.append(tbl(rows,[1.6,1.1,1.5,1.4,1.4]))
S.append(Paragraph(f"Read: on October 23, with every leg at its entry IV plus {FR['Oct 23 (28 DTE)']['dvol_5']*100:.0f} points, the book marks +5% with no move in any underlying; +{FR['Oct 23 (28 DTE)']['dvol_10']*100:.0f} points marks +10%. "
 f"At the November 16 mark the required re-rate exceeds +{FR['Nov 16 (4 DTE)']['dvol_5']*100:.0f} points, so the +5% to +10% flat outcome is an early-exit, vol-event case, not an expiry case. "
 f"The AMD contract is the drag on the flat re-rate: a uniform point shift is a small proportional change for a 56%-IV call that is {pick['AMD']['cost']/dep:.0%} of premium.", BODY))

S.append(h2("DRAM Anchor-Leg Sensitivity"))
S.append(Paragraph(f"DRAM is {p['cost']*nD/5000:.0%} of premium. The 42-day one-standard-deviation move at {p['iv']:.1%} IV is {sig:.1%} (${spot['DRAM']*sig:,.2f}). Breakeven at the four-day mark is DRAM of "
 f"approximately ${BE:,.2f} ({BE/spot['DRAM']-1:+.1%}; versus ${p['K']+p['mid']:,.2f} / {(p['K']+p['mid'])/spot['DRAM']-1:+.1%} at expiry). Other legs are held at the Base Case column for the book-level row; "
 f"the V3 column shows the MU 1300C book at the same percentage move in MU.", BODY))
XROWS=[]
rows=[["DRAM on Nov 16","Move",f"Call value (x{nD})","DRAM leg P&L","DRAM leg return","Book P&L (rest @ Base)","Book return","V3 book return"]]
others=scen['Base']['pnl']-scen['Base']['rows']['DRAM']['pnl']; others3=V3['scen']['Base']['pnl']-V3['scen']['Base']['rows']['MU']['pnl']; pm=V3['pick']['MU']
for mvp in [-0.20,-0.10,0.0,0.10,0.18,0.25,0.30,sig+0.18,0.45,2*sig+0.18,0.75,1.00]:
    S1=spot['DRAM']*(1+mvp); v=bs(S1,p['K'],4/365,p['iv'])*100*nD; pnl=v-p['cost']*nD
    v3=bs(spot['MU']*(1+mvp),1300,4/365,pm['iv'])*100-pm['cost']
    rows.append([f"${S1:,.2f}", f"{mvp:+.1%}", f"${v:,.0f}", f"{pnl:+,.0f}", f"{pnl/(p['cost']*nD):+.0%}", f"{pnl+others:+,.0f}", f"{(pnl+others)/5000:+.0%}", f"{(v3+others3)/5000:+.0%}"])
    XROWS.append((mvp,(pnl+others)/5000,(v3+others3)/5000))
XOVER=next((m for m,a,b_ in XROWS if b_>a), 1.0); V3_LEADS_ALL=all(b_>a for m,a,b_ in XROWS if m>=0)
LEAD=[r for r in XROWS if r[0]>=0 and r[1]>=r[2]]; LAST=LEAD[-1] if LEAD else None
OVER=next(((m,a,b_) for m,a,b_ in XROWS if LAST and m>LAST[0] and b_>a), None)
if V3_LEADS_ALL:
    XO_TXT=f"On the anchor-only axis (other legs held at the Base Case) V3 leads at every print from flat upward: V4's satellites contribute {others:+,.0f} against {others3:+,.0f} in V3. V4 overtakes V3 only when the satellite legs run with the anchor, which is what the Bull and Gamma Upside columns assume."
elif LAST and OVER:
    XO_TXT=f"On the anchor-only axis (other legs held at the Base Case) V4 leads through a {LAST[0]:+.0%} anchor move (V4 {LAST[1]:+.0%} vs. V3 {LAST[2]:+.0%}), carried by the in-the-money anchor and the restored satellites; V3 overtakes from {OVER[0]:+.0%} ({OVER[2]:+.0%} vs. {OVER[1]:+.0%}) as the 1300C's percentage payoff accelerates."
else:
    XO_TXT="On the anchor-only axis (other legs held at the Base Case) V4 leads at every modeled print."
S.append(tbl(rows,[0.95,0.6,0.9,0.9,0.95,1.45,0.9,0.95], font=7.9))

S.append(h1("Backtest: Six-Week Forward Returns","4")); S.append(sub("(overlapping 42-day windows from weekly closes; n = 99 per name, DRAM n = 21 since its April 2026 listing; thresholds use each leg's entry IV)"))
rows=[["Ticker","n","Real. Vol","Entry IV","Mean 6wk","Max 6wk","Base thr.","Hit Base","Bull thr.","Hit Bull","Gam. thr.","Hit Gam."]]
for tk in ["DRAM","MU","NVDA","AMD","INTC","TER","RTX","BA","MRVL","GDX"]:
    v=bt[tk]; rows.append([tk+("*" if tk in ("MU","RTX","TER") else ""), str(v['n']), f"{v['rv']:.1%}", f"{v['iv']:.1%}", f"{v['mean']:+.1%}", f"{v['mx']:+.1%}", f"{v['base']:.0%}", f"{v['hb']:.0%}", f"{v['bull']:.1%}", f"{v['hu']:.0%}", f"{v['gam']:.1%}", f"{v['hg']:.0%}"])
S.append(tbl(rows,[0.6,0.35,0.65,0.6,0.65,0.65,0.6,0.6,0.6,0.6,0.65,0.65]))
S.append(Paragraph("* MU, RTX and TER are not in the V4 Sleeve: MU and RTX are the legs replaced; TER is the candidate not selected (modeled in the TER alternative).", NOTE))
S.append(h2("Key Findings"))
S += bullets([
 f"<b>DRAM</b> has cleared +18% in {bt['DRAM']['hb']:.0%} of its 21 windows (mean +{bt['DRAM']['mean']:.1%}, maximum +{bt['DRAM']['mx']:.1%}), with realized volatility of {bt['DRAM']['rv']:.1%} against a {bt['DRAM']['iv']:.1%} entry IV: the basket has moved more than its options price, but on a sample of one spring-to-autumn stretch.",
 f"Versus V3 the columns move as follows: Flat {V3['scen']['Flat']['ret']:+.0%} to {scen['Flat']['ret']:+.0%} (the in-the-money DRAM contract retains intrinsic value), Base {V3['scen']['Base']['ret']:+.0%} to {scen['Base']['ret']:+.0%} (AMD and INTC are both out of the money at +18%), Bull {V3['scen']['Bull']['ret']:+.0%} to {scen['Bull']['ret']:+.0%}, Gamma Upside {V3['scen']['Gamma']['ret']:+.0%} to {scen['Gamma']['ret']:+.0%}.",
 XO_TXT,
 f"<b>AMD and INTC</b> are the semiconductor tail legs. At a +18% print AMD 760C is $28 out of the money ({scen['Base']['rows']['AMD']['ret']:.0%}) and INTC 155C is $13 out ({scen['Base']['rows']['INTC']['ret']:.0%}), which holds the Base Case to {scen['Base']['ret']:+.0%}; at +2 s.d. they return {scen['Gamma']['rows']['AMD']['ret']:+.0%} and {scen['Gamma']['rows']['INTC']['ret']:+.0%} on the leg and together supply {scen['Gamma']['rows']['AMD']['pnl']+scen['Gamma']['rows']['INTC']['pnl']:+,.0f} of the Gamma Upside column.",
 f"Versus the TER alternative the INTC book is {(scen['Flat']['ret']-V4B['scen']['Flat']['ret'])*100:+.0f} points on Flat, {(scen['Base']['ret']-V4B['scen']['Base']['ret'])*100:+.0f} on Base, {(scen['Bull']['ret']-V4B['scen']['Bull']['ret'])*100:+.0f} on Bull and {(scen['Gamma']['ret']-V4B['scen']['Gamma']['ret'])*100:+.0f} on Gamma Upside, with MRVL kept in the book and the slot executed in a chain 20 times deeper at a market 3% wide instead of 39%.",
 "Concentration: the largest single-name exposure in V4 is MU at roughly a quarter of DRAM's basket weight, against 61% of premium in V3; the sleeve's memory beta is unchanged in direction but diversified across the ETF's holdings.",
 "In-window dated catalysts (approximate): SK Hynix third-quarter results late October and Samsung preliminary results early October (both DRAM constituents); INTC third-quarter report Oct 22\u201323, BA Oct 21\u201322 and AMD Nov 3\u20134 (all three trade through earnings inside the window); FOMC Oct 27–28. NVDA (Nov 18–19) and MU (December) report after the exit.",
])
S.append(h1("Assessment"))
S.append(Paragraph(
 f"RWS V4 trades the V3 anchor's convexity for carry and breadth. Flat and Base Case outcomes improve by {(scen['Flat']['ret']-V3['scen']['Flat']['ret'])*100:.0f} and {(scen['Base']['ret']-V3['scen']['Base']['ret'])*100:.0f} points respectively; "
 f"Bull and Gamma Upside give up {(V3['scen']['Bull']['ret']-scen['Bull']['ret'])*100:.0f} and {(V3['scen']['Gamma']['ret']-scen['Gamma']['ret'])*100:.0f} points. The anchor's single-name risk is replaced by basket risk across the "
 f"ETF's holdings, and the three-contract structure allows the leg to be scaled down in thirds rather than closed outright. The +5% to +10% flat-spot outcome exists only as an early-exit vol-event: "
 f"it requires a uniform +{FR['Oct 23 (28 DTE)']['dvol_5']*100:.0f} to +{FR['Oct 23 (28 DTE)']['dvol_10']*100:.0f} point rise in implied volatility marked on October 23, or +{FR['Oct 30 (21 DTE)']['dvol_5']*100:.0f} to +{FR['Oct 30 (21 DTE)']['dvol_10']*100:.0f} points on October 30, and is not reachable at the November 16 mark. "
 f"With INTC in the slot the book is seven legs across memory (DRAM), GPU (NVDA, AMD), foundry/CPU (INTC), AI networking (MRVL), aerospace (BA) and gold miners (GDX): Base Case {scen['Base']['ret']:+.0%}, Bull {scen['Bull']['ret']:+.0%}, Gamma Upside {scen['Gamma']['ret']:+.0%}. "
 f"AMD remains the one leg below the 0.20 floor and the largest single premium ({pick['AMD']['cost']/5000:.0%}); every other leg trades in a chain with four-figure open interest and a market no wider than $0.40. "
 f"Three in-window earnings prints (INTC, BA, AMD) are the dated catalysts; the DRAM anchor carries no single-name print inside the window.", BODY))

from addendum_jan2026 import addendum
S += addendum("5")
S.append(h1("Endnotes"))
S += [Paragraph(t, EN) for t in [
 "(1) Entry Monday, October 5, 2026; exit Monday, November 16, 2026; contracts expire Friday, November 20, 2026. Dates in the catalyst list are approximate.",
 "(2) Delta and gamma by Black-Scholes at 46 days to expiry (r = 4%, q = 0%) using each contract's mid implied volatility. Entry cost per contract is the Interactive Brokers SMART mid at the October 2, 2026 close multiplied by 100. NVDA and GDX: minimum entry delta 0.20, then maximum gamma per dollar of premium. AMD: floor relaxed to 0.18 so that it fits the book, then maximum gamma per dollar; INTC and TER at the 0.20 floor. DRAM anchor: minimum entry delta 0.70, then deepest call open interest.",
 "(3) Scenarios are marked on November 16, 2026 by Black-Scholes at four days to expiry using each leg's entry implied volatility. The per-name standard deviation is entry IV multiplied by the square root of 42/365. The two flat re-rate rows are marked on October 30, 2026 (21 days to expiry) with every leg's implied volatility raised by the stated number of points and spot unchanged; the rise is solved by bisection to the +5% and +10% book targets.",
 "(4) Backtest: Interactive Brokers weekly closes, two-year lookback through the September 28, 2026 bar, overlapping six-week forward returns, n = 99 per name; DRAM n = 21 (27 weekly bars since listing).",
 "(5) Statement figures are as printed on the January 1–30, 2026 J.P. Morgan Securities statement. Blotter statistics are parsed from its trade-activity section and capture 134 closing transactions totaling $22,224 against the statement's $22,602 net realized.",
 "Model code: memos/ritts_6wk_model_v3.py (run with argument v4; v4a for the AMD-only alternative; v4b for the TER alternative). AMD, INTC and TER quotes and two-year weekly closes were pulled October 2.",
]]
S += disclosure("memo", "Mythos", "Donald B. Ritts III",
 extra=["<b>Statement Example.</b> The January 2026 statement presented in the addendum is a single selected period and may not be representative of all periods or of the Sleeve's own outcome. It should not be "
        "assumed that the Sleeve will make equally successful or comparable trades. The positions in that statement were entered under different market conditions and with a different structure (30–45 "
        "concurrent lines, one- to two-week tenors) from the Sleeve presented herein."])
doc.build(S); print("ok v4")
