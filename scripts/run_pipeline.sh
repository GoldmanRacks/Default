#!/usr/bin/env bash
# Rebuild the optimized model and the fact sheet from the original workbook.
#   bash scripts/run_pipeline.sh models/<original>.xlsx
# Requires: python3 + openpyxl + formulas (pip), node + playwright with Chromium.
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"; ORIG="$1"; TMP="$(mktemp -d)"
python3 "$HERE/optimize_model.py" "$ORIG" "$TMP/model_v3.xlsx"
python3 "$HERE/compute_values.py" "$TMP/model_v3.xlsx" "$TMP/values.json"
python3 "$HERE/inject_cached_values.py" "$TMP/model_v3.xlsx" "$TMP/values.json" "$HERE/../models/Leviathan_PE_HOLDCO_Model_IC_VFinal_v3_Optimized_Letalis.xlsx"
python3 "$HERE/build_factsheet.py" "$HERE/../models/Leviathan_PE_HOLDCO_Model_IC_VFinal_v3_Optimized_Letalis.xlsx" "$HERE/../factsheet" "$HERE/fonts"
