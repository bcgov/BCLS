# Handoff

**Date**
2026-04-08

**What Changed**
- Life Sciences dashboard:
  - Removed top-box `LIVE DASHBOARD` / `DATA: ...` display lines via render-time cleanup.
  - Replaced subtitle `?` artifacts in chart defaults with clean separators.
  - Switched to strict single workbook source (`Life_Sciences_light.xlsx`) and removed legacy fallback.
- Life Sciences data cleanup:
  - Removed unused files (`Life_Sciences.xlsx`, `Life_Sciences_light_template.xlsx`, launcher pycache under `scripts`).
- BC Dashboard Hub (Sectors page):
  - Sector cards now render 4 per row (desktop).
  - Replaced `Live/Planned + Open` card footer with `Last updated: ...` / `Coming Soon`.
  - Removed top summary counters (`Live`, `Planned`, `Total`).
  - Updated file:// update-data prompt to point to `python scripts/serve.py` and hub URL.
- Runtime/distribution:
  - `scripts/serve.py` now auto-selects port (`8080`, `8081`, `8090`, fallback any free port) to avoid WinError 10048.
  - Added Windows handoff package assets:
    - `BC_Dashboard_App.bat`
    - `INSTALL_WINDOWS_ONE_PAGE.md`
    - `scripts/package_windows_zip.ps1`
    - built `dist/BCLS_Dashboard_App.zip`
  - Removed launcher stack per user direction (kept simple `serve.py` flow):
    - deleted `run_dashboard_launcher.bat`
    - deleted `scripts/dashboard_launcher.py`
    - deleted `scripts/build_dashboard_launcher_exe.ps1`
    - deleted `launch_dashboard_hub.bat`

**Files Touched**
- `C:/Users/smehd/BCLS/dashboards/sectors/life_sciences/html/dashboard.html`
- `C:/Users/smehd/BCLS/dashboards/sectors/life_sciences/docs/README.md`
- `C:/Users/smehd/BCLS/dashboards/bc_dashboard_hub/html/dashboard.html`
- `C:/Users/smehd/BCLS/scripts/serve.py`
- `C:/Users/smehd/BCLS/BC_Dashboard_App.bat` (new)
- `C:/Users/smehd/BCLS/INSTALL_WINDOWS_ONE_PAGE.md` (new)
- `C:/Users/smehd/BCLS/scripts/package_windows_zip.ps1` (new)
- `C:/Users/smehd/BCLS/archive/stage_2026-04-08_pre_single_window_launcher/*` (snapshot backup)

**Unresolved Issues**
- StatCan proxy via removed launcher path is no longer relevant; current validated path is `python scripts/serve.py`.
- Some legacy text encoding artifacts may still exist in older comments/labels.
- `rg.exe` remains unavailable (`Access is denied`) in this shell.

**Next Recommended Step**
- On a clean Windows machine, validate `dist/BCLS_Dashboard_App.zip` end-to-end using `BC_Dashboard_App.bat`.
- Confirm `scripts/serve.py` printed port matches browser URL and `Update Data` succeeds.
- If distribution is stable, freeze package naming/versioning (e.g., date-stamped zip).

**Warnings**
- `scripts/serve.py` now includes multiple networking fallbacks; avoid broad refactor without regression test of `Update Data`.
- Hub and macro update flow are coupled to local proxy endpoints (`/api/statcan-wds`, `/api/statcan-csv`).
