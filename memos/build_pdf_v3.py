import json
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from math import sqrt, log, exp
from statistics import NormalDist

M = json.load(open("model_out.json"))
pick, legs, scen, bt, screen = M["pick"], M["legs"], M["scen"], M["bt"], M["screen"]
spot = {"MU":1091.89,"NVDA":231.59,"RTX":186.12,"LMT":506.50,"MRVL":269.30,"SKHY":191.40,"GDX":86.13}
N = NormalDist().cdf; R=0.04
def bs(S,K,T,iv):
    if T<=0: return max(S-K,0)
    d1=(log(S/K)+(R+.5*iv*iv)*T)/(iv*sqrt(T)); return S*N(d1)-K*exp(-R*T)*N(d1-iv*sqrt(T))

ss = getSampleStyleSheet()
H1 = ParagraphStyle('h1', parent=ss['Heading1'], fontSize=15, spaceAfter=4)
H2 = ParagraphStyle('h2', parent=ss['Heading2'], fontSize=11.5, spaceBefore=10, spaceAfter=4)
B  = ParagraphStyle('b', parent=ss['BodyText'], fontSize=8.6, leading=11.2)
SM = ParagraphStyle('sm', parent=B, fontSize=7.4, leading=9.4, textColor=colors.HexColor('#444444'))
BL = ParagraphStyle('bl', parent=B, leftIndent=12, bulletIndent=2)

_P = Paragraph
def Paragraph(text, style, **kw):
    return _P(text.replace("P&L", "P&amp;L"), style, **kw)

def tbl(data, widths, hdr=True, zebra=True, align_right_from=1):
    t = Table(data, colWidths=widths, repeatRows=1 if hdr else 0)
    st = [('FONT',(0,0),(-1,-1),'Helvetica',7.8),('GRID',(0,0),(-1,-1),0.3,colors.HexColor('#BBBBBB')),
          ('VALIGN',(0,0),(-1,-1),'MIDDLE'),('ALIGN',(align_right_from,1),(-1,-1),'RIGHT'),
          ('TOPPADDING',(0,0),(-1,-1),2.5),('BOTTOMPADDING',(0,0),(-1,-1),2.5)]
    if hdr: st += [('FONT',(0,0),(-1,0),'Helvetica-Bold',7.8),('BACKGROUND',(0,0),(-1,0),colors.HexColor('#1F3A5F')),('TEXTCOLOR',(0,0),(-1,0),colors.white)]
    if zebra:
        for i in range(1,len(data)):
            if i%2==0: st.append(('BACKGROUND',(0,i),(-1,i),colors.HexColor('#F2F5F9')))
    t.setStyle(TableStyle(st)); return t

doc = SimpleDocTemplate("Ritts_6_week_Wedding_Model_V3_MU.pdf", pagesize=letter, leftMargin=0.6*inch, rightMargin=0.6*inch, topMargin=0.55*inch, bottomMargin=0.55*inch,
                        title="Ritts Wedding Memo V3 - MU calls, Oct 5 to Nov 16 2026", author="Mythos")
S = []
S.append(Paragraph("Ritts Wedding Memo / Mythos &mdash; V3 (MU add, 6-week horizon)", H1))
S.append(Paragraph("Prepared for: Donald B. Ritts III &nbsp;|&nbsp; Date: October 2, 2026 &nbsp;|&nbsp; Book size: $5,000 &nbsp;|&nbsp; "
                   "Entry: Mon Oct 5 '26 &nbsp;|&nbsp; Exit: Mon Nov 16 '26 (42-day hold) &nbsp;|&nbsp; Contract expiry: Nov 20 '26 (46 DTE at entry, 4 DTE at exit)", SM))
S.append(Spacer(1,6))

dep = M["deployed"]; cash = M["cash"]
S.append(Paragraph("1. Executive Summary", H2))
S.append(Paragraph(
 f"This V3 revision implements three changes to the V2 (Sep 23) sleeve: (i) <b>MU is added as the anchor leg</b> (MU Nov 20 '26 1300C, 1 contract, "
 f"${pick['MU']['cost']:,.0f}, {pick['MU']['cost']/5000:.0%} of the book); (ii) the <b>entry date moves to Oct 5 '26</b> with all legs re-priced off IBKR SMART mids and "
 f"mid-IVs pulled Oct 2; (iii) the <b>horizon is extended to Nov 16 '26</b> and the whole book rolls from the Oct 30 weekly to the <b>Nov 20 '26 monthly</b>, the first "
 f"regular expiry that covers the Nov 16 exit. The hold is 42 days (6 weeks) versus 37 in V2; the 4 remaining days of time value at exit are marked by Black-Scholes rather than intrinsic. "
 f"The selection rule is unchanged: delta &ge; 0.20 floor, maximum gamma per dollar of premium. Funding the MU contract required dropping LMT (lowest gamma-per-premium of all "
 f"candidates, 0.07&ndash;0.09) and SKHY (redundant memory proxy once MU is held outright). Deployed: ${dep:,.0f}; cash: ${cash:,.0f}. "
 f"Scenario ladder (Base +18% uniform; Bull +18%+1&sigma;; Gamma Upside +18%+2&sigma;, 42-day &sigma; per name): "
 f"<b>{scen['Base']['ret']:+.0%} / {scen['Bull']['ret']:+.0%} / {scen['Gamma']['ret']:+.0%}</b> on $5,000 "
 f"(${scen['Base']['end']:,.0f} / ${scen['Bull']['end']:,.0f} / ${scen['Gamma']['end']:,.0f}). "
 f"A 2-year, 99-window backtest of 6-week forward returns puts MU's Base/Bull/Gamma hit rates at {bt['MU']['hb']:.0%} / {bt['MU']['hu']:.0%} / {bt['MU']['hg']:.0%}, "
 f"the highest in the book and the reason it carries the anchor weight.", B))

S.append(Paragraph("2. Book Construction (Nov 20 '26 calls, entry Oct 5 '26)", H2))
rows = [["Leg","Ctr","Spot","Entry $/ctr","Delta","Gamma","Gamma/$ prem","Mid-IV","Call OI","Deployed $"]]
for tk,n in legs:
    p=pick[tk]
    rows.append([f"{tk} {p['K']}C", str(n), f"{spot[tk]:,.2f}", f"${p['cost']:,.0f}", f"{p['delta']:.3f}", f"{p['gamma']:.5f}", f"{p['gpp']:.3f}", f"{p['iv']:.1%}", f"{p['oi']:,}", f"${p['cost']*n:,.0f}"])
rows.append(["Cash / dry powder","—","—","—","—","—","—","—","—",f"${cash:,.0f}"])
rows.append(["Total","","","","","","","","","$5,000"])
t=tbl(rows,[1.1*inch,0.35*inch,0.6*inch,0.75*inch,0.5*inch,0.6*inch,0.95*inch,0.55*inch,0.6*inch,0.75*inch])
t.setStyle(TableStyle([('FONT',(0,-1),(-1,-1),'Helvetica-Bold',7.8)])); S.append(t); S.append(Spacer(1,5))

S.append(Paragraph("<b>MU strike screen (Nov 20 '26).</b> Four strikes were screened at 46 DTE. 1350C has the best gamma-per-premium but fails the 0.20 delta floor (0.182); "
 "1300C is the cheapest strike that clears it, at 42% less premium than the 1250C the V2 memo screened out. Open interest of 3,722 is the deepest among the four strikes after 1350C.", B))
rows=[["Strike","Mid $","IV","Delta","Gamma","Gamma/$ prem","Cost/ctr","Call OI","Verdict"]]
for r in screen["MU"]:
    v = "SELECTED" if r["K"]==pick["MU"]["K"] else ("fails delta floor" if r["delta"]<0.20 else "clears floor, lower gamma/$")
    rows.append([f"{r['K']}C", f"{r['mid']:.2f}", f"{r['iv']:.1%}", f"{r['delta']:.3f}", f"{r['gamma']:.5f}", f"{r['gpp']:.4f}", f"${r['cost']:,.0f}", f"{r['oi']:,}", v])
S.append(tbl(rows,[0.6*inch,0.55*inch,0.5*inch,0.5*inch,0.6*inch,0.95*inch,0.65*inch,0.6*inch,1.7*inch])); S.append(Spacer(1,5))
S.append(Paragraph(
 "<b>Roll and re-strike of carried legs.</b> Every V2 leg was re-screened at Nov 20 '26 (V2 strikes shown in parentheses): NVDA 255C (245C), RTX 200C (205C; the Nov chain has no 205 strike and 210C fails the delta floor at 0.141), "
 "MRVL 330C (305C), GDX 98C (108C; the Nov chain tops out at 102 and GDX has retraced to 86.13, so the 98C is the max-gamma strike that clears the floor). "
 "<b>Dropped:</b> LMT 550C/555C screen at 0.079&ndash;0.086 gamma/$, the worst of all 28 candidates, with 35&ndash;137 OI; SKHY 230C (0.122 gamma/$) was the memory proxy carried in V2 "
 "because the MU contract was unaffordable &mdash; with MU now held outright the SKHY leg duplicates exposure and was released to fund it. The $204 residual was used for a second GDX 98C.", B))

S.append(Paragraph("3. Scenario Ladder &amp; Portfolio Payout (marked Nov 16 '26, 4 DTE, Black-Scholes at entry IV)", H2))
S.append(Paragraph("Base case anchors at a uniform +18% spot move across all legs. Bull and Gamma Upside stack each name's own 42-day &sigma; (&sigma; = IV &times; &radic;(42/365)) on top of the +18% base. "
 "Flat (0%) is shown as the time-decay reference point for the 4-DTE exit mark.", B))
rows=[["Leg","Flat (0%)","Base +18%","Bull (+18%+1σ)","Gamma Upside (+18%+2σ)"]]
for tk,n in legs:
    p=pick[tk]; c=p['cost']*n
    def cell(s): r=scen[s]['rows'][tk]; return f"{r['pnl']:+,.0f} ({r['ret']:+.0%})"
    def mv(s): return f"{scen[s]['rows'][tk]['move']:+.1%}"
    rows.append([f"{tk} {p['K']}C (x{n})", cell('Flat'), cell('Base'), f"{cell('Bull')}  @{mv('Bull')}", f"{cell('Gamma')}  @{mv('Gamma')}"])
S.append(tbl(rows,[1.15*inch,1.2*inch,1.3*inch,1.7*inch,1.9*inch])); S.append(Spacer(1,5))
rows=[["Scenario","Portfolio P&L","Ending Value","Return on $5,000"]]
for s,lab in [("Flat","Flat (0%)"),("Base","Base (+18%)"),("Bull","Bull (+18%+1σ)"),("Gamma","Gamma Upside (+18%+2σ)")]:
    v=scen[s]; rows.append([lab, f"{v['pnl']:+,.0f}", f"${v['end']:,.0f}", f"{v['ret']:+.1%}"])
S.append(tbl(rows,[1.9*inch,1.4*inch,1.4*inch,1.5*inch])); S.append(Spacer(1,5))

# MU sensitivity
p=pick['MU']; TH=42/365; sig=p['iv']*sqrt(TH)
lo,hi=1100.0,1500.0
for _ in range(80):
    mid_=(lo+hi)/2
    if bs(mid_,1300,4/365,p['iv'])*100 < p['cost']: lo=mid_
    else: hi=mid_
BE=(lo+hi)/2
S.append(Paragraph(f"<b>MU anchor-leg sensitivity (Nov 16 mark).</b> MU is {p['cost']/5000:.0%} of the book, so the sleeve's return is dominated by where MU prints on Nov 16. "
 f"42-day 1&sigma; at 57.0% IV = {sig:.1%} (${spot['MU']*sig:,.0f}). Breakeven at the 4-DTE mark is MU &asymp; ${BE:,.0f} ({BE/spot['MU']-1:+.1%}; "
 f"vs. ${1300+p['mid']:,.0f} / {(1300+p['mid'])/spot['MU']-1:+.1%} at expiry). Other legs held at the Base (+18%) column for the book-level row.", B))
rows=[["MU on Nov 16","Move","Call value","MU leg P&L","MU leg return","Book P&L (others @ Base)","Book return"]]
others_base = scen['Base']['pnl'] - scen['Base']['rows']['MU']['pnl']
for mvp in [0.0,0.10,0.18,0.25,0.30,sig+0.18,0.45,0.50,2*sig+0.18,0.75,1.00]:
    S1=spot['MU']*(1+mvp); v=bs(S1,1300,4/365,p['iv'])*100; pnl=v-p['cost']
    rows.append([f"${S1:,.0f}", f"{mvp:+.1%}", f"${v:,.0f}", f"{pnl:+,.0f}", f"{pnl/p['cost']:+.0%}", f"{pnl+others_base:+,.0f}", f"{(pnl+others_base)/5000:+.0%}"])
S.append(tbl(rows,[0.95*inch,0.7*inch,0.85*inch,0.95*inch,0.95*inch,1.55*inch,0.9*inch]))

S.append(Paragraph("4. Backtest: Historical Frequency of Modeled 6-Week Moves", H2))
S.append(Paragraph("All overlapping 6-week (42-day) forward returns were computed from 2 years of weekly closes (n=99 windows per name, IBKR historical data through the 9/28/26 bar). "
 "Hit rates are measured against each name's own V3 thresholds (Bull and Gamma use the leg's entry IV, so thresholds differ by name and are shown). SKHY (13 weekly bars since listing) "
 "is excluded; LMT is shown for reference although it is no longer in the book.", B))
rows=[["Ticker","Real. Vol","Entry IV","Mean 6wk","Max 6wk","Base thr.","Hit Base","Bull thr.","Hit Bull","Gamma thr.","Hit Gamma"]]
for tk in ["MU","NVDA","RTX","MRVL","GDX","LMT"]:
    v=bt[tk]; rows.append([tk+("*" if tk=="LMT" else ""), f"{v['rv']:.1%}", f"{v['iv']:.1%}", f"{v['mean']:+.1%}", f"{v['mx']:+.1%}", f"{v['base']:.0%}", f"{v['hb']:.0%}", f"{v['bull']:.1%}", f"{v['hu']:.0%}", f"{v['gam']:.1%}", f"{v['hg']:.0%}"])
S.append(tbl(rows,[0.5*inch,0.65*inch,0.6*inch,0.65*inch,0.65*inch,0.6*inch,0.6*inch,0.6*inch,0.6*inch,0.7*inch,0.7*inch]))
S.append(Paragraph("* LMT not in the V3 book; shown for continuity with V2.", SM)); S.append(Spacer(1,4))
S.append(Paragraph("Key findings:", B))
for s in [
 f"<b>MU is the only leg whose Bull threshold (+{bt['MU']['bull']:.1%}) has a double-digit historical hit rate ({bt['MU']['hu']:.0%} of windows); its Gamma Upside threshold (+{bt['MU']['gam']:.1%}) has printed in {bt['MU']['hg']:.0%} of windows (max observed 6-week move: +{bt['MU']['mx']:.1%}).</b> Mean 6-week return in-sample is +{bt['MU']['mean']:.1%}, i.e. the uniform +18% Base case is MU's historical average, not a tail.",
 f"Extending the window from 5 to 6 weeks raises Base hit rates versus V2 for every carried name (MU 39%&rarr;{bt['MU']['hb']:.0%}, MRVL 32%&rarr;{bt['MRVL']['hb']:.0%}, GDX 14%&rarr;{bt['GDX']['hb']:.0%}, RTX 0%&rarr;{bt['RTX']['hb']:.0%}); NVDA is flat at {bt['NVDA']['hb']:.0%}.",
 f"Entry IVs sit within 2&ndash;10 points of 2-year realized vol on every leg (MU 57.0% vs {bt['MU']['rv']:.1%} realized is the largest discount: the leg is bought at a vol below what the name has delivered).",
 f"RTX and GDX function as cheap-gamma ballast (0.60 and 1.21 gamma/$); RTX's +18% Base has now occurred in {bt['RTX']['hb']:.0%} of windows (max +{bt['RTX']['mx']:.1%}), GDX's in {bt['GDX']['hb']:.0%}. Their Bull/Gamma thresholds remain out-of-sample events.",
 "In-window dated catalysts (approx.): RTX Q3 print ~Oct 20&ndash;21; FOMC Oct 27&ndash;28; SK Hynix Q3 results late Oct (direct HBM/DRAM pricing read-through to MU); NVDA's Q3 print (~Nov 18&ndash;19) falls after the Nov 16 exit, so the NVDA leg is sold into pre-earnings IV rather than through the event; MU's own fiscal Q1 report is mid-/late-December, outside the window.",
]:
    S.append(Paragraph(s, BL, bulletText='•'))

S.append(Paragraph("5. Assessment &amp; Recommendation", H2))
S.append(Paragraph(
 f"All five legs clear the delta &ge; 0.20 floor with positive gamma-per-premium, and the book is fully deployed (${dep:,.0f} of $5,000). The structure has changed character from V2: "
 f"it is now a <b>concentrated MU convexity position with four satellite gamma legs</b>. MU contributes {scen['Bull']['rows']['MU']['pnl']/scen['Bull']['pnl']:.0%} of Bull P&L and "
 f"{scen['Gamma']['rows']['MU']['pnl']/scen['Gamma']['pnl']:.0%} of Gamma Upside P&L. The Base (+18% uniform) column is carried by NVDA/RTX/GDX, while MU and MRVL sit just below "
 f"strike at the 4-DTE mark (the 1300 strike is +19.1% from spot); MU needs a {BE/spot['MU']-1:+.1%} move to break even at the Nov 16 mark and a +{sig+0.18:.1%} move (Bull) to return "
 f"{scen['Bull']['rows']['MU']['ret']:+.0%} on the leg. The 6-week extension works in the book's favor on both axes: historical Base/Bull hit rates rise across the board, and the Nov 20 "
 f"monthly carries materially deeper open interest than the Oct 30 weeklies used in V2 (MU 3,722; NVDA 11,600; GDX 3,000).", B))
S.append(Paragraph(
 "Concentration note: MU plus MRVL is 78% of premium. Where the user wants the MU weight reduced without leaving the name, the alternative is MU 1350C (delta 0.182, $2,355) which "
 "breaks the delta floor but frees $710 &mdash; enough to restore SKHY 230C and hold cash. That variant is not modeled here; the mandate was to maximize upside, which the 1300C delivers "
 f"(Gamma Upside leg P&L {scen['Gamma']['rows']['MU']['pnl']:+,.0f} vs an estimated +{(bs(spot['MU']*(1.18+2*sig),1350,4/365,.577)*100-2355):,.0f} for 1350C).", B))
S.append(Spacer(1,6))
S.append(Paragraph("Methodology: Black-Scholes (r=4%, q=0%) at entry (46 DTE) for delta/gamma; entry $/ctr = IBKR SMART mid quote at 2026-10-02 close ×100; scenarios marked Nov 16 '26 "
 "by Black-Scholes at 4 DTE using each leg's entry IV (no vol change assumed). Scenario σ = IV × √(42/365). Backtest: IBKR weekly closes, 2-year lookback, overlapping 6-week forward returns, "
 "n=99 per name. Model code: memos/ritts_6wk_model_v3.py. Not investment advice.", SM))
doc.build(S)
print("ok")
