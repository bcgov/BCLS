# Handoff

**Date**
2026-04-03

**What Changed**
- Reworked `life_sciences` dashboard structure:
  - Removed subsector section/tabs from active page flow.
  - Moved KPIs into `Sector Trends` (above charts), with subsector tags per card.
  - Kept charts sector-level (`ALL`) and added local cached show/hide controls: `Select KPIs`, `Select Charts`, `Select Goals`.
  - Integrated subsector definitions into top sector definition box as inline text.
  - Removed life sciences footer.
- Extended Excel-driven chart model in life sciences:
  - `CHART_CATALOG` support for chart order/visibility/title/subtitle/caveat/data sheet.
  - Per-chart sheet mapping support (`DATA_*`) with legacy fallback.
- Updated Dashboard Hub UX:
  - Removed hub footer.
  - Simplified nav labels (removed icons from Macro/Look West/Sectors/Projects tab labels).
  - Removed duplicate `BC Industry Sectors` dropdown headers.
  - Added iframe auto-height fit + `scrolling="no"` to reduce nested scrollbars.

**Files Touched**
- `C:/Users/smehd/BCLS/dashboards/sectors/life_sciences/html/dashboard.html`
- `C:/Users/smehd/BCLS/dashboards/sectors/life_sciences/data/create_excel.py`
- `C:/Users/smehd/BCLS/dashboards/sectors/life_sciences/docs/README.md`
- `C:/Users/smehd/BCLS/dashboards/bc_dashboard_hub/html/dashboard.html`
- `C:/Users/smehd/BCLS/dashboards/sectors/life_sciences/data/Life_Sciences_light_template.xlsx` (new template)

**Unresolved Issues**
- `Life_Sciences_light.xlsx` may be file-locked when open in Excel; migration/write can fail until closed.
- Some legacy encoding artifacts still exist in older HTML comments/labels.
- `rg.exe` remains unavailable (`Access is denied`) in this shell; use `Select-String`/Python.

**Next Recommended Step**
- Run `python C:/Users/smehd/BCLS/scripts/serve.py`.
- Smoke test:
  - `http://localhost:8080/dashboards/sectors/life_sciences/html/dashboard.html`
  - `http://localhost:8080/dashboards/bc_dashboard_hub/html/dashboard.html`
- Verify:
  - Life sciences: section order, `Select ...` toggles persistence, no footer.
  - Hub: no footer, cleaned nav labels, reduced double-scroll behavior in macro embed.

**Warnings**
- `life_sciences/html/dashboard.html` has many iterative edits; avoid broad refactor without visual regression pass.
- Hub dropdown/nav and iframe sizing logic are behavior-coupled; test macro + sectors + strategy tabs after edits.
