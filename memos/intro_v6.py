"""Introduction to the high-convexity, high-gamma long-premium strategy, with the January 2026 statement as the realized reference."""
import json
from reportlab.platypus import Spacer, Table, TableStyle, KeepTogether
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.graphics.shapes import Drawing, Rect, String, Line
from bxpe import Paragraph, h1, h2, sub, tbl, bullets, note, stats, BODY, NOTE, CHART, GRAYTXT, RULE, BLACK
from addendum_jan2026 import opt, wins, losses, expired, top10, net_parsed, BEGIN, CHG, by

rets=sorted((r["gl"]/r["basis"] for r in opt if r["basis"]>0))
n=len(rets); n100=sum(x>=1 for x in rets); n200=sum(x>=2 for x in rets); nloss=sum(x<0 for x in rets); nfull=sum(x<=-0.99 for x in rets)
top5=sum(r["gl"] for r in sorted(opt,key=lambda r:-r["gl"])[:5])

def signature(width=7.3*inch, height=2.3*inch):
    """Sorted per-closing returns on premium, January 2026: the convexity signature (many small losses, a few large wins)."""
    d=Drawing(width,height); L=0.55*inch; R=width-0.1*inch; T=0.15*inch; B=0.35*inch
    lo,hi=-1.0,max(rets); ph=height-T-B; y0=B+ph*(0-lo)/(hi-lo)
    def y(v): return B+ph*(v-lo)/(hi-lo)
    bw=(R-L)/n
    for i,v in enumerate(rets):
        col = colors.HexColor(CHART[1]) if v>=1 else (colors.HexColor(CHART[0]) if v>0 else colors.HexColor(CHART[4]))
        top=max(y(v),y0); bot=min(y(v),y0)
        d.add(Rect(L+i*bw, bot, max(bw-0.6,0.4), top-bot, fillColor=col, strokeColor=None))
    for v in (-1.0,0.0,1.0,2.0,3.0,4.0,5.0):
        d.add(Line(L,y(v),R,y(v),strokeColor=RULE,strokeWidth=0.4))
        d.add(String(L-4,y(v)-2.5,f"{v:+.0%}",fontName="SourceSans3-Regular",fontSize=6.5,fillColor=GRAYTXT,textAnchor="end"))
    d.add(Line(L,y0,R,y0,strokeColor=BLACK,strokeWidth=0.6))
    d.add(String(L,B-11,f"{n} option closings, January 1-30, 2026, sorted by return on premium paid",fontName="SourceSans3-Regular",fontSize=6.8,fillColor=GRAYTXT))
    d.add(String(R,B-11,f"gray: {nloss} losers ({nfull} at -100%)   teal: {n-nloss-n100} winners under +100%   dark: {n100} at +100% or more",fontName="SourceSans3-Regular",fontSize=6.8,fillColor=GRAYTXT,textAnchor="end"))
    return d

def intro(noteref=None, gamma_note="see Scenario Ladder"):
    S=[h1("The Strategy: High-Convexity, High-Gamma Long Premium", noteref), sub("(what the sleeve does, why it is built from gamma, and what the same process produced in January 2026)")]
    S.append(Paragraph(
     "The sleeve buys listed options outright, short-dated and out of the money, and never sells premium against them. Each line can lose only what it cost, and each line can return several multiples of that cost if the "
     "underlying moves far enough, fast enough. That asymmetry is the whole strategy: the loss is capped at the premium, the gain is not, and the book is built so that a few lines that pay 100&#8211;500% "
     "carry a larger number that expire worthless or are cut.", BODY))
    S.append(Paragraph(
     "<b>Why gamma.</b> An option's delta is its exposure to the next dollar of the move; gamma is how fast that exposure grows as the move continues. A 25-delta call behaves like 25 shares at entry, 50 shares after a one-standard-deviation rally and close to 100 shares after two, "
     "so the position is small when it is wrong and large when it is right. Gamma is highest in options that are close to expiry and close to the money, which is why the sleeve holds 3&#8211;7 week tenors at 20&#8211;35 delta and ranks every candidate on gamma per dollar of premium: "
     "the ranking finds the contracts where a given move produces the most convexity for the least capital. The cost of that convexity is theta, the daily decay of the premium, which is why a flat tape is the losing case in every version of this memo and why the window is dated and the exits are fixed.", BODY))
    S.append(Paragraph(
     "<b>What has to happen.</b> Each line needs the underlying to move at least one standard deviation of its own implied volatility over the hold to roughly double, and two to three to pay the multiples the Gamma Upside Case assumes. The two-year backtest measures how often each name has done that; "
     "the ladder prices what the contract is worth when it does. Diversification across sleeves is not for safety in the usual sense, since every line can still go to zero; it is to have several independent chances at the move, each with its own catalyst.", BODY))
    S.append(h2("Linkage to Past Usage: January 2026"))
    S.append(Paragraph(
     f"The same process ran in a Ritts-family self-directed Roth IRA in January 2026 (detailed in the Addendum). The account began the month at ${BEGIN:,.0f}, took ${11617:,.0f} out, and ended at $77,821: a +{CHG/BEGIN:.0%} change in investment value in 20 trading days with no deposits. "
     f"It did that with the payoff shape described above, not with a high hit rate. Of {n} option closings, {nloss} lost money and {nfull} expired worthless at &#8722;100%; {n100} returned +100% or more and {n200} returned +200% or more. "
     f"The five largest closings produced ${top5:,.0f}, {top5/net_parsed:.0%} of the parsed net option P&L of ${net_parsed:,.0f}, and the ten largest exceeded it, which means every closing outside the top ten lost money in aggregate. The chart is that distribution, sorted.", BODY))
    S.append(signature()); S.append(Spacer(1,4))
    jan={u:v for u,v in by.items()}
    rows=[["Dimension","January 2026 (realized)","RWS V6 (model)"]]
    for a,b,c in [
     ("Instrument","Short-dated long calls (and a few puts); 1&#8211;6 week tenors; 1&#8211;5 contracts per line","Short-dated long calls and one index put; 3&#8211;7 week tenors; 1&#8211;2 contracts per line"),
     ("Sectors","Aerospace/defense, semis/memory, gold/metals, plus single-name tech","Memory/AI compute, defense, gold, AI power, index hedge"),
     ("Names in common",f"MU (+${jan['MU']['gl']:,.0f}), RTX (+${jan['RTX']['gl']:,.0f}), NOC (+${jan['NOC']['gl']:,.0f}), GLD (+${jan['GLD']['gl']:,.0f}), BA (+${jan['BA']['gl']:,.0f}), LMT, GDX","MU via DRAM/SKHY, RTX, GLD, GDX, BA, NVDA, VRT; NOC and LMT screened out on open interest"),
     ("Lines open at once","30&#8211;45","3, then 6, then 9 (twelve contracts)"),
     ("Win rate",f"{len(wins)}/{n} closings ({len(wins)/n:.0%}); {len(expired)} lines expired worthless","Backtest hit rate on +1 s.d.: 22&#8211;42% per leg; the ladder assumes a few legs reach +2 or +3 s.d."),
     ("Payoff concentration",f"Top 5 closings = {top5/net_parsed:.0%} of net option P&L; top 10 &gt; 100%",gamma_note),
     ("Result / model",f"+{CHG/BEGIN:.0%} on beginning capital in 20 trading days","Base +59%, Bull +413%, Gamma Upside +857% over 42 days; Flat &#8722;70%"),
     ("What V6 adds","All lines carried from day one through the month's events; no index hedge","Three dated tranches (24% / 58% / 92%), 25% ticket cap, 40% sleeve cap, SPY put, cut and profit-taking rules"),
    ]: rows.append([a, Paragraph(b, NOTE), Paragraph(c, NOTE)])
    S.append(tbl(rows,[1.3,3.0,3.0],font=7.4))
    S.append(Paragraph(
     f"The January month is the realized precedent for the ladder's shape, not a forecast of its level: it was produced with 30&#8211;45 concurrent lines and larger single tickets, in a month when defense and gold both moved more than two standard deviations. "
     f"V6 keeps the instrument, the sectors and the payoff shape, and changes how much is at risk on any given date.", NOTE))
    return S
