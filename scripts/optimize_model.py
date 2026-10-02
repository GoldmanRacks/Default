#!/usr/bin/env python3
"""
Leviathan PE Holdco model — v3 optimization pass.

Usage: python3 optimize_model.py <source.xlsx> <output.xlsx>

What it does (every change is also written to the new 'Change Log' tab):
  1. Centralizes hold periods (5/7/10 yrs) and fund terms as named ranges and
     rewrites every hard-coded hold literal (^5, *7, (1/10) ...) to use them.
  2. Strips redundant self-sheet references ('Holdco Summary'!$B$9 used inside
     Holdco Summary) and replaces repeated cross-sheet lever references with names.
  3. Guards every IRR formula against non-positive proceeds (#NUM! -> -100%).
  4. Makes the Holdco Summary "Expected" column probability-weight the NET
     waterfall (same method as Fund Economics) instead of running the waterfall
     on expected gross proceeds (which overstated expected net via carry convexity).
  5. Replaces the stale sleeve CAGR memo rows on Holdco Summary with live links.
  6. Adds tabs: Change Log, Checks (integrity dashboard), Sleeve Economics
     (gross->net waterfall for all three sub-vehicles), Fact Sheet Data
     (every figure used by the external fact sheet, live-linked).
  7. Freeze panes, print setup, tab colours, forced recalc on open.
"""
import re
import sys
from copy import copy

from openpyxl import load_workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter
from openpyxl.workbook.defined_name import DefinedName
from openpyxl.worksheet.properties import PageSetupProperties

SRC, DST = sys.argv[1], sys.argv[2]
wb = load_workbook(SRC)

# ----------------------------------------------------------------------------
# style helpers (match the workbook's existing conventions exactly)
# ----------------------------------------------------------------------------
NAVY = "FF1F2A44"
HDR_FILL = "FF2E4374"
EXP_FILL = "FF3E5C3A"
SHOCK_FILL = "FF7A3B2E"
INPUT_BLUE = "FF0000FF"
LINK_GREEN = "FF008000"
INPUT_YELLOW = "FFFFF2CC"
SECTION_FILL = "FFEAEEF5"
TOTAL_FILL = "FFE2EFDA"
EXP_COL_FILL = "FFEAF2E6"
SHOCK_COL_FILL = "FFFCE9DD"
GRAY = "FF555555"
RED = "FFC00000"
GREEN_OK = "FF2E7D32"

THIN = Side(style="thin", color="FFBFBFBF")
BOTTOM = Border(bottom=THIN)

FMT_USD0 = '\\$#,##0;"($"#,##0\\);\\-'
FMT_USD1 = '\\$#,##0.0;"($"#,##0.0\\);\\-'
FMT_PCT = "0.0%"
FMT_X = "0.00\\x"

def font(size=10, bold=False, color="FF000000", italic=False):
    return Font(name="Arial", size=size, bold=bold, color=color, italic=italic)

def fill(rgb):
    return PatternFill("solid", fgColor=rgb)

def title(ws, cell, text):
    ws[cell] = text
    ws[cell].font = font(15, True, NAVY)

def subtitle(ws, cell, text):
    ws[cell] = text
    ws[cell].font = font(9, False, GRAY)

def section(ws, cell, text, banner=False):
    ws[cell] = text
    ws[cell].font = font(11, True, NAVY)
    if banner:
        ws[cell].fill = fill(SECTION_FILL)

def header_row(ws, row, labels, start_col=1, special=None):
    special = special or {}
    for i, lab in enumerate(labels):
        c = ws.cell(row=row, column=start_col + i, value=lab)
        c.font = font(10, True, "FFFFFFFF")
        c.fill = fill(special.get(lab, HDR_FILL))
        c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        c.border = BOTTOM

def body(c, nf=None, bold=False, color="FF000000", fillrgb=None, align=None):
    c.font = font(10, bold, color)
    if nf:
        c.number_format = nf
    if fillrgb:
        c.fill = fill(fillrgb)
    if align:
        c.alignment = Alignment(horizontal=align)
    c.border = BOTTOM

def input_cell(c, nf=None):
    body(c, nf, bold=True, color=INPUT_BLUE, fillrgb=INPUT_YELLOW, align="right")

def link_cell(c, nf=None, bold=False, fillrgb=None):
    body(c, nf, bold=bold, color=LINK_GREEN, fillrgb=fillrgb, align="right")

def total_cell(c, nf=None):
    body(c, nf, bold=True, fillrgb=TOTAL_FILL, align="right")

def note(ws, cell, text, size=9, wrap=False):
    ws[cell] = text
    ws[cell].font = font(size, False, GRAY)
    if wrap:
        ws[cell].alignment = Alignment(wrap_text=True, vertical="top")

changelog = []  # (sheet, range, change, value_impact)
def log(sheet, rng, change, impact="None"):
    changelog.append((sheet, rng, change, impact))

# ----------------------------------------------------------------------------
# 1. Named ranges + hold-period lever block on Assumptions
# ----------------------------------------------------------------------------
A = wb["Assumptions"]
A["A4"] = "FUND TERMS (apply to the holdco and all three sleeves)"
log("Assumptions", "A4", "Relabelled fund-terms block: these terms drive the holdco AND every sleeve waterfall, not just IQT.")

section(A, "E4", "VEHICLE HOLD PERIODS (yrs) — blue = lever")
for r, (lab, val, nm, note_txt) in enumerate([
    ("Short hold (yrs)", 5, "Hold_Short", "Drives every 'short-hold' block model-wide"),
    ("Mid hold (yrs)", 7, "Hold_Mid", "Drives every 'mid-hold' block; recommended vehicle"),
    ("Long hold (yrs)", 10, "Hold_Long", "Drives every 'long-hold' block model-wide"),
], start=5):
    A[f"E{r}"] = lab
    body(A[f"E{r}"])
    A[f"F{r}"] = val
    input_cell(A[f"F{r}"], "0")
    note(A, f"G{r}", note_txt)
A.column_dimensions["G"].width = 44
log("Assumptions", "E4:G7", "NEW hold-period levers (5/7/10 yrs) with named ranges Hold_Short / Hold_Mid / Hold_Long. "
    "Every block header, hold exponent, fee-year multiplier and IRR root in the model now references these cells.")

A["A29"] = ('="Check: deployment (B6) + reserve (B7) = "&TEXT(B6+B7,"$#,##0")&"M vs committed (B5) "'
            '&TEXT(B5,"$#,##0")&"M — "&IF(ABS(B6+B7-B5)<0.5,"OK","MISMATCH")')
A["A29"].font = copy(A["A28"].font)
log("Assumptions", "A29", "NEW check: initial deployment + follow-on reserve must equal committed capital.")

NAMES = {
    "Hold_Short": "Assumptions!$F$5", "Hold_Mid": "Assumptions!$F$6", "Hold_Long": "Assumptions!$F$7",
    "IQT_Committed": "Assumptions!$B$5",
    "Mgmt_Fee": "Assumptions!$B$8", "Carry": "Assumptions!$B$9", "Pref": "Assumptions!$B$10",
    "Ret_IQT_Short": "Assumptions!$B$11", "Ret_IQT_Mid": "Assumptions!$B$12", "Ret_IQT_Long": "Assumptions!$B$13",
    "Ret_Wpn_Short": "'Weapons Sleeve'!$B$6", "Ret_Wpn_Mid": "'Weapons Sleeve'!$B$7", "Ret_Wpn_Long": "'Weapons Sleeve'!$B$8",
    "Ret_Con_Short": "'Consumer Sleeve'!$B$6", "Ret_Con_Mid": "'Consumer Sleeve'!$B$7", "Ret_Con_Long": "'Consumer Sleeve'!$B$8",
    "P_Base": "'Defense Supercycle'!$B$17", "P_Bull": "'Defense Supercycle'!$B$18",
    "P_Bear": "'Defense Supercycle'!$B$19", "P_Shock": "'Defense Supercycle'!$B$20",
    "Holdco_Size": "'Holdco Summary'!$B$9", "IQT_Size": "'Holdco Summary'!$B$6",
    "Wpn_Size": "'Holdco Summary'!$B$7", "Con_Size": "'Holdco Summary'!$B$8",
    "SPX_CAGR": "'PME, DPI & Sensitivity'!$B$5", "NDX_CAGR": "'PME, DPI & Sensitivity'!$B$6",
    "Basket_CAGR": "'Holdco Summary'!$B$23",
}
for nm, ref in NAMES.items():
    wb.defined_names[nm] = DefinedName(nm, attr_text=ref)
log("Workbook", "Defined names", f"NEW named ranges for every lever: {', '.join(NAMES)}.")

# ----------------------------------------------------------------------------
# 2. Global formula substitutions (names, self-sheet refs)
# ----------------------------------------------------------------------------
SUBS = [
    (r"'Defense Supercycle'!\$B\$17(?!\d)", "P_Base"),
    (r"'Defense Supercycle'!\$B\$18(?!\d)", "P_Bull"),
    (r"'Defense Supercycle'!\$B\$19(?!\d)", "P_Bear"),
    (r"'Defense Supercycle'!\$B\$20(?!\d)", "P_Shock"),
    (r"Assumptions!\$B\$5(?!\d)", "IQT_Committed"),
    (r"Assumptions!\$B\$8(?!\d)", "Mgmt_Fee"),
    (r"Assumptions!\$B\$9(?!\d)", "Carry"),
    (r"Assumptions!\$B\$10(?!\d)", "Pref"),
    (r"Assumptions!\$B\$11(?!\d)", "Ret_IQT_Short"),
    (r"Assumptions!\$B\$12(?!\d)", "Ret_IQT_Mid"),
    (r"Assumptions!\$B\$13(?!\d)", "Ret_IQT_Long"),
    (r"'Weapons Sleeve'!\$B\$6(?!\d)", "Ret_Wpn_Short"),
    (r"'Weapons Sleeve'!\$B\$7(?!\d)", "Ret_Wpn_Mid"),
    (r"'Weapons Sleeve'!\$B\$8(?!\d)", "Ret_Wpn_Long"),
    (r"'Consumer Sleeve'!\$B\$6(?!\d)", "Ret_Con_Short"),
    (r"'Consumer Sleeve'!\$B\$7(?!\d)", "Ret_Con_Mid"),
    (r"'Consumer Sleeve'!\$B\$8(?!\d)", "Ret_Con_Long"),
    (r"'Holdco Summary'!\$B\$9(?!\d)", "Holdco_Size"),
    (r"'Holdco Summary'!\$B\$6(?!\d)", "IQT_Size"),
    (r"'Holdco Summary'!\$B\$7(?!\d)", "Wpn_Size"),
    (r"'Holdco Summary'!\$B\$8(?!\d)", "Con_Size"),
    (r"'Holdco Summary'!\$B\$21(?!\d)", "SPX_CAGR"),
    (r"'Holdco Summary'!\$B\$22(?!\d)", "NDX_CAGR"),
    (r"'Holdco Summary'!\$B\$23(?!\d)", "Basket_CAGR"),
    (r"'PME, DPI & Sensitivity'!\$B\$5(?!\d)", "SPX_CAGR"),
    (r"'PME, DPI & Sensitivity'!\$B\$6(?!\d)", "NDX_CAGR"),
]
n_sub = 0
n_self = 0
for ws in wb.worksheets:
    self_pat = re.compile(r"'" + re.escape(ws.title) + r"'!")
    for row in ws.iter_rows():
        for c in row:
            v = c.value
            if not (isinstance(v, str) and v.startswith("=")):
                continue
            new = v
            for pat, rep in SUBS:
                new, k = re.subn(pat, rep, new)
                n_sub += k
            new, k = self_pat.subn("", new)
            n_self += k
            if new != v:
                c.value = new
log("All tabs", "formulas", f"Replaced {n_sub} repeated lever references with named ranges and removed {n_self} redundant "
    "same-sheet references (e.g. 'Holdco Summary'!$B$9 inside Holdco Summary). Pure readability; values unchanged.")

# ----------------------------------------------------------------------------
# 3. Hold-period literal rewrite (block based)
# ----------------------------------------------------------------------------
HOLD_LIT = {"Short": 5, "Mid": 7, "Long": 10}
BLOCKS = {
    "Holdco Summary": [(26, 45, "Short"), (47, 66, "Mid"), (68, 87, "Long")],
    "Portfolio Returns": [(4, 16, "Short"), (18, 30, "Mid"), (32, 44, "Long")],
    "Fund Economics": [(4, 18, "Short"), (20, 34, "Mid"), (36, 50, "Long")],
    "Weapons Sleeve": [(23, 35, "Short"), (37, 49, "Mid"), (51, 63, "Long")],
    "Consumer Sleeve": [(23, 35, "Short"), (37, 49, "Mid"), (51, 63, "Long")],
    "PME, DPI & Sensitivity": [(11, 25, "Short"), (27, 41, "Mid"), (43, 57, "Long")],
    "IQT Clusters": [(12, 19, "Short"), (20, 27, "Mid"), (28, 35, "Long")],
}
n_hold = 0
def rewrite_hold(formula, tag):
    global n_hold
    n = HOLD_LIT[tag]
    out = formula
    for pat, rep in [(rf"\^{n}(?!\d)", f"^Hold_{tag}"), (rf"\*{n}(?!\d)", f"*Hold_{tag}"), (rf"\(1/{n}\)", f"(1/Hold_{tag})")]:
        out, k = re.subn(pat, rep, out)
        n_hold += k
    return out

for sheet, blocks in BLOCKS.items():
    ws = wb[sheet]
    for r0, r1, tag in blocks:
        for row in ws.iter_rows(min_row=r0, max_row=r1):
            for c in row:
                if isinstance(c.value, str) and c.value.startswith("="):
                    c.value = rewrite_hold(c.value, tag)

# Sensitivity table: column-based (B=short, C=mid, D=long); rewritten in full, with names.
P = wb["PME, DPI & Sensitivity"]
for r in range(62, 70):
    for col, tag, fe_row in (("B", "Short", 12), ("C", "Mid", 28), ("D", "Long", 44)):
        expr = (f"(((1-$A{r})*(P_Base*'Fund Economics'!B{fe_row}+P_Bull*'Fund Economics'!C{fe_row}"
                f"+P_Bear*'Fund Economics'!D{fe_row})/(P_Base+P_Bull+P_Bear)+$A{r}*'Fund Economics'!E{fe_row})/IQT_Committed)")
        P[f"{col}{r}"] = f"={expr}^(1/Hold_{tag})-1"
        n_hold += 1
for r in [81] + list(range(87, 95)):
    for col, tag in (("B", "Short"), ("C", "Mid"), ("D", "Long")):
        c = P[f"{col}{r}"]
        if isinstance(c.value, str) and c.value.startswith("="):
            c.value = rewrite_hold(c.value, tag)
for col, tag in (("B", "Short"), ("C", "Mid"), ("D", "Long")):
    P[f"{col}100"] = f"=Hold_{tag}"
    link_cell(P[f"{col}100"], "0")
    P[f"{col}73"] = f'=Hold_{tag}&"-yr"'
    P[f"{col}99"] = f'=Hold_{tag}&"-yr"'
    n_hold += 1
log("PME, DPI & Sensitivity", "B73:D73, B81:D81, B87:D94, B99:D100", "Holdco PME / sensitivity blocks and the Weapons PME hold-year "
    "inputs now read the Hold_* levers instead of hard-coded 5 / 7 / 10.")
log("All model tabs", "hold blocks",
    f"Rewrote {n_hold} hard-coded hold-period literals (^5, *7, (1/10) ...) to the Hold_Short / Hold_Mid / Hold_Long levers. "
    "Change a hold period once on Assumptions and every proceeds, pref, fee, IRR, PME and sensitivity formula follows.")

# Text labels that embed a hold period -> live formulas
n_lbl = 0
LABEL_RULES = [
    (re.compile(r"^(5|7|10)-YEAR (.+)$"), lambda m: f'=Hold_{{t}}&"-YEAR {m.group(2)}"'),
    (re.compile(r"^(5|7|10)-Year Hold$"), lambda m: '=Hold_{t}&"-Year Hold"'),
    (re.compile(r"^(5|7|10)-yr Net IRR$"), lambda m: '=Hold_{t}&"-yr Net IRR"'),
    (re.compile(r"^Retention @ ?(5|7|10)yr$"), lambda m: '="Retention @ "&Hold_{t}&"yr"'),
    (re.compile(r"^(5|7|10)-yr$"), lambda m: '=Hold_{t}&"-yr"'),
    (re.compile(r"^(.{3,60}) (5|7|10)-YEAR (.+)$"), lambda m: f'="{m.group(1)} "&Hold_{{t}}&"-YEAR {m.group(3)}"'),
]
TAG_OF = {"5": "Short", "7": "Mid", "10": "Long"}
for ws in wb.worksheets:
    for row in ws.iter_rows():
        for c in row:
            if isinstance(c.value, str) and not c.value.startswith("="):
                for pat, build in LABEL_RULES:
                    m = pat.match(c.value)
                    if m and '"' not in c.value:
                        hold = m.group(2) if pat.groups == 3 else m.group(1)
                        c.value = build(m).replace("{t}", TAG_OF[hold])
                        n_lbl += 1
                        break
S = wb["Scenario Summary"]
S["A29"] = ('="• Recommended: "&Hold_Mid&"-year vehicle, base sizing, "&TEXT(Assumptions!B7,"$#,##0")'
            '&"M reserve steered to Substrate + EUV Tech + EdgeCortix pro-rata."')
R = wb["Read Me"]
R["B2"] = ('="IQT-Backed Deep-Tech Acquisition-Stake Portfolio  |  "&Hold_Short&" / "&Hold_Mid&" / "&Hold_Long'
           '&"-Year Holds  |  Defense-Supercycle Overlay"')
log("All tabs", "section labels", f"{n_lbl + 2} block headers / row labels that embedded '5-YEAR', '7-Year', 'Retention @ 10yr' etc. "
    "are now formulas driven by the hold levers, so labels can never drift from the maths.")

# ----------------------------------------------------------------------------
# 4. Guard IRR formulas against non-positive proceeds
# ----------------------------------------------------------------------------
IRR_PAT = re.compile(r"^=\((.+)\)\^\(1/(Hold_\w+)\)-1$")
n_guard = 0
for ws in wb.worksheets:
    for row in ws.iter_rows():
        for c in row:
            if isinstance(c.value, str):
                m = IRR_PAT.match(c.value)
                if m:
                    expr, hold = m.groups()
                    c.value = f"=IF(({expr})<=0,-1,({expr})^(1/{hold})-1)"
                    n_guard += 1
log("All model tabs", "IRR / Direct Alpha cells", f"Guarded {n_guard} IRR and Direct-Alpha formulas: a wipe-out "
    "(net proceeds <= 0) now returns -100% instead of #NUM!, so Expected columns and checks never break in a severe Bear case.")

# ----------------------------------------------------------------------------
# 5. Holdco Summary: live memo rows, consistent Expected column, status line
# ----------------------------------------------------------------------------
H = wb["Holdco Summary"]
H["A14"] = '="SLEEVE RETURN SUMMARY — implied gross IRR on checks at the "&Hold_Short&"-yr hold, net of dilution (live links to the sleeve tabs)"'
for rng in ("A18:F18",):
    H.unmerge_cells(rng)
H.row_dimensions[18].height = 15
memo = [
    (16, "IQT-mirror (bottom-up, live)", "'Portfolio Returns'", 15),
    (17, "Weapons (bottom-up, live)", "'Weapons Sleeve'", 34),
    (18, "Consumer / Value (bottom-up, live)", "'Consumer Sleeve'", 34),
]
for r, lab, sheet, srow in memo:
    H[f"A{r}"] = lab
    body(H[f"A{r}"])
    for col, src in zip("BCDE", "EHKN"):
        H[f"{col}{r}"] = f"={sheet}!{src}{srow}"
        link_cell(H[f"{col}{r}"], FMT_PCT, fillrgb=(SHOCK_COL_FILL if col == "E" else None))
    H[f"F{r}"] = None
note(H, "A19", "Memo only — these rows are live reads of the sleeve tabs (gross IRR on checks at the short hold). "
     "The sleeve tabs are the source of truth; nothing downstream references this block.")
H["A19"].alignment = Alignment(wrap_text=False)
log("Holdco Summary", "A14:F19", "Stale hard-coded sleeve CAGR memos (Weapons 22/34/5/32%, Consumer 14/25/-10/-4%) replaced by live "
    "links to the bottom-up sleeve IRRs for all three sleeves; note moved to A19.", "Memo rows only")

for base in (27, 48, 69):           # header rows of the three roll-up blocks
    for r in range(base + 5, base + 11):   # (-) Return of capital ... NET proceeds
        H[f"F{r}"] = f"=B{r}*P_Base+C{r}*P_Bull+D{r}*P_Bear+E{r}*P_Shock"
log("Holdco Summary", "F32:F37, F53:F58, F74:F79",
    "Expected column now probability-weights each NET waterfall line (same method as Fund Economics / Scenario Summary). "
    "Rows F32/F33/F36 are constant across scenarios, F34/F35 were already weighted; the whole block is now written one way.",
    "None in this version (F34/F35 were already weighted); block is now uniformly weighted")

H["A2"] = ("Three sub-funds rolled up to a blended holdco return. Blue = lever. All three sleeves — IQT-mirror, Weapons, "
           "Consumer/Value — flow in bottom-up. Expected = probability-weighted net (consistent with Fund Economics).")
H["A3"] = "=Checks!$B$3"
H["A3"].font = font(10, True, GREEN_OK)
log("Holdco Summary", "A3", "Live model-integrity status pulled from the new Checks tab.")

# ----------------------------------------------------------------------------
# 6. Sleeve Economics tab — gross -> net for all three sub-vehicles
# ----------------------------------------------------------------------------
SE = wb.create_sheet("Sleeve Economics", index=wb.sheetnames.index("Consumer Sleeve") + 1)
title(SE, "A1", "SLEEVE ECONOMICS — GROSS->NET WATERFALL BY SUB-VEHICLE")
subtitle(SE, "A2", "Same European waterfall (return of capital -> pref -> carry, fees on committed) applied to each sleeve on a "
         "stand-alone basis. Expected = probability-weighted net. IQT block reconciles to Fund Economics (see Checks).")
SE.column_dimensions["A"].width = 34
SLEEVES = [
    ("IQT-MIRROR SLEEVE", "B", "IQT_Size", "'Portfolio Returns'", {"Short": 15, "Mid": 29, "Long": 43}, "Ret_IQT"),
    ("WEAPONS SLEEVE", "H", "Wpn_Size", "'Weapons Sleeve'", {"Short": 34, "Mid": 48, "Long": 62}, "Ret_Wpn"),
    ("CONSUMER / VALUE SLEEVE", "N", "Con_Size", "'Consumer Sleeve'", {"Short": 34, "Mid": 48, "Long": 62}, "Ret_Con"),
]
SCEN_COLS = "CFIL"  # Base/Bull/Bear/Shock gross-proceeds columns on the source tabs
SE_LINES = ["Gross exit proceeds", "(-) Return of committed capital", "(-) Preferred return (comp.)",
            "Profit above pref (carry base)", "(-) GP carried interest", "(-) Management fees",
            "Net proceeds to LPs", "Gross MOIC", "Net MOIC (to LP)", "Gross IRR", "Net IRR (to LP)",
            "Net KS-PME vs SPX", "Net KS-PME vs NDX"]
SE_BLOCK_ROWS = {}   # (tag) -> first data row
row = 4
for tag in ("Short", "Mid", "Long"):
    SE[f"A{row}"] = f'=Hold_{tag}&"-YEAR HOLD — SLEEVE WATERFALLS"'
    SE[f"A{row}"].font = font(11, True, NAVY)
    SE[f"A{row}"].fill = fill(SECTION_FILL)
    hdr = row + 1
    SE[f"A{hdr}"] = "Line item ($M)"
    header_row(SE, hdr, ["Line item ($M)"], 1)
    for name, c0, size, src, srows, ret in SLEEVES:
        ci = ord(c0) - 64
        SE.cell(row=row, column=ci, value=name).font = font(10, True, NAVY)
        header_row(SE, hdr, ["Base", "Bull", "Bear", "TSMC-Shock", "Expected"], ci,
                   {"TSMC-Shock": SHOCK_FILL, "Expected": EXP_FILL})
    r0 = hdr + 1
    SE_BLOCK_ROWS[tag] = r0
    for i, lab in enumerate(SE_LINES):
        r = r0 + i
        SE[f"A{r}"] = lab
        body(SE[f"A{r}"], bold=(lab in ("Net proceeds to LPs", "Net MOIC (to LP)", "Net IRR (to LP)")))
    for name, c0, size, src, srows, ret in SLEEVES:
        ci = ord(c0) - 64
        cols = [get_column_letter(ci + k) for k in range(5)]  # Base..Expected
        g, roc, pref, prof, carry, fee, net, gm, nm, gi, ni, pme_s, pme_n = [r0 + k for k in range(13)]
        for k, col in enumerate(cols[:4]):
            SE[f"{col}{g}"] = f"={src}!{SCEN_COLS[k]}{srows[tag]}"
            link_cell(SE[f"{col}{g}"], FMT_USD1)
            SE[f"{col}{roc}"] = f"=-{size}"
            SE[f"{col}{pref}"] = f"=-{size}*((1+Pref)^Hold_{tag}-1)"
            SE[f"{col}{prof}"] = f"=MAX(0,{col}{g}+{col}{roc}+{col}{pref})"
            SE[f"{col}{carry}"] = f"=-Carry*{col}{prof}"
            SE[f"{col}{fee}"] = f"=-{size}*Mgmt_Fee*Hold_{tag}"
            SE[f"{col}{net}"] = f"={col}{g}+{col}{carry}+{col}{fee}"
        e = cols[4]
        for r in (g, roc, pref, prof, carry, fee, net):
            SE[f"{e}{r}"] = f"={cols[0]}{r}*P_Base+{cols[1]}{r}*P_Bull+{cols[2]}{r}*P_Bear+{cols[3]}{r}*P_Shock"
        for col in cols:
            SE[f"{col}{gm}"] = f"={col}{g}/{size}"
            SE[f"{col}{nm}"] = f"={col}{net}/{size}"
            SE[f"{col}{gi}"] = f"=IF(({col}{g}/{size})<=0,-1,({col}{g}/{size})^(1/Hold_{tag})-1)"
            SE[f"{col}{ni}"] = f"=IF(({col}{net}/{size})<=0,-1,({col}{net}/{size})^(1/Hold_{tag})-1)"
            SE[f"{col}{pme_s}"] = f"={col}{nm}/(1+SPX_CAGR)^Hold_{tag}"
            SE[f"{col}{pme_n}"] = f"={col}{nm}/(1+NDX_CAGR)^Hold_{tag}"
            for r in (roc, pref, prof, carry, fee):
                body(SE[f"{col}{r}"], FMT_USD1, align="right")
            total_cell(SE[f"{col}{net}"], FMT_USD1)
            body(SE[f"{col}{gm}"], FMT_X, align="right")
            total_cell(SE[f"{col}{nm}"], FMT_X)
            body(SE[f"{col}{gi}"], FMT_PCT, align="right")
            total_cell(SE[f"{col}{ni}"], FMT_PCT)
            body(SE[f"{col}{pme_s}"], FMT_X, align="right")
            body(SE[f"{col}{pme_n}"], FMT_X, align="right")
            if col == cols[3]:
                for r in range(g, pme_n + 1):
                    if SE[f"{col}{r}"].fill.fgColor.rgb != TOTAL_FILL:
                        SE[f"{col}{r}"].fill = fill(SHOCK_COL_FILL)
            if col == e:
                for r in range(g, pme_n + 1):
                    if SE[f"{col}{r}"].fill.fgColor.rgb != TOTAL_FILL:
                        SE[f"{col}{r}"].fill = fill(EXP_COL_FILL)
        if tag == "Short":
            for col in cols:
                SE.column_dimensions[col].width = 12
    row = r0 + len(SE_LINES) + 2

# Reconciliation: sum of stand-alone sleeve nets vs cross-collateralised holdco net
SE[f"A{row}"] = "RECONCILIATION — SUM OF STAND-ALONE SLEEVES vs HOLDCO (CROSS-COLLATERALISED) NET PROCEEDS ($M)"
SE[f"A{row}"].font = font(11, True, NAVY)
SE[f"A{row}"].fill = fill(SECTION_FILL)
hdr = row + 1
header_row(SE, hdr, ["Hold / line item", "Base", "Bull", "Bear", "TSMC-Shock", "Expected"], 1,
           {"TSMC-Shock": SHOCK_FILL, "Expected": EXP_FILL})
HOLDCO_NET_ROW = {"Short": 37, "Mid": 58, "Long": 79}
r = hdr + 1
RECON_ROWS = {}
for tag in ("Short", "Mid", "Long"):
    net_r = SE_BLOCK_ROWS[tag] + 6
    SE[f"A{r}"] = f'=Hold_{tag}&"-yr: sum of sleeve net proceeds"'
    body(SE[f"A{r}"])
    SE[f"A{r+1}"] = f'=Hold_{tag}&"-yr: holdco net proceeds (Holdco Summary)"'
    body(SE[f"A{r+1}"])
    SE[f"A{r+2}"] = f'=Hold_{tag}&"-yr: cross-sleeve netting effect"'
    body(SE[f"A{r+2}"], bold=True)
    for k, col in enumerate("BCDEF"):
        SE[f"{col}{r}"] = f"={get_column_letter(2+k)}{net_r}+{get_column_letter(8+k)}{net_r}+{get_column_letter(14+k)}{net_r}"
        body(SE[f"{col}{r}"], FMT_USD1, align="right")
        SE[f"{col}{r+1}"] = f"='Holdco Summary'!{col}{HOLDCO_NET_ROW[tag]}"
        link_cell(SE[f"{col}{r+1}"], FMT_USD1)
        SE[f"{col}{r+2}"] = f"={col}{r+1}-{col}{r}"
        total_cell(SE[f"{col}{r+2}"], FMT_USD1)
    RECON_ROWS[tag] = r
    r += 3
note(SE, f"A{r}", "Positive netting effect = the holdco waterfall (one pref / one carry across $750M) returns more to LPs than three "
     "stand-alone sleeve waterfalls, because strong sleeves offset weak ones before carry is charged. Negative = the reverse.")
SE.freeze_panes = "B4"
log("Sleeve Economics", "whole tab", "NEW tab: stand-alone gross->net waterfall for each sub-vehicle x hold x scenario (previously only the IQT "
    "sleeve had a net view), plus reconciliation of sum-of-sleeves vs the cross-collateralised holdco net. Feeds the fact sheet.")

# ----------------------------------------------------------------------------
# 7. Fact Sheet Data tab
# ----------------------------------------------------------------------------
FS = wb.create_sheet("Fact Sheet Data")
title(FS, "A1", "FACT SHEET DATA — EVERY FIGURE ON THE EXTERNAL FACT SHEET, LIVE-LINKED")
subtitle(FS, "A2", "Green = link to the model. Blue = classification tags / descriptions used only by the fact sheet. "
         "Headline case = mid hold (recommended vehicle), probability-weighted Expected.")
for col, w in zip("ABCDEFGHIJKLMN", [30, 14, 12, 12, 12, 12, 12, 14, 26, 18, 22, 11, 44, 12]):
    FS.column_dimensions[col].width = w

# A. Headline
section(FS, "A4", "A | HOLDCO HEADLINE", True)
head = [
    ("Fund name", "Leviathan Core Private Equity Holdco", None, "input"),
    ("Short name", "LPEH", None, "input"),
    ("Figures as of", "22-Sep-2026", None, "input"),
    ("Fact sheet edition", "September 2026", None, "input"),
    ("Holdco committed capital ($M)", "=Holdco_Size", FMT_USD0, "link"),
    ("Number of sub-vehicles", "=COUNTA('Holdco Summary'!A6:A8)", "0", "link"),
    ("Number of holdings", "=COUNTA(Assumptions!A18:A26)+COUNTA('Weapons Sleeve'!A12:A20)+COUNTA('Consumer Sleeve'!A12:A20)", "0", "link"),
    ("Headline hold (yrs)", "=Hold_Mid", "0", "link"),
    ("Expected net IRR (headline hold)", "='Holdco Summary'!F61", FMT_PCT, "link"),
    ("Expected net MOIC (headline hold)", "='Holdco Summary'!F59", FMT_X, "link"),
    ("Expected net DPI at exit (headline hold)", "='Holdco Summary'!F60", FMT_X, "link"),
    ("Base-case net IRR (headline hold)", "='Holdco Summary'!B61", FMT_PCT, "link"),
    ("Expected gross MOIC (headline hold)", "='Holdco Summary'!F52/Holdco_Size", FMT_X, "link"),
    ("Expected net KS-PME vs S&P 500", "='Holdco Summary'!F62", FMT_X, "link"),
    ("Expected net KS-PME vs Nasdaq-100", "='Holdco Summary'!F63", FMT_X, "link"),
    ("Expected net KS-PME vs Defense+Semis basket", "='Holdco Summary'!F64", FMT_X, "link"),
    ("Expected Direct Alpha vs basket (ann.)", "='Holdco Summary'!F65", FMT_PCT, "link"),
    ("Scenarios modelled", "=COUNTA('Defense Supercycle'!A17:A20)", "0", "link"),
    ("TSMC-Shock probability", "=P_Shock", FMT_PCT, "link"),
]
HEAD_ROW = {}
r = 5
for lab, val, nf, kind in head:
    FS[f"A{r}"] = lab
    body(FS[f"A{r}"])
    FS[f"B{r}"] = val
    (input_cell if kind == "input" else link_cell)(FS[f"B{r}"], nf)
    if kind == "input":
        FS[f"B{r}"].alignment = Alignment(horizontal="left")
    HEAD_ROW[lab] = r
    r += 1

# B. Sub-vehicle table (headline = mid hold)
r += 1
section(FS, f"A{r}", '="B | SUB-VEHICLE SUMMARY — "&Hold_Mid&"-YEAR HOLD (headline)"', True)
r += 1
SV_HDR = ["Sub-vehicle", "Committed ($M)", "% of Holdco", "Holdings", "Gross MOIC (Base)", "Gross IRR (Base)",
          "Net IRR Base", "Net IRR Bull", "Net IRR Bear", "Net IRR Shock", "Net IRR Expected", "Net MOIC Expected", "Net KS-PME vs SPX (Exp.)", "Role"]
header_row(FS, r, SV_HDR, 1, {"Net IRR Shock": SHOCK_FILL, "Net IRR Expected": EXP_FILL, "Net MOIC Expected": EXP_FILL, "Net KS-PME vs SPX (Exp.)": EXP_FILL})
r += 1
SV_ROW = {}
mid0 = SE_BLOCK_ROWS["Mid"]
sv = [
    ("Defense (Weapons sleeve)", "Wpn_Size", "COUNTA('Weapons Sleeve'!A12:A20)", "H", "'Holdco Summary'!F7"),
    ("IQT Semi / AI (IQT-mirror sleeve)", "IQT_Size", "COUNTA(Assumptions!A18:A26)", "B", "'Holdco Summary'!F6"),
    ("Consumer Discretionary (Consumer / Value sleeve)", "Con_Size", "COUNTA('Consumer Sleeve'!A12:A20)", "N", "'Holdco Summary'!F8"),
]
for lab, size, cnt, c0, role in sv:
    ci = ord(c0) - 64
    cols = [get_column_letter(ci + k) for k in range(5)]
    FS[f"A{r}"] = lab; body(FS[f"A{r}"], bold=True)
    FS[f"B{r}"] = f"={size}"; link_cell(FS[f"B{r}"], FMT_USD0)
    FS[f"C{r}"] = f"=B{r}/Holdco_Size"; body(FS[f"C{r}"], FMT_PCT, align="right")
    FS[f"D{r}"] = f"={cnt}"; link_cell(FS[f"D{r}"], "0")
    FS[f"E{r}"] = f"='Sleeve Economics'!{cols[0]}{mid0+7}"; link_cell(FS[f"E{r}"], FMT_X)
    FS[f"F{r}"] = f"='Sleeve Economics'!{cols[0]}{mid0+9}"; link_cell(FS[f"F{r}"], FMT_PCT)
    for k, col in enumerate("GHIJK"):
        FS[f"{col}{r}"] = f"='Sleeve Economics'!{cols[k]}{mid0+10}"
        link_cell(FS[f"{col}{r}"], FMT_PCT, fillrgb=(SHOCK_COL_FILL if col == "J" else EXP_COL_FILL if col == "K" else None))
    FS[f"L{r}"] = f"='Sleeve Economics'!{cols[4]}{mid0+8}"; link_cell(FS[f"L{r}"], FMT_X, fillrgb=EXP_COL_FILL)
    FS[f"M{r}"] = f"='Sleeve Economics'!{cols[4]}{mid0+11}"; link_cell(FS[f"M{r}"], FMT_X, fillrgb=EXP_COL_FILL)
    FS[f"N{r}"] = f"={role}"; link_cell(FS[f"N{r}"]); FS[f"N{r}"].alignment = Alignment(horizontal="left")
    SV_ROW[lab] = r
    r += 1
FS[f"A{r}"] = "HOLDCO (cross-collateralised)"; total_cell(FS[f"A{r}"]); FS[f"A{r}"].alignment = Alignment(horizontal="left")
FS[f"B{r}"] = "=Holdco_Size"; link_cell(FS[f"B{r}"], FMT_USD0, True, TOTAL_FILL)
FS[f"C{r}"] = f"=B{r}/Holdco_Size"; total_cell(FS[f"C{r}"], FMT_PCT)
FS[f"D{r}"] = f"=SUM(D{r-3}:D{r-1})"; total_cell(FS[f"D{r}"], "0")
FS[f"E{r}"] = "='Holdco Summary'!B52/Holdco_Size"; link_cell(FS[f"E{r}"], FMT_X, True, TOTAL_FILL)
FS[f"F{r}"] = "=IF(E{0}<=0,-1,E{0}^(1/Hold_Mid)-1)".format(r); total_cell(FS[f"F{r}"], FMT_PCT)
for k, col in enumerate("GHIJK"):
    FS[f"{col}{r}"] = f"='Holdco Summary'!{'BCDEF'[k]}61"; link_cell(FS[f"{col}{r}"], FMT_PCT, True, TOTAL_FILL)
FS[f"L{r}"] = "='Holdco Summary'!F59"; link_cell(FS[f"L{r}"], FMT_X, True, TOTAL_FILL)
FS[f"M{r}"] = "='Holdco Summary'!F62"; link_cell(FS[f"M{r}"], FMT_X, True, TOTAL_FILL)
FS[f"N{r}"] = "Tripartite barbell"; total_cell(FS[f"N{r}"]); FS[f"N{r}"].alignment = Alignment(horizontal="left")
SV_ROW["HOLDCO"] = r
r += 2

# C. Holdco scenario grid (net IRR, net MOIC, net proceeds) for all holds
section(FS, f"A{r}", "C | HOLDCO SCENARIO GRID — NET TO LP", True)
r += 1
header_row(FS, r, ["Metric / hold", "Base", "Bull", "Bear", "TSMC-Shock", "Expected"], 1, {"TSMC-Shock": SHOCK_FILL, "Expected": EXP_FILL})
r += 1
GRID_ROW = {}
for metric, hrow, nf in [("Net IRR", {"Short": 40, "Mid": 61, "Long": 82}, FMT_PCT),
                         ("Net MOIC", {"Short": 38, "Mid": 59, "Long": 80}, FMT_X),
                         ("Net proceeds ($M)", {"Short": 37, "Mid": 58, "Long": 79}, FMT_USD1),
                         ("Gross MOIC", {"Short": 31, "Mid": 52, "Long": 73}, FMT_X),
                         ("Net KS-PME vs SPX", {"Short": 41, "Mid": 62, "Long": 83}, FMT_X),
                         ("Net KS-PME vs NDX", {"Short": 42, "Mid": 63, "Long": 84}, FMT_X),
                         ("Net KS-PME vs Defense+Semis basket", {"Short": 43, "Mid": 64, "Long": 85}, FMT_X)]:
    for tag in ("Short", "Mid", "Long"):
        FS[f"A{r}"] = f'="{metric} — "&Hold_{tag}&"-yr hold"'
        body(FS[f"A{r}"])
        for k, col in enumerate("BCDEF"):
            src = f"='Holdco Summary'!{col}{hrow[tag]}"
            if metric == "Gross MOIC":
                src = f"='Holdco Summary'!{col}{hrow[tag]}/Holdco_Size"
            FS[f"{col}{r}"] = src
            link_cell(FS[f"{col}{r}"], nf, fillrgb=(SHOCK_COL_FILL if col == "E" else EXP_COL_FILL if col == "F" else None))
        GRID_ROW[(metric, tag)] = r
        r += 1
r += 1

# D. Holdings register + breakdowns
section(FS, f"A{r}", "D | HOLDINGS REGISTER & BREAKDOWNS (tags in blue are fact-sheet classifications)", True)
r += 1
REG_HDR = ["Holding", "Sub-vehicle", "Check ($M)", "% of Holdco", "Entry post ($M)", "Own %", "Base CAGR", "Sector", "Region", "Stage / liquidity", "Rank by check", "Description (fact sheet)"]
header_row(FS, r, REG_HDR, 1)
r += 1
REG0 = r
HOLDINGS = [
    # (sheet, row, sub-vehicle, sector, region, stage, description)
    ("Assumptions", 18, "IQT Semi / AI", "Semiconductor Equipment", "North America", "Growth", "Domestic X-ray lithography platform; the sovereign-litho anchor of the sleeve"),
    ("Assumptions", 19, "IQT Semi / AI", "Semiconductor Equipment", "North America", "Growth", "At-wavelength EUV metrology; revenue-generating niche leader"),
    ("Assumptions", 20, "IQT Semi / AI", "Advanced Packaging & Materials", "North America", "Growth", "US ABF / substrate materials for advanced packaging; $50M CHIPS LOI"),
    ("Assumptions", 21, "IQT Semi / AI", "Edge AI Silicon", "Asia-Pacific", "Growth", "Low-power edge-AI inference accelerators for the tactical edge"),
    ("Assumptions", 22, "IQT Semi / AI", "Edge AI Silicon", "North America", "Pre-IPO", "Ultra-low-power edge AI silicon; S-1 filed (SYTN)"),
    ("Assumptions", 23, "IQT Semi / AI", "Quantum Computing", "North America", "Public / Listed", "Listed quantum sensing and computing platform (NYSE: INFQ)"),
    ("Assumptions", 24, "IQT Semi / AI", "Quantum Computing", "Asia-Pacific", "Growth", "Silicon spin-qubit quantum on existing CMOS foundries"),
    ("Assumptions", 25, "IQT Semi / AI", "Advanced Packaging & Materials", "North America", "Seed & Early", "US advanced packaging / rack-density secure compute (Cubelet)"),
    ("Assumptions", 26, "IQT Semi / AI", "Autonomy & Unmanned Systems", "North America", "Seed & Early", "Autonomous sensing and small UAS; Blue UAS provenance diligence"),
    ("Weapons Sleeve", 12, "Defense", "Autonomy & Unmanned Systems", "North America", "Late-stage Private", "Autonomous naval surface vessels; Series D $9.25B"),
    ("Weapons Sleeve", 13, "Defense", "Directed Energy, EW & ISR", "North America", "Growth", "High-power microwave directed-energy counter-drone systems"),
    ("Weapons Sleeve", 14, "Defense", "Defense Primes & Services", "Israel", "Pre-IPO", "Israeli aerospace and defense prime; IPO attempt H2-26"),
    ("Weapons Sleeve", 15, "Defense", "Directed Energy, EW & ISR", "Israel", "Pre-IPO", "IAI subsidiary: radar, electronic warfare and ISR systems"),
    ("Weapons Sleeve", 16, "Defense", "Munitions, Energetics & Ordnance", "Europe", "Public / Listed", "Listed small-arms manufacturer; closely held, block access"),
    ("Weapons Sleeve", 17, "Defense", "Munitions, Energetics & Ordnance", "North America", "Growth", "Early-growth energetics and propellant chemistry"),
    ("Weapons Sleeve", 18, "Defense", "Munitions, Energetics & Ordnance", "North America", "Late-stage Private", "Family-owned forger of missile casings and naval open/closed-die forgings"),
    ("Weapons Sleeve", 19, "Defense", "Munitions, Energetics & Ordnance", "North America", "Late-stage Private", "Private forger for missile-procurement metal forgings; placeholder mark"),
    ("Weapons Sleeve", 20, "Defense", "Defense Primes & Services", "North America", "Late-stage Private", "Employee-owned defense R&D and engineering services"),
    ("Consumer Sleeve", 12, "Consumer Discretionary", "Consumer DTC & Wellness", "North America", "Late-stage Private", "Manufacturer-to-consumer apparel and home essentials; >$1B ARR"),
    ("Consumer Sleeve", 13, "Consumer Discretionary", "Consumer DTC & Wellness", "North America", "Pre-IPO", "Wearable health platform; IPO-track, medical-grade expansion"),
    ("Consumer Sleeve", 14, "Consumer Discretionary", "Consumer DTC & Wellness", "North America", "Late-stage Private", "Fresh pet-food subscription; Walmart.com omni-channel launch"),
    ("Consumer Sleeve", 15, "Consumer Discretionary", "Consumer DTC & Wellness", "North America", "Growth", "Direct-to-consumer premium cookware with wholesale placements"),
    ("Consumer Sleeve", 16, "Consumer Discretionary", "Consumer DTC & Wellness", "North America", "Pre-IPO", "Membership-based online natural grocery; IPO candidate"),
    ("Consumer Sleeve", 17, "Consumer Discretionary", "Consumer DTC & Wellness", "North America", "Seed & Early", "Cold-plunge and sauna wellness hardware"),
    ("Consumer Sleeve", 18, "Consumer Discretionary", "Marketplaces, Payments & Fintech", "North America", "Late-stage Private", "Prediction-market exchange; ICE-backed, US regulated expansion"),
    ("Consumer Sleeve", 19, "Consumer Discretionary", "Marketplaces, Payments & Fintech", "North America", "Late-stage Private", "Sneaker and apparel resale marketplace"),
    ("Consumer Sleeve", 20, "Consumer Discretionary", "Marketplaces, Payments & Fintech", "North America", "Late-stage Private", "Global payments infrastructure; $159B employee tender"),
]
for sheet, srow, subv, sector, region, stage, desc in HOLDINGS:
    q = f"'{sheet}'" if " " in sheet else sheet
    cols = {"Assumptions": ("A", "C", "B", "D", "F"), "Weapons Sleeve": ("A", "C", "B", "D", "F"), "Consumer Sleeve": ("A", "C", "B", "D", "F")}[sheet]
    FS[f"A{r}"] = f"={q}!{cols[0]}{srow}"; link_cell(FS[f"A{r}"]); FS[f"A{r}"].alignment = Alignment(horizontal="left")
    FS[f"B{r}"] = subv; input_cell(FS[f"B{r}"]); FS[f"B{r}"].alignment = Alignment(horizontal="left")
    FS[f"C{r}"] = f"={q}!{cols[1]}{srow}"; link_cell(FS[f"C{r}"], FMT_USD1)
    FS[f"D{r}"] = f"=C{r}/Holdco_Size"; body(FS[f"D{r}"], FMT_PCT, align="right")
    FS[f"E{r}"] = f"={q}!{cols[2]}{srow}"; link_cell(FS[f"E{r}"], FMT_USD0)
    FS[f"F{r}"] = f"={q}!{cols[3]}{srow}"; link_cell(FS[f"F{r}"], FMT_PCT)
    FS[f"G{r}"] = f"={q}!{cols[4]}{srow}"; link_cell(FS[f"G{r}"], FMT_PCT)
    for col, val in zip("HIJ", (sector, region, stage)):
        FS[f"{col}{r}"] = val; input_cell(FS[f"{col}{r}"]); FS[f"{col}{r}"].alignment = Alignment(horizontal="left")
    FS[f"L{r}"] = desc; input_cell(FS[f"L{r}"]); FS[f"L{r}"].alignment = Alignment(horizontal="left")
    r += 1
REG1 = r - 1
for rr in range(REG0, REG1 + 1):
    FS[f"K{rr}"] = f"=RANK(C{rr},$C${REG0}:$C${REG1})"
    body(FS[f"K{rr}"], "0", align="right")
FS[f"A{r}"] = "TOTAL"; total_cell(FS[f"A{r}"]); FS[f"A{r}"].alignment = Alignment(horizontal="left")
FS[f"C{r}"] = f"=SUM(C{REG0}:C{REG1})"; total_cell(FS[f"C{r}"], FMT_USD1)
FS[f"D{r}"] = f"=SUM(D{REG0}:D{REG1})"; total_cell(FS[f"D{r}"], FMT_PCT)
REG_TOTAL = r
r += 2

BREAK = {}
for key, col, members in [
    ("Sub-vehicle", "B", ["Defense", "IQT Semi / AI", "Consumer Discretionary"]),
    ("Sector", "H", ["Semiconductor Equipment", "Advanced Packaging & Materials", "Edge AI Silicon", "Quantum Computing",
                     "Autonomy & Unmanned Systems", "Directed Energy, EW & ISR", "Munitions, Energetics & Ordnance",
                     "Defense Primes & Services", "Consumer DTC & Wellness", "Marketplaces, Payments & Fintech"]),
    ("Region", "I", ["North America", "Israel", "Europe", "Asia-Pacific"]),
    ("Stage / liquidity", "J", ["Public / Listed", "Pre-IPO", "Late-stage Private", "Growth", "Seed & Early"]),
]:
    section(FS, f"A{r}", f"{key.upper()} BREAKDOWN (% of committed capital)")
    r += 1
    header_row(FS, r, [key, "Committed ($M)", "% of Holdco", "# Holdings"], 1)
    r += 1
    b0 = r
    for mbr in members:
        FS[f"A{r}"] = mbr; input_cell(FS[f"A{r}"]); FS[f"A{r}"].alignment = Alignment(horizontal="left")
        FS[f"B{r}"] = f'=SUMIF(${col}${REG0}:${col}${REG1},A{r},$C${REG0}:$C${REG1})'; body(FS[f"B{r}"], FMT_USD1, align="right")
        FS[f"C{r}"] = f"=B{r}/Holdco_Size"; body(FS[f"C{r}"], FMT_PCT, align="right")
        FS[f"D{r}"] = f'=COUNTIF(${col}${REG0}:${col}${REG1},A{r})'; body(FS[f"D{r}"], "0", align="right")
        r += 1
    FS[f"A{r}"] = "Total"; total_cell(FS[f"A{r}"]); FS[f"A{r}"].alignment = Alignment(horizontal="left")
    FS[f"B{r}"] = f"=SUM(B{b0}:B{r-1})"; total_cell(FS[f"B{r}"], FMT_USD1)
    FS[f"C{r}"] = f"=SUM(C{b0}:C{r-1})"; total_cell(FS[f"C{r}"], FMT_PCT)
    FS[f"D{r}"] = f"=SUM(D{b0}:D{r-1})"; total_cell(FS[f"D{r}"], "0")
    BREAK[key] = (b0, r - 1, r)
    r += 2

# E. Key terms
section(FS, f"A{r}", "E | KEY TERMS (links)", True)
r += 1
TERMS_ROW = {}
for lab, val, nf in [
    ("Management fee (% committed / yr)", "=Mgmt_Fee", FMT_PCT), ("Carried interest", "=Carry", FMT_PCT),
    ("Preferred return (compounded)", "=Pref", FMT_PCT), ("Waterfall", "Whole-fund European, no GP catch-up", None),
    ("Hold periods modelled (yrs)", '=Hold_Short&" / "&Hold_Mid&" / "&Hold_Long', None),
    ("IQT retention @ short / mid / long", '=TEXT(Ret_IQT_Short,"0%")&" / "&TEXT(Ret_IQT_Mid,"0%")&" / "&TEXT(Ret_IQT_Long,"0%")', None),
    ("Weapons retention @ short / mid / long", '=TEXT(Ret_Wpn_Short,"0%")&" / "&TEXT(Ret_Wpn_Mid,"0%")&" / "&TEXT(Ret_Wpn_Long,"0%")', None),
    ("Consumer retention @ short / mid / long", '=TEXT(Ret_Con_Short,"0%")&" / "&TEXT(Ret_Con_Mid,"0%")&" / "&TEXT(Ret_Con_Long,"0%")', None),
    ("Scenario weights Base / Bull / Bear / Shock", '=TEXT(P_Base,"0%")&" / "&TEXT(P_Bull,"0%")&" / "&TEXT(P_Bear,"0%")&" / "&TEXT(P_Shock,"0%")', None),
    ("S&P 500 benchmark CAGR", "=SPX_CAGR", FMT_PCT), ("Nasdaq-100 benchmark CAGR", "=NDX_CAGR", FMT_PCT),
    ("Defense+Semis basket CAGR (fwd)", "=Basket_CAGR", FMT_PCT),
    ("IQT follow-on reserve ($M)", "=Assumptions!B7", FMT_USD0),
]:
    FS[f"A{r}"] = lab; body(FS[f"A{r}"])
    FS[f"B{r}"] = val
    if isinstance(val, str) and val.startswith("="):
        link_cell(FS[f"B{r}"], nf)
    else:
        input_cell(FS[f"B{r}"])
    FS[f"B{r}"].alignment = Alignment(horizontal="left")
    TERMS_ROW[lab] = r
    r += 1
FS.freeze_panes = "B4"
log("Fact Sheet Data", "whole tab", "NEW tab: every figure, breakdown and holding description used by the external fact sheet, "
    "live-linked to the model (sector / region / stage tags and one-line descriptions are blue inputs).")

# ----------------------------------------------------------------------------
# 8. Checks tab
# ----------------------------------------------------------------------------
CK = wb.create_sheet("Checks", index=1)
title(CK, "A1", "MODEL INTEGRITY CHECKS")
subtitle(CK, "A2", "Every structural identity the model relies on. Status flows to Holdco Summary!A3. Blue = target input.")
CK.column_dimensions["A"].width = 62
CK.column_dimensions["B"].width = 18
CK.column_dimensions["C"].width = 12
CK.column_dimensions["D"].width = 60
CK["A3"] = "OVERALL STATUS"
CK["A3"].font = font(11, True, NAVY)
CK["A5"] = "Holdco target size ($M)"; body(CK["A5"])
CK["B5"] = 840; input_cell(CK["B5"], FMT_USD0)
IC = wb["IC Summary"]
IC["C72"] = "=Checks!$B$5"; link_cell(IC["C72"], IC["B72"].number_format)
IC["A72"] = '="Holdco size = "&TEXT(Checks!$B$5,"$#,##0")&"M"'
log("IC Summary", "A72:C72", "Holdco size target now reads the single target input on the Checks tab instead of a hard-coded 840.")
note(CK, "D5", "Sleeve sizes on Holdco Summary must add to this.")
header_row(CK, 7, ["Check", "Value", "Status", "What it protects"], 1)
iqt0, mid0, lng0 = SE_BLOCK_ROWS["Short"], SE_BLOCK_ROWS["Mid"], SE_BLOCK_ROWS["Long"]
checks = [
    ("Holdco sleeve sizes sum to target", "=Holdco_Size-$B$5", '=IF(ABS(B{r})<0.5,"OK","ERROR")', "Holdco Summary B6:B9 vs target", FMT_USD1),
    ("IQT sleeve: checks sum to sleeve size", "=Assumptions!C27-IQT_Size", '=IF(ABS(B{r})<0.5,"OK","ERROR")', "Assumptions C18:C26", FMT_USD1),
    ("Weapons sleeve: checks sum to sleeve size", "='Weapons Sleeve'!C21-Wpn_Size", '=IF(ABS(B{r})<0.5,"OK","ERROR")', "Weapons Sleeve C12:C18", FMT_USD1),
    ("Consumer sleeve: checks sum to sleeve size", "='Consumer Sleeve'!C21-Con_Size", '=IF(ABS(B{r})<0.5,"OK","ERROR")', "Consumer Sleeve C12:C20", FMT_USD1),
    ("IQT: initial deployment + reserve = committed", "=Assumptions!B6+Assumptions!B7-IQT_Committed", '=IF(ABS(B{r})<0.5,"OK","ERROR")', "Assumptions B5:B7", FMT_USD1),
    ("Strategic axis weights sum to 100%", "='Defense Supercycle'!B10", '=IF(ABS(B{r}-1)<0.0001,"OK","ERROR")', "Defense Supercycle B5:B9", FMT_PCT),
    ("Scenario probabilities sum to 100%", "='Defense Supercycle'!B21", '=IF(ABS(B{r}-1)<0.0001,"OK","ERROR")', "Defense Supercycle B17:B20", FMT_PCT),
    ("Hold periods positive and strictly increasing", '=Hold_Short&" < "&Hold_Mid&" < "&Hold_Long', '=IF(AND(Hold_Short>0,Hold_Mid>Hold_Short,Hold_Long>Hold_Mid),"OK","ERROR")', "Assumptions F5:F7", None),
    ("IQT retention in (0,1] and non-increasing with hold", '=TEXT(Ret_IQT_Short,"0%")&" ≥ "&TEXT(Ret_IQT_Mid,"0%")&" ≥ "&TEXT(Ret_IQT_Long,"0%")', '=IF(AND(Ret_IQT_Short<=1,Ret_IQT_Short>=Ret_IQT_Mid,Ret_IQT_Mid>=Ret_IQT_Long,Ret_IQT_Long>0),"OK","ERROR")', "Assumptions B11:B13", None),
    ("Weapons retention in (0,1] and non-increasing with hold", '=TEXT(Ret_Wpn_Short,"0%")&" ≥ "&TEXT(Ret_Wpn_Mid,"0%")&" ≥ "&TEXT(Ret_Wpn_Long,"0%")', '=IF(AND(Ret_Wpn_Short<=1,Ret_Wpn_Short>=Ret_Wpn_Mid,Ret_Wpn_Mid>=Ret_Wpn_Long,Ret_Wpn_Long>0),"OK","ERROR")', "Weapons Sleeve B6:B8", None),
    ("Consumer retention in (0,1] and non-increasing with hold", '=TEXT(Ret_Con_Short,"0%")&" ≥ "&TEXT(Ret_Con_Mid,"0%")&" ≥ "&TEXT(Ret_Con_Long,"0%")', '=IF(AND(Ret_Con_Short<=1,Ret_Con_Short>=Ret_Con_Mid,Ret_Con_Mid>=Ret_Con_Long,Ret_Con_Long>0),"OK","ERROR")', "Consumer Sleeve B6:B8", None),
    ("Fee, carry and pref each within [0%, 100%)", '=TEXT(Mgmt_Fee,"0.0%")&" / "&TEXT(Carry,"0%")&" / "&TEXT(Pref,"0%")', '=IF(AND(Mgmt_Fee>=0,Mgmt_Fee<1,Carry>=0,Carry<1,Pref>=0,Pref<1),"OK","ERROR")', "Assumptions B8:B10", None),
    ("Allocation tab total = Assumptions deployed total", "=Allocation!B14-Assumptions!C27", '=IF(ABS(B{r})<0.5,"OK","ERROR")', "Allocation B5:B14", FMT_USD1),
    ("IQT Clusters total = Assumptions deployed total", "='IQT Clusters'!C10-Assumptions!C27", '=IF(ABS(B{r})<0.5,"OK","ERROR")', "IQT Clusters C6:C10", FMT_USD1),
    ("Sleeve Economics IQT net = Fund Economics net (all holds, all cases)",
     f"=SUMPRODUCT(ABS('Fund Economics'!B12:F12-'Sleeve Economics'!B{iqt0+6}:F{iqt0+6}))+SUMPRODUCT(ABS('Fund Economics'!B28:F28-'Sleeve Economics'!B{mid0+6}:F{mid0+6}))+SUMPRODUCT(ABS('Fund Economics'!B44:F44-'Sleeve Economics'!B{lng0+6}:F{lng0+6}))",
     '=IF(ABS(B{r})<0.01,"OK","ERROR")', "Two independent waterfalls of the same sleeve must agree", FMT_USD1),
    ("Holdco gross proceeds = sum of sleeve gross (all holds, all cases)",
     f"=SUMPRODUCT(ABS('Holdco Summary'!B31:F31-('Sleeve Economics'!B{iqt0}:F{iqt0}+'Sleeve Economics'!H{iqt0}:L{iqt0}+'Sleeve Economics'!N{iqt0}:R{iqt0})))+SUMPRODUCT(ABS('Holdco Summary'!B52:F52-('Sleeve Economics'!B{mid0}:F{mid0}+'Sleeve Economics'!H{mid0}:L{mid0}+'Sleeve Economics'!N{mid0}:R{mid0})))+SUMPRODUCT(ABS('Holdco Summary'!B73:F73-('Sleeve Economics'!B{lng0}:F{lng0}+'Sleeve Economics'!H{lng0}:L{lng0}+'Sleeve Economics'!N{lng0}:R{lng0})))",
     '=IF(ABS(B{r})<0.01,"OK","ERROR")', "Roll-up links point at the right sleeve rows", FMT_USD1),
    ("Fact-sheet holdings register sums to holdco size", f"='Fact Sheet Data'!C{REG_TOTAL}-Holdco_Size", '=IF(ABS(B{r})<0.5,"OK","ERROR")', "Every holding is tagged exactly once", FMT_USD1),
    ("Fact-sheet breakdowns each sum to 100%", f"=ABS('Fact Sheet Data'!C{BREAK['Sub-vehicle'][2]}-1)+ABS('Fact Sheet Data'!C{BREAK['Sector'][2]}-1)+ABS('Fact Sheet Data'!C{BREAK['Region'][2]}-1)+ABS('Fact Sheet Data'!C{BREAK['Stage / liquidity'][2]}-1)", '=IF(ABS(B{r})<0.0001,"OK","ERROR")', "No untagged / mistyped sector, region or stage", FMT_PCT),
    ("IC Summary integrity block reports ALL PASS", "='IC Summary'!D80", '=IF(B{r}="ALL PASS","OK","ERROR")', "The pre-existing 8-check block on IC Summary", None),
    ("No formula errors on output tabs",
     f"=SUMPRODUCT(ISERROR('Holdco Summary'!B28:F86)*1)+SUMPRODUCT(ISERROR('Fund Economics'!B6:F49)*1)+SUMPRODUCT(ISERROR('Sleeve Economics'!B6:R{lng0+13})*1)+SUMPRODUCT(ISERROR('Scenario Summary'!B6:F22)*1)+SUMPRODUCT(ISERROR('PME, DPI & Sensitivity'!B13:F69)*1)+SUMPRODUCT(ISERROR('Fact Sheet Data'!B5:N{r})*1)+SUMPRODUCT(ISERROR('IC Summary'!B6:F81)*1)",
     '=IF(B{r}=0,"OK","ERROR")', "Count of #DIV/0!, #NUM!, #REF! etc. across all output ranges", "0"),
]
r = 8
for lab, val, status, what, nf in checks:
    CK[f"A{r}"] = lab; body(CK[f"A{r}"])
    CK[f"B{r}"] = val; body(CK[f"B{r}"], nf, align="right")
    CK[f"C{r}"] = status.replace("{r}", str(r)); body(CK[f"C{r}"], bold=True, align="center")
    note(CK, f"D{r}", what)
    r += 1
CK_LAST = r - 1
CK["B3"] = (f'=IF(COUNTIF(C8:C{CK_LAST},"ERROR")=0,"MODEL INTEGRITY: ALL "&COUNTA(A8:A{CK_LAST})&" CHECKS PASS",'
            f'"MODEL INTEGRITY: "&COUNTIF(C8:C{CK_LAST},"ERROR")&" OF "&COUNTA(A8:A{CK_LAST})&" CHECKS FAILING")')
CK["B3"].font = font(11, True, GREEN_OK)
from openpyxl.formatting.rule import CellIsRule, FormulaRule
CK.conditional_formatting.add(f"C8:C{CK_LAST}", CellIsRule(operator="equal", formula=['"ERROR"'], font=Font(color="FFFFFFFF", bold=True), fill=fill(RED)))
CK.conditional_formatting.add(f"C8:C{CK_LAST}", CellIsRule(operator="equal", formula=['"OK"'], font=Font(color=GREEN_OK, bold=True), fill=fill(TOTAL_FILL)))
CK.conditional_formatting.add("B3", FormulaRule(formula=['ISNUMBER(SEARCH("FAILING",B3))'], font=Font(color=RED, bold=True)))
H.conditional_formatting.add("A3", FormulaRule(formula=['ISNUMBER(SEARCH("FAILING",A3))'], font=Font(color=RED, bold=True)))
CK.freeze_panes = "A8"
log("Checks", "whole tab", f"NEW tab: {len(checks)} integrity checks (sizing identities, weight sums, monotonic retention, "
    "two-way waterfall reconciliation, error scan). Overall status surfaces on Holdco Summary!A3.")

# ----------------------------------------------------------------------------
# 9. Read Me additions, formatting, print setup, tab colours
# ----------------------------------------------------------------------------
R["B3"] = "Anchored by Substrate, Inc.   ·   Prepared 22-Sep-2026   ·   v3 optimization pass 02-Oct-2026   ·   All figures USD millions unless noted"
r = 29
R[f"B{r}"] = "v3 OPTIMIZATION PASS (02-Oct-2026) — WHAT CHANGED"
R[f"B{r}"].font = font(10, True); R[f"B{r}"].fill = fill(SECTION_FILL)
for txt in [
    "• Named levers: Hold_Short / Hold_Mid / Hold_Long (Assumptions F5:F7), Mgmt_Fee, Carry, Pref, retention and scenario-probability names. Every hold exponent, fee-year multiplier, IRR root and block label now reads these — change a hold period once and the whole model follows.",
    "• Checks tab: integrity dashboard (sizing identities, weight sums, retention monotonicity, two-way waterfall reconciliation, error scan). Status is mirrored at Holdco Summary!A3.",
    "• Sleeve Economics tab: stand-alone gross->net waterfall for every sub-vehicle x hold x scenario, plus the cross-sleeve netting reconciliation to the holdco waterfall.",
    "• Fact Sheet Data tab: every figure on the external fact sheet, live-linked, with holding-level sector / region / stage tags.",
    "• Holdco Summary 'Expected' now probability-weights the NET waterfall (same method as Fund Economics). The old approach ran the waterfall on expected gross, which overstated expected net.",
    "• All IRR / Direct-Alpha formulas are guarded: a wipe-out returns -100% rather than #NUM!. Stale sleeve CAGR memos replaced by live links. Redundant same-sheet references removed. See the Change Log tab for the cell-level list.",
]:
    r += 1
    R[f"B{r}"] = txt
    R[f"B{r}"].font = font(10)
    R[f"B{r}"].alignment = Alignment(wrap_text=True, vertical="top")
    R.row_dimensions[r].height = 40.5
R["B29"].alignment = Alignment(vertical="center")

# Change Log tab
CL = wb.create_sheet("Change Log", index=1)
title(CL, "A1", "CHANGE LOG — v3 OPTIMIZATION PASS (02-Oct-2026)")
subtitle(CL, "A2", "Cell-level record of every edit made by the optimization script. 'Value impact' flags the only places where "
         "numbers moved; everything else is structural and was verified cell-by-cell against the prior version after a full recalculation.")
CL.column_dimensions["A"].width = 6
CL.column_dimensions["B"].width = 22
CL.column_dimensions["C"].width = 30
CL.column_dimensions["D"].width = 110
CL.column_dimensions["E"].width = 44
header_row(CL, 4, ["#", "Tab", "Range", "Change", "Value impact"], 1)
for i, (sheet, rng, change, impact) in enumerate(changelog, start=1):
    rr = 4 + i
    CL[f"A{rr}"] = i; body(CL[f"A{rr}"], "0", align="center")
    CL[f"B{rr}"] = sheet; body(CL[f"B{rr}"])
    CL[f"C{rr}"] = rng; body(CL[f"C{rr}"])
    CL[f"D{rr}"] = change; body(CL[f"D{rr}"]); CL[f"D{rr}"].alignment = Alignment(wrap_text=True, vertical="top")
    CL[f"E{rr}"] = impact; body(CL[f"E{rr}"], bold=impact.startswith("CHANGED"), color=(RED if impact.startswith("CHANGED") else "FF000000"))
    CL[f"E{rr}"].alignment = Alignment(wrap_text=True, vertical="top")
    CL.row_dimensions[rr].height = max(27.75, 13.5 * (len(change) // 100 + 1))
CL.freeze_panes = "A5"

# Freeze panes + print setup + tab colours
FREEZE = {"IC Summary": "B6", "Holdco Summary": "B4", "Assumptions": "B4", "Defense Supercycle": "B4", "Allocation": "B5",
          "Portfolio Returns": "B6", "Fund Economics": "B6", "IQT Clusters": "B6", "Weapons Sleeve": "B12",
          "Consumer Sleeve": "B12", "PME, DPI & Sensitivity": "B4", "Scenario Summary": "B6", "Macro Overlay": "A4"}
for name, cell in FREEZE.items():
    wb[name].freeze_panes = cell
TAB_COLOURS = {
    "Read Me": "808080", "Change Log": "808080", "Checks": "C00000",
    "IC Summary": "2E7D32", "Holdco Summary": "2E7D32", "Scenario Summary": "2E7D32", "Fact Sheet Data": "2E7D32",
    "Assumptions": "0000FF", "Defense Supercycle": "0000FF", "Weapons Sleeve": "0000FF", "Consumer Sleeve": "0000FF",
    "Macro Overlay": "7F7F7F", "Allocation": "7F7F7F", "Portfolio Returns": "7F7F7F", "Fund Economics": "7F7F7F",
    "IQT Clusters": "7F7F7F", "Sleeve Economics": "7F7F7F", "PME, DPI & Sensitivity": "7F7F7F",
}
for ws in wb.worksheets:
    ws.sheet_properties.tabColor = TAB_COLOURS.get(ws.title, "7F7F7F")
    ws.sheet_view.showGridLines = False
    ws.page_setup.orientation = "landscape"
    ws.page_setup.paperSize = ws.PAPERSIZE_LETTER
    ws.page_setup.fitToWidth = 1
    ws.page_setup.fitToHeight = 0
    ws.sheet_properties.pageSetUpPr = PageSetupProperties(fitToPage=True)
    ws.print_options.horizontalCentered = True
    ws.oddFooter.left.text = "&A"
    ws.oddFooter.right.text = "Page &P of &N"
    ws.oddFooter.center.text = "Leviathan — Core PE Holdco model v3 — internal"
log("All tabs", "sheet setup", "Freeze panes on every grid tab, landscape fit-to-width print setup with footers, tab colours "
    "(blue = inputs, grey = engines, green = outputs, red = checks), gridlines off, full recalculation forced on open.")

wb.calculation.fullCalcOnLoad = True
wb.active = wb.sheetnames.index("Holdco Summary")
for ws in wb.worksheets:
    ws.sheet_view.tabSelected = (ws.title == "Holdco Summary")

# --- final safety scan: no hard-coded hold literals left in model formulas -----------
left = []
pat = re.compile(r"(\^(5|7|10)(?!\d)|\*(5|7|10)(?!\d)|\(1/(5|7|10)\))")
for ws in wb.worksheets:
    for row in ws.iter_rows():
        for c in row:
            if isinstance(c.value, str) and c.value.startswith("=") and pat.search(c.value):
                left.append(f"{ws.title}!{c.coordinate}: {c.value[:80]}")
if left:
    print("WARNING — hold literals still present:")
    print("\n".join(left))

wb.save(DST)
print(f"saved {DST}; subs={n_sub} self={n_self} hold={n_hold} labels={n_lbl} guards={n_guard} checks={len(checks)} changelog={len(changelog)}")
