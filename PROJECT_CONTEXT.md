# Project Context

**What This Project Is**
A BC dashboard workspace with multiple standalone dashboards and a parent shell (`BC Dashboard Hub`) that embeds them.

**Current Goal**
Stabilize local runtime + user handoff for Windows:
- reliable local server start (`scripts/serve.py`)
- simple non-technical launch flow (`BC_Dashboard_App.bat`)
- maintain Hub + Life Sciences UX polish

**Stack**
- Frontend: standalone HTML/CSS/JS dashboards (Chart.js)
- Data: dashboard-specific Excel files + some live StatsCan usage in macro
- Local server/proxy: `scripts/serve.py`

**Architecture Summary**
- Hub: `C:/Users/smehd/BCLS/dashboard/hub/html/dashboard.html`
- Life Sciences: `C:/Users/smehd/BCLS/dashboard/sectors/life_sciences/html/dashboard.html`
- Life Sciences workbook (single source): `.../life_sciences/data/Life_Sciences_light.xlsx`
- Windows distribution artifacts:
  - `C:/Users/smehd/BCLS/BC_Dashboard_App.bat`
  - `C:/Users/smehd/BCLS/INSTALLATION_INSTRUCTION.md`
  - `C:/Users/smehd/BCLS/scripts/package_windows_zip.ps1`
  - `C:/Users/smehd/BCLS/dist/BCLS_Dashboard_App.zip`

**Key Constraints**
- Child dashboards remain independently editable; hub embeds via iframe.
- Life Sciences charts are sector-level in current UX.
- Life Sciences data is strict Excel single-source (no legacy fallback workbook).
- Display toggles are local-cache only (no Excel writes).
- Environment: `rg.exe` unreliable (`Access is denied`), use PowerShell/Python search.

**Conventions**
- Keep edits minimal and scoped to target dashboard.
- Do not edit `archive/` unless intentionally restoring history.
- Validate UI behavior in browser after each change.

**Important Files**
- `C:/Users/smehd/BCLS/dashboard/sectors/life_sciences/html/dashboard.html`
- `C:/Users/smehd/BCLS/dashboard/hub/html/dashboard.html`
- `C:/Users/smehd/BCLS/scripts/serve.py`
- `C:/Users/smehd/BCLS/BC_Dashboard_App.bat`
- `C:/Users/smehd/BCLS/HANDOFF.md`
- `C:/Users/smehd/BCLS/TASKS.md`

**Current Status**
- Life Sciences: top-box cleanup done; subtitle encoding artifacts fixed; strict single-workbook mode applied.
- Hub sectors page: 4-column card layout, `Last updated`/`Coming Soon` footer text, no top counters.
- Runtime: `serve.py` auto-selects available port; `launch_dashboard_hub.bat` replaced by `BC_Dashboard_App.bat` as the single app entrypoint.

**Top Next Steps**
- Validate packaged ZIP on a clean Windows laptop.
- Verify `Update Data` reliability via `scripts/serve.py` path.
- Continue residual encoding cleanup where still visible.
