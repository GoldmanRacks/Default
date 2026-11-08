"""Builds guides/D.B._Ritts_III_PE_Investment_Profile.pptx (regenerated Guide #1 in profile-deck format)."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from pptkit import *

OUT = os.path.join(os.path.dirname(__file__), "..", "guides", "D.B._Ritts_III_PE_Investment_Profile.pptx")
p = new_deck()
N = [0]

def slide(section, title, ts=30):
    s = blank(p); N[0] += 1
    header(s, section, title, ts)
    return s

# ---------------------------------------------------------------- 1 COVER
s = blank(p); N[0] += 1
txt(s, 0.5, 0.45, 12.3, 0.8, "D. B. Ritts III — Private Equity Investment Profile", size=34, color=NAVY, font=SERIF)
rect(s, 0.5, 1.3, 12.33, 0.012, fill=LINE)
txt(s, 0.5, 1.42, 12, 0.3, [[("How I research & select investment targets  \u00b7  Selection lenses  \u00b7  Case studies  \u00b7  Leviathan holdco", {"caps": True, "track": 150})]], size=10.5, color=MUTED)
rect(s, 0.5, 1.95, 4.1, 4.8, fill=NAVY)
txt(s, 0.8, 2.15, 3.6, 1.6, "Executive Assessment: a research-led selector of constrained, multi-engine assets", size=20, color=WHITE, font=SERIF, line_spacing=1.05)
rect(s, 0.8, 3.85, 0.6, 0.02, fill=GOLD)
txt(s, 0.8, 4.0, 3.6, 1.2, "Selects targets pulled by more than one secular demand curve \u2014 national security and the AI boom, or a TAM that spans every demographic \u2014 then owns the scarce asset privately.", size=11, color=WHITE)
rect(s, 0.8, 5.15, 3.5, 0.01, fill=RGBColor(0x55, 0x66, 0x88))
txt(s, 0.8, 5.3, 3.6, 1.3, "Underwrites contracts, not narratives: program-level revenue builds, four-scenario returns, and a thematic-ETF hurdle (KS-PME) as the scoreboard.", size=11, color=WHITE)
rect(s, 4.85, 1.95, 7.98, 1.55, fill=PANEL, line=LINE)
txt(s, 5.0, 1.95, 0.6, 0.8, "“", size=54, color=NAVY, font=SERIF)
txt(s, 5.6, 2.1, 6.6, 1.3, "Follow the macro shift down through budgets, programs and production lines until you find the constraint that has to be paid — then own it privately, at an entry price the public market will not offer twice.", size=15, color=NAVY, font=SERIF, italic=True)
band(s, 4.85, 3.65, 7.98, 0.32, "Target research & selection architecture")
steps = [("1. Demand engines", "How many secular curves pull on it? How wide is the TAM?"), ("2. Constraint / moat", "What can\u2019t the market route around?"), ("3. Evidence", "Contracts, filings, priced marks over narrative"), ("4. Underwrite", "Program / unit build; 4 scenarios; KS-PME hurdle"), ("5. Entry & access", "Real price, real route in, right structure")]
cw = 7.98 / 5
for i, (a, b) in enumerate(steps):
    x = 4.85 + i * cw
    rect(s, x, 3.97, cw, 1.55, fill=WHITE, line=LINE)
    num(s, x + cw / 2 - 0.16, 4.07, i + 1)
    txt(s, x + 0.05, 4.45, cw - 0.1, 0.35, [[(a[3:], {"caps": True, "bold": True})]], size=9, color=NAVY, align="c")
    txt(s, x + 0.08, 4.8, cw - 0.16, 0.7, b, size=9, color=MUTED, align="c")
rect(s, 4.85, 5.65, 7.98, 1.1, fill=PANEL, line=LINE)
txt(s, 5.0, 5.7, 1.9, 1.0, [[("Vehicle", {"caps": True, "bold": True})], "Leviathan Core PE Holdco"], size=10, color=NAVY, anchor="m")
bullets(s, 7.0, 5.72, 5.7, 1.0, [("$855M tripartite holdco: ", "IQT-mirror $250M · Weapons $405M · Consumer/Value $200M · 29 positions."),
                                ("7-yr Expected: ", "19.4% net IRR · 3.46x net MOIC · 1.30x KS-PME vs Defense+Semis basket."),
                                ("Holds: ", "5 / 7 / 10-yr vehicles; 2% / 8% pref / 20% carry, European waterfall.")], size=9.5)
txt(s, 0.5, 7.05, 6, 0.25, FOOTER, size=8, color=GREY)

# ---------------------------------------------------------------- 2 DEFINING CHARACTERISTIC
s = slide("01 | PE philosophy", "The Defining Characteristic: Decomposing Macro Into Constraint")
txt(s, 0.5, 1.4, 12.33, 0.55, [[("We do not buy the theme. ", {"bold": True}), ("We decompose a macro event into the physical, financial, technological and institutional constraints that must clear before spending becomes fielded output — and buy the constraint.", {})]], size=12, align="c", color=INK)
for j, (hd, rows, out, fill) in enumerate([
    ("Conventional PE / growth investor", [("Observation", "Defense spending is rising."), ("Inference", "Defense tech will benefit."), ("Action", "Chase the hot late-stage name at a marked-up round.")],
     "Crowded rounds, price set by momentum, exposure to whoever wins the narrative.", GREY),
    ("D. B. Ritts III approach", [("Observation", "Munitions & interceptor budgets are rising."), ("Question", "What physically prevents output?"), ("Decompose", "Trace motors, forgings, energetics, case machining."), ("Own", "Private stakes in the chokepoint at contract-derived prices.")],
     "Early access to bottlenecks; revenue visible in contract awards; few competing bidders.", NAVY)]):
    x = 0.5 + j * 6.4
    band(s, x, 2.05, 5.93, 0.32, hd, fill=fill)
    rect(s, x, 2.37, 5.93, 1.75, fill=WHITE, line=LINE)
    for i, (a, b) in enumerate(rows):
        num(s, x + 0.12, 2.47 + i * 0.4, i + 1, d=0.26, size=9, fill=fill)
        txt(s, x + 0.45, 2.45 + i * 0.4, 3.4, 0.4, [[(a, {"bold": True, "caps": True, "size": 8.5, "color": NAVY})], b], size=9)
    rect(s, x + 3.95, 2.5, 0.01, 1.5, fill=LINE)
    txt(s, x + 4.05, 2.55, 1.8, 1.5, [[("Outcome", {"bold": True, "caps": True, "size": 8.5, "color": NAVY})], out], size=9)
txt(s, 6.43, 2.9, 0.5, 0.5, "VS.", size=14, color=NAVY, font=SERIF, align="c")
band(s, 0.5, 4.25, 12.33, 0.3, "Example: munitions & interceptor demand is rising — what prevents it from becoming output?", fill=WHITE, color=NAVY)
cons = [("Macro event", "NATO 5% · Tomahawk MYP 1,000+/yr · PAC-3 600→2,000/yr", True),
        ("Physical", "Forging, deep-hole machining and SRM casting capacity", False),
        ("Technological", "Energetics chemistry, propellant & warhead-case know-how", False),
        ("Financial", "Long cycles, FFP risk, capex ahead of awards", False),
        ("Institutional", "ITAR, clearances, sole-source qualification, recompetes", False),
        ("Output enabled", "Only when these clear does spend convert to fielded weapons", False)]
cw = 12.33 / 6
for i, (a, b, dark) in enumerate(cons):
    x = 0.5 + i * cw
    rect(s, x + 0.04, 4.62, cw - 0.3, 1.05, fill=NAVY if dark else WHITE, line=None if dark else LINE)
    txt(s, x + 0.1, 4.66, cw - 0.42, 1.0, [[(a, {"bold": True, "caps": True, "size": 8.5})], b], size=8.8, color=WHITE if dark else INK)
    if i < 5:
        arrow(s, x + cw - 0.24, 5.06, 0.18, 0.14)
rect(s, 0.5, 5.77, 12.33, 0.42, fill=PANEL, line=LINE)
txt(s, 0.6, 5.77, 2.0, 0.42, [[("Chokepoints → targets", {"bold": True, "caps": True})]], size=8.5, color=NAVY, anchor="m")
txt(s, 2.6, 5.77, 10.2, 0.42, "Solid-rocket motors (L3Harris MSL)  ·  Energetics (Helicon)  ·  Missile-casing forgings (Ellwood, Superior & Grand Valley)  ·  Warhead-case machining (Faxon)  ·  EUV metrology & substrates (EUV Tech, ThinTronics)", size=9.5, anchor="m")
rect(s, 0.5, 6.3, 12.33, 0.55, fill=WHITE, line=NAVY, lw=1)
arrow(s, 0.65, 6.49, 0.3, 0.18)
txt(s, 1.1, 6.3, 11.6, 0.55, [[("Insight drives ownership. ", {"bold": True, "color": NAVY}), ("Decomposition finds the scarce, mission-critical enablers — usually private, family-held or buried inside a parent — where moats are physical and returns compound.", {})]], size=10.5, anchor="m")

# ---------------------------------------------------------------- 3 SELECTION CHAIN
s = slide("02 | Investment process", "PE Selection Chain: Macro → Mechanism → Constraint → Beneficiary → Structure", 26)
rows = [("1. Structural observation", 0.95), ("2. Central question", 0.6), ("3. Analytical chain", 1.75), ("4. Disciplined through-line", 1.25)]
y = 1.45
fills = [NAVY, NAVY, NAVY, TEAL]
ys = []
for (lab, h), f in zip(rows, fills):
    rect(s, 0.5, y, 1.75, h, fill=f)
    txt(s, 0.58, y, 1.6, h, [[(lab, {"caps": True, "bold": True})]], size=9.5, color=WHITE, anchor="m")
    rect(s, 2.35, y, 10.48, h, fill=WHITE, line=LINE)
    ys.append((y, h)); y += h + 0.12
obs = ["Geopolitical confrontation", "Western rearmament", "AI / semi race", "Taiwan / TSMC tail", "Black-budget growth", "CHIPS / reshoring", "Golden Dome", "Rates & exit windows"]
cw = 10.48 / 8
for i, o in enumerate(obs):
    txt(s, 2.35 + i * cw, ys[0][0] + 0.1, cw, 0.75, [[(f"{i+1:02d}", {"bold": True, "color": GOLD, "size": 11})], o], size=9, align="c", color=NAVY)
y0, h0 = ys[1]
num(s, 2.5, y0 + 0.14, "?", d=0.32)
txt(s, 2.95, y0, 9.8, h0, [[("What must physically, financially and contractually happen for this thesis to produce cash — and who gets paid along the way?", {"bold": True, "color": NAVY})]], size=11, anchor="m")
chain = [("Geopolitics", "Durable pressure"), ("Policy", "NDAA, export rules"), ("Appropriations", "Money actually funded"), ("Programs", "MYP, IDIQ, LRIP"),
         ("Production targets", "Rounds/yr ramps"), ("Capacity", "Labor, tooling, plants"), ("Bottleneck", "Binding constraint"), ("Supplier", "Who gates throughput"),
         ("Ownership", "Private, family, ESOP, parent"), ("Entry structure", "Primary, secondary, pref, pre-IPO"), ("Catalyst", "Award, IPO, recompete"), ("Payoff", "Implied CAGR vs KS-PME")]
y0, h0 = ys[2]
cw = 10.48 / 12
for i, (a, b) in enumerate(chain):
    x = 2.35 + i * cw
    num(s, x + cw / 2 - 0.13, y0 + 0.1, i + 1, d=0.26, size=8.5)
    txt(s, x + 0.02, y0 + 0.42, cw - 0.04, 0.5, [[(a, {"bold": True})]], size=8.3, color=NAVY, align="c")
    txt(s, x + 0.02, y0 + 0.9, cw - 0.04, 0.8, b, size=8, color=MUTED, align="c")
    if i < 11:
        arrow(s, x + cw - 0.07, y0 + 0.18, 0.12, 0.1)
y0, h0 = ys[3]
tl = [("Evidence-based", ["Contracts & filings over commentary", "Marks confirmed by cap-table access"]),
      ("Physics first", ["Capacity & qualification are the moat", "Separate must-haves from nice-to-haves"]),
      ("Risk-aware", ["Bear case is a capital-loss case", "Sizing — not thesis — protects"]),
      ("Time arbitrage", ["Private entry before public re-rate", "Own the backlog, not the headline"]),
      ("Capital discipline", ["Trim to fund substitutes", "New money only for new exposure"])]
cw = 10.48 / 5
for i, (a, bl) in enumerate(tl):
    x = 2.35 + i * cw
    txt(s, x + 0.12, y0 + 0.08, cw - 0.2, 0.3, [[(a, {"caps": True, "bold": True})]], size=9, color=TEAL)
    bullets(s, x + 0.12, y0 + 0.38, cw - 0.2, 0.85, bl, size=8.8)

# ---------------------------------------------------------------- 4 SECOND ORDER
s = slide("03 | PE philosophy", "The Core Edge: Second- and Third-Order Thinking Applied to Private Markets", 27)
band(s, 0.5, 1.45, 4.6, 0.5, "First-order (consensus) — the obvious deal")
band(s, 5.4, 1.45, 7.43, 0.5, "Second / third-order (non-consensus) — what happens after everyone does the obvious deal?")
rowsx = [("Defense budgets rise.", "Buy the hottest defense-tech unicorn", "Throughput is set by tier-2/3 suppliers — motors, forgings, energetics, case machining — not by software primes.",
          "Own the constraints", ["Solid-rocket motors — MSL pre-IPO", "Energetics — Helicon (27% stake)", "Forgings & machining — Ellwood, Faxon"]),
         ("AI race with China intensifies.", "Buy late-stage AI at peak marks", "If Taiwan is contested, the scarce asset is the domestic fail-safe stack: litho, metrology, substrates, packaging.",
          "Own the fail-safe stack", ["X-ray litho — Substrate (anchor)", "EUV metrology — EUV Tech", "ABF substrates — ThinTronics (+CHIPS LOI)"]),
         ("Intelligence budget grows.", "Ignore — it is classified", "IQT is funded inside the NIP: a +14% IC budget means a larger, earlier, government-validated deal pipeline to mirror.",
          "Mirror the smart money", ["Nine IQT-backed names, sized by wartime function", "Denied-environment edge AI", "Post-Moore compute optionality"])]
for i, (obs, buy, ins, own, bl) in enumerate(rowsx):
    y = 2.05 + i * 1.45
    rect(s, 0.5, y, 4.6, 1.35, fill=WHITE, line=LINE)
    txt(s, 0.65, y + 0.2, 2.2, 1.0, [[(obs, {"bold": True})], [("Do the obvious.", {"color": MUTED})]], size=10.5)
    arrow(s, 2.85, y + 0.6, 0.25, 0.16)
    rect(s, 3.2, y + 0.25, 1.75, 0.85, fill=PALE)
    txt(s, 3.25, y + 0.25, 1.65, 0.85, [[(buy, {"caps": True, "bold": True})]], size=8.5, color=NAVY, align="c", anchor="m")
    arrow(s, 5.12, y + 0.6, 0.25, 0.16)
    rect(s, 5.4, y, 7.43, 1.35, fill=WHITE, line=LINE)
    txt(s, 5.5, y + 0.15, 0.5, 1.0, str(i + 1), size=32, color=NAVY, font=SERIF)
    txt(s, 6.0, y + 0.15, 3.3, 1.1, ins, size=9.5)
    txt(s, 9.45, y + 0.1, 3.3, 0.3, [[("▶  " + own, {"caps": True, "bold": True})]], size=9, color=TEAL)
    bullets(s, 9.5, y + 0.42, 3.3, 0.9, bl, size=9)
rect(s, 0.5, 6.4, 12.33, 0.5, fill=NAVY)
txt(s, 0.7, 6.4, 12, 0.5, [[("The edge is systems thinking applied to private capital: ", {"bold": True}), ("stop where others stop at the obvious, then go two layers down the supply chain to where the rent accrues.", {})]], size=11, color=WHITE, anchor="m")

# ---------------------------------------------------------------- 5 WHERE RENT ACCRUES
s = slide("04 | Private-market edge", "Public vs. Private: Where the Rent Accrues and Why the Scoreboard Is KS-PME")
band(s, 0.5, 1.45, 3.6, 0.32, "Key conclusion")
rect(s, 0.5, 1.77, 3.6, 2.6, fill=PANEL, line=LINE)
txt(s, 0.65, 1.9, 3.3, 1.2, "The theme is already priced publicly. The entry point is the alpha.", size=16, color=NAVY, font=SERIF, align="c")
txt(s, 0.65, 3.1, 3.3, 1.2, "ITA +29% and SOXX +170% (1-yr to Jun-26). Rheinmetall at 17x EBITDA. Buying the theme in public markets is beta; capturing it at private / pre-IPO entry is what we are paid for.", size=9.5, align="c", color=INK)
band(s, 4.3, 1.45, 4.5, 0.32, "Benchmarks & hurdle (forward, tempered)")
table(s, 4.3, 1.77, 4.5, 1.6, [["Benchmark", "Fwd CAGR", "Role"], ["S&P 500 (SPX)", "9%", "Floor"], ["Nasdaq-100 (NDX)", "13%", "Growth floor"], [("ITA/SOXX 50/50 basket", {"bold": True, "color": NAVY}), ("15%", {"bold": True}), ("Real hurdle", {"bold": True})]], col_w=[2.2, 1, 1.3], size=9.5)
txt(s, 4.3, 3.45, 4.5, 0.9, "Trailing 5-yr basket ≈ 26% (inflated by the AI + rearmament run) — deliberately not used. KS-PME > 1.0x = beat owning the ETF on identical cash-flow timing.", size=9, color=MUTED)
band(s, 9.0, 1.45, 3.83, 0.32, "The CIO question")
rect(s, 9.0, 1.77, 3.83, 2.6, fill=PANEL, line=LINE)
txt(s, 9.15, 1.9, 3.5, 0.6, "Not “what’s the hot deal?”", size=14, color=NAVY, font=SERIF, align="c")
txt(s, 9.15, 2.5, 3.5, 1.8, "“Where does the economic rent actually accrue, what ownership structure gives me access to it, and does it beat the thematic ETF after fees?”", size=12, color=NAVY, font=SERIF, italic=True, align="c")
band(s, 0.5, 4.55, 12.33, 0.3, "Implication: eight PE access routes to the rent", fill=WHITE, color=NAVY)
routes = [("Direct minority stakes", "Significant minority (>15%) with board seat", "EUV Tech, ThinTronics, Helicon"),
          ("Structured preferred", "Downside-protected pref in family-owned industrials", "Ellwood Group"),
          ("Pre-IPO / cornerstone", "Discount to expected IPO value", "L3Harris MSL, IAI"),
          ("Carve-out stakes", "Segments spun from a parent", "MSL (>80% retained)"),
          ("Secondaries", "Late-stage via Forge / blocks", "Saronic, Quince, Whoop"),
          ("ESOP / closely held", "Structural access others skip", "ARA, Heckler & Koch"),
          ("PIPE / listed small-cap", "Liquid benchmark & DPI", "Infleqtion"),
          ("Seed optionality", "Milestone-gated small checks", "Mueon, DefendEye")]
cw = 12.33 / 8
for i, (a, b, c) in enumerate(routes):
    x = 0.5 + i * cw
    rect(s, x + 0.03, 4.92, cw - 0.06, 0.45, fill=NAVY)
    txt(s, x + 0.03, 4.92, cw - 0.06, 0.45, [[(f"{i+1}  {a}", {"bold": True, "caps": True})]], size=8, color=WHITE, align="c", anchor="m")
    rect(s, x + 0.03, 5.37, cw - 0.06, 1.5, fill=PANEL, line=LINE)
    txt(s, x + 0.08, 5.45, cw - 0.16, 0.8, b, size=8.8, align="c")
    txt(s, x + 0.08, 6.25, cw - 0.16, 0.55, [[(c, {"italic": True, "color": TEAL})]], size=8.5, align="c")

# ---------------------------------------------------------------- 6 PORTFOLIO ARCHITECTURE
s = slide("05 | Portfolio architecture", "Portfolio Architecture: A Barbell With a Ballast")
band(s, 0.5, 1.45, 4.0, 0.55, "Not a diversified PE book — a role-based holdco", size=9.5)
rect(s, 0.5, 2.0, 4.0, 4.85, fill=WHITE, line=LINE)
txt(s, 0.7, 2.1, 3.6, 0.9, "Every target must fill a role. A good company that fills no role is a pass.", size=11, color=NAVY, font=SERIF, align="c")
why = [("Two legs, one supercycle", "IQT = capex leg (build the domestic stack); Weapons = opex leg (consume munitions)."),
       ("Convex to the tail", "Both legs re-rate in a Taiwan/TSMC shock — the book is net long the scenario it hedges."),
       ("Uncorrelated ballast", "Consumer carries near-term DPI; the only sleeve hurt in the shock — by design."),
       ("Sizing is the protection", "Bear case loses capital (net MOIC < 1.0x); position caps, not thesis, limit damage."),
       ("Function-based clusters", "IQT names grouped by wartime function, not SIC code.")]
for i, (a, b) in enumerate(why):
    y = 3.0 + i * 0.75
    num(s, 0.7, y + 0.05, i + 1, d=0.28, size=9)
    txt(s, 1.1, y, 3.3, 0.75, [[(a, {"bold": True, "caps": True, "size": 8.5, "color": NAVY})], b], size=9)
table(s, 4.7, 1.45, 8.13, 2.35, [
    ["Sleeve", "Size", "Return driver", "Duration", "Role", "TSMC-Shock"],
    ["IQT-mirror (deep tech)", "$250M · 29%", "Onshoring capex, sovereign compute", "Longest", "Convex optionality / tail hedge", ("++ convex", {"color": TEAL, "bold": True})],
    ["Weapons (physical layer)", "$405M · 47%", "Defense opex: budgets, replenishment", "Medium", "Cash-generating core", ("++ demand", {"color": TEAL, "bold": True})],
    ["Consumer / Value", "$200M · 23%", "Consumer cycle, DTC & wellness", "Shortest", "Ballast & DPI engine", ("− inflation", {"color": BURG, "bold": True})],
    [("Holdco", {"bold": True, "color": NAVY}), ("$855M · 29 pos.", {"bold": True}), "", "", "", ("Net long shock", {"bold": True})]],
    col_w=[1.9, 1.2, 2.2, 0.9, 1.9, 1.1], size=9)
band(s, 4.7, 3.95, 8.13, 0.32, "IQT sleeve sized by wartime function")
table(s, 4.7, 4.27, 8.13, 1.9, [
    ["Cluster", "Holdings", "% sleeve", "Avg score", "Why it exists"],
    ["TSMC-alternative packaging & substrates", "Substrate, ThinTronics, EUV Tech", "53%", "4.62", "Build & package chips if Taiwan is blockaded"],
    ["Denied-environment edge AI", "Syntiant, EdgeCortix", "25%", "3.03", "On-board AI when GPS/cloud/comms are jammed"],
    ["Post-Moore next-gen compute", "Infleqtion, Diraq, Mueon", "20%", "3.47", "Quantum & dense compute hedge"],
    ["Autonomous sensing (adjacent)", "DefendEye", "3%", "1.70", "Optionality"]],
    col_w=[2.3, 2.0, 0.8, 0.8, 2.6], size=8.8)
rect(s, 4.7, 6.3, 8.13, 0.55, fill=PANEL, line=LINE)
txt(s, 4.85, 6.3, 7.9, 0.55, [[("Weapons: ", {"bold": True, "color": NAVY}), ("Saronic, Epirus, IAI, Elta, Heckler & Koch, Helicon, Ellwood, Superior & Grand Valley, ARA, Faxon, L3Harris MSL.  ", {}), ("Consumer: ", {"bold": True, "color": NAVY}), ("Quince, Thrive, Farmer’s Dog, Whoop, Plunge, Made In, Polymarket, GOAT, Stripe.", {})]], size=8.8, anchor="m")

# ---------------------------------------------------------------- 7 THESIS DRIVERS
s = slide("06 | Thesis engine", "The Thesis Engine: No Dollar Flow, No Thesis")
txt(s, 0.5, 1.4, 12.33, 0.4, "A theme is owned only if I can name the dollar flow behind it and its direction of impact on each sleeve.", size=12, color=INK, align="c")
G, R = ("++", {"color": TEAL, "bold": True}), ("−", {"color": BURG, "bold": True})
def d(v):
    if v.startswith("++"): return (v, {"color": TEAL, "bold": True})
    if v.startswith("+"): return (v, {"color": TEAL})
    if v.startswith("−"): return (v, {"color": BURG, "bold": True})
    return (v, {"color": MUTED})
data = [["Driver", "Evidence anchored on", "IQT", "Weapons", "Consumer"]]
for a, b, c1, c2, c3 in [
    ("NATO / EU rearmament", "Hague 5%-of-GDP (3.5% core + 1.5%) to 2035; EU + Canada +20% in 2025; Rheinmetall +40%/yr", "+", "++", "0"),
    ("US munitions & missiles", "Tomahawk MYP to 1,000+/yr; PAC-3 600→2,000/yr; THAAD 96→400/yr; PrSM ~4x FY27", "+", "++", "0"),
    ("Classified / black budget", "~$170–215B FY26 (16–20% of topline, rising); IC budget +14.2% YoY — IQT funded inside NIP", "++", "++", "0"),
    ("China modernization / decoupling", "PLA budget ~+7%/yr; export controls; entity-list expansion", "++", "+", "−"),
    ("Taiwan / TSMC shock", "‘Davidson window’ (2027); TSMC leading edge = single point of failure", "++ convex", "++", "−"),
    ("CHIPS / reshoring capital", "CHIPS LOIs (ThinTronics $50M, Jul-26); allied industrial policy", "++", "+", "0"),
    ("Golden Dome", "FY27 request $17.5B — only $398M base budget, rest reconciliation-dependent", "+", "++", "0"),
    ("Higher-for-longer rates", "Compresses long-duration terminal multiples; delays exits (DPI timing)", "−", "− / 0", "−"),
    ("USD strength / inflation", "Hits import- and hardware-exposed consumer names", "0", "0", "−−")]:
    data.append([a, (b, {"size": 8.8}), d(c1), d(c2), d(c3)])
table(s, 0.5, 1.9, 8.3, 4.95, data, col_w=[2.0, 4.3, 0.6, 0.85, 0.9], size=9, align=["l", "l", "c", "c", "c"])
band(s, 9.0, 1.9, 3.83, 0.32, "Second-order reads")
rect(s, 9.0, 2.22, 3.83, 4.63, fill=PANEL, line=LINE)
so = [("Edge scales with the black budget", "Bigger IC budget → bigger IQT pipeline → more government-validated signal to mirror. An independent second driver."),
      ("Backlog cushions the Bear case", "Multiyear procurement contracts mean munitions exposure still adds CAGR in Bear (+0.4% per point)."),
      ("Rates are a timing risk, not a thesis risk", "They mostly move IQT exit timing and DPI, not fundamentals."),
      ("Requests ≠ appropriations", "Golden Dome and CR risk: haircut drivers; never let Bull assumptions leak into Base.")]
for i, (a, b) in enumerate(so):
    txt(s, 9.15, 2.32 + i * 1.12, 3.55, 1.1, [[(a, {"bold": True, "color": NAVY})], b], size=9.3)

# ---------------------------------------------------------------- 8 SOURCING
s = slide("07 | Sourcing", "Sourcing: Seven Lenses for Finding Constrained Private Assets")
lenses = [("Mirror sovereign smart money", "IQT, DIU, DARPA, AFWERX and CHIPS awards are free diligence: the government has already validated strategic value.", "Nine IQT names"),
          ("Physical-layer chokepoints", "Forgings, energetics, case machining, SRMs — requalifying a supplier takes years; capacity is the moat.", "Ellwood, Helicon, Faxon"),
          ("Follow the contract trail", "FPDS/SAM awards, IDIQ awardee lists, MYP announcements, sources-sought notices.", "$473M BLU-136/B award"),
          ("Pre-IPO & carve-outs", "Parents taking segments public; cornerstone entry at a discount to IPO value.", "L3Harris MSL"),
          ("Hard-to-access ownership", "Family-owned, ESOP, closely held listed. Few bidders = structural price edge.", "Ellwood, ARA, H&K"),
          ("Allied strategics with events", "IPO attempts and subsidiary consolidations in allied defense champions.", "IAI, Elta"),
          ("Secondary markets for marks", "Forge and block trades give market-priced marks for late-stage names.", "Quince, Whoop")]
for i, (a, b, c) in enumerate(lenses):
    col, row = i % 4, i // 4
    x = 0.5 + col * 3.1; y = 1.5 + row * 2.6
    rect(s, x, y, 2.95, 2.45, fill=WHITE, line=LINE)
    rect(s, x, y, 0.08, 2.45, fill=NAVY)
    txt(s, x + 0.2, y + 0.1, 0.6, 0.6, str(i + 1), size=28, color=NAVY, font=SERIF)
    txt(s, x + 0.75, y + 0.15, 2.1, 0.6, [[(a, {"bold": True, "caps": True})]], size=9.5, color=NAVY, anchor="m")
    txt(s, x + 0.2, y + 0.85, 2.65, 1.1, b, size=9.5)
    rect(s, x + 0.2, y + 1.95, 2.6, 0.35, fill=PALE)
    txt(s, x + 0.2, y + 1.95, 2.6, 0.35, [[("e.g. " + c, {"italic": True})]], size=9, color=TEAL, align="c", anchor="m")
x, y = 0.5 + 3 * 3.1, 1.5 + 2.6
rect(s, x, y, 2.95, 2.45, fill=NAVY)
txt(s, x + 0.2, y + 0.2, 2.6, 2.1, [[("Sourcing rule", {"caps": True, "bold": True, "size": 9, "color": GOLD})],
    [("Start from the constraint, then find who owns it.", {"font": SERIF, "size": 15})],
    [("Never start from a banker’s CIM and work backward to a thesis.", {"size": 9.5})]], size=12, color=WHITE, spacing=6)

# ---------------------------------------------------------------- 9 EVIDENCE HIERARCHY
s = slide("08 | Research methodology", "Underwriting Evidence: A Weighted Hierarchy for Private Targets")
txt(s, 0.5, 1.5, 3.4, 1.4, "We underwrite compelled disclosures and contracts over data-vendor estimates and narrative.", size=15, color=NAVY, font=SERIF)
rect(s, 0.5, 2.95, 0.6, 0.02, fill=NAVY)
txt(s, 0.5, 3.05, 3.4, 1.6, "Private targets have no 10-K. Revenue is rebuilt from what governments are legally required to publish — awards, ceilings, periods of performance — and confirmed through cap-table and management access.", size=9.8)
rect(s, 0.5, 4.75, 3.4, 2.1, fill=PANEL, line=LINE)
txt(s, 0.65, 4.82, 3.15, 2.0, [[("Case in point — Faxon", {"bold": True, "caps": True, "color": NAVY})],
    "Aggregator revenue: ~$21M. Contract-derived FY26E: $60M (BLU-136/B $473M award, LPWC IDIQ, MOP, NGP, TLAM). The aggregator was stale; the contract trail set the entry price.",
    [("Objective: ", {"bold": True}), ("not to prove the thesis — to find what deserves capital.", {})]], size=9.3, spacing=4)
data = [["Tier", "Description", "Typical sources", "Weight"],
        [("Tier 1 — Primary", {"bold": True, "color": NAVY}), "Compelled, verifiable; the foundation", "Appropriations, FPDS awards, IDIQ ceilings, MYP notices, S-1s, priced rounds, cap tables", ("60%", {"bold": True, "size": 14, "color": NAVY})],
        [("Tier 2 — Industry", {"bold": True, "color": TEAL}), "Operational inputs on scale, timing, feasibility", "Management, prime supplier disclosures, production rates, capacity data", ("25%", {"bold": True, "size": 14, "color": TEAL})],
        [("Tier 3 — Market", {"bold": True, "color": MUTED}), "Pricing & sentiment; timing", "Secondary prints (Forge), public comps (LHX, RHM, AVAV), sell-side", ("10%", {"bold": True, "size": 14, "color": MUTED})],
        [("Tier 4 — Narrative", {"bold": True, "color": BURG}), "Lowest reliability; never alone", "Aggregator estimates, press, unverified valuations", ("5%", {"bold": True, "size": 14, "color": BURG})]]
table(s, 4.1, 1.5, 8.73, 4.2, data, col_w=[1.6, 2.2, 3.8, 0.9], size=9.5, align=["l", "l", "l", "c"])
rect(s, 4.1, 5.85, 8.73, 1.0, fill=WHITE, line=NAVY, lw=1)
txt(s, 4.25, 5.85, 8.5, 1.0, [[("Mark discipline: ", {"bold": True, "color": NAVY}), ("6 of 9 IQT entry marks and most Weapons marks are estimates. Each is flagged in the model and must be confirmed via primary cap-table access before an IC vote on a material check. Lower tiers refine; only Tier 1 sets conviction.", {})]], size=10, anchor="m")

# ---------------------------------------------------------------- 10 SCREENING
s = slide("09 | Screening", "Screening Gates I: The Five-Axis Strategic Score")
table(s, 0.5, 1.45, 5.6, 2.55, [["Axis", "Weight", "Question"],
    ["China AI/semi-race criticality", "25%", "Advances US AI-compute / node lead?"],
    [("Taiwan / TSMC insulation", {"bold": True, "color": NAVY}), ("30%", {"bold": True}), "Reduces dependence on Taiwan fabs?"],
    ["Gov / defense embeddedness", "15%", "IQT, DoD, DIU, DARPA, CHIPS pull?"],
    ["CFIUS-clean / US-sovereign", "15%", "US domicile; acquirable by gov/primes?"],
    ["Supply-chain chokepoint", "15%", "Sole / near-sole source at a node?"]], col_w=[2.2, 0.7, 2.7], size=9.2, align=["l", "c", "l"])
rect(s, 0.5, 4.15, 5.6, 1.15, fill=NAVY)
txt(s, 0.65, 4.2, 5.3, 1.05, [[("Shock CAGR formula", {"caps": True, "bold": True, "color": GOLD, "size": 9})],
    [("Shock CAGR = Base CAGR + (Composite − 2.5) × 8%/pt", {"font": SERIF, "size": 14})],
    "Substrate 4.85 → +18.8% → 40.8%   ·   DefendEye 1.70 → −6.4% drag"], size=9.5, color=WHITE, spacing=3)
band(s, 0.5, 5.45, 5.6, 0.3, "Interpretation bands", fill=WHITE, color=NAVY)
for i, (lab, d_, f) in enumerate([("> 4.0", "Core sovereign exposure", TEAL), ("2.5–4.0", "Partial winner", NAVY), ("< 2.5", "Drag — needs a non-thesis reason", BURG)]):
    x = 0.5 + i * 1.87
    rect(s, x + 0.02, 5.8, 1.83, 1.05, fill=PANEL, line=LINE)
    txt(s, x + 0.05, 5.85, 1.77, 0.45, lab, size=16, color=f, font=SERIF, align="c")
    txt(s, x + 0.05, 6.3, 1.77, 0.5, d_, size=9, align="c")
sc = [["Company", "China", "TSMC", "Gov", "CFIUS", "Choke", "Composite", "Shock CAGR"],
      ["Substrate (anchor)", 5, 5, 4, 5, 5, "4.85", "40.8%"], ["EUV Tech", 5, 4, 4, 5, 5, "4.55", "30.4%"], ["ThinTronics", 4, 5, 4, 5, 4, "4.45", "41.6%"],
      ["Diraq", 4, 4, 4, 2, 3, "3.55", "38.4%"], ["Mueon", 3, 3, 4, 5, 3, "3.45", "39.6%"], ["Infleqtion", 4, 2, 4, 5, 3, "3.40", "22.2%"],
      ["Syntiant", 4, 2, 4, 5, 2, "3.25", "22.0%"], ["EdgeCortix", 4, 2, 4, 2, 2, "2.80", "26.4%"], ["DefendEye", 2, 1, 3, 2, 1, "1.70", "21.6%"]]
for r in sc[1:]:
    c = float(r[6]); col = TEAL if c > 4 else (BURG if c < 2.5 else NAVY)
    r[6] = (r[6], {"bold": True, "color": col})
band(s, 6.3, 1.45, 6.53, 0.32, "Scoring matrix — IQT-mirror sleeve (1 = low, 5 = high)")
table(s, 6.3, 1.77, 6.53, 3.9, sc, col_w=[2.0, 0.6, 0.6, 0.6, 0.65, 0.65, 0.9, 0.95], size=9.2)
rect(s, 6.3, 5.8, 6.53, 1.05, fill=PANEL, line=LINE)
txt(s, 6.45, 5.82, 6.3, 1.0, [[("Scores are levers, not facts. ", {"bold": True, "color": NAVY}), ("A ±1 point error on the TSMC axis moves shock CAGR by ±2.4%. Each score carries written justification and is sensitivity-tested before IC. Axis weights and scenario weights must each sum to 100% (integrity check).", {})]], size=9.5, anchor="m")

# ---------------------------------------------------------------- 11 OVERLAY + GATES
s = slide("09 | Screening", "Screening Gates II: Munitions / FMS Overlay and Hard Pass-Fail Gates")
band(s, 0.5, 1.45, 6.0, 0.32, "Munitions / FMS overlay — Weapons sleeve")
txt(s, 0.5, 1.85, 6.0, 0.75, [[("Exposure = avg(Munitions shortage 0–5, FMS / export backlog 0–5).  ", {"bold": True}), ("CAGR uplift per point: Base +0.5% · Bull +0.8% · Bear +0.4% (backlog cushion) · Shock +0.6%.", {})]], size=9.8)
table(s, 0.5, 2.6, 6.0, 3.3, [["Holding", "Shortage", "FMS", "Exposure", "Base → Adj."],
    ["Israel Aerospace Ind.", 5, 5, ("5.0", {"bold": True, "color": TEAL}), "17.0% → 19.5%"],
    ["Ellwood Group", 5, 4, "4.5", "13.0% → 15.3%"], ["Superior & Grand Valley", 5, 4, "4.5", "13.0% → 15.3%"],
    ["Helicon Chemical", 5, 3, "4.0", "28.0% → 30.0%"], ["Epirus", 3, 3, "3.0", "24.0% → 25.5%"],
    ["Elta Systems", 2, 4, "3.0", "16.0% → 17.5%"], ["Heckler & Koch", 3, 3, "3.0", "12.0% → 13.5%"],
    ["Saronic", 2, 3, "2.5", "26.0% → 27.3%"], ["Applied Research Assoc.", 3, 2, "2.5", "14.0% → 15.3%"]], col_w=[2.2, 0.8, 0.7, 0.9, 1.4], size=9)
rect(s, 0.5, 6.0, 6.0, 0.85, fill=PANEL, line=LINE)
txt(s, 0.65, 6.0, 5.75, 0.85, "Why the Bear uplift stays positive: multiyear procurement and FMS backlog are contracted demand. A budget slip delays but rarely cancels replenishment already under contract.", size=9.5, anchor="m")
band(s, 6.7, 1.45, 6.13, 0.32, "Hard gates — pass / fail before any modeling", fill=BURG)
table(s, 6.7, 1.77, 6.13, 3.75, [["Gate", "Pass condition", "If it fails"],
    ["Domicile / CFIUS", "US-sovereign, or allied with minority structuring", "Minority-only, capped (EdgeCortix, Diraq)"],
    ["ITAR / foreign ownership", "Holdable structure (cornerstone, CDR, block)", "Reduce or pass"],
    ["NDAA / Blue UAS", "Clean component provenance", "Provenance diligence first (DefendEye)"],
    ["Access", "Real route: primary, secondary, cornerstone, pref", "Flag access-constrained; placeholder only"],
    ["Entry mark source", "Priced round, secondary print, or contract-derived EV", "Flag estimate; confirm before IC"]],
    col_w=[1.5, 2.4, 2.2], hdr_fill=BURG, size=9, align=["l", "l", "l"])
rect(s, 6.7, 5.65, 6.13, 1.2, fill=WHITE, line=BURG, lw=1)
txt(s, 6.85, 5.68, 5.9, 1.15, [[("Hard passes", {"bold": True, "caps": True, "color": BURG})],
    "• No defensible route to a stake at any price   • Thesis needs the Bull case to clear the hurdle",
    "• Provenance/CFIUS issue not curable by minority structuring   • Revenue not traceable to contracts (Weapons) or no government validation (IQT)"], size=9.2, spacing=2)

# ---------------------------------------------------------------- 12 UNDERWRITING
s = slide("10 | Underwriting", "Underwriting: Program-Level Bottom-Up Builds")
flow = [("Program lines", "Each tied to one named driver"), ("Program CAGR", "Driver growth + share gain, per scenario"), ("Discrete steps", "Awards, LRIP→FRP, IPO — not smoothed"),
        ("Margin ramp", "Linear to scenario exit margin over N yrs"), ("Cash", "EBITDA × FCF conversion, retained"), ("Exit equity", "Exit EBITDA × multiple − net debt + cash"),
        ("Implied CAGR", "(Exit equity / entry post)^(1/T) − 1 → sleeve")]
cw = 12.33 / 7
for i, (a, b) in enumerate(flow):
    x = 0.5 + i * cw
    rect(s, x + 0.03, 1.45, cw - 0.3, 1.2, fill=NAVY if i in (0, 6) else WHITE, line=None if i in (0, 6) else LINE)
    txt(s, x + 0.08, 1.5, cw - 0.4, 1.1, [[(a, {"bold": True, "caps": True, "size": 9})], b], size=9, color=WHITE if i in (0, 6) else INK, align="c", anchor="m")
    if i < 6: arrow(s, x + cw - 0.24, 1.97, 0.18, 0.14)
band(s, 0.5, 2.8, 6.05, 0.32, "Faxon Machining — $9M / 9.8% @ $92M post")
table(s, 0.5, 3.12, 6.05, 2.75, [["Program", "FY26E $M", "Driver", "Base CAGR"],
    ["BLU-136/B warhead cases", "30", "US munitions procurement", "6%"], ["Tomahawk (TLAM) components", "7", "TLAM MYP ramp", "20%"],
    ["Commercial & other defense", "7", "Industrial", "3%"], ["GBU-57 MOP penetrator cases", "4", "MOP replenishment", "17%"],
    ["FMS / allied pull-through", "4", "FMS demand", "12%"], ["LPWC IDIQ + missile structures", "6", "Penetrators / missiles", "11–14%"],
    ["NGP GBU-76/B (dev + production step)", "2", "Award yr 3 Base / never in Bear", "10% + step"],
    [("Total / weighted", {"bold": True, "color": NAVY}), ("60", {"bold": True}), "", ("9.2%", {"bold": True})]], col_w=[2.5, 0.9, 1.8, 0.9], size=8.8)
rect(s, 0.5, 5.95, 6.05, 0.9, fill=PANEL, line=LINE)
txt(s, 0.65, 5.95, 5.8, 0.9, [[("Entry check: ", {"bold": True, "color": NAVY}), ("Bear $21M / Base $76M / Bull $194M at 25/50/25 = $91.75M EV → $92M post is fair, not a discount. Implied 10.95x FY26E EBITDA ($8.4M @ 14%) vs LHX 15.1x, RHM 17.3x.", {})]], size=9.3, anchor="m")
band(s, 6.75, 2.8, 6.08, 0.32, "L3Harris Missile Solutions — $15M pre-IPO")
rect(s, 6.75, 3.12, 6.08, 1.55, fill=NAVY)
txt(s, 6.9, 3.17, 5.8, 1.45, [[("Pre-IPO entry", {"caps": True, "bold": True, "color": GOLD, "size": 9})],
    [("2027E EBIT $574M × 22x = $12.6B IPO value", {"font": SERIF, "size": 13})],
    [("× (1 − 15% pre-IPO discount) = $10.7B entry", {"font": SERIF, "size": 13})],
    "Program build: PAC-3, THAAD, SM, Tomahawk, GMLRS/PrSM, hypersonics, Golden Dome NGI/GMD/SM-3/GPI"], size=9, color=WHITE, spacing=3)
txt(s, 6.75, 4.8, 6.08, 0.3, [[("Embedded underwriting principles", {"caps": True, "bold": True})]], size=9, color=NAVY)
bullets(s, 6.75, 5.1, 6.08, 1.8, [("Contracts over aggregators: ", "revenue rebuilt from awards and periods of performance."),
    ("Recompete risk lives in Bear: ", "BLU-136/B order period ends 30-Sep-26 → partial loss modeled."),
    ("Dilution explicit: ", "Proceeds = Check × (1+CAGR)^T × Retention. IQT 0.85/0.78/0.68; Weapons 0.92/0.88/0.82 at 5/7/10 yrs."),
    ("Post-IPO dilution: ", "3% for DoW warrants and equity comp at MSL.")], size=9.2)

# ---------------------------------------------------------------- 13 CLOCKS
s = slide("11 | Catalyst orientation", "Catalyst Orientation: Multiple Clocks, One Holdco")
band(s, 0.5, 1.45, 8.5, 0.32, "Constraint research separates each thesis into different clocks")
clocks = [("Near-term", "0–12 months", "Contract & recompete cycles", ["BLU-136/B order period ends 30-Sep-26", "IDIQ task orders", "FY27 appropriations / CR"]),
          ("Binary events", "0–24 months", "Award & listing windows", ["MSL IPO (Q1-27; co. guided mid-27)", "NGP GBU-76/B production award", "IAI IPO attempt (H2-26)"]),
          ("Multi-year", "1–5 years", "Production ramps", ["Tomahawk MYP to 1,000+/yr", "PAC-3 / THAAD interceptor ramps", "CHIPS disbursement"]),
          ("Long-duration", "5+ years", "Structural regimes", ["NATO 5% path to 2035", "Taiwan / Davidson window", "Domestic fail-safe stack build-out"])]
cw = 8.5 / 4
for i, (a, b, c, bl) in enumerate(clocks):
    x = 0.5 + i * cw
    rect(s, x + 0.03, 1.82, cw - 0.06, 2.75, fill=WHITE, line=LINE)
    txt(s, x + 0.1, 1.9, cw - 0.2, 0.5, [[(a, {"caps": True, "bold": True})], [(b, {"color": MUTED})]], size=9.5, color=NAVY, align="c")
    txt(s, x + 0.1, 2.45, cw - 0.2, 0.35, [[(c, {"italic": True})]], size=9, color=TEAL, align="c")
    bullets(s, x + 0.12, 2.85, cw - 0.24, 1.7, bl, size=9)
band(s, 9.2, 1.45, 3.63, 0.32, "Key distinction")
rect(s, 9.2, 1.77, 3.63, 2.8, fill=PANEL, line=LINE)
txt(s, 9.3, 1.85, 3.43, 0.8, "Thesis duration is not hold duration.", size=15, color=NAVY, font=SERIF, align="c")
bullets(s, 9.35, 2.7, 3.38, 1.85, ["A 2035 rearmament thesis can be harvested through a 5-yr vehicle.", "5 / 7 / 10-yr holds price the same names on different clocks.", "Pre-IPO and listed names ladder DPI ahead of private exits.", "Never treat all clocks as one timeline — it mis-times capital."], size=9.2)
band(s, 0.5, 4.75, 12.33, 0.32, "The six-step PE capital cycle")
cyc = [("Establish structural thesis", "Long-term constraint across multiple clocks"), ("Identify catalyst", "Nearest reachable award, IPO or ramp"),
       ("Size around catalyst", "Probability, payoff and access asymmetry"), ("Monetize the event", "IPO, strategic sale, secondary, recap"),
       ("Retain structural exposure", "Keep core through the long clock"), ("Rotate into next bottleneck", "Recycle into the next binding constraint")]
cw = 12.33 / 6
for i, (a, b) in enumerate(cyc):
    x = 0.5 + i * cw
    rect(s, x + 0.03, 5.12, cw - 0.3, 1.72, fill=WHITE, line=LINE)
    num(s, x + (cw - 0.3) / 2 - 0.13, 5.2, i + 1, d=0.28, size=9)
    txt(s, x + 0.08, 5.55, cw - 0.4, 0.5, [[(a, {"caps": True, "bold": True})]], size=8.8, color=NAVY, align="c")
    txt(s, x + 0.08, 6.1, cw - 0.4, 0.7, b, size=9, align="c", color=MUTED)
    if i < 5: arrow(s, x + cw - 0.24, 5.9, 0.18, 0.14)

# ---------------------------------------------------------------- 14 SCENARIOS & RETURNS
s = slide("12 | Scenarios & return math", "Scenario Architecture and Return Math: Underwrite to Expected")
sc4 = [("Base", "45%", "Supercycle continues at funded budget levels", NAVY), ("Bull", "25%", "Accelerated procurement, multiple expansion, faster exits", TEAL),
       ("Bear", "15%", "Budget slip, recompete losses, exit window shut, venture write-downs", BURG), ("TSMC-Shock", "15%", "Taiwan blockade / hard decoupling: sovereign names re-rate; Consumer hit", GOLD)]
for i, (a, w, b, f) in enumerate(sc4):
    y = 1.45 + i * 0.95
    rect(s, 0.5, y, 1.1, 0.85, fill=f)
    txt(s, 0.5, y, 1.1, 0.85, [[(w, {"font": SERIF, "size": 18})], [(a, {"caps": True, "bold": True, "size": 8})]], size=9, color=WHITE, align="c", anchor="m")
    rect(s, 1.6, y, 3.0, 0.85, fill=WHITE, line=LINE)
    txt(s, 1.7, y, 2.85, 0.85, b, size=9.3, anchor="m")
rect(s, 0.5, 5.3, 4.1, 1.55, fill=PANEL, line=LINE)
txt(s, 0.65, 5.33, 3.85, 1.5, [[("Scenario rules", {"caps": True, "bold": True, "color": NAVY})],
    "• Weights fixed before looking at output.", "• Shock is a low-probability tail; its 10-yr multiples are large by design — keep 15% honest.",
    "• Each scenario has its own drivers, share gain, margin and multiple — no blanket haircuts."], size=9.2, spacing=2)
band(s, 4.8, 1.45, 8.03, 0.32, "Holdco 7-yr hold — net to LP")
table(s, 4.8, 1.77, 8.03, 1.6, [["Metric", "Base", "Bull", "Bear", "Shock", "Expected"],
    ["Net IRR", "16.0%", "28.2%", ("−5.0%", {"color": BURG}), "23.4%", ("19.4%", {"bold": True, "color": NAVY})],
    ["Net MOIC", "2.83x", "5.69x", ("0.70x", {"color": BURG}), "4.37x", ("3.46x", {"bold": True, "color": NAVY})],
    ["KS-PME vs ITA/SOXX", "1.06x", "2.14x", ("0.26x", {"color": BURG}), "1.64x", ("1.30x", {"bold": True, "color": NAVY})],
    ["KS-PME vs SPX", "1.55x", "3.11x", ("0.38x", {"color": BURG}), "2.39x", ("1.89x", {"bold": True, "color": NAVY})]], col_w=[2.0, 1, 1, 1, 1, 1.2], size=9.5)
band(s, 4.8, 3.55, 3.9, 0.32, "Fund terms & waterfall")
bullets(s, 4.85, 3.95, 3.85, 1.5, [("2% ", "management fee on committed, full life"), ("8% ", "compounded preferred return"), ("20% ", "carry, no GP catch-up (conservative)"), ("Whole-fund ", "European waterfall")], size=9.5)
band(s, 8.9, 3.55, 3.93, 0.32, "Decision thresholds", fill=TEAL)
bullets(s, 8.95, 3.95, 3.85, 1.5, [("Required: ", "Expected KS-PME vs basket > 1.0x — else buy the ETF."), ("Preferred: ", "Base KS-PME ≥ 1.0x (today 1.06x — thin; demands entry discipline)."), ("Position: ", "Base gross MOIC ≥ ~2.0x at 5 yrs (≈15% IRR) unless ballast or liquidity bridge.")], size=9.2)
rect(s, 4.8, 5.55, 8.03, 1.3, fill=WHITE, line=NAVY, lw=1)
txt(s, 4.95, 5.58, 7.8, 1.25, [[("Read-through. ", {"bold": True, "color": NAVY}), ("Bear is a capital-loss case at every hold, carried by IQT seeds and Consumer — sizing is the protection. The Shock tail lifts Expected because the book is overweight US sovereign chokepoints; Consumer is the one sleeve hurt there. Biggest swing factors: Weapons CAGR (largest sleeve), the thematic hurdle, and the rate path via IQT exit timing.", {})]], size=9.6, anchor="m")

# ---------------------------------------------------------------- 15 CONSTRUCTION
s = slide("13 | Portfolio construction", "Sizing & Construction: Anchor, Core, Pre-IPO, Venture, Optionality, Ballast", 27)
tr = [("Anchor", "Highest-conviction sovereign bet, capped", ["Substrate ~32% of IQT sleeve", "Binary tech risk capped even at max conviction"], "5–10 yrs"),
      ("Growth core", "Revenue-generating chokepoint leaders", ["EUV Tech, ThinTronics, Helicon", ">15% stake → board seat / observer"], "5–7 yrs"),
      ("Pre-IPO / liquid", "Discounted entry ahead of listing", ["MSL, Syntiant, IAI, Infleqtion", "Ladders DPI ahead of private exits"], "1–3 yrs"),
      ("Quantum venture", "Post-Moore optionality", ["Diraq (allied, minority-only)", "Listed benchmark: Infleqtion"], "7–10 yrs"),
      ("Seed optionality", "Small, milestone-gated", ["Mueon (needs shipping design win)", "DefendEye (provenance first)"], "7–10 yrs"),
      ("Ballast", "Uncorrelated DPI engine", ["Consumer/Value sleeve, $200M", "Market-priced via secondaries"], "3–5 yrs")]
cw = 12.33 / 6
for i, (a, b, bl, t) in enumerate(tr):
    x = 0.5 + i * cw
    num(s, x + cw / 2 - 0.16, 1.42, i + 1)
    rect(s, x + 0.03, 1.8, cw - 0.06, 0.45, fill=NAVY if i < 5 else TEAL)
    txt(s, x + 0.03, 1.8, cw - 0.06, 0.45, a, size=12, color=WHITE, font=SERIF, align="c", anchor="m")
    rect(s, x + 0.03, 2.25, cw - 0.06, 2.55, fill=WHITE, line=LINE)
    txt(s, x + 0.1, 2.32, cw - 0.2, 0.7, [[(b, {"bold": True})]], size=9.5, color=NAVY, align="c")
    bullets(s, x + 0.12, 3.05, cw - 0.24, 1.2, bl, size=9)
    rect(s, x + 0.03, 4.3, cw - 0.06, 0.5, fill=PANEL)
    txt(s, x + 0.03, 4.3, cw - 0.06, 0.5, [[("Horizon", {"caps": True, "bold": True, "size": 8})], t], size=9, align="c", anchor="m")
band(s, 0.5, 4.95, 12.33, 0.32, "Construction rules", fill=WHITE, color=NAVY)
rules = [("Trim vs new money", "Substitute exposure is funded by trimming (Faxon: Superior & GV $40M→$31M). Additive exposure gets new commitment (MSL: Weapons $390M→$405M)."),
         ("Never drift", "Each sleeve's deployed capital must equal its commitment — enforced by integrity checks."),
         ("Follow-on reserve", "IQT holds $25M of $250M for pro-rata defense of winners, embedded in retention factors."),
         ("Allied = smaller", "Foreign / allied names stay minority-only and capped; the CFIUS ceiling limits exit buyers.")]
cw = 12.33 / 4
for i, (a, b) in enumerate(rules):
    x = 0.5 + i * cw
    rect(s, x + 0.03, 5.32, cw - 0.06, 1.53, fill=PANEL, line=LINE)
    txt(s, x + 0.12, 5.38, cw - 0.24, 1.45, [[(a, {"bold": True, "caps": True, "color": NAVY, "size": 9})], b], size=9.2, spacing=3)

# ---------------------------------------------------------------- 16 TRIPWIRES
s = slide("14 | Risk management", "Risk Management: A Tripwire-Based Falsification Framework")
rect(s, 0.5, 1.42, 12.33, 0.45, fill=NAVY)
txt(s, 0.6, 1.42, 12.1, 0.45, "Each holdco thesis carries explicit conditions that would break it — not just catalysts that confirm it.", size=13, color=WHITE, font=SERIF, align="c", anchor="m")
rect(s, 0.5, 2.0, 2.6, 3.95, fill=PANEL, line=LINE)
txt(s, 0.62, 2.08, 2.4, 3.85, [[("Why tripwires?", {"bold": True, "caps": True, "color": NAVY})],
    "In illiquid PE the principal risk is thesis invalidation, not mark volatility — marks lag reality by quarters.",
    "We pre-define the conditions under which the underwriting stops being valid, and act on them before the mark moves.",
    [("Principle", {"bold": True, "caps": True, "color": NAVY})], "Paid to be wrong early when the constraint disappears, not right at any cost."], size=9.3, spacing=5)
tw = [("Durable US-China détente", "Verified de-escalation that reprices the Taiwan tail toward zero.", ["Credible cross-strait framework", "Export-control rollback", "Taiwan risk premia compress"], TEAL),
      ("Procurement retrenchment", "Congress scales back munitions MYPs or Golden Dome funding.", ["MYP quantities cut / cancelled", "Reconciliation fails; prolonged CRs", "NATO members slip from 5% path"], NAVY),
      ("Constraint dissolves", "Capacity catches up and the bottleneck stops binding.", ["New SRM / forging entrants qualify", "Lead times normalize", "Pricing power lost at recompete"], GOLD),
      ("Exit-window failure", "IPO and M&A windows stay shut through hold horizon.", ["MSL / IAI IPOs pulled again", "Higher-for-longer compresses multiples", "Secondary discounts widen > 30%"], BURG)]
cw = 9.6 / 4
for i, (a, b, bl, f) in enumerate(tw):
    x = 3.23 + i * cw
    rect(s, x + 0.02, 2.0, cw - 0.04, 3.95, fill=WHITE, line=LINE)
    num(s, x + cw / 2 - 0.16, 2.1, i + 1, fill=f)
    txt(s, x + 0.1, 2.5, cw - 0.2, 0.5, [[(a, {"bold": True, "caps": True})]], size=9.5, color=NAVY, align="c")
    txt(s, x + 0.1, 3.0, cw - 0.2, 0.85, b, size=9.2, align="c")
    txt(s, x + 0.1, 3.9, cw - 0.2, 0.3, [[("What would falsify the thesis", {"bold": True})]], size=8.8, color=NAVY)
    bullets(s, x + 0.12, 4.2, cw - 0.24, 1.4, bl, size=8.8)
    rect(s, x + 0.1, 5.82, cw - 0.2, 0.05, fill=f)
band(s, 0.5, 6.05, 1.6, 0.8, "Position kill rules", fill=BURG, size=9)
rect(s, 2.1, 6.05, 10.73, 0.8, fill=PANEL, line=LINE)
txt(s, 2.25, 6.05, 10.5, 0.8, [[("If triggered: pause follow-ons, de-risk, reassess. ", {"bold": True, "color": NAVY}), ("Position-level tripwires: key contract lost at recompete (Faxon BLU-136/B) · milestone missed on gated seed (Mueon design win) · provenance unresolved (DefendEye) · entry mark not confirmable via cap table · CFIUS/ITAR structure fails.", {})]], size=9.3, anchor="m")

# ---------------------------------------------------------------- 17 DILIGENCE & IC
s = slide("15 | Diligence & IC workflow", "From Idea to IC: Diligence Workflow and Model Discipline")
wf = ["Macro driver", "Map $ flow & chokepoints", "Source via 7 lenses", "Hard gates", "Score + overlay", "Program build", "4-scenario returns", "KS-PME > 1.0x?", "Size & structure", "Integrity checks", "IC vote", "Confirm marks"]
cw = 12.33 / 12
for i, a in enumerate(wf):
    x = 0.5 + i * cw
    dark = i in (3, 7)
    rect(s, x + 0.02, 1.45, cw - 0.16, 0.85, fill=BURG if dark else NAVY if i in (0, 10) else WHITE, line=None if (dark or i in (0, 10)) else LINE)
    txt(s, x + 0.04, 1.45, cw - 0.2, 0.85, [[(a, {"bold": True})]], size=8.5, color=WHITE if (dark or i in (0, 10)) else NAVY, align="c", anchor="m")
    if i < 11: arrow(s, x + cw - 0.13, 1.8, 0.11, 0.1)
txt(s, 0.5, 2.35, 12.33, 0.3, [[("Red = gates where a target exits to pass / watchlist.", {"italic": True})]], size=8.5, color=BURG, align="c")
cols = [("Thesis fit", ["Which driver(s) does it monetize? Show the $ flow.", "Which cluster / role? What does it replace or add?", "5-axis score and/or munitions/FMS exposure, justified per axis."]),
        ("Commercial", ["Contract inventory: values, periods, recompete dates, IDIQ ceilings & awardee count.", "Program split — disclosed or estimated (flag).", "Customer concentration; capacity to deliver the ramp; capex."]),
        ("Financial & valuation", ["QoE on EBITDA; margin vs peers (precision machining 10–18%).", "FCF conversion after growth capex; net debt and debt-like items.", "Entry multiple vs LHX / RHM / AVAV and private marks (Anduril, Saronic)."]),
        ("Structure, regulatory & exit", ["Pref stack, anti-dilution, pro rata, info & board rights; dilution path.", "CFIUS, ITAR/EAR, FOCI, facility clearance, NDAA, CMMC.", "Natural acquirers, IPO feasibility, secondary depth."])]
cw = 12.33 / 4
for i, (a, bl) in enumerate(cols):
    x = 0.5 + i * cw
    band(s, x + 0.03, 2.75, cw - 0.06, 0.32, a, fill=NAVY if i < 3 else TEAL, size=9)
    rect(s, x + 0.03, 3.07, cw - 0.06, 2.3, fill=WHITE, line=LINE)
    bullets(s, x + 0.12, 3.15, cw - 0.24, 2.2, bl, size=9.2, bullet="☐", spacing=6)
band(s, 0.5, 5.5, 12.33, 0.32, "Model discipline", fill=WHITE, color=NAVY)
md = [("Colour code", "Blue = input · green = link · black = formula. The IC Summary page holds no inputs."),
      ("Integrity checks", "Holdco = $855M · each sleeve deployed = committed · probabilities = 100% · axis weights = 100% · holdco ties to sleeves."),
      ("Versioning", "Every new position is a dedicated build tab, re-pointed links, all checks pass, versioned file committed.")]
cw = 12.33 / 3
for i, (a, b) in enumerate(md):
    x = 0.5 + i * cw
    rect(s, x + 0.03, 5.87, cw - 0.06, 0.98, fill=PANEL, line=LINE)
    txt(s, x + 0.12, 5.9, cw - 0.24, 0.92, [[(a, {"bold": True, "caps": True, "color": NAVY, "size": 9})], b], size=9.2, spacing=2)

# ---------------------------------------------------------------- 18 EIGHT CHARACTERISTICS
s = slide("16 | How I think", "Eight Defining Characteristics of the PE Process")
ch = [("Constraint-first", "Geopolitics → budgets → contracts → capacity → equity value", ["Every link evidenced", "Buy what the world can’t expand fast enough"]),
      ("Non-consensus", "Two layers below the obvious deal", ["Tier-2/3 suppliers over headline primes", "Comfortable being early"]),
      ("Physical over narrative", "Forgings, energetics, motors, metrology", ["Requalification takes years", "The moat is physical"]),
      ("Evidence-driven", "Contracts and filings over vendor estimates", ["Tier-1 sources set conviction", "Facts first, interpretation second"]),
      ("Asymmetry-seeking", "Convex to the most mispriced scenario", ["Long the Taiwan/TSMC tail", "Base case must still pay"]),
      ("Catalyst-aware", "Discrete events stay discrete", ["Awards, IPOs, recompetes as steps", "Multiple clocks, one holdco"]),
      ("Access-oriented", "Structure solves access", ["Pref, cornerstone, secondary blocks", "Illiquidity is paid for, not feared"]),
      ("Honest about tails", "Weights fixed before output", ["Benchmark vs the thematic ETF", "Bear case reported beside Expected"])]
for i, (a, b, bl) in enumerate(ch):
    col, row = i // 4, i % 4
    x = 0.5 + col * 6.25; y = 1.45 + row * 1.37
    rect(s, x, y, 0.65, 1.27, fill=NAVY)
    txt(s, x, y, 0.65, 1.27, str(i + 1), size=30, color=WHITE, font=SERIF, align="c", anchor="m")
    rect(s, x + 0.65, y, 5.43, 1.27, fill=PANEL, line=LINE)
    txt(s, x + 0.8, y + 0.12, 2.5, 1.05, [[(a, {"bold": True, "caps": True, "size": 10.5, "color": NAVY})], [(b, {"size": 9, "color": MUTED, "caps": True})]], size=9, spacing=4)
    bullets(s, x + 3.35, y + 0.18, 2.65, 1.0, bl, size=9.2)

# ---------------------------------------------------------------- 19 BLIND SPOTS
s = slide("17 | Self-critique", "Stress-Testing the Framework: Known Blind Spots and Fixes")
txt(s, 0.5, 1.4, 12.33, 0.4, [[("Complexity is not superiority. ", {"bold": True, "color": NAVY}), ("A framework earns trust by naming where its own model flatters the answer.", {})]], size=12, align="c")
table(s, 0.5, 1.9, 12.33, 4.3, [["Blind spot", "Mechanism / why it matters", "Direction of bias", "Fix"],
    ["Single-factor concentration", "~76% of holdco (IQT + Weapons) loads on one geopolitical factor; no de-escalation scenario", "Understates correlated downside", "Add a 5th ‘De-escalation’ scenario; cap factor exposure"],
    ["Judgment-based scores", "±1 pt on TSMC axis = ±2.4% shock CAGR; scores drive the convexity case", "Overstates conviction", "Score sensitivity tables; second-scorer review"],
    ["Point-to-point IRR", "Single exit cash flow; no J-curve, staged calls or interim DPI", "Overstates net IRR", "Build quarterly call / distribution schedule"],
    ["Simplified waterfall", "No GP catch-up, whole-fund; real LPAs usually include catch-up", "Overstates upside net to LP", "Model full catch-up as sensitivity"],
    ["Minority liquidity", "Family / ESOP stakes may need deep discounts to exit", "Overstates exit value", "Apply DLOM; negotiate puts / redemption"],
    ["Budget execution", "Requests ≠ appropriations; CRs and reconciliation risk (Golden Dome)", "Front-loads ramps", "Tie Base to appropriated $ only"],
    ["Elevated exit multiples", "Uses today’s 15–22x for 2031–36 exits after the re-rate", "Overstates terminal value", "Mean-revert exit multiples in Base"]],
    col_w=[2.0, 4.4, 2.1, 3.8], size=9, align=["l", "l", "l", "l"])
rect(s, 0.5, 6.3, 12.33, 0.55, fill=WHITE, line=NAVY, lw=1)
arrow(s, 0.65, 6.49, 0.3, 0.18)
txt(s, 1.1, 6.3, 11.6, 0.55, [[("That is what separates an investment framework from an interesting research hobby: ", {"bold": True, "color": NAVY}), ("the model is built to be falsified, not admired.", {})]], size=10.5, anchor="m")

# ---------------------------------------------------------------- 20 SCORECARD
s = slide("18 | Tools", "One-Page PE Target Scorecard")
fields = [("Thesis", ["Company / sleeve / cluster", "Driver(s) monetized & $ flow evidence", "Binding constraint it owns", "Role in book: replaces or adds?"]),
          ("Screening", ["5-axis composite / shock premium", "Munitions shortage / FMS / exposure", "Domicile · CFIUS · ITAR · NDAA", "Access route & structure"]),
          ("Valuation", ["Entry post-money & source (priced / secondary / contract / estimate)", "Check · ownership · board rights", "Implied entry multiple vs comps", "Pref stack & dilution path"]),
          ("Underwriting", ["FY revenue (program-built) · margin · FCF", "Base / Bull / Bear / Shock CAGR", "Discrete events & dates", "Retention @ 5 / 7 / 10 yrs"]),
          ("Returns", ["Gross MOIC / IRR by scenario", "Expected MOIC / IRR", "Contribution to holdco KS-PME", "Funding: trim (which) or new money"]),
          ("Risk", ["Top 3 risks", "Thesis tripwires", "Position kill rules", "Open diligence items before IC"])]
for i, (a, fl) in enumerate(fields):
    col, row = i % 3, i // 3
    x = 0.5 + col * 4.15; y = 1.45 + row * 2.75
    band(s, x, y, 4.0, 0.34, a, fill=NAVY if i < 5 else BURG, size=9.5)
    for j, f in enumerate(fl):
        yy = y + 0.4 + j * 0.56
        rect(s, x, yy, 4.0, 0.52, fill=PANEL if j % 2 == 0 else WHITE, line=LINE)
        txt(s, x + 0.1, yy, 2.2, 0.52, f, size=8.8, anchor="m", color=INK)
        rect(s, x + 2.4, yy + 0.08, 1.5, 0.36, fill=WHITE, line=LINE)

# ---------------------------------------------------------------- 21 FINAL
s = slide("19 | Final assessment", "Final PE Assessment")
band(s, 0.5, 1.45, 5.3, 0.32, "Who D. B. Ritts III is as a PE allocator")
rect(s, 0.5, 1.77, 5.3, 2.4, fill=WHITE, line=LINE)
txt(s, 0.65, 1.85, 5.0, 1.0, "A high-conviction, research-intensive allocator who finds structural constraints before they become consensus deals.", size=12, color=NAVY, font=SERIF, align="c")
txt(s, 0.65, 2.9, 5.0, 1.25, "Maps geopolitical and structural themes through budgets, programs and production lines until he finds the scarce asset — the motor, the forging, the energetic, the metrology tool — then uses structure (minority, pref, pre-IPO, secondary) to own it at a price that beats the thematic ETF.", size=9.5, align="c")
band(s, 6.0, 1.45, 6.83, 0.32, "The edge: an integrated framework")
ed = ["Macro awareness", "Constraint decomposition", "Contract-based research", "Strategic scoring", "Program-level builds", "Catalyst clocks", "Private-market access", "Tripwire discipline"]
cw = 6.83 / 8
rect(s, 6.0, 1.77, 6.83, 2.4, fill=WHITE, line=LINE)
for i, a in enumerate(ed):
    x = 6.0 + i * cw
    num(s, x + cw / 2 - 0.15, 1.95, i + 1, d=0.3, size=9)
    txt(s, x + 0.02, 2.35, cw - 0.04, 0.8, [[(a, {"bold": True})]], size=8.5, color=NAVY, align="c")
txt(s, 6.1, 3.3, 6.63, 0.8, [[("Integrated analysis  →  structural insight  →  asymmetric private returns", {"caps": True, "bold": True})]], size=9.5, color=TEAL, align="c", anchor="m")
band(s, 0.5, 4.32, 12.33, 0.32, "How conviction is built")
bc = [("Theme identification", "Structural shift with a named $ flow"), ("Constraint mapping", "Budget → program → capacity"), ("Chokepoint detection", "Who gates throughput"),
      ("Value accretion", "Where rent accrues; contract-derived value"), ("Ownership strategy", "Optimal structure to access it"), ("Catalyst & realization", "Monetize event; rotate to next bottleneck")]
cw = 12.33 / 6
for i, (a, b) in enumerate(bc):
    x = 0.5 + i * cw
    rect(s, x + 0.03, 4.69, cw - 0.3, 1.1, fill=PANEL, line=LINE)
    txt(s, x + 0.08, 4.72, cw - 0.4, 1.05, [[(f"{i+1}. {a}", {"bold": True, "caps": True, "size": 8.8, "color": NAVY})], b], size=9, align="c", anchor="m", spacing=3)
    if i < 5: arrow(s, x + cw - 0.24, 5.17, 0.18, 0.14)
rect(s, 0.5, 5.95, 12.33, 0.9, fill=WHITE, line=NAVY, lw=1.25)
txt(s, 0.6, 5.9, 0.7, 0.8, "“", size=48, color=NAVY, font=SERIF)
txt(s, 1.3, 5.97, 10.8, 0.55, "He follows the thesis down the supply chain until he finds the bottleneck — then finds the best structure to own it privately.", size=15, color=NAVY, font=SERIF, align="c", anchor="m")
txt(s, 1.3, 6.5, 10.8, 0.3, [[("Seeks the constraint. Owns the bottleneck. Captures the rent before the re-rate.", {"caps": True, "track": 100})]], size=8.5, color=MUTED, align="c")
txt(s, 12.1, 5.95, 0.7, 0.8, "”", size=48, color=NAVY, font=SERIF)

# ================================================================ NEW: RESEARCH & SELECTION SLIDES (22+)
# ---------------------------------------------------------------- 22 SELECTION EQUATION
s = slide("Target selection", "What Makes a Target Selectable: The Selection Equation")
rect(s, 0.5, 1.42, 12.33, 0.75, fill=NAVY)
txt(s, 0.6, 1.42, 12.1, 0.75, [[("Attractiveness  =  ", {}), ("Demand engines", {"color": GOLD}), ("  ×  ", {}), ("Constraint / moat", {"color": GOLD}), ("  ×  ", {}),
    ("Evidence quality", {"color": GOLD}), ("  ×  ", {}), ("Entry price", {"color": GOLD}), ("  ×  ", {}), ("Access", {"color": GOLD})]], size=16, color=WHITE, font=SERIF, align="c", anchor="m")
eq = [("Demand engines", "How many independent secular curves pull on this company — and how wide is the addressable market?",
       ["Two engines beat one: Substrate = national security + AI boom", "Breadth beats depth: Made In sells to every household cohort"]),
      ("Constraint / moat", "What can the market not route around — capacity, qualification, IP, brand, network?",
       ["Physical: forgings, energetics, SRMs, metrology", "Commercial: pro-chef credibility, subscription habit, payments network"]),
      ("Evidence quality", "Is the thesis provable from compelled disclosures, contracts and priced marks?",
       ["Contract-derived revenue (Faxon $60M vs $21M aggregator)", "Forge / tender prints over stale rounds"]),
      ("Entry price", "Does today’s mark leave room for the Base case to clear ~15% gross IRR and beat the ETF?",
       ["Pre-IPO discount (MSL −15%)", "Compressed multiples (Thrive −27% vs 2021)"]),
      ("Access", "Is there a real, structurable route to a meaningful stake?",
       ["Significant minority + board (EUV Tech 17%)", "Family / ESOP / carve-out routes others skip"])]
cw = 12.33 / 5
for i, (a, q, ex) in enumerate(eq):
    x = 0.5 + i * cw
    rect(s, x + 0.03, 2.32, cw - 0.06, 3.55, fill=WHITE, line=LINE)
    num(s, x + cw / 2 - 0.16, 2.42, i + 1)
    txt(s, x + 0.1, 2.8, cw - 0.2, 0.35, [[(a, {"bold": True, "caps": True})]], size=10, color=NAVY, align="c")
    txt(s, x + 0.12, 3.15, cw - 0.24, 1.1, [[(q, {"italic": True})]], size=9.5, color=INK, align="c")
    rect(s, x + 0.12, 4.3, cw - 0.24, 0.01, fill=LINE)
    bullets(s, x + 0.12, 4.38, cw - 0.24, 1.45, ex, size=9)
rect(s, 0.5, 6.0, 12.33, 0.85, fill=PANEL, line=LINE)
txt(s, 0.65, 6.0, 2.1, 0.85, [[("Multiplicative, not additive", {"bold": True, "caps": True})]], size=9.5, color=BURG, anchor="m")
txt(s, 2.8, 6.0, 9.9, 0.85, "Any factor near zero kills the target, however strong the rest. A brilliant chokepoint with no access route, or a huge TAM at a mark that can’t clear the hurdle, is a pass — or a watchlist entry until the weak factor changes.", size=10, anchor="m")

# ---------------------------------------------------------------- 23 EIGHT SELECTION LENSES
s = slide("Target selection", "Eight Selection Lenses: How I Decide a Company Deserves Capital")
lens = [("Dual-engine convergence", "Pulled by two independent secular demand curves?", "Substrate (nat-sec + AI) · ThinTronics (CHIPS + AI packaging) · MSL (Golden Dome + munitions)"),
        ("TAM breadth", "How many demographics, channels and geographies can buy it without category education?", "Made In (every household) · Quince (value trade-down) · Stripe (every online merchant)"),
        ("Chokepoint / sole source", "Can the system route around it?", "EUV Tech (no fab qualifies without it) · Ellwood · Helicon"),
        ("Contract-visible demand", "Is the demand already signed?", "Faxon ($473M BLU-136/B) · MSL (PAC-3, THAAD MYPs) · IAI"),
        ("Sovereign validation", "Has a strategic allocator already vetted it?", "Nine IQT-backed names · ThinTronics $50M CHIPS LOI"),
        ("Unit economics & repeat", "Does each customer pay back — and come back?", "Farmer’s Dog (profitable, >$1B rev) · Thrive (membership) · Whoop (subscription)"),
        ("Catalyst proximity", "What event re-rates it inside my hold?", "MSL IPO · Whoop IPO track · Farmer’s Dog Walmart.com · NGP award"),
        ("Mark quality & access", "Is the price real, and can I get in?", "Stripe tender ($159B) · Forge prints — vs. GOAT’s 5-yr-stale mark")]
for i, (a, q, ex) in enumerate(lens):
    col, row = i % 4, i // 4
    x = 0.5 + col * 3.1; y = 1.45 + row * 2.72
    rect(s, x, y, 2.95, 2.6, fill=WHITE, line=LINE)
    rect(s, x, y, 2.95, 0.55, fill=NAVY if i not in (1, 5) else TEAL)
    txt(s, x + 0.1, y, 0.5, 0.55, str(i + 1), size=20, color=WHITE, font=SERIF, anchor="m")
    txt(s, x + 0.55, y, 2.35, 0.55, [[(a, {"bold": True, "caps": True})]], size=9.5, color=WHITE, anchor="m")
    txt(s, x + 0.15, y + 0.65, 2.65, 0.85, [[(q, {"italic": True})]], size=10, color=NAVY, font=SERIF)
    rect(s, x + 0.15, y + 1.5, 2.65, 0.01, fill=LINE)
    txt(s, x + 0.15, y + 1.57, 2.65, 0.95, [[("In the book: ", {"bold": True, "color": TEAL}), (ex, {})]], size=9)

# ---------------------------------------------------------------- 24 RESEARCH QUESTION STACK
s = slide("Research process", "How I Research a Target: The Question Stack")
txt(s, 0.5, 1.4, 12.33, 0.4, "Research is a sequence of questions, each with its own evidence. A target advances only when the current layer is answered from primary sources.", size=11.5, align="c")
table(s, 0.5, 1.9, 12.33, 4.35, [["Stage", "Core questions", "Primary sources", "Output / gate"],
    [("1  Demand engines", {"bold": True, "color": NAVY}), "Who must buy this? How many independent curves drive it? How wide is the TAM across demographics, channels, geographies?", "Budgets & appropriations, procurement notices, census / household data, category sizing, channel checks", "Named $ flow; engine count; TAM map"],
    [("2  Constraint / moat", {"bold": True, "color": NAVY}), "What can’t the market route around? How long to replicate? Who else could supply?", "Supplier lists, qualification records, IDIQ awardee counts, patents, expert calls", "Chokepoint or brand moat — or pass"],
    [("3  Company proof", {"bold": True, "color": NAVY}), "Is revenue real and visible? Contracts, cohorts, repeat rates, margins?", "FPDS / SAM awards, S-1s, management data, QoE, cohort data", "Program-level or unit-level build"],
    [("4  Price", {"bold": True, "color": NAVY}), "What is the mark, and what tier of evidence supports it?", "Priced rounds, Forge / tender prints, contract-derived EV, comps", "Mark tier: priced / secondary / contract / estimate"],
    [("5  Access & structure", {"bold": True, "color": NAVY}), "Can I get a meaningful stake? Which structure protects me?", "Cap table, ROFR / transfer terms, CFIUS / ITAR review", "Route + structure + ownership %"],
    [("6  Scenarios & exit", {"bold": True, "color": NAVY}), "What happens in Base / Bull / Bear / Shock? Who buys it, and when?", "Model, precedent exits, IPO windows, strategic acquirer map", "Expected MOIC / IRR, KS-PME, tripwires"]],
    col_w=[1.7, 4.0, 3.9, 2.4], size=9.2, align=["l", "l", "l", "l"])
rect(s, 0.5, 6.35, 12.33, 0.5, fill=NAVY)
txt(s, 0.7, 6.35, 12, 0.5, [[("Rule: ", {"bold": True, "color": GOLD}), ("never skip to stage 4. A cheap price on a company without a demand engine or moat is a value trap, not an opportunity.", {})]], size=10.5, color=WHITE, anchor="m")

# ---------------------------------------------------------------- CASE STUDY TEMPLATE
def case(section, title, tag, logic, engines, must, risks, facts, rets, verdict, eng_fills=(NAVY, TEAL)):
    s = slide(section, title)
    rect(s, 0.5, 1.42, 7.4, 0.32, fill=PALE)
    txt(s, 0.6, 1.42, 7.2, 0.32, [[("Selection lens: ", {"bold": True, "color": NAVY}), (tag, {"color": NAVY})]], size=10, anchor="m")
    ew = 7.4 / len(engines)
    for i, (hd, bl) in enumerate(engines):
        x = 0.5 + i * ew
        band(s, x + (0.03 if i else 0), 1.85, ew - 0.06, 0.34, hd, fill=eng_fills[i % 2], size=9.5)
        rect(s, x + (0.03 if i else 0), 2.19, ew - 0.06, 1.85, fill=WHITE, line=LINE)
        bullets(s, x + 0.12, 2.27, ew - 0.24, 1.75, bl, size=9.2, spacing=4)
    rect(s, 0.5, 4.15, 7.4, 0.95, fill=PANEL, line=LINE)
    txt(s, 0.62, 4.15, 7.2, 0.95, [[("Why it was selected: ", {"bold": True, "color": NAVY}), (logic, {})]], size=9.8, anchor="m")
    for i, (hd, bl, f) in enumerate([("What must be true", must, TEAL), ("Risks & tripwires", risks, BURG)]):
        x = 0.5 + i * 3.73
        txt(s, x, 5.2, 3.6, 0.28, [[(hd, {"bold": True, "caps": True})]], size=9, color=f)
        rect(s, x, 5.47, 3.6, 0.02, fill=f)
        bullets(s, x, 5.55, 3.6, 1.35, bl, size=9, spacing=2)
    band(s, 8.1, 1.42, 4.73, 0.32, "Position")
    table(s, 8.1, 1.74, 4.73, 0.3 * len(facts), [["Item", "Value"]] + facts, col_w=[2.2, 2.5], size=9, align=["l", "l"])
    yy = 1.74 + 0.3 * len(facts) + 0.45
    band(s, 8.1, yy - 0.05, 4.73, 0.32, "Gross MOIC by scenario (model)")
    table(s, 8.1, yy + 0.27, 4.73, 1.0, [["Hold", "Base", "Bull", "Bear", "Shock"]] + rets, col_w=[1.0, 0.9, 0.9, 0.9, 0.9], size=9.5)
    vy = yy + 1.42
    rect(s, 8.1, vy, 4.73, 6.85 - vy, fill=NAVY)
    txt(s, 8.25, vy + 0.05, 4.45, 6.85 - vy - 0.1, [[("Verdict", {"caps": True, "bold": True, "color": GOLD, "size": 9})], [(verdict, {"font": SERIF, "size": 11.5})]], size=10, color=WHITE, spacing=4, anchor="m")
    return s

def br(v):  # colour bear/shock sub-1x
    return (v, {"color": BURG}) if float(v.rstrip("x")) < 1 else v

# ---------------------------------------------------------------- 25 SUBSTRATE
case("Case study · IQT-mirror", "Case Study — Substrate: Two Engines, One Asset",
     "Dual-engine convergence — national security × the AI boom",
     "Two independent demand curves converge on one asset. If the AI cycle cools, the national-security need for domestic leading-edge patterning remains; if geopolitics calms, AI demand for leading-edge wafer capacity remains. That gives a high floor on strategic value with convex upside — the highest composite score in the book (4.85).",
     [("Engine 1 — National security", ["Domestic X-ray lithography and US fabs: a path to leading-edge chips if Taiwan / TSMC access is lost", "IQT-backed — sovereign validation", "CFIUS-clean US sovereign: acquirable by government or primes"]),
      ("Engine 2 — AI boom", ["AI accelerators consume leading-edge wafers; fab capacity is the binding constraint", "Aims to lower cost per leading-edge wafer versus EUV-based patterning", "US fab build-out captures onshoring and CHIPS capital"])],
     ["Tool reaches production-grade yield and throughput", "Fab financing and anchor customers or government offtake secured", "Timeline lands inside the 7–10-yr vehicles"],
     ["Binary technology risk — Bear 0.32x (5-yr)", "Capital intensity drives dilution (retention 0.78 at 7 yrs)", ">$1B entry mark leaves little room for slippage"],
     [["Entry post-money", "$1,050M (est., Oct-25 round)"], ["Check / ownership", "$80M / 7.6%"], ["Sizing", "Anchor — 32% of IQT sleeve (capped)"], ["Composite / shock prem.", "4.85 / +18.8%"], ["CAGR B / Bu / Be / S", "22% / 34% / −18% / 40.8%"]],
     [["5-yr", "2.30x", "3.67x", br("0.32x"), "4.70x"], ["7-yr", "3.14x", "6.05x", br("0.19x"), "8.56x"]],
     "Anchor position: maximum conviction, capped size. The dual engine justifies the largest check; the binary technology risk justifies the cap.")

# ---------------------------------------------------------------- 26 MADE IN
case("Case study · Consumer / Value", "Case Study — Made In Cookware: TAM Breadth Across Demographics",
     "TAM breadth — a universal category reachable through every cohort and channel",
     "Cookware is bought by virtually every household, at every life stage, through several channels at once — no category education needed. A premium brand with professional-kitchen credibility can compound across age, income and channel. Capital efficiency (only ~$8.3M ever raised) signals self-funded unit economics and means low dilution for a 6.25% stake.",
     [("Demographic breadth", ["Household formation: first-kitchen buyers (Gen Z / millennials)", "Affluent upgrade and replacement cycle", "Gifting and wedding registries", "Home-cooking and aging cohorts trading up"]),
      ("Channel breadth", ["DTC brand, with wholesale / retail placements", "Restaurant and pro-chef placements — pro use feeds consumer trust", "Category extension: knives, bakeware, tools", "International runway"])],
     ["Repeat and attach rates across product lines", "Wholesale scales without eroding brand pricing", "DTC CAC stays stable as the brand scales"],
     ["Least-grounded mark in the sleeve — no secondary market exists", "Import / COGS / tariff exposure: −14% Shock CAGR", "Base IRR ~11–12% sits below the ~15% position hurdle"],
     [["Entry EV", "$280M (estimate)"], ["Check / ownership", "$17.5M / 6.25%"], ["Capital raised to date", "~$8.3M ($5M 2019 seed)"], ["Channels", "DTC + wholesale + restaurant"], ["CAGR B / Bu / Be / S", "14% / 26% / −10% / −14%"]],
     [["5-yr", "1.73x", "2.86x", br("0.53x"), br("0.42x")], ["7-yr", "2.10x", "4.24x", br("0.40x"), br("0.29x")]],
     "Held for TAM optionality (Bull 4.2x at 7 yrs). Before any upsizing, confirm the mark through company financials, repeat rate and wholesale mix.")

# ---------------------------------------------------------------- 27 EUV TECH
case("Case study · IQT-mirror", "Case Study — EUV Tech: The Chokepoint With a Floor",
     "Chokepoint / sole source — plus downside protection",
     "At-wavelength EUV metrology is a node no leading-edge fab can route around: processes aren’t qualified without it. The company already generates revenue as a niche leader, so the Bear case is roughly capital-preserving (~1.0x) — the best risk-adjusted name in the IQT sleeve. A ~17% stake earns governance.",
     [("Chokepoint", ["At-wavelength EUV metrology: no fab qualifies without it", "Revenue-generating niche leader", "Supply-chain chokepoint score 5 / 5"]),
      ("Sovereignty", ["US (CA), CFIUS-clean: score 5 / 5", "China-race criticality 5 / 5", "Every domestic EUV fab is a customer"])],
     ["Domestic EUV fab build-out proceeds", "Retains its niche as tool vendors integrate", "Board seat secured at ~17%"],
     ["Niche TAM caps Base at 14% CAGR (below hurdle)", "Dependence on the EUV ecosystem", "Mark is an estimate (undisclosed)"],
     [["Entry post-money", "$180M (estimate)"], ["Check / ownership", "$30M / 16.7%"], ["Governance", "Significant minority — board seat"], ["Composite / shock prem.", "4.55 / +16.4%"], ["CAGR B / Bu / Be / S", "14% / 26% / 3% / 30.4%"]],
     [["5-yr", "1.64x", "2.70x", br("0.99x"), "3.20x"], ["7-yr", "1.95x", "3.93x", br("0.96x"), "5.00x"]],
     "Growth-core holding selected for asymmetry: limited downside, 5x in Shock. It is the book’s protection against the binary risk in the anchor.")

# ---------------------------------------------------------------- 28 FARMER'S DOG vs THRIVE
s = slide("Case study · Consumer / Value", "Case Study — Reading the Secondary Tape: Farmer’s Dog vs. Thrive Market")
txt(s, 0.5, 1.4, 12.33, 0.4, "Two subscription consumer names, both priced by Forge secondaries (Sep-26). Same lens — unit economics and repeat — with opposite lessons on entry price.", size=11.5, align="c")
for j, (nm, hd, f, pts, facts, rets, lesson) in enumerate([
    ("The Farmer’s Dog", "Compounding with a catalyst", TEAL,
     [("Unit economics: ", "profitable, >$1B annualized revenue"), ("Repeat: ", "subscription staple — pets eat every day"), ("Catalyst: ", "Walmart.com launch (2025): DTC-only → omnichannel"), ("Tape: ", "Forge $23.64/sh = $3.76B, up from $2.5B Series E (Jun-22)"), ("Defensive: ", "Bear CAGR +10%; Shock only −5%")],
     "$24.5M check · 0.65% · CAGR 22 / 34 / 10 / −5%", [["5-yr", "2.43x", "3.89x", "1.45x", br("0.70x")], ["7-yr", "3.38x", "6.52x", "1.64x", br("0.59x")]],
     "The market has repriced it up, and the fundamentals justify it. It is the only consumer name above 1.0x in the Bear case."),
    ("Thrive Market", "Growth without return", BURG,
     [("Unit economics: ", "membership DTC; revenue $400M → $700M+"), ("Tape: ", "Forge $17.98/sh = ~$945M, down ~27% from $1.29B Series C (Jul-21)"), ("Diagnosis: ", "real multiple compression — the 2021 entry multiple was the problem"), ("Role: ", "IPO candidate at a compressed entry"), ("Base CAGR: ", "7% — the lowest in the sleeve")],
     "$14M check · 1.5% · CAGR 7 / 16 / −5 / −8%", [["5-yr", "1.26x", "1.89x", br("0.70x"), br("0.59x")], ["7-yr", "1.35x", "2.37x", br("0.59x"), br("0.47x")]],
     "Revenue nearly doubled and the equity still fell. Growth does not equal return when the entry price is set at peak multiples.")]):
    x = 0.5 + j * 6.27
    band(s, x, 1.9, 6.06, 0.36, f"{nm} — {hd}", fill=f)
    rect(s, x, 2.26, 6.06, 2.15, fill=WHITE, line=LINE)
    bullets(s, x + 0.15, 2.35, 5.8, 2.0, pts, size=9.5, spacing=4)
    txt(s, x, 4.48, 6.06, 0.28, [[(facts, {"bold": True})]], size=9.2, color=NAVY)
    table(s, x, 4.78, 6.06, 0.9, [["Gross MOIC", "Base", "Bull", "Bear", "Shock"]] + rets, col_w=[1.2, 1, 1, 1, 1], size=9.5)
    rect(s, x, 5.8, 6.06, 0.55, fill=PANEL, line=LINE)
    txt(s, x + 0.12, 5.8, 5.85, 0.55, [[("Lesson: ", {"bold": True, "color": f}), (lesson, {})]], size=9.3, anchor="m")
rect(s, 0.5, 6.45, 12.33, 0.42, fill=NAVY)
txt(s, 0.7, 6.45, 12, 0.42, [[("Price the tape, not the last round. ", {"bold": True, "color": GOLD}), ("Secondary prints are Tier-3 evidence for timing — and the best available truth on what a 2021 mark is really worth today.", {})]], size=10.2, color=WHITE, anchor="m")

# ---------------------------------------------------------------- 29 RATIONALE MAP I
s = slide("Selection map", "Selection Rationale Map I: Why Each IQT-Mirror and Consumer Name Is Held")
L = lambda t: (t, {"color": TEAL, "bold": True, "size": 8.3})
band(s, 0.5, 1.42, 6.06, 0.32, "IQT-mirror (deep tech) — $250M")
table(s, 0.5, 1.74, 6.06, 5.1, [["Name", "Primary lens", "Selection rationale"],
    ["Substrate", L("Dual engine"), "National-security litho + AI wafer capacity; anchor, capped"],
    ["EUV Tech", L("Chokepoint"), "EUV metrology no fab can skip; revenue; ~1.0x Bear"],
    ["ThinTronics", L("Dual engine"), "US ABF substrates vs. Ajinomoto; $50M CHIPS LOI catalyst"],
    ["EdgeCortix", L("Sovereign valid."), "Denied-environment edge AI; Japan → minority only; Renesas exit"],
    ["Syntiant", L("Catalyst"), "Edge-AI inference; S-1 filed — liquidity ladder"],
    ["Infleqtion", L("Mark quality"), "Listed quantum benchmark (INFQ); PIPE / secondary"],
    ["Diraq", L("Dual engine"), "Quantum on standard CMOS foundries; AUKUS-aligned optionality"],
    ["Mueon", L("Sovereign valid."), "Dense domestic AI compute; seed, milestone-gated"],
    ["DefendEye", L("Optionality"), "Autonomous sensing; gated on NDAA / Blue UAS provenance"]],
    col_w=[1.2, 1.25, 3.6], size=8.6, align=["l", "l", "l"])
band(s, 6.77, 1.42, 6.06, 0.32, "Consumer / Value — $200M", fill=TEAL)
table(s, 6.77, 1.74, 6.06, 5.1, [["Name", "Primary lens", "Selection rationale"],
    ["Quince", L("TAM breadth"), "Manufacturer-to-consumer value model; >$1B ARR; $10.1B Mar-26"],
    ["Whoop", L("Catalyst"), "Wearable → medical-grade / glucose; IPO track; $10.1B Mar-26"],
    ["Farmer’s Dog", L("Unit economics"), "Profitable subscription >$1B; Walmart.com; tape up to $3.76B"],
    ["Made In", L("TAM breadth"), "Every household cohort and channel; capital-light; mark unproven"],
    ["Thrive Market", L("Mark quality"), "Membership DTC at compressed entry (−27%); IPO candidate"],
    ["Plunge", L("Category creation"), "Cold-plunge wellness; ~$200M lifetime sales, mostly self-funded"],
    ["Polymarket", L("Dual engine"), "Event-volume convexity + regulated US / ICE distribution"],
    ["GOAT Group", L("Re-underwrite"), "Resale marketplace; 5-yr-stale 2021 mark — verify before check"],
    ["Stripe", L("Mark quality"), "Payments infrastructure; TPV +34%; $159B tender — most liquid"]],
    col_w=[1.2, 1.25, 3.6], hdr_fill=TEAL, size=8.6, align=["l", "l", "l"])

# ---------------------------------------------------------------- 30 RATIONALE MAP II
s = slide("Selection map", "Selection Rationale Map II: Why Each Weapons Name Is Held")
table(s, 0.5, 1.45, 12.33, 4.85, [["Name", "Primary lens", "Selection rationale", "Access / structure", "Exposure"],
    ["Saronic", L("Dual engine"), "Naval autonomy hypergrowth: $200M 2025 revenue (+1,500%); Replicator", "Late and expensive ($9.25B) → secondary only", "2.5"],
    ["Epirus", L("Chokepoint"), "High-power microwave counter-drone — fastest-growing threat pool", "US clean; growth stage", "3.0"],
    ["Israel Aerospace Ind.", L("Contract demand"), "Allied prime with maximum munitions and FMS backlog", "IPO cornerstone; ITAR remains", "5.0"],
    ["Elta Systems", L("Contract demand"), "EW / ISR franchise consolidating into the IAI IPO", "Within IAI", "3.0"],
    ["Heckler & Koch", L("Contract demand"), "NATO small-arms standardization and rearmament", "Listed, closely held → block", "3.0"],
    ["Helicon Chemical", L("Chokepoint"), "Energetics: the scarcest input in replenishment; early growth", "Real stake: 26.7%", "4.0"],
    ["The Ellwood Group", L("Chokepoint"), "Missile-casing and naval forgings; ~0.9x sales entry", "Family-owned → structured pref", "4.5"],
    ["Superior & Grand Valley", L("Chokepoint"), "Missile procurement metal forging", "Placeholder mark", "4.5"],
    ["Applied Research Assoc.", L("Sovereign valid."), "R&D house; NGP system design agent", "ESOP — structurally hard", "2.5"],
    ["Faxon Machining", L("Contract demand"), "Warhead-case machining: BLU-136/B, MOP, NGP, TLAM", "9.8% minority; contract-derived EV", "4.0"],
    ["L3Harris MSL", L("Dual engine"), "#2 US SRM maker: munitions MYPs + Golden Dome interceptors", "Pre-IPO, 15% discount", "—"]],
    col_w=[2.0, 1.4, 4.6, 3.0, 0.9], size=9, align=["l", "l", "l", "l", "c"])
rect(s, 0.5, 6.4, 12.33, 0.45, fill=PANEL, line=LINE)
txt(s, 0.65, 6.4, 12.1, 0.45, [[("Pattern: ", {"bold": True, "color": NAVY}), ("the Weapons sleeve concentrates on chokepoints and contract-visible demand; the hard-access structures (family, ESOP, carve-out, IPO cornerstone) are where the price edge comes from.", {})]], size=9.8, anchor="m")

# ---------------------------------------------------------------- 31 RED FLAGS
s = slide("Selection discipline", "Selection Discipline: Red Flags That Gate or Shrink a Check")
table(s, 0.5, 1.45, 12.33, 4.6, [["Name", "Red flag", "Evidence", "Action taken"],
    ["GOAT Group", ("Stale mark", {"color": BURG, "bold": True}), "Last priced Series F Jun-21; no live Forge quote", "Re-underwrite before any check"],
    ["Made In Cookware", ("Unproven mark", {"color": BURG, "bold": True}), "No secondary market; estimated EV", "Confirm via financials before upsizing"],
    ["Superior & Grand Valley", ("Placeholder mark", {"color": BURG, "bold": True}), "No disclosed valuation", "Trimmed $40M → $31M to fund Faxon"],
    ["Saronic", ("Price", {"color": BURG, "bold": True}), "$9.25B on $200M revenue (~46x)", "Secondary or late primary only"],
    ["DefendEye", ("Provenance", {"color": BURG, "bold": True}), "EU cap table; Krakow manufacturing", "NDAA / Blue UAS diligence before defense credit"],
    ["EdgeCortix", ("Foreign nexus", {"color": BURG, "bold": True}), "Japan HQ; TSMC-Kumamoto exposure", "Minority-only; CFIUS ceiling on exit"],
    ["Thrive Market", ("Multiple compression", {"color": BURG, "bold": True}), "−27% vs 2021 despite revenue +75%", "Small check; held as IPO candidate"],
    ["Faxon Machining", ("Recompete", {"color": BURG, "bold": True}), "BLU-136/B order period ends 30-Sep-26", "Partial loss in Bear; diligence position"],
    ["Applied Research Assoc.", ("Access", {"color": BURG, "bold": True}), "Employee-owned ESOP", "Structured approach; realistic liquidity"]],
    col_w=[2.2, 1.8, 4.3, 4.0], size=9.2, align=["l", "l", "l", "l"])
rect(s, 0.5, 6.15, 12.33, 0.7, fill=WHITE, line=BURG, lw=1)
txt(s, 0.65, 6.15, 12.1, 0.7, [[("A red flag rarely kills a great company outright — it changes the size, the structure or the timing. ", {"bold": True, "color": BURG}), ("Only flags that can’t be cured (no access, incurable provenance, a thesis that needs the Bull case) are hard passes.", {})]], size=10, anchor="m")

# final order: research & selection first, then portfolio, risk and tools
reorder(p, [1, 22, 23, 2, 3, 24, 9, 8, 25, 26, 27, 28, 12, 29, 30, 10, 11, 31, 4, 5, 6, 7, 14, 15, 13, 16, 17, 18, 19, 20, 21])
stamp_pages(p)

p.save(OUT)
print("saved", OUT, N[0], "slides")
