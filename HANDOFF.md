# Handoff

**Date**
2026-04-02

**Recent Meaningful Changes**
- Restructured the repo around standalone dashboards under `dashboards/`.
- Created the parent dashboard `BC Dashboard Hub` in `dashboards/bc_dashboard_hub/html/dashboard.html`.
- Copied the legacy BC macroeconomy dashboard into `dashboards/bc_macroeconomy/html/dashboard.html`.
- Copied the legacy Life Sciences dashboard into `dashboards/sectors/life_sciences/html/dashboard.html`.
- Added placeholder standalone dashboards for Look West, Projects, and the remaining sector folders.
- Moved old root work into `archive/restructure_2026-04-02/root_working_state/`.
- Updated the macroeconomy dashboard employment KPIs to: Employment, Unemployment Rate, Labour Force (each with MoM + YoY deltas).
- Changed the macro “Employment — British Columbia” chart to a combined chart: Employment + Labour Force lines (left axis) and Unemployed bars (right axis, 0–500k).
- Removed/hid legacy headers and yellow “mock/sample” ribbons in child dashboards where they interfered with embedding (macro + Life Sciences).
- Updated `scripts/serve.py` to serve UTF-8 for HTML/CSS/JS/JSON and to print ASCII-safe status lines.
- Added an “industry movers” table to the macroeconomy dashboard (top 5 job gainers + bottom 5 job losers by MoM employment change) with a month selector and gainer/loser row styling.

**Files Touched**
- `C:/Users/smehd/BCLS/dashboards/bc_dashboard_hub/html/dashboard.html`
- `C:/Users/smehd/BCLS/scripts/serve.py`
- `C:/Users/smehd/BCLS/README.md`
- `C:/Users/smehd/BCLS/dashboards/look_west_strategy/html/dashboard.html`
- `C:/Users/smehd/BCLS/dashboards/projects/html/dashboard.html`
- `C:/Users/smehd/BCLS/dashboards/sectors/*/html/dashboard.html`
- `C:/Users/smehd/BCLS/dashboards/bc_macroeconomy/html/dashboard.html`
- `C:/Users/smehd/BCLS/dashboards/sectors/life_sciences/html/dashboard.html`

**Unresolved Issues**
- The root folder still contains `data/00_reference` because it was locked by another process during archive cleanup. (Confirmed)
- The final names of sector 9 and sector 10 are not yet specified, so `future_sector_01` and `future_sector_02` are temporary placeholders. (Uncertain)
- The parent hub still contains legacy unused macro script blocks internally; they are no longer initialized, but the file could be trimmed later. (Confirmed)
- `rg.exe` fails with “Access is denied” in this environment; use PowerShell `Select-String` for searches instead. (Confirmed)
- Macro industry movers table uses hardcoded StatsCan industry vector IDs (table `14-10-0355-01`) rather than discovering vectors from WDS cube metadata at runtime. (Confirmed)

**Next Recommended Step**
Run `python C:/Users/smehd/BCLS/scripts/serve.py` and verify:
- `http://localhost:8080/dashboards/bc_dashboard_hub/html/dashboard.html`
- `http://localhost:8080/dashboards/bc_macroeconomy/html/dashboard.html`
- `http://localhost:8080/dashboards/sectors/life_sciences/html/dashboard.html`
Then validate macro employment behavior:
- Click `Update Data` and confirm KPI cards + the Employment/Labour Force/Unemployed chart populate correctly.
- Confirm the industry movers table populates, defaults to the most recent month, and the month selector works.

**Warnings**
- Do not edit files under `archive/` unless you are intentionally restoring from history.
- The parent hub assumes each child dashboard keeps its entry point at `html/dashboard.html`.
- Macro live updates require HTTP (not `file://`) due to browser fetch restrictions.
