#!/usr/bin/env python3
"""Write computed values (from the Python `formulas` engine) into an openpyxl-written xlsx as
cached <v> values, so previewers / pandas / data_only loads see numbers while every formula stays intact.
Usage: inject_cached_values.py <in.xlsx> <values.json> <out.xlsx>
"""
import json, re, sys, zipfile
from xml.sax.saxutils import escape

src, vals_json, dst = sys.argv[1:4]
vals = json.load(open(vals_json))

zin = zipfile.ZipFile(src)
wbxml = zin.read("xl/workbook.xml").decode()
rels = zin.read("xl/_rels/workbook.xml.rels").decode()
rid_target = dict(re.findall(r'<Relationship[^>]*Id="([^"]+)"[^>]*Target="([^"]+)"', rels))
rid_target.update({a: b for b, a in re.findall(r'<Relationship[^>]*Target="([^"]+)"[^>]*Id="([^"]+)"', rels)})
sheets = {}
for m in re.finditer(r'<sheet [^>]*name="([^"]+)"[^>]*r:id="([^"]+)"', wbxml):
    name = m.group(1).replace("&amp;", "&").replace("&quot;", '"').replace("&apos;", "'")
    tgt = rid_target[m.group(2)]
    sheets["xl/" + tgt.lstrip("/").replace("xl/", "", 1) if not tgt.startswith("/") else tgt.lstrip("/")] = name

cell_re = re.compile(r'<c r="([A-Z]+\d+)"([^>]*)><f>(.*?)</f><v\s*/>(</c>)', re.S)
stats = {"num": 0, "str": 0, "bool": 0, "err": 0, "missing": 0}

def repl(sheet):
    def _r(m):
        ref, attrs, f, close = m.groups()
        v = vals.get(f"{sheet}!{ref}")
        attrs = re.sub(r'\s+t="[^"]*"', "", attrs)
        if v is None:
            stats["missing"] += 1
            return m.group(0)
        if isinstance(v, bool):
            stats["bool"] += 1
            return f'<c r="{ref}"{attrs} t="b"><f>{f}</f><v>{int(v)}</v>{close}'
        if isinstance(v, (int, float)):
            stats["num"] += 1
            return f'<c r="{ref}"{attrs}><f>{f}</f><v>{repr(float(v)) if isinstance(v, float) else v}</v>{close}'
        s = str(v)
        if s.startswith("#"):
            stats["err"] += 1
            return f'<c r="{ref}"{attrs} t="e"><f>{f}</f><v>{escape(s)}</v>{close}'
        stats["str"] += 1
        return f'<c r="{ref}"{attrs} t="str"><f>{f}</f><v>{escape(s)}</v>{close}'
    return _r

zout = zipfile.ZipFile(dst, "w", zipfile.ZIP_DEFLATED)
for item in zin.infolist():
    data = zin.read(item.filename)
    if item.filename in sheets:
        data = cell_re.sub(repl(sheets[item.filename]), data.decode()).encode()
    zout.writestr(item, data)
zout.close()
print("injected cached values:", stats)
