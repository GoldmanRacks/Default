"""Fact-card theme (BXPE July 2026 fact card): Source Sans 3 (for Guardian Sans), Playfair Display (for Sanomat), black header bars,
#E4E4E4 zebra rows, rust #A95228 stat figures and links, teal chart family, HIGHLY CONFIDENTIAL running header, disclosure clauses."""
import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_JUSTIFY, TA_RIGHT, TA_LEFT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame, NextPageTemplate, Paragraph as _P, Spacer, Table, TableStyle,
                                PageBreak, KeepTogether, HRFlowable)
from reportlab.graphics.shapes import Drawing, Rect, String
from reportlab.graphics.charts.piecharts import Pie

FD = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fonts")
for n in ["SourceSans3-Light","SourceSans3-Regular","SourceSans3-Medium","SourceSans3-Semibold","SourceSans3-Bold",
          "SourceSans3-Italic-Regular","SourceSans3-Italic-Semibold","PlayfairDisplay-Regular","PlayfairDisplay-Semibold","PlayfairDisplay-Bold"]:
    pdfmetrics.registerFont(TTFont(n, os.path.join(FD, n+".ttf")))
pdfmetrics.registerFont(TTFont("DejaVuSans", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"))
pdfmetrics.registerFontFamily("SourceSans3", normal="SourceSans3-Regular", bold="SourceSans3-Semibold", italic="SourceSans3-Italic-Regular", boldItalic="SourceSans3-Italic-Semibold")
pdfmetrics.registerFontFamily("SourceSans3-Light", normal="SourceSans3-Light", bold="SourceSans3-Semibold", italic="SourceSans3-Italic-Regular", boldItalic="SourceSans3-Italic-Semibold")
pdfmetrics.registerFontFamily("PlayfairDisplay", normal="PlayfairDisplay-Regular", bold="PlayfairDisplay-Semibold", italic="PlayfairDisplay-Regular", boldItalic="PlayfairDisplay-Bold")

BLACK=colors.HexColor("#000000"); WHITE=colors.white; RUST=colors.HexColor("#A95228"); GRAYTXT=colors.HexColor("#4D4D4D")
GRAYCAP=colors.HexColor("#737373"); ZEBRA=colors.HexColor("#E4E4E4"); RULE=colors.HexColor("#BFBFBF")
CHART=["#4C9F8B","#1B5E5C","#C39D78","#006492","#BFBFBF","#A5CD24","#A5CFC5"]   # fact-card chart family, fixed order

PAGE_W, PAGE_H = letter
ML = MR = 0.6*inch; MB = 0.72*inch
USABLE = PAGE_W - ML - MR

BODY  = ParagraphStyle('fc-body',  fontName='SourceSans3-Regular', fontSize=9.5, leading=12.3, textColor=BLACK, spaceAfter=5, alignment=TA_LEFT)
INTRO = ParagraphStyle('fc-intro', fontName='SourceSans3-Light',   fontSize=11.5, leading=15, textColor=BLACK, spaceAfter=8)
DATE  = ParagraphStyle('fc-date',  fontName='SourceSans3-Semibold',fontSize=9, leading=11, textColor=BLACK, spaceAfter=2)
TITLE = ParagraphStyle('fc-title', fontName='PlayfairDisplay-Semibold', fontSize=25, leading=29, textColor=BLACK, spaceAfter=6)
H1    = ParagraphStyle('fc-h1',    fontName='PlayfairDisplay-Semibold', fontSize=14.5, leading=18, textColor=BLACK, spaceBefore=12, spaceAfter=2, keepWithNext=1)
SUB   = ParagraphStyle('fc-sub',   fontName='SourceSans3-Light', fontSize=9.5, leading=12, textColor=BLACK, spaceAfter=5, keepWithNext=1)
H2    = ParagraphStyle('fc-h2',    fontName='SourceSans3-Semibold', fontSize=10.5, leading=13, textColor=BLACK, spaceBefore=8, spaceAfter=3, keepWithNext=1)
NOTE  = ParagraphStyle('fc-note',  fontName='SourceSans3-Regular', fontSize=7.5, leading=9.4, textColor=GRAYTXT, alignment=TA_JUSTIFY, spaceAfter=3)
SM    = NOTE
BL    = ParagraphStyle('fc-bl',    parent=BODY, leftIndent=13, bulletIndent=2, spaceAfter=3, bulletFontName='DejaVuSans', bulletFontSize=6, bulletColor=RUST)
EN    = ParagraphStyle('fc-en', fontName='SourceSans3-Regular', fontSize=8.5, leading=11, textColor=BLACK, leftIndent=18, firstLineIndent=-18, spaceAfter=3)
META  = ParagraphStyle('fc-meta',  fontName='PlayfairDisplay-Regular', fontSize=8.5, leading=10, textColor=BLACK)
STATN = ParagraphStyle('fc-statn', fontName='PlayfairDisplay-Semibold', fontSize=28, leading=30, textColor=RUST)
STATL = ParagraphStyle('fc-statl', fontName='SourceSans3-Regular', fontSize=10, leading=12, textColor=BLACK)
STATS = ParagraphStyle('fc-stats', fontName='SourceSans3-Regular', fontSize=8, leading=10, textColor=BLACK)
CAPS  = ParagraphStyle('fc-caps',  fontName='SourceSans3-Regular', fontSize=7.3, leading=9, textColor=GRAYCAP, alignment=TA_RIGHT)

def Paragraph(text, style=BODY, **kw):
    return _P(text.replace("P&L","P&amp;L").replace("<a ", '<a color="#A95228" '), style, **kw)
def defined(term, article="the"): return f'({article} &#8220;{term}&#8221;)'
def h1(title, note=None): return Paragraph(title + (f"<super><font size=8>({note})</font></super>" if note else ""), H1)
def sub(text): return Paragraph(text, SUB)
def h2(title): return Paragraph(title, H2)
def bullets(items): return [Paragraph(t, BL, bulletText='▪') for t in items]
def note(text): return [HRFlowable(width="100%", thickness=0.5, color=RULE, spaceBefore=6, spaceAfter=3), Paragraph(text, NOTE)]
def rule(th=0.5, col=RULE, before=4, after=4): return HRFlowable(width="100%", thickness=th, color=col, spaceBefore=before, spaceAfter=after)

def stats(items):
    """items: [(big, label, sublabel)] x3 -> fact-card stat row."""
    cells=[]
    for big,lab,sl in items:
        cells.append([Paragraph(big, STATN), Paragraph(lab, STATL), Paragraph(sl or "", STATS)])
    data=[[c[0] for c in cells],[c[1] for c in cells],[c[2] for c in cells]]
    w=USABLE/len(items)
    t=Table(data, colWidths=[w]*len(items))
    t.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),0),('RIGHTPADDING',(0,0),(-1,-1),10),
                           ('TOPPADDING',(0,0),(-1,-1),1),('BOTTOMPADDING',(0,0),(-1,-1),1),('LINEBELOW',(0,-1),(-1,-1),0.6,RULE),('BOTTOMPADDING',(0,-1),(-1,-1),8)]))
    return t

def tbl(data, widths, bold_last=False, font=8.3, first_col_medium=True):
    widths=[w*inch for w in widths]; total=sum(widths)
    if total>USABLE: widths=[w*USABLE/total for w in widths]
    t=Table(data, colWidths=widths, repeatRows=1)
    st=[('FONT',(0,0),(-1,-1),'SourceSans3-Regular',font),('FONT',(0,0),(-1,0),'SourceSans3-Semibold',font),
        ('BACKGROUND',(0,0),(-1,0),BLACK),('TEXTCOLOR',(0,0),(-1,0),WHITE),('TEXTCOLOR',(0,1),(-1,-1),BLACK),
        ('VALIGN',(0,0),(-1,-1),'MIDDLE'),('ALIGN',(1,1),(-1,-1),'RIGHT'),('ALIGN',(1,0),(-1,0),'RIGHT'),
        ('TOPPADDING',(0,0),(-1,-1),3.2),('BOTTOMPADDING',(0,0),(-1,-1),3.2),('LEFTPADDING',(0,0),(-1,-1),4),('RIGHTPADDING',(0,0),(-1,-1),4),
        ('LINEBELOW',(0,-1),(-1,-1),0.75,BLACK)]
    if first_col_medium: st.append(('FONT',(0,1),(0,-1),'SourceSans3-Medium',font))
    for i in range(2,len(data),2): st.append(('BACKGROUND',(0,i),(-1,i),ZEBRA))
    if bold_last: st.append(('FONT',(0,-1),(-1,-1),'SourceSans3-Semibold',font))
    t.setStyle(TableStyle(st)); return t

def pie(labels, values, width=2.9*inch, height=2.2*inch):
    if len(values)>5: height=2.9*inch
    d=Drawing(width,height); p=Pie()
    p.x=width*0.30; p.y=height*0.12; p.width=p.height=min(width*0.42, height*0.76)
    p.data=values; p.labels=[f"{l} {v:.0f}%" for l,v in zip(labels,values)]
    p.sideLabels=1; p.simpleLabels=0; p.slices.strokeColor=WHITE; p.slices.strokeWidth=1.5
    p.slices.fontName="SourceSans3-Semibold"; p.slices.fontSize=7.5; p.slices.label_pointer_strokeColor=GRAYTXT; p.slices.label_pointer_piePad=4
    p.slices.label_pointer_elbowLength=8; p.sideLabelsOffset=0.12
    for i in range(len(values)): p.slices[i].fillColor=colors.HexColor(CHART[i%len(CHART)])
    d.add(p); return d

BANNER=("THIS IS A MODELING COMMUNICATION. PLEASE REFER TO THE ENDNOTES AND IMPORTANT DISCLOSURE INFORMATION BEFORE ACTING ON ANY FIGURE HEREIN. "
        "PREPARED SOLELY FOR DONALD B. RITTS III. FOR THE RECIPIENT'S USE ONLY. NOT FOR DISTRIBUTION TO ANY OTHER PERSON OR THE GENERAL PUBLIC.")

def make_doc(path, short, doc_id, update_label, title):
    def footer(c, doc):
        c.setFont("SourceSans3-Regular", 7.5); c.setFillColor(BLACK)
        c.drawString(ML, 0.48*inch, update_label)
        c.drawRightString(PAGE_W-MR, 0.48*inch, f"Mythos   |   {doc.page}")
    def first(c, doc):
        c.saveState()
        c.setFillColor(BLACK); c.rect(ML, PAGE_H-1.22*inch, 1.75*inch, 0.56*inch, stroke=0, fill=1)
        c.setFillColor(WHITE); c.setFont("PlayfairDisplay-Semibold", 21); c.drawCentredString(ML+0.875*inch, PAGE_H-1.05*inch, "Mythos")
        pw=4.9*inch; par=_P(BANNER, CAPS); w,h=par.wrap(pw, 2*inch); par.drawOn(c, PAGE_W-MR-pw, PAGE_H-0.28*inch-h)
        c.setFillColor(BLACK); c.setFont("PlayfairDisplay-Regular", 16); c.drawRightString(PAGE_W-MR, PAGE_H-1.18*inch, short)
        c.setLineWidth(3); c.setStrokeColor(BLACK); c.line(ML, PAGE_H-1.36*inch, PAGE_W-MR, PAGE_H-1.36*inch)
        footer(c, doc); c.setFont("PlayfairDisplay-Regular", 8.5); c.drawRightString(PAGE_W-MR, 0.32*inch, doc_id)
        c.restoreState()
    def later(c, doc):
        c.saveState()
        c.setFillColor(GRAYCAP); c.setFont("SourceSans3-Regular", 9.5); c.drawRightString(PAGE_W-MR, PAGE_H-0.5*inch, "H I G H L Y   C O N F I D E N T I A L   &   T R A D E   S E C R E T")
        c.setLineWidth(3); c.setStrokeColor(BLACK); c.line(ML, PAGE_H-0.8*inch, PAGE_W-MR, PAGE_H-0.8*inch)
        footer(c, doc); c.restoreState()
    f1=Frame(ML, MB, USABLE, PAGE_H-1.5*inch-MB, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, id='f1')
    f2=Frame(ML, MB, USABLE, PAGE_H-0.95*inch-MB, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, id='f2')
    doc=BaseDocTemplate(path, pagesize=letter, title=title, author="Mythos", leftMargin=ML, rightMargin=MR, topMargin=0.95*inch, bottomMargin=MB)
    doc.addPageTemplates([PageTemplate(id='first', frames=[f1], onPage=first), PageTemplate(id='later', frames=[f2], onPage=later)])
    return doc

def title_block(date_caps, title, intro):
    return [NextPageTemplate('later'), Paragraph(date_caps, DATE), Paragraph(title, TITLE), Paragraph(intro, INTRO)]

PAST_PERF = ("<b>Past performance does not predict future returns.</b> This sleeve is subject to the risk of capital loss and the premium paid may be lost in full. "
             "The modeled figures presented herein are hypothetical, are provided for illustrative purposes only and are not a forecast of any outcome.")

def disclosure(doc_type, sponsor, recipient, extra=None):
    S=[h1("Important Disclosure Information")]
    paras=[
     f"This material is not to be reproduced or distributed to any other persons (other than professional advisors of the persons receiving this material) and is intended solely for the use of the "
     f"persons to whom it has been delivered, being {recipient}.",
     f"The sole purpose of this material is to inform, and it in no way is intended to attract any funds or deposits. The instruments mentioned may not be appropriate for all investors. "
     f"Any position discussed herein should be entered only after the recipient has reviewed the current option chain, the live quotes and the applicable risk disclosure for listed options.",
     "Short-dated long options are speculative, carry a high degree of risk, and are appropriate only for investors who are willing to put the entire premium at risk over a defined period. "
     "They are subject to time decay, changes in implied volatility and liquidity constraints at exit.",
     f"<b>Proprietary Data.</b> The source of information in this communication is Interactive Brokers market data as quoted on the date stated, the {sponsor} pricing model and the {sponsor} backtest "
     f"unless otherwise stated. While {sponsor} currently believes that such information is reliable for the purposes used herein, it is subject to change, and no representations are made as to its "
     f"accuracy or completeness.",
     f"<b>Estimates / Targets.</b> Any scenario values, breakevens, hit rates or similar predictions or returns set forth herein are based on assumptions and assessments made by {sponsor} that it considers "
     f"reasonable under the circumstances as of the date hereof. They are necessarily speculative, hypothetical, and inherently uncertain in nature, and it can be expected that some or all of the "
     f"assumptions underlying them will not materialize and/or that actual events and consequences thereof will vary materially from the assumptions upon which they have been based. Among the "
     f"assumptions to be made by {sponsor} in performing its analysis are (i) the entry price equal to the quoted mid, (ii) no change in implied volatility between entry and exit, (iii) the exit mark "
     f"at four days to expiry, and (iv) the uniform spot moves of the scenario ladder. None of {sponsor}, its affiliates or any of their respective officers makes any assurance, representation or "
     f"warranty as to the accuracy of such assumptions. Recipients are cautioned not to place undue reliance on these forward-looking statements.",
    ]
    if extra: paras += extra
    for t in paras: S.append(Paragraph(t, NOTE))
    return S
