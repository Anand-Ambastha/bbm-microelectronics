import json, os, copy
from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.text.paragraph import Paragraph
from docx.table import Table
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.enum.text import WD_ALIGN_PARAGRAPH
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
RES, FIG = os.path.join(ROOT, 'results'), os.path.join(ROOT, 'figures')
S = json.load(open(os.path.join(RES, 'summary.json'))); O = json.load(open(os.path.join(RES, 'summary_opt.json')))
FONT = 'Times New Roman'

class Cur:
    """insertion cursor: everything is inserted AFTER the current element"""
    def __init__(self, el, parent): self.el, self.parent = el, parent
    def _p(self):
        p = OxmlElement('w:p'); self.el.addnext(p); self.el = p; return Paragraph(p, self.parent)
    def para(self, text='', bold=False, italic=False, size=10, indent=0.0, align=None, after=3, color=None, mono=False):
        p = self._p(); pf = p.paragraph_format; pf.space_after = Pt(after); pf.space_before = Pt(0)
        if indent: pf.left_indent = Inches(indent)
        if align == 'c': p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        elif align == 'j': p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        self.runs(p, text, bold, italic, size, color, mono); return p
    def runs(self, p, text, bold=False, italic=False, size=10, color=None, mono=False):
        # **bold** inline markup
        parts = [text.replace('**', '')]
        for i, t in enumerate(parts):
            if not t: continue
            r = p.add_run(t); r.bold = bold; r.italic = italic; r.font.size = Pt(size)
            r.font.name = 'Consolas' if mono else FONT
            if color: r.font.color.rgb = RGBColor(*color)
    def bullet(self, text, size=10, indent=0.25): return self.para('\u2022  ' + text, size=size, indent=indent, align='j')
    def eq(self, text, num=''): 
        p = self.para(text + ('        ' + num if num else ''), italic=True, size=10.5, align='c', after=4); return p
    def image(self, path, width=6.0, caption=''):
        p = self._p(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER; p.paragraph_format.space_after = Pt(2); p.paragraph_format.keep_with_next = True
        p.add_run().add_picture(path, width=Inches(width))
        if caption: self.para(caption, italic=True, size=8.5, align='c', after=6)
    def table(self, rows, widths=None, size=8, header=True, shade='D9E2F3'):
        t = Document().add_table(rows=len(rows), cols=len(rows[0]))   # build detached then move
        tbl = t._tbl; self.el.addnext(tbl); self.el = tbl
        T = Table(tbl, self.parent)
        pr = tbl.tblPr; b = OxmlElement('w:tblBorders')
        for e in ('top', 'left', 'bottom', 'right', 'insideH', 'insideV'):
            x = OxmlElement('w:' + e); x.set(qn('w:val'), 'single'); x.set(qn('w:sz'), '4'); x.set(qn('w:color'), '808080'); b.append(x)
        pr.append(b)
        for i, row in enumerate(rows):
            for j, v in enumerate(row):
                c = T.cell(i, j); c.text = ''; p = c.paragraphs[0]; p.paragraph_format.space_after = Pt(0)
                self.runs(p, str(v), bold=(header and i == 0), size=size)
                if header and i == 0:
                    sh = OxmlElement('w:shd'); sh.set(qn('w:val'), 'clear'); sh.set(qn('w:fill'), shade); c._tc.get_or_add_tcPr().append(sh)
                if widths: c.width = Inches(widths[j])
        self.para('', size=4, after=2); return T

def fill_after_label(p, text):
    """template line 'Label: ______' -> keep bold label run, replace underscores"""
    for r in p.runs[1:]: r.text = ''
    r = p.runs[0] if len(p.runs) == 1 else p.add_run()
    r2 = p.add_run(' ' + text); r2.font.size = Pt(10.5); r2.font.name = FONT
def set_blank(p, text, size=10.5, bold=False, align=None):
    for r in p.runs: r.text = ''
    parts = [text.replace('**', '')]
    for i, t in enumerate(parts):
        if not t: continue
        r = p.add_run(t); r.font.size = Pt(size); r.font.name = FONT; r.bold = bold
    if align == 'j': p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY

# ---- sizing bookkeeping (nm) ----
BASE = dict(conv=dict(wp1=220, lp1=370, wn1=220, ln1=880, wp2=880, lp2=730, wn2=1050, ln2=1320),
            bbm=dict(wp1=220, lp1=740, wn1=390, ln1=180, wpt=220, lpt=350, wnf=220, lnf=950, wp2=220, lp2=180, wn2=220, ln2=220))
UNIT = (860*180 + 220*180)
def area_um2(kind, p):
    """gate-area proxy: sum(W*L) of all transistors incl. both unit inverters, in um^2 (NOT layout area)"""
    q = dict(BASE['conv' if kind == 'conventional' else 'bbm']); q.update(p)
    a = 2*UNIT + q['wp1']*q['lp1'] + q['wn1']*q['ln1'] + q['wp2']*q['lp2'] + q['wn2']*q['ln2']
    if kind == 'bbm': a += q['wpt']*q['lpt'] + q['wnf']*q['lnf']
    return a*1e-6
def pct(ref, new): return 100.0*(ref-new)/ref
CITE = 'Puhan, J., Raič, D., Tuma, T., & Bűrmen, Á. (2014). Break-before-Make CMOS Inverter for Power-Efficient Delay Implementation. The Scientific World Journal, 2014, Article ID 349131, 11 pp. doi:10.1155/2014/349131.'
