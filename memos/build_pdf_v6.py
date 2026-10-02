import json
from reportlab.platypus import Spacer, Table, TableStyle, KeepTogether
from reportlab.lib.units import inch
from reportlab.lib.styles import ParagraphStyle
from bxpe import *
O=json.load(open("model_out_v6.json")); P=O["primary"]; MV=O["mu_variant"]; FL=O["front_loaded"]; SC=O["screen"]; TRN=O["tranches"]
legs=P["legs"]; dep=P["deployed"]; cash=P["cash"]; S5=json.load(open("model_out_v5.json"))["primary"]["scen"]
CELL=ParagraphStyle("cell", fontName="SourceSans3-Regular", fontSize=7.4, leading=8.8, textColor=BLACK)
def cell(t): return Paragraph(t, CELL)
def ret(o,c): return o["scen"][c]["ret"]
def legname(l): return f"{l['tk']} {l['K']}{l['cp']}"
def exp_s(l): return "Nov 20" if l["exp"].startswith("2026-11") else "Dec 18"
by_tr={t:[l for l in legs if l["tranche"]==t] for t in ("T1","T2","T3")}
tr_cost={t:sum(l["cost"]*l["n"] for l in by_tr[t]) for t in by_tr}
sched={s["label"]:s for s in P["schedule"]}

doc = make_doc("Ritts_6_week_Wedding_Model_V6_Redesign.pdf", "RWS V6", "MYTHOS-RWS-V6-20261002", "October 2026 RWS Update", "Ritts Wedding Sleeve V6")
S = title_block("OCTOBER 2026", "Ritts Wedding Sleeve &#8211; Version 6: Redesigned Book (&#8220;RWS V6&#8221;)",
    "RWS V6 keeps the V3&#8211;V5 process (short-dated out-of-the-money calls ranked on gamma per dollar of premium, Black-Scholes scenario ladder, two-year backtest) and rebuilds the book around it: "
    "three dated tranches instead of one entry, five sleeves instead of two, a crash-convexity leg, and quantitative screens on volatility value, liquidity and ticket size. "
    f"Entry begins October 5; the last exit is November 25, the day before Thanksgiving<super><font size=7>(1)</font></super>")
S.append(stats([(f"{sched['Oct 5 entry T1']['pct']:.0%}","of the book at risk in week one",f"{sched['Oct 22 entry T2']['pct']:.0%} after Oct 22, {sched['Nov 5 entry T3']['pct']:.0%} after Nov 5; a single Oct 5 entry would carry 92% from day one"),
                (f"{ret(P,'Gamma'):+.0%}","Gamma Upside Case return on book",f"Base {ret(P,'Base'):+.0%}, Bull {ret(P,'Bull'):+.0%}; vol-normalized +1, +2, +3 s.d. per leg over its own hold<super>(3)</super>"),
                (f"{ret(P,'Shock'):+.0%}","Shock Case return on book","every leg &#8722;2 s.d. with IV +10 points; the SPY put returns "+f"{[l for l in legs if l['tk']=='SPY'][0]['pnl']['Shock']:+,.0f}")]))

S.append(h1("How the Book Is Built","2")); S.append(sub("(the V3&#8211;V5 convexity process, re-applied with time, sleeve and volatility discipline)"))
S += bullets([
 "<b>Same engine.</b> Every candidate is a listed call (or, for the hedge, a put) 15&#8211;35 delta at entry, ranked on gamma per $100 of premium and priced on the same Black-Scholes ladder and two-year weekly backtest as Versions 3&#8211;5. Nothing is sold; maximum loss on any leg is its premium.",
 "<b>Three dated tranches, not one.</b> Tranche 1 (Oct 5&#8211;9) is the quietest week of the window: no CPI, no FOMC, no in-book earnings. It buys only the three legs with no dated event inside their hold and the deepest markets, and it carries "
 f"{sched['Oct 5 entry T1']['pct']:.0%} of the book. Tranche 2 (Oct 22&#8211;23) is bought after the October 14 CPI and after the RTX and Vertiv prints, so the defense and power legs enter on post-earnings, post-crush volatility. "
 "Tranche 3 (Nov 5&#8211;6) is bought after the October 28 FOMC and the November 3 midterms and takes the book to 92%. The Flat Case cost of the staging is time value not paid: the same nine lines bought on October 5 would cost "
 f"${FL['deployed']:,.0f}, 131% of the book.",
 "<b>Five sleeves with a 40% sleeve cap and a 25% ticket cap.</b> Memory / AI compute (36%), defense / geopolitics (18%), gold / real-asset (17%), AI power / grid (14%) and crash convexity (7%), leaving 8% cash for the roll-up rule. No single contract may exceed 25% of the book at its indicative entry; that rule, not a view, is what removes a single MU contract (27&#8211;57% of the book at every quoted strike and tranche date) in favor of the DRAM basket and SKHY. The MU-anchored variant is shown for comparison.",
 "<b>Volatility value screen.</b> Calls are bought only where implied volatility is at or below 1.25&#215; one-year realized; the book's calls average 0.98&#215;. Gold (0.94&#215;), GDX (0.85&#215;), DRAM (0.76&#215;) and RTX (0.91&#215;) are cheap on this measure; SKHY (1.11&#215;) and NVDA (1.07&#215;) are at value; nothing is bought above 1.15&#215;.",
 "<b>Liquidity screen.</b> Open interest &#8805; 500 and quoted spread &#8804; 25% of mid. The screen removes NOC, LHX, LMT and GEV (open interest of 4 to 468 at the relevant strikes), VICR, LITE and TER (carried over from V4), and the VRT 280/290/310 strikes in favor of the 300.",
 "<b>Event rule.</b> No leg is held through its own earnings unless the print is the thesis. RTX (Oct 20), VRT (Oct 21), BA (Oct 27) and SK hynix (late October) are therefore bought after their reports; NVDA (Nov 18) and MU (December) report after the exits; CEG (Nov 6) and AMD (Nov 3, ticket &gt; 25%) are excluded.",
 "<b>Crash convexity.</b> One SPY December 700 put (11.5 delta, $372, 7% of the book) is bought with Tranche 2 to cover the FOMC, the midterms and the reported intent to resume strikes on Iran after the election. It is the only leg that pays in the Shock Case and the only leg the volatility-value screen is waived for, because index puts always carry skew.",
])
S += note("Please reference the Endnotes for sourcing and methodology. (1) Tranche 1 contracts expire Nov 20 and are marked Nov 16 at 4 days to expiry; Tranche 2 and 3 contracts expire Dec 18 and are marked Nov 25 at 23 days to expiry. "
          "(2) Tranche 2 and 3 entry prices are indicative: the Oct 2 mid-implied volatility priced at the tranche entry date with spot unchanged. Live fills will differ with the drift to the entry date.")

S.append(h1("Macro, Geopolitical and Quantitative Backdrop","4")); S.append(sub("(what the calendar does to the book, and what the book does about it)"))
rows=[["Date","Event","Book action / exposure"]]
for d,e,a in [
 ("Oct 2","September payrolls (printed)","Reference point for the Oct 5 entry; no action"),
 ("Oct 5&#8211;9","Tranche 1 entry","GLD 405C, GDX 98C x2, NVDA 255C: $1,224, 24% of book; no dated event inside their holds"),
 ("Oct 14","September CPI","Held at 24%; gate for Tranche 2: a hot print that lifts the December hike above ~90% delays Tranche 2 one week"),
 ("Oct 16","Monthly expiration","No action"),
 ("Oct 20&#8211;22","RTX, NOC (20), GEV, VRT (21), LMT, INTC (22) report","Watch only; RTX and VRT are bought after their prints"),
 ("Oct 22&#8211;23","Tranche 2 entry","RTX 200C x2, VRT 300C, SPY 700P: $1,693, book to 58%"),
 ("Oct 27","Boeing reports","Watch; BA is bought after the print in Tranche 3"),
 ("Oct 27&#8211;28","FOMC (3.75&#8211;4.00%; ~70% hold priced, December hike ~83%)","Held at 58% with the SPY put on; a hike is the Shock Case trigger"),
 ("Late Oct","SK hynix third-quarter results; September PCE","Read-through to SKHY and DRAM before Tranche 3"),
 ("Nov 3","Midterm elections; AMD reports","Held at 58% with the put on; defense sleeve waits for the result"),
 ("Nov 5&#8211;6","Tranche 3 entry; October payrolls (6); CEG reports (6)","SKHY 230C x2, DRAM 70C x2, BA 215C: $1,690, book to 92%"),
 ("~Nov 12","October CPI","Held; first profit-taking checkpoint for Tranche 1"),
 ("Nov 16","Tranche 1 exit (4 DTE)","Close GLD, GDX, NVDA; roll winners into Dec strikes per the roll-up rule"),
 ("Nov 18&#8211;20","NVDA reports (18); monthly expiration (20)","NVDA is out of the book before its print"),
 ("Nov 25","Tranche 2 and 3 exit (23 DTE)","Close everything the day before Thanksgiving; December MU print is not held"),
]: rows.append([cell(d),cell(e),cell(a)])
S.append(tbl(rows,[0.85,2.55,3.9],font=7.4))
S.append(h2("Regime Read"))
S += bullets([
 "<b>Rates.</b> The Fed raised to 3.75&#8211;4.00% on September 16 and projects another increase; October 28 is priced ~70% hold after core PCE held at 3.4%, with a December hike ~83%. The two-year is near 4.9% and the ten-year near 5.2%, a two-decade high. A hiking Fed into 58.4 composite PMIs is the macro reason the book is staged and hedged rather than front-loaded: the policy path can re-price twice inside the window (Oct 28, and the Nov 12 CPI into December).",
 "<b>Geopolitics.</b> A Middle East war with Iran is live: tanker attacks in the Strait of Hormuz, strikes on regional refineries, a second carrier under consideration, 10,000 sailors and Marines being evaluated for the Gulf, and reporting that strikes could resume after the midterms. Qatar-mediated US&#8211;Iran talks are the de-escalation path. Russia&#8211;Ukraine and Taiwan remain open. This is the thesis for the defense sleeve (post-midterm clearing event), the gold sleeve (gold near $4,175 while real yields rise) and the SPY put.",
 "<b>Midterms (Nov 3).</b> Morgan Stanley's public-policy read: the executive-led agenda (tariffs, export controls, deregulation) does not change with Congress; what Congress moves is fiscal timing, including defense appropriations. The book treats the election as a volatility event to hold through with the put, and as the trigger for the defense tranche, not as a directional bet.",
 "<b>Memory.</b> Micron's September 30 call: DRAM is the principal constraint on data-center expansion; HBM 2027 volume is largely sold out at prices 'much higher' than 2026; HBM outgrows DRAM through 2028. The sleeve expresses this through the DRAM basket (MU is its largest holding) and SKHY rather than a single MU contract.",
 "<b>AI power.</b> Vertiv's CEO at the September Goldman conference: 'no sign of weakening... the pipeline is getting stronger and stronger.' VRT is 18% below its 13-week-ago level, the largest drawdown of any passing name; the leg is bought after the October 21 print.",
 "<b>Quantitative.</b> Thirteen-week momentum is positive in the AI names (NVDA +19%, AMD +19%, MU +13%, GDX +11%) and negative across defense and power (LHX &#8722;21%, VRT &#8722;18%, BA &#8722;15%, NOC &#8722;12%, GEV &#8722;11%, RTX &#8722;7%). Tranche 1 buys momentum; Tranches 2 and 3 buy the drawdowns after their catalysts clear. Implied volatility sits below one-year realized in gold, GDX, DRAM, RTX and MU and above it only in SKHY and NVDA, so the book is buying volatility at or below its realized cost.",
])

S.append(h1("Staged Book","2")); S.append(sub("(nine lines, twelve contracts; Oct 2 quotes; Tranche 2 and 3 entries indicative at the tranche date with spot unchanged)"))
rows=[["Tr.","Leg","Exp.","Ctr","Sleeve","Oct 2 mid","Entry $/ctr","Delta","IV","IV/HV","Gamma/$100","Call OI","Deployed"]]
for t in ("T1","T2","T3"):
    for l in by_tr[t]:
        rows.append([t,legname(l),exp_s(l),str(l["n"]),cell(l["sleeve"]),f"{l['mid']:.2f}",f"${l['cost']:,.0f}",f"{l['delta']:+.2f}",f"{l['iv']:.0%}",f"{l['ivhv']:.2f}",f"{l['gamma_per_100']:.2f}",f"{l['oi']:,}",f"${l['cost']*l['n']:,.0f}"])
    rows.append(["",f"Tranche {t[1]} subtotal","","","","","","","","","","",f"${tr_cost[t]:,.0f}"])
rows.append(["","Cash","","","","","","","","","","",f"${cash:,.0f}"]); rows.append(["","Total","","12","","","","","","","","","$5,000"])
S.append(tbl(rows,[0.3,0.85,0.5,0.3,1.25,0.6,0.7,0.5,0.4,0.45,0.7,0.55,0.65],bold_last=True,font=7.4))
S.append(Paragraph("Gamma/$100 is the dollar P&L from the second-order term of a 1% move, per $100 of premium; it is the ranking statistic of the V3&#8211;V5 process. Low-IV names (GLD, RTX, BA, NVDA) rank highest because their premium is smallest relative to the move a one-point change produces; "
 "the book deliberately spans sleeves instead of taking the ranking to its end (which would be all gold).", NOTE))
labels=list(P["sleeves"].keys())+["Cash"]; vals=[v/50 for v in list(P["sleeves"].values())+[cash]]
S.append(KeepTogether([h2("Sleeve Map and Screen Results"), Table([[pie(labels,vals,width=3.1*inch,height=2.5*inch),
   tbl([["Name","Best strike","Result"]]+[[a,b,cell(c)] for a,b,c in [
     ("MU","Dec 1350C","ticket $1,872&#8211;$2,832 &gt; 25% cap; shown as variant"),("AMD","Dec 750C","ticket $1,528 &gt; 25% cap; reports Nov 3"),
     ("CEG","Dec 300C","passes screens; reports Nov 6 inside the hold"),("LMT","Dec 550C","OI 267; spread 12%"),("NOC","Dec 540C","OI 102; spread 46%"),
     ("LHX","Dec 270C","OI 655 but spread 67%"),("GEV","Dec 1200C","OI 284; ticket $1,781"),("MRVL","Nov 330C","passes; crowded out by SKHY/DRAM on IV/HV"),
     ("INTC","Nov 155C","passes; reports Oct 22, 73% IV; left out"),("VICR / LITE / TER","–","OI and spread, as in V4")]],[0.95,0.85,2.0],font=7.2)]],
   colWidths=[3.3*inch,3.9*inch], style=TableStyle([("VALIGN",(0,0),(-1,-1),"TOP"),("LEFTPADDING",(0,0),(-1,-1),0),("RIGHTPADDING",(0,0),(-1,-1),0)]))]))

S.append(h2("Premium at Risk Through the Calendar"))
rows=[["Date","Event","Lines held","Premium at risk","% of book","Book theta / day"]]
for s in P["schedule"]:
    rows.append([s["date"][5:].replace("-","/"),cell(s["label"]),str(s["n"]),f"${s['premium']:,.0f}",f"{s['pct']:.0%}",f"{s['theta']:+,.0f}"])
S.append(tbl(rows,[0.6,2.3,0.8,1.1,0.8,1.1]))
S.append(Paragraph(f"The book carries ${sched['Oct 14 CPI']['premium']:,.0f} through the CPI and the first defense prints, ${sched['Oct 28 FOMC']['premium']:,.0f} through the FOMC and the midterms with the put on, and reaches its full ${dep:,.0f} only for the last three weeks. "
 f"Daily decay runs ${-sched['Oct 5 entry T1']['theta']:.0f} in week one against ${-FL['schedule'][0]['theta']:.0f} for the front-loaded alternative.", BODY))
S.append(h1("Scenario Ladder","3")); S.append(sub("(each leg marked at its own exit: Nov 16 at 4 DTE for Tranche 1, Nov 25 at 23 DTE for Tranches 2&#8211;3; moves are multiples of each leg's own standard deviation over its own hold, at entry IV; Shock is &#8722;2 s.d. with IV +10 points)"))
rows=[["Leg (ctr)","Hold","1 s.d.","Flat","Base (+1 s.d.)","Bull (+2 s.d.)","Gamma (+3 s.d.)","Shock (-2 s.d., IV +10)"]]
for l in legs:
    n=l["n"]
    rows.append([f"{legname(l)} (x{n})",f"{l['hold']}d",f"{l['sig']:.1%}",f"{l['pnl']['Flat']*n:+,.0f}",f"{l['pnl']['Base']*n:+,.0f} ({l['pnl']['Base']/l['cost']:+.0%})",
                 f"{l['pnl']['Bull']*n:+,.0f} ({l['pnl']['Bull']/l['cost']:+.0%})",f"{l['pnl']['Gamma']*n:+,.0f} ({l['pnl']['Gamma']/l['cost']:+.0%})",f"{l['pnl']['Shock']*n:+,.0f}"])
rows.append(["Book","","",f"{P['scen']['Flat']['pnl']:+,.0f}",f"{P['scen']['Base']['pnl']:+,.0f}",f"{P['scen']['Bull']['pnl']:+,.0f}",f"{P['scen']['Gamma']['pnl']:+,.0f}",f"{P['scen']['Shock']['pnl']:+,.0f}"])
S.append(tbl(rows,[1.1,0.4,0.45,0.6,1.0,1.05,1.15,1.1],bold_last=True,font=7.4))
S.append(Spacer(1,6))
rows=[["Scenario","V6 P&L","V6 Ending Value","V6 Return","MU variant","Front-loaded*","V5 (ref.)**"]]
for c,lab in [("Flat","Flat (0%, entry IV)"),("Base","Base (+1 s.d. per leg)"),("Bull","Bull (+2 s.d. per leg)"),("Gamma","Gamma Upside (+3 s.d. per leg)"),("Shock","Shock (-2 s.d., IV +10 pts)")]:
    rows.append([lab,f"{P['scen'][c]['pnl']:+,.0f}",f"${P['scen'][c]['end']:,.0f}",f"{ret(P,c):+.1%}",f"{ret(MV,c):+.1%}",f"{ret(FL,c):+.1%}",(f"{S5[c]['ret']:+.1%}" if c in S5 else "n/a")])
for c,lab in [("Base","Standing ladder: Base +18% uniform"),("Bull","Standing: Bull +18% + 1 s.d."),("Gamma","Standing: Gamma +18% + 2 s.d.")]:
    rows.append([cell(lab),f"{P['stand'][c]['pnl']:+,.0f}",f"${5000+P['stand'][c]['pnl']:,.0f}",f"{P['stand'][c]['ret']:+.1%}",f"{MV['stand'][c]['ret']:+.1%}",f"{FL['stand'][c]['ret']:+.1%}",f"{S5[c]['ret']:+.1%}"])
S.append(tbl(rows,[2.0,0.8,1.0,0.8,0.85,0.9,0.8]))
S.append(Paragraph(f"* The same twelve contracts bought on October 5 (Dec legs at 74 days to expiry) would cost ${FL['deployed']:,.0f}; returns are shown on a $5,000 base for comparison and the Flat Case therefore exceeds &#8722;100%. "
 "The MU variant replaces VRT, SKHY, DRAM and BA with one MU Dec 1350C bought November 5 ($1,872 indicative, 37% of the book, 0.17 delta). "
 f"The standing-ladder rows apply the V3&#8211;V5 uniform +18% to every leg; on that ladder the SPY put expires worthless and the low-vol legs (GLD, RTX, BA) print 2&#8211;3 standard-deviation moves, which is why the figures are far above the normalized rows. ** V5 returns are on the standing ladder in every row; V5 has no Shock Case.", NOTE))
S += note(PAST_PERF)
S.append(h2("Flat Case: Volatility Re-rate Needed for +5% / +10%"))
rows=[["Exit mark","Lines held","Flat return (entry IV)","IV rise for +5%","IV rise for +10%"]]
for k,r in P["rerate"].items():
    rows.append([k,str(r["held"]),f"{r['flat_ret']:+.1%}",f"+{r['dvol_5']*100:.0f} pts" if r["dvol_5"] else "not reachable",f"+{r['dvol_10']*100:.0f} pts" if r["dvol_10"] else "not reachable"])
S.append(tbl(rows,[1.2,1.0,1.6,1.4,1.4]))
S.append(Paragraph("A flat tape is the losing case for any long-premium book and V6 does not change that; the staging changes how much is exposed to it and for how long. The re-rate figures are larger than V5's (+17&#8211;25 points there) because V6 holds more lines at lower implied volatility, where a point of vol is worth less in dollars.", BODY))

S.append(h1("Backtest: Forward Returns Over Each Leg's Hold","4")); S.append(sub("(overlapping windows from two years of weekly closes; the window length is each leg's hold rounded to weeks; thresholds are the leg's own +1 / +2 / +3 s.d.)"))
rows=[["Leg","Weeks","n","1y realized","Entry IV","Mean","Median","Max","Min","Hit +1 s.d.","Hit +2 s.d.","Hit +3 s.d.","Hit -2 s.d."]]
for l in legs:
    b=l["bt"]
    if not b: rows.append([legname(l),"–","–",f"{l['hv']:.0%}",f"{l['iv']:.0%}","n/a","","","","","","",""]); continue
    rows.append([legname(l),str(b["w"]),str(b["n"]),f"{l['hv']:.0%}",f"{l['iv']:.0%}",f"{b['mean']:+.1%}",f"{b['med']:+.1%}",f"{b['mx']:+.0%}",f"{b['mn']:+.0%}",f"{b['h1']:.0%}",f"{b['h2']:.0%}",f"{b['h3']:.0%}",f"{b['hneg']:.0%}"])
S.append(tbl(rows,[0.85,0.45,0.35,0.7,0.6,0.55,0.6,0.5,0.5,0.65,0.65,0.65,0.7],font=7.4))
S.append(Paragraph("SKHY has ten windows (listed July 2026) and DRAM twenty-four; their rows are indicative. SPY has no weekly history in the model file; its put is sized on the Shock Case, not on a hit rate.", NOTE))
S.append(h2("Rules of Engagement"))
S += bullets([
 "<b>Entry gates.</b> Tranche 2 proceeds on Oct 22 unless the Oct 14 CPI lifts December hike odds above ~90% or SPY front-month IV exceeds 25%; either delays it one week. Tranche 3 proceeds on Nov 5 unless the book is below &#8722;25% on Nov 4, in which case it is halved and the cash is kept.",
 "<b>Cuts.</b> Any leg at &#8722;50% of its premium after half its hold is closed; the proceeds are not redeployed in that name. Any leg that reaches 4 days to expiry is closed regardless of mark.",
 "<b>Profit-taking.</b> One third of a line is sold at +100% and another third at +200%; the remainder runs to the exit date. Sold thirds fund the roll-up rule.",
 "<b>Roll-ups.</b> On Nov 16, Tranche 1 winners are rolled into the December strike nearest 25 delta, sized to the proceeds of the sold thirds plus the 8% cash reserve; losers are not rolled.",
 "<b>Hedge.</b> The SPY put is held to Nov 25 unless it doubles, in which case half is sold and the rest is held as a free hedge. It is never sold to fund a call.",
 "<b>Exits.</b> Nov 16 for Tranche 1 and Nov 25 for Tranches 2&#8211;3, before the Nov 18 NVDA print, before Thanksgiving, and three weeks before the December MU print.",
])

S.append(h1("Key Findings"))
S += bullets([
 f"<b>The staging removes a week-one blow-up as a possibility.</b> Through October 21 the book has ${sched['Oct 14 CPI']['premium']:,.0f} at risk ({sched['Oct 14 CPI']['pct']:.0%}), in three legs with no dated event inside their holds; the worst possible outcome of the first seventeen days is &#8722;{sched['Oct 14 CPI']['pct']:.0%}.",
 f"<b>Convexity is preserved.</b> The Gamma Upside Case returns {ret(P,'Gamma'):+.0%} on the normalized ladder and {P['stand']['Gamma']['ret']:+.0%} on the standing V3&#8211;V5 ladder, against {S5['Gamma']['ret']:+.0%} for V5 on the standing ladder, because the premium is spread over twelve contracts at 22&#8211;31 delta instead of seven.",
 f"<b>The hedge converts the Shock Case from {sum(l['pnl']['Shock']*l['n'] for l in legs if l['cp']=='C')/5000:+.0%} to {ret(P,'Shock'):+.0%}.</b> At &#8722;2 standard deviations across every leg with IV +10 points the calls lose ${-sum(l['pnl']['Shock']*l['n'] for l in legs if l['cp']=='C'):,.0f} and the SPY put makes {[l for l in legs if l['tk']=='SPY'][0]['pnl']['Shock']:+,.0f}.",
 "<b>MU is accessed, not owned.</b> The DRAM basket (MU its largest holding) and SKHY give the memory sleeve 36% of the book across four contracts with hit rates on +1 s.d. of 42% and 30%; the single-contract MU variant scores lower on every case except Shock because one 0.17-delta contract absorbs 37% of the premium.",
 "<b>The defense sleeve is bought into a drawdown after its own catalysts clear.</b> RTX and BA are 7% and 15% below their 13-week-ago levels, report on Oct 20 and Oct 27, and are bought on Oct 22 and Nov 5 with implied volatility at 0.91&#215; and 1.10&#215; realized.",
 "<b>Where the ladder is least supported.</b> RTX's +2 s.d. threshold has never printed in 100 five-week windows and GLD's +3 s.d. never in 99 six-week windows; those two cells of the Gamma Upside column are the model's assumption, not history. MU, DRAM and VRT carry the historically supported tail.",
])
S.append(h1("Assessment"))
S.append(Paragraph(
 f"RWS V6 is the process of Versions 3 through 5 with the timing, breadth and hedging that a six-week window across a CPI, an FOMC, a midterm election and a live war requires. It deploys {sched['Oct 5 entry T1']['pct']:.0%} in the quiet first week, {sched['Oct 22 entry T2']['pct']:.0%} by the FOMC and {sched['Nov 5 entry T3']['pct']:.0%} after the election, buys every event-exposed name after its own print, and holds an index put through the two macro dates. "
 f"On the vol-normalized ladder it returns {ret(P,'Flat'):+.0%} / {ret(P,'Base'):+.0%} / {ret(P,'Bull'):+.0%} / {ret(P,'Gamma'):+.0%} / {ret(P,'Shock'):+.0%} across Flat, Base, Bull, Gamma Upside and Shock; on the standing +18% ladder used in Versions 3 through 5 it returns "
 f"{P['stand']['Base']['ret']:+.0%} / {P['stand']['Bull']['ret']:+.0%} / {P['stand']['Gamma']['ret']:+.0%}. The MU-anchored variant is the same book with one large contract in place of four small ones and is lower on every upside case. "
 "The redesign does not change the one fact that governs every version: a flat tape through November 25 loses most of the premium, and the only defense against that is the staging, the cut rule and the cash it keeps.", BODY))

from addendum_jan2026 import addendum
S += addendum("5")
S.append(h1("Endnotes"))
S += [Paragraph(t, EN) for t in [
 "(1) Tranche 1: entry October 5&#8211;9, exit Monday November 16, 2026, contracts expiring November 20, 2026 (42-day hold). Tranche 2: entry October 22&#8211;23, Tranche 3: entry November 5&#8211;6, both exiting Wednesday November 25, 2026 in contracts expiring December 18, 2026 (34- and 20-day holds). Event dates are from the Bigdata.com corporate calendar (earnings) and public Federal Reserve and BLS schedules; CPI and PCE dates are approximate.",
 "(2) Quotes: Interactive Brokers, October 2, 2026 after the close. Nov 20 '26 mids for the V3&#8211;V5 names as in candidates.py; Dec 18 '26 and GLD Nov 20 '26 bid/ask and open interest pulled this session for MU, NVDA, RTX, LMT, BA, AMD, GDX, SKHY, DRAM, NOC, LHX, VRT, CEG, GEV, GLD and SPY (puts). Implied volatility is backed out of each mid by Black-Scholes (r = 4%, q = 0) at the Oct 2 days to expiry. Tranche 2 and 3 entry prices re-price that volatility at the tranche entry date with spot unchanged. Screens: delta 0.18&#8211;0.40 at entry (puts 0.08&#8211;0.22), open interest &#8805; 500, spread &#8804; 25% of mid, ticket &#8804; 25% of the book, call IV &#8804; 1.25&#215; one-year realized.",
 "(3) Vol-normalized ladder: for each leg, s.d. = entry IV &#215; &#8730;(hold / 365); Base, Bull and Gamma Upside move the underlying +1, +2 and +3 s.d. at entry IV; Shock moves it &#8722;2 s.d. and raises IV 10 points; each leg is marked at its own exit date. The standing ladder is the V3&#8211;V5 definition (Flat 0%; Base +18%; Bull +18% + 1 s.d.; Gamma Upside +18% + 2 s.d.). Gamma/$100 = &#915; &#215; S&#178; / 100 per $100 of premium. Book theta is the sum of per-contract Black-Scholes theta on the stated date.",
 "(4) Backtest: Interactive Brokers weekly closes, two-year lookback through the September 28, 2026 bar; overlapping forward returns over each leg's hold rounded to weeks (6, 5 or 3); n = 99&#8211;102 for names with full history, 24 for DRAM and 10 for SKHY. One-year realized volatility is the annualized standard deviation of the last 52 weekly log returns. Thirteen-week momentum is the close-to-close change over the last 13 weekly bars. Macro and company commentary is from Bigdata.com news and transcript search on October 2, 2026 (Micron Q4 FY26 call of September 30; Morgan Stanley Thoughts on the Market, September 30; Vertiv at the Goldman Sachs conference, September; Federal Reserve commentary and CME FedWatch pricing as reported).",
 "(5) Statement figures are as printed on the January 1&#8211;30, 2026 J.P. Morgan Securities statement. Blotter statistics are parsed from its trade-activity section and capture 134 closing transactions totaling $22,224 against the statement's $22,602 net realized.",
 "Model code: memos/model_v6.py (pricing, ladder, schedule, screen) and memos/quotes_v6.py (quote universe); backtest input in memos/weekly_closes.json.",
]]
S += disclosure("memo", "Mythos", "Donald B. Ritts III",
 extra=["<b>Statement Example.</b> The January 2026 statement presented in the addendum is a single selected period and may not be representative of all periods or of the Sleeve's own outcome. It should not be "
        "assumed that the Sleeve will make equally successful or comparable trades. The positions in that statement were entered under different market conditions and with a different structure (30&#8211;45 "
        "concurrent lines, one- to two-week tenors) from the Sleeve presented herein.",
        "<b>Indicative Entries.</b> Tranche 2 and 3 entry prices are model values at a future date under the assumption of unchanged spot and implied volatility and are not quotes. The entry gates, cut and profit-taking rules herein are mechanical rules of the model and their execution depends on market conditions at the time.",
        "<b>Third-Party Content.</b> Macro, geopolitical and company commentary summarized herein is drawn from third-party news and transcript sources retrieved through Bigdata.com and is reproduced for context only; Mythos has not independently verified it."])
doc.build(S); print("ok v6")
