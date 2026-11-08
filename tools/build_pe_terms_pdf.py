"""Render Guide #2 (PE terminology) as a designed PDF using the Fund Communications
Design System v2, marketing register: Source Serif 4 display, Public Sans Light text,
ink / paper foundation, ordered data palette, horizontal bars, endnotes, disclosure lines.

Usage: python3 tools/build_pe_terms_pdf.py  ->  guides/PE_Essentials_Terminology_Guide.pdf
"""
import os, re, subprocess, json, html
import markdown

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SRC = os.path.join(ROOT, "guides", "02_PE_Terminology_Structure_Concepts.md")
HTML_OUT = os.path.join(ROOT, "guides", "PE_Essentials_Terminology_Guide.html")
PDF_OUT = os.path.join(ROOT, "guides", "PE_Essentials_Terminology_Guide.pdf")
DOC_ID = "LEVIATHAN-PEG02-20261108"

# ordered data palette (design system: assign in order, Mist = residual)
P = ["#1B5E5C", "#4C9F8B", "#006492", "#C39D78", "#A5CD24", "#CACED7"]
T = ["#8DAEAD", "#A5CFC5", "#80B1C8", "#E0CEBB", "#D2E592", "#E3E6EA"]

CSS = """
@page { size: Letter; margin: 0.85in 0.7in 0.95in 0.7in; }
* { box-sizing: border-box; }
html { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
body { margin:0; font-family:'Public Sans',Helvetica,Arial,sans-serif; font-weight:300; color:#000;
       font-size:9.5pt; line-height:1.4; -webkit-font-smoothing:antialiased; }
.serif { font-family:'Source Serif 4',Georgia,serif; font-weight:600; }
b, strong { font-weight:500; }
em { font-style:normal; font-weight:500; }
sup.en { font-size:7pt; font-weight:500; margin-left:1px; }
.xref { color:#A95228; font-weight:500; }
p { margin:0 0 7pt; }
/* masthead / cover */
.mast-top { display:flex; justify-content:space-between; font-size:8pt; font-weight:300; letter-spacing:.04em; text-transform:uppercase; }
.mast-top b { font-weight:500; }
.rule-ink { height:1px; background:#000; margin:8pt 0 18pt; }
.eyebrow { font-size:10pt; font-weight:500; letter-spacing:.04em; text-transform:uppercase; }
h1.title { font-family:'Source Serif 4',Georgia,serif; font-weight:600; font-size:27pt; line-height:1.08; margin:8pt 0 12pt; letter-spacing:-.01em; }
.lead { font-size:12pt; line-height:1.35; font-weight:300; max-width:6.1in; margin-bottom:14pt; }
.keyfigs { display:grid; grid-template-columns:repeat(3,1fr); gap:14pt; margin:6pt 0 20pt; }
.kf { border-top:2px solid #1B5E5C; padding-top:7pt; }
.kf .v { font-family:'Source Serif 4',Georgia,serif; font-weight:600; font-size:26pt; line-height:1; }
.kf .l { font-size:9pt; font-weight:400; margin-top:4pt; line-height:1.3; }
.disc-box { border:1px solid #000; padding:7pt 9pt; font-size:7.5pt; font-weight:500; line-height:1.4; letter-spacing:.01em; margin:14pt 0 8pt; }
/* sections */
.sec { break-before: page; }
.sec.flow { break-before: auto; margin-top:22pt; }
.sec-head { display:flex; align-items:baseline; gap:10pt; border-bottom:1px solid #000; padding-bottom:6pt; margin-bottom:10pt; break-after:avoid; }
.sec-head .n { font-size:9pt; font-weight:500; color:#727272; }
.sec-head h2 { margin:0; font-family:'Source Serif 4',Georgia,serif; font-weight:600; font-size:20pt; line-height:1.1; }
h3 { font-family:'Source Serif 4',Georgia,serif; font-weight:600; font-size:13pt; margin:14pt 0 6pt; break-after:avoid; }
.sub { font-size:9pt; font-weight:300; margin:-3pt 0 8pt; }
/* tables (4.3 performance table pattern) */
table { width:100%; border-collapse:collapse; font-size:8.1pt; font-weight:300; margin:4pt 0 10pt; }
thead { display:table-header-group; }
th { background:#1B5E5C; color:#FFF; font-weight:500; text-align:left; padding:4pt 6pt; vertical-align:bottom; }
td { padding:3.4pt 6pt; border-bottom:1px solid #BFBFBF; vertical-align:top; }
tbody tr:nth-child(even) td { background:#F2F2F2; }
tbody tr:last-child td { border-bottom:1px solid #000; }
td:first-child { font-weight:500; }
tr { break-inside:avoid; }
/* formula block */
.formula { border-top:1px solid #000; border-bottom:1px solid #000; padding:9pt 0; margin:6pt 0 12pt;
           font-family:'Source Serif 4',Georgia,serif; font-weight:600; font-size:11.5pt; text-align:center; }
/* lists */
ul { margin:2pt 0 10pt 0; padding-left:14pt; } li { margin-bottom:3pt; }
/* components */
.panel { background:#FFF; border:1px solid #E4E4E4; padding:10pt 12pt; margin:6pt 0 12pt; break-inside:avoid; }
.panel-title { font-family:'Source Serif 4',Georgia,serif; font-weight:600; font-size:12pt; margin-bottom:2pt; }
.grid-map { display:grid; grid-template-columns:repeat(2,1fr); gap:6pt; margin:6pt 0 8pt; }
.dom { border-top:3px solid #000; background:#F4F4F2; padding:5pt 9pt; break-inside:avoid; }
.dom .k { font-size:8pt; font-weight:500; color:#727272; }
.dom .h { font-family:'Source Serif 4',Georgia,serif; font-weight:600; font-size:11pt; margin:0 0 2pt; }
.dom .d { font-size:8.3pt; line-height:1.35; }
.track { display:grid; gap:4pt; margin:8pt 0 12pt; }
.step { border-top:3px solid #1B5E5C; background:#F4F4F2; padding:7pt 8pt; font-size:8pt; line-height:1.3; break-inside:avoid; }
.step .h { font-weight:500; font-size:8.6pt; margin-bottom:2pt; }
.step .y { color:#727272; font-size:7.6pt; margin-bottom:3pt; }
.step.hl { border-top-color:#A95228; }
.legend { display:flex; flex-wrap:wrap; gap:4pt 14pt; font-size:8pt; margin-top:6pt; }
.legend span.sw { display:inline-block; width:9px; height:9px; margin-right:5px; vertical-align:-1px; }
.stack { display:flex; height:20px; gap:2px; margin:3pt 0; }
.barrow { display:grid; grid-template-columns:1.55in 1fr 0.75in; gap:8pt; align-items:center; font-size:8.3pt; padding:3pt 0; }
.barrow .track2 { height:13px; background:#E4E4E4; position:relative; }
.barrow .fill { position:absolute; top:0; bottom:0; }
.barrow .val { text-align:right; font-weight:500; }
.note { font-size:7.8pt; color:#727272; line-height:1.4; margin-top:4pt; }
.struct { display:grid; grid-template-columns:repeat(4,1fr); gap:6pt; margin:8pt 0 4pt; font-size:8pt; text-align:center; }
.box { border:1px solid #000; padding:6pt 4pt; background:#FFF; line-height:1.25; }
.box b { display:block; font-size:8.6pt; }
.box.ink { background:#1B5E5C; color:#FFF; border-color:#1B5E5C; }
.arrowline { text-align:center; font-size:9pt; color:#727272; margin:2pt 0; letter-spacing:.04em; }
.notes ol { padding-left:16pt; font-size:8pt; line-height:1.45; }
.two { display:grid; grid-template-columns:1fr 1fr; gap:14pt; }
"""

def esc(s): return html.escape(s, quote=False)

def bars(rows, maxv, fmt=lambda v: f"{v}", label_w=None):
    out = []
    for i, (lab, v, color) in enumerate(rows):
        out.append(f'<div class="barrow"><span>{lab}</span><div class="track2"><div class="fill" style="left:0;width:{100*v/maxv:.1f}%;background:{color}"></div></div><span class="val">{fmt(v)}</span></div>')
    return "".join(out)

def range_bars(rows, lo_axis, hi_axis):
    out = []
    for lab, lo, hi, color, txt in rows:
        l = 100 * (lo - lo_axis) / (hi_axis - lo_axis); w = 100 * (hi - lo) / (hi_axis - lo_axis)
        out.append(f'<div class="barrow"><span>{lab}</span><div class="track2"><div class="fill" style="left:{l:.1f}%;width:{w:.1f}%;background:{color}"></div></div><span class="val">{txt}</span></div>')
    return "".join(out)

# ---------------------------------------------------------------- components
MAP = '<div class="grid-map">' + "".join(
    f'<div class="dom"><div class="k">{i:02d}</div><div class="h">{h}</div><div class="d">{d}</div></div>'
    for i, (h, d) in enumerate([
        ("Structure", "GP, LP, ManCo, fund vehicle; feeders, parallels, AIVs, blockers; SPVs and co-invest; continuation vehicles; holdco and sleeves"),
        ("Lifecycle", "Fundraise and closes; investment period; harvest; capital calls and distributions"),
        ("Economics", "Management fee; carry, hurdle and catch-up; European vs American waterfall; clawback"),
        ("Metrics", "IRR and MOIC; TVPI, DPI, RVPI; public market equivalent; the J-curve"),
        ("Strategies", "VC, growth, buyout; carve-outs and take-privates; secondaries and co-invest; credit and distressed"),
        ("Deal process", "Teaser, CIM, IOI, LOI; diligence and QoE; SPA, signing and closing"),
        ("Valuation", "Enterprise-to-equity bridge; multiples, DCF and LBO; pre- and post-money"),
        ("Capital structure", "Revolver, TLB, unitranche; second lien, mezzanine, PIK; preferred and common"),
        ("Equity terms", "Liquidation preference; anti-dilution; drag, tag and ROFR; board and information rights"),
        ("Exits & regulation", "Strategic, sponsor, IPO, continuation; CFIUS, ITAR, FOCI; Advisers Act, ERISA; defense contracting"),
    ], 1)) + "</div>"

STRUCT = """
<div class="panel"><div class="panel-title">How the entities connect</div>
<div class="sub">Capital flows down, proceeds flow back up through the waterfall</div>
<div class="struct" style="grid-template-columns:1fr"><div class="box"><b>Limited Partners</b>Pensions · endowments · sovereigns · insurers · family offices · HNW</div></div>
<div class="arrowline">↓ commitments and capital calls</div>
<div class="struct" style="grid-template-columns:repeat(3,1fr)"><div class="box"><b>Feeder fund</b>pools offshore / wealth LPs</div><div class="box"><b>Parallel fund</b>ERISA / non-US wrapper</div><div class="box"><b>Blocker corp.</b>blocks UBTI / ECI</div></div>
<div class="arrowline">↓</div>
<div class="struct" style="grid-template-columns:2fr 1fr 1fr"><div class="box ink"><b>The Fund (limited partnership)</b>closed-end, ~10 yrs + extensions, governed by the LPA</div><div class="box"><b>General Partner</b>controls fund · earns carry</div><div class="box"><b>Management Co.</b>adviser · earns fee</div></div>
<div class="arrowline">↓ investments</div>
<div class="struct"><div class="box"><b>Portfolio Co. A</b>control buyout</div><div class="box"><b>Portfolio Co. B</b>minority stake</div><div class="box"><b>Co-invest SPV</b>LPs alongside fund</div><div class="box"><b>AIV</b>deal-specific vehicle</div></div>
</div>"""

LIFECYCLE = '<div class="track" style="grid-template-columns:repeat(5,1fr)">' + "".join(
    f'<div class="step{" hl" if hl else ""}"><div class="h">{h}</div><div class="y">{y}</div>{d}</div>' for h, y, d, hl in [
        ("Fundraise", "Year 0 · 12–18 months", "First close, final close, LPA and side letters", False),
        ("Investment period", "Years 1–5", "Capital calls; new platforms; follow-on reserve set", False),
        ("Value creation", "Years 3–8", "Add-ons, follow-ons, operating improvements", False),
        ("Harvest", "Years 4–10", "Exits and distributions; DPI builds", True),
        ("Extension", "Years 10–12", "Tail-end sales or continuation vehicle; wind-down", False)]) + "</div>"

DEAL = '<div class="track" style="grid-template-columns:repeat(5,1fr)">' + "".join(
    f'<div class="step{" hl" if hl else ""}"><div class="h">{i}. {h}</div>{d}</div>' for i, (h, d, hl) in enumerate([
        ("Sourcing → NDA", "Proprietary or banker-led; confidentiality signed", False),
        ("Teaser / CIM → IOI", "Anonymous summary, full book, non-binding range", False),
        ("Mgmt pres. + VDR → LOI", "Data room; price, structure, exclusivity", True),
        ("Confirmatory diligence", "QoE, legal, tax, commercial, regulatory", False),
        ("SPA → sign → close", "HSR / CFIUS clearance, then funds flow", False)], 1)) + "</div>"

def waterfall_panel():
    soft = [("Return of capital", 100.0, P[0]), ("Preferred return", 46.93, P[1]), ("LP 80% split", 73.07, P[2]), ("GP catch-up", 11.73, P[3]), ("GP 20% split", 18.27, T[3])]
    hard = [("Return of capital", 100.0, P[0]), ("Preferred return", 46.93, P[1]), ("LP 80% split", 82.46, P[2]), ("GP 20% split", 20.61, T[3])]
    def stack(rows): return '<div class="stack">' + "".join(f'<div style="flex:{v};background:{c}"></div>' for _, v, c in rows) + "</div>"
    leg = [("Return of capital", P[0]), ("Preferred return", P[1]), ("LP share of remaining", P[2]), ("GP catch-up", P[3]), ("GP 20% carry", T[3])]
    return f"""
<div class="keyfigs">
 <div class="kf"><div class="v">$30.0M</div><div class="l">GP carry with full catch-up (20% of $150M profit)</div></div>
 <div class="kf"><div class="v">$20.6M</div><div class="l">GP carry, hard hurdle, no catch-up <span class="xref">▸</span></div></div>
 <div class="kf"><div class="v">$9.4M</div><div class="l">value of the catch-up to the GP in this example</div></div>
</div>
<div class="panel"><div class="panel-title">Distribution of $250M gross proceeds<sup class="en">(2)</sup></div><div class="sub">$M, before management fees</div>
<div style="font-size:8.3pt;font-weight:500;margin-top:6pt">Soft hurdle, full catch-up</div>{stack(soft)}
<div style="font-size:8.3pt;font-weight:500;margin-top:8pt">Hard hurdle, no catch-up</div>{stack(hard)}
<div class="legend">{''.join(f'<span><span class="sw" style="background:{c}"></span>{l}</span>' for l, c in leg)}</div>
</div>"""

def capstack_panel():
    rows = [("Revolver (RCF)", 2.5, P[0], "S + 2–3%"), ("Term Loan A / B", 3.75, P[0], "S + 3–4.5%"), ("Unitranche", 6.0, P[1], "S + 5–7%"),
            ("Second lien", 7.5, P[1], "S + 6–9%"), ("Mezzanine / PIK", 13.5, P[2], "12–15%"), ("Preferred equity", 12.0, P[3], "10–14%"), ("Common equity", 20.0, P[5], "20%+ target")]
    body = "".join(f'<div class="barrow"><span>{l}</span><div class="track2"><div class="fill" style="left:0;width:{100*v/22:.1f}%;background:{c}"></div></div><span class="val">{t}</span></div>' for l, v, c, t in rows)
    return f"""<div class="panel"><div class="panel-title">The capital stack: senior to junior<sup class="en">(3)</sup></div>
<div class="sub">Indicative cost of capital; bar = midpoint. S = SOFR spread for floating-rate debt.</div>{body}
<div class="note">Senior claims are paid first and cost least; common equity is paid last and targets the highest return. Pricing varies with rates and credit quality.</div></div>"""

def lbo_panel():
    rows = [("Entry equity", 250, P[0]), ("EBITDA growth (+30 × 10x)", 300, P[1]), ("Multiple expansion", 0, P[3]), ("Debt paydown (250 → 120)", 130, P[2]), ("Exit equity", 680, P[0])]
    return f"""
<div class="keyfigs">
 <div class="kf"><div class="v">$680M</div><div class="l">exit equity value (80 × 10x − 120 net debt)</div></div>
 <div class="kf"><div class="v">2.72x</div><div class="l">MOIC on $250M sponsor equity</div></div>
 <div class="kf"><div class="v">22.2%</div><div class="l">IRR over a 5-year hold</div></div>
</div>
<div class="panel"><div class="panel-title">LBO value-creation bridge<sup class="en">(2)</sup></div><div class="sub">$M; entry 10x $50M EBITDA with 5x debt</div>
{bars(rows, 700, lambda v: f"${v:,.0f}M")}</div>"""

def targets_panel():
    rows = [("Large buyout", 15, 20, P[0], "15–20%"), ("Mid-market buyout", 18, 25, P[0], "18–25%"), ("Growth equity", 20, 25, P[1], "20–25%"),
            ("Venture (fund)", 20, 30, P[2], "20–30%+"), ("Secondaries", 12, 18, P[3], "12–18%"), ("Private credit", 9, 13, P[4], "9–13%"),
            ("Leviathan 7-yr Expected", 19.2, 19.6, "#A95228", "19.4%")]
    return f"""<div class="panel"><div class="panel-title">Target net IRR ranges<sup class="en">(4)</sup></div><div class="sub">axis 5% to 35%; bar spans the rule-of-thumb range</div>
{range_bars(rows, 5, 35)}<div class="note">The Leviathan marker is the probability-weighted 7-year holdco net IRR from the IC model.<sup class="en">(1)</sup></div></div>"""

# ---------------------------------------------------------------- markdown -> sections
src = open(SRC, encoding="utf-8").read()
src = re.sub(r"```mermaid.*?```", "", src, flags=re.S)
src = src.replace("▸", '<span class="xref">▸</span>')
md = markdown.Markdown(extensions=["tables", "fenced_code"])

parts = re.split(r"^## ", src, flags=re.M)
sections = []
for part in parts[1:]:
    head, body = part.split("\n", 1)
    m = re.match(r"(\d+)\.\s+(.*)", head.strip())
    n, title = int(m.group(1)), m.group(2)
    body = re.sub(r"\n---\s*$", "", body.strip())
    sections.append((n, title, body))

def render(body):
    md.reset()
    h = md.convert(body)
    h = re.sub(r"<pre><code>(.*?)</code></pre>", lambda m: f'<div class="formula">{m.group(1).strip()}</div>', h, flags=re.S)
    return h

ENDNOTE = {1: 1, 3: 2, 4: 1, 8: 2, 12: 5, 14: 4}
FLOW = {11, 14}  # short sections that continue on the same page
out = []
for n, title, body in sections:
    if n == 0:
        continue  # map is rendered on the cover
    h = render(body)
    if n == 1:
        h = STRUCT + h
    if n == 2:
        h = LIFECYCLE + h
    if n == 3:
        h = h.replace("<h3>3.3", "<h3>3.3", 1)
        idx = h.find("<h3>3.3")
        h = h[:idx] + h[idx:] + waterfall_panel() if idx >= 0 else h
    if n == 6:
        h = DEAL + h
    if n == 8:
        h = capstack_panel() + h + lbo_panel()
    if n == 14:
        h = targets_panel() + h
    en = f'<sup class="en">({ENDNOTE[n]})</sup>' if n in ENDNOTE else ""
    cls = "sec flow" if n in FLOW else "sec"
    out.append(f'<section class="{cls}"><div class="sec-head"><span class="n">{n:02d}</span><h2>{esc(title)}{en}</h2></div>{h}</section>')

NOTES = """<section class="sec flow notes"><div class="sec-head"><span class="n">Notes</span><h2>Sources and endnotes</h2></div><ol>
<li>Leviathan Core PE Holdco IC model, v2 (Faxon / MSL / Golden Dome), September 2026. All <span class="xref">▸</span> figures (holdco size, sleeve structure, net IRR / MOIC, KS-PME, retention, entry marks) are model outputs, estimated and unaudited.</li>
<li>Worked examples (waterfall, LBO, EV bridge, dilution) use round illustrative numbers chosen for arithmetic clarity, not market data.</li>
<li>Capital-stack pricing is indicative and varies with the rate environment, leverage and credit quality.</li>
<li>Return targets are rule-of-thumb ranges used in industry practice, not sourced performance data.</li>
<li>Regulatory thresholds and rules are summarized for reference; confirm against current statute and counsel before relying on them.</li>
</ol><div class="disc-box">THIS IS AN INTERNAL EDUCATIONAL REFERENCE. IT IS NOT AN OFFER, A SOLICITATION OR INVESTMENT ADVICE. NOT FOR DISTRIBUTION.</div><p style="font-size:8pt"><b>Note:</b> Model figures are estimated and unaudited. See Sources and endnotes 1–5.</p></section>"""

COVER = f"""<section>
<div class="rule-ink" style="margin-top:0"></div>
<div class="eyebrow">November 2026</div>
<h1 class="title">Private Equity Essentials:<br>Terminology, Structure and Concepts</h1>
<p class="lead">A reference map of private-market vocabulary, organized from fund structure through economics, metrics, deals, capital structure, terms, exits and <b>regulation</b>. Cross-references to the Leviathan model are marked <span class="xref">▸</span>.</p>
<div class="keyfigs">
 <div class="kf"><div class="v">10</div><div class="l">domains in the reference map</div></div>
 <div class="kf"><div class="v">3</div><div class="l">worked examples: waterfall, LBO, EV bridge<sup class="en">(2)</sup></div></div>
 <div class="kf"><div class="v">$855M</div><div class="l">Leviathan holdco used as the running example<sup class="en">(1)</sup></div></div>
</div>
<div class="sec-head" style="margin-top:6pt"><span class="n">00</span><h2>The map</h2></div>
{MAP}
</section>"""

doc = f"""<!DOCTYPE html><html><head><meta charset="utf-8"><title>PE Essentials Guide</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Public+Sans:wght@300;400;500;600&family=Source+Serif+4:opsz,wght@8..60,400;8..60,600&display=swap" rel="stylesheet">
<style>{CSS}</style></head><body>{COVER}{''.join(out)}{NOTES}</body></html>"""
open(HTML_OUT, "w", encoding="utf-8").write(doc)

HEADER = """<div style="width:100%;font-family:Helvetica,Arial,sans-serif;font-size:7px;letter-spacing:.05em;text-transform:uppercase;padding:0 0.7in;display:flex;justify-content:space-between;color:#000;">
<span style="font-weight:600">D. B. Ritts III · PE Essentials</span><span>Confidential — internal reference</span></div>"""
FOOTER = f"""<div style="width:100%;font-family:Helvetica,Arial,sans-serif;font-size:7px;padding:0 0.7in;color:#000;">
<div style="border-top:1px solid #000;padding-top:4px;display:flex;justify-content:space-between;align-items:baseline;">
<span style="font-weight:600">Illustrative figures are estimated and unaudited. Not investment advice.</span>
<span style="font-family:'Times New Roman',Times,serif;font-size:8px;letter-spacing:.02em">{DOC_ID}</span>
<span><span class="pageNumber"></span> / <span class="totalPages"></span></span></div></div>"""

js = f"""
const {{ chromium }} = require('playwright');
(async () => {{
  const b = await chromium.launch();
  const pg = await b.newPage();
  await pg.goto('file://{HTML_OUT}', {{ waitUntil: 'networkidle' }});
  await pg.evaluate(() => document.fonts.ready);
  await pg.pdf({{ path: '{PDF_OUT}', format: 'Letter', printBackground: true, preferCSSPageSize: true,
    displayHeaderFooter: true, headerTemplate: {json.dumps(HEADER)}, footerTemplate: {json.dumps(FOOTER)} }});
  await b.close();
}})();"""
subprocess.run(["node", "-e", js], check=True, cwd=ROOT)
print("wrote", PDF_OUT)
