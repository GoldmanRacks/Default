import json
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph as _P, Spacer, Table, TableStyle
from math import sqrt, log, exp
from statistics import NormalDist

M = json.load(open("model_out_v3b.json")); V3 = json.load(open("model_out.json"))
pick, legs, scen, bt, screen = M["pick"], M["legs"], M["scen"], M["bt"], M["screen"]
spot = {"BA":192.35,"MU":1091.89,"NVDA":231.59,"RTX":186.12,"LMT":506.50,"MRVL":269.30,"SKHY":191.40,"GDX":86.13}
N = NormalDist().cdf; R=0.04
def bs(S,K,T,iv):
    if T<=0: return max(S-K,0)
    d1=(log(S/K)+(R+.5*iv*iv)*T)/(iv*sqrt(T)); return S*N(d1)-K*exp(-R*T)*N(d1-iv*sqrt(T))
def Paragraph(t, st, **kw): return _P(t.replace("P&L","P&amp;L"), st, **kw)

ss = getSampleStyleSheet()
H1 = ParagraphStyle('h1', parent=ss['Heading1'], fontSize=15, spaceAfter=4)
H2 = ParagraphStyle('h2', parent=ss['Heading2'], fontSize=11.5, spaceBefore=10, spaceAfter=4)
B  = ParagraphStyle('b', parent=ss['BodyText'], fontSize=8.6, leading=11.2)
SM = ParagraphStyle('sm', parent=B, fontSize=7.4, leading=9.4, textColor=colors.HexColor('#444444'))
BL = ParagraphStyle('bl', parent=B, leftIndent=12, bulletIndent=2)
def tbl(data, widths, bold_last=False):
    t = Table(data, colWidths=widths, repeatRows=1)
    st = [('FONT',(0,0),(-1,-1),'Helvetica',7.8),('GRID',(0,0),(-1,-1),0.3,colors.HexColor('#BBBBBB')),('VALIGN',(0,0),(-1,-1),'MIDDLE'),
          ('ALIGN',(1,1),(-1,-1),'RIGHT'),('TOPPADDING',(0,0),(-1,-1),2.5),('BOTTOMPADDING',(0,0),(-1,-1),2.5),
          ('FONT',(0,0),(-1,0),'Helvetica-Bold',7.8),('BACKGROUND',(0,0),(-1,0),colors.HexColor('#5B2C6F')),('TEXTCOLOR',(0,0),(-1,0),colors.white)]
    for i in range(2,len(data),2): st.append(('BACKGROUND',(0,i),(-1,i),colors.HexColor('#F6F2F8')))
    if bold_last: st.append(('FONT',(0,-1),(-1,-1),'Helvetica-Bold',7.8))
    t.setStyle(TableStyle(st)); return t

doc = SimpleDocTemplate("Ritts_6_week_Wedding_Model_V3b_MU_SKHY_BA.pdf", pagesize=letter, leftMargin=0.6*inch, rightMargin=0.6*inch, topMargin=0.55*inch, bottomMargin=0.55*inch,
                        title="Ritts Wedding Memo V3b - MU 1350C, SKHY restored, BA for LMT", author="Mythos")
S=[]
S.append(Paragraph("Ritts Wedding Memo / Mythos &mdash; V3b variant (MU 1350C, SKHY restored, BA in for LMT)", H1))
S.append(Paragraph("Prepared for: Donald B. Ritts III &nbsp;|&nbsp; Date: October 2, 2026 &nbsp;|&nbsp; Book size: $5,000 &nbsp;|&nbsp; Entry: Mon Oct 5 '26 &nbsp;|&nbsp; "
                   "Exit: Mon Nov 16 '26 (42-day hold) &nbsp;|&nbsp; Contract expiry: Nov 20 '26 (46 DTE at entry, 4 DTE at exit) &nbsp;|&nbsp; Companion to V3 (same date)", SM))
S.append(Spacer(1,6))
dep=M["deployed"]; cash=M["cash"]; p=pick["MU"]; TH=42/365; sig=p["iv"]*sqrt(TH)
S.append(Paragraph("1. Executive Summary", H2))
S.append(Paragraph(
 f"This variant models the alternative flagged in V3's concentration note and adds the user's BA-for-LMT swap. Three changes versus V3: (i) the MU anchor moves one strike out to "
 f"<b>MU Nov 20 '26 1350C</b> (${p['cost']:,.0f}, delta 0.182), which breaks the 0.20 delta floor but frees $710; (ii) <b>SKHY 230C is restored</b> (${pick['SKHY']['cost']:,.0f}); "
 f"(iii) <b>BA takes the LMT slot</b> as the second aerospace/defense leg alongside RTX (BA Nov 20 '26 220C, ${pick['BA']['cost']:,.0f}). To fit all seven legs in $5,000 the delta floor "
 f"is relaxed to 0.18 for MU and BA only; NVDA, RTX, MRVL, SKHY and GDX hold their V3 strikes at the 0.20 floor. GDX drops from 2 contracts to 1. Deployed ${dep:,.0f}; cash ${cash:,.0f}. "
 f"Ladder (Base +18% uniform; Bull +18%+1&sigma;; Gamma +18%+2&sigma;, 42-day &sigma; per name): <b>{scen['Base']['ret']:+.0%} / {scen['Bull']['ret']:+.0%} / {scen['Gamma']['ret']:+.0%}</b> "
 f"(${scen['Base']['end']:,.0f} / ${scen['Bull']['end']:,.0f} / ${scen['Gamma']['end']:,.0f}) versus V3's {V3['scen']['Base']['ret']:+.0%} / {V3['scen']['Bull']['ret']:+.0%} / {V3['scen']['Gamma']['ret']:+.0%}. "
 f"The variant gives up {(V3['scen']['Base']['ret']-scen['Base']['ret'])*100:.0f} points of Base return (the 1350C is deeper out of the money at a +18% print) and picks up "
 f"{(scen['Gamma']['ret']-V3['scen']['Gamma']['ret'])*100:.0f} points of Gamma Upside, while cutting MU's share of Bull P&L from {V3['scen']['Bull']['rows']['MU']['pnl']/V3['scen']['Bull']['pnl']:.0%} to "
 f"{scen['Bull']['rows']['MU']['pnl']/scen['Bull']['pnl']:.0%}.", B))

S.append(Paragraph("2. Book Construction (Nov 20 '26 calls, entry Oct 5 '26)", H2))
rows=[["Leg","Ctr","Spot","Entry $/ctr","Delta","Gamma","Gamma/$ prem","Mid-IV","Call OI","Deployed $","vs V3"]]
v3legs = {t:n for t,n in V3["legs"]}
for tk,n in legs:
    q=pick[tk]; d = ("new" if tk in ("BA","SKHY") else ("1300C→1350C" if tk=="MU" else ("x2→x1" if tk=="GDX" else "same")))
    rows.append([f"{tk} {q['K']}C", str(n), f"{spot[tk]:,.2f}", f"${q['cost']:,.0f}", f"{q['delta']:.3f}", f"{q['gamma']:.5f}", f"{q['gpp']:.3f}", f"{q['iv']:.1%}", f"{q['oi']:,}", f"${q['cost']*n:,.0f}", d])
rows.append(["Cash / dry powder","—","—","—","—","—","—","—","—",f"${cash:,.0f}","$12"])
rows.append(["Total","","","","","","","","","$5,000",""])
S.append(tbl(rows,[0.9*inch,0.33*inch,0.55*inch,0.7*inch,0.48*inch,0.6*inch,0.95*inch,0.5*inch,0.55*inch,0.7*inch,0.95*inch], bold_last=True)); S.append(Spacer(1,5))
S.append(Paragraph("<b>BA strike screen (Nov 20 '26).</b> BA trades at 38.0% mid-IV against 29.4% 30-day realized (IV sits 9 points rich, the widest premium to realized in the book). "
 "The 220C is the max gamma-per-premium strike at the relaxed 0.18 floor and carries the deepest open interest in the BA chain (7,602). The 215C clears the 0.20 floor but at $378 would push "
 "the book $74 over $5,000 unless the GDX leg were released.", B))
rows=[["Strike","Mid $","IV","Delta","Gamma","Gamma/$ prem","Cost/ctr","Call OI","Verdict"]]
for r in screen["BA"]:
    v = "SELECTED (0.18 floor)" if r["K"]==pick["BA"]["K"] else ("fails 0.18 floor" if r["delta"]<0.18 else ("clears 0.20 floor; does not fit" if r["K"]==215 else "clears floor, lower gamma/$"))
    rows.append([f"{r['K']}C", f"{r['mid']:.2f}", f"{r['iv']:.1%}", f"{r['delta']:.3f}", f"{r['gamma']:.5f}", f"{r['gpp']:.4f}", f"${r['cost']:,.0f}", f"{r['oi']:,}", v])
S.append(tbl(rows,[0.6*inch,0.55*inch,0.5*inch,0.5*inch,0.6*inch,0.95*inch,0.65*inch,0.6*inch,1.7*inch])); S.append(Spacer(1,5))
S.append(Paragraph(f"<b>Why BA over LMT in this slot.</b> At the Nov 20 '26 expiry LMT's best strike screens at 0.086 gamma/$ with 35&ndash;137 OI; BA 220C screens at {pick['BA']['gpp']:.3f} gamma/$ "
 f"(4.3&times;) with 7,602 OI, for $280 against LMT's $655&ndash;$930. BA's 2-year realized vol ({bt['BA']['rv']:.1%}) is 9 points above LMT's ({bt['LMT']['rv']:.1%}) and its max 6-week move "
 f"(+{bt['BA']['mx']:.1%}) is 17 points higher, so the same +18% Base threshold has been hit {bt['BA']['hb']:.0%} of the time versus LMT's {bt['LMT']['hb']:.0%}.", B))

S.append(Paragraph("3. Scenario Ladder &amp; Portfolio Payout (marked Nov 16 '26, 4 DTE, Black-Scholes at entry IV)", H2))
rows=[["Leg","Flat (0%)","Base +18%","Bull (+18%+1σ)","Gamma Upside (+18%+2σ)"]]
for tk,n in legs:
    q=pick[tk]
    def cell(s): r=scen[s]['rows'][tk]; return f"{r['pnl']:+,.0f} ({r['ret']:+.0%})"
    def mv(s): return f"{scen[s]['rows'][tk]['move']:+.1%}"
    rows.append([f"{tk} {q['K']}C (x{n})", cell('Flat'), cell('Base'), f"{cell('Bull')}  @{mv('Bull')}", f"{cell('Gamma')}  @{mv('Gamma')}"])
S.append(tbl(rows,[1.15*inch,1.2*inch,1.3*inch,1.7*inch,1.9*inch])); S.append(Spacer(1,5))
rows=[["Scenario","V3b P&L","V3b Ending Value","V3b Return","V3 Return (ref.)","Diff vs V3"]]
for s,lab in [("Flat","Flat (0%)"),("Base","Base (+18%)"),("Bull","Bull (+18%+1σ)"),("Gamma","Gamma Upside (+18%+2σ)")]:
    v=scen[s]; w=V3['scen'][s]; rows.append([lab, f"{v['pnl']:+,.0f}", f"${v['end']:,.0f}", f"{v['ret']:+.1%}", f"{w['ret']:+.1%}", f"{(v['ret']-w['ret'])*100:+.1f} pts"])
S.append(tbl(rows,[1.7*inch,1.0*inch,1.2*inch,1.0*inch,1.1*inch,0.9*inch])); S.append(Spacer(1,5))

lo,hi=1100.0,1600.0
for _ in range(80):
    m_=(lo+hi)/2
    if bs(m_,1350,4/365,p['iv'])*100 < p['cost']: lo=m_
    else: hi=m_
BE=(lo+hi)/2
S.append(Paragraph(f"<b>MU anchor-leg sensitivity (Nov 16 mark, 1350C).</b> MU is {p['cost']/5000:.0%} of the book (V3: 61%). 42-day 1&sigma; at {p['iv']:.1%} IV = {sig:.1%} (${spot['MU']*sig:,.0f}). "
 f"Breakeven at the 4-DTE mark is MU &asymp; ${BE:,.0f} ({BE/spot['MU']-1:+.1%}; vs. ${1350+p['mid']:,.0f} / {(1350+p['mid'])/spot['MU']-1:+.1%} at expiry). "
 f"Other six legs held at the Base (+18%) column for the book-level row.", B))
rows=[["MU on Nov 16","Move","Call value","MU leg P&L","MU leg return","Book P&L (others @ Base)","Book return","V3 book return"]]
others = scen['Base']['pnl']-scen['Base']['rows']['MU']['pnl']; others3 = V3['scen']['Base']['pnl']-V3['scen']['Base']['rows']['MU']['pnl']
for mvp in [0.0,0.10,0.18,0.25,0.30,sig+0.18,0.45,0.50,2*sig+0.18,0.75,1.00]:
    S1=spot['MU']*(1+mvp); v=bs(S1,1350,4/365,p['iv'])*100; pnl=v-p['cost']
    v3=bs(S1,1300,4/365,V3['pick']['MU']['iv'])*100-V3['pick']['MU']['cost']
    rows.append([f"${S1:,.0f}", f"{mvp:+.1%}", f"${v:,.0f}", f"{pnl:+,.0f}", f"{pnl/p['cost']:+.0%}", f"{pnl+others:+,.0f}", f"{(pnl+others)/5000:+.0%}", f"{(v3+others3)/5000:+.0%}"])
S.append(tbl(rows,[0.85*inch,0.6*inch,0.75*inch,0.85*inch,0.85*inch,1.4*inch,0.85*inch,0.9*inch]))

S.append(Paragraph("4. Backtest: Historical Frequency of Modeled 6-Week Moves", H2))
S.append(Paragraph("Overlapping 6-week (42-day) forward returns from 2 years of weekly closes (n=99 windows per name, IBKR data through the 9/28/26 bar). Thresholds use each leg's V3b entry IV. "
 "SKHY (13 weekly bars since listing) is excluded; LMT shown for reference as the leg BA replaces.", B))
rows=[["Ticker","Real. Vol","Entry IV","Mean 6wk","Max 6wk","Base thr.","Hit Base","Bull thr.","Hit Bull","Gamma thr.","Hit Gamma"]]
for tk in ["MU","NVDA","RTX","BA","MRVL","GDX","LMT"]:
    v=bt[tk]; rows.append([tk+("*" if tk=="LMT" else ""), f"{v['rv']:.1%}", f"{v['iv']:.1%}", f"{v['mean']:+.1%}", f"{v['mx']:+.1%}", f"{v['base']:.0%}", f"{v['hb']:.0%}", f"{v['bull']:.1%}", f"{v['hu']:.0%}", f"{v['gam']:.1%}", f"{v['hg']:.0%}"])
S.append(tbl(rows,[0.5*inch,0.65*inch,0.6*inch,0.65*inch,0.65*inch,0.6*inch,0.6*inch,0.6*inch,0.6*inch,0.7*inch,0.7*inch]))
S.append(Paragraph("* LMT not in the book; shown as the leg BA replaces.", SM)); S.append(Spacer(1,4))
S.append(Paragraph("Key findings:", B))
for s in [
 f"<b>BA</b> clears the +18% Base case in {bt['BA']['hb']:.0%} of windows (LMT: {bt['LMT']['hb']:.0%}; RTX: {bt['RTX']['hb']:.0%}), making it the strongest of the three aerospace/defense candidates on historical frequency; "
 f"its Bull (+{bt['BA']['bull']:.1%}) and Gamma (+{bt['BA']['gam']:.1%}) thresholds each printed once in 99 windows (max +{bt['BA']['mx']:.1%}). Entry IV ({bt['BA']['iv']:.1%}) is in line with 2-year realized ({bt['BA']['rv']:.1%}).",
 f"<b>MU 1350C</b> shifts the leg's thresholds by only 0.3 points versus the 1300C (Bull +{bt['MU']['bull']:.1%}, Gamma +{bt['MU']['gam']:.1%}), so hit rates are unchanged at {bt['MU']['hb']:.0%} / {bt['MU']['hu']:.0%} / {bt['MU']['hg']:.0%}; "
 f"what changes is the payoff shape: at a +18% print the 1350C loses {scen['Base']['rows']['MU']['ret']:.0%} versus {V3['scen']['Base']['rows']['MU']['ret']:.0%} for the 1300C, while at +57% it returns {scen['Gamma']['rows']['MU']['ret']:+.0%} versus {V3['scen']['Gamma']['rows']['MU']['ret']:+.0%}.",
 "Two memory legs (MU + SKHY) now sit side by side: 59% of premium is memory/HBM beta. SKHY's Oct 5&ndash;Nov 16 window contains SK Hynix's Q3 report (late Oct), a dated catalyst MU itself does not have in-window.",
 "In-window dated catalysts (approx.): BA Q3 print ~Oct 21&ndash;22 and RTX Q3 ~Oct 20&ndash;21 (both aerospace/defense legs trade through earnings); FOMC Oct 27&ndash;28; SK Hynix Q3 late Oct; NVDA Q3 (~Nov 18&ndash;19) and MU fiscal Q1 (Dec) fall after the Nov 16 exit.",
]:
    S.append(Paragraph(s, BL, bulletText='•'))

S.append(Paragraph("5. Assessment", H2))
S.append(Paragraph(
 f"V3b is the broader book: seven legs, five sectors of convexity (memory &times;2, GPU, AI networking, aerospace/defense &times;2, gold miners), MU at {p['cost']/5000:.0%} of premium rather than 61%, "
 f"and MU contributing {scen['Bull']['rows']['MU']['pnl']/scen['Bull']['pnl']:.0%} / {scen['Gamma']['rows']['MU']['pnl']/scen['Gamma']['pnl']:.0%} of Bull / Gamma P&L (V3: 54% / 58%). The price of the breadth is in the Base column: "
 f"{scen['Base']['ret']:+.0%} versus {V3['scen']['Base']['ret']:+.0%}, because the 1350C needs MU above ${BE:,.0f} on Nov 16 to be worth its premium versus $1,299 for the 1300C. On the MU-only axis (other legs held at Base) V3 leads at every MU print "
 f"by a near-constant ~80 points, because the 1300C carries $5,000 more intrinsic per contract than the 1350C at any MU level above both strikes while costing $710 more. V3b overtakes V3 "
 f"only when the satellite legs also run (Bull +{(scen['Bull']['ret']-V3['scen']['Bull']['ret'])*100:.0f} pts, Gamma +{(scen['Gamma']['ret']-V3['scen']['Gamma']['ret'])*100:.0f} pts): it is the better book in a broad "
 f"semis/defense/gold move and the worse one in a MU-only move. Two legs (MU, BA) sit below the 0.20 delta floor at 0.182 and 0.187; the other five hold it.", B))
S.append(Spacer(1,6))
S.append(Paragraph("Methodology: Black-Scholes (r=4%, q=0%) at entry (46 DTE) for delta/gamma; entry $/ctr = IBKR SMART mid quote at 2026-10-02 close ×100; scenarios marked Nov 16 '26 by Black-Scholes at 4 DTE "
 "using each leg's entry IV (no vol change assumed). Scenario σ = IV × √(42/365). Backtest: IBKR weekly closes, 2-year lookback, overlapping 6-week forward returns, n=99 per name. "
 "Model code: memos/ritts_6wk_model_v3.py (run with argument v3b). Not investment advice.", SM))
doc.build(S); print("ok")
