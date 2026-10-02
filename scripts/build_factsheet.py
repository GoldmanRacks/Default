#!/usr/bin/env python3
"""
Build the LPEH fact sheet (HTML + PDF) from the recalculated model workbook.

Usage: python3 build_factsheet.py <model_recalculated.xlsx> <out_dir> [fonts_dir]

Every number comes from the 'Fact Sheet Data' tab of the workbook; nothing is typed in here.
Visual theme mirrors the BXPE fact card (Blackstone Private Equity Strategies Fund, July 2026):
black masthead rule, serif display numbers in terracotta, black table headers with grey banding,
teal / dark-teal / tan pie palette, grey small-caps disclaimers, 'Confidential' running header.
"""
import base64
import math
import os
import subprocess
import sys

from openpyxl import load_workbook

SRC, OUT = sys.argv[1], sys.argv[2]
FONTS = sys.argv[3] if len(sys.argv) > 3 else os.path.join(os.path.dirname(os.path.abspath(__file__)), "fonts")
os.makedirs(OUT, exist_ok=True)

wb = load_workbook(SRC, data_only=True)
ws = wb["Fact Sheet Data"]
rows = list(ws.iter_rows(values_only=True))

def find_row(label, col=0, startswith=False):
    for i, r in enumerate(rows):
        v = r[col]
        if isinstance(v, str) and ((v.startswith(label)) if startswith else (v == label)):
            return i
    raise KeyError(label)

# ---- Section A / E: label -> value -----------------------------------------
KV = {}
for r in rows:
    if isinstance(r[0], str) and r[1] is not None and r[2] is None:
        KV.setdefault(r[0], r[1])

# ---- Section B: sub-vehicle table -----------------------------------------
hdr = find_row("Sub-vehicle")
SV = []
i = hdr + 1
while rows[i][0] and rows[i][0] != "HOLDCO (cross-collateralised)":
    SV.append(rows[i]); i += 1
HOLDCO_ROW = rows[i]

# ---- Section C: grid -------------------------------------------------------
GRID = {}
for r in rows:
    if isinstance(r[0], str) and " — " in r[0] and r[0].endswith("-yr hold") and r[1] is not None:
        metric, hold = r[0].split(" — ")
        GRID[(metric, int(hold.split("-")[0]))] = r[1:6]

# ---- Section D: holdings + breakdowns --------------------------------------
hdr = find_row("Holding")
HOLD = []
i = hdr + 1
while rows[i][0] != "TOTAL":
    HOLD.append(dict(zip(["name", "subv", "check", "pct", "post", "own", "cagr", "sector", "region", "stage", "rank", "desc"], rows[i]))); i += 1
BREAK = {}
for key in ["SUB-VEHICLE BREAKDOWN", "SECTOR BREAKDOWN", "REGION BREAKDOWN", "STAGE / LIQUIDITY BREAKDOWN"]:
    s = find_row(key, startswith=True) + 2
    items = []
    while rows[s][0] != "Total":
        items.append((rows[s][0], rows[s][1], rows[s][2], rows[s][3])); s += 1
    BREAK[key] = items

holdco_size = KV["Holdco committed capital ($M)"]
n_hold = int(KV["Number of holdings"])
hold_mid = int(KV["Headline hold (yrs)"])
holds = sorted({h for (_, h) in GRID})
asof = KV["Figures as of"]
edition = KV["Fact sheet edition"]
fund_name = KV["Fund name"]
short = KV["Short name"]

# ---- formatting helpers ----------------------------------------------------
def pct(x, d=1, signed=False):
    if x is None: return "–"
    s = f"{x*100:.{d}f}%"
    return ("+" + s) if (signed and x > 0) else s
def mult(x, d=2): return "–" if x is None else f"{x:.{d}f}x"
def usd_m(x, d=0): return "–" if x is None else f"${x:,.{d}f}M"
def usd_big(x):
    if x >= 1000: return f"${x/1000:.2f}B".replace(".00B", "B")
    return f"${x:,.0f}M"
def sup(n): return f'<sup>({n})</sup>'

# ---- fonts -----------------------------------------------------------------
def font_face(family, weight, fn):
    p = os.path.join(FONTS, fn)
    with open(p, "rb") as f:
        b64 = base64.b64encode(f.read()).decode()
    return f"@font-face{{font-family:'{family}';font-weight:{weight};font-style:normal;src:url(data:font/ttf;base64,{b64}) format('truetype');}}"
def img64(fn):
    with open(os.path.join(FONTS, fn), "rb") as f:
        return "data:image/png;base64," + base64.b64encode(f.read()).decode()
LOGO = img64("leviathan_logo.png")
SIG = img64("signature.png")
FONT_CSS = "\n".join([
    font_face("LF", 400, "LibreFranklin-400.ttf"), font_face("LF", 500, "LibreFranklin-500.ttf"),
    font_face("LF", 600, "LibreFranklin-600.ttf"), font_face("LF", 700, "LibreFranklin-700.ttf"),
    font_face("SS", 400, "SourceSerif4-400.ttf"), font_face("SS", 600, "SourceSerif4-600.ttf"),
])

# ---- palette (sampled from the BXPE card) ----------------------------------
PAL = ["#4F9B86", "#1E5A4D", "#C7A17A", "#BFCFCB", "#CFCFCF", "#0E4F6D", "#A8C545", "#8FBFB6", "#7FB2C9", "#E3CDB5", "#6E8F89", "#B9D5CF"]
RUST = "#B85C2B"

# ---- SVG pie with leader labels (BXPE style) --------------------------------
def wrap_words(name, width=15):
    words, lines, cur = name.split(), [], ""
    for wd in words:
        if cur and len(cur) + 1 + len(wd) > width:
            lines.append(cur); cur = wd
        else:
            cur = (cur + " " + wd).strip()
    if cur: lines.append(cur)
    return lines

def pie(items, w=430, h=270, r=78):
    items = sorted([(k, v) for k, v, *_ in items if v and v > 0], key=lambda t: -t[1])
    if len(items) > 6:
        h = 330
    cx, cy = w / 2, h / 2 + 2
    total = sum(v for _, v in items)
    a = -math.pi / 2
    out = [f'<svg viewBox="0 0 {w} {h}" width="100%" xmlns="http://www.w3.org/2000/svg" font-family="LF" font-size="10.5">']
    labels = []
    for idx, (name, v) in enumerate(items):
        frac = v / total
        a2 = a + 2 * math.pi * frac
        x1, y1 = cx + r * math.cos(a), cy + r * math.sin(a)
        x2, y2 = cx + r * math.cos(a2), cy + r * math.sin(a2)
        large = 1 if frac > 0.5 else 0
        col = PAL[idx % len(PAL)]
        if frac >= 0.999:
            out.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{col}"/>')
        else:
            out.append(f'<path d="M{cx},{cy} L{x1:.2f},{y1:.2f} A{r},{r} 0 {large},1 {x2:.2f},{y2:.2f} Z" fill="{col}" stroke="#fff" stroke-width="1"/>')
        mid = (a + a2) / 2
        labels.append({"name": name, "pct": frac, "mid": mid, "side": 1 if math.cos(mid) >= 0 else -1})
        a = a2
    # resolve label collisions per side (each label = name lines + pct line)
    LH = 11.5
    for l in labels:
        l["lines"] = wrap_words(l["name"])
        l["h"] = LH * (len(l["lines"]) + 1)
    for side in (1, -1):
        L = [l for l in labels if l["side"] == side]
        for l in L:
            l["y"] = cy + (r + 22) * math.sin(l["mid"]) - l["h"] / 2   # top of label block
        L.sort(key=lambda l: l["y"])
        for k in range(1, len(L)):
            if L[k]["y"] < L[k - 1]["y"] + L[k - 1]["h"] + 4:
                L[k]["y"] = L[k - 1]["y"] + L[k - 1]["h"] + 4
        overflow = (L[-1]["y"] + L[-1]["h"]) - (h - 2) if L else 0
        if overflow > 0:
            for l in L: l["y"] -= overflow
        for k in range(len(L) - 2, -1, -1):
            if L[k]["y"] + L[k]["h"] + 4 > L[k + 1]["y"]:
                L[k]["y"] = L[k + 1]["y"] - L[k]["h"] - 4
        if L and L[0]["y"] < 2:
            shift = 2 - L[0]["y"]
            for l in L: l["y"] += shift
    for l in labels:
        side = l["side"]
        px, py = cx + r * math.cos(l["mid"]), cy + r * math.sin(l["mid"])
        ex = cx + (r + 12) * math.cos(l["mid"])
        ey = cy + (r + 12) * math.sin(l["mid"])
        lx = cx + side * (r + 26)
        ty = l["y"] + l["h"] / 2
        out.append(f'<polyline points="{px:.1f},{py:.1f} {ex:.1f},{ey:.1f} {lx:.1f},{ty:.1f}" fill="none" stroke="#333" stroke-width="0.8"/>')
        anchor = "start" if side == 1 else "end"
        tx = lx + side * 4
        y0 = l["y"] + LH - 2
        out.append(f'<text x="{tx:.1f}" y="{y0:.1f}" text-anchor="{anchor}" font-weight="700" fill="#111">' +
                   "".join(f'<tspan x="{tx:.1f}" dy="{0 if j == 0 else LH}">{ln}</tspan>' for j, ln in enumerate(l["lines"])) +
                   f'<tspan x="{tx:.1f}" dy="{LH}" font-weight="400">{l["pct"]*100:.0f}%</tspan></text>')
    out.append("</svg>")
    return "\n".join(out)

# ---- derived numbers -------------------------------------------------------
exp_irr = KV["Expected net IRR (headline hold)"]
exp_moic = KV["Expected net MOIC (headline hold)"]
base_irr = KV["Base-case net IRR (headline hold)"]
top10 = sorted(HOLD, key=lambda h: -h["check"])[:10]
top10_pct = sum(h["check"] for h in top10) / holdco_size
subv_names = {"Defense (Weapons sleeve)": "Defense", "IQT Semi / AI (IQT-mirror sleeve)": "IQT Semi / AI",
              "Consumer Discretionary (Consumer / Value sleeve)": "Consumer Discretionary"}
sv_by = {subv_names.get(r[0], r[0]): r for r in SV}
def svrow(name): return sv_by[name]
saronic = next(h for h in HOLD if h["name"] == "Saronic")
substrate = next(h for h in HOLD if "Substrate" in h["name"])
sv_colors = {"Defense": PAL[1], "IQT Semi / AI": PAL[0], "Consumer Discretionary": PAL[2]}
sleeve_tag = {"Defense": "Physical-layer defense effectors", "IQT Semi / AI": "IQT-mirror deep-tech & semiconductors", "Consumer Discretionary": "DTC, wellness & marketplaces · cohort-weighted TAM"}

# ---- HTML -------------------------------------------------------------------
CSS = f"""
{FONT_CSS}
@page {{ size: Letter; margin: 0; }}
* {{ box-sizing: border-box; }}
html, body {{ margin: 0; padding: 0; background: #fff; color: #111; font-family: 'LF', Arial, sans-serif; font-size: 9.5pt; line-height: 1.32; -webkit-print-color-adjust: exact; print-color-adjust: exact; }}
.page {{ width: 8.5in; height: 11in; padding: 0.42in 0.5in 0.38in 0.5in; position: relative; page-break-after: always; overflow: hidden; display: flex; flex-direction: column; }}
.page:last-child {{ page-break-after: auto; }}
.masthead {{ display: flex; justify-content: space-between; align-items: flex-start; }}
.logo {{ background: #000; color: #fff; font-family: 'SS', Georgia, serif; font-weight: 600; font-size: 21pt; padding: 10px 14px 9px; letter-spacing: 0.2px; margin-top: 44px; }}
.disc-top {{ width: 5.9in; text-align: right; font-size: 6.6pt; line-height: 1.35; color: #6f6f6f; text-transform: uppercase; letter-spacing: 0.15px; }}
.disc-top b {{ color: #333; }}
.ticker {{ font-family: 'SS', Georgia, serif; font-size: 15pt; text-align: right; margin-top: 10px; letter-spacing: 0.3px; }}
.rule {{ border-top: 3.2px solid #000; margin: 6px 0 8px; }}
.conf {{ text-align: right; color: #7a7a7a; font-size: 8.2pt; letter-spacing: 0.6px; text-transform: uppercase; margin-top: 2px; margin-bottom: 26px; }}
.date {{ font-weight: 700; font-size: 9.5pt; letter-spacing: 0.4px; margin-top: 4px; }}
h1 {{ font-family: 'SS', Georgia, serif; font-weight: 600; font-size: 25pt; line-height: 1.08; margin: 2px 0 8px; letter-spacing: -0.2px; }}
.lede {{ font-size: 11pt; color: #333; line-height: 1.3; margin-bottom: 14px; max-width: 7.2in; }}
.kpis {{ display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 0 18px; margin: 8px 0 14px; }}
.kpi .num {{ font-family: 'SS', Georgia, serif; font-weight: 400; font-size: 34pt; color: {RUST}; line-height: 1; letter-spacing: -0.5px; }}
.kpi .lab {{ font-size: 10pt; color: #111; margin-top: 6px; line-height: 1.25; }}
.kpi .sub {{ font-size: 8pt; color: #444; }}
h2 {{ font-family: 'SS', Georgia, serif; font-weight: 600; font-size: 15.5pt; margin: 0 0 2px; padding-top: 7px; border-top: 1px solid #999; line-height: 1.15; }}
h2.noline {{ border-top: 0; padding-top: 0; }}
h2 sup, h1 sup, .kpi sup, h3 sup {{ font-size: 55%; font-weight: 400; vertical-align: super; line-height: 0; }}
.subh {{ font-size: 9pt; color: #333; margin: 0 0 8px; }}
.cards {{ display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 16px; margin: 6px 0 16px; }}
.card .img {{ height: 118px; color: #fff; padding: 12px 13px; display: flex; flex-direction: column; justify-content: flex-end; position: relative; overflow: hidden; }}
.card .img .big {{ font-family: 'SS', Georgia, serif; font-size: 23pt; font-weight: 600; line-height: 1; }}
.card .img .small {{ font-size: 8.4pt; opacity: 0.92; margin-top: 4px; line-height: 1.25; }}
.card .img .stripe {{ position: absolute; right: -30px; top: -30px; width: 120px; height: 120px; border-radius: 50%; background: rgba(255,255,255,0.10); }}
.card .cap {{ font-weight: 700; font-size: 9.6pt; margin-top: 7px; }}
.card .cap span {{ font-weight: 400; color: #444; }}
table {{ border-collapse: collapse; width: 100%; font-size: 8.9pt; }}
th {{ background: #000; color: #fff; font-weight: 700; text-align: center; padding: 6px 7px; font-size: 8.9pt; }}
th:first-child, td:first-child {{ text-align: left; }}
td {{ padding: 5.5px 7px; text-align: center; border-bottom: 1px solid #fff; }}
tr:nth-child(even) td {{ background: #E8E8E8; }}
td.b, th.b {{ font-weight: 700; }}
table.tight td {{ padding: 4px 6px; }}
table.lastline tr:last-child td {{ border-bottom: 1.2px solid #000; }}
.spacer {{ flex: 1; }}
.fine {{ font-size: 7.6pt; color: #333; line-height: 1.32; text-align: justify; margin-top: 6px; }}
.fine b {{ color: #000; }}
.fine p {{ margin: 0 0 5px; }}
.fine .note {{ border-top: 1px solid #000; padding-top: 5px; margin-top: 6px; }}
.footer {{ display: flex; justify-content: space-between; font-size: 7.4pt; color: #222; margin-top: 10px; }}
.footer .r {{ text-align: right; }}
.footer .id {{ font-family: 'SS', Georgia, serif; font-size: 8.4pt; letter-spacing: 0.4px; margin-top: 2px; }}
.stats3 {{ display: grid; grid-template-columns: 1fr 1fr 1fr; margin: 10px 0 16px; }}
.stats3 .num {{ font-family: 'SS', Georgia, serif; font-size: 34pt; line-height: 1; letter-spacing: -0.5px; }}
.stats3 .lab {{ font-size: 10pt; margin-top: 6px; }}
.grid2 {{ display: grid; grid-template-columns: 1fr 1fr; gap: 10px 26px; }}
.grid2 h3 {{ font-family: 'SS', Georgia, serif; font-weight: 600; font-size: 14pt; margin: 0; line-height: 1.15; }}
.grid2 .subh {{ margin-bottom: 0; }}
.pillar {{ margin: 10px 0 4px; font-size: 10.5pt; }}
.pillar b {{ font-weight: 700; }}
.bar {{ border-left: 4px solid {PAL[0]}; padding-left: 10px; margin: 6px 0 14px 4px; font-size: 10pt; }}
.spot {{ display: flex; justify-content: space-between; align-items: flex-start; border-top: 1px solid #999; padding-top: 10px; }}
.spot h3 {{ font-weight: 700; font-size: 10.5pt; margin: 2px 0 6px; }}
.spot .logo2 {{ font-family: 'SS', Georgia, serif; font-weight: 600; font-size: 13pt; color: {PAL[1]}; border: 2px solid {PAL[1]}; padding: 6px 12px; letter-spacing: 1px; text-transform: uppercase; }}
.spot-body {{ display: grid; grid-template-columns: 1.55in 1fr; gap: 22px; margin: 10px 0 18px; }}
.bignum {{ font-family: 'SS', Georgia, serif; font-size: 23pt; color: {RUST}; line-height: 1; margin-top: 4px; }}
.bignum + .lab {{ font-size: 8.6pt; margin: 3px 0 14px; }}
.dots {{ list-style: none; padding: 0; margin: 2px 0 0; }}
.dots li {{ position: relative; padding-left: 26px; margin-bottom: 9px; font-size: 9.6pt; line-height: 1.3; }}
.dots li:before {{ content: ''; position: absolute; left: 0; top: 4px; width: 9px; height: 9px; border-radius: 50%; background: {PAL[0]}; }}
.dots li:after {{ content: ''; position: absolute; left: 11px; top: 8px; width: 9px; border-top: 1.2px solid #333; }}
.dots li:nth-child(2):before {{ background: {PAL[3]}; }}
.dots li:nth-child(3):before {{ background: {PAL[1]}; }}
.sq {{ display: inline-block; width: 5px; height: 5px; background: {RUST}; margin: 0 7px 2px 0; }}
.cover {{ justify-content: center; align-items: center; text-align: center; }}
.cover img {{ width: 4.2in; }}
.cover .t1 {{ font-family: 'SS', Georgia, serif; font-weight: 600; font-size: 22pt; margin-top: 30px; line-height: 1.15; }}
.cover .t2 {{ font-size: 11.5pt; color: #333; margin-top: 8px; }}
.cover .t3 {{ font-size: 9pt; color: #7a7a7a; letter-spacing: 1.2px; text-transform: uppercase; margin-top: 34px; }}
.cover .rule2 {{ width: 1.2in; border-top: 3px solid #000; margin: 26px auto 0; }}
.cover .bottom {{ position: absolute; bottom: 0.5in; left: 0.5in; right: 0.5in; font-size: 7.4pt; color: #555; text-align: left; line-height: 1.35; }}
.memo {{ font-size: 9.6pt; line-height: 1.38; }}
.memo h2 {{ border-top: 0; padding-top: 0; font-size: 17pt; margin-bottom: 2px; }}
.memo .meta {{ font-size: 8.4pt; color: #555; margin-bottom: 10px; letter-spacing: 0.3px; }}
.memo p {{ margin: 0 0 8px; text-align: justify; }}
.memo h4 {{ font-family: 'SS', Georgia, serif; font-weight: 600; font-size: 11.5pt; margin: 10px 0 3px; color: #111; }}
.memo h4 span {{ color: {RUST}; }}
.memo .sig {{ margin-top: 10px; }}
.memo .sig img {{ height: 0.75in; display: block; margin: 2px 0 0 -6px; }}
.memo .sig .name {{ font-weight: 700; font-size: 9.6pt; margin-top: 2px; }}
.memo .sig .title {{ font-size: 8.6pt; color: #444; }}
.terms td {{ text-align: left; vertical-align: top; }}
.terms td:first-child {{ font-weight: 700; width: 1.5in; }}
.terms th {{ text-align: left; }}
.end {{ column-count: 2; column-gap: 24px; font-size: 7.6pt; line-height: 1.33; text-align: justify; }}
.end p {{ margin: 0 0 6px; }}
.end .n {{ display: inline-block; width: 22px; }}
.gloss td {{ text-align: left; vertical-align: top; font-size: 8.2pt; }}
.gloss td:first-child {{ font-weight: 700; width: 1.7in; }}
"""

def masthead_p1():
    return f"""
<div class="masthead">
  <img src="{LOGO}" alt="Leviathan" style="height:0.9in;margin-top:12px">
  <div>
    <div class="disc-top"><b>This is an internal investment-committee planning document.</b> It is a model-based illustration prepared for Leviathan's
    principals and advisers. Figures are modelled outcomes, not realised performance, and do not constitute an offer, a solicitation or investment advice.
    Not for distribution to clients or the general public.</div>
    <div class="ticker">{short}</div>
  </div>
</div>
<div class="rule"></div>"""

def masthead_pn():
    return '<div class="conf">Highly confidential &amp; trade secret</div><div class="rule" style="margin-top:0"></div>'

def footer(n):
    return f"""<div class="footer"><div>{edition} {short} Update</div>
<div class="r">Leviathan&nbsp;&nbsp;|&nbsp;&nbsp;{n}<div class="id">LEVIATHAN-{short}-V3-{asof.replace('-', '').upper()}</div></div></div>"""

# ---------------- page 1 -----------------
perf_rows = ""
for nm in ["Defense", "IQT Semi / AI", "Consumer Discretionary"]:
    r = svrow(nm)
    perf_rows += f"<tr><td class='b'>{nm}</td><td>{usd_m(r[1])}</td><td>{pct(r[2],0)}</td><td>{int(r[3])}</td><td>{mult(r[4])}</td><td>{pct(r[6])}</td><td>{pct(r[7])}</td><td>{pct(r[8])}</td><td>{pct(r[9])}</td><td class='b'>{pct(r[10])}</td></tr>"
h = HOLDCO_ROW
perf_rows += f"<tr><td class='b'>{short} Holdco (cross-collateralised)</td><td class='b'>{usd_m(h[1])}</td><td class='b'>100%</td><td class='b'>{int(h[3])}</td><td class='b'>{mult(h[4])}</td><td class='b'>{pct(h[6])}</td><td class='b'>{pct(h[7])}</td><td class='b'>{pct(h[8])}</td><td class='b'>{pct(h[9])}</td><td class='b'>{pct(h[10])}</td></tr>"

cards = ""
for nm, size_key in [("Defense", "Wpn"), ("IQT Semi / AI", "IQT"), ("Consumer Discretionary", "Con")]:
    r = svrow(nm)
    cards += f"""<div class="card"><div class="img" style="background:{sv_colors[nm]}"><div class="stripe"></div>
      <div class="big">{usd_m(r[1])}</div><div class="small">{sleeve_tag[nm]} · {int(r[3])} holdings · {pct(r[2],0)} of holdco</div></div>
      <div class="cap">{nm} <span>— {r[13]}</span></div></div>"""

page1 = f"""
<div class="page">
{masthead_p1()}
<div class="date">{edition.upper()}</div>
<h1>{fund_name} (“{short}”)</h1>
<div class="lede">{short} is a {usd_m(holdco_size)} three-sleeve private equity holding vehicle that gives Leviathan's principals exposure to the
defense supercycle, the In-Q-Tel-mirror semiconductor / AI stack and a consumer-discretionary ballast{sup(1)} through a single commitment.</div>
<div class="kpis">
  <div class="kpi"><div class="num">{usd_m(holdco_size)}</div><div class="lab">holdco committed capital</div><div class="sub">three sub-vehicles, {n_hold} holdings</div></div>
  <div class="kpi"><div class="num">{pct(exp_irr)}</div><div class="lab">expected net IRR to LPs<br><span class="sub">(probability-weighted, {hold_mid}-year hold){sup(2)}</span></div></div>
  <div class="kpi"><div class="num">{mult(exp_moic)}</div><div class="lab">expected net MOIC / DPI at exit<br><span class="sub">({hold_mid}-year hold){sup(2)}</span></div></div>
</div>
<h2>Sub-Vehicle Spotlight{sup(3)}</h2>
<div class="cards">{cards}</div>
<h2>Performance Summary{sup(4)}</h2>
<div class="subh">(net IRR to LPs by scenario, {hold_mid}-year hold; MOIC gross of fees, Base case)</div>
<table class="lastline">
<tr><th>Sub-vehicle</th><th>Committed</th><th>% Holdco</th><th>Holdings</th><th>Gross MOIC</th><th>Base</th><th>Bull</th><th>Bear</th><th>TSMC-Shock</th><th>Expected</th></tr>
{perf_rows}
</table>
<div class="spacer"></div>
<div class="fine">
<p>Please reference page 4 for the full scenario tables. See “Modelled Returns” on page 6 for how net figures are derived. Sub-vehicle rows are stand-alone waterfalls; the holdco row nets the three sleeves under one preferred return and one carry.</p>
<p><b>Modelled outcomes are not forecasts and do not predict future returns.</b> All figures are outputs of Leviathan's internal IC model as of {asof}. Six of the nine IQT-sleeve entry marks and most Weapons-sleeve marks are estimates pending primary cap-table access; the TSMC-Shock case is a deliberately low-probability tail. Investment examples are shown for illustration and may not be representative of the vehicle's eventual portfolio.</p>
<p class="note">Note: Please refer to pages 5–6 for key terms, sourcing and endnotes 1–12. For a more detailed description of the model's wiring, assumptions and caveats, refer to the Read Me, Checks and Change Log tabs of the v3 workbook.</p>
</div>
{footer(1)}
</div>"""

# ---------------- page 2 -----------------
pies = ""
for title_, key, n in [("Sub-Vehicle Breakdown", "SUB-VEHICLE BREAKDOWN", 5), ("Sector Breakdown", "SECTOR BREAKDOWN", 6),
                       ("Regional Breakdown", "REGION BREAKDOWN", 7), ("Stage &amp; Liquidity Breakdown", "STAGE / LIQUIDITY BREAKDOWN", 8)]:
    items = [(k, v) for k, v, p_, c_ in BREAK[key]]
    pies += f"<div><h3>{title_}{sup(n)}</h3><div class='subh'>(% of committed capital){sup(9)}</div>{pie(items)}</div>"
n_scen = int(KV["Scenarios modelled"])
page2 = f"""
<div class="page">
{masthead_pn()}
<h2 class="noline">{short}'s Scaled and Diversified Portfolio</h2>
<div class="stats3">
  <div><div class="num">3</div><div class="lab">sub-vehicles<sup>(i)</sup></div></div>
  <div><div class="num">{n_hold}</div><div class="lab">portfolio holdings<sup>(ii)</sup></div></div>
  <div><div class="num">{n_scen}</div><div class="lab">return scenarios underwritten<sup>(iii)</sup></div></div>
</div>
<div class="grid2">{pies}</div>
<div class="spacer"></div>
<div class="fine">
<p>There can be no assurance that {short} will achieve its objectives, avoid substantial losses or source or execute transactions relating to the above themes. Several positions are access-constrained (employee-owned, closely held, IPO-pending or secondary-only) and the final allocation may differ materially from the modelled book. Diversification does not ensure a profit or protect against losses. Sector, regional and stage classifications are Leviathan's own and are made in its sole discretion.</p>
<p class="note">Note: Financial data is modelled and unaudited. Please refer to pages 5–6 for key terms and endnotes 1–12. (i) Defense (Weapons sleeve), IQT Semi / AI (IQT-mirror sleeve) and Consumer Discretionary (Consumer / Value sleeve). (ii) {n_hold} named holdings across the three sleeves; checks sum to exactly {usd_m(holdco_size)}. (iii) Base, Bull, Bear and TSMC-Shock, weighted {KV['Scenario weights Base / Bull / Bear / Shock']} to form the Expected case.</p>
</div>
{footer(2)}
</div>"""

# ---------------- page 3 -----------------
top_rows = ""
for hld in top10:
    top_rows += f"<tr><td class='b'>{hld['name'].replace(' (anchor)', '')}</td><td>{hld['subv']}</td><td>{usd_m(hld['check'], 1)}</td><td style='text-align:left'>{hld['desc']}</td></tr>"
page3 = f"""
<div class="page">
{masthead_pn()}
<h2 class="noline">Leviathan's Thematic Pillar Spotlight: Defense Supercycle{sup(3)}{sup(10)}</h2>
<div class="pillar"><b>Defense Supercycle</b> anchors the holdco in the two sleeves that are long the geopolitical cycle: physical-layer effectors and the semiconductor / AI stack beneath them</div>
<div class="bar"><b>Weapons:</b> cash-generative defense opex — munitions, autonomy, directed energy and counter-drone demand pulled by NATO's 5%-of-GDP pledge and US replenishment budgets; each name's CAGR carries a munitions-shortage / FMS-backlog overlay{sup(10)}</div>
<div class="spot">
  <div><h3>Spotlight: Saronic</h3>
  <div><span class="sq"></span>Investment in a leading autonomous naval-surface-vessel platform scaling under the US Navy's Replicator programme</div></div>
  <div class="logo2">Saronic</div>
</div>
<div class="spot-body">
  <div>
    <div class="bignum">{usd_big(saronic['post'])}</div><div class="lab">entry post-money valuation (Series D, Mar-26)</div>
    <div class="bignum">{usd_m(saronic['check'])}</div><div class="lab">{short} check — largest position in the holdco ({pct(saronic['pct'])} of committed capital)</div>
  </div>
  <ul class="dots">
    <li>Naval autonomy is among the fastest-growing defense budget lines; the company's 2025 revenue scaled roughly 15x year-on-year</li>
    <li>Modelled at a {pct(saronic['cagr'],0)} Base-case gross CAGR, with the TSMC-Shock case re-rating conflict-driven demand higher</li>
    <li>Ownership kept deliberately small ({pct(saronic['own'])}) given the late entry mark; value creation comes from programme-of-record wins and a public-market exit window</li>
  </ul>
</div>
<h2>Top 10 Largest Positions{sup(11)}</h2>
<div class="subh">Represents ~{top10_pct*100:.0f}% of committed capital</div>
<table class="lastline tight">
<tr><th>Investment</th><th>Sub-vehicle</th><th>Check</th><th style="text-align:left">Description</th></tr>
{top_rows}
</table>
<div class="spacer"></div>
<div class="fine">
<p>There can be no assurance that any Leviathan vehicle or investment will achieve its objectives or avoid substantial losses, or that Leviathan will source or execute transactions relating to the above themes and opportunities. The investment examples presented herein are modelled target positions, several of which depend on secondary, tender, cornerstone or block access that has not been secured. There is no assurance that the trends described herein will continue or will not reverse.</p>
<p class="note">Note: Entry marks are as of {asof} and reflect the latest priced round, live secondary quote or Leviathan estimate as flagged in the model. Please refer to pages 5–6 for key terms and endnotes.</p>
</div>
{footer(3)}
</div>"""

# ---------------- page 4 -----------------
def grid_table(metric, fmt, hdr_first):
    out = f"<tr><th>{hdr_first}</th><th>Base</th><th>Bull</th><th>Bear</th><th>TSMC-Shock</th><th class='b'>Expected</th></tr>"
    for hd in holds:
        v = GRID[(metric, hd)]
        out += f"<tr><td class='b'>{hd}-year hold</td>" + "".join(f"<td{' class=b' if k == 4 else ''}>{fmt(x)}</td>" for k, x in enumerate(v)) + "</tr>"
    return out
sv_scen = ""
for nm in ["Defense", "IQT Semi / AI", "Consumer Discretionary"]:
    r = svrow(nm)
    sv_scen += f"<tr><td class='b'>{nm}</td><td>{pct(r[6])}</td><td>{pct(r[7])}</td><td>{pct(r[8])}</td><td>{pct(r[9])}</td><td class='b'>{pct(r[10])}</td><td>{mult(r[11])}</td><td>{mult(r[12])}</td></tr>"
sv_scen += f"<tr><td class='b'>{short} Holdco</td><td>{pct(h[6])}</td><td>{pct(h[7])}</td><td>{pct(h[8])}</td><td>{pct(h[9])}</td><td class='b'>{pct(h[10])}</td><td>{mult(h[11])}</td><td>{mult(h[12])}</td></tr>"
pme_rows = ""
for hd in holds:
    pme_rows += (f"<tr><td class='b'>{hd}-year hold</td><td>{mult(GRID[('Net KS-PME vs SPX', hd)][4])}</td>"
                 f"<td>{mult(GRID[('Net KS-PME vs NDX', hd)][4])}</td><td>{mult(GRID[('Net KS-PME vs Defense+Semis basket', hd)][4])}</td>"
                 f"<td>{mult(GRID[('Gross MOIC', hd)][4])}</td><td>{mult(GRID[('Net MOIC', hd)][4])}</td><td>{usd_m(GRID[('Net proceeds ($M)', hd)][4],1)}</td></tr>")
page4 = f"""
<div class="page">
{masthead_pn()}
<h2 class="noline">Modelled Net Return{sup(4)}</h2>
<div class="subh">(net IRR to LPs, % per annum, after management fee, preferred return and carried interest)</div>
<table class="lastline">{grid_table('Net IRR', pct, 'Holdco')}</table>
<h2 style="margin-top:16px">Net Multiple of Invested Capital</h2>
<div class="subh">(net MOIC to LPs; paid-in assumed fully drawn, so DPI = TVPI at exit)</div>
<table class="lastline">{grid_table('Net MOIC', mult, 'Holdco')}</table>
<h2 style="margin-top:16px">Sub-Vehicle Net Returns, {hold_mid}-Year Hold</h2>
<div class="subh">(stand-alone sleeve waterfalls; holdco row is cross-collateralised)</div>
<table class="lastline">
<tr><th>Sub-vehicle</th><th>Base</th><th>Bull</th><th>Bear</th><th>TSMC-Shock</th><th class='b'>Expected IRR</th><th>Expected MOIC</th><th>KS-PME vs S&amp;P</th></tr>
{sv_scen}</table>
<h2 style="margin-top:16px">Public-Market Equivalent &amp; Proceeds — Expected Case{sup(2)}</h2>
<div class="subh">(Kaplan-Schoar PME &gt; 1.00x = beats the index; benchmarks {pct(KV['S&P 500 benchmark CAGR'],1)} S&amp;P 500, {pct(KV['Nasdaq-100 benchmark CAGR'],1)} Nasdaq-100, {pct(KV['Defense+Semis basket CAGR (fwd)'],1)} Defense+Semis basket)</div>
<table class="lastline">
<tr><th>Holdco</th><th>vs S&amp;P 500</th><th>vs Nasdaq-100</th><th>vs Defense+Semis</th><th>Gross MOIC</th><th>Net MOIC</th><th>Net proceeds</th></tr>
{pme_rows}</table>
<div class="spacer"></div>
<div class="fine">
<p><b>Modelled outcomes do not predict future returns.</b> Returns are single-terminal-exit illustrations: proceeds = check × (1 + CAGR)^hold × retention, with fees charged on committed capital over the full hold and a whole-fund European waterfall with no GP catch-up. IRRs are therefore annualised multiples, not cash-flow IRRs, and will differ from realised figures once capital is drawn and distributed over time.</p>
<p class="note">Note: Financial data is modelled and unaudited and sourced from Leviathan's internal IC model (v3, {asof}). Expected = probability-weighted across the four scenarios at the weights shown on page 5.</p>
</div>
{footer(4)}
</div>"""

# ---------------- page 5 -----------------
T = KV
page5 = f"""
<div class="page">
{masthead_pn()}
<h2 class="noline">Summary of Key Terms</h2>
<table class="terms lastline">
<tr><th>Key Terms</th><th>Description</th></tr>
<tr><td>Vehicle</td><td><span class="sq"></span>{fund_name}: a {usd_m(holdco_size)} holding company owning three sub-vehicles, modelled on a committed-capital basis{sup(1)}</td></tr>
<tr><td>Sub-vehicles</td><td><span class="sq"></span>Defense (Weapons sleeve, {usd_m(svrow('Defense')[1])}) · IQT Semi / AI (IQT-mirror sleeve, {usd_m(svrow('IQT Semi / AI')[1])}) · Consumer Discretionary (Consumer / Value sleeve, {usd_m(svrow('Consumer Discretionary')[1])})</td></tr>
<tr><td>Hold periods</td><td><span class="sq"></span>{T['Hold periods modelled (yrs)']} years modelled; the {hold_mid}-year vehicle is the recommended underwriting case<br><span class="sq"></span>Follow-on reserve of {usd_m(T['IQT follow-on reserve ($M)'])} within the IQT sleeve, steered pro-rata to Substrate, EUV Tech and EdgeCortix</td></tr>
<tr><td>Dilution / retention{sup(5)}</td><td><span class="sq"></span>Ownership retained at short / mid / long hold — IQT {T['IQT retention @ short / mid / long']}; Weapons {T['Weapons retention @ short / mid / long']}; Consumer {T['Consumer retention @ short / mid / long']}</td></tr>
<tr><td>Scenario weights{sup(2)}</td><td><span class="sq"></span>Base / Bull / Bear / TSMC-Shock = {T['Scenario weights Base / Bull / Bear / Shock']}<br><span class="sq"></span>TSMC-Shock CAGRs for the IQT sleeve are derived from a five-axis strategic score (China-race criticality, Taiwan insulation, government embeddedness, CFIUS-clean sovereignty, chokepoint leverage)</td></tr>
<tr><td>Cohort overlay{sup(12)}</td><td><span class="sq"></span>Consumer-sleeve CAGRs carry a demographic cohort-exposure uplift: TAM scored 0–5 per name across prime-earning (35–54), entering-prime (22–34) and retiring-boomer (60+) cohorts, weighted {T['Consumer cohort weights prime / entering / boomer']}, at {T['Consumer cohort uplift per point Base / Bull / Bear / Shock']} per point (Base / Bull / Bear / Shock); average exposure score {T['Consumer avg cohort exposure score']:.1f}</td></tr>
<tr><td>Benchmarks</td><td><span class="sq"></span>S&amp;P 500 {pct(T['S&P 500 benchmark CAGR'])}, Nasdaq-100 {pct(T['Nasdaq-100 benchmark CAGR'])}, Defense+Semis thematic basket {pct(T['Defense+Semis basket CAGR (fwd)'])} forward (50/50 ITA/SOXX, tempered from a ~26% trailing five-year blend)</td></tr>
<tr><td>Reference currency</td><td><span class="sq"></span>USD; all figures in USD millions unless noted</td></tr>
</table>
<br>
<table class="terms lastline">
<tr><th>Costs</th><th style="width:1.9in">Fees</th><th>Terms applied in the model</th></tr>
<tr><td>Ongoing costs</td><td>Management fee</td><td><span class="sq"></span>{pct(T['Management fee (% committed / yr)'])} per annum of committed capital, charged over the full hold</td></tr>
<tr><td></td><td>Preferred return</td><td><span class="sq"></span>{pct(T['Preferred return (compounded)'],0)} per annum, compounded, returned to LPs before any carry</td></tr>
<tr><td>Incidental costs</td><td>Carried interest</td><td><span class="sq"></span>{pct(T['Carried interest'],0)} of profits above the preferred return; {T['Waterfall']}</td></tr>
<tr><td>Not modelled</td><td>Organisational, transaction and secondary-access costs</td><td><span class="sq"></span>Excluded; a feeder or SPV wrapper for access-constrained names would add a layer of cost not reflected here</td></tr>
</table>
<div class="spacer"></div>
<div class="fine">
<p>The sub-vehicle figures on pages 1 and 4 apply the same fee, preferred-return and carry terms to each sleeve on a stand-alone basis. The holdco figures net the three sleeves under a single waterfall, so strong sleeves offset weak ones before carry is charged; the difference is reported on the Sleeve Economics tab of the model as the cross-sleeve netting effect.</p>
<p class="note">Note: The information above is a summary of the terms as modelled only and is qualified in its entirety by the governing documents of any vehicle ultimately formed. Capitalised terms not defined have the meanings given in the model's Read Me tab.</p>
</div>
{footer(5)}
</div>"""

# ---------------- page 6 -----------------
w = T['Scenario weights Base / Bull / Bear / Shock']
page6 = f"""
<div class="page">
{masthead_pn()}
<h2 class="noline" style="font-size:12pt">Endnotes</h2>
<div class="end">
<p>Note: All figures presented are as of {asof} unless otherwise indicated and are outputs of the Leviathan Core PE Holdco model, v3 optimisation pass dated 02-Oct-2026. “{short}”, “the holdco” and “the vehicle” refer to {fund_name}. Leviathan runs four vehicles (~$1.5B AUM in total); this fact sheet covers only the core PE holdco and its three sub-vehicles.</p>
<p><span class="n">(1)</span>Committed-capital basis. Paid-in capital is assumed fully drawn at inception, so Net DPI equals Net MOIC and RVPI is zero at exit (TVPI = DPI).</p>
<p><span class="n">(2)</span>“Expected” figures are probability-weighted across the four scenarios (Base / Bull / Bear / TSMC-Shock = {w}). Each line of the net waterfall is weighted separately and ratios are then derived from the weighted net proceeds, so Expected net figures are the expected value of LP proceeds rather than the waterfall applied to expected gross proceeds. Headline figures use the {hold_mid}-year hold.</p>
<p><span class="n">(3)</span>The sub-vehicle and investment examples presented reflect the modelled target book as of {asof}. They are shown to illustrate the vehicle's themes and are not a representation that any position will be acquired on the modelled terms. Several names require secondary, tender, cornerstone or block access that has not been secured.</p>
<p><span class="n">(4)</span>Net returns are after a {pct(T['Management fee (% committed / yr)'])} management fee on committed capital over the full hold, an {pct(T['Preferred return (compounded)'],0)} compounded preferred return and {pct(T['Carried interest'],0)} carried interest under a whole-fund European waterfall with no GP catch-up. Gross and net IRRs are annualised multiples ((proceeds / capital)^(1/hold) − 1), not cash-flow IRRs; a wipe-out is shown as −100%.</p>
<p><span class="n">(5)</span>Retention is the share of entry ownership kept after follow-on dilution, applied to exit proceeds, and is set per sleeve and per hold.</p>
<p><span class="n">(6)</span>“Sector Breakdown” groups holdings into Leviathan's ten thematic sectors by committed check. Classifications are made in Leviathan's sole discretion; different criteria could result in materially different classifications.</p>
<p><span class="n">(7)</span>“Regional Breakdown” is by principal place of business. DefendEye (US HQ, Polish manufacturing, EU cap table) is classified North America. Allied-nation names (EdgeCortix, Diraq) are minority-only positions.</p>
<p><span class="n">(8)</span>“Stage &amp; Liquidity Breakdown” reflects the entry route: listed shares, pre-IPO / IPO-track names, late-stage private rounds, tenders and secondaries, growth-stage primaries, and seed / early rounds.</p>
<p><span class="n">(9)</span>Represents {short}'s modelled committed capital of {usd_m(holdco_size)}; all breakdowns are percentages of that total and may not sum to 100% due to rounding.</p>
<p><span class="n">(10)</span>“Thematic Pillar” is selected from the drivers set out on the model's Macro Overlay tab (NATO 5%-of-GDP pledge, US munitions and autonomy budgets, classified / black-budget growth, China decoupling and CHIPS reshoring). Saronic entry mark: Series D, March 2026, $9.25B post-money; 2025 revenue of approximately $200M. Weapons-sleeve CAGRs are the base assumptions plus an exposure-score uplift (average of munitions-shortage and FMS / export-backlog scores, 0–5) at per-point rates set on the Weapons Sleeve tab.</p>
<p><span class="n">(11)</span>Top 10 positions are the ten largest modelled checks by committed capital and are listed in descending order of check size.</p>
<p><span class="n">(12)</span>The cohort overlay mirrors the Weapons-sleeve munitions / FMS overlay. Scores reflect Leviathan's judgment of each name's addressable market across cohorts in or entering their prime earning years while retaining boomer TAM through retirement; they are levers, not facts. The two defense sleeves (IQT Semi / AI and Defense) are deliberately co-exposed to the same driver, US insulation of the semiconductor / AI supply chain and munitions production scale, so roughly {pct(svrow('Defense')[2]+svrow('IQT Semi / AI')[2],0)} of committed capital moves on one macro factor; the Consumer sleeve is the uncorrelated ballast.</p>
<p><b>Modelled returns.</b> The model compounds a per-name CAGR over a single terminal exit; it does not model interim cash flows, recycling, credit facilities, FX, taxes or organisational expenses. Six of nine IQT-sleeve entry marks and most Weapons-sleeve marks are estimates pending primary cap-table access; two Consumer-sleeve marks (Made In Cookware, Plunge) have no market reference and Goat Group's last priced round is from June 2021. The TSMC-Shock case is a deliberately low-probability tail whose compounded CAGRs produce very large multiples by design; its weight should be kept honest.</p>
<p><b>Important disclosure.</b> This material is prepared solely for Leviathan's investment committee and professional advisers and must not be reproduced or distributed to any other person. It is not an offer to sell or a solicitation of an offer to buy any security, and nothing herein is investment, legal or tax advice. Alternative investments are speculative, typically carry higher fees, are illiquid, may employ leverage and involve a high degree of risk, including the possible loss of the entire investment. Opinions expressed are those of Leviathan as of the date hereof and are subject to change without notice. Visual design of this document follows a conventional institutional fact-card layout; it is not affiliated with, endorsed by or derived from any third-party manager's materials.</p>
</div>
<div class="spacer"></div>
{footer(6)}
</div>"""

cover = f"""
<div class="page cover">
  <img src="{LOGO}" alt="Leviathan">
  <div class="rule2"></div>
  <div class="t1">{fund_name}<br>(“{short}”)</div>
  <div class="t2">Fact Sheet &nbsp;·&nbsp; {edition} Update</div>
  <div class="t3">Internal investment-committee planning document &nbsp;·&nbsp; Highly confidential &amp; trade secret</div>
  <div class="bottom">Figures as of {asof}, from the Leviathan Core PE Holdco model (v3). Modelled outcomes are not forecasts and do not predict future returns. Not an offer, a solicitation or investment advice. Not for distribution to clients or the general public.</div>
</div>"""
d, q, c = svrow('Defense'), svrow('IQT Semi / AI'), svrow('Consumer Discretionary')
defense_share = d[2] + q[2]
memo = f"""
<div class="page memo">
{masthead_pn()}
<h2>A Letter to Our Investors</h2>
<div class="meta">{edition.upper()} &nbsp;·&nbsp; FROM THE DESK OF DONALD BRITTS III &nbsp;·&nbsp; {fund_name} (“{short}”)</div>
<p>The world is re-industrialising around two imperatives: the United States must insulate its semiconductor and artificial-intelligence supply chain from a single point of failure in the Taiwan Strait, and the West must rebuild the capacity to produce weapons and munitions at scale. Those two imperatives are one trend viewed from two angles, and {short} is built to own both legs of it while a third sleeve compounds on the most durable force in any economy: the household balance sheet. Across {n_hold} holdings and {usd_m(holdco_size)} of committed capital, our model points to a {pct(exp_irr)} probability-weighted net IRR and a {mult(exp_moic)} net multiple over a {hold_mid}-year hold, beating the public defense-and-semiconductor basket on a public-market-equivalent basis in every scenario we underwrite.</p>
<h4><span>I.</span> IQT Semi / AI — the sovereign chokepoints ({usd_m(q[1])}, {pct(q[2],0)})</h4>
<p>Nine names, anchored by Substrate, mirror the In-Q-Tel playbook: own the nodes a nation cannot do without if Taiwan goes dark. Domestic X-ray lithography, at-wavelength EUV metrology, substrate materials that break a single-supplier monopoly, edge-AI silicon that works when the cloud is jammed, and quantum compute built on existing CMOS lines. Every name is scored on five strategic axes, and that score drives its re-rating in a TSMC-Shock. This is the convex leg of the book: it earns a {pct(q[6])} base-case net IRR and {pct(q[9])} in the shock case precisely because the names we hold are the ones Washington will pay any price for.</p>
<h4><span>II.</span> Defense — the physical effectors ({usd_m(d[1])}, {pct(d[2],0)})</h4>
<p>If the IQT sleeve is the brain, the Weapons sleeve is the hands. Naval autonomy, directed energy, energetics, missile forgings and the primes that integrate them are the beneficiaries of NATO's five-percent pledge and an American munitions base that has been drawn down to levels not seen in generations. Each position carries an explicit munitions-shortage and foreign-military-sales backlog score that lifts its growth path. The sleeve is the cash-generative core of the holdco: {pct(d[6])} base-case net, {pct(d[10])} expected, and a {mult(d[12])} public-market equivalent against the S&amp;P 500.</p>
<h4><span>III.</span> Consumer Discretionary — the demographic engine ({usd_m(c[1])}, {pct(c[2],0)})</h4>
<p>Our consumer sleeve is not a bet on the consumer; it is a bet on <i>which</i> consumer. Every name is scored on its addressable market across the cohorts in or entering their prime earning years, while deliberately retaining exposure to the baby boomers as they carry the largest wealth transfer in history into retirement. Direct-to-consumer essentials, wearable health, membership grocery, fresh pet food, payments and marketplaces: businesses that sell to every cohort and scale with the one that is spending. It is the sleeve that pays distributions first, at a {pct(c[6])} base-case net IRR, and the one that is uncorrelated with everything else we own.</p>
<h4><span>IV.</span> Why the three belong together</h4>
<p>The IQT and Defense sleeves are intentionally correlated. Semiconductor insulation and munitions scale are funded by the same appropriations, driven by the same adversary and accelerated by the same shock. Together they are {pct(defense_share,0)} of the holdco and move as one factor, which is the point: we want maximum exposure to the sovereign-capital supercycle, and we want the two legs to reinforce each other operationally. Edge-AI silicon from the first sleeve goes into the autonomous vessels and counter-drone systems of the second; the primes in the second are the natural acquirers of the first. The consumer sleeve sits apart from that factor by design. It provides early DPI, lowers dispersion, and in the one scenario that hurts it, a Taiwan shock, the other two sleeves more than compensate, which is why the holdco's expected net return rises in that case rather than falls. One factor for conviction, one ballast for durability, and a single waterfall that lets the strong sleeves carry the weak before any carry is charged. That is {short}.</p>
<div class="sig"><img src="{SIG}" alt="signature"><div class="name">Donald Britts III</div><div class="title">Leviathan &nbsp;·&nbsp; Miami · London · Zurich · Tokyo</div></div>
<div class="spacer"></div>
<div class="footer"><div>{edition} {short} Update</div><div class="r">Leviathan</div></div>
</div>"""
html = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><title>{short} Fact Sheet — {edition}</title><style>{CSS}</style></head>
<body>{cover}{memo}{page1}{page2}{page3}{page4}{page5}{page6}</body></html>"""

html_path = os.path.join(OUT, f"Leviathan_{short}_Fact_Sheet_{edition.replace(' ', '')}.html")
pdf_path = html_path[:-5] + ".pdf"
with open(html_path, "w") as f:
    f.write(html)
render = os.path.join(os.path.dirname(os.path.abspath(__file__)), "render_pdf.js")
subprocess.run(["node", render, os.path.abspath(html_path), os.path.abspath(pdf_path)], check=True)
print("wrote", html_path, pdf_path)
print("headline:", usd_m(holdco_size), pct(exp_irr), mult(exp_moic), "| top10 share", f"{top10_pct:.1%}")
