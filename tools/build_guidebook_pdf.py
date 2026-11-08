"""Render a guidebook Markdown file as a designed PDF
(Fund Communications Design System v2, marketing register).

Cover text, header label, doc ID, output name and endnotes come from the
Markdown front matter (one `key: value` per line; `kf` and `note` repeat).

Usage:
  python3 tools/build_guidebook_pdf.py                      # Guide #1
  python3 tools/build_guidebook_pdf.py guides/03_....md     # any guidebook
"""
import os, re, subprocess, json, html, sys
import markdown

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SRC = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else os.path.join(ROOT, "guides", "01_Investment_Selection_Guidebook.md")

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

EXTRA_CSS = """
.lead2 { font-size:11.5pt; line-height:1.4; font-weight:300; margin:2pt 0 12pt; }
.habits { display:grid; grid-template-columns:1fr 1fr; gap:6pt 14pt; margin:6pt 0 12pt; }
.hb { border-top:1px solid #BFBFBF; padding-top:5pt; font-size:8.6pt; line-height:1.38; break-inside:avoid; }
.hb span { display:block; font-family:'Source Serif 4',Georgia,serif; font-weight:600; font-size:13pt; line-height:1; margin-bottom:3pt; }
.case { border-top:3px solid #000; background:#F4F4F2; padding:9pt 12pt 4pt; margin:6pt 0 12pt; break-inside:avoid; }
.case p { font-size:9pt; margin:0 0 6pt; }
.case-tag { font-size:8pt; font-weight:500; letter-spacing:.05em; text-transform:uppercase; margin-bottom:5pt; }
.two .case { margin-top:0; }
.track5 { display:grid; grid-template-columns:repeat(5,1fr); gap:4pt; margin:6pt 0 10pt; }
.st { border-top:3px solid #1B5E5C; background:#F4F4F2; padding:6pt 7pt; font-size:8pt; line-height:1.3; break-inside:avoid; }
.st b { display:block; font-size:8.6pt; margin-bottom:2pt; }
.st.dark { border-top-color:#000; }
.toc { columns:2; column-gap:20pt; font-size:9pt; margin:6pt 0 0; padding:0; list-style:none; }
.toc li { display:flex; gap:8pt; border-bottom:1px solid #E4E4E4; padding:4pt 0; break-inside:avoid; }
.toc li span { color:#727272; font-weight:500; width:16pt; }
.keep { break-after:avoid; }
.sec-head + * , h3 + * { break-before:avoid; }
h3 { break-after:avoid; }
.pull { font-family:'Source Serif 4',Georgia,serif; font-weight:600; font-size:14pt; line-height:1.3; border-top:1px solid #000; border-bottom:1px solid #000; padding:10pt 0; margin:4pt 0 16pt; }
"""


def esc(s): return html.escape(s, quote=False)

raw = open(SRC, encoding="utf-8").read()
fm_match = re.match(r"^---\n(.*?)\n---\s*", raw, flags=re.S)
meta = {}
for line in (fm_match.group(1).splitlines() if fm_match else []):
    if ":" in line:
        k, v = line.split(":", 1)
        meta.setdefault(k.strip(), []).append(v.strip())
M = lambda k, d="": meta.get(k, [d])[0]
src = raw[fm_match.end():] if fm_match else raw
OUT_STEM = M("out", "Guidebook")
HTML_OUT = os.path.join(ROOT, "guides", OUT_STEM + ".html")
PDF_OUT = os.path.join(ROOT, "guides", OUT_STEM + ".pdf")
DOC_ID = M("doc_id", "LEVIATHAN-GB")
src = src.replace("▸", '<span class="xref">▸</span>')
md = markdown.Markdown(extensions=["tables"])

sections = []
for part in re.split(r"^## ", src, flags=re.M)[1:]:
    head, body = part.split("\n", 1)
    m = re.match(r"(\d+)\.\s+(.*)", head.strip())
    sections.append((int(m.group(1)), m.group(2), body.strip()))

FLOW_ALL = M("flow", "no").lower() == "yes"
BREAKS = {int(x) for x in M("break_before", "").replace(" ", "").split(",") if x}
out = []
for n, title, body in sections:
    md.reset()
    h = md.convert(body)
    if M("keep_tables", "no").lower() == "yes":
        h = re.sub(r"<table>(.*?)</table>", lambda m: ('<table style="break-inside:avoid">' if m.group(1).count("<tr>") <= 15 else "<table>") + m.group(1) + "</table>", h, flags=re.S)
    cls = "sec flow" if FLOW_ALL and n not in BREAKS else "sec"
    head = f'<div class="sec-head"><span class="n">{n:02d}</span><h2>{esc(title)}</h2></div>'
    if M("keep_tables", "no").lower() == "yes":
        # bind each h3 to the content through its first short table
        h = re.sub(r'(<h3>(?:(?!<h3>).)*?<table style="break-inside:avoid">.*?</table>)', r'<div style="break-inside:avoid">\1</div>', h, flags=re.S)
        # bind the section heading + intro + first short table (if it comes before any h3)
        m1 = re.search(r'<table style="break-inside:avoid">.*?</table>', h, flags=re.S)
        if m1 and "<h3>" not in h[:m1.start()] and '<div style="break-inside:avoid">' not in h[:m1.start()]:
            h = f'<div style="break-inside:avoid">{head}{h[:m1.end()]}</div>{h[m1.end():]}'
            head = ""
    out.append(f'<section class="{cls}">{head}{h}</section>')

toc = "".join(f"<li><span>{n:02d}</span>{esc(t)}</li>" for n, t, _ in sections)
kfs = "".join(f'<div class="kf"><div class="v">{v.split("|",1)[0]}</div><div class="l">{v.split("|",1)[1]}</div></div>' for v in meta.get("kf", []))
COVER = f"""<section>
<div class="rule-ink" style="margin-top:0"></div>
<div class="eyebrow">{M("eyebrow")}</div>
<h1 class="title">{M("title_html")}</h1>
<p class="lead">{M("lead_html")}</p>
<div class="keyfigs" style="grid-template-columns:repeat({max(len(meta.get("kf", [])), 1)},1fr)">{kfs}</div>
<div class="pull">{M("pull")}</div>
<div class="eyebrow" style="margin-bottom:2pt">Contents</div>
<ul class="toc">{toc}</ul>
</section>"""

notes = "".join(f"<li>{n}</li>" for n in meta.get("note", []))
DISC = f"""<div class="disc-box">INTERNAL REFERENCE ONLY. NOT AN OFFER, A SOLICITATION OR INVESTMENT ADVICE. NOT FOR LP OR EXTERNAL DISTRIBUTION.</div>
<p style="font-size:8pt"><b>Note:</b> {M("closing_note", "Model figures are estimated and unaudited.")}</p>"""
if notes:
    NOTES = f"""<section class="sec flow notes"><div class="sec-head"><span class="n">Notes</span><h2>Sources and endnotes</h2></div><ol>{notes}</ol>{DISC}</section>"""
else:
    NOTES = f"""<div style="break-inside:avoid;margin-top:14pt">{DISC}</div>"""

doc = f"""<!DOCTYPE html><html><head><meta charset="utf-8"><title>{M("html_title", "Guidebook")}</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Public+Sans:wght@300;400;500;600&family=Source+Serif+4:opsz,wght@8..60,400;8..60,600&display=swap" rel="stylesheet">
<style>{CSS}{EXTRA_CSS}</style></head><body>{COVER}{''.join(out)}{NOTES}</body></html>"""
open(HTML_OUT, "w", encoding="utf-8").write(doc)

HEADER = f"""<div style="width:100%;font-family:Helvetica,Arial,sans-serif;font-size:7px;letter-spacing:.05em;text-transform:uppercase;padding:0 0.7in;display:flex;justify-content:space-between;color:#000;">
<span style="font-weight:600">{M("header_name", "D. B. Ritts III")} · {M("header_label", "Guidebook")}</span><span>{M("header_right", "Confidential — internal reference · not for LP distribution")}</span></div>"""
FOOTER = f"""<div style="width:100%;font-family:Helvetica,Arial,sans-serif;font-size:7px;padding:0 0.7in;color:#000;">
<div style="border-top:1px solid #000;padding-top:4px;display:flex;justify-content:space-between;align-items:baseline;">
<span style="font-weight:600">Model figures are estimated and unaudited. Not investment advice.</span>
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
