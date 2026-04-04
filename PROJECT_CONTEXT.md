# Project Context

**What This Project Is**
A BC economic dashboard workspace: multiple standalone dashboards plus a parent hub (`BC Dashboard Hub`) that embeds child dashboards.

**Current Goal**
Finalize the macro dashboard UX/data behavior, then bring other child dashboards (Look West, Projects, sectors) up to the same maturity.

**Stack**
- Frontend: standalone HTML/CSS/JS dashboards (Chart.js)
- Data: dashboard-specific Excel files + live StatsCan API/table pulls
- Local server: `scripts/serve.py`

**Architecture Summary**
- Hub entry: `C:/Users/smehd/BCLS/dashboards/bc_dashboard_hub/html/dashboard.html`
- Macro child: `C:/Users/smehd/BCLS/dashboards/bc_macroeconomy/html/dashboard.html`
- Other children: `dashboards/look_west_strategy/`, `dashboards/projects/`, `dashboards/sectors/*/`
- Legacy history: `archive/`

**Key Constraints**
- Child dashboards stay independently editable; hub embeds rather than reimplements.
- Entry point convention remains `html/dashboard.html`.
- Several non-macro dashboards are still placeholders pending workbook/content inputs.
- Environment constraint: `rg.exe` not reliable (`Access is denied`) in current shell context.

**Conventions**
- Keep edits minimal and local to target dashboard.
- Use repo-relative stable paths; avoid touching `archive/` unless restoring.
- Verify visual/data behavior in browser after every macro change.

**Important Files**
- `C:/Users/smehd/BCLS/dashboards/bc_macroeconomy/html/dashboard.html`
- `C:/Users/smehd/BCLS/dashboards/bc_dashboard_hub/html/dashboard.html`
- `C:/Users/smehd/BCLS/scripts/serve.py`
- `C:/Users/smehd/BCLS/HANDOFF.md`
- `C:/Users/smehd/BCLS/TASKS.md`

**Current Status**
- Macro dashboard is actively developed and now includes:
  - Expanded KPI set/order and unit formatting
  - GDP/GDP-share, employment/labour, CPI, CPI-contribution, and trade charts
  - Industry movers table
  - Clickable StatCan dataset links from chart source tags
  - Fixed y-axis ranges for trade charts
- Hub structure is stable; non-macro dashboards still need substantive build-out.

**Top Next Steps**
- Run macro QA pass (layout, units, chart ranges, source links, update flow).
- Normalize remaining text encoding artifacts in UI strings.
- Implement real data/content for Look West, Projects, and remaining sectors.
