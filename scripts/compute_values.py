#!/usr/bin/env python3
"""Evaluate every formula in an xlsx with the pure-Python `formulas` engine and dump {Sheet!Cell: value} JSON.
Usage: compute_values.py <model.xlsx> <values.json>"""
import sys, re, json, formulas
from openpyxl import load_workbook
fn, out = sys.argv[1], sys.argv[2]
names = {ws.title.upper(): ws.title for ws in load_workbook(fn, read_only=True).worksheets}
sol = formulas.ExcelModel().loads(fn).finish().calculate()
vals = {}
for k, v in sol.items():
    m = re.match(r"'?\[[^\]]+\]([^'!]+)'?!([A-Z]+\d+)$", str(k))
    if not m: continue
    val = v.value[0][0] if hasattr(v, "value") else v
    vals[f"{names.get(m.group(1), m.group(1))}!{m.group(2)}"] = val if isinstance(val, (int, float, str)) else str(val)
json.dump(vals, open(out, "w"))
print("computed", len(vals), "cells ->", out)
