import re
"""Minimal styling kit reproducing the D. B. Ritts III investment-profile deck look."""
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.oxml.ns import qn

NAVY = RGBColor(0x14, 0x24, 0x4A)
TEAL = RGBColor(0x1F, 0x5E, 0x5B)
BURG = RGBColor(0x8B, 0x1E, 0x2B)
GOLD = RGBColor(0xB8, 0x8A, 0x3E)
INK = RGBColor(0x26, 0x2B, 0x33)
MUTED = RGBColor(0x5F, 0x66, 0x70)
LINE = RGBColor(0xC9, 0xCC, 0xD1)
PANEL = RGBColor(0xF5, 0xF4, 0xF0)
PALE = RGBColor(0xE8, 0xEC, 0xF3)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
GREY = RGBColor(0x8A, 0x8F, 0x96)

SERIF = "Georgia"
SANS = "Calibri"
FOOTER = "D. B. Ritts III — PE Investment Profile"


def new_deck():
    p = Presentation()
    p.slide_width = Inches(13.333)
    p.slide_height = Inches(7.5)
    return p


def blank(p):
    return p.slides.add_slide(p.slide_layouts[6])


def rect(s, x, y, w, h, fill=None, line=None, lw=0.75, shape=MSO_SHAPE.RECTANGLE):
    sh = s.shapes.add_shape(shape, Inches(x), Inches(y), Inches(w), Inches(h))
    if fill is None:
        sh.fill.background()
    else:
        sh.fill.solid(); sh.fill.fore_color.rgb = fill
    if line is None:
        sh.line.fill.background()
    else:
        sh.line.color.rgb = line; sh.line.width = Pt(lw)
    st = sh._element.find(qn("p:style"))
    if st is not None:
        sh._element.remove(st)
    sh.text_frame.text = ""
    return sh


def txt(s, x, y, w, h, content, size=10, color=INK, bold=False, font=SANS, align="l",
        anchor="t", italic=False, spacing=None, margin=0.04, line_spacing=None):
    """content: str | list of paragraphs; paragraph = str | list of runs; run = (text, {opts})."""
    tb = s.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = Inches(margin)
    tf.margin_top = tf.margin_bottom = Inches(0.02)
    tf.vertical_anchor = {"t": MSO_ANCHOR.TOP, "m": MSO_ANCHOR.MIDDLE, "b": MSO_ANCHOR.BOTTOM}[anchor]
    paras = content if isinstance(content, list) else [content]
    for i, para in enumerate(paras):
        pg = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        pg.alignment = {"l": PP_ALIGN.LEFT, "c": PP_ALIGN.CENTER, "r": PP_ALIGN.RIGHT}[align]
        if line_spacing:
            pg.line_spacing = line_spacing
        if spacing is not None:
            pg.space_after = Pt(spacing)
        runs = para if isinstance(para, list) else [(para, {})]
        for r in runs:
            if isinstance(r, str):
                r = (r, {})
            t, o = r
            run = pg.add_run(); run.text = t
            f = run.font
            f.size = Pt(o.get("size", size)); f.bold = o.get("bold", bold)
            f.italic = o.get("italic", italic); f.name = o.get("font", font)
            f.color.rgb = o.get("color", color)
            if o.get("caps"):
                rPr = run._r.get_or_add_rPr(); rPr.set("cap", "all")
            if o.get("track"):
                run._r.get_or_add_rPr().set("spc", str(o["track"]))
    return tb


def bullets(s, x, y, w, h, items, size=9.5, color=INK, bullet="•", spacing=3, bold_lead=True):
    paras = []
    for it in items:
        if isinstance(it, tuple):
            lead, rest = it
            paras.append([(f"{bullet} ", {"color": NAVY}), (lead, {"bold": True}), (rest, {})])
        else:
            paras.append([(f"{bullet} ", {"color": NAVY}), (it, {})])
    return txt(s, x, y, w, h, paras, size=size, color=color, spacing=spacing)


def fit_title(title, max_size=30, width_pt=880.0, em=0.6):
    return max(20, min(max_size, int(width_pt / (len(title) * em))))


def header(s, section, title, title_size=30):
    title_size = fit_title(title, title_size)
    section = re.sub(r"^\d+\s*\|\s*", "", section)
    txt(s, 0.5, 0.28, 12.3, 0.3, [[(section, {"caps": True, "track": 150})]], size=10, color=MUTED)
    txt(s, 0.5, 0.55, 12.4, 0.75, title, size=title_size, color=NAVY, font=SERIF)
    rect(s, 0.5, 1.27, 12.33, 0.012, fill=LINE)
    rect(s, 0.5, 7.0, 12.33, 0.008, fill=LINE)
    txt(s, 0.5, 7.05, 6, 0.25, FOOTER, size=8, color=GREY)


def reorder(p, order):
    """order: list of 1-based creation indices in desired final order."""
    lst = p.slides._sldIdLst
    ids = list(lst)
    for e in ids:
        lst.remove(e)
    for i in order:
        lst.append(ids[i - 1])


def stamp_pages(p, skip_first=True):
    for i, s in enumerate(p.slides, 1):
        if skip_first and i == 1:
            continue
        page_no(s, i)


def page_no(s, n):
    txt(s, 12.0, 7.05, 0.83, 0.25, str(n), size=8, color=GREY, align="r")


def band(s, x, y, w, h, text, fill=NAVY, color=WHITE, size=10, align="c", font=SANS, bold=True, caps=True):
    rect(s, x, y, w, h, fill=fill)
    txt(s, x + 0.05, y, w - 0.1, h, [[(text, {"caps": caps, "track": 80 if caps else 0})]], size=size,
        color=color, bold=bold, align=align, anchor="m", font=font)


def num(s, x, y, n, d=0.32, fill=NAVY, color=WHITE, size=11):
    c = rect(s, x, y, d, d, fill=fill, shape=MSO_SHAPE.OVAL)
    txt(s, x, y, d, d, str(n), size=size, color=color, bold=True, align="c", anchor="m", margin=0)
    return c


def arrow(s, x, y, w=0.22, h=0.16, fill=NAVY):
    return rect(s, x, y, w, h, fill=fill, shape=MSO_SHAPE.RIGHT_ARROW)


def table(s, x, y, w, h, data, col_w=None, hdr_fill=NAVY, size=9, hdr_size=9, first_bold=True,
          zebra=True, align=None, row_h=None):
    rows, cols = len(data), len(data[0])
    gt = s.shapes.add_table(rows, cols, Inches(x), Inches(y), Inches(w), Inches(h))
    tbl = gt.table
    tblPr = tbl._tbl.tblPr
    # remove default style banding look
    style = tblPr.find(qn("a:tableStyleId"))
    if style is not None:
        style.text = "{5940675A-B579-460E-94D1-54222C63F5DA}"  # No Style, Table Grid
    if col_w:
        tot = sum(col_w)
        for i, cw in enumerate(col_w):
            tbl.columns[i].width = Inches(w * cw / tot)
    for r in range(rows):
        if row_h:
            tbl.rows[r].height = Inches(row_h)
        for c in range(cols):
            cell = tbl.cell(r, c)
            val = data[r][c]
            cell.margin_left = cell.margin_right = Inches(0.06)
            cell.margin_top = cell.margin_bottom = Inches(0.03)
            cell.vertical_anchor = MSO_ANCHOR.MIDDLE
            tf = cell.text_frame; tf.word_wrap = True
            opts = {}
            if isinstance(val, tuple):
                val, opts = val
            tf.text = ""
            pg = tf.paragraphs[0]
            a = (align[c] if align else ("l" if c == 0 else "c"))
            pg.alignment = {"l": PP_ALIGN.LEFT, "c": PP_ALIGN.CENTER, "r": PP_ALIGN.RIGHT}[a]
            run = pg.add_run(); run.text = str(val)
            f = run.font; f.name = SANS
            if r == 0:
                f.size = Pt(hdr_size); f.bold = True; f.color.rgb = WHITE
                cell.fill.solid(); cell.fill.fore_color.rgb = hdr_fill
                run._r.get_or_add_rPr().set("cap", "all")
            else:
                f.size = Pt(opts.get("size", size))
                f.bold = opts.get("bold", first_bold and c == 0)
                f.color.rgb = opts.get("color", INK)
                fill = opts.get("fill", PANEL if (zebra and r % 2 == 0) else WHITE)
                cell.fill.solid(); cell.fill.fore_color.rgb = fill
    return tbl
