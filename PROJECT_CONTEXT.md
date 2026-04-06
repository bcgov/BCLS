# Project Context

**What This Project Is**
A BC dashboard workspace with multiple standalone dashboards and a parent shell (`BC Dashboard Hub`) that embeds them.

**Current Goal**
Stabilize two active surfaces:
- `life_sciences` sector dashboard UX/data flow
- `bc_dashboard_hub` embedding/navigation behavior

**Stack**
- Frontend: standalone HTML/CSS/JS dashboards (Chart.js)
- Data: dashboard-specific Excel files + some live StatsCan usage in macro
- Local server: `scripts/serve.py`

**Architecture Summary**
- Hub: `C:/Users/smehd/BCLS/dashboards/bc_dashboard_hub/html/dashboard.html`
- Life Sciences: `C:/Users/smehd/BCLS/dashboards/sectors/life_sciences/html/dashboard.html`
- Workbook/template:
  - `.../life_sciences/data/Life_Sciences_light.xlsx`
  - `.../life_sciences/data/Life_Sciences_light_template.xlsx`

**Key Constraints**
- Child dashboards remain independently editable; hub embeds via iframe.
- Life Sciences charts are sector-level in current UX.
- Display toggles are local-cache only (no Excel writes).
- Environment: `rg.exe` unreliable (`Access is denied`), use PowerShell/Python search.

**Conventions**
- Keep edits minimal and scoped to target dashboard.
- Do not edit `archive/` unless intentionally restoring history.
- Validate UI behavior in browser after each change.

**Important Files**
- `C:/Users/smehd/BCLS/dashboards/sectors/life_sciences/html/dashboard.html`
- `C:/Users/smehd/BCLS/dashboards/bc_dashboard_hub/html/dashboard.html`
- `C:/Users/smehd/BCLS/dashboards/sectors/life_sciences/data/create_excel.py`
- `C:/Users/smehd/BCLS/HANDOFF.md`
- `C:/Users/smehd/BCLS/TASKS.md`

**Current Status**
- Life Sciences: subsector section removed from active flow; KPIs + charts centralized in sector trends; local display selectors added; footer removed.
- Hub: footer removed; nav labels simplified; dropdown header duplication removed; iframe auto-height logic added to reduce nested scrolling.

**Top Next Steps**
- Smoke-test Life Sciences + Hub end-to-end using local server.
- Finalize workbook migration while workbook file is unlocked.
- Clean residual encoding artifacts and prune dead code paths.
