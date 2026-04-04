# Handoff

**Date**
2026-04-03

**Recent Meaningful Changes**
- Continued iterative refinement of `dashboards/bc_macroeconomy/html/dashboard.html`.
- Added/updated macro cards and chart behavior:
  - GDP line chart (2010+; current vs chained toggle).
  - GDP share by industry chart.
  - CPI contribution stacked+line chart for BC (last 2 years).
  - Interprovincial and international trade charts.
  - Industry movers table (BC, recent period selection, gainers/losers formatting).
- Added dataset-code hyperlinks in chart source tags (`.ds-tag`) to open StatCan table pages in a new tab.
- Updated KPI behavior and layout:
  - KPI order set to: GDP, Inflation, Employment, Unemployment, Labour Force.
  - Employment and Labour Force KPI values now display in millions.
- Applied UI/chrome updates:
  - Removed footer content.
  - Kept update controls in macro hero (right side).
  - Added thin bottom ribbon styled like the macro hero color treatment.
- Set fixed axis ranges for trade charts:
  - Interprovincial: left 10–40, right -20–20 ($B).
  - International: left 50–100, right -40–20 ($B).

**Files Touched**
- `C:/Users/smehd/BCLS/dashboards/bc_macroeconomy/html/dashboard.html`

**Unresolved Issues**
- Some text still appears with encoding artifacts (`â€”`, `?` replacing punctuation in some contexts). Needs UTF-8 normalization pass. (Confirmed)
- `rg.exe` is not usable in this environment (`Access is denied`); use PowerShell `Select-String`/Python for search/edit workflows. (Confirmed)
- Look West, Projects, and most sector dashboards are still placeholders; only macro is heavily developed in this cycle. (Confirmed)

**Next Recommended Step**
Run `python C:/Users/smehd/BCLS/scripts/serve.py` and smoke-test:
- `http://localhost:8080/dashboards/bc_macroeconomy/html/dashboard.html`

Validate specifically:
- KPI order and units (Employment/Labour Force in M).
- StatCan dataset links open correct table pages in new tab.
- Trade chart axis bounds match specified ranges.
- Bottom ribbon rendering and overall page layout on desktop/mobile.

**Warnings**
- `dashboard.html` has many rapid iterative edits; avoid broad refactors before a visual regression pass.
- Keep changes in active dashboards only; do not edit `archive/` unless intentionally restoring history.
