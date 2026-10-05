import json
from reportlab.platypus import Spacer, Table, TableStyle, KeepTogether
from reportlab.lib.units import inch
from reportlab.lib.styles import ParagraphStyle
from bxpe import *
R=json.load(open("model_out_v6_1500.json")); P=R["unhedged"]["model"]; H=R["hedged"]["model"]; V6=json.load(open("model_out_v6.json"))["primary"]
BK=1500; legs=P["legs"]; dep=P["deployed"]; cash=P["cash"]
CELL=ParagraphStyle("cell", fontName="SourceSans3-Regular", fontSize=7.4, leading=8.8, textColor=BLACK)
def cell(t): return Paragraph(t, CELL)
def ret(o,c): return o["scen"][c]["ret"]
def legname(l): return f"{l['tk']} {l['K']}{l['cp']}"
def exp_s(l): return "Nov 20" if l["exp"].startswith("2026-11") else "Dec 18"
def usd(x): return f"{'+' if x>=0 else '-'}${abs(x):,.0f}"
sched={s["label"]:s for s in P["schedule"]}
by_tr={t:[l for l in legs if l["tranche"]==t] for t in ("T1","T2","T3")}
tr_cost={t:sum(l["cost"]*l["n"] for l in by_tr[t]) for t in by_tr}
ncon=sum(l["n"] for l in legs)
gam=sorted(legs,key=lambda l:-l["pnl"]["Gamma"]*l["n"]); gtot=P["scen"]["Gamma"]["pnl"]
NV=[l for l in legs if l["tk"]=="NVDA"][0]; GL=[l for l in legs if l["tk"]=="GLD"][0]

doc = make_doc("Ritts_6_week_Wedding_Model_V6_1500.pdf", "RWS V6-S", "MYTHOS-RWS-V6S-1500-20261005", "October 2026 RWS Update", "Ritts Wedding Sleeve V6 at $1,500")
S = title_block("OCTOBER 2026", "Ritts Wedding Sleeve &#8211; Version 6 at $1,500 (&#8220;RWS V6-S&#8221;)",
    "RWS V6-S runs the V6 process on $1,500 of starting capital: three dated tranches, an event rule that keeps every line out of its own earnings print, vol-value, liquidity and delta screens, and a 25% ticket cap, "
    f"now $375. Five lines and {ncon} contracts survive; the book is {sched['Oct 5 entry T1']['pct']:.0%} deployed on October 5, {sched['Oct 22 entry T2']['pct']:.0%} after October 22 and {sched['Nov 5 entry T3']['pct']:.0%} after November 5, with exits on November 16 and November 25"
    "<super><font size=7>(1)</font></super>")
S.append(stats([("$1,500","starting capital",f"${dep:,.0f} deployed in {ncon} contracts across 5 lines; ${cash:,.0f} cash"),
                (f"{ret(P,'Gamma'):+.0%}","Gamma Upside Case return on book",f"{usd(P['scen']['Gamma']['pnl'])}; Base {ret(P,'Base'):+.0%}, Bull {ret(P,'Bull'):+.0%}; vol-normalized<super>(3)</super>"),
                (f"{ret(P,'Flat'):+.0%}","Flat Case return on book",f"{usd(P['scen']['Flat']['pnl'])}; a hedged variant ({ret(H,'Shock'):+.0%} in the Shock Case) is on page 3")]))

S.append(h1("What Changes at $1,500","2")); S.append(sub("(the V6 rules do not move; the ticket cap does, and it decides which names survive)"))
S += bullets([
 "<b>The ticket cap does the selecting.</b> V6's rule is that no contract may exceed 25% of the book at its entry price. At $5,000 that is $1,250; at $1,500 it is $375. At a $375 cap, 26 contract-and-tranche combinations clear the delta, liquidity and volatility-value screens; the event rule leaves 17, across seven names (GDX, NVDA, RTX, GLD, DRAM, BA and the SPY put).",
 "<b>Dropped by price:</b> VRT ($723), SKHY ($473), CEG ($686), GEV, AMD, MU and MRVL, plus every contract on LMT, NOC and LHX that had already failed on liquidity. The AI power sleeve is therefore empty; memory / AI compute, gold and defense remain.",
 "<b>Dropped by the event rule:</b> RTX, BA and INTC cannot be bought in Tranche 1 (they report Oct 20, Oct 27 and Oct 22 inside the hold); NVDA cannot be held to the Nov 25 exit (reports Nov 18); DRAM waits for SK hynix (late October). The tranche each name sits in is therefore forced, not chosen.",
 "<b>Whole contracts are the unit.</b> A line is one or two contracts of one strike. The search is exhaustive over every combination that satisfies the constraints (a line cap of 30% / $450, a sleeve cap of 40% / $600, at least four lines and three sleeves, 8% cash), maximizing the mean of the Base, Bull and Gamma Upside P&L on the vol-normalized ladder.",
 f"<b>The hedge is priced out.</b> V6 spends 7% on a SPY December put. The cheapest passing put here (the 690, 0.08 delta) is ${[l for l in H['legs'] if l['tk']=='SPY'][0]['cost']:,.0f}, {[l for l in H['legs'] if l['tk']=='SPY'][0]['cost']/BK:.0%} of the book, and a hedged book (page 3) gives up {ret(P,'Base')-ret(H,'Base'):.0%} of Base Case return for it. The primary book is unhedged; the hedged book is shown as a variant.",
])
S += note("Please reference the Endnotes for sourcing and methodology. (1) Tranche 1 contracts expire Nov 20 and are marked Nov 16 at 4 days to expiry; Tranche 2 and 3 contracts expire Dec 18 and are marked Nov 25 at 23 days to expiry. "
          "(2) Quotes are the Oct 2 close, except the SPY puts, quoted live on Oct 5. Tranche 1 fills on Oct 5 will differ from the model entry prices; re-quote before ordering. The strategy and its January 2026 realized precedent are described in the RWS V6 memo (introduction and addendum).")

S.append(h1("Staged Book","2")); S.append(sub("(Oct 2 quotes; Tranche 2 and 3 entry prices are indicative at the tranche date with spot unchanged)"))
rows=[["Tr.","Entry","Leg","Exp.","Ctr","Sleeve","Quoted mid","Entry $/ctr","Delta","IV","IV/HV","Gamma/$100","Open int.","Deployed"]]
for t in ("T1","T2","T3"):
    for l in by_tr[t]:
        rows.append([t,l["entry"][5:].replace("-","/"),legname(l),exp_s(l),str(l["n"]),cell(l["sleeve"]),f"{l['mid']:.2f}",f"${l['cost']:,.0f}",f"{l['delta']:+.2f}",f"{l['iv']:.0%}",f"{l['ivhv']:.2f}",f"{l['gamma_per_100']:.2f}",f"{l['oi']:,}",f"${l['cost']*l['n']:,.0f}"])
    rows.append(["",f"Tranche {t[1]} subtotal"]+[""]*11+[f"${tr_cost[t]:,.0f}"])
rows.append(["","Cash"]+[""]*11+[f"${cash:,.0f}"]); rows.append(["","Total","","",str(ncon)]+[""]*8+["$1,500"])
S.append(tbl(rows,[0.28,0.42,0.75,0.45,0.28,1.0,0.5,0.55,0.45,0.35,0.4,0.6,0.5,0.6],bold_last=True,font=7.0))
S.append(Paragraph("Gamma/$100 is the dollar P&L from the second-order term of a 1% move per $100 of premium, the ranking statistic of the V3&#8211;V6 process. Calls are in 0.20&#8211;0.27 delta; implied volatility is below one-year realized in GDX, RTX, DRAM and GLD and at value in NVDA.", NOTE))
S.append(h2("Why These Five"))
S += bullets([f"<b>{legname(l)}{' x'+str(l['n']) if l['n']>1 else ''} ({exp_s(l)}, bought {l['entry'][5:].replace('-','/')}).</b> {l['why']}." for l in legs])
S.append(h2("Premium at Risk Through the Calendar"))
rows=[["Date","Event","Lines held","Premium at risk","% of book","Book theta / day"]]
for s in P["schedule"]: rows.append([s["date"][5:].replace("-","/"),cell(s["label"]),str(s["n"]),f"${s['premium']:,.0f}",f"{s['pct']:.0%}",f"{s['theta']:+,.0f}"])
S.append(tbl(rows,[0.6,2.3,0.8,1.1,0.8,1.1]))
S.append(Paragraph(f"One contract (${sched['Oct 14 CPI']['premium']:,.0f}) is at risk through the October 14 CPI and the first defense prints; ${sched['Oct 28 FOMC']['premium']:,.0f} through the FOMC and the midterms; the full ${dep:,.0f} only for the last three weeks of the window.", BODY))

S.append(h1("Scenario Ladder","3")); S.append(sub("(each leg marked at its own exit; moves are multiples of the leg's own standard deviation over its own hold, at entry IV; Shock is -2 s.d. with IV +10 points)"))
rows=[["Leg (ctr)","Hold","1 s.d.","Flat","Base (+1 s.d.)","Bull (+2 s.d.)","Gamma (+3 s.d.)","Shock (-2 s.d., IV +10)"]]
for l in legs:
    n=l["n"]; rows.append([f"{legname(l)} (x{n})",f"{l['hold']}d",f"{l['sig']:.1%}",f"{l['pnl']['Flat']*n:+,.0f}",f"{l['pnl']['Base']*n:+,.0f} ({l['pnl']['Base']/l['cost']:+.0%})",
                 f"{l['pnl']['Bull']*n:+,.0f} ({l['pnl']['Bull']/l['cost']:+.0%})",f"{l['pnl']['Gamma']*n:+,.0f} ({l['pnl']['Gamma']/l['cost']:+.0%})",f"{l['pnl']['Shock']*n:+,.0f}"])
rows.append(["Book","","",f"{P['scen']['Flat']['pnl']:+,.0f}",f"{P['scen']['Base']['pnl']:+,.0f}",f"{P['scen']['Bull']['pnl']:+,.0f}",f"{P['scen']['Gamma']['pnl']:+,.0f}",f"{P['scen']['Shock']['pnl']:+,.0f}"])
S.append(tbl(rows,[1.1,0.4,0.45,0.6,1.0,1.05,1.15,1.1],bold_last=True,font=7.4)); S.append(Spacer(1,6))
rows=[["Scenario","Primary: P&L","Ending value","Primary: return","Hedged variant","V6 at $5,000 (ref.)"]]
for c,lab in [("Flat","Flat (0%, entry IV)"),("Base","Base (+1 s.d. per leg)"),("Bull","Bull (+2 s.d. per leg)"),("Gamma","Gamma Upside (+3 s.d. per leg)"),("Shock","Shock (-2 s.d., IV +10 pts)")]:
    rows.append([lab,f"{P['scen'][c]['pnl']:+,.0f}",f"${P['scen'][c]['end']:,.0f}",f"{ret(P,c):+.1%}",f"{ret(H,c):+.1%}",f"{V6['scen'][c]['ret']:+.1%}"])
for c,lab in [("Base","Standing ladder: Base +18% uniform"),("Bull","Standing: Bull +18% + 1 s.d."),("Gamma","Standing: Gamma +18% + 2 s.d.")]:
    rows.append([cell(lab),f"{P['stand'][c]['pnl']:+,.0f}",f"${BK+P['stand'][c]['pnl']:,.0f}",f"{P['stand'][c]['ret']:+.1%}",f"{H['stand'][c]['ret']:+.1%}",f"{V6['stand'][c]['ret']:+.1%}"])
S.append(tbl(rows,[2.1,1.0,1.0,1.0,1.1,1.2]))
hl=H["legs"]
S.append(Paragraph("<b>Hedged variant:</b> "+", ".join(f"{legname(l)} x{l['n']} ({exp_s(l)}, ${l['cost']*l['n']:,.0f})" for l in sorted(hl,key=lambda l:(l['tranche'],l['tk'])))+
  f". It drops the RTX and DRAM lines of the primary book and adds the SPY 690 put and BA 215C; deployed ${H['deployed']:,.0f}. Standing-ladder rows use the V3&#8211;V5 uniform +18% on every leg; on that ladder the low-IV legs (GLD, RTX, BA) print 2&#8211;3 standard deviations, which is why those rows sit far above the normalized ones.", NOTE))
S += note(PAST_PERF)
S.append(h2("Flat Case: Volatility Re-rate Needed for +5% / +10%"))
rows=[["Exit mark","Lines held","Flat return (entry IV)","IV rise for +5%","IV rise for +10%"]]
for k,r in P["rerate"].items(): rows.append([k,str(r["held"]),f"{r['flat_ret']:+.1%}",f"+{r['dvol_5']*100:.0f} pts" if r["dvol_5"] else "not reachable",f"+{r['dvol_10']*100:.0f} pts" if r["dvol_10"] else "not reachable"])
S.append(tbl(rows,[1.2,1.0,1.6,1.4,1.4]))

S.append(h1("Backtest and Screen Results","4")); S.append(sub("(overlapping windows from two years of weekly closes; window = the leg's hold in weeks; thresholds are the leg's own +1 / +2 / +3 s.d.)"))
rows=[["Leg","Weeks","n","1y realized","Entry IV","Mean","Median","Max","Min","Hit +1 s.d.","Hit +2 s.d.","Hit +3 s.d.","Hit -2 s.d."]]
for l in legs:
    b=l["bt"]; rows.append([legname(l),str(b["w"]),str(b["n"]),f"{l['hv']:.0%}",f"{l['iv']:.0%}",f"{b['mean']:+.1%}",f"{b['med']:+.1%}",f"{b['mx']:+.0%}",f"{b['mn']:+.0%}",f"{b['h1']:.0%}",f"{b['h2']:.0%}",f"{b['h3']:.0%}",f"{b['hneg']:.0%}"])
S.append(tbl(rows,[0.85,0.45,0.35,0.7,0.6,0.55,0.6,0.5,0.5,0.65,0.65,0.65,0.7],font=7.4))
S.append(Paragraph("DRAM has 24 weekly windows (listed 2026); its row is indicative.", NOTE))
rows=[["Name","Result at $375 ticket cap"]]
for a,b in [("GDX","Passes: 98C Nov, 100C Dec"),("NVDA","Passes in Tranche 1 only (reports Nov 18); Dec 260C passes screens but cannot be held to Nov 25"),("RTX","Passes in Tranche 2 or 3 (Dec 200C); Tranche 1 excluded by the Oct 20 print"),
            ("GLD","Passes only as Dec 410C in Tranche 3 ($346); Nov 405C is $484"),("DRAM","Passes as Dec 70C / 75C in Tranche 3 only (SK hynix, late October)"),("BA","Passes as Dec 215C / 220C in Tranche 3 only (Oct 27 print)"),
            ("INTC","Nov 155C passes screens; excluded by the Oct 22 print"),("SPY","690P and 695P pass; 690P is 18% of the book"),
            ("VRT, SKHY, CEG, GEV, AMD, MU, MRVL","Ticket above $375 at every quoted strike"),("NOC, LHX, LMT, VICR, LITE, TER","Open interest and spread, as in V4 and V6")]:
    rows.append([cell(a),cell(b)])
S.append(tbl(rows,[2.2,5.1],font=7.4))
S.append(h2("Rules of Engagement at Whole-Contract Size"))
S += bullets([
 "<b>Entry gates (unchanged from V6).</b> Tranche 2 proceeds on Oct 22 unless the Oct 14 CPI lifts December hike odds above ~90%; either delays it one week. Tranche 3 proceeds on Nov 5 unless the book is below -25% on Nov 4, in which case the weakest line is skipped and its cash kept.",
 "<b>Cuts.</b> Any line at -50% of its premium after half its hold is closed and not redeployed in that name. Any contract at 4 days to expiry is closed regardless of mark.",
 "<b>Profit-taking.</b> V6 sells thirds, which a one-contract line cannot do. The DRAM line (two contracts) sells one at +100%. Single-contract lines have a stop at +50% once they reach +150%, and are sold in full at +300% or at the exit date.",
 "<b>Roll-ups.</b> On Nov 16 the NVDA proceeds roll into a December contract only if they cover a whole contract at 25 delta; otherwise they go to cash.",
 "<b>Exits.</b> Nov 16 for Tranche 1 and Nov 25 for Tranches 2&#8211;3, before the Nov 18 NVDA print, before Thanksgiving, and three weeks before the December MU print.",
])
S.append(h1("Key Findings"))
mx3=max(legs,key=lambda l:l["bt"]["h3"]); z3=[legname(l) for l in legs if l["bt"]["h3"]==0]
S += bullets([
 f"<b>NVDA and GLD carry {(NV['pnl']['Gamma']*NV['n']+GL['pnl']['Gamma']*GL['n'])/gtot:.0%} of Gamma Upside P&L</b> on {(NV['cost']*NV['n']+GL['cost']*GL['n'])/dep:.0%} of premium: NVDA has the largest 42-day move in the book (one s.d. is {NV['sig']:.1%}, so +3 s.d. is {3*NV['sig']:.0%}), and GLD has the highest gamma per dollar of any contract that clears the screens ({GL['gamma_per_100']:.2f} per $100).",
 f"<b>The book is more convex than V6 at one-third the size.</b> Gamma Upside {ret(P,'Gamma'):+.0%} against {V6['scen']['Gamma']['ret']:+.0%} for V6 at $5,000, Bull {ret(P,'Bull'):+.0%} against {V6['scen']['Bull']['ret']:+.0%}, Base {ret(P,'Base'):+.0%} against {V6['scen']['Base']['ret']:+.0%}. The price is the Shock Case: {ret(P,'Shock'):+.0%} against {V6['scen']['Shock']['ret']:+.0%}, because the cheapest SPY put is 18% of the book at this size.",
 f"<b>Week one risks {sched['Oct 5 entry T1']['pct']:.0%} of the book.</b> One NVDA contract is held through the CPI; everything else is bought after its event clears.",
 f"<b>Where the ladder is least supported.</b> The +3 s.d. threshold has never printed in the lookback for {', '.join(z3) if z3 else 'no leg'}; the highest hit rate on +3 s.d. is {mx3['bt']['h3']:.0%} ({legname(mx3)}). The Gamma Upside column is the model's assumption for most of this book, not history.",
 f"<b>A flat tape costs {abs(ret(P,'Flat')):.0%}.</b> The re-rate table shows what would have to happen to implied volatility to avoid it.",
])
S.append(h1("Assessment"))
S.append(Paragraph(
 f"RWS V6-S is the V6 process at the size where whole contracts and a $375 ticket cap decide the book. Five lines and {ncon} contracts survive the screens and the event rule; the exhaustive search picks the combination with the highest mean Base / Bull / Gamma P&L: "
 f"{', '.join(legname(l)+(' x'+str(l['n']) if l['n']>1 else '') for l in sorted(legs,key=lambda l:(l['tranche'],l['tk'])))}. It returns {ret(P,'Flat'):+.0%} / {ret(P,'Base'):+.0%} / {ret(P,'Bull'):+.0%} / {ret(P,'Gamma'):+.0%} / {ret(P,'Shock'):+.0%} across Flat, Base, Bull, Gamma Upside and Shock "
 f"on the vol-normalized ladder, and {P['stand']['Base']['ret']:+.0%} / {P['stand']['Bull']['ret']:+.0%} / {P['stand']['Gamma']['ret']:+.0%} on the standing +18% ladder. Against V6 it trades the hedge and the AI-power sleeve for a higher upside; the hedged variant restores a "
 f"{ret(H,'Shock'):+.0%} Shock Case at {ret(H,'Base'):+.0%} Base. In both books a flat tape through the exits loses most of the premium.", BODY))
S.append(h1("Endnotes"))
S += [Paragraph(t, EN) for t in [
 "(1) Tranche 1: entry October 5, exit Monday November 16, 2026, contracts expiring November 20 (42-day hold). Tranche 2: entry October 22. Tranche 3: entry November 5. Both exit Wednesday November 25, 2026 in contracts expiring December 18, 2026. Event dates are from the Bigdata.com corporate calendar and public Federal Reserve and BLS schedules; CPI dates are approximate.",
 "(2) Quotes: Interactive Brokers. Nov 20 '26 mids and Dec 18 '26 bid/ask as quoted on October 2, 2026 after the close; SPY Dec 18 '26 690 and 695 puts quoted live October 5 with SPY at 770.53. Implied volatility is backed out of each mid by Black-Scholes (r = 4%, q = 0) at the quote date. Tranche 2 and 3 entry prices re-price that volatility at the tranche entry date with spot unchanged. Screens: delta 0.18&#8211;0.40 at entry (puts 0.08&#8211;0.22), open interest &#8805; 500, spread &#8804; 25% of mid, ticket &#8804; 25% of $1,500 ($375), call IV &#8804; 1.25&#215; one-year realized, no earnings date inside the hold.",
 "(3) Vol-normalized ladder: s.d. = entry IV &#215; &#8730;(hold / 365); Base, Bull and Gamma Upside move the underlying +1, +2 and +3 s.d. at entry IV; Shock moves it -2 s.d. and raises IV 10 points; each leg is marked at its own exit date. The standing ladder is the V3&#8211;V5 definition (Flat 0%; Base +18%; Bull +18% + 1 s.d.; Gamma Upside +18% + 2 s.d.). Optimizer: exhaustive search over one line per name (one or two contracts of one strike in one allowed tranche) subject to line &#8804; 30%, sleeve &#8804; 40%, Tranche 1 &#8804; 30%, Tranches 1&#8211;2 &#8804; 62%, total &#8804; 92%, at least four lines and three sleeves; objective is the mean of Base, Bull and Gamma Upside P&L.",
 "(4) Backtest: Interactive Brokers weekly closes, two-year lookback through the September 28, 2026 bar, overlapping forward returns over each leg's hold rounded to weeks; n = 99&#8211;102 for names with full history, 24 for DRAM. One-year realized volatility is the annualized standard deviation of the last 52 weekly log returns.",
 "Model code: memos/optimize_v6_small.py (search) and memos/model_v6.py (pricing, ladder, schedule); quote universe in memos/quotes_v6.py.",
]]
S += disclosure("memo", "Mythos", "Donald B. Ritts III",
 extra=["<b>Indicative Entries and Size.</b> Tranche 1 entry prices are model values at October 5 from October 2 quotes; Tranche 2 and 3 entry prices are model values at a future date under the assumption of unchanged spot and implied volatility. None are quotes. "
        "At $1,500 each contract is 6% to 23% of the book, a bid-ask spread of a few cents is a material share of the premium, and the book holds five lines; results are therefore more sensitive to fills and to any single line than the $5,000 book.",
        "<b>Optimization.</b> The allocation maximizes a model objective over a fixed quote set, fixed screens and a fixed scenario definition; it has no view on the likelihood of any case. A different objective, such as including the Shock Case, selects the hedged variant."])
doc.build(S); print("ok")
