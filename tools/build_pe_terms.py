"""Builds guides/D.B._Ritts_III_PE_Essentials_Guide.pptx (Guide #2 in profile-deck format)."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import pptkit
pptkit.FOOTER = "D. B. Ritts III — PE Essentials: Terminology, Structure & Concepts"
from pptkit import *
from pptx.chart.data import CategoryChartData
from pptx.enum.chart import XL_CHART_TYPE
from pptx.util import Inches, Pt

OUT = os.path.join(os.path.dirname(__file__), "..", "guides", "D.B._Ritts_III_PE_Essentials_Guide.pptx")
p = new_deck()

def slide(section, title, ts=30):
    s = blank(p); header(s, section, title, ts); return s

def card(s, x, y, w, h, title, body, fill=NAVY, size=9.2):
    band(s, x, y, w, 0.32, title, fill=fill, size=9)
    rect(s, x, y + 0.32, w, h - 0.32, fill=WHITE, line=LINE)
    if isinstance(body, list):
        bullets(s, x + 0.1, y + 0.4, w - 0.2, h - 0.45, body, size=size, spacing=3)
    else:
        txt(s, x + 0.1, y + 0.4, w - 0.2, h - 0.45, body, size=size)

def hline(s, x, y, w, c=NAVY): rect(s, x, y, w, 0.02, fill=c)
def vline(s, x, y, h, c=NAVY): rect(s, x, y, 0.02, h, fill=c)

# ---------------------------------------------------------------- 1 COVER
s = blank(p)
txt(s, 0.5, 0.45, 12.3, 0.8, "Private Equity Essentials: Terminology, Structure & Concepts", size=27, color=NAVY, font=SERIF)
rect(s, 0.5, 1.3, 12.33, 0.012, fill=LINE)
txt(s, 0.5, 1.42, 12, 0.3, [[("Reference map  ·  Fund structure → economics → metrics → deals → capital structure → terms → exits → regulation", {"caps": True, "track": 120})]], size=10.5, color=MUTED)
rect(s, 0.5, 1.95, 4.1, 4.8, fill=NAVY)
txt(s, 0.8, 2.15, 3.6, 1.3, "The vocabulary of private capital, organized as a system", size=20, color=WHITE, font=SERIF)
rect(s, 0.8, 3.5, 0.6, 0.02, fill=GOLD)
txt(s, 0.8, 3.65, 3.6, 1.4, "Every term sits in one of ten domains. Learn the structure first, then the economics and metrics; the deal, capital-structure and legal terms hang off that skeleton.", size=11, color=WHITE)
rect(s, 0.8, 5.05, 3.5, 0.01, fill=RGBColor(0x55, 0x66, 0x88))
txt(s, 0.8, 5.2, 3.6, 1.4, "▸ marks where a concept appears in the Leviathan holdco model, so each term ties back to a live example.", size=11, color=WHITE)
doms = [("Structure", "GP, LP, ManCo, feeders, blockers, SPVs"), ("Lifecycle", "Closes, calls, investment & harvest periods"), ("Economics", "Fees, carry, hurdle, catch-up, waterfall"),
        ("Metrics", "IRR, MOIC, TVPI, DPI, PME, J-curve"), ("Strategies", "VC, growth, buyout, secondaries, credit"), ("Deal process", "Teaser → LOI → diligence → close"),
        ("Valuation", "EV bridge, multiples, pre/post-money"), ("Capital structure", "Revolver → TLB → mezz → equity"), ("Equity terms", "Prefs, anti-dilution, drag / tag, board"),
        ("Exits & regulation", "IPO, M&A, CFIUS, ITAR, defense contracting")]
for i, (a, b) in enumerate(doms):
    col, row = i % 2, i // 2
    x = 4.85 + col * 4.02; y = 1.95 + row * 0.98
    rect(s, x, y, 3.94, 0.9, fill=PANEL if row % 2 == 0 else WHITE, line=LINE)
    num(s, x + 0.12, y + 0.29, i + 1, d=0.32, size=10)
    txt(s, x + 0.55, y + 0.08, 3.3, 0.8, [[(a, {"bold": True, "caps": True, "color": NAVY})], [(b, {"color": MUTED})]], size=10, anchor="m")
txt(s, 0.5, 7.05, 8, 0.25, pptkit.FOOTER, size=8, color=GREY)

# ---------------------------------------------------------------- 2 FUND STRUCTURE DIAGRAM
s = slide("01 | Structure", "How a Private Equity Fund Is Structured")
# LPs
rect(s, 0.6, 1.5, 7.6, 0.75, fill=PANEL, line=LINE)
txt(s, 0.6, 1.5, 7.6, 0.75, [[("Limited Partners (LPs)", {"bold": True, "caps": True, "color": NAVY})], "Pensions · endowments · sovereign wealth · insurers · family offices · HNW / wealth platforms"], size=10, align="c", anchor="m")
# feeders
for i, (a, b) in enumerate([("Feeder fund", "Pools offshore / wealth investors"), ("Parallel fund", "Side-by-side for ERISA / non-US"), ("Blocker corp.", "Blocks UBTI / ECI")]):
    x = 0.6 + i * 1.95
    rect(s, x, 2.6, 1.8, 0.7, fill=WHITE, line=LINE)
    txt(s, x, 2.6, 1.8, 0.7, [[(a, {"bold": True, "color": NAVY})], [(b, {"size": 8.5, "color": MUTED})]], size=9.5, align="c", anchor="m")
vline(s, 4.4, 2.25, 0.35); vline(s, 4.4, 3.3, 0.35)
txt(s, 4.5, 2.27, 2.2, 0.3, "commitments / capital calls", size=8, color=MUTED)
# fund
rect(s, 2.6, 3.65, 3.6, 0.85, fill=NAVY)
txt(s, 2.6, 3.65, 3.6, 0.85, [[("The Fund (Limited Partnership)", {"bold": True})], [("Closed-end, ~10 yrs + extensions · governed by the LPA", {"size": 8.5})]], size=10.5, color=WHITE, align="c", anchor="m")
# GP and ManCo
rect(s, 6.6, 3.65, 1.6, 0.85, fill=TEAL)
txt(s, 6.6, 3.65, 1.6, 0.85, [[("General Partner", {"bold": True})], [("controls fund; earns carry", {"size": 8})]], size=9.5, color=WHITE, align="c", anchor="m")
hline(s, 6.2, 4.07, 0.4, TEAL)
rect(s, 6.6, 2.6, 1.6, 0.7, fill=WHITE, line=TEAL, lw=1.25)
txt(s, 6.6, 2.6, 1.6, 0.7, [[("Management Co.", {"bold": True, "color": TEAL})], [("adviser; earns mgmt fee", {"size": 8, "color": MUTED})]], size=9.5, align="c", anchor="m")
vline(s, 7.4, 3.3, 0.35, TEAL)
# portfolio
vline(s, 4.4, 4.5, 0.4)
hline(s, 1.3, 4.9, 6.2)
for i, (a, b) in enumerate([("Portfolio Co. A", "control buyout"), ("Portfolio Co. B", "minority stake"), ("Co-invest SPV", "LPs alongside fund"), ("AIV", "deal-specific vehicle")]):
    x = 0.6 + i * 1.95
    vline(s, x + 0.85, 4.9, 0.3)
    rect(s, x, 5.2, 1.75, 0.75, fill=WHITE, line=LINE)
    txt(s, x, 5.2, 1.75, 0.75, [[(a, {"bold": True, "color": NAVY})], [(b, {"size": 8.5, "color": MUTED})]], size=9.5, align="c", anchor="m")
rect(s, 0.6, 6.1, 7.6, 0.75, fill=PANEL, line=LINE)
txt(s, 0.75, 6.1, 7.35, 0.75, [[("Cash flows: ", {"bold": True, "color": NAVY}), ("LPs fund calls → fund invests → exits return cash → waterfall splits proceeds between LPs and the GP (carry). The ManCo is paid the management fee for running the strategy.", {})]], size=9.5, anchor="m")
band(s, 8.5, 1.5, 4.33, 0.32, "Who does what")
table(s, 8.5, 1.82, 4.33, 5.03, [["Entity", "Role / economics"],
    ["GP", "Legal control; unlimited liability (via LLC); receives carry"],
    ["LP", "Passive capital; liability capped at commitment"],
    ["ManCo", "Registered adviser; employs team; receives fees"],
    ["LPA", "Contract: terms, governance, economics"],
    ["LPAC", "Large-LP committee: conflicts, valuations, extensions"],
    ["Side letter", "LP-specific terms; usually with MFN"],
    ["GP commit", "GP’s own capital (1–5%): alignment"],
    [("▸ Leviathan", {"bold": True, "color": TEAL}), "$855M holdco across 3 sleeves = sub-fund structure"]], col_w=[1.1, 3.2], size=9, align=["l", "l"])

# ---------------------------------------------------------------- 3 VEHICLES GLOSSARY
s = slide("01 | Structure", "Vehicles and Governance: Core Structural Terms")
table(s, 0.5, 1.45, 6.06, 5.4, [["Vehicle", "Definition", "Why it matters"],
    ["Feeder fund", "Pools investors into the main fund", "Tax / regulatory access"],
    ["Parallel fund", "Separate vehicle investing pro rata", "Same deals, different wrapper"],
    ["AIV", "Deal-specific alternative vehicle", "Routes one investment"],
    ["Blocker corp.", "Corporation interposed for tax", "Avoids UBTI / ECI"],
    ["SPV", "Single-asset vehicle", "Co-invest, deal-by-deal economics"],
    ["Co-investment", "LP invests directly beside fund", "Low / no fee & carry"],
    ["Fund of funds", "Invests in other PE funds", "Diversification; double fees"],
    ["SMA", "Single-LP custom mandate", "Custom terms for large LPs"],
    ["Evergreen fund", "Open-ended, periodic liquidity", "No fixed term; gates"],
    ["Continuation vehicle", "GP-led secondary: assets roll to new vehicle", "Extends hold on winners"],
    [("▸ Holdco / sleeve", {"bold": True, "color": TEAL}), "Holding company with sub-strategies", "IQT / Weapons / Consumer"]],
    col_w=[1.5, 2.6, 1.95], size=8.8, align=["l", "l", "l"])
table(s, 6.77, 1.45, 6.06, 4.1, [["Governance term", "Definition"],
    ["PPM", "Offering memorandum: strategy, team, risks, terms"],
    ["Subscription docs", "Binding commitment and investor qualification"],
    ["MFN", "LP may elect better terms given to similar-size LPs"],
    ["Key person clause", "Investment period suspends if named partners leave"],
    ["No-fault divorce", "LP supermajority can remove GP without cause"],
    ["GP removal for cause", "Removal after fraud, breach or gross negligence"],
    ["ILPA Principles", "LP best-practice standards for terms and reporting"],
    ["Equalization", "Late closers compensate earlier LPs with interest"]],
    hdr_fill=TEAL, col_w=[1.8, 4.2], size=9, align=["l", "l"])
rect(s, 6.77, 5.7, 6.06, 1.15, fill=NAVY)
txt(s, 6.92, 5.72, 5.8, 1.1, [[("Rule of thumb", {"caps": True, "bold": True, "color": GOLD, "size": 9})], [("Every extra vehicle exists to solve a tax, regulatory or economics problem for a specific investor class. Ask which problem a structure solves.", {"font": SERIF, "size": 12})]], size=10, color=WHITE, spacing=3, anchor="m")

# ---------------------------------------------------------------- 4 LIFECYCLE
s = slide("02 | Lifecycle", "Fund Lifecycle: From First Close to Wind-Down")
ph = [("Fundraise", "Year 0 (12–18 mo)", ["First and final close", "LPA and side letters", "GP commitment"]),
      ("Investment period", "Years 1–5", ["Capital calls", "New platforms", "Follow-on reserve set"]),
      ("Value creation", "Years 3–8", ["100-day plans", "Add-ons, follow-ons", "Operating improvements"]),
      ("Harvest", "Years 4–10", ["Exits, distributions", "Recycling (capped)", "DPI builds"]),
      ("Extension / wind-down", "Years 10–12", ["1–2 yr extensions", "Tail sales / CVs", "Final distributions"])]
cw = 12.33 / 5
for i, (a, b, bl) in enumerate(ph):
    x = 0.5 + i * cw
    rect(s, x + 0.03, 1.5, cw - 0.3, 0.6, fill=NAVY if i != 3 else TEAL)
    txt(s, x + 0.03, 1.5, cw - 0.3, 0.6, [[(a, {"bold": True, "caps": True})], [(b, {"size": 8.5})]], size=9.5, color=WHITE, align="c", anchor="m")
    rect(s, x + 0.03, 2.1, cw - 0.3, 1.35, fill=WHITE, line=LINE)
    bullets(s, x + 0.12, 2.2, cw - 0.45, 1.2, bl, size=9.2)
    if i < 4: arrow(s, x + cw - 0.24, 1.73, 0.18, 0.14)
table(s, 0.5, 3.65, 8.1, 3.2, [["Term", "Definition"],
    ["Commitment", "Total capital an LP agrees to provide over the fund’s life"],
    ["Capital call (drawdown)", "GP request for part of commitments, ~10 business days’ notice"],
    ["Paid-in capital (PIC) / unfunded", "Capital called to date / commitment not yet called"],
    ["Dry powder", "Uncalled capital available to invest"],
    ["Recycling", "Reinvesting early proceeds instead of distributing (capped)"],
    ["Subscription line", "Loan secured by LP commitments; delays calls and inflates IRR"],
    ["NAV loan", "Fund-level borrowing secured by portfolio value"],
    ["Vintage year", "Year of first investment; used for peer comparison"]], col_w=[2.4, 5.7], size=9, align=["l", "l"])
rect(s, 8.8, 3.65, 4.03, 3.2, fill=PANEL, line=LINE)
txt(s, 8.95, 3.72, 3.75, 3.1, [[("▸ Leviathan application", {"bold": True, "caps": True, "color": TEAL})],
    "Three hold vehicles (5 / 7 / 10 yrs) price the same names on different lifecycles.",
    "IQT sleeve keeps a $25M follow-on reserve of $250M, embedded in retention factors.",
    "Pre-IPO and listed names (MSL, Syntiant, Infleqtion) pull DPI forward relative to private exits."], size=9.5, spacing=6)

# ---------------------------------------------------------------- 5 ECONOMICS TERMS
s = slide("03 | Economics", "Fund Economics: Fees, Carry, Hurdles and Waterfalls")
card(s, 0.5, 1.45, 4.0, 2.6, "Fees", [("Management fee: ", "1.5–2.0% of committed capital in the investment period, then of invested capital or a lower rate"), ("Fee offset: ", "80–100% of deal / monitoring fees credited against the fee"), ("Fund expenses: ", "audit, admin, legal, broken-deal costs; org. expenses capped")])
card(s, 4.67, 1.45, 4.0, 2.6, "Carry & hurdle", [("Carried interest: ", "GP share of profits, typically 20% (10–30%)"), ("Preferred return: ", "LP minimum return before carry, usually 8% compounded"), ("Catch-up: ", "after the pref, GP takes a large share (often 100%) until it holds 20% of total profit")], fill=TEAL)
card(s, 8.83, 1.45, 4.0, 2.6, "Protections", [("Clawback: ", "GP returns carry not supported by final fund results"), ("Escrow / holdback: ", "part of carry withheld to secure the clawback"), ("GP commitment: ", "1–5% of fund from the GP: alignment")], fill=BURG)
for j, (hd, f, pts) in enumerate([("European (whole-fund) waterfall", NAVY, ["Carry only after LPs receive all contributed capital + pref across the whole fund", "LP-friendly; carry arrives late", "▸ Leviathan uses whole-fund, no catch-up"]),
                                   ("American (deal-by-deal) waterfall", GREY, ["Carry paid on each realized deal after that deal’s cost and expenses", "GP-friendly; carry arrives early", "Needs a clawback to protect LPs"])]):
    x = 0.5 + j * 6.4
    band(s, x, 4.25, 5.93, 0.32, hd, fill=f)
    rect(s, x, 4.57, 5.93, 1.4, fill=WHITE, line=LINE)
    bullets(s, x + 0.15, 4.65, 5.65, 1.3, pts, size=9.5, spacing=4)
txt(s, 6.43, 4.9, 0.5, 0.5, "VS.", size=14, color=NAVY, font=SERIF, align="c")
rect(s, 0.5, 6.1, 12.33, 0.75, fill=PANEL, line=LINE)
txt(s, 0.65, 6.1, 12.1, 0.75, [[("Hard vs. soft hurdle: ", {"bold": True, "color": NAVY}), ("a hard hurdle pays carry only on profit above the pref (no catch-up). A soft hurdle, once met, pays carry on all profit through the catch-up. The difference grows with performance; see the worked example next.", {})]], size=10, anchor="m")

# ---------------------------------------------------------------- 6 WATERFALL WORKED
s = slide("03 | Economics", "Worked Waterfall: $100M Fund, $250M Gross Proceeds, 5-Year Single Exit")
tiers = [("1  Return of capital", "100% to LPs until contributed capital is returned", "$100.00M"), ("2  Preferred return", "100% to LPs until 8% compounded is paid: 100 × (1.08⁵ − 1)", "$46.93M"),
         ("3  GP catch-up", "100% to GP until GP holds 20% of profit (soft hurdle only)", "$11.73M"), ("4  Carried interest split", "Remaining profit split 80% LP / 20% GP", "$91.34M")]
for i, (a, b, v) in enumerate(tiers):
    y = 1.5 + i * 0.95
    w = 6.0 - i * 0.35
    rect(s, 0.5, y, w, 0.82, fill=[NAVY, NAVY, GOLD, TEAL][i])
    txt(s, 0.62, y, w - 1.4, 0.82, [[(a, {"bold": True, "caps": True})], [(b, {"size": 8.8})]], size=9.5, color=WHITE, anchor="m")
    txt(s, 0.5 + w - 1.3, y, 1.2, 0.82, v, size=13, color=WHITE, font=SERIF, align="r", anchor="m")
txt(s, 0.5, 5.35, 6.0, 0.35, [[("Total profit = $150M  ·  Pref = $46.93M  ·  Full catch-up = Pref × 20 / 80", {"bold": True})]], size=9.5, color=NAVY)
band(s, 6.77, 1.5, 6.06, 0.32, "Outcome by waterfall design")
table(s, 6.77, 1.82, 6.06, 3.3, [["Tier", "Full catch-up (soft)", "No catch-up (hard) ▸"],
    ["Return of capital (LP)", "100.00", "100.00"], ["Preferred 8% (LP)", "46.93", "46.93"], ["GP catch-up", "11.73", "—"],
    ["Remaining split 80 / 20", "LP 73.07 / GP 18.27", "LP 82.46 / GP 20.61"],
    [("GP carry total", {"bold": True, "color": NAVY}), ("30.00 (20% of 150)", {"bold": True}), ("20.61", {"bold": True})],
    [("LP total before fees", {"bold": True, "color": NAVY}), ("220.00", {"bold": True}), ("229.39", {"bold": True})]], col_w=[2.0, 2.1, 2.0], size=9.5)
rect(s, 6.77, 5.25, 6.06, 1.6, fill=NAVY)
txt(s, 6.92, 5.28, 5.8, 1.55, [[("Read-through", {"caps": True, "bold": True, "color": GOLD, "size": 9})],
    [("Catch-up is worth $9.4M to the GP here, and the gap widens as performance rises.", {"font": SERIF, "size": 12.5})],
    "Fees come off afterward: 2% × $100M × 5 yrs = $10M. Leviathan models the hard (no catch-up) case, which flatters LP returns in upside scenarios."], size=9.3, color=WHITE, spacing=4, anchor="m")
rect(s, 0.5, 5.8, 6.0, 1.05, fill=PANEL, line=LINE)
txt(s, 0.65, 5.8, 5.75, 1.05, [[("Check: ", {"bold": True, "color": NAVY}), ("100 + 46.93 + 11.73 + 91.34 = $250M. With full catch-up, GP carry = 11.73 + 18.27 = $30.0M = exactly 20% of the $150M profit.", {})]], size=9.5, anchor="m")

# ---------------------------------------------------------------- 7 METRICS
s = slide("04 | Metrics", "Performance Metrics: What Each One Measures and How It Misleads")
mets = [("MOIC", "Total value ÷ invested capital", "Simple multiple; ignores time", "Gross (deal) vs. net (to LP)"),
        ("IRR", "r where Σ CFₜ / (1+r)ᵗ = 0", "Time-weighted return", "Gamed by sub-lines and quick flips"),
        ("TVPI", "(Distributions + NAV) ÷ PIC", "Net total multiple", "Includes unrealized NAV"),
        ("DPI", "Distributions ÷ PIC", "Cash-on-cash realized", "What LPs prize in tight markets"),
        ("RVPI", "NAV ÷ PIC", "Unrealized remainder", "TVPI = DPI + RVPI"),
        ("PME", "PE flows vs. an index", "Beat the market on the same timing?", "KS-PME > 1.0x = outperformed")]
for i, (a, f, m, n) in enumerate(mets):
    col, row = i % 3, i // 3
    x = 0.5 + col * 4.15; y = 1.45 + row * 2.0
    rect(s, x, y, 4.0, 1.85, fill=WHITE, line=LINE)
    rect(s, x, y, 1.1, 1.85, fill=NAVY if row == 0 else TEAL)
    txt(s, x, y, 1.1, 1.85, a, size=17, color=WHITE, font=SERIF, align="c", anchor="m")
    txt(s, x + 1.2, y + 0.1, 2.7, 1.7, [[(f, {"font": SERIF, "size": 11, "color": NAVY})], [(m, {"bold": True})], [(n, {"color": MUTED})]], size=9.3, spacing=4)
rect(s, 0.5, 5.5, 6.06, 1.35, fill=PANEL, line=LINE)
txt(s, 0.65, 5.52, 5.8, 1.3, [[("Shortcuts", {"bold": True, "caps": True, "color": NAVY})], "Single-exit IRR = MOIC^(1/T) − 1.  2x in 5 yrs ≈ 14.9%; 3x in 5 yrs ≈ 24.6%; 3x in 7 yrs ≈ 17.0%.", "Gross-to-net spread for buyout is typically 4–7 points (fees, carry, expenses)."], size=9.3, spacing=3)
rect(s, 6.77, 5.5, 6.06, 1.35, fill=WHITE, line=BURG, lw=1)
txt(s, 6.92, 5.52, 5.8, 1.3, [[("Traps", {"bold": True, "caps": True, "color": BURG})], "Subscription lines inflate IRR. MOIC hides time. Interim NAVs are Level 3 judgment marks.", "Always read DPI and PME together before trusting an IRR."], size=9.3, spacing=3)

# ---------------------------------------------------------------- 8 J-CURVE & PME
s = slide("04 | Metrics", "The J-Curve, PME and Quartiles")
band(s, 0.5, 1.45, 6.3, 0.32, "Illustrative cumulative net cash flow to LPs ($M per $100M committed)")
cd = CategoryChartData()
cd.categories = [f"Y{i}" for i in range(11)]
cd.add_series("Cumulative net cash flow", (0, -12, -28, -42, -48, -44, -30, -8, 18, 42, 60))
gf = s.shapes.add_chart(XL_CHART_TYPE.LINE_MARKERS, Inches(0.5), Inches(1.8), Inches(6.3), Inches(3.4), cd)
ch = gf.chart; ch.has_legend = False; ch.has_title = False
ser = ch.plots[0].series[0]; ser.format.line.color.rgb = NAVY; ser.format.line.width = Pt(2.5); ser.smooth = True
ser.marker.format.fill.solid(); ser.marker.format.fill.fore_color.rgb = NAVY
ch.value_axis.tick_labels.font.size = Pt(9); ch.category_axis.tick_labels.font.size = Pt(9)
ch.value_axis.major_gridlines.format.line.color.rgb = LINE
ch.value_axis.format.line.color.rgb = LINE; ch.category_axis.format.line.color.rgb = LINE
from pptx.enum.chart import XL_TICK_LABEL_POSITION
ch.category_axis.tick_label_position = XL_TICK_LABEL_POSITION.LOW
txt(s, 0.5, 5.25, 6.3, 0.6, "Early fees and write-downs push cumulative cash flow negative; value creation and exits turn it up. A subscription line flattens the trough artificially.", size=9.3, color=MUTED)
band(s, 7.0, 1.45, 5.83, 0.32, "KS-PME (Kaplan–Schoar)")
rect(s, 7.0, 1.77, 5.83, 1.75, fill=NAVY)
txt(s, 7.15, 1.82, 5.55, 1.65, [[("Σ Distₜ·(Iₜ/Iₜ) + NAVₜ  ÷  Σ Callₜ·(Iₜ/Iₜ)", {"font": SERIF, "size": 13})],
    "Each flow is compounded at the index return to the measurement date. Single in / out: MOIC ÷ (1 + r_index)^T.",
    [("▸ Leviathan 5-yr Base: 2.068x ÷ 1.09⁵ = 1.34x vs. SPX", {"bold": True, "color": GOLD})]], size=9.5, color=WHITE, spacing=5, anchor="m")
table(s, 7.0, 3.65, 5.83, 2.2, [["Measure", "What it tells you"],
    ["Direct Alpha", "Annualized excess return over the index"],
    ["LN-PME", "IRR from investing the same flows in the index"],
    ["Vintage year", "Compare funds that started together"],
    ["Quartile", "Rank vs. same-vintage peers; dispersion is wide in VC"],
    ["Loss ratio", "% of capital in deals returning < 1.0x"]], col_w=[1.5, 4.3], size=9, align=["l", "l"])
rect(s, 0.5, 6.0, 12.33, 0.85, fill=PANEL, line=LINE)
txt(s, 0.65, 6.0, 12.1, 0.85, [[("Why PME is the honest scoreboard: ", {"bold": True, "color": NAVY}), ("IRR alone can’t tell you whether illiquidity paid. PME asks whether the same cash flows in an index would have done better. ▸ Leviathan benchmarks against a forward 15% ITA/SOXX basket, not just the S&P 500.", {})]], size=10, anchor="m")

# ---------------------------------------------------------------- 9 STRATEGIES
s = slide("05 | Strategies", "Private Market Strategies: Risk, Control and Return Drivers")
table(s, 0.5, 1.45, 12.33, 5.4, [["Strategy", "Profile", "Control / leverage", "Return driver", "Net target", "▸ Example"],
    ["Venture capital", "Pre-profit, power-law outcomes", "Minority, none", "A few outsized winners", "20–30%+", "Mueon, DefendEye"],
    ["Growth equity", "Scaling revenue, near profit", "Minority, little", "Revenue growth", "20–25%", "Quince, Whoop"],
    ["Buyout / LBO", "Mature, cash-generative", "Control, 4–7x debt", "EBITDA, deleveraging, multiple", "15–25%", "—"],
    ["Take-private", "Listed company acquired", "Control", "Re-rating + operations", "15–20%", "—"],
    ["Carve-out / spin-off", "Division bought from parent", "Control or minority", "Standalone efficiency; TSAs", "15–25%", "L3Harris MSL"],
    ["Buy-and-build", "Platform + add-ons", "Control", "Multiple arbitrage", "18–25%", "—"],
    ["Minority / structured", "Preferred with protection", "Minority, structured", "Contractual return + upside", "12–18%", "Ellwood, ARA"],
    ["Pre-IPO / crossover", "Last private round", "Minority", "Discount to IPO", "15–25%", "MSL, IAI, Syntiant"],
    ["PIPE", "Private stake in public co.", "Minority", "Discount + terms", "12–20%", "Infleqtion"],
    ["Secondaries", "LP interests or GP-led CVs", "Passive / varies", "Discount to NAV; short J-curve", "12–18%", "Saronic, Stripe tender"],
    ["Private credit", "Senior loans to sponsor cos.", "Lender", "Floating-rate spread", "9–13%", "—"],
    ["Distressed / special sits", "Stressed balance sheets", "Loan-to-own", "Restructuring", "15–20%", "—"]],
    col_w=[1.9, 2.4, 1.8, 2.5, 1.0, 1.9], size=8.9, align=["l", "l", "l", "l", "c", "l"])

# ---------------------------------------------------------------- 10 DEAL PROCESS
s = slide("06 | Deal process", "The Deal Process: From Sourcing to Closing")
steps = [("Sourcing", "Proprietary or banker-led"), ("NDA", "Confidentiality"), ("Teaser / CIM", "Anonymous summary → full book"), ("IOI", "Non-binding range"),
         ("Mgmt pres. + VDR", "Data room access"), ("LOI", "Price, structure, exclusivity"), ("Confirmatory DD", "QoE, legal, commercial, regulatory"), ("SPA / APA", "Definitive agreement"),
         ("Signing", "Covenants apply"), ("Regulatory", "HSR, CFIUS"), ("Closing", "Funds flow")]
cw = 12.33 / 11
for i, (a, b) in enumerate(steps):
    x = 0.5 + i * cw
    dark = i in (5, 10)
    rect(s, x + 0.02, 1.45, cw - 0.16, 1.15, fill=NAVY if dark else WHITE, line=None if dark else LINE)
    txt(s, x + 0.04, 1.5, cw - 0.2, 1.05, [[(a, {"bold": True})], [(b, {"size": 8, "color": WHITE if dark else MUTED})]], size=8.8, color=WHITE if dark else NAVY, align="c", anchor="m")
    if i < 10: arrow(s, x + cw - 0.13, 1.95, 0.11, 0.1)
table(s, 0.5, 2.8, 7.9, 4.05, [["Term", "Definition"],
    ["Proprietary vs. auction", "Off-market sourcing vs. banker-run competitive rounds"],
    ["QoE", "Accounting diligence that normalizes EBITDA"],
    ["Reps & warranties / RWI", "Seller statements of fact / insurance covering breaches"],
    ["Indemnity & escrow", "Seller’s post-close liability and the cash securing it"],
    ["MAC / MAE", "Material adverse change: walk-away right"],
    ["Locked box vs. completion accounts", "Fixed historical balance sheet vs. post-close true-up"],
    ["Earn-out", "Contingent consideration tied to future performance"],
    ["Rollover equity", "Sellers or management reinvest part of proceeds"],
    ["TSA", "Parent keeps providing services to a carve-out"]], col_w=[2.6, 5.3], size=9, align=["l", "l"])
rect(s, 8.6, 2.8, 4.23, 4.05, fill=PANEL, line=LINE)
txt(s, 8.75, 2.88, 3.95, 3.9, [[("▸ Minority and pre-IPO variant", {"bold": True, "caps": True, "color": TEAL})],
    "Leviathan’s deals are mostly minority stakes, so the process compresses:",
    "• Access via secondary, tender, cornerstone or structured pref replaces the auction.",
    "• Diligence focuses on the cap table, preference stack, transfer restrictions (ROFR) and the contract trail.",
    "• Regulatory review (CFIUS, ITAR, FOCI) can be the critical path for defense names."], size=9.4, spacing=5)

# ---------------------------------------------------------------- 11 VALUATION
s = slide("07 | Valuation", "Valuation: Enterprise Value to Equity Value")
band(s, 0.5, 1.45, 6.6, 0.32, "Illustrative EV → equity bridge ($M)")
bars = [("Enterprise value", 0, 500, NAVY), ("− Debt", 300, 500, BURG), ("− Preferred", 260, 300, BURG), ("− Debt-like items", 240, 260, BURG), ("+ Cash", 240, 290, TEAL), ("Equity value", 0, 290, NAVY)]
base_y, top_y, scale = 5.6, 1.95, 3.5 / 500
bw = 6.6 / 6
for i, (lab, lo, hi, f) in enumerate(bars):
    x = 0.5 + i * bw
    y1 = base_y - hi * scale; h = (hi - lo) * scale
    rect(s, x + 0.15, y1, bw - 0.3, h, fill=f)
    txt(s, x, y1 - 0.28, bw, 0.28, f"{hi - lo:,.0f}" if i not in (0, 5) else f"{hi:,.0f}", size=9.5, bold=True, color=f, align="c")
    txt(s, x, base_y + 0.05, bw, 0.45, lab, size=8.8, color=INK, align="c")
hline(s, 0.5, base_y, 6.6, LINE)
txt(s, 0.5, 6.15, 6.6, 0.7, [[("Equity = EV − Debt − Preferred − Minorities − Debt-like items + Cash", {"font": SERIF, "size": 12, "color": NAVY})]], size=10, align="c", anchor="m")
table(s, 7.3, 1.45, 5.53, 5.4, [["Term", "Definition / ▸ example"],
    ["EBITDA / Adjusted", "Operating cash proxy; adjustments are where sellers inflate"],
    ["EV / EBITDA, EV / EBIT", "Core multiples ▸ LHX 15.1x, RHM 17.3x"],
    ["Trading comps", "Multiples of listed peers"],
    ["Precedent transactions", "M&A multiples incl. control premium"],
    ["DCF", "PV of FCF + terminal value"],
    ["Pre- / post-money", "Post = Pre + new money; Own % = Check ÷ Post ▸ $9M ÷ $92M = 9.8%"],
    ["Fully diluted", "Counts options, warrants, convertibles"],
    ["Down / flat round", "Price below / equal to prior round"],
    ["ASC 820 Level 3", "Model-based fair value for private marks"],
    ["Prob.-weighted EV", "Σ pᵢ × EVᵢ ▸ Faxon 25/50/25 → $91.75M"],
    ["DLOM", "Discount for lack of marketability"]], col_w=[1.8, 3.7], size=8.8, align=["l", "l"])

# ---------------------------------------------------------------- 12 CAPITAL STRUCTURE
s = slide("08 | Capital structure", "The Capital Stack: Seniority, Cost and Control")
stack = [("Revolver (RCF)", "Senior secured · drawable working capital", "SOFR + 2–3%", NAVY),
         ("Term Loan A / B", "Senior secured · TLA amortizes; TLB mostly bullet", "SOFR + 3–4.5%", NAVY),
         ("Unitranche", "Single blended senior loan from a direct lender", "SOFR + 5–7%", NAVY),
         ("Second lien", "Junior secured on same collateral", "SOFR + 6–9%", TEAL),
         ("Mezzanine / PIK", "Subordinated; warrants or interest accruing in kind", "12–15%", TEAL),
         ("Preferred equity", "Senior to common; liquidation preference, dividends", "10–14%", GOLD),
         ("Common equity", "Sponsor + management; residual claim, control", "20%+ target", BURG)]
for i, (a, b, c, f) in enumerate(stack):
    y = 1.5 + i * 0.66
    w = 5.2 + i * 0.25
    rect(s, 0.5, y, w, 0.58, fill=f)
    txt(s, 0.62, y, 2.0, 0.58, [[(a, {"bold": True})]], size=10, color=WHITE, anchor="m")
    txt(s, 2.6, y, w - 3.8, 0.58, b, size=8.6, color=WHITE, anchor="m")
    txt(s, 0.5 + w - 1.25, y, 1.15, 0.58, [[(c, {"bold": True})]], size=9, color=WHITE, align="r", anchor="m")
txt(s, 0.5, 6.15, 3.4, 0.6, [[("▲ Senior: paid first, lowest cost", {"bold": True})], [("▼ Junior: paid last, highest return", {"bold": True})]], size=9, color=NAVY)
txt(s, 3.9, 6.15, 3.3, 0.6, [[("Indicative pricing only — varies with rates and credit quality.", {"italic": True})]], size=8.5, color=MUTED)
table(s, 7.4, 1.5, 5.43, 5.35, [["Term", "Definition"],
    ["Leverage", "Debt ÷ EBITDA (total, senior, net)"],
    ["Interest coverage", "EBITDA ÷ interest"],
    ["FCCR", "(EBITDA − capex − tax) ÷ fixed charges"],
    ["Maintenance covenant", "Tested every quarter"],
    ["Incurrence covenant", "Tested only when taking an action"],
    ["Cov-lite", "No maintenance covenants (common in TLB)"],
    ["Sources & uses", "Where the money comes from and goes"],
    ["Dividend recap", "Borrow to pay sponsor a dividend (DPI, no exit)"],
    ["MIP / sweet equity", "Management equity, often 5–15% of common"]], col_w=[1.8, 3.6], size=9, align=["l", "l"])

# ---------------------------------------------------------------- 13 LBO WORKED
s = slide("08 | Capital structure", "Worked LBO: Entry, Exit and the Value-Creation Bridge")
band(s, 0.5, 1.45, 4.0, 0.32, "Sources & uses at entry ($M)")
table(s, 0.5, 1.77, 4.0, 1.6, [["Uses", "$M", "Sources", "$M"], ["Purchase EV (10x $50M)", "500", "Debt (5.0x)", "250"], ["", "", "Sponsor equity", "250"], [("Total", {"bold": True}), ("500", {"bold": True}), ("Total", {"bold": True}), ("500", {"bold": True})]], col_w=[1.6, 0.5, 1.3, 0.5], size=9, align=["l", "c", "l", "c"])
band(s, 0.5, 3.55, 4.0, 0.32, "Exit in year 5 ($M)")
table(s, 0.5, 3.87, 4.0, 1.6, [["Item", "Value"], ["Exit EBITDA × 10x", "80 × 10 = 800"], ["Less net debt (paid down)", "−120"], [("Equity value", {"bold": True}), ("680", {"bold": True})]], col_w=[2.2, 1.8], size=9.5, align=["l", "c"])
rect(s, 0.5, 5.65, 4.0, 1.2, fill=NAVY)
txt(s, 0.65, 5.68, 3.7, 1.15, [[("MOIC = 680 ÷ 250 = 2.72x", {"font": SERIF, "size": 14})], [("IRR = 2.72^(1/5) − 1 = 22.2%", {"font": SERIF, "size": 14})]], size=10, color=WHITE, anchor="m", spacing=3)
band(s, 4.7, 1.45, 8.13, 0.32, "Equity value-creation bridge ($M)")
br_ = [("Entry equity", 0, 250, NAVY), ("EBITDA growth\n(+30 × 10x)", 250, 550, TEAL), ("Multiple\nexpansion", 550, 550, GREY), ("Debt paydown\n(250 → 120)", 550, 680, TEAL), ("Exit equity", 0, 680, NAVY)]
base_y, scale = 6.2, 4.0 / 700
bw = 8.13 / 5
for i, (lab, lo, hi, f) in enumerate(br_):
    x = 4.7 + i * bw
    h = max((hi - lo) * scale, 0.03)
    rect(s, x + 0.25, base_y - hi * scale, bw - 0.5, h, fill=f)
    v = hi if i in (0, 4) else hi - lo
    txt(s, x, base_y - hi * scale - 0.3, bw, 0.28, f"{v:,.0f}" if v else "0", size=10, bold=True, color=f, align="c")
    txt(s, x, base_y + 0.05, bw, 0.6, lab.split("\n"), size=8.8, align="c")
hline(s, 4.7, base_y, 8.13, LINE)

# ---------------------------------------------------------------- 14 EQUITY TERMS
s = slide("09 | Equity terms", "Equity Terms: The Minority Investor’s Protection Kit")
table(s, 0.5, 1.45, 7.6, 5.4, [["Term", "What it does", "Investor-friendly version"],
    ["Liquidation preference", "Paid before common at exit", "1x non-participating is standard"],
    ["Participating preferred", "Preference back, then shares pro rata", "“Double dip”; often capped (3x)"],
    ["Anti-dilution", "Price protection in down rounds", "Full ratchet > broad-based weighted avg."],
    ["Pro rata right", "Keep ownership % in later rounds", "Essential for follow-on reserves"],
    ["ROFR", "First refusal on share transfers", "Controls who enters the cap table"],
    ["Tag-along (co-sale)", "Sell alongside the majority, same terms", "Core minority protection"],
    ["Drag-along", "Majority can force a sale", "Minority wants a price floor"],
    ["Protective provisions", "Vetoes: new senior stock, sale, debt", "Key minority control"],
    ["Board seat / observer", "Governance or visibility", "▸ Sought at >15% ownership"],
    ["Redemption / put", "Force buyback after N years", "Liquidity in family / ESOP cos."],
    ["IPO ratchet", "Extra shares if IPO prices low", "Pre-IPO protection"],
    ["Warrants / conversion", "Right to buy / convert to common", "▸ DoW warrants & conv. pref at MSL"]],
    col_w=[1.9, 2.9, 2.8], size=8.8, align=["l", "l", "l"])
band(s, 8.3, 1.45, 4.53, 0.32, "Worked example: preference at exit")
txt(s, 8.3, 1.85, 4.53, 0.55, "Investor put in $20M for 20%. Company sells for $60M.", size=9.8, color=INK)
table(s, 8.3, 2.4, 4.53, 1.35, [["Structure", "Investor gets"], ["1x non-participating", "max($20M, 20% × 60) = $20M"], ["1x participating", "$20M + 20% × $40M = $28M"], ["Common only", "20% × $60M = $12M"]], col_w=[1.8, 2.7], size=9.2, align=["l", "l"])
band(s, 8.3, 3.95, 4.53, 0.32, "Dilution & retention", fill=TEAL)
rect(s, 8.3, 4.27, 4.53, 1.45, fill=WHITE, line=LINE)
txt(s, 8.45, 4.32, 4.25, 1.35, ["Own 10%; later rounds sell 15%, 10%, 10%:", [("10% × 0.85 × 0.90 × 0.90 = 6.9%", {"font": SERIF, "size": 12, "color": NAVY})], "Retention = 0.69 ▸ the model uses 0.68 at 10 yrs for IQT names."], size=9.3, spacing=4)
rect(s, 8.3, 5.85, 4.53, 1.0, fill=PANEL, line=LINE)
txt(s, 8.45, 5.85, 4.25, 1.0, [[("Early stage: ", {"bold": True, "color": NAVY}), ("convertible notes and SAFEs convert at the next round with a cap and discount; pay-to-play strips preferences from non-participants.", {})]], size=9, anchor="m")

# ---------------------------------------------------------------- 15 EXITS & VALUE CREATION
s = slide("10 | Exits & value creation", "Exits and Value Creation")
ex = [("Strategic sale", "Corporate buyer pays for synergies", "Highest price; CFIUS limits buyers"), ("Secondary buyout", "Sale to another sponsor", "Common; “pass the parcel”"),
      ("IPO", "Listing, then staged sell-down", "180-day lock-up, greenshoe, cornerstones"), ("Continuation vehicle", "GP-led roll into a new vehicle", "Liquidity for LPs; longer hold"),
      ("Dividend recap", "Partial liquidity through debt", "DPI without change of control"), ("Strip / minority sale", "Sell part of the stake", "Partial DPI")]
for i, (a, b, c) in enumerate(ex):
    col, row = i % 3, i // 3
    x = 0.5 + col * 2.75; y = 1.45 + row * 1.65
    rect(s, x, y, 2.62, 1.52, fill=WHITE, line=LINE)
    rect(s, x, y, 2.62, 0.4, fill=NAVY)
    txt(s, x, y, 2.62, 0.4, [[(a, {"bold": True, "caps": True})]], size=9, color=WHITE, align="c", anchor="m")
    txt(s, x + 0.1, y + 0.48, 2.42, 1.0, [[(b, {"bold": True})], [(c, {"color": MUTED})]], size=9.2, align="c", spacing=3)
rect(s, 0.5, 4.85, 8.12, 2.0, fill=PANEL, line=LINE)
txt(s, 0.65, 4.9, 7.85, 1.9, [[("▸ Exit routes in the Leviathan book", {"bold": True, "caps": True, "color": TEAL})],
    "• IPO: L3Harris MSL (Q1-27 target), IAI attempt, Syntiant (S-1 filed), Whoop (IPO track).",
    "• Strategic: EdgeCortix → Renesas; US sovereign names acquirable by government or primes (CFIUS-clean).",
    "• Secondary / tender: Stripe annual tender; Forge markets for Quince, Farmer’s Dog, Thrive."], size=9.4, spacing=5)
band(s, 8.83, 1.45, 4.0, 0.32, "Value-creation levers", fill=TEAL)
rect(s, 8.83, 1.77, 4.0, 5.08, fill=WHITE, line=LINE)
bullets(s, 8.95, 1.87, 3.78, 4.9, [("100-day plan: ", "management, KPIs, quick wins, reporting"), ("Revenue: ", "pricing, new markets, salesforce"), ("Margin: ", "procurement, footprint, automation"),
    ("Capital efficiency: ", "working capital, capex discipline"), ("M&A: ", "add-ons; buy at 6x, consolidate at 11x"), ("Capital structure: ", "refinancing, recaps"),
    ("Defense-specific: ", "capacity ahead of MYP awards, program qualification, tier-2 → tier-1, FMS approvals, CMMC, facility clearance")], size=9.3, spacing=5)

# ---------------------------------------------------------------- 16 REGULATORY
s = slide("11 | Regulation", "Regulation: Fund-Level Rules and National-Security Gates")
band(s, 0.5, 1.45, 6.06, 0.32, "Fund & investor regulation (US)")
table(s, 0.5, 1.77, 6.06, 5.08, [["Term", "Definition"],
    ["Advisers Act / Form ADV", "Adviser registration and disclosure"],
    ["Accredited investor", "$1M net worth (ex-home) or $200K income"],
    ["Qualified purchaser", "≥ $5M in investments (individuals)"],
    ["3(c)(1) / 3(c)(7)", "≤ 100 beneficial owners / QPs only"],
    ["ERISA 25% test", "Avoid plan-asset status if benefit-plan LPs < 25%"],
    ["UBTI / ECI", "Tax issues for tax-exempt / non-US LPs → blockers"],
    ["IRC §1061", "Carry needs a 3-yr hold for long-term gains"],
    ["QSBS (§1202)", "Gain exclusion on qualifying C-corp stock held 5+ yrs"]], col_w=[2.0, 4.0], size=9, align=["l", "l"])
band(s, 6.77, 1.45, 6.06, 0.32, "National security & defense investing", fill=BURG)
table(s, 6.77, 1.77, 6.06, 5.08, [["Term", "Definition / ▸ relevance"],
    ["CFIUS", "Reviews foreign investment; mandatory for critical tech ▸ exit buyer set"],
    ["TID business", "Critical Tech, Infrastructure or Data: heightened review"],
    ["ITAR / EAR", "Export controls: defense articles / dual-use ▸ IAI"],
    ["FOCI", "Foreign ownership mitigation: SSA, SCA, proxy agreement"],
    ["Facility clearance (FCL)", "Needed for classified work; slow to obtain = moat"],
    ["NDAA §889 / Blue UAS", "Bans on Chinese components ▸ DefendEye diligence"],
    ["CMMC / DFARS 7012", "DoD supplier cybersecurity requirements"],
    ["Outbound investment rules", "US limits on investing in Chinese semis, AI, quantum"]], hdr_fill=BURG, col_w=[2.0, 4.0], size=9, align=["l", "l"])

# ---------------------------------------------------------------- 17 DEFENSE CONTRACTING
s = slide("11 | Regulation", "Defense Contracting Vocabulary for Investors")
txt(s, 0.5, 1.4, 12.33, 0.4, "Budget dollars only become revenue after passing through this chain. Each step is a place a thesis can stall.", size=11.5, align="c")
chain = [("Request", "President’s budget"), ("Authorization", "NDAA sets policy limits"), ("Appropriation", "Money actually funded"), ("Contract vehicle", "IDIQ, MYP, OTA"), ("Task order", "Revenue is created"), ("LRIP → FRP", "Production ramps")]
cw = 12.33 / 6
for i, (a, b) in enumerate(chain):
    x = 0.5 + i * cw
    rect(s, x + 0.03, 1.9, cw - 0.3, 0.8, fill=NAVY if i in (2, 4) else WHITE, line=None if i in (2, 4) else LINE)
    txt(s, x + 0.05, 1.9, cw - 0.34, 0.8, [[(a, {"bold": True})], [(b, {"size": 8.5})]], size=9.8, color=WHITE if i in (2, 4) else NAVY, align="c", anchor="m")
    if i < 5: arrow(s, x + cw - 0.24, 2.23, 0.18, 0.14)
table(s, 0.5, 2.9, 12.33, 3.95, [["Term", "Definition", "Term", "Definition"],
    ["PPBE", "DoD planning, programming, budgeting, execution cycle", "FFP vs. cost-plus", "Contractor bears cost risk (margin upside) vs. cost + fee"],
    ["CR", "Continuing resolution: prior-year levels; no new starts", "FMS vs. DCS", "Gov-to-gov sales via DSCA vs. direct commercial sales"],
    ["Reconciliation", "Budget route for large one-off funding ▸ Golden Dome", "Prime / tier-1 / 2 / 3", "Supply-chain position ▸ Faxon, Ellwood are tier-2/3"],
    ["IDIQ", "Ceiling contract; revenue only from task orders", "Sole source / J&A", "Non-competitive award with justification: a moat"],
    ["MYP", "Congress-approved multiyear buys ▸ Tomahawk, PAC-3", "Recompete", "Re-bid at expiry: revenue cliff ▸ BLU-136/B"],
    ["LRIP / FRP", "Low-rate initial / full-rate production", "OTA", "Fast prototyping outside the FAR (DIU)"],
    ["Black budget", "Classified programs; IC funds NIP / MIP ▸ IQT", "SBIR / STTR I–III", "Small-business R&D; Phase III = production, no re-compete"]],
    col_w=[1.4, 4.4, 1.6, 4.9], size=8.9, align=["l", "l", "l", "l"])

# ---------------------------------------------------------------- 18 FORMULAS & TARGETS
s = slide("12 | Reference", "Formula Cheat Sheet and Return Targets")
table(s, 0.5, 1.45, 7.4, 5.4, [["Item", "Formula"],
    ["Ownership", "Check ÷ Post-money"], ["Post-money", "Pre-money + New money"], ["Single-exit IRR", "MOIC^(1/T) − 1"],
    ["TVPI", "DPI + RVPI"], ["KS-PME (single flow)", "MOIC ÷ (1 + index return)^T"], ["Compounded pref", "Capital × [(1 + h)^T − 1]"],
    ["Full catch-up", "Pref × carry ÷ (1 − carry)"], ["Equity value", "EV − net debt − preferred − minorities − debt-like"],
    ["Value bridge", "ΔEBITDA × entry multiple + Δmultiple × exit EBITDA + debt paydown"], ["Retention", "Π (1 − dilution per round)"],
    [("▸ Leviathan proceeds", {"bold": True, "color": TEAL}), "Check × (1 + CAGR)^Hold × Retention"],
    [("▸ Shock CAGR", {"bold": True, "color": TEAL}), "Base CAGR + (Composite − 2.5) × 8%"],
    [("▸ Pre-IPO entry", {"bold": True, "color": TEAL}), "Fwd EBIT × IPO multiple × (1 − discount)"]], col_w=[2.2, 5.2], size=9.2, align=["l", "l"])
band(s, 8.1, 1.45, 4.73, 0.32, "Rule-of-thumb net targets")
table(s, 8.1, 1.77, 4.73, 3.6, [["Strategy", "Net IRR", "Net MOIC"],
    ["Large buyout", "15–20%", "1.8–2.2x"], ["Mid-market buyout", "18–25%", "2.0–2.5x"], ["Growth equity", "20–25%", "2.5–3.0x"],
    ["Venture (fund)", "20–30%+", "3.0x+"], ["Secondaries", "12–18%", "1.5–1.8x"], ["Private credit", "9–13%", "1.3–1.5x"],
    [("▸ Leviathan 7-yr Exp.", {"bold": True, "color": NAVY}), ("19.4%", {"bold": True}), ("3.46x", {"bold": True})]], col_w=[2.1, 1.3, 1.3], size=9.2)
rect(s, 8.1, 5.5, 4.73, 1.35, fill=NAVY)
txt(s, 8.25, 5.52, 4.45, 1.3, [[("Rule of 72", {"caps": True, "bold": True, "color": GOLD, "size": 9})], [("Years to double ≈ 72 ÷ IRR%", {"font": SERIF, "size": 14})], "15% doubles in ~4.8 yrs; 24% triples in ~5 yrs."], size=9.5, color=WHITE, spacing=3, anchor="m")

stamp_pages(p)
p.save(OUT)
print("saved", OUT, len(p.slides), "slides")
